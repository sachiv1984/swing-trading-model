import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "../api/base44Client";
import { Loader2, Filter, TrendingUp, TrendingDown, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import PageHeader from "@/components/ui/PageHeader";
import StatsCard from "@/components/ui/StatsCard";
import TradeHistoryTable from "@/components/trades/TradeHistoryTable";
import PnLBarChart from "@/components/charts/PnLBarChart";
import WinRateChart from "@/components/charts/WinRateChart";
import { motion } from "framer-motion";

export default function TradeHistory() {
  const [filters, setFilters] = useState({
    market: "all",
    result: "all",
    dateFrom: "",
    dateTo: "",
  });

  const { data: closedPositions, isLoading } = useQuery({
    queryKey: ["positions", "closed"],
    queryFn: () => base44.entities.Position.filter({ status: "closed" }, "-exit_date"),
  });

  const trades = closedPositions || [];

  // Apply filters
  const filteredTrades = trades.filter((trade) => {
    if (filters.market !== "all" && trade.market !== filters.market) return false;
    if (filters.result === "win" && trade.pnl < 0) return false;
    if (filters.result === "loss" && trade.pnl >= 0) return false;
    if (filters.dateFrom && trade.exit_date < filters.dateFrom) return false;
    if (filters.dateTo && trade.exit_date > filters.dateTo) return false;
    return true;
  });

  // Calculate stats
  const totalPnL = filteredTrades.reduce((sum, t) => sum + (t.pnl || 0), 0);
  const winningTrades = filteredTrades.filter((t) => t.pnl >= 0);
  const losingTrades = filteredTrades.filter((t) => t.pnl < 0);
  const winRate = filteredTrades.length > 0 
    ? (winningTrades.length / filteredTrades.length) * 100 
    : 0;
  const avgWin = winningTrades.length > 0
    ? winningTrades.reduce((sum, t) => sum + t.pnl, 0) / winningTrades.length
    : 0;
  const avgLoss = losingTrades.length > 0
    ? losingTrades.reduce((sum, t) => sum + t.pnl, 0) / losingTrades.length
    : 0;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Trade History"
        description="Review your closed positions and performance"
      />

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      ) : (
        <>
          {/* Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatsCard
              title="Total P&L"
              value={`${totalPnL >= 0 ? "+" : ""}£${totalPnL.toFixed(2)}`}
              trend={totalPnL >= 0 ? "up" : "down"}
              icon={totalPnL >= 0 ? TrendingUp : TrendingDown}
              gradient={totalPnL >= 0 ? "emerald" : "rose"}
            />
            <StatsCard
              title="Win Rate"
              value={`${winRate.toFixed(1)}%`}
              subtitle={`${winningTrades.length}W / ${losingTrades.length}L`}
              trend={winRate >= 50 ? "up" : "down"}
              gradient="violet"
            />
            <StatsCard
              title="Avg Win"
              value={`+£${avgWin.toFixed(2)}`}
              trend="up"
              gradient="emerald"
            />
            <StatsCard
              title="Avg Loss"
              value={`£${Math.abs(avgLoss).toFixed(2)}`}
              trend="down"
              gradient="rose"
            />
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <PnLBarChart trades={filteredTrades} />
            </div>
            <div>
              <WinRateChart 
                winRate={winRate} 
                wins={winningTrades.length} 
                losses={losingTrades.length} 
              />
            </div>
          </div>

          {/* Filters */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-5"
          >
            <div className="flex items-center gap-2 mb-4">
              <Filter className="w-4 h-4 text-cyan-400" />
              <span className="text-sm font-medium text-slate-300">Filters</span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Select
                value={filters.market}
                onValueChange={(value) => setFilters({ ...filters, market: value })}
              >
                <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white">
                  <SelectValue placeholder="Market" />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="all">All Markets</SelectItem>
                  <SelectItem value="UK">UK</SelectItem>
                  <SelectItem value="US">US</SelectItem>
                </SelectContent>
              </Select>

              <Select
                value={filters.result}
                onValueChange={(value) => setFilters({ ...filters, result: value })}
              >
                <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white">
                  <SelectValue placeholder="Result" />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="all">All Results</SelectItem>
                  <SelectItem value="win">Winners</SelectItem>
                  <SelectItem value="loss">Losers</SelectItem>
                </SelectContent>
              </Select>

              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input
                  type="date"
                  value={filters.dateFrom}
                  onChange={(e) => setFilters({ ...filters, dateFrom: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white pl-10"
                  placeholder="From"
                />
              </div>

              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input
                  type="date"
                  value={filters.dateTo}
                  onChange={(e) => setFilters({ ...filters, dateTo: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white pl-10"
                  placeholder="To"
                />
              </div>
            </div>
          </motion.div>

          {/* Trade Table */}
          <TradeHistoryTable trades={filteredTrades} />

          {filteredTrades.length > 0 && (
            <p className="text-center text-sm text-slate-500">
              Showing {filteredTrades.length} of {trades.length} trades
            </p>
          )}
        </>
      )}
    </div>
  );
}
