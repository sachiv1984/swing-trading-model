# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-05-31 (Release planning v4.7 — release slice added)
**Last rebalance:** 2026-05-27 (cycle 2026-05-27__scheduled — DL-035; IW-20260527-01; 31 new items: BLG-GOV-57–68, BLG-OPS-36–41, BLG-QA-36–38, BLG-SPEC-41–42, BLG-FE-51–55, BLG-BE-22–24)

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

*Release Slice v4.6 removed — cycle 2026-05-30__release-v4.6 closed 2026-05-31. Archived canonical home: claude/cycles/2026-05-30__release-v4.6/stage4_backlog_slice.md*

---

## Release Slice — v4.7

<!-- release-plan-marker: RP:v4.7:2026-05-31__release-v4.7 -->

| ST | EPIC | Item | Priority | Effort | Sprint |
|----|------|------|----------|--------|--------|
| ST-01 | EPIC-01 | SI-04 §13 formal pre-assessment (BLG-GOV-62) | P1 | S | Sprint 1 (firm) |
| ST-02 | EPIC-01 | SI-05 Phase 1 implementation (BLG-GOV-67) | P2 | M | Sprint 2 (conditional — gate 2026-06-21) |
| ST-03 | EPIC-02 | Arc 5 compliance score in monthly P&L (BLG-FEAT-38) | P2 | M | Sprint 1 (firm) |
| ST-04 | EPIC-03 | Staging deploy live verification (BLG-OPS-28) | P2 | XS | Sprint 1 (firm) |
| ST-05 | EPIC-03 | DS-07 migration staging verification (BLG-OPS-44) | P3 | XS | Sprint 1 (firm) |
| ST-06 | EPIC-03 | Severity field staging verification (BLG-OPS-45) | P3 | XS | Sprint 1 (firm) |
| ST-07 | EPIC-03 | Render log retention policy (BLG-OPS-31) | P2 | S | Sprint 1 (firm) |
| ST-08 | EPIC-04 | Anthropic API tier cost assessment (BLG-OPS-37) | P2 | S | Sprint 1 (firm) |
| ST-09 | EPIC-04 | Pre-entry validation panel UX assessment (BLG-FE-49) | P2 | S | Sprint 1 (firm) |

