import { useState, useEffect } from "react";
import { apiFetch } from "../api/base44Client";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const cache = {};

export function useEarnings(ticker, market = "US") {
  const key = `${ticker}:${market}`;
  const [data, setData] = useState(cache[key] || null);
  const [loading, setLoading] = useState(!cache[key]);

  useEffect(() => {
    if (!ticker) return;
    if (cache[key]) {
      setData(cache[key]);
      setLoading(false);
      return;
    }
    let cancelled = false;
    setLoading(true);
    apiFetch(`${API_BASE}/earnings/${ticker}?market=${market}`)
      .then((r) => r.json())
      .then((json) => {
        if (!cancelled) {
          cache[key] = json;
          setData(json);
          setLoading(false);
        }
      })
      .catch(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [key, ticker, market]);

  return { data, loading };
}
