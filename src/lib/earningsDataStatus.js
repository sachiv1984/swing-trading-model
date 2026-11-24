// ST-33 (BLG-FE-294, v9.18): GET /earnings/{ticker} and GET /positions/{id}/gap-risk
// return data_status "ok" | "unavailable" (earnings_endpoints.md v0.4,
// position_endpoints.md v2.24.0). "unavailable" is a failed lookup: shown as a
// muted "unknown" and never cached for the session. It is held for
// UNAVAILABLE_HOLD_MS, so the first render after that retries (Product Owner
// ruling 2026-11-24: without a hold, every remount re-sent every failed lookup
// while Yahoo throttled). An answer with no data_status (an older backend) reads
// as "ok"; a non-object answer is not cached.

export const EARNINGS_UNKNOWN_TOOLTIP = "The earnings date could not be fetched. It will be retried.";

// What a badge shows when the request itself fails (a non-2xx response or a
// network error): the same as a failed lookup.
export const UNAVAILABLE_ANSWER = Object.freeze({
  next_earnings_date: null,
  days_until_earnings: null,
  data_status: "unavailable",
});

// What the Alerts cell shows when the gap-risk request itself fails.
export const GAP_RISK_UNAVAILABLE = Object.freeze({
  flagged: false,
  reasons: [],
  data_status: "unavailable",
});

export function isEarningsUnavailable(answer) {
  return Boolean(answer) && typeof answer === "object" && answer.data_status === "unavailable";
}

// Whether a fetched answer may go in the session cache.
export function isCacheableAnswer(answer) {
  return Boolean(answer) && typeof answer === "object" && !isEarningsUnavailable(answer);
}

export const UNAVAILABLE_HOLD_MS = 60 * 1000;

// Session cache for earnings and gap-risk answers: an ok answer is kept for the
// session; an unavailable one for UNAVAILABLE_HOLD_MS; anything else not at all.
export function createAnswerCache(holdMs = UNAVAILABLE_HOLD_MS) {
  const entries = new Map();
  return {
    get(key, now = Date.now()) {
      const entry = entries.get(key);
      if (!entry) return undefined;
      if (entry.expiresAt !== null && now >= entry.expiresAt) {
        entries.delete(key);
        return undefined;
      }
      return entry.answer;
    },
    set(key, answer, now = Date.now()) {
      if (isCacheableAnswer(answer)) entries.set(key, { answer, expiresAt: null });
      else if (isEarningsUnavailable(answer)) entries.set(key, { answer, expiresAt: now + holdMs });
      else entries.delete(key);
    },
  };
}
