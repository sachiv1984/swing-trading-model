import { useState, useEffect, useCallback } from "react";
import { cn } from "../lib/utils";
import PageHeader from "../components/ui/PageHeader";
import NotificationTabBar from "../components/notifications/NotificationTabBar";
import { Button } from "../components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { ChevronUp, ChevronDown } from "lucide-react";
import { format, parseISO } from "date-fns";
import { apiFetch } from "../api/base44Client";

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const TYPE_LABELS = {
  stop_loss_approach: "Stop Loss Approach",
  grace_period_warning: "Grace Period Warning",
  market_regime_change: "Market Regime Change",
  daily_portfolio_summary: "Daily Portfolio Summary",
};

// Human-readable labels for values_compared keys
const VALUE_LABELS = {
  stop_price:        "Stop Price",
  current_price:     "Current Price",
  gap_pct:           "Gap to Stop",
  threshold_pct:     "Threshold",
  days_remaining:    "Days Left",
  grace_period_days: "Grace Period",
  regime:            "Regime",
  previous_regime:   "Previous Regime",
  positions_count:   "Positions",
  total_pnl:         "Total P&L",
};

// Keys to show in the compact cell, per rule type (max 3)
const COMPACT_PRIORITY = {
  stop_loss_approach:      ["current_price", "stop_price", "gap_pct"],
  grace_period_warning:    ["days_remaining", "grace_period_days"],
  market_regime_change:    ["regime", "previous_regime"],
  daily_portfolio_summary: ["positions_count", "total_pnl"],
};

function labelFor(key) {
  if (VALUE_LABELS[key]) return VALUE_LABELS[key];
  // Fallback: title-case the snake_case key
  return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatTimestamp(iso) {
  try {
    return format(parseISO(iso), "yyyy-MM-dd HH:mm");
  } catch {
    return iso;
  }
}

function formatValue(key, value) {
  if (value === null || value === undefined) return "—";
  const k = key.toLowerCase();
  if (typeof value === "number") {
    if (k.includes("_price") || k === "price" || k === "total_pnl") return `$${value.toFixed(2)}`;
    if (k.includes("_pct") || k.endsWith("pct")) return `${parseFloat(value.toFixed(2))}%`;
  }
  if (typeof value === "boolean") return value ? "Yes" : "No";
  return String(value);
}

function compactValues(obj, ruleType) {
  if (!obj || typeof obj !== "object") return "—";
  const keys = Object.keys(obj);
  const priority = COMPACT_PRIORITY[ruleType] || keys.slice(0, 3);
  const selected = priority.filter((k) => k in obj);
  const display = selected.length > 0 ? selected : keys.slice(0, 3);
  return display
    .map((k) => `${labelFor(k)} ${formatValue(k, obj[k])}`)
    .join(" · ");
}

function formatValuesExpanded(obj) {
  if (!obj || typeof obj !== "object") return [];
  const labelWidth = Math.max(...Object.keys(obj).map((k) => labelFor(k).length));
  return Object.entries(obj).map(([k, v]) => ({
    label: labelFor(k).padEnd(labelWidth, " "),
    value: formatValue(k, v),
    isNegative: k === "gap_pct" && typeof v === "number" && v < 0,
  }));
}

function TriggeredBadge({ value }) {
  return value ? (
    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-amber-500/20 text-amber-400 border border-amber-500/30">
      Yes
    </span>
  ) : (
    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-slate-700/50 text-slate-600 dark:text-slate-400 border border-slate-600/30">
      No
    </span>
  );
}

function NotifiedBadge({ value }) {
  return value ? (
    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
      Yes
    </span>
  ) : (
    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-slate-700/50 text-slate-600 dark:text-slate-400 border border-slate-600/30">
      No
    </span>
  );
}

function SkeletonRows() {
  return (
    <>
      {Array.from({ length: 5 }).map((_, i) => (
        <tr key={i}>
          {Array.from({ length: 6 }).map((_, j) => (
            <td key={j} className="px-5 py-4">
              <div className="h-4 bg-slate-700 rounded animate-pulse" style={{ width: `${60 + (j * 17) % 40}%` }} />
            </td>
          ))}
        </tr>
      ))}
    </>
  );
}

export default function NotificationsHistory() {
  const [evaluations, setEvaluations] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [filterType, setFilterType] = useState("all");
  const [sortDir, setSortDir] = useState("desc");
  const [expandedId, setExpandedId] = useState(null);

  const fetchHistory = useCallback(async (params = "last_n_days=30") => {
    setLoadError(false);
    try {
      const res = await apiFetch(`${API_BASE_URL}/alerts/history?${params}`);
      if (!res.ok) throw new Error();
      const json = await res.json();
      return json.data;
    } catch {
      throw new Error("load_failed");
    }
  }, []);

  useEffect(() => {
    setLoading(true);
    fetchHistory("last_n_days=30")
      .then((data) => {
        setEvaluations(data.evaluations);
        setTotal(data.total);
      })
      .catch(() => setLoadError(true))
      .finally(() => setLoading(false));
  }, [fetchHistory]);

  const handleLoadMore = async () => {
    setLoadingMore(true);
    try {
      const data = await fetchHistory("last_n_records=200");
      setEvaluations(data.evaluations);
      setTotal(data.total);
    } catch {
      // silently fail — user can retry
    } finally {
      setLoadingMore(false);
    }
  };

  const toggleSort = () => setSortDir((d) => (d === "desc" ? "asc" : "desc"));

  const toggleExpand = (id) => setExpandedId((prev) => (prev === id ? null : id));

  // Filter client-side
  const filtered = evaluations.filter(
    (e) => filterType === "all" || e.rule_type === filterType
  );

  // Sort
  const sorted = [...filtered].sort((a, b) => {
    const diff = new Date(a.evaluation_timestamp) - new Date(b.evaluation_timestamp);
    return sortDir === "desc" ? -diff : diff;
  });

  const hasMore = evaluations.length < total;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Alert History"
        description="A log of every alert rule evaluation by the system."
      />

      <NotificationTabBar />

      {/* Controls */}
      <div className="flex justify-end items-center gap-3">
        <span className="text-sm text-slate-600 dark:text-slate-400">Filter by type:</span>
        <Select value={filterType} onValueChange={setFilterType}>
          <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white w-52">
            <SelectValue />
          </SelectTrigger>
          <SelectContent className="bg-slate-800 border-slate-700">
            <SelectItem value="all">All types</SelectItem>
            <SelectItem value="stop_loss_approach">Stop Loss Approach</SelectItem>
            <SelectItem value="grace_period_warning">Grace Period Warning</SelectItem>
            <SelectItem value="market_regime_change">Market Regime Change</SelectItem>
            <SelectItem value="daily_portfolio_summary">Daily Portfolio Summary</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Table */}
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 overflow-hidden">
        {loadError ? (
          <div className="p-6 text-rose-400 text-sm">
            Unable to load alert history. Please refresh.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700/50">
                  {/* Date / Time — sortable */}
                  <th
                    className="px-5 py-3.5 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider whitespace-nowrap cursor-pointer select-none hover:text-white transition-colors"
                    onClick={toggleSort}
                  >
                    <span className="inline-flex items-center gap-1">
                      Date / Time
                      {sortDir === "desc" ? (
                        <ChevronDown className="w-3.5 h-3.5" />
                      ) : (
                        <ChevronUp className="w-3.5 h-3.5" />
                      )}
                    </span>
                  </th>
                  {["Alert Type", "Symbol", "Triggered", "Notified", "Values"].map((h) => (
                    <th key={h} className="px-5 py-3.5 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider whitespace-nowrap">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/30">
                {loading ? (
                  <SkeletonRows />
                ) : sorted.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-5 py-16 text-center">
                      {filterType === "all" ? (
                        <div>
                          <p className="text-base font-semibold text-white mb-1">No alert history yet.</p>
                          <p className="text-sm text-slate-600 dark:text-slate-400">Alert evaluations will appear here once the system has run.</p>
                        </div>
                      ) : (
                        <div>
                          <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">No evaluations found for the selected alert type.</p>
                          <button
                            onClick={() => setFilterType("all")}
                            className="text-sm text-cyan-400 hover:text-cyan-300 underline transition-colors"
                          >
                            Clear filter
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                ) : (
                  sorted.map((ev) => {
                    const isExpanded = expandedId === ev.id;
                    return (
                      <>
                        <tr
                          key={ev.id}
                          onClick={() => toggleExpand(ev.id)}
                          className={cn(
                            "cursor-pointer transition-colors",
                            isExpanded
                              ? "bg-slate-800/60"
                              : "hover:bg-slate-800/30"
                          )}
                        >
                          <td className="px-5 py-4 text-sm text-slate-300 whitespace-nowrap">
                            <span title={ev.evaluation_timestamp}>
                              {formatTimestamp(ev.evaluation_timestamp)}
                            </span>
                          </td>
                          <td className="px-5 py-4 text-sm text-white font-medium whitespace-nowrap">
                            {TYPE_LABELS[ev.rule_type] ?? ev.rule_type}
                          </td>
                          <td className="px-5 py-4 text-sm text-slate-300 font-mono">
                            {ev.symbol ?? "—"}
                          </td>
                          <td className="px-5 py-4">
                            <TriggeredBadge value={ev.triggered} />
                          </td>
                          <td className="px-5 py-4">
                            <NotifiedBadge value={ev.notification_sent} />
                          </td>
                          <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-400 max-w-xs truncate">
                            {isExpanded ? null : compactValues(ev.values_compared, ev.rule_type)}
                          </td>
                        </tr>

                        {/* Expanded row */}
                        {isExpanded && (
                          <tr key={`${ev.id}-expanded`} className="bg-slate-800/60">
                            <td colSpan={6} className="px-8 pb-5 pt-0">
                              <div className="font-mono text-xs text-slate-300 space-y-1 pt-1">
                                {formatValuesExpanded(ev.values_compared).map(({ label, value, isNegative }) => (
                                  <div key={label} className="flex gap-3">
                                    <span className="text-slate-600 dark:text-slate-400 whitespace-pre">{label}</span>
                                    <span className={isNegative ? "text-amber-400" : undefined}>{String(value)}</span>
                                  </div>
                                ))}
                              </div>
                            </td>
                          </tr>
                        )}
                      </>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Load more */}
      {!loading && !loadError && hasMore && (
        <div className="flex justify-center">
          <Button
            variant="outline"
            onClick={handleLoadMore}
            disabled={loadingMore}
            className="bg-slate-800/50 border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700"
          >
            {loadingMore ? "Loading…" : "Load more"}
          </Button>
        </div>
      )}
    </div>
  );
}
