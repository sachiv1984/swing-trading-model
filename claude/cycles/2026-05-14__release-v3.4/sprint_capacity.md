**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-14
**Cycle:** 2026-05-14__release-v3.4

---

# Sprint Capacity — v3.4 Arc 3 In-Trade Risk Management (continued)

## Capacity Inputs

```
Sprint duration:    2 sprints (Sprint 1 + Sprint 2), standard solo-developer cycle
Available FTE:      1 (solo developer, evenings + weekends)
Total capacity:     ~10–13 working days (mid-point: ~11.5 days)
Skill constraints:  Frontend development required for 10 of 14 stories (all EPIC-01, EPIC-02, EPIC-03 items);
                    spec/documentation authorship for EPIC-04 autonomous items (no scarce skill conflict)
```

Source: `release_plan.md ## Capacity Check` and `workforce_capacity.md` (current entry: v3.4 rebalance 2026-05-13).

## Item Effort Mapping

| Story | EPIC | Sprint | Effort band | Est. days |
|-------|------|--------|-------------|-----------|
| ST-01 Position lifecycle state frontend (IT-01) | EPIC-01 | 2 | M | ~1.25 |
| ST-02 Grace Period Decision Support frontend (IT-02) | EPIC-01 | 2 | M | ~1.0 |
| ST-03 Stop Management Workflow frontend (IT-03) | EPIC-01 | 2 | M | ~1.0 |
| ST-04 Drawdown-Triggered Review Prompt backend (IT-04) | EPIC-02 | 2 | M | ~1.5 |
| ST-05 Drawdown-Triggered Review Prompt frontend (IT-04) | EPIC-02 | 2 | M | ~1.0 |
| ST-06 Position Concentration Limits backend + frontend (IT-05) | EPIC-02 | 2 | S | ~1.0 |
| ST-07 Research page UK suffix + negative earnings display | EPIC-03 | 1 | XS | ~0.5 |
| ST-08 Signals page default to most recent day | EPIC-03 | 1 | S | ~0.5 |
| ST-09 Watchlist research status indicator | EPIC-03 | 1 | XS | ~0.5 |
| ST-10 Trade plan status badges + abandonment UI | EPIC-03 | 1 | S | ~1.0 |
| ST-11 Research view component library | EPIC-04 | 1 | S | ~0.5 |
| ST-12 Screener morning routine UX spec | EPIC-04 | 1 | S | ~0.5 |
| ST-13 trade_plan.md §6.2 spec update + AI journal review cadence | EPIC-04 | 1 | XS | ~0.5 |
| ST-14 Screener accuracy test protocol | EPIC-04 | 1 | S | ~0.5 |
| **Total** | | | | **~11.25 days** |

## Sprint Phase Breakdown

| Phase | Sprint | EPICs | Stories | Est. days |
|-------|--------|-------|---------|-----------|
| Phase 1 | Sprint 1 | EPIC-03, EPIC-04 | ST-07–14 | ~4.0 |
| Phase 2 | Sprint 2 | EPIC-01, EPIC-02 | ST-01–06 | ~7.25 |

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~10–13 days (mid-point ~11.5) |
| Total estimated effort | ~11.25 days |
| Utilisation (mid-point) | ~98% |
| Over-allocation | No — within capacity band |
| Capacity verdict | **WARN** — at upper end; minimal buffer |

## Capacity WARN Acknowledgement

Capacity WARN acknowledged by Product Owner at release planning (2026-05-14). `capacity_warn_acknowledged = true` in `.claude_current_state.json`. Risk buffer: if Sprint 2 is over-capacity, EPIC-02 (IT-04/05) can slip to v3.5 — Arc 3 frontend (EPIC-01) and quick wins (EPIC-03) retain independent value.

## Skill Constraints

| Skill | Stories requiring it | Availability |
|-------|----------------------|--------------|
| Frontend development (React) | ST-01–03, ST-05–10 (10 stories) | Head of Engineering (solo developer) |
| Backend engineering (FastAPI) | ST-04, ST-06 (backend component) | Head of Engineering |
| Spec/documentation authorship | ST-11, ST-12, ST-13, ST-14 | Head of Specs Team |

No scarce skill conflicts — solo developer covers all execution roles.
