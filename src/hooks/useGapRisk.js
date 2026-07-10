import { useState, useEffect } from "react";
import { apiFetch } from "../api/base44Client";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const cache = {};

// ST-02 (BLG-FEAT-65, v6.9) — per-position gap risk flag.
// Mirrors useEarnings.js: lazily fetched per position, cached by position id,
// so the bulk /positions list load is not slowed by the historical-OHLCV lookup.
export function useGapRisk(positionId) {
  const [data, setData] = useState(cache[positionId] || null);
  const [loading, setLoading] = useState(!cache[positionId]);

  useEffect(() => {
    if (!positionId) return;
    if (cache[positionId]) {
      setData(cache[positionId]);
      setLoading(false);
      return;
    }
    let cancelled = false;
    setLoading(true);
    apiFetch(`${API_BASE}/positions/${positionId}/gap-risk`)
      .then((r) => r.json())
      .then((json) => {
        if (!cancelled) {
          cache[positionId] = json.data;
          setData(json.data);
          setLoading(false);
        }
      })
      .catch(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [positionId]);

  return { data, loading };
}
