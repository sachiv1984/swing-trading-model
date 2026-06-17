**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-17__release-v5.9
**Published:** 2026-06-17
**Scope revision:** v1 — 2026-06-17: EPIC-02 replaced with 6 ungated ready-now items. Deferred: BLG-FE-64/41, BLG-OPS-70, BLG-GOV-112/113/115, BLG-OPS-59, BLG-GOV-130 → v5.10.

---

# Release Backlog Slice — v5.9

<!-- release-plan-marker: RP:v5.9:2026-06-17__release-v5.9 -->

**Firm stories:** 11 | **Conditional stories:** 0 | **Total:** 11

---

## EPIC-01 — Governance Simplification (SC-03–SC-07)

**Maps to:** S2-01
**Owner:** Head of Specs Team
**Sprint:** 1
**Classification:** Firm

### ST-01 — SC-03: Consolidate spec_references policy sub-variants in execution_prompt.md

**Source:** BLG-GOV-125
**Effort:** XS (~1 hour)

**Scope:** STEP 3.1.A steps 2a, 2b, 2c of `execution_prompt.md` each handle a distinct spec_references edge case as separate numbered sub-steps. Consolidate into a single unified rule with a 3-case lookup table (~25 lines → ~10 lines). No logic change.

**Acceptance Criteria:**
- AC-01: Steps 2a, 2b, 2c replaced by a single consolidated rule with a 3-case lookup table
- AC-02: All three edge cases preserved (path verify, documentation-creation, test-authoring)
- AC-03: Version bump on execution_prompt.md; prompt_change_log.md entry appended; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

### ST-02 — SC-04: Remove STEP 8.6–8.7 fatigue detection guardrail from roadmap_prompt.md

**Source:** BLG-GOV-126
**Effort:** XS (~1 hour)

**Scope:** STEPs 8.6 (Fatigue Detection Guardrail) and 8.7 (Pivot Loop) have never been triggered. First verify STEP 5 Challenger failure rule covers convergence bias (add consolidating note if narrower); then remove STEPs 8.6–8.7.

**Acceptance Criteria:**
- AC-01: STEP 5 Challenger failure rule verified to cover convergence bias; updated if narrower
- AC-02: STEPs 8.6 and 8.7 removed from roadmap_prompt.md
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

### ST-03 — SC-05: Remove dead-load advisory steps from release_planning_prompt.md

**Source:** BLG-GOV-127
**Effort:** XS (~1 hour)

**Scope:** Make STEP 5.7 (Decision Record Integrity) conditional on escalations existing. Remove or reduce STEP 1.3 (Design-Gate Language Scan) to a single-line reminder.

**Acceptance Criteria:**
- AC-01: STEP 5.7 conditional: runs only when `artifacts.escalations = present` in state.json
- AC-02: STEP 1.3 removed or reduced to a single-line note
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

### ST-04 — SC-06: Make Playwright selector check conditional on DOM changes in execution_prompt.md

**Source:** BLG-GOV-128
**Effort:** XS (<1 hour)

**Scope:** STEP 3.1.A step 13: tighten condition to "if this story modifies a DOM element targeted by existing Playwright selectors." Governance-only and backend-only stories skip the scan.

**Acceptance Criteria:**
- AC-01: Step 13 condition tightened — scan skipped for stories with no DOM changes
- AC-02: Frontend EPICs retain full scan requirement (no regression)
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

### ST-05 — SC-07: Compress Advisory Summary Block format docs in post_ship_closure.md

**Source:** BLG-GOV-129
**Effort:** XS (<30 min)

**Scope:** Compress ~20-line Advisory Summary Block format documentation to ≤5 lines with a single-sentence explanation. No behaviour change.

**Acceptance Criteria:**
- AC-01: Advisory Summary Block format documentation ≤5 lines (from ~20 lines)
- AC-02: All format elements preserved
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

## EPIC-02 — QA Coverage, Governance Audits & UX Improvement

**Maps to:** S2-02, S2-03, S2-04
**Owner:** Director of Quality; QA Lead; Head of UX & Design
**Sprint:** 1
**Classification:** All firm — no gate conditions

### ST-06 — BLG-QA-24: Yahoo Finance backoff path integration test stub

**Source:** BLG-QA-24
**Effort:** S (~0.5 day)
**Owner:** QA Lead

**Scope:** Add integration test to `tests/test_screener_data_service.py` that stubs the Yahoo Finance session, injects a 401 followed by a 200 with valid chart data, and verifies the retry occurred exactly once. Verify exponential backoff timing via mock of `_time.sleep`.

**Acceptance Criteria:**
- AC-01: Integration test runs without a live Yahoo Finance connection
- AC-02: Test verifies: 401 first call → crumb refresh → sleep called once → 200 second call → valid OHLCV result returned
- AC-03: Passes in CI
- AC-04: QA Lead sign-off

---

### ST-07 — BLG-GOV-38: DoQ sign-off date compliance audit (v3.7–v3.9)

**Source:** BLG-GOV-38
**Effort:** S (~0.5–1 day)
**Owner:** QA Lead; Director of Quality

**Scope:** Review all QA evidence files from v3.7, v3.8, and v3.9 cycles. Check: header fields present, DoQ sign-off date present, sign-off block format consistent with PR template v1.2 standard. Document findings as advisory only — sealed artefacts not modified retroactively.

**Acceptance Criteria:**
- AC-01: All QA evidence files from v3.7, v3.8, v3.9 reviewed
- AC-02: Format inconsistencies documented (missing sign-off dates, format variations)
- AC-03: Findings filed as advisory note — no retroactive modification to sealed artefacts
- AC-04: Director of Quality sign-off on findings

---

### ST-08 — BLG-QA-34: QA evidence file format audit (v3.7–v4.0)

**Source:** BLG-QA-34
**Effort:** S (~0.5 day)
**Owner:** QA Lead; Director of Quality

**Scope:** Review QA evidence files from v3.7, v3.8, v3.9, and v4.0 cycles for consistency with current standard. Check header fields, DoQ sign-off date field presence, sign-off block format. Findings are advisory only for closed cycles.

**Acceptance Criteria:**
- AC-01: All QA evidence files from v3.7–v4.0 reviewed
- AC-02: Format inconsistencies documented
- AC-03: Findings submitted to Director of Quality as advisory note
- AC-04: Director of Quality sign-off

---

### ST-09 — BLG-GOV-53: Agent idea participation tracking summary

**Source:** BLG-GOV-53
**Effort:** S (~0.5 day)
**Owner:** Director of HR

**Scope:** Produce agent participation summary across all closed idea windows (IW-20260322-01 through the most recent closed window). Per agent: window count, submission count, participation rate. Output: advisory note filed — no governance action required unless pattern identified.

**Acceptance Criteria:**
- AC-01: Participation summary produced covering all closed idea windows
- AC-02: Per-agent data: window count, submission count, participation rate
- AC-03: Filed as advisory note in appropriate governance location
- AC-04: Director of HR review and sign-off

---

### ST-10 — BLG-QA-50: Formal regression test suite baseline document

**Source:** BLG-QA-50
**Effort:** S (~0.5 day)
**Owner:** QA Lead; Director of Quality

**Scope:** Create a formal regression baseline document covering: all `backend/routers/test.py` entries with feature mapping; all Playwright spec files in `tests/e2e/` with scenario count and feature mapping; version history showing which tests were added at which release.

**Acceptance Criteria:**
- AC-01: Regression baseline document created in `docs/qa/` or `docs/testing/`
- AC-02: All test.py entries mapped to features
- AC-03: All Playwright specs listed with scenario count and feature mapping
- AC-04: Director of Quality sign-off

---

### ST-11 — BLG-FE-57: Pre-entry panel: show warning/fail count when collapsed

**Source:** BLG-FE-57
**Effort:** XS (~0.5 day)
**Owner:** Head of UX & Design

**Scope:** When PreEntryValidationPanel is collapsed and advisory status is `warn` or `fail`: show a count badge in the header ("2 warnings", "1 fail"). Additive change — does not affect expanded panel behaviour. No badge shown when all checks pass.

**Note:** Frontend-visible change — requires Playwright automated test coverage OR human staging sign-off with date recorded in DoQ sign-off block before PR opens (per CLAUDE.md §2).

**Acceptance Criteria:**
- AC-01: Collapsed header shows count of warn/fail items when advisory status is warn or fail
- AC-02: No badge shown when all checks pass (no unnecessary visual clutter)
- AC-03: Existing collapse/expand behaviour preserved
- AC-04: Playwright test covering: collapsed warn state shows badge; collapsed pass state shows no badge
- AC-05: Head of UX & Design sign-off
