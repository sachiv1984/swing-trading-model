---
Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-06-23
Cycle: 2026-06-22__release-v6.1
---

# Lessons Learnt — 2026-06-22__release-v6.1

## Phase 3 — 2026-06-22__release-v6.1

### Friction Log

| # | Area | Friction Observed | Root Cause | Resolution Applied | Action |
|---|------|-------------------|------------|-------------------|--------|
| 1 | Playwright CI | Strict mode violations in morning-briefing.spec.js (SC-MB-02, SC-MB-02b, SC-MB-03, SC-MB-06) and screener-quality.spec.js (SC-SQ-01) caused CI failure after spec registration (ST-04). getByText() case-insensitive substring matching hit SignalStatusCard text, empty-state text, and stale advisory text on the same page. | Playwright getByText() defaults to case-insensitive substring match. Tests written against isolated pages fail on full-page renders with other components. | Fixed in 2 commits: { exact: true } on card title/empty-state assertions; scoped /new signals today/ to [data-testid="morning-briefing"]. | No template change needed — pattern documented here. Spec author checklist: always scope page-wide getByText() with exact:true or testid scoping when component is co-rendered with other panels. |
| 2 | Frontend API client | SetupQualityScorePanel (ST-09) queryFn checked res.status after doFetch() had already unwrapped the {status,data} envelope. res was the unwrapped data object; res.status was undefined; component always returned null. Not caught locally because the component renders without error — it simply returns null silently. | doFetch() returns json.data when response has {status,data} envelope. The queryFn pattern copied from older code that used raw:true was incompatible with the standard doFetch return. | Simplified queryFn to return api.tradePlans.setupQualityScore(ticker) directly. doFetch() already throws on error. | No backlog item needed. Pattern is consistent across other api.*.xxx() calls — apply same simplification if seen in future. |
| 3 | Cross-EPIC conflict resolution | EPIC-04 merged after EPIC-01/02/03, requiring conflict resolution on 5 shared files. The execution_state.json add/add conflict had 12 conflict blocks. playwright.yml needed union of all 3 EPIC additions (26 spec files). SC-SS-01b needed updating from 68→69 after both sector-weights and setup-quality-score endpoints were added. | Sequential EPIC merges that all touch shared infrastructure files (test.py, playwright.yml, openapi.yaml, System Status) necessarily produce merge conflicts. | Resolved per CLAUDE.md §8 (union of completed items, most-current state). test.py and SystemStatus.js updated to 69 at conflict resolution. | No process change needed — CLAUDE.md §8 procedure is sufficient. Observation: the EPIC-04 note in ST-09 correctly anticipated the rebase requirement; include explicit "files to update at merge" in ST notes going forward. |
| 4 | Playwright registration process | ST-04 (register specs in playwright.yml) existed specifically because specs were written in a prior sprint but not registered, then re-used in this sprint. This is the second time this BLG-QA pattern has occurred (v6.0 was the first). BLG-QA-62 (auto-registration via glob) was filed at v6.0 sprint close. | Explicit file list in playwright.yml requires manual registration for each new spec. | ST-04 implemented the manual fix. BLG-QA-62 is the structural fix. | No new action — BLG-QA-62 already filed and open. Priority recommendation: schedule BLG-QA-62 within next 2 sprints to eliminate this class of ST. |

### Summary

Sprint executed cleanly from a governance perspective — no escalations, no blocked stories, no delegated items. All 9 stories merged and verified. Two CI fixes required post-merge (Playwright strict mode, queryFn bug) but both were diagnosed and fixed within the same session. Conflict resolution at EPIC-04 merge was the heaviest mechanical step.

**No new backlog items from this sprint.** BLG-QA-62 (filed v6.0) remains the structural fix for the registration friction. No new template changes applied this sprint.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-06-22__release-v6.1
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-06-23
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Autonomous class sign-off (BLG-GOV-19) misapplied to EPIC-03 and EPIC-04 — Sprint Execution Engine ticked criterion 3 (no frontend-visible change) as met because Playwright covered all observable ACs; criterion is binary and independent of Playwright coverage | Phase 4 | A | defer | File BLG-GOV-135: add explicit pre-PR-open check in execution_prompt.md that detects any story with frontend-visible changes in the EPIC and enforces DoQ counter-sign path (not autonomous class); template advisory in qa_evidence_template.md v1.1 (v3.7) was insufficient | Head of Specs Team | v6.2 |
| test_scenarios in execution_state.json for EPIC-03 populated with stale prior-cycle staging scripts (v2.3 and v2.5) instead of v6.1 Playwright E2E specs (sector-heatmap.spec.js, gate-progress.spec.js); STEP 12 post-story test file check was not applied correctly | Phase 4 | A | defer | File BLG-GOV-136: add validation step in execution_prompt STEP 12 (or STEP 3.2.A) that cross-checks test_scenarios file paths against the current cycle_id — reject paths referencing prior cycle staging scripts; actual coverage was complete per QA evidence (no quality gap) | Head of Specs Team | v6.2 |
| ST-04 QA evidence AC-04 shows ⏳ Pending CI at sprint close; PR merged (CI implied passed) but evidence not updated; creates documentation gap for delivery verification | Phase 4 | B | defer | Low priority — merged PR status is sufficient evidence of CI pass; however, consider adding a sprint close STEP 5 advisory to update any Pending CI entries in QA evidence before sealing | Director of Quality | v6.3 |

**Recurrence Notes:**
- Friction item 1 (autonomous class misapplication) is a **Recurrence**. Prior action: `qa_evidence_template.md` v1.1 in v3.7 added a "criterion 3 fail-path advisory" for BLG-GOV-19 (System Status Report entry 2026-05-18). That advisory was applied but proved insufficient — the engine interpreted criterion 3 as met via Playwright coverage, not as a binary check on frontend-visible changes. Prior outstanding action was completed (v3.7 template); this is a new escalation requiring a harder gate in the execution prompt itself (BLG-GOV-135). Surfacing to Head of Specs Team per recurrence protocol.
- Friction items 2 and 3: first occurrence this cycle.
