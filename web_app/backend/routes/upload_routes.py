# web_app/backend/routes/upload_routes.py

import os
from flask import Blueprint, request, jsonify, current_app, g
from services.db_manager import insert_video, clear_session_data
from services.file_cleanup import remove_files_in_folder

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_video():
    """
    1) Clears old data (videos, frames, annotated) for this session.
    2) Saves new video to 'uploads/<session_id>_<original_name>'.
    3) Inserts a 'videos' row with (session_id, new_filename).
    Returns { filename, video_id }.
    """
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file found"}), 400

    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({"error": "No session_id found"}), 500

    # 1) Clear old DB data for this session
    video_names, frame_files, annotated_files = clear_session_data(session_id)

    # 2) Remove old files from disk
    #    old videos in 'uploads/'
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    for v in video_names:
        old_video_path = os.path.join(upload_folder, v)
        if os.path.exists(old_video_path):
            os.remove(old_video_path)

    # remove frames from 'temp_frames'
    temp_frames_folder = os.path.join(current_app.root_path, 'temp_frames')
    remove_files_in_folder(temp_frames_folder, frame_files)

    # remove annotated from 'temp_annotated_frames'
    temp_annotated_folder = os.path.join(current_app.root_path, 'temp_annotated_frames')
    remove_files_in_folder(temp_annotated_folder, annotated_files)

    # 3) Store the new video
    orig_filename = file.filename
    new_filename = f"{session_id}_{orig_filename}"
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, new_filename)
    file.save(save_path)

    video_id = insert_video(session_id, new_filename)

    return jsonify({
        "filename": new_filename,
        "video_id": video_id
    }), 200
