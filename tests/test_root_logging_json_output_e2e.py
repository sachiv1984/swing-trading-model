"""
End-to-end confirmation that backend/main.py's wired root logger actually
emits JSON in situ (ST-10, BLG-QA-179, EPIC-03, v9.8).

tests/test_root_logging_config.py confirms the root logger is configured
(level, handler count, propagation) but never captures and parses an
actually-emitted log line -- so a regression that reverted
`JsonLinesFormatter` to a plain-text `Formatter` (or any other non-JSON
formatter) on the handler `main.py` installs would pass every existing
check in that file while silently breaking every downstream JSON log
consumer. This test closes that gap by running main.py's real import path
in a subprocess (same isolation rationale as test_root_logging_config.py --
`main` holds the live singleton `app` other test files patch in-process),
emitting one real log record through the fully-wired root logger, and
json-parsing the captured line.
"""
import json
import subprocess
import sys
import textwrap
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"

_SCRIPT = textwrap.dedent("""
    import logging
    import os
    os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test_stub")

    import main  # noqa: F401  (triggers main.py's logging.basicConfig() call)

    logger = logging.getLogger("services.some_module")
    logger.info("ST-10 e2e JSON logging probe")
""")


def _emit_one_log_line() -> str:
    result = subprocess.run(
        [sys.executable, "-c", _SCRIPT],
        cwd=str(BACKEND_DIR),
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, (
        f"isolated main.py import + log emit failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    # StreamHandler's default stream is stderr.
    lines = [line for line in result.stderr.strip().splitlines() if "ST-10 e2e JSON logging probe" in line]
    assert len(lines) == 1, f"expected exactly one matching log line, got: {result.stderr!r}"
    return lines[0]


class TestRootLoggerEmitsJsonInSitu:
    def test_emitted_log_line_is_valid_json(self):
        line = _emit_one_log_line()
        try:
            json.loads(line)
        except json.JSONDecodeError as exc:
            raise AssertionError(
                f"root logger's emitted line is not valid JSON (formatter reverted to "
                f"plain text or replaced?): {line!r} ({exc})"
            )

    def test_emitted_json_carries_the_structured_log_fields(self):
        """Per docs/specs/structured_logging_standards.md §Structured Log
        Format -- confirms JsonLinesFormatter specifically, not just any
        JSON-producing formatter (e.g. a bare `json.dumps({"message": ...})`
        with none of the mandated fields would satisfy the previous check
        alone)."""
        line = _emit_one_log_line()
        payload = json.loads(line)
        assert payload["level"] == "INFO"
        assert payload["message"] == "ST-10 e2e JSON logging probe"
        assert payload["service"] == "services.some_module"
        assert "timestamp" in payload
        assert "correlation_id" in payload
