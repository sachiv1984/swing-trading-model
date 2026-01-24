import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { base44 } from "../api/base44Client";
import { Loader2, LayoutGrid, List, Plus, Edit2, LogOut, TrendingUp, TrendingDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import PageHeader from "@/components/ui/PageHeader";
import PositionCard from "@/components/positions/PositionCard";
import PositionModal from "@/components/positions/PositionModal";
import ExitModal from "@/components/positions/ExitModal";
import { DataTable, TableHeader, TableHead, TableBody, TableRow, TableCell } from "@/components/ui/DataTable";
import { cn } from "@/lib/utils";
import { differenceInDays } from "date-fns";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";

export default function Positions() {
  const [viewMode, setViewMode] = useState("grid");
  const [editingPosition, setEditingPosition] = useState(null);
  const [exitingPosition, setExitingPosition] = useState(null);
  const queryClient = useQueryClient();

  const { data: positions, isLoading } = useQuery({
    queryKey: ["positions", "open"],
    queryFn: () => base44.entities.Position.filter({ status: "open" }, "-entry_date"),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => base44.entities.Position.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
      setEditingPosition(null);
      setExitingPosition(null);
    },
  });

  const handleSave = (position) => {
    updateMutation.mutate({
      id: position.id,
      data: {
        current_price: position.current_price,
        stop_price: position.stop_price,
      },
    });
  };

  const handleExit = (position) => {
    updateMutation.mutate({
      id: position.id,
      data: {
        status: "closed",
        exit_date: position.exit_date,
        exit_price: position.exit_price,
        exit_reason: position.exit_reason,
        pnl: position.pnl,
        pnl_percent: position.pnl_percent,
      },
    });
  };

  const openPositions = positions || [];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Open Positions"
        description={`${openPositions.length} active position${openPositions.length !== 1 ? "s" : ""}`}
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

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      ) : openPositions.length === 0 ? (
        <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-12 text-center">
          <p className="text-slate-500 mb-4">No open positions</p>
          <Link to={createPageUrl("TradeEntry")}>
            <Button className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white">
              <Plus className="w-4 h-4 mr-2" />
              Enter First Position
            </Button>
          </Link>
        </div>
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
            <TableHead className="text-right">P&L</TableHead>
            <TableHead>Days</TableHead>
            <TableHead>Actions</TableHead>
          </TableHeader>
          <TableBody>
            {openPositions.map((position) => {
              const pnl = ((position.current_price || position.entry_price) - position.entry_price) * position.shares;
              const pnlPercent = ((position.current_price || position.entry_price) - position.entry_price) / position.entry_price * 100;
              const isProfit = pnl >= 0;
              const daysHeld = differenceInDays(new Date(), new Date(position.entry_date));
              const currencySymbol = position.market === "UK" ? "£" : "$";

              return (
                <TableRow key={position.id}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-white">{position.ticker}</span>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                        {position.market}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell className="text-slate-300">{currencySymbol}{position.entry_price.toFixed(2)}</TableCell>
                  <TableCell className="text-slate-300">{currencySymbol}{position.current_price?.toFixed(2) || "—"}</TableCell>
                  <TableCell className="text-rose-400 font-medium">{currencySymbol}{position.stop_price?.toFixed(2) || "—"}</TableCell>
                  <TableCell className="text-slate-300">{position.shares}</TableCell>
                  <TableCell className="text-right">
                    <div className={cn(
                      "inline-flex items-center gap-1.5 font-medium",
                      isProfit ? "text-emerald-400" : "text-rose-400"
                    )}>
                      {isProfit ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                      {currencySymbol}{Math.abs(pnl).toFixed(2)}
                      <span className="text-xs opacity-70">({pnlPercent.toFixed(1)}%)</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-slate-400">{daysHeld}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
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
    </div>
  );
}
