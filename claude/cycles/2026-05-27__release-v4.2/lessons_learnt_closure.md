**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-27__release-v4.2
**Produced by:** Post-Ship Closure Engine (lessons_learnt_prompt.md §3.5)

---

# Lessons Learnt Closure Record — 2026-05-27__release-v4.2

## Purpose

This record consolidates all lessons learnt across the v4.2 release cycle — Release Planning, Sprint Execution, and Delivery Verification phases — and documents the classification and disposition of every action item. It is the governance record of process learning applied (or carried forward) at cycle close.

---

## Records Reviewed

| Record | File | Phase(s) | Items Identified |
|--------|------|----------|-----------------|
| Release Planning lessons | `claude/cycles/2026-05-27__release-v4.2/lessons_learnt.md` | Release Planning | 2 observations; 0 immediate actions (1 type D deferred advisory, 1 type E positive) |
| Sprint Execution + Verification lessons | `claude/cycles/2026-05-27__release-v4.2/lessons_learnt_cycle.md` | Phase 3 + Phase 4 | 7 items (Phase 3: 2 type C defer, 3 type E action-now; Phase 4: 1 type B defer, 2 type E action-now) |

Prior cycle closure checked: `claude/cycles/2026-05-26__release-v4.1/lessons_learnt_closure.md` — found.

**Prior cycle carry-forward resolution:**
- v4.1 had no carry-forward items (all v4.1 lessons were action-now positive patterns or resolved by v4.1 delivery). No outstanding items to carry forward from v4.0 closure were listed in v4.1 lessons_learnt_closure.md.

---

## Closure Phase Observations

### Document Closure Friction
- **No unusual friction.** All required artefacts were present and correctly located. Changelog, roadmap, scope, decisions, backlog, velocity metrics, and Specs Index all updated without blockers.
- **Endpoint coverage drift** (advisory): GET /ai/claude-audit-log was added in v4.2 (ST-07) and is present in openapi.yaml but absent from api_performance_baseline.md — BLG-OPS-42 filed. Normal outcome (performance re-runs require live environment).
- **No spec deviations to check** — STEP 5 passed with no action (zero deviations filed this sprint).
- **BLG-OPS-36/38/39 already marked COMPLETE** in backlog before closure run — the execution engine had marked them during sprint execution. Confirms state is being maintained in-cycle as expected.

### Action Application Rate
- 9 action items reviewed across 3 lessons learnt records.
- 0 immediate actions applied (no prompt or template edits identified as safe to apply without ambiguity at this closure run).
- 5 type E (positive) items — confirmed as working patterns, no change required.
- 3 type B/C/D defer items — classified defer to v4.3 per the lessons learnt records' own classification.
- 0 decision-required escalations.

### Whether Closure Steps Revealed Gaps
- No gaps surfaced during closure that should have been caught earlier.
- BLG-OPS-42 endpoint drift is a structural pattern (performance baselines require live runs); the backlog item is the correct vehicle.

---

## Action Item Disposition

### Release Planning Lessons (lessons_learnt.md)

| # | Item | Type | Disposition | Owner | Target |
|---|------|------|-------------|-------|--------|
| 1 | Roadmap section gap after Extended-tier rebalance — "Next planned release: [TBD]" caused STEP -1.2 hard gate at plan release invocation | D (process friction) | Deferred — advisory only; add roadmap_prompt.md advisory note at STEP 8.1 if pattern recurs in v4.3 | PMO Lead | v4.3 (if recurs) |
| 2 | BLG-GOV-58 pre-resolved before planning commenced — backlog not yet marked COMPLETE | E (positive) | Positive — BLG-GOV-58 to be marked COMPLETE at STEP 12 groom backlog run (this closure) | PMO Lead | Resolved at STEP 12 |

### Sprint Execution Lessons — Phase 3 (lessons_learnt_cycle.md)

| # | Item | Type | Disposition | Owner | Target |
|---|------|------|-------------|-------|--------|
| 3 | EPIC-01 and EPIC-02 merged between sessions — STEP 5.0A guard + merge gate sync recovered both correctly | E (positive) | Positive — merge gate resume pattern validated. No action. | — | — |
| 4 | `qa_signed_off: true` not updated in same commit as qa_evidence_EPIC-xx.md DoQ sign-off | C (process gap — minor) | Deferred — add advisory to execution_prompt.md STEP 3.2.A: update qa_signed_off: true in same commit as QA evidence file. | Head of Specs Team | v4.3 |
| 5 | All 6 delegation records resolved cleanly; 0 sign-off retries across 13 stories | E (positive) | Positive — agent-mediated sign-off pattern reliable for governance/ops class. No action. | — | — |
| 6 | Sprint close artefacts committed on EPIC-02 exec branch rather than main — execution_prompt.md STEP 8 has no branch safety check | A (process gap — minor) | Deferred — add branch safety advisory to execution_prompt.md STEP 5.3/STEP 8. Consult Head of Specs Team on preferred gate vs advisory. | Head of Specs Team | v4.3 |

### Delivery Verification Lessons — Phase 4 (lessons_learnt_cycle.md)

| # | Item | Type | Disposition | Owner | Target |
|---|------|------|-------------|-------|--------|
| 7 | Zero deviations, zero QA fails, 13/13 stories done — cleanest sprint to date | E (positive) | Positive — governance/ops sprint scope with well-defined ACs is most reliable delivery pattern. No action. | — | — |
| 8 | QA evidence AC numbering consolidation (ST-11: 4 ACs → 3 evidence rows; ST-13: 5 ACs → 3 evidence rows) — all substantive criteria met but traceability cross-reference friction at verification | B (process gap — notation) | Deferred — add advisory to qa_evidence_template.md: evidence rows should map 1:1 to backlog slice ACs; note which ACs are covered when consolidating. | Head of Specs Team | v4.3 |
| 9 | Phase 3 deferred items (qa_signed_off stale + branch safety) filed correctly; no recurrence escalations triggered; verification sign-off coordination friction: none | E (positive) | Positive — deferred item filing + verification sign-off process working correctly. No action. | — | — |

---

## Consolidated Action Summary

| Class | Count | Items |
|-------|-------|-------|
| Immediate actions applied | 0 | None |
| Deferred to next cycle (v4.3) | 3 | #4 (qa_signed_off advisory), #6 (branch safety advisory), #8 (qa_evidence_template AC mapping advisory) |
| Escalated for decision | 0 | None |
| Positive observations (no action) | 5 | #3, #5, #7, #9 + #2 resolved at STEP 12 |
| Type D deferred advisory | 1 | #1 (roadmap section gap — if pattern recurs) |

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | qa_signed_off stale state: after DoQ sign-off, execution_state.json qa_signed_off field must be updated in the same commit as the QA evidence file (execution_prompt.md STEP 3.2.A advisory) | Sprint Planning: check if this patch (target: v4.3) is in the sprint backlog before sealing | Sprint Planning |
| 2 | Branch safety gap at sprint close: sprint close artefacts may land on an exec branch; execution_prompt.md STEP 8 has no branch safety check (gate vs advisory TBD by Head of Specs Team) | Sprint Planning: check if this patch (target: v4.3) is in the sprint backlog before sealing | Sprint Planning |
| 3 | QA evidence AC numbering: evidence rows should map 1:1 to backlog ACs; qa_evidence_template.md advisory needed (target: v4.3) | Sprint Planning: check if this patch is in the sprint backlog before sealing | Sprint Planning |
