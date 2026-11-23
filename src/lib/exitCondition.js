// Shared §8 exit-condition predicate (ST-08/ST-09, BLG-FE-198/199, v9.10).
// Used by the Positions exit dialog pre-selection and the Dashboard
// "Exit Conditions Met" row. Spec: positions.md §Exit Dialog Pre-Selection
// and Deep Link. Display-only: nothing here submits an exit.

// The reason strings come from the shared exit-reason module (v9.13 ST-03).
import { EXIT_REASON_RISK_OFF, EXIT_REASON_STOP } from "../constants/exitReasons";

export { EXIT_REASON_RISK_OFF, EXIT_REASON_STOP, EXIT_REASON_MANUAL } from "../constants/exitReasons";

// ST-27 (BLG-BE-223, v9.18; strategy_rules.md §9.1): a detected stock split
// not yet confirmed. Until it is, the stored entry and stop are in pre-split
// units, so no stop breach and no exit condition is shown for the position.
export function isSplitPending(position) {
  return position?.split_pending != null && typeof position.split_pending === "object";
}

// Same GBP-basis comparison as the Positions breach badge.
export function isPostGraceStopBreach(position) {
  if (!position || position.grace_period !== false) return false;
  if (isSplitPending(position)) return false;
  const stop = Number(position.current_trailing_stop);
  const price = Number(position.current_price);
  return stop > 0 && price > 0 && price <= stop;
}

export function getExitCondition(position) {
  const riskOff = position?.risk_off_exit === true && !isSplitPending(position);
  const stopBreach = isPostGraceStopBreach(position);
  let reason = null;
  if (riskOff) reason = EXIT_REASON_RISK_OFF;
  else if (stopBreach) reason = EXIT_REASON_STOP;
  return { reason, riskOff, stopBreach };
}

export function exitPreselectNote(position) {
  const { riskOff, stopBreach } = getExitCondition(position);
  if (riskOff) {
    const market = position?.market === "UK" ? "UK" : "US";
    const base = `Pre-selected because the ${market} market is in a risk-off regime (index below its 200-day average).`;
    return stopBreach ? `${base} The price is also at or below the trailing stop.` : base;
  }
  if (stopBreach) {
    return "Pre-selected because the price is at or below the trailing stop and the grace period has ended.";
  }
  return null;
}
