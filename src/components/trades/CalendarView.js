import { useState, useEffect, useCallback } from "react";
import { DayPicker } from "react-day-picker";
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon } from "lucide-react";
import { cn } from "../../lib/utils";
import { apiFetch } from "../../api/base44Client";
import DataState from "../ui/DataState";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function formatGbp(value) {
  const sign = value >= 0 ? "+" : "−";
  return `${sign}£${Math.abs(value).toFixed(2)}`;
}

function makeDayButton(dailyPnlByDay, onDaySelect) {
  function CalendarDayButton({ day, modifiers, className, children, ...buttonProps }) {
    const dayNum = day.date.getDate();
    const entry = !day.outside ? dailyPnlByDay[dayNum] : null;
    const hasExits = entry && entry.trade_count > 0;
    const isPositive = hasExits && entry.realised_pnl_gbp >= 0;

    const title = hasExits
      ? `${formatGbp(entry.realised_pnl_gbp)} (${entry.trade_count} trade${entry.trade_count === 1 ? "" : "s"})`
      : undefined;

    return (
      <button
        {...buttonProps}
        title={title}
        disabled={!hasExits}
        onClick={hasExits ? () => onDaySelect(day.date) : undefined}
        className={cn(
          className,
          "relative h-9 w-9 p-0 font-normal rounded-md text-sm",
          day.outside ? "text-slate-700" : "text-slate-300",
          hasExits ? "cursor-pointer hover:bg-slate-700/60" : "cursor-default"
        )}
      >
        {children}
        {hasExits && (
          <span
            className={cn(
              "absolute bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 rounded-full",
              isPositive ? "bg-emerald-400" : "bg-rose-400"
            )}
          />
        )}
      </button>
    );
  }
  return CalendarDayButton;
}

export default function CalendarView({ hasAnyClosedTrades, onDaySelect }) {
  const [month, setMonth] = useState(() => new Date());
  const [dailyPnl, setDailyPnl] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [estimatedUnrealisedPnl, setEstimatedUnrealisedPnl] = useState(null);

  const fetchMonth = useCallback(async (d) => {
    setLoading(true);
    setLoadError(false);
    try {
      const year = d.getFullYear();
      const monthNum = d.getMonth() + 1;
      const res = await apiFetch(`${API_BASE_URL}/reports/daily-pnl?year=${year}&month=${monthNum}`);
      if (!res.ok) throw new Error();
      const json = await res.json();
      setDailyPnl(Array.isArray(json.data) ? json.data : []);
      setEstimatedUnrealisedPnl(json.estimated_unrealised_pnl);
    } catch {
      setLoadError(true);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchMonth(month); }, [month, fetchMonth]);

  if (!hasAnyClosedTrades) {
    return (
      <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6">
        <DataState
          loading={false}
          error={false}
          empty
          emptyIcon={<CalendarIcon className="w-10 h-10 text-slate-600" />}
          emptyHeading="No closed trades yet"
          emptyBody="Your trading calendar will populate as you close trades."
        />
      </div>
    );
  }

  const dailyPnlByDay = Object.fromEntries(dailyPnl.map((d) => [d.day, d]));

  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 space-y-4">
      <div className="rounded-lg bg-slate-900/50 border border-slate-700/30 px-4 py-2 text-sm text-slate-300">
        Unrealised P&L (as of today): {estimatedUnrealisedPnl != null ? formatGbp(estimatedUnrealisedPnl) : "—"}
      </div>

      {loadError ? (
        <p className="text-rose-400 text-sm">Unable to load calendar data. Please refresh.</p>
      ) : (
        <DayPicker
          month={month}
          onMonthChange={setMonth}
          // No selection mode is used (read-only calendar) — but DayPicker only
          // renders the custom DayButton component (below) when interactive
          // (mode or onDayClick set); a no-op here forces that without adding
          // a selection state. Actual click handling lives in CalendarDayButton.
          onDayClick={() => {}}
          showOutsideDays
          className="p-0"
          classNames={{
            months: "flex flex-col",
            month_caption: "flex justify-center items-center py-2 text-sm font-medium text-white",
            nav: "flex items-center justify-between absolute inset-x-0 top-0 px-2",
            weekdays: "flex",
            weekday: "text-slate-600 dark:text-slate-400 w-9 font-normal text-xs text-center",
            week: "flex w-full mt-1",
            month_grid: "w-full border-collapse",
          }}
          components={{
            Chevron: ({ orientation }) =>
              orientation === "left" ? (
                <ChevronLeft className="h-4 w-4 text-slate-400" />
              ) : (
                <ChevronRight className="h-4 w-4 text-slate-400" />
              ),
            DayButton: makeDayButton(dailyPnlByDay, onDaySelect),
          }}
        />
      )}

      {loading && <p className="text-xs text-slate-600 dark:text-slate-400">Loading…</p>}
    </div>
  );
}
