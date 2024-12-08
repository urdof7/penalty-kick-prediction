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

# ---------------------------------------------------------
# Determine Paths
# ---------------------------------------------------------
# Current file is in: PK_PREDICTION/scripts/data_processing/feature_engineering_single_frame.py
# We need to go up three directories to reach PK_PREDICTION.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed', 'single_frame')

kick_db_path = os.path.join(DATA_DIR, 'kick_data.db')
pose_db_path = os.path.join(DATA_DIR, 'pose_data.db')

os.makedirs(PROCESSED_DIR, exist_ok=True)

# ---------------------------------------------------------
# Connect to Databases
# ---------------------------------------------------------
kick_conn = sqlite3.connect(kick_db_path)
pose_conn = sqlite3.connect(pose_db_path)

# Load Data and Filter for Mid-Swing Frame (frame_no = 11)
df_frames = pd.read_sql_query("SELECT * FROM frames WHERE frame_no = 11", kick_conn)
df_kicks = pd.read_sql_query("SELECT * FROM kicks", kick_conn)
df_pose = pd.read_sql_query("SELECT * FROM pose_features", pose_conn)

kick_conn.close()
pose_conn.close()

# ---------------------------------------------------------
# Merge Data
# ---------------------------------------------------------
df_merged = df_frames.merge(df_kicks, on='kick_id', how='inner')
df_merged = df_merged.merge(df_pose, on='frame_id', how='inner')

# ---------------------------------------------------------
# Pivot so each frame is one row with all landmarks as columns
# ---------------------------------------------------------
df_wide = df_merged.pivot_table(
    index=['frame_id', 'kick_id', 'kick_direction'],
    columns='landmark_name',
    values=['x','y','z','visibility']
).reset_index()

df_wide.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df_wide.columns.values]

def has_landmark(name, axis='x'):
    return f"{axis}_{name}" in df_wide.columns

# ---------------------------------------------------------
# Normalization
# ---------------------------------------------------------
origin_x_col, origin_y_col = None, None

if has_landmark('mid_hip'):
    origin_x_col, origin_y_col = 'x_mid_hip', 'y_mid_hip'
elif has_landmark('left_hip') and has_landmark('right_hip'):
    df_wide['x_mid_hip'] = (df_wide['x_left_hip'] + df_wide['x_right_hip']) / 2.0
    df_wide['y_mid_hip'] = (df_wide['y_left_hip'] + df_wide['y_right_hip']) / 2.0
    origin_x_col, origin_y_col = 'x_mid_hip', 'y_mid_hip'
else:
    if has_landmark('left_shoulder') and has_landmark('right_shoulder'):
        df_wide['x_origin'] = (df_wide['x_left_shoulder'] + df_wide['x_right_shoulder']) / 2.0
        df_wide['y_origin'] = (df_wide['y_left_shoulder'] + df_wide['y_right_shoulder']) / 2.0
        origin_x_col, origin_y_col = 'x_origin', 'y_origin'
    else:
        candidate_joints = ['left_shoulder', 'right_shoulder', 'nose']
        for cj in candidate_joints:
            if has_landmark(cj):
                origin_x_col, origin_y_col = f'x_{cj}', f'y_{cj}'
                break

if has_landmark('left_shoulder') and has_landmark('right_shoulder'):
    scale = (df_wide['x_right_shoulder'] - df_wide['x_left_shoulder']).abs() + 1e-6
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

# ---------------------------------------------------------
# Compute Example Angles 
# ---------------------------------------------------------
if all(has_landmark(l) for l in ['hip_left', 'knee_left', 'ankle_left']):
    df_wide['angle_knee_left'] = df_wide.apply(lambda row: compute_angle(
        (row.get('x_hip_left', 0), row.get('y_hip_left', 0)),
        (row.get('x_knee_left', 0), row.get('y_knee_left', 0)),
        (row.get('x_ankle_left', 0), row.get('y_ankle_left', 0))
    ), axis=1)

# ---------------------------------------------------------
# Save the single-frame training data
# ---------------------------------------------------------
output_path = os.path.join(PROCESSED_DIR, 'training_data_single_frame.csv')
df_wide.to_csv(output_path, index=False)
print(f"Single-frame training data saved to {output_path}")
