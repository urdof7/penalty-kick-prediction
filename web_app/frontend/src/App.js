// web_app/frontend/src/App.js
import React, { useState, useRef } from 'react';

function App() {
  // ------------------ State ------------------
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState('');
  const [frameURLs, setFrameURLs] = useState([]);
  const [annotatedURLs, setAnnotatedURLs] = useState([]);
  const [statusMessage, setStatusMessage] = useState('');
  const [videoURL, setVideoURL] = useState('');

  // For stepping through frames:
  const [currentFrameIndex, setCurrentFrameIndex] = useState(0);
  // For stepping through annotated frames:
  const [currentAnnIndex, setCurrentAnnIndex] = useState(0);

  const videoRef = useRef(null);

  // ------------------ File Selection ------------------
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // ------------------ 1) Upload ------------------
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

      // Clear frames & annotated from previous session
      setFrameURLs([]);
      setAnnotatedURLs([]);
      setCurrentFrameIndex(0);
      setCurrentAnnIndex(0);

      // Create local preview URL
      const localVideoURL = URL.createObjectURL(selectedFile);
      setVideoURL(localVideoURL);

      setStatusMessage(`Upload success! Server stored: ${data.filename}`);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // ------------------ 2) Extract Frames ------------------
  const handleExtractFrames = async () => {
    if (!uploadedFilename) {
      alert('No uploaded file reference.');
      return;
    }
    if (!videoRef.current) {
      alert('Video not loaded.');
      return;
    }

    // We'll extract frames at the current time in the video
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
      setStatusMessage(data.message || 'Frames extracted!');

      // Clear old annotated frames if any
      setAnnotatedURLs([]);
      setCurrentAnnIndex(0);

      // Cache-buster so the browser always loads fresh images
      const now = Date.now();
      const newFrameURLs = (data.frame_urls || []).map(url =>
        `http://localhost:8098${url}?cb=${now}`
      );
      setFrameURLs(newFrameURLs);
      setCurrentFrameIndex(0);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // ------------------ 3) Detect Pose (Annotate) ------------------
  const handleDetectPose = async () => {
    if (!uploadedFilename) {
      alert('No uploaded file reference.');
      return;
    }
    if (frameURLs.length === 0) {
      alert('No frames found. Extract frames first.');
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
      setStatusMessage(data.message || 'Pose detection complete.');

      const now = Date.now();
      const annURLs = (data.annotated_frames || []).map(
        url => `http://localhost:8098${url}?cb=${now}`
      );
      setAnnotatedURLs(annURLs);
      setCurrentAnnIndex(0);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // ------------------ Navigation: Frames ------------------
  const handlePrevFrame = () => {
    setCurrentFrameIndex((idx) => (idx > 0 ? idx - 1 : idx));
  };
  const handleNextFrame = () => {
    setCurrentFrameIndex((idx) =>
      idx < frameURLs.length - 1 ? idx + 1 : idx
    );
  };

  // ------------------ Navigation: Annotated ------------------
  const handlePrevAnnotated = () => {
    setCurrentAnnIndex((idx) => (idx > 0 ? idx - 1 : idx));
  };
  const handleNextAnnotated = () => {
    setCurrentAnnIndex((idx) =>
      idx < annotatedURLs.length - 1 ? idx + 1 : idx
    );
  };

  // Helpers
  const totalFrames = frameURLs.length;
  const currentFrameUrl =
    totalFrames > 0 ? frameURLs[currentFrameIndex] : null;

  const totalAnn = annotatedURLs.length;
  const currentAnnUrl =
    totalAnn > 0 ? annotatedURLs[currentAnnIndex] : null;

  // ------------------ Render ------------------
  return (
    <div style={{ margin: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Frame & Pose Extraction</h1>

      {/* Upload Section */}
      <div>
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button onClick={handleUpload} style={{ marginLeft: '1rem' }}>
          Upload
        </button>
      </div>

      {statusMessage && <p>{statusMessage}</p>}

      {/* Video Preview + Frame Extraction */}
      {videoURL && (
        <div style={{ marginTop: '1rem' }}>
          <video
            ref={videoRef}
            src={videoURL}
            width="600"
            controls
          />
          <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
            <button onClick={handleExtractFrames}>
              Extract Frames at Current Time
            </button>
            {/* Only enable "Detect Pose" if we have some frames */}
            <button
              onClick={handleDetectPose}
              disabled={frameURLs.length === 0}
            >
              Detect Pose Features
            </button>
          </div>
        </div>
      )}

      {/* Single-Frame Viewer for raw frames */}
      {totalFrames > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Extracted Frames (Unannotated)</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button onClick={handlePrevFrame} disabled={currentFrameIndex === 0}>
              Prev
            </button>

            {currentFrameUrl ? (
              <img
                src={currentFrameUrl}
                alt={`Frame ${currentFrameIndex + 1}`}
                style={{ maxWidth: '600px', border: '1px solid #ccc' }}
              />
            ) : (
              <div>No Frame</div>
            )}

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

      {/* Single-Frame Viewer for annotated frames */}
      {totalAnn > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Annotated Frames (Pose Detection)</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button onClick={handlePrevAnnotated} disabled={currentAnnIndex === 0}>
              Prev
            </button>

            {currentAnnUrl ? (
              <img
                src={currentAnnUrl}
                alt={`Annotated ${currentAnnIndex + 1}`}
                style={{ maxWidth: '600px', border: '1px solid #ccc' }}
              />
            ) : (
              <div>No Annotated Frame</div>
            )}

            <button
              onClick={handleNextAnnotated}
              disabled={currentAnnIndex >= totalAnn - 1}
            >
              Next
            </button>
          </div>
          <p style={{ marginTop: '0.5rem' }}>
            Frame {currentAnnIndex + 1} of {totalAnn}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
