import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "../ui/dialog";
import { Button } from "../ui/button";
import { Textarea } from "../ui/textarea";
import { Loader2, BookOpen, CheckCircle2 } from "lucide-react";
import { cn } from "../../lib/utils";
import { api } from "../../api/base44Client";

// Spec: docs/specs/frontend/pages/trade_reflection.md v0.1
// EPIC-01, ST-02, v1.9

const REFLECTION_FIELDS = [
  { id: "trade_rationale",       label: "Why did you enter this trade? What was the setup?" },
  { id: "what_worked",           label: "What did the trade do well? Was the setup validated?" },
  { id: "what_didnt_work",       label: "What went wrong or was unexpected?" },
  { id: "discipline_assessment", label: "Did you follow your rules? Any impulse decisions?" },
  { id: "key_takeaway",          label: "One lesson from this trade." },
];

const MAX_CHARS = 500;

function formatExitReason(reason) {
  const map = { stop_hit: "STOP", manual: "MANUAL", target: "TARGET", market_regime: "REGIME" };
  return map[reason] || (reason ? reason.toUpperCase() : "—");
}

function SummaryRow({ label, value }) {
  return (
    <div className="flex flex-col">
      <span className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">{label}</span>
      <span className="text-sm font-medium text-white">{value ?? "—"}</span>
    </div>
  );
}

export default function TradeReflectionModal({ trade, open, onClose }) {
  const [fields, setFields] = useState({
    trade_rationale: "",
    what_worked: "",
    what_didnt_work: "",
    discipline_assessment: "",
    key_takeaway: "",
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(false);

  // Pre-populate reflection fields if a reflection already exists for this trade
  useEffect(() => {
    if (!open || !trade?.id) return;
    setFields({ trade_rationale: "", what_worked: "", what_didnt_work: "", discipline_assessment: "", key_takeaway: "" });
    setError(null);
    setSaved(false);

    api.trades.getReflection(trade.id)
      .then((data) => {
        if (data) {
          setFields({
            trade_rationale:       data.trade_rationale || "",
            what_worked:           data.what_worked || "",
            what_didnt_work:       data.what_didnt_work || "",
            discipline_assessment: data.discipline_assessment || "",
            key_takeaway:          data.key_takeaway || "",
          });
        }
      })
      .catch(() => {}); // 404 = no reflection saved yet; fields stay empty
  }, [open, trade?.id]);

  if (!trade) return null;

  // All summary values are backend-sourced — do not compute on frontend (spec §4 hard rule)
  const holdDays = trade.holding_days ?? null;
  const rMultiple = trade.r_multiple ?? null;
  const exitState = trade.exit_state ?? null;
  const currencySymbol = trade.market === "UK" ? "£" : "$";

  const exitDateFormatted = trade.exit_date
    ? new Date(trade.exit_date).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" })
    : null;

  const handleFieldChange = (id, value) => {
    if (value.length <= MAX_CHARS) {
      setFields((prev) => ({ ...prev, [id]: value }));
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    try {
      await api.trades.saveReflection(trade.id, {
        trade_rationale:       fields.trade_rationale || null,
        what_worked:           fields.what_worked || null,
        what_didnt_work:       fields.what_didnt_work || null,
        discipline_assessment: fields.discipline_assessment || null,
        key_takeaway:          fields.key_takeaway || null,
      });
      setSaved(true);
      setTimeout(() => { onClose(); }, 1200);
    } catch (e) {
      setError("Failed to save reflection. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(v) => { if (!v && !saving) onClose(); }}>
      <DialogContent
        aria-label={`Trade Reflection — ${trade.ticker}`}
        className="bg-slate-900 border-slate-700 text-white !max-w-2xl max-h-[92vh] overflow-hidden !flex !flex-col"
      >
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-cyan-400">
            <BookOpen className="w-5 h-5" />
            Trade Reflection — <span className="font-bold">{trade.ticker}</span>
          </DialogTitle>
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
            Reflect on this trade to reinforce discipline and learning.
          </p>
        </DialogHeader>

        <div className="overflow-y-auto space-y-6 pr-1" style={{ maxHeight: "calc(90vh - 200px)" }}>
          {/* Trade Summary — read-only; all values backend-sourced (spec §4) */}
          <div className="rounded-xl bg-slate-800/60 border border-slate-700/50 p-4">
            <p className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider mb-3">
              Trade Summary
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <SummaryRow label="Ticker" value={<span className="text-cyan-400 font-bold">{trade.ticker}</span>} />
              <SummaryRow label="Entry Price" value={trade.entry_price != null ? `${currencySymbol}${trade.entry_price.toFixed(2)}` : null} />
              <SummaryRow label="Exit Price"  value={trade.exit_price  != null ? `${currencySymbol}${trade.exit_price.toFixed(2)}`  : null} />
              <SummaryRow label="Hold Time"   value={holdDays != null ? `${holdDays} day${holdDays !== 1 ? "s" : ""}` : null} />
              <SummaryRow
                label="R-Multiple"
                value={rMultiple != null ? (
                  <span className={rMultiple >= 0 ? "text-emerald-400" : "text-rose-400"}>
                    {rMultiple >= 0 ? "+" : ""}{rMultiple.toFixed(2)}R
                  </span>
                ) : null}
              />
              <SummaryRow label="Exit Reason" value={formatExitReason(trade.exit_reason)} />
              <SummaryRow label="Exit State"  value={exitState} />
              <SummaryRow label="Exit Date"   value={exitDateFormatted} />
            </div>
          </div>

          {/* Reflection Fields */}
          <div className="space-y-4">
            {REFLECTION_FIELDS.map((field) => (
              <div key={field.id} className="space-y-1.5">
                <label className="text-sm text-slate-300 font-medium">{field.label}</label>
                <Textarea
                  value={fields[field.id]}
                  onChange={(e) => handleFieldChange(field.id, e.target.value)}
                  disabled={saving || saved}
                  placeholder="Optional — write your thoughts here..."
                  className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-600 focus:border-cyan-500/50 resize-none h-24 text-sm"
                  rows={3}
                />
                <div className="flex justify-end">
                  <span className={cn(
                    "text-xs",
                    fields[field.id].length > MAX_CHARS - 50 ? "text-amber-400" : "text-slate-600"
                  )}>
                    {fields[field.id].length}/{MAX_CHARS}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {error && (
            <p className="text-sm text-rose-400 bg-rose-500/10 border border-rose-500/30 rounded-lg px-4 py-2">
              {error}
            </p>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-800 mt-2">
          <Button
            variant="ghost"
            onClick={onClose}
            disabled={saving}
            className="text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800"
          >
            Skip
          </Button>
          <Button
            onClick={handleSave}
            disabled={saving || saved}
            className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 min-w-[140px]"
          >
            {saved ? (
              <><CheckCircle2 className="w-4 h-4 mr-2" />Saved!</>
            ) : saving ? (
              <><Loader2 className="w-4 h-4 mr-2 animate-spin" />Saving...</>
            ) : (
              "Save Reflection"
            )}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
