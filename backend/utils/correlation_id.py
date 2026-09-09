"""
Correlation-ID Context (ST-03, EPIC-01, v9.3, BLG-BE-48)

Provides a request-scoped correlation ID accessible to any log line emitted
during that request's lifecycle, without threading an explicit parameter
through every function call in the router -> service -> database chain.

Uses a contextvars.ContextVar rather than thread-local storage because the
backend is an async FastAPI app — each incoming request runs as its own
asyncio Task, and asyncio Tasks each capture their own copy of the current
context, so a value set here for one request is never visible to a
concurrently-handled request.

Documented in backend_engineering_patterns.md §12.
"""
import contextvars
import logging
import uuid

_correlation_id_var: contextvars.ContextVar = contextvars.ContextVar(
    "correlation_id", default="-"
)


def get_correlation_id() -> str:
    """Return the correlation ID for the current request.

    Returns "-" outside a request context (e.g. app startup, a background
    thread that was not given an explicit copy of the request's context).
    """
    return _correlation_id_var.get()


def set_correlation_id(value: str) -> contextvars.Token:
    """Set the correlation ID for the current context. Returns a Token that
    must be passed to reset_correlation_id() when the request completes."""
    return _correlation_id_var.set(value)


def reset_correlation_id(token: contextvars.Token) -> None:
    """Restore the correlation ID to what it was before set_correlation_id()."""
    _correlation_id_var.reset(token)


def new_correlation_id() -> str:
    """Generate a new correlation ID for a request that did not supply one."""
    return str(uuid.uuid4())


def install_correlation_id_log_record_factory() -> None:
    """Install a LogRecordFactory that stamps every LogRecord with the
    current request's correlation ID (record.correlation_id) at creation
    time, for reference from a logging format string (e.g.
    "%(correlation_id)s").

    A record factory (rather than a logging.Filter attached to specific
    handlers) is used deliberately: a Filter only runs for the handlers it is
    explicitly attached to, and logging.Logger.callHandlers() never consults
    ancestor loggers' own Logger-level filters during propagation — so a
    filter attached only to the handler(s) present at startup would silently
    miss any handler attached later (e.g. pytest's `caplog` fixture, which
    adds its own handler to the root logger per-test). Overriding the record
    factory stamps every record at creation, before any handler exists,
    which every handler then sees regardless of when it was attached.

    Idempotent — safe to call more than once (re-installing is a no-op).
    """
    current_factory = logging.getLogRecordFactory()
    if getattr(current_factory, "_is_correlation_id_factory", False):
        return

    def _factory(*args, **kwargs):
        record = current_factory(*args, **kwargs)
        record.correlation_id = get_correlation_id()
        return record

    _factory._is_correlation_id_factory = True
    logging.setLogRecordFactory(_factory)
