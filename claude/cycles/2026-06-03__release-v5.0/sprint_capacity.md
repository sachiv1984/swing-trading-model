**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-03
**Cycle:** 2026-06-03__release-v5.0

---

# Sprint Capacity — 2026-06-03__release-v5.0

## Capacity Inputs

```
Sprint duration:     12–14 working days (double capacity sprint)
Available capacity:  ~40–48 hrs (double capacity — workforce_capacity.md baseline 2026-05-27)
Skill constraints:   None — all items within single-developer scope (governance, spec, backend, frontend)
Source:              release_plan.md §Capacity Check + workforce_capacity.md (effective 2026-05-27)
```

## Item Effort Mapping

| EPIC | Story | Effort Band | Hours (mid) | Sprint |
|------|-------|-------------|-------------|--------|
| EPIC-01 | ST-01 — Verify/append prompt_change_log.md entries | S | 2 | 1 |
| EPIC-01 | ST-02 — Fix 5 non-standard agent file headers | S | 2.5 | 1 |
| EPIC-01 | ST-03 — Add PO acceptance note to PR template | XS | 1 | 1 |
| | **EPIC-01 subtotal** | S+S+XS | **~7 hrs** | |
| EPIC-02 | ST-04 — execution_prompt.md governance file edit check | M | 5 | 1 |
| EPIC-02 | ST-05 — Post-ship audit advisory + last_audit_cycle_count | M | 6 | 1 |
| | **EPIC-02 subtotal** | M+M | **~12 hrs** | |
| EPIC-03 | ST-06 — allocation_insufficient status + inline explanation | S | 3 | 1 |
| EPIC-03 | ST-07 — Pre-entry regime gate fix: shared market status | S | 3 | 1 |
| EPIC-03 | ST-08 — Anthropic SDK staging verification | XS | 1 | 1 |
| | **EPIC-03 subtotal** | S+S+XS | **~7 hrs** | |
| EPIC-04 | ST-09 — SI-05 notification channel trade-off document | S | 3 | 1 |
| EPIC-04 | ST-10 — SI-05 Telegram message format specification | S | 3 | 1 |
| EPIC-04 | ST-11 — SI-02 re-entry trigger criteria definition | S | 3 | 1 |
| EPIC-04 | ST-12 — SI-04 formal binding conditions decisions document | S | 3 | 1 |
| EPIC-04 | ST-13 — SI-02 drift summary feasibility assessment | S | 3 | 1 |
| | **EPIC-04 firm subtotal** | 5×S | **~15 hrs** | |
| | **SPRINT 1 TOTAL (13 firm stories)** | | **~41 hrs** | |

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Confirmed capacity (double) | ~40–48 hrs |
| Estimated effort (Sprint 1 firm) | ~41 hrs |
| Utilisation | ~85–100% |
| Over-allocation | No |
| Outcome | **PASS** |

## Conditional (Deferred)

| EPIC | Story | Effort Band | Gate Condition |
|------|-------|-------------|----------------|
| EPIC-04 | ST-14 — SI-05 Phase 1 implementation (BLG-GOV-67) | M (~6 hrs) | SI-01 + SI-03 live ≥ 30 days; clears 2026-06-21 |

> **Gate re-invocation:** If the gate condition above is met during the sprint, do not add ST-14 informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-03__release-v5.0 --reason "BLG-GOV-67 gate met 2026-06-21"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
