"""
ST-08 (BLG-SEC-13, EPIC-02, v7.10): Raw exception text returned in API error
responses.

Covers: all 27 explicit 500-class error paths in backend/main.py (25
HTTPException(status_code=500, ...) call sites + 2 JSONResponse(status_code=500,
...) call sites) now return a generic client-facing message instead of the
raw exception string, with the full exception still printed server-side
(traceback.print_exc()) for debugging. Intentional 4xx error messages
(RISK-03) are confirmed unchanged — they still surface str(e) verbatim,
since these are safe, deliberate messages (e.g. "Position not found"),
not internal-detail leaks.

Spot-checks a representative sample of endpoints rather than all 27 — the
fix was a single mechanical substitution applied identically everywhere
(verified via `grep -c 'detail="Internal server error"'` == 25 and
`grep -c 'message": "Internal server error"'` == 2 during implementation).

CI-safe: no live DB or network connections — TestClient(app) with the
session-scoped database stub; underlying service functions are mocked to
raise directly.
"""

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)

_SENSITIVE_DETAIL = "psycopg2.OperationalError: password authentication failed for user 'admin' at /secret/internal/path.py"


class Test500PathsNoLongerLeakRawExceptionText:

    def test_post_settings_500_returns_generic_message(self):
        with patch("main.create_settings", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.post("/settings", json={"min_hold_days": 5})
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body.get("detail") == "Internal server error"

    def test_get_positions_500_path_returns_generic_message(self):
        # get_positions_endpoint: ValueError -> 404 (str(e) kept, RISK-03);
        # any other Exception -> 500 (generic message).
        with patch("main.get_positions_with_prices", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/positions")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body.get("detail") == "Internal server error"

    def test_reports_daily_pnl_500_json_response_path_returns_generic_message(self):
        with patch("main.get_daily_pnl_report", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/reports/daily-pnl", params={"year": 2026, "month": 7})
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body.get("message") == "Internal server error"

    def test_reports_monthly_pnl_500_json_response_path_returns_generic_message(self):
        with patch("main.get_monthly_pnl_report", side_effect=RuntimeError(_SENSITIVE_DETAIL)):
            resp = CLIENT.get("/reports/monthly-pnl")
        assert resp.status_code == 500
        body = resp.json()
        assert _SENSITIVE_DETAIL not in str(body)
        assert body.get("message") == "Internal server error"


class Test4xxPathsUnchangedPerRiskO3:
    """RISK-03: intentional, safe 4xx error messages must not change."""

    def test_get_positions_value_error_still_returns_404_with_original_message(self):
        with patch("main.get_positions_with_prices", side_effect=ValueError("Portfolio not found")):
            resp = CLIENT.get("/positions")
        assert resp.status_code == 404
        assert resp.json().get("detail") == "Portfolio not found"


if __name__ == "__main__":
    import unittest
    unittest.main()
