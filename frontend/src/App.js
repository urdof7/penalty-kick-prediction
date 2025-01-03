// src/App.js

import React, { useState, useRef } from 'react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  // We'll use a ref to interact with the <video> element
  const videoRef = useRef(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setStatusMessage('No file selected');
      return;
    }
    setStatusMessage('Uploading...');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      // Upload to your Flask /upload endpoint
      const res = await fetch('http://localhost:8080/upload', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) throw new Error('Upload failed');

      const data = await res.json();
      setUploadedFilename(data.filename);
      setStatusMessage('Upload successful!');
    } catch (err) {
      console.error(err);
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  const handleMarkMidswing = () => {
    if (!videoRef.current) {
      return;
    }
    // currentTime is the playback time in seconds
    const midswingTime = videoRef.current.currentTime;
    alert(`Midswing time marked at ${midswingTime.toFixed(2)}s`);

    // Here, you could do a POST request to Flask with the midswing time
    // or store it in state for future processing
    // Example:
    // fetch('http://localhost:8080/set_midswing', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ filename: uploadedFilename, midswing: midswingTime }),
    // });
  };

  return (
    <div style={styles.container}>
      <h1>Penalty Kick Prediction</h1>
      <p>Upload a video to mark the midswing time.</p>

      <div style={styles.uploadSection}>
        <input
          type="file"
          accept="video/*"
          onChange={handleFileChange}
        />
        <button style={styles.uploadButton} onClick={handleUpload}>
          Upload
        </button>
      </div>

      {statusMessage && <p>{statusMessage}</p>}

      {uploadedFilename && (
        <div style={styles.videoSection}>
          <h3>Uploaded Video:</h3>
          <video
            ref={videoRef}
            src={`http://localhost:8080/videos/${uploadedFilename}`}
            controls
            width="600"
          />
          <div style={styles.btnRow}>
            <button onClick={handleMarkMidswing}>
              Mark Midswing
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    margin: '2rem',
    fontFamily: 'Arial, sans-serif',
  },
  uploadSection: {
    marginBottom: '1rem',
  },
  uploadButton: {
    marginLeft: '1rem',
  },
  videoSection: {
    marginTop: '2rem'
  },
  btnRow: {
    marginTop: '1rem'
  }
};

export default App;
