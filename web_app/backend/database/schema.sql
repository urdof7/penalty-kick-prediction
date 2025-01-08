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

CREATE TABLE IF NOT EXISTS engineered_features (
    efeature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    frame_id INTEGER,
    x_mid_hip REAL,
    y_mid_hip REAL,
    z_mid_hip REAL,
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
