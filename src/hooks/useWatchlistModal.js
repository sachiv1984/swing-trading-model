import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { sortEntries } from "./useWatchlistData";

const FADE_OUT_DURATION_MS = 200;
const NAVIGATE_DELAY_MS = 220;

function buildWatchlistPrefillState(entry) {
  return {
    watchlist_prefill: {
      id: entry.id,
      ticker: entry.ticker,
      market: entry.market,
      entry_price: entry.target_entry_price != null ? String(entry.target_entry_price) : "",
      stop_price: entry.initial_stop_price != null ? String(entry.initial_stop_price) : "",
    },
  };
}

export function useWatchlistModal(setEntries) {
  const navigate = useNavigate();
  const [modal, setModal] = useState(null);
  const [removing, setRemoving] = useState({});

  const fadeOutAndRemove = (id) => {
    setRemoving((prev) => ({ ...prev, [id]: true }));
    setTimeout(() => {
      setEntries((prev) => prev.filter((e) => e.id !== id));
      setRemoving((prev) => {
        const next = { ...prev };
        delete next[id];
        return next;
      });
    }, FADE_OUT_DURATION_MS);
  };

  const handleAdded = (entry) => {
    setEntries((prev) => sortEntries([...prev, entry]));
    setModal(null);
  };

  const handleUpdated = (entry) => {
    setEntries((prev) =>
      sortEntries(prev.map((e) => (e.id === entry.id ? entry : e)))
    );
    setModal(null);
  };

  const handleDeleted = (id) => {
    setModal(null);
    fadeOutAndRemove(id);
  };

  const handleAddToPosition = (entry) => {
    fadeOutAndRemove(entry.id);
    setTimeout(() => {
      navigate("/TradeEntry", { state: buildWatchlistPrefillState(entry) });
    }, NAVIGATE_DELAY_MS);
  };

  return { modal, setModal, removing, handleAdded, handleUpdated, handleDeleted, handleAddToPosition };
}
