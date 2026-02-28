import {
BarChart,
Bar,
XAxis,
YAxis,
CartesianGrid,
Tooltip,
ReferenceLine,
ResponsiveContainer,
Cell,
} from recharts;

// ─────────────────────────────────────────────────────────────────────────────
// WinRateByMonth — Component 12 (BLG-FEAT-05)
// Spec: analytics.md v1.2 §Win Rate by Month
//
// Source: monthly_data from GET /analytics/metrics
// Fields consumed: monthly_data[].month, monthly_data[].winRate, monthly_data[].tradeCount
//
// Y-axis: fixed 0–100%, does not auto-scale.
// Reference line: 50% (muted dashed, orientation only — no interactive label).
// Colour coding: bar above 50% → emerald (profit); at or below 50% → rose (loss).
//   Each bar is a single colour, no gradient.
// Tooltip: month label + win rate % + tradeCount.
//   Field is tradeCount (camelCase after toCamelCase conversion in PerformanceAnalytics).
// Empty state: does not render at all when monthly_data is empty (no empty message).
//   The page-level has_enough_data guard is the primary gate; this guard is redundant
//   safety that prevents any render when the array is empty.
// ─────────────────────────────────────────────────────────────────────────────

// ─── Colour helpers ───────────────────────────────────────────────────────────
// Binary profit/loss colouring per design_system.md.
// Above 50% = emerald; at or below 50% = rose.
const BAR_ABOVE = “#34d399”; // emerald-400
const BAR_BELOW = “#fb7185”; // rose-400

function barColour(winRate) {
return winRate > 50 ? BAR_ABOVE : BAR_BELOW;
}

// ─── Month label formatter ────────────────────────────────────────────────────
// monthly_data[].month comes in as “YYYY-MM” from the API.
// Display as “Jan 26”, “Feb 26”, etc.
function formatMonth(monthStr) {
if (!monthStr) return “”;
try {
// “2026-01” → Date object → short month + 2-digit year
const [year, month] = monthStr.split(”-”);
const d = new Date(Number(year), Number(month) - 1, 1);
return d.toLocaleString(“en-GB”, { month: “short” }) + “ “ + String(year).slice(2);
} catch {
return monthStr;
}
}

// ─── Custom tooltip ───────────────────────────────────────────────────────────
function WinRateTooltip({ active, payload, label }) {
if (!active || !payload || payload.length === 0) return null;
const d = payload[0].payload;
return (
<div className="rounded-xl bg-slate-800 border border-slate-700 px-4 py-3 shadow-xl text-sm">
<p className="font-semibold text-white mb-1">{label}</p>
<p className="text-slate-300">
Win rate: <span className="font-medium text-white">{d.winRate.toFixed(1)}%</span>
</p>
<p className="text-slate-400 text-xs mt-0.5">
{d.tradeCount} trade{d.tradeCount !== 1 ? “s” : “”}
</p>
</div>
);
}

// ─────────────────────────────────────────────────────────────────────────────

/**

- WinRateByMonth
- 
- @param {object[]} monthlyData — analyticsData.monthlyData
- Each entry: { month: “YYYY-MM”, winRate: number, tradeCount: number, … }
- 
- Returns null (renders nothing) when monthlyData is empty.
- The calling page should only render this component inside the has_enough_data guard,
- but this component is also safe to call unconditionally.
  */
  export default function WinRateByMonth({ monthlyData = [] }) {
  // Spec: component does not render when monthly_data is empty (F-27).
  if (!monthlyData || monthlyData.length === 0) return null;

// Map API shape → chart shape, adding formatted label
const chartData = monthlyData.map((d) => ({
…d,
label: formatMonth(d.month),
// Clamp to valid range for display safety
winRate: Math.max(0, Math.min(100, d.winRate ?? 0)),
}));

return (
<div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
{/* Header */}
<div className="mb-6">
<h3 className="text-lg font-semibold text-white">Win Rate by Month</h3>
<p className="text-sm text-slate-400 mt-1">Monthly win rate with 50% break-even reference</p>
</div>

```
  {/* Chart */}
  <ResponsiveContainer width="100%" height={260}>
    <BarChart
      data={chartData}
      margin={{ top: 8, right: 16, left: 0, bottom: 4 }}
      barCategoryGap="30%"
    >
      <CartesianGrid
        strokeDasharray="3 3"
        stroke="#334155"
        vertical={false}
      />

      <XAxis
        dataKey="label"
        tick={{ fill: "#94a3b8", fontSize: 12 }}
        axisLine={{ stroke: "#334155" }}
        tickLine={false}
      />

      {/* Fixed 0–100 scale — spec requirement (F-25) */}
      <YAxis
        domain={[0, 100]}
        tickFormatter={(v) => `${v}%`}
        tick={{ fill: "#94a3b8", fontSize: 12 }}
        axisLine={false}
        tickLine={false}
        width={42}
      />

      <Tooltip content={<WinRateTooltip />} cursor={{ fill: "rgba(255,255,255,0.04)" }} />

      {/* 50% reference line — spec requirement (F-24).
          Muted dashed line. No label (orientation only). */}
      <ReferenceLine
        y={50}
        stroke="#64748b"
        strokeDasharray="4 4"
        strokeWidth={1.5}
      />

      {/* Colour-coded bars — one Cell per bar (F-25) */}
      <Bar dataKey="winRate" radius={[4, 4, 0, 0]} maxBarSize={48}>
        {chartData.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={barColour(entry.winRate)} />
        ))}
      </Bar>
    </BarChart>
  </ResponsiveContainer>
</div>
```

);
}
