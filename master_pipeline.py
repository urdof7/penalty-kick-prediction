import os
import subprocess
import sys

# Paths to the scripts
default_scripts = [
    "kick_data.py",
    "scripts/extract_frames.py",
    "scripts/extract_pose_features.py",
    "scripts/pose_data_setup.py",
]

optional_scripts = [
    "scripts/data_preprocessing/feature_engineering_single_frame.py",
    "scripts/data_preprocessing/feature_engineering_sequence.py",
]

def run_script(script_path):
    """Run a single script using subprocess."""
    try:
        print(f"Running: {script_path}")
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"Output:\n{result.stdout}")
        print(f"Errors:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}:\n{e.stderr}")
        print(f"Standard output before error:\n{e.stdout}")
        raise


def main():
    """Run the pipeline scripts."""
    print("")
    # Check for TRAIN_MODELS environment variable
    train_models = os.environ.get("TRAIN_MODELS") == "1"

    # Run default scripts
    print("Running default scripts...")
    for script in default_scripts:
        run_script(script)
    
    # Run optional scripts if TRAIN_MODELS is set to "1"
    if train_models:
        print("Running optional training scripts...")
        for script in optional_scripts:
            run_script(script)
    print("Pipeline execution completed!")

if __name__ == "__main__":
    main()
    