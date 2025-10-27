import { motion } from "framer-motion";

export default function JumpingDots() {
  return (
    <span style={{ display: "inline-block", marginLeft: "4px" }}>
      <motion.span
        style={{ display: "inline-block" }}
        animate={{ y: [0, -6, 0] }}
        transition={{
          duration: 0.6,
          repeat: Infinity,
          repeatDelay: 0.2,
          ease: "easeInOut",
        }}
      >
        .
      </motion.span>
      <motion.span
        style={{ display: "inline-block" }}
        animate={{ y: [0, -6, 0] }}
        transition={{
          duration: 0.6,
          repeat: Infinity,
          repeatDelay: 0.2,
          delay: 0.2,
          ease: "easeInOut",
        }}
      >
        .
      </motion.span>
      <motion.span
        style={{ display: "inline-block" }}
        animate={{ y: [0, -6, 0] }}
        transition={{
          duration: 0.6,
          repeat: Infinity,
          repeatDelay: 0.2,
          delay: 0.4,
          ease: "easeInOut",
        }}
      >
        .
      </motion.span>
    </span>
  );
}
