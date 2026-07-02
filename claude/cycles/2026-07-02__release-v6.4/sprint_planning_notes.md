**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-02
**Cycle:** 2026-07-02__release-v6.4

# Sprint Planning Notes — 2026-07-02__release-v6.4

## Backlog Slice Source

Original — `claude/cycles/2026-07-02__release-v6.4/stage4_backlog_slice.md`. `amended_backlog_slice_path` is empty in both `.claude_current_state.json` and `state.json` — no amendment sealed for this cycle.

## Deferred Items

None. All 13 candidate items (ST-01–ST-13) fit within confirmed capacity (7.8 of ~12–14 days) with no blocked dependencies or missing owners — all classified `include` at STEP 3. Nothing returns to the backlog slice for a future sprint.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-13 | ST-08 | Internal (sequencing, not a hard blocker) | Resolved — same-EPIC ordering only |
| ST-08 (backend layer) | — | Internal (RISK-05) | Resolved — story-internal sequencing: endpoint → contract → test.py → frontend panel, per `/commit-check` |
| ST-03 | — | None | N/A |
| All other items | — | None identified | N/A |

**Rationale for ST-13→ST-08:** Design gate record notes ST-08 introduces a new "Panel 0 — Open Positions" placed *before* the existing Panel 1, while explicitly preserving Panel 1/2/3 numbering that ST-13's ACs reference (AC-03 Panel 1 placeholder, AC-04 Panel 3 toggle modes). No renumbering occurs, so this is not a hard blocker, but ST-08 should merge first within EPIC-03 to avoid ST-13's Playwright selectors being authored against a DOM structure that then shifts under a concurrently-landing panel addition.

No circular dependencies detected.

## Execution Sequence

1. **EPIC-01 — Backend Correctness & Security Hardening** (autonomous, no dependencies, contains the mandatory P1 fast-track item)
   1. ST-01 (BLG-BE-40) — P1 mandatory correctness fix
   2. ST-02 (BLG-SEC-01)
   3. ST-03 (BLG-SEC-02)
2. **EPIC-02 — Governance & Audit Remediation** (autonomous, no dependencies)
   1. ST-04 (BLG-GOV-150)
   2. ST-05 (BLG-GOV-151)
   3. ST-06 (BLG-GOV-152)
   4. ST-07 (BLG-GOV-153)
3. **EPIC-03 — Strategy Benchmark Enhancement & UX/QA Polish** (delegated_frontend items; Design Gate already Passed)
   1. ST-08 (BLG-FEAT-54) — merge first (see Dependency Map)
   2. ST-09 (BLG-UX-01)
   3. ST-10 (BLG-UX-02)
   4. ST-11 (BLG-OPS-82)
   5. ST-12 (TEST-GAP-EPIC-01)
   6. ST-13 (TEST-GAP-EPIC-03) — merge after ST-08

EPIC-01 and EPIC-02 (fully autonomous) are sequenced ahead of EPIC-03 (mixed autonomous/delegated_frontend) per §3.1's "group autonomous before delegated" guidance, and because ST-01 is the mandatory P1 STEP 8.0 fast-track item.

### Multi-EPIC Execution Notes (Required — 3 EPICs in scope)

- **`execution_state.json` owner: EPIC-01.** Designated as first in execution order. EPIC-02 and EPIC-03 branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.
- **Shared file ownership advisory:** No source files were identified that more than one EPIC modifies this sprint. EPIC-01 touches `signal_service.py`, `database.py`/`ticker_universe_service`, and the `ai_chat()` router only. EPIC-02 touches governance/prompt files exclusively (`OPERATIONAL_GUIDE.md`, `shared_standards.md`, `execution_prompt.md`, `amendment_cycle_prompt.md`, `team_charter.md`, `claude/audit.py`, `metrics_definitions_analytics_owner.md`, README.md, CLAUDE.md, `scored_initiatives.md`). EPIC-03 touches `strategy_benchmark.md` spec, `AiDailyBriefing.js`, `AiChatWidget.js`, a new `backtest_open_positions` table, `openapi.yaml`, and `docs/ops/api_performance_baseline.md`. No overlap across EPICs — no rebase-before-merge advisory required at the cross-EPIC level.
  - **Intra-EPIC note (EPIC-02):** ST-06 and ST-07 both touch `shared_standards.md` (different sections — §7 append-only guard vs §13 dry-run table). Sequence ST-06 before ST-07 within EPIC-02 to avoid a same-file merge conflict inside the branch.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 / ST-01 | Valid — verify parity via Ticker Universe Management before merge (flagged as staging-only evidence below) |
| RISK-02 | EPIC-01 / ST-02, ST-03 | Valid — test validation regex against full current `ticker_universe` active list before deploy |
| RISK-03 | EPIC-02 / ST-06 | Valid — FI-P3-01 fold-in documented explicitly in ST-06 AC-05 and `decisions--2026-07-02__release-v6.4.md` |
| RISK-04 | EPIC-02 / ST-04–ST-07 | Valid — run `/governance-drift` before each governance commit in EPIC-02 (4 governance-file-editing stories in one EPIC) |
| RISK-05 | EPIC-03 / ST-08 | Valid — sequence backend endpoint → contract → `test.py` registration before frontend panel work; use `/commit-check` before each commit |
| RISK-06 | EPIC-03 / ST-08, ST-09, ST-10 | **Resolved this session** — Design Gate ran (`design_gate.md`, 2026-07-02) and returned PASSED, 13/13 items cleared, 0 blocked. No longer a live risk to sprint planning; retained here as a closed reference. |

No risk has materialised since release planning. All mitigations remain valid as stated.

## Pre-Sprint Vulnerability Scan

`pip-audit` is **unavailable** in this environment (`pip-audit: command not found`). Advisory only — does not block sprint planning. Recommend installing `pip-audit` before sprint execution begins so STEP -1's mandatory scan can run cleanly at the next governed routine invocation.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Resolve `cycle_summary.md` Pre-sprint Planning Required Decision — RISK-06 Design Gate clearance | Head of UX & Design | Yes — **Resolved**: `run design-gate` completed 2026-07-02, status PASSED, all 3 UI-facing items (ST-08/09/10) cleared. Not a blocker to seal. |
| Install `pip-audit` in the execution environment | Infrastructure & Operations Owner | No — advisory |
| DF-06 minimum-scenario check: ST-08 has 4 ACs (below the ≥5 threshold that mandates a Playwright scenario stub in the delegation spec per DF-06) — no stub is strictly required, but recommended given RISK-05/RISK-06 profile and the staging-only AC noted below | QA & Testing Owner | No — advisory |
| Pre-stage backlog filing obligation for staging-only ACs deferred to post-merge sign-off (see `sprint_backlog.md` per-story **Staging-only ACs** fields) — per CLAUDE.md §2, if staging sign-off is deferred, a backlog item must be filed before the PR opens | Execution Engine (at delegation time) | No — advisory, flagged now per LL-v3.9-P3-2 to avoid a surprise P3 deviation |

No outstanding action is marked `Blocker? Yes`.

## Pre-Sprint Backlog Advisory

Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v6.4 sprint planning` — **none found**. No advisory items.

## Carry-Forward Items

Per `shared_standards.md §16.8`, checked the most recently completed cycle (`2026-06-26__release-v6.3`, `last_post_ship_cycle`) `lessons_learnt_closure.md` `## Carry-Forward` section: **10 items reviewed** (DF-01–DF-10). Summary:

- **For v6.4 Sprint Execution (Head of Specs Team):** DF-01, DF-02, DF-04, DF-05, DF-10 (DF-10 is escalation risk — 2-cycle if missed in v6.4; also folded into ST-06 AC-02 per BLG-GOV-152 scope).
- **For v6.4 Sprint Execution (PMO Lead):** DF-03.
- **For v6.4 Sprint Execution (QA & Testing Owner):** DF-06 (see Outstanding Actions above — applied to ST-08 check).
- **For v6.4 Release Planning (PMO Lead):** DF-08, DF-09 — already actioned/acknowledged at release planning (out of sprint planning's scope).
- **Advisory, no action:** DF-07.

These are primarily Sprint Execution Engine (`execution_prompt.md`) housekeeping items, not sprint-scope items — no ST item is added or altered because of them. Flagged here for Execution Engine STEP 0 pickup.

## Hygiene Advisories (STEP -1 check 7 — non-blocking)

- ⚠ Prompt change log gap: `roadmap_prompt.md` current v7.7 — last log entry v7.5→v7.6 (2026-06-22). The v7.6→v7.7 bump (FI-META-02 action-now patch, rebalance 2026-07-01__scheduled per `.claude_current_state.json last_rebalance_outcome`) has not yet been logged as a row in `prompt_change_log.md`. Add a prepended row per CLAUDE.md §6.
- ⚠ Prompt change log gap: `execution_prompt.md` current v3.48 — last log entry v3.46→v3.47 (2026-06-22). No v3.47→v3.48 row found. Add a prepended row per CLAUDE.md §6.
- No "Before v6.4 sprint planning" backlog items found (see Pre-Sprint Backlog Advisory above).

These gaps are pre-existing (not introduced by this sprint planning run) and are outside this engine's write scope (`claude/system/prompt_change_log.md` is not a permitted write path for `plan sprint`). Surfaced for Head of Specs Team follow-up.

## Staging-Only AC Assessment (LL-v3.9-P3-2 / OA-02 pre-staging)

Applied at planning time to pre-stage the backlog-filing obligation and avoid a surprise P3 notation at execution. Judgment recorded here; final field values also appear per-story in `sprint_backlog.md`:

| Story | AC(s) flagged | Reason |
|-------|---------------|--------|
| ST-01 | AC-02 | Requires observing live signal generation output change in response to a real Ticker Universe Management action — not CI-reproducible as a pure unit test |
| ST-08 | AC-01 | New Panel 0 rendering — no Playwright test is scoped for Panel 0 specifically this sprint (ST-13 covers Panels 1/3 only); visual presence/one-line-summary check needs human staging confirmation or a dedicated Playwright addition at execution time |
| ST-09 | AC-01, AC-02 | Contrast ratio and "no visual regression" are visual/rendering checks; precedent in this project (`ai_disclaimer_visibility_assessment.md`, v6.3 BLG-GOV-147) used human visual QA sign-off rather than automated contrast assertions |
| ST-10 | AC-01 | Contrast ratio check — AC-03's Playwright test covers visibility/text content but not computed contrast value |
| ST-11 | AC-01 | Requires 5 warm requests measured against a live API to produce p50/p95 — inherently a staging/production measurement, not CI-reproducible |

All other ACs across all 13 stories are CI-testable (unit/integration/Playwright) or are process/documentation checks not requiring live-environment evidence.
