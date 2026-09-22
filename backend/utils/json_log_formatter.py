"""
JSON Lines log formatter (ST-02, EPIC-01, v9.5, BLG-BE-112).

Emits one JSON object per log record per
docs/specs/structured_logging_standards.md §Structured Log Format. Replaces
the plain-text format string backend/main.py used previously (documented as
DEV-v9.3-ST03-01 in that spec's Known Deviations section prior to this
story).
"""
import json
import logging
from datetime import datetime, timezone

# Optional domain fields per the spec's §Structured Log Format table —
# included only when actually present on the record (e.g. passed via
# logger.info(..., extra={...})). None of these are fabricated if absent.
_OPTIONAL_FIELDS = (
    "endpoint", "status_code", "duration_ms", "ticker",
    "position_id", "error_type", "error_detail", "job_id", "retry_count",
)

# structured_logging_standards.md §Structured Log Format: `message` is
# "Free text (max 500 chars)". Truncated (ST-11, EPIC-03, v9.6, BLG-BE-120)
# — previously unenforced, so a long message (e.g. an unsanitised exception
# string landing in `message` instead of `error_detail`) could exceed the
# spec's own limit in the emitted JSON.
_MAX_MESSAGE_LENGTH = 500
_TRUNCATION_SUFFIX = "...[truncated]"


class JsonLinesFormatter(logging.Formatter):
    """Formats each LogRecord as a single-line JSON object (NDJSON)."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(
            record.created, tz=timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # record.correlation_id is stamped by
        # utils.correlation_id.install_correlation_id_log_record_factory().
        # Its own default is "-" outside a request context; the spec's
        # allowed values for this field are a UUID v4 or the literal
        # string "none", so translate at the format boundary rather than
        # changing the context-var's internal default (which other code —
        # e.g. tests/test_correlation_id_propagation.py — asserts is "-").
        correlation_id = getattr(record, "correlation_id", "-")
        if correlation_id in (None, "-"):
            correlation_id = "none"

        message = record.getMessage()
        if len(message) > _MAX_MESSAGE_LENGTH:
            message = message[: _MAX_MESSAGE_LENGTH - len(_TRUNCATION_SUFFIX)] + _TRUNCATION_SUFFIX

        payload = {
            "timestamp": timestamp,
            "level": record.levelname,
            "correlation_id": correlation_id,
            # "service" is the originating module's dotted logger name
            # (e.g. "services.position_service", "routers.screener",
            # "main") rather than the 5-value enum this field's row
            # originally illustrated — see structured_logging_standards.md
            # §Structured Log Format Changelog entry for this story.
            "service": record.name,
            "message": message,
        }

        for field in _OPTIONAL_FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value

        if record.exc_info:
            payload.setdefault(
                "error_type",
                record.exc_info[0].__name__ if record.exc_info[0] else "none",
            )
            payload.setdefault("error_detail", self.formatException(record.exc_info))

        return json.dumps(payload, ensure_ascii=False)
