import { useState, useEffect, useCallback } from "react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Label } from "../../components/ui/label";
import { BellPlus, Trash2 } from "lucide-react";
import { cn } from "../../lib/utils";
import { apiFetch } from "../../api/base44Client";

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const TICKER_RE = /^[A-Z0-9.]{1,10}$/;

function formatThresholdPrice(ticker, price) {
  const isUK = (ticker || "").toUpperCase().endsWith(".L");
  const symbol = isUK ? "£" : "$";
  return `${symbol}${Number(price).toFixed(2)}`;
}

function ConditionText({ alert }) {
  const label = alert.condition === "above" ? "Above" : "Below";
  return (
    <span className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
      {label} {formatThresholdPrice(alert.ticker, alert.threshold_price)}
    </span>
  );
}

function StatusBadge({ alert }) {
  if (alert.active) {
    return (
      <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400">
        Active
      </span>
    );
  }
  return (
    <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-slate-700/50 text-slate-600 dark:text-slate-400">
      Triggered
    </span>
  );
}

function SkeletonRows() {
  return (
    <>
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="flex items-center justify-between px-6 py-5">
          <div className="space-y-2">
            <div className="h-4 w-24 bg-slate-700 rounded animate-pulse" />
            <div className="h-3 w-32 bg-slate-800 rounded animate-pulse" />
          </div>
          <div className="h-7 w-14 bg-slate-700 rounded animate-pulse" />
        </div>
      ))}
    </>
  );
}

function CreateForm({ onSave, onCancel }) {
  const [ticker, setTicker] = useState("");
  const [tickerError, setTickerError] = useState("");
  const [condition, setCondition] = useState("above");
  const [threshold, setThreshold] = useState("");
  const [thresholdError, setThresholdError] = useState("");
  const [saveError, setSaveError] = useState(null);
  const [saving, setSaving] = useState(false);

  const handleTickerChange = (val) => {
    const upper = val.toUpperCase();
    setTicker(upper);
    if (upper && !TICKER_RE.test(upper)) {
      setTickerError("Invalid format. Use 1–10 alphanumeric characters.");
    } else {
      setTickerError("");
    }
  };

  const handleThresholdChange = (val) => {
    setThreshold(val);
    if (val === "") {
      setThresholdError("");
      return;
    }
    const n = Number(val);
    if (isNaN(n) || n <= 0) {
      setThresholdError("Threshold must be a positive number.");
    } else {
      setThresholdError("");
    }
  };

  const handleSubmit = async () => {
    if (!ticker) { setTickerError("Ticker is required."); return; }
    if (!TICKER_RE.test(ticker)) { setTickerError("Invalid format."); return; }
    const n = Number(threshold);
    if (threshold === "" || isNaN(n) || n <= 0) {
      setThresholdError("Threshold must be a positive number.");
      return;
    }

    setSaveError(null);
    setSaving(true);
    try {
      const res = await apiFetch(`${API_BASE_URL}/price-alerts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker, condition, threshold_price: n }),
      });
      if (res.status === 400) {
        const json = await res.json().catch(() => ({}));
        // ST-08 (EPIC-02, v8.3, BLG-BE-69): canonical error envelope uses "message", not "detail".
        const detail = json.message || "";
        if (detail.toLowerCase().includes("maximum number")) {
          setSaveError("You've reached the maximum number of active price alerts.");
        } else {
          setSaveError("Failed to create price alert. Please try again.");
        }
        setSaving(false);
        return;
      }
      if (!res.ok) throw new Error();
      onSave();
    } catch {
      setSaveError("Failed to create price alert. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="px-6 py-5 bg-slate-800/40 border-t border-slate-700/50 space-y-4">
      <div className="space-y-1">
        <Label className="text-slate-600 dark:text-slate-400 text-xs">Ticker Symbol</Label>
        <Input
          value={ticker}
          onChange={(e) => handleTickerChange(e.target.value)}
          placeholder="e.g. AAPL"
          className={cn(
            "bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-600 dark:text-slate-400 h-9 w-40",
            tickerError && "!border-rose-500/60"
          )}
        />
        {tickerError && <p className="text-xs text-rose-700 dark:text-rose-400">{tickerError}</p>}
      </div>

      <div className="space-y-1">
        <Label className="text-slate-600 dark:text-slate-400 text-xs">Condition</Label>
        <div className="flex gap-2">
          {["above", "below"].map((c) => (
            <button
              key={c}
              type="button"
              onClick={() => setCondition(c)}
              className={cn(
                "px-4 py-2 rounded-lg text-sm font-medium border transition-all capitalize",
                condition === c
                  ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 border-cyan-500/40 text-cyan-400"
                  : "bg-slate-800/50 border-slate-700 text-slate-600 dark:text-slate-400"
              )}
            >
              {c}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-1.5">
        <Label className="text-slate-600 dark:text-slate-400 text-xs">Threshold Price</Label>
        <Input
          type="text"
          inputMode="decimal"
          value={threshold}
          onChange={(e) => handleThresholdChange(e.target.value)}
          placeholder="0.00"
          className={cn(
            "bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-600 dark:text-slate-400 h-9 w-40",
            thresholdError && "!border-rose-500/60"
          )}
        />
        {thresholdError && <p className="text-xs text-rose-700 dark:text-rose-400">{thresholdError}</p>}
      </div>

      {saveError && <p className="text-xs text-rose-700 dark:text-rose-400">{saveError}</p>}

      <div className="flex gap-2">
        <Button
          onClick={handleSubmit}
          disabled={saving || !!tickerError || !!thresholdError}
          className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 h-8 text-xs"
        >
          {saving ? "Saving…" : "Save"}
        </Button>
        <Button
          variant="ghost"
          onClick={onCancel}
          className="text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800 h-8 text-xs"
        >
          Cancel
        </Button>
      </div>
    </div>
  );
}

function DeleteConfirmRow({ alert, onDeleted, onCancel }) {
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    setDeleting(true);
    try {
      const res = await apiFetch(`${API_BASE_URL}/price-alerts/${alert.id}`, { method: "DELETE" });
      if (!res.ok) throw new Error();
      onDeleted(alert.id);
    } catch {
      setDeleting(false);
    }
  };

  return (
    <div className="px-6 py-4 bg-slate-800/40 border-t border-slate-700/50 space-y-3">
      <p className="text-sm text-slate-300">
        Delete price alert for <span className="font-semibold text-white">{alert.ticker}</span>?
      </p>
      <div className="flex gap-2">
        <Button
          onClick={handleDelete}
          disabled={deleting}
          className="bg-rose-600 hover:bg-rose-500 text-white border-0 h-8 text-xs"
        >
          {deleting ? "Deleting…" : "Delete"}
        </Button>
        <Button
          variant="ghost"
          onClick={onCancel}
          className="text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800 h-8 text-xs"
        >
          Cancel
        </Button>
      </div>
    </div>
  );
}

export default function CustomPriceAlertsSection() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);

  const fetchAlerts = useCallback(async () => {
    setLoadError(false);
    try {
      const res = await apiFetch(`${API_BASE_URL}/price-alerts`);
      if (!res.ok) throw new Error();
      const json = await res.json();
      setAlerts(json.data);
    } catch {
      setLoadError(true);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchAlerts(); }, [fetchAlerts]);

  const handleCreated = async () => {
    setShowCreateForm(false);
    setLoading(true);
    await fetchAlerts();
  };

  const handleDeleted = (id) => {
    setConfirmDeleteId(null);
    setAlerts((prev) => prev.filter((a) => a.id !== id));
  };

  return (
    <div className="space-y-4">
      <div className="px-1 flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-white">Custom Price Alerts</h2>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-0.5">
            Get notified when a ticker crosses a price you choose.
          </p>
        </div>
        {!loading && alerts.length > 0 && !showCreateForm && (
          <Button
            onClick={() => setShowCreateForm(true)}
            className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 h-8 text-xs"
          >
            Add price alert
          </Button>
        )}
      </div>

      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 divide-y divide-slate-700/50 overflow-hidden">
        {loadError ? (
          <div className="p-6 text-rose-400 text-sm">
            Unable to load price alerts. Please refresh.
          </div>
        ) : loading ? (
          <SkeletonRows />
        ) : alerts.length === 0 ? (
          <>
            <div className="flex flex-col items-center justify-center py-16 text-center px-6">
              <BellPlus className="w-10 h-10 text-slate-600 mb-3" />
              <h3 className="text-base font-semibold text-white mb-1">No custom price alerts.</h3>
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-5">
                Create an alert to be notified when a ticker crosses a price you choose.
              </p>
              {!showCreateForm && (
                <Button
                  onClick={() => setShowCreateForm(true)}
                  className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 h-8 text-xs"
                >
                  Add price alert
                </Button>
              )}
            </div>
            {showCreateForm && (
              <CreateForm onSave={handleCreated} onCancel={() => setShowCreateForm(false)} />
            )}
          </>
        ) : (
          <>
            {showCreateForm && (
              <CreateForm onSave={handleCreated} onCancel={() => setShowCreateForm(false)} />
            )}
            {alerts.map((alert) => (
              <div key={alert.id}>
                <div className="flex items-center justify-between px-6 py-4">
                  <div className="flex flex-col">
                    <span className="text-sm font-semibold text-white">{alert.ticker}</span>
                    <ConditionText alert={alert} />
                  </div>
                  <div className="flex items-center gap-3">
                    <StatusBadge alert={alert} />
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => setConfirmDeleteId(alert.id)}
                      className="h-7 w-7 text-slate-600 dark:text-slate-400 hover:text-rose-400 hover:bg-rose-500/10"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </Button>
                  </div>
                </div>
                {confirmDeleteId === alert.id && (
                  <DeleteConfirmRow
                    alert={alert}
                    onDeleted={handleDeleted}
                    onCancel={() => setConfirmDeleteId(null)}
                  />
                )}
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}
