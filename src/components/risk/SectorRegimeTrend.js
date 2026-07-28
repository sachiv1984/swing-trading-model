import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/base44Client";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const DEFAULT_TREND_WEEKS = 12;
const SECTOR_COLOURS = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"];
const OTHER_COLOUR = "#64748b";

function colourForSector(index, name) {
  if (name === "Other") return OTHER_COLOUR;
  return SECTOR_COLOURS[index % SECTOR_COLOURS.length];
}

function reshapeWeeksForChart(weeks) {
  return weeks.map((w) => {
    const row = { week_start: w.week_start };
    for (const s of w.sectors) {
      row[s.sector_name] = s.exposure_pct;
    }
    return row;
  });
}

function SectorTrendTooltip({ active, payload, label }) {
  if (!active || !payload || payload.length === 0) return null;
  return (
    <div className="rounded-xl bg-slate-800 border border-slate-700 px-4 py-3 shadow-xl text-sm">
      <p className="font-semibold text-white mb-1">{label}</p>
      {payload.map((p) => (
        <p key={p.dataKey} className="text-slate-300">
          {p.dataKey}: <span className="font-medium text-white">{p.value.toFixed(1)}%</span>
        </p>
      ))}
    </div>
  );
}

function RegimeRow({ label, weeks, field }) {
  return (
    <div className="flex items-center gap-2" data-testid={`regime-row-${field}`}>
      <span className="text-xs text-slate-600 dark:text-slate-400 w-8 shrink-0">{label}</span>
      <div className="flex gap-0.5 flex-1">
        {weeks.map((w) => (
          <div
            key={w.week_start}
            className={`h-4 flex-1 rounded-sm ${w[field] ? "bg-emerald-500/70" : "bg-amber-500/70"}`}
            title={`${w.week_start}: ${label} ${w[field] ? "risk-on" : "risk-off"}`}
            aria-label={`${label} regime ${w[field] ? "risk-on" : "risk-off"} for week of ${w.week_start}`}
          />
        ))}
      </div>
    </div>
  );
}

function RegimeTrendStrip({ weeks }) {
  return (
    <div className="flex flex-col gap-1.5 mt-4">
      <RegimeRow label="US" weeks={weeks} field="regime_us" />
      <RegimeRow label="UK" weeks={weeks} field="regime_uk" />
    </div>
  );
}

function CardShell({ children }) {
  return (
    <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
      <h3 className="text-sm font-medium text-slate-300 mb-3">Sector &amp; Regime Exposure Trend</h3>
      {children}
    </div>
  );
}

function SectorTrendChart({ weeks }) {
  const chartData = reshapeWeeksForChart(weeks);
  const sectorNames = weeks.length > 0 ? weeks[weeks.length - 1].sectors.map((s) => s.sector_name) : [];

  return (
    <ResponsiveContainer width="100%" height={220}>
      <AreaChart data={chartData} margin={{ top: 8, right: 8, left: 0, bottom: 4 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
        <XAxis
          dataKey="week_start"
          tick={{ fill: "#94a3b8", fontSize: 11 }}
          axisLine={{ stroke: "#334155" }}
          tickLine={false}
        />
        <YAxis
          tickFormatter={(v) => `${v}%`}
          tick={{ fill: "#94a3b8", fontSize: 12 }}
          axisLine={false}
          tickLine={false}
          width={44}
        />
        <Tooltip content={<SectorTrendTooltip />} />
        <Legend wrapperStyle={{ fontSize: 12, color: "#94a3b8" }} />
        {sectorNames.map((name, i) => (
          <Area
            key={name}
            type="monotone"
            dataKey={name}
            stackId="sectors"
            stroke={colourForSector(i, name)}
            fill={colourForSector(i, name)}
            fillOpacity={0.5}
          />
        ))}
      </AreaChart>
    </ResponsiveContainer>
  );
}

export default function SectorRegimeTrend() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["sector-regime-trend"],
    queryFn: () => api.portfolio.sectorRegimeTrend(DEFAULT_TREND_WEEKS),
    staleTime: 60_000,
  });

  if (isLoading) {
    return (
      <CardShell>
        <div className="h-48 rounded-lg bg-slate-800 animate-pulse" />
      </CardShell>
    );
  }

  if (isError) {
    return (
      <CardShell>
        <p className="text-sm text-slate-600 dark:text-slate-400">Unable to load exposure trend.</p>
      </CardShell>
    );
  }

  if (data?.insufficient_history) {
    const weeksAvailable = data?.weeks_available ?? 0;
    return (
      <CardShell>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Not enough history yet to show a trend (8 weeks of data required; {weeksAvailable} available).
        </p>
      </CardShell>
    );
  }

  const weeks = data?.weeks ?? [];
  return (
    <CardShell>
      <SectorTrendChart weeks={weeks} />
      <RegimeTrendStrip weeks={weeks} />
    </CardShell>
  );
}
