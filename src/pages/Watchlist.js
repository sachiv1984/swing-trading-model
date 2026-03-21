import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, Trash2 } from "lucide-react";
import PageHeader from "../components/ui/PageHeader";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "../components/ui/dialog";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { cn } from "../lib/utils";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// ─── Helpers ─────────────────────────────────────────────────────────────────

function SignalBadge({ status }) {
  const config = {
    active: {
      label: "Active",
      cls: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
    },
    watch: {
      label: "Watch",
      cls: "bg-amber-500/20 text-amber-400 border-amber-500/30",
    },
    no_signal: {
      label: "No Signal",
      cls: "bg-slate-700/50 text-slate-400 border-slate-600/30",
    },
  };
  const { label, cls } = config[status] || config.no_signal;
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${cls}`}
    >
      {label}
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
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${cls}`}
    >
      {market}
    </span>
  );
}

function formatPrice(value, market) {
  if (value == null) return "—";
  const symbol = market === "UK" ? "£" : "$";
  return `${symbol}${Number(value).toFixed(2)}`;
}

// ─── Add / Edit Modal ─────────────────────────────────────────────────────────

const EMPTY_FORM = {
  ticker: "",
  market: "UK",
  target_entry_price: "",
  initial_stop_price: "",
  current_stop_price: "",
};

function WatchlistModal({ open, onClose, onSave, onDelete, editEntry, removeMode }) {
  const isEdit = !!editEntry;
  const [form, setForm] = useState(EMPTY_FORM);
  const [tickerError, setTickerError] = useState("");
  const [saving, setSaving] = useState(false);
  const [showRemoveConfirm, setShowRemoveConfirm] = useState(false);
  const [removing, setRemoving] = useState(false);

  useEffect(() => {
    if (open) {
      if (editEntry) {
        setForm({
          ticker: editEntry.ticker,
          market: editEntry.market,
          target_entry_price:
            editEntry.target_entry_price != null
              ? String(editEntry.target_entry_price)
              : "",
          initial_stop_price:
            editEntry.initial_stop_price != null
              ? String(editEntry.initial_stop_price)
              : "",
          current_stop_price:
            editEntry.current_stop_price != null
              ? String(editEntry.current_stop_price)
              : "",
        });
      } else {
        setForm(EMPTY_FORM);
      }
      setTickerError("");
      setShowRemoveConfirm(removeMode || false);
      setSaving(false);
      setRemoving(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, editEntry]);

  const handleSubmit = async () => {
    if (!form.ticker.trim()) {
      setTickerError("Ticker symbol is required.");
      return;
    }
    if (!/^[A-Z0-9.]{1,10}$/.test(form.ticker)) {
      setTickerError("Ticker must be 1–10 alphanumeric characters.");
      return;
    }
    setSaving(true);
    try {
      const payload = {
        ticker: form.ticker,
        market: form.market,
        target_entry_price: form.target_entry_price
          ? parseFloat(form.target_entry_price)
          : null,
        initial_stop_price: form.initial_stop_price
          ? parseFloat(form.initial_stop_price)
          : null,
        current_stop_price: form.current_stop_price
          ? parseFloat(form.current_stop_price)
          : null,
      };
      await onSave(payload, editEntry?.id);
      onClose();
    } catch (err) {
      if (err.status === 409) {
        setTickerError("This ticker is already on your watchlist.");
      }
    } finally {
      setSaving(false);
    }
  };

  const handleRemove = async () => {
    setRemoving(true);
    try {
      await onDelete(editEntry.id);
      onClose();
    } catch {
      setRemoving(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(v) => !v && onClose()}>
      <DialogContent className="bg-slate-900 border border-slate-700 text-white sm:max-w-md">
        <DialogHeader>
          <DialogTitle>
            {isEdit ? "Edit Watchlist Entry" : "Add Ticker"}
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4 py-2">
          {/* Ticker symbol */}
          <div className="space-y-1">
            <Label className="text-slate-300">Ticker symbol</Label>
            <Input
              value={form.ticker}
              onChange={(e) => {
                const v = e.target.value
                  .toUpperCase()
                  .replace(/[^A-Z0-9.]/g, "");
                setForm((p) => ({ ...p, ticker: v }));
                setTickerError("");
              }}
              disabled={isEdit}
              maxLength={10}
              placeholder="e.g. AAPL"
              className={cn(
                "bg-slate-800 border-slate-700 text-white placeholder:text-slate-500",
                isEdit && "opacity-60 cursor-not-allowed",
                tickerError && "border-rose-500"
              )}
            />
            {tickerError && (
              <p className="text-xs text-rose-400">{tickerError}</p>
            )}
          </div>

          {/* Market */}
          <div className="space-y-1">
            <Label className="text-slate-300">Market</Label>
            <div className="flex gap-3">
              {["UK", "US"].map((m) => (
                <button
                  key={m}
                  type="button"
                  disabled={isEdit}
                  onClick={() =>
                    !isEdit && setForm((p) => ({ ...p, market: m }))
                  }
                  className={cn(
                    "flex-1 py-2 rounded-lg text-sm font-medium border transition-colors",
                    form.market === m
                      ? "bg-cyan-500/20 text-cyan-400 border-cyan-500/50"
                      : "bg-slate-800 text-slate-400 border-slate-700 hover:bg-slate-700",
                    isEdit && "opacity-60 cursor-not-allowed"
                  )}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>

          {/* Price fields */}
          {[
            { key: "target_entry_price", label: "Target Entry Price" },
            { key: "initial_stop_price", label: "Initial Stop Price" },
            { key: "current_stop_price", label: "Current Stop Price" },
          ].map(({ key, label }) => (
            <div key={key} className="space-y-1">
              <Label className="text-slate-300">
                {label}{" "}
                <span className="text-slate-500">(optional)</span>
              </Label>
              <Input
                type="number"
                step="0.01"
                min="0"
                value={form[key]}
                onChange={(e) =>
                  setForm((p) => ({ ...p, [key]: e.target.value }))
                }
                placeholder="—"
                className="bg-slate-800 border-slate-700 text-white placeholder:text-slate-500"
              />
            </div>
          ))}
        </div>

        {/* Remove confirmation (edit mode only) */}
        {isEdit && showRemoveConfirm && (
          <div className="rounded-lg bg-rose-950/50 border border-rose-800/50 p-4 space-y-3">
            <p className="text-sm text-rose-300">
              Remove{" "}
              <span className="font-semibold text-white">
                {editEntry.ticker}
              </span>{" "}
              from your watchlist?
            </p>
            <div className="flex gap-2">
              <Button
                variant="destructive"
                size="sm"
                onClick={handleRemove}
                disabled={removing}
                className="bg-rose-600 hover:bg-rose-700"
              >
                {removing ? "Removing…" : "Remove"}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowRemoveConfirm(false)}
                className="bg-slate-800 border-slate-600 text-slate-300 hover:bg-slate-700"
              >
                Cancel
              </Button>
            </div>
          </div>
        )}

        <DialogFooter className="flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          {isEdit && !showRemoveConfirm && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowRemoveConfirm(true)}
              className="text-rose-400 hover:text-rose-300 hover:bg-rose-950/50 self-start"
            >
              <Trash2 className="w-4 h-4 mr-1" />
              Remove from Watchlist
            </Button>
          )}
          <div className="flex gap-2 ml-auto">
            <Button
              variant="outline"
              size="sm"
              onClick={onClose}
              className="bg-slate-800 border-slate-600 text-slate-300 hover:bg-slate-700"
            >
              Cancel
            </Button>
            {!showRemoveConfirm && (
              <Button
                size="sm"
                onClick={handleSubmit}
                disabled={saving}
                className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-600 hover:to-violet-600 text-white"
              >
                {saving
                  ? "Saving…"
                  : isEdit
                  ? "Save Changes"
                  : "Add to Watchlist"}
              </Button>
            )}
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

// ─── Sort helper ─────────────────────────────────────────────────────────────

const SIGNAL_ORDER = { active: 1, watch: 2, no_signal: 3 };

function sortEntries(list) {
  return [...list].sort((a, b) => {
    const od =
      (SIGNAL_ORDER[a.signal_status] || 3) -
      (SIGNAL_ORDER[b.signal_status] || 3);
    return od !== 0 ? od : a.ticker.localeCompare(b.ticker);
  });
}

// ─── Main page ────────────────────────────────────────────────────────────────

export default function Watchlist() {
  const navigate = useNavigate();
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editEntry, setEditEntry] = useState(null);
  const [removeMode, setRemoveMode] = useState(false);
  const [removingId, setRemovingId] = useState(null);

  const load = () => {
    setLoading(true);
    setLoadError(false);
    fetch(`${API_BASE_URL}/watchlist`)
      .then((r) => {
        if (!r.ok) throw new Error();
        return r.json();
      })
      .then((json) => {
        setEntries(sortEntries(json.data));
        setLoading(false);
      })
      .catch(() => {
        setLoadError(true);
        setLoading(false);
      });
  };

  useEffect(() => {
    load();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const openAdd = () => {
    setEditEntry(null);
    setRemoveMode(false);
    setModalOpen(true);
  };

  const openEdit = (entry, startRemove = false) => {
    setEditEntry(entry);
    setRemoveMode(startRemove);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setEditEntry(null);
    setRemoveMode(false);
  };

  const handleSave = async (payload, entryId) => {
    if (entryId) {
      // PATCH — ticker and market are read-only; strip them
      const { ticker, market, ...patchPayload } = payload; // eslint-disable-line no-unused-vars
      const r = await fetch(`${API_BASE_URL}/watchlist/${entryId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(patchPayload),
      });
      if (!r.ok) {
        const err = new Error("Failed to update");
        err.status = r.status;
        throw err;
      }
      const json = await r.json();
      setEntries((prev) =>
        sortEntries(prev.map((e) => (e.id === entryId ? json.data : e)))
      );
    } else {
      // POST
      const r = await fetch(`${API_BASE_URL}/watchlist`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!r.ok) {
        const err = new Error("Failed to create");
        err.status = r.status;
        throw err;
      }
      const json = await r.json();
      setEntries((prev) => sortEntries([...prev, json.data]));
    }
  };

  const removeRow = (entryId) => {
    setRemovingId(entryId);
    setTimeout(() => {
      setEntries((prev) => prev.filter((e) => e.id !== entryId));
      setRemovingId(null);
    }, 200);
  };

  const handleDelete = async (entryId) => {
    const r = await fetch(`${API_BASE_URL}/watchlist/${entryId}`, {
      method: "DELETE",
    });
    if (!r.ok) throw new Error("Failed to delete");
    removeRow(entryId);
  };

  const handleAddToPosition = (entry) => {
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
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-start justify-between gap-4">
        <PageHeader
          title="Watchlist"
          description="Monitor tickers for entry opportunities."
        />
        <Button
          onClick={openAdd}
          size="sm"
          className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-600 hover:to-violet-600 text-white shrink-0 mt-1"
        >
          <Plus className="w-4 h-4 mr-1" />
          Add Ticker
        </Button>
      </div>

      {/* Table card */}
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50">
        {loadError ? (
          <div className="flex flex-col items-center justify-center py-16 text-center gap-3">
            <p className="text-sm text-rose-400">
              Unable to load watchlist. Please refresh.
            </p>
            <Button
              variant="outline"
              size="sm"
              onClick={load}
              className="bg-slate-800 border-slate-600 text-slate-300 hover:bg-slate-700"
            >
              Retry
            </Button>
          </div>
        ) : loading ? (
          /* Skeleton */
          <div className="divide-y divide-slate-700/50">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="flex gap-6 px-6 py-4">
                <div className="h-4 w-16 bg-slate-700 rounded animate-pulse" />
                <div className="h-4 w-10 bg-slate-700 rounded animate-pulse" />
                <div className="h-4 w-20 bg-slate-700 rounded animate-pulse" />
                <div className="h-4 w-14 bg-slate-800 rounded animate-pulse" />
                <div className="h-4 w-14 bg-slate-800 rounded animate-pulse" />
                <div className="h-4 w-14 bg-slate-800 rounded animate-pulse ml-auto" />
              </div>
            ))}
          </div>
        ) : entries.length === 0 ? (
          /* Empty state */
          <div className="flex flex-col items-center justify-center py-16 text-center gap-4">
            <p className="text-sm font-medium text-slate-300">
              Your watchlist is empty.
            </p>
            <p className="text-xs text-slate-500">
              Add tickers you're monitoring for entry opportunities.
            </p>
            <Button
              onClick={openAdd}
              size="sm"
              className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-600 hover:to-violet-600 text-white"
            >
              <Plus className="w-4 h-4 mr-1" />
              Add Ticker
            </Button>
          </div>
        ) : (
          /* Table */
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
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
                      className="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wide first:pl-6 last:pr-6"
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/50">
                {entries.map((entry) => (
                  <tr
                    key={entry.id}
                    className={cn(
                      "hover:bg-slate-800/30 transition-all duration-200",
                      removingId === entry.id && "opacity-0"
                    )}
                  >
                    <td className="px-4 py-4 pl-6">
                      <button
                        onClick={() => openEdit(entry)}
                        className="font-medium text-cyan-400 hover:text-cyan-300 transition-colors"
                      >
                        {entry.ticker}
                      </button>
                    </td>
                    <td className="px-4 py-4">
                      <MarketBadge market={entry.market} />
                    </td>
                    <td className="px-4 py-4">
                      <SignalBadge status={entry.signal_status} />
                    </td>
                    <td className="px-4 py-4 text-slate-300">
                      {formatPrice(entry.target_entry_price, entry.market)}
                    </td>
                    <td className="px-4 py-4 text-slate-300">
                      {formatPrice(entry.initial_stop_price, entry.market)}
                    </td>
                    <td className="px-4 py-4 text-slate-300">
                      {formatPrice(entry.current_stop_price, entry.market)}
                    </td>
                    <td className="px-4 py-4 pr-6">
                      <div className="flex items-center gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleAddToPosition(entry)}
                          className="bg-slate-800 border-slate-600 text-slate-300 hover:bg-slate-700 hover:text-white text-xs"
                        >
                          Add to Position
                        </Button>
                        <button
                          onClick={() => openEdit(entry, true)}
                          title="Remove"
                          className="p-1.5 text-slate-500 hover:text-rose-400 transition-colors rounded"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <WatchlistModal
        open={modalOpen}
        onClose={closeModal}
        onSave={handleSave}
        onDelete={handleDelete}
        editEntry={editEntry}
        removeMode={removeMode}
      />
    </div>
  );
}
