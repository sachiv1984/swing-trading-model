"""
ST-02 (BLG-BE-107, EPIC-01, v9.0): root logging configuration.

Production runs `uvicorn main:app --host 0.0.0.0 --port $PORT`
(render.yaml's startCommand) with no --log-config/--log-level flag, and
nothing else in backend/ configured the root logger — every
logger.info(...) call in application code (logging.getLogger(__name__),
used throughout backend/services/) was silently filtered out before ever
reaching a handler. Root cause verified in
docs/ops/api_performance_baseline.md §36.5 (services/si05_digest_service.py's
"SI-05 digest sent..." line confirmed genuinely absent from a real
post-merge invocation).

These tests verify the fix (backend/main.py's logging.basicConfig() call)
in isolation from actually running a live uvicorn process — the AC's "a
real post-deploy production invocation confirms ... captured in Render
logs" requires live Render dashboard access this sandbox does not have
(delegated; see execution_state.json ST-02).

Each check below runs in its own subprocess rather than importing `main`
in-process: `main` holds the live, singleton FastAPI `app` instance that
every other test file in this suite imports and shares
(`CLIENT = TestClient(main.app)`-style module-level state, patched via
`patch("main.<name>", ...)`). Forcibly re-importing `main` in-process (via
`sys.modules.pop("main")`) creates a second, distinct module object —
`unittest.mock.patch("main.get_settings", ...)` in another test file would
then patch that second object while the original `TestClient` still holds
a reference to the first, silently defeating the patch and causing
unrelated tests elsewhere in the suite to hit a real (refused) DB
connection. A subprocess is fully isolated from this session's own
`sys.modules`, so it cannot corrupt any other test's module state.
"""
import subprocess
import sys
import textwrap
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"

# Simulates the real production startup order: uvicorn's CLI calls
# Config.configure_logging() (which applies uvicorn.config.LOGGING_CONFIG
# via dictConfig) before the app module (main.py) is ever imported.
_SCRIPT = textwrap.dedent("""
    import logging
    import logging.config
    import os
    os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test_stub")

    import uvicorn.config
    logging.config.dictConfig(uvicorn.config.LOGGING_CONFIG)

    import main  # noqa: F401  (triggers main.py's logging.basicConfig() call)

    root = logging.getLogger()
    app_logger = logging.getLogger("services.si05_digest_service")

    print("root_level=%d" % root.level)
    print("root_handler_count=%d" % len(root.handlers))
    print("app_logger_effective_level=%d" % app_logger.getEffectiveLevel())
    print("app_logger_propagate=%s" % app_logger.propagate)
    print("uvicorn_propagate=%s" % logging.getLogger("uvicorn").propagate)
    print("uvicorn_access_propagate=%s" % logging.getLogger("uvicorn.access").propagate)
    print("uvicorn_error_handler_count=%d" % len(logging.getLogger("uvicorn.error").handlers))

    # Re-run the same basicConfig() call path directly, simulating a second
    # module attempting to configure logging again — must be a no-op.
    handlers_before = len(root.handlers)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    print("handlers_stable_on_reconfigure=%s" % (len(root.handlers) == handlers_before))
""")


def _run_isolated() -> dict:
    result = subprocess.run(
        [sys.executable, "-c", _SCRIPT],
        cwd=str(BACKEND_DIR),
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, (
        f"isolated main.py import failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    out = {}
    for line in result.stdout.strip().splitlines():
        k, _, v = line.partition("=")
        out[k] = v
    return out


class TestRootLoggingConfig:
    def test_root_logger_configured_at_info_with_a_handler(self):
        out = _run_isolated()
        assert out["root_level"] == "20"  # logging.INFO
        assert int(out["root_handler_count"]) >= 1

    def test_application_logger_reaches_root_handler(self):
        """A logging.getLogger(__name__)-style logger from application code
        (e.g. services/si05_digest_service.py's pattern) must now have an
        effective level that lets INFO records through, and must propagate
        up to root (default, unless something explicitly disables it)."""
        out = _run_isolated()
        assert int(out["app_logger_effective_level"]) <= 20
        assert out["app_logger_propagate"] == "True"

    def test_uvicorn_loggers_do_not_propagate_to_root_no_duplicate_lines(self):
        """uvicorn's default LOGGING_CONFIG sets propagate: False on both
        "uvicorn" and "uvicorn.access" — this must remain true after
        main.py's basicConfig() call, or every uvicorn access/error line
        would print twice (once via uvicorn's own handler, once via root's
        new handler)."""
        out = _run_isolated()
        assert out["uvicorn_propagate"] == "False"
        assert out["uvicorn_access_propagate"] == "False"
        # uvicorn.error has no handler of its own and propagates to its
        # parent "uvicorn" logger (which does have propagate=False),
        # never reaching root directly either way.
        assert out["uvicorn_error_handler_count"] == "0"

    def test_basicconfig_is_a_no_op_if_root_already_has_a_handler(self):
        """logging.basicConfig() only takes effect if the root logger has
        no handlers yet (without force=True) — confirms a second
        configuration attempt can't silently stack duplicate handlers."""
        out = _run_isolated()
        assert out["handlers_stable_on_reconfigure"] == "True"
