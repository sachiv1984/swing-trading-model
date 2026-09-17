# Product Backlog — Momentum Trading Assistant

<!-- last-spec-debt-deep-review: 2026-09-14__release-v9.4 -->

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-09-17 (session — 1 new item added: `BLG-GOV-334` (correction mechanism for qa_evidence_EPIC-03.md's stale test-count claim, filed per Head of Specs Team ruling resolving ST-21/EPIC-03's sealed-artefact block)); prior — 2026-09-16 (session — 2 new items added: `BLG-BE-120`, `BLG-QA-179` (PR #1712 review findings — JsonLinesFormatter message-truncation gap and missing end-to-end JSON-log test)); prior — 2026-09-16 (session — 1 new item added: `BLG-BE-119` (calculate_trailing_stop's entry-price floor diverges from strategy_rules.md §7.2/§7.3 and the backtest tool)); prior history retained — see prior entries in version control.
**Last rebalance:** 2026-07-12 (cycle 2026-07-12__scheduled — DL-064; 36 new backlog items added (BLG-GOV-203–217, BLG-QA-94–99/101–103, BLG-BE-57/58, BLG-FE-103–105, BLG-SEC-17, BLG-SPEC-78–82, BLG-OPS-106/107) via idea intake IW-20260712-01 (44 submissions, 22 agents) disposition: 36 Promoted-Backlog, 7 Rejected (all resolved by direct action), 1 Promoted-Added (process patch), 2 Parked; 0 active initiatives, CPS=N/A; STEP 2.4 Product Value Ratio 0.21 (U=8 G=9 D=21 P=0, window v6.5–v6.9) — 🔴 3rd consecutive Product Value Alert, improved from prior 0.18 but still below 0.30 floor; mandatory pull-forward named BLG-FE-102 as anchor candidate for next `plan release`, BLG-FE-97 secondary; SI-02 gate live re-checked via production API — NOT MET (0/11 linked trade plans; behavioural-drift endpoint self-reports insufficient_data); STEP 7.1 Skill-Silo rolling-3-cycle avg 76.9% (v6.7/v6.8/v6.9) — Alert persists but improved from 78.2%; STEP 8.1 empty horizon gate: Option (b) — defer, scoping deferred to next `plan release`; Backlog Accessibility Warning RE-TRIGGERED (A=19.9%, down from 38.8%); prior — 2026-07-10 (cycle 2026-07-10__scheduled — DL-063; 39 new backlog items added (BLG-GOV-191–202, BLG-QA-87–93, BLG-OPS-101–105, BLG-SEC-14–16, BLG-BE-53–56, BLG-SPEC-74–77, BLG-FE-99–101, BLG-FEAT-72) via idea intake IW-20260710-01 (44 submissions, 22 agents) disposition: 39 Promoted-Backlog, 3 Parked-cycle-1, 2 Rejected; 0 active initiatives, CPS=N/A; STEP 2.4 Product Value Ratio 0.18 (U=9 G=16 D=24 P=0, window v6.4–v6.8) — 🔴 2nd consecutive Product Value Alert, worse than prior 0.26; mandatory pull-forward named BLG-FEAT-64 as anchor candidate for `plan release v6.9`; STEP 7.1 Skill-Silo rolling-3-cycle avg 78.2% (v6.6/v6.7/v6.8) — Alert persists, single-reading worsening after 2 consecutive improvements; STEP 8.1 empty horizon gate: Option (b) — defer, v6.9 scoping deferred to `plan release v6.9`; prior — 2026-07-02 (cycle 2026-07-02__scheduled — DL-059; 24 new backlog items added (BLG-FEAT-55–60, BLG-FE-81–84, BLG-BE-41/42, BLG-GOV-154/156, BLG-QA-69/70/71, BLG-SEC-09, BLG-SPEC-62/63/65/66, BLG-OPS-84/85) via idea intake IW-20260702-01 (44 submissions) + 19 carried ideas at 3-cycle hard cap; STEP 8.0: 0 fast-track items this cycle; STEP 3.1 Actionable Backlog Assessment: A=35/28%, T=7/6%, D=27/22%, L=55/44% of 124 baseline items — Backlog Accessibility Warning triggered (A% below 30% floor); PVR=0.344 Advisory; Skill-Silo rolling-3-cycle avg=64.8% Alert, worse than prior 53.2% (pull-forward candidate BLG-FE-46)))

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

### BLG-SPEC-133 — position_endpoints.md example JSON: current_trailing_stop_native doesn't reconcile with current_trailing_stop × live_fx_rate

**Priority:** P4 (Trivial)
**Type:** Specification / Documentation Accuracy
**Owner:** API Contracts & Documentation Owner
**Source:** PR #1452 review (Director of Quality agent-mediated review, 2026-08-18) — `docs/specs/api_contracts/position_endpoints.md`'s `GET /positions` example response block shows `current_trailing_stop: 560.50`, `live_fx_rate: 1.3650`, and `current_trailing_stop_native: 764.00` in the same object; `560.50 × 1.3650 = 765.08`, not `764.00` (off by ~£1.08 / 0.14%), so the example doesn't reconcile with the documented conversion formula for the two fields.
**Effort:** XS (~15min)
**Provisional-Target:** Unscheduled

**Problem**
Purely an illustrative-example inconsistency (not test-enforced, no functional impact — the live conversion in `backend/services/position_service.py` is correct and covered by `tests/test_position_currency_basis.py`), but a reader manually verifying the field notes against the example would hit an arithmetic mismatch.

**Scope**
- Correct the example JSON's `current_trailing_stop_native` value (or its `current_trailing_stop`/`live_fx_rate` counterparts) so all three reconcile exactly

**Acceptance Criteria**
- Example JSON block in `docs/specs/api_contracts/position_endpoints.md` is internally consistent (`current_trailing_stop × live_fx_rate == current_trailing_stop_native`, within rounding)
- API Contracts & Documentation Owner sign-off (or Head of Specs Team, per standard doc-fix delegation)

---

### BLG-QA-165 — Extract governance_sync.yml's embedded bash logic into a shared, sourced script

**Priority:** P3 (Low)
**Type:** QA / CI
**Owner:** QA & Testing Owner
**Source:** Agent-mediated Director of Quality review of PR #1598 (EPIC-03, cycle 2026-09-07__release-v9.2) — 2026-09-08
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
`.github/workflows/governance_sync.yml` embeds two pieces of logic directly in its YAML `run:` blocks — the diff-based newly-done detection (Parse Commits for Governance step) and the `is_story_done()` close-gate check (Update State and Close Issues step). Both now have dedicated regression tests (`scripts/test_governance_sync_diff_logic.sh`, `scripts/test_governance_sync_close_gate_logic.sh`, added v9.1 ST-19/`BLG-GOV-314` and v9.2 ST-09/`BLG-QA-159` respectively), but each test script works by hand-maintaining its own copy of the corresponding bash function, with a comment asking a future editor to keep it in sync manually. A future edit to the workflow's embedded logic with no matching edit to the test script's copy would leave the tests silently validating stale logic while still reporting green — the tests would give false confidence exactly when they're most needed (right after a change to the logic they cover).

**Scope**
- Extract `governance_sync.yml`'s two embedded bash functions (the newly-done diff detection, and `is_story_done()`) into a shared script (or two) under `scripts/`, parameterised the same way the current test copies already are (e.g. accepting a base directory / ref pair rather than hardcoding paths)
- Update `governance_sync.yml` to source/call the extracted script(s) instead of embedding the logic inline
- Update both existing test scripts (`test_governance_sync_diff_logic.sh`, `test_governance_sync_close_gate_logic.sh`) to source the same extracted script(s) rather than maintaining their own copies, so a future logic change and its test are structurally the same code

**Acceptance Criteria**
- `governance_sync.yml`'s diff-detection and close-gate logic each live in exactly one place (a sourced script), not duplicated between the workflow and its tests
- Both existing regression test scripts still pass, now by exercising the real extracted functions rather than hand-maintained copies
- QA & Testing Owner sign-off

---

### BLG-GOV-316 — Wire the wall-clock cost logging convention (§22) into an engine's STEP list

**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Agent-mediated DoQ + Product Owner review of PR #1599 (EPIC-04, v9.2) — 2026-09-08
**Effort:** XS (<1h)
**Provisional-Target:** v9.3

**Problem**
`shared_standards.md` §22 (Governance-Cycle Wall-Clock Cost Logging Convention) declares that every governed routine should capture `Session start (UTC)`/`Session end (UTC)` timestamps in its `run_manifest.md`/`cycle_record.md`, but no engine's STEP list was actually patched to do so — grepped every `claude/system/*_prompt.md` for the field names, zero hits outside the standard itself. §22's own AC ("applied from the next cycle onward") cannot happen until some engine's STEP list references it.

**Scope**
- Patch `roadmap_prompt.md` STEP 1.1 (or each engine's own manifest-equivalent STEP) to capture and record `Session start (UTC)` at first write and `Session end (UTC)` at final write, per §22's own derivation rules

**Acceptance Criteria**
- At least one engine's STEP list explicitly instructs capturing `Session start (UTC)`/`Session end (UTC)`
- A real session record demonstrates the convention in use

---

### BLG-SPEC-139 — Triage contract example-payload freshness check findings

**Priority:** P3 (Low)
**Type:** Spec / Documentation Debt
**Owner:** API Contracts & Documentation Owner
**Source:** ST-44 (EPIC-05, v9.2, BLG-SPEC-120) — 2026-09-08
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
ST-44 added `scripts/check_contract_example_freshness.py`, a structural drift detector comparing `docs/specs/api_contracts/*.md` response examples against the `docs/reference/openapi.yaml` schema for the same method+path. Its first baseline run (`docs/ops/contract_example_freshness_baseline_2026-09-08.md`) flagged 37 examples as POSSIBLE DRIFT and 3 as SKIPPED. None of these have been individually triaged yet — some are likely genuine example/schema drift, others are likely artifacts of the script's own nested-array depth-resolution limit (documented in the baseline doc §3). Left untriaged, real drift and tooling noise stay indistinguishable.

**Scope**
- Review each of the 37 POSSIBLE DRIFT findings and 3 SKIPPED findings in `docs/ops/contract_example_freshness_baseline_2026-09-08.md`
- For genuine drift: fix the stale contract example or the `openapi.yaml` schema, whichever is wrong
- For script-resolver artifacts: note the specific limitation (and, if cheap, fix the script's depth handling)

**Acceptance Criteria**
- Every one of the 40 baseline findings has a recorded disposition (fixed, or documented as a resolver artifact)
- `python3 scripts/check_contract_example_freshness.py` re-run and its updated finding count recorded
- API Contracts & Documentation Owner sign-off

---

### BLG-SPEC-140 — Make check_orphaned_specs.py path-aware to resolve duplicate-basename blind spots

**Priority:** P3 (Low)
**Type:** Spec Debt / Tooling
**Owner:** Head of Specs Team
**Source:** ST-17 (BLG-SPEC-70, EPIC-04, `2026-09-09__release-v9.3` sprint execution) — 2026-09-10
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Problem**
`scripts/check_orphaned_specs.py` (ST-17, BLG-SPEC-70, v9.3) matches spec references by basename only. `docs/specs/` currently has 2 duplicated basenames (`README.md` in `frontend/` and `api_contracts/`; `red_flag_journal.md` in `frontend/pages/` and `api_contracts/`) — for a duplicated name, a reference to either file clears both from the orphan scan, so a genuinely-orphaned file sharing a name with a well-referenced one would go undetected. See `docs/specs/orphaned_spec_scan_20260910.md` for the full disclosure from this story's initial run (0 orphans found; both current duplicate pairs manually spot-checked as non-orphans, so this is a latent blind spot, not a known-missed finding today).

**Scope**
- Extend the detector to resolve references by full relative path where the reference text includes a directory prefix (a common but not universal pattern in this codebase — many existing references cite bare filenames without a path)
- For a duplicated basename referenced only by bare filename (no path), fall back to today's basename-only behaviour (conservative — clears both) but flag the ambiguity explicitly in the output rather than silently clearing both
- Add a `--duplicates` flag or section to the output listing all duplicate-basename pairs found, independent of whether either is flagged as orphaned

**Acceptance Criteria**
- Detector distinguishes path-qualified references to same-named files in different directories
- A duplicate-basename pair with only one member referenced (unambiguous path-qualified reference) correctly flags the other as orphaned
- Existing 10 unit tests in `tests/test_check_orphaned_specs.py` still pass; new tests added for path-aware resolution and the ambiguity-flagging fallback

---

### BLG-OPS-153 — AI audit log cost-monitoring follow-ons: storage projection, per-feature trend, silent-purge-failure visibility

**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** Agent-mediated FinOps & Resource Architect review of ST-13/ST-14 (EPIC-03, `2026-09-09__release-v9.3`) — 2026-09-10
**Effort:** M (~2 days, 3 small sub-items)
**Provisional-Target:** Unscheduled

**Problem**
ST-13 (BLG-OPS-94, retention policy) and ST-14 (BLG-OPS-96, per-feature cost breakdown) both met their acceptance criteria, but the agent-mediated FinOps & Resource Architect review identified 3 related, non-blocking gaps worth tracking as deliberate follow-ons rather than left implicit:
1. `docs/ops/ai_audit_log_retention_policy.md`'s 730-day window for `claude_audit_log` is qualitatively justified but carries no estimated row-count/storage-size projection at current call volume.
2. `GET /ai/monthly-cost-by-feature` (current month only) and `GET /ai/spend-trend` (overall total, last 6 cycles) don't combine into a per-feature trend-over-time view — there's no way to see "is feature X's spend trending up" without manually cross-referencing both endpoints across cycles.
3. `POST /ops/purge-audit-logs` and its underlying purge functions fail safe (return `0` rather than raise on error) — good defensive design against breaking the daily scheduled job, but it also means a silently-broken purge (e.g. a credentials issue on the cron step) produces no error signal; deletions would stay at 0 indefinitely with nothing to notice beyond manually checking workflow run logs.

**Scope**
- Add a rough row-count/storage-size projection to `ai_audit_log_retention_policy.md` at current observed call volume
- Add a per-feature spend-trend view (combining `monthly-cost-by-feature`'s grouping with `spend-trend`'s multi-cycle window), and consider tying it to `gemini_cost_tracking.md`'s existing (currently manual-check-only) $5/month alert threshold
- Add a lightweight signal (log line or similar) if `claude_audit_log_rows_deleted`/`gemini_audit_log_rows_deleted` stays at 0 for an implausibly long stretch given known accumulation, to surface a silently-broken purge

**Acceptance Criteria**
- All 3 sub-items addressed (or explicitly re-scoped/split into separate items at grooming time)
- FinOps & Resource Architect sign-off

---

### BLG-QA-166 — Add unit test coverage for check_contract_example_freshness.py

**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Agent-mediated Director of Quality review of PR #1600 (EPIC-05, v9.2) — 2026-09-08
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
`scripts/check_contract_example_freshness.py` (ST-44, EPIC-05, v9.2) was run once manually to produce its baseline doc (`docs/ops/contract_example_freshness_baseline_2026-09-08.md`), but nothing pins its `$ref`-resolution or envelope-unwrapping comparison logic going forward — unlike its sibling tool `check_specs_index_freshness.py`, which received dedicated pytest coverage (`tests/test_check_specs_index_freshness.py`) the same sprint it was added (EPIC-03 ST-11, v9.2). A future edit to the script could silently break its detection logic with no test to catch it.

**Scope**
- Add pytest coverage for `scripts/check_contract_example_freshness.py`, mirroring `test_check_specs_index_freshness.py`'s shape
- Cover: `$ref` resolution (including `allOf`/nested schemas), the envelope-unwrapping comparison logic (`data.foo` vs. bare `foo`), and at least one known-good and one known-drift fixture

**Acceptance Criteria**
- New test file exists and passes
- QA & Testing Owner sign-off

---

### BLG-QA-167 — Playwright coverage matrix file-inventory count is stale (39 vs actual ~100+ spec files)

**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner; Director of Quality
**Source:** ST-05 (BLG-QA-82, EPIC-02, v9.3 sprint execution) — 2026-09-09
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Problem**
`docs/qa/playwright_coverage_matrix.md`'s "Total: 39 spec files" line (Last Updated 2026-07-20) is far behind the actual `tests/e2e/` directory count (102 as of 2026-09-09). Discovered while consolidating the 3 overlapping SignalCard specs into `tests/e2e/signal-card.spec.js` (ST-05) — updating that one row highlighted that the doc's running total and per-file table have not kept pace with the many spec files added since v4.8. A full re-inventory is out of scope for ST-05, which only touches the SignalCard rows.

**Scope**
- Full re-scan of `tests/e2e/*.spec.js` against the matrix's per-file table
- Add missing rows, remove stale ones (including reconciling the ST-05 SignalCard consolidation once it lands)
- Correct the running total

**Acceptance Criteria**
- Per-file table matches the actual `tests/e2e/` directory contents
- Running total corrected
- Doc Version/Last Updated bumped per the doc's own convention

---

### BLG-GOV-318 — Codify whether opportunistic in-file fixes found mid-story need their own backlog entry

**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** Agent-mediated Product Owner review of PR #1600 (EPIC-05, v9.2) — 2026-09-08
**Effort:** XS (<1h)
**Provisional-Target:** Unscheduled

**Problem**
`CLAUDE.md` §7 explicitly allows filing a *new* backlog item for a genuinely out-of-scope finding discovered mid-sprint, but says nothing about the case where the engine instead fixes a small incidental defect directly in a file it is already editing for an unrelated story. PR #1600 did this twice — a duplicate "Appendix D" heading collision in `metrics_definitions.md` (found while executing ST-48) and a stale `execution_state.json` field left by an unrelated, already-merged EPIC — both currently disclosed only via commit message, with no documented rule on when that is sufficient versus when the fix should get its own backlog entry first.

**Scope**
- Define the rule: backlog entry always required / commit-message disclosure sufficient / a size-or-risk-based threshold distinguishing the two
- Record the rule in `CLAUDE.md` §7 or `shared_standards.md` (whichever this repo's existing convention for this kind of process rule prefers)

**Acceptance Criteria**
- Rule documented in a governance source file
- Product Owner sign-off

---

### BLG-GOV-319 — record-visual-qa skill's documented output format has drifted ~5 months from actual staging sign-off practice

**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Director of Quality; QA & Testing Owner
**Source:** ST-07 (BLG-QA-88, EPIC-02, v9.3 sprint execution — DoQ sign-off template freshness check) — 2026-09-09
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Problem**
`.claude/skills/record-visual-qa/SKILL.md` documents a structured output format for recording staging visual QA results (a `**Visual AC — Staging results**` table plus a `**Visual sign-off status:**` line in the QA evidence file). This format appears in only 2 `qa_evidence_EPIC-*.md` entries across the entire cycle history, both from `2026-03-24__release-v2.3`/`2026-04-11__release-v2.6`. Git history confirms only 3 actual invocations of the skill, the most recent on 2026-04-12 (`2307c91d`) — roughly 5 months before this review. Every staging sign-off recorded since then instead uses free-form prose directly in the DoQ sign-off block's `Comments:` field or an ad hoc `Staging sign-off:`/`Staging confirmation:` line (see `docs/testing/doq_signoff_template_freshness_review_20260909.md` for sampled examples). The freeform format is functionally valid — it satisfies CLAUDE.md's frontend testing gate — but the skill has not been the actual mechanism producing it for a long time, and its documented format no longer matches what "current staging sign-off practice" looks like.

**Scope**
- Determine whether the skill's structured-table format should be updated to match the freeform practice that has actually been used for ~5 months, or whether the freeform practice should be reined back in favour of the skill's structured format (a real design decision, not a mechanical sync)
- Update `.claude/skills/record-visual-qa/SKILL.md` accordingly, or formally deprecate/narrow it if freeform is the accepted path going forward
- Consider whether the skill's assumption of a pre-authored `docs/testing/staging_visual_test_script_ST-xx.md` file with named check IDs is still a good fit for how staging sign-offs are actually being requested/performed today (single ad hoc confirmations, not always against a pre-written check list)

**Acceptance Criteria**
- Skill documentation matches actual current staging sign-off practice, confirmed against a sample of recent `qa_evidence_EPIC-*.md` entries
- Director of Quality sign-off on the reconciled approach

---

### BLG-BE-112 — Backend logging output does not conform to structured_logging_standards.md's mandatory JSON Lines format
**Priority:** P3 (Low)
**Type:** Backend / Technical Debt
**Owner:** Backend Engineering Patterns Owner; Head of Engineering
**Source:** Discovered mid-sprint while executing ST-03 (EPIC-01, `2026-09-09__release-v9.3`, correlation-ID logging propagation) — 2026-09-09
**Effort:** M (~2-3 days)
**Provisional-Target:** Unscheduled

**Problem**
`docs/specs/structured_logging_standards.md` (Class 1 Canonical Specification, v0.1.0, Status: Active) mandates that all backend log output be valid JSON Lines (NDJSON) with required top-level fields (`timestamp`, `level`, `correlation_id`, `service`, `message`). The actual backend logging configuration (`backend/main.py`'s `logging.basicConfig`) has only ever emitted plain-text formatted log lines (`"%(asctime)s %(levelname)s %(name)s [%(correlation_id)s]: %(message)s"`), never JSON — a pre-existing spec-vs-implementation gap, not introduced by ST-03. ST-03 itself only added the `correlation_id` value (via a contextvars-based mechanism, documented as a deviation in `structured_logging_standards.md` — see that document's Known Deviations) and does not resolve the wider JSON-format gap, which is out of that story's scope.

**Scope**
- Migrate `backend/main.py`'s logging configuration to emit JSON Lines per `structured_logging_standards.md` §Structured Log Format (or formally revise that spec's Status/requirement if plain-text logging is the accepted long-term choice)
- Confirm the required fields (`timestamp`, `level`, `correlation_id`, `service`, `message`) are present on every emitted record

**Acceptance Criteria**
- Backend log output is valid JSON Lines matching the canonical example in `structured_logging_standards.md`, OR the spec is formally revised to match accepted practice
- No regression to existing log-based monitoring/alerting that depends on the current plain-text format

---

### BLG-BE-113 — Validate limit/offset are non-negative on screener endpoints
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Backend Engineering Patterns Owner
**Source:** Director of Quality agent-mediated review of PR #1629 (EPIC-01, 2026-09-09__release-v9.3) — 2026-09-09
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
`GET /screener/results` and `GET /screener/history` (backend/routers/screener.py) validate that `limit` does not exceed 200, but neither validates that `limit` or `offset` are non-negative. A negative value passed through to the underlying `SELECT ... LIMIT %s OFFSET %s` query raises a Postgres error ("LIMIT must not be negative"), which propagates as an unhandled exception (HTTP 500 with a raw traceback) instead of the clean HTTP 400 this codebase uses for every other invalid-parameter case. Pre-existing gap in the established validation pattern, not introduced by PR #1629 (both endpoints share it; ST-01 simply copied the existing `/screener/results` pattern into the new `/screener/history` endpoint).

**Scope**
- Add `limit < 0` / `offset < 0` checks to both endpoints, returning the existing `INVALID_PARAMS` 400 shape
- Audit other paginated endpoints in the codebase for the same gap

**Acceptance Criteria**
- A negative `limit` or `offset` on either endpoint returns HTTP 400 `INVALID_PARAMS`, not a 500
- Any other paginated endpoint found with the same gap is either fixed or filed as a follow-up item

---

### BLG-QA-168 — ST-09 cross-browser evaluation cites stale pre-sharding CI baseline

**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Agent-mediated Director of Quality review of PR #1630 (EPIC-02, `2026-09-09__release-v9.3`) — 2026-09-10
**Effort:** XS (<1h)
**Provisional-Target:** Unscheduled

**Problem**
`docs/qa/cross_browser_playwright_matrix_evaluation_20260909.md` bases its "~3×" cost extrapolation on `ci_pipeline_baseline.md` §3.1's 2026-05-29 single-sample figure (~133s), taken before 4-way sharding was added (REC-CI-01, actioned 2026-07-28) — the "4 parallel workers" framing attached to that figure is inconsistent with what §3.1 actually measured at that date (workers were still forced to 1). The same source document's own §8.5 (2026-09-08, one day before this PR's cycle date) records the current sharded critical path at 198.5–210.6s, roughly 1.5–1.6× the figure actually used. This does not overturn the evaluation's "defer" recommendation — a higher current baseline strengthens, not weakens, the case against adding 2 more unsharded browsers — but the quantitative estimate underpinning it is built on a stale, superseded number from the same document rather than the correct current one sitting one section later.

**Scope**
- Correct the cost/benefit figure in `cross_browser_playwright_matrix_evaluation_20260909.md` to cite `ci_pipeline_baseline.md` §8.5's current sharded baseline instead of §3.1's pre-sharding figure
- Recompute the cost multiplier and confirm the "defer" recommendation still holds under the corrected figure

**Acceptance Criteria**
- Document cites the current CI baseline, not the superseded pre-sharding one
- QA & Testing Owner sign-off

---

### BLG-QA-169 — ST-05 SignalCard spec consolidation lacks before/after runtime evidence

**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Agent-mediated Product Owner review of PR #1630 (EPIC-02, `2026-09-09__release-v9.3`) — 2026-09-10
**Effort:** XS (<1h)
**Provisional-Target:** Unscheduled

**Problem**
ST-05's acceptance criteria include "suite runtime reduced" following the consolidation of 3 SignalCard Playwright spec files into `tests/e2e/signal-card.spec.js`. Full scenario coverage was independently confirmed retained (1:1 diff against the 3 deleted files), and a runtime reduction is plausible given shared setup and fewer browser-context spins, but no before/after timing number was ever captured anywhere in the PR, `qa_evidence_EPIC-02.md`, or the consolidation doc to substantiate the claim.

**Scope**
- Capture a `time npx playwright test` (or equivalent) before/after comparison, using the pre-consolidation 3-file baseline (recoverable via `git show` on the parent commit) and the current single file
- Record the result in the existing consolidation documentation

**Acceptance Criteria**
- A real before/after runtime number is recorded substantiating (or correcting) the "runtime reduced" claim
- QA & Testing Owner sign-off

---

### BLG-OPS-154 — New `api_call_log` table has no retention/purge policy

**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** Agent-mediated Director of Quality review of PR #1631 (EPIC-03, `2026-09-09__release-v9.3`) — 2026-09-10
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
ST-13 (this same EPIC) defines and wires retention/purge policies for `gemini_audit_log` and `claude_audit_log`, but ST-11/ST-12 (also this EPIC) introduce a new `api_call_log` table (`backend/database.py`) with no retention window, purge function, or scheduled cleanup of its own. Left as-is, it will grow unbounded indefinitely — the exact problem this EPIC exists to fix for the other two tables.

**Scope**
- Define a retention window for `api_call_log` (e.g. mirroring the 730-day window chosen for `claude_audit_log`, or a shorter window appropriate to per-call operational logs)
- Add a purge function and wire it into the existing scheduled purge step (`.github/workflows/daily-snapshot.yml`) alongside the gemini/claude purges

**Acceptance Criteria**
- `api_call_log` has a documented retention window and a scheduled purge function
- Infrastructure & Operations Owner sign-off

---

### BLG-QA-170 — `qa_evidence_EPIC-03.md` test-count claim inaccurate (30 vs. actual 28)

**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Agent-mediated Director of Quality review of PR #1631 (EPIC-03, `2026-09-09__release-v9.3`) — 2026-09-10
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`qa_evidence_EPIC-03.md` and PR #1631's description both state `tests/test_cost_monitoring.py` contains "30 tests" / "30/30 pass". Independently counting `def test_*` functions in the file at the PR head commit finds 28, all passing. Coverage itself is solid (every new DB function, both instrumentation call sites, and all 4 new endpoints have direct tests) — this is a factual inaccuracy in the self-reported count, not a coverage gap, but the QA evidence document is exactly the artifact the STEP 4 merge gate relies on being accurate.

**Scope**
- Correct the test count in `qa_evidence_EPIC-03.md` and, if still editable, the PR description

**Acceptance Criteria**
- Test count in `qa_evidence_EPIC-03.md` matches the actual number of tests in `tests/test_cost_monitoring.py`
- QA & Testing Owner sign-off

---

### BLG-OPS-155 — `get_api_session_report()` anomaly baseline is self-inclusive

**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Source:** Agent-mediated Director of Quality review of PR #1631 (EPIC-03, `2026-09-09__release-v9.3`) — 2026-09-10
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`backend/database.py::get_api_session_report()`'s "&gt;2x baseline" anomaly check (ST-12) computes its baseline as the mean of all sessions' call counts, including any anomalous session(s) themselves — a large outlier inflates the very baseline it is compared against, and two similarly-sized outliers can mask each other (e.g. sessions `[1, 10, 10]` → mean 7, threshold 14, neither 10 flags). This meets the story's literal AC ("&gt;2x baseline" is implemented correctly for the tested case) but is a real methodological limitation for a signal intended to catch genuine cost anomalies.

**Scope**
- Replace the self-inclusive mean baseline with a trimmed mean, median, or leave-one-out baseline
- Add a test case covering the multiple-similarly-sized-outliers scenario

**Acceptance Criteria**
- Anomaly baseline is no longer inflated by the session(s) it is evaluating
- Infrastructure & Operations Owner sign-off

---

### BLG-SPEC-141 — Spec debt dashboard sort key mishandles same-day-filed items

**Priority:** P3 (Low)
**Type:** Spec / Documentation Debt
**Owner:** API Contracts & Documentation Owner
**Source:** Agent-mediated Director of Quality review of PR #1632 (EPIC-04, `2026-09-09__release-v9.3`) — 2026-09-10
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`scripts/generate_spec_debt_dashboard.py`'s sort key uses `-(r["age_days"] or -1)`. Because `0` is falsy in Python, an item filed the same day the dashboard is generated (`age_days == 0`) evaluates identically to the `None` (undated) case, so it would silently sort as if undated rather than as the newest item in its priority tier. Verified via direct interpreter check. No current dashboard row triggers it (no live BLG-SPEC item has age 0 today), and it is not covered by the script's 14-test suite.

**Scope**
- Fix the sort key to distinguish `age_days == 0` from `age_days is None` (e.g. an explicit `-1 if r["age_days"] is None else -r["age_days"]`)
- Add a test case covering `age_days == 0`

**Acceptance Criteria**
- A same-day-filed item sorts as the newest item in its priority tier, not as undated
- API Contracts & Documentation Owner sign-off

---

### BLG-GOV-320 — File a Product Owner decision record for ST-20's trade-tagging "no closed taxonomy" call

**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Product Owner; Head of Specs Team
**Source:** Agent-mediated Product Owner review of PR #1632 (EPIC-04, `2026-09-09__release-v9.3`) — 2026-09-10
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-20's AC reads "canonical allowed-tag taxonomy... documented," which a literal reading suggests a closed vocabulary. The story instead correctly determined (and independently verified as accurate) that `trade_plans.trade_tags` is intentionally free-text/format-constrained by design, and documented that instead of inventing a fake enum. This codebase has an established pattern for exactly this kind of "AC assumed X, accepting Y instead" call — a dedicated `docs/product/decisions/*.md` record (precedent: `setup-type-other-conflation-decision--2026-08-21.md`) — but no equivalent record was filed for ST-20; the reasoning is only documented inline in the new spec doc's Purpose section.

**Scope**
- File a short `docs/product/decisions/*.md` record for the trade-tagging taxonomy-scope reframing, consistent with the existing precedent
- Cross-reference it from `docs/specs/trade_tagging_taxonomy.md`

**Acceptance Criteria**
- Decision record filed and cross-referenced
- Product Owner sign-off

---

### BLG-OPS-156 — Add 1 new endpoint to api_performance_baseline.md re-run

**Priority:** P3 (Low)
**Type:** Operations
**Owner:** Infrastructure & Operations Owner
**Source:** Post-ship closure `2026-09-09__release-v9.3` STEP 6 Endpoint Coverage Drift Check
**Effort:** XS (<1h, plus a live measurement re-run)
**Provisional-Target:** TBD

**Problem**
Comparing `docs/reference/openapi.yaml` (144 normalised method+path endpoints) against `docs/ops/api_performance_baseline.md` (250 normalised entries) after path-parameter and Markdown-formatting normalisation finds 1 genuine gap: `GET /positions/{id}` (the single-position fetch) has no baseline measurement row. The baseline's existing `positions`-prefixed rows cover the list endpoint (`GET /positions`) and several `/positions/{id}/...` sub-resource actions, but not the bare single-position `GET`.

**Scope**
- Add a row for `GET /positions/{id}` to `api_performance_baseline.md`'s measured or pending-measurement table
- Re-run against a live environment to obtain real p50/p95/p99 figures where the measured table is used; if no live access is available, add to the pending-measurement table with the same disclosure convention as the file's other `pending baseline measurement` rows

**Acceptance Criteria**
- `api_performance_baseline.md` has a row for `GET /positions/{id}`
- Infrastructure & Operations Owner sign-off

---

### BLG-FE-175 — Bring the 4 known motion-timing non-compliant components under the 500ms ceiling

**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend Prompt Owner
**Source:** Design gate `2026-09-14__release-v9.4` (ST-13/BLG-SPEC-136) — target release assigned, remediation approach fixed in `docs/design/2026-09-14__release-v9.4/motion-timing-target-release/decision_record.md` and `design_system.md` v1.14 §Accessibility — 2026-09-14
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v9.5

**Problem**
`design_system.md`'s motion-vs-contrast guideline (v1.12+) caps entrance-animation text elements at a combined `delay + duration ≤ 500ms`. Four components are documented as non-compliant, via two distinct failure modes: unbounded/user-editable index-scaled stagger (`src/pages/SystemStatus.js` — `delay: index * 0.02`/`index * 0.05`, no cap; `src/pages/Signals.js` — `delay: index * 0.05` over a list capped via `slice(0, topN)`, but `topN` has no `max`), and fixed stagger values already at/over the ceiling (`src/pages/Reports.js` — four hardcoded per-card delays, `0.05`–`0.2`; `src/components/dashboard/widgets/RecentTradesWidget.js` — `delay: idx * 0.05` over a list capped at 5 items, max delay `0.2s`). The v9.4 design gate fixed a target release (v9.5) and a remediation approach per failure mode but did not implement any fix — this item is that implementation.

**Scope**
- `Reports.js` and `RecentTradesWidget.js`: reduce max per-item `delay` (or shorten `duration`) so `max(delay) + duration ≤ 500ms`, verified against each component's own actual current `duration` value (not assumed at the ~0.3–0.5s Framer Motion default)
- `SystemStatus.js` and `Signals.js`: introduce a fixed stagger cap independent of list length or user-editable bounds (e.g. `delay: Math.min(index, N) * step`, with `N` chosen so the combined total stays under the ceiling) rather than removing staggering outright
- Remove each component from `design_system.md`'s known-non-compliant list in the same commit that fixes it, per that list's existing convention

**Acceptance Criteria**
- All 4 components verified against their own actual current `duration` value and brought to `max(delay) + duration ≤ 500ms`
- Each component removed from `design_system.md`'s known-non-compliant list in the same commit that fixes it
- No visual regression beyond the timing change itself — existing Playwright coverage, if any, still passes

---

### BLG-UX-05 — Arc 5 low-trade-volume advisory: surface the 20-trade threshold and remaining-trades count, reconsider placement above the stat grid
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** ST-26 (EPIC-06, v9.4, BLG-UX-03) usability review — 2026-09-15
**Effort:** XS (<1h)
**Provisional-Target:** v9.5

**Problem**
The Arc 5 Signal Compliance low-trade-volume advisory banner (`docs/specs/frontend/components/arc5_compliance_section.md#Low-Trade-Volume Advisory`, `src/components/analytics/Arc5ComplianceSection.js`) tells the user "treat these figures as indicative until more trade history accumulates" but never states the actual threshold (20 closed trades) or how many more trades the user needs before the figures are considered fully reliable. It also renders below the four stat cards, so the user sees the (potentially low-confidence) numbers before the caveat that qualifies them.

**Scope**
- Consider stating the threshold explicitly and/or a remaining-trades count (e.g. "Based on 5 closed trades — figures become more reliable at 20+ (15 more needed).")
- Consider moving the advisory above the stat grid so the caveat is read before the numbers, not after
- Head of UX & Design to decide whether either change is worth making, or whether the current copy/placement is an acceptable simplicity trade-off

**Acceptance Criteria**
- Placement and copy decision recorded (keep as-is, or specify the change)
- If changed: `arc5_compliance_section.md` updated in the same commit as the implementation, existing Playwright coverage (`tests/e2e/arc5-compliance-section.spec.js`) still passes

---

### BLG-FE-176 — Bring 9 non-conforming toast call sites into line with the Toast Notification Timing standard
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend Prompt Owner
**Source:** ST-27 (EPIC-06, v9.4, BLG-UX-04) non-conforming-screens inventory — 2026-09-15
**Effort:** XS (<1h)
**Provisional-Target:** v9.5

**Problem**
`design_system.md`'s Toast Notification Timing standard (v1.15/v1.17, §Shared UI Components) defines severity-based durations, but ST-27's inventory found 9 non-conforming `toast.*()` call sites across 6 files: 8 `toast.error(...)` calls with no `duration` override (rendering at `sonner`'s 4s default instead of the standard's 8s-or-manual-dismiss for errors) in `Settings.js` (×2), `Signals.js` (×2), `Positions.js` (×2 — stop-update failure and mark-reviewed failure), `PositionCard.js` (×1 — its own copy of the mark-reviewed-failure message), `useWatchlistModal.js` (×1); and 1 `toast.info(...)` call in `Layout.js` with an incorrect explicit duration (8000ms on a <80-char message that should use the 4s info default).

**Scope**
- Add `duration: 8000` (or manual-dismiss per the standard's error-with-required-next-action clause) to the 8 non-conforming `toast.error(...)` calls
- Correct `Layout.js`'s `toast.info(...)` duration from 8000 to the 4s default (remove the override)
- Also fix the pre-existing duplicate "Failed to mark position as reviewed" message noted during the inventory (identical string independently hardcoded in both `Positions.js` and `PositionCard.js`) while touching that call site, if low-risk to do so

**Acceptance Criteria**
- All 9 call sites named in the inventory conform to `design_system.md` v1.17's Toast Notification Timing table
- `design_system.md`'s non-conforming-screens table updated to reflect the fix (or the table removed/marked historical if all sites now conform)
- No visual regression beyond the timing change itself

---

## Idea Intake IW-20260914-01 — Promoted-Backlog Disposition (roadmap rebalance `2026-09-14__scheduled`)

*40 of the window's 44 submissions promoted directly to backlog per STEP 4 "📋 Backlog (gate-conditional)" disposition — no hard gate on any item, all ungated and ready. 2 Challenger submissions resolved as process patches feeding this cycle's STEP 11.4 meta-review (see `lessons_learnt.md`/`meta_review.md`), not filed here. All items carry `**Provisional-Target:** TBD` (Now/Next horizons both empty — §16.6 fallback) and no day-range effort (§16.12 n/a, target not release-specific).*


### BLG-BE-114 — Consolidate duplicated ATR trailing-stop recalculation logic
**Priority:** P3 (Low)
**Type:** Backend / Tech Debt
**Owner:** Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** M
**Provisional-Target:** TBD

**Problem**
ATR trailing-stop recalculation logic is duplicated across 3 call sites (nightly job, on-demand recompute endpoint, and a test helper), risking drift between them if one is updated and the others are not.

**Scope**
- Identify all 3 call sites precisely
- Extract to one shared service function; update all call sites to use it

**Acceptance Criteria**
- Single shared implementation exists; all 3 call sites use it
- Existing trailing-stop tests still pass unchanged

---

### BLG-SPEC-142 — Canonical position/trade lifecycle state diagram
**Priority:** P3 (Low)
**Type:** Documentation / Spec Debt
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** M
**Provisional-Target:** TBD

**Problem**
The position/trade lifecycle (open → managed → closed → journalled) is implicit across `position_service.py`, `trade_plan.md`, and the frontend state machine, with no single canonical diagram a new contributor (human or agent) could read to understand the whole lifecycle.

**Scope**
- Produce one state diagram in `data_model.md` covering the full lifecycle across all 3 current implicit sources
- Cross-reference from each of the 3 sources back to the canonical diagram

**Acceptance Criteria**
- Diagram exists in `data_model.md`
- All 3 source files cross-reference it

---

### BLG-GOV-321 — Lightweight role-retirement process for inactive agent charters
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
No documented process exists for what to do with an agent role charter that has gone 6+ months with no idea-intake submission and no owned story — leave it in `claude/agents/` indefinitely, or formally flag/retire it.

**Scope**
- Define a lightweight review trigger (e.g. checked at each `run ideas housekeeping` or annual review)
- Define outcomes: keep as-is, merge into another role, or formally retire with rationale

**Acceptance Criteria**
- Process documented (likely a short addition to `team_charter.md` or a new §)
- Applied at least once to confirm it runs end to end (may find 0 qualifying roles — that is a valid outcome)

---

### BLG-GOV-322 — Cross-role pairing rotation note in workforce_capacity.md
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
Skill-Silo mitigation (§7.1) currently relies on ad hoc pull-forward candidate naming each cycle rather than any standing rotation guidance for which roles should be favoured next given recent concentration.

**Scope**
- Add a short rotation-guidance note to `workforce_capacity.md`, informed by the §7.1/§7.2 historical readings
- Not a hard rule — advisory input for release planning's scope selection

**Acceptance Criteria**
- Note added and cross-referenced from `roadmap_prompt.md` §7.1's pull-forward step

---

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

### BLG-OPS-157 — Recurring quarterly hosting-cost trend review
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
Hosting-cost trend review has happened ad hoc (see `BLG-OPS-25`/`26` precedent items) rather than on a recurring cadence, risking cost drift going unnoticed between reviews.

**Scope**
- Define a quarterly cadence
- Run the first review under the new cadence

**Acceptance Criteria**
- Cadence documented
- First cadence-driven review completed with results recorded

---

### BLG-GOV-323 — Cost-per-cycle wall-clock rollup in workforce_capacity.md
**Priority:** P3 (Low)
**Type:** Governance / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
The §22 governance-cycle wall-clock cost logging convention produces per-cycle figures, but nothing rolls them up into a trend view across cycles — each figure is only ever read in isolation.

**Scope**
- Add a rollup table to `workforce_capacity.md` aggregating the last 10 cycles' §22 figures
- Define the refresh cadence (likely: updated at each rebalance)

**Acceptance Criteria**
- Rollup table added and populated with available historical figures
- Refresh cadence documented

---

### BLG-SPEC-143 — Consolidate divergent empty-state copy patterns
**Priority:** P3 (Low)
**Type:** Frontend Spec / Consistency
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
`v9.1`'s ST-29 already began consolidating duplicate empty-state pattern specs; this submission confirms 3 divergent copy patterns remain across Dashboard/Screener/Journal specifically (a narrower, still-open remainder of that broader effort).

**Scope**
- Confirm current state post-v9.1-ST-29 (some consolidation may already be done)
- Document one canonical empty-state copy pattern for the 3 named screens if still divergent

**Acceptance Criteria**
- Confirmed status against v9.1 ST-29's prior consolidation recorded
- Canonical pattern documented if a genuine remaining gap is confirmed

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

### BLG-GOV-324 — Formalise the STEP 8.0.5 / STEP 8.2 candidate-verification pattern as one subroutine
**Priority:** P3 (Low)
**Type:** Governance / Prompt Engineering
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
`roadmap_prompt.md` STEP 8.0.5 and STEP 8.2 both independently verify that a candidate BLG-ID is still active/unshipped, with near-duplicated logic and rationale text, rather than one shared subroutine both steps call.

**Scope**
- Extract the shared verification logic into one callable subroutine (matching the pattern already used for `preflight_common.md`/`governance_preamble.md`)
- Update both STEP 8.0.5 and STEP 8.2 to reference it

**Acceptance Criteria**
- Subroutine extracted; version bump + `prompt_change_log.md` entry per the Governance File Edit Checklist
- Both steps reference the shared subroutine with no behavioural change

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

### BLG-OPS-158 — Synthetic uptime monitor for /health independent of hosting dashboard
**Priority:** P3 (Low)
**Type:** Operations
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260914-01 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** S
**Provisional-Target:** TBD

**Problem**
Uptime monitoring currently relies solely on the hosting provider's own dashboard — there is no independent synthetic check that would catch an outage the provider's own monitoring itself misses or is unavailable to report.

**Scope**
- Stand up an external synthetic monitor (free-tier service acceptable at this scale) hitting `/health` on a fixed interval
- Configure a notification path (e.g. email) on failure

**Acceptance Criteria**
- Monitor configured and confirmed firing on a deliberate test failure
- Notification path confirmed working

---

### BLG-OPS-159 — Document the dashboard-only deploy path-filter gotcha in the ops runbook
**Priority:** P3 (Low)
**Type:** Operations / Documentation
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260914-02 — Promoted-Backlog, idea intake IW-20260914-01, roadmap rebalance 2026-09-14__scheduled
**Effort:** XS
**Provisional-Target:** TBD

**Problem**
The hosting provider's dashboard-only deploy path filters are invisible to a repo-only search — a runtime-read file can be changed without triggering a deploy, and nothing in the repo documents this so a future session catches it before, not after, a missed deploy.

**Scope**
- Add a short, explicit note to the ops runbook describing the gotcha and how to check the dashboard-side filter configuration
- Cross-reference from wherever deploy troubleshooting is currently documented

**Acceptance Criteria**
- Note added to the ops runbook
- Cross-referenced from the deploy-troubleshooting doc

---

### BLG-OPS-160 — nightly-stop-update and rebalance-exit appear to have no live scheduled trigger
**Priority:** P1 (High)
**Type:** Operations / Backend Correctness
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** ST-05, EPIC-01, v9.4 (2026-09-14__release-v9.4) — surfaced during the scheduled-job-runner inventory; out of ST-05's own spec-only scope, filed separately per execution_prompt.md §7
**Effort:** S (investigation/confirmation) — remediation effort TBD pending confirmation
**Provisional-Target:** TBD

**Problem**
`docs/specs/qa/scheduler_architecture_review_v6.3.md` (2026-06-29, ST-13/BLG-OPS-79/v6.3) explicitly flagged as a "pre-existing configuration gap" that `POST /positions/nightly-stop-update` (trailing-stop recompute) and `POST /signals/rebalance-exit` (rebalance-exit + inv_vol_sizing signal generation) were "currently absent from `daily-snapshot.yml`" and "must be invoked externally." Re-checked live at ST-05 (v9.4, ~11 weeks later): a repo-wide search for callers of either endpoint (`.github/workflows/*.yml`, `production_strategy.py`, and all backend/scripts sources) found none outside the endpoint definitions themselves and their test files — `daily-snapshot.yml` still does not call either endpoint, and no other workflow file does either. If accurate, trailing stops have not been recalculated, and rebalance-exit/inv_vol_sizing signals have not been generated, by any automated process since before v6.3 — both are risk-management-relevant features that would be silently inert in production.

**Important caveat — verify before treating as confirmed:** this repo has a documented precedent (`render_build_filters_gotcha`, 2026-07-28, `docs/ops/` deploy-filter incident) for scheduling/trigger configuration living Render-dashboard-side only (e.g. a native Render Cron Job), invisible to any repo grep. `RENDER_API_KEY` in this repo is the app's own `X-API-Key`, not a Render platform key, so it cannot be used to query Render's API to check this either. **Do not treat this as a confirmed gap until the Render dashboard's own Cron Jobs / Scheduled Jobs configuration has been checked directly** — if a dashboard-native cron already calls these two endpoints, this item should be closed as a documentation-only fix (update the stale `scheduler_architecture_review_v6.3.md` trigger-mechanism table to record the dashboard-side cron instead of "GitHub Actions (external call)"). If no such dashboard cron exists either, this is a live P0-class correctness gap and should be escalated accordingly.

**Scope**
- Infrastructure & Operations Owner: check the Render dashboard for `trading-assistant-api-c0f9` (or the relevant service) for any native Cron Job calling `/positions/nightly-stop-update` or `/signals/rebalance-exit`
- If none found: wire both into `daily-snapshot.yml` (or a dedicated workflow) on an appropriate schedule, matching the cadence implied by their nature (trailing-stop: daily; rebalance-exit: last trading day of month, per its own endpoint docstring)
- Either way: correct `docs/specs/qa/scheduler_architecture_review_v6.3.md`'s trigger-mechanism table, which is currently stale/inaccurate regardless of which outcome applies
- Cross-check `GET /health/scheduler`'s `trailing_stop`/`rebalance_exit`/`inv_vol_sizing` job entries in production for their actual `last_run` timestamps as a second, independent confirmation signal

**Acceptance Criteria**
- Render dashboard checked and outcome documented (dashboard-cron found, or confirmed absent)
- If absent: both endpoints wired into a live schedule; live confirmation that `GET /health/scheduler` shows a recent `last_run` for all three affected job names
- `scheduler_architecture_review_v6.3.md` corrected to match the confirmed live trigger mechanism

---

### BLG-SPEC-D18 — data_model.md `positions` table (DS-17 addition) not confirmed against live deployed schema
**Priority:** P2 (Medium)
**Type:** Spec Debt / Documentation Drift
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-01, EPIC-01, v9.4 (2026-09-14__release-v9.4) — filed per this role's own charter §8 ("Any divergence between `data_model.md` column definitions and the live deployed schema is a P2 spec debt item... If confirmation cannot be given, a BLG-SPEC-D item must be filed before the dependent work proceeds"), raised during the DS-17 agent-mediated review of ST-01's migration
**Effort:** XS (confirmation only, once DB access is available)
**Provisional-Target:** TBD

**Problem**
DS-17 (`docs/specs/data_model.md`, `positions` unique-constraint migration) was drafted and reviewed with no live database access in this execution environment (RISK-01 — no `DATABASE_URL`). The charter for this role requires the live `positions` schema be confirmed to match the spec before sign-off on a migration/integration test against a domain table; that confirmation could not be given here. This mirrors the existing precedent at `data_model.md` §1 (`portfolios` table's own "Schema verification" note, confirmed 2026-04-02 against actual Supabase output) — `positions` has had no equivalent direct-DB confirmation logged since DS-17 was added.

**Scope**
- When DB access is available, run `CREATE TABLE public.positions` (or equivalent introspection) against the live/production Supabase instance
- Confirm the deployed `positions` schema matches `docs/specs/data_model.md`'s documented definition, including the new `idx_positions_open_ticker_entry_date_unique` partial index from DS-17
- Add a "Schema verification" note to the `positions` table section, dated, per the existing `portfolios` table convention

**Acceptance Criteria**
- Live schema confirmed to match spec (or discrepancies filed as their own follow-on items)
- Schema verification note added to `data_model.md`'s Positions Table section

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
**Priority:** P3 (Low)
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

### BLG-BE-117 — CI-blocking test_changelog_service.py failure on every PR
**Priority:** P1 (High)
**Type:** Bug / CI
**Owner:** Product Owner; API Contracts & Documentation Owner (changelog ownership — confirm exact owner during investigation)
**Source:** PR #1662 agent-mediated Director of Quality review, EPIC-01/v9.4 — 2026-09-14
**Effort:** S (~0.5–1d, pending root cause)
**Provisional-Target:** v9.5

**Problem**
`tests/test_changelog_service.py::test_real_changelog_is_parseable` fails with `assert None is not None` (`tests/test_changelog_service.py:90`) on every current CI run — confirmed failing 2 jobs (`Backend Test Coverage Report`, both `Pytest Phase B` matrix legs) on PR #1662, and confirmed via `git diff main...HEAD` that PR #1662 touches none of `docs/product/changelog.md`, `backend/services/changelog_service.py`, or the test file itself, so this is pre-existing on `main`, not a regression from that PR. Every open and future PR inherits this same CI-red state, blocking the merge gate's "CI passed, all checks green" requirement across the board, not just for one PR.

**Scope**
- Determine why `changelog_service`'s real-changelog parse returns `None` against the current `docs/product/changelog.md` (likely a changed heading/format the parser no longer recognises)
- Fix whichever side is wrong per canonical spec — the parser or the changelog file

**Acceptance Criteria**
- `test_real_changelog_is_parseable` passes against the real `docs/product/changelog.md`
- A clean PR shows CI green with no dependency on this fix

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

### BLG-OPS-161 — claude_audit_log has no latency column; no real-data source for AI endpoint latency anomaly checks

**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Data Model & Domain Schema Owner / Infrastructure & Operations Owner
**Source:** ST-09/EPIC-03, `2026-09-14__release-v9.4` — discovered while wiring the AI endpoint cost/latency anomaly check into a scheduled job (BLG-OPS-151) — 2026-09-14
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v9.5

**Problem**
`claude_audit_log` (`backend/database.py`) stores `endpoint`, `model_id`, `prompt_version`, `input_tokens`, `output_tokens`, `cost_usd`, `generated_at` — no latency/duration column. `services/ai_endpoint_anomaly_service.py`'s `check_latency_anomaly` therefore has no real production data to check against: `POST /ai/check-endpoint-anomalies` (ST-09, v9.4) only exercises it via a `simulated_latency_feed` test/dry-run parameter on the underlying service function, and always reports `latency_data_source: "not_available_pending_BLG-OPS-161"` over its public HTTP surface.

**Scope**
- Add a `latency_ms` (or `duration_ms`) column to `claude_audit_log`
- Populate it at each Claude API call site (`backend/services/gemini_service.py` and other call sites writing to `claude_audit_log`)
- Add a `get_claude_endpoint_latency_windows()` counterpart to `database.get_claude_endpoint_cost_windows()` and wire it into `run_scheduled_anomaly_check()` in place of the current simulated-feed-only path

**Acceptance Criteria**
- `claude_audit_log` carries a populated latency column for new rows
- `POST /ai/check-endpoint-anomalies` reports real (non-simulated) `latency_anomalies` with `latency_data_source` no longer `"not_available_pending_BLG-OPS-161"`

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

### BLG-OPS-162 — Provision read-only staging `DATABASE_URL` for sprint-execution sessions

**Priority:** P3 (Low)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** User request, session 2026-09-14, following recurring `DATABASE_URL`-unavailable disclosures across v9.2/v9.3/v9.4 sprint execution (RISK-01/RISK-03 pattern — e.g. ST-01/EPIC-01 duplicate pre-check, ST-09/ST-10/EPIC-03 real cost queries, all v9.4) — 2026-09-14
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v9.5

**Problem**
The interactive Claude Code sprint-execution session has no `DATABASE_URL` configured at all, by design (unlike the deployed Render backend and various GitHub Actions workflows, which each have their own separately-configured `DATABASE_URL`/`STAGING_DATABASE_URL`/`PROD_DATABASE_URL` secrets, `sync: false` in `render.yaml`, human-set only). This is correct isolation, not a misconfiguration, but it means every sprint-execution story whose AC calls for verification against real/live-shaped data (duplicate checks, cost-trend queries, migration pre-checks) has to be delivered against synthetic fixtures instead and explicitly disclosed as pending real-data verification — a recurring pattern across at least 3 consecutive release cycles (v9.2, v9.3, v9.4).

**Scope**
- Provision a read-only DB role scoped to the staging database only (never production)
- Make its connection string available to sprint-execution sessions as an environment variable set outside the conversation/session transcript (not pasted into chat, not committed to the repo) — mirroring the existing `STAGING_DATABASE_URL` / `reset-and-seed-staging.yml` infrastructure already used by CI

**Acceptance Criteria**
- A read-only staging DB credential exists and is scoped so it cannot mutate any table
- The credential is injected into sprint-execution sessions via environment configuration, never appearing as chat text or in git history
- A sprint-execution session can successfully run a real read-only query against staging data end-to-end as a smoke test

---

### BLG-GOV-332 — Require resolving commits to update the canonical spec's own Known Deviation fields when closing a deviation

**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Cross-EPIC Deviation Consolidation Review, 4th run (`docs/governance/deviation_consolidation_review_2026-09-03.md`, Recommendation 1) and 5th run (`docs/governance/deviation_consolidation_review_2026-09-15.md`, Finding 3) — recommended in 2 of 5 review runs with no backlog item filed until now; raised as Outstanding Action #5 in post-ship closure `2026-09-14__release-v9.4`'s `closure_record.md` §6 — 2026-09-15
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
When a story or engine action fixes the root cause of a pre-existing, already-filed deviation, nothing currently requires that same commit to also update the deviation's own labeled Known Deviation fields (`Target resolution release`, `Status`, resolution narrative) in the canonical spec where it was originally filed. This produces a recurring resolution-status drift pattern: the fix lands and is documented elsewhere (a QA evidence log, a test-scenario doc, an operational record), but the deviation's own canonical-spec entry is left reading as still-open or still-targeting a future release. The Cross-EPIC Deviation Consolidation Review has independently found and corrected this same drift class 3 times across its first 4 runs (`DEV-ST14-01`, `DEV-v8.6-ST02-01`, `DEV-EPIC03-ST09-01`), spanning 3 different documents — confirming it is a structural gap, not a one-off oversight.

**Scope**
- Add a rule (likely to `execution_prompt.md` §3.1.A, alongside the existing `deviations_filed` atomic-write discipline for *filing* a deviation) requiring that any commit which resolves a pre-existing deviation's root cause also updates that deviation's own labeled fields in the same commit
- Cross-reference from `claude/charter/document_lifecycle_guide.md §9` (Known Deviation Documentation Standard)

**Acceptance Criteria**
- A named governed-routine step requires resolving-commit-updates-canonical-entry discipline, mirroring the existing filing-time discipline
- Next Cross-EPIC Deviation Consolidation Review confirms 0 new resolution-status-drift instances found after this rule lands
- Head of Specs Team sign-off

---

### BLG-FE-177 — Fix trade plan link display to use formatted text instead of snake_case
**Priority:** P2 (Medium)
**Type:** Frontend / UX Bug
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Source:** User request, session 2026-09-15
**Effort:** XS (<1h)
**Provisional-Target:** v9.5

**Problem**
On trade entry, when linking to a trade plan, the linked plan's identifier/name is rendered in raw snake_case (e.g. `aapl_swing_plan`) rather than human-readable formatted text. This is inconsistent with the rest of the trade entry UI and makes the linked plan harder to scan at a glance.

**Scope**
- Identify the component rendering the trade plan link on the trade entry screen
- Apply a display-formatting transform (snake_case → readable text) before rendering
- Apply consistently to any other trade-plan references formatted the same way nearby, if trivial

**Acceptance Criteria**
- Trade plan link/reference on trade entry displays human-readable formatted text, not snake_case
- No underscores visible in the rendered trade plan link text
- Existing trade plan linkage functionality (click-through/navigation) unaffected

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

### BLG-GOV-334 — Correct qa_evidence_EPIC-03.md's stale test-count claim via cross-cycle deviation consolidation

**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Director of Quality (executes via Post-Ship Closure Engine STEP 5.1); Head of Specs Team (ruling authority, document lifecycle)
**Source:** ST-21 (BLG-QA-170, EPIC-03, `2026-09-15__release-v9.5` sprint execution) — Head of Specs Team ruling on the correction mechanism, 2026-09-17
**Effort:** XS (<1h)
**Provisional-Target:** Next `run post-ship` for `2026-09-15__release-v9.5`
**Depends on:** BLG-QA-170 (superseded by this item's correction mechanism, not closed by it directly)

**Problem**
`BLG-QA-170` found `claude/cycles/2026-09-09__release-v9.3/qa_evidence_EPIC-03.md` claims `tests/test_cost_monitoring.py` contains "30 tests" / "30/30 pass"; the actual count at that PR's head commit was 28 (re-confirmed independently this session via `grep -c "^def test_" tests/test_cost_monitoring.py` against `main`). `BLG-QA-170`'s own scope named the qa_evidence file itself as the correction target, but that file lives inside `claude/cycles/2026-09-09__release-v9.3/`, a cycle whose `state.json` reads `"status": "Published"` with a `"sealed"` block (`sealed_utc: 2026-09-09T02:20:00Z`) — CLAUDE.md §2's "Never modify sealed artefacts... immutable" rule applies, and no prompt, role, or user instruction may override it (CLAUDE.md's own text). `execution_prompt.md` §7's write-scope restriction independently confirms Sprint Execution may only write within the *active* cycle's `claude/cycles/<cycle_id>/` tree, not a prior cycle's.

Ruled by Head of Specs Team (2026-09-17, acting on explicit user direction, `claude/agents/head_of_specs_team.md` §5/§6 — Change Governance and Decision Escalation & Conflict Resolution): the sealed file must not be touched, in any form (including an addendum appended within the sealed cycle folder) — consistent with existing codebase precedent (`e06cfa94`'s commit message: "Historical changelog/report entries in `docs/product/changelog.md` and sealed cycle records were left untouched — they describe point-in-time history, not current state"). The correct mechanism for this class of correction already exists and has been used once before in this exact codebase: `docs/ops/api_performance_baseline.md`'s Document History §v2.32 entry, made by the **Post-Ship Closure Engine's STEP 5.1 cross-cycle deviation consolidation review** — a routine explicitly designed to correct stale/inaccurate claims discovered in prior-cycle artefacts, operating under its own write scope rather than Sprint Execution's.

**Scope**
- At the next `run post-ship` invocation for `2026-09-15__release-v9.5` (or any later cycle, if this item ages before then), action this correction via STEP 5.1's cross-cycle deviation consolidation review, following the exact resolution mechanism `api_performance_baseline.md` §v2.32 already demonstrates for this class of finding
- The correction target remains `claude/cycles/2026-09-09__release-v9.3/qa_evidence_EPIC-03.md`'s "30 tests" / "30/30 pass" claims (2 locations: the `Test scenarios used` header line and the `Scenarios run` bullet in its DoQ sign-off block) — correct to 28, sourced from the verified `grep -c` count above, not re-derived from scratch
- Record the correction in whatever mechanism STEP 5.1 uses for its own audit trail (mirroring `api_performance_baseline.md`'s Document History table entry)
- Close `BLG-QA-170` and this item together once the correction lands

**Acceptance Criteria**
- `claude/cycles/2026-09-09__release-v9.3/qa_evidence_EPIC-03.md`'s test-count claims read 28, not 30, in both locations named above
- The correction is recorded via Post-Ship Closure Engine's own audit-trail mechanism, not a direct out-of-scope edit from a different governed routine
- `BLG-QA-170` and `BLG-GOV-334` both closed in the same action

---

## Release Slice — v9.5 (ephemeral — remove at next `groom backlog` per Placement Rule)

<!-- release-plan-marker: RP:v9.5:2026-09-15__release-v9.5 -->

43 items selected into `2026-09-15__release-v9.5` scope (27.99 estimated days, full capacity). Full acceptance criteria: `claude/cycles/2026-09-15__release-v9.5/stage4_backlog_slice.md`. Selection method: P1 items first, then P2 items (ascending ID), then category-balanced round-robin oldest-first, from a 62-item / ~43.79-day ungated ready pool.

| ST-ID | Item | EPIC |
|-------|------|------|
| ST-01 | BLG-BE-117 | EPIC-01 |
| ST-02 | BLG-BE-112 | EPIC-01 |
| ST-03 | BLG-BE-113 | EPIC-01 |
| ST-04 | BLG-BE-114 | EPIC-01 |
| ST-05 | BLG-OPS-160 | EPIC-02 |
| ST-06 | BLG-OPS-153 | EPIC-02 |
| ST-07 | BLG-OPS-154 | EPIC-02 |
| ST-08 | BLG-OPS-155 | EPIC-02 |
| ST-09 | BLG-OPS-156 | EPIC-02 |
| ST-10 | BLG-OPS-157 | EPIC-02 |
| ST-11 | BLG-OPS-158 | EPIC-02 |
| ST-12 | BLG-OPS-159 | EPIC-02 |
| ST-13 | BLG-OPS-161 | EPIC-02 |
| ST-14 | BLG-OPS-162 | EPIC-02 |
| ST-15 | BLG-QA-59 | EPIC-03 |
| ST-16 | BLG-QA-165 | EPIC-03 |
| ST-17 | BLG-QA-166 | EPIC-03 |
| ST-18 | BLG-QA-167 | EPIC-03 |
| ST-19 | BLG-QA-168 | EPIC-03 |
| ST-20 | BLG-QA-169 | EPIC-03 |
| ST-21 | BLG-QA-170 | EPIC-03 |
| ST-22 | BLG-SPEC-D18 | EPIC-04 |
| ST-23 | BLG-SPEC-56 | EPIC-04 |
| ST-24 | BLG-SPEC-57 | EPIC-04 |
| ST-25 | BLG-SPEC-133 | EPIC-04 |
| ST-26 | BLG-SPEC-139 | EPIC-04 |
| ST-27 | BLG-SPEC-140 | EPIC-04 |
| ST-28 | BLG-SPEC-141 | EPIC-04 |
| ST-29 | BLG-SPEC-142 | EPIC-04 |
| ST-30 | BLG-SPEC-143 | EPIC-04 |
| ST-31 | BLG-GOV-332 | EPIC-05 |
| ST-32 | BLG-GOV-316 | EPIC-05 |
| ST-33 | BLG-GOV-318 | EPIC-05 |
| ST-34 | BLG-GOV-319 | EPIC-05 |
| ST-35 | BLG-GOV-320 | EPIC-05 |
| ST-36 | BLG-GOV-321 | EPIC-05 |
| ST-37 | BLG-GOV-322 | EPIC-05 |
| ST-38 | BLG-GOV-323 | EPIC-05 |
| ST-39 | BLG-GOV-324 | EPIC-05 |
| ST-40 | BLG-FE-177 | EPIC-06 |
| ST-41 | BLG-FE-175 | EPIC-06 |
| ST-42 | BLG-FE-176 | EPIC-06 |
| ST-43 | BLG-UX-05 | EPIC-06 |

Not re-selected: `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76` (substantively gate-blocked per their own body text, no formal `Gate` field). Design-gate-triggering: `BLG-FE-177`, `BLG-FE-175`, `BLG-FE-176`, `BLG-UX-05` (all of EPIC-06 — observable UI ACs) — `run design-gate --cycle 2026-09-15__release-v9.5` required before `plan sprint` seals.

---

