# web_app/backend/model_loader.py

import os
import joblib
import numpy as np
from tensorflow.keras.models import load_model

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..')
# Paths to your saved model & scaler
SEQUENCE_LSTM_MODEL_PATH = os.path.join(
    BASE_DIR,
    'development_and_training',
    'models',
    'sequence_models',
    'sequence_model.h5'
)
SEQUENCE_LSTM_SCALER_PATH = os.path.join(
    BASE_DIR,
    'development_and_training',
    'models',
    'sequence_models',
    'sequence_scaler.pkl'
)
class SequenceLSTMModel:
    def __init__(self):
        # Load model + scaler
        if not os.path.exists(SEQUENCE_LSTM_MODEL_PATH):
            raise FileNotFoundError(f"Sequence model not found at {SEQUENCE_LSTM_MODEL_PATH}")
        if not os.path.exists(SEQUENCE_LSTM_SCALER_PATH):
            raise FileNotFoundError(f"Sequence scaler not found at {SEQUENCE_LSTM_SCALER_PATH}")

        self.model = load_model(SEQUENCE_LSTM_MODEL_PATH)
        self.scaler = joblib.load(SEQUENCE_LSTM_SCALER_PATH)

    def predict_quadrant_probs(self, arr_3d):
        """
        arr_3d shape: (1, time_steps=21, features=48)
        1) Flatten => shape (21,48)
        2) scaler.transform => shape (21,48)
        3) Reshape => (1,21,48)
        4) model.predict => shape (6,)
        """
        import numpy as np

        b, t, f = arr_3d.shape  # maybe (1,21,48)
        # Flatten
        arr_2d = arr_3d.reshape(b*t, f)  # (21,48)

        # Transform
        arr_2d_scaled = self.scaler.transform(arr_2d)

        # Reshape
        arr_3d_scaled = arr_2d_scaled.reshape(b, t, f)

        # Predict
        probs = self.model.predict(arr_3d_scaled)[0]  # shape (6,)
        return probs.tolist()

# Create a global instance so we only load once
sequence_LSTM_model = SequenceLSTMModel()
