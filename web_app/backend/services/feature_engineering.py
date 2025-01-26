import pandas as pd
import numpy as np
from math import atan2, degrees

def compute_angle_3pts(a, b, c):
    angle_deg = degrees(atan2(c[1]-b[1], c[0]-b[0]) - atan2(a[1]-b[1], a[0]-b[0]))
    return angle_deg + 360 if angle_deg < 0 else angle_deg

def transform_skeleton_2d(df):
    # 1) compute mid-hip
    if "x_hip_left" in df.columns and "x_hip_right" in df.columns:
        df["x_mid_hip"] = (df["x_hip_left"] + df["x_hip_right"]) / 2.0
    else:
        df["x_mid_hip"] = 0.0

    if "y_hip_left" in df.columns and "y_hip_right" in df.columns:
        df["y_mid_hip"] = (df["y_hip_left"] + df["y_hip_right"]) / 2.0
    else:
        df["y_mid_hip"] = 0.0

    # 2) subtract mid_hip from all x_, y_
    for col in df.columns:
        if col.startswith("x_"):
            df[col] = df[col] - df["x_mid_hip"]
        elif col.startswith("y_"):
            df[col] = df[col] - df["y_mid_hip"]

    # 3) scale by shoulder distance
    dx = 0.0
    dy = 0.0
    if "x_shoulder_left" in df.columns and "x_shoulder_right" in df.columns:
        dx = df["x_shoulder_right"] - df["x_shoulder_left"]
    if "y_shoulder_left" in df.columns and "y_shoulder_right" in df.columns:
        dy = df["y_shoulder_right"] - df["y_shoulder_left"]

    shoulder_dist = np.sqrt(dx*dx + dy*dy)
    shoulder_dist[shoulder_dist < 1e-6] = 1.0

    for col in df.columns:
        if col.startswith("x_") or col.startswith("y_"):
            df[col] = df[col] / shoulder_dist

def angle_knee_left(df):
    if all(c in df.columns for c in ["x_hip_left","y_hip_left","x_knee_left","y_knee_left","x_ankle_left","y_ankle_left"]):
        return df.apply(lambda r: compute_angle_3pts(
            (r["x_hip_left"], r["y_hip_left"]),
            (r["x_knee_left"], r["y_knee_left"]),
            (r["x_ankle_left"], r["y_ankle_left"])
        ), axis=1)
    return 0.0

def angle_knee_right(df):
    if all(c in df.columns for c in ["x_hip_right","y_hip_right","x_knee_right","y_knee_right","x_ankle_right","y_ankle_right"]):
        return df.apply(lambda r: compute_angle_3pts(
            (r["x_hip_right"], r["y_hip_right"]),
            (r["x_knee_right"], r["y_knee_right"]),
            (r["x_ankle_right"], r["y_ankle_right"])
        ), axis=1)
    return 0.0

def angle_elbow_left(df):
    if all(c in df.columns for c in ["x_shoulder_left","y_shoulder_left","x_elbow_left","y_elbow_left","x_wrist_left","y_wrist_left"]):
        return df.apply(lambda r: compute_angle_3pts(
            (r["x_shoulder_left"], r["y_shoulder_left"]),
            (r["x_elbow_left"], r["y_elbow_left"]),
            (r["x_wrist_left"], r["y_wrist_left"])
        ), axis=1)
    return 0.0

def angle_elbow_right(df):
    if all(c in df.columns for c in ["x_shoulder_right","y_shoulder_right","x_elbow_right","y_elbow_right","x_wrist_right","y_wrist_right"]):
        return df.apply(lambda r: compute_angle_3pts(
            (r["x_shoulder_right"], r["y_shoulder_right"]),
            (r["x_elbow_right"], r["y_elbow_right"]),
            (r["x_wrist_right"], r["y_wrist_right"])
        ), axis=1)
    return 0.0

def angle_ankle_left(df):
    if all(c in df.columns for c in ["x_knee_left","y_knee_left","x_ankle_left","y_ankle_left","x_left_foot_index","y_left_foot_index"]):
        return df.apply(lambda r: compute_angle_3pts(
            (r["x_knee_left"], r["y_knee_left"]),
            (r["x_ankle_left"], r["y_ankle_left"]),
            (r["x_left_foot_index"], r["y_left_foot_index"])
        ), axis=1)
    return 0.0

def angle_ankle_right(df):
    if all(c in df.columns for c in ["x_knee_right","y_knee_right","x_ankle_right","y_ankle_right","x_right_foot_index","y_right_foot_index"]):
        return df.apply(lambda r: compute_angle_3pts(
            (r["x_knee_right"], r["y_knee_right"]),
            (r["x_ankle_right"], r["y_ankle_right"]),
            (r["x_right_foot_index"], r["y_right_foot_index"])
        ), axis=1)
    return 0.0

def angle_foot_left(df):
    if all(c in df.columns for c in ["x_ankle_left","y_ankle_left","x_left_foot_index","y_left_foot_index"]):
        return df.apply(lambda r: compute_angle_3pts(
            (r["x_ankle_left"], r["y_ankle_left"]),
            (r["x_left_foot_index"], r["y_left_foot_index"]),
            (r["x_ankle_left"]+0.01, r["y_ankle_left"])  # a small offset in x for reference
        ), axis=1)
    return 0.0

def angle_foot_right(df):
    if all(c in df.columns for c in ["x_ankle_right","y_ankle_right","x_right_foot_index","y_right_foot_index"]):
        return df.apply(lambda r: compute_angle_3pts(
            (r["x_ankle_right"], r["y_ankle_right"]),
            (r["x_right_foot_index"], r["y_right_foot_index"]),
            (r["x_ankle_right"]+0.01, r["y_ankle_right"])
        ), axis=1)
    return 0.0

def engineer_features_2d(df):
    transform_skeleton_2d(df)

    df["angle_knee_left"] = angle_knee_left(df)
    df["angle_knee_right"] = angle_knee_right(df)
    df["angle_elbow_left"] = angle_elbow_left(df)
    df["angle_elbow_right"] = angle_elbow_right(df)
    df["angle_ankle_left"] = angle_ankle_left(df)
    df["angle_ankle_right"] = angle_ankle_right(df)
    df["angle_foot_left"] = angle_foot_left(df)
    df["angle_foot_right"] = angle_foot_right(df)

    return df
