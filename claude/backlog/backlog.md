# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-06-10 (post-ship closure 2026-06-09__release-v5.4 — BLG-OPS-60 ✅ COMPLETE; BLG-FE-56 ✅ COMPLETE; BLG-GOV-92 already marked COMPLETE; BLG-FE-64 sprint history updated)
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

### BLG-FEAT-38 — Arc 5 compliance score in monthly P&L report ✅ COMPLETE v4.7 (2026-05-31)
**Priority:** P2 (Medium)
**Type:** Product Feature / Reporting
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2 days)
**Provisional-Target:** v4.1
**Completed:** ST-03, EPIC-02, cycle 2026-05-31__release-v4.7

**Gate cleared:** BLG-FEAT-36 ✅ COMPLETE v4.0 (validation_pass_rate_by_rule in Arc5ComplianceSection analytics endpoint) and BLG-FEAT-37 ✅ COMPLETE v4.0 (events_per_week metric in same delivery). Gate cleared inline at STEP 4.0, roadmap rebalance 2026-05-25__scheduled.

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

### BLG-FEAT-41 — Gemini thesis adoption rate metric
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-analytics-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
The Gemini thesis generation feature (shipped v4.0) writes to the setup_thesis field on trade plans. There is no metric tracking whether generated theses are accepted, edited, or discarded. Adoption rate is a useful early signal of feature value and cost-per-use justification.

**Scope**
- Define metric: thesis_adoption_rate = trade_plans_with_non-empty_setup_thesis_at_entry / trade_plans_with_thesis_generated
- Requires comparing gemini_audit_log (thesis generated) against trade_plan final setup_thesis at position entry
- Document in metrics_definitions.md

**Acceptance Criteria**
- Metric defined in metrics_definitions.md
- Query approach documented (gemini_audit_log join trade_plans)
- Reviewed by Financial Reporting & Records Owner and Product Owner

---

### BLG-FEAT-43 — Insufficient-allocation signal: distinct status and inline explanation ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Product Feature / Signal UX
**Owner:** Head of Backend Engineering; Head of UX & Design
**Source:** PO direction — 2026-06-02
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0

**Problem**
When a signal's per-share GBP price exceeds the per-position allocation budget, the backend returns suggested_shares=0 but leaves status as "new" — indistinguishable from an actionable buy signal. SNDK has been rank-1 for weeks at ~£1,259/share against a ~£1,147 allocation, silently returning 0 shares with no explanation. For high-priced stocks this is a structural recurring gap, not an edge case.

**Scope**
- Backend: set status to "allocation_insufficient" (not "new") when suggested_shares=0 and price_gbp > allocation_gbp
- Backend: include a human-readable reason field (e.g. "1 share (£1,259) exceeds position allocation (£1,147) — cannot size")
- Frontend: display the reason inline on the signal card/row when status is "allocation_insufficient"
- Frontend: visually differentiate allocation_insufficient signals from actionable new signals
- (Deferred) Override path allowing user to manually record a share count — scope to be defined if and when taken up

**Acceptance Criteria**
- Signal with price_gbp > allocation_gbp has status "allocation_insufficient", not "new"
- A reason string is returned from the backend and displayed inline in the signal view
- Allocation_insufficient signals are visually distinct from new/watchlisted signals
- Existing signals with status "new" and suggested_shares > 0 are unaffected
- No change to already_held or watchlisted status logic

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

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-11; maintain current structure; no changes recommended; Head of UX & Design sign-off)

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

### BLG-FE-46 — Gemini thesis generation user feedback mechanism
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend; Head of UX & Design
**Source:** IDEA-base44-frontend-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Problem**
The Gemini thesis generation button (shipped v4.0) produces a thesis and populates the setup_thesis field. There is no feedback mechanism: the user cannot signal whether the generated thesis was useful, edited heavily, or discarded. Without feedback, the system cannot track thesis quality or improve prompt engineering over time.

**Scope**
- Simple feedback UI on thesis generation: "Useful / Not useful" binary or a brief edit indicator
- Data stored in gemini_audit_log or a lightweight feedback table
- Does not require a full feedback loop — MVP is a binary signal

**Acceptance Criteria**
- Feedback mechanism available after thesis generation
- Feedback data persisted (table or audit log field)
- UX reviewed by Head of UX & Design before sprint planning

---

### BLG-FE-47 — Red Flag Journal design review scope document
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
RedFlagJournal.js (shipped v3.9) implemented the primary display. BLG-FE-41 (Red Flag Journal visual design review, gate: SI-03 live 30+ days) is now gate-eligible. A formal design review scope document should be produced before BLG-FE-41 sprint planning to define what aspects of the journal are in scope for the review: filters, pagination UI, empty state, colour/severity coding, and mobile layout.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-12; rfj_design_review_scope.md created; gate date 2026-06-21; PO + Head of UX & Design reviewed)

**Scope**
- Produce design review scope document for RedFlagJournal.js
- Define: what is reviewable (presentation, UX), what is out of scope (data structure, backend)
- Input to BLG-FE-41 sprint planning

**Acceptance Criteria**
- Design review scope document produced and filed
- Reviewed by Product Owner and Head of UX & Design
- Input to BLG-FE-41 before its sprint planning

---

### BLG-FE-49 — Pre-entry validation panel UX assessment
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-09, EPIC-04; pre_entry_panel_ux_assessment.md produced; 3 improvement candidates filed BLG-FE-56/57/58; Head of UX & Design sign-off; no implementation committed)

**Problem**
PreEntryValidationPanel (shipped v3.8) displays validation results and override acknowledgement. As Arc 5 evolves (SI-02, SI-05), the pre-entry panel will need to surface additional compliance context. A UX assessment of the current panel — layout, density, override acknowledgement flow — identifies improvement opportunities before Arc 5 sprint planning forces ad-hoc changes.

**Scope**
- Review PreEntryValidationPanel UX: layout clarity, override acknowledgement UX, text density
- Identify specific improvement candidates with rough effort estimates
- Assessment note filed; not a full redesign

**Acceptance Criteria**
- UX assessment note produced and reviewed by Product Owner
- Improvement candidates ranked by effort/value
- No sprint scope commitment required from this item

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

### BLG-FE-56 — Pre-entry panel: separate warn/fail override acknowledgement flow
**Priority:** P2 (Medium)
**Type:** Frontend / UX Improvement
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** docs/product/ux/pre_entry_panel_ux_assessment.md — candidate P1 — cycle 2026-05-31__release-v4.7 (ST-09)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

✅ COMPLETE — 2026-06-10 — cycle 2026-06-09__release-v5.4 (ST-02, EPIC-02; pre_entry_override_ux_spec.md produced; agent-mediated Head of UX & Design sign-off)

**Problem**
PreEntryValidationPanel treats `warn` and `fail` checks with the same override acknowledgement checkbox. `fail` represents a strategy hard stop; `warn` is advisory. Identical acknowledgement paths may encourage reflexive override of hard stops. As Arc 5 compliance rigour increases, distinct override flows are warranted.

**Scope**
- Separate override path for `fail` checks (confirmation modal or explicit "I understand this violates my strategy") vs `warn` checks (current checkbox)
- `fail` acknowledgement should be more deliberate — extra friction is intentional
- Assessment only — scope to be confirmed at implementation sprint

**Acceptance Criteria**
- Override UX differentiates warn (advisory) from fail (strategy violation)
- Fail override requires additional explicit acknowledgement step
- Existing warn-only acknowledgement flow preserved for warn-only states

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

### BLG-FE-60 — SI-05 notification channel trade-off document ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Frontend / UX / Spec Pre-work
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design; Product Owner
**Source:** IDEA-frontend-ux-20260601-02 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; STEP 5 debate advance; Challenger Clearance)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0
**Sequencing constraint:** Must complete before BLG-GOV-67 (SI-05 Phase 1) sprint planning seals.

**Problem**
SI-05 Phase 1 is specified as Telegram push notification (existing infrastructure v2.4). No formal trade-off document compares Telegram push (immediate, out-of-app, format-constrained) vs in-app notification (integrated, discoverable, format-flexible). If the PO decides post-implementation that in-app was preferable, reversing a Telegram delivery mechanism requires a new sprint. A pre-implementation trade-off document locks in the channel decision with documented evidence before sprint planning seals.

**Scope**
- Trade-off document comparing: Telegram push (existing infra, character limit constraints, no in-app UX) vs in-app notification (new build, integrated, discoverable)
- Evaluation criteria: implementation effort, user discovery, format flexibility, alignment with existing v2.4 weekly digest pattern
- PO channel decision recorded; if Telegram confirmed: format constraints fed to BLG-GOV-86

**Acceptance Criteria**
- Trade-off document produced with evaluation across defined criteria
- PO channel decision explicitly recorded in document
- If Telegram confirmed: channel decision fed as input to BLG-GOV-86 (message format spec)
- Sequencing constraint: completed before BLG-GOV-67 sprint planning seals

---

### BLG-FE-61 — ST-06 allocation_insufficient SignalCard badge Playwright E2E coverage
**Priority:** P3 (Low)
**Type:** Frontend / QA
**Owner:** QA & Testing Owner
**Source:** v5.0 EPIC-03 ST-06 — frontend testing gate (LL-v3.1-EX-01); code review only; filed 2026-06-03 per CLAUDE.md §2 hard gate before PR opens
**Effort:** XS (<1h)
**Provisional-Target:** v5.1

**Problem**
ST-06 introduced a visible frontend change (SignalCard orange "Cannot Size" badge + reason inline when signal status = `allocation_insufficient`). No Playwright E2E test covers this observable AC. Code review was accepted for the v5.0 PR under the hard gate, but a Playwright scenario must be authored before the v5.1 sprint planning seals.

**Scope**
- Add a Playwright scenario to an appropriate `tests/e2e/` spec file
- Mock signal payload with `status: "allocation_insufficient"` and a `reason` string
- Assert: orange "Cannot Size" badge is visible; reason text is rendered inline on the signal card

**Acceptance Criteria**
- Playwright test exists and passes in CI covering: (a) badge visible, (b) reason inline, (c) signal visually distinct from `status: "active"` signals
- Test added to test_scenarios in the relevant execution_state.json or qa_evidence for the sprint it ships

✅ COMPLETE — 2026-06-04 — cycle 2026-06-21__release-v5.1 (ST-04, EPIC-03; Playwright E2E tests/e2e/signals-allocation-insufficient.spec.js — 5 scenarios covering SC-SIG-AI-01/02/03; all pass in CI)

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

**Sprint history:** Planned as ST-03 (EPIC-02) in cycle 2026-06-09__release-v5.4; returned to backlog 2026-06-10 — date gate (2026-06-21) not met at sprint close; PO-authorised deferral. Eligible from next cycle on or after 2026-06-21.

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

### BLG-FE-66 — Red Flag Journal post-launch UX review
**Priority:** P3 (Low)
**Type:** Frontend / UX Review
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Source:** IDEA-base44-frontend-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-21, EPIC-04; rfj_ux_review_v53.md produced; top-3 friction points documented; follow-up items filed; Base44 Frontend Prompt Owner + Head of UX & Design sign-off)
**Displacement:** BLG-FE-55 (mobile responsiveness baseline, P3) deprioritised.

**Problem**
Red Flag Journal (RFJ.js) shipped v3.9 (2026-05-22 — 7+ weeks ago) with no post-launch UX review. As the most recently shipped complex frontend component, friction points and usability improvements may be present that are not captured by CI tests.

**Scope**
- Review RFJ.js for: filter UX clarity, pagination interaction, empty state messaging, table readability
- Identify top-3 friction points with proposed improvements
- File follow-up backlog items for any identified improvements

**Acceptance Criteria**
- UX review document produced covering filters, pagination, empty state, table layout
- Top-3 friction points documented with proposed improvements
- Any significant friction filed as a separate backlog item
- Base44 Frontend Prompt Owner and Head of UX & Design sign-off

---

### BLG-FE-67 — BLG-FE-64 visual design review scope definition
**Priority:** P2 (Medium)
**Type:** Frontend / Planning
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.
**Gate:** BLG-FE-64 gate clears 2026-06-21 — scope definition should complete before that date.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-22, EPIC-04; blg_fe_64_scope_definition.md produced; scope defined and BLG-FE-64 distinguished from BLG-FE-66; Frontend Specs & UX Documentation Owner + Head of UX & Design sign-off)

**Problem**
BLG-FE-64 (Red Flag Journal visual design review pre-brief) is in backlog with gate 2026-06-21 but its scope is vague — it is unclear what "visual design review" covers (typography, colours, spacing, component consistency, all of the above). Without a clear scope document, the story cannot be properly estimated or executed at sprint planning.

**Scope**
- Define the precise scope of BLG-FE-64: which visual elements, which pages/components, what acceptance criteria look like
- Distinguish BLG-FE-64 from BLG-FE-66 (UX review) — this is visual design, not interaction design
- Produce a one-page scope document that can be used as the BLG-FE-64 story AC at sprint planning

**Acceptance Criteria**
- Scope document produced: specifies which components and visual properties are in scope for review
- Clear distinction from BLG-FE-66 documented
- Frontend Specs & UX Documentation Owner and Head of UX & Design sign-off

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

### BLG-BE-16 — Red flag events severity field
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model & Domain Schema Owner; Head of Backend Engineering
**Source:** IDEA-data-model-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 (Behavioural Drift Detection) sprint planning imminent — severity taxonomy should be informed by SI-02 design to avoid schema rework.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-09; severity column + backfill + filter support; staging verification pending BLG-OPS-45)

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

### BLG-BE-25 — Fix pre-entry regime gate to use shared market status instead of independent yf.download ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** User-reported — pre-entry regime gate shows risk_off while dashboard shows risk_on — 2026-06-02
**Effort:** S (~0.5d)
**Provisional-Target:** v5.0

**Problem**
`_check_regime()` in `pre_entry_validation.py` calls `check_market_regime()` directly, which triggers a fresh `yf.download("SPY")` / `yf.download("^FTSE")` call independent of the `/market/status` endpoint. On rapid sequential requests, Yahoo Finance can return slightly different data (different row counts, trailing NaN values), causing the rolling 200MA calculation to resolve differently. This produces spurious regime_gate failures that contradict the authoritative dashboard reading, eroding user trust in the pre-entry check.

**Scope**
- Refactor `_check_regime()` to call `GET /market/status` (or a shared in-process cache) rather than invoking `check_market_regime()` directly
- Ensure the regime result used in pre-entry validation is always consistent with what `/market/status` returns
- Add a server-side cache (e.g. 5-minute TTL) to `check_market_regime()` so all callers share one result per window

**Acceptance Criteria**
- Dashboard regime and pre-entry regime gate always agree when called within the same session
- No spurious risk_off failures when SPY is clearly above its 200MA per the dashboard
- `/portfolio/pre-entry-validation` does not make an independent `yf.download` call

---

### BLG-BE-26 — SI-02 lightweight drift summary assessment (backend-only state mitigation) ✅ ASSESSMENT COMPLETE v5.0 (2026-06-03) — implementation ready for sprint planning with conditions
**Priority:** P2 (Medium)
**Type:** Backend Engineering / UX Assessment
**Owner:** Head of Backend Engineering; Head of UX & Design; Product Owner
**Source:** IDEA-challenger-20260601-01 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; STEP 5 debate advance; PO Rebut — assessment scope with UX risk evaluation)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.0 (conditional on assessment outcome)

**Problem**
Behavioural drift scores are computed by the SI-02 backend (4 metrics, 35 unit tests, shipped v4.6) but are not surfaced to the user because the SI-02 frontend has been deferred ~8 cycles (~2027-Q1). The system "knows" about drift but cannot communicate it, creating an information asymmetry that grows with each deferral cycle. A read-only drift summary (e.g., in System Status or Reports page) may mitigate without a full frontend sprint.

**Scope (assessment — not committed implementation):**
- Assess feasibility of adding a read-only drift summary to System Status or Reports page
- Evaluate UX risk: can drift scores be displayed with sufficient context (framing, threshold calibration advisory, §13 disclosure) to prevent misinterpretation by user?
- If feasible and UX risk manageable: define minimal scope (which metrics, where displayed, what framing text)
- If UX risk is too high: document assessment outcome as "assess only — not implemented" and close item

**Acceptance Criteria**
- Assessment document produced: feasibility determination + UX risk evaluation
- If UX risk manageable: minimal display scope defined (ready for sprint planning)
- If UX risk too high: outcome documented and item closed with rationale
- Product Owner reviews and signs off on assessment outcome

---

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

### BLG-BE-32 — SI-05 Telegram delivery retry and failure handling
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-05, EPIC-02; retry max 2 retries 30s/60s backoff; ERROR logging confirmed; 3 unit tests added; injectable sleep for CI; 24 tests passing; staging AC-04 PASS)
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Reliability
**Owner:** Backend Engineering Patterns Owner; Infrastructure & Operations Owner
**Source:** IDEA-backend-engineering-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-BE-21 (Arc 5 analytics endpoint versioning strategy, P3, gate-conditional) deprioritised.

**Problem**
si05_digest_service.py sends weekly digests via Telegram. The current failure mode for Telegram delivery failures (connection timeout, API error, message too long) is undocumented. For a scheduled service, silent failure means the user misses the weekly digest without knowing. Defining and documenting retry/failure handling before the service encounters production issues prevents silent failures.

**Scope**
- Document current si05_digest_service.py failure mode: what happens when Telegram API call fails (exception raised? logged? swallowed?)
- Define retry policy: does the service retry on transient failures? How many times? What backoff?
- If no retry exists: implement simple exponential backoff (max 2 retries, 30s/60s delays)
- Document failure handling in ops runbook or inline code comment (single clear explanation)
- If failure is unrecoverable: ensure error is logged at ERROR level so it appears in Render logs

**Acceptance Criteria**
- Failure mode documented and addressed in si05_digest_service.py
- At minimum: delivery failure is logged at ERROR level and not silently swallowed
- Retry policy (or explicit no-retry decision) documented
- Infrastructure & Operations Owner confirms the failure mode is observable in Render logs

---

### BLG-BE-33 — SI-05 digest delivery log table
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-06, EPIC-02; si05_digest_log table; schema: id/sent_at/status/event_count/telegram_message_id/error_message/created_at; CREATE TABLE IF NOT EXISTS guard; log rows on both paths; registered in main.py on_startup(); Data Model Owner sign-off; staging AC-04 PASS)
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model & Domain Schema Owner; Backend Engineering Patterns Owner
**Source:** IDEA-data-model-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~1 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-BE-14 (trade plan schema versioning, P3, gate-conditional) deprioritised.

**Problem**
SI-05 delivers weekly digests via Telegram. There is no persistent record of each delivery attempt: when it was sent, whether it succeeded, how many events were included, or the Telegram message ID. Without a delivery log, diagnosing missed digests requires Render log archaeology with a 7-day retention window. A delivery log table provides durable, queryable delivery history.

**Scope**
- New table: `si05_digest_log` (id, sent_at, status [sent/failed], event_count, telegram_message_id, error_message, created_at)
- Backend: write log row on each send attempt in si05_digest_service.py
- Migration: add table to database startup script
- Optional: GET /digest/si05/log endpoint (read-only, last N entries) for operational visibility

**Acceptance Criteria**
- si05_digest_log table created via migration
- Delivery attempt recorded on each send (success and failure)
- Data model reviewed by Data Model & Domain Schema Owner
- Optional endpoint: if implemented, registered in test.py and openapi.yaml per CLAUDE.md §2

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

### BLG-BE-35 — Add API key authentication to POST /digest/si05/send
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Security
**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Source:** ST-11 (BLG-GOV-99) — security review finding, 2026-06-08__release-v5.2
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-08, EPIC-02; API key auth applied to POST /digest/si05/send; unit test for 401 response added; digest_endpoints.md updated; Cybersecurity & Trust Lead + Head of Engineering sign-off)

**Problem**
POST /digest/si05/send is an unauthenticated endpoint (`backend/routers/digest.py:227`). It triggers Telegram API calls and digest sends without requiring authentication. An unauthenticated caller could trigger repeated sends (Telegram quota abuse, spam to digest chat). The existing authentication pattern (BLG-SEC-01/v2.2) applies API key auth — this pattern is not applied to the digest endpoint. Finding documented in `docs/security/security_register.md` Review 003 (ST-11, v5.2).

**Scope**
- Apply API key authentication to POST /digest/si05/send using the existing auth pattern (Depends injection, consistent with other protected endpoints)
- Add unit test verifying 401 response on unauthenticated POST /digest/si05/send
- Update `docs/specs/api_contracts/digest_endpoints.md` authentication requirements section
- Cybersecurity & Trust Lead sign-off on fix

**Acceptance Criteria**
- POST /digest/si05/send requires API key authentication per the existing pattern
- 401 returned on unauthenticated request
- Unit test added verifying 401 behaviour
- digest_endpoints.md updated with authentication requirements
- Cybersecurity & Trust Lead and Head of Engineering sign-off

---

## 5. QA & Test Automation Backlog

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

### BLG-QA-39 — Coverage matrix update and v4.7 contract completeness verification ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage + Spec Verification
**Owner:** QA Lead; API Contracts & Documentation Owner
**Source:** IDEA-qa-lead-20260601-01 + IDEA-api-contracts-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v4.8

**Problem**
v4.7 shipped compliance_summary field in GET /reports/monthly-pnl (ST-03, EPIC-04). This observable field is not yet in the test coverage matrix. Additionally, v4.7 bumped the monthly P&L response schema to v0.6 — the API contract documentation should reflect this version increment.

**Scope**
- Add compliance_summary field to QA coverage matrix as an observable regression point
- Verify that docs/specs/api_contracts/ reflects the v0.6 monthly P&L response schema
- Document any contract gaps found

**Acceptance Criteria**
- Coverage matrix includes compliance_summary field with regression test reference
- GET /reports/monthly-pnl v0.6 confirmed in API contract documentation
- Any contract gaps filed as BLG-SPEC items

---

### BLG-QA-40 — Wire Phase B CI with real Postgres service to catch missing-column errors
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** QA Lead; Head of Engineering
**Source:** Bug: position_state column missing from positions table, not caught by CI — 2026-06-01
**Effort:** M (~1–2 days)
**Provisional-Target:** v4.9

✅ COMPLETE — 2026-06-02 — cycle 2026-06-02__release-v4.9 (ST-03, EPIC-02; postgres:15 service container wired; DATABASE_URL injected; Phase A unaffected; 13 pre-existing Phase B failures surfaced and fixed)

**Problem**
The Phase A CI suite (ci-tests.yml) runs against a stub DATABASE_URL with all DB calls mocked, making missing schema columns completely invisible to CI. When `position_state`, `state_entered_at`, and `state_history` were never added to the `positions` table via a startup migration, every endpoint that queried those columns returned a 500 in production — yet all CI jobs were green. The ci-tests.yml workflow comment explicitly notes Phase B ("requires DATABASE_URL secret") was deferred; until it is wired, no automated job will catch a column referenced in SQL that doesn't exist in the DB.

**Scope**
- Spin up a Postgres service container in ci-tests.yml (GitHub Actions `services:` block)
- Wire the `DATABASE_URL` secret for the Phase B job step
- Enable the Phase B test run (currently commented out in the workflow)
- Verify all existing integration tests pass against the real service container

**Acceptance Criteria**
- A PR that introduces a SQL query referencing a non-existent column causes the CI Phase B job to fail
- Phase A (stub/mock tests) continues to run without a real DB
- No test collection errors in Phase B

---

### BLG-QA-41 — Schema smoke test: assert lifecycle columns exist on positions table
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA Lead
**Source:** Bug: position_state column missing from positions table, not caught by CI — 2026-06-01
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.9
**Depends on:** BLG-QA-40 (Phase B CI with real Postgres required)

✅ COMPLETE — 2026-06-02 — cycle 2026-06-02__release-v4.9 (ST-04, EPIC-02; tests/test_schema.py created; skips in Phase A; passes in Phase B with real Postgres)

**Problem**
There is no test that verifies the `positions` table contains the lifecycle columns (`position_state`, `state_entered_at`, `state_history`) that `ensure_lifecycle_columns()` is supposed to create. Without this, a missing `ensure_*` call at startup — or a call that silently errors — leaves a schema gap that is only discovered when a user hits the broken endpoint. A schema introspection test would close this class of bug permanently.

**Scope**
- Add a test (in `tests/test_position_lifecycle.py` or a new `tests/test_schema.py`) that calls `ensure_lifecycle_columns()` and then queries `information_schema.columns` to assert all three columns are present on the `positions` table
- Test must run under Phase B CI (real Postgres) and be excluded from Phase A

**Acceptance Criteria**
- Test fails if any of `position_state`, `state_entered_at`, `state_history` is absent from the `positions` table
- Test is skipped/excluded when `DATABASE_URL` points to the stub (Phase A)
- Test passes in the Phase B CI environment

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

### BLG-QA-43 — compliance_summary field population validation
**Priority:** P3 (Low)
**Type:** QA / Data Quality
**Owner:** QA Lead; Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.1 or spot-check session

**Gate criteria:** None. Can be done in any session that includes a monthly P&L report review.

**Problem**
v4.7 shipped compliance_summary in GET /reports/monthly-pnl (ST-03, EPIC-04). No verification confirms the field is populated from Arc5ComplianceSection data and matches what is displayed there. A mismatch would be a silent data quality issue.

**Scope**
- Verify compliance_summary in monthly P&L matches Arc5ComplianceSection display values
- Check that all 5 Arc 5 compliance metrics are correctly included in the summary
- Document verification result; file P2 bug if mismatch found

**Acceptance Criteria**
- Verification performed against staging or production monthly P&L output
- Result documented; any mismatch filed as a P2 bug item immediately
- No gate condition required

✅ COMPLETE — 2026-06-04 — cycle 2026-06-21__release-v5.1 (ST-05, EPIC-03; code review confirmed all 5 Arc 5 compliance fields present in reports_endpoints.md spec; staging AC-01 deferred to staged verification sprint — I&O Owner sign-off outstanding)

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

### BLG-QA-45 — Arc 5 QA completion criteria definition
**Priority:** P2 (Medium)
**Type:** QA / Planning
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before BLG-QA-26 sprint planning
**Displacement:** BLG-QA-22 (Arc 2 DoQ standards review, P3, gate-conditional) deprioritised.

**Problem**
BLG-QA-26 (Arc 5 E2E QA protocol) gates on "all five Arc 5 features shipped" but "fully complete" is undefined: does SI-05 Phase 2 count? Does SI-02 frontend count separately from SI-02 backend? Without defined criteria, BLG-QA-26 sprint planning will encounter scope ambiguity that delays the protocol.

**Scope**
- Define canonical "Arc 5 fully complete" criteria: explicit list of what must be shipped for BLG-QA-26 to trigger (proposed: SI-01 ✅, SI-03 ✅, SI-05 Phase 1 ✅, SI-02 frontend, SI-04 — all five features have shipped their full scopes)
- Confirm with Product Owner and Head of Specs Team: does SI-05 Phase 2 count separately, or is Phase 1 sufficient?
- Document criteria in BLG-QA-26 gate condition field
- Reviewed by Director of Quality and Product Owner

**Acceptance Criteria**
- Arc 5 completion criteria explicitly defined and documented
- BLG-QA-26 gate condition updated with the explicit list
- Product Owner and Director of Quality sign-off

---

### BLG-QA-46 — SI-05 digest service edge case test gap analysis
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-13, EPIC-04; 2 gaps found and fixed: test_telegram_api_connection_failure_logs_error + test_message_truncation_at_character_limit; 26 tests total passing; QA Lead sign-off)
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** QA Lead; Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.2
**Displacement:** BLG-QA-23 (trade plan lifecycle E2E test, P3, gate-conditional) deprioritised.

**Problem**
si05_digest_service.py was delivered with 21 unit tests. A gap analysis confirms whether key edge cases are covered: (a) zero events in the 7-day window, (b) Telegram API connection failure, (c) message content at character limit boundary, (d) partial send (some events included, others truncated), (e) service invocation when SI-01 has no pass/fail data yet.

**Scope**
- Review the 21 unit tests in the relevant test file against the 5 edge cases above
- Document: which edge cases are covered, which are missing
- If gaps found: author the missing tests; if all covered: document as verified
- Filed as sprint story if tests need authoring (XS effort)

**Acceptance Criteria**
- Gap analysis document produced listing all 5 edge cases with coverage status
- Any missing tests authored and passing
- QA Lead and Backend Engineering Patterns Owner sign-off

---

### BLG-QA-47 — SI-05 Phase 1 acceptance test protocol
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-14, EPIC-04; docs/qa/si05_acceptance_test_protocol.md produced; covers v5.1 deferred ACs: AC-09 Telegram delivery, AC-01 compliance_summary; Director of Quality sign-off)
**Priority:** P2 (Medium)
**Type:** QA / Test Planning
**Owner:** QA & Testing Owner; Director of Quality
**Source:** IDEA-qa-testing-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before staged verification sprint
**Displacement:** BLG-QA-24 (Yahoo Finance backoff path integration test stub, P3) deprioritised.

**Problem**
v5.1 post-ship closure deferred 2 staging-only ACs to a staged verification sprint: ST-01 AC-09 (Telegram delivery confirmed on staging) and ST-05 AC-01 (compliance_summary live data on staging). Without a formal acceptance test protocol, the staged verification sprint lacks structured guidance for what to test, how to record evidence, and what constitutes pass/fail for each deferred AC.

**Scope**
- Produce acceptance test protocol for the SI-05 Phase 1 staged verification sprint
- Per deferred AC: test steps, expected outcome, evidence format (screenshot? log entry?), pass/fail definition, sign-off authority
- Reference BLG-GOV-89 (staged verification sprint protocol, v1.0) for format
- Reviewed by Director of Quality before staged verification sprint planning

**Acceptance Criteria**
- Acceptance test protocol document produced for each deferred AC (ST-01 AC-09, ST-05 AC-01)
- Each AC has explicit: test steps, expected outcome, evidence format, sign-off authority
- Director of Quality sign-off

---

### BLG-QA-48 — Regression test suite baseline refresh post-v5.1
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-15, EPIC-04; POST /digest/si05/send confirmed in test.py; 5 Playwright scenarios confirmed; no formal baseline doc — BLG-QA-50 filed; QA Lead sign-off)
**Priority:** P2 (Medium)
**Type:** QA / Test Infrastructure
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.2
**Displacement:** BLG-QA-27 (CI test suite execution time baseline, P3, gate-conditional) deprioritised.

**Problem**
v5.1 shipped POST /digest/si05/send (new endpoint) and tests/e2e/signals-allocation-insufficient.spec.js (5 new Playwright scenarios). The regression test baseline has not been updated to include these new scenarios. Without the update, future regression checks may miss failures introduced in these areas.

**Scope**
- Add POST /digest/si05/send to the regression test baseline (endpoint presence and basic response check)
- Confirm signals-allocation-insufficient.spec.js scenarios are included in the CI regression run
- Update any regression baseline document (if one exists) to reflect v5.1 additions
- Note: if no formal regression baseline document exists, file its creation as a follow-on backlog item

**Acceptance Criteria**
- Regression baseline updated to include v5.1 additions
- All 5 signals-allocation-insufficient.spec.js Playwright scenarios confirmed in CI
- POST /digest/si05/send confirmed in backend/routers/test.py
- QA Lead sign-off

---

### BLG-QA-49 — Arc 5 test scenario completeness assessment
**Priority:** P2 (Medium)
**Type:** QA / Planning
**Owner:** QA Lead; Director of Quality
**Source:** IDEA-qa-lead-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-FE-39 (Arc 2 user journey map, P3, gate-conditional) deprioritised.

**Problem**
With SI-01, SI-03, and SI-05 Phase 1 shipped (3 of 5 Arc 5 features), an intermediate test scenario completeness assessment identifies QA gaps before the remaining features ship. This is not BLG-QA-26 (full Arc 5 QA protocol, gated on full completion) — it is a partial completeness check that surfaces gaps while there is still time to address them before the arc closes.

**Scope**
- Enumerate all Playwright E2E tests currently covering Arc 5 features: SI-01 (PreEntryValidationPanel), SI-03 (RedFlagJournal.js), SI-05 (allocation_insufficient badge — ST-04)
- Map each test to its Arc 5 AC coverage: which ACs are Playwright-covered, which are human-staging-only, which are not covered
- Identify top-3 coverage gaps that should be addressed before SI-02 or SI-04 sprint
- Output: coverage gap report filed with QA Lead

**Acceptance Criteria**
- Arc 5 Playwright test coverage map produced (feature × AC × test scenario)
- Top-3 coverage gaps identified with proposed remediation
- Director of Quality sign-off on coverage assessment

---

### BLG-QA-51 — BLG-SPEC-49–52 QA acceptance criteria definition
**Priority:** P2 (Medium)
**Type:** QA / Governance
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-QA-44 (SI-04 test planning, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-03, EPIC-01; endpoint_contract_qa_criteria_template.md produced; AC template applied to all 6 BLG-SPEC-49–52 gaps; Director of Quality sign-off)

**Problem**
BLG-SPEC-49–52 (6 endpoint contract gaps) need clearly defined acceptance criteria before they enter v5.3 sprint planning. Without QA-defined AC, the contract authoring stories will have vague verification criteria, risking incomplete sign-off.

**Scope**
- Define AC template for endpoint contract stories: what constitutes a "complete" contract (## METHOD /path at ## level, openapi.yaml entry, test.py entry, SystemStatus fallback count updated)
- Apply template to all 6 gaps in BLG-SPEC-49–52
- Ensure Director of Quality can sign off using the AC template at delivery verification

**Acceptance Criteria**
- QA readiness document produced with AC template and application to SPEC-49–52
- Template is reusable for future endpoint contract gap stories
- Director of Quality sign-off

---

### BLG-QA-52 — Tax year P&L boundary edge case validation
**Priority:** P2 (Medium)
**Type:** QA / Financial Accuracy
**Owner:** QA Lead; Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-QA-44 (SI-04 test planning, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-18, EPIC-04; 6 boundary test scenarios in tests/test_tax_year_pnl_boundary.py; all passing; Financial Reporting & Records Owner + QA Lead sign-off)

**Problem**
The tax year P&L report (shipped v2.0, March 2026) generates tax-year-segmented P&L summaries. A trade opened in one UK tax year (before April 5) and closed in the next (after April 6) may be misattributed to the wrong year. This edge case has never been formally tested.

**Scope**
- Identify the tax year boundary logic in the P&L report endpoint (GET /reports/monthly-pnl or the annual equivalent)
- Create test data scenarios: trade opened Dec 31, closed April 7 (straddling April 5 boundary); trade opened April 4, closed April 8
- Verify P&L is attributed to the correct tax year in each scenario
- Document findings; file a bug item if misattribution detected

**Acceptance Criteria**
- Year-boundary test scenarios documented and executed
- P&L attribution confirmed correct for all boundary cases (or bug filed if incorrect)
- Financial Reporting & Records Owner and QA Lead sign-off

---

### BLG-QA-53 — SI-05 digest Playwright E2E coverage
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** QA Lead; QA & Testing Owner
**Source:** IDEA-qa-testing-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** M (~1–2 days)
**Provisional-Target:** v5.3
**Displacement:** BLG-QA-44 (SI-04 test planning, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-19, EPIC-04; 4 Playwright scenarios in tests/e2e/si05-digest-delivery.spec.js; Telegram API mocked; all passing in CI; QA Lead sign-off)

**Problem**
si05_digest_service.py has 21 unit tests but no Playwright E2E coverage for the digest trigger → delivery flow. The observable AC for SI-05 (Telegram message received, compliance data present, red flag summary accurate) cannot be fully verified by unit tests alone. CLAUDE.md §2 requires Playwright coverage or staging sign-off for observable ACs.

**Scope**
- Define Playwright test scenarios for SI-05: trigger delivery, verify Telegram mock receives message, verify message format/content structure
- Implement minimum 3 Playwright scenarios covering: happy path delivery, empty red flag scenario, compliance score present
- Ensure scenarios run in CI without real Telegram API (mock or stub Telegram bot endpoint)

**Acceptance Criteria**
- ≥ 3 Playwright E2E scenarios for SI-05 digest delivery implemented and passing in CI
- Scenarios cover: happy path, empty state, compliance score
- Telegram API mocked or stubbed to avoid real API calls in CI
- QA Lead sign-off

---

### BLG-QA-54 — Playwright coverage matrix update post-v5.2
**Priority:** P2 (Medium)
**Type:** QA / Documentation
**Owner:** QA Lead; Director of Quality
**Source:** IDEA-qa-lead-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-QA-44 (SI-04 test planning, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-20, EPIC-04; playwright_coverage_matrix.md updated to reflect v5.2 + v5.3 additions; coverage gaps identified; Director of Quality sign-off)

**Problem**
v5.2 added 26 new edge case tests (BLG-QA-44 base scope) and other QA improvements. The Playwright coverage matrix (produced by BLG-QA-49, v5.2) does not yet reflect these additions. A stale matrix leads to incorrect QA sign-off assessments at delivery verification.

**Scope**
- Count all Playwright E2E test scenarios post-v5.2 (tests/e2e/*.spec.js)
- Update the coverage matrix to include all new scenarios added in v5.2
- Map new scenarios to their corresponding feature ACs
- Identify any ACs still lacking Playwright coverage

**Acceptance Criteria**
- Coverage matrix updated to reflect all v5.2 Playwright additions
- New scenarios mapped to feature ACs
- Coverage gaps identified and noted
- Director of Quality sign-off

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

### BLG-OPS-28 — Staging deploy live verification (ST-09 staging-only AC)
**Priority:** P2 (Medium)
**Type:** Operations / CI/CD
**Owner:** Infrastructure & Operations Owner
**Source:** ST-09 staging-only AC — v4.0 sprint execution 2026-05-24
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.1

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-04, EPIC-03; staging_deploy_verification.md produced; RENDER_STAGING_DEPLOY_HOOK confirmed; code-change deploy verified; docs-only filter verified; Infrastructure & Operations Owner sign-off)

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

### BLG-OPS-31 — Render application log retention policy
**Priority:** P2 (Medium)
**Type:** Operations / Data Management
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-07, EPIC-03; render_log_retention_policy.md produced; Render 7-day retention documented; database audit tables confirmed durable; decision: Render logs + database tables sufficient; Infrastructure & Operations Owner sign-off)

**Problem**
Render (production hosting platform) provides application logs with a default retention period. As Arc 5 compliance data and Gemini audit logs accumulate, understanding Render's log retention limits and whether application-level log archiving is required becomes an operational concern.

**Scope**
- Review Render log retention policy (current plan limitations)
- Assess whether gemini_audit_log and red_flag_events database tables provide sufficient durable audit trail independent of Render logs
- Determine if additional log archiving or export is required
- Document policy decision

**Acceptance Criteria**
- Render log retention policy reviewed and documented
- Database tables (gemini_audit_log, red_flag_events) confirmed as durable audit trail
- Policy decision documented in ops runbook or equivalent

---

### BLG-OPS-37 — Anthropic API tier cost assessment
**Priority:** P2 (Medium)
**Type:** Operations / Cost Planning
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-36 (Claude API first monthly review) complete.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-08, EPIC-04; anthropic_api_tier_assessment.md produced; no upgrade required; upgrade threshold defined at $5/month; FinOps & Resource Architect sign-off)

**Problem**
Anthropic API pricing tiers differ from Gemini. Without a tier cost assessment, there is no defined threshold at which a paid-tier upgrade becomes cost-effective. BLG-OPS-36 provides the usage data; this item performs the tier comparison and defines the decision threshold.

**Scope**
- Review Anthropic API pricing tiers vs actual usage from BLG-OPS-36 review
- Define usage threshold at which paid-tier upgrade is cost-effective
- Document decision framework and feed to FinOps monitoring

**Acceptance Criteria**
- Tier comparison document produced
- Usage threshold for upgrade decision defined
- Gate condition (BLG-OPS-36 complete) verified before commencing

---

### BLG-OPS-40 — Arc 5 hosting cost projection
**Priority:** P2 (Medium)
**Type:** Operations / Cost Planning
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260522-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 sprint planning initiated.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-10; arc5_hosting_cost_projection.md; current Render Starter tier adequate; no upgrade required; FinOps sign-off)

**Problem**
SI-02 drift detection will add recurring background analysis queries. The current Render compute tier was sized for Arc 1–4 workloads. Before SI-02 sprint planning, an assessment of whether the additional Arc 5 load is within the current tier is needed to prevent mid-sprint resource surprises.

**Scope**
- Estimate additional compute load from SI-02 background queries (query frequency, data volume)
- Compare against current Render compute tier headroom
- Recommendation: current tier adequate or upgrade required before SI-02 ships

**Acceptance Criteria**
- Load estimate produced with data and assumptions
- Tier adequacy determination made
- Gate condition (SI-02 sprint planning initiated) verified before commencing

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

### BLG-OPS-46 — Build minutes monitoring policy ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** Operations / Platform Continuity
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.8

**Problem**
Render CI build minutes were exhausted 2026-05-31, blocking deploys until the billing cycle reset. There is no monitoring of build minute consumption rate against the monthly allocation, and no early-warning threshold defined. Recurrence is likely in double-capacity sprints.

**Scope**
- Document monthly Render build minute allocation and consumption rate (v4.6–v4.7 actual usage)
- Establish early-warning threshold at 80% utilisation
- Confirm billing cycle reset date and document in ops runbook
- Assess whether double-capacity sprint cadence requires a plan upgrade

**Acceptance Criteria**
- Monthly build minute consumption documented
- Early-warning threshold defined and operator-visible (manual check or alert)
- Billing cycle reset date documented
- Ops runbook updated with monitoring procedure

---

### BLG-OPS-47 — Dependency audit post-v4.7 ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** Operations / Security
**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Source:** IDEA-head-of-engineering-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v4.8

**Problem**
Last CVE remediation was starlette upgrade (v4.0, 2026-05-25). Dependencies were not audited during v4.1–v4.7 sprints. New CVEs may have been disclosed for packages used in the application (FastAPI, psycopg2, alpaca-trade-api, anthropic SDK).

**Scope**
- Run `pip-audit` or equivalent dependency vulnerability scan against requirements.txt
- Run `npm audit` on frontend package.json
- Document findings; file BLG-OPS items for any HIGH/CRITICAL vulnerabilities
- Update ANTHROPIC SDK version if patch available

**Acceptance Criteria**
- Dependency audit complete for backend (Python) and frontend (npm)
- HIGH/CRITICAL vulnerabilities addressed or filed as P0/P1 backlog items
- Audit findings documented in security register (if exists) or ops runbook

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

### BLG-OPS-49 — npm devDependency HIGH CVEs (react-scripts chain)
**Priority:** P1 (High)
**Type:** Operations / Security
**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Source:** v4.8 ST-05 dependency audit (2026-06-01)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.9

✅ COMPLETE — 2026-06-02 — cycle 2026-06-02__release-v4.9 (ST-01, EPIC-01; npm audit fix applied; HIGH=0; 6 moderate remain CRA chain non-production; security_register.md Audit 001 updated)

**Problem**
npm audit (2026-06-01) found 21 HIGH severity vulnerabilities in the frontend devDependency chain via `react-scripts` (Create React App). All are build toolchain CVEs — not in the production runtime bundle. Nonetheless, HIGH severity requires P1 filing per security policy.

**Key CVEs:** GHSA-fv7c-fp4j-7gwp (@babel/plugin-transform-modules-systemjs), nth-check ReDoS (GHSA-rp65-9cf3-cjxr), node-forge HMAC bypass, lodash prototype pollution.

**Scope**
- Run `npm audit fix` on the project root package.json
- Verify no breaking changes to the build output after fix
- Confirm 0 HIGH vulnerabilities remain after fix
- Document in security_register.md

**Acceptance Criteria**
- `npm audit fix` applied and build passes
- HIGH vulnerability count = 0
- No regression in production bundle behaviour

---

### BLG-OPS-50 — Anthropic SDK upgrade (0.40.0 → current)
**Priority:** P2 (Medium)
**Type:** Operations / Maintenance
**Owner:** Head of Engineering
**Source:** v4.8 ST-05 dependency audit (2026-06-01)
**Effort:** S–M (~0.5–1 day)
**Provisional-Target:** v4.9

✅ COMPLETE — 2026-06-02 — cycle 2026-06-02__release-v4.9 (ST-02, EPIC-01; anthropic==0.40.0→0.105.2; 447 tests passing; security_register.md Upgrade 001 updated; AC-04 staging deferred: BLG-OPS-52)

**Problem**
The Anthropic Python SDK is pinned at v0.40.0 in `backend/requirements.txt`. Latest available version is 0.105.2 (65 minor versions behind as of 2026-06-01). Upgrading ensures access to latest API features, bug fixes, and security patches.

**Scope**
- Update `backend/requirements.txt`: `anthropic==0.40.0` → `anthropic==0.105.2` (or latest stable)
- Run full backend test suite to verify no breaking changes
- Review Anthropic SDK changelog (0.40.0 → current) for breaking API changes that may affect `/ai/generate-thesis` and `/ai/check-daily-cost` endpoints
- Document upgrade in security_register.md

**Acceptance Criteria**
- requirements.txt updated to latest stable Anthropic SDK version
- All backend tests pass
- AI endpoints functional post-upgrade

---

### BLG-SPEC-32 — External API integration spec template
**Priority:** P3 (Low)
**Type:** Spec Debt / Governance
**Owner:** Head of Specs Team
**Source:** IDEA-spec-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 2 external API integration contracts exist (second contract after Alpaca and Yahoo Finance).

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-21; _external_api_template.md created; 6 required sections; Anthropic + Alpaca conformance advisory noted)

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

### BLG-SPEC-43 — SI-04 strategy version comparison endpoint contract ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260527-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036; advanced STEP 5; Challenger clearance issued)
**Effort:** S-M (~1–2 days)
**Provisional-Target:** v4.8 (execute when SI-04 confirmed for next release planning cycle)

**Gate criteria:** SI-04 (Strategy Version Comparison) is confirmed for the next release planning cycle. §13 PASS already recorded v4.7 (6 binding conditions).

**Problem**
SI-04 strategy version comparison will introduce GET /analytics/strategy-version-comparison. Without a pre-authored API contract, the sprint implementing SI-04 must author the contract simultaneously, creating same-sprint spec debt per BLG-GOV-55 rule. Pattern of same-sprint spec debt occurred in SI-03 (spec debt filed v4.0, cleared v4.1) and SI-01 (similar pattern). Pre-authoring before sprint planning eliminates the risk.

**Scope**
- Author GET /analytics/strategy-version-comparison contract document under docs/specs/api_contracts/
- Define response schema: version_comparison (current strategy version vs historical, trade count per version, win_rate per version, avg_R per version, performance_delta)
- Define query parameters: version_from, version_to, date_range
- Define error cases: version_not_found (404), insufficient_data (422)
- Add endpoint entry to docs/reference/openapi.yaml (placeholder — implementation not required until SI-04 sprint)
- Review by SI-04 §13 binding conditions owner (Strategy Rules & System Intent Owner)

**Acceptance Criteria**
- API contract document created in docs/specs/api_contracts/
- Response schema defined (pending final SI-04 implementation confirmation)
- openapi.yaml entry added
- §13 binding conditions owner sign-off recorded on draft contract
- Gate condition (SI-04 in next release planning) verified before authoring begins

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

### BLG-SPEC-45 — SI-05 financial reporting scope verification (BLG-GOV-86 review)
**Priority:** P3 (Low)
**Type:** Specification / Documentation
**Owner:** Financial Reporting & Records Owner; Frontend Specs & UX Documentation Owner
**Source:** IDEA-financial-reporting-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-86 shipped v5.0)
**Effort:** XS (~1 hour)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-GOV-86 (SI-05 Telegram message format spec, shipped v5.0) reviewed to determine if financial reporting scope was explicitly addressed. If addressed → close this item; if not → define supplementary spec before SI-05 Phase 1 sprint planning.

**Problem**
SI-05 weekly digest will include compliance metrics. Whether it should also include financial performance summary (distinct from Arc5ComplianceSection data) was an open question to be resolved by BLG-GOV-86 format spec. Now that BLG-GOV-86 shipped, this question needs a closure decision.

**Scope**
- Review BLG-GOV-86 (Telegram message format spec) for explicit financial reporting scope decision
- If covered: document the decision and close this item
- If not covered: define supplementary spec addressing financial reporting in SI-05 digest

**Acceptance Criteria**
- BLG-GOV-86 reviewed; financial reporting scope question explicitly answered
- If supplementary spec needed: spec document produced and reviewed by Financial Reporting & Records Owner
- Gate condition verified before SI-05 sprint planning

✅ COMPLETE — 2026-06-04 — cycle 2026-06-21__release-v5.1 (ST-02, EPIC-01; BLG-GOV-86 reviewed — financial reporting confirmed OUT OF SCOPE for Phase 1; scope decision documented at docs/product/decisions/si05-financial-reporting-scope-decision.md)

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

### BLG-SPEC-47 — Align SI-05 `pass_rate` computation with BLG-GOV-86 §5.2 (mean-of-per-rule vs overall aggregate)
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-03, EPIC-01; Option(a) chosen — BLG-GOV-86 §5.2 amended to accept volume-weighted overall rate; si05-telegram-message-format-spec.md v1.1→v1.2; DEV-v51-EPIC01-01 resolved and closed; Head of Specs Team sign-off)
**Priority:** P3 (Low)
**Type:** Spec Debt / API Contracts
**Owner:** Head of Specs Team; Head of Backend Engineering
**Source:** DEV-v51-EPIC01-01 — v5.1 EPIC-01 QA sign-off — 2026-06-21
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.2

**Problem**
`si05_digest_service.py` computes `validation_pass_rate` as a volume-weighted overall ratio (`total_pass / total_validations` across all rules combined), while BLG-GOV-86 §5.2 specifies the mean of per-rule pass rates from `validation_pass_rate_by_rule`. These differ when validation rules have unequal sample volumes — high-volume rules dominate the aggregate but receive equal weighting in the mean. Additionally, `digest_endpoints.md` v0.2 documents the data source as "Overall pass/total ratio (7d)", creating a spec-to-spec inconsistency with the canonical format spec. P3 deviation DEV-v51-EPIC01-01 filed at v5.1 EPIC-01 QA sign-off. Must resolve before the next SI-05 feature increment.

**Scope**
- Head of Specs Team to determine canonical intent: (a) amend BLG-GOV-86 §5.2 to accept volume-weighted overall rate as the accepted computation, or (b) require the mean-of-per-rule-rates approach as originally specified
- If option (b): correct `backend/services/si05_digest_service.py` to iterate `validation_pass_rate_by_rule` entries and compute arithmetic mean; update `docs/specs/api_contracts/digest_endpoints.md` data source description accordingly
- If option (a): update `digest_endpoints.md` v0.2 to document the accepted overall-ratio computation and confirm alignment with BLG-GOV-86
- Apply CLAUDE.md §6 governance edit checklist if any governance file is modified

**Acceptance Criteria**
- BLG-GOV-86 §5.2 and `digest_endpoints.md` v0.2 are internally consistent and match the implementation
- `si05_digest_service.py` `validation_pass_rate` computation method matches the canonical spec decision
- Any spec amendments include version bump and `prompt_change_log.md` entry per CLAUDE.md §6 if governance files are modified
- DEV-v51-EPIC01-01 resolved and closed

---

### BLG-SPEC-48 — POST /digest/si05/send API contract gap check and authoring
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-04, EPIC-01; digest_endpoints.md v0.2→v0.3 with authentication requirements section; API Contracts & Documentation Owner sign-off; Head of Specs Team sign-off)
**Priority:** P1 (High)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS–S (~1–2 hours if contract exists; ~0.5 day if authoring needed)
**Provisional-Target:** v5.2
**Displacement:** BLG-SPEC-46 (Arc 4 API surface area, P3, gate-conditional) deprioritised.

**Problem**
CLAUDE.md §2 requires "Every new API endpoint added to `backend/routers/` must have a corresponding `## METHOD /path` entry in a file in `docs/specs/api_contracts/` in the same sprint." v5.1 shipped POST /digest/si05/send via BLG-GOV-67 (ST-01, EPIC-01). No BLG-SPEC item for a digest endpoint API contract was filed alongside the implementation. If the contract was not authored, this is spec debt that must be resolved before the next sprint touching SI-05.

**Scope**
- Check: does `docs/specs/api_contracts/` contain a file with `## POST /digest/si05/send` as a heading?
- If YES: confirm it was filed in the v5.1 sprint and complies with CLAUDE.md §2; close item
- If NO: author the contract document covering: POST /digest/si05/send request/response schema, error cases (503 Telegram unavailable), authentication requirements; add entry to openapi.yaml; add to backend/routers/test.py if not present
- Apply CLAUDE.md §2 same-sprint rule retroactively for this v5.1 spec debt

**Acceptance Criteria**
- POST /digest/si05/send has a corresponding `## POST /digest/si05/send` entry in docs/specs/api_contracts/
- openapi.yaml has a corresponding entry
- backend/routers/test.py confirms the endpoint exists
- If contract was authored: version bump and prompt_change_log.md entry per CLAUDE.md §6 if any governance files were modified
- API Contracts & Documentation Owner and Head of Specs Team sign-off

---

### BLG-SPEC-49 — Author GET /ai/journal-summary/history API contract and openapi.yaml entry
**Priority:** P2 (Medium)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** ST-12 (BLG-GOV-100) — endpoint coverage audit post-v5.1, 2026-06-08__release-v5.2
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-04, EPIC-01; ## GET /ai/journal-summary/history added to ai_endpoints.md; openapi.yaml updated; API Contracts & Documentation Owner sign-off)

**Problem**
`GET /ai/journal-summary/history` exists in `backend/routers/ai.py` and is tested in `backend/routers/test.py` but has no entry in `docs/specs/api_contracts/ai_endpoints.md` and is absent from `docs/reference/openapi.yaml`. This is a CLAUDE.md §2 spec debt gap identified in the post-v5.1 coverage audit.

**Acceptance Criteria**
- `## GET /ai/journal-summary/history` heading added to ai_endpoints.md (##-level, not ###)
- openapi.yaml updated with the path entry
- API Contracts & Documentation Owner sign-off

---

### BLG-SPEC-50 — Author GET /analytics/compliance-metrics API contract and openapi.yaml entry
**Priority:** P2 (Medium)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** ST-12 (BLG-GOV-100) — endpoint coverage audit post-v5.1, 2026-06-08__release-v5.2
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-05, EPIC-01; ## GET /analytics/compliance-metrics added to analytics_endpoints.md; openapi.yaml updated; API Contracts & Documentation Owner sign-off)

**Problem**
`GET /analytics/compliance-metrics` exists in `backend/routers/analytics.py` and is tested in `backend/routers/test.py` but has no entry in `docs/specs/api_contracts/analytics_endpoints.md` (which documents other analytics endpoints) and is absent from `docs/reference/openapi.yaml`. This is spec debt identified in the post-v5.1 coverage audit.

**Acceptance Criteria**
- `## GET /analytics/compliance-metrics` heading added to analytics_endpoints.md (##-level)
- openapi.yaml updated with the path entry
- API Contracts & Documentation Owner sign-off

---

### BLG-SPEC-51 — Author GET /news/{ticker} API contract and openapi.yaml entry
**Priority:** P2 (Medium)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** ST-12 (BLG-GOV-100) — endpoint coverage audit post-v5.1, 2026-06-08__release-v5.2
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-06, EPIC-01; ## GET /news/{ticker} added to news_endpoints.md; openapi.yaml updated; API Contracts & Documentation Owner sign-off)

**Problem**
`GET /news/{ticker}` exists in `backend/routers/news.py` and is tested in `backend/routers/test.py` but has no dedicated API contract document in `docs/specs/api_contracts/` (the Alpaca integration contract covers the external news API, not this internal endpoint) and is absent from `docs/reference/openapi.yaml`. This is spec debt identified in the post-v5.1 coverage audit.

**Acceptance Criteria**
- A file in `docs/specs/api_contracts/` contains `## GET /news/{ticker}` as a ##-level heading
- openapi.yaml updated with the path entry
- API Contracts & Documentation Owner sign-off

---

### BLG-SPEC-52 — Author watchlist endpoint contracts and add openapi.yaml + test.py entries
**Priority:** P2 (Medium)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team; Head of Engineering
**Source:** ST-12 (BLG-GOV-100) — endpoint coverage audit post-v5.1, 2026-06-08__release-v5.2
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-07, EPIC-01; watchlist_endpoints.md authored with ## GET/POST/DELETE headings; openapi.yaml + test.py entries added; SystemStatus fallback count and SC-SS-01b updated; API Contracts & Documentation Owner + Head of Specs Team sign-off)

**Problem**
Watchlist endpoints (`GET /watchlist`, `POST /watchlist`, `DELETE /watchlist/{entry_id}`) exist in `backend/routers/watchlist.py` but have no API contract document in `docs/specs/api_contracts/`, no entries in `docs/reference/openapi.yaml`, and are absent from `backend/routers/test.py`. This is a triple-gap (contract + openapi.yaml + test) identified in the post-v5.1 coverage audit. CLAUDE.md §2 same-sprint rule applies retroactively as spec debt.

**Acceptance Criteria**
- A file in `docs/specs/api_contracts/` contains `## GET /watchlist`, `## POST /watchlist`, `## DELETE /watchlist/{entry_id}` as ##-level headings
- openapi.yaml updated with all three path entries
- backend/routers/test.py entries added for all three watchlist endpoints
- SystemStatus.js fallback count and SC-SS-01b in tests/e2e/system-status.spec.js updated if test.py count changes (per CLAUDE.md §2)
- API Contracts & Documentation Owner and Head of Specs Team sign-off

---

### BLG-SPEC-53 — BLG-SPEC-49–52 contract gap resolution plan
**Priority:** P1 (High)
**Type:** Spec Debt / Governance
**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Source:** IDEA-head-of-specs-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** M (~1–2 days)
**Provisional-Target:** v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-01, EPIC-01; api_contract_gap_resolution_plan.md produced; all 6 gaps priority-ranked; sprint scope confirmed; Head of Specs Team + API Contracts & Documentation Owner sign-off)

**Problem**
v5.2 endpoint coverage audit (BLG-GOV-100, ST-12) found 6 routes without API contracts: GET /ai/journal-summary/history, GET /analytics/compliance-metrics, GET /news/{ticker}, GET /watchlist, POST /watchlist, DELETE /watchlist/{entry_id} (BLG-SPEC-49–52). These contracts are required by CLAUDE.md §2 but were not filed at the time the endpoints shipped. A structured resolution plan ensures they are all resolved in a single v5.3 effort.

**Scope**
- Produce a resolution plan document for all 6 endpoint contract gaps
- Priority-rank the 6 gaps by risk (auth exposure, external-facing vs internal, complexity)
- Define sprint scope for v5.3: which gaps ship in the same sprint story vs separate stories
- Confirm whether any additional openapi.yaml gaps exist beyond BLG-SPEC-49–52

**Acceptance Criteria**
- Resolution plan document produced with priority-ranked gap list
- Sprint scope recommendation made for v5.3 sprint planning
- Head of Specs Team and API Contracts & Documentation Owner sign-off

---

### BLG-SPEC-54 — openapi.yaml completeness audit against all 50 routes
**Priority:** P1 (High)
**Type:** Spec Debt / API Governance
**Owner:** API Contracts & Documentation Owner; Head of Engineering
**Source:** IDEA-api-contracts-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-SPEC-46 (Arc 4 API contract pre-planning, gate-conditional) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-02, EPIC-01; all 50 routes audited against openapi.yaml; gaps identified and resolved; gap report produced; API Contracts & Documentation Owner sign-off)

**Problem**
v5.2 found 50 routes in backend/routers/. openapi.yaml coverage against all 50 routes has never been formally audited. The drift detection gate catches routes missing from api_contracts/ documents, but may not catch routes that are in contracts but missing from openapi.yaml. A formal audit ensures the public API surface is fully documented.

**Scope**
- List all 50 routes from backend/routers/ test.py or router files
- Compare against docs/reference/openapi.yaml entries
- Identify any routes present in contract files but absent from openapi.yaml
- Produce gap report; file additional BLG-SPEC items for any uncovered routes
- Update openapi.yaml for any confirmed gaps

**Acceptance Criteria**
- All 50 routes audited against openapi.yaml
- Gap report produced
- openapi.yaml updated for any confirmed gaps
- API Contracts & Documentation Owner sign-off

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

### BLG-GOV-30 — Sprint planning staging-only AC designation flag
**Priority:** P1 (High)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before v4.0 sprint planning

**Problem**
v3.9 post-ship closure carry-forward advisory item #2: environment-dependent ACs (those referencing Yahoo Finance, Alpaca, or other live service behaviour) were not designated "staging-only" at sprint planning. This resulted in BLG-QA-24 being filed as a surprise P3 notation at QA sign-off. A per-story staging_only_evidence flag at sprint planning time prevents this pattern.

✅ COMPLETE — v4.1 — sprint_planning_prompt.md v3.7 added staging-only AC gate (OA-02; confirmed resolved per v4.5 scope reference and lessons_learnt.md v4.6)

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

✅ COMPLETE — v4.x — LL-v3.9-P3-1 in-session merge gate sync implemented in execution_prompt.md; advisory pattern resolved (confirmed resolved per v4.5 scope reference and lessons_learnt.md v4.6)

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

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-15; release_planning_prompt.md v2.33 STEP 1.4 Gate-Condition Proximity Scan added; combined with BLG-GOV-43)

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

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-16; Q1=6 closed trades, Q2=0 with linked trade_plans; gate NOT MET; EPIC-02 deferred 6th time; BLG-FEAT-25 updated)

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

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-17; arc4_data_density_trajectory_v4.6.md; Option A selected — proceed on current trajectory; SI-02 gate ~Nov 2026, PT-04 sub-gate ~Sep 2026; PO + Challenger sign-off)

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

### BLG-GOV-40 — Delivery verification STEP 5.0A pr_number null guard
**Priority:** P2 (Medium)
**Type:** Governance / Prompt Engineering
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Head of Specs Team OA-04 resolution at v4.1 sprint planning — delivery_verification_prompt.md STEP 5.0A pr_number null guard patch.

**Problem**
OA-04 (from v4.0 post-ship closure) identified that delivery_verification_prompt.md STEP 5.0A lacks a null guard for pr_number — if a PR was merged without a number being recorded, the step may fail or produce misleading output. The guard should gracefully handle missing pr_number by surfacing a warning rather than halting.

**Scope**
- Add null guard to STEP 5.0A in delivery_verification_prompt.md
- Bump prompt version; update OPERATIONAL_GUIDE.md §14; append prompt_change_log.md entry
- Per CLAUDE.md §6 governance file edit checklist

**Acceptance Criteria**
- STEP 5.0A includes null guard for pr_number (warning output, not halt)

✅ COMPLETE — v4.1 — delivery_verification_prompt.md v2.6 pr_number null guard implemented (OA-04 resolution; confirmed resolved per lessons_learnt.md v4.6)
- Prompt version bumped; OPERATIONAL_GUIDE.md §14 updated; prompt_change_log.md appended
- Gate condition (OA-04 resolution at v4.1 sprint planning) verified

---

### BLG-GOV-41 — Sprint close automation failure investigation
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** PMO Lead; Infrastructure & Operations Owner
**Source:** IDEA-pmo-lead-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** sprint_close_reminder.yml failure mechanism identified — per OA-03 from v4.0 post-ship closure.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-20; workflow functioning as designed — observer effect/early filing; no fix required; investigation doc committed)

**Problem**
OA-03 (from v4.0 post-ship closure) flagged that sprint_close_reminder.yml failed silently. Investigation is needed to determine: what the failure mode is, whether it is a GitHub Actions timing issue, environment issue, or logic error, and whether automated sprint close reminders should be retained or replaced with a documented manual trigger.

**Scope**
- Review sprint_close_reminder.yml workflow for failure cause
- Check GitHub Actions run logs for the failing cycle (2026-05-22__release-v4.0)
- Propose fix or retirement of the automated trigger
- Document findings and chosen resolution

**Acceptance Criteria**
- Root cause identified and documented
- Fix implemented or workflow retired with documented rationale
- Gate condition (investigation outcome) verified before item closes

---

### BLG-GOV-43 — Arc 4 data density formal checkpoint
**Priority:** P2 (Medium)
**Type:** Governance / Release Gate
**Owner:** Product Owner; PMO Lead
**Source:** IDEA-product-owner-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
Arc 4 features (PO-02 through PO-05) all have data density gates: 6+ months AI journal entries (PO-02), 50+ trades with plans (PO-04), 50+ trades with regime-at-entry (PO-05). A formal checkpoint at each release planning cycle confirms whether gates are approaching satisfaction. Currently this check is informal and reactive. A structured checkpoint prevents sprint planning a story against a gate that won't clear for months.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-15; release_planning_prompt.md v2.33 STEP 1.4 Gate-Condition Proximity Scan added; combined with BLG-GOV-32)

**Scope**
- Define Arc 4 data density checkpoint procedure: trade count, plan count, AI journal entry count
- Add checkpoint step to release planning prompt or OPERATIONAL_GUIDE.md §6B
- Checkpoint produces a pass/fail per Arc 4 gate condition

**Acceptance Criteria**
- Checkpoint procedure defined
- Integrated into release planning reference materials
- Product Owner and PMO Lead sign-off

---

### BLG-GOV-45 — Arc 6 Monte Carlo §13 pre-assessment
**Priority:** P2 (Medium)
**Type:** Governance / §13 Compliance Pre-work
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
PS-03 (Monte Carlo Simulation, Arc 6) is documented as "§13 compliant — deterministic simulation" on the roadmap. Before Arc 6 sprint planning, a formal §13 pre-assessment of Monte Carlo confirms: the simulation uses actual trade distribution data only (no external benchmarks), produces context not recommendations, and does not engage the ML/prediction boundary. Early pre-assessment prevents a last-minute gate discovery at Arc 6 planning.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-18; PASS — 10 binding conditions; arc6_ps03_section13_preassessment.md; Arc 6 planning path clear; Strategy Rules & System Intent Owner sign-off)

**Scope**
- Run §13 checklist against PS-03 Monte Carlo feature definition
- Confirm: simulation is deterministic, uses own trade data only, output is statistical context not a recommendation
- Document assessment and binding conditions (if any)

**Acceptance Criteria**
- §13 assessment produced for PS-03
- Binding conditions documented
- Reviewed by Strategy Rules & System Intent Owner

---

### BLG-GOV-52 — Trade plan schema field count gate check
**Priority:** P2 (Medium)
**Type:** Governance / Data Model
**Owner:** Data Model & Domain Schema Owner; Product Owner
**Source:** IDEA-data-model-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
The trade plan data model (shipped v3.1, expanded through v3.5) contains a growing number of fields. Before Arc 4 deep analytics (PO-02, PO-03) and Arc 5 SI-02 add further fields, a gate check confirms: current field count is within manageable scope, there are no orphaned fields (captured but never surfaced), and the schema remains internally consistent with the roadmap's stated field list.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-19; trade_plan_schema_audit_v4.6.md; 25 fields post-DS-07; 0 orphaned fields; 3 P3 process gaps filed; Data Model & Domain Schema Owner sign-off)

**Scope**
- Review trade plan schema: enumerate all fields, cross-reference with roadmap feature descriptions
- Identify: orphaned fields (present but unused), missing fields (needed but absent), consistency with PT-01 trade plan object definition
- Output: schema audit note

**Acceptance Criteria**
- Schema audit note produced
- Orphaned fields identified (if any) with remediation recommendation
- Reviewed by Data Model & Domain Schema Owner

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

### BLG-GOV-55 — API contract same-sprint delivery rule
**Priority:** P1 (High)
**Type:** Governance / Process Rule
**Owner:** Head of Specs Team; API Contracts Documentation Owner
**Source:** IDEA-head-of-specs-20260525-01 — Promoted-Backlog (STEP 5 debate) cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
v4.0 shipped POST /trade-plans/{plan_id}/generate-thesis (ST-12) without a formal API contract document (addressed retroactively by BLG-SPEC-38). CLAUDE.md §2 already requires every new endpoint to be added to openapi.yaml in the same commit. A complementary rule requiring a formal API contract document in docs/specs/api_contracts/ in the same sprint as the endpoint prevents retroactive BLG-SPEC debt from recurring.

**Scope**
- Add rule to CLAUDE.md §2 (or sprint planning checklist): every new ## METHOD /path heading in a backend router file must have a corresponding API contract document in docs/specs/api_contracts/ in the same sprint
- Align with existing CLAUDE.md §2 openapi.yaml same-commit rule
- Head of Specs Team sign-off; bump CLAUDE.md version if applicable

**Acceptance Criteria**
- Rule added to CLAUDE.md §2 or sprint planning reference
- Head of Specs Team sign-off
- Rule applies from v4.1 sprint planning onward

✅ COMPLETE — v4.1+ — CLAUDE.md §2 rule added: "Every new API endpoint must be added to `docs/reference/openapi.yaml` in the same commit as the contract." and "Every new backend route must be registered in the endpoint test suite in the same commit." (confirmed resolved per v4.5 scope reference and lessons_learnt.md v4.6)

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

### BLG-GOV-67 — SI-05 early delivery (Phase 1 without SI-02)
**Priority:** P2 (Medium)
**Type:** Governance / Feature Scope Definition
**Owner:** Product Owner; Head of Specs Team
**Source:** IDEA-product-owner-20260522-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap; gate cleared; Challenger gate modification applied)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-01 + SI-03 live ≥ 30 days (gate clears 2026-06-21).

**Problem**
SI-05 (Weekly Strategy Integrity Digest) requires SI-02 (drift detection) for the drift score component. Phase 1 of SI-05 can ship using SI-01 and SI-03 data only: validation pass rate, override count, and red flag trends. BLG-GOV-54 (shipped v4.1) defined Phase 1 scope; this item is the implementation backlog entry.

**Scope**
- Implement SI-05 Phase 1: weekly digest using SI-01 + SI-03 data only
- Metrics: validation_pass_rate, override_count, red_flag_frequency_trend
- No drift score in Phase 1 (requires SI-02)
- Gate: SI-01 + SI-03 live ≥ 30 days (2026-06-21)

**Acceptance Criteria**
- Weekly digest renders with SI-01 + SI-03 metrics
- No SI-02 dependency in Phase 1 implementation
- Gate condition (SI-01 + SI-03 live ≥ 30 days) verified before sprint planning

✅ COMPLETE — 2026-06-04 — cycle 2026-06-21__release-v5.1 (ST-01, EPIC-01; backend/services/si05_digest_service.py delivered; POST /digest/si05/send; 21 unit tests; gate confirmed 2026-06-21; 1 P3 deviation DEV-v51-EPIC01-01 filed)

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

### BLG-GOV-69 — §13 register completion (AUD-2026-05-30-001 gap) ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** Governance / Compliance
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260601-01 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v4.8

**Problem**
AUD-2026-05-30-001 identified 7 governance prompts missing from §13 ARTEFACT_STATUS entries in OPERATIONAL_GUIDE.md §14: sprint_planning_prompt.md, execution_prompt.md, post_ship_closure.md, design_gate_prompt.md, roadmap_management_prompt.md, backlog_management_prompt.md, ideas_housekeeping_prompt.md. This governance integrity gap depresses the audit Governance Integrity dimension score.

**Scope**
- Add §13 ARTEFACT_STATUS entries for each of the 7 missing prompts in OPERATIONAL_GUIDE.md §14
- Ensure entries follow existing §13 format (version, last_updated, authority)
- Bump OPERATIONAL_GUIDE.md version per §6 governance edit checklist

**Acceptance Criteria**
- All 7 missing prompts added to §14 §13 register
- OPERATIONAL_GUIDE.md version bumped; prompt_change_log.md appended
- AUD-2026-05-30-001 gap confirmed closed

---

### BLG-GOV-70 — Agent charter header compliance remediation ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** Governance / Compliance
**Owner:** Director of HR; Head of Specs Team
**Source:** IDEA-director-of-hr-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.8

**Problem**
AUD-2026-05-30 Stage 3 identified 2 non-compliant agent charter files:
- api_contracts_documentation_owner.md: uses `## Role:` instead of `**Role:**`
- backend_engineering_patterns_owner.md: uses `**Owner:**` not `**Role:**`

Non-compliant headers may cause governance engines to fail role validation.

**Scope**
- Fix header in api_contracts_documentation_owner.md (`## Role:` → `**Role:**`)
- Fix header in backend_engineering_patterns_owner.md (`**Owner:**` → `**Role:**`)
- Verify no other agent files have non-compliant format

**Acceptance Criteria**
- Both files have compliant `**Role:**` header format
- All other agent files verified as compliant
- No governance engine role-validation failures after fix

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

### BLG-GOV-72 — AUD-2026-05-30-006 gap resolution verification ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** Governance / Audit Follow-up
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260601-01 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.8

**Problem**
AUD-2026-05-30-006 identified 3 deferred patches in v4.4 lessons_learnt_closure.md without BLG IDs — untracked in the backlog. Whether these were resolved in v4.5–v4.7 is unclear.

**Scope**
- Load v4.4 lessons_learnt_closure.md and identify the 3 patches
- Check v4.5–v4.7 sprint records for resolution
- If resolved: document and close; if not: file new BLG-GOV items

**Acceptance Criteria**
- v4.4 patches identified; resolution status confirmed
- Unresolved patches filed as new BLG items; AUD-2026-05-30-006 gap closed or escalated

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

### BLG-OPS-52 — ST-02 staging verification: Anthropic SDK 0.40.0 → 0.105.2 endpoint validation
✅ COMPLETE — 2026-06-03 — cycle 2026-06-03__release-v5.0 (ST-08, EPIC-03; staging verification run on trading-assistant-api-staging.onrender.com; AC-01 POST /trade-plans/{plan_id}/generate-thesis HTTP 200 + non-null thesis confirmed; AC-02 POST /ai/check-daily-cost HTTP 200 + cost structure confirmed; Infrastructure & Operations Owner sign-off 2026-06-03; DoQ agent-mediated sign-off 2026-06-03)
**Priority:** P2 (Medium)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** v4.9 EPIC-01 ST-02 AC-04 staging gate deferred post-merge (CLAUDE.md §2) — 2026-06-02
**Effort:** XS (<1h)
**Provisional-Target:** v4.10

**Problem**
ST-02 (Anthropic SDK upgrade 0.40.0 → 0.105.2) includes a staging-only AC requiring verification that POST /trade-plans/{plan_id}/generate-thesis and POST /ai/check-daily-cost remain functional post-upgrade. This cannot be confirmed autonomously and was deferred post-merge per CLAUDE.md §2 staging gate. Sign-off must be obtained before the next cycle that touches AI endpoints.

**Scope**
- On staging environment post v4.9 deploy: verify POST /trade-plans/{plan_id}/generate-thesis returns a valid AI-generated thesis
- Verify POST /ai/check-daily-cost returns the expected cost response
- Record Infrastructure & Operations Owner sign-off in the relevant QA evidence log

**Acceptance Criteria**
- POST /trade-plans/{plan_id}/generate-thesis returns HTTP 200 with non-null thesis field post SDK upgrade
- POST /ai/check-daily-cost returns HTTP 200 with expected cost structure post SDK upgrade
- Infrastructure & Operations Owner sign-off recorded with staging verification date

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

### BLG-OPS-55 — Deployment runbook update for SI-05 operational environment
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-07, EPIC-02; docs/ops/production_deployment_runbook.md v0.1→v0.2; §6 added covering SI-05 env vars, cron schedule, service verification, failure detection; Infrastructure & Operations Owner sign-off)
**Priority:** P2 (Medium)
**Type:** Operations / Documentation
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.2
**Displacement:** BLG-OPS-20 (research endpoint cost monitoring, P3, gate-conditional) deprioritised.

**Problem**
SI-05 Phase 1 (shipped v5.1) introduced new operational requirements not yet documented in the deployment runbook: (a) Telegram bot token environment variable (`TELEGRAM_BOT_TOKEN` or equivalent), (b) weekly digest cron schedule configuration, (c) si05_digest_service.py as a background/scheduled service that must be running in the deployed environment. If Render is rebuilt or the service is redeployed, missing this configuration silently disables the weekly digest.

**Scope**
- Update deployment runbook (docs/operations/ or equivalent) with SI-05 operational requirements:
  - Environment variable: name, purpose, where to obtain the Telegram bot token
  - Cron schedule: how the weekly digest schedule is configured (Render cron job? APScheduler?)
  - Service health check: how to verify the weekly digest service is running
  - Failure detection: how to confirm a digest was sent (reference BLG-BE-33 delivery log once shipped)
- Infrastructure & Operations Owner signs off on updated runbook

**Acceptance Criteria**
- Deployment runbook updated with all SI-05 environment requirements
- Telegram bot token environment variable documented
- Cron schedule configuration documented
- Infrastructure & Operations Owner sign-off

---

### BLG-OPS-56 — SI-05 service scheduled run health check
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-08, EPIC-02; docs/ops/si05_health_check_procedure.md created; 3 check options: si05_digest_log (Option A), Render logs (Option B interim), Telegram history (Option C); escalation path; weekly cadence; Infrastructure & Operations Owner sign-off)
**Priority:** P2 (Medium)
**Type:** Operations / Service Reliability
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-head-of-engineering-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.2
**Displacement:** BLG-OPS-23 (screener performance benchmark, P3, gate-conditional) deprioritised.

**Problem**
si05_digest_service.py runs on a weekly schedule. There is currently no documented way to verify whether the scheduled run completed successfully on any given week. Without a health check, a silently failing cron job (environment misconfiguration, scheduler crash, Render dyno sleep) would not be detected until the PO notices they haven't received a digest.

**Scope**
- Define health check procedure: how to confirm the weekly digest ran successfully
  - Option A: check si05_digest_log table (BLG-BE-33) for a recent send_at timestamp
  - Option B: check Render service logs for the service's INFO log entry
  - Option C: check Telegram chat history for a digest message
- Implement the simplest observable check; document in ops runbook
- If no observable check is possible without BLG-BE-33: document that BLG-BE-33 is a prerequisite for reliable health checking

**Acceptance Criteria**
- Health check procedure documented for si05_digest_service.py
- Procedure specifies: what to check, where to find the evidence, what constitutes PASS
- Infrastructure & Operations Owner and Head of Engineering sign-off

---

### BLG-OPS-57 — SI-05 Telegram delivery failure alerting
**Priority:** P1 (High)
**Type:** Operations / Monitoring
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-infra-ops-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-OPS-13 (performance baseline gaps, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-09, EPIC-02; FAILED status logged to si05_digest_log; ERROR-level Render log alert; ops runbook updated; Infrastructure & Operations Owner sign-off)

**Problem**
SI-05 delivers a weekly Telegram digest. BLG-OPS-56 (health check, v5.2) provides a manual verification procedure, but there is no automated alerting when delivery fails — a Telegram API error, revoked bot token, or rejected message would go undetected until manual inspection.

**Scope**
- Add a delivery confirmation check to si05_digest_service.py: if Telegram API returns non-200 or the send raises an exception, log to si05_digest_log with status = FAILED and trigger an admin alert
- Admin alert mechanism: write a log entry to stderr/Render logs at ERROR level; optionally post an alert message to the operator's Telegram or email
- Ensure retry logic (BLG-BE-32, shipped v5.2) still applies before the failure alert triggers

**Acceptance Criteria**
- Failed digest delivery is logged with status=FAILED in si05_digest_log
- A human-observable alert is triggered (Render log at ERROR level minimum)
- Delivery failure alerting documented in ops runbook (update docs/operations/deployment_runbook.md)
- Infrastructure & Operations Owner sign-off

---

### BLG-OPS-58 — CI secret scanning gate
**Priority:** P1 (High)
**Type:** Operations / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-OPS-13 (performance baseline gaps, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-10, EPIC-02; gitleaks CI secret scanning gate operational via .github/workflows/secret-scanning.yml + .gitleaks.toml; test_token advisory noted as low-risk; Cybersecurity & Trust Lead sign-off)

**Problem**
No secret scanning is configured in the CI pipeline. A developer could accidentally commit TELEGRAM_BOT_TOKEN, ANTHROPIC_API_KEY, or Supabase credentials to the repository. Given that the Telegram bot controls production digest delivery and the Anthropic API key incurs real costs, a leaked secret would be high-impact.

**Scope**
- Add a secret scanning step to GitHub Actions CI pipeline (e.g., gitleaks action or trufflehog)
- Configure to scan for: Telegram bot token patterns, Anthropic API key patterns, Supabase URL/key patterns, generic high-entropy strings
- Fail CI on detection; produce a clear error message identifying the type of secret
- Add a .gitleaks.toml or equivalent allowlist for known false positives (e.g., test fixture tokens)

**Acceptance Criteria**
- Secret scanning step added to CI and runs on every PR
- Confirmed to detect a test dummy token (AAAA-format) before allowlisting it
- Allowlist documented for any confirmed false positives
- CI fails and blocks merge when a real-looking secret is detected
- Cybersecurity & Trust Lead sign-off

---

### BLG-OPS-60 — Add v5.3 new endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** Post-ship closure 2026-06-08__release-v5.3 — STEP 6 endpoint coverage drift check
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.4

✅ COMPLETE — 2026-06-10 — cycle 2026-06-09__release-v5.4 (ST-01, EPIC-01; 5 endpoint rows added to api_performance_baseline.md §17 with live Render measurements; I&O Owner sign-off)

**Problem**
v5.3 shipped 5 new endpoints that appear in openapi.yaml but are absent from api_performance_baseline.md: GET /ai/journal-summary/history, GET /news/{ticker}, GET /watchlist, POST /watchlist, DELETE /watchlist/{entry_id}. (GET /analytics/compliance-metrics was already baselined.) Without baseline entries, performance regressions on these endpoints will go undetected.

**Scope**
- Run performance baseline measurements for all 5 missing endpoints in a staging/production environment
- Add measurement rows to docs/ops/api_performance_baseline.md
- Note p50/p95/p99 and any threshold flags

**Acceptance Criteria**
- All 5 new endpoints have baseline rows in api_performance_baseline.md
- Performance measurements made against a live environment (not mocked)
- Infrastructure & Operations Owner sign-off

---

### BLG-OPS-59 — SI-05 service production p99 latency baseline review
**Priority:** P2 (Medium)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-head-of-engineering-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled (review after 4 weeks production operation, ~2026-07-04)
**Displacement:** BLG-OPS-13 (performance baseline gaps, P3) deprioritised.

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

### BLG-GOV-78 — roadmap_prompt.md STEP 8.1 Empty Now Horizon gate strengthening
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** LL-RP-v4.8-01 (post-ship closure 2026-06-01__release-v4.8)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

✅ COMPLETE — 2026-06-02 — cycle 2026-06-02__release-v4.9 (ST-05, EPIC-03; roadmap_prompt.md v6.7→v6.8; STEP 8.1 converted to soft gate; OPERATIONAL_GUIDE.md v4.25→v4.26; prompt_change_log.md appended; HoST + PMO Lead sign-off)

**Problem**
When a roadmap rebalance runs as "No-change" and the Now horizon is empty, roadmap_prompt.md v6.6 STEP 8.1 fires an advisory — but does not require an explicit PO decision. In v4.8 release planning, this caused STEP -1.2 to fail because no formal v4.8 roadmap section existed after the no-change rebalance. The advisory was silently ignored.

**Scope**
- Strengthen STEP 8.1 of roadmap_prompt.md: when the Now horizon is empty and no next-release section exists in current_roadmap.md, require an explicit PO decision — either (a) add the next-release section now, or (b) defer intentionally with written rationale recorded in the cycle summary
- This converts a silent advisory into a soft gate requiring a documented PO choice

**Acceptance Criteria**
- roadmap_prompt.md STEP 8.1 updated: empty-Now-horizon with no next-release section requires explicit PO decision before completing the rebalance
- PO decision options documented (add section now OR defer with rationale)
- OPERATIONAL_GUIDE.md version bumped per CLAUDE.md §6 governance edit checklist
- Head of Specs Team + PMO Lead sign-off

---

### BLG-GOV-79 — Append 7 missing prompt_change_log.md entries for cycles 31–35 ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** AUD-2026-06-02 (AUD-2026-06-02-001, STALE 2nd occurrence) — 2026-06-02
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0

**Problem**
prompt_change_log.md is missing 7 entries for prompt version changes that occurred in cycles 31–35 (v4.5–v4.8). The OPERATIONAL_GUIDE §14 changelog confirms all 7 changes occurred and all engine versions in §14 are correct, but the corresponding prompt_change_log rows were never written — violating the CLAUDE.md §2 hard rule "any prompt version increment must have a matching entry in prompt_change_log.md." This was flagged as a recurring advisory (2nd occurrence) in v4.9 LL-RP-v4.9-02 and is now STALE. The 7 missing entries are fully specified in AUD-2026-06-02 §5 AUD-001 PATCH 1.

**Scope**
- Append 7 rows to prompt_change_log.md for: delivery_verification_prompt.md v2.7→v2.8, post_ship_closure.md v2.11→v2.12, execution_prompt.md v3.33→v3.34, release_planning_prompt.md v2.32→v2.33, roadmap_prompt.md v6.6→v6.7, roadmap_prompt.md v6.7→v6.8, execution_prompt.md v3.34→v3.35
- All change descriptions available verbatim in audit_report_AUD-2026-06-02.md §5 AUD-001 PATCH 1

**Acceptance Criteria**
- All 7 entries present in prompt_change_log.md in reverse-chronological order (newest first)
- Each entry has correct Date, Prompt path, Version transition, Change summary, Authority
- No other prompt_change_log gaps exist for any engine version changes in cycles 31–35

---

### BLG-GOV-80 — Add governance file edit check to execution_prompt.md STEP 8 commit ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** AUD-2026-06-02 (AUD-2026-06-02-003, root cause of BLG-GOV-79) — 2026-06-02
**Effort:** M (~1–2 days)
**Provisional-Target:** v5.0
**Depends on:** BLG-GOV-79 (prompt_change_log completion — apply before or together)

**Problem**
The roadmap engine (STEP 12) and amendment engine (STEP 9) have structural governance file edit checks that enforce prompt_change_log.md entries when governance files are modified. The execution engine lacks an equivalent check at its STEP 8 commit, creating a structural gap. Since execution stories frequently apply OA-clearance patches to governance prompts, this silent bypass was the confirmed root cause of all 7 missing prompt_change_log.md entries (BLG-GOV-79).

**Scope**
- Add governance file edit check to execution_prompt.md STEP 8 before commit: scan git diff for modified files in `claude/system/`, `claude/charter/`, `claude/agents/`; for each modified governance file, verify prompt_change_log.md entry exists; append if missing before proceeding
- Bump execution_prompt.md version (v3.35→v3.36)
- Update OPERATIONAL_GUIDE.md §8 source prompt header + §14 Execution Engine Source + §14 changelog (v4.26→v4.27)
- Append entry to prompt_change_log.md for this change
- Full PATCH block in audit_report_AUD-2026-06-02.md §5 AUD-003

**Acceptance Criteria**
- execution_prompt.md v3.36 contains governance file edit check at STEP 8 (before commit step)
- Check is STRUCTURAL: scans git diff --name-only for claude/system/, claude/charter/, claude/agents/ paths; appends missing prompt_change_log rows inline
- OPERATIONAL_GUIDE §8 source header, §14 Execution Engine Source, and §14 changelog updated in same commit
- prompt_change_log.md entry for execution_prompt.md v3.35→v3.36 present
- Head of Specs Team sign-off

---

### BLG-GOV-81 — Fix 5 non-standard agent file headers ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** AUD-2026-06-02 (AUD-2026-06-02-004; 2nd carry from AUD-2026-05-30-005) — 2026-06-02
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0

**Problem**
5 agent files use setext-style headings (`====` underline) with a trailing backslash on the Role field, deviating from the `# Name` / `**Role:** Name` (no backslash) standard used by all other 18 agent files. This has been open since AUD-2026-05-30-005 (first audit carry) and is now in its second consecutive carry. Affected files: ai_compliance_governance_officer.md, cybersecurity_trust_lead.md, director_of_hr.md, financial_reporting_records_owner.md, finops_resource_architect.md.

**Scope**
- For each of the 5 files: replace setext heading (`Name\n====`) with standard `# Name` ATX heading
- Remove trailing backslash from `**Role:** Name\` line → `**Role:** Name`
- Full PATCH blocks in audit_report_AUD-2026-06-02.md §5 AUD-004 (5 PATCH blocks, one per file)

**Acceptance Criteria**
- All 5 files use `# Name` ATX heading format (no setext `====`)
- All 5 files have `**Role:** Name` with no trailing backslash
- Format is consistent with the other 18 agent files in claude/agents/
- Head of Specs Team sign-off

---

### BLG-GOV-82 — Strengthen post-ship audit advisory to prevent multi-cycle skips ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** AUD-2026-06-02 (AUD-2026-06-02-005 — audit skipped 2 cycles, due at cycle 33, run at cycle 35) — 2026-06-02
**Effort:** M (~1–2 days)
**Provisional-Target:** v5.0

**Problem**
The post-ship STEP 0 audit advisory fires when `completed_cycle_count % 3 == 0`, but there is no re-fire mechanism if the advisory is not acted upon. In cycle 33 (v4.7), the audit due advisory was not recorded in the post-ship closure, allowing the audit to be skipped until cycle 35 — 2 cycles late. Additionally, the OPERATIONAL_GUIDE STEP 0 post-ship advisory does not track how many cycles ago the last audit ran, so the system cannot distinguish "due" from "overdue."

**Scope**
- Update post_ship_closure.md STEP 0 audit cadence check: in addition to `completed_cycle_count % 3 == 0`, add cumulative overdue check — if the delta between current completed_cycle_count and the count at last audit >= 4, fire AUDIT DUE regardless of modulo
- Add `last_audit_cycle_count` field to `.claude_current_state.json` schema: post-ship records the cycle count at which the last audit ran (for delta tracking)
- Update lifecycle_schema.json if needed for the new state field
- Bump post_ship_closure.md version + OPERATIONAL_GUIDE §10 header + §14 Post-Ship Closure Engine + §14 changelog
- Append entry to prompt_change_log.md
- Full PATCH in audit_report_AUD-2026-06-02.md §5 AUD-005

**Acceptance Criteria**
- post_ship_closure.md STEP 0 fires AUDIT DUE if `completed_cycle_count % 3 == 0` OR `(completed_cycle_count - last_audit_cycle_count) >= 4`
- `.claude_current_state.json` has `last_audit_cycle_count` field set at each post-ship closure when audit runs
- Post-ship closure Outstanding Actions records AUDIT DUE with Owner and target timeline when advisory fires
- OPERATIONAL_GUIDE §10 source header + §14 Post-Ship Closure Engine + changelog updated in same commit
- prompt_change_log.md entry present

---

### BLG-GOV-83 — Document PO acceptance requires GitHub review approval (not PR comment) ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** PMO Lead
**Source:** AUD-2026-06-02 (AUD-2026-06-02-006; v4.9 D-3 first occurrence — PO commented but PR remained BLOCKED) — 2026-06-02
**Effort:** XS (<1h)
**Provisional-Target:** v5.0

**Problem**
In v4.9, the Product Owner accepted PR #645 via a PR comment but the branch remained BLOCKED requiring human intervention because GitHub branch protection requires a formal "Approve" review action (not just a comment). This distinction is not documented anywhere — not in the PR template, team guide, or OPERATIONAL_GUIDE.

**Scope**
- Add a callout note to `.github/pull_request_template.md` in the QA Evidence or PO acceptance section clarifying: PO acceptance must be submitted as a GitHub Approve review action, not a PR comment
- PATCH block in audit_report_AUD-2026-06-02.md §5 AUD-006

**Acceptance Criteria**
- `.github/pull_request_template.md` contains explicit note that PO acceptance = GitHub "Approve review" action
- Note is visible in the PR template before any reviewer opens the PR
- Director of Quality sign-off (PR process governance)

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

### BLG-GOV-86 — SI-05 Phase 1 Telegram message format specification ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / Spec Pre-work
**Owner:** Head of Specs Team; Base44 Frontend; Product Owner
**Source:** IDEA-base44-frontend-20260601-01 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; STEP 5 advance; Challenger Clearance)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0
**Depends on:** BLG-FE-60 (notification channel decision — must confirm Telegram before specifying format)

**Problem**
SI-05 Phase 1 will deliver the weekly strategy integrity digest via Telegram (assuming BLG-FE-60 channel assessment confirms Telegram). Telegram imposes character limits, formatting constraints (Markdown subset), and no interactive elements. Without a pre-specified message format, implementation must decide format details concurrently with coding — increasing rework risk on an immutable notification channel.

**Scope**
- Message format specification document covering:
  - Character limit compliance strategy
  - Section structure: opening summary, Red Flag count (SI-03 data), compliance score trend (SI-01 data), key rule breach (if any), weekly recommendation to review
  - Data field definitions: which fields from SI-01 and SI-03 endpoints populate each section
  - Frequency: weekly (consistent with v2.4 weekly digest cadence)
  - Failure modes: what the message says when data is unavailable
- Review by Product Owner and Base44 Frontend before sprint planning seals

**Acceptance Criteria**
- Message format specification document produced and filed
- All data fields mapped to SI-01/SI-03 endpoint responses
- Telegram character limits verified not exceeded
- Product Owner and Head of Specs Team sign-off
- Gate condition (BLG-FE-60 channel confirmed as Telegram) verified before authoring

---

### BLG-GOV-87 — SI-02 frontend re-entry trigger criteria definition ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / Process Definition
**Owner:** PMO Lead; Product Owner
**Source:** IDEA-product-owner-20260601-02 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; STEP 5 advance; Challenger Clearance)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0

**Problem**
SI-02 frontend has been deferred 8 consecutive sprint planning cycles (v3.9–v4.9). The stated gate is "≥20 closed trades with linked trade_plans" but this is not formally documented anywhere as a hard gate with an explicit PMO Lead verification step. Without a formal, written, PMO-Lead-checked trigger, SI-02 frontend risks being informally deferred again when the trade count approaches 20. A documented re-entry trigger prevents this.

**Scope**
- Formal re-entry criteria document: defines the exact conditions for re-entering SI-02 frontend into sprint planning:
  - Hard gate: ≥20 closed trades with linked trade_plans confirmed by PMO Lead via production database query
  - Soft advisory: drift score data accumulation period ≥ 3 months (qualitative signal assessment)
  - Formal trigger: PMO Lead runs re-entry check at each release planning kickoff starting 2026-09-01
- Document filed in `claude/roadmap/` or `docs/product/decisions/`
- Re-entry check step added to release planning checklist (as advisory item for PMO Lead)

**Acceptance Criteria**
- Re-entry criteria document produced with hard gate and soft advisory defined
- PMO Lead acknowledges ownership of the periodic check
- Product Owner confirms criteria are the intended re-entry conditions
- Check cadence starts at v5.1 release planning (2026-09 earliest)

---

### BLG-GOV-88 — SI-04 formal binding conditions decisions document ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / §13 Compliance Record
**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Source:** IDEA-strategy-owner-20260601-01 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; STEP 5 advance; Challenger Clearance)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0

**Problem**
SI-04 §13 pre-assessment was completed in v4.7 ST-01 (si04_section13_preassessment.md — PASS; 6 binding conditions). The API contract was pre-authored in v4.8 (BLG-SPEC-43). However, a formal decisions document equivalent to the SI-01 record (decisions--2026-05-19__release-v3.8--SI-01-section13-review.md) does not yet exist for SI-04. This leaves the 6 binding conditions in an ad-hoc pre-assessment file rather than a proper Class 5 decisions record that sprint planning can reference.

**Scope**
- Author a formal SI-04 §13 compliance decisions document in `docs/product/decisions/`
- Content: reproduce the 6 binding conditions from si04_section13_preassessment.md; add formal sign-off block; reference BLG-SPEC-43 contract
- Document class: Planning Document or Decisions Record per document_lifecycle_guide.md
- Reviewed and signed off by Strategy Rules & System Intent Owner

**Acceptance Criteria**
- SI-04 §13 decisions document created in `docs/product/decisions/`
- All 6 binding conditions from si04_section13_preassessment.md reproduced
- Strategy Rules & System Intent Owner formal sign-off recorded
- BLG-SPEC-43 (API contract) cross-referenced

---

### BLG-GOV-89 — Staged verification sprint protocol document
**Priority:** P3 (Low)
**Type:** Governance / Process Documentation
**Owner:** Director of Quality; PMO Lead
**Source:** IDEA-director-of-quality-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.1 or v5.2

**Gate criteria:** None. Pattern validated across v4.7 (first use) and v5.0 (second use). Actionable now.

**Problem**
The staged verifications sprint pattern (batch-closing staging-only ACs from prior releases in a dedicated sprint) was validated at v4.7 and confirmed at v5.0. No formal protocol document exists. Without documentation, future verification-heavy releases cannot reference a standard approach, increasing coordination overhead.

**Scope**
- Document the staged verifications sprint pattern: trigger conditions, how to batch staging ACs, evidence requirements, sprint planning notes
- File in docs/operations/ or docs/governance/
- Review by Director of Quality and PMO Lead

**Acceptance Criteria**
- Protocol document produced and filed
- Covers: trigger conditions, batching approach, evidence format, sprint sizing note
- Reviewed by Director of Quality and PMO Lead

✅ COMPLETE — 2026-06-04 — cycle 2026-06-21__release-v5.1 (ST-06, EPIC-03; docs/operations/staged_verification_sprint_protocol.md v1.0 produced; Director of Quality + PMO Lead sign-off)

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

### BLG-GOV-92 — SI-05 Phase 2 activation criteria definition
**Priority:** P2 (Medium)
**Type:** Governance / Feature Scope Definition
**Status:** COMPLETE — v5.4 ST-04; criteria doc filed at docs/governance/si05_phase2_activation_criteria.md 2026-06-10
**Owner:** Product Owner; PMO Lead
**Source:** IDEA-product-owner-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** Before SI-02 frontend sprint planning (~Nov 2026)
**Displacement:** BLG-GOV-27 (cross-arc dependency map, P3, gate-conditional) deprioritised.

**Problem**
SI-05 Phase 2 (integrating SI-02 drift signals into the weekly digest) has no documented activation criteria. When SI-02 frontend activates (~Nov 2026), the decision to proceed with Phase 2 will be made without empirical reference unless criteria are defined now. Without criteria, Phase 2 may be activated prematurely (before SI-02 data quality is established) or unnecessarily delayed.

**Scope**
- Define SI-05 Phase 2 activation criteria: minimum conditions required before Phase 2 sprint planning seals
  - Hard gate: SI-02 frontend shipped and in active use (drift scores visible to user)
  - Quality gate: SI-02 drift scores confirmed as meaningful (not dominated by statistical noise at current trade volume)
  - Phase 1 effectiveness gate: PO confirms SI-05 Phase 1 is being actively used (per BLG-GOV-96 effectiveness measurement)
  - Optional: minimum weeks of SI-02 drift data accumulated
- Document criteria in a decisions record or project planning note
- PMO Lead to include criteria check at SI-02 frontend release planning kickoff

**Acceptance Criteria**
- Phase 2 activation criteria document produced and reviewed by Product Owner
- Criteria cover: SI-02 frontend shipping, data quality threshold, Phase 1 effectiveness confirmation
- PMO Lead acknowledges responsibility for criteria check at relevant release planning

---

### BLG-GOV-93 — OA-01/02 pre-sprint-planning resolution check procedure
**Priority:** P1 (High)
**Type:** Governance / Process Improvement
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-pmo-lead-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.2 (must complete before v5.2 sprint planning seals)
**Displacement:** BLG-GOV-26 (Arc velocity tracking dashboard, P3, gate-conditional) deprioritised.

**Problem**
OA-01 (release_planning_prompt.md §-1.2 patch) and OA-02 (execution_prompt.md §3.1.A patch) are due before v5.2 sprint planning seals. The OVERDUE patch pattern (F-01, 2026-06-03 lessons learnt: backlog_management_prompt.md patch missed 2 cycles) shows that deferred patches with stated deadline dates can be missed without an explicit enforcement mechanism. Without a defined check step, OA-01/02 risk becoming OVERDUE at v5.2 STEP -1.5.

**Scope**
- Define a pre-sprint-planning resolution check: at v5.2 release planning STEP 0, PMO Lead explicitly checks OA-01 and OA-02 resolution status before the run proceeds
- Add this check to the v5.2 release planning run manifest as a hard verification step
- If OA-01/02 are unresolved at v5.2 release planning: escalate to Head of Specs Team immediately (OVERDUE classification applies at 2nd consecutive carry)
- Apply the patches for OA-01/02 now if this item is sprint-planned in v5.2

**Acceptance Criteria**
- OA-01 and OA-02 explicitly resolved before v5.2 sprint planning seals
- Resolution evidence: release_planning_prompt.md §-1.2 updated + prompt_change_log.md entry (OA-01); execution_prompt.md §3.1.A updated + prompt_change_log.md entry (OA-02)
- PMO Lead confirms OA resolution in v5.2 run manifest
- Head of Specs Team sign-off on each prompt patch

---

### BLG-GOV-94 — SI-05 Phase 1 delivery verification protocol
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-14, EPIC-04; docs/qa/si05_delivery_verification_protocol.md created; covers AC-09 Telegram + AC-01 compliance_summary; cross-referenced with SI-05 acceptance test protocol; Director of Quality sign-off)
**Priority:** P2 (Medium)
**Type:** Governance / QA Planning
**Owner:** Director of Quality; QA & Testing Owner
**Source:** IDEA-director-of-quality-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** Before staged verification sprint
**Displacement:** BLG-QA-21 (Arc 2 E2E QA protocol, P3, gate-conditional) deprioritised.

**Problem**
v5.1 post-ship deferred 2 staging-only ACs to a staged verification sprint: ST-01 AC-09 (Telegram digest delivery confirmed on staging) and ST-05 AC-01 (compliance_summary live data confirmed). Without a formal verification protocol, the staged sprint lacks: who is responsible for each check, what constitutes evidence of completion, and when sign-off should be recorded.

**Scope**
- Produce delivery verification protocol for SI-05 Phase 1 staged ACs:
  - AC-09 (ST-01): steps to trigger the digest on staging, confirm Telegram delivery, record delivery timestamp and message ID as evidence
  - AC-01 (ST-05): steps to generate a monthly P&L report on staging and confirm compliance_summary fields are populated from live data
  - Sign-off format: which role signs off, what evidence is attached, where the sign-off is recorded (QA evidence file)
- Reference BLG-GOV-89 staged verification sprint protocol for format guidance
- Reviewed by Director of Quality; includes BLG-QA-47 (acceptance test protocol) as a companion input

**Acceptance Criteria**
- Verification protocol document produced for both deferred ACs
- Each AC has explicit: trigger steps, expected evidence, sign-off authority
- Director of Quality sign-off on the protocol
- Protocol ready before staged verification sprint is scheduled

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

### BLG-GOV-96 — SI-05 Phase 1 effectiveness measurement criteria
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-16, EPIC-04; 3 effectiveness criteria defined; 30-day review scheduled 2026-07-04; criteria documented at claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md; Product Owner sign-off)
**Priority:** P2 (Medium)
**Type:** Governance / Product Accountability
**Owner:** Product Owner; PMO Lead
**Source:** IDEA-challenger-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-FEAT-44 (Arc5ComplianceSection advisory at low trade volume, P3, gate-conditional) deprioritised.

**Problem**
SI-05 Phase 1 (weekly Telegram digest, shipped v5.1) has no defined effectiveness criteria. The decision to proceed to Phase 2 (SI-02 drift signal integration) should be evidence-based. Without defined criteria, Phase 2 will be activated based on subjective judgment rather than demonstrated Phase 1 value.

**Scope**
- Define SI-05 Phase 1 effectiveness criteria (qualitative, since no usage analytics for single-user system):
  - Frequency criteria: PO reviews at least N of the last M digests without skipping (suggested: 3 of last 4)
  - Action criteria: at least 1 digest-triggered app action per month (PO logs any "checked app after digest" event)
  - Content usefulness: PO self-assessment at 30-day mark (2026-07-04): was the digest content actionable?
- Record criteria in a governance note (not a formal document) for review at v5.2 or when Phase 2 is proposed
- Review at 30-day post-ship mark (2026-07-04) and record PO assessment

**Acceptance Criteria**
- Effectiveness criteria defined and acknowledged by Product Owner
- 30-day review scheduled (2026-07-04)
- 30-day review findings recorded when due
- PMO Lead confirms effectiveness criteria check is included in Phase 2 activation criteria (BLG-GOV-92)

---

### BLG-GOV-97 — Claude API model deprecation compliance check
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-09, EPIC-03; PASS — claude-haiku-4-5-20251001 not deprecated; check documented at docs/governance/ai_model_deprecation_check_v52.md; next review 2026-09-08; AI Compliance & Governance Officer sign-off)
**Priority:** P1 (High)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Head of Engineering
**Source:** IDEA-ai-compliance-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~30 minutes)
**Provisional-Target:** v5.2
**Displacement:** BLG-GOV-84 (Arc 6 gate revision assessment, P3, gate-conditional) deprioritised.

**Problem**
BLG-GOV-64 pins the Claude API model to a specific version (claude-3-5-sonnet-20241022 or equivalent at time of pinning). Anthropic publishes model deprecation notices on their platform. If the pinned model is deprecated and the system is not updated, API calls will fail in production, breaking both POST /trade-plans/{plan_id}/generate-thesis and POST /ai/check-daily-cost. BLG-GOV-90 defines a quarterly deprecation check procedure but has not been executed yet.

**Scope**
- Check Anthropic model lifecycle page for the currently pinned model's deprecation status
- Confirm the model pinned in BLG-GOV-64 (backend/services/ai_service.py or equivalent) is not deprecated
- If not deprecated: record check date and next review date in a governance note
- If deprecated: file P0 sprint story immediately to update the pinned model per BLG-GOV-90 trigger procedure

**Acceptance Criteria**
- Anthropic model lifecycle checked for the pinned model
- Check result recorded with timestamp (not deprecated: record + schedule next check; deprecated: P0 filed)
- AI Compliance & Governance Officer sign-off on check

---

### BLG-GOV-98 — Telegram bot token minimal-permission security review
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-10, EPIC-03; PASS with recommendation — send-only confirmed; BotFather manual check recommended as advisory; security_register.md updated; Cybersecurity & Trust Lead sign-off)
**Priority:** P2 (Medium)
**Type:** Governance / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-OPS-41 (red flag events table archiving strategy, P2, gate-conditional) deprioritised.

**Problem**
SI-05 Phase 1 introduced a Telegram bot token used to send weekly digest messages. Telegram Bot API tokens can have various permission scopes. A send-only bot token (permission to send messages to a pre-authorised chat) should be minimal — it should not be able to read messages from users or access chats beyond the designated digest channel. No security review of the token's permission scope has been documented.

**Scope**
- Verify the Telegram bot token in use is configured with minimal permissions: send-only to the designated chat
- Confirm the bot cannot read incoming messages, list chats, or send to arbitrary chats
- Document review findings: what permissions were verified, how verified (Telegram BotFather settings check)
- If overly permissive: request token rotation with appropriate scope restriction
- Record review in security_register.md per existing review pattern

**Acceptance Criteria**
- Telegram bot token permissions verified as minimal (send-only to designated chat)
- Review documented in security_register.md
- Cybersecurity & Trust Lead sign-off

---

### BLG-GOV-99 — SI-05 digest endpoint authentication review
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-11, EPIC-03; GAP_FOUND — POST /digest/si05/send unauthenticated; BLG-BE-35 P2 filed for future sprint; security_register.md updated (Review 003); does not block EPIC-03; Cybersecurity & Trust Lead sign-off)
**Priority:** P2 (Medium)
**Type:** Governance / Security
**Owner:** Cybersecurity & Trust Lead; Head of Engineering
**Source:** IDEA-cybersecurity-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-OPS-18 (data pipeline cost baseline, P3, gate-conditional) deprioritised.

**Problem**
POST /digest/si05/send is a new endpoint that triggers external Telegram API calls. The authentication requirements for this endpoint have not been formally reviewed: can it be called without authentication? Should it require API key authentication (like other endpoints per BLG-SEC-01/v2.2)? An unauthenticated endpoint that triggers external API calls is a potential abuse vector (sending arbitrary digests, incurring Telegram API usage).

**Scope**
- Review POST /digest/si05/send authentication: does it require API key auth per the existing authentication pattern?
- If unauthenticated: determine appropriate protection (API key, rate limiting, or scope restriction to internal calls only)
- If already authenticated: confirm auth is enforced and document
- File P2 fix if authentication gap found; record in security_register.md

**Acceptance Criteria**
- Authentication status of POST /digest/si05/send documented
- If gap found: P2 fix filed (or fixed inline); Cybersecurity & Trust Lead sign-off
- Security_register.md updated with review outcome

---

### BLG-GOV-100 — Backend endpoint documentation coverage audit post-v5.1
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-12, EPIC-03; 50 routes enumerated; 6 contract gaps found: BLG-SPEC-49/50/51/52 filed; audit documented at docs/ops/endpoint_coverage_audit_v52.md; Head of Engineering sign-off)
**Priority:** P2 (Medium)
**Type:** Governance / Process Compliance
**Owner:** Head of Engineering; API Contracts & Documentation Owner
**Source:** IDEA-head-of-engineering-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-OPS-19 (external API cost attribution, P3, gate-conditional) deprioritised.

**Problem**
CLAUDE.md §2 requires every new backend route to have: (a) corresponding entry in openapi.yaml, (b) corresponding entry in backend/routers/test.py, and (c) corresponding API contract document in docs/specs/api_contracts/. After v5.1 shipped POST /digest/si05/send, it's unclear whether all three requirements were met. A systematic audit after each release prevents cumulative spec debt from building undetected.

**Scope**
- Enumerate all routes in backend/routers/ (all @router.get/post/put/delete decorators)
- For each route: check (a) openapi.yaml entry exists, (b) test.py entry exists, (c) API contract document exists
- Document any gaps found; file BLG-SPEC items for each contract gap
- This item covers v5.1 deliverables; routine coverage audits should be added to post-ship closure checklist going forward

**Acceptance Criteria**
- All backend/routers/ routes enumerated and cross-checked against openapi.yaml, test.py, and docs/specs/api_contracts/
- Coverage gaps documented; BLG-SPEC items filed for any contract gaps found
- Head of Engineering and API Contracts & Documentation Owner sign-off

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

### BLG-GOV-104 — strategy_rules.md §11 parameter validation (first annual instance)
**Priority:** P2 (Medium)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Source:** IDEA-strategy-owner-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** M (~1–2 days)
**Provisional-Target:** v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-17, EPIC-03; docs/governance/strategy_parameter_validation_v53.md produced; ATR multiplier, regime gate, position sizing validated against trade data; Strategy Rules & System Intent Owner + Product Owner sign-off)

**Problem**
strategy_rules.md §11 defines ATR multiplier, regime gate parameters, and position sizing rules. These parameters have never been formally validated against actual trade outcomes since they were set. BLG-GOV-95 (annual parameter review schedule, v5.2) established that validation should happen annually; this item is the first instance of that schedule.

**Scope**
- Pull all closed trades from production database; compute per-parameter outcomes
- For ATR multiplier: was the initial stop placed correctly against ATR? Did trailing stop advances follow the multiplier?
- For regime gate: how many entries were blocked by the regime gate? Of those that were allowed, what was the pass rate?
- For position sizing: is the documented formula correctly implemented in the UI?
- Produce a parameter validation document; recommend any changes (or confirm no changes needed)

**Acceptance Criteria**
- Parameter validation document produced for §11 parameters
- Each parameter validated against actual trade data (or documented as "insufficient data if <20 trades")
- Strategy Rules & System Intent Owner sign-off; Product Owner ratifies any recommended parameter changes

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

### BLG-GOV-106 — PT-04 trade count gate re-verification
**Priority:** P1 (High)
**Type:** Governance / Gate Tracking
**Owner:** PMO Lead; Product Owner
**Source:** IDEA-challenger-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 hr)
**Provisional-Target:** Before v5.3 sprint planning seals
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

**Problem**
PT-04 gate requires 20+ closed trades (trades with pnl IS NOT NULL in trade_history). Last formal count: 6 trades at v4.6 audit (2026-05-31). The count has never been updated. If the gate has cleared, PT-04 should enter v5.3 sprint planning. If not, the gate status record should be updated with the current count.

**Scope**
- Query: `SELECT COUNT(*) FROM trade_history WHERE pnl IS NOT NULL`
- Compare against 20-trade gate threshold
- Update PT-04 gate status in current_roadmap.md and backlog.md (BLG-FEAT-25)
- If gate cleared: add PT-04 to v5.3 candidate scope

**Acceptance Criteria**
- Current closed trade count queried and recorded
- PT-04 gate status updated in current_roadmap.md and BLG-FEAT-25
- PMO Lead and Product Owner sign-off on gate status

---

### BLG-GOV-107 — SI-02 frontend activation criteria precision
**Priority:** P2 (Medium)
**Type:** Governance / Gate Tracking
**Owner:** PMO Lead; Product Owner; Head of Engineering
**Source:** IDEA-challenger-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-13, EPIC-03; current_roadmap.md SI-02 entry updated with 3 precise, measurable gate conditions; PMO Lead + Product Owner sign-off)

**Problem**
SI-02 frontend activation is recorded as "~Nov 2026" — a date estimate rather than a measurable gate. Sprint planning for SI-02 frontend cannot be triggered reliably against a vague date. Precise, measurable criteria are needed.

**Scope**
- Define 2-3 specific, checkable conditions that unblock SI-02 frontend sprint planning, e.g.:
  1. 20+ closed trades with linked trade_plans (PT-04 gate condition — SI-02 drift score data quality gate)
  2. SI-02 backend API performance confirmed stable (GET /analytics/behavioural-drift p99 < 2s)
  3. SI-02 drift scores confirmed meaningful (not dominated by noise at current trade volume — per BLG-GOV-92 Phase 2 activation criteria)
- Update SI-02 status in current_roadmap.md with precise gate conditions
- PMO Lead to check these conditions at each release planning kickoff

**Acceptance Criteria**
- SI-02 frontend gate conditions defined (2-3 specific, checkable criteria)
- current_roadmap.md SI-02 entry updated with precise conditions replacing "~Nov 2026"
- PMO Lead and Product Owner sign-off

---

### BLG-GOV-108 — AI model pin update policy (BLG-GOV-64 gap)
**Priority:** P2 (Medium)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance Governance Officer; Head of Engineering
**Source:** IDEA-ai-compliance-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-14, EPIC-03; docs/governance/ai_model_version_pinning_policy.md produced; policy covers trigger, process, sign-offs, 30-day deprecation response timeline; AI Compliance Governance Officer + Head of Engineering sign-off)

**Problem**
BLG-GOV-64 (model pinning policy, v4.2) defines that the model must be pinned explicitly, but does not specify when or how to update the pin. claude-haiku-4-5 was pinned at v4.2 (2026-05-28). As new Claude versions release, there is no governed process for evaluating and performing pin updates.

**Scope**
- Add to BLG-GOV-64 or create a companion document: "AI model pin update policy"
  - Update trigger: when Anthropic releases a new Claude model or deprecates the current pinned model
  - Update process: review release notes for breaking changes, run test suite against new model, document cost/quality trade-off
  - Required sign-offs: AI Compliance Governance Officer + Head of Engineering
  - Timeline: updates must complete within 30 days of deprecation notice

**Acceptance Criteria**
- Model pin update policy documented (in BLG-GOV-64 update or companion doc)
- Policy covers: trigger, process, sign-offs, timeline for deprecation response
- AI Compliance Governance Officer and Head of Engineering sign-off

---

### BLG-GOV-109 — AI audit log retention policy
**Priority:** P2 (Medium)
**Type:** Governance / Data Compliance
**Owner:** AI Compliance Governance Officer; Infrastructure & Operations Owner
**Source:** IDEA-ai-compliance-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-OPS-13 (performance baseline gaps, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-15, EPIC-03; docs/governance/ai_audit_log_retention_policy.md produced; 12-month retention period defined; cleanup mechanism documented; AI Compliance Governance Officer + Infrastructure & Operations Owner sign-off)

**Problem**
claude_audit_log entries have been accumulating since v3.8 with no defined retention period. Without a retention policy: (a) storage costs grow indefinitely, (b) it is unclear which log entries are reliable for compliance purposes vs stale.

**Scope**
- Define retention period for claude_audit_log entries: recommended 12 months (or align with Supabase retention policy from BLG-OPS-53)
- Implement: add a scheduled cleanup job or Supabase row-level TTL for entries older than the retention period
- Document in the AI compliance governance records (docs/compliance/ or existing AI audit log spec)

**Acceptance Criteria**
- Retention policy defined and documented (period, rationale)
- Cleanup mechanism implemented (scheduled job or TTL)
- AI Compliance Governance Officer and Infrastructure & Operations Owner sign-off

---

### BLG-GOV-110 — Arc 4 trade_plan data completeness audit
**Priority:** P2 (Medium)
**Type:** Governance / Data Readiness
**Owner:** Data Model & Domain Schema Owner; Product Owner
**Source:** IDEA-data-model-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3 or before Arc 4 sprint planning (PO-02 gate ~Oct 2026)
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-16, EPIC-03; docs/governance/arc4_trade_plan_data_completeness_audit.md produced; per-field null% computed; Arc 4 data dependency risk assessed; Data Model & Domain Schema Owner + Product Owner sign-off)

**Problem**
Trade plans have been active since v3.1 (3+ months). However, which optional fields (entry_rationale, confirmation_criteria, r_target, setup_type, pre_entry_validation_snapshot) are being consistently populated is unknown. Arc 4 analytics (PO-02 journal pattern recognition, PO-03 behavioural error taxonomy) depend on this data.

**Scope**
- Query trade_plans table: for each optional field, compute null% and non-null% across all records
- Identify fields with > 50% null rate as "data gaps" — these are risky dependencies for Arc 4
- Produce a data completeness report; flag any Arc 4 features that depend on gapped fields
- If gaps are critical: file backlog items for UI/UX improvements to encourage field completion

**Acceptance Criteria**
- Data completeness report produced: per-field null% for all trade_plan optional fields
- Arc 4 data dependency risk assessment included
- Data Model & Domain Schema Owner and Product Owner sign-off

---

### BLG-GOV-111 — v5.3 design gate pre-assessment
**Priority:** P2 (Medium)
**Type:** Governance / Release Planning
**Owner:** Head of UX & Design; Product Owner
**Source:** IDEA-head-of-ux-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 hr)
**Provisional-Target:** Before plan release v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

**Problem**
CLAUDE.md §1 requires a design gate assessment before sprint planning for any release with new UI/UX components. v5.3 candidate scope (governance debt, spec gaps, security, ops) appears to be exclusively backend/governance with no new UI components — but this should be formally assessed rather than assumed.

**Scope**
- Review v5.3 candidate scope from current_roadmap.md RA:v5.3 section
- For each candidate item: does it introduce new UI or UX components? (Yes/No)
- If all items are No: record "Design gate not required" with itemised justification; seal in run_manifest at plan release v5.3
- If any item is Yes: normal design gate process applies

**Acceptance Criteria**
- Design gate pre-assessment document produced (or incorporated into plan release v5.3 run manifest)
- Each v5.3 candidate item assessed for UI/UX dependency
- Head of UX & Design and Product Owner sign-off

---

### BLG-GOV-112 — SI-05 digest weekly cadence review (gate-conditional)
**Priority:** P2 (Medium)
**Type:** Governance / Product Review
**Owner:** Product Owner; Director of Quality
**Source:** IDEA-product-owner-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** After 2026-07-04 SI-05 effectiveness review
**Displacement:** BLG-GOV-85 (Arc 6 §13 pre-assessment boundary doc, gate-conditional) deprioritised.

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

### BLG-GOV-113 — SI-05 Phase 1 effectiveness review protocol (gate-conditional)
**Priority:** P1 (High)
**Type:** Governance / QA Planning
**Owner:** Director of Quality; Product Owner
**Source:** IDEA-director-of-quality-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** Before 2026-07-04 effectiveness review
**Displacement:** BLG-QA-34 (SI-02 test planning, gate-conditional) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-23, EPIC-03; docs/governance/si05_effectiveness_review_protocol.md produced; participants, evidence sources, output format, decision authority defined; Director of Quality + Product Owner sign-off; completed before 2026-07-01 gate)

**Gate criteria:** Must complete before 2026-07-04. BLG-GOV-96 (effectiveness criteria) defines WHAT to measure; this item defines HOW to conduct the review.

**Problem**
BLG-GOV-96 (SI-05 effectiveness measurement criteria, v5.2) defines what to measure at the 2026-07-04 review but does not define the review process: who participates, what evidence is examined, what format the output takes, and what decision authority exists. Without a protocol, the review may be inconsistent.

**Scope**
- Define the SI-05 Phase 1 effectiveness review protocol:
  - Participants: Product Owner + Director of Quality (minimum)
  - Evidence sources: si05_digest_log, BLG-GOV-96 criteria, user feedback (if any), Red Flag Journal view counts post-delivery
  - Output format: a one-page effectiveness review report
  - Decision authority: Product Owner decides whether to proceed with Phase 2 or extend Phase 1 observation
- Protocol must complete by 2026-07-01 (3 days before first review date)

**Acceptance Criteria**
- SI-05 effectiveness review protocol document produced
- Protocol specifies: participants, evidence sources, output format, decision authority
- Must complete by 2026-07-01
- Director of Quality and Product Owner sign-off

---

### BLG-GOV-114 — si05_digest_log schema validation for effectiveness review (gate-conditional)
**Priority:** P1 (High)
**Type:** Governance / Data
**Owner:** Data Model & Domain Schema Owner; Infrastructure & Operations Owner
**Source:** IDEA-data-model-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 hr)
**Provisional-Target:** Before 2026-07-04 effectiveness review
**Displacement:** BLG-GOV-90 (Claude model deprecation monitoring, gate-conditional) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-24, EPIC-03; docs/governance/si05_digest_log_schema_validation.md produced; schema validated as PASS against BLG-GOV-96 criteria; Director of Quality + Data Model & Domain Schema Owner sign-off)

**Gate criteria:** Must complete before 2026-07-04. The effectiveness review relies on si05_digest_log data being complete.

**Problem**
The 2026-07-04 SI-05 effectiveness review (BLG-GOV-96, BLG-GOV-113) will rely on si05_digest_log entries. If the schema is missing fields needed for the review (e.g., send_at timestamp, recipient, status, content_hash), the review will be unable to assess delivery reliability or consistency.

**Scope**
- Review si05_digest_log schema against BLG-GOV-96 effectiveness criteria
- Confirm that the schema captures: send_at, status (SUCCESS/FAILED), recipient, digest content hash or preview
- If any required fields are missing: file an urgent story to add them (before 2026-07-01)
- If schema is complete: record PASS

**Acceptance Criteria**
- Schema validated against BLG-GOV-96 effectiveness criteria fields
- Schema PASS or gap items filed as urgent stories
- Must complete before 2026-07-01 (before review date)
- Data Model & Domain Schema Owner sign-off

---

### BLG-GOV-115 — SI-05 digest actionability metric definition (gate-conditional)
**Priority:** P2 (Medium)
**Type:** Governance / Metrics
**Owner:** Metrics Definitions & Analytics Owner; Infrastructure & Operations Owner
**Source:** IDEA-metrics-analytics-20260607-01 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.4 (gate: 2026-07-04 SI-05 effectiveness review complete)
**Gate criteria:** BLG-GOV-113 (SI-05 Phase 1 effectiveness review protocol) complete — i.e., the 2026-07-04 effectiveness review has been conducted

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

*Release Slice v4.6 removed — cycle 2026-05-30__release-v4.6 closed 2026-05-31. Archived canonical home: claude/cycles/2026-05-30__release-v4.6/stage4_backlog_slice.md*

---

*Release Slice v4.8 removed — cycle 2026-06-01__release-v4.8 closed 2026-06-02. Archived canonical home: claude/cycles/2026-06-01__release-v4.8/stage4_backlog_slice.md*

---

*Release Slice v4.9 removed — cycle 2026-06-02__release-v4.9 closed 2026-06-02. Archived canonical home: claude/cycles/2026-06-02__release-v4.9/stage4_backlog_slice.md*

---

*Release Slice v5.0 removed — cycle 2026-06-03__release-v5.0 closed 2026-06-03. Archived canonical home: claude/cycles/2026-06-03__release-v5.0/stage4_backlog_slice.md*

---

## Release Slice v5.2 — cycle 2026-06-08__release-v5.2

<!-- release-plan-marker: RP:v5.2:2026-06-08__release-v5.2 -->

**Canonical home:** claude/cycles/2026-06-08__release-v5.2/stage4_backlog_slice.md

| ST-ID | EPIC | Description | Priority | Delegation |
|-------|------|-------------|----------|-----------|
| ST-01 | EPIC-01 | OA-01: release_planning_prompt.md §-1.2 STEP 8.1 Option(b) patch | P1/OA | autonomous |
| ST-02 | EPIC-01 | OA-02: execution_prompt.md §3.1.A test-authoring spec_references guidance | P1/OA | autonomous |
| ST-03 | EPIC-01 | BLG-SPEC-47: Align SI-05 pass_rate computation with BLG-GOV-86 §5.2 | P3* | autonomous |
| ST-04 | EPIC-01 | BLG-SPEC-48: POST /digest/si05/send API contract gap check and authoring | P1 | autonomous |
| ST-05 | EPIC-02 | BLG-BE-32: SI-05 Telegram delivery retry and failure handling | P2 | delegated_backend |
| ST-06 | EPIC-02 | BLG-BE-33: SI-05 digest delivery log table | P2 | delegated_backend |
| ST-07 | EPIC-02 | BLG-OPS-55: Deployment runbook update for SI-05 | P2 | autonomous |
| ST-08 | EPIC-02 | BLG-OPS-56: SI-05 service scheduled run health check | P2 | autonomous |
| ST-09 | EPIC-03 | BLG-GOV-97: Claude API model deprecation compliance check | P1 | autonomous |
| ST-10 | EPIC-03 | BLG-GOV-98: Telegram bot token security review | P2 | autonomous |
| ST-11 | EPIC-03 | BLG-GOV-99: SI-05 digest endpoint authentication review | P2 | autonomous |
| ST-12 | EPIC-03 | BLG-GOV-100: Backend endpoint coverage audit post-v5.1 | P2 | autonomous |
| ST-13 | EPIC-04 | BLG-QA-46: SI-05 digest edge case test gap analysis | P2 | autonomous |
| ST-14 | EPIC-04 | BLG-QA-47 + BLG-GOV-94: SI-05 acceptance test + delivery verification protocol | P2 | autonomous |
| ST-15 | EPIC-04 | BLG-QA-48: Regression test suite baseline refresh post-v5.1 | P2 | autonomous |
| ST-16 | EPIC-04 | BLG-GOV-96: SI-05 Phase 1 effectiveness measurement criteria | P2 | autonomous |
| ST-17 | EPIC-04 | BLG-FE-64: RFJ design review pre-brief (CONDITIONAL — gate 2026-06-21) | P2 | autonomous |

*BLG-SPEC-47 is P3 severity but mandatory before next SI-05 feature increment (DEV-v51-EPIC01-01)

---

## Release Slice v5.3 — cycle 2026-06-08__release-v5.3

<!-- release-plan-marker: RP:v5.3:2026-06-08__release-v5.3 -->

**Canonical home:** claude/cycles/2026-06-08__release-v5.3/stage4_backlog_slice.md

| ST-ID | EPIC | Description | Priority | Delegation |
|-------|------|-------------|----------|-----------|
| ST-01 | EPIC-01 | BLG-SPEC-53: API contract gap resolution plan for SPEC-49–52 | P1 | autonomous |
| ST-02 | EPIC-01 | BLG-SPEC-54: openapi.yaml completeness audit vs all 50 routes | P1 | autonomous |
| ST-03 | EPIC-01 | BLG-QA-51: QA acceptance criteria for SPEC-49–52 contract stories | P2 | autonomous |
| ST-04 | EPIC-01 | BLG-SPEC-49: GET /ai/journal-summary/history contract + openapi.yaml | P2 | autonomous |
| ST-05 | EPIC-01 | BLG-SPEC-50: GET /analytics/compliance-metrics contract + openapi.yaml | P2 | autonomous |
| ST-06 | EPIC-01 | BLG-SPEC-51: GET /news/{ticker} contract + openapi.yaml | P2 | autonomous |
| ST-07 | EPIC-01 | BLG-SPEC-52: Watchlist endpoint contracts + openapi.yaml + test.py | P2 | autonomous |
| ST-08 | EPIC-02 | BLG-BE-35: POST /digest/si05/send API key authentication | P2 | autonomous |
| ST-09 | EPIC-02 | BLG-OPS-57: SI-05 Telegram delivery failure alerting | P1 | autonomous |
| ST-10 | EPIC-02 | BLG-OPS-58: CI secret scanning gate | P1 | autonomous |
| ST-11 | EPIC-03 | LL-v5.2-P4-01: qa_evidence_template.md signer format note (CF-1) | P1 | autonomous |
| ST-12 | EPIC-03 | LL-v5.2-P4-02: execution_prompt.md STEP 5.3A SSR sub-step (CF-2) | P1 | autonomous |
| ST-13 | EPIC-03 | BLG-GOV-107: SI-02 frontend activation criteria precision | P2 | autonomous |
| ST-14 | EPIC-03 | BLG-GOV-108: AI model pin update policy | P2 | autonomous |
| ST-15 | EPIC-03 | BLG-GOV-109: AI audit log retention policy | P2 | autonomous |
| ST-16 | EPIC-03 | BLG-GOV-110: Arc 4 trade_plan data completeness audit | P2 | autonomous |
| ST-17 | EPIC-03 | BLG-GOV-104: strategy_rules.md §11 parameter validation (first annual) | P2 | autonomous |
| ST-18 | EPIC-04 | BLG-QA-52: Tax year P&L boundary edge case validation | P2 | autonomous |
| ST-19 | EPIC-04 | BLG-QA-53: SI-05 digest Playwright E2E coverage (≥3 scenarios) | P2 | autonomous |
| ST-20 | EPIC-04 | BLG-QA-54: Playwright coverage matrix update post-v5.2 | P2 | autonomous |
| ST-21 | EPIC-04 | BLG-FE-66: Red Flag Journal post-launch UX review | P3 | autonomous |
| ST-22 | EPIC-04 | BLG-FE-67: BLG-FE-64 visual design review scope definition | P2 | autonomous |

*Conditional: ST-23 (BLG-GOV-113), ST-24 (BLG-GOV-114) gate before 2026-07-01; ST-25 (BLG-FE-64) gate 2026-06-21 — add to sprint planning if gates clear.*

---


## Release Slice — v5.4 (cycle: 2026-06-09__release-v5.4)

<!-- release-plan-marker: RP:v5.4:2026-06-09__release-v5.4 -->

**Sprint 1 (firm):**
- ST-01 [EPIC-01]: Add v5.3 new endpoints to api_performance_baseline.md (BLG-OPS-60, S)
- ST-02 [EPIC-02]: Pre-entry panel: separate warn/fail override acknowledgement flow (BLG-FE-56, S)
- ST-03 [EPIC-02]: RFJ visual design review pre-brief (BLG-FE-64, S, gate 2026-06-21)
- ST-04 [EPIC-03]: SI-05 Phase 2 activation criteria definition (BLG-GOV-92, S)

**Sprint 2 (conditional, gate ≥2026-07-04):**
- ST-05 [EPIC-01]: SI-05 p99 production latency baseline review (BLG-OPS-59, S, gate ≥2026-07-04)
- ST-06 [EPIC-03]: SI-05 digest actionability metric definition (BLG-GOV-115, S, gate 2026-07-04)
- ST-07 [EPIC-03]: SI-05 digest weekly cadence review (BLG-GOV-112, S, gate 2026-07-04 + ST-06)

---
