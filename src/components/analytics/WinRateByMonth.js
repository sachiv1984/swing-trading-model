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
} from "recharts";

// WinRateByMonth - Component 12 (BLG-FEAT-05)
// Source: monthly_data from GET /analytics/metrics
// Fields: winRate, tradeCount (camelCase - toCamelCase applied by PerformanceAnalytics)
// Y-axis: fixed 0-100%. Reference line at 50%. Returns null when empty.

const BAR_ABOVE = "#34d399";
const BAR_BELOW = "#fb7185";

function barColour(winRate) {
  return winRate > 50 ? BAR_ABOVE : BAR_BELOW;
}

function formatMonth(monthStr) {
  if (!monthStr) return "";
  try {
    const [year, month] = monthStr.split("-");
    const d = new Date(Number(year), Number(month) - 1, 1);
    return d.toLocaleString("en-GB", { month: "short" }) + " " + String(year).slice(2);
  } catch {
    return monthStr;
  }
}

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
        {d.tradeCount} trade{d.tradeCount !== 1 ? "s" : ""}
      </p>
    </div>
  );
}

export default function WinRateByMonth({ monthlyData = [] }) {
  if (!monthlyData || monthlyData.length === 0) return null;

  const chartData = monthlyData.map((d) => ({
    ...d,
    label: formatMonth(d.month),
    winRate: Math.max(0, Math.min(100, d.winRate ?? 0)),
  }));

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white">Win Rate by Month</h3>
        <p className="text-sm text-slate-400 mt-1">
          Monthly win rate with 50% break-even reference
        </p>
      </div>

      <ResponsiveContainer width="100%" height={260}>
        <BarChart
          data={chartData}
          margin={{ top: 8, right: 16, left: 0, bottom: 4 }}
          barCategoryGap="30%"
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />

          <XAxis
            dataKey="label"
            tick={{ fill: "#94a3b8", fontSize: 12 }}
            axisLine={{ stroke: "#334155" }}
            tickLine={false}
          />

          <YAxis
            domain={[0, 100]}
            tickFormatter={(v) => `${v}%`}
            tick={{ fill: "#94a3b8", fontSize: 12 }}
            axisLine={false}
            tickLine={false}
            width={42}
          />

          <Tooltip content={<WinRateTooltip />} cursor={{ fill: "rgba(255,255,255,0.04)" }} />

          <ReferenceLine y={50} stroke="#64748b" strokeDasharray="4 4" strokeWidth={1.5} />

          <Bar dataKey="winRate" radius={[4, 4, 0, 0]} maxBarSize={48}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={barColour(entry.winRate)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
