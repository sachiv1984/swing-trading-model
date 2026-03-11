import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Loader2, BookOpen, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { base44 } from "@/api/base44Client";
import { differenceInDays, format } from "date-fns";

const REFLECTION_FIELDS = [
  { id: "trade_rationale",       label: "Why did you enter this trade? What was the setup?" },
  { id: "what_worked",           label: "What did the trade do well? Was the setup validated?" },
  { id: "what_didnt_work",       label: "What went wrong or was unexpected?" },
  { id: "discipline_assessment", label: "Did you follow your rules? Any impulse decisions?" },
  { id: "key_takeaway",          label: "One lesson from this trade." },
];

const MAX_CHARS = 500;

function calcRMultiple(trade) {
  if (!trade.stop_price || !trade.entry_price || trade.entry_price === trade.stop_price) return null;
  const riskPerShare = Math.abs(trade.entry_price - trade.stop_price);
  const pnlPerShare = (trade.pnl || 0) / (trade.shares || 1);
  return pnlPerShare / riskPerShare;
}

function formatExitReason(reason) {
  const map = { stop_hit: "STOP", manual: "MANUAL", target: "TARGET", market_regime: "REGIME" };
  return map[reason] || (reason || "—").toUpperCase();
}

function SummaryRow({ label, value }) {
  return (
    <div className="flex flex-col">
      <span className="text-xs text-slate-500 mb-0.5">{label}</span>
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

  // Pre-populate reflection fields if an existing reflection exists for this trade
  useEffect(() => {
    if (!open || !trade) return;
    setFields({ trade_rationale: "", what_worked: "", what_didnt_work: "", discipline_assessment: "", key_takeaway: "" });
    setError(null);
    setSaved(false);

    // Try to load existing reflection
    base44.entities.TradeReflection.filter({ trade_id: trade.id })
      .then((results) => {
        if (results && results.length > 0) {
          const r = results[0];
          setFields({
            trade_rationale:      r.trade_rationale || "",
            what_worked:          r.what_worked || "",
            what_didnt_work:      r.what_didnt_work || "",
            discipline_assessment: r.discipline_assessment || "",
            key_takeaway:         r.key_takeaway || "",
          });
        }
      });
  }, [open, trade?.id]);

  if (!trade) return null;

  const holdDays = trade.entry_date && trade.exit_date
    ? differenceInDays(new Date(trade.exit_date), new Date(trade.entry_date))
    : null;

  const rMultiple = calcRMultiple(trade);

  const exitDateFormatted = trade.exit_date
    ? format(new Date(trade.exit_date), "dd MMM yyyy")
    : null;

  const currencySymbol = trade.market === "UK" ? "£" : "$";

  const handleFieldChange = (id, value) => {
    if (value.length <= MAX_CHARS) {
      setFields(prev => ({ ...prev, [id]: value }));
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);

    const reflectionData = {
      trade_id:              trade.id,
      ticker:                trade.ticker,
      entry_price:           trade.entry_price,
      exit_price:            trade.exit_price,
      exit_reason:           trade.exit_reason,
      exit_date:             trade.exit_date,
      hold_days:             holdDays,
      r_multiple:            rMultiple,
      pnl:                   trade.pnl,
      market:                trade.market,
      trade_rationale:       fields.trade_rationale || null,
      what_worked:           fields.what_worked || null,
      what_didnt_work:       fields.what_didnt_work || null,
      discipline_assessment: fields.discipline_assessment || null,
      key_takeaway:          fields.key_takeaway || null,
    };

    // Check if existing reflection to update vs create
    const existing = await base44.entities.TradeReflection.filter({ trade_id: trade.id });
    if (existing && existing.length > 0) {
      await base44.entities.TradeReflection.update(existing[0].id, reflectionData);
    } else {
      await base44.entities.TradeReflection.create(reflectionData);
    }

    setSaving(false);
    setSaved(true);
    setTimeout(() => {
      onClose();
    }, 1200);
  };

  return (
    <Dialog open={open} onOpenChange={(v) => { if (!v && !saving) onClose(); }}>
      <DialogContent
        aria-label={`Trade Reflection — ${trade.ticker}`}
        className="bg-slate-900 border-slate-700 text-white max-w-2xl max-h-[92vh] flex flex-col"
      >
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-cyan-400">
            <BookOpen className="w-5 h-5" />
            Trade Reflection — <span className="font-bold">{trade.ticker}</span>
          </DialogTitle>
          <p className="text-xs text-slate-500 mt-0.5">
            Reflect on this trade to reinforce discipline and learning.
          </p>
        </DialogHeader>

        <div className="overflow-y-auto flex-1 space-y-6 pr-1">
          {/* Trade Summary */}
          <div className="rounded-xl bg-slate-800/60 border border-slate-700/50 p-4">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
              Trade Summary
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <SummaryRow label="Ticker" value={<span className="text-cyan-400 font-bold">{trade.ticker}</span>} />
              <SummaryRow label="Entry Price" value={trade.entry_price != null ? `${currencySymbol}${trade.entry_price.toFixed(2)}` : null} />
              <SummaryRow label="Exit Price" value={trade.exit_price != null ? `${currencySymbol}${trade.exit_price.toFixed(2)}` : null} />
              <SummaryRow label="Hold Time" value={holdDays != null ? `${holdDays} day${holdDays !== 1 ? "s" : ""}` : null} />
              <SummaryRow
                label="R-Multiple"
                value={rMultiple != null ? (
                  <span className={rMultiple >= 0 ? "text-emerald-400" : "text-rose-400"}>
                    {rMultiple >= 0 ? "+" : ""}{rMultiple.toFixed(2)}R
                  </span>
                ) : null}
              />
              <SummaryRow label="Exit Reason" value={formatExitReason(trade.exit_reason)} />
              <SummaryRow
                label="P&L"
                value={trade.pnl != null ? (
                  <span className={trade.pnl >= 0 ? "text-emerald-400" : "text-rose-400"}>
                    {trade.pnl >= 0 ? "+" : ""}£{trade.pnl.toFixed(2)}
                  </span>
                ) : null}
              />
              <SummaryRow label="Exit Date" value={exitDateFormatted} />
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
            className="text-slate-400 hover:text-white hover:bg-slate-800"
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
