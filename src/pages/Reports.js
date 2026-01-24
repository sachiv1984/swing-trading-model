import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "@/api/base44Client";
import { 
  FileText, 
  Download, 
  Calendar, 
  TrendingUp, 
  TrendingDown,
  BarChart3,
  PieChart,
  Loader2,
  FileSpreadsheet,
  FileDown
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import PageHeader from "@/components/ui/PageHeader";
import StatsCard from "@/components/ui/StatsCard";
import PerformanceSummary from "@/components/reports/PerformanceSummary";
import PortfolioGrowthChart from "@/components/reports/PortfolioGrowthChart";
import TradeBreakdown from "@/components/reports/TradeBreakdown";
import ExportModal from "@/components/reports/ExportModal";
import { motion } from "framer-motion";

export default function Reports() {
  const [period, setPeriod] = useState("month");
  const [exportModalOpen, setExportModalOpen] = useState(false);
  const [dateRange, setDateRange] = useState({ start: null, end: null });

  const { data: positions, isLoading: loadingPositions } = useQuery({
    queryKey: ["allPositions"],
    queryFn: () => base44.entities.Position.list("-exit_date"),
  });

  const { data: portfolios } = useQuery({
    queryKey: ["portfolios"],
    queryFn: () => base44.entities.Portfolio.list(),
  });

  const portfolio = portfolios?.[0];

  // Calculate date range based on period
  const periodDates = useMemo(() => {
    const now = new Date();
    let start = new Date();
    
    switch (period) {
      case "week":
        start.setDate(now.getDate() - 7);
        break;
      case "month":
        start.setMonth(now.getMonth() - 1);
        break;
      case "quarter":
        start.setMonth(now.getMonth() - 3);
        break;
      case "year":
        start.setFullYear(now.getFullYear() - 1);
        break;
      case "ytd":
        start = new Date(now.getFullYear(), 0, 1);
        break;
      case "all":
        start = new Date(2020, 0, 1);
        break;
      default:
        start.setMonth(now.getMonth() - 1);
    }
    
    return { start, end: now };
  }, [period]);

  // Filter positions by date range
  const filteredPositions = useMemo(() => {
    if (!positions) return [];
    
    const range = dateRange.start ? dateRange : periodDates;
    
    return positions.filter(p => {
      const exitDate = p.exit_date ? new Date(p.exit_date) : null;
      const entryDate = new Date(p.entry_date);
      
      // Include if position was active during the period
      return entryDate <= range.end && (!exitDate || exitDate >= range.start);
    });
  }, [positions, periodDates, dateRange]);

  // Calculate performance metrics
  const metrics = useMemo(() => {
    const closedTrades = filteredPositions.filter(p => p.status === "closed");
    const openTrades = filteredPositions.filter(p => p.status === "open");
    
    const totalPnL = closedTrades.reduce((sum, p) => sum + (p.pnl || 0), 0);
    const winningTrades = closedTrades.filter(p => (p.pnl || 0) > 0);
    const losingTrades = closedTrades.filter(p => (p.pnl || 0) < 0);
    
    const grossProfit = winningTrades.reduce((sum, p) => sum + (p.pnl || 0), 0);
    const grossLoss = Math.abs(losingTrades.reduce((sum, p) => sum + (p.pnl || 0), 0));
    
    const avgWin = winningTrades.length > 0 ? grossProfit / winningTrades.length : 0;
    const avgLoss = losingTrades.length > 0 ? grossLoss / losingTrades.length : 0;
    
    const winRate = closedTrades.length > 0 
      ? (winningTrades.length / closedTrades.length) * 100 
      : 0;
    
    const profitFactor = grossLoss > 0 ? grossProfit / grossLoss : grossProfit > 0 ? Infinity : 0;
    
    const totalFees = closedTrades.reduce((sum, p) => sum + (p.fees || 0), 0);
    
    return {
      totalPnL,
      winRate,
      totalTrades: closedTrades.length,
      winningTrades: winningTrades.length,
      losingTrades: losingTrades.length,
      grossProfit,
      grossLoss,
      avgWin,
      avgLoss,
      profitFactor,
      totalFees,
      openPositions: openTrades.length,
      bestTrade: closedTrades.length > 0 ? Math.max(...closedTrades.map(p => p.pnl || 0)) : 0,
      worstTrade: closedTrades.length > 0 ? Math.min(...closedTrades.map(p => p.pnl || 0)) : 0,
    };
  }, [filteredPositions]);

  const periodLabels = {
    week: "Last 7 Days",
    month: "Last Month",
    quarter: "Last Quarter",
    year: "Last Year",
    ytd: "Year to Date",
    all: "All Time"
  };

  const isLoading = loadingPositions;

  return (
    <div className="space-y-8">
      <PageHeader
        title="Reports"
        description="Performance analysis and export tools"
        actions={
          <div className="flex items-center gap-3">
            <Select value={period} onValueChange={setPeriod}>
              <SelectTrigger className="w-40 bg-slate-800/50 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="week">Last 7 Days</SelectItem>
                <SelectItem value="month">Last Month</SelectItem>
                <SelectItem value="quarter">Last Quarter</SelectItem>
                <SelectItem value="year">Last Year</SelectItem>
                <SelectItem value="ytd">Year to Date</SelectItem>
                <SelectItem value="all">All Time</SelectItem>
              </SelectContent>
            </Select>
            <Button
              onClick={() => setExportModalOpen(true)}
              className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-600 hover:to-violet-600 text-white"
            >
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
          </div>
        }
      />

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      ) : (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatsCard
              title="Total P&L"
              value={`${metrics.totalPnL >= 0 ? "+" : ""}£${metrics.totalPnL.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
              subtitle={periodLabels[period]}
              icon={metrics.totalPnL >= 0 ? TrendingUp : TrendingDown}
              gradient={metrics.totalPnL >= 0 ? "emerald" : "rose"}
 
