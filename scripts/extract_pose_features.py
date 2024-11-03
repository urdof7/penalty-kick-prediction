import os
import cv2
import mediapipe as mp
import sqlite3
import logging
from pose_data_setup import insert_pose_feature, get_pose_data_connection, initialize_pose_data

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def extract_pose_features_from_frame(frame_path, frame_id, conn):
    """
    Extracts pose features from a given frame using Mediapipe and inserts them into the database.
    :param frame_path: Path to the frame image
    :param frame_id: ID of the frame
    :param conn: Database connection to reuse
    """
    # List of relevant landmarks for kicking (lower body and torso)
    relevant_landmarks = [
        mp_pose.PoseLandmark.LEFT_HIP,
        mp_pose.PoseLandmark.RIGHT_HIP,
        mp_pose.PoseLandmark.LEFT_KNEE,
        mp_pose.PoseLandmark.RIGHT_KNEE,
        mp_pose.PoseLandmark.LEFT_ANKLE,
        mp_pose.PoseLandmark.RIGHT_ANKLE,
        mp_pose.PoseLandmark.LEFT_FOOT_INDEX,
        mp_pose.PoseLandmark.RIGHT_FOOT_INDEX,
        mp_pose.PoseLandmark.LEFT_SHOULDER,
        mp_pose.PoseLandmark.RIGHT_SHOULDER,
        mp_pose.PoseLandmark.LEFT_ELBOW,
        mp_pose.PoseLandmark.RIGHT_ELBOW,
        mp_pose.PoseLandmark.LEFT_WRIST,
        mp_pose.PoseLandmark.RIGHT_WRIST
    ]

    # Read the frame image
    image = cv2.imread(frame_path)
    if image is None:
        logging.error(f"Error reading frame: {frame_path}. The frame does not exist or cannot be accessed.")
        return

    # Convert BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe Pose
    results = pose.process(image_rgb)

    # Check if pose landmarks were detected
    if results.pose_landmarks:
        # Draw landmarks on the image
        annotated_image = image.copy()
        mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Save the annotated image
        annotated_image_path = frame_path.replace('.png', '_annotated.png')
        cv2.imwrite(annotated_image_path, annotated_image)

        # Iterate over the detected landmarks and insert pose features into the database
        for landmark_enum in relevant_landmarks:
            idx = landmark_enum.value
            landmark = results.pose_landmarks.landmark[idx]
            landmark_name = landmark_enum.name
            logging.debug(f"Inserting landmark {landmark_name} with frame_id={frame_id}")
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
                logging.error(f"Error inserting pose feature for landmark {landmark_name}: {e}")
        logging.info(f"Pose features extracted and saved for frame: {frame_path}")
    else:
        logging.warning(f"No pose landmarks detected for frame: {frame_path}. Analysis cannot proceed without landmarks.")

def extract_frames_from_kick_data():
    """
    Extracts frames from the kick_data database and processes them using Mediapipe.
    Only frames that exist in the kick_data database are processed to ensure consistency.
    """
    # Initialize pose_data database to clear previous data
    initialize_pose_data()

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
            pose_conn = get_pose_data_connection()
            extract_pose_features_from_frame(full_frame_path, frame_id, pose_conn)
            pose_conn.close()
        else:
            logging.warning(f"Frame path does not exist: {full_frame_path}")

    # Close connections
    kick_conn.close()

# Example usage
if __name__ == "__main__":
    # Extract pose features for frames listed in the kick_data database
    extract_frames_from_kick_data()

# Release resources
pose.close()
