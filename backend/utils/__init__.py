"""
Utils Package

Utility functions isolated from FastAPI for testability and reusability.

Modules:
    - pricing: Stock prices, FX rates, market regime, ATR calculations
    - formatting: Data formatting and type conversion helpers
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

__all__ = [
    # Pricing
    'get_current_price',
    'get_live_fx_rate',
    'check_market_regime',
    'calculate_atr',
    # Formatting
    'decimal_to_float'
]
