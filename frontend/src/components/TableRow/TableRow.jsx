import { useIsPresent } from "framer-motion";
import { motion } from "framer-motion";
import "./TableRow.css";

export default function TableRow({ video, handleViewSummary }) {
  let isPresent = useIsPresent();

  return (
    <motion.tr
      className="dashboard-table-row"
      layout
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
      style={{ position: isPresent ? "relative" : "absolute" }}
    >
      <td className="dashboard-td dashboard-td-video">{video.title}</td>
      <td className="dashboard-td dashboard-td-platform">{video.platform}</td>
      <td className="dashboard-td dashboard-td-date">{video.date}</td>
      <td
        className="dashboard-td dashboard-td-summary"
        onClick={() => handleViewSummary(video.id)}
      >
        View Summary
      </td>
    </motion.tr>
  );
}
