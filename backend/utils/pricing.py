"""
Pricing and Market Data Utilities

This module handles all external data fetching for prices, FX rates, and market regime.
Isolated from FastAPI for testability and reusability.

Functions:
    - get_current_price(): Fetch live stock price from Yahoo Finance
    - get_live_fx_rate(): Fetch GBP/USD exchange rate
    - check_market_regime(): Check SPY/FTSE vs 200-day MA for risk on/off
    - calculate_atr(): Calculate Average True Range for a ticker
"""

import time
import requests
from typing import Optional, Dict


def get_current_price(ticker: str) -> Optional[float]:
    """
    Fetch current price directly from Yahoo Finance API
    
    Args:
        ticker: Stock symbol (e.g., 'NVDA', 'FRES.L')
    
    Returns:
        Current price as float, or None if fetch fails
        
    Notes:
        - Includes 300ms delay to avoid rate limiting
        - Returns price in native currency (USD for US, pence for UK)
        - UK stocks need pence->pounds conversion by caller if needed
    """
    try:
        # Add delay to avoid rate limiting
        time.sleep(0.3)
        
        # Direct Yahoo Finance API call
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "range": "1d"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️  {ticker}: HTTP {response.status_code}")
            return None
        
        data = response.json()
        
        # Extract price from response
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            
            # Try meta.regularMarketPrice first
            if "meta" in result and "regularMarketPrice" in result["meta"]:
                price = float(result["meta"]["regularMarketPrice"])
                if price > 0:
                    print(f"✓ {ticker}: ${price:.2f} (Yahoo API)")
                    return price
            
            # Try latest close price from indicators
            if "indicators" in result and "quote" in result["indicators"]:
                quotes = result["indicators"]["quote"]
                if len(quotes) > 0 and "close" in quotes[0]:
                    closes = [c for c in quotes[0]["close"] if c is not None]
                    if closes:
                        price = float(closes[-1])
                        if price > 0:
                            print(f"✓ {ticker}: ${price:.2f} (Yahoo API - close)")
                            return price
        
        print(f"⚠️  {ticker}: No price in API response")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"❌ {ticker}: Network error - {str(e)}")
        return None
    except Exception as e:
        print(f"❌ {ticker}: Error - {str(e)}")
        return None


def get_live_fx_rate() -> float:
    """
    Fetch live GBP/USD exchange rate from Yahoo Finance
    
    Returns:
        GBP/USD rate as float (e.g., 1.3684)
        Falls back to 1.27 if fetch fails
        
    Notes:
        - Includes 200ms delay to avoid rate limiting
        - Used for converting USD positions to GBP
    """
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
                    print(f"✓ Live FX rate (GBP/USD): {fx_rate:.4f}")
                    return fx_rate
            
            # Try latest close price
            if "indicators" in result and "quote" in result["indicators"]:
                quotes = result["indicators"]["quote"]
                if len(quotes) > 0 and "close" in quotes[0]:
                    closes = [c for c in quotes[0]["close"] if c is not None]
                    if closes:
                        fx_rate = float(closes[-1])
                        if fx_rate > 0:
                            print(f"✓ Live FX rate (GBP/USD): {fx_rate:.4f}")
                            return fx_rate
        
        print(f"⚠️  Could not fetch live FX rate, using default {DEFAULT_FX_RATE}")
        return DEFAULT_FX_RATE
        
    except Exception as e:
        print(f"⚠️  FX rate fetch error: {e}, using default {DEFAULT_FX_RATE}")
        return DEFAULT_FX_RATE


def check_market_regime() -> Dict[str, any]:
    """
    Check SPY and FTSE for risk on/off using 200-day moving average
    
    Returns:
        Dictionary with:
            - spy_risk_on: bool (SPY > 200-day MA)
            - ftse_risk_on: bool (FTSE > 200-day MA)
            - spy_price: float
            - spy_ma200: float
            - ftse_price: float
            - ftse_ma200: float
            
    Notes:
        - Defaults to risk-on if data unavailable
        - Includes 300ms delay to avoid rate limiting
        - Used to determine if positions should be exited
    """
    try:
        time.sleep(0.3)
        
        def get_ma200(ticker: str):
            """Get current price and 200-day MA for a ticker"""
            try:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
                params = {
                    "interval": "1d",
                    "range": "1y"
                }
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=15)
                data = response.json()
                
                if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
                    result = data["chart"]["result"][0]
                    
                    # Get current price
                    current = None
                    if "meta" in result and "regularMarketPrice" in result["meta"]:
                        current = float(result["meta"]["regularMarketPrice"])
                    
                    # Get historical closes for MA200
                    ma200 = None
                    if "indicators" in result and "quote" in result["indicators"]:
                        quotes = result["indicators"]["quote"]
                        if len(quotes) > 0 and "close" in quotes[0]:
                            closes = [c for c in quotes[0]["close"] if c is not None]
                            if len(closes) >= 200:
                                # Calculate 200-day moving average
                                ma200 = sum(closes[-200:]) / 200
                            elif len(closes) > 0:
                                # Use available data if less than 200 days
                                ma200 = sum(closes) / len(closes)
                    
                    return current, ma200
                
                return None, None
            except Exception as e:
                print(f"Error getting MA200 for {ticker}: {e}")
                return None, None
        
        # Get SPY data
        spy_price, spy_ma200 = get_ma200("SPY")
        
        # Get FTSE data
        ftse_price, ftse_ma200 = get_ma200("^FTSE")
        
        # Default to risk-on if we can't fetch data
        if spy_price is None or spy_ma200 is None:
            print("⚠️  Could not fetch SPY data, defaulting to risk-on")
            spy_risk_on = True
            spy_price = 0
            spy_ma200 = 0
        else:
            spy_risk_on = spy_price > spy_ma200
        
        if ftse_price is None or ftse_ma200 is None:
            print("⚠️  Could not fetch FTSE data, defaulting to risk-on")
            ftse_risk_on = True
            ftse_price = 0
            ftse_ma200 = 0
        else:
            ftse_risk_on = ftse_price > ftse_ma200
        
        return {
            'spy_risk_on': spy_risk_on,
            'ftse_risk_on': ftse_risk_on,
            'spy_price': spy_price or 0,
            'spy_ma200': spy_ma200 or 0,
            'ftse_price': ftse_price or 0,
            'ftse_ma200': ftse_ma200 or 0
        }
    except Exception as e:
        print(f"❌ Market regime check failed: {e}")
        return {
            'spy_risk_on': True,
            'ftse_risk_on': True,
            'spy_price': 0,
            'spy_ma200': 0,
            'ftse_price': 0,
            'ftse_ma200': 0
        }


def calculate_atr(ticker: str, period: int = 14) -> Optional[float]:
    """
    Calculate Average True Range (ATR) for a ticker
    
    Args:
        ticker: Stock symbol (e.g., 'NVDA', 'FRES.L')
        period: Number of days for ATR calculation (default: 14)
    
    Returns:
        ATR value as float, or None if calculation fails
        
    Notes:
        - Fetches 1 month of historical data
        - Returns ATR in native currency (USD/GBP/pence)
        - UK stocks (ending in .L) are automatically converted from pence to pounds
        - Used for stop loss calculations
    """
    try:
        # Fetch historical data
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "range": "1mo"  # Need enough data for ATR calculation
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            
            if "indicators" in result and "quote" in result["indicators"]:
                quote = result["indicators"]["quote"][0]
                
                # Get high, low, close
                highs = [h for h in quote.get("high", []) if h is not None]
                lows = [l for l in quote.get("low", []) if l is not None]
                closes = [c for c in quote.get("close", []) if c is not None]
                
                if len(highs) >= period and len(lows) >= period and len(closes) >= period:
                    # Calculate True Range
                    true_ranges = []
                    for i in range(1, len(closes)):
                        high_low = highs[i] - lows[i]
                        high_close = abs(highs[i] - closes[i-1])
                        low_close = abs(lows[i] - closes[i-1])
                        true_range = max(high_low, high_close, low_close)
                        true_ranges.append(true_range)
                    
                    # Calculate ATR (simple moving average of TR)
                    if len(true_ranges) >= period:
                        atr = sum(true_ranges[-period:]) / period
                        
                        # Fix UK stocks: Yahoo returns pence, need to convert to pounds
                        if ticker.endswith('.L') and atr > 100:
                            atr = atr / 100
                            print(f"   📊 Calculated ATR for {ticker}: {atr:.2f} (converted from pence)")
                        else:
                            print(f"   📊 Calculated ATR for {ticker}: {atr:.2f}")
                        
                        return atr
        
        print(f"   ⚠️  Could not calculate ATR for {ticker}")
        return None
        
    except Exception as e:
        print(f"   ❌ ATR calculation error for {ticker}: {e}")
        return None
