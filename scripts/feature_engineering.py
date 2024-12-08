import os
import sqlite3
import pandas as pd
import numpy as np
from math import atan2, degrees

def compute_angle(p1, p2, p3):
    # Compute the angle at p2 formed by p1->p2->p3
    v1 = (p1[0]-p2[0], p1[1]-p2[1])
    v2 = (p3[0]-p2[0], p3[1]-p2[1])
    angle = degrees(atan2(v2[1], v2[0]) - atan2(v1[1], v1[0]))
    return angle + 360 if angle < 0 else angle

# Determine project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

kick_db_path = os.path.join(DATA_DIR, 'kick_data.db')
pose_db_path = os.path.join(DATA_DIR, 'pose_data.db')

# Connect to databases
kick_conn = sqlite3.connect(kick_db_path)
pose_conn = sqlite3.connect(pose_db_path)

df_frames = pd.read_sql_query("SELECT frame_id, kick_id, video_id, frame_no, frame_path FROM frames", kick_conn)
df_kicks = pd.read_sql_query("SELECT * FROM kicks", kick_conn)
df_pose = pd.read_sql_query("SELECT * FROM pose_features", pose_conn)

kick_conn.close()
pose_conn.close()

# Merge data
df_merged = df_pose.merge(df_frames, on='frame_id', how='inner').merge(df_kicks, on='kick_id', how='inner')

df_wide = df_merged.pivot_table(
    index=['frame_id', 'kick_id', 'kick_direction'],
    columns='landmark_name',
    values=['x','y','z','visibility']
).reset_index()

# Flatten multi-level columns
df_wide.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df_wide.columns.values]

# Collect available landmarks
landmarks = {c.split('_',1)[1] for c in df_wide.columns if '_' in c}
def has_landmark(name, axis='x'):
    return f"{axis}_{name}" in df_wide.columns

# Try to find a reference for translation
origin_x_col, origin_y_col = None, None
scale_reference = None

# 1) If mid_hip present
if has_landmark('mid_hip'):
    origin_x_col = 'x_mid_hip'
    origin_y_col = 'y_mid_hip'
elif has_landmark('left_hip') and has_landmark('right_hip'):
    # Compute mid_hip from hips
    df_wide['x_mid_hip'] = (df_wide['x_left_hip'] + df_wide['x_right_hip']) / 2.0
    df_wide['y_mid_hip'] = (df_wide['y_left_hip'] + df_wide['y_right_hip']) / 2.0
    origin_x_col = 'x_mid_hip'
    origin_y_col = 'y_mid_hip'
else:
    # Fallback: try shoulders
    if has_landmark('left_shoulder') and has_landmark('right_shoulder'):
        df_wide['x_origin'] = (df_wide['x_left_shoulder'] + df_wide['x_right_shoulder']) / 2.0
        df_wide['y_origin'] = (df_wide['y_left_shoulder'] + df_wide['y_right_shoulder']) / 2.0
        origin_x_col = 'x_origin'
        origin_y_col = 'y_origin'
    else:
        # If no pairs found, pick a single joint that is most likely present (e.g., left_shoulder)
        # If that joint isn't present, we just won't translate.
        candidate_joints = ['left_shoulder', 'right_shoulder', 'nose', 'left_eye', 'right_eye']
        for cj in candidate_joints:
            if has_landmark(cj):
                origin_x_col = f'x_{cj}'
                origin_y_col = f'y_{cj}'
                break

# Scaling factor
# Prefer shoulders for scale if available
if has_landmark('left_shoulder') and has_landmark('right_shoulder'):
    scale = (df_wide['x_right_shoulder'] - df_wide['x_left_shoulder']).abs() + 1e-6
else:
    # If no shoulders, default scale=1.0
    scale = 1.0

# Translation and scaling
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
else:
    # No origin found, skip translation and scaling
    # Data remains as-is, which is not ideal but a fallback
    pass

# Compute angles if landmarks exist
if all(has_landmark(l) for l in ['hip_left', 'knee_left', 'ankle_left']):
    df_wide['angle_knee_left'] = df_wide.apply(lambda row: compute_angle(
        (row.get('x_hip_left', 0), row.get('y_hip_left', 0)),
        (row.get('x_knee_left', 0), row.get('y_knee_left', 0)),
        (row.get('x_ankle_left', 0), row.get('y_ankle_left', 0))
    ), axis=1)

processed_dir = os.path.join(DATA_DIR, 'processed')
os.makedirs(processed_dir, exist_ok=True)
output_path = os.path.join(processed_dir, 'training_data.csv')
df_wide.to_csv(output_path, index=False)
print(f"Processed data saved to {output_path}")
