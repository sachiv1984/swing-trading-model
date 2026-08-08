import { useState } from "react";
import { apiFetch, API_BASE_URL } from "../api/base44Client";

const TICKER_RE = /^[A-Z0-9.]{1,10}$/;
const HTTP_CONFLICT = 409;

function buildPriceFields(form) {
  return {
    target_entry_price: form.target_entry_price !== "" ? parseFloat(form.target_entry_price) : null,
    initial_stop_price: form.initial_stop_price !== "" ? parseFloat(form.initial_stop_price) : null,
    current_stop_price: form.current_stop_price !== "" ? parseFloat(form.current_stop_price) : null,
  };
}

async function saveEdit(entry, body, onUpdated) {
  const res = await apiFetch(`${API_BASE_URL}/watchlist/${entry.id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error();
  const json = await res.json();
  onUpdated(json.data);
}

async function saveNewOrConflict(form, body, onAdded) {
  const res = await apiFetch(`${API_BASE_URL}/watchlist`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ticker: form.ticker, market: form.market, ...body }),
  });
  if (res.status === HTTP_CONFLICT) return "conflict";
  if (!res.ok) throw new Error();
  const json = await res.json();
  onAdded(json.data);
  return undefined;
}

export function useWatchlistEntryForm({ mode, entry, onAdded, onUpdated, onDeleted }) {
  const isEdit = mode === "edit" || mode === "edit-confirm";

  const [form, setForm] = useState({
    ticker: entry?.ticker || "",
    market: entry?.market || "UK",
    target_entry_price: entry?.target_entry_price ?? "",
    initial_stop_price: entry?.initial_stop_price ?? "",
    current_stop_price: entry?.current_stop_price ?? "",
  });
  const [tickerError, setTickerError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(mode === "edit-confirm");
  const [deleting, setDeleting] = useState(false);

  const handleTickerChange = (val) => {
    const upper = val.toUpperCase();
    setForm((f) => ({ ...f, ticker: upper }));
    setTickerError(upper && !TICKER_RE.test(upper) ? "Invalid format. Use 1–10 alphanumeric characters." : "");
  };

  const handleSubmit = async () => {
    if (!form.ticker) { setTickerError("Ticker is required."); return; }
    if (!TICKER_RE.test(form.ticker)) { setTickerError("Invalid format."); return; }

    const body = buildPriceFields(form);
    setSubmitting(true);
    try {
      if (isEdit) {
        await saveEdit(entry, body, onUpdated);
      } else if ((await saveNewOrConflict(form, body, onAdded)) === "conflict") {
        setTickerError("This ticker is already on your watchlist.");
      }
    } catch {
      setSubmitting(false);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await apiFetch(`${API_BASE_URL}/watchlist/${entry.id}`, { method: "DELETE" });
      onDeleted(entry.id);
    } catch {
      setDeleting(false);
    }
  };

  return {
    isEdit, form, setForm, tickerError, submitting, confirmDelete, setConfirmDelete, deleting,
    handleTickerChange, handleSubmit, handleDelete,
  };
}
