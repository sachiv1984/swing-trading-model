"""
Application Configuration

Constants and configuration values for the Trading Assistant API.
"""

import os

# API Metadata
API_TITLE = "Trading Assistant API"
API_VERSION = "1.2.0"

# CORS Origins
# ST-43 (BLG-SEC-43, EPIC-06, v9.14): one list used to serve every environment,
# so production accepted credentialed requests from http://localhost:3000 and
# the staging frontend. The list is now chosen per deployment; defaults and
# precedence are documented in docs/infrastructure/cors_allow_list.md.
PAGES_ORIGIN = "https://sachiv1984.github.io"
CORS_DEFAULT_ORIGINS = {
    "production": [
        PAGES_ORIGIN,
        "https://trading-assistant-api-c0f9.onrender.com",
    ],
    "staging": [
        "https://trading-assistant-staging.onrender.com",  # Staging frontend (render.yaml)
        "http://localhost:3000",
    ],
    "development": [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
}


def resolve_deploy_env(env=None) -> str:
    """production | staging | development. DEPLOY_ENV wins; otherwise a Render
    service (RENDER is set) is staging when its RENDER_SERVICE_NAME ends in
    "-staging" and production when it does not; off Render it is development."""
    env = os.environ if env is None else env
    explicit = (env.get("DEPLOY_ENV") or "").strip().lower()
    if explicit:
        if explicit not in CORS_DEFAULT_ORIGINS:
            raise ValueError(
                f"DEPLOY_ENV={explicit!r}; expected one of {sorted(CORS_DEFAULT_ORIGINS)}"
            )
        return explicit
    if env.get("RENDER"):
        return "staging" if env.get("RENDER_SERVICE_NAME", "").endswith("-staging") else "production"
    return "development"


def resolve_allowed_origins(env=None) -> list:
    """CORS_ALLOWED_ORIGINS (comma-separated) if set, else the defaults for
    resolve_deploy_env()."""
    env = os.environ if env is None else env
    override = env.get("CORS_ALLOWED_ORIGINS", "")
    origins = [o.strip().rstrip("/") for o in override.split(",") if o.strip()]
    return origins or list(CORS_DEFAULT_ORIGINS[resolve_deploy_env(env)])


DEPLOY_ENV = resolve_deploy_env()
ALLOWED_ORIGINS = resolve_allowed_origins()

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

# Alert delivery (Telegram Bot API) — ST-04
# Set these env vars on Render: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
# TELEGRAM_BOT_TOKEN: token from @BotFather
# TELEGRAM_CHAT_ID: your chat ID (from getUpdates)
import os
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Claude API daily cost threshold alert (ST-09, BLG-OPS-34)
# Set AI_DAILY_COST_THRESHOLD on Render to override the default.
AI_DAILY_COST_THRESHOLD = float(os.getenv("AI_DAILY_COST_THRESHOLD", "1.00"))

# API Delays (rate limiting)
PRICE_FETCH_DELAY_SECONDS = 0.3
FX_RATE_FETCH_DELAY_SECONDS = 0.2
MARKET_REGIME_FETCH_DELAY_SECONDS = 0.3
