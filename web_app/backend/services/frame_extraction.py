# web_app/backend/services/frame_extraction.py

import os
import subprocess
import tempfile

def extract_frames_around_time(video_path, midswing_time, frames_before=10, frames_after=10, fps=30):
    """
    Extract frames around midswing_time. Returns (temp_dir, frames_list).
    """
    total_frames = frames_before + frames_after + 1
    duration = total_frames / fps
    start_time = max(midswing_time - (frames_before/fps), 0)

    temp_dir = tempfile.mkdtemp(prefix="kick_extract_")
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
    for i in range(1, total_frames+1):
        fpath = os.path.join(temp_dir, f"frame_{i:03d}.png")
        if os.path.exists(fpath):
            frames_list.append(fpath)

    return temp_dir, frames_list
