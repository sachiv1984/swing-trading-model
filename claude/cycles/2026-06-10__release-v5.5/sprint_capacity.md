**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-10
**Cycle:** 2026-06-10__release-v5.5

---

# Sprint Capacity — v5.5

## Capacity Inputs

```
Sprint duration:    Standard sprint cadence (evenings/weekends)
Available FTE:      1 (solo developer)
Per-sprint capacity: ~12–14 working days (revised baseline; workforce_capacity.md 2026-05-27)
Warn threshold:     Effort > 14 days per sprint
Skill constraints:  None — all skills held by sole operator
```

> **Capacity WARN advisory (IMP-41):** The `stage4_5_capacity_check` outcome in state.json is `warn`. This WARN originated from the old 5–7 day baseline; Sprint 1 (~6 days estimated) is well within the revised 12–14 day baseline. Product Owner has acknowledged the WARN by issuing `plan sprint`. `capacity_warn_acknowledged = true` is set in global state.

---

## Sprint 1 — Item Effort Mapping

| EPIC | ST | Title | Effort Band | Est. (days) | Delegation class |
|------|----|-------|-------------|-------------|-----------------|
| EPIC-01 | ST-01 | sprint_planning_prompt.md within-sprint date gate advisory | S | ~0.5 | autonomous |
| EPIC-01 | ST-02 | execution_prompt.md pr_status read-after-open improvement | S | ~0.5 | autonomous |
| EPIC-01 | ST-03 | qa_evidence commit discipline advisory in execution_prompt.md | S | ~0.5 | autonomous |
| EPIC-02 | ST-04 | Trade count gate-monitoring view (backend) | S | ~0.5 | autonomous |
| EPIC-02 | ST-05 | Trade data density progress tracker (frontend display) | S | ~0.5 | autonomous |
| EPIC-03 | ST-06 | v2.8–v4.6 endpoint performance baseline re-run (24 endpoints) | M | ~2.0 | delegated_backend |
| EPIC-03 | ST-07 | v5.1–v5.4 endpoint baseline extension | S | ~0.75 | delegated_backend |
| EPIC-03 | ST-08 | POST /digest/si05/send to api_performance_baseline.md | XS | ~0.25 | delegated_backend |
| EPIC-03 | ST-09 | Formal regression test suite baseline document | S | ~0.5 | autonomous |
| EPIC-03 | ST-10 | User journey map: SI-05 Telegram digest to app action | S | ~0.5 | delegated_qa |

**Sprint 1 total estimate: ~6.5 days — PASS (within 12–14 day capacity)**

> ST-08 note: ST-07 (OPS-61) scope explicitly includes v5.1–v5.4 endpoints. If POST /digest/si05/send is included in ST-07, ST-08 is trivially complete. Sprint execution to confirm at start of ST-07.

---

## Sprint 2 — Item Effort Mapping

| EPIC | ST | Title | Effort Band | Est. (days) | Delegation class | Gate |
|------|----|-------|-------------|-------------|-----------------|------|
| EPIC-04 | ST-11 | Red Flag Journal visual design review pre-brief | S | ~0.5 | delegated_decision | 2026-06-21 |
| EPIC-04 | ST-12 | SI-05 p99 production latency baseline review | S | ~0.5 | delegated_backend | 2026-07-04 |
| EPIC-04 | ST-13 | SI-05 digest weekly cadence review | S | ~0.5 | delegated_decision | 2026-07-04 |
| EPIC-04 | ST-14 | SI-05 digest actionability metric definition | S | ~0.75 | delegated_decision | 2026-07-04 |

**Sprint 2 total estimate: ~2.25 days — PASS (well within capacity)**

---

## Capacity Gate

- Sprint 1: ~6.5 days estimated vs ~12–14 days available → **PASS**
- Sprint 2: ~2.25 days estimated vs ~12–14 days available → **PASS**
- No over-allocation. No items deferred for capacity reasons.

---

## Conditional (Deferred at Planning)

No items are deferred at planning. All 14 firm stories enter the sprint backlog. Sprint 2 stories are conditionally gated by date (not planning deferral) and are marked `Status at sprint open: conditional — gate <date>` in the sprint backlog.

> **Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-10__release-v5.5 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
