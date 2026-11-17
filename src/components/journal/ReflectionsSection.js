import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api, toReflectionRow } from "../../api/base44Client";
import { BookOpen, Calendar } from "lucide-react";
import { format } from "date-fns";
import { cn } from "../../lib/utils";
import { Button } from "../ui/button";
import DataState from "../ui/DataState";
import OnwardLink from "../ui/OnwardLink";
import TradeReflectionModal from "../trades/TradeReflectionModal";
import { formatCurrency, formatR } from "../../lib/format";
import { exitReasonBadgeClass, exitReasonShortLabel } from "../../constants/exitReasons";
import { tickerMatches } from "../../lib/journalFilter";

// Journal → Reflections section (journal.md v1.1 §4; ST-05, BLG-FE-258).
// Content and states from reflections.md §4–§7 and §9. The card body is the
// button that opens the reflection modal; "View trade" is a sibling link in
// the card footer, so no interactive element is nested in another.
export default function ReflectionsSection({ ticker, onCount, onClearFilter }) {
  const [selectedTrade, setSelectedTrade] = useState(null);

  // The same ['trades'] query Trade History and Position notes read, so the
  // Journal requests GET /trades once.
  const { data: trades = [], isLoading, isError, refetch } = useQuery({
    queryKey: ["trades"],
    queryFn: () => api.trades.list(),
    select: (data) => (data?.trades || []).map(toReflectionRow),
  });

  const filtered = trades.filter((r) => tickerMatches(r.ticker, ticker));
  const loaded = !isLoading && !isError;

  useEffect(() => {
    onCount(loaded ? filtered.length : null);
  }, [loaded, filtered.length, onCount]);

  if (isLoading || isError) {
    return (
      <DataState
        loading={isLoading}
        error={isError}
        onRetry={() => refetch()}
        errorHeading="Unable to load reflections"
        errorBody="Please try again."
      />
    );
  }

  if (filtered.length === 0) {
    const filteredOut = trades.length > 0;
    return (
      <div
        data-testid="reflections-empty"
        className="rounded-2xl bg-white dark:bg-gradient-to-br dark:from-slate-900 dark:to-slate-800 border border-app-line p-12 text-center"
      >
        <BookOpen className="w-10 h-10 text-app-muted mx-auto mb-3" />
        {filteredOut ? (
          <>
            <p className="text-slate-600 dark:text-slate-400">
              No closed trades match {ticker.trim().toUpperCase()}.
            </p>
            <Button variant="outline" size="sm" className="mt-3" onClick={onClearFilter}>
              Clear filter
            </Button>
          </>
        ) : (
          <p className="text-slate-600 dark:text-slate-400">
            No closed trades yet — close a trade to write your first reflection.
          </p>
        )}
      </div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {filtered.map((r) => {
          const pnl = r.pnl ?? 0;
          return (
            <div
              key={r.id}
              data-testid="reflection-card"
              className="flex flex-col rounded-2xl bg-white dark:bg-gradient-to-br dark:from-slate-900 dark:to-slate-800 border border-app-line hover:border-cyan-500/40 hover:shadow-lg hover:shadow-cyan-500/5 transition-all"
            >
              <button
                type="button"
                onClick={() => setSelectedTrade(r)}
                className="flex-1 text-left p-5 pb-3 rounded-t-2xl group"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <span className="text-lg font-bold text-app-fg group-hover:text-cyan-700 dark:group-hover:text-cyan-400 transition-colors">
                      {r.ticker}
                    </span>
                    <span className="ml-2 text-xs px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700">
                      {r.market || "—"}
                    </span>
                  </div>
                  <span data-testid="exit-reason-badge" className={exitReasonBadgeClass(r.exit_reason)}>
                    {exitReasonShortLabel(r.exit_reason)}
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-2 mb-3">
                  <div>
                    <div className="text-xs text-slate-600 dark:text-slate-400">P&L</div>
                    <div className={cn("text-sm font-semibold", pnl > 0 ? "text-app-positive" : pnl < 0 ? "text-app-negative" : "text-slate-700 dark:text-slate-300")}>
                      {formatCurrency(pnl, { signed: true })}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-600 dark:text-slate-400">R-Multiple</div>
                    <div className={cn("text-sm font-semibold", r.r_multiple == null ? "text-slate-600 dark:text-slate-400" : r.r_multiple > 0 ? "text-app-positive" : r.r_multiple < 0 ? "text-app-negative" : "text-slate-700 dark:text-slate-300")}>
                      {r.r_multiple != null ? formatR(r.r_multiple) : "N/A"}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-600 dark:text-slate-400">Hold</div>
                    <div className="text-sm font-medium text-slate-700 dark:text-slate-300">
                      {r.hold_days != null ? `${r.hold_days}d` : "—"}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-1 text-xs text-app-muted">
                  <Calendar className="w-3 h-3" />
                  {r.exit_date ? format(new Date(r.exit_date), "dd MMM yyyy") : "—"}
                </div>
              </button>
              <div className="px-5 pb-4 pt-1 border-t border-slate-200 dark:border-slate-700/30">
                {r.ticker && (
                  <OnwardLink
                    to={`/TradeHistory?ticker=${encodeURIComponent(r.ticker)}`}
                    label="View trade"
                    testId="reflection-view-trade"
                    className="text-xs"
                  />
                )}
              </div>
            </div>
          );
        })}
      </div>

      {selectedTrade && (
        <TradeReflectionModal
          trade={selectedTrade}
          open={!!selectedTrade}
          onClose={() => setSelectedTrade(null)}
        />
      )}
    </>
  );
}
