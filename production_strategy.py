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
from datetime import datetime

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

def compute_risk_on(price, ma_period=200):
    """True where price is above its own ma_period-day moving average.

    Forward-fills the raw price series *before* computing the moving average
    and the comparison — not after. A malformed/incomplete daily bar from the
    data provider (e.g. SPY's Close coming back NaN while Volume is populated,
    seen 2026-07-24) would otherwise poison both sides: the rolling mean drops
    below min_periods and returns NaN, and `NaN > NaN` evaluates to a real
    `False`, not a NaN — so a downstream `.ffill()` on the comparison result
    can't recover it, and the day gets silently recorded as risk-off even
    though the last known close was solidly risk-on. Forward-filling the
    price itself first means one missing bar just carries the prior day's
    price forward into both calculations, as intended.
    """
    price_filled = price.ffill()
    ma = price_filled.rolling(ma_period).mean()
    return price_filled > ma

def is_risk_on(ticker, date, mode="single"):
    spy_on = bool(spy_risk_on.at[date])
    ftse_on = bool(ftse_risk_on.at[date])
    
    if mode == "single":
        return ftse_on if ticker.endswith(".L") else spy_on
    elif mode == "dual":
        return spy_on or ftse_on
    elif mode == "dual_strict":
        return spy_on and ftse_on

def transaction_fee(ticker, side):
    if ticker.endswith(".L"):
        return 0.005 if side == "buy" else 0.0
    return 0.0015

# =====================================================================
# TECHNICAL INDICATORS
# =====================================================================

def compute_atr(prices):
    high = prices.copy()
    low = prices.copy()
    close = prices.copy()

    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1)
    tr.columns = pd.MultiIndex.from_tuples([(c, "tr") for c in tr.columns])
    tr = tr.T.groupby(level=0).max().T
    atr = tr.rolling(14).mean()
    return atr

def compute_signals(prices, lookback, top_n, ma_period=200, created_at=None):
    momentum = prices.pct_change(lookback)
    if created_at:
        # Mask each ticker's momentum to NaN before its own created_at date so
        # it cannot participate in the cross-sectional rank computation for
        # any other ticker on those historical dates (na_option="bottom" below
        # excludes NaNs from influencing the relative ranks of real values).
        # This is what makes a ticker addition today retroactively inert for
        # the entire pre-existing historical window (AC-01/AC-02/AC-03,
        # BLG-BE-59) — masking only the final signal (below) is not enough,
        # since the ticker's raw momentum score would still shift the ranks
        # of every other ticker on dates before it was ever tracked.
        for ticker in momentum.columns:
            cutoff = created_at.get(ticker)
            if cutoff is not None and not pd.isna(cutoff):
                momentum.loc[momentum.index < cutoff, ticker] = np.nan
    ranks = momentum.rank(axis=1, ascending=False, na_option="bottom", method="first")
    trend = prices > prices.rolling(ma_period).mean()
    signals = (trend) & (ranks <= top_n)
    signals = signals.fillna(False).astype(bool)
    if created_at:
        for ticker in signals.columns:
            cutoff = created_at.get(ticker)
            if cutoff is not None and not pd.isna(cutoff):
                signals.loc[signals.index < cutoff, ticker] = False
    return signals

# =====================================================================
# BACKTEST ENGINE
# =====================================================================

def compute_rebalance_dates(price_index, rebalance_freq, as_of=None):
    """Return the subset of price_index at which a rebalance occurs.

    price_index.resample(rebalance_freq).last().index would return calendar
    period-end labels (e.g. 2026-01-31) even when that exact date is a
    weekend and never appears in price_index — silently skipping monthly
    rotation for any month whose last calendar day falls on a Sat/Sun.
    Group the actual (business-day) index by period and take each period's
    real last row instead, so the result only ever contains dates that
    genuinely exist in price_index.

    BLG-BE-109: a nightly run always fetches prices through "today", so the
    naive tail(1)-per-period grab above treats today's row as if it were
    that period's true close even when the period (e.g. the current
    calendar month) has not actually finished yet — a premature/incorrect
    rebalance signal. Exclude any rebalance date whose period is still the
    real current period as of wall-clock "now" (or the injected `as_of`,
    for deterministic testing). Purely historical windows (e.g. the
    in-sample TRAIN_END slice used below) are unaffected, since their last
    row's period will already be strictly before the real current period.
    """
    period_freq = rebalance_freq[:-1] if rebalance_freq.endswith("E") else rebalance_freq
    rebalance_dates = price_index.to_series().groupby(price_index.to_period(period_freq)).tail(1).index

    now = as_of if as_of is not None else pd.Timestamp.now(tz=price_index.tz)
    current_real_period = now.to_period(period_freq)
    return rebalance_dates[rebalance_dates.to_period(period_freq) != current_real_period]


def backtest(signals, prices, volatility, atr, rebalance_freq, atr_mult,
             min_position_pct=0.05, max_position_pct=0.15, min_hold_days=7,
             risk_off_mode="single", stop_loss_mode="simple", initial_atr_mult=None,
             profit_atr_mult=None, as_of=None):

    if initial_atr_mult is None:
        initial_atr_mult = atr_mult * 1.5
    if profit_atr_mult is None:
        profit_atr_mult = atr_mult

    rebalance_dates = compute_rebalance_dates(prices.index, rebalance_freq, as_of=as_of)
    holdings = pd.Series(0.0, index=prices.columns)
    entry_prices = {}
    entry_dates = {}
    stop_prices = {}
    trades = []
    cash = INITIAL_CAPITAL
    portfolio_values = []

    for date in prices.index:
        current_positions = list(holdings[holdings > 0].index)
        
        # Stop loss with profit-lock logic
        for t in current_positions:
            if holdings[t] == 0:
                continue
                
            shares = holdings[t]
            
            if date not in atr.index or t not in atr.columns:
                continue
            atr_val = atr.loc[date, t]
            if np.isnan(atr_val):
                continue

            holding_days = (date - entry_dates[t]).days
            if holding_days < min_hold_days:
                continue

            current_price = prices.loc[date, t]
            entry_price = entry_prices[t]
            current_profit_pct = (current_price - entry_price) / entry_price
            
            if stop_loss_mode == "simple":
                active_atr_mult = atr_mult
            elif stop_loss_mode == "tiered":
                active_atr_mult = initial_atr_mult if holding_days < min_hold_days * 2 else atr_mult
            elif stop_loss_mode == "profit_lock":
                active_atr_mult = profit_atr_mult if current_profit_pct > 0 else initial_atr_mult
            else:
                active_atr_mult = atr_mult

            current_stop = stop_prices.get(t, -np.inf)
            new_stop = current_price - active_atr_mult * atr_val
            stop_prices[t] = max(current_stop, new_stop)

            if current_price <= stop_prices[t]:
                exit_price = current_price
                fee = transaction_fee(t, "sell")
                exit_adj = exit_price * (1 - fee)
                pnl = (exit_adj - entry_price) * shares

                trades.append({
                    "Ticker": t,
                    "Entry Date": entry_dates[t],
                    "Exit Date": date,
                    "Holding Days": holding_days,
                    "Entry": entry_price,
                    "Exit": exit_adj,
                    "PnL (£)": pnl,
                    "PnL %": round(current_profit_pct * 100, 2),
                    "Market": "UK" if t.endswith(".L") else "US",
                    "Exit Reason": "Stop",
                    "Was Profitable": current_profit_pct > 0
                })

                cash += shares * exit_adj
                holdings[t] = 0
                entry_prices.pop(t, None)
                entry_dates.pop(t, None)
                stop_prices.pop(t, None)

        # Risk-off exits
        for t in current_positions:
            if holdings[t] == 0:
                continue
                
            shares = holdings[t]
            
            if not is_risk_on(t, date, mode=risk_off_mode):
                holding_days = (date - entry_dates[t]).days
                exit_price = prices.loc[date, t]
                entry_price = entry_prices[t]
                current_profit_pct = (exit_price - entry_price) / entry_price
                
                fee = transaction_fee(t, "sell")
                exit_adj = exit_price * (1 - fee)
                pnl = (exit_adj - entry_price) * shares

                trades.append({
                    "Ticker": t,
                    "Entry Date": entry_dates[t],
                    "Exit Date": date,
                    "Holding Days": holding_days,
                    "Entry": entry_price,
                    "Exit": exit_adj,
                    "PnL (£)": pnl,
                    "PnL %": round(current_profit_pct * 100, 2),
                    "Market": "UK" if t.endswith(".L") else "US",
                    "Exit Reason": "Risk-Off",
                    "Was Profitable": current_profit_pct > 0
                })

                cash += shares * exit_adj
                holdings[t] = 0
                entry_prices.pop(t, None)
                entry_dates.pop(t, None)
                stop_prices.pop(t, None)

        # Today's qualifying, risk-on candidates — used both for the monthly
        # rotation-out below and the daily slot fill-in that follows it.
        selected = signals.loc[date][signals.loc[date]].index.tolist()
        selected = [t for t in selected if is_risk_on(t, date, mode=risk_off_mode)]

        # Monthly rebalance: rotate out any holding that has fallen out of the
        # current top-n qualifying set. Only evaluated on rebalance dates so a
        # position isn't force-sold mid-month over a temporary rank dip.
        if date in rebalance_dates:
            exits = []
            for t in list(holdings[holdings > 0].index):
                if t not in selected:
                    exits.append(t)

            for t in exits:
                shares = holdings[t]
                holding_days = (date - entry_dates[t]).days
                exit_price = prices.loc[date, t]
                entry_price = entry_prices[t]
                current_profit_pct = (exit_price - entry_price) / entry_price

                fee = transaction_fee(t, "sell")
                exit_adj = exit_price * (1 - fee)
                pnl = (exit_adj - entry_price) * shares

                trades.append({
                    "Ticker": t,
                    "Entry Date": entry_dates[t],
                    "Exit Date": date,
                    "Holding Days": holding_days,
                    "Entry": entry_price,
                    "Exit": exit_adj,
                    "PnL (£)": pnl,
                    "PnL %": round(current_profit_pct * 100, 2),
                    "Market": "UK" if t.endswith(".L") else "US",
                    "Exit Reason": "No longer qualifies",
                    "Was Profitable": current_profit_pct > 0
                })

                cash += shares * exit_adj
                holdings[t] = 0
                entry_prices.pop(t, None)
                entry_dates.pop(t, None)
                stop_prices.pop(t, None)

        # Daily slot fill-in: whenever fewer than top-n positions are held
        # (a stop, risk-off, or rotation exit freed up a slot), buy a
        # qualifying candidate as soon as one is available rather than
        # waiting for the next month-end rebalance to deploy the cash.
        num_existing = (holdings > 0).sum()
        num_new_slots = len(selected) - num_existing

        if num_new_slots > 0:
            existing_tickers = holdings[holdings > 0].index.tolist()
            new_candidates = [t for t in selected if t not in existing_tickers][:num_new_slots]

            if len(new_candidates) > 0:
                available_cash = cash
                vols = volatility.loc[date, new_candidates].replace(0, np.nan).dropna()

                if len(vols) > 0:
                    inv_vol = 1 / vols
                    weights = inv_vol / inv_vol.sum()

                    weights_constrained = {}
                    for t, w in weights.items():
                        weights_constrained[t] = max(min_position_pct, min(w, max_position_pct))

                    total_weight = sum(weights_constrained.values())
                    weights_final = {t: w / total_weight for t, w in weights_constrained.items()}

                    for t, w in weights_final.items():
                        buy_fee = transaction_fee(t, "buy")
                        price = prices.loc[date, t] * (1 + buy_fee)
                        alloc = available_cash * w
                        shares = alloc / price

                        holdings[t] = shares
                        entry_prices[t] = price
                        entry_dates[t] = date

                        atr_val = atr.loc[date, t]
                        if stop_loss_mode == "simple":
                            stop_prices[t] = price - atr_mult * atr_val
                        else:
                            stop_prices[t] = price - initial_atr_mult * atr_val

                        cash -= shares * price

        daily_value = cash + (holdings * prices.loc[date]).sum()
        portfolio_values.append(daily_value)

    # Positions still open when the price data ends never hit a stop, risk-off,
    # or rebalance exit, so the loop above never appends a trade for them — without
    # this they vanish from trades_df entirely, making the final weeks of a run
    # look like no activity took place even though capital is deployed.
    last_date = prices.index[-1]
    for t in list(holdings[holdings > 0].index):
        shares = holdings[t]
        entry_price = entry_prices[t]
        current_price = prices.loc[last_date, t]
        current_profit_pct = (current_price - entry_price) / entry_price
        holding_days = (last_date - entry_dates[t]).days

        trades.append({
            "Ticker": t,
            "Entry Date": entry_dates[t],
            "Exit Date": last_date,
            "Holding Days": holding_days,
            "Entry": entry_price,
            "Exit": current_price,
            "PnL (£)": (current_price - entry_price) * shares,
            "PnL %": round(current_profit_pct * 100, 2),
            "Market": "UK" if t.endswith(".L") else "US",
            "Exit Reason": "Open (Unrealized)",
            "Was Profitable": current_profit_pct > 0
        })

    pv = pd.Series(portfolio_values, index=prices.index)
    returns = pv.pct_change().fillna(0)
    trades_df = pd.DataFrame(trades)

    return pv, returns, trades_df

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
    # `global` — is_risk_on() (module-level function) reads these as free
    # variables resolved against module scope; without this declaration they
    # would be local to main() and invisible to is_risk_on() when it's called
    # from inside backtest() below (LEGB scoping — is_risk_on is not nested
    # inside main(), so its non-local names resolve to the module, not to
    # main()'s locals). This is the only module-global state any function
    # defined above main() depends on.
    global spy_risk_on, ftse_risk_on

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
    spy_risk_on = compute_risk_on(spy).reindex(prices.index).ffill().fillna(False).astype(bool)
    ftse_risk_on = compute_risk_on(ftse).reindex(prices.index).ffill().fillna(False).astype(bool)

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
        signals_full, prices, volatility_full, atr,
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
        signals_train, prices_train, volatility_train, atr_train,
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
        signals_test, prices_test, volatility_test, atr_test,
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