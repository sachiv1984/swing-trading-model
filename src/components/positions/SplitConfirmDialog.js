// ST-27 (BLG-BE-223, EPIC-05, v9.18): a detected stock split on an open position.
// Spec: positions.md §Split Detected State (v2.30; odd-lot count v2.31).
// Rule: strategy_rules.md §9.1. Design: docs/design/2026-11-18__release-v9.18/
// position-data-states/decision_record.md §2. Display and a user-confirmed data
// correction only (§13): the dialog states the arithmetic and recommends nothing.
// The figures come from GET /positions `split_pending` (position_endpoints.md v2.23.0).
import { useEffect, useId, useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { format } from "date-fns";
import { toast } from "sonner";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "../ui/dialog";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { apiFetch } from "../../api/base44Client";
import { formatCurrency, currencyForMarket } from "../../lib/format";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const SOURCE_LABELS = { yahoo: "Yahoo Finance" };

export function splitSourceLabel(source) {
  return SOURCE_LABELS[source] || source || "market data";
}

export function formatSplitDate(isoDate) {
  if (!isoDate) return "—";
  const d = new Date(`${String(isoDate).slice(0, 10)}T00:00:00`);
  return Number.isNaN(d.getTime()) ? String(isoDate) : format(d, "d MMM yyyy");
}

// positions.md §Split Detected State: the expanded row's one line.
export function splitPausedLine(split) {
  if (!split) return null;
  return `${split.ratio_label} split on ${formatSplitDate(split.effective_date)} (${splitSourceLabel(split.source)}). ` +
    "Stop alerts and exit suggestions are paused for this position until you confirm.";
}

// The Action needed line: a link-styled button that opens the dialog.
// onOpen(position, triggerElement): the dialog returns focus to the trigger on close.
export function SplitDetectedButton({ position, onOpen }) {
  return (
    <button
      type="button"
      data-testid={`split-detected-${position.ticker}`}
      onClick={(e) => onOpen(position, e.currentTarget)}
      className="text-xs font-medium text-app-warning underline underline-offset-2 hover:no-underline text-left"
    >
      Split detected — confirm adjustment
    </button>
  );
}

function shareText(n) {
  if (n == null || Number.isNaN(Number(n))) return "—";
  return Number(n).toLocaleString("en-GB", { maximumFractionDigits: 4 });
}

// returnFocusTo: the element that opened the dialog. The dialog is controlled
// (no Radix DialogTrigger), so Radix has nothing to restore focus to on its own
// (LL-v8.3-P3-02); onCloseAutoFocus sends focus back explicitly.
export default function SplitConfirmDialog({ position, open, onClose, returnFocusTo }) {
  const split = position?.split_pending || null;
  const currency = currencyForMarket(position?.market);
  const queryClient = useQueryClient();
  const sharesId = useId();
  const sharesHintId = useId();
  const [sharesInput, setSharesInput] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    if (open) {
      setSharesInput("");
      setError(null);
    }
  }, [open, split?.id]);

  const isWhole = split?.shares_after_is_whole === true;
  const enteredShares = sharesInput.trim() === "" ? null : Number(sharesInput);
  const sharesAfter = isWhole ? split?.shares_after : enteredShares;
  const sharesValid = isWhole || (enteredShares != null && Number.isFinite(enteredShares) && enteredShares > 0);
  const costAfter =
    sharesAfter != null && split?.entry_after != null && Number.isFinite(sharesAfter) ? sharesAfter * split.entry_after : null;

  const confirm = useMutation({
    mutationFn: async () => {
      const body = isWhole ? {} : { shares: enteredShares };
      const res = await apiFetch(`${API_BASE}/positions/${position.id}/split-adjustment/confirm`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const json = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(json?.detail || json?.message || "The split could not be confirmed. Please try again.");
      return json?.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
      toast.success(`${position.ticker} ${split.ratio_label} split applied.`);
      onClose();
    },
    onError: (e) => setError(e.message),
  });

  if (!split) return null;

  const rows = [
    { label: "Shares", before: shareText(split.shares_before), after: isWhole ? shareText(split.shares_after) : shareText(enteredShares) },
    { label: "Entry price", before: formatCurrency(split.entry_before, { currency }), after: formatCurrency(split.entry_after, { currency }) },
    { label: "Stop", before: formatCurrency(split.stop_before, { currency }), after: formatCurrency(split.stop_after, { currency }) },
  ];

  return (
    <Dialog open={open} onOpenChange={(next) => { if (!next) onClose(); }}>
      <DialogContent
        data-testid="split-confirm-dialog"
        onCloseAutoFocus={(e) => {
          if (returnFocusTo && document.contains(returnFocusTo)) {
            e.preventDefault();
            returnFocusTo.focus();
          }
        }}
        className="bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white max-w-md"
      >
        <DialogHeader>
          <DialogTitle>{`Confirm ${position.ticker} ${split.ratio_label} split`}</DialogTitle>
          <DialogDescription className="text-slate-600 dark:text-slate-400">
            {splitPausedLine(split)}
          </DialogDescription>
        </DialogHeader>

        <table className="w-full text-sm" data-testid="split-before-after">
          <caption className="sr-only">Before and after the split</caption>
          <thead>
            <tr className="text-xs text-app-muted">
              <th scope="col" className="text-left font-medium py-1"> </th>
              <th scope="col" className="text-right font-medium py-1">Before</th>
              <th scope="col" className="text-right font-medium py-1">After</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.label} className="border-t border-slate-200 dark:border-slate-800">
                <th scope="row" className="text-left font-normal py-1.5 text-app-muted">{r.label}</th>
                <td className="text-right py-1.5">{r.before}</td>
                <td className="text-right py-1.5 font-medium">{r.after}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {!isWhole && (
          <div className="space-y-1">
            <label htmlFor={sharesId} className="text-sm font-medium">Post-split shares</label>
            <Input
              id={sharesId}
              data-testid="split-shares-input"
              inputMode="decimal"
              value={sharesInput}
              onChange={(e) => setSharesInput(e.target.value)}
              aria-describedby={sharesHintId}
              placeholder={shareText(split.shares_after_exact)}
            />
            <p id={sharesHintId} className="text-xs text-app-muted">
              {`${shareText(split.shares_before)} × ${split.ratio_label} is ${shareText(split.shares_after_exact)}, not a whole number. `}
              Enter the share count your broker shows.
            </p>
          </div>
        )}

        <p className="text-sm" data-testid="split-cost-line">
          {isWhole
            ? `Cost unchanged: ${formatCurrency(split.cost_before, { currency })}`
            : costAfter != null
              ? `Cost: ${formatCurrency(split.cost_before, { currency })} → ${formatCurrency(costAfter, { currency })} (cash in lieu: ${formatCurrency(split.cost_before - costAfter, { currency })})`
              : `Cost before: ${formatCurrency(split.cost_before, { currency })}`}
        </p>

        {error && (
          <p role="alert" className="text-sm text-rose-700 dark:text-rose-400" data-testid="split-confirm-error">{error}</p>
        )}

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button
            data-testid="split-confirm-button"
            onClick={() => confirm.mutate()}
            disabled={!sharesValid || confirm.isPending}
          >
            Confirm adjustment
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
