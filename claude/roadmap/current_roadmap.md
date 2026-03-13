# Product Roadmap — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-13 (post-ship closure — v1.9 Sprint 2 fully shipped)
**Last rebalance:** 2026-03-06 (cycle 2026-03-06__item-3.4 — v1.8 completion event)

> ⚠️ **Standing Notice:** This document records product intent and prioritisation thinking. All implementation detail (formulas, schemas, endpoint paths) is illustrative and indicative only. Before any feature moves to implementation, the relevant canonical specifications must be authored or updated by the appropriate domain owner. This document must not be cited as canonical intent.

---

## 1. Current Version

**v1.9** — User Value & Insight — Fully Shipped (Sprint 1: 2026-03-09 | Sprint 2: 2026-03-13)
**Next planned release:** **v2.0**

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

> ⚠️ **Product Owner Action Required:** No verification report path or decision log entry exists for this item (predates governance). Please provide a verification reference or decision log entry before the next `manage roadmap` run so this item can be retired to the archive.

---

### v1.9 — User Value & Insight *(✅ Fully Shipped — Sprint 1: 2026-03-09 | Sprint 2: 2026-03-13)*

Three closely related user-facing features that build on existing data and the existing journal system. Delivered together as a cohesive release.

> **v1.9 Sprint 1 shipped (2026-03-09):** Risk Dashboard deviations (EPIC-04), Playwright test infrastructure + Service Layer Test Coverage Standard (EPIC-05 partial), and full documentation hygiene backlog (EPIC-06) — 13 ST items complete. Cycle: `2026-03-06__release-v1.9`.

> **v1.9 Sprint 2 shipped (2026-03-13):** User-facing features — structured trade reflection template (EPIC-01), basic compliance metrics (EPIC-01), cohort analysis (EPIC-02), R-multiple distribution report (EPIC-02), dashboard homepage (EPIC-03), canonical test scenarios Phase 2 (EPIC-05) — 6 ST items complete. Verified_with_deviations (2 deviations accepted, both P2/P3, targeting v1.10). Cycle: `2026-03-06__release-v1.9`.

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
> 3. QA planning session for notification delivery — **pending** *(uncleared as of 2026-03-04)*

> 🔄 **Auto-advance trigger (DL-003, 2026-03-04):** Once the QA planning session for notification delivery is completed and documented, 3.5 Alerts auto-advances to active v2.0 planning without requiring a new rebalance cycle. The session output must specify: test types required, notification delivery modes to be tested, expected test infrastructure.

Email alerts for: stop loss approach, grace period ending (days 8–9 warning), market regime change to risk-off, daily portfolio summary. Optional SMS. In-app notification feed. Configurable per-user preferences.

> **Before implementation:** Database schema must be defined in `docs/specs/data_model.md`. API endpoints must be specified in `docs/specs/api_contracts/`. Notification preference model must be specced before frontend work begins.

#### 4.1b — Tax-Year P&L Statement *(new sub-item)*
**Status:** Planned
**Effort:** Low–Medium (1–2 days)
**Value:** High (formal financial record for tax purposes)

A structured, server-side generated tax-year P&L statement. GBP-adjusted, fee-inclusive, covering all realised gains and losses in a given tax year. This is a financial record, not an analytics view — it requires its own canonical specification separate from the analytics endpoint. Dedicated report endpoint required.

> **Scope note (2026-03-04):** Realised vs Unrealised P&L display labelling (originally submitted as BLG-NEW-06) is pre-work for this item. The P&L statement must clearly distinguish realised and unrealised amounts per trade. BLG-NEW-06 is merged into 4.1b pre-work scope — not a standalone backlog item.

#### 4.1c — Server-Side PDF Report *(new sub-item)*
**Status:** Planned
**Effort:** Low–Medium (1–2 days)
**Value:** Medium — replaces brittle browser-print approach

Replaces the current client-side browser-print PDF export on the analytics page. Server-side generation using a library (WeasyPrint or equivalent). Output: a consistently formatted, printable performance report. Covers executive summary, key insights, and advanced metrics. Removes dependency on browser print behaviour.

#### 4.3 — Signal Exposure Enhancement *(new — narrow scope)*
**Status:** Planned — active v2.0 planning *(§13 gate cleared; PoG POG-20260304-01 issued 2026-03-04)*
**Effort:** Low (frontend only — backend already supports these parameters)
**Value:** Medium

Expose the existing `top_n` and `lookback_days` signal generation parameters as user-facing controls on the signals page. The backend already supports these parameters — this is a frontend and spec task, not an engineering one.

> **Gate clearance (DL-004, 2026-03-04):** The v1.7 SRB (EPIC-02) confirmed that `top_n` and `lookback_days` are display/query-scope controls, not strategy execution parameters, and their exposure does not violate §13.2. PoG: `claude/evidence/gates/signal-exposure-4.3_20260304.md` (POG-20260304-01). Referenced document: `strategy_rules.md` v1.3.

> **Scope constraint (immutable):** Only `top_n` and `lookback_days` are cleared by this PoG. Any parameter beyond these two — including signal weights, scoring logic, or ranking methodology — requires a new §13 review before it may enter pre-alignment. This PoG is automatically stale if `strategy_rules.md` is incremented.

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
| ~~Signal parameter exposure (4.3)~~ | ~~`strategy_rules.md` updated to formally define `top_n` and `lookback_days` as user-configurable~~ | ~~Strategy Rules owner + Product Owner~~ |
| AI Journal Summarisation | §13 boundary decision documented: does non-deterministic AI output conflict with the deterministic system principle? | Product Owner + Strategy Rules owner |
| New Technical Indicators | Strategy rules review: which indicators, if any, are canonical to this strategy? | Strategy Rules owner |
| Market Correlation | External data pipeline decision: do we ingest benchmark prices (SPY, FTSE)? | Product Owner + Head of Engineering |

> **Gate cleared (2026-03-04):** Signal parameter exposure (4.3) gate cleared by PoG POG-20260304-01. Item promoted to active v2.0 planning. See 4.3 entry in §3 above.

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
| **v1.6.1** | Correctness & Quick Wins | Quick Wins Bundle (6 features) — ✅ Shipped 2026-03-01 |
| **v1.7** | Foundation | CI/CD gate, §13 boundary review, metrics definitions, observability, API versioning decision — ✅ Shipped 2026-03-03 |
| **v1.8** | Risk Dashboard | Full risk page — heat, drawdown, grace period, position-level risk — ✅ Shipped 2026-03-06 |
| **v1.9** | User Value & Insight | ✅ Fully Shipped (Sprint 1: 2026-03-09; Sprint 2: 2026-03-13) — Risk Dashboard fixes, test infrastructure, docs hygiene, trade reflection template, compliance metrics, cohort analysis, R-multiple distribution, dashboard homepage |
| **v2.0** | Reporting & Alerts | Alerts & notifications (QA gate pending), tax-year statement, server-side PDF, signal parameter exposure (gate cleared — active planning) |
| **v2.1+** | Enhancements | Watchlists, chart interactivity, Prometheus |

---

*For delivery history, see `docs/product/changelog.md`.*
*For backlog and quick wins, see `claude/backlog/backlog.md`.*
*For strategic constraints and system boundaries, see `docs/specs/strategy_rules.md`.*
