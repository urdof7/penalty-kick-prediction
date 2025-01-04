# web_app/backend/routes/pose_routes.py

import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory, g
from services.db_manager import get_video_by_name
from services.pose_manager import detect_pose_and_annotate

pose_bp = Blueprint('pose_bp', __name__)

@pose_bp.route('/detect_pose', methods=['POST'])
def detect_pose():
    """
    JSON body: { "filename": <str> }
    1) Verify session_id
    2) Find video in DB by (session_id, filename)
    3) detect_pose_and_annotate() -> annotated frames
    4) Return { "annotated_frames": [...] }
    """
    data = request.json
    filename = data.get('filename')

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

    # Run pose detection
    annotated_list = detect_pose_and_annotate(video_id, session_id)

    # Build URLs for each annotated image (under /api/annotated/<filename>)
    annotated_urls = []
    for ann_name in annotated_list:
        # We might add a cache-busting param
        annotated_urls.append(f"/api/annotated/{ann_name}")

    return jsonify({
        "message": "Pose detection complete",
        "annotated_frames": annotated_urls
    }), 200

@pose_bp.route('/annotated/<path:filename>')
def serve_annotated_file(filename):
    """
    Serves the annotated frames from 'temp_annotated_frames/'.
    """
    annotated_folder = os.path.join(current_app.root_path, 'temp_annotated_frames')
    return send_from_directory(annotated_folder, filename)
