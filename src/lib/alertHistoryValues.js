import { formatCurrency, formatPercent } from "./format";

// ST-04 (BLG-FE-228, v9.18): labels and compact text follow the keys
// alerts_service.py writes (notifications.md v0.12 §Alert History Values).
// Expanded-row labels per key:
const VALUE_LABELS = {
  stop_price:     "Stop price",
  current_price:  "Current price",
  gap_pct:        "Gap to stop",
  threshold_pct:  "Threshold",
  holding_days:   "Days held",
  min_hold_days:  "Grace period (days)",
  days_remaining: "Days left",
  spy_risk_on:    "US regime",
  ftse_risk_on:   "UK regime",
  open_positions: "Open positions",
};

// Prices are in the position's native currency. UK tickers keep the .L
// suffix (data_model.md positions.ticker) and UK prices are pounds.
export function currencyForSymbol(symbol) {
  return typeof symbol === "string" && symbol.toUpperCase().endsWith(".L") ? "GBP" : "USD";
}

function regimeText(value) {
  if (value === true) return "RISK-ON";
  if (value === false) return "RISK-OFF";
  return "UNKNOWN";
}

const has = (obj, ...keys) => keys.every((k) => k in obj);

// Compact text per rule type; null when the row lacks the keys, so the
// generic fallback shows whatever it does have.
const COMPACT_TEXT = {
  stop_loss_approach: (v, currency) =>
    has(v, "current_price", "stop_price", "gap_pct")
      ? `Price ${formatValue("current_price", v.current_price, currency)} · Stop ${formatValue("stop_price", v.stop_price, currency)} · Gap ${formatValue("gap_pct", v.gap_pct)}`
      : null,
  grace_period_warning: (v) =>
    has(v, "holding_days", "min_hold_days", "days_remaining")
      ? `Day ${formatValue("holding_days", v.holding_days)} of ${formatValue("min_hold_days", v.min_hold_days)} · ${formatValue("days_remaining", v.days_remaining)} day(s) left`
      : null,
  // {} (not triggered) falls through to compactValues' "—".
  market_regime_change: (v) =>
    has(v, "spy_risk_on", "ftse_risk_on")
      ? `US ${regimeText(v.spy_risk_on)} · UK ${regimeText(v.ftse_risk_on)}`
      : null,
  daily_portfolio_summary: (v) =>
    has(v, "open_positions") ? `${formatValue("open_positions", v.open_positions)} open position(s)` : null,
};

export function labelFor(key) {
  if (VALUE_LABELS[key]) return VALUE_LABELS[key];
  // Fallback: title-case the snake_case key
  return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function formatValue(key, value, currency = "USD") {
  const k = key.toLowerCase();
  if (k === "spy_risk_on" || k === "ftse_risk_on") return regimeText(value);
  if (value === null || value === undefined) return "—";
  if (typeof value === "number") {
    if (k.includes("_price") || k === "price" || k === "total_pnl") return formatCurrency(value, { currency, signed: k === "total_pnl" });
    if (k.includes("_pct") || k.endsWith("pct")) return formatPercent(value);
  }
  if (typeof value === "boolean") return value ? "Yes" : "No";
  return String(value);
}

export function compactValues(obj, ruleType, symbol) {
  if (!obj || typeof obj !== "object") return "—";
  const currency = currencyForSymbol(symbol);
  const text = COMPACT_TEXT[ruleType]?.(obj, currency);
  if (text) return text;
  const keys = Object.keys(obj);
  if (keys.length === 0) return "—";
  return keys
    .slice(0, 3)
    .map((k) => `${labelFor(k)} ${formatValue(k, obj[k], currency)}`)
    .join(" · ");
}

export function formatValuesExpanded(obj, symbol) {
  if (!obj || typeof obj !== "object") return [];
  const currency = currencyForSymbol(symbol);
  const labelWidth = Math.max(...Object.keys(obj).map((k) => labelFor(k).length));
  return Object.entries(obj).map(([k, v]) => ({
    label: labelFor(k).padEnd(labelWidth, " "),
    value: formatValue(k, v, currency),
    isNegative: k === "gap_pct" && typeof v === "number" && v < 0,
  }));
}
