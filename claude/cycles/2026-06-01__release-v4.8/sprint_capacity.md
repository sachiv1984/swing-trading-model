**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-01
**Cycle:** 2026-06-01__release-v4.8

---

# Sprint Capacity — v4.8

---

## Capacity Inputs

Derived from `claude/roadmap/workforce_capacity.md` and `release_plan.md ## Capacity Check`.

```
Sprint duration:    ~12–14 working days (standard capacity baseline; revised 2026-05-27)
Available FTE:      1 (solo developer, evenings/weekends)
Total capacity:     ~12–14 dev-days
Skill constraints:  None — v4.8 is entirely documentation/governance/ops work; no scarce engineering skill required
```

---

## Item Effort Mapping

| EPIC | ST Item | Title | Effort Band | Firm/Conditional |
|------|---------|-------|-------------|-----------------|
| EPIC-01 | ST-01 | §13 register completion | S (~0.5–1d) | Firm |
| EPIC-01 | ST-02 | Agent charter header compliance | S (~0.5d) | Firm |
| EPIC-01 | ST-03 | AUD gap resolution verification | S (~0.5d) | Firm |
| EPIC-02 | ST-04 | Build minutes monitoring policy | S (~0.5d) | Firm |
| EPIC-02 | ST-05 | Dependency audit post-v4.7 | S (~0.5–1d) | Firm |
| EPIC-02 | ST-06 | Coverage matrix + v4.7 contract | S (~0.5–1d) | Firm |
| EPIC-02 | ST-07 | SI-04 strategy version comparison endpoint contract | S–M (~1–2d) | Conditional (PO confirmation pending) |

**Effort subtotals:**
- EPIC-01 (firm): ~1.5 dev-days
- EPIC-02 (firm, ST-04–ST-06): ~1.5–2.5 dev-days
- EPIC-02 (conditional, ST-07): ~1–2 dev-days

---

## Total Effort vs Capacity

| Scope | Estimated effort | Available capacity | Utilisation | Verdict |
|-------|-----------------|-------------------|-------------|---------|
| Firm only (6 stories) | ~3–4 dev-days | ~12–14 dev-days | ~25–30% | ✅ PASS |
| Firm + conditional (7 stories) | ~4–6 dev-days | ~12–14 dev-days | ~30–45% | ✅ PASS |

Well within standard capacity. No phasing required.

---

## Conditional (Deferred) Items

| EPIC | ST Item | Title | Effort Band | Gate Condition |
|------|---------|-------|-------------|----------------|
| EPIC-03 | ST-08 | SI-05 Phase 1 implementation | M (~2–3d) | SI-01 + SI-03 live ≥ 30 days — clears 2026-06-21; gate NOT MET at sprint planning (today 2026-06-01) |

> **Gate re-invocation:** If the gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-01__release-v4.8 --reason "SI-05 gate met (2026-06-21)"`) to add ST-08 to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
