import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useEarnings } from "../hooks/useEarnings";
import { base44, api, apiFetch } from "../api/base44Client";
import {
  LayoutGrid,
  List,
  BookOpen,
  Plus,
  Edit2,
  LogOut,
  TrendingUp,
  TrendingDown,
  FolderOpen,
  AlertTriangle,
  X,
} from "lucide-react";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
import DataState from "../components/ui/DataState";
import { Button } from "../components/ui/button";
import PageHeader from "../components/ui/PageHeader";
import PositionCard from "../components/positions/PositionCard";
import PositionModal from "../components/positions/PositionModal";
import ExitModal from "../components/positions/ExitModal";
import JournalView from "../components/positions/JournalView";
import TradeReflectionModal from "../components/trades/TradeReflectionModal";
import {
  DataTable,
  TableHeader,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
} from "../components/ui/DataTable";
import { cn } from "../lib/utils";
import { friendlyErrorMessage } from "../lib/apiError";
import { differenceInDays } from "date-fns";
import { Link, useNavigate } from "react-router-dom";
import { createPageUrl } from "../utils";
import MetricsStalenessIndicator from "../components/analytics/MetricsStalenessIndicator";
import StrategyCompliancePanel from "../components/positions/StrategyCompliancePanel";

const LIFECYCLE_BADGE_COLOURS = {
  GRACE: "bg-blue-600",
  PROFITABLE: "bg-green-700",
  LOSING: "bg-red-600",
  "EXIT ZONE": "bg-violet-600",
  UNKNOWN: "bg-gray-500",
};

function DrawdownReviewPrompt() {
  const [dismissed, setDismissed] = useState(false);
  const { data } = useQuery({
    queryKey: ["drawdown-status"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/portfolio/drawdown-status`);
      const json = await res.json();
      return json?.data || {};
    },
    staleTime: 2 * 60 * 1000,
  });

  if (dismissed || !data?.threshold_breached) return null;

  const stateColours = {
    GRACE: "bg-blue-600",
    PROFITABLE: "bg-green-700",
    LOSING: "bg-red-600",
    "EXIT ZONE": "bg-violet-600",
    UNKNOWN: "bg-gray-500",
  };

  const statesByCount = Object.entries(data.positions_by_state || {}).filter(([, count]) => count > 0);

  return (
    <div className="rounded-lg bg-amber-50 border border-amber-300 p-4" role="alert">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-700 flex-shrink-0" aria-hidden="true" />
          <span className="font-semibold text-amber-900">Portfolio Drawdown Review</span>
        </div>
        <button
          onClick={() => setDismissed(true)}
          aria-label="Dismiss drawdown review prompt"
          className="text-amber-700 hover:text-amber-900 transition-colors flex-shrink-0"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
      <div className="mt-3 grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: "Current Drawdown", value: `${data.current_drawdown_pct?.toFixed(1) ?? "—"}%`, amber: true },
          { label: "Threshold", value: `${data.threshold_pct?.toFixed(1) ?? "—"}%` },
          { label: "Portfolio Heat", value: data.portfolio_heat_pct != null ? `${data.portfolio_heat_pct.toFixed(1)}%` : "—" },
          { label: "Regime", value: data.regime_status || "—" },
        ].map(({ label, value, amber }) => (
          <div key={label} className="bg-amber-100/60 rounded p-2">
            <p className="text-amber-700 text-xs font-medium">{label}</p>
            <p className={`text-sm font-bold mt-0.5 ${amber ? "text-amber-700" : "text-amber-900"}`}>{value}</p>
          </div>
        ))}
      </div>
      {statesByCount.length > 0 && (
        <div className="mt-3 flex flex-wrap items-center gap-2">
          <span className="text-xs text-amber-700 font-medium">Positions by state:</span>
          {statesByCount.map(([state, count]) => (
            <span
              key={state}
              className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs text-white font-medium ${stateColours[state] || "bg-gray-500"}`}
            >
              {state} <span className="opacity-80">{count}</span>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function ConcentrationLimitsWarning() {
  const { data } = useQuery({
    queryKey: ["concentration-status"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/portfolio/concentration-status`);
      const json = await res.json();
      return json?.data || {};
    },
    staleTime: 2 * 60 * 1000,
  });

  if (!data?.any_breach) return null;

  const { breaching_positions = [], breaching_sectors = [] } = data;

  return (
    <div className="rounded-lg bg-amber-50 border border-amber-300 p-4" role="alert">
      <div className="flex items-center gap-2">
        <AlertTriangle className="w-5 h-5 text-amber-700 flex-shrink-0" aria-hidden="true" />
        <span className="font-semibold text-amber-900">Concentration Limits</span>
      </div>
      {breaching_positions.length > 0 && (
        <div className="mt-3">
          <p className="text-xs text-amber-700 font-medium mb-1.5">
            Positions exceeding limit ({data.position_threshold_pct}% of portfolio heat):
          </p>
          <ul className="space-y-1">
            {breaching_positions.map((p) => (
              <li key={p.ticker} className="text-sm text-amber-900">
                <span className="font-semibold">{p.ticker}</span>
                {" — "}{p.heat_pct.toFixed(1)}% of heat{" "}
                <span className="text-amber-700 text-xs">(limit: {p.limit_pct}%)</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      {breaching_sectors.length > 0 && (
        <div className="mt-3">
          <p className="text-xs text-amber-700 font-medium mb-1.5">
            Sectors exceeding limit ({data.sector_threshold_pct}% concentration):
          </p>
          <ul className="space-y-1">
            {breaching_sectors.map((s) => (
              <li key={s.sector} className="text-sm text-amber-900">
                <span className="font-semibold">{s.sector}</span>
                {" — "}{s.concentration_pct.toFixed(1)}%{" "}
                <span className="text-amber-700 text-xs">(limit: {s.limit_pct}%)</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      <a
        href="/#/Settings"
        className="mt-3 inline-block text-xs text-amber-700 underline hover:text-amber-900"
        aria-label="Review portfolio concentration limit settings"
      >
        Review Settings
      </a>
    </div>
  );
}

function PositionEarningsCell({ ticker, market }) {
  const { data, loading } = useEarnings(ticker, market);
  if (loading) return <TableCell><span className="text-slate-600 text-xs">…</span></TableCell>;
  if (!data || data.days_until_earnings == null) return <TableCell><span className="text-slate-600 text-xs">—</span></TableCell>;
  const days = data.days_until_earnings;
  const isNear = days <= 5;
  return (
    <TableCell>
      <span
        className={`text-xs font-medium px-2 py-0.5 rounded ${isNear ? "bg-amber-500/15 text-amber-400 border border-amber-500/25" : "text-slate-400"}`}
        title={data.next_earnings_date}
      >
        {isNear ? `⚠ ${days}d` : `${days}d`}
      </span>
    </TableCell>
  );
}

export default function Positions() {
  const [viewMode, setViewMode] = useState("grid");
  const [editingPosition, setEditingPosition] = useState(null);
  const [exitingPosition, setExitingPosition] = useState(null);
  const [reflectionTrade, setReflectionTrade] = useState(null);

  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: positions, isLoading, isError, refetch } = useQuery({
    queryKey: ["positions"],
    queryFn: async () => {
      const result = await base44.entities.Position.list("-entry_date");
      console.log("Positions query result:", result);
      return result;
    },
  });

  const { data: availableTags = [] } = useQuery({
    queryKey: ["position-tags"],
    queryFn: async () => {
      const positionsList = await base44.entities.Position.list();
      const allTags = positionsList.flatMap((p) => p.tags || []);
      return [...new Set(allTags)].sort();
    },
  });

  // FIXED: Exit mutation now accepts exitData directly from ExitModal
  const exitMutation = useMutation({
    mutationFn: (exitData) => {
      // exitData contains:
      // { position_id, shares, exit_price, exit_date, exit_reason, fx_rate }
      console.log("Exit mutation received:", exitData);

      // Pass the entire exitData object - base44Client handles it
      return base44.entities.Position.exit(exitData);
    },
    onSuccess: async (data) => {
      console.log("Exit successful:", data);

      // Aggressive cache invalidation
      queryClient.invalidateQueries({ queryKey: ["positions"] });
      queryClient.invalidateQueries({ queryKey: ["portfolio"] });
      queryClient.invalidateQueries({ queryKey: ["trades"] });

      // Optional refetch
      queryClient.refetchQueries({ queryKey: ["positions", "open"] });
      queryClient.refetchQueries({ queryKey: ["portfolio"] });

      setExitingPosition(null);

      // Trigger reflection modal: fetch the most recent trade to get trade ID and backend data
      try {
        const tradesResult = await api.trades.list();
        const trades = tradesResult?.trades || [];
        if (trades.length > 0) {
          setReflectionTrade(trades[0]);
        }
      } catch (e) {
        // Non-critical — skip reflection modal if trade fetch fails
      }
    },
    onError: (error) => {
      console.error("Exit failed:", error);
      alert(`Failed to exit position: ${friendlyErrorMessage(error)}`);
    },
  });

  // ✅ FIXED: Updated handleSave to only update notes and tags
  const handleSave = async (position) => {
    try {
      await base44.entities.Position.updateNote(
        position.id,
        position.entry_note || ""
      );

      await base44.entities.Position.updateTags(position.id, position.tags || []);

      queryClient.invalidateQueries({ queryKey: ["positions"] });
      setEditingPosition(null);
    } catch (error) {
      console.error("Failed to save position:", error);
      alert(`Failed to save changes: ${friendlyErrorMessage(error)}`);
    }
  };

  // FIXED: handleExit passes exitData through to mutation
  const handleExit = (exitData) => {
    console.log("handleExit called with:", exitData);

    if (!exitData.position_id) {
      alert("Invalid position data");
      return;
    }

    if (!exitData.shares || exitData.shares <= 0) {
      alert("Invalid number of shares");
      return;
    }

    if (!exitData.exit_price || exitData.exit_price <= 0) {
      alert("Invalid exit price");
      return;
    }

    exitMutation.mutate(exitData);
  };

  const allPositions = positions || [];
  const openPositions = allPositions.filter((p) => p.status === "open");

  return (
    <div className="space-y-6">
      <PageHeader
        title={viewMode === "journal" ? "Trade Journal" : "Open Positions"}
        description={
          viewMode === "journal"
            ? `${allPositions.length} total entries`
            : `${openPositions.length} active position${
                openPositions.length !== 1 ? "s" : ""
              }`
        }
        actions={
          <div className="flex items-center gap-3">
            <div className="flex items-center rounded-xl bg-slate-800/50 border border-slate-700/50 p-1">
              <Button
                aria-label="Grid view"
                variant="ghost"
                size="sm"
                onClick={() => setViewMode("grid")}
                className={cn(
                  "h-8 w-8 p-0 rounded-lg",
                  viewMode === "grid"
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400"
                    : "text-slate-400 hover:text-white"
                )}
              >
                <LayoutGrid className="w-4 h-4" />
              </Button>

              <Button
                aria-label="Table view"
                variant="ghost"
                size="sm"
                onClick={() => setViewMode("table")}
                className={cn(
                  "h-8 w-8 p-0 rounded-lg",
                  viewMode === "table"
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400"
                    : "text-slate-400 hover:text-white"
                )}
              >
                <List className="w-4 h-4" />
              </Button>

              <Button
                aria-label="Journal view"
                variant="ghost"
                size="sm"
                onClick={() => setViewMode("journal")}
                className={cn(
                  "h-8 w-8 p-0 rounded-lg",
                  viewMode === "journal"
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400"
                    : "text-slate-400 hover:text-white"
                )}
              >
                <BookOpen className="w-4 h-4" />
              </Button>
            </div>

            <Link to={createPageUrl("TradeEntry")}>
              <Button className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25">
                <Plus className="w-4 h-4 mr-2" />
                New Position
              </Button>
            </Link>
          </div>
        }
      />

      {/* ST-02 (BLG-FEAT-09): Metrics staleness indicator — below title, inline with view controls */}
      <MetricsStalenessIndicator />

      {/* IT-04 (Arc 3): Drawdown review prompt — portfolio-level, highest severity */}
      <DrawdownReviewPrompt />

      {/* IT-05 (Arc 3): Concentration limits warning — portfolio-level, structural */}
      <ConcentrationLimitsWarning />

      {/* ST-12 (BLG-FE-02): DataState standardised loading/empty/error — Table/Grid views */}
      <DataState
        loading={isLoading}
        error={isError}
        onRetry={refetch}
        className="min-h-[300px]"
        empty={!isLoading && !isError && viewMode !== "journal" && openPositions.length === 0}
        emptyIcon={<FolderOpen className="w-10 h-10 text-slate-600" />}
        emptyHeading="No open positions"
        emptyBody="Enter a trade to see your positions here."
        emptyAction={
          <Link to={createPageUrl("TradeEntry")}>
            <Button className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0">
              <Plus className="w-4 h-4 mr-2" />
              Enter First Position
            </Button>
          </Link>
        }
      >
        {viewMode === "journal" ? (
          <JournalView positions={allPositions} availableTags={availableTags} />
        ) : viewMode === "grid" ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {openPositions.map((position) => (
            <PositionCard
              key={position.id}
              position={position}
              onEdit={setEditingPosition}
              onExit={setExitingPosition}
            />
          ))}
        </div>
      ) : (
        <DataTable>
          <TableHeader>
            <TableHead>Ticker</TableHead>
            <TableHead>Entry Price</TableHead>
            <TableHead>Current Price</TableHead>
            <TableHead>Stop</TableHead>
            <TableHead>Shares</TableHead>
            <TableHead className="text-right">P&amp;L (GBP)</TableHead>
            <TableHead className="text-right">P&amp;L %</TableHead>
            <TableHead>Days</TableHead>
            <TableHead>Grace</TableHead>
            <TableHead title="Days until next earnings">Earnings</TableHead>
            <TableHead>Actions</TableHead>
          </TableHeader>

          <TableBody>
            {openPositions.map((position) => {
              // P&L is already calculated in GBP by backend
              const pnl = position.pnl || 0;
              const pnlPercent = position.pnl_percent || 0;
              const isProfit = pnl >= 0;
              const daysHeld = differenceInDays(
                new Date(),
                new Date(position.entry_date)
              );

              const currencySymbol = position.market === "UK" ? "£" : "$";

              // Use native prices for display
              const displayCurrentPrice =
                position.current_price_native || position.current_price;
              const displayStopPrice =
                position.stop_price_native || position.stop_price;

              return (
                <TableRow key={position.id}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-white">
                        {position.ticker}
                      </span>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                        {position.market}
                      </span>
                    </div>
                  </TableCell>

                  <TableCell className="text-slate-300">
                    {currencySymbol}
                    {position.entry_price.toFixed(2)}
                  </TableCell>

                  <TableCell className="text-slate-300">
                    {currencySymbol}
                    {displayCurrentPrice?.toFixed(2) || "—"}
                  </TableCell>

                  <TableCell className="text-rose-400 font-medium">
                    {currencySymbol}
                    {displayStopPrice?.toFixed(2) || "—"}
                  </TableCell>

                  <TableCell className="text-slate-300">
                    {position.shares}
                  </TableCell>

                  <TableCell className="text-right">
                    <div
                      className={cn(
                        "inline-flex items-center gap-1.5 font-medium",
                        isProfit ? "text-emerald-400" : "text-rose-400"
                      )}
                    >
                      {isProfit ? (
                        <TrendingUp className="w-4 h-4" />
                      ) : (
                        <TrendingDown className="w-4 h-4" />
                      )}
                      £{Math.abs(pnl).toFixed(2)}
                    </div>
                  </TableCell>

                  <TableCell className="text-right">
                    <span
                      className={cn(
                        "text-sm font-medium",
                        isProfit ? "text-emerald-400" : "text-rose-400"
                      )}
                    >
                      {isProfit ? "+" : ""}{pnlPercent.toFixed(1)}%
                    </span>
                  </TableCell>

                  <TableCell className="text-slate-400">{daysHeld}</TableCell>

                  {/* BLG-FEAT-06: Grace Days Remaining */}
                  <TableCell>
                    {position.grace_days_remaining !== null &&
                    position.grace_days_remaining !== undefined ? (
                      <span className="text-xs font-medium px-2 py-1 rounded-lg bg-amber-500/15 text-amber-400 border border-amber-500/25 whitespace-nowrap">
                        Day {(position.holding_days ?? 0) + 1} of 10
                      </span>
                    ) : (
                      <span className="text-slate-600">—</span>
                    )}
                  </TableCell>

                  <PositionEarningsCell ticker={position.ticker} market={position.market} />

                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 text-slate-400 hover:text-white hover:bg-slate-800"
                        onClick={() => setEditingPosition(position)}
                      >
                        <Edit2 className="w-4 h-4" />
                      </Button>

                      <Button
                        variant="ghost"
                        size="icon"
                        title="Trade Plan"
                        className="h-8 w-8 text-cyan-500/70 hover:text-cyan-400 hover:bg-cyan-500/10"
                        onClick={() => navigate(`/TradePlan?position_id=${position.id}&ticker=${position.ticker}&market=${position.market}`)}
                      >
                        <BookOpen className="w-4 h-4" />
                      </Button>

                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 text-rose-400 hover:text-rose-300 hover:bg-rose-500/10"
                        onClick={() => setExitingPosition(position)}
                      >
                        <LogOut className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </DataTable>
      )}
      </DataState>

      {/* ST-01 (BLG-FEAT-11): Strategy Compliance Panel — Table View only; display-only §13.3 */}
      {viewMode === "table" && openPositions.length > 0 && (
        <StrategyCompliancePanel />
      )}

      <PositionModal
        position={editingPosition}
        open={!!editingPosition}
        onClose={() => setEditingPosition(null)}
        onSave={handleSave}
      />

      <ExitModal
        position={exitingPosition}
        open={!!exitingPosition}
        onClose={() => setExitingPosition(null)}
        onConfirm={handleExit}
      />

      <TradeReflectionModal
        trade={reflectionTrade}
        open={!!reflectionTrade}
        onClose={() => setReflectionTrade(null)}
      />
    </div>
  );
}
