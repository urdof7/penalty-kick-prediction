import os
import sqlite3
import pandas as pd
import numpy as np
from math import atan2, degrees

# Configuration flags
PAD_SEQUENCES = False  # Set to True to enable padding/truncation, False to exclude non-matching lengths
MIN_FRAMES = 10  # Example threshold if you want to exclude sequences shorter than this if not padding

def compute_angle(p1, p2, p3):
    v1 = (p1[0]-p2[0], p1[1]-p2[1])
    v2 = (p3[0]-p2[0], p3[1]-p2[1])
    angle = degrees(atan2(v2[1], v2[0]) - atan2(v1[1], v1[0]))
    return angle + 360 if angle < 0 else angle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Backend base directory
DATA_DIR = os.path.join(BASE_DIR, 'data')
SEQUENCE_DIR = os.path.join(DATA_DIR, 'processed', 'sequence')
kick_db_path = os.path.join(DATA_DIR, 'kick_data.db')
pose_db_path = os.path.join(DATA_DIR, 'pose_data.db')

os.makedirs(SEQUENCE_DIR, exist_ok=True)

kick_conn = sqlite3.connect(kick_db_path)
pose_conn = sqlite3.connect(pose_db_path)

df_kicks = pd.read_sql_query("SELECT * FROM kicks", kick_conn)
df_frames = pd.read_sql_query("SELECT * FROM frames", kick_conn)
df_pose = pd.read_sql_query("SELECT * FROM pose_features", pose_conn)

kick_conn.close()
pose_conn.close()

df_merged = df_frames.merge(df_pose, on='frame_id', how='inner').merge(df_kicks, on='kick_id', how='inner')

# Determine maximum frames
kick_frame_counts = df_frames.groupby('kick_id')['frame_no'].count()
MAX_FRAMES = kick_frame_counts.max()

def normalize_landmark_names(df):
    df.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df.columns]
    visibility_cols = [c for c in df.columns if c.startswith('visibility_')]
    df.drop(columns=visibility_cols, inplace=True, errors='ignore')
    
    def norm_name(col):
        if '_' not in col:
            return col
        prefix, landmark = col.split('_', 1)
        landmark = landmark.lower()
        parts = landmark.split('_')
        if len(parts) == 2:
            side, joint = parts
            landmark = f"{joint}_{side}"
        return f"{prefix}_{landmark}"
    df.columns = [norm_name(c) for c in df.columns]
    return df

def has_landmark(df, name, axis='x'):
    return f"{axis}_{name}" in df.columns

def compute_angles(df):
    def add_angle_feature(df, joint_center, joint_1, joint_2, angle_name):
        if (has_landmark(df, joint_center) and has_landmark(df, joint_1) and has_landmark(df, joint_2) and
            has_landmark(df, joint_center, 'y') and has_landmark(df, joint_1, 'y') and has_landmark(df, joint_2, 'y')):
            df[angle_name] = df.apply(lambda row: compute_angle(
                (row[f'x_{joint_1}'], row[f'y_{joint_1}']),
                (row[f'x_{joint_center}'], row[f'y_{joint_center}']),
                (row[f'x_{joint_2}'], row[f'y_{joint_2}'])
            ), axis=1)
    add_angle_feature(df, 'knee_left', 'hip_left', 'ankle_left', 'angle_knee_left')
    add_angle_feature(df, 'knee_right', 'hip_right', 'ankle_right', 'angle_knee_right')
    add_angle_feature(df, 'elbow_left', 'shoulder_left', 'wrist_left', 'angle_elbow_left')
    add_angle_feature(df, 'elbow_right', 'shoulder_right', 'wrist_right', 'angle_elbow_right')

def normalize_frames(df, ref_frame_no=11):
    ref_frame = df[df['frame_no'] == ref_frame_no]
    if ref_frame.empty:
        # Use the first frame as reference if mid-swing isn't found
        ref_frame = df.iloc[[0]]
    ref_row = ref_frame.iloc[0]
    
    def frame_has_landmark(name, axis='x'):
        return f"{axis}_{name}" in ref_row.index
    
    if frame_has_landmark('mid_hip'):
        origin_x_col, origin_y_col = 'x_mid_hip', 'y_mid_hip'
    elif frame_has_landmark('hip_left') and frame_has_landmark('hip_right'):
        df['x_mid_hip'] = (df['x_hip_left'] + df['x_hip_right']) / 2.0
        df['y_mid_hip'] = (df['y_hip_left'] + df['y_hip_right']) / 2.0
        origin_x_col, origin_y_col = 'x_mid_hip', 'y_mid_hip'
    else:
        origin_x_col, origin_y_col = None, None
        if frame_has_landmark('shoulder_left') and frame_has_landmark('shoulder_right'):
            df['x_origin'] = (df['x_shoulder_left'] + df['x_shoulder_right']) / 2.0
            df['y_origin'] = (df['y_shoulder_left'] + df['y_shoulder_right']) / 2.0
            origin_x_col, origin_y_col = 'x_origin', 'y_origin'
        else:
            candidates = ['shoulder_left', 'shoulder_right', 'nose']
            for cj in candidates:
                if frame_has_landmark(cj):
                    origin_x_col, origin_y_col = f'x_{cj}', f'y_{cj}'
                    break
    
    if frame_has_landmark('shoulder_left') and frame_has_landmark('shoulder_right'):
        scale = (ref_row['x_shoulder_right'] - ref_row['x_shoulder_left'])
        if scale == 0:
            scale = 1e-6
    else:
        scale = 1.0
    
    if origin_x_col and origin_y_col:
        ref_x = df[origin_x_col]
        ref_y = df[origin_y_col]
        for c in df.columns:
            if c.startswith('x_'):
                df[c] = (df[c] - ref_x) / scale
            elif c.startswith('y_'):
                df[c] = (df[c] - ref_y) / scale
            elif c.startswith('z_'):
                df[c] = df[c] / scale

X_list = []
y_list = []

for kick_id in df_kicks['kick_id'].unique():
    kick_data = df_merged[df_merged['kick_id'] == kick_id]
    if kick_data.empty:
        continue

    frame_pivot = kick_data.pivot_table(
        index=['frame_id', 'kick_id', 'kick_direction', 'frame_no'],
        columns='landmark_name',
        values=['x','y','z','visibility']
    ).reset_index()

    frame_pivot = normalize_landmark_names(frame_pivot)
    normalize_frames(frame_pivot, ref_frame_no=11)
    compute_angles(frame_pivot)

    target = frame_pivot['kick_direction'].iloc[0]
    non_feature_cols = ['frame_id','kick_id','kick_direction','frame_no']
    feature_cols = [c for c in frame_pivot.columns if c not in non_feature_cols]

    frame_pivot = frame_pivot.sort_values('frame_no')
    kick_features = frame_pivot[feature_cols].values
    num_frames = kick_features.shape[0]

    if PAD_SEQUENCES:
        # With padding/truncation
        if num_frames < MAX_FRAMES:
            pad_amount = MAX_FRAMES - num_frames
            pad_array = np.zeros((pad_amount, kick_features.shape[1]))
            kick_features = np.concatenate([kick_features, pad_array], axis=0)
        elif num_frames > MAX_FRAMES:
            kick_features = kick_features[:MAX_FRAMES]
        X_list.append(kick_features)
        y_list.append(target)
    else:
        # Without padding: consider only sequences that meet length criteria
        # For example, only include those with at least MIN_FRAMES frames
        # and at most MAX_FRAMES if you want exact length or some range.
        # Here we require exactly MAX_FRAMES for simplicity:
        if num_frames == MAX_FRAMES and num_frames >= MIN_FRAMES:
            X_list.append(kick_features)
            y_list.append(target)
        # else discard this kick

X_seq = np.stack(X_list, axis=0) if X_list else np.empty((0, MAX_FRAMES, len(feature_cols)))
y_seq = np.array(y_list) if y_list else np.empty((0,))

output_path = os.path.join(SEQUENCE_DIR, 'training_data_sequence.npz')
np.savez(output_path, X_seq=X_seq, y_seq=y_seq)

rel_path = os.path.relpath(output_path, BASE_DIR)
print(f"Sequence training data saved to {rel_path}")
