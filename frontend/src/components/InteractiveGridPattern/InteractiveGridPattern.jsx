import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./InteractiveGridPattern.css";

export default function InteractiveGridPattern({ className = "" }) {
  const [activeSquares, setActiveSquares] = useState(new Map());
  const [currentSquare, setCurrentSquare] = useState(null);

  const SQUARE_SIZE = 35;

  const FADE_DURATION = 500;

  useEffect(() => {
    const handleMouseMove = (e) => {
      // Since grid is position: fixed, use clientX/clientY (viewport coordinates)
      const col = Math.floor(e.clientX / SQUARE_SIZE);
      const row = Math.floor(e.clientY / SQUARE_SIZE);
      const key = `${col}-${row}`;

      setCurrentSquare(key);

      // Add current square to active squares with timestamp
      setActiveSquares((prev) => {
        const newMap = new Map(prev);
        newMap.set(key, Date.now());
        return newMap;
      });
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, [SQUARE_SIZE]);

  // Clean up old squares periodically
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      setActiveSquares((prev) => {
        const newMap = new Map(prev);
        for (const [key, timestamp] of newMap.entries()) {
          if (now - timestamp > FADE_DURATION) {
            newMap.delete(key);
          }
        }
        return newMap;
      });
    }, 100);

    return () => clearInterval(interval);
  }, []);

  const getSquareOpacity = (key, timestamp) => {
    const now = Date.now();
    const age = now - timestamp;

    // Current square - full opacity
    if (key === currentSquare) {
      return 0.3;
    }

    // Previous squares - fade out over time
    const opacity = 0.3 * (1 - age / FADE_DURATION);
    return Math.max(0, opacity);
  };

  return (
    <div className={`interactive-grid-container ${className}`}>
      <svg className="interactive-grid-svg">
        <defs>
          <pattern
            id="interactive-grid"
            width={SQUARE_SIZE}
            height={SQUARE_SIZE}
            patternUnits="userSpaceOnUse"
          >
            <path
              d={`M ${SQUARE_SIZE} 0 L 0 0 0 ${SQUARE_SIZE}`}
              fill="none"
              stroke="rgba(255, 255, 255, 0.06)"
              strokeWidth="1"
            />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#interactive-grid)" />
      </svg>

      <div className="interactive-grid-overlay">
        <AnimatePresence>
          {Array.from(activeSquares.entries()).map(([key, timestamp]) => {
            const [col, row] = key.split("-").map(Number);
            const opacity = getSquareOpacity(key, timestamp);

            if (opacity <= 0) return null;

            return (
              <motion.div
                key={key}
                className="interactive-grid-square"
                style={{
                  left: `${col * SQUARE_SIZE}px`,
                  top: `${row * SQUARE_SIZE}px`,
                  width: `${SQUARE_SIZE}px`,
                  height: `${SQUARE_SIZE}px`,
                }}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{
                  opacity: opacity,
                  scale: key === currentSquare ? 1 : 0.95,
                }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.15, ease: "easeOut" }}
              />
            );
          })}
        </AnimatePresence>
      </div>
    </div>
  );
}
