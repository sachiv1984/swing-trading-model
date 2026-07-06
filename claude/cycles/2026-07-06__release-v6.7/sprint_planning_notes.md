**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-06
**Cycle:** 2026-07-06__release-v6.7

# Sprint Planning Notes — 2026-07-06__release-v6.7

## Backlog Slice Source

Original — `claude/cycles/2026-07-06__release-v6.7/stage4_backlog_slice.md`. `.claude_current_state.json` and `state.json` both carry `amended_backlog_slice_path: ""` — no amendment in effect.

## Acceptance Criteria Confirmation (STEP 4)

All 7 items' acceptance criteria (as filed in `stage4_backlog_slice.md`) confirmed against the §7 standard (Technical / Quality / Security / Verification). None required drafting from scratch — all four dimensions are already covered by the existing AC language, mapped below for Head of Specs Team sign-off:

| Item | Technical | Quality | Security | Verification |
|------|-----------|---------|----------|---------------|
| ST-01 (BLG-FE-87) | AC-01: systematic replacement of failing `text-slate-500` dark-theme instances, verified per-surface | AC-02: contrast spot-checks recorded for representative sample | N/A — pure text-colour class change, no security surface touched | AC-03: Playwright coverage or recorded staging sign-off (CLAUDE.md frontend-visible rule) |
| ST-02 (BLG-FE-88) | AC-01: paired `dark:`/light-mode class combination added per affected surface | AC-02: prioritised by page traffic/visibility | N/A — pure text-colour class change | AC-03: Playwright coverage or recorded manual light-theme QA pass (highest-traffic pages minimum) |
| ST-03 (BLG-FE-89) | AC-01: canonical secondary-text token/component defined | AC-01 (design decision reviewed and approved in `design_gate.md`, Head of UX & Design + Product Owner) | N/A — documentation/design-system definition only | AC-02: frontend spec (`design_system.md`) updated to reference it — Director of Quality confirms transcription matches `ux_spec.md` artefact exactly |
| ST-04 (BLG-GOV-167) | AC-01/AC-02: write-scope provision added to `shared_standards.md`; diff-verification step added to `commit-check/SKILL.md` | Confirmed via direct read of both files post-change | N/A — governance prompt/skill text only | AC-03: 3-cycle carry-forward item closed in `prompt_change_log.md` |
| ST-05 (BLG-GOV-168) | AC-01: single canonical verification procedure block in `shared_standards.md` | AC-03: confirmed via direct read of each of the 4 engines' actual write steps — not documentation alone | N/A — governance prompt text only | AC-02: all 4 engines reference and apply the block |
| ST-06 (BLG-GOV-169) | AC-01: `audit.py` SLA block states same-session commit requirement | Confirmed via direct read of `audit.py` | N/A — governance script text only | Direct read confirms the SLA line present |
| ST-07 (BLG-GOV-170) | AC-01: STEP 6 of `delivery_verification_prompt.md` documents the status-line update | Confirmed via direct read | N/A — governance prompt text only | Direct read confirms the step present |

**Director of Quality readiness check:** No test coverage gaps flagged. ST-01/ST-02 QA evidence will require either a passing Playwright suite entry or a dated staging sign-off note per CLAUDE.md's frontend-visible-change rule; ST-03–ST-07 are documentation/governance-text changes verified by direct read, no QA test-scenario gap exists for these.

**Staging-only AC check (STEP 6.2):** No AC in this slice is staging-only-exclusive — ST-01/ST-02's Verification ACs each offer Playwright (CI-capable) as a sufficient evidence path, with staging sign-off as an alternative, not a CI-incapable requirement. **Staging-only ACs: None** for all 7 stories.

No `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders remain.

## Deferred Items

None. All 7 ST items from the authoritative backlog slice are classified `include` — within capacity (≈10.7d of ≈12–14d), owned, AC-complete, no unresolved dependency or escalation blocking any item.

## Delegation Class Confirmation

| Item | Delegation class | Justification |
|------|------------------|----------------|
| ST-01 | `delegated_frontend` | Visible UX/contrast change at scale (~90 files); does not qualify for BLG-GOV-72 autonomous fast-path (not a prop/state bug fix, rename, or locked-spec new-component build) — design gate already cleared. |
| ST-02 | `delegated_frontend` | Same defect class as ST-01, visible contrast change across ~102 files; same fast-path exclusion. |
| ST-03 | `autonomous` | Documents an already-locked design decision (`ux_spec.md`, cleared at design gate) into `design_system.md` — mechanical transcription, no new UX decision required. |
| ST-04 | `autonomous` | Governance prompt/skill-file text edit, no UX change. |
| ST-05 | `autonomous` | Governance prompt text edit only. |
| ST-06 | `autonomous` | Governance script (`audit.py`) text edit only. |
| ST-07 | `autonomous` | Governance prompt text edit only. |

LL-v2.0-P4-2 (test scenario gap) check: neither ST-01 nor ST-02 introduces a new page or new user-facing control — both are contrast-only refactors of existing UI surfaces. No `test_scenarios = "pending"` flag required in `execution_state.json`.

LL-v2.2-SP-01 (blocked-decision design artefact) check: no item in this slice is classified `delegated_decision`. Not applicable.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal (sequencing — avoid rework per backlog slice `**Depends on:**` field) | Unresolved until ST-01 merges to main |
| ST-03 | ST-01, ST-02 | Internal (recommended sequencing — documents the canonical treatment based on concrete fixes landed) | Unresolved until ST-01/ST-02 merge |
| EPIC-02 (ST-04–ST-07) | None | — | N/A — independent of EPIC-01 per `release_plan.md` Execution Plan ("Sequencing constraint: None") |

No circular dependencies detected.

## Execution Sequence

1. **EPIC-02 — Governance Process Hardening** (ST-04, ST-05, ST-06, ST-07) — all `autonomous`, no dependencies; sequenced first per the "autonomous before delegated" grouping rule (STEP 5.2). ST-06/ST-07 (XS effort) may run in parallel with ST-04/ST-05 per the release plan's sequencing note.
2. **EPIC-01 — UX & Accessibility Contrast Remediation** (ST-01 → ST-02 → ST-03, strict order) — ST-01 (`delegated_frontend`) first, ST-02 (`delegated_frontend`) after ST-01 merges to main, ST-03 (`autonomous`) last to document the canonical treatment based on the landed fixes. Design gate already cleared for all three (see `design_gate.md`).

### Multi-EPIC Execution Notes

2 EPICs in scope (> 1) — `execution_state.json` ownership rule applies. **`execution_state.json` owner: EPIC-02** (first in execution order, fully autonomous, no dependency on EPIC-01). EPIC-01's branch must check for `execution_state.json` existence before creating its own version — if found, read it and append its EPIC's section rather than overwrite.

### Shared File Ownership Advisory

No shared source files identified across EPIC-01/EPIC-02 this sprint:
- **EPIC-01 touches:** frontend component/style files carrying `text-slate-400`/`text-slate-500` classes (~90–102 files, ST-01/ST-02), `docs/specs/frontend/pages/positions.md` (v2.0), `docs/specs/frontend/pages/dashboard.md` (v2.6), `docs/specs/frontend/pages/reflections.md` (v0.2), `docs/specs/frontend/design_system.md` (ST-03).
- **EPIC-02 touches:** `claude/system/shared_standards.md`, `.claude/skills/commit-check/SKILL.md`, `claude/system/prompt_change_log.md`, `claude/audit.py`, `claude/system/delivery_verification_prompt.md`.

No overlap — no rebase-ordering constraint required at merge time beyond the general EPIC-02→EPIC-01 sequence above. Merge order for STEP 6.1: **EPIC-02 → EPIC-01**.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — ST-01/ST-02's own ACs require Playwright coverage or recorded staging sign-off, phased by page traffic/visibility, with per-surface contrast spot-checks recorded. To be verified at delivery verification. |
| RISK-02 | EPIC-01 | Valid — mitigated by the explicit sequencing constraint (ST-02 `**Depends on:**` ST-01) enforced in the Execution Sequence above; ST-01 must merge to main before ST-02 branch work begins. |
| RISK-03 | EPIC-02 | Valid — mitigation is scoping ST-04's write-scope grant narrowly to `.claude/skills/` only, naming Head of Specs Team explicitly (not open-ended), per the item's own AC-01. |
| RISK-04 | EPIC-02 | Valid — mitigation is ST-05's own AC-03 requiring direct read-verification of all 4 affected engines' actual write steps post-change, not documentation alone (this is the exact failure mode that created BLG-GOV-168 in the first place). |

No risk has materialised since release planning. All four remain valid with their originally-recorded mitigation approach.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — no known vulnerabilities found across all 59 resolved backend dependencies (fastapi 0.135.1, anthropic 0.105.2, sqlalchemy 2.0.23, pydantic 2.13.4, etc.). No High/Critical CVEs; no PO/Head of Engineering risk acceptance required.

## Hygiene Advisories (STEP -1.7)

- **Prompt change log gaps:** Verified all 11 Class 6 governed prompts (`release_planning_prompt.md` v2.41, `sprint_planning_prompt.md` v3.12, `execution_prompt.md` v3.51, `delivery_verification_prompt.md` v3.1, `post_ship_closure.md` v2.17, `design_gate_prompt.md` v1.4, `amendment_cycle_prompt.md` v1.9, `roadmap_management_prompt.md` v1.4, `backlog_management_prompt.md` v1.10, `roadmap_prompt.md` v8.3, `gh_issue_template.md` v1.0) each have a `prompt_change_log.md` entry whose target version matches the file's current `**Version:**` header exactly. No gaps found.
- **"Before Sprint Planning" backlog items:** Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v6.7 sprint planning` — no matches found. No unconverted "Before Sprint Planning" items.

## Carry-Forward Items

Most recently completed cycle: `2026-07-04__release-v6.6` (`post_ship_complete = true`). Read `lessons_learnt_closure.md ## Carry-Forward` — 2 items:

| # | Observation | Implication | Engine | Status re: v6.7 |
|---|-------------|-------------|--------|------------------|
| 1 | `/commit-check` diff-verification patch is an open escalation (`ESC-CLOSE-20260706-01`) with no routine holding write scope for `.claude/skills/` — do not let a 4th cycle pass unresolved. | Head of Specs Team must apply the patch directly or formally amend a routine's write scope before this cycle's Phase 3 friction review. | All | **Actioned this cycle** — ST-04 (BLG-GOV-167) is firm scope in EPIC-02, directly resolving this 3-cycle-carried item. Sequenced first in Execution Sequence above. |
| 2 | 2nd consecutive cycle (v6.5, v6.6) where an audit/investigation-shaped story counted as "nominal U" at scoping resolved to `D` at ship, leaving only 1 of 2 planned U-items genuinely user-facing. | Treat audit/investigation-shaped stories as `D`-leaning, not `U`, until a scoping-heuristic fix is applied. | Roadmap | **Already actioned at roadmap/release-planning level** — `roadmap_prompt.md` v8.2→v8.3 added the mandatory pull-forward clause (§7.1); this cycle's EPIC-01 (ST-01/ST-02) was selected specifically as build-and-ship-shaped, ungated U-items under the new STEP 2.4 content-based test — not a repeat of the audit/investigation-shaped pattern. |

Recorded per `shared_standards.md §16.8` — advisory only, no halt. Carry-forward items reviewed: 2 items from cycle `2026-07-04__release-v6.6`, both addressed by this cycle's scope.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| None. | — | — |

No outstanding action is a seal blocker.

## Capacity WARN Acknowledgement

Not applicable — capacity check outcome is `pass` (≈10.7d vs ~12–14d available). `capacity_warn_acknowledged` will be omitted/`false` at STEP 7.

## Pre-Sprint Backlog Advisory

Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v6.7 sprint planning` — no matches found. No unconverted "Before Sprint Planning" items.
