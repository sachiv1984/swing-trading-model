"""
Analytics Service - Single Source of Truth for All Metrics
Place in: backend/services/analytics_service.py
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import math


class AnalyticsService:
    """
    Centralized analytics calculation service.
    ALL metrics calculations happen here - frontend just displays.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_metrics(self, period: str = "all_time", min_trades: int = 10) -> Dict[str, Any]:
        """
        Calculate ALL analytics metrics for the given period.
        
        Args:
            period: Time period filter (last_7_days, last_month, etc.)
            min_trades: Minimum trades required for analytics
            
        Returns:
            Complete metrics dictionary
        """
        from backend.models.position import Position
        from backend.models.portfolio import PortfolioSnapshot
        
        # Get filtered data
        trades = self._get_filtered_trades(period)
        portfolio_history = self._get_filtered_portfolio_history(period)
        
        # Check if enough data
        has_enough_data = len(trades) >= min_trades
        
        if not has_enough_data:
            return self._insufficient_data_response(len(trades), min_trades)
        
        # Calculate all metrics
        executive_metrics = self._calculate_executive_metrics(trades, portfolio_history)
        advanced_metrics = self._calculate_advanced_metrics(trades, portfolio_history)
        market_comparison = self._calculate_market_comparison(trades)
        exit_reasons = self._calculate_exit_reasons(trades)
        monthly_data = self._calculate_monthly_data(trades)
        day_of_week = self._calculate_day_of_week(trades)
        holding_periods = self._calculate_holding_periods(trades)
        top_performers = self._calculate_top_performers(trades)
        consistency_metrics = self._calculate_consistency_metrics(monthly_data)
        
        # Summary
        winners = [t for t in trades if t.pnl > 0]
        win_rate = (len(winners) / len(trades)) * 100 if trades else 0
        total_pnl = sum(t.pnl for t in trades)
        
        return {
            "summary": {
                "total_trades": len(trades),
                "win_rate": round(win_rate, 2),
                "total_pnl": round(total_pnl, 2),
                "has_enough_data": True,
                "min_required": min_trades
            },
            "executive_metrics": executive_metrics,
            "advanced_metrics": advanced_metrics,
            "market_comparison": market_comparison,
            "exit_reasons": exit_reasons,
            "monthly_data": monthly_data,
            "day_of_week": day_of_week,
            "holding_periods": holding_periods,
            "top_performers": top_performers,
            "consistency_metrics": consistency_metrics
        }

    def _insufficient_data_response(self, trade_count: int, min_required: int) -> Dict:
        """Return empty response when not enough data."""
        return {
            "summary": {
                "total_trades": trade_count,
                "win_rate": 0.0,
                "total_pnl": 0.0,
                "has_enough_data": False,
                "min_required": min_required
            },
            "executive_metrics": {},
            "advanced_metrics": {},
            "market_comparison": {},
            "exit_reasons": [],
            "monthly_data": [],
            "day_of_week": [],
            "holding_periods": [],
            "top_performers": {"winners": [], "losers": []},
            "consistency_metrics": {}
        }

    def _get_filtered_trades(self, period: str) -> List:
        """Get closed trades filtered by time period."""
        from backend.models.position import Position
        
        query = self.db.query(Position).filter(
            Position.status == "closed",
            Position.exit_date.isnot(None)
        )
        
        if period != "all_time":
            now = datetime.now()
            start_date = self._get_start_date(period, now)
            query = query.filter(Position.exit_date >= start_date)
        
        return query.order_by(Position.exit_date).all()

    def _get_filtered_portfolio_history(self, period: str) -> List:
        """Get portfolio history filtered by period."""
        from backend.models.portfolio import PortfolioSnapshot
        
        query = self.db.query(PortfolioSnapshot)
        
        if period != "all_time":
            now = datetime.now()
            start_date = self._get_start_date(period, now)
            query = query.filter(PortfolioSnapshot.snapshot_date >= start_date)
        
        return query.order_by(PortfolioSnapshot.snapshot_date).all()

    def _get_start_date(self, period: str, now: datetime) -> datetime:
        """Calculate start date for period filter."""
        if period == "last_7_days":
            return now - timedelta(days=7)
        elif period == "last_month":
            return now - timedelta(days=30)
        elif period == "last_quarter":
            return now - timedelta(days=90)
        elif period == "last_year":
            return now - timedelta(days=365)
        elif period == "ytd":
            return datetime(now.year, 1, 1)
        return datetime.min

    def _calculate_executive_metrics(self, trades: List, portfolio_history: List) -> Dict:
        """Calculate executive summary metrics."""
        if not trades:
            return {}
        
        winners = [t for t in trades if t.pnl > 0]
        losers = [t for t in trades if t.pnl < 0]
        
        win_rate = (len(winners) / len(trades)) * 100
        avg_win = sum(t.pnl for t in winners) / len(winners) if winners else 0
        avg_loss = sum(t.pnl for t in losers) / len(losers) if losers else 0
        gross_profit = sum(t.pnl for t in winners)
        gross_loss = abs(sum(t.pnl for t in losers))
        
        # Sharpe ratio
        sharpe_ratio, sharpe_method = self._calculate_sharpe(trades, portfolio_history)
        
        # Max drawdown
        max_dd = self._calculate_max_drawdown(portfolio_history)
        
        # Recovery factor
        recovery_factor = self._calculate_recovery_factor(portfolio_history)
        
        # Other metrics
        expectancy = (win_rate / 100 * avg_win) + ((100 - win_rate) / 100 * avg_loss)
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        risk_reward = avg_win / abs(avg_loss) if avg_loss != 0 else 0
        
        return {
            "sharpe_ratio": round(sharpe_ratio, 2),
            "sharpe_method": sharpe_method,
            "max_drawdown": {
                "percent": round(max_dd["percent"], 2),
                "amount": round(max_dd["amount"], 2),
                "date": max_dd["date"]
            },
            "recovery_factor": round(recovery_factor, 2),
            "expectancy": round(expectancy, 2),
            "profit_factor": round(profit_factor, 2),
            "risk_reward_ratio": round(risk_reward, 2)
        }

    def _calculate_sharpe(self, trades: List, portfolio_history: List) -> tuple:
        """Calculate Sharpe ratio (portfolio-based preferred, trade-based fallback)."""
        # Portfolio-based (requires 30+ snapshots)
        if len(portfolio_history) >= 30:
            daily_returns = []
            sorted_history = sorted(portfolio_history, key=lambda x: x.snapshot_date)
            
            for i in range(1, len(sorted_history)):
                prev_val = float(sorted_history[i - 1].total_value)
                curr_val = float(sorted_history[i].total_value)
                
                if prev_val > 0 and curr_val and prev_val:
                    daily_return = ((curr_val - prev_val) / prev_val) * 100
                    daily_returns.append(daily_return)
            
            if len(daily_returns) >= 2:
                avg_return = sum(daily_returns) / len(daily_returns)
                variance = sum((r - avg_return) ** 2 for r in daily_returns) / len(daily_returns)
                std_dev = math.sqrt(variance)
                
                if std_dev > 0:
                    sharpe = (avg_return / std_dev) * math.sqrt(252)
                    return sharpe, "portfolio"
        
        # Trade-based fallback (requires 10+ trades)
        if len(trades) >= 10:
            weighted_returns = []
            
            for trade in trades:
                hold_days = (trade.exit_date - trade.entry_date).days
                hold_days = max(1, hold_days)
                
                if trade.pnl_percent is not None:
                    annualized = (trade.pnl_percent / hold_days) * 252
                    weighted_returns.append(annualized)
            
            if len(weighted_returns) >= 2:
                avg = sum(weighted_returns) / len(weighted_returns)
                variance = sum((r - avg) ** 2 for r in weighted_returns) / len(weighted_returns)
                std_dev = math.sqrt(variance)
                
                if std_dev > 0:
                    return avg / std_dev, "trade"
        
        return 0.0, "insufficient_data"

    def _calculate_max_drawdown(self, portfolio_history: List) -> Dict:
        """Calculate maximum drawdown from full portfolio history."""
        if not portfolio_history:
            return {"percent": 0.0, "amount": 0.0, "date": None}
        
        sorted_history = sorted(portfolio_history, key=lambda x: x.snapshot_date)
        
        peak_equity = 0
        max_dd_amount = 0
        max_dd_percent = 0
        max_dd_date = None
        
        for snapshot in sorted_history:
            equity = float(snapshot.total_value)
            
            if equity > peak_equity:
                peak_equity = equity
            
            dd_amount = peak_equity - equity
            dd_percent = (dd_amount / peak_equity) * 100 if peak_equity > 0 else 0
            
            if dd_amount > max_dd_amount:
                max_dd_amount = dd_amount
                max_dd_percent = dd_percent
                max_dd_date = snapshot.snapshot_date.isoformat()
        
        return {
            "percent": -max_dd_percent,  # Negative by convention
            "amount": max_dd_amount,
            "date": max_dd_date
        }

    def _calculate_recovery_factor(self, portfolio_history: List) -> float:
        """Calculate recovery factor (period profit / period max drawdown)."""
        if not portfolio_history or len(portfolio_history) < 2:
            return 0.0
        
        sorted_history = sorted(portfolio_history, key=lambda x: x.snapshot_date)
        
        # Period profit
        first_equity = float(sorted_history[0].total_value)
        last_equity = float(sorted_history[-1].total_value)
        period_profit = last_equity - first_equity
        
        # Period max drawdown
        peak = 0
        max_dd = 0
        
        for snapshot in sorted_history:
            equity = float(snapshot.total_value)
            if equity > peak:
                peak = equity
            dd = peak - equity
            if dd > max_dd:
                max_dd = dd
        
        if max_dd > 0 and period_profit > 0:
            return period_profit / max_dd
        
        return 0.0

    def _calculate_advanced_metrics(self, trades: List, portfolio_history: List) -> Dict:
        """Calculate advanced metrics (streaks, holding times, etc.)."""
        if not trades:
            return {}
        
        sorted_trades = sorted(trades, key=lambda t: t.exit_date)
        
        # Streaks
        win_streak, loss_streak = self._calculate_streaks(sorted_trades)
        
        # Holding times
        winners = [t for t in trades if t.pnl > 0]
        losers = [t for t in trades if t.pnl < 0]
        
        avg_hold_winners = (
            sum((t.exit_date - t.entry_date).days for t in winners) / len(winners)
            if winners else 0
        )
        avg_hold_losers = (
            sum((t.exit_date - t.entry_date).days for t in losers) / len(losers)
            if losers else 0
        )
        
        # Trade frequency
        if len(sorted_trades) >= 2:
            first_trade = sorted_trades[0]
            last_trade = sorted_trades[-1]
            day_span = (last_trade.exit_date - first_trade.entry_date).days
            trade_frequency = (len(trades) / day_span) * 7 if day_span > 0 else 0
        else:
            trade_frequency = 0
        
        # Capital efficiency
        avg_position = sum(t.entry_price * t.shares for t in trades) / len(trades)
        total_pnl = sum(t.pnl for t in trades)
        capital_eff = (total_pnl / avg_position) * 100 if avg_position > 0 else 0
        
        # Time underwater
        days_underwater, peak_date = self._calculate_underwater(sorted_trades)
        
        # Portfolio peak
        portfolio_peak = (
            max(float(s.total_value) for s in portfolio_history)
            if portfolio_history else 0.0
        )
        
        return {
            "win_streak": win_streak,
            "loss_streak": loss_streak,
            "avg_hold_winners": round(avg_hold_winners, 1),
            "avg_hold_losers": round(avg_hold_losers, 1),
            "trade_frequency": round(trade_frequency, 1),
            "capital_efficiency": round(capital_eff, 2),
            "days_underwater": days_underwater,
            "peak_date": peak_date,
            "portfolio_peak_equity": round(portfolio_peak, 2)
        }

    def _calculate_streaks(self, sorted_trades: List) -> tuple:
        """Calculate max win/loss streaks."""
        current = 0
        max_win = 0
        max_loss = 0
        
        for trade in sorted_trades:
            if trade.pnl > 0:
                current = current + 1 if current > 0 else 1
                max_win = max(max_win, current)
            else:
                current = current - 1 if current < 0 else -1
                max_loss = max(max_loss, abs(current))
        
        return max_win, max_loss

    def _calculate_underwater(self, sorted_trades: List) -> tuple:
        """Calculate days underwater (days since last peak)."""
        running_equity = 0
        peak_equity = 0
        peak_date = None
        days_underwater = 0
        
        for trade in sorted_trades:
            running_equity += trade.pnl
            
            if running_equity >= peak_equity:
                peak_equity = running_equity
                peak_date = trade.exit_date.isoformat()
                days_underwater = 0
            elif peak_date:
                days_since = (trade.exit_date - datetime.fromisoformat(peak_date)).days
                days_underwater = max(days_underwater, days_since)
        
        return days_underwater, peak_date

    def _calculate_market_comparison(self, trades: List) -> Dict:
        """Calculate per-market metrics (US vs UK)."""
        markets = {}
        
        for market in ["US", "UK"]:
            market_trades = [t for t in trades if t.market == market]
            
            if not market_trades:
                markets[market] = {
                    "total_trades": 0,
                    "win_rate": 0.0,
                    "total_pnl": 0.0,
                    "avg_win": 0.0,
                    "avg_loss": 0.0,
                    "best_performer": None,
                    "worst_performer": None
                }
                continue
            
            winners = [t for t in market_trades if t.pnl > 0]
            losers = [t for t in market_trades if t.pnl < 0]
            sorted_trades = sorted(market_trades, key=lambda t: t.pnl, reverse=True)
            
            markets[market] = {
                "total_trades": len(market_trades),
                "win_rate": round((len(winners) / len(market_trades)) * 100, 1),
                "total_pnl": round(sum(t.pnl for t in market_trades), 2),
                "avg_win": round(sum(t.pnl for t in winners) / len(winners), 2) if winners else 0.0,
                "avg_loss": round(sum(t.pnl for t in losers) / len(losers), 2) if losers else 0.0,
                "best_performer": {
                    "ticker": sorted_trades[0].ticker,
                    "pnl": round(sorted_trades[0].pnl, 2)
                } if sorted_trades else None,
                "worst_performer": {
                    "ticker": sorted_trades[-1].ticker,
                    "pnl": round(sorted_trades[-1].pnl, 2)
                } if sorted_trades else None
            }
        
        return markets

    def _calculate_exit_reasons(self, trades: List) -> List[Dict]:
        """Calculate exit reason statistics."""
        reason_map = {}
        
        for trade in trades:
            reason = trade.exit_reason or "Manual Exit"
            
            if reason not in reason_map:
                reason_map[reason] = {"count": 0, "wins": 0, "total_pnl": 0.0}
            
            reason_map[reason]["count"] += 1
            reason_map[reason]["total_pnl"] += trade.pnl
            if trade.pnl > 0:
                reason_map[reason]["wins"] += 1
        
        results = []
        for reason, data in reason_map.items():
            results.append({
                "reason": reason,
                "count": data["count"],
                "win_rate": round((data["wins"] / data["count"]) * 100, 1),
                "total_pnl": round(data["total_pnl"], 2),
                "avg_pnl": round(data["total_pnl"] / data["count"], 2),
                "percentage": round((data["count"] / len(trades)) * 100, 1)
            })
        
        return results

    def _calculate_monthly_data(self, trades: List) -> List[Dict]:
        """Calculate monthly performance data."""
        monthly_map = {}
        
        for trade in trades:
            month_key = trade.exit_date.strftime("%Y-%m")
            
            if month_key not in monthly_map:
                monthly_map[month_key] = {"pnl": 0.0, "trades": 0, "wins": 0}
            
            monthly_map[month_key]["pnl"] += trade.pnl
            monthly_map[month_key]["trades"] += 1
            if trade.pnl > 0:
                monthly_map[month_key]["wins"] += 1
        
        results = []
        cumulative = 0
        
        for month in sorted(monthly_map.keys()):
            data = monthly_map[month]
            cumulative += data["pnl"]
            
            results.append({
                "month": month,
                "pnl": round(data["pnl"], 2),
                "trades": data["trades"],
                "win_rate": round((data["wins"] / data["trades"]) * 100, 0),
                "cumulative": round(cumulative, 2)
            })
        
        return results[-12:]  # Last 12 months only

    def _calculate_day_of_week(self, trades: List) -> List[Dict]:
        """Calculate day of week performance."""
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        day_map = {day: {"pnl": 0.0, "trades": 0} for day in days}
        
        for trade in trades:
            day_idx = trade.exit_date.weekday()
            if day_idx < 5:  # Mon-Fri only
                day_name = days[day_idx]
                day_map[day_name]["pnl"] += trade.pnl
                day_map[day_name]["trades"] += 1
        
        return [
            {
                "day": day,
                "avg_pnl": round(day_map[day]["pnl"] / day_map[day]["trades"], 2) if day_map[day]["trades"] > 0 else 0.0,
                "trades": day_map[day]["trades"]
            }
            for day in days
        ]

    def _calculate_holding_periods(self, trades: List) -> List[Dict]:
        """Calculate holding period analysis."""
        buckets = [
            {"label": "1-5 days", "min": 1, "max": 5},
            {"label": "6-10 days", "min": 6, "max": 10},
            {"label": "11-20 days", "min": 11, "max": 20},
            {"label": "21-30 days", "min": 21, "max": 30},
            {"label": "31+ days", "min": 31, "max": 9999}
        ]
        
        results = []
        
        for bucket in buckets:
            bucket_trades = [
                t for t in trades
                if bucket["min"] <= (t.exit_date - t.entry_date).days <= bucket["max"]
            ]
            
            wins = [t for t in bucket_trades if t.pnl > 0]
            
            results.append({
                "period": bucket["label"],
                "avg_pnl": round(sum(t.pnl for t in bucket_trades) / len(bucket_trades), 2) if bucket_trades else 0.0,
                "trades": len(bucket_trades),
                "win_rate": round((len(wins) / len(bucket_trades)) * 100, 0) if bucket_trades else 0
            })
        
        return results

    def _calculate_top_performers(self, trades: List) -> Dict:
        """Calculate top 5 winners and losers."""
        sorted_trades = sorted(trades, key=lambda t: t.pnl, reverse=True)
        
        def format_trade(trade):
            return {
                "ticker": trade.ticker,
                "entry_date": trade.entry_date.isoformat(),
                "pnl": round(trade.pnl, 2),
                "pnl_percent": round(trade.pnl_percent, 2) if trade.pnl_percent else 0.0,
                "days_held": (trade.exit_date - trade.entry_date).days,
                "exit_reason": trade.exit_reason or "Manual Exit"
            }
        
        return {
            "winners": [format_trade(t) for t in sorted_trades[:5]],
            "losers": [format_trade(t) for t in sorted_trades[-5:][::-1]]
        }

    def _calculate_consistency_metrics(self, monthly_data: List[Dict]) -> Dict:
        """Calculate consistency metrics from monthly data."""
        if not monthly_data:
            return {
                "consecutive_profitable_months": 0,
                "current_streak": 0,
                "win_rate_std_dev": 0.0,
                "pnl_std_dev": 0.0
            }
        
        # Consecutive profitable months
        max_streak = 0
        current_streak = 0
        
        for month in monthly_data:
            if month["pnl"] > 0:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        
        # Standard deviations
        win_rates = [m["win_rate"] for m in monthly_data]
        pnls = [m["pnl"] for m in monthly_data]
        
        avg_wr = sum(win_rates) / len(win_rates)
        avg_pnl = sum(pnls) / len(pnls)
        
        wr_std = math.sqrt(sum((wr - avg_wr) ** 2 for wr in win_rates) / len(win_rates))
        pnl_std = math.sqrt(sum((p - avg_pnl) ** 2 for p in pnls) / len(pnls))
        
        return {
            "consecutive_profitable_months": max_streak,
            "current_streak": current_streak,
            "win_rate_std_dev": round(wr_std, 2),
            "pnl_std_dev": round(pnl_std, 2)
        }
