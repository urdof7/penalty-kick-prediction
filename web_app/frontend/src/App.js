// web_app/frontend/src/App.js
import React, { useState, useRef } from 'react';
import GoalQuadrantOverlay from './components/GoalQuadrantOverlay';

function App() {
  // ------------------ State ------------------
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState('');
  const [frameURLs, setFrameURLs] = useState([]);
  const [annotatedURLs, setAnnotatedURLs] = useState([]);
  const [directionProbs, setDirectionProbs] = useState([]); // 6 probabilities
  const [statusMessage, setStatusMessage] = useState('');
  const [videoURL, setVideoURL] = useState('');

  // Single-frame nav for extracted frames
  const [currentFrameIndex, setCurrentFrameIndex] = useState(0);
  // Single-frame nav for annotated frames
  const [currentAnnIndex, setCurrentAnnIndex] = useState(0);

  const videoRef = useRef(null);

  // ------------------ 1) Select file ------------------
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // ------------------ 2) Upload ------------------
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
        credentials: 'include',
      });
      if (!res.ok) throw new Error('Upload failed');

      const data = await res.json();
      setUploadedFilename(data.filename);

      // Clear old data
      setFrameURLs([]);
      setAnnotatedURLs([]);
      setDirectionProbs([]);

      // Reset indices
      setCurrentFrameIndex(0);
      setCurrentAnnIndex(0);

      // Show local video preview
      const localVideoURL = URL.createObjectURL(selectedFile);
      setVideoURL(localVideoURL);

      setStatusMessage(`Upload success! Server filename: ${data.filename}`);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // ------------------ 3) Extract Frames ------------------
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
      setStatusMessage(data.message || 'Frames extracted!');

      // Clear annotated + directionProbs
      setAnnotatedURLs([]);
      setDirectionProbs([]);
      setCurrentAnnIndex(0);

      // Build frame URLs with cache-buster
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

  // ------------------ 4) Detect Pose ------------------
  const handleDetectPose = async () => {
    if (!uploadedFilename) {
      alert('No uploaded file reference.');
      return;
    }
    if (frameURLs.length === 0) {
      alert('No frames extracted. Please extract frames first.');
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

      // Build annotated frame URLs with cache-buster
      const now = Date.now();
      const annURLs = (data.annotated_frames || []).map(
        url => `http://localhost:8098${url}?cb=${now}`
      );
      setAnnotatedURLs(annURLs);
      setCurrentAnnIndex(0);

      // Clear directionProbs
      setDirectionProbs([]);
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // ------------------ 5) Predict Kick Direction ------------------
  const handlePredictDirection = async () => {
    if (!uploadedFilename) {
      alert('No uploaded file reference.');
      return;
    }
    if (annotatedURLs.length === 0) {
      alert('No annotated frames. Please detect pose first.');
      return;
    }

    setStatusMessage('Predicting kick direction from DB...');
    try {
      // We only pass { filename } to let the backend do the DB-based feature engineering
      const body = { filename: uploadedFilename };
      const res = await fetch('http://localhost:8098/api/predict_kick', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        credentials: 'include'
      });
      if (!res.ok) throw new Error('Prediction request failed');

      const data = await res.json();
      const probs = data.quadrant_probs || [];
      setDirectionProbs(probs);

      setStatusMessage(data.message || 'Kick direction predicted.');
    } catch (err) {
      setStatusMessage(err.message);
    }
  };

  // ---------- Single-frame navigation: frames ----------
  const totalFrames = frameURLs.length;
  const currentFrameUrl =
    totalFrames > 0 ? frameURLs[currentFrameIndex] : null;

  const handlePrevFrame = () => {
    setCurrentFrameIndex((idx) => (idx > 0 ? idx - 1 : idx));
  };
  const handleNextFrame = () => {
    setCurrentFrameIndex((idx) =>
      idx < totalFrames - 1 ? idx + 1 : idx
    );
  };

  // ---------- Single-frame navigation: annotated ----------
  const totalAnn = annotatedURLs.length;
  const currentAnnUrl =
    totalAnn > 0 ? annotatedURLs[currentAnnIndex] : null;

  const handlePrevAnn = () => {
    setCurrentAnnIndex((idx) => (idx > 0 ? idx - 1 : idx));
  };
  const handleNextAnn = () => {
    setCurrentAnnIndex((idx) =>
      idx < totalAnn - 1 ? idx + 1 : idx
    );
  };

  // ---------- Render ----------
  return (
    <div style={{ margin: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>Frame & Pose Extraction + Kick Prediction (6 Quadrants)</h1>

      {/* 1) File Upload */}
      <div>
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button onClick={handleUpload} style={{ marginLeft: '1rem' }}>
          Upload
        </button>
      </div>

      {statusMessage && <p>{statusMessage}</p>}

      {/* 2) Video Preview + Extract + Pose */}
      {videoURL && (
        <div style={{ marginTop: '1rem' }}>
          <video ref={videoRef} src={videoURL} width="600" controls />
          <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
            <button onClick={handleExtractFrames}>
              Extract Frames
            </button>
            <button
              onClick={handleDetectPose}
              disabled={frameURLs.length === 0}
            >
              Detect Pose
            </button>
            <button
              onClick={handlePredictDirection}
              disabled={annotatedURLs.length === 0}
            >
              Predict Kick Direction
            </button>
          </div>
        </div>
      )}

      {/* 3) Single-frame viewer: extracted frames */}
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

      {/* 4) Single-frame viewer: annotated frames */}
      {totalAnn > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Annotated Frames (Pose Detection)</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button onClick={handlePrevAnn} disabled={currentAnnIndex === 0}>
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
              onClick={handleNextAnn}
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

      {/* 5) GoalQuadrantOverlay if we have directionProbs */}
      {directionProbs.length === 6 && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Kick Direction Probabilities (6 Quadrants)</h3>
          <GoalQuadrantOverlay quadrantProbs={directionProbs} />
          <div style={{ marginTop: '1rem' }}>
            <p>
              Quadrant Probabilities:
              {directionProbs.map((p, i) => (
                <span key={i} style={{ marginLeft: '0.5rem' }}>
                  Q{i}: {(p * 100).toFixed(1)}%
                </span>
              ))}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
