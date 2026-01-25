"""
=====================================================================
POSITION MANAGER - PHASE 2: DAILY MONITORING
=====================================================================
Run this DAILY to get:
- Current stop loss levels for each position
- Which positions to exit (stop hit or risk-off)
- Updated portfolio status
=====================================================================
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import json
import os

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# =====================================================================
# CONFIGURATION
# =====================================================================

BASE_DIR = os.path.dirname(__file__)

PARAMS = {
    'min_hold_days': 10,
    'initial_atr_mult': 5,  # Wide stops for new/losing positions
    'profit_atr_mult': 2,   # Tight stops when profitable
    'atr_period': 14
}

PORTFOLIO_FILE = os.path.join(BASE_DIR, "current_portfolio.json")

# =====================================================================
# HELPER FUNCTIONS
# =====================================================================

def load_portfolio():
    """Load current portfolio"""
    if not os.path.exists(PORTFOLIO_FILE):
        print(f"❌ Portfolio file not found: {PORTFOLIO_FILE}")
        return None
    
    with open(PORTFOLIO_FILE, 'r') as f:
        return json.load(f)

def save_portfolio(portfolio):
    """Save updated portfolio"""
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=2, default=str)
    print(f"\n✓ Portfolio updated and saved")

def get_current_prices_and_atr(tickers):
    """Download current prices and ATR for all positions"""
    
    start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    data = yf.download(tickers, start=start, auto_adjust=True, progress=False)
    
    if isinstance(data, pd.Series):
        data = data.to_frame()
        data.columns = [tickers[0]]
    
    prices = data["Close"] if "Close" in data else data
    
    # Calculate ATR
    high = prices.copy()
    low = prices.copy()
    close = prices.copy()
    
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    
    if isinstance(tr1, pd.Series):
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    else:
        tr = pd.concat([tr1, tr2, tr3], axis=1)
        tr.columns = pd.MultiIndex.from_tuples([(c, "tr") for c in tr.columns])
        tr = tr.T.groupby(level=0).max().T
    
    atr = tr.rolling(PARAMS['atr_period']).mean()
    
    # Get latest values
    latest_prices = prices.iloc[-1]
    latest_atr = atr.iloc[-1]
    latest_date = prices.index[-1]
    
    return latest_prices, latest_atr, latest_date

def check_market_regime():
    """Check if market is risk-on or risk-off"""

    def _close_series(download_df):
        """Extract Close prices as a clean Series"""
        close = download_df["Close"]

        if isinstance(close, pd.DataFrame):
            close = close.squeeze("columns")

        close = pd.to_numeric(close, errors="coerce").dropna()

        if not isinstance(close, pd.Series):
            close = pd.Series(close).dropna()

        return close

    def _last_float(x):
        """Convert to Python float"""
        if isinstance(x, pd.Series):
            x = x.iloc[-1]
        return float(x)

    start = (datetime.now() - timedelta(days=250)).strftime('%Y-%m-%d')

    spy_df = yf.download("SPY", start=start, auto_adjust=True, progress=False)
    ftse_df = yf.download("^FTSE", start=start, auto_adjust=True, progress=False)

    spy = _close_series(spy_df)
    ftse = _close_series(ftse_df)

    spy_ma200_series = spy.rolling(200, min_periods=200).mean()
    ftse_ma200_series = ftse.rolling(200, min_periods=200).mean()

    spy_current = _last_float(spy.iloc[-1]) if len(spy) else np.nan
    ftse_current = _last_float(ftse.iloc[-1]) if len(ftse) else np.nan

    spy_ma200 = _last_float(spy_ma200_series.iloc[-1]) if len(spy_ma200_series.dropna()) else np.nan
    ftse_ma200 = _last_float(ftse_ma200_series.iloc[-1]) if len(ftse_ma200_series.dropna()) else np.nan

    spy_risk_on = bool(np.isfinite(spy_current) and np.isfinite(spy_ma200) and (spy_current > spy_ma200))
    ftse_risk_on = bool(np.isfinite(ftse_current) and np.isfinite(ftse_ma200) and (ftse_current > ftse_ma200))

    asof_date = spy.index[-1] if len(spy) else datetime.now()

    return {
        'spy_risk_on': spy_risk_on,
        'ftse_risk_on': ftse_risk_on,
        'spy_price': spy_current,
        'spy_ma200': spy_ma200,
        'ftse_price': ftse_current,
        'ftse_ma200': ftse_ma200,
        'date': asof_date
    }

def is_risk_on(ticker, market_status):
    """Check if specific ticker's market is risk-on"""
    if ticker.endswith(".L"):
        return market_status['ftse_risk_on']
    return market_status['spy_risk_on']

# =====================================================================
# POSITION ANALYSIS
# =====================================================================

def analyze_positions(portfolio, current_prices, current_atr, market_status):
    """
    Analyze all positions and determine actions
    
    Returns:
    - actions: List of recommended actions (HOLD, EXIT)
    - updated_positions: Updated position data
    """
    
    print("\n" + "=" * 70)
    print("📊 POSITION ANALYSIS")
    print("=" * 70)
    
    if len(portfolio['positions']) == 0:
        print("\n✓ No open positions")
        return [], {}, 0, 0
    
    today = datetime.now().date()
    actions = []
    updated_positions = {}
    
    total_value = 0
    total_pnl = 0
    
    print(f"\nAnalyzing {len(portfolio['positions'])} positions as of {market_status['date'].strftime('%Y-%m-%d')}...")
    
    for ticker, pos in portfolio['positions'].items():
        
        # Get position data
        entry_date = pd.to_datetime(pos['entry_date']).date()
        entry_price = pos['entry_price']
        shares = pos['shares']
        current_stop = pos.get('current_stop', pos.get('initial_stop'))
        
        # Get current market data
        if ticker not in current_prices:
            print(f"\n⚠️  {ticker}: Could not get current price")
            continue
        
        current_price = current_prices[ticker]
        current_atr_val = current_atr[ticker] if ticker in current_atr.index else 0
        
        # Calculate metrics
        holding_days = (today - entry_date).days
        current_value = shares * current_price
        total_value += current_value
        
        pnl = (current_price - entry_price) * shares
        pnl_pct = ((current_price - entry_price) / entry_price) * 100
        total_pnl += pnl
        
        is_profitable = pnl > 0
        
        # Determine appropriate ATR multiplier
        grace_period_active = holding_days < PARAMS['min_hold_days']
        
        if grace_period_active:
            active_atr_mult = PARAMS['initial_atr_mult']
            stop_reason = f"Grace period ({holding_days}/{PARAMS['min_hold_days']} days)"
        elif is_profitable:
            active_atr_mult = PARAMS['profit_atr_mult']
            stop_reason = f"Profitable (tight {PARAMS['profit_atr_mult']}x ATR)"
        else:
            active_atr_mult = PARAMS['initial_atr_mult']
            stop_reason = f"At loss (wide {PARAMS['initial_atr_mult']}x ATR)"
        
        # Calculate new stop (trailing - only moves up)
        new_stop = current_price - (active_atr_mult * current_atr_val)
        trailing_stop = max(current_stop, new_stop)
        
        # Check exit conditions
        action = "HOLD"
        exit_reason = None
        
        # 1. Stop loss hit (only after grace period)
        if not grace_period_active and current_price <= trailing_stop:
            action = "EXIT"
            exit_reason = "Stop Loss Hit"
        
        # 2. Risk-off (can exit any time)
        elif not is_risk_on(ticker, market_status):
            action = "EXIT"
            exit_reason = "Risk-Off Signal"
        
        # Store action
        actions.append({
            'ticker': ticker,
            'action': action,
            'exit_reason': exit_reason,
            'holding_days': holding_days,
            'entry_price': entry_price,
            'current_price': current_price,
            'shares': shares,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'current_stop': trailing_stop,
            'grace_period': grace_period_active,
            'stop_reason': stop_reason,
            'current_value': current_value
        })
        
        # Update position data
        if action == "HOLD":
            updated_positions[ticker] = {
                'entry_date': pos['entry_date'],
                'entry_price': entry_price,
                'shares': shares,
                'initial_stop': pos.get('initial_stop'),
                'current_stop': trailing_stop,
                'current_price': float(current_price),
                'holding_days': holding_days,
                'pnl': float(pnl),
                'pnl_pct': float(pnl_pct),
                'market': pos.get('market', 'UK' if ticker.endswith('.L') else 'US')
            }
    
    return actions, updated_positions, total_value, total_pnl

def print_position_summary(actions, portfolio, total_value, total_pnl, market_status):
    """Print detailed position summary"""
    
    print("\n" + "=" * 70)
    print("💼 PORTFOLIO SUMMARY")
    print("=" * 70)
    
    cash = portfolio['cash']
    total_portfolio = cash + total_value
    
    print(f"\nPortfolio Value: £{total_portfolio:,.2f}")
    print(f"  Cash: £{cash:,.2f} ({cash/total_portfolio*100:.1f}%)")
    print(f"  Positions: £{total_value:,.2f} ({total_value/total_portfolio*100:.1f}%)")
    print(f"  Total P&L: £{total_pnl:,.2f} ({total_pnl/20000*100:+.1f}%)")
    
    print(f"\nMarket Status ({market_status['date'].strftime('%Y-%m-%d')}):")
    print(f"  SPY: {'🟢 RISK ON' if market_status['spy_risk_on'] else '🔴 RISK OFF'} "
          f"({market_status['spy_price']:.2f} vs MA200 {market_status['spy_ma200']:.2f})")
    print(f"  FTSE: {'🟢 RISK ON' if market_status['ftse_risk_on'] else '🔴 RISK OFF'} "
          f"({market_status['ftse_price']:.2f} vs MA200 {market_status['ftse_ma200']:.2f})")
    
    print("\n" + "=" * 70)
    print("📍 POSITION DETAILS")
    print("=" * 70)
    
    holds = [a for a in actions if a['action'] == 'HOLD']
    exits = [a for a in actions if a['action'] == 'EXIT']
    
    if holds:
        print(f"\n✅ HOLDING ({len(holds)} positions):")
        print("-" * 70)
        
        for pos in holds:
            status = "🆕" if pos['grace_period'] else ("📈" if pos['pnl'] > 0 else "📉")
            
            print(f"\n{status} {pos['ticker']}")
            print(f"   Entry: £{pos['entry_price']:.2f} | Current: £{pos['current_price']:.2f} | "
                  f"P&L: £{pos['pnl']:+,.2f} ({pos['pnl_pct']:+.1f}%)")
            print(f"   Shares: {int(pos['shares'])} | Value: £{pos['current_value']:,.2f}")
            print(f"   Days held: {pos['holding_days']}")
            print(f"   Current stop: £{pos['current_stop']:.2f} ({pos['stop_reason']})")
    
    if exits:
        print(f"\n\n❌ EXIT SIGNALS ({len(exits)} positions):")
        print("-" * 70)
        
        for pos in exits:
            print(f"\n🚨 {pos['ticker']} - {pos['exit_reason']}")
            print(f"   Entry: £{pos['entry_price']:.2f} | Current: £{pos['current_price']:.2f}")
            print(f"   Exit P&L: £{pos['pnl']:+,.2f} ({pos['pnl_pct']:+.1f}%)")
            print(f"   Days held: {pos['holding_days']}")

def update_portfolio_with_actions(portfolio, updated_positions, actions, execute_exits=False):
    """Update portfolio based on actions"""
    
    exits = [a for a in actions if a['action'] == 'EXIT']
    
    if execute_exits and exits:
        print("\n" + "=" * 70)
        print("EXECUTING EXITS")
        print("=" * 70)
        
        for pos in exits:
            ticker = pos['ticker']
            proceeds = pos['shares'] * pos['current_price']
            
            # Add back to cash (approximate - doesn't account for sell fees)
            portfolio['cash'] += proceeds
            
            # Record trade
            if 'trade_history' not in portfolio:
                portfolio['trade_history'] = []
            
            portfolio['trade_history'].append({
                'ticker': ticker,
                'entry_date': portfolio['positions'][ticker]['entry_date'],
                'exit_date': datetime.now().strftime('%Y-%m-%d'),
                'entry_price': pos['entry_price'],
                'exit_price': pos['current_price'],
                'shares': pos['shares'],
                'pnl': pos['pnl'],
                'pnl_pct': pos['pnl_pct'],
                'holding_days': pos['holding_days'],
                'exit_reason': pos['exit_reason']
            })
            
            print(f"✓ Exited {ticker}: {pos['pnl_pct']:+.1f}% | £{pos['pnl']:+,.2f}")
    
    # Update positions
    portfolio['positions'] = updated_positions
    portfolio['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return portfolio

# =====================================================================
# MAIN EXECUTION
# =====================================================================

if __name__ == "__main__":
    
    print("\n" + "=" * 70)
    print("POSITION MANAGER - DAILY MONITORING")
    print("=" * 70)
    
    # Load portfolio
    portfolio = load_portfolio()
    if portfolio is None:
        exit(1)
    
    if len(portfolio['positions']) == 0:
        print("\n✓ No open positions to manage")
        exit(0)
    
    # Get current market data
    print("\nFetching current prices and market conditions...")
    tickers = list(portfolio['positions'].keys())
    
    try:
        current_prices, current_atr, latest_date = get_current_prices_and_atr(tickers)
        market_status = check_market_regime()
        
        # Analyze positions
        actions, updated_positions, total_value, total_pnl = analyze_positions(
            portfolio, current_prices, current_atr, market_status
        )
        
        # Print summary
        print_position_summary(actions, portfolio, total_value, total_pnl, market_status)
        
        # Update portfolio
        portfolio = update_portfolio_with_actions(
            portfolio, updated_positions, actions, execute_exits=False
        )
        save_portfolio(portfolio)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("END OF POSITION MANAGEMENT")
    print("=" * 70)