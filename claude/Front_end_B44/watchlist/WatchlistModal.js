import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const TICKER_RE = /^[A-Z0-9.]{1,10}$/;

export default function WatchlistModal({ mode, entry, onClose, onAdded, onUpdated, onDeleted }) {
  const isEdit = mode === "edit" || mode === "edit-confirm";

  const [form, setForm] = useState({
    ticker: entry?.ticker || "",
    market: entry?.market || "UK",
    target_entry_price: entry?.target_entry_price ?? "",
    initial_stop_price: entry?.initial_stop_price ?? "",
    current_stop_price: entry?.current_stop_price ?? "",
  });

  const [tickerError, setTickerError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(mode === "edit-confirm");
  const [deleting, setDeleting] = useState(false);

  const handleTickerChange = (val) => {
    const upper = val.toUpperCase();
    setForm((f) => ({ ...f, ticker: upper }));
    if (upper && !TICKER_RE.test(upper)) {
      setTickerError("Invalid format. Use 1–10 alphanumeric characters.");
    } else {
      setTickerError("");
    }
  };

  const handleSubmit = async () => {
    if (!form.ticker) { setTickerError("Ticker is required."); return; }
    if (!TICKER_RE.test(form.ticker)) { setTickerError("Invalid format."); return; }

    const body = {
      target_entry_price: form.target_entry_price !== "" ? parseFloat(form.target_entry_price) : null,
      initial_stop_price: form.initial_stop_price !== "" ? parseFloat(form.initial_stop_price) : null,
      current_stop_price: form.current_stop_price !== "" ? parseFloat(form.current_stop_price) : null,
    };

    setSubmitting(true);
    try {
      if (isEdit) {
        const res = await fetch(`${API_BASE}/watchlist/${entry.id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
        if (!res.ok) throw new Error();
        const json = await res.json();
        onUpdated(json.data);
      } else {
        const res = await fetch(`${API_BASE}/watchlist`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ticker: form.ticker, market: form.market, ...body }),
        });
        if (res.status === 409) {
          setTickerError("This ticker is already on your watchlist.");
          setSubmitting(false);
          return;
        }
        if (!res.ok) throw new Error();
        const json = await res.json();
        onAdded(json.data);
      }
    } catch {
      // Let it fail silently — user can retry
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await fetch(`${API_BASE}/watchlist/${entry.id}`, { method: "DELETE" });
      onDeleted(entry.id);
    } catch {
      setDeleting(false);
    }
  };

  const priceField = (label, key) => (
    <div className="space-y-1.5">
      <Label className="text-slate-400 text-xs">{label}</Label>
      <Input
        type="number"
        step="0.01"
        value={form[key]}
        onChange={(e) => setForm((f) => ({ ...f, [key]: e.target.value }))}
        placeholder="Optional"
        className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 h-9"
      />
    </div>
  );

  return (
    <Dialog open onOpenChange={onClose}>
      <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-md">
        <DialogHeader>
          <DialogTitle className="text-white">
            {isEdit ? `Edit ${entry.ticker}` : "Add Ticker to Watchlist"}
          </DialogTitle>
          <DialogDescription className="text-slate-400">
            {isEdit ? "Update price levels for this ticker." : "Track a new ticker for entry opportunities."}
          </DialogDescription>
        </DialogHeader>

        {confirmDelete ? (
          /* ---- Inline delete confirmation ---- */
          <div className="py-4 space-y-4">
            <p className="text-sm text-slate-300">
              Remove <span className="font-semibold text-white">{entry.ticker}</span> from your watchlist?
            </p>
            <div className="flex gap-3">
              <Button
                onClick={handleDelete}
                disabled={deleting}
                className="bg-rose-600 hover:bg-rose-500 text-white border-0"
              >
                {deleting ? "Removing…" : "Remove"}
              </Button>
              <Button
                variant="ghost"
                onClick={() => setConfirmDelete(false)}
                className="text-slate-400 hover:text-white hover:bg-slate-800"
              >
                Cancel
              </Button>
            </div>
          </div>
        ) : (
          /* ---- Main form ---- */
          <>
            <div className="space-y-4 py-2">
              {/* Ticker */}
              <div className="space-y-1.5">
                <Label className="text-slate-400 text-xs">Ticker Symbol</Label>
                <Input
                  value={form.ticker}
                  onChange={(e) => handleTickerChange(e.target.value)}
                  disabled={isEdit}
                  placeholder="e.g. AAPL"
                  className={cn(
                    "bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 h-9",
                    isEdit && "opacity-50 cursor-not-allowed",
                    tickerError && "border-rose-500/60"
                  )}
                />
                {tickerError && <p className="text-xs text-rose-400">{tickerError}</p>}
              </div>

              {/* Market toggle */}
              <div className="space-y-1.5">
                <Label className="text-slate-400 text-xs">Market</Label>
                <div className="grid grid-cols-2 gap-2">
                  {["UK", "US"].map((m) => (
                    <button
                      key={m}
                      type="button"
                      disabled={isEdit}
                      onClick={() => !isEdit && setForm((f) => ({ ...f, market: m }))}
                      className={cn(
                        "py-2 rounded-lg text-sm font-medium border transition-all",
                        form.market === m
                          ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 border-cyan-500/40 text-cyan-400"
                          : "bg-slate-800/50 border-slate-700 text-slate-400",
                        isEdit && "opacity-50 cursor-not-allowed"
                      )}
                    >
                      {m}
                    </button>
                  ))}
                </div>
              </div>

              {/* Price fields */}
              {priceField("Target Entry Price", "target_entry_price")}
              {priceField("Initial Stop Price", "initial_stop_price")}
              {priceField("Current Stop Price", "current_stop_price")}
            </div>

            <DialogFooter className="flex items-center justify-between gap-2 pt-2">
              <div>
                {isEdit && (
                  <Button
                    variant="ghost"
                    onClick={() => setConfirmDelete(true)}
                    className="text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 px-2"
                  >
                    Remove from Watchlist
                  </Button>
                )}
              </div>
              <div className="flex gap-2">
                <Button
                  variant="ghost"
                  onClick={onClose}
                  className="text-slate-400 hover:text-white hover:bg-slate-800"
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleSubmit}
                  disabled={submitting}
                  className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25"
                >
                  {submitting ? "Saving…" : isEdit ? "Save Changes" : "Add to Watchlist"}
                </Button>
              </div>
            </DialogFooter>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}
