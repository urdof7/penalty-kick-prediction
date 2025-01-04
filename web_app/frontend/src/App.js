// web_app/frontend/src/App.js

import React, { useState, useRef } from 'react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState('');
  const [frameURLs, setFrameURLs] = useState([]);
  const [statusMessage, setStatusMessage] = useState('');
  const [videoURL, setVideoURL] = useState('');
  const [currentFrameIndex, setCurrentFrameIndex] = useState(0);

  const videoRef = useRef(null);

  // -------- Handle file selection
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // -------- Upload the file to /api/upload
  const handleUpload = async () => {
    if (!selectedFile) {
      alert('No file selected!');
      return;
    }

    setStatusMessage('Uploading...');
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const res = await fetch('http://localhost:8098/api/upload', {
        method: 'POST',
        body: formData,
        credentials: 'include'
      });
      if (!res.ok) throw new Error('Upload failed');

      // Parse response
      const data = await res.json();
      setUploadedFilename(data.filename);

      // Clear out old frames from UI
      setFrameURLs([]);
      setCurrentFrameIndex(0);

      // Create a local object URL for the new video
      const localVideoURL = URL.createObjectURL(selectedFile);
      setVideoURL(localVideoURL);

      setStatusMessage(`Upload success! Stored filename: ${data.filename}`);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // -------- Extract frames at current video time
  const handleExtractFrames = async () => {
    if (!uploadedFilename) {
      alert('No uploaded file reference. Please upload first.');
      return;
    }
    if (!videoRef.current) {
      alert('Video not loaded.');
      return;
    }

    const currentTime = videoRef.current.currentTime;
    setStatusMessage(`Extracting frames at time: ${currentTime.toFixed(2)}s...`);

    try {
      const body = {
        filename: uploadedFilename, // matches DB
        timestamp: currentTime
      };
      const res = await fetch('http://localhost:8098/api/extract_frames', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        credentials: 'include'
      });
      if (!res.ok) throw new Error('Frame extraction failed');

      const data = await res.json();
      setStatusMessage(data.message);

      // CLEAR out any old frames
      setFrameURLs([]);

      // We'll build new frame URLs with a cache-buster param
      // e.g. ?cb=1679590285
      const now = Date.now();
      const newFrameURLs = (data.frame_urls || []).map((url) => {
        return `http://localhost:8098${url}?cb=${now}`;
      });

      setFrameURLs(newFrameURLs);
      setCurrentFrameIndex(0);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // -------- Single-Frame Navigation
  const handleNextFrame = () => {
    setCurrentFrameIndex((prev) =>
      prev < frameURLs.length - 1 ? prev + 1 : prev
    );
  };

  const handlePrevFrame = () => {
    setCurrentFrameIndex((prev) => (prev > 0 ? prev - 1 : prev));
  };

  const totalFrames = frameURLs.length;
  const currentFrameUrl =
    totalFrames > 0 && currentFrameIndex < totalFrames
      ? frameURLs[currentFrameIndex]
      : null;

  return (
    <div style={{ margin: '2rem' }}>
      <h1>Penalty Kick Frame Extraction</h1>

      <div>
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button onClick={handleUpload} style={{ marginLeft: '1rem' }}>
          Upload
        </button>
      </div>

      {statusMessage && <p>{statusMessage}</p>}

      {/* Video + Extract */}
      {videoURL && (
        <div style={{ marginTop: '1rem' }}>
          <video ref={videoRef} src={videoURL} width="600" controls />
          <div style={{ marginTop: '1rem' }}>
            <button onClick={handleExtractFrames}>
              Extract Frames at Current Time
            </button>
          </div>
        </div>
      )}

      {/* Single-Frame Viewer */}
      {totalFrames > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Extracted Frames</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            {/* Prev Button */}
            <button onClick={handlePrevFrame} disabled={currentFrameIndex <= 0}>
              Prev
            </button>

            {/* The main image */}
            {currentFrameUrl ? (
              <img
                src={currentFrameUrl}
                alt={`Frame ${currentFrameIndex + 1}`}
                style={{ maxWidth: '800px', border: '1px solid #ccc' }}
              />
            ) : (
              <div>No Frame</div>
            )}

            {/* Next Button */}
            <button
              onClick={handleNextFrame}
              disabled={currentFrameIndex >= totalFrames - 1}
            >
              Next
            </button>
          </div>
          <p style={{ marginTop: '0.5rem' }}>
            Frame {currentFrameIndex + 1} of {totalFrames}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
