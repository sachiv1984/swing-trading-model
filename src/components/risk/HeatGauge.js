export default function HeatGauge({ heatPercent }) {
  const value = heatPercent ?? 0;

  const getColor = (v) => {
    if (v >= 30) return "#ef4444";
    if (v >= 20) return "#f97316";
    if (v >= 10) return "#f59e0b";
    return "#22c55e";
  };

  const color = getColor(value);
  const clampedValue = Math.min(value, 100);

  // Arc gauge: semi-circle (180 deg)
  const r = 70;
  const cx = 100;
  const cy = 100;
  const startAngle = -180;
  const endAngle = 0;
  const totalAngle = 180;
  const sweepAngle = (clampedValue / 100) * totalAngle;

  const toRad = (deg) => (deg * Math.PI) / 180;
  const startX = cx + r * Math.cos(toRad(startAngle));
  const startY = cy + r * Math.sin(toRad(startAngle));
  const endX = cx + r * Math.cos(toRad(startAngle + sweepAngle));
  const endY = cy + r * Math.sin(toRad(startAngle + sweepAngle));
  const largeArc = sweepAngle > 180 ? 1 : 0;

  // Background arc full
  const bgEndX = cx + r * Math.cos(toRad(0));
  const bgEndY = cy + r * Math.sin(toRad(0));

  return (
    <div className="flex flex-col items-center">
      <svg viewBox="20 25 160 90" className="w-56 h-28">
        {/* Background track */}
        <path
          d={`M ${cx - r} ${cy} A ${r} ${r} 0 0 1 ${cx + r} ${cy}`}
          fill="none"
          stroke="#1e293b"
          strokeWidth="14"
          strokeLinecap="round"
        />
        {/* Filled arc */}
        {clampedValue > 0 && (
          <path
            d={`M ${startX} ${startY} A ${r} ${r} 0 ${largeArc} 1 ${endX} ${endY}`}
            fill="none"
            stroke={color}
            strokeWidth="14"
            strokeLinecap="round"
            style={{ transition: "stroke 0.4s ease" }}
          />
        )}
        {/* Centre text */}
        <text
          x={cx}
          y={cy + 4}
          textAnchor="middle"
          fontSize="22"
          fontWeight="bold"
          fill={color}
          style={{ transition: "fill 0.4s ease" }}
        >
          {value.toFixed(1)}%
        </text>
        <text x={cx} y={cy + 18} textAnchor="middle" fontSize="9" fill="#64748b">
          Portfolio Heat
        </text>
      </svg>
      {/* Threshold labels */}
      <div className="flex gap-4 text-xs mt-1">
        {[
          { label: "Low", range: "< 10%", color: "#22c55e" },
          { label: "Mod", range: "10–20%", color: "#f59e0b" },
          { label: "High", range: "20–30%", color: "#f97316" },
          { label: "Max", range: "≥ 30%", color: "#ef4444" },
        ].map((t) => (
          <div key={t.label} className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full" style={{ background: t.color }} />
            <span className="text-slate-400">{t.range}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
