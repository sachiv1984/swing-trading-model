Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Sealed
Last Updated: 2026-06-17
Cycle: 2026-06-17__release-v5.9

---

# Sprint Backlog — v5.9

## Sprint Scope

**Release:** v5.9 — Governance Simplification, QA Coverage & UX Improvement
**Cycle:** 2026-06-17__release-v5.9
**Sprint:** 1 (single sprint)
**Stories:** 11 firm | 0 conditional | 11 total
**EPICs:** 2

## Merge Order

**EPIC-01 → EPIC-02**

- `execution_state.json` owner: **EPIC-01** (first in merge order)
- EPIC-02 branch must check for `execution_state.json` before creating; append EPIC-02 section if found
- No shared source files across EPICs — no rebase conflicts expected

## Sprint Goal

Simplify five governance prompts (SC-03–SC-07) to reduce per-cycle overhead, complete QA coverage baseline documentation and audit records, and deliver the pre-entry validation warning badge UX improvement.

*Confirmed by Product Owner: 2026-06-17*

---

## EPIC-01 — Governance Simplification (SC-03–SC-07)

**Branch:** `exec/2026-06-17__release-v5.9/EPIC-01`
**Owner:** Head of Specs Team
**Delegation class:** autonomous
**execution_state.json owner:** Yes (EPIC-01 creates this file)

---

### ST-01 — SC-03: Consolidate spec_references policy sub-variants in execution_prompt.md

**Source:** BLG-GOV-125
**Effort:** XS (~1 hour)
**Owner:** Head of Specs Team
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None
**spec_references:** stage4_backlog_slice.md#ST-01

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-01`
- AC-01: Steps 2a, 2b, 2c replaced by a single consolidated rule with a 3-case lookup table
- AC-02: All three edge cases preserved
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

### ST-02 — SC-04: Remove STEP 8.6–8.7 fatigue detection guardrail from roadmap_prompt.md

**Source:** BLG-GOV-126
**Effort:** XS (~1 hour)
**Owner:** Head of Specs Team
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None
**spec_references:** stage4_backlog_slice.md#ST-02

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-02`
- AC-01: STEP 5 Challenger failure rule verified to cover convergence bias; updated if narrower
- AC-02: STEPs 8.6 and 8.7 removed from roadmap_prompt.md
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

### ST-03 — SC-05: Remove dead-load advisory steps from release_planning_prompt.md

**Source:** BLG-GOV-127
**Effort:** XS (~1 hour)
**Owner:** Head of Specs Team
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None
**spec_references:** stage4_backlog_slice.md#ST-03

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-03`
- AC-01: STEP 5.7 conditional: runs only when `artifacts.escalations = present` in state.json
- AC-02: STEP 1.3 removed or reduced to a single-line note
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

### ST-04 — SC-06: Make Playwright selector check conditional on DOM changes in execution_prompt.md

**Source:** BLG-GOV-128
**Effort:** XS (<1 hour)
**Owner:** Head of Specs Team
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None
**spec_references:** stage4_backlog_slice.md#ST-04

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-04`
- AC-01: Step 13 condition tightened — scan skipped for stories with no DOM changes
- AC-02: Frontend EPICs retain full scan requirement (no regression)
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

### ST-05 — SC-07: Compress Advisory Summary Block format docs in post_ship_closure.md

**Source:** BLG-GOV-129
**Effort:** XS (<30 min)
**Owner:** Head of Specs Team
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None
**spec_references:** stage4_backlog_slice.md#ST-05

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-05`
- AC-01: Advisory Summary Block format documentation ≤5 lines (from ~20 lines)
- AC-02: All format elements preserved
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

## EPIC-02 — QA Coverage, Governance Audits & UX Improvement

**Branch:** `exec/2026-06-17__release-v5.9/EPIC-02`
**Owner:** Director of Quality; QA Lead; Head of UX & Design
**Delegation class:** autonomous
**execution_state.json owner:** No — append EPIC-02 section to EPIC-01's file

---

### ST-06 — BLG-QA-24: Yahoo Finance backoff path integration test stub

**Source:** BLG-QA-24
**Effort:** S (~0.5 day)
**Owner:** QA Lead
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None
**spec_references:** stage4_backlog_slice.md#ST-06

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-06`
- AC-01: Integration test runs without a live Yahoo Finance connection
- AC-02: Test verifies 401 → crumb refresh → sleep once → 200 → valid OHLCV result
- AC-03: Passes in CI
- AC-04: QA Lead sign-off

---

### ST-07 — BLG-GOV-38: DoQ sign-off date compliance audit (v3.7–v3.9)

**Source:** BLG-GOV-38
**Effort:** S (~0.5–1 day)
**Owner:** QA Lead; Director of Quality
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None
**spec_references:** stage4_backlog_slice.md#ST-07

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-07`
- AC-01: All QA evidence files from v3.7, v3.8, v3.9 reviewed
- AC-02: Format inconsistencies documented
- AC-03: Findings filed as advisory note — no retroactive modification to sealed artefacts
- AC-04: Director of Quality sign-off on findings

---

### ST-08 — BLG-QA-34: QA evidence file format audit (v3.7–v4.0)

**Source:** BLG-QA-34
**Effort:** S (~0.5 day)
**Owner:** QA Lead; Director of Quality
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None
**spec_references:** stage4_backlog_slice.md#ST-08

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-08`
- AC-01: All QA evidence files from v3.7–v4.0 reviewed
- AC-02: Format inconsistencies documented
- AC-03: Findings submitted to Director of Quality as advisory note
- AC-04: Director of Quality sign-off

---

### ST-09 — BLG-GOV-53: Agent idea participation tracking summary

**Source:** BLG-GOV-53
**Effort:** S (~0.5 day)
**Owner:** Director of HR
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None
**spec_references:** stage4_backlog_slice.md#ST-09

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-09`
- AC-01: Participation summary produced covering all closed idea windows
- AC-02: Per-agent data: window count, submission count, participation rate
- AC-03: Filed as advisory note in appropriate governance location
- AC-04: Director of HR review and sign-off

---

### ST-10 — BLG-QA-50: Formal regression test suite baseline document

**Source:** BLG-QA-50
**Effort:** S (~0.5 day)
**Owner:** QA Lead; Director of Quality
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None
**spec_references:** stage4_backlog_slice.md#ST-10

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-10`
- AC-01: Regression baseline document created in `docs/qa/` or `docs/testing/`
- AC-02: All test.py entries mapped to features
- AC-03: All Playwright specs listed with scenario count and feature mapping
- AC-04: Director of Quality sign-off

---

### ST-11 — BLG-FE-57: Pre-entry panel: show warning/fail count when collapsed

**Source:** BLG-FE-57
**Effort:** XS (~0.5 day)
**Owner:** Head of UX & Design
**Delegation class:** autonomous
**Status at sprint open:** ready
**Staging-only ACs:** None (Playwright automated test coverage required — AC-04)
**spec_references:** stage4_backlog_slice.md#ST-11

**Note:** Frontend-visible change — Playwright test coverage required (AC-04) before PR opens. Per BLG-GOV-72(c): additive badge change against defined spec with Playwright ACs — classified autonomous.

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-11`
- AC-01: Collapsed header shows count of warn/fail items when advisory status is warn or fail
- AC-02: No badge shown when all checks pass
- AC-03: Existing collapse/expand behaviour preserved
- AC-04: Playwright test covering collapsed warn state shows badge; collapsed pass state shows no badge
- AC-05: Head of UX & Design sign-off

---

## Product Owner Sign-Off

Product Owner: Confirmed
Date: 2026-06-17

All acceptance criteria reviewed and confirmed. No `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders outstanding. No outstanding actions marked `Blocker? Yes`. Sprint goal confirmed.

**Staging-only AC check (STEP 6.2):** ST-11 Staging-only ACs field = None — AC-04 requires Playwright automated coverage (not staging-only); CI-verifiable. All other stories have no staging-only ACs. Check PASS.
