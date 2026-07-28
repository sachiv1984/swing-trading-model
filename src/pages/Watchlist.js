import { useState, useEffect } from "react";
import { Eye } from "lucide-react";
import PageHeader from "../components/ui/PageHeader";
import WatchlistModal from "../components/watchlist/WatchlistModal";
import WatchlistTable from "../components/watchlist/WatchlistTable";
import AddTickerButton from "../components/watchlist/AddTickerButton";
import DataState from "../components/ui/DataState";
import BulkActionToolbar from "../components/shared/BulkActionToolbar";
import { useWatchlistData } from "../hooks/useWatchlistData";
import { useWatchlistNews } from "../hooks/useWatchlistNews";
import { useWatchlistModal } from "../hooks/useWatchlistModal";
import { apiFetch, API_BASE_URL } from "../api/base44Client";

export default function Watchlist() {
  const { entries, setEntries, loading, loadError, screenerTickers, fetchEntries } = useWatchlistData();
  const newsHook = useWatchlistNews();
  const modalHook = useWatchlistModal(setEntries);
  const [selectedIds, setSelectedIds] = useState(new Set());
  const [tagOptions, setTagOptions] = useState([]);

  useEffect(() => {
    apiFetch(`${API_BASE_URL}/watchlist/tags`)
      .then((r) => (r.ok ? r.json() : { data: [] }))
      .then((json) => setTagOptions(json.data || []))
      .catch(() => {});
  }, []);

  const toggleRow = (id) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const toggleAll = () => {
    setSelectedIds((prev) =>
      prev.size === entries.length ? new Set() : new Set(entries.map((e) => e.id))
    );
  };

  const handleBulkResult = async (result) => {
    if (result.failed.length === 0) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(result.failed.map((f) => f.id)));
    }
    await fetchEntries();
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Watchlist"
        description="Monitor tickers for entry opportunities."
        actions={<AddTickerButton onClick={() => modalHook.setModal({ mode: "add" })} />}
      />

      <BulkActionToolbar
        selectedCount={selectedIds.size}
        onClear={() => setSelectedIds(new Set())}
        itemLabel="entries"
        tagAction={{
          tagOptions,
          onSubmit: async (tags) => {
            const res = await apiFetch(`${API_BASE_URL}/watchlist/bulk-tag`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ ids: Array.from(selectedIds), tags }),
            });
            const json = await res.json();
            return json.data;
          },
        }}
        destructiveActions={[
          {
            key: "remove",
            label: "Bulk Remove",
            confirmText: `Remove ${selectedIds.size} selected watchlist entries?`,
            onConfirm: async () => {
              const res = await apiFetch(`${API_BASE_URL}/watchlist/bulk`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ids: Array.from(selectedIds) }),
              });
              const json = await res.json();
              return json.data;
            },
          },
        ]}
        onResult={handleBulkResult}
      />

      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 overflow-hidden">
        <DataState
          loading={loading}
          error={loadError}
          onRetry={fetchEntries}
          empty={!loading && !loadError && entries.length === 0}
          emptyIcon={<Eye className="w-10 h-10 text-slate-600" />}
          emptyHeading="Your watchlist is empty"
          emptyBody="Add tickers you're monitoring for entry opportunities."
          emptyAction={<AddTickerButton onClick={() => modalHook.setModal({ mode: "add" })} />}
        >
          <WatchlistTable
            entries={entries}
            screenerTickers={screenerTickers}
            newsHook={newsHook}
            modalHook={modalHook}
            selectedIds={selectedIds}
            onToggleRow={toggleRow}
            onToggleAll={toggleAll}
            onKeep={modalHook.handleKeep}
          />
        </DataState>
      </div>

      {modalHook.modal && (
        <WatchlistModal
          mode={modalHook.modal.mode}
          entry={modalHook.modal.entry || null}
          onClose={() => modalHook.setModal(null)}
          onAdded={modalHook.handleAdded}
          onUpdated={modalHook.handleUpdated}
          onDeleted={modalHook.handleDeleted}
        />
      )}
    </div>
  );
}
