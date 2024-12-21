"""
Description: This program gets the data from kick_data via kick_data.py, and inserts them into the kick_data.db.
It streams videos from the Hugging Face Hub (urdof7/penalty-kick-data/videos) and uploads frames to 
urdof7/penalty-kick-data/frames, minimizing local storage and only committing changes if files differ.
"""

import os
import sys
import sqlite3
import subprocess
import json
import tempfile
import shutil
from huggingface_hub import HfApi, hf_hub_url, Repository

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

from kick_data import kick_data  # Import the kick data

# Database path stays local
DB_PATH = os.path.join(PROJECT_ROOT, "data/kick_data.db")

# Hugging Face repository info
VIDEO_REPO_ID = "urdof7/penalty-kick-data"
FRAMES_REPO_ID = "urdof7/penalty-kick-data"  # same repo for frames
VIDEOS_FOLDER = "videos"            # folder in Hugging Face repo where videos are stored
FRAMES_FOLDER = "frames"            # folder in Hugging Face repo where frames should be uploaded

api = HfApi()

# Set up the SQLite database
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS kicks")
cursor.execute("DROP TABLE IF EXISTS videos")
cursor.execute("DROP TABLE IF EXISTS frames")

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

def get_frame_rate(video_url):
    command = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=r_frame_rate", "-of", "json", video_url
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe error: {result.stderr.decode('utf-8')}")
    info = json.loads(result.stdout)
    if 'streams' not in info or len(info['streams']) == 0:
        stderr_msg = result.stderr.decode('utf-8')
        raise KeyError(f"'streams' not found in ffprobe output. Ensure the video URL is public and valid.\nffprobe stderr: {stderr_msg}")
    frame_rate_str = info['streams'][0]['r_frame_rate']
    num, denom = map(int, frame_rate_str.split('/'))
    return num / denom

def extract_frames(video_name, timestamp, direction, player_name, player_team, goal_scored, num_frames):
    # Check if the video already exists in the videos table
    cursor.execute("SELECT video_id FROM videos WHERE original_name = ?", (video_name,))
    row = cursor.fetchone()
    
    if row is None:
        # Insert the video into the videos table if it doesn't exist
        cursor.execute("INSERT INTO videos (original_name) VALUES (?)", (video_name,))
        conn.commit()
        cursor.execute("SELECT video_id FROM videos WHERE original_name = ?", (video_name,))
        video_id = cursor.fetchone()[0]
    else:
        video_id = row[0]

    # Convert timestamp to seconds
    minutes, seconds = timestamp.split(':')
    t = int(minutes) * 60 + float(seconds)

    # Get the video URL from Hugging Face
    video_url = hf_hub_url(
        repo_id=VIDEO_REPO_ID, 
        filename=f"{VIDEOS_FOLDER}/{video_name}", 
        repo_type="dataset", 
        revision="main"
    )

    # Get the frame rate of the video from the remote URL
    frame_rate = get_frame_rate(video_url)

    duration_before = num_frames / frame_rate
    duration_after = num_frames / frame_rate
    start_time = max(t - duration_before, 0)
    total_duration = duration_before + (1 / frame_rate) + duration_after

    # Determine kick_number
    cursor.execute("SELECT COUNT(*) + 1 FROM kicks WHERE video_id = ?", (video_id,))
    kick_number = cursor.fetchone()[0]

    # Insert or ignore this kick entry
    cursor.execute("""
        INSERT OR IGNORE INTO kicks (video_id, timestamp, kick_direction, player_name, player_team, goal_scored)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (video_id, timestamp, direction, player_name, player_team, goal_scored))
    conn.commit()
    cursor.execute("SELECT kick_id FROM kicks WHERE video_id = ? AND timestamp = ?", (video_id, timestamp))
    kick_id = cursor.fetchone()[0]

    # Use a temporary directory for frame extraction
    temp_dir = tempfile.mkdtemp(prefix="frame_extraction_")
    output_pattern = os.path.join(temp_dir, f"VID_{video_id}_KICK_{kick_number}_FRAME_%03d.png")

    # Extract frames from the remote video using ffmpeg (streaming)
    command = [
        "ffmpeg", "-ss", str(start_time), "-i", video_url,
        "-t", str(total_duration), "-vf", f"fps={frame_rate}", "-start_number", "1", output_pattern
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Clone the dataset repo locally, copy all frames, then commit if there are changes
    repo_local_dir = tempfile.mkdtemp(prefix="hf_repo_")
    repo = Repository(
        local_dir=repo_local_dir,
        clone_from=FRAMES_REPO_ID,
        repo_type="dataset",
        use_auth_token=False  # Public dataset
    )

    # Ensure the frames directory exists in the repo
    frames_dir_in_repo = os.path.join(repo_local_dir, FRAMES_FOLDER)
    os.makedirs(frames_dir_in_repo, exist_ok=True)

    # Prepare data for DB insertion and copy frames into the repo
    frames_data = []
    total_extracted = 2 * num_frames + 1
    for i in range(1, total_extracted + 1):
        frame_filename = f"VID_{video_id}_KICK_{kick_number}_FRAME_{i:03d}.png"
        local_frame_path = os.path.join(temp_dir, frame_filename)
        repo_frame_path = os.path.join(frames_dir_in_repo, frame_filename)
        # Copy (overwrite if exists) the frame into the repo
        shutil.copyfile(local_frame_path, repo_frame_path)
        frames_data.append((kick_id, video_id, i, f"{FRAMES_FOLDER}/{frame_filename}"))

    # Insert frames_data into DB
    cursor.executemany("""
        INSERT OR IGNORE INTO frames (kick_id, video_id, frame_no, frame_path)
        VALUES (?, ?, ?, ?)
    """, frames_data)
    conn.commit()

    # Add all changes
    repo.git_add(".")

    # Check if there are any changes to commit by running `git status --porcelain`
    status_result = subprocess.run(["git", "status", "--porcelain"], cwd=repo_local_dir, capture_output=True, text=True)
    if status_result.stdout.strip():
        # There are changes, so we commit and push
        repo.git_commit(f"Add frames for video_id={video_id}, kick_id={kick_id}")
        repo.git_push()
    else:
        print("No changes to commit - files are identical to what is already in the repository.")

    # Cleanup local temp directories
    shutil.rmtree(temp_dir)
    shutil.rmtree(repo_local_dir)

num_frames = 10
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
