"""
Scoped `utils.*` (and `config`) stubs for tests that load a backend module
against stand-ins (ST-46, BLG-QA-209, EPIC-06, v9.12).

Before this module, test_alerts_service.py, test_plan_vs_reality.py and
test_trade_service.py installed module-level stubs for `utils`,
`utils.pricing`, `utils.calculations`, `utils.formatting` and others, and
never removed them during collection. Every file collected after them saw the
stubs. The default alphabetical order happened to pass. In reverse file order,
32 tests failed and tests/test_pagination.py failed to collect ('utils' is not
a package). This is the same leak shape ST-14 removed for
sys.modules["database"] (see tests/_real_database.py).

    with scoped_stub_modules({"utils": _utils_stub, "utils.pricing": _pricing_stub},
                             fresh=("services.trade_service",)):
        import services.trade_service as trade_service

Inside the block, the stubs are in sys.modules and each `fresh` name is
evicted first, so the module under test is imported against the stubs and
not against a copy that some earlier file already imported. On exit, every
stubbed or `fresh` name gets back exactly what it held before. Any other
backend module first imported inside the block (for example
`services/__init__.py`'s own imports, which bound to the stubs) is evicted,
so a later file imports it again against the real `utils`. Third-party
modules first imported inside the block (numpy, pandas, ...) are kept, which
is where this helper differs from a plain `patch.dict(sys.modules, ...)`:
evicting and re-importing C-extension packages is not safe. Modules imported
inside the block keep their own references to the stubs, so the tests in
that file behave as before.

tests/conftest.py's `utils.*` leak guard fails any file or test that leaves
a stub installed.
"""
import sys
from contextlib import contextmanager
from pathlib import Path

BACKEND_DIR = (Path(__file__).resolve().parent.parent / "backend").resolve()


def _is_backend_module(module) -> bool:
    path = getattr(module, "__file__", None)
    if not path:
        return False
    try:
        return Path(path).resolve().is_relative_to(BACKEND_DIR)
    except (OSError, ValueError):
        return False


def stub_utils_package(**submodules):
    """A stand-in `utils` package whose named submodules are the given stubs.
    Its __path__ points at backend/utils, so any submodule not stubbed (for
    example utils.position_lifecycle_states, reached through services/__init__)
    is imported from its real file instead of failing with "'utils' is not a
    package"."""
    import types
    pkg = types.ModuleType("utils")
    pkg.__path__ = [str(BACKEND_DIR / "utils")]
    for name, module in submodules.items():
        setattr(pkg, name, module)
    return pkg


@contextmanager
def scoped_stub_modules(stubs: dict, fresh=()):
    names = set(stubs) | set(fresh)
    saved = {name: sys.modules.get(name) for name in names}
    before = set(sys.modules)
    for name in fresh:
        sys.modules.pop(name, None)
    sys.modules.update(stubs)
    try:
        yield
    finally:
        evicted = [n for n in sys.modules if n not in before and n not in names
                   and _is_backend_module(sys.modules[n])]
        for name in evicted:
            del sys.modules[name]
        for name, original in saved.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original
        # An import binds each dotted module as an attribute of its parent
        # package (`services.trade_service`). Point that attribute back at the
        # restored module, or remove it, so `from services import trade_service`
        # cannot return the copy built against the stubs.
        for name in list(names) + evicted:
            parent_name, _, child = name.rpartition(".")
            parent = sys.modules.get(parent_name) if parent_name else None
            if parent is None:
                continue
            if sys.modules.get(name) is not None:
                setattr(parent, child, sys.modules[name])
            elif hasattr(parent, child):
                try:
                    delattr(parent, child)
                except AttributeError:
                    pass
