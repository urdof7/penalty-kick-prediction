# web_app/backend/services/pose_manager.py

import os
import cv2
import mediapipe as mp
import shutil

from services.db_manager import get_connection, insert_pose_feature

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def detect_pose_and_annotate(video_id, session_id):
    """
    1) Finds frames for the given video_id.
    2) Uses MediaPipe Pose to detect landmarks.
    3) Saves annotated frames in 'temp_annotated_frames/' + session_id prefix.
    4) Inserts pose features in DB (pose_features table).
    5) Returns a list of annotated frame filenames to display.

    Returns: List of final annotated image filenames (no path prefix).
    """
    # 1) Get all frames from DB for this video
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT frame_id, frame_path
        FROM frames
        WHERE video_id=?
        ORDER BY frame_no ASC
    """, (video_id,))
    frames_db = cur.fetchall()
    conn.close()

    # 2) Prepare the output folder
    #    We'll store annotated images in 'temp_annotated_frames/'
    #    Possibly prefix them with session_id to avoid collisions
    base_dir = os.path.dirname(__file__)  # .../services
    backend_root = os.path.dirname(base_dir)  # .../backend
    annotated_folder = os.path.join(backend_root, 'temp_annotated_frames')
    os.makedirs(annotated_folder, exist_ok=True)

    annotated_filenames = []

    # 3) Initialize MediaPipe Pose once
    with mp_pose.Pose(static_image_mode=True) as pose:
        for (frame_id, frame_path) in frames_db:
            # 'frame_path' is something like "my_frame.png" or "sessionID_frame_001.png"
            # The actual file is in <backend_root>/temp_frames/<frame_path>
            temp_frames_folder = os.path.join(backend_root, 'temp_frames')
            in_path = os.path.join(temp_frames_folder, frame_path)

            if not os.path.exists(in_path):
                # Skip if the frame is missing
                continue

            # Build the out_path in 'temp_annotated_frames/<session_id>_<frame_path>'
            ann_name = f"{session_id}_{frame_path}"
            out_path = os.path.join(annotated_folder, ann_name)

            # 4) Run MediaPipe Pose
            img = cv2.imread(in_path)
            if img is None:
                continue
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)

            # If we detect landmarks, insert into DB + draw
            if results.pose_landmarks:
                # Draw landmarks on a copy
                annotated_img = img.copy()
                mp_drawing.draw_landmarks(
                    annotated_img,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )
                cv2.imwrite(out_path, annotated_img)

                # For each landmark of interest, store in pose_features
                # Or store all landmarks. Here we store all 33. 
                for idx, lm in enumerate(results.pose_landmarks.landmark):
                    insert_pose_feature(
                        frame_id,
                        f"LANDMARK_{idx}",
                        lm.x,
                        lm.y,
                        lm.z,
                        lm.visibility
                    )
                # Save the final annotated filename
                annotated_filenames.append(ann_name)
            else:
                # No landmarks
                # (Optional) we can create an empty annotated or skip
                pass

    return annotated_filenames
