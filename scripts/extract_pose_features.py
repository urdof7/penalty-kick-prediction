import os
import cv2
import mediapipe as mp
import sqlite3
from pose_data_setup import insert_pose_feature

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Define the path to frames and database
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FRAMES_PATH = os.path.join(PROJECT_ROOT, 'data', 'frames')
KICK_DB_PATH = os.path.join(PROJECT_ROOT, 'data', 'kick_data.db')

# Ensure the frames directory exists
os.makedirs(FRAMES_PATH, exist_ok=True)

def get_kick_data_connection():
    """
    Connects to the kick_data.db database and returns the connection.
    """
    return sqlite3.connect(KICK_DB_PATH)

def extract_pose_features_from_frame(frame_path, frame_id):
    """
    Extracts pose features from a given frame using Mediapipe and inserts them into the database.
    :param frame_path: Path to the frame image
    :param frame_id: ID of the frame
    """
    # Read the frame image
    image = cv2.imread(frame_path)
    if image is None:
        raise ValueError(f"Error reading frame: {frame_path}. The frame does not exist or cannot be accessed.")

    # Convert BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe Pose
    results = pose.process(image_rgb)

    # Check if pose landmarks were detected
    if results.pose_landmarks:
        # Iterate over the detected landmarks and insert pose features into the database
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            landmark_name = mp_pose.PoseLandmark(idx).name
            print(f"Inserting landmark {landmark_name} with frame_id={frame_id}")
            try:
                insert_pose_feature(
                    frame_id=frame_id,
                    landmark_name=landmark_name,
                    x=landmark.x,
                    y=landmark.y,
                    z=landmark.z,
                    visibility=landmark.visibility
                )
            except sqlite3.Error as e:
                print(f"Error inserting pose feature for landmark {landmark_name}: {e}")

        # Optional: Draw the landmarks on the frame and save for reference
        annotated_image = image.copy()
        mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        annotated_frame_path = frame_path.replace('.png', '_annotated.png')
        cv2.imwrite(annotated_frame_path, annotated_image)
        print(f"Pose features extracted and saved for frame: {frame_path}")
    else:
        raise ValueError(f"No pose landmarks detected for frame: {frame_path}. Analysis cannot proceed without landmarks.")

def extract_frames_from_kick_data():
    """
    Extracts frames from the kick_data database and processes them using Mediapipe.
    Only frames that exist in the kick_data database are processed to ensure consistency.
    """
    # Open kick_data database connection
    kick_conn = get_kick_data_connection()
    kick_cursor = kick_conn.cursor()

    # Query all frames from kick_data.db
    kick_cursor.execute("SELECT frame_id, frame_no, frame_path FROM frames")
    frames = kick_cursor.fetchall()

    for frame in frames:
        frame_id, frame_no, frame_path = frame
        # Construct the full path relative to the project root
        full_frame_path = os.path.join(PROJECT_ROOT, frame_path)
        if os.path.exists(full_frame_path):
            try:
                extract_pose_features_from_frame(full_frame_path, frame_id)
            except ValueError as e:
                print(e)
        else:
            print(f"Frame path does not exist: {full_frame_path}")

    kick_conn.close()

# Example usage
if __name__ == "__main__":
    # Extract pose features for frames listed in the kick_data database
    extract_frames_from_kick_data()

# Release resources
pose.close()
