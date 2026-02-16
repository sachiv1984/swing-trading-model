"""
Analytics Service - Single Source of Truth for All Metrics
Works with Base44 entities (not SQLAlchemy models)
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import math


class AnalyticsService:
    """
    Centralized analytics calculation service.
    Works with pre-fetched data (no database queries).
    """

    def __init__(self):
        """
        No database session needed - works with provided data.
        """
        pass

    def get_metrics(self, period: str = "all_time", min_trades: int = 10) -> Dict[str, Any]:
        """
        Calculate ALL analytics metrics for the given period.

        NOTE: This version is designed to work with data fetched via API endpoints.
        The analytics service should be called from the router AFTER fetching
        the necessary data (trades and portfolio history).

        For now, returns a structure indicating implementation is needed.
        """

        return {
            "summary": {
                "total_trades": 0,
                "win_rate": 0.0,
                "total_pnl": 0.0,
                "has_enough_data": False,
                "min_required": min_trades,
                "message": "Analytics service needs to be called with pre-fetched data",
            },
            "executive_metrics": {},
            "advanced_metrics": {},
            "market_comparison": {},
            "exit_reasons": [],
            "monthly_data": [],
            "day_of_week": [],
            "holding_periods": [],
            "top_performers": {"winners": [], "losers": []},
            "consistency_metrics": {},
        }

    def calculate_metrics_from_data(
        self,
        trades: List[Dict],
        portfolio_history: List[Dict],
        period: str = "all_time",
        min_trades: int = 10,
    ) -> Dict[str, Any]:
        """
        Calculate metrics from pre-fetched data.

        Args:
            trades: List of trade dicts (from /trades endpoint)
            portfolio_history: List of portfolio snapshot dicts
            period: Time period filter
            min_trades: Minimum trades required

        Returns:
            Complete metrics dictionary
        """
        # Filter by period
        filtered_trades = self._filter_trades_by_period(trades, period)
        filtered_history = self._filter_history_by_period(portfolio_history, period)

        # Check minimum
        if len(filtered_trades) < min_trades:
            return self._insufficient_data_response(len(filtered_trades), min_trades)

        # Calculate all metrics
        executive = self._calculate_executive_metrics(filtered_trades, filtered_history)
        advanced = self._calculate_advanced_metrics(filtered_trades, filtered_history)
        market_comp = self._calculate_market_comparison(filtered_trades)
        exit_reasons = self._calculate_exit_reasons(filtered_trades)
        monthly = self._calculate_monthly_data(filtered_trades)
        day_of_week = self._calculate_day_of_week(filtered_trades)
        holding_periods = self._calculate_holding_periods(filtered_trades)
        top_performers = self._calculate_top_performers(filtered_trades)
        consistency = self._calculate_consistency_metrics(monthly)

        # Summary
        winners = [t for t in filtered_trades if t.get("pnl", 0) > 0]
        win_rate = (len(winners) / len(filtered_trades)) * 100 if filtered_trades else 0
        total_pnl = sum(t.get("pnl", 0) for t in filtered_trades)

        # Add trades for charts (before the return statement)
        trades_for_charts = [
            {
                "id": t.get("id"),
                "ticker": t.get("ticker"),
                "market": t.get("market"),
                "entry_date": t.get("entry_date"),
                "exit_date": t.get("exit_date"),
                "pnl": t.get("pnl", 0),
                "pnl_percent": t.get("pnl_percent", 0),
                "exit_reason": t.get("exit_reason"),
                "holding_days": t.get("holding_days", 0),
                "tags": t.get("tags"),
            }
            for t in filtered_trades
        ]

        return {
            "summary": {
                "total_trades": len(filtered_trades),
                "win_rate": round(win_rate, 2),
                "total_pnl": round(total_pnl, 2),
                "has_enough_data": True,
                "min_required": min_trades,
            },
            "executive_metrics": executive,
            "advanced_metrics": advanced,
            "market_comparison": market_comp,
            "exit_reasons": exit_reasons,
            "monthly_data": monthly,
            "day_of_week": day_of_week,
            "holding_periods": holding_periods,
            "top_performers": top_performers,
            "consistency_metrics": consistency,
            "trades_for_charts": trades_for_charts,
        }

    def _insufficient_data_response(self, trade_count: int, min_required: int) -> Dict[str, Any]:
        """Return empty response when not enough data."""
        return {
            "summary": {
                "total_trades": trade_count,
                "win_rate": 0.0,
                "total_pnl": 0.0,
                "has_enough_data": False,
                "min_required": min_required,
            },
            "executive_metrics": {},
            "advanced_metrics": {},
            "market_comparison": {},
            "exit_reasons": [],
            "monthly_data": [],
            "day_of_week": [],
            "holding_periods": [],
            "top_performers": {"winners": [], "losers": []},
            "consistency_metrics": {},
            "trades_for_charts": [],
        }
    def _filter_trades_by_period(self, trades: List[Dict], period: str) -> List[Dict]:
        """Filter trades by time period."""
        if period == "all_time":
            return trades
        
        now = datetime.now()
        start_date = self._get_start_date(period, now)
        
        return [
            t for t in trades 
            if t.get('exit_date') and datetime.fromisoformat(t['exit_date'].replace('Z', '+00:00')) >= start_date
        ]

    def _filter_history_by_period(self, history: List[Dict], period: str) -> List[Dict]:
        """Filter portfolio history by period."""
        if period == "all_time":
            return history
        
        now = datetime.now()
        start_date = self._get_start_date(period, now)
        
        return [
            h for h in history
            if h.get('snapshot_date') and datetime.fromisoformat(h['snapshot_date'].replace('Z', '+00:00')) >= start_date
        ]

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

    def _calculate_executive_metrics(self, trades: List[Dict], portfolio_history: List[Dict]) -> Dict:
        """Calculate executive summary metrics."""
        if not trades:
            return {}
        
        winners = [t for t in trades if t.get('pnl', 0) > 0]
        losers = [t for t in trades if t.get('pnl', 0) < 0]
        
        win_rate = (len(winners) / len(trades)) * 100
        avg_win = sum(t['pnl'] for t in winners) / len(winners) if winners else 0
        avg_loss = sum(t['pnl'] for t in losers) / len(losers) if losers else 0
        gross_profit = sum(t['pnl'] for t in winners)
        gross_loss = abs(sum(t['pnl'] for t in losers))
        
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

    def _calculate_sharpe(self, trades: List[Dict], portfolio_history: List[Dict]) -> tuple:
        """Calculate Sharpe ratio."""
        # Portfolio-based (requires 30+ snapshots)
        if len(portfolio_history) >= 30:
            daily_returns = []
            sorted_history = sorted(portfolio_history, key=lambda x: x.get('snapshot_date', ''))
            
            for i in range(1, len(sorted_history)):
                prev_val = float(sorted_history[i - 1].get('total_value', 0))
                curr_val = float(sorted_history[i].get('total_value', 0))
                
                if prev_val > 0:
                    daily_return = ((curr_val - prev_val) / prev_val) * 100
                    daily_returns.append(daily_return)
            
            if len(daily_returns) >= 2:
                avg_return = sum(daily_returns) / len(daily_returns)
                variance = sum((r - avg_return) ** 2 for r in daily_returns) / len(daily_returns)
                std_dev = math.sqrt(variance)
                
                if std_dev > 0:
                    sharpe = (avg_return / std_dev) * math.sqrt(252)
                    return sharpe, "portfolio"
        
        # Trade-based fallback
        if len(trades) >= 10:
            weighted_returns = []
            
            for trade in trades:
                entry_date = datetime.fromisoformat(trade.get('entry_date', '').replace('Z', '+00:00'))
                exit_date = datetime.fromisoformat(trade.get('exit_date', '').replace('Z', '+00:00'))
                hold_days = max(1, (exit_date - entry_date).days)
                
                pnl_percent = trade.get('pnl_percent', 0)
                if pnl_percent is not None:
                    annualized = (pnl_percent / hold_days) * 252
                    weighted_returns.append(annualized)
            
            if len(weighted_returns) >= 2:
                avg = sum(weighted_returns) / len(weighted_returns)
                variance = sum((r - avg) ** 2 for r in weighted_returns) / len(weighted_returns)
                std_dev = math.sqrt(variance)
                
                if std_dev > 0:
                    return avg / std_dev, "trade"
        
        return 0.0, "insufficient_data"

    def _calculate_max_drawdown(self, portfolio_history: List[Dict]) -> Dict:
        """Calculate maximum drawdown."""
        if not portfolio_history:
            return {"percent": 0.0, "amount": 0.0, "date": None}
        
        sorted_history = sorted(portfolio_history, key=lambda x: x.get('snapshot_date', ''))
        
        peak_equity = 0
        max_dd_amount = 0
        max_dd_percent = 0
        max_dd_date = None
        
        for snapshot in sorted_history:
            equity = float(snapshot.get('total_value', 0))
            
            if equity > peak_equity:
                peak_equity = equity
            
            dd_amount = peak_equity - equity
            dd_percent = (dd_amount / peak_equity) * 100 if peak_equity > 0 else 0
            
            if dd_amount > max_dd_amount:
                max_dd_amount = dd_amount
                max_dd_percent = dd_percent
                max_dd_date = snapshot.get('snapshot_date')
        
        return {
            "percent": -max_dd_percent,
            "amount": max_dd_amount,
            "date": max_dd_date
        }

    def _calculate_recovery_factor(self, portfolio_history: List[Dict]) -> float:
        """Calculate recovery factor."""
        if not portfolio_history or len(portfolio_history) < 2:
            return 0.0
        
        sorted_history = sorted(portfolio_history, key=lambda x: x.get('snapshot_date', ''))
        
        first_equity = float(sorted_history[0].get('total_value', 0))
        last_equity = float(sorted_history[-1].get('total_value', 0))
        period_profit = last_equity - first_equity
        
        peak = 0
        max_dd = 0
        
        for snapshot in sorted_history:
            equity = float(snapshot.get('total_value', 0))
            if equity > peak:
                peak = equity
            dd = peak - equity
            if dd > max_dd:
                max_dd = dd
        
        if max_dd > 0 and period_profit > 0:
            return period_profit / max_dd
        
        return 0.0

    def _calculate_advanced_metrics(self, trades, history):
        """Calculate advanced metrics."""
        if not trades:
            return {"win_streak": 0, "loss_streak": 0}
        
        sorted_trades = sorted(trades, key=lambda t: t.get('exit_date', ''))
        
        # Streaks
        win_streak, loss_streak = self._calculate_streaks(sorted_trades)
        
        # Holding times
        winners = [t for t in trades if t.get('pnl', 0) > 0]
        losers = [t for t in trades if t.get('pnl', 0) < 0]
        
        avg_hold_winners = sum(t.get('holding_days', 0) for t in winners) / len(winners) if winners else 0
        avg_hold_losers = sum(t.get('holding_days', 0) for t in losers) / len(losers) if losers else 0
        
        # Trade frequency
        if len(sorted_trades) >= 2:
            first_date = datetime.fromisoformat(sorted_trades[0].get('entry_date', '').replace('Z', '+00:00'))
            last_date = datetime.fromisoformat(sorted_trades[-1].get('exit_date', '').replace('Z', '+00:00'))
            day_span = (last_date - first_date).days
            trade_frequency = (len(trades) / day_span) * 7 if day_span > 0 else 0
        else:
            trade_frequency = 0
        
        # Capital efficiency
        avg_position = sum(t.get('entry_price', 0) * t.get('shares', 0) for t in trades) / len(trades) if trades else 0
        total_pnl = sum(t.get('pnl', 0) for t in trades)
        capital_eff = (total_pnl / avg_position) * 100 if avg_position > 0 else 0
        
        # Time underwater
        days_underwater, peak_date = self._calculate_underwater(sorted_trades)
        
        # Portfolio peak
        portfolio_peak = max(float(s.get('total_value', 0)) for s in history) if history else 0.0
        
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
    
    def _calculate_streaks(self, sorted_trades):
        """Calculate win/loss streaks."""
        current = 0
        max_win = 0
        max_loss = 0
        
        for trade in sorted_trades:
            if trade.get('pnl', 0) > 0:
                current = current + 1 if current > 0 else 1
                max_win = max(max_win, current)
            else:
                current = current - 1 if current < 0 else -1
                max_loss = max(max_loss, abs(current))
        
        return max_win, max_loss
    
    def _calculate_underwater(self, sorted_trades):
        """Calculate days underwater."""
        running_equity = 0
        peak_equity = 0
        peak_date = None
        days_underwater = 0
        
        for trade in sorted_trades:
            running_equity += trade.get('pnl', 0)
            
            if running_equity >= peak_equity:
                peak_equity = running_equity
                peak_date = trade.get('exit_date')
                days_underwater = 0
            elif peak_date:
                try:
                    peak_dt = datetime.fromisoformat(peak_date.replace('Z', '+00:00'))
                    exit_dt = datetime.fromisoformat(trade.get('exit_date', '').replace('Z', '+00:00'))
                    days_since = (exit_dt - peak_dt).days
                    days_underwater = max(days_underwater, days_since)
                except:
                    pass
        
        return days_underwater, peak_date
    
    def _calculate_market_comparison(self, trades):
        """Calculate per-market metrics."""
        markets = {}
        
        for market in ["US", "UK"]:
            market_trades = [t for t in trades if t.get('market') == market]
            
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
            
            winners = [t for t in market_trades if t.get('pnl', 0) > 0]
            losers = [t for t in market_trades if t.get('pnl', 0) < 0]
            sorted_trades = sorted(market_trades, key=lambda t: t.get('pnl', 0), reverse=True)
            
            markets[market] = {
                "total_trades": len(market_trades),
                "win_rate": round((len(winners) / len(market_trades)) * 100, 1),
                "total_pnl": round(sum(t.get('pnl', 0) for t in market_trades), 2),
                "avg_win": round(sum(t.get('pnl', 0) for t in winners) / len(winners), 2) if winners else 0.0,
                "avg_loss": round(sum(t.get('pnl', 0) for t in losers) / len(losers), 2) if losers else 0.0,
                "best_performer": {
                    "ticker": sorted_trades[0].get('ticker'),
                    "pnl": round(sorted_trades[0].get('pnl', 0), 2)
                } if sorted_trades else None,
                "worst_performer": {
                    "ticker": sorted_trades[-1].get('ticker'),
                    "pnl": round(sorted_trades[-1].get('pnl', 0), 2)
                } if sorted_trades else None
            }
        
        return markets
    
    def _calculate_exit_reasons(self, trades):
        """Calculate exit reason statistics."""
        reason_map = {}
        
        for trade in trades:
            reason = trade.get('exit_reason') or "Manual Exit"
            
            if reason not in reason_map:
                reason_map[reason] = {"count": 0, "wins": 0, "total_pnl": 0.0}
            
            reason_map[reason]["count"] += 1
            reason_map[reason]["total_pnl"] += trade.get('pnl', 0)
            if trade.get('pnl', 0) > 0:
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
    
    def _calculate_monthly_data(self, trades):
        """Calculate monthly performance."""
        monthly_map = {}
        
        for trade in trades:
            exit_date = trade.get('exit_date', '')
            if not exit_date:
                continue
            
            month_key = exit_date[:7]  # YYYY-MM
            
            if month_key not in monthly_map:
                monthly_map[month_key] = {"pnl": 0.0, "trades": 0, "wins": 0}
            
            monthly_map[month_key]["pnl"] += trade.get('pnl', 0)
            monthly_map[month_key]["trades"] += 1
            if trade.get('pnl', 0) > 0:
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
        
        return results[-12:]  # Last 12 months
    
    def _calculate_day_of_week(self, trades):
        """Calculate day of week performance."""
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        day_map = {day: {"pnl": 0.0, "trades": 0} for day in days}
        
        for trade in trades:
            try:
                exit_date = datetime.fromisoformat(trade.get('exit_date', '').replace('Z', '+00:00'))
                day_idx = exit_date.weekday()
                if day_idx < 5:
                    day_name = days[day_idx]
                    day_map[day_name]["pnl"] += trade.get('pnl', 0)
                    day_map[day_name]["trades"] += 1
            except:
                pass
        
        return [
            {
                "day": day,
                "avg_pnl": round(day_map[day]["pnl"] / day_map[day]["trades"], 2) if day_map[day]["trades"] > 0 else 0.0,
                "trades": day_map[day]["trades"]
            }
            for day in days
        ]
    
    def _calculate_holding_periods(self, trades):
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
                if bucket["min"] <= t.get('holding_days', 0) <= bucket["max"]
            ]
            
            wins = [t for t in bucket_trades if t.get('pnl', 0) > 0]
            
            results.append({
                "period": bucket["label"],
                "avg_pnl": round(sum(t.get('pnl', 0) for t in bucket_trades) / len(bucket_trades), 2) if bucket_trades else 0.0,
                "trades": len(bucket_trades),
                "win_rate": round((len(wins) / len(bucket_trades)) * 100, 0) if bucket_trades else 0
            })
        
        return results
    
    def _calculate_top_performers(self, trades):
        """Calculate top winners and losers."""
        sorted_trades = sorted(trades, key=lambda t: t.get('pnl', 0), reverse=True)
        
        def format_trade(trade):
            return {
                "ticker": trade.get('ticker'),
                "entry_date": trade.get('entry_date'),
                "pnl": round(trade.get('pnl', 0), 2),
                "pnl_percent": round(trade.get('pnl_percent', 0), 2),
                "days_held": trade.get('holding_days', 0),
                "exit_reason": trade.get('exit_reason') or "Manual Exit"
            }
        
        return {
            "winners": [format_trade(t) for t in sorted_trades[:5]],
            "losers": [format_trade(t) for t in sorted_trades[-5:][::-1]]
        }
    
    def _calculate_consistency_metrics(self, monthly_data):
        """Calculate consistency metrics."""
        if not monthly_data:
            return {
                "consecutive_profitable_months": 0,
                "current_streak": 0,
                "win_rate_std_dev": 0.0,
                "pnl_std_dev": 0.0
            }
        
        # Consecutive profitable
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
