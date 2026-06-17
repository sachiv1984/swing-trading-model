Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-06-17
Cycle: 2026-06-17__release-v5.8

---

# Lessons Learnt — Post-Ship Closure — v5.8

## Closure-Phase Observations

| ID | Observation | Type | Classification |
|----|-------------|------|----------------|
| CL-v58-01 | Scope and decisions documents were both in `Published` status (not `Active`) at closure time — supersession went smoothly but the status convention differs from prior cycles where `Active` was the pre-closure state. No impact on closure. | Process observation | Deferred |
| CL-v58-02 | All §6/§7 Specs_Index entries were already RESOLVED — closure step was a no-op. Confirms clean spec debt position entering v5.9. | Positive | No action |
| CL-v58-03 | Ghost backlog entries (BLG-GOV-116/117/118, BLG-BE-34, BLG-GOV-120) identified by LL-RP-v58-03 were confirmed present in backlog.md without ✅ markers despite being archived in backlog_archive.md. These are addressed in STEP 12 groom backlog subroutine. | Process gap | Immediate (STEP 12) |

## Consolidated Action Summary

**Records reviewed:**
- `claude/cycles/2026-06-17__release-v5.8/lessons_learnt.md` (Release Planning — 3 items)
- `claude/cycles/2026-06-17__release-v5.8/lessons_learnt_cycle.md` (Phase 3 — 3 items; Phase 4 — 0 items)

### Immediate actions applied: 1

| # | Action | Document updated | Version |
|---|--------|-----------------|---------|
| 1 | LL-RP-v58-03: Ghost backlog entries (BLG-GOV-116/117/118/BLG-BE-34/BLG-GOV-120) confirmed as shipped-but-unarchived — addressed via STEP 12 groom backlog which archives these entries. No template or prompt edit required. | claude/backlog/backlog.md (via STEP 12) | N/A |

### Deferred to next cycle: 4

| # | Action | Owner | Target cycle |
|---|--------|-------|-------------|
| 1 | LL-RP-v58-01: Consider whether a lightweight Now-section addition at post-ship closure would streamline the §-1.2 check in release planning (2nd consecutive cycle with same pattern) | PMO Lead | v5.9 post-ship |
| 2 | Phase-3: BLG-FE-64 gate 2026-06-21 is now time-certain — release planning for v5.9 must check gate date before excluding; plan ST-01 as first story | PMO Lead | v5.9 release planning |
| 3 | Phase-3: BLG-GOV-112/115 and BLG-OPS-59 (EPIC-02) should be treated as ineligible for release planning before 2026-07-04 to avoid a 4th consecutive gate-deferral cycle | PMO Lead | v5.9 release planning |
| 4 | Phase-3: BLG-OPS-70 (ST-03 AC-04) — confirm SI-05 deep link functionality in production at next digest delivery (~2026-06-23) | Infrastructure & Operations Owner | ~2026-06-23 |

### Escalated for decision: 0

None.

## Recurrence Check

Prior cycle lessons learnt closure: `claude/cycles/2026-06-16__release-v5.7/lessons_learnt_closure.md`

BLG-FE-64 deferral pattern noted in v5.7 closure as well (4th deferral). v5.8 marks 5th deferral — this is a recurrence but the gate date (2026-06-21) is now 4 days away from cycle start. The deferred action above (action #2) captures the forward plan. Not escalated because the gate is time-certain and the path forward is clear.

EPIC-02 3-cycle gate-deferral pattern (v5.5/v5.7/v5.8) is a recurrence. Captured in deferred action #3 — release planning must treat these items as ineligible scope before 2026-07-04. Not escalated because the gate date is fixed and cannot be changed.

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | BLG-FE-64 gate 2026-06-21 is now time-certain — it will clear during the v5.9 sprint window. This item has been returned 5 times; the next planning cycle must include it as a firm story. | Include BLG-FE-64 as firm scope at v5.9 release planning without gate check (gate clears 2026-06-21; always before v5.9 sprint open) | Release Planning |
| 2 | BLG-GOV-112/115 and BLG-OPS-59 must not enter sprint scope before 2026-07-04 — 3 consecutive gate-deferrals confirm this pattern is not anomalous | Treat these 3 items as ineligible scope in v5.9 release planning unless release open date is after 2026-07-04 | Release Planning |
| 3 | BLG-OPS-70 (ST-03 AC-04) is a trailing obligation due at ~2026-06-23 (next SI-05 digest delivery). Delivery verification for v5.9 must confirm BLG-OPS-70 outcome if unresolved. | Check BLG-OPS-70 status at v5.9 delivery verification STEP 5 | Sprint Planning |
