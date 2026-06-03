"""
Signal Service

Business logic for momentum signal generation including:
- Momentum signal generation from price data
- Signal retrieval and filtering
- Signal status updates
- Signal deletion

All functions are independent of FastAPI for maximum testability.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd

from database import (
    get_portfolio,
    get_positions,
    get_settings,
    create_signal,
    get_signals as db_get_signals,
    update_signal as db_update_signal,
    delete_signal as db_delete_signal,
    get_all_tickers,
    download_ticker_data,
    compute_atr_simple
)

from utils.pricing import get_live_fx_rate
from utils.formatting import decimal_to_float


def generate_momentum_signals(
    lookback_days: int = 252,
    top_n: int = 5,
    ma_period: int = 200,
    atr_period: int = 14,
    volatility_window: int = 60,
    min_position_pct: float = 0.05,
    max_position_pct: float = 0.20
) -> Dict:
    """
    Generate momentum signals based on current portfolio state
    
    Args:
        lookback_days: Momentum calculation period (default 252 = 1 year)
        top_n: Number of top momentum stocks to signal (default 5)
        ma_period: Moving average period for trend filter (default 200)
        atr_period: ATR calculation period (default 14)
        volatility_window: Volatility calculation window (default 60)
        min_position_pct: Minimum position size as % of cash (default 5%)
        max_position_pct: Maximum position size as % of cash (default 20%)
    
    Returns:
        Dictionary with:
            - signals_generated: Total number of signals
            - new_signals: Number of new signals (not already held)
            - already_held: Number of signals for stocks already in portfolio
            - signal_date: Signal generation date
            - fx_rate: GBP/USD rate used
            - available_cash: Cash available for new positions
            - market_regime: SPY and FTSE risk status
            - signals: List of signal dictionaries
    
    Raises:
        ValueError: If portfolio not found or price data unavailable
    
    Note:
        - Only generates signals in risk-on market conditions
        - Filters by 200-day MA trend (price > MA200)
        - Calculates position sizing based on available cash
        - Saves signals to database for later review
    """
    print("\n" + "="*70)
    print("🎯 GENERATING MOMENTUM SIGNALS")
    print("="*70)
    
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    available_cash = float(portfolio['cash'])
    
    # Get open positions to check for already-held stocks
    open_positions = get_positions(portfolio_id, status='open')
    held_tickers = set([pos['ticker'] for pos in open_positions])
    
    print(f"Portfolio cash: £{available_cash:,.2f}")
    print(f"Open positions: {len(open_positions)}")
    print(f"Held tickers: {held_tickers}\n")
    
    # Get settings
    settings_list = get_settings()
    settings = settings_list[0] if settings_list else None
    
    # Load universe
    tickers = get_all_tickers()
    
    print(f"Universe: {len(tickers)} tickers")
    
    # Calculate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=lookback_days + 300)
    
    signal_date_str = end_date.strftime('%Y-%m-%d')
    
    # Download prices for all tickers
    print("Downloading price data...\n")

    prices_dict = {}
    # Store full DataFrames (close + high + volume) for supplementary indicators (ST-09)
    full_data_dict = {}
    failed = []

    for ticker in tickers:
        df_price = download_ticker_data(
            ticker,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        if df_price is not None and len(df_price) >= lookback_days:
            prices_dict[ticker] = df_price['close']
            full_data_dict[ticker] = df_price
        else:
            failed.append(ticker)

    if not prices_dict:
        raise ValueError("Failed to download price data")

    prices = pd.DataFrame(prices_dict)
    prices = prices.ffill(limit=5)
    
    print(f"✓ Downloaded {len(prices.columns)} tickers")
    if failed:
        print(f"⚠️  Failed: {len(failed)} tickers\n")
    
    # Get live FX rate
    live_fx_rate = get_live_fx_rate()
    
    # Download market indices
    print("Checking market regime...")
    spy_data = download_ticker_data(
        "SPY", 
        start_date.strftime('%Y-%m-%d'), 
        end_date.strftime('%Y-%m-%d')
    )
    ftse_data = download_ticker_data(
        "^FTSE", 
        start_date.strftime('%Y-%m-%d'), 
        end_date.strftime('%Y-%m-%d')
    )
    
    # Benchmark momentum for relative_strength_pct (ST-09 supplementary indicator)
    spy_benchmark_momentum = None
    ftse_benchmark_momentum = None

    if spy_data is None or ftse_data is None:
        print("⚠️  Market data unavailable, assuming risk-on\n")
        spy_risk_on = True
        ftse_risk_on = True
    else:
        spy_close = spy_data['close']
        ftse_close = ftse_data['close']

        spy_ma200 = spy_close.rolling(ma_period).mean()
        ftse_ma200 = ftse_close.rolling(ma_period).mean()

        spy_risk_on = spy_close.iloc[-1] > spy_ma200.iloc[-1]
        ftse_risk_on = ftse_close.iloc[-1] > ftse_ma200.iloc[-1]

        # Benchmark momentum over same lookback_days (for relative_strength_pct)
        spy_mom_series = spy_close.pct_change(lookback_days)
        if len(spy_mom_series) > 0 and not pd.isna(spy_mom_series.iloc[-1]):
            spy_benchmark_momentum = spy_mom_series.iloc[-1]

        ftse_mom_series = ftse_close.pct_change(lookback_days)
        if len(ftse_mom_series) > 0 and not pd.isna(ftse_mom_series.iloc[-1]):
            ftse_benchmark_momentum = ftse_mom_series.iloc[-1]
    
    print(f"SPY: {'🟢 Risk On' if spy_risk_on else '🔴 Risk Off'}")
    print(f"FTSE: {'🟢 Risk On' if ftse_risk_on else '🔴 Risk Off'}\n")
    
    # Calculate momentum
    print("Calculating momentum...")
    momentum = prices.pct_change(lookback_days, fill_method=None)
    
    # Calculate MA200 trend
    ma200 = prices.rolling(ma_period).mean()
    trend = prices > ma200
    
    # Get latest values
    latest_momentum = momentum.iloc[-1]
    latest_trend = trend.iloc[-1]
    latest_prices = prices.iloc[-1]
    
    # Calculate ATR for all tickers
    print("Calculating ATR...")
    atr_dict = {}
    for ticker in prices.columns:
        atr = compute_atr_simple(prices[ticker], atr_period)
        if len(atr) > 0 and not pd.isna(atr.iloc[-1]):
            atr_dict[ticker] = atr.iloc[-1]
    
    # Calculate volatility
    print("Calculating volatility...")
    volatility_dict = {}
    for ticker in prices.columns:
        returns = prices[ticker].pct_change()
        vol = returns.rolling(volatility_window).std()
        if len(vol) > 0 and not pd.isna(vol.iloc[-1]):
            volatility_dict[ticker] = vol.iloc[-1]

    # ST-09: Pre-compute 50-day MA for price_vs_50d_ma supplementary indicator
    ma50 = prices.rolling(50).mean()

    # Rank stocks by momentum
    ranks = latest_momentum.rank(ascending=False, method='first')
    
    # Generate signals
    print("\nGenerating signals...\n")
    signals = []
    
    for ticker in prices.columns:
        # Check trend and rank
        if pd.isna(latest_trend[ticker]) or not latest_trend[ticker]:
            continue
        
        if pd.isna(ranks[ticker]) or ranks[ticker] > top_n:
            continue
        
        # Check market regime
        is_uk = ticker.endswith('.L')
        market_risk_on = ftse_risk_on if is_uk else spy_risk_on
        
        if not market_risk_on:
            continue
        
        # Get price and ATR
        native_price = latest_prices[ticker]
        native_atr = atr_dict.get(ticker)
        
        if pd.isna(native_atr) or native_atr == 0:
            continue
        
        # Convert to GBP
        if is_uk:
            # UK prices in pence, convert to pounds
            price_gbp = native_price / 100
            atr_gbp = native_atr / 100
            price_display = price_gbp
            currency = "GBP"
            market = "UK"
        else:
            # US prices in USD
            price_gbp = native_price / live_fx_rate
            atr_gbp = native_atr / live_fx_rate
            price_display = native_price
            currency = "USD"
            market = "US"
        
        # Get volatility
        vol = volatility_dict.get(ticker, 0)
        if pd.isna(vol) or vol == 0:
            continue
        
        # Check if already held
        status = 'already_held' if ticker in held_tickers else 'new'

        # -------------------------------------------------------------------
        # ST-09 supplementary indicators (display-only, do not affect rank)
        # -------------------------------------------------------------------

        # 1. relative_strength_pct: stock momentum vs benchmark (informational)
        benchmark_mom = spy_benchmark_momentum if market == 'US' else ftse_benchmark_momentum
        stock_mom = latest_momentum[ticker]
        if benchmark_mom is not None and not pd.isna(stock_mom) and not pd.isna(benchmark_mom):
            relative_strength_pct = round((stock_mom - benchmark_mom) * 100, 2)
        else:
            relative_strength_pct = None

        # 2. week52_high_proximity_pct: how far below the 52-week high (native price)
        full_df = full_data_dict.get(ticker)
        if full_df is not None and 'high' in full_df.columns and len(full_df) >= 252:
            week52_high = full_df['high'].iloc[-252:].max()
            if week52_high and week52_high > 0:
                week52_high_proximity_pct = round(
                    (native_price - float(week52_high)) / float(week52_high) * 100, 2
                )
            else:
                week52_high_proximity_pct = None
        else:
            week52_high_proximity_pct = None

        # 3. avg_daily_volume_20d: average daily volume over last 20 trading days
        if full_df is not None and 'volume' in full_df.columns and len(full_df) >= 20:
            recent_vol_series = full_df['volume'].iloc[-20:].dropna()
            avg_daily_volume_20d = (
                int(recent_vol_series.mean()) if len(recent_vol_series) > 0 else None
            )
        else:
            avg_daily_volume_20d = None

        # 4. price_vs_50d_ma: % deviation from 50-day moving average (native price)
        ma50_val = ma50[ticker].iloc[-1] if ticker in ma50.columns else None
        if ma50_val is not None and not pd.isna(ma50_val) and float(ma50_val) > 0:
            price_vs_50d_ma = round((native_price - float(ma50_val)) / float(ma50_val) * 100, 2)
        else:
            price_vs_50d_ma = None

        signals.append({
            'ticker': ticker,
            'market': market,
            'rank': int(ranks[ticker]),
            'momentum_percent': round(latest_momentum[ticker] * 100, 2),
            'current_price': round(price_display, 2),
            'price_gbp': round(price_gbp, 2),
            'atr_value': round(atr_gbp, 4),
            'volatility': round(vol, 6),
            'initial_stop': round(
                price_display - (5 * (atr_gbp if currency == 'GBP' else native_atr)),
                2
            ),
            'status': status,
            # ST-09 supplementary indicators — display-only, no effect on rank
            'relative_strength_pct': relative_strength_pct,
            'week52_high_proximity_pct': week52_high_proximity_pct,
            'avg_daily_volume_20d': avg_daily_volume_20d,
            'price_vs_50d_ma': price_vs_50d_ma,
        })
    
    if not signals:
        print("⚠️  No qualifying signals found\n")
        return {
            "signals_generated": 0,
            "new_signals": 0,
            "already_held": 0,
            "signal_date": signal_date_str,
            "fx_rate": live_fx_rate,
            "available_cash": available_cash,
            "market_regime": {
                "spy_risk_on": spy_risk_on,
                "ftse_risk_on": ftse_risk_on
            },
            "signals": []
        }
    
    # Sort by rank
    signals_sorted = sorted(signals, key=lambda x: x['rank'])
    
    # Calculate position sizing (equal weight)
    available_for_new = available_cash
    new_signals = [s for s in signals_sorted if s['status'] == 'new']
    
    if new_signals:
        allocation_per_stock = available_for_new / len(new_signals)
        
        # Clamp to min/max
        min_allocation = available_for_new * min_position_pct
        max_allocation = available_for_new * max_position_pct
        allocation_per_stock = max(min_allocation, min(max_allocation, allocation_per_stock))
    
    # Add position sizing to signals
    for signal in signals_sorted:
        if signal['status'] == 'new':
            signal['allocation_gbp'] = round(allocation_per_stock, 2)
            signal['suggested_shares'] = int(allocation_per_stock / signal['price_gbp'])

            # ST-06 (BLG-FEAT-43): flag signals where price exceeds allocation
            if signal['suggested_shares'] == 0:
                signal['status'] = 'allocation_insufficient'
                signal['reason'] = (
                    f"1 share (£{signal['price_gbp']:,.0f}) exceeds position allocation "
                    f"(£{allocation_per_stock:,.0f}) — cannot size"
                )
            else:
                signal['reason'] = None

            # Calculate fees
            if signal['market'] == 'UK':
                fee_rate = 0.005  # 0.5% stamp duty
            else:
                fee_rate = 0.0015  # 0.15% FX fee

            gross_cost = signal['suggested_shares'] * signal['price_gbp']
            fees = gross_cost * fee_rate
            signal['total_cost'] = round(gross_cost + fees, 2)
        else:
            # Already held - no allocation
            signal['allocation_gbp'] = 0
            signal['suggested_shares'] = 0
            signal['total_cost'] = 0
            signal['reason'] = None
    
    # Save to database
    print(f"Saving {len(signals_sorted)} signals to database...")
    
    for signal_data in signals_sorted:
        signal_data['portfolio_id'] = portfolio_id
        signal_data['signal_date'] = signal_date_str
        create_signal(portfolio_id, signal_data)
    
    print(f"✓ Saved {len(signals_sorted)} signals\n")
    print("="*70 + "\n")
    
    return {
        "signals_generated": len(signals_sorted),
        "new_signals": len(new_signals),
        "already_held": len([s for s in signals_sorted if s['status'] == 'already_held']),
        "signal_date": signal_date_str,
        "fx_rate": live_fx_rate,
        "available_cash": available_cash,
        "market_regime": {
            "spy_risk_on": spy_risk_on,
            "ftse_risk_on": ftse_risk_on
        },
        "signals": [decimal_to_float(s) for s in signals_sorted]
    }


def get_signals(status: Optional[str] = None) -> List[Dict]:
    """
    Get all signals, optionally filtered by status
    
    Args:
        status: Optional status filter - "new", "entered", "dismissed", 
               "expired", "already_held" (None = all signals)
    
    Returns:
        List of signal dictionaries with:
            - ticker: Stock symbol
            - market: US or UK
            - rank: Momentum rank
            - momentum_percent: Momentum return %
            - current_price: Current price (native currency)
            - atr_value: ATR value
            - suggested_shares: Recommended position size
            - status: Signal status
            - signal_date: When signal was generated
    
    Raises:
        ValueError: If portfolio not found
    
    Note:
        - Returns empty list if no signals exist
        - Signals are sorted by rank (best first)
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")
    
    portfolio_id = str(portfolio['id'])
    signals = db_get_signals(portfolio_id, status)
    
    formatted = [decimal_to_float(s) for s in signals]
    
    print(f"✓ Retrieved {len(formatted)} signal(s)")
    if status:
        print(f"   Filtered by status: {status}")
    print()
    
    return formatted


def update_signal_status(signal_id: str, updates: Dict) -> Dict:
    """
    Update a signal (typically to change status)
    
    Args:
        signal_id: UUID of signal to update
        updates: Dictionary of fields to update (e.g., {"status": "entered"})
    
    Returns:
        Updated signal dictionary
    
    Raises:
        ValueError: If signal not found
    
    Note:
        - Common status transitions:
          - "new" → "entered" (position opened)
          - "new" → "dismissed" (user skipped)
          - "new" → "expired" (signal too old)
    """
    updated = db_update_signal(signal_id, updates)
    
    print(f"✓ Signal {signal_id} updated:")
    for key, value in updates.items():
        print(f"   {key}: {value}")
    print()
    
    return decimal_to_float(updated)


def delete_signal(signal_id: str) -> None:
    """
    Delete a signal
    
    Args:
        signal_id: UUID of signal to delete
    
    Raises:
        ValueError: If signal not found
    
    Note:
        - Permanently removes signal from database
        - Cannot be undone
        - Typically used to clean up old/stale signals
    """
    db_delete_signal(signal_id)
    
    print(f"✓ Signal {signal_id} deleted\n")
