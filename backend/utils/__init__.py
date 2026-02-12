"""
Utils Package

Utility functions isolated from FastAPI for testability and reusability.

Modules:
    - pricing: Stock prices, FX rates, market regime, ATR calculations
    - formatting: Data formatting and type conversion helpers
    - calculations: Fee, P&L, and stop loss calculations
"""

from .pricing import (
    get_current_price,
    get_live_fx_rate,
    check_market_regime,
    calculate_atr
)

from .formatting import (
    decimal_to_float
)

from .calculations import (
    # Fee calculations
    calculate_uk_entry_fees,
    calculate_us_entry_fees,
    calculate_uk_exit_fees,
    calculate_us_exit_fees,
    # P&L calculations
    calculate_position_pnl,
    calculate_exit_proceeds,
    calculate_realized_pnl,
    calculate_portfolio_pnl,
    # Stop loss calculations
    calculate_initial_stop,
    calculate_trailing_stop,
    should_exit_position,
    calculate_holding_days,
    # Position sizing (future use)
    calculate_position_size
)

__all__ = [
    # Pricing
    'get_current_price',
    'get_live_fx_rate',
    'check_market_regime',
    'calculate_atr',
    # Formatting
    'decimal_to_float',
    # Fee calculations
    'calculate_uk_entry_fees',
    'calculate_us_entry_fees',
    'calculate_uk_exit_fees',
    'calculate_us_exit_fees',
    # P&L calculations
    'calculate_position_pnl',
    'calculate_exit_proceeds',
    'calculate_realized_pnl',
    'calculate_portfolio_pnl',
    # Stop loss calculations
    'calculate_initial_stop',
    'calculate_trailing_stop',
    'should_exit_position',
    'calculate_holding_days',
    # Position sizing
    'calculate_position_size'
]
