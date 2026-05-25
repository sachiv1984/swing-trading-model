# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-05-22 (post-ship closure 2026-05-21__release-v3.9 — 7 items marked COMPLETE: BLG-TECH-10, BLG-BE-10, BLG-BE-11, BLG-BE-12, BLG-FE-37, BLG-FE-38, BLG-GOV-25; BLG-FEAT-25 STALE note added)
**Last rebalance:** 2026-05-22 (cycle 2026-05-22__scheduled — DL-033; IW-20260522-01; 32 new items: BLG-GOV-30–39, BLG-SPEC-33–37, BLG-BE-16–18, BLG-FE-40–43, BLG-FEAT-36–39, BLG-OPS-25–27, BLG-QA-25–27)

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

> 📋 Placement Rule
> New items must be appended to the correct existing type section (§1–§8). Do not create new numbered session sections. The backlog is organised by type, not by session date.
> **Ephemeral sections** (Release Slice tables, Test Scenario Gap sections, and "Returned to Backlog" sections appended by governance engines) are temporary. They must be removed during the next `groom backlog` run after the cycle closes. Any still-open items within them must be promoted to the appropriate §1–§8 type section before the ephemeral section is removed.

*Completed and killed items are recorded in `claude/backlog/backlog_archive.md`.*

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

*BLG-TECH-05 deferred to §9 (DL-023, 2026-04-24).*

---

*BLG-TECH-10 (Fix Yahoo Finance crumb/401 rate-limiting in screener batch) — ✅ COMPLETE v3.9 — ST-01, cycle: 2026-05-21__release-v3.9*

---

## 2. Product Feature Backlog (User-Facing)

---

*BLG-FEAT-18 (Consecutive losing streak metric) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-FEAT-19 (Monthly P&L summary report) — ✅ COMPLETE v3.1 — archived to backlog_archive.md 2026-05-05*

---

### BLG-FEAT-20 — Net-of-costs performance tracking
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260321-02 — promoted cycle 2026-05-05__scheduled (DL-024)
**Effort:** M (~2–3 days)
**Provisional-Target:** Arc 3/4 context (deliver alongside Arc 3 or Arc 4 data model work — not a standalone sprint item)

**Problem**
Performance metrics (R-multiple, win rate, expectancy) use gross P&L figures. When evaluating edge in Arc 4/6, R-multiples that ignore transaction costs overstate performance and may mask a genuinely unprofitable strategy. The Fee Drag % metric (v2.4) surfaces aggregate cost impact but per-trade R-multiples remain gross.

**Scope**
- Add brokerage cost fields per trade (commission, spread cost in GBP) — optional capture, not mandatory
- Recalculate R-multiple as net-of-costs where cost data is present
- Surface net-of-costs vs gross R-multiple on trade records and performance reports
- Sequence alongside Arc 3/4 data model work to avoid standalone migration overhead

**Acceptance Criteria**
- Brokerage cost fields capturable per trade (optional — not all trades will have explicit cost data)
- Net-of-costs R-multiple calculated and displayed where cost data exists
- Performance report breakdowns show gross vs net comparison where material
- No impact to existing R-multiple calculations where cost data is absent

---

*BLG-FEAT-21 (Trade plan abandonment status field) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FEAT-23 (Setup type classification field on trade plans) — ✅ COMPLETE v3.8 — ST-06, cycle: 2026-05-19__release-v3.8 — archived to backlog_archive.md 2026-05-21*

---

*BLG-FEAT-24 (AI-assisted setup thesis generation) — ✅ COMPLETE v3.8 — ST-08, cycle: 2026-05-19__release-v3.8 — archived to backlog_archive.md 2026-05-21*

---

*BLG-FEAT-22 (Ticker Universe Management page) — ✅ COMPLETE v3.8 — ST-09, cycle: 2026-05-19__release-v3.8 — archived to backlog_archive.md 2026-05-21*

---

### BLG-FEAT-25 — PT-04 Setup Quality Score (backend + frontend)
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Head of Backend Engineering; Metrics & Analytics Owner; Head of UX & Design
**Source:** Arc 2 roadmap — deferred from v3.8 (ST-04/ST-05, EPIC-02) — gate not met 2026-05-19: < 20 closed trades. Traceability entry added by delivery verification engine 2026-05-20.
**Effort:** L (~2–4 days, backend + frontend)
**Provisional-Target:** v4.0+ (gate-conditional — explicit re-park confirmed by PO 2026-05-22: advance when 20+ closed trades confirmed)
**Gate:** PO confirms 20+ closed trades in production before sprint planning for the target release. PMO Lead checks gate status at each release planning kickoff.

*PO disposition 2026-05-22: remain on backlog under gate — advance when 20+ closed trades confirmed. STALE flag cleared.*
*ST-10 (backend) and ST-11 (frontend) returned from 2026-05-22__release-v4.0 at sprint planning — gate not met (PO confirmed <20 closed trades 2026-05-23). 4th deferral noted.*

**Problem**
A deterministic setup quality score (0–100) based on own trade history cannot be computed until sufficient closed trades exist. When the user has entered with similar regime/signal/ATR conditions before, the score reflects historical win rate under those conditions. The gate condition (20+ closed trades) was not met at v3.8 sprint planning (PO confirmed 2026-05-19).

**Scope (Backend — ST-04)**
- `GET /trade-plans/setup-quality-score?ticker={ticker}` endpoint
- Score (0–100) computed from closed trade history matching current regime/signal/ATR conditions
- Gate response: `{"gate_not_met": true, "min_trades_required": 20}` when fewer than 20 closed trades
- Score factors: matching_trades count, win_rate, average_R, score_explanation
- Endpoint registered in backend/routers/test.py and openapi.yaml

**Scope (Frontend — ST-05)**
- Setup Quality Score displayed in Pre-Trade Research View and Trade Plan form
- Score badge with numeric value (0–100) and qualitative label (Excellent/Good/Fair/Low)
- "Insufficient trade history (< 20 trades)" message when gate not met
- Tooltip/expandable: matching_trades, win_rate, average_R

**Acceptance Criteria**
- Backend: endpoint implemented, gate enforced, unit tests cover gate_not_met, gate_met mixed, perfect history
- Frontend: score renders in Pre-Trade Research View and Trade Plan form; gate-not-met state clearly displayed; score updates when ticker changes
- Playwright: score renders; gate-not-met message renders; score updates on ticker change

---

### BLG-FEAT-26 — ATR position-sizing retrospective analysis
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped and live for ≥ 30 days; sufficient attributed closed trades to support retrospective.

**Problem**
There is no retrospective view of whether ATR-based position sizing (risked R per trade) was consistent over time, or whether deviation from the ATR sizing formula correlated with outcome. Understanding sizing discipline and its P&L impact requires a dedicated analytics view built on historical trade data.

**Scope**
- Retrospective dashboard: actual position size vs ATR-recommended size per trade
- Correlation view: sizing deviation vs R-multiple outcome
- Summary metric: sizing discipline score over rolling window

**Acceptance Criteria**
- ATR-sizing deviation visible per trade and in aggregate
- Correlation between sizing deviation and R-multiple summarised
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-27 — Candidate quality retrospective (screener-to-trade attribution)
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days AND ≥ 60 closed trades with screener attribution.

**Problem**
No retrospective analysis links screener-surfaced candidates to eventual trade outcomes. Without attribution, it is impossible to evaluate whether the screener is generating genuinely high-quality candidates or just high-volume noise. This item requires sufficient attributed history (60d + 60 trades) to yield statistically meaningful results.

**Scope**
- Attribution link: screener candidate → watchlist → trade plan → closed trade
- Retrospective metric: screener hit rate, win rate of attributed trades vs baseline
- Filter by screener run date range

**Acceptance Criteria**
- End-to-end attribution pipeline queryable
- Screener hit rate and attributed-trade win rate reportable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-28 — Screener hit rate metric
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days.

**Problem**
No aggregate metric tracks how often screener results lead to a trade plan or closed position. The screener hit rate (surfaced candidates that progressed to trade) is a key indicator of screener quality and operator workflow efficiency. This metric requires 60 days of screener history to be meaningful.

**Scope**
- Aggregate metric: screener_candidates_total, advanced_to_watchlist, advanced_to_trade_plan, advanced_to_closed_trade
- Displayable in governance/operations reporting view

**Acceptance Criteria**
- Hit rate metric computed and displayable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-29 — Regime distribution metric over screener history
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-04 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days.

**Problem**
No view exists showing how market regime distribution (bull/bear/neutral/volatile) has evolved across screener runs over time. Understanding regime frequency and drift helps contextualise screener output quality and strategy performance in different market conditions.

**Scope**
- Aggregate view: regime distribution over screener history (rolling 30d/60d/all)
- Displayable as percentage breakdown or time-series chart

**Acceptance Criteria**
- Regime distribution over screener history computable and displayable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-30 — Screener-to-trade full attribution pipeline
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-05 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** L (~3–4 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days AND ≥ 60 closed trades with screener attribution.

**Problem**
The full pipeline from screener hit → watchlist add → research → trade plan → execution → close is not yet instrumented end-to-end. Attribution gaps prevent retrospective analysis of conversion rates at each stage and make it impossible to identify where candidates are lost or degraded.

**Scope**
- Full attribution model: screener_run_id linkage through to trade close
- Conversion funnel: screener → watchlist → plan → closed
- Exportable for offline analysis

**Acceptance Criteria**
- Full attribution pipeline implemented
- Conversion funnel metrics computable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-31 — Research-to-trade conversion rate metric
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-06 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-02 (Research View) live ≥ 30 days AND ≥ 30 research sessions with attribution.

**Problem**
No metric tracks how often a research session (opening the research view for a ticker) results in a trade plan creation. This conversion rate is an indicator of research quality and operator decision confidence. Requires 30 days of research session history with attribution.

**Scope**
- Metric: research_sessions_total, sessions_leading_to_plan, sessions_leading_to_closed_trade
- Attribution requires `session_id` or equivalent linkage from research view to trade plan

**Acceptance Criteria**
- Research-to-trade conversion rate computable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-32 — Trade plan completion rate tracking
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-07 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped.

**Problem**
No metric tracks what proportion of created trade plans are completed (i.e., result in a closed trade) vs abandoned. The completion rate is a key indicator of plan quality, operator follow-through, and whether PT-04 quality scores correlate with plan execution. Requires PT-04 to create the quality score baseline for correlation.

**Scope**
- Metric: plans_created, plans_completed (closed trade), plans_abandoned, completion_rate
- Optional: completion rate segmented by setup quality score tier

**Acceptance Criteria**
- Trade plan completion rate computable and displayable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-33 — Trade plan approval workflow
**Priority:** P3 (Low)
**Type:** Product Feature / Workflow
**Owner:** Product Owner; Head of UX & Design
**Source:** IDEA-trade-plan-20260508-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** L (~3–4 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-05 (Trade Plan feature set) live ≥ 3 months with ≥ 20 plans created; operator confirms approval workflow adds value.

**Problem**
Trade plans are currently created and immediately actionable without a formal review or approval step. As plan complexity grows (multi-day setup, multi-leg risk), an explicit approval checkpoint may improve discipline — but the value of an approval workflow vs friction cost is not yet established. Gate ensures sufficient usage history before committing implementation effort.

**Scope**
- Approval state: Draft → Pending Approval → Approved / Rejected
- Approval action: operator-controlled (self-approval supported for solo use)
- Approved plans visible separately from drafts

**Acceptance Criteria**
- Approval workflow implemented and functional
- Plan state transitions correct and persisted
- Gate condition and usage volume verified by Product Owner before sprint planning

---

### BLG-FEAT-34 — Trade plan P&L attribution
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner; Financial Reporting & Records Owner
**Source:** IDEA-trade-plan-20260508-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** `plan_id` linkage live on closed trades (PT-05 shipped and plans actively used).

**Problem**
Closed trade P&L cannot currently be attributed back to the trade plan that governed the entry. Without `plan_id` on position records, it is impossible to compare planned R-risk vs realised R-multiple or evaluate whether adhering to a plan improved outcomes vs discretionary deviation.

**Scope**
- Link `plan_id` from trade plan to position/trade close record
- Attribution report: planned_risk_R vs realised_R per attributed trade
- Aggregate: plan-adhered trades vs plan-deviated trades outcome comparison

**Acceptance Criteria**
- `plan_id` linkage implemented on closed trades
- Attribution report computable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-35 — Entry zone discipline reporting
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-trade-plan-20260508-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 20 closed trades with linked trade plans AND `entry_delta_pct` field captured on closed trades.

**Problem**
No metric tracks whether entries were executed within the planned entry zone. `entry_delta_pct` (actual entry vs planned entry midpoint) is a candidate field but is not yet captured at trade close. Without this data, it is impossible to assess entry zone discipline or its correlation with trade outcome.

**Scope**
- Capture `entry_delta_pct` on trade close: actual_entry_price vs planned_entry_zone midpoint
- Discipline metric: % of trades entering within planned zone
- Correlation: entry discipline vs R-multiple outcome

**Acceptance Criteria**
- `entry_delta_pct` captured on trade close where plan linkage exists
- Entry discipline metric computable and displayable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-36 — SI-01 validation pass/fail rate by rule
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-analytics-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2–3 days)
**Provisional-Target:** v4.0

**Problem**
GET /portfolio/pre-entry-validation (SI-01, shipped v3.8) returns per-attempt pass/fail results but no aggregate metric tracks pass/fail rate broken down by individual rule type over time. Understanding which rules most frequently block entries reveals behavioural patterns (e.g., "regime gate fails 40% of the time") without requiring SI-02 (drift detection).

**Scope**
- Define named metric: validation_pass_rate_by_rule — pass count / (pass + fail count) per rule per rolling period
- Backend: query pre-entry validation log for rule-level pass/fail aggregation
- Frontend: surface metric in SI-05 Weekly Digest or standalone compliance dashboard
- Requires confirmation that the pre-entry validation log captures per-rule outcomes (may require minor schema addition)

**Acceptance Criteria**
- Pass/fail rate per rule computable and displayable
- Rolling period configurable (7d / 30d)
- Backend analysis of current log schema completed before sprint planning

---

### BLG-FEAT-37 — Red flag event frequency metric
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-analytics-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Problem**
No canonical metric tracks red flag event frequency over time. Override rate and rule-breach-by-type distribution are queryable from red_flag_events (shipped v3.9) but not defined as named product metrics with specified aggregation periods and display locations. Defining these metrics makes them inputs to SI-05 Weekly Digest and the monthly P&L compliance section.

**Scope**
- Named metrics: events_per_week, override_rate (overrides / validation attempts), event_type_distribution
- Backend: aggregate query on red_flag_events table
- Metric definitions registered in metrics_definitions.md

**Acceptance Criteria**
- Three named metrics defined and queryable
- Metrics definitions registered per canonical standards
- Data available for SI-05 and BLG-FEAT-38 (monthly P&L compliance section) consumption

---

### BLG-FEAT-38 — Arc 5 compliance score in monthly P&L report
**Priority:** P3 (Low)
**Type:** Product Feature / Reporting
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-FEAT-36 (SI-01 pass rate metric) and BLG-FEAT-37 (red flag frequency metric) shipped.

**Problem**
Monthly P&L report (shipped v3.1) covers financial performance. As Arc 5 ships compliance data, adding a strategy compliance section enables holistic monthly review: financial performance + behavioural discipline in one document.

**Scope**
- New section in monthly P&L report: strategy compliance period summary
- Fields: validation_pass_rate (period), override_count, red_flag_events_count, most_frequent_rule_breach
- Data sourced from BLG-FEAT-36 and BLG-FEAT-37 metrics

**Acceptance Criteria**
- Compliance section present in monthly P&L report output
- Data sourced from canonical metrics (BLG-FEAT-36, BLG-FEAT-37)
- Gate conditions verified before sprint planning

---

### BLG-FEAT-39 — Trade plan adherence rate metric
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Gate criteria:** plan_id linkage actively captured on closed trades (requires active use of trade plan creation workflow).

**Problem**
No metric tracks what percentage of closed trades have an associated trade plan (plan_id linkage). This metric measures systematic discipline adoption — whether the operator is consistently using trade plans before entry. It is a direct input to Arc 4 PO-04 (reflection/outcome correlation) and a candidate for the compliance section of the monthly P&L report.

**Scope**
- Named metric: trade_plan_adherence_rate — trades_with_plan_id / total_closed_trades
- Backend: aggregate query on closed trades
- Metric definition registered in metrics_definitions.md
- Surface in performance reports and SI-05 Weekly Digest

**Acceptance Criteria**
- Metric defined and queryable
- Registered in metrics definitions
- Gate condition verified by Product Owner before sprint planning

---

## 3. Frontend & UX Backlog

---

*BLG-FE-16 (React component inventory) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*


---

*BLG-FE-19 (Keyboard shortcuts) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*
*BLG-FE-18 (Screener news panel attachment) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-FE-21 (Design system document) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

*BLG-FE-31 (Research view component library) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-22 (Screener morning routine UX spec) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-23 (Research page UK ticker suffix not stripped) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-24 (Negative earnings days display for past earnings dates) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-25 (Signals page: default to most recent day's signals) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-26 (Research page UX review: regime lozenge and font consistency) — ✅ COMPLETE v3.6 — archived to backlog_archive.md 2026-05-17*

---

### BLG-FE-27 — Nav bar redesign exploration
**Priority:** P3 (Low)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design
**Source:** v3.2 delivery verification — user feedback 2026-05-06
**Effort:** M (~1–2 days design + spec)
**Provisional-Target:** Arc 3 (design exploration — not urgent; no current blocking workflow)

**Problem**
The current nav bar occupies a fixed portion of the visible screen area. As the application grows in Arc 2 and beyond, the navigation structure may benefit from a redesign to reclaim vertical space. Options to evaluate: Sticky/Fixed Header (current pattern, optimised), mega menu (grouped sections), or breadcrumb navigation (context-sensitive, minimal footprint).

**Scope**
- Head of UX & Design to evaluate the three navigation patterns in the context of current and Arc 2 page inventory
- Produce a design recommendation with rationale (no implementation required at this stage)
- If redesign is recommended, produce a UX spec and create a follow-on implementation backlog item

**Acceptance Criteria**
- Design recommendation document produced (one of: maintain current, redesign to pattern X)
- Rationale covers: screen real-estate impact, mobile responsiveness, Arc 2 page count
- If redesign: UX spec produced and implementation backlog item filed

---

*BLG-FE-28 (Pre-Trade Research View UX spec) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-FE-29 (Watchlist research status indicator) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-30 (Trade plan status badges) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-FE-34 (Trade plan form signal context panel — SignalContextPanel.js with entry_rationale/confirmation pre-population) — ✅ COMPLETE v3.7 — ST-03, cycle: 2026-05-18__release-v3.7*

---

*BLG-FE-33 (Signals page Add to Watchlist CTA — watchlisted status backend + SignalCard CTA replacement) — ✅ COMPLETE v3.7 — ST-01 + ST-02, cycle: 2026-05-18__release-v3.7*

---

*BLG-FE-32 (Research view SC-RV-18/SC-RV-19 Playwright coverage) — ✅ COMPLETE v3.6 — archived to backlog_archive.md 2026-05-17*

---

*BLG-FE-35 (ST-08 AC-02: Research page font conformance staging) — ✅ COMPLETE v3.7 — staging run performed 2026-05-18 (Head of UX & Design); conformant; Playwright SC-RV-TYP-01 added for CI regression; archived to backlog_archive.md 2026-05-18*

---

*BLG-FE-36 (Add news context panel to trade plan form) — ✅ COMPLETE v3.8 — ST-07, cycle: 2026-05-19__release-v3.8 — archived to backlog_archive.md 2026-05-21*

---

*BLG-FE-37 (Strip .L suffix from Ticker Universe page display labels) — ✅ COMPLETE v3.9 — ST-05, cycle: 2026-05-21__release-v3.9*

---

*BLG-FE-38 (Add degraded-run warning to screener when OHLCV failure rate exceeds 20%) — ✅ COMPLETE v3.9 — ST-04, cycle: 2026-05-21__release-v3.9*

---

### BLG-FE-39 — Arc 2 user journey map
**Priority:** P3 (Low)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design
**Source:** IDEA-ux-design-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped.

**Problem**
No end-to-end user journey map exists covering the full Arc 2 flow: Screener → Watchlist → Research View → Trade Plan → Execution. As Arc 2 ships its final features, a journey map would surface UX gaps, confirm feature sequencing, and establish the baseline for Arc 3 UX planning. Requires PT-04 to be shipped so the full flow is complete before mapping.

**Scope**
- User journey map covering screener discovery → trade plan creation → execution
- Identify friction points and hand-off gaps between views
- Produce design recommendation: maintain current or file targeted UX improvement items

**Acceptance Criteria**
- Journey map document produced
- Friction points enumerated; any actionable items filed as backlog entries
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FE-40 — Red Flag Journal filter state persistence
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend; Head of UX & Design
**Source:** IDEA-base44-frontend-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Red Flag Journal in active use for ≥ 30 days post-v3.9 (confirm filter persistence adds value before implementing).

**Problem**
Red Flag Journal filter state (date range, severity, rule type) resets on page reload. Users who open the RFJ daily to review recent events must re-apply their filter preferences on each visit. localStorage persistence is a standard UX pattern that reduces friction on repeat visits.

**Scope**
- Persist RFJ filter state to localStorage (date range, event type, severity if/when added)
- Version the localStorage key to handle filter schema changes gracefully
- Restore filter state on page load; clear stale state if key version mismatch

**Acceptance Criteria**
- Filter state persists across page reloads
- Stale state (version mismatch) cleared gracefully without error
- Playwright test: set filter → reload page → verify filter state restored
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FE-41 — Red Flag Journal visual design review
**Priority:** P3 (Low)
**Type:** Frontend / UX Design
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days design + spec)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-03 Red Flag Journal live ≥ 30 days (on/after 2026-06-21).

**Problem**
Red Flag Journal (v3.9) is functional but minimally styled. As RFJ becomes a primary Arc 5 review surface, a design review covering severity visual hierarchy, timeline layout option, and colour coding for rule breach types will improve usability and consistency with the rest of the application design language.

**Scope**
- Design review: severity visual hierarchy; event type colour coding; timeline vs list layout evaluation
- Produce design recommendation with rationale
- If redesign recommended: produce UX spec and file implementation backlog item
- Review against existing design system

**Acceptance Criteria**
- Design recommendation document produced
- If redesign: UX spec produced and implementation item filed
- Gate condition verified before sprint planning

---

### BLG-FE-42 — Arc 5 navigation and information architecture cohesion review
**Priority:** P2 (Medium)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 (Behavioural Drift Detection) in sprint planning — Arc 5 near-complete.

**Problem**
As Arc 5 ships SI-02, SI-04, and SI-05 alongside existing SI-01 and SI-03, the "Trading" navigation section may become congested. A cohesion review before Arc 5 is complete ensures any structural navigation changes are planned proactively rather than reactively patched after all features ship.

**Scope**
- Review current Trading nav structure against projected Arc 5 complete state (SI-01 through SI-05)
- Assess: navigability, grouping logic, naming clarity, page depth
- Produce recommendation: maintain current or propose structural changes
- If changes recommended: author UX spec and file implementation item

**Acceptance Criteria**
- Cohesion review document produced
- Recommendation covers projected full Arc 5 nav inventory
- Gate condition verified by Head of UX & Design before sprint planning

---

### BLG-FE-44 — Research view: surface signal_type as Setup Type column
**Priority:** P3 (Low)
**Type:** Frontend / Backend
**Owner:** Head of Engineering; Head of UX & Design
**Source:** v4.0 sprint execution — out-of-scope change stashed and deferred
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
The Research page signal card shows Current Price, Signal, Status, ATR, and Entry Price but does not surface `signal_type` (e.g. "strong_momentum", "momentum"). This field is already in the signals table and available in `GET /research/{ticker}` response. Adding it gives traders immediate context on setup quality without navigating away.

**Scope**
- `backend/routers/research.py`: include `signal_type` in `_get_signal()` response dict (1-line change)
- `src/pages/Research.js`: add `SetupTypeBadge` component; add 5th column to Price & Signal grid showing setup type with colour-coded badge (violet for strong_momentum, cyan for momentum)
- No new endpoint, no schema change, no migration required

**Acceptance Criteria**
- AC-01: `GET /research/{ticker}` response includes `signal_type` field
- AC-02: Research page Price & Signal section shows Setup Type badge alongside ATR and Entry Price
- AC-03: strong_momentum → violet badge; momentum → cyan badge; null → dash

---

### BLG-FE-43 — SI-05 Weekly Digest frontend component spec
**Priority:** P2 (Medium)
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner; Base44 Frontend
**Source:** IDEA-base44-frontend-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-05 (Weekly Strategy Integrity Digest) sprint planning imminent.

**Problem**
SI-05 will deliver the Weekly Strategy Integrity Digest via Telegram notification and potentially an in-app view. No frontend component spec or UX spec exists for the digest display. Authoring this spec before sprint planning ensures frontend scope is clearly defined and sized — preventing mid-sprint ambiguity on rendering requirements.

**Scope**
- UX spec: digest layout, content sections (drift signal, red flag summary, compliance score trend), notification vs in-app view decision
- Component requirements document: data inputs, update frequency, display states (no data, loading, populated)
- Review against Telegram notification format constraints (v2.4 weekly digest pattern)

**Acceptance Criteria**
- Frontend component spec and UX spec produced and filed
- Component requirements document covers all SI-05 data inputs
- Spec reviewed by Product Owner and Head of UX & Design before sprint planning
- Gate condition verified before sprint planning

---

## 4. Backend & Data Backlog


---

*BLG-AI-02 (Model version contract for AI Journal) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-AI-03 (AI Journal Summarisation quarterly review cadence) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-BE-10 (Fix sector/industry data dropped in screener batch) — ✅ COMPLETE v3.9 — ST-02, cycle: 2026-05-21__release-v3.9*

---

*BLG-BE-11 (Remove DAY from ticker universe — invalid Yahoo Finance symbol) — ✅ COMPLETE v3.9 — ST-03, cycle: 2026-05-21__release-v3.9*

---

*BLG-BE-12 (Add company_name column to ticker universe) — ✅ COMPLETE v3.9 — ST-06, cycle: 2026-05-21__release-v3.9*

---

### BLG-BE-13 — Screener result history table
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** IDEA-backend-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days (sufficient history to make a queryable history table valuable).

**Problem**
Each screener run overwrites or appends to the current results without a queryable historical table. After 60 days, trend analysis (how screener output has evolved over time) becomes valuable but requires a properly structured history table with per-run metadata (run_timestamp, run_id, ticker count, pass count, regime distribution). Without this, historical comparison is not possible.

**Scope**
- `screener_run_history` table: run_id, run_timestamp, total_tickers, pass_count, regime_distribution JSON
- `GET /screener/history` endpoint returning run history with pagination
- Backfill not required; populate from next run forward

**Acceptance Criteria**
- History table created and populated on each screener run
- `GET /screener/history` returns paginated run history
- Gate condition verified by Product Owner before sprint planning

---

### BLG-BE-14 — Trade plan schema versioning
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering; Head of Specs Team
**Source:** IDEA-backend-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 3 new fields added to trade plan schema after v3.4 baseline (indicating schema churn warrants versioning overhead).

**Problem**
Trade plan schema has grown incrementally. If the schema continues to change at pace (new fields, deprecated fields), reading old plans stored under prior schema versions becomes an issue. Schema versioning adds a `schema_version` field to each trade plan record, enabling readers to apply the correct transformation for older records. Gate ensures the overhead is warranted before introducing this complexity.

**Scope**
- Add `schema_version` field to trade plan records (default: current version)
- Transformation layer: when reading plans, apply version-appropriate defaults for missing fields
- Migration: backfill existing plans with baseline schema_version

**Acceptance Criteria**
- `schema_version` field present on all trade plan records
- Read path applies correct field defaults for legacy records
- Gate condition (≥3 new fields post v3.4) verified by Product Owner before sprint planning

---

### BLG-BE-15 — Validate ticker symbol on add (sector/industry lookup)
**Priority:** P1 (High)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** User request — 2026-05-22
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.0

**Problem**
When a user adds a ticker symbol and market to the universe, no validation is performed to confirm the ticker actually exists. Any arbitrary string can be saved, leading to junk entries that silently produce empty screener results or data fetch errors. Validating sector and industry at add-time gives immediate feedback and prevents invalid tickers from polluting the universe.

**Scope**
- On ticker add (POST `/tickers` or equivalent), call the market data provider (Yahoo Finance) to fetch sector and industry for the submitted symbol+market
- If the lookup returns no data or raises an error, reject the request with a clear 400/422 response and message (e.g. "Ticker XXXX not found — please check the symbol and market")
- If the lookup succeeds, optionally auto-populate sector/industry fields from the returned data
- Frontend to surface the rejection error inline on the add-ticker form

**Acceptance Criteria**
- Submitting a non-existent ticker symbol returns an error response and the ticker is not saved
- Submitting a valid ticker returns success; sector and industry are confirmed present
- Error message displayed to user is specific and actionable (not a generic 500)
- Existing tickers already in the universe are unaffected

---

### BLG-BE-16 — Red flag events severity field
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model & Domain Schema Owner; Head of Backend Engineering
**Source:** IDEA-data-model-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 (Behavioural Drift Detection) sprint planning imminent — severity taxonomy should be informed by SI-02 design to avoid schema rework.

**Problem**
red_flag_events table (shipped v3.9) has no severity classification. Adding a severity field (info/warning/critical) enables better filtering in SI-03 Red Flag Journal, more actionable grouping in SI-05 Weekly Digest, and meaningful colour coding in BLG-FE-41 visual design review. The field is additive and backward-compatible but should be deferred until SI-02 sprint planning is imminent to ensure the severity taxonomy is informed by drift detection severity requirements.

**Scope**
- Add `severity` column to `red_flag_events` table: enum (info/warning/critical)
- Default severity for existing event types (SI-01 overrides: warning; future drift events: critical)
- Migration: backfill existing events with default severity
- Update `GET /portfolio/red-flag-journal` to support severity filter parameter
- Update openapi.yaml with severity field and filter parameter

**Acceptance Criteria**
- severity field present on all red_flag_events records
- `GET /portfolio/red-flag-journal?severity=warning` filters correctly
- Migration backfills existing events without data loss
- openapi.yaml updated
- Gate condition verified by Product Owner before sprint planning

---

### BLG-BE-17 — SI-02 drift detection query pre-design
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Spec Pre-work
**Owner:** Head of Backend Engineering
**Source:** IDEA-backend-engineering-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 sprint planning imminent.

**Problem**
SI-02 (Behavioural Drift Detection) requires rolling analysis queries over trade history comparing actual entry conditions against stated setup criteria. The SQL and data access patterns for these queries are not pre-designed. Mid-sprint discovery of missing data fields (e.g., regime_at_entry not captured) would require emergency schema migration. Pre-designing the queries before sprint planning surfaces data gaps that can be addressed in the sprint plan.

**Scope**
- Define data access patterns: which fields are required per trade record for drift analysis
- Draft SQL queries: rolling win-rate vs stated setup criteria per entry type, per regime
- Identify any missing fields requiring schema migration (e.g., regime_at_entry, setup_type_at_entry)
- Output: technical pre-design document; input to SI-02 sprint planning
- Include assessment of query performance on current trade history volume

**Acceptance Criteria**
- Query pre-design document produced and reviewed by Head of Backend Engineering
- Missing data fields (if any) enumerated with migration scope estimate
- Document filed before SI-02 sprint planning seals
- Gate condition verified before sprint planning

---

### BLG-BE-18 — Arc 5 backend architecture review for SI query patterns
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Architecture
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 sprint planning imminent.

**Problem**
SI-02 (drift detection) and SI-04 (strategy version comparison) will add analytical queries over trade history that may be expensive synchronously. The current endpoint pattern (synchronous request/response) may not be appropriate for background rolling analysis. Before SI-02 sprint planning, assessing whether a background job or queue pattern is needed prevents an architectural dead-end mid-sprint.

**Scope**
- Review current endpoint pattern (synchronous FastAPI) against SI-02/SI-04 query complexity
- Assess: synchronous viability, background job option (Celery/cron), response caching
- Recommendation: maintain synchronous or add background processing layer
- If background layer recommended: produce architecture decision record (ADR)

**Acceptance Criteria**
- Architecture review document produced
- Synchronous vs background recommendation made with rationale
- If background layer recommended: ADR filed and input to SI-02 sprint planning
- Gate condition verified before sprint planning

### BLG-BE-19 — Base Gemini Flash API wiring — thesis generation service + endpoint
**Priority:** P1 (High)
**Type:** Backend Engineering / Frontend
**Owner:** Head of Backend Engineering
**Source:** Session observation 2026-05-22 — BLG-FEAT-24 marked complete v3.8 but Gemini not wired into codebase; prerequisite for BLG-GOV-35 and BLG-OPS-26
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Problem**
BLG-FEAT-24 (AI thesis generation) was marked complete in v3.8 but no Gemini code exists in the codebase — no `google-generativeai` dependency, no env var, no service, no endpoint. BLG-GOV-35 (Gemini audit trail) and BLG-OPS-26 (cost tracking) both instrument Gemini API calls; they have nothing to build on until the base wiring exists. This is a blocking prerequisite for both v4.0 EPIC-03 Sprint 2 stories.

**Scope**
- Add `google-generativeai` to `backend/requirements.txt`
- Wire `GEMINI_API_KEY` env var (Render + local `.env`)
- Create `backend/services/gemini_service.py` with `generate_setup_thesis(ticker, signal_data, plan_data) -> dict` using `gemini-1.5-flash`; returns `{thesis, model_version, prompt_version}` or graceful error
- Add `POST /trade-plans/{plan_id}/generate-thesis` endpoint in `backend/routers/trade_plans.py`
- Frontend: "Generate Thesis" button on TradePlan page that calls the endpoint and populates `setup_thesis` field

**Acceptance Criteria**
- `google-generativeai` present in `requirements.txt`
- `GEMINI_API_KEY` env var documented in `.env.example`
- `POST /trade-plans/{plan_id}/generate-thesis` returns `{thesis, model_version, prompt_version}` when key is set
- Returns graceful error (not 500) when `GEMINI_API_KEY` is absent
- Frontend button triggers generation and populates `setup_thesis` textarea
- New endpoint registered in `backend/routers/test.py` and `docs/reference/openapi.yaml`

---

## 5. QA & Test Automation Backlog

---

*BLG-QA-18 (Screener accuracy test protocol) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-QA-14 (Author Playwright E2E test suite for entry checklist) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*TEST-GAP-ST14 (AI audit service unit tests) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-QA-15 (PT-02 research view acceptance test protocol) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-QA-16 (Research endpoint integration test coverage) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-QA-17 (Research view test scenario library) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*TEST-GAP-EPIC-03-v33 (SC-RV-18 and SC-RV-19 Playwright coverage) — ✅ COMPLETE v3.6 — archived to backlog_archive.md 2026-05-17*

---

*BLG-QA-19 (Research view regression test protocol) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-QA-20 (Consolidate database stub files into shared pytest conftest fixture — session-scoped stub) — ✅ COMPLETE v3.7 — ST-09, cycle: 2026-05-18__release-v3.7*

---

### BLG-QA-21 — Arc 2 end-to-end QA protocol
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead
**Source:** IDEA-qa-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped — Arc 2 feature set complete.

**Problem**
No consolidated end-to-end QA protocol covers the full Arc 2 feature set (Screener, Research View, Trade Plan, Setup Quality Score). Individual EPICs have per-story DoQ sign-offs, but there is no arc-level protocol that exercises the full workflow from screener discovery to closed trade with a quality score. Such a protocol is most valuable once Arc 2 is complete.

**Scope**
- Arc-level E2E test protocol document covering full Arc 2 flow
- Playwright automation for the core arc-level happy path
- Manual checklist for Arc 2 edge cases not covered by Playwright

**Acceptance Criteria**
- Arc 2 E2E protocol document produced and filed in `docs/qa/`
- Core happy path covered by Playwright
- Gate condition verified by QA Lead and Product Owner before sprint planning

---

### BLG-QA-22 — Arc 2 DoQ standards review
**Priority:** P3 (Low)
**Type:** QA / Governance
**Owner:** QA Lead; Head of Specs Team
**Source:** IDEA-qa-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped — Arc 2 feature set complete.

**Problem**
DoQ standards (shared_standards.md §DoQ) were established in Arc 1 and have evolved incrementally. Arc 2 introduced new feature types (research views, AI-assisted UX, trade plans) that may expose gaps in the existing DoQ rubric. A targeted review of DoQ standards against Arc 2 artefacts will ensure the standards remain fit for Arc 3 and beyond.

**Scope**
- Review DoQ standards against Arc 2 EPIC QA evidence files
- Identify any rubric gaps introduced by Arc 2 feature types
- Propose amendments to `shared_standards.md` DoQ section if warranted

**Acceptance Criteria**
- DoQ standards reviewed; gaps (if any) documented
- If amendments warranted: `shared_standards.md` updated per §6 governance checklist
- Gate condition verified before sprint planning

---

### BLG-QA-23 — Trade plan lifecycle end-to-end test
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead
**Source:** IDEA-qa-20260421-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped.

**Problem**
No Playwright test covers the full trade plan lifecycle: create → edit → link to position → close → view in plan-vs-reality. Individual story tests cover creation and display, but lifecycle continuity (plan survives position link, quality score visible at creation, plan-vs-reality renders post-close) is not tested end-to-end. PT-04 must be shipped to make the quality-score step part of the lifecycle.

**Scope**
- Playwright E2E test: create plan with quality score visible → link to position → close position → verify plan-vs-reality
- Cover: plan state transitions, quality score persistence, plan-vs-reality accuracy

**Acceptance Criteria**
- Full lifecycle Playwright test authored and passing in CI
- Gate condition verified by QA Lead and Product Owner before sprint planning

---

### BLG-QA-24 — Yahoo Finance backoff path integration test stub
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead
**Source:** DoQ sign-off notation — EPIC-01 v3.9 QA evidence, 2026-05-22
**Effort:** S (~0.5 days)
**Provisional-Target:** Unscheduled

**Problem**
ST-01 AC-04 ("screener run completes without >5% OHLCV failures under normal YF conditions") is a runtime/environment-dependent criterion. The crumb refresh mechanism and exponential backoff are unit-tested, but a controlled integration test stub that simulates the full 401 → crumb-refresh → backoff → retry → success path is absent. The DoQ sign-off for EPIC-01 accepted this as staging-only evidence and filed this backlog item.

**Scope**
- Add integration test to `tests/test_screener_data_service.py` that stubs the Yahoo Finance session, injects a 401 followed by a 200 with valid chart data, and verifies that the result is non-null and the retry occurred exactly once.
- Verify exponential backoff timing via mock of `_time.sleep`.

**Acceptance Criteria**
- Integration test runs without a live Yahoo Finance connection
- Test verifies: 401 first call → crumb refresh → sleep called once → 200 second call → valid OHLCV result returned
- Passes in CI

---

### BLG-QA-25 — Red Flag Journal E2E Playwright test (SI-01→SI-03 integration path)
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner; QA Lead
**Source:** IDEA-qa-testing-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Problem**
SC-RFJ-01/02/03 (v3.9) cover RFJ component-level display. The SI-01 → SI-03 integration path — where a SI-01 override event is written and subsequently appears in the Red Flag Journal — is not tested end-to-end. This integration path is the primary produce of the Arc 5 data pipeline and is critical to validate before SI-02/SI-04/SI-05 extend the event model.

**Scope**
- Playwright E2E test: navigate to a position → trigger pre-entry validation → acknowledge override → navigate to Red Flag Journal → verify override event is present with correct metadata (type, timestamp, rule breached)
- Cover: filter by event type → verify filtered results contain the override event
- Integrate into existing Playwright test suite

**Acceptance Criteria**
- Full SI-01→SI-03 integration path covered by Playwright test
- Test passes in CI
- Override event metadata (type, timestamp, rule) verified in RFJ display

---

### BLG-QA-26 — Arc 5 QA protocol
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** All five Arc 5 features (SI-01 through SI-05) shipped.

**Problem**
SI-01 through SI-03 shipped across v3.8 and v3.9. Each sprint produced per-story DoQ sign-offs but no arc-level QA protocol exists covering the full Arc 5 feature set end-to-end. Once all five features ship, an arc-level protocol analogous to BLG-QA-21 (Arc 2 E2E QA protocol) will ensure the complete Strategy Integrity workflow is tested holistically.

**Scope**
- Arc-level E2E test protocol document covering full Arc 5 flow: validation gate → override event → red flag journal → drift detection review → strategy version comparison → weekly digest
- Playwright automation for the arc-level happy path
- Manual checklist for Arc 5 edge cases not covered by Playwright
- Filed in `docs/qa/arc5_qa_protocol.md`

**Acceptance Criteria**
- Arc 5 E2E protocol document produced and filed
- Core happy path covered by Playwright
- Gate condition verified by QA Lead and Product Owner before sprint planning

---

### BLG-QA-27 — CI test suite execution time baseline
**Priority:** P3 (Low)
**Type:** QA / Operations
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** CI pipeline total execution time exceeds 5 minutes sustained across 3+ consecutive cycles.

**Problem**
As the test suite grows with Arc 5 additions (BLG-QA-25 + per-sprint Playwright tests), no baseline exists for total CI pipeline execution time. Without a baseline, suite bloat is invisible until developer cycle time is materially impacted. A baseline established when the gate is met enables regression detection for each subsequent sprint.

**Scope**
- Establish CI pipeline execution time baseline: unit tests, integration tests, Playwright suite
- Record p50/p95 execution times per suite tier
- File baseline in `docs/ops/ci_performance_baseline.md`
- Define regression threshold: > 1.5× baseline triggers advisory

**Acceptance Criteria**
- CI execution time baseline measured and filed
- Regression threshold defined
- Gate condition verified by QA Lead before sprint planning

### BLG-QA-28 — Playwright E2E coverage for Arc5ComplianceSection (PerformanceAnalytics §19)
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead
**Source:** v4.0 ST-02/ST-04 EPIC-01 — deferred observable AC per CLAUDE.md §2
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
ST-02 and ST-04 introduced Arc5ComplianceSection (four stat cards: Red Flag Events/Week, Override Rate, Top Rule Breach, Trade Plan Adherence) into PerformanceAnalytics.js §19. These are frontend-visible changes but no Playwright test covers the rendering. Per CLAUDE.md §2, a backlog item must be filed before the PR opens when observable AC is deferred to staging.

**Scope**
- Add Playwright test in `tests/e2e/` for PerformanceAnalytics page
- Cover: Arc5ComplianceSection heading present, all 4 card titles visible, loading skeleton renders, error state renders "Unable to load"
- Use `page.route()` to mock `GET /analytics/arc5-compliance`

**Acceptance Criteria**
- AC-01: "Arc 5 Signal Compliance" heading visible on PerformanceAnalytics page
- AC-02: All 4 stat card titles visible (Red Flag Events/Week, Override Rate, Top Rule Breach, Trade Plan Adherence)
- AC-03: Loading skeleton shown when API pending
- AC-04: Error state shown when API returns 500

---

### BLG-QA-29 — Staging verification for Gemini thesis generation (ST-12 staging-only AC)
**Priority:** P2 (Medium)
**Type:** QA / Staging Verification
**Owner:** QA Lead
**Source:** v4.0 ST-12 EPIC-03 — staging-only AC per CLAUDE.md §2
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
ST-12 (Gemini Flash base wiring) introduced `POST /trade-plans/{plan_id}/generate-thesis` and the "Improve with AI" button in TradePlan. The acceptance criteria for thesis generation requires a live `GEMINI_API_KEY`. This cannot be verified in CI. Per CLAUDE.md §2, a backlog item must be filed before the PR opens.

**Scope**
- Configure `GEMINI_API_KEY` in staging environment (Render backend env vars)
- Configure `REACT_APP_GEMINI_API_KEY` in staging frontend (Render Static Site env vars)
- Test: create or open a trade plan in edit mode on staging
- Verify "Improve with AI" button appears and calls the endpoint
- Verify thesis text is generated and populates the textarea
- Record sign-off date in `qa_evidence_EPIC-03.md` DoQ block

**Acceptance Criteria**
- AC-01: `POST /trade-plans/{plan_id}/generate-thesis` returns thesis text when GEMINI_API_KEY is set on staging
- AC-02: "Improve with AI" button visible on TradePlan edit page when REACT_APP_GEMINI_API_KEY set
- AC-03: Button click generates thesis and populates setup_thesis textarea
- AC-04: Sign-off date recorded in qa_evidence_EPIC-03.md

---

### BLG-QA-30 — Staging verification: ST-05 ticker validation live Yahoo Finance rejection path
**Priority:** P2 (Medium)
**Type:** QA / Staging Verification
**Owner:** Director of Quality; Head of Engineering
**Source:** v4.0 ST-05 EPIC-02 — staging-only AC per CLAUDE.md §2
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
ST-05 (BLG-BE-15) adds Yahoo Finance symbol validation to `POST /ticker-universe`. The AC "invalid ticker returns HTTP 422 with error message (not saved)" requires a live internet-connected staging environment with `SKIP_TICKER_VALIDATION` unset. This cannot be verified in CI (no live network calls permitted).

**Scope**
- Remove (or unset) `SKIP_TICKER_VALIDATION` on staging environment
- POST an invalid ticker symbol (e.g. `ZZZINVALID`) to `POST /ticker-universe` on staging
- Confirm: HTTP 422 returned with `detail` containing "not found or not tradeable"
- Confirm: ticker does NOT appear in subsequent `GET /ticker-universe` response
- POST a valid ticker (e.g. `AAPL`) and confirm: HTTP 201, ticker added successfully
- Record staging sign-off date in this item and notify Director of Quality

**Acceptance Criteria**
- AC-01: Invalid ticker → HTTP 422, detail message present, ticker not saved (staging)
- AC-02: Valid ticker → HTTP 201, ticker present in GET /ticker-universe (staging)
- AC-03: Timeout scenario documented (if testable — can mock by blocking yfinance)

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add new v2.8/v2.9/v3.0/v3.4/v3.9 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 (3 endpoints); v3.0 post-ship closure 2026-04-28 OA-v30-01 (5 additional endpoints); v3.1 post-ship closure 2026-05-05 (10 additional endpoints); v3.4 post-ship closure 2026-05-14 (2 additional endpoints); v3.5 post-ship closure 2026-05-15 (2 additional endpoints); v3.9 post-ship closure 2026-05-22 (1 additional endpoint: GET /portfolio/red-flag-journal)
**Effort:** M (~2 days — 23 endpoints total)
**Provisional-Target:** Before next performance baseline review

**Problem**
Twenty-two endpoints shipped in v2.8/v2.9/v3.0/v3.1/v3.4/v3.5 are absent from `docs/ops/api_performance_baseline.md`. Performance re-runs require a live environment and human coordination — baseline updates cannot be automated.

**Scope (updated 2026-05-15):**
- v2.8/v2.9 endpoints (3): `POST /ai/journal-summary`, `GET /ai/journal-summary/history`, `GET /v1beta1/news`
- v3.0 endpoints (5): `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}`, `GET /screener/results`, `POST /screener/run`
- v3.1 endpoints (10): `POST /trade-plans`, `GET /trade-plans/{id}`, `PUT /trade-plans/{id}`, `DELETE /trade-plans/{id}`, `GET /trade-plans/by-position/{position_id}`, `GET /trade-plans/by-ticker/{ticker}`, `GET /research/{ticker}`, `GET /earnings/{ticker}`, `GET /reports/monthly-pnl`, plus any additional v3.1 routes
- v3.4 endpoints (2): `GET /portfolio/drawdown-status`, `GET /portfolio/concentration-status`
- v3.5 endpoints (2): `GET /portfolio/paper-positions`, `GET /trades/{trade_id}/plan-vs-reality`
- v3.9 endpoints (1): `GET /portfolio/red-flag-journal`
- Run each against staging to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- All 23 endpoints have p50 and p95 latency entries in the baseline document
- Entries consistent with existing baseline measurement methodology

---

---

### BLG-OPS-17 — Alpaca API cost monitoring
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days (sufficient history to establish a meaningful cost baseline).

**Problem**
Alpaca API call volume (paper-positions, orders, account data) is not tracked. After 60 days of screener and research operations, a cost-per-run baseline can be established. Without a baseline, it is impossible to detect cost regressions when new features or higher screener frequency are introduced.

**Scope**
- Instrument Alpaca API call count per endpoint per day
- Log to `api_cost_log` or equivalent structured log
- Daily/weekly aggregate report

**Acceptance Criteria**
- Alpaca API call count logged per endpoint per run
- Aggregate report computable
- Gate condition verified by Infrastructure & Operations Owner before sprint planning

---

### BLG-OPS-18 — Data pipeline cost baseline
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-17 complete (Alpaca cost monitoring instrumented).

**Problem**
No aggregate data pipeline cost baseline exists covering Alpaca, Yahoo Finance, and news API calls together. Once Alpaca is instrumented (BLG-OPS-17), a combined baseline across all external data dependencies can be produced. Without this, cost anomalies across the pipeline are invisible.

**Scope**
- Aggregate cost baseline: Alpaca + YF + news API per week
- Baseline document filed in `docs/ops/`
- Alert threshold definition: >2× baseline triggers advisory

**Acceptance Criteria**
- Combined pipeline cost baseline document produced
- Alert threshold defined
- Gate condition (BLG-OPS-17 complete) verified before sprint planning

---

### BLG-OPS-19 — External API cost attribution per feature
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-17 complete (Alpaca cost monitoring instrumented).

**Problem**
External API calls are not attributed to the feature or workflow that triggered them. After BLG-OPS-17 instruments Alpaca, the next step is attributing each API call to the triggering feature (screener run, research view load, trade plan creation). This enables per-feature cost analysis and informs future optimisation decisions.

**Scope**
- Call attribution: tag each outbound API call with the triggering endpoint/feature
- Attribution report: cost breakdown by feature
- Identify top 3 cost contributors

**Acceptance Criteria**
- Each external API call tagged with triggering feature
- Attribution report computable
- Gate condition (BLG-OPS-17 complete) verified before sprint planning

---

### BLG-OPS-20 — Research endpoint cost monitoring
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-04 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-02 (Research View) live ≥ 30 days.

**Problem**
Research view loads trigger multiple downstream API calls (Yahoo Finance OHLCV, earnings, news). The per-session API cost of the research endpoint is not tracked. After 30 days of research view usage, a cost-per-session baseline can be established and anomalies detected.

**Scope**
- Instrument research endpoint: log external API calls triggered per request
- Cost-per-session aggregate (weekly baseline)
- Anomaly detection: sessions with >2× baseline API call count

**Acceptance Criteria**
- Research endpoint API call count logged per session
- Weekly baseline computable
- Gate condition verified by Infrastructure & Operations Owner before sprint planning

---

### BLG-OPS-21 — Arc 2 compute cost review
**Priority:** P3 (Low)
**Type:** Operations / Cost Review
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-05 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped AND 30-day cost baseline exists (BLG-OPS-17 or BLG-OPS-18 complete).

**Problem**
Arc 2 adds screener batch processing, research endpoints, and AI-assisted trade plan features. No compute cost review has been conducted since Arc 1. Once Arc 2 is complete and a 30-day cost baseline is available, a targeted review of Arc 2 compute overhead (CPU, memory, external API cost) should be conducted to inform Arc 3 infrastructure decisions.

**Scope**
- Review compute cost across Arc 2 features against Arc 1 baseline
- Identify top 3 cost drivers
- Produce recommendations for Arc 3 infrastructure planning

**Acceptance Criteria**
- Arc 2 vs Arc 1 compute cost comparison produced
- Recommendations filed
- Gate condition verified before sprint planning

---

### BLG-OPS-22 — Research data caching layer
**Priority:** P3 (Low)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner; Head of Backend Engineering
**Source:** IDEA-ops-20260421-06 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-13 (performance baseline) complete AND p95 research endpoint latency exceeds 3s threshold.

**Problem**
Research view loads require multiple sequential external API calls (YF OHLCV, earnings, news). If p95 latency (measured via BLG-OPS-13) exceeds 3 seconds, a caching layer (TTL-based, per-ticker) would materially reduce latency and external API call volume. Gate ensures implementation effort is only incurred if a real performance concern is observed.

**Scope**
- TTL-based cache (Redis or in-memory): research data per ticker, 15-minute TTL
- Cache invalidation on screener run
- Cache hit/miss logging

**Acceptance Criteria**
- Research view p95 latency reduced to ≤2s for cached tickers
- Cache hit rate ≥ 50% in typical usage
- Gate condition (BLG-OPS-13 + p95 concern) verified before sprint planning

---

### BLG-OPS-23 — Screener performance benchmark
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-07 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-13 (performance baseline) complete.

**Problem**
Screener batch runs involve 500+ ticker OHLCV fetches. No formal latency benchmark exists for screener run duration (p50/p95 end-to-end). BLG-OPS-13 establishes the API endpoint baseline; this item extends that to the full screener batch run. Without a benchmark, regressions introduced by new screener features (e.g., quality scoring) cannot be detected.

**Scope**
- Benchmark: full screener run duration (p50/p95) against full ticker universe
- Filed in `docs/ops/api_performance_baseline.md`
- Regression alert threshold: >1.5× baseline duration

**Acceptance Criteria**
- Screener run p50/p95 benchmark measured and filed
- Regression threshold defined
- Gate condition (BLG-OPS-13 complete) verified before sprint planning

---

### BLG-OPS-24 — Research endpoint performance benchmark
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-08 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-13 (performance baseline) complete AND research endpoint shows regression risk (p95 latency trending up over 30d).

**Problem**
BLG-OPS-13 adds research endpoints to the API performance baseline, but ongoing p95 trending is not monitored. If the research endpoint p95 latency trends upward over 30 days (indicating regression from data volume growth or upstream API changes), a targeted benchmark re-run and root cause investigation is warranted.

**Scope**
- Monthly p95 latency tracking for research endpoint
- Trend report: 30d rolling p95 chart
- Root cause investigation trigger at >1.5× baseline

**Acceptance Criteria**
- Monthly p95 tracking implemented
- Trend report computable
- Gate condition (BLG-OPS-13 + regression trend) verified before sprint planning

---

### BLG-OPS-25 — Automated staging smoke test on CI/CD deploy
**Priority:** P2 (Medium)
**Type:** Operations / CI/CD
**Owner:** Director of Quality; Infrastructure & Operations Owner
**Source:** IDEA-director-of-quality-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-27 (automated staging re-deployment on main merge) complete.

**Problem**
Every delivery verification run begins with manual staging health checks. An automated smoke test triggered by CI/CD on each staging deployment would catch deployment regressions (broken environment, missing env vars, cold-start failures) before the delivery verification engine starts, reducing lag and false-positive manual effort.

**Scope**
- Smoke test suite: 3–5 critical endpoint health checks (backend health, screener availability, positions endpoint)
- Triggered automatically after staging deploy (requires BLG-OPS-27 deploy hook)
- Failure: deploy pipeline reports failure; delivery verification engine advised
- Output: smoke test pass/fail result stored in CI artefacts

**Acceptance Criteria**
- Smoke test suite authored and triggered on staging deploy
- Suite covers minimum 3 critical endpoints
- Failure prevents "staging ready" signal from being issued
- Gate condition (BLG-OPS-27 complete) verified before sprint planning

---

### BLG-OPS-26 — Gemini API cost tracking
**Priority:** P2 (Medium)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Problem**
BLG-FEAT-24 (AI thesis generation, shipped v3.8) uses the Gemini API in production with no cost monitoring. The Gemini free tier is not unlimited; tracking monthly call volume and projected costs provides early warning of approaching tier boundaries before unexpected billing occurs.

**Scope**
- Instrument Gemini API call count per day/week (count of `generate_content` requests)
- Log call count to structured log or ops metrics table
- Monthly aggregate report: call count, projected monthly total, tier proximity
- Alert threshold: > 80% of free-tier monthly limit

**Acceptance Criteria**
- Gemini API call count logged per request
- Monthly aggregate computable
- Alert threshold defined and documented
- No change to BLG-FEAT-24 user-facing behaviour

---

### BLG-OPS-27 — Automated staging re-deployment on main merge
**Priority:** P2 (Medium)
**Type:** Operations / CI/CD
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** v4.0

**Problem**
Staging environment is currently manually re-synced after each main branch merge. This introduces risk of forgotten staging updates and adds lag to delivery verification runs. Automating the staging re-deployment trigger on main merges removes the manual step and ensures staging is always current.

**Scope**
- Configure Render staging auto-deploy trigger on main branch push
- Scope: trigger only when backend or frontend source files change (not on docs/governance-only commits) to conserve free-tier build minutes
- Confirm free-tier build minute impact is acceptable
- Coordinate with BLG-OPS-25 (smoke test) which depends on this deploy hook

**Acceptance Criteria**
- Staging auto-deploys on main merge for code changes
- Documentation-only commits do not trigger a deploy
- Free-tier build minute impact assessed and documented
- BLG-OPS-25 dependency satisfied (deploy hook available for smoke test integration)

---

### BLG-OPS-28 — Staging deploy live verification (ST-09 staging-only AC)
**Priority:** P2 (Medium)
**Type:** Operations / CI/CD
**Owner:** Infrastructure & Operations Owner
**Source:** ST-09 staging-only AC — v4.0 sprint execution 2026-05-24
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
ST-09 (BLG-OPS-27) implements the staging deploy workflow and deploy hook mechanism, but the AC "staging auto-deploys on main merge" requires a live Render environment with `RENDER_STAGING_DEPLOY_HOOK` secret configured. This cannot be verified in CI.

**Scope**
- Set `RENDER_STAGING_DEPLOY_HOOK` secret in GitHub repo settings (Render dashboard → staging service → Settings → Deploy Hook)
- Merge a code-change commit to main and confirm Render dashboard shows a triggered deploy
- Merge a docs-only commit and confirm no deploy is triggered
- Record staging sign-off date in BLG-OPS-27 post-verification note

**Acceptance Criteria**
- `RENDER_STAGING_DEPLOY_HOOK` secret configured
- Code-change merge triggers Render staging deploy (confirmed in Render dashboard)
- Docs-only commit does not trigger deploy (path filter verified)
- Results recorded as staging sign-off evidence

---

*BLG-OPS-14 (AI Journal monitoring metrics) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*
*BLG-OPS-12 (External API health check extension) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-OPS-15 (Research endpoint latency monitoring) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-OPS-16 (Remove tracked backend/__pycache__ files from git + .gitignore) — ✅ COMPLETE v3.7 — ST-10, cycle: 2026-05-18__release-v3.7*

---

*BLG-SEC-06 (Trade plan data sensitivity classification) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SEC-05 (Alpaca API key rotation policy and credential audit) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

## 7. Spec Debt Backlog

*BLG-SPEC-20 deferred to §9 (DL-023, 2026-04-24).*

---

*BLG-SPEC-24 (PT-02 research view canonical spec) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SPEC-25 (PT-02 research endpoint API contract) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SPEC-26 (Research view data source provenance spec) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-SPEC-27 (Research endpoint HTTP error code differentiation) — ✅ COMPLETE v3.6 — archived to backlog_archive.md 2026-05-17*

---

*BLG-SPEC-28 (Update trade_plan.md §6.2 entry checklist field references) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

*BLG-SPEC-29 (Correct grace-period-alert ux_spec.md §5 dismiss storage to sessionStorage) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-SPEC-30 (Correct stop-management-workflow ux_spec.md §4.4 stop-update HTTP verb to PATCH) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-SPEC-31 (Review React Query v5 onSuccess migration impact across codebase) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

### BLG-SPEC-32 — External API integration spec template
**Priority:** P3 (Low)
**Type:** Spec Debt / Governance
**Owner:** Head of Specs Team
**Source:** IDEA-spec-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 2 external API integration contracts exist (second contract after Alpaca and Yahoo Finance).

**Problem**
Alpaca and Yahoo Finance are currently the only external API integrations, each with ad hoc contract documentation. If a second external API integration is scoped (e.g., a data vendor, broker alternative), a standardised spec template would reduce documentation inconsistency and ensure all new integrations capture: authentication model, rate limits, error taxonomy, cost attribution, and data model mapping. Gate ensures the overhead of a template is justified by reuse demand.

**Scope**
- Template document: `docs/specs/api_contracts/_external_api_template.md`
- Required sections: authentication, rate limits, error taxonomy, cost attribution, data model mapping, retry policy
- Retroactively apply template to Alpaca and YF contracts if conformant

**Acceptance Criteria**
- Template document produced and filed
- At minimum, the triggering (second) external API contract conforms to the template
- Gate condition verified by Head of Specs Team before sprint planning

---

### BLG-SPEC-33 — SI-03 Red Flag Journal API contract document
**Priority:** P1 (High)
**Type:** Spec Debt
**Owner:** API Contracts Documentation Owner
**Source:** IDEA-api-contracts-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Problem**
`GET /portfolio/red-flag-journal` shipped v3.9 (SI-03) without a formal API contract document in `docs/specs/api_contracts/`. SI-04 and SI-05 will extend or reference the Red Flag Journal endpoint; without a contract, downstream implementations lack an authoritative spec for filter parameters, pagination schema, response structure, and error codes.

**Scope**
- Author `docs/specs/api_contracts/red_flag_journal.md`
- Document: endpoint URL, HTTP method, authentication requirement, query parameters (date range, event type, severity when BLG-BE-16 ships), pagination schema, response fields, error codes
- Register in `docs/reference/openapi.yaml` per CLAUDE.md §2
- Use `## METHOD /path` heading format per CLAUDE.md §2

**Acceptance Criteria**
- API contract document produced and filed
- Contract registered in openapi.yaml with correct heading format
- All filter parameters and response fields documented
- Reviewed by Head of Specs Team and API Contracts Documentation Owner

---

### BLG-SPEC-34 — SI-01 Pre-Entry Validation API contract document
**Priority:** P1 (High)
**Type:** Spec Debt
**Owner:** API Contracts Documentation Owner
**Source:** IDEA-api-contracts-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Problem**
`GET /portfolio/pre-entry-validation` shipped v3.8 (SI-01) without a formal API contract document. SI-02 and SI-05 will reference the validation rule taxonomy and response schema; without a contract, there is no authoritative source for rule enumeration, response structure, or override acknowledgement path.

**Scope**
- Author `docs/specs/api_contracts/pre_entry_validation.md`
- Document: endpoint URL, HTTP method, query parameters, response fields (per-rule pass/fail, override_required), override acknowledgement path, error codes
- Enumerate all 5 validation rules per strategy_rules.md v1.4 §4.2
- Register in `docs/reference/openapi.yaml`

**Acceptance Criteria**
- API contract document produced and filed
- All 5 validation rules documented with pass/fail conditions
- Override acknowledgement path specified
- Contract registered in openapi.yaml
- Reviewed by Head of Specs Team

---

### BLG-SPEC-35 — PO-02 §13 boundary review for AI cross-journal analysis
**Priority:** P1 (High)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning imminent.

**Problem**
PO-02 (Journal Pattern Recognition) will use AI to analyse cross-journal entries for recurring themes, emotional patterns, and setup types. This is an AI-assisted analysis of trading behaviour — the §13 boundary review must confirm this constitutes display/insight only and does not constitute signal generation or automated advisory. §13 PASS is required before PO-02 sprint planning seals.

**Scope**
- Run §13 checklist against PO-02 story set before sprint planning seals
- Confirm AI analysis output is: display-only, human-reviewed, no automated position recommendations
- Document binding conditions (if any) analogous to IT-06 §13 PASS conditions
- Sign-off recorded in sprint planning artefact

**Acceptance Criteria**
- §13 review completed; PASS or FAIL determination documented
- Binding conditions (if any) recorded
- Gate condition verified before PO-02 sprint planning seals

---

### BLG-SPEC-36 — PO-02 AI output audit schema
**Priority:** P2 (Medium)
**Type:** Spec / Governance
**Owner:** AI Compliance & Governance Officer; Head of Specs Team
**Source:** IDEA-ai-compliance-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning imminent.

**Problem**
PO-02 will generate AI output (pattern summaries, theme classifications) using an LLM. Governance policy requires AI-generated content to be traceable to model version, prompt version, and input at time of generation. Designing the audit log schema before sprint planning ensures it is built in from day 1, avoiding retroactive compliance debt.

**Scope**
- Design audit log schema: pattern_id, model_version, prompt_version, journal_ids_included, output_hash, generated_at
- Storage mechanism: append-only table or structured log file
- Retention policy: minimum 90 days
- Schema reviewed by AI Compliance & Governance Officer and Head of Specs Team

**Acceptance Criteria**
- Audit log schema designed and documented
- Storage mechanism defined
- Retention policy specified
- Gate condition verified before sprint planning

---

### BLG-SPEC-37 — SI-02 data schema pre-definition
**Priority:** P1 (High)
**Type:** Spec / Data Model Pre-work
**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Source:** IDEA-data-model-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 (Behavioural Drift Detection) sprint planning imminent.

**Problem**
SI-02 (Behavioural Drift Detection) requires per-trade data fields (regime_at_entry, setup_type, signal_conditions) that may not be fully captured in the current trade/position data model. Discovering these gaps mid-sprint would require emergency schema migrations. Pre-defining the required data structures before sprint planning allows the sprint to include any necessary migration stories proactively.

**Scope**
- Identify all data fields required for SI-02 drift analysis
- Compare against current trade, position, and trade plan schemas
- Gap analysis: enumerate missing fields with migration complexity estimate
- Produce data schema pre-definition document: required fields, data types, tables affected, migration approach
- Input to SI-02 sprint planning and BLG-BE-17 (drift query pre-design)

**Acceptance Criteria**
- Schema pre-definition document produced
- Gap analysis complete: missing fields identified or confirmed absent
- Migration approach defined for any missing fields
- Document reviewed by Data Model Owner and Head of Specs Team before sprint planning

---

## 8. Governance Backlog

*BLG-GOV-23 (scored_initiatives.md Arc 3–6 comprehensive refresh — OA-RP-05 resolved) — ✅ COMPLETE v3.7 — ST-11, cycle: 2026-05-18__release-v3.7*

---

*BLG-GOV-24 (Add gh_issue_template.md to §14 governance table) — ✅ COMPLETE v3.8 — ST-10, cycle: 2026-05-19__release-v3.8 — archived to backlog_archive.md 2026-05-21*

---

*BLG-GOV-19 (PT-05 entry checklist §13 compliance review) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-GOV-20 (Trade plan field extension governance) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

*BLG-GOV-21 (Arc 4 data requirements capture) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-GOV-22 (sprint_planning_prompt.md patch: shared execution_state.json ownership + multi-EPIC Positions.js conflict guidance) — ✅ COMPLETE v3.5 — archived to backlog_archive.md 2026-05-15*

---

*BLG-GOV-18 (External API dependency risk register) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

*BLG-GOV-11 (Cycle artefact inventory and maintenance review) — ✅ COMPLETE v3.2 — archived to backlog_archive.md 2026-05-09*

---

*BLG-GOV-25 (Add --dry-run support to plan release and run delivery verification engines) — ✅ COMPLETE v3.9 — ST-11, cycle: 2026-05-21__release-v3.9*

---

### BLG-GOV-26 — Arc velocity tracking dashboard
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead
**Source:** IDEA-governance-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped — Arc 2 velocity history complete.

**Problem**
No arc-level velocity tracking exists. Cycle velocity is tracked per-cycle (cycle_velocity in run_manifest.md), but no aggregate view shows velocity trends across an entire arc. Once Arc 2 is complete (PT-04 shipped), an Arc 2 velocity retrospective would establish baseline expectations for Arc 3 planning.

**Scope**
- Arc velocity report: stories/cycle, epic completion rate, arc-level rolling velocity
- Filed in governance reporting; updated at arc close
- Input to release planning engine for arc-boundary cycles

**Acceptance Criteria**
- Arc 2 velocity report produced at arc close
- Report format reusable for Arc 3+
- Gate condition verified by PMO Lead before sprint planning

---

### BLG-GOV-27 — Cross-arc dependency map
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-governance-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 3 arcs running concurrently (Arc 3, Arc 4, Arc 5 or later all in active/planned state simultaneously).

**Problem**
Current arcs (Arc 2, Arc 3, Arc 4) have informal dependency tracking (noted in roadmap annotations). If 3 or more arcs are in concurrent active or planned state, cross-arc dependency conflicts become a risk: feature data dependencies, shared backend schema changes, and governance sequencing conflicts all require explicit mapping. Gate ensures effort is only incurred when the complexity warrants it.

**Scope**
- Cross-arc dependency map: for each arc, list upstream arcs (data dependencies) and downstream arcs (consumes output)
- Conflict detection: identify stories across arcs that modify shared resources
- Filed in `claude/strategy/`

**Acceptance Criteria**
- Cross-arc dependency map produced
- Conflicts (if any) documented and escalation plan filed
- Gate condition (≥3 concurrent arcs) verified by PMO Lead before sprint planning

---

### BLG-GOV-28 — PT-04 §13 compliance review
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** IDEA-governance-20260421-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~0.5 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 sprint planning imminent (sprint planning seals within the next cycle).

**Problem**
PT-04 (Setup Quality Score) involves a new backend scoring algorithm and a new API endpoint. §13 compliance review (execution_prompt.md §13 — pre-sprint implementation review checklist) must be completed before PT-04 sprint planning seals, per CLAUDE.md §13 gate rules. This item tracks the gate-conditional §13 review so it is not missed when PT-04 is next scheduled.

**Scope**
- Run §13 checklist against PT-04 story set before sprint planning seals
- Flag any compliance gaps to Head of Specs Team and Product Owner
- Sign-off recorded in sprint planning artefact

**Acceptance Criteria**
- §13 review completed and sign-off recorded
- Gate condition (PT-04 sprint planning imminent) verified before initiating review

---

### BLG-GOV-29 — Trade plan AI summary audit log
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; QA Lead
**Source:** IDEA-governance-20260421-04 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** AI trade plan analysis feature scoped and scheduled (i.e., a story exists in the backlog that adds AI-generated trade plan summaries or analysis).

**Problem**
If an AI-assisted trade plan analysis feature is scoped (generating text summaries, recommendations, or signals using an LLM), an audit log is required per governance policy (AI-generated content must be traceable to the model version, prompt version, and input at time of generation). Without a pre-designed audit log schema, retrofitting this after feature delivery creates governance debt.

**Scope**
- Audit log schema: plan_id, model_version, prompt_version, input_hash, output_hash, generated_at
- Storage: append-only table or log file
- Retention policy: minimum 90 days

**Acceptance Criteria**
- Audit log schema designed and documented
- Storage mechanism implemented
- Gate condition (AI trade plan analysis feature scoped) verified by Head of Specs Team before sprint planning

---

### BLG-GOV-30 — Sprint planning staging-only AC designation flag
**Priority:** P1 (High)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before v4.0 sprint planning

**Problem**
v3.9 post-ship closure carry-forward advisory item #2: environment-dependent ACs (those referencing Yahoo Finance, Alpaca, or other live service behaviour) were not designated "staging-only" at sprint planning. This resulted in BLG-QA-24 being filed as a surprise P3 notation at QA sign-off. A per-story staging_only_evidence flag at sprint planning time prevents this pattern.

**Scope**
- Add `staging_only_evidence` notation to sprint_backlog.md story schema documentation
- Update sprint_planning_prompt.md to prompt for staging-only designation when an AC references external live service behaviour
- Applies CLAUDE.md §6 governance file edit checklist (version bump, OPERATIONAL_GUIDE.md update, prompt_change_log.md entry)

**Acceptance Criteria**
- sprint_planning_prompt.md updated with explicit staging-only AC designation prompt
- sprint_backlog.md story format updated to include staging_only_evidence field documentation
- prompt_change_log.md entry appended per §6 checklist
- Head of Specs Team sign-off recorded

---

### BLG-GOV-31 — Merge gate re-invocation advisory in sprint capacity template
**Priority:** P1 (High)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** XS (~0.5 day)
**Provisional-Target:** Before v4.0 sprint planning

**Problem**
v3.9 post-ship closure carry-forward advisory item #1: merge_gate.epics_merged was not updated during out-of-band GitHub merges, causing stale state when the execution engine resumed. The fix is documenting in the sprint capacity template that the execution engine must be re-invoked after each EPIC GitHub merge.

**Scope**
- Add advisory note to sprint capacity template: "After each EPIC PR merge to main, re-invoke the execution engine to update merge_gate.epics_merged before proceeding to the next EPIC"
- Applies CLAUDE.md §6 governance file edit checklist if sprint_capacity_template.md is a governed file

**Acceptance Criteria**
- Sprint capacity template updated with re-invocation advisory
- Head of Specs Team sign-off recorded

---

### BLG-GOV-32 — Gate-condition clearing tracker at release planning
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled

**Problem**
Gate-conditional backlog items (e.g., BLG-GOV-39, BLG-SPEC-35) have gates that may clear at unpredictable times. Currently gates are checked reactively (if PO remembers at release planning). A structured gate-scan checklist at each release planning kickoff — listing items likely to clear in the next 30–60 days — provides proactive pipeline visibility for sprint sequencing.

**Scope**
- Add a gate-scan checklist step to the release planning prompt or release planning artefact
- At each release planning kickoff: scan all gate-conditional backlog items; flag gates likely to clear within 30–60 days given current trajectory
- Output: gate proximity table in the release plan artefact

**Acceptance Criteria**
- Release planning process includes a gate-scan step
- Gate proximity table produced at each release planning run
- Applies CLAUDE.md §6 checklist if release_planning_prompt.md is modified

---

### BLG-GOV-33 — PT-04 closed trade count audit
**Priority:** P2 (Medium)
**Type:** Governance / Product Audit
**Owner:** Product Owner; Challenger
**Source:** IDEA-challenger-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.0 release planning

**Problem**
PT-04 (Setup Quality Score) gate (20+ closed trades) has been unmet for 4 consecutive cycles (v3.6–v3.9). No verification of the actual production closed trade count has been documented in any cycle artefact. If the count is 15–19, PT-04 is near-clearing and should be planned proactively. If under 10, the gate condition calibration may warrant review.

**Scope**
- Query production database for current closed trade count
- Document count in release planning artefact (v4.0) and in PT-04 backlog item
- If count ≥ 20: advance PT-04 to v4.0 sprint planning
- If count 15–19: note in v4.0 release plan as near-gate item with projected clearing date
- If count < 10: consider gate revision at v4.0 release planning

**Acceptance Criteria**
- Closed trade count documented in v4.0 release planning artefact
- PT-04 gate status updated based on count
- PO decision recorded for any gate revision

---

### BLG-GOV-34 — Arc 4 data density risk trajectory assessment
**Priority:** P2 (Medium)
**Type:** Governance / Risk Assessment
**Owner:** Product Owner; Challenger
**Source:** IDEA-challenger-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v4.0 release planning

**Problem**
PO-02 (Journal Pattern Recognition) requires 6+ months of AI journal entries. PO-04 (Reflection/Outcome Correlation) requires 50+ trades with plans. PO-05 (Lightweight Replay Mode) requires IT-06 foundation + significant trade history. At current trade frequency, these gates may not clear within v4.0–v4.2. Without a formal trajectory assessment, these features are perpetually "planned" without realistic delivery dates.

**Scope**
- Assessment: current trade frequency (trades/month), AI journal entry rate, trade plan creation rate
- Trajectory: projected dates for PO-02 gate (6+ months AI journals), PO-04 gate (50+ trades with plans), PO-04 gate (50+ closed trades)
- Recommendation: are gates realistic within 4 cycles, or should gate conditions be reconsidered?
- Output: trajectory assessment document; input to v4.0 release planning

**Acceptance Criteria**
- Trajectory assessment document produced at v4.0 release planning
- Gate clearing dates projected
- PO decision recorded: proceed on current trajectory, revise gates, or re-scope features

---

### BLG-GOV-35 — Gemini thesis generation audit trail
**Priority:** P2 (Medium)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Head of Backend Engineering
**Source:** IDEA-ai-compliance-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** v4.0

**Problem**
BLG-FEAT-24 (AI thesis generation, shipped v3.8) generates AI setup thesis text using Gemini API in production. No audit trail records the model version, prompt version, or output hash per generation. As Gemini usage scales, retroactive compliance tracking becomes impossible. An audit trail should be implemented before usage volume increases.

**Scope**
- Audit trail record per generation: plan_id, model_version, prompt_version, input_hash (thesis generation request), output_hash, generated_at, user_acknowledged (bool)
- Storage: append-only table (gemini_audit_log) or structured log file
- Retention policy: minimum 90 days
- No change to user-facing BLG-FEAT-24 behaviour

**Acceptance Criteria**
- Audit log created for each Gemini thesis generation call
- Record fields present: model_version, prompt_version, input_hash, output_hash, generated_at
- Retention policy enforced (90-day minimum)
- No performance impact on thesis generation response time

---

### BLG-GOV-36 — API key rotation cadence policy
**Priority:** P2 (Medium)
**Type:** Governance / Security Policy
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.0

**Problem**
Alpaca API keys (financial account access) and Gemini API keys have no defined rotation cadence. Without a formal policy specifying minimum rotation interval and documented responsibility, the exposure window for a compromised credential is unbounded.

**Scope**
- Define rotation cadence: Alpaca keys — minimum annual rotation; Gemini keys — minimum annual rotation
- Document rotation procedure: how to rotate without service disruption (environment variable update, staging + prod)
- Assign responsibility: Infrastructure & Operations Owner as rotation executor; Cybersecurity & Trust Lead as policy owner
- File policy document in `docs/ops/api_key_rotation_policy.md`

**Acceptance Criteria**
- Policy document produced covering Alpaca and Gemini key rotation
- Rotation cadence, procedure, and responsibility defined
- Next rotation date recorded (based on last known rotation date or "unknown — rotate on policy adoption")

---

### BLG-GOV-37 — Red flag endpoint authentication and PII review
**Priority:** P2 (Medium)
**Type:** Governance / Security Review
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.0

**Problem**
SI-03 Red Flag Journal endpoint (GET /portfolio/red-flag-journal, shipped v3.9) exposes trading strategy override events. A targeted review confirms: (1) the endpoint is protected by API key authentication (shipped v2.2), (2) response payloads do not expose PII or sensitive strategy parameters beyond event type and timestamp, (3) pagination does not leak adjacent users' data (single-user system, but confirm).

**Scope**
- Verify API key auth covers /portfolio/red-flag-journal
- Review response payload: confirm no PII, no sensitive position data, no information beyond event_type, rule_type, timestamp, severity
- Document findings in security review note filed in `docs/security/`

**Acceptance Criteria**
- Authentication confirmed (API key auth active on endpoint)
- Response payload reviewed: PII-free, no sensitive strategy data confirmed
- Review findings documented
- If gap found: remediation backlog item filed

---

### BLG-GOV-38 — DoQ sign-off date compliance audit (v3.7–v3.9)
**Priority:** P3 (Low)
**Type:** Governance / Quality Audit
**Owner:** QA Lead; Director of Quality
**Source:** IDEA-qa-lead-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled

**Problem**
PR template v1.2 (shipped v3.9, ST-12) now enforces DoQ sign-off date fields on all QA evidence. A one-time historical audit of v3.7–v3.9 QA evidence files confirms whether existing closed-cycle artefacts are compliant with the new standard or require retrospective annotation. Bounded scope (3 cycles); findings are advisory only for closed cycles.

**Scope**
- Review all QA evidence files from v3.7, v3.8, and v3.9 cycles for DoQ sign-off date presence
- Document any missing dates
- Findings filed as advisory annotation — no retroactive modification to sealed artefacts required
- If pattern found: inform Head of Specs Team for future sprint planning guidance

**Acceptance Criteria**
- All QA evidence files from v3.7–v3.9 reviewed
- Missing sign-off dates documented
- Findings filed; sealed artefacts not modified

---

### BLG-GOV-39 — SI-02 §13 formal boundary review
**Priority:** P1 (High)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 (Behavioural Drift Detection) sprint planning imminent.

**Problem**
SI-02 (Behavioural Drift Detection) involves rolling analysis comparing actual trade entries against stated setup criteria. Before sprint planning seals, formal §13 review must confirm: this is deterministic analysis of historical data, not a predictive signal; drift detection is display-only (shows patterns, does not recommend actions); the rolling window analysis is not an adaptive strategy parameter. Prevents last-minute sprint gate discovery.

**Scope**
- Run §13 checklist against SI-02 story set before sprint planning seals
- Confirm drift detection output is: deterministic, display-only, no automated recommendations
- Document binding conditions (e.g., "drift alerts are informational only; no automated position management")
- Sign-off recorded in sprint planning artefact

**Acceptance Criteria**
- §13 review completed; PASS or FAIL determination documented
- Binding conditions (if any) enumerated and recorded
- Gate condition (SI-02 sprint planning imminent) verified before initiating review

---

## 9. Deferred / Future Candidates

- Daily email portfolio summary
- FX rate history tracking
- **BLG-TECH-05 — Prometheus metrics endpoint** (P3, M effort — permanently deferred at single-user scale; DL-023 2026-04-24)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system
- **BLG-SPEC-20 — Machine-readable spec front-matter standard** (P3, S effort — deferred; Arc 1 specs shipped without requiring this standard; DL-023 2026-04-24)

---

## 10. Explicitly Out of Scope (Product-Level)

These are deliberate product decisions, not deferrals:

- Broker API integration
- Automated trading execution
- Configurable strategy builder
- ML-based predictions
- Social / community features
- Options and futures trading support

---

## 11. Lifecycle Governance Notes

- This backlog is not canonical and must never override: strategy rules, metrics definitions, API contracts

---

## Release Slice — v3.9 (cycle: 2026-05-21__release-v3.9)

<!-- release-plan-marker: RP:v3.9:2026-05-21__release-v3.9 -->

*This section is ephemeral. Remove during `groom backlog` after v3.9 post-ship closure.*

| EPIC | ST | Title | Source | Sprint |
|------|----|-------|--------|--------|
| EPIC-01 | ST-01 | Fix YF crumb/401 rate-limiting in screener batch | BLG-TECH-10 | Sprint 1 |
| EPIC-01 | ST-02 | Fix sector/industry data dropped in screener batch | BLG-BE-10 | Sprint 1 |
| EPIC-01 | ST-03 | Remove invalid DAY ticker / investigate PHNX.L | BLG-BE-11 | Sprint 1 |
| EPIC-01 | ST-04 | Add degraded-run warning banner to screener results | BLG-FE-38 | Sprint 1 |
| EPIC-02 | ST-05 | Strip .L suffix from Ticker Universe display labels | BLG-FE-37 | Sprint 1 |
| EPIC-02 | ST-06 | Add company_name to ticker universe + management page | BLG-BE-12 | Sprint 1 |
| EPIC-03 | ST-07 | Red Flag Journal — data model and backend | SI-03 | Sprint 2 |
| EPIC-03 | ST-08 | Red Flag Journal — frontend display | SI-03 | Sprint 2 |
| EPIC-04 | ST-09 | execution_prompt.md patches (test_scenarios + createPageUrl) | CF-2, CF-4 | Sprint 2 |
| EPIC-04 | ST-10 | sprint_planning_prompt.md patch (planning-deferred) | CF-5 | Sprint 2 |
| EPIC-04 | ST-11 | BLG-GOV-25 dry-run for plan release + delivery verification | BLG-GOV-25 | Sprint 2 |
| EPIC-04 | ST-12 | QA evidence pre-merge enforcement — PR template | CF-3 (DoQ) | Sprint 2 |
| EPIC-05 (cond.) | ST-13 | PT-04 Setup Quality Score — backend (conditional) | BLG-FEAT-25 | Sprint 2 |
| EPIC-05 (cond.) | ST-14 | PT-04 Setup Quality Score — frontend (conditional) | BLG-FEAT-25 | Sprint 2 |

---

## Release Slice — v4.0 (cycle: 2026-05-22__release-v4.0)

<!-- release-plan-marker: RP:v4.0:2026-05-22__release-v4.0 -->

*This section is ephemeral. Remove during `groom backlog` after v4.0 post-ship closure.*

| EPIC | ST | Title | Source | Sprint |
|------|----|-------|--------|--------|
| EPIC-01 | ST-01 | SI-01 pass/fail rate by rule — backend metric endpoint | BLG-FEAT-36 | Sprint 1 |
| EPIC-01 | ST-02 | Red flag event frequency metric — backend + frontend | BLG-FEAT-37 | Sprint 1 |
| EPIC-01 | ST-03 | E2E Playwright test — SI-01→SI-03 integration path | BLG-QA-25 | Sprint 1 |
| EPIC-01 | ST-04 | Trade plan adherence rate metric — backend + frontend | BLG-FEAT-39 | Sprint 1 |
| EPIC-02 | ST-05 | Validate ticker symbol on add | BLG-BE-15 | Sprint 1 |
| EPIC-02 | ST-06 | Red flag endpoint auth and PII review | BLG-GOV-37 | Sprint 1 |
| EPIC-03 | ST-07 | Gemini audit trail — log AI thesis generation calls | BLG-GOV-35 | Sprint 2 |
| EPIC-03 | ST-08 | Gemini cost tracking — token usage and cost per call | BLG-OPS-26 | Sprint 2 |
| EPIC-03 | ST-09 | CI/CD automated staging re-deploy on main merge | BLG-OPS-27 | Sprint 2 |
| EPIC-04 (cond.) | ST-10 | PT-04 Setup Quality Score — backend (conditional) | BLG-FEAT-25 | Sprint 2 |
| EPIC-04 (cond.) | ST-11 | PT-04 Setup Quality Score — frontend (conditional) | BLG-FEAT-25 | Sprint 2 |
| EPIC-03 | ST-12 | Gemini Flash base wiring | BLG-BE-19 | Sprint 2 | [ADDED AMD-20260523-01 — prerequisite for ST-07/ST-08] |
| EPIC-02 | ST-13 | Starlette security upgrade to ≥1.0.1 | CVE PYSEC-2026-161 | Sprint 1 | [ADDED AMD-20260523-01 — emergency security fix] |
<!-- amendment-marker: AMD:v4.0:2026-05-22__release-v4.0:AMD-20260523-01 -->

