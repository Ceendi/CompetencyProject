const MOCK_MODE = true; // Set to false when real backend is ready
import videosData from "../data/videos.json";

export async function fetchVideo(signal) {
  if (MOCK_MODE) {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        resolve({
          success: true,
          message: "Wideo zostało pobrane pomyślnie",
        });
      }, 500);

      // Listen for abort signal
      if (signal) {
        signal.addEventListener("abort", () => {
          clearTimeout(timeout);
          reject(new DOMException("Aborted", "AbortError"));
        });
      }
    });
  }
}

export async function convertSpeechToText(signal) {
  if (MOCK_MODE) {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        resolve({
          success: true,
          message: "Konwersja speech-to-text zakończona pomyślnie",
        });
      }, 500);

      // Listen for abort signal
      if (signal) {
        signal.addEventListener("abort", () => {
          clearTimeout(timeout);
          reject(new DOMException("Aborted", "AbortError"));
        });
      }
    });
  }
}

export async function analyzeSentiment(signal, usedVideoIds = []) {
  if (MOCK_MODE) {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        // Filter out already used videos
        const availableVideos = videosData.filter(
          (video) => !usedVideoIds.includes(video.id)
        );

        // If all videos are used, return error
        if (availableVideos.length === 0) {
          reject(
            new Error("Wszystkie dostępne video zostały już przeanalizowane")
          );
          return;
        }

        // Get random video from available videos
        const randomIndex = Math.floor(Math.random() * availableVideos.length);
        const randomVideo = availableVideos[randomIndex];

        resolve({
          success: true,
          message: "Analiza sentymentu ukończona pomyślnie",
          video: randomVideo,
        });
      }, 500);

      // Listen for abort signal
      if (signal) {
        signal.addEventListener("abort", () => {
          clearTimeout(timeout);
          reject(new DOMException("Aborted", "AbortError"));
        });
      }
    });
  }
}
