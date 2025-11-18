import { motion, AnimatePresence } from "framer-motion";
import TableRow from "../TableRow/TableRow";

export default function AnimatedTable({ videos, handleViewSummary, maxItems }) {
  const displayedVideos = maxItems ? videos.slice(0, maxItems) : videos;

  return (
    <div className="dashboard-table-container">
      <table className="dashboard-table">
        <thead>
          <tr className="dashboard-table-header">
            <th className="dashboard-th dashboard-th-video">Video Title</th>
            <th className="dashboard-th dashboard-th-platform">Platform</th>
            <th className="dashboard-th dashboard-th-date">Date</th>
            <th className="dashboard-th dashboard-th-summary">
              Sentiment Summary
            </th>
          </tr>
        </thead>
        <tbody>
          <AnimatePresence>
            {displayedVideos.map((video) => (
              <TableRow
                key={video.id}
                video={video}
                handleViewSummary={handleViewSummary}
              />
            ))}
          </AnimatePresence>
        </tbody>
      </table>
    </div>
  );
}
