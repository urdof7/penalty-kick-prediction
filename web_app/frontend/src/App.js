// web_app/frontend/src/App.js
import React, { useState, useRef } from 'react';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState('');
  const [frameURLs, setFrameURLs] = useState([]);
  const [annotatedURLs, setAnnotatedURLs] = useState([]); // <-- NEW
  const [statusMessage, setStatusMessage] = useState('');
  const [videoURL, setVideoURL] = useState('');
  const [currentFrameIndex, setCurrentFrameIndex] = useState(0);

  const videoRef = useRef(null);

  // 1) Choose a file
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // 2) Upload
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
      const data = await res.json();
      setUploadedFilename(data.filename);

      // Clear old frames & annotated
      setFrameURLs([]);
      setAnnotatedURLs([]);
      setCurrentFrameIndex(0);

      // Local URL for preview
      const localVideoURL = URL.createObjectURL(selectedFile);
      setVideoURL(localVideoURL);

      setStatusMessage(`Upload success! Stored filename: ${data.filename}`);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // 3) Extract frames at currentTime
  const handleExtractFrames = async () => {
    if (!uploadedFilename) {
      alert('No uploaded file reference.');
      return;
    }
    if (!videoRef.current) {
      alert('Video not loaded.');
      return;
    }

    const currentTime = videoRef.current.currentTime;
    setStatusMessage(`Extracting frames at ${currentTime.toFixed(2)}s...`);

    try {
      const body = { filename: uploadedFilename, timestamp: currentTime };
      const res = await fetch('http://localhost:8098/api/extract_frames', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        credentials: 'include'
      });
      if (!res.ok) throw new Error('Frame extraction failed');
      const data = await res.json();
      setStatusMessage(data.message || 'Frames extracted');
      
      // Clear any annotated frames from previous run
      setAnnotatedURLs([]);
      setCurrentFrameIndex(0);

      // Add cache-buster param to avoid old images
      const now = Date.now();
      const newFrameURLs = (data.frame_urls || []).map(url => 
        `http://localhost:8098${url}?cb=${now}`
      );
      setFrameURLs(newFrameURLs);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // 4) Detect Pose
  const handleDetectPose = async () => {
    if (!uploadedFilename) {
      alert('No uploaded file reference.');
      return;
    }
    setStatusMessage('Detecting pose...');

    try {
      const body = { filename: uploadedFilename };
      const res = await fetch('http://localhost:8098/api/detect_pose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        credentials: 'include'
      });
      if (!res.ok) throw new Error('Pose detection failed');
      const data = await res.json();
      setStatusMessage(data.message || 'Pose detection done.');

      // Build annotated frame URLs with cache-buster
      const now = Date.now();
      const annURLs = (data.annotated_frames || []).map(url =>
        `http://localhost:8098${url}?cb=${now}`
      );
      setAnnotatedURLs(annURLs);
      setCurrentFrameIndex(0);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // Single-frame nav for annotated
  const handleNextFrame = () => {
    setCurrentFrameIndex(i => (i < annotatedURLs.length - 1 ? i + 1 : i));
  };
  const handlePrevFrame = () => {
    setCurrentFrameIndex(i => (i > 0 ? i - 1 : 0));
  };

  return (
    <div style={{ margin: '2rem' }}>
      <h1>Frame & Pose Extraction</h1>

      <div>
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button onClick={handleUpload} style={{ marginLeft: '1rem' }}>
          Upload
        </button>
      </div>

      {statusMessage && <p>{statusMessage}</p>}

      {videoURL && (
        <div style={{ marginTop: '1rem' }}>
          <video ref={videoRef} src={videoURL} width="600" controls />
          <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
            <button onClick={handleExtractFrames}>
              Extract Frames at Current Time
            </button>
            <button onClick={handleDetectPose} disabled={frameURLs.length === 0}>
              Detect Pose
            </button>
          </div>
        </div>
      )}

      {/* Show extracted frames in a small grid */}
      {frameURLs.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Extracted Frames (Not Annotated)</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            {frameURLs.map((url, i) => (
              <img
                key={i}
                src={url}
                alt={`Frame ${i + 1}`}
                style={{ width: '120px', border: '1px solid #ccc' }}
              />
            ))}
          </div>
        </div>
      )}

      {/* Single-frame viewer for annotated frames */}
      {annotatedURLs.length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Annotated Frames Viewer</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button onClick={handlePrevFrame} disabled={currentFrameIndex === 0}>
              Prev
            </button>
            <img
              src={annotatedURLs[currentFrameIndex]}
              alt={`Annotated ${currentFrameIndex + 1}`}
              style={{ maxWidth: '600px', border: '1px solid #ccc' }}
            />
            <button
              onClick={handleNextFrame}
              disabled={currentFrameIndex === annotatedURLs.length - 1}
            >
              Next
            </button>
          </div>
          <p>
            Frame {currentFrameIndex + 1} of {annotatedURLs.length}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
