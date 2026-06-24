Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-24

---

# QA Evidence — EPIC-03 — Governance & QA Debt
**Cycle:** 2026-06-24__release-v6.2

---

## Per-Story Evidence: ST-13

**Story:** ST-13 — Playwright spec auto-registration via glob pattern (BLG-QA-62)
**Classification:** delegated_qa
**Commit:** 61890e35d6950cb499f58f3e3e78eb159405c002
**Status:** blocked_qa — awaiting Director of Quality sign-off

**What was built:**
`.github/workflows/playwright.yml` updated: the explicit 26-file spec list in the `playwright-e2e` job was replaced with the glob pattern `tests/e2e/**/*.spec.js`. The header comment was updated to remove the stale manual spec inventory and document the auto-discovery behaviour. No other CI or test configuration changes were made.

**Spec references:** None (CI configuration change — no prior canonical spec; notes: "no prior spec applicable")

**Acceptance criteria:**

| AC | Description | Verification method | Status |
|----|-------------|---------------------|--------|
| AC-01 | playwright.yml updated to use glob pattern `tests/e2e/**/*.spec.js` replacing explicit spec file list | Code review — diff confirms glob replaces explicit list | Pass |
| AC-02 | All existing spec files continue to run in CI (no regression) | CI: all prior Playwright scenarios pass | **Pending — Director of Quality to confirm CI green** |
| AC-03 | A new spec file added to `tests/e2e/` is automatically included without manual registration | Document inspection — no manual registration step required | Pass |

**Test scenarios to execute (DoQ verification):**
- Confirm CI run on commit 61890e35 shows all Playwright E2E scenarios passing
- Confirm no spec file from the prior explicit list was dropped from the CI run output
- Confirm the glob `tests/e2e/**/*.spec.js` is syntactically valid in the workflow

**Open section for QA findings:**
*(Director of Quality to complete)*

**Disposition:**
*(Pass / Pass with notes / Fail — Director of Quality to complete)*

---

## EPIC-Level Consolidation Block

**EPIC:** EPIC-03 — Governance & QA Debt
**Cycle:** 2026-06-24__release-v6.2
**Sprint goal:** Sprint 1: Ship the production strategy parity cluster and close governance & QA debt items.
**Test scenarios used:** Derived from spec + AC (no test_scenarios files for governance-patch stories)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-10 | claude/system/execution_prompt.md | §3.2.A Autonomous DoQ criterion 3 updated with BLG-GOV-135 detection rule (src/components/** or src/pages/** → autonomous class unavailable); qa_evidence_template.md criterion 3 updated | AC-01: detection rule added. AC-02: blocks regardless of Playwright coverage. AC-03: version bump + OPERATIONAL_GUIDE + change log. AC-04: template updated. | Pass | None |
| ST-11 | claude/system/execution_prompt.md | STEP 0 instruction 6 updated with BLG-GOV-136 advisory: test_scenarios paths must be under tests/ or tests/e2e/, not docs/testing/; schema comment corrected | AC-01: advisory added + schema comment updated. AC-02: version bump included in ST-10 batch. | Pass | None |
| ST-12 | docs/ops/api_performance_baseline.md | Deferred — Render internal logs unavailable at execution; p50/p95 values cannot be computed from code | AC-01–AC-03: not completed | Returned to backlog | N/A — not completed; BLG-OPS-75 remains in backlog |
| ST-13 | N/A (CI config change) | playwright.yml explicit 26-spec list replaced with `tests/e2e/**/*.spec.js` glob | AC-01: glob implemented. AC-02: pending CI confirmation. AC-03: auto-discovery confirmed by doc inspection. | Pending DoQ sign-off | None |

**QA test coverage:**
- Scenarios run: Manual code review + CI run (commit 61890e35)
- Regression areas checked: Playwright CI workflow; execution_prompt.md autonomous class path; test_scenarios population in execution_state.json
- Known deviations filed: None

---

## Sign-Off Block

> **Director of Quality — action required for ST-13 (AC-02):**
> Confirm all existing Playwright spec scenarios pass in the CI run on commit 61890e35 (branch exec/2026-06-24__release-v6.2/EPIC-03). Check the GitHub Actions run for "Playwright E2E Acceptance Tests" — all scenarios should pass. If they do, complete the sign-off block below.

**Autonomous class eligibility check (BLG-GOV-19):**
- [✗] Criterion 1: Not all stories autonomous (ST-13 is delegated_qa) — criterion fails
- Autonomous class does NOT apply for EPIC-03. Standard sign-off required.

- Signed off by: [AWAITING Director of Quality]
- Date: [AWAITING — must be non-blank before PR can be opened]
- Comments:
