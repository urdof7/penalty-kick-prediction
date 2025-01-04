# web_app/backend/routes/upload_routes.py

import os
from flask import Blueprint, request, jsonify, current_app, g
from services.db_manager import insert_video

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_video():
    """
    Receives a file, saves it in 'uploads/' with its original filename,
    inserts a row with (session_id, original_name).
    Returns JSON with { filename, video_id }.
    """
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file found"}), 400

    # Session ID from flask.g
    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({"error": "No session_id found (unexpected)"}), 500

    upload_folder = os.path.join(current_app.root_path, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    orig_filename = file.filename  # Use the file's original name can change
    save_path = os.path.join(upload_folder, orig_filename)
    file.save(save_path)

    # Insert into DB with session_id + original name
    video_id = insert_video(session_id, orig_filename)

    return jsonify({
        "filename": orig_filename,
        "video_id": video_id
    }), 200
