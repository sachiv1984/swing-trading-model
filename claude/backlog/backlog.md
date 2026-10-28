# Product Backlog — Momentum Trading Assistant

<!-- last-spec-debt-deep-review: 2026-10-06__release-v9.10 -->

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-10-28 (session — 3 new item(s) added: BLG-OPS-196, BLG-OPS-197, BLG-OPS-198; post-merge remainders of ST-29, ST-30/ST-31 and ST-32, EPIC-05 v9.13); prior — 2026-10-27 (session — 1 new item(s) added: BLG-OPS-195; ST-30 data pipeline cost baseline, EPIC-05 v9.13); prior — 2026-10-27 (session — 6 new item(s) added: BLG-BE-192, BLG-BE-193, BLG-BE-194, BLG-FE-234, BLG-SPEC-209, BLG-OPS-194; ST-33 data-provider risk assessment, EPIC-05 v9.13); prior history retained — see prior entries in version control
**Last rebalance:** 2026-10-06 (cycle 2026-10-06__scheduled — DL-083; 0 active roadmap initiatives, CPS=N/A; STEP 8.0 Correctness Fast-Track: BLG-BE-138 (P1) → v9.10 Now horizon; §7.1 Skill-Silo sustained-failure pull-forward: BLG-FE-193 + BLG-FE-198 committed to v9.10; idea intake IW-20261006-01 (44 submissions, full 22-role roster) → 25 backlog items, 2 rejected)

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
**Gate criteria:** A §13 review opened and passed for persistence design (chat is currently stateless per SRB-v1.7). The ≥30-days-of-AI-chat-usage limb is met (see note).
**Gate note (2026-10-08):** (Release Planning `2026-10-08__release-v9.11`, §1.3a date-lapsed disposition, within the ESC-CLOSE-20261007-01 bounds) Re-gated (b) on the same condition. The usage limb is met: AI chat has been live since v6.2, and `docs/ops/ai_feature_usage_review_2026-09-24.md` (filed 2026-10-05, ST-19) reviewed its usage. The §13 limb is unchanged and not met (no review opened). AC 3 ("Gate condition (30 days usage) verified by Product Owner") names the met limb and is listed here, not edited.

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

### BLG-TECH-21 — Migrate the frontend build toolchain off Create React App to Vite
**Priority:** P2 (Medium)
**Type:** Platform / Technical Debt
**Owner:** Head of Engineering
**Source:** GitHub issue #1885 rescan triage (`docs/security/npm_audit_rescan_triage_2026-10-06.md`); executes the plan scoped by BLG-TECH-11 (`docs/ops/cra_migration_scoping_2026-09-08.md`, v9.2) — 2026-10-06
**Effort:** M (2–3d per scoping document)
**Provisional-Target:** v10.0

**Problem**
Two consecutive npm-audit triages (2026-08-16, 2026-10-06) have been dominated by HIGH findings pinned by `react-scripts` v5 (`svgo`, `webpack-dev-server`, `webpack-dev-middleware`, `node-forge`), none fixable without a `react-scripts` major bump that does not exist — Create React App is unmaintained upstream. 17 advisory IDs are currently held as accept-risk with a 2027-02-16 review-by date; each monthly rescan adds more. BLG-TECH-11 scoped the migration but no item exists to execute it, so the accept-risk will otherwise be renewed indefinitely.

**Scope**
- Replace `react-scripts` with Vite per the scoping document (§3 target toolchain, §4 effort breakdown)
- Port `PUBLIC_URL`/asset-path handling to Vite `base` config for both deploy targets (GitHub Pages and Render) — highest-risk area, BLG-OPS-148 precedent
- Port `REACT_APP_*` env var handling and update the Playwright `webServer` build/serve command
- Schedule as a dedicated single-EPIC story, not folded into a mixed-scope sprint (scoping document §6)

**Acceptance Criteria**
- `react-scripts` removed from `package.json`; `npm ci`, build, and the full Playwright suite pass in CI
- Human staging run recorded for both GitHub Pages and Render deploys confirming assets load and routing works (date recorded in DoQ sign-off)
- Fresh `npm audit` shows the `react-scripts`-pinned HIGH/CRITICAL findings resolved; `docs/security/dependency_vuln_baseline.json` and the two accept-risk review records updated to close them out
- Ships before the 2027-02-16 accept-risk review-by date, or that review is performed on schedule if it slips

---

### BLG-QA-214 — Behaviour test that alerts grace warning ignores settings.min_hold_days
**Priority:** P4 (Low)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** ST-01/ST-02/ST-04 (EPIC-01, cycle `2026-10-06__release-v9.10`) — agent-mediated Director of Quality review of the EPIC-01 PR — 2026-10-06
**Effort:** XS (<0.5 day)
**Provisional-Target:** TBD

**Problem**
ST-01 moved `alerts_service`'s grace-period warning from `settings.min_hold_days` to the fixed `GRACE_PERIOD_DAYS`. That change is checked only by text-matching the source (`tests/test_strategy_parameter_parity.py`). `test_settings_row_min_hold_days_does_not_shorten_grace` would also pass on the pre-change code, because `analyze_positions` never read `min_hold_days`.

**Scope**
- A behaviour test of the alert evaluation with a settings row of `min_hold_days = 5`. It asserts the warning fires on days 8–9 of the 10-day window, not days 3–4.

**Acceptance Criteria**
- [ ] The test fails if `alerts_service` reads `min_hold_days` from the settings row again

---

### BLG-API-07 — Settings API still accepts the four fixed strategy-parameter fields, which no stop path reads
**Priority:** P4 (Low)
**Type:** API Contract
**Owner:** API Contracts & Documentation Owner
**Source:** ST-01/ST-02/ST-04 (EPIC-01, cycle `2026-10-06__release-v9.10`) — agent-mediated Product Owner review of the EPIC-01 PR — 2026-10-06
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
After ST-01 (ruling (a)), `POST /settings` and `PATCH /settings/{settings_id}` still accept and store `min_hold_days`, `atr_period`, `atr_multiplier_initial` and `atr_multiplier_trailing`. `settings_endpoints.md` documents that they have no effect, but an API caller gets a 200 and cannot tell that the change was ignored.

**Scope**
- Choose one: reject the four fields with a 400 naming the §11 rule, or return a deprecation warning field. Update the contract and OpenAPI in the same commit.

**Acceptance Criteria**
- [ ] A write that includes any of the four fields is rejected or flagged in the response, and documented

---

### BLG-TECH-23 — Assess major/breaking dependency upgrades from the October 2026 quarterly review
**Priority:** P3 (Low)
**Type:** Platform / Technical Debt
**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Source:** ST-17 (BLG-OPS-92), EPIC-04, cycle `2026-10-06__release-v9.10` — `docs/security/dependency_update_review_2026-10-06.md` — 2026-10-06
**Effort:** M (~2-3 days across items; assess first, then split)
**Provisional-Target:** TBD

**Problem**
Several direct dependencies are a major version, or a breaking minor series, behind: anthropic 0.105 → 1.11 (used by 3 AI services), SQLAlchemy 2.0 → 2.1, reportlab 4 → 5 (PDF export), uvicorn 0.24 → 0.54, framer-motion 12 → 14, lucide-react 0.563 → 1.x (renamed icons), eslint 9 → 10. `moment` is deprecated, and `date-fns` is already a dependency. None carries a known vulnerability today, so these are maintainability risks, not security ones.

**Scope**
- For each package, record breaking changes that affect this codebase, the effort, and an upgrade-or-hold decision. File a separate story for each upgrade worth doing.
- tailwindcss 4 is excluded and stays with BLG-TECH-21.

**Acceptance Criteria**
- [ ] A dated assessment covers all 8 packages, with a decision for each and a backlog item for each upgrade it approves

---

### BLG-TECH-24 — numpy 2.5 needs Python 3.12; check pinned bumps resolve on the pinned Python before they land
**Priority:** P3 (Low)
**Type:** Tech Debt / Dependencies
**Owner:** Head of Engineering; Infrastructure & Operations Owner
**Source:** ST-28/EPIC-04, cycle `2026-10-12__release-v9.12` — 2026-10-15
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
The October 2026 review (`docs/security/dependency_update_review_2026-10-06.md` §3) listed `numpy` 2.4.6 → 2.5.3 as a batch bump, but numpy 2.5.x requires Python ≥ 3.12. The backend is pinned to 3.11.0 (`backend/.python-version`, CI, `render.yaml`). ST-28 applied it, and the Render staging build and CI Pytest failed with "No matching distribution found for numpy==2.5.3". It was reverted to 2.4.6, the newest 3.11-compatible release. Neither the review nor the bump was checked against the pinned Python, and the sandbox venv runs Python 3.14, so it installed there.

**Scope**
- Keep numpy at 2.4.x until the backend moves to Python 3.12+. Record that dependency in the next quarterly review.
- Add a check, in CI or the quarterly review method, that `backend/requirements*.txt` resolve for the pinned Python (`pip download --python-version $(cat backend/.python-version) ...`, or install on a 3.11 runner)

**Acceptance Criteria**
- A requirements change that does not resolve on the pinned Python fails a check before merge
- The quarterly review method names the pinned-Python resolve step

---

### BLG-GOV-387 — Correct the v9.8–v9.10 rolling line's compound Owner count in role_share_history.md (17 of 21, not 19)
**Priority:** P3 (Low)
**Type:** Governance Process / Workforce Metrics
**Owner:** PMO Lead
**Source:** ST-44/EPIC-06, cycle `2026-10-12__release-v9.12`, PMO Lead observation in the agent-mediated approval recorded in `ESC-EXEC-20261013-04` — 2026-10-13
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`claude/roadmap/role_share_history.md`'s rolling 3-cycle aggregate line for v9.8–v9.10 says 19 of v9.10's 21 Owner values are compound. `scripts/compute_role_share_history.py` finds 17: 21 Owner values, of which 4 have no `"; "` separator. ST-44's named-file write covered only the split-credit column, so the prose was left as it is.

**Scope**
- Re-derive the count with the script and correct the figure in the rolling-aggregate line at the next §7.2 append, or in a PMO Lead edit

**Acceptance Criteria**
- The v9.8–v9.10 rolling line's compound count matches the script's output for v9.10

---

### BLG-GOV-388 — Gate scan: count an item as shipped only on a ✅ COMPLETE banner line, not a prose mention
**Priority:** P3 (Low)
**Type:** Governance Tooling
**Owner:** Head of Specs Team; Head of Engineering
**Source:** PR #2023 agent-mediated Director of Quality review (ST-40/EPIC-06, cycle `2026-10-12__release-v9.12`) — 2026-10-13
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-40's `gating_item_shipped()` in `scripts/scan_backlog_gate_conditions.py` treats an active item as shipped if the string `✅ COMPLETE` appears anywhere in its body. A prose mention therefore counts as a banner. Today the only occurrence in `backlog.md` is inside BLG-GOV-386's own Scope text ("archived or bannered ✅ COMPLETE"), so any gate naming BLG-GOV-386 would be wrongly listed as "gating item shipped". The list is advisory and never clears a gate, so the impact is a false prompt to re-read, not a wrong scope decision.

**Scope**
- Match the banner only in its conventional positions (the `###` heading line or a line starting `> ✅ COMPLETE` / `**Status:** ✅ COMPLETE`), not as a substring anywhere in the body
- Add a test where an item mentions `✅ COMPLETE` in prose and is still treated as open

**Acceptance Criteria**
- An item whose only `✅ COMPLETE` occurrence is in prose is not treated as shipped
- Existing `tests/test_scan_backlog_gate_conditions_gating_item_shipped.py` cases still pass

---

### BLG-QA-222 — Extend the utils.* leak guard to attributes patched on the real utils modules
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** PR #2023 agent-mediated Director of Quality review (ST-46/EPIC-06, cycle `2026-10-12__release-v9.12`), non-blocking finding — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
ST-46's conftest guard checks only *which module object* sits under `utils` / `utils.*` in `sys.modules`. A test that does `sys.modules["utils.calculations"].some_fn = MagicMock()` without restoring it leaks just as badly, but passes the guard. `tests/test_live_exit_decision.py:25` and `tests/test_position_trade_plan_link.py:64` still carry workarounds (loading a private copy of `utils/calculations.py`) for exactly this shape.

**Scope**
- Snapshot the public callables of the real `utils.*` modules at session start, and fail any file or test that leaves one replaced, as the module-identity guard does
- Then remove the private-copy workarounds where they become unnecessary

**Acceptance Criteria**
- The guard fails a test that replaces an attribute on a real `utils.*` module without restoring it
- Default and reverse-order full suites still pass

---

### BLG-TECH-25 — Upgrade the anthropic Python SDK from 0.105 to 2.x
**Priority:** P3 (Low)
**Type:** Tech Debt / Dependencies
**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Source:** ST-34 (BLG-TECH-23), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/security/dependency_major_upgrade_assessment_2026-10-27.md` §anthropic — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
The backend pins `anthropic==0.105.2`. The 0.x line no longer gets fixes and sends API version `2023-06-01`; 2.x sends `2026-10-21`. The assessment found nothing in the four AI services that breaks (no sampling parameters, dict-literal messages, `api_key` only), but 1.0 moved the SDK to `httpx2`, so two tests that build `RateLimitError` from `httpx` objects must change.

**Scope**
- Bump `anthropic` to the latest 2.x in `backend/requirements.txt`, and confirm it resolves on Python 3.11.0 (BLG-TECH-24)
- Port `tests/test_upstream_call_helper.py` and `tests/test_gemini_claude_retry_backoff.py` to build errors from `httpx2`
- Run one live call per AI feature on staging

**Acceptance Criteria**
- The backend installs and the full pytest suite passes on Python 3.11.0 with anthropic 2.x
- `utils/upstream_call.py` still retries on the four anthropic error types (tests)
- Each AI feature returns generated content on staging after the upgrade

---

### BLG-TECH-26 — Remove the unused SQLAlchemy dependency
**Priority:** P3 (Low)
**Type:** Tech Debt / Dependencies
**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Source:** ST-34 (BLG-TECH-23), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/security/dependency_major_upgrade_assessment_2026-10-27.md` §SQLAlchemy — 2026-10-27
**Effort:** XS (<1h)
**Provisional-Target:** v9.14

**Problem**
`backend/requirements.txt` pins `sqlalchemy==2.0.52`, but no file in `backend/`, `scripts/` or `tests/` imports it; all database access uses `psycopg2`. It was added in `3579d2ff` (2026-02-16) and never used. Upgrading it to 2.1 would be wasted work; it adds install time and audit surface.

**Scope**
- Delete the `sqlalchemy` line from `backend/requirements.txt`

**Acceptance Criteria**
- `grep -ri sqlalchemy backend scripts tests` finds no import
- The full pytest suite passes and the Render staging backend builds and starts without it

---

### BLG-TECH-27 — Upgrade reportlab from 4.2 to 5.x and test the tax-year PDF build
**Priority:** P3 (Low)
**Type:** Tech Debt / Dependencies
**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Source:** ST-34 (BLG-TECH-23), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/security/dependency_major_upgrade_assessment_2026-10-27.md` §reportlab — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
`reportlab==4.2.5` builds the tax-year PDF export (`services/reports_service.py::build_tax_year_pdf`). Releases 4.4.8 to 5.0.3 record several security fixes this pin misses. 5.0.4 starts changing the default base font, so the PDF can look different. No test builds a PDF today, so a break would only show in production.

**Scope**
- Add a pytest that builds a PDF from a fixed report and checks the bytes parse as a PDF with the expected page count
- Bump `reportlab` to the latest 5.x, confirming it resolves on Python 3.11.0 (BLG-TECH-24)
- Compare one exported tax-year PDF before and after

**Acceptance Criteria**
- The new PDF build test passes on 4.2.5 before the bump and on 5.x after it
- An exported tax-year PDF from staging is checked for layout and fonts after the upgrade, with the result recorded

---

### BLG-TECH-28 — Upgrade uvicorn from 0.24 to 0.54
**Priority:** P3 (Low)
**Type:** Tech Debt / Dependencies
**Owner:** Head of Engineering; Infrastructure & Operations Owner
**Source:** ST-34 (BLG-TECH-23), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/security/dependency_major_upgrade_assessment_2026-10-27.md` §uvicorn — 2026-10-27
**Effort:** XS (~0.25d)
**Provisional-Target:** v9.14

**Problem**
The backend server is pinned to `uvicorn[standard]==0.24.0`, 30 minor releases behind on a pre-1.0 package. The assessment found no breaking change for this app: the Render start command uses only `--host` and `--port`, there are no WebSocket routes, and the `uvicorn`, `uvicorn.error` and `uvicorn.access` logger names that `main.py` configures are unchanged.

**Scope**
- Bump `uvicorn[standard]` to the latest release, confirming it resolves on Python 3.11.0 (BLG-TECH-24)

**Acceptance Criteria**
- The full pytest suite passes
- The Render staging backend starts and its access log lines keep their current format

---

### BLG-TECH-29 — Upgrade framer-motion from 12 to 14 with a design check
**Priority:** P3 (Low)
**Type:** Tech Debt / Dependencies
**Owner:** Head of Engineering; Head of UX & Design
**Source:** ST-34 (BLG-TECH-23), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/security/dependency_major_upgrade_assessment_2026-10-27.md` §framer-motion — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
28 files use `motion` and `AnimatePresence` from `framer-motion` 12. The 13.0 and 14.0 breaking changes do not affect this usage, but fixes between 12.43 and 14.7 change `AnimatePresence` exit ordering, first-render values and springs. That can change how an animation looks without failing any test.

**Scope**
- Bump `framer-motion` to the latest 14.x and update the lockfile
- Run the Playwright suite
- Head of UX & Design checks the animated surfaces (modals, panels, page transitions) on staging

**Acceptance Criteria**
- All Playwright shards pass in CI
- A recorded staging design check of the animated surfaces finds no unwanted change

---

### BLG-TECH-30 — Upgrade lucide-react from 0.563 to 1.x with a design check
**Priority:** P3 (Low)
**Type:** Tech Debt / Dependencies
**Owner:** Head of Engineering; Head of UX & Design
**Source:** ST-34 (BLG-TECH-23), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/security/dependency_major_upgrade_assessment_2026-10-27.md` §lucide-react — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
127 files import 105 icons from `lucide-react` 0.563. In 1.62.0 all 105 names are still exported (the 18 old names such as `AlertTriangle` and `Loader2` included), the `lucide-<name>` classes the Playwright specs select on remain, and `aria-hidden="true"` is now the default. What can change is icon artwork, which no test catches.

**Scope**
- Bump `lucide-react` to the latest 1.x and update the lockfile
- Run the Playwright suite
- Head of UX & Design checks the most-used icons on staging

**Acceptance Criteria**
- All Playwright shards pass in CI, including the four specs that select icons by class
- A recorded staging design check finds no unwanted icon change

---

### BLG-TECH-31 — Replace moment with date-fns on System Status and remove moment
**Priority:** P3 (Low)
**Type:** Tech Debt / Dependencies
**Owner:** Head of Engineering; Head of UX & Design
**Source:** ST-34 (BLG-TECH-23), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/security/dependency_major_upgrade_assessment_2026-10-27.md` §moment — 2026-10-27
**Effort:** XS (~0.25d)
**Provisional-Target:** v9.14

**Problem**
`moment` is deprecated and is used in two places only, both in `src/pages/SystemStatus.js` (`format('HH:mm, D MMM YYYY')` and `fromNow()`). `date-fns` 4.4.0 is already a dependency used in 19 files. GHSA-4p3w-j4w9-5jqw (moment below 2.31.0, server-side only) does not affect this browser use, and the lockfile already has 2.31.0.

**Scope**
- Replace the two calls with `format(date, 'HH:mm, d MMM yyyy')` and `formatDistanceToNow(date, { addSuffix: true })`
- Remove `moment` from `package.json` and the lockfile

**Acceptance Criteria**
- `moment` no longer appears in `src/` or `package.json`
- A Playwright test checks the "As of" time format and the health-check relative time on System Status, and passes in CI

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

**Gate criteria:** claude_audit_log table 6+ months old — clears 2026-11-22 (6 months after the v4.0 ship). BLG-OPS-31 (Render log retention policy) shipped v4.7; this extends scope to Supabase query logs and claude_audit_log.
**Gate note (2026-10-08):** (Release Planning `2026-10-08__release-v9.11`, §1.3a date-lapsed disposition, within the ESC-CLOSE-20261007-01 bounds) Re-gated (b) on the same condition. The embedded date (2026-05-22) was the start of the 6-month count, so the scan reported a false-positive lapse; the concrete clearance date is now stated. AC 3 ("6+ months of audit log data") restates the same condition and is listed here, not edited.

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
**Gate criteria:** SI-05 Phase 1 effectiveness review output (BLG-GOV-113 protocol) filed AND Phase 2 activation decision made
**Gate note (2026-10-08):** (Release Planning `2026-10-08__release-v9.11`, §1.3a date-lapsed disposition, within the ESC-CLOSE-20261007-01 bounds) Re-gated (b) on the same condition. 2026-07-04 was the review's scheduled date, not a clearance date. No Phase 2 activation decision is recorded, so the gate is not met. No AC names the gate's date or gating item.

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

### BLG-GOV-142 — AI feature ROI assessment at 3-month post-ship mark
**Priority:** P2 (Medium)
**Type:** Governance Process / Value Assessment
**Owner:** Challenger; FinOps & Resource Architect; Product Owner
**Source:** IDEA-challenger-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Resolved (2026-10-05, ST-19):** this assessment is `docs/ops/ai_feature_usage_review_2026-09-24.md` — adoption rate (31 calls, 5 of 15 weeks active, 3 of 6 AI features never used), cost per use ($0.0017–$0.0080; ≈$0.17 total), continue/modify recommendation, and the Product Owner decision (continue building; gate removed). Archive at the next `groom backlog`.

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
**Gate criteria:** Same gate as BLG-FEAT-55 — §13 review opened and passed for chat persistence. The AI adoption-window limb is met (see note).
**Gate note (2026-10-08):** (Release Planning `2026-10-08__release-v9.11`, §1.3a date-lapsed disposition, within the ESC-CLOSE-20261007-01 bounds) Re-gated (b) on the same condition. The adoption-window limb is met: the 90-day AI feature usage review was filed 2026-10-05 (`docs/ops/ai_feature_usage_review_2026-09-24.md`, ST-19), and the Product Owner removed that gate from its sibling items. This also meets `BLG-GOV-361`'s scope (drop the adoption-window half and keep the §13 half). No AC names the gate's date or gating item.

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
**Gate criteria:** ≥20 closed trades captured since PT-04 shipped, with sufficient `setup_type` diversity to justify presets (at least 3 distinct setup types with ≥3 trades each).
**Gate note (2026-10-08):** (Release Planning `2026-10-08__release-v9.11`, §1.3a date-lapsed disposition, within the ESC-CLOSE-20261007-01 bounds) Re-gated (b) on the same condition. The embedded date (2026-06-23, PT-04 ship) was the start of the trade count, not a clearance date, so the scan reported a false-positive lapse. Not verified as met: no production read this session. No AC names the gate's date.

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
**Gate criteria:** A Render resource alert (memory or CPU) on the backend service, or a sustained backend latency breach.
**Gate change (ST-19, Product Owner authorised):** unbundled on 2026-10-05 from the 90-day AI usage review (`docs/ops/ai_feature_usage_review_2026-09-24.md`), which found AI load negligible (31 calls in 102 days) and so gives no dyno-sizing signal.

**Problem**
The 2 AI endpoints are only 8 days live as of this idea's submission; no cost/performance signal yet indicates a right-sizing need.

**Scope**
- Review dyno tier when the gate fires (a Render resource alert or latency breach), using Render metrics rather than AI usage

**Acceptance Criteria**
- Review conducted after the gate fires, citing the triggering alert or breach

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
**Gate criteria:** Inherits `BLG-FEAT-30`'s gate (screener live ≥60 days AND ≥60 closed trades with attribution) — track disposition there.
**Gate note (2026-10-08):** (Release Planning `2026-10-08__release-v9.11`, §1.3a date-lapsed disposition, within the ESC-CLOSE-20261007-01 bounds) Re-gated (b) on the same condition. The dates in the former gate text were history, not clearance dates, so the scan reported a false-positive lapse. That history is preserved here: Reconciled as a sub-scope of `BLG-FEAT-30` at the Product Owner's `2026-09-03__release-v9.1` decision (reaffirmed each cycle since, most recently `decisions--2026-09-07__release-v9.2.md`); this field added `2026-09-09` (post-ship closure `2026-09-07__release-v9.2` outstanding-actions resolution, Head of Specs Team direct action per the new Gate-Inheritance Field-Completeness Scan, `backlog_management_prompt.md` v1.17) so future rebalance/release-planning sessions no longer need to re-locate a prior cycle's decisions document to confirm this item's exclusion — 4 consecutive cycles (v8.9–v9.2) required that manual lookup before this fix.

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

**Update (2026-10-05, ST-19):** the 90-day review is now filed (`docs/ops/ai_feature_usage_review_2026-09-24.md`) and the `## Shared Gate References` section has been removed, since no item cites it any more. BLG-SPEC-65's adoption-window half is therefore met; the fix is to drop that half from its gate line (keeping the §13 / BLG-FEAT-55 half), not to point it at the removed section.

**Acceptance Criteria**
- No backlog item restates the AI adoption window gate or cites the 2026-07-25 date; BLG-SPEC-65 references the canonical statement or carries an explicit disposition

---

### BLG-GOV-360 — Apply the §13.3 gap-risk clarification and §13.5 roster row for the Gap Risk Flag to strategy_rules.md
**Priority:** P2 (Medium)
**Type:** Governance Process / Strategy Boundary
**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Source:** §13 retroactive review of the Gap Risk Flag (ST-20, EPIC-04, v9.9; `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`, Binding Condition 9); escalation ESC-EXEC-20261001-03 — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** Next routine or session with `claude/strategy/` write scope (e.g. post-ship closure `2026-09-30__release-v9.9`); before the first §13.5 re-attestation (2027-02-06) at the latest

**Resolved (2026-10-05, ST-20):** applied to `strategy_rules.md` v1.14 in ST-20's own commit on the user's explicit instruction, using the wording as amended by an independent second-pass Strategy Rules & System Intent Owner review (carve-out limited to canonically recognised events — today only earnings; weekend-hold trigger recorded in §13.3 as a time-boxed deviation, BLG-BE-136; re-attestation step added to the roster row). The original Provisional-Target (post-ship closure) was not a valid route — `post_ship_closure.md` §5 forbids `strategy_rules.md` edits. Archive at the next `groom backlog`.

**Problem**
The ST-20 determination (CONDITIONAL) finds §13.3's literal text ("Exposing a gap risk metric would increase noise…") contradicts the shipped, reviewed earnings-triggered flag on its face, and the feature is missing from §13.5's re-attestation roster. Sprint Execution may not write `claude/strategy/strategy_rules.md` (`execution_prompt.md` §7), so the decision record was filed alone (sufficient for ST-20's AC) and the canonical-text edits were left as exact proposed wording in the record's appendix.

**Scope**
- Apply the §13.3 clarification and the §13.5 roster row verbatim from the appendix "Proposed strategy_rules.md Wording" of `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`
- Bump `strategy_rules.md` (v1.13→v1.14 if still current, else next free version — CLAUDE.md §8 step 2a), add its Change Log row and `**Last Updated:**` entry; documentation-only per §12.3/§16; re-run the §15 version cross-reference grep

**Acceptance Criteria**
- §13.3 distinguishes standing/real-time gap risk monitoring (excluded) from a display-only, on-request, position-specific dated-event flag, and cites the decision record
- §13.5's roster lists the Gap Risk Flag as CONDITIONAL with the 2027-02-06 weekend-hold disposition deadline

---

### BLG-GOV-368 — Pre-PR check that an EPIC branch carries no other EPIC's commits
**✅ COMPLETE — 2026-10-15 — closed as met: `execution_prompt.md` v3.81→v3.82 §3.2.B cross-EPIC commit pre-PR hard gate (LL-v9.9-P3-01, post-ship closure `2026-09-30__release-v9.9`, 2026-10-06), shipped with the full CLAUDE.md §6 checklist (`prompt_change_log.md`; `OPERATIONAL_GUIDE.md` v4.221). The optional `quality_gate.yml` mirror is declined by Head of Specs Team ruling (agent-mediated, user-directed, 2026-10-15): AC 1's CI clause applies only "if the workflow option is adopted", and the prompt gate has held since (v9.10–v9.12 had no cross-EPIC PR). Closes post-ship closure `2026-10-12__release-v9.12` §6 row 7.**
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Sprint close, cycle `2026-09-30__release-v9.9` — EPIC-02 PR #1886 / `execution_state.json` process_notes (2026-10-05) — 2026-10-06
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
EPIC-02's branch was cut on top of the EPIC-04/EPIC-05 linear history rather than from `main`, so merging PR #1886 also brought 19 commits from other EPICs into `main` (12 `[EPIC-04]`, 7 `[EPIC-05]`). Those stories skipped their own STEP 4 merge gate, which breaks the CLAUDE.md §2 branch-matching rule. EPIC-04 and EPIC-05 then needed retroactive gates (qa_evidence written after the fact, agent-mediated DoQ sign-off, Product Owner acceptance through PRs #1891/#1892). `execution_prompt.md` STEP 2 step 3 says "verify it is based on `main`", but nothing checks the branch's actual commit set before the PR opens. A branch based on `main` plus unrelated commits passes that wording.

**Scope**
- Add a hard pre-PR check to `execution_prompt.md` STEP 3.2.B: run `git log origin/main..HEAD --format='%H %s'` and halt if any commit is tagged with an EPIC other than this one (`[GOVERNANCE]` merge-resolution commits excepted)
- Consider the same check in `quality_gate.yml` so a PR cannot pass CI with another EPIC's commits
- Apply the CLAUDE.md §6 checklist to any prompt changed

**Acceptance Criteria**
- An EPIC PR whose branch carries another EPIC's `[EPIC-yy]` commit is stopped before the PR opens (prompt) or fails CI (if the workflow option is adopted)
- The full CLAUDE.md §6 checklist ships with any prompt change

---

### BLG-GOV-377 — strategy_rules.md §13.5 roster row still says PO-05 reuses IT-06's paper-trading mechanics
**Priority:** P3 (Low)
**Type:** Governance Process / Strategy Text Alignment
**Owner:** Strategy Rules & System Intent Owner
**Source:** ST-20 (EPIC-04, cycle `2026-10-06__release-v9.10`) — 2026-10-07
**Effort:** XS (~0.25 day)
**Provisional-Target:** TBD (before the first §13.5 re-attestation, 2027-02-06)

**Problem**
ST-20 corrected the PO-05 pre-assessment, the roadmap and `replay_mode.md` after the Strategy Rules & System Intent Owner acknowledged findings F1, F2 and F4 (ESC-EXEC-20261006-05). `strategy_rules.md` v1.14 §13.5's PO-05 roster row still says the PASS "explicitly reuses IT-06's paper-trading mechanics under IT-06's own binding conditions". PO-05 runs on `strategy_engine.py` and makes no Alpaca call. Sprint Execution cannot write `claude/strategy/strategy_rules.md` (`execution_prompt.md` §7), so the row was left as is.

**Scope**
- Replace that clause with: "runs on the strategy backtest engine with no Alpaca call, so Binding Condition 5's isolation is met by construction (v9.10 corrections, `po05_section13_preassessment.md`)".
- Change Log row (documentation only) and §15 grep. Can share a commit with BLG-GOV-376.

**Acceptance Criteria**
- [ ] §13.5's PO-05 row no longer says PO-05 reuses IT-06.

---

### BLG-SPEC-180 — Correct metrics_definitions.md's claim that a NULL positions.fees_paid yields a silently-zero trade_history fee leg
**Priority:** P4 (Trivial)
**Type:** Spec Debt / Metrics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** ST-30/EPIC-05, 2026-09-30__release-v9.9 — Data Model & Domain Schema Owner disposition on BLG-SPEC-165 — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`docs/specs/metrics_definitions.md` §Fee-Netting Basis (the "Audit finding: a NULL fee leg is silently treated as zero" paragraph) gives, as an example cause of a NULL `trade_history.entry_fees`, "the source `positions.fees_paid` was itself `NULL` at entry". That cannot happen via the application: `position_service.py` `exit_position()` computes `float(position.get('fees_paid', 0))`, which raises `TypeError` on a NULL value (the key is always present in the row dict), so such a position cannot be exited and no trade_history row is written; `entry_fees` is always the numeric `exit_entry_fees`. With DS-23 (`data_model.md`) re-applying `NOT NULL` on `positions.fees_paid`, the cited cause is additionally structurally impossible. A NULL `entry_fees`/`exit_fees` can only originate from legacy or hand-inserted `trade_history` rows. The `null_fee_trade_count` flag itself remains correct and useful.

**Scope**
- Reword the example cause to "legacy or manually inserted `trade_history` rows", and cross-reference DS-23
- Remove the dependency on `BLG-SPEC-151` as a live drift (now dispositioned)

**Acceptance Criteria**
- The paragraph no longer cites a NULL `positions.fees_paid` as a reachable cause of a NULL trade_history fee leg
- No change to the `null_fee_trade_count` contract or computation

---

### BLG-SPEC-184 — Extend check_data_model_drift.py to compare documented column defaults
**Priority:** P4 (Trivial)
**Type:** Spec Debt / Tooling
**Owner:** Data Model & Domain Schema Owner
**Source:** PR #1892 agent-mediated Director of Quality review (EPIC-05, cycle `2026-09-30__release-v9.9`) — 2026-10-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`scripts/check_data_model_drift.py` compares only column presence and `is_nullable` (`:95`). `data_model.md` documented `fees_paid DECIMAL(10, 2) DEFAULT 0` for many versions, but no default ever existed live. The error was found by hand during ST-30, not by the ST-28 drift tool, which cannot see defaults. Any other documented `DEFAULT` in a `CREATE TABLE` block (for example `state_history` "Default `[]`") could have drifted the same way without detection.

**Scope**
- Parse `DEFAULT <expr>` from each section's `CREATE TABLE` block (and/or "Default `x`" in Fields descriptions).
- Select `column_default` from `information_schema.columns`, and report a "default mismatch" class next to the existing nullable mismatches, normalising Postgres casts such as `'[]'::jsonb` and `0`.
- Add unit tests in `tests/test_check_data_model_drift.py` with mocked rows.

**Acceptance Criteria**
- [ ] A doc showing `DEFAULT 0` against a live `column_default = NULL` is reported as a default mismatch, and vice versa.
- [ ] Equivalent forms (`0` vs `0::numeric`, `'[]'::jsonb` vs `'[]'`) do not produce false positives.
- [ ] The tool remains read-only (`SELECT` against `information_schema` only), and the existing 36 drift/orphan/dashboard tests still pass.

---

### BLG-FE-195 — Settings › Strategy Parameters: §11 defaults, §7.2-correct helper text, governed-parameter treatment
**Priority:** P2 (High)
**Type:** Frontend / Strategy Conformance (build-and-ship)
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design; QA Lead
**Source:** `IDEA-base44-frontend-20261006-01`, `IDEA-head-of-ux-20261006-02`, `IDEA-qa-lead-20261006-01`, `IDEA-qa-lead-20261006-02` (consolidated, `IW-20261006-01`), roadmap rebalance `2026-10-06__scheduled`
**Gate criteria:** `BLG-BE-138`'s parameter-authority ruling recorded (decides read-only vs editable-with-warning)
**Effort:** S (~1.5-2 days)
**Provisional-Target:** TBD

**Problem**
`src/pages/Settings.js` pre-fills 2× / 3× ATR and 5 hold days when no settings row exists (§11: 5×, 2×, 10). Helper text says the losing stop is 'Entry − 5×ATR' and the profitable stop 'High − 2×ATR'; §7.2 and the code use the current price, with a breakeven floor for profitable positions. The parameters sit in the same editable form as theme and fees, with no sign that changing them moves live stops. No test covers these values.

**Scope**
- Defaults equal §11; helper text states the §7.2 formulas.
- A separate 'Strategy (governed by strategy rules)' panel: read-only or editable behind a consequence warning, per `BLG-BE-138`'s ruling.
- Playwright: empty settings fixture shows §11 defaults. Unit test: frontend strategy constants equal §11.

**Acceptance Criteria**
- [ ] Displayed defaults are 5, 2, 10, 14; helper text matches §7.2 (Playwright).
- [ ] Governed panel behaves per the recorded ruling.
- [ ] Constants test passes.

---

### BLG-SPEC-186 — Define the allowed exit reasons and map each to one of §8's three exit conditions
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner; Metrics Definitions & Analytics Owner
**Source:** `IDEA-data-model-20261006-02`, `IDEA-metrics-20261006-01` (consolidated, `IW-20261006-01`), roadmap rebalance `2026-10-06__scheduled`
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
`exit_reason` is free text: 6 UI values (`ExitModal.js:356-361`) plus snake-case legacy variants that `TradeHistoryTable.js:86-98` maps by alias. §8 defines exactly three exit conditions; 'Target Reached', 'Trailing Stop' and 'Partial Profit Taking' have no stated mapping, so exit analytics cannot be read against the strategy.

**Scope**
- Allowed values and §8 category in `data_model.md` and `metrics_definitions.md`; backfill legacy spellings; CHECK constraint.

**Acceptance Criteria**
- [ ] Every stored value maps to exactly one §8 condition.
- [ ] Constraint rejects unlisted values; existing rows backfilled.

---

### BLG-SPEC-188 — Define a stop-freshness metric (hours since `stop_calculated_at`)
**Priority:** P3 (Low)
**Type:** Metrics Definition
**Owner:** Metrics Definitions & Analytics Owner
**Source:** `IDEA-metrics-20261006-02` (`IW-20261006-01`), roadmap rebalance `2026-10-06__scheduled`
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
v9.9 made stop recalculation time observable, but no metric reports how stale open-position stops are, so §7.1's 'recalculated daily' claim is untested in operation.

**Scope**
- Median and maximum age of `stop_calculated_at` across open positions, defined in `metrics_definitions.md`; shown on System Status.

**Acceptance Criteria**
- [ ] Metric defined with formula and source; displayed value matches a manual check.

---

### BLG-GOV-373 — Known-false-positive allow-list for `scan_backlog_gate_conditions.py`
**Priority:** P3 (Low)
**Type:** Governance Tooling
**Owner:** PMO Lead
**Source:** `IDEA-pmo-lead-20261006-01` (`IW-20261006-01`, refines `BLG-GOV-347`), roadmap rebalance `2026-10-06__scheduled`
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
The date-lapse scan flags `BLG-OPS-53` (a ship-date mention) and `BLG-FEAT-92` (a provenance note) every run; three consecutive rebalances (2026-09-28, 2026-09-30, 2026-10-06) excluded them by hand.

**Scope**
- An allow-list of item IDs with the reason each date does not govern; reported separately as 'known non-gate dates'.

**Acceptance Criteria**
- [ ] Both items no longer appear in the lapsed list; allow-list entries carry a reason and a review date.

---

### BLG-GOV-374 — Structured ready-pool history written by Release Planning, read by roadmap STEP 7.3
**Priority:** P3 (Low)
**Type:** Governance Process / Capacity Monitoring
**Owner:** PMO Lead; Head of Specs Team
**Source:** `IDEA-pmo-lead-20261006-02` (`IW-20261006-01`), roadmap rebalance `2026-10-06__scheduled` (see that cycle's lessons learnt)
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
STEP 7.3 was recorded as 'not re-measured — no plan release since v9.5' at the 2026-09-28 and 2026-09-30 rebalances, although v9.6–v9.9 release planning had each recorded ready-pool figures in their run manifests. `metrics_definitions.md` Appendix F's runway table stops at v9.7 and is outside the roadmap engine's write scope, although §7.3 tells it to 'update it there at each rebalance'.

**Scope**
- `claude/roadmap/ready_pool_history.md` (one row per release: pool days, selected days, leftover, capacity ceiling), appended by Release Planning.
- §7.3 and Appendix F read it; resolve the Appendix F write-scope instruction.

**Acceptance Criteria**
- [ ] File exists, backfilled v9.3–v9.9; next rebalance's §7.3 reads it.
- [ ] §7.3 no longer instructs a write outside the engine's scope.

---

### BLG-FEAT-99 — Monthly P&L breakdown by §8 exit condition
**Priority:** P3 (Low)
**Type:** Product Feature / Financial Reporting
**Owner:** Financial Reporting & Records Owner
**Source:** `IDEA-financial-reporting-20261006-01` (`IW-20261006-01`), roadmap rebalance `2026-10-06__scheduled`
**Gate criteria:** `BLG-SPEC-186` shipped (exit reasons mapped to §8 conditions)
**Effort:** M (~2 days)
**Provisional-Target:** TBD

**Problem**
Monthly P&L cannot show realised P&L by stop exit, risk-off exit and discretionary exit — the basic question for judging whether §7/§8 work. `Reports.js` has no exit-reason grouping, and `exit_reason` is inconsistent until `BLG-SPEC-186` lands.

**Scope**
- Per-month table of realised P&L and trade count by §8 category in the Monthly P&L report.

**Acceptance Criteria**
- [ ] Table totals reconcile to the month's realised P&L (test).

---

### BLG-GOV-376 — Update strategy_rules.md §13.3 now that the Gap Risk Flag's weekend-hold trigger is removed
**Priority:** P3 (Low)
**Type:** Governance Process / Strategy Text Alignment
**Owner:** Strategy Rules & System Intent Owner
**Source:** ST-13/ST-14 (EPIC-03, cycle `2026-10-06__release-v9.10`) — 2026-10-07
**Effort:** XS (~0.25 day)
**Provisional-Target:** TBD (before the first §13.5 re-attestation, 2027-02-06)

**Problem**
ST-14 removed the Gap Risk Flag's standalone `weekend_hold` trigger, and ST-13 ruled that the earnings trigger covers US positions only, from the day after today up to the next trading day. `strategy_rules.md` v1.14 §13.3's third paragraph still describes the weekend-hold trigger as a live, time-boxed deviation due by 2027-02-06. The behaviour now meets §13.3. Only this descriptive text is stale. Sprint Execution cannot write `claude/strategy/strategy_rules.md` (`execution_prompt.md` §7).

**Scope**
- Replace §13.3's third paragraph with the text in the v9.10 addendum of `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md` ("Proposed §13.3 third paragraph").
- Update the §13.5 roster row's weekend-hold clause to record Binding Condition 6 as met (v9.10).
- Bump the version, add the Change Log row (documentation only, per ST-05's behaviour-only registry rule) and run the §15 grep.

**Acceptance Criteria**
- [ ] §13.3 and the §13.5 roster row no longer describe the weekend-hold trigger as live.
- [ ] Change Log row and §15 grep recorded.

---

### BLG-QA-215 — Assert the stop-details tooltip time under a non-UTC browser timezone
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Agent-mediated pre-PR review of EPIC-02 (Director of Quality + Product Owner roles), cycle `2026-10-06__release-v9.10`, finding on ST-06 (BLG-FE-193) — 2026-10-07
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
The per-row "How this stop was set" tooltip formats `stop_calculated_at` in the viewer's local time. The API returns it as an offset ISO string (TIMESTAMPTZ). The SC-SCP Playwright cases use offset-less timestamps, so they pass in any timezone and never exercise the UTC-to-local conversion a UK user sees during BST.

**Scope**
- Add a case to `tests/e2e/stop-cell-provenance.spec.js` using an offset timestamp (e.g. `2026-10-05T21:15:00+00:00`) with `test.use({ timezoneId: 'Europe/London' })`, asserting the BST-local time.

**Acceptance Criteria**
- New SC-SCP case asserts "Last recalculated 5 Oct 2026, 22:15 — nightly update" for a `21:15+00:00` input under Europe/London, passing in CI

---

### BLG-QA-219 — Stop the ⌘K hint toast intercepting the chat submit click in SC-AC-03
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Sprint Execution, ST-25 / EPIC-04, cycle `2026-10-08__release-v9.11` (DoQ regression run of the shared AI badge's Playwright coverage) — 2026-10-09
**Effort:** XS (<1h)
**Provisional-Target:** v9.12

**Problem**
`tests/e2e/epic02-v62-ai-briefing-chat.spec.js` SC-AC-03 fails intermittently locally: 2 of 3, 1 of 3 and 3 of 3 in repeated runs on EPIC-04. It fails 1 of 3 on EPIC-04 at `dde0501c`, before any ST-25 change, and 0 of 3 on EPIC-06. The click on `ai-chat-submit` times out because the first-visit sonner toast ("Press ⌘K (or Ctrl K) to search pages, tickers, and trade plans.", `src/Layout.js`) sits over the chat widget's submit button and "intercepts pointer events". Whether the toast is still showing when the test clicks is a matter of timing, which makes this a flaky test, not a regression. CI has passed it on every EPIC-04 run so far.

**Scope**
- In the spec, suppress or dismiss the hint before interacting: set the hint's "seen" flag with `addInitScript`, or close the toast. Do not change the app.
- Check the other chat-widget scenarios in the same file for the same exposure.

**Acceptance Criteria**
- SC-AC-03 passes 10 of 10 with `--repeat-each=10` locally
- No `test.fixme` quarantine is needed

---

### BLG-QA-216 — Assert the applied theme in every Reports/Notifications axe scan, not just Reports Monthly
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Agent-mediated PR #1918 review (Director of Quality role), EPIC-04 ST-19, cycle `2026-10-06__release-v9.10` — 2026-10-07
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`tests/e2e/accessibility-axe-scan.spec.js` sets the theme through the localStorage key `Layout.js` reads. It confirms the theme applied (`html` has, or lacks, `.dark`) only in the Reports Monthly test (around line 306). The Tax Year, Notification Preferences and Notification History tests scan without that check. If theme application broke, their "light" runs would silently become second dark runs. The `:light` baseline entries (BLG-FE-200) would then grandfather nothing real, and light-theme regressions would go unscanned.

**Scope**
- Move the theme assertion into a shared helper used by all four tests in each theme, or into the `beforeEach`.

**Acceptance Criteria**
- All 8 Reports/Notifications axe tests assert the applied theme before scanning, and pass in CI

---

### BLG-QA-218 — Stop test files from adding backend/services/ to sys.path
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Agent-mediated PR #1921 review (Director of Quality role) — 2026-10-07
**Effort:** M (~1–2d)
**Provisional-Target:** TBD

**Problem**
Nine test files still add `backend/services/` to `sys.path` so they can load a service module by bare name without running `services/__init__.py`. Among them are `test_plan_vs_reality.py`, `test_alerts_service.py` and `test_watchlist_service.py`. pytest runs every file in one process, so that entry stays active for the whole run. Code under test can then resolve imports that fail in production, which is exactly how the ST-23 bare import passed CI (BLG-BE-150).

**Scope**
- Change those files to load modules by file path (`importlib.util.spec_from_file_location`) or through `services.<module>`, without changing `sys.path`.
- Add a guard (conftest or lint) that fails if a test adds `backend/services` to `sys.path`.

**Acceptance Criteria**
- No file under `tests/` adds `backend/services` to `sys.path`, and the guard enforces it
- The full suite still passes

---

### BLG-QA-220 — Behavioural tests for live holding days in the compliance and AI briefing readers
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** PR #1969 agent-mediated Director of Quality review (EPIC-02, cycle `2026-10-08__release-v9.11`) — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** v9.12

**Problem**
ST-12 moved the compliance and AI-briefing readers to `live_holding_days()`, but they are guarded only by a source-scan test (`test_other_readers_no_longer_read_the_stored_column`); only the portfolio and alerts paths have behavioural tests.

**Scope**
- Tests for `compliance_service` position compliance and the `ai_service` daily-briefing context

**Acceptance Criteria**
- With stored `holding_days` 9 and `entry_date` 10 days ago, compliance reports the position out of grace and the AI context marks it not in grace

---

### BLG-GOV-378 — Decide whether the debrief focus area may be longer than one strictly restating sentence
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance Governance Officer; Product Owner
**Source:** User testing of the post-trade debrief in production — 2026-10-07 ("Not really sure that is an AI debrief")
**Effort:** S (~0.5d)
**Provisional-Target:** TBD
**Depends on:** BLG-BE-152 (derived figures), so the decision is made against improved output, not the current one

**Problem**
The §13 review limits the model's output to one observational sentence, which may only restate given numbers. Users see a summary built in code plus, at best, one sentence that largely repeats it, and question whether the feature is an AI debrief at all. Some of this is fixed by better inputs (BLG-BE-152). The remaining limit, one sentence about how execution differed from plan, leaves little to say on trades that went to plan.

**Scope**
- Once BLG-BE-152 ships, review a sample of real debriefs.
- Decide whether to keep the current limits, or to allow 2–3 observational sentences (still non-prescriptive and number-checked) covering what went well as well as what differed.
- If changed, record the ruling as an amendment to the §13 review and file the implementation item.

**Acceptance Criteria**
- A recorded decision (keep or amend), with rationale, from the AI Compliance Governance Officer and Product Owner

---

### BLG-SPEC-189 — Reconcile `risk_dashboard.md` §5.1/§6.1 data-source wording with the shipped `GET /portfolio` fields
**Priority:** P3 (Low)
**Type:** Spec / Documentation Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Idea intake `IW-20261008-01` — `IDEA-frontend-specs-20261008-02`; roadmap rebalance `2026-10-08__scheduled` STEP 4 (Backlog, ungated)
**Effort:** XS (~0.25 day)
**Provisional-Target:** TBD

**Problem**
`risk_dashboard.md` §5.1 says the grace panel uses "positions where `status = "GRACE"`". `GET /portfolio` returns `status: "open"` for every position, plus a `grace_period` boolean and a `display_status` field, and `GracePeriodPanel.js` filters on `grace_period`. The spec names a field value that never occurs.

**Scope**
- Amend §5.1 and §6.1 to name `grace_period` and `display_status` as the sources.

**Acceptance Criteria**
- [ ] §5.1 and §6.1 name only fields that `GET /portfolio` returns

---

### BLG-SPEC-192 — Make review-cadence grace suppression and the grace alert agree in the ended-grace state
**Priority:** P3 (Low)
**Type:** Specification / Consistency
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** PR #1969 agent-mediated Director of Quality review (EPIC-02, cycle `2026-10-08__release-v9.11`) — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** v9.12

**Problem**
ST-14's suppression predicate (`Positions.js` ~592, `PositionCard.js` ~97) reads `GET /positions`' `grace_days_remaining`, which is null once holding days reach 10, while the grace-alert endpoint uses `max(0, 10 − days)` on the stored GRACE state. A position whose stored state still says GRACE on day 10+ shows "Grace period has ended" but its Last Reviewed flag is not suppressed, though `positions.md` calls the two predicates the same.

**Scope**
- Either suppress when state is GRACE with null `grace_days_remaining` and holding days ≥ 10, or document the difference in `positions.md` §Last Reviewed Column

**Acceptance Criteria**
- A Playwright case (stored GRACE, `grace_days_remaining` null, holding days ≥ 10, stale review) behaves as the spec states

---

### BLG-GOV-379 — Split `execution_prompt.md` into a core plus an appendix so it fits a single read
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Lifecycle audit AUD-2026-10-08, improvement AUD-2026-10-08-002 (`claude/cycles/2026-10-08__release-v9.11/audit_report_AUD-2026-10-08.md` Stage 5); filed under the `shared_standards.md` §11 engine prompt size budget — 2026-10-08
**Effort:** L (~3–5d)
**Provisional-Target:** TBD

**Problem**
`claude/system/execution_prompt.md` is 133,341 bytes (≈48.6k tokens), over the 68,500-byte single-read cap that `shared_standards.md` §11 now sets (≈25k tokens at the 2.74 bytes/token ratio calibrated from `BLG-GOV-343`). Every `run sprint` invocation needs at least two reads to load it, and it is the largest engine prompt by a wide margin. A session that reads only the first page can miss later STEPs, including write-safety and commit steps. That failure mode was recorded at `2026-10-06__scheduled` Friction Item 4 (Type D) for `roadmap_prompt.md`.

**Scope**
- Split `execution_prompt.md` into a core plus an appendix, following the `BLG-GOV-343` method (rationale and detail to the appendix; mandatory process steps stay in the core with one-line pointers).
- Update every reference to the moved sections, CLAUDE.md §1 if the load instruction changes, and the OPERATIONAL_GUIDE.md §13 and §14 rows for the new appendix file.
- Apply the CLAUDE.md §6 checklist.

**Acceptance Criteria**
- `wc -c claude/system/execution_prompt.md` is at most 68,500 bytes.
- The appendix exists with a Class 6 header and is registered in OPERATIONAL_GUIDE.md §13 and §14.
- No mandatory STEP is moved out of the core (every STEP heading in the pre-split file is either still in the core or reached by an explicit pointer from it).
- `governance-drift` reports all versions in sync.

---

### BLG-GOV-380 — Split `shared_standards.md` into a core plus an appendix so it fits a single read
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Lifecycle audit AUD-2026-10-08, improvement AUD-2026-10-08-002 (`claude/cycles/2026-10-08__release-v9.11/audit_report_AUD-2026-10-08.md` Stage 5); filed under the `shared_standards.md` §11 engine prompt size budget — 2026-10-08
**Effort:** M (~1–2d)
**Provisional-Target:** TBD

**Problem**
`claude/system/shared_standards.md` is about 95,500 bytes (≈34.9k tokens), over the 68,500-byte single-read cap that `shared_standards.md` §11 now sets (≈25k tokens at the 2.74 bytes/token ratio calibrated from `BLG-GOV-343`). Every engine cites it, and §16's embedded templates and mixed heading levels already make heading-based navigation unreliable. A session that reads only the first page can miss later STEPs, including write-safety and commit steps. That failure mode was recorded at `2026-10-06__scheduled` Friction Item 4 (Type D) for `roadmap_prompt.md`.

**Scope**
- Split `shared_standards.md` into a core plus an appendix, following the `BLG-GOV-343` method (rationale and detail to the appendix; mandatory process steps stay in the core with one-line pointers).
- Update every reference to the moved sections, CLAUDE.md §1 if the load instruction changes, and the OPERATIONAL_GUIDE.md §13 and §14 rows for the new appendix file.
- Apply the CLAUDE.md §6 checklist.

**Acceptance Criteria**
- `wc -c claude/system/shared_standards.md` is at most 68,500 bytes.
- The appendix exists with a Class 6 header and is registered in OPERATIONAL_GUIDE.md §13 and §14.
- No mandatory STEP is moved out of the core (every STEP heading in the pre-split file is either still in the core or reached by an explicit pointer from it).
- `governance-drift` reports all versions in sync.

---

### BLG-GOV-381 — Trim or split `post_ship_closure.md` so it fits a single read
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Lifecycle audit AUD-2026-10-08, improvement AUD-2026-10-08-002 (`claude/cycles/2026-10-08__release-v9.11/audit_report_AUD-2026-10-08.md` Stage 5); filed under the `shared_standards.md` §11 engine prompt size budget — 2026-10-08
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`claude/system/post_ship_closure.md` is about 70,600 bytes (≈25.8k tokens), over the 68,500-byte single-read cap that `shared_standards.md` §11 now sets (≈25k tokens at the 2.74 bytes/token ratio calibrated from `BLG-GOV-343`). It is only marginally over, so moving rationale-only text to an appendix may be enough. A session that reads only the first page can miss later STEPs, including write-safety and commit steps. That failure mode was recorded at `2026-10-06__scheduled` Friction Item 4 (Type D) for `roadmap_prompt.md`.

**Scope**
- Split `post_ship_closure.md` into a core plus an appendix, following the `BLG-GOV-343` method (rationale and detail to the appendix; mandatory process steps stay in the core with one-line pointers).
- Update every reference to the moved sections, CLAUDE.md §1 if the load instruction changes, and the OPERATIONAL_GUIDE.md §13 and §14 rows for the new appendix file.
- Apply the CLAUDE.md §6 checklist.

**Acceptance Criteria**
- `wc -c claude/system/post_ship_closure.md` is at most 68,500 bytes.
- The appendix exists with a Class 6 header and is registered in OPERATIONAL_GUIDE.md §13 and §14.
- No mandatory STEP is moved out of the core (every STEP heading in the pre-split file is either still in the core or reached by an explicit pointer from it).
- `governance-drift` reports all versions in sync.

---

### BLG-BE-156 — Monthly P&L: a snapshot-store failure should not block the report
**Priority:** P4 (Low)
**Type:** Backend Engineering / Resilience
**Owner:** Financial Reporting & Records Owner; Head of Engineering
**Source:** ST-29 (BLG-SPEC-170), EPIC-05, cycle `2026-10-08__release-v9.11` — out-of-scope finding while reconciling the Monthly Restatement Marker spec — 2026-10-08
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`reports.md` §Monthly Restatement Marker says P&L figures are never blocked by the restatement check. In code, `get_monthly_pnl_report()` reads and writes `monthly_pnl_snapshots` inline, and any failure there propagates to `GET /reports/monthly-pnl`'s generic 500, so the whole Monthly P&L report fails. The UI's "Restatement check unavailable." line (shown when no month carries a boolean `restated`) therefore never appears for a real snapshot failure.

**Scope**
- Catch snapshot-store failures in `get_monthly_pnl_report()`, log them with `exc_info`, and return the months without the four restatement fields
- Note the behaviour in `reports_endpoints.md` (`GET /reports/monthly-pnl`) and drop the Known limitation note in `reports.md`

**Acceptance Criteria**
- With the snapshot read mocked to fail, `GET /reports/monthly-pnl` returns 200 with realised P&L for every month and no `restated` field (unit test)
- Playwright: that response shows the table and "Restatement check unavailable."

---

### BLG-SPEC-190 — Positions data dictionary states `entry_price` is native currency; the code stores GBP
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-30 (BLG-SPEC-173), EPIC-05, cycle `2026-10-08__release-v9.11` — 2026-10-08
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`add_position()` stores `positions.entry_price` as the entry price **in GBP** (native ÷ `fx_rate` for US positions), and stores the native entry price in `fill_price`; the user's broker fill goes in `user_fill_price`. `data_model.md` §2 was corrected at v2.55 (ST-30). `docs/specs/data_model_positions_dictionary.md` (the canonical field dictionary) still says `entry_price` is native and `fill_price` is the actual execution fill, and its §derivation formulas (`total_cost`, `pnl`) use `entry_price` as if it were native.

**Scope**
- Correct the dictionary's `entry_price`, `fill_price` and `user_fill_price` rows and the derivation formulas to match the code
- Check other specs that describe `positions.entry_price` as native

**Acceptance Criteria**
- The dictionary and `data_model.md` §2 agree with `add_position()` for every price field
- No spec describes `positions.entry_price` as native currency for US positions

---
### BLG-FE-208 — Add a useful / not-useful rating to each AI chat answer
**Priority:** P3 (Low)
**Type:** Frontend / UX — AI Advisory Measurement
**Owner:** Metrics Definitions & Analytics Owner; Frontend Specifications & UX Documentation Owner
**Source:** ST-24 (BLG-FEAT-60), EPIC-04, cycle `2026-10-08__release-v9.11` — out-of-scope finding while defining the AI chat engagement metrics — 2026-10-08
**Effort:** S (~0.5d plus a live migration if a new column or table is needed)
**Provisional-Target:** TBD

**Problem**
`metrics_definitions.md` § AI Chat Engagement (v1.27.0) defines a Response Acceptance Rate: chat answers rated useful ÷ chat answers rated. The chat widget has no rating control and nothing stores a rating, so the measure is "not instrumented" and the 2027-01-03 AI feature usage review cannot report it.

**Scope**
- Add a useful / not-useful control to each AI chat answer, following the trade-plan thesis feedback pattern (DS-09 `thesis_feedback`)
- Store each rating against the answer it rates (for example, a row keyed to the `claude_audit_log` call), with a `data_model.md` DS entry and live migration
- Document the query that computes the rate in `metrics_definitions.md` § AI Chat Engagement and drop its "not instrumented" status

**Acceptance Criteria**
- A user can rate each chat answer once, and the rating persists (Playwright + unit test)
- The Response Acceptance Rate query returns a value from stored ratings, and `null` when none exist

---

### BLG-GOV-382 — Run the 2027-01-03 AI feature usage review
**Priority:** P3 (Low)
**Type:** Governance Process — AI Feature Review Cadence
**Owner:** Metrics Definitions & Analytics Owner; Product Owner
**Source:** ST-28 (BLG-GOV-366), EPIC-04, cycle `2026-10-08__release-v9.11` — new gated tracking item; `BLG-FEAT-60` is not edited — 2026-10-08
**Effort:** S (~0.5d)
**Provisional-Target:** TBD
**Gate criteria:** AI feature usage review due 2027-01-03 (90 days after the 2026-10-05 baseline review, `docs/ops/ai_feature_usage_review_2026-09-24.md`). Not actionable before that date.

**Problem**
The 2026-10-05 review found 31 AI calls in 102 days, and the Product Owner chose to build more AI features to try to raise engagement. v9.11 adds the first of them (the monthly P&L narrative, ST-25) and defines the measures to judge it (ST-24 AI chat engagement, ST-26 narrative usage count). Nothing schedules the follow-up review, so it would surface only when someone happens to notice the date.

**Scope**
- On or after 2027-01-03, query production `claude_audit_log` read-only for the period since 2026-10-05
- Report the AI chat engagement measures (`metrics_definitions.md` § AI Chat Engagement: sessions per week, questions per session, response acceptance rate if `BLG-FE-208` has shipped) and the monthly P&L narrative usage count (ST-26), each against the 2026-09-24 review baseline
- File the review as `docs/ops/ai_feature_usage_review_2027-01-03.md` and record a Product Owner decision on further AI investment

**Acceptance Criteria**
- The review artefact exists with the measures above, compared with the baseline
- A dated Product Owner decision on further AI investment is recorded in it

---

### BLG-FE-209 — Replay page fails WCAG colour contrast in the light theme
**Priority:** P3 (Low)
**Type:** Frontend / Accessibility
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Source:** ST-37 (BLG-QA-196), EPIC-06, cycle `2026-10-08__release-v9.11` — first axe scan of the Replay page in both themes — 2026-10-08
**Effort:** S (~0.5-1 day, or as part of BLG-FE-200)
**Provisional-Target:** TBD

**Problem**
The axe scan added by ST-37 finds serious `color-contrast` violations on the Replay page (`src/pages/Replay.js`) in the **light** theme only: in Date Range mode (3 nodes), Trade Set mode (5 nodes) and the populated result (20 nodes). The page uses dark-only classes (`bg-slate-800/50` cards, `text-white`/`text-slate-300` text, `text-emerald-400`/`text-rose-400` P&L) that sit on a mid-grey background in the light theme, giving ratios from 1.2:1 to 3.25:1. This is the same gap as `BLG-FE-200` (Reports and Notifications), which `design_system.md` cannot fix without light-mode tokens. The dark theme passes.

**Scope**
- Apply the light-mode tokens `BLG-FE-200` introduces (or define them, if this lands first) to the Replay page
- Remove the three `Replay*:light` `color-contrast` entries from `KNOWN_VIOLATIONS` in `tests/e2e/accessibility-axe-scan.spec.js` in the same commit

**Acceptance Criteria**
- The light-theme Replay axe scans (Date Range, Trade Set, populated result) pass with no `color-contrast` baseline entry

---

### BLG-GOV-383 — Split `release_planning_prompt.md` so it fits a single read
**Priority:** P3 (Low)
**Type:** Governance Process — Prompt Size Budget
**Owner:** Head of Specs Team
**Source:** ST-35 (BLG-GOV-359), EPIC-06, cycle `2026-10-08__release-v9.11` — required by `shared_standards.md` §11's engine prompt size budget at the v2.60→v2.61 bump — 2026-10-08
**Effort:** M (~1d)
**Provisional-Target:** TBD

**Problem**
`claude/system/release_planning_prompt.md` is 84,469 bytes at v2.61, above `shared_standards.md` §11's 68,500-byte engine prompt budget (≈25,000 tokens, the single-read cap). An engine that cannot read its prompt in one pass risks acting on a partial read. `BLG-GOV-381` tracks the same problem for `post_ship_closure.md`.

**Scope**
- Move rationale, history and worked examples into a new `claude/system/release_planning_prompt_appendix.md`, following the `roadmap_prompt.md` / `roadmap_prompt_appendix.md` pattern, leaving every mandatory STEP in the core or reached by an explicit pointer
- Register the appendix in `OPERATIONAL_GUIDE.md` §13 and §14 under the CLAUDE.md §6 checklist

**Acceptance Criteria**
- The core file is at or under 68,500 bytes (`wc -c`)
- No mandatory STEP is moved out of the core (every STEP heading in the pre-split file is still in the core or reached by an explicit pointer from it)
- `governance-drift` reports all versions in sync

---

### BLG-GOV-384 — Let compute_effort_weighted_pvr.py take the window as an argument
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Metrics Definitions & Analytics Owner
**Source:** ST-34 (BLG-GOV-355), EPIC-06, cycle 2026-10-08__release-v9.11 — Head of Specs Team / Product Owner review of ESC-EXEC-20261008-03 — 2026-10-09
**Effort:** S (~0.5d)
**Provisional-Target:** v9.12

**Problem**
`scripts/compute_effort_weighted_pvr.py` hard-codes its `VERSION_TO_FOLDER` and `WINDOWS` maps, which stop at v9.7. `roadmap_prompt.md` v9.32 STEP 2.4 now records the effort-weighted PVR at every rebalance, but `scripts/` is outside the roadmap engine's §4 write scope, so the script can only be used for windows already in its maps and every new rebalance falls back to the by-hand method.

**Scope**
- Add a `--window vA-vB` argument; derive each version's cycle folder from `claude/cycles/*__release-<v>` instead of the hard-coded map
- Keep the current no-argument run reproducing Appendix F's 5 backfilled readings
- Update STEP 2.4's script sentence via the CLAUDE.md §6 checklist once the script no longer needs editing per window

**Acceptance Criteria**
- `python3 scripts/compute_effort_weighted_pvr.py --window v9.6-v9.10` prints 0.327 with 155/155 coverage, with no source edit
- The no-argument run still prints 0.457 / 0.115 / 0.109 / 0.021 / 0.093

---

### BLG-SPEC-191 — Align Appendix F's effort-weighted PVR table and status with the script and STEP 2.4
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Metrics Definitions & Analytics Owner
**Source:** ST-34 (BLG-GOV-355), EPIC-06, cycle 2026-10-08__release-v9.11 — Head of Specs Team review of ESC-EXEC-20261008-03 (findings N4, N5) — 2026-10-09
**Effort:** XS (<1h)
**Provisional-Target:** v9.12

**Problem**
`docs/specs/metrics_definitions.md` Appendix F's effort normalisation table has no row for hour-scale bands (`XS (<1h)`), which `scripts/compute_effort_weighted_pvr.py` weights at 0.15, and the script matches a `VS` band that has no midpoint. A by-hand run under `roadmap_prompt.md` STEP 2.4 (which excludes values the table does not cover) can therefore exclude a story the script weights. Appendix F's Status and "Authoritative computation (once adopted) … (not yet wired)" lines are also stale for the effort-weighted sub-metric now that v9.32 STEP 2.4 records it.

**Scope**
- Add the `<1h → 0.15` row to the normalisation table (or remove the script's extra cases), and resolve the `VS` match
- Update Appendix F's Status / authoritative-computation lines for the effort-weighted sub-metric only; the D-split and U-pool indicator stay proposal-only
- Changelog row in `metrics_definitions.md`

**Acceptance Criteria**
- The table and the script weight exactly the same set of effort values
- Appendix F names `roadmap_prompt.md` STEP 2.4 (v9.32) as where the effort-weighted reading is recorded; the other two sub-metrics still read proposal-only

---

### BLG-BE-161 — Standalone `position_manager.py` still ratchets the stop during grace
**Priority:** P3 (Low)
**Type:** Backend Engineering / Strategy alignment
**Owner:** Strategy Rules & System Intent Owner; Head of Engineering
**Source:** ST-16 (BLG-BE-143), EPIC-03, cycle `2026-10-08__release-v9.11` — raised in the Strategy Rules & System Intent Owner's ruling on `ESC-EXEC-20261008-01` (2026-10-09)
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
`strategy_rules.md` §6.3 (v1.15) says the stored stop is not recalculated or ratcheted during the 10-day grace period. The live paths, `services/strategy_engine.py` and `services/replay_service.py` all follow this. The legacy standalone tool `backend/position_manager.py` does not: in grace it applies `max(current_stop, current_price − 5 × ATR)`. It is not on the live path, and is already an accepted exception for §7.2's multipliers.

**Scope**
- Either align it with §6.3 (no trailing during grace) or record it as an explicit exception next to the existing §7.2 one

**Acceptance Criteria**
- `position_manager.py` matches §6.3, or `strategy_rules.md` names it as an exception with the Owner's sign-off

---

### BLG-BE-163 — Retire the unused POST /trade-plans/{plan_id}/generate-thesis endpoint
**Priority:** P3 (Low)
**Type:** Backend Engineering / Technical Debt
**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer
**Source:** ST-02 staging run (EPIC-01, cycle `2026-10-08__release-v9.11`) — 2026-10-09
**Effort:** S (~0.5d)
**Provisional-Target:** v9.12

**Problem**
"Improve with AI" moved from `generate-thesis` to `POST /trade-plans/generate-plan` on 2026-05-25 (`f91a718a`), which fills every plan field, including the thesis, and works before the plan is saved. No UI calls `generate-thesis` now; the "Generate thesis" button is a deliberate no-model template (`trade_plan.md` §5b). The endpoint still makes paid Claude calls, carries a rate limit, audit and cost tracking, and appears in the endpoint test list, and its contract is duplicated in `ai_thesis_generation.md` and `gemini_thesis_generation.md`.

**Scope**
- Remove the route and `generate_setup_thesis()` (or keep the function only if another caller is found)
- Remove its `openapi.yaml` path and contract section, and merge the duplicate contract files into one
- Remove its entry from `backend/routers/test.py`, update the `SystemStatus.js` fallback count and `SC-SS-01b`
- Update or remove the tests and golden fixtures that reference it
- Record the retirement in `api_changelog.md`

**Acceptance Criteria**
- `POST /trade-plans/{plan_id}/generate-thesis` returns 404, and the OpenAPI drift gate passes
- "Improve with AI" and the template "Generate thesis" button behave as before (Playwright `trade-plan.spec.js` passes)
- One thesis-generation contract file remains, documenting `generate-plan`

---

### BLG-BE-164 — A debrief that fails compliance then errors writes two audit rows, one mislabelled
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer
**Source:** PR #1968 agent-mediated review (EPIC-01, cycle `2026-10-08__release-v9.11`) — Director of Quality finding 1 — 2026-10-12
**Effort:** XS (<1h plus tests)
**Provisional-Target:** v9.12

**Problem**
In `debrief_service.generate_trade_debrief()`, if the first model attempt returns text that fails the compliance check and the second attempt raises, the exception branch writes a `model_call_failed` audit row and the later `usage_for_audit is not None` block writes a second row with `compliance_check_result=None`. One request produces two `claude_audit_log` rows, and one of them misstates the outcome.

**Scope**
- In the exception branch, set the result to `model_call_failed` or clear `usage_for_audit`, so each request writes exactly one row
- Add a test for the fail-then-raise sequence

**Acceptance Criteria**
- A fail-then-raise debrief writes exactly one audit row, marked `model_call_failed`
- Existing debrief audit tests still pass

---

### BLG-BE-165 — Stop recalculation times in briefing and chat are labelled UTC without being converted
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Backend Engineering Patterns Owner
**Source:** PR #1968 agent-mediated review (EPIC-01, cycle `2026-10-08__release-v9.11`) — Director of Quality finding 3 — 2026-10-12
**Effort:** XS (<1h plus tests)
**Provisional-Target:** v9.12

**Problem**
`ai_service.py`'s stop-time formatter (added by ST-08) prints `stop_calculated_at` with a literal "UTC" suffix but never converts it. The column is TIMESTAMPTZ and psycopg returns it in the database session's timezone, so the time shown to the model, and quoted to the user, can be off by the session offset.

**Scope**
- Convert timezone-aware values with `astimezone(timezone.utc)` before formatting; treat naive values as UTC explicitly
- Add tests for a non-UTC aware timestamp and a naive one

**Acceptance Criteria**
- A `stop_calculated_at` of `2026-10-12 09:00+01:00` is rendered as `2026-10-12 08:00 UTC`
- Existing ST-08 tests still pass

---

### BLG-BE-166 — Run the claude_audit_log column checks once per process, not on every insert
**Priority:** P3 (Low)
**Type:** Backend Engineering / Performance
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Source:** PR #1968 agent-mediated review (EPIC-01, cycle `2026-10-08__release-v9.11`) — Director of Quality finding 4 — 2026-10-12
**Effort:** S (~0.5d)
**Provisional-Target:** v9.12

**Problem**
`create_claude_audit_entry()` now runs four `ensure_*` DDL calls before every insert (`database.py`), extending the ensure-on-every-insert pattern. Each `ALTER TABLE … ADD COLUMN IF NOT EXISTS` opens its own connection and takes an ACCESS EXCLUSIVE lock even when it changes nothing, on every AI call. DS-27 is now applied live, so the per-insert check buys nothing.

**Scope**
- Skip the ensure calls after the first success in each process, with a module-level flag
- Check other `ensure_*`-before-insert call sites for the same pattern and list them

**Acceptance Criteria**
- A second audit insert in the same process runs no DDL (asserted by a test)
- The first insert still adds missing columns

---

### BLG-BE-167 — `GET /portfolio` P&L line throws on a US position whose `fill_price` is NULL
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Backend Engineering Patterns Owner
**Source:** PR #1969 agent-mediated Director of Quality review (EPIC-02, cycle `2026-10-08__release-v9.11`) — 2026-10-12
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.12

**Problem**
`portfolio_service.py` (P&L block, ~line 144) reads `pos.get('fill_price', pos['entry_price'])`. When the `fill_price` column exists but is NULL, `.get` returns None and the P&L calculation raises a TypeError. The ST-10 stale-price fallback a few lines above already uses `pos.get('fill_price') or pos['entry_price']`, so the two lines now disagree. Pre-existing, not introduced by EPIC-02.

**Scope**
- Use `or` for the US entry price in the P&L block so it matches the fallback

**Acceptance Criteria**
- A unit test with a US position whose `fill_price` is None and a live price: `GET /portfolio` returns the row using `entry_price`

---

### BLG-BE-168 — Flag stale prices on `GET /positions` and the Positions page
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner
**Source:** PR #1969 agent-mediated Product Owner review (EPIC-02, cycle `2026-10-08__release-v9.11`) — 2026-10-12
**Effort:** S (~0.5d)
**Provisional-Target:** v9.12

**Problem**
When the live price fetch fails, `position_service.py` (~lines 121–130) silently falls back to the stored `current_price` with no flag, and the Positions page shows that price, P&L and value as live. Since ST-10, `/risk` marks the same position stale, so the two pages disagree.

**Scope**
- Add `price_is_stale` to `GET /positions` (contract and `openapi.yaml` in the same commit)
- Show the `risk_dashboard.md` §6.6-style marker on the Positions table and grid price cells (positions.md design pass)

**Acceptance Criteria**
- A unit test with the fetch mocked to fail returns `price_is_stale: true`
- Playwright shows the marker on a stale row and none on a live row

---

### BLG-BE-169 — Flag the FX fallback (`DEFAULT_FX_RATE` 1.27) instead of applying it silently
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Backend Engineering Patterns Owner
**Source:** PR #1969 agent-mediated Product Owner review (EPIC-02, cycle `2026-10-08__release-v9.11`) — 2026-10-12
**Effort:** S (~0.5d)
**Provisional-Target:** v9.12

**Problem**
`utils/pricing.get_live_fx_rate()` returns a hard-coded 1.27 when the FX fetch fails. US current prices, P&L, total value and heat are then converted at a guessed rate with nothing on screen saying so — the same class of issue as the ×1.38 constant ST-10 removed (BLG-BE-154), and against `strategy_rules.md` §11's no-hidden-parameters intent. It also makes the ST-10 stale tooltip ("converted at today's FX rate") untrue in that case.

**Scope**
- Expose an `fx_is_stale` flag (or a last-known-good cached rate with its timestamp) on `GET /portfolio` and `GET /positions`
- Show it on the Dashboard and Risk Dashboard; document it in both contracts

**Acceptance Criteria**
- A unit test with the FX fetch mocked to fail sets the flag and never presents 1.27 as a live rate
- Playwright shows the indicator

---

### BLG-FE-211 — Debrief Regenerate leaves the card blank when a successful response has no data
**Priority:** P3 (Low)
**Type:** Frontend / Correctness
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Source:** PR #1968 agent-mediated review (EPIC-01, cycle `2026-10-08__release-v9.11`) — Director of Quality finding 5 — 2026-10-12
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.12

**Problem**
`TradeDebrief.js`'s Regenerate `onSuccess` writes `{ status: "found", data: newDebrief }` straight into the query cache. If a 2xx response carries no `data`, the cache holds `data: undefined` and neither the debrief nor the empty state renders, so the user sees a blank card.

**Scope**
- Only write to the cache when `newDebrief` is present; otherwise invalidate the query
- Add a Playwright scenario mocking a 200 with no `data`

**Acceptance Criteria**
- Playwright: a mocked 200 with no `data` leaves the previous debrief (or the empty state) visible
- SC-DBF-06a/07a/08a still pass

---

### BLG-FE-212 — Check the debrief error text's colour contrast in light theme
**Priority:** P3 (Low)
**Type:** Frontend / Accessibility
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Source:** PR #1968 agent-mediated review (EPIC-01, cycle `2026-10-08__release-v9.11`) — Product Owner note 4 — 2026-10-12
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.12

**Problem**
The debrief failure messages in `TradeDebrief.js` use `text-rose-400` with no light-theme variant. SC-DBF-06a's axe scan only covers the normal state, so the error text's contrast in light theme has never been checked, and rose-400 on a light background is likely below 4.5:1.

**Scope**
- Give the error text a light-theme colour (e.g. `text-rose-600 dark:text-rose-400`)
- Extend the axe scan to the error state in both themes

**Acceptance Criteria**
- Playwright: the axe scan of the debrief section in its error state reports no colour-contrast violations in either theme

---

### BLG-FE-213 — Recent Trades glyph and amount disagree at a half-penny loss
**Priority:** P3 (Low)
**Type:** Frontend / Correctness
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** PR #1969 agent-mediated Director of Quality and Product Owner review (EPIC-02, cycle `2026-10-08__release-v9.11`) — 2026-10-12
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.12

**Problem**
ST-15's `displayedPnl` (`src/components/dashboard/widgets/RecentTradesWidget.js`) uses `Math.round(x*100)/100`, which rounds −0.005 to −0 (neutral glyph and colour), while `formatCurrency` (`src/lib/format.js`) rounds the absolute value with `toFixed(2)` and renders "−£0.01". Checked in node: `Math.round(-0.5)/100 = -0`, `(0.005).toFixed(2) = '0.01'`.

**Scope**
- Derive the glyph and colour from the same rounding as `formatCurrency` (e.g. a shared helper in `src/lib/format.js` using the `signOf` test)

**Acceptance Criteria**
- Playwright: `pnl −0.005` shows the down glyph and rose colour matching "−£0.01"; SC-RTB-06 (0.004 neutral, 0.01 up) still passes

---

### BLG-FE-214 — Make the stale-price explanation reachable on touch, keyboard and screen readers
**Priority:** P3 (Low)
**Type:** Frontend / Accessibility
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Source:** PR #1969 agent-mediated Product Owner review (EPIC-02, cycle `2026-10-08__release-v9.11`) — 2026-10-12
**Effort:** S (~0.5d)
**Provisional-Target:** v9.12

**Problem**
ST-10's `StaleMarker` (`PositionRiskTable.js`) and the Dashboard Card 2 notice explain staleness only via `title` plus an `aria-label` on a non-focusable span: touch and keyboard users cannot reach it, assistive tech may announce only "stale", and the copy gives no next step or note that value, P&L and heat use that price.

**Scope**
- A focusable tooltip/popover or `sr-only` description; one line of next-step copy; design-gate review of the wording

**Acceptance Criteria**
- axe passes on `/risk` with a stale row
- The explanation is reachable by keyboard focus and exposed as the marker's accessible description (Playwright `toHaveAccessibleDescription`)

---

### BLG-BE-170 — Price-alert duplicate fallback returns 500 when the threshold has more than 4 decimal places
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Source:** PR #1970 agent-mediated review (EPIC-03, cycle `2026-10-08__release-v9.11`), Director of Quality finding 2: ST-20 (DS-28) — 2026-10-12
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.12

**Problem**
`price_alerts.threshold_price` is `NUMERIC(10,4)`, so a threshold such as 100.12345 is stored as 100.1235. `create_price_alert()` compares `threshold_price = %s` with the unrounded float, both in the ST-09 dedup SELECT and in ST-20's unique-violation fallback SELECT. On a second submit of the same >4-dp threshold, the dedup SELECT misses, the INSERT hits `idx_price_alerts_active_unique`, the fallback SELECT also misses, and `_price_alert_row(None)` raises, so the request returns 500. Before DS-28 the same input created a silent duplicate. `CreatePriceAlertRequest.threshold_price` is an unconstrained `float`.

**Scope**
- Round `threshold_price` to 4 dp in `create_price_alert()` before both SELECTs and the INSERT (or compare with `%s::numeric(10,4)`)
- If the fallback SELECT still finds no row, raise a clear error rather than passing `None` to `_price_alert_row`

**Acceptance Criteria**
- Submitting the same threshold with 5+ decimal places twice returns the existing alert both times, with one active row (test, including the real-Postgres DS-28 suite)
- No code path calls `_price_alert_row(None)`

---

### BLG-BE-171 — Use the deploy date, not the ruling date, as strategy v1.15's effective date
**Priority:** P3 (Low)
**Type:** Backend Engineering / Strategy Records
**Owner:** Strategy Rules & System Intent Owner; Financial Reporting & Records Owner
**Source:** PR #1970 agent-mediated review (EPIC-03, cycle `2026-10-08__release-v9.11`), Director of Quality finding 3: ST-16 — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** v9.12

**Problem**
`strategy_version_registry.py` registers v1.15 (the §6.3 in-grace stop freeze) with `effective_date` 2026-10-09, the ruling date from the `strategy_rules.md` Change Log. The behaviour reaches production only when PR #1970 deploys. SI-04 attributes trades to a version by `entry_date` window, so positions entered between 9 October and the deploy fall in the v1.15 cohort. Those positions are stamped `strategy_version_at_entry = "1.4"` by the code running at the time, and the old nightly job ratcheted their stops during grace. The two attribution methods disagree for that window, and the v1.15 cohort contains trades produced by v1.4 rules.

**Scope**
- Strategy Rules & System Intent Owner rules whether a behavioural version's effective date is the ruling date or the production deploy date, and records the rule in the registry docstring
- If the ruling is the deploy date: set v1.15's `effective_date` (and the Change Log date, if `tests/test_strategy_version_registry.py` requires them to match) to the actual deploy date
- List any trades entered in the gap and confirm their attribution

**Acceptance Criteria**
- The rule for behavioural effective dates is written in `strategy_version_registry.py`'s docstring
- v1.15's window and the `strategy_version_at_entry` stamps agree for every trade entered from 9 October 2026 onwards (query output or test)

---

### BLG-FE-215 — Pluralise the month counts in the monthly P&L summary fallback text
**Priority:** P3 (Low)
**Type:** Frontend / UX — Copy
**Owner:** Frontend Specifications & UX Documentation Owner; Financial Reporting & Records Owner
**Source:** PR #1972 agent-mediated review (EPIC-04, cycle `2026-10-08__release-v9.11`), Director of Quality / Product Owner finding: ST-25 — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** v9.12

**Problem**
The code-written fallback summary (`build_fallback_text`, `backend/services/monthly_pnl_narrative_service.py`) ends with "{profitable} months ended above zero and {losing} below." It pluralises "closed trade(s)" and "month(s)" earlier in the sentence but not these counts, so a tax year with one profitable month reads "1 months ended above zero". The template in `reports.md` §AI Summary and the design record §2.6 have the same wording. The fallback is shown whenever the AI text fails its checks, so the user sees it when the summary already looks least trustworthy.

**Scope**
- Pluralise "month"/"months" for the profitable and losing counts in `build_fallback_text`
- Update the fallback template in `docs/specs/frontend/pages/reports.md` §AI Summary to match
- Add a unit test case with exactly one profitable month

**Acceptance Criteria**
- With one profitable month, the fallback text reads "1 month ended above zero" (asserted in `tests/test_monthly_pnl_narrative.py`)
- The `reports.md` template wording matches the code

---

### BLG-FE-216 — Keep a generated monthly P&L summary visible after switching tax year and back
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** PR #1972 agent-mediated review (EPIC-04, cycle `2026-10-08__release-v9.11`), Director of Quality finding: ST-25 — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** v9.12

**Problem**
`MonthlyNarrativeCard` keeps a newly generated summary in local state, which it resets when the tax year changes. A successful POST does not update the react-query cache entry `["monthlyPnlNarrative", year]`, which still holds the earlier GET result with `narrative: null`. If the user switches to another tax year and back, the card shows the empty "Get a short written summary" state until the background refetch returns. That can prompt an unnecessary Regenerate, which is a real model call counted against the daily cap.

**Scope**
- After a successful POST, write the returned payload into the query cache for that year (`queryClient.setQueryData`) or invalidate the key
- Extend `tests/e2e/monthly-pnl-narrative.spec.js` with a generate → switch year → switch back scenario

**Acceptance Criteria**
- After Generate, switching tax year and back shows the generated summary immediately, with no empty-state render in between (Playwright)
- No extra POST is made by the round trip

---

### BLG-BE-172 — Show the code-written fallback when the monthly P&L summary's regeneration call fails
**Priority:** P3 (Low)
**Type:** Backend Engineering / AI Feature Resilience
**Owner:** Head of Engineering; Financial Reporting & Records Owner
**Source:** PR #1972 agent-mediated review (EPIC-04, cycle `2026-10-08__release-v9.11`), Product Owner finding: ST-25 — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** v9.12

**Problem**
In `generate_narrative` (`backend/services/monthly_pnl_narrative_service.py`), if the first model attempt fails the §13 output checks and the regeneration call then raises, the endpoint returns 503 and stores nothing. A failed check on both attempts falls back to the code-written summary, but this path does not, although it has the same figures. The user gets an error in place of a usable, compliant summary. This matches the contract's 503 row (`reports_endpoints.md`), so it is an improvement, not a deviation.

**Scope**
- When attempt 1 failed its checks and attempt 2's model call raises, store and return the fallback summary (`source: "fallback"`) with a terminal audit result. The cap and audit rules still apply.
- Keep 503 for a model failure on attempt 1 (no checked output exists)
- Update the `reports_endpoints.md` 503 row and `metrics_definitions.md` § AI Monthly P&L Narrative Usage if the terminal-result set changes; add a unit test

**Acceptance Criteria**
- A unit test with attempt 1 failing checks and attempt 2 raising receives `source: "fallback"` and a stored row
- `count_monthly_pnl_narrative_generations` counts that request exactly once

---

### BLG-BE-173 — Trail Stop modal's ATR trail value uses a hardcoded 2.0 multiplier and no breakeven floor
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Source:** ST-10 (EPIC-02, cycle `2026-10-12__release-v9.12`), Strategy Rules & System Intent Owner ruling ESC-EXEC-20261013-06, binding condition 7 — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`GET /positions/{id}/stop-trail` (`backend/main.py`, the stop-trail handler) computes `atr_trail_stop` as `current price − 2.0 × stored ATR`, with the 2.0 hardcoded, and without the §7.2 breakeven floor (`max(..., EntryPrice)`) that the live recompute applies (`backend/utils/calculations.py::calculate_trailing_stop`). The read-only View Trail modal (ST-10, Branch B) therefore shows a trail value that can differ from what the system will actually set, and its static footnote restates the 2.0. It is display-only now, so it writes nothing, but it can mislead.

**Scope**
- Compute `atr_trail_stop` with the same §7.2 formula and §11 multipliers the live recompute uses (`backend/strategy_parameters.py`), including the breakeven floor, or call the shared function
- Update the modal footnote (`positions.md` §Trail Stop Action) and `position_endpoints.md`'s stop-trail description to match; add a unit test

**Acceptance Criteria**
- For a profitable position, `atr_trail_stop` equals the value `calculate_trailing_stop` would produce from the same inputs (unit test), including a case where the breakeven floor binds
- No literal multiplier remains in the handler or the modal footnote

---

### BLG-BE-174 — Gap-risk weekend statistic: pick it by the exchange calendar and count ordinary weekends
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Source:** ST-14 (EPIC-02, cycle `2026-10-12__release-v9.12`), Strategy Rules & System Intent Owner ruling ESC-EXEC-20261013-07 (non-binding recommendations, verified by the engine) — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
Three defects in the gap-risk statistic and earnings date, outside ST-14's scope lock (binding condition 8):
1. `_compute_gap_stats` (`backend/services/gap_risk_service.py`) classifies a gap as a weekend gap only when `(cur_date − prev_date).days > 3`. A Friday-to-Monday gap is exactly 3 days, so ordinary weekends fall into the overnight set and the "weekend" set holds only 4+ day closures, contrary to the function's docstring.
2. `get_gap_risk` chooses the weekend statistic with `today.weekday() >= 4`. That ignores the NYSE calendar ST-14 introduced: for example, a Thursday view before Good Friday shows the overnight statistic.
3. `earnings_service.py` converts `earningsTimestamp` with `datetime.utcfromtimestamp(...).date()`, so a release after about 20:00 ET (19:00 EST) rolls to the next date.

**Scope**
- Classify a gap as multi-day when it spans one or more non-session days, using the ST-14 calendar
- Select the statistic by whether the next session follows a non-session day
- Convert the earnings timestamp to the America/New_York date
- Re-confirm Binding Condition 4 (retrospective statistic only) in the §13 record's next addendum, if the statistic's definition changes

**Acceptance Criteria**
- A Friday-to-Monday gap is counted in the weekend set (unit test)
- A Thursday view before Good Friday uses the weekend statistic (unit test)
- An `earningsTimestamp` of 21:00 ET maps to that ET date (unit test)

---

### BLG-BE-175 — Exiting a US position with a NULL fill_price fails in the P&L arithmetic
**Priority:** P3 (Low)
**Type:** Backend / Robustness
**Owner:** Head of Engineering
**Source:** ST-12 (EPIC-02, cycle `2026-10-12__release-v9.12`) — found while fixing BLG-BE-145's recompute paths — 2026-10-13
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
`exit_position()` (`backend/services/position_service.py`) reads the native entry as `position.get('fill_price', position['entry_price'])` for US positions. When the key exists but is NULL this returns None, and the realised P&L arithmetic raises. Falling back to `entry_price` would also be wrong, because `positions.entry_price` is GBP for every market (`data_model_positions_dictionary.md` v0.4). ST-12 fixed the same pattern on the on-load, nightly and `GET /positions` paths with `native_entry_price()`, which uses `fill_price`, else `entry_price × fx_rate`. The exit path was left alone because it writes a closed trade's realised P&L, which is outside ST-12's scope.

**Scope**
- Use `native_entry_price(position, <stored fx_rate, else the exit fx_rate>)` in `exit_position()`
- Add a unit test for a US exit with a NULL `fill_price`

**Acceptance Criteria**
- A US position with a NULL `fill_price` exits without error, and its realised P&L uses `entry_price × fx_rate` as the native entry (unit test)

---

### BLG-BE-176 — Lifecycle badge and Risk page disagree for a US row with no fill_price and no fx_rate
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Head of Engineering
**Source:** EPIC-02 PR review (agent-mediated Director of Quality, user-directed), cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
`classify_position()` (`backend/services/position_lifecycle_service.py`) returns UNKNOWN for a US row whose `fill_price` and `fx_rate` are both NULL (ST-13, v9.12), while `native_entry_price()` (`position_service.py`) and `portfolio_service.get_portfolio_summary()` fall back to the live FX rate, so `display_status` still shows PROFITABLE/LOSING for the same row. ST-13's goal was that the two agree.

**Scope**
- Use one fallback on all paths (either all UNKNOWN, or all live-rate), decided against `position_endpoints.md`'s `position_state` field note
- Add a unit test for this row

**Acceptance Criteria**
- For a US row with NULL `fill_price` and NULL `fx_rate`, `display_status` and `position_state` agree (unit test)

---

### BLG-BE-177 — Frozen-stop marker is not written when the on-load recompute has no live price
**Priority:** P3 (Low)
**Type:** Backend Engineering / Improvement
**Owner:** Head of Engineering
**Source:** EPIC-02 PR review (agent-mediated Director of Quality, user-directed), cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
On the on-load path, `stop_frozen_reason` (ST-15, DS-32) is written only inside `if live_price:` (`analyze_positions`, `backend/services/position_service.py`). A post-grace position with no live price and no ATR keeps its stop but is never marked frozen until the nightly job runs.

**Scope**
- Write the marker when the stop is kept for lack of ATR even without a live price, or document the exclusion in `position_endpoints.md`

**Acceptance Criteria**
- Unit test: no live price and no ATR, post-grace → `stop_frozen_reason = 'atr_unavailable'` (or the contract states the exclusion)

---

### BLG-BE-178 — Batch signal sizing can allocate more than available cash once fees are added
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Head of Engineering; Financial Reporting & Records Owner
**Source:** EPIC-02 PR review (agent-mediated Product Owner, user-directed), cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`size_batch_inv_vol()` floors shares from each signal's allocation of `available_cash` and then adds entry fees to `total_cost` (BLG-BE-158, v9.12). The weights sum to 1.0, so the sum of `total_cost` across a batch can exceed `available_cash` by up to the fees.

**Scope**
- Size against cash net of estimated fees (or reduce shares until fees fit), per signal or per batch
- Unit tests for UK, US and mixed batches

**Acceptance Criteria**
- For UK, US and mixed batches, the sum of `total_cost` is ≤ `available_cash` (unit test)

---

### BLG-BE-179 — Tag lifecycle transitions caused by the v9.12 badge currency correction
**Priority:** P3 (Low)
**Type:** Backend Engineering / Data Quality
**Owner:** Head of Engineering; Metrics Definitions & Analytics Owner
**Source:** EPIC-02 PR review (agent-mediated Product Owner, user-directed), cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
ST-13 (v9.12) corrected `classify_position()` to compare native with native for US positions. On first load after deploy, affected US positions change state (e.g. PROFITABLE→LOSING, or in/out of EXIT ZONE) with no market move. Each change writes a `state_history` / `position_state_history` entry and resets `days_in_state`, which later lifecycle analytics will read as real transitions.

**Scope**
- Mark transitions on the first post-deploy recompute with a reason such as `basis_correction`, or exclude them from days-in-state and lifecycle analytics
- Document the convention in `data_model.md`

**Acceptance Criteria**
- Correction transitions are identifiable or excluded (unit test)

---

### BLG-SPEC-193 — Trade plan contract still lists 3 plan statuses after openapi.yaml moved to 7
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** ST-31 (BLG-SPEC-177), EPIC-05, cycle `2026-10-08__release-v9.11` — PR #1973 agent-mediated review — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-31 corrected every TradePlan `status` enum in `openapi.yaml` to DS-21's 7 values (`draft`, `research_pending`, `research_complete`, `entry_conditions_set`, `active`, `closed`, `abandoned`). The canonical contract `docs/specs/api_contracts/trade_plan_endpoints.md` still documents `draft | active | closed` for the `POST /trade-plans` body field (line 72) and the `GET /trade-plans` `status` filter (line 123). `docs/specs/security/trade_plan_data_sensitivity.md` (line 29) lists 4 values. A reader of the contract would reject 4 statuses the API accepts and the frontend uses.

**Scope**
- Correct both `trade_plan_endpoints.md` rows to the 7 DS-21 values (or cite DS-21) and add a changelog row
- Correct the `status` row in `trade_plan_data_sensitivity.md`
- Optionally extend `tests/test_trade_plan_status_enum_parity.py` to cover the contract table

**Acceptance Criteria**
- `trade_plan_endpoints.md` and `trade_plan_data_sensitivity.md` list the same 7 statuses as `openapi.yaml` and `data_model.md` DS-21
- `grep` finds no current-state spec listing the 3- or 4-value set (historical migration notes excepted)

---

### BLG-SPEC-194 — Clear the 8 pre-existing success-example drifts so check_contract_example_freshness.py exits 0
**Priority:** P4 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** ST-31 / ST-32, EPIC-05, cycle `2026-10-08__release-v9.11` — PR #1973 agent-mediated review — 2026-10-12
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`scripts/check_contract_example_freshness.py` exits 1 on `main` and on the EPIC-05 branch alike. Error-envelope violations are now 0 (ST-32), but 8 contract success examples carry keys the resolved `openapi.yaml` schema does not have: `health_endpoints.md` POST /test/endpoints; `position_endpoints.md` GET /positions/analyze; `reports_endpoints.md` GET /reports/tax-year; `saved_filters_endpoints.md` GET /saved-filters; `settings_endpoints.md` POST /settings and PATCH /settings/{settings_id}; `signal_endpoints.md` POST /signals/generate; `strategy_benchmark_endpoints.md` GET /strategy/backtest-rule-change/runs. The script is not a CI gate, so an AC such as ST-31's "both still pass" can only be read as "no new finding", and a real new drift is hard to see among the 8.

**Scope**
- For each of the 8, decide which side is right (contract example or `openapi.yaml` response schema) and correct it
- Once the script exits 0, consider adding it to `quality_gate.yml` as a gate

**Acceptance Criteria**
- `python3 scripts/check_contract_example_freshness.py` exits 0 on `main`
- Each correction is recorded in the changed contract's changelog

---

### BLG-FE-217 — Group /reports endpoints on the System Status page instead of "Other"
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of Engineering
**Source:** Post-ship closure `2026-10-08__release-v9.11`, closure_record.md §6 row 9 (closure Friction Item 2) — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** v9.12

**Problem**
`categorizeEndpoint()` in `src/pages/SystemStatus.js` has no `/reports` case, so every `/reports/*` endpoint registered in `backend/routers/test.py` (6 today, growing — v9.11 added the monthly P&L narrative routes) falls into the "Other" group. Post-ship closure STEP 6 only flags *new* top-level prefixes, so this pre-existing gap is never surfaced.

**Scope**
- Add a `/reports` case to `categorizeEndpoint()`, mapping to the existing "Analytics" group or a new "Reports" group (frontend owner's choice, matching the app's nav taxonomy in `src/Layout.js`).
- Add a Playwright assertion in `tests/e2e/system-status.spec.js` that a `/reports/*` endpoint renders under the chosen group, not "Other".

**Acceptance Criteria**
- On the System Status page, no `/reports/*` endpoint appears under "Other".
- A Playwright test asserting the grouping passes in CI.

---

### BLG-FE-218 — Align the View Trail modal wording with the read-only ruling
**Priority:** P3 (Low)
**Type:** Frontend / UX Copy
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** EPIC-02 PR review (agent-mediated Product Owner, user-directed), cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
ST-10 (v9.12) made the Trail Stop modal read-only and renamed the button "View Trail", but the modal heading still reads "Trail Stop — {TICKER}", the "Raise by" label suggests an action the user cannot take (and shows negative values), and the disabled-button tooltip says "Add a stop to use trail management", although a stop can no longer be added (an entry `stop_price` is rejected with 400).

**Scope**
- Heading "View Trail — {TICKER}"; rename "Raise by" (e.g. "Difference vs current stop"); reword the disabled tooltip
- Update `positions.md` §Trail Stop Action (design pass with the Head of UX & Design)
- Update Playwright SC-TS-* assertions

**Acceptance Criteria**
- The three texts are changed in `positions.md` and `Positions.js`, and Playwright asserts the new heading and label

---

### BLG-FE-219 — Label signal cost as including fees, and make the zero-ATR sizing reason plain English
**Priority:** P3 (Low)
**Type:** Frontend / UX Copy
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Source:** EPIC-02 PR review (agent-mediated Product Owner, user-directed), cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
Since BLG-BE-158 (v9.12) a signal's `total_cost` is GBP including entry fees, but SignalCard still labels it "Allocation Cost" (`src/components/signals/SignalCard.js`). The new zero-ATR `reason` (BLG-BE-157), which sprint planning recorded as API-only, is displayed by SignalCard's existing `reason` line as "⚠ Inv-vol sizing: ATR unavailable for this signal", which is jargon. No Playwright test covers the reason line.

**Scope**
- Label the value "Total cost (incl. fees)"
- Reword the zero-ATR reason in plain English (backend string and `signal_endpoints.md`)
- Playwright test for the reason line

**Acceptance Criteria**
- The label and reason text are changed, and Playwright asserts the reason line for a zero-ATR signal

---

### BLG-AI-14 — AI chat context: label available cash and starting capital separately (as ST-03 did for the briefing)
**Priority:** P4 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Sprint Execution, ST-03 / EPIC-01, cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** XS (<1h plus tests)
**Provisional-Target:** v9.13

**Problem**
ST-03 (`BLG-AI-12`) relabelled the daily-briefing context to "available cash £X; starting capital £Y", omitting starting capital when it is 0, because "cash £X of £{initial_cash}" was read as a target cash level. `ai_chat()` in `backend/services/ai_service.py` still renders "Cash: £X of £{initial_cash} initial capital". On staging, where `initial_cash` is 0, that reads "of £0 initial capital", which carries the same risk of misreading. ST-03's AC covered the briefing only.

**Scope**
- Apply the same labelling to the chat context (reuse `_briefing_cash_line()` or an equivalent helper)
- Bump `CHAT_PROMPT_VERSION` if the golden-fixture procedure requires it, and update `tests/fixtures/ai_prompt_template_golden_fixtures.json`
- Update the context list in `docs/specs/api_contracts/ai_endpoints.md` §POST /ai/chat

**Acceptance Criteria**
- The chat context no longer uses "of £{initial_cash}", and omits starting capital when it is 0
- Golden-fixture and chat tests pass with any recorded prompt-version bump

---

### BLG-SPEC-195 — Journal summary: remove the stale AI_MODEL override line, or cost the model actually used
**Priority:** P4 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner; Backend Engineering Patterns Owner
**Source:** Agent-mediated Director of Quality review (second pass) of EPIC-01, ST-06, cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** XS (<1h)
**Provisional-Target:** v9.13

**Problem**
`ai_endpoints.md` §POST /ai/journal-summary says "Default model: `claude-haiku-4-5-20251001`. Override via `AI_MODEL` env var." No such override exists: `summarise_journal_notes()` uses `MODEL_VERSION = CLAUDE_HAIKU_4_5`, and the router never passes a model. ST-06 (v9.12) added `claude_audit_log` cost logging for the journal summary at Haiku 4.5 rates regardless of the `model` argument. That is correct today, but the costing would be wrong if an override were ever added.

**Scope**
- Remove the `AI_MODEL` override sentence from the contract (or implement the override and cost by model)
- If a non-Haiku model can ever be passed, select the cost rates by model in `_audit_journal_summary_call()`

**Acceptance Criteria**
- The contract describes only model selection that exists in code
- A test pins the cost rates to the model used, or the contract states the endpoint is Haiku-only

---

### BLG-AI-15 — Journal summary: add an output-language scan so summaries cannot suggest trading changes
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Sprint Execution, ST-01 / EPIC-01 staging run (cycle `2026-10-12__release-v9.12`), user-confirmed in-session — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** v9.13

**Problem**
The first working staging journal summary (2026-10-13, after the ST-01 fix) ended with "...limits visibility into whether setups are working, or if stop placements need adjustment". That is borderline advisory wording about the user's stops. `scan_prescriptive` and `scan_prediction` do not flag it. Unlike the post-trade debrief and the monthly P&L narrative, `POST /ai/journal-summary` runs no output-language check at all: the prompt's "Do not make investment recommendations" is its only control. Until v9.12 every request failed with 422, so this went unnoticed.

**Scope**
- Add a post-generation language check to `summarise_journal_notes()`, reusing the debrief / monthly-narrative pattern (prescriptive scan, plus a check for wording that suggests changing stops, sizing or setups)
- Decide the failure action with AI Compliance & Governance Officer sign-off: regenerate once, then use a code-written fallback, or return the text with the result logged. Record the outcome in `claude_audit_log.compliance_check_result` (the journal summary writes a row from v9.12)
- Tighten the prompt if needed, and bump `JOURNAL_SUMMARY_PROMPT_VERSION` if its text changes
- Update `ai_endpoints.md` §POST /ai/journal-summary and add scenarios to `docs/specs/qa/ai_s13_boundary_test_suite.md`

**Acceptance Criteria**
- A fixture summary containing "stop placements need adjustment" (and a plainly prescriptive one) is caught, and the chosen failure action is applied and tested
- A descriptive fixture summary passes unchanged
- Each call's check result is recorded in `claude_audit_log.compliance_check_result`

---

### BLG-AI-16 — Daily briefing: check the summary text for tickers outside the context
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** PR #2022 agent-mediated review (EPIC-01, cycle `2026-10-12__release-v9.12`), Product Owner finding 3 — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** v9.13

**Problem**
ST-02 (`BLG-AI-11`) drops briefing *actions* whose ticker is not an open position or context signal, but the briefing `summary` prose is returned unfiltered. The model can still write about an invented ticker such as `NEW_SIGNAL` in the summary, unlogged and uncounted, so BLG-AI-11's trust problem is only partly solved.

**Scope**
- Scan the briefing `summary` for upper-case ticker-like tokens not in the context's positions or signals
- Decide the action with AI Compliance & Governance Officer sign-off (log and count, or append a code-written caveat, or regenerate)
- Record the result alongside the stop-time result in `claude_audit_log.compliance_check_result`

**Acceptance Criteria**
- A fixture summary naming an unknown ticker is caught and the chosen action is applied and tested
- A summary naming only context tickers passes unchanged

---

### BLG-AI-17 — Briefing ticker filter: treat UK `.L` and bare tickers as the same instrument
**Priority:** P2 (Medium)
**Type:** AI Compliance / Correctness
**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer
**Source:** PR #2022 agent-mediated review (EPIC-01, cycle `2026-10-12__release-v9.12`), Director of Quality finding 1 — 2026-10-13
**Effort:** XS (<1h plus tests)
**Provisional-Target:** v9.13

**Problem**
ST-02's `_filter_actions_to_context()` (`backend/services/ai_service.py`) needs an exact, case-insensitive ticker match. If the model writes `VOD` for a held `VOD.L` (or the reverse), a valid EXIT or MONITOR action for a held UK position is silently dropped and only a server warning is logged. Elsewhere the codebase already treats bare and `.L` UK tickers as the same instrument (`database.py`, trade-plan lookup with `ticker_bare` / `ticker_bare + ".L"`).

**Scope**
- Normalise both sides (upper case, strip a trailing `.L`) before matching in `_filter_actions_to_context()`
- Apply the same normalisation to the stop-time check's ticker attribution

**Acceptance Criteria**
- A fixture action for `VOD` is kept when `VOD.L` is held, and the reverse
- Tests cover the suffixed case

---

### BLG-AI-18 — Stop-time check: attribute chat stop citations to the focused ticker, and case-normalise action tickers
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** PR #2022 agent-mediated review (EPIC-01, cycle `2026-10-12__release-v9.12`), Product Owner finding 4 and Director of Quality finding 6 — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** v9.13

**Problem**
ST-04's stop-time check (`_append_missing_stop_times`) gets no `own_ticker` from `ai_chat()`, even when `context_opts.ticker` focuses the chat on one position. The commonest chat case, "Your stop is at £450" asked from a position, is therefore only counted as `unattributed` and gets no recalculation time. `own_ticker` matching is also case-sensitive, so an action with ticker `aapl` (kept by the case-insensitive ST-02 filter) gets no note either. The note is appended after the whole field, apart from the sentence it qualifies, and not visibly marked as system-added.

**Scope**
- Pass `context_opts.ticker` as `own_ticker` for chat, extending the `ESC-EXEC-20261013-01` ruling with AI Compliance & Governance Officer sign-off
- Case-normalise `own_ticker` against the position tickers
- Ask the Head of UX & Design whether the appended note needs visible "system-added" styling, using the `[STOP-TIME-MISSING]` rate as input

**Acceptance Criteria**
- A ticker-focused chat reply citing a stop without the ticker gets the note
- An action with a lower-case held ticker gets the note
- Tests cover both

---

### BLG-AI-19 — Monthly P&L narrative: stop the directive scan flagging retrospective and discourse wording
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** PR #2022 agent-mediated review (EPIC-01, cycle `2026-10-12__release-v9.12`), Director of Quality finding 2 and Product Owner finding 5 — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** v9.13

**Problem**
ST-05 widened `_INSTRUMENT_DIRECTIVE_RE` (`backend/services/monthly_pnl_narrative_service.py`) to inflected forms. It now also flags descriptive prose that matched nothing before v9.12: "Selling the position early cost you £40.", "You were adding to the position in week 2.", "You were selling the position into strength." and "Adding to that, your win rate rose to 60%.". ("...fell short this month" was already a false positive.) A match forces regenerate-then-fallback, so users get the generic text and pay for a second call on legitimate narratives. BLG-AI-13's scope asked for no false positives on past-tense reporting, but ST-05's restated AC tested only the simple past. Meanwhile "exit/close/trim the position" still pass the scan.

**Scope**
- Exclude gerund-subject and past-progressive forms (sentence-initial "Selling...", "were/was adding|selling|buying") and discourse phrases ("Adding to that", "fell short")
- Consider adding exit/close/trim + holding noun as directives
- Add the examples above as B-MPN-04 negative cases and update `ai_s13_boundary_test_suite.md`

**Acceptance Criteria**
- The listed retrospective and discourse sentences are not reported
- All ST-05 positive cases are still reported
- The representative output and the fallback still scan clean

---

### BLG-AI-20 — Journal summary: catch advisory phrasings the trading-change check misses
**Priority:** P2 (Medium)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** PR #2074 agent-mediated review (EPIC-03, cycle `2026-10-16__release-v9.13`), Director of Quality finding 1 — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
ST-18 (BLG-AI-15) fails a journal summary on `scan_prescriptive` or `_TRADING_CHANGE_RE` (subject, then a present-tense or modal word, then a change verb, per ruling `ESC-EXEC-20261027-03` (A)). Its ACs are met. But common advisory phrasings still pass both scans, so they would be shown to the user unchanged: "Consider tightening stops on volatile names.", "It may be worth revisiting position sizing.", "Stops could be tightened.", "Tighter stops could help.", "Reducing position size after losses would be prudent.", "A review of setups is warranted." and "Stop placement is something to revisit." (all checked against `journal_summary_language_failures()` at `c8fd54e7`; each returns `[]`). These are the §13 risk the check exists for.

**Scope**
- Ask the AI Compliance & Governance Officer to extend the ruling's pattern: imperative "consider/try" + change verb + subject; verb-first and passive forms ("tightening stops", "could be tightened"); "worth" / "would be prudent / wise / better" / "is warranted" / "something to revisit"
- Implement in `_TRADING_CHANGE_RE` or a sibling pattern; keep the past-tense exclusions
- Add the sentences above as positive cases and ST-18's descriptive cases as negatives; update `ai_s13_boundary_test_suite.md` (B-JS)

**Acceptance Criteria**
- Each sentence listed in Problem is reported as `trading_change` (or `prescriptive`)
- All ST-18 positive and descriptive test cases keep their current results
- The ruling extension is recorded before the code change

---

### BLG-AI-21 — Daily briefing: stop the ticker caveat firing on indicator and macro acronyms
**Priority:** P2 (Medium)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** PR #2074 agent-mediated review (EPIC-03, cycle `2026-10-16__release-v9.13`), Director of Quality finding 2 and Product Owner finding 1 — 2026-10-27
**Effort:** XS (<1h plus tests)
**Provisional-Target:** v9.14

**Problem**
ST-17 (BLG-AI-16) appends "(Note: <TOKEN> is not one of your open positions or today's top signals.)" for any upper-case token not held, not a signal, not in the context and not in `_NON_TICKER_WORDS`. That list has 23 words and lacks common market vocabulary, so ordinary summaries get a wrong, confusing caveat: "RSI is overbought on NVDA." → caveat for RSI; "MACD crossed; EPS beat." → MACD, EPS; "GDP and CPI data due." → GDP, CPI; "NB: no exits." → NB (checked against `_summary_ticker_caveat()` at `b0254cf3`). Each hit is also counted as `ticker_outside_context_appended`, which inflates the measure the ruling uses to judge the check. The ruling (`ESC-EXEC-20261027-02` (B), condition 2) names a minimum list ("at least"), so adding words stays within it.

**Scope**
- Add indicator, earnings and macro acronyms (e.g. RSI, MACD, EMA, SMA, VWAP, EPS, PE, IPO, CEO, CFO, GDP, CPI, PPI, PMI, FOMC, FED, ECB, BOE, NB, NYSE, LSE, NASDAQ) to `_NON_TICKER_WORDS`
- Once a few weeks of briefings have run, review the logged `ticker check: ... action=caveat_appended` tokens and add any further non-tickers found (needs the user's permission for a live log/DB query)

**Acceptance Criteria**
- The four example summaries above get no caveat
- `NEW_SIGNAL` and `TSLA` (ST-17 fixtures) are still caught
- `test_non_ticker_words_ignored` covers every added word

---

### BLG-AI-22 — Chat stop-time note: do not attribute a sentence naming another ticker to the focus ticker
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** PR #2074 agent-mediated review (EPIC-03, cycle `2026-10-16__release-v9.13`), Director of Quality finding 3 — 2026-10-27
**Effort:** XS (<1h plus tests)
**Provisional-Target:** v9.14

**Problem**
ST-16 (BLG-AI-18) attributes a chat sentence that cites a stop to the focused, held ticker when the sentence "names no held ticker" (ruling `ESC-EXEC-20261027-01` (B), condition 3). A sentence that names a ticker the user does not hold therefore still gets the focus ticker's note: with focus `MU`, "TSLA's stop was hit last week." becomes "TSLA's stop was hit last week. (MU stop last recalculated 2026-10-20 21:05 UTC)" (checked against `_append_missing_stop_times()` at `d1a71c13`). The note reads as if it were about TSLA, which is the misattribution the ruling's grounds (charter §7, explainability) set out to avoid.

**Scope**
- Ask the AI Compliance & Governance Officer to amend condition 3: attribute to the focus ticker only when the sentence names no ticker-like token other than the focus ticker (reuse ST-17's `_TICKER_TOKEN_RE` and `_NON_TICKER_WORDS`)
- Such a sentence is left unattributed (`[STOP-TIME-MISSING]` path), as before ST-16
- Add the example above as a test

**Acceptance Criteria**
- With focus `MU`, "TSLA's stop was hit last week." gets no MU note
- All ST-16 tests (`tests/test_ai_stop_time_focus_attribution.py`) still pass
- The ruling amendment is recorded before the code change

---

### BLG-OPS-186 — Daily AI cost check: close the last-hours-of-day blind spot
**Priority:** P3 (Low)
**Type:** Operations / Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** PR #2022 agent-mediated review (EPIC-01, cycle `2026-10-12__release-v9.12`), Director of Quality finding 3 — 2026-10-13
**Effort:** XS (<1h plus tests)
**Provisional-Target:** v9.13

**Problem**
`ai-daily-cost-check.yml` (ST-06) runs at 00:15, 06:15, 12:15 and 18:15 UTC, and `get_daily_ai_cost()` sums today's spend only (`generated_at >= CURRENT_DATE`). Spend after the last run of the day (later still if GitHub delays it) is never compared against that day's total, because the 00:15 run starts a new day, which leaves a blind spot of about 6 hours every day.

**Scope**
- Either have the first run of each day also check the previous UTC day, or alert on a rolling 24-hour window (keeping the per-day de-duplication)
- Update `ai_endpoints.md` §POST /ai/check-daily-cost

**Acceptance Criteria**
- Spend between the last run and midnight is checked against its own day's threshold
- A test covers the day-boundary case

---

### BLG-OPS-187 — Daily AI cost alert: stop reporting $0 on query failure, and alert when the scheduler fails
**Priority:** P2 (Medium)
**Type:** Operations / Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** PR #2022 agent-mediated review (EPIC-01, cycle `2026-10-12__release-v9.12`), Director of Quality finding 4 and Product Owner finding 8 — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** v9.13

**Problem**
`get_daily_ai_cost()` catches every exception and returns `{"total_cost_usd": 0.0, "request_count": 0}` with no log line. Since ST-06 it is the alert's only cost source, so a failed query (missing column, connection error) reports $0, the alert never fires, and `ai-daily-cost-check.yml` still passes because the endpoint returns HTTP 200. A failed workflow run (bad secret, API down) only produces GitHub's default email. Either way the alert can go silent again, which is the failure BLG-OPS-183 set out to fix.

**Scope**
- Log the exception and return an explicit error status (or non-200) from `POST /ai/check-daily-cost` when the cost query fails
- Make the workflow fail on an error status, and send a Telegram message when the workflow itself fails (the same could apply to `ai-endpoint-anomaly-check.yml`)

**Acceptance Criteria**
- A simulated query failure is logged, reported as an error and fails the workflow step
- A failed run sends a notification beyond GitHub's default email

---

### BLG-OPS-188 — Make ci-usage-report.yml's monthly commit succeed (failed on its only scheduled run)
**Priority:** P3 (Low)
**Type:** Operations / FinOps Reporting
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Source:** ST-32/EPIC-04, cycle `2026-10-12__release-v9.12` (scheduled-workflow inventory, `docs/ops/scheduled_workflows_inventory.md`) — 2026-10-15
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
`ci-usage-report.yml` (ST-17, BLG-OPS-165, v9.6) has run once on its schedule, on 2026-10-01 (run 36861580190), and failed: "Generate report" succeeded and "Commit report" failed. `docs/ops/ci_usage_reports/` still holds only `2026-08.md`, which ST-17 committed by hand, so no monthly report has been produced since. The run's logs have expired. A likely cause is `main`'s branch rule "Changes must be made through a pull request", which a `GITHUB_TOKEN` push cannot bypass. This is not confirmed.

**Scope**
- Find the cause (re-run with `workflow_dispatch` and read the "Commit report" log)
- Fix it, for example by opening a PR with the report or by uploading it as an artifact, and produce the missing 2026-09 report

**Acceptance Criteria**
- A `ci-usage-report.yml` run succeeds and its report reaches `docs/ops/ci_usage_reports/` (or the agreed destination)
- `docs/ops/ci_usage_reports/2026-09.md` exists

---

### BLG-OPS-189 — Point staging-deploy.yml at both staging services' deploy hooks and wait on the one it deployed
**Priority:** P2 (Medium)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** ST-29/EPIC-04, cycle `2026-10-12__release-v9.12` (BLG-OPS-181 cause, DEL-20261015-02) — 2026-10-15
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`staging-deploy.yml` calls one deploy hook, `RENDER_STAGING_DEPLOY_HOOK`, and that secret holds the staging **frontend's** hook. `wait_for_staging_deploy_live.py` then waits for the staging **backend** (`srv-d6rtdg94tr6s73ce2j6g`) to go live on the pushed commit. The backend is never hook-deployed, so every run has failed since 2026-09-03, and with Render auto-deploy off the staging backend changes only by manual deploy. Staging has two services, and one hook can deploy only one of them.

**Scope**
- Two secrets, `RENDER_STAGING_BACKEND_DEPLOY_HOOK` and `RENDER_STAGING_FRONTEND_DEPLOY_HOOK`, each copied from that service's Settings → Deploy Hook; retire `RENDER_STAGING_DEPLOY_HOOK`
- `staging-deploy.yml` calls both; the wait step checks both services (or each hook's returned deploy ID) reach the pushed commit
- Check the hook response's deploy ID belongs to the expected service (Render API `GET /v1/services/{id}/deploys`), so a mis-pasted hook fails loudly
- Make the smoke test confirm the host behind `STAGING_API_URL` is `srv-d6rtdg94tr6s73ce2j6g` (e.g. compare its `deployed_commit_sha` with the Render API's live deploy for that service), so a stale URL fails loudly. Until 2026-10-15 the secret pointed at an unidentified host on `90099bec` (BLG-OPS-181 Notes)
- Update `docs/ops/staging_deploy_notes.md` §4 and `docs/ops/github_actions_secrets_ownership_map.md`

**Acceptance Criteria**
- A `staging-deploy.yml` run on `main` succeeds, with both staging services live on the run's commit
- A test fails if the workflow calls only one hook or waits on a service it did not deploy

---

### BLG-QA-221 — Real-Postgres tests for the ai_audit_log UUID[] path and the claude_audit_log daily cost sum
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner; Backend Engineering Patterns Owner
**Source:** PR #2022 agent-mediated review (EPIC-01, cycle `2026-10-12__release-v9.12`), Director of Quality finding 5 — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** v9.13

**Problem**
All the new SQL in EPIC-01 is verified only through mocks or a hand-written fake: the `ANY(%s::uuid[])` notes query, the `%s::uuid[]` audit insert, the history filter's `%s::uuid = ANY(trade_ids)`, the DS-31 `ALTER ... TYPE UUID[] USING NULL`, and `SUM(cost_usd) FROM claude_audit_log`. The ST-01 staging run exercised the notes query and the insert. The history filter's UUID path and the cost sum have no real-database evidence.

**Scope**
- Add Pytest Phase B (real Postgres) tests: DS-31 conversion from an INTEGER[] table, an insert and history filter with UUIDs, and a daily cost sum over claude_audit_log rows across a day boundary

**Acceptance Criteria**
- The Phase B tests pass in CI and fail if the casts or the table name are wrong

---

### BLG-SPEC-196 — Re-apply NOT NULL on positions.portfolio_id and positions.total_cost
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-34/EPIC-05, cycle `2026-10-12__release-v9.12` (drift-detector triage of BLG-SPEC-178, read-only staging reads authorised by the user) — 2026-10-13
**Effort:** S (~0.5d; pre-check, migration and live confirmation in two environments)
**Provisional-Target:** TBD

**Problem**
`data_model.md`'s `CREATE TABLE positions` declares `portfolio_id UUID NOT NULL` and `total_cost DECIMAL(12, 2) NOT NULL`, and its Fields table says both are not nullable. On live staging (2026-10-13), both columns are nullable, so a row without a portfolio or a cost basis can be written. Production has not been checked. The other 6 positions nullable mismatches from BLG-SPEC-178 finding 3 were documentation errors and were fixed in `data_model.md` v2.60; these 2 are genuine enforcement gaps.

**Scope**
- Read-only pre-check on staging and production: count rows where `portfolio_id IS NULL` or `total_cost IS NULL`
- If both counts are 0, add a DS-xx migration (`ALTER TABLE positions ALTER COLUMN ... SET NOT NULL`, reversible) and apply it to staging, then production, per the DS-23 pattern
- If any row is NULL, record the rows' origin and a backfill decision before migrating
- Remove the "nullable on live staging" notes on both Fields rows once applied

**Acceptance Criteria**
- `information_schema.columns` reports `is_nullable = NO` for both columns in staging and production, with the output recorded in the DS-xx Live Confirmation
- `scripts/check_data_model_drift.py` no longer reports either column as a nullable mismatch

---

### BLG-SPEC-197 — Apply DS-17's open-position unique index to staging
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-34/EPIC-05, cycle `2026-10-12__release-v9.12` (drift-detector triage of BLG-SPEC-178, read-only staging reads authorised by the user); BLG-SPEC-178 finding 1 — 2026-10-13
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
DS-17's `idx_positions_open_ticker_entry_date_unique` was confirmed live in production on 2026-09-23, but it does not exist on staging (`pg_indexes`, 2026-10-13). The staging reset workflow (`reset-and-seed-staging.yml`) clears data but never applies DS-17, so staging has not had the index since it was introduced. Staging therefore accepts duplicate open positions that production rejects, and staging tests cannot catch a regression in the duplicate guard.

**Scope**
- Run DS-17's duplicate pre-check on staging, then its Up Migration
- Record the staging Live Confirmation in DS-17
- Decide whether `reset-and-seed-staging.yml`'s migrate step should also apply DS-17 (`CREATE UNIQUE INDEX IF NOT EXISTS`) so a future staging rebuild keeps it

**Acceptance Criteria**
- `pg_indexes` on staging lists `idx_positions_open_ticker_entry_date_unique` with DS-17's definition
- DS-17 records the staging confirmation alongside the production one

---

### BLG-QA-223 — Stop check_data_model_drift.py reading index names from rollback blocks
**Priority:** P4 (Trivial)
**Type:** QA / Test Tooling
**Owner:** QA & Testing Owner; Data Model & Domain Schema Owner
**Source:** ST-34/EPIC-05, cycle `2026-10-12__release-v9.12` (drift-detector triage of BLG-SPEC-178, read-only staging reads authorised by the user); BLG-SPEC-178 finding 5 — 2026-10-13
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`scripts/check_data_model_drift.py` collects every `CREATE INDEX` name in `data_model.md`, including those inside "Reversible:" and Down Migration blocks. A rollback that recreates a superseded index is then reported as a missing live index. `idx_trade_plans_ticker` (replaced by `idx_trade_plans_ticker_upper` in v2.22) is reported on every run for this reason. Each run therefore needs the same false positive to be ruled out by hand.

**Scope**
- Exclude SQL inside blocks introduced by `Reversible:` or under a `Down Migration` heading from index and CHECK-constraint name parsing
- Add a unit test with a fixture containing a rollback-only index name
- Keep each run's `--json` output (for example, a dated file under `docs/ops/` committed with the triage that uses it), so later triage can name every finding. The v9.9 run kept no output, which left 3 of finding 5's 11 names unidentifiable at ST-34 (v9.12; agent-mediated Director of Quality review, condition C1)

**Acceptance Criteria**
- Running the detector against `data_model.md` no longer reports `idx_trade_plans_ticker`
- A unit test fails if a rollback-only index name is reported again
- The detector's documented usage, or the triage procedure, says where a run's `--json` output is kept, and the next triage cites it

**Notes:** Priority confirmed P4 (2026-10-15, owner decision on user direction, closing post-ship closure `2026-10-12__release-v9.12` §6 row 6). `sprint_close.md`'s P3 is the ST-34 `Pass_with_deviation` default severity, a separate figure (`execution_prompt.md` v3.87 §5.3 now shows both). The 3 unnamed finding-5 names cannot be recovered, so this item's value is preventing a recurrence, which is tooling hygiene.

---

### BLG-QA-224 — Make SC-TS-* Playwright scenario IDs unique across tests/e2e
**Priority:** P3 (Low)
**Type:** QA / Test Traceability
**Owner:** QA & Testing Owner
**Source:** EPIC-02 PR review (agent-mediated Product Owner, user-directed), cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
`tests/e2e/epic01-v34-lifecycle.spec.js` (Trail Stop modal, SC-TS-01..07) and `tests/e2e/epic01-v62-stops-alerts.spec.js` (trailing-stop column, SC-TS-01..06) use the same IDs for different scenarios. ST-10 (v9.12) added SC-TS-04..07 to the first file, widening the overlap. Evidence citing an SC-TS ID is ambiguous. `docs/System_status_report.md` and `docs/specs/Specs_Index.md` cite SC-TS-01..03 for the v3.4 file.

**Scope**
- Give one file a distinct prefix and update every citation in `docs/` and `claude/cycles/` that refers to the renamed IDs

**Acceptance Criteria**
- No scenario ID is used in more than one file under `tests/e2e` (a script or test checks this)

---

### BLG-QA-225 — Keep a bare `pytest` from the repo root out of backend/mutmut_pilot_tests
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner
**Source:** ST-31/EPIC-04, cycle `2026-10-12__release-v9.12` (AC 1 fresh-clone verification) — 2026-10-15
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
With no path argument, `backend/.venv/bin/python3 -m pytest --collect-only -q` from the repo root collects `backend/mutmut_pilot_tests/test_pilot.py` (the ST-15/v9.8 mutation-testing pilot, meant to run only from `backend/` via `mutmut run`) before `tests/`. Its standalone conftest and module-level `import database` leave `sys.modules["database"]` as something other than `tests/conftest.py`'s stub, so the BLG-QA-190 leak guard fails collection of the first `tests/` file (`tests/test_add_position_stop_handling.py`) with "replaced sys.modules['database'] ... without restoring it". Result: 2690 collected, 1 error. `pytest tests/` collects cleanly (2674), and CI always passes `tests/`, so CI is unaffected, but CLAUDE.md §9 and `README.md` both show the bare form.

**Scope**
- Make a bare root `pytest` collect only `tests/` (for example a root pytest config with `testpaths = tests`), confirming that `cd backend && python3 -m mutmut run` still selects `mutmut_pilot_tests/test_pilot.py` with the same rootdir and node IDs
- Or make the pilot's conftest restore `sys.modules["database"]`, if the config route breaks mutmut

**Acceptance Criteria**
- `backend/.venv/bin/python3 -m pytest --collect-only -q` from the repo root exits 0
- The mutmut pilot's pytest selection still collects its tests from `backend/`

---

### BLG-SPEC-198 — Open-position pnl: code uses the live FX rate and does not deduct fees; the dictionary says entry-time FX, fees deducted
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner; Metrics Definitions & Analytics Owner
**Source:** ST-38/EPIC-05, cycle `2026-10-12__release-v9.12` — Data Model & Domain Schema Owner ruling on `ESC-EXEC-20261013-05`, condition C2 (agent-mediated, §5.3) — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`data_model_positions_dictionary.md` §5.2 (v0.4) defines open-position `pnl` for US positions as `(current_price − fill_price) × shares / fx_rate − fees_paid`, using the **entry-time** `fx_rate`. The live computation in `backend/services/portfolio_service.py` (around lines 141–146) divides native P&L by `live_fx_rate` and does not subtract `fees_paid`, and `utils/calculations.py`'s `calculate_position_pnl()` takes a `live_fx_rate` too. Spec and code therefore disagree on both the FX rate and the fee deduction, so a reader of the dictionary cannot reproduce the displayed unrealised P&L. ST-38 corrected only the entry-price currency in these formulas.

**Scope**
- Decide which is canonical, including whether currency movement since entry belongs in unrealised P&L. Check `metrics_definitions.md` and the Positions/Portfolio frontend specs for the displayed definition
- Align the losing side. A code change that alters displayed P&L needs a design pass
- Also correct `metrics_definitions.md` Position Risk's data sources. They still label `positions.entry_price` "native currency", which contradicts the GBP ruling (ST-38, v9.12). For US positions the native entry is `fill_price`; the formula `(entry − stop)` must not mix GBP `entry_price` with the native `initial_stop` (agent-mediated Director of Quality review of EPIC-05, condition C2)

**Acceptance Criteria**
- `metrics_definitions.md` Position Risk names `fill_price` (US) or `entry_price` (UK) as the native entry, with a version bump
- The dictionary's §5.2 and the `pnl` row state the same FX basis and fee treatment as the code that produces the displayed figure, or a code change brings the code to the spec with Data Model & Domain Schema Owner sign-off
- The decision is recorded with its rationale

---

### BLG-SPEC-199 — Align the positions data dictionary's nullability with data_model.md v2.60
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** PR #2024 agent-mediated Director of Quality review (EPIC-05, cycle `2026-10-12__release-v9.12`) — 2026-10-13
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Resolved (2026-10-13, PR #2024, before merge):** fixed on the EPIC-05 branch at the user's request. The dictionary is now v0.5: the six Nullable values match `data_model.md` v2.60 and there is a `risk_off_exit` row. `si02_gap_analysis.md` is now v1.1, with the US risk derivation using `fill_price`. Not fixed here: `metrics_definitions.md` Position Risk (BLG-SPEC-198), and 11 newer columns still missing from the dictionary (listed in its v0.5 coverage note).

**Problem**
ST-34 (v9.12) corrected `data_model.md` §2's Fields table to say `holding_days`, `pnl`, `pnl_pct`, `status`, `created_at` and `updated_at` are nullable (each has a `DEFAULT` but no `NOT NULL`, in the documented `CREATE TABLE` and live). It also corrected `risk_off_exit` to `NOT NULL DEFAULT FALSE`. `data_model_positions_dictionary.md` (v0.4) still marks all six as `NO` (rows at lines ~79–111) and has no `risk_off_exit` row. The two canonical documents now disagree on these columns. Separately, `docs/specs/si02_gap_analysis.md:108` still derives risk as `(entry_price − initial_stop) × shares` "in native currency", but `positions.entry_price` is GBP (ST-38); for US positions the native entry is `fill_price`.

**Scope**
- Set the six dictionary rows' Nullable to `YES`, with the same "DEFAULT but no NOT NULL" note `data_model.md` v2.60 uses, and add a `risk_off_exit` row (`NOT NULL DEFAULT FALSE`). Dictionary version bump.
- Correct `si02_gap_analysis.md`'s risk derivation to use `fill_price` for US positions (or add a dated correction note, if that document is treated as historical)

**Acceptance Criteria**
- For every positions column, the dictionary's Nullable value equals `data_model.md` §2's
- No spec describes `positions.entry_price` as native currency for US positions (`metrics_definitions.md` Position Risk is handled under BLG-SPEC-198)

---

### BLG-SPEC-200 — Add the 11 missing positions columns to the positions data dictionary
**Priority:** P4 (Trivial)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** BLG-SPEC-199 fix on PR #2024 (EPIC-05, cycle `2026-10-12__release-v9.12`), user request — 2026-10-13
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`data_model_positions_dictionary.md` (v0.5) does not describe 11 `positions` columns that `data_model.md` §2 documents: `user_fill_price`, `position_state`, `state_entered_at`, `state_history`, `stop_calculated_at`, `atr_calculated_at`, `active_atr_multiplier`, `atr_source`, `stop_calculation_source`, `strategy_version_at_entry`, `last_reviewed_at`. Its v0.5 coverage note sends readers to `data_model.md` for them. The dictionary is meant to be the canonical per-field reference, so readers have to consult two documents. It also still carries an `exit_note` row for a column that does not exist live, kept only for traceability.

**Scope**
- Add a dictionary row for each of the 11 columns (SQL type, Nullable, description), taken from `data_model.md` §2 and its DS-xx migration sections, in the matching §3.x subsection
- Decide whether to remove the `exit_note` row or keep it as a marked historical row
- Remove the v0.5 coverage note once every column is listed; version bump

**Acceptance Criteria**
- Every column in `data_model.md` §2's Fields table has a dictionary row, with the same type and Nullable value
- The dictionary lists no column that `data_model.md` §2 does not, other than an explicitly marked historical row

---

### BLG-SPEC-201 — Point settings.md at the moved strategy constants module
**Priority:** P4 (Trivial)
**Type:** Spec Debt / Frontend
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-21/EPIC-03, cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-21 moved the frontend display mirror of the `strategy_rules.md` §11 parameters from `src/lib/strategyParameters.js` to `src/constants/strategy.js` (Head of Specs Team interpretation, 2026-10-13), leaving one module. `docs/specs/frontend/pages/settings.md` §Strategy Parameter Presentation (line ~121) still says the displayed values come from `src/lib/strategyParameters.js`, which no longer exists. Sprint Execution may not edit a canonical spec beyond deviation documentation, so the path was not changed in ST-21's commit.

**Scope**
- Replace the path in `settings.md` with `src/constants/strategy.js`; version bump and changelog row

**Acceptance Criteria**
- `settings.md` names `src/constants/strategy.js`, and no canonical spec under `docs/specs/` names `src/lib/strategyParameters.js`

---

### BLG-FE-220 — Fix the Strategy Benchmark Rebalance badge's contrast and settle tinted vs filled exit-reason badges
**Priority:** P3 (Low)
**Type:** Frontend / Accessibility
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-24/EPIC-03, cycle `2026-10-12__release-v9.12` (v9.12 design gate observation, `design_gate.md` line ~142, filed at execution per `sprint_backlog.md` Outstanding Actions) — 2026-10-13
**Effort:** XS (<1h plus test updates)
**Provisional-Target:** TBD

**Problem**
On the Strategy Benchmark Trade Log, the Rebalance exit badge is `bg-teal-600 text-white`, about 3.7:1, below WCAG AA for its small text. ST-24 moved the Risk-Off badge on the same table to `bg-amber-700` (5.02:1) but did not touch teal, which is outside its amber scope. `strategy_benchmark.md` §7 also describes tinted exit-reason badges, while the shipped table uses filled ones.

**Scope**
- Decide tinted vs filled badges with the Head of UX & Design, and align `strategy_benchmark.md` §7 and `src/pages/StrategyBenchmark.js`
- Move Rebalance to a passing token (e.g. `bg-teal-700`, measured first)
- Update `tests/e2e/strategy-benchmark.spec.js` SC-SB-04a's `bg-teal-600` assertion and add a scoped axe color-contrast check

**Acceptance Criteria**
- Every exit-reason badge on the Trade Log passes a scoped axe color-contrast scan in both themes
- `strategy_benchmark.md` §7 matches the shipped badge style

---

### BLG-FE-221 — A coloured className on `<Button>` never renders: Button's default bg-primary wins
**Priority:** P2 (Medium)
**Type:** Frontend / Accessibility
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Source:** ST-24/EPIC-03, cycle `2026-10-12__release-v9.12` — 2026-10-13 (found by ST-24's scoped axe scan of the Trade Plan "Abandon Plan" button)
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`src/lib/utils.js` `cn()` is plain `clsx`, with no `tailwind-merge`, so a `<Button className="bg-emerald-600 …">` keeps the default variant's `bg-primary` as well. In the built CSS `.bg-primary` comes after every colour `bg-*` utility (e.g. `.bg-amber-700` at offset ~26.7k, `.bg-emerald-600` ~29.1k, `.bg-primary` ~30.4k), and the same holds for `hover:bg-primary/90`, so the custom colour never shows. The Trade Plan "Abandon Plan" button rendered `#fafafa` behind white text in dark mode (contrast 1.04:1). ST-24 fixed that one button with `!bg-amber-700 hover:!bg-amber-800`. Other `<Button>`s with a colour fill and no `variant` override are affected the same way, for example `src/pages/Screener.js` (lines ~333 and ~1065, `bg-emerald-600`) and `src/pages/TradePlans.js` (~385, `bg-rose-600`).

**Scope**
- Fix at the root: add `tailwind-merge` to `cn()` (the shadcn default), or give coloured buttons a variant with no background; then remove ST-24's `!` workaround
- Audit every `<Button>` with a colour `bg-*` className and confirm each renders its intended fill
- Add a Playwright `toHaveCSS('background-color', …)` or scoped axe check for at least the affected buttons

**Acceptance Criteria**
- Every `<Button>` with a colour `bg-*` className renders that colour (asserted for the listed sites)
- No `!bg-` workaround remains for this cause

---

### BLG-FE-222 — Normalise the Trade Entry ticker the same way for the ATR preview and for save
**Priority:** P3 (Low)
**Type:** Frontend / Backend Correctness
**Owner:** Head of Engineering
**Source:** ST-17/EPIC-03, cycle `2026-10-12__release-v9.12`, agent-mediated Director of Quality review (follow-up 1) — 2026-10-13
**Effort:** XS (<1h plus tests)
**Provisional-Target:** TBD

**Problem**
`GET /market/atr/{ticker}` trims and upper-cases the ticker; `POST /portfolio/position` does neither (`AddPositionRequest.ticker` has no validator), and Trade Entry upper-cases on change but does not trim, nor upper-case a prefilled ticker. With `"AAPL "`, the preview fetches the ATR for `AAPL` while save calls `calculate_atr("AAPL ")`, so the shown stop can differ from the stored one. ST-17's AC 2 test covers only already-normalised input. Related minor inconsistency: the `?position=` deep link requires `status === "open"` while `?exit=` uses `!== "closed"` (follow-up 6).

**Scope**
- Normalise (trim, upper-case) the ticker once, server-side in `AddPositionRequest`/`add_position()`, and in Trade Entry before both the preview and the submit
- Extend `tests/test_market_atr_preview_endpoint.py` AC 2 cases with untrimmed and lower-case input
- Align the two Positions deep links' status test

**Acceptance Criteria**
- For an untrimmed or lower-case ticker, the preview stop equals the saved `initial_stop` (backend test)
- `?position=` and `?exit=` use the same open-position test

---

### BLG-GOV-389 — Decide whether the strategy-copy lint should fail CI, and whether the 200-day MA belongs in the constants module
**Priority:** P3 (Low)
**Type:** Governance Process / Strategy Conformance
**Owner:** Head of Specs Team; Frontend Specifications & UX Documentation Owner
**Source:** ST-21/EPIC-03, cycle `2026-10-12__release-v9.12`, agent-mediated Director of Quality review (follow-ups 2 and 3) — 2026-10-13
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`scripts/check_strategy_copy.py` runs in CI job `strategy-copy` without `--strict`, so a future contradiction is only a warning (BLG-GOV-369's scope asked for a CI warning; `tests/test_check_strategy_copy.py` does pin the current clean tree). The lint also deliberately skips the 200-day MA (`strategy_rules.md` §8.2), which is inside ST-21's §5–§11 title scope but not a §11 parameter; `SignalContextPanel.js` still writes "200-day MA" as a literal.

**Scope**
- Head of Specs Team rules: (a) warning only, or `--strict` in CI; (b) whether the regime MA length joins `src/constants/strategy.js` and the lint
- Apply the ruling to the workflow, the lint and the constants module

**Acceptance Criteria**
- A dated ruling on (a) and (b), applied

---

### BLG-FE-223 — Inputs apply dark:text-slate-400 to typed text instead of the placeholder
**Priority:** P3 (Low)
**Type:** Frontend / Accessibility
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** EPIC-03, cycle `2026-10-12__release-v9.12`, agent-mediated Director of Quality review (follow-up 4) — 2026-10-13
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
Several inputs use `placeholder:text-slate-600 dark:text-slate-400`. The `dark:` variant applies to the typed text, not the placeholder (`dark:placeholder:` was intended), so typed values render slate-400 in dark mode and placeholder colour is unpaired. Seen on the Trade Entry inputs and the Notifications inputs.

**Scope**
- Replace with `placeholder:text-slate-600 dark:placeholder:text-slate-400` and an explicit typed-text pair (`text-slate-900 dark:text-white`) across `src/`

**Acceptance Criteria**
- No input class string uses a bare `dark:text-*` intended for its placeholder (grep check); typed text passes contrast in both themes

---

### BLG-FE-224 — Move amber-600 text on light surfaces to amber-700
**Priority:** P3 (Low)
**Type:** Frontend / Accessibility
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-24/EPIC-03, cycle `2026-10-12__release-v9.12`, agent-mediated Director of Quality review (follow-up 5) — 2026-10-13
**Effort:** S (~0.5 day plus test updates)
**Provisional-Target:** TBD

**Problem**
ST-24 fixed white text on amber-600 fills. `text-amber-600` used as text on light surfaces remains (about 3.2:1 on white, below AA; `design_system.md` §Light-Theme Colour Tokens rule 3): WatchlistRow, PositionSizingWidget, WhatIfSizingPreview, TradePlans (~285, stale marker), Positions/PositionCard. Some tests assert the class (e.g. `trade-plan-stale-marker.spec.js` SC-TPS-05, `position-sizing-concentration.spec.js` V-SIZE-01, `position-review-cadence-nudge.spec.js`).

**Scope**
- Move each to `text-amber-700 dark:text-amber-400` and update the asserting tests in the same commit

**Acceptance Criteria**
- No `text-amber-600` remains in `src/` outside Replay; scoped axe color-contrast scans of the changed elements pass in the light theme

---

### BLG-BE-180 — Reject a fetched ATR that puts the initial stop at or below zero
**Priority:** P2 (Medium)
**Type:** Backend / Strategy correctness
**Owner:** Backend & Data Owner
**Source:** PR #2026 (EPIC-03, cycle `2026-10-12__release-v9.12`), agent-mediated Director of Quality review — 2026-10-15
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
ST-18 added a guard in `add_position()` (`backend/services/position_service.py` ~907) that rejects a *typed* ATR when 5 × ATR ≥ entry. A *fetched* ATR (field left blank) has no such check: on a low-priced, volatile ticker where 5 × the 14-day ATR meets or exceeds the entry price, `calculate_initial_stop()` returns a stop at or below zero and save stores it silently. Trade Entry's ST-17 preview shows the same value (`TradeEntry.js` ~288, `systemStop = price - atr * 5`, no lower bound), so the user sees a negative "Initial Stop (set by system)" with no explanation.

**Scope**
- Decide the rule with the strategy owner (reject with 400, or apply a floor), recorded in `strategy_rules.md` §5 if it changes stop behaviour
- Apply it in `add_position()` for fetched and fallback ATRs, and show a matching inline message on Trade Entry when the previewed stop is ≤ 0

**Acceptance Criteria**
- A backend test with a mocked fetched ATR where 5 × ATR ≥ entry does not store a stop ≤ 0
- Playwright: with a mocked preview ATR where 5 × ATR ≥ entry, Trade Entry shows no negative stop and explains why

---

### BLG-FE-225 — Cache the Trade Entry ATR preview per ticker and market
**Priority:** P3 (Low)
**Type:** Frontend / Performance
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** PR #2026 (EPIC-03, cycle `2026-10-12__release-v9.12`), agent-mediated Director of Quality review — 2026-10-15
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
ST-17's preview (`src/pages/TradeEntry.js` ~90–112) calls `GET /market/atr/{ticker}` from a bare `useEffect` after each 300 ms pause in typing. Nothing is cached, so editing the ticker and changing it back, toggling market, or clearing and re-entering the ATR field refetches, and each fetch is an uncached Alpaca/Yahoo call on the backend. The rest of the page uses react-query.

**Scope**
- Move the preview to `useQuery` keyed on `["market-atr", normalisedTicker, market]` with a staleTime (e.g. 5 minutes), keeping the debounce and the idle/loading/ready/none states

**Acceptance Criteria**
- Playwright: entering the same ticker twice within the staleTime issues one `GET /market/atr` request; SC-TAP-01..05 still pass

---

### BLG-SPEC-202 — Define or remove the 2R Exit Zone threshold the Positions page states
**Priority:** P3 (Low)
**Type:** Specification / Strategy copy
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** PR #2026 (EPIC-03, cycle `2026-10-12__release-v9.12`), agent-mediated Director of Quality review — 2026-10-15
**Effort:** XS (~0.25 day)
**Provisional-Target:** TBD

**Problem**
The PROFITABLE lifecycle tooltip in `src/pages/Positions.js` (~69) says "Advances to Exit Zone when P&L reaches 2R target". `strategy_rules.md` has no 2R or R-multiple rule, so the ST-21 strategy-copy lint cannot check it and the constants module has no value for it. Either the UI restates a rule the strategy does not define, or the rule exists only in code.

**Scope**
- Find where the Exit Zone threshold is computed; with the strategy owner, either add it to `strategy_rules.md` §11 (then to `src/constants/strategy.js` and the lint) or reword the tooltip to describe the shipped behaviour without a rule number

**Acceptance Criteria**
- The tooltip's threshold is either defined in `strategy_rules.md` and imported from `src/constants/strategy.js`, or no longer stated as a number; `scripts/check_strategy_copy.py` passes

---

### BLG-BE-181 — Keep GET /settings working when the settings change-log read fails
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Engineering
**Source:** PR #2027 review (Director of Quality, agent-mediated), ST-26/EPIC-04, cycle `2026-10-12__release-v9.12` — 2026-10-15
**Effort:** XS (<1h)
**Provisional-Target:** v9.13

**Problem**
Since ST-26, `GET /settings` (`backend/main.py` `get_settings_endpoint`) calls `get_last_settings_change()` inside the endpoint's single `try`. Any failure of that read becomes a 500 for the whole settings read: the `settings_change_log` table missing in an environment, a permission error, or a bad row. Every page that loads settings then fails, not just the last-change line. The migration is applied on staging and production, so this is latent. It bites on any new or rebuilt environment, and on any future change to the table.

**Scope**
- Wrap the `get_last_settings_change()` call so a failure logs a warning and returns `last_change: null`; the rest of the settings payload is unaffected
- Add a test: when `get_last_settings_change` raises, `GET /settings` returns 200 with the settings row and `last_change` null

**Acceptance Criteria**
- With the change-log read raising, `GET /settings` returns 200 and the settings data, with `last_change: null` (test)
- The failure is logged at warning level or above

---

### BLG-QA-226 — Run the settings change-log SQL against a real Postgres in CI
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality; Head of Engineering
**Source:** PR #2027 review (Director of Quality, agent-mediated), ST-26/EPIC-04, cycle `2026-10-12__release-v9.12` — 2026-10-15
**Effort:** S (~0.5d)
**Provisional-Target:** v9.13

**Problem**
`tests/test_settings_change_log.py` mocks the cursor. The SQL that ST-26 added in `backend/database.py` is never executed in CI: the `SELECT ... FOR UPDATE`, the `INSERT INTO settings_change_log`, and the `batch_id` subquery in `get_last_settings_change()`. `ci-tests.yml` Pytest Phase B starts a real `postgres:15` service, but no test creates the DS-33 schema in it. A typo or type mismatch in that SQL would first show up on staging or production as a failed settings save, because the log insert shares the save's transaction.

**Scope**
- In Phase B, create `settings` and the DS-33 `settings_change_log` table (from `data_model.md` DS-33) and run `create_settings` / `update_settings` / `get_last_settings_change` against it
- Skip cleanly when no real `DATABASE_URL` is available, as the existing Phase A/B split expects

**Acceptance Criteria**
- A Phase B test saves settings twice against real Postgres and asserts the log rows (field, old, new, source, shared `batch_id`) and the `last_change` payload
- A deliberately broken column name in the insert makes that test fail in CI

---

### BLG-GOV-390 — Treat `Gate criteria: None`/`N/A` as ungated in scan_backlog_gate_conditions.py
**Priority:** P2 (Medium)
**Type:** Governance Tooling
**Owner:** Head of Engineering; Head of Specs Team
**Source:** `ESC-CLOSE-20261015-01` Head of Specs Team ruling, option (a), post-ship closure `2026-10-12__release-v9.12`; originally v9.10 Release Planning Friction Item 1, carried 3 cycles under `BLG-GOV-373`, which does not cover it — 2026-10-15
**Effort:** XS (<1h, ~0.25d)
**Provisional-Target:** v9.13

**Problem**
`GATE_CRITERIA_RE` in `scripts/scan_backlog_gate_conditions.py` captures any non-empty value, so a literal `**Gate criteria:** None` is reported as a gate condition. On 2026-10-15 this counted 17 active items as gated (`BLG-GOV-178`, `184`, `185`, `186`, `189`, `191`–`196`, `198`, `200`, `201`, `BLG-SPEC-77`, `BLG-OPS-105`, `BLG-QA-93`) and inflated the gated count to 124. Release Planning §1.3a uses this list to fix the ready pool, so these items are silently left out of every release.

**Scope**
- In `classify_item()`, treat a `Gate criteria` value of `None`, `N/A` or `-`/`—` (case-insensitive, trimmed, optional trailing period) as ungated
- Report those items in a separate informational "explicitly ungated" count, so the change is visible in the scan output
- Add tests covering `None`, `N/A` and a real gate
- Confirm each of the 17 newly ungated items still deserves a ready-pool slot, and record the result in the PR (no item edits required)

**Acceptance Criteria**
- The 17 items above no longer appear in the gated list, and the gated count drops by 17
- A real gate (for example `BLG-GOV-382`, 2027-01-03) is still reported as gated
- New tests pass under `backend/.venv/bin/python3 -m pytest`

**Notes:** `BLG-GOV-373` (known-false-positive allow-list for date-lapse matches) is a separate problem and keeps its own scope.

---

### BLG-SPEC-203 — Reports unrealised P&L is a nightly snapshot while the Positions page is live (re-files archived BLG-SPEC-87)
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Integrity
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Re-file of `BLG-SPEC-87` (archived at `2026-08-03__release-v8.1` without shipping) for open deviation `DEV-REPORTS-ST06-01`; deviation consolidation review 2026-10-07 Finding 1; post-ship closure `2026-10-12__release-v9.12` §6 row 3 — 2026-10-15
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`get_estimated_unrealised_pnl()` (`backend/services/reports_service.py`) still sums the `positions.pnl` column, which is written once per night by `run_nightly_trailing_stop_update()`. The Positions page computes `pnl` against the live price on every request. So `GET /reports/monthly-pnl` and `GET /reports/tax-year` can show a different unrealised P&L from the Positions page for the same position at the same moment, with no in-app sign that one is a snapshot (−£126.25 vs −£115.06 in production, 2026-07-14). Confirmed still present in code on 2026-10-15. The deviation has had no active tracking item since `BLG-SPEC-87` was archived.

**Scope**
- Decide one direction: (a) compute the figure live via `get_positions_with_prices()`, or (b) keep the snapshot and add an explicit "as of last nightly update" caveat to `unrealised_note`
- Implement it, and update `reports.md` §Unrealised P&L Card
- Mark `DEV-REPORTS-ST06-01` resolved in `reports.md` Known Deviations

**Acceptance Criteria**
- If (a): the Reports and Positions unrealised figures match at the same moment (verified on staging)
- If (b): the `unrealised_note` text states the snapshot time basis and is reviewed by the Head of UX & Design
- `DEV-REPORTS-ST06-01` is marked resolved, citing this item

---

### BLG-FE-226 — Make the Daily Position Monitor's "confirm exits" open the real exit flow (it calls a route that does not exist)
**Priority:** P1 (High)
**Type:** Frontend / Correctness
**Owner:** Head of Engineering; Product Owner
**Source:** `IDEA-head-of-engineering-20261016-01`, `IDEA-product-owner-20261016-01`, `IDEA-qa-lead-20261016-01`, `IDEA-financial-reporting-20261016-01` (consolidated), roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~1-1.5 days)
**Provisional-Target:** v9.13

**Problem**
Dashboard → Quick Actions → Run Monitor (`MonitorModal.js`) suggests exits for positions with a stop hit or a risk-off market. Its confirm calls `Dashboard.js::handleExitPositions`, which calls `base44.entities.Position.update` → `PATCH /positions/{id}` (`base44Client.js:223`). No such route exists; only `GET /positions/{position_id}` and three `PATCH` sub-routes do, so FastAPI returns 405. The handler has no try/catch: the first failure is an unhandled rejection, the modal stays open with the selection cleared, and no position closes and no error shows. The payload also computes `pnl = (current_price − entry_price) × shares` itself, with no fees, broker fill or exit FX, and writes no `trade_history` row, unlike `POST /positions/{id}/exit` (`ExitPositionRequest`). The defect dates from commit `997ed1b2` (2026-01-24).

**Scope**
- Replace the bulk `Position.update` loop with a queue that opens the existing ExitModal for each selected position, pre-selecting the exit reason ("Stop Loss Hit" for a stop suggestion, "Risk-Off Signal" for a regime suggestion)
- Show a visible error and keep the queue state if any exit fails
- Delete `Position.update` from `base44Client.js`
- Playwright: select a suggested exit, confirm, complete the exit flow and assert the position leaves the open list (staging seed); a failed request shows an error

**Acceptance Criteria**
- [ ] No code path calls `PATCH /positions/{id}`
- [ ] Confirming a Monitor exit records the exit through `POST /positions/{id}/exit`, with fees, fill price and FX captured as in every other exit
- [ ] A failed exit shows an error message; the modal does not silently clear
- [ ] Both Playwright tests pass in CI

---

### BLG-FE-227 — One shared exit-reason module: Trade Reflections badges and labels never match stored values
**Priority:** P2 (Medium)
**Type:** Frontend / UX Correctness
**Owner:** Head of UX & Design; Head of Engineering
**Source:** `IDEA-head-of-ux-20261016-01`, `IDEA-head-of-engineering-20261016-02` (consolidated), roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~0.5-1 day)
**Provisional-Target:** v9.13

**Problem**
`TradeReflection.js:12-22`, `TradeReflectionModal.js:23-26` and `PerformanceAnalytics.js:443-448` map legacy keys (`stop_hit`, `manual`, `target`, `market_regime`) that `ExitModal.js` never writes. Stored values are "Manual Exit", "Stop Loss Hit", "Trailing Stop", "Risk-Off Signal", "Target Reached" and "Partial Profit Taking". Every Trade Reflections card therefore shows a grey badge with raw uppercase text, and the colour coding that separates stop exits from discretionary exits never renders.

**Scope**
- `src/constants/exitReasons.js`: the 6 stored values with label, colour and §8 category; legacy keys kept as aliases
- Import it in ExitModal, TradeReflection, TradeReflectionModal, PerformanceAnalytics and TradeHistoryTable
- Playwright coverage of each badge colour on Trade Reflections

**Acceptance Criteria**
- [ ] Each of the 6 stored values renders its own label and colour on Trade Reflections cards and in the modal
- [ ] No frontend file keeps its own exit-reason map
- [ ] Playwright colour tests pass

**Notes:** Refines `BLG-SPEC-186` (allowed values and §8 mapping in the specs and a DB constraint) with the frontend consumers it does not touch. If `BLG-SPEC-186` lands first, take the §8 category from it.

---

### BLG-BE-182 — Record `checklist_skipped` events and stop offering Red Flag Journal filters that can never match
**Priority:** P2 (Medium)
**Type:** Backend + Frontend / Strategy Discipline
**Owner:** Strategy Rules & System Intent Owner; Head of UX & Design; QA & Testing Owner
**Source:** `IDEA-strategy-owner-20261016-02`, `IDEA-head-of-ux-20261016-02`, `IDEA-qa-testing-20261016-01` (consolidated), roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~1-1.5 days)
**Provisional-Target:** v9.13

**Problem**
`database.py::_VALID_EVENT_TYPES` and the Red Flag Journal contract (`red_flag_journal.md:39-40, 68`) define 4 event types, but only `pre_entry_override` is ever written (`trade_plans.py:174-185`). TradePlan saves plans with `checklist_completed: false` (`TradePlan.js:442, 674`), the case `checklist_skipped` exists for, but nothing records it. The journal's filter (`RedFlagJournal.js:43-49`) still offers Checklist Skipped, Stop Prompt Dismissed and Drawdown Prompt Dismissed, which always return an empty list. A user filtering for skipped checklists concludes they never skipped one.

**Scope**
- On plan create or update where a non-empty checklist is saved incomplete, write a non-blocking `checklist_skipped` event (ticker, plan id, unchecked item count)
- In the journal filter, mark types with no writer as "not yet recorded" (or hide them), and say in the empty state which types are recorded
- Pytest: each declared event type has a writer, or a dated allow-list entry for the two prompt types

**Acceptance Criteria**
- [ ] Saving a plan with an incomplete checklist produces one `checklist_skipped` row, visible in the journal (Playwright)
- [ ] Filter options for types with no writer are labelled as such
- [ ] The writer-coverage test passes and fails if a declared type loses its writer

---

### BLG-BE-183 — Grace-period warning numbers days differently from the Positions page
**Priority:** P3 (Low)
**Type:** Backend + Frontend / Copy Correctness
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** `IDEA-frontend-specs-20261016-01`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** XS (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`alerts_service.py:697-713` writes "(day 8 of 10)" from 0-based `holding_days`. Positions numbers the entry day as Day 1 (`Positions.js:146-148`), so the same position on the same day is Day 9 there. `NotificationPreferences.js:20` says "Notify on days 8–9 of the grace period", also 0-based.

**Scope**
- Use entry-day-is-Day-1 numbering in the alert message and context
- Preference copy: "Notify on the last 2 days of the grace period", built from `GRACE_PERIOD_DAYS`

**Acceptance Criteria**
- [ ] For a position on its last grace day, feed/email and Positions show the same day number
- [ ] Preference copy contains no hard-coded day numbers

---

### BLG-FE-228 — Alert History compact values look for keys the backend never writes
**Priority:** P3 (Low)
**Type:** Frontend / Display Correctness
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** `IDEA-frontend-specs-20261016-02`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** XS (~0.25 day)
**Provisional-Target:** TBD

**Problem**
`NotificationsHistory.js` expects `grace_period_days` and `positions_count`/`total_pnl`. The backend writes `min_hold_days` (`alerts_service.py:697-701`) and `open_positions` (line 763), so the Grace Period value never appears and summary rows fall back to raw keys.

**Scope**
- Align UI keys and labels with the backend (or rename backend keys) and record the mapping in the Alert History page spec

**Acceptance Criteria**
- [ ] All 4 alert types show their intended compact fields (unit or Playwright test)

---

### BLG-FE-229 — Trade Reflections says "No closed trades yet" when a ticker search has no match
**Priority:** P3 (Low)
**Type:** Frontend / UX Copy
**Owner:** Base44 Frontend Prompt Owner
**Source:** `IDEA-base44-frontend-20261016-01`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** XS (~0.25 day)
**Provisional-Target:** TBD

**Problem**
`TradeReflection.js:61-66` shows "No closed trades yet — close a trade to write your first reflection" both for an empty list and for a search with no match.

**Scope**
- Separate no-match empty state with a clear-search action

**Acceptance Criteria**
- [ ] With ≥1 closed trade and a non-matching search, the page shows a no-match message (Playwright)

---

### BLG-FE-230 — Remove dead Base44 client methods and the unused bearer-token path
**Priority:** P3 (Low)
**Type:** Frontend / Security Hygiene
**Owner:** Base44 Frontend Prompt Owner; Cybersecurity & Trust Lead
**Source:** `IDEA-base44-frontend-20261016-02`, `IDEA-cybersecurity-20261016-01` (consolidated), roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`base44Client.js` keeps `Signal.create` (`POST /signals`, no route), `getPublicSettingsById` and `exchangeCodeForToken` (`POST /auth/callback`, no route), none with a caller. `getToken` reads a `localStorage` token and `doFetch` sends it as `Authorization: Bearer` on every request, but no backend code reads `Authorization`.

**Scope**
- Delete the uncalled methods, `getToken`/`setToken` and the `Authorization` header
- Note in `credential_policy.md` that the frontend sends only `X-API-Key`

**Acceptance Criteria**
- [ ] No client method targets a route missing from `openapi.yaml`
- [ ] No request carries an `Authorization` header
- [ ] Full frontend and e2e suites pass

---

### BLG-SEC-43 — Per-environment CORS allow-list (production accepts localhost:3000)
**Priority:** P3 (Low)
**Type:** Security / Configuration
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** `IDEA-cybersecurity-20261016-02`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`backend/config.py:12-17` uses one `ALLOWED_ORIGINS` list for every environment, so production accepts credentialed cross-origin requests from `http://localhost:3000`, the staging frontend and its own origin (`allow_credentials=True`, `allow_methods=['*']`).

**Scope**
- Build the list from an environment variable per deployment, with documented defaults

**Acceptance Criteria**
- [ ] Production preflight from `http://localhost:3000` is rejected; the Pages origin is accepted (staging/production check recorded)

---

### BLG-BE-184 — Daily Portfolio Summary notification carries only an open-position count
**Priority:** P3 (Low)
**Type:** Backend / Notification Content
**Owner:** Product Owner; Backend Engineering Patterns Owner
**Source:** `IDEA-product-owner-20261016-02`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
Notification Preferences promises "a daily digest of portfolio status" (`NotificationPreferences.js:31-45`), but the message is "Daily summary: N open position(s) as of today." (`alerts_service.py:763-766`).

**Scope**
- Add total unrealised P&L (GBP), the day's change, positions within the stop-approach threshold and grace periods ending in ≤2 days, from existing computations; numeric only

**Acceptance Criteria**
- [ ] The daily summary row and email contain the 5 fields (unit test)
- [ ] No narrative text is generated

---

### BLG-QA-227 — Fail Playwright on any 404/405 from the app's API and sweep state-changing primary actions
**Priority:** P2 (Medium)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality; QA Lead
**Source:** `IDEA-director-of-quality-20261016-01`, `IDEA-challenger-20261016-01` (consolidated), roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** M (~2-3 days)
**Provisional-Target:** TBD

**Problem**
The Daily Position Monitor's confirm has returned 405 since January (`BLG-FE-226`) while every gate passed. SC-DCO-03 opens the Monitor but checks only layout, and no e2e test asserts that a state-changing button's request succeeds.

**Scope**
- Shared Playwright fixture that fails a test on any 404/405 from the app's own API origin (with an allow-list for intentional probes)
- List every state-changing primary action in `src/` and add a test for each not already exercised

**Acceptance Criteria**
- [ ] The fixture is applied suite-wide and fails on a deliberate 405
- [ ] The action list is recorded in `docs/testing/` with its coverage status, and every listed action is covered or has a dated backlog item

---

### BLG-QA-228 — CI check that every frontend API call exists in openapi.yaml
**Priority:** P2 (Medium)
**Type:** QA / Contract Tooling
**Owner:** API Contracts & Documentation Owner
**Source:** `IDEA-api-contracts-20261016-01`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
`check_openapi_drift.py` compares routers, contracts and `openapi.yaml`; `check_consumer_contract_drift.js` covers only the `api` object's response fields. Neither checks that the frontend's method and path exist, so `PATCH /positions/{id}` and `POST /signals` went unnoticed.

**Scope**
- Script extracting every `doFetch`/`apiFetch` method and path in `src/` and comparing it with `docs/reference/openapi.yaml` (allow-list for external calls), run in the quality gate

**Acceptance Criteria**
- [ ] The check fails on a call to a non-existent route and passes on `main` once `BLG-FE-226` and `BLG-FE-230` land

---

### BLG-SPEC-204 — Weekly Digest calls journal completion rate "Compliance Score"
**Priority:** P3 (Low)
**Type:** Spec Debt / Metric Naming
**Owner:** Metrics Definitions & Analytics Owner; API Contracts & Documentation Owner
**Source:** `IDEA-metrics-20261016-01`, `IDEA-api-contracts-20261016-02` (consolidated), roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`GET /digest/weekly` returns `compliance_score_current`/`_7d_ago`, computed as journal completion rate (`database.py:5255`), and the Weekly Digest labels them "Compliance Score". `metrics_definitions.md` defines compliance as the Arc 5 composite, and the v7.7 Strategy Owner decision says one field must mean one thing.

**Scope**
- Relabel the rows "Journal Completion Rate" (or source them from the composite)
- Add `journal_completion_rate_*` fields with the old names as deprecated aliases; update contract and `openapi.yaml`

**Acceptance Criteria**
- [ ] No UI label or API field named "compliance" carries the journal completion rate
- [ ] Contract, `openapi.yaml` and `metrics_definitions.md` agree

---

### BLG-SPEC-205 — "Alerts Dismissed (7d)" computation differs from its definition
**Priority:** P3 (Low)
**Type:** Spec Debt / Metric Definition
**Owner:** Metrics Definitions & Analytics Owner
**Source:** `IDEA-metrics-20261016-02`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** XS (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`routers/digest.py:59` defines `alerts_dismissed_7d` as notifications marked read in the last 7 days. The SQL counts notifications created in the last 7 days that are now read.

**Scope**
- Either add `read_at` and count by it, or change the definition and label; record the choice in `metrics_definitions.md`

**Acceptance Criteria**
- [ ] Definition and computation match (unit test with an old alert read inside the window)

---

### BLG-BE-185 — Log and count failed red-flag override writes instead of discarding them
**Priority:** P3 (Low)
**Type:** Backend / Observability
**Owner:** Backend Engineering Patterns Owner
**Source:** `IDEA-backend-engineering-20261016-01`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** XS (~0.25 day)
**Provisional-Target:** TBD

**Problem**
`trade_plans.py::_maybe_write_override_event` (lines 174-185) wraps the write in `except Exception: pass`, so a failed override insert is lost without a trace.

**Scope**
- Keep it non-blocking; log at WARNING with ticker and event type; expose a failure count on `GET /health`

**Acceptance Criteria**
- [ ] A forced insert failure produces a log line and increments the count (unit test)

---

### BLG-BE-186 — Link override events to their position, and bound the AI debrief's flags to the trade's window
**Priority:** P3 (Low)
**Type:** Backend / Data Model / AI Advisory
**Owner:** Data Model & Domain Schema Owner; AI Compliance & Governance Officer
**Source:** `IDEA-data-model-20261016-01`, `IDEA-ai-compliance-20261016-01` (consolidated), roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
Pre-entry override events are written at plan creation with a null `position_id` (`trade_plans.py:260`) and never back-filled. The AI Post-Trade Debrief then fetches the 5 most recent flags for the ticker with no date bound (`debrief_service.py:413-421`), so a debrief can cite overrides from later plans in the same ticker.

**Scope**
- Set `position_id` on a plan's override events when the plan is linked to a position; back-fill existing linked rows; document the column lifecycle in `data_model.md`
- Debrief: filter flags by `position_id`, or by the trade's own date window

**Acceptance Criteria**
- [ ] Override events for plan-linked trades carry `position_id`
- [ ] The debrief cites no flag dated outside the trade's window (unit test)

---

### BLG-GOV-391 — Strategy determination: month-end rebalance exits are live but not in strategy_rules.md
**Priority:** P2 (Medium)
**Type:** Strategy Conformance
**Owner:** Strategy Rules & System Intent Owner
**Source:** `IDEA-strategy-owner-20261016-01`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~0.5-1 day, determination)
**Provisional-Target:** TBD

**Problem**
Since v6.2 (`BLG-FEAT-47`), `generate_rebalance_exit_signals` (`signal_service.py:411`) recommends exiting every open position outside the current top-5 momentum ranking on the last trading day of each month; `rebalance-exit.yml` runs it nightly. `strategy_rules.md` never mentions rebalancing, §8 allows "exactly three" exit conditions, and §1 requires any outcome-affecting behaviour to be specified there.

**Scope**
- Strategy Rules & System Intent Owner determines whether rebalance exit enters §8 through §12.3 change control or is withdrawn; record the decision
- Until decided, label the signal "outside §8 — informational" in the UI

**Acceptance Criteria**
- [ ] A dated determination is recorded and either `strategy_rules.md` §8 is amended under §12.3 or the signal is withdrawn

---

### BLG-OPS-190 — Rebalance-exit generation should check that today's screener run completed
**Priority:** P3 (Low)
**Type:** Operations / Job Dependencies
**Owner:** Infrastructure & Operations Owner
**Source:** `IDEA-infra-ops-20261016-01`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`screener-refresh.yml` (22:00 UTC), `nightly-stop-update.yml` (22:30) and `rebalance-exit.yml` (22:45) rely on start times for ordering. Nothing checks that the screener finished, so a month-end run after a screener failure ranks on stale signals without warning.

**Scope**
- Freshness precondition in the rebalance-exit endpoint or workflow: skip and alert if no screener run completed today

**Acceptance Criteria**
- [ ] With no completed screener run today, rebalance-exit creates no signals and raises an alert (test)

---

### BLG-OPS-191 — Skip the five code-test workflows on governance-only and docs-only pushes
**Priority:** P3 (Low)
**Type:** Operations / CI Efficiency
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** `IDEA-finops-20261016-01`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
878 of 1,034 commits on `main` since 2026-09-15 touch only `claude/` or `docs/`, yet CI Pytest, Critical-Path Smoke, Service Layer Coverage, Golden Output and Portfolio Integration run on every push (~5,500 run-minutes in 2026-08).

**Scope**
- `paths-ignore: ['claude/**', 'docs/**']` with a pass-through job so required checks still report (constraint noted at `backlog_archive.md:2167`)

**Acceptance Criteria**
- [ ] A governance-only PR completes with all required checks reported, without running the five suites
- [ ] A code PR still runs them

---

### BLG-GOV-392 — Reconcile shared_standards §2's "write Blocked before halting" with engines that may not write status
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** `IDEA-head-of-specs-20261016-01`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** XS (~0.25 day)
**Provisional-Target:** TBD

**Problem**
`shared_standards.md` §2 step 3 requires setting state to `Blocked` before any hard-gate halt. `roadmap_prompt.md` §4/STEP 12.1 forbid the rebalance engine to write `status`. At `2026-10-16__scheduled` STEP -1.5 the two could not both be followed.

**Scope**
- State in §2 how non-cycle engines record a halt (own artefact or a `last_halt` key), with the §6 checklist

**Acceptance Criteria**
- [ ] §2 and each engine's state-write rule agree

---

### BLG-GOV-393 — File a backlog item for every deferred roadmap prompt patch so a sprint can seat it
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead; Head of Specs Team
**Source:** `IDEA-pmo-lead-20261016-01`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** XS (~0.5 day)
**Provisional-Target:** TBD

**Problem**
Three patches deferred on 2026-10-06 (target 2026-10-20) went OVERDUE by carry count at `2026-10-16__scheduled` and halted STEP -1.5. Two sprints ran in between, but no step turned the deferred patches into backlog work.

**Scope**
- `roadmap_prompt.md` STEP 11.2: a deferred patch also files a backlog item; STEP -1.5: a patch whose item is seated in the current release counts as carried

**Acceptance Criteria**
- [ ] Both prompt changes applied with the §6 checklist

---

### BLG-GOV-394 — Append the role-share history row at post-ship closure
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Director of HR; PMO Lead
**Source:** `IDEA-director-of-hr-20261016-01`, roadmap rebalance `2026-10-16__scheduled` (`IW-20261016-01`) — 2026-10-16
**Effort:** XS (~0.25 day)
**Provisional-Target:** TBD

**Problem**
`role_share_history.md` rows are appended only at rebalances, so it ended at v9.10 while v9.11 and v9.12 had shipped (both appended at `2026-10-16__scheduled`).

**Scope**
- Post-ship closure runs `scripts/compute_role_share_history.py` for the closed cycle and appends the row

**Acceptance Criteria**
- [ ] After the next closure the file includes that cycle's row

---

### BLG-GOV-395 — Make Release Planning's STEP 7 sync write execution_state_path with active_cycle
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Release Planning `2026-10-16__release-v9.13`, PR #2029 CI failure (`test_state_execution_path_consistency.py`, fixed by `9f85acfe`); same failure on PR #1923 at v9.11 (fixed by `15d24fda`) — 2026-10-16
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`.claude_current_state.json`'s `execution_state_path` has no owning engine (`claude/schemas/state_field_owners.json`: "corrected manually at cycle transition"). Release Planning's STEP 7 sync switches `active_cycle` but does not touch the field, so `test_state_execution_path_consistency.py` fails on the release-plan PR. This has happened twice: v9.11 (PR #1923) and v9.13 (PR #2029). Each time a follow-up commit was needed before the PR could merge.

**Scope**
- Add `execution_state_path: claude/cycles/<cycle_id>/execution_state.json` to `release_planning_prompt.md` STEP 7's intermediate-sync YAML block, written atomically with `active_cycle`
- Set the field's owner in `state_field_owners.json` to `release_planning_prompt.md` (Phase 1B, STEP 7), replacing the "none — advisory" entry
- Run the CLAUDE.md §6 governance-file checklist for the prompt bump

**Acceptance Criteria**
- `release_planning_prompt.md` STEP 7 writes `execution_state_path` in the same sync as `active_cycle`
- `state_field_owners.json` names Release Planning as the field's owner
- The next release-plan PR passes `test_state_execution_path_consistency.py` with no follow-up commit

---

### BLG-BE-187 — Detect the live month-end on the exchange calendar, not weekdays only
**Priority:** P3 (Low)
**Type:** Backend / Strategy Conformance
**Owner:** Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner
**Source:** ST-05 / EPIC-01, sprint execution `2026-10-16__release-v9.13` — ruling `ESC-EXEC-20261016-01` binding condition 5 (`strategy_rules.md` v1.17 §8.4 known deviation) — 2026-10-16
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`signal_service.py::_is_last_trading_day_of_month` skips weekends only. The production backtest's month-end dates follow the trading calendar, so when a month's last weekday is an exchange holiday the live §8.4 rebalance signal fires on a non-trading day, or a session early or late against the backtest. `strategy_rules.md` v1.17 §8.4 records this as a known deviation. Separately, `rebalance-exit.yml`'s header comment says `screener-refresh.yml` feeds the top-5 ranking; the ranking comes from `POST /signals/generate` in `daily-snapshot.yml`.

**Scope**
- Detect the last session per market on its exchange calendar (reuse the NYSE observance rules from v9.12 ST-14's gap-risk session calendar; add LSE)
- Correct `rebalance-exit.yml`'s header comment about which job feeds the ranking
- Remove the §8.4 known-deviation line from `strategy_rules.md` (needs its own `strategy_rules.md` write route at the planning that seats this item)

**Acceptance Criteria**
- A month whose last weekday is an exchange holiday is detected on its true last session (pytest)
- The §8.4 known-deviation line is removed

---

### BLG-SPEC-206 — Add a seventh exit_reason, "Rebalance Exit", for §8.4 exits
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner; Metrics Definitions & Analytics Owner
**Source:** ST-05 / EPIC-01, sprint execution `2026-10-16__release-v9.13` — ruling `ESC-EXEC-20261016-01` binding condition 6 (backlog option chosen because DS-34's CHECK constraint awaits live application under `DEL-20261016-01`) — 2026-10-16
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
`strategy_rules.md` v1.17 adds §8.4 Month-end rebalance exit, but the allowed `exit_reason` values (`data_model.md` §3, DS-34) have none for it. A position exited on a rebalance recommendation can only be recorded as Manual Exit (§8.3), so exit analytics by §8 condition cannot separate rebalance exits.

**Scope**
- Add "Rebalance Exit" (category "§8.4 Month-end rebalance exit") to `backend/exit_reasons.py`, `data_model.md` §3 with a DS-xx constraint update, `metrics_definitions.md` §Exit Condition Category and `src/constants/exitReasons.js` (label, short label, badge colour per the exit-reason-badges decision record)
- Offer it in `ExitModal`; pre-select it when exiting from an `exit_rebalance` signal

**Acceptance Criteria**
- `POST /positions/{id}/exit` and the CHECK constraint accept the value
- `tests/test_exit_reason_values.py` and `tests/e2e/exit-reason-badges.spec.js` cover it

---

### BLG-FE-231 — Daily Position Monitor suggests "Stop price hit" during the grace period
**Priority:** P2 (Medium)
**Type:** Frontend / Strategy Conformance
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Source:** ST-01 / EPIC-01, sprint execution `2026-10-16__release-v9.13` — `docs/design/2026-10-16__release-v9.13/monitor-exit-queue/decision_record.md` §7 (recommended for filing; not filed at Sprint Planning) — 2026-10-16
**Effort:** XS (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`MonitorModal.js::getPositionStatus` compares `current_price` with `stop_price` and ignores the grace period. `strategy_rules.md` §8.1 makes the stop-loss trigger active only after grace, and the shared predicate `getExitCondition()` (`src/lib/exitCondition.js`) uses `current_trailing_stop` and `grace_period`. The Monitor can therefore suggest "Stop Loss Hit" for an in-grace position, and since v9.13 that suggestion pre-selects the exit reason.

**Scope**
- Switch the Monitor's suggestions to `getExitCondition()`

**Acceptance Criteria**
- An in-grace breached position is not suggested (Playwright)
- Post-grace breaches and risk-off positions still are

---

### BLG-BE-188 — POST /positions/{id}/exit returns 500 where its contract says 404 or 400
**Priority:** P2 (Medium)
**Type:** Backend / API Contract Conformance
**Owner:** Backend Engineering Patterns Owner; API Contracts & Documentation Owner
**Source:** ST-02 / EPIC-01, sprint execution `2026-10-16__release-v9.13` (found while adding `exit_reason` validation) — 2026-10-16
**Effort:** XS (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`backend/main.py::exit_position_endpoint` calls `services/position_service.py::exit_position` with no error mapping. That function raises `ValueError` for "Position not found", "Position already closed", an invalid price or share count and a missing US FX rate, and the app has no `ValueError` handler, so each becomes a 500. `position_endpoints.md` documents 404 for a missing position and 400 for the others. The v9.13 Monitor exit queue shows the response `detail`, which a 500 does not carry.

**Scope**
- Map each `ValueError` to its documented 404 or 400 with a `detail` string at the endpoint

**Acceptance Criteria**
- One pytest per error case asserts the status and `detail`

---

### BLG-OPS-192 — Tell "no qualifying tickers" apart from "momentum run missing" in the month-end rebalance job
**Priority:** P3 (Low)
**Type:** Operations / Job Dependencies
**Owner:** Infrastructure & Operations Owner; Strategy Rules & System Intent Owner
**Source:** PR #2071 review (ST-05 / EPIC-01), sprint execution `2026-10-16__release-v9.13` — 2026-10-16
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
Since v9.13 (`strategy_rules.md` §8.4), `POST /signals/rebalance-exit` returns 503 and creates nothing when no momentum signal rows are dated today. It cannot tell a missing run from a completed run that found no qualifying tickers, because `generate_momentum_signals` persists no run record. On a month-end where no ticker passes the trend and regime filters, the job raises a false alert and makes no §8.4 recommendations, although every held position is then out of the ranking.

**Scope**
- Persist a completion marker for each momentum signal run (date, tickers ranked, count), or reuse an existing run table
- Rebalance job: no marker today → 503 (unchanged); marker with zero tickers → an empty ranking and the §8.4 recommendations it implies

**Acceptance Criteria**
- pytest: zero-qualifier completed run → signals for non-risk-off, post-§8.1 positions and no 503; missing run → 503 as now

---

### BLG-FE-232 — Positions page exit failures still use a browser alert; adopt ExitModal's inline error
**Priority:** P3 (Low)
**Type:** Frontend / UX Consistency
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Source:** PR #2071 review (ST-01 / EPIC-01), sprint execution `2026-10-16__release-v9.13`; `monitor-exit-queue/decision_record.md` §5 ("The Positions page can adopt the same error state") — 2026-10-16
**Effort:** XS (~0.5 day)
**Provisional-Target:** TBD

**Problem**
v9.13 gave `ExitModal` an inline `exit-error` state that keeps the dialog and its values when an exit fails, but only the Monitor's exit queue uses it. The Positions page's exit mutation still calls `alert()` on failure and the dialog stays open without saying what failed, so the same dialog behaves differently depending on where it was opened.

**Scope**
- Positions page passes an awaitable `onConfirm` so `ExitModal` shows its inline error, "Exiting…" and retry; remove the `alert()`
- Update `positions.md` §Exit Dialog to say the failure state applies everywhere

**Acceptance Criteria**
- A failed Positions-page exit shows `exit-error` with the backend detail and keeps entered values (Playwright)

---

### BLG-BE-189 — Decide whether checklist_skipped should count plans rather than saves
**Priority:** P3 (Low)
**Type:** Backend / Product Decision
**Owner:** Product Owner; Strategy Rules & System Intent Owner
**Source:** PR #2071 review (ST-04 / EPIC-01), sprint execution `2026-10-16__release-v9.13`; DoQ review non-blocking finding 5 — 2026-10-16
**Effort:** XS (~0.5 day)
**Provisional-Target:** TBD

**Problem**
v9.13 writes one `checklist_skipped` event on every create or update of a plan whose checklist is still incomplete (`red_flag_journal.md` contract v1.1.0). Editing a plan's thesis five times before completing the checklist therefore records five deviations. The Red Flag Journal then reads as a count of incomplete saves, which overstates how often the user skipped the checklist.

**Scope**
- Product Owner decides: one event per save (as now), per plan, or only when the unchecked count changes
- If changed: implement in `trade_plans.py::_maybe_write_checklist_skipped_event` and update the contract

**Acceptance Criteria**
- Decision recorded; if changed, pytest covers repeated saves of the same incomplete plan

---

### BLG-SPEC-207 — check_data_model_drift.py: strip SQL comments only outside quotes, and fix two default-normalisation false positives
**Priority:** P4 (Trivial)
**Type:** Spec Debt / Tooling
**Owner:** Data Model & Domain Schema Owner
**Source:** PR #2072 agent-mediated review (Director of Quality role), ST-37 / EPIC-06, sprint execution `2026-10-16__release-v9.13` — 2026-10-17
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`_create_table_columns()` in `scripts/check_data_model_drift.py` (ST-37, BLG-SPEC-184) strips `--` comments from each line before it tracks quotes. A quoted default that contains `--` (for example `DEFAULT '--'`) therefore loses its closing quote, and the rest of the `CREATE TABLE` block is read as one string: later columns go missing and the default comes out as garbage. No current `data_model.md` row triggers this. `normalize_default()` also has two false positives: `'NaN'::numeric` never equals itself, because it becomes a Decimal NaN, and `ARRAY[]::text[]` is reported as different from `'{}'::text[]`.

**Scope**
- Strip `--` comments only outside single-quoted literals
- Compare NaN/Infinity numeric defaults as text, and normalise empty-array forms (`ARRAY[]` and `'{}'`) to one form
- Add tests in `tests/test_check_data_model_drift.py` for each case

**Acceptance Criteria**
- A fixture with `DEFAULT '--'` followed by another column parses both columns correctly
- `'NaN'::numeric` vs `'NaN'::numeric` and `ARRAY[]::text[]` vs `'{}'::text[]` do not report a mismatch
- The existing drift/orphan/dashboard tests still pass

---

### BLG-GOV-396 — Release Planning §1.3a: read the gate scan's "explicitly ungated" and "known non-gate dates" sections
**Priority:** P3 (Low)
**Type:** Governance Process / Tooling Integration
**Owner:** Head of Specs Team; PMO Lead
**Source:** PR #2072 agent-mediated review (Product Owner role), ST-35/ST-36 / EPIC-06, sprint execution `2026-10-16__release-v9.13` — 2026-10-17
**Effort:** XS (~0.25 day)
**Provisional-Target:** TBD (before BLG-OPS-53's allow-list review date, 2026-11-22)

**Problem**
`release_planning_prompt.md` §1.3a tells Release Planning to read the gate scan's "date-lapsed — verify", "gating item shipped — verify" and already-resolved lists. It does not mention the two sections added by ST-35 (BLG-GOV-390, "explicitly ungated") and ST-36 (BLG-GOV-373, "known non-gate dates"). So nothing asks Release Planning to record the explicitly-ungated count next to the gated count in `run_manifest.md`. Nothing asks it to act when an allow-list entry is flagged `REVIEW DUE` or "not in the item's current gate" either. Without that, the review dates in `KNOWN_NON_GATE_DATES` are recorded but nothing enforces them. BLG-OPS-53's entry comes due on 2026-11-22.

**Scope**
- Add both sections to §1.3a's read list: record the explicitly-ungated count in `run_manifest.md`, and review any allow-list entry flagged `REVIEW DUE` or no longer present, keeping it with a new review date or raising its removal
- Apply the CLAUDE.md §6 governance edit checklist (version bump, OPERATIONAL_GUIDE.md §14, `prompt_change_log.md`)

**Acceptance Criteria**
- §1.3a names both sections and the disposition for each
- The next Release Planning run's `run_manifest.md` records the explicitly-ungated count and any allow-list review outcome

---

### BLG-SPEC-208 — First live run of check_data_model_drift.py's default-mismatch comparison
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Integrity
**Owner:** Data Model & Domain Schema Owner
**Source:** PR #2072 agent-mediated review (Product Owner role), ST-37 / EPIC-06, sprint execution `2026-10-16__release-v9.13` — 2026-10-17
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
ST-37 (BLG-SPEC-184) added a default-mismatch class to `scripts/check_data_model_drift.py`, but it has only been tested against fixtures and mocked rows. No live database was queried, under the rule that a live query needs the user's permission. Until a real run happens, nobody knows whether `data_model.md`'s `CREATE TABLE` defaults have drifted elsewhere the way `fees_paid DEFAULT 0` had. Nor is it known how many false positives come from defaults set later by `ALTER TABLE`, which the comparison does not read.

**Scope**
- With the user's permission, run `python3 scripts/check_data_model_drift.py docs/specs/data_model.md` read-only against staging (and production, if permitted)
- Triage every default mismatch: correct `data_model.md`, or record it as a known false positive in §Drift Detector Triage

**Acceptance Criteria**
- The run is recorded with its date and target environment
- Every reported default mismatch has a recorded disposition

---

### BLG-OPS-193 — Restore eslint-config-react-app so the frontend builds on Render and GitHub Pages
**Priority:** P1 (High)
**Type:** Operations / Build & Deploy
**Owner:** Infrastructure & Operations Owner
**Source:** Sprint execution `2026-10-16__release-v9.13` EPIC-02, ST-10 staging manual check (DEL-20261017-01): the Render staging frontend build of `826ee17a` failed — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
`react-scripts build` lints with the `react-app` config named in `package.json` `eslintConfig`, which comes from the `eslint-config-react-app` package. `2909e67e` (ST-28, EPIC-04, v9.12 dependency bumps) regenerated `package-lock.json` without that package, so the build fails with `[eslint] Failed to load config "react-app" to extend from.` The Render staging frontend failed this way on 2026-10-27, and the production GitHub Pages deploy (`deploy.yml`) has failed at its Build step on every `main` push since `2909e67e`; its last success was `efdd9494` on 2026-10-15 (the failed runs' logs have expired, so the cause there is inferred). CI and Playwright set `DISABLE_ESLINT_PLUGIN=true` (`playwright.config.js`), so no check exercises the real build.

**Scope**
- Restore `eslint-config-react-app` to the lockfile (declare it explicitly in `devDependencies` if `npm install` drops it again), or remove the `eslintConfig` block if lint-at-build is not wanted, and record which
- Confirm `CI=false npm run build` passes without `DISABLE_ESLINT_PLUGIN`, then re-run `deploy.yml` and confirm production goes live
- Add a CI step that runs the production build without `DISABLE_ESLINT_PLUGIN`, so a lockfile change that breaks it fails a PR
- Remove the temporary `DISABLE_ESLINT_PLUGIN=true` environment variable from the Render `trading-assistant-staging` service if it was added as a workaround, or record it in `render.yaml` if kept

**Acceptance Criteria**
- `deploy.yml` succeeds on `main` and production serves the new build
- The Render staging frontend builds from `main` with no dashboard-only ESLint workaround, or the workaround is in `render.yaml`
- A PR that removes `eslint-config-react-app` from the lockfile fails CI

---

### BLG-QA-229 — Repeat the Stop Freshness manual check with stamped positions
**Priority:** P3 (Low)
**Type:** QA / Staging Verification
**Owner:** Infrastructure & Operations Owner; QA & Testing Owner
**Source:** EPIC-02 agent-mediated DoQ review (Director of Quality role), ST-10, sprint execution `2026-10-16__release-v9.13` — 2026-10-27
**Effort:** XS (<1h)
**Provisional-Target:** v9.14

**Problem**
ST-10's AC 2 asks for the System Status Stop Freshness value to match a recorded manual check. The 2026-10-27 staging check (`qa_evidence_EPIC-02.md`, `DEL-20261017-01`) matched only the empty state: both open staging positions (BARC, LGEN) had a NULL `stop_calculated_at`, so the median and maximum age and the oldest ticker were never compared with the database. The age calculation on real `TIMESTAMPTZ` values from the driver is unchecked on a deployed environment. Staging stamps come only from the on-load path after grace, because `nightly-stop-update.yml` calls `API_URL`, not `STAGING_API_URL`.

**Scope**
- Once at least one (ideally two or more) open staging position has a non-NULL `stop_calculated_at` (for example after loading Positions for a position past day 10), read the panel and run the read-only query in `metrics_definitions.md` §Stop Freshness → Manual check at about the same time
- Record both in the QA evidence of the cycle that runs it

**Acceptance Criteria**
- The panel's median, oldest age and oldest ticker match the query's non-NULL `age_hours` median, maximum and ticker (allowing for the seconds between reads), with date and environment recorded
- Any mismatch is filed as a defect

---

### BLG-BE-190 — US position sizing multiplies the stop distance by the GBP/USD rate instead of dividing
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Strategy Correctness
**Owner:** Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner
**Source:** EPIC-02 agent-mediated DoQ review (Director of Quality role), ST-14 strategy-values check, sprint execution `2026-10-16__release-v9.13` — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
The system's FX rate is GBP/USD, i.e. USD per GBP: `add_position()` stores `entry_price` in GBP as the native price divided by `fx_rate` (`data_model_positions_dictionary.md` `entry_price`, `fx_rate`), and `size_position()` itself converts costs to GBP by dividing (`sizing_service.py` estimated cost, sector price). But `size_position()` computes `raw_shares = risk_amount / (stop_distance * fx_rate_used)` (`backend/services/sizing_service.py` §4.1.3 block). A US stop distance of D dollars is D / fx pounds of risk per share, so the correct count is `RiskAmount × fx / D`; the code's suggestion risks `RiskAmount / fx²`, about 53–62% of the budget at fx 1.27–1.37. The ST-14 property oracle (`tests/test_strategy_invariants_property.py`, both the upper bound and the new lower bound) encodes the same inverted direction, so the tests pass on the wrong value. Pre-existing; not introduced by EPIC-02.

**Scope**
- Confirm the FX convention with the Strategy Rules & System Intent Owner against `strategy_rules.md` §4.1.2/§4.1.5, and state the US formula explicitly in §4.1.3 or §4.1.5 if it is ambiguous (RISK-02 route if `strategy_rules.md` changes)
- Correct `size_position()` and the property-test oracle together, with a worked US example test (e.g. £100 risk, $10 stop distance, fx 1.27 → 12.7 shares)
- Check every other US risk or sizing calculation (frontend Trade Entry risk display, heat impact, `MaxAffordableShares`) for the same inversion
- Update `portfolio_endpoints.md` §POST /portfolio/size if its example shows the old value

**Acceptance Criteria**
- For a US position, `suggested_shares × StopDistance / fx` is within one 4dp floor step of `RiskAmount`
- The property test asserts the corrected relationship and fails against the old formula
- Any other inverted calculation found is fixed or filed

---

### BLG-BE-191 — Monthly P&L narrative treats missing restatement fields as "not restated"
**Priority:** P3 (Low)
**Type:** Backend Engineering / AI Input Correctness
**Owner:** Backend Engineering Lead; Strategy Rules & System Intent Owner (§13 check)
**Source:** PR #2073 agent-mediated review (Director of Quality role), ST-09 / EPIC-02, sprint execution `2026-10-16__release-v9.13` — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
Since v9.13 ST-09, `get_monthly_pnl_report` leaves out all four restatement fields when the `monthly_pnl_snapshots` store fails, instead of failing the request. `monthly_pnl_narrative_service.build_inputs` sets `"restated": bool(r.get("restated"))`, so a missing field becomes `False`. During a snapshot outage, `POST /reports/monthly-pnl/narrative` therefore spends a model call, counts against the daily cap, and stores a narrative whose inputs say no month was restated when the status is unknown. Before ST-09 that path failed with the request.

**Scope**
- Decide the behaviour: fail closed (503, no model call) or pass an explicit restatement-unavailable flag in the inputs and prompt
- Update `build_inputs` and the input hash accordingly
- Update `reports_endpoints.md` §POST /reports/monthly-pnl/narrative

**Acceptance Criteria**
- With the snapshot read mocked to fail, the narrative endpoint either returns 503 without calling the model or sends inputs that mark restatement as unavailable (unit test)
- No stored narrative row records `restated: false` for a month whose restatement status was unknown
- The contract documents the behaviour

---

### BLG-FE-233 — Stop Freshness panel: fix the 48 h and negative-age formats, follow page refresh, and explain its states
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Engineering Lead; Frontend Specifications & UX Documentation Owner
**Source:** PR #2073 agent-mediated reviews (Director of Quality and Product Owner roles), ST-10 / EPIC-02, sprint execution `2026-10-16__release-v9.13` — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
`formatStopAge` (`src/pages/SystemStatus.js`) picks the branch before rounding, so ages from 47.95 h to just under 48 h show "48.0 h" while 48.0 h shows "2 d 0 h"; SC-SS-09b pins "48.0 h" under a "below 48 h" comment. A negative age from small clock skew would show "-0.1 h". The panel's own query is not tied to the page's Refresh button (which refetches health only) or auto-refresh, so its figures and "As of" time go stale until remount. "Stop freshness unavailable." has no retry, and "N never recalculated" does not say when stops get stamped.

**Scope**
- Round first, then choose the branch; clamp negative ages to 0 (or state the intended rounding in `system_status.md`)
- Refetch the panel from the page's Refresh button and auto-refresh
- Add a retry action to the unavailable state and a muted hint to the never-recalculated state (grace period, on-load recompute, nightly job)
- Correct SC-SS-09b's comment and expectation; update `system_status.md`

**Acceptance Criteria**
- 47.96 h renders "2 d 0 h" (or the spec states otherwise and the test matches); a negative age renders "0.0 h"
- Playwright: clicking Refresh, and auto-refresh, re-request `GET /positions/stop-freshness` and update "As of"
- The unavailable state's retry works; the never-recalculated hint renders only when `never_recalculated > 0`

---

### BLG-UX-06 — Plain-language guidance when Trade Entry has no valid stop, and no internal references in stop-rule errors
**Priority:** P3 (Low)
**Type:** UX / Copy
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner; API Contracts & Documentation Owner (400 wording)
**Source:** PR #2073 agent-mediated reviews (Product Owner and Director of Quality roles), ST-06 and ST-08 / EPIC-02, sprint execution `2026-10-16__release-v9.13` — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
ST-06's "No valid stop" caption on Trade Entry explains why there is no stop but cites "§5" and gives no next step (for example, that the instrument is too volatile for the strategy). When the fetched ATR is rejected at save, the trader sees the backend 400 only in a toast that disappears, and it cites "strategy_rules.md §5"; the ST-08 settings 400 similarly cites §11/§12.3, with precedent at `main.py` and `pre_entry_validation.py`. The fetched-ATR 400 in `position_service.add_position` also hard-codes "14-day" instead of `ATR_PERIOD_DAYS`, unlike the caption and the settings 400. The current wording was set by `ESC-EXEC-20261017-02` condition 2, so a change needs a recorded decision.

**Scope**
- Decide, with a decision record, whether user-facing errors drop document references; revise the `initial-stop-invalid` caption and the fetched-ATR 400 to plain language with a next step, keeping the ATR, its source and the entry figures
- Build the 400 from `ATR_PERIOD_DAYS`
- Decide whether the save-time rejection should stay visible on the form rather than only in a toast
- Update `position_form.md`, `portfolio_endpoints.md` (and `settings_endpoints.md` if its wording changes), SC-TAP-06 and SC-TAP-08

**Acceptance Criteria**
- No hard-coded ATR period in the message (a test patches the constant)
- If adopted, the caption and messages contain no document or section references and state a next step; contract text matches the code exactly
- The Strategy Rules & System Intent Owner confirms the reject behaviour is unchanged

---

### BLG-UX-07 — Mark code-written notes in AI briefing and chat answers as system-added
**Priority:** P3 (Low) — provisional; set from the `[STOP-TIME-MISSING]` miss rate before planning
**Type:** UX / AI Advisory Presentation
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner; API Contracts & Documentation Owner (response shape)
**Source:** ST-16 AC 4 / EPIC-03, sprint execution `2026-10-16__release-v9.13` — Head of UX & Design answer (agent-mediated, §5.3) recorded in `ESC-EXEC-20261027-01` — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
Code appends deterministic notes to AI text: the stop-time note "(<TICKER> stop last recalculated …)" (ST-04, v9.12; chat focus ticker ST-16, v9.13) and, from ST-17 (v9.13), the briefing caveat for a ticker outside the context. They render exactly like model prose, so the reader cannot tell what the system added from what the model wrote. The Head of UX & Design answered that provenance needs visible "system-added" styling. Because `summary`, `actions[].description` and chat `response` are plain strings, styling needs a structured field or a delimiter, which changes the contract and `openapi.yaml`.

**Scope**
- Before planning: pull the `[STOP-TIME-MISSING]` miss rate (with the user's permission for the read-only DB query) and set priority from it
- Choose how the notes are carried (separate field such as `system_notes`, or a delimiter) and record it in `ai_endpoints.md` and `openapi.yaml`
- Style the notes as system-added in the Daily Briefing card and the AI Trade Advisor widget, covering both note kinds

**Acceptance Criteria**
- The miss rate and resulting priority are recorded before the item enters a sprint
- Both note kinds render with a visible system-added treatment that passes AA contrast in both themes (Playwright, including an axe scan)
- Model text is still never edited; the contract and `openapi.yaml` describe the new shape

---

### BLG-FEAT-100 — Decide whether Stop Freshness needs a staleness threshold
**Priority:** P4 (Backlog)
**Type:** Product Feature / Decision
**Owner:** Product Owner; Metrics Definitions & Analytics Owner; Strategy Rules & System Intent Owner
**Source:** PR #2073 agent-mediated review (Product Owner role), ST-10 / EPIC-02, sprint execution `2026-10-16__release-v9.13` — 2026-10-27
**Effort:** XS (<1h) for the decision; S if adopted
**Provisional-Target:** TBD

**Problem**
§7.1 recalculates stops daily, but the v9.13 Stop Freshness metric is deliberately neutral ("Threshold: none"). A trader cannot tell from the panel whether an oldest stop of 3 days is normal (a weekend) or a failed recalculation job, so the panel informs but never alerts.

**Scope**
- Decide whether a threshold is wanted; if so, define a trading-day-aware one in `metrics_definitions.md` §Stop Freshness and add a design record for a status indication on the panel

**Acceptance Criteria**
- A dated decision is recorded
- If adopted: the definition is in `metrics_definitions.md` and the panel shows the status for a stale case, covered by Playwright; if rejected: the rationale is on the "Threshold: none" line

---

### BLG-BE-192 — Compute the SPY market regime from Alpaca bars when Yahoo Finance fails
**Priority:** P2 (Medium)
**Type:** Backend / Data Provider Resilience
**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Source:** ST-33 (BLG-OPS-77), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/operations/data_provider_risk_assessment.md` §3 QW-1 — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
`check_market_regime()` reads SPY and FTSE 200-day data only from Yahoo Finance. When Yahoo fails it defaults that market to risk-on, so during a Yahoo outage US entries are allowed and no US risk-off exit alert is raised, whatever the market is doing. Alpaca already supplies US daily bars and could compute the SPY figure.

**Scope**
- When the Yahoo SPY fetch fails, compute SPY price and 200-day MA from Alpaca daily bars (`get_ohlcv_bars("SPY", limit=210)`)
- Record which source produced the regime result

**Acceptance Criteria**
- With Yahoo mocked to fail and Alpaca mocked to return bars, the SPY regime is computed from the Alpaca bars, not defaulted to risk-on (test)
- With both failing, behaviour is unchanged until BLG-BE-193 rules otherwise (test)

---

### BLG-BE-193 — Show an unknown market regime instead of silently defaulting to risk-on
**Priority:** P2 (Medium)
**Type:** Backend / Data Provider Resilience
**Owner:** Strategy Rules & System Intent Owner; Infrastructure & Operations Owner
**Source:** ST-33 (BLG-OPS-77), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/operations/data_provider_risk_assessment.md` §2, §3 QW-2 — 2026-10-27
**Effort:** S (~0.5d, plus a strategy ruling)
**Provisional-Target:** v9.14

**Problem**
When SPY or FTSE regime data is unavailable, `check_market_regime()` sets that market to risk-on with price and MA 0, and nothing tells the user. Entry checks and the nightly risk-off job then act on a regime that was never measured. This is the most consequential single failure in the data-provider assessment.

**Scope**
- Strategy Rules & System Intent Owner rules what "regime unknown" means for entries and the risk-off job (block entries, keep the last known regime, or risk-on with a warning)
- Return an explicit unknown state from `check_market_regime()` and apply the ruling
- Show the unknown state wherever the regime is shown

**Acceptance Criteria**
- A dated ruling is recorded
- With regime data mocked unavailable, the result is marked unknown and the ruled behaviour applies (tests)
- The dashboard shows the regime as unknown in that case (Playwright)

---

### BLG-BE-194 — Use the last good GBP/USD rate, with its age, before the fixed 1.27 fallback
**Priority:** P2 (Medium)
**Type:** Backend / Data Provider Resilience
**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Source:** ST-33 (BLG-OPS-77), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/operations/data_provider_risk_assessment.md` §2, §3 QW-3 — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
`get_live_fx_rate()` gets GBP/USD only from Yahoo Finance. After the 5-minute cache expires it falls back to the constant `DEFAULT_FX_RATE = 1.27`, so a Yahoo outage silently values every US position, and sizes new ones, at a fixed rate that can be far from the market.

**Scope**
- Store the last successfully fetched rate and its timestamp
- On fetch failure, use the stored rate before the constant
- Expose the rate's source and age where FX-dependent figures are shown

**Acceptance Criteria**
- With Yahoo mocked to fail, the last stored rate is used, not 1.27 (test)
- The constant is used only when no stored rate exists (test)
- The rate's age is shown when it is older than one trading day

---

### BLG-FE-234 — Mark a position's price as stale when the live price fetch fails
**Priority:** P3 (Low)
**Type:** Frontend / Data Provider Resilience
**Owner:** Infrastructure & Operations Owner; Head of UX & Design
**Source:** ST-33 (BLG-OPS-77), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/operations/data_provider_risk_assessment.md` §2, §3 QW-4 — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14

**Problem**
When `get_current_price()` returns nothing, the positions view falls back to the stored `current_price` or the entry price and shows it as if it were live. UK prices have no second source, so a Yahoo outage shows stale UK P&L and stop distances with no sign that they are stale.

**Scope**
- Return a flag from the positions response when the live price fetch failed and a stored price is used
- Show a stale-price marker on that position

**Acceptance Criteria**
- With the price fetch mocked to fail, the response flags the stored price (test)
- The positions view shows the stale marker for that position (Playwright)

---

### BLG-SPEC-209 — Correct the external API dependency register and credential inventory for Alpaca news and the inactive Stooq and Twelve Data fetchers
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** PMO Lead; Infrastructure & Operations Owner
**Source:** ST-33 (BLG-OPS-77), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/operations/data_provider_risk_assessment.md` §1, §3 QW-5 — 2026-10-27
**Effort:** XS (<1h)
**Provisional-Target:** v9.14

**Problem**
`docs/ops/external_api_dependency_register.md` describes the news provider as newsapi.org, but news comes from Alpaca's news endpoint (`news_service.py`). Its MIT-08 says the screener falls back to Stooq and Twelve Data, but `fetch_ohlcv` never calls either fetcher. Anyone relying on the register during an incident would expect failover that does not exist.

**Scope**
- Rewrite the News API entry for Alpaca news
- Correct MIT-08 to say Stooq and Twelve Data are not active, and why
- In `docs/ops/external_api_credential_inventory.md`, retire the `NEWS_API_KEY` (newsapi.org) entry and record the Alpaca entry's cost tier (free while `ALPACA_DATA_FEED` is `iex`)
- Delete the two unused fetchers from `screener_data_service.py`, or record why they are kept

**Acceptance Criteria**
- The register and the credential inventory match the code for news and screener fallbacks
- The two fetchers are either removed with tests still passing, or their retention is documented

---

### BLG-OPS-194 — Make the System Status Yahoo Finance check detect an outage
**Priority:** P2 (Medium)
**Type:** Operations / Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** ST-33 (BLG-OPS-77), EPIC-05, cycle `2026-10-16__release-v9.13` — agent-mediated Infrastructure & Operations Owner review of `docs/operations/data_provider_risk_assessment.md` §2, §3 QW-6 — 2026-10-27
**Effort:** XS (~1-2h)
**Provisional-Target:** v9.14

**Problem**
The System Status Yahoo Finance check calls `get_live_fx_rate()` and reports healthy unless it raises (`health_service.py:310-320`). `get_live_fx_rate()` never raises; it returns the constant 1.27 on failure. The rolling `yahoo_finance` metrics are fed only by screener calls and reset on restart. A Yahoo outage therefore shows as healthy, while the regime fails open to risk-on and FX freezes.

**Scope**
- Have the FX fetch report whether it fell back to the constant, and mark the Yahoo Finance check unhealthy (or degraded) when it did
- Do the same when the latest market-regime fetch defaulted a market to risk-on because its data was unavailable
- Show the reason in the check's details

**Acceptance Criteria**
- With the Yahoo FX fetch mocked to fail, the health check reports Yahoo Finance unhealthy or degraded, not healthy (test)
- With the fetch succeeding, it reports healthy with the live rate (test)
- With the regime fetch mocked to fail, the check is not reported healthy (test)

---

### BLG-OPS-195 — Alert when weekly market-data call volume exceeds 2× the baseline
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Source:** ST-30 (BLG-OPS-18), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/ops/data_pipeline_cost_baseline.md` §5 — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.14
**Depends on:** ST-30's weekly baseline recorded in `docs/ops/data_pipeline_cost_baseline.md` §4

**Problem**
`data_pipeline_cost_baseline.md` §5 defines an advisory when a source's weekly calls, failures or estimated cost exceed 2× baseline, but nothing checks it; the comparison is manual at the monthly cost review. A provider starting to throttle, or a feature that suddenly multiplies calls, can go unnoticed for weeks.

**Scope**
- A weekly scheduled workflow that calls `GET /ops/api-call-attribution?window=weekly`, compares each source's calls, failures and estimated cost with the recorded baseline, and sends a Telegram message naming the source and the top features when any exceeds 2×
- Keep the baseline figures in one place the check reads, not copied into the workflow

**Acceptance Criteria**
- A test with a report over 2× baseline produces the advisory message, and one under it produces none
- A failed report call fails the workflow loudly (as `ai-daily-cost-check.yml` does)

---

### BLG-OPS-196 — Confirm both staging services deploy from main, then retire the old hook
**Priority:** P2 (Medium)
**Type:** Operations / Deployment
**Owner:** Infrastructure & Operations Owner
**Source:** ST-29 (BLG-OPS-189), EPIC-05, cycle `2026-10-16__release-v9.13` — post-merge remainder of AC 2 and AC 4, `DEL-20261027-03` — 2026-10-28
**Effort:** XS (<1h)
**Provisional-Target:** v9.14
**Depends on:** EPIC-05 merged to `main`

**Problem**
ST-29 changed `staging-deploy.yml` to call one deploy hook per staging service and wait on each, and both new hook secrets are set. Its AC 2 (a green run on `main` with both services live on the run's commit) and AC 4 (the smoke test confirms the host behind `STAGING_API_URL`) can only be checked by the first run on `main` after EPIC-05 merges, because `main` still has the old single-hook workflow. Until then, staging deploys from `main` keep timing out, and other stories' staging checks depend on them.

**Scope**
- After EPIC-05 merges, confirm the `staging-deploy.yml` run on `main` (or dispatch one)
- Record the run in `qa_evidence_EPIC-05.md` and close `DEL-20261027-03`
- Delete the retired `RENDER_STAGING_DEPLOY_HOOK` repository secret once that run is green

**Acceptance Criteria**
- A green `staging-deploy.yml` run on `main` shows both trigger steps' deploy IDs matching their services, both services live on the run's commit, and the smoke-test host check passing (`srv-d6rtdg94tr6s73ce2j6g`); its run ID is recorded in `qa_evidence_EPIC-05.md`
- `RENDER_STAGING_DEPLOY_HOOK` no longer appears in `gh secret list`

---

### BLG-OPS-197 — Record the weekly market-data call-volume baseline from production
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** ST-30 (BLG-OPS-18) and ST-31 (BLG-OPS-19), EPIC-05, cycle `2026-10-16__release-v9.13` — post-merge remainder, `DEL-20261027-06` and the production half of `DEL-20261027-04` — 2026-10-28
**Effort:** XS (<1h)
**Provisional-Target:** v9.14
**Depends on:** EPIC-05 merged and deployed to production; 7 days of production data

**Problem**
ST-30 filed the combined weekly cost baseline ($0.00, every source free) and the 2× advisory threshold, but the per-source weekly call volumes in `docs/ops/data_pipeline_cost_baseline.md` §4 are pending: they need a week of production attribution data, which only exists after EPIC-05 deploys. ST-31's DS-36 columns were confirmed on staging; their production Live Confirmation is also outstanding. Without the volume baseline, the 2× advisory (and BLG-OPS-195's automated check) has nothing to compare with.

**Scope**
- After the production deploy, run DS-36's Verification query on production and record it in `data_model.md` DS-36
- 7 full days after deploy, call `GET /ops/api-call-attribution?window=weekly` on production and fill §4's calls and failures per source, with the date and `top_contributors`
- Close `DEL-20261027-04` and `DEL-20261027-06`

**Acceptance Criteria**
- DS-36 Live Confirmation for production is recorded: `api_call_log.feature` text YES, `screener_runs.duration_seconds` numeric YES, index `idx_acl_called_at_feature`
- `data_pipeline_cost_baseline.md` §4 has weekly calls and failures for each source and combined, from one production weekly report, with its date and top contributors; the §6 volume sign-off line is ticked

---

### BLG-OPS-198 — Record the full screener run p50/p95 baseline from production
**Priority:** P3 (Low)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner
**Source:** ST-32 (BLG-OPS-23), EPIC-05, cycle `2026-10-16__release-v9.13` — post-merge remainder of AC 1, `DEL-20261027-05` — 2026-10-28
**Effort:** XS (<1h)
**Provisional-Target:** v9.14
**Depends on:** EPIC-05 merged and deployed to production; at least 10 nightly production screener runs after deploy

**Problem**
ST-32 made each screener run record `duration_seconds` and added `scripts/screener_run_benchmark.py`, which computes p50/p95 over full-universe runs, and defined the >1.5× regression threshold in `docs/ops/api_performance_baseline.md` §53. The p50/p95 values themselves are pending: runs before v9.13 have no duration, so the baseline needs about 10 nightly production runs (two weeks of weekdays) after deploy. Until then the regression threshold has no baseline to multiply.

**Scope**
- After at least 10 nightly production runs, run `API_URL=<production> API_KEY=<key> python3 scripts/screener_run_benchmark.py`
- Record its output (runs counted, min tickers, p50, p95, regression threshold, first and last run) in `api_performance_baseline.md` §53
- Close `DEL-20261027-05`

**Acceptance Criteria**
- The script exits 0 (at least 10 qualifying runs) and its p50, p95 and 1.5× threshold in seconds are recorded in `api_performance_baseline.md` §53 with the run date range

---
