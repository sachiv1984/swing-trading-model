**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-19
**Cycle:** 2026-06-19__release-v6.0

---

# Sprint Capacity — v6.0 Signal Correctness, User Intelligence & SI-05 Effectiveness

---

## Capacity Inputs

```
Sprint duration:    ~12–14 working days (solo developer; evenings/weekends)
Available FTE:      1 (solo developer)
Total capacity:     ~12–14 working days
Warn threshold:     effort > 14 days
Skill constraints:  None — solo developer covers all skill domains
```

Source: `claude/roadmap/workforce_capacity.md` (revised baseline 2026-05-27 — raised from ~8–10 days to ~12–14 days to reflect actual sustained pace).

---

## Item Effort Mapping

| Story | BLG-ID | EPIC | Effort Band | Mid-point | Classification | Delegation Class |
|-------|--------|------|-------------|-----------|----------------|-----------------|
| ST-01 | BLG-BE-36 | EPIC-01 | S | 0.5 day | Firm | autonomous |
| ST-02 | BLG-FEAT-46 | EPIC-02 | M | 2.5 days | Firm | autonomous |
| ST-03 | BLG-FEAT-20 | EPIC-02 | M | 2.5 days | Firm | autonomous |
| ST-04 | BLG-FEAT-47 | EPIC-03 | S | 1.0 day | Firm | autonomous |
| ST-05 | BLG-OPS-70 | EPIC-03 | XS | 0.1 day | Conditional (gate ~2026-06-23) | autonomous |
| ST-06 | BLG-FE-64 | EPIC-04 | S | 0.5 day | Conditional (gate 2026-06-21) | delegated_decision |
| ST-07 | BLG-FE-41 | EPIC-04 | M | 1.5 days | Conditional (gate 2026-06-21 + ST-06) | delegated_decision |
| ST-08 | BLG-GOV-112 | EPIC-04 | S | 0.5 day | Conditional (gate 2026-07-04) | delegated_decision |
| ST-09 | BLG-GOV-115 | EPIC-04 | S | 0.75 day | Conditional (gate 2026-07-04) | autonomous |
| ST-10 | BLG-GOV-130 | EPIC-04 | S | 0.5 day | Conditional (gate 2026-07-04) | delegated_decision |
| ST-11 | BLG-OPS-59 | EPIC-04 | S | 0.5 day | Conditional (gate 2026-07-04) | autonomous |

Effort estimates: Tier 3 (backlog estimates) for all except ST-11 (BLG-OPS-59, Tier 1 from scored_initiatives.md).

---

## Total Effort vs Capacity

```
Firm scope total:                 0.5 + 2.5 + 2.5 + 1.0 = 6.5 days   → PASS
Conditional scope total:          0.1 + 0.5 + 1.5 + 0.5 + 0.75 + 0.5 + 0.5 = 4.35 days
Total if all conditional activate: 10.85 days                          → WARN (approaches ceiling; remains feasible)
```

**Capacity outcome:** WARN (all-conditional scenario). Product Owner acknowledgement required before scope selection proceeds (IMP-41 — see Outstanding Actions).

---

## Phasing Recommendation

| Phase | Sprint Days | Stories | Effort | Rationale |
|-------|-------------|---------|--------|-----------|
| Phase 1 — Firm | Days 1–7 | ST-01, ST-02, ST-03, ST-04 | 6.5 days | Firm stories first; guarantees Product Value Alert commitment (3 U-stories) |
| Phase 2a — Cluster A | ~Day 8 (gate 2026-06-21) | ST-06, ST-07 | 2.0 days | Activates if SI-03 ≥ 30 days confirmed |
| Phase 2b — ST-05 | ~Day 9 (gate ~2026-06-23) | ST-05 | 0.1 day | Activates when SI-05 digest delivery confirmed |
| Phase 2c — Cluster B | ~Day 12–14 (gate 2026-07-04) | ST-08, ST-09, ST-10, ST-11 | 2.25 days | Activates after effectiveness review; may extend to final days |

---

## Conditional (Deferred) — Amendment Pathway

PT-04 (BLG-FEAT-25) and SI-02 frontend (BLG-FE-52/53) are NOT included in this sprint. They were explicitly deferred at release planning with gate: ≥20 closed trades (~13 as of 2026-06-16; trajectory ~2026-07-02). If the gate clears during the sprint, do not add these informally.

> **Gate re-invocation:** If PT-04 or SI-02 gate conditions are met during the sprint, invoke the amendment cycle (`amend cycle --cycle "2026-06-19__release-v6.0" --reason "PT-04 gate met: ≥20 closed trades"`) to add items to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.

---

## Skill-Silo Advisory

| Scenario | Composition | G+D+P % | Status |
|----------|-------------|---------|--------|
| Firm scope only (4 stories) | 3U + 1G | 25% G | ✅ Within 40% ceiling |
| + Cluster A (7 stories) | 3U + 1G + 1D + 2P | 57% G+D+P | ⚠️ Exceeds 40% ceiling |
| All scope (11 stories) | 3U + 4G + 2D + 2P | 73% G+D+P | ⚠️ Exceeds ceiling |

Advisory: EPIC-04 is governance/design-heavy. Conditional items may not all activate. Solo operator sequencing them as gates clear is the natural capacity management mechanism. If Cluster B fully activates, PO and PMO Lead should confirm the governance load is sustainable within the sprint close date.
