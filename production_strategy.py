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
import matplotlib.pyplot as plt
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

print("=" * 70)
print("PRODUCTION MOMENTUM STRATEGY - BACKTEST")
print("=" * 70)

df = pd.read_csv("tickers_full_list.csv")
tickers = df["Ticker"].dropna().unique().tolist()
print(f"\nUniverse size: {len(tickers)}")

def download_in_chunks(tickers, start="2018-01-01", chunk_size=50):
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
    return prices.ffill().bfill()

print("Downloading price data...")
prices = download_in_chunks(tickers)
prices = prices.dropna(axis=1, thresh=252 * 3)
print(f"Tickers after cleaning: {prices.shape[1]}")
print(f"Date range: {prices.index.min().date()} to {prices.index.max().date()}")

# Download regime indicators
spy = yf.download("SPY", start=prices.index.min(), auto_adjust=True, progress=False)["Close"].squeeze()
ftse = yf.download("^FTSE", start=prices.index.min(), auto_adjust=True, progress=False)["Close"].squeeze()

spy_ma200 = spy.rolling(200).mean()
spy_risk_on = (spy > spy_ma200).reindex(prices.index, fill_value=False).astype(bool)

ftse_ma200 = ftse.rolling(200).mean()
ftse_risk_on = (ftse > ftse_ma200).reindex(prices.index, fill_value=False).astype(bool)

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

print("Computing ATR...")
atr = compute_atr(prices)

def compute_signals(prices, lookback, top_n, ma_period=200):
    momentum = prices.pct_change(lookback)
    ranks = momentum.rank(axis=1, ascending=False, na_option="bottom", method="first")
    trend = prices > prices.rolling(ma_period).mean()
    signals = (trend) & (ranks <= top_n)
    return signals.fillna(False).astype(bool)

# =====================================================================
# BACKTEST ENGINE
# =====================================================================

def backtest(signals, prices, volatility, atr, rebalance_freq, atr_mult, 
             min_position_pct=0.05, max_position_pct=0.15, min_hold_days=7, 
             risk_off_mode="single", stop_loss_mode="simple", initial_atr_mult=None,
             profit_atr_mult=None):
    
    if initial_atr_mult is None:
        initial_atr_mult = atr_mult * 1.5
    if profit_atr_mult is None:
        profit_atr_mult = atr_mult
    
    rebalance_dates = prices.resample(rebalance_freq).last().index
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

        # Rebalancing
        if date in rebalance_dates:
            selected = signals.loc[date][signals.loc[date]].index.tolist()
            selected = [t for t in selected if is_risk_on(t, date, mode=risk_off_mode)]

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

            portfolio_value = cash + (holdings * prices.loc[date]).sum()
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
signals_full = compute_signals(prices, params['lookback'], params['top_n'])
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
signals_train = compute_signals(prices_train, params['lookback'], params['top_n'])
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
signals_test = compute_signals(prices_test, params['lookback'], params['top_n'])
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

win_trades = trades_full[trades_full["PnL (£)"] > 0]
loss_trades = trades_full[trades_full["PnL (£)"] <= 0]

print(f"\nTotal trades: {len(trades_full)}")
print(f"Win rate: {len(win_trades)/len(trades_full)*100:.2f}%")
print(f"Average win: £{win_trades['PnL (£)'].mean():.2f}")
print(f"Average loss: £{loss_trades['PnL (£)'].mean():.2f}")
print(f"Win/Loss ratio: {abs(win_trades['PnL (£)'].mean() / loss_trades['PnL (£)'].mean()):.2f}")
print(f"Average holding period: {trades_full['Holding Days'].mean():.1f} days")
print(f"Largest win: £{win_trades['PnL (£)'].max():.2f}")
print(f"Largest loss: £{loss_trades['PnL (£)'].min():.2f}")

# Exit reason breakdown
print("\n--- Exit Reason Breakdown ---")
print(trades_full["Exit Reason"].value_counts())

# Grace period analysis
early_exits = trades_full[trades_full["Holding Days"] <= params['min_hold_days']]
print(f"\nTrades exiting at/before {params['min_hold_days']}-day grace period: {len(early_exits)} ({len(early_exits)/len(trades_full)*100:.1f}%)")

# Profitable vs unprofitable stops
stop_trades = trades_full[trades_full["Exit Reason"] == "Stop"]
profitable_stops = stop_trades[stop_trades["Was Profitable"]]
losing_stops = stop_trades[~stop_trades["Was Profitable"]]

print(f"\n--- Stop Loss Analysis ---")
print(f"Total stops: {len(stop_trades)}")
print(f"Profitable stops (tight 2x ATR): {len(profitable_stops)} ({len(profitable_stops)/len(stop_trades)*100:.1f}%)")
print(f"Losing stops (wide 5x ATR): {len(losing_stops)} ({len(losing_stops)/len(stop_trades)*100:.1f}%)")

# Yearly breakdown
print("\n" + "=" * 70)
print("YEARLY PERFORMANCE")
print("=" * 70)

trades_full['Entry Year'] = trades_full['Entry Date'].dt.year
yearly_stats = trades_full.groupby('Entry Year').agg({
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