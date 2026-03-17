**Owner:** Facilitator
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04

---

# Scored Initiatives — 2026-03-04__item-3.4

*Scores are decision support only. Proximity Score (SPS) is display-only; does not contribute to weighted total.*

**Scoring scale:** 1 (low/poor) → 5 (high/excellent). WF Intensity: 1=high effort, 5=hours only. Time to Value: 1=slow, 5=immediate.

---

## Existing Roadmap Initiatives

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 3.4 Risk Dashboard | 5 | 4 | 4 | 2 | 5 | 4 | 2 |
| 5.1 Trade Reflection | 4 | 3 | 3 | 3 | 4 | 5 | 2 |
| BLG-FEAT-08 Compliance Metrics | 4 | 3 | 2 | 4 | 4 | 5 | 2 |
| 5.2 Cohort Analysis | 4 | 3 | 2 | 3 | 4 | 5 | 2 |
| 5.3 Dashboard Homepage | 4 | 4 | 2 | 3 | 5 | 5 | 1 |
| 4.1b Tax-Year P&L | 4 | 5 | 3 | 3 | 3 | 4 | 1 |
| 4.1c Server-Side PDF | 3 | 2 | 3 | 3 | 3 | 4 | 1 |
| 4.3 Signal Exposure (PoG cleared) | 3 | 3 | 2 | 4 | 3 | 3 | 4 |
| 4.2 Watchlists (P2 — hold) | 3 | 3 | 2 | 2 | 3 | 4 | 2 |
| Chart Interactivity (P2 — hold) | 3 | 2 | 2 | 3 | 4 | 5 | 2 |

---

## New Items — Promoted to Backlog (STEP 5 Advance)

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Golden Output CI Baseline | 5 | 3 | 5 | 4 | 4 | 4 | 1 |
| Backtest Stop Reconciliation | 5 | 4 | 5 | 3 | 3 | 5 | 1 |
| Unavailability Failure Mode | 4 | 4 | 4 | 5 | 5 | 5 | 2 |
| AI Governance Policy | 3 | 2 | 3 | 4 | 4 | 5 | 1 |
| Dependency Vulnerability Scanning | 4 | 3 | 4 | 4 | 4 | 4 | 1 |
| Realised vs Unrealised P&L (into 4.1b) | 4 | 4 | 3 | 3 | 4 | 4 | 1 |
| Running API Changelog | 4 | 2 | 3 | 5 | 5 | 5 | 1 |
| OpenAPI Drift Detection CI | 4 | 2 | 3 | 4 | 5 | 5 | 1 |

---

## Facilitator Observations

Highest-value new items: Golden Output CI Baseline (closes silent regression gap), Backtest Stop Reconciliation (retrospective correctness), Unavailability Failure Mode (best effort-to-risk ratio — ~hours).

Lowest-value existing initiative: 4.1c Server-Side PDF Report — lowest combined Strat+Fin+Risk of all roadmap items; natural displacement candidate if a future Add requires stops.

SPS=4 note: 4.3 Signal Exposure PoG issued (POG-20260304-01). Implementation must not expand beyond top_n and lookback_days.

---

## Cycle 2026-03-17__item-v1.10 — Active Initiatives

**Last Updated:** 2026-03-17

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 3.5 Alerts & Notifications | 5 | 4 | 2 | 1 | 2 | 3 | 3 | L |
| 4.1b Tax-Year P&L | 4 | 5 | 3 | 3 | 3 | 4 | 1 | M |
| 4.3 Signal Exposure (PoG valid) | 3 | 3 | 2 | 5 | 4 | 4 | 4 | S |
| 4.2 Watchlists (P2 — hold) | 3 | 3 | 2 | 2 | 3 | 4 | 2 | M |
| Chart Interactivity (P2 — hold) | 3 | 2 | 2 | 3 | 4 | 5 | 2 | S |

**CPS:** 2.40 (5 items)

---

## New Items — Promoted to Backlog (STEP 5 Advance — cycle 2026-03-17__item-v1.10)

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BLG-OPS-02 Production Deployment Runbook | 3 | 2 | 5 | 5 | 5 | 5 | 1 | S |
| BLG-DATA-01 Positions Table Data Dictionary | 3 | 2 | 4 | 5 | 5 | 5 | 1 | S |
| BLG-TECH-07 Database Migration Governance Standard | 3 | 2 | 5 | 5 | 5 | 5 | 1 | S |

---

## Facilitator Observations (cycle 2026-03-17__item-v1.10)

All new backlog items from this cycle are S-effort governance/documentation items with high risk-reduction value and immediate time-to-value. The highest-value item is BLG-OPS-02 (Production Deployment Runbook) — directly enables the newly-live staging environment to be used safely in a governed deployment workflow.

Current displacement candidate: CHART-IX (Chart Interactivity) — SPS=2, S effort, lowest strategic urgency. No change required from prior scoring.

SPS=4 note: 4.3 Signal Exposure PoG POG-20260304-01 remains valid at strategy_rules.md v1.3. Scope constraint immutable: only `top_n` and `lookback_days` are cleared.
