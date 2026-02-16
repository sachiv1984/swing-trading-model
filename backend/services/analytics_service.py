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
    Works with Base44 entity system instead of direct SQLAlchemy queries.
    """

    def __init__(self, db):
        """
        Args:
            db: Database session (not used with Base44, kept for compatibility)
        """
        self.db = db

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
                "message": "Analytics service needs to be called with pre-fetched data"
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

    def calculate_metrics_from_data(
        self, 
        trades: List[Dict], 
        portfolio_history: List[Dict],
        period: str = "all_time",
        min_trades: int = 10
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
        winners = [t for t in filtered_trades if t.get('pnl', 0) > 0]
        win_rate = (len(winners) / len(filtered_trades)) * 100 if filtered_trades else 0
        total_pnl = sum(t.get('pnl', 0) for t in filtered_trades)
        
        return {
            "summary": {
                "total_trades": len(filtered_trades),
                "win_rate": round(win_rate, 2),
                "total_pnl": round(total_pnl, 2),
                "has_enough_data": True,
                "min_required": min_trades
            },
            "executive_metrics": executive,
            "advanced_metrics": advanced,
            "market_comparison": market_comp,
            "exit_reasons": exit_reasons,
            "monthly_data": monthly,
            "day_of_week": day_of_week,
            "holding_periods": holding_periods,
            "top_performers": top_performers,
            "consistency_metrics": consistency
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

    # Add remaining calculation methods (_calculate_advanced_metrics, etc.)
    # Simplified for space - full implementation in complete file
    
    def _calculate_advanced_metrics(self, trades, history):
        return {"win_streak": 0, "loss_streak": 0}
    
    def _calculate_market_comparison(self, trades):
        return {"US": {}, "UK": {}}
    
    def _calculate_exit_reasons(self, trades):
        return []
    
    def _calculate_monthly_data(self, trades):
        return []
    
    def _calculate_day_of_week(self, trades):
        return []
    
    def _calculate_holding_periods(self, trades):
        return []
    
    def _calculate_top_performers(self, trades):
        return {"winners": [], "losers": []}
    
    def _calculate_consistency_metrics(self, monthly_data):
        return {}
