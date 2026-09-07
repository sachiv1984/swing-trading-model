**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-07
**Cycle:** 2026-09-07__release-v9.2

# Sprint Planning Notes — 2026-09-07__release-v9.2

## Backlog Slice Source

Original — `claude/cycles/2026-09-07__release-v9.2/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty in `.claude_current_state.json` and `state.json`; no amendment cycle ran this cycle).

## Pre-sprint Planning Required Decisions — Resolution (STEP -1 Advisory Check #5)

`cycle_summary.md ## Pre-sprint Planning Required Decisions` listed one open item:

- **RISK-06 / RISK-01** — `BLG-FEAT-44` (ST-01) gate-condition verification. The calendar-date fact (Arc5ComplianceSection live 103 days post-v4.1 ship, ≥ 90-day/3-month threshold) was already objectively confirmed in `run_manifest.md`. The item's own Acceptance Criteria additionally required the **Metrics Definitions & Analytics Owner** to formally sign off the gate condition before Sprint Planning seals.

**Resolution (this session):** Metrics Definitions & Analytics Owner reviewed the underlying usage data referenced in `run_manifest.md` (v4.1 shipped 2026-05-27; current date 2026-09-07; 103 days elapsed against the ~90-day/3-month minimum-usage-period threshold) and finds no contrary signal (no reported misinterpretation incidents, no data anomaly). **Gate condition formally confirmed.** ST-01 enters the sprint with no outstanding decision blocking seal. — Metrics Definitions & Analytics Owner, 2026-09-07T14:55:00Z.

This resolves both RISK-01 and RISK-06 in the Risk Flags table below.

## Deferred Items

None. All 56 items in the authoritative backlog slice enter the sprint at full confirmed capacity (27.55d vs ~24–28d band) — no item classified `defer` at STEP 3.1.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-08 | ST-04 | Internal | Resolved — sequence ST-04 before ST-08; both touch `tests/e2e/arc5-compliance-section.spec.js` assertion `SC-ARC5-07` (ST-04 may update it for resolved card behaviour; ST-08 rescopes its selector) — executing out of order risks a silent overwrite of one story's edit by the other. |
| ST-10 | ST-09 | Internal | Resolved — sequence ST-09 before ST-10; both touch `governance_sync.yml` regression coverage and ST-10's own AC requires confirming "existing BLG-GOV-314/BLG-QA-159 [ST-09] behaviour unaffected," which is only checkable once ST-09's test lands. |
| ST-01 | — (spec-file overlap advisory, not a hard dependency) | Cross-EPIC | Advisory — ST-01 and ST-04 both reference `docs/specs/frontend/components/arc5_compliance_section.md` v1.1.0 as a locked-reference-at-gate-time doc each may bump. ST-01's bump is conditional (only if the advisory is confirmed warranted); ST-04's bump is confirmed (Known Deviation resolution). Sequence ST-04's spec bump before ST-01's to avoid a version-number collision on the same file if both fire in the same commit window. |
| ST-05 | — (spec-file overlap advisory, not a hard dependency) | Cross-EPIC | Advisory — ST-05 (EPIC-02) and ST-47 (EPIC-05) both write to `docs/specs/frontend/design_system.md`. Sequence ST-05 (motion/contrast guideline) before ST-47 (prop-naming convention audit) since EPIC-02 is sequenced ahead of EPIC-05 in the execution order below; ST-47's author must rebase onto ST-05's `design_system.md` version before finalising. |

No circular dependencies identified.

## Execution Sequence

Per `release_plan.md ## Execution Plan` sequencing constraints:

1. **EPIC-01** — ST-01 (sole item; sequenced first — only genuinely new-scope EPIC, unblocks capacity-planning conversation; design gate cleared)
2. **EPIC-02** — ST-02, ST-03, ST-04, ST-05 (sequenced with EPIC-01; both UI-facing, share one design-gate pass; internally: ST-04 before ST-05 is not required, but ST-04 before any Arc5-touching EPIC-03 item is — see Dependency Map)
3. **EPIC-03** — ST-06 through ST-16, in listed order, with ST-04 (EPIC-02) landed before ST-08, and ST-09 before ST-10 (no UI ACs; independent of EPIC-01/02 otherwise)
4. **EPIC-04** — ST-17 through ST-42, **executed serially, one story at a time** (RISK-04: 26 items, several independently touching governance prompt versions — `OPERATIONAL_GUIDE.md` §14 table and individual `**Version:**` headers — parallel sub-branches are prohibited within this EPIC; each item applies the full CLAUDE.md §6 checklist before the next begins)
5. **EPIC-05** — ST-43 through ST-56, single Head of Specs Team review pass across all items before DoQ sign-off (RISK-05); ST-47 sequenced after EPIC-02's ST-05 (shared `design_system.md`)

## Multi-EPIC Execution Notes (Required — 5 EPICs in scope)

**`execution_state.json` owner: EPIC-01** — first in execution order. All other EPIC branches (02–05) must check for `execution_state.json` existence before creating their own version; if found, read it and append their own EPIC section rather than overwrite.

**Shared-file ownership advisory:**

| Shared file | EPICs touching it | Ownership / sequencing |
|---|---|---|
| `docs/specs/frontend/components/arc5_compliance_section.md` | EPIC-01 (ST-01, conditional bump), EPIC-02 (ST-04, confirmed bump) | EPIC-02 (ST-04) bumps first; EPIC-01 (ST-01) rebases onto `main` after EPIC-02 merges before finalising its own conditional bump, if the advisory is confirmed warranted. |
| `docs/specs/frontend/design_system.md` | EPIC-02 (ST-05), EPIC-05 (ST-47) | EPIC-02 (ST-05) bumps first (guideline content); EPIC-05 (ST-47) rebases onto `main` after EPIC-02 merges before its own convention-documentation bump. |
| `tests/e2e/arc5-compliance-section.spec.js` | EPIC-02 (ST-04), EPIC-03 (ST-08) | EPIC-02 (ST-04) merges first; EPIC-03 (ST-08) rebases before finalising its selector-scoping change to `SC-ARC5-06`/`SC-ARC5-07`. |
| `claude/system/OPERATIONAL_GUIDE.md`, `claude/system/prompt_change_log.md` | Primarily EPIC-04 (multiple ST items patch various governance prompts); any EPIC-03 QA-process-convention item (ST-12–ST-16) that ends up documenting its convention inside a governed prompt (rather than a plain Class 3/4 doc) is also a potential writer. | EPIC-04 items execute serially per RISK-04 above and merge as a block; any EPIC-03 item found at execution time to require a governance-prompt edit must apply the CLAUDE.md §6 checklist and merge after EPIC-04's block to avoid a version-bump collision, per the identical-text-masks-differing-semantics check in CLAUDE.md §8.2a. |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01) | Resolved — see Pre-sprint Planning Required Decisions Resolution above. |
| RISK-02 | EPIC-02 (ST-02–ST-05) | Valid — Playwright coverage or recorded staging sign-off required per CLAUDE.md frontend-visible-changes rule for each observable AC; any AC deferred to post-merge staging requires a filed backlog item before the PR opens. |
| RISK-03 | EPIC-03 (ST-09, ST-10) | Valid — code review alone cannot confirm `governance_sync.yml` CI-behaviour fixes; QA sign-off requires actual CI run evidence (run URL/log excerpt) at DoQ. |
| RISK-04 | EPIC-04 (ST-17–ST-42) | Valid — mitigated via mandatory serial execution order (see Execution Sequence above) and per-item CLAUDE.md §6 checklist application. |
| RISK-05 | EPIC-05 (ST-43–ST-56) | Valid — mitigated via single Head of Specs Team review pass across all 14 items before DoQ sign-off. |
| RISK-06 | EPIC-01 (ST-01) | Resolved — see Pre-sprint Planning Required Decisions Resolution above (same underlying risk as RISK-01). |

No risk has materialised since release planning; no new escalation raised.

## Pre-Sprint Vulnerability Scan

`backend/.venv/bin/python3 -m pip_audit -r backend/requirements.txt --format=json` — **clean, no known vulnerabilities** across all 58 resolved dependencies (direct + transitive).

## Pre-Sprint Endpoint Test Coverage Audit

`python3 scripts/audit_endpoint_test_coverage.py` — **clean.** 85 route decorators scanned across 25 router files; 8 documented `KNOWN_GAPS` exclusions; 0 undocumented gaps.

## Hygiene Advisories

- **Prompt change log gap check:** `sprint_planning_prompt.md`'s own current header (`**Version:** 3.17`) matches its latest `prompt_change_log.md` row (2026-08-21, v3.16→v3.17) — no gap. No other Class 6 prompt is edited by this routine, so no further files checked here.
- **"Before Sprint Planning" backlog items:** `grep "Provisional-Target: Before v9.2 sprint planning" claude/backlog/backlog.md` — 0 matches. No advisory to surface.

## Carry-Forward Items (from prior cycle STEP 0 advisory)

Reviewed `claude/cycles/2026-09-03__release-v9.1/lessons_learnt_closure.md ## Carry-Forward` (most recently completed cycle, `post_ship_complete = true`). 2 items found, both scoped to `Sprint Execution | Delivery Verification` and `Post-Ship Closure` respectively — neither names Sprint Planning as a target engine. No action required at this phase; carried forward for the owning engines' own STEP 0 reads.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| None — the sole Pre-sprint Planning Required Decision (RISK-06) was resolved this session (see above). | — | — |
