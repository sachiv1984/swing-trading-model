# Product Backlog — Momentum Trading Assistant

<!-- last-spec-debt-deep-review: 2026-09-23__release-v9.7 -->

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-10-05 (sprint execution EPIC-04/ST-20, BLG-GOV-358 — §13 retroactive review of the Gap Risk Flag (CONDITIONAL); 4 remediation items added: BLG-BE-136 (weekend-hold trigger disposition + trigger-timing label/spec alignment), BLG-SPEC-179 (positions.md Gap Risk Badge data source), BLG-GOV-359 (§13 ACs must cite every §13 clause naming the subject), BLG-GOV-360 (apply §13.3/§13.5 strategy_rules.md wording)); prior — 2026-10-05 (sprint execution EPIC-04/ST-24, BLG-GOV-350, under Head of Specs Team write-scope ruling ESC-EXEC-20261001-01 — new `## Shared Gate References` section holding the canonical 90-Day AI Feature Usage Review Gate statement; Gate criteria lines of BLG-FEAT-59/60/63, BLG-FE-84, BLG-OPS-88 now cite it; 2 new items added: BLG-GOV-361 (BLG-SPEC-65's stale sixth gate copy), BLG-GOV-362 (standing plan-authorised write-scope rule)); prior — 2026-10-05 (PR #1888/#1889 agent-mediated DoQ + PO review — 4 new items added: BLG-QA-210 (ST-12 sizing property lacks a lower bound), BLG-QA-211 (real-bound modules cached across the session), BLG-OPS-178 (test-only deps in the production build), BLG-FE-194 (zero-P&L badge glyph)); prior history retained — see prior entries in version control.
**Last rebalance:** 2026-09-30 (cycle 2026-09-30__scheduled — DL-082; 0 active initiatives, CPS=N/A (15th consecutive); idea intake IW-20260930-01 (4 submissions, 2-agent disclosed reduced scope, run standalone pre-run per idea_intake_prompt.md §2), consolidated into BLG-BE-135 (ungated) + BLG-FE-193 (gate-conditional on BLG-BE-135); IDEA-director-of-hr-20260919-02 resolved at 3-cycle park hard cap → Backlog (ungated), BLG-GOV-357; new §13-boundary finding filed, BLG-GOV-358; PVR 0.094 🔴 Alert (5th consecutive, marginal improvement, U=16/G=41/D=109/P=4 of 170, window v9.4–v9.8) — PO Modify, BLG-BE-135/BLG-FE-193 named as recommended candidate; Skill-Silo 83.7% (2nd consecutive improving reading) — advisory only, no mandatory pull-forward; STEP 8.1 Option (b) defer, 8th consecutive; STEP 11.4 meta-review due and actioned, 0 action-now from the meta-review itself, 1 action-now patch from live STEP -1.6 friction)

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

## Shared Gate References

> Canonical statements of gate conditions shared by more than one backlog item. An item that depends on one of these gates names it in its own `**Gate criteria:**` line instead of restating the condition. Each citing line keeps the gate's review-due date as a plain `due YYYY-MM-DD` token, because `scripts/scan_backlog_gate_conditions.py` — read by `post_ship_closure.md` STEP 12.6, `roadmap_prompt.md` STEP 3.1 and `release_planning_prompt.md` §1.3a — only sees the item's own line. Everything else about the gate is stated here and nowhere else. Section owner: Head of Specs Team.

### 90-Day AI Feature Usage Review Gate

- **What is reviewed:** the 90-day AI feature usage and cost review of the AI briefing and chat features (BLG-GOV-74 cadence — 90 days after the v6.2 ship of 2026-06-25). It assesses adoption rate, cost per use, usage-pattern stability and continued-investment justification (BLG-GOV-142's criteria). Conducting the review is tracked as BLG-GOV-356.
- **Review due date:** 2026-09-24. Every citing item carries this same date as `due 2026-09-24`. If the review is rescheduled, change this line and every citing item's date token in the same commit — `grep -n "90-Day AI Feature Usage Review Gate" claude/backlog/backlog.md` lists them.
- **Evidence:** a dated review artefact matching `docs/ops/*ai*usage*review*<date>*.md` (the same pattern `post_ship_closure.md` STEP 12.6 checks), or the equivalent artefact named when BLG-GOV-356 closes.
- **Clearance rule:** the gate clears for an item only when that artefact exists, records an explicit disposition for that item, and the item's named clearance owner has confirmed it on the item. Until then the gate is unmet. A passed due date on its own is never a clearance.
- **After the review:** each citing item's outcome (cleared, or re-parked with a new concrete trigger) is recorded on that item, replacing its `**Gate criteria:**` line. This statement does not change when the review completes. Remove it in the same commit that dispositions the last item still citing it.

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
**Gate criteria:** 90-Day AI Feature Usage Review Gate — review due 2026-09-24 (canonical statement: § Shared Gate References at the top of this file). Clearance for this item confirmed by: Financial Reporting & Records Owner.

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
**Gate criteria:** 90-Day AI Feature Usage Review Gate — review due 2026-09-24 (canonical statement: § Shared Gate References at the top of this file). Clearance for this item confirmed by: Metrics Definitions & Analytics Owner.

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
**Gate criteria:** 90-Day AI Feature Usage Review Gate — review due 2026-09-24 (canonical statement: § Shared Gate References at the top of this file). Clearance for this item confirmed by: Head of UX & Design.

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
**Gate criteria:** 90-Day AI Feature Usage Review Gate — review due 2026-09-24 (canonical statement: § Shared Gate References at the top of this file). This item is bundled with that review (carried out alongside it) rather than cleared by an adoption finding — no standalone signal yet shows the current dyno tier is mismatched. Clearance for this item confirmed by: FinOps & Resource Architect.

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
**Gate criteria:** 90-Day AI Feature Usage Review Gate — review due 2026-09-24 (canonical statement: § Shared Gate References at the top of this file). This estimate feeds BLG-FEAT-59 — its disposition follows BLG-FEAT-59's. Clearance for this item confirmed by: Financial Reporting & Records Owner.

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

---

### BLG-GOV-235 — Idea-intake minimum-submission flex condition
**Priority:** P3 (Low) | **Type:** Governance | **Owner:** Head of Specs Team | **Source:** IDEA-director-of-hr-20260715-01 | **Effort:** S | **Provisional-Target:** TBD
**Gate criteria:** Recurs at 3+ consecutive scheduled cycles where the Now horizon is already populated with 3+ ad-hoc (non-governed-cycle) P1 items at window-open — not yet met (this is the 1st such occurrence).
**Problem:** `idea_intake_prompt.md`'s standing 2-net-new-ideas-per-agent minimum does not flex when the Now horizon is already saturated with ad-hoc additions, potentially generating submissions redundant with just-added scope.
**Scope:** If the gate condition recurs, evaluate whether the minimum should reduce or the window should skip agents whose domain is already covered by the ad-hoc additions.
**Acceptance Criteria:** Gate re-checked each scheduled cycle; a written decision follows once met.

---

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

### BLG-GOV-347 — scan_backlog_gate_conditions.py date-disambiguation gap can produce false negatives
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Agent-mediated Director of Quality review, PR #1758, cycle 2026-09-21__release-v9.6 — 2026-09-23
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`scripts/scan_backlog_gate_conditions.py`'s `_lapsed_date()` (added ST-27, `BLG-GOV-345`) uses `EMBEDDED_DATE_RE` with `re.search`, which returns the FIRST ISO date found in a gate_condition string — not necessarily the date the gate actually clears on. The function's own docstring already discloses "Multiple dates... not disambiguated — the first match is used." On the live `backlog.md` this hasn't produced a wrong answer (verified: `BLG-FEAT-55`'s two dates, `2026-06-25` and `2026-07-25`, are both in the past, so the gate correctly reports lapsed regardless of which is picked). But the mechanism doesn't guarantee this: a gate-condition string mentioning an earlier, still-future date before a later, already-past clears-date would be silently reported as NOT lapsed (false negative) — the reverse ordering would produce a false positive. Since this script drives a real release-planning gate decision (`release_planning_prompt.md` §1.3a), an undetected false negative means a genuinely-clearable item stays hidden from the ready pool indefinitely.

**Scope**
- Either: prefer a date immediately following a keyword like "clears"/"due"/"completes"/"by" over a bare first-match, or explicitly flag (not silently resolve) any `gate_condition` containing more than one embedded date for manual disambiguation
- Add a test file covering at least: single-date lapsed, single-date not-lapsed, multi-date-both-past, multi-date-both-future, and the specific false-negative/false-positive orderings described above

**Acceptance Criteria**
- A `gate_condition` with an early future date and a later past date is correctly flagged as lapsed (or explicitly flagged for manual disambiguation, not silently resolved wrong)
- A test file exists and passes in CI covering the cases above

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

### BLG-SPEC-164 — Drop 4 confirmed-orphaned, always-NULL columns from the live positions table
**Priority:** P4 (Trivial)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-25/EPIC-06, 2026-09-23__release-v9.7 — 2026-09-24
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`data_model.md`'s Positions Table section (v2.41) documents 4 live `positions` columns — `atr_value`, `stop_price`, `fees`, `pnl_percent` — as confirmed orphaned (always NULL on every row, no read or write path anywhere in `backend/` references them; their documented same-purpose counterparts `atr`/`current_stop`/`fees_paid`/`pnl_pct` are the ones actually used) and recommends a drop. The documentation-only disposition was completed; the actual `DROP COLUMN` migration was not applied — that is a live production schema change requiring the Data Model & Domain Schema Owner's own migration process, not a documentation story.

**Scope**
- Apply a migration dropping `atr_value`, `stop_price`, `fees`, `pnl_percent` from the live `positions` table
- Update `data_model.md`'s Migration History section with the down/drop migration record, and remove the now-resolved orphaned-column disclosure note once dropped

**Acceptance Criteria**
- All 4 columns no longer exist on the live `positions` table
- `data_model.md` reflects the drop in its Migration History

---

### BLG-SPEC-165 — Reconcile positions.fees_paid NOT NULL constraint (re-apply live, or confirm nullable is intentional)
**Priority:** P4 (Trivial)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-26/EPIC-06, 2026-09-23__release-v9.7 — 2026-09-24
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`data_model.md` (v2.42) documented `fees_paid` as `NOT NULL as of v1.6`, citing the "Migration from v1.5 to v1.6" record (`ALTER TABLE positions ALTER COLUMN fees_paid SET NOT NULL`). A live schema query (readonly staging) confirmed the column is nullable today — the constraint was either later dropped (not documented anywhere in this file's migration history) or never durably applied in the environment queried. The documentation was reconciled to nullable (matching live reality) as the safe, non-destructive disposition; this item tracks the actual reconciliation decision.

**Scope**
- Determine why the v1.6 `NOT NULL` constraint is not present live (dropped, rolled back, or never applied) — check migration run history if available
- Decide: re-apply the `NOT NULL` constraint live (if no existing row has a NULL `fees_paid`, and the original v1.6 intent should be re-enforced), or confirm nullable is now the intentional, permanent state and document why

**Acceptance Criteria**
- Disposition recorded (constraint re-applied, or nullable confirmed intentional with a stated reason)
- `data_model.md` and the live schema agree, one way or the other, with the reasoning documented (not just the fact)

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

### BLG-QA-190 — Convert remaining test files sharing test_trade_plan_audit_log.py's unrestored sys.modules["database"] swap pattern
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality
**Source:** ST-21 (EPIC-05, v9.6, BLG-QA-178) AC-3 audit — DEV-EPIC05-ST21-01, `claude/cycles/2026-09-21__release-v9.6/qa_evidence_EPIC-05.md` — 2026-09-22
**Effort:** M (~1-2d)
**Provisional-Target:** v9.7

**Problem**
ST-21 fixed `test_trade_plan_audit_log.py`'s permanent, unrestored `sys.modules.pop("database", None); import database` (converted to the isolated-copy `importlib.util.spec_from_file_location` pattern `test_position_audit_log.py` already uses). Its own AC-3 required grepping `tests/` for the same pattern and fixing every match in the same commit. The audit found ~29 other files matching the literal text, but they are not structurally uniform, so the fix could not safely be mass-applied within that story's XS effort budget.

**Scope**
- Category A (convertible, low risk): files that just call `database.X()` directly with no FastAPI TestClient/main.app dependency — apply the same isolated-copy pattern. Includes (non-exhaustive, re-grep to confirm current list): `test_arc5_total_closed_trades_null_vs_zero.py`, `test_changelog_service.py`, `test_changelog_digest_service.py`, `test_monthly_ai_cost.py`, `test_rebalance_exit_signal_numpy_regression.py` (also pops `utils.formatting` — widen the audit to that module too), `test_signal_write_path_consolidation.py`, `test_service_layer_direct_coverage.py`, `test_signal_write_sanitization.py`, `test_strategy_benchmark_summary.py`, `test_strategy_version_at_entry.py`, `test_tax_year_boundary_completeness.py`, `test_trade_plan_tags.py`, `test_ticker_market_sanitization_regression.py`, `test_trade_origin_query.py`, `test_trade_plan_completion_rate.py`, `test_trade_plans_ticker_index.py`, `test_trade_plan_thesis_provenance.py`
- Category B (needs a different fix): files importing FastAPI's TestClient/main.app, where router-level `from database import X` bindings resolve against `sys.modules["database"]` at import time — the isolated-copy pattern does not apply. Needs a restore-based fix instead (e.g. a module-scoped teardown/fixture that re-installs `conftest.py`'s stub after the module's tests run). Includes: `test_api_contracts.py`, `test_backtest_rule_runs_pagination.py`, `test_main_500_no_raw_exception_text.py`, `test_idempotency_endpoints.py`, `test_job_registration_screener_risk_off.py`, `test_rate_limit_endpoints.py`, `test_router_error_envelope_conformance.py`, `test_st04_implicit_200_error_paths_fixed.py`, `test_tag_performance_ensure_table_call.py`, `test_trade_plan_setup_type_default.py`, `test_cost_monitoring.py`
- Category C (already deliberate, review only): `test_ensure_trade_plans_table_memoization.py`, `test_schema.py`, `test_schema_rollback_verification.py` — already re-acquire the module fresh per-test/function-scoped rather than at plain module level; confirm whether their own documented rationale still holds or whether they'd also benefit from the restore-based fix

**Acceptance Criteria**
- Re-run `grep -rln 'sys.modules.pop("database", None)' tests/*.py` to confirm the current file list (this list may have drifted since 2026-09-22)
- Every Category A file converted to the isolated-copy pattern; every Category B file given a restore-based fix; Category C files reviewed and either left as-is with rationale reconfirmed, or fixed if the review finds a live gap
- Full backend test suite passes with no new failures (only the 7 pre-existing `test_schema*.py` live-staging-DB-permission failures remain)
- A manual reordering check (run in a non-default order, or via a throwaway canary asserting `sys.modules["database"]` is unchanged after each fixed file) confirms no cross-file leakage remains from this pattern anywhere in `tests/`

---

### BLG-QA-191 — Add automated test coverage for the I/O-boundary functions in EPIC-04's staleness/CI-usage scripts
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality
**Source:** PR #1753 (EPIC-04) agent-mediated Director of Quality review finding — 2026-09-22
**Effort:** S (~0.5d)
**Provisional-Target:** v9.7

**Problem**
`scripts/check_nightly_stop_update_staleness.py` and `scripts/generate_ci_usage_report.py` (ST-14/ST-17, EPIC-04, v9.6) both separate pure comparison/aggregation logic from I/O, and the pure logic is well unit-tested (7 and 14 tests respectively). But every I/O-boundary function in both scripts (`get_scheduler_health`, `fetch_workflows`, `fetch_workflow_run_count_and_sample`, `fetch_run_duration_ms`, `fetch_artifacts_in_window`, and the shared `_gh_api`/`_gh_api_paginated` helpers) has zero automated test coverage — they were verified only via live manual runs during the v9.6 sprint session, not CI-reproducible. A future regression in the pagination or response-parsing logic (e.g. the `gh api --paginate` NDJSON-concatenation gotcha `generate_ci_usage_report.py`'s own code comment documents having hit once already) would not be caught until the next scheduled/live run surfaces it.

**Scope**
- Add tests for the I/O-boundary functions in both scripts using mocked subprocess/requests calls (e.g. the `responses` library or `unittest.mock.patch` on `subprocess.run` / `requests.get`) so the pagination, error-handling, and response-parsing logic is exercised without live GitHub/API calls
- Cover at minimum: the `gh api --paginate` manual-pagination loop (`_gh_api_paginated`), a multi-page response, and the `GET /health/scheduler` response-shape parsing in `check_nightly_stop_update_staleness.py`'s `main()`

**Acceptance Criteria**
- Both scripts' I/O-boundary functions have unit tests using mocked external calls (no live network/`gh` CLI dependency)
- A deliberate regression in the pagination loop (e.g. an off-by-one in the page-continuation condition) is confirmed to fail the new tests

---

### BLG-QA-192 — test_null_fee_trade_audit.py's inspect.getsource() call fails against the database module stub
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** ST-11/EPIC-03, 2026-09-23__release-v9.7 — 2026-09-24
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`tests/test_null_fee_trade_audit.py::test_get_monthly_pnl_sql_filters_on_either_fee_leg_null` does `from database import get_monthly_pnl` then `inspect.getsource(get_monthly_pnl)`. `tests/conftest.py` replaces `sys.modules["database"]` with a session-scoped `MagicMock` stub (BLG-QA-20/retired BLG-QA-73), so this import binds to the stub, not the real function, and `inspect.getsource()` on a `MagicMock` raises `TypeError`. Confirmed failing on `main` before this story's changes (reproduced in isolation, unrelated to ST-11's own fix) — found while writing `tests/test_month_closure_clock_source.py`'s sibling SQL-inspection test for `get_monthly_pnl`, which uses the correct pattern instead.

**Scope**
- Convert the test to use the private, isolated `backend/database.py` import pattern already used by `tests/test_reflection_reminder.py` / `tests/test_monthly_pnl_snapshot.py` / `tests/test_month_closure_clock_source.py` (`importlib.util.spec_from_file_location`, never touching `sys.modules["database"]`)

**Acceptance Criteria**
- The test passes when run both in isolation and as part of the full suite
- No other test in the file is affected

---

### BLG-SPEC-166 — Cross-reference current_roadmap.md's SI-02 field to the canonical "linked trade plan" definition
**Priority:** P4 (Backlog)
**Type:** Spec Debt
**Owner:** Head of Specs Team; PMO Lead
**Source:** ST-23/EPIC-06, cycle 2026-09-23__release-v9.7 — surfaced during agent-mediated Product Owner review of PR #1795 — 2026-09-24
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-23 (EPIC-06, `2026-09-23__release-v9.7`) shipped the canonical "linked trade plan" definition for the SI-02 gate, but its acceptance criteria also required `current_roadmap.md`'s SI-02 field to cross-reference that definition. `claude/roadmap/*` is outside Sprint Execution's write scope (`execution_prompt.md` §7), so the cross-reference was correctly left undone by that engine rather than written out of scope — but no backlog item was filed to track the gap, unlike the two sibling out-of-scope findings from the same EPIC (`BLG-SPEC-164`/`165`), which were properly filed. Without this item, the half-completed AC has no tracked path to closure.

**Scope**
- Add a cross-reference in `current_roadmap.md`'s SI-02 field to the canonical "linked trade plan" definition shipped by ST-23
- Action via Roadmap Rebalance or another engine with `claude/roadmap/*` write authority — not Sprint Execution

**Acceptance Criteria**
- `current_roadmap.md`'s SI-02 field cross-references the canonical "linked trade plan" definition
- ST-23's originally-scoped acceptance criteria are fully met

---

### BLG-SPEC-167 — data_model.md DS-19 "Verification status" still says the migration was never run against a live PostgreSQL
**Priority:** P4 (Backlog)
**Type:** Spec Debt
**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Source:** ST-27/EPIC-07, cycle 2026-09-23__release-v9.7 — DEL-20260924-02 staging verification — 2026-09-24
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`docs/specs/data_model.md` DS-19's "Verification status" paragraph states the DDL and SQL are covered only by mocked-cursor tests and "have **not** been executed against a live PostgreSQL". That is no longer true: on 2026-09-24 a human operator confirmed on STAGING that both `alert_type` CHECK constraints include `reflection_reminder` and `uq_notifications_reflection_reminder_trade` exists with the DS-19 definition, and that two `POST /alerts/evaluate` runs created 14 then 0 reflection reminders with no duplicate rows. Sprint Execution may not edit canonical specs beyond deviation documentation, so the stale text was left in place rather than corrected in ST-27.

**Scope**
- Replace DS-19's "Verification status" paragraph with a live-confirmation note (dated, staging only) following the precedent of DS-17's "Live Confirmation" section
- Cite `qa_evidence_EPIC-07.md` (cycle `2026-09-23__release-v9.7`) as the evidence source; record that this is staging, not production
- Follow the Governance File Edit Checklist / version-sync rules for `data_model.md` (header, footer, changelog)

**Acceptance Criteria**
- DS-19 no longer claims the migration has never run against a live database, and states what was confirmed, where (staging) and when
- `data_model.md` header/footer versions stay in sync

---

### BLG-SEC-40 — Two residual gaps in the just-hardened non-registry dependency guard
**Priority:** P3 (Low)
**Type:** Security / Supply Chain
**Owner:** Cybersecurity & Trust Lead
**Source:** ST-19/EPIC-04 (BLG-SEC-39), cycle 2026-09-28__release-v9.8 — agent-mediated review of PR #1846 — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
Two gaps found reviewing `scripts/check_non_registry_dependencies.py` after BLG-SEC-39's hardening (PR #1846):
1. `_PIP_LOCAL_PATH_RE` requires a trailing `/` after `-e ` and the dot(s) (`\.{1,2}/`), so it catches `-e ./pkg` and `-e ../pkg` but misses the bare current-directory self-install form `-e .` (no trailing slash) — a real, still-unflagged local-path install.
2. `check_package_lock_json` flags any `resolved` value not served from `https://registry.npmjs.org/` as a violation, including a legitimate npm workspace-local reference (`"resolved": "file:../packages/foo"` without a `"link": true` marker) — currently dormant since this repo has no npm workspaces, but would false-positive the moment one is introduced.

**Scope**
- Extend `_PIP_LOCAL_PATH_RE` (or add a second pattern) to also match a bare `-e .`/`-e ..` with no trailing slash
- Add an exemption (or a documented allow-list check) for `file:` workspace-local `resolved` entries in `check_package_lock_json`, scoped narrowly enough not to reopen the general `file:` non-registry gap
- Add a regression test for each

**Acceptance Criteria**
- `-e .` and `-e ..` (no trailing slash) are rejected by a test
- A synthetic npm-workspace-local `file:` lockfile entry is confirmed NOT flagged by a test, while a genuine non-workspace `file:`/git resolved URL is still flagged

---

### BLG-QA-193 — Prove the non-registry dependency check fails a real PR, and confirm it is a required status check on main
**Priority:** P4 (Backlog)
**Type:** QA / Test Automation
**Owner:** Director of Quality; Infrastructure & Operations Owner
**Source:** ST-29/EPIC-07 (BLG-SEC-38), cycle 2026-09-23__release-v9.7 — ST-29 recorded as "Pass with notes" and flagged in the agent-mediated review of PR #1800 — 2026-09-24
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-29's acceptance criterion is "a test PR adding a `git+ssh` dependency fails CI". The guard's logic is unit-tested, and the workflow runs on `pull_request`, but nobody has observed a real GitHub Actions run failing on a deliberately introduced non-registry dependency, and it has not been confirmed that `Non-Registry Dependency Check (ST-29)` is a required status check on `main` (if it is not, a failing run would not block a merge).

**Scope**
- Open a throwaway PR that adds a `git+ssh` dependency to `backend/requirements.txt`, record the failing run, then close the PR unmerged
- Check the `main` branch protection settings and record whether this check is required; if not, raise that with the Infrastructure & Operations Owner

**Acceptance Criteria**
- A recorded failing CI run (run URL) for a PR adding a `git+ssh` dependency
- The required-status-check state on `main` is recorded, either way

---

### BLG-SPEC-168 — Correct the BLG-BE-128 citation to BLG-BE-129 for the latency_ms composition decision
**Priority:** P4 (Backlog)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner; Infrastructure & Operations Owner
**Source:** ST-13/EPIC-03 and ST-28/EPIC-07, cycle 2026-09-23__release-v9.7 — agent-mediated review of PR #1800 — 2026-09-24
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`docs/specs/api_contracts/ai_endpoints.md` attributes the `latency_ms` composition decision (ST-13, EPIC-03, v9.7) to `BLG-BE-128` at lines 5, 419 and 829. That decision is `BLG-BE-129`; `BLG-BE-128` is a different item (remaining ad hoc `timeout=`/retry call sites not yet on the shared upstream helper). The external-dependency register (`docs/ops/external_api_dependency_register.md`, entry CFM-03, ST-28) copied the wrong ID from the contract, so a reader following either citation lands on an unrelated item.

**Scope**
- Correct the three `BLG-BE-128` citations in `ai_endpoints.md` to `BLG-BE-129`, following the contract's version-history conventions
- Correct the same citation in the dependency register's CFM-03 entry

**Acceptance Criteria**
- No reference to `BLG-BE-128` remains where `BLG-BE-129` is meant, in `ai_endpoints.md` or the dependency register
- `BLG-BE-128`'s own legitimate references are untouched

---

### BLG-SPEC-169 — Correct notifications.md and the alert-thresholds empty-state scenario doc to the no-trailing-period empty-state headings now shipped
**Priority:** P4 (Backlog)
**Type:** Spec Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-05/ST-06/EPIC-02, cycle 2026-09-23__release-v9.7 (Known Deviation DEV-v9.7-ST05-01, `notifications.md`) — 2026-09-24
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`docs/specs/frontend/pages/notifications.md` still specifies the empty-state headings with a trailing period — "No alert rules configured." (§Section 2) and "No alert history yet." (§Alert History) — and `docs/testing/alert_thresholds_empty_state_scenarios.md` (line 36) still describes the first as "No alert rules configured." ST-05/ST-06 (v9.7) brought the shipped code to the canonical no-trailing-period pattern in `design_system.md` §Data States, so the page spec and the scenario doc now disagree with both the shipped code and the design system. The v9.5 ST-30 sweep corrected the same staleness in three other specs but left these two headings alone because the code then violated the pattern; they were not revisited when the code was fixed.

**Scope**
- Drop the trailing period from the two headings in `notifications.md` and bump its version/changelog
- Correct the heading text in `alert_thresholds_empty_state_scenarios.md`
- Close Known Deviation DEV-v9.7-ST05-01 in `notifications.md` as resolved

**Acceptance Criteria**
- `notifications.md` and `alert_thresholds_empty_state_scenarios.md` state "No alert rules configured" and "No alert history yet" without a trailing period, matching shipped code and `design_system.md` §Data States
- DEV-v9.7-ST05-01 is marked resolved with this item's ID

---

### BLG-SPEC-170 — Reconcile the Monthly Restatement Marker spec with what GET /reports/monthly-pnl actually returns (snapshot date, failure signal)
**Priority:** P4 (Backlog)
**Type:** Spec Debt
**Owner:** Frontend Specifications & UX Documentation Owner; API Contracts & Documentation Owner
**Source:** ST-04/EPIC-02, cycle 2026-09-23__release-v9.7 (Known Deviation DEV-v9.7-ST04-01, `reports.md`) — 2026-09-24
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`docs/specs/frontend/pages/reports.md` §Monthly Restatement Marker (v0.19) specifies that the detail row's "As reviewed" value carries the snapshot date (`{snapshot_date}`), but `GET /reports/monthly-pnl` (`reports_endpoints.md` v0.13) returns no such field — only `snapshotted`, `restated`, `snapshot_realised_pnl_gbp` and `restated_diff_gbp` — so the shipped UI shows "As reviewed" undated. The same section's Failure line ("if snapshot data cannot be loaded ... Restatement check unavailable.") names no API signal for that condition; the endpoint has no partial-failure field, so the shipped UI treats "no row carries the snapshot fields at all" as the trigger, which is an implementation choice the spec never made.

**Scope**
- Decide which side moves: drop `{snapshot_date}` from the spec, or add `snapshot_date` to the response and contract (the `monthly_pnl_snapshots` table already stores when a snapshot was taken)
- Define the failure signal for "Restatement check unavailable." in the spec and, if it needs an API field, the contract
- Update `reports.md`, and `reports_endpoints.md`/`openapi.yaml` if the API side moves, then close DEV-v9.7-ST04-01

**Acceptance Criteria**
- `reports.md` and `reports_endpoints.md` agree on whether the detail row is dated and on how the unavailable state is signalled
- The shipped UI matches the reconciled spec, or a follow-up is filed for the difference
- DEV-v9.7-ST04-01 is marked resolved with this item's ID

---

### BLG-QA-194 — Harden the UI-copy boundary lint against obfuscation-grade and cross-node phrase splits
**Priority:** P4 (Backlog)
**Type:** QA / Test Tooling
**Owner:** Frontend Specifications & UX Documentation Owner; QA & Testing Owner
**Source:** ST-07/EPIC-02, cycle 2026-09-23__release-v9.7 — agent-mediated DoQ review (second pass) — 2026-09-24
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`scripts/check_ui_copy_forbidden_phrases.py` (BLG-FE-183, ST-07) is a dependency-free tokeniser, not a full JS parser. The DoQ review found residual ways a forbidden §13.2 phrase can evade it. None occurs in `src/` today (a `@babel/parser` differential over 12,010 literals agrees) and all need deliberate obfuscation or an unusual layout, so they were accepted as non-blocking, but the gate is a compliance control and the list should be closed or consciously documented.

**Scope**
- Decode `\uXXXX`/`\xXX` escapes and HTML numeric/named entities (`&#160;`, `&#32;`, `&ensp;`) to their characters, and fold invisible characters (zero-width space, soft hyphen, non-breaking hyphen) before matching
- Extract JSX attribute strings that span lines
- Decide on cross-node splits (`'you ' + 'should'`, `You{' '}should`, `<b>Buy</b> now`, `['you','should'].join(' ')`): join adjacent literals, or document them as accepted limits alongside the existing docstring list
- Or replace the tokeniser with `@babel/parser` if a Node-based CI step is judged acceptable

**Acceptance Criteria**
- Each bypass above is either detected by a regression test or listed in the script docstring as an accepted limit with rationale
- The `@babel/parser` differential still reports no missed phrase hit over `src/`

---

### BLG-QA-195 — Add the Reports and Notifications pages to the axe accessibility scan, with light-theme contrast coverage
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner; Frontend Specifications & UX Documentation Owner
**Source:** PR #1802 review (agent-mediated DoQ), ST-03/ST-04/ST-05/ST-06/EPIC-02, cycle 2026-09-23__release-v9.7 — 2026-09-24
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`tests/e2e/accessibility-axe-scan.spec.js` scans only DashboardHome, Positions and TradePlan. EPIC-02 (v9.7) added new interactive markup to `Reports.js` — the "Restated" button (`aria-expanded`/`aria-controls`, whose target id does not exist while collapsed), an `aria-label` on a table cell, a `dl` detail row and amber/cyan text tones — and changed two Notifications headings. None of it has automated accessibility or light-theme contrast coverage, so the new elements' contrast and ARIA validity were reasoned about, not measured.

**Scope**
- Add the Reports page (Monthly tab with a restated month expanded, and the Tax Year tab with the restated-months notice) and the Notifications preferences/history pages to the axe scan
- Run the new scans in both dark and light themes, evaluating the settled state per the design-system motion-vs-contrast guideline
- Fix or file any findings

**Acceptance Criteria**
- The axe scan covers the Reports (both tabs, restated row expanded) and Notifications pages in dark and light themes
- Any serious/critical finding is fixed or has its own filed item

---

### BLG-SPEC-171 — Correct the PO-05 pre-assessment, roadmap and replay page spec: replay does not reuse IT-06's Alpaca mechanics, determinism wording, engine-versus-live rule divergences
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Strategy Rules & System Intent Owner; Frontend Specifications & UX Documentation Owner
**Source:** ST-01a/EPIC-01, cycle 2026-09-23__release-v9.7 — `docs/product/decisions/po05_replay_scope_confirmation.md` §1 (F1, F2, F4) and its independent review — 2026-09-24
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`po05_section13_preassessment.md`, `current_roadmap.md` (PO-05), `docs/specs/frontend/pages/replay_mode.md` §13 item 5 and the sealed `sprint_backlog.md` (ST-01b) say the replay "reuses IT-06's paper-trading mechanics". In code IT-06 is a real-time Alpaca mirror of position events that cannot replay history; the replay is built on the deterministic `strategy_engine.py` and makes no Alpaca call. The pre-assessment also states byte-identical output unconditionally, which does not hold for a `yfinance`-fed float pipeline (the scope note restates it as a fingerprint-checkable guarantee), and it assumes the replay applies the live rule set, whereas the engine differs from `strategy_rules.md` §7.2 (no breakeven floor, close-only ATR, stop evaluated before risk-off, entry-fee treatment). The scope note takes precedence for the build, but the source documents still carry the inaccurate wording, and the approved banner says "the current rules".

**Scope**
- The Strategy Rules & System Intent Owner acknowledges F1, F2 and F4 and decides the results-view caption wording (for example "Simulated with the strategy backtest engine's exit rules.")
- Correct the IT-06 reuse premise and the determinism wording in the pre-assessment and roadmap, and `replay_mode.md` §13 item 5 (the last in the frontend implementation change)

**Acceptance Criteria**
- No governed document other than sealed artefacts (which the scope note supersedes for the build) still states that PO-05 reuses IT-06's Alpaca paper-trading mechanics; the roadmap correction is routed through the Roadmap Rebalance Engine, which owns that file
- The determinism guarantee and the engine-versus-live rule divergences are stated consistently across the pre-assessment, the roadmap and the replay page spec

---

### BLG-QA-196 — Extend the axe accessibility scan to the new Replay page
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner; Frontend Specifications & UX Documentation Owner
**Source:** PR #1803 review (agent-mediated DoQ + PO), ST-01c/EPIC-01, cycle 2026-09-23__release-v9.7 — 2026-09-25
**Effort:** XS (<0.5d)
**Provisional-Target:** Backlog (no release scheduled; P3)
**Depends on:** BLG-QA-195 (same underlying gap — `tests/e2e/accessibility-axe-scan.spec.js` scans only a small, fixed set of pages)

**Problem**
`tests/e2e/accessibility-axe-scan.spec.js` still scans only DashboardHome, Positions and TradePlan (BLG-QA-195 already tracks adding Reports and Notifications). EPIC-01 (v9.7) added a new page, `src/pages/Replay.js`, with a tab-switched selector, a checkbox list, and a results table — none of it has automated accessibility or light-theme contrast coverage. The selector tabs are plain `<button>` elements with no `role="tablist"`/`role="tab"`/`aria-selected` (the same pattern `StrategyBenchmark.js`'s own mode toggle already uses, so this is not a new inconsistency, but it means an axe scan is the only practical way to catch a real accessibility regression here without inventing a new interaction pattern).

**Scope**
- Add the Replay page to the axe scan (Date Range mode, Trade Set mode with the checkbox list visible, and a populated result view) in both dark and light themes
- Fix or file any findings
- Consider covering this and BLG-QA-195 together in one pass, since both are the same underlying "scan is a fixed, small page list" gap

**Acceptance Criteria**
- The axe scan covers the Replay page (both selector modes, populated result) in dark and light themes
- Any serious/critical finding is fixed or has its own filed item

---

### BLG-QA-197 — reports-performance-tab.spec.js SC-REP-04a expects a signed "+£0.00" for zero Total P&L, contradicting the established zero-is-unsigned money convention
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** ST-03/EPIC-01, cycle 2026-09-28__release-v9.8 — discovered while running the existing Reports Playwright suite to confirm no regressions from a Monthly P&L Tax Year filter change — 2026-09-28
**Effort:** XS (<1h)
**Provisional-Target:** Backlog (no release scheduled; P3)

**Problem**
`tests/e2e/reports-performance-tab.spec.js`'s SC-REP-04a ("Total P&L shows £0.00 when no trades", line 281-284) asserts `page.getByText(/\+£0\.00/)` is visible when `metrics.totalPnL = 0`. This contradicts `src/lib/format.js`'s canonical `formatCurrency` convention (`design_system.md` §Number and Currency Formatting, v1.21): a value that rounds to zero is always rendered unsigned (`"£0.00"`, never `"+£0.00"` or `"−£0.00"`) — `formatCurrency`'s `signOf()` helper explicitly special-cases this. The Performance tab's Total P&L stat card correctly renders the unsigned `"£0.00"` for a zero value, so this test fails (element not found) — it appears to predate the "zero is unsigned" convention being formally established and was never updated to match. Confirmed pre-existing and unrelated to any specific feature work: fails identically before and after the ST-03/EPIC-01/v9.8 changes that surfaced it (`git stash` bisection against the pre-ST-03 commit reproduces the same single failure, in isolation, with no other test in the file affected).

**Scope**
- Change the assertion to `page.getByText('£0.00', { exact: true })` (or scope it to the specific Total P&L stat card testid if one exists) and drop the `+` from the regex

**Acceptance Criteria**
- SC-REP-04a passes and matches the same zero-is-unsigned convention already correctly asserted elsewhere (e.g. `tests/e2e/number-format-tables.spec.js` SC-NFT-01's "zero is unsigned" checks)

---

### BLG-QA-199 — size_position mutation-testing survivors: US-market and batch-sizing paths need their own mutation score confirmed
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA Lead
**Source:** ST-15 (BLG-QA-184, EPIC-03, cycle 2026-09-28__release-v9.8) — mutation-testing pilot found 119/246 `size_position` mutants survived — 2026-09-29
**Effort:** S (~0.5–1d)
**Provisional-Target:** Backlog (no release scheduled; P3)

**Problem**
The ST-15 mutation-testing pilot (`docs/testing/mutation_testing_pilot_sizing_and_stop_ratchet.md`) scoped its own test file to `size_position`'s UK-market path only (5 cases, adapted from `tests/golden_outputs.json`'s pre-ST-04 golden vectors). `size_position`'s US-market FX-rate branch and `size_batch_inv_vol` (a separate function in the same file, also mutated since `only_mutate` is file-granular) were never exercised by this pilot's own tests, contributing the bulk of its 119 survivors. `tests/test_signal_sizing.py` already covers `size_batch_inv_vol`'s behaviour with unit tests, but its own mutation score has not been separately measured.

**Scope**
- Extend the pilot's mutmut config (`backend/setup.cfg`, `backend/mutmut_pilot_tests/`) to also select `tests/test_signal_sizing.py`-equivalent cases (or a standalone-conftest-compatible port of them) and a US-market `size_position` case
- Re-run and record the updated `size_position`/`size_batch_inv_vol` mutation scores in the pilot doc

**Acceptance Criteria**
- `size_position`'s US-market path and `size_batch_inv_vol` each have at least one mutation-testing case in the pilot's test file
- Updated mutation score recorded in `docs/testing/mutation_testing_pilot_sizing_and_stop_ratchet.md`

---

### BLG-QA-200 — Ceiling/count-assertion tests in ST-11/ST-12 regression files don't read the source they claim to verify
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** PR #1845 review (Director of Quality persona), cycle 2026-09-28__release-v9.8 — 2026-09-29
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`tests/test_motion_timing_500ms_ceiling_regression.py`'s `test_max_combined_time_to_full_opacity_within_ceiling` methods (one per component class) and `tests/test_toast_notification_timing_regression.py`'s `test_exactly_8_error_call_sites_covered`/`test_nine_call_sites_covered_between_info_and_error_classes` all assert on hardcoded Python literals (e.g. `max_delay = 4 * 0.05; duration = 0.3; assert max_delay + duration <= 0.5`) rather than values extracted from the actual source file. The motion-timing file's own docstring claims these tests "independently recompute max(delay) + duration for each to confirm the 500ms ceiling itself, not just the presence of a particular string" — but they don't read the source at all, so if the sibling string-match test in the same class were ever weakened or removed, these "ceiling" tests would keep passing regardless of the real component's values. The toast-count tests are similarly tautological (asserting `len()` of a hardcoded list equals a hardcoded number).

**Scope**
- Rework the ceiling tests to parse the actual delay/duration values out of the regex match (or a dedicated extraction helper) rather than hardcoding them a second time
- Remove or repurpose the toast "count" tests, which currently verify nothing about the source code

**Acceptance Criteria**
- Each "ceiling" test fails if the actual source value regresses over 500ms, verified by temporarily editing a component's duration value in a scratch branch and confirming the test catches it without relying on the sibling string-match test
- No test in either file asserts purely on hardcoded literals unrelated to the source file's actual content

---

### BLG-QA-201 — mutmut_pilot_tests/test_pilot.py shares mutable database mock state across tests with no reset — order-dependency risk
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA Lead
**Source:** PR #1845 review (Director of Quality persona), cycle 2026-09-28__release-v9.8 — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`backend/mutmut_pilot_tests/test_pilot.py`'s `TestSizePositionGoldenVectors` tests set `database.get_portfolio.return_value`, `database.get_latest_snapshot.return_value`, and `database.get_settings.return_value` directly on the session-scoped database stub module (`backend/mutmut_pilot_tests/conftest.py`) with no fixture-based reset/teardown between tests. Every current test happens to set all three before use, so there is no live failure today, but a future test added to this file that forgets to set one of the three would silently inherit a stale `return_value` left by whichever test last set it, rather than failing loudly or getting a fresh mock — an order-dependency trap. The sibling `_no_heat_impact` fixture in the same file uses `unittest.mock.patch.object(...)` correctly (with automatic teardown); the three database stub assignments don't follow the same pattern.

**Scope**
- Convert the three `database.*` mock assignments to a fixture using `unittest.mock.patch.object` (or `reset_mock()`/an autouse fixture) so each test starts from a clean, unconfigured mock

**Acceptance Criteria**
- Each test in `TestSizePositionGoldenVectors` is independently runnable in isolation and in any order with identical results
- A test added without configuring all three database mocks fails loudly (AttributeError/None) rather than silently inheriting a prior test's stale `return_value`

---

### BLG-QA-202 — backend/setup.cfg's mutmut comment references a leaked sandbox-local /tmp path
**Priority:** P3 (Low)
**Type:** QA / Test Tooling
**Owner:** QA Lead
**Source:** PR #1845 review (Director of Quality persona), cycle 2026-09-28__release-v9.8 — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`backend/setup.cfg`'s `[mutmut]` section header comment says to invoke via `/tmp/mutmut_pilot_venv/venv/bin/python3 -m mutmut run` — a session-specific temporary path from the original pilot's own sandbox investigation (used to temporarily relocate `backend/.venv` out of the way) that will not exist for anyone else reproducing the pilot. `docs/testing/mutation_testing_pilot_sizing_and_stop_ratchet.md`'s own "Reproducing this pilot" section correctly uses a generic `python3 -m pip install mutmut` / `python3 -m mutmut run` with no such path, so the `setup.cfg` comment is now the only place with the stale reference.

**Scope**
- Correct `backend/setup.cfg`'s comment to reference the backend venv (e.g. `backend/.venv/bin/python3`) or simply match the doc's generic invocation, dropping the `/tmp` path

**Acceptance Criteria**
- `backend/setup.cfg` contains no sandbox-specific `/tmp` path

---

### BLG-QA-203 — GET /reports/tax-year returns HTTP 500 against its own test fixture
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** Head of Engineering; Director of Quality
**Source:** ST-17/EPIC-04, cycle 2026-09-28__release-v9.8 — discovered incidentally while running `tests/test_api_contracts.py` to check for regressions from ST-17's `health_service.py` change — 2026-09-29
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`tests/test_api_contracts.py::TestReportsEndpoints::test_get_tax_year_report_returns_ok` fails on the current `main` tip when run in isolation or as part of just `test_api_contracts.py`: `GET /reports/tax-year` returns HTTP 500 (`{"status":"error","message":"Internal server error"}`) instead of the expected 200, with the traceback originating in `backend/main.py` line 887 (`get_tax_year_report_endpoint`). Confirmed pre-existing and unrelated to any in-flight EPIC-04 change (reproduces identically with those changes stashed out) — not a regression introduced this cycle, but a live, currently-red test in some run configurations. **Test-order dependency found:** the same test *passes* when the full suite is run (`pytest tests/ -q --ignore=tests/e2e`, 1941 passed / 0 failed) — some other test file, when collected/run first, leaves shared state (likely module-level or in-memory) that this test's own fixture does not set up on its own. This makes it either an order-dependent test-isolation bug (the real defect) or a genuinely broken endpoint that happens to be masked by leftover state from another test — root-causing which is this item's first step.

**Scope**
- Determine whether `GET /reports/tax-year` is genuinely broken (masked by cross-test state pollution) or the test's own fixture is incomplete/order-dependent (bisect which other test file's execution makes it pass, e.g. `pytest tests/test_api_contracts.py tests/<suspect>.py -q`)
- Root-cause the 500 (`backend/main.py:887`, `get_tax_year_report_endpoint`) and fix the underlying defect, or fix the test fixture/isolation if the endpoint's behaviour is actually correct and only the test's own setup is incomplete
- Confirm `tests/test_api_contracts.py::TestReportsEndpoints::test_get_tax_year_report_returns_ok` passes **both** in isolation and as part of the full suite

**Acceptance Criteria**
- `backend/.venv/bin/python3 -m pytest tests/test_api_contracts.py::TestReportsEndpoints::test_get_tax_year_report_returns_ok` passes when run alone
- `backend/.venv/bin/python3 -m pytest tests/ -q --ignore=tests/e2e` continues to pass (confirms the fix didn't just move the order-dependency elsewhere)
- Root cause (genuine endpoint defect vs. test-isolation gap) is documented in the fix's commit message or a linked deviation record

---

### BLG-FE-192 — RecentTradesWidget icon-background badge uses two-way (>=0) colour logic for zero P&L, inconsistent with the neutral-tone convention
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-01/EPIC-01, formatting-helper migration, cycle 2026-09-28__release-v9.8 — 2026-09-28
**Effort:** XS (<1h)
**Provisional-Target:** Backlog (no release scheduled; P3)

**Problem**
In `src/components/dashboard/widgets/RecentTradesWidget.js` (line 36-38), the trade-row icon badge background/icon colour uses `(trade.pnl || 0) >= 0 ? "bg-emerald-500/20 text-emerald-400" : "bg-rose-500/20 text-rose-400"` — a two-way threshold that colours an exact-zero P&L trade the same green as a genuine winner. This is the same "zero-P&L should render neutral, not green" bug pattern already fixed at the adjacent P&L text a few lines below (line 48, now a three-way `> 0` / `< 0` / neutral split) and fixed across several other files in the ST-01 formatting migration (v9.8). This specific site isn't a `toFixed()`/`toLocaleString()` call site, so it fell outside that migration's scope and was left unmigrated by design.

**Scope**
- Change the badge's background/icon-colour condition to the same three-way split already used for the adjacent P&L text (`trade.pnl > 0` emerald / `trade.pnl < 0` rose / else neutral slate)

**Acceptance Criteria**
- A trade with `pnl === 0` renders the icon badge in a neutral (non-green, non-rose) colour, consistent with the adjacent P&L text's own zero-P&L treatment
- Winning (`pnl > 0`) and losing (`pnl < 0`) trades retain their existing emerald/rose badge colours

---

### BLG-FE-193 — Stop-loss cell ATR/multiplier/recalculation-source display; live-event explainer tooltip
**Priority:** P2 (High)
**Type:** Frontend / UX Trust & Transparency
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Source:** `IDEA-head-of-ux-20260930-01`, `IDEA-head-of-ux-20260930-02` (consolidated, `IW-20260930-01`), roadmap rebalance `2026-09-30__scheduled`
**Gate criteria:** `BLG-BE-135`'s `atr`/active-multiplier/`stop_calculated_at` fields shipped and available on `GET /positions`
**Effort:** M (~4-6 days)
**Provisional-Target:** TBD

**Problem**
User-reported loss of confidence in the displayed stop-loss for open positions: the stop-loss cell (`src/pages/Positions.js`, `PositionCard.js`) shows only the final Init/Trailing prices — no ATR, no multiplier, no source event — so the user cannot independently verify a displayed stop. `strategy_rules.md` §5 (Initial stop calculation) states its purpose is "to make downside risk visible... to reduce reactive decision-making"; a stop the user cannot verify produces the opposite effect. Separately, `TrailingStopExplainerIcon.js`'s tooltip states "ATR is recalculated daily (14-day period)," but the live system recalculates on every `GET /positions` page load as well as nightly — the copy is a hardcoded claim, not a reflection of what actually happened for the row it sits next to, undermining `strategy_rules.md` §3's "decision support only" trust model independent of whether the underlying number is correct.

**Scope**
- Add ATR value, the active multiplier (2× profitable / 5× losing, per §7.2), and a recalculation source line to the stop-loss cell/tooltip, checkable against the §5/§7.2 formula without leaving the page
- Source the explainer tooltip copy from the row's actual last-recalculation event/timestamp (e.g. "Recalculated when you opened this page at 09:14" / "Recalculated by the nightly job at 22:30 UTC") instead of a hardcoded cadence claim
- A first increment (removing the false "daily" claim from the tooltip) may ship independently if full live-event sourcing is not yet available

**Acceptance Criteria**
- Stop-loss cell/tooltip displays ATR value, active multiplier, and calculation source, checkable against the documented formula without leaving the page
- Explainer tooltip copy reflects the actual last-recalculation event (on-load timestamp or nightly-job timestamp) rather than a hardcoded "daily" claim
- Depends on `BLG-BE-135` shipping first — do not begin implementation until the backend fields are available on `GET /positions`

---

### BLG-GOV-350 — Five near-duplicate "AI adoption window" gate-criteria texts should be one canonical shared reference
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Idea intake `IW-20260928-01` (`IDEA-head-of-specs-20260928-01`), roadmap rebalance `2026-09-28__scheduled` STEP 3.1/4 — 2026-09-28
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`BLG-FEAT-59`, `BLG-FEAT-60`, `BLG-FE-84`, `BLG-FEAT-63`, and `BLG-OPS-88` each carry their own copy of the same "AI adoption window verification due at the 2026-09-24 AI feature usage review (BLG-GOV-74 cadence)" gate text, each with a slightly different owner clause. This is the same class of drift risk the Candidate/Item Backlog-Status Verification Subroutine (`BLG-GOV-324`) was extracted to prevent for procedure text — here it is gate-criteria prose, so a future update to the review's schedule or scope must be hand-propagated across 5 separate items or silently drift.

**Scope**
- Define one canonical gate reference (e.g. a named gate ID in `current_roadmap.md` §6 or a shared backlog convention) that all 5 items point to by reference
- Update the 5 items' `**Gate criteria:**` fields to cite the canonical reference instead of restating it

**Acceptance Criteria**
- A single canonical statement of the 2026-09-24 AI adoption review gate exists
- All 5 affected items reference it rather than restating it

---

### BLG-SPEC-173 — Column provenance annotations in data_model.md (user-entered / derived / system-stamped)
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Data Model & Domain Schema Owner
**Source:** `IDEA-data-model-20260919-02` (window `IW-20260919-01`), re-evaluated and cleared at roadmap rebalance `2026-09-28__scheduled` STEP 4.0 — gate (`BLG-SPEC-150` disposition) shipped v9.7 — 2026-09-28
**Effort:** S (~1d)
**Provisional-Target:** TBD

**Problem**
`data_model.md` documents each column's name, type, and nullability but not its provenance — whether a field is user-entered, derived/computed, or system-stamped. Analytics and future migration work has no canonical way to know which fields are safe to recompute versus which represent an authoritative user input, short of reading the originating service code each time. This was previously blocked on `BLG-SPEC-150`'s disposition of 4 orphaned `positions` columns (annotating provenance before that triage would have documented columns about to be dropped) — that triage shipped v9.7 (ST-25), clearing the dependency.

**Scope**
- Add a provenance column/tag (user-entered / derived / system-stamped) to each table's field documentation in `data_model.md`
- Start with `positions` and `trade_plans` (highest-traffic tables); expand to others opportunistically

**Acceptance Criteria**
- `positions` and `trade_plans` tables in `data_model.md` carry a provenance annotation per field
- No field is left ambiguous between user-entered and derived without an explicit note

---

### BLG-SPEC-174 — No adoption/usage counter for the AI-assisted monthly P&L narrative feature
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Financial Reporting & Records Owner
**Source:** Idea intake `IW-20260928-01` (`IDEA-financial-reporting-20260928-01`), roadmap rebalance `2026-09-28__scheduled` STEP 4 — 2026-09-28
**Effort:** S (~1d)
**Provisional-Target:** TBD

**Problem**
`BLG-FEAT-59`'s gate (AI adoption window verification, part of the `BLG-GOV-351` cluster above) requires the Financial Reporting & Records Owner to "confirm usage patterns have stabilised," but no mechanism logs how often the AI-assisted monthly P&L narrative feature is actually used — every prior review of this gate has relied on ad hoc estimation rather than a real count.

**Scope**
- Add a lightweight usage/adoption counter (e.g. a log row or counter column) recorded whenever the AI-assisted monthly P&L narrative is generated
- Document the field in `data_model.md` and cite it as the authoritative source for future `BLG-FEAT-59`-style adoption reviews

**Acceptance Criteria**
- A real, queryable count of AI-assisted monthly P&L narrative generations exists
- The `BLG-FEAT-59` gate criteria is updated to cite this count as its evidence source instead of an estimate

---

### BLG-BE-131 — GET /reports/monthly-pnl's new `year` param has no bounds check, unlike its sibling GET /reports/tax-year
**Priority:** P4 (Trivial)
**Type:** Backend Debt
**Owner:** Backend Engineering Patterns Owner
**Source:** PR #1843 review (agent-mediated Director of Quality), EPIC-01/ST-03, cycle 2026-09-28__release-v9.8 — 2026-09-28
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`GET /reports/monthly-pnl?year=<n>` (added ST-03, EPIC-01, v9.8, BLG-FE-190) passes `year` straight into `date(year, 4, 6)` inside `get_monthly_pnl_report()` with no numeric bounds check, unlike its sibling `GET /reports/tax-year`, whose handler explicitly validates `year < 1000 or year > 9999` before calling the service layer. Confirmed live: `GET /reports/monthly-pnl?year=0` returns `404 {"message": "year must be in 1..9999, not 0"}` — a raw Python `ValueError` from `date()` construction, caught by the endpoint's generic `except ValueError` branch and returned as an ambiguous 404 with a leaked internal message, instead of a clean `400` matching the sibling endpoint's convention. Not reachable via the current UI (the frontend's year dropdown is always bounded `2020..currentTaxYear`), so not user-facing today, but it is a defensive-validation gap and an inconsistency between two sibling endpoints that should be closed.

**Scope**
- Add the same `year < 1000 or year > 9999` (or equivalent) bounds check to `get_monthly_pnl_endpoint` in `backend/main.py`, returning `400` with a clear message, before calling `get_monthly_pnl_report(year=year)`

**Acceptance Criteria**
- `GET /reports/monthly-pnl?year=0` (and other out-of-range values) returns a clean `400` with a validation message, not a `404` with a raw Python error string
- Regression test added confirming the bounds check, mirroring the existing `GET /reports/tax-year` bounds-check test pattern

---

### BLG-OPS-171 — Confirm the stale-staging-deploy alert fires on a real stale-staging condition
**Priority:** P3 (Low)
**Type:** Operations / QA
**Owner:** Infrastructure & Operations Owner; Director of Quality
**Source:** ST-17/EPIC-04 (BLG-OPS-169), cycle 2026-09-28__release-v9.8 — staging-only AC deferred at PR-open time per sprint_backlog.md ST-17 Notes — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-17 (BLG-OPS-169) added a stale-deploy check to `staging-smoke-test.yml` (compares `GET /health/detailed`'s `deployed_commit_sha` against the merged commit on `main`) and unit-tested the comparison logic in isolation (`tests/test_staging_smoke_test.py`), but confirming the check actually produces a visible failure/alert against a *real* stale-staging condition cannot be reproduced in CI or this sandbox — there is no way to genuinely desynchronize a real staging deploy from `main` without either withholding a real deploy or reverting staging to an old commit, both of which require live Render/GitHub Actions access this environment does not have.

**Scope**
- Deliberately let (or force) staging fall behind `main` by one commit (e.g. temporarily pause auto-deploy, or manually redeploy an older commit via the Render dashboard)
- Confirm the next `staging-smoke-test.yml` scheduled run (or a manual `workflow_dispatch`) reports the `STALE STAGING DEPLOY` failure and the Telegram alert fires
- Restore staging to the current `main` commit afterward and confirm the check reports a pass

**Acceptance Criteria**
- A recorded failing CI run (run URL) showing the `STALE STAGING DEPLOY` message for a real, deliberately-introduced staging/main divergence
- A recorded passing run (run URL) after staging is restored to the current `main` commit

---

### BLG-GOV-352 — Rebalance diagnostic tallies (STEP 2.4/7.1/7.2) are recomputed by hand each cycle
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** Idea intake `IW-20260928-01` (`IDEA-infra-ops-20260928-02`), roadmap rebalance `2026-09-28__scheduled` STEP 4 — 2026-09-28
**Effort:** M (~2d)
**Provisional-Target:** TBD

**Problem**
`roadmap_prompt.md` STEP 2.4 (Product Value Ratio), STEP 7.1 (Skill-Silo Alert), and STEP 7.2 (Cross-Role Workload Balance) each require manually re-reading several `docs/product/changelog.md`/`sprint_backlog.md` files per rebalance and hand-tallying U/G/D/P tags or `**Owner:**` field text. This is exactly the transcription-variance risk STEP 2.4's own "read the tag, don't re-derive it" rule already flags for the U/G/D/P classification itself — the tallying step downstream of reading the tags carries the same risk and is not mechanized.

**Scope**
- Write `scripts/compute_rebalance_diagnostics.py` that reads the relevant changelog/sprint_backlog files for a given cycle window and outputs the STEP 2.4/7.1/7.2 tallies
- Wire it as an optional-but-recommended step in `roadmap_prompt.md`'s own STEP 2.4/7.1/7.2 instructions (advisory — a routine without script access must still be able to perform the tally manually)

**Acceptance Criteria**
- The script reproduces this cycle's STEP 2.4 (14/36/104/4 of 158) and STEP 7.1 (85.7% rolling average) figures exactly, given the same input files
- `roadmap_prompt.md` references the script as an optional acceleration, not a hard dependency

---

### BLG-BE-132 — gemini_service.py's daily-cost Telegram alert still uses a hardcoded timeout, not utils.upstream_call
**Priority:** P4 (Trivial)
**Type:** Backend / Reliability
**Owner:** Backend Engineering Patterns Owner
**Source:** PR #1844 review (agent-mediated Director of Quality), EPIC-02/ST-07, cycle 2026-09-28__release-v9.8 — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`backend/services/gemini_service.py:394` (`check_and_alert_daily_cost`) calls `urllib.request.urlopen(url, timeout=10)` to send a Telegram alert. ST-07 (BLG-BE-128, EPIC-02, v9.8) added a `"telegram"` provider entry to `backend/utils/upstream_call.py` (`get_timeout("telegram")` == 10) and migrated the two other Telegram call sites (`si05_digest_service.py`, `ai_endpoint_anomaly_service.py`) to it, but this third site was never on BLG-BE-128's original list (filed 2026-09-22) and so was out of ST-07's scope.

**Scope**
- Replace the hardcoded `timeout=10` with `get_timeout("telegram")`, config-only (no retry-shape change), same treatment ST-07 gave the other two Telegram call sites

**Acceptance Criteria**
- `gemini_service.py`'s Telegram alert timeout is sourced from `get_timeout("telegram")`; no behaviour change to the existing alert logic

---

### BLG-BE-133 — utils/pricing.py's ATR-fallback Yahoo Finance call still uses a hardcoded timeout, not utils.upstream_call
**Priority:** P4 (Trivial)
**Type:** Backend / Reliability
**Owner:** Backend Engineering Patterns Owner
**Source:** PR #1844 review (agent-mediated Director of Quality), EPIC-02/ST-07, cycle 2026-09-28__release-v9.8 — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`backend/utils/pricing.py:403` (an ATR-fallback function that queries Yahoo Finance directly when Alpaca ATR data is unavailable) calls `requests.get(url, params=params, headers=headers, timeout=10)`. This is a different function than the one ST-13 (BLG-BE-122, v9.6) already migrated in the same file — this ATR-fallback path was missed by both ST-13's original migration and ST-07's (BLG-BE-128) follow-up list.

**Scope**
- Replace the hardcoded `timeout=10` with `get_timeout("yfinance")` (matching value, config-only, no retry-shape change)

**Acceptance Criteria**
- The ATR-fallback Yahoo Finance call's timeout is sourced from `get_timeout("yfinance")`; no behaviour change to the existing fallback logic

---

### BLG-BE-134 — alpaca_paper_sync_service.py's 3 Alpaca calls still use hardcoded timeouts, not utils.upstream_call
**Priority:** P4 (Trivial)
**Type:** Backend / Reliability
**Owner:** Backend Engineering Patterns Owner
**Source:** PR #1844 review (agent-mediated Director of Quality), EPIC-02/ST-07, cycle 2026-09-28__release-v9.8 — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`backend/services/alpaca_paper_sync_service.py` (IT-06, paper-trading position mirroring) has 3 call sites — lines 68 (`requests.post`), 115 (`requests.delete`), 158 (`requests.get`) — each hardcoding `timeout=10` against the Alpaca API, matching the `"alpaca"` provider value ST-13 (BLG-BE-122, v9.6) already configured in `utils/upstream_call.py`. This file/service was never on BLG-BE-128's original list, likely because it postdates that list (IT-06 tag suggests a later initiative).

**Scope**
- Replace all 3 hardcoded `timeout=10` literals with `get_timeout("alpaca")`, config-only (no retry-shape change) — the file already imports `from utils.retry import retry_with_backoff`, so check whether any of the 3 call sites already use retry wrapping before deciding whether a retry-shape change is in scope or should stay a pure timeout substitution like `BLG-BE-132`/`BLG-BE-133` above

**Acceptance Criteria**
- All 3 Alpaca call sites in `alpaca_paper_sync_service.py` source their timeout from `get_timeout("alpaca")`; no behaviour change to existing sync/retry logic

---

### BLG-BE-135 — Consolidate 4 duplicate ATR implementations; persist stop/ATR recalculation timestamp; expose atr/multiplier/timestamp on GET /positions
**Priority:** P2 (High)
**Type:** Backend / Data Integrity
**Owner:** Backend Engineering Patterns Owner; Head of Engineering
**Source:** `IDEA-head-of-engineering-20260930-01`, `IDEA-head-of-engineering-20260930-02` (consolidated, `IW-20260930-01`), roadmap rebalance `2026-09-30__scheduled`
**Effort:** L (~6-10 days)
**Provisional-Target:** TBD

**Problem**
ATR is independently implemented in at least 4 places (`backend/utils/pricing.py::calculate_atr`, `backend/services/strategy_engine.py::compute_atr`, `backend/services/screener_engine.py::compute_atr`, `backend/database.py::compute_atr_simple`), plus a 5th, unwired dead copy in `backend/position_manager.py` never imported by `main.py` or any live service — if these diverge, exposing a raw ATR value in the UI (`BLG-FE-193`) would surface the inconsistency directly to the user rather than resolving it. Separately, no `atr_calculated_at`/`stop_calculated_at` column or field exists anywhere in the system, though a refresh-on-login (`position_service.py::get_positions_with_prices`, recalculated on every `GET /positions`) and a nightly backstop (`.github/workflows/nightly-stop-update.yml`) both already exist in code — neither is visible or timestamped anywhere the user can see. `strategy_rules.md` §7.1 states "ATR is recalculated daily," while `position_endpoints.md` line 147 documents the stop as "always present and non-zero after the first nightly update" — both describe a nightly-only cadence that doesn't match the actual on-load + nightly behaviour. `strategy_rules.md` §12.3 requires strategy parameters "applied consistently across backtests, live logic, and documentation" — §12.3 already carries one documented, tested exception for `position_manager.py`'s backtest path (the breakeven-floor divergence, v9.5); a second, undocumented divergence source (independent ATR math) in the same file is a materially different, unaccepted risk.

**Scope**
- Designate one canonical ATR implementation (the live-path function backing `calculate_trailing_stop`'s callers); have the other live call sites use it; remove the dead `position_manager.py` copy, or explicitly document why it is exempt if intentionally kept as a standalone backtest tool
- Add a `stop_calculated_at` (and reuse for `atr`) timestamp column, written alongside `current_stop`/`atr` in both the on-load recompute path and the nightly job
- Expose `atr`, the active multiplier, and the timestamp on `GET /positions`; document in `position_endpoints.md` + `openapi.yaml` in the same commit
- Raise a mid-implementation spec query (per Head of Engineering charter) to the Strategy Rules & System Intent Owner: either `strategy_rules.md` §7.1 and `position_endpoints.md` are updated to describe the actual on-load + nightly cadence, or the implementation is deliberately constrained to nightly-only recompute to match the documented "daily" cadence — this is a spec decision, not an engineering judgment call

**Acceptance Criteria**
- ATR implementation count reduced from 4 (5 including dead code) to 1 canonical source across `backend/utils/pricing.py`, `strategy_engine.py`, `screener_engine.py`, `database.py`; `position_manager.py`'s dead copy removed or explicitly documented as an exempt standalone tool
- `stop_calculated_at`/`atr_calculated_at` persisted alongside `current_stop`/`atr` in both the on-load recompute path and the nightly job
- `atr`, active multiplier, and the timestamp exposed on `GET /positions` and documented in `position_endpoints.md` + `openapi.yaml` (same commit)
- Spec query raised and resolved; `strategy_rules.md` §7.1 and `position_endpoints.md` updated to reflect the actual recompute cadence (or engineering constrained to match the documented cadence, per the Owner's ruling)

---

### BLG-GOV-353 — role_share_history.md has no governance-authorized home under claude/roadmap/
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** ST-33 (BLG-GOV-341), EPIC-06, cycle 2026-09-28__release-v9.8 — 2026-09-30
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-33's AC ("persist STEP 7.2 role-share tallies as a structured history file") assumes the resulting file lives at `claude/roadmap/role_share_history.md`, mirroring the existing `product_value_ratio_history.md` precedent in the same directory. But `execution_prompt.md` §7's write-scope restriction only carves out `claude/roadmap/workforce_capacity.md` (BLG-GOV-337) for direct engine writes to `claude/roadmap/*`, and that ruling explicitly states it extends to no other roadmap file. Sprint Execution has no standing authority to create a new file at that path without an explicit `sprint_backlog.md` Notes-field authorization, which ST-33's sealed Notes field does not provide (PMO Lead confirmed this reading in-session via `AskUserQuestion`, 2026-09-30). As a result, ST-33 delivered the backfilled history data and computation script at a cycle-scoped interim location (`claude/cycles/2026-09-28__release-v9.8/role_share_history.md`) rather than the canonical roadmap location, and `roadmap_prompt.md` §7.2 was **not** updated to read from it — the AC's second half ("STEP 7.2 reads the file instead of re-parsing Owner fields") remains outstanding.

**Scope**
- Roadmap Engine (or Head of Specs Team acting directly) formally authorises and creates `claude/roadmap/role_share_history.md`, migrating the interim data from `claude/cycles/2026-09-28__release-v9.8/role_share_history.md`
- Update `roadmap_prompt.md` §7.2 to read the structured file instead of re-parsing `sprint_backlog.md` Owner fields at each rebalance (applying the full CLAUDE.md §6 governance-file-edit checklist for the version bump)
- Confirm whether `product_value_ratio_history.md`'s own original creation had an equivalent explicit authorisation on record, to establish the precedent cleanly for this and future `claude/roadmap/` additions

**Acceptance Criteria**
- `claude/roadmap/role_share_history.md` exists, seeded with the 3-cycle backfill already computed by `scripts/compute_role_share_history.py`
- `roadmap_prompt.md` §7.2 reads from it instead of re-deriving the tally by hand
- The interim `claude/cycles/2026-09-28__release-v9.8/role_share_history.md` file is either superseded/removed or left as a dated historical snapshot, at the implementer's discretion

---

### BLG-GOV-354 — .claude_current_state.json's execution_state_path points to the prior cycle, not the active one
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** ST-33, EPIC-06, cycle 2026-09-28__release-v9.8 — 2026-09-30
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`.claude_current_state.json`'s `active_cycle` field correctly reads `2026-09-28__release-v9.8`, but its `execution_state_path` field still reads `claude/cycles/2026-09-23__release-v9.7/execution_state.json` — the prior cycle's file, not `claude/cycles/2026-09-28__release-v9.8/execution_state.json` (which exists and is the file Sprint Execution has actually been reading/writing all cycle via its own resumability model). Nothing appears to have updated this pointer at cycle transition. A tool or reader that trusts this field rather than deriving the path from `active_cycle` would silently read/write the wrong cycle's execution state.

**Scope**
- Update `.claude_current_state.json`'s `execution_state_path` to match the active cycle
- Check whether any script or governance prompt STEP actually reads this field (vs. deriving the path from `active_cycle` directly, as Sprint Execution appears to do) — if something does trust it, this is a live correctness bug, not just stale metadata
- Confirm whether the roadmap/sprint-planning engine's cycle-transition steps are supposed to update this field and, if so, why it didn't happen at the `2026-09-28__release-v9.8` transition

**Acceptance Criteria**
- `execution_state_path` matches `active_cycle`'s own `execution_state.json`
- Root cause of the missed update at cycle transition is identified and, if a real reader depends on it, fixed so it can't drift again

---

### BLG-GOV-355 — product_value_ratio_history.md's effort-weighted PVR column has no governance-authorized home
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** ST-31 (BLG-GOV-339), EPIC-06, cycle 2026-09-28__release-v9.8 — 2026-09-30
**Effort:** S (~0.5-1d)
**Provisional-Target:** TBD

**Problem**
`BLG-GOV-339`'s own Scope text names `claude/roadmap/product_value_ratio_history.md` directly as the intended target for a new effort-weighted PVR column ("Report an effort-weighted PVR alongside the story-count PVR in `product_value_ratio_history.md`"). But `execution_prompt.md` §7's write-scope restriction only carves out `claude/roadmap/workforce_capacity.md` (BLG-GOV-337) for direct engine writes to `claude/roadmap/*`, and `sprint_backlog.md`'s ST-31 Notes field carries no per-file authorisation ("None"). This is the third instance of the same write-scope gap this sprint (see `BLG-GOV-353`, ST-33/role-share history; the runway forecast for ST-32/`BLG-GOV-340` avoided it by using `metrics_definitions.md` instead). Resolved for ST-31 (`ESC-EXEC-20260930-03`) by defining and backfilling the effort-weighted PVR metric in `docs/specs/metrics_definitions.md` Appendix F instead, independently cross-validated against `product_value_ratio_history.md`'s own recorded U/G/D/P counts (4 of 5 windows matched exactly). The canonical file itself was not touched.

**Scope**
- Roadmap Engine (or Head of Specs Team acting directly) formally authorises and performs the `product_value_ratio_history.md` append: a new effort-weighted PVR column added to the `## History` table, backfilled from the 5-window data already computed and cross-validated in `metrics_definitions.md` Appendix F via `scripts/compute_effort_weighted_pvr.py`
- Going forward, `roadmap_prompt.md` STEP 2.4 appends both readings each rebalance (subject to the separate Head of Specs Team + Product Owner sign-off `BLG-GOV-339` itself already requires before any STEP 2.4 behaviour change)
- **Secondary recommendation:** this is the third near-identical `claude/roadmap/*` write-scope conflict raised in one sprint (`BLG-GOV-353`, this item, and the runway forecast that avoided it). Consider whether `execution_prompt.md` §7 should gain a standing, lighter-weight escalation path for "extend an existing, already-authorised `claude/roadmap/*` file with a new column/section the file's own owning engine will consume" — distinct from the heavier bar appropriate to creating a brand-new file at that path — rather than re-litigating this per-story each time it recurs

**Acceptance Criteria**
- `product_value_ratio_history.md`'s `## History` table carries the effort-weighted PVR reading alongside the existing story-count PVR, backfilled for the same 5 windows already computed in `metrics_definitions.md` Appendix F
- `roadmap_prompt.md` STEP 2.4 is updated to append both readings at future rebalances, contingent on `BLG-GOV-339`'s own required sign-off for any STEP 2.4 behaviour change

---

### BLG-SPEC-177 — openapi.yaml's new TradePlan schema declares the stale 3-value status enum
**Priority:** P3 (Low)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner
**Source:** PR #1847 agent-mediated review (Director of Quality finding), EPIC-05/ST-23, cycle 2026-09-28__release-v9.8 — 2026-09-30
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Note on numbering:** PR #1847 (EPIC-05, not yet merged) already claims `BLG-SPEC-175`/`176` on its own branch — this item is numbered `177` deliberately, ahead of what is visible on this branch's own `backlog.md`, to avoid a collision when the two branches merge (see CLAUDE.md §8's identical-text-masks-differing-semantics / cross-EPIC collision guidance). Confirm this number is still free at merge time.

**Problem**
`docs/reference/openapi.yaml`'s new `TradePlan` schema (added by ST-23, EPIC-05, v9.8, `BLG-SPEC-153`, referenced by `POST /trade-plans` 201) declares `status: { type: string, enum: [draft, active, closed] }` — the stale 3-value list. In the very same PR, ST-24 (`BLG-SPEC-154`) corrects `data_model.md`'s DS-04 CHECK constraint to the live 7-value list (`draft, research_pending, research_complete, entry_conditions_set, active, closed, abandoned`) and adds DS-21 documenting exactly this migration. The new schema directly contradicts its own PR-sibling's fix. Not a live bug today — `POST /trade-plans` always creates with `status="draft"` (confirmed in `backend/routers/trade_plans.py`) — but `TradePlan` is a general-purpose, reusable schema name; a future consumer reusing it for a GET response, a codegen client, or a contract test would be misled into thinking only 3 statuses are ever valid.

**Scope**
- Update `TradePlan.status`'s enum in `openapi.yaml` to the same 7-value list DS-21 documents
- Confirm no example/test relies on the narrower 3-value assumption

**Acceptance Criteria**
- `TradePlan.status` enum matches `data_model.md` DS-04's live CHECK constraint exactly (7 values)
- `scripts/check_openapi_drift.py` and `scripts/check_contract_example_freshness.py` both still pass

---

### BLG-OPS-172 — POST /ai/check-daily-cost has no de-duplication guard against a double-submitted Telegram alert
**Priority:** P4 (Trivial)
**Type:** Operations / Reliability
**Owner:** Infrastructure & Operations Owner
**Source:** ST-20/EPIC-05 (BLG-API-04), cycle 2026-09-28__release-v9.8 — idempotency/double-submit documentation sweep — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`docs/specs/api_contracts/ai_endpoints.md`'s `POST /ai/check-daily-cost` sends a Telegram alert whenever `threshold_exceeded` is true, with no already-alerted-today guard. A double-submitted or accidentally-repeated call within the same day re-evaluates the same threshold and can send a duplicate alert.

**Scope**
- Add a per-day "already alerted" guard (e.g. a marker row, or checking whether an alert was already sent today before sending another)

**Acceptance Criteria**
- A second call on the same UTC day, after an alert has already been sent for a still-exceeded threshold, does not send a second Telegram message

---

### BLG-OPS-173 — POST /ai/check-endpoint-anomalies has no de-duplication guard against a double-submitted Telegram alert
**Priority:** P4 (Trivial)
**Type:** Operations / Reliability
**Owner:** Infrastructure & Operations Owner
**Source:** ST-20/EPIC-05 (BLG-API-04), cycle 2026-09-28__release-v9.8 — idempotency/double-submit documentation sweep — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`docs/specs/api_contracts/ai_endpoints.md`'s `POST /ai/check-endpoint-anomalies` sends a Telegram alert whenever `firing_count > 0`, with no already-alerted guard. A double-submitted or accidentally-repeated call while the same anomaly is still firing re-sends the summarising alert.

**Scope**
- Add an already-alerted-for-this-firing-window guard (e.g. a marker row keyed by the check window, or suppressing a repeat alert within a short cooldown)

**Acceptance Criteria**
- A second call within the same firing window, with the same anomalies still firing, does not send a second Telegram message

---

### BLG-OPS-174 — POST /price-alerts has no de-duplication guard against a double-submitted duplicate alert
**Priority:** P4 (Trivial)
**Type:** Operations / Reliability
**Owner:** Infrastructure & Operations Owner
**Source:** ST-20/EPIC-05 (BLG-API-04), cycle 2026-09-28__release-v9.8 — idempotency/double-submit documentation sweep — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`docs/specs/api_contracts/alerts_endpoints.md`'s `POST /price-alerts` has no uniqueness guard on `(ticker, condition, threshold_price)`. A double-submit (e.g. a duplicate click on the Add Alert button) creates a second, functionally-duplicate active alert, bounded only by the unrelated 50-active-alert cap.

**Scope**
- Consider a uniqueness guard (return 409, matching `POST /alerts/rules`'s pattern) or a client-side submit-guard, for an exact `(ticker, condition, threshold_price)` match already active

**Acceptance Criteria**
- A double-submit of the same `(ticker, condition, threshold_price)` while the first alert is still active does not create a second active alert (or, if guarding is deemed unnecessary, the disposition is recorded as accepted with rationale)

---

### BLG-API-06 — POST /trade-plans has no guard against a double-submitted duplicate plan
**Priority:** P4 (Trivial)
**Type:** Spec Debt / API Contracts
**Owner:** Head of Specs Team
**Source:** ST-20/EPIC-05 (BLG-API-04), cycle 2026-09-28__release-v9.8 — idempotency/double-submit documentation sweep — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`docs/specs/api_contracts/trade_plan_endpoints.md`'s `POST /trade-plans` has no uniqueness guard — every call creates a new row. A double-submit (e.g. a duplicate click on the Save button) creates a second, functionally-duplicate draft plan with no warning. Deliberate multi-plan creation for the same ticker is a legitimate use case, so a DB-level uniqueness constraint is not the right fix.

**Scope**
- Consider a client-side submit-guard (disable button on submit) as the primary mitigation, since a server-side uniqueness constraint would block legitimate multi-plan use cases
- Record the disposition (client-side guard vs. accepted risk) once decided

**Acceptance Criteria**
- A disposition is recorded (client-side guard added, or accepted risk with rationale) for the double-submit duplicate-plan-creation case

---

### BLG-SPEC-175 — 5 pre-existing error-response examples diverge from the canonical envelope, newly caught by the extended freshness checker
**Priority:** P4 (Trivial)
**Type:** Spec Debt / API Contracts
**Owner:** API Contracts & Documentation Owner
**Source:** ST-21/EPIC-05 (BLG-API-05), cycle 2026-09-28__release-v9.8 — error-envelope conformance check extension — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-21 extended `scripts/check_contract_example_freshness.py` to validate documented 4xx/5xx error examples against the canonical envelope (`conventions.md` §13.1: `{"status": "error", "message": "<str>"}`). Running the extended check against the existing contract corpus (not just this story's own 10 new examples, all of which conform) surfaced 5 pre-existing, already-documented error examples that predate this story and diverge from the envelope — the same "default FastAPI envelope instead of canonical" non-conformance pattern `backend_engineering_patterns.md` already documents as a known audit finding, now caught mechanically for these 5 specific cases:
- `ai_endpoints.md`: `POST /ai/journal-summary` — the documented "503 Service Unavailable (LLM unreachable)" example is actually returned as HTTP 200 (by design, for graceful frontend degradation) with a domain-specific shape (`summary`, `trade_count`, `model`, `cached`, `message`), not the canonical envelope — the heading's "503" label is misleading given the endpoint never actually returns that status.
- `ai_thesis_generation.md` and `gemini_thesis_generation.md` (duplicate content): `POST /trade-plans/{plan_id}/generate-thesis`'s documented `404 — Plan not found` example uses `{"detail": "Trade plan not found"}` — FastAPI's default envelope, not the canonical one.
- `arc5_compliance_analytics.md`: `GET /analytics/arc5-compliance`'s documented `500` example uses `{"detail": "..."}` — same default-envelope non-conformance.
- `behavioural_drift_contract.md`: `GET /analytics/behavioural-drift`'s documented `401` example uses `{"detail": "Unauthorized"}` — same default-envelope non-conformance.

**Scope**
- For the 3 genuine `{"detail": ...}` cases (`generate-thesis` x2, `arc5-compliance`, `behavioural-drift` — 4 total call sites across 3 backend routers): confirm whether the router actually raises `HTTPException(detail=...)` (FastAPI default) or already returns the canonical envelope and only the *documentation* is stale; fix whichever side (code or doc) is wrong, per `backend_engineering_patterns.md`'s existing remediation guidance
- For `ai_endpoints.md`'s `POST /ai/journal-summary`: correct the misleading "503" heading label to reflect the endpoint's actual, intentional HTTP 200 graceful-degradation behaviour (matching the phrasing already used correctly by its sibling `/ai/daily-briefing`/`/ai/chat` "unavailable" responses)

**Acceptance Criteria**
- All 5 flagged cases are resolved (code fixed to conform, or documentation corrected to match actual conforming behaviour, or heading label corrected)
- `python3 scripts/check_contract_example_freshness.py` reports 0 error-envelope violations

---

### BLG-SPEC-176 — DELETE /trade-plans/{id} uses a different success envelope than conventions.md §12's documented DELETE convention
**Priority:** P4 (Trivial)
**Type:** Spec Debt / API Contracts
**Owner:** API Contracts & Documentation Owner
**Source:** ST-23/EPIC-05 (BLG-SPEC-153), cycle 2026-09-28__release-v9.8 — openapi.yaml response-schema authoring — 2026-09-29
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`conventions.md` §12 (DELETE Response Convention) states successful DELETE operations return `{"status": "ok", "data": {"deleted": true, "id": "..."}}`, and every other DELETE endpoint's documented example in this codebase follows that shape. `trade_plan_endpoints.md`'s `DELETE /trade-plans/{id}` is the one exception: its documented response is `{"status": "ok", "message": "Trade plan deleted"}` — a `message` field instead of a `data.deleted`/`data.id` object. Found while authoring `openapi.yaml`'s response schema for this endpoint (ST-23) — the schema was written to match what is actually documented (not silently reconciled to the convention), since changing which side is "correct" is a decision, not a typo fix.

**Scope**
- Confirm which side is authoritative: does the live `DELETE /trade-plans/{id}` route actually return `{status, message}` (in which case `conventions.md` §12 should note this endpoint as a named exception, or the route should be migrated to the standard envelope), or was the markdown simply never updated when the route was built against the standard envelope
- Reconcile the losing side (code or doc) to match

**Acceptance Criteria**
- `DELETE /trade-plans/{id}`'s documented response and its live behaviour agree with each other, and conventions.md §12 either lists this endpoint as an explicit exception or the endpoint is migrated to the standard DELETE envelope

---

### BLG-GOV-356 — Conduct the overdue 90-day AI feature usage review (BLG-GOV-74/140/141/142 cluster)
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** Post-ship closure `2026-09-28__release-v9.8` STEP 12.6 (90-Day AI Feature Usage Review Trigger Check, `post_ship_closure.md` v2.36, shipped this same cycle as ST-38/`BLG-GOV-351`) — first live run of the new trigger found the review still due, now 6 days overdue — 2026-09-30
**Effort:** M (~1–2d)
**Provisional-Target:** TBD

**Problem**
`BLG-GOV-351` (shipped this cycle, ST-38) built the trigger mechanism that fires this check automatically at post-ship closure, but explicitly scoped conducting the review itself as out of scope for that item ("Once triggered, actually conduct the review (real adoption/cost data) — out of scope for this item itself, which is only the trigger mechanism"). This is that follow-on item. The review was due 2026-09-24 (90 days post-v6.2 ship, 2026-06-25); as of this closure (2026-09-30) it is 6 days overdue with no review artefact filed in `docs/ops/` or `docs/governance/` for this due date (the nearest existing artefact, `docs/governance/ai_feature_usage_quarterly_review_2026-09-07.md`, predates the due date and does not cover it).

**Downstream items blocked on this review's outcome:**
- `BLG-FEAT-59` — AI adoption window verification (Financial Reporting & Records Owner)
- `BLG-FEAT-60` — AI adoption window verification (Metrics Definitions & Analytics Owner)
- `BLG-FEAT-63` — same AI-adoption gate as `BLG-FEAT-59`
- `BLG-FE-84` — AI adoption window verification (Head of UX & Design)
- `BLG-OPS-88` — bundled with this same 90-day AI cost review
- `BLG-GOV-140` — first quarterly review due 2026-09-24
- `BLG-GOV-141` — schedule within 90 days of v6.2 ship
- `BLG-GOV-142` — assess adoption rate, cost per use, and continued-investment justification

**Scope**
- Gather real adoption/cost data for the AI briefing and chat features (Anthropic API cost per use, session counts, usage-pattern stability) per `BLG-GOV-142`'s stated assessment criteria
- Produce a dated review artefact (`docs/ops/ai_feature_usage_review_<date>.md` or equivalent) confirming or disconfirming that usage patterns have stabilised
- Disposition each of the 8 downstream gated items above against the review's finding (clear the gate, or re-park with an updated concrete trigger)

**Acceptance Criteria**
- A dated review artefact exists assessing AI feature adoption rate, cost per use, and continued-investment justification
- All 8 downstream gated items listed above have an explicit disposition recorded against this review's finding

---

### BLG-GOV-357 — Sign-off single-point-of-failure matrix (per governance gate, which roles can sign)
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; Director of HR
**Source:** `IDEA-director-of-hr-20260919-02` (3-cycle park hard cap reached, resolved to terminal disposition), roadmap rebalance `2026-09-30__scheduled`
**Effort:** S (~1-2 days)
**Provisional-Target:** TBD

**Problem**
No document currently maps which roles are authorised to sign off each governance gate across this system's routines, or flags where a single agent-mediated role is the sole signer for a given gate — a concentration risk that would be invisible without deliberately enumerating it. Originally submitted 2026-09-19, parked twice (rationale: `BLG-GOV-335`/`337`'s signer-topology effect not yet observable with only 2 sprints of post-ruling data) and reached the 3-cycle park hard cap this cycle, at which point re-parking is no longer a valid outcome per `roadmap_prompt.md §4.5`.

**Scope**
- Enumerate the governance gates across all governed routines (roadmap, release planning, sprint planning, sprint execution, delivery verification, post-ship closure) and the role(s) authorised to sign each, per each routine's own prompt file
- Flag any gate where only one agent-mediated role can sign, as a concentration risk worth Product Owner/Director of HR awareness
- A follow-up note on whether concentration is an observed live risk (the originally-deferred question) may be added once more sprints of `BLG-GOV-335`/`337`-era data accrue — the matrix's existence does not depend on that data being available yet

**Acceptance Criteria**
- A published matrix (governance gate × authorised signer role(s)) exists in an appropriate location (e.g. `docs/ops/` or `claude/roadmap/`)
- Gates with a sole authorised signer are explicitly flagged in the matrix

---

### BLG-GOV-358 — gap_risk_service.py (BLG-FEAT-65) shipped without a recorded §13 review or §13.5 roster row; apparently contradicts §13.3's exclusion text
**Priority:** P2 (High)
**Type:** Governance Process / Strategy Boundary
**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Source:** STEP 8.1.5 finding, roadmap rebalance `2026-09-30__scheduled` (surfaced via `window_summary_IW-20260930-01.md`'s out-of-scope note)
**Effort:** S (~1-2 days)
**Provisional-Target:** TBD

**Problem**
`strategy_rules.md` §13.3 states: "Gap risk monitoring is excluded by design because the system operates on a daily decision cadence and cannot act on gaps at the moment they occur. Exposing a gap risk metric would increase noise without enabling a decision." Yet `backend/services/gap_risk_service.py` and its `GapRiskBadge`/`GapRiskCardBadge` UI components are live and shipped (`BLG-FEAT-65`, v6.9). Confirmed this cycle: `docs/product/decisions/decisions--2026-07-10__release-v6.9.md` (the feature's own ship decision record) contains no §13 reference at all, and the feature does not appear on `strategy_rules.md` §13.5's semi-annual re-attestation roster table. This is a genuine live-vs-canonical-spec boundary question, not a housekeeping gap.

**Scope**
- Strategy Rules & System Intent Owner determines whether the shipped badge (a static per-position display flag, not an active notification/alerting mechanism) falls within or outside §13.3's stated exclusion
- If in-scope: retroactively conduct a §13 review and add the feature to the §13.5 roster (with any binding conditions the review finds necessary)
- If out-of-scope: record why a passive display flag differs from the "gap risk metric" §13.3's exclusion contemplates, narrowing/clarifying §13.3's wording if the distinction is not already clear from its text

**Acceptance Criteria**
- A dated determination is recorded (new `docs/product/decisions/` file, or a `strategy_rules.md` §13.3/§13.5 wording update, as appropriate to the outcome)
- If the determination is CONDITIONAL or finds a genuine gap, binding conditions or a remediation item are filed

---

### BLG-QA-204 — test_position_atr_timestamp_persistence.py doesn't mock get_settings(), so active_atr_multiplier assertions don't confirm production values
**Priority:** P4 (Low)
**Type:** QA / Test Debt
**Owner:** Director of Quality; QA & Testing Owner
**Source:** PR #1884 (EPIC-01, cycle `2026-09-30__release-v9.9`) code review — 2026-10-01
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`tests/test_position_atr_timestamp_persistence.py::TestAnalyzePositionsWritesTimestamps::test_post_grace_write_includes_stop_calculated_at_and_multiplier` only asserts `active_atr_multiplier > 0`, not that it equals the real production values (`2.0` profitable / `5.0` losing, per `calculate_trailing_stop()`/`strategy_rules.md` §7.2), because `get_settings()` is not mocked in that test — the test environment's `get_settings()` returns an unconfirmed value (observed `1.0` during development, not either production multiplier). The test passes either way, so it would not catch a regression that silently changed which multiplier value gets persisted.

**Scope**
- Mock `get_settings()` in the affected test(s) to return the real `atr_multiplier_trailing=2`/`atr_multiplier_initial=5` production values

**Acceptance Criteria**
- Test explicitly mocks `get_settings()` to the real production multiplier values
- Assertion checks `active_atr_multiplier` equals the exact expected value (`2.0` or `5.0`) in both the profitable and losing branches, not merely `> 0`

---

### BLG-SPEC-178 — New live-vs-doc divergences found by the ST-28 drift-detector tool, beyond the 5 originally known
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-28/EPIC-05, cycle `2026-09-30__release-v9.9` (`scripts/check_data_model_drift.py`, `BLG-SPEC-157`) — 2026-10-01
**Effort:** S (~1d, triage + disposition; may grow if any finding requires a live migration)
**Provisional-Target:** TBD

**Problem**
Running the new `scripts/check_data_model_drift.py` against this sandbox's `readonly_staging` `DATABASE_URL` reproduced the 2 of 5 originally-known divergence classes still live today (BLG-SPEC-148's missing-index pattern, BLG-SPEC-150's orphaned-columns pattern — see below), confirming the tool works as intended. It also surfaced genuinely new findings beyond the original 5 that no prior story has triaged:

1. **DS-17's unique index (`idx_positions_open_ticker_entry_date_unique`) is absent from staging's live `positions` table**, despite `data_model.md`'s own DS-17 section recording it "confirmed live in production as of 2026-09-23." The verification query cited there was run against **production** only — this is the first time anyone has checked staging specifically since. Staging and production may have been migrated independently and now disagree, or staging was never migrated. Needs a Data Model & Domain Schema Owner check against production (write access this sandbox does not have) to confirm whether production still has it, and if staging should be brought in line.
2. **3 further undocumented, always-present `positions` columns** beyond the 4 already known and disclosed (`BLG-SPEC-150`/`BLG-SPEC-164`): `last_reviewed_at`, `risk_off_exit`, `strategy_version_at_entry`. Unlike the 4 known orphans, these are **not confirmed always-NULL** by this story — only their absence from `data_model.md`'s Fields table was checked. Needs its own live NULL/populated check and disposition (document vs. drop) before being folded into the existing orphaned-columns item.
3. **8 nullable mismatches between `data_model.md`'s Fields table and live `positions`** — `created_at`, `holding_days`, `pnl`, `pnl_pct`, `portfolio_id`, `status`, `total_cost`, `updated_at` are all documented `NO` (not nullable) but report `YES` (nullable) live. Severity varies: `portfolio_id`/`total_cost`/`status` have an explicit `NOT NULL` in the documented `CREATE TABLE` block itself (a real, more concerning doc-vs-enforcement gap), while the other 5 (`created_at`, `holding_days`, `pnl`, `pnl_pct`, `updated_at`) only carry a `DEFAULT` in the documented SQL with no `NOT NULL` keyword — i.e. the Fields table's "NO" already disagreed with this document's own `CREATE TABLE` block before live was even checked.
4. **`notifications.updated_at` is documented but not present live.**
5. **10 documented `CREATE INDEX` names and 1 documented `ADD CONSTRAINT ... CHECK` name (`settings_risk_percent_check`) were not found live** — not yet individually triaged; at least one spot-checked case (`idx_trade_plans_ticker`) turned out to be a false positive from the tool reading a "Reversible:" rollback block's old index name rather than the current migration's actual index (`idx_trade_plans_ticker_upper`), so each of these 11 names needs a manual check before assuming it is a genuine gap rather than another rollback-text false positive.

**Scope**
- Data Model & Domain Schema Owner triages findings 1–5 above, one disposition each (confirm/correct `data_model.md`, or schedule a live migration)
- Finding 5's false-positive risk means each of the 11 names needs individual confirmation, not a bulk assumption

**Acceptance Criteria**
- Each of the 5 findings above has an explicit disposition recorded (matches known pattern / needs live action / false positive / documentation fix)
- Any genuine gap gets its own canonical-spec correction or migration-scheduling item, per the existing `BLG-SPEC-150`/`BLG-SPEC-151` precedent for the original 4 orphaned columns

---

### BLG-OPS-175 — ST-09's price-alert de-duplication guard has no DB-level unique constraint
**Priority:** P4 (Trivial)
**Type:** Backend / Reliability
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** PR #1886 (EPIC-02, cycle `2026-09-30__release-v9.9`) code review — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-09 (`BLG-OPS-174`) added a SELECT-then-INSERT de-duplication check to `create_price_alert()` (`backend/services/alerts_service.py`) so a sequential double-submit of the same `(portfolio_id, ticker, condition, threshold_price)` returns the existing active alert instead of creating a second one. This closes the common sequential case but is not race-safe: two genuinely concurrent requests can both pass the SELECT check before either INSERTs, still producing two active duplicate alerts. This was disclosed at the time (PR #1886 description, commit message) rather than silently left as a gap, but was not itself filed as a tracked follow-up.

**Scope**
- Add a partial unique index on `price_alerts (portfolio_id, ticker, condition, threshold_price) WHERE active = TRUE`, mirroring the `idx_positions_open_ticker_entry_date_unique` precedent (DS-17)
- Requires a live migration — same write-access constraint as other `delegated_backend` DB-schema stories this cycle

**Acceptance Criteria**
- A genuinely concurrent double-submit (not just sequential) is rejected or absorbed at the DB layer, not just the application layer
- `data_model.md`'s `price_alerts` section documents the new constraint

---

### BLG-OPS-176 — run_scheduled_anomaly_check()'s dedup-fingerprint-clear path ignores send_alert, unlike the send path
**Priority:** P4 (Trivial)
**Type:** Backend / Code Quality
**Owner:** Infrastructure & Operations Owner
**Source:** PR #1886 (EPIC-02, cycle `2026-09-30__release-v9.9`) code review — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-08 (`BLG-OPS-173`) added `_send_anomaly_telegram_alert_deduped()`/`_clear_anomaly_alert_fingerprint()` to `backend/services/ai_endpoint_anomaly_service.py`'s `run_scheduled_anomaly_check()`. The send path is correctly gated on both `firing` and `send_alert` (`if firing and send_alert`), but the clear path is gated on `not firing` alone (`elif not firing: _clear_anomaly_alert_fingerprint()`), with no `send_alert` check. A call made with `send_alert=False` (e.g. a future preview/dry-run/status endpoint) while nothing is firing will still mutate the persisted dedup state. Today this is low-impact — clearing an already-empty-or-soon-to-be-cleared fingerprint is idempotent — but the asymmetry between the two branches was not a deliberate design choice, just an oversight, and could surprise a future caller that expects `send_alert=False` to mean "no side effects."

**Scope**
- Decide whether the clear path should also respect `send_alert` (making both branches symmetric), or keep the current behaviour with an explicit code comment stating it is intentional (dedup state should always reflect the true current firing status, independent of whether this particular call was asked to alert)

**Acceptance Criteria**
- Either the clear path is gated on `send_alert` to match the send path, or a comment explains why it deliberately is not
- A test exercises the chosen behaviour explicitly (today's tests only exercise `send_alert`'s default `True`, or `False` combined with no-firing as an incidental side effect, not a deliberate assertion of this specific interaction)

---

### BLG-QA-205 — No backend test asserts the §4.1.5 FX defaulting/echo or the §4.1.6 insufficient-cash sizing result
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** ST-11/EPIC-03, cycle `2026-09-30__release-v9.9` — strategy-rule → test traceability matrix (`docs/testing/strategy_rule_test_traceability_matrix.md`) — 2026-10-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
The traceability matrix found `services/sizing_service.py::size_position`'s FX handling and cash constraint unasserted in CI: C4.1.5-01 (user FX override, Partial), C4.1.5-02 (live FX default, None), C4.1.5-03 (`fx_rate_used` returned, None), C4.1.6-01 (`cash_sufficient: false` when estimated cost exceeds cash, None), C4.1.6-02 (`max_affordable_shares`, None). The only backend tests of the cash path live in `backend/mutmut_pilot_tests/`, which no CI workflow runs; Playwright mocks the response.

**Scope**
- Add pytest coverage of `size_position` for: US with no `fx_rate` (uses `get_live_fx_rate()`), US with an override (override used and echoed as `fx_rate_used`), UK (`fx_rate_used == 1.0`), estimated cost above available cash (`cash_sufficient` false, `max_affordable_shares` present and affordable), and below it

**Acceptance Criteria**
- Each clause above asserted by a CI-run test; matrix rows updated to Asserted

---

### BLG-QA-206 — §4.1.7 sizing-widget behaviours have no Playwright coverage
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** ST-11/EPIC-03, cycle `2026-09-30__release-v9.9` — strategy-rule → test traceability matrix (`docs/testing/strategy_rule_test_traceability_matrix.md`) — 2026-10-05
**Effort:** M (~1d)
**Provisional-Target:** TBD

**Problem**
The traceability matrix found most of `strategy_rules.md` §4.1.7's Position Sizing Calculator UI rules unasserted: C4.1.7-01 always visible / no toggle (Partial), C4.1.7-02 auto-recalculation with 300ms debounce, C4.1.7-03 loading state, C4.1.7-05 manually entered shares not overwritten + "use this" affordance, C4.1.7-06 no auto-fill on INSUFFICIENT_CASH with MaxAffordableShares shown as information, C4.1.7-07 no auto-fill on an invalid result + inline message, C4.1.7-08 sizing result never blocks form submission (all None). The no-overwrite rule is described in §4.1.7 as a financial safety constraint.

**Scope**
- Add Playwright scenarios (mocked `POST /portfolio/size`, per `shared_standards.md` §18) for each clause listed

**Acceptance Criteria**
- Each listed clause has a passing CI Playwright scenario; matrix rows updated

---

### BLG-QA-207 — The live exit decision (should_exit_position) and grace-period behaviour are not called by any CI test
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** ST-11/EPIC-03, cycle `2026-09-30__release-v9.9` — strategy-rule → test traceability matrix (`docs/testing/strategy_rule_test_traceability_matrix.md`) — 2026-10-05
**Effort:** S (~1d)
**Provisional-Target:** TBD

**Problem**
The traceability matrix found §6.3 and §8 asserted only on the replay engine's equivalent logic or a compliance view, never against `backend/utils/calculations.py::should_exit_position` (tests only stub it): C6.3-01 no stop-based exit during grace (Partial), C8.1-01 stop trigger after grace (Partial), C8.2 risk-off exit regardless of stop (Partial), C8-00 exactly three exit conditions, C8.1-02 manual confirmation, C8.3 / C6.3-03 manual exit always permitted (None). Also partial: C5-02 stop persisted from day one, C6.3-02 stop calculated and stored during grace, C7.1-02 on-load ATR recompute cadence.

**Scope**
- Unit-test `should_exit_position` directly: grace boundary (day 9 vs day 10), price at/below/above stop, risk-off overriding both grace and stop, the closed set of exit reasons
- Assert the entry write path persists an initial stop, and the grace-period path still stores the calculated stop
- Assert manual exit is accepted inside the grace period

**Acceptance Criteria**
- Each listed clause asserted by a CI-run test; matrix rows updated

---

### BLG-QA-208 — Entry required-field set and the advisory panel's non-blocking rule are untested at their boundary
**Priority:** P4 (Backlog)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** ST-11/EPIC-03, cycle `2026-09-30__release-v9.9` — strategy-rule → test traceability matrix (`docs/testing/strategy_rule_test_traceability_matrix.md`) — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
The traceability matrix found C4-01 (`POST /portfolio/position` requires ticker, entry date, entry price, shares and ATR) unasserted, and C4.2.6 (advisory checks never prevent plan submission) asserted only at the API level (`test_response_always_200_on_fail`), not at the trade-plan form.

**Scope**
- Add a contract test that each required entry field, when omitted, is rejected
- Add a Playwright scenario submitting a trade plan while the pre-entry panel shows FAIL/WARN

**Acceptance Criteria**
- Both clauses asserted by CI-run tests; matrix rows updated

---

### BLG-OPS-177 — Make "Non-Registry Dependency Check (ST-29)" a required status check on main
**Priority:** P3 (Low)
**Type:** Operations / CI Governance
**Owner:** Infrastructure & Operations Owner
**Source:** ST-17/EPIC-03, cycle `2026-09-30__release-v9.9` — live-fire confirmation (`docs/ops/non_registry_dependency_check_live_fire_2026-10-05.md`) — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-17 proved the guard fails a real PR (run 37282917791), but `main`'s branch protection does not list `Non-Registry Dependency Check (ST-29)` among its required checks (required today: `verify_governance`, `Pytest Phase A`, `Endpoint Coverage Report (ST-16)`, `OpenAPI Drift Detection (ST-08)`). A non-registry entry in `backend/requirements.txt` is still blocked indirectly, because Phase A's `pip install` fails. A non-registry `package.json`/`package-lock.json` entry is not blocked at all, since nothing required depends on resolving it.

**Scope**
- Add `Non-Registry Dependency Check (ST-29)` to `main`'s required status checks (repository settings, admin access needed)
- Confirm the workflow runs on every PR to `main` (no `paths:` filter that would leave the required check pending on unrelated PRs). If it has one, remove it or add a pass-through job first

**Acceptance Criteria**
- `gh api repos/sachiv1984/swing-trading-model/branches/main` lists the check under `protection.required_status_checks`
- A PR that does not touch dependency files is not left blocked waiting on the check

---

### BLG-QA-209 — Test files leave permanent utils.* stubs in sys.modules, so a reordered run fails 32 tests and one collection
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** ST-14/EPIC-03, cycle `2026-09-30__release-v9.9` — BLG-QA-190's "widen the audit to utils.formatting" scope item — 2026-10-05
**Effort:** M (~1d)
**Provisional-Target:** TBD

**Problem**
ST-14 removed every unrestored `sys.modules["database"]` swap and added a conftest guard against new ones. The same shape of leak exists for `utils.*`. `tests/test_alerts_service.py`, `tests/test_plan_vs_reality.py` and `tests/test_trade_service.py` install module-level stubs for `utils`, `utils.pricing`, `utils.calculations`, `utils.formatting` (and others) with no restore. Meanwhile `test_money_arithmetic_golden.py`, `test_nightly_computations.py`, `test_golden_outputs.py` and `test_rebalance_exit_signal_numpy_regression.py` pop them again to recover. The default alphabetical order happens to pass. Run in reverse file order, the suite fails identically on `main` and with ST-14: 32 failures (`test_replay_service.py`, `test_atr_consolidation.py`, `test_upstream_call_helper.py`, `test_strategy_engine_*`, `test_production_strategy.py`, `test_pre_entry_validation.py::TestMarketRegimeCache`, `test_backtest_rule_service.py`, ...) plus a collection error in `tests/test_pagination.py` (`'utils' is not a package`).

**Scope**
- Convert the stub-installing files to scoped stubs (`patch.dict(sys.modules, ...)` around the import, as `tests/test_reflection_reminder.py` does), and drop the compensating pops where they become unnecessary
- Extend `tests/conftest.py`'s ST-14 leak guard (or add a sibling) to cover the `utils` package modules

**Acceptance Criteria**
- `pytest $(ls tests/test_*.py | sort -r)` passes with no failures, matching the default order
- The guard fails a file that leaves a `utils.*` stub installed

---

### BLG-QA-210 — ST-12's valid-input sizing property checks only an upper bound, so it would pass if size_position returned 0 shares
**Priority:** P4 (Backlog)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** PR #1888 (EPIC-03, cycle `2026-09-30__release-v9.9`) agent-mediated Director of Quality review — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`tests/test_strategy_invariants_property.py::test_valid_inputs_produce_valid_conservative_size` asserts `shares >= 0` and `shares × StopDistance × FX <= RiskAmount`, but nothing from below. A regression that returned `suggested_shares = 0` (or any value well under the §4.1.3 result) would still satisfy the property. The golden tests (`test_golden_outputs.py` PS01–PS05) cover the formula on fixed cases, so this is a gap in the property's strength, not a coverage hole today.

**Scope**
- Add a lower bound: `shares` is within one 4dp floor step of `RiskAmount / (StopDistance × FX)` (before the ST-04 concentration adjustment, which `ticker=None` already disables)

**Acceptance Criteria**
- A deliberately zeroed or halved `suggested_shares` falsifies the property

---

### BLG-QA-211 — Backend modules imported inside real_database_imports() stay bound to the real database module for the rest of the pytest session
**Priority:** P4 (Backlog)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** PR #1888 (EPIC-03, cycle `2026-09-30__release-v9.9`) agent-mediated Director of Quality review (ST-14) — 2026-10-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
ST-14's `real_database_imports()` restores `sys.modules["database"]` after its block, and the conftest guard enforces that. But the modules imported inside the block stay cached in `sys.modules` with `from database import X` bindings to the real module: `main`, every router, and the services they import (first imported by `tests/test_api_contracts.py` at collection). Any later test file importing one of those services gets the real-bound copy, not a stub-bound one. The suite passes today because tests patch at the service level, but this is still cross-file coupling the new guard does not detect. ST-14 deliberately did not evict them, because eviction would break other files' string `patch()` targets.

**Scope**
- Decide whether to accept this as documented behaviour (and say so in `tests/_real_database.py`), or move contract tests to a pattern that does not populate the shared module cache (e.g. a session-scoped app fixture shared by every TestClient file)
- If accepted, extend the conftest guard's docstring to state what it does not cover

**Acceptance Criteria**
- Either a documented, reviewed decision in `tests/_real_database.py`, or no backend module bound to the real database survives past the importing file

---

### BLG-OPS-178 — Test-only Python dependencies (pytest, pytest-cov, hypothesis) are installed in the production Render build
**Priority:** P4 (Backlog)
**Type:** Operations / Build
**Owner:** Infrastructure & Operations Owner
**Source:** PR #1888 (EPIC-03, cycle `2026-09-30__release-v9.9`) agent-mediated Director of Quality review (ST-12 added hypothesis==6.168.4) — 2026-10-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`render.yaml` builds the production service with `pip install -r requirements.txt`, and `backend/requirements.txt` mixes runtime and test-only packages. `pytest` and `pytest-cov` were already there; ST-12 followed that precedent and added `hypothesis`. Each one adds production install time and attack surface for no runtime use.

**Scope**
- Split test-only packages into `backend/requirements-dev.txt` (which includes `-r requirements.txt`)
- Point every CI workflow that runs tests at the dev file, and keep the venv cache key covering both files
- Leave the Render build on `requirements.txt` only

**Acceptance Criteria**
- The production build installs no test-only package
- All CI test workflows still pass

---

### BLG-FE-194 — Recent Trades badge still shows an up-trend glyph for a break-even trade
**Priority:** P4 (Backlog)
**Type:** Frontend / UX
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Source:** PR #1889 (EPIC-06/ST-35, cycle `2026-09-30__release-v9.9`) agent-mediated Product Owner / Director of Quality review — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-35 (BLG-FE-192) made the `RecentTradesWidget` icon badge's colour neutral for `pnl === 0`, as scoped. The glyph inside it still uses the old two-way `>= 0` split (`src/components/dashboard/widgets/RecentTradesWidget.js:45`), so a break-even trade shows a neutral-coloured badge with a `TrendingUp` arrow, which still signals a gain.

**Scope**
- Use a neutral glyph (e.g. lucide `Minus`) for `pnl === 0` / missing pnl, keeping `TrendingUp`/`TrendingDown` for > 0 / < 0
- Extend `tests/e2e/recent-trades-zero-pnl-badge.spec.js` to assert the glyph

**Acceptance Criteria**
- A zero-P&L trade renders a neutral glyph; winners and losers keep their arrows
- Playwright scenario passes in CI

---

### BLG-GOV-361 — BLG-SPEC-65 still carries a stale sixth copy of the AI adoption window gate text
**Priority:** P4 (Backlog)
**Type:** Governance Process
**Owner:** Head of Specs Team; Data Model & Domain Schema Owner
**Source:** ST-24 (BLG-GOV-350), EPIC-04, cycle `2026-09-30__release-v9.9` — out-of-scope finding in the Head of Specs Team write-scope ruling for ESC-EXEC-20261001-01 — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-24 replaced the restated AI adoption window gate text on its 5 named items (BLG-FEAT-59/60/63, BLG-FE-84, BLG-OPS-88) with a pointer to the new `## Shared Gate References` → "90-Day AI Feature Usage Review Gate" statement at the top of this file. BLG-SPEC-65 (AI interaction history data model) has a sixth variant of the same clause — "…AND AI adoption window clears ~2026-07-25" — that still cites the superseded 2026-07-25 date. It was not one of BLG-GOV-350's five items, so ST-24's ruling did not authorise editing it.

**Scope**
- Point BLG-SPEC-65's adoption-window half at the canonical "90-Day AI Feature Usage Review Gate" statement (keeping a `due 2026-09-24` token so `scan_backlog_gate_conditions.py` still detects it), leaving its §13 / BLG-FEAT-55 half unchanged — or have BLG-GOV-356 (the review itself) disposition it directly

**Acceptance Criteria**
- No backlog item restates the AI adoption window gate or cites the 2026-07-25 date; BLG-SPEC-65 references the canonical statement or carries an explicit disposition

---

### BLG-GOV-362 — Make "the sealed plan names this file" a standing Sprint Execution write-scope rule for claude/roadmap/* and existing backlog item fields
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; Product Owner
**Source:** Head of Specs Team write-scope ruling for ESC-EXEC-20261001-01/-04/-05 (ST-24, ST-26, ST-31), cycle `2026-09-30__release-v9.9` — recommendation section — 2026-10-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
Three escalations this cycle (ESC-EXEC-20261001-01/-04/-05) had the same root cause: a sealed AC named a `claude/roadmap/*` file or an existing `backlog.md` item's field, but `execution_prompt.md` §7 only carves out `workforce_capacity.md` (BLG-GOV-337), so each needed a one-off Head of Specs Team ruling. The same gap was hit at v9.8 (ESC-EXEC-20260930-02), v9.7 (ST-23's deferred SI-02 cross-reference) and v8.5 (ST-22 created `product_value_ratio_history.md` out of scope, unflagged). Sprint Planning also classified ST-24 and ST-31 `autonomous` despite both needing out-of-scope writes.

**Scope**
- Consider widening BLG-GOV-337's exception in `execution_prompt.md` §7 to a general "plan-authorised named-file" rule: Sprint Execution may write a `claude/roadmap/*` file, or edit an existing `backlog.md` item's non-priority fields, when the sealed AC names that exact file and field — keeping the existing prioritisation/scope/capacity exclusions
- Consider a Sprint Planning check that classifies any AC naming a `claude/roadmap/*` path or existing-item `backlog.md` content as `delegated_decision` with a RISK entry at seal, rather than `autonomous`
- Apply the CLAUDE.md §6 checklist to each prompt changed

**Acceptance Criteria**
- A ruling is recorded on both proposals; any adopted change ships with the full CLAUDE.md §6 checklist

---

### BLG-BE-136 — Gap risk flag: disposition the standalone weekend-hold trigger (§13.3) and align trigger-timing label/spec with code
**Priority:** P2 (Medium)
**Type:** Backend + Frontend / §13 Remediation
**Owner:** Head of Engineering; Head of UX & Design; Strategy Rules & System Intent Owner (disposition sign-off)
**Source:** §13 retroactive review of the Gap Risk Flag (ST-20, EPIC-04, v9.9; `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`, Binding Conditions 6 and 8, Remediation Item 1); escalation ESC-EXEC-20261001-03
**Effort:** S (~1–2 days)
**Provisional-Target:** No later than the first §13.5 semi-annual re-attestation (2027-02-06) — hard deadline per Binding Condition 6

**Problem**
`backend/services/gap_risk_service.py:117-119` adds `"weekend_hold"` to every open position's flag whenever the server date is a Friday (`_is_weekend_hold`, `:40-43`). That flags the whole book identically every week, regardless of ticker or event. The §13 review found this standalone trigger falls within `strategy_rules.md` §13.3's "noise without enabling a decision" rationale, and it is the only binding condition the shipped code does not meet. Separately, the reason label "Weekend hold (flagged at Friday close)" (`src/pages/Positions.js:466`, `src/components/positions/PositionCard.js:19`), `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md:76` and `docs/specs/frontend/pages/positions.md:484` all describe the flag as raised "at Friday close", but the code flags it all day Friday (server date). The earnings window is also measured in calendar days (`_EARNINGS_NEXT_SESSION_WINDOW_DAYS = 1`, `:37`, `:114`), so viewed on a Friday it does not flag Monday-morning earnings. Today the weekend trigger covers that case incidentally.

**Scope**
- Default (recommended): remove the standalone `weekend_hold` trigger. Make the earnings trigger aware of trading sessions ("earnings before the position's next trading session", per the original AC-01), so that a Friday view flags Monday earnings. When an earnings flag spans a weekend, the tooltip may still show the historical *weekend* gap statistic as context (Binding Condition 4).
- Alternative (only with sign-off): the Product Owner and the Strategy Rules & System Intent Owner record a position-specific justification for keeping a weekend trigger, and §13.3's clarification is extended to cover it. Without that, the default applies.
- Whichever option is chosen, align the reason label, `ux_spec.md` §5 and `positions.md` §Gap Risk Badge with the actual trigger timing (no "at Friday close" wording unless the code implements it).
- Add a citation of the §13 review record to `gap_risk_service.py`'s module docstring (Binding Condition 8; currently `:11-12` cites only "§13, AC-04").
- Update `tests/test_gap_risk.py` (e.g. `test_flagged_for_weekend_hold_on_friday`, `:79-88`, and `test_both_reasons_stack_when_earnings_and_weekend_coincide`, `:91`) and `tests/e2e/gap-risk-flag.spec.js` to match. Update `docs/specs/api_contracts/position_endpoints.md` and `docs/reference/openapi.yaml` if the `reasons` enum changes (CLAUDE.md §2 same-commit rule).

**Acceptance Criteria**
- No flag trigger in `gap_risk_service.py` fires identically for all open positions independent of ticker or event (Binding Condition 6), or a signed alternative disposition is recorded in the §13 review record's Known Deviations / disposition section
- A position viewed on a Friday with earnings on the following Monday is flagged with reason `earnings`
- Label, UX spec, frontend spec and code agree on trigger timing
- Module docstring cites the §13 review record
- Unit and Playwright tests updated and passing; contract/OpenAPI updated if the `reasons` enum changes
- Strategy Rules & System Intent Owner sign-off recorded confirming Binding Conditions 1–8 still hold after the change

---

### BLG-SPEC-179 — positions.md Gap Risk Badge names the wrong data source (GET /positions field vs dedicated gap-risk endpoint)
**Priority:** P3 (Low)
**Type:** Spec Debt / Frontend Spec Drift
**Owner:** Head of Specs Team; Frontend Specification Owner
**Source:** §13 retroactive review of the Gap Risk Flag (ST-20, EPIC-04, v9.9; `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`, Remediation Item 2)
**Effort:** XS (<0.5 day)
**Provisional-Target:** TBD (may be folded into BLG-BE-136 if that lands first)

**Problem**
`docs/specs/frontend/pages/positions.md:482` states the Gap Risk Badge's data source is "`gap_risk` object from `GET /positions` (new field…)". The shipped implementation uses a dedicated, lazily fetched `GET /positions/{position_id}/gap-risk` endpoint (`backend/main.py:1759`; `src/hooks/useGapRisk.js:23`). This alternative was pre-authorised and is already documented in `docs/specs/api_contracts/position_endpoints.md` (2.4.0 changelog row, `:37`; implementation note in the endpoint section). The frontend spec was never updated to match.

**Scope**
- Update `positions.md` §Gap Risk Badge's Data source line to name `GET /positions/{position_id}/gap-risk` (lazily fetched per position, independent per-cell loading state), with a version bump and changelog row per the document lifecycle guide

**Acceptance Criteria**
- `positions.md` §Gap Risk Badge names the shipped endpoint; no remaining reference claims a `gap_risk` field on `GET /positions`

---

### BLG-GOV-359 — §13 sign-off ACs must cite every §13 clause that names the feature's subject matter
**Priority:** P3 (Low)
**Type:** Governance Process / §13 Gate Quality
**Owner:** Head of Specs Team; Strategy Rules & System Intent Owner
**Source:** §13 retroactive review of the Gap Risk Flag (ST-20, EPIC-04, v9.9; `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`, Critical Boundary Question 4 / Remediation Item 3)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** TBD

**Problem**
BLG-FEAT-65's v6.9 AC-04 was framed only as "no prediction of gap direction or magnitude" (`claude/cycles/2026-07-10__release-v6.9/stage4_backlog_slice.md:75`), a §13.2 test. So the agent-mediated sign-off (`qa_evidence_EPIC-02.md:33-39`) answered only that question. Nobody asked about `strategy_rules.md` §13.3, which names gap risk monitoring explicitly as excluded, until an unrelated idea-intake window noticed it roughly 12 weeks later (`claude/ideas/window_summary_IW-20260930-01.md:101`). The cycle's "expected fast pass given SI-01 precedent" framing (`cycle_summary.md:32` of that cycle) likely reduced scrutiny.

**Scope**
- Add a check to the governing prompt(s) that author §13 sign-off ACs (release planning and/or sprint planning; owning prompt to be confirmed by the Head of Specs Team). When drafting a §13 AC, search `strategy_rules.md` §13 for the feature's subject terms, and have the AC cite every §13 clause that names that subject explicitly (not only §13.2's generic prediction test)
- Apply the CLAUDE.md §6 governance-file edit checklist to whichever prompt is changed

**Acceptance Criteria**
- The governing prompt requires §13 ACs to cite each §13 clause that names the feature's subject, with a worked example referencing this gap-risk case
- CLAUDE.md §6 checklist complete (version bump, OPERATIONAL_GUIDE §14 + phase header, prompt_change_log row)

---

### BLG-GOV-360 — Apply the §13.3 gap-risk clarification and §13.5 roster row for the Gap Risk Flag to strategy_rules.md
**Priority:** P2 (Medium)
**Type:** Governance Process / Strategy Boundary
**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Source:** §13 retroactive review of the Gap Risk Flag (ST-20, EPIC-04, v9.9; `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`, Binding Condition 9); escalation ESC-EXEC-20261001-03 — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** Next routine or session with `claude/strategy/` write scope (e.g. post-ship closure `2026-09-30__release-v9.9`); before the first §13.5 re-attestation (2027-02-06) at the latest

**Problem**
The ST-20 determination (CONDITIONAL) finds §13.3's literal text ("Exposing a gap risk metric would increase noise…") contradicts the shipped, reviewed earnings-triggered flag on its face, and the feature is missing from §13.5's re-attestation roster. Sprint Execution may not write `claude/strategy/strategy_rules.md` (`execution_prompt.md` §7), so the decision record was filed alone (sufficient for ST-20's AC) and the canonical-text edits were left as exact proposed wording in the record's appendix.

**Scope**
- Apply the §13.3 clarification and the §13.5 roster row verbatim from the appendix "Proposed strategy_rules.md Wording" of `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`
- Bump `strategy_rules.md` (v1.13→v1.14 if still current, else next free version — CLAUDE.md §8 step 2a), add its Change Log row and `**Last Updated:**` entry; documentation-only per §12.3/§16; re-run the §15 version cross-reference grep

**Acceptance Criteria**
- §13.3 distinguishes standing/real-time gap risk monitoring (excluded) from a display-only, on-request, position-specific dated-event flag, and cites the decision record
- §13.5's roster lists the Gap Risk Flag as CONDITIONAL with the 2027-02-06 weekend-hold disposition deadline

---

## Release Slice — v9.9 (ephemeral — remove at next `groom backlog` per Placement Rule)

<!-- release-plan-marker: RP:v9.9:2026-09-30__release-v9.9 -->

35 items selected into `2026-09-30__release-v9.9` scope (27.85 estimated days, full capacity). Full acceptance criteria: `claude/cycles/2026-09-30__release-v9.9/stage4_backlog_slice.md`. Selection method: 0 ready P1 items; all 4 ready P2 items seated first per §1.4c, then category-balanced round-robin oldest-first for the remaining P3/P4, from a 53-item / 36.20-day ready pool. Excluded as gate-blocked: `BLG-FEAT-73`, `BLG-FEAT-76`, `BLG-FE-193` (gated on `BLG-BE-135` shipping).

| ST-ID | Item | EPIC |
|-------|------|------|
| ST-01 | BLG-BE-135 | EPIC-01 |
| ST-02 | BLG-BE-131 | EPIC-01 |
| ST-03 | BLG-BE-132 | EPIC-01 |
| ST-04 | BLG-BE-133 | EPIC-01 |
| ST-05 | BLG-BE-134 | EPIC-01 |
| ST-06 | BLG-SEC-40 | EPIC-02 |
| ST-07 | BLG-OPS-172 | EPIC-02 |
| ST-08 | BLG-OPS-173 | EPIC-02 |
| ST-09 | BLG-OPS-174 | EPIC-02 |
| ST-10 | BLG-QA-203 | EPIC-03 |
| ST-11 | BLG-QA-185 | EPIC-03 |
| ST-12 | BLG-QA-186 | EPIC-03 |
| ST-13 | BLG-QA-189 | EPIC-03 |
| ST-14 | BLG-QA-190 | EPIC-03 |
| ST-15 | BLG-QA-191 | EPIC-03 |
| ST-16 | BLG-QA-192 | EPIC-03 |
| ST-17 | BLG-QA-193 | EPIC-03 |
| ST-18 | BLG-QA-194 | EPIC-03 |
| ST-19 | BLG-GOV-356 | EPIC-04 |
| ST-20 | BLG-GOV-358 | EPIC-04 |
| ST-21 | BLG-GOV-343 | EPIC-04 |
| ST-22 | BLG-GOV-344 | EPIC-04 |
| ST-23 | BLG-GOV-347 | EPIC-04 |
| ST-24 | BLG-GOV-350 | EPIC-04 |
| ST-25 | BLG-GOV-352 | EPIC-04 |
| ST-26 | BLG-GOV-353 | EPIC-04 |
| ST-27 | BLG-GOV-354 | EPIC-04 |
| ST-28 | BLG-SPEC-157 | EPIC-05 |
| ST-29 | BLG-SPEC-164 | EPIC-05 |
| ST-30 | BLG-SPEC-165 | EPIC-05 |
| ST-31 | BLG-SPEC-166 | EPIC-05 |
| ST-32 | BLG-SPEC-167 | EPIC-05 |
| ST-33 | BLG-SPEC-168 | EPIC-05 |
| ST-34 | BLG-SPEC-169 | EPIC-05 |
| ST-35 | BLG-FE-192 | EPIC-06 |

---
