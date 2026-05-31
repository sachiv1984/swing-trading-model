**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Release:** v4.7
**Cycle:** 2026-05-31__release-v4.7
**Filed:** 2026-05-31

---

# Lessons Learnt — Release Planning v4.7

---

## Observations

**Observation 1 — Aged backlog items surface reliably via advisory check**

STEP 1.1 (backlog age advisory) correctly flagged BLG-FEAT-38 (Provisional-Target v4.1, 3+ cycles) and BLG-OPS-28 (Provisional-Target v4.1, 4+ cycles). Both were promoted to firm scope. The advisory mechanism is working well for surfacing items that risk perpetual deferral. No change required.

**Observation 2 — Gate proximity scan (STEP 1.4) identifies SI-05 Phase 1 gate clearing within sprint window**

BLG-GOV-67 gate (SI-01 + SI-03 live ≥30 days, clears 2026-06-21) was identified proactively via the gate proximity table. This allows conditional sprint 2 planning rather than a surprised late addition via amendment. The STEP 1.4 gate scan (shipped in v4.6 as BLG-GOV-32) is delivering value.

**Observation 3 — OA carry-forward is lean (2 items, both advisory/monitor)**

v4.6 closed with only 2 OAs, both advisory (OA-01: SI-02 gate monitor; OA-02: endpoint baseline drift). This is the leanest OA set in recent cycles. No immediate action required in v4.7 for OA items. v4.7 scope is thus driven by backlog priority rather than OA clearance.

**Observation 4 — Double capacity same as v4.6 produces low utilisation**

v4.7 firm scope (~7–9 days total effort) against double capacity (~48–56 days across two sprints) yields ~14–17% utilisation. This is very low but correct — available actionable items constrain scope, not capacity. For v4.8, Product Owner should assess whether double capacity remains appropriate or whether standard capacity (~12–14 days/sprint) better matches available actionable scope.

---

## Action Classification

| # | Observation | Action | Owner | When |
|---|-------------|--------|-------|------|
| 1 | Aged backlog advisory working well | No action | — | — |
| 2 | Gate proximity scan delivering value | No action | — | — |
| 3 | OA set lean — no v4.7 OA clearance stories needed | No action | — | — |
| 4 | Double capacity likely oversized for v4.7 actual scope | Advisory: PO review capacity model at v4.8 planning | Product Owner | v4.8 release planning |

---

// ARTEFACT_STATUS
```json
{
  "phase": "Release",
  "cycle_id": "2026-05-31__release-v4.7",
  "release": "v4.7",
  "status": "filed",
  "filed_utc": "2026-05-31T12:15:00Z",
  "action_now_count": 0,
  "deferred_count": 1,
  "carry_forward_count": 0
}
```
