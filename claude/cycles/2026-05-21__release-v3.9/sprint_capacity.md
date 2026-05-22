Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-22
Cycle: 2026-05-21__release-v3.9

---

# Sprint Capacity — v3.9

---

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | 2 sprints (~5–6 working days each) |
| Available FTE | 1 (solo dev, standard pace) |
| Total capacity | ~11 days across both sprints |
| Capacity check outcome | WARN (standard mode) |
| Capacity WARN acknowledged | Yes — Product Owner, 2026-05-22 |
| Skill constraints | None — all stories within single-team scope |

---

## Item Effort Mapping

### Sprint 1

| EPIC | Story | Effort Band | Estimate |
|------|-------|-------------|---------|
| EPIC-01 | ST-01 Fix YF crumb/401 rate-limiting | M | ~1–2 days |
| EPIC-01 | ST-02 Fix sector/industry silently dropped | XS | <1h |
| EPIC-01 | ST-03 Remove invalid DAY ticker | XS | <1h |
| EPIC-01 | ST-04 Degraded-run warning banner | S | ~0.5 days |
| EPIC-02 | ST-05 Strip .L suffix from display labels | XS | <1h |
| EPIC-02 | ST-06 Add company_name column | S | ~0.5 days |

**Sprint 1 total estimate:** ~2.5–4 days
**Sprint 1 capacity:** ~5–6 days
**Sprint 1 result:** Within capacity ✅

### Sprint 2

| EPIC | Story | Effort Band | Estimate |
|------|-------|-------------|---------|
| EPIC-03 | ST-07 Red Flag Journal — data model and backend | M | ~1.5–2 days |
| EPIC-03 | ST-08 Red Flag Journal — frontend display | M | ~1.5 days |
| EPIC-04 | ST-09 execution_prompt.md patches | S | ~1h |
| EPIC-04 | ST-10 sprint_planning_prompt.md patch | S | ~1h |
| EPIC-04 | ST-11 BLG-GOV-25 dry-run support | M | ~1–2 days |
| EPIC-04 | ST-12 QA evidence pre-merge enforcement | S | ~1h |

**Sprint 2 total estimate:** ~4–6 days (firm)
**Sprint 2 capacity:** ~5–6 days
**Sprint 2 result:** Within capacity (firm scope) ✅

### Conditional (Deferred)

| EPIC | Story | Effort Band | Status |
|------|-------|-------------|--------|
| EPIC-05 | ST-13 PT-04 Setup Quality Score — backend | M | deferred_at_planning |
| EPIC-05 | ST-14 PT-04 Setup Quality Score — frontend | M | deferred_at_planning |

**Gate not met:** Product Owner confirmed < 20 closed trades (2026-05-22). ST-13/ST-14 recorded as `deferred_at_planning` with `gate_condition: "20+ closed trades not confirmed by PO (2026-05-22)"`.

---

## Total Effort vs Capacity

| Scope | Effort | Capacity | Status |
|-------|--------|----------|--------|
| Firm (EPIC-01–04) | ~7–10 days | ~11 days | ✅ Within capacity |
| With EPIC-05 | ~9–14 days | ~11 days | ⚠ WARN (deferred — not in scope) |

**Conclusion:** Firm scope is within available capacity. EPIC-05 exclusion resolves the WARN condition. Sprint proceeds on firm scope only.
