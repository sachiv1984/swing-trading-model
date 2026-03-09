import { AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "../ui/button";

function ErrorCard({ onRetry }) {
  return (
    <div className="rounded-2xl bg-rose-900/20 border border-rose-500/40 p-6 flex flex-col items-center gap-4 w-full">
      <div className="flex items-center gap-3">
        <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
        <p className="text-sm text-rose-300">Unable to load heat data</p>
      </div>
      {onRetry && (
        <Button
          variant="outline"
          size="sm"
          onClick={onRetry}
          className="border-rose-500/40 text-rose-300 hover:bg-rose-500/10 hover:text-rose-200 gap-2"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Retry
        </Button>
      )}
    </div>
  );
}

export default function HeatGauge({ heatPercent, positionRisks = [], error, onRetry }) {
  const totalAtRisk = (positionRisks ?? []).reduce((sum, p) => sum + (p.position_risk_gbp ?? 0), 0);

  const getColor = (v) => {
    if (v >= 30) return "#ef4444";
    if (v >= 20) return "#f97316";
    if (v >= 10) return "#f59e0b";
    return "#22c55e";
  };

  const value = heatPercent ?? 0;
  const color = getColor(value);
  const clampedValue = Math.min(value, 100);

  // Arc gauge: semi-circle (180 deg)
  const r = 70;
  const cx = 100;
  const cy = 100;
  const startAngle = -180;
  const sweepAngle = (clampedValue / 100) * 180;

  const toRad = (deg) => (deg * Math.PI) / 180;
  const startX = cx + r * Math.cos(toRad(startAngle));
  const startY = cy + r * Math.sin(toRad(startAngle));
  const endX = cx + r * Math.cos(toRad(startAngle + sweepAngle));
  const endY = cy + r * Math.sin(toRad(startAngle + sweepAngle));
  const largeArc = sweepAngle > 180 ? 1 : 0;

  return (
    <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6 flex flex-col items-center justify-center">
      {error ? (
        <ErrorCard onRetry={onRetry} />
      ) : (
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
            <text x={cx} y={cy + 30} textAnchor="middle" fontSize="8" fill="#475569">
              {`£${totalAtRisk.toFixed(2)} at risk`}
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
      )}
    </div>
  );
}
