// WinRateByMonth.js
// DEF-QWB-F-25 FIX — 2026-02-25
//
// Root cause: PerformanceAnalytics.js applies toCamelCase() to the entire
// analytics API response before passing data to components. This means:
//   monthly_data[].win_rate   → winRate
//   monthly_data[].trade_count → tradeCount
//   monthly_data[].month       → month  (unchanged — no underscore)
//
// The original implementation used snake_case field names (win_rate,
// trade_count) as the Recharts dataKey and in the custom tooltip.
// Both resolved to undefined, producing zero-height invisible bars.
//
// This fix: all field references use camelCase throughout.
//
// Spec authority: analytics.md v1.2 §Win Rate by Month
// Canonical formula: bar colour = winRate > 50 ? green : red (exactly 50 = red)
// Tooltip: month label, win rate %, tradeCount
// Y-axis: fixed 0–100, no auto-scaling
// Reference line: 50%, dashed, muted
// Empty guard: returns null when monthlyData is empty

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
import { BarChart2 } from "lucide-react";

// Format "2026-02" → "Feb 26"
const formatMonthLabel = (monthStr) => {
  if (!monthStr) return "";
  const [year, month] = monthStr.split("-");
  const date = new Date(parseInt(year), parseInt(month) - 1, 1);
  return date.toLocaleDateString("en-GB", { month: "short", year: "2-digit" });
};

// Custom tooltip
// Uses camelCase (winRate, tradeCount) — matching toCamelCase output
const WinRateTooltip = ({ active, payload }) => {
  if (!active || !payload || !payload.length) return null;

  const data = payload[0]?.payload;
  if (!data) return null;

  const winRate = data.winRate ?? 0;
  const tradeCount = data.tradeCount ?? 0;
  const monthLabel = formatMonthLabel(data.month);

  return (
    <div className="bg-slate-900 border border-slate-700 rounded-lg p-3 text-xs shadow-xl">
      <p className="font-semibold text-white mb-1">{monthLabel}</p>
      <p className="text-slate-300">
        Win rate:{" "}
        <span className={winRate > 50 ? "text-emerald-400" : "text-rose-400"}>
          {winRate.toFixed(1)}%
        </span>
      </p>
      <p className="text-slate-400">
        {tradeCount} trade{tradeCount !== 1 ? "s" : ""}
      </p>
    </div>
  );
};

export default function WinRateByMonth({ monthlyData = [] }) {
  // Empty guard — component must not render when monthlyData is empty
  // Spec: analytics.md v1.2 §empty state
  if (!monthlyData || monthlyData.length === 0) return null;

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600">
          <BarChart2 className="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-white">Win Rate by Month</h3>
          <p className="text-sm text-slate-400">Monthly win rate vs 50% break-even</p>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={260}>
        <BarChart
          data={monthlyData}
          margin={{ top: 8, right: 16, left: 0, bottom: 8 }}
          barCategoryGap="40%"
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#334155"
            opacity={0.4}
            vertical={false}
          />

          <XAxis
            dataKey="month"
            tickFormatter={formatMonthLabel}
            stroke="#64748b"
            tick={{ fill: "#94a3b8", fontSize: 12 }}
            tickLine={false}
            axisLine={false}
          />

          {/* Fixed 0–100 domain — spec requirement, no auto-scaling */}
          <YAxis
            domain={[0, 100]}
            tickFormatter={(v) => `${v}%`}
            stroke="#64748b"
            tick={{ fill: "#94a3b8", fontSize: 12 }}
            tickLine={false}
            axisLine={false}
            width={42}
          />

          {/* 50% reference line — dashed, muted, no label per spec */}
          <ReferenceLine
            y={50}
            stroke="#64748b"
            strokeDasharray="4 4"
            strokeWidth={1.5}
          />

          <Tooltip
            content={<WinRateTooltip />}
            cursor={{ fill: "rgba(148, 163, 184, 0.05)" }}
          />

          {/*
           * DEF-QWB-F-25 FIX:
           * dataKey="winRate"  ← camelCase (was "win_rate" — undefined after transform)
           *
           * Colour rule per analytics.md v1.2:
           *   winRate > 50  → emerald-500  (profit colour)
           *   winRate ≤ 50  → rose-500     (loss colour, boundary inclusive)
           */}
          <Bar dataKey="winRate" radius={[4, 4, 0, 0]} maxBarSize={72}>
            {monthlyData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={(entry.winRate ?? 0) > 50 ? "#10b981" : "#f43f5e"}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      {/* Trade count summary row beneath chart */}
      <div
        className="mt-3 grid text-center"
        style={{ gridTemplateColumns: `repeat(${monthlyData.length}, 1fr)` }}
      >
        {monthlyData.map((entry, idx) => (
          <div key={idx} className="text-xs text-slate-500">
            {/*
             * DEF-QWB-F-25 FIX:
             * entry.tradeCount  ← camelCase (was "trade_count" — undefined after transform)
             */}
            {entry.tradeCount ?? 0} trade{(entry.tradeCount ?? 0) !== 1 ? "s" : ""}
          </div>
        ))}
      </div>
    </div>
  );
}
