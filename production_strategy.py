# =====================================================================
# PRODUCTION MOMENTUM STRATEGY - FINAL VERSION
# =====================================================================
# Optimized parameters from extensive backtesting:
# - 26.37% CAGR, 1.29 Sharpe, -25.38% Max DD
# - Profit-lock stop loss system with 10-day grace period
# =====================================================================

import pandas as pd
import numpy as np
import yfinance as yf
import os
import sys
from datetime import datetime

# ST-05 (BLG-TECH-15, v9.0): compute_signals/compute_atr/compute_risk_on/
# transaction_fee/compute_rebalance_dates/backtest are the single shared
# implementation in backend/services/strategy_engine.py — also used by
# backend/services/backtest_rule_service.py. See that module's docstring
# for the consolidation's design notes (regime state as an explicit
# parameter; trade record field-naming schema).
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
from services.strategy_engine import (  # noqa: E402
    compute_risk_on,
    compute_atr,
    compute_signals,
    transaction_fee,
    compute_rebalance_dates,
    backtest,
)

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# =====================================================================
# CONFIGURATION
# =====================================================================

# Mode: 'optimize' or 'production'
MODE = "production"  # Set to 'optimize' to re-run parameter sweep

# Data split for validation
TRAIN_END = "2022-12-31"  # In-sample period: 2018 - 2022
TEST_START = "2023-01-01"  # Out-of-sample: 2023 - 2026

# Optimal parameters (from backtesting)
OPTIMAL_PARAMS = {
    'lookback': 252,
    'top_n': 5,
    'atr_mult': 2,
    'rebalance_freq': 'ME',
    'min_position_pct': 0.05,
    'max_position_pct': 0.20,
    'min_hold_days': 10,
    'risk_off_mode': 'single',
    'stop_loss_mode': 'profit_lock',
    'initial_atr_mult': 5,
    'profit_atr_mult': 2
}

# Optimization parameter ranges (only used if MODE = 'optimize')
OPTIMIZE_PARAMS = {
    'lookbacks': [252],
    'top_ns': [5],
    'atr_mults': [2],
    'rebalance_freqs': ['ME'],
    'min_position_pcts': [0.05],
    'max_position_pcts': [0.20],
    'min_hold_days': [7, 10],
    'risk_off_modes': ['single'],
    'stop_loss_modes': ['simple', 'profit_lock'],
    'initial_atr_mults': [4, 5],
    'profit_atr_mults': [2, 3]
}

INITIAL_CAPITAL = 20000
OUTPUT_DIR = "production_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================================
# DATA LOADING
# =====================================================================

def _load_tickers() -> tuple:
    """Load active tickers from the DB ticker_universe table, along with each
    ticker's `created_at` date (used to gate its eligibility in compute_signals —
    BLG-BE-59 — so a ticker added today can't retroactively join the momentum/
    trend ranking competition for the entire historical window).
    Falls back to the CSV if DATABASE_URL is not set (local runs without DB);
    the CSV has no created_at column, so those tickers are returned with a
    created_at of None (no eligibility gating applied — preserves prior
    behaviour for local runs without a DB).
    """
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        try:
            import psycopg2
            from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
            # Render uses postgres:// scheme and may include ?pgbouncer=true which
            # psycopg2 rejects as an unknown DSN parameter — strip it here.
            clean_url = db_url.replace("postgres://", "postgresql://", 1)
            parsed = urlparse(clean_url)
            qs = {k: v for k, v in parse_qs(parsed.query).items() if k != "pgbouncer"}
            clean_url = urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))
            conn = psycopg2.connect(clean_url)
            with conn.cursor() as cur:
                cur.execute("SELECT ticker, created_at FROM ticker_universe WHERE active = TRUE ORDER BY ticker")
                rows = cur.fetchall()
            conn.close()
            tickers = [r[0] for r in rows]
            created_at = {r[0]: (pd.Timestamp(r[1]).normalize() if r[1] is not None else None) for r in rows}
            print(f"Loaded {len(tickers)} tickers from DB ticker_universe")
            return tickers, created_at
        except Exception as e:
            print(f"Warning: DB load failed ({e}), falling back to CSV")

    _SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(_SCRIPT_DIR, "backend", "tickers_full_list.csv"))
    tickers = df["Ticker"].dropna().unique().tolist()
    print(f"Loaded {len(tickers)} tickers from CSV fallback")
    return tickers, {t: None for t in tickers}

def download_in_chunks(tickers, calendar_index, start="2018-01-01", chunk_size=50):
    chunks = []
    for i in range(0, len(tickers), chunk_size):
        data = yf.download(
            tickers[i:i + chunk_size],
            start=start,
            auto_adjust=True,
            progress=False
        )["Close"]

        if isinstance(data, pd.Series):
            data = data.to_frame()

        data = data.dropna(axis=1, how="all")
        chunks.append(data)

    prices = pd.concat(chunks, axis=1).sort_index()
    # Constrain to SPY's own trading calendar so a stray off-calendar quote
    # from any single instrument (e.g. an index feed, or a live intraday
    # snapshot picked up mid-session on a manual run) can't inject a phantom
    # "trading day" that every other ticker then gets forward-filled into —
    # that previously produced fake same-day round-trip trades.
    prices = prices.reindex(calendar_index)
    return prices.ffill().bfill()

def perf_stats(returns, name, initial_capital=INITIAL_CAPITAL):
    equity = (1 + returns).cumprod()
    cagr = equity.iloc[-1]**(252 / len(returns)) - 1
    vol = returns.std() * np.sqrt(252)
    dd = equity / equity.cummax() - 1
    sharpe = np.nan if vol == 0 else cagr / vol
    
    downside = returns.copy()
    downside[downside > 0] = 0
    sortino = np.nan if downside.std() == 0 else cagr / (downside.std() * np.sqrt(252))
    calmar = np.nan if dd.min() == 0 else cagr / abs(dd.min())

    return {
        "Strategy": name,
        "CAGR %": round(cagr * 100, 2),
        "Volatility %": round(vol * 100, 2),
        "Sharpe": round(sharpe, 2) if not np.isnan(sharpe) else np.nan,
        "Sortino": round(sortino, 2) if not np.isnan(sortino) else np.nan,
        "Calmar": round(calmar, 2) if not np.isnan(calmar) else np.nan,
        "Max DD %": round(dd.min() * 100, 2),
        "Final Value (£)": round(equity.iloc[-1] * initial_capital, 0)
    }

def main():
    print("=" * 70)
    print("PRODUCTION MOMENTUM STRATEGY - BACKTEST")
    print("=" * 70)

    tickers, ticker_created_at = _load_tickers()
    print(f"\nUniverse size: {len(tickers)}")

    # Regime indicators, downloaded first so the reference US trading calendar
    # (SPY's own index) is available to constrain the price universe below.
    spy = yf.download("SPY", start="2018-01-01", auto_adjust=True, progress=False)["Close"].squeeze()
    ftse = yf.download("^FTSE", start="2018-01-01", auto_adjust=True, progress=False)["Close"].squeeze()

    # Never trust "today" (run time) as a completed trading day. Liquid
    # instruments like SPY get live pre-market quotes stamped with today's date
    # well before the session actually opens/closes, regardless of which
    # instrument sources them — anchoring the calendar to SPY's own index isn't
    # enough if SPY itself carries that incomplete snapshot. Truncating here
    # drops it from the shared calendar before anything else is built from it.
    _today = pd.Timestamp.now().normalize()
    spy = spy[spy.index < _today]
    ftse = ftse[ftse.index < _today]

    print("Downloading price data...")
    prices = download_in_chunks(tickers, calendar_index=spy.index)
    prices = prices.dropna(axis=1, thresh=252 * 3)
    print(f"Tickers after cleaning: {prices.shape[1]}")
    print(f"Date range: {prices.index.min().date()} to {prices.index.max().date()}")

    # Reindex then forward-fill (not fill_value=False): a date missing from
    # spy/ftse's own data (e.g. a market holiday for one side) should carry
    # forward the last known regime state, not be silently treated as risk-off.
    # ST-05 (BLG-TECH-15, v9.0): local variables passed explicitly into
    # backtest() below, not module globals — see strategy_engine.py's
    # module docstring design note 1. The full prices.index is a superset
    # of the train/test slices used further down, so the same regime_us/
    # regime_uk series is valid for all three backtest() calls without
    # re-slicing (is_risk_on only ever looks up dates actually iterated).
    regime_us = compute_risk_on(spy).reindex(prices.index).ffill().fillna(False).astype(bool)
    regime_uk = compute_risk_on(ftse).reindex(prices.index).ffill().fillna(False).astype(bool)

    print("Computing ATR...")
    atr = compute_atr(prices)

    # =====================================================================
    # RUN BACKTEST
    # =====================================================================

    print("\n" + "=" * 70)
    print("RUNNING PRODUCTION BACKTEST")
    print("=" * 70)

    params = OPTIMAL_PARAMS
    print(f"\nParameters:")
    for k, v in params.items():
        print(f"  {k}: {v}")

    # Full period backtest
    signals_full = compute_signals(prices, params['lookback'], params['top_n'], created_at=ticker_created_at)
    volatility_full = prices.pct_change().rolling(60).std()
    
    pv_full, returns_full, trades_full = backtest(
        signals_full, prices, volatility_full, atr, regime_us, regime_uk,
        rebalance_freq=params['rebalance_freq'],
        atr_mult=params['atr_mult'],
        min_position_pct=params['min_position_pct'],
        max_position_pct=params['max_position_pct'],
        min_hold_days=params['min_hold_days'],
        risk_off_mode=params['risk_off_mode'],
        stop_loss_mode=params['stop_loss_mode'],
        initial_atr_mult=params['initial_atr_mult'],
        profit_atr_mult=params['profit_atr_mult']
    )
    
    # In-sample backtest (training period)
    prices_train = prices.loc[:TRAIN_END]
    signals_train = compute_signals(prices_train, params['lookback'], params['top_n'], created_at=ticker_created_at)
    volatility_train = prices_train.pct_change().rolling(60).std()
    atr_train = compute_atr(prices_train)
    
    pv_train, returns_train, trades_train = backtest(
        signals_train, prices_train, volatility_train, atr_train, regime_us, regime_uk,
        rebalance_freq=params['rebalance_freq'],
        atr_mult=params['atr_mult'],
        min_position_pct=params['min_position_pct'],
        max_position_pct=params['max_position_pct'],
        min_hold_days=params['min_hold_days'],
        risk_off_mode=params['risk_off_mode'],
        stop_loss_mode=params['stop_loss_mode'],
        initial_atr_mult=params['initial_atr_mult'],
        profit_atr_mult=params['profit_atr_mult']
    )
    
    # Out-of-sample backtest (validation period)
    prices_test = prices.loc[TEST_START:]
    signals_test = compute_signals(prices_test, params['lookback'], params['top_n'], created_at=ticker_created_at)
    volatility_test = prices_test.pct_change().rolling(60).std()
    atr_test = compute_atr(prices_test)
    
    pv_test, returns_test, trades_test = backtest(
        signals_test, prices_test, volatility_test, atr_test, regime_us, regime_uk,
        rebalance_freq=params['rebalance_freq'],
        atr_mult=params['atr_mult'],
        min_position_pct=params['min_position_pct'],
        max_position_pct=params['max_position_pct'],
        min_hold_days=params['min_hold_days'],
        risk_off_mode=params['risk_off_mode'],
        stop_loss_mode=params['stop_loss_mode'],
        initial_atr_mult=params['initial_atr_mult'],
        profit_atr_mult=params['profit_atr_mult']
    )
    
    # =====================================================================
    # RESULTS & ANALYSIS
    # =====================================================================
    
    print("\n" + "=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)
    
    stats_full = perf_stats(returns_full, "Full Period (2018-2026)")
    stats_train = perf_stats(returns_train, "In-Sample (2018-2022)")
    stats_test = perf_stats(returns_test, "Out-of-Sample (2023-2026)")
    
    comparison_df = pd.DataFrame([stats_full, stats_train, stats_test]).set_index("Strategy")
    print("\n", comparison_df)
    
    # Trade statistics
    print("\n" + "=" * 70)
    print("TRADE STATISTICS - FULL PERIOD")
    print("=" * 70)
    
    # Realized (closed) vs still-open positions — win rate, avg win/loss, and grace-period
    # stats describe completed round trips, so mixing in unrealized marks would conflate
    # the two. Open positions are reported separately below instead.
    closed_trades = trades_full[trades_full["Exit Reason"] != "Open (Unrealized)"].copy()
    open_trades = trades_full[trades_full["Exit Reason"] == "Open (Unrealized)"].copy()
    
    win_trades = closed_trades[closed_trades["PnL (£)"] > 0]
    loss_trades = closed_trades[closed_trades["PnL (£)"] <= 0]
    
    print(f"\nTotal closed trades: {len(closed_trades)}")
    print(f"Win rate: {len(win_trades)/len(closed_trades)*100:.2f}%")
    print(f"Average win: £{win_trades['PnL (£)'].mean():.2f}")
    print(f"Average loss: £{loss_trades['PnL (£)'].mean():.2f}")
    print(f"Win/Loss ratio: {abs(win_trades['PnL (£)'].mean() / loss_trades['PnL (£)'].mean()):.2f}")
    print(f"Average holding period: {closed_trades['Holding Days'].mean():.1f} days")
    print(f"Largest win: £{win_trades['PnL (£)'].max():.2f}")
    print(f"Largest loss: £{loss_trades['PnL (£)'].min():.2f}")
    
    # Exit reason breakdown
    print("\n--- Exit Reason Breakdown ---")
    print(closed_trades["Exit Reason"].value_counts())
    
    # Grace period analysis
    early_exits = closed_trades[closed_trades["Holding Days"] <= params['min_hold_days']]
    print(f"\nTrades exiting at/before {params['min_hold_days']}-day grace period: {len(early_exits)} ({len(early_exits)/len(closed_trades)*100:.1f}%)")
    
    # Profitable vs unprofitable stops
    stop_trades = closed_trades[closed_trades["Exit Reason"] == "Stop"]
    profitable_stops = stop_trades[stop_trades["Was Profitable"]]
    losing_stops = stop_trades[~stop_trades["Was Profitable"]]
    
    print(f"\n--- Stop Loss Analysis ---")
    print(f"Total stops: {len(stop_trades)}")
    print(f"Profitable stops (tight 2x ATR): {len(profitable_stops)} ({len(profitable_stops)/len(stop_trades)*100:.1f}%)")
    print(f"Losing stops (wide 5x ATR): {len(losing_stops)} ({len(losing_stops)/len(stop_trades)*100:.1f}%)")
    
    # Still-open positions (never hit an exit condition before the price data ended)
    if len(open_trades) > 0:
        print(f"\n--- Open Positions (unrealized, as of {prices.index[-1].date()}) ---")
        print(open_trades[["Ticker", "Entry Date", "Entry", "Exit", "PnL (£)", "PnL %"]].to_string(index=False))
    
    # Yearly breakdown
    print("\n" + "=" * 70)
    print("YEARLY PERFORMANCE")
    print("=" * 70)
    
    trades_full['Entry Year'] = trades_full['Entry Date'].dt.year
    
    # Yearly aggregates feed backtest_yearly_performance on the Strategy Benchmark page,
    # which (like Panel 1) assumes closed trades — computed on closed_trades to stay
    # consistent with the win-rate/PnL stats above and with import_backtest.py's filtering.
    closed_trades['Entry Year'] = closed_trades['Entry Date'].dt.year
    yearly_stats = closed_trades.groupby('Entry Year').agg({
        'PnL (£)': ['count', 'mean', 'sum'],
        'Holding Days': 'mean',
        'Was Profitable': lambda x: x.sum() / len(x) * 100
    })
    yearly_stats.columns = ['Num Trades', 'Avg PnL (£)', 'Total PnL (£)', 'Avg Hold Days', 'Win Rate %']
    print("\n", yearly_stats)
    
    # Top winners and losers
    print("\n" + "=" * 70)
    print("TOP 10 WINNERS")
    print("=" * 70)
    print(trades_full.nlargest(10, 'PnL (£)')[['Ticker', 'Entry Date', 'Exit Date', 'Holding Days', 'Entry', 'Exit', 'PnL (£)', 'PnL %', 'Exit Reason']])
    
    print("\n" + "=" * 70)
    print("TOP 10 LOSERS")
    print("=" * 70)
    print(trades_full.nsmallest(10, 'PnL (£)')[['Ticker', 'Entry Date', 'Exit Date', 'Holding Days', 'Entry', 'Exit', 'PnL (£)', 'PnL %', 'Exit Reason']])
    
    # =====================================================================
    # SAVE RESULTS
    # =====================================================================
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    comparison_df.to_csv(os.path.join(OUTPUT_DIR, f"performance_summary_{timestamp}.csv"))
    trades_full.to_csv(os.path.join(OUTPUT_DIR, f"all_trades_{timestamp}.csv"), index=False)
    yearly_stats.to_csv(os.path.join(OUTPUT_DIR, f"yearly_performance_{timestamp}.csv"))
    
    print("\n" + "=" * 70)
    print("FILES SAVED")
    print("=" * 70)
    print(f"Performance summary: production_results/performance_summary_{timestamp}.csv")
    print(f"All trades: production_results/all_trades_{timestamp}.csv")
    print(f"Yearly performance: production_results/yearly_performance_{timestamp}.csv")
    
    print("\n" + "=" * 70)
    print("BACKTEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()