# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-06-17 (post-ship closure 2026-06-16__release-v5.7 — 8 items marked ✅ COMPLETE: BLG-FE-75, BLG-QA-56/57/58, BLG-OPS-66/67/68/69)
**Last rebalance:** 2026-06-09 (cycle 2026-06-09__scheduled — DL-041/042; IW skipped ≥20 open ideas; 8 new items; meta-review DUE conducted; v5.4 Now section added)

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
*v4.6 gate audit 2026-05-31 (ST-16 BLG-GOV-33): 6 closed trades total (trade_history WHERE pnl IS NOT NULL); 0 with linked trade_plans. Gate NOT MET. EPIC-02 deferred. 6th deferral (SI-02 Frontend also deferred). Advance when ≥20 closed trades with linked trade_plans confirmed.*
*v5.3 gate re-verification 2026-06-09 (OA-RP-01 / BLG-GOV-106): 6 closed trades (trade_history WHERE pnl IS NOT NULL); 11 total trades. Gate NOT MET. PT-04 remains parked. Next re-verification at v5.4 sprint planning.*
*v5.6 gate re-verification 2026-06-16 (ST-08 / BLG-GOV-106): **13 closed trades** (SELECT COUNT(*) FROM trade_history WHERE pnl IS NOT NULL — PO-provided data, 2026-06-16). Gate NOT MET (need 20; 7 more required). Trajectory: accelerating — 7 new closed trades in 7 days (vs prior ~0.5/month estimate). PT-04 remains parked. Next re-verification: when PO confirms 20+ closed trades.*

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

### BLG-FE-41 — Red Flag Journal visual design review
**Priority:** P3 (Low)
**Type:** Frontend / UX Design
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days design + spec)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-03 Red Flag Journal live ≥ 30 days (on/after 2026-06-21). **Not eligible for release planning or sprint planning before 2026-06-21.** Depends on BLG-FE-64 (pre-brief) completing first.

**Sprint history:** Planned as ST-02 (EPIC-01) in cycle 2026-06-17__release-v5.8; returned to backlog 2026-06-17 mid-sprint — PO-authorised deferral; gate date 2026-06-21 not yet reached.

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

### BLG-FE-57 — Pre-entry panel: show warning/fail count when collapsed
**Priority:** P3 (Low)
**Type:** Frontend / UX Improvement
**Owner:** Head of UX & Design
**Source:** docs/product/ux/pre_entry_panel_ux_assessment.md — candidate P2 — cycle 2026-05-31__release-v4.7 (ST-09)
**Effort:** XS (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
PreEntryValidationPanel collapses to header only with no visible indicator of warning/fail count. Traders scanning the Trade Plan form cannot determine if there are warnings without expanding the panel.

**Scope**
- When panel is collapsed and advisory status is `warn` or `fail`: show a count badge in the header ("2 warnings", "1 fail")
- Additive change — does not affect expanded panel behaviour

**Acceptance Criteria**
- Collapsed header shows count of warn/fail items when advisory status is warn or fail
- Count badge is not shown when all checks pass (no unnecessary visual clutter)
- Existing collapse/expand behaviour preserved

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

### BLG-FE-64 — BLG-FE-41 Red Flag Journal visual design review pre-brief
**Priority:** P2 (Medium)
**Type:** Frontend / UX Pre-work
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.2 (gate clears 2026-06-21 — 14 days)
**Displacement:** BLG-FE-27 (Nav bar redesign exploration, P3) deprioritised.

**Gate criteria:** SI-03 Red Flag Journal live ≥ 30 days (2026-06-21 — gate clears in 14 days from 2026-06-07).

**Sprint history:** Planned as ST-03 (EPIC-02) in cycle 2026-06-09__release-v5.4; returned to backlog 2026-06-10 — date gate (2026-06-21) not met at sprint close; PO-authorised deferral. Planned again as ST-11 (EPIC-04) in cycle 2026-06-10__release-v5.5; returned to backlog 2026-06-15 — gate date 2026-06-21 still not reached. Planned again as ST-03 (EPIC-01) in cycle 2026-06-16__release-v5.6; returned to backlog 2026-06-16 — gate date 2026-06-21 not yet cleared at planning time. Planned as ST-09 (EPIC-02) in cycle 2026-06-16__release-v5.7; returned to backlog 2026-06-17 — gate date 2026-06-21 not yet cleared at sprint close (4th deferral). Planned as ST-01 (EPIC-01) in cycle 2026-06-17__release-v5.8; returned to backlog 2026-06-17 mid-sprint — PO-authorised deferral; gate date 2026-06-21 still not reached at time of return (5th deferral). **Not eligible for release planning or sprint planning before 2026-06-21** (gate: SI-03 Red Flag Journal live ≥ 30 days from 2026-05-22).

**Problem**
BLG-FE-41 (Red Flag Journal visual design review) has a gate date of 2026-06-21. When the gate clears, sprint planning delay can be avoided if the design review brief is already prepared. The brief defines: scope (which aspects of RedFlagJournal.js are in scope for visual review), evaluation criteria, and deliverables from the review.

**Scope**
- Produce a design review brief for BLG-FE-41: define review scope (filters UX, severity visual hierarchy, event type colour coding, timeline vs list layout), evaluation criteria, and expected deliverable
- Input to BLG-FE-41 sprint planning when gate clears 2026-06-21
- Brief reviewed by Head of UX & Design

**Acceptance Criteria**
- Design review brief produced and reviewed before 2026-06-21
- Brief covers: scope definition, evaluation criteria, deliverable format
- Head of UX & Design sign-off on brief scope

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

### BLG-BE-34 — Trade count gate-monitoring view
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Infrastructure
**Owner:** Data Model & Domain Schema Owner; PMO Lead
**Source:** IDEA-data-model-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-BE-13 (screener result history table, P3, gate-conditional) deprioritised.

**Problem**
Multiple roadmap features are gated on trade count thresholds: PT-04 (20+ closed trades), SI-02 frontend (20+ closed trades with linked trade_plans), PS-01–PS-05 (50+ or 100+ trades). At each release planning cycle, the PMO Lead must manually query the production database to check gate conditions. A dedicated view or function standardises this check and prevents missed gate opportunities.

**Scope**
- Create a database view or PostgreSQL function: `get_gate_metrics()` returning: closed_trades_count (trade_history WHERE pnl IS NOT NULL), closed_trades_with_plans (trade_history WHERE plan_id IS NOT NULL AND pnl IS NOT NULL), active_positions_count, ai_journal_entry_count (if exists), oldest_trade_date, newest_trade_date
- Optional: expose as GET /portfolio/gate-metrics (read-only, admin-only endpoint) for automated gate checks at sprint planning
- Document view usage in release planning checklist

**Acceptance Criteria**
- Gate metrics view or function created and tested
- Returns all key gate condition inputs (closed_trades_count, with_plans_count at minimum)
- If endpoint added: registered in test.py and openapi.yaml per CLAUDE.md §2
- Data Model & Domain Schema Owner sign-off

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

### BLG-QA-34 — QA evidence file format audit
**Priority:** P3 (Low)
**Type:** QA / Governance
**Owner:** QA Lead; Director of Quality
**Source:** IDEA-qa-lead-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
QA evidence files (qa_evidence_EPIC-*.md) from v3.7–v4.0 were produced under evolving standards. PR template v1.2 (shipped v3.9) standardised the DoQ sign-off date field. A format audit confirms whether existing evidence files are consistent with the current standard, identifies format variations that complicate future audit (AUD-2026-05-21 scored QA reliability at 84). Narrow, bounded scope.

**Scope**
- Review QA evidence files from v3.7, v3.8, v3.9, and v4.0 cycles
- Check: header fields present, DoQ sign-off date present, sign-off block format consistent
- Findings documented (advisory only — sealed artefacts not modified retroactively)
- Inform any future QA evidence template updates

**Acceptance Criteria**
- All QA evidence files from v3.7–v4.0 reviewed
- Format inconsistencies documented
- Findings submitted to Director of Quality as advisory note

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

### BLG-QA-50 — Create formal regression test suite baseline document
**Priority:** P3 (Low)
**Type:** QA / Documentation
**Owner:** QA Lead; Director of Quality
**Source:** ST-15 (BLG-QA-48) — v5.2 regression baseline refresh identified absence of formal document
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
No formal regression test suite baseline document exists. The current test coverage is tracked ad hoc through `backend/routers/test.py` (endpoint smoke tests) and Playwright specs in `tests/e2e/`. Without a baseline document, there is no authoritative reference for which tests are in scope for regression, which features they cover, or when new test entries were added. This makes it difficult to verify regression coverage at delivery verification and during QA sign-off.

**Scope**
- Create a formal regression baseline document covering:
  - All `backend/routers/test.py` entries (endpoint smoke tests) with feature mapping
  - All Playwright spec files in `tests/e2e/` with scenario count and feature mapping
  - Version history: which tests were added at which release
- Document will serve as the authoritative regression scope reference for future sprints

**Acceptance Criteria**
- Regression baseline document created in docs/qa/ or docs/testing/
- All test.py entries mapped to features
- All Playwright specs listed with scenario count
- Director of Quality sign-off

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

### BLG-OPS-44 — DS-07 migration staging verification (v4.6 delivery)
**Priority:** P3 (Low)
**Type:** Operations / Staging Verification
**Owner:** Infrastructure & Operations Owner; Data Model & Domain Schema Owner
**Source:** v4.6 delivery verification — ST-01 AC-05 deferred to Phase 4 (staging-only AC)
**Effort:** XS (~0.5 hr)
**Provisional-Target:** v4.7

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-05, EPIC-03; ds07_migration_staging_verification.md produced; all 5 SI-02 columns confirmed; 3 indexes confirmed; Infrastructure & Operations Owner + Data Model & Domain Schema Owner sign-off)

**Problem**
ST-01 (DS-07 data migration) was verified by code review only in v4.6. AC-05 (staging verification) was pre-designated as staging-only and explicitly deferred to Phase 4 delivery verification. The migration adds 5 nullable columns (signal_id, risk_percent_used, portfolio_value_at_entry, pre_entry_validation_snapshot, effective_settings_snapshot) and 3 indexes to trade_plans. Confirmation that these applied correctly in the staging environment is outstanding.

**Scope**
- Apply DS-07 migration to staging environment
- Run `\d trade_plans` and confirm all 5 SI-02 columns are present
- Confirm 3 indexes created: idx_trade_plans_signal (P1) + idx_trade_history_exit_date + idx_trade_history_entry_date (P2)
- Record staging sign-off evidence in a verification note

**Acceptance Criteria**
- Migration applied cleanly on staging with no errors
- All 5 columns confirmed present in trade_plans via `\d trade_plans`
- All 3 indexes confirmed created
- Staging verification date recorded

---

### BLG-OPS-45 — red_flag_events severity field staging verification (v4.6 delivery)
**Priority:** P3 (Low)
**Type:** Operations / Staging Verification
**Owner:** Infrastructure & Operations Owner; Data Model & Domain Schema Owner
**Source:** v4.6 delivery verification — ST-09 AC-01/02/03 deferred to Phase 4 (staging-only ACs); AC-08 pending
**Effort:** XS (~0.5 hr)
**Provisional-Target:** v4.7

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-06, EPIC-03; severity_field_staging_verification.md produced; severity column confirmed; assignment rule verified; backfill confirmed zero nulls; Infrastructure & Operations Owner + Data Model & Domain Schema Owner sign-off; AC-08 cleared)

**Problem**
ST-09 (BLG-BE-16: red_flag_events severity field) was verified by code review and unit tests in v4.6. Three ACs were pre-designated as staging-only and explicitly deferred to Phase 4 delivery verification: AC-01 (severity column confirmed in staging DB), AC-02 (default severity assignment confirmed), AC-03 (backfill of existing records confirmed). Additionally, AC-08 (Data Model & Domain Schema Owner sign-off) was pending at merge; DoQ accepted at EPIC level.

**Scope**
- Run migration on staging and confirm severity column in red_flag_events
- Confirm default severity assignment (pre_entry_override events → warning, others → info)
- Confirm backfill applied to existing records (all existing events have non-null severity)
- Obtain Data Model & Domain Schema Owner sign-off on staging evidence

**Acceptance Criteria**
- severity column confirmed in red_flag_events on staging (`\d red_flag_events`)
- Default severity assignment confirmed (override events = warning, others = info)
- Backfill confirmed: no null severity values in existing events
- Data Model & Domain Schema Owner sign-off recorded

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

### BLG-GOV-53 — Agent idea participation tracking
**Priority:** P3 (Low)
**Type:** Governance / HR
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
Idea intake windows record per-agent submission counts (ideas_window.json). Director of HR observes that tracking participation trends over multiple windows (e.g., which agents consistently submit, which have reduced participation) could provide early signal of governance engagement health. A simple participation tracking summary across all IW-* windows would formalise this.

**Scope**
- Produce agent participation summary across all closed idea windows (IW-20260322-01 through IW-20260525-01)
- Per agent: window count, submission count, participation rate
- Output: advisory note filed; not a blocking governance gate

**Acceptance Criteria**
- Participation summary produced covering all closed windows
- Reviewed by Director of HR
- Filed as advisory note (no governance action required unless pattern identified)

---

### BLG-GOV-62 — SI-04 §13 formal pre-assessment
**Priority:** P1 (High)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-01, EPIC-01; si04_section13_preassessment.md produced; determination: PASS; 6 binding conditions; Strategy Rules & System Intent Owner sign-off)

**Problem**
SI-04 (Strategy Version Comparison) compares performance metrics across strategy versions. Before sprint planning seals, a formal §13 review must confirm this is display-only historical analysis (not adaptive or predictive). Last-minute §13 discoveries blocked v3.5 (IT-06); pre-assessment eliminates this risk.

**Scope**
- §13 review of SI-04 feature scope: performance comparison across strategy versions
- Confirm: deterministic historical analysis, display-only, no adaptive or predictive component
- Produce §13 compliance assessment document

**Acceptance Criteria**
- §13 assessment document produced (PASS or CONDITIONAL)
- Reviewed by Strategy Rules & System Intent Owner
- Gate condition (SI-04 sprint planning imminent) verified before commencing

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

**Problem**
`POST /digest/si05/send` was added to `docs/reference/openapi.yaml` in v5.1 (ST-01, EPIC-01). This endpoint is not present in `docs/ops/api_performance_baseline.md`. Performance baseline re-runs require a live environment and human coordination — cannot be filled autonomously.

**Scope**
- Add `POST /digest/si05/send` to `docs/ops/api_performance_baseline.md` performance measurement table
- Capture baseline latency, payload size, and response time in live/staging environment

**Acceptance Criteria**
- POST /digest/si05/send present in api_performance_baseline.md with baseline measurements recorded

---

### BLG-OPS-70 — ST-03 AC-04: Confirm SI-05 deep links work in production after FRONTEND_URL set
**Priority:** P2 (Medium)
**Type:** Operations / Staging Verification
**Owner:** Infrastructure & Operations Owner
**Source:** ST-03 v5.8 — AC-04 staging-only deferral (CLAUDE.md §2). FRONTEND_URL set on production backend 2026-06-17; deep link confirmation requires next scheduled SI-05 digest delivery.
**Effort:** XS (<1 hour)
**Provisional-Target:** v5.9 (verify at next SI-05 digest delivery after 2026-06-17)

**Acceptance Criteria**
- SI-05 Telegram digest received after FRONTEND_URL env var applied
- Deep links in digest are present and resolve to correct frontend pages
- Infrastructure & Operations Owner confirmation recorded

---

### BLG-OPS-59 — SI-05 service production p99 latency baseline review
**Priority:** P2 (Medium)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-head-of-engineering-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled (review after 4 weeks production operation, ~2026-07-04)
**Displacement:** BLG-OPS-13 (performance baseline gaps, P3) deprioritised.

**Sprint history:** Planned as ST-12 (EPIC-04) in cycle 2026-06-10__release-v5.5; returned to backlog 2026-06-15 — gate date 2026-07-04 not yet reached. Planned as ST-14 (EPIC-03) in cycle 2026-06-16__release-v5.7; returned to backlog 2026-06-17 — gate date 2026-07-04 not yet reached. Planned as ST-07 (EPIC-02) in cycle 2026-06-17__release-v5.8; returned to backlog 2026-06-17 — gate date 2026-07-04 not yet reached. **Not eligible for sprint planning before 2026-07-04** (gate: ≥ 4 weeks of POST /digest/si05/send production operation).

**Problem**
POST /digest/si05/send was baselined pre-launch in BLG-OPS-54. Production p99 latency under real data volume (actual trade history, real Red Flag Journal entries, real compliance scores) may differ from the pre-launch baseline. Confirming production performance validates the service is not degrading under real conditions.

**Scope**
- After 4 weeks of production operation (≥ 2026-07-04): extract p99 latency from Render logs for POST /digest/si05/send
- Compare against BLG-OPS-54 pre-launch baseline
- If p99 > 2× baseline: file a performance investigation item; otherwise record PASS
- Document findings in a brief perf review note

**Acceptance Criteria**
- Post-4-week p99 latency extracted and documented
- Comparison against BLG-OPS-54 baseline made
- Performance PASS or investigation item filed
- Infrastructure & Operations Owner sign-off

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

### BLG-GOV-101 — Governance model complexity assessment
**Priority:** P2 (Medium)
**Type:** Governance / Process Assessment
**Owner:** Director of HR; PMO Lead; Head of Specs Team
**Source:** IDEA-director-of-hr-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-QA-34 (QA evidence file format audit, P3, gate-conditional) deprioritised.

**Evidence trigger:** AUD-2026-06-02 overall score = 73 (down from 79 at AUD-2026-05-21; Δ = -6). 5 open audit items (BLG-GOV-79–83). Score decline and open item count provide the evidence-based trigger previously lacking.

**Problem**
The governance system has grown across 37 cycles. AUD-2026-06-02 scored overall 73 — a 6-point decline from AUD-2026-05-21 (79). Hypothesis: some portion of this decline may reflect governance overhead that exceeds the value delivered per cycle, rather than specific item failures. A bounded complexity assessment determines whether the model should be simplified (steps consolidated, gates relaxed, prompts shortened) or whether the decline is fully explained by specific remediable items (BLG-GOV-79–83).

**Scope**
- Review audit score decline context: are BLG-GOV-79–83 the full explanation, or is there residual structural complexity?
- Per-engine step count analysis: for each governance prompt, count hard gates, write operations, and step count; compare against pre-v4.0 baseline if available
- Identify: steps that consistently produce no output (friction with no value), gates that have never fired in 10+ cycles, prompts that are longest vs. their usage frequency
- Hypothesis test: resolve BLG-GOV-79–83 first; if audit score recovers to ≥78, complexity is not the root cause; if score remains at 73 or below, complexity may be a contributing factor
- Output: complexity assessment report with finding: "complexity is NOT a root cause — specific items explain the decline" or "complexity IS a contributing factor — recommend simplification candidates"

**Acceptance Criteria**
- Assessment report produced after BLG-GOV-79–83 are resolved
- Report includes per-engine step counts and complexity indicators
- BLG-GOV-71 (gate-conditional: audit score < 70) remains separate; this item is an earlier-trigger analysis
- Director of HR, PMO Lead, and Head of Specs Team sign-off on findings

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

### BLG-GOV-112 — SI-05 digest weekly cadence review (gate-conditional)
**Priority:** P2 (Medium)
**Type:** Governance / Product Review
**Owner:** Product Owner; Director of Quality
**Source:** IDEA-product-owner-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** After 2026-07-04 SI-05 effectiveness review
**Displacement:** BLG-GOV-85 (Arc 6 §13 pre-assessment boundary doc, gate-conditional) deprioritised.

**Sprint history:** Planned as ST-13 (EPIC-04) in cycle 2026-06-10__release-v5.5; returned to backlog 2026-06-15 — gate date 2026-07-04 not yet reached. Planned as ST-12 (EPIC-03) in cycle 2026-06-16__release-v5.7; returned to backlog 2026-06-17 — gate date 2026-07-04 not yet reached. Planned as ST-05 (EPIC-02) in cycle 2026-06-17__release-v5.8; returned to backlog 2026-06-17 — gate date 2026-07-04 not yet reached. **Not eligible for sprint planning before 2026-07-04** (gate: SI-05 Phase 1 effectiveness review complete).

**Gate criteria:** SI-05 Phase 1 first effectiveness review (BLG-GOV-96) complete — gate clears 2026-07-04.

**Problem**
SI-05 delivers a weekly digest. After 4+ weeks of production use, the weekly cadence should be reviewed: is weekly too frequent/infrequent? Are users actioning the digest? The first effectiveness review (2026-07-04) will provide the data needed for this cadence assessment.

**Scope**
- After 2026-07-04 effectiveness review: assess weekly cadence appropriateness
- Review si05_digest_log delivery count, any feedback from the user, and whether digest content is acted upon (indirectly measurable via red flag journal views post-delivery)
- Produce a cadence recommendation: maintain weekly / move to bi-weekly / or introduce adaptive cadence

**Acceptance Criteria**
- Cadence review document produced after 2026-07-04 effectiveness review
- Recommendation made with data backing
- Product Owner sign-off

---

### BLG-GOV-115 — SI-05 digest actionability metric definition (gate-conditional)
**Priority:** P2 (Medium)
**Type:** Governance / Metrics
**Owner:** Metrics Definitions & Analytics Owner; Infrastructure & Operations Owner
**Source:** IDEA-metrics-analytics-20260607-01 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.4 (gate: 2026-07-04 SI-05 effectiveness review complete)
**Gate criteria:** BLG-GOV-113 (SI-05 Phase 1 effectiveness review protocol) complete — i.e., the 2026-07-04 effectiveness review has been conducted

**Sprint history:** Planned as ST-14 (EPIC-04) in cycle 2026-06-10__release-v5.5; returned to backlog 2026-06-15 — gate date 2026-07-04 not yet reached. Planned as ST-13 (EPIC-03) in cycle 2026-06-16__release-v5.7; returned to backlog 2026-06-17 — gate date 2026-07-04 not yet reached. Planned as ST-06 (EPIC-02) in cycle 2026-06-17__release-v5.8; returned to backlog 2026-06-17 — gate date 2026-07-04 not yet reached. **Not eligible for sprint planning before 2026-07-04** (gate: BLG-GOV-113 effectiveness review protocol complete).

**Problem**
SI-05 launched 2026-06-04. After the 2026-07-04 effectiveness review (BLG-GOV-113), the digest's actionability should be formally assessed. This requires defining what "actionable" means for an SI-05 digest: did the user open the Red Flag Journal? Did they review their strategy compliance? Did they act on a drift signal? Without formal metric definitions, the effectiveness review cannot produce measurable outcomes.

**Scope**
- Define 2–4 actionability metrics for SI-05 digest effectiveness
- Metrics should be measurable from existing data sources (si05_digest_log, red_flag_events, trade data)
- Produce a brief metrics definition document for Metrics Definitions & Analytics Owner review
- Input to BLG-GOV-96 (effectiveness measurement criteria) and BLG-GOV-112 (cadence review)

**Acceptance Criteria**
- 2–4 actionability metrics formally defined with data source mapping
- Metrics document reviewed by Metrics Definitions & Analytics Owner
- Gate condition verified: 2026-07-04 effectiveness review (BLG-GOV-113) complete
- Metrics feed BLG-GOV-112 cadence review and BLG-GOV-96 effectiveness criteria

---

### BLG-GOV-116 — sprint_planning_prompt.md within-sprint date gate advisory
**Priority:** P2 (Medium)
**Type:** Governance / Process Improvement
**Owner:** Head of Specs Team
**Source:** LL-P3-01 (v5.4 lessons_learnt_closure.md) — carry-forward; rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.5
**Displacement:** N/A (governance patch — no displacement required)

**Problem**
Stories with within-sprint date gates (e.g., "ST-03 CONDITIONAL — gate 2026-06-21") are not marked with a standard notation in sprint_backlog.md at planning time. This led to v5.4 ST-03 being returned mid-sprint when the gate date was not met, which could have been predicted at planning. A standard marker at sprint planning time would make conditional stories visible.

**Scope**
- Add advisory to sprint_planning_prompt.md: stories with a date gate that falls within the sprint window should be marked `Status at sprint open: conditional — gate <date>` in sprint_backlog.md at planning time
- Version bump sprint_planning_prompt.md; update OPERATIONAL_GUIDE §14; append prompt_change_log.md entry

**Acceptance Criteria**
- sprint_planning_prompt.md updated with advisory marker rule
- Version bumped; §14 and change log updated per CLAUDE.md §6
- Head of Specs Team sign-off

---

### BLG-GOV-117 — execution_prompt.md pr_status read-after-open improvement
**Priority:** P2 (Medium)
**Type:** Governance / Process Improvement
**Owner:** Head of Specs Team; PMO Lead
**Source:** LL-P3-03 (v5.4 lessons_learnt_closure.md, 2nd recurrence) — carry-forward; rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.5
**Displacement:** N/A (governance patch)

**Problem**
After opening a PR, execution_prompt.md writes `pr_status: "open"` to execution_state.json without reading the actual `gh pr view` response. This means if the PR is created but immediately encounters an issue (merge conflict, CI failure), the state records "open" incorrectly. When the session resumes, STEP 5.0A catches the stale status — but this is reactive rather than proactive. Second recurrence in v5.4.

**Scope**
- Update execution_prompt.md: after `gh pr create`, immediately read `gh pr view <number> --json state,mergeStateStatus` and write the actual state to execution_state.json
- Version bump execution_prompt.md; update OPERATIONAL_GUIDE §14; append change log

**Acceptance Criteria**
- execution_prompt.md updated: pr_status written from `gh pr view` response, not assumed
- Version bumped; §14 and change log updated per CLAUDE.md §6
- Head of Specs Team sign-off

---

### BLG-GOV-118 — qa_evidence commit discipline advisory in execution_prompt.md
**Priority:** P2 (Medium)
**Type:** Governance / Process Improvement
**Owner:** PMO Lead; Head of Specs Team
**Source:** LL-P3-02 (v5.4 lessons_learnt_closure.md) — carry-forward; rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.5
**Displacement:** N/A (governance patch)

**Problem**
v5.4 sprint execution had an operator error where qa_evidence_EPIC-xx.md was not committed to the EPIC branch before opening the PR. The existing CLAUDE.md §2 rule says "Every new API endpoint must be added in the same commit" but there is no explicit reminder in execution_prompt.md about committing qa_evidence before PR open.

**Scope**
- Add advisory to execution_prompt.md STEP 5 (or the PR-opening step): "Before opening the PR, verify qa_evidence_EPIC-xx.md is committed to the EPIC branch"
- Version bump; update §14; append change log

**Acceptance Criteria**
- execution_prompt.md updated with qa_evidence pre-PR commit advisory
- Version bumped; §14 and change log updated per CLAUDE.md §6
- Head of Specs Team sign-off

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

### BLG-GOV-120 — Trade data density progress tracker
**Priority:** P2 (Medium)
**Type:** Governance / Operational Visibility
**Owner:** Product Owner; Infrastructure & Operations Owner
**Source:** IDEA-product-owner-20260610-01 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.5

**Problem**
Multiple high-value features are gated on closed trade counts (PT-04: 20 trades; SI-02 frontend: 20 trades; Arc 6 PS-01: 100 trades). Current count is 6 closed trades. The count is invisible between sprint planning sessions. A visible progress indicator would make gate-clearing trajectory tangible and help PO set timing expectations.

**Scope**
- Add trade count display to System Status page or dashboard: "Closed trades: N / Gate 1: 20 / Gate 2: 50 / Gate 3: 100"
- Alternatively: add to weekly SI-05 Telegram digest as a data density summary line
- Data source: existing trade_history query (SELECT COUNT(*) WHERE pnl IS NOT NULL)

**Acceptance Criteria**
- Trade count visible in at least one operational context (System Status or weekly digest)
- Count queries real production data (not hardcoded)
- Playwright coverage or staging sign-off for observable AC

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

### BLG-GOV-125 — SC-03: Consolidate spec_references policy sub-variants in execution_prompt.md
**Priority:** P2 (Medium)
**Type:** Governance / Prompt Simplification
**Owner:** Head of Specs Team
**Source:** GCA-2026-06-17 — ST-04 (BLG-GOV-101) simplification candidate SC-03
**Effort:** XS (~1 hour)
**Provisional-Target:** v5.9

**Scope**
STEP 3.1.A steps 2a, 2b, 2c of `execution_prompt.md` each handle a distinct spec_references edge case (path verify, documentation-creation stories, test-authoring stories) as separate numbered sub-steps with prose. Consolidate into a single unified rule with a 3-case lookup table (~25 lines → ~10 lines). No logic change.

**Acceptance Criteria**
- Steps 2a, 2b, 2c replaced by a single consolidated rule with lookup table
- All three edge cases preserved in the table
- Version bump + changelog entry
- Head of Specs Team sign-off

---

### BLG-GOV-126 — SC-04: Remove STEP 8.6–8.7 fatigue detection guardrail from roadmap_prompt.md
**Priority:** P3 (Low)
**Type:** Governance / Prompt Simplification
**Owner:** Head of Specs Team
**Source:** GCA-2026-06-17 — ST-04 (BLG-GOV-101) simplification candidate SC-04
**Effort:** XS (~1 hour)
**Provisional-Target:** v5.9

**Scope**
STEP 8.6 (Fatigue Detection Guardrail) and STEP 8.7 (Pivot Loop) in `roadmap_prompt.md` detect convergence bias where all candidates advance and the Challenger issues only Clearance Statements. This condition has never been triggered. The Challenger failure rule in STEP 5 (mandatory counter-argument) provides equivalent protection. Remove STEPs 8.6–8.7; verify Challenger failure rule in STEP 5 is sufficient.

**Implementation constraint (Head of Specs Team sign-off GCA-2026-06-17):** Before removing STEP 8.6–8.7, verify that STEP 5's Challenger failure rule explicitly covers convergence bias (all candidates advance with only clearance statements). If STEP 5's language is narrower, add a consolidating note to STEP 5 before deletion.

**Acceptance Criteria**
- STEP 5 Challenger failure rule verified to cover convergence bias scenario (or updated to do so)
- STEPs 8.6 and 8.7 removed from roadmap_prompt.md
- Version bump + changelog entry
- Head of Specs Team sign-off

---

### BLG-GOV-127 — SC-05: Remove dead-load advisory steps from release_planning_prompt.md
**Priority:** P3 (Low)
**Type:** Governance / Prompt Simplification
**Owner:** Head of Specs Team
**Source:** GCA-2026-06-17 — ST-04 (BLG-GOV-101) simplification candidate SC-05
**Effort:** XS (~1 hour)
**Provisional-Target:** v5.9

**Scope**
Two advisory steps in `release_planning_prompt.md` run unconditionally but produce no decision-relevant output in the common case: (a) STEP 1.3 (Design-Gate Language Scan) duplicates Sprint Planning Engine STEP -1 check; (b) STEP 5.7 (Decision Record Integrity) has no effect when no escalations are raised (common in v4.x–v5.x). Make STEP 5.7 conditional on escalations existing. Assess whether STEP 1.3 can be removed or reduced to a single-line reminder.

**Acceptance Criteria**
- STEP 5.7 made conditional (only runs if escalation records exist)
- STEP 1.3 removed or reduced to one-line note
- Version bump + changelog entry
- Head of Specs Team sign-off

---

### BLG-GOV-128 — SC-06: Make Playwright selector check conditional on DOM changes in execution_prompt.md
**Priority:** P3 (Low)
**Type:** Governance / Prompt Simplification
**Owner:** Head of Specs Team
**Source:** GCA-2026-06-17 — ST-04 (BLG-GOV-101) simplification candidate SC-06
**Effort:** XS (<1 hour)
**Provisional-Target:** v5.9

**Scope**
STEP 3.1.A step 13 in `execution_prompt.md` mandates a scan of all Playwright spec files for stale selectors whenever any DOM element is modified. For governance-only or backend-only EPICs (~60% of sprints) this is dead load. Tighten the condition: "if this story modifies a DOM element that is targeted by existing Playwright selectors." No logic change for frontend EPICs.

**Acceptance Criteria**
- Step 13 condition tightened to DOM-change-relevant stories only
- Existing coverage for frontend EPICs preserved
- Version bump + changelog entry
- Head of Specs Team sign-off

---

### BLG-GOV-129 — SC-07: Compress Advisory Summary Block format docs in post_ship_closure.md
**Priority:** P3 (Low)
**Type:** Governance / Prompt Simplification
**Owner:** Head of Specs Team
**Source:** GCA-2026-06-17 — ST-04 (BLG-GOV-101) simplification candidate SC-07
**Effort:** XS (<30 min)
**Provisional-Target:** v5.9

**Scope**
The Advisory Summary Block section at the end of `post_ship_closure.md` contains ~20 lines of format documentation for a simple 3-line summary block. Compress to a 5-line format block with a single-sentence explanation. No behaviour change.

**Acceptance Criteria**
- Advisory Summary Block format documentation compressed to ≤5 lines
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

## Release Slice v5.8 — cycle 2026-06-17__release-v5.8

<!-- release-plan-marker: RP:v5.8:2026-06-17__release-v5.8 -->

**Theme:** RFJ UX Design Completion, SI-05 Effectiveness Review & Production Hardening

| ST-ID | BLG-ID | Title | EPIC | Sprint | Effort | Conditional |
|-------|--------|-------|------|--------|--------|-------------|
| ST-01 | BLG-FE-64 | RFJ design review pre-brief | EPIC-01 | 1 | XS | No — gate 2026-06-21 (time-certain) |
| ST-02 | BLG-FE-41 | Red Flag Journal visual design review | EPIC-01 | 1 | M | No — gate 2026-06-21 (time-certain) |
| ST-03 | — | FRONTEND_URL production env var configuration | EPIC-01 | 1 | XS | No |
| ST-04 | BLG-GOV-101 | Governance model complexity assessment | EPIC-01 | 1 | M | No |
| ST-05 | BLG-GOV-112 | SI-05 digest weekly cadence review | EPIC-02 | 2 | S | Yes — gate 2026-07-04 |
| ST-06 | BLG-GOV-115 | SI-05 digest actionability metric definition | EPIC-02 | 2 | S | Yes — gate 2026-07-04 |
| ST-07 | BLG-OPS-59 | SI-05 service production p99 latency review | EPIC-02 | 2 | S | Yes — gate 2026-07-04 |

*Authoritative source: claude/cycles/2026-06-17__release-v5.8/stage4_backlog_slice.md*

---

## Release Slice v5.7 — cycle 2026-06-16__release-v5.7

<!-- release-plan-marker: RP:v5.7:2026-06-16__release-v5.7 -->

**Theme:** Staging Verification Completion, SI-05 Effectiveness Review & Engineering/Governance Patches

| ST-ID | BLG-ID | Title | EPIC | Sprint | Effort | Conditional |
|-------|--------|-------|------|--------|--------|-------------|
| ST-01 | BLG-OPS-66 | Staging verification: concentration-status p95 after FX cache fix | EPIC-01 | 1 | XS | No |
| ST-02 | BLG-OPS-67 | Staging verification: red-flag-journal p95 after schema-once fix | EPIC-01 | 1 | XS | No |
| ST-03 | BLG-OPS-68 | Staging verification: behavioural-drift p95 + cache hit rate | EPIC-01 | 1 | XS | No |
| ST-04 | BLG-OPS-69 | Staging verification: research view p95 + cache hit rate | EPIC-01 | 1 | S | No |
| ST-05 | BLG-FE-75 | Staging verification: SI-05 deep links on mobile Telegram | EPIC-01 | 1 | XS | No |
| ST-06 | BLG-QA-56 | SI-01 all-pass state Playwright scenario | EPIC-01 | 1 | XS | No |
| ST-07 | BLG-QA-57 | SI-03 RFJ pagination Playwright scenario | EPIC-01 | 1 | XS | No |
| ST-08 | BLG-QA-58 | Arc 5 compliance score trend Playwright scenario | EPIC-01 | 1 | XS | No |
| ST-09 | BLG-FE-64 | RFJ design review pre-brief | EPIC-02 | 1 | XS | Yes — gate 2026-06-21 |
| ST-10 | BLG-BE-36 | Lazy-import pattern documentation (backend engineering patterns guide) | EPIC-02 | 1 | S | No |
| ST-11 | BLG-GOV-123 | Confirm dual sign-off pattern documented in execution_prompt.md | EPIC-02 | 1 | S | No |
| ST-12 | BLG-GOV-112 | SI-05 digest weekly cadence review | EPIC-03 | 2 | S | Yes — gate 2026-07-04 |
| ST-13 | BLG-GOV-115 | SI-05 actionability metric definition | EPIC-03 | 2 | S | Yes — gate 2026-07-04 |
| ST-14 | BLG-OPS-59 | SI-05 service production p99 latency baseline review | EPIC-03 | 2 | S | Yes — gate 2026-07-04 |

*Authoritative source: claude/cycles/2026-06-16__release-v5.7/stage4_backlog_slice.md*

---
