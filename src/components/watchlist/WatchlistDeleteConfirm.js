import PropTypes from "prop-types";
import { Button } from "../ui/button";

export default function WatchlistDeleteConfirm({ entry, deleting, onConfirm, onCancel }) {
  return (
    <div className="py-4 space-y-4">
      <p className="text-sm text-slate-300">
        Remove{" "}
        <span className="font-semibold text-white">{entry.ticker}</span>{" "}
        from your watchlist?
      </p>
      <div className="flex gap-3">
        <Button
          onClick={onConfirm}
          disabled={deleting}
          className="bg-rose-600 hover:bg-rose-500 text-white border-0"
        >
          {deleting ? "Removing…" : "Remove"}
        </Button>
        <Button
          variant="ghost"
          onClick={onCancel}
          className="text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800"
        >
          Cancel
        </Button>
      </div>
    </div>
  );
}

WatchlistDeleteConfirm.propTypes = {
  entry: PropTypes.shape({ ticker: PropTypes.string.isRequired }).isRequired,
  deleting: PropTypes.bool,
  onConfirm: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
};
