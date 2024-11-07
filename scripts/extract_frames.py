import os
import sys
import sqlite3
import subprocess
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

from kick_data import kick_data  # Import the kick data

# Define paths relative to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VIDEO_DIR = os.path.join(PROJECT_ROOT, "data/raw_videos")
FRAME_DIR = os.path.join(PROJECT_ROOT, "data/frames")
DB_PATH = os.path.join(PROJECT_ROOT, "data/kick_data.db")

# Create output directory if it doesn't exist
os.makedirs(FRAME_DIR, exist_ok=True)

# Set up the SQLite database
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""DROP TABLE IF EXISTS kicks""")
cursor.execute("""DROP TABLE IF EXISTS videos""")
cursor.execute("""DROP TABLE IF EXISTS frames""")

# Create the videos and kicks tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
    video_id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_name TEXT UNIQUE
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS kicks (
        kick_id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id INTEGER,
        timestamp TEXT,
        kick_direction INTEGER,
        player_name TEXT,
        player_team TEXT,
        goal_scored BOOLEAN,
        FOREIGN KEY (video_id) REFERENCES videos(video_id),
        UNIQUE (video_id, timestamp)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS frames (
    frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
    kick_id INTEGER,
    video_id INTEGER,
    frame_no INTEGER,
    frame_path TEXT,
    FOREIGN KEY (kick_id) REFERENCES kicks(kick_id),
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    UNIQUE (kick_id, frame_no)
    )
""")


# Create an index on original_name to speed up lookups
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_original_name ON videos(original_name)
""")
conn.commit()

# Function to get frame rate of a video
def get_frame_rate(video_path):
    command = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=r_frame_rate", "-of", "json", video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info = json.loads(result.stdout)
    frame_rate_str = info['streams'][0]['r_frame_rate']
    num, denom = map(int, frame_rate_str.split('/'))
    return num / denom

# Function to extract frames around a given timestamp
def extract_frames(video_name, timestamp, direction, player_name, player_team, goal_scored, num_frames):
    # Check if the video already exists in the videos table
    cursor.execute("""
        SELECT video_id FROM videos WHERE original_name = ?
    """, (video_name,))
    row = cursor.fetchone()
    
    if row is None:
        # Insert the video into the videos table if it doesn't exist
        cursor.execute("""
            INSERT INTO videos (original_name)
            VALUES (?)
        """, (video_name,))
        conn.commit()
        # Re-fetch the video_id after insertion
        cursor.execute("""
            SELECT video_id FROM videos WHERE original_name = ?
        """, (video_name,))
        video_id = cursor.fetchone()[0]
    else:
        video_id = row[0]

    # Calculate seconds before and after the given timestamp
    t = int(timestamp.split(':')[0]) * 60 + float(timestamp.split(':')[1])
    
    # Get the frame rate of the video
    video_path = os.path.join(VIDEO_DIR, video_name)
    frame_rate = get_frame_rate(video_path)

    # Calculate the start time and total duration for frame extraction
    duration_before = num_frames / frame_rate
    duration_after = num_frames / frame_rate
    start_time = max(t - duration_before, 0)
    total_duration = duration_before + (1 / frame_rate) + duration_after

    # Get the current kick number for the video
    cursor.execute("""
        SELECT COUNT(*) + 1 FROM kicks WHERE video_id = ?
    """, (video_id,))
    kick_number = cursor.fetchone()[0]

    # Insert the kick into the kicks table and get the kick_id
    cursor.execute("""
        INSERT OR IGNORE INTO kicks (video_id, timestamp, kick_direction, player_name, player_team, goal_scored)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (video_id, timestamp, direction, player_name, player_team, goal_scored))
    conn.commit()
    cursor.execute("""
        SELECT kick_id FROM kicks WHERE video_id = ? AND timestamp = ?
    """, (video_id, timestamp))
    kick_id = cursor.fetchone()[0]

    # Batch extract frames using ffmpeg
    output_pattern = f"{FRAME_DIR}/VID_{video_id}_KICK_{kick_number}_FRAME_%03d.png"
    command = [
        "ffmpeg", "-ss", str(start_time), "-i", video_path,
        "-t", str(total_duration), "-vf", f"fps={frame_rate}", "-start_number", "1", output_pattern
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Prepare frame data for database insertion
    frames_data = []
    for i in range(1, 2 * num_frames + 1 + 1):
        output_file = f"data/frames/VID_{video_id}_KICK_{kick_number}_FRAME_{i:03d}.png"
        frames_data.append((kick_id, video_id, i, os.path.relpath(output_file, PROJECT_ROOT)))

    # Insert all frame data into the frames table in one go
    cursor.executemany("""
        INSERT OR IGNORE INTO frames (kick_id, video_id, frame_no, frame_path)
        VALUES (?, ?, ?, ?)
    """, frames_data)
    conn.commit()

# Loop through kick data and call extract_frames
num_frames = 10  # Set the default number of frames to extract before and after the timestamp
for kick in kick_data:
    extract_frames(
        video_name=kick["video_name"],
        timestamp=kick["timestamp"],
        direction=kick["direction"],
        player_name=kick["player_name"],
        player_team=kick["player_team"],
        goal_scored=kick["goal_scored"],
        num_frames=num_frames
    )

conn.close()
