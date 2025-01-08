# web_app/backend/routes/dev_routes.py

import os
import os
from flask import Blueprint, request, jsonify, current_app
from services.db_manager import get_connection
from services.file_cleanup import remove_files_in_folder

# We'll call the secret PK_DEV_SECRET
PK_DEV_SECRET = os.environ.get("PK_DEV_SECRET", None)

dev_bp = Blueprint('dev_bp', __name__)

@dev_bp.route('/nuke_all', methods=['POST'])
def dev_nuke_all():
    """
    Completely wipes ALL data from the database (all sessions, videos, frames, pose_features, etc.)
    and removes all files from 'uploads/', 'temp_frames/', and 'temp_annotated_frames/'.

    Developer-only. Not exposed in the front-end UI. Must provide ?secret= or x-dev-secret header
    matching the PK_DEV_SECRET environment variable.

    Example usage:
      curl -X POST "http://localhost:8098/api/dev/nuke_all?secret=YOUR_SECRET"
      OR
      curl -X POST http://localhost:8098/api/dev/nuke_all -H "x-dev-secret: YOUR_SECRET"
    """
    # 1) Check the secret
    secret_param = request.args.get('secret') or request.headers.get('x-dev-secret')
    if not PK_DEV_SECRET or secret_param != PK_DEV_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # 2) Nuke DB tables
        conn = get_connection()
        cur = conn.cursor()

        # Wipe everything in your tables as needed:
        cur.execute("DELETE FROM pose_features;")
        cur.execute("DELETE FROM frames;")
        cur.execute("DELETE FROM kicks;")
        cur.execute("DELETE FROM videos;")
        # When we add engineered_features table, add:
        # cur.execute("DELETE FROM engineered_features;")

        conn.commit()
        conn.close()

        # 3) Remove all files from these folders
        upload_folder = os.path.join(current_app.root_path, 'uploads')
        temp_frames_folder = os.path.join(current_app.root_path, 'temp_frames')
        temp_annotated_folder = os.path.join(current_app.root_path, 'temp_annotated_frames')

        for folder in [upload_folder, temp_frames_folder, temp_annotated_folder]:
            if os.path.isdir(folder):
                for fname in os.listdir(folder):
                    fpath = os.path.join(folder, fname)
                    if os.path.isfile(fpath):
                        os.remove(fpath)

        return jsonify({"message": "All data and files have been nuked!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
