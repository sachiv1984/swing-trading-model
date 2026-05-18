**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-18
**Cycle:** 2026-05-18__release-v3.7

---

# Sprint Capacity — v3.7

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | ~5 working days / sprint (standard solo-dev) |
| Available FTE | 1 |
| Total capacity (per sprint) | ~5 days |
| Skill constraints | Full-stack: Python backend, React frontend, governance spec authoring |
| Source | `release_plan.md ## Capacity Check`; `claude/roadmap/workforce_capacity.md` |

## Item Effort Mapping

| Story | EPIC | Size | Estimated Effort | Sprint |
|-------|------|------|-----------------|--------|
| ST-01 — Signals backend: watchlisted status support | EPIC-01 | M | ~1–2 days | 1 |
| ST-02 — Signals frontend: Add to Watchlist CTA | EPIC-01 | M | ~1–2 days | 1 |
| ST-03 — Trade plan form: signal context panel | EPIC-01 | M | ~1–2 days | 1 |
| ST-07 — execution_prompt.md patches ×3 | EPIC-03 | S | ~0.5 day | 1 |
| ST-08 — qa_evidence_template.md BLG-GOV-19 fail-path | EPIC-03 | S | ~0.5 day | 1 |
| ST-09 — Database stub conftest consolidation | EPIC-04 | S | ~0.5 day | 1 |
| ST-10 — Pycache git hygiene + Research page font staging | EPIC-04 | XS+XS | ~0.5 day | 1 |
| ST-11 — scored_initiatives.md comprehensive refresh | EPIC-04 | S | ~0.5–1 day | 1 |

**EPIC-02 deferred (ST-04, ST-05, ST-06) — gate not met.** Product Owner confirmed < 20 closed trades (2026-05-18). EPIC-02 defers to v3.8.

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total confirmed capacity (1 sprint) | ~5 days |
| Total estimated effort — Sprint 1 in-scope items | ~8.5 days |
| Utilisation | ~170% of single sprint |
| Over-allocation | Yes — acknowledged by Product Owner (2026-05-18) |

**Capacity WARN:** Total in-scope effort (~8.5 days) exceeds single sprint capacity (~5 days). Accepted phasing: EPIC-04 (1.5 days) → EPIC-03 (1 day) → EPIC-01 (6 days) within Sprint 1. Execution is sequential per merge order; total elapsed wall-clock time will exceed one sprint. Product Owner explicitly acknowledged over-capacity risk (2026-05-18).
