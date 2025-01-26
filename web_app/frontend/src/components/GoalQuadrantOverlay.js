import React, { useState } from 'react';
import goalImg from '../assets/goal.png';

const GoalQuadrantOverlay = ({ quadrantProbs }) => {
  const [hoveredIndex, setHoveredIndex] = useState(null);
  
  const containerWidth = 600;
  const containerHeight = 400;
  
  const goalTop = containerHeight * 0.29;
  const goalHeight = containerHeight * 0.4;
  const goalWidth = containerWidth * 0.58;
  const goalLeft = (containerWidth - goalWidth) / 2;

  const cellW = goalWidth / 3;
  const cellH = goalHeight / 2;

  const formatPercentage = (value) => {
    const percentage = value > 1 ? value : value * 100;
    return percentage.toFixed(1);
  };

  const maxProb = Math.max(...quadrantProbs);
  
  const getOpacity = (prob) => {
    const decimal = prob > 1 ? prob / 100 : prob;
    const relativeValue = decimal / (maxProb > 1 ? maxProb / 100 : maxProb);
    return 0.2 + (relativeValue * 0.4);
  };

  const quadrantStyle = {
    position: 'absolute',
    backgroundColor: 'green',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.2s ease-in-out',
    cursor: 'pointer',
    border: 'none',
  };

  const textStyle = {
    color: 'white',
    fontSize: '1rem',
    fontWeight: 'bold',
    textShadow: '1px 1px 2px rgba(0,0,0,0.7)',
    transition: 'transform 0.2s ease-in-out',
  };

  return (
    <div
      style={{
        position: 'relative',
        width: containerWidth,
        height: containerHeight,
      }}
    >
      <img
        src={goalImg}
        alt="Soccer Goal"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
        }}
      />

      {quadrantProbs.map((prob, index) => {
        const row = Math.floor(index / 3);
        const col = index % 3;
        const isHovered = hoveredIndex === index;
        
        return (
          <div
            key={index}
            style={{
              ...quadrantStyle,
              top: goalTop + (row * cellH),
              left: goalLeft + (col * cellW),
              width: cellW,
              height: cellH,
              opacity: isHovered ? getOpacity(prob) + 0.15 : getOpacity(prob),
              border: isHovered ? '2px solid rgba(255, 255, 255, 0.8)' : 'none',
              transform: isHovered ? 'scale(1.02)' : 'scale(1)',
              zIndex: isHovered ? 2 : 1,
            }}
            onMouseEnter={() => setHoveredIndex(index)}
            onMouseLeave={() => setHoveredIndex(null)}
          >
            <span 
              style={{
                ...textStyle,
                transform: isHovered ? 'scale(1.1)' : 'scale(1)',
                fontSize: isHovered ? '1.1rem' : '1rem',
              }}
            >
              {formatPercentage(prob)}%
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default GoalQuadrantOverlay;