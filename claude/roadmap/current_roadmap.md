# Product Roadmap — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-03

> ⚠️ **Standing Notice:** This document records product intent and prioritisation thinking. All implementation detail (formulas, schemas, endpoint paths) is illustrative and indicative only. Before any feature moves to implementation, the relevant canonical specifications must be authored or updated by the appropriate domain owner. This document must not be cited as canonical intent.

---

## 1. Current Version

**v1.7** — Foundation & Governance — Shipped 2026-03-03
**Next planned release:** **v1.8**

---

## 2. Strategic Scope

### This system is
- A deterministic, human-in-the-loop decision support tool for momentum trading
- A risk-managed framework built around ATR-based trailing stops and regime detection
- A single-user portfolio tracker with journalling and analytics

### Strategic exclusions (canonical — see `docs/specs/strategy_rules.md §13`)

These are not deferred features. They are formally recorded as system boundaries in the Strategy Rules canonical spec and prevail over any planning document:

- **Not an automated trading bot.** All exits require manual confirmation.
- **Not a configurable strategy builder.** The strategy is a fixed, versioned behavioural contract.
- **Not an ML-based prediction system.** The system is explicitly deterministic.

### Product scope exclusions (deferred, not strategically excluded)

These may be revisited in future versions without any canonical spec change:

- Broker API integration
- Real-time streaming prices
- Social / community features
- Options and futures trading support

---

## 3. Delivery Plan

---

**3.1 Performance Analytics Page**
**Status:** ✅ Complete (shipped v1.5)
Delivered via a unified GET /analytics/metrics?period= endpoint. Includes a POST /validate/calculations endpoint for smoke-testing metric correctness against a known dataset.

**3.2 Position Sizing Calculator (Primary Feature)**
**Status:** ✅ Complete (shipped v1.6)
**Effort:** Low–Medium (2–3 days) (revised from 1–2 days — see scope note below)
**Value:** High (daily workflow improvement)
Always-visible widget inside the position entry form, directly above the shares field. User provides risk percentage (pre-populated from settings default) and stop price; system calculates suggested share count. Auto-fills the shares field when empty; shows a "use this" affordance when the user has already entered a value. Validates against available cash in real time via debounced calculation (300ms).

**Scope note (revised 2026-02-19):** Scope expanded during pre-alignment to include default_risk_percent field in the settings table, settings endpoint, and settings page UI. This is required to support widget pre-population and is in scope for v1.6 — not deferred. The original 1–2 day estimate did not account for the settings field, database migration, and additional spec updates across four documents. Revised estimate: 2–3 days. Full decision rationale: docs/product/decisions/3.2-position-sizing-calculator.md.

**Canonical specifications:** Sizing formula, validity rules, FX handling, and cash constraint behaviour are canonicalised in docs/specs/strategy_rules.md §4.1. Endpoint contract at docs/specs/api_contracts/portfolio_endpoints.md (POST /portfolio/size). Data model at docs/specs/data_model.md §6. Settings field at docs/specs/api_contracts/settings_endpoints.md.

**Shipped:** Director of Quality sign-off 2026-02-20. Verification report: docs/product/verification/3.2-position-sizing-calculator-verification.md (v1.4). Changelog: v1.6 entry. Scope and decisions documents superseded.

---

### v1.6.1 — Correctness & Quick Wins *(new)*

This release is inserted immediately after v1.6. It exists to resolve known correctness issues and ship a cluster of small, high-value backlog items before any new feature investment begins. No new feature work opens until this release is complete.

#### BLG-TECH-01 — Fix Sharpe Variance + Capital Efficiency *(promoted from backlog — P0)*
**Status:** ✅ Complete — 2026-02-21
**Closed:** Canonical Owner sign-off granted 2026-02-21. Validation confirmed 13/13 pass at 2026-02-21T00:24:41Z. `metrics_definitions.md` updated to v1.5.7 (Appendix E both items resolved). `analytics_endpoints.md` updated to v1.8.1. No regressions.

Fix `_calculate_sharpe()` to use sample variance (n−1) for portfolio and trade-level Sharpe. Fixed capital efficiency to use `total_cost (GBP)` from `trade_history` instead of `entry_price × shares`. `validation_data.py` expected values updated accordingly. v1.6 quality gate satisfied.

#### BLG-TECH-02 + BLG-TECH-03 — Validation Severity Model + Service Layer Consolidation (promoted from backlog — P1)
**Status:** ✅ Complete — 2026-02-21
**Closed:** Director of Quality sign-off 2026-02-21T21:30:00Z. 14/14 validation results pass with severity model. Phase Gate Documents filed.

Severity field added to every validation result (critical / high / medium / low) per analytics_endpoints.md v1.8.1
by_severity aggregation added to summary — all four tiers always present
All validation logic consolidated into services/validation_service.py per backend_engineering_patterns.md §3
Router thinned to HTTP in/out only — delegates entirely to ValidationService.validate_all()
Delivered co-delivered on single branch: fix/blg-tech-02-03-severity-service-consolidation
Phase Gate Documents: docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md, docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md
BLG-TECH-04 (CI/CD gate) dependency now unblocked ✅

#### Quick Wins Bundle *(promoted from backlog --- P2)*

**Status:** ✅ Complete --- 2026-03-01 **Estimated total effort:** ~8--10.5 hours (revised from ~6--8 hours to account for spec authoring --- A-S05, 2026-02-25) **Scope document:** `docs/product/scope/scope--QWB-quick-wins-bundle.md` **Decisions record:** `docs/product/decisions/QWB-quick-wins-bundle.md` **Phase Gate Document:** `docs/product/phase_gates/QWB_quick_wins_bundle_phase_gate.md` **Value:** Visible, tangible user-facing improvements. All decisions closed. All specs locked and QA-signed.

| Item | Effort | Status |
| --- | --- | --- |
| BLG-FEAT-01 --- Current Drawdown Widget | ~30 min | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-02 --- R-Multiple Column in Trade History | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-04 --- Best / Worst Trades Widget | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-05 --- Win Rate by Month Chart | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-06 --- Grace Period Indicator | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-07 --- CSV Export of Trade History | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |

**Locked canonical specs (implementation source of truth):**

| Spec | Version |
| --- | --- |
| `docs/specs/metrics_definitions.md` | v1.5.8 |
| `docs/specs/api_contracts/portfolio_endpoints.md` | v1.8.2 |
| `docs/specs/api_contracts/position_endpoints.md` | v1.8.3 |
| `docs/specs/api_contracts/trade_endpoints.md` | v1.8.4 |
| `docs/specs/api_contracts/analytics_endpoints.md` | v1.8.1 |
| `docs/specs/data_model.md` | v1.7 |
| `docs/specs/frontend/pages/dashboard.md` | v1.1 |
| `docs/specs/frontend/pages/trade_history.md` | v1.1 |
| `docs/specs/frontend/pages/analytics.md` | v1.2 |
| `docs/specs/frontend/pages/positions.md` | v1.2 |
| `docs/specs/api_dependencies.md` | v1.2 |
| `docs/reference/openapi.yaml` | current |

Verification: docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
Director of Quality sign-off: 2026-03-01 — Pass with logged deferrals (F-17, F-27)
Changelog: docs/product/changelog.md — v1.6.1 entry
Last Updated: 2026-03-01

---

### v1.7 — Foundation & Governance *(revised)*

**Status:** ✅ Complete — Shipped 2026-03-03
**Cycle:** 2026-03-02__release-v1.7
**Verification:** Verified — `claude/cycles/2026-03-02__release-v1.7/verification_report.md`
**Changelog:** `docs/product/changelog.md` — v1.7 entry

This release delivered the technical and governance foundations that de-risk everything that follows. It was non-user-facing but a hard dependency for several v1.8+ features.

#### BLG-TECH-04 — CI/CD GitHub Actions Validation Workflow
**Status:** ✅ Complete — 2026-03-03 (EPIC-01)
`.github/workflows/validate-analytics.yml` merged. Triggers on PR/push to main/develop. Blocks merge on `critical_failed > 0`. Posts severity breakdown as PR comment. PR #11 merged.

#### Strategy Rules §13 Boundary Review
**Status:** ✅ Complete — 2026-03-03 (EPIC-02)
Three features reviewed: Signal Params COMPLIANT, AI Journal CONDITIONALLY COMPLIANT, New Indicators COMPLIANT if canonical. §13-gated features cleared to proceed. Decision record: `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md`.

#### Metrics Definitions — Portfolio Heat Formula & Thresholds *(pre-work gate for v1.8)*
**Status:** ✅ Complete — 2026-03-03 (EPIC-03)
`metrics_definitions.md` v1.6.0: Position Risk (GBP-adjusted), Portfolio Heat formula, explicit display thresholds. v1.8 pre-alignment gate cleared.

#### Structured Logging / Observability Standards
**Status:** ✅ Complete — 2026-03-03 (EPIC-04)
`docs/specs/structured_logging_standards.md` v0.1.0 created (Class 1 Canonical Specification). Log levels, JSON format, correlation IDs, async observability. v2.0 pre-alignment gate (logging) cleared.

#### API Versioning Strategy Decision Record
**Status:** ✅ Complete — 2026-03-03 (EPIC-05)
`docs/product/decisions/api-versioning-v1.7.md` filed. URL path versioning deferred to first breaking change; 60-day deprecation; webhooks versioned from inception. v2.0 pre-alignment gate (API versioning) cleared.

#### Spec Debt Resolution (BLG-TECH-06, BLG-TECH-08, BLG-TECH-09)
**Status:** ✅ Complete — 2026-03-03 (EPIC-06)
`analytics_endpoints.md` v1.9.0 (14 metrics, OBS-01 resolved); `portfolio_endpoints.md` v1.9.0 (corrected to live API, OBS-QWB-R1-01 resolved); `trade_endpoints.md` v1.9.0 (`holding_days` added, OBS-QWB-R3-01 resolved).

---

### v1.8 — Risk Dashboard *(expanded from 3.4)*

#### 3.4 Risk Dashboard
**Status:** Planned
**Effort:** Medium (3–4 days with expanded scope)
**Value:** High (risk management — daily visibility)
**Pre-requisite:** Metrics Definitions (Portfolio Heat formula and thresholds) must be canonical before pre-alignment opens *(v1.7 gate)*

Previously scoped as a single Portfolio Heat Gauge widget. Scope expanded to a dedicated Risk Dashboard page that consolidates all risk-awareness features.

**Planned page contents:**
- Portfolio Heat Gauge — total capital at risk across open positions as a percentage of portfolio value
- Current Drawdown summary — from peak equity, days underwater *(if not already shipped in v1.6.1)*
- Grace Period status panel — positions currently in grace period with days remaining
- Position-level risk table — stop distance, ATR, position state (GRACE / LOSING / PROFITABLE) per open position
- Prospective heat indicator — integration with Position Sizing Calculator to show heat impact of a new position before entry

> **Before implementation:** The heat formula and display thresholds must be canonical in `docs/specs/metrics_definitions.md`. All other data is available from existing endpoints — `GET /portfolio`, `GET /positions`, `GET /analytics/metrics`. No new backend data dependencies beyond the heat calculation endpoint.

---

### v1.9 — User Value & Insight *(new)*

Three closely related user-facing features that build on existing data and the existing journal system. Delivered together as a cohesive release.

#### 5.1 Structured Trade Reflection Template *(new)*
**Status:** Planned
**Effort:** Low–Medium (1–2 days)
**Value:** High — daily discipline and learning reinforcement
**Pre-requisite:** BLG-FEAT-08 (Basic Compliance Metrics definitions must be canonical — they inform the reflection prompts)

A structured post-trade reflection form presented at trade close, built on top of the existing v1.4 notes and journal system. Pre-populated from the trade record: hold time, R-multiple, exit reason, position state history. Prompts the user with structured reflection questions (trade rationale, what worked, what didn't, discipline assessment). No AI — fully deterministic and testable.

> This is distinct from AI Journal Summarisation, which requires a §13 boundary decision before it can enter the roadmap. See Section 6 (Gated Features).

#### BLG-FEAT-08 — Basic Compliance Metrics *(promoted from backlog)*
**Status:** Planned — pre-work gate for 5.1
**Effort:** ~1 day
**Value:** Discipline visibility

Lightweight compliance metrics: journal completion rate, stop-based exit rate, average position size as a percentage of portfolio. Definitions must be canonicalised in `metrics_definitions.md` before implementation. These metrics also feed the reflection template prompts.

> ⚠️ **Capacity check required at v1.9 pre-alignment:** The Metrics Definitions & Analytics Owner was committed to EPIC-03 (v1.7). Before BLG-FEAT-08 enters pre-alignment, the FinOps & Resource Architect must confirm the Metrics Definitions owner is available and EPIC-03 deliverables are stable. Do not open v1.9 pre-alignment without this confirmation. *(LL-05, v1.7 Release Planning Lessons — 2026-03-02)*

#### 5.2 Cohort Analysis *(new — from roadmap review session)*
**Status:** Planned
**Effort:** Low–Medium (1–2 days)
**Value:** High — performance insight over time
**Pre-requisite:** Cohort metric definitions must be added to `metrics_definitions.md`

Group closed trade performance by entry period (month, quarter, year). Derivable entirely from existing trade data — no new data dependencies. Extends the Performance Analytics page with a cohort analysis tab or panel. Backend: new query or analytics endpoint extension. Frontend: new chart component.

#### 5.3 Dashboard Homepage / Session Summary *(new — from roadmap review session)*
**Status:** Planned
**Effort:** Low–Medium (1–2 days)
**Value:** High — makes the product feel complete for daily use

A proper home page for the product. On load: open positions count, total portfolio heat, any positions in grace period today, today's signal status, recent trade activity summary. All data sourced from existing endpoints — `GET /portfolio`, `GET /positions`, `GET /signals`. A composite endpoint may be introduced to reduce page-load request count; this is an engineering decision to be confirmed in pre-alignment.

---

### v2.0 — Reporting & Alerts *(consolidated)*

#### 3.5 Alerts & Notifications
**Status:** Planned
**Effort:** Medium–High (4–5 days)
**Value:** High

> ⛔ **Hard gates — v2.0 pre-alignment may not open until ALL THREE are confirmed:**
> 1. Structured logging / observability standards (v1.7) — **complete**
> 2. API versioning strategy decision record (v1.7) — **complete**
> 3. QA planning session for notification delivery — **complete**

Email alerts for: stop loss approach, grace period ending (days 8–9 warning), market regime change to risk-off, daily portfolio summary. Optional SMS. In-app notification feed. Configurable per-user preferences.

> **Before implementation:** Database schema must be defined in `docs/specs/data_model.md`. API endpoints must be specified in `docs/specs/api_contracts/`. Notification preference model must be specced before frontend work begins.

#### 4.1a — CSV Export of Trade History
**Status:** ❌ Killed — superseded by BLG-FEAT-07 (shipped v1.6.1, 2026-03-01)

BLG-FEAT-07 (CSV Export) was delivered as part of the QWB Quick Wins Bundle and shipped in v1.6.1. This planning item is closed. Decision log: 2026-03-01__item-3.2.

#### 4.1b — Tax-Year P&L Statement *(new sub-item)*
**Status:** Planned
**Effort:** Low–Medium (1–2 days)
**Value:** High (formal financial record for tax purposes)

A structured, server-side generated tax-year P&L statement. GBP-adjusted, fee-inclusive, covering all realised gains and losses in a given tax year. This is a financial record, not an analytics view — it requires its own canonical specification separate from the analytics endpoint. Dedicated report endpoint required.

#### 4.1c — Server-Side PDF Report *(new sub-item)*
**Status:** Planned
**Effort:** Low–Medium (1–2 days)
**Value:** Medium — replaces brittle browser-print approach

Replaces the current client-side browser-print PDF export on the analytics page. Server-side generation using a library (WeasyPrint or equivalent). Output: a consistently formatted, printable performance report. Covers executive summary, key insights, and advanced metrics. Removes dependency on browser print behaviour.

#### 4.3 — Signal Exposure Enhancement *(new — narrow scope)*
**Status:** Planned — gated
**Effort:** Low (frontend only once spec gate is cleared)
**Value:** Medium
**Pre-requisite:** `strategy_rules.md` update confirming `top_n` and `lookback_days` are formally user-configurable parameters. Decision record required before pre-alignment opens.

Expose the existing `top_n` and `lookback_days` signal generation parameters as user-facing controls on the signals page. The backend already supports these parameters — this is a frontend and spec task, not an engineering one. Must not be treated as a configurable strategy builder; scope is strictly limited to these two existing parameters.

> **Scope boundary:** Any screening parameter beyond `top_n` and `lookback_days` would constitute a configurable strategy builder, which is a §13 boundary violation. This item must not expand beyond the two named parameters without a formal strategy rules revision.

---

## 4. Priority 2 — Next Phase (post v2.0)

#### 4.2 Watchlists & Screening
**Status:** Planned — do not pull forward
**Effort:** Medium (3–4 days)
**Value:** Medium

Monitor tickers for entry signals. Target entry and stop fields. Quick-add to position entry modal. Requires new data model tables, new endpoints, and integration with signal status. Keep at this priority; do not accelerate ahead of v2.0 items.

#### Chart Interactivity Enhancements *(new — from roadmap review session)*
**Status:** Planned
**Effort:** Low–Medium (1–2 days)
**Value:** Medium — UX improvement on existing analytics

Add interactivity to existing analytics page charts: hover tooltips, zoom, drill-down. Applies to the underwater equity curve, monthly heatmap, and R-multiple distribution chart. No new indicators, no new data, no recalculation on the frontend. All values must remain consistent with the canonical backend response — no client-side re-derivation.

> **Scope boundary:** New technical indicators (RSI, MACD, Bollinger Bands, etc.) require a strategy rules review before they can be added. They are not in scope for this item.

---

## 5. Priority 3 — Deferred (v2.1 / v3.0)

| Feature | Effort | Rationale for deferral |
|---------|--------|------------------------|
| Position Correlation Analysis | High | Value confirmed; not urgent for single-user system |
| Backtesting Module | Very High | High value for validation; significant scope |
| Multi-Portfolio Support | High | Low value at current scale |
| Mobile App | Very High | Web experience sufficient |
| Full Compliance Scoring | High | Requires more trade history; lightweight version ships in v1.9 |
| BLG-TECH-05 — Prometheus metrics endpoint | Low–Medium | Defer until operational need or multi-user |
| Market Correlation Analysis | High | Blocked: requires external benchmark data pipeline (SPY, FTSE daily prices). Revisit when/if that pipeline is introduced |
| AI Journal Summarisation | Unknown | Blocked: requires §13 boundary decision (determinism principle). Not on active roadmap until that decision is documented |
| New Technical Indicators | Low–Medium | Blocked: requires strategy rules review. Not in scope without formal §13 confirmation |
| Customisable Dashboard Layout | High | High build cost, low current priority. Defer indefinitely at current scale |

---

## 6. Gated Features — Awaiting Pre-Conditions

These features have been discussed and provisionally agreed but may not enter pre-alignment until the stated pre-condition is met. They are not deferred — they are waiting on an explicit gate.

| Feature | Gate condition | Gate owner |
|---------|---------------|------------|
| Signal parameter exposure (4.3) | `strategy_rules.md` updated to formally define `top_n` and `lookback_days` as user-configurable | Strategy Rules owner + Product Owner |
| AI Journal Summarisation | §13 boundary decision documented: does non-deterministic AI output conflict with the deterministic system principle? | Product Owner + Strategy Rules owner |
| New Technical Indicators | Strategy rules review: which indicators, if any, are canonical to this strategy? | Strategy Rules owner |
| Market Correlation | External data pipeline decision: do we ingest benchmark prices (SPY, FTSE)? | Product Owner + Head of Engineering |

---

## 7. Decision Framework

When evaluating new features:

1. Does it help make better trading decisions?
2. Will it be used daily or weekly?
3. Can it be implemented in under a week?
4. Does it require external dependencies?
5. Does it conflict with system boundaries in `strategy_rules.md §13`? If yes, do not proceed without a canonical spec change.
6. Does it require pre-work (spec definitions, canonical updates, decision records) that isn't yet complete? If yes, add the pre-work as an explicit roadmap item before the feature.

---

## 8. Release Summary

| Release | Theme | Key deliveries |
|---------|-------|----------------|
| **v1.5** | Performance Analytics | Unified analytics endpoint, validation endpoint — ✅ Shipped |
| **v1.6** | Position Sizing | Calculator, settings default risk % — ✅ Shipped |
| **v1.6.1** | Correctness & Quick Wins | Quick Wins Bundle (6 features) — ✅ Shipped 2026-03-01" |
| **v1.7** | Foundation | CI/CD gate, §13 boundary review, metrics definitions, observability, API versioning decision — ✅ Shipped 2026-03-03 |
| **v1.8** | Risk Dashboard | Full risk page — heat, drawdown, grace period, position-level risk |
| **v1.9** | User Value & Insight | Trade reflection template, compliance metrics, cohort analysis, dashboard homepage |
| **v2.0** | Reporting & Alerts | Alerts & notifications (hard gates apply), tax-year statement, server-side PDF, signal parameter exposure (gated) |
| **v2.1+** | Enhancements | Watchlists, chart interactivity, Prometheus |

---

*For delivery history, see `docs/product/changelog.md`.*
*For backlog and quick wins, see `claude/backlog/backlog.md`.*
*For strategic constraints and system boundaries, see `docs/specs/strategy_rules.md`.*
