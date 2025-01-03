CREATE TABLE IF NOT EXISTS videos (
    video_id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_name TEXT
);

CREATE TABLE IF NOT EXISTS kicks (
    kick_id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id INTEGER,
    timestamp REAL,  -- or INTEGER
    kick_direction TEXT,
    player_name TEXT,
    player_team TEXT,
    goal_scored INTEGER,  -- or BOOLEAN
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
