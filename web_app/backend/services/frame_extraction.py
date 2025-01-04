import os
import subprocess
import tempfile
import json

def get_frame_rate(video_path):
    """
    Uses ffprobe to determine the video's frame rate (FPS).
    Returns a float representing frames per second.
    """
    command = [
        "ffprobe", "-hide_banner", "-loglevel", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate",
        "-of", "json",
        video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe error: {result.stderr.decode('utf-8')}")

    info = json.loads(result.stdout)
    if 'streams' not in info or len(info['streams']) == 0:
        stderr_msg = result.stderr.decode('utf-8')
        raise KeyError(f"'streams' not found in ffprobe output. Stderr: {stderr_msg}")

    frame_rate_str = info['streams'][0]['r_frame_rate']
    num, denom = map(int, frame_rate_str.split('/'))
    return num / denom

def extract_frames_around_time(
    video_path,
    midswing_time,
    frames_before=10,
    frames_after=10,
    fps=None,
    exact_frames=True
):
    """
    Extract frames around 'midswing_time', returning (temp_dir, frames_list).
    
    This function automatically detects the video's actual FPS via ffprobe
    unless you provide a specific 'fps' value.

    By default (exact_frames=True), we extract exactly (frames_before + frames_after + 1)
    frames using -frames:v. This is more precise if the chosen FPS matches
    the real video framerate.

    If exact_frames=False, we revert to time-based logic:
      - Use '-t duration' and '-vf fps=<fps>' to sample frames over a small time window.

    Args:
        video_path (str): Path to the local video file.
        midswing_time (float): The main time of interest in seconds.
        frames_before (int): Number of frames before 'midswing_time' to extract.
        frames_after (int): Number of frames after 'midswing_time' to extract.
        fps (float|None): If None, we detect the true FPS from the video via ffprobe.
                          If a float, we use that instead.
        exact_frames (bool): Whether to extract an exact count of frames (True) or
                             use time-based sampling (False).

    Returns:
        tuple:
          temp_dir (str): Path to the temporary directory holding extracted frames.
          frames_list (List[str]): List of file paths for each extracted frame.
    """
    # Detect the real FPS if not provided
    if fps is None:
        fps = get_frame_rate(video_path)

    # Create a temporary directory for extracted frames
    temp_dir = tempfile.mkdtemp(prefix="kick_extract_")

    # Total number of frames to extract
    total_frames = frames_before + frames_after + 1

    if exact_frames:
        # We skip back a certain # of frames, measured by frames_before / fps in seconds
        start_time = max(midswing_time - (frames_before / fps), 0)

        out_pattern = os.path.join(temp_dir, "frame_%03d.png")

        # -frames:v to exactly get 'total_frames'
        ffmpeg_cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-ss", str(start_time),
            "-i", video_path,
            "-frames:v", str(total_frames),
            "-an",            # no audio
            "-c:v", "png",    # store as PNG
            out_pattern
        ]
        subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    else:
        # Time-based approach: sample frames over a small duration
        duration = total_frames / fps
        start_time = max(midswing_time - (frames_before / fps), 0)

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

    # Gather the extracted frames in a list
    frames_list = []
    for i in range(1, total_frames + 1):
        fpath = os.path.join(temp_dir, f"frame_{i:03d}.png")
        if os.path.exists(fpath):
            frames_list.append(fpath)

    return temp_dir, frames_list
