import os
import sys
import sqlite3
import subprocess
import logging
import json
import tempfile
import shutil
from collections import defaultdict
from huggingface_hub import HfApi, hf_hub_url, CommitOperationAdd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # development_and_training base directory
sys.path.append(BASE_DIR)

from kick_data import kick_data  # Your kick_data

DB_PATH = os.path.join(BASE_DIR, "data/kick_data.db")

VIDEO_REPO_ID = "urdof7/penalty-kick-data"
VIDEOS_FOLDER = "videos"
FRAMES_FOLDER = "frames"

api = HfApi()

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS kicks")
cursor.execute("DROP TABLE IF EXISTS videos")
cursor.execute("DROP TABLE IF EXISTS frames")

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

cursor.execute("CREATE INDEX IF NOT EXISTS idx_original_name ON videos(original_name)")
conn.commit()

def get_frame_rate(video_url):
    command = [
        "ffprobe", "-hide_banner", "-loglevel", "error",
        "-select_streams", "v:0", "-show_entries",
        "stream=r_frame_rate", "-of", "json", video_url
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe error: {result.stderr.decode('utf-8')}")
    info = json.loads(result.stdout)
    if 'streams' not in info or len(info['streams']) == 0:
        stderr_msg = result.stderr.decode('utf-8')
        raise KeyError(f"'streams' not found in ffprobe output.\nffprobe stderr: {stderr_msg}")
    frame_rate_str = info['streams'][0]['r_frame_rate']
    num, denom = map(int, frame_rate_str.split('/'))
    return num / denom

def extract_frames(video_name, timestamp, direction, player_name, player_team, goal_scored, num_frames):
    # Insert or find video
    cursor.execute("SELECT video_id FROM videos WHERE original_name = ?", (video_name,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute("INSERT INTO videos (original_name) VALUES (?)", (video_name,))
        conn.commit()
        cursor.execute("SELECT video_id FROM videos WHERE original_name = ?", (video_name,))
        video_id = cursor.fetchone()[0]
    else:
        video_id = row[0]

    # Convert timestamp to seconds
    minutes, seconds = timestamp.split(':')
    t = int(minutes)*60 + float(seconds)

    video_url = hf_hub_url(
        repo_id=VIDEO_REPO_ID,
        filename=f"{VIDEOS_FOLDER}/{video_name}",
        repo_type="dataset",
        revision="main"
    )
    frame_rate = get_frame_rate(video_url)

    duration_before = num_frames / frame_rate
    duration_after = num_frames / frame_rate
    start_time = max(t - duration_before, 0)
    total_duration = duration_before + (1/frame_rate) + duration_after

    # Determine kick_number
    cursor.execute("SELECT COUNT(*)+1 FROM kicks WHERE video_id = ?", (video_id,))
    kick_number = cursor.fetchone()[0]

    cursor.execute("""
        INSERT OR IGNORE INTO kicks (video_id, timestamp, kick_direction, player_name, player_team, goal_scored)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (video_id, timestamp, direction, player_name, player_team, goal_scored))
    conn.commit()

    cursor.execute("SELECT kick_id FROM kicks WHERE video_id=? AND timestamp=?", (video_id, timestamp))
    kick_id = cursor.fetchone()[0]

    temp_dir = tempfile.mkdtemp(prefix="frame_extraction_")
    output_pattern = os.path.join(temp_dir, f"VID_{video_id}_KICK_{kick_number}_FRAME_%03d.png")

    ffmpeg_cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-ss", str(start_time),
        "-i", video_url,
        "-t", str(total_duration),
        "-vf", f"fps={frame_rate}",
        "-start_number", "1",
        output_pattern
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    frames_data = []
    total_extracted = 2*num_frames + 1
    for i in range(1, total_extracted+1):
        frame_filename = f"VID_{video_id}_KICK_{kick_number}_FRAME_{i:03d}.png"
        local_frame_path = os.path.join(temp_dir, frame_filename)
        cursor.execute("""
            INSERT OR IGNORE INTO frames (kick_id, video_id, frame_no, frame_path)
            VALUES (?, ?, ?, ?)
        """, (kick_id, video_id, i, f"{FRAMES_FOLDER}/{frame_filename}"))
        frames_data.append((frame_filename, local_frame_path))

    conn.commit()
    return frames_data, temp_dir, video_id

def main():
    num_frames = 10
    kicks_by_video = defaultdict(list)
    for kick in kick_data:
        kicks_by_video[kick["video_name"]].append(kick)

    for vid_idx, (video_name, kicks) in enumerate(kicks_by_video.items(), start=1):
        print(f"Processing video {vid_idx}/{len(kicks_by_video)}: {video_name}")
        operations = {}
        total_added = 0
        temp_dirs = []

        for idx, kick in enumerate(kicks, start=1):
            print(f"  Processing kick {idx}/{len(kicks)} at {kick['timestamp']}")
            frames_data, temp_dir, video_id = extract_frames(
                video_name=kick["video_name"],
                timestamp=kick["timestamp"],
                direction=kick["direction"],
                player_name=kick["player_name"],
                player_team=kick["player_team"],
                goal_scored=kick["goal_scored"],
                num_frames=num_frames
            )
            temp_dirs.append(temp_dir)

            # Add frames as operations (no duplicates expected)
            for (frame_filename, local_frame_path) in frames_data:
                path_in_repo = f"{FRAMES_FOLDER}/{frame_filename}"
                operations[path_in_repo] = CommitOperationAdd(
                    path_in_repo=path_in_repo,
                    path_or_fileobj=local_frame_path
                )
                total_added += 1

        if operations:
            print(f"Uploading {total_added} new frames for video: {video_name}...")
            try:
                commit_info = api.create_commit(
                    repo_id=VIDEO_REPO_ID,
                    repo_type="dataset",
                    operations=list(operations.values()),
                    commit_message=f"Upload/Update frames for video {video_name}"
                )

                if not commit_info or not hasattr(commit_info, 'commit_id') or commit_info.commit_id is None:
                    # No changes
                    print(f"No new frames were actually uploaded for video {video_name} (no changes detected).")
                else:
                    print(f"Upload complete for video {video_name}. {total_added} frames added/updated.")
            except Exception as e:
                err_msg = str(e)
                if "No files have been modified since last commit" in err_msg:
                    print(f"No new frames were actually uploaded for video {video_name} (all already existed).")
                else:
                    print(f"Failed to upload frames for video {video_name} due to error: {e}")
        else:
            print(f"No frames extracted for video {video_name}, no commit made.")

        # Remove temp dirs
        for d in temp_dirs:
            shutil.rmtree(d)

    conn.close()

if __name__ == "__main__":
    main()
