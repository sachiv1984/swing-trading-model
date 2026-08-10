import { useState, useEffect, useCallback, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api/base44Client";
import { useEarnings } from "../hooks/useEarnings";
import { Button } from "../components/ui/button";
import PageHeader from "../components/ui/PageHeader";
import DataState from "../components/ui/DataState";
import { cn } from "../lib/utils";
import {
  RefreshCw,
  ChevronUp,
  ChevronDown,
  Newspaper,
  Plus,
  Check,
  X,
  Search,
  Loader2,
  AlertTriangle,
  BarChart2,
} from "lucide-react";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const POLL_INTERVAL_MS = 5000;
const POLL_MAX_MS = 300000; // 5 minutes — screener runs async in background
const STALE_HOURS = 24;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function relativeTime(isoString) {
  if (!isoString) return null;
  const diff = Date.now() - new Date(isoString).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins} minute${mins !== 1 ? "s" : ""} ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs} hour${hrs !== 1 ? "s" : ""} ago`;
  const days = Math.floor(hrs / 24);
  return `${days} day${days !== 1 ? "s" : ""} ago`;
}

function isStale(isoString) {
  if (!isoString) return false;
  const diff = Date.now() - new Date(isoString).getTime();
  return diff > STALE_HOURS * 3600000;
}

function currencySymbol(currency) {
  if (!currency) return "$";
  if (currency === "GBP" || currency === "GBp") return "£";
  return "$";
}

function formatPrice(value, currency) {
  if (value == null) return "—";
  return `${currencySymbol(currency)}${Number(value).toFixed(2)}`;
}

function formatATR(atr, atrPct, currency) {
  if (atr == null) return "—";
  const pct = atrPct != null ? ` (${(atrPct * 100).toFixed(1)}%)` : "";
  return `${currencySymbol(currency)}${Number(atr).toFixed(2)}${pct}`;
}

function formatSignal(score) {
  if (score == null) return "—";
  return `${(score * 100).toFixed(0)}%`;
}

function entryZoneLabel(proximity) {
  if (proximity == null) return "—";
  if (proximity <= 0.02) return "In zone";
  if (proximity <= 0.05) return "Near entry";
  return "—";
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function stripUkSuffix(ticker) {
  return ticker ? ticker.replace(/\.L$/, "") : ticker;
}

function RegimeBadge({ status }) {
  if (status === "risk_on") {
    return (
      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
        Risk On
      </span>
    );
  }
  return (
    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-slate-700/50 text-slate-600 dark:text-slate-400 border border-slate-600/30">
      Risk Off
    </span>
  );
}

function MarketBadge({ market }) {
  const cls =
    market === "UK"
      ? "bg-blue-500/20 text-blue-400 border-blue-500/30"
      : "bg-violet-500/20 text-violet-400 border-violet-500/30";
  return (
    <span className={cn("inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border", cls)}>
      {market}
    </span>
  );
}

// ST-21 (BLG-FEAT-29, EPIC-06, v8.5) — Regime History panel.
// Design source: docs/design/2026-08-08__release-v8.5/regime-distribution-panel/decision_record.md
//
// Colour correction from the decision record's own prose (RISK-01-style
// implementation check): the record describes "green segment = risk_on, red
// segment = risk_off — reusing the exact chip colours already defined for
// the per-row Regime column." The *actual* per-row RegimeBadge above uses
// emerald for risk_on but a neutral slate/grey (not red) for risk_off — a
// risk-off market isn't itself an alarm condition, it's the strategy
// correctly sitting out, so a red "danger" colour was never really
// appropriate there. This panel reuses RegimeBadge's *real* colours
// (emerald / slate-grey) rather than the record's red assumption, which
// most faithfully satisfies the record's own stated intent — visual
// consistency with the existing per-row chips, not a new second convention.
function RegimeHistoryPanel() {
  const [window_, setWindow_] = useState("30d");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchDistribution = useCallback(async (win) => {
    setLoading(true);
    setError(false);
    try {
      const res = await apiFetch(`${API_BASE}/screener/regime-distribution?window=${win}`);
      if (!res.ok) throw new Error();
      const json = await res.json();
      setData(json.data || json);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDistribution(window_);
  }, [window_, fetchDistribution]);

  const hasData = data && data.total_observations > 0;

  return (
    <div
      data-testid="regime-history-panel"
      className="mb-4 p-4 rounded-xl border border-slate-700/50 bg-slate-800/30"
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-white">Regime History</h3>
        <div className="flex rounded-md border border-slate-700 overflow-hidden text-xs" data-testid="regime-window-selector">
          {["30d", "60d", "all"].map((w) => (
            <button
              key={w}
              data-testid={`regime-window-${w}`}
              onClick={() => setWindow_(w)}
              className={cn(
                "px-3 py-1.5 transition-colors capitalize",
                window_ === w
                  ? "bg-slate-700 text-white"
                  : "bg-slate-900 text-slate-600 dark:text-slate-400 hover:text-white"
              )}
            >
              {w === "all" ? "All" : w}
            </button>
          ))}
        </div>
      </div>

      <DataState
        loading={loading}
        error={error}
        onRetry={() => fetchDistribution(window_)}
        empty={!loading && !error && !hasData}
        emptyIcon={<BarChart2 className="w-8 h-8 text-slate-600" />}
        emptyHeading="No regime history yet"
        emptyBody="Regime history accrues as screener runs complete over the selected window."
        compact
      >
        {hasData && (
          <>
            <div
              data-testid="regime-distribution-bar"
              className="flex h-2.5 rounded-full overflow-hidden bg-slate-900"
            >
              <div
                data-testid="regime-bar-risk-on"
                className="bg-emerald-500"
                style={{ width: `${data.risk_on_pct}%` }}
              />
              <div
                data-testid="regime-bar-risk-off"
                className="bg-slate-600"
                style={{ width: `${data.risk_off_pct}%` }}
              />
            </div>
            <p className="mt-2 text-xs text-slate-600 dark:text-slate-400" data-testid="regime-distribution-readout">
              Risk-On {data.risk_on_pct}% · Risk-Off {data.risk_off_pct}% ({window_ === "all" ? "All" : window_})
            </p>
          </>
        )}
      </DataState>
    </div>
  );
}

function EarningsBadge({ ticker, market }) {
  const { data, loading } = useEarnings(ticker, market);
  if (loading) return <span className="text-slate-600 text-xs">…</span>;
  if (!data || data.days_until_earnings == null) return <span className="text-slate-600 text-xs">—</span>;
  const days = data.days_until_earnings;
  if (days < 0) return <span className="text-slate-600 text-xs">—</span>;
  if (days === 0) return <span className="text-amber-400 font-medium text-xs">Today</span>;
  const cls =
    days <= 5
      ? "text-amber-400 font-medium"
      : days <= 14
      ? "text-yellow-500"
      : "text-slate-600 dark:text-slate-400";
  return <span className={`text-xs ${cls}`}>{days}d</span>;
}

function SkeletonRow() {
  return (
    <tr className="border-b border-slate-800/50">
      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((i) => (
        <td key={i} className="px-3 py-3">
          <div className="h-4 bg-slate-700/50 rounded animate-pulse" style={{ width: `${50 + (i * 13) % 40}%` }} />
        </td>
      ))}
    </tr>
  );
}

// ---------------------------------------------------------------------------
// Inline watchlist popover
// ---------------------------------------------------------------------------

function WatchlistPopover({ result, onClose, onAdded }) {
  const [targetPrice, setTargetPrice] = useState(
    result.price != null ? String(Number(result.price).toFixed(2)) : ""
  );
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleAdd = async () => {
    setSubmitting(true);
    setError(null);
    try {
      const body = {
        ticker: result.market === "UK" ? stripUkSuffix(result.ticker) : result.ticker,
        market: result.market,
        target_entry_price: targetPrice !== "" ? parseFloat(targetPrice) : null,
      };
      const res = await apiFetch(`${API_BASE}/watchlist`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (res.status === 409) {
        onAdded(result.ticker); // already in watchlist — treat as success
        onClose();
        return;
      }
      if (!res.ok) throw new Error();
      onAdded(result.ticker);
      onClose();
    } catch {
      setError("Could not add to watchlist — try again");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <td colSpan={10} className="p-0">
      <div className="mx-3 my-1 p-3 bg-slate-800 border border-slate-700 rounded-lg">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div className="flex items-center gap-3 flex-wrap">
            <span className="text-sm font-medium text-white">
              Add <span className="text-emerald-400">{result.market === "UK" ? stripUkSuffix(result.ticker) : result.ticker}</span> to Watchlist
            </span>
            <span className="text-xs text-slate-600 dark:text-slate-400">
              {formatPrice(result.price, result.currency)}
            </span>
            <div className="flex items-center gap-2">
              <label className="text-xs text-slate-600 dark:text-slate-400">Target entry</label>
              <input
                type="number"
                step="0.01"
                className="w-24 px-2 py-1 text-sm bg-slate-900 border border-slate-600 rounded text-white focus:outline-none focus:border-emerald-500"
                value={targetPrice}
                onChange={(e) => setTargetPrice(e.target.value)}
                placeholder="Optional"
              />
            </div>
          </div>
          <div className="flex items-center gap-2">
            {error && <span className="text-xs text-red-400">{error}</span>}
            <Button
              size="sm"
              onClick={handleAdd}
              disabled={submitting}
              className="bg-emerald-600 hover:bg-emerald-700 text-white h-7 px-3 text-xs"
            >
              {submitting ? <Loader2 className="w-3 h-3 animate-spin" /> : "Add to Watchlist"}
            </Button>
            <button
              onClick={onClose}
              className="text-slate-600 dark:text-slate-400 hover:text-white p-1 rounded"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </td>
  );
}

// ---------------------------------------------------------------------------
// News panel row
// ---------------------------------------------------------------------------

function NewsPanel({ ticker, cache, onClose }) {
  const { loading, headlines = [] } = cache || { loading: true, headlines: [] };
  return (
    <td colSpan={10} className="p-0">
      <div className="mx-3 my-1 p-3 bg-slate-800/60 border border-slate-700/50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-slate-300">
            <Newspaper className="w-3 h-3 inline mr-1" />
            Recent news — {ticker}
          </span>
          <button onClick={onClose} className="text-slate-600 dark:text-slate-400 hover:text-white">
            <X className="w-3 h-3" />
          </button>
        </div>
        {loading ? (
          <p className="text-xs text-slate-600 dark:text-slate-400 animate-pulse">Loading headlines…</p>
        ) : headlines.length > 0 ? (
          <ul className="space-y-1.5">
            {headlines.slice(0, 10).map((h, i) => (
              <li key={i} className="text-xs text-slate-300 flex gap-2">
                <span className="shrink-0 text-slate-600 dark:text-slate-400 mt-0.5">
                  {h.published_at ? relativeTime(h.published_at) : ""}
                </span>
                {h.url ? (
                  <a href={h.url} target="_blank" rel="noopener noreferrer" className="hover:text-blue-400 hover:underline">{h.headline || h.title}</a>
                ) : (
                  <span>{h.headline || h.title}</span>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-xs text-slate-600 dark:text-slate-400">No recent news available for {ticker}.</p>
        )}
        <button
          onClick={onClose}
          className="mt-2 text-xs text-slate-600 dark:text-slate-400 hover:text-slate-300 underline"
        >
          Close
        </button>
      </div>
    </td>
  );
}

// ---------------------------------------------------------------------------
// Sort header cell
// ---------------------------------------------------------------------------

function SortHeader({ label, field, current, dir, onSort, className }) {
  const active = current === field;
  return (
    <th
      className={cn(
        "px-3 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider cursor-pointer select-none whitespace-nowrap",
        active && "text-white",
        className
      )}
      onClick={() => onSort(field)}
    >
      <span className="flex items-center gap-1">
        {label}
        {active ? (
          dir === "asc" ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />
        ) : (
          <ChevronDown className="w-3 h-3 opacity-30" />
        )}
      </span>
    </th>
  );
}

// ---------------------------------------------------------------------------
// Screener quality panel (ST-04, EPIC-03, v6.0 — replaces DegradedRunBanner)
// ---------------------------------------------------------------------------

function ScreenerQualityPanel({ runQuality, tickersRequested, tickersLoaded, tickersFailed, lastFullRunUtc }) {
  const [failedExpanded, setFailedExpanded] = useState(false);

  const staleHours = lastFullRunUtc
    ? Math.round((Date.now() - new Date(lastFullRunUtc).getTime()) / 3600000)
    : null;
  const isStale = staleHours !== null && staleHours > 24;

  if (runQuality === "FULL") {
    return (
      <div data-testid="screener-quality-panel" data-quality="FULL" className="mb-4 space-y-2">
        <div className="flex items-center gap-2 px-4 py-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-sm text-emerald-400">
          <span className="font-semibold">Full run</span>
          <span className="text-emerald-300">{tickersLoaded} / {tickersRequested} tickers loaded</span>
        </div>
        {isStale && (
          <div data-testid="stale-advisory" className="px-4 py-2 rounded-lg bg-slate-800 border border-slate-700 text-xs text-slate-600 dark:text-slate-400">
            Last full run: {staleHours} hours ago
          </div>
        )}
      </div>
    );
  }

  if (runQuality === "DEGRADED") {
    const failedCount = Array.isArray(tickersFailed) ? tickersFailed.length : 0;
    return (
      <div data-testid="screener-quality-panel" data-quality="DEGRADED" className="mb-4 space-y-2">
        <div className="flex items-start gap-2 px-4 py-3 rounded-lg bg-amber-500/10 border border-amber-500/30 text-sm text-amber-400">
          <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="font-semibold">Degraded run</span>
              <span className="text-amber-300">{tickersLoaded} / {tickersRequested} tickers loaded</span>
            </div>
            <p className="text-amber-300/80">Results may be incomplete — {failedCount} ticker{failedCount !== 1 ? "s" : ""} failed to load</p>
            {failedCount > 0 && (
              <button
                className="mt-1 text-xs underline text-amber-400/70 hover:text-amber-400"
                onClick={() => setFailedExpanded(v => !v)}
                aria-expanded={failedExpanded}
              >
                {failedExpanded ? "Hide" : "Show"} failed tickers
              </button>
            )}
            {failedExpanded && failedCount > 0 && (
              <div data-testid="failed-ticker-list" className="mt-2 text-xs text-amber-300/60 flex flex-wrap gap-1">
                {tickersFailed.map(t => (
                  <span key={t} className="px-1.5 py-0.5 bg-amber-500/10 rounded">{t}</span>
                ))}
              </div>
            )}
          </div>
        </div>
        {isStale && (
          <div data-testid="stale-advisory" className="px-4 py-2 rounded-lg bg-slate-800 border border-slate-700 text-xs text-slate-600 dark:text-slate-400">
            Last full run: {staleHours} hours ago
          </div>
        )}
      </div>
    );
  }

  // FAILED state
  return (
    <div data-testid="screener-quality-panel" data-quality="FAILED" className="mb-4">
      <div className="flex items-center gap-2 px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/30 text-sm text-red-400">
        <AlertTriangle className="w-4 h-4 shrink-0" />
        <span>Screener run failed — </span>
        <button className="underline hover:text-red-300" onClick={() => window.dispatchEvent(new Event("app:refresh"))}>
          retry
        </button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export default function Screener() {
  const navigate = useNavigate();
  const [results, setResults] = useState([]);
  const [runTimestamp, setRunTimestamp] = useState(null);
  const [runId, setRunId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [scanError, setScanError] = useState(false);
  const [degradedRun, setDegradedRun] = useState(false);
  const [failureRate, setFailureRate] = useState(0);
  const [runQuality, setRunQuality] = useState(null);
  const [tickersRequested, setTickersRequested] = useState(0);
  const [tickersLoaded, setTickersLoaded] = useState(0);
  const [tickersFailed, setTickersFailed] = useState([]);
  const [lastFullRunUtc, setLastFullRunUtc] = useState(null);

  const [sortField, setSortField] = useState("signal_score");
  const [sortDir, setSortDir] = useState("desc");
  const [marketFilter, setMarketFilter] = useState("All");
  const [regimeFilter, setRegimeFilter] = useState(false);
  const [sectorFilter, setSectorFilter] = useState([]);
  const [sectorMenuOpen, setSectorMenuOpen] = useState(false);

  const [watchlistAdded, setWatchlistAdded] = useState(new Set());
  const [promoRow, setPromoRow] = useState(null); // ticker of row with open popover
  const [expandedNews, setExpandedNews] = useState({});
  const [newsCache, setNewsCache] = useState({});

  const pollRef = useRef(null);
  const scanStartRef = useRef(null);
  const sectorMenuRef = useRef(null);

  // ---------------------------------------------------------------------------
  // Data fetch
  // ---------------------------------------------------------------------------

  const fetchResults = useCallback(async () => {
    setError(false);
    setLoading(true);
    try {
      const res = await apiFetch(`${API_BASE}/screener/results?limit=200`);
      if (res.status === 404) {
        setResults([]);
        setRunTimestamp(null);
        setRunId(null);
        return;
      }
      if (!res.ok) throw new Error();
      const json = await res.json();
      const payload = json.data || json;
      setResults(payload.results || []);
      setRunTimestamp(payload.run_timestamp || null);
      setRunId(payload.run_id || null);
      setDegradedRun(!!payload.degraded_run);
      setFailureRate(payload.failure_rate || 0);
      setRunQuality(payload.run_quality || null);
      setTickersRequested(payload.tickers_requested || 0);
      setTickersLoaded(payload.tickers_loaded || 0);
      setTickersFailed(payload.tickers_failed || []);
      setLastFullRunUtc(payload.last_full_run_utc || null);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchResults();
  }, [fetchResults]);

  // Listen for keyboard 'r' refresh event (ST-11)
  useEffect(() => {
    const handler = () => fetchResults();
    window.addEventListener("app:refresh", handler);
    return () => window.removeEventListener("app:refresh", handler);
  }, [fetchResults]);

  // Listen for keyboard 'w' watchlist event (ST-11) — focus first promotable row
  useEffect(() => {
    const handler = () => {
      if (filtered.length > 0 && !watchlistAdded.has(filtered[0].ticker)) {
        setPromoRow(filtered[0].ticker);
      }
    };
    window.addEventListener("app:add-to-watchlist", handler);
    return () => window.removeEventListener("app:add-to-watchlist", handler);
  });

  // Close sector dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (sectorMenuRef.current && !sectorMenuRef.current.contains(e.target)) {
        setSectorMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  // ---------------------------------------------------------------------------
  // Manual scan
  // ---------------------------------------------------------------------------

  const triggerScan = async () => {
    if (scanning) return;
    setScanError(false);
    setDegradedRun(false);
    setRunQuality(null);
    setTickersFailed([]);
    setScanning(true);
    scanStartRef.current = Date.now();
    try {
      const res = await apiFetch(`${API_BASE}/screener/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      if (res.status === 409) {
        // run already in progress — just poll
      } else if (!res.ok) {
        throw new Error();
      }
      const json = res.status === 409 ? {} : await res.json();
      const newRunId = json.data?.run_id;
      startPolling(newRunId);
    } catch {
      setScanError(true);
      setScanning(false);
    }
  };

  const startPolling = (newRunId) => {
    clearInterval(pollRef.current);
    pollRef.current = setInterval(async () => {
      if (Date.now() - scanStartRef.current > POLL_MAX_MS) {
        clearInterval(pollRef.current);
        setScanError(true);
        setScanning(false);
        return;
      }
      try {
        const url = newRunId
          ? `${API_BASE}/screener/results?run_id=${newRunId}&limit=200`
          : `${API_BASE}/screener/results?limit=200`;
        const res = await apiFetch(url);
        if (res.status === 404 && newRunId) {
          // Run completed with 0 results (likely risk-off regime)
          setResults([]);
          setRunTimestamp(new Date().toISOString());
          setRunId(newRunId);
          clearInterval(pollRef.current);
          setScanning(false);
          return;
        }
        if (!res.ok) return;
        const json = await res.json();
        const payload = json.data || json;
        if (payload.results?.length >= 0) {
          setResults(payload.results || []);
          setRunTimestamp(payload.run_timestamp || null);
          setRunId(payload.run_id || null);
          setDegradedRun(!!payload.degraded_run);
          setFailureRate(payload.failure_rate || 0);
          setRunQuality(payload.run_quality || null);
          setTickersRequested(payload.tickers_requested || 0);
          setTickersLoaded(payload.tickers_loaded || 0);
          setTickersFailed(payload.tickers_failed || []);
          setLastFullRunUtc(payload.last_full_run_utc || null);
          clearInterval(pollRef.current);
          setScanning(false);
        }
      } catch {
        // retry next tick
      }
    }, POLL_INTERVAL_MS);
  };

  useEffect(() => () => clearInterval(pollRef.current), []);

  // ---------------------------------------------------------------------------
  // News fetch
  // ---------------------------------------------------------------------------

  const fetchNews = useCallback(async (ticker) => {
    if (newsCache[ticker]?.headlines) return; // already fetched
    setNewsCache((prev) => ({ ...prev, [ticker]: { loading: true, headlines: null } }));
    try {
      const res = await apiFetch(`${API_BASE}/news/${ticker}`);
      if (!res.ok) throw new Error();
      const json = await res.json();
      setNewsCache((prev) => ({
        ...prev,
        [ticker]: { loading: false, headlines: json.data?.headlines || json.headlines || [] },
      }));
    } catch {
      setNewsCache((prev) => ({ ...prev, [ticker]: { loading: false, headlines: [] } }));
    }
  }, [newsCache]);

  const toggleNews = (ticker) => {
    const next = !expandedNews[ticker];
    setExpandedNews((prev) => ({ ...prev, [ticker]: next }));
    if (next) fetchNews(ticker);
  };

  // ---------------------------------------------------------------------------
  // Sort & filter
  // ---------------------------------------------------------------------------

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortField(field);
      setSortDir(field === "signal_score" ? "desc" : "asc");
    }
  };

  const allSectors = [...new Set(results.map((r) => r.sector).filter(Boolean))].sort();

  const filtered = results
    .filter((r) => marketFilter === "All" || r.market === marketFilter)
    .filter((r) => !regimeFilter || r.regime_status === "risk_on")
    .filter((r) => sectorFilter.length === 0 || sectorFilter.includes(r.sector))
    .sort((a, b) => {
      const mul = sortDir === "asc" ? 1 : -1;
      const av = a[sortField] ?? -Infinity;
      const bv = b[sortField] ?? -Infinity;
      return (av < bv ? -1 : av > bv ? 1 : 0) * mul;
    });

  // ---------------------------------------------------------------------------
  // Render helpers
  // ---------------------------------------------------------------------------

  const stale = isStale(runTimestamp);
  const noRuns = !loading && !error && results.length === 0 && !runTimestamp;
  const noPass = !loading && !error && results.length === 0 && !!runTimestamp;
  const allFiltered = !loading && !error && results.length > 0 && filtered.length === 0;

  const freshnessBadge = runTimestamp ? (
    <span
      className={cn(
        "text-xs px-2 py-0.5 rounded-full border",
        stale
          ? "bg-amber-500/10 text-amber-400 border-amber-500/30"
          : "bg-slate-700/50 text-slate-600 dark:text-slate-400 border-slate-600/30"
      )}
    >
      {stale ? "Results may be stale — " : "Last screened: "}
      {relativeTime(runTimestamp)}
    </span>
  ) : (
    <span className="text-xs text-slate-600 dark:text-slate-400">No screener run yet</span>
  );

  const refreshBtn = (
    <Button
      size="sm"
      variant="outline"
      onClick={triggerScan}
      disabled={scanning}
      className="h-8 gap-2 text-xs border-slate-700 text-slate-300 hover:text-white hover:border-slate-500"
    >
      {scanning ? (
        <>
          <Loader2 className="w-3 h-3 animate-spin" />
          Scanning…
        </>
      ) : (
        <>
          <RefreshCw className="w-3 h-3" />
          Refresh
        </>
      )}
    </Button>
  );

  // ---------------------------------------------------------------------------
  // JSX
  // ---------------------------------------------------------------------------

  return (
    <div>
      <PageHeader
        title="Screener"
        description="Strategy-filtered ticker candidates ranked by momentum signal"
        actions={
          <div className="flex items-center gap-3">
            {freshnessBadge}
            {refreshBtn}
          </div>
        }
      />

      <RegimeHistoryPanel />

      {runQuality && (
        <ScreenerQualityPanel
          runQuality={runQuality}
          tickersRequested={tickersRequested}
          tickersLoaded={tickersLoaded}
          tickersFailed={tickersFailed}
          lastFullRunUtc={lastFullRunUtc}
        />
      )}

      {scanError && (
        <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-sm text-red-400">
          Screener run failed — try again
        </div>
      )}

      {/* Filter bar */}
      {!loading && !error && results.length > 0 && (
        <div className="flex flex-wrap items-center gap-3 mb-4">
          {/* Market filter */}
          <div className="flex rounded-md border border-slate-700 overflow-hidden text-xs" data-testid="market-filter-bar">
            {["All", "US", "UK"].map((m) => (
              <button
                key={m}
                data-testid={`market-filter-${m.toLowerCase()}`}
                onClick={() => setMarketFilter(m)}
                className={cn(
                  "px-3 py-1.5 transition-colors",
                  marketFilter === m
                    ? "bg-slate-700 text-white"
                    : "bg-slate-900 text-slate-600 dark:text-slate-400 hover:text-white"
                )}
              >
                {m}
              </button>
            ))}
          </div>

          {/* Regime filter */}
          <button
            onClick={() => setRegimeFilter((v) => !v)}
            className={cn(
              "px-3 py-1.5 rounded-md border text-xs transition-colors",
              regimeFilter
                ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-400"
                : "border-slate-700 bg-slate-900 text-slate-600 dark:text-slate-400 hover:text-white"
            )}
          >
            Risk-On only
          </button>

          {/* Sector filter */}
          {allSectors.length > 0 && (
            <div className="relative" ref={sectorMenuRef}>
              <button
                onClick={() => setSectorMenuOpen((v) => !v)}
                className={cn(
                  "px-3 py-1.5 rounded-md border text-xs transition-colors flex items-center gap-1",
                  sectorFilter.length > 0
                    ? "border-blue-500/50 bg-blue-500/10 text-blue-400"
                    : "border-slate-700 bg-slate-900 text-slate-600 dark:text-slate-400 hover:text-white"
                )}
              >
                <Search className="w-3 h-3" />
                {sectorFilter.length > 0 ? `${sectorFilter.length} sector${sectorFilter.length > 1 ? "s" : ""}` : "Sector"}
                <ChevronDown className="w-3 h-3" />
              </button>
              {sectorMenuOpen && (
                <div className="absolute top-full left-0 mt-1 z-20 w-48 bg-slate-800 border border-slate-700 rounded-lg shadow-xl py-1 max-h-52 overflow-y-auto">
                  <button
                    className="w-full text-left px-3 py-1.5 text-xs text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-700"
                    onClick={() => { setSectorFilter([]); setSectorMenuOpen(false); }}
                  >
                    All sectors
                  </button>
                  {allSectors.map((s) => (
                    <button
                      key={s}
                      onClick={() =>
                        setSectorFilter((prev) =>
                          prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s]
                        )
                      }
                      className={cn(
                        "w-full text-left px-3 py-1.5 text-xs flex items-center gap-2",
                        sectorFilter.includes(s)
                          ? "text-blue-400 bg-blue-500/10"
                          : "text-slate-300 hover:text-white hover:bg-slate-700"
                      )}
                    >
                      {sectorFilter.includes(s) && <Check className="w-3 h-3 shrink-0" />}
                      {s}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {(marketFilter !== "All" || regimeFilter || sectorFilter.length > 0) && (
            <button
              onClick={() => { setMarketFilter("All"); setRegimeFilter(false); setSectorFilter([]); }}
              className="text-xs text-slate-600 dark:text-slate-400 hover:text-slate-300 underline"
            >
              Clear filters
            </button>
          )}
        </div>
      )}

      <DataState
        loading={loading}
        error={error}
        onRetry={fetchResults}
        empty={noRuns}
        emptyHeading="No screener results yet"
        emptyBody="Run your first screen to find strategy-passing candidates."
        emptyAction={
          <Button onClick={triggerScan} disabled={scanning} className="bg-emerald-600 hover:bg-emerald-700">
            {scanning ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
            Run Screener
          </Button>
        }
      >
        {noPass && (
          <div className="text-center py-16 text-slate-600 dark:text-slate-400">
            <p className="text-sm">No tickers pass your current strategy filters.</p>
            <p className="text-xs mt-1 text-slate-600 dark:text-slate-400">
              This may indicate a risk-off market regime.
            </p>
          </div>
        )}

        {allFiltered && (
          <div className="text-center py-8 text-slate-600 dark:text-slate-400 text-sm">
            No tickers match your current filters. Adjust filters to see results.
          </div>
        )}

        {!noRuns && !noPass && (
          <div className="overflow-x-auto rounded-lg border border-slate-800">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-800 bg-slate-900/50">
                  <th className="px-3 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider">Ticker</th>
                  <th className="px-3 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider">Market</th>
                  <SortHeader label="Price" field="price" current={sortField} dir={sortDir} onSort={handleSort} />
                  <SortHeader label="ATR" field="atr" current={sortField} dir={sortDir} onSort={handleSort} />
                  <th className="px-3 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider">Regime</th>
                  <SortHeader label="Signal" field="signal_score" current={sortField} dir={sortDir} onSort={handleSort} />
                  <th className="px-3 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider hidden md:table-cell">Sector</th>
                  <th className="px-3 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider hidden md:table-cell">Entry Zone</th>
                  <th className="px-3 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider hidden lg:table-cell" title="Days until next earnings">Earnings</th>
                  <th className="px-3 py-3 text-left text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider">News</th>
                </tr>
              </thead>
              <tbody>
                {loading
                  ? Array.from({ length: 8 }, (_, i) => <SkeletonRow key={i} />)
                  : filtered.map((row) => {
                      const isPromoOpen = promoRow === row.ticker;
                      const newsOpen = expandedNews[row.ticker];
                      const added = watchlistAdded.has(row.ticker);

                      return (
                        <>
                          <tr
                            key={row.ticker}
                            className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors"
                          >
                            <td className="px-3 py-3 font-mono font-medium text-white">
                              {row.market === "UK" ? stripUkSuffix(row.ticker) : row.ticker}
                            </td>
                            <td className="px-3 py-3">
                              <MarketBadge market={row.market} />
                            </td>
                            <td className="px-3 py-3 text-slate-300">
                              {formatPrice(row.price, row.currency)}
                            </td>
                            <td className="px-3 py-3 text-slate-300">
                              {formatATR(row.atr, row.atr_pct, row.currency)}
                            </td>
                            <td className="px-3 py-3">
                              <RegimeBadge status={row.regime_status} />
                            </td>
                            <td className="px-3 py-3">
                              <div className="flex items-center gap-2">
                                <div className="w-16 bg-slate-700/50 rounded-full h-1.5 overflow-hidden">
                                  <div
                                    className="h-full bg-emerald-500 rounded-full"
                                    style={{ width: `${(row.signal_score || 0) * 100}%` }}
                                  />
                                </div>
                                <span className="text-slate-300 text-xs">
                                  {formatSignal(row.signal_score)}
                                </span>
                              </div>
                            </td>
                            <td className="px-3 py-3 text-slate-600 dark:text-slate-400 hidden md:table-cell">
                              {row.sector || "—"}
                            </td>
                            <td className="px-3 py-3 text-slate-600 dark:text-slate-400 hidden md:table-cell">
                              {entryZoneLabel(row.proximity_to_entry_zone)}
                            </td>
                            <td className="px-3 py-3 hidden lg:table-cell">
                              <EarningsBadge ticker={row.ticker} market={row.market} />
                            </td>
                            <td className="px-3 py-3">
                              <div className="flex items-center gap-2">
                                {/* News badge — US only */}
                                {row.market === "US" && row.news_headline_count > 0 ? (
                                  <button
                                    onClick={() => toggleNews(row.ticker)}
                                    className={cn(
                                      "inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs border transition-colors",
                                      newsOpen
                                        ? "bg-blue-500/20 text-blue-400 border-blue-500/30"
                                        : "bg-slate-700/50 text-slate-600 dark:text-slate-400 border-slate-600/30 hover:text-blue-400"
                                    )}
                                    title="Show news headlines"
                                  >
                                    <Newspaper className="w-3 h-3" />
                                    {row.news_headline_count}
                                  </button>
                                ) : null}

                                {/* Watchlist button */}
                                {added ? (
                                  <span className="inline-flex items-center gap-1 text-xs text-emerald-400">
                                    <Check className="w-3 h-3" /> Added
                                  </span>
                                ) : (
                                  <button
                                    onClick={() => {
                                      setPromoRow(isPromoOpen ? null : row.ticker);
                                    }}
                                    className={cn(
                                      "inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs border transition-colors",
                                      isPromoOpen
                                        ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-400"
                                        : "border-slate-600/30 text-slate-600 dark:text-slate-400 hover:text-emerald-400 hover:border-emerald-500/30"
                                    )}
                                    title="Add to watchlist"
                                  >
                                    <Plus className="w-3 h-3" />
                                    Watchlist
                                  </button>
                                )}
                                {/* Research link */}
                                <button
                                  onClick={() => navigate(`/research/${row.ticker}`)}
                                  className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs border border-slate-600/30 text-slate-600 dark:text-slate-400 hover:text-cyan-400 hover:border-cyan-500/30 transition-colors"
                                  title="Pre-trade research"
                                >
                                  Research
                                </button>
                              </div>
                            </td>
                          </tr>

                          {/* Watchlist promotion popover row */}
                          {isPromoOpen && (
                            <tr key={`promo-${row.ticker}`} className="bg-slate-900/40">
                              <WatchlistPopover
                                result={row}
                                onClose={() => setPromoRow(null)}
                                onAdded={(ticker) => {
                                  setWatchlistAdded((prev) => new Set([...prev, ticker]));
                                  setPromoRow(null);
                                }}
                              />
                            </tr>
                          )}

                          {/* News panel row */}
                          {newsOpen && (
                            <tr key={`news-${row.ticker}`} className="bg-slate-900/40">
                              <NewsPanel
                                ticker={row.ticker}
                                cache={newsCache[row.ticker]}
                                onClose={() => setExpandedNews((prev) => ({ ...prev, [row.ticker]: false }))}
                              />
                            </tr>
                          )}
                        </>
                      );
                    })}
              </tbody>
            </table>
          </div>
        )}
      </DataState>
    </div>
  );
}
