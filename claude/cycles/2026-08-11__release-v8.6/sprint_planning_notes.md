**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-11
**Cycle:** 2026-08-11__release-v8.6

# Sprint Planning Notes — 2026-08-11__release-v8.6

## Backlog Slice Source

Original — `claude/cycles/2026-08-11__release-v8.6/stage4_backlog_slice.md`. `.claude_current_state.json.amended_backlog_slice_path` and `state.json.amended_backlog_slice_path` are both empty — no amendment sealed for this cycle.

## Carry-Forward Items

Carry-forward items reviewed: 3 items from cycle `2026-08-08__release-v8.5` (`lessons_learnt_closure.md ## Carry-Forward`):

| # | Observation | Status at this planning run |
|---|-------------|------------------------------|
| 1 | `scripts/check_api_performance_baseline_drift.py` substring-matching false-negative fix + `execution_prompt.md` `test_scenarios` roll-up cross-reference — 2 consecutive cycles unapplied, next miss should trigger direct application rather than a 3rd deferral | No item in this cycle's 26-story scope directly carries this forward; advisory only, no sprint-planning action required |
| 2 | `reports.md` deviation-register concentration (2 of 10 register rows) — light signal, next check due at the 3rd deviation-consolidation review (not due this cycle) | No action required this cycle |
| 3 | `BLG-GOV-292` escalation + 5-failure-mode gate-detection pattern, pending Head of Specs Team 72-hour decision | Already resolved — `git log` commit `3c1a2cea` ("Head of Specs Team resolves 2 post-ship closure escalations (BLG-GOV-292, DEV-EPIC02-ST03-01)"), predates this planning run. No open item carried in. |

## Deferred Items

None. All 26 items in `stage4_backlog_slice.md` classify `include` — total estimated effort (23.75 days) does not exceed confirmed capacity (~24-28 days); no item is blocked by an unresolved dependency or escalation.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-05 | ST-04 | Internal | Resolved — sequenced within EPIC-03 execution order (ST-04 before ST-05) |

No other cross-item dependencies identified. No circular dependencies detected.

**ST-21 timing note (not a blocking dependency):** ST-21's AC requires a confirmed-successful post-merge run of `dependency-vuln-rescan.yml`. This can only be observed after this sprint's own PRs (including ST-21's own EPIC-06 branch) merge to `main`. Sequenced last within EPIC-06; verification step to be performed once the EPIC-06 PR (and any earlier-merging EPIC PRs) are on `main`, via a manual `workflow_dispatch` if the monthly schedule has not fired naturally within the sprint window.

## Execution Sequence

1. EPIC-01 — User-Facing Product Features (ST-01, ST-02) — leads per Skill-Silo rotation guideline (§3), per `release_plan.md` Execution Plan sequencing note (2026-08-11 rebalance, 3rd-consecutive-worsening Skill-Silo Alert)
2. EPIC-02 — Trade-Plan Data Integrity Foundation (ST-03)
3. EPIC-03 — Frontend Design Consistency & Correctness Carryover (ST-04 → ST-05, ST-06, ST-07, ST-08, ST-09, ST-10)
4. EPIC-04 — Backend & Financial Correctness (ST-11, ST-12, ST-13, ST-14)
5. EPIC-05 — QA Test-Coverage Debt Closure (ST-15, ST-16, ST-17, ST-18)
6. EPIC-06 — Operations & Governance Debt Closure (ST-19, ST-20, ST-21, ST-22, ST-23, ST-24, ST-25, ST-26)

Autonomous items are grouped ahead of delegated items within each EPIC where the dependency map allows (per §5.2); the EPIC-level sequence above otherwise follows `release_plan.md`'s own Execution Plan table order, which the Skill-Silo rotation note already sequenced.

### Multi-EPIC Execution Notes

**`execution_state.json` owner: EPIC-01** (first in execution order). All other EPIC branches (EPIC-02 through EPIC-06) must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

**Shared file ownership advisory:**

| File | EPICs touching it | Ownership |
|------|--------------------|-----------|
| `docs/specs/frontend/pages/analytics.md` | EPIC-01 (ST-01, spec already updated to v2.1 §21 at design gate), EPIC-03 (ST-10, references §15 as a locked, unchanged reference) | EPIC-01 owns the canonical §21 addition; EPIC-03's ST-10 does not further modify the spec — no rebase required, but EPIC-03 should confirm §15 is unchanged after EPIC-01 merges |
| `docs/specs/frontend/pages/trade_plan.md` | EPIC-01 (ST-02, spec already updated to v1.4 §10.5 at design gate), EPIC-02 (ST-03, references §10 as a locked, unchanged reference) | EPIC-01 owns the canonical §10.5 addition; EPIC-02's ST-03 does not further modify the spec |
| `docs/specs/frontend/design_system.md` | EPIC-03 (ST-04 token registration reference, ST-06 canonical-token restoration, ST-07 decision record's new "Modal / Dialog Theming" subsection — all already updated to v1.9 at design gate) | EPIC-03 owns; no cross-EPIC collision — all touches are within EPIC-03 |
| `execution_state.json` | All 6 EPICs (story status tracking) | EPIC-01 (see above) |

No other shared source files identified across EPICs for this cycle's scope (EPIC-04/05/06 items are backend-, test-, or governance-doc-only with no shared frontend spec touches).

**No new API endpoints identified in this cycle's scope** (ST-02 and ST-10 both reuse existing endpoints per the design gate's own analysis). If any story's implementation surfaces a new endpoint requirement during execution, the same-commit `docs/reference/openapi.yaml` + `docs/specs/api_contracts/` obligations (CLAUDE.md §2) apply regardless.

## Delegation Class Assignment

| EPIC | ST | Delegation Class | Justification |
|------|----|--------------------|----------------|
| EPIC-01 | ST-01 | autonomous | New component against a now-locked spec (`analytics.md` v2.1 §21, decision record cleared at design gate) — BLG-GOV-72 fast-path (c) |
| EPIC-01 | ST-02 | autonomous | New UI element against a now-locked spec (`trade_plan.md` v1.4 §10.5, ux_spec.md cleared at design gate); reuses existing thesis-generation service, no new inference call — BLG-GOV-72 fast-path (c) |
| EPIC-02 | ST-03 | delegated_backend | AC requires staging-verified enforcement plus explicit Data Model, Domain & Schema Owner + Product Owner sign-off — human review at a specific step |
| EPIC-03 | ST-04 | autonomous | Corrective build-config fix restoring already-canonical tokens; identical root cause to v8.5 ST-06 (design gate note) |
| EPIC-03 | ST-05 | autonomous | Test-coverage-only story for already-shipped tokens, no UX change — LL-v1.10-P3-3 |
| EPIC-03 | ST-06 | autonomous | Corrective fix restoring an already-canonical token across 6 named call sites — BLG-GOV-72 fast-path (a)-equivalent |
| EPIC-03 | ST-07 | delegated_decision | Genuine design-system judgment call; HoST/UX design artefact already exists (`docs/design/2026-08-11__release-v8.6/modal-light-theme-support/decision_record.md`, cleared at design gate) — satisfies LL-v2.2-SP-01 check |
| EPIC-03 | ST-08 | autonomous | Technical render-timing/lifecycle-hook fix, no UI/design decision; AC itself permits a code-comment-only outcome |
| EPIC-03 | ST-09 | autonomous | Documentation correction only, no live UI change |
| EPIC-03 | ST-10 | autonomous | Architecture refactor against an already-specified canonical backend source; AC states no visual change expected — BLG-GOV-72 fast-path (a)-equivalent |
| EPIC-04 | ST-11 | autonomous | Backend documentation/behaviour correctness fix, no UI |
| EPIC-04 | ST-12 | delegated_backend | AC requires explicit Financial Reporting & Records Owner sign-off on audit findings |
| EPIC-04 | ST-13 | delegated_backend | AC requires explicit Financial Reporting & Records Owner sign-off |
| EPIC-04 | ST-14 | autonomous | CI/CD tool robustness fix, no sign-off condition beyond normal QA |
| EPIC-05 | ST-15 | autonomous | Test-only, no UI |
| EPIC-05 | ST-16 | autonomous | Test-only (Playwright), no UI change — coverage for already-shipped behaviour |
| EPIC-05 | ST-17 | autonomous | Test-only, no UI |
| EPIC-05 | ST-18 | autonomous | Test-infrastructure documentation, no UI |
| EPIC-06 | ST-19 | autonomous | CI/CD workflow fix, no UI |
| EPIC-06 | ST-20 | autonomous | CI/CD documentation, no UI |
| EPIC-06 | ST-21 | autonomous | CI/CD verification (see timing note above); no human decision required |
| EPIC-06 | ST-22 | autonomous | Governance record only, matches an existing DEV-record format precedent |
| EPIC-06 | ST-23 | autonomous | Governance document fix, no UI |
| EPIC-06 | ST-24 | delegated_decision | AC requires explicit Head of Specs Team sign-off on the corrected field-meaning documentation |
| EPIC-06 | ST-25 | autonomous | Governance document annotation, no UI |
| EPIC-06 | ST-26 | autonomous | Governance document correction, no UI |

No `delegated_frontend` items this cycle — all frontend-shaped stories (ST-01, ST-02, ST-04, ST-05, ST-06, ST-08, ST-09, ST-10) qualify for `autonomous` under the BLG-GOV-72 fast-path or LL-v1.10-P3-3 heuristic given the design gate has already cleared every open design question for this scope (see `design_gate.md` — 26/26 items cleared, 0 blocked).

No EPIC introduces a new page or new user-facing controls that would trigger the LL-v2.0-P4-2 `test_scenarios` roll-up flag (ST-01 and ST-02 add new elements to existing pages/flows, not new pages).

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — PO's qualitative usage-pattern disposition already recorded in `decisions--2026-08-11__release-v8.6.md` at release planning; no change since |
| RISK-02 | EPIC-02 | Valid — staging verification requirement is carried into ST-03's AC and this sprint's delegated_backend classification |
| RISK-03 | EPIC-03 | Valid — Playwright coverage or staging sign-off requirement is carried into every EPIC-03 item's AC per CLAUDE.md's frontend-visible-change hard gate |
| RISK-04 | EPIC-04 | Valid — audit-first scope; Financial Reporting & Records Owner sign-off requirement carried into ST-12/ST-13's delegated_backend classification |
| RISK-05 | EPIC-05, EPIC-06 | Valid — this sprint's own capacity check (23.75 days) confirms fit within the confirmed ~24-28 day band; no phasing required |
| RISK-06 | EPIC-06 | Valid — EPIC-06 subtotal (5.25 days) remains a small fraction (~22%) of total sprint effort; accepted as low-cost cleanup per release plan rationale |

No risk has materialised since release planning; no new escalation raised.

## Pre-Sprint Vulnerability Scan

`pip-audit` is not available in this environment (`pip-audit` command not found). Flagged per STEP -1 advisory check 6 — recommend installing `pip-audit` in the execution environment before sprint execution begins so the per-PR CI gate (`vulnerability-scan.yml`) remains the authoritative check for this sprint; this pre-sprint local scan is advisory-only and does not block planning.

## Hygiene Advisories

- **Prompt change log gap check:** `sprint_planning_prompt.md` — current header `v3.16`; latest `prompt_change_log.md` row (date-scan method, §11.1) is `2026-08-06 | v3.15→v3.16`. No gap.
- **"Before Sprint Planning" backlog items:** scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v8.6 sprint planning` — 0 matches. Nothing to surface.
- **Recurring endpoint test coverage audit** (`scripts/audit_endpoint_test_coverage.py`): exit 0 — 79 route decorators scanned across 23 router files, 8 documented `KNOWN_GAPS` exclusions, 0 undocumented gaps. Recorded: "pre-sprint endpoint coverage audit: clean."

## Director of Quality Readiness Check

For each `include` EPIC, the Director of Quality (agent-embodied role) confirms the QA criteria in `stage4_backlog_slice.md` are sufficient to produce `qa_evidence_EPIC-xx.md` at sprint close for all 6 EPICs — every item's AC names a specific, testable condition (endpoint behaviour, computed value, file content match, or explicit sign-off requirement); no item has a vague "tested"-only criterion. No known test coverage gap flagged that would block sign-off.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Install `pip-audit` in the execution environment before sprint execution begins | Head of Engineering | No — advisory only |
| Verify `dependency-vuln-rescan.yml` post-merge run once EPIC-06's PR lands (ST-21) | Director of Quality | No — this is ST-21's own execution-time AC, not a planning seal blocker |

No outstanding action is marked `Blocker? Yes`.
