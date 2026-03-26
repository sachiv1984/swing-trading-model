import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { base44, api } from "../api/base44Client";
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
} from "lucide-react";
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
import { differenceInDays } from "date-fns";
import { Link } from "react-router-dom";
import { createPageUrl } from "../utils";

export default function Positions() {
  const [viewMode, setViewMode] = useState("grid");
  const [editingPosition, setEditingPosition] = useState(null);
  const [exitingPosition, setExitingPosition] = useState(null);
  const [reflectionTrade, setReflectionTrade] = useState(null);

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
      alert(`Failed to exit position: ${error.message}`);
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
      alert(`Failed to save changes: ${error.message}`);
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

      <DataState
        loading={isLoading}
        error={isError}
        onRetry={refetch}
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
            <TableHead className="text-right">P&amp;L</TableHead>
            <TableHead>Days</TableHead>
            <TableHead>Grace</TableHead>
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
                      <span className="text-xs opacity-70">
                        ({pnlPercent.toFixed(1)}%)
                      </span>
                    </div>
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
