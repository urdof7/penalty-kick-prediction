"""
extract_pose_features.py

can be optimized for both local computer and high-powered GPU/CPU machines.
1) Downloads frames (potentially concurrently for I/O) from Hugging Face.
2) Processes frames with Mediapipe Pose (can be single-threaded or multi-threaded).
3) Commits annotated frames in one go per video.

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
import argparse  # For optional CLI arguments
from collections import defaultdict

from huggingface_hub import HfApi, hf_hub_url, CommitOperationAdd
from pose_data_setup import initialize_pose_data, insert_pose_feature


# Configuration / Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KICK_DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'kick_data.db')

VIDEO_REPO_ID = "PK-Prediction/pk_data"
FRAMES_FOLDER = "frames"  # frames on HF
ANNOTATED_FRAMES_FOLDER = "annotated-frames"
api = HfApi()

# I/O Download Helpers
def download_frame_from_hf(hf_filename: str, local_path: str) -> bool:
    """
    Downloads a single frame from Hugging Face Hub and saves to local_path.
    Returns True on success, False if download fails.
    """
    url = hf_hub_url(repo_id=VIDEO_REPO_ID, filename=hf_filename, repo_type="dataset", revision="main")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(local_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        return True
    logging.warning(f"Download failed (status={r.status_code}): {url}")
    return False



# Pose Processing
def process_frame_mediapipe(local_pose, local_frame: str, local_annotated: str, frame_id: int) -> bool:
    """
    Runs Mediapipe Pose on a single frame.
    - local_pose: a local mp_pose.Pose() instance
    - local_frame: path to input frame
    - local_annotated: path to save annotated image
    - frame_id: ID in the DB
    Returns True on success or if no landmarks found (but no crash),
    False if any catastrophic failure (like missing file).
    """
    # Landmarks of interest
    landmarks_of_interest = [
        mp.solutions.pose.PoseLandmark.LEFT_HIP,    mp.solutions.pose.PoseLandmark.RIGHT_HIP,
        mp.solutions.pose.PoseLandmark.LEFT_KNEE,   mp.solutions.pose.PoseLandmark.RIGHT_KNEE,
        mp.solutions.pose.PoseLandmark.LEFT_ANKLE,  mp.solutions.pose.PoseLandmark.RIGHT_ANKLE,
        mp.solutions.pose.PoseLandmark.LEFT_FOOT_INDEX, mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX,
        mp.solutions.pose.PoseLandmark.LEFT_SHOULDER, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER,
        mp.solutions.pose.PoseLandmark.LEFT_ELBOW,  mp.solutions.pose.PoseLandmark.RIGHT_ELBOW,
        mp.solutions.pose.PoseLandmark.LEFT_WRIST,  mp.solutions.pose.PoseLandmark.RIGHT_WRIST
    ]

    # Read image
    img = cv2.imread(local_frame)
    if img is None:
        logging.error(f"Unable to read frame_id={frame_id} at {local_frame}")
        return False

    # Mediapipe Pose
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = local_pose.process(rgb)
    if results.pose_landmarks:
        # Draw annotated
        ann_img = img.copy()
        mp.solutions.drawing_utils.draw_landmarks(
            ann_img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS
        )
        cv2.imwrite(local_annotated, ann_img)

        # Insert selected landmark data into DB
        for lm_enum in landmarks_of_interest:
            idx = lm_enum.value
            lm = results.pose_landmarks.landmark[idx]
            insert_pose_feature(
                frame_id,
                lm_enum.name,
                lm.x,
                lm.y,
                lm.z,
                lm.visibility
            )
    else:
        logging.warning(f"No landmarks for frame_id={frame_id}")

    return True


def single_thread_pose_inference(frames_list, frames_dir, annotated_dir):
    """
    Processes all frames in a single-thread loop using *one* Pose instance 
    (which is safe for sequential inference).
    """
    with mp.solutions.pose.Pose(static_image_mode=True) as local_pose:
        for frame_id, frame_no, hf_path in frames_list:
            local_frame_path = os.path.join(frames_dir, f"frame_{frame_id}.png")
            ann_name = os.path.basename(hf_path).replace(".png", "_annotated.png")
            local_annotated_path = os.path.join(annotated_dir, ann_name)

            ok = process_frame_mediapipe(local_pose, local_frame_path, local_annotated_path, frame_id)
            if not ok:
                logging.error(f"Pose processing failed for frame_id={frame_id}")


def multi_thread_pose_inference(frames_list, frames_dir, annotated_dir, max_workers):
    """
    Processes frames concurrently. Each thread creates its own Pose instance.
    This avoids timestamp mismatch but can still be CPU/GPU heavy. 
    Useful if your machine can handle multi-thread inference.

    NOTE: For heavy GPU usage, 
      - test if multiple Pose instances in parallel degrade performance.
      - On a multi-core CPU with no GPU usage, this might help.
    """
    def _thread_worker(frame_info):
        frame_id, frame_no, hf_path = frame_info
        local_frame_path = os.path.join(frames_dir, f"frame_{frame_id}.png")
        ann_name = os.path.basename(hf_path).replace(".png", "_annotated.png")
        local_annotated_path = os.path.join(annotated_dir, ann_name)

        # Create a local Pose instance
        with mp.solutions.pose.Pose(static_image_mode=True) as local_pose:
            ok = process_frame_mediapipe(local_pose, local_frame_path, local_annotated_path, frame_id)
        return (ok, ann_name if ok else None)

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_frame = {executor.submit(_thread_worker, f): f for f in frames_list}
        for future in concurrent.futures.as_completed(future_to_frame):
            results.append(future.result())
    return results


# Main Processing: Download + Pose + Commit
def batch_process_video(
    video_id,
    frames_list,
    download_workers=8,
    pose_workers=1,  # 1 => single-thread pose inference
):
    """
    Processes frames for one video:
    1) Download all frames (concurrently if desired).
    2) Pose inference (single-threaded or multi-threaded).
    3) Commit annotated frames in one go.

    :param video_id: The video ID from DB
    :param frames_list: [(frame_id, frame_no, frame_path), ...]
    :param download_workers: number of threads for downloading frames
    :param pose_workers: number of threads for pose
                         - if 1 => single-thread
                         - if >1 => multi-thread, each with its own Pose instance
    """

    # Sort frames by frame_no so local file naming is consistent
    # (This ensures local directory has frame_1, frame_2, ... in ascending order.)
    frames_list.sort(key=lambda x: x[1])

    # Prepare temp dirs
    temp_dir_frames = tempfile.mkdtemp(prefix=f"video_{video_id}_frames_")
    temp_dir_annot = tempfile.mkdtemp(prefix=f"video_{video_id}_ann_")

    # 1) Download frames from Hugging Face (I/O concurrency)
    def _download_worker(f):
        frame_id, frame_no, hf_path = f
        local_frame = os.path.join(temp_dir_frames, f"frame_{frame_id}.png")
        success = download_frame_from_hf(hf_path, local_frame)
        return success

    # Run concurrent downloads
    with concurrent.futures.ThreadPoolExecutor(max_workers=download_workers) as executor:
        download_futures = {executor.submit(_download_worker, f): f for f in frames_list}
        for future in concurrent.futures.as_completed(download_futures):
            if not future.result():
                # log if download failed
                fail_f = download_futures[future]
                logging.warning(f"Download failed for frame_id={fail_f[0]}")

    # 2) Pose inference
    if pose_workers == 1:
        # Single-thread for Pose
        single_thread_pose_inference(frames_list, temp_dir_frames, temp_dir_annot)
        # We'll gather annotated filenames from the directory after we finish
        results = []
        for (fid, fno, hf_path) in frames_list:
            ann_name = os.path.basename(hf_path).replace(".png", "_annotated.png")
            local_annot = os.path.join(temp_dir_annot, ann_name)
            # Just approximate the "ok" for demonstration
            ok = os.path.exists(local_annot)
            results.append((ok, ann_name if ok else None))
    else:
        # Multi-thread Pose: each thread has its own Pose instance
        results = multi_thread_pose_inference(frames_list, temp_dir_frames, temp_dir_annot, pose_workers)

    # 3) Build create_commit operations for annotated frames
    ops = []
    for (ok, ann_name) in results:
        if ok and ann_name is not None:
            local_annot_path = os.path.join(temp_dir_annot, ann_name)
            if os.path.exists(local_annot_path):
                path_in_repo = f"{ANNOTATED_FRAMES_FOLDER}/{ann_name}"
                ops.append(
                    CommitOperationAdd(
                        path_in_repo=path_in_repo,
                        path_or_fileobj=local_annot_path
                    )
                )

    # 4) Create a single commit if we have changes
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

    # Cleanup
    shutil.rmtree(temp_dir_frames)
    shutil.rmtree(temp_dir_annot)


def extract_frames_from_kick_data(
    download_workers=8,
    pose_workers=1
):
    """
    Main function that:
    1) Initializes pose_data DB (via pose_data_setup)
    2) Reads frames from kick_data.db
    3) Batches them by video
    4) Calls batch_process_video(...) for each video

    :param download_workers: concurrency for downloading frames
    :param pose_workers: concurrency for pose inference
    """
    # Ensure pose_data.db is set up
    initialize_pose_data()

    # Read frames from DB
    conn = sqlite3.connect(KICK_DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT video_id, frame_id, frame_no, frame_path FROM frames")
    rows = cur.fetchall()
    conn.close()

    frames_by_video = defaultdict(list)
    for (vid, fid, fno, fpath) in rows:
        frames_by_video[vid].append((fid, fno, fpath))

    # Process each video
    for video_id, frames_list in frames_by_video.items():
        logging.info(f"Processing video_id={video_id} with {len(frames_list)} frames.")
        batch_process_video(video_id, frames_list, download_workers, pose_workers)


# CLI + Main
def main():
    parser = argparse.ArgumentParser(description="Extract pose features from frames using MediaPipe Pose.")
    parser.add_argument(
        "--download-workers",
        type=int,
        default=8,
        help="Number of threads for frame downloading (I/O). Default=8."
    )
    parser.add_argument(
        "--pose-workers",
        type=int,
        default=1,
        help="Number of threads for pose inference. Default=1 (single-thread)."
    )

    args = parser.parse_args()

    # Info logging for clarity
    logging.info(f"Starting pose extraction with {args.download_workers} download threads "
                 f"and {args.pose_workers} pose threads.")

    extract_frames_from_kick_data(
        download_workers=args.download_workers,
        pose_workers=args.pose_workers
    )


if __name__ == "__main__":
    main()
