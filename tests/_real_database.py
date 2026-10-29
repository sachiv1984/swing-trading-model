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

Known limit: real-bound modules outlive the importing file (decision recorded
by ST-27, BLG-QA-211, EPIC-04, v9.13; ESC-EXEC-20261028-01).
Only sys.modules["database"] is restored on exit. Every other module first
imported inside a real_database_imports() block -- main, the routers, and the
services they import -- stays in sys.modules for the rest of the session,
holding the real module through its module-level `from database import X`
names (or `import database`, as routers/strategy_benchmark.py does). A later
file that imports one of those modules gets that cached, real-bound copy, not a
fresh stub-bound one. Modules already imported earlier with the stub are not
re-imported inside the block, so they stay stub-bound: the session holds a mix,
decided by collection order (in a full run today the first block run at
collection is in
tests/test_api_call_attribution.py, which sorts before
tests/test_api_contracts.py; any new file sorting earlier changes it). A
function-level `from database import X` looks the name up at call time and
gets the stub.
This is accepted, not fixed, because:
- Evicting them would make a later patch("services.x.name") re-import a fresh
  services.x, so the patch would land on a module object that main's routers
  do not call.
- Making every Category B file share one session-scoped app (so nothing is
  imported per file) would touch about 30 files and their patch() targets.
To stay independent of collection order, a test that calls into a service or
router must patch the names that module uses, at the module level
(patch("services.x.get_y") or patch.object(module, "get_y")). For a
function-level `from database import`, patch("database.get_y"), which hits
conftest's stub at call time. A test must never
assume conftest's stub sits behind a service's database calls: in a full run
it may be the real module. conftest.py's leak guard checks only
sys.modules["database"] itself and does not detect this case.
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
