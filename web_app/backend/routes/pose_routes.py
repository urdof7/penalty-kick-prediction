# web_app/backend/routes/pose_routes.py

import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory, g
from services.db_manager import get_video_by_name, get_pose_data_for_video, insert_engineered_feature, clear_engineered_for_frames
from services.pose_manager import detect_pose_and_annotate
from services.feature_engineering import engineer_features

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

@pose_bp.route("/compute_engineered",methods=["POST"])
def compute_engineered():
    data=request.json
    if "filename" not in data:
        return jsonify({"error":"No filename"}),400
    session_id=getattr(g,"session_id",None)
    if not session_id:
        return jsonify({"error":"No session_id"}),500
    filename=data["filename"]
    row=get_video_by_name(session_id,filename)
    if not row:
        return jsonify({"error":"Video not found"}),404
    video_id=row[0]
    df_raw=get_pose_data_for_video(session_id,video_id)
    if df_raw.empty:
        return jsonify({"error":"No pose data"}),404
    df_pivot=df_raw.pivot_table(
        index="frame_no",
        columns="landmark_name",
        values=["x","y","z"]
    ).reset_index()
    df_pivot.columns=[f"{c[0]}_{c[1]}" if c[1] else c[0] for c in df_pivot.columns]
    if "frame_no_" in df_pivot.columns:
        df_pivot.rename(columns={"frame_no_":"frame_no"},inplace=True)
    df_pivot.sort_values("frame_no",inplace=True)
    df_eng=engineer_features(df_pivot)
    frame_map=df_raw[["frame_id","frame_no"]].drop_duplicates()
    fm=dict(zip(frame_map["frame_no"],frame_map["frame_id"]))
    frame_ids=list(fm.values())
    clear_engineered_for_frames(frame_ids)
    count=0
    for _,r in df_eng.iterrows():
        fn=r["frame_no"]
        if fn in fm:
            f_id=fm[fn]
            x_m=float(r.get("x_mid_hip",0))
            y_m=float(r.get("y_mid_hip",0))
            z_m=float(r.get("z_mid_hip",0))
            a_kl=float(r.get("angle_knee_left",0))
            a_kr=float(r.get("angle_knee_right",0))
            a_el=float(r.get("angle_elbow_left",0))
            a_er=float(r.get("angle_elbow_right",0))
            a_al=float(r.get("angle_ankle_left",0))
            a_ar=float(r.get("angle_ankle_right",0))
            a_fl=float(r.get("angle_foot_left",0))
            a_fr=float(r.get("angle_foot_right",0))
            insert_engineered_feature(f_id,x_m,y_m,z_m,a_kl,a_kr,a_el,a_er,a_al,a_ar,a_fl,a_fr)
            count+=1
    return jsonify({"message":"Engineered features computed","row_count":count}),200

@pose_bp.route('/annotated/<path:filename>')
def serve_annotated_file(filename):
    """
    Serves the annotated frames from 'temp_annotated_frames/'.
    """
    annotated_folder = os.path.join(current_app.root_path, 'temp_annotated_frames')
    return send_from_directory(annotated_folder, filename)
