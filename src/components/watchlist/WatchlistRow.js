import PropTypes from "prop-types";
import { BookOpen, Newspaper, ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "../../lib/utils";
import { SignalBadge, MarketBadge, priceDisplay, WatchlistEarningsBadge } from "./WatchlistBadges";
import WatchlistRowActions from "./WatchlistRowActions";
import WatchlistNewsRow from "./WatchlistNewsRow";
import { Checkbox } from "../ui/checkbox";

function NewsToggleCell({ entry, isExpanded, onToggle }) {
  if (entry.market !== "US") return <span className="text-slate-600 text-xs">—</span>;
  return (
    <button
      onClick={onToggle}
      className="flex items-center gap-1 text-xs text-slate-600 dark:text-slate-400 hover:text-cyan-400 transition-colors"
      title="Show news headlines"
    >
      <Newspaper className="w-3.5 h-3.5" />
      {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
    </button>
  );
}
NewsToggleCell.propTypes = {
  entry: PropTypes.shape({ market: PropTypes.string }).isRequired,
  isExpanded: PropTypes.bool,
  onToggle: PropTypes.func.isRequired,
};

export default function WatchlistRow({
  entry, isRemoving, hasResearch, isNewsExpanded, newsState, isSelected, onToggleSelect,
  onEdit, onToggleNews, onCloseNews, onResearch, onAddToPosition, onDeleteConfirm,
}) {
  return (
    <>
      <tr className={cn(
        "transition-all duration-200",
        isRemoving ? "opacity-0" : "opacity-100",
        isSelected && "bg-cyan-500/5"
      )}>
        <td className="px-5 py-4">
          <Checkbox checked={isSelected} onCheckedChange={onToggleSelect} aria-label={`Select ${entry.ticker}`} />
        </td>
        <td className="px-5 py-4">
          <button onClick={onEdit} className="text-left group">
            <span className="block text-cyan-400 group-hover:text-cyan-300 font-semibold text-sm transition-colors">
              {entry.ticker}
            </span>
            {entry.company_name && (
              <span className="block text-slate-600 dark:text-slate-400 text-xs truncate max-w-[140px]">
                {entry.company_name}
              </span>
            )}
          </button>
        </td>
        <td className="px-5 py-4"><MarketBadge market={entry.market} /></td>
        <td className="px-5 py-4"><SignalBadge status={entry.signal_status} /></td>
        <td className="px-5 py-4 text-sm text-slate-300">{priceDisplay(entry.target_entry_price, entry.market)}</td>
        <td className="px-5 py-4 text-sm text-slate-300">{priceDisplay(entry.initial_stop_price, entry.market)}</td>
        <td className="px-5 py-4 text-sm text-slate-300">{priceDisplay(entry.current_stop_price, entry.market)}</td>
        <td className="px-5 py-4"><WatchlistEarningsBadge ticker={entry.ticker} market={entry.market} /></td>
        <td className="px-5 py-4">
          <BookOpen className={cn("w-4 h-4", hasResearch ? "text-emerald-400" : "text-slate-600")}
            title={hasResearch ? "Research data available" : "No research data"} />
        </td>
        <td className="px-5 py-4">
          <NewsToggleCell entry={entry} isExpanded={isNewsExpanded} onToggle={onToggleNews} />
        </td>
        <td className="px-5 py-4">
          <WatchlistRowActions onResearch={onResearch} onAddToPosition={onAddToPosition} onDeleteConfirm={onDeleteConfirm} />
        </td>
      </tr>
      {isNewsExpanded && entry.market === "US" && (
        <WatchlistNewsRow ticker={entry.ticker} newsState={newsState} onClose={onCloseNews} />
      )}
    </>
  );
}

WatchlistRow.propTypes = {
  entry: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    ticker: PropTypes.string.isRequired,
    market: PropTypes.string.isRequired,
    company_name: PropTypes.string,
    signal_status: PropTypes.string,
    target_entry_price: PropTypes.number,
    initial_stop_price: PropTypes.number,
    current_stop_price: PropTypes.number,
  }).isRequired,
  isRemoving: PropTypes.bool,
  hasResearch: PropTypes.bool,
  isNewsExpanded: PropTypes.bool,
  newsState: PropTypes.shape({ loading: PropTypes.bool, headlines: PropTypes.array }),
  isSelected: PropTypes.bool,
  onToggleSelect: PropTypes.func.isRequired,
  onEdit: PropTypes.func.isRequired,
  onToggleNews: PropTypes.func.isRequired,
  onCloseNews: PropTypes.func.isRequired,
  onResearch: PropTypes.func.isRequired,
  onAddToPosition: PropTypes.func.isRequired,
  onDeleteConfirm: PropTypes.func.isRequired,
};
