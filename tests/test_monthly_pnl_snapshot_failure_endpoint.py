"""
ST-09 (EPIC-02, v9.13, BLG-BE-156): GET /reports/monthly-pnl stays up when the
monthly_pnl_snapshots store fails.

Endpoint-level companion to TestMonthlyPnlSnapshotFailure in
test_monthly_pnl_snapshot.py: drives the real route through TestClient with
the snapshot read mocked to fail, and asserts a 200 with realised P&L for every
month and no `restated` field on any month.

CI-safe: no live DB or network connections. The service's database functions
are patched in the module namespace get_monthly_pnl_report actually resolves
them from (its __globals__), so the patch holds whichever copy of the module
main.py bound at import time.
"""

import sys
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import real_database_imports  # noqa: E402

# Real backend/database.py only while these modules import; conftest's stub is
# restored afterwards so later test files still see it (ST-14, BLG-QA-190).
with real_database_imports():

    from fastapi.testclient import TestClient  # noqa: E402

    import main  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)

ROWS = [
    {"year": 2026, "month": 8, "realised_pnl_gbp": 250.0, "trade_count": 3, "null_fee_trade_count": 0},
    {"year": 2026, "month": 9, "realised_pnl_gbp": -75.5, "trade_count": 1, "null_fee_trade_count": 0},
]


def test_monthly_pnl_returns_200_without_restated_when_snapshot_read_fails(caplog):
    service_globals = main.get_monthly_pnl_report.__globals__
    fake_datetime = MagicMock()
    fake_datetime.now.return_value.date.return_value = date(2026, 9, 22)
    with patch.dict(service_globals, {
        "get_portfolio": MagicMock(return_value={"id": "portfolio-test-001"}),
        "get_monthly_pnl": MagicMock(return_value=ROWS),
        "get_db": MagicMock(),
        "ensure_monthly_pnl_snapshots_table": MagicMock(),
        "get_monthly_pnl_snapshot": MagicMock(side_effect=RuntimeError("snapshot read failed")),
        "insert_monthly_pnl_snapshot_if_absent": MagicMock(),
        "get_estimated_unrealised_pnl": MagicMock(return_value=None),
        "datetime": fake_datetime,
    }), patch.object(main, "get_arc5_compliance_summary", return_value={}):
        with caplog.at_level("ERROR"):
            resp = CLIENT.get("/reports/monthly-pnl")

    assert resp.status_code == 200
    body = resp.json()
    assert [(m["year"], m["month"], m["realised_pnl_gbp"]) for m in body["data"]] == [
        (2026, 8, 250.0),
        (2026, 9, -75.5),
    ]
    assert all("restated" not in m for m in body["data"])
    failures = [r for r in caplog.records if r.levelname == "ERROR" and r.exc_info]
    assert failures, "snapshot failure must be logged with exc_info"
