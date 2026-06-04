---
**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-06-04 (post-ship closure 2026-06-21__release-v5.1)
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
| v3.9  | 12      | 12        | 1.00     | Zero deviations — cleanest cycle in recent series; all 5 v3.8 governance carry-forward patches resolved; Arc 5 SI-03 Red Flag Journal delivered; EPIC-05 PT-04 deferred_at_planning (gate not met) |
| v4.0  | 11      | 11        | 1.00     | AMD-20260523-01 added ST-12 (Gemini base wiring prereq) + ST-13 (Starlette CVE fix) mid-sprint; EPIC-04 PT-04 deferred_at_planning (gate not met, 4th deferral); all 11 firm stories delivered; zero spec deviations |
| v4.1  | 15      | 14        | 0.93     | ST-11 staging ACs 02–04 returned to backlog per PO discretionary deferral authority; 14/14 remaining stories done; zero spec deviations; Gemini→Claude API switch applied mid-sprint without amendment; both 2nd-recurrence escalations (OA-01, OA-02) resolved |
| v4.2  | 13      | 13        | 1.00     | All 13 stories done; zero spec deviations; cleanest sprint on record by QA metrics; governance/ops/documentation scope with no frontend changes; 6 delegation records all resolved before sprint close |
| v4.3  | 18      | 18        | 1.00     | All 18 stories done; zero spec deviations; 5 delegations (3 cancelled, 2 delegated_qa) all resolved; ANTHROPIC_API_KEY added to staging permanently; BLG-QA-27 gate cleared (CI baseline ≥5 min) |
| v4.4  | 13      | 13        | 1.00     | Zero spec deviations; 5 governance patches (ST-01–05) + OPERATIONAL_GUIDE §7.9 (ST-13); all 7 SI-02 pre-planning artefacts delivered (ST-06–12); 5 delegations all agent-mediated and resolved within sprint |
| v4.5  | 8       | 8         | 1.00     | Zero spec deviations; 4 execution_prompt.md OA patches (ST-01–04) + agent header standardization 5 files (ST-05) + SI-02 spec pre-sprint (ST-06–08: §13 PASS + metric definition + data schema); 3 delegated_decision all agent-mediated; LL-v4.5-EX-01 validated in-sprint; sixth consecutive clean verification |
| v4.6  | 18      | 18        | 1.00     | EPIC-02 (ST-06/07/08) deferred at planning — data density gate NOT MET (6th deferral; confirmed at sprint close); 2 P3 staging deviations (BLG-OPS-44/45) accepted; Arc 6 §13 PASS; 6 delegated_decision all resolved within sprint; EPIC-04 autonomous class sign-off |
| v4.7  | 8       | 8         | 1.00     | Zero deviations; all 7 delegated_decision stories agent-mediated and resolved within sprint; ST-02 conditional deferred at planning (gate clears 2026-06-21); staged verifications sprint design validated — 3 v4.6 staging ACs closed in batch (BLG-OPS-28/44/45) |
| v4.8  | 7       | 7         | 1.00     | Zero deviations; all 7 stories autonomous; ST-08 (SI-05 Phase 1) deferred_at_planning — gate clears 2026-06-21 (never entered sprint scope); execution_prompt.md v3.34→v3.35 governance patch at sprint close (LL-v4.8-EX-01 null commit_sha action-now); both EPICs autonomous class sign-off (BLG-GOV-19) |
| v4.9  | 5       | 5         | 1.00     | Zero spec deviations; all 5 stories autonomous; EPIC-04 (ST-06/ST-07) gate-deferred 2026-06-21 (never in sprint scope); 3 EPICs autonomous class sign-off (BLG-GOV-19); EPIC-03 vs main execution_state.json conflict resolved per CLAUDE.md §8 (second application); 13 pre-existing Phase B failures surfaced and fixed as RISK-02 bonus |
| v5.0  | 13      | 13        | 1.00     | Zero spec deviations; 13 stories across 4 EPICs (governance patches + product correctness + SI-05 pre-work + staging verification); 2 delegations (ST-08 delegated_qa, ST-09 delegated_decision) both resolved same-session day; all 4 EPICs autonomous class sign-off (BLG-GOV-19); cleanest mixed-type sprint on record |
| v5.1  | 6       | 6         | 1.00     | 1 P3 deviation (DEV-v51-EPIC01-01 — pass_rate computation method; BLG-SPEC-47 filed); all 6 stories autonomous; zero delegations; SI-05 Phase 1 Telegram digest delivered; BLG-FE-61 3-cycle recurrence closed; staged verification protocol filed (BLG-GOV-89) |

**Rolling 6-cycle average (v4.6–v5.1):** 1.00

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
