-- web_app/backend/database/schema.sql

CREATE TABLE IF NOT EXISTS videos (
    video_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,             -- to scope to each user's session
    original_name TEXT
);

CREATE TABLE IF NOT EXISTS kicks (
    kick_id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id INTEGER,
    timestamp REAL,
    FOREIGN KEY (video_id) REFERENCES videos(video_id)
);

CREATE TABLE IF NOT EXISTS frames (
    frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
    kick_id INTEGER,
    video_id INTEGER,
    frame_no INTEGER,
    frame_path TEXT,
    FOREIGN KEY (kick_id) REFERENCES kicks(kick_id),
    FOREIGN KEY (video_id) REFERENCES videos(video_id)
);

CREATE TABLE IF NOT EXISTS pose_features (
    feature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    frame_id INTEGER,
    landmark_name TEXT,
    x REAL,
    y REAL,
    z REAL,
    visibility REAL,
    FOREIGN KEY (frame_id) REFERENCES frames(frame_id)
);

CREATE TABLE IF NOT EXISTS engineered_features (
    efeature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    frame_id INTEGER,

    -- 2D coords for the main joints of interest (already normalized)
    x_hip_left REAL,      y_hip_left REAL,
    x_hip_right REAL,     y_hip_right REAL,
    x_knee_left REAL,     y_knee_left REAL,
    x_knee_right REAL,    y_knee_right REAL,
    x_ankle_left REAL,    y_ankle_left REAL,
    x_ankle_right REAL,   y_ankle_right REAL,
    x_left_foot_index REAL,   y_left_foot_index REAL,
    x_right_foot_index REAL,  y_right_foot_index REAL,
    x_shoulder_left REAL, y_shoulder_left REAL,
    x_shoulder_right REAL,y_shoulder_right REAL,
    x_elbow_left REAL,    y_elbow_left REAL,
    x_elbow_right REAL,   y_elbow_right REAL,
    x_wrist_left REAL,    y_wrist_left REAL,
    x_wrist_right REAL,   y_wrist_right REAL,

    -- Angles
    angle_knee_left REAL,
    angle_knee_right REAL,
    angle_elbow_left REAL,
    angle_elbow_right REAL,
    angle_ankle_left REAL,
    angle_ankle_right REAL,
    angle_foot_left REAL,
    angle_foot_right REAL,

    FOREIGN KEY (frame_id) REFERENCES frames(frame_id)
);