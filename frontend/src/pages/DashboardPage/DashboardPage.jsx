import { useState, useRef } from "react";
import { motion, AnimatePresence, useMotionValue } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "./DashboardPage.css";
import ProgressBar from "../../components/ProgressBar/ProgressBar";
import FloatingInput from "../../components/FloatingInput/FloatingInput";
import JumpingDots from "../../components/JumpingDots/JumpingDots";
import AnimatedTable from "../../components/AnimatedTable/AnimatedTable";
import { useVideos } from "../../hooks/useVideos";
import {
  fetchVideo,
  convertSpeechToText,
  analyzeSentiment,
} from "../../services/api";

export default function DashboardPage() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isCompleting, setIsCompleting] = useState(false);
  const { videos, setVideos } = useVideos();
  const progress = useMotionValue(0);
  const [videoUrl, setVideoUrl] = useState("");
  const abortControllerRef = useRef(null);
  const navigate = useNavigate();

  function handleViewSummary(videoId) {
    navigate(`/reviews/${videoId}`);
  }

  function handleCancelAnalyze() {
    // Don't allow cancel during completion phase
    if (isCompleting) return;

    // Abort the ongoing API requests
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setIsAnalyzing(false);
    progress.set(0);
  }

  async function handleAnalyzeClick() {
    if (!videoUrl.trim()) {
      alert("Proszę wpisać URL wideo");
      return;
    }

    // Create new AbortController for this analysis
    abortControllerRef.current = new AbortController();
    const signal = abortControllerRef.current.signal;

    setIsAnalyzing(true);
    progress.set(0);

    try {
      // Step 1: Fetch video (33%)
      const fetchResult = await fetchVideo(signal);
      if (signal.aborted) return; // Check if cancelled
      console.log("Fetch video result:", fetchResult);
      progress.set(33);

      // Step 2: Convert speech to text (66%)
      const speechResult = await convertSpeechToText(signal);
      if (signal.aborted) return; // Check if cancelled
      console.log("Speech to text result:", speechResult);
      progress.set(66);

      // Step 3: Analyze sentiment (100%)
      const usedVideoIds = videos.map((v) => v.id);
      const sentimentResult = await analyzeSentiment(signal, usedVideoIds);
      if (signal.aborted) return; // Check if cancelled
      console.log("Sentiment analysis result:", sentimentResult);
      progress.set(100);

      // Enter completion phase - can't cancel anymore
      setIsCompleting(true);

      // Reset after completion
      setTimeout(() => {
        setIsAnalyzing(false);
        setIsCompleting(false);
        progress.set(0);

        setTimeout(() => {
          if (sentimentResult.success && sentimentResult.video) {
            setVideos((prevVideos) => {
              const newVideos = [sentimentResult.video, ...prevVideos];
              console.log("Updated videos array:", newVideos);
              return newVideos;
            });
          }
        }, [400]);
      }, 1750);
    } catch (error) {
      // Check if error is due to abort
      if (error.name === "AbortError") {
        console.log("Analysis was cancelled");
        return;
      }
      console.error("Error during analysis:", error);
      alert("Wystąpił błąd podczas analizy");
      setIsAnalyzing(false);
      setIsCompleting(false);
      progress.set(0);
    } finally {
      abortControllerRef.current = null;
    }
  }

  return (
    <div>
      <h1 className="dashboard-title">Analyze Video Reviews</h1>
      <p className="dashboard-paste-info">
        Paste the link to a video review from YouTube, TikTok, or Instagram to
        get started.
      </p>
      <div className="dashboard-input-container">
        <FloatingInput
          id="video-url-input"
          label="Paste video link here..."
          value={videoUrl}
          onChange={(e) => setVideoUrl(e.target.value)}
          disabled={isAnalyzing}
        />

        <AnimatePresence>
          {isAnalyzing && (
            <motion.div
              className="dashboard-analyzing-container"
              initial={{ opacity: 0, y: -20, height: 0 }}
              animate={{ opacity: 1, y: 0, height: "auto" }}
              exit={{ opacity: 0, y: -20, height: 0 }}
              transition={{ duration: 0.4, ease: "easeOut" }}
            >
              <p className="dashboard-analyzing-text">
                Analyzing video
                <JumpingDots />
              </p>
              <ProgressBar progress={progress} />
              <p className="dashboard-analyzing-info">
                This may take a few minutes.
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        <motion.button
          className={`dashboard-analyze-button ${isAnalyzing ? "cancel" : ""}`}
          onClick={isAnalyzing ? handleCancelAnalyze : handleAnalyzeClick}
          disabled={isCompleting}
          layout
          whileHover={{ scale: isCompleting ? 1 : 1.05 }}
          whileTap={{ scale: isCompleting ? 1 : 0.95 }}
          transition={{ duration: 0.2 }}
          style={{
            opacity: isCompleting ? 0.5 : 1,
            cursor: isCompleting ? "not-allowed" : "pointer",
          }}
        >
          {isAnalyzing ? "Cancel Analyze" : "Analyze"}
        </motion.button>
      </div>

      <h2 className="dashboard-subtitle">Recent Analyses</h2>

      <AnimatedTable
        videos={videos}
        handleViewSummary={handleViewSummary}
        maxItems={3}
      />
    </div>
  );
}
