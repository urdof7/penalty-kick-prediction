# web_app/backend/services/db_manager.py

from database.db_setup import get_connection

def clear_session_data(session_id):
    """
    Removes all videos under this session_id (and associated kicks, frames, pose_features).
    Returns (video_files, frame_files) so the caller can remove them from disk if desired.
    """
    conn = get_connection()
    cur = conn.cursor()

    # 1) Collect all video_ids + their filenames for this session
    cur.execute("SELECT video_id, original_name FROM videos WHERE session_id=?", (session_id,))
    video_rows = cur.fetchall()
    video_ids = [r[0] for r in video_rows]
    video_files = [r[1] for r in video_rows]  # the actual filenames on disk

    if not video_ids:
        # Nothing to clear
        conn.close()
        return ([], [])

    # Make a tuple or list for WHERE ... IN usage
    video_ids_tuple = tuple(video_ids)
    placeholders = ",".join(["?"] * len(video_ids))

    # 2) Collect frame filenames so we can remove them from disk
    frame_files = []
    if len(video_ids) == 1:
        # single video -> can do simpler queries
        cur.execute("SELECT frame_path FROM frames WHERE video_id=?", video_ids_tuple)
    else:
        cur.execute(f"SELECT frame_path FROM frames WHERE video_id IN ({placeholders})", video_ids)
    rows = cur.fetchall()
    frame_files = [row[0] for row in rows if row[0] is not None]

    # 3) Delete pose_features for these frames
    #    First find all frame_ids
    if len(video_ids) == 1:
        cur.execute("SELECT frame_id FROM frames WHERE video_id=?", video_ids_tuple)
    else:
        cur.execute(f"SELECT frame_id FROM frames WHERE video_id IN ({placeholders})", video_ids)
    frame_ids = [r[0] for r in cur.fetchall()]

    if frame_ids:
        if len(frame_ids) == 1:
            cur.execute("DELETE FROM pose_features WHERE frame_id=?", (frame_ids[0],))
        else:
            frame_placeholders = ",".join(["?"] * len(frame_ids))
            cur.execute(f"DELETE FROM pose_features WHERE frame_id IN ({frame_placeholders})", frame_ids)

    # 4) Delete frames + kicks + videos
    if len(video_ids) == 1:
        cur.execute("DELETE FROM frames WHERE video_id=?", video_ids_tuple)
        cur.execute("DELETE FROM kicks WHERE video_id=?", video_ids_tuple)
        cur.execute("DELETE FROM videos WHERE video_id=?", video_ids_tuple)
    else:
        cur.execute(f"DELETE FROM frames WHERE video_id IN ({placeholders})", video_ids)
        cur.execute(f"DELETE FROM kicks WHERE video_id IN ({placeholders})", video_ids)
        cur.execute(f"DELETE FROM videos WHERE video_id IN ({placeholders})", video_ids)

    conn.commit()
    conn.close()

    return (video_files, frame_files)

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
