---
Owner: PMO Lead
Class: Governance Record (Class 3)
Status: Final
Release: v6.1
Cycle: 2026-06-22__release-v6.1
Last Updated: 2026-06-23 (post-ship closure)
---

# Lessons Learnt Closure — v6.1 Governance Correctness, CI Quality & User Value Foundation

Generated at: post-ship closure 2026-06-23

---

## STEP 8 Classification Summary

| Classification | Count | Items |
|----------------|-------|-------|
| Immediate (prompt patches this session) | 0 | — |
| Deferred (backlog items already filed) | 2 | BLG-GOV-135, BLG-GOV-136 |
| Advisory (no backlog item, monitoring only) | 1 | Phase 4 friction #3 — QA evidence Pending CI entries (DoQ, v6.3) |
| Decision_required | 0 | — |

**No immediate prompt patches required.** All governance fixes for this cycle either shipped in the sprint itself (EPIC-01: ST-01/ST-02) or are captured in deferred backlog items for v6.2.

---

## Planning-Phase Observations — Final Disposition

| ID | Observation | Post-Ship Outcome | Status |
|----|-------------|------------------|--------|
| LP-01 | Within-Sprint Date Gate Classification working correctly — BLG-FEAT-25/PT-04 conditional correctly triggered under STEP 1.4b | Gate cleared at sprint planning (15 trades confirmed). STEP 1.4b functioned as designed. | ✅ Confirmed — no action |
| LP-02 | PT-04 carry-forward loop risk — 8+ consecutive deferrals; gate trajectory accelerating | Gate cleared at sprint planning (15 trades); EPIC-04 executed and shipped; all 4 PT-04 stories delivered and merged. Carry-forward loop closed. | ✅ Closed |
| LP-03 | Design gate sequencing governance gap — v6.0 required manual halt and state restoration | EPIC-01 (ST-01 BLG-GOV-132, ST-02 BLG-GOV-133) shipped and merged. release_planning_prompt.md STEP 4.1 + sprint_planning_prompt.md STEP -1.3 in production. Gap systematically closed. | ✅ Closed |
| LP-04 | Capacity warn — Skill-Silo ceiling constrains EPIC-01/EPIC-02 batching | Single sprint executed. EPIC-01 (3G stories), EPIC-02 (2D stories), EPIC-03 (2U stories), EPIC-04 (2U stories, conditional). Sprint planning sealing respected the ceiling via EPIC sequencing; no second sprint required. | ✅ Recorded |

---

## Phase 3 Friction — Carry-Forward

| Friction # | Item | Action Already Taken | Future Action |
|------------|------|---------------------|---------------|
| 1 | Playwright strict mode violations (SC-MB-02/02b/03/06, SC-SQ-01) | Fixed in-sprint with { exact: true } scoping | None — pattern documented in lessons_learnt_cycle.md. No backlog item needed. |
| 2 | SetupQualityScorePanel queryFn envelope unwrap bug | Fixed in-sprint (simplified to return api.tradePlans.setupQualityScore() directly) | None — documented. Consistent pattern in other api.*() callers. |
| 3 | Cross-EPIC merge conflict resolution — 5 shared files, 12 conflict blocks in execution_state.json | Resolved per CLAUDE.md §8 in-sprint | None — CLAUDE.md §8 procedure confirmed sufficient. |
| 4 | Playwright registration friction (BLG-QA-62 structural fix pending) | ST-04 delivered manual fix; BLG-QA-62 remains open | Priority recommendation: schedule BLG-QA-62 within next 2 sprints. No new backlog item needed. |

---

## Phase 4 Friction — Deferred Items

### Deferred Item 1: BLG-GOV-135 (target v6.2)

**Item:** Autonomous class sign-off (BLG-GOV-19) misapplied to EPIC-03 and EPIC-04. Sprint Execution Engine interpreted criterion 3 (no frontend-visible change) as satisfied by Playwright coverage rather than as a binary check on frontend-visible changes.

**Resolution applied this cycle:** Retrospective DoQ counter-sign applied at delivery verification 2026-06-23. No quality gap in delivered ACs.

**Backlog action:** BLG-GOV-135 filed — add explicit pre-PR-open check in execution_prompt.md that detects frontend-visible changes and enforces DoQ counter-sign path (not autonomous class). Requires Head of Specs Team sign-off per §6 checklist. Target: v6.2.

**Classification:** Deferred — BLG-GOV-135 (v6.2)

---

### Deferred Item 2: BLG-GOV-136 (target v6.2)

**Item:** test_scenarios in execution_state.json for EPIC-03 contained stale prior-cycle staging scripts (v2.3 and v2.5) instead of v6.1 Playwright E2E specs. STEP 12 post-story test file check not applied correctly.

**Resolution applied this cycle:** Documented in QA evidence; actual coverage was complete (no quality gap) — Playwright specs (SC-SHM-01..04, SC-GP-01..04) confirmed in CI.

**Backlog action:** BLG-GOV-136 filed — add validation step in execution_prompt STEP 12 (or STEP 3.2.A) that cross-checks test_scenarios file paths against current cycle_id and rejects prior-cycle staging script paths. Target: v6.2.

**Classification:** Deferred — BLG-GOV-136 (v6.2)

---

### Advisory Item 3: QA Evidence Pending CI Entries (no backlog item)

**Item:** ST-04 QA evidence AC-04 showed ⏳ Pending CI at sprint close; PR merged (CI implied passed) but evidence not updated. Documentation gap.

**Note:** Low severity — merged PR status is sufficient evidence of CI pass. No quality gap. DoQ recommendation: consider advisory in sprint close STEP 5 to update Pending CI entries in QA evidence before sealing.

**Classification:** Advisory — Director of Quality, v6.3 consideration. No backlog item filed.

---

## Audit Cadence Check

- completed_cycle_count before this closure: 46
- After increment: 47
- 47 % 3 = 2 — **Audit NOT due** (next audit due at count = 48)
- last_audit_cycle_count: 46 → updated to 47 (no new audit triggered)

---

## Rebalance Cadence Check

- completed_cycle_count after increment: 47 (odd)
- **REBALANCE NOT DUE** at even count — count 47 is odd
- ⚠ **CORRECTION:** completed_cycle_count was 46 before closure. After increment to 47, count is now 47 (odd). Rebalance was due at count 46 (even). The rebalance advisory fires against the pre-increment count (46 = even).
- **REBALANCE DUE advisory confirmed:** completed_cycle_count was 46 (even) at cycle close. Run `run roadmap --reason "scheduled"` before next `plan release`.

---

## Endpoint Coverage Drift

- 2 new paths added in v6.1 not yet in api_performance_baseline.md:
  - GET /portfolio/sector-weights (EPIC-03, ST-06)
  - GET /trade-plans/setup-quality-score (EPIC-04, ST-08)
- BLG-OPS-75 filed (target v6.2) to add both measurement rows.

---

## Deferred Backlog Items — Carry-Forward Confirmation

| BLG ID | Summary | Target | Status |
|--------|---------|--------|--------|
| BLG-GOV-135 | Execution prompt: hard gate for autonomous class when frontend-visible changes detected | v6.2 | Open — carry-forward |
| BLG-GOV-136 | Execution prompt: test_scenarios path validation against current cycle_id | v6.2 | Open — carry-forward |
| BLG-OPS-75 | api_performance_baseline.md: add 2 new v6.1 endpoints | v6.2 | Open — filed this closure |
| BLG-QA-61 | signals_scenarios.md review vs ST-01 sizing model changes | Before next signal sprint | Open — carry-forward |
| BLG-QA-62 | Playwright spec auto-registration via glob pattern | Next 2 sprints | Open — carry-forward (priority recommendation) |
