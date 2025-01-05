# web_app/backend/routes/extract_routes.py

import os
import shutil
from flask import Blueprint, request, jsonify, send_from_directory, current_app, g
from services.db_manager import (
    get_video_by_name,
    insert_kick,
    insert_frame,
    clear_frames_for_video
)
from services.file_cleanup import remove_files_in_folder
from services.frame_extraction import extract_frames_around_time

extract_bp = Blueprint('extract_bp', __name__)

@extract_bp.route('/extract_frames', methods=['POST'])
def extract_frames():
    """
    JSON body: { filename, timestamp }
    1) Clears old frames + annotated frames for this video (in case user re-extracts).
    2) Extracts new frames around 'timestamp'.
    3) Returns list of new frame URLs.
    """
    data = request.json
    filename = data.get('filename')
    midswing_time = float(data.get('timestamp', 0.0))

    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({"error": "No session_id found."}), 500

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    row = get_video_by_name(session_id, filename)
    if not row:
        return jsonify({"error": "Video not found for this session"}), 404

    video_id = row[0]

    # 1) Clear old frames + annotated for this video (just in case user is redoing)
    frame_files, annotated_files = clear_frames_for_video(session_id, video_id)

    temp_frames_folder = os.path.join(current_app.root_path, 'temp_frames')
    remove_files_in_folder(temp_frames_folder, frame_files)

    temp_annotated_folder = os.path.join(current_app.root_path, 'temp_annotated_frames')
    remove_files_in_folder(temp_annotated_folder, annotated_files)

    # 2) Extract frames
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    video_path = os.path.join(upload_folder, filename)
    if not os.path.exists(video_path):
        return jsonify({"error": f"File {filename} not found"}), 404

    kick_id = insert_kick(video_id, midswing_time)

    temp_dir, frames_list = extract_frames_around_time(video_path, midswing_time, exact_frames=True)
    # ^ We assume 'exact_frames=True' for better accuracy or you can pass as needed.

    # Copy frames to 'temp_frames' and insert DB
    os.makedirs(temp_frames_folder, exist_ok=True)

    from services.db_manager import get_connection
    conn = get_connection()
    cur = conn.cursor()

    frame_urls = []
    for i, src_path in enumerate(frames_list, start=1):
        # Insert row in frames
        cur.execute("""
            INSERT INTO frames (kick_id, video_id, frame_no, frame_path)
            VALUES (?, ?, ?, ?)
        """, (kick_id, video_id, i, ""))  # placeholder
        frame_id = cur.lastrowid

        base_name = os.path.basename(src_path)
        final_name = base_name  # if you want session_id_{base_name}, do that
        dst_path = os.path.join(temp_frames_folder, final_name)
        shutil.copy(src_path, dst_path)

        cur.execute("UPDATE frames SET frame_path=? WHERE frame_id=?", (final_name, frame_id))

        url = f"/api/temp_frames/{final_name}"
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
