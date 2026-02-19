"""
Request Models for Trading Assistant API

Pydantic models for validating incoming API requests.
"""

from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime


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
    min_hold_days: Optional[int] = None
    atr_multiplier_initial: Optional[float] = None
    atr_multiplier_trailing: Optional[float] = None
    atr_period: Optional[int] = None
    default_currency: Optional[str] = None
    theme: Optional[str] = None
    uk_commission: Optional[float] = None
    us_commission: Optional[float] = None
    stamp_duty_rate: Optional[float] = None
    fx_fee_rate: Optional[float] = None
    min_trades_for_analytics: Optional[int] = None
    default_risk_percent: Optional[float] = None

    @validator('default_risk_percent')
    def validate_default_risk_percent(cls, v):
        if v is not None and (v <= 0 or v > 100):
            raise ValueError('default_risk_percent must be greater than 0 and at most 100')
        return v


class SizePositionRequest(BaseModel):
    """Request model for position sizing calculation"""
    entry_price: float
    stop_price: float
    risk_percent: float
    market: Optional[str] = "UK"
    fx_rate: Optional[float] = None

    @validator('entry_price')
    def validate_entry_price(cls, v):
        if v is None:
            raise ValueError('entry_price is required')
        return v

    @validator('stop_price')
    def validate_stop_price(cls, v):
        if v is None:
            raise ValueError('stop_price is required')
        return v

    @validator('risk_percent')
    def validate_risk_percent(cls, v):
        if v is None:
            raise ValueError('risk_percent is required')
        return v

    @validator('market')
    def validate_market(cls, v):
        if v is not None and v not in ('US', 'UK'):
            raise ValueError('market must be "US" or "UK"')
        return v

    @validator('fx_rate')
    def validate_fx_rate(cls, v):
        if v is not None and v <= 0:
            raise ValueError('fx_rate must be greater than 0')
        return v


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
