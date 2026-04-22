Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Release: v2.9
Cycle: 2026-04-22__release-v2.9
Last Updated: 2026-04-22

---

# Lessons Learnt — Release Planning v2.9

## Planning Observations

| # | Observation | Classification |
|---|-------------|----------------|
| 1 | **BLG-GOV-08 fifth consecutive deferral — retirement triggered.** Item deferred v2.4–v2.8 (5 cycles). PO decision: retire at next `groom backlog` run. The pattern of indefinite deferral for L-effort governance items with no evidence of friction is now resolved. Retirement is the correct outcome rather than indefinite re-parking. | Process observation — resolved |
| 2 | **Carry-forwards CF-1 and CF-2 from v2.8 addressed as sprint stories.** Both DoQ counter-sign requirement patches were cleanly converted to BLG-GOV-14 (ST-11) with concrete ACs. The two-cycle carry-forward mechanism is functioning as designed. | Positive — process working |
| 3 | **Arc 1 scope introduces new dependency surface area.** Two hard gates must be satisfied before Sprint 2 implementation: BLG-SPEC-22 (contract before DS-05) and BLG-GOV-16 (§13 review before DS-06). Both gates are well-specified and pre-sprint required decisions are captured in cycle_summary.md. Sprint Planning Engine should surface RISK-01 as a sprint start gate check. | New dependency pattern — advisory |
| 4 | **sprint_planning_prompt.md version gap (OA-v29-01).** The prompt is at v2.5 but the change log shows no entry for the v2.3→v2.5 transition. Advisory only — does not block execution — but indicates a log maintenance gap. Head of Specs Team should verify and backfill during sprint execution. | Process gap — advisory |

## Action Summary

### Immediate Actions Applied: 0

None required — no governance file changes identified at planning time.

### Deferred to Next Cycle: 3

| # | Action | Owner | Target |
|---|--------|-------|--------|
| 1 | OA-v29-01: Verify sprint_planning_prompt.md v2.3→v2.5 change log gap and backfill if missing | Head of Specs Team | Sprint execution (v2.9) |
| 2 | OA-v29-02: BLG-GOV-08 retirement — execute at next `groom backlog` run | Product Owner | Next groom backlog |
| 3 | OA-v29-03: CF-1/CF-2 patches (BLG-GOV-14, ST-11) — execute in Sprint 1 of v2.9 | Head of Specs Team | Sprint 1 v2.9 |

## Friction Items

| # | Description | Type | Disposition |
|---|-------------|------|-------------|
| — | None | — | — |

---

```json
// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-04-22__release-v2.9",
  "friction_item_count": 0,
  "action_now_count": 0,
  "deferred_count": 3,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
