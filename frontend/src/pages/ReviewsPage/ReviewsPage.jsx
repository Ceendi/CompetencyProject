import { useNavigate } from "react-router-dom";
import { useVideos } from "../../hooks/useVideos";
import AnimatedTable from "../../components/AnimatedTable/AnimatedTable";

export default function ReviewsPage() {
  const { videos } = useVideos();
  const navigate = useNavigate();

  function handleViewSummary(videoId) {
    navigate(`/reviews/${videoId}`);
  }

  return (
    <div>
      <h2>All Analyses</h2>
      <AnimatedTable videos={videos} handleViewSummary={handleViewSummary} />
    </div>
  );
}
