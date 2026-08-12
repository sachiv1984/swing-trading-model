**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-12
**Cycle:** 2026-08-12__release-v8.7

# Sprint Planning Notes — 2026-08-12__release-v8.7

## Backlog Slice Source

Original — `claude/cycles/2026-08-12__release-v8.7/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty in both `.claude_current_state.json` and `state.json` — no amendment sealed for this cycle).

## Carry-Forward Items

2 items reviewed from cycle `2026-08-11__release-v8.6` (`lessons_learnt_closure.md ## Carry-Forward`):
1. `scripts/check_api_performance_baseline_drift.py` substring-match false-negative fix (carried v8.4→v8.5→v8.6) — **actioned this cycle** as ST-17 (EPIC-06, `BLG-OPS-142`), filed directly as a sprint story per the closure's own recommendation rather than deferred again.
2. `reports.md` deviation-register concentration signal — re-check not yet due (2 of 3 cycles since 2026-08-08). No action required this cycle.

## Pre-Sprint Backlog Advisory

No `backlog.md` items carry `Provisional-Target: Before v8.7 sprint planning` (0 matches).

## Pre-sprint Planning Required Decisions (from `cycle_summary.md`)

- **[RISK-02] `BLG-BE-96` (ST-07, EPIC-02) staging/live-Postgres access.** Re-checked at this planning run: no `DATABASE_URL`/staging credential is available in this sandbox, `psql` is not installed, and there is no outbound network path to a live Postgres host (confirmed via direct reachability check — identical constraint to the one recorded at v8.6's `qa_evidence_EPIC-02.md`/`delegation_log.md`). Staging access is **still unavailable**, unchanged since v8.6.
  - **Resolution (Product Owner, agent-mediated, 2026-08-12 — pending final human confirmation, same disposition pattern as v8.6's `BLG-BE-96` acceptance):** ST-07 proceeds via best-available proxy rather than being deferred again — Head of Engineering executes the linkage-confirmation and DS-12 constraint checks against the best available evidence (code-path/test-suite confirmation, migration-state inspection) at execution time, and explicitly documents the residual staging-verification gap rather than silently treating it as met. The v8.6-established condition carries forward unchanged: **if the legacy-row audit finds any of the 11 known rows with `status='active'`, that finding escalates to its own P0 immediately** — it does not fold into ST-07's own timeline.
  - Recorded as **resolved**, not `Blocker? Yes` — sign-off gate is not blocked by this item. Reason: this is a re-confirmation of an already-accepted, actively-tracked risk (not a new unresolved question), and the decision required by `cycle_summary.md` ("PO must explicitly re-confirm the item proceeds via best-available proxy") has been made and recorded here.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — "No known vulnerabilities found" across all scanned dependencies (fastapi 0.135.1, pandas 3.0.3, sqlalchemy 2.0.23, anthropic 0.105.2, and all transitive dependencies).

## Hygiene Advisories

- **Prompt change log gaps:** date-scan method run across all 15 versioned Class 6 prompt files in `claude/system/`. No gaps found — every file's current `**Version:**` header is at or behind the latest dated `prompt_change_log.md` row naming it (spot-verified by direct row inspection for `sprint_planning_prompt.md` v3.16, dated 2026-08-06, and `idea_intake_prompt.md` v2.8, dated 2026-07-27, after an initial substring-match false-positive on both was ruled out by reading the actual matched rows).
- **Recurring endpoint test coverage audit:** `python3 scripts/audit_endpoint_test_coverage.py` — exit 0. 80 route decorators scanned across 23 router files; 8 documented `KNOWN_GAPS` exclusions; no undocumented gaps.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-08 | ST-06 | Internal | Resolved — sequenced after EPIC-01 in execution order (RISK-03 mitigation: land ST-06's modal token conversion before ST-08's Playwright coverage authoring, so selectors are stable) |

No other cross-item dependencies identified. No external (delegated third-party) blockers. No spec-dependent items pending a lock — all Design Required items (ST-01, ST-02, ST-21) were cleared with locked spec artefacts at the Design Gate (`design_gate.md`, Passed 2026-08-12).

No circular dependencies detected.

## Execution Sequence

1. **EPIC-01** — User-Facing Product Features & UX Completion (ST-01, ST-02, ST-03, ST-04, ST-05, ST-06) — leads per explicit user "user features to be prioritised" capacity directive; no dependency blocks it starting first.
2. **EPIC-02** — Trade-Plan Data Integrity Closure (ST-07) — mandatory carryover, no dependency on EPIC-01, sequenced second to close the v8.6 PO risk-acceptance condition early in the sprint.
3. **EPIC-03** — Test Coverage for Shipped UI & Financial Correctness (ST-08, ST-09) — ST-08 requires EPIC-01/ST-06's token conversion to have landed first (RISK-03).
4. **EPIC-04** — Backend Reliability & Performance Hardening (ST-10, ST-11, ST-12)
5. **EPIC-05** — Security Hardening (ST-13, ST-14)
6. **EPIC-06** — Operations & Infrastructure Debt (ST-15, ST-16, ST-17)
7. **EPIC-07** — Governance & Spec Debt (ST-18, ST-19, ST-20, ST-21)

EPIC-04 through EPIC-07 carry no sequencing constraint against each other or against EPIC-01/02/03; ordered here per `release_plan.md`'s Execution Plan table order for consistency.

### Multi-EPIC Execution Notes

**`execution_state.json` owner: EPIC-01** (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

**Shared file ownership advisory:**
- `docs/specs/frontend/design_system.md` — touched by **EPIC-01** (ST-06, Modal / Dialog Theming token conversion — corrective, uses the existing v1.9 section) and **EPIC-07** (ST-21, new "Gated variant" subsection under Shared UI Components → Cards → Data States, v1.10 already cut at Design Gate). EPIC-01 merges first per execution order; EPIC-07 must rebase onto `main` after EPIC-01 merges before finalising its `design_system.md` changes.
- `docs/specs/data_model.md` — plausible touch point for both **EPIC-01** (ST-03, new `trade_plans.is_ai_draft` column — new migration block) and **EPIC-02** (ST-07, DS-12 constraint verification note on the same `trade_plans` table, no new migration). EPIC-01 merges first; EPIC-02 rebases onto `main` after EPIC-01 merges before finalising any `data_model.md` note it adds.
- `execution_state.json` — all 7 EPICs (see owner designation above).

No other cross-EPIC shared source files identified — EPIC-03's `trade_plan.md`/token references are read-only against EPIC-01's locked spec additions (§5.1, §10.6), not concurrent edits to the same section.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01) | Valid — resolved at Design Gate (`decision_record.md`, `trade_plan.md` v1.5 §5.1); no longer an open placement/copy question |
| RISK-02 | EPIC-02 (ST-07) | Changed — staging access confirmed still unavailable at sprint planning (re-checked this run); resolution recorded above (best-available proxy, PO re-confirmed, P0-escalation condition carried forward) |
| RISK-03 | EPIC-03 (ST-08) | Valid — mitigated via execution sequencing (EPIC-01 before EPIC-03; see Execution Sequence) |
| RISK-04 | EPIC-04 (ST-11) | Valid — scope explicitly bounded to audit + clearly-attributable fixes; broader-refactor cases to be filed as follow-up backlog items rather than expanded in-cycle |
| RISK-05 | EPIC-05 (ST-13, ST-14) | Valid — mitigation (staging/test environment only, no production traffic generation) unchanged and still applicable |
| RISK-06 | EPIC-06 | Valid — no material risk, standard review |
| RISK-07 | EPIC-07 | Valid — no material risk, standard review |

No risk has materialised into a new escalation.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Confirm ST-07 best-available-proxy execution approach and residual-gap documentation at delivery verification | Head of Engineering | No — resolved at planning per Pre-sprint Planning Required Decisions above; tracked for execution-time follow-through, not a seal blocker |
| Rebase `design_system.md` (EPIC-07 onto EPIC-01) and `data_model.md` (EPIC-02 onto EPIC-01) after EPIC-01 merges | EPIC-07 / EPIC-02 branch owners | No — execution-time merge-sequencing action, not a planning seal blocker |

No outstanding action is marked `Blocker? Yes`.
