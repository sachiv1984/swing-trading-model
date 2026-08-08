import PropTypes from "prop-types";
import { DialogFooter } from "../ui/dialog";
import { Button } from "../ui/button";

export default function WatchlistModalFooter({ isEdit, submitting, onRemoveClick, onCancel, onSubmit }) {
  return (
    <DialogFooter className="flex items-center !justify-between gap-2 pt-2">
      <div>
        {isEdit && (
          <Button
            variant="ghost"
            onClick={onRemoveClick}
            className="text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 px-2"
          >
            Remove from Watchlist
          </Button>
        )}
      </div>
      <div className="flex gap-2">
        <Button
          variant="ghost"
          onClick={onCancel}
          className="text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800"
        >
          Cancel
        </Button>
        <Button
          onClick={onSubmit}
          disabled={submitting}
          className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25"
        >
          {submitting ? "Saving…" : isEdit ? "Save Changes" : "Add to Watchlist"}
        </Button>
      </div>
    </DialogFooter>
  );
}

WatchlistModalFooter.propTypes = {
  isEdit: PropTypes.bool,
  submitting: PropTypes.bool,
  onRemoveClick: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
};
