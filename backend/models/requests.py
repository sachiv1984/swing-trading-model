"""
Request Models for Trading Assistant API

Pydantic models for validating incoming API requests.
"""

from pydantic import BaseModel
from typing import Optional


class AddPositionRequest(BaseModel):
    """Request model for adding a new position"""
    ticker: str
    market: str
    entry_date: str
    shares: float  # Supports fractional shares
    entry_price: float  # Native currency (USD for US, GBP for UK)
    current_price: Optional[float] = None
    fx_rate: Optional[float] = None
    atr_value: Optional[float] = None
    stop_price: Optional[float] = None
    fees: Optional[float] = None
    status: Optional[str] = "open"
    entry_note: Optional[str] = None
    tags: Optional[List[str]] = None


class SettingsRequest(BaseModel):
    """Request model for updating settings"""
    min_hold_days: Optional[int] = 5
    atr_multiplier_initial: Optional[float] = 2
    atr_multiplier_trailing: Optional[float] = 2
    atr_period: Optional[int] = 14
    default_currency: Optional[str] = "GBP"
    theme: Optional[str] = "dark"
    uk_commission: Optional[float] = 9.95
    us_commission: Optional[float] = 0
    stamp_duty_rate: Optional[float] = 0.005
    fx_fee_rate: Optional[float] = 0.0015


class CashTransactionRequest(BaseModel):
    """Request model for recording cash deposits/withdrawals"""
    type: str  # "deposit" or "withdrawal"
    amount: float
    date: Optional[str] = None
    note: Optional[str] = ""


class ExitPositionRequest(BaseModel):
    """
    Request model for exiting a position (full or partial)
    
    v1.2 Features:
    - Supports partial exits via shares parameter
    - Requires user-provided exit price (actual broker execution)
    - Accepts custom exit date for backdating
    - Requires FX rate for US stocks (from broker statement)
    """
    shares: Optional[float] = None  # Optional: defaults to all shares
    exit_price: float  # REQUIRED: user-provided exit price
    exit_date: Optional[str] = None  # Optional: defaults to today
    exit_reason: Optional[str] = "Manual Exit"
    exit_fx_rate: Optional[float] = None  # REQUIRED for US stocks, ignored for UK
    exit_note: Optional[str] = None
