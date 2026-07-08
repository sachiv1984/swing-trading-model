import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api/base44Client";
import { useEarnings } from "../hooks/useEarnings";
import { Button } from "../components/ui/button";
import PageHeader from "../components/ui/PageHeader";
import { Plus, Trash2, Eye, Newspaper, ChevronDown, ChevronUp, BookOpen } from "lucide-react";
import { cn } from "../lib/utils";
import WatchlistModal from "../components/watchlist/WatchlistModal";
import DataState from "../components/ui/DataState";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const SIGNAL_ORDER = { active: 0, watch: 1, no_signal: 2 };

function sortEntries(entries) {
  return [...entries].sort((a, b) => {
    const sigDiff =
      (SIGNAL_ORDER[a.signal_status] ?? 2) -
      (SIGNAL_ORDER[b.signal_status] ?? 2);
    if (sigDiff !== 0) return sigDiff;
    return a.ticker.localeCompare(b.ticker);
  });
}

function SignalBadge({ status }) {
  const cfg =
    {
      active: { label: "Active", cls: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
      watch: { label: "Watch", cls: "bg-amber-500/20 text-amber-400 border-amber-500/30" },
      no_signal: { label: "No Signal", cls: "bg-slate-700/50 text-slate-600 dark:text-slate-400 border-slate-600/30" },
    }[status] || { label: status, cls: "bg-slate-700/50 text-slate-600 dark:text-slate-400 border-slate-600/30" };
  return (
    <span
      className={cn(
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border",
        cfg.cls
      )}
    >
      {cfg.label}
    </span>
  );
}

function MarketBadge({ market }) {
  const cls =
    market === "UK"
      ? "bg-blue-500/20 text-blue-400 border-blue-500/30"
      : "bg-violet-500/20 text-violet-400 border-violet-500/30";
  return (
    <span
      className={cn(
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border",
        cls
      )}
    >
      {market}
    </span>
  );
}

function priceDisplay(value, market) {
  if (value == null) return "—";
  const sym = market === "UK" ? "£" : "$";
  return `${sym}${Number(value).toFixed(2)}`;
}

function WatchlistEarningsBadge({ ticker, market }) {
  const { data, loading } = useEarnings(ticker, market);
  if (loading) return <span className="text-slate-600 text-xs">…</span>;
  if (!data || data.days_until_earnings == null) return <span className="text-slate-600 text-xs">—</span>;
  const days = data.days_until_earnings;
  if (days < 0) return <span className="text-slate-600 text-xs">—</span>;
  if (days === 0) return <span className="text-amber-400 font-medium text-xs" title={data.next_earnings_date}>Today</span>;
  const cls = days <= 5 ? "text-amber-400 font-medium" : days <= 14 ? "text-yellow-500" : "text-slate-600 dark:text-slate-400";
  return <span className={`text-xs ${cls}`} title={data.next_earnings_date}>{days}d</span>;
}


export default function Watchlist() {
  const navigate = useNavigate();
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [removing, setRemoving] = useState({}); // { [id]: true } while fading out
  const [modal, setModal] = useState(null); // null | { mode, entry }
  const [expandedNews, setExpandedNews] = useState({}); // { [ticker]: true } expanded
  const [newsCache, setNewsCache] = useState({}); // { [ticker]: { loading, headlines } }

  // ST-09 (BLG-FE-29): screener results used as proxy for "research record exists"
  const { data: screenerTickers = new Set() } = useQuery({
    queryKey: ["screener-tickers"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/screener/results`);
      const json = await res.json();
      const rows = json?.data || [];
      return new Set(rows.map(r => (r.ticker || "").toUpperCase()));
    },
    staleTime: 5 * 60 * 1000,
  });

  const fetchEntries = useCallback(async () => {
    setLoadError(false);
    setLoading(true);
    try {
      const res = await apiFetch(`${API_BASE}/watchlist`);
      if (!res.ok) throw new Error();
      const json = await res.json();
      setEntries(sortEntries(json.data));
    } catch {
      setLoadError(true);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchEntries();
  }, [fetchEntries]);

  const handleAdded = (entry) => {
    setEntries((prev) => sortEntries([...prev, entry]));
    setModal(null);
  };

  const handleUpdated = (entry) => {
    setEntries((prev) =>
      sortEntries(prev.map((e) => (e.id === entry.id ? entry : e)))
    );
    setModal(null);
  };

  const fadeOutAndRemove = (id) => {
    setRemoving((prev) => ({ ...prev, [id]: true }));
    setTimeout(() => {
      setEntries((prev) => prev.filter((e) => e.id !== id));
      setRemoving((prev) => {
        const next = { ...prev };
        delete next[id];
        return next;
      });
    }, 200);
  };

  const handleDeleted = (id) => {
    setModal(null);
    fadeOutAndRemove(id);
  };

  const toggleNews = useCallback(async (entry) => {
    const key = entry.ticker;
    if (expandedNews[key]) {
      setExpandedNews((prev) => ({ ...prev, [key]: false }));
      return;
    }
    setExpandedNews((prev) => ({ ...prev, [key]: true }));
    if (newsCache[key]) return; // already fetched
    setNewsCache((prev) => ({ ...prev, [key]: { loading: true, headlines: [] } }));
    try {
      const res = await apiFetch(`${API_BASE}/news/${entry.ticker}?market=${entry.market}`);
      const json = await res.json();
      setNewsCache((prev) => ({
        ...prev,
        [key]: { loading: false, headlines: json.data?.headlines || [] },
      }));
    } catch {
      setNewsCache((prev) => ({ ...prev, [key]: { loading: false, headlines: [] } }));
    }
  }, [expandedNews, newsCache]);

  const handleAddToPosition = (entry) => {
    fadeOutAndRemove(entry.id);
    setTimeout(() => {
      navigate("/TradeEntry", {
        state: {
          watchlist_prefill: {
            id: entry.id,
            ticker: entry.ticker,
            market: entry.market,
            entry_price:
              entry.target_entry_price != null
                ? String(entry.target_entry_price)
                : "",
            stop_price:
              entry.initial_stop_price != null
                ? String(entry.initial_stop_price)
                : "",
          },
        },
      });
    }, 220);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Watchlist"
        description="Monitor tickers for entry opportunities."
        actions={
          <Button
            onClick={() => setModal({ mode: "add" })}
            className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Ticker
          </Button>
        }
      />

      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 overflow-hidden">
        <DataState
          loading={loading}
          error={loadError}
          onRetry={fetchEntries}
          empty={!loading && !loadError && entries.length === 0}
          emptyIcon={<Eye className="w-10 h-10 text-slate-600" />}
          emptyHeading="Your watchlist is empty"
          emptyBody="Add tickers you're monitoring for entry opportunities."
          emptyAction={
            <Button
              onClick={() => setModal({ mode: "add" })}
              className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25"
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Ticker
            </Button>
          }
        >
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700/50">
                  {[
                    "Ticker",
                    "Market",
                    "Entry Signal",
                    "Target Entry",
                    "Stop (Initial)",
                    "Stop (Current)",
                    "Earnings",
                    "Research",
                    "News",
                    "Actions",
                  ].map((h) => (
                    <th
                      key={h}
                      className="px-5 py-3.5 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider whitespace-nowrap"
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/30">
                {entries.map((entry) => (
                  <>
                  <tr
                    key={entry.id}
                    className={cn(
                      "transition-all duration-200",
                      removing[entry.id] ? "opacity-0" : "opacity-100"
                    )}
                  >
                    <td className="px-5 py-4">
                      <button
                        onClick={() => setModal({ mode: "edit", entry })}
                        className="text-left group"
                      >
                        <span className="block text-cyan-400 group-hover:text-cyan-300 font-semibold text-sm transition-colors">
                          {entry.ticker}
                        </span>
                        {entry.company_name && (
                          <span className="block text-slate-600 dark:text-slate-400 text-xs truncate max-w-[140px]">
                            {entry.company_name}
                          </span>
                        )}
                      </button>
                    </td>
                    <td className="px-5 py-4">
                      <MarketBadge market={entry.market} />
                    </td>
                    <td className="px-5 py-4">
                      <SignalBadge status={entry.signal_status} />
                    </td>
                    <td className="px-5 py-4 text-sm text-slate-300">
                      {priceDisplay(entry.target_entry_price, entry.market)}
                    </td>
                    <td className="px-5 py-4 text-sm text-slate-300">
                      {priceDisplay(entry.initial_stop_price, entry.market)}
                    </td>
                    <td className="px-5 py-4 text-sm text-slate-300">
                      {priceDisplay(entry.current_stop_price, entry.market)}
                    </td>
                    <td className="px-5 py-4">
                      <WatchlistEarningsBadge ticker={entry.ticker} market={entry.market} />
                    </td>
                    <td className="px-5 py-4">
                      {screenerTickers.has(entry.ticker?.toUpperCase())
                        ? <BookOpen className="w-4 h-4 text-emerald-400" title="Research data available" />
                        : <BookOpen className="w-4 h-4 text-slate-600" title="No research data" />}
                    </td>
                    <td className="px-5 py-4">
                      {entry.market === "US" ? (
                        <button
                          onClick={() => toggleNews(entry)}
                          className="flex items-center gap-1 text-xs text-slate-600 dark:text-slate-400 hover:text-cyan-400 transition-colors"
                          title="Show news headlines"
                        >
                          <Newspaper className="w-3.5 h-3.5" />
                          {expandedNews[entry.ticker]
                            ? <ChevronUp className="w-3 h-3" />
                            : <ChevronDown className="w-3 h-3" />}
                        </button>
                      ) : (
                        <span className="text-slate-600 text-xs">—</span>
                      )}
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => navigate(`/research/${entry.ticker}`)}
                          className="bg-slate-800/50 border-slate-700 text-slate-300 hover:text-cyan-400 hover:border-cyan-500/30 text-xs h-7 px-2.5"
                        >
                          Research
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleAddToPosition(entry)}
                          className="bg-slate-800/50 border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700 text-xs h-7 px-2.5"
                        >
                          Add to Position
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() =>
                            setModal({ mode: "edit-confirm", entry })
                          }
                          className="h-7 w-7 text-slate-600 dark:text-slate-400 hover:text-rose-400 hover:bg-rose-500/10"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                  {expandedNews[entry.ticker] && entry.market === "US" && (
                    <tr key={`${entry.id}-news`} className="bg-slate-800/40">
                      <td colSpan={9} className="px-6 py-3">
                        {newsCache[entry.ticker]?.loading ? (
                          <p className="text-slate-600 dark:text-slate-400 text-xs animate-pulse">Loading headlines…</p>
                        ) : newsCache[entry.ticker]?.headlines?.length > 0 ? (
                          <ul className="space-y-1.5">
                            {newsCache[entry.ticker].headlines.map((h, i) => (
                              <li key={i} className="flex flex-col gap-0.5">
                                {h.url ? (
                                  <a href={h.url} target="_blank" rel="noopener noreferrer" className="text-slate-200 text-xs hover:text-blue-400 hover:underline">{h.headline}</a>
                                ) : (
                                  <span className="text-slate-200 text-xs">{h.headline}</span>
                                )}
                                <span className="text-slate-600 dark:text-slate-400 text-xs">
                                  {h.source ? `${h.source} · ` : ""}
                                  {h.published_at
                                    ? new Date(h.published_at).toLocaleDateString()
                                    : ""}
                                </span>
                              </li>
                            ))}
                          </ul>
                        ) : (
                          <p className="text-slate-600 dark:text-slate-400 text-xs">No recent news available for {entry.ticker}.</p>
                        )}
                        <button
                          onClick={() => setExpandedNews((prev) => ({ ...prev, [entry.ticker]: false }))}
                          className="mt-2 text-slate-600 dark:text-slate-400 hover:text-slate-300 text-xs underline"
                        >
                          Close
                        </button>
                      </td>
                    </tr>
                  )}
                  </>
                ))}
              </tbody>
            </table>
          </div>
        </DataState>
      </div>

      {modal && (
        <WatchlistModal
          mode={modal.mode}
          entry={modal.entry || null}
          onClose={() => setModal(null)}
          onAdded={handleAdded}
          onUpdated={handleUpdated}
          onDeleted={handleDeleted}
        />
      )}
    </div>
  );
}
