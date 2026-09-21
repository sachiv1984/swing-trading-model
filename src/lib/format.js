// ST-06 (EPIC-01, v9.6, BLG-FE-182): the single number/currency formatting helper.
//
// The OUTPUT TABLE in docs/design/2026-09-21__release-v9.6/number-format-convention/decision_record.md
// §2.1 (design_system.md v1.21 §Number and Currency Formatting) is the contract:
//   money (unsigned)   £1,234.50  $48.20        symbol + en-GB grouping + 2 dp
//   money (signed)     +£150.00  −£80.00  £0.00 sign, then symbol; zero is unsigned
//   percentage         12.5%  +4.2%  −1.8%      1 dp (default); 2 dp for small cost metrics
//   R computed         +1.25R  −0.50R           signed, 2 dp
//   R user target      2.5R  3R                 as entered, up to 2 dp, trailing zeros trimmed
//   missing            —                        null / undefined / NaN / non-numeric
// Negative sign is the typographic minus U+2212, placed BEFORE the currency symbol.
//
// Strings only: colour stays at the call site (a negative is never conveyed by colour alone —
// the sign is always in the string). The helper never converts currency; the caller decides the
// display basis (strategy_rules.md §4.1.5). CSV exports are exempt (plain numeric values).
//
// Plain functions, no imports — deliberately loadable outside the bundler for unit tests.

export const MINUS = "−";
export const MISSING = "—";

const SYMBOLS = { GBP: "£", USD: "$" };

export function currencyForMarket(market) {
  return market === "UK" ? "GBP" : "USD";
}

function toNumber(value) {
  if (value == null || (typeof value === "string" && value.trim() === "")) return null;
  const n = typeof value === "number" ? value : Number(value);
  return Number.isFinite(n) ? n : null;
}

// Sign for a value already rounded to `dp` places: a value that rounds to zero is unsigned.
function signOf(n, dp, signed) {
  if (Number(Math.abs(n).toFixed(dp)) === 0) return "";
  if (n < 0) return MINUS;
  return signed ? "+" : "";
}

function grouped(abs, dp) {
  return Number(abs.toFixed(dp)).toLocaleString("en-GB", { minimumFractionDigits: dp, maximumFractionDigits: dp });
}

/** Money. `signed: true` for P&L / differences (explicit + on gains). Unsigned amounts still show − when negative. */
export function formatCurrency(value, { currency = "GBP", signed = false } = {}) {
  const n = toNumber(value);
  if (n === null) return MISSING;
  return `${signOf(n, 2, signed)}${SYMBOLS[currency] ?? SYMBOLS.GBP}${grouped(Math.abs(n), 2)}`;
}

/** Percentage: 1 dp default; pass dp: 2 for small-magnitude cost metrics (slippage, fee drag). */
export function formatPercent(value, { signed = false, dp = 1 } = {}) {
  const n = toNumber(value);
  if (n === null) return MISSING;
  return `${signOf(n, dp, signed)}${grouped(Math.abs(n), dp)}%`;
}

/**
 * R-multiple. Default = computed/realised: signed, 2 dp (`+1.25R`, `−0.50R`).
 * `target: true` = a user-entered target: as entered, up to 2 dp, trailing zeros trimmed, unsigned (`2.5R`, `3R`).
 */
export function formatR(value, { target = false } = {}) {
  const n = toNumber(value);
  if (n === null) return MISSING;
  if (target) return `${signOf(n, 2, false)}${Number(Math.abs(n).toFixed(2))}R`;
  return `${signOf(n, 2, true)}${Math.abs(n).toFixed(2)}R`;
}
