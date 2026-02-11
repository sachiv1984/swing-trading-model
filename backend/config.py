"""
Application Configuration

Constants and configuration values for the Trading Assistant API.
"""

# API Metadata
API_TITLE = "Trading Assistant API"
API_VERSION = "1.2.0"

# CORS Origins
ALLOWED_ORIGINS = [
    "https://sachiv1984.github.io",
    "https://trading-assistant-api-c0f9.onrender.com",
    "http://localhost:3000"
]

# Default Fee Rates
DEFAULT_UK_COMMISSION = 9.95  # GBP
DEFAULT_US_COMMISSION = 0.00  # GBP (zero commission brokers)
DEFAULT_STAMP_DUTY_RATE = 0.005  # 0.5%
DEFAULT_FX_FEE_RATE = 0.0015  # 0.15%

# Strategy Parameters
DEFAULT_MIN_HOLD_DAYS = 10  # Grace period
DEFAULT_ATR_MULTIPLIER_INITIAL = 5.0  # Wide stop for losing positions
DEFAULT_ATR_MULTIPLIER_TRAILING = 2.0  # Tight stop for profitable positions
DEFAULT_ATR_PERIOD = 14  # Days

# Default Currency
DEFAULT_CURRENCY = "GBP"

# Theme
DEFAULT_THEME = "dark"

# Signal Generation Parameters
MOMENTUM_LOOKBACK_DAYS = 252  # 1 year
TOP_N_SIGNALS = 5
MA_PERIOD = 200
ATR_PERIOD = 14
VOLATILITY_WINDOW = 60
MIN_POSITION_PCT = 0.05  # 5% of portfolio
MAX_POSITION_PCT = 0.20  # 20% of portfolio

# Default FX Rate Fallback
DEFAULT_FX_RATE = 1.27  # GBP/USD fallback if API fails

# Price Conversion
PENCE_TO_POUNDS_THRESHOLD = 1000  # UK prices above this are in pence

# API Delays (rate limiting)
PRICE_FETCH_DELAY_SECONDS = 0.3
FX_RATE_FETCH_DELAY_SECONDS = 0.2
MARKET_REGIME_FETCH_DELAY_SECONDS = 0.3
