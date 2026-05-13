---
**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-05-13
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

**Rolling 6-cycle average (v2.8–v3.3):** 0.97

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
