// web_app/frontend/src/components/GoalQuadrantOverlay.js
import React from 'react';
import goalImg from '../assets/goal.png';  // Adjust path as needed

/**
 * Renders a goal image with 6 overlays, each tinted
 * green according to the probability in quadrantProbs[i].
 *
 * quadrantProbs = [
 *   p0, p1, p2,   // top row
 *   p3, p4, p5    // bottom row
 * ]
 */
function GoalQuadrantOverlay({ quadrantProbs }) {
  // For example, 600×400 image
  const containerWidth = 600;
  const containerHeight = 400;

  const cellW = containerWidth / 3;  // 3 columns
  const cellH = containerHeight / 2; // 2 rows

  // Simple function: scale probabilities up to 0.8 for opacity
  const alpha = (p) => 0.8 * p;

  return (
    <div
      style={{
        position: 'relative',
        width: containerWidth,
        height: containerHeight
      }}
    >
      {/* The background goal image */}
      <img
        src={goalImg}
        alt="Goal"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: containerWidth,
          height: containerHeight,
          objectFit: 'cover',
        }}
      />

      {/* Q0: top-left */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: cellW,
        height: cellH,
        backgroundColor: 'green',
        opacity: alpha(quadrantProbs[0] || 0),
      }} />

      {/* Q1: top-mid */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: cellW,
        width: cellW,
        height: cellH,
        backgroundColor: 'green',
        opacity: alpha(quadrantProbs[1] || 0),
      }} />

      {/* Q2: top-right */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: cellW * 2,
        width: cellW,
        height: cellH,
        backgroundColor: 'green',
        opacity: alpha(quadrantProbs[2] || 0),
      }} />

      {/* Q3: bottom-left */}
      <div style={{
        position: 'absolute',
        top: cellH,
        left: 0,
        width: cellW,
        height: cellH,
        backgroundColor: 'green',
        opacity: alpha(quadrantProbs[3] || 0),
      }} />

      {/* Q4: bottom-mid */}
      <div style={{
        position: 'absolute',
        top: cellH,
        left: cellW,
        width: cellW,
        height: cellH,
        backgroundColor: 'green',
        opacity: alpha(quadrantProbs[4] || 0),
      }} />

      {/* Q5: bottom-right */}
      <div style={{
        position: 'absolute',
        top: cellH,
        left: cellW * 2,
        width: cellW,
        height: cellH,
        backgroundColor: 'green',
        opacity: alpha(quadrantProbs[5] || 0),
      }} />
    </div>
  );
}

export default GoalQuadrantOverlay;
