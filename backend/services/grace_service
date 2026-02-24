"""
services/grace_service.py — QWB Quick Wins Bundle (v1.6.1)
===========================================================
New service file. Place at: backend/services/grace_service.py
Export compute_grace_days_remaining from backend/services/__init__.py

Canonical spec: position_endpoints.md v1.8.3
               QWB decision D4
"""

from typing import Optional


def compute_grace_days_remaining(
    grace_period: bool,
    holding_days: int,
) -> Optional[int]:
    """
    Compute grace_days_remaining for a single position object.

    Rules (canonical — position_endpoints.md v1.8.3):
        When grace_period is True:
            grace_days_remaining = max(0, 10 - holding_days)
        When grace_period is False:
            grace_days_remaining = None  (serialises as JSON null)

    CRITICAL (A-QA-05): On day 10, grace_period becomes False.
    The field returns None — NOT 0. The formula max(0, 10-10) = 0
    does NOT apply because the grace_period flag gates which branch
    executes. Day 10 is post-grace. Returning 0 on day 10 is a defect.

    Args:
        grace_period:  Whether the position is in its grace window.
                       Sourced directly from the position record.
        holding_days:  Calendar days held. Sourced from position record.

    Returns:
        int  — days remaining in grace window (>= 1), when in grace
        None — when grace_period is False (post-grace)
    """
    if not grace_period:
        return None

    return max(0, 10 - holding_days)
