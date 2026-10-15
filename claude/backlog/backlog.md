# Product Backlog — Momentum Trading Assistant

<!-- last-spec-debt-deep-review: 2026-10-06__release-v9.10 -->

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-10-15 (session — ST-29, EPIC-04, 2026-10-12__release-v9.12: BLG-OPS-181 Notes cause line (plan-authorised, sprint_backlog.md ST-29 Notes); 1 new item BLG-OPS-189); prior — 2026-10-15 (session — 1 new item added from Sprint Execution ST-32, EPIC-04, 2026-10-12__release-v9.12: BLG-OPS-188); prior — 2026-10-15 (session — 1 new item added from Sprint Execution ST-31, EPIC-04, 2026-10-12__release-v9.12: BLG-QA-225); prior history retained — see prior entries in version control
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

### BLG-BE-144 — First-time Settings save writes NULL strategy columns; trade-plan settings snapshot records editable-row multipliers
**Priority:** P3 (Low)
**Type:** Backend / Data Integrity
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Source:** ST-01/ST-02/ST-04 (EPIC-01, cycle `2026-10-06__release-v9.10`) — agent-mediated Director of Quality review of the EPIC-01 PR — 2026-10-06
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
After ST-01 (ruling (a)), the Settings page no longer sends `min_hold_days`, `atr_period`, `atr_multiplier_initial` or `atr_multiplier_trailing`. On the first-time create path, `SettingsRequest.dict()` fills them as None, and `create_settings` inserts every key (`database.py`), which overrides the column defaults with NULL. No stop path reads them, but `routers/trade_plans.py` still copies those row values into `effective_settings_snapshot`. Under ruling (a) that snapshot is misleading.

**Scope**
- `create_settings` (and update) drops None values.
- Trade-plan snapshots record the fixed §11 values from `utils/strategy_parameters.py`.
- A Playwright or API test covers the create path (SC-SPF-04 covers update only).

**Acceptance Criteria**
- [ ] A first-time Settings save leaves the four columns at their defaults
- [ ] New trade-plan snapshots carry the §11 values

---

### BLG-BE-145 — US position with NULL fill_price crashes both stop recompute paths; no US coverage in parity tests
**Priority:** P3 (Low)
**Type:** Backend / Robustness
**Owner:** Head of Engineering
**Source:** ST-01/ST-02/ST-04 (EPIC-01, cycle `2026-10-06__release-v9.10`) — agent-mediated Director of Quality review of the EPIC-01 PR — 2026-10-06 (pre-existing; not introduced by EPIC-01)
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`pos.get('fill_price', entry_price)` returns None when the key exists but is NULL (`position_service.py`, in `analyze_positions` and `run_nightly_trailing_stop_update`). A US position with a NULL `fill_price` would raise in stop arithmetic. The ST-01 parity and ST-02 provenance fixtures are all UK, so the US branch is untested on both paths.

**Scope**
- Fall back to `entry_price` when `fill_price` is NULL, as `pos.get('fill_price') or entry_price`.
- Add US-position cases to `tests/test_strategy_parameter_parity.py` and `tests/test_atr_provenance.py`.

**Acceptance Criteria**
- [ ] A NULL `fill_price` US position recomputes without error on both paths. Both test files include a US case.

---

### BLG-BE-148 — Gap-risk "next trading session" ignores exchange holidays and the US market date
**Priority:** P3 (Low)
**Type:** Backend / Correctness
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Source:** ST-13/ST-14 (EPIC-03, cycle `2026-10-06__release-v9.10`) — agent-mediated Director of Quality / Product Owner pre-PR review of the EPIC-03 branch — 2026-10-07
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
`gap_risk_service._days_to_next_trading_day` uses a weekday calendar and the server's `date.today()` (UTC), as the ST-13 addendum discloses. Two cases miss an actionable flag:
1. **Holidays.** Viewed Friday before a Monday market holiday, Tuesday earnings are 4 days away and are not flagged. On Monday no session exists, so the last actionable session goes unflagged.
2. **Date basis.** Between 00:00 and about 05:00 UTC the US trading date is still the previous day. In that window, earnings due the next US session read as day 0 and are not flagged.

**Scope**
- Use the US exchange calendar (holidays, the `America/New_York` date) for "today" and the next session. Keep it deterministic, with no network call at request time.
- If this changes Ruling 3's stated rule, record a dated addendum note in the §13 review record (Strategy Rules & System Intent Owner).

**Acceptance Criteria**
- [ ] A Friday view before a Monday holiday flags Tuesday earnings (unit test).
- [ ] A 02:00 UTC view uses the US market date (unit test).

---

### BLG-BE-149 — Risk page `display_status` decides LOSING/PROFITABLE on GBP P&L; the lifecycle badge uses native P&L
**Priority:** P3 (Low)
**Type:** Backend / Spec–Code Consistency
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Source:** ST-11 (EPIC-03, cycle `2026-10-06__release-v9.10`) — agent-mediated Director of Quality / Product Owner pre-PR review of the EPIC-03 branch — 2026-10-07
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
ST-11 ruled that post-grace LOSING/PROFITABLE follow §9's P&L sign, on the native price against entry, which is the test that picks the §7.2 stop multiplier (`is_profitable = pnl_native > 0`). `display_status` in `position_service.py` and `portfolio_service.py` uses `pnl_gbp > 0`, which includes FX movement. It is shown on the Risk page (`PositionRiskTable.js`). A US position that is up in dollars but down in sterling (or the reverse) therefore shows LOSING on one page and PROFITABLE on the other, contrary to role charter §5 ("UI, backend logic, and analytics interpret states consistently").

**Scope**
- Derive `display_status` from the same native test, or from `position_state`, and state the basis in `position_endpoints.md` / `portfolio_endpoints.md`.

**Acceptance Criteria**
- [ ] For a US position with native P&L > 0 and GBP P&L < 0, `display_status` and `position_state` agree (unit test).

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

### BLG-TECH-22 — Batch the in-range dependency patch/minor bumps from the October 2026 quarterly review
**Priority:** P3 (Low)
**Type:** Platform / Technical Debt
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** ST-17 (BLG-OPS-92), EPIC-04, cycle `2026-10-06__release-v9.10` — `docs/security/dependency_update_review_2026-10-06.md` — 2026-10-06
**Effort:** S (~0.5-1 day)
**Provisional-Target:** TBD

**Problem**
The quarterly review found 8 backend and 20 frontend direct dependencies behind their latest patch/minor release, with no known vulnerabilities. They were not applied in-story because each lockfile or requirements change needs its own full CI run. yfinance (1.3.0 → 1.7.0) matters most: it tracks Yahoo's changing endpoints, so falling behind risks silent price/ATR fetch failures.

**Scope**
- Backend: fastapi + starlette, pandas, numpy, pydantic, psycopg2-binary, hypothesis, yfinance, at the versions in the review's §3
- Frontend: every row marked "Batch" in the review's §4–§5 (`npm update` within the existing ranges, plus eslint 9.39.5)

**Acceptance Criteria**
- [ ] Bumps applied in one PR. The full pytest suite and all Playwright shards pass in CI, including the focus-restoration specs, because `@radix-ui/react-dialog` changes.
- [ ] A staging check confirms yfinance price and ATR fetches still work for one US and one UK ticker

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

### BLG-QA-212 — Add unit tests for scripts/compute_role_share_history.py now that roadmap §7.2 depends on it
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner; PMO Lead
**Source:** PR #1891 agent-mediated Director of Quality review (EPIC-04, cycle `2026-09-30__release-v9.9`) — 2026-10-05
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`roadmap_prompt.md` v9.30 §7.2 step 1 now requires running `scripts/compute_role_share_history.py` to append each shipped cycle's row to `claude/roadmap/role_share_history.md`. The script has no tests (`git grep compute_role_share_history -- tests` returns nothing). It silently drops any ST block that has no `**Owner:**` line, which understates the total. It also matches only `#### ST-` headings. Today its totals equal the ST-heading counts for every cycle from v7.6 to v9.9, but nothing would catch a format drift in a future `sprint_backlog.md`. The same gap exists for STEP 7.1 in `compute_rebalance_diagnostics.py`: only STEP 2.4 is pinned against the real changelog, and a 7.1 pin would have caught the 84.0%/84.8% misstatement (finding F-1).

**Scope**
- Add `tests/test_compute_role_share_history.py` covering:
  - a fixture with simple and compound Owner strings
  - a story with no Owner line, which should produce a warning or non-zero exit rather than a silent drop
  - the `--json` output shape
  - a regression pin against `claude/cycles/2026-09-28__release-v9.8/sprint_backlog.md` (39 stories, Head of Specs Team 12)
- Make the script report stories it found but could not attribute, rather than dropping them silently
- Add a STEP 7.1 real-changelog pin to `tests/test_compute_rebalance_diagnostics.py` (v9.6–v9.8 window → 84/99 = 84.8%)

**Acceptance Criteria**
- New test file passes in CI Phase B and covers compound owners, a missing Owner line and the v9.8 regression pin
- The script's total equals the number of ST headings, or it reports the difference
- The STEP 7.1 real-changelog figure is pinned in a test

---

### BLG-GOV-367 — Skill-Silo rolling-3-cycle series mixes a plain per-cycle average with §7.1's pooled formula
**Priority:** P3 (Low)
**Type:** Governance Process / Metrics Integrity
**Owner:** Metrics Definitions & Analytics Owner; Head of Specs Team
**Source:** PR #1891 agent-mediated Product Owner review (EPIC-04, cycle `2026-09-30__release-v9.9`) — 2026-10-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`roadmap_prompt.md:563` defines Governance story % as a pooled ratio: (G+D+P) ÷ total stories over the last 3 cycles. The recorded series in `claude/roadmap/decision_log.md` is labelled "rolling-3-cycle avg" and matches a plain mean of the per-cycle percentages. For example, 85.7% = mean(100.0, 75.0, 82.1). ST-25's `scripts/compute_rebalance_diagnostics.py` computes the pooled form (84.8% for v9.6–v9.8, against the recorded 83.7%). Once rebalances adopt the script, the "improving/worsening" comparison against prior readings mixes the two methods. That comparison drives §7.1's mandatory pull-forward after 3 consecutive worsening readings, so a change of method could flip a trend reading that the data does not support.

**Scope**
- Confirm which method §7.1 intends (pooled per its formula, or plain mean per the recorded series) and state it explicitly in §7.1
- Restate the recent readings (at least the last 4) under the chosen method, or record an explicit method-break note the next rebalance must honour when judging trend direction
- Align `compute_rebalance_diagnostics.py`'s output (or add a flag) with the chosen method; apply the CLAUDE.md §6 checklist if `roadmap_prompt.md` changes

**Acceptance Criteria**
- §7.1 names one aggregation method unambiguously
- The next rebalance's trend comparison uses readings computed by that single method, or cites the recorded method-break note

---

### BLG-SPEC-182 — Refresh the Gap Risk Flag §13 decision record to match strategy_rules.md v1.14 as applied
**Priority:** P3 (Low)
**Type:** Spec Debt / §13 Record Integrity
**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Source:** PR #1891 agent-mediated Product Owner review (EPIC-04, cycle `2026-09-30__release-v9.9`) — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** TBD (before the first §13.5 re-attestation, 2027-02-06)

**Problem**
`docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md` was updated only in its appendix after the v1.14 wording was applied. The body's write-scope note (`:11`) and Binding Condition 9 (`:175`) still state that Sprint Execution cannot write `strategy_rules.md` and that registration is pending. Remediation Item 4 (`:188`) still reads as open. Binding Condition 6 (`:172`) permits any "known, dated event specific to the position's ticker", which is wider than the second-pass-amended §13.3 (`strategy_rules.md:504`: only events already recognised as gap-risk events by a canonical rule — today only earnings). The 2027-02-06 re-attestation will read this record's binding conditions as the operative terms.

**Scope**
- Update the write-scope note, Binding Condition 9 and Remediation Item 4 to record that registration was completed in `strategy_rules.md` v1.14 (`a5d4dbd2`, BLG-GOV-360 resolved)
- Narrow Binding Condition 6's wording to match §13.3 as applied, or add an explicit note that §13.3 v1.14 supersedes it where they differ
- Bump the record's `**Last Updated:**` per the 3-entry rule

**Acceptance Criteria**
- No statement in the record's body contradicts `strategy_rules.md` v1.14 §13.3/§13.5 or describes BLG-GOV-360 as pending
- Binding Condition 6's permitted-trigger scope equals §13.3's carve-out

---

### BLG-GOV-363 — Script the execution_state.json read-back check introduced by execution_prompt.md v3.81 §9.2
**Priority:** P3 (Low)
**Type:** Governance Tooling
**Owner:** Head of Engineering; Head of Specs Team
**Source:** Head of Specs Team ruling on ESC-CLOSE-20260930-02 (agent-mediated, user-directed) — 2026-10-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`execution_prompt.md` v3.81 §9.2 makes the top-level `completed_items`, `blocked_items`, `delegated_items` and `merge_gate` fields projections of per-story `status` / per-EPIC `pr_status`, and requires a 4-equality read-back from disk after every state write. The check is currently performed by hand, which is the same memory-dependent failure mode the ruling exists to remove.

**Scope**
- Add `scripts/check_execution_state_consistency.py <execution_state.json>` asserting the 4 equalities in §9.2 (plus `status: done` ⇒ `commit_sha`/`completed_utc` set), exiting non-zero with a per-field diff
- Reference it from §9.2 as the mechanical form of the read-back (CLAUDE.md §6 checklist applies)

**Acceptance Criteria**
- Script passes on a consistent file and fails, naming the field, for each of the 4 equality breaks
- Unit tests cover each failure mode

---

### BLG-GOV-364 — Decide whether idea-intake windows may run with a reduced roster, and if so cap them
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; Product Owner
**Source:** ESC-CLOSE-20260930-01 Product Owner review (agent-mediated, confirmed by the human Product Owner) — 2026-10-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`idea_intake_prompt.md` §4 and STEP 0 assume every role in `eligible_agents` is exercised, yet `IW-20260928-01` (3 roles) and `IW-20260930-01` (2 roles) ran with a disclosed reduced roster. v2.10's roster rule now constrains such windows while a build-and-ship pull-forward is mandatory, but whether reduced windows are permitted at all — and how they interact with `roadmap_prompt.md` STEP -1.6's standalone pre-run exception — has never been ruled on. `IW-20260928-01` exercised no user-facing role, which left the PO Modify directive unsatisfiable at v9.8.

**Scope**
- Rule on whether §4/STEP 0 should permit reduced-roster windows; if yes, define when and set a cap (e.g. no two consecutive reduced windows)
- Apply the CLAUDE.md §6 checklist to any prompt changed

**Acceptance Criteria**
- A recorded ruling; any adopted change ships with the full CLAUDE.md §6 checklist

---

### BLG-GOV-368 — Pre-PR check that an EPIC branch carries no other EPIC's commits
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

### BLG-SPEC-181 — Action-rate metric spec and query docstring still cite the dropped positions.stop_price column
**Priority:** P3 (Low)
**Type:** Spec Debt / Metrics
**Owner:** Metrics Definitions & Analytics Owner; Data Model & Domain Schema Owner
**Source:** EPIC-05 agent-mediated Director of Quality review (ST-29), cycle `2026-09-30__release-v9.9` — 2026-10-05
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-29 dropped the orphaned, always-NULL `positions.stop_price` column (`data_model.md` DS-24). `docs/specs/metrics_definitions.md` (the action-rate definition, around lines 687 and 1110) and the docstring near `backend/database.py:2421` still describe the action-rate query as matching a later `PATCH /positions/{id}` that set `positions.stop_price >= recommended_stop`. The live stop column is `current_stop`. Nothing breaks today because the action-rate metric is not yet computed, but an implementation built from this text would query a column that no longer exists.

**Scope**
- Replace `positions.stop_price` with `positions.current_stop` in both `metrics_definitions.md` passages (version bump per the document's lifecycle) and in the `database.py` docstring

**Acceptance Criteria**
- No spec or code comment refers to `positions.stop_price` as a live column
- `grep -rn "positions.stop_price" docs backend` returns only historical/migration references (DS-24)

---

### BLG-QA-213 — Regression guard for the positions.fees_paid NOT NULL invariant (entry flow and SQL seeds)
**Priority:** P3 (Low)
**Type:** Testing Gap / Data Model
**Owner:** QA & Testing Owner
**Source:** PR #1892 agent-mediated Director of Quality review (EPIC-05, cycle `2026-09-30__release-v9.9`) — 2026-10-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
DS-23 (`docs/specs/data_model.md:2517`) re-applied `NOT NULL` with no default on `positions.fees_paid` in staging and production. Its justification is that every write path supplies a numeric value. Nothing in the test suite enforces this. `create_position()` binds `position_data.get('fees_paid')` (`backend/database.py:98-135`), so a refactor of `position_service.py`'s entry flow (`:838-888`) that drops or renames the key would pass all 2054 tests and fail only in production, as a `NOT NULL` violation on every new position. In the same way, no test checks that the SQL seeds (`backend/test_data/seed_chart_test_data.sql`, `scripts/seeds/seed_portfolio_trades.sql`) supply `fees_paid`. The chart seed omitted it until ST-30, and it is run against staging by `.github/workflows/seed-preview.yml:64`.

**Scope**
- Unit test (database layer mocked): open a UK and a US position through the service entry flow, capture the `position_data` passed to `create_position()`, and assert that `fees_paid` is present, non-None and numeric (≥ 0).
- Unit test: a partial exit passes a numeric, non-None `fees_paid` to `update_position()`.
- Static test: every `INSERT INTO positions` statement in `*.sql` files under `backend/` and `scripts/` names `fees_paid` in its column list, and has as many values as columns.

**Acceptance Criteria**
- [ ] Both tests fail if `'fees_paid'` is removed from `position_data` in `position_service.py`, or if its value is `None`, for either market.
- [ ] The static test fails on a fixture or temporary copy of a seed insert that omits `fees_paid`, and passes on the current repo.
- [ ] Runs under the stub `DATABASE_URL` convention, with no live DB access.

---

### BLG-SPEC-183 — positions.entry_price currency: specs say native, code stores GBP
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** PR #1892 agent-mediated Director of Quality review (EPIC-05, cycle `2026-09-30__release-v9.9`) — 2026-10-05
**Effort:** S (~0.5d; includes a read-only live sample check of US rows)
**Provisional-Target:** TBD

**Problem**
`docs/specs/data_model.md:114` ("Entry price in native currency (USD for US, GBP for UK)") and `docs/specs/data_model_positions_dictionary.md:53,58` (US `total_cost = entry_price × shares / fx_rate + fees_paid`) describe `positions.entry_price` as native currency. The application stores `entry_price_gbp` (`backend/services/position_service.py:845,882`) and the native price in `fill_price`. Readers work around this by using `fill_price` for US (`backend/services/portfolio_service.py:141`). DS-23 (`data_model.md:2536`), added in PR #1892, asserts that `entry_price` is GBP. The canonical model now contradicts itself, and the dictionary's US derivation formula is wrong for application-created rows. The fee reconstruction guidance in DS-23 and any future analytics built from the Fields table can therefore be wrong by a factor of the FX rate on US positions. The chart seed adds a third convention: UK prices in pence (`seed_chart_test_data.sql:45`).

**Scope**
- Confirm the stored convention with a read-only sample of live US rows (`entry_price` vs `fill_price / fx_rate`).
- Correct `data_model.md:114` and the dictionary's `entry_price`/`total_cost` rows (or file a code defect if native was the intended convention), and align the DS-23 reconstruction note.
- Note the pence convention in the chart seed, or normalise it.

**Acceptance Criteria**
- [ ] `data_model.md`, `data_model_positions_dictionary.md` and DS-23 state one consistent `entry_price` currency that matches `create_position()`'s input.
- [ ] The dictionary's US `total_cost` derivation matches `position_service.py`'s computation.
- [ ] The decision (doc fix vs code fix) is recorded with Data Model & Domain Schema Owner sign-off.

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

### BLG-SEC-41 — Audit trail for strategy-parameter changes in Settings
**Priority:** P3 (Low)
**Type:** Security / Integrity
**Owner:** Cybersecurity & Trust Lead
**Source:** `IDEA-cybersecurity-20261006-01` (`IW-20261006-01`), roadmap rebalance `2026-10-06__scheduled`
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
Settings writes overwrite ATR multipliers and hold days in place. They drive the on-load stop recompute and §7.3's ratchet makes the effect permanent, but nothing records who changed what and when.

**Scope**
- Append a change-log row (field, old, new, timestamp, request source) on every settings write; show the last change on the Settings page.

**Acceptance Criteria**
- [ ] Every settings write produces a log row (test).

---

### BLG-SEC-42 — Re-assess the bundled `REACT_APP_API_KEY` against its actual write scope
**Priority:** P3 (Low)
**Type:** Security / Credential Policy
**Owner:** Cybersecurity & Trust Lead; Product Owner (accept-risk)
**Source:** `IDEA-cybersecurity-20261006-02` (`IW-20261006-01`), roadmap rebalance `2026-10-06__scheduled`
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`docs/operations/credential_policy.md:34` classes the frontend key, which is embedded in the JS bundle, as 'low-sensitivity'. The same key authorises settings writes, position entry/exit and `GET /positions/analyze` (which writes stops).

**Scope**
- Re-rate the key; either scope a narrower frontend key or record an explicit Product Owner accept-risk.

**Acceptance Criteria**
- [ ] `credential_policy.md` classification states the key's write scope and the decision taken.

---

### BLG-GOV-369 — Strategy-copy conformance: frontend constants module, lint for UI text restating §5–§11, and a named owner
**Priority:** P3 (Low)
**Type:** Governance Process / Strategy Conformance
**Owner:** Head of Specs Team; Frontend Specifications & UX Documentation Owner; Director of HR (charter update)
**Source:** `IDEA-head-of-specs-20261006-02`, `IDEA-base44-frontend-20261006-02`, `IDEA-director-of-hr-20261006-02` (consolidated, `IW-20261006-01`), roadmap rebalance `2026-10-06__scheduled`
**Effort:** S (~1-1.5 days)
**Provisional-Target:** TBD

**Problem**
Strategy numbers and formulas are literals in several pages (`TradeEntry.js`, `Settings.js`, `Positions.js`, `SignalContextPanel.js`) and have drifted apart; four UI texts contradicting §5–§11 were found by chance in one idea window. No role charter owns this check.

**Scope**
- `src/constants/strategy.js` mirroring §11, used by those pages.
- A script listing `src/` strings with ATR multiples, grace lengths or stop formulas that differ from §5–§11 (CI warning).
- Add the duty to the Frontend Specifications & UX Documentation Owner charter.

**Acceptance Criteria**
- [ ] No strategy-number literals outside the constants module.
- [ ] Lint runs in CI and reports zero contradictions after `BLG-FE-195`/`196`/`197` ship.
- [ ] Charter updated.

---

### BLG-GOV-371 — Inventory the scheduled GitHub workflows: owner, cron, tables written, monthly minutes
**Priority:** P3 (Low)
**Type:** Operations / Governance
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Source:** `IDEA-finops-20261006-02`, `IDEA-infra-ops-20261006-02` (consolidated, `IW-20261006-01`), roadmap rebalance `2026-10-06__scheduled`
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
20 workflows run on a schedule and nothing lists what each writes or costs. Two of them (`daily-snapshot.yml`, `nightly-stop-update.yml`) both write stops with different parameter sources; this was found only by reading code.

**Scope**
- One table in `docs/ops/` (owner, cron, tables written, minutes/month); reviewed at each `run audit`.

**Acceptance Criteria**
- [ ] All scheduled workflows listed with a 'writes' column.

---

### BLG-GOV-372 — Add a split-credit secondary tally to `compute_role_share_history.py`
**Priority:** P3 (Low)
**Type:** Governance Process / Workforce Metrics
**Owner:** Director of HR; PMO Lead
**Source:** `IDEA-director-of-hr-20261006-01` (`IW-20261006-01`, refines `BLG-GOV-353` and the deferred Owner-field canonicalisation patch), roadmap rebalance `2026-10-06__scheduled`
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
At v9.9 all 35 stories had compound Owner strings, so the raw tally that §7.2 reads names only compound buckets and cannot show whether one role carries the load.

**Scope**
- Secondary output splitting each compound story's credit equally across its named roles; `role_share_history.md` gains a split-credit column; raw tally stays primary.

**Acceptance Criteria**
- [ ] Script emits both tallies; tests cover compound strings (extends `BLG-QA-212`).

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

### BLG-FE-200 — Reports and Notifications pages fail WCAG colour contrast in the light theme
**Priority:** P3 (Low)
**Type:** Frontend / Accessibility
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Source:** ST-19 (BLG-QA-195), EPIC-04, cycle `2026-10-06__release-v9.10` — first axe scan of these pages in both themes, 2026-10-06
**Effort:** M (~2-3 days)
**Provisional-Target:** TBD

**Problem**
The axe-core scan added by ST-19 finds serious `color-contrast` violations on the Reports page and on the Notification Preferences and History pages in the **light** theme only. The dark theme passes. Reports' Monthly tab (restated month expanded) has 25 nodes, and its Tax Year tab has 14. The pages hard-code dark-theme classes (`bg-slate-800/50` cards, `text-white`, `text-slate-200`, `text-emerald-400` / `text-rose-400`) with no light variant, so text lands at contrast ratios of 1.1–3.4:1. Notification History has 2 nodes: the active tab link (`text-cyan-400` on `#f1f5f9`) and the type-filter value (`text-white`). Notification Preferences has 3: the same tab link and two `text-white` section headings. `docs/frontend/design_system.md` (line 200) says light mode is not implemented and defines no light-mode tokens. ST-19's AC requires fixes to use existing tokens, so these could not be fixed in-story.

**Scope**
- Decide whether light mode is a supported theme (the Layout toggle exists). If it is, add light-mode colour tokens to `design_system.md`.
- Apply them to Reports (Monthly, Tax Year) and Notification Preferences and History, and remove the `color-contrast` entries from the light-theme `KNOWN_VIOLATIONS` baseline in `tests/e2e/accessibility-axe-scan.spec.js` in the same commit.

**Acceptance Criteria**
- [ ] The light-theme Reports and Notifications axe scans pass with no `color-contrast` baseline entry

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

### BLG-FE-201 — Settings helper text for the fixed strategy parameters contradicts §6 and §7.2
**Priority:** P3 (Low)
**Type:** Frontend / UX Copy
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Source:** ST-01/ST-02/ST-04 (EPIC-01, cycle `2026-10-06__release-v9.10`) — agent-mediated Product Owner review of the EPIC-01 PR — 2026-10-06
**Effort:** XS (<0.5 day)
**Provisional-Target:** TBD

**Problem**
The read-only Strategy Parameters on Settings keep their old helper text. The ST-01 decision record (§2.2) said to keep it, but the text is wrong:
- "Days before stop can trail": during grace there is no active stop.
- "e.g., 5 = Entry − 5×ATR": the losing stop is current price − 5×ATR, per §7.2 and the ST-03 contract correction.
- "e.g., 2 = High − 2×ATR": the code uses current price.
- The "e.g." framing no longer fits fixed values.

**Scope**
- Replace the four helper lines with §6/§7.2-accurate text. Update `settings.md` §1 and the Playwright text assertions.

**Acceptance Criteria**
- [ ] Each helper line matches `strategy_rules.md` §6/§7.2 wording; covered by Playwright (wording-only, FI-P3-02 may apply)

---

### BLG-FE-202 — Positions with no ATR available are never shown to the user
**Priority:** P3 (Low)
**Type:** Frontend / Backend / Transparency
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Source:** ST-01/ST-02/ST-04 (EPIC-01, cycle `2026-10-06__release-v9.10`) — agent-mediated Product Owner review of the EPIC-01 PR — 2026-10-06 (ST-02 AC 2 met only in the analyze response)
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
ST-02 keeps the stored stop when no ATR is available and sets `atr_unavailable: true`, but only on the `GET /positions/analyze` response. Nothing stores it, `GET /positions` does not return it, and no `src/` code reads it. When the nightly job hits the same case, it skips the position ("ATR unavailable") and raises no flag. The user cannot see that a position's stop is frozen for lack of ATR.

**Scope**
- Expose an ATR-unavailable indicator on `GET /positions`, stored or derived, and show it in the Positions stop cell (ties in with ST-06's provenance line).

**Acceptance Criteria**
- [ ] A position whose last recompute had no ATR shows a visible indicator on Positions (Playwright). Contract and OpenAPI updated in the same commit.

---

### BLG-BE-146 — Add an ATR preview so Trade Entry can show the stop, risk and size before save
**Priority:** P3 (Low)
**Type:** Backend / Frontend — Trade Entry
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; API Contracts & Documentation Owner
**Source:** Agent-mediated pre-PR review of EPIC-02 (Director of Quality + Product Owner roles), cycle `2026-10-06__release-v9.10`, finding on ST-07 (BLG-FE-197) — 2026-10-07
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
Since ST-07, Trade Entry shows only the stop the backend will store: entry − 5× ATR. When the ATR field is blank, the backend fetches ATR only at save. Until then the Initial Stop, Risk (to stop) and the Position Sizing widget all show "Calculated on save" or an empty state. A user who does not know the ticker's ATR can no longer size a position before submitting it. Previously they could type a stop. No endpoint exposes the `calculate_atr()` value that `add_position()` uses.

**Scope**
- A read-only endpoint (e.g. `GET /market/atr/{ticker}?market=`) returning the 14-day ATR from the same `calculate_atr()` path `add_position()` uses, with a `null` result when unavailable. Contract, `openapi.yaml`, `backend/routers/test.py` and SystemStatus count updated per CLAUDE.md §2.
- Trade Entry calls it once the ticker and market are known and the ATR field is blank, and uses the result for the system stop, risk and sizing preview, labelled as fetched. A typed ATR still takes precedence.

**Acceptance Criteria**
- With a ticker and entry price entered and ATR blank, Trade Entry shows a numeric system stop, risk and suggested shares before save (Playwright, mocked endpoint)
- The stop shown before save equals the `initial_stop` returned by `POST /portfolio/position` for the same inputs (backend test)
- When the endpoint returns no ATR, the existing "Calculated on save" states remain

---

### BLG-FE-203 — Show the currency unit on Trade Entry's ATR field and reject implausible typed ATRs
**Priority:** P3 (Low)
**Type:** Frontend / Backend Validation
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Source:** Agent-mediated pre-PR review of EPIC-02 (Director of Quality + Product Owner roles), cycle `2026-10-06__release-v9.10`, finding on ST-07 (BLG-FE-197) — 2026-10-07
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
The ATR field ("ATR (14-day)") shows no unit, while the backend treats a typed ATR as native currency (pounds for UK, dollars for US). Since ST-07 the typed ATR alone sets the stored initial stop. A UK user who types ATR in pence, the unit UK quotes are often read in, gets a stop 100× too far below entry. It is stored with `atr_source = user` and nothing checks it.

**Scope**
- Show the market's currency symbol on the ATR field label, as the old Stop Price field did (e.g. "ATR (14-day, £)").
- In `add_position()`, reject a typed ATR that is implausible relative to entry (e.g. ATR ≥ 20% of entry, or 5× ATR ≥ entry so the stop would be ≤ 0) with a clear 400 message. Trade Entry shows the same warning inline before submit.

**Acceptance Criteria**
- The ATR label shows £ for UK and $ for US (Playwright)
- A typed ATR whose 5× multiple meets or exceeds the entry price is rejected by the API with a 400 and an explanatory message (backend test)
- Trade Entry shows the warning inline and disables submit for that input (Playwright)

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

### BLG-OPS-181 — Find out why a staging-deploy.yml hook deploy of a governance-only main commit never went live
**Priority:** P3 (Low)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** Sprint Execution, ST-18 / EPIC-04, cycle `2026-10-06__release-v9.10` — 2026-10-07
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`staging-deploy.yml` run 37600608347 (`workflow_dispatch`, `main` at `1639c956`, a commit touching only `claude/`) got HTTP 200 and deploy `dep-db310hp42hec7387gh90` from the Render deploy hook. Staging stayed on `ef4088b4` for the whole 480s wait, and the job failed. A manual "Deploy latest commit" from the Render dashboard then went live on `1639c956`. The cause is unconfirmed: a dashboard-only Build Filter skipping hook deploys, a failed build, or a slow build. If hook deploys are silently skipped, `workflow_dispatch` of `staging-deploy.yml` can't be used to bring staging level with `main`.

**Scope**
- Check `dep-db310hp42hec7387gh90`'s final state and the staging backend's Settings → Build Filters in the Render dashboard.
- If a filter skips hook deploys, either document it in `docs/ops/staging_deploy_notes.md` or change the filter.

**Acceptance Criteria**
- The cause is recorded against this item
- If it is a filter: the staging deploy notes say whether a `workflow_dispatch` deploy of a non-code commit is expected to go live

**Notes**
- **Cause found (ST-29, EPIC-04, v9.12, 2026-10-15, Render dashboard read by the user, acting for the Infrastructure & Operations Owner; DEL-20261015-02):** not a Build Filter (none set) and not a failed build (none). Two configuration faults: (1) `RENDER_STAGING_DEPLOY_HOOK` holds the **staging frontend's** deploy hook, not the backend's. Today's hook call (07:39:19 UTC, `dep-db8869u89jmc73cjn4n0`) appears only as a frontend deploy at that second. `wait_for_staging_deploy_live.py` polls the **backend**, which the hook never deploys, so every `staging-deploy.yml` run has timed out since 2026-09-03 (last success run 33769711448). With Render auto-deploy off (correct for the hook approach), the staging backend moved only by manual deploy: `90099bec` went live on 2026-10-13 09:11 UTC from a manual deploy. (2) The staging frontend's branch was `exec/2026-09-09__release-v9.3/EPIC-02`, not `main`, so each hook deploy rebuilt that branch's tip, `76283f43` (2026-09-10). The user is resetting it to `main` (2026-10-15). `dep-db310hp42hec7387gh90` (this item's 2026-10-07 case) fits the same cause: a frontend deploy while the backend was watched. A `workflow_dispatch` deploy of a non-code commit is therefore not blocked by any filter; it failed for the same reason as every other run. Fix filed as BLG-OPS-189.

---

### BLG-OPS-182 — Live-fire the stale-staging check from main against a deliberate staging/main divergence
**Priority:** P3 (Low)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** Sprint Execution, ST-18 / EPIC-04, cycle `2026-10-06__release-v9.10` (agent-mediated Director of Quality review; ST-18 AC 1 narrowed) — 2026-10-07
**Effort:** XS (<1h)
**Provisional-Target:** v9.11
**Depends on:** EPIC-04 (v9.10) merged to `main`

**Problem**
ST-18's failing run (37598457966) was dispatched on the EPIC-04 branch: staging `ef4088b4` lacked the branch's deploy-path commit `d6644b25`. It proved the check and the Telegram alert fire on a real divergence, but not a deliberately introduced staging/`main` divergence as AC 1 worded it. The new comparison target in `scripts/staging_smoke_test.py` (latest staging-deploying commit, ancestor-aware) has not yet run from `main`'s copy of the workflow.

**Scope**
- After EPIC-04 merges, deliberately put staging behind `main` on a deploy-path commit (e.g. hold a code commit's deploy, or redeploy an older commit from the Render dashboard).
- Run `staging-smoke-test.yml` on `main`, then restore staging and run it again.

**Acceptance Criteria**
- A failing `main` run URL showing `STALE STAGING DEPLOY` for the deliberate divergence, with the Telegram alert received
- A passing `main` run URL after staging is restored

---

### BLG-OPS-183 — Make the daily AI cost alert count Claude calls, not only Gemini calls
**Priority:** P2 (Medium)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** Sprint Execution, ST-25 / EPIC-04, cycle `2026-10-08__release-v9.11` (agent-mediated Cybersecurity & Trust Lead review of the ST-25 AI endpoint security checklist) — 2026-10-09
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.12

**Problem**
`POST /ai/check-daily-cost` → `check_and_alert_daily_cost()` → `database.get_daily_ai_cost()` sums `estimated_cost_usd` from `gemini_audit_log` only. `gemini_audit_log` is written only by `gemini_service._log_audit`, for plan and thesis generation. Every Claude-calling feature (daily briefing, chat, journal summary, post-trade debrief, and ST-25's monthly P&L narrative) logs to `claude_audit_log`, so its spend is never counted, and the $1.00 `AI_DAILY_COST_THRESHOLD` alert can never fire for it. `docs/ops/ai_monthly_pnl_narrative_cost_estimate_2026-10-08.md` (ST-23) relies on this alert ("fires well before this"), as did the first draft of ST-25's security checklist. The per-endpoint anomaly check (`check-endpoint-anomalies`, reading `claude_audit_log`) and `GET /ai/monthly-cost-by-feature` do cover Claude spend.

**Scope**
- Make `get_daily_ai_cost()` sum today's `claude_audit_log.cost_usd` only, and alert on that. `gemini_service._log_audit` writes both tables on every plan and thesis call, so summing both would count those calls twice; `claude_audit_log` already holds every call.
- Confirm which scheduler calls `POST /ai/check-daily-cost` and that it runs.
- Add a correction note to the ST-23 cost estimate's runaway row.

**Acceptance Criteria**
- A pytest showing a `claude_audit_log` row counted in the daily total, a plan-generation call counted once, and the alert firing when Claude spend passes the threshold
- The scheduler that calls `POST /ai/check-daily-cost` named in `ai_endpoints.md`, with its last successful run recorded
- The ST-23 cost estimate notes the corrected coverage

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

### BLG-FE-207 — Grace Period panel: link each row to its position, and align text and date format with the spec
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design; Product Owner
**Source:** Idea intake `IW-20261008-01` — consolidates `IDEA-product-owner-20261008-02` and `IDEA-head-of-ux-20261008-02` (same component, `GracePeriodPanel.js`); roadmap rebalance `2026-10-08__scheduled` STEP 4 (Backlog, ungated)
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
The Risk Dashboard's Grace Period panel (`src/components/risk/GracePeriodPanel.js`) lists grace positions with no route to the position, where notes, thesis and exit detail live. Its text has also drifted from `risk_dashboard.md` §5.2: the heading is "Grace Period" (spec: "Grace Period Positions"), the badge reads "N positions" (spec: "N positions in grace period"), and entry dates render `dd MMM yy` (spec: DD MMM YYYY).

**Scope**
- Make each grace row a link to the Positions page for that position.
- Align the heading, badge text and entry-date format with §5.2, or amend §5.2 if the Product Owner prefers the shipped text.

**Acceptance Criteria**
- [ ] Playwright: clicking a grace row opens the Positions page showing that position
- [ ] Heading, badge and date format match `risk_dashboard.md` §5.2 (wording-only ACs may be code-reviewed per FI-P3-02)

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

### BLG-BE-159 — Trail Stop "apply" calls an endpoint that does not exist, and add-position ignores a supplied stop
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Correctness
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Source:** ST-30 (BLG-SPEC-173), EPIC-05, cycle `2026-10-08__release-v9.11` — found while tracing which code path writes each `positions` field — 2026-10-08
**Effort:** S (~0.5-1d)
**Provisional-Target:** TBD

**Problem**
1. The Positions page's Trail Stop modal applies a recommended stop with `PATCH /positions/{id}` and body `{stop_price}` (`src/pages/Positions.js`, `updateStopMutation`). No such route exists: the backend has only `PATCH /positions/{id}/note`, `/tags` and `/mark-reviewed`, and no contract or `openapi.yaml` entry documents it. Every apply therefore fails and shows "Failed to update stop". `GET /positions/{id}/stop-trail` and the trail-stop recommendation log assume the user can act on the recommendation.
2. `POST /portfolio/position` accepts `stop_price` (`AddPositionRequest`), and `add_position()`'s docstring says it is used "if provided", but the code always stores `entry − 5 × ATR` as `initial_stop`, so a supplied stop is silently dropped.

**Scope**
- Decide (Strategy Rules & System Intent Owner) whether a user may set or raise a stop manually, given `strategy_rules.md` §7.3's ratchet. Then either add the route (contract, `openapi.yaml`, `routers/test.py`, ratchet-only validation) or remove the apply action from the modal.
- Either honour `stop_price` at entry (with validation) or remove it from the request model and docstring

**Acceptance Criteria**
- The Trail Stop modal's action succeeds against a real route, or the action is gone; a Playwright test covers whichever ships
- A supplied entry stop is either stored or rejected with a clear error, never silently ignored

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

### BLG-FE-210 — White text on amber-600 badges fails WCAG contrast outside Replay
**Priority:** P3 (Low)
**Type:** Frontend / Accessibility
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-37 (BLG-QA-196), EPIC-06, cycle `2026-10-08__release-v9.11` — out-of-scope finding while fixing the Replay Risk-Off badge — 2026-10-08
**Effort:** XS (<1h plus test updates)
**Provisional-Target:** TBD

**Problem**
White 12px bold text on `bg-amber-600` measures 3.18:1 (axe `color-contrast`, serious; 4.5:1 needed). ST-37 fixed the Replay page's Risk-Off badge by moving it to `bg-amber-700` (the `BLG-FE-165` precedent). The same class pair remains in pages the axe scan does not cover: `StrategyBenchmark.js` (Risk-Off badges, lines 26–27), `AiChatWidget.js` (line 70) and `AiDailyBriefing.js` (`MONITOR` action, line 14).

**Scope**
- Move those badges to `bg-amber-700` (or the design-system token for an amber badge with white text)
- Update any Playwright assertion that names `bg-amber-600` for them

**Acceptance Criteria**
- No `bg-amber-600 text-white` pair remains in `src/`
- The affected specs pass; an axe scan of each changed component reports no `color-contrast` finding on the badge

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

### BLG-BE-157 — Batch signal sizing gives a zero-ATR signal a 5% allocation
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Correctness
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Source:** ST-39 (BLG-QA-199), EPIC-06, cycle `2026-10-08__release-v9.11` — found while writing mutation-testing cases for `size_batch_inv_vol` — 2026-10-08
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`sizing_service.size_batch_inv_vol()` (used by `signal_service.py` for every new signal's suggested shares) gives a signal with `atr_value` 0 or missing an inverse-ATR weight of 0, then clamps every weight to the 5% minimum, so that signal still receives 5% of available cash (before renormalisation) and a non-zero share count. Its own docstring says "Signals with atr_value == 0 get 0 shares". Reproduced 2026-10-08: signals with ATR 1, 0 and 2 and £10,000 cash gave the zero-ATR signal a weight of 0.111 and 22 shares. `tests/test_signal_sizing.py::test_zero_atr_produces_zero_shares` passes only because it uses a batch where every ATR is 0, which takes the early-exit branch; the mixed case is untested.

**Scope**
- Exclude zero/missing-ATR signals from the clamp and renormalisation, and give them 0 shares with a reason
- Add a mixed-batch test (some zero-ATR, some valid)

**Acceptance Criteria**
- In a mixed batch, a zero-ATR signal gets `suggested_shares` 0, `inv_vol_weight` 0 and a reason, and the other signals' weights sum to 1.0
- The existing all-zero and capping tests still pass

---

### BLG-BE-158 — Batch signal sizing never adds entry fees to total cost
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Correctness
**Owner:** Head of Engineering; Financial Reporting & Records Owner
**Source:** ST-39 (BLG-QA-199), EPIC-06, cycle `2026-10-08__release-v9.11` — found while writing mutation-testing cases for `size_batch_inv_vol` — 2026-10-08
**Effort:** XS (<1h plus tests)
**Provisional-Target:** TBD

**Problem**
`sizing_service.size_batch_inv_vol()` reads the fee as `calculate_uk_entry_fees(...).get('total_fee', 0)` (and the same for US), but both fee functions return the key `total`, not `total_fee`. The fee is therefore always 0, and every signal's `total_cost` is the gross cost only: no stamp duty or commission for UK, no FX fee for US. Reproduced 2026-10-08: a UK signal of 44 shares at £100 showed `total_cost` 4,400.00 with no fees. Signal costs on the Signals page are understated, and cash checks based on them are optimistic. Note also that `gross_cost` uses `current_price` (native) for US signals while `allocation_gbp` is GBP; confirm the intended currency when fixing.

**Scope**
- Read the fee functions' `total` key, and confirm the currency basis of `gross_cost` / `total_cost` for US signals
- Add tests asserting UK and US fees are included

**Acceptance Criteria**
- A UK batch signal's `total_cost` equals gross cost plus stamp duty and commission; a US signal's includes the FX fee in the documented currency
- `signal_endpoints.md` states the currency of `total_cost`

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

### BLG-BE-160 — Rounding the stored stop to 2 dp can lower it, breaching the §7.3 ratchet
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Source:** ST-16 (BLG-BE-143), EPIC-03, cycle `2026-10-08__release-v9.11` — raised in the Strategy Rules & System Intent Owner's ruling on `ESC-EXEC-20261008-01` (2026-10-09)
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
`add_position()` stores `initial_stop` and `current_stop` unrounded in `DECIMAL(10,4)` columns. The post-grace stop writes, `analyze_positions()` (`'current_stop': round(trailing_stop_native, 2)`) and `run_nightly_trailing_stop_update()` (`round(new_stop_native, 2)`), round to 2 dp after the `max()`. When `calculate_trailing_stop` keeps the stored stop (no rise), rounding can lower it by up to 0.005. `strategy_rules.md` §7.3 says stops "must never move downwards" and that the rule is absolute. ST-16 removed the in-grace write, so this now affects only positions past grace.

**Scope**
- Write the stop at the column's own precision (4 dp), or round only a genuinely new stop and never round below the stored value

**Acceptance Criteria**
- A test with a 4-dp stored stop that the recompute keeps shows the written value is never below the stored one, on both the on-load and nightly paths

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

### BLG-BE-162 — Journal summary rejects every request: trade_ids typed as integers but trade IDs are UUIDs
**Priority:** P1 (High)
**Type:** Backend Engineering / Correctness
**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer
**Source:** ST-02 staging run (EPIC-01, cycle `2026-10-08__release-v9.11`), staging at `82633f5` — 2026-10-09
**Effort:** S (~0.5d)
**Provisional-Target:** v9.12

**Problem**
`POST /ai/journal-summary` declares `trade_ids: list[int]` (`backend/routers/ai.py`), but `trade_history.id` is a UUID, so every request from Trade History fails with HTTP 422 `int_parsing` before reaching the AI. The int assumption also runs through `fetch_journal_notes()` and the `ai_audit_log.trade_ids INTEGER[]` column, and `ai_endpoints.md` documents "array of integers". The Playwright spec (`trade-history-ai-journal-summary.spec.js`) mocks the API, so CI never exercised the real request shape.

**Scope**
- Type `trade_ids` as UUID strings in the request model, `fetch_journal_notes()` and `log_ai_run()`
- Migrate `ai_audit_log.trade_ids` from `INTEGER[]` to `UUID[]` via the existing `ensure_*()` pattern, and record the migration in `data_model.md`
- Update `ai_endpoints.md` and `openapi.yaml` to "array of string (UUID)"
- Add a backend test that posts real UUID trade IDs, and check the `GET /ai/journal-summary/history?trade_id=` filter

**Acceptance Criteria**
- A journal summary requested from Trade History on staging returns generated content
- The run is written to `ai_audit_log` with the UUID trade IDs
- A backend test posting UUID `trade_ids` passes; integer IDs are rejected with 422

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

### BLG-AI-10 — Check that briefing and chat responses citing a stop include its recalculation time
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** EPIC-01 DoQ consolidation (ST-08, BLG-BE-141), cycle `2026-10-08__release-v9.11` — 2026-10-12
**Effort:** S (~0.5d)
**Provisional-Target:** v9.12

**Problem**
ST-08 puts `stop_calculated_at` in the briefing and chat context and tells the model to state it whenever it cites a stop, but nothing checks the response: a reply quoting a stop without its recalculation time is returned as-is. The AC asked for responses to include the time; only the prompt side is enforced.

**Scope**
- Add a post-generation check (like the debrief numeric check) that flags a briefing/chat response citing a stop price without a recalculation time
- Decide the action on failure (append the time from context, or log and count it), with AI Compliance & Governance Officer sign-off
- Add the check to the boundary-sample audit so sampled outputs are scored on it

**Acceptance Criteria**
- A fixture response citing a stop without its time is caught; one with the time passes
- The chosen failure action is applied and tested for both briefing and chat

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

### BLG-AI-11 — Daily briefing can recommend ENTER for a ticker that does not exist
**Priority:** P2 (Medium)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** ST-02 staging run (2026-10-09) and PR #1968 agent-mediated review (EPIC-01, cycle `2026-10-08__release-v9.11`) — Product Owner note 3 — 2026-10-12
**Effort:** S (~0.5d)
**Provisional-Target:** v9.12

**Problem**
On staging, with only held tickers among the top signals, the daily briefing returned an ENTER action for the placeholder ticker `NEW_SIGNAL`. Nothing in the prompt forbids invented tickers and nothing checks the returned actions against the signals the model was given. An advisory feature recommending a ticker that does not exist undermines trust.

**Scope**
- Validate each returned action's ticker against held positions and the provided signals; drop or relabel any that match neither, and log it
- Tell the prompt that actions may only name tickers from the context, and bump `BRIEFING_PROMPT_VERSION`

**Acceptance Criteria**
- A fixture briefing response with an ENTER for an unknown ticker is not returned as an action, and the drop is logged
- Golden-fixture tests pass with the recorded prompt-version bump

---

### BLG-AI-12 — Daily briefing reads starting cash as a target cash level
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** ST-02 staging run (2026-10-09) and PR #1968 agent-mediated review (EPIC-01, cycle `2026-10-08__release-v9.11`) — Product Owner note 3 — 2026-10-12
**Effort:** XS (<1h plus tests)
**Provisional-Target:** v9.12

**Problem**
The briefing context renders cash as "cash £X of £{initial_cash}". On staging `initial_cash` is 0, and the model reported "£15,006 against a £0 target cash level", treating starting capital as a target. The wording invites that reading whatever the value.

**Scope**
- Label the figures explicitly (e.g. "available cash £X; starting capital £Y"), and omit starting capital when it is 0 or missing
- Bump `BRIEFING_PROMPT_VERSION` and update the golden fixture

**Acceptance Criteria**
- The briefing context no longer uses "of £{initial_cash}", and omits starting capital when it is 0
- Golden-fixture tests pass with the recorded prompt-version bump

---

### BLG-AI-13 — Monthly P&L narrative: widen the instrument-directive scan to inflected and indirect wording
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Sprint Execution, ST-25 / EPIC-04, cycle `2026-10-08__release-v9.11` (agent-mediated AI Compliance & Governance Officer review of the new narrative endpoint) — 2026-10-12
**Effort:** XS (<1h plus tests)
**Provisional-Target:** v9.12

**Problem**
`_INSTRUMENT_DIRECTIVE_RE` in `backend/services/monthly_pnl_narrative_service.py` matches only base verb forms followed directly by a pronoun or an upper-case ticker. Inflected or indirect wording passes the D4 scan: "Consider buying MSFT" and "sell the position" both return no finding. Risk is low because the narrative's inputs carry no tickers (§13 Condition 2) and the prescriptive scan still runs, but a model-invented ticker would be caught only if its wording matched.

**Scope**
- Extend the pattern to inflected forms (buying/selling/shorting, "consider/should buy", "sell the position/holding") without false positives on past-tense reporting ("you sold 9 trades")
- Add B-MPN-04 cases for the new forms and negative cases for past-tense reporting

**Acceptance Criteria**
- "Consider buying MSFT" and "sell the position" are reported as `instrument_directive`
- The representative output and the code-written fallback still scan clean
- `tests/test_monthly_pnl_narrative.py` passes

---

### BLG-OPS-184 — Stop the post-grace stop-health monitor alerting on the morning a position's grace ends
**Priority:** P2 (Medium)
**Type:** Operations / Monitoring
**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Source:** PR #1970 agent-mediated review (EPIC-03, cycle `2026-10-08__release-v9.11`), Director of Quality finding 1: ST-18 × ST-16 interaction — 2026-10-12
**Effort:** S (~0.5d)
**Provisional-Target:** v9.12

**Problem**
ST-16 stops the nightly job (and the on-load path) stamping `active_atr_multiplier` while a position is in grace. The first post-grace stamp happens only at the next nightly run (22:30 UTC, weekdays) or an on-load `/positions/analyze` call, and after ST-19 no frontend screen calls `/positions/analyze`. ST-18's `scripts/check_post_grace_stop_health.py` runs at 07:30 UTC on weekdays and after every deploy, and flags any post-grace position whose `active_atr_multiplier` is null. So every position raises a false Telegram alert on the first check after its day 10: the same morning on a weekday, or Monday morning when day 10 falls on a weekend. Repeated false alerts teach the user to ignore the monitor.

**Scope**
- Choose one fix and record it in the script docstring: (a) the monitor treats a null multiplier as pending, not a violation, while `stop_calculated_at` is null and the position is no more than 3 calendar days past grace (covers weekends and one missed nightly); or (b) stamp the multiplier at the grace boundary, e.g. the nightly job processes positions with `holding_days == GRACE_PERIOD_DAYS - 1` so that the stop is in place at day 10. Option (b) changes live stop behaviour and needs a Strategy Rules & System Intent Owner ruling first
- Add a fixture for a position on day 10 with a null multiplier and no `stop_calculated_at`

**Acceptance Criteria**
- `tests/test_post_grace_stop_health.py` passes the new day-10 fixture and still fails `non_s11_multiplier.json` and `missing_stop.json`
- A post-grace position whose multiplier stays null beyond the tolerance window is still reported as a violation (test)

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

### BLG-OPS-185 — Add requirements-dev.txt to the local backend setup instructions
**Priority:** P3 (Low)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** PR #1971 review (EPIC-06, ST-43 / BLG-OPS-178), v9.11 — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** v9.12

**Problem**
ST-43 moved `pytest`, `pytest-cov` and `hypothesis` out of `backend/requirements.txt` into `backend/requirements-dev.txt` and updated every CI test workflow, but the local setup instructions were not updated. `README.md`'s backend setup still runs only `.venv/bin/pip install -r requirements.txt`, so a fresh venv built from it cannot run the CLAUDE.md §9 command `backend/.venv/bin/python3 -m pytest` (No module named pytest). Existing venvs still have pytest installed, which hides the gap. `docs/ops/quarterly_dependency_upgrade_cadence_policy.md`'s verification step has the same stale install command.

**Scope**
- `README.md` backend setup: install `-r requirements.txt -r requirements-dev.txt`
- `docs/ops/quarterly_dependency_upgrade_cadence_policy.md` verification step: same change
- Mention `requirements-dev.txt` in CLAUDE.md §9's description of the venv, if the Head of Specs Team agrees (governance file)

**Acceptance Criteria**
- Following `README.md` from a fresh clone yields a venv in which `backend/.venv/bin/python3 -m pytest --collect-only -q` succeeds
- `grep -rn "pip install -r .*requirements.txt" README.md docs/ops/quarterly_dependency_upgrade_cadence_policy.md` shows `requirements-dev.txt` alongside every test-running install

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

### BLG-GOV-385 — Check backlog item integrity after every cross-EPIC merge resolution
**Priority:** P2 (Medium)
**Type:** Governance Process / Tooling
**Owner:** PMO Lead; Head of Specs Team
**Source:** EPIC-05, cycle `2026-10-08__release-v9.11` — PR #1973 agent-mediated review — 2026-10-12
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
The CLAUDE.md §8 merge of `main` (EPIC-06, PR #1971) into EPIC-05 (`3237cb5e`) reported no conflict on `backlog.md` but spliced two items: BLG-SPEC-190's header kept only its first 5 metadata lines, and its Problem/Scope/AC landed inside BLG-BE-157, which then carried two bodies. Both items end with the same `**Effort:** S (~0.5d)` / `**Provisional-Target:** TBD` lines, so git's line merge treated them as shared context. Merging PR #1973 unrepaired would have put the corrupted P2 item on `main`. No step in §8 or STEP 4 step 3c checks item structure after a clean auto-merge.

**Scope**
- Add `scripts/check_backlog_item_integrity.py`: every `### BLG-…` item has exactly one `**Problem**`, `**Scope**` and `**Acceptance Criteria**` block and the required metadata fields, and no ID repeats
- Run it in CI on PRs touching `backlog.md`, and add it to CLAUDE.md §8 step 2b (or a new step) as a mandatory post-merge check
- Optionally compare each item's text against both merge parents and flag any item that matches neither

**Acceptance Criteria**
- The script fails on `3237cb5e`'s `backlog.md` and passes on the repaired file
- The check is wired into CI and named in CLAUDE.md §8

---

### BLG-GOV-386 — Report gated items whose gating backlog item has shipped, and read that list in Release Planning §1.3a
**Priority:** P2 (Medium)
**Type:** Governance Tooling
**Owner:** Head of Specs Team; Head of Engineering
**Source:** Post-ship closure `2026-10-08__release-v9.11`, closure_record.md §6 row 7 (v9.11 Release Planning Friction Item 1) — 2026-10-12
**Effort:** S (~0.5–1d)
**Provisional-Target:** v9.12

**Problem**
`scripts/scan_backlog_gate_conditions.py` reports date-lapsed gates and resolution banners, but a gate whose condition is "`BLG-X` shipped/complete" stays gated after `BLG-X` ships, because nothing re-reads it. At v9.11 Release Planning a manual check found 26 gated items whose gate names only items no longer in the active backlog. `BLG-OPS-179` was genuinely ready and `BLG-FE-195` had already been delivered. Ready work is silently excluded from the ungated pool.

**Scope**
- Add a "gating item shipped — verify" output list to `scan_backlog_gate_conditions.py`: gated items whose `Gate criteria` names one or more `BLG-*` IDs, all of which are absent from the active `backlog.md` (archived or bannered ✅ COMPLETE). Mirror the format of the date-lapsed list.
- Add unit tests covering: all named items shipped (listed), one still open (not listed), no `BLG-*` reference (not listed).
- Update `release_planning_prompt.md` §1.3a so the new list is read in the same read-before-fixing-the-pool step as the date-lapsed list (CLAUDE.md §6 checklist applies).

**Acceptance Criteria**
- Running the script against a fixture where a gate names only an archived item lists that item under the new heading.
- An item whose gate names at least one still-active item is not listed.
- `release_planning_prompt.md` §1.3a names the new list, with the version bump, OPERATIONAL_GUIDE.md §14 and `prompt_change_log.md` updates in the same commit.

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
