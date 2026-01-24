import StatsCard from "../ui/StatsCard";
import { Wallet, TrendingUp, Briefcase, PieChart, Award, Clock } from "lucide-react";

export function PortfolioValueWidget({ portfolio, totalPositionsValue }) {
  const value = portfolio?.total_value || totalPositionsValue + (portfolio?.cash_balance || 0);
  return (
    <StatsCard
      title="Portfolio Value"
      value={`£${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
      icon={Wallet}
      gradient="cyan"
    />
  );
}

export function CashBalanceWidget({ portfolio }) {
  return (
    <StatsCard
      title="Cash Balance"
      value={`£${(portfolio?.cash_balance || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
      icon={Briefcase}
      gradient="violet"
    />
  );
}

export function OpenPositionsWidget({ totalPositionsValue, positionsCount }) {
  return (
    <StatsCard
      title="Open Positions"
      value={`£${totalPositionsValue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
      subtitle={`${positionsCount} position${positionsCount !== 1 ? "s" : ""}`}
      icon={PieChart}
      gradient="fuchsia"
    />
  );
}

export function TotalPnLWidget({ totalPnL, totalPositionsValue }) {
  return (
    <StatsCard
      title="Total P&L"
      value={`${totalPnL >= 0 ? "+" : ""}£${totalPnL.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
      trend={totalPnL >= 0 ? "up" : "down"}
      trendValue={`${totalPnL >= 0 ? "+" : ""}${((totalPnL / (totalPositionsValue || 1)) * 100).toFixed(2)}%`}
      icon={TrendingUp}
      gradient={totalPnL >= 0 ? "emerald" : "rose"}
    />
  );
}

export function WinRateWidget({ closedPositions }) {
  const wins = closedPositions?.filter(p => (p.pnl || 0) > 0).length || 0;
  const total = closedPositions?.length || 0;
  const winRate = total > 0 ? ((wins / total) * 100).toFixed(1) : "0.0";
  
  return (
    <StatsCard
      title="Win Rate"
      value={`${winRate}%`}
      subtitle={`${wins}W / ${total - wins}L`}
      icon={Award}
      gradient="amber"
    />
  );
}

export function AvgHoldTimeWidget({ closedPositions }) {
  const avgDays = closedPositions?.length > 0
    ? closedPositions.reduce((sum, p) => {
        if (p.entry_date && p.exit_date) {
          const days = Math.ceil((new Date(p.exit_date) - new Date(p.entry_date)) / (1000 * 60 * 60 * 24));
          return sum + days;
        }
        return sum;
      }, 0) / closedPositions.length
    : 0;

  return (
    <StatsCard
      title="Avg Hold Time"
      value={`${avgDays.toFixed(1)} days`}
      subtitle="Average position duration"
      icon={Clock}
      gradient="cyan"
    />
  );
}
