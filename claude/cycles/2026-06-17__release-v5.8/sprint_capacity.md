**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-17
**Cycle:** 2026-06-17__release-v5.8

---

# Sprint Capacity — v5.8

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | ~12–14 working days (solo developer, evenings/weekends) |
| Available FTE | 1 (solo developer) |
| Capacity baseline | ~12–14 days / sprint (revised 2026-05-27 per workforce_capacity.md) |
| Warn threshold | Effort > 14 days / sprint |
| Skill constraints | None — all v5.8 items are documentation, ops, and governance deliverables |
| Capacity check outcome | PASS (from release_plan.md ## Capacity Check) |

Source: `claude/roadmap/workforce_capacity.md` (effective 2026-05-27 revision) + `release_plan.md ## Capacity Check`.

---

## Sprint 1 — EPIC-01

| ST | Title | Effort Band | Effort Est. |
|----|-------|-------------|-------------|
| ST-01 | RFJ design review pre-brief | XS | ~0.5 day |
| ST-02 | Red Flag Journal visual design review | M | ~1–2 days |
| ST-03 | FRONTEND_URL production env var configuration | XS | ~0.25 day |
| ST-04 | Governance model complexity assessment | M | ~2 days |
| **Sprint 1 total** | | | **~3.75–4.75 days** |

**Sprint 1 capacity utilisation:** ~3.75–4.75 days vs 12–14 day capacity = **~30–35% utilised**. Well within bounds.

---

## Sprint 2 — EPIC-02 (Conditional)

| ST | Title | Effort Band | Effort Est. | Gate |
|----|-------|-------------|-------------|------|
| ST-05 | SI-05 digest weekly cadence review | S | ~0.5 day | 2026-07-04 |
| ST-06 | SI-05 digest actionability metric definition | S | ~0.5–1 day | 2026-07-04 |
| ST-07 | SI-05 service production p99 latency review | S | ~0.5 day | 2026-07-04 |
| **Sprint 2 total** | | | **~1.5–2 days** | |

**Sprint 2 capacity utilisation (if gate clears):** ~1.5–2 days vs 12–14 day capacity = **~12–15% utilised**.

---

## Total Estimated Effort

| Sprint | Effort |
|--------|--------|
| Sprint 1 | ~3.75–4.75 days |
| Sprint 2 (conditional) | ~1.5–2 days |
| **Total (if both sprints run)** | **~5.25–6.75 days** |

**Outcome: PASS** — total effort well within per-sprint capacity across both sprints.

---

## Conditional (Deferred)

| EPIC | ST | Effort | Gate Condition |
|------|-----|--------|----------------|
| EPIC-02 | ST-05 | S | 2026-07-04 gate: BLG-GOV-113 (SI-05 Phase 1 effectiveness review) must be complete |
| EPIC-02 | ST-06 | S | 2026-07-04 gate: BLG-GOV-113 must be complete |
| EPIC-02 | ST-07 | S | 2026-07-04 gate: ≥4 weeks POST /digest/si05/send production operation (≥2026-07-04) |

> **Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-17__release-v5.8 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
