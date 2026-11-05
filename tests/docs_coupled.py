"""
Docs-coupled test selection for governance-only and docs-only CI runs.

ST-31 (EPIC-05, v9.15, BLG-OPS-191; Product Owner ruling ESC-EXEC-20261105-05).
On a push or PR that changes only `claude/**` and `docs/**`, the CI Pytest
suite's Phase A runs `pytest tests/ --docs-coupled-only` instead of its usual
module list, and the other code-test suites skip. This module decides which
test files are "docs-coupled": any file whose source could read a file under
`claude/` or `docs/`, so a governance-only change still runs the tests that
check governance and documentation content (for example
`test_strategy_version_registry.py` against `strategy_rules.md`).

The rule is a static scan, re-derived on every run, so a new test that reads a
document is picked up without a list to maintain (the same approach as
`conftest.py`'s database-stub scan, BLG-QA-73). It errs towards including a
file: a false positive only costs run time.

A file is docs-coupled if its source has any of:
  - `claude` or `docs` as a quoted string or a path component
    ("claude/...", 'docs', / "docs" /, Path(...) / "claude");
  - a quoted `.md` file name;
  - a reference to the repository's `scripts` directory (most scripts there
    read governance or spec files).
"""

import re
from pathlib import Path

_PATTERN = re.compile(
    r"""(["'/])(claude|docs)(["'/])"""   # "claude/", 'docs', /docs/
    r"""|\.md["']"""                     # "backlog.md", 'data_model.md'
    r"""|\bscripts[/."']""",             # scripts/x.py, scripts.x, "scripts"
)

_cache = {}


def is_docs_coupled(path) -> bool:
    """True if the test file at `path` may read a file under claude/ or docs/."""
    path = Path(path)
    key = str(path)
    if key not in _cache:
        try:
            source = path.read_text(encoding="utf-8")
        except OSError:
            source = ""
        _cache[key] = bool(_PATTERN.search(source))
    return _cache[key]
