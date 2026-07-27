import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// AiSpendTrendChart — ST-06 (EPIC-06, v7.8, BLG-FEAT-82)
// Source: GET /ai/spend-trend. Extends the existing Claude API Usage &
// Costs card (settings.md §6) below the current-month figure.
// Follows the same bar-chart pattern as analytics.md §12 Win Rate by Month
// (fixed-axis, no zoom/pan) but with an auto-scaled Y-axis (no fixed
// ceiling — spend has no natural upper bound, unlike win rate's 0-100%)
// and no reference line (spend has no natural break-even/target value).
//
// Single fixed accent colour (blue-500), not theme-conditional: no existing
// chart component in this codebase switches bar colour by light/dark theme
// (WinRateByMonth.js, PnLBarChart.js etc. all use fixed hex values), and
// this chart's card shell is itself fixed-dark like its siblings — so a
// single colour is consistent with established convention.
const BAR_COLOUR = "#3b82f6"; // blue-500

function SpendTrendTooltip({ active, payload, label }) {
  if (!active || !payload || payload.length === 0) return null;
  const d = payload[0].payload;
  return (
    <div className="rounded-xl bg-slate-800 border border-slate-700 px-4 py-3 shadow-xl text-sm">
      <p className="font-semibold text-white mb-1">{label}</p>
      <p className="text-slate-300">
        Spend: <span className="font-medium text-white">${d.spend_usd.toFixed(2)}</span>
      </p>
    </div>
  );
}

export default function AiSpendTrendChart({ data = [] }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="mt-4" data-testid="ai-spend-trend-chart">
      <p className="text-xs text-slate-600 dark:text-slate-400 mb-2">Spend by release cycle</p>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart
          data={data}
          margin={{ top: 8, right: 8, left: 0, bottom: 4 }}
          barCategoryGap="30%"
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />

          <XAxis
            dataKey="version"
            tick={{ fill: "#94a3b8", fontSize: 12 }}
            axisLine={{ stroke: "#334155" }}
            tickLine={false}
          />

          <YAxis
            tickFormatter={(v) => `$${v}`}
            tick={{ fill: "#94a3b8", fontSize: 12 }}
            axisLine={false}
            tickLine={false}
            width={48}
          />

          <Tooltip content={<SpendTrendTooltip />} cursor={{ fill: "rgba(255,255,255,0.04)" }} />

          <Bar dataKey="spend_usd" fill={BAR_COLOUR} radius={[4, 4, 0, 0]} maxBarSize={48} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
