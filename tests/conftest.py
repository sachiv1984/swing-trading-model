"""
Pytest configuration for the swing trading model test suite.

Sets up sys.path to include backend/ and provides a dummy DATABASE_URL
environment variable to prevent database.py from raising a ValueError at
import time. Tests that require a real database use their own mocking strategy.
"""
import os
import sys
from pathlib import Path

# Add backend to sys.path so all test files can import backend modules directly
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Provide a dummy DATABASE_URL before any test module imports database.py.
# This prevents the "DATABASE_URL environment variable not set" ValueError
# that would otherwise fire at collection time for any test importing the
# backend database module (directly or via services/__init__.py).
# Tests that need a real DB use their own mock/stub strategy.
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/test_stub"

# Import mock harness fixtures (BLG-QA-08 / ST-09)
from tests.mock_harness.conftest_extension import (  # noqa: F401, E402
    alpaca_mock_harness,
    yahoo_mock_harness,
    screener_mocks,
    scenario_mocks,
)
