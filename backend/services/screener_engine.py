"""
Screener Engine (DS-01 / ST-03)

Computes screener result for a single ticker from normalised OHLCV data.
Pure computation — no external calls; all I/O is the caller's responsibility.

Filter order (screener_results_schema.md §4):
  1. Regime gate   — market index above MA200?
  2. Data gate     — minimum 15 bars for 14-period ATR?
  3. ATR gate      — ATR above minimum threshold?
  4. Signal gate   — signal score above minimum threshold?

Parameters (strategy_rules.md §11):
  ATR_PERIOD        = 14
  MIN_ATR_PCT       = 0.005   (0.5% of price; rejects near-zero-volatility tickers)
  MIN_SIGNAL_SCORE  = 0.25    (0.0–1.0 scale)
"""
import math
from typing import Optional, List, Dict

# ---------------------------------------------------------------------------
# Strategy parameters
# ---------------------------------------------------------------------------
ATR_PERIOD = 14
MIN_ATR_PCT = 0.005
MIN_SIGNAL_SCORE = 0.25

OHLCVRecord = Dict[str, object]


# ---------------------------------------------------------------------------
# ATR calculation (Wilder's 14-period)
# ---------------------------------------------------------------------------

def compute_atr(ohlcv: List[OHLCVRecord], period: int = ATR_PERIOD) -> Optional[float]:
    """
    Returns Wilder's ATR for the given OHLCV records, or None if insufficient data.
    ohlcv must be sorted by date ascending.
    Requires len(ohlcv) >= period + 1 bars.
    """
    if len(ohlcv) < period + 1:
        return None

    def _tr(curr, prev) -> float:
        h, l, prev_c = float(curr["high"]), float(curr["low"]), float(prev["close"])
        return max(h - l, abs(h - prev_c), abs(l - prev_c))

    # Seed: simple average of first `period` true ranges
    trs = [_tr(ohlcv[i], ohlcv[i - 1]) for i in range(1, period + 1)]
    atr = sum(trs) / period

    # Wilder smoothing for remaining bars
    for i in range(period + 1, len(ohlcv)):
        atr = (atr * (period - 1) + _tr(ohlcv[i], ohlcv[i - 1])) / period

    return atr


# ---------------------------------------------------------------------------
# Signal scoring (RSI + MACD + volume)
# ---------------------------------------------------------------------------

def _ema(values: List[float], period: int) -> List[float]:
    if not values:
        return []
    k = 2 / (period + 1)
    result = [values[0]]
    for v in values[1:]:
        result.append(v * k + result[-1] * (1 - k))
    return result


def _rsi(closes: List[float], period: int = 14) -> Optional[float]:
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        delta = closes[i] - closes[i - 1]
        gains.append(max(delta, 0))
        losses.append(max(-delta, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


def _macd_histogram(closes: List[float]) -> Optional[float]:
    if len(closes) < 26:
        return None
    fast = _ema(closes, 12)
    slow = _ema(closes, 26)
    macd_line = [f - s for f, s in zip(fast[13:], slow[13:])]
    if not macd_line:
        return None
    signal_line = _ema(macd_line, 9)
    return macd_line[-1] - signal_line[-1]


def compute_signal_score(ohlcv: List[OHLCVRecord]) -> float:
    """
    Returns composite signal score 0.0–1.0.
    Components: RSI momentum (40%), MACD histogram direction (40%), volume surge (20%).
    """
    closes = [float(r["close"]) for r in ohlcv]
    volumes = [float(r["volume"]) for r in ohlcv]

    score = 0.0

    # RSI component (0–40 points → 0.0–0.4)
    rsi = _rsi(closes)
    if rsi is not None:
        # Optimal RSI range for momentum: 50–70 → maps to 0.4 max
        if rsi >= 50:
            score += min((rsi - 50) / 50, 1.0) * 0.4
        else:
            # Below 50 contributes 0
            pass

    # MACD histogram component (0–40 points → 0.0–0.4)
    hist = _macd_histogram(closes)
    if hist is not None and len(closes) >= 26:
        price = closes[-1]
        # Normalise histogram vs price: positive histogram = bullish
        if price > 0:
            norm = hist / price  # fraction of price
            macd_contrib = max(min(norm / 0.02, 1.0), 0.0) * 0.4
            score += macd_contrib

    # Volume surge component (0–20 points → 0.0–0.2)
    if len(volumes) >= 10:
        recent_vol = volumes[-1]
        avg_vol = sum(volumes[-10:-1]) / 9 if len(volumes) >= 10 else recent_vol
        if avg_vol > 0:
            ratio = recent_vol / avg_vol
            # 1.5× average volume → full contribution
            vol_contrib = min((ratio - 1.0) / 0.5, 1.0) * 0.2 if ratio > 1.0 else 0.0
            score += vol_contrib

    return min(max(score, 0.0), 1.0)


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def compute_screener_result(
    ticker: str,
    market: str,
    ohlcv_data: List[OHLCVRecord],
    regime_status: str,
    regime_index: str,
    regime_index_price: float,
    regime_index_ma200: float,
    sector: Optional[str] = None,
    industry: Optional[str] = None,
    news_headlines: Optional[list] = None,
    run_id: Optional[str] = None,
    run_timestamp: Optional[str] = None,
) -> Optional[Dict]:
    """
    Evaluate one ticker through the screener filter pipeline.

    Returns a ScreenerResultRecord dict (screener_results_schema.md §1.1) if the
    ticker passes all gates, or None if it is excluded.

    regime_status must be "risk_on" or "risk_off".
    """
    # Gate 1: Regime
    if regime_status != "risk_on":
        return None

    # Gate 2: Data sufficiency
    if not ohlcv_data or len(ohlcv_data) < ATR_PERIOD + 1:
        return None

    closes = [float(r["close"]) for r in ohlcv_data]
    price = closes[-1]
    if price <= 0:
        return None

    # Gate 3: ATR
    atr = compute_atr(ohlcv_data, ATR_PERIOD)
    if atr is None or atr <= 0:
        return None
    atr_pct = atr / price
    if atr_pct < MIN_ATR_PCT:
        return None

    # Gate 4: Signal score
    signal_score = compute_signal_score(ohlcv_data)
    if signal_score < MIN_SIGNAL_SCORE:
        return None

    currency = "GBP" if market == "UK" else "USD"
    news = news_headlines or []
    proximity = None
    if atr > 0:
        entry_zone_lower = price - 2 * atr
        if entry_zone_lower > 0:
            proximity = (price - entry_zone_lower) / entry_zone_lower

    return {
        "ticker": ticker,
        "market": market,
        "currency": currency,
        "price": price,
        "atr": atr,
        "atr_period": ATR_PERIOD,
        "regime_status": regime_status,
        "regime_index": regime_index,
        "regime_index_price": regime_index_price,
        "regime_index_ma200": regime_index_ma200,
        "signal_score": signal_score,
        "signal_type": "strong_momentum" if signal_score >= 0.6 else "momentum",
        "sector": sector,
        "industry": industry,
        "proximity_to_entry_zone": proximity,
        "news_headline_count": len(news),
        "news_headlines": news,
        "run_id": run_id,
        "run_timestamp": run_timestamp,
    }
