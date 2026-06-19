Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Release: v6.0
Cycle: 2026-06-19__release-v6.0
Phase: Release Planning
Last Updated: 2026-06-19

---

# Lessons Learnt — Release Planning v6.0

## Process Observations

### What Worked Well

1. **Correctness fast-track identification** — BLG-BE-36 (signal card suggested_shares risk-based sizing) was correctly elevated to P0 position per the correctness fast-track rule introduced in roadmap_prompt v7.4. No ambiguity in sequencing; EPIC-01 was naturally the lead EPIC.

2. **Product Value Alert addressed cleanly** — With a prior rebalance ratio of 0.093 (G+D+P dominant), the v6.0 roadmap section placed 3 U-classified stories (BLG-BE-36, BLG-FEAT-46, BLG-FEAT-20) in the firm scope. This was a clean resolution requiring no re-negotiation at planning.

3. **STEP 1.4b reclassification applied correctly** — BLG-OPS-70 was listed as "firm" in the roadmap but its gate (~2026-06-23) falls within the expected sprint window. STEP 1.4b mandatory rule applied; reclassification to conditional was clean and documented.

4. **Dual gate cluster structure for EPIC-04** — Having two distinct gate clusters (Cluster A: 2026-06-21 for ST-06/ST-07; Cluster B: 2026-07-04 for ST-08–ST-11) was successfully encoded in the release plan and backlog slice. Sprint planning can activate clusters independently.

### Process Issues to Watch

1. **Documentation discrepancy: Skill-Silo ceiling** — The roadmap v6.0 Now section text states ">60% of total stories" as the Skill-Silo ceiling. However, roadmap_prompt.md v7.5 (authoritative engine) specifies 40%. The roadmap text is a stale reference from a pre-v7.4 authoring. Sprint planning and future rebalances must use 40% as the ceiling. The roadmap text should be corrected at next roadmap management pass.

2. **BLG-FE-64 perennial return (5 cycles)** — This item has returned to planning 5 consecutive cycles. STEP 1.4a triggered; PO disposition (a) — retain conditional — was recorded. However, this is a pattern risk: the gate (2026-06-21) is now genuinely imminent. Sprint planning **must** treat ST-06 as the highest-priority conditional: if the gate clears within the sprint window, schedule it immediately to avoid a 6th deferral and the 7th escalation cycle.

3. **Carry-forward miscommunication risk** — The v5.9 `lessons_learnt_closure.md` noted BLG-FE-64's gate "should have cleared by now" (written 2026-06-18, gate 2026-06-21). This could mislead sprint planning into treating it as already cleared. Corrected here: gate date 2026-06-21 was NOT cleared as of planning date 2026-06-19.

### Engine Notes

- **issues_mode = none** for this cycle — GitHub Issues sync not triggered at release planning; `sync gh` remains available if needed after sprint planning.
- **stage5_7 = not_applicable** — No escalations were raised; decision record integrity check therefore not required per schema.
- **capacity_check = warn** — Firm scope 6.5 days PASSES; total with all conditional ~10.85 days exceeds standard timebox. Standard mode allows WARN without blocking publication. Sprint planning must phase conditional items by gate cluster to stay within capacity.

## Carry-Forward Outstanding Actions for Sprint Planning

| # | Item | Priority | Owner |
|---|------|----------|-------|
| LL-P1-01 | Re-verify BLG-FE-64 gate (2026-06-21): if cleared, activate ST-06 as time-critical conditional in sprint | HIGH | Sprint Planning Engine |
| LL-P1-02 | Re-verify SI-03 ≥ 30-day gate for ST-07 (depends on ST-06) | HIGH | Sprint Planning Engine |
| LL-P1-03 | Confirm SI-05 digest delivery and deep link verification for ST-05 (BLG-OPS-70, gate ~2026-06-23) | MEDIUM | Sprint Planning Engine |
| LL-P1-04 | Verify SI-02 closed trade count ≥20: if met, PT-04 (BLG-FEAT-25) + SI-02 frontend eligible for conditional add | MEDIUM | Sprint Planning Engine |
| LL-P2-01 | Correct Skill-Silo ceiling text in roadmap v6.0 Now section (60% → 40%) at next roadmap management pass | LOW | Roadmap Management Engine |
| LL-P2-02 | Apply roadmap_prompt.md STEP 8.2 deferred patch (active-backlog verification) — filed as backlog item | LOW | Roadmap Management Engine |

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-06-19__release-v6.0",
  "release": "v6.0",
  "status": "Active",
  "carry_forward_count": 6,
  "high_priority_carry_forwards": ["LL-P1-01", "LL-P1-02"],
  "medium_priority_carry_forwards": ["LL-P1-03", "LL-P1-04"],
  "low_priority_carry_forwards": ["LL-P2-01", "LL-P2-02"],
  "authored_utc": "2026-06-19T00:00:00Z"
}
