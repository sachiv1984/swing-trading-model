// ST-06 (BLG-FE-193, EPIC-02, v9.10): stop provenance line and per-row stop
// details tooltip. Spec: docs/specs/frontend/pages/positions.md §Stop Provenance
// Line and Per-Row Stop Details. Design source:
// docs/design/2026-10-06__release-v9.10/stop-cell-provenance/decision_record.md
// Display-only (§13): explains an already-computed stop, no action.
import { format } from "date-fns";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "../ui/tooltip";
import { formatCurrency } from "../../lib/format";
import { ATR_PERIOD_DAYS, PROFIT_ATR_MULTIPLIER } from "../../lib/strategyParameters";

function formatMultiplier(m) {
  return Number.isInteger(m) ? `${m}×` : `${m.toFixed(1)}×`;
}

function hasAtr(position) {
  const atr = Number(position?.atr_value);
  return Number.isFinite(atr) && atr > 0;
}

function activeMultiplier(position) {
  const m = position?.active_atr_multiplier;
  return m == null || !Number.isFinite(Number(m)) ? null : Number(m);
}

const ATR_SOURCE_SUFFIX = { fallback: " · estimated", user: " · entered" };

const CALCULATION_SOURCE_LABEL = {
  nightly: "nightly update",
  on_load: "when positions loaded",
};

export function stopProvenanceText(position, currency) {
  const suffix = ATR_SOURCE_SUFFIX[position?.atr_source] ?? "";
  if (!hasAtr(position)) return `ATR unavailable${suffix}`;
  const atr = formatCurrency(position.atr_value, { currency });
  const m = activeMultiplier(position);
  return m == null ? `ATR ${atr}${suffix}` : `${formatMultiplier(m)} ATR ${atr}${suffix}`;
}

export function StopProvenanceLine({ position, currency }) {
  return (
    <span className="text-xs font-normal text-slate-600 dark:text-slate-400" data-testid="stop-provenance">
      {stopProvenanceText(position, currency)}
    </span>
  );
}

function lastRecalculatedText(position) {
  if (!position?.stop_calculated_at) return "Not recalculated since recalculation tracking began.";
  const when = format(new Date(position.stop_calculated_at), "d MMM yyyy, HH:mm");
  const source = CALCULATION_SOURCE_LABEL[position.stop_calculation_source];
  return source ? `Last recalculated ${when} — ${source}` : `Last recalculated ${when}`;
}

function StopDetailsContent({ position, currency }) {
  const m = activeMultiplier(position);
  const isProfitStop = m != null && m <= PROFIT_ATR_MULTIPLIER;
  const atrText = hasAtr(position) ? formatCurrency(position.atr_value, { currency }) : "unavailable";
  const multiplierText = m == null
    ? "Multiplier: not recorded yet"
    : `Multiplier: ${formatMultiplier(m)} (${isProfitStop ? "profitable, tight" : "losing or flat, wide"})`;
  return (
    <>
      <p className="font-semibold mb-1">How this stop was set</p>
      <p>
        ATR ({ATR_PERIOD_DAYS}-day): {atrText}
        {position?.atr_source === "fallback" && " (estimated from 2% of entry price)"}
      </p>
      <p>{multiplierText}</p>
      {m != null && (
        <p>
          {isProfitStop
            ? `Price − ${formatMultiplier(m)} ATR, never below entry (§7.2)`
            : `Price − ${formatMultiplier(m)} ATR (§7.2)`}
        </p>
      )}
      <p>A stop never loosens: the stop shown is the highest level reached (§7.3).</p>
      <p>{lastRecalculatedText(position)}</p>
      {position?.grace_period && <p>Grace period: the stop is tracked but not enforced (§6.3).</p>}
    </>
  );
}

/** The trailing-stop value rendered as the trigger for its per-row details tooltip. */
export function StopDetailsTrigger({ position, currency, children }) {
  return (
    <TooltipProvider delayDuration={200}>
      <Tooltip>
        <TooltipTrigger asChild>
          <button
            type="button"
            className="underline decoration-dotted underline-offset-2 cursor-help"
            aria-label={`Stop calculation details for ${position?.ticker}`}
          >
            {children}
          </button>
        </TooltipTrigger>
        <TooltipContent className="max-w-xs text-left space-y-0.5" data-testid="stop-details-tooltip">
          <StopDetailsContent position={position} currency={currency} />
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
