**Owner:** QA Lead; Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Complete
**Last Updated:** 2026-09-29 (ST-15, BLG-QA-184, EPIC-03, v9.8 — BLG-QA-198 resolved, real mutation score recorded); prior — 2026-09-29 (initial investigation, blocked on BLG-QA-198)
**Source:** ST-15 (BLG-QA-184, EPIC-03, v9.8 sprint execution)

---

# Mutation-Testing Pilot — Sizing Calculator and Stop Ratchet

## Scope (per BLG-QA-184)

- Target modules: `backend/services/sizing_service.py` (strategy_rules.md §4.1 Position Sizing Calculator) and `backend/utils/calculations.py::calculate_trailing_stop` (§7.2/§7.3 stop-ratchet rule).
- Tool: `mutmut` 3.8.0 (Python mutation testing), installed and used ad hoc for this pilot only — not adopted as a pinned dependency, uninstalled again after the run.
- AC: baseline mutation score computed; survivors triaged.

## BLG-QA-198 — environmental blocker, now resolved

The first attempt (`source_paths=backend` invoked from the repo root) failed: mutmut's mutant "keys" are derived from each file's path relative to the process's cwd at mutation-generation time (`mutmut/utils/format_utils.py::get_mutant_name`, which strips only a literal `"src."` prefix), while this repo's `tests/conftest.py` puts `backend/` itself on `sys.path` so application code imports as `services.X`/`utils.X` (bare), never `backend.services.X`. The two naming schemes never lined up, so mutmut reported every mutant "not exercised" regardless of real coverage and aborted before running any of them.

**Fix applied (option (a) from the original investigation):** ran mutmut with `cwd=backend/` instead of the repo root (`backend/setup.cfg`'s `[mutmut]` section, `source_paths = .`) — with cwd already at `backend/`, a mutated file's path relative to cwd is exactly `services/sizing_service.py` → key `services.sizing_service...`, matching the bare import convention with no prefix-stripping needed at all. This sidesteps needing to change `tests/conftest.py` (option (b), which would have touched the whole suite's collection path) entirely.

The remaining piece was a working, isolated test entry point: `tests/conftest.py`'s own `sys.path`/DB-stub setup is computed relative to its own file location in a way that breaks once copied to a different relative depth under `mutants/`. Rather than fight that, this pilot uses its own standalone conftest at `backend/mutmut_pilot_tests/conftest.py`, which replicates the same DB-stub mechanism (AST-scanning `backend/` for `from database import (...)` names, same approach as the real `tests/conftest.py`, BLG-QA-73) but computes its `sys.path` insert from its own location one level inside `backend/`, so it resolves correctly both when run directly (`cwd=backend/`) and when copied wholesale into mutmut's `mutants/` tree (since `source_paths="."` copies all of `backend/`, including this pilot directory, automatically).

`BLG-QA-198` closed — see `claude/backlog/backlog.md`.

## Test coverage added

`backend/mutmut_pilot_tests/test_pilot.py` (17 tests): `calculate_trailing_stop` (9 cases covering §7.2 profitable/losing paths, the breakeven floor, the §7.3 ratchet, default settings-key fallback values, and explicit non-default multiplier values), `_floor_4dp` (3 cases), and `size_position` end-to-end (5 cases, golden vectors adapted from `tests/golden_outputs.json` PS-01/02/03 plus an invalid-input and a cash-insufficient case).

## Mutation score (baseline)

Run: `cd backend && python3 -m mutmut run` (899 total mutants generated across the two `only_mutate`-scoped files; 896 resolved, all pytest-selection-covered ones settled in this run).

**Overall raw totals across both files (896 mutants):** 208 killed, 275 survived, 412 no-tests, 1 timeout. These file-level totals are heavily diluted by functions in `calculations.py` outside this story's actual scope (`calculate_exit_proceeds`, `calculate_realized_pnl`, `should_exit_position`, etc. — `only_mutate` is file-granular, not function-granular, so every function in a targeted file gets mutated even though only `calculate_trailing_stop` was in scope). The meaningful, per-function scores:

| Function | Killed | Survived | Total | Score |
|---|---|---|---|---|
| **`calculate_trailing_stop`** (§7.2/§7.3 stop ratchet — full story scope) | 35 | 0 | 35 | **100%** |
| `_floor_4dp` (§4.1.3 rounding) | 5 | 0 | 5 | **100%** |
| `size_position` (§4.1 main sizing orchestrator) | 127 | 119 | 246 | 51.6% |
| `_apply_concentration_adjustment` (ST-04, sector concentration) | 7 | 118 (+1 timeout) | 126 | 5.6%* |
| `_calculate_heat_impact` (ST-05, portfolio heat) | 0 | 20 | 20 | 0%* |

**\*Pilot-scope artifact, not a real gap** — see Survivor Triage below.

## Survivor triage

**`calculate_trailing_stop` — fully killed after 2 fix rounds (real findings, both fixed in this pilot's own test file):**
- Initial run: 13/35 survived. Inspection (`mutmut show <id>`) found two genuine categories: (1) every test case supplied an explicit `atr_multiplier_trailing`/`_initial` value that happened to equal the function's own default (2.0/5.0), so a mutant that mangled the settings key name or the default value fell back to the same-valued default and produced an identical result; (2) one mutant deleted `new_stop` entirely from `trailing_stop = max(current_stop, new_stop, entry_price)` — undetected because every existing case had `current_stop` or `entry_price` already dominating the max, so removing `new_stop` from consideration never changed the observable output.
- Fix: added `test_new_stop_actually_participates_in_the_ratchet_max` (constructs a case where `new_stop` is genuinely the largest of the three) and `test_explicit_{trailing,initial}_multiplier_value_and_key_name_both_matter` (uses multiplier values that differ from the defaults, so a key-name or default-value mutation becomes observable). Re-run: 35/35 killed.

**`size_position` — 119 survivors, genuine coverage gaps, not fixed in this pilot (follow-up filed):** this pilot's 5 cases only exercise the UK market path with a handful of settings/cash combinations. Untested by this pilot (and therefore contributing real survivors): the US-market FX-rate branch, `size_batch_inv_vol`'s entire inverse-volatility path (a separate function, also under `only_mutate` since it's file-scoped), and several `estimated_cost`/`estimated_fees` rounding-boundary combinations. **Filed as `BLG-QA-199`** (see backlog) rather than expanding this pilot's own test file indefinitely — `size_position`'s US-market and batch-sizing paths already have their own dedicated coverage elsewhere (`tests/test_signal_sizing.py` for `size_batch_inv_vol`) not included in this standalone pilot run; `BLG-QA-199` tracks confirming that coverage's own mutation score separately rather than assuming it from line coverage alone.

**`_apply_concentration_adjustment` / `_calculate_heat_impact` — near-zero score is this pilot's own test-design choice, confirmed not a real production gap:** every `size_position` case in this pilot's test file passes `ticker=None` (matching `tests/golden_outputs.json`'s PS-01/02/03 vectors, which predate the ST-04 concentration feature), so `_apply_concentration_adjustment` short-circuits at its very first guard clause (`if not ticker or suggested_shares <= 0: return default`) — no mutation deeper in the function can ever be observed. Likewise, `_calculate_heat_impact` is deliberately isolated from live heat calculation (`calculate_prospective_heat` mocked to always return `{"valid": False}`) to keep this pilot's scope to sizing arithmetic — so nothing downstream of that check is ever exercised.

Confirmed via a real coverage run rather than assumed: `python3 -m coverage run --source=backend -m pytest tests/test_sizing_concentration.py tests/test_sizing_heat_impact.py` (the repo's actual dedicated coverage for these two features) reports **61% line coverage of `sizing_service.py`**, with the missing lines concentrated in `size_position`'s own error/batch paths, not in `_apply_concentration_adjustment`'s or `_calculate_heat_impact`'s core logic — confirming these two functions already have real, ticker-driven test coverage in the main suite; this pilot's low per-function mutation score for them reflects this pilot's own narrow test file, not the codebase's actual state. No follow-up filed for these two functions on this basis.

**1 timeout** (`_apply_concentration_adjustment__mutmut_100`) — not investigated further in this pilot; noted for whoever next runs a full (not scoped-to-two-files) mutation pass, since a mutation-induced infinite loop or pathological slowdown is itself sometimes an interesting finding, but pinning down which specific mutation caused it is out of this pilot's scope.

## Reproducing this pilot

```bash
cd backend
python3 -m pip install mutmut   # not a pinned dependency; install ad hoc
python3 -m mutmut run           # uses backend/setup.cfg's [mutmut] section
python3 -m mutmut results --all true
python3 -m pip uninstall -y mutmut libcst textual setproctitle linkify-it-py mdit-py-plugins
```

`backend/mutmut_pilot_tests/` (conftest + test file) and `backend/setup.cfg` are committed so this is fully reproducible without re-deriving the cwd/import-path fix.
