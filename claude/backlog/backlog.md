# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-05-21 (cycle 2026-05-21__scheduled — 29 gate-conditional items added: BLG-FEAT-26–35, BLG-FE-39, BLG-BE-13–14, BLG-QA-21–23, BLG-OPS-17–24, BLG-SPEC-32, BLG-GOV-26–29)
**Last rebalance:** 2026-05-21 (cycle 2026-05-21__scheduled — DL-032; 3-cycle cap applied: 29 Promoted-Backlog, 4 Rejected)

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

### BLG-TECH-10 — Fix Yahoo Finance crumb/401 rate-limiting in screener batch
**Priority:** P1 (High)
**Type:** Platform / Technical Debt
**Owner:** Head of Backend Engineering
**Source:** Screener render log analysis — 2026-05-20
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.9

**Problem**
The screener batch service makes concurrent OHLCV requests to Yahoo Finance. Under load, YF returns heavy 401 "Invalid Crumb" and "User is unable to access this feature" errors, causing the majority of US tickers to fail data fetch in a single run. This silently produces degraded screener results — only the tickers whose requests happened to succeed appear. The root cause is that the crumb auth token expires and is not refreshed between requests, and concurrent request volume exceeds YF's tolerance.

**Scope**
- Implement crumb refresh logic: detect 401 responses and re-fetch the crumb before retrying
- Add per-request exponential backoff with jitter on 401/429 responses
- Cap concurrent YF requests to a safe limit (e.g. 5 in-flight at a time)
- Log crumb refresh events and consecutive failure counts for observability

**Acceptance Criteria**
- Screener run against full ticker universe completes without >5% OHLCV failures under normal YF conditions
- A 401 response triggers a crumb refresh and one retry before marking the ticker as failed
- Concurrent request cap is configurable via environment variable
- Crumb refresh events visible in backend logs

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
**Provisional-Target:** v3.9 (conditional — 20+ closed trades gate must be confirmed by Product Owner before sprint planning seals)

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

### BLG-FE-37 — Strip .L suffix from Ticker Universe page display labels
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** Post-sprint QA observation — 2026-05-20
**Effort:** XS (<1h)
**Provisional-Target:** v3.9

**Problem**
The Ticker Universe page displays LSE ticker symbols with the `.L` suffix (e.g. `BATS.L`) because that is how they are stored in the database for identification. This is correct internally but looks unpolished to users — LSE tickers are conventionally displayed without the suffix in UI contexts (e.g. `BATS`). The suffix is meaningful to data sources but irrelevant to a trader reading the page.

**Scope**
- In `TickerUniverse.js`, strip `.L` from the displayed ticker label (not from the underlying value used for API calls)
- DB storage and API payloads remain unchanged

**Acceptance Criteria**
- LSE tickers on the Ticker Universe page display without `.L` suffix
- Ticker symbol sent in API requests (add, delete, toggle) is unchanged (still includes `.L`)
- US tickers are unaffected

---

### BLG-FE-38 — Add degraded-run warning to screener when OHLCV failure rate exceeds 20%
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Head of Backend Engineering; Head of UX & Design
**Source:** Screener render log analysis — 2026-05-20
**Effort:** S (~0.5 days)
**Provisional-Target:** v3.9

**Problem**
When Yahoo Finance rate-limits during a screener run, the majority of US tickers fail OHLCV fetch silently. The screener returns results with no indication that coverage was degraded — a trader sees UK-only or partial results and may act on them without realising most of the universe was excluded. There is currently no way to distinguish a clean full-coverage run from a heavily degraded one.

**Scope**
- In the screener batch service, calculate `ohlcv_failure_rate = failed_tickers / total_tickers` at run completion
- If `ohlcv_failure_rate > 0.20`, set `degraded_run: true` and `failure_rate: <float>` on the screener run record
- Expose `degraded_run` and `failure_rate` in `GET /screener/results` response
- In the screener frontend, display a visible warning banner when `degraded_run` is true: "Results may be incomplete — {N}% of tickers failed data fetch"

**Acceptance Criteria**
- `degraded_run: true` is set on any screener run where >20% of tickers returned no OHLCV data
- `GET /screener/results` response includes `degraded_run` boolean and `failure_rate` float
- Screener results page shows a warning banner when `degraded_run` is true, citing the failure rate
- Clean runs (failure rate ≤20%) show no banner

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

## 4. Backend & Data Backlog


---

*BLG-AI-02 (Model version contract for AI Journal) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-AI-03 (AI Journal Summarisation quarterly review cadence) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

---

### BLG-BE-10 — Fix sector/industry data dropped in screener batch
**Priority:** P1 (High)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** Post-sprint QA observation — 2026-05-20
**Effort:** XS (<1h)
**Provisional-Target:** v3.9

**Problem**
`screener_batch_service.py` fetches full ticker records from `ticker_universe` (including `sector` and `industry`) but immediately extracts only the ticker string into a list, silently discarding the sector/industry fields. These fields are never passed to `compute_screener_result()`, so screener results are stored with NULL sector and industry for every ticker. Sector/industry-based filtering and display in screener results is therefore always empty.

**Scope**
- In `screener_batch_service.py`, retain the full ticker dict instead of extracting the ticker string only
- Pass `sector` and `industry` from the ticker record when calling `compute_screener_result()`
- Verify screener results now persist non-null sector/industry for tickers that have this data in `ticker_universe`

**Acceptance Criteria**
- Screener results for tickers with sector/industry in `ticker_universe` have non-null sector and industry values
- No change to screener result schema or API contract

---

### BLG-BE-11 — Remove DAY from ticker universe (invalid Yahoo Finance symbol)
**Priority:** P2 (Medium)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** Screener render log — Yahoo Finance 404 for DAY (range=30d) — 2026-05-20
**Effort:** XS (<1h)
**Provisional-Target:** v3.9

**Problem**
The ticker `DAY` (Dayforce Inc., formerly Ceridian) is in `tickers_full_list.csv` and is synced into `ticker_universe` as active. Yahoo Finance returns HTTP 404 for `DAY` on historical data requests (30d range), meaning it consistently fails OHLCV fetch on every screener run, wasting processing time and appearing in the active ticker list despite producing no usable data. Also investigate whether `PHNX.L` is a permanent YF 404 or a transient issue.

**Scope**
- Remove `DAY` from `backend/tickers_full_list.csv`
- Deactivate or delete `DAY` from the `ticker_universe` table via migration or startup cleanup
- Investigate the correct YF symbol for Dayforce Inc. and add back if a valid symbol exists
- Confirm `PHNX.L` status — if consistently 404, apply same treatment

**Acceptance Criteria**
- `DAY` no longer appears in `ticker_universe` active tickers
- No `OHLCV FAILED for DAY` log entries on screener runs
- `tickers_full_list.csv` does not contain `DAY`

---

### BLG-BE-12 — Add company_name column to ticker universe
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering; Head of UX & Design
**Source:** Post-sprint QA observation — 2026-05-20
**Effort:** S (~0.5 days)
**Provisional-Target:** v3.9

**Problem**
The `ticker_universe` table stores only ticker symbol, market, sector, industry, and active status — no company name. `tickers_full_list.csv` already contains company names (e.g. `HOLX,NASDAQ,Hologic`), so the data is available at source. The Ticker Universe management page therefore shows only bare ticker symbols with no human-readable company name, making the list harder to scan for non-technical users.

**Scope**
- Add `company_name TEXT` column to `ticker_universe` table via `ensure_company_name_column()` in `ticker_universe_service.py`
- Backfill `company_name` from `tickers_full_list.csv` for all existing rows on startup
- Populate `company_name` from CSV when syncing new tickers
- Include `company_name` in `GET /ticker-universe` response
- Display company name alongside ticker symbol on the Ticker Universe page

**Acceptance Criteria**
- `ticker_universe` rows have non-null `company_name` for all tickers present in the CSV
- `GET /ticker-universe` response includes `company_name` field
- Ticker Universe page shows company name next to each ticker symbol

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

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add new v2.8/v2.9/v3.0/v3.4 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 (3 endpoints); v3.0 post-ship closure 2026-04-28 OA-v30-01 (5 additional endpoints); v3.1 post-ship closure 2026-05-05 (10 additional endpoints); v3.4 post-ship closure 2026-05-14 (2 additional endpoints); v3.5 post-ship closure 2026-05-15 (2 additional endpoints)
**Effort:** M (~2 days — 22 endpoints total)
**Provisional-Target:** Before next performance baseline review

**Problem**
Twenty-two endpoints shipped in v2.8/v2.9/v3.0/v3.1/v3.4/v3.5 are absent from `docs/ops/api_performance_baseline.md`. Performance re-runs require a live environment and human coordination — baseline updates cannot be automated.

**Scope (updated 2026-05-15):**
- v2.8/v2.9 endpoints (3): `POST /ai/journal-summary`, `GET /ai/journal-summary/history`, `GET /v1beta1/news`
- v3.0 endpoints (5): `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}`, `GET /screener/results`, `POST /screener/run`
- v3.1 endpoints (10): `POST /trade-plans`, `GET /trade-plans/{id}`, `PUT /trade-plans/{id}`, `DELETE /trade-plans/{id}`, `GET /trade-plans/by-position/{position_id}`, `GET /trade-plans/by-ticker/{ticker}`, `GET /research/{ticker}`, `GET /earnings/{ticker}`, `GET /reports/monthly-pnl`, plus any additional v3.1 routes
- v3.4 endpoints (2): `GET /portfolio/drawdown-status`, `GET /portfolio/concentration-status`
- v3.5 endpoints (2): `GET /portfolio/paper-positions`, `GET /trades/{trade_id}/plan-vs-reality`
- Run each against staging to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- All 22 endpoints have p50 and p95 latency entries in the baseline document
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

### BLG-GOV-25 — Add --dry-run support to plan release and run delivery verification engines
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Audit AUD-2026-05-21-004 — 2026-05-21
**Effort:** M (~1–2d)
**Provisional-Target:** v3.9

**Problem**
`plan release` and `run delivery verification` are both absent from the §13 dry-run capability table in `shared_standards.md`. `plan release` is the highest-cost engine at approximately 8,232 tokens/run; a failed run that a dry-run could have caught wastes full context and requires a complete re-execution. `run delivery verification` cross-checks all cycle artefacts and similarly has no safe preview mode. Without dry-run support, there is no low-cost way to validate pre-conditions before committing to full engine execution.

**Scope**
- Add `--dry-run` flag handling to `release_planning_prompt.md`: validate inputs, check artefact availability, report what would be created — no writes
- Add `--dry-run` flag handling to `delivery_verification_prompt.md`: validate inputs, report which checks would run — no writes
- Add two rows to `shared_standards.md` §13 dry-run table for `plan release` and `run delivery verification`
- Bump versions on all three files per §6 governance checklist

**Acceptance Criteria**
- `plan release --version vX.Y --dry-run` exits cleanly with a preflight summary and no artefact writes
- `run delivery verification --cycle <id> --dry-run` exits cleanly with a check inventory and no artefact writes
- Both commands appear in the §13 dry-run table in `shared_standards.md`
- All three modified files have bumped version headers and `prompt_change_log.md` entries

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


