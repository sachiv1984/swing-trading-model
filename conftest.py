"""
Repo-root pytest conftest (ST-37, BLG-QA-225, v9.18).

A bare `pytest` (or `backend/.venv/bin/python3 -m pytest`) from the repo root
collects every directory under it. `backend/` sorts before `tests/`, so
`backend/mutmut_pilot_tests/conftest.py` installed its own stub
`sys.modules["database"]` first, and `tests/conftest.py`'s import guard
(ST-14, BLG-QA-190) then failed collection of
`tests/test_add_position_stop_handling.py`. The mutation-testing pilot's tests
are run only from `backend/` (`cd backend && python3 -m mutmut run`; see
`backend/setup.cfg`), so a root run must not collect them.

Why a conftest and not a root `pytest.ini` with `testpaths = tests`: an ini
file at the repo root is found by pytest's upward search from `backend/` too,
which would move the pilot's rootdir from `backend/` (or `backend/mutants/`
inside a mutmut run) to the repo root and change its node IDs. This file is
loaded only when pytest's rootdir is the repo root: with no ini file, pytest
sets `confcutdir` to the rootdir, and a run started in `backend/` has rootdir
`backend/`, so conftest files above it are not read.
"""

# Paths are relative to this file's directory (the repo root).
collect_ignore = ["backend"]
