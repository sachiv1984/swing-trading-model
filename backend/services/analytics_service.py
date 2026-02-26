"""
Analytics Service

AnalyticsService calculates all portfolio metrics from trade and portfolio
history data passed in by the analytics router.

The trades_for_charts key in the returned dict is overridden by the router
with data sourced via a positions LEFT JOIN (BLG-TECH-07). The value built
here is a placeholder only.
"""

from collections import Counter, defaultdict
from datetime import date, timedelta
from typing import Dict, List, Optional


def _period_to_since_date(period: str) -> Optional[date]:
    """Convert a period string to the earliest exit_date to include."""
    today = date.today()
    period_map = {
        "all_time":     None,
        "last_7_days":  today - timedelta(days=7),
        "last_month":   today - timedelta(days=30),
        "last_quarter": today - timedelta(days=90),
        "last_year":    today - timedelta(days=365),
        "ytd":          date(today.year, 1, 1),
    }
    if period not in period_map:
        raise ValueError(
            f"Invalid period '{period}'. "
            f"Allowed: {', '.join(period_map.keys())}"
        )
    return period_map[period]


class AnalyticsService:
    """
    Calculates comprehensive portfolio analytics from trade and portfolio
    history data. Called by the analytics router via
    calculate_metrics_from_data().

    NOTE (BLG-TECH-07): The trades_for_charts key in the dict returned by
    calculate_metrics_from_data() is a placeholder. The analytics router
    replaces it with data sourced via a LEFT JOIN to positions.initial_stop.
    """

    def calculate_metrics_from_data(
        self,
        trades: List[Dict],
        portfolio_history: List[Dict],
        period: str = "all_time",
        min_trades: int = 10,
    ) -> Dict:
        filtered_trades = self._filter_trades_by_period(trades, period)
        filtered_history = self._filter_history_by_period(portfolio_history, period)

        total_trades = len(filtered_trades)
        has_enough_data = total_trades >= min_trades

        if not has_enough_data:
            return {
                "summary": {
                    "total_trades": total_trades,
                    "win_rate": 0.0,
                    "total_pnl": 0.0,
                    "has_enough_data": False,
                    "min_required": min_trades,
                },
                "executive_metrics": {},
                "advanced_metrics": {},
                "market_comparison": {},
                "exit_reasons": [],
                "monthly_data": self._build_monthly_data(filtered_trades),
                "day_of_week": [],
                "holding_periods": [],
                "top_performers": {"winners": [], "losers": []},
                "consistency_metrics": {},
                "trades_for_charts": [],  # overridden by router
            }

        wins = [t for t in filtered_trades if t.get("pnl", 0) > 0]
        losses = [t for t in filtered_trades if t.get("pnl", 0) < 0]
        total_pnl = sum(t.get("pnl", 0) for t in filtered_trades)
        win_rate = (len(wins) / total_trades * 100) if total_trades else 0.0

        return {
            "summary": {
                "total_trades": total_trades,
                "win_rate": round(win_rate, 1),
                "total_pnl": round(total_pnl, 2),
                "has_enough_data": True,
                "min_required": min_trades,
            },
            "executive_metrics": self._build_executive_metrics(
                filtered_trades, filtered_history
            ),
            "advanced_metrics": self._build_advanced_metrics(filtered_trades),
            "market_comparison": self._build_market_comparison(filtered_trades),
            "exit_reasons": self._build_exit_reasons(filtered_trades),
            "monthly_data": self._build_monthly_data(filtered_trades),
            "day_of_week": self._build_day_of_week(filtered_trades),
            "holding_periods": self._build_holding_periods(filtered_trades),
            "top_performers": self._build_top_performers(filtered_trades),
            "consistency_metrics": self._build_consistency_metrics(filtered_trades),
            "trades_for_charts": [],  # overridden by router
        }

    # ----------------------------------------------------------------
    # Period filtering
    # ----------------------------------------------------------------

    def _filter_trades_by_period(self, trades: List[Dict], period: str) -> List[Dict]:
        since = _period_to_since_date(period)
        if since is None:
            return trades
        since_str = since.isoformat()
        return [t for t in trades if (t.get("exit_date") or "") >= since_str]

    def _filter_history_by_period(self, history: List[Dict], period: str) -> List[Dict]:
        since = _period_to_since_date(period)
        if since is None:
            return history
        since_str = since.isoformat()
        return [h for h in history if (h.get("snapshot_date") or "") >= since_str]

    # ----------------------------------------------------------------
    # Metric builders
    # ----------------------------------------------------------------

    def _build_executive_metrics(self, trades: List[Dict], history: List[Dict]) -> Dict:
        if not trades:
            return {}

        wins = [t for t in trades if t.get("pnl", 0) > 0]
        losses = [t for t in trades if t.get("pnl", 0) < 0]

        avg_win = sum(t["pnl"] for t in wins) / len(wins) if wins else 0
        avg_loss = sum(t["pnl"] for t in losses) / len(losses) if losses else 0
        expectancy = (
            (len(wins) / len(trades)) * avg_win
            + (len(losses) / len(trades)) * avg_loss
        )
        gross_wins = sum(t["pnl"] for t in wins) if wins else 0
        gross_losses = abs(sum(t["pnl"] for t in losses)) if losses else 0
        profit_factor = gross_wins / gross_losses if gross_losses > 0 else 0

        max_dd_pct = 0.0
        if history:
            peak = 0.0
            for h in history:
                v = h.get("total_value", 0)
                if v > peak:
                    peak = v
                if peak > 0:
                    dd = (v - peak) / peak * 100
                    if dd < max_dd_pct:
                        max_dd_pct = dd

        return {
            "sharpe_ratio": 0.0,
            "sharpe_method": "insufficient_data",
            "max_drawdown": {"percent": round(max_dd_pct, 2), "amount": 0.0, "date": None},
            "recovery_factor": 0.0,
            "expectancy": round(expectancy, 2),
            "profit_factor": round(profit_factor, 2),
            "risk_reward_ratio": round(avg_win / abs(avg_loss) if avg_loss != 0 else 0, 2),
        }

    def _build_advanced_metrics(self, trades: List[Dict]) -> Dict:
        if not trades:
            return {}

        wins = [t for t in trades if t.get("pnl", 0) > 0]
        losses = [t for t in trades if t.get("pnl", 0) <= 0]

        avg_hold_winners = (
            sum(t.get("holding_days", 0) for t in wins) / len(wins) if wins else 0
        )
        avg_hold_losers = (
            sum(t.get("holding_days", 0) for t in losses) / len(losses) if losses else 0
        )

        win_streak = loss_streak = cur_win = cur_loss = 0
        for t in trades:
            if t.get("pnl", 0) > 0:
                cur_win += 1
                cur_loss = 0
            else:
                cur_loss += 1
                cur_win = 0
            win_streak = max(win_streak, cur_win)
            loss_streak = max(loss_streak, cur_loss)

        return {
            "win_streak": win_streak,
            "loss_streak": loss_streak,
            "avg_hold_winners": round(avg_hold_winners, 1),
            "avg_hold_losers": round(avg_hold_losers, 1),
            "trade_frequency": 0.0,
            "capital_efficiency": 0.0,
            "days_underwater": 0,
        }

    def _build_market_comparison(self, trades: List[Dict]) -> Dict:
        result = {}
        for market in ("US", "UK"):
            mt = [t for t in trades if t.get("market") == market]
            if not mt:
                continue
            wins = [t for t in mt if t.get("pnl", 0) > 0]
            result[market.lower()] = {
                "total_trades": len(mt),
                "win_rate": round(len(wins) / len(mt) * 100, 1),
                "total_pnl": round(sum(t.get("pnl", 0) for t in mt), 2),
                "avg_pnl": round(sum(t.get("pnl", 0) for t in mt) / len(mt), 2),
            }
        return result

    def _build_exit_reasons(self, trades: List[Dict]) -> List[Dict]:
        counts = Counter(t.get("exit_reason", "Unknown") for t in trades)
        total = len(trades)
        return [
            {
                "exit_reason": reason,
                "count": count,
                "percentage": round(count / total * 100, 1),
                "total_pnl": round(
                    sum(t.get("pnl", 0) for t in trades if t.get("exit_reason") == reason), 2
                ),
            }
            for reason, count in counts.most_common()
        ]

    def _build_monthly_data(self, trades: List[Dict]) -> List[Dict]:
        buckets: Dict[str, list] = defaultdict(list)
        for t in trades:
            exit_date = str(t.get("exit_date", ""))
            if len(exit_date) >= 7:
                buckets[exit_date[:7]].append(t)
        result = []
        for month in sorted(buckets.keys()):
            mt = buckets[month]
            wins = [t for t in mt if t.get("pnl", 0) > 0]
            result.append({
                "month": month,
                "trade_count": len(mt),
                "win_rate": round(len(wins) / len(mt) * 100, 1) if mt else 0,
                "total_pnl": round(sum(t.get("pnl", 0) for t in mt), 2),
            })
        return result

    def _build_day_of_week(self, trades: List[Dict]) -> List[Dict]:
        return []

    def _build_holding_periods(self, trades: List[Dict]) -> List[Dict]:
        return []

    def _build_top_performers(self, trades: List[Dict]) -> Dict:
        sorted_trades = sorted(trades, key=lambda t: t.get("pnl", 0), reverse=True)
        return {"winners": sorted_trades[:3], "losers": sorted_trades[-3:]}

    def _build_consistency_metrics(self, trades: List[Dict]) -> Dict:
        return {}
