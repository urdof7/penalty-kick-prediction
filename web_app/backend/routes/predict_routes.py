# web_app/backend/routes/predict_routes.py

from flask import Blueprint, request, jsonify, g
import numpy as np
import pandas as pd
from math import atan2, degrees

from services.db_manager import get_video_by_name, get_pose_data_for_video
from services.model_loader import sequence_LSTM_model

predict_bp = Blueprint('predict_bp', __name__)

# --------------------------- HELPER FUNCTIONS ---------------------------

def compute_angle_3pts(p1, p2, p3):
    """
    p1, p2, p3 are (x, y).
    Compute the angle at p2 formed by p1->p2 and p3->p2, range [0..360).
    """
    v1 = (p1[0] - p2[0], p1[1] - p2[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    angle_deg = degrees(atan2(v2[1], v2[0]) - atan2(v1[1], v1[0]))
    return angle_deg + 360 if angle_deg < 0 else angle_deg

def add_angle_feature(df, center_col_prefix, p1_col_prefix, p2_col_prefix, angle_name):
    """
    df has columns like x_ankle_left, y_ankle_left, etc.
    We'll compute the angle at 'center' formed by (p1->center, p2->center).
    """
    # e.g. center_col_prefix='knee_left' => x_knee_left, y_knee_left
    xc, yc = f'x_{center_col_prefix}', f'y_{center_col_prefix}'
    xp1, yp1 = f'x_{p1_col_prefix}', f'y_{p1_col_prefix}'
    xp2, yp2 = f'x_{p2_col_prefix}', f'y_{p2_col_prefix}'

    if all(col in df.columns for col in [xc,yc,xp1,yp1,xp2,yp2]):
        def calc_angle(row):
            p1 = (row[xp1], row[yp1])
            c  = (row[xc],  row[yc])
            p2 = (row[xp2], row[yp2])
            return compute_angle_3pts(p1, c, p2)

        df[angle_name] = df.apply(calc_angle, axis=1)
    else:
        df[angle_name] = 0.0  # fallback if columns not found

# --------------------------- MAIN ROUTE ---------------------------

@predict_bp.route('/predict_kick', methods=['POST'])
def predict_kick():
    """
    JSON: { "filename": <str> }
    1) get video_id from (session_id, filename)
    2) gather frames+pose for that video
    3) pivot into EXACT columns used at training (48 columns)
    4) compute x_mid_hip, angles, etc.
    5) shape => (1, time_steps, 48), flatten->scale->reshape
    6) model.predict => quadrant_probs
    """
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

    # 1) Get the raw DataFrame
    df = get_pose_data_for_video(session_id, video_id)
    if df.empty:
        return jsonify({"error": "No pose data for this video"}), 404

    # 2) pivot: each row = 1 frame_no, columns = x_ankle_left, y_ankle_left, z_ankle_left, ...
    #    pivot index => 'frame_no'
    #    pivot columns => 'landmark_name'
    #    values => ['x','y','z']
    df_pivot = df.pivot_table(
        index='frame_no',
        columns='landmark_name',
        values=['x','y','z']
    ).reset_index()

    # Flatten columns => x_ankle_left, y_ankle_left, z_ankle_left, ...
    df_pivot.columns = [
        f"{col[0]}_{col[1]}" if col[1] else col[0]
        for col in df_pivot.columns
    ]
    # 'frame_no' is now a column named 'frame_no_'

    # rename 'frame_no_' => 'frame_no' if needed
    if 'frame_no_' in df_pivot.columns:
        df_pivot.rename(columns={'frame_no_':'frame_no'}, inplace=True)

    # 3) sort by frame_no
    df_pivot.sort_values('frame_no', inplace=True)

    # 4) compute x_mid_hip / y_mid_hip
    #    => average x_hip_left, x_hip_right => x_mid_hip
    #    => average y_hip_left, y_hip_right => y_mid_hip
    if 'x_hip_left' in df_pivot.columns and 'x_hip_right' in df_pivot.columns:
        df_pivot['x_mid_hip'] = (df_pivot['x_hip_left'] + df_pivot['x_hip_right']) / 2.0
    else:
        df_pivot['x_mid_hip'] = 0.0

    if 'y_hip_left' in df_pivot.columns and 'y_hip_right' in df_pivot.columns:
        df_pivot['y_mid_hip'] = (df_pivot['y_hip_left'] + df_pivot['y_hip_right']) / 2.0
    else:
        df_pivot['y_mid_hip'] = 0.0

    # 5) compute angles => knee_left, knee_right, elbow_left, elbow_right
    add_angle_feature(df_pivot, 'knee_left', 'hip_left', 'ankle_left', 'angle_knee_left')
    add_angle_feature(df_pivot, 'knee_right','hip_right','ankle_right','angle_knee_right')
    add_angle_feature(df_pivot, 'elbow_left','shoulder_left','wrist_left','angle_elbow_left')
    add_angle_feature(df_pivot, 'elbow_right','shoulder_right','wrist_right','angle_elbow_right')

    # 6) EXACT columns => 48 total
    #    e.g. 
    #       x_ankle_left, x_elbow_left, x_left_foot_index, x_hip_left, ...
    #       y_ankle_left, y_elbow_left, ...
    #       z_ankle_left, ...
    #       x_mid_hip, y_mid_hip,
    #       angle_knee_left, angle_knee_right, angle_elbow_left, angle_elbow_right
    #    We'll define them explicitly:
    feature_cols = [
        'x_ankle_left','x_elbow_left','x_left_foot_index','x_hip_left','x_knee_left','x_shoulder_left','x_wrist_left','x_ankle_right','x_elbow_right','x_right_foot_index','x_hip_right','x_knee_right','x_shoulder_right','x_wrist_right',
        'y_ankle_left','y_elbow_left','y_left_foot_index','y_hip_left','y_knee_left','y_shoulder_left','y_wrist_left','y_ankle_right','y_elbow_right','y_right_foot_index','y_hip_right','y_knee_right','y_shoulder_right','y_wrist_right',
        'z_ankle_left','z_elbow_left','z_left_foot_index','z_hip_left','z_knee_left','z_shoulder_left','z_wrist_left','z_ankle_right','z_elbow_right','z_right_foot_index','z_hip_right','z_knee_right','z_shoulder_right','z_wrist_right',
        'x_mid_hip','y_mid_hip',
        'angle_knee_left','angle_knee_right','angle_elbow_left','angle_elbow_right'
    ]
    # Check if all exist; if not, fill missing with 0.0
    for col in feature_cols:
        if col not in df_pivot.columns:
            df_pivot[col] = 0

    # Reorder
    df_pivot = df_pivot[['frame_no'] + feature_cols]  # keep frame_no around if you want, or drop it

    # 7) Build the final feature array => shape (time_steps, 48)
    arr = df_pivot[feature_cols].values
    time_steps, feat_count = arr.shape

    # 8) pad/trim to 21 frames
    required_timesteps = 21
    if time_steps < required_timesteps:
        pad_count = required_timesteps - time_steps
        pad_arr = np.zeros((pad_count, feat_count), dtype=np.float32)
        arr = np.concatenate([arr, pad_arr], axis=0)
        time_steps = required_timesteps
    elif time_steps > required_timesteps:
        arr = arr[:required_timesteps]

    arr_3d = arr.reshape((1,required_timesteps,feat_count))  # (1,21,48)

    # 9) Let the model do flatten->scale->reshape internally
    probs = sequence_LSTM_model.predict_quadrant_probs(arr_3d)

    return jsonify({
        "message": "Kick direction predicted from DB pose features (48 columns)",
        "quadrant_probs": probs
    }), 200
