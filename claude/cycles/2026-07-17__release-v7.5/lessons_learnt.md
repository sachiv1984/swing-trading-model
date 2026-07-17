**Owner:** Head of Specs Team
**Status:** Complete
**Release:** v7.5
**Cycle:** 2026-07-17__release-v7.5
**Last Updated:** 2026-07-17

---

# Lessons Learnt — v7.5 UI Feature Expansion Continuation

## Friction Items

1. **Roadmap section for v7.5 did not exist at invocation time — third consecutive cycle requiring an out-of-band formalization write.** `current_roadmap.md` §3 still carried `BLG-FE-115/116/117/118` unversioned. Resolved by repeating the DL-068 direct-write pattern (DL-071), per explicit user direction to bypass the now-available `run roadmap` STEP 8.1 condition-1b path (closes `BLG-GOV-240`) in favour of speed. This is a deliberate, informed choice each time, not a process gap — but it means the compliant path added at v9.2 has not actually been exercised for a real cycle yet. Recommend: no prompt change — the fix exists and works as designed; it's simply not the path chosen operationally.

2. **Same 4 items hit the same Design Gate blocker for a second consecutive release-planning pass.** `BLG-FE-115/116/117/118` were removed pre-seal from v7.4 by `AMD-20260717-01` because no design artefacts existed. At this session's invocation, no artefacts had been produced in the interim — the root cause (design-artefact production not sequenced ahead of the gate) had not yet been structurally fixed, only diagnosed. This release plan classifies all 4 conditional and explicitly requires artefact production as a precursor step before `run design-gate`, rather than repeating the v7.4 scheduling error — but this is a plan-level mitigation, not a verified fix; it will only be proven if Design Gate actually passes this time. If it fails again for the same reason, that would be a 2nd consecutive occurrence crossing STEP 1.4a's mandatory-disposition threshold and should escalate to Head of Specs Team.

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | RISK-01 (design-artefact production for all 4 items) is a must-resolve-before-sprint-planning-seal item. | Design Gate Engine (`run design-gate --cycle 2026-07-17__release-v7.5`) must confirm artefacts exist and PASS for all 4 items before `plan sprint` seals; if it fails again, this crosses the Perennial-Return mandatory-disposition threshold. | Design Gate / Sprint Planning |
| 2 | `BLG-GOV-249` (DL-069 capacity baseline ~24–28 days/sprint reflected correctly in `sprint_capacity.md`) has now been forwarded unresolved across 2 consecutive release-planning cycles (v7.4, v7.5). | Sprint Planning Engine STEP -1 should close this out explicitly this time rather than forwarding it a third time. | Sprint Planning |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-17__release-v7.5",
  "phase": "Release",
  "filed_utc": "2026-07-17T18:42:00Z",
  "friction_item_count": 2,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
