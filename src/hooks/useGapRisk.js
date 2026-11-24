import { useState, useEffect } from "react";
import { apiFetch } from "../api/base44Client";
import { createAnswerCache, GAP_RISK_UNAVAILABLE, GAP_RISK_UK_FAILED, visibleAnswer } from "../lib/earningsDataStatus";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const cache = createAnswerCache();

// ST-02 (BLG-FEAT-65, v6.9) — per-position gap risk flag.
// Mirrors useEarnings.js: lazily fetched per position, cached by position id,
// so the bulk /positions list load is not slowed by the historical-OHLCV lookup.
// `market` (BLG-FE-335, v9.18): a UK position makes no earnings lookup, so a
// failed gap-risk request for it is not an earnings failure and shows nothing.
export function useGapRisk(positionId, market = "US") {
  const [data, setData] = useState(() => visibleAnswer(cache.get(positionId)) || null);
  const [loading, setLoading] = useState(() => !cache.get(positionId));

  useEffect(() => {
    if (!positionId) return;
    const cached = cache.get(positionId);
    if (cached) {
      setData(visibleAnswer(cached));
      setLoading(false);
      return;
    }
    let cancelled = false;
    setLoading(true);
    apiFetch(`${API_BASE}/positions/${positionId}/gap-risk`)
      // ST-33 (BLG-FE-294, v9.18): a non-2xx response or a failed request means
      // the flag could not be worked out. For a US position that reads like a
      // failed earnings input ("Earnings: unknown"), held for 60 seconds. A UK
      // position makes no earnings lookup, so its failure is also held 60
      // seconds but shows nothing (BLG-FE-335).
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null)
      .then((json) => {
        if (!cancelled) {
          const failed = !(json && json.data);
          const answer = !failed ? json.data : market === "UK" ? GAP_RISK_UK_FAILED : GAP_RISK_UNAVAILABLE;
          cache.set(positionId, answer);
          setData(visibleAnswer(answer));
          setLoading(false);
        }
      });
    return () => { cancelled = true; };
  }, [positionId, market]);

  return { data, loading };
}
