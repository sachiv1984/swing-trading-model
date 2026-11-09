// ST-07 (BLG-FE-255, EPIC-02, v9.16): "Plan this" target URL, shared by the
// Signals card and the Screener row. trade_plan.md v1.22 §2; signals.md v0.9
// §"Plan this" Action; screener_results.md v1.11 §11.1. Navigation only: no
// write, no status change, no plan until the user saves.
export function planThisUrl({ ticker, market, price, signalId } = {}) {
  const params = new URLSearchParams();
  params.set("ticker", ticker || "");
  params.set("market", market || "US");
  const p = Number(price);
  if (price != null && price !== "" && Number.isFinite(p) && p > 0) params.set("entry_price", String(price));
  if (signalId != null && signalId !== "") params.set("signal_id", String(signalId));
  return `/TradePlan?${params.toString()}`;
}

// Signals card: shown for new and watchlisted signals only (signals.md v0.9).
export const PLAN_THIS_SIGNAL_STATUSES = ["new", "watchlisted"];
