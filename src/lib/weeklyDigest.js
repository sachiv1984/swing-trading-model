// Weekly Digest figures — weekly_digest.md v0.5 §2 (ST-14, ST-15, ST-16, v9.18).
//
// Turns a GET /digest/weekly `data` object into the rows the page shows:
// a plain-language label, the display value, whether it is muted, the link on
// the value (never on a null or "not available" value) and an optional second
// line. Pure functions, no React, so they are unit-tested in
// weeklyDigest.test.js (frontend_development_guide.md §14).
import { formatCurrency, formatPercent } from "./format";

// Onward links (navigation.md §Onward Links, Weekly Digest row). Realised P&L
// opens Performance on its "Last 7 Days" period, which uses the same
// exit_date cutoff as the digest (Head of UX & Design ruling, 2026-11-27).
export const DIGEST_LINKS = {
  realised_pnl_7d: "/Performance?section=summary&period=last_7_days",
  alerts_fired_7d: "/notifications?since_days=7",
  alerts_dismissed_7d: "/notifications?since_days=7&read=true",
  journal_completion_rate_current: "/Performance?section=compliance",
  red_flags_7d: "/Journal?section=red-flags",
};

const isMissing = (v) => v === null || v === undefined;

function count(value) {
  return isMissing(value) ? null : String(value);
}

// The journal completion rates are 0.0 both for "no closed trades" and for
// "no notes", so the trade counts decide the text (ST-14 ruling 2026-11-27).
function journalRow(data) {
  const rate = data.journal_completion_rate_current;
  const total = data.closed_trades_total;
  const row = {
    field: "journal_completion_rate_current",
    label: "Journal completion (all closed trades)",
  };
  if (isMissing(rate) || isMissing(total)) return { ...row, value: "Not available", muted: true, href: null, secondLine: null };
  if (total === 0) return { ...row, value: "No closed trades yet", muted: true, href: null, secondLine: null };

  const before = data.journal_completion_rate_7d_ago;
  const beforeTotal = data.closed_trades_total_7d_ago;
  let secondLine = null;
  if (!isMissing(before) && !isMissing(beforeTotal)) {
    secondLine = { text: beforeTotal === 0 ? "A week ago: no closed trades" : `A week ago: ${formatPercent(before)}`, href: null };
  }
  return { ...row, value: formatPercent(rate), muted: false, href: DIGEST_LINKS[row.field], secondLine };
}

/** The five figure rows, in weekly_digest.md §2 order. */
export function digestFigures(data) {
  const d = data || {};
  const delta = d.unrealised_pnl_delta_7d;
  const alerts = count(d.alerts_fired_7d);
  const read = count(d.alerts_dismissed_7d);
  const flags = count(d.red_flags_7d);
  const realised = isMissing(d.realised_pnl_7d) ? null : formatCurrency(d.realised_pnl_7d, { signed: true });

  return [
    {
      field: "realised_pnl_7d",
      label: "Realised P&L, last 7 days",
      value: realised ?? "Not available",
      muted: realised === null,
      href: realised === null ? null : DIGEST_LINKS.realised_pnl_7d,
      secondLine: null,
    },
    {
      field: "unrealised_pnl_delta_7d",
      label: "Change in open P&L, last 7 days",
      value: isMissing(delta) ? "Not enough history yet" : formatCurrency(delta, { signed: true }),
      muted: isMissing(delta),
      href: null, // no page shows this delta
      secondLine: null,
    },
    {
      field: "alerts_fired_7d",
      // "Alerts", not "Alerts sent": the count is every alert raised, and a
      // Feed row can be "Not sent" (Head of UX & Design ruling, 2026-11-27).
      label: "Alerts, last 7 days",
      value: alerts ?? "Not available",
      muted: alerts === null,
      href: alerts === null ? null : DIGEST_LINKS.alerts_fired_7d,
      secondLine: read === null ? null : { text: `${read} marked read`, href: DIGEST_LINKS.alerts_dismissed_7d },
    },
    journalRow(d),
    {
      field: "red_flags_7d",
      label: "Red flags, last 7 days",
      value: flags ?? "Not available",
      muted: flags === null,
      href: flags === null ? null : DIGEST_LINKS.red_flags_7d,
      secondLine: null,
    },
  ];
}

const AS_OF_FORMAT = new Intl.DateTimeFormat("en-GB", {
  timeZone: "UTC",
  day: "numeric",
  month: "short",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit",
  hourCycle: "h23",
});

/** "27 Nov 2026, 14:15" in UTC, or null for a missing or unparseable time. */
export function formatAsOfUtc(iso) {
  if (!iso) return null;
  const t = new Date(iso);
  if (Number.isNaN(t.getTime())) return null;
  const parts = Object.fromEntries(AS_OF_FORMAT.formatToParts(t).map((p) => [p.type, p.value]));
  return `${parts.day} ${parts.month} ${parts.year}, ${parts.hour}:${parts.minute}`;
}

/** The freshness caption under the figures (weekly_digest.md §2 Freshness Caption). */
export function freshnessCaption(data) {
  const d = data || {};
  const asOf = formatAsOfUtc(d.as_of_utc);
  const snapshot = isMissing(d.staleness_hours)
    ? "no portfolio snapshot yet"
    : `portfolio snapshot ${Number(d.staleness_hours).toFixed(1)} hours old`;
  return asOf ? `Figures as of ${asOf} UTC · ${snapshot}` : `Figures as of now · ${snapshot}`;
}

// This week's loop (ST-17, metrics_definitions.md §Core Loop Metrics;
// weekly_digest.md §2 This Week's Loop): five counts in loop order, each
// linked to its step's list page except the review step (this page).
const LOOP_STEPS = [
  { key: "signals", label: "Signals", href: "/Signals" },
  { key: "plans", label: "Plans", href: "/TradePlans" },
  { key: "entries", label: "Entries", href: "/Positions" },
  { key: "reflections", label: "Reflections", href: "/Journal?section=reflections" },
  { key: "reviews", label: "Reviews", href: null },
];

/** The five loop steps for display; a null or missing count is "Not available" and unlinked. */
export function loopSteps(loop) {
  const l = loop || {};
  return LOOP_STEPS.map(({ key, label, href }) => {
    const n = l[key];
    const known = typeof n === "number";
    return { key, label, value: known ? String(n) : "Not available", muted: !known, href: known ? href : null };
  });
}

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/** "Monday 23 Nov to today (UTC)" from the API's week_start (YYYY-MM-DD), or null. */
export function loopCaption(weekStart) {
  if (typeof weekStart !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(weekStart)) return null;
  const d = new Date(`${weekStart}T00:00:00Z`);
  // A calendar-invalid date (2026-02-30) rolls over; reject it by round trip.
  if (Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== weekStart) return null;
  return `Monday ${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]} to today (UTC)`;
}
