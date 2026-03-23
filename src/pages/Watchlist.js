import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api/base44Client";
import { Button } from "../components/ui/button";
import PageHeader from "../components/ui/PageHeader";
import { Plus, Trash2, Eye } from "lucide-react";
import { cn } from "../lib/utils";
import WatchlistModal from "../components/watchlist/WatchlistModal";

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
      no_signal: { label: "No Signal", cls: "bg-slate-700/50 text-slate-400 border-slate-600/30" },
    }[status] || { label: status, cls: "bg-slate-700/50 text-slate-400 border-slate-600/30" };
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

function SkeletonTable() {
  return (
    <div className="divide-y divide-slate-700/30">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="flex gap-6 px-5 py-4">
          <div className="h-4 w-16 bg-slate-700 rounded animate-pulse" />
          <div className="h-4 w-12 bg-slate-700 rounded animate-pulse" />
          <div className="h-4 w-20 bg-slate-700 rounded animate-pulse" />
          <div className="h-4 w-16 bg-slate-800 rounded animate-pulse" />
          <div className="h-4 w-16 bg-slate-800 rounded animate-pulse" />
          <div className="h-4 w-16 bg-slate-800 rounded animate-pulse" />
        </div>
      ))}
    </div>
  );
}

function EmptyState({ onAdd }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center px-6">
      <Eye className="w-12 h-12 text-slate-600 mb-4" />
      <h3 className="text-lg font-semibold text-white mb-2">
        Your watchlist is empty.
      </h3>
      <p className="text-sm text-slate-400 mb-6">
        Add tickers you're monitoring for entry opportunities.
      </p>
      <Button
        onClick={onAdd}
        className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25"
      >
        <Plus className="w-4 h-4 mr-2" />
        Add Ticker
      </Button>
    </div>
  );
}

export default function Watchlist() {
  const navigate = useNavigate();
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [removing, setRemoving] = useState({}); // { [id]: true } while fading out
  const [modal, setModal] = useState(null); // null | { mode, entry }

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
        {loadError ? (
          <div className="flex flex-col items-center justify-center py-16 gap-4">
            <p className="text-rose-400 text-sm">
              Unable to load watchlist. Please refresh.
            </p>
            <Button
              variant="outline"
              size="sm"
              onClick={fetchEntries}
              className="bg-slate-800/50 border-slate-700 text-slate-300 hover:text-white"
            >
              Retry
            </Button>
          </div>
        ) : loading ? (
          <SkeletonTable />
        ) : entries.length === 0 ? (
          <EmptyState onAdd={() => setModal({ mode: "add" })} />
        ) : (
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
                    "Actions",
                  ].map((h) => (
                    <th
                      key={h}
                      className="px-5 py-3.5 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider whitespace-nowrap"
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/30">
                {entries.map((entry) => (
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
                        className="text-cyan-400 hover:text-cyan-300 font-semibold text-sm transition-colors"
                      >
                        {entry.ticker}
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
                      <div className="flex items-center gap-2">
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
                          className="h-7 w-7 text-slate-500 hover:text-rose-400 hover:bg-rose-500/10"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
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
