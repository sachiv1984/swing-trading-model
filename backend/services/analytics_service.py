"""
Analytics Service

Calculates all portfolio metrics from trade and portfolio history data.
Field names match the canonical API contract (analytics_endpoints.md v1.8.1)
and the frontend component field expectations exactly.

Key field mappings (snake_case → camelCase after frontend conversion):
  monthly_data:      pnl, trades, win_rate, month
  exit_reasons:      reason, count, win_rate, total_pnl, avg_pnl, percentage
  market_comparison: US/UK keys → totalTrades, winRate, totalPnl, avgWin,
                     avgLoss, bestPerformer, worstPerformer
  top_performers:    winners/losers → ticker, pnl, pnl_percent, entry_date,
                     holding_days, exit_reason
  consistency_metrics: consecutive_profitable_months, current_streak,
                       win_rate_std_dev, pnl_std_dev
  day_of_week:       day, trade_count, avg_pnl (7 entries always)
  holding_periods:   period, trades, avg_pnl, win_rate (5 buckets always)
"""

from collections import Counter, defaultdict
from datetime import date, timedelta
from typing import Dict, List, Optional
import math
import statistics


def _period_to_since_date(period: str) -> Optional[date]:
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
        raise ValueError(f"Invalid period '{period}'.")
    return period_map[period]


class AnalyticsService:

    def calculate_metrics_from_data(
        self,
        trades: List[Dict],
        portfolio_history: List[Dict],
        period: str = "all_time",
        min_trades: int = 10,
    ) -> Dict:
        filtered = self._filter_trades_by_period(trades, period)
        filtered_history = self._filter_history_by_period(portfolio_history, period)

        total_trades = len(filtered)
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
                "monthly_data": [],
                "day_of_week": self._build_day_of_week(filtered),
                "holding_periods": self._build_holding_periods(filtered),
                "top_performers": {"winners": [], "losers": []},
                "consistency_metrics": {},
                "trades_for_charts": [],
            }

        wins = [t for t in filtered if t.get("pnl", 0) > 0]
        total_pnl = sum(t.get("pnl", 0) for t in filtered)
        win_rate = round(len(wins) / total_trades * 100, 1)

        monthly = self._build_monthly_data(filtered)

        return {
            "summary": {
                "total_trades": total_trades,
                "win_rate": win_rate,
                "total_pnl": round(total_pnl, 2),
                "has_enough_data": True,
                "min_required": min_trades,
            },
            "executive_metrics": self._build_executive_metrics(filtered, filtered_history),
            "advanced_metrics": self._build_advanced_metrics(filtered, filtered_history),
            "market_comparison": self._build_market_comparison(filtered),
            "exit_reasons": self._build_exit_reasons(filtered),
            "monthly_data": monthly,
            "day_of_week": self._build_day_of_week(filtered),
            "holding_periods": self._build_holding_periods(filtered),
            "top_performers": self._build_top_performers(filtered),
            "consistency_metrics": self._build_consistency_metrics(monthly),
            "trades_for_charts": [],  # overridden by router
        }

    # ----------------------------------------------------------------
    # Period filtering
    # ----------------------------------------------------------------

    def _filter_trades_by_period(self, trades, period):
        since = _period_to_since_date(period)
        if since is None:
            return trades
        s = since.isoformat()
        return [t for t in trades if (t.get("exit_date") or "") >= s]

    def _filter_history_by_period(self, history, period):
        since = _period_to_since_date(period)
        if since is None:
            return history
        s = since.isoformat()
        return [h for h in history if (h.get("snapshot_date") or "") >= s]

    # ----------------------------------------------------------------
    # executive_metrics
    # ----------------------------------------------------------------

    def _build_executive_metrics(self, trades, history):
        if not trades:
            return {}

        wins  = [t for t in trades if t.get("pnl", 0) > 0]
        losses = [t for t in trades if t.get("pnl", 0) < 0]
        n = len(trades)

        avg_win  = sum(t["pnl"] for t in wins)  / len(wins)  if wins  else 0.0
        avg_loss = sum(t["pnl"] for t in losses) / len(losses) if losses else 0.0

        gross_profit = sum(t["pnl"] for t in wins)  if wins  else 0.0
        gross_loss   = abs(sum(t["pnl"] for t in losses)) if losses else 0.0
        profit_factor = round(gross_profit / gross_loss, 2) if gross_loss > 0 else 0.0

        expectancy = round(
            (len(wins) / n) * avg_win + (len(losses) / n) * avg_loss, 2
        )

        rr = round(avg_win / abs(avg_loss), 2) if avg_loss != 0 else 0.0

        # Max drawdown from portfolio history
        max_dd_pct = 0.0
        max_dd_amt = 0.0
        max_dd_date = None
        if history:
            peak = 0.0
            for h in history:
                v = h.get("total_value", 0)
                if v > peak:
                    peak = v
                if peak > 0:
                    dd_pct = (v - peak) / peak * 100
                    if dd_pct < max_dd_pct:
                        max_dd_pct = dd_pct
                        max_dd_amt = v - peak
                        max_dd_date = h.get("snapshot_date")

        # Sharpe (sample variance, requires 30+ history points)
        sharpe = 0.0
        sharpe_method = "insufficient_data"
        if len(history) >= 30:
            daily_returns = []
            for i in range(1, len(history)):
                prev = history[i - 1].get("total_value", 0)
                curr = history[i].get("total_value", 0)
                if prev > 0:
                    daily_returns.append((curr - prev) / prev)
            if len(daily_returns) >= 2:
                mean_r = sum(daily_returns) / len(daily_returns)
                variance = sum((r - mean_r) ** 2 for r in daily_returns) / (len(daily_returns) - 1)
                std_dev = math.sqrt(variance) if variance > 0 else 0
                if std_dev > 0:
                    sharpe = round((mean_r / std_dev) * math.sqrt(252), 2)
                    sharpe_method = "portfolio"

        # Recovery factor
        period_profit = (history[-1].get("total_value", 0) - history[0].get("total_value", 0)) if len(history) >= 2 else 0
        recovery_factor = round(period_profit / abs(max_dd_amt), 2) if max_dd_amt < 0 and period_profit > 0 else 0.0

        return {
            "sharpe_ratio": sharpe,
            "sharpe_method": sharpe_method,
            "max_drawdown": {
                "percent": round(max_dd_pct, 2),
                "amount": round(max_dd_amt, 2),
                "date": str(max_dd_date) if max_dd_date else None,
            },
            "recovery_factor": recovery_factor,
            "expectancy": expectancy,
            "profit_factor": profit_factor,
            "risk_reward_ratio": rr,
        }

    # ----------------------------------------------------------------
    # advanced_metrics
    # ----------------------------------------------------------------

    def _build_advanced_metrics(self, trades, history):
        if not trades:
            return {}

        wins   = [t for t in trades if t.get("pnl", 0) > 0]
        losses = [t for t in trades if t.get("pnl", 0) < 0]

        avg_hold_winners = round(
            sum(t.get("holding_days", 0) for t in wins) / len(wins), 1
        ) if wins else 0.0
        avg_hold_losers = round(
            sum(t.get("holding_days", 0) for t in losses) / len(losses), 1
        ) if losses else 0.0

        # Streak calculation (exit_date order, already ASC from router query)
        win_streak = loss_streak = cur_w = cur_l = 0
        for t in trades:
            if t.get("pnl", 0) > 0:
                cur_w += 1; cur_l = 0
            else:
                cur_l += 1; cur_w = 0
            win_streak  = max(win_streak,  cur_w)
            loss_streak = max(loss_streak, cur_l)

        # Trade frequency (trades per week)
        trade_frequency = 0.0
        if len(trades) >= 2:
            try:
                first = date.fromisoformat(str(trades[0].get("entry_date", "")))
                last  = date.fromisoformat(str(trades[-1].get("exit_date", "")))
                span  = (last - first).days
                if span > 0:
                    trade_frequency = round(len(trades) / span * 7, 1)
            except (ValueError, TypeError):
                pass

        # Capital efficiency — total_pnl / mean(total_cost) * 100
        capital_efficiency = 0.0
        costs = [t.get("total_cost") or t.get("shares", 0) * t.get("entry_price", 0)
                 for t in trades]
        valid_costs = [c for c in costs if c and c > 0]
        if valid_costs:
            avg_cost = sum(valid_costs) / len(valid_costs)
            total_pnl = sum(t.get("pnl", 0) for t in trades)
            capital_efficiency = round(total_pnl / avg_cost * 100, 2) if avg_cost else 0.0

        # Days underwater (trade-sequence method)
        running_eq = peak_eq = 0.0
        peak_date_str = None
        max_days_uw = 0
        for t in trades:
            running_eq += t.get("pnl", 0)
            if running_eq >= peak_eq:
                peak_eq = running_eq
                peak_date_str = str(t.get("exit_date", ""))
            elif peak_date_str:
                try:
                    td = date.fromisoformat(str(t.get("exit_date", "")))
                    pd = date.fromisoformat(peak_date_str)
                    max_days_uw = max(max_days_uw, (td - pd).days)
                except (ValueError, TypeError):
                    pass

        # Portfolio peak equity from history
        portfolio_peak = max((h.get("total_value", 0) for h in history), default=0.0)

        return {
            "win_streak": win_streak,
            "loss_streak": loss_streak,
            "avg_hold_winners": avg_hold_winners,
            "avg_hold_losers": avg_hold_losers,
            "trade_frequency": trade_frequency,
            "capital_efficiency": capital_efficiency,
            "days_underwater": max_days_uw,
            "peak_date": peak_date_str,
            "portfolio_peak_equity": round(portfolio_peak, 2),
        }

    # ----------------------------------------------------------------
    # market_comparison  — keys must be "US" / "UK" (uppercase)
    # ----------------------------------------------------------------

    def _build_market_comparison(self, trades):
        result = {}
        for market in ("US", "UK"):
            mt = [t for t in trades if t.get("market") == market]
            if not mt:
                result[market] = {
                    "total_trades": 0, "win_rate": 0.0, "total_pnl": 0.0,
                    "avg_win": 0.0, "avg_loss": 0.0,
                    "best_performer": None, "worst_performer": None,
                }
                continue
            wins   = [t for t in mt if t.get("pnl", 0) > 0]
            losses = [t for t in mt if t.get("pnl", 0) < 0]
            best   = max(mt, key=lambda t: t.get("pnl", 0))
            worst  = min(mt, key=lambda t: t.get("pnl", 0))
            result[market] = {
                "total_trades": len(mt),
                "win_rate":     round(len(wins) / len(mt) * 100, 1),
                "total_pnl":    round(sum(t.get("pnl", 0) for t in mt), 2),
                "avg_win":      round(sum(t["pnl"] for t in wins)   / len(wins),   2) if wins   else 0.0,
                "avg_loss":     round(sum(t["pnl"] for t in losses) / len(losses), 2) if losses else 0.0,
                "best_performer":  {"ticker": best["ticker"],  "pnl": round(best.get("pnl", 0),  2)},
                "worst_performer": {"ticker": worst["ticker"], "pnl": round(worst.get("pnl", 0), 2)},
            }
        return result

    # ----------------------------------------------------------------
    # exit_reasons  — field "reason" (not "exit_reason")
    # ----------------------------------------------------------------

    def _build_exit_reasons(self, trades):
        buckets: Dict[str, list] = defaultdict(list)
        for t in trades:
            reason = t.get("exit_reason") or "Manual Exit"
            buckets[reason].append(t)
        total = len(trades)
        result = []
        for reason, group in sorted(buckets.items(), key=lambda x: -len(x[1])):
            wins   = [t for t in group if t.get("pnl", 0) > 0]
            pnls   = [t.get("pnl", 0) for t in group]
            result.append({
                "reason":     reason,
                "count":      len(group),
                "win_rate":   round(len(wins) / len(group) * 100, 1),
                "total_pnl":  round(sum(pnls), 2),
                "avg_pnl":    round(sum(pnls) / len(pnls), 2),
                "percentage": round(len(group) / total * 100, 1),
            })
        return result

    # ----------------------------------------------------------------
    # monthly_data  — fields: month, pnl, trades, win_rate
    #   "pnl" (not "total_pnl"), "trades" (not "trade_count")
    #   MonthlyHeatmap reads: month.pnl, month.trades, month.winRate
    #   Win Rate by Month reads: month.winRate, month.tradeCount
    #   Both are satisfied: pnl + trades + win_rate + trade_count
    # ----------------------------------------------------------------

    def _build_monthly_data(self, trades):
        buckets: Dict[str, list] = defaultdict(list)
        for t in trades:
            d = str(t.get("exit_date", ""))
            if len(d) >= 7:
                buckets[d[:7]].append(t)

        result = []
        for month in sorted(buckets.keys()):
            mt   = buckets[month]
            wins = [t for t in mt if t.get("pnl", 0) > 0]
            pnl_val = round(sum(t.get("pnl", 0) for t in mt), 2)
            wr      = round(len(wins) / len(mt) * 100, 1) if mt else 0.0
            result.append({
                "month":       month,
                "pnl":         pnl_val,    # MonthlyHeatmap: month.pnl
                "trades":      len(mt),    # MonthlyHeatmap: month.trades
                "win_rate":    wr,         # → winRate after camelCase
                "trade_count": len(mt),    # Win Rate by Month tooltip: month.tradeCount
            })
        return result

    # ----------------------------------------------------------------
    # day_of_week  — 7 entries always
    # ----------------------------------------------------------------

    def _build_day_of_week(self, trades):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        buckets: Dict[str, list] = defaultdict(list)
        for t in trades:
            try:
                d = date.fromisoformat(str(t.get("exit_date", "")))
                buckets[days[d.weekday()]].append(t)
            except (ValueError, TypeError):
                pass
        return [
            {
                "day":         day,
                "trade_count": len(buckets[day]),
                "avg_pnl":     round(
                    sum(t.get("pnl", 0) for t in buckets[day]) / len(buckets[day]), 2
                ) if buckets[day] else 0.0,
            }
            for day in days
        ]

    # ----------------------------------------------------------------
    # holding_periods  — 5 buckets always
    # ----------------------------------------------------------------

    def _build_holding_periods(self, trades):
        buckets = [
            ("1-5 days",   1,  5),
            ("6-10 days",  6,  10),
            ("11-20 days", 11, 20),
            ("21-30 days", 21, 30),
            ("31+ days",   31, 9999),
        ]
        result = []
        for label, lo, hi in buckets:
            group = [t for t in trades if lo <= (t.get("holding_days") or 0) <= hi]
            wins  = [t for t in group if t.get("pnl", 0) > 0]
            result.append({
                "period":   label,
                "trades":   len(group),
                "avg_pnl":  round(
                    sum(t.get("pnl", 0) for t in group) / len(group), 2
                ) if group else 0.0,
                "win_rate": round(len(wins) / len(group) * 100, 1) if group else 0.0,
            })
        return result

    # ----------------------------------------------------------------
    # top_performers  — ticker, pnl, pnl_percent, entry_date,
    #                   holding_days, exit_reason  (up to 5 each)
    # ----------------------------------------------------------------

    def _build_top_performers(self, trades):
        by_pnl = sorted(trades, key=lambda t: t.get("pnl", 0), reverse=True)
        def _fmt(t):
            return {
                "ticker":       t.get("ticker", ""),
                "pnl":          round(t.get("pnl", 0), 2),
                "pnl_percent":  round(t.get("pnl_percent", 0), 2),
                "entry_date":   str(t.get("entry_date", "")),
                "holding_days": t.get("holding_days", 0),
                "exit_reason":  t.get("exit_reason") or "Manual Exit",
            }
        return {
            "winners": [_fmt(t) for t in by_pnl[:5]  if t.get("pnl", 0) > 0],
            "losers":  [_fmt(t) for t in by_pnl[-5:]  if t.get("pnl", 0) < 0],
        }

    # ----------------------------------------------------------------
    # consistency_metrics  — derived from monthly_data
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # calculate_cohort  — groups trades by entry period, computes stats
    # per metrics_definitions.md v1.7.0 Cohort Metrics section
    # ----------------------------------------------------------------

    def calculate_cohort(self, trades_with_stop: List[Dict], cohort_period: str) -> Dict:
        def _cohort_key(entry_date_str):
            if not entry_date_str:
                return None
            try:
                d = date.fromisoformat(str(entry_date_str)[:10])
            except (ValueError, TypeError):
                return None
            if cohort_period == "month":
                return f"{d.year}-{d.month:02d}"
            elif cohort_period == "quarter":
                q = (d.month - 1) // 3 + 1
                return f"{d.year}-Q{q:01d}"
            else:
                return str(d.year)

        def _period_label(key):
            if cohort_period == "month":
                y, m = key.split("-")
                month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                return f"{month_names[int(m) - 1]} {y}"
            elif cohort_period == "quarter":
                y, q = key.split("-")
                return f"{q} {y}"
            else:
                return key

        def _r_multiple(t):
            ep = t.get("entry_price") or 0
            sp = t.get("stop_price")
            xp = t.get("exit_price") or 0
            if sp is None or ep <= sp:
                return None
            denom = ep - sp
            if denom <= 0:
                return None
            return (xp - ep) / denom

        buckets: Dict[str, list] = defaultdict(list)
        for t in trades_with_stop:
            key = _cohort_key(t.get("entry_date"))
            if key:
                buckets[key].append(t)

        cohorts = []
        for key in sorted(buckets.keys(), reverse=True):
            group = buckets[key]
            wins = [t for t in group if t.get("pnl", 0) > 0]
            r_vals = [r for t in group for r in [_r_multiple(t)] if r is not None]
            cohorts.append({
                "period_label": _period_label(key),
                "trade_count": len(group),
                "win_rate": round(len(wins) / len(group) * 100, 1) if group else 0.0,
                "avg_r_multiple": round(sum(r_vals) / len(r_vals), 2) if r_vals else None,
                "total_pnl": round(sum(t.get("pnl", 0) for t in group), 2),
            })

        return {
            "period": cohort_period,
            "cohorts": cohorts,
            "has_enough_data": len(cohorts) >= 3,
        }

    # ----------------------------------------------------------------
    # calculate_r_multiple_distribution
    # per metrics_definitions.md v1.7.0 R-Multiple (Canonical Server-Side)
    # ----------------------------------------------------------------

    def calculate_r_multiple_distribution(self, trades_with_stop: List[Dict]) -> Dict:
        def _r_multiple(t):
            ep = t.get("entry_price") or 0
            sp = t.get("stop_price")
            xp = t.get("exit_price") or 0
            if sp is None or ep <= sp:
                return None
            denom = ep - sp
            if denom <= 0:
                return None
            return (xp - ep) / denom

        r_values = [r for t in trades_with_stop for r in [_r_multiple(t)] if r is not None]
        n = len(r_values)

        if n < 5:
            return {
                "has_enough_data": False,
                "total_qualifying_trades": n,
                "buckets": [],
                "median_r": None,
                "pct_above_1r": None,
                "avg_winner_r": None,
                "avg_loser_r": None,
            }

        bucket_defs = [
            ("< -2R",      None, -2),
            ("-2R to -1R",   -2, -1),
            ("-1R to 0R",    -1,  0),
            ("0R to 1R",      0,  1),
            ("1R to 2R",      1,  2),
            ("2R to 3R",      2,  3),
            ("> 3R",          3, None),
        ]
        buckets = []
        for label, lo, hi in bucket_defs:
            count = sum(
                1 for r in r_values
                if (lo is None or r >= lo) and (hi is None or r < hi)
            )
            buckets.append({"range": label, "count": count})

        sorted_r = sorted(r_values)
        mid = n // 2
        median_r = round(
            (sorted_r[mid - 1] + sorted_r[mid]) / 2 if n % 2 == 0 else sorted_r[mid], 2
        )

        winners = [r for r in r_values if r > 0]
        losers  = [r for r in r_values if r <= 0]

        return {
            "has_enough_data": True,
            "total_qualifying_trades": n,
            "buckets": buckets,
            "median_r": median_r,
            "pct_above_1r": round(sum(1 for r in r_values if r > 1) / n * 100, 1),
            "avg_winner_r": round(sum(winners) / len(winners), 2) if winners else None,
            "avg_loser_r":  round(sum(losers)  / len(losers),  2) if losers  else None,
        }

    def _build_consistency_metrics(self, monthly_data):
        if not monthly_data:
            return {
                "consecutive_profitable_months": 0,
                "current_streak": 0,
                "win_rate_std_dev": 0.0,
                "pnl_std_dev": 0.0,
            }

        # Longest profitable run
        best_streak = cur_streak = 0
        for m in monthly_data:
            if m.get("pnl", 0) > 0:
                cur_streak += 1
                best_streak = max(best_streak, cur_streak)
            else:
                cur_streak = 0

        # Current streak (from end)
        current = 0
        for m in reversed(monthly_data):
            if m.get("pnl", 0) > 0:
                current += 1
            else:
                break

        def _pop_std(values):
            if len(values) < 2:
                return 0.0
            mean = sum(values) / len(values)
            return round(math.sqrt(sum((v - mean) ** 2 for v in values) / len(values)), 2)

        return {
            "consecutive_profitable_months": best_streak,
            "current_streak": current,
            "win_rate_std_dev": _pop_std([m.get("win_rate", 0) for m in monthly_data]),
            "pnl_std_dev":      _pop_std([m.get("pnl", 0)      for m in monthly_data]),
        }
