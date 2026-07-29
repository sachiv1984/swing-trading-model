"""
ST-03 (BLG-BE-76, EPIC-01, v7.10): Idempotency-key pattern for state-mutating
POST endpoints.

Covers utils/idempotency.py::replay_or_create in isolation:
- RISK-02: when idempotency_key is absent, create_fn() is called and its
  result returned with zero access to the idempotency_keys table.
- When idempotency_key is present and no prior record exists, create_fn()
  runs once and the result is stored.
- When idempotency_key is present and a prior record exists, create_fn() is
  NOT called again — the cached response is replayed verbatim (dedup).

CI-safe: no live DB or network connections.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from utils.idempotency import replay_or_create


class TestReplayOrCreate(unittest.TestCase):

    def test_no_key_calls_create_fn_with_no_db_access(self):
        create_fn = MagicMock(return_value={"status": "ok", "data": {"id": "abc"}})
        with patch("database.ensure_idempotency_keys_table") as mock_ensure, \
             patch("database.get_idempotency_record") as mock_get, \
             patch("database.create_idempotency_record") as mock_create_rec:
            result = replay_or_create("portfolio-1", "POST /portfolio/position", None, create_fn)

        create_fn.assert_called_once()
        mock_ensure.assert_not_called()
        mock_get.assert_not_called()
        mock_create_rec.assert_not_called()
        self.assertEqual(result, {"status": "ok", "data": {"id": "abc"}})

    def test_empty_string_key_treated_as_absent(self):
        create_fn = MagicMock(return_value={"status": "ok"})
        result = replay_or_create("portfolio-1", "POST /trade-plans", "", create_fn)
        create_fn.assert_called_once()
        self.assertEqual(result, {"status": "ok"})

    def test_first_call_with_key_stores_result(self):
        create_fn = MagicMock(return_value={"status": "ok", "data": {"id": "new-1"}})
        with patch("database.ensure_idempotency_keys_table") as mock_ensure, \
             patch("database.get_idempotency_record", return_value=None) as mock_get, \
             patch("database.create_idempotency_record") as mock_create_rec:
            result = replay_or_create("portfolio-1", "POST /portfolio/position", "key-123", create_fn)

        mock_ensure.assert_called_once()
        mock_get.assert_called_once_with("portfolio-1", "POST /portfolio/position", "key-123")
        create_fn.assert_called_once()
        mock_create_rec.assert_called_once_with(
            "portfolio-1", "POST /portfolio/position", "key-123",
            {"status": "ok", "data": {"id": "new-1"}},
        )
        self.assertEqual(result, {"status": "ok", "data": {"id": "new-1"}})

    def test_retried_call_with_same_key_replays_cached_response_no_duplicate_create(self):
        create_fn = MagicMock(return_value={"status": "ok", "data": {"id": "should-not-be-created"}})
        cached = {"status": "ok", "data": {"id": "original-1"}}
        with patch("database.ensure_idempotency_keys_table"), \
             patch("database.get_idempotency_record", return_value=cached), \
             patch("database.create_idempotency_record") as mock_create_rec:
            result = replay_or_create("portfolio-1", "POST /portfolio/position", "key-123", create_fn)

        create_fn.assert_not_called()
        mock_create_rec.assert_not_called()
        self.assertEqual(result, cached)


if __name__ == "__main__":
    unittest.main()
