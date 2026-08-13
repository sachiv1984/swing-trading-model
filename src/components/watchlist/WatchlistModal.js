import PropTypes from "prop-types";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "../ui/dialog";
import { useWatchlistEntryForm } from "../../hooks/useWatchlistEntryForm";
import WatchlistDeleteConfirm from "./WatchlistDeleteConfirm";
import WatchlistEntryFields from "./WatchlistEntryFields";
import WatchlistModalFooter from "./WatchlistModalFooter";

export default function WatchlistModal({ mode, entry, onClose, onAdded, onUpdated, onDeleted }) {
  const {
    isEdit, form, setForm, tickerError, submitting, confirmDelete, setConfirmDelete, deleting,
    handleTickerChange, handleSubmit, handleDelete,
  } = useWatchlistEntryForm({ mode, entry, onAdded, onUpdated, onDeleted });

  return (
    <Dialog open onOpenChange={onClose}>
      <DialogContent className="bg-background border-border text-foreground max-w-md">
        <DialogHeader>
          <DialogTitle className="text-foreground">
            {isEdit ? `Edit ${entry.ticker}` : "Add Ticker to Watchlist"}
          </DialogTitle>
          <DialogDescription className="text-slate-600 dark:text-slate-400">
            {isEdit ? "Update price levels for this ticker." : "Track a new ticker for entry opportunities."}
          </DialogDescription>
        </DialogHeader>

        {confirmDelete ? (
          <WatchlistDeleteConfirm
            entry={entry}
            deleting={deleting}
            onConfirm={handleDelete}
            onCancel={() => setConfirmDelete(false)}
          />
        ) : (
          <>
            <WatchlistEntryFields
              form={form}
              setForm={setForm}
              tickerError={tickerError}
              isEdit={isEdit}
              onTickerChange={handleTickerChange}
            />
            <WatchlistModalFooter
              isEdit={isEdit}
              submitting={submitting}
              onRemoveClick={() => setConfirmDelete(true)}
              onCancel={onClose}
              onSubmit={handleSubmit}
            />
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}

WatchlistModal.propTypes = {
  mode: PropTypes.oneOf(["add", "edit", "edit-confirm"]).isRequired,
  entry: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    ticker: PropTypes.string,
    market: PropTypes.string,
    target_entry_price: PropTypes.number,
    initial_stop_price: PropTypes.number,
    current_stop_price: PropTypes.number,
  }),
  onClose: PropTypes.func.isRequired,
  onAdded: PropTypes.func.isRequired,
  onUpdated: PropTypes.func.isRequired,
  onDeleted: PropTypes.func.isRequired,
};
