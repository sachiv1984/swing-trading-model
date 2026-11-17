import PropTypes from "prop-types";
import { Trash2 } from "lucide-react";
import { Button } from "../ui/button";

export default function WatchlistRowActions({ ticker, isStale, onResearch, onAddToPosition, onDeleteConfirm, onKeep }) {
  return (
    <div className="flex items-center gap-2">
      {isStale && (
        <Button
          variant="outline"
          size="sm"
          onClick={onKeep}
          className="bg-app-raised border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:text-emerald-700 dark:hover:text-emerald-400 hover:border-emerald-500/30 text-xs h-7 px-2.5"
        >
          Keep
        </Button>
      )}
      <Button
        variant="outline"
        size="sm"
        onClick={onResearch}
        className="bg-app-raised border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:text-cyan-700 dark:hover:text-cyan-400 hover:border-cyan-500/30 text-xs h-7 px-2.5"
      >
        Research
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={onAddToPosition}
        className="bg-app-raised border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-slate-700 text-xs h-7 px-2.5"
      >
        Add to Position
      </Button>
      <Button
        variant="ghost"
        size="icon"
        onClick={onDeleteConfirm}
        aria-label={ticker ? `Remove ${ticker} from watchlist` : "Remove from watchlist"}
        className="h-7 w-7 text-slate-600 dark:text-slate-400 hover:text-rose-700 dark:hover:text-rose-400 hover:bg-rose-500/10"
      >
        <Trash2 className="w-4 h-4" />
      </Button>
    </div>
  );
}

WatchlistRowActions.propTypes = {
  ticker: PropTypes.string,
  isStale: PropTypes.bool,
  onResearch: PropTypes.func.isRequired,
  onAddToPosition: PropTypes.func.isRequired,
  onDeleteConfirm: PropTypes.func.isRequired,
  onKeep: PropTypes.func.isRequired,
};
