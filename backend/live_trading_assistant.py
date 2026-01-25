"""
=====================================================================
LIVE TRADING ASSISTANT - PRODUCTION VERSION
=====================================================================
Generates monthly entry signals with proper error handling and validation.

Dependencies: pandas, numpy, yfinance, requests
=====================================================================
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import json
import os
from typing import Tuple, Dict, Optional
import warnings

warnings.filterwarnings("ignore")
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# =====================================================================
# CONFIGURATION - All parameters in one place
# =====================================================================

BASE_DIR = os.path.dirname(__file__)

class Config:
    """Centralized configuration"""

    # Strategy parameters (from backtest optimization)
    LOOKBACK_DAYS = 252
    TOP_N = 5
    MA_PERIOD = 200
    ATR_PERIOD = 14
    VOLATILITY_WINDOW = 60

    # Risk management
    MIN_POSITION_PCT = 0.05
    MAX_POSITION_PCT = 0.20
    MIN_HOLD_DAYS = 10
    INITIAL_ATR_MULT = 5.0  # Wide stops for new/losing positions
    PROFIT_ATR_MULT = 2.0  # Tight stops for profitable positions

    # Transaction fees (configurable)
    UK_BUY_FEE = 0.005  # 0.5% stamp duty
    UK_SELL_FEE = 0.000  # No stamp duty on sells
    US_BUY_FEE = 0.0015  # 0.15% SEC fee
    US_SELL_FEE = 0.0015  # 0.15% SEC fee

    # Currency
    GBP_PENCE_CONVERSION = 100  # UK stocks quote in pence
    FX_SANITY_MIN = 1.15
    FX_SANITY_MAX = 1.40

    # Files
    UNIVERSE_FILE = os.path.join(BASE_DIR, "tickers_full_list.csv")
    PORTFOLIO_FILE = os.path.join(BASE_DIR, "current_portfolio.json")

    # Defaults
    DEFAULT_CASH = 20000.0
    DEFAULT_FX_RATE = 1.28


# =====================================================================
# EXCHANGE RATE MANAGEMENT
# =====================================================================


class FXManager:
    """Handles currency conversion with proper error handling"""

    def __init__(self):
        self.rate = None

    def fetch_rate(self) -> float:
        """Fetch GBP/USD rate from multiple sources"""

        # Try API sources
        apis = [
            (
                "https://api.exchangerate-api.com/v4/latest/GBP",
                lambda d: d["rates"]["USD"],
            ),
            (
                "https://api.frankfurter.app/latest?from=GBP&to=USD",
                lambda d: d["rates"]["USD"],
            ),
        ]

        for url, extractor in apis:
            try:
                import requests

                print(f"Fetching GBP/USD rate from {url.split('/')[2]}...")
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    rate = extractor(data)

                    if Config.FX_SANITY_MIN < rate < Config.FX_SANITY_MAX:
                        self.rate = rate
                        print(f"✓ Exchange rate: 1 GBP = {self.rate:.4f} USD\n")
                        return rate
                    else:
                        print(
                            f"  Rate {rate:.4f} outside normal range, trying next source..."
                        )

            except ImportError:
                print("⚠️  'requests' library needed: pip install requests")
                break
            except Exception as e:
                print(f"  Failed: {str(e)[:50]}")
                continue

        # Ultimate fallback
        self.rate = Config.DEFAULT_FX_RATE
        print(f"\n⚠️  Using default rate: {self.rate:.4f}")
        print("   Verify current rate for accurate position sizing!\n")
        return self.rate

    def to_gbp(self, amount_usd: float) -> float:
        """Convert USD to GBP"""
        if self.rate is None:
            self.fetch_rate()
        return amount_usd / self.rate

    def to_usd(self, amount_gbp: float) -> float:
        """Convert GBP to USD"""
        if self.rate is None:
            self.fetch_rate()
        return amount_gbp * self.rate


# =====================================================================
# DATA UTILITIES
# =====================================================================


def download_prices_safe(
    tickers: list, 
    start_date: str, 
    chunk_size: int = 50
) -> pd.DataFrame:
    """Download adjusted CLOSE prices for many tickers with robust error handling"""

    print(f"Downloading {len(tickers)} tickers in chunks of {chunk_size}...\n")

    all_chunks = []
    failed_tickers = []

    for i in range(0, len(tickers), chunk_size):
        chunk = tickers[i : i + chunk_size]

        try:
            data = yf.download(
                tickers=chunk,
                start=start_date,
                auto_adjust=True,
                progress=False,
                group_by="ticker",
            )

            # Normalize data structure
            if len(chunk) == 1:
                ticker = chunk[0]

                if isinstance(data, pd.DataFrame) and "Close" in data.columns:
                    close = data[["Close"]].rename(columns={"Close": ticker})
                elif isinstance(data, pd.Series):
                    close = data.to_frame(name=ticker)
                else:
                    print(f"  ⚠️  Unexpected data format for {ticker}, skipping")
                    failed_tickers.append(ticker)
                    continue

            else:
                if isinstance(data.columns, pd.MultiIndex):
                    levels = data.columns.names

                    close_level = None
                    for lvl in range(len(levels)):
                        if "Close" in data.columns.get_level_values(lvl):
                            close_level = lvl
                            break

                    if close_level is None:
                        print("  ⚠️  No Close level found, skipping chunk")
                        failed_tickers.extend(chunk)
                        continue

                    close = data.xs("Close", axis=1, level=close_level)

                elif "Close" in data.columns:
                    close = data[["Close"]].copy()
                    close.columns = chunk
                else:
                    print("  ⚠️  Unexpected non-MultiIndex format, skipping chunk")
                    failed_tickers.extend(chunk)
                    continue

            # Drop tickers with no valid data
            close = close.dropna(axis=1, how="all")

            if close.empty:
                failed_tickers.extend(chunk)
            else:
                all_chunks.append(close)

        except Exception as e:
            print(f"  ⚠️  Failed chunk {i//chunk_size+1}: {str(e)[:60]}")
            failed_tickers.extend(chunk)
            continue

    if not all_chunks:
        raise ValueError("❌ No price data downloaded for any tickers.")

    prices = pd.concat(all_chunks, axis=1).sort_index()
    prices = prices.loc[:, ~prices.columns.duplicated()]
    prices = prices.ffill(limit=5)

    print(f"✓ Successfully downloaded {prices.shape[1]} tickers.")

    if failed_tickers:
        print(f"⚠️  Failed tickers ({len(failed_tickers)}): {failed_tickers}\n")

    return prices


def compute_atr_proper(prices: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Calculate ATR using close-to-close approximation"""
    close_to_close = prices.diff().abs()
    atr = close_to_close.rolling(window=period, min_periods=period).mean()
    return atr


def calculate_volatility(prices: pd.DataFrame, window: int = 60) -> pd.Series:
    """Calculate annualized volatility"""
    returns = prices.pct_change()
    volatility = returns.rolling(window=window, min_periods=window).std()
    volatility = volatility.replace(0, np.nan)
    return volatility.iloc[-1]


def transaction_fee(ticker: str, side: str) -> float:
    """Calculate transaction fee for a trade"""
    is_uk = ticker.endswith(".L")

    if is_uk:
        return Config.UK_BUY_FEE if side == "buy" else Config.UK_SELL_FEE
    else:
        return Config.US_BUY_FEE if side == "buy" else Config.US_SELL_FEE


# =====================================================================
# PORTFOLIO MANAGEMENT
# =====================================================================


def load_portfolio() -> dict:
    """Load portfolio with validation"""
    if os.path.exists(Config.PORTFOLIO_FILE):
        try:
            with open(Config.PORTFOLIO_FILE, "r") as f:
                portfolio = json.load(f)

            if "cash" not in portfolio:
                portfolio["cash"] = Config.DEFAULT_CASH
            if "positions" not in portfolio:
                portfolio["positions"] = {}

            return portfolio
        except Exception as e:
            print(f"⚠️  Error loading portfolio: {e}")
            print("   Creating new portfolio...")

    return {"cash": Config.DEFAULT_CASH, "positions": {}}


def save_portfolio(portfolio: dict):
    """Save portfolio safely"""
    try:
        with open(Config.PORTFOLIO_FILE, "w") as f:
            json.dump(portfolio, f, indent=2)
        print(f"\n✓ Portfolio saved to {Config.PORTFOLIO_FILE}")
    except Exception as e:
        print(f"❌ Failed to save portfolio: {e}")


# =====================================================================
# SIGNAL GENERATION
# =====================================================================


def generate_signals(
    as_of_date: Optional[datetime] = None, fx_manager: FXManager = None
) -> Tuple[pd.DataFrame, datetime]:
    """Generate buy signals with comprehensive error handling"""

    if as_of_date is None:
        as_of_date = datetime.now()
    else:
        as_of_date = pd.to_datetime(as_of_date)

    if fx_manager is None:
        fx_manager = FXManager()

    print("=" * 70)
    print(f"GENERATING SIGNALS FOR: {as_of_date.strftime('%Y-%m-%d')}")
    print("=" * 70 + "\n")

    fx_manager.fetch_rate()

    # Load universe
    try:
        df = pd.read_csv(Config.UNIVERSE_FILE)
        tickers = df["Ticker"].dropna().unique().tolist()
        print(f"Universe: {len(tickers)} tickers\n")
    except Exception as e:
        raise FileNotFoundError(f"Cannot load universe file: {e}")

    # Download data
    start_date = (as_of_date - timedelta(days=Config.LOOKBACK_DAYS + 300)).strftime("%Y-%m-%d")

    try:
        prices = download_prices_safe(tickers, start_date)
        prices = prices.dropna(axis=1, thresh=Config.LOOKBACK_DAYS)
        prices = prices.loc[:as_of_date]
    except Exception as e:
        raise RuntimeError(f"Failed to download prices: {e}")

    print(f"Valid tickers: {prices.shape[1]}\n")

    # Download indices
    print("Downloading market indices...")
    try:
        spy = yf.download("SPY", start=start_date, auto_adjust=True, progress=False)["Close"]
        ftse = yf.download("^FTSE", start=start_date, auto_adjust=True, progress=False)["Close"]

        if isinstance(spy, pd.DataFrame):
            spy = spy.iloc[:, 0]
        if isinstance(ftse, pd.DataFrame):
            ftse = ftse.iloc[:, 0]

    except Exception as e:
        raise RuntimeError(f"Failed to download indices: {e}")

    # Calculate regime
    spy_ma200 = spy.rolling(Config.MA_PERIOD).mean()
    ftse_ma200 = ftse.rolling(Config.MA_PERIOD).mean()

    latest_date = prices.index[-1]

    try:
        latest_spy = spy.loc[:latest_date].iloc[-1]
        latest_spy_ma = spy_ma200.loc[:latest_date].iloc[-1]
        latest_ftse = ftse.loc[:latest_date].iloc[-1]
        latest_ftse_ma = ftse_ma200.loc[:latest_date].iloc[-1]
    except Exception as e:
        print(f"⚠️  Date alignment issue, using approximate match: {e}")
        latest_spy = spy.iloc[-1]
        latest_spy_ma = spy_ma200.iloc[-1]
        latest_ftse = ftse.iloc[-1]
        latest_ftse_ma = ftse_ma200.iloc[-1]

    print(f"\nMarket conditions ({latest_date.strftime('%Y-%m-%d')}):")
    print(f"  SPY: ${latest_spy:.2f} vs MA200 ${latest_spy_ma:.2f} - {'🟢 RISK ON' if latest_spy > latest_spy_ma else '🔴 RISK OFF'}")
    print(f"  FTSE: {latest_ftse:.2f} pts vs MA200 {latest_ftse_ma:.2f} pts - {'🟢 RISK ON' if latest_ftse > latest_ftse_ma else '🔴 RISK OFF'}\n")

    # Calculate signals
    print("Calculating momentum...")
    momentum = prices.pct_change(Config.LOOKBACK_DAYS)
    ranks = momentum.rank(axis=1, ascending=False, na_option="bottom", method="first")

    ma200 = prices.rolling(Config.MA_PERIOD).mean()
    trend = prices > ma200

    latest_momentum = momentum.iloc[-1]
    latest_ranks = ranks.iloc[-1]
    latest_trend = trend.iloc[-1]
    latest_prices = prices.iloc[-1]

    atr = compute_atr_proper(prices, Config.ATR_PERIOD)
    latest_atr = atr.iloc[-1]

    volatility = calculate_volatility(prices, Config.VOLATILITY_WINDOW)

    # Generate signals
    signals = []

    for ticker in prices.columns:
        if pd.isna(latest_trend[ticker]) or pd.isna(latest_ranks[ticker]):
            continue

        spy_on = latest_spy > latest_spy_ma
        ftse_on = latest_ftse > latest_ftse_ma
        ticker_risk_on = ftse_on if ticker.endswith(".L") else spy_on

        if (
            latest_trend[ticker]
            and latest_ranks[ticker] <= Config.TOP_N
            and ticker_risk_on
        ):

            native_price = latest_prices[ticker]
            native_atr = latest_atr[ticker]

            if pd.isna(native_atr):
                print(f"  ⚠️  Skipping {ticker}: No ATR data")
                continue

            # Convert to GBP
            if ticker.endswith(".L"):
                price_gbp = native_price / Config.GBP_PENCE_CONVERSION
                atr_gbp = native_atr / Config.GBP_PENCE_CONVERSION
                currency = "GBP"
                display_price = price_gbp
            else:
                price_gbp = fx_manager.to_gbp(native_price)
                atr_gbp = fx_manager.to_gbp(native_atr)
                currency = "USD"
                display_price = native_price

            vol = volatility[ticker]
            if pd.isna(vol) or vol == 0:
                print(f"  ⚠️  Skipping {ticker}: Invalid volatility")
                continue

            signals.append(
                {
                    "Ticker": ticker,
                    "Rank": int(latest_ranks[ticker]),
                    "Momentum %": round(latest_momentum[ticker] * 100, 2),
                    "Price (Native)": round(display_price, 2),
                    "Price (GBP)": round(price_gbp, 2),
                    "ATR (GBP)": round(atr_gbp, 4),
                    "Volatility": round(vol, 6),
                    "Currency": currency,
                    "Market": "UK" if ticker.endswith(".L") else "US",
                }
            )

    if not signals:
        print("\n⚠️  No qualifying signals found")
        return pd.DataFrame(), latest_date

    signals_df = pd.DataFrame(signals).sort_values("Rank")
    print(f"✓ Found {len(signals_df)} qualifying stocks\n")

    return signals_df, latest_date


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("MOMENTUM STRATEGY - SIGNAL GENERATOR")
    print("=" * 70 + "\n")

    try:
        fx = FXManager()
        portfolio = load_portfolio()

        print(f"Portfolio: £{portfolio['cash']:,.2f} cash, {len(portfolio['positions'])} positions\n")

        signals_df, date = generate_signals(fx_manager=fx)

        if len(signals_df) > 0:
            signals_df.to_csv(f"signals_{date.strftime('%Y%m%d')}.csv", index=False)
            print(f"\n✓ Saved to signals_{date.strftime('%Y%m%d')}.csv")
        else:
            print("⚠️  No signals generated")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)
    print("END")
    print("=" * 70)