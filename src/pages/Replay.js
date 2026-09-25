/**
 * Replay Mode — PO-05 Lightweight Replay Mode (ST-01c, EPIC-01, v9.7, BLG-FEAT-74)
 *
 * Design source: docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md
 * Wire contract: docs/product/decisions/po05_replay_scope_confirmation.md (rev 3)
 * Spec: docs/specs/frontend/pages/replay_mode.md v0.2
 * API: POST /replay/run — docs/specs/api_contracts/replay_endpoints.md
 *
 * §13 boundary (binding — see the design source's §13 Boundary section):
 * this page has NO control that writes to real positions/trade_history or adjusts
 * real strategy parameters, stop multipliers, or risk percentages. The retrospective
 * banner is always the first element of a populated/empty output view and its wording
 * is rendered from the server's own `data.retrospective_notice` field, with an
 * identical hard-coded fallback literal below so a missing/renamed field can never
 * silently drop the banner (replay_endpoints.md's own field note).
 */
import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, Calendar, Loader2 } from "lucide-react";
import { api } from "../api/base44Client";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Checkbox } from "../components/ui/checkbox";
import { StandingAlert } from "../components/ui/StandingAlert";
import PageHeader from "../components/ui/PageHeader";
import { formatCurrency, formatPercent } from "../lib/format";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

// Binding Condition 2 fallback — kept identical to the backend's own
// services/replay_service.py::RETROSPECTIVE_NOTICE constant. Used only if the
// server response is ever missing the field; the server value is always preferred.
const RETROSPECTIVE_NOTICE_FALLBACK =
  "Retrospective result — shows what the current rules would have produced over " +
  "this past period. Not a prediction of future performance.";

// Reuses StrategyBenchmark.js's exit-reason badge convention (Stop = red, Risk-Off =
// amber) for visual consistency with the existing backtest-style view. "Actual Exit"
// is deliberately not in this map — no rule fired before the trade's own real exit
// date, so it renders as plain text (replay_endpoints.md's own field note).
const EXIT_REASON_BADGE = {
  Stop: { label: "Stop", cls: "bg-red-600 text-white" },
  "Risk-Off": { label: "Risk-Off", cls: "bg-amber-600 text-white" },
};

function ExitReasonBadge({ reason }) {
  const config = EXIT_REASON_BADGE[reason] || null;
  if (!config) {
    return <span className="text-xs text-slate-600 dark:text-slate-400">{reason || "—"}</span>;
  }
  return (
    <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${config.cls}`}>{config.label}</span>
  );
}

const SKIPPED_REASON_LABEL = {
  trade_not_found: "not found",
  price_data_unavailable: "price data unavailable",
  insufficient_history: "insufficient price history",
};

export default function Replay() {
  const [mode, setMode] = useState("date_range");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [selectedTradeIds, setSelectedTradeIds] = useState(() => new Set());
  const [runState, setRunState] = useState("idle"); // idle | running | success | failure
  const [result, setResult] = useState(null);

  const { data: tradesData, isLoading: tradesLoading } = useQuery({
    queryKey: ["replay-trade-list"],
    queryFn: () => api.trades.list(),
    enabled: mode === "trade_set",
    staleTime: 30000,
  });
  const closedTrades = tradesData?.trades ?? [];

  const canRun = useMemo(() => {
    if (mode === "date_range") return !!dateFrom && !!dateTo;
    return selectedTradeIds.size > 0;
  }, [mode, dateFrom, dateTo, selectedTradeIds]);

  const toggleTrade = (id) => {
    setSelectedTradeIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const switchMode = (nextMode) => {
    // A fresh mode switch clears any prior run's output (decision_record.md §2.2:
    // two mutually exclusive input modes) -- not specified explicitly, but leaving a
    // stale result from the other mode visible while the selector shows a different
    // mode's controls would be confusing; the initial-state prompt is more honest.
    setMode(nextMode);
    setRunState("idle");
    setResult(null);
  };

  const handleRunReplay = async () => {
    if (!canRun || runState === "running") return;
    setRunState("running");
    try {
      const body = mode === "date_range" ? { date_from: dateFrom, date_to: dateTo } : { trade_ids: Array.from(selectedTradeIds) };
      const res = await fetch(`${API_BASE}/replay/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const json = await res.json();
      if (!res.ok || json.status !== "ok") {
        setRunState("failure");
        return;
      }
      setResult(json.data);
      setRunState("success");
    } catch {
      setRunState("failure");
    }
  };

  const skipped = result?.run?.skipped ?? [];
  const trades = result?.trades ?? [];

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      <PageHeader title="Replay Mode" description="Replay your own past trades through today's strategy rules." />

      {/* Selector — decision_record.md §2.2: two mutually exclusive, tab-switched input modes */}
      <div className="bg-slate-800/50 rounded-lg border border-slate-700/50 p-5 space-y-4">
        <div className="flex gap-1" data-testid="replay-mode-tabs">
          <button
            type="button"
            data-testid="replay-mode-tab-date-range"
            onClick={() => switchMode("date_range")}
            className={`text-sm px-3 py-1.5 rounded-md border transition-colors ${
              mode === "date_range"
                ? "border-slate-400 bg-slate-700 text-white"
                : "border-slate-700 text-slate-600 dark:text-slate-400 hover:text-slate-300 hover:bg-slate-800"
            }`}
          >
            Date Range
          </button>
          <button
            type="button"
            data-testid="replay-mode-tab-trade-set"
            onClick={() => switchMode("trade_set")}
            className={`text-sm px-3 py-1.5 rounded-md border transition-colors ${
              mode === "trade_set"
                ? "border-slate-400 bg-slate-700 text-white"
                : "border-slate-700 text-slate-600 dark:text-slate-400 hover:text-slate-300 hover:bg-slate-800"
            }`}
          >
            Trade Set
          </button>
        </div>

        {mode === "date_range" ? (
          <div className="flex flex-wrap gap-3" data-testid="replay-date-range-controls">
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <Input
                type="date"
                data-testid="replay-date-from"
                aria-label="Date from"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="bg-slate-800/50 border-slate-700 text-white pl-10"
              />
            </div>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <Input
                type="date"
                data-testid="replay-date-to"
                aria-label="Date to"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="bg-slate-800/50 border-slate-700 text-white pl-10"
              />
            </div>
          </div>
        ) : (
          <div data-testid="replay-trade-set-controls" className="max-h-80 overflow-y-auto rounded-lg border border-slate-700/50 divide-y divide-slate-700/30">
            {tradesLoading ? (
              <div className="p-4 text-sm text-slate-600 dark:text-slate-400">Loading your closed trades…</div>
            ) : closedTrades.length === 0 ? (
              <div className="p-4 text-sm text-slate-600 dark:text-slate-400">No closed trades to select from yet.</div>
            ) : (
              closedTrades.map((t) => (
                <label
                  key={t.id}
                  htmlFor={`replay-trade-checkbox-${t.id}`}
                  className="flex items-center gap-3 px-4 py-2.5 cursor-pointer hover:bg-slate-700/20"
                >
                  <Checkbox
                    id={`replay-trade-checkbox-${t.id}`}
                    data-testid={`replay-trade-checkbox-${t.id}`}
                    checked={selectedTradeIds.has(t.id)}
                    onCheckedChange={() => toggleTrade(t.id)}
                  />
                  <span className="text-sm text-white font-medium">{t.ticker}</span>
                  <span className="text-xs text-slate-600 dark:text-slate-400">exited {t.exit_date}</span>
                </label>
              ))
            )}
          </div>
        )}

        <Button
          data-testid="replay-run-button"
          onClick={handleRunReplay}
          disabled={!canRun || runState === "running"}
          className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0"
        >
          {runState === "running" ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Running…
            </>
          ) : (
            "Run Replay"
          )}
        </Button>
      </div>

      {/* Output view */}
      {runState === "idle" && (
        <p data-testid="replay-empty-state" className="text-sm text-slate-600 dark:text-slate-400">
          Select a date range or trade set, then run a replay.
        </p>
      )}

      {runState === "failure" && (
        <div data-testid="replay-failure-banner" className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-6 text-center">
          <p className="text-rose-300 text-sm">Couldn't run the replay. Try again.</p>
        </div>
      )}

      {runState === "success" && (
        <div className="space-y-4" data-testid="replay-output-view">
          <div data-testid="replay-retrospective-banner">
            <StandingAlert severity="info" dismissible={false} message={result.retrospective_notice || RETROSPECTIVE_NOTICE_FALLBACK} />
          </div>

          {trades.length === 0 ? (
            <>
              <p data-testid="replay-empty-result" className="text-sm text-slate-600 dark:text-slate-400">
                No closed trades in the selected range/set.
              </p>
              {skipped.length > 0 && (
                <SkippedNotice skipped={skipped} />
              )}
            </>
          ) : (
            <>
              {/* Summary row */}
              <div className="grid grid-cols-3 gap-4">
                <div className="rounded-xl border border-slate-700/50 bg-slate-800/50 p-4">
                  <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Trades Replayed</p>
                  <p data-testid="replay-summary-trade-count" className="text-xl font-bold text-white">
                    {result.summary.trade_count}
                  </p>
                </div>
                <div className="rounded-xl border border-slate-700/50 bg-slate-800/50 p-4">
                  <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Win Rate</p>
                  <p data-testid="replay-summary-win-rate" className="text-xl font-bold text-white">
                    {formatPercent(result.summary.win_rate_pct)}
                  </p>
                </div>
                <div className="rounded-xl border border-slate-700/50 bg-slate-800/50 p-4">
                  <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Total Simulated P&L</p>
                  <p
                    data-testid="replay-summary-total-pnl"
                    className={`text-xl font-bold ${
                      result.summary.total_simulated_pnl_gbp > 0
                        ? "text-emerald-400"
                        : result.summary.total_simulated_pnl_gbp < 0
                        ? "text-rose-400"
                        : "text-slate-600 dark:text-slate-400"
                    }`}
                  >
                    {formatCurrency(result.summary.total_simulated_pnl_gbp, { signed: true })}
                  </p>
                </div>
              </div>

              {/* Independence note (scope note §7 item 3a) */}
              <p data-testid="replay-independence-note" className="text-xs text-slate-600 dark:text-slate-400">
                Each trade is replayed independently — there is no shared cash, position limit, or chronology between the trades shown here.
              </p>

              {skipped.length > 0 && <SkippedNotice skipped={skipped} />}

              {/* FX-basis caption (scope note §7 item 2) */}
              <p data-testid="replay-fx-basis-caption" className="text-xs text-slate-600 dark:text-slate-400">
                GBP figures use each trade's recorded entry exchange rate.
              </p>

              {/* Results table */}
              <div className="bg-slate-800/50 rounded-lg border border-slate-700/50 overflow-hidden">
                <table className="w-full text-sm" data-testid="replay-results-table">
                  <thead>
                    <tr className="border-b border-slate-700/50">
                      <th className="px-5 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Ticker</th>
                      <th className="px-5 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Entry Date</th>
                      <th className="px-5 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Simulated Exit Date</th>
                      <th className="px-5 py-3 text-right text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Simulated P&L</th>
                      <th className="px-5 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Exit Reason</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-700/30">
                    {trades.map((t) => (
                      <tr key={t.trade_id} data-testid={`replay-result-row-${t.trade_id}`} className="hover:bg-slate-700/20 transition-colors">
                        <td className="px-5 py-3 text-white font-medium">{t.ticker}</td>
                        <td className="px-5 py-3 text-slate-300">{t.entry_date}</td>
                        <td className="px-5 py-3 text-slate-300">{t.simulated_exit_date}</td>
                        <td
                          className={`px-5 py-3 text-right font-medium ${
                            t.simulated_pnl_gbp == null
                              ? "text-slate-600 dark:text-slate-400"
                              : t.simulated_pnl_gbp > 0
                              ? "text-emerald-400"
                              : t.simulated_pnl_gbp < 0
                              ? "text-rose-400"
                              : "text-slate-600 dark:text-slate-400"
                          }`}
                        >
                          {formatCurrency(t.simulated_pnl_gbp, { signed: true })}
                        </td>
                        <td className="px-5 py-3">
                          <ExitReasonBadge reason={t.simulated_exit_reason} />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

function SkippedNotice({ skipped }) {
  const byReason = skipped.reduce((acc, s) => {
    acc[s.reason] = (acc[s.reason] || 0) + 1;
    return acc;
  }, {});
  const parts = Object.entries(byReason).map(([reason, count]) => `${count} ${SKIPPED_REASON_LABEL[reason] || reason}`);
  return (
    <p data-testid="replay-skipped-notice" className="text-xs text-amber-600 dark:text-amber-400 flex items-start gap-1.5">
      <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" aria-hidden="true" />
      {skipped.length === 1 ? "1 trade" : `${skipped.length} trades`} could not be replayed ({parts.join(", ")}).
    </p>
  );
}
