import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SEQUENCE_FILE = os.path.join(DATA_DIR, 'processed', 'sequence', 'training_data_sequence.npz')

REPORT_DIR = os.path.join(BASE_DIR, 'report', 'sequence')
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'sequence_models')

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

def load_data(npz_path):
    data = np.load(npz_path)
    X_seq = data['X_seq']
    y_seq = data['y_seq']
    return X_seq, y_seq

def remap_labels(y_seq):
    # Ensure zero-based labels
    unique_labels = np.unique(y_seq)
    # Create a mapping from old labels to new labels (0 to num_classes-1)
    label_map = {old_label: new_label for new_label, old_label in enumerate(sorted(unique_labels))}
    y_new = np.array([label_map[label] for label in y_seq])
    return y_new, len(unique_labels)

def scale_features(X_train, X_test):
    num_train, num_frames, num_features = X_train.shape
    num_test = X_test.shape[0]

    X_train_2d = X_train.reshape(num_train * num_frames, num_features)
    X_test_2d = X_test.reshape(num_test * num_frames, num_features)

    scaler = StandardScaler()
    X_train_2d = scaler.fit_transform(X_train_2d)
    X_test_2d = scaler.transform(X_test_2d)

    X_train_scaled = X_train_2d.reshape(num_train, num_frames, num_features)
    X_test_scaled = X_test_2d.reshape(num_test, num_frames, num_features)

    return X_train_scaled, X_test_scaled, scaler

def build_lstm_model(input_shape, num_classes):
    model = Sequential()
    model.add(Input(shape=input_shape))  # Define input layer
    model.add(LSTM(64))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

if __name__ == "__main__":
    X_seq, y_seq = load_data(SEQUENCE_FILE)

    # Remap labels to zero-based
    y_seq, num_classes = remap_labels(y_seq)

    # Check class counts for stratify
    unique, counts = np.unique(y_seq, return_counts=True)
    min_count = counts.min()

    if min_count < 2:
        print("Warning: Not enough samples in at least one class to stratify. Using random split.")
        X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)
    else:
        X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42, stratify=y_seq)

    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    input_shape = (X_train_scaled.shape[1], X_train_scaled.shape[2]) 
    model = build_lstm_model(input_shape, num_classes)

    history = model.fit(X_train_scaled, y_train, validation_split=0.2, epochs=20, batch_size=32)

    y_pred = model.predict(X_test_scaled)
    y_pred_labels = np.argmax(y_pred, axis=1)

    print("Classification Report:")
    report = classification_report(y_test, y_pred_labels, zero_division=0)
    print(report)

    cm = confusion_matrix(y_test, y_pred_labels)
    print("Confusion Matrix:")
    print(cm)

    model_path = os.path.join(MODELS_DIR, 'sequence_model.h5')
    model.save(model_path)

    scaler_path = os.path.join(MODELS_DIR, 'sequence_scaler.pkl')
    joblib.dump(scaler, scaler_path)

    report_path = os.path.join(REPORT_DIR, 'classification_report_sequence.txt')
    with open(report_path, 'w') as f:
        f.write(report)

    print(f"Model saved to: {os.path.relpath(model_path, BASE_DIR)}")
    print(f"Scaler saved to: {os.path.relpath(scaler_path, BASE_DIR)}")
    print(f"Report saved to: {os.path.relpath(report_path, BASE_DIR)}")
