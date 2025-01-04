// web_app/frontend/src/App.js
import React, { useState, useRef } from 'react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState('');
  const [frameURLs, setFrameURLs] = useState([]);
  const [statusMessage, setStatusMessage] = useState('');
  const videoRef = useRef(null);
  const [videoURL, setVideoURL] = useState('');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // Upload the file to /api/upload
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
        credentials: 'include' // if you need to send or receive cookies
      });
      if (!res.ok) throw new Error('Upload failed');

      const data = await res.json();
      setUploadedFilename(data.filename);

      // Create a local object URL to preview
      const localVideoURL = URL.createObjectURL(selectedFile);
      setVideoURL(localVideoURL);

      setStatusMessage(`Upload success! Stored filename: ${data.filename}`);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // Extract frames at current video time
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
        filename: uploadedFilename,  // must match what was stored in DB
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
      setFrameURLs(data.frame_urls || []);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

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

      {videoURL && (
        <div style={{ marginTop: '1rem' }}>
          <video
            ref={videoRef}
            src={videoURL}
            width="600"
            controls
          />
          <div style={{ marginTop: '1rem' }}>
            <button onClick={handleExtractFrames}>
              Extract Frames at Current Time
            </button>
          </div>
        </div>
      )}

      {frameURLs.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Extracted Frames:</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            {frameURLs.map((url, i) => (
              <img
                key={i}
                src={`http://localhost:8098${url}`}
                alt={`Frame ${i + 1}`}
                style={{ width: '150px', border: '1px solid #ccc' }}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
