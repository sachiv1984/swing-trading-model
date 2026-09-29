**Owner:** QA Lead; Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Blocked — environmental, investigation complete
**Last Updated:** 2026-09-29 (ST-15, BLG-QA-184, EPIC-03, v9.8 — initial investigation)
**Source:** ST-15 (BLG-QA-184, EPIC-03, v9.8 sprint execution)

---

# Mutation-Testing Pilot — Sizing Calculator and Stop Ratchet

## Scope (per BLG-QA-184)

- Target modules: `backend/services/sizing_service.py` (strategy_rules.md §4.1 Position Sizing Calculator) and `backend/utils/calculations.py::calculate_trailing_stop` (§7.2/§7.3 stop-ratchet rule).
- Tool: `mutmut` 3.8.0 (Python mutation testing).
- AC: baseline mutation score computed for v9.5; per-cycle survivor triage.

## What was done

1. Installed `mutmut` 3.8.0 into the backend venv and confirmed it runs.
2. Identified the exact target files and confirmed their existing fast test coverage: `tests/test_golden_outputs.py`, `tests/test_signal_sizing.py`, `tests/test_sizing_heat_impact.py`, `tests/test_sizing_concentration.py`, `tests/test_trailing_stop_breakeven_floor.py`, `tests/test_money_arithmetic_golden.py` (full suite of these six: <1s).
3. Configured a scoped `[mutmut]` run (`source_paths=backend`, `only_mutate` limited to the two target files, `pytest_add_cli_args_test_selection` limited to the six files above).
4. `backend/.venv` (403MB) was temporarily relocated out of `backend/` for the run (mutmut's file-copy walks `source_paths` with no directory-exclude option, so leaving the venv in place would have copied it wholesale on every invocation) — moved back immediately after this investigation; **no residual change to the repo from this step** (`backend/.venv` is git-ignored either way).
5. Mutant generation succeeded (2 files mutated, 99 mutants). The run then hard-stopped before executing any mutant against the test suite.

## Blocker found (environmental, not a defect in the target modules)

`mutmut run` failed with:

```
Stopping early, because tests recorded trampoline hits but none match any mutant key.
It looks like tests import the source under a different module path than mutmut sees
from the file path.
Recorded keys (e.g.): ['services.sizing_service.x__apply_concentration_adjustment', ...]
Expected keys (e.g.): ['backend.services.sizing_service.x__apply_concentration_adjustment', ...]
```

**Root cause:** mutmut 3.x only auto-adds `mutants/.`, `mutants/src`, or `mutants/source` to `sys.path` for the mutated copy (hardcoded in `mutmut/utils/file_utils.py::setup_source_paths` — not configurable via `source_paths`). This repo's test suite instead relies on `tests/conftest.py` inserting `backend/` itself onto `sys.path` (`sys.path.insert(0, ".../backend")`), so every test imports backend modules as `services.sizing_service` / `utils.calculations` (bare, backend-relative — the convention used throughout `tests/*.py`), never as `backend.services.sizing_service`. With `source_paths=backend`, mutmut computes its mutant keys using the `backend.*`-qualified form, which never matches what conftest's own `sys.path` setup actually produces at test-run time — so mutmut reports every mutant "not exercised" regardless of real coverage, and aborts before running any of them (a correctness safeguard on mutmut's part, not a hang or crash).

This is a repo-layout mismatch, not a problem with the target modules or their tests: `tests/test_golden_outputs.py` and `tests/test_trailing_stop_breakeven_floor.py` demonstrably exercise both modules today (32 passing tests, confirmed above) — mutmut simply cannot yet observe that from outside the repo's `backend/`-relative import convention.

**Two viable fixes, neither attempted in this pilot (out of scope for a first investigation pass):**
- (a) Run mutmut with `cwd=backend/` and a relocated/aliased `tests/` copy alongside it (`also_copy = ../tests`, `pytest_add_cli_args_test_selection` pointed at `../tests/...`), so the mutated copy's root matches the `services.*`/`utils.*` import convention the tests already use. Workable, but every path in the mutmut config becomes cwd-relative to `backend/` rather than the repo root, which is easy to get subtly wrong (confirmed only conceptually here, not executed).
- (b) Change `tests/conftest.py`'s `sys.path` setup to add the repo root instead of `backend/`, and repoint the whole suite's imports to `backend.services.X` style. Correct fix for mutmut-compatibility long-term, but touches the shared test-collection path for the entire suite (hundreds of files) — well outside a QA pilot's write scope, and a decision for whoever owns `tests/conftest.py`'s conventions, not something to change silently as a side effect of adding a new dev tool.

## Disposition

No mutation score or survivor list could be produced this session — the blocker above is structural, not a quick fix, and forcing option (b) to unblock a P3 pilot would risk the entire test suite's collection path for hundreds of unrelated tests. Filed as a follow-on rather than silently deferred: **`BLG-QA-193`** (mutmut source-path compatibility fix, see `claude/backlog/backlog.md`) tracks resolving one of the two options above; this pilot resumes once that lands. `mutmut` itself was uninstalled from the backend venv after this investigation (not adopted as a dependency yet — nothing to pin in `requirements.txt`).
