import sys
import os
import numpy as np

def print_npz_info(X_seq, y_seq):
    print("=== NPZ File Info ===")
    print(f"X_seq shape: {X_seq.shape} (samples, frames, features)")
    print(f"y_seq shape: {y_seq.shape} (samples,)")
    print(f"X_seq dtype: {X_seq.dtype}, y_seq dtype: {y_seq.dtype}")
    print(f"Number of samples: {X_seq.shape[0]}")
    if X_seq.shape[0] > 0:
        print(f"Number of frames per sample: {X_seq.shape[1]}")
        print(f"Number of features per frame: {X_seq.shape[2]}")
    unique_labels, counts = np.unique(y_seq, return_counts=True)
    print("Label distribution:")
    for label, count in zip(unique_labels, counts):
        print(f"  Label {label}: {count} samples")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect_npz_info.py <path_to_npz>")
        sys.exit(1)

    npz_path = sys.argv[1]
    if not os.path.exists(npz_path):
        print(f"File not found: {npz_path}")
        sys.exit(1)

    data = np.load(npz_path)
    X_seq = data.get('X_seq')
    y_seq = data.get('y_seq')

    if X_seq is None or y_seq is None:
        print("Error: X_seq or y_seq not found in the NPZ file.")
        sys.exit(1)

    print_npz_info(X_seq, y_seq)
