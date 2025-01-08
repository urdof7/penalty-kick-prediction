# web_app/backend/services/db_manager.py

import os
import sqlite3
from database.db_setup import get_connection
import pandas as pd

def clear_session_data(session_id):
    """
    Removes all videos + frames + pose_features under this session_id.
    Returns (video_files, frame_files, annotated_frame_files)
      so caller can remove them from disk.
    """
    conn = get_connection()
    cur = conn.cursor()

    # 1) Find all videos for this session
    cur.execute("SELECT video_id, original_name FROM videos WHERE session_id=?", (session_id,))
    video_rows = cur.fetchall()
    if not video_rows:
        conn.close()
        return ([], [], [])

    video_ids = [row[0] for row in video_rows]
    video_names = [row[1] for row in video_rows]

    # Gather all frames for these videos
    placeholders = ",".join(["?"]*len(video_ids))
    cur.execute(f"SELECT frame_id, frame_path FROM frames WHERE video_id IN ({placeholders})", video_ids)
    frame_rows = cur.fetchall()
    frame_files = [r[1] for r in frame_rows]

    # Pose features: we can just remove them by frame_id
    frame_ids = [r[0] for r in frame_rows]
    if frame_ids:
        frame_placeholders = ",".join(["?"]*len(frame_ids))
        cur.execute(f"DELETE FROM pose_features WHERE frame_id IN ({frame_placeholders})", frame_ids)

    # Delete frames
    cur.execute(f"DELETE FROM frames WHERE video_id IN ({placeholders})", video_ids)

    # Delete kicks
    cur.execute(f"DELETE FROM kicks WHERE video_id IN ({placeholders})", video_ids)

    # Finally delete videos
    cur.execute(f"DELETE FROM videos WHERE video_id IN ({placeholders})", video_ids)

    conn.commit()
    conn.close()

    # For annotated frames, we typically name them with session_id + frame_path,
    # so we can guess them. Let's build them all:
    annotated_frame_files = []
    for ff in frame_files:
        # The annotated name might be session_id + "_" + ff
        # e.g. sessionID_frame_001.png
        annotated_frame_files.append(f"{session_id}_{ff}")

    return (video_names, frame_files, annotated_frame_files)

def clear_frames_for_video(session_id, video_id):
    """
    Clears frames + pose_features for a specific video in this session, 
    so we can re-extract them. Returns (frame_files, annotated_frame_files).
    (We do NOT remove the video row.)
    """
    conn = get_connection()
    cur = conn.cursor()

    # 1) Gather frames for that video
    cur.execute("SELECT frame_id, frame_path FROM frames WHERE video_id=?", (video_id,))
    frame_rows = cur.fetchall()
    if not frame_rows:
        conn.close()
        return ([], [])

    frame_ids = [r[0] for r in frame_rows]
    frame_files = [r[1] for r in frame_rows]

    # 2) Delete pose_features for these frames
    placeholders = ",".join(["?"]*len(frame_ids))
    cur.execute(f"DELETE FROM pose_features WHERE frame_id IN ({placeholders})", frame_ids)

    # 3) Delete frames
    cur.execute("DELETE FROM frames WHERE video_id=?", (video_id,))

    # 4) Delete any kicks referencing these frames 
    #    (Optional if you only store 1 kick per video. 
    #     If you want to keep the 'kicks' row, remove this.)
    # cur.execute("DELETE FROM kicks WHERE video_id=?", (video_id,))

    conn.commit()
    conn.close()

    # Build annotated names (sessionID_frame_001.png => sessionID_frame_001.png)
    # If your naming convention is "sessionID_<originalFrame>", we do:
    annotated_frame_files = [f"{session_id}_{ff}" for ff in frame_files]
    return (frame_files, annotated_frame_files)

def insert_video(session_id, original_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO videos (session_id, original_name)
        VALUES (?, ?)
    """, (session_id, original_name))
    vid = cur.lastrowid
    conn.commit()
    conn.close()
    return vid

def get_video_by_name(session_id, filename):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT video_id, original_name
        FROM videos
        WHERE session_id=? AND original_name=?
        LIMIT 1
    """, (session_id, filename))
    row = cur.fetchone()
    conn.close()
    return row

def insert_kick(video_id, timestamp):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO kicks (video_id, timestamp)
        VALUES (?, ?)
    """, (video_id, timestamp))
    kid = cur.lastrowid
    conn.commit()
    conn.close()
    return kid

def insert_frame(kick_id, video_id, frame_no, frame_path):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO frames (kick_id, video_id, frame_no, frame_path)
        VALUES (?, ?, ?, ?)
    """, (kick_id, video_id, frame_no, frame_path))
    fid = cur.lastrowid
    conn.commit()
    conn.close()
    return fid

def insert_pose_feature(frame_id, landmark_name, x, y, z, visibility):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pose_features (frame_id, landmark_name, x, y, z, visibility)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (frame_id, landmark_name, x, y, z, visibility))
    conn.commit()
    conn.close()

def get_pose_data_for_video(session_id, video_id):
    """
    Returns a pandas DataFrame containing frames+pose for the given session_id + video_id,
    with columns: [frame_id, kick_id, video_id, frame_no, landmark_name, x, y, z]
    Merged from frames + pose_features, plus we can also join kicks if needed.
    """
    conn = get_connection()
    
    # We only merge frames that belong to this session_id & video_id
    # Then join with pose_features
    query = """
    SELECT f.frame_id, f.kick_id, f.video_id, f.frame_no,
           p.landmark_name, p.x, p.y, p.z
    FROM frames f
    JOIN pose_features p ON f.frame_id = p.frame_id
    JOIN videos v ON f.video_id = v.video_id
    WHERE v.session_id = ?
      AND f.video_id = ?
    ORDER BY f.frame_no ASC
    """
    df = pd.read_sql_query(query, conn, params=(session_id, video_id))
    
    conn.close()
    return df

def insert_engineered_feature(
    frame_id,
    x_hip_left, y_hip_left, x_hip_right, y_hip_right,
    x_knee_left, y_knee_left, x_knee_right, y_knee_right,
    x_ankle_left, y_ankle_left, x_ankle_right, y_ankle_right,
    x_left_foot_index, y_left_foot_index,
    x_right_foot_index, y_right_foot_index,
    x_shoulder_left, y_shoulder_left,
    x_shoulder_right, y_shoulder_right,
    x_elbow_left, y_elbow_left,
    x_elbow_right, y_elbow_right,
    x_wrist_left, y_wrist_left,
    x_wrist_right, y_wrist_right,
    angle_knee_left, angle_knee_right,
    angle_elbow_left, angle_elbow_right,
    angle_ankle_left, angle_ankle_right,
    angle_foot_left, angle_foot_right
):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
    INSERT INTO engineered_features (
        frame_id,
        x_hip_left, y_hip_left,
        x_hip_right, y_hip_right,
        x_knee_left, y_knee_left,
        x_knee_right, y_knee_right,
        x_ankle_left, y_ankle_left,
        x_ankle_right, y_ankle_right,
        x_left_foot_index, y_left_foot_index,
        x_right_foot_index, y_right_foot_index,
        x_shoulder_left, y_shoulder_left,
        x_shoulder_right, y_shoulder_right,
        x_elbow_left, y_elbow_left,
        x_elbow_right, y_elbow_right,
        x_wrist_left, y_wrist_left,
        x_wrist_right, y_wrist_right,
        angle_knee_left, angle_knee_right,
        angle_elbow_left, angle_elbow_right,
        angle_ankle_left, angle_ankle_right,
        angle_foot_left, angle_foot_right
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    cur.execute(sql, (
        frame_id,
        x_hip_left, y_hip_left,
        x_hip_right, y_hip_right,
        x_knee_left, y_knee_left,
        x_knee_right, y_knee_right,
        x_ankle_left, y_ankle_left,
        x_ankle_right, y_ankle_right,
        x_left_foot_index, y_left_foot_index,
        x_right_foot_index, y_right_foot_index,
        x_shoulder_left, y_shoulder_left,
        x_shoulder_right, y_shoulder_right,
        x_elbow_left, y_elbow_left,
        x_elbow_right, y_elbow_right,
        x_wrist_left, y_wrist_left,
        x_wrist_right, y_wrist_right,
        angle_knee_left, angle_knee_right,
        angle_elbow_left, angle_elbow_right,
        angle_ankle_left, angle_ankle_right,
        angle_foot_left, angle_foot_right
    ))
    conn.commit()
    conn.close()


def clear_engineered_for_frames(frame_ids):
    if not frame_ids:
        return
    c = get_connection()
    cur = c.cursor()
    placeholders = ",".join(["?"]*len(frame_ids))
    cur.execute(f"DELETE FROM engineered_features WHERE frame_id IN ({placeholders})", frame_ids)
    c.commit()
    c.close()