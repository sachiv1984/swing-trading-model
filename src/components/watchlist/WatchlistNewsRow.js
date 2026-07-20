import PropTypes from "prop-types";

export default function WatchlistNewsRow({ ticker, newsState, onClose }) {
  return (
    <tr className="bg-slate-800/40">
      <td colSpan={10} className="px-6 py-3">
        {newsState?.loading ? (
          <p className="text-slate-600 dark:text-slate-400 text-xs animate-pulse">Loading headlines…</p>
        ) : newsState?.headlines?.length > 0 ? (
          <ul className="space-y-1.5">
            {newsState.headlines.map((h, i) => (
              <li key={i} className="flex flex-col gap-0.5">
                {h.url ? (
                  <a href={h.url} target="_blank" rel="noopener noreferrer" className="text-slate-200 text-xs hover:text-blue-400 hover:underline">{h.headline}</a>
                ) : (
                  <span className="text-slate-200 text-xs">{h.headline}</span>
                )}
                <span className="text-slate-600 dark:text-slate-400 text-xs">
                  {h.source ? `${h.source} · ` : ""}
                  {h.published_at
                    ? new Date(h.published_at).toLocaleDateString()
                    : ""}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-slate-600 dark:text-slate-400 text-xs">No recent news available for {ticker}.</p>
        )}
        <button
          onClick={onClose}
          className="mt-2 text-slate-600 dark:text-slate-400 hover:text-slate-300 text-xs underline"
        >
          Close
        </button>
      </td>
    </tr>
  );
}

WatchlistNewsRow.propTypes = {
  ticker: PropTypes.string.isRequired,
  newsState: PropTypes.shape({
    loading: PropTypes.bool,
    headlines: PropTypes.array,
  }),
  onClose: PropTypes.func.isRequired,
};
