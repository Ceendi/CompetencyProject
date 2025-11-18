import { useParams } from "react-router-dom";
import videos from "../../data/videos.json";
import "./ReviewDetailPage.css";

export function ReviewDetailPage() {
  const { id } = useParams();
  const video = videos.find((v) => v.id === id);

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
        <div className="review-detail-meta-item">
          <span className="review-detail-meta-label">ID:</span>
          {video.id}
        </div>
      </div>

      <div className="review-detail-summary">
        <h2 className="review-detail-summary-title">Analysis Summary</h2>
        <div className="review-detail-analysis">
          <p>{video.analysis}</p>
        </div>
      </div>
    </div>
  );
}
