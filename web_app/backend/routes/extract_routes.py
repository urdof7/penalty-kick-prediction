# web_app/backend/routes/extract_routes.py

import os
import shutil
from flask import Blueprint, request, jsonify, current_app, send_from_directory, g
from services.db_manager import (
    get_video_by_name,
    insert_kick,
    insert_frame
)
from services.frame_extraction import extract_frames_around_time

extract_bp = Blueprint('extract_bp', __name__)

@extract_bp.route('/extract_frames', methods=['POST'])
def extract_frames():
    """
    JSON: {
      "filename": <str>,
      "timestamp": <float>
    }
    Extract frames around the given 'timestamp' in the user's video,
    store in DB, copy images to 'temp_frames'.
    """
    data = request.json
    filename = data.get('filename')
    midswing_time = float(data.get('timestamp', 0.0))

    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({"error": "No session_id found."}), 500

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    # Validate the video belongs to this session
    row = get_video_by_name(session_id, filename)
    if not row:
        return jsonify({"error": "Video not found for this session"}), 404
    video_id = row[0]

    # Check file existence
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    video_path = os.path.join(upload_folder, filename)
    if not os.path.exists(video_path):
        return jsonify({"error": f"File {filename} not found"}), 404

    # Insert 'kick' row
    kick_id = insert_kick(video_id, midswing_time)

    # Extract frames
    temp_dir, frames_list = extract_frames_around_time(video_path, midswing_time)

    # Copy frames to 'temp_frames' and insert into DB
    temp_frames_folder = os.path.join(current_app.root_path, 'temp_frames')
    os.makedirs(temp_frames_folder, exist_ok=True)

    from services.db_manager import get_connection
    conn = get_connection()
    cur = conn.cursor()

    frame_urls = []
    for i, src_path in enumerate(frames_list, start=1):
        # Insert a row in frames, but no special naming
        cur.execute("""
            INSERT INTO frames (kick_id, video_id, frame_no, frame_path)
            VALUES (?, ?, ?, ?)
        """, (kick_id, video_id, i, ""))  # placeholder, will update below
        frame_id = cur.lastrowid

        # Let's keep exactly the base name from the extracted frame
        base_name = os.path.basename(src_path)

        # Copy to temp_frames with the same base name
        dst_path = os.path.join(temp_frames_folder, base_name)
        shutil.copy(src_path, dst_path)

        # Update frame_path in DB with the same base name
        cur.execute("UPDATE frames SET frame_path=? WHERE frame_id=?", (base_name, frame_id))

        url = f"/api/temp_frames/{base_name}"
        frame_urls.append(url)

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Frames extracted successfully",
        "kick_id": kick_id,
        "frame_urls": frame_urls
    }), 200

@extract_bp.route('/temp_frames/<path:filename>')
def serve_temp_frames(filename):
    temp_frames_folder = os.path.join(current_app.root_path, 'temp_frames')
    return send_from_directory(temp_frames_folder, filename)
