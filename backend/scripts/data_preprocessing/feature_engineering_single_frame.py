import os
import sqlite3
import pandas as pd
import numpy as np
from math import atan2, degrees

def compute_angle(p1, p2, p3):
    # Compute angle at p2 formed by p1->p2->p3
    v1 = (p1[0]-p2[0], p1[1]-p2[1])
    v2 = (p3[0]-p2[0], p3[1]-p2[1])
    angle = degrees(atan2(v2[1], v2[0]) - atan2(v1[1], v1[0]))
    return angle + 360 if angle < 0 else angle

# Determine BASE_DIR relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Backend base directory
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed', 'single_frame')
kick_db_path = os.path.join(DATA_DIR, 'kick_data.db')
pose_db_path = os.path.join(DATA_DIR, 'pose_data.db')

os.makedirs(PROCESSED_DIR, exist_ok=True)

# Connect to Databases
kick_conn = sqlite3.connect(kick_db_path)
pose_conn = sqlite3.connect(pose_db_path)

# Load Data for mid-swing frame_no = 11
df_frames = pd.read_sql_query("SELECT * FROM frames WHERE frame_no = 11", kick_conn)
df_kicks = pd.read_sql_query("SELECT * FROM kicks", kick_conn)
df_pose = pd.read_sql_query("SELECT * FROM pose_features", pose_conn)

kick_conn.close()
pose_conn.close()

# Merge Data
df_merged = df_frames.merge(df_kicks, on='kick_id', how='inner')
df_merged = df_merged.merge(df_pose, on='frame_id', how='inner')

# Pivot
df_wide = df_merged.pivot_table(
    index=['frame_id', 'kick_id', 'kick_direction'],
    columns='landmark_name',
    values=['x','y','z','visibility']
).reset_index()

# Flatten columns
df_wide.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df_wide.columns]

# Remove visibility columns
visibility_cols = [c for c in df_wide.columns if c.startswith('visibility_')]
df_wide.drop(columns=visibility_cols, inplace=True)

# Normalize Landmark Names to lowercase and standard form: joint_side
def normalize_landmark_name(col):
    if '_' not in col:
        return col
    prefix, landmark = col.split('_', 1)  # e.g., x_LEFT_HIP
    landmark = landmark.lower()  # left_hip
    # Convert left_hip -> hip_left
    parts = landmark.split('_')
    if len(parts) == 2:
        side, joint = parts
        # Convert [left|right]_[joint] to joint_side
        landmark = f"{joint}_{side}"
    return f"{prefix}_{landmark}"

df_wide.columns = [normalize_landmark_name(c) for c in df_wide.columns]

def has_landmark(name, axis='x'):
    return f"{axis}_{name}" in df_wide.columns

# Normalization
origin_x_col, origin_y_col = None, None

if has_landmark('mid_hip'):
    origin_x_col, origin_y_col = 'x_mid_hip', 'y_mid_hip'
elif has_landmark('hip_left') and has_landmark('hip_right'):
    df_wide['x_mid_hip'] = (df_wide['x_hip_left'] + df_wide['x_hip_right']) / 2.0
    df_wide['y_mid_hip'] = (df_wide['y_hip_left'] + df_wide['y_hip_right']) / 2.0
    origin_x_col, origin_y_col = 'x_mid_hip', 'y_mid_hip'
else:
    if has_landmark('shoulder_left') and has_landmark('shoulder_right'):
        df_wide['x_origin'] = (df_wide['x_shoulder_left'] + df_wide['x_shoulder_right']) / 2.0
        df_wide['y_origin'] = (df_wide['y_shoulder_left'] + df_wide['y_shoulder_right']) / 2.0
        origin_x_col, origin_y_col = 'x_origin', 'y_origin'
    else:
        candidate_joints = ['shoulder_left', 'shoulder_right', 'nose']
        for cj in candidate_joints:
            if has_landmark(cj):
                origin_x_col, origin_y_col = f'x_{cj}', f'y_{cj}'
                break

if has_landmark('shoulder_left') and has_landmark('shoulder_right'):
    scale = (df_wide['x_shoulder_right'] - df_wide['x_shoulder_left']).abs() + 1e-6
else:
    scale = 1.0

if origin_x_col and origin_y_col:
    ref_x = df_wide[origin_x_col]
    ref_y = df_wide[origin_y_col]
    for c in df_wide.columns:
        if c.startswith('x_'):
            df_wide[c] = (df_wide[c] - ref_x) / scale
        elif c.startswith('y_'):
            df_wide[c] = (df_wide[c] - ref_y) / scale
        elif c.startswith('z_'):
            df_wide[c] = df_wide[c] / scale

def add_angle_feature(df, joint_center, joint_1, joint_2, angle_name):
    if (has_landmark(joint_center) and has_landmark(joint_1) and has_landmark(joint_2) and
        has_landmark(joint_center, 'y') and has_landmark(joint_1, 'y') and has_landmark(joint_2, 'y')):
        df[angle_name] = df.apply(lambda row: compute_angle(
            (row[f'x_{joint_1}'], row[f'y_{joint_1}']),
            (row[f'x_{joint_center}'], row[f'y_{joint_center}']),
            (row[f'x_{joint_2}'], row[f'y_{joint_2}'])
        ), axis=1)

# Add angles
add_angle_feature(df_wide, 'knee_left', 'hip_left', 'ankle_left', 'angle_knee_left')
add_angle_feature(df_wide, 'knee_right', 'hip_right', 'ankle_right', 'angle_knee_right')
add_angle_feature(df_wide, 'elbow_left', 'shoulder_left', 'wrist_left', 'angle_elbow_left')
add_angle_feature(df_wide, 'elbow_right', 'shoulder_right', 'wrist_right', 'angle_elbow_right')

# We keep frame_id but drop kick_id now
df_wide.drop(columns=['kick_id'], inplace=True, errors='ignore')

output_filename = 'training_data_single_frame.csv'
output_path = os.path.join(PROCESSED_DIR, output_filename)
df_wide.to_csv(output_path, index=False)

rel_path = os.path.relpath(output_path, BASE_DIR)
print(f"Single-frame training data saved to {rel_path}")
