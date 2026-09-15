"""
ai_output_sampling_service regression tests (ST-23, BLG-AI-06, EPIC-05, v9.4).

Proves the sampling hook's three AC-mandated properties:
  1. Default OFF -- no env var set, nothing is ever sampled.
  2. Opt-in / sampling-rate-bounded -- even when enabled, only a bounded
     fraction of calls are sampled, never every call.
  3. Never breaks the caller -- a store failure inside maybe_sample_output()
     is swallowed, matching create_gemini_audit_entry/create_claude_audit_entry's
     existing fail-safe convention.

Isolation note (found live, this story, CI): `maybe_sample_output()`
deliberately does `from database import create_ai_output_boundary_sample`
as a *deferred*, function-local import, resolving against whatever
`sys.modules["database"]` is at call time. conftest.py's session-scoped
stub makes that a bare MagicMock with no internal logic -- adequate for
proving the sampling hook was invoked, not adequate for proving the real
create_ai_output_boundary_sample()'s own get_db()-based fail-safe
behaviour, which several tests below need to exercise for real.

An earlier version of this file loaded the real module via a permanent
`sys.modules.pop("database", None); import database` at module level
(the same pattern `test_trade_plan_audit_log.py` already uses). That
mutates the shared, process-global `sys.modules["database"]` slot for
the rest of the pytest session with no restore -- and because this
file's name sorts alphabetically *before* `test_alerts_service.py`,
that permanent swap was observed leaking into `alerts_service.py`'s own
test file (which expects the stub) and causing a real Postgres
connection attempt there in CI's real-Postgres integration job.
`test_trade_plan_audit_log.py` has the identical unrestored swap but
happens to sort late enough alphabetically that nothing after it needs
the stub back -- this file is not so lucky.

Fixed here by loading a *private* copy of the real module under its own
name (`database_real_for_ai_output_sampling_test`) -- mirroring
`test_position_audit_log.py`'s established convention for the exact
same problem -- and using `patch.dict(sys.modules, {"database": ...})`
scoped to individual `with` blocks (auto-restored at each block's exit)
wherever `sampling.maybe_sample_output()`'s deferred import needs to
resolve to the real module. `sys.modules["database"]` itself is never
mutated outside those tightly-scoped blocks, so no leakage into any
other test file is possible regardless of collection order.
"""
import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.ai_output_sampling_service as sampling  # noqa: E402

_db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'database.py')
_spec = importlib.util.spec_from_file_location('database_real_for_ai_output_sampling_test', _db_path)
_real_database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_real_database)


def _mock_conn():
    mock_cursor = MagicMock()
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


def _real_database_active():
    """Context manager: sys.modules["database"] is the real module for the
    duration of the `with` block only -- auto-restored at exit via
    patch.dict, regardless of what it was before (conftest.py's stub in
    the normal case). Safe against any collection-order leakage."""
    return patch.dict(sys.modules, {"database": _real_database})


class _EnvHelper:
    def setup_method(self):
        self._saved = {}
        for key in ("AI_OUTPUT_SAMPLING_ENABLED", "AI_OUTPUT_SAMPLING_RATE"):
            self._saved[key] = os.environ.pop(key, None)

    def teardown_method(self):
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


class TestDefaultOff(_EnvHelper):
    def test_is_sampling_enabled_defaults_false_when_unset(self):
        assert sampling.is_sampling_enabled() is False

    def test_maybe_sample_output_writes_nothing_when_unset(self):
        with _real_database_active(), patch.object(_real_database, "get_db") as mock_get_db:
            result = sampling.maybe_sample_output("chat", "some AI output text")
        assert result is False
        mock_get_db.assert_not_called()

    def test_is_sampling_enabled_false_for_explicit_off_values(self):
        for value in ("false", "0", "no", "off", ""):
            os.environ["AI_OUTPUT_SAMPLING_ENABLED"] = value
            assert sampling.is_sampling_enabled() is False, f"value={value!r} should be off"


class TestOptInTruthyValues(_EnvHelper):
    def test_is_sampling_enabled_true_for_explicit_on_values(self):
        for value in ("true", "1", "yes", "on", "TRUE", "On"):
            os.environ["AI_OUTPUT_SAMPLING_ENABLED"] = value
            assert sampling.is_sampling_enabled() is True, f"value={value!r} should be on"


class TestSamplingRateBounded(_EnvHelper):
    def test_sampling_rate_defaults_to_point_one(self):
        assert sampling.sampling_rate() == 0.1

    def test_sampling_rate_clamped_above_one(self):
        os.environ["AI_OUTPUT_SAMPLING_RATE"] = "5.0"
        assert sampling.sampling_rate() == 1.0

    def test_sampling_rate_clamped_below_zero(self):
        os.environ["AI_OUTPUT_SAMPLING_RATE"] = "-2.0"
        assert sampling.sampling_rate() == 0.0

    def test_sampling_rate_falls_back_to_default_on_bad_value(self):
        os.environ["AI_OUTPUT_SAMPLING_RATE"] = "not-a-number"
        assert sampling.sampling_rate() == 0.1

    def test_maybe_sample_output_never_samples_at_rate_zero(self):
        os.environ["AI_OUTPUT_SAMPLING_ENABLED"] = "true"
        os.environ["AI_OUTPUT_SAMPLING_RATE"] = "0.0"
        with _real_database_active(), patch.object(_real_database, "get_db") as mock_get_db:
            for _ in range(20):
                assert sampling.maybe_sample_output("chat", "text") is False
        mock_get_db.assert_not_called()

    def test_maybe_sample_output_always_samples_at_rate_one(self):
        os.environ["AI_OUTPUT_SAMPLING_ENABLED"] = "true"
        os.environ["AI_OUTPUT_SAMPLING_RATE"] = "1.0"
        mock_conn, mock_cursor = _mock_conn()
        with _real_database_active(), \
             patch.object(_real_database, "get_db", return_value=mock_conn), \
             patch.object(_real_database, "ensure_ai_output_boundary_samples_table"):
            for _ in range(5):
                assert sampling.maybe_sample_output("chat", "text") is True


class TestNotFullContentLogging(_EnvHelper):
    def test_maybe_sample_output_does_not_write_empty_text(self):
        os.environ["AI_OUTPUT_SAMPLING_ENABLED"] = "true"
        os.environ["AI_OUTPUT_SAMPLING_RATE"] = "1.0"
        with _real_database_active(), patch.object(_real_database, "get_db") as mock_get_db:
            assert sampling.maybe_sample_output("chat", "") is False
            assert sampling.maybe_sample_output("chat", None) is False
        mock_get_db.assert_not_called()


class TestNeverBreaksCaller(_EnvHelper):
    def test_maybe_sample_output_never_raises_on_store_failure(self):
        os.environ["AI_OUTPUT_SAMPLING_ENABLED"] = "true"
        os.environ["AI_OUTPUT_SAMPLING_RATE"] = "1.0"
        with _real_database_active(), patch.object(_real_database, "get_db", side_effect=RuntimeError("db down")):
            # Must not raise -- caller's real AI response must never fail
            # because sampling instrumentation failed. create_ai_output_
            # boundary_sample() itself swallows this (same fire-and-forget
            # convention as create_gemini_audit_entry/create_claude_audit_
            # entry), so maybe_sample_output correctly still reports True
            # (a write was attempted) -- it is not a second failure-
            # detection layer. The property under test is "does not raise",
            # not "detects the downstream failure".
            result = sampling.maybe_sample_output("chat", "text")
        assert result is True

    def test_maybe_sample_output_never_raises_on_env_parsing_failure(self):
        os.environ["AI_OUTPUT_SAMPLING_ENABLED"] = "true"
        with patch.object(sampling, "sampling_rate", side_effect=RuntimeError("boom")):
            result = sampling.maybe_sample_output("chat", "text")
        assert result is False


class TestDatabaseLayer:
    """Direct tests of the new database.py functions (ST-23), against the
    private real-module copy -- never touches sys.modules["database"]."""

    def test_ensure_ai_output_boundary_samples_table_creates_table_and_index(self):
        mock_conn, mock_cursor = _mock_conn()
        with patch.object(_real_database, "get_db", return_value=mock_conn):
            _real_database.ensure_ai_output_boundary_samples_table()

        sql_statements = [call.args[0] for call in mock_cursor.execute.call_args_list if call.args]
        assert any("CREATE TABLE IF NOT EXISTS ai_output_boundary_samples" in s for s in sql_statements)
        assert any("idx_aobs_sampled_at" in s for s in sql_statements)

    def test_create_ai_output_boundary_sample_inserts_row(self):
        mock_conn, mock_cursor = _mock_conn()
        with patch.object(_real_database, "get_db", return_value=mock_conn), \
             patch.object(_real_database, "ensure_ai_output_boundary_samples_table"):
            _real_database.create_ai_output_boundary_sample("chat (POST /ai/chat)", "some output text", "claude-haiku-4-5")

        insert_calls = [c for c in mock_cursor.execute.call_args_list if c.args and "INSERT INTO ai_output_boundary_samples" in c.args[0]]
        assert len(insert_calls) == 1
        params = insert_calls[0].args[1]
        assert params == ("chat (POST /ai/chat)", "some output text", "claude-haiku-4-5")

    def test_create_ai_output_boundary_sample_never_raises_on_failure(self):
        with patch.object(_real_database, "get_db", side_effect=RuntimeError("db down")):
            _real_database.create_ai_output_boundary_sample("chat", "text")  # must not raise

    def test_get_ai_output_boundary_samples_returns_rows(self):
        mock_conn, mock_cursor = _mock_conn()
        mock_cursor.fetchall.return_value = [
            {"feature": "chat", "output_text": "hi", "model_version": "v1", "sampled_at": "2026-09-15"},
        ]
        with patch.object(_real_database, "get_db", return_value=mock_conn), \
             patch.object(_real_database, "ensure_ai_output_boundary_samples_table"):
            rows = _real_database.get_ai_output_boundary_samples(limit=5)
        assert rows == [{"feature": "chat", "output_text": "hi", "model_version": "v1", "sampled_at": "2026-09-15"}]

    def test_get_ai_output_boundary_samples_returns_empty_list_on_failure(self):
        with patch.object(_real_database, "get_db", side_effect=RuntimeError("db down")):
            assert _real_database.get_ai_output_boundary_samples() == []

    def test_purge_ai_output_boundary_samples_older_than_90_days(self):
        mock_conn, mock_cursor = _mock_conn()
        mock_cursor.rowcount = 3
        with patch.object(_real_database, "get_db", return_value=mock_conn):
            deleted = _real_database.purge_ai_output_boundary_samples_older_than_90_days()
        assert deleted == 3
