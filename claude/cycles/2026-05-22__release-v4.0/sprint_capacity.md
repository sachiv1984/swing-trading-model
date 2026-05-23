**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-23
**Cycle:** 2026-05-22__release-v4.0

---

# Sprint Capacity — 2026-05-22__release-v4.0

## Capacity Inputs

```
Sprint duration:    2 sprints (~10 working days total; ~5 days each)
Available FTE:      1 (solo-dev, standard mode)
Total capacity:     ~10 days
Skill constraints:  None — all in-scope items are solo-implementable; no scarce role dependency
```

Source: `release_plan.md ## Capacity Check` (schema v2); `workforce_capacity.md`.

## Item Effort Mapping

### Sprint 1

| EPIC | ST | Title | Source | Effort | Effort (days) |
|------|----|-------|--------|--------|---------------|
| EPIC-01 | ST-01 | SI-01 pass/fail rate by rule — backend metric endpoint | BLG-FEAT-36 | M | ~2 |
| EPIC-01 | ST-02 | Red flag event frequency metric — backend + frontend | BLG-FEAT-37 | S | ~1 |
| EPIC-01 | ST-03 | E2E Playwright test — SI-01→SI-03 integration path | BLG-QA-25 | S | ~1 |
| EPIC-01 | ST-04 | Trade plan adherence rate metric — backend + frontend | BLG-FEAT-39 | S | ~1 |
| EPIC-02 | ST-05 | Validate ticker symbol on add | BLG-BE-15 | S | ~1 |
| EPIC-02 | ST-06 | Red flag endpoint auth and PII review | BLG-GOV-37 | XS | ~0.5 |
| EPIC-02 | ST-13 | Starlette security upgrade to ≥1.0.1 | CVE PYSEC-2026-161 | XS | ~0.5 |

**Sprint 1 total:** ~7 days

### Sprint 2

| EPIC | ST | Title | Source | Effort | Effort (days) |
|------|----|-------|--------|--------|---------------|
| EPIC-03 | ST-12 | Gemini Flash base wiring | BLG-BE-19 | S | ~1 |
| EPIC-03 | ST-07 | Gemini audit trail — log AI thesis generation calls | BLG-GOV-35 | M | ~2 |
| EPIC-03 | ST-08 | Gemini cost tracking — token usage and cost per call | BLG-OPS-26 | S | ~1 |
| EPIC-03 | ST-09 | CI/CD automated staging re-deploy on main merge | BLG-OPS-27 | M | ~2 |

**Sprint 2 total:** ~6 days

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Sprint 1 estimated effort | ~7 days |
| Sprint 2 estimated effort | ~6 days |
| Firm total | ~13 days |
| Available capacity | ~10 days |
| Over-allocation | Yes — ~3 days |
| Outcome | **WARN** — PO acknowledged (capacity_warn_acknowledged = true; standard mode) |

**PO acceptance (recorded):** Capacity WARN acknowledged. BLG-BE-19 effort was implicit in original EPIC-03 estimates; net genuinely new effort vs published plan is ~0.5 day (starlette XS). Sprint 1 is the heavier sprint at ~7 days; if Sprint 1 runs long, Sprint 2 EPIC-03 stories may need to slip to v4.1. PO accepts this risk.

## Conditional (Deferred) Items

| EPIC | ST | Title | Effort | Gate Condition |
|------|----|-------|--------|----------------|
| EPIC-04 | ST-10 | PT-04 Setup Quality Score — backend | L | 20+ closed trades (gate not met — <20 confirmed) |
| EPIC-04 | ST-11 | PT-04 Setup Quality Score — frontend | M | 20+ closed trades (gate not met — <20 confirmed) |

> **Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-05-22__release-v4.0 --reason "hard-blocker"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
