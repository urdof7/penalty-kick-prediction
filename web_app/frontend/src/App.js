// App.js (place in /frontend/src/App.js, for example)

import React, { useState, useRef } from 'react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState('');
  const [videoURL, setVideoURL] = useState('');
  const [frameURLs, setFrameURLs] = useState([]);
  const [statusMessage, setStatusMessage] = useState('');
  const videoRef = useRef(null);

  // 1) Handle file selection
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // 2) Upload file to Flask
  const handleUpload = async () => {
    if (!selectedFile) {
      alert('No file selected!');
      return;
    }

    setStatusMessage('Uploading...');
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const res = await fetch('http://localhost:8098/upload', {
        method: 'POST',
        body: formData
      });
      if (!res.ok) {
        throw new Error('Upload failed');
      }
      const data = await res.json();
      setUploadedFilename(data.filename);
      setStatusMessage(`Upload succeeded: ${data.filename}`);

      // Create an object URL so we can preview the video locally
      // This only helps user watch it; it doesn't come from the server
      const localURL = URL.createObjectURL(selectedFile);
      setVideoURL(localURL);
    } catch (error) {
      setStatusMessage(error.message);
    }
  };

  // 3) Mark midswing -> call extract_frames
  const handleExtractFrames = async () => {
    if (!uploadedFilename) {
      alert('No uploaded filename found. Please upload first.');
      return;
    }
    if (!videoRef.current) {
      alert('No video ref found.');
      return;
    }

    const midswingTime = videoRef.current.currentTime;
    setStatusMessage('Extracting frames...');

    try {
      const res = await fetch('http://localhost:8098/extract_frames', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ filename: uploadedFilename, midswing_time: midswingTime })
      });
      if (!res.ok) {
        throw new Error('Frame extraction failed');
      }
      const data = await res.json();
      setStatusMessage(data.message);
      setFrameURLs(data.frame_urls || []);
    } catch (error) {
      setStatusMessage(error.message);
    }
  };

  return (
    <div style={{ margin: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>Penalty Kick Frame Extractor (Demo)</h1>

      <div style={{ marginBottom: '1rem' }}>
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button onClick={handleUpload} style={{ marginLeft: '1rem' }}>
          Upload
        </button>
      </div>

      {statusMessage && <p>{statusMessage}</p>}

      {/* If we have a local videoURL, show a video player */}
      {videoURL && (
        <div style={{ marginBottom: '1rem' }}>
          <video
            ref={videoRef}
            src={videoURL}
            width="600"
            controls
          />
          <div style={{ marginTop: '0.5rem' }}>
            <button onClick={handleExtractFrames}>
              Extract Frames at Current Time
            </button>
          </div>
        </div>
      )}

      {/* Display extracted frames */}
      {frameURLs.length > 0 && (
        <div>
          <h3>Extracted Frames:</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            {frameURLs.map((url, idx) => (
              <img
                key={idx}
                src={`http://localhost:8098${url}`}
                alt={`Frame ${idx + 1}`}
                style={{ width: '120px', border: '1px solid #ccc' }}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
