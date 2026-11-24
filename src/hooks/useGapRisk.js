import { useState, useEffect } from "react";
import { apiFetch } from "../api/base44Client";
import { createAnswerCache, GAP_RISK_UNAVAILABLE } from "../lib/earningsDataStatus";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const cache = createAnswerCache();

// ST-02 (BLG-FEAT-65, v6.9) — per-position gap risk flag.
// Mirrors useEarnings.js: lazily fetched per position, cached by position id,
// so the bulk /positions list load is not slowed by the historical-OHLCV lookup.
export function useGapRisk(positionId) {
  const [data, setData] = useState(() => cache.get(positionId) || null);
  const [loading, setLoading] = useState(() => !cache.get(positionId));

  useEffect(() => {
    if (!positionId) return;
    const cached = cache.get(positionId);
    if (cached) {
      setData(cached);
      setLoading(false);
      return;
    }
    let cancelled = false;
    setLoading(true);
    apiFetch(`${API_BASE}/positions/${positionId}/gap-risk`)
      // ST-33 (BLG-FE-294, v9.18): a non-2xx response or a failed request means
      // the flag could not be worked out, so it reads like a failed earnings
      // input ("Earnings: unknown"), held for 60 seconds.
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null)
      .then((json) => {
        if (!cancelled) {
          const answer = json && json.data ? json.data : GAP_RISK_UNAVAILABLE;
          cache.set(positionId, answer);
          setData(answer);
          setLoading(false);
        }
      });
    return () => { cancelled = true; };
  }, [positionId]);

  return { data, loading };
}
