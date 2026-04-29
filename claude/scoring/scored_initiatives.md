**Owner:** Facilitator
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-31

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

---

## Cycle 2026-03-18__item-4.3 — Active Initiatives

**Last Updated:** 2026-03-18

*4.1b and 4.3 shipped in v2.0 and removed from active pool. Active initiatives: 3.5 Alerts, 4.2 Watchlists, CHART-IX.*

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 3.5 Alerts & Notifications | 5 | 4 | 2 | 1 | 2 | 3 | 3 | L |
| 4.2 Watchlists (P2 — hold) | 3 | 3 | 2 | 2 | 3 | 4 | 2 | M |
| CHART-IX (P2 — hold) | 3 | 2 | 2 | 3 | 4 | 5 | 2 | S |

**CPS:** 2.33 (3 items; prior: 2.40 — decrease reflects removal of SPS=4 item 4.3 and SPS=1 item 4.1b from active pool)

---

## New Items — Promoted to Backlog (STEP 5 Advance — cycle 2026-03-18__item-4.3)

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BLG-FR-01 Tax Year P&L PDF Export | 4 | 5 | 2 | 3 | 4 | 4 | 1 | S |
| BLG-FR-02 Tax Year P&L CSV Export | 4 | 5 | 2 | 4 | 5 | 5 | 1 | S |

---

## Facilitator Observations (cycle 2026-03-18__item-4.3)

Both new backlog items (BLG-FR-01/02) are S-effort financial reporting enhancements from v2.0 staging feedback. High financial value score (5) reflects statutory filing use case. Minimal risk (SPS=1 — no strategy boundary contact). CSV export (BLG-FR-02) is highest TTV (immediate — format conversion only).

Current displacement candidate: CHART-IX (Chart Interactivity) — SPS=2, S effort, lowest strategic urgency in active pool. No change from DL-009.

---

## Cycle 2026-03-21__item-3.5 — Active Initiatives (CPS Update)

**Last Updated:** 2026-03-21

*3.5 Alerts, 4.2 Watchlists, and CHART-IX all shipped in v2.1. Active initiatives pool is now empty.*

**CPS:** 0.0 (0 active initiatives; all v2.1 items shipped)
**Prior CPS:** 2.33 (cycle 2026-03-18__item-4.3)
**Delta:** −2.33 (all active roadmap initiatives completed; v2.2 scope TBD)

*No displacement candidate — no active initiatives to displace.*

---

## New Items — Promoted to Backlog (STEP 5 Advance — cycle 2026-03-21__item-3.5)

*Scoring scale: 1 (low/poor) → 5 (high/excellent). WF Intensity: 1=high effort, 5=hours only. TTV: 1=slow, 5=immediate.*

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BLG-SEC-01 API Key Authentication | 3 | 4 | 5 | 4 | 5 | 5 | 1 | M |
| BLG-FEAT-12 Alert History Table | 4 | 3 | 3 | 3 | 4 | 4 | 2 | M |
| BLG-FEAT-10 Alert Threshold Customisation | 4 | 3 | 2 | 3 | 4 | 4 | 2 | M |
| BLG-FEAT-11 Strategy Compliance Score | 4 | 3 | 4 | 2 | 3 | 4 | 4 | M–L |
| BLG-SPEC-T01 Spec-to-Test Traceability Matrix | 3 | 2 | 4 | 4 | 4 | 5 | 1 | M |
| BLG-FEAT-09 Metrics Staleness Indicator | 4 | 3 | 2 | 4 | 4 | 4 | 2 | S–M |
| BLG-QA-02 Test Automation Readiness Assessment | 3 | 2 | 3 | 5 | 5 | 5 | 1 | XS–S |
| BLG-FE-02 Loading State Standardisation | 3 | 2 | 2 | 3 | 4 | 4 | 1 | M |
| BLG-FE-03 User-Facing Error Message Mapping | 3 | 2 | 2 | 4 | 4 | 4 | 1 | S–M |
| BLG-OPS-05 API Performance Baseline | 3 | 2 | 3 | 4 | 5 | 5 | 1 | S |
| BLG-OPS-06 Health Check Endpoint | 3 | 2 | 3 | 5 | 5 | 5 | 1 | XS |
| BLG-SEC-02 Content Security Policy Headers | 2 | 2 | 4 | 5 | 5 | 5 | 1 | XS |

---

## Facilitator Observations (cycle 2026-03-21__item-3.5)

Highest-value items from this cycle: BLG-SEC-01 (API Key Auth — highest risk reduction, P1 priority), BLG-OPS-06 (Health Check — XS effort, immediate operational value), BLG-SEC-02 (CSP Headers — XS effort, direct security hardening). All three are sub-1-day items with high rev/TTV scores.

BLG-FEAT-11 (Strategy Compliance Score) carries SPS=4 due to §13.3 proximity. Scope is display-only — no automated enforcement. STEP 5 debate cleared after scope constraint was accepted. This constraint must be re-verified at pre-alignment before any implementation work begins.

Natural v2.2 sequencing: BLG-SEC-01 (P1) → BLG-QA-02 + BLG-SPEC-T01 (quality foundations) → BLG-FEAT-10/12 (alert enhancements, after BLG-OPS-04 alert scheduling design) → BLG-FEAT-09/11 (user-facing metrics). BLG-OPS-05/06 and BLG-SEC-02 are small-enough to slot into any sprint as fast-follow items.

---

## New Items — Promoted to Backlog (STEP 5 Advance — cycle 2026-03-24__scheduled)

**Last Updated:** 2026-03-24

*Active initiatives pool remains empty post-v2.2 ship. CPS = 0.0 (0 active initiatives). No active initiative scoring required this cycle.*

*Scoring scale: 1 (low/poor) → 5 (high/excellent). WF Intensity: 1=high effort, 5=hours only. TTV: 1=slow, 5=immediate.*

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BLG-OPS-07 System Health Check Playbook | 2 | 2 | 3 | 5 | 5 | 5 | 1 | S |
| BLG-QA-03 Canonical Test Execution Report Template | 2 | 2 | 3 | 5 | 5 | 5 | 1 | S |
| BLG-QA-04 Integration Test Coverage Report | 3 | 2 | 4 | 4 | 4 | 5 | 1 | M |
| BLG-QA-05 Critical-path Smoke Test (Playwright) | 4 | 2 | 4 | 3 | 4 | 4 | 1 | M |
| BLG-OPS-08 Staging Data Reset Script | 3 | 2 | 4 | 5 | 5 | 5 | 1 | S |
| BLG-OPS-09 Database Size Monitoring Alert | 3 | 3 | 5 | 5 | 5 | 5 | 1 | S |
| BLG-FE-05 Alert Notification Badge | 3 | 3 | 2 | 5 | 4 | 5 | 2 | S |
| BLG-QA-06 Test Data Seed Script Library | 3 | 2 | 4 | 4 | 4 | 5 | 1 | S–M |

---

## Facilitator Observations (cycle 2026-03-24__scheduled)

Highest-value items: BLG-OPS-09 (data safety, risk=5 — active data-loss risk on Render free tier), BLG-QA-05 (critical-path quality safety net, strat=4 — follows BLG-QA-01 Playwright investment), BLG-QA-04 (coverage visibility — makes DoQ sign-off better-informed).

All 8 items are SPS=1 or SPS=2 — no §13 boundary proximity. All are S or M effort — quick wins at v2.3. All items high reversibility (rev=5). BLG-QA-05 has an explicit §3 scope constraint: Playwright pass is supporting evidence for non-visual AC only — not a DoQ gate replacement. BLG-OPS-08 (staging reset) should be sequenced before BLG-QA-05 and BLG-QA-04 as a prerequisite.

**CPS this cycle:** 0.0 (zero active initiatives). Prior CPS: 0.0 (cycle 2026-03-21__item-3.5). Delta: 0.0.

---

## Cycle 2026-03-31__scheduled — New Backlog Items

*Standard-tier run. Zero active roadmap initiatives. 4 new backlog items scored as STEP 6 output.*

| Initiative | Strat | Fin | Risk | WF Int | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BLG-FEAT-14 — Weekly trading review digest | 4 | 3 | 2 | 3 | 3 | 4 | 2 | M |
| BLG-OPS-10 — Render hosting tier review | 3 | 4 | 4 | 5 | 5 | 5 | 1 | XS |
| BLG-BE-06 — Alert evaluation idempotency | 4 | 2 | 5 | 3 | 3 | 3 | 2 | M |
| BLG-GOV-09 — Cycle velocity metric | 3 | 2 | 3 | 4 | 4 | 5 | 1 | S |

*Scores: Strat=Strategic alignment, Fin=Financial impact, Risk=Risk reduction, WF Int=Workforce intensity (5=minimal), TTV=Time to value (5=fast), Rev=Reversibility (5=fully reversible), SPS=Strategy Proximity Score (carried from STEP 5 debate). Scale: 1–5.*

---

## Cycle 2026-04-05__scheduled — New Backlog Items

*Standard-tier run. Zero active roadmap initiatives. 3 new backlog items from stale ideas advancing after v2.4 gate clearance. CPS = 0.0 (unchanged).*

| Initiative | Strat | Fin | Risk | WF Int | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BLG-FE-09 — Define Frontend Performance Budget | 2 | 1 | 2 | 5 | 4 | 5 | 1 | S |
| BLG-SPEC-D17 — Spec Dependency Map | 3 | 1 | 3 | 4 | 3 | 5 | 1 | M |
| BLG-GOV-14 — Governance Health Score | 3 | 1 | 3 | 4 | 3 | 5 | 1 | M |

*Scores: Strat=Strategic alignment, Fin=Financial impact, Risk=Risk reduction, WF Int=Workforce intensity (5=minimal), TTV=Time to value (5=fast), Rev=Reversibility (5=fully reversible), SPS=Strategy Proximity Score (carried from STEP 5 debate). Scale: 1–5.*

**CPS this cycle:** 0.0 (zero active initiatives). Prior CPS: 0.0 (cycle 2026-03-31__scheduled). Delta: 0.0.

**Facilitator observations (cycle 2026-04-05__scheduled):** All 3 items are P3 / S–M effort governance or spec-debt items with low financial impact (Fin=1) but meaningful risk-reduction potential (Risk=2–3). High reversibility (Rev=5) across the board. BLG-FE-09 scope constraint: documentation and budget definition only — no implementation work included. BLG-SPEC-D17 scope constraint: initial map covers priority specs only (API contracts, data model, strategy rules) — full coverage is a stretch goal. Skill-Silo Alert fired this cycle (100% governance-heavy additions). Pull-forward candidate BLG-OPS-12 confirmed already in backlog at P2 — no action required.

**Last Updated:** 2026-04-05

---

## Cycle 2026-04-24__scheduled — New Backlog Items

*Standard-tier run. Zero active roadmap initiatives. 2 new backlog items from gate-cleared ideas after v2.9 ship. CPS = 0.0 (unchanged).*

| Initiative | Strat | Fin | Risk | WF Int | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BLG-FE-19 — Keyboard Shortcuts | 3 | 2 | 1 | 5 | 5 | 5 | 2 | S |
| BLG-OPS-14 — AI Journal Monitoring Metrics | 4 | 2 | 4 | 5 | 5 | 5 | 2 | S |

*Scores: Strat=Strategic alignment, Fin=Financial impact, Risk=Risk reduction, WF Int=Workforce intensity (5=minimal), TTV=Time to value (5=fast), Rev=Reversibility (5=fully reversible), SPS=Strategy Proximity Score (carried from STEP 5 debate). Scale: 1–5.*

**CPS this cycle:** 0.0 (zero active initiatives). Prior CPS: 0.0 (cycle 2026-04-21__scheduled). Delta: 0.0.

**Facilitator observations (cycle 2026-04-24__scheduled):** Both items are P3 / S-effort with immediate time-to-value (TTV=5) and full reversibility (Rev=5). BLG-OPS-14 has the stronger risk-reduction case (Risk=4) — AI monitoring fills a live operational gap post-BLG-AI-01 delivery. BLG-FE-19 is low-risk UX polish (Risk=1) with a 10-cycle overdue gate; reasonable to include. No Skill-Silo Alert (Governance load = 0%). No scarce skill conflicts.

**Last Updated:** 2026-04-28 (cycle 2026-04-28__scheduled — 5 post-Arc 1 operational/QA items)

---

## Cycle 2026-04-28__scheduled — New Backlog Items

*Standard-tier run. Zero active roadmap initiatives. 5 new backlog items from Arc 1 gate-clearance batch (v3.0 shipped 2026-04-27). CPS = 0.0 (unchanged).*

| Initiative | Strat | Fin | Risk | WF Int | TTV | Rev | SPS | Effort |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BLG-SEC-03 — Alpaca API key rotation policy | 3 | 2 | 5 | 5 | 5 | 5 | 1 | S |
| BLG-SEC-04 — External API credential audit | 3 | 2 | 4 | 5 | 5 | 5 | 1 | XS |
| BLG-GOV-17 — External API dependency risk register | 3 | 2 | 4 | 5 | 5 | 5 | 1 | XS |
| BLG-QA-10 — Screener scenario library | 4 | 3 | 4 | 3 | 3 | 5 | 1 | M |
| BLG-QA-11 — Screener accuracy test protocol | 4 | 3 | 4 | 4 | 4 | 5 | 1 | S |

*Scores: Strat=Strategic alignment, Fin=Financial impact, Risk=Risk reduction, WF Int=Workforce intensity (5=minimal), TTV=Time to value (5=fast), Rev=Reversibility (5=fully reversible), SPS=Strategy Proximity Score (carried from STEP 5 debate). Scale: 1–5.*

**CPS this cycle:** 0.0 (zero active initiatives). Prior CPS: 0.0 (cycle 2026-04-24__scheduled). Delta: 0.0.

**Facilitator observations (cycle 2026-04-28__scheduled):** All 5 items are SPS=1 with no §13 boundary proximity and full reversibility (Rev=5). Security items (BLG-SEC-03/04) have the highest risk-reduction scores (Risk=5/4) for their effort class (S/XS). BLG-SEC-03 Alpaca key rotation policy is the strongest risk-per-effort item — sub-day effort, Risk=5. BLG-QA-10/11 are the highest-priority (P2) items and directly address screener quality assurance for the newly-live Arc 1 engine. BLG-GOV-17 (XS) closes the external API dependency gap surfaced by the v3.0 hotfix cycle. No Skill-Silo Alert this cycle (governance load = 60%, at ceiling, no alert threshold breached per cycle_record). Natural v3.1 sequencing: BLG-SEC-03/04 + BLG-GOV-17 (credential and dependency hygiene) → BLG-QA-11 (screener protocol) → BLG-QA-10 (scenario library, requires 2–4 weeks screener operational history).


