import { useParams } from "react-router-dom";
import "./ReviewDetailPage.css";
import { useVideos } from "../../hooks/useVideos";

import { Chart as ChartJS, ArcElement } from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement);

const formatLabel = (label) =>
  label.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

const generateGradientChartData = () => {
  const segments = 50;
  const dataArray = new Array(segments).fill(1);
  const colorsArray = [];
  for (let i = 0; i < segments; i++) {
    const hue = (i / (segments - 1)) * 120;
    colorsArray.push(`hsl(${hue}, 100%, 50%)`);
  }
  return { dataArray, colorsArray };
};

const { dataArray: gradientData, colorsArray: gradientColors } =
  generateGradientChartData();

const needlePlugin = {
  id: "needlePlugin",
  afterDatasetDraw(chart, args, plugins) {
    const { ctx } = chart;
    const sentimentValue = plugins.value ?? 0;
    const normalizedValue = (Math.max(-1, Math.min(1, sentimentValue)) + 1) / 2;

    const meta = chart.getDatasetMeta(0).data[0];
    const needleLength = 0.65 * meta.outerRadius - 5;
    const angle = Math.PI + Math.PI * normalizedValue;

    ctx.save();
    ctx.translate(meta.x, meta.y);
    ctx.rotate(angle);

    ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
    ctx.shadowBlur = 6;
    ctx.shadowOffsetX = 2;
    ctx.shadowOffsetY = 2;

    ctx.beginPath();
    ctx.moveTo(0, -5);
    ctx.lineTo(needleLength, 0);
    ctx.lineTo(0, 5);
    ctx.fillStyle = "#ffffff";
    ctx.fill();

    ctx.beginPath();
    ctx.arc(0, 0, 6, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    ctx.restore();
  },
};

const SentimentGauge = ({ label, value, isLarge = false }) => {
  const data = {
    datasets: [
      {
        data: gradientData,
        backgroundColor: gradientColors,
        borderWidth: 0,
        cutout: "60%",
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    rotation: -90,
    circumference: 180,
    events: [],
    layout: { padding: 0 },
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
      needlePlugin: { value: value },
    },
  };

  return (
    <div className={`gauge-item ${isLarge ? "gauge-item-large" : ""}`}>
      <h3 className="gauge-title">{formatLabel(label)}</h3>
      <div className="gauge-content">
        <div className="gauge-chart-wrapper">
          <Doughnut data={data} options={options} plugins={[needlePlugin]} />
        </div>
        <div className="gauge-value-text">{value.toFixed(2)}</div>
      </div>
    </div>
  );
};

const NoDataGauge = ({ label }) => (
  <div className="gauge-item gauge-item-empty">
    <h3 className="gauge-title">{formatLabel(label)}</h3>
    <div className="gauge-no-data-content">
      <span className="no-data-text">No Data Provided</span>
    </div>
  </div>
);

export function ReviewDetailPage() {
  const { id } = useParams();
  const { videos } = useVideos();

  const video = videos.find((v) => String(v.id) === id);

  if (!video) {
    return (
      <div className="review-detail-container">
        <div className="review-detail-not-found">Video not found</div>
      </div>
    );
  }

  const analysisEntries = video.analysis
    ? Object.entries(video.analysis).slice(0, 10)
    : [];

  const validScores = analysisEntries
    .map(([, val]) => val)
    .filter((val) => typeof val === "number");

  const overallScore =
    validScores.length > 0
      ? validScores.reduce((acc, curr) => acc + curr, 0) / validScores.length
      : null;

  return (
    <div className="review-detail-container">
      <h1 className="review-detail-title">{video.title}</h1>

      <div className="review-detail-meta">
        <div className="review-detail-meta-item">
          <span className="review-detail-meta-label">Platform:</span>
          {video.platform}
        </div>
        <div className="review-detail-meta-item">
          <span className="review-detail-meta-label">Date:</span>
          {video.date || "—"}
        </div>
      </div>

      <div className="review-detail-summary">
        {overallScore !== null && (
          <div className="review-hero-section">
            <h2 className="section-title center-text">Overall Score</h2>
            <hr className="hero-divider" />
            <div className="hero-gauge-wrapper">
              <SentimentGauge
                label="Average Sentiment Score"
                value={overallScore}
                isLarge={true}
              />
            </div>
          </div>
        )}

        <h2 className="section-title">Detailed Analysis</h2>
        {analysisEntries.length > 0 ? (
          <div className="review-gauges-grid">
            {analysisEntries.map(([key, value]) =>
              typeof value === "number" ? (
                <SentimentGauge key={key} label={key} value={value} />
              ) : (
                <NoDataGauge key={key} label={key} />
              )
            )}
          </div>
        ) : (
          <p>Brak analizy do wyświetlenia.</p>
        )}

        <div className="review-transcription-section">
          <h2 className="section-title">Video Transcription</h2>
          <div className="transcription-box">
            {video.transcribed_text ||
              "No transcription available for this video."}
          </div>
        </div>
      </div>
    </div>
  );
}
