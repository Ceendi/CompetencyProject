import { useSpring, useTransform } from "framer-motion";
import { motion } from "framer-motion";
import "./ProgressBar.css";

export default function ProgressBar({ progress }) {
  const springProgress = useSpring(progress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001,
  });

  const scaleX = useTransform(springProgress, [0, 100], [0, 1]);

  return (
    <div className="progress-bar-container">
      <motion.div
        className="progress-bar-fill"
        style={{ scaleX, originX: 0 }}
      />
    </div>
  );
}
