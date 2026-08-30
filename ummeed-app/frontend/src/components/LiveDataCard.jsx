export function LiveDataCard({ label, value }) {
  return (
    <div className="live-card">
      <span className="live-card-tag">Right now</span>
      <span className="live-card-label">{label}</span>
      <span className="live-card-value">{value}</span>
    </div>
  );
}
