# web_app/backend/routes/predict_routes.py

from flask import Blueprint, request, jsonify, g
import numpy as np
import pandas as pd
from services.db_manager import get_video_by_name, get_engineered_data
from services.model_loader import sequence_LSTM_model

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/predict_kick', methods=['POST'])
def predict_kick():
    data = request.json
    if not data or 'filename' not in data:
        return jsonify({"error": "No filename provided"}), 400

    session_id = getattr(g, 'session_id', None)
    if not session_id:
        return jsonify({"error": "No session_id found"}), 500

    filename = data['filename']
    row = get_video_by_name(session_id, filename)
    if not row:
        return jsonify({"error": "Video not found for this session"}), 404
    video_id = row[0]

    # 1) Fetch from engineered_features
    df = get_engineered_data(session_id, video_id)
    if df.empty:
        return jsonify({"error": "No engineered features found for this video"}), 404

    # 2) We have columns like x_hip_left, y_hip_left, angle_knee_left, etc. + frame_no
    #    Sort by frame_no
    df.sort_values('frame_no', inplace=True)

    # 3) Define that exact order the model expects:
    feature_cols = [
      # e.g. x_hip_left, y_hip_left, x_hip_right, y_hip_right, x_knee_left, ...
      # plus angles. EXACTLY match your training order
      'x_hip_left','y_hip_left',
      'x_hip_right','y_hip_right',
      'x_knee_left','y_knee_left',
      'x_knee_right','y_knee_right',
      'x_ankle_left','y_ankle_left',
      'x_ankle_right','y_ankle_right',
      'x_left_foot_index','y_left_foot_index',
      'x_right_foot_index','y_right_foot_index',
      'x_shoulder_left','y_shoulder_left',
      'x_shoulder_right','y_shoulder_right',
      'x_elbow_left','y_elbow_left',
      'x_elbow_right','y_elbow_right',
      'x_wrist_left','y_wrist_left',
      'x_wrist_right','y_wrist_right',
      'angle_knee_left','angle_knee_right',
      'angle_elbow_left','angle_elbow_right',
      'angle_ankle_left','angle_ankle_right',
      'angle_foot_left','angle_foot_right',
    ]

    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0.0

    arr = df[feature_cols].values
    time_steps, feat_count = arr.shape

    required_timesteps = 21
    if time_steps < required_timesteps:
        pad_count = required_timesteps - time_steps
        pad_arr = np.zeros((pad_count, feat_count), dtype=np.float32)
        arr = np.concatenate([arr, pad_arr], axis=0)
    elif time_steps > required_timesteps:
        arr = arr[:required_timesteps]

    arr_3d = arr.reshape((1, required_timesteps, feat_count))

    # 4) Predict with LSTM
    probs = sequence_LSTM_model.predict_quadrant_probs(arr_3d)

    return jsonify({
        "message": f"Kick direction predicted using {feat_count} features from engineered_features",
        "quadrant_probs": probs
    }), 200
