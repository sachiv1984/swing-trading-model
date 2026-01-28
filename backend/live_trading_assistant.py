"""
=====================================================================
LIVE TRADING ASSISTANT - PRODUCTION VERSION (Updated)
=====================================================================
Generates monthly entry signals with proper error handling and validation.
Uses Yahoo Finance API directly for better reliability.

Dependencies: pandas, numpy, requests
=====================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import time
import requests
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
# YAHOO FINANCE API - Direct API calls
# =====================================================================

def get_live_fx_rate():
    """Fetch live GBP/USD exchange rate from Yahoo Finance"""
    try:
        time.sleep(0.2)
        
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GBPUSD=X"
        params = {
            "interval": "1d",
            "range": "1d"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            
            # Try meta.regularMarketPrice first
            if "meta" in result and "regularMarketPrice" in result["meta"]:
                fx_rate = float(result["meta"]["regularMarketPrice"])
                if fx_rate > 0:
                    print(f"✓ Live FX rate (GBP/USD): {fx_rate:.4f}\n")
                    return fx_rate
            
            # Try latest close price
            if "indicators" in result and "quote" in result["indicators"]:
                quotes = result["indicators"]["quote"]
                if len(quotes) > 0 and "close" in quotes[0]:
                    closes = [c for c in quotes[0]["close"] if c is not None]
                    if closes:
                        fx_rate = float(closes[-1])
                        if fx_rate > 0:
                            print(f"✓ Live FX rate (GBP/USD): {fx_rate:.4f}\n")
                            return fx_rate
        
        print("⚠️  Could not fetch live FX rate, using default 1.28\n")
        return 1.28
        
    except Exception as e:
        print(f"⚠️  FX rate fetch error: {e}, using default 1.28\n")
        return 1.28


def download_ticker_data(ticker: str, start_date: str, end_date: str = None):
    """Download historical data for a single ticker using Yahoo API"""
    try:
        time.sleep(0.1)  # Rate limiting
        
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Convert dates to timestamps
        start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
        end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
        
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "period1": start_ts,
            "period2": end_ts
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            
            # Get timestamps
            if "timestamp" not in result:
                return None
                
            timestamps = result["timestamp"]
            dates = [datetime.fromtimestamp(ts) for ts in timestamps]
            
            # Get price data
            if "indicators" not in result or "quote" not in result["indicators"]:
                return None
                
            quote = result["indicators"]["quote"][0]
            
            # Use adjusted close if available, otherwise close
            if "adjclose" in result["indicators"] and result["indicators"]["adjclose"]:
                closes = result["indicators"]["adjclose"][0]["adjclose"]
            else:
                closes = quote.get("close", [])
            
            highs = quote.get("high", [])
            lows = quote.get("low", [])
            
            # Create DataFrame
            df = pd.DataFrame({
                'date': dates,
                'close': closes,
                'high': highs,
                'low': lows
            })
            
            # Remove None values
            df = df.dropna()
            
            if len(df) < 50:  # Minimum data requirement
                return None
            
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            
            return df
            
        return None
        
    except Exception as e:
        print(f"  ⚠️  Error fetching {ticker}: {str(e)[:50]}")
        return None


def download_prices_batch(tickers: list, start_date: str, end_date: str = None):
    """Download prices for multiple tickers"""
    
    print(f"Downloading {len(tickers)} tickers...\n")
    
    all_prices = {}
    failed = []
    
    for i, ticker in enumerate(tickers, 1):
        if i % 10 == 0:
            print(f"  Progress: {i}/{len(tickers)}")
        
        df = download_ticker_data(ticker, start_date, end_date)
        
        if df is not None:
            all_prices[ticker] = df['close']
        else:
            failed.append(ticker)
    
    if not all_prices:
        raise ValueError("❌ No price data downloaded for any tickers.")
    
    # Combine into single DataFrame
    prices_df = pd.DataFrame(all_prices)
    prices_df = prices_df.sort_index()
    prices_df = prices_df.fillna(method='ffill', limit=5)
    
    print(f"\n✓ Successfully downloaded {len(all_prices)} tickers")
    
    if failed:
        print(f"⚠️  Failed tickers ({len(failed)}): {failed[:10]}{'...' if len(failed) > 10 else ''}\n")
    
    return prices_df


# =====================================================================
# TECHNICAL INDICATORS
# =====================================================================

def compute_atr(ticker_data: pd.DataFrame, period: int = 14):
    """Calculate ATR from high/low/close data"""
    if 'high' not in ticker_data.columns or 'low' not in ticker_data.columns:
        # Fallback: use close-to-close
        close_to_close = ticker_data['close'].diff().abs()
        atr = close_to_close.rolling(window=period, min_periods=period).mean()
        return atr
    
    high = ticker_data['high']
    low = ticker_data['low']
    close = ticker_data['close']
    
    # True Range calculation
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period, min_periods=period).mean()
    
    return atr


def compute_atr_simple(prices: pd.Series, period: int = 14):
    """Calculate ATR using close-to-close approximation (simpler)"""
    close_to_close = prices.diff().abs()
    atr = close_to_close.rolling(window=period, min_periods=period).mean()
    return atr


def calculate_volatility(prices: pd.Series, window: int = 60):
    """Calculate annualized volatility"""
    returns = prices.pct_change()
    volatility = returns.rolling(window=window, min_periods=window).std()
    return volatility


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

def generate_signals(as_of_date: Optional[datetime] = None):
    """Generate buy signals with comprehensive error handling"""

    if as_of_date is None:
        as_of_date = datetime.now()
    else:
        as_of_date = pd.to_datetime(as_of_date)

    print("=" * 70)
    print(f"GENERATING SIGNALS FOR: {as_of_date.strftime('%Y-%m-%d')}")
    print("=" * 70 + "\n")

    # Get live FX rate
    fx_rate = get_live_fx_rate()

    # Load universe
    try:
        df = pd.read_csv(Config.UNIVERSE_FILE)
        tickers = df["Ticker"].dropna().unique().tolist()
        print(f"Universe: {len(tickers)} tickers\n")
    except Exception as e:
        raise FileNotFoundError(f"Cannot load universe file: {e}")

    # Download data
    start_date = (as_of_date - timedelta(days=Config.LOOKBACK_DAYS + 300)).strftime("%Y-%m-%d")
    end_date = as_of_date.strftime("%Y-%m-%d")

    try:
        prices = download_prices_batch(tickers, start_date, end_date)
        prices = prices.dropna(axis=1, thresh=Config.LOOKBACK_DAYS)
        prices = prices.loc[:as_of_date]
    except Exception as e:
        raise RuntimeError(f"Failed to download prices: {e}")

    print(f"Valid tickers: {prices.shape[1]}\n")

    # Download indices
    print("Downloading market indices...")
    
    spy_data = download_ticker_data("SPY", start_date, end_date)
    ftse_data = download_ticker_data("^FTSE", start_date, end_date)
    
    if spy_data is None or ftse_data is None:
        raise RuntimeError("Failed to download market indices")
    
    spy = spy_data['close']
    ftse = ftse_data['close']

    # Calculate regime
    spy_ma200 = spy.rolling(Config.MA_PERIOD).mean()
    ftse_ma200 = ftse.rolling(Config.MA_PERIOD).mean()

    latest_date = prices.index[-1]

    try:
        latest_spy = spy.loc[:latest_date].iloc[-1]
        latest_spy_ma = spy_ma200.loc[:latest_date].iloc[-1]
        latest_ftse = ftse.loc[:latest_date].iloc[-1]
        latest_ftse_ma = ftse_ma200.loc[:latest_date].iloc[-1]
    except Exception:
        latest_spy = spy.iloc[-1]
        latest_spy_ma = spy_ma200.iloc[-1]
        latest_ftse = ftse.iloc[-1]
        latest_ftse_ma = ftse_ma200.iloc[-1]

    spy_risk_on = latest_spy > latest_spy_ma
    ftse_risk_on = latest_ftse > latest_ftse_ma

    print(f"\nMarket conditions ({latest_date.strftime('%Y-%m-%d')}):")
    print(f"  SPY: ${latest_spy:.2f} vs MA200 ${latest_spy_ma:.2f} - {'🟢 RISK ON' if spy_risk_on else '🔴 RISK OFF'}")
    print(f"  FTSE: {latest_ftse:.2f} pts vs MA200 {latest_ftse_ma:.2f} pts - {'🟢 RISK ON' if ftse_risk_on else '🔴 RISK OFF'}\n")

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

    # Calculate ATR for all tickers (simple version)
    print("Calculating ATR...")
    atr_dict = {}
    for ticker in prices.columns:
        atr = compute_atr_simple(prices[ticker], Config.ATR_PERIOD)
        if len(atr) > 0:
            atr_dict[ticker] = atr.iloc[-1]
    
    # Calculate volatility
    print("Calculating volatility...")
    volatility_dict = {}
    for ticker in prices.columns:
        vol = calculate_volatility(prices[ticker], Config.VOLATILITY_WINDOW)
        if len(vol) > 0:
            volatility_dict[ticker] = vol.iloc[-1]

    # Generate signals
    print("\nGenerating signals...\n")
    signals = []

    for ticker in prices.columns:
        if pd.isna(latest_trend[ticker]) or pd.isna(latest_ranks[ticker]):
            continue

        # Check market regime
        ticker_risk_on = ftse_risk_on if ticker.endswith(".L") else spy_risk_on

        if (
            latest_trend[ticker]
            and latest_ranks[ticker] <= Config.TOP_N
            and ticker_risk_on
        ):

            native_price = latest_prices[ticker]
            native_atr = atr_dict.get(ticker)

            if pd.isna(native_atr) or native_atr == 0:
                continue

            # Convert to GBP
            if ticker.endswith(".L"):
                price_gbp = native_price / Config.GBP_PENCE_CONVERSION
                atr_gbp = native_atr / Config.GBP_PENCE_CONVERSION
                currency = "GBP"
                display_price = price_gbp
            else:
                price_gbp = native_price / fx_rate
                atr_gbp = native_atr / fx_rate
                currency = "USD"
                display_price = native_price

            vol = volatility_dict.get(ticker, 0)
            if pd.isna(vol) or vol == 0:
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
                    "Initial Stop": round(display_price - (Config.INITIAL_ATR_MULT * (atr_gbp if currency == "GBP" else native_atr)), 2)
                }
            )

    if not signals:
        print("\n⚠️  No qualifying signals found")
        return pd.DataFrame(), latest_date, fx_rate

    signals_df = pd.DataFrame(signals).sort_values("Rank")
    print(f"✓ Found {len(signals_df)} qualifying stocks\n")

    return signals_df, latest_date, fx_rate


def print_signals_summary(signals_df: pd.DataFrame, fx_rate: float):
    """Pretty print signals for easy review"""
    
    print("\n" + "=" * 70)
    print("MONTHLY ENTRY SIGNALS - SUMMARY")
    print("=" * 70 + "\n")
    
    print(f"FX Rate: 1 GBP = {fx_rate:.4f} USD\n")
    
    if len(signals_df) == 0:
        print("No signals generated.\n")
        return
    
    # Separate by market
    us_signals = signals_df[signals_df['Market'] == 'US']
    uk_signals = signals_df[signals_df['Market'] == 'UK']
    
    if len(us_signals) > 0:
        print("🇺🇸 US MARKET SIGNALS:")
        print("-" * 70)
        for _, row in us_signals.iterrows():
            print(f"\n{row['Rank']}. {row['Ticker']}")
            print(f"   Price: ${row['Price (Native)']:.2f} (£{row['Price (GBP)']:.2f})")
            print(f"   Momentum: {row['Momentum %']:+.1f}%")
            print(f"   ATR: £{row['ATR (GBP)']:.4f}")
            print(f"   Initial Stop: ${row['Initial Stop']:.2f}")
            print(f"   Volatility: {row['Volatility']:.4f}")
    
    if len(uk_signals) > 0:
        print("\n\n🇬🇧 UK MARKET SIGNALS:")
        print("-" * 70)
        for _, row in uk_signals.iterrows():
            print(f"\n{row['Rank']}. {row['Ticker'].replace('.L', '')}")
            print(f"   Price: £{row['Price (Native)']:.2f}")
            print(f"   Momentum: {row['Momentum %']:+.1f}%")
            print(f"   ATR: £{row['ATR (GBP)']:.4f}")
            print(f"   Initial Stop: £{row['Initial Stop']:.2f}")
            print(f"   Volatility: {row['Volatility']:.4f}")
    
    print("\n" + "=" * 70)


def calculate_position_sizes(signals_df: pd.DataFrame, available_cash: float):
    """Calculate suggested position sizes using equal weighting"""
    
    if len(signals_df) == 0:
        return signals_df
    
    # Equal weight allocation
    num_positions = len(signals_df)
    allocation_per_stock = available_cash / num_positions
    
    # Clamp to min/max position size
    min_allocation = available_cash * Config.MIN_POSITION_PCT
    max_allocation = available_cash * Config.MAX_POSITION_PCT
    
    allocation_per_stock = max(min_allocation, min(max_allocation, allocation_per_stock))
    
    # Calculate shares
    signals_df['Allocation (GBP)'] = allocation_per_stock
    signals_df['Suggested Shares'] = (allocation_per_stock / signals_df['Price (GBP)']).astype(int)
    signals_df['Actual Cost (GBP)'] = signals_df['Suggested Shares'] * signals_df['Price (GBP)']
    
    # Add fees
    signals_df['Fees (GBP)'] = signals_df.apply(
        lambda row: row['Actual Cost (GBP)'] * (Config.UK_BUY_FEE if row['Market'] == 'UK' else Config.US_BUY_FEE),
        axis=1
    )
    
    signals_df['Total Cost (GBP)'] = signals_df['Actual Cost (GBP)'] + signals_df['Fees (GBP)']
    
    return signals_df


def print_position_sizing(signals_df: pd.DataFrame):
    """Print position sizing recommendations"""
    
    if len(signals_df) == 0:
        return
    
    print("\n" + "=" * 70)
    print("POSITION SIZING RECOMMENDATIONS")
    print("=" * 70 + "\n")
    
    total_cost = signals_df['Total Cost (GBP)'].sum()
    
    print(f"Total Capital Required: £{total_cost:,.2f}\n")
    
    for _, row in signals_df.iterrows():
        ticker_display = row['Ticker'].replace('.L', '') if row['Market'] == 'UK' else row['Ticker']
        print(f"{ticker_display}:")
        print(f"  Buy {row['Suggested Shares']} shares @ {'$' if row['Market'] == 'US' else '£'}{row['Price (Native)']:.2f}")
        print(f"  Cost: £{row['Actual Cost (GBP)']:.2f} + Fees: £{row['Fees (GBP)']:.2f} = Total: £{row['Total Cost (GBP)']:.2f}\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("MOMENTUM STRATEGY - SIGNAL GENERATOR")
    print("=" * 70 + "\n")

    try:
        portfolio = load_portfolio()
        available_cash = portfolio['cash']

        print(f"Portfolio: £{available_cash:,.2f} cash, {len(portfolio['positions'])} open positions\n")

        # Generate signals
        signals_df, date, fx_rate = generate_signals()

        if len(signals_df) > 0:
            # Print summary
            print_signals_summary(signals_df, fx_rate)
            
            # Calculate position sizes
            signals_df = calculate_position_sizes(signals_df, available_cash)
            
            # Print position sizing
            print_position_sizing(signals_df)
            
            # Save to CSV
            filename = f"signals_{date.strftime('%Y%m%d')}.csv"
            signals_df.to_csv(filename, index=False)
            print(f"\n✓ Signals saved to {filename}")
        else:
            print("\n⚠️  No signals generated")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)
    print("END")
    print("=" * 70)
