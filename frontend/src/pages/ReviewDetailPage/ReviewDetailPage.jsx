import { useParams } from "react-router-dom";
import "./ReviewDetailPage.css";
import { useVideos } from "../../hooks/useVideos";

export function ReviewDetailPage() {
  const { id } = useParams();
  const { videos, setVideos } = useVideos();

  // `useParams` returns strings, while `video.id` may be a number — compare as strings
  const video = videos.find((v) => String(v.id) === id);

  if (!video) {
    return (
      <div className="review-detail-container">
        <div className="review-detail-not-found">Video not found</div>
      </div>
    );
  }

  return (
    <div className="review-detail-container">
      <h1 className="review-detail-title">{video.videoTitle}</h1>

      <div className="review-detail-meta">
        <div className="review-detail-meta-item">
          <span className="review-detail-meta-label">Platform:</span>
          {video.platform}
        </div>
        <div className="review-detail-meta-item">
          <span className="review-detail-meta-label">Date:</span>
          {video.date}
        </div>
        {/* <div className="review-detail-meta-item">
          <span className="review-detail-meta-label">ID:</span>
          {video.id}
        </div> */}
      </div>

      <div className="review-detail-summary">
        <h2 className="review-detail-summary-title">Analysis Summary</h2>
        <div className="review-detail-analysis">
          {video.analysis && typeof video.analysis === "object" ? (
            <ul className="review-analysis-list">
              {Object.entries(video.analysis).map(([key, value]) => (
                <li key={key} className="review-analysis-item">
                  <span className="review-analysis-key">
                    {key
                      .replace(/_/g, " ")
                      .replace(/\b\w/g, (c) => c.toUpperCase())}
                    :
                  </span>
                  <span className="review-analysis-value">
                    {value === null || value === undefined
                      ? "—"
                      : typeof value === "number"
                      ? String(value)
                      : String(value)}
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p>Brak analizy do wyświetlenia.</p>
          )}
        </div>
      </div>
    </div>
  );
}
