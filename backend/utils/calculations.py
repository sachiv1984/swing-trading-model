"""
Calculation Utilities

Business logic for fees, P&L, and stop loss calculations.
All calculations isolated for testability and reusability.
"""

from typing import Dict, Tuple, Optional
from datetime import datetime


# ============================================================================
# FEE CALCULATIONS
# ============================================================================

def calculate_uk_entry_fees(gross_cost: float, settings: Dict) -> Dict[str, float]:
    """
    Calculate UK position entry fees
    
    Args:
        gross_cost: Gross cost in GBP (shares × price)
        settings: Settings dict with uk_commission and stamp_duty_rate
    
    Returns:
        Dictionary with:
            - commission: Fixed commission (£9.95)
            - stamp_duty: 0.5% of gross cost
            - total: Total fees
    
    Example:
        >>> calculate_uk_entry_fees(1000, {'uk_commission': 9.95, 'stamp_duty_rate': 0.005})
        {'commission': 9.95, 'stamp_duty': 5.0, 'total': 14.95}
    """
    commission = float(settings.get('uk_commission', 9.95))
    stamp_duty_rate = float(settings.get('stamp_duty_rate', 0.005))
    stamp_duty = gross_cost * stamp_duty_rate
    
    return {
        'commission': commission,
        'stamp_duty': stamp_duty,
        'fx_fee': 0,
        'total': commission + stamp_duty
    }


def calculate_us_entry_fees(gross_cost_usd: float, settings: Dict) -> Dict[str, float]:
    """
    Calculate US position entry fees
    
    Args:
        gross_cost_usd: Gross cost in USD (shares × price)
        settings: Settings dict with us_commission and fx_fee_rate
    
    Returns:
        Dictionary with:
            - commission: US commission (usually £0)
            - stamp_duty: Always 0 for US
            - fx_fee: 0.15% of gross cost
            - total: Total fees in USD
    
    Example:
        >>> calculate_us_entry_fees(1000, {'us_commission': 0, 'fx_fee_rate': 0.0015})
        {'commission': 0, 'stamp_duty': 0, 'fx_fee': 1.5, 'total': 1.5}
    """
    commission = float(settings.get('us_commission', 0.00))
    fx_fee_rate = float(settings.get('fx_fee_rate', 0.0015))
    fx_fee = gross_cost_usd * fx_fee_rate
    
    return {
        'commission': commission,
        'stamp_duty': 0,
        'fx_fee': fx_fee,
        'total': commission + fx_fee
    }


def calculate_uk_exit_fees(gross_proceeds: float, settings: Dict) -> Dict[str, float]:
    """
    Calculate UK position exit fees
    
    Args:
        gross_proceeds: Gross proceeds in GBP
        settings: Settings dict with uk_commission
    
    Returns:
        Dictionary with:
            - commission: Fixed commission (£9.95)
            - stamp_duty: Always 0 on sales
            - total: Total fees
    
    Note:
        No stamp duty on sales, only on purchases
    """
    commission = float(settings.get('uk_commission', 9.95))
    
    return {
        'commission': commission,
        'stamp_duty': 0,
        'fx_fee': 0,
        'total': commission
    }


def calculate_us_exit_fees(gross_proceeds_usd: float, settings: Dict) -> Dict[str, float]:
    """
    Calculate US position exit fees
    
    Args:
        gross_proceeds_usd: Gross proceeds in USD
        settings: Settings dict with us_commission and fx_fee_rate
    
    Returns:
        Dictionary with:
            - commission: US commission (usually £0)
            - stamp_duty: Always 0
            - fx_fee: 0.15% of gross proceeds
            - total: Total fees in USD
    """
    commission = float(settings.get('us_commission', 0.00))
    fx_fee_rate = float(settings.get('fx_fee_rate', 0.0015))
    fx_fee = gross_proceeds_usd * fx_fee_rate
    
    return {
        'commission': commission,
        'stamp_duty': 0,
        'fx_fee': fx_fee,
        'total': commission + fx_fee
    }


# ============================================================================
# P&L CALCULATIONS
# ============================================================================

def calculate_position_pnl(
    entry_price: float,
    current_price: float,
    shares: float,
    market: str,
    live_fx_rate: float
) -> Tuple[float, float, float]:
    """
    Calculate position P&L in both native currency and GBP
    
    Args:
        entry_price: Entry price in native currency
        current_price: Current price in native currency
        shares: Number of shares (can be fractional)
        market: "US" or "UK"
        live_fx_rate: Current GBP/USD rate (ignored for UK)
    
    Returns:
        Tuple of (pnl_native, pnl_gbp, pnl_pct):
            - pnl_native: P&L in native currency (USD or GBP)
            - pnl_gbp: P&L in GBP
            - pnl_pct: P&L percentage
    
    Example:
        >>> calculate_position_pnl(100, 110, 10, "UK", 1.37)
        (100.0, 100.0, 10.0)
        
        >>> calculate_position_pnl(100, 110, 10, "US", 1.37)
        (100.0, 72.99, 10.0)
    """
    # Calculate P&L in native currency
    pnl_native = (current_price - entry_price) * shares
    
    # Convert to GBP if needed
    if market == 'US':
        pnl_gbp = pnl_native / live_fx_rate
    else:
        pnl_gbp = pnl_native
    
    # Calculate percentage
    pnl_pct = ((current_price - entry_price) / entry_price) * 100 if entry_price > 0 else 0
    
    return pnl_native, pnl_gbp, pnl_pct


def calculate_exit_proceeds(
    exit_price: float,
    shares: float,
    market: str,
    exit_fx_rate: float,
    settings: Dict
) -> Dict[str, float]:
    """
    Calculate exit proceeds and fees
    
    Args:
        exit_price: Exit price in native currency
        shares: Number of shares to exit
        market: "US" or "UK"
        exit_fx_rate: GBP/USD rate at exit (ignored for UK)
        settings: Settings dict with fee rates
    
    Returns:
        Dictionary with:
            - gross_proceeds_native: Gross proceeds in native currency
            - gross_proceeds_gbp: Gross proceeds in GBP
            - exit_fees_native: Fees in native currency
            - exit_fees_gbp: Fees in GBP
            - net_proceeds_native: Net proceeds in native currency
            - net_proceeds_gbp: Net proceeds in GBP
            - fee_breakdown: Dict with commission, stamp_duty, fx_fee
    """
    # Gross proceeds in native currency
    gross_proceeds_native = exit_price * shares
    
    # Calculate fees based on market
    if market == 'UK':
        fee_breakdown = calculate_uk_exit_fees(gross_proceeds_native, settings)
        exit_fees_native = fee_breakdown['total']
        
        # UK: already in GBP
        gross_proceeds_gbp = gross_proceeds_native
        exit_fees_gbp = exit_fees_native
    else:
        fee_breakdown = calculate_us_exit_fees(gross_proceeds_native, settings)
        exit_fees_native = fee_breakdown['total']
        
        # US: convert to GBP using exit FX rate
        gross_proceeds_gbp = gross_proceeds_native / exit_fx_rate
        exit_fees_gbp = exit_fees_native / exit_fx_rate
    
    # Net proceeds
    net_proceeds_native = gross_proceeds_native - exit_fees_native
    net_proceeds_gbp = gross_proceeds_gbp - exit_fees_gbp
    
    return {
        'gross_proceeds_native': gross_proceeds_native,
        'gross_proceeds_gbp': gross_proceeds_gbp,
        'exit_fees_native': exit_fees_native,
        'exit_fees_gbp': exit_fees_gbp,
        'net_proceeds_native': net_proceeds_native,
        'net_proceeds_gbp': net_proceeds_gbp,
        'fee_breakdown': fee_breakdown
    }


def calculate_realized_pnl(
    net_proceeds_gbp: float,
    total_cost: float,
    shares_exited: float,
    total_shares: float
) -> Tuple[float, float]:
    """
    Calculate realized P&L for position exit
    
    Args:
        net_proceeds_gbp: Net proceeds from exit in GBP
        total_cost: Total cost of full position in GBP
        shares_exited: Number of shares being exited
        total_shares: Total shares in position
    
    Returns:
        Tuple of (realized_pnl_gbp, realized_pnl_pct):
            - realized_pnl_gbp: Realized P&L in GBP
            - realized_pnl_pct: Realized P&L percentage
    
    Example:
        >>> calculate_realized_pnl(1100, 1000, 10, 10)
        (100.0, 10.0)
        
        >>> calculate_realized_pnl(550, 1000, 5, 10)  # Partial exit
        (50.0, 10.0)
    """
    # Calculate proportional cost
    cost_per_share = total_cost / total_shares
    exit_total_cost = cost_per_share * shares_exited
    
    # Calculate P&L
    realized_pnl_gbp = net_proceeds_gbp - exit_total_cost
    realized_pnl_pct = (realized_pnl_gbp / exit_total_cost) * 100 if exit_total_cost > 0 else 0
    
    return realized_pnl_gbp, realized_pnl_pct


def calculate_portfolio_pnl(
    total_value: float,
    net_deposits: float,
    net_withdrawals: float
) -> float:
    """
    Calculate true portfolio P&L accounting for cash flows
    
    Args:
        total_value: Current total portfolio value (cash + positions)
        net_deposits: Total deposits
        net_withdrawals: Total withdrawals
    
    Returns:
        True portfolio P&L in GBP
    
    Formula:
        P&L = Total Value - (Deposits - Withdrawals)
    
    Example:
        >>> calculate_portfolio_pnl(5500, 5000, 0)
        500.0
        
        >>> calculate_portfolio_pnl(5500, 5000, 200)  # Withdrew £200
        700.0
    """
    net_cash_flow = net_deposits - net_withdrawals
    return total_value - net_cash_flow


# ============================================================================
# STOP LOSS CALCULATIONS
# ============================================================================

def calculate_initial_stop(entry_price: float, atr: float, multiplier: float = 5.0) -> float:
    """
    Calculate initial stop loss for new position
    
    Args:
        entry_price: Entry price in native currency
        atr: Average True Range in native currency
        multiplier: ATR multiplier (default 5.0 for wide initial stop)
    
    Returns:
        Initial stop price in native currency
    
    Example:
        >>> calculate_initial_stop(100, 5, 5.0)
        75.0
    """
    return entry_price - (multiplier * atr)


def calculate_trailing_stop(
    current_price: float,
    atr: float,
    is_profitable: bool,
    current_stop: float,
    entry_price: float,
    settings: Dict
) -> Tuple[float, str, float]:
    """
    Calculate trailing stop based on profitability
    
    Args:
        current_price: Current price in native currency
        atr: Average True Range in native currency
        is_profitable: True if position has unrealized profit
        current_stop: Current stop level in native currency
        entry_price: Entry price in native currency
        settings: Settings dict with atr_multiplier_trailing and atr_multiplier_initial
    
    Returns:
        Tuple of (new_stop, reason, atr_multiplier):
            - new_stop: New stop price (only moves up, never down)
            - reason: Explanation of stop calculation
            - atr_multiplier: Multiplier used (2 or 5)
    
    Strategy:
        - Profitable positions: Tight 2×ATR stop, never below entry
        - Losing positions: Wide 5×ATR stop, can be below entry
        - Stops only trail upward, never downward
    
    Example:
        >>> calculate_trailing_stop(110, 5, True, 100, 100, {'atr_multiplier_trailing': 2})
        (100.0, 'Profitable (tight 2x ATR)', 2.0)
        
        >>> calculate_trailing_stop(90, 5, False, 60, 100, {'atr_multiplier_initial': 5})
        (65.0, 'At loss (wide 5x ATR)', 5.0)
    """
    # Determine ATR multiplier based on profitability
    if is_profitable:
        atr_mult = float(settings.get('atr_multiplier_trailing', 2.0))
        reason = f"Profitable (tight {atr_mult}x ATR)"
    else:
        atr_mult = float(settings.get('atr_multiplier_initial', 5.0))
        reason = f"At loss (wide {atr_mult}x ATR)"
    
    # Calculate new stop: current price - (multiplier × ATR)
    new_stop = current_price - (atr_mult * atr)
    
    # Trailing logic based on profitability
    if is_profitable:
        # Profitable: Never go below entry (protect gains)
        trailing_stop = max(current_stop, new_stop, entry_price)
    else:
        # Losing: Allow wide stop, can be below entry (room to recover)
        trailing_stop = max(current_stop, new_stop)
    
    return trailing_stop, reason, atr_mult


def should_exit_position(
    current_price: float,
    stop_price: float,
    holding_days: int,
    market_risk_on: bool,
    grace_period_days: int = 10
) -> Tuple[bool, Optional[str]]:
    """
    Determine if position should be exited
    
    Args:
        current_price: Current price in native currency
        stop_price: Stop loss price in native currency
        holding_days: Days held
        market_risk_on: True if market regime is risk-on
        grace_period_days: Grace period before stops are active (default 10)
    
    Returns:
        Tuple of (should_exit, exit_reason):
            - should_exit: True if position should be exited
            - exit_reason: Reason for exit, or None if holding
    
    Exit Conditions:
        1. Market risk-off → EXIT (regardless of grace period or stop)
        2. After grace period AND price <= stop → EXIT
        3. Otherwise → HOLD
    
    Example:
        >>> should_exit_position(95, 100, 15, True)
        (True, 'Stop Loss Hit')
        
        >>> should_exit_position(95, 100, 5, True)
        (False, None)  # Grace period
        
        >>> should_exit_position(105, 100, 15, False)
        (True, 'Risk-Off Signal')
    """
    # Check market regime first (overrides everything)
    if not market_risk_on:
        return True, "Risk-Off Signal"
    
    # Check grace period
    in_grace_period = holding_days < grace_period_days
    if in_grace_period:
        return False, None
    
    # Check stop loss
    if current_price <= stop_price:
        return True, "Stop Loss Hit"
    
    # Hold position
    return False, None


def calculate_holding_days(entry_date: str, exit_date: Optional[str] = None) -> int:
    """
    Calculate days held between entry and exit
    
    Args:
        entry_date: Entry date as string (YYYY-MM-DD)
        exit_date: Exit date as string (YYYY-MM-DD), or None for today
    
    Returns:
        Number of days held
    
    Example:
        >>> calculate_holding_days('2026-01-01', '2026-01-11')
        10
        
        >>> calculate_holding_days('2026-01-01')  # Uses today
        # Returns days from 2026-01-01 to today
    """
    entry = datetime.strptime(entry_date, '%Y-%m-%d')
    
    if exit_date:
        exit = datetime.strptime(exit_date, '%Y-%m-%d')
    else:
        exit = datetime.now()
    
    return (exit - entry).days


# ============================================================================
# POSITION SIZING (Future use)
# ============================================================================

def calculate_position_size(
    portfolio_value: float,
    risk_pct: float,
    entry_price: float,
    stop_price: float
) -> Tuple[float, float]:
    """
    Calculate optimal position size based on risk
    
    Args:
        portfolio_value: Total portfolio value in GBP
        risk_pct: Risk per trade as percentage (e.g., 2.0 for 2%)
        entry_price: Entry price in native currency
        stop_price: Stop loss price in native currency
    
    Returns:
        Tuple of (shares, risk_amount):
            - shares: Optimal number of shares
            - risk_amount: Amount risked in GBP
    
    Formula:
        Risk Amount = Portfolio Value × Risk %
        Stop Distance = Entry Price - Stop Price
        Shares = Risk Amount / Stop Distance
    
    Example:
        >>> calculate_position_size(10000, 2.0, 100, 95)
        (40.0, 200.0)
    
    Note:
        This function is for future use. Not currently used in position entry.
    """
    risk_amount = portfolio_value * (risk_pct / 100)
    stop_distance = entry_price - stop_price
    
    if stop_distance <= 0:
        return 0, 0
    
    shares = risk_amount / stop_distance
    
    return shares, risk_amount
