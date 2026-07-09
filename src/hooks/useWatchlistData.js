import { useState, useEffect, useCallback } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiFetch, API_BASE_URL } from "../api/base44Client";

const SIGNAL_ORDER = { active: 0, watch: 1, no_signal: 2 };
const SCREENER_CACHE_STALE_TIME_MS = 300000;

export function sortEntries(entries) {
  return [...entries].sort((a, b) => {
    const sigDiff =
      (SIGNAL_ORDER[a.signal_status] ?? 2) -
      (SIGNAL_ORDER[b.signal_status] ?? 2);
    if (sigDiff !== 0) return sigDiff;
    return a.ticker.localeCompare(b.ticker);
  });
}

export function useWatchlistData() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);

  const { data: screenerTickers = new Set() } = useQuery({
    queryKey: ["screener-tickers"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE_URL}/screener/results`);
      const json = await res.json();
      const rows = json?.data || [];
      return new Set(rows.map(r => (r.ticker || "").toUpperCase()));
    },
    staleTime: SCREENER_CACHE_STALE_TIME_MS,
  });

  const fetchEntries = useCallback(async () => {
    setLoadError(false);
    setLoading(true);
    try {
      const res = await apiFetch(`${API_BASE_URL}/watchlist`);
      if (!res.ok) throw new Error();
      const json = await res.json();
      setEntries(sortEntries(json.data));
    } catch {
      setLoadError(true);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchEntries();
  }, [fetchEntries]);

  return { entries, setEntries, loading, loadError, screenerTickers, fetchEntries };
}
