# Scored Initiatives

**Owner:** Facilitator
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-03-01

> ⚠️ Standing Notice: Scores are decision support only. They do not determine outcomes. Final decisions rest with the Product Owner within all governance constraints.

---

## Scoring Key

Each dimension scored 1–5 (5 = strongest).

| Dimension | Description |
|-----------|-------------|
| Strategic alignment | How directly does this serve strategy intent and product goals? |
| Financial impact | Revenue, cost reduction, or financial record value |
| Risk reduction | Reduces operational, quality, or strategic risk |
| Workforce intensity | 1 = very heavy, 5 = very light |
| Time to value | How quickly does value materialise post-delivery? |
| Reversibility | 1 = high lock-in, 5 = easily reversible |

---

## Cycle 2026-03-01__item-3.2 — Surviving Items

### BLG-TECH-04 — CI/CD Validation Workflow

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Strategic alignment | 4 | Delivery quality governance — enables safe releases |
| Financial impact | 2 | Indirect — prevents regressions rather than generating value directly |
| Risk reduction | 5 | Removes the only gap between manual and automated correctness enforcement |
| Workforce intensity | 4 | ~1 day effort |
| Time to value | 5 | Immediate from first PR |
| Reversibility | 4 | Workflow file; easily removed or modified |
| **Total** | **24** | |

---

### §13 Boundary Review (v1.7)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Strategic alignment | 5 | Required gate for three gated features; directly governs system identity |
| Financial impact | 1 | No direct financial impact — governance task |
| Risk reduction | 5 | Removes ambiguity blocking v2.0 planning |
| Workforce intensity | 5 | ~0.5 day workshop + doc update |
| Time to value | 4 | Value realised when gated features unblock |
| Reversibility | 5 | A documented decision — can be revised |
| **Total** | **25** | |

---

### Metrics Definitions — Portfolio Heat Formula (v1.7)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Strategic alignment | 5 | Hard gate for v1.8 Risk Dashboard |
| Financial impact | 1 | Definitional spec work — no direct impact |
| Risk reduction | 4 | Prevents scope ambiguity in Risk Dashboard implementation |
| Workforce intensity | 5 | ~0.5 day |
| Time to value | 4 | Value realised when Risk Dashboard enters pre-alignment |
| Reversibility | 5 | Spec update; can be revised |
| **Total** | **24** | |

---

### 3.4 Risk Dashboard (v1.8)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Strategic alignment | 5 | Risk management is core to the strategy intent (§2 — defend profits, enforce asymmetric risk) |
| Financial impact | 3 | Improves capital protection via better risk visibility |
| Risk reduction | 4 | Reduces user risk of missing dangerous portfolio heat levels |
| Workforce intensity | 2 | Medium effort (3–4 days with expanded scope) |
| Time to value | 3 | Pre-requisite chain (v1.7 items) must clear first |
| Reversibility | 3 | Page can be modified; heat formula once canonical is more stable |
| **Total** | **20** | |

---

### 3.5 Alerts & Notifications (v2.0) — Pre-conditions elevated to hard gates

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Strategic alignment | 4 | Directly supports human-in-the-loop model with timely signal delivery |
| Financial impact | 3 | Reduces risk of missed exits (stop-loss approach, regime change) |
| Risk reduction | 3 | Reduces operational risk of missed alerts — but only if async is reliable |
| Workforce intensity | 1 | Most complex feature to date — email/SMS/async/preferences (~4–5 days plus QA) |
| Time to value | 2 | Long pre-requisite chain; QA planning required |
| Reversibility | 2 | Notification infrastructure is relatively high lock-in once built |
| **Total** | **15** | Lowest scoring surviving item — reflects complexity and pre-req chain |

---

### 4.1b — Tax-Year P&L Statement (v2.0)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Strategic alignment | 3 | Supports financial record keeping — adjacent to core strategy |
| Financial impact | 5 | Direct tax compliance value; financial record requirement |
| Risk reduction | 3 | Reduces risk of tax reporting errors |
| Workforce intensity | 3 | Low–Medium (1–2 days) |
| Time to value | 3 | Seasonal (tax year end) |
| Reversibility | 3 | Report format; adjustable but financial records have compliance implications |
| **Total** | **20** | |

---

### v1.9 items (5.1, 5.2, 5.3, BLG-FEAT-08) — Grouped

| Item | Strategic alignment | Financial impact | Risk reduction | Workforce intensity | Time to value | Reversibility | Total |
|------|--------------------|-----------------|-----------|--------------------|--------------|--------------|-------|
| BLG-FEAT-08 Compliance Metrics | 4 | 1 | 3 | 4 | 3 | 5 | 20 |
| 5.1 Trade Reflection | 5 | 2 | 3 | 3 | 4 | 4 | 21 |
| 5.2 Cohort Analysis | 4 | 2 | 2 | 4 | 4 | 5 | 21 |
| 5.3 Dashboard Homepage | 5 | 2 | 2 | 3 | 5 | 4 | 21 |

---

## Score Summary (Descending)

| Initiative | Total |
|-----------|-------|
| §13 Boundary Review | 25 |
| BLG-TECH-04 CI/CD | 24 |
| Metrics Defs — Heat Formula | 24 |
| 5.1 Trade Reflection | 21 |
| 5.2 Cohort Analysis | 21 |
| 5.3 Dashboard Homepage | 21 |
| 3.4 Risk Dashboard | 20 |
| 4.1b Tax-Year P&L | 20 |
| BLG-FEAT-08 Compliance Metrics | 20 |
| 3.5 Alerts & Notifications | 15 |

Scores inform decisions but do not decide them. The lower score for 3.5 Alerts reflects genuine complexity and pre-requisite depth — consistent with the debate outcome (advance with hard gates, not immediate action).
