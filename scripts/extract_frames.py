import os
import sqlite3
import subprocess

# Define paths relative to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VIDEO_DIR = os.path.join(PROJECT_ROOT, "data/videos")
FRAME_DIR = os.path.join(PROJECT_ROOT, "data/frames")
DB_PATH = os.path.join(PROJECT_ROOT, "data/kick_data.db")

# Create output directory if it doesn't exist
os.makedirs(FRAME_DIR, exist_ok=True)

# Set up the SQLite database
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the kicks table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS kicks (
        kick_id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_name TEXT,
        timestamp TEXT,
        frame_no INTEGER,
        kick_direction INTEGER,
        player_name TEXT,
        player_team TEXT,
        frame_path TEXT,
        goal_scored BOOLEAN,
        UNIQUE(video_name, timestamp, frame_no)
    )
""")
conn.commit()

# Function to extract frames around a given timestamp
def extract_frames(video_name, timestamp, direction, player_name, player_team, goal_scored, num_frames=5):
    # Calculate seconds before and after the given timestamp
    t = int(timestamp.split(':')[0]) * 60 + float(timestamp.split(':')[1])

    for i in range(-num_frames, num_frames + 1):
        frame_time = max(t + (i / 30), 0)  # Minimal frame increment assuming 30 FPS
        output_file = f"{FRAME_DIR}/{video_name}_frame_{i + num_frames}.png"

        # Extract the specific frame using FFmpeg
        command = [
            "ffmpeg", "-i", f"{VIDEO_DIR}/{video_name}",
            "-vf", f"select='eq(n,{int(frame_time * 30)})'",  # Assuming 30 FPS
            "-vsync", "vfr", output_file
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Save the metadata in the database if it doesn't already exist
        cursor.execute("""
            INSERT OR IGNORE INTO kicks (video_name, timestamp, frame_no, kick_direction, 
                                        player_name, player_team, frame_path, goal_scored)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (video_name, timestamp, i + num_frames, direction, player_name, player_team, output_file, goal_scored))
        conn.commit()

# Directions:
# 1 - Top left
# 2 - Middle top
# 3 - Top right
# 4 - Bottom left
# 5 - Middle bottom
# 6 - Bottom right

extract_frames(
    video_name="Argentina v France： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup Final [MCWJNOfJoSM].mp4",
    timestamp="00:28",  # Time of the kick in the video
    direction=1,  # Top left corner
    player_name="Kylian Mbappé",
    player_team="France",
    goal_scored=True,  # Indicate if the goal was scored
    num_frames=5       # Number of frames before and after
)

conn.close()
