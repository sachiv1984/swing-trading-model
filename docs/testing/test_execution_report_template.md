**Owner:** QA Lead
**Class:** Governance Template (Class 6)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-25
**Lifecycle Guide:** `claude/charter/document_lifecycle_guide.md`
**Governing process:** `docs/team_skills/quality/defect_lifecycle.md`

---

# Test Execution Report Template

> **How to use this template:**
> Copy this file. Replace all `[PLACEHOLDER]` values. Remove this instruction block and any sections that do not apply (e.g. remove §2.2 for manual-only runs). Do not remove the DoQ sign-off block — it is mandatory on every report.
>
> **File naming convention:** `test_execution_report_[STORY_ID]_[YYYYMMDD].md`
> **Storage location:** `claude/cycles/[CYCLE_ID]/` or `docs/testing/reports/` per the active cycle's QA evidence log.

---

# Test Execution Report — [STORY_ID]: [Story Title]

**Cycle:** [CYCLE_ID, e.g. 2026-03-24__release-v2.3]
**EPIC:** [EPIC-XX]
**Story:** [ST-XX]
**Backlog item:** [BLG-XX-YY]
**QA Lead:** [Name or "engine"]
**Execution date:** [YYYY-MM-DD]
**Environment:** [staging / local / CI]
**Report version:** 1.0

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | [YYYY-MM-DD] | Initial execution |

---

## 1. Scope

**What is being tested:** [One paragraph. State the feature, the spec source(s), and the boundary of this test run.]

**Spec sources:**

| Document | Version | Section |
|----------|---------|---------|
| [e.g. docs/specs/frontend/pages/analytics.md] | [v1.6] | [§Metrics Staleness Indicator] |

**Acceptance criteria in scope:**

| AC # | Criterion (verbatim from spec or backlog slice) |
|------|-------------------------------------------------|
| AC-1 | [text] |
| AC-2 | [text] |

---

## 2. Test Execution

### 2.1 Run Configuration

> Complete this section for **automated runs** (Playwright, pytest, CI). For manual-only runs, write "Manual execution — no automated runner." and skip the table.

| Field | Value |
|-------|-------|
| Test runner | [Playwright 1.58.2 / pytest 9.0.2 / other] |
| Spec file(s) / test file(s) | [e.g. tests/e2e/chart-interactivity.spec.js] |
| Run command | [e.g. `npx playwright test tests/e2e/chart-interactivity.spec.js`] |
| CI workflow | [e.g. .github/workflows/playwright.yml — job: playwright-chart-interactivity] |
| Data / seed used | [e.g. tests/e2e/mocks/analytics-mock-data.js / seed_all.sh] |
| Environment URL | [e.g. staging URL or localhost:3000] |
| Run output artifact | [link or path to CI run log, if applicable] |

### 2.2 Scenario Results

> One row per scenario. For automated runs, populate Result from the test runner output. For manual runs, populate from direct observation.
>
> **Result values:** `Pass` | `Fail` | `Blocked` | `N/A`
> **Type values:** `automated` | `manual` | `manual (visual)` | `hybrid`

| Scenario ID | Description | AC # | Type | Result | Notes / Evidence |
|-------------|-------------|------|------|--------|-----------------|
| [SC-XX-01] | [Brief description] | AC-1 | [type] | [Pass] | [Observation or link] |
| [SC-XX-02] | [Brief description] | AC-2 | [type] | [Fail → DEF-001] | [What was observed vs expected] |

### 2.3 Pass / Fail Summary

| Result | Count |
|--------|-------|
| Pass | [N] |
| Fail | [N] |
| Blocked | [N] |
| N/A | [N] |
| **Total scenarios** | **[N]** |

**All AC covered:** [Yes / No — if No, list uncovered AC numbers and reason]

---

## 3. Defects

> Raise one defect record per distinct divergence from canonical spec. Follow severity classification in `defect_lifecycle.md §2`. All defects are assigned to Head of Engineering on raise.
>
> If no defects were raised, write "No defects raised."

### 3.1 Defect Summary

| Severity | Raised | Resolved | Accepted (Medium only) | Open |
|----------|--------|----------|------------------------|------|
| Critical | [N] | [N] | — | [N] |
| High | [N] | [N] | — | [N] |
| Medium | [N] | [N] | [N] | [N] |
| Low | [N] | [N] | — | [N] |

> All Open counts must be zero before Director of Quality sign-off is granted.

### 3.2 Defect Records

> One block per defect. Use sequential IDs within this report.

```
ID:                DEF-001
Severity:          [Critical / High / Medium / Low]
Title:             [One sentence — wrong behaviour]
Scenario:          [SC-XX-02 — or multiple IDs]
Steps to reproduce:
  1. [step]
  2. [step]
Expected result:   [From test scenario or canonical spec]
Actual result:     [What was observed]
Canonical source:  [Spec doc and section that defines expected behaviour]
Hypothesis:        [QA Lead's view on root cause — not authoritative]
Assigned to:       Head of Engineering
Raised:            [YYYY-MM-DD]
Status:            Open
```

> **Re-verification record** (update when resolved):

```
Resolution:        [What was changed, where, and why it addresses the root cause]
Re-verified by:    QA Lead
Re-verification date: [YYYY-MM-DD]
Re-verification result: [Pass / Fail]
Status:            Resolved
```

---

## 4. Observations

> Observations are not defects. They are notable behaviour, UX concerns, or risk flags not covered by an acceptance criterion. See `defect_lifecycle.md §8` for the full process.
>
> If no observations were made, write "No observations."

| OBS ID | Description | Disposition |
|--------|-------------|-------------|
| OBS-001 | [What was noticed and why it is notable] | [Raised as BLG-XX / Deferred / Closed — reason] |

---

## 5. Coverage Gaps

> List any acceptance criteria, scenarios, or endpoints that could not be covered in this run, with the reason. If none, write "No coverage gaps."

| Gap | Reason | Disposition |
|-----|--------|-------------|
| [AC-N / SC-XX-NN / endpoint] | [Reason — e.g. staging environment not available] | [Deferred to [date] / Raised as backlog item BLG-XX] |

---

## 6. Deviation Notes

> If any implemented behaviour was found to diverge from the canonical spec and a formal deviation record was filed, list it here.
>
> If no deviations were filed, write "No deviations filed."

| DEV ID | Story | Summary | Status |
|--------|-------|---------|--------|
| [DEV-EPIC-XX-STyy-NN] | [ST-XX] | [One line] | [Open / Resolved] |

---

## 7. Director of Quality Sign-Off

> This block is mandatory. The DoQ reviews this section and the full report before signing. Criteria per `defect_lifecycle.md §6`.

**Pre-sign-off checklist (DoQ completes):**

- [ ] All acceptance criteria have a corresponding scenario result
- [ ] All Critical and High defects are Resolved with re-verification Pass
- [ ] All Medium defects are Resolved or formally accepted with written rationale
- [ ] All Low defects are recorded
- [ ] All observations have a documented disposition (not silently dropped)
- [ ] All coverage gaps are documented with disposition
- [ ] Report version history reflects actual sequence of verification activity
- [ ] QA Lead who executed scenarios did not author or modify the canonical specifications under test
- [ ] Verification method is stated for any AC requiring observable UI behaviour (code review / local run / staging — per CLAUDE.md §2)

**AC verification method note:** [State the verification method used for each AC requiring observable behaviour, e.g. "AC-3 (debounce timing): verified by local run against staging; AC-4 (colour rendering): verified by staging visual inspection."]

**Sign-off decision:** [Approved / Withheld]

> If withheld: document which criterion or defect is unsatisfactory, what is required, and whether this constitutes a shipping block.

**Withheld reason (if applicable):** [text]

**Signed off by:** Director of Quality
**Date:** [YYYY-MM-DD]
