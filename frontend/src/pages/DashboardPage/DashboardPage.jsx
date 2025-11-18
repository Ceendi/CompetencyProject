import { useState, useRef } from "react";
import { motion, AnimatePresence, useMotionValue } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "./DashboardPage.css";
import ProgressBar from "../../components/ProgressBar/ProgressBar";
import FloatingInput from "../../components/FloatingInput/FloatingInput";
import JumpingDots from "../../components/JumpingDots/JumpingDots";
import AnimatedTable from "../../components/AnimatedTable/AnimatedTable";
import { useVideos } from "../../hooks/useVideos";
import { initiateAnalysis, getStatus, getResult } from "../../services/api";

export default function DashboardPage() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isCompleting, setIsCompleting] = useState(false);
  const { videos, setVideos } = useVideos();
  const progress = useMotionValue(0);
  const [videoUrl, setVideoUrl] = useState("");
  const abortControllerRef = useRef(null);
  const intervalRef = useRef(null);
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
    // Clear the interval
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
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
      // Initiate analysis
      const job = await initiateAnalysis(videoUrl);
      if (signal.aborted) return;
      console.log("Initiate analysis result:", job);

      if (job.error_message) {
        alert(`Błąd: ${job.error_message}`);
        setIsAnalyzing(false);
        return;
      }

      intervalRef.current = setInterval(async () => {
        try {
          const statusResponse = await getStatus(job.id);
          console.log("Status response:", statusResponse);

          if (statusResponse.error_message) {
            alert(`Błąd: ${statusResponse.error_message}`);
            clearInterval(intervalRef.current);
            intervalRef.current = null;
            setIsAnalyzing(false);
            progress.set(0);
            return;
          }

          // Update progress based on status
          switch (statusResponse.status) {
            case "downloading":
              progress.set(0);
              break;
            case "transcribing":
              progress.set(33);
              break;
            case "analyzing":
              progress.set(66);
              break;
            case "complete":
              progress.set(100);
              // Stop polling
              clearInterval(intervalRef.current);
              intervalRef.current = null;

              // Enter completion phase
              setIsCompleting(true);

              // Get result
              const result = await getResult(statusResponse.film_id);
              console.log("Result:", result);

              // Reset after completion
              setTimeout(() => {
                setIsAnalyzing(false);
                setIsCompleting(false);
                progress.set(0);

                setTimeout(() => {
                  setVideos((prevVideos) => {
                    const newVideos = [result, ...prevVideos];
                    console.log("Updated videos array:", newVideos);
                    return newVideos;
                  });
                }, 400);
              }, 1750);
              break;
            default:
              break;
          }
        } catch (error) {
          console.error("Error polling status:", error);
          clearInterval(intervalRef.current);
          intervalRef.current = null;
          setIsAnalyzing(false);
          progress.set(0);
          alert("Wystąpił błąd podczas sprawdzania statusu");
        }
      }, 2000);
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
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
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
