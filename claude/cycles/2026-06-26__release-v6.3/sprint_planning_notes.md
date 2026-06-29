**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-29
**Cycle:** 2026-06-26__release-v6.3

---

# Sprint Planning Notes — 2026-06-26__release-v6.3

## Backlog Slice Source

Original — `claude/cycles/2026-06-26__release-v6.3/stage4_backlog_slice.md`

No amendment sealed. `amended_backlog_slice_path` is empty; original slice is authoritative.

## Carry-Forward Items

Carry-forward items reviewed: 3 items from cycle `2026-06-24__release-v6.2` (source: `lessons_learnt_closure.md`).

| ID | Description | Owner | Target | Action |
|----|-------------|-------|--------|--------|
| FI-P3-01 | Add Playwright strict mode advisory (`{exact: true}` / testid scoping) to Base44 prompt draft §6 Expected outcome (2nd recurrence — template change required) | Director of Quality | v6.3 sprint execution | Action during sprint execution, not a planning blocker |
| FI-P3-02 | Clarify frontend testing gate: when code review of static JSX is accepted substitute for staging sign-off (wording-only vs visual rendering/colour ACs) | Head of Specs Team | v6.3 sprint execution | Action during sprint execution |
| FI-P4-01 | Add CI/infrastructure spec_references convention to execution_prompt.md §3.1.A: for stories with no prior canonical spec, reference the primary file changed as de facto spec reference | Head of Specs Team | v6.3 sprint execution | Action during sprint execution |

All three are process improvement items to be actioned during sprint execution (per cycle_summary.md Outstanding Actions). None are planning blockers.

## Capacity WARN Acknowledgement

Release plan capacity check outcome was `warn`. Per IMP-41: Product Owner acknowledged in sprint_capacity.md. Key facts:
- Per-sprint capacity: 12–14 days (revised 2026-05-27, workforce_capacity.md)
- Sprint 1 effort: ~5.25d (all items) — 38–44% of per-sprint capacity
- Sprint 2 effort: ~6.5d (all items) — 46–54% of per-sprint capacity
- 2-sprint total: 11.75d vs 24–28d combined capacity
- Determination: within capacity; WARN reflects original conservatism, not over-allocation

PO capacity acceptance: all 15 stories (8 firm + 7 conditional) confirmed for sprint inclusion. No items deferred.

## Deferred Items

No items deferred at planning. All 15 ST items (8 firm + 7 conditional) are included in the sealed sprint backlog.

ST-13 (BLG-OPS-79) is included with a within-sprint architecture review gate (see sprint_backlog.md). ST-14 (BLG-OPS-78) is included with a within-sprint production deployment dependency.

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | — | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-08 | ST-07 | Spec precedes implementation | Resolved — ST-07 and ST-08 in same EPIC-02 branch; sequence ST-08 first (spec) then ST-07 (tests use spec) |
| ST-11 (API) | ST-11 (DB schema migration) | Internal story sequencing | Resolved — schema migration must land before API implementation; import_backtest.py can develop in parallel |
| ST-11 (frontend) | ST-11 (API) | Internal story sequencing | Resolved — frontend gates on API completion |
| ST-13 (implementation) | Architecture review of v6.2 scheduler | Within-sprint gate | Open — Infrastructure & Operations Owner must complete review before ST-13 implementation begins |
| ST-14 | Sprint 2 merge to production | Deployment dependency | Open — live measurements require production deployment; execute at end of Sprint 2 cycle |
| EPIC-03 | EPIC-01 + EPIC-02 merge | Sprint sequencing | Resolved — EPIC-03 is Sprint 2 (starts after Sprint 1 merges) |

No circular dependencies detected.

## Execution Sequence

### Sprint 1 — Parallel EPIC-01 and EPIC-02 Branches

**EPIC-01 branch** (`exec/2026-06-26__release-v6.3/EPIC-01`):
1. ST-01 — Fix AI journal summary (autonomous; investigate and resolve silent failure in ai_service.py)
2. ST-02 — Fix R-multiple display (delegated_frontend; observable UI rendering fix)
3. ST-03 — AI endpoint rate limiting (autonomous; backend middleware + 429 responses + openapi.yaml documentation)
4. ST-04 — AI injection risk assessment (autonomous; threat model document)
5. ST-05 — AI disclaimer visibility assessment (autonomous; conditional — if capacity after ST-01–04)
6. ST-06 — API contract review checklist (autonomous; conditional — if capacity after ST-01–04)

**EPIC-02 branch** (`exec/2026-06-26__release-v6.3/EPIC-02`):
1. ST-08 — Strategy signal regression test specification (autonomous; spec document first — ST-07 tests depend on it)
2. ST-07 — Nightly stop computation CI simulation tests (autonomous; implementation per ST-08 spec)
3. ST-09 — AI chat schema validation tests (autonomous; conditional — if capacity after ST-07/08)
4. ST-10 — §13 boundary test suite spec (autonomous; conditional — if capacity after ST-07/08)

**Merge order for Sprint 1:** EPIC-02 → EPIC-01
- EPIC-02 merges first: pure QA/spec work, minimal shared file conflict
- EPIC-01 merges second: touches openapi.yaml, api_contracts, backend/routers/test.py — rebase onto main after EPIC-02 merge before finalising

### Sprint 2 — EPIC-03 Branch

**EPIC-03 branch** (`exec/2026-06-26__release-v6.3/EPIC-03`):
1. ST-11 DB schema migration (backtest_trades, backtest_yearly_performance tables)
2. ST-11 backend API (POST /strategy/benchmark/import, GET /strategy/benchmark/summary, GET /strategy/benchmark/trades)
3. ST-11 import_backtest.py script (parallel to API implementation)
4. ST-11 frontend (3-panel Strategy Benchmark page — gates on API completion)
5. ST-12 — Morning briefing progressive disclosure (delegated_frontend; can run in parallel with ST-11)
6. ST-13 — Scheduler health endpoint (autonomous; architecture review gate must clear first)
7. ST-14 — AI endpoint latency measurement (autonomous; production deployment dependency)
8. ST-15 — Render rollback runbook (autonomous; documentation; no dependencies)

**Merge order for Sprint 2:** EPIC-03 only (single EPIC). Merge to main after Sprint 2 complete.

## Multi-EPIC Execution Notes

**execution_state.json ownership:** EPIC-01 is the designated `execution_state.json` owner. EPIC-01 branch initialises the execution_state.json at Phase 3 STEP 0. EPIC-02 branch must check for existence of execution_state.json before initialising — if found, append the EPIC-02 section rather than overwrite.

**Shared file advisory — Sprint 1:**

| Shared File | EPIC-01 touches? | EPIC-02 touches? | Owner | Advisory |
|-------------|-----------------|-----------------|-------|---------|
| `backend/routers/test.py` | Yes (ST-03 — 429 test) | Yes (ST-07 CI simulation tests, ST-09 schema validation tests) | EPIC-01 (canonical) | EPIC-02 must rebase onto main after EPIC-01 merges, or coordinate to avoid conflict |
| `docs/reference/openapi.yaml` | Yes (ST-03 rate limit documentation) | No | EPIC-01 | No conflict with EPIC-02 |
| `docs/specs/api_contracts/` | Yes (ST-03, ST-06) | No | EPIC-01 | No conflict with EPIC-02 |

**Recommendation:** EPIC-02 should merge first (no openapi.yaml/api_contracts changes). After EPIC-02 merges, EPIC-01 should rebase onto main to pick up any EPIC-02 test.py changes before finalising its own test.py edits.

**Test scenario advisory (LL-v2.0-P4-2):** ST-11 introduces a new Strategy Benchmark page (full 3-panel page, new user-facing controls). EPIC-03 `test_scenarios` status at execution_state.json initialisation should be set to `"pending — QA & Testing Owner to author Playwright test scenarios before next sprint on this domain"`. ST-12 adds expand/collapse interaction — Playwright test scenario AC-05 is already defined in the backlog slice and covers the primary interaction path.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status | Notes |
|---------|----------------|------------------|-------|
| RISK-01 | ST-11 (EPIC-03) | Valid — monitor | BLG-FEAT-53 is L-effort (5.0d). Sequence: DB schema → API → frontend. Import script parallel. Conditional EPIC-03 items (ST-13/14/15) defer if ST-11 overruns Sprint 2 capacity. |
| RISK-02 | ST-04 (EPIC-01) | Valid — accepted | GOV-146 injection risk assessment may surface open items. Mitigation: assessment-only; any remediation items target v6.4 unless P0 critical. |
| RISK-03 | Release-level | Valid — resolved at planning | Capacity WARN: all items within 2-sprint capacity at revised baseline. No active over-allocation. |

## Pre-Sprint Vulnerability Scan

pip-audit unavailable (tool not installed). Advisory: recommend installing pip-audit before Sprint 1 execution begins.

Command to run: `pip install pip-audit && pip-audit -r backend/requirements.txt`

## Pre-Sprint Backlog Advisory

No "Before v6.3 sprint planning" items found in `claude/backlog/backlog.md`.

## Staging-Only AC Designations (LL-v3.9-P3-2)

The following ACs require staging-only evidence (cannot be verified by CI):

| ST-ID | AC-ID | Reason |
|-------|-------|--------|
| ST-02 | AC-01, AC-02, AC-03 | Delegated_frontend UI rendering fix — visual display of R-multiple requires staging run or Playwright E2E test against running app |
| ST-11 | AC-06 | POST /strategy/benchmark/import upsert verification requires real CSV data and production-like environment |
| ST-11 | AC-07 | `import_backtest.py` reading CSVs from `production_results/` requires production data files not available in CI |
| ST-14 | AC-01 | Minimum 5 authenticated warm requests against production — requires production deployment |
| ST-14 | AC-02 | p50/p95 population requires production measurements |
| ST-14 | AC-03 | Regression threshold documentation requires production measurements |

Pre-staging backlog filing obligation: Any staging-only AC deferred to post-merge staging must have a backlog item filed via /backlog-add before the PR opens (CLAUDE.md §2). This is a hard gate blocking the PR. Sprint execution engine must enforce this at delegation record creation.

## Outstanding Actions

| Action | Owner | Blocker? |
|--------|-------|---------|
| BLG-BE-39 and BLG-FE-79 Provisional-Target: update from `v6.2` → `v6.3` in backlog.md | Product Owner | No — advisory from release planning |
| ST-13 architecture review of v6.2 scheduler before implementation | Infrastructure & Operations Owner | No at seal; Yes before ST-13 implementation begins |
| Action FI-P3-01: Base44 prompt draft §6 strict mode advisory | Director of Quality | No — during sprint execution |
| Action FI-P3-02: Frontend testing gate clarification | Head of Specs Team | No — during sprint execution |
| Action FI-P4-01: CI/infra spec_references convention in execution_prompt.md §3.1.A | Head of Specs Team | No — during sprint execution |
| pip-audit scan before Sprint 1 execution | Head of Engineering | No — advisory |

No actions marked Blocker? Yes at seal time.
