import { useState, useCallback } from "react";
import { apiFetch, API_BASE_URL } from "../api/base44Client";

export function useWatchlistNews() {
  const [expandedNews, setExpandedNews] = useState({});
  const [newsCache, setNewsCache] = useState({});

  const toggleNews = useCallback(async (entry) => {
    const key = entry.ticker;
    if (expandedNews[key]) {
      setExpandedNews((prev) => ({ ...prev, [key]: false }));
      return;
    }
    setExpandedNews((prev) => ({ ...prev, [key]: true }));
    if (newsCache[key]) return;
    setNewsCache((prev) => ({ ...prev, [key]: { loading: true, headlines: [] } }));
    try {
      const res = await apiFetch(`${API_BASE_URL}/news/${entry.ticker}?market=${entry.market}`);
      const json = await res.json();
      setNewsCache((prev) => ({
        ...prev,
        [key]: { loading: false, headlines: json.data?.headlines || [] },
      }));
    } catch {
      setNewsCache((prev) => ({ ...prev, [key]: { loading: false, headlines: [] } }));
    }
  }, [expandedNews, newsCache]);

  return { expandedNews, setExpandedNews, newsCache, toggleNews };
}
