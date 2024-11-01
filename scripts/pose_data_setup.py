import os
import sqlite3

# Define the project root and database path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
POSE_DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'pose_data.db')

# Ensure the data directory exists
os.makedirs(os.path.dirname(POSE_DB_PATH), exist_ok=True)

# Database connection function
def get_pose_data_connection():
    """Connects to the pose_data.db database and returns the connection."""
    return sqlite3.connect(POSE_DB_PATH)

# Initialize tables in pose_data.db
def initialize_pose_data():
    """Deletes pose_data.db if it exists and recreates it with the frames and pose_features tables."""
    # Remove the existing database file if it exists
    if os.path.exists(POSE_DB_PATH):
        os.remove(POSE_DB_PATH)

    # Connect and create a new database with the latest schema
    conn = get_pose_data_connection()
    cursor = conn.cursor()

    # Create the frames table
    cursor.execute('''
        CREATE TABLE frames (
            frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
            kick_id INTEGER,
            video_id INTEGER,
            frame_no INTEGER,
            frame_path TEXT,
            FOREIGN KEY (kick_id) REFERENCES kicks(kick_id),
            FOREIGN KEY (video_id) REFERENCES videos(video_id),
            UNIQUE (kick_id, frame_no)
        )
    ''')

    # Create the pose_features table
    cursor.execute('''
        CREATE TABLE pose_features (
            feature_id INTEGER PRIMARY KEY AUTOINCREMENT,
            frame_id INTEGER,
            kick_id INTEGER,
            landmark_name TEXT,
            x REAL,
            y REAL,
            z REAL,
            visibility REAL,
            FOREIGN KEY (frame_id) REFERENCES frames(frame_id),
            FOREIGN KEY (kick_id) REFERENCES kicks(kick_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("pose_data.db deleted, recreated, and initialized with tables.")


# Insert a frame record in pose_data.db
def insert_frame(kick_id, video_id, frame_no, frame_path):
    """Inserts a frame into the frames table, linked to a specific kick and video."""
    conn = get_pose_data_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO frames (kick_id, video_id, frame_no, frame_path)
        VALUES (?, ?, ?, ?)
    ''', (kick_id, video_id, frame_no, frame_path))
    
    conn.commit()
    frame_id = cursor.lastrowid
    conn.close()
    return frame_id  # Returning frame_id for linking with pose features

# Insert pose feature data for a frame
def insert_pose_feature(frame_id, kick_id, landmark_name, x, y, z, visibility):
    """Inserts pose feature data into the pose_features table, linked to frame_id and kick_id."""
    conn = get_pose_data_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO pose_features (frame_id, kick_id, landmark_name, x, y, z, visibility)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (frame_id, kick_id, landmark_name, x, y, z, visibility))
    
    conn.commit()
    conn.close()

# Example usage
if __name__ == "__main__":
    # Initialize the database structure
    initialize_pose_data()
