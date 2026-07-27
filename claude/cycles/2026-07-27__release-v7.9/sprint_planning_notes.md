**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-27
**Cycle:** 2026-07-27__release-v7.9

# Sprint Planning Notes — 2026-07-27__release-v7.9

## Design Gate / Lifecycle Note (Process Deviation — Advisory)

The design gate genuinely ran and Passed (`design_gate.md`, this cycle: 15/15 items cleared, 0 blocked; PMO Lead, Head of UX & Design, and Product Owner all confirmed; cycle-level `state.json.design_gate_status = "Passed"`). However, `design_gate_prompt.md` v1.4's write scope (§5) does not include `.claude_current_state.json` — it only writes the cycle-level `state.json`. As a result the root state pointer's `status` field was never advanced from `Release_Planning_Complete` to `Design_Gate_Passed`, and `design_gate_status`/`design_gate_record`/`design_gate_completed_utc` in `.claude_current_state.json` remained stale (`not_started` / empty / empty) even though the cycle-level record shows the gate passed.

STEP -1.3's bypass audit is keyed off the literal `.claude_current_state.json.status` value and would treat entry from `Release_Planning_Complete` as "design gate skipped entirely," requiring `design_gate_bypass_authority`/`design_gate_bypass_reason`. Consistent with the identical situation and Product Owner decision recorded in `claude/cycles/2026-07-24__release-v7.8/sprint_planning_notes.md`: this is a state-pointer sync gap in `design_gate_prompt.md` (already tracked as `BLG-GOV-190`), not an actual bypass — gate 3 was independently verified directly against the authoritative cycle-level `state.json` (`design_gate_status = Passed`), and sprint planning proceeds on that basis rather than populating bypass-authority fields for a gate that was not, in fact, bypassed. No new backlog item filed — `BLG-GOV-190` already covers this gap (2nd recurrence, v7.8 → v7.9).

## Backlog Slice Source

Original — `claude/cycles/2026-07-27__release-v7.9/stage4_backlog_slice.md` (`.claude_current_state.json.amended_backlog_slice_path` is absent/empty — no amendment in effect).

## Carry-Forward Items

Carry-forward items reviewed: 3 items from cycle `2026-07-24__release-v7.8` (`lessons_learnt_closure.md ## Carry-Forward`).

1. **Cross-EPIC `execution_state.json` conflict recurrence (2nd occurrence, v7.7 → v7.8).** This is directly relevant to this sprint: v7.9 is again a multi-EPIC (15-EPIC) sprint, so the same merge-conflict pattern is likely to recur a 3rd time. The carry-forward note advises Sprint Execution should not proceed past a 3rd occurrence without either applying the deferred structural fix or re-confirming with Head of Specs Team that the manual-resolve cost is accepted. **Notable:** `BLG-GOV-263` (cross-EPIC `execution_state.json` structural fix, L effort, filed at the `2026-07-27__scheduled` rebalance specifically in response to this recurrence) was **not** pulled into this v7.9 scope — the 15 items in this sprint were selected on other grounds and capacity filled before it was reached. Flagged here as an explicit risk: if this sprint's merges hit the pattern a 3rd time, Sprint Execution must escalate to Head of Specs Team per the carry-forward guidance rather than silently absorbing another manual-resolve round. Recorded as an Outstanding Action below.
2. **Real test execution over "written but not run" sign-off.** Applies generically to this sprint's QA sign-off discipline — no specific action required here; carried forward as a standing execution-time practice.
3. **Post-Ship Closure STEP 6 gap-count verification.** Not applicable to Sprint Planning; no action required.

## Deferred Items

None. All 15 EPICs / ST items are within confirmed capacity (~26.5 days vs ~24-28 day ceiling, ~95-110% utilisation) and all 3 conditionally-gated EPICs (EPIC-01/02/05) cleared the Design Gate with 0 blocked. Full backlog slice enters the sprint.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-04 (EPIC-04) | ST-06 (EPIC-06) | Internal (soft — sequencing preference per `release_plan.md ## Execution Plan`, shared audit-trail/reporting domain, not a hard dependency) | Resolved — merge order below |
| ST-06 (EPIC-06) | ST-03 (EPIC-03) | Internal (soft — shared file: `docs/data_model.md`, EPIC-03 adds the FK linkage schema section, EPIC-06 adds the audit-log table schema section) | Resolved — merge order below |
| ST-08 (EPIC-08) | External — real credential provisioning | External (human action — Infrastructure & Operations Owner must obtain an actual scoped API key/token from the provider; the execution engine cannot generate a genuine external secret) | Open — does not block sprint seal; must resolve before EPIC-08's own AC-01/AC-02 can close |
| ST-06 (EPIC-06) | Write-path scope clarification | Internal (decision — no existing "manual position edit" API endpoint was found in `backend/routers/`; the actual write path to instrument (existing internal service call vs. a new endpoint) is not fully specified in the backlog item) | Open — must resolve with Financial Reporting & Records Owner before EPIC-06 implementation begins; does not block sprint seal |

No circular dependencies identified.

## Execution Sequence

Ordered to unblock non-UI/autonomous items first, respect the EPIC-03 → EPIC-06 → EPIC-04 shared-file/domain sequencing preference, and place the one `delegated_decision` item (EPIC-08) ahead of the Design Required cluster per STEP 5.2 grouping guidance:

1. EPIC-03 — BLG-SPEC-105 (data_model.md FK linkage schema — first to touch `data_model.md`)
2. EPIC-11 — BLG-FE-130 (WCAG contrast checklist addendum)
3. EPIC-13 — BLG-FE-129 (dark-mode AC checklist addendum)
4. EPIC-14 — BLG-GOV-258 (displacement debt register)
5. EPIC-15 — BLG-QA-123 (visual-regression baseline refresh cadence)
6. EPIC-09 — BLG-QA-124 (shared cross-EPIC smoke-test tagging)
7. EPIC-10 — BLG-QA-125 (pre-commit hook for `test.py` registration)
8. EPIC-07 — BLG-BE-74 (nightly backtest CI smoke test)
9. EPIC-08 — BLG-OPS-121 (staging credential provisioning — `delegated_decision`, sequenced before the remaining autonomous items so the external dependency surfaces early)
10. EPIC-12 — BLG-OPS-120 (cost-tag cloud infra spend)
11. EPIC-06 — BLG-BE-73 (audit trail for manual position overrides — rebases onto `data_model.md` after EPIC-03)
12. EPIC-04 — BLG-FEAT-85 (P&L CSV cost-basis reconciliation — sequencing preference after EPIC-06 per release plan)
13. EPIC-01 — BLG-FEAT-66 (watchlist staleness review — Design Required)
14. EPIC-02 — BLG-FEAT-67 (sector/regime exposure trend — Design Required, new backend endpoint)
15. EPIC-05 — BLG-FEAT-87 (trailing-stop explainer tooltip — Design Required)

**Multi-EPIC `execution_state.json` ownership:** EPIC-03 (first in execution order) owns `execution_state.json` for this sprint. All other 14 EPIC branches must check for its existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite, per `shared_standards.md §12`.

## Multi-EPIC Execution Notes

**Shared file ownership advisory (15 EPICs in scope):**

| Shared file | Owning EPIC | Must rebase after | Basis |
|---|---|---|---|
| `docs/data_model.md` | EPIC-03 | EPIC-06 | EPIC-03 adds the trade_plan↔position FK linkage schema section; EPIC-06 adds the manual-override audit-log table schema section |
| `docs/reference/openapi.yaml`, `docs/specs/api_contracts/*.md`, `backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js` | EPIC-02 | Any EPIC discovered at kickoff to require a new endpoint | Router inspection at planning time (`backend/routers/portfolio_risk.py`) found no existing sector/regime **history** endpoint (only current-snapshot endpoints: `sector-weights`, `concentration-status`, `drawdown-status`, `gate-metrics`) — EPIC-02 will very likely add one. By contrast, EPIC-01 can reuse the existing `PATCH /watchlist/{entry_id}` and `DELETE /watchlist/{entry_id}` endpoints (confirmed present in `backend/routers/watchlist.py`) for its Keep/Remove actions, so it is not expected to touch this cluster. EPIC-06 and EPIC-12 are flagged as **possible** but unconfirmed touches to this cluster (see Outstanding Actions) — if either turns out to need a new endpoint at kickoff, it must rebase onto `main` after EPIC-02 merges. |
| `render.yaml` | EPIC-12 | — | Sole owner this sprint; cost-tag additions are config-only, no other EPIC touches this file |

No `execution_state.json` ownership conflict beyond the standard designation above.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01, EPIC-02, EPIC-05 | Resolved — Design Gate Passed (15/15 cleared, 0 blocked); Playwright coverage or recorded staging sign-off still required per CLAUDE.md §2 for each observable AC, to be confirmed at kickoff |
| RISK-02 | EPIC-07 | Valid — mitigation (treat any newly-surfaced data-integrity defect as its own backlog item, not a blocker to EPIC-07's own AC) carried into this story's sprint backlog Notes |
| RISK-03 | Release-level (all 15 EPICs) | Valid — scope is deliberately at the top of the confirmed ~24-28 day capacity band (~26.5 days midpoint, ~95-110% utilisation) per explicit user "use the full capacity" instruction; accepted per `docs/product/decisions/decisions--2026-07-27__release-v7.9.md`. No Phasing Recommendation exists (capacity outcome was `pass`, not `warn`), so no phasing adopt/decline decision is required at this step. |

No risk has materialised since release planning.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json` (run via `backend/.venv/bin/python3 -m pip_audit`, per CLAUDE.md §9): **clean** — no known vulnerabilities found across all 60 resolved dependencies.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Confirm the actual manual-position-edit write path (existing internal service call vs. new endpoint) for EPIC-06 before implementation begins | Financial Reporting & Records Owner | No |
| Provision the real staging/scoped-production credential for EPIC-08 (external action — cannot be generated by the execution engine) | Infrastructure & Operations Owner | No |
| If Sprint Execution's `execution_state.json` cross-EPIC merge conflict recurs a 3rd consecutive time this sprint (v7.7 → v7.8 → v7.9), escalate to Head of Specs Team per the v7.8 carry-forward note rather than silently absorbing another manual-resolve round; `BLG-GOV-263` (the deferred structural fix) was not in this sprint's scope | Sprint Execution / Head of Specs Team | No |
| Prompt change log gaps (advisory, pre-existing — not introduced this session): `release_planning_prompt.md` current v2.44, last logged transition target v2.41; `sprint_planning_prompt.md` current v3.13, last logged target v3.12; `execution_prompt.md` current v3.60, last logged target v3.58; `delivery_verification_prompt.md` current v3.5, last logged target v3.4; `post_ship_closure.md` current v2.20, last logged target v2.19; `backlog_management_prompt.md` current v1.12, last logged target v1.9; `roadmap_prompt.md` current v9.6, last logged target v9.4. Add prepended rows per CLAUDE.md §6. | Head of Specs Team | No |
| Confirm Playwright feasibility (or arrange staging sign-off) for each of EPIC-01/02/05's observable ACs at kickoff | Director of Quality | No |
| Confirm at kickoff whether EPIC-02 (and, less likely, EPIC-06/EPIC-12) require a genuinely new backend endpoint, and apply the same-commit `openapi.yaml`/`docs/specs/api_contracts/*.md`/`backend/routers/test.py`/`SystemStatus.js`/`SC-SS-01b` requirements (CLAUDE.md §2) accordingly | Head of Engineering | No |

No outstanding action is marked `Blocker? Yes`.
