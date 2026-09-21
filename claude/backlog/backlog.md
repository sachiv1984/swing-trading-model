# Product Backlog — Momentum Trading Assistant

<!-- last-spec-debt-deep-review: 2026-09-14__release-v9.4 -->

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-09-21 (Sprint Execution `2026-09-21__release-v9.6` EPIC-01 — 7 new items filed from execution findings: BLG-SPEC-161/162, BLG-FE-184/185, BLG-OPS-168, BLG-QA-188/189; BLG-QA-188 wording corrected to name the staging database); prior — 2026-09-21 (Release Planning `2026-09-21__release-v9.6` STEP 4 — 32-item / 28.00-day release slice appended, marker `RP:v9.6:2026-09-21__release-v9.6`); prior — 2026-09-19 (roadmap rebalance `2026-09-19__scheduled` — idea intake `IW-20260919-01` dispositioned: 37 items filed (`BLG-AI-07`, `BLG-API-04/05`, `BLG-BE-121/122`, `BLG-FE-180–183`, `BLG-FEAT-96–98`, `BLG-FR-04/05`, `BLG-GOV-338–345`, `BLG-OPS-165–167`, `BLG-QA-182–187`, `BLG-SEC-37/38`, `BLG-SPEC-157–160`); `BLG-GOV-329` P3→P2); prior history retained — see prior entries in version control.
**Last rebalance:** 2026-09-19 (cycle 2026-09-19__scheduled — DL-080; 0 active initiatives, CPS=N/A; idea intake IW-20260919-01 (44 submissions, 22 agents): 41 Promoted-Backlog (36 items after 4 consolidations), 2 Parked-cycle-1, 1 Rejected; PVR 0.046 🔴 Alert (3rd consecutive, new low, U=9/G=60/D=122/P=4 of 195, window v9.1–v9.5); Skill-Silo 98.8% (5th consecutive worsening) — PO committed `BLG-FEAT-96`/`97` (P2) as the ≥2 build-and-ship U-items; STEP 8.1 Option (b) defer, 6th consecutive)

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

### BLG-FEAT-30 — Screener-to-trade attribution pipeline & retrospective analytics (consolidated)
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-05 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032); consolidates BLG-FEAT-27 (retrospective quality/win-rate analysis) and BLG-FEAT-28 (hit-rate metric) — both are reporting views over the same attribution linkage this item builds; filed together in the same 2026-04-21 idea batch but scoped as if independently buildable, when in practice all three need the same underlying instrumentation — merged 2026-07-27, session duplicate-consolidation cleanup
**Effort:** L (~3–4 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days AND ≥ 60 closed trades with screener attribution (the more demanding of the original gate conditions — the merged retrospective/quality-correlation scope needs both).

**Problem**
The full pipeline from screener hit → watchlist add → research → trade plan → execution → close is not yet instrumented end-to-end. Attribution gaps prevent retrospective analysis of conversion rates at each stage, make it impossible to evaluate whether the screener generates genuinely high-quality candidates vs high-volume noise, and leave no aggregate hit-rate metric available — all needs originally filed as three separate items requiring the same underlying linkage.

**Scope**
- Full attribution model: screener_run_id linkage through to trade close
- Conversion funnel: screener → watchlist → plan → closed
- Aggregate hit-rate metric: screener_candidates_total, advanced_to_watchlist, advanced_to_trade_plan, advanced_to_closed_trade — displayable in governance/operations reporting view
- Retrospective metric: screener hit rate and win rate of attributed trades vs baseline, filterable by screener run date range
- Exportable for offline analysis

**Acceptance Criteria**
- Full attribution pipeline implemented; conversion funnel metrics computable
- Hit-rate metric computed and displayable
- Screener hit rate and attributed-trade win rate reportable, filterable by date range
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

> ⚠️ **Partially pre-met (backlog audit 2026-08-13):** The gate has cleared and most of the core scope already shipped — `backend/services/plan_vs_reality_service.py` (`GET /trades/{id}/plan-vs-reality`) already links trades to their governing plan and computes `r_achieved` vs `r_target` (`r_delta`) per closed trade, contradicting this item's problem statement that the comparison "cannot currently be attributed." Only the aggregate "plan-adhered vs plan-deviated outcome comparison" scope bullet appears unbuilt. Recommend Product Owner narrow this item to that residual aggregate-reporting scope at next `groom backlog`/`plan release`.

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

> ⚠️ **Partially pre-met (backlog audit 2026-08-13):** `entry_delta_pct` is already captured at trade close (`backend/services/plan_vs_reality_service.py::_compute_entry_delta_pct()`), contradicting this item's problem statement that it "is not yet captured." Half the gate condition is therefore met — only the ≥20-linked-trades count remains to verify. The discipline metric and R-multiple correlation reporting layer remain unbuilt. Recommend Product Owner re-check the trade-count gate and narrow this item to the reporting-layer scope if still open.

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

### BLG-FEAT-55 — AI chat conversation history persistence across sessions
**Priority:** P3 (Low)
**Type:** Product Feature / AI
**Owner:** Product Owner; Data Model & Domain Schema Owner
**Source:** IDEA-product-owner-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥30 days of AI chat usage (v6.2 shipped 2026-06-25; clears ~2026-07-25) AND a §13 review opened and passed for persistence design (chat is currently stateless per SRB-v1.7).

**Problem**
POST /ai/chat (shipped v6.2) is stateless — no conversation history persists across sessions. Users who want to continue a prior chat thread cannot. Persisting history is a genuine schema and §13 boundary question (stored AI conversation content) that should not be designed ahead of both an established usage pattern and a formal boundary review.

**Scope**
- §13 review: does persisting chat history change SRB-v1.7's stateless-advisory classification?
- Schema design: chat session/message data model (companion to BLG-SPEC-65/66)
- Frontend: session list, resume-conversation UX

**Acceptance Criteria**
- §13 review passed before design begins
- Chat session schema designed and reviewed by Data Model & Domain Schema Owner
- Gate condition (30 days usage) verified by Product Owner before sprint planning

---

### BLG-FEAT-57 — Strategy parameter sensitivity analysis framework
**Priority:** P3 (Low)
**Type:** Product Feature / Strategy Analytics
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** L (~3–4 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥20 closed trades (currently ~15–17) AND Arc 5/6 tooling prerequisite in place.

**Problem**
There is no systematic pre-process to evaluate the effect of a §11 strategy parameter change (e.g. ATR multiplier) against historical trade data before committing to a version bump. Building this ahead of sufficient trade density or the Arc 5/6 analytical foundation would produce statistically unreliable output.

**Scope**
- Sensitivity analysis: apply candidate parameter values against historical trade set, compare outcome deltas
- Feeds into SI-04 (Strategy Version Comparison) as a pre-change evaluation step

**Acceptance Criteria**
- Framework produces before/after outcome comparison for a candidate parameter change
- Gate condition (≥20 closed trades) verified by Strategy Rules & System Intent Owner before sprint planning

---

### BLG-FEAT-58 — Trade annotation model
**Priority:** P3 (Low)
**Type:** Product Feature / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Arc 4 PO-02 (Journal Pattern Recognition) data model established (~2026-10-20, 6+ months AI-summarised journal data).

**Problem**
No schema exists for user-authored free-text annotations on individual trades, distinct from the AI-summarised journal entry. Designing this ahead of PO-02's data model risks a schema that conflicts with or duplicates the eventual journal-pattern data structure.

**Scope**
- `trade_annotations` schema: trade_id, annotation_text, created_at, tags (optional, see BLG-FEAT-52)
- Co-designed with PO-02 data model once that gate clears

**Acceptance Criteria**
- Schema co-designed with PO-02 data model, not ahead of it
- Gate condition (PO-02 data model established) verified before sprint planning

---

### BLG-FEAT-59 — AI-assisted monthly P&L narrative
**Priority:** P3 (Low)
**Type:** Product Feature / AI
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 (same constraint as BLG-FEAT-55/56 — too early to layer additional AI-generated content onto financial reporting).

**Problem**
Monthly P&L (shipped v2.x) is a fixed-format report. An optional AI-generated narrative commentary could add interpretive value, but adding it before existing AI features (daily briefing, chat) are validated risks compounding unvalidated AI surface area onto a financial-reporting document specifically.

**Scope**
- Optional AI narrative section appended to Monthly P&L using existing Claude infrastructure
- Advisory-only framing consistent with §13 SRB-v1.7

**Acceptance Criteria**
- Narrative section renders as optional/dismissible
- Gate condition (AI adoption window) verified by Financial Reporting & Records Owner before sprint planning

---

### BLG-FEAT-60 — AI chat engagement metric
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 — usage patterns remain unestablished at current usage duration; metric definition would be premature.

**Problem**
No metric tracks AI chat engagement (sessions per week, questions per session, response acceptance rate). Defining the metric before usage patterns stabilise risks needing early revision.

**Scope**
- Define engagement metric set: sessions/week, questions/session, response-acceptance rate
- Document in `metrics_definitions.md`

**Acceptance Criteria**
- Metric set defined and documented
- Gate condition (AI adoption window) verified before sprint planning

---

### BLG-FEAT-73 — SI-02 Behavioural Drift Detection — frontend build
**Priority:** P1 (High)
**Type:** Product Feature / Frontend, gate-conditional
**Owner:** Head of Engineering; Head of UX & Design
**Source:** Feature-gap review (current_roadmap.md Arc 5 status table cross-referenced with BLG-GOV-107, BLG-BE-46, BLG-BE-52) — 2026-07-10
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled — do not re-check before 2026-11-09 or 10 new linked trade_plans, whichever first (PO disposition 2026-08-17, see below); `[gate status unverified/unmet]` — BLG-GOV-107 gate conditions last confirmed NOT MET 2026-07-21 (9th consecutive identical reading); not independently reconfirmed since; may not enter sprint planning until independently reconfirmed met
**Depends on:** BLG-FE-56, BLG-FE-57, BLG-FE-58, BLG-FE-59 (UI extension specs); BLG-BE-27, BLG-BE-29 (perf baseline, index review) — all currently gate-conditional on this item entering sprint planning

> ⚠️ **PO disposition — re-check cadence reset (2026-08-17, ad hoc session, acting Product Owner per explicit user direction):** Reviewed without a fresh live query (this session has no production DB/API credentials — dev-only `.env`, consistent with every prior in-session attempt, e.g. `2026-07-24__release-v7.8` run_manifest's 401). Decision: remain excluded from firm scope, **and** stop the every-cycle identical-reading re-check pattern (9 consecutive NOT MET readings 2026-07-12→2026-07-21, zero movement, each one a wasted live-query cycle). Rationale for the reset: gate Condition 1's root cause (0/11 linked `trade_plans`) was structurally fixed by `BLG-BE-91` (enforce trade-plan linkage at position entry — shipped v8.6, 2026-08-11), so the blocker is no longer "nothing is being linked," it's "not enough time/volume has passed since the fix went live" — only 6 days as of this session, nowhere near enough for ≥20 *new* closed, linked trades to accrue. Re-checking every cycle in the meantime cannot produce a different reading and has already cost 9 cycles of live-query overhead. New re-check trigger: **no earlier than 2026-11-09** (90 days post-`BLG-BE-91` ship, a realistic accrual window at this system's trade volume) **or** when a cheap milestone check (10 new `trade_plans` rows created with `position_id` populated post-2026-08-11) is hit, whichever comes first — PMO Lead to action per its existing gate-recheck ownership (`current_roadmap.md` SI-02 entry). This item remains Arc 5's flagship "tell me when I'm deviating from my own rules" feature (backend live since v4.6, zero UI) — once the gate clears this should be a near-immediate sprint-planning candidate, not re-litigated from scratch.

**Problem**
The behavioural drift detection backend service shipped in v4.6 and computes drift scores from `trade_history`/`trade_plans` window functions, but no frontend was ever built to surface it — there is no UI showing drift scores, trend, or explanation anywhere in the app. This is Arc 5's flagship "tell me when I'm deviating from my own rules" feature, and it is currently invisible to the user despite the backend existing and running.

**Scope**
- Drift score display card(s) in `Arc5ComplianceSection`, per the existing extension-point spec (BLG-FE-59)
- Historical trend view for drift score over time
- Plain-language explanatory copy for what a drift score means and what action it implies

**Acceptance Criteria**
- User can view current drift score(s) in the Arc 5 compliance UI
- User can see a historical trend of drift score over time
- Each score is accompanied by plain-language explanation of contributing factors
- Feature does not enter sprint planning until all 3 BLG-GOV-107 gate conditions are independently reconfirmed met: (1) ≥20 closed trades with **linked** trade_plans (`trade_plans.position_id` populated) — note this gate can only clear via new trade_plans created going forward, since BLG-BE-52 declined to backfill the 11 pre-existing unlinked rows; (2) `GET /analytics/behavioural-drift` p99 < 2s stable over a 7-day window; (3) drift scores show non-trivial variance across trades (not all 0 or 1.0)

---

### BLG-FEAT-74 — PO-05 Lightweight Replay Mode
**Priority:** P1 (High) — escalated from P2, 2026-07-27, session product review (see note below)
> ⚠️ **Priority escalation (2026-07-27):** Raised P2→P1 during a session backlog review — the roadmap itself names this "the highest-value long-term validation feature" in Arc 4. Escalation reflects value judgment only; the §13 pre-clearance and effort-phasing conditions in this item's own scope note still apply before sprint entry.
**Type:** Product Feature / Backend + Frontend, gated
**Owner:** Head of Engineering; Product Owner
**Source:** Feature-gap review (current_roadmap.md §5 Arc 4, PO-05 — flagged as unbacklogged) — 2026-07-10
**Effort:** VH (>2 weeks)
**Provisional-Target:** Unscheduled (gated — §13 determinism pre-clearance not yet run)
**Depends on:** IT-06 Alpaca Paper Trading Integration (shipped v3.5) — foundational infrastructure this feature reuses

> PO re-deferral 2026-08-21: `Provisional-Target` corrected from the stale `v7.7` anchor (DL-074, named 2026-07-21, shipped 2026-07-24 without this item ever entering a sprint) to `Unscheduled (gated)`, matching the item's actual state — the real blocker is that nobody has run the §13 determinism pre-clearance review yet, not a scheduling gap per se. Priority remains P1 and the roadmap's "highest-value long-term validation feature" framing stands; this item should be re-targeted to a specific release once the §13 pre-clearance review (Strategy Rules & System Intent Owner) is scheduled and completed, not before.

**Problem**
The roadmap names this "the highest-value long-term validation feature" in Arc 4, but no backlog item exists for it at all. There is currently no way for the user to test how a candidate strategy-rule change would have performed historically, or to replay a specific past setup/period against the paper-trading infrastructure that already exists and is otherwise unused for this purpose.

**Scope**
- §13 compliance pre-clearance: confirm the feature is a deterministic replay of the user's own historical data, not a predictive simulation (precedent: PS-03 Monte Carlo's determinism framing; IT-06's four binding conditions as a template for the review)
- Backend: replay a historical window of the user's own trade/candidate history through the existing paper-trading mechanics under the *current* rule set
- Frontend: date range or trade-set selector, and a clearly-labelled retrospective/deterministic output view
- Exact scope (single trade replay vs. full historical window, output format) to be confirmed by canonical spec before implementation, per the roadmap's Standing Notice

**Acceptance Criteria**
- User can select a historical date range or trade set and run it through paper-trading mechanics under current strategy rules
- Output is clearly labelled as retrospective/deterministic, not predictive
- §13 pre-clearance review completed and documented before sprint planning begins

---


### BLG-FEAT-76 — SI-05 Weekly Strategy Integrity Digest — Phase 2 (full digest)
**Priority:** P3 (Low)
**Type:** Product Feature / Backend + Frontend, gate-conditional
**Owner:** Head of Engineering; Head of UX & Design
**Source:** Feature-gap review (current_roadmap.md Arc 5 status table cross-referenced with BLG-FE-69, BLG-FE-71, BLG-GOV-121 — prep-only, no primary Phase 2 item existed) — 2026-07-10
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled (gated)
**Depends on:** BLG-FEAT-73 (SI-02 frontend) and BLG-FEAT-75 (SI-04) — hard-blocked on both shipping first; BLG-FE-69, BLG-FE-71, BLG-GOV-121 are prep items for this build

**Problem**
Only Phase 1 shipped (v5.0/v5.1) — a lightweight Telegram-only digest. The full-scope digest, incorporating SI-02 drift scores and SI-04 version comparison data, has prep items filed but no primary "build Phase 2" item ties them together, so this content will not exist even once its dependencies ship unless the digest itself is scoped and built.

**Scope**
- Extend the existing Telegram digest (or add an in-app channel, pending the Phase 2 channel decision referenced by BLG-FE-69/71) to include SI-02 drift score summaries and SI-04 version comparison highlights
- Sequenced explicitly last of the 5 items in this batch — must not enter sprint planning before SI-02 and SI-04 ship

**Acceptance Criteria**
- Weekly digest includes a drift score summary line
- Weekly digest includes a brief before/after comparison note when a strategy version change occurred in the reporting period
- Phase 2 channel decision (Telegram-only vs. added in-app view) resolved before frontend work begins

---


## 3. Frontend & UX Backlog

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

### BLG-FE-43 — SI-05 Weekly Digest frontend component spec
**Priority:** P1 (High) — escalated from P2, 2026-07-27, session product review (see note below)
> ⚠️ **Priority escalation (2026-07-27):** Raised P2→P1 during a session backlog review as the highest-priority Frontend/UX item. Note this item is a component spec (pre-work), not a shippable feature — its own gate criteria (SI-05 sprint planning imminent) still govern entry.
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
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
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

### BLG-FE-54 — Arc 5 unified pre-entry gateway
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
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

### BLG-FE-58 — Pre-entry panel: check grouping for Arc 5 expansion
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
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
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
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
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
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
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
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

### BLG-FE-68 — Arc 5 compliance score sparkline trend chart (gate-conditional)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
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
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
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
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
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
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
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

### BLG-FE-83 — Frontend bundle size optimization assessment
**Priority:** P3 (Low)
**Type:** Frontend / Performance
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** A user-reported performance issue OR profiling data indicates bundle-size impact.

**Problem**
No formal assessment of current React bundle size or heavy dependencies has been performed. No user-reported issue currently motivates this — the gate exists specifically to avoid speculative optimisation work.

**Scope**
- Bundle analysis (e.g. source-map-explorer or equivalent) to identify heaviest dependencies
- Recommendations report; no implementation required at this stage

**Acceptance Criteria**
- Bundle analysis report produced
- Gate condition (reported issue or profiling signal) verified before commencing

---

### BLG-FE-84 — AI chat UI interaction study protocol
**Priority:** P3 (Low)
**Type:** Frontend / UX Research
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 — usage patterns must stabilise before a research protocol targeting them is designed.

**Problem**
No structured protocol exists to study how the AI chat advisor is actually used. Designing one before interaction patterns stabilise risks studying patterns that later shift.

**Scope**
- 5-question interaction study protocol targeting chat advisor usage
- Applied once gate clears

**Acceptance Criteria**
- Protocol document produced
- Gate condition (AI adoption window) verified before use

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

### BLG-QA-42 — SI-02 E2E Playwright test strategy and scaffold (consolidated)
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038); consolidates BLG-QA-55 — a readiness-assessment follow-up on this item's own scaffold, gated on the same 20+ closed-trades condition — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed. BLG-QA-37 (Playwright mock strategy for drift features, shipped v4.2) defines the approach — this item implements it.

**Problem**
SI-02 drift service (35 unit tests, shipped v4.6) has no E2E Playwright coverage. When the frontend ships (~2027-Q1), test coverage must be ready immediately. Pre-building the scaffold 1–2 cycles before activation avoids rushed test creation under sprint pressure.

**Scope**
- Define E2E test strategy for GET /analytics/behavioural-drift (per BLG-QA-37 Playwright mock strategy)
- Scaffold Playwright test file with scenarios: drift scores render, gate-not-met state, all 4 metric cards display
- Confirm mock data approach (per BLG-QA-37 mock strategy)
- Once the 20+ closed-trades gate clears and SI-02 frontend enters sprint planning: re-review this scaffold against the final drift service implementation (which may have evolved since authoring) and confirm the mock strategy is still valid before sprint entry

**Acceptance Criteria**
- E2E test strategy document produced
- Playwright test scaffold created and passing against mock data
- All 4 drift metric display scenarios covered
- Gate condition verified before sprint planning
- Pre-sprint-entry readiness confirmation recorded: "proceed with scaffold as-is" or a revision document produced, with Director of Quality sign-off

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

### BLG-BE-42 — Backend request tracing
**Priority:** P3 (Low)
**Type:** Backend Engineering / Observability
**Owner:** Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** A demonstrated multi-service call failure requiring cross-service tracing to diagnose.

**Problem**
No per-request trace ID propagation exists across routers/services. No incident has yet demonstrated a need for this level of observability — the gate exists to avoid speculative infrastructure investment.

**Scope**
- Trace ID generation at request entry; propagation through service-layer calls
- Surfaced in structured logs

**Acceptance Criteria**
- Trace ID present in logs across a multi-service call path
- Gate condition (demonstrated failure requiring tracing) verified before commencing

---

### BLG-BE-66 — Index review pass for trade_plan queries as row count grows
**Priority:** P3 (Low) | **Type:** Backend / Data Model | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260717-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `trade_plans` row count is currently small (11 rows per live check 2026-07-17) so no index pressure exists yet, but several endpoints join or filter on `position_id`/`ticker`/`status` without a confirmed index review.
**Scope:** A lightweight index audit against current query patterns, to be actioned proactively rather than reactively once row count grows materially.
**Acceptance Criteria:** Audit completed; any missing indexes identified (implementation deferred if no current performance impact, per gate below).
**Gate criteria:** Revisit when `trade_plans` row count exceeds ~500 or any query is observed exceeding baseline latency — not urgent at current scale.

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
**Provisional-Target:** ~v4.9 (date-gated)
**Gate criteria:** No earlier than 2026-11-01 (~6 months after BLG-OPS-36 scope review in v4.2, 2026-05-28)

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


### BLG-GOV-29 — Trade plan AI summary audit log
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; QA Lead
**Source:** IDEA-governance-20260421-04 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** AI trade plan analysis feature scoped and scheduled (i.e., a story exists in the backlog that adds AI-generated trade plan summaries or analysis).

> ⚠️ **Partially pre-met (backlog audit 2026-08-13):** The gate has cleared — `POST /trade-plans/{plan_id}/generate-thesis` (backend/routers/trade_plans.py) already generates AI trade plan summaries via Claude, and already logs to an append-only `claude_audit_log` table (backend/database.py::ensure_claude_audit_log_table) with `endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd, generated_at`. This covers the item's intent but uses different field names than the AC's proposed schema (`plan_id, model_version, prompt_version, input_hash, output_hash`) and no explicit 90-day retention policy is confirmed for this specific table. Recommend Product Owner confirm whether the existing `claude_audit_log` schema satisfies this item's governance requirement as-is, or whether the field-level gap needs closing.

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

### BLG-OPS-53 — Application log retention policy expansion (Supabase + claude_audit_log)
**Priority:** P3 (Low)
**Type:** Operations / Data Lifecycle
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-infra-ops-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** claude_audit_log table 6+ months old (~Nov 2026, since v4.0 ship 2026-05-22). BLG-OPS-31 (Render log retention policy) shipped v4.7; this extends scope to Supabase query logs and claude_audit_log.

> ⚠️ **Partially pre-met (backlog audit 2026-08-13):** `docs/governance/ai_audit_log_retention_policy.md` already defines a 12-month rolling retention period with an automated purge function — satisfying the `claude_audit_log` half of this item's scope verbatim (the item's own example: "12 months rolling"). The Supabase-query-log retention definition and archiving-trigger scope remain open. Recommend Product Owner narrow this item to the Supabase-log sub-scope at next `groom backlog`/`plan release`.

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

### BLG-GOV-90 — Claude model deprecation monitoring procedure (consolidated)
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Source:** IDEA-ai-compliance-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038); consolidates BLG-GOV-239 — same "track Claude model deprecation on a defined schedule" capability, independently re-proposed as a standalone calendar at the 2026-07-16 idea-intake cycle without cross-reference to this existing item — merged 2026-07-28, session duplicate-consolidation cleanup
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

### BLG-GOV-95 — strategy_rules.md annual parameter review schedule (consolidated)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Source:** IDEA-strategy-owner-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039); consolidates BLG-GOV-122, BLG-GOV-187 — the same "§11 production parameter review against live trading data" capability was independently re-proposed across two later idea-intake cycles (2026-06-10 and 2026-07-08) without cross-reference to this existing item or each other — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-GOV-29 (trade plan AI audit log, P3, gate-conditional) deprioritised.

**Gate criteria:** Whichever comes first: ≥ 30 closed trades with ATR-based stop exits in production (sufficient data density to assess parameter appropriateness), OR 12 months elapsed since parameters were last reviewed, OR the annual review cadence date if neither condition has fired sooner.

**Problem**
strategy_rules.md §11 defines production parameters (5× initial ATR, 2× profitable ATR, 10-day grace period, regime gate thresholds). These have never been reviewed against live trading performance data — the system has run on its original parameter settings since inception (last validated at v5.3, BLG-GOV-104, not against realised outcomes). §12.3 requires documented rationale for any parameter change, but there is no scheduled review mechanism to surface whether changes are warranted.

**Scope**
- Define annual parameter review process: PMO Lead adds review to the next roadmap rebalance after the gate clears
- Review actual trading behaviour over the review window against each parameter's assumptions; identify any divergence between documented parameters and actual practice
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
**Provisional-Target:** Gate-conditional — first review due 2026-09-24, not yet due

**Gate criteria:** First review due 2026-09-24 (90 days post-v6.2 ship 2026-06-25). Quarterly cadence thereafter.

> **Product Owner note (2026-08-21, post-ship closure `2026-08-17__release-v8.9` STEP 12 review):** This item was flagged by `groom backlog`'s Deferral Age Validation as a stale-target/kill candidate because its `Provisional-Target` field still read the leftover placeholder `v6.3` (long since shipped). That flag was a false positive — the item's own `Gate criteria` field is the actual operative schedule, and 2026-09-24 has not yet arrived. Not neglected, not a kill candidate. `Provisional-Target` corrected above to avoid re-triggering the same false-positive check at the next groom run.

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
**Provisional-Target:** Gate-conditional — schedule within 90 days of v6.2 ship, due 2026-09-24, not yet due

**Gate criteria:** Schedule within 90 days of v6.2 ship (by 2026-09-24).

> **Product Owner note (2026-08-21, post-ship closure `2026-08-17__release-v8.9` STEP 12 review):** This item was flagged by `groom backlog`'s Deferral Age Validation as a stale-target/kill candidate because its `Provisional-Target` field still read the leftover placeholder `v6.3` (long since shipped). That flag was a false positive — the item's own `Gate criteria` field is the actual operative schedule, and 2026-09-24 has not yet arrived. Not neglected, not a kill candidate. `Provisional-Target` corrected above to avoid re-triggering the same false-positive check at the next groom run.

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

### BLG-GOV-144 — Agent role charter annual review schedule (consolidated)
**Priority:** P3 (Low)
**Type:** Governance Process / HR
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057); consolidates BLG-GOV-182, BLG-GOV-199, BLG-GOV-236 — the same "periodic role-charter freshness review" capability was independently re-proposed across three later idea-intake cycles (2026-07-08 through 2026-07-15) without cross-reference to this existing item or each other — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Time-gated — first review due 2027-06-26 (annual cadence from first filing). A lighter-weight spot-check may also be run at any 10-cycle interval in the interim (per the absorbed BLG-GOV-236 proposal), without waiting for the full annual date.

**Problem**
Agent role charter files (`claude/agents/*.md`) define role responsibilities and decision authorities. As the governance system evolves, role definitions may become stale — including drift against current tooling and practice (e.g. `gh` CLI usage, current write-scope conventions). Without a scheduled review cadence, charter drift accumulates silently. An annual review, with a lighter interim spot-check, ensures each role definition remains current.

**Scope**
- Author an annual review procedure for all `claude/agents/*.md` charter files
- Schedule first review: 2027-06-26
- Procedure: review each charter for accuracy and continued relevance to current tooling/practice; propose amendments through Head of Specs Team; record in prompt_change_log.md
- Optional lighter interim spot-check every 10 cycles, flagging any staleness found as a follow-up ahead of the next full annual review

**Acceptance Criteria**
- Annual review procedure documented
- First review date: 2027-06-26 recorded
- Director of HR sign-off

---

### BLG-QA-63 — Automated accessibility testing (axe-core) in Playwright CI
**Priority:** P3 (Low)
**Type:** QA / Accessibility
**Owner:** Director of Quality; Head of Frontend Engineering
**Source:** IDEA-director-of-quality-20260619-02 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate criteria:** Arc 5 fully complete (all SI features shipped) — accessibility testing added after frontend feature set stabilises

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

### BLG-OPS-76 — Enhanced health check with external dependency verification
**Priority:** P3 (Low)
**Type:** Operations / Observability
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260619-02 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate criteria:** BLG-OPS-25 (automated staging smoke test) complete AND ≥3 external dependency failures observed in production logs

> ⚠️ **Partially pre-met (backlog audit 2026-08-13):** `backend/services/health_service.py::get_external_api_health()` already surfaces external dependency status (Alpaca/Yahoo Finance — last successful call, error rate, p95 latency) on `GET /health`, and `src/pages/SystemStatus.js` already renders it (shipped v3.0, ST-08/BLG-OPS-12). The literal AC (`?extended=true` opt-in param, unchanged default response) and Anthropic API coverage remain unbuilt. Recommend Product Owner narrow this item's scope to the residual gap at next `groom backlog`/`plan release`, rather than treating it as a from-scratch build.

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
**Gate criteria:** BLG-OPS-71 (system threat model) complete — data provider risk will be enumerated in the threat model

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


### BLG-GOV-156 — Base44 prompt template versioning
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥3 Base44 prompt draft revisions within a single release cycle (current iteration frequency does not warrant versioning overhead).

**Problem**
No versioning exists to track which version of the Base44 generation prompt produced each delivered component. At current low iteration frequency this is not yet a problem, but the gate defines a concrete trigger for when it would become one.

**Scope**
- Lightweight per-revision log (date, summary of change) appended to the Base44 prompt draft file
- No tooling required — a changelog section within the existing prompt file

**Acceptance Criteria**
- Changelog section added once gate condition is met
- Gate condition (≥3 revisions/cycle) verified before commencing

---

### BLG-QA-71 — Playwright fixture isolation tooling
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** First empirical Playwright fixture-isolation failure observed in CI (no such failure has occurred to date).

**Problem**
No test data fixtures or state-reset mechanism exists between Playwright runs. No empirical fixture-isolation failure has occurred — the gate exists to avoid building tooling for a problem not yet demonstrated.

**Scope**
- Fixture reset mechanism between Playwright test runs
- Applied once a real isolation failure is observed

**Acceptance Criteria**
- Fixture isolation tooling implemented once gate condition met
- Gate condition (demonstrated failure) verified before commencing

---

### BLG-SPEC-63 — Spec coverage gap detection script design
**Priority:** P3 (Low)
**Type:** Spec Debt / Tooling
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Head of Specs Team completes a script-design scoping decision (static route diff vs frontend spec inventory approach).

**Problem**
No automated check compares frontend page specs against deployed routes to detect coverage gaps. The scoping approach (static diff vs inventory-based) has not yet been decided.

**Scope**
- Scope and select an implementation approach
- Build a lightweight script to flag routes with no corresponding spec file (or vice versa)

**Acceptance Criteria**
- Scoping decision recorded
- Script implemented and run at least once with findings documented

---

### BLG-SPEC-65 — AI interaction history data model
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Same gate as BLG-FEAT-55 — §13 review opened and passed for chat persistence AND AI adoption window clears ~2026-07-25.

**Problem**
Companion spec item to BLG-FEAT-55 (chat persistence). §13-compliant schema design for persisting user chat sessions must not precede the boundary review itself.

**Scope**
- §13-compliant schema design, co-developed with BLG-FEAT-55
- No implementation ahead of the §13 review passing

**Acceptance Criteria**
- Schema spec produced only after §13 review passes
- Gate condition verified before commencing

---

### BLG-SPEC-66 — AI chat conversation persistence spec
**Priority:** P3 (Low)
**Type:** Spec Debt / Frontend Spec
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Same §13 review gate as BLG-FEAT-55/BLG-SPEC-65.

**Problem**
Companion frontend spec item to BLG-FEAT-55/BLG-SPEC-65 — persisting and displaying chat session history. Authoring this spec ahead of the §13 boundary decision risks rework or discard.

**Scope**
- Frontend spec for session list and resume-conversation UX, authored only once the §13 gate clears

**Acceptance Criteria**
- Spec produced only after §13 review passes
- Gate condition verified before commencing

---

### BLG-OPS-84 — Annual data provider cost comparison review
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Annual cadence — first review due ≥2027-06-25.

**Problem**
No scheduled review compares current data provider (Yahoo Finance, Alpaca) costs against alternatives. Annual cadence is appropriate; the gate simply establishes when the first review is due.

**Scope**
- Cost/feature comparison of current vs alternative data providers
- Recommendation: retain or switch

**Acceptance Criteria**
- Review conducted and documented at gate date
- FinOps & Resource Architect sign-off

---

### BLG-OPS-85 — Compute cost trending by feature area
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** BLG-OPS-74 (Anthropic API cost logging) ships.

**Problem**
No view partitions Render dyno compute cost by feature area. Meaningful cost trending depends on the per-call cost logging BLG-OPS-74 will provide — building this ahead of that data source would have nothing to trend.

**Scope**
- Partition compute cost by feature area (AI endpoints, screener, core CRUD) once BLG-OPS-74 data is available

**Acceptance Criteria**
- Cost trending view implemented and populated
- Gate condition (BLG-OPS-74 shipped) verified before sprint planning

---

### BLG-FEAT-61 — Screener-to-watchlist promotion friction audit
**Priority:** P3 (Low)
**Type:** Product Feature / UX Research
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A user-reported friction signal on the DS-07 promotion flow, or an observed drop in promotion-to-watchlist conversion rate.

**Problem**
DS-07 (screener → watchlist promotion) has been unchanged since v3.0 with no reported usage issue. Auditing it now would be speculative.

**Scope**
- Review promotion flow usage once a friction signal exists
- Recommend UX changes if warranted

**Acceptance Criteria**
- Audit conducted and documented only after gate signal observed

---

### BLG-FEAT-62 — Trade plan template presets by setup type
**Priority:** P3 (Low)
**Type:** Product Feature
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥20 closed trades captured post-PT-04 (2026-06-23) with sufficient `setup_type` diversity to justify presets (at least 3 distinct setup types with ≥3 trades each).

**Problem**
PT-04 (Setup Quality Score) is live, but trade volume since its gate clearance is too low to know which setup-type presets would actually be useful.

**Scope**
- Analyse `setup_type` distribution once gate clears
- Design preset templates for the most common setup types

**Acceptance Criteria**
- Preset design only commences after gate condition confirmed

---

### BLG-GOV-171 — Spec staleness scan across owning code paths
**Priority:** P3 (Low)
**Type:** Governance / Spec Debt
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** A staleness-threshold definition (e.g. "spec unedited N releases while its code path changed") is authored first — this item is the scan itself, not the threshold definition.

**Problem**
No demonstrated spec-drift incident motivates this yet, and no threshold exists to define "stale."

**Scope**
- Author a staleness threshold, then run a one-off scan of specs against their owning code paths

**Acceptance Criteria**
- Threshold defined before scan is run
- Scan report produced identifying any specs exceeding the threshold

---

### BLG-GOV-172 — Governance prompt cross-reference integrity check
**Priority:** P3 (Low)
**Type:** Governance
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic — run at the next scheduled lifecycle audit (`run audit`, every 3 cycles) or upon discovery of a broken cross-reference, whichever comes first.

**Problem**
No evidence yet of a broken cross-reference between governance prompts, but none has been checked systematically either.

**Scope**
- Scan all `claude/system/*.md` cross-references for validity, bundled into the next scheduled `run audit` pass

**Acceptance Criteria**
- Check performed alongside next lifecycle audit; findings (if any) filed as backlog items

---

### BLG-GOV-173 — Escalation SLA dashboard
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Open escalation volume grows to ≥3 concurrent open escalations (current baseline: 0) — below that, existing manual tracking is sufficient.

**Problem**
Escalation volume is currently zero; a dashboard has no data to justify its build cost yet.

**Scope**
- Build a simple SLA-tracking view once escalation volume justifies it

**Acceptance Criteria**
- Dashboard built only after gate condition confirmed

---

### BLG-QA-75 — Playwright flake-rate tracking (consolidated)
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled; consolidates BLG-QA-80 (flaky Playwright test tracker) and BLG-QA-87 (Playwright flake tracking log) — the same underlying capability was re-proposed across the 2026-07-08 and 2026-07-10 idea-intake cycles without cross-reference to this existing item — merged 2026-07-27, session duplicate-consolidation cleanup
**Effort:** S (~1 day) for the lightweight quarantine list; CI-pipeline-integrated flake-rate tracking (gated, see below) is a larger follow-on effort
**Provisional-Target:** Unscheduled
**Gate criteria:** A lightweight quarantine list/log has no gate and can be built now (per BLG-QA-80/87's original proposal). Full CI-pipeline-integrated flake-rate tracking remains gated on the first demonstrated flaky-test incident (a test that fails intermittently without a code change) — building that fuller tooling ahead of any observed flakiness would be premature.

**Problem**
Occasionally-flaky Playwright tests are re-run ad hoc with no tracking of which tests flake, how often, or why. Intermittent CI failures are currently indistinguishable from confirmed defects in QA evidence logs, and there is no visibility into whether flake rate is worsening.

**Scope**
- Maintain a quarantine list / flake log now: test name, first-flagged date, flake count, whether a re-run passed, re-enable criteria
- Once a first flaky-test incident is confirmed: add flake-rate tracking to the CI pipeline itself (gated follow-on)

**Acceptance Criteria**
- Quarantine list / log created; any currently-known flaky test logged
- CI-pipeline flake-rate tracking built only after the gate condition (first flaky-test incident) is confirmed

---

### BLG-QA-76 — QA evidence cross-link audit
**Priority:** P3 (Low)
**Type:** QA / Governance
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic — bundle into the next scheduled lifecycle audit, or run on discovery of a dangling DoQ claim.

**Problem**
No evidence yet of a dangling (unlinked/broken) DoQ sign-off claim, but none has been checked systematically.

**Scope**
- Scan `qa_evidence_*.md` files for DoQ claims lacking a valid evidence link, bundled with the next `run audit` pass

**Acceptance Criteria**
- Check performed alongside next lifecycle audit; findings (if any) filed as backlog items

---

### BLG-OPS-88 — Render dyno right-sizing review
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Bundle with the existing scheduled 90-day AI cost review (due 2026-09-24) — no standalone signal yet indicates the current dyno tier is mismatched.

**Problem**
The 2 AI endpoints are only 8 days live as of this idea's submission; no cost/performance signal yet indicates a right-sizing need.

**Scope**
- Review dyno tier alongside the 2026-09-24 AI cost review

**Acceptance Criteria**
- Review conducted at or after the 2026-09-24 gate date

---

### BLG-OPS-89 — Anthropic API budget alert threshold calibration
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** The existing `POST /ai/check-daily-cost` alert (shipped v4.1) produces a first false positive or false negative.

**Problem**
The existing cost alert has not misfired since shipping; recalibrating its threshold now would be speculative.

**Scope**
- Recalibrate the alert threshold once a false positive/negative is observed

**Acceptance Criteria**
- Recalibration only performed after gate condition confirmed

---

### BLG-OPS-91 — Deploy rollback runbook dry-run
**Priority:** P3 (Low)
**Type:** Operations
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** After the next real production deploy that uses the BLG-OPS-80 rollback runbook.

**Problem**
The rollback runbook (BLG-OPS-80) is authored but has not yet been exercised against a real production deploy.

**Scope**
- Perform a dry-run (or live use) of the runbook at the next production deploy

**Acceptance Criteria**
- Dry-run performed and runbook gaps (if any) documented after the next deploy

---

### BLG-GOV-174 — Skill-Silo Alert historical trend chart
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** PMO Lead
**Source:** IDEA-challenger-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Adoption of a second Skill-Silo escalation tier (BLG-GOV-176a / companion idea IDEA-challenger-20260702-01, Advanced this cycle — see `cycle_record.md` STEP 5) — if a second tier is adopted, this chart becomes part of its supporting dashboard; if not adopted, defer indefinitely.

**Problem**
The underlying data already exists across `workforce_capacity.md` and `decision_log.md` cycle entries; a chart is a presentation nice-to-have, not new capability, and its value depends on whether a second escalation tier is adopted.

**Scope**
- Build a historical trend chart of the rolling Skill-Silo percentage, contingent on the companion escalation-tier decision

**Acceptance Criteria**
- Built only if the companion decision (STEP 5, this cycle) adopts a second tier

---

### BLG-SPEC-67 — OpenAPI example-response completeness sweep
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic documentation debt — bundle with the next scheduled lifecycle audit.

**Problem**
No evidence gaps in `openapi.yaml` example responses have caused an actual integration problem; this is opportunistic hygiene, not urgent.

**Scope**
- Sweep `docs/reference/openapi.yaml` for endpoints missing example responses, bundled with the next `run audit` pass

**Acceptance Criteria**
- Sweep performed alongside next lifecycle audit; gaps (if any) filed as backlog items

---

### BLG-GOV-175 — Base44 prompt draft changelog
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Base44 prompt draft revision frequency increases to a point where informal tracking becomes error-prone (e.g. ≥3 revisions to the same prompt draft within a single sprint).

**Problem**
Prompt revision frequency remains low; a formal changelog/versioning process is not yet warranted.

**Scope**
- Introduce a lightweight changelog for Base44 prompt drafts once revision frequency justifies it

**Acceptance Criteria**
- Changelog introduced only after gate condition confirmed

---

### BLG-BE-43 — Trade plan field usage audit
**Priority:** P3 (Low)
**Type:** Backend / Data
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Arc 4 PO-02 (Journal Pattern Recognition) design phase begins (gated to ~2026-10-20, 6+ months AI-summarised journal data).

**Problem**
This audit would directly inform Arc 4 PO-02/PO-03 design, but running it ahead of that design phase risks auditing fields that later change.

**Scope**
- Audit actual usage of trade plan fields once PO-02 design phase begins

**Acceptance Criteria**
- Audit conducted only after gate condition (PO-02 design phase start) confirmed

---

### BLG-GOV-176 — Facilitator workload note
**Priority:** P3 (Low)
**Type:** Governance / HR
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Facilitator workload is reported as a bottleneck in any cycle's lessons learnt or escalation record.

**Problem**
No signal currently indicates Facilitator workload is a bottleneck; formal tracking is not yet warranted.

**Scope**
- Produce a workload note/assessment once a bottleneck signal is reported

**Acceptance Criteria**
- Assessment produced only after gate condition confirmed

---

### BLG-FEAT-63 — P&L report AI narrative cost estimate
**Priority:** P3 (Low)
**Type:** Product Feature / FinOps
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Same AI-adoption gate as BLG-FEAT-59 (AI-assisted monthly P&L narrative) — clears ~2026-07-25.

**Problem**
This cost estimate directly feeds BLG-FEAT-59, which is itself gated on the AI-adoption window; estimating cost ahead of that gate is premature.

**Scope**
- Produce a cost estimate for AI-generated P&L narrative once the adoption window clears

**Acceptance Criteria**
- Estimate produced only after gate condition confirmed

---

### BLG-BE-45 — Trade cost field completeness check
**Priority:** P3 (Low)
**Type:** Backend / Data Quality
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic — bundle with the next scheduled lifecycle audit.

**Problem**
No evidence yet of missing `trade_costs` values; this is a data-quality hygiene check, not an urgent fix.

**Scope**
- Check completeness of `trade_costs` fields across closed trades, bundled with the next `run audit` pass

**Acceptance Criteria**
- Check performed alongside next lifecycle audit; gaps (if any) filed as backlog items

---

### BLG-QA-77 — Playwright suite runtime trend
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** CI suite runtime is reported as a bottleneck (e.g. blocking rapid iteration or exceeding a defined CI time budget).

**Problem**
CI suite runtime has not been reported as a bottleneck at the current spec-file count; trend tracking now would be premature.

**Scope**
- Add runtime trend tracking to CI once runtime is reported as a bottleneck

**Acceptance Criteria**
- Tracking added only after gate condition confirmed

---

### BLG-OPS-92 — Dependency update review
**Priority:** P2 (Medium)
**Type:** Operations / Security Hygiene
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A new CVE or deprecation warning surfaces on a project dependency, OR the next quarterly hygiene cadence (~2026-10-06, 3 months post v4.0 starlette remediation).

**Problem**
No known CVE or deprecation warning is currently outstanding since the v4.0 starlette remediation; a full review now would be opportunistic rather than urgent.

**Scope**
- Full dependency update review triggered by either a new CVE/deprecation signal or the quarterly cadence, whichever comes first

**Acceptance Criteria**
- Review conducted at or after the gate condition (signal or cadence date)

---

### BLG-FE-90 — Open Positions panel visual consistency check
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A visual inconsistency in the Open Positions panel (BLG-FEAT-54, shipped v6.4) is reported.

**Problem**
BLG-FEAT-54 shipped with Head of UX & Design input already incorporated at design-gate time; no visual inconsistency has been reported since.

**Scope**
- Review and correct any reported visual inconsistency once one surfaces

**Acceptance Criteria**
- Review conducted only after a specific inconsistency is reported

---

### BLG-GOV-177 — DoQ sign-off audit spot-check
**Priority:** P3 (Low)
**Type:** Governance / QA
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A non-compliant DoQ sign-off is found, OR bundle with the next scheduled lifecycle audit.

**Problem**
Every recent cycle has shipped Verified with zero deviations; no evidence yet of a non-compliant DoQ sign-off.

**Scope**
- Spot-check DoQ sign-off compliance, bundled with the next `run audit` pass

**Acceptance Criteria**
- Spot-check performed alongside next lifecycle audit; findings (if any) filed as backlog items

---

### BLG-QA-78 — Test data fixture staleness check
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A test failure is attributed to a stale test fixture.

**Problem**
No test failures have been attributed to stale fixtures since v6.4's signal/security changes; a staleness check now would be speculative.

**Scope**
- Check test data fixtures for staleness once a failure is attributed to one

**Acceptance Criteria**
- Check conducted only after gate condition confirmed

---

### BLG-GOV-178 — Quarterly AI output sampling audit (consolidated)
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer
**Source:** IDEA-ai-compliance-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled; consolidates BLG-GOV-197, BLG-GOV-251 — the same "recurring sampled review of AI output against the §13 boundary" capability was independently re-proposed across two later idea-intake cycles (2026-07-10 and 2026-07-24) without cross-reference to this existing item or each other — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day per quarter)
**Provisional-Target:** Unscheduled
**Gate criteria:** None
**Cross-reference (delivery verification, added 2026-09-14):** ST-22/EPIC-05, cycle `2026-09-09__release-v9.3` — dry-run sample conducted (10 illustrative examples, 0 findings), satisfying this item's literal AC. The stronger live-production-sample bar remains open as escalation `ESC-EXEC-20260910-01` (non-blocking, owned by AI Compliance & Governance Officer, SLA breached 2026-09-13, carried forward past sprint close).

**Update (AI Compliance & Governance Officer, 2026-09-14):** `ESC-EXEC-20260910-01` reviewed. Its SLA-breach was carried forward and caught by `plan release`'s new STEP -1.6 SLA-breach carry-forward gate (`AUD-2026-09-14-001`) when opening v9.4. Genuine resolution (an actual live-production sample) remains structurally blocked in this execution environment (no `DATABASE_URL`, no `ANTHROPIC_API_KEY` — re-confirmed this session); Accepted Risk is not a permitted disposition for a Strategy-boundary trigger-type escalation (`shared_standards.md` §4). Disposition changed `Open` → `Deferred` (see `.claude_current_state.json`); concrete remediation filed as `BLG-AI-06` (generation-time sampling hook). Re-acknowledgement due once `BLG-AI-06` ships or production credentials become available in-session, whichever is first.

**Problem**
AI output (thesis generation, chat, daily briefing) has no recurring compliance sampling — only ad hoc review during feature work. As prompts and models evolve over time, outputs could drift from §13's determinism/no-prediction boundary without a scheduled check to catch it.

**Scope**
- Sample 10 random AI outputs per quarter; check against §13.2 boundary language (no autonomous-sounding directives, advisory framing preserved) and for determinism/no-prediction drift as prompts/models evolve

**Acceptance Criteria**
- First quarterly sample conducted and findings (if any) filed as backlog items

---

### BLG-GOV-184 — Canonical "win rate" definition consistency confirmation
**Priority:** P3 (Low)
**Type:** Governance / Metrics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
"Win rate" is surfaced in at least 4 places (dashboard, P&L report, drift analytics, journal) with no confirmation they all use the same calculation.

**Scope**
- Confirm calculation consistency across all 4 surfaces against `metrics_definitions.md`

**Acceptance Criteria**
- Consistency confirmed, or discrepancy filed as a correctness backlog item

---

### BLG-GOV-185 — Changelog section in metrics_definitions.md
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`metrics_definitions.md` has no changelog — formula version bumps are not tracked, making it hard to know when a metric's calculation last changed.

**Scope**
- Add a changelog section; backfill known recent formula changes

**Acceptance Criteria**
- Changelog section added with at least the most recent known change recorded

---

### BLG-GOV-186 — §13 boundary illustrative examples appendix
**Priority:** P3 (Low)
**Type:** Governance / Documentation
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Score-4/5 debates require citing specific §13 clauses, but §13 itself has no worked examples — every debate re-derives what "engaging a boundary" looks like in practice.

**Scope**
- Add an appendix to `strategy_rules.md` (or a companion doc) with 1–2 concrete right/wrong examples per §13 sub-clause

**Acceptance Criteria**
- Appendix authored, reviewed by Strategy Rules & System Intent Owner

---

### BLG-GOV-188 — Sprint Velocity Trend Chart
**Priority:** P3 (Low)
**Type:** Governance / Process Visibility
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260708-01 (IW-20260708-01), resubmission of IDEA-pmo-lead-20260619-02 (originally rejected at `2026-06-24__scheduled`, 3-cycle hard cap) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None — revival condition (velocity_metrics.md populated ≥5 cycles/2 rebalances) confirmed Met 2026-07-08 (49 rows across 8 rebalance-tracked cycles)

**Problem**
Sprint velocity trend (delivered stories per sprint, U/G/D/P breakdown, delivery rate) requires manual changelog/velocity_metrics.md analysis to see at rebalance time — no visualisation exists.

**Scope**
- Chart of velocity trend across the last 10 rebalance-tracked cycles, sourced from `velocity_metrics.md`

**Acceptance Criteria**
- Chart built, showing at least delivered-story-count and U/G/D/P split per cycle over the available history

---

### BLG-GOV-189 — Governance overhead audit (PMO/spec time per shipped story)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Challenger; PMO Lead
**Source:** IDEA-challenger-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The Product Value Ratio and Skill-Silo alerts both measure governance overhead indirectly (via story classification) — no direct measurement exists of actual PMO/spec time cost per shipped user story, which would ground future governance-cadence decisions (e.g. `IDEA-pmo-lead-20260708-02`, debated this cycle) in harder evidence.

**Scope**
- Retrospective estimate of PMO/spec/governance effort vs. shipped-story count over the last 10 cycles, using available run_manifest/cycle_record artefacts as a proxy

**Acceptance Criteria**
- Estimate produced; findings inform the next cycle-cadence discussion if one recurs

---

### BLG-GOV-191 — Spec debt aging report
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-specs-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
There is no standing report surfacing which `BLG-SPEC-*` items are approaching the 2-cycle-without-story-assignment advisory threshold defined in `release_planning_prompt.md` STEP 1.1 — it currently only fires reactively when a release plan happens to scan for it.

**Proposed solution**
Add a lightweight scan (reusable at `groom backlog` or release planning time) that lists spec-debt items by cycles-aged, surfaced proactively rather than only at the moment a release plan checks.

---

### BLG-GOV-192 — Governance prompt cross-reference sweep cadence
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-specs-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
§14 OPERATIONAL_GUIDE.md version drift is currently only caught opportunistically (e.g. by the `governance-drift` skill when invoked, or when a friction item happens to surface it) rather than on a fixed cadence.

**Proposed solution**
Schedule a periodic (e.g. every-3-cycle, alongside the meta-review) explicit governance-drift check rather than relying on incidental discovery.

---

### BLG-GOV-193 — Escalation SLA breach dry-run test
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** PMO Lead
**Source:** Idea intake IW-20260710-01 (IDEA-pmo-lead-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The `BLOCKED_SLA_BREACH` 72-hour notice path (`shared_standards.md` §4) has never been exercised end-to-end in this repository's history — it is untested governance machinery.

**Proposed solution**
Construct a deliberate dry-run (e.g. a synthetic escalation with a backdated timestamp) to confirm the breach notice actually fires and halts as designed.

---

### BLG-GOV-194 — §13 boundary language clarity pass — AI journal summarisation
**Priority:** P3 (Low)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner
**Source:** Idea intake IW-20260710-01 (IDEA-strategy-owner-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`strategy_rules.md` §13's "deterministic scoring" boundary language pre-dates the AI journal summarisation feature; it has not been explicitly re-read against that feature to confirm the language still functions as an unambiguous boundary.

**Proposed solution**
Strategy Rules & System Intent Owner re-reads §13 against the AI journal summarisation feature specifically and confirms (or clarifies) the boundary language remains unambiguous.

---

### BLG-GOV-195 — Strategic exclusions review cadence
**Priority:** P3 (Low)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner
**Source:** Idea intake IW-20260710-01 (IDEA-strategy-owner-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The 4 product-scope exclusions in `current_roadmap.md` §2 (broker API integration, real-time streaming, social features, options/futures) have not been explicitly re-confirmed since they were first recorded — they could be stale rather than deliberate.

**Proposed solution**
Add a periodic (e.g. every-N-cycle) explicit re-confirmation that each exclusion remains a deliberate choice, not simply an un-revisited default.

---

### BLG-GOV-196 — Sunset review for Priority 3 — Deferred initiatives
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Product Owner
**Source:** Idea intake IW-20260710-01 (IDEA-challenger-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The 7-item `initiative_register.md` Priority 3 — Deferred list (Position Correlation Analysis, Backtesting Module, Multi-Portfolio Support, Mobile App, Full Compliance Scoring, Prometheus, Customisable Dashboard Layout) has not been explicitly re-confirmed since first recorded; some entries may now be stale rather than deliberately deferred.

**Proposed solution**
Product Owner reviews each Priority 3 item and confirms it is still deliberately deferred (not simply forgotten), recording the confirmation date.

---

### BLG-GOV-198 — Base44 prompt versioning convention
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Base44 Frontend Prompt Owner
**Source:** Idea intake IW-20260710-01 (IDEA-base44-frontend-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
There is no convention tracking which Base44 prompt draft shipped with which ST-id, making future regression triage ("which prompt produced this component") harder than necessary.

**Proposed solution**
Adopt a lightweight convention (e.g. a comment header or delegation log field) recording the ST-id alongside each Base44 prompt draft.

---

### BLG-SPEC-77 — Gate-status indicator reusable component pattern documentation
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Idea intake IW-20260710-01 (IDEA-frontend-specs-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
BLG-FEAT-71's SI-02 gate visibility indicator is a one-off implementation; the pattern is not documented for reuse by future gated features.

**Proposed solution**
Document the SI-02 indicator as a reusable gate-status component pattern in the relevant frontend spec, for future gated-feature reuse.

---

### BLG-OPS-105 — CI pipeline runtime audit
**Priority:** P3 (Low)
**Type:** Operations / QA
**Owner:** Head of Engineering
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-engineering-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Full CI suite runtime has been creeping up without a recent audit identifying which test files are slowest.

**Proposed solution**
Profile CI runtime by file and identify the slowest contributors as candidates for optimisation or parallelisation.

---

### BLG-GOV-200 — Skill-Silo rolling-average automation
**Priority:** P3 (Low)
**Type:** Governance Tooling
**Owner:** Metrics Definitions & Analytics Owner
**Source:** Idea intake IW-20260710-01 (IDEA-metrics-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The STEP 7.1 Skill-Silo rolling-3-cycle average is currently computed manually each rebalance by reading the prior 2 cycles' recorded percentages from decision-log prose.

**Proposed solution**
Compute the rolling average from a structured source (e.g. a small per-cycle metrics file) instead of manual re-derivation each rebalance.

---

### BLG-GOV-201 — QA evidence log template consolidation
**Priority:** P3 (Low)
**Type:** Governance / QA Process
**Owner:** QA Lead
**Source:** Idea intake IW-20260710-01 (IDEA-qa-lead-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Per-EPIC `qa_evidence_EPIC-*.md` files currently duplicate a substantial amount of boilerplate header/structure across files.

**Proposed solution**
Consolidate shared boilerplate into a referenced template section, reducing duplication across EPIC evidence files.

---

### BLG-QA-93 — conftest.py AST-scan coverage confirmation (consolidated)
**Priority:** P3 (Low)
**Type:** QA / Backend
**Owner:** QA & Testing Owner
**Source:** Idea intake IW-20260710-01 (IDEA-qa-testing-20260710-02), roadmap rebalance 2026-07-10__scheduled; consolidates BLG-QA-99 — the same capability was independently re-proposed at the 2026-07-12__scheduled idea-intake cycle without cross-reference to this existing item — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
BLG-QA-73 replaced the manual `_DB_STUB_FUNCTIONS` list with an AST-scan derivation; no confirmation has been recorded that the scan's glob/traversal logic still covers all `backend/` modules and subpackages added since v6.8.

**Proposed solution**
Re-verify the AST scan's module coverage and glob/traversal logic against the current `backend/` tree; extend if a subpackage was missed; record confirmation.

---

### BLG-SPEC-81 — Research view `signal_type` filter spec
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260712-02 | **Effort:** S | **Provisional-Target:** Unscheduled
**Gate criteria:** ≥5 distinct `signal_type` values observed in practice (currently fewer; re-check at next backlog grooming).
**Problem:** v4.1 added `signal_type` (Setup Type) to the research view with no filter/sort spec as the field accumulates distinct values.
**Scope:** Spec a filter control once the gate condition is met.
**Acceptance Criteria:** Filter spec written; gate condition re-verified before implementation.

### BLG-GOV-235 — Idea-intake minimum-submission flex condition
**Priority:** P3 (Low) | **Type:** Governance | **Owner:** Head of Specs Team | **Source:** IDEA-director-of-hr-20260715-01 | **Effort:** S | **Provisional-Target:** TBD
**Gate criteria:** Recurs at 3+ consecutive scheduled cycles where the Now horizon is already populated with 3+ ad-hoc (non-governed-cycle) P1 items at window-open — not yet met (this is the 1st such occurrence).
**Problem:** `idea_intake_prompt.md`'s standing 2-net-new-ideas-per-agent minimum does not flex when the Now horizon is already saturated with ad-hoc additions, potentially generating submissions redundant with just-added scope.
**Scope:** If the gate condition recurs, evaluate whether the minimum should reduce or the window should skip agents whose domain is already covered by the ad-hoc additions.
**Acceptance Criteria:** Gate re-checked each scheduled cycle; a written decision follows once met.

### BLG-FEAT-83 — Cohort-based (setup/signal type) performance metric
**Priority:** P3 (Low) | **Type:** Product Feature / Analytics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260724-02 | **Effort:** M | **Provisional-Target:** TBD
**Gate criteria:** Sufficient `setup_type`/signal-type diversity in closed-trade history to produce a meaningful cohort split (same data-density concern as `BLG-FEAT-62`).
**Problem:** Performance Analytics has no cohort-based (grouped by setup/signal type) performance metric, despite the underlying `signal_type` field being captured since the Research view shipped it (v4.1).
**Scope:** Add a cohort-based performance metric to Performance Analytics, building on the existing Arc 5 compliance analytics layer.
**Acceptance Criteria:** Metric available once gate clears; at least 3 distinct cohorts represented.

---

### BLG-QA-122 — Broker statement reconciliation (blocked — no broker import mechanism)
**Priority:** P3 (Low) | **Type:** QA / Financial Reporting, gate-conditional | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260724-02 | **Effort:** M | **Provisional-Target:** TBD
**Gate criteria:** A broker statement import mechanism exists. Per `current_roadmap.md` §2 Product Scope Exclusions, "Broker API integration (execution)" is currently a deferred (not strategically excluded) exclusion — no import path exists today for this item to reconcile against.
**Problem:** Idea proposed a reconciliation check between journal/trade entries and broker statement data, but no broker statement import mechanism currently exists to reconcile against.
**Scope:** Deferred until broker integration (or a manual statement upload path) exists.
**Acceptance Criteria:** N/A until gate clears.

---

### BLG-FEAT-92 — Screener-to-trade conversion funnel view
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner; Product Owner
**Source:** Product Owner feature-vision session — 2026-08-17; related to existing `BLG-FEAT-30` (Screener-to-trade attribution pipeline & retrospective analytics, consolidated) — overlap to be reconciled before scheduling
**Effort:** M (~2d)
**Provisional-Target:** Unscheduled
**Depends on:** BLG-FEAT-30 (shares the same underlying attribution linkage; Product Owner/Head of Specs Team to confirm whether this is a sub-scope of BLG-FEAT-30 or a genuinely separate item before either enters sprint planning)
**Gate criteria:** Inherits `BLG-FEAT-30`'s gate (screener live ≥60 days AND ≥60 closed trades with attribution) — track disposition there. Reconciled as a sub-scope of `BLG-FEAT-30` at the Product Owner's `2026-09-03__release-v9.1` decision (reaffirmed each cycle since, most recently `decisions--2026-09-07__release-v9.2.md`); this field added `2026-09-09` (post-ship closure `2026-09-07__release-v9.2` outstanding-actions resolution, Head of Specs Team direct action per the new Gate-Inheritance Field-Completeness Scan, `backlog_management_prompt.md` v1.17) so future rebalance/release-planning sessions no longer need to re-locate a prior cycle's decisions document to confirm this item's exclusion — 4 consecutive cycles (v8.9–v9.2) required that manual lookup before this fix.

**Problem**
The full pipeline (screener hit → watchlist → research → trade plan → position → close) exists end-to-end, but there is no aggregate view of where candidates drop off at each stage, or what fraction of screener hits ever convert into a trade — let alone a profitable one. Without this, it isn't possible to tell whether the screener's complexity and cost are earning their keep, and every other planned analytics feature building on screener attribution (`BLG-FEAT-30` and its consolidated items) is downstream of having this instrumentation in place.

**Scope**
- Funnel view: screener hit → watchlist add → trade plan created → position opened → position closed, with count and conversion % at each stage
- Filterable by date range and, where available, setup/signal type
- Product Owner/Head of Specs Team to reconcile scope against `BLG-FEAT-30` before this enters sprint planning — may be absorbed as a sub-scope rather than shipped separately

**Acceptance Criteria**
- Funnel view displays counts and conversion % for all 5 pipeline stages over a selectable date range
- Reconciliation with `BLG-FEAT-30` completed and documented (merged, superseded, or confirmed distinct) before either item is scheduled
- Product Owner sign-off

---

## Idea Intake IW-20260914-01 — Promoted-Backlog Disposition (roadmap rebalance `2026-09-14__scheduled`)

*40 of the window's 44 submissions promoted directly to backlog per STEP 4 "📋 Backlog (gate-conditional)" disposition — no hard gate on any item, all ungated and ready. 2 Challenger submissions resolved as process patches feeding this cycle's STEP 11.4 meta-review (see `lessons_learnt.md`/`meta_review.md`), not filed here. All items carry `**Provisional-Target:** TBD` (Now/Next horizons both empty — §16.6 fallback) and no day-range effort (§16.12 n/a, target not release-specific).*


### BLG-QA-171 — Quarterly full-suite Playwright re-run against a fresh staging seed
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** M
**Provisional-Target:** TBD

**Problem**
The full Playwright suite is currently only re-run when a story touches the relevant surface, so a regression introduced by an unrelated change (data drift, dependency bump) between touches could go undetected for a long stretch.

**Scope**
- Define a quarterly cadence and a fresh-staging-seed procedure
- Run once to confirm the procedure works end to end

**Acceptance Criteria**
- Cadence and seed procedure documented
- First quarterly run completed with results recorded

---

### BLG-QA-172 — DoQ checklist addendum for flaky-test disposition
**Priority:** P3 (Low)
**Type:** QA / Governance
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
When a test is found flaky, the DoQ sign-off process has no documented decision framework for whether to retry, quarantine, or fix immediately — each occurrence is handled ad hoc.

**Scope**
- Add a short decision-framework addendum to the DoQ sign-off template/checklist
- Cross-reference the existing flaky-test quarantine backlog item (gate-conditional) so the two do not diverge

**Acceptance Criteria**
- Addendum added to the DoQ checklist
- Cross-reference confirmed correct against the existing quarantine item

---

### BLG-SPEC-144 — Canonical colour-blind-safe chart palette spec
**Priority:** P3 (Low)
**Type:** Frontend Spec
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
Chart colour usage is referenced ad hoc across chart components with no single documented colour-blind-safe palette spec to regenerate or extend against.

**Scope**
- Document a canonical palette in the relevant design/frontend spec
- Cross-reference from existing chart components (documentation only this cycle, not a visual re-skin)

**Acceptance Criteria**
- Palette documented with justification (e.g. a recognised colour-blind-safe source)
- Cross-referenced from at least the design system spec

---

### BLG-SPEC-145 — Lightweight ADR log for cross-cutting backend decisions
**Priority:** P3 (Low)
**Type:** Documentation / Process
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** M
**Provisional-Target:** TBD

**Problem**
Cross-cutting backend architecture decisions currently live scattered across individual PR descriptions with no single searchable log, making it hard to answer "why was it built this way" without archaeology.

**Scope**
- Create `docs/ops/architecture_decisions.md` (or similar) with a lightweight ADR template
- Backfill 2-3 of the most consequential recent decisions as a starting seed (not a full historical backfill)

**Acceptance Criteria**
- File exists with template and at least 2 seeded entries
- Referenced from a relevant onboarding/index document

---

### BLG-GOV-325 — Fixed-cadence audit of every governance prompt's §14 version-table entry
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
The `governance-drift` skill catches §14 version-table mismatches when invoked, but nothing guarantees it is invoked on any particular cadence — drift could persist for a long stretch between voluntary invocations.

**Scope**
- Define a fixed cadence (e.g. every N cycles) at which `governance-drift` is invoked as a mandatory step rather than an optional check
- Likely insertion point: a STEP in `roadmap_prompt.md` or `manage roadmap`

**Acceptance Criteria**
- Cadence defined and wired into a governed routine's mandatory steps
- First mandatory-cadence run completed with results recorded

---

### BLG-SPEC-146 — Canonicalise the Sharpe-ratio lookback window
**Priority:** P3 (Low)
**Type:** Spec Debt / Metrics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
3 slightly different Sharpe-ratio lookback windows are used across the dashboard, a generated report, and an API response, with no single canonical definition to reconcile against.

**Scope**
- Identify the 3 current windows precisely (dashboard, report, API)
- Decide and document one canonical window in `metrics_definitions.md`

**Acceptance Criteria**
- Canonical window documented with rationale
- Discrepancy noted explicitly for each of the 3 current call sites (fix itself may be a separate follow-on item)

---

### BLG-SPEC-147 — Formal definition of "linked trade plan" counting for the SI-02 gate
**Priority:** P3 (Low)
**Type:** Spec Debt / Metrics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
The SI-02 gate's "linked trade plan" count is well-specified as a query (`current_roadmap.md` §5) but has no formal canonical definition document of its own, unlike the drift-score threshold which already has one (`docs/specs/metrics/si02_drift_score.md`).

**Scope**
- Create a companion canonical definition doc (or extend the existing drift-score one) formally defining "linked trade plan" for gate purposes
- Cross-reference from `current_roadmap.md`'s SI-02 structured field

**Acceptance Criteria**
- Canonical definition exists
- `current_roadmap.md` SI-02 field cross-references it

---

### BLG-SPEC-148 — DS-17 unique index migration not yet applied to live positions table
**Priority:** P2 (Medium)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner; Infrastructure & Operations Owner
**Source:** ST-22/EPIC-04, 2026-09-15__release-v9.5 — 2026-09-18
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
DS-17 (`docs/specs/data_model.md`, v2.33, 2026-09-14) adds a partial unique index `idx_positions_open_ticker_entry_date_unique` on `positions(portfolio_id, ticker, entry_date) WHERE status = 'open'`, authored and tested against a synthetic SQLite fixture only (`DATABASE_URL` was unavailable that cycle — AC-03 explicitly disclosed as pending). `DATABASE_URL` (readonly staging) was available this session for the first time in several cycles: confirmed live via `\d positions` that the index does not exist (only the pre-existing 5 indexes are present). Re-ran the migration's own duplicate pre-check live — 0 duplicate `(portfolio_id, ticker, entry_date)` groups among open positions — so the migration is safe to apply as-is.

**Scope**
- Apply the DS-17 up-migration to the live database (requires write access this session's readonly credential does not have)
- Confirm the index exists post-apply and re-run the duplicate pre-check as a final safety net immediately before applying

**Acceptance Criteria**
- `idx_positions_open_ticker_entry_date_unique` exists on the live `positions` table
- DS-17's AC-03 "pending" disclosure in `data_model.md` is updated to confirmed-applied, with date

---

### BLG-SPEC-149 — positions.exit_note documented in data_model.md does not exist on live table
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-22/EPIC-04, 2026-09-15__release-v9.5 — 2026-09-18
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
`data_model.md`'s Positions Table field list documents an `exit_note` TEXT column. Live schema query against the (readonly staging) database confirmed this column does not exist on `positions` (`ERROR: column "exit_note" does not exist`). Journal notes at exit are actually stored on `trade_history.exit_note` (confirmed present there via `\d trade_history`) — closed-position exit notes live on the trade history record, not on the position row itself.

**Scope**
- Remove or correct the `exit_note` row in `data_model.md`'s Positions Table field list
- Add a note cross-referencing `trade_history.exit_note` as the actual storage location, if not already clear from that table's own docs

**Acceptance Criteria**
- `data_model.md`'s Positions Table section no longer claims a live `exit_note` column that doesn't exist

---

### BLG-SPEC-150 — 4 orphaned, always-NULL, undocumented columns on live positions table
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-22/EPIC-04, 2026-09-15__release-v9.5 — 2026-09-18
**Effort:** S (~0.5–1d)
**Provisional-Target:** v9.6

**Problem**
Live `positions` table (confirmed via readonly staging access) has 4 columns not referenced anywhere in `data_model.md`: `atr_value`, `stop_price`, `fees`, `pnl_percent` (all nullable numeric). Queried both live open-position rows — all 4 columns are NULL on every row, while their apparent same-purpose counterparts already documented in spec (`atr`, `current_stop`, `fees_paid`, `pnl_pct`) are populated and match the spec exactly. These read as leftover columns from an old naming convention or an aborted rename, never backfilled, populated, or dropped.

**Scope**
- Data Model & Domain Schema Owner to confirm whether any live code path still reads or writes these 4 columns
- If genuinely unused: file a follow-on migration to drop them
- If still meaningfully used somewhere: document them properly in `data_model.md`

**Acceptance Criteria**
- Disposition recorded (drop vs document) with supporting evidence
- `data_model.md` and the live schema agree on every `positions` column, one way or the other

---

### BLG-SPEC-151 — positions.fees_paid documented as NOT NULL but live column is nullable
**Priority:** P4 (Trivial)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-22/EPIC-04, 2026-09-15__release-v9.5 — 2026-09-18
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
`data_model.md`'s Positions Table field notes state `fees_paid | DECIMAL(10,2) | NO | Total fees. NOT NULL as of v1.6`. Live schema query (readonly staging, `\d positions`) shows `fees_paid` with no `NOT NULL` constraint.

**Scope**
- Reconcile: either add the missing `NOT NULL` constraint live, or correct the spec's claim to reflect actual (nullable) live behaviour

**Acceptance Criteria**
- `data_model.md` and the live schema agree on `fees_paid` nullability

---

### BLG-SPEC-152 — Full field-level openapi.yaml authoring pass for 20 generic/thin `data` payload schemas
**Priority:** P3 (Low)
**Type:** Spec Debt / API Contracts
**Owner:** API Contracts & Documentation Owner
**Source:** ST-26/EPIC-04, 2026-09-15__release-v9.5 — 2026-09-18
**Effort:** M (~1–2 days)
**Provisional-Target:** v9.6

**Problem**
`docs/ops/contract_example_freshness_triage_2026-09-18.md` §5 found 20 endpoints where `openapi.yaml`'s declared schema leaves the response `data` payload as a generic `type: object` with little or no declared properties, while the markdown contract in `docs/specs/api_contracts/` carries the real field-level detail. Some of these carry an explicit "Intentionally broad to avoid drift" description (a deliberate, established convention); others (e.g. `GET /watchlist`, `GET /reports/tax-year`'s `trades[]`/`summary`) are bare `{type: object}` with no description at all, and it isn't yet confirmed case-by-case which category each falls into.

**Scope**
- For each of the 20 endpoints listed in the triage doc §5: confirm whether the schema is intentionally broad (add the standard description if missing, no functional change) or genuinely under-authored (fill in real properties matching the markdown contract, types included)
- Re-run `scripts/check_contract_example_freshness.py` after each fix to confirm it drops off the POSSIBLE DRIFT list (or is deliberately left, once labelled intentional)

**Acceptance Criteria**
- All 20 endpoints from the triage doc's §5 have a case-by-case disposition recorded
- `scripts/check_contract_example_freshness.py`'s POSSIBLE DRIFT count reflects only genuinely-remaining intentional gaps, each carrying the standard description

---

### BLG-SPEC-153 — POST /trade-plans and DELETE /trade-plans/{id} declare no response schema in openapi.yaml
**Priority:** P3 (Low)
**Type:** Spec Debt / API Contracts
**Owner:** API Contracts & Documentation Owner
**Source:** ST-26/EPIC-04, 2026-09-15__release-v9.5 — 2026-09-18
**Effort:** S (~0.5d)
**Provisional-Target:** v9.6

**Problem**
`docs/ops/contract_example_freshness_triage_2026-09-18.md` §6 found `POST /trade-plans` (201) and `DELETE /trade-plans/{id}` (200) declare only a bare `description` in `openapi.yaml`, no `content`/`schema` at all — confirmed as a genuine spec gap, not a freshness-check script limitation (both response codes are ones the script already checks). Both have real, documented JSON examples in `docs/specs/api_contracts/trade_plan_endpoints.md`.

**Scope**
- Author `content`/`schema` entries for both responses in `openapi.yaml`, matching `trade_plan_endpoints.md`'s documented examples

**Acceptance Criteria**
- Both endpoints have a real response schema in `openapi.yaml`
- `scripts/check_contract_example_freshness.py` no longer reports either as SKIPPED

---

### BLG-SPEC-154 — trade_plans CREATE TABLE / DS-04 CHECK constraint undocumented since ensure_trade_plans_extended_status() shipped
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-29/EPIC-04, 2026-09-15__release-v9.5 — 2026-09-18
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
`data_model.md`'s `trade_plans` `CREATE TABLE` block (§Trade Plan Object, DS-04) still declares `status VARCHAR(20) ... CHECK (status IN ('draft', 'active', 'closed'))` — 3 values. `backend/database.py::ensure_trade_plans_extended_status()` extends this to 7 (`draft`, `research_pending`, `research_complete`, `entry_conditions_set`, `active`, `closed`, `abandoned`) and has clearly already shipped: confirmed live via `DATABASE_URL` (readonly staging) this session — `pg_get_constraintdef` on `trade_plans_status_check` returns exactly the 7-value list — and `docs/specs/frontend/pages/trade_plan.md` §9's Status Badge Scheme (v3.3) has correctly documented and styled all 7 statuses for a long time. Only `data_model.md`'s own DDL/CHECK-constraint documentation was never updated with a DS-xx entry for this migration.

**Scope**
- Add a DS-xx entry documenting `ensure_trade_plans_extended_status()`'s migration (7-value CHECK constraint), following the existing DS-xx entry format
- Update the `trade_plans` `CREATE TABLE` block's CHECK constraint and field notes to show all 7 values

**Acceptance Criteria**
- `data_model.md`'s `trade_plans` CHECK constraint and field notes match the live 7-value constraint
- A DS-xx entry exists documenting the migration, matching this doc's own established format

---

### BLG-SPEC-155 — openapi.yaml's OperationalHealthResponse.ai_journal doesn't model its either/or shape with oneOf
**Priority:** P4 (Trivial)
**Type:** Spec Debt / API Contracts
**Owner:** API Contracts & Documentation Owner
**Source:** Agent-mediated Director of Quality review, PR #1715 (EPIC-04, 2026-09-15__release-v9.5) — 2026-09-18
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
`docs/reference/openapi.yaml`'s `OperationalHealthResponse.ai_journal` schema (added PR #1715, ST-26/BLG-SPEC-139) lists `status` (enum `[unavailable]`) as a sibling property alongside `usage_rate`/`error_rate`/`p95_latency_ms`, rather than modelling the real "either the 3 metric fields, or `{status: unavailable}`" either/or shape via `oneOf`. The description text correctly explains the real behaviour, but the schema itself currently permits (and doesn't forbid) a response carrying all 4 keys at once, which the real endpoint never returns. Low-severity — a pre-existing style pattern elsewhere in this file, not a regression introduced by PR #1715.

**Scope**
- Model `ai_journal` as a `oneOf` of the two real shapes (3-metric object, or `{status: unavailable}`)

**Acceptance Criteria**
- `ai_journal`'s schema forbids a response carrying both the metric fields and `status: unavailable` simultaneously

---

### BLG-SPEC-156 — PO-04 (Reflection ↔ Outcome Correlation) needs its own §13 boundary review, not just a stub-file note
**Priority:** P3 (Low)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** Agent-mediated Product Owner review, PR #1715 (EPIC-04, 2026-09-15__release-v9.5, ST-23) — 2026-09-18
**Effort:** XS (~0.5 day)
**Provisional-Target:** Unscheduled (pre-work before PO-04 gate)

**Problem**
`docs/specs/api_contracts/reflection_outcome_correlation_stub.md` (ST-23) flags that "correlation" language reads closer to a predictive claim than PO-02/PO-03's pattern-recognition/classification framing, and suggests PO-04 may need its own §13 boundary check rather than inheriting `BLG-SPEC-35`'s PO-02 clearance if that lands first. That suggestion currently exists only as prose inside a pre-authoring stub file — nothing tracks it as an actionable item, so it risks being silently dropped once `BLG-SPEC-35` closes and nobody re-reads the stub.

**Scope**
- File (or confirm covered by) a dedicated §13 pre-assessment for PO-04, distinct from `BLG-SPEC-35`'s PO-02 scope
- Cross-reference from `reflection_outcome_correlation_stub.md`

**Acceptance Criteria**
- A trackable item (this one, or a successor) exists for PO-04's own §13 review — not just prose in a stub file

---

### BLG-GOV-326 — Rolling wall-clock cost dashboard across the last 10 cycles
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
Overlaps materially with `BLG-GOV-323` (FinOps's cost-per-cycle rollup submission this same window) — both ask for a rollup of §22 wall-clock figures. Filed as a separate item only because it names a slightly different consumer (PMO trend visibility vs FinOps capacity planning); should likely be merged into `BLG-GOV-323`'s implementation rather than built twice.

**Scope**
- Confirm with `BLG-GOV-323`'s owner whether one rollup satisfies both use cases before either is implemented

**Acceptance Criteria**
- Merge decision recorded (expected: yes, satisfied by `BLG-GOV-323`) before either enters sprint planning

---

### BLG-GOV-327 — Quarterly "governance overhead ratio" metric
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** M
**Provisional-Target:** TBD

**Problem**
Given the sustained scheduled-rebalance cadence and heavily governance/debt-weighted release composition (see this cycle's Product Value Ratio finding), there is no single metric tracking the ratio of process-cycle effort to shipped-cycle effort over time.

**Scope**
- Define the metric precisely (candidate: governance-tagged wall-clock time ÷ total wall-clock time, using §22 logging)
- Compute a first historical baseline reading

**Acceptance Criteria**
- Metric defined in a canonical spec (likely `metrics_definitions.md`)
- First baseline reading recorded

---

### BLG-GOV-328 — Revisit sprint capacity band given sustained ≥90% utilisation
**Priority:** P3 (Low)
**Type:** Governance / Workforce
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
The ~24-28 working-day-equivalent sprint capacity band has now seen 9+ consecutive cycles at or above ~90% utilisation (per `workforce_capacity.md` history) without a formal re-baseline decision since the band was last confirmed unchanged at `2026-07-28__scheduled`.

**Scope**
- FinOps & Resource Architect to review the full utilisation history against the band
- Decide: hold, raise, or explicitly reconfirm the band as correctly calibrated (sustained high utilisation is not automatically evidence the band is wrong — it may reflect a deliberate "use full capacity" operating pattern)

**Acceptance Criteria**
- Review completed and documented in `workforce_capacity.md`
- Explicit hold/raise decision recorded, not merely re-noted as "revisit again next cycle"

---

### BLG-QA-173 — Standing regression check for the OpenAPI Drift Detection gate itself
**Priority:** P3 (Low)
**Type:** QA / CI Tooling
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
The OpenAPI Drift Detection gate is relied upon heavily (it is a hard, PR-blocking gate) but has no test of its own confirming it actually still fires when it should — a regression in the gate's own script could silently stop protecting anything.

**Scope**
- Add a test fixture that deliberately introduces a drift case (missing contract heading) and confirms the gate fires
- Add a second fixture confirming a compliant case passes

**Acceptance Criteria**
- Both fixtures exist and pass in CI
- A deliberate revert of the gate's logic is confirmed to fail the fixture (proving the test actually tests something)

---

### BLG-QA-174 — CI check flagging merged `.skip()`/`.only()` Playwright specs
**Priority:** P3 (Low)
**Type:** QA / CI Tooling
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
A Playwright spec left with `.skip()` or `.only()` in a merged PR silently disables coverage (or narrows a full run to one spec) with no CI signal calling it out — this is a distinct gap from the existing flaky-test quarantine item, which addresses tests confirmed flaky, not specs left skipped/scoped for unrelated reasons.

**Scope**
- Add a CI grep/lint step scanning merged Playwright spec files for `.skip(`/`.only(` usage
- Allow a documented, deliberate exception mechanism (e.g. a comment tag) for genuinely intentional long-term skips

**Acceptance Criteria**
- CI check added and fires on a deliberately-introduced test case
- Exception mechanism documented

---

### BLG-QA-175 — Recurring pre-sprint endpoint test coverage audit
**Priority:** P3 (Low)
**Type:** QA / Process
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
Endpoint test coverage (the CLAUDE.md-mandated same-commit `backend/routers/test.py` requirement) is only checked at commit time. A drift that slipped through (e.g. an older endpoint predating the rule) is only caught reactively, not proactively before a sprint starts.

**Scope**
- Add a pre-sprint audit step (likely in `sprint_planning_prompt.md` STEP 0) scanning all `@router.*` decorators against `test.py` coverage
- Report any gap found before sprint scope is sealed, not after

**Acceptance Criteria**
- Audit method documented
- First run completed; any gap found filed as its own item (e.g. this cycle's own `BLG-OPS-156` is an example of the same class of gap, caught at post-ship instead — this item would catch it earlier)

---

### BLG-QA-176 — Backfill negative-path tests for the 3 newest v9.2/v9.3 routers
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** M
**Provisional-Target:** TBD

**Problem**
The 3 newest routers shipped in v9.2/v9.3 have positive-path endpoint test coverage (satisfying the CLAUDE.md same-commit requirement) but no negative-path coverage (invalid input, missing auth, not-found) confirmed yet.

**Scope**
- Identify the 3 newest routers precisely
- Add negative-path test cases for each

**Acceptance Criteria**
- 3 routers identified
- Negative-path tests added and passing for each

---

### BLG-GOV-329 — Re-confirm §13 boundary review cadence
**Priority:** P2 (Medium) — escalated from P3, 2026-09-19 (roadmap rebalance `2026-09-19__scheduled` STEP 8.1.5: 2nd rebalance carried past the §13-adjacent expiry threshold and not selected at v9.5 at P3; raised so §1.4c's P2-first selection seats this decision-only story at v9.6)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
Per this cycle's STEP 8.1.5 §13-Adjacent Initiative Expiry Review, 2 `rejected_but_strong.md` entries (`IDEA-strategy-owner-20260304-02`/`IDEA-challenger-20260304-01`) have sat "§13 ATR review-gated" and "Unmet" since 2026-03-04 — 6+ months with no scheduled ATR review, and no standing cadence exists to force one to be scheduled rather than re-flagged indefinitely.

**Scope**
- Decide whether to schedule the named ATR review now, or formally document why it remains not-yet-warranted with a concrete future trigger
- Consider whether a standing cadence (not just per-item expiry flagging) is warranted given this is the item's 2nd rebalance being carried past the STEP 8.1.5 threshold

**Acceptance Criteria**
- Explicit decision recorded (schedule now / defer with concrete trigger)
- If deferred again, the new trigger must be more concrete than the prior one (per the STEP 8.1.5 finding)

---

### BLG-GOV-330 — Review whether the SI-02 gate threshold should scale with observed trade cadence
**Priority:** P3 (Low)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
This is the same substantive question `IDEA-challenger-20260809-02` raised and had rejected-strong as a duplicate of `BLG-GOV-237`'s "still appropriate" answer (v8.3). This submission restates it from the Strategy Rules & System Intent Owner's own perspective rather than the Challenger's — arguably not materially new, but filed rather than dropped since the submitting role differs and the underlying data (9+ consecutive NOT MET readings, now approaching a full year) has continued to accumulate since `BLG-GOV-237` last examined it.

**Scope**
- Confirm whether `BLG-GOV-237`'s "still appropriate" conclusion should be formally re-examined given the extended data since, or whether this is correctly closed as no-new-information

**Acceptance Criteria**
- Disposition recorded: re-examine (with new analysis) or confirm-closed (citing `BLG-GOV-237`, no new information)

---

### BLG-GOV-331 — Document ensure_ascii=False convention for governance JSON writes
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** PR #1662 agent-mediated Director of Quality review, EPIC-01/v9.4 — 2026-09-14
**Effort:** XS
**Provisional-Target:** TBD

**Problem**
A programmatic write to `.claude_current_state.json` during EPIC-01/v9.4 execution used Python's `json.dump(..., indent=2)` with the default `ensure_ascii=True`, which re-escaped every non-ASCII character (em-dashes, `§`) across the *entire* ~125-line file into `\uXXXX` sequences — not just the ~5 fields that actually changed. Result: 15 of 125 lines showed as changed in the PR diff for a semantically ~5-field edit, and the file's raw readability degraded (literal `—`/`§` replaced by escape sequences). No existing convention documents the correct approach for future writers (agent or human) to this and other governance JSON files (`execution_state.json`, etc.) that routinely carry non-ASCII prose.

**Scope**
- Add a short note (e.g. `shared_standards.md` or a `CLAUDE.md` line) stating that any programmatic write to governance JSON files must preserve non-ASCII characters literally (e.g. Python's `json.dump(..., ensure_ascii=False)`) rather than escaping them, to keep diffs minimal and files human-readable

**Acceptance Criteria**
- Convention documented somewhere a future governance-JSON writer (agent or human) would see it before writing

---

### BLG-QA-177 — Validate `get_claude_endpoint_cost_windows()` SQL against a real Postgres instance

**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Data Model & Domain Schema Owner / QA Testing Owner
**Source:** PR #1665 agent-mediated Director of Quality review, EPIC-03/ST-09, `2026-09-14__release-v9.4` — 2026-09-14
**Effort:** S (~0.5d)
**Provisional-Target:** v9.5

**Problem**
`backend/database.py`'s `get_claude_endpoint_cost_windows()` (added ST-09, `BLG-OPS-151`) uses `FILTER` clauses and `(param || ' hours')::interval` / `(param || ' days')::interval` string-concatenation arithmetic to compute recent-vs-baseline cost windows. No test in the repo actually executes this SQL: `tests/test_ai_endpoint_anomaly_service.py`'s new tests all go through `tests/conftest.py`'s session-scoped `database`-module stub (every `from database import (...)` anywhere in `backend/` is AST-discovered and replaced with a `MagicMock`), and since `ai_endpoint_anomaly_service.py` imports `get_claude_endpoint_cost_windows` locally inside the function body, even the "monkeypatched" tests only patch the stub's attribute, never the real function. No `DATABASE_URL` is available in the current execution environment to run it live either. The query is nontrivial (interval arithmetic via the `||` operator + cast) and has zero real or synthetic execution coverage.

**Scope**
- Run the query manually against a real (or synthetic/local) Postgres instance and confirm the recent/baseline window boundaries and `FILTER` aggregates behave as documented
- Or add a synthetic-DB test (e.g. a local Postgres/sqlite-compatible fixture, following the pattern used for `tests/test_positions_open_ticker_entry_date_unique_migration.py` in EPIC-01/ST-01 this same cycle) that actually executes the real function rather than a stub

**Acceptance Criteria**
- The query has been run at least once against a real or synthetic Postgres instance with confirmed-correct recent/baseline window boundaries, or a new test exists that executes the real (non-stubbed) `get_claude_endpoint_cost_windows()` and asserts its output shape/values

---

### BLG-QA-178 — `test_trade_plan_audit_log.py`'s unrestored `sys.modules["database"]` swap is a latent test-isolation hazard
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality
**Source:** ST-23 (EPIC-05, v9.4, BLG-AI-06) CI investigation — 2026-09-15
**Effort:** XS (<1h)
**Provisional-Target:** v9.5

**Problem**
`test_trade_plan_audit_log.py` loads the real `backend/database.py` module via a permanent, module-level `sys.modules.pop("database", None); import database` (no restore), overwriting `conftest.py`'s session-scoped stub for the rest of the pytest session. This was confirmed live to cause cross-file test breakage this cycle when a new, alphabetically-earlier-sorting test file (`test_ai_output_sampling_service.py`, since fixed to use an isolated-copy pattern instead) did the same thing and leaked a real Postgres connection attempt into `test_alerts_service.py`'s own tests. `test_trade_plan_audit_log.py` has the identical unrestored pattern and currently only avoids the same problem by sorting late enough alphabetically that nothing after it needs the stub back — it is not actually safe, just not yet triggered.

**Scope**
- Convert `test_trade_plan_audit_log.py` to the safer, already-established isolated-copy pattern (load the real module via `importlib.util.spec_from_file_location` under its own private `sys.modules` key, as `test_position_audit_log.py` and the fixed `test_ai_output_sampling_service.py` both do) instead of mutating the shared `sys.modules["database"]` slot
- Grep the rest of `tests/` for the same `sys.modules.pop("database"...)` pattern with no matching restore fixture, and apply the same fix to any other file found

**Acceptance Criteria**
- `test_trade_plan_audit_log.py` no longer mutates the shared `sys.modules["database"]` entry
- Full backend test suite (`backend/.venv/bin/python3 -m pytest tests/`) still passes, and a manual reordering check confirms no other order-dependent leakage remains from this specific pattern
- Any other file found with the same unrestored pattern is fixed in the same commit

---

### BLG-FE-178 — AlertThresholdsSection.js empty-state heading has a trailing period, violating the empty-state microcopy pattern
**Priority:** P4 (Trivial)
**Type:** Frontend / UX Bug
**Owner:** Base44 Frontend Prompt Owner; Frontend Specifications & UX Documentation Owner
**Source:** ST-30/EPIC-04, 2026-09-15__release-v9.5 — 2026-09-18
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
`src/components/notifications/AlertThresholdsSection.js`'s empty-state heading renders `"No alert rules configured."` with a trailing period, violating `design_system.md`'s v1.8 empty-state microcopy pattern ("no trailing period — it's a label, not a sentence"). This is the same class of generation mistake already caught and fixed elsewhere in the app for `TradePlans.js`/`CalendarView.js` (`base44_prompt_template_library.md` v1.7 changelog) and confirmed still-correct for `Notifications.js`/`Watchlist.js`/`TradePlans.js` during this cycle's ST-30 review — this component was missed by that prior sweep. `docs/specs/frontend/pages/notifications.md`'s own spec for this heading already correctly omits the period (matches the canonical pattern, not this component).

**Scope**
- Remove the trailing period from `AlertThresholdsSection.js`'s empty-state heading string

**Acceptance Criteria**
- Empty-state heading renders `"No alert rules configured"` (no trailing period)
- Playwright coverage or a recorded staging run confirms the rendered heading, per CLAUDE.md's frontend-visible-change rule (wording-only — code review may substitute per the FI-P3-02 exception if genuinely no visual/layout change results)

---

### BLG-FE-179 — NotificationsHistory.js empty-state heading has a trailing period, violating the empty-state microcopy pattern
**Priority:** P4 (Trivial)
**Type:** Frontend / UX Bug
**Owner:** Base44 Frontend Prompt Owner; Frontend Specifications & UX Documentation Owner
**Source:** ST-30/EPIC-04, 2026-09-15__release-v9.5 — 2026-09-18
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
`src/pages/NotificationsHistory.js`'s empty-state heading renders `"No alert history yet."` with a trailing period, violating `design_system.md`'s v1.8 empty-state microcopy pattern ("no trailing period — it's a label, not a sentence"). Same defect class as `BLG-FE-178`, found in the same ST-30 review sweep. `docs/specs/frontend/pages/notifications.md`'s own spec for this heading already correctly omits the period (matches the canonical pattern, not this component).

**Scope**
- Remove the trailing period from `NotificationsHistory.js`'s empty-state heading string

**Acceptance Criteria**
- Empty-state heading renders `"No alert history yet"` (no trailing period)
- Playwright coverage or a recorded staging run confirms the rendered heading, per CLAUDE.md's frontend-visible-change rule (wording-only — code review may substitute per the FI-P3-02 exception if genuinely no visual/layout change results)

---

### BLG-GOV-333 — Reconcile sprint_planning_prompt.md STEP -1 status-vocabulary wording against shared_standards.md §10.1
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Sprint Planning session, 2026-09-15__release-v9.5 (`sprint_planning_notes.md` Preflight Vocabulary Drift Advisory) — 2026-09-16
**Effort:** XS (~0.5–1h)
**Provisional-Target:** TBD

**Problem**
`sprint_planning_prompt.md` STEP -1 Hard Gates 1 and 2 restate their own literal status-value enums for `.claude_current_state.json.status` (`Published`/`Validated`/`Committed`) and cycle-level `state.json.status` (`Published`) rather than citing `shared_standards.md §10.1`'s Lifecycle Guard, which is the actual authoritative source (already correctly cited by this same prompt's own §2 Invocation Rule). Both enums are now stale: the current cycle's status was correctly `Design_Gate_Passed` (not in Gate 1's list) and `Validated` (not `Published`, per Gate 2). This has now been silently worked around at both `2026-09-14__release-v9.4` and `2026-09-15__release-v9.5` sprint planning without being fixed at the source.

**Scope**
- Update STEP -1 Hard Gates 1 and 2 to cite `shared_standards.md §10.1` directly instead of restating an independent status enum
- Apply the full CLAUDE.md §6 Governance File Edit Checklist (version bump, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry) in the same commit

**Acceptance Criteria**
- STEP -1 Hard Gates 1–2 no longer contain a literal status enum independent of `shared_standards.md §10.1`
- Next `plan sprint` invocation's preflight reads cleanly with no drift advisory needed
- Head of Specs Team sign-off

---

### BLG-BE-118 — list_backtest_rule_runs has no negative-limit validation and no offset param
**Priority:** P3 (Low)
**Type:** Bug
**Owner:** Backend Engineering Patterns Owner
**Source:** ST-03/EPIC-01/2026-09-15__release-v9.5 (BLG-BE-113) — discovered while implementing that story's screener limit/offset negative-value fix, out of scope for it — 2026-09-16
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
`GET /backtest-rule-changes/runs` (`backend/routers/backtest_rule_change.py::list_backtest_rule_runs`) accepts `limit: int = 20` with no lower-bound validation and has no `offset` param at all. A negative `limit` falls through to `get_backtest_rule_runs(limit=limit)`, and the endpoint's broad `except Exception` handler returns HTTP 500 with the raw exception message rather than a clean 400, the same class of gap BLG-BE-113 fixed on the screener endpoints.

**Scope**
- Validate `limit` is non-negative (and apply a sane upper bound, matching the screener endpoints' pattern) before calling `get_backtest_rule_runs`
- Return HTTP 400 `INVALID_PARAMS` for a negative `limit` instead of relying on the generic exception handler
- Decide whether an `offset` param is actually needed for this endpoint's use case (add if so; document why not if not)

**Acceptance Criteria**
- A negative `limit` on `GET /backtest-rule-changes/runs` returns HTTP 400 `INVALID_PARAMS`, not a 500
- Existing passing behaviour for valid `limit` values is unchanged

---

### BLG-BE-119 — calculate_trailing_stop's entry-price floor for profitable positions diverges from strategy_rules.md §7.2/§7.3 and from the backtest tool
**Priority:** P2 (Medium-High)
**Type:** Backend / Strategy Correctness
**Owner:** Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner
**Source:** ST-04/EPIC-01/2026-09-15__release-v9.5 (BLG-BE-114) — discovered while diffing the 3 named ATR trailing-stop implementations before attempting consolidation, per that story's own Notes ("file any unclear divergence as its own item rather than guess") — 2026-09-16
**Effort:** S (~0.5–1d — mostly decision + documentation; code change scope depends on which side is chosen)
**Provisional-Target:** v9.6
**Depends on:** BLG-BE-114 (ST-04's consolidation cannot safely complete until this is ratified)

**Problem**
`backend/utils/calculations.py::calculate_trailing_stop` — the production function used by both call sites in `backend/services/position_service.py` (the nightly stop-update job and the position-analysis path) — computes `trailing_stop = max(current_stop, new_stop, entry_price)` for profitable positions, i.e. it floors the stop at `entry_price` ("protect gains", per its own inline comment). The canonical strategy spec `claude/strategy/strategy_rules.md` §7.2/§7.3 defines the formula with only two terms — `Stop = CurrentPrice - (ProfitATRMultiplier * ATR)` then `UpdatedStop = max(CurrentStop, NewlyCalculatedStop)` — with no entry-price floor at all. `backend/position_manager.py` (the standalone backtest tool)'s `analyze_positions()` and `tests/test_stop_reconciliation.py`'s `spec_stop`/`spec_updated_stop` helpers both correctly implement the two-term spec formula and reconcile against each other and against `golden_outputs.json` — but none of the existing golden vectors (SL-01 through SL-07) supply both an `entry_price` and a profitable `new_stop` below it, so this divergence between production and the documented spec has never been caught by any test. Backtest results are therefore not a faithful simulation of live behaviour for profitable positions, and no one has formally decided which formula is actually correct.

**Scope**
- Strategy Rules & System Intent Owner decides: (a) ratify the entry-price floor as intentional, add it to `strategy_rules.md` §7.2 as a normative rule (removing the now-stale two-term-only wording), and bring `position_manager.py`'s backtest formula into line with it — this will change backtest results for profitable positions; or (b) treat production's floor as an unintended deviation and decide whether to remove it from `calculate_trailing_stop` — this is a live trading behaviour change on real capital and needs explicit sign-off before any code change
- Add a golden-output test case that actually exercises the entry-price-floor-binding scenario (profitable position, `new_stop` computed below `entry_price`) regardless of which side is chosen, so this class of gap cannot recur silently
- Once ratified, resume `BLG-BE-114`/ST-04's shared-function consolidation using the now-single, decided formula

**Acceptance Criteria**
- A formal decision is recorded (either updates `strategy_rules.md` §7.2 to include the floor, or removes it from `calculate_trailing_stop` — not both, not neither)
- `position_manager.py`, `calculate_trailing_stop`, and the spec formula all agree after the decision is implemented
- A new golden-output case exercises the previously-untested entry-price-floor-binding scenario
- `BLG-BE-114`/ST-04 unblocked and able to proceed to a single shared implementation

---

### BLG-BE-120 — JsonLinesFormatter does not truncate `message` to the spec's 500-char max
**Priority:** P3 (Low)
**Type:** Backend / Spec Conformance
**Owner:** Backend Engineering Patterns Owner
**Source:** PR #1712 review (Director of Quality agent-mediated review), EPIC-01/v9.5 (BLG-BE-112) — 2026-09-16
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
`backend/utils/json_log_formatter.py::JsonLinesFormatter` (added by `BLG-BE-112`/ST-02) does not truncate the `message` field to the 500-character max that `docs/specs/structured_logging_standards.md`'s §Structured Log Format table documents ("message | string | Free text (max 500 chars)"). An unbounded log message (e.g. a long exception string or a runaway f-string) could produce oversized JSON log lines, which is worth bounding given this repo already tracks log/AI-audit storage cost elsewhere (EPIC-02's cost-monitoring items).

**Scope**
- Truncate `message` to 500 characters in `JsonLinesFormatter.format()`, with a clear marker (e.g. trailing `"…[truncated]"`) when truncation occurs
- Add a unit test confirming a message over 500 characters is truncated and one at/under the limit is untouched

**Acceptance Criteria**
- A log message longer than 500 characters is truncated to the spec's limit in the emitted JSON
- Existing `tests/test_json_log_formatter.py` cases still pass unchanged

---

### BLG-QA-179 — No end-to-end test confirms backend/main.py's wired root logger actually emits JSON in situ
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** PR #1712 review (Director of Quality agent-mediated review), EPIC-01/v9.5 (BLG-BE-112) — 2026-09-16
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
`BLG-BE-112`/ST-02 added `tests/test_json_log_formatter.py` (unit coverage of `JsonLinesFormatter` in isolation) and relies on the pre-existing `tests/test_root_logging_config.py` (structural coverage of root logger handler count/level). Neither test connects the two: there is no test that actually runs application code through `backend/main.py`'s wired root logger handler and confirms the captured output is valid JSON Lines end-to-end. A future change that reintroduces a plain-text formatter, or wires a second handler with a different formatter, would not be caught by either existing suite.

**Scope**
- Add a subprocess-isolated test (following the existing pattern in `tests/test_root_logging_config.py`'s `_run_isolated()` helper) that imports `main`, emits a log line through a real application logger, captures stdout, and asserts it parses as JSON with the required fields

**Acceptance Criteria**
- A new test fails if `backend/main.py`'s root handler formatter is reverted to plain text or replaced with a non-JSON formatter
- Test passes against the current implementation

---

### BLG-GOV-335 — Clarify whether BLG-GOV-19/LL-v4.5-EX-01's "live system interaction" bar means AC-mandated or verification-method-used
**✅ COMPLETE — 2026-09-19 — resolved directly in post-ship closure `2026-09-15__release-v9.5` follow-up (not sprint-scoped) — `execution_prompt.md` v3.79 §3.2.A**
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Agent-mediated Director of Quality review, PR #1715 (EPIC-04, 2026-09-15__release-v9.5) — 2026-09-18
**Effort:** XS (~0.5–1h)
**Provisional-Target:** TBD

**Problem**
`execution_prompt.md` §3.2.A's LL-v4.5-EX-01 sub-criterion lets a `delegated_decision`-classified story satisfy BLG-GOV-19 Criterion 1 "provided... no observable UI behaviour, staging run, or live system interaction is required." EPIC-04's PR #1715 used this path for ST-22 (`delegated_decision`), whose own AC is written to be satisfiable either with or without live DB access ("Live schema confirmed to match spec, **or** discrepancies filed as follow-on items") — but `DATABASE_URL` happened to be available this session, and the story used it as its actual verification method, performing genuine read-only queries against a live staging database. Agent-mediated review flagged this as a defensible-but-arguable reading: the AC did not *require* live system interaction (the fallback path exists precisely for when it's unavailable), but the verification method *actually used* was live system interaction, and the sub-criterion's wording doesn't clearly distinguish "the AC mandates it" from "the session happened to use it." The engine's own autonomous-class self-sign-off resolved this ambiguity in its own favour, which is the kind of self-graded gate-eligibility call CLAUDE.md's "verify role ownership... flag the mismatch, ask for confirmation" principle is meant to catch rather than let ride.

**Scope**
- Head of Specs Team to rule: does LL-v4.5-EX-01's "no ... live system interaction is required" bar on (a) the AC's own literal requirement, or (b) whichever verification method was actually used this session?
- Update `execution_prompt.md` §3.2.A's wording to remove the ambiguity, per CLAUDE.md §6's Governance File Edit Checklist if a change is made

**Acceptance Criteria**
- Ruling recorded
- If (b): PR #1715's EPIC-04 autonomous-class sign-off should be reconsidered by an actual Director of Quality, not just the engine's own self-check — flag for the human developer's attention on that PR
- `execution_prompt.md` wording updated if the ruling requires a clarification, per the standing Governance File Edit Checklist


**Resolution (2026-09-19):** Head of Specs Team ruled (agent-mediated, §5.3) for reading **(b)**: LL-v4.5-EX-01's "no ... live system interaction is required" bar is judged against the verification method actually used, not merely whether the AC permits a documentation-only fallback; the engine may not resolve a borderline eligibility call in its own favour. `execution_prompt.md` §3.2.A wording updated (v3.78→v3.79) with the full Governance File Edit Checklist. **AC 2 — EPIC-04 sign-off reviewed (2026-09-19, Director of Quality role, agent-mediated §5.3):** independently re-ran all 5 live-schema findings (`BLG-SPEC-148`/`149`/`150`/`151`/`154`) read-only against staging as `readonly_staging` — every one reproduced exactly, so the substance is sound. Under the ruling, EPIC-04 did not qualify for autonomous class (Criteria 1 and 2 unmet: ST-22 and ST-29 verified against a live database); it was reclassified to the standard agent-mediated DoQ block, the format EPIC-01/02/03/06 used. Sealed cycle artefacts untouched (`BLG-GOV-334` precedent); review recorded in `docs/governance/doq_review_epic04_v9.5_autonomous_class_2026-09-19.md`. **Stated limit:** agent-mediated, not a human review; the broader systemic question (a forced human decision point when authoring and verifying are both agent-mediated) is not answered here and stays in `lessons_learnt_closure.md` Carry-Forward item 1.

---

### BLG-OPS-163 — Document GitHub Actions secrets ownership map

**Priority:** P3 (Low)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** Agent-mediated Director of Quality / Product Owner review of PR #1713 (EPIC-02, `2026-09-15__release-v9.5`) — 2026-09-18
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
During ST-14's staging DB credential provisioning, the bare `DATABASE_URL` GitHub Actions repo secret was repointed at a new read-only staging role — but it was also `backtest.yml`'s sole consumer, which needs write access (`production_strategy.py` upserts backtest results directly), breaking that nightly workflow until caught and fixed (`[EPIC-02][ST-14]` commit `26d5b2b1`). The same session came within one message of doing the same thing to `STAGING_DATABASE_URL`, which `reset-and-seed-staging.yml`, `seed-preview.yml`, and `scripts/reset_staging_db.sh` all depend on for write access. Both incidents happened because nothing in the repo documents which secret is used by which workflow(s), what access level each needs, or which secrets are safe to rotate independently. This is a real, now-twice-demonstrated risk class, not a hypothetical.

**Scope**
- Add a short reference doc (or a new section in an existing ops runbook) inventorying every GitHub Actions repo secret currently in use: name, consuming workflow(s), required access level (read-only / read-write, staging / production), and any known aliasing relationships (e.g. `DATABASE_URL` and `PROD_DATABASE_URL` are treated as interchangeable by `scripts/check_si05_digest_staleness.py` and `si05-digest-staleness-check.yml`)
- Cross-reference from `docs/infrastructure/staging_setup.md` §8 (the read-only staging role section added by ST-14) and from `docs/ops/production_deployment_runbook.md`

**Acceptance Criteria**
- Every secret referenced in `.github/workflows/*.yml` via `secrets.*` appears in the inventory with its consuming workflow(s) and required access level
- Document is discoverable from the two cross-references named above
- Infrastructure & Operations Owner sign-off

---

### BLG-OPS-164 — Confirm synthetic uptime monitor live-fire and notification delivery (ST-11 follow-up)

**Priority:** P3 (Low)
**Type:** Operations
**Owner:** Infrastructure & Operations Owner
**Source:** Agent-mediated Product Owner review of PR #1713 (EPIC-02, `2026-09-15__release-v9.5`) — 2026-09-18; follow-up to ST-11 (BLG-OPS-158)
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-11 (`BLG-OPS-158`) found `.github/workflows/health-check-alert.yml` already satisfies "monitor configured, independent of hosting dashboard" — but could not complete the "confirmed firing on a deliberate test failure" or "notification path confirmed working" halves of its own AC: both `gh workflow run health-check-alert.yml -f test_url=...` and `gh secret list` returned `HTTP 403` (insufficient token scope) in that execution session. Concrete follow-up steps are already written down in `docs/ops/synthetic_uptime_monitor_confirmation_2026-09-16.md` §6, but nothing outside that document tracks or surfaces the gap — it was flagged in review (PR #1713) as needing its own visible item rather than staying buried in a confirmation doc.

**Scope**
- Run `gh workflow run health-check-alert.yml --ref main -f test_url=https://httpstat.us/500` (or trigger the equivalent via the Actions tab UI) with a token/session that has Actions-write access
- Confirm the run's "Send alert on sustained 5xx" step executes (not the `::warning::` fallback branch) and a real Telegram message is received
- Append the confirmed result to `docs/ops/synthetic_uptime_monitor_confirmation_2026-09-16.md` §7 (already scaffolded, currently "Not yet performed")

**Acceptance Criteria**
- A real live-fire test run is confirmed to have triggered the alert path (run URL/ID recorded)
- A real Telegram notification is confirmed received (not just that the workflow step executed)
- `docs/ops/synthetic_uptime_monitor_confirmation_2026-09-16.md` §7 and §8 updated to reflect the confirmed result; `BLG-OPS-158`'s (ST-11's) original disclosed gap closed

---

### BLG-QA-180 — Add Playwright duration-assertion coverage for the 9 toast call sites fixed in ST-42 (Toast Notification Timing standard)

**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Sprint execution `2026-09-15__release-v9.5`, ST-42/`BLG-FE-176`, discovered mid-story — 2026-09-18
**Effort:** S (~0.5d)
**Provisional-Target:** v9.6

**Problem**
ST-42 fixed all 9 non-conforming toast call sites (`Layout.js`, `Settings.js` ×2, `Signals.js` ×2, `Positions.js` ×2, `PositionCard.js`, `useWatchlistModal.js`) to carry the correct `duration` per `design_system.md`'s Toast Notification Timing standard — `Layout.js`'s incorrect `duration: 8000` on an info toast was removed (reverting to the 4s default), and the 8 `toast.error(...)` sites each gained an explicit `duration: 8000`. No existing Playwright test asserts on toast duration/dismissal timing for any of these 9 sites (confirmed via grep across `tests/e2e/` for each site's exact message text — zero matches). The fix was verified by code review plus re-running unrelated-but-adjacent Playwright suites (`watchlist.spec.js`, `settings-heading-order-and-aria-labelledby-regression.spec.js`, `v7.2-dashboard-tradeplan-ux-hardening.spec.js`) confirming no runtime regression, but none of those assert the new duration values themselves.

**Scope**
- Add Playwright assertions for the 9 call sites confirming each toast's configured duration matches the standard (8s for error, 4s default for the `Layout.js` info toast) — e.g. asserting the toast remains visible past the old 4s default before disappearing, or reading the rendered duration where `sonner` exposes it

**Acceptance Criteria**
- A regression test exists per call site (or a consolidated test covering all 9) that would fail if a future change silently reverted any site's `duration` back to a non-conforming value
- Tests pass against the current (ST-42) implementation

---

### BLG-GOV-336 — OPERATIONAL_GUIDE.md §14 quick-reference table's own "Last Updated" cell desyncs from its "Version" cell across multi-bump sessions
**✅ COMPLETE — 2026-09-19 — resolved directly in post-ship closure `2026-09-15__release-v9.5` follow-up (not sprint-scoped) — `governance-drift` skill Step 1b; `OPERATIONAL_GUIDE.md` v4.198**

**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Agent-mediated Director of Quality review of PR #1716 (EPIC-05, `2026-09-15__release-v9.5`) — 2026-09-18
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`OPERATIONAL_GUIDE.md` §14's "Playbook Governance" quick-reference table has two adjacent cells: `Version` and `Last Updated`. Across PR #1716's 6 consecutive governance-prompt version bumps (v4.190→v4.196, ST-31/32/33/36/37/39), every commit message claimed "§14 self-row Version/Last Updated 4.19X/2026-09-18→4.19Y/2026-09-18" — but only the `Version` cell was actually edited each time; the `Last Updated` cell was never touched and still reads its pre-session value (`2026-09-15`) despite `Version` reading `4.196`. This is exactly the class of self-inconsistency the `governance-drift` skill's Step 1b check exists to catch (header / §14 self-row / Change Log top row), but that check's own definition of "§14 self-row" apparently covers only the `Version` cell, not its sibling `Last Updated` cell in the same quick-reference table — so it did not fire across 6 consecutive misses in one session.

**Scope**
- Fix the current `Last Updated` cell value in the §14 quick-reference table to match the document's own top-header `Last Updated` date
- Extend the `governance-drift` skill's self-consistency check (or the equivalent instruction in `execution_prompt.md` §3.2.A) to explicitly include this `Last Updated` cell as a 4th checked field, not just `Version`

**Acceptance Criteria**
- §14 quick-reference table's `Last Updated` cell matches the document's top-header `Last Updated` date
- `governance-drift` skill (or equivalent) documented to check this cell going forward; re-run confirms no drift


**Resolution (2026-09-19):** §14 self-row corrected (`Version 4.196 / Last Updated 2026-09-15` → `4.198 / 2026-09-19`; the 4.197 bump earlier that day had missed it too — the same failure recurring). `.claude/skills/governance-drift/SKILL.md` Step 1b now compares all six readings (version and date at header, §14 self-row, Change Log top row) and reports `DATE-ONLY DRIFT`. Re-run confirmed PASS on all six readings.

---

### BLG-QA-181 — Add regression coverage for the motion-timing values fixed in ST-41 (500ms ceiling components)

**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Agent-mediated Director of Quality review of PR #1717 (EPIC-06, `2026-09-15__release-v9.5`) — 2026-09-18
**Effort:** S (~0.5d)
**Provisional-Target:** v9.6

**Problem**
ST-42 (same EPIC) correctly filed `BLG-QA-180` when it found no Playwright test asserts the specific `duration` values its 9 toast fixes introduced. ST-41 has the identical gap and none was filed for it: no Playwright test asserts `SystemStatus.js`/`Signals.js`/`Reports.js`/`RecentTradesWidget.js`'s actual `delay`/`duration` transition-prop values (Playwright cannot easily read a React `transition` prop directly — coverage would need a timing-based or prop-inspection approach). Two of the fixed values now sit at exactly the 500ms ceiling with zero margin (`Reports.js`: `0.2s` max delay + `0.3s` duration = `0.5s`; `RecentTradesWidget.js`: same), meaning a future, unrelated change to either component's animation (e.g. bumping `duration` for a different visual reason) could silently push it back over the ceiling with nothing in CI to catch it.

**Scope**
- Add regression coverage for the 4 components' motion-timing values fixed in ST-41 — e.g. a lightweight source-inspection test (grep/AST-based, checking the literal `delay`/`duration` values in each file) or a timing-based Playwright assertion, whichever is more practical for framer-motion transition props
- Cover both fixed-value components (exact-ceiling risk) and the capped/staggered components (regression risk if the cap constant is later removed)

**Acceptance Criteria**
- A regression test/check exists that would fail if any of the 4 components' `max(delay) + duration` were pushed back over 500ms by a future change
- Test/check passes against the current (ST-41) implementation

---

### BLG-GOV-337 — Decide whether `claude/roadmap/workforce_capacity.md` needs an explicit Sprint Execution write-scope exception
**✅ COMPLETE — 2026-09-19 — resolved directly in post-ship closure `2026-09-15__release-v9.5` follow-up (not sprint-scoped) — `execution_prompt.md` v3.79 §7**

**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team; Product Owner
**Source:** Agent-mediated Product Owner review of PR #1716 (EPIC-05, `2026-09-15__release-v9.5`) — 2026-09-18
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`execution_prompt.md` §7 (Write Scope Restriction) lists `claude/roadmap/*` under "Must not modify" with no carve-out — yet ST-37/ST-38 (this same PR) both edit `claude/roadmap/workforce_capacity.md` directly, per their own sealed `sprint_backlog.md` acceptance criteria. The engine's own disclosure treated the sealed sprint plan's "Within-EPIC only: workforce_capacity.md (EPIC-05 — ST-37 lands before ST-38)" sequencing note as implicit authorization for this specific file, but §7's own text carries no such exception — unlike `claude/backlog/backlog.md`, which already has a narrow, explicitly-documented new-item-addition exception for exactly this kind of situation. Leaving the question inferred rather than decided risks a different session reading the same hard-gate text more strictly (and incorrectly halting a similarly-scoped future story) or more loosely (and writing to a genuinely out-of-scope roadmap file without sealed-plan cover).

**Scope**
- Product Owner + Head of Specs Team rule on whether Sprint Execution should have a standing, narrow write-scope exception for `workforce_capacity.md` specifically (mirroring the existing `backlog.md` new-item-only exception's shape — i.e. still barred from `current_roadmap.md`, `scored_initiatives.md`, and other roadmap-planning content)
- If yes: add the exception to `execution_prompt.md` §7 with the same Governance File Edit Checklist rigor as any other prompt change
- If no: document why ST-37/ST-38's write was accepted as sealed-plan-authorized this one time without generalising it, so the next similar case isn't decided ad hoc again

**Acceptance Criteria**
- A recorded Product Owner + Head of Specs Team decision exists (either a §7 prompt change, or a documented one-off ruling)
- The decision is cross-referenced from `execution_prompt.md` §7 (as a change, or as a note pointing to the ruling) so a future session reading §7 sees the resolved position rather than re-deriving it


**Resolution (2026-09-19):** Head of Specs Team + Product Owner ruled (agent-mediated, §5.3) for a **narrow, plan-authorised standing exception**: `workforce_capacity.md` may be written only where the cycle's sealed `sprint_backlog.md` names it in an ST item's AC or sequencing note (so authority comes from a plan the Product Owner already signed at the Sprint Planning seal, not from the engine's inference). Not extended to any other `claude/roadmap/*` file or to any prioritisation decision. ST-37/ST-38 retroactively ratified. `execution_prompt.md` §7 updated (v3.78→v3.79), which is the cross-reference AC 2 requires.

---


## Idea Intake IW-20260919-01 — Promoted-Backlog Disposition (roadmap rebalance `2026-09-19__scheduled`)

*41 of the window's 44 submissions promoted to backlog per STEP 4 "📋 Backlog" disposition, filed as **36 items** after 4 consolidations (Idea Consolidation convention); 35 are ungated and 1 (`BLG-SEC-37`) is gate-conditional. 2 submissions parked (`Parked-cycle-1`), 1 rejected as already implemented. **Plus 1 item (`BLG-GOV-345`) filed from this rebalance's own lessons learnt, not an idea** — 37 items in all. All carry `**Provisional-Target:** TBD` (Now/Next horizons both empty — §16.6 fallback) and no release-specific effort day-range is required (§16.12 n/a). `BLG-FEAT-96`, `BLG-FEAT-97`, `BLG-SPEC-160`, `BLG-OPS-166` and `BLG-GOV-345` are P2 by explicit PO decision (see `claude/cycles/2026-09-19__scheduled/cycle_record.md` STEP 4). Window: `claude/ideas/window_summary_IW-20260919-01.md`.*

### BLG-AI-07 — Golden-fixture CI regression for AI prompt templates — boundary-language drift caught at template-change time
**Priority:** P3 (Low)
**Type:** AI Compliance / QA Tooling
**Owner:** AI Compliance & Governance Officer; QA & Testing Owner
**Source:** IDEA-ai-compliance-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
Boundary-language sampling (`BLG-AI-04` quarterly re-scan, `BLG-AI-06` generation-time hook) inspects text after generation, so a prompt-template edit that reintroduces predictive or advice-crossing phrasing is caught only at the next sample (up to ~90 days). `claude_audit_log` already records `model_id` and `prompt_version` (confirmed in `backend/database.py`), so attribution exists — but nothing asserts that `prompt_version` actually changes when a template's text changes.

**Scope**
- Fixed rendered-prompt fixtures per AI endpoint (chat, briefing, debrief) checked against the `strategy_rules.md` §13.2 disallowed-phrase list — deterministic, template-level, no live API call
- CI test asserting no disallowed phrase appears in any rendered template
- CI test asserting `prompt_version` differs whenever a template's text hash differs

**Acceptance Criteria**
- CI fails when a disallowed phrase is introduced into any covered template
- CI fails when template text changes without a `prompt_version` change
- The suite runs without `ANTHROPIC_API_KEY`

*Note: `IDEA-ai-compliance-20260919-02` (stamp model/prompt version on audit rows) was rejected as already implemented; its residual value — asserting the version actually moves — is folded into this item's third scope bullet.*

---

### BLG-API-04 — Document idempotency and double-submit behaviour for every mutating endpoint
**Priority:** P3 (Low)
**Type:** Spec Debt / API Contracts
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
No contract states what a retried `POST` does. `BLG-BE-115`/DS-17 (duplicate open positions) shows the risk is real, yet retry and double-submit semantics for `POST /trades`, `POST /trade-plans` and position entry are specified nowhere.

**Scope**
- Add an "Idempotency / retry behaviour" subsection to every mutating endpoint's contract in `docs/specs/api_contracts/`
- Verify each statement against code and tests (for example the DS-17 unique index); where behaviour is undefined, record it as such and file a follow-up item

**Acceptance Criteria**
- Every `POST`/`PUT`/`PATCH`/`DELETE` heading in `docs/specs/api_contracts/` carries the subsection
- Undefined behaviours are listed and each has a filed backlog item
- Endpoint headings remain `## METHOD /path` (OpenAPI drift gate unaffected)

---

### BLG-API-05 — Error-payload (4xx/5xx) examples for the 10 most-called endpoints, covered by the example-freshness checker
**Priority:** P3 (Low)
**Type:** Spec Debt / API Contracts
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
Contracts carry success examples; the overlap scan found no backlog item covering error-response examples, so client-side error handling is specified by reading code. `BLG-SPEC-139` established freshness checking for example payloads; error payloads are outside what any item covers.

**Scope**
- Pick the 10 most-called endpoints (from `api_performance_baseline.md`) and add at least one 4xx example each
- Extend the contract example-freshness checker to compare error examples against the canonical error envelope

**Acceptance Criteria**
- 10 endpoints carry ≥1 error example
- The freshness checker fails when an error example diverges from the envelope

---

### BLG-BE-121 — Float-vs-Decimal money-arithmetic audit with rounding-boundary golden tests
**Priority:** P3 (Low)
**Type:** Backend / Correctness
**Owner:** Backend Engineering Patterns Owner; Financial Reporting & Records Owner
**Source:** IDEA-backend-engineering-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** M (~1.5–2d)
**Provisional-Target:** TBD

**Problem**
Share-count, FX-conversion and P&L paths mix float operations across services; rounding-boundary behaviour (`strategy_rules.md` §4.1.3, §4.1.5) is asserted nowhere as a class, so a one-penny discrepancy would surface only in reconciliation.

**Scope**
- Inventory float-vs-Decimal use in sizing, FX conversion and P&L code paths
- Add golden tests pinning rounding at the boundary cases in §4.1.3/§4.1.5
- Where a path is unsafe, file a fix item rather than changing behaviour in this story

**Acceptance Criteria**
- Inventory recorded in the QA evidence file
- Golden tests for each boundary case pass
- 0 unexplained ≥£0.01 discrepancies across the sizing golden set

---

### BLG-BE-122 — Shared upstream-call helper: uniform timeout and bounded retry budget for yfinance, Alpaca and Anthropic
**Priority:** P3 (Low)
**Type:** Backend / Reliability
**Owner:** Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** M (~1.5–2d)
**Provisional-Target:** TBD

**Problem**
`timeout=` is set ad hoc at ~25 call sites across at least 8 backend modules that call external APIs; a hung call in the nightly stop-update path would stall stop ratcheting (`strategy_rules.md` §7.3).

**Scope**
- Introduce one helper that applies a per-provider timeout and a bounded retry budget
- Migrate the nightly stop-update and screener call paths first; list remaining call sites as follow-ups

**Acceptance Criteria**
- No unbounded upstream call remains in the nightly stop-update path
- Timeout and retry values are configured in one place
- Existing tests still pass; new tests cover timeout and retry-exhaustion

---

### BLG-FE-180 — Flag stale 'planned' trade plans on the Trade Plans list
**Priority:** P3 (Low)
**Type:** Frontend / UX Enhancement
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-product-owner-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
Trade plans in `planned` status accumulate with no visual cue that they are old and unactioned.

**Scope**
- Show a display-only "Stale (N days)" marker on plans in `planned` status older than a fixed threshold (default 14 days)
- No automated action — marker only (§3 human-in-the-loop)

**Acceptance Criteria**
- A `planned` plan older than the threshold shows the marker; a newer plan does not
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

---

### BLG-FE-181 — Name one primary next action in every empty state
**Priority:** P3 (Low)
**Type:** Frontend / UX Enhancement
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~1d)
**Provisional-Target:** TBD

**Problem**
v9.5 consolidated empty-state copy (wording); the overlap scan found no backlog item requiring each empty state to name a next action, so a first-time or cleared view can be a dead end.

**Scope**
- Audit empty states across pages
- Add one primary next-action link per empty state (for example "Run the screener", "Create a plan")

**Acceptance Criteria**
- 0 audited empty states without a next-action link
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

---

### BLG-FE-182 — Single number/currency formatting helper — audit and migrate the highest-traffic tables
**Priority:** P3 (Low)
**Type:** Frontend / Consistency
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** M (~2d)
**Provisional-Target:** TBD

**Problem**
`toFixed(` appears in 68 files under `src/` and `toLocaleString`/`Intl.NumberFormat` in 19, and no shared currency-format helper export was found — inviting inconsistent GBP/USD symbol, decimals and negative-number presentation (`strategy_rules.md` §4.1.5).

**Scope**
- Add one shared helper for currency, percentage and R-multiple formatting
- Migrate Positions, TradeHistory and TradePlans first; list the rest as follow-ups

**Acceptance Criteria**
- The three tables use the helper with identical negative/decimal conventions
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

---

### BLG-FE-183 — CI lint of static UI copy for forbidden predictive or advice-crossing phrases
**Priority:** P3 (Low)
**Type:** Frontend / QA Tooling
**Owner:** Base44 Frontend Prompt Owner; AI Compliance & Governance Officer
**Source:** IDEA-base44-frontend-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
The overlap scan found no automated check of static UI copy (as distinct from AI output) for §13.2 language; review is the only control on record.

**Scope**
- Scan string literals in `src/` against the §13.2 disallowed-phrase list in CI
- Allow-list mechanism with a required justification

**Acceptance Criteria**
- CI fails on a disallowed phrase in a new string literal
- Allow-list entries require a justification

---

### BLG-FEAT-96 — 'Clone as new plan' action on the Trade Plans list
**Priority:** P2 (Medium)
**Type:** Product Feature / Frontend
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-head-of-engineering-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
Creating a plan for a similar setup restarts from blank (`TradePlans.js`/`TradePlan.js` offer no clone), which adds friction to the pre-entry planning that `strategy_rules.md` §4 requires and that drives the linked-plan volume the SI-02 gate depends on. **Priority escalated P3→P2 at intake as a named `roadmap_prompt.md` §7.1 mandatory pull-forward candidate** (ungated, build-and-ship; same mechanism as `BLG-FEAT-95` at `2026-09-14__scheduled`).

**Scope**
- Add a Clone action to each plan row/detail that opens a new plan pre-populated with setup fields, thesis and checklist template
- The clone starts in `planned` status with no position link — `position_id` must NOT be copied (would corrupt the SI-02 linked-plan count)

**Acceptance Criteria**
- Clicking Clone opens a new, unsaved plan pre-populated from the source
- The cloned plan has status `planned`, fresh dates and no `position_id`
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

---

### BLG-FEAT-97 — CSV export for Screener results and Watchlist
**Priority:** P2 (Medium)
**Type:** Product Feature / Frontend
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-head-of-engineering-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
Reports and TradeHistory export CSV (`src/pages/Reports.js`, `TradeHistory.js`); Screener and Watchlist do not (confirmed by `src/` search), so ranked candidates cannot leave the app. **Priority escalated P3→P2 at intake as a named `roadmap_prompt.md` §7.1 mandatory pull-forward candidate** (ungated, build-and-ship).

**Scope**
- Add an Export CSV control to Screener results and Watchlist reusing the existing export pattern
- Columns match the visible columns; UTF-8 with a header row; filename carries the date; client-side, nothing persisted

**Acceptance Criteria**
- Export downloads a file whose columns equal the visible columns on both pages
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

---

### BLG-FEAT-98 — In-app reminder to complete TradeReflection within 48 hours of a trade closing
**Priority:** P3 (Low)
**Type:** Product Feature / Frontend + Backend
**Owner:** Product Owner; Head of Engineering
**Source:** IDEA-product-owner-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** M (~1–2d)
**Provisional-Target:** TBD

**Problem**
Reflection data feeds Arc 4 (PO-02/PO-04), which are gated on data volume; completion currently depends on the operator remembering. A reminder raises reflection completion and so accelerates the data-density gates without automating anything (`strategy_rules.md` §3 — prompt, never act).

**Scope**
- Create a dismissible in-app notification 48h after a trade closes with no reflection, using the existing Notifications infrastructure
- At most one reminder per trade; respects `NotificationPreferences`

**Acceptance Criteria**
- A closed trade without a reflection produces exactly one reminder after 48h
- Completing the reflection or dismissing suppresses it
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

---

### BLG-FR-04 — Audit whether closed-trade P&L is net of fees_paid; flag closed trades with NULL fees_paid in Monthly P&L
**Priority:** P3 (Low)
**Type:** Financial Reporting / Data Integrity
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
`fees_paid` is calculated at entry (`position_service.py`, `calculate_uk/us_entry_fees`) and `BLG-SPEC-151` records it as nullable on the live table, but `fees_paid` is not referenced in `analytics.py` or `trades_export.py` — so it is unclear whether reported P&L is gross or net of fees, and a NULL would silently differ.

**Scope**
- Determine and document whether Monthly P&L and the tax-year table are net or gross of fees
- Surface a 'fees not recorded' count where NULL-fee closed trades exist

**Acceptance Criteria**
- The net/gross basis is documented in the canonical metrics spec
- A NULL-fee closed trade is counted and visible in Monthly P&L

---

### BLG-FR-05 — Month-end immutable snapshot of Monthly P&L and the tax-year table, with a restatement diff
**Priority:** P3 (Low)
**Type:** Financial Reporting / Records Integrity
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** M (~2d)
**Provisional-Target:** TBD

**Problem**
A later edit to a closed-trade row silently restates an already-reviewed month; nothing records what a month showed when it was reviewed.

**Scope**
- Persist a read-only snapshot per closed month
- Show a diff when the live figures for a snapshotted month differ

**Acceptance Criteria**
- A snapshot exists per closed month
- Editing a closed trade in a snapshotted month surfaces a restatement diff

---

### BLG-GOV-338 — Bake accessible-name and heading-order rules into the Base44 prompt template
**Priority:** P3 (Low)
**Type:** Governance / Base44
**Owner:** Base44 Frontend Prompt Owner; Frontend Specifications & UX Documentation Owner
**Source:** IDEA-base44-frontend-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
Accessible-name and heading-order defects were fixed page by page (`BLG-FE-170`/`171`) with nothing preventing the next regeneration reintroducing them.

**Scope**
- Add `aria-labelledby`-over-duplicated-`aria-label` and heading-order rules to the Base44 prompt template
- Record the change in the prompt versioning changelog

**Acceptance Criteria**
- The template carries both rules
- A regenerated page in a test run introduces no new axe-core `KNOWN_VIOLATIONS` entries

---

### BLG-GOV-339 — PVR / Skill-Silo measurement package — split debt into user-protective vs hygiene, add effort-weighted PVR, add a leading ungated-U-pool indicator
**Priority:** P3 (Low)
**Type:** Governance / Metrics
**Owner:** Metrics Definitions & Analytics Owner; Head of Specs Team
**Source:** IDEA-challenger-20260919-01, IDEA-challenger-20260919-02, IDEA-metrics-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled (consolidates 3 ideas — Idea Consolidation convention)
**Effort:** M (~1.5–2d)
**Provisional-Target:** TBD

**Problem**
Three consecutive PVR Alert readings (0.110 / 0.092 / 0.046) and a 99.0% Skill-Silo reading cannot drive a differentiated response: `D` is 122 of 195 stories in the current window, conflating user-protective debt (bug, security, data integrity) with hygiene; story counts weight a one-hour fix like a two-week build; and both mandatory clauses depend on a pool of ungated U-items that neither clause replenishes. Three submissions converge on this one problem (Idea Consolidation convention).

**Scope**
- Define a user-protective vs hygiene split of `D` and re-tag at ship time going forward
- Report an effort-weighted PVR alongside the story-count PVR in `product_value_ratio_history.md`
- Add a leading indicator: count of ungated, build-and-ship U-items in the backlog at each rebalance
- **Proposal only** — any change to `roadmap_prompt.md` STEP 2.4/§7.1 needs Head of Specs Team + Product Owner sign-off and the CLAUDE.md §6 checklist

**Acceptance Criteria**
- Definitions documented in `metrics_definitions.md`
- History file carries both readings for the last 5 windows
- Leading indicator computed at the next rebalance

---

### BLG-GOV-340 — Delivery-flow metrics — lead time by priority band and ready-pool runway forecast
**Priority:** P3 (Low)
**Type:** Governance / Metrics
**Owner:** Metrics Definitions & Analytics Owner; PMO Lead
**Source:** IDEA-metrics-20260919-02, IDEA-pmo-lead-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled (consolidates 2 ideas — Idea Consolidation convention)
**Effort:** S (~1d)
**Provisional-Target:** TBD

**Problem**
No measure shows whether P1/P2 items ship faster than P3, and §7.3 measures the ready-pool gap retrospectively — nothing projects when the pool empties. Both are delivery-flow observability gaps (Idea Consolidation convention).

**Scope**
- Median filed→shipped days by priority band per cycle (from `backlog_archive.md` and the changelog)
- One projected 'cycles until empty' number per rebalance, given intake and capacity

**Acceptance Criteria**
- Both metrics defined and computed for the last 5 cycles
- The runway figure is cited in the next rebalance's STEP 7.3

---

### BLG-GOV-341 — Persist STEP 7.2 role-share tallies as a structured history file
**Priority:** P3 (Low)
**Type:** Governance / Workforce
**Owner:** Director of HR; PMO Lead
**Source:** IDEA-director-of-hr-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
STEP 7.2 re-tallies free-text `**Owner:**` fields each rebalance; at `2026-09-14__scheduled` raw counts exceeded story totals in 3 of 3 cycles, and at this rebalance again (v9.3: 35 raw vs 27 stories). Complements — does not replace — the deferred Owner-field canonicalisation patch.

**Scope**
- Create a history file (one row per cycle, primary-owner counts) analogous to `product_value_ratio_history.md`
- Wire STEP 7.2 to read and append it

**Acceptance Criteria**
- History backfilled for the last 3 cycles
- STEP 7.2 reads the file instead of re-parsing Owner fields

---

### BLG-GOV-342 — JSON Schema for `.claude_current_state.json`, including the `last_updated_utc` field the roadmap engine reads
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
`roadmap_prompt.md` STEP -1.6 reads `last_updated_utc`, which the state file does not carry, so the state-age advisory fires on every run (confirmed at `2026-09-19__scheduled`, with `last_sync_utc` fresh).

**Scope**
- Author a JSON Schema for the state file
- Identify each engine that writes state and have it set `last_updated_utc`
- Validate against the schema in preflight or the `governance-drift` skill

**Acceptance Criteria**
- The state file validates
- The state-age advisory computes a real age instead of always firing

---

### BLG-GOV-343 — Split `roadmap_prompt.md` into a core plus an appendix so it fits a single read
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** M (~1.5–2d)
**Provisional-Target:** TBD

**Problem**
`BLG-GOV-08` (retired 2026-05-13) fixed engine-prompt size once; `roadmap_prompt.md` has since regrown to 957 lines (~34,214 tokens), past the 25,000-token single-read cap — it could not be read in one pass at `2026-09-19__scheduled`. Re-opens that concern with new evidence.

**Scope**
- Move dated decision notes and long rationale blocks to an appendix with pointer stubs; keep every STEP's procedure in the core
- Apply the CLAUDE.md §6 checklist

**Acceptance Criteria**
- Core ≤25,000 tokens
- No procedural step lost (diff-verified)
- §6 checklist complete

---

### BLG-GOV-344 — Parameter-change ledger for `strategy_rules.md` §11 production parameters
**Priority:** P3 (Low)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
Parameter history is recoverable only from git and the change log. Refines `BLG-GOV-95` (annual review schedule): that item schedules review; this adds the history ledger it would read.

**Scope**
- One row per §11 parameter change: date, old→new, justification, link

**Acceptance Criteria**
- Ledger backfilled from the strategy_rules change log
- §12.3 change control references it

---

### BLG-GOV-345 — Release-planning gate scan treats lapsed date gates as permanently gated
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** Head of Specs Team; Product Owner
**Source:** Roadmap rebalance 2026-09-19__scheduled, Friction Item 1 (`lessons_learnt.md`) — not an idea submission
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
`scripts/scan_backlog_gate_conditions.py` and `release_planning_prompt.md` §1.3a classify by the presence of a `**Gate criteria:**` field, not by evaluating dates. At 2026-09-19, gates whose date has lapsed are still counted gated: `BLG-FEAT-59`, `BLG-FEAT-60`, `BLG-FEAT-63`, `BLG-FE-84` ("AI adoption window clears ~2026-07-25"), `BLG-GOV-90` (gate: first `BLG-GOV-74` review, due 2026-08-29; `BLG-GOV-74` shipped v9.1), and `BLG-GOV-188` ("None — … Met 2026-07-08"). Gates clearing 2026-09-24: `BLG-GOV-140`/`141`/`142`, `BLG-OPS-88`. Each is excluded from the ready pool at v9.3–v9.5 planning, which also hid `BLG-FEAT-59` (an ungated-once-verified build-and-ship U-item) from the §7.1 candidate search. Found at `2026-09-19__scheduled` (Friction Item 1).

**Scope**
- Extend the scan to parse ISO dates in gate text and emit a 'date-lapsed — verify' list
- Update `release_planning_prompt.md` §1.3a to require that list be read before the ready pool is fixed
- Individually verify and clear or re-gate the six items above

**Acceptance Criteria**
- Scan reports lapsed-date items separately
- Each of the six items is verified and either cleared (gate line removed, dated note) or re-gated with a new dated condition
- §6 checklist complete for any prompt change

*Note: Source: this rebalance's own lessons learnt, not an idea.*

---

### BLG-OPS-165 — CI minutes and artifact-storage visibility; explicit retention on the 3 uploads that lack it
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260919-01, IDEA-finops-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled (consolidates 2 ideas — Idea Consolidation convention)
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
Cost visibility covers AI and hosting spend but not CI minutes, which grew with the Playwright shard increase 4→8 (v9.3). Retention is explicit on `playwright-report` (14 days) and the DB backup (90 days) but not on `visual-snapshot-report`, `visual-regression-report` or `smoke-test-report` (Idea Consolidation: both ideas concern GitHub Actions consumption).

**Scope**
- Track minutes and artifact storage per workflow monthly
- Set explicit `retention-days` on the three uploads without one

**Acceptance Criteria**
- A monthly per-workflow figure exists
- All artifact uploads carry explicit retention

---

### BLG-OPS-166 — Dead-man's-switch alert when nightly-stop-update has not succeeded within 26 hours
**Priority:** P2 (Medium)
**Type:** Operations / Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
A silently missed nightly run leaves stops stale on live positions until a human notices (`strategy_rules.md` §7.3). `BLG-OPS-160` (P1, v9.5) created the live trigger; `BLG-OPS-110` monitors the nightly backtest job; `BLG-OPS-164` confirms the uptime monitor — none alerts on absence of a successful stop-update run. P2 mirrors `BLG-OPS-160`'s rationale at the detection layer.

**Scope**
- Alert (existing Telegram channel) when no successful nightly-stop-update run is recorded within 26h
- Include the last-success timestamp in the alert

**Acceptance Criteria**
- A simulated missed run raises the alert within the window
- A successful run clears it

---

### BLG-OPS-167 — External-dependency failure-mode matrix (yfinance, Alpaca, Anthropic, Supabase, Render)
**Priority:** P3 (Low)
**Type:** Operations / Documentation
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
Health checks detect failures (`BLG-OPS-76`); no document states what the operator sees or does when each dependency is down.

**Scope**
- One table: dependency → user-visible degradation → manual fallback → detection

**Acceptance Criteria**
- All 5 dependencies documented

---

### BLG-QA-182 — Escaped-defect and follow-on-ratio tracking per cycle
**Priority:** P3 (Low)
**Type:** QA / Metrics
**Owner:** Director of Quality; PMO Lead
**Source:** IDEA-director-of-quality-20260919-01, IDEA-pmo-lead-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled (consolidates 2 ideas — Idea Consolidation convention)
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
v9.5 filed 21 follow-on items during execution and two PR review rounds (~0.49 per shipped story), several found only by review — no measure separates defects escaping a story from planned debt (Idea Consolidation: both concern post-merge findings).

**Scope**
- Per cycle: defects first observed after merge, linked to the originating story; follow-ons filed per shipped story

**Acceptance Criteria**
- Baseline computed for v9.5
- A per-cycle row is added at each post-ship closure

---

### BLG-QA-183 — DoQ checklist addendum for AI-touching stories
**Priority:** P3 (Low)
**Type:** QA / Governance
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
AI-touching stories (for example `BLG-AI-06`) reached sign-off with two ACs staging-only and no standard evidence shape.

**Scope**
- Addendum: record prompt-template version and a boundary-language sample in the evidence file

**Acceptance Criteria**
- The addendum exists in the DoQ template
- The next AI-touching story uses it

---

### BLG-QA-184 — Mutation-testing pilot on the sizing calculator and stop ratchet
**Priority:** P3 (Low)
**Type:** QA / Test Quality
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** M (~2d)
**Provisional-Target:** TBD

**Problem**
Passing tests do not show that the sizing (§4.1) and stop-ratchet (§7.3) tests would catch a mutated rule.

**Scope**
- Run a Python mutation tool over the two modules
- Record the mutation score and survivors; file survivors as follow-ups

**Acceptance Criteria**
- Baseline mutation score recorded for both modules
- Survivors triaged

---

### BLG-QA-185 — Strategy-rule → test traceability matrix for `strategy_rules.md` §4–§8
**Priority:** P3 (Low)
**Type:** QA / Traceability
**Owner:** QA Lead; Strategy Rules & System Intent Owner
**Source:** IDEA-qa-lead-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** M (~2d)
**Provisional-Target:** TBD

**Problem**
`BLG-BE-119` found the entry-price-floor case exercised by no golden test; no artefact maps each normative clause to an asserting test.

**Scope**
- Matrix: each normative clause → asserting test (or 'none')
- File a follow-up per clause with no test

**Acceptance Criteria**
- Matrix published
- % of clauses with an asserting test reported

---

### BLG-QA-186 — Property-based tests for 'stop never decreases' and sizing validity rules
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~1d)
**Provisional-Target:** TBD

**Problem**
Example-based tests cover chosen cases; the §7.3 hard constraint (stops never decrease) and §4.1.4 validity rules are universal invariants.

**Scope**
- Add `hypothesis` property tests for both invariants

**Acceptance Criteria**
- Both properties pass over generated inputs in CI
- A deliberately broken ratchet fails the property

---

### BLG-QA-187 — Enable Playwright trace and screenshot retain-on-failure
**Priority:** P4 (Trivial)
**Type:** QA / CI Tooling
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`playwright.yml` already retains the report artifact 14 days, but no `trace`/`screenshot` option is configured, so failure evidence is thin. Narrowed from the submitted idea after checking the workflow.

**Scope**
- Set `trace: 'retain-on-failure'` and `screenshot: 'only-on-failure'`

**Acceptance Criteria**
- A failing run's report includes a trace

---

### BLG-SEC-37 — Read-only production credential scoped to aggregate gate-check views for governed routines
**Priority:** P3 (Low)
**Type:** Security / Credentials
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD
**Gate criteria:** Explicit Product Owner + Cybersecurity & Trust Lead approval of the credential's scope and storage channel — a governed routine must not create or store this credential itself.

**Problem**
The read-only credential available to sprint-execution sessions is for **staging** and cannot answer the production questions the SI-02 gate asks; SI-02 readings have been cited from a stale structured field at every rebalance since 2026-07-28. Refines `BLG-OPS-121` (staging) and `BLG-OPS-99` (X-API-Key).

**Scope**
- A database role limited to `SELECT` on aggregate views (linked-plan count, closed-trade count)
- Injected via environment only; never committed; rotation per `api_key_rotation_policy.md`

**Acceptance Criteria**
- Role exists with no access beyond the named views
- A governed routine can read the gate counts without any credential in git

---

### BLG-SEC-38 — CI guard rejecting non-registry dependency specifiers (git+ssh, git+https, file:)
**Priority:** P4 (Trivial)
**Type:** Security / Supply Chain
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`BLG-TECH-18`'s production-build regression came from a git+ssh dependency. `package.json` and `requirements` carry no non-registry specifier today (checked 2026-09-19), so this is preventive only — hence P4.

**Scope**
- CI step failing on non-registry specifiers with an allow-list requiring justification

**Acceptance Criteria**
- A test PR adding a `git+ssh` dependency fails CI

---

### BLG-SPEC-157 — Read-only live-schema vs `data_model.md` drift detector
**Priority:** P3 (Low)
**Type:** Spec Debt / Tooling
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** M (~2d)
**Provisional-Target:** TBD

**Problem**
v9.5 found five live-vs-spec divergences by hand (`BLG-SPEC-148`/`149`/`150`/`151`/`154`: missing index, orphaned columns, nullable mismatch, undocumented CHECK).

**Scope**
- Script comparing live columns, indexes and constraints with `data_model.md`
- Runs read-only wherever `DATABASE_URL` is available

**Acceptance Criteria**
- The five known divergences are reproduced by the tool
- Output lists undocumented and missing objects

---

### BLG-SPEC-158 — Responsive-table behaviour spec for Positions, TradeHistory and TradePlans
**Priority:** P3 (Low)
**Type:** Frontend Spec
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5–1d)
**Provisional-Target:** TBD

**Problem**
No spec states table behaviour below 768px (column priority, scroll vs card).

**Scope**
- Spec each table's narrow-width behaviour

**Acceptance Criteria**
- Three tables have stated behaviour in the frontend specs

---

### BLG-SPEC-159 — Canonical keyboard-shortcut inventory spec
**Priority:** P4 (Trivial)
**Type:** Frontend Spec
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260919-02 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
Keyboard-event handling appears in `Layout`, `TradeEntry`, `TradePlan`, `RedFlagJournal` and `TickerUniverse`; the overlap scan found no single inventory (`BLG-FE-19` shipped the shortcuts).

**Scope**
- Inventory every shortcut; flag conflicts

**Acceptance Criteria**
- One inventory; conflicts resolved or filed

---

### BLG-SPEC-160 — PO-05 (Lightweight Replay Mode) §13 determinism pre-clearance review, standalone
**Priority:** P2 (Medium)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260919-01 — Promoted-Backlog, idea intake IW-20260919-01, roadmap rebalance 2026-09-19__scheduled
**Effort:** XS (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`BLG-FEAT-74` (P1, "highest-value long-term validation feature") is blocked only because its §13 determinism pre-clearance was never run — that review is small; the build is >2 weeks. Extracting it as its own item makes `BLG-FEAT-74` either genuinely ungated-ready or cleanly rejected, and is the only route to a further qualifying U-candidate for the Skill-Silo clause. Analogue of `BLG-SPEC-156` (PO-04).

**Scope**
- Confirm the feature is a deterministic replay of the operator's own history, not predictive simulation (precedent: PS-03 Monte Carlo framing; IT-06's four binding conditions)
- Record the determination in a decisions document and update `BLG-FEAT-74`'s gate line

**Acceptance Criteria**
- A dated §13 determination exists
- `BLG-FEAT-74`'s gate line reflects the outcome

---

### BLG-SPEC-161 — screener_results.md column list omits the Earnings column that the shipped table has
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-03/EPIC-01/2026-09-21__release-v9.6 (BLG-FEAT-97) — found while building the CSV export; `screener_results.md` §4/§5.3 list nine columns but the rendered table has ten — 2026-09-21
**Effort:** XS (<1h)
**Provisional-Target:** v9.7

**Problem**
The Screener results table renders an "Earnings" column (`lg`-visible, days until next earnings), but `screener_results.md` §4 never documents it and the v1.7 §5.3 CSV column list ("Ticker, Market, Price, ATR, Regime, Signal, Sector, Entry Zone, News") omits it. ST-03 exported it anyway, following the AC "columns equal the visible columns", so the spec now disagrees with shipped behaviour.

**Scope**
- Document the Earnings column in §4 (source, format, responsive rule) and add it to the §5.3 export column list
- Bump the spec version and changelog

**Acceptance Criteria**
- `screener_results.md` §4 and §5.3 name all ten columns in display order
- The §5.3 list matches `SCREENER_COLUMNS` in `src/pages/Screener.js`

---

### BLG-SPEC-162 — trade_reflection.md §4 specifies an en dash for a missing R-multiple; the convention is an em dash
**Priority:** P4 (Backlog)
**Type:** Spec Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-06/EPIC-01/2026-09-21__release-v9.6 (BLG-FE-182) — known discrepancy recorded in `number-format-convention/decision_record.md` §2.7 and left for a follow-up — 2026-09-21
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`design_system.md` v1.21 §Number and Currency Formatting defines a missing value as an em dash (U+2014). `trade_reflection.md` §4 (Canonical, v0.2) still specifies an en dash for a missing R-multiple, so the reflection modal cannot both conform to its own spec and to the shared convention.

**Scope**
- Decide which wins (expected: the shared convention), update `trade_reflection.md` §4, and align `TradeReflectionModal.js` to use `src/lib/format.js`

**Acceptance Criteria**
- Spec and modal agree on the missing-value glyph
- The modal's R-multiple, P&L and price fields format via the shared helper

---

### BLG-FE-184 — Migrate the remaining toFixed / toLocaleString call sites to the shared formatting helper
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Source:** ST-06/EPIC-01/2026-09-21__release-v9.6 (BLG-FE-182) — the design record scopes the migration to Positions, Trade History and Trade Plans and lists the rest as follow-ups — 2026-09-21
**Effort:** L (~3-5d)
**Provisional-Target:** TBD

**Problem**
`src/lib/format.js` now implements the canonical formats, but ~60 other files under `src/` still format money, percentages and R-multiples ad hoc (`toFixed(`, `toLocaleString`, `Intl.NumberFormat`), so identical values still render differently across pages. Zero P&L also still takes the >= 0 (green) tone at existing call sites rather than the neutral tone the convention specifies.

**Scope**
- Inventory the remaining call sites (`grep -rn "toFixed(\|toLocaleString\|Intl.NumberFormat" src`) and migrate in page-sized batches, updating affected Playwright assertions in the same commit
- Apply the neutral tone for zero P&L where P&L is coloured
- Add a lint/CI check that fails on new ad hoc money formatting in components
- Harden `src/lib/format.js` (DoQ review note): reject non-number inputs such as booleans (`formatCurrency(true)` currently returns `£1.00`) and treat an unknown currency code as an error rather than silently falling back to `£`

**Acceptance Criteria**
- 0 unmigrated money/percentage/R formatting call sites outside `src/lib/format.js` (or an explicit, reasoned allow-list)
- Zero P&L renders unsigned in the neutral tone wherever P&L is coloured

---

### BLG-FE-185 — Drive Screener and Watchlist table body cells from the shared column definitions
**Priority:** P4 (Backlog)
**Type:** Frontend / UX
**Owner:** Head of Engineering; Head of UX & Design
**Source:** ST-03/EPIC-01/2026-09-21__release-v9.6 (BLG-FEAT-97) — the design record asks for one `{header, value}` array consumed by both the table renderer and the CSV builder; the shipped arrays drive the header and the CSV but not the cell JSX — 2026-09-21
**Effort:** M (~1-2d)
**Provisional-Target:** TBD

**Problem**
`SCREENER_COLUMNS` and `WATCHLIST_COLUMNS` are the single source for the header row and the CSV, but each table's body cells are still hand-written JSX. A future column can therefore be added to the JSX and the header without a matching CSV `value` (or the reverse); only the header/CSV pairing is protected by construction today.

**Scope**
- Add a `cell` renderer to each column definition and render body rows from the array
- Keep responsive hiding, badges and row actions unchanged
- Consider extending the CSV formula-injection guard to a leading TAB or CR, which OWASP also lists (DoQ review note; the sealed ST-03 record specifies only `= + - @`, so this needs a design-record amendment)

**Acceptance Criteria**
- Header, cell and CSV value for every data column come from one definition
- Existing Screener/Watchlist Playwright specs pass unchanged

---

### BLG-OPS-168 — Post-deploy staging verification of the reflection-reminder migration and SQL (never run against a live database)
**Priority:** P2 (Medium)
**Type:** Operations
**Owner:** Infrastructure & Operations Owner; Data Model & Domain Schema Owner; Product Owner
**Source:** ST-04/EPIC-01/2026-09-21__release-v9.6 (BLG-FEAT-98) — the sandbox had no database access (SBX-NO-LIVE-DB), so the new SQL was only asserted with mocked cursors — 2026-09-21
**Effort:** XS (<1h)
**Provisional-Target:** v9.6

**Problem**
The reflection-reminder work adds startup DDL (two `alert_type` CHECK extensions and a partial unique index) and an evaluation query using `ON CONFLICT ((context->>'trade_id')) WHERE ...`. It is covered by structural mocked-cursor tests only; no statement has been executed against PostgreSQL. A typo in any of it would surface at the first startup or evaluation run after deploy.

**Scope**
- After the v9.6 staging deploy, run the verification queries in `data_model.md` DS-19 and confirm the reminder step creates one row per eligible trade and none on a second `POST /alerts/evaluate`
- Product Owner to confirm or change the 30-day look-back (`REFLECTION_REMINDER_LOOKBACK_DAYS`) and the `trade_history.created_at` close-timestamp choice, which the design record left open

**Acceptance Criteria**
- Both CHECK constraints and `uq_notifications_reflection_reminder_trade` are confirmed present on staging, with evidence recorded
- A second evaluation run creates 0 duplicate reminders
- The look-back and close-timestamp decisions are recorded

---

### BLG-QA-188 — The backend test suite can connect to a real database when DATABASE_URL is set to one
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner; Infrastructure & Operations Owner
**Source:** ST-04/EPIC-01/2026-09-21__release-v9.6 — found when running the backend suite in a session whose environment had a `DATABASE_URL` for the staging Supabase database (user-confirmed; credential believed read-only, unverified) — 2026-09-21
**Effort:** S (~0.5d)
**Provisional-Target:** v9.7

**Problem**
`tests/conftest.py` only sets a dummy `DATABASE_URL` when none is set, and `tests/test_schema.py` skips only when the URL contains `stub`. With a real URL in the environment the suite opens real connections and attempts `CREATE TABLE IF NOT EXISTS` / `ALTER TABLE` statements against it (they would alter staging if the credential can write; if it is read-only the suite would instead fail noisily); `CLAUDE.md` §9 tells contributors to run pytest via the virtualenv without warning about this. The safe invocation (`DATABASE_URL=postgresql://stub:stub@localhost:5432/stub`) is nowhere documented.

**Scope**
- Make `conftest.py` refuse (or override to a stub) any non-stub `DATABASE_URL` unless an explicit opt-in variable is set for Phase B CI
- Document the safe invocation next to `CLAUDE.md` §9 (governance file: route via Head of Specs Team)

**Acceptance Criteria**
- Running `backend/.venv/bin/python3 -m pytest tests/` with a real-looking `DATABASE_URL` and no opt-in makes zero real connections
- Phase B CI still runs `tests/test_schema.py` against its real Postgres with the opt-in set

---

### BLG-QA-189 — Real-Postgres integration test for the reflection-reminder evaluation step
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner; Backend Engineering Patterns Owner
**Source:** ST-04/EPIC-01/2026-09-21__release-v9.6 — DoQ agent-mediated review finding: the 48h trigger, one-reminder-ever rule and CHECK/index migration are covered in-repo by mocked-cursor tests only; the reviewer verified them once against a throwaway Postgres 18 by hand — 2026-09-21
**Effort:** S (~0.5-1d)
**Provisional-Target:** v9.7

**Problem**
`tests/test_reflection_reminder.py` asserts SQL text and parameters but never executes them. The behaviour that matters (eligibility windows, `ON CONFLICT` on the partial unique index, savepoint isolation, the settled-when-preference-off rows) was checked only by a one-off manual run. CI Phase B already provides a real Postgres service, so this can be an ordinary test.

**Scope**
- Add a Phase-B-only test that runs `ensure_alerts_tables()` from a pre-v9.6 schema and then `_evaluate_reflection_reminders` against seeded trades (47h/49h/72h, 29/31 days, reflected, back-dated `exit_date`, other portfolio), asserting idempotence and that rows created with the preference off are not re-delivered when it is later turned on
- Skip when `DATABASE_URL` contains `stub` (Phase A), matching `tests/test_schema.py`

**Acceptance Criteria**
- The test runs in Phase B CI and fails if the partial-index conflict target or an eligibility clause is broken
- Phase A remains fully mocked

---

## Release Slice — v9.6 (ephemeral — remove at next `groom backlog` per Placement Rule)

<!-- release-plan-marker: RP:v9.6:2026-09-21__release-v9.6 -->

32 items selected into `2026-09-21__release-v9.6` scope (28.00 estimated days, full capacity). Full acceptance criteria: `claude/cycles/2026-09-21__release-v9.6/stage4_backlog_slice.md`. Selection method: P1-then-P2-first (0 ready P1; all 8 ready P2), then category-balanced round-robin oldest-first for the remaining P3/P4, from a 76-item / 61.75-day ready pool — per `release_planning_prompt.md` §1.4c. Excluded as already complete or already satisfied: `BLG-GOV-335`, `BLG-GOV-336`, `BLG-GOV-337`, `BLG-GOV-326` (archive at next groom).

| ST-ID | Item | EPIC |
|-------|------|------|
| ST-01 | BLG-FEAT-96 | EPIC-01 |
| ST-02 | BLG-FE-180 | EPIC-01 |
| ST-03 | BLG-FEAT-97 | EPIC-01 |
| ST-04 | BLG-FEAT-98 | EPIC-01 |
| ST-05 | BLG-FE-181 | EPIC-01 |
| ST-06 | BLG-FE-182 | EPIC-01 |
| ST-07 | BLG-FR-04 | EPIC-02 |
| ST-08 | BLG-FR-05 | EPIC-02 |
| ST-09 | BLG-BE-119 | EPIC-03 |
| ST-10 | BLG-BE-118 | EPIC-03 |
| ST-11 | BLG-BE-120 | EPIC-03 |
| ST-12 | BLG-BE-121 | EPIC-03 |
| ST-13 | BLG-BE-122 | EPIC-03 |
| ST-14 | BLG-OPS-166 | EPIC-04 |
| ST-15 | BLG-OPS-163 | EPIC-04 |
| ST-16 | BLG-OPS-164 | EPIC-04 |
| ST-17 | BLG-OPS-165 | EPIC-04 |
| ST-18 | BLG-QA-171 | EPIC-05 |
| ST-19 | BLG-QA-172 | EPIC-05 |
| ST-20 | BLG-QA-173 | EPIC-05 |
| ST-21 | BLG-QA-178 | EPIC-05 |
| ST-22 | BLG-SPEC-148 | EPIC-06 |
| ST-23 | BLG-SPEC-160 | EPIC-06 |
| ST-24 | BLG-SPEC-144 | EPIC-06 |
| ST-25 | BLG-SPEC-145 | EPIC-06 |
| ST-26 | BLG-SPEC-146 | EPIC-06 |
| ST-27 | BLG-GOV-345 | EPIC-07 |
| ST-28 | BLG-GOV-329 | EPIC-07 |
| ST-29 | BLG-GOV-328 | EPIC-07 |
| ST-30 | BLG-GOV-325 | EPIC-07 |
| ST-31 | BLG-GOV-90 | EPIC-07 |
| ST-32 | BLG-GOV-188 | EPIC-07 |

