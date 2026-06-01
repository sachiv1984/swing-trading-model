**Owner:** Facilitator
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.8
**Cycle:** 2026-06-01__release-v4.8
**Filed:** 2026-06-01

---

# Lessons Learnt — Release Planning v4.8

---

## Friction Items

### LL-RP-v4.8-01 — Roadmap entry missing after "No-change" rebalance

**Observed:** The 2026-06-01 rebalance ran as "No-change (roadmap)" and did not add a formal v4.8 entry to current_roadmap.md, causing STEP -1.2 to fail at release planning invocation.

**Root cause:** The roadmap_prompt.md v6.6 STEP 8.1 "Empty Now Horizon Advisory" (BLG-GOV-71, v4.4 ST-01) is non-blocking and advisory — it advises the PO to add a next-release section but does not enforce it. When the advisory fires and is acknowledged without action, the gap persists to the next planning cycle.

**Recommended action:** STEP 8.1 of `roadmap_prompt.md` should be strengthened from "advisory" to a softer gate: when the Now horizon is empty and no next-release section exists in `current_roadmap.md`, require explicit PO decision — either (a) add the v4.8 section now, or (b) defer intentionally and record in the cycle summary that release planning will require a pre-planning fix next cycle. This makes the choice explicit rather than silent.

**Classification:** Deferred — product_owner / head_of_specs_team decision
**Action:** BLG-GOV item to be filed for roadmap_prompt.md v6.7+ "Empty Now Horizon" strengthening

---

## Positive Observations

### LL-RP-v4.8-02 — Rebalance cycle summary provides adequate v4.8 evidence

The 2026-06-01 rebalance cycle_summary.md explicitly named v4.8 in 4+ places, providing sufficient evidence to justify the minimal roadmap fix and proceed. The release planning engine's "cannot invent new releases" rule was not violated — v4.8 was sanctioned, just not formally registered.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Roadmap "No-change" rebalances may omit next-release section, causing STEP -1.2 failure | Roadmap prompt STEP 8.1 advisory should be strengthened to require explicit PO decision when Now horizon is empty | Roadmap |

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-06-01__release-v4.8",
  "release": "v4.8",
  "status": "complete",
  "generated_utc": "2026-06-01T14:50:00Z"
}
