import { Eye } from "lucide-react";
import PageHeader from "../components/ui/PageHeader";
import WatchlistModal from "../components/watchlist/WatchlistModal";
import WatchlistTable from "../components/watchlist/WatchlistTable";
import AddTickerButton from "../components/watchlist/AddTickerButton";
import DataState from "../components/ui/DataState";
import { useWatchlistData } from "../hooks/useWatchlistData";
import { useWatchlistNews } from "../hooks/useWatchlistNews";
import { useWatchlistModal } from "../hooks/useWatchlistModal";

export default function Watchlist() {
  const { entries, setEntries, loading, loadError, screenerTickers, fetchEntries } = useWatchlistData();
  const newsHook = useWatchlistNews();
  const modalHook = useWatchlistModal(setEntries);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Watchlist"
        description="Monitor tickers for entry opportunities."
        actions={<AddTickerButton onClick={() => modalHook.setModal({ mode: "add" })} />}
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
          <WatchlistTable entries={entries} screenerTickers={screenerTickers} newsHook={newsHook} modalHook={modalHook} />
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
