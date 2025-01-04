# web_app/backend/services/db_manager.py

from database.db_setup import get_connection

def insert_video(session_id, original_name):
    """
    Insert a row into 'videos' with session_id + original_name.
    Return the video_id.
    """
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
    """
    Return (video_id, original_name) for a video matching
    session_id + filename, or None if not found.
    """
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
    """
    Insert a row in 'kicks' with video_id + timestamp.
    Return the kick_id.
    """
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
    """
    Insert a row in 'frames' referencing the kick + video.
    """
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
