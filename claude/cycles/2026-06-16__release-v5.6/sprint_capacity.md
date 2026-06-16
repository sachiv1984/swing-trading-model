**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-16
**Cycle:** 2026-06-16__release-v5.6

---

# Sprint Capacity — v5.6

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | ~12–14 working days per sprint (revised baseline per workforce_capacity.md 2026-05-27) |
| Available FTE | 1 (solo developer, evenings/weekends) |
| Warn threshold | Effort > 14 days per sprint |
| Capacity baseline per sprint | ~12–14 days |
| Skill constraints | None identified — all items autonomous; single operator model |

Source: `claude/roadmap/workforce_capacity.md` (revised baseline 2026-05-27) and `release_plan.md ## Capacity Check`.

## Item Effort Mapping

### Sprint 1 — EPIC-03 + EPIC-01

| ST | EPIC | Item | Effort Band | Source |
|----|------|------|-------------|--------|
| ST-08 | EPIC-03 | BLG-GOV-106: PT-04 gate re-verification | S (~0.5 hour) | inline estimate |
| ST-09 | EPIC-03 | BLG-QA-45: Arc 5 QA completion criteria | S (~0.5–1 day) | inline estimate |
| ST-10 | EPIC-03 | BLG-QA-49: Arc 5 test scenario completeness | S-M (~0.5–1 day) | inline estimate |
| ST-11 | EPIC-03 | BLG-OPS-65: Anthropic API cost trend analysis | S (~0.5–1 day) | inline estimate |
| ST-01 | EPIC-01 | BLG-FE-73: SI-05 digest deep links | S (~0.5 day) | inline estimate |
| ST-02 | EPIC-01 | BLG-FE-74: N/A pass rate clarification | XS (<1 hour) | inline estimate |

**Sprint 1 total (firm):** ~2.5–4 days

### Sprint 2 — EPIC-02

| ST | EPIC | Item | Effort Band | Source |
|----|------|------|-------------|--------|
| ST-04 | EPIC-02 | BLG-OPS-62: Concentration-status latency | S (~0.5 day) | inline estimate |
| ST-05 | EPIC-02 | BLG-OPS-63: Red-flag-journal latency | S (~0.5 day) | inline estimate |
| ST-06 | EPIC-02 | BLG-OPS-64: Behavioural-drift latency | S (~0.5 day) | inline estimate |
| ST-07 | EPIC-02 | BLG-OPS-22: Research data caching layer | M (~2–3 days) | inline estimate |

**Sprint 2 total:** ~3.5–4.5 days

## Total Effort vs Capacity

| Sprint | Estimated effort | Capacity | Status |
|--------|-----------------|----------|--------|
| Sprint 1 (EPIC-01 + EPIC-03) | ~2.5–4 days firm | ~12–14 days | ✅ Within capacity |
| Sprint 2 (EPIC-02) | ~3.5–4.5 days | ~12–14 days | ✅ Within capacity |
| **Release total** | **~6–8.5 days firm** | ~24–28 days (2 sprints) | ✅ Within capacity |

**Capacity feasibility:** WARN (inherited from release plan — total effort approaches 2-sprint boundary at release level). Each individual sprint is well within capacity. Product Owner acknowledgement recorded in sprint_planning_notes.md.

## Conditional (Deferred)

| EPIC | Story | Effort Band | Gate Condition |
|------|-------|-------------|----------------|
| EPIC-01 | ST-03 (BLG-FE-64: RFJ design review pre-brief) | S (~0.5 day) | SI-03 Red Flag Journal live ≥30 days — gate clears 2026-06-21 (not yet cleared at planning 2026-06-16) |

> **Gate re-invocation:** If the gate condition above is met during the sprint, do not add ST-03 informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-16__release-v5.6 --reason "BLG-FE-64 gate cleared 2026-06-21"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
