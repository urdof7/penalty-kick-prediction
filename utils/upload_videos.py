from huggingface_hub import Repository, HfApi, create_repo, upload_file
import os

# Define the Hugging Face repository and subdirectory
repo_name = "PK-Prediction/pk_data"
subfolder = "videos"  # Target subdirectory for videos

# Path to the video file or directory you want to upload
input_path = "/Users/braydenmiller/Downloads/brayden_kicks.mp4"  # Replace with your actual file or directory path

# Validate the input exists
if not os.path.exists(input_path):
    raise FileNotFoundError(f"Input path '{input_path}' not found")

# Collect video files
if os.path.isdir(input_path):
    video_files = [
        os.path.join(input_path, f)
        for f in os.listdir(input_path)
        if f.endswith((".mp4", ".mov"))
    ]
    if not video_files:
        raise ValueError(f"No video files found in directory '{input_path}'.")
else:
    video_files = [input_path]

# Ensure the repository exists
api = HfApi()
try:
    api.create_repo(repo_id=repo_name, repo_type="dataset", exist_ok=True)
except Exception as e:
    print(f"Error creating repo: {e}")

# Upload each video file to the 'videos/' subdirectory
for video_file in video_files:
    file_name = os.path.basename(video_file)
    target_path = f"{subfolder}/{file_name}"  # Upload to 'videos/' subdirectory
    try:
        upload_file(
            path_or_fileobj=video_file,
            path_in_repo=target_path,
            repo_id=repo_name,
            repo_type="dataset",
        )
        print(f"Uploaded {video_file} to {target_path} in {repo_name}.")
    except Exception as e:
        print(f"Failed to upload {video_file}: {e}")
