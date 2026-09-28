import PropTypes from "prop-types";
import { BookOpen, Newspaper, ChevronDown, ChevronUp, Clock } from "lucide-react";
import { cn } from "../../lib/utils";
import { signalLabel, SignalBadge, MarketBadge, priceDisplay, WatchlistEarningsBadge } from "./WatchlistBadges";
import WatchlistRowActions from "./WatchlistRowActions";
import WatchlistNewsRow from "./WatchlistNewsRow";
import { Checkbox } from "../ui/checkbox";
import { getCachedEarningsDays } from "../../hooks/useEarnings";

function AddedCell({ entry }) {
  const days = entry.days_on_watchlist ?? 0;
  const isStale = !!entry.is_stale;

  if (isStale) {
    return (
      <span
        className="inline-flex items-center gap-1 text-xs text-amber-600 dark:text-amber-400"
        aria-label={`On watchlist ${days} days with no action — consider Keep or Remove`}
      >
        <Clock className="w-3.5 h-3.5" />
        {days}d, no action
      </span>
    );
  }

  return (
    <span
      className="text-xs text-slate-600 dark:text-slate-400"
      aria-label={`Added ${days} days ago`}
    >
      {days}d
    </span>
  );
}
AddedCell.propTypes = {
  entry: PropTypes.shape({
    days_on_watchlist: PropTypes.number,
    is_stale: PropTypes.bool,
  }).isRequired,
};

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

function TickerCell({ entry, onEdit }) {
  return (
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
  );
}
TickerCell.propTypes = {
  entry: PropTypes.shape({ ticker: PropTypes.string, company_name: PropTypes.string }).isRequired,
  onEdit: PropTypes.func.isRequired,
};

// ST-03 (EPIC-01, v9.6, BLG-FEAT-97): single column definition consumed by the table header
// AND by the Watchlist CSV export (buildCsv) — see WatchlistTable.js's re-export.
// ST-02 (EPIC-01, v9.8, BLG-FE-185): `cell` renders the table body <td> content for this column,
// so header, body cell and CSV export all derive from one definition instead of the row below
// separately hand-duplicating each column's field mapping. `cell` receives `(entry, ctx)`; only
// Research and News use `ctx`. The Actions column is deliberately not a data column.
// Design: docs/design/2026-09-21__release-v9.6/screener-watchlist-csv-export/decision_record.md §2.2
export const WATCHLIST_COLUMNS = [
  { header: "Ticker", value: (e) => e.ticker, cell: (e, ctx) => <TickerCell entry={e} onEdit={ctx.onEdit} /> },
  { header: "Market", value: (e) => e.market, cell: (e) => <MarketBadge market={e.market} /> },
  {
    header: "Entry Signal", value: (e) => (e.signal_status ? signalLabel(e.signal_status) : ""),
    cell: (e) => <SignalBadge status={e.signal_status} />,
  },
  { header: "Added", value: (e) => e.days_on_watchlist, cell: (e) => <AddedCell entry={e} /> },
  { header: "Target Entry", value: (e) => e.target_entry_price, cell: (e) => priceDisplay(e.target_entry_price, e.market) },
  { header: "Stop (Initial)", value: (e) => e.initial_stop_price, cell: (e) => priceDisplay(e.initial_stop_price, e.market) },
  { header: "Stop (Current)", value: (e) => e.current_stop_price, cell: (e) => priceDisplay(e.current_stop_price, e.market) },
  {
    header: "Earnings", value: (e) => getCachedEarningsDays(e.ticker, e.market),
    cell: (e) => <WatchlistEarningsBadge ticker={e.ticker} market={e.market} />,
  },
  {
    header: "Research", value: (e, ctx) => (ctx.screenerTickers.has(e.ticker?.toUpperCase()) ? "Yes" : "No"),
    cell: (e, ctx) => (
      <BookOpen
        className={cn("w-4 h-4", ctx.hasResearch ? "text-emerald-400" : "text-slate-600")}
        title={ctx.hasResearch ? "Research data available" : "No research data"}
      />
    ),
  },
  {
    header: "News", value: (e) => (e.market === "US" ? "Yes" : "No"),
    cell: (e, ctx) => <NewsToggleCell entry={e} isExpanded={ctx.isNewsExpanded} onToggle={ctx.onToggleNews} />,
  },
];

export default function WatchlistRow({
  entry, isRemoving, hasResearch, isNewsExpanded, newsState, isSelected, onToggleSelect,
  onEdit, onToggleNews, onCloseNews, onResearch, onAddToPosition, onDeleteConfirm, onKeep,
}) {
  const cellCtx = { onEdit, hasResearch, isNewsExpanded, onToggleNews };
  // Columns whose <td> previously carried "text-sm text-slate-300" beyond the shared padding.
  const TEXT_CELL_HEADERS = new Set(["Target Entry", "Stop (Initial)", "Stop (Current)"]);

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
        {WATCHLIST_COLUMNS.map((col) => (
          <td
            key={col.header}
            className={cn("px-5 py-4", TEXT_CELL_HEADERS.has(col.header) && "text-sm text-slate-300")}
          >
            {col.cell(entry, cellCtx)}
          </td>
        ))}
        <td className="px-5 py-4">
          <WatchlistRowActions
            isStale={!!entry.is_stale}
            onResearch={onResearch}
            onAddToPosition={onAddToPosition}
            onDeleteConfirm={onDeleteConfirm}
            onKeep={onKeep}
          />
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
    days_on_watchlist: PropTypes.number,
    is_stale: PropTypes.bool,
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
  onKeep: PropTypes.func.isRequired,
};
