"""
extract_pose_features.py

Batches frames by video, processes frames in parallel (one thread per frame),
downloads from Hugging Face, runs Mediapipe Pose, and commits annotated frames 
in a single commit per video using huggingface_hub's create_commit, 
storing pose features in pose_data.db.
"""

import os
import sys
import cv2
import mediapipe as mp
import sqlite3
import logging
import tempfile
import shutil
import requests
import concurrent.futures

from collections import defaultdict
from huggingface_hub import HfApi, hf_hub_url, CommitOperationAdd
from pose_data_setup import initialize_pose_data, insert_pose_feature

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KICK_DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'kick_data.db')

VIDEO_REPO_ID = "urdof7/penalty-kick-data"
FRAMES_FOLDER = "frames"               # frames on HF
ANNOTATED_FRAMES_FOLDER = "annotated-frames"
api = HfApi()

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def get_kick_data_connection():
    return sqlite3.connect(KICK_DB_PATH)

def download_frame_from_hf(hf_filename, local_path):
    url = hf_hub_url(repo_id=VIDEO_REPO_ID, filename=hf_filename, repo_type="dataset", revision="main")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(local_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        return True
    logging.warning(f"Download failed (status={r.status_code}): {url}")
    return False

def process_frame_mediapipe(local_frame, local_annotated, frame_id):
    landmarks = [
        mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP,
        mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.RIGHT_KNEE,
        mp_pose.PoseLandmark.LEFT_ANKLE, mp_pose.PoseLandmark.RIGHT_ANKLE,
        mp_pose.PoseLandmark.LEFT_FOOT_INDEX, mp_pose.PoseLandmark.RIGHT_FOOT_INDEX,
        mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER,
        mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.RIGHT_ELBOW,
        mp_pose.PoseLandmark.LEFT_WRIST, mp_pose.PoseLandmark.RIGHT_WRIST
    ]
    img = cv2.imread(local_frame)
    if img is None:
        logging.error(f"Unable to read frame_id={frame_id} at {local_frame}")
        return False

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)
    if results.pose_landmarks:
        ann_img = img.copy()
        mp_drawing.draw_landmarks(ann_img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imwrite(local_annotated, ann_img)
        for lm_enum in landmarks:
            idx = lm_enum.value
            lm = results.pose_landmarks.landmark[idx]
            insert_pose_feature(frame_id, lm_enum.name, lm.x, lm.y, lm.z, lm.visibility)
        return True
    else:
        logging.warning(f"No landmarks for frame_id={frame_id}")
        return True

def process_single_frame(frame_info, frames_dir, annotated_dir):
    """
    Downloads + processes a single frame in a separate thread.
    Returns (success, annotated_filename) for use in commits.
    """
    frame_id, frame_no, hf_path = frame_info
    local_frame = os.path.join(frames_dir, f"frame_{frame_id}.png")
    if not download_frame_from_hf(hf_path, local_frame):
        return (False, None)
    ann_name = os.path.basename(hf_path).replace(".png", "_annotated.png")
    local_annotated = os.path.join(annotated_dir, ann_name)
    ok = process_frame_mediapipe(local_frame, local_annotated, frame_id)
    return (ok, ann_name if ok else None)

def batch_process_video(video_id, frames_list):
    """
    Processes frames for one video concurrently. 
    After all frames are annotated, creates a single commit with create_commit.
    """
    temp_dir_frames = tempfile.mkdtemp(prefix=f"video_{video_id}_frames_")
    temp_dir_annot = tempfile.mkdtemp(prefix=f"video_{video_id}_ann_")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=21) as executor:
        future_to_frame = {
            executor.submit(process_single_frame, f, temp_dir_frames, temp_dir_annot): f
            for f in frames_list
        }
        for future in concurrent.futures.as_completed(future_to_frame):
            ok, ann_name = future.result()
            results.append((ok, ann_name))

    # Build create_commit operations
    ops = []
    for (ok, ann_name) in results:
        if ok and ann_name is not None:
            local_annot_path = os.path.join(temp_dir_annot, ann_name)
            if os.path.exists(local_annot_path):
                # Prepare add_or_update for huggingface_hub
                from huggingface_hub import CommitOperationAdd
                path_in_repo = f"{ANNOTATED_FRAMES_FOLDER}/{ann_name}"
                ops.append(
                    CommitOperationAdd(
                        path_in_repo=path_in_repo,
                        path_or_fileobj=local_annot_path
                    )
                )

    if ops:
        msg = f"Add annotated frames for video_id={video_id}"
        try:
            commit_info = api.create_commit(
                repo_id=VIDEO_REPO_ID,
                repo_type="dataset",
                operations=ops,
                commit_message=msg
            )
            if not commit_info or not getattr(commit_info, 'commit_id', None):
                logging.info(f"No changes for video_id={video_id} (commit empty).")
            else:
                logging.info(f"Committed {len(ops)} annotated frames for video_id={video_id} in one commit.")
        except Exception as e:
            logging.error(f"Commit failed for video_id={video_id}: {e}")
    else:
        logging.info(f"No annotated frames to commit for video_id={video_id}.")

    shutil.rmtree(temp_dir_frames)
    shutil.rmtree(temp_dir_annot)

def extract_frames_from_kick_data():
    from pose_data_setup import initialize_pose_data
    initialize_pose_data()

    conn = sqlite3.connect(KICK_DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT video_id, frame_id, frame_no, frame_path FROM frames")
    rows = cur.fetchall()
    conn.close()

    frames_by_video = defaultdict(list)
    for (vid, fid, fno, fpath) in rows:
        # fpath example: "frames/VID_1_KICK_2_FRAME_001.png"
        frames_by_video[vid].append((fid, fno, fpath))

    for video_id, frames_list in frames_by_video.items():
        logging.info(f"Processing video_id={video_id} with {len(frames_list)} frames.")
        batch_process_video(video_id, frames_list)

def main():
    extract_frames_from_kick_data()
    pose.close()

if __name__ == "__main__":
    main()
