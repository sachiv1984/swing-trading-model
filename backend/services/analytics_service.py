"""
Analytics Service - Single Source of Truth for All Metrics
Works with Base44 entities (not SQLAlchemy models)

BLG-TECH-01 fixes applied 2026-02-20:
  AP-06: _calculate_sharpe() — population variance (÷n) replaced with
         sample variance (÷n−1) for both portfolio and trade methods
  AP-07: _calculate_advanced_metrics() — capital efficiency cost basis
         changed from entry_price × shares to trade.total_cost (GBP)
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
        pass

    def get_metrics(self, period: str = "all_time", min_trades: int = 10) -> Dict[str, Any]:
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
        filtered_trades = self._filter_trades_by_period(trades, period)
        filtered_history = self._filter_history_by_period(portfolio_history, period)

        if len(filtered_trades) < min_trades:
            return self._insufficient_data_response(len(filtered_trades), min_trades)

        executive = self._calculate_executive_metrics(filtered_trades, filtered_history)
        advanced = self._calculate_advanced_metrics(filtered_trades, filtered_history)
        market_comp = self._calculate_market_comparison(filtered_trades)
        exit_reasons = self._calculate_exit_reasons(filtered_trades)
        monthly = self._calculate_monthly_data(filtered_trades)
        day_of_week = self._calculate_day_of_week(filtered_trades)
        holding_periods = self._calculate_holding_periods(filtered_trades)
        top_performers = self._calculate_top_performers(filtered_trades)
        consistency = self._calculate_consistency_metrics(filtered_trades)

        winners = [t for t in filtered_trades if t.get('pnl', 0) > 0]
        total_pnl = sum(t.get('pnl', 0) for t in filtered_trades)
        win_rate = (len(winners) / len(filtered_trades)) * 100

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
        }

    def _filter_trades_by_period(self, trades: List[Dict], period: str) -> List[Dict]:
        if period == "all_time":
            return trades
        cutoff = self._get_period_cutoff(period)
        return [
            t for t in trades
            if datetime.fromisoformat(t.get('exit_date', '').replace('Z', '+00:00')) >= cutoff
        ]

    def _filter_history_by_period(self, history: List[Dict], period: str) -> List[Dict]:
        if period == "all_time":
            return history
        cutoff = self._get_period_cutoff(period)
        return [
            h for h in history
            if datetime.fromisoformat(h.get('snapshot_date', '').replace('Z', '+00:00')) >= cutoff
        ]

    def _get_period_cutoff(self, period: str) -> datetime:
        now = datetime.utcnow()
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

    def _insufficient_data_response(self, actual: int, minimum: int) -> Dict:
        return {
            "summary": {
                "total_trades": actual,
                "win_rate": 0.0,
                "total_pnl": 0.0,
                "has_enough_data": False,
                "min_required": minimum,
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

    def _calculate_executive_metrics(self, trades: List[Dict], portfolio_history: List[Dict]) -> Dict:
        if not trades:
            return {}

        winners = [t for t in trades if t.get('pnl', 0) > 0]
        losers = [t for t in trades if t.get('pnl', 0) < 0]

        win_rate = (len(winners) / len(trades)) * 100
        avg_win = sum(t['pnl'] for t in winners) / len(winners) if winners else 0
        avg_loss = sum(t['pnl'] for t in losers) / len(losers) if losers else 0
        gross_profit = sum(t['pnl'] for t in winners)
        gross_loss = abs(sum(t['pnl'] for t in losers))

        sharpe_ratio, sharpe_method = self._calculate_sharpe(trades, portfolio_history)
        max_dd = self._calculate_max_drawdown(portfolio_history)
        recovery_factor = self._calculate_recovery_factor(portfolio_history)

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
        """
        Calculate Sharpe ratio using canonical method selection and sample variance.

        BLG-TECH-01 AP-06: Both portfolio and trade variance calculations updated
        from population variance (÷ n) to sample variance (÷ n−1).
        """

        # Portfolio-based method (preferred — requires 30+ snapshots)
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
                # BLG-TECH-01 FIX: sample variance (n−1) replaces population variance (n)
                variance = sum((r - avg_return) ** 2 for r in daily_returns) / (len(daily_returns) - 1)
                std_dev = math.sqrt(variance)

                if std_dev > 0:
                    sharpe = (avg_return / std_dev) * math.sqrt(252)
                    return sharpe, "portfolio"

        # Trade-based fallback (requires 10+ trades)
        if len(trades) >= 10:
            annualised_returns = []

            for trade in trades:
                entry_date = datetime.fromisoformat(trade.get('entry_date', '').replace('Z', '+00:00'))
                exit_date = datetime.fromisoformat(trade.get('exit_date', '').replace('Z', '+00:00'))
                hold_days = max(1, (exit_date - entry_date).days)

                pnl_percent = trade.get('pnl_percent', 0)
                if pnl_percent is not None:
                    annualised = (pnl_percent / hold_days) * 252
                    annualised_returns.append(annualised)

            if len(annualised_returns) >= 2:
                avg = sum(annualised_returns) / len(annualised_returns)
                # BLG-TECH-01 FIX: sample variance (n−1) replaces population variance (n)
                variance = sum((r - avg) ** 2 for r in annualised_returns) / (len(annualised_returns) - 1)
                std_dev = math.sqrt(variance)

                if std_dev > 0:
                    return avg / std_dev, "trade"

        return 0.0, "insufficient_data"

    def _calculate_max_drawdown(self, portfolio_history: List[Dict]) -> Dict:
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

    def _calculate_advanced_metrics(self, trades: List[Dict], history: List[Dict]) -> Dict:
        """
        BLG-TECH-01 AP-07: Capital efficiency cost basis corrected.
        Replaced entry_price × shares (currency-mixed) with
        Mean(trade.total_cost) which is always GBP.
        """
        if not trades:
            return {
                "win_streak": 0, "loss_streak": 0,
                "avg_hold_winners": 0.0, "avg_hold_losers": 0.0,
                "trade_frequency": 0.0, "capital_efficiency": 0.0,
                "days_underwater": 0, "peak_date": None, "portfolio_peak_equity": 0.0
            }

        sorted_trades = sorted(trades, key=lambda t: t.get('exit_date', ''))

        win_streak, loss_streak = self._calculate_streaks(sorted_trades)

        winners = [t for t in trades if t.get('pnl', 0) > 0]
        losers = [t for t in trades if t.get('pnl', 0) < 0]

        avg_hold_winners = (
            sum(t.get('holding_days', 0) for t in winners) / len(winners)
            if winners else 0
        )
        avg_hold_losers = (
            sum(t.get('holding_days', 0) for t in losers) / len(losers)
            if losers else 0
        )

        if len(sorted_trades) >= 2:
            first_date = datetime.fromisoformat(
                sorted_trades[0].get('entry_date', '').replace('Z', '+00:00')
            )
            last_date = datetime.fromisoformat(
                sorted_trades[-1].get('exit_date', '').replace('Z', '+00:00')
            )
            day_span = (last_date - first_date).days
            trade_frequency = (len(trades) / day_span) * 7 if day_span > 0 else 0
        else:
            trade_frequency = 0

        # BLG-TECH-01 AP-07 FIX:
        # Previous (non-conformant): avg_position = mean(entry_price × shares) — mixes USD/GBP
        # Corrected (canonical):     avg_position = mean(total_cost) — always GBP
        total_cost_values = [t.get('total_cost', 0) for t in trades]
        avg_position_gbp = sum(total_cost_values) / len(total_cost_values) if total_cost_values else 0
        total_pnl = sum(t.get('pnl', 0) for t in trades)
        capital_eff = (total_pnl / avg_position_gbp) * 100 if avg_position_gbp > 0 else 0

        days_underwater, peak_date = self._calculate_underwater(sorted_trades)

        portfolio_peak = (
            max(float(s.get('total_value', 0)) for s in history)
            if history else 0.0
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

    def _calculate_streaks(self, sorted_trades: List[Dict]):
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

    def _calculate_underwater(self, sorted_trades: List[Dict]):
        running_equity = 0
        peak_equity = 0
        peak_date = None
        max_days_underwater = 0

        for trade in sorted_trades:
            running_equity += trade.get('pnl', 0)
            if running_equity >= peak_equity:
                peak_equity = running_equity
                peak_date = trade.get('exit_date')
            elif peak_date is not None:
                exit_dt = datetime.fromisoformat(
                    trade.get('exit_date', '').replace('Z', '+00:00')
                )
                peak_dt = datetime.fromisoformat(peak_date.replace('Z', '+00:00'))
                days_uw = (exit_dt - peak_dt).days
                max_days_underwater = max(max_days_underwater, days_uw)

        return max_days_underwater, peak_date

    def _calculate_market_comparison(self, trades: List[Dict]) -> Dict:
        result = {}
        for market in ["US", "UK"]:
            market_trades = [t for t in trades if t.get('market') == market]
            if not market_trades:
                result[market] = {
                    "total_trades": 0, "win_rate": 0.0, "total_pnl": 0.0,
                    "avg_win": 0.0, "avg_loss": 0.0,
                    "best_performer": None, "worst_performer": None
                }
                continue

            winners = [t for t in market_trades if t.get('pnl', 0) > 0]
            losers = [t for t in market_trades if t.get('pnl', 0) < 0]

            result[market] = {
                "total_trades": len(market_trades),
                "win_rate": round(len(winners) / len(market_trades) * 100, 2),
                "total_pnl": round(sum(t.get('pnl', 0) for t in market_trades), 2),
                "avg_win": round(sum(t['pnl'] for t in winners) / len(winners), 2) if winners else 0.0,
                "avg_loss": round(sum(t['pnl'] for t in losers) / len(losers), 2) if losers else 0.0,
                "best_performer": max(market_trades, key=lambda t: t.get('pnl', 0), default=None) and
                    {"ticker": max(market_trades, key=lambda t: t.get('pnl', 0))['ticker'],
                     "pnl": max(market_trades, key=lambda t: t.get('pnl', 0))['pnl']},
                "worst_performer": min(market_trades, key=lambda t: t.get('pnl', 0), default=None) and
                    {"ticker": min(market_trades, key=lambda t: t.get('pnl', 0))['ticker'],
                     "pnl": min(market_trades, key=lambda t: t.get('pnl', 0))['pnl']},
            }
        return result

    def _calculate_exit_reasons(self, trades: List[Dict]) -> List[Dict]:
        from collections import defaultdict
        reason_groups = defaultdict(list)
        for trade in trades:
            reason = trade.get('exit_reason') or 'Manual Exit'
            reason_groups[reason].append(trade)

        result = []
        for reason, group in reason_groups.items():
            winners = [t for t in group if t.get('pnl', 0) > 0]
            result.append({
                "reason": reason,
                "count": len(group),
                "win_rate": round(len(winners) / len(group) * 100, 2),
                "total_pnl": round(sum(t.get('pnl', 0) for t in group), 2),
                "avg_pnl": round(sum(t.get('pnl', 0) for t in group) / len(group), 2),
                "percentage": round(len(group) / len(trades) * 100, 2)
            })
        return result

    def _calculate_monthly_data(self, trades: List[Dict]) -> List[Dict]:
        from collections import defaultdict
        monthly = defaultdict(list)
        for trade in trades:
            exit_date = trade.get('exit_date', '')[:7]  # YYYY-MM
            monthly[exit_date].append(trade)

        result = []
        for month in sorted(monthly.keys())[-12:]:
            group = monthly[month]
            winners = [t for t in group if t.get('pnl', 0) > 0]
            result.append({
                "month": month,
                "trade_count": len(group),
                "pnl": round(sum(t.get('pnl', 0) for t in group), 2),
                "win_rate": round(len(winners) / len(group) * 100, 2) if group else 0.0,
            })
        return result

    def _calculate_day_of_week(self, trades: List[Dict]) -> List[Dict]:
        from collections import defaultdict
        days = defaultdict(list)
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for trade in trades:
            try:
                exit_dt = datetime.fromisoformat(trade.get('exit_date', '').replace('Z', '+00:00'))
                days[exit_dt.weekday()].append(trade)
            except (ValueError, AttributeError):
                pass
        return [
            {
                "day": day_names[i],
                "trade_count": len(days[i]),
                "avg_pnl": round(sum(t.get('pnl', 0) for t in days[i]) / len(days[i]), 2) if days[i] else 0.0
            }
            for i in range(7)
        ]

    def _calculate_holding_periods(self, trades: List[Dict]) -> List[Dict]:
        buckets = [
            ("1-5 days", 1, 5),
            ("6-10 days", 6, 10),
            ("11-20 days", 11, 20),
            ("21-30 days", 21, 30),
            ("31+ days", 31, 9999),
        ]
        result = []
        for label, low, high in buckets:
            group = [t for t in trades if low <= t.get('holding_days', 0) <= high]
            winners = [t for t in group if t.get('pnl', 0) > 0]
            result.append({
                "period": label,
                "trades": len(group),
                "avg_pnl": round(sum(t.get('pnl', 0) for t in group) / len(group), 2) if group else 0.0,
                "win_rate": round(len(winners) / len(group) * 100, 2) if group else 0.0,
            })
        return result

    def _calculate_top_performers(self, trades: List[Dict]) -> Dict:
        sorted_by_pnl = sorted(trades, key=lambda t: t.get('pnl', 0), reverse=True)
        return {
            "winners": [
                {"ticker": t.get('ticker'), "pnl": t.get('pnl'), "pnl_percent": t.get('pnl_percent')}
                for t in sorted_by_pnl[:5] if t.get('pnl', 0) > 0
            ],
            "losers": [
                {"ticker": t.get('ticker'), "pnl": t.get('pnl'), "pnl_percent": t.get('pnl_percent')}
                for t in sorted_by_pnl[-5:] if t.get('pnl', 0) < 0
            ]
        }

    def _calculate_consistency_metrics(self, trades: List[Dict]) -> Dict:
        monthly = self._calculate_monthly_data(trades)
        if not monthly:
            return {
                "consecutive_profitable_months": 0, "current_streak": 0,
                "win_rate_std_dev": 0.0, "pnl_std_dev": 0.0
            }

        max_streak = cur_streak = current_streak = 0
        for m in monthly:
            if m['pnl'] > 0:
                cur_streak += 1
                max_streak = max(max_streak, cur_streak)
            else:
                cur_streak = 0

        for m in reversed(monthly):
            if m['pnl'] > 0:
                current_streak += 1
            else:
                break

        pnls = [m['pnl'] for m in monthly]
        win_rates = [m['win_rate'] for m in monthly]
        pnl_mean = sum(pnls) / len(pnls)
        wr_mean = sum(win_rates) / len(win_rates)
        pnl_std = math.sqrt(sum((p - pnl_mean) ** 2 for p in pnls) / len(pnls))
        wr_std = math.sqrt(sum((w - wr_mean) ** 2 for w in win_rates) / len(win_rates))

        return {
            "consecutive_profitable_months": max_streak,
            "current_streak": current_streak,
            "win_rate_std_dev": round(wr_std, 2),
            "pnl_std_dev": round(pnl_std, 2)
        }
