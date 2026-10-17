import { useState, useCallback, useEffect } from "react";
import { apiFetch } from "../api/base44Client";
import { Button } from "../components/ui/button";
import PageHeader from "../components/ui/PageHeader";
import { Skeleton } from "../components/ui/skeleton";
import { cn } from "../lib/utils";
import {
  AlertTriangle,
  CheckSquare,
  SkipForward,
  TrendingDown,
  ChevronLeft,
  ChevronRight,
  RefreshCw,
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const EVENT_TYPE_CONFIG = {
  pre_entry_override: {
    label: "Pre-Entry Override",
    icon: AlertTriangle,
    className: "text-amber-400",
  },
  checklist_skipped: {
    label: "Checklist Skipped",
    icon: CheckSquare,
    className: "text-sky-400",
  },
  stop_prompt_dismissed: {
    label: "Stop Prompt Dismissed",
    icon: SkipForward,
    className: "text-red-400",
  },
  drawdown_prompt_dismissed: {
    label: "Drawdown Prompt Dismissed",
    icon: TrendingDown,
    className: "text-red-500",
  },
};

// Event types that have a backend writer (red_flag_journal.md v1.4, ST-04).
// Must equal the written set checked by tests/test_red_flag_checklist_skipped.py:
// adding a writer means editing that test's allow-list and this list.
export const RECORDED_EVENT_TYPES = ["pre_entry_override", "checklist_skipped"];

const EVENT_TYPE_OPTIONS = [
  { value: "", label: "All types" },
  ...Object.entries(EVENT_TYPE_CONFIG).map(([value, { label }]) =>
    RECORDED_EVENT_TYPES.includes(value)
      ? { value, label }
      : { value, label: `${label} — not yet recorded`, disabled: true }
  ),
];

// Phrases for the recorded-types note, built from RECORDED_EVENT_TYPES.
const NOTE_PHRASES = {
  pre_entry_override: "pre-entry overrides",
  checklist_skipped: "skipped checklists",
  stop_prompt_dismissed: "stop prompt dismissals",
  drawdown_prompt_dismissed: "drawdown prompt dismissals",
};

function joinPhrases(phrases) {
  // "stop prompt dismissals" + "drawdown prompt dismissals" → "stop and drawdown prompt dismissals"
  const suffix = " prompt dismissals";
  if (phrases.length > 1 && phrases.every((p) => p.endsWith(suffix))) {
    return joinPhrases(phrases.map((p) => p.slice(0, -suffix.length))) + suffix;
  }
  if (phrases.length <= 1) return phrases.join("");
  return `${phrases.slice(0, -1).join(", ")} and ${phrases[phrases.length - 1]}`;
}

function capitalise(text) {
  return text ? text[0].toUpperCase() + text.slice(1) : text;
}

export function recordedTypesNote() {
  const types = Object.keys(EVENT_TYPE_CONFIG);
  const recorded = types.filter((t) => RECORDED_EVENT_TYPES.includes(t)).map((t) => NOTE_PHRASES[t]);
  const unrecorded = types.filter((t) => !RECORDED_EVENT_TYPES.includes(t)).map((t) => NOTE_PHRASES[t]);
  let note = `${capitalise(joinPhrases(recorded))} are recorded here.`;
  if (unrecorded.length) note += ` ${capitalise(joinPhrases(unrecorded))} are not recorded yet.`;
  return note;
}

// A stored filter naming a type with no writer resets to "All types".
function storedEventTypeFilter() {
  const stored = loadStoredFilters()?.eventTypeFilter ?? "";
  return stored && !RECORDED_EVENT_TYPES.includes(stored) ? "" : stored;
}

const FILTER_STORAGE_KEY = "redFlagJournal.filters";
const FILTER_STORAGE_VERSION = 1;

function loadStoredFilters() {
  try {
    const raw = localStorage.getItem(FILTER_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed || parsed.version !== FILTER_STORAGE_VERSION || !parsed.data) {
      localStorage.removeItem(FILTER_STORAGE_KEY);
      return null;
    }
    return parsed.data;
  } catch {
    try {
      localStorage.removeItem(FILTER_STORAGE_KEY);
    } catch {
      // ignore — localStorage unavailable (e.g. private browsing)
    }
    return null;
  }
}

function stripLSuffix(ticker) {
  if (!ticker) return ticker;
  return ticker.endsWith(".L") ? ticker.slice(0, -2) : ticker;
}

function relativeTime(isoStr) {
  if (!isoStr) return "";
  const diff = Date.now() - new Date(isoStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins} minute${mins === 1 ? "" : "s"} ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours} hour${hours === 1 ? "" : "s"} ago`;
  const days = Math.floor(hours / 24);
  return `${days} day${days === 1 ? "" : "s"} ago`;
}

function contextSummary(eventType, context) {
  if (!context) return "";
  if (typeof context === "string") return context;
  if (eventType === "checklist_skipped" && context.unchecked_items != null) {
    const n = context.unchecked_items;
    return context.total_items != null
      ? `${n} of ${context.total_items} checklist items unchecked when the plan was saved`
      : `${n} checklist item${n === 1 ? "" : "s"} unchecked`;
  }
  if (context.source && context.override_acknowledged) {
    return `Override acknowledged (${context.source})`;
  }
  const entries = Object.entries(context);
  if (entries.length === 0) return "";
  return entries
    .slice(0, 2)
    .map(([k, v]) => `${k}: ${v}`)
    .join("; ");
}

function EventRow({ event }) {
  const config = EVENT_TYPE_CONFIG[event.event_type] || {
    label: event.event_type,
    icon: AlertTriangle,
    className: "text-slate-600 dark:text-slate-400",
  };
  const Icon = config.icon;
  const displayTicker = stripLSuffix(event.ticker);
  const summary = contextSummary(event.event_type, event.context);
  const relTime = relativeTime(event.created_at);
  const absDate = event.created_at
    ? new Date(event.created_at).toLocaleString()
    : "";

  return (
    <div
      data-testid="event-row"
      className="flex items-start gap-4 px-4 py-3 border border-slate-700/50 rounded-lg bg-slate-800/40 hover:bg-slate-800/60 transition-colors"
    >
      <div className={cn("mt-0.5 shrink-0", config.className)}>
        <Icon className="w-4 h-4" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <span data-testid="event-type-label" className={cn("text-sm font-medium", config.className)}>
            {config.label}
          </span>
          <span
            data-testid="event-ticker"
            className="text-sm font-mono text-slate-300"
          >
            {displayTicker}
          </span>
        </div>
        {summary && (
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5 truncate">{summary}</p>
        )}
      </div>
      <div className="shrink-0 text-right">
        <span
          data-testid="event-date"
          className="text-xs text-slate-600 dark:text-slate-400"
          title={absDate}
        >
          {relTime}
        </span>
      </div>
    </div>
  );
}

// Canonical loading-skeleton pattern (v9.4, ST-25, BLG-FE-174): composed
// from the shared Skeleton primitive (design_system.md §Shared UI
// Components -> Data States) rather than page-local bg-*/animate-pulse
// divs. bg-slate-700 overrides preserve this row's exact pre-existing
// colour -- same override convention DataState.js already uses for its
// own skeleton (bg-slate-300/60 dark:bg-slate-700/60).
function SkeletonRow() {
  return (
    <div className="flex items-start gap-4 px-4 py-3 border border-slate-700/30 rounded-lg bg-slate-800/20">
      <Skeleton className="w-4 h-4 mt-0.5 bg-slate-700 shrink-0" />
      <div className="flex-1 space-y-2">
        <Skeleton className="h-3 w-40 bg-slate-700" />
        <Skeleton className="h-3 w-64 bg-slate-700/60" />
      </div>
      <Skeleton className="w-20 h-3 bg-slate-700" />
    </div>
  );
}

export default function RedFlagJournal() {
  const [page, setPage] = useState(1);
  const [eventTypeFilter, setEventTypeFilter] = useState(storedEventTypeFilter);
  const [tickerFilter, setTickerFilter] = useState(
    () => loadStoredFilters()?.tickerFilter ?? ""
  );
  const [sinceFilter, setSinceFilter] = useState(
    () => loadStoredFilters()?.sinceFilter ?? ""
  );
  const [tickerInput, setTickerInput] = useState(
    () => loadStoredFilters()?.tickerFilter ?? ""
  );

  const PAGE_SIZE = 20;

  useEffect(() => {
    try {
      localStorage.setItem(
        FILTER_STORAGE_KEY,
        JSON.stringify({
          version: FILTER_STORAGE_VERSION,
          data: { eventTypeFilter, tickerFilter, sinceFilter },
        })
      );
    } catch {
      // ignore — localStorage unavailable (e.g. private browsing)
    }
  }, [eventTypeFilter, tickerFilter, sinceFilter]);

  const queryKey = ["red-flag-journal", page, eventTypeFilter, tickerFilter, sinceFilter];

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey,
    queryFn: async () => {
      const params = new URLSearchParams({ page, page_size: PAGE_SIZE });
      if (eventTypeFilter) params.set("event_type", eventTypeFilter);
      if (tickerFilter) params.set("ticker", tickerFilter);
      if (sinceFilter) params.set("since", sinceFilter);
      const res = await apiFetch(`${API_BASE}/portfolio/red-flag-journal?${params}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const body = await res.json();
      return body.data;
    },
    keepPreviousData: true,
  });

  const hasFilters = eventTypeFilter || tickerFilter || sinceFilter;

  const clearFilters = useCallback(() => {
    setEventTypeFilter("");
    setTickerFilter("");
    setTickerInput("");
    setSinceFilter("");
    setPage(1);
  }, []);

  const applyTickerFilter = useCallback(() => {
    setTickerFilter(tickerInput.trim().toUpperCase() || "");
    setPage(1);
  }, [tickerInput]);

  const handleEventTypeChange = useCallback((e) => {
    setEventTypeFilter(e.target.value);
    setPage(1);
  }, []);

  const handleSinceChange = useCallback((e) => {
    setSinceFilter(e.target.value);
    setPage(1);
  }, []);

  const total = data?.total ?? 0;
  const items = data?.items ?? [];
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <PageHeader title="Red Flag Journal" />

      {/* Filter controls */}
      <div
        data-testid="filter-controls"
        className="flex flex-wrap gap-3 items-end"
      >
        <div className="flex flex-col gap-1">
          <label className="text-xs text-slate-600 dark:text-slate-400">Event type</label>
          <select
            data-testid="event-type-filter"
            value={eventTypeFilter}
            onChange={handleEventTypeChange}
            className="bg-slate-800 border border-slate-600 text-slate-200 text-sm rounded px-2 py-1.5 focus:outline-none focus:border-slate-400"
          >
            {EVENT_TYPE_OPTIONS.map((o) => (
              <option key={o.value} value={o.value} disabled={o.disabled}>
                {o.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-xs text-slate-600 dark:text-slate-400">Ticker</label>
          <div className="flex gap-1">
            <input
              data-testid="ticker-filter-input"
              type="text"
              value={tickerInput}
              onChange={(e) => setTickerInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && applyTickerFilter()}
              placeholder="e.g. AAPL"
              className="bg-slate-800 border border-slate-600 text-slate-200 text-sm rounded px-2 py-1.5 w-28 focus:outline-none focus:border-slate-400"
            />
            <Button
              variant="outline"
              size="sm"
              onClick={applyTickerFilter}
              className="text-xs"
            >
              Apply
            </Button>
          </div>
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-xs text-slate-600 dark:text-slate-400">From date</label>
          <input
            type="date"
            value={sinceFilter}
            onChange={handleSinceChange}
            className="bg-slate-800 border border-slate-600 text-slate-200 text-sm rounded px-2 py-1.5 focus:outline-none focus:border-slate-400"
          />
        </div>

        {hasFilters && (
          <Button variant="ghost" size="sm" onClick={clearFilters} className="text-xs text-slate-600 dark:text-slate-400 mt-5">
            Clear filters
          </Button>
        )}
      </div>

      {/* Loading */}
      {isLoading && (
        <div data-testid="loading-state" className="space-y-2">
          {Array.from({ length: 5 }).map((_, i) => (
            <SkeletonRow key={i} />
          ))}
        </div>
      )}

      {/* Error */}
      {isError && !isLoading && (
        <div
          data-testid="error-state"
          className="flex flex-col items-center gap-3 py-12 text-center"
        >
          <p className="text-slate-300">
            Unable to load Red Flag Journal. Please try again.
          </p>
          <Button variant="outline" size="sm" onClick={() => refetch()}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Retry
          </Button>
        </div>
      )}

      {/* Empty state */}
      {!isLoading && !isError && items.length === 0 && (
        <div
          data-testid="empty-state"
          className="flex flex-col items-center gap-2 py-16 text-center"
        >
          {hasFilters ? (
            <>
              <p className="text-slate-300 text-sm">
                No events match your current filters.
              </p>
              <button
                onClick={clearFilters}
                className="text-xs text-slate-600 dark:text-slate-400 underline hover:text-slate-300"
              >
                Clear filters
              </button>
            </>
          ) : (
            <p className="text-slate-300">No strategy deviations recorded yet</p>
          )}
          <p data-testid="recorded-types-note" className="text-sm text-slate-600 dark:text-slate-400 max-w-sm">
            {recordedTypesNote()}
          </p>
        </div>
      )}

      {/* Event list */}
      {!isLoading && !isError && items.length > 0 && (
        <>
          <p className="text-xs text-slate-600 dark:text-slate-400">{total} event{total === 1 ? "" : "s"} recorded</p>
          <div className="space-y-2">
            {items.map((event) => (
              <EventRow key={event.id} event={event} />
            ))}
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between pt-2">
            <Button
              variant="outline"
              size="sm"
              disabled={page <= 1}
              onClick={() => setPage((p) => p - 1)}
            >
              <ChevronLeft className="w-4 h-4 mr-1" />
              Previous
            </Button>
            <span className="text-xs text-slate-600 dark:text-slate-400">
              Page {page} of {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              disabled={page >= totalPages}
              onClick={() => setPage((p) => p + 1)}
            >
              Next
              <ChevronRight className="w-4 h-4 ml-1" />
            </Button>
          </div>
        </>
      )}
    </div>
  );
}
