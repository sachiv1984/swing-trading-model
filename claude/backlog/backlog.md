# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-06-26 (rebalance 2026-06-26__scheduled — DL-057; 25 new items added (IW-20260626-01): BLG-FE-80, BLG-QA-65–68, BLG-OPS-79–81, BLG-GOV-137–149, BLG-SPEC-58–61; 135 active items)
**Last rebalance:** 2026-06-26 (cycle 2026-06-26__scheduled — DL-057; 14 Promoted-Backlog, 10 Backlog-gate-conditional, 19 Parked C1, 6 Parked C3; STEP 8.0: BLG-BE-39 + BLG-FE-79 mandatory v6.3 Now; PVR=0.37 Advisory; Skill-Silo=51.5% Advisory)

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

---

## 2. Product Feature Backlog (User-Facing)

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

### BLG-FEAT-41 — Claude thesis adoption rate metric
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-analytics-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
The Claude thesis generation feature (shipped v4.0) writes to the setup_thesis field on trade plans. There is no metric tracking whether generated theses are accepted, edited, or discarded. Adoption rate is a useful early signal of feature value and cost-per-use justification.

**Scope**
- Define metric: thesis_adoption_rate = trade_plans_with_non-empty_setup_thesis_at_entry / trade_plans_with_thesis_generated
- Requires comparing claude_audit_log (thesis generated) against trade_plan final setup_thesis at position entry
- Document in metrics_definitions.md

**Acceptance Criteria**
- Metric defined in metrics_definitions.md
- Query approach documented (claude_audit_log join trade_plans)
- Reviewed by Financial Reporting & Records Owner and Product Owner

---

### BLG-FEAT-44 — Arc 5 compliance score utility advisory at low trade volume
**Priority:** P3 (Low)
**Type:** Product Feature / UX Advisory
**Owner:** Metrics Definitions & Analytics Owner; Head of UX & Design
**Source:** IDEA-metrics-analytics-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc5ComplianceSection live 3+ months post-v4.1 ship (~Aug 2026). Minimum usage period needed to assess whether low-volume score values are misinterpreted in practice.

**Problem**
The Arc 5 composite compliance score (shipped v4.1) is computed from fewer than 20 closed trades. At low sample volumes, the score may represent statistical noise rather than actionable signal. Without a "minimum data" advisory in the UI, users may over-interpret early values.

**Scope**
- Assess whether compliance scores at <20 trades are statistically meaningful
- If noise at low volume: add a "Minimum trade history required (< 20 trades)" advisory near the score display
- Gate condition verification by Metrics Definitions & Analytics Owner before sprint planning

**Acceptance Criteria**
- Assessment document produced (advisory or advisory-not-needed conclusion)
- If advisory warranted: UI advisory added to Arc5ComplianceSection for sub-20-trade states
- Gate condition verified before sprint planning

---

### BLG-FEAT-45 — Monthly P&L report format review — 3-month usage retrospective
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥ 2026-08-05 (3+ months since Monthly P&L shipped 2026-05-05)

**Problem**
Monthly P&L shipped 2026-05-05 with a fixed column/section layout. After 3 months of real usage, the format may benefit from minor adjustments (column order, section grouping, display precision). A lightweight retrospective assessment at 3 months is appropriate before any format changes are considered.

**Scope**
- Review current Monthly P&L format against 3+ months of usage experience
- Identify any column, section, or display precision improvements
- Produce a brief recommendations document; if no changes warranted, record "no change" decision
- Product Owner sign-off

**Acceptance Criteria**
- Format review conducted with 3+ months of data available
- Recommendations document produced (or "no change" decision recorded)
- Any format changes flow into the next appropriate sprint as separate stories
- Gate condition verified: ≥ 2026-08-05

---

### BLG-FEAT-52 — Trade tagging and tag-based performance filtering
**Priority:** P3 (Low)
**Type:** Product Feature / User Value
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260619-02 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** L (~1 week)
**Provisional-Target:** [TBD — gate-conditional]
**Gate:** Arc 4 PO-02 (Journal Pattern Recognition) sprint planning imminent — tag data model provides complementary structure for cross-trade pattern analysis

**Problem**
Trades are currently classified only by market, sector, and signal type. There is no mechanism for a user to apply free-form tags (e.g. "earnings catalyst", "gap-and-go", "sector rotation") and subsequently filter performance analytics by those tags. Tag-based filtering would allow comparison of win rate and average R across user-defined trade categories.

**Scope**
- Data model: `trade_tags` table (trade_id, tag_name, created_at); many-to-many relationship
- API: POST/DELETE /trades/{id}/tags; GET /analytics/tag-performance (win rate, avg R, count by tag)
- Frontend: tag input on Trade Plan form; tag filter on PerformanceAnalytics page

**Acceptance Criteria**
- AC-01: User can add/remove tags on any trade plan
- AC-02: GET /analytics/tag-performance returns win rate and average R broken down by tag
- AC-03: PerformanceAnalytics page surfaces tag-based filter controls

---

### BLG-FEAT-53 — Strategy Benchmark page: compare live trades against backtest
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Product Owner
**Source:** Product Owner decision 2026-06-26 — session design proposal (Head of UX & Design)
**Effort:** L (~1 week)
**Provisional-Target:** v6.3

**Problem**
There is no way to know whether live trading is tracking the production strategy's backtest performance. The backtest (`production_strategy.py`) generates trade-level and annual performance data in CSV files, but these are not connected to the live system. Without a comparison view, there is no way to answer: "Am I trading this strategy?", "Is it still producing the outcomes the backtest predicted?", or "How does my actual win rate compare to the 56.7% backtest baseline?"

**Design**
UX specification: Head of UX & Design design proposal 2026-06-26 — single scrollable page with sticky year + market filters, three panels:
- Panel 1 — Performance Parity: backtest vs actual side-by-side stat cards (CAGR, Win Rate, Avg Hold Days, Total PnL) + yearly PnL bar chart
- Panel 2 — Yearly Breakdown: year-by-year table (Num Trades, Win Rate %, Total PnL for both backtest and actual)
- Panel 3 — Trade Log: toggleable backtest / actual / side-by-side view, filterable by year and market; exit reason badges matching existing Positions/Signals badge language

**Scope**
- Two new DB tables: `backtest_trades` (Ticker, Entry Date, Exit Date, Holding Days, Entry, Exit, PnL, PnL %, Market, Exit Reason, Was Profitable, Entry Year) and `backtest_yearly_performance` (Entry Year, Num Trades, Avg PnL, Total PnL, Avg Hold Days, Win Rate %)
- Import mechanism: `POST /strategy/benchmark/import` endpoint accepts the three CSV outputs from `production_strategy.py` and upserts into DB; companion local script `import_backtest.py` reads latest CSVs from `production_results/` and posts to this endpoint. User runs this nightly (or on any schedule) from their local machine — no server-side execution of `production_strategy.py`
- Read endpoints: `GET /strategy/benchmark/summary?year=&market=` and `GET /strategy/benchmark/trades?year=&market=`
- Frontend: `StrategyBenchmark.js` page with all three panels, sticky filter bar, toggle modes; displays "Last updated: {date}" timestamp from DB (no Refresh button — data is managed externally)
- Route registered in app router; all endpoints registered in `backend/routers/test.py`

**Acceptance Criteria**
- AC-01: Strategy Benchmark page accessible from main navigation
- AC-02: Year filter (All / individual year) applies to all three panels simultaneously
- AC-03: Panel 1 shows backtest stats and actual stats side-by-side; actual shows `—` when no live trades exist for the selected period (not zero)
- AC-04: Panel 2 yearly breakdown table covers all years present in backtest data (2018–present)
- AC-05: Panel 3 trade log supports three toggle modes; exit reason badges use Stop (red) / Risk-Off (amber) / Rebalance (teal) consistent with existing badge language
- AC-06: `POST /strategy/benchmark/import` upserts data correctly; "Last updated" timestamp reflects the most recent import date
- AC-07: `import_backtest.py` script reads latest CSVs from `production_results/` and calls the import endpoint; runnable with `python import_backtest.py`
- AC-08: All new API endpoints documented in `docs/reference/openapi.yaml` and `docs/specs/api_contracts/` in the same sprint

---

## 3. Frontend & UX Backlog

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

### BLG-FE-45 — Arc5ComplianceSection layout expandability review
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend; Head of UX & Design
**Source:** IDEA-base44-frontend-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** v4.1 sprint planning complete — layout expandability review requires knowing which Arc 6 compliance data points will be added to the PerformanceAnalytics page.

**Problem**
Arc5ComplianceSection.js (shipped v4.0) displays 5 compliance metrics. Arc 6 will add performance science metrics to the same analytics surface. Without an expandability review, the component layout may require significant rework when additional data sections are added. A pre-sprint review ensures the component is structurally extensible.

**Scope**
- Review Arc5ComplianceSection layout for extensibility: grid, card count, responsive breakpoints
- Identify layout constraints that would prevent additional section additions
- Produce short design note with recommendations (retain, refactor, or modularise)

**Acceptance Criteria**
- Design note produced and reviewed by Product Owner
- Gate condition verified before sprint planning

---

### BLG-FE-46 — Claude thesis generation user feedback mechanism
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend; Head of UX & Design
**Source:** IDEA-base44-frontend-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Problem**
The Claude thesis generation button (shipped v4.0) produces a thesis and populates the setup_thesis field. There is no feedback mechanism: the user cannot signal whether the generated thesis was useful, edited heavily, or discarded. Without feedback, the system cannot track thesis quality or improve prompt engineering over time.

**Scope**
- Simple feedback UI on thesis generation: "Useful / Not useful" binary or a brief edit indicator
- Data stored in claude_audit_log or a lightweight feedback table
- Does not require a full feedback loop — MVP is a binary signal

**Acceptance Criteria**
- Feedback mechanism available after thesis generation
- Feedback data persisted (table or audit log field)
- UX reviewed by Head of UX & Design before sprint planning

---

### BLG-FE-54 — Arc 5 unified pre-entry gateway
**Priority:** P3 (Low)
**Type:** Frontend / UX Exploration
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260522-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 5 fully complete (SI-02, SI-04, SI-05 all shipped).

**Problem**
SI-01 (pre-entry validation panel) and PT-05 (entry checklist) are separate views requiring multi-view navigation before trade finalisation. A unified pre-entry gateway combining all required checks into a single screen could reduce friction and navigation complexity. Gate ensures design is informed by the complete Arc 5 feature set.

**Scope**
- Explore combining SI-01 and PT-05 into a single pre-entry gateway screen
- Map decision points and information needs for the combined flow
- Propose structural changes; not a committed sprint item until gate clears

**Acceptance Criteria**
- UX exploration document produced
- Combined flow mapped with clear decision points
- Gate condition (Arc 5 fully complete) verified before commencing

---

### BLG-FE-55 — Mobile responsiveness baseline assessment
**Priority:** P3 (Low)
**Type:** Frontend / UX Quality
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260522-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 5 fully complete (feature set stabilised — SI-02, SI-04, SI-05 all shipped).

**Problem**
No formal mobile responsiveness testing has been performed. The most frequently used views (positions, screener, trade plan form, Red Flag Journal) have been built for desktop-first usage. Assessing mobile responsiveness after Arc 5 closes the feature set provides a stable baseline before any mobile polish work.

**Scope**
- Identify most-used views from user behaviour observation
- Assess mobile responsiveness for each identified view
- Produce assessment report with severity-ranked findings

**Acceptance Criteria**
- Mobile responsiveness assessment report produced
- Views assessed: at minimum positions, screener, trade plan form, Red Flag Journal
- Gate condition verified before commencing

---

### BLG-FE-58 — Pre-entry panel: check grouping for Arc 5 expansion
**Priority:** P3 (Low)
**Type:** Frontend / UX Improvement
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** docs/product/ux/pre_entry_panel_ux_assessment.md — candidate P4 — cycle 2026-05-31__release-v4.7 (ST-09)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 or SI-04 sprint planning initiated (Arc 5 expansion imminent).

**Problem**
PreEntryValidationPanel currently displays 5 checks in a flat list. As SI-02 drift detection and SI-04 strategy version comparison add compliance context to the pre-entry flow, check count may grow to 8–10+ items. A flat list at that scale is dense and unscannable.

**Scope**
- Group checks into labelled sections: "Compliance" (Arc 5 checks), "Risk" (cash, sizing), "Technical" (regime, earnings)
- Section headers use small separator labels; no collapsible sub-groups required
- Prepare component structure for Arc 5 check additions before SI-02/SI-04 ship

**Acceptance Criteria**
- Checks grouped into at minimum 2 sections (Compliance and Risk/Technical)
- Grouping does not break existing override acknowledgement behaviour
- Gate condition (SI-02 or SI-04 sprint planning) verified before commencing

---

### BLG-FE-59 — Arc5ComplianceSection extension spec for SI-02/SI-04
**Priority:** P3 (Low)
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner; Base44 Frontend
**Source:** IDEA-frontend-ux-20260527-02 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; terminal Parked-cycle-2 disposition)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend + SI-04 sprint planning imminent (both Arc 5 features approaching their sprint entry).

**Problem**
Arc5ComplianceSection.js (shipped v4.0) displays 5 compliance metrics. SI-02 drift detection frontend and SI-04 strategy version comparison will each add new display cards to this section. Without extension point specifications defined in advance, each addition will require layout redesign rather than slotting into a prepared contract. Pre-specifying card layout contracts prevents rework.

**Scope**
- Update BLG-FE-48 spec (if exists) or author new: extension point specifications for SI-02 drift score card and SI-04 version comparison card
- Define card layout contract: minimum data fields, display states (loading, populated, gate-not-met), responsive breakpoints
- Ensure additions require no Arc5ComplianceSection.js layout redesign

**Acceptance Criteria**
- Extension spec document produced covering SI-02 and SI-04 card requirements
- Card layout contract defines all required display states
- Gate conditions (both SI-02 frontend + SI-04 sprint planning imminent) verified before commencing

---

### BLG-FE-62 — Pre-entry panel combined component specification (BLG-FE-56/57/58)
**Priority:** P3 (Low)
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner; Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-87 shipped v5.0)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-FE-56/57/58 sprint planning imminent; SI-02 frontend activation triggered (20+ closed trades confirmed). BLG-GOV-87 re-entry criteria shipped v5.0 — functional activation gate still pending.

**Problem**
BLG-FE-56 (warn/fail override separation), BLG-FE-57 (count badge when collapsed), and BLG-FE-58 (check grouping for Arc 5) are three interdependent PreEntryValidationPanel improvements. Specifying them individually risks fragmented UX implementation. A combined specification aligns all three changes before sprint planning seals.

**Scope**
- Combined component spec covering all three BLG-FE-56/57/58 improvements as a coherent design
- Map interaction dependencies (e.g., grouping in BLG-FE-58 affects badge count in BLG-FE-57)
- Input to sprint planning when gate triggers; replaces need for three separate spec documents

**Acceptance Criteria**
- Combined component spec produced and reviewed by Head of UX & Design
- All three BLG-FE-56/57/58 scopes covered in a single document
- Gate condition verified before sprint planning

---

### BLG-FE-63 — Arc 5 completion visual consistency pre-review
**Priority:** P3 (Low)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 binding conditions shipped v5.0; SI-04 is in Later horizon — gate triggers when SI-04 enters sprint planning.

**Problem**
SI-04 (strategy version comparison) and SI-05 (weekly digest display) will introduce new panels to the Arc 5 UI surface. No review of the existing Arc 5 design vocabulary (Pre-Entry panel, Red Flag Journal, Arc5ComplianceSection) has been done to ensure consistency before these additions begin. A pre-review before SI-04 implementation prevents retroactive consistency fixes.

**Scope**
- Review existing Arc 5 panel design patterns (colour, typography, layout, empty states)
- Identify consistency vocabulary: what patterns to carry forward to SI-04/SI-05 panels
- Produce short design vocabulary note; no implementation required

**Acceptance Criteria**
- Design vocabulary note produced covering existing Arc 5 panels
- Consistency patterns identified; input to SI-04/SI-05 sprint planning
- Gate condition verified before sprint planning

---

### BLG-FE-65 — User journey map: SI-05 Telegram digest to app action
**Priority:** P3 (Low)
**Type:** Frontend / UX Research
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-FE-55 (mobile responsiveness baseline, P3, gate-conditional) deprioritised.

**Problem**
SI-05 Phase 1 introduces a new workflow pattern: the user receives a Telegram notification (weekly digest) and then takes an action in the app (review Red Flag Journal, check compliance score, adjust behaviour). This is the first push notification → app action flow in the system. Friction mapping this journey surfaces improvements before SI-05 Phase 2 scope is defined.

**Scope**
- Map the user journey from receiving the SI-05 digest to completing an in-app action
- Identify: entry points (what links are in the digest), navigation steps to the relevant app screen, any friction encountered
- Produce a brief journey map document with friction findings; file follow-up backlog items if significant friction discovered

**Acceptance Criteria**
- User journey map document produced
- Entry points and navigation steps documented
- Friction findings enumerated; any significant friction filed as a separate backlog item
- Head of UX & Design sign-off

---

### BLG-FE-66 — RFJ date-range filter (date-to field)
**Priority:** P3 (Low)
**Type:** Frontend / UX Refinement
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Source:** ST-07 RFJ visual design review — filed 2026-06-22 (cycle 2026-06-19__release-v6.0)
**Effort:** XS
**Provisional-Target:** Unscheduled
**Gate criteria:** Event volume makes date-from-only filtering insufficient for review workflows.

**Problem**
The Red Flag Journal filter panel supports a "From date" input only. A growing journal has no upper date bound — a user reviewing "last month's" events cannot scope the view to a period. At current low event volume this is acceptable, but will become limiting as the journal grows.

**Scope**
- Add a "To date" input to the RFJ filter panel
- Update `GET /portfolio/red-flag-journal` to accept an optional `until` parameter
- Convert current date-from-only filter to a date range (from + to)

**Acceptance Criteria**
- "To date" filter input present in filter panel
- Results are scoped to [date-from, date-to] when both are set
- "Clear filters" clears both date inputs
- Existing "From date" behaviour unchanged when "To date" is not set

---

### BLG-FE-67 — RFJ event type colour palette refinement
**Priority:** P3 (Low)
**Type:** Frontend / Cosmetic / Accessibility
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Source:** ST-07 RFJ visual design review — filed 2026-06-22 (cycle 2026-06-19__release-v6.0)
**Effort:** XS
**Provisional-Target:** Unscheduled

**Problem**
The Red Flag Journal uses four warm-spectrum colours (amber-400, orange-400, red-400, rose-400) that are semantically arbitrary and difficult to distinguish under the `light-daltonized` theme. The colour for `checklist_skipped` (orange-400) blends with risk-event colours, and `drawdown_prompt_dismissed` (rose-400) is perceptually similar to `stop_prompt_dismissed` (red-400).

**Scope**
- Update `EVENT_TYPE_CONFIG` in `src/pages/RedFlagJournal.js`:
  - `checklist_skipped`: `orange-400` → `sky-400` (administrative miss, not a risk event)
  - `drawdown_prompt_dismissed`: `rose-400` → `red-500` (deeper risk signal, distinguishable from red-400)
- No other changes required (icons, layout, data model unchanged)

**Acceptance Criteria**
- `checklist_skipped` renders with `sky-400` colour indicator
- `drawdown_prompt_dismissed` renders with `red-500` colour indicator
- Other two event types (amber-400, red-400) unchanged
- Colours visible and semantically distinct under `light-daltonized` theme

---

### BLG-FE-68 — Arc 5 compliance score sparkline trend chart (gate-conditional)
**Priority:** P3 (Low)
**Type:** Frontend / Analytics Display
**Owner:** Metrics Definitions & Analytics Owner; Base44 Frontend Prompt Owner
**Source:** IDEA-metrics-analytics-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** BLG-FE-45 (Arc5ComplianceSection layout expandability review) complete

**Problem**
The Arc 5 compliance score is displayed as a single value on the compliance section. A sparkline trend chart showing the score's trajectory over recent weeks would help identify improving or degrading compliance at a glance. The gate is BLG-FE-45 — adding widgets to Arc5ComplianceSection before the layout expandability review is premature.

**Scope**
- Add sparkline trend chart to Arc5ComplianceSection (or equivalent compliance view)
- Data source: existing compliance score history endpoint or new rolling-window endpoint
- Chart shows last 8–12 weeks of compliance scores
- BLG-FE-45 must be complete before this enters sprint planning

**Acceptance Criteria**
- Sparkline chart renders in compliance section
- Data sourced from a defined endpoint (not mocked)
- Gate condition (BLG-FE-45) verified before sprint planning
- Playwright: chart renders with data; empty state handled

---

### BLG-FE-69 — SI-05 in-app digest panel — read-only last-sent view (gate-conditional)
**Priority:** P3 (Low)
**Type:** Frontend / Notification Display
**Owner:** Base44 Frontend Prompt Owner; Frontend Specs & UX Documentation Owner
**Source:** IDEA-base44-frontend-20260607-01 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Phase 2 channel decision (BLG-GOV-92 SI-05 Phase 2 activation criteria) — if Telegram remains the sole channel, this item is not required

**Problem**
SI-05 weekly digest is delivered via Telegram (v5.1). Users who miss a Telegram message have no way to retrieve the last digest content from within the app. An in-app read-only panel showing the last-sent digest content would provide a fallback reference point. However, this is premature until the Phase 2 channel decision confirms an in-app component is warranted.

**Scope**
- Read-only digest panel in Settings or a new SI-05 section
- Shows last digest sent: date, content summary, link counts
- No composition or editing — display only
- Phase 2 channel decision must be made before sprint planning

**Acceptance Criteria**
- Panel renders last-sent digest content
- Date and delivery status visible
- Gate condition (BLG-GOV-92 Phase 2 decision) verified before sprint planning

---

### BLG-FE-70 — Compliance score trend widget on dashboard homepage (gate-conditional)
**Priority:** P3 (Low)
**Type:** Frontend / Dashboard
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Source:** IDEA-base44-frontend-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** BLG-FE-45 (Arc5ComplianceSection layout expandability review) complete

**Problem**
Dashboard homepage shows key portfolio metrics but not the Arc 5 compliance score trend. A small trend widget on the homepage would surface compliance trajectory without requiring navigation to the full compliance section. Gate is BLG-FE-45 — homepage widget additions should follow the expandability assessment.

**Scope**
- Small compliance score trend widget on dashboard homepage
- Shows current score + trend arrow (up/down/flat vs prior week)
- Links to full Arc5ComplianceSection
- BLG-FE-45 must be complete before this enters sprint planning

**Acceptance Criteria**
- Widget renders on dashboard with current score and trend indicator
- Links correctly to full compliance section
- Gate condition (BLG-FE-45) verified before sprint planning

---

### BLG-FE-71 — SI-05 in-app digest UX spec — Phase 2 potential (gate-conditional)
**Priority:** P3 (Low)
**Type:** Frontend Spec / UX
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Phase 2 channel decision (BLG-GOV-92) — if in-app delivery is confirmed for Phase 2, this spec should precede implementation

**Problem**
If SI-05 Phase 2 includes an in-app delivery channel, a UX spec will be required before frontend implementation begins. Authoring the spec before the Phase 2 channel decision is premature — the spec scope depends entirely on which channel(s) Phase 2 targets.

**Scope**
- Interaction pattern for SI-05 digest delivery in-app (read, dismiss, archive)
- Visual design: notification panel, badge indicators, read/unread states
- Produced only if Phase 2 channel decision confirms in-app component
- Must be completed before BLG-FE-69 sprint planning

**Acceptance Criteria**
- UX spec produced covering interaction patterns and visual design
- Reviewed by Head of UX & Design and Frontend Specs & UX Documentation Owner
- Gate condition (BLG-GOV-92) verified before authoring

---

## 4. Backend & Data Backlog

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

### BLG-BE-21 — Arc 5 analytics endpoint versioning strategy
**Priority:** P3 (Low)
**Type:** Backend / API Design
**Owner:** Head of Backend Engineering; API Contracts Documentation Owner
**Source:** IDEA-backend-engineering-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 6 planning trigger — analytics endpoint versioning strategy needed when Arc 6 analytics endpoints are being designed alongside existing Arc 5 endpoints.

**Problem**
GET /analytics/arc5-compliance (shipped v4.0) and future Arc 6 analytics endpoints will coexist on the same service. Without an explicit versioning and naming convention, Arc 6 additions may collide with or shadow Arc 5 endpoints. A versioning strategy (path prefix, query param, or response envelope version) must be decided before Arc 6 sprint planning.

**Scope**
- Define endpoint versioning convention for analytics namespace
- Assess whether current /analytics/ prefix is extensible or requires refactoring
- Input to Arc 6 analytics endpoint design

**Acceptance Criteria**
- Versioning strategy documented in API design notes or openapi.yaml preamble
- Reviewed by API Contracts Documentation Owner and Head of Specs Team
- Gate condition (Arc 6 planning trigger) verified before commencing

---

### BLG-BE-24 — Red flag events retention policy
**Priority:** P2 (Medium)
**Type:** Backend / Data Lifecycle
**Owner:** Head of Backend Engineering; Infrastructure & Operations Owner
**Source:** IDEA-backend-engineering-20260522-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** red_flag_events table 6+ months old (post 2026-11-22).

**Problem**
The red_flag_events table has no defined data retention policy. As override events accumulate over months, query performance may degrade without indexes and archiving strategy. Defining a retention policy before the table requires unplanned maintenance is standard operational hygiene.

**Scope**
- Define minimum required event fields for retention
- Define archiving cadence (e.g. events older than 12 months archived to cold storage)
- Define query performance thresholds that trigger archiving review
- Document policy in ops notes

**Acceptance Criteria**
- Retention policy document produced
- Archiving cadence defined
- Gate condition (table 6+ months old) verified before commencing

### BLG-BE-27 — SI-02 drift service query performance baseline
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Performance
**Owner:** Backend Engineering Patterns Owner; Head of Engineering
**Source:** IDEA-backend-engineering-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed (BLG-GOV-87 re-entry criteria shipped v5.0 — functional activation still pending trade count gate).

**Problem**
The SI-02 drift service (shipped v4.6) uses window functions over trade_history and trade_plans. With only 6 closed trades, current query volume is too low to surface meaningful index gaps. A performance baseline at activation volume (20+ trades) establishes the query cost before concurrent frontend load is introduced.

**Scope**
- Run drift score queries against staging at 20+ trade volume
- Record p50/p95 query latency per metric (early_entry_rate, momentum_override_rate, losing_streak_sizing, regime_deviation_rate)
- Identify indexes required to maintain sub-200ms response at projected load

**Acceptance Criteria**
- Performance baseline document produced for all 4 drift metric queries
- Indexes identified and filed as implementation items if needed
- Gate condition verified before sprint planning

---

### BLG-BE-28 — Arc 4 PO-03 behavioral pattern storage pre-design
**Priority:** P3 (Low)
**Type:** Backend Engineering / Data Model
**Owner:** Backend Engineering Patterns Owner; Data Model, Domain & Schema Owner
**Source:** IDEA-backend-engineering-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 gate met (6+ months AI journal entries ~Oct 2026) + Arc 4 sprint planning triggered.

**Problem**
PO-03 (Behavioural Error Taxonomy) requires a new classification table and error_type enum. Pre-designing the schema before Arc 4 sprint planning prevents same-sprint data model debt (pattern observed in v3.3 IT-01/02/03 backend split).

**Scope**
- Define error_type enum values (entry_too_early, sized_incorrectly, ignored_regime, held_too_long, etc.)
- Define behavioral_errors table schema (id, trade_id, journal_entry_id, error_type, notes, detected_at)
- Pre-design migration strategy; no implementation until Arc 4 sprint

**Acceptance Criteria**
- Schema pre-design document produced
- error_type enum values defined and reviewed by Metrics Definitions & Analytics Owner
- Gate condition verified before sprint planning

---

### BLG-BE-29 — Database index review for SI-02 drift queries
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Performance
**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Source:** IDEA-head-of-engineering-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed. To be completed alongside or immediately after BLG-BE-27.

**Problem**
SI-02 drift service queries trade_plans and trade_history with window functions and date-range filters. Appropriate indexes must be confirmed before frontend activation adds concurrent load. BLG-BE-27 establishes the baseline; this item implements any gaps found.

**Scope**
- Review current indexes on trade_plans (signal_id, entry_date, exit_date) and trade_history (trade_id, close_date)
- Add indexes identified as missing from BLG-BE-27 performance baseline
- Verify drift score queries benefit from new indexes via EXPLAIN ANALYZE

**Acceptance Criteria**
- Index gaps identified and addressed
- EXPLAIN ANALYZE output confirms index usage for all drift metric queries
- Gate condition verified before sprint planning

---

### BLG-BE-30 — SI-04 schema requirements pre-design
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner
**Source:** IDEA-data-model-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 binding conditions shipped v5.0 — next gate is active sprint planning for SI-04 (Later horizon).

**Problem**
SI-04 strategy version comparison requires linking trade_plans to historical strategy_rules.md versions. Whether this is a new strategy_versions table, a foreign key, or a snapshot field must be decided before SI-04 sprint to avoid same-sprint data model debt. BLG-SPEC-43 (API contract) exists; data model pre-design is the remaining gap.

**Scope**
- Evaluate three schema options: new table (strategy_versions), FK on trade_plans (strategy_version), snapshot field (strategy_snapshot JSON)
- Recommend approach with rationale (versioning overhead vs query simplicity)
- Define migration path for existing trade_plans (backfill strategy)

**Acceptance Criteria**
- Schema pre-design document produced with recommended approach
- Reviewed by Data Model, Domain & Schema Owner and Strategy Rules & System Intent Owner
- Gate condition verified before sprint planning

---

### BLG-BE-31 — Arc 4 PO-04 reflection-outcome correlation data prerequisites
**Priority:** P3 (Low)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner
**Source:** IDEA-data-model-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 gate met + Arc 4 sprint planning triggered (~Oct-Dec 2026).

**Problem**
PO-04 (Reflection ↔ Outcome Correlation) requires journal entries with quantified reflection depth scores linked to trade outcomes. Neither reflection depth scoring nor the linkage from journal_entries to trade outcomes is currently captured. A data prerequisites assessment determines whether new fields are needed before Arc 4 sprint planning.

**Scope**
- Assess current journal_entries and trade_history data models for PO-04 readiness
- Identify new fields required: reflection_depth_score, journal_entry_id on trade_history, etc.
- Document prerequisites; no implementation until Arc 4 sprint

**Acceptance Criteria**
- Data prerequisites assessment document produced
- New fields required for PO-04 identified and estimated
- Gate condition verified before sprint planning

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

### BLG-QA-26 — Arc 5 QA protocol
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 5 fully complete per BLG-QA-45 criteria (docs/qa/arc5_qa_completion_criteria.md): SI-01 ✅, SI-02 backend ✅, SI-03 ✅, SI-05 Phase 1 ✅, BLG-QA-49 coverage assessment ✅. SI-02 frontend, SI-04, and SI-05 Phase 2 explicitly excluded from trigger. Updated 2026-06-16 (ST-09 v5.6).

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

### BLG-QA-42 — SI-02 E2E Playwright test strategy and scaffold
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed. BLG-QA-37 (Playwright mock strategy for drift features, shipped v4.2) defines the approach — this item implements it.

**Problem**
SI-02 drift service (35 unit tests, shipped v4.6) has no E2E Playwright coverage. When the frontend ships (~2027-Q1), test coverage must be ready immediately. Pre-building the scaffold 1–2 cycles before activation avoids rushed test creation under sprint pressure.

**Scope**
- Define E2E test strategy for GET /analytics/behavioural-drift (per BLG-QA-37 Playwright mock strategy)
- Scaffold Playwright test file with scenarios: drift scores render, gate-not-met state, all 4 metric cards display
- Confirm mock data approach (per BLG-QA-37 mock strategy)

**Acceptance Criteria**
- E2E test strategy document produced
- Playwright test scaffold created and passing against mock data
- All 4 drift metric display scenarios covered
- Gate condition verified before sprint planning

---

### BLG-QA-44 — SI-04 test planning requirements definition
**Priority:** P2 (Medium)
**Type:** QA / Test Planning
**Owner:** QA Lead; Director of Quality
**Source:** IDEA-qa-lead-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 binding conditions shipped v5.0 — functional activation gate is SI-04 entering sprint planning (Later horizon).

**Problem**
SI-04 (strategy version comparison) requires test coverage across: unit tests (version comparison logic), integration tests (trade_plans version linkage), and Playwright (version diff display). Defining test requirements before sprint planning ensures test scope is clear and prevents test debt analogous to BLG-QA-24 (Yahoo Finance backoff).

**Scope**
- Define unit test requirements: version comparison logic, version not found case
- Define integration test requirements: trade_plans version linkage correctness
- Define Playwright scenario requirements: version diff display, empty state, gate-not-met
- Estimate test effort; input to sprint sizing

**Acceptance Criteria**
- Test requirements document produced covering all three test tiers
- Playwright scenario outlines defined
- Gate condition verified before sprint planning

---

### BLG-QA-55 — SI-02 Playwright scaffold readiness assessment (gate-conditional)
**Priority:** P3 (Low)
**Type:** QA / Test Planning
**Owner:** QA & Testing Owner; Director of Quality
**Source:** IDEA-qa-testing-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥20 closed trades confirmed (same gate as SI-02 frontend activation — BLG-QA-42)

**Problem**
BLG-QA-42 (SI-02 Playwright scaffold) is gated on 20+ closed trades. When that gate clears and SI-02 frontend enters sprint planning, a readiness assessment of the BLG-QA-42 scaffold design should confirm it still reflects the final drift service implementation (which may have evolved since BLG-QA-42 was authored). This assessment prevents outdated scaffold assumptions from entering sprint planning.

**Scope**
- Review BLG-QA-42 Playwright pre-design against the final GET /analytics/behavioural-drift response schema
- Confirm mock strategy is still valid or update scaffold design
- Produce brief readiness confirmation document
- Gate: 20+ closed trades must be confirmed before this assessment is commissioned

**Acceptance Criteria**
- Scaffold design reviewed against current drift endpoint response schema
- Assessment confirms "proceed with BLG-QA-42 as-is" or produces a revision document
- Director of Quality sign-off
- Gate condition verified (≥20 closed trades)

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add new v2.8/v2.9/v3.0/v3.4/v3.9/v4.6 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 (3 endpoints); v3.0 post-ship closure 2026-04-28 OA-v30-01 (5 additional endpoints); v3.1 post-ship closure 2026-05-05 (10 additional endpoints); v3.4 post-ship closure 2026-05-14 (2 additional endpoints); v3.5 post-ship closure 2026-05-15 (2 additional endpoints); v3.9 post-ship closure 2026-05-22 (1 additional endpoint: GET /portfolio/red-flag-journal); v4.6 post-ship closure 2026-05-31 (1 additional endpoint: GET /analytics/behavioural-drift)
**Effort:** M (~2 days — 24 endpoints total)
**Provisional-Target:** Before next performance baseline review

**Problem**
Twenty-two endpoints shipped in v2.8/v2.9/v3.0/v3.1/v3.4/v3.5 are absent from `docs/ops/api_performance_baseline.md`. Performance re-runs require a live environment and human coordination — baseline updates cannot be automated.

**Scope (updated 2026-05-31):**
- v2.8/v2.9 endpoints (3): `POST /ai/journal-summary`, `GET /ai/journal-summary/history`, `GET /v1beta1/news`
- v3.0 endpoints (5): `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}`, `GET /screener/results`, `POST /screener/run`
- v3.1 endpoints (10): `POST /trade-plans`, `GET /trade-plans/{id}`, `PUT /trade-plans/{id}`, `DELETE /trade-plans/{id}`, `GET /trade-plans/by-position/{position_id}`, `GET /trade-plans/by-ticker/{ticker}`, `GET /research/{ticker}`, `GET /earnings/{ticker}`, `GET /reports/monthly-pnl`, plus any additional v3.1 routes
- v3.4 endpoints (2): `GET /portfolio/drawdown-status`, `GET /portfolio/concentration-status`
- v3.5 endpoints (2): `GET /portfolio/paper-positions`, `GET /trades/{trade_id}/plan-vs-reality`
- v3.9 endpoints (1): `GET /portfolio/red-flag-journal`
- v4.6 endpoints (1): `GET /analytics/behavioural-drift`
- Run each against staging to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- All 24 endpoints have p50 and p95 latency entries in the baseline document
- Entries consistent with existing baseline measurement methodology

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

### BLG-OPS-41 — Red flag events table archiving strategy
**Priority:** P2 (Medium)
**Type:** Operations / Data Lifecycle
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260522-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** red_flag_events table 6+ months old (post 2026-11-22).

**Problem**
The red_flag_events table has no defined retention or archiving strategy. As override events accumulate, the table will grow. Without an archiving policy, the table may require unplanned manual intervention. Defining the strategy before the table reaches significant size is operationally prudent.

**Scope**
- Define: retention window (e.g., keep 12 months active; archive older rows to cold storage)
- Define: archiving trigger (size-based vs age-based) and procedure
- Document strategy in ops notes; complement BLG-BE-24 retention policy

**Acceptance Criteria**
- Archiving strategy document produced
- Retention window and trigger defined
- Gate condition (table 6+ months old) verified before commencing

---

### BLG-OPS-48 — ANTHROPIC_API_KEY 6-month scope audit
**Priority:** P2 (Medium)
**Type:** Operations / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** ~v4.9 (date-gated: no earlier than 2026-11-01)
**Provisional-Target:** Gate date: 2026-11-01 (~6 months after BLG-OPS-36 scope review in v4.2, 2026-05-28)

**Problem**
BLG-OPS-36 (ANTHROPIC_API_KEY scope review) was completed in v4.2 (2026-05-28). Security policy (BLG-OPS-38) requires periodic key scope reviews. 6-month follow-up due ~November 2026 to verify key scope remains minimal and no scope creep has occurred in the API key permissions.

**Scope**
- Review ANTHROPIC_API_KEY permissions against current usage patterns
- Confirm key is not used outside the documented endpoints (generate-thesis, check-daily-cost)
- Verify key rotation has occurred per BLG-OPS-38 policy
- Document review findings

**Acceptance Criteria**
- ANTHROPIC_API_KEY scope confirmed minimal (only documented endpoints)
- Key rotation confirmed per BLG-OPS-38 schedule
- Review findings documented

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

### BLG-SPEC-44 — SI-02 drift threshold calibration specification
**Priority:** P2 (Medium)
**Type:** Specification / Metrics Definition
**Owner:** Metrics Definitions & Analytics Owner; Head of Specs Team
**Source:** IDEA-metrics-analytics-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-87 shipped v5.0)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed. BLG-GOV-87 re-entry criteria document shipped v5.0 — functional activation gate still pending.

**Problem**
SI-02 backend (shipped v4.6) defines 4 drift metrics (early_entry_rate, momentum_override_rate, losing_streak_sizing, regime_deviation_rate) but does not specify meaningful alert thresholds. Without calibrated thresholds, the frontend display may surface false positives (alert fatigue) or miss genuine drift. Thresholds should be defined before frontend activation.

**Scope**
- Define alert thresholds for each of the 4 drift metrics (e.g., early_entry_rate > 40% = amber, > 60% = red)
- Provide rationale for each threshold (e.g., based on your own historical compliance data, statistical percentiles)
- Define score interpretation guidance for the user-facing display
- Add threshold definitions to metrics_definitions.md (per §12 of that document)

**Acceptance Criteria**
- Threshold calibration specification document produced
- All 4 drift metrics have defined alert levels with rationale
- metrics_definitions.md updated with drift threshold definitions
- Gate condition verified before sprint planning

---

### BLG-SPEC-46 — Arc 4 API contract pre-planning surface area
**Priority:** P3 (Low)
**Type:** Specification / API Contracts
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-SPEC-35 (PO-02 §13 boundary review) complete. Arc 4 API contract surface area is premature before §13 determines whether PO-02/PO-03 constitute "adaptive logic" or "structured pattern extraction."

**Problem**
PO-02 (journal pattern recognition) and PO-03 (behavioural error taxonomy) will each require new API endpoints. Pre-defining the endpoint surface area (GET /analytics/journal-patterns, classification endpoints) before Arc 4 sprint prevents same-sprint API spec debt analogous to the Arc 5 retroactive contracts filed in v4.1/v4.2.

**Scope**
- Define candidate endpoint names and response shapes for PO-02 and PO-03
- Produce lightweight endpoint surface area document (not full contracts — just paths, methods, response envelopes)
- Input to Arc 4 release planning; pre-authorise contract authoring for named endpoints

**Acceptance Criteria**
- Endpoint surface area document produced for PO-02 and PO-03 APIs
- Reviewed by API Contracts & Documentation Owner and Head of Specs Team
- Gate condition (BLG-SPEC-35 complete) verified before commencing

---

### BLG-SPEC-55 — Arc 4 API contract pre-planning surface area advancement check (gate-conditional)
**Priority:** P3 (Low)
**Type:** Specification / API Contracts
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning confirmed imminent — when PO confirms ≥6 months AI-summarised journal entries gate is cleared and PO-02 is entering sprint planning

**Problem**
BLG-SPEC-46 (Arc 4 API surface area) is a gate-conditional spec planning item that was parked until PO-02 sprint planning is imminent (~Oct 2026). When that gate clears, an advancement check should confirm BLG-SPEC-46's scope still reflects the final Arc 4 API surface — the surface may have evolved since BLG-SPEC-46 was authored. This item tracks that confirmation step.

**Scope**
- Review BLG-SPEC-46 against current api_contracts/ documents and openapi.yaml
- Confirm Arc 4 API surface is still accurately captured or produce a revision scope
- Produce brief readiness note: "BLG-SPEC-46 proceed as-is" or list required updates
- Gate: PO-02 sprint planning imminent confirmation by PMO Lead

**Acceptance Criteria**
- BLG-SPEC-46 scope reviewed against current API surface
- Readiness note produced with clear proceed/update decision
- API Contracts & Documentation Owner sign-off
- Gate condition verified

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

### BLG-GOV-68 — Backlog item inter-dependency tracking
**Priority:** P2 (Medium)
**Type:** Governance / Process Enhancement
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-pmo-lead-20260522-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** 20+ concurrent implementation items in a single sprint causing dependency-blocking.

**Problem**
Backlog items have no explicit Blocks/Blocked-by fields. Cross-item dependencies are currently documented via prose in backlog entries (e.g. "Gate: BLG-OPS-36 complete"). As the backlog grows, undiscovered dependencies become sprint-time blockers. A formal inter-dependency field would surface critical path items at sprint planning.

**Scope**
- Add Blocks/Blocked-by field to backlog item format (optional; populated when dependency is known)
- Update sprint planning engine to surface Blocks/Blocked-by chains
- Back-fill critical known dependencies (BLG-OPS-36 → BLG-OPS-37, etc.)

**Acceptance Criteria**
- Field format defined and documented in backlog header conventions
- Sprint planning engine updated to surface dependency chains
- Gate condition (20+ concurrent items with dependency-blocking evidence) verified before commencing

---

### BLG-GOV-71 — Governance engine complexity assessment (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Director of HR; PMO Lead
**Source:** IDEA-director-of-hr-20260525-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036; terminal 3-cycle disposition)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Audit overall score drops below 70 OR a step-skip event is formally documented in an audit report.

**Problem**
Governance engine prompts have grown complex over 33 cycles. Without periodic complexity assessment, latent process friction accumulates invisibly. This assessment would identify steps that rarely trigger, candidates for simplification, and produce a governance simplification roadmap for meta-review.

**Scope**
- For each governance engine prompt: count steps, hard gates, and write operations
- Identify steps with documented "never triggered" patterns from lessons_learnt.md history
- Propose candidates for simplification, consolidation, or removal

**Acceptance Criteria**
- Per-engine complexity metrics documented
- Simplification candidates enumerated with rationale
- Gate condition verified before commencing

---

### BLG-GOV-73 — Scheduled rebalance cadence review
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-pmo-lead-20260601-02 + IDEA-challenger-20260601-02 (merged) — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Advance at next meta-review cycle (rebalance_cycles_since_meta_review ≥ 3).

**Problem**
10+ scheduled rebalances since 2026-03-24. CPS stable at 1.15. Multiple consecutive scheduled rebalances have had empty Now horizons with no items advancing. The Challenger raised the concern that running full governance process when no strategic decision is pending may produce overhead without proportional value.

**Scope**
- Review scheduled rebalances since last meta-review for value produced (items advanced, horizon movements, CPS changes)
- Assess whether a lightweight mode for no-change-expected cycles could reduce overhead
- Produce recommendation: maintain cadence or propose modification; present at next meta-review

**Acceptance Criteria**
- Value analysis of recent scheduled rebalances documented
- Recommendation produced and presented at next meta-review
- Gate condition (cycles_since_meta_review ≥ 3) verified before commencing

---

### BLG-GOV-74 — AI feature usage quarterly review (BLG-GOV-63 mandate)
**Priority:** P2 (Medium)
**Type:** Governance / Compliance
**Owner:** AI Compliance & Governance Officer; PMO Lead
**Source:** IDEA-ai-compliance-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036; fulfills BLG-GOV-63 mandate)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.10 or first cycle after 2026-08-29
**Gate date:** First review due 2026-08-29 (3 months after v4.0 AI feature ship 2026-05-29)

**Problem**
BLG-GOV-63 (shipped v4.2) requires a quarterly review of the claude_audit_log. First quarterly review due 2026-08-29. Without a backlog item it will be missed.

**Scope**
- Review claude_audit_log for the preceding quarter (v4.0–v4.8 window)
- Assess: total thesis generation requests, model version used, override_rate, cost per use
- Flag anomalies; document findings; file BLG items for any anomalies

**Acceptance Criteria**
- Quarterly audit log review completed; findings documented
- Anomalies (if any) filed as BLG items
- Next review date recorded (2026-11-29)

---

### BLG-OPS-51 — Add GET /analytics/strategy-version-comparison to api_performance_baseline.md (when implemented)
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner; API Contracts & Documentation Owner
**Source:** Post-ship closure 2026-06-01__release-v4.8 — endpoint coverage drift advisory (STEP 6)
**Effort:** S (~0.5 day)
**Provisional-Target:** SI-04 sprint (whenever GET /analytics/strategy-version-comparison is implemented)

**Problem**
v4.8 ST-07 added a placeholder entry for GET /analytics/strategy-version-comparison to openapi.yaml (pre-authored contract; not yet implemented). Once implemented, this endpoint will need p50/p95 latency measurement and an entry in docs/ops/api_performance_baseline.md.

**Scope**
- After SI-04 sprint implements the endpoint: run performance baseline measurement (p50/p95)
- Add measurement to docs/ops/api_performance_baseline.md

**Acceptance Criteria**
- GET /analytics/strategy-version-comparison present in api_performance_baseline.md with p50/p95 values
- Measurement conducted with ≥5 staging samples

---

### BLG-OPS-53 — Application log retention policy expansion (Supabase + claude_audit_log)
**Priority:** P3 (Low)
**Type:** Operations / Data Lifecycle
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-infra-ops-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** claude_audit_log table 6+ months old (~Nov 2026, since v4.0 ship 2026-05-22). BLG-OPS-31 (Render log retention policy) shipped v4.7; this extends scope to Supabase query logs and claude_audit_log.

**Problem**
BLG-OPS-31 defined Render log retention. claude_audit_log (shipped v4.0) and Supabase query logs have no defined retention policy. As audit log volume grows, query performance and storage cost may degrade without archiving strategy.

**Scope**
- Define retention period for claude_audit_log (e.g., 12 months rolling)
- Define Supabase query log retention consistent with data privacy obligations
- Define archiving trigger (log volume threshold or time-based)
- Document policy in docs/operations/

**Acceptance Criteria**
- Retention policy document produced covering claude_audit_log and Supabase query logs
- Archiving cadence defined
- Gate condition (6+ months of audit log data) verified before sprint planning

---

### BLG-OPS-54 — Add POST /digest/si05/send to api_performance_baseline.md
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner; PMO Lead
**Source:** Post-ship closure 2026-06-21__release-v5.1 — endpoint drift check (STEP 6)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** Unscheduled (pending live environment access)
**Scope revision (I&O Owner, 2026-06-22):** Standard external HTTP measurement is not viable for this endpoint — it blocks on the Telegram Bot API and timed out at 45s in the §19 baseline run. Revised approach: (1) Render internal log duration (server-side p50/p95), (2) weekly delivery success rate from `si05_digest_log`, (3) Telegram API timeout flag if request duration > 30s. See ST-11 staging evidence (docs/testing/staging_latency_review_ST-11.md).

**Problem**
`POST /digest/si05/send` was added to `docs/reference/openapi.yaml` in v5.1 (ST-01, EPIC-01). This endpoint is not present in `docs/ops/api_performance_baseline.md`. Standard external HTTP measurement is not viable (Telegram API timeout — excluded from §19 standard run). A Render internal log-based measurement approach is required.

**Scope**
- Add `POST /digest/si05/send` to `docs/ops/api_performance_baseline.md` using Render internal log duration (server-side), not external HTTP timing
- Extract p50/p95 from Render production logs for the dispatch endpoint
- Record weekly delivery success rate from `si05_digest_log` as the primary health metric

**Acceptance Criteria**
- POST /digest/si05/send present in api_performance_baseline.md with Render internal log-based measurements recorded
- Measurement methodology note added explaining why standard external HTTP timing does not apply

---

### BLG-GOV-84 — Arc 6 gate revision and threshold assessment
**Priority:** P3 (Low)
**Type:** Governance / Product Planning
**Owner:** Product Owner; Challenger; Strategy Rules & System Intent Owner
**Source:** IDEA-product-owner-20260527-02 + IDEA-challenger-20260527-01 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; terminal Parked-cycle-2 combined disposition)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 50 closed trades (trajectory approaching) — at current ~1–2 trades/month, this is approximately 2026-Q4/2027.

**Problem**
PS-01 (Edge Analysis Dashboard) gate requires 100+ trades with plans and lifecycle data. At current trade frequency (1–2 trades/month), this gate takes 5–8 years to clear. The Challenger has raised (twice) that a meaningful edge analysis may be achievable with 20–30 closed trades with explicit statistical caveats. The Product Owner's Arc 6 minimum viable entry assessment (also raised twice) asks whether the gate calibration is appropriate. Both ideas address the same question: is the 100-trade threshold right? A formal assessment when trade count approaches 50 is the appropriate trigger.

**Scope**
- Formal assessment: at ≥50 closed trades, evaluate whether PS-01 can yield meaningful signal with available history (20–30 qualifying trades as a subset)
- Assess: what statistical confidence is achievable at 30 vs 50 vs 100 trades? Are explicit caveats sufficient to communicate limited confidence?
- Challenge the threshold: if PO decides 30–50 trades is sufficient with caveats, recommend gate revision; document decision in decision_log.md
- §13 check: any gate revision must remain within the "deterministic historical analysis" framework; no predictive claims

**Acceptance Criteria**
- Assessment document produced when ≥50 closed trades confirmed
- Threshold recommendation made (maintain 100-trade gate OR revise with documented caveats)
- PO + Challenger + Strategy Rules Owner sign-off on recommendation
- If gate revised: decision_log.md updated; PS-01 roadmap section updated
- Gate condition (≥50 closed trades approaching) verified before commencing

---

### BLG-GOV-85 — Arc 6 §13 pre-assessment boundary document
**Priority:** P3 (Low)
**Type:** Governance / §13 Compliance Pre-work
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260527-02 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; terminal Parked-cycle-2 disposition)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 6 release planning trigger (first sprint planning cycle that includes a PS-01 through PS-05 story).

**Problem**
Arc 6 features (PS-01 through PS-05) are roadmapped with informal §13 compliance notes ("deterministic simulation, §13 COMPLIANT"; "statistical observation, not prediction"). Before Arc 6 sprint planning seals, a formal §13 pre-assessment must consolidate binding conditions for each feature — as was done for SI-01 (8 conditions), IT-06 (4 conditions), SI-04 (6 conditions). PS-03 already has a formal §13 PASS assessment (10 conditions, v4.6). PS-01, PS-02, PS-04, PS-05 need similar pre-assessment documents.

**Scope**
- Formal §13 pre-assessment for PS-01, PS-02, PS-04, PS-05 (PS-03 already complete)
- Each assessment confirms: deterministic calculation only, display-only output, no automated recommendations, no ML/prediction components
- Binding conditions documented per the SI-01/IT-06 pattern
- Strategy Rules & System Intent Owner sign-off required on each assessment

**Acceptance Criteria**
- §13 assessment documents produced for PS-01, PS-02, PS-04, PS-05
- Binding conditions documented for each PASS determination
- Gate condition (Arc 6 release planning trigger) verified before commencing

---

### BLG-GOV-90 — Claude model deprecation monitoring procedure
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Source:** IDEA-ai-compliance-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-GOV-74 first quarterly AI feature review completes (due 2026-08-29). Consolidate this procedure definition with the BLG-GOV-74 review action.

**Problem**
BLG-GOV-64 pins the model to claude-3-5-sonnet. Anthropic publishes model deprecation notices. No formal procedure exists for checking deprecation notices on a schedule and triggering a governed sprint story to update the pinned model. BLG-GOV-74 (quarterly AI review, first due 2026-08-29) is the natural integration point for a standard procedure.

**Scope**
- Define quarterly deprecation check procedure: check Anthropic model lifecycle page, compare against pinned model in BLG-GOV-64 policy
- Define trigger: if deprecation notice issued → file P1 sprint story to update pinned model
- Document procedure in docs/governance/ai_model_policy.md or equivalent

**Acceptance Criteria**
- Deprecation monitoring procedure defined and documented
- Procedure integrated with BLG-GOV-74 quarterly review cadence
- Gate condition (BLG-GOV-74 first review complete) verified before sprint planning

---

### BLG-GOV-91 — SI-04 strategy history access security review
**Priority:** P2 (Medium)
**Type:** Governance / Security Review
**Owner:** Cybersecurity & Trust Lead; Strategy Rules & System Intent Owner
**Source:** IDEA-cybersecurity-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 (binding conditions doc) shipped v5.0 — SI-04 remains in Later horizon; gate triggers when SI-04 enters sprint planning.

**Problem**
SI-04 (strategy version comparison) will access historical strategy_rules.md content and link it to trade data. This creates a data access pattern not present in SI-01 through SI-03: querying historical document versions alongside personal trade records. A security pre-assessment confirms whether this pattern introduces any data pattern or access control concerns before sprint planning.

**Scope**
- Assess data access pattern: historical strategy content + trade data linkage
- Determine if any additional access controls or audit logging are required
- Document as security review record per BLG-GOV-31 (security review pattern)
- Cybersecurity & Trust Lead sign-off

**Acceptance Criteria**
- Security review record produced covering SI-04 data access pattern
- PASS or REQUIRES_MITIGATIONS determination with evidence
- Cybersecurity & Trust Lead sign-off recorded
- Gate condition verified before sprint planning

---

### BLG-GOV-95 — strategy_rules.md annual parameter review schedule
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Source:** IDEA-strategy-owner-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-GOV-29 (trade plan AI audit log, P3, gate-conditional) deprioritised.

**Gate criteria:** ≥ 30 closed trades with ATR-based stop exits in production (sufficient data density to assess parameter appropriateness).

**Problem**
strategy_rules.md §11 defines production parameters (5× initial ATR, 2× profitable ATR, 10-day grace period). These have never been reviewed against live trading performance data — the system has run on its original parameter settings since inception. §12.3 requires documented rationale for any parameter change, but there is no scheduled review mechanism to surface whether changes are warranted.

**Scope**
- Define annual parameter review process: PMO Lead adds review to the next roadmap rebalance after gate clears (≥30 closed trades with stop exits)
- Review scope: compare actual trade outcomes against parameter-predicted outcomes for each parameter (does 5× ATR give sufficient breathing room? does 2× ATR lock in enough gain on average?)
- Output: parameter review report; PO + Strategy Rules owner decision: maintain, adjust (with §12.3 rationale), or schedule future review
- If parameters adjusted: follow §12.3 change control (version increment, rationale, consistency across backtests)

**Acceptance Criteria**
- Parameter review process document produced
- Gate condition (≥30 closed trades with stops) verified before review commences
- Product Owner and Strategy Rules & System Intent Owner sign-off on review findings
- If parameters adjusted: strategy_rules.md version increment with §12.3-compliant rationale

---

### BLG-GOV-102 — Arc completion velocity scorecard (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Product Planning Reference
**Owner:** Product Owner; PMO Lead
**Source:** IDEA-product-owner-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-GOV-85 (Arc 6 §13 boundary document, P3, gate-conditional) deprioritised.

**Gate criteria:** Arc 5 fully complete (all five Arc 5 features: SI-01 ✅, SI-03 ✅, SI-05 Phase 1 ✅, SI-02 frontend, SI-04 — all shipped).

**Problem**
With 6 arcs spanning v2.9–v4.0+, there is no single reference document showing arc-level completion status: which arcs are done, which are in progress, which features remain, and what gate conditions are outstanding. As the project moves from Arc 5 toward Arc 6, assembling this picture from multiple sections of current_roadmap.md is time-consuming at each release planning session.

**Scope**
- One-page arc completion scorecard: for each of the 6 arcs, list (a) arc status (Complete/In Progress/Planned), (b) features shipped, (c) features remaining, (d) gate conditions outstanding, (e) earliest realistic activation date
- Filed in docs/product/ or claude/roadmap/
- Updated at each major arc milestone; not a living document requiring cycle-by-cycle updates

**Acceptance Criteria**
- Arc completion scorecard document produced covering all 6 arcs
- Gate condition (Arc 5 fully complete) verified before authoring (ensures Arc 5 data is final)
- Product Owner sign-off

---

### BLG-GOV-103 — Staged verification sprint tracking worksheet (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Process Tool
**Owner:** Director of Quality; PMO Lead
**Source:** IDEA-pmo-lead-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1 hour)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-GOV-90 (Claude model deprecation monitoring procedure, P2, gate-conditional) deprioritised.

**Gate criteria:** BLG-GOV-89 (staged verification sprint protocol, shipped v5.1) used 2+ times in practice. First use: v5.1 staged ACs; second use: this staged verification sprint (SI-05 Phase 1 deferred ACs). Gate clears after the v5.1 staged verification sprint is completed.

**Problem**
BLG-GOV-89 (staged verification sprint protocol) defines the pattern. After 2+ uses, a companion tracking worksheet — a simple checklist capturing: which releases have deferred ACs, which ACs per release, their status (pending/verified/signed-off) — would reduce coordination overhead when multiple staged ACs accumulate across releases.

**Scope**
- Produce a single-page tracking worksheet template (Markdown table) for staged verification sprints: columns = Release, AC ID, Description, Status, Evidence, Sign-off Date
- Template filed in docs/operations/ alongside BLG-GOV-89 protocol
- Reviewed by Director of Quality and PMO Lead

**Acceptance Criteria**
- Worksheet template produced and filed
- Gate condition (BLG-GOV-89 used 2+ times) verified before authoring
- Director of Quality and PMO Lead sign-off

---

### BLG-GOV-105 — Arc 6 PS-03 Monte Carlo §13 threshold pre-assessment
**Priority:** P2 (Medium)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (before Arc 6 moves from Later to Next)
**Displacement:** BLG-GOV-111 (v5.3 design gate pre-assessment, lower-P) deprioritised.

**Problem**
Arc 6 PS-03 (Monte Carlo simulation) requires a §13 review before sprint planning. The core §13 question — "is Monte Carlo simulation deterministic or predictive?" — can be answered definitively now without knowing implementation details. A pre-assessment scoped to this threshold question de-risks Arc 6 sprint planning entry.

**Scope**
- Assess whether Monte Carlo simulation as described in current_roadmap.md §5 (PS-03 notes) is deterministic (replaying own trade distribution) or predictive (forecasting future outcomes)
- Determine: does PS-03 engage the §13 boundary "Not an ML-based prediction system"?
- Produce a one-page §13 threshold assessment; if PASS (deterministic), note that binding conditions will be defined at full §13 review when Arc 6 moves to Next
- Note: scope is threshold question only — NOT a full §13 review with binding conditions

**Acceptance Criteria**
- §13 threshold assessment produced for PS-03 (deterministic vs predictive question answered)
- PASS/FAIL on the threshold question documented
- Strategy Rules & System Intent Owner sign-off

---

### BLG-GOV-119 — Arc 5 delivered value retrospective (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Strategic Review
**Owner:** Product Owner; Strategy Rules & System Intent Owner
**Source:** IDEA-challenger-20260610-01 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** SI-04 (strategy version comparison) AND SI-05 Phase 2 both shipped

**Problem**
Arc 5 is functionally near-complete (SI-01/02/03 shipped; SI-04 pre-planned; SI-05 Phase 1 live). Before committing to Arc 6, a retrospective against the original Arc 5 end-state intent would confirm whether the arc is delivering its stated purpose: "making every deviation visible, deliberate, and recorded."

**Scope**
- Review Arc 5 end-state description against delivered features
- Assess whether SI-01/02/03/05 collectively achieve the stated purpose
- Produce a 1-page retrospective document; note gaps or intent drift

**Acceptance Criteria**
- Retrospective document produced and filed
- Gap list (if any) filed as backlog items
- Product Owner + Strategy Rules & System Intent Owner sign-off
- Gate: SI-04 + SI-05 Phase 2 both shipped

---

### BLG-GOV-121 — SI-05 Phase 2 §13 pre-clearance document (gate-conditional)
**Priority:** P2 (Medium)
**Type:** Governance / Strategy Compliance
**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Source:** IDEA-strategy-owner-20260610-02 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** 2026-07-04 SI-05 effectiveness review output (BLG-GOV-113) complete AND Phase 2 activation decision made

**Problem**
SI-05 Phase 2 integrates drift signals (SI-02) with the Telegram digest. Before Phase 2 activates, a targeted §13 review should confirm that incorporating drift signals into an automated notification remains compliant with the "not an automated trading system" and "human-in-the-loop" principles. Phase 1 cleared §13 (notification of compliance scores + red flags). Phase 2 adds drift-signal interpretation — this boundary warrants formal pre-clearance.

**Scope**
- Extend the SI-05 Phase 1 §13 review framework to Phase 2 scope
- Confirm: drift signal summary in digest is informational, not prescriptive; no automated action triggered
- Document binding conditions for Phase 2 operation (analogous to IT-06 §13 conditions)

**Acceptance Criteria**
- §13 pre-clearance document produced and filed
- Strategy Rules & System Intent Owner sign-off
- Gate condition verified before Phase 2 sprint planning

---

### BLG-GOV-122 — strategy_rules.md §11 parameter annual review
**Priority:** P3 (Low)
**Type:** Governance / Strategy Review
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260610-01 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
strategy_rules.md §11 defines concrete trading parameters (ATR multipliers, grace period days, regime gate thresholds). These were validated at v5.3 (BLG-GOV-104) but an annual review should confirm they still reflect the operator's current strategy intent. With 40+ cycles and real trading data accumulating, parameter drift (operating differently from what §11 states) should be checked.

**Scope**
- Review §11 parameters against actual trading behaviour over the last 12 months
- Identify any divergence between documented parameters and actual practice
- If divergence found: either update strategy_rules.md (version increment) or document intentional deviation

**Acceptance Criteria**
- Review conducted; findings documented
- If changes: strategy_rules.md versioned and change rationale filed
- Strategy Rules & System Intent Owner sign-off

---

### BLG-GOV-123 — SC-01: Extract Playwright test standard from execution_prompt.md to shared_standards
**Priority:** P2 (Medium)
**Type:** Governance / Prompt Simplification
**Owner:** Head of Specs Team
**Source:** GCA-2026-06-17 — ST-04 (BLG-GOV-101) simplification candidate SC-01
**Effort:** XS (~1 hour)
**Provisional-Target:** v5.9

**Scope**
Section 14 of `execution_prompt.md` defines Playwright test authoring standards (waitFor patterns, mock payload advisory, ~30 lines). This content is loaded on every invocation of the execution engine regardless of whether the sprint contains any Playwright work. Extract to `shared_standards.md §16` (or a new §17) and replace Section 14 with a single reference line. No logic change — structural refactoring only.

**Acceptance Criteria**
- Section 14 content moved to shared_standards.md with a new heading
- execution_prompt.md Section 14 replaced with reference: "Playwright test standard: per shared_standards.md §X"
- Version bump on both files; changelog entries appended
- Head of Specs Team sign-off

---

### BLG-GOV-124 — SC-02: Remove RESUME PRECHECK mutation detection block from release_planning_prompt.md
**Priority:** P3 (Low)
**Type:** Governance / Prompt Simplification
**Owner:** Head of Specs Team
**Source:** GCA-2026-06-17 — ST-04 (BLG-GOV-101) simplification candidate SC-02
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled (governance sprint)

**Scope**
The RESUME PRECHECK mutation detection block in `release_planning_prompt.md` (~80 lines, lines 417–510) handles interrupted multi-session runs and assumption invalidation. This path has never been exercised in 100% of recorded v4.x–v5.x cycles. The lightweight state.json resume rule (7 lines) provides sufficient resumability for the observed failure mode. Remove the invalidation map and efficiency policy block; retain the state.json check. Requires dry-run validation pass.

**Implementation constraint (Head of Specs Team sign-off GCA-2026-06-17):** The Terminal State Guard ("Published Is Immutable") and State File Immutability Rule hard gates within the RESUME PRECHECK block must be extracted and retained outside the block before the mutation detection/invalidation map machinery is removed. The implementing story must explicitly scope the deletion and confirm these two gates survive.

**Acceptance Criteria**
- RESUME PRECHECK mutation detection/invalidation map block removed (mutation-detection portion only)
- Terminal State Guard and State File Immutability Rule hard gates extracted and retained in the prompt body
- State.json resume rule retained
- Dry-run validation pass confirming no functional regression
- Version bump + changelog entry
- Head of Specs Team sign-off

---

### BLG-FE-72 — Arc 4 PO-02 journal pattern UX spec (gate-conditional)
**Priority:** P3 (Low)
**Type:** Frontend & UX / Specification
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260608-02 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-043)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning confirmed imminent — PMO Lead confirmation required before commissioning this work

**Problem**
PO-02 (Journal Pattern Recognition) requires displaying cross-entry AI analysis results: recurring themes, emotional patterns, setup types, conditions present at winning vs losing entries. No UX specification exists for how this data should be presented. Before PO-02 enters sprint planning (gate: 6+ months AI journals, ~Oct 2026), a UX spec should be prepared to enable accurate scope definition at sprint planning.

**Scope**
- Define the display patterns for journal theme analysis (list view? heatmap? timeline?)
- Specify how patterns are surfaced: by entry count, by theme frequency, by outcome correlation
- Define empty state and gate-not-met state (< 6 months of journals)
- Produce a canonical frontend spec for the Journal Pattern Recognition UI component

**Acceptance Criteria**
- Frontend spec document produced: data display patterns, empty states, component architecture
- Spec reviewed and signed off by Head of UX & Design and Frontend Specs & UX Documentation Owner
- Gate: PMO Lead confirms PO-02 sprint planning is imminent before this story begins

---

### BLG-OPS-61 — BLG-OPS-13 v5.1–v5.4 endpoint baseline extension
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260610-01 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.5

**Problem**
BLG-OPS-60 (completed v5.4) added v5.3 endpoints to api_performance_baseline.md. However, v5.1 and v5.2 endpoints (POST /digest/si05/send, GET /portfolio/paper-positions enhancements, new v5.2 routes from BLG-SPEC-49–52) were not included. BLG-OPS-13 targets v2.8–v4.6 endpoints; BLG-OPS-61 closes the v5.1–v5.4 gap.

**Scope**
- Identify all new routes added in v5.1 and v5.2 not yet in api_performance_baseline.md
- Run p50/p95 latency measurements against staging
- Add entries to api_performance_baseline.md

**Acceptance Criteria**
- All v5.1/v5.2 new endpoints have latency entries in the baseline document
- Consistent with existing measurement methodology
- Infrastructure & Operations Owner sign-off

---

### BLG-OPS-71 — System threat model document
**Priority:** P2 (Medium)
**Type:** Operations / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260304-01 (rejected_but_strong.md) — revival triggered by strategic review 2026-06-18; original rejection condition (no production-scale external exposure) no longer holds; system now handles real position data, stop levels, P&L, Alpaca API credentials, Anthropic/Gemini billing keys, and Telegram bot tokens across staging + production
**Effort:** S (~1 day)
**Provisional-Target:** v6.0

**Problem**
No formal threat model exists. The system handles high-sensitivity financial data (positions, stop levels, P&L) and multiple third-party API credentials with billing exposure (Alpaca, Anthropic, Gemini, Telegram). Current security controls (API key auth on endpoints, CSP, CI secret scanning) were added reactively. A formal threat model identifies attack surfaces and data sensitivity levels in one place — producing a prioritised gap list before an incident forces it.

**Scope**
- Identify attack surfaces: endpoint auth coverage, Supabase access controls, Render environment variable exposure, Telegram webhook, Alpaca paper trading credentials, AI API keys
- Data sensitivity classification: position data (HIGH), stop levels (HIGH), P&L (HIGH), API keys (CRITICAL), user preferences (MEDIUM)
- Threat actors: external web attacker, compromised dependency, accidental exposure
- Document existing mitigations already in place (API key auth, CSP, CI secret scanning gate)
- Identify gaps; file a BLG-OPS or BLG-SPEC item for each gap discovered
- Output: `docs/security/threat_model.md`

**Acceptance Criteria**
- `docs/security/threat_model.md` produced covering all attack surfaces, data classifications, threat actors, current mitigations, and identified gaps
- Any gaps produce separate BLG items before sign-off
- Reviewed and signed off by Cybersecurity & Trust Lead and Infrastructure & Operations Owner

---

### BLG-SPEC-56 — Arc 4 API contract pre-authoring (PO-02/03/04)
**Priority:** P3 (Low)
**Type:** Spec / Pre-authoring
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (pre-work before PO-02 gate ~2026-10)

**Problem**
PO-02 (journal pattern recognition), PO-03 (behavioural error taxonomy), and PO-04 (reflection/outcome correlation) are currently gate-blocked (~2026-10). However, the API contract surface for these features can be pre-authored now, reducing execution risk and spec bottlenecks when the gate clears. Pre-authoring allows the Specs team to identify ambiguities, surface §13 questions, and establish endpoint naming conventions before sprint planning pressure exists.

**Scope**
- Draft API contract stub files for PO-02, PO-03, PO-04 feature endpoints in `docs/specs/api_contracts/`
- Flag any §13 boundary questions for BLG-SPEC-35 (§13 pre-assessment, P1, active)
- No implementation; contract stubs only

**Acceptance Criteria**
- Stub contract files exist for PO-02, PO-03, PO-04 endpoint groups in `docs/specs/api_contracts/`
- Each stub includes at minimum: endpoint path, HTTP method, brief description, key request/response fields
- BLG-SPEC-35 §13 pre-assessment reviewed or updated if new boundary questions arise

---

### BLG-SPEC-57 — Data model v3 pre-definition for Arc 4 journal intelligence
**Priority:** P3 (Low)
**Type:** Spec / Pre-authoring
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260619-02 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (pre-work before PO-02 gate ~2026-10)

**Problem**
Arc 4 journal intelligence (PO-02/03/04) will require data model changes. Pre-defining the schema additions now (while the architecture is in working memory post-Arc 3 delivery) reduces execution risk and produces a migration plan that can be reviewed before sprint planning pressure exists.

**Scope**
- Define data model additions for PO-02/03/04 features (new tables or columns for pattern recognition, error taxonomy, outcome correlation)
- Document as a pre-definition document in `docs/specs/` or `docs/data_models/`
- No migration SQL; schema design only

**Acceptance Criteria**
- Data model pre-definition document produced covering Arc 4 schema additions
- BLG-SPEC-56 Arc 4 API contracts reference the pre-defined model where applicable
- Reviewed by Head of Specs Team and Infrastructure & Operations Owner

---

### BLG-SPEC-58 — Dashboard homepage visual hierarchy review post-v6.2
**Priority:** P3 (Low)
**Type:** UX Spec / Assessment
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
v6.2 added an AI daily briefing card to the dashboard homepage alongside existing portfolio summary, positions overview, and system status. The information architecture and visual hierarchy may no longer optimally match trader workflow priority. A rapid assessment before v6.3 scope is defined confirms the hierarchy is correct or surfaces actionable improvements.

**Scope**
- Review current dashboard homepage layout against trader workflow priority (morning review: briefing → positions → action)
- Assess visual weight, card ordering, and information density after AI briefing card addition
- Produce short findings note: "hierarchy confirmed" or list of priority-order or layout improvements
- File any actionable improvements as separate backlog items

**Acceptance Criteria**
- Assessment document produced covering visual hierarchy post-v6.2 dashboard changes
- Findings reviewed by Head of UX & Design and Product Owner
- Any improvements filed as separate backlog items with priority and effort estimates

---

### BLG-SPEC-59 — R-multiple cross-currency normalization specification
**Priority:** P2 (Medium)
**Type:** Spec / Documentation
**Owner:** Financial Reporting & Records Owner; Head of Specs Team
**Source:** IDEA-financial-reporting-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
R-multiple is a core trade evaluation metric. GBP-denominated positions have a different native currency from USD positions. The specification for how R-multiple is calculated and displayed for cross-currency positions is not documented. This gap is directly related to BLG-FE-79 (P1 R-multiple display bug) — fixing the display correctly requires a clear specification of cross-currency behaviour.

**Scope**
- Define R-multiple calculation behaviour for GBP/USD positions: native currency vs normalised currency
- Specify aggregate R-multiple behaviour (how GBP and USD R-multiples aggregate in portfolio-level views)
- Document "N/A" vs "0.00" vs empty rendering for trades with insufficient stop loss data
- Reviewed by Financial Reporting & Records Owner and Product Owner before BLG-FE-79 fix enters sprint

**Acceptance Criteria**
- Specification document produced covering per-trade and aggregate R-multiple cross-currency behaviour
- "Insufficient data" display contract specified
- Reviewed by Financial Reporting & Records Owner and Product Owner

---

### BLG-SPEC-60 — Trailing stop visual indicator frontend specification
**Priority:** P2 (Medium)
**Type:** Frontend Spec / UX
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-specs-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
v6.2 ships nightly trailing stop computation. The positions page shows current open positions but does not display the current trailing stop price or distance-to-stop. Users must recall the stop level from memory or refer to external records. A frontend specification for a visual stop indicator enables a future sprint to implement this without spec ambiguity.

**Scope**
- Define visual indicator design: where on the position row the stop price and distance-to-stop appear
- Define data source: trailing_stop field from positions endpoint (confirm field name and availability)
- Define display states: stop set (show price + distance), stop not set (show "Not set" or omit indicator)
- Reviewed by Head of UX & Design and Product Owner before implementation sprint

**Acceptance Criteria**
- Frontend specification document produced covering indicator placement, data source, and display states
- Reviewed by Head of UX & Design and Product Owner

---

### BLG-SPEC-61 — Trailing stop effectiveness metric definition
**Priority:** P2 (Medium)
**Type:** Spec / Metrics
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-20260626-01 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
v6.2 ships nightly trailing stop computation. There is no metric tracking whether computed trailing stop updates were acted upon (position adjusted) vs ignored (position held unchanged). Without this metric, it is impossible to evaluate the feature's impact on trading behaviour or demonstrate the ROI of the v6.2 trailing stop investment. Defining the metric now ensures data is captured from the first day of usage.

**Scope**
- Define metric: trailing_stop_action_rate = positions_adjusted_after_stop_update / positions_with_stop_update_computed
- Define data capture requirement: link trailing stop computation events to subsequent position adjustment events
- Document in `docs/specs/metrics_definitions.md` or equivalent
- Reviewed by Metrics Definitions & Analytics Owner, FinOps & Resource Architect, and Product Owner

**Acceptance Criteria**
- Metric definition document produced covering definition, data sources, and capture requirements
- Reviewed by Metrics Definitions & Analytics Owner and Product Owner

---

### BLG-QA-59 — Arc 4 E2E test strategy pre-design (PO-02/03/04)
**Priority:** P3 (Low)
**Type:** Quality Assurance / Pre-design
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (pre-work before PO-02 gate ~2026-10)

**Problem**
Arc 4 AI-driven features (PO-02/03/04) introduce Playwright test challenges not present in current arcs: AI response non-determinism, journal pattern recognition latency, cost implications of running AI calls in CI. Pre-designing the test strategy before sprint planning avoids last-minute patching of the CI pipeline during delivery.

**Scope**
- Define Playwright test strategy for Arc 4 features: which ACs require Playwright vs unit tests vs staging-only verification
- Define mocking approach for AI API calls in CI (extend existing mock harness)
- Document in `docs/specs/qa/` or `docs/operations/`

**Acceptance Criteria**
- Arc 4 E2E test strategy document produced
- Mocking approach for PO-02/03/04 AI calls defined and consistent with existing BLG-QA-37 Playwright mock strategy
- Reviewed by Director of Quality

---

### BLG-QA-61 — Review signals_scenarios.md against ST-01 signal sizing model changes
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner; Director of Quality
**Source:** v6.0 delivery verification (TSG-v60-01) — signals_scenarios.md listed in execution_state.json test_scenarios for EPIC-01 but not referenced as run in QA evidence; ST-01 removed cash-allocation model and replaced with risk-based sizing
**Effort:** XS (<1 hour)
**Provisional-Target:** v6.1 (before next sprint touching signal generation)

**Problem**
`docs/testing/signals_scenarios.md` documents broader signal domain scenarios. ST-01 (v6.0) removed the cash-allocation model for `suggested_shares` and replaced it with `size_position()` per strategy_rules.md §4.1. Any scenario in `signals_scenarios.md` that asserts a specific `suggested_shares` value based on the old cash-allocation formula (cash / n_signals) will now produce incorrect expected values. These scenarios were not run in v6.0 QA — `tests/test_signal_sizing.py` (new) covered the story-specific ACs, but broader domain regression via `signals_scenarios.md` was not confirmed.

**Acceptance Criteria**
- QA & Testing Owner reviews each scenario in `docs/testing/signals_scenarios.md` that references `suggested_shares`
- Any scenario with stale cash-allocation-based expected values is updated to reflect the risk-based formula output
- Confirmed "no changes needed" or updated scenarios committed before next sprint touching signal generation
- Review outcome noted in next sprint's QA evidence or as a backlog closure note

---

### BLG-OPS-72 — AI API cost model for Arc 4 journal intelligence features
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled (before Arc 4 sprint planning)

**Problem**
PO-02 (journal pattern recognition) and PO-03/04 will call the Anthropic or Gemini API for AI summarisation and pattern analysis. Current AI cost modelling (BLG-OPS-65, completed v5.6) covers the thesis generation feature only. Arc 4 AI features will process trade journal entries in volume — potentially 1 AI call per journal entry per user per week. Without a cost model, Arc 4 budget impact is unknown and could exceed the current $0.05–$0.15/month baseline significantly.

**Scope**
- Estimate API call volume for PO-02/03/04 features based on expected usage patterns
- Model monthly cost at current Anthropic/Gemini pricing tiers
- Identify cost controls (caching, batching, user limits) and their estimated savings
- Document as `docs/operations/arc4_ai_cost_model.md`

**Acceptance Criteria**
- Cost model document produced with estimated monthly AI API cost for Arc 4 features
- Cost controls identified and quantified
- Reviewed by FinOps & Resource Architect

---

### BLG-BE-37 — Database index audit for Arc 4 cross-table queries
**Priority:** P3 (Low)
**Type:** Backend Engineering / Performance
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-infra-ops-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled (before Arc 4 sprint planning)

**Problem**
Arc 4 (PO-02/03/04) will introduce cross-table queries joining trade_plans, red_flag_events, arc5_compliance_scores, and potentially new journal tables. The current index strategy was designed for Arc 1–3 query patterns. Without an audit, Arc 4 sprint delivery may encounter unexpected latency regressions on production Supabase once real data volumes are involved.

**Scope**
- Review current index coverage on trade_plans, red_flag_events, arc5_compliance_scores, ai_journal_summaries tables
- Model likely Arc 4 query patterns based on BLG-SPEC-56 pre-authored contracts
- Identify missing indexes; file BLG-OPS or BLG-BE items for each gap discovered
- Document in `docs/operations/` or `docs/data_models/`

**Acceptance Criteria**
- Index audit document produced covering Arc 4 query patterns
- Any missing indexes produce separate BLG items before sign-off
- Reviewed by Infrastructure & Operations Owner

---

### BLG-BE-38 — Sector Concentration: join ticker_universe for sector data
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Bug
**Owner:** Head of Backend Engineering
**Source:** User-reported 2026-06-23 — Sector Concentration panel shows all positions as "Unclassified"
**Effort:** XS (~2 hours)
**Provisional-Target:** Next available sprint

**Problem**
`GET /portfolio/sector-weights` fetches raw `positions` rows and reads `pos.get("sector")`, falling back to `"Unclassified"` when the field is absent. The `positions` table has no `sector` column — sector data lives in `ticker_universe` (columns `sector`, `industry`), which is populated at ticker-add time via yfinance. Because no join is made, every position shows as "Unclassified" regardless of what is stored in `ticker_universe`.

**Scope**
- In `backend/routers/portfolio_risk.py` `get_sector_weights()`: after fetching `raw_positions`, resolve each position's sector by looking up `(ticker, market)` in `ticker_universe`. Fall back to `"Unclassified"` only when the ticker is genuinely absent from the universe or has a NULL sector.
- Same fix should be applied to the concentration-status endpoint (`GET /portfolio/concentration-status`) which has the same `pos.get("sector")` pattern at line 240.
- No schema change required — `ticker_universe.sector` already exists.

**Acceptance Criteria**
- AC-01: Sector Concentration panel on Risk Dashboard shows correct sector tiles for open positions whose tickers exist in `ticker_universe` with a non-null sector
- AC-02: Positions whose ticker has no sector in `ticker_universe` still render as "Unclassified" (graceful fallback preserved)
- AC-03: `GET /portfolio/concentration-status` sector breach calculation also reflects correct sectors
- AC-04: No yfinance live-call added to the hot path — sector is read from `ticker_universe` only

---

### BLG-BE-39 — Fix AI journal summary on Trade History tab
**Priority:** P1 (High)
**Type:** Backend Engineering / Bug
**Owner:** Head of Backend Engineering
**Source:** User-reported — 2026-06-25
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.2

**Problem**
The AI journal summary feature on the Trade History tab does not work. Users expect an AI-generated summary of their journal notes for a given trade, but the feature is non-functional. This may be a broken endpoint, a failed Claude API call, a missing API key, or a silent error in ai_service.py's journal summarisation path.

**Scope**
- Reproduce and diagnose the failure in the AI journal summary endpoint
- Fix the root cause (endpoint error, AI service config, prompt construction, or response parsing)
- Confirm the summary generates and displays correctly on the Trade History tab

**Acceptance Criteria**
- AI journal summary generates successfully for trades with journal notes on the Trade History tab
- Error states are surfaced clearly to the user rather than silently failing
- No regression to other ai_service.py functionality

---

### BLG-GOV-134 — CI: inline OpenAPI drift detection for api_performance_baseline.md
**Priority:** P2 (Medium)
**Type:** Governance Process / CI
**Owner:** Head of Specs Team; PMO Lead
**Source:** IW-20260622-01 (IDEA-head-of-specs-20260622-01) — Promoted-Backlog STEP 4; rebalance 2026-06-22__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.1

**Problem**
BLG-OPS-73 (PATCH /trades/{trade_id}/costs missing from api_performance_baseline.md) revealed a systemic gap: when an endpoint is added to `docs/reference/openapi.yaml`, there is no CI check confirming a corresponding entry exists in `docs/operations/api_performance_baseline.md`. The execution_prompt.md v3.47 advisory is a reminder, not enforcement.

**Scope**
- Add a CI step (GitHub Actions workflow) that extracts endpoint paths from `openapi.yaml` and compares against entries in `api_performance_baseline.md`
- Output a warning (non-blocking advisory gate) listing any endpoints in openapi.yaml that have no baseline entry
- Does not block PR merge; surfaces as advisory annotation on PR

**Acceptance Criteria**
- CI workflow step runs on PRs that modify `openapi.yaml` or `api_performance_baseline.md`
- Step outputs a diff list of endpoints present in openapi.yaml but absent from baseline
- Advisory only — does not fail the CI run

---

### BLG-GOV-137 — API contract version tagging for all api_contracts documents
**Priority:** P3 (Low)
**Type:** Governance Process / Spec Quality
**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Source:** IDEA-head-of-specs-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Tooling assessment confirming version tagging adds drift detection value not already covered by `quality_gate.yml` OpenAPI validation.

**Problem**
API contract documents in `docs/specs/api_contracts/` do not carry a version field. When a contract is amended (endpoint added, field type changed), there is no audit trail of which version was in force when a sprint was planned. Version tagging creates a lightweight reference that enables contract consumers to identify changes.

**Scope**
- Add `version:` field to each api_contracts document (start at v1.0 for all existing docs)
- Define version bump rules: patch for additive changes, minor for breaking changes
- Update checklist for new endpoint authoring to include version bump step

**Acceptance Criteria**
- All api_contracts documents carry a `version:` field
- Version bump rules documented
- Gate condition verified before sprint planning

---

### BLG-GOV-138 — Sprint velocity trend alert in run_manifest (rolling 3-cycle drop)
**Priority:** P3 (Low)
**Type:** Governance Process / Metrics
**Owner:** PMO Lead; Infrastructure & Operations Owner
**Source:** IDEA-pmo-lead-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** velocity_metrics.md path discrepancy resolved (file currently at `claude/cycles/velocity_metrics.md` instead of `claude/roadmap/velocity_metrics.md` — see DL-057 friction items).

**Problem**
The roadmap_prompt.md reads velocity_metrics.md but does not auto-surface a warning when the rolling 3-cycle velocity falls below 0.90. PMO must manually compare values and raise the concern. An explicit alert rule in the run_manifest generation step ensures degrading velocity is visible without manual tracking.

**Scope**
- Add rule to roadmap_prompt.md STEP 1.1: if rolling 3-cycle average velocity < 0.90, surface "Velocity Trend Advisory" in run_manifest header
- Rule documents the threshold, current value, and whether the advisory is advisory or hard gate

**Acceptance Criteria**
- Rule added to roadmap_prompt.md per §6 governance checklist (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry)
- Gate condition (velocity_metrics.md path resolved) verified before sprint planning

---

### BLG-GOV-139 — Regression impact analysis at sprint planning
**Priority:** P3 (Low)
**Type:** Governance Process / Quality
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Tooling approach identified — cross-reference methodology between changed files and Playwright coverage map assessed (automated script vs manual checklist approach).

**Problem**
When sprint planning seals scope, there is no step to cross-reference the changed files against existing Playwright coverage. A regression could be introduced in a file that has Playwright coverage but whose coverage is not triggered by the specific code path being changed. A lightweight impact analysis would surface this risk at planning time.

**Scope**
- Define methodology: compare sprint story file scope against `tests/e2e/` coverage map
- Produce a "coverage gap report" template: stories × files × test coverage status
- Integrate as an advisory step in sprint_planning_prompt.md STEP 3 or STEP 4

**Acceptance Criteria**
- Methodology document produced; approach decision (automated vs manual) recorded
- Gate condition verified before sprint planning entry
- If integrated into sprint_planning_prompt.md: all §6 governance checklist steps completed

---

### BLG-GOV-140 — AI chat advisory §13 quarterly self-audit checklist
**Priority:** P2 (Medium)
**Type:** Governance Process / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner; AI Compliance & Governance Officer
**Source:** IDEA-strategy-owner-20260626-02 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Gate criteria:** First review due 2026-09-24 (90 days post-v6.2 ship 2026-06-25). Quarterly cadence thereafter.

**Problem**
v6.2 AI chat advisor and daily briefing are now live. §13 requires AI advisory outputs to remain advisory-only and not cross into automated decision-making. Periodic self-audit confirms this boundary is maintained as prompts and response handling evolve. Without a scheduled review, §13 compliance depends on individual vigilance rather than a governed cadence.

**Scope**
- Author §13 self-audit checklist document covering: output advisory language confirmation, no-automated-action verification, disclaimer visibility check, prompt injection risk review
- Schedule first review 2026-09-24; quarterly cadence thereafter
- Owner: Strategy Rules & System Intent Owner; co-reviewer: AI Compliance & Governance Officer

**Acceptance Criteria**
- Checklist document produced and filed
- First review date scheduled (2026-09-24)
- Product Owner and Strategy Rules owner sign-off

---

### BLG-GOV-141 — AI model output logging completeness audit
**Priority:** P2 (Medium)
**Type:** Governance Process / §13 Compliance
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Source:** IDEA-ai-compliance-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Gate criteria:** Schedule within 90 days of v6.2 ship (by 2026-09-24).

**Problem**
v6.2 AI features (briefing, chat) should be logging all AI responses with model ID, prompt hash, and response length per AI governance policy. A completeness audit verifies the logging is in place and complete. Without this audit, log completeness is assumed rather than verified.

**Scope**
- Review claude_audit_log (or equivalent) for completeness: all POST /ai/daily-briefing and POST /ai/chat responses logged
- Verify fields: model_id, prompt_hash, response_length, timestamp
- If gaps found: file remediation items
- Schedule review by 2026-09-24

**Acceptance Criteria**
- Audit completed before 2026-09-24
- Logging completeness confirmed or gaps filed as remediation backlog items
- AI Compliance Officer sign-off

---

### BLG-GOV-142 — AI feature ROI assessment at 3-month post-ship mark
**Priority:** P2 (Medium)
**Type:** Governance Process / Value Assessment
**Owner:** Challenger; FinOps & Resource Architect; Product Owner
**Source:** IDEA-challenger-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** 2026-09-24 (90 days post-v6.2 ship). Assess: adoption rate of AI briefing and chat features, cost per use (Anthropic API cost / sessions), and whether usage data justifies continued investment.

**Problem**
v6.2 AI features have a per-use cost (Anthropic API call for each briefing and chat interaction). Without a formal ROI assessment at 3 months, there is no trigger to reconsider the feature investment if adoption is low or costs are disproportionate. The assessment is a formal governance checkpoint, not a presumption of cancellation.

**Scope**
- Assess: AI briefing usage rate (sessions/week), AI chat usage rate (questions/week), cost-per-session
- Compare against: value hypothesis from v6.2 release planning (trader intelligence value)
- Output: continue / sunset / modify recommendation with rationale
- Product Owner decision authority

**Acceptance Criteria**
- Assessment document produced by 2026-09-24
- Recommendation with rationale produced
- Product Owner decision recorded

---

### BLG-GOV-143 — OpenAPI completeness validation in CI (endpoint count reconciliation)
**Priority:** P3 (Low)
**Type:** Governance Process / CI
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Coverage methodology assessment confirming this complements (not duplicates) the existing OpenAPI drift detection in `quality_gate.yml`.

**Problem**
The existing `quality_gate.yml` drift detection checks `openapi.yaml` for new endpoints mentioned in contract files. BLG-GOV-134 adds advisory CI annotation. This item proposes a complementary check: validate that `openapi.yaml` covers 100% of routes in `backend/routers/`. These are distinct checks (forward vs backward coverage). Gate: confirm no duplication before implementing.

**Scope**
- Assess current coverage gap between quality_gate.yml (contract → openapi) and a hypothetical route scan (routes → openapi)
- If gap confirmed: author CI step to scan `backend/routers/` for `@router.[get|post|put|delete]` and cross-reference against openapi.yaml paths
- Gate condition assessment first; CI implementation only if gap confirmed

**Acceptance Criteria**
- Coverage gap assessment document produced
- If gap confirmed: CI step implemented as advisory (non-blocking, analogous to BLG-GOV-134)
- Gate condition verified before implementation

---

### BLG-GOV-144 — Agent role charter annual review schedule
**Priority:** P3 (Low)
**Type:** Governance Process / HR
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Time-gated — first review due 2027-06-26 (annual cadence from first filing).

**Problem**
Agent role charter files (`claude/agents/*.md`) define role responsibilities and decision authorities. As the governance system evolves, role definitions may become stale. Without a scheduled review cadence, charter drift accumulates silently. An annual review ensures each role definition remains current.

**Scope**
- Author an annual review procedure for all `claude/agents/*.md` charter files
- Schedule first review: 2027-06-26
- Procedure: review each charter for accuracy; propose amendments through Head of Specs Team; record in prompt_change_log.md

**Acceptance Criteria**
- Annual review procedure documented
- First review date: 2027-06-26 recorded
- Director of HR sign-off

---

### BLG-GOV-145 — Database connection pool sizing review for AI endpoints
**Priority:** P3 (Low)
**Type:** Governance Process / Operations Assessment
**Owner:** Head of Engineering; Infrastructure & Operations Owner
**Source:** IDEA-head-of-engineering-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** 30+ days AI endpoint usage observation post-v6.2 ship (by 2026-07-25). v6.2 AI endpoints make additional DB reads; pool sizing should be reviewed under real load.

**Problem**
v6.2 added POST /ai/daily-briefing and POST /ai/chat, both of which read from the database (portfolio state, trade history for context). Supavisor connection pool configuration was set before AI endpoints existed. Under sustained AI endpoint load, the pool may be undersized. A review at 30 days confirms the pool is sized correctly or identifies adjustment needed.

**Scope**
- Review current Supavisor pool configuration (connection count, timeout settings)
- Cross-reference with AI endpoint DB query volume (from logs or monitoring)
- Identify whether pool size adjustment is warranted
- Document findings; file implementation item if adjustment needed

**Acceptance Criteria**
- Pool configuration review document produced
- Findings: "no change needed" or specific adjustment filed as a separate item
- Gate condition (30+ days usage) verified before review commences

---

### BLG-GOV-146 — AI response injection risk assessment
**Priority:** P1 (High)
**Type:** Governance Process / Security
**Owner:** Cybersecurity & Trust Lead; AI Compliance & Governance Officer
**Source:** IDEA-cybersecurity-20260626-01 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
v6.2 AI chat and daily briefing features consume external data (market data, strategy rules, trade history) as context for Anthropic API calls. A threat model question: can a malicious actor craft market data API responses or strategy_rules.md content that causes the AI output to produce misleading trading advice? This threat category was not covered by the SRB-v1.7 §13 design gate review. A formal threat model assessment is time-sensitive for a live production AI system.

**Scope**
- Enumerate external data inputs to the AI prompt construction pipeline (POST /ai/daily-briefing and POST /ai/chat context assembly)
- For each input: assess injection risk (can this input contain content that changes advisory output in ways the user would not expect?)
- Document: accepted risks, mitigations, and any remediation items

**Acceptance Criteria**
- Threat model document produced covering all external data inputs to the AI pipeline
- Risk classification per input: accepted / mitigated / open
- Open risks filed as separate backlog items
- Cybersecurity & Trust Lead and AI Compliance Officer sign-off

---

### BLG-GOV-147 — AI feature advisory disclaimer visibility assessment
**Priority:** P2 (Medium)
**Type:** Governance Process / §13 Compliance
**Owner:** AI Compliance & Governance Officer; Head of UX & Design
**Source:** IDEA-ai-compliance-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (<0.5 day)
**Provisional-Target:** v6.3

**Problem**
§13 requires AI advisory disclaimers to be prominently visible on all AI outputs. v6.2 shipped with the assumption that disclaimers were properly implemented. Playwright spec SC-AI-01 confirms the disclaimer is rendered, but does not verify prominence (size, contrast, position, ability to dismiss). A visual assessment confirms §13 compliance at the presentation layer.

**Scope**
- Visual assessment of AI daily briefing and AI chat disclaimer display: font size, colour contrast, position relative to AI output, dismissal behaviour (if any)
- Confirm disclaimer is visible on first render without scrolling
- If gaps found: file remediation items targeting v6.3

**Acceptance Criteria**
- Visual assessment completed and documented
- Confirmation: "disclaimer prominent and compliant" OR remediation items filed
- AI Compliance Officer and Head of UX & Design sign-off

---

### BLG-GOV-148 — API contract review checklist for AI advisory endpoints
**Priority:** P2 (Medium)
**Type:** Governance Process / Spec Quality
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
API contracts for AI advisory endpoints (POST /ai/daily-briefing, POST /ai/chat) require §13 boundary confirmation in addition to standard endpoint documentation. No standardised checklist exists for this confirmation step. Without a checklist, §13 compliance review quality depends on the individual contract author's knowledge of §13 requirements.

**Scope**
- Author a §13 boundary confirmation checklist for AI advisory endpoint contracts: advisory-only response structure, no automated action fields in response, disclaimer presence, rate limiting documented, audit logging documented
- Apply checklist retroactively to existing v6.2 AI endpoint contracts (POST /ai/daily-briefing, POST /ai/chat)
- Integrate checklist into the API contract authoring procedure

**Acceptance Criteria**
- Checklist document produced and filed in `docs/specs/api_contracts/`
- Checklist applied to existing v6.2 AI endpoint contracts; gaps (if any) filed as remediation items
- API Contracts Owner and Head of Specs Team sign-off

---

### BLG-GOV-149 — AI response caching evaluation for morning briefing
**Priority:** P3 (Low)
**Type:** Governance Process / Architecture Assessment
**Owner:** Backend Engineering Patterns Owner; FinOps & Resource Architect
**Source:** IDEA-backend-engineering-20260626-01 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
POST /ai/daily-briefing makes an Anthropic API call on every request. If the same briefing is requested multiple times in the same trading day, each call incurs API cost and latency. A caching evaluation assesses whether same-day caching is technically feasible and whether the staleness risk (briefing should reflect the day's market data) outweighs the cost benefit.

**Scope**
- Evaluate caching feasibility: cache key options (date, user, market open/close state), cache invalidation triggers
- Assess staleness risk: how often does market data change in a way that would materially change the briefing during a trading day?
- Produce evaluation document: recommend cache (with approach) or no-cache (with rationale)
- No implementation commitment; evaluation output only

**Acceptance Criteria**
- Evaluation document produced covering cache key design, staleness risk, and cost-benefit analysis
- Recommendation: cache / no-cache with rationale
- Backend Engineering Owner and FinOps sign-off

---

### BLG-SEC-01 — Sanitise context_opts.ticker before system prompt injection (POST /ai/chat)
**Priority:** P2 (Medium)
**Type:** Security / Input Validation
**Owner:** Cybersecurity & Trust Lead; Backend Engineering Patterns Owner
**Source:** ST-04 open risk — AI injection risk assessment v1.0 (2026-06-29)
**Effort:** XS (<0.25 day)
**Provisional-Target:** v6.4

**Problem**
`context_opts.ticker` from the request body is interpolated directly into the `ai_chat()` system prompt f-string with no sanitization. A value containing newlines followed by instruction text (e.g. `"AAPL\n\nIgnore all previous instructions..."`) is injected into the system prompt verbatim, elevating the attacker's payload to system-prompt authority level. Attacker must be authenticated.

**Scope**
- Validate `context_opts.ticker` at the router layer: strip or reject values containing `\n`, `\r`, or characters outside `[A-Z0-9.:/-]`, max 20 characters
- Return HTTP 422 with descriptive error if ticker fails validation

**Acceptance Criteria**
- `context_opts.ticker` validated before insertion into system prompt
- Strings with newlines or injection characters rejected with HTTP 422
- Unit test added for validation logic
- Cybersecurity & Trust Lead sign-off

---

### BLG-SEC-02 — Validate ticker/market strings at signal write time (screener pipeline)
**Priority:** P3 (Low)
**Type:** Security / Input Validation
**Owner:** Cybersecurity & Trust Lead; Backend Engineering Patterns Owner
**Source:** ST-04 open risk — AI injection risk assessment v1.0 (2026-06-29)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.4

**Problem**
Signal ticker and market strings stored in the `signals` table are interpolated into AI prompts for both `POST /ai/daily-briefing` and `POST /ai/chat`. If the screener's external data source (index list, CSV, screener API) provides crafted ticker values containing newlines or injection payloads, those propagate to the AI prompt. No validation is applied at signal write time.

**Scope**
- Add ticker/market validation at signal write/import boundary
- Strip non-alphanumeric characters (allow `.`, `-`, `/`, `:` for international tickers, max 12 chars)
- Review existing signals in DB for anomalous values and document findings

**Acceptance Criteria**
- Signal write path validates ticker and market strings
- Existing signals reviewed; anomalous values documented or cleaned
- Cybersecurity & Trust Lead sign-off

---

### BLG-QA-63 — Automated accessibility testing (axe-core) in Playwright CI
**Priority:** P3 (Low)
**Type:** QA / Accessibility
**Owner:** Director of Quality; Head of Frontend Engineering
**Source:** IDEA-director-of-quality-20260619-02 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate:** Arc 5 fully complete (all SI features shipped) — accessibility testing added after frontend feature set stabilises

**Problem**
The Playwright E2E suite provides functional coverage but no accessibility validation. axe-core (via @axe-core/playwright) can be added to the existing Playwright setup to surface WCAG 2.1 AA violations in CI without blocking test runs.

**Scope**
- Install @axe-core/playwright
- Add a dedicated accessibility spec (tests/e2e/accessibility.spec.js) that visits each major page (Dashboard, Positions, Signals, Screener, Watchlist, Risk, Research, Reports, SystemStatus) and runs axe analysis
- Report violations as CI warnings (non-blocking initially); convert to hard failure after a clean baseline is established

**Acceptance Criteria**
- AC-01: axe-core runs on all major pages in CI (advisory, non-blocking)
- AC-02: Zero critical (level A) violations on any page at time of implementation
- AC-03: Violation report surfaced as CI annotation on PRs

---

### BLG-QA-64 — Fix 12 dark spec files surfaced by Playwright glob discovery
**Priority:** P2 (Medium)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality; Head of Frontend Engineering
**Source:** ST-13 (EPIC-03, v6.2) — glob discovery surfaced 12 pre-existing spec files that were excluded from the old explicit playwright.yml list. Identified 2026-06-25.
**Effort:** M (~1 day — each spec needs investigation and either fix or deletion)
**Provisional-Target:** v6.3
**Gate:** None

**Problem**
ST-13 replaced the explicit 26-file spec list in `playwright.yml` with `npx playwright test` (auto-discovery via `playwright.config.js` `testDir`). This surfaced 12 spec files that existed in `tests/e2e/` but were never included in CI. All 12 are failing — likely due to UI text mismatches (component text evolved after spec was written) or pending feature implementations.

Currently excluded via `testIgnore` in `playwright.config.js`:
- arc5-compliance-section.spec.js
- entry-checklist.spec.js
- gate-progress.spec.js
- paper-account.spec.js
- plan-vs-reality.spec.js
- pre-entry-panel-badge.spec.js
- red-flag-journal.spec.js
- sector-heatmap.spec.js
- si01-si03-integration.spec.js
- si05-digest-delivery.spec.js
- signals-add-to-watchlist.spec.js
- signals-allocation-insufficient.spec.js

**Scope**
For each spec file above: investigate failure cause, fix assertions to match current UI/API, remove from `testIgnore` in `playwright.config.js`. Delete any spec that tests a feature not yet implemented (refile as spec debt in appropriate epic).

**Acceptance Criteria**
- AC-01: All 12 spec files removed from `testIgnore` in `playwright.config.js`
- AC-02: All assertions pass in CI without modification to application source
- AC-03: `playwright.config.js` `testIgnore` array is empty or removed

---

### BLG-QA-65 — Nightly stop computation CI simulation tests
**Priority:** P1 (High)
**Type:** QA / Test Coverage
**Owner:** QA Lead; Backend Engineering Patterns Owner
**Source:** IDEA-qa-lead-20260626-01 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~1 day)
**Provisional-Target:** v6.3

**Problem**
v6.2 introduced nightly computation of trailing stops, rebalance exits, and inverse-vol position sizing. These computations run on a schedule (no on-demand CI trigger) and have zero automated test coverage. A silent regression in any of these computations would affect production trailing stop levels without any CI alarm. A fixture-based CI simulation detects regressions before they reach production.

**Scope**
- Author fixture dataset representing known portfolio state (positions with stop history, price data)
- Run trailing stop computation, rebalance exit detection, and inv-vol sizing computation against fixtures
- Assert computed outputs match expected values
- Register tests in CI to run on any change to the nightly computation services

**Acceptance Criteria**
- AC-01: Trailing stop computation test passes against fixture dataset
- AC-02: Rebalance exit detection test passes against fixture dataset
- AC-03: Inverse-vol sizing computation test passes against fixture dataset
- AC-04: All tests run in CI on changes to affected services
- AC-05: Fixture update procedure documented

---

### BLG-QA-66 — Strategy signal regression test specification
**Priority:** P1 (High)
**Type:** QA / Spec
**Owner:** QA & Testing Owner; Director of Quality
**Source:** IDEA-qa-testing-20260626-01 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
BLG-QA-65 (nightly stop CI simulation) requires a formal specification document defining: which scenarios the fixture dataset must cover, what the expected outputs are, and how fixture data should be maintained. Without a specification, the CI simulation tests may cover an incomplete scenario set or drift from production behaviour.

**Scope**
- Define scenario coverage requirements for BLG-QA-65: which portfolio states must be represented (trailing stop active, no stop, position at rebalance threshold, inv-vol position, mixed)
- Define expected output format and tolerance ranges
- Define fixture maintenance procedure (when and how to update fixtures after strategy_rules.md changes)
- Document filed as `docs/specs/qa/strategy_signal_regression_spec.md`

**Acceptance Criteria**
- Specification document produced covering all scenario coverage requirements
- Expected output formats and tolerances defined
- Fixture maintenance procedure documented
- Director of Quality and QA Lead sign-off

---

### BLG-QA-67 — AI chat response schema validation tests
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** QA Lead; API Contracts & Documentation Owner
**Source:** IDEA-qa-lead-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
POST /ai/chat must return advisory-only structured responses conforming to the expected JSON schema. No test currently validates the response schema or confirms that directive language patterns are absent. Schema drift or an Anthropic SDK update could silently change response structure without any CI alarm.

**Scope**
- Define expected POST /ai/chat response schema (fields, types, optional fields)
- Author schema validation tests: response conforms to expected schema, advisory-only language constraint confirmed
- Tests registered in CI alongside existing API endpoint tests in `backend/routers/test.py`

**Acceptance Criteria**
- AC-01: Response schema validation test passes in CI
- AC-02: Advisory-only constraint test (no directive language patterns) passes in CI
- AC-03: Tests registered in `backend/routers/test.py` or equivalent CI test entry point

---

### BLG-QA-68 — §13 boundary test suite for AI advisory endpoints
**Priority:** P2 (Medium)
**Type:** QA / Spec
**Owner:** QA & Testing Owner; AI Compliance & Governance Officer
**Source:** IDEA-qa-testing-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
§13 compliance for AI advisory endpoints depends on consistent enforcement of advisory-only output constraints across all AI endpoints. No document defines the full set of §13 boundary test scenarios for POST /ai/daily-briefing, POST /ai/chat, and any future AI endpoints. Without this document, §13 compliance testing is inconsistent and new AI endpoints may not be assessed against the same criteria.

**Scope**
- Author §13 boundary test scenario document: enumerate all AI advisory endpoints; for each, define the §13 compliance test scenarios (advisory language confirmation, no automated action, disclaimer rendered, no financial instrument recommendations)
- Document applies to current endpoints and serves as the template for future AI endpoint §13 test scenarios
- Filed as `docs/specs/qa/ai_s13_boundary_test_suite.md`

**Acceptance Criteria**
- §13 boundary test scenario document produced covering all current AI endpoints
- Scenarios cover: advisory-only language, no automated-action fields, disclaimer visibility, no specific instrument recommendations
- AI Compliance Officer and QA & Testing Owner sign-off

---

### BLG-OPS-74 — Log Anthropic API token usage and cost per morning briefing call
**Priority:** P3 (Low)
**Type:** Operations / Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IW-20260622-01 (IDEA-finops-20260622-01) — Promoted-Backlog STEP 4; rebalance 2026-06-22__scheduled
**Effort:** S (<0.5 day)
**Provisional-Target:** v6.1

**Problem**
The Trader Morning Briefing (BLG-FEAT-46, shipped v6.0) calls the Claude API each time it generates a briefing. Token usage and estimated cost per call are not tracked. As briefing frequency or complexity grows, cost visibility is needed for informed FinOps decisions.

**Scope**
- Log token usage (prompt_tokens, completion_tokens) and estimated cost per morning briefing generation call
- Follow the established `claude_audit_log` pattern (from Gemini wiring v3.8); extend or add a parallel log entry for Claude briefing calls
- Surface aggregate monthly cost in `/system-status` or the existing AI cost review mechanism

**Acceptance Criteria**
- Each morning briefing API call produces a log entry with token counts and estimated cost
- Log entries are queryable for weekly/monthly cost aggregation
- GET /system-status or equivalent surfaces cumulative briefing cost for the current month

---

### BLG-OPS-76 — Enhanced health check with external dependency verification
**Priority:** P3 (Low)
**Type:** Operations / Observability
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260619-02 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate:** BLG-OPS-25 (automated staging smoke test) complete AND ≥3 external dependency failures observed in production logs

**Problem**
GET /health returns only internal service health (database connectivity, scheduler status). External dependency status (Alpaca API reachability, Anthropic API reachability, Yahoo Finance fallback) is not surfaced in the health check, making degraded-run detection reactive rather than proactive.

**Scope**
- Add optional `?extended=true` query param to GET /health
- Extended check: attempt lightweight connectivity test for each external dependency (Alpaca: GET /v2/clock; Anthropic: no-op; Yahoo Finance: HEAD check)
- Return dependency status map in health response
- No latency regression on default (non-extended) health check

**Acceptance Criteria**
- AC-01: GET /health?extended=true returns a `dependencies` object with status for each external dependency
- AC-02: GET /health (no param) remains unchanged in response shape and latency
- AC-03: Degraded dependency status visible in `/system-status` page

---

### BLG-OPS-77 — Data provider diversity risk assessment and failover strategy
**Priority:** P3 (Low)
**Type:** Operations / Risk
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Source:** IDEA-challenger-20260619-01 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate:** BLG-OPS-71 (system threat model) complete — data provider risk will be enumerated in the threat model

**Problem**
All market data (OHLCV, signals, news) is sourced exclusively from Alpaca and Yahoo Finance. No documented failover strategy exists for a scenario where either provider becomes unavailable for an extended period. The risk has been accepted at current scale but has not been formally assessed.

**Scope**
- Produce a data provider risk assessment document (docs/operations/data_provider_risk_assessment.md): enumerate current dependencies, failure modes, estimated impact per provider loss, and mitigation options
- Identify any quick-win failover paths (e.g. Yahoo Finance as sole fallback if Alpaca unavailable)
- Document accepted risk and conditions under which a more robust failover should be re-evaluated

**Acceptance Criteria**
- AC-01: data_provider_risk_assessment.md produced covering all active external data providers
- AC-02: Failure modes and impact documented per provider
- AC-03: Accepted risk statement signed off by Infrastructure & Operations Owner and FinOps & Resource Architect

---

### BLG-OPS-78 — Measure live latency for POST /ai/daily-briefing and POST /ai/chat
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** Post-ship closure 2026-06-24__release-v6.2 — endpoint drift advisory; api_performance_baseline.md §22.3 timing run deferred
**Effort:** XS (<1 hour)
**Provisional-Target:** v6.3

**Problem**
`POST /ai/daily-briefing` and `POST /ai/chat` were registered in api_performance_baseline.md §22 during v6.2 with estimated latency characteristics (AI inference, claude-sonnet-4-6). Actual timing measurements were deferred until post-deployment to production. Without live p50/p95 measurements, the regression threshold from §22.2 ("p95 > 2× measured p95 triggers a review") cannot be established.

**Scope**
- Run minimum 5 authenticated warm requests against production for each endpoint
- Record p50/p95 using standard §19 methodology
- Update api_performance_baseline.md §22.3 with actual measurements
- Establish regression threshold: p95 > 2× measured p95

**Acceptance Criteria**
- AC-01: api_performance_baseline.md §22.3 populated with actual p50/p95 for both endpoints
- AC-02: Regression threshold documented per §22.2 formula

---

### BLG-OPS-79 — Background scheduler health monitoring endpoint
**Priority:** P2 (Medium)
**Type:** Operations / Monitoring
**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Source:** IDEA-infra-ops-20260622-01 — Promoted-Backlog (gate cleared: BLG-FEAT-46/47 shipped v6.2); rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Gate criteria:** v6.2 scheduler architecture reviewed and monitoring endpoint design specified. BLG-FEAT-46/47 shipped (gate event cleared 2026-06-25); new condition: architecture review before endpoint design.

**Problem**
v6.2 added a production background scheduler running nightly trailing stop computation, rebalance exits, and inverse-vol sizing. These computations run without any health monitoring endpoint. If the scheduler silently fails, there is no alert and no way to detect the failure from an external monitoring system. A health endpoint enables uptime monitoring and operational visibility.

**Scope**
- Design health monitoring endpoint: `GET /health/scheduler` returning last-run timestamps per job type, status (success/failure), and any error details from most recent run
- Integrate with existing `GET /health` endpoint or create separate scheduler health endpoint
- Review v6.2 scheduler architecture before endpoint design to confirm available data fields

**Acceptance Criteria**
- AC-01: `GET /health/scheduler` returns last-run status for each nightly computation job
- AC-02: Endpoint registered in `backend/routers/test.py` and `docs/reference/openapi.yaml`
- AC-03: Architecture review documented before implementation begins

---

### BLG-OPS-80 — Render deployment rollback procedure documentation
**Priority:** P3 (Low)
**Type:** Operations / Runbook
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** XS (<0.5 day)
**Provisional-Target:** v6.3

**Gate criteria:** None — documentation can be produced now.

**Problem**
There is no documented runbook for rolling back to the prior Render deployment version in case of a production incident. If a deployment causes a regression, the resolution depends on whoever is on call knowing the correct steps. A documented rollback procedure removes single-point-of-knowledge risk.

**Scope**
- Document Render deployment rollback procedure: navigate to Render dashboard, identify prior deploy version, initiate rollback, verify rollback succeeded
- Include: rollback decision criteria (what severity warrants immediate rollback vs fix-forward), estimated rollback time, how to verify the rollback deployed the correct version

**Acceptance Criteria**
- Rollback procedure document produced and filed in `docs/operations/`
- Document covers: rollback steps, decision criteria, verification steps
- Infrastructure & Operations Owner sign-off

---

### BLG-OPS-81 — AI endpoint per-endpoint rate limiting hardening
**Priority:** P1 (High)
**Type:** Operations / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Source:** IDEA-cybersecurity-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
POST /ai/daily-briefing and POST /ai/chat have no per-endpoint rate limiting. Both endpoints make Anthropic API calls on every request. A single automated abuse vector (web scraper, API probe, or broken client loop) could exhaust the monthly Anthropic API budget within minutes without any circuit-breaker. Rate limiting is a standard security control for API endpoints with external service cost implications.

**Scope**
- Implement per-endpoint rate limits: POST /ai/daily-briefing (~10 req/min/IP), POST /ai/chat (~30 req/min/IP)
- Return standard 429 Too Many Requests with Retry-After header
- Document rate limits in openapi.yaml and api_contracts
- Test: verify 429 returned after limit exceeded; verify Retry-After header is set

**Acceptance Criteria**
- AC-01: POST /ai/daily-briefing rate limit enforced (429 returned after limit exceeded)
- AC-02: POST /ai/chat rate limit enforced (429 returned after limit exceeded)
- AC-03: Retry-After header present in 429 responses
- AC-04: Rate limits documented in openapi.yaml and api_contracts
- AC-05: Endpoint test updated to cover 429 scenario

---

### BLG-FE-77 — Refactor `Watchlist.js` to ESLint compliance
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of Frontend Engineering
**Source:** ESLint hook run — pre-existing violations surfaced after eslint-plugin-playwright, eslint-plugin-no-comments, eslint-plugin-better-max-params installed — 2026-06-22
**Effort:** M (~1–2 days)
**Provisional-Target:** v6.1

**Problem**
`src/pages/Watchlist.js` has 16 pre-existing ESLint violations that were hidden because three required plugins were not installed. Now that the plugins are in place, the lint-feedback hook fires on every edit to this file, creating noise and discouraging changes. The primary violations are: `max-lines-per-function` (the `Watchlist` component body is 312 lines against a 50-line limit), multiple magic number literals (`200`, `220`, `5`, `60`, `1000`), and inline comments in state declarations. Zero violations were introduced by recent changes — all are pre-existing.

**Scope**
- Extract sub-components from `Watchlist.js`: `WatchlistTableRow`, `WatchlistNewsRow`, and inline badges are all candidates
- Replace magic number literals with named constants at the top of the file
- Remove inline comments; express intent through component and variable names instead
- Ensure all extracted components independently pass ESLint

**Acceptance Criteria**
- `npx eslint src/pages/Watchlist.js` exits 0 with no errors or warnings
- All extracted sub-components also pass ESLint clean
- Watchlist page renders and behaves identically to pre-refactor (no functional regression)
- Playwright E2E watchlist specs continue to pass

---

### BLG-FE-79 — Fix R-multiple not displaying on Reflection page
**Priority:** P1 (High)
**Type:** Frontend / Bug
**Owner:** Base44 Frontend Prompt Owner; Head of Backend Engineering
**Source:** User-reported — 2026-06-25
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.2

**Problem**
The Reflection page shows a dash ("—") for the R-multiple column across all tickers, rather than a calculated value. R-multiple is a core trade evaluation metric; its absence makes the Reflection page unreliable for post-trade review. The root cause may be either the backend not computing/returning the field, or the frontend not reading it correctly.

**Scope**
- Identify whether R-multiple is absent from the API response or null in the database
- Fix calculation or field mapping at the source (backend service or frontend display logic)
- Verify R-multiple renders correctly for all closed tickers on the Reflection page

**Acceptance Criteria**
- R-multiple is displayed as a numeric value for all closed trades with sufficient data on the Reflection page
- Trades with insufficient data (no stop loss recorded) show a clearly labelled "N/A" rather than a silent dash
- No regression to other Reflection page columns

---

### BLG-FE-80 — Morning briefing progressive disclosure (expand/collapse sections)
**Priority:** P2 (Medium)
**Type:** Frontend / UX Enhancement
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Source:** IDEA-base44-frontend-20260626-01 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Problem**
The AI daily briefing card (AiDailyBriefing.js, shipped v6.2) displays three content-dense sections: market context, signals, and chat prompt. All sections are always fully expanded. A user who has already read the market context and signals but wants to access the AI chat prompt must scroll past the full briefing content on every page load. Progressive disclosure (expand/collapse per section) reduces visual noise for repeat daily usage.

**Scope**
- Add expand/collapse toggle per section in AiDailyBriefing.js (market context, signals, chat prompt)
- Default state: all sections expanded (no UX regression for new users)
- Persist section collapse state to localStorage (collapsed sections stay collapsed on next page load)
- Version the localStorage key to handle section schema changes gracefully

**Acceptance Criteria**
- AC-01: Each section of the AI daily briefing has a visible expand/collapse toggle
- AC-02: Sections collapse and expand without losing content
- AC-03: Section state persists across page reloads via localStorage
- AC-04: Default state is all expanded (no UX regression)
- AC-05: Playwright: expand all → collapse market context → reload → verify market context still collapsed

---

*Release Slice v4.6 removed — cycle 2026-05-30__release-v4.6 closed 2026-05-31. Archived canonical home: claude/cycles/2026-05-30__release-v4.6/stage4_backlog_slice.md*

---

*Release Slice v4.8 removed — cycle 2026-06-01__release-v4.8 closed 2026-06-02. Archived canonical home: claude/cycles/2026-06-01__release-v4.8/stage4_backlog_slice.md*

---

*Release Slice v4.9 removed — cycle 2026-06-02__release-v4.9 closed 2026-06-02. Archived canonical home: claude/cycles/2026-06-02__release-v4.9/stage4_backlog_slice.md*

---

*Release Slice v5.0 removed — cycle 2026-06-03__release-v5.0 closed 2026-06-03. Archived canonical home: claude/cycles/2026-06-03__release-v5.0/stage4_backlog_slice.md*

---
*Release Slice v5.2 removed — cycle 2026-06-08__release-v5.2 closed 2026-06-08. Archived canonical home: claude/cycles/2026-06-08__release-v5.2/stage4_backlog_slice.md*

---

*Release Slice v5.3 removed — cycle 2026-06-08__release-v5.3 closed 2026-06-09. Archived canonical home: claude/cycles/2026-06-08__release-v5.3/stage4_backlog_slice.md*

---

*Release Slice v5.4 removed — cycle 2026-06-09__release-v5.4 closed 2026-06-10. Archived canonical home: claude/cycles/2026-06-09__release-v5.4/stage4_backlog_slice.md*

---

*Release Slice v5.5 removed — cycle 2026-06-10__release-v5.5 closed 2026-06-16. Archived canonical home: claude/cycles/2026-06-10__release-v5.5/stage4_backlog_slice.md*

---

*Release Slice v5.6 removed — cycle 2026-06-16__release-v5.6 closed 2026-06-16. Archived canonical home: claude/cycles/2026-06-16__release-v5.6/stage4_backlog_slice.md*

---

*Release Slice v5.8 removed — cycle 2026-06-17__release-v5.8 closed 2026-06-17. Archived canonical home: claude/cycles/2026-06-17__release-v5.8/stage4_backlog_slice.md*

*Release Slice v5.7 removed — cycle 2026-06-16__release-v5.7 closed 2026-06-17. Archived canonical home: claude/cycles/2026-06-16__release-v5.7/stage4_backlog_slice.md*

---

---

*Release Slice v5.9 removed — cycle 2026-06-17__release-v5.9 closed 2026-06-18. Archived canonical home: claude/cycles/2026-06-17__release-v5.9/stage4_backlog_slice.md*

*Release Slice v6.0 removed — cycle 2026-06-19__release-v6.0 closed 2026-06-22. Archived canonical home: claude/cycles/2026-06-19__release-v6.0/stage4_backlog_slice.md*

---

*Release Slice v6.1 removed — cycle 2026-06-22__release-v6.1 closed 2026-06-23. Archived canonical home: claude/cycles/2026-06-22__release-v6.1/stage4_backlog_slice.md*

---

*Release Slice v6.2 removed — cycle 2026-06-24__release-v6.2 closed 2026-06-25. Archived canonical home: claude/cycles/2026-06-24__release-v6.2/stage4_backlog_slice.md*

---

## Release Slice — v6.3 (2026-06-26__release-v6.3)

<!-- release-plan-marker: RP:v6.3:2026-06-26__release-v6.3 -->

**Canonical slice:** `claude/cycles/2026-06-26__release-v6.3/stage4_backlog_slice.md`

15 stories across 3 EPICs (8 firm, 7 conditional). See canonical slice for full acceptance criteria.

| ST-ID | BLG-ID | Description | EPIC | Type | Effort |
|-------|--------|-------------|------|------|--------|
| ST-01 | BLG-BE-39 | Fix AI journal summary on Trade History tab | EPIC-01 | Firm | S |
| ST-02 | BLG-FE-79 | Fix R-multiple not displaying on Reflection page | EPIC-01 | Firm | S |
| ST-03 | BLG-OPS-81 | AI endpoint per-endpoint rate limiting hardening | EPIC-01 | Firm | S |
| ST-04 | BLG-GOV-146 | AI response injection risk assessment | EPIC-01 | Firm | S |
| ST-05 | BLG-GOV-147 | AI feature advisory disclaimer visibility assessment | EPIC-01 | Conditional | S |
| ST-06 | BLG-GOV-148 | API contract review checklist for AI advisory endpoints | EPIC-01 | Conditional | S |
| ST-07 | BLG-QA-65 | Nightly stop computation CI simulation tests | EPIC-02 | Firm | S |
| ST-08 | BLG-QA-66 | Strategy signal regression test specification | EPIC-02 | Firm | S |
| ST-09 | BLG-QA-67 | AI chat response schema validation tests | EPIC-02 | Conditional | S |
| ST-10 | BLG-QA-68 | §13 boundary test suite for AI advisory endpoints | EPIC-02 | Conditional | S |
| ST-11 | BLG-FEAT-53 | Strategy Benchmark page: compare live trades against backtest | EPIC-03 | Firm | L |
| ST-12 | BLG-FE-80 | Morning briefing progressive disclosure (expand/collapse sections) | EPIC-03 | Firm | S |
| ST-13 | BLG-OPS-79 | Background scheduler health monitoring endpoint | EPIC-03 | Conditional | S |
| ST-14 | BLG-OPS-78 | Measure live latency for POST /ai/daily-briefing and POST /ai/chat | EPIC-03 | Conditional | XS |
| ST-15 | BLG-OPS-80 | Render deployment rollback procedure documentation | EPIC-03 | Conditional | XS |
