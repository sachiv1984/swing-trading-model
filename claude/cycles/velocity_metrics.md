---
**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-05-20
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Created by:** ST-13 (BLG-GOV-09, v2.4)
---

# Cycle Velocity Metrics

---

## Definition

**Velocity** = Stories Completed / Stories Planned per sprint cycle.

- **Planned**: count of ST stories assigned to the sprint at sprint-planning seal (execution_state.json stories at cycle start, excluding stories added mid-cycle).
- **Completed**: count of ST stories with `status: done` at post-ship closure. Delegated stories that were unblocked and delivered count as Completed. Stories remaining `blocked` or `not_started` at cycle close do not count.
- **Range**: 0.0–1.0 nominal; >1.0 possible if mid-cycle scope additions are all completed.

---

## Velocity History

| Cycle | Planned | Completed | Velocity | Notes |
|-------|---------|-----------|----------|-------|
| v1.9  | 14      | 14        | 1.00     | No delegated items outstanding at close |
| v1.10 | 13      | 13        | 1.00     | OA-01–OA-05 deferred post-ship; counted as out-of-scope |
| v2.1  | 15      | 15        | 1.00     | All stories closed; 5 deferred actions not counted |
| v2.2  | 15      | 15        | 1.00     | LL-RP-v22-01 deferred patch not counted (governance, not ST story) |
| v2.3  | 17      | 16        | 0.94     | 1 story (ST-11 BLG-FEAT-05) remained delegated_backend at close |
| v2.4  | 17      | 17        | 1.00     | All stories closed; no deferred items |
| v2.5  | 13      | 13        | 1.00     | ST-06 delegated (frontend) — delivered and counted as completed |
| v2.6  | 15      | 15        | 1.00     | All stories closed; no deferred items |
| v2.7  | 11      | 11        | 1.00     | All stories closed; ST-01 delegated (Unblocked 2026-04-16); AC-6 frontend deferred (in-spec, not a missed story) |
| v2.8  | 8       | 8         | 1.00     | All 8 stories closed; no delegated items; no deferred stories |
| v2.9  | 15      | 15        | 1.00     | All 15 stories closed; DEV-01 P3 accepted (not a missed story); no delegated items |
| v3.0  | 16      | 16        | 1.00     | All 16 stories closed; DEV-01 P3 cross-EPIC branch deviation (not a missed story); Base44 delegation retired mid-cycle |
| v3.1  | 14      | 14        | 1.00     | All 14 stories closed; 2 frontend items reclassified delegated→autonomous and delivered; no deviations |
| v3.2  | 17      | 17        | 1.00     | All 17 stories closed; zero spec deviations; EPIC-01 required re-verification pass after P1 staging fixes but all stories delivered and verified |
| v3.3  | 17      | 14        | 0.82     | 3 frontend stories returned to backlog (ST-03/05/07 — delegated_frontend); Arc 3 backend foundation complete; 4 P3 deviations accepted |
| v3.4  | 14      | 14        | 1.00     | All 14 stories completed; IT-01–05 Arc 3 frontend + risk prompts delivered; 4 P3 deviations accepted (no P0/P1/P2) |
| v3.5  | 13      | 13        | 1.00     | Zero deviations — cleanest sprint on record; §13 gate PASS (human delegation); Arc 3 complete (IT-06); Arc 4 foundation (PO-01) |
| v3.6  | 7       | 7         | 1.00     | EPIC-02 deferred at planning (< 20 closed trades gate); 1 P3 deviation (BLG-FE-33 staging advisory); 0 stories missed |
| v3.7  | 8       | 8         | 1.00     | Zero deviations — all 8 stories delivered; EPIC-02 PT-04 gate still not met (deferred to v3.8); scored_initiatives.md OA-RP-05 resolved |
| v3.8  | 8       | 8         | 1.00     | 1 P3 deviation (DEV-EPIC04-ST09-01 — resolved same release); EPIC-02 PT-04 formally parked (gate not met); Arc 5 SI-01 foundation delivered |

**Rolling 6-cycle average (v3.3–v3.8):** 0.97

---

## Update Rule

Append a row after each post-ship closure. Values come from the cycle's `execution_state.json`:
- Planned = count of stories in execution_state at sprint-plan seal
- Completed = count of stories with `status: done` at post-ship
- Update rolling average to cover the most recent 6 completed cycles

---

## Usage

Referenced by `claude/system/roadmap_prompt.md` v4.7 STEP 1.1 Run Manifest — Cycle Velocity field.
Do not re-derive velocity from cycle artefacts directly — always read this file.
