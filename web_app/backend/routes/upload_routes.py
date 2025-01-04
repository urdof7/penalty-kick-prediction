# web_app/backend/routes/upload_routes.py

import os
import shutil
from flask import Blueprint, request, jsonify, current_app, g
from services.db_manager import insert_video, clear_session_data

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_video():
    """
    Receives a file, saves it in 'uploads/<session_id>_<orig_filename>',
    clears old data in DB for this session, inserts row (session_id, new_name).
    Returns JSON with { filename, video_id }.
    """
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file found"}), 400

    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({"error": "No session_id found (unexpected)"}), 500

    # --- 1) Clear existing DB data for this session
    old_videos, old_frames = clear_session_data(session_id)

    # Remove old frames from 'temp_frames' folder
    temp_frames_folder = os.path.join(current_app.root_path, 'temp_frames')
    for f in old_frames:
        old_path = os.path.join(temp_frames_folder, f)
        if os.path.exists(old_path):
            os.remove(old_path)

    # Remove old video files in 'uploads' if needed
    uploads_folder = os.path.join(current_app.root_path, 'uploads')
    for vid_filename in old_videos:
        old_vid_path = os.path.join(uploads_folder, vid_filename)
        if os.path.exists(old_vid_path):
            os.remove(old_vid_path)

    # --- 2) Store the new video with session_id prefix
    orig_filename = file.filename
    new_filename = f"{session_id}_{orig_filename}"  # prefix session
    save_path = os.path.join(uploads_folder, new_filename)
    file.save(save_path)

    # --- 3) Insert into DB (videos table)
    video_id = insert_video(session_id, new_filename)

    return jsonify({
        "filename": new_filename,
        "video_id": video_id
    }), 200
