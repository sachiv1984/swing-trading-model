"""
ST-13 (EPIC-02, v9.13, BLG-QA-208): strategy_rules.md §4 "Required at entry"
(traceability matrix C4-01) at the POST /portfolio/position contract.

§4 requires ticker, entry date, entry price, shares and an ATR value. The first
four (with market, which §4's fee rule needs) are required request fields: each
one, omitted, is rejected with a 422 before add_position() runs. The ATR is
required on the stored position, not from the client: an omitted atr_value is
accepted and add_position() derives it (fetched, else the 2% fallback, with
atr_source recording which -- asserted in tests/test_atr_provenance.py
TestEntryProvenance), so a position is never stored without one.

CI-safe: add_position is patched; no live DB or network connections.
"""
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import real_database_imports  # noqa: E402

# Real backend/database.py only while these modules import; conftest's stub is
# restored afterwards so later test files still see it (ST-14, BLG-QA-190).
with real_database_imports():
    from fastapi.testclient import TestClient  # noqa: E402

    import main  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)

VALID_BODY = {"ticker": "VOD.L", "market": "UK", "entry_date": "2026-10-13", "shares": 10, "entry_price": 100.0}

REQUIRED_FIELDS = ["ticker", "market", "entry_date", "entry_price", "shares"]


@pytest.mark.parametrize("field", REQUIRED_FIELDS)
def test_omitting_a_required_entry_field_is_rejected(field):
    body = {k: v for k, v in VALID_BODY.items() if k != field}
    with patch.object(main, "add_position") as mock_add:
        response = CLIENT.post("/portfolio/position", json=body)
    assert response.status_code == 422
    assert field in response.text
    mock_add.assert_not_called()


def test_complete_body_without_atr_is_accepted_and_atr_left_to_the_server():
    with patch.object(main, "add_position", return_value={"position_id": "p-1"}) as mock_add:
        response = CLIENT.post("/portfolio/position", json=VALID_BODY)
    assert response.status_code == 200
    mock_add.assert_called_once()
    assert mock_add.call_args.kwargs["atr_value"] is None  # derived by add_position(), never stored empty


def test_required_set_matches_the_request_model():
    """Guards the list above: if a field becomes optional (or a new one required),
    this fails and the C4-01 matrix row must be revisited."""
    required = {name for name, f in main.AddPositionRequest.model_fields.items() if f.is_required()}
    assert required == set(REQUIRED_FIELDS)
