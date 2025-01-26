# web_app/backend/routes/pose_routes.py

import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory, g
from services.db_manager import (
    get_video_by_name,
    get_pose_data_for_video,
    insert_engineered_feature,
    clear_engineered_for_frames
)
from services.pose_manager import detect_pose_and_annotate
from services.feature_engineering import engineer_features_2d

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

@pose_bp.route("/compute_engineered", methods=["POST"])
def compute_engineered():
    data = request.json
    if "filename" not in data:
        return jsonify({"error": "No filename"}), 400

    session_id = getattr(g, "session_id", None)
    if not session_id:
        return jsonify({"error": "No session_id"}), 500

    filename = data["filename"]
    row = get_video_by_name(session_id, filename)
    if not row:
        return jsonify({"error": "Video not found"}), 404
    video_id = row[0]

    df_raw = get_pose_data_for_video(session_id, video_id)
    if df_raw.empty:
        return jsonify({"error": "No pose data"}), 404

    # Pivot
    df_pivot = df_raw.pivot_table(
        index="frame_no",
        columns="landmark_name",
        values=["x", "y"]  # ignoring z for pure 2D
    ).reset_index()

    # Flatten columns => x_ankle_left, y_ankle_left, etc.
    df_pivot.columns = [f"{c[0]}_{c[1]}" if c[1] else c[0] for c in df_pivot.columns]
    if "frame_no_" in df_pivot.columns:
        df_pivot.rename(columns={"frame_no_": "frame_no"}, inplace=True)
    df_pivot.sort_values("frame_no", inplace=True)

    # For safety, fill missing columns with 0.0
    needed_cols = [
        "x_hip_left","y_hip_left","x_hip_right","y_hip_right",
        "x_knee_left","y_knee_left","x_knee_right","y_knee_right",
        "x_ankle_left","y_ankle_left","x_ankle_right","y_ankle_right",
        "x_left_foot_index","y_left_foot_index","x_right_foot_index","y_right_foot_index",
        "x_shoulder_left","y_shoulder_left","x_shoulder_right","y_shoulder_right",
        "x_elbow_left","y_elbow_left","x_elbow_right","y_elbow_right",
        "x_wrist_left","y_wrist_left","x_wrist_right","y_wrist_right"
    ]
    for col in needed_cols:
        if col not in df_pivot.columns:
            df_pivot[col] = 0.0

    # Engineer
    df_eng = engineer_features_2d(df_pivot)

    # Map frame_no -> frame_id
    frame_map = df_raw[["frame_id","frame_no"]].drop_duplicates()
    fm = dict(zip(frame_map["frame_no"], frame_map["frame_id"]))

    # Clear old engineered if re-running
    frame_ids = list(fm.values())
    clear_engineered_for_frames(frame_ids)

    count = 0
    for _, row2 in df_eng.iterrows():
        fn = row2["frame_no"]
        if fn in fm:
            f_id = fm[fn]
            insert_engineered_feature(
                f_id,
                row2["x_hip_left"], row2["y_hip_left"],
                row2["x_hip_right"], row2["y_hip_right"],
                row2["x_knee_left"], row2["y_knee_left"],
                row2["x_knee_right"], row2["y_knee_right"],
                row2["x_ankle_left"], row2["y_ankle_left"],
                row2["x_ankle_right"], row2["y_ankle_right"],
                row2["x_left_foot_index"], row2["y_left_foot_index"],
                row2["x_right_foot_index"], row2["y_right_foot_index"],
                row2["x_shoulder_left"], row2["y_shoulder_left"],
                row2["x_shoulder_right"], row2["y_shoulder_right"],
                row2["x_elbow_left"], row2["y_elbow_left"],
                row2["x_elbow_right"], row2["y_elbow_right"],
                row2["x_wrist_left"], row2["y_wrist_left"],
                row2["x_wrist_right"], row2["y_wrist_right"],
                row2["angle_knee_left"], row2["angle_knee_right"],
                row2["angle_elbow_left"], row2["angle_elbow_right"],
                row2["angle_ankle_left"], row2["angle_ankle_right"],
                row2["angle_foot_left"], row2["angle_foot_right"]
            )
            count += 1

    return jsonify({"message":"Engineered features computed","row_count":count}),200

@pose_bp.route('/annotated/<path:filename>')
def serve_annotated_file(filename):
    """
    Serves the annotated frames from 'temp_annotated_frames/'.
    """
    annotated_folder = os.path.join(current_app.root_path, 'temp_annotated_frames')
    return send_from_directory(annotated_folder, filename)
