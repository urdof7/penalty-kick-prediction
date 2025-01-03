# app.py

import os
import sqlite3
import tempfile
import subprocess
import uuid

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

###############################################################################
# 1) GLOBAL SETUP: in-memory SQLite + folder paths
###############################################################################

# We'll use a global connection to an in-memory SQLite DB (ephemeral)
conn = None

# Folders for uploaded videos and extracted frames
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
TEMP_FRAMES_FOLDER = os.path.join(os.path.dirname(__file__), 'temp_frames')

app = Flask(__name__)
CORS(app)

###############################################################################
# 2) DB INIT: create ephemeral tables (videos, frames).
###############################################################################

def init_db():
    global conn
    if conn is None:
        # Use an in-memory database:
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON;")
        
        cur = conn.cursor()
        # A simple 'videos' table storing the original filename, plus an ID
        cur.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                video_id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_name TEXT
            )
        """)
        # A simple 'frames' table referencing videos, storing file paths to extracted frames
        cur.execute("""
            CREATE TABLE IF NOT EXISTS frames (
                frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                frame_no INTEGER,
                frame_path TEXT,
                FOREIGN KEY (video_id) REFERENCES videos(video_id)
            )
        """)
        conn.commit()

# Call init_db() once at startup:
init_db()

###############################################################################
# 3) HELPER FUNCTIONS
###############################################################################

def extract_frames_around_time(video_path, midswing_time, frames_before=10, frames_after=10, fps=30):
    """
    Extract frames from local `video_path` around `midswing_time`.
    Returns (temp_dir, list_of_frame_paths).
    """
    total_frames = frames_before + frames_after + 1
    duration = total_frames / fps
    # Calculate start time (can't go below 0)
    start_time = max(midswing_time - (frames_before / fps), 0)

    # Create a temp directory to store the frames
    temp_dir = tempfile.mkdtemp(prefix="web_extract_")
    out_pattern = os.path.join(temp_dir, "frame_%03d.png")

    ffmpeg_cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-ss", str(start_time),
        "-i", video_path,
        "-t", str(duration),
        "-vf", f"fps={fps}",
        "-start_number", "1",
        out_pattern
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    frames_list = []
    for i in range(1, total_frames + 1):
        frame_file = os.path.join(temp_dir, f"frame_{i:03d}.png")
        if os.path.exists(frame_file):
            frames_list.append(frame_file)

    return temp_dir, frames_list

def insert_video_and_frames(original_name, frames_list):
    """
    Insert a row into 'videos', then insert each frame into 'frames' table.
    Return the video_id and a list of (frame_id, frame_path) tuples.
    """
    cur = conn.cursor()

    # Insert video record
    cur.execute("INSERT INTO videos (original_name) VALUES (?)", (original_name,))
    video_id = cur.lastrowid

    # Insert frames
    results = []
    for i, fpath in enumerate(frames_list, start=1):
        cur.execute("""
            INSERT INTO frames (video_id, frame_no, frame_path)
            VALUES (?, ?, ?)
        """, (video_id, i, fpath))
        frame_id = cur.lastrowid
        results.append((frame_id, fpath))

    conn.commit()
    return video_id, results

###############################################################################
# 4) ROUTES
###############################################################################

@app.route('/')
def index():
    return "Flask is running (ephemeral DB for frames)."

# A) Upload route
@app.route('/upload', methods=['POST'])
def upload_video():
    """
    Receives a video file and saves it to UPLOAD_FOLDER with a unique name
    to avoid collisions. Returns JSON with the final filename.
    """
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file found"}), 400

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Give the file a unique name to prevent collisions
    orig_filename = file.filename
    unique_name = str(uuid.uuid4()) + "_" + orig_filename
    save_path = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(save_path)

    return jsonify({"filename": unique_name}), 200

# B) Extract frames route
@app.route('/extract_frames', methods=['POST'])
def extract_frames():
    """
    JSON body: { "filename": "...", "midswing_time": <float> }
    - Locates the uploaded video in UPLOAD_FOLDER
    - Extracts frames around that time
    - Stores them in ephemeral DB
    - Copies them to TEMP_FRAMES_FOLDER so we can serve them
    - Returns a list of /temp_frames/<frame_filename> URLs to display
    """
    data = request.json
    filename = data.get('filename')
    midswing_time = float(data.get('midswing_time', 0))

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    # Check if file exists
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(video_path):
        return jsonify({"error": f"File {filename} not found"}), 404

    # Extract frames around midswing
    temp_dir, frames_list = extract_frames_around_time(video_path, midswing_time)

    # Insert into ephemeral DB
    video_id, frame_records = insert_video_and_frames(filename, frames_list)

    # Copy extracted frames into TEMP_FRAMES_FOLDER so we can serve them
    if not os.path.exists(TEMP_FRAMES_FOLDER):
        os.makedirs(TEMP_FRAMES_FOLDER)

    frame_urls = []
    for (frame_id, src_path) in frame_records:
        frame_name = os.path.basename(src_path)
        dest_path = os.path.join(TEMP_FRAMES_FOLDER, f"v{video_id}_f{frame_id}_{frame_name}")
        # rename frames to ensure uniqueness
        subprocess.run(["cp", src_path, dest_path])
        
        # The URL the frontend can use to display the frame
        url = f"/temp_frames/{os.path.basename(dest_path)}"
        frame_urls.append(url)

    return jsonify({
        "message": "Frames extracted successfully",
        "frame_urls": frame_urls
    }), 200

# C) Serve frames from TEMP_FRAMES_FOLDER
@app.route('/temp_frames/<path:filename>')
def serve_temp_frame(filename):
    return send_from_directory(TEMP_FRAMES_FOLDER, filename)

###############################################################################
# 5) MAIN ENTRY POINT
###############################################################################
if __name__ == '__main__':
    # Ensure DB is initialized
    init_db()
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(TEMP_FRAMES_FOLDER):
        os.makedirs(TEMP_FRAMES_FOLDER)

    app.run(debug=True, host='0.0.0.0', port=8098)
