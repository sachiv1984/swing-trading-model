import { useState } from "react";
import { ChevronDown, ChevronRight, Zap, Loader2 } from "lucide-react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { cn } from "../../lib/utils";
import { api } from "../../api/base44Client";

export default function ProspectiveHeatPanel({ currentHeat }) {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ ticker: "", shares: "", entry_price: "", stop_price: "" });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [apiError, setApiError] = useState(null);

  const validate = () => {
    const e = {};
    if (!form.ticker.trim()) e.ticker = "Required";
    const shares = parseFloat(form.shares);
    if (isNaN(shares) || shares <= 0) e.shares = "Must be > 0";
    const entry = parseFloat(form.entry_price);
    if (isNaN(entry) || entry <= 0) e.entry_price = "Must be > 0";
    const stop = parseFloat(form.stop_price);
    if (isNaN(stop) || stop <= 0) e.stop_price = "Must be > 0";
    else if (stop >= entry) e.stop_price = "Must be less than entry price";
    return e;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    setErrors(errs);
    if (Object.keys(errs).length > 0) return;

    setLoading(true);
    setResult(null);
    setApiError(null);

    try {
      const data = await api.portfolio.prospectiveHeat(
        form.ticker.trim(),
        form.shares,
        form.entry_price,
        form.stop_price
      );
      setResult(data);
    } catch (err) {
      setApiError(err?.message || `Server error ${err?.status ?? ''}`);
    } finally {
      setLoading(false);
    }
  };

  const delta = result?.projected_heat_percent != null && currentHeat != null
    ? result.projected_heat_percent - currentHeat
    : null;

  const heatThreshold = (pct) => {
    if (pct >= 30) return { label: "Extreme", color: "text-rose-400 bg-rose-500/20 border-rose-500/40" };
    if (pct >= 20) return { label: "High",    color: "text-orange-400 bg-orange-500/20 border-orange-500/40" };
    if (pct >= 10) return { label: "Moderate", color: "text-amber-400 bg-amber-500/20 border-amber-500/40" };
    return             { label: "Low",        color: "text-emerald-400 bg-emerald-500/20 border-emerald-500/40" };
  };
  const threshold = result?.projected_heat_percent != null ? heatThreshold(result.projected_heat_percent) : null;

  const field = (id, label, placeholder, type = "text") => (
    <div className="space-y-1">
      <Label htmlFor={id} className="text-xs text-slate-600 dark:text-slate-400">{label}</Label>
      <Input
        id={id}
        type={type === "number" ? "number" : "text"}
        step="any"
        min={type === "number" ? "0" : undefined}
        placeholder={placeholder}
        value={form[id]}
        onChange={(e) => {
          // XSS: only alphanumeric / decimal for numeric fields
          const val = type === "number" ? e.target.value.replace(/[^0-9.]/g, "") : e.target.value.replace(/[^a-zA-Z0-9.]/g, "");
          setForm((f) => ({ ...f, [id]: val }));
          setErrors((ev) => { const n = { ...ev }; delete n[id]; return n; });
        }}
        className={cn("bg-slate-900/50 border-slate-700 text-slate-200 text-sm h-9",
          errors[id] && "border-rose-500/70")}
      />
      {errors[id] && <p className="text-xs text-rose-700 dark:text-rose-400">{errors[id]}</p>}
    </div>
  );

  return (
    <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center gap-3 p-5 hover:bg-slate-800/30 transition-colors text-left"
      >
        <div className="p-2 rounded-lg bg-gradient-to-br from-cyan-500/30 to-violet-500/30">
          <Zap className="w-5 h-5 text-cyan-400" />
        </div>
        <span className="text-sm font-medium text-slate-300">Prospective Heat Calculator</span>
        <span className="ml-auto">
          {open ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
        </span>
      </button>

      {open && (
        <div className="px-5 pb-5 border-t border-slate-700/30">
          <form onSubmit={handleSubmit} className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-4">
            {field("ticker", "Ticker", "e.g. AAPL")}
            {field("shares", "Shares", "100", "number")}
            {field("entry_price", "Entry Price", "150.00", "number")}
            {field("stop_price", "Stop Price", "140.00", "number")}
            <div className="col-span-2 sm:col-span-4 flex items-center gap-4 mt-1">
              <Button
                type="submit"
                disabled={loading}
                className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-600 hover:to-violet-600 text-white h-9 px-6"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Calculate"}
              </Button>

              {apiError && <p className="text-sm text-rose-700 dark:text-rose-400">{apiError}</p>}

              {result && !apiError && (
                <div className="flex items-center gap-4 text-sm">
                  <div>
                    <span className="text-slate-600 dark:text-slate-400 text-xs">Projected Heat</span>
                    <div className="flex items-center gap-2">
                      <p className="font-bold text-white">{result.projected_heat_percent?.toFixed(1)}%</p>
                      {threshold && (
                        <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${threshold.color}`}>
                          {threshold.label}
                        </span>
                      )}
                    </div>
                  </div>
                  {delta !== null && (
                    <div>
                      <span className="text-slate-600 dark:text-slate-400 text-xs">Delta</span>
                      <p className={cn("font-bold", delta > 0 ? "text-rose-400" : "text-emerald-400")}>
                        {delta > 0 ? "+" : ""}{delta.toFixed(1)}%
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
