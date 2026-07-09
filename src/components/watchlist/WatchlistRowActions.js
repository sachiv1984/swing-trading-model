import PropTypes from "prop-types";
import { Trash2 } from "lucide-react";
import { Button } from "../ui/button";

export default function WatchlistRowActions({ onResearch, onAddToPosition, onDeleteConfirm }) {
  return (
    <div className="flex items-center gap-2">
      <Button
        variant="outline"
        size="sm"
        onClick={onResearch}
        className="bg-slate-800/50 border-slate-700 text-slate-300 hover:text-cyan-400 hover:border-cyan-500/30 text-xs h-7 px-2.5"
      >
        Research
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={onAddToPosition}
        className="bg-slate-800/50 border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700 text-xs h-7 px-2.5"
      >
        Add to Position
      </Button>
      <Button
        variant="ghost"
        size="icon"
        onClick={onDeleteConfirm}
        className="h-7 w-7 text-slate-600 dark:text-slate-400 hover:text-rose-400 hover:bg-rose-500/10"
      >
        <Trash2 className="w-4 h-4" />
      </Button>
    </div>
  );
}

WatchlistRowActions.propTypes = {
  onResearch: PropTypes.func.isRequired,
  onAddToPosition: PropTypes.func.isRequired,
  onDeleteConfirm: PropTypes.func.isRequired,
};
