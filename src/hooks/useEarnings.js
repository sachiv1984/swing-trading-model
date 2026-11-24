import { useState, useEffect } from "react";
import { apiFetch } from "../api/base44Client";
import { createAnswerCache, UNAVAILABLE_ANSWER } from "../lib/earningsDataStatus";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const cache = createAnswerCache();

// ST-03 (v9.6): read-only access to the already-loaded earnings cache so the CSV export can
// include the Earnings column without a network call. Returns whole days (>= 0) or null.
export function getCachedEarningsDays(ticker, market = "US") {
  const days = cache.get(`${ticker}:${market}`)?.days_until_earnings;
  return typeof days === "number" && days >= 0 ? days : null;
}

// ST-33 (BLG-FE-294, v9.18): an answer with data_status "unavailable" (a failed
// lookup) is held for 60 seconds, not for the session, so the first mount of a
// badge after that retries (lib/earningsDataStatus.js). A falsy ticker makes no
// lookup (the Screener passes none for UK rows).
export function useEarnings(ticker, market = "US") {
  const key = `${ticker}:${market}`;
  const [data, setData] = useState(() => cache.get(key) || null);
  const [loading, setLoading] = useState(() => Boolean(ticker) && !cache.get(key));

  useEffect(() => {
    if (!ticker) {
      setData(null);
      setLoading(false);
      return;
    }
    const cached = cache.get(key);
    if (cached) {
      setData(cached);
      setLoading(false);
      return;
    }
    let cancelled = false;
    setLoading(true);
    apiFetch(`${API_BASE}/earnings/${ticker}?market=${market}`)
      // ST-33: a non-2xx response or a failed request is a failed lookup too,
      // shown as "unknown" and not cached (apiFetch does not reject on 5xx).
      .then((r) => (r.ok ? r.json() : UNAVAILABLE_ANSWER))
      .catch(() => UNAVAILABLE_ANSWER)
      .then((json) => {
        if (!cancelled) {
          cache.set(key, json);
          setData(json);
          setLoading(false);
        }
      });
    return () => { cancelled = true; };
  }, [key, ticker, market]);

  return { data, loading };
}
