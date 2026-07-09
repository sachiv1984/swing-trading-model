import PropTypes from "prop-types";
import { useNavigate } from "react-router-dom";
import WatchlistRow from "./WatchlistRow";

const TABLE_HEADERS = [
  "Ticker", "Market", "Entry Signal", "Target Entry", "Stop (Initial)",
  "Stop (Current)", "Earnings", "Research", "News", "Actions",
];

export default function WatchlistTable({ entries, screenerTickers, newsHook, modalHook }) {
  const navigate = useNavigate();

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-slate-700/50">
            {TABLE_HEADERS.map((h) => (
              <th key={h} className="px-5 py-3.5 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider whitespace-nowrap">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-700/30">
          {entries.map((entry) => (
            <WatchlistRow
              key={entry.id}
              entry={entry}
              isRemoving={!!modalHook.removing[entry.id]}
              hasResearch={screenerTickers.has(entry.ticker?.toUpperCase())}
              isNewsExpanded={!!newsHook.expandedNews[entry.ticker]}
              newsState={newsHook.newsCache[entry.ticker]}
              onEdit={() => modalHook.setModal({ mode: "edit", entry })}
              onToggleNews={() => newsHook.toggleNews(entry)}
              onCloseNews={() => newsHook.setExpandedNews((prev) => ({ ...prev, [entry.ticker]: false }))}
              onResearch={() => navigate(`/research/${entry.ticker}`)}
              onAddToPosition={() => modalHook.handleAddToPosition(entry)}
              onDeleteConfirm={() => modalHook.setModal({ mode: "edit-confirm", entry })}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}

WatchlistTable.propTypes = {
  entries: PropTypes.array.isRequired,
  screenerTickers: PropTypes.instanceOf(Set).isRequired,
  newsHook: PropTypes.shape({
    expandedNews: PropTypes.object.isRequired,
    setExpandedNews: PropTypes.func.isRequired,
    newsCache: PropTypes.object.isRequired,
    toggleNews: PropTypes.func.isRequired,
  }).isRequired,
  modalHook: PropTypes.shape({
    removing: PropTypes.object.isRequired,
    setModal: PropTypes.func.isRequired,
    handleAddToPosition: PropTypes.func.isRequired,
  }).isRequired,
};
