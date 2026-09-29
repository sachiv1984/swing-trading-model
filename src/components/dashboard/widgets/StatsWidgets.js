import StatsCard from "../../ui/StatsCard";
import { Wallet, TrendingUp, Briefcase, PieChart, Award, Clock } from "lucide-react";
import { formatCurrency, formatPercent } from "../../../lib/format";

export function PortfolioValueWidget({ portfolio, totalPositionsValue }) {
  const cashBalance = portfolio?.cash_balance || 0;
  const value = cashBalance + totalPositionsValue;
  return (
    <StatsCard
      title="Portfolio Value"
      value={formatCurrency(value)}
      subtitle={`Cash + Positions`}
      icon={Wallet}
      gradient="cyan"
    />
  );
}

export function CashBalanceWidget({ portfolio, onManageCash }) {
  return (
    <div onClick={onManageCash} className="cursor-pointer">
      <StatsCard
        title="Cash Balance"
        value={formatCurrency(portfolio?.cash_balance || 0)}
        subtitle="Click to manage"
        icon={Briefcase}
        gradient="violet"
      />
    </div>
  );
}

export function OpenPositionsWidget({ totalPositionsValue, positionsCount }) {
  return (
    <StatsCard
      title="Open Positions"
      value={formatCurrency(totalPositionsValue)}
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
      value={formatCurrency(totalPnL, { signed: true })}
      trend={totalPnL >= 0 ? "up" : "down"}
      trendValue={formatPercent((totalPnL / (totalPositionsValue || 1)) * 100, { signed: true })}
      icon={TrendingUp}
      gradient={totalPnL >= 0 ? "emerald" : "rose"}
    />
  );
}

export function WinRateWidget({ closedPositions }) {
  const wins = closedPositions?.filter(p => (p.pnl || 0) > 0).length || 0;
  const total = closedPositions?.length || 0;
  const winRate = total > 0 ? (wins / total) * 100 : 0;

  return (
    <StatsCard
      title="Win Rate"
      value={formatPercent(winRate)}
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
