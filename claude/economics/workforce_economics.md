**Owner:** FinOps & Resource Architect
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04

---

# Workforce Economics — 2026-03-04__item-3.4

## Capacity Released (v1.7 Completion)

v1.7 Foundation & Governance sprint released capacity from 6 EPICs over ~3.5–4 days of effort. Primary skill demand was governance and spec authorship.

| Capacity released | Amount | Skills |
|------------------|--------|--------|
| FTE-weeks freed | Unknown (single-developer) | Governance-heavy: spec authoring, decision records, process design |
| Duration available | Immediate | All skills available for v1.8 |
| Constraints | None | No skill silo constraints |

Note: FTE values are Unknown for this single-developer project. Capacity conflicts are resolved by sequencing rather than allocation.

---

## Workforce Load by Initiative

### Existing Roadmap — v1.8 and Beyond

| Initiative | Est. Effort | Primary Skill | Classification |
|-----------|------------|---------------|---------------|
| 3.4 Risk Dashboard | 3–4 days | Engineering + QA | Execution-heavy |
| 5.1 Trade Reflection | 1–2 days | Engineering + spec | Execution-heavy |
| BLG-FEAT-08 Compliance Metrics | ~1 day | Spec + engineering | Mixed |
| 5.2 Cohort Analysis | 1–2 days | Engineering | Execution-heavy |
| 5.3 Dashboard Homepage | 1–2 days | Engineering | Execution-heavy |
| 4.1b Tax-Year P&L | 1–2 days | Spec + engineering | Mixed |
| 4.1c Server-Side PDF | 1–2 days | Engineering | Execution-heavy |
| 4.3 Signal Exposure | Low (FE + spec) | Frontend + spec | Mixed |
| 4.2 Watchlists (P2) | 3–4 days | Engineering | Execution-heavy |
| Chart Interactivity (P2) | 1–2 days | Frontend | Execution-heavy |

### New Backlog Items (Promoted from STEP 5)

| Item | Est. Effort | Primary Skill | Classification |
|------|------------|---------------|---------------|
| Golden Output CI Baseline | 1–3 days | Engineering + QA | Execution-heavy |
| Backtest Stop Reconciliation | 1–3 days | Engineering + QA | Execution-heavy |
| Unavailability Failure Mode | ~0.5 day | Governance | Governance-heavy |
| AI Governance Policy | ~0.5 day | Governance | Governance-heavy |
| Dependency Vulnerability Scanning | ~0.5 day | Engineering (CI) | Execution-heavy |
| Running API Changelog | ~0.5 day | Documentation | Governance-heavy |
| OpenAPI Drift Detection CI | ~0.5 day | Engineering (CI) | Execution-heavy |

---

## STEP 7.1 Skill-Silo Alert Check

### v1.8 Release (Risk Dashboard + accompanying items)

Planned v1.8 scope: Risk Dashboard (3–4 days, execution), plus high-priority backlog items.

Governance-heavy items in v1.8 candidate scope:
- Unavailability Failure Mode: ~0.5 day
- AI Governance Policy: ~0.5 day
- Running API Changelog: ~0.5 day

Total governance-heavy estimate: ~1.5 days
Total v1.8 scope estimate: ~6–8 days (Risk Dashboard + backlog items)

Governance load %: ~1.5 / ~7 = **~21%**

**Result: Within both bounds (20%–60%).**
- Ceiling (60%): Not exceeded. ✅
- Floor (20%): Met (just above floor). No sign-off capacity concern.
- Product Owner has confirmed adequate review and sign-off capacity.

**No Skill-Silo Alert required.**

---

## Opportunity Cost Assessment

**Does any initiative consume scarce skills that could deliver more value elsewhere?**

4.3 Signal Exposure Enhancement — frontend-only scope once PoG cleared and spec written. Not scarce. No opportunity cost concern.

4.1c Server-Side PDF Report — requires WeasyPrint or equivalent. Engineering skill; same pool as other execution items. Lowest-value item in portfolio; opportunity cost is moderate — same engineering time could advance Risk Dashboard or Golden Baseline. No forced reallocation at this stage; flag for v2.0 planning.

**No workforce constraint violations.** No forced Replace/Defer/Kill from workforce constraints alone.

---

## Capacity Freed vs Added (Net Assessment)

- Capacity freed by v1.7 completion: ~3.5–4 days governance/spec/engineering
- Capacity demand added (new backlog items): ~4–6 days (8 items at 0.5–1.5 days each)
- Net: Slight increase in backlog volume, but all new items are lower effort than v1.7

The backlog is larger, but no single item requires the governance overhead of v1.7. The new items are predominantly execution-heavy (CI, engineering) which is healthy given the prior cycle was governance-heavy.
