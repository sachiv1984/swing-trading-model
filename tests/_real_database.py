"""
Shared helpers for tests that need the real backend/database.py rather than
conftest.py's session-scoped sys.modules["database"] stub (ST-14, BLG-QA-190,
EPIC-03, v9.9).

Before this module, ~29 test files did a bare, module-level
`sys.modules.pop("database", None)` followed by an import, and never put the stub
back. Every test file collected after one of them then saw the real module instead
of the stub. Whether a given test got the stub or the real module therefore
depended on collection order: a reordered run, or a new file sorting earlier,
could silently change behaviour (BLG-QA-178's source incident).

Two patterns, matching BLG-QA-190's categories:

Category A -- the test calls `database.<fn>()` (or loads a service whose only
database dependency is exercised through mocks) and has no FastAPI app:
    database = load_real_database("database_real_for_<test_file>")
A private copy loaded straight from the file. It is never registered in
sys.modules, so nothing else can see it (shared_standards.md §18).

Category B -- the test imports main.app / routers / services whose
`from database import X` bindings must resolve to the real module at import
time, so a private copy cannot be injected:
    with real_database_imports():
        from main import app
Inside the block sys.modules["database"] is a real module. On exit, whatever
was there before (conftest's stub) is put back, so the next file collected
still sees the stub. Modules imported inside the block keep their own
references to the real module, so the tests in that file behave as before.
"""
import importlib
import importlib.util
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import pytest

_DATABASE_PY = Path(__file__).parent.parent / "backend" / "database.py"
_DUMMY_URL = "postgresql://user:pw@localhost:5432/dummy"


def load_real_database(alias):
    """Return a private copy of backend/database.py under module name `alias`.
    Never touches sys.modules["database"]."""
    spec = importlib.util.spec_from_file_location(alias, _DATABASE_PY)
    module = importlib.util.module_from_spec(spec)
    env = {} if os.getenv("DATABASE_URL") else {"DATABASE_URL": _DUMMY_URL}
    with patch.dict("os.environ", env):
        spec.loader.exec_module(module)
    return module


@contextmanager
def real_database_imports(*evict):
    """Expose a freshly imported real `database` module as sys.modules["database"]
    for the duration of the block, then restore the previous entry (conftest's
    stub). `evict` names further modules (e.g. "utils.formatting") to drop
    before the block so they too are re-imported fresh inside it."""
    saved = sys.modules.pop("database", None)
    for name in evict:
        sys.modules.pop(name, None)
    try:
        yield importlib.import_module("database")
    finally:
        if saved is not None:
            sys.modules["database"] = saved
        else:
            sys.modules.pop("database", None)


@pytest.fixture
def restore_database_module():
    """For tests that (re)import the real `database` inside the test body, so that
    `patch("database.<fn>")` and the code under test resolve to the same object:
    put back whatever sys.modules["database"] held before the test (conftest's stub)
    once it finishes. Apply with
        pytestmark = pytest.mark.usefixtures("restore_database_module")
    after importing this fixture into the test module."""
    saved = sys.modules.get("database")
    yield
    if saved is not None:
        sys.modules["database"] = saved
    else:
        sys.modules.pop("database", None)
