"""
JSON Lines log formatter tests (ST-02, EPIC-01, v9.5, BLG-BE-112).

Verifies backend/utils/json_log_formatter.JsonLinesFormatter produces output
conforming to docs/specs/structured_logging_standards.md §Structured Log
Format: valid JSON, one object per line, all required fields present with
correct types, correlation_id "-" (context-var default) mapped to the
spec's documented "none" sentinel, and optional fields included only when
actually present on the record.
"""
import json
import logging

import pytest
from utils.json_log_formatter import JsonLinesFormatter


def _make_record(msg="hello", level=logging.INFO, name="services.position_service", **extra):
    record = logging.getLogger(name).makeRecord(
        name, level, __file__, 1, msg, (), None,
    )
    for key, value in extra.items():
        setattr(record, key, value)
    return record


class TestJsonLinesFormatter:
    def test_output_is_valid_single_line_json(self):
        record = _make_record()
        output = JsonLinesFormatter().format(record)
        assert "\n" not in output
        json.loads(output)  # raises if not valid JSON

    def test_required_fields_present_with_correct_types(self):
        record = _make_record(correlation_id="f47ac10b-58cc-4372-a567-0e02b2c3d479")
        payload = json.loads(JsonLinesFormatter().format(record))
        assert isinstance(payload["timestamp"], str)
        assert payload["timestamp"].endswith("Z")
        assert payload["level"] == "INFO"
        assert payload["correlation_id"] == "f47ac10b-58cc-4372-a567-0e02b2c3d479"
        assert payload["service"] == "services.position_service"
        assert payload["message"] == "hello"

    def test_missing_correlation_id_attribute_maps_to_none_sentinel(self):
        # No correlation_id set on the record at all (e.g. a log line from
        # outside the correlation-ID factory's coverage).
        record = _make_record()
        payload = json.loads(JsonLinesFormatter().format(record))
        assert payload["correlation_id"] == "none"

    def test_context_var_default_dash_maps_to_none_sentinel(self):
        # correlation_id.py's ContextVar default is "-", not "none" — the
        # formatter is responsible for the spec-mandated translation.
        record = _make_record(correlation_id="-")
        payload = json.loads(JsonLinesFormatter().format(record))
        assert payload["correlation_id"] == "none"

    def test_level_is_always_uppercase(self):
        for level, name in (
            (logging.ERROR, "ERROR"), (logging.WARNING, "WARNING"),
            (logging.INFO, "INFO"), (logging.DEBUG, "DEBUG"),
        ):
            record = _make_record(level=level)
            payload = json.loads(JsonLinesFormatter().format(record))
            assert payload["level"] == name

    def test_optional_fields_included_only_when_present(self):
        bare = json.loads(JsonLinesFormatter().format(_make_record()))
        for field in ("endpoint", "status_code", "duration_ms", "ticker",
                      "position_id", "error_type", "error_detail",
                      "job_id", "retry_count"):
            assert field not in bare

        enriched = _make_record(
            endpoint="POST /portfolio/snapshot", status_code=500,
            duration_ms=142, error_type="psycopg2.OperationalError",
        )
        payload = json.loads(JsonLinesFormatter().format(enriched))
        assert payload["endpoint"] == "POST /portfolio/snapshot"
        assert payload["status_code"] == 500
        assert payload["duration_ms"] == 142
        assert payload["error_type"] == "psycopg2.OperationalError"
        assert "ticker" not in payload

    def test_exception_info_populates_error_fields(self):
        try:
            raise KeyError("missing")
        except KeyError:
            record = logging.getLogger("services.position_service").makeRecord(
                "services.position_service", logging.ERROR, __file__, 1,
                "unhandled error", (), __import__("sys").exc_info(),
            )
        payload = json.loads(JsonLinesFormatter().format(record))
        assert payload["error_type"] == "KeyError"
        assert "error_detail" in payload

    def test_message_with_format_args_is_interpolated(self):
        record = logging.getLogger("services.x").makeRecord(
            "services.x", logging.INFO, __file__, 1,
            "value is %s", ("42",), None,
        )
        payload = json.loads(JsonLinesFormatter().format(record))
        assert payload["message"] == "value is 42"


class TestMessageTruncation:
    """ST-11, EPIC-03, v9.6, BLG-BE-120 — structured_logging_standards.md
    §Structured Log Format: `message` is "Free text (max 500 chars)"."""

    def test_message_at_500_chars_is_unchanged(self):
        message = "x" * 500
        record = _make_record(msg=message)
        payload = json.loads(JsonLinesFormatter().format(record))
        assert payload["message"] == message
        assert len(payload["message"]) == 500

    def test_message_under_500_chars_is_unchanged(self):
        message = "short message"
        record = _make_record(msg=message)
        payload = json.loads(JsonLinesFormatter().format(record))
        assert payload["message"] == message

    def test_message_over_500_chars_is_truncated_to_500(self):
        message = "y" * 600
        record = _make_record(msg=message)
        payload = json.loads(JsonLinesFormatter().format(record))
        assert len(payload["message"]) == 500
        assert payload["message"].endswith("...[truncated]")
        assert payload["message"].startswith("y" * 100)

    def test_truncated_message_is_still_valid_json(self):
        record = _make_record(msg="z" * 10_000)
        output = JsonLinesFormatter().format(record)
        payload = json.loads(output)  # raises if not valid JSON
        assert len(payload["message"]) == 500
