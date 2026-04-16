# Lessons Learnt — 2026-04-13__release-v2.7

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active

---

## Phase 3 — 2026-04-13__release-v2.7

**Appended:** 2026-04-16

### Process Observations

1. **Cross-EPIC governance file conflicts at merge time (recurring).**
   EPIC-02 (ST-03/ST-04) and EPIC-05 (ST-11) both modified `OPERATIONAL_GUIDE.md` and `prompt_change_log.md` in parallel. This caused version number collisions (both wrote to v3.55–v3.57 range independently). Resolution required post-merge renumbering. A local governance commit (`[GOVERNANCE] post_ship_closure.md v2.3→v2.4`) on main added further collision surface. Mitigation: when multiple EPICs modify governance files in the same sprint, merge them in strict order and update the later EPIC branch to rebase against origin/main before raising its PR. Alternatively, defer governance file updates to a single coordinated commit at sprint close.

2. **QA sign-off blocks missing formal `Date:` field in EPIC-01, 03, 04, 05.**
   Four of five QA evidence files had dates embedded in sign-off prose rather than a formal `- Date:` field. This required STEP 5.1 remediation. Going forward: the sign-off block template (formal `Date:` line) should be used consistently in all qa_evidence files from the point of sign-off, not retrofitted at sprint close.

3. **Smoke test suite required two rounds of debugging.**
   Initial EPIC-04 smoke tests used incorrect data construction (per-element seeded RNG producing constant values; plain lists where pd.Series required; wrong function name `_compute_severity` vs `_correlation_severity`). Resolved in session but consumed time that could have been avoided with a documented test data construction pattern for Pearson correlation tests.

4. **Playwright LIFO route ordering (ST-06 root cause — cross-cycle carry).**
   Route ordering bug was a new root cause; ST-06 fix is now codified and should be applied consistently to all future Playwright test files. The fix pattern (register catch-all first, specific mocks after) should be documented in `docs/team_skills/qa/playwright_patterns.md` if that file exists, or raised as a backlog item.

### Items to Carry Forward (Non-blocking)

- **AC-6 (ST-08): Market Correlation frontend rendering.** Backend contract fully specified in `analytics_endpoints.md` v2.1.0. Frontend story to be raised in next backlog grooming.
- **Playwright fix pattern documentation.** Advisory: document LIFO pattern in a shared testing guide.

---

## Phase 4 — 2026-04-13__release-v2.7

**Appended:** 2026-04-16

### Phase 4 Friction Areas

| # | Area | Observation | Classification | Action |
|---|------|-------------|----------------|--------|
| 1 | Gate sequencing | sprint_close.md QA sign-off blocks for EPIC-01/03/04/05 used inline date format rather than formal `- Date:` field, requiring STEP 5.1 remediation at sprint close. The formal sign-off block template should be applied at time of sign-off, not retrospectively. | Process gap | Advisory: include formal `Date:` field in DoQ sign-off block template reminder in execution_prompt.md §3.2.A. No change made this cycle — monitoring only. |
| 2 | Test scenario coverage | EPIC-04 registered pre-existing scenario files (`analytics_scenarios.md` v1.0, `signals_scenarios.md` v1.0) that predate and do not cover the new v2.7 endpoints. The `test_scenarios` field in execution_state.json should only reference files that actively cover the EPIC's new functionality, not adjacent legacy files. | Scope mismatch | BLG-QA-13 created. Advisory: when populating `test_scenarios` in execution_state.json, confirm the referenced files cover the new AC rather than prior adjacent functionality. |
| 3 | Deviation severity consistency | Three sprint_close.md "deviations" were process notations (autonomous class records, exemption tokens) rather than spec deviations. The deviation register should distinguish clearly between spec deviations (P0–P3) and process notations. The sprint_close.md template conflates these. | Terminology gap | No block. Advisory: clarify that sprint_close.md "Deviations filed" should list only spec deviations; process notations belong in the notes column of execution_state.json. |
| 4 | Sign-off coordination | Both Director of Quality and Product Owner sign-offs completed in same session. No coordination friction observed. | Pass | — |

### Carry-Forward Actions

None required. BLG-QA-13 is the only open item from this verification run and is captured in backlog.md.
