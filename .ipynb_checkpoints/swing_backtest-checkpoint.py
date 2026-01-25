import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from collections import defaultdict
import warnings

# =========================
# CONFIG
# =========================

START_DATE = "2024-01-01"
END_DATE = "2026-01-01"

ACCOUNT_SIZE = 10_000
RISK_PER_TRADE = 0.01  # 1%

ATR_STOP = 2.0
ATR_TARGET = 4.0
MAX_HOLD_DAYS = 10

MAX_TRADES_PER_DAY = 3
MIN_ATR_PCT = 0.015  # 1.5%

TICKER_FILE = "tickers_full_list.csv"

# =========================
# DATA
# =========================

def download_data(ticker):
    try:
        df = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=True,
            progress=False,
        )
    except Exception:
        return None

    if df is None or df.empty:
        return None

    # Flatten multi-index columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    required = {"Open", "High", "Low", "Close"}
    if not required.issubset(df.columns):
        return None

    return df.dropna()

# =========================
# INDICATORS
# =========================

def add_indicators(df):
    df = df.copy()

    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()

    high_low = df["High"] - df["Low"]
    high_close = np.abs(df["High"] - df["Close"].shift())
    low_close = np.abs(df["Low"] - df["Close"].shift())

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()

    df["ATR_PCT"] = df["ATR"] / df["Close"]

    return df.dropna()

# =========================
# FEES
# =========================

def get_fees(ticker, amount, side):
    """
    side = "buy" or "sell"
    """
    # US tickers (no .L)
    if not ticker.endswith(".L"):
        fee_rate = 0.0015  # 0.15%
        return amount * fee_rate

    # UK tickers
    if ticker.endswith(".L"):
        if side == "buy":
            fee_rate = 0.005  # 0.5%
            return amount * fee_rate
        else:
            return 0.0

    return 0.0

# =========================
# STRATEGY
# =========================

def backtest_ticker(ticker, daily_trade_count):
    df = download_data(ticker)
    if df is None:
        return []

    df = add_indicators(df)
    trades = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]

        date = df.index[i].date()

        # ----- max trades per day -----
        if daily_trade_count[date] >= MAX_TRADES_PER_DAY:
            continue

        # ----- ATR % filter -----
        if row["ATR_PCT"] < MIN_ATR_PCT:
            continue

        # ENTRY: trend + momentum
        if (
            prev["Close"] < prev["SMA20"]
            and row["Close"] > row["SMA20"]
            and row["SMA20"] > row["SMA50"]
        ):
            entry_price = row["Close"]
            atr = row["ATR"]

            stop = entry_price - ATR_STOP * atr
            target = entry_price + ATR_TARGET * atr

            risk_amount = ACCOUNT_SIZE * RISK_PER_TRADE
            position_size = risk_amount / (entry_price - stop)

            # APPLY FEES AT ENTRY
            entry_fee = get_fees(ticker, entry_price * position_size, "buy")

            entry_date = df.index[i]

            for j in range(i + 1, len(df)):
                high = df.iloc[j]["High"]
                low = df.iloc[j]["Low"]
                exit_date = df.index[j]
                days_held = (exit_date - entry_date).days

                if low <= stop:
                    exit_price = df.iloc[j]["Close"]
                    pnl = (exit_price - entry_price) * position_size

                    # APPLY SELL FEES
                    sell_fee = get_fees(ticker, exit_price * position_size, "sell")

                    pnl = pnl - entry_fee - sell_fee
                    break

                if high >= target:
                    exit_price = df.iloc[j]["Close"]
                    pnl = (exit_price - entry_price) * position_size

                    sell_fee = get_fees(ticker, exit_price * position_size, "sell")
                    pnl = pnl - entry_fee - sell_fee
                    break

                # time stop
                if days_held >= MAX_HOLD_DAYS:
                    exit_price = df.iloc[j]["Close"]
                    pnl = (exit_price - entry_price) * position_size

                    sell_fee = get_fees(ticker, exit_price * position_size, "sell")
                    pnl = pnl - entry_fee - sell_fee
                    break
            else:
                continue

            daily_trade_count[date] += 1

            trades.append({
                "Ticker": ticker,
                "Entry Date": entry_date,
                "Exit Date": exit_date,
                "Entry": entry_price,
                "Exit": exit_price,
                "P&L": pnl,
                "Return": pnl / risk_amount,
            })

    return trades

# =========================
# RUNNER
# =========================

def run_backtest():
    tickers = pd.read_csv(TICKER_FILE)["Ticker"].dropna().unique()

    all_trades = []
    daily_trade_count = defaultdict(int)

    for ticker in tickers:
        all_trades.extend(backtest_ticker(ticker, daily_trade_count))

    if not all_trades:
        print("No trades found.")
        return

    trades_df = pd.DataFrame(all_trades)
    trades_df.sort_values("Entry Date", inplace=True)

    # EQUITY CURVE
    trades_df["Cumulative P&L"] = trades_df["P&L"].cumsum()
    trades_df["Equity"] = ACCOUNT_SIZE + trades_df["Cumulative P&L"]

    print("\n=== BACKTEST RESULTS ===")
    print(f"Trades: {len(trades_df)}")
    print(f"Win rate: {(trades_df['P&L'] > 0).mean() * 100:.2f}%")
    print(f"Total return: {trades_df['P&L'].sum():.2f}")

    print("\nTop 10 trades:")
    print(trades_df.sort_values("P&L", ascending=False).head(10))

    print("\nWorst 10 trades:")
    print(trades_df.sort_values("P&L").head(10))

    # Plot equity curve
    plt.figure(figsize=(12, 6))
    plt.plot(trades_df["Exit Date"], trades_df["Equity"])
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Equity (£)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_backtest()

