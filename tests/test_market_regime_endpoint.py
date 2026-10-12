"""
ST-19 (BLG-BE-140, EPIC-03, v9.11) — GET /market/regime is a read-only regime
source: it returns US/UK risk-on/risk-off from check_market_regime() and runs no
position analysis and no write.
"""
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
import main  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)
REGIME = {"spy_risk_on": True, "ftse_risk_on": False, "spy_price": 1, "spy_ma200": 1,
          "ftse_price": 1, "ftse_ma200": 1, "date": datetime(2026, 10, 8, 9, 0, 0)}


def test_returns_us_and_uk_regime():
    with patch.object(main, "check_market_regime", return_value=REGIME):
        resp = CLIENT.get("/market/regime")
    assert resp.status_code == 200
    body = resp.json()
    assert body["data"] == [{"market": "US", "status": "risk_on"}, {"market": "UK", "status": "risk_off"}]
    assert body["as_of"] == "2026-10-08T09:00:00"


def test_runs_no_position_analysis_and_no_write():
    with patch.object(main, "check_market_regime", return_value=REGIME), \
         patch("services.position_service.analyze_positions") as analyze, \
         patch("database.update_position") as update, \
         patch.object(main, "get_live_fx_rate") as fx:
        CLIENT.get("/market/regime")
    analyze.assert_not_called()
    update.assert_not_called()
    fx.assert_not_called()


def test_frontend_regime_client_does_not_call_analyze():
    src = (Path(__file__).resolve().parent.parent / "src" / "api" / "base44Client.js").read_text()
    start = src.index("MarketRegime: {")
    block = src[start:src.index("CashTransaction: {", start)]
    assert "getRegime()" in block
    assert "analyze" not in block.replace("/positions/analyze, which", "")
