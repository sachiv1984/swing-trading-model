Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-07

# QA Evidence — EPIC-01 (2026-09-07__release-v9.2)

**EPIC:** EPIC-01 — Arc 5 Compliance Score Low-Volume Advisory
**Cycle:** 2026-09-07__release-v9.2
**Sprint goal:** Ship the Arc 5 low-volume compliance-score advisory and clear a full-capacity slate of 55 accessibility, QA/CI reliability, governance-process, and spec/tech/ops debt items across all 5 EPICs — exhausting the confirmed ~24–28 day capacity band at 27.55 days, with 0 P1/P2 debt items carried past this sprint on capacity grounds.
**Test scenarios used:** `tests/e2e/arc5-compliance-section.spec.js` (SC-ARC5-09, SC-ARC5-10a, SC-ARC5-10b — new; full file 11/11 verified, no regression to SC-ARC5-01–08)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `docs/specs/frontend/components/arc5_compliance_section.md#Low-Trade-Volume Advisory` (v1.2.0); `docs/specs/api_contracts/arc5_compliance_analytics.md#total_closed_trades` (v1.1.0) | Produced the required assessment (concluded advisory warranted); added `total_closed_trades` to `GET /analytics/arc5-compliance` (additive, non-breaking); added a static, non-dismissible Info-tone advisory banner to `Arc5ComplianceSection` when `total_closed_trades < 20` | AC-01 Assessment document produced (advisory or advisory-not-needed conclusion). AC-02 If advisory warranted: UI advisory added to Arc5ComplianceSection for sub-20-trade states. AC-03 Gate condition verified before sprint planning. | Pass | None found |

> AC-01 evidence: `docs/design/2026-09-07__release-v9.2/arc5-low-volume-advisory/assessment.md` — concludes "Advisory warranted", with Metrics Definitions & Analytics Owner sign-off. AC-02 evidence: `src/components/analytics/Arc5ComplianceSection.js` (banner), covered by `tests/e2e/arc5-compliance-section.spec.js` SC-ARC5-09/10. AC-03 evidence: `docs/design/2026-09-07__release-v9.2/arc5-low-volume-advisory/decision_record.md` §5 (Head of UX & Design + Product Owner confirmed at design gate, 2026-09-07), referenced in `sprint_backlog.md`.

**QA test coverage:**
- Scenarios run: `tests/e2e/arc5-compliance-section.spec.js` — full file, 11/11 passed (real Playwright/Chromium run, executed independently twice: once during implementation, once during agent-mediated DoQ review)
- Regression areas checked: `Arc5ComplianceSection` existing four stat cards (SC-ARC5-01–08 unchanged); `GET /analytics/arc5-compliance` existing response fields unchanged (additive field only); `tests/test_api_contracts.py` and `tests/ -k analytics` backend suites (11 passed, no regressions); `scripts/check_api_performance_baseline_drift.py` (PASSED); `scripts/check_specs_index_freshness.py` (no new drift introduced — the two touched spec files were already part of the pre-existing 78-file ST-49 backlog baseline)
- Known deviations: None found — the story's deviation check completed with nothing to file; implementation matches the locked design record's intent exactly (container classes, `Info` icon, section-scoped placement, non-dismissible behaviour, copy pattern, 20-trade threshold anchor)

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, this component uses the `api.analytics.arc5Compliance()` wrapper exclusively, no direct URL construction
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-07
- Comments: Reviewed ST-01 (EPIC-01, "Arc 5 compliance score utility advisory at low trade volume") on `exec/2026-09-07__release-v9.2/EPIC-01` @ `8c12a7df06036ed98309e6dae1d4fe624e3fd15b`. All three ACs are satisfied: the assessment document concludes "advisory warranted" with proper sign-off, the UI advisory was added to `Arc5ComplianceSection` for sub-20-trade all-time states, and the gate condition (design record locked pre-sprint) was verified. Implementation matches the locked decision record precisely — Info-tone container reused verbatim, `Info` icon, section-scoped (not `StandingAlertStack`) placement below the stat grid, non-dismissible, correct copy pattern and 20-trade threshold anchor — with a well-reasoned, properly assessed and documented backend addition (`total_closed_trades`, non-breaking, contract/openapi/docstring all updated in the same commit) to source the count. The frontend testing gate is satisfied with genuine, non-tautological Playwright coverage for both the shown and hidden banner states (SC-ARC5-09/10), independently re-run in full, confirming 11/11 pass. No regression to the 8 pre-existing scenarios. (Independent review note: `execution_state.json`'s `deviations_filed: true` for this story was queried during review — confirmed correct per the field's canonical meaning, "deviation check performed," not "a deviation was found/filed" — see `execution_state_schema.json` `_deviations_filed_note` / `shared_standards.md` §16.15. No correction needed.)

**Frontend testing gate (LL-v3.1-EX-01):** This EPIC introduces a frontend-visible change (`src/components/analytics/Arc5ComplianceSection.js`). Observable AC (banner visible/hidden, copy content) is fully covered by real Playwright tests in CI (`tests/e2e/arc5-compliance-section.spec.js` SC-ARC5-09/10) — no "code review only" items, no staging-sign-off-deferred backlog item required.

**BLG-GOV-19 autonomous class eligibility (checked, not used):** Criterion 3 (no frontend-visible change) is unmet — `src/components/analytics/Arc5ComplianceSection.js` under `src/components/**` was modified (BLG-GOV-135 detection rule). Standard Sign-Off Block above applies instead, per an agent-mediated Director of Quality review (§5.3).

## Verification Readiness (this EPIC)

| Field | Status |
|-------|--------|
| Spec references populated for all `done` ST items | Yes |
| Deviations filed (check completed) for all `done` ST items | Yes |
| DoQ sign-off non-blank | Yes |
