# Product Backlog — Momentum Trading Assistant

<!-- last-spec-debt-deep-review: 2026-10-16__release-v9.13 -->

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-11-05 (Sprint Execution `2026-11-03__release-v9.15` EPIC-04 and PR #2192 review — 7 new items added: BLG-AI-27 to BLG-AI-33); prior — 2026-11-05 (PR #2191 agent-mediated Director of Quality / Product Owner review — 2 new items added: BLG-FE-273, BLG-FE-274); prior — 2026-11-05 (Sprint Execution `2026-11-03__release-v9.15` EPIC-02 — 4 new items added: BLG-BE-205, BLG-GOV-409, BLG-SPEC-220, BLG-QA-246); prior history retained — see prior entries in version control
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
**Gate criteria:** Arc 4 PO-02 (Journal Pattern Recognition) data model established. PO-02 is itself preconditioned on 6+ months of AI-summarised journal data; it clears when PO-02's data model is recorded, which requires PO-02 to enter sprint planning (Later horizon, `current_roadmap.md` §5).
**Gate note (2026-10-29):** (Release Planning `2026-10-29__release-v9.14`, §1.3a date-lapsed disposition, within the ESC-CLOSE-20261007-01 bounds) Re-gated (b) on the same condition. The embedded date (~2026-10-20) projected when PO-02's 6-month data precondition would be met; it was never this gate's clearance date, so the scan reported a false-positive lapse. The condition is not met: PO-02 has not entered sprint planning (0 active roadmap initiatives) and no PO-02 data model is recorded. No AC names the gate's date (AC 2 names the PO-02 data model and is unchanged).

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
`moment` is deprecated and is used in two places only, both in `src/pages/SystemStatus.js` (`format('HH:mm, D MMM YYYY')` and `fromNow()`). `date-fns` 4.4.0 is already a dependency used in 19 files. GHSA-4p3w-j4w9-5jqw (moment below 2.31.0, server-side only) does not affect this browser use, and the lockfile already has 2.31.0.

**Scope**
- Replace the two calls with `format(date, 'HH:mm, d MMM yyyy')` and `formatDistanceToNow(date, { addSuffix: true })`
- Remove `moment` from `package.json` and the lockfile

**Acceptance Criteria**
- `moment` no longer appears in `src/` or `package.json`
- A Playwright test checks the "As of" time format and the health-check relative time on System Status, and passes in CI

---

### BLG-TECH-32 — Retire the per-call-site Alpaca call logging now that every Alpaca call is attributed
**Priority:** P3 (Low)
**Type:** Tech Debt / Observability
**Owner:** Head of Engineering; FinOps & Resource Architect
**Source:** PR #2075 review (EPIC-05, cycle `2026-10-16__release-v9.13`, ST-29/ST-31) — 2026-10-28
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
Since v9.13 every Alpaca bar call writes two `api_call_log` rows: `service = 'alpaca'` from `alpaca_service._log_alpaca_call()` (one database connection per call, `external_api_dependency_register.md` SFM-01) and `service = 'alpaca_data'` from the transport-level attribution (`utils/api_attribution.py`, batched). The reports keep them apart by service name, but the table grows twice as fast for Alpaca and any total over `api_call_log` double-counts.

**Scope**
- Point `GET /ops/alpaca-call-report` at the attributed rows (`alpaca_data`), keeping its response shape
- Remove `_log_alpaca_call()` and its call sites
- Update `ops_endpoints.md` and `api_changelog.md`; note the cut-over date so earlier `alpaca` rows stay readable

**Acceptance Criteria**
- One Alpaca bar call writes exactly one `api_call_log` row (test)
- `GET /ops/alpaca-call-report` returns the same fields, counted from `alpaca_data` (test)

---

### BLG-TECH-33 — Make the ESLint 9 flat config load an ESLint-9-compatible react-hooks plugin
**Priority:** P3 (Low)
**Type:** Platform / Tooling
**Owner:** Head of Engineering
**Source:** Sprint execution `2026-10-29__release-v9.14`, ST-01 (BLG-OPS-193), EPIC-01 — 2026-10-29
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15

**Problem**
`eslint.config.mjs` (ESLint 9 flat config, the lint path for files Claude writes) imports `eslint-plugin-react-hooks`. Before ST-01 there was no top-level install, so the flat config could not load at all. ST-01's lockfile fix hoists `eslint-config-react-app`'s dependency `eslint-plugin-react-hooks@4.6.2`, which is not ESLint-9 compatible: `npx eslint src/pages/TradePlan.js` fails with `TypeError: context.getSource is not a function` in `react-hooks/exhaustive-deps`. No CI workflow runs the flat config, so nothing fails, but the lint path is broken.

**Scope**
- Add an ESLint-9-compatible `eslint-plugin-react-hooks` (v5 or later) as an explicit devDependency, and check `react-scripts`' build still resolves its own v4 through `eslint-config-react-app`
- Or remove the react-hooks rules from the flat config, with Product Owner sign-off (protected file)

**Acceptance Criteria**
- `npx eslint src/pages/TradePlan.js` runs without a crash
- `CI=false npm run build` (the Frontend Production Build workflow) still passes

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
**Gate note (2026-11-03):** (Release Planning `2026-11-03__release-v9.15`, §1.3a date-lapsed disposition (a), within the ESC-CLOSE-20261007-01 bounds; also on the "gating item shipped" list, so cleared once under the date-lapsed disposition) Gate cleared. The removed gate read "No earlier than 2026-11-01 (~6 months after BLG-OPS-36 scope review in v4.2, 2026-05-28)". Its whole condition is met: the gating item `BLG-OPS-36` shipped in v4.2 (2026-05-28, archived), and the gate's only other limb is the calendar date itself, now passed (scan as-of 2026-11-03). No AC names the gate's date or gating item.

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
**Gate criteria:** Arc 4 PO-02 (Journal Pattern Recognition) design phase begins. PO-02 is itself preconditioned on 6+ months of AI-summarised journal data; it clears when PO-02 enters sprint planning (Later horizon, `current_roadmap.md` §5).
**Gate note (2026-10-29):** (Release Planning `2026-10-29__release-v9.14`, §1.3a date-lapsed disposition, within the ESC-CLOSE-20261007-01 bounds) Re-gated (b) on the same condition. The embedded date (~2026-10-20) projected when PO-02's 6-month data precondition would be met; it was never this gate's clearance date, so the scan reported a false-positive lapse. The condition is not met: PO-02's design phase has not begun (0 active roadmap initiatives). The AC names the PO-02 design phase start, not the date, and is unchanged.

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

**Cross-reference (sprint close, added 2026-11-02):** ST-23/EPIC-03, cycle `2026-10-29__release-v9.14` — `ESC-EXEC-20260910-01` re-acknowledged and re-deferred by the AI Compliance & Governance Officer on 2026-10-30 (addendum in `docs/ops/ai_output_boundary_sample_audit_20260910.md`, `109728bf`). The live production sample is carried post-sprint in `DEL-20261030-04` and tracked by `BLG-GOV-399`.

**Problem**
AI output (thesis generation, chat, daily briefing) has no recurring compliance sampling — only ad hoc review during feature work. As prompts and models evolve over time, outputs could drift from §13's determinism/no-prediction boundary without a scheduled check to catch it.

**Scope**
- Sample 10 random AI outputs per quarter; check against §13.2 boundary language (no autonomous-sounding directives, advisory framing preserved) and for determinism/no-prediction drift as prompts/models evolve

**Acceptance Criteria**
- First quarterly sample conducted and findings (if any) filed as backlog items

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

### BLG-GOV-361 — BLG-SPEC-65 still carries a stale sixth copy of the AI adoption window gate text
**✅ COMPLETE — 2026-10-08 — Release Planning `2026-10-08__release-v9.11` §1.3a — `BLG-SPEC-65`'s gate now carries an explicit disposition (adoption-window limb met, 2026-10-08 gate note); no backlog item restates the AI adoption window gate or cites 2026-07-25; banner added 2026-11-03 by the Head of Specs Team with the Data Model & Domain Schema Owner (agent-mediated per §5.3, user-directed 2026-11-03; closure_record.md `2026-10-29__release-v9.14` §6 row 7)**
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

### BLG-FE-195 — Settings › Strategy Parameters: §11 defaults, §7.2-correct helper text, governed-parameter treatment
**✅ COMPLETE — 2026-10-15 (v9.12 ship) — met by sibling items, cycles `2026-10-06__release-v9.10` (`BLG-BE-138`/ST-01, ruling (a): fixed §11 values shown read-only) and `2026-10-12__release-v9.12` (`BLG-FE-201`/ST-20, §5–§7.2 helper text) — Playwright `tests/e2e/settings-strategy-parameters-fixed.spec.js` SC-SPF-01/02/06; constants parity `tests/test_strategy_parameter_parity.py`; banner added 2026-11-03 by the Base44 Frontend Prompt Owner with the Head of UX & Design and QA Lead (agent-mediated per §5.3, user-directed 2026-11-03; closure_record.md `2026-10-29__release-v9.14` §6 row 7)**
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

### BLG-GOV-374 — Structured ready-pool history written by Release Planning, read by roadmap STEP 7.3
**✅ COMPLETE — 2026-10-16 — roadmap rebalance `2026-10-16__scheduled` STEP -1.5 action-now patches — `claude/roadmap/ready_pool_history.md` (backfilled v9.3 onward), `roadmap_prompt.md` v9.35 STEP 7.3 reads it, `release_planning_prompt.md` v2.65 §1.4c appends to it; the appendix now leaves Appendix F to its owner (AC 2); banner added 2026-11-03 by the PMO Lead with the Head of Specs Team (agent-mediated per §5.3, user-directed 2026-11-03; closure_record.md `2026-10-29__release-v9.14` §6 row 7)**
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

### BLG-QA-220 — Behavioural tests for live holding days in the compliance and AI briefing readers
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** PR #1969 agent-mediated Director of Quality review (EPIC-02, cycle `2026-10-08__release-v9.11`) — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.12, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
> PO re-deferral 2026-11-03: missed v9.12, v9.13 and v9.14; re-deferred to v9.15 on the user's direction (resets the STEP 3.5 deferral count).

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.12, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
> PO re-deferral 2026-11-03: missed v9.12, v9.13 and v9.14; re-deferred to v9.15 on the user's direction (resets the STEP 3.5 deferral count).

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

### BLG-BE-170 — Price-alert duplicate fallback returns 500 when the threshold has more than 4 decimal places
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Source:** PR #1970 agent-mediated review (EPIC-03, cycle `2026-10-08__release-v9.11`), Director of Quality finding 2: ST-20 (DS-28) — 2026-10-12
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.12, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
> PO re-deferral 2026-11-03: missed v9.12, v9.13 and v9.14; re-deferred to v9.15 on the user's direction (resets the STEP 3.5 deferral count).

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.12, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
> PO re-deferral 2026-11-03: missed v9.12, v9.13 and v9.14; re-deferred to v9.15 on the user's direction (resets the STEP 3.5 deferral count).

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

### BLG-BE-172 — Show the code-written fallback when the monthly P&L summary's regeneration call fails
**Priority:** P3 (Low)
**Type:** Backend Engineering / AI Feature Resilience
**Owner:** Head of Engineering; Financial Reporting & Records Owner
**Source:** PR #1972 agent-mediated review (EPIC-04, cycle `2026-10-08__release-v9.11`), Product Owner finding: ST-25 — 2026-10-12
**Effort:** XS (<1h)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.12, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
> PO re-deferral 2026-11-03: missed v9.12, v9.13 and v9.14; re-deferred to v9.15 on the user's direction (resets the STEP 3.5 deferral count).

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

### BLG-SPEC-195 — Journal summary: remove the stale AI_MODEL override line, or cost the model actually used
**Priority:** P4 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner; Backend Engineering Patterns Owner
**Source:** Agent-mediated Director of Quality review (second pass) of EPIC-01, ST-06, cycle `2026-10-12__release-v9.12` — 2026-10-13
**Effort:** XS (<1h)
**Provisional-Target:** TBD (re-targeted from v9.13 by the PMO Lead 2026-10-29: v9.13 shipped without it; `ESC-CLOSE-20260923-01`, closure_record.md §6 row 5)

**Problem**
`ai_endpoints.md` §POST /ai/journal-summary says "Default model: `claude-haiku-4-5-20251001`. Override via `AI_MODEL` env var." No such override exists: `summarise_journal_notes()` uses `MODEL_VERSION = CLAUDE_HAIKU_4_5`, and the router never passes a model. ST-06 (v9.12) added `claude_audit_log` cost logging for the journal summary at Haiku 4.5 rates regardless of the `model` argument. That is correct today, but the costing would be wrong if an override were ever added.

**Scope**
- Remove the `AI_MODEL` override sentence from the contract (or implement the override and cost by model)
- If a non-Haiku model can ever be passed, select the cost rates by model in `_audit_journal_summary_call()`

**Acceptance Criteria**
- The contract describes only model selection that exists in code
- A test pins the cost rates to the model used, or the contract states the endpoint is Haiku-only

---

### BLG-AI-23 — Review logged briefing ticker-caveat tokens for further non-tickers
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** ST-16 (EPIC-03, cycle `2026-10-29__release-v9.14`, BLG-AI-21 second Scope bullet; ST-16 AC 4 — the live-log review was not granted in-sprint, so it is filed) — 2026-10-30
**Effort:** XS (<1h plus tests)
**Provisional-Target:** TBD

**Problem**
ST-16 added 22 indicator, earnings, macro and exchange acronyms to `_NON_TICKER_WORDS`. Other non-ticker words may still get the "(Note: X is not one of your open positions or today's top signals.)" caveat, which confuses the user and inflates the `ticker_outside_context_appended` count the ruling uses to judge the check. The `ticker check: ... action=caveat_appended` warning lines record which tokens fired; reading them needs a live log or database read, which needs the user's permission.

**Scope**
- With the user's permission, list the tokens caveated since 2026-10-30 with their counts
- Classify each as ticker or non-ticker
- Add the non-tickers to `_NON_TICKER_WORDS` (ruling `ESC-EXEC-20261027-02` (B) condition 2 is a minimum list)

**Acceptance Criteria**
- The token list with counts is recorded
- Each non-ticker found is added, and `test_non_ticker_words_ignored` covers it; or the review records that none was found

---

### BLG-AI-24 — Journal summary advisory check: remaining false positives and misses
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Agent-mediated Director of Quality review of EPIC-03 (cycle `2026-10-29__release-v9.14`, ST-15 / BLG-AI-20), finding 3 — 2026-10-30
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
ST-15 added five advisory forms (ruling `ESC-EXEC-20261030-02`) to `journal_summary_language_failures()`. The DoQ review's probe found descriptive false positives: "Stops can be moved only upward under the system." (a statement of the system's own rule, via the passive form's "can") and reported speech ("The trader wrote that a review of setups is warranted."). Negation and gaps crossing ";" were fixed in-sprint (`9322b502`). It also found advisory sentences that still pass: "Consider a tighter stop.", "Perhaps revisit stop placement.", "It could help to tighten stops.", "Think about tightening stops.", "Your sizing is worth a second look." and "Stops would benefit from tightening.". A false positive fails safe (one regeneration, then the fallback) but costs a call and hides a legitimate summary.

**Scope**
- Ask the AI Compliance & Governance Officer whether to drop "can" from the passive form, exclude reported speech, and add the missed forms (each is a change to the ruling's forms)
- Implement the ruled forms; add the sentences above as positive or negative cases; update `ai_s13_boundary_test_suite.md` B-JS-04

**Acceptance Criteria**
- The ruling is recorded before the code change
- Each sentence above has the result the ruling assigns it, in a test
- Every ST-15 and v9.13 ST-18 case keeps its result

---

### BLG-AI-25 — Chat stop-time focus rule: ignore common upper-case non-ticker words
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Agent-mediated PR #2135 review (EPIC-03, cycle `2026-10-29__release-v9.14`, ST-17 / BLG-AI-22), Director of Quality finding 1 — 2026-10-30
**Effort:** XS (<1h plus tests)
**Provisional-Target:** TBD

**Problem**
ST-17 (ruling `ESC-EXEC-20261030-03`) stops giving a chat stop sentence to the focus ticker when the sentence names another ticker-like token, using `_TICKER_TOKEN_RE` and `_NON_TICKER_WORDS`. That list was built for the briefing summary, and chat uses other upper-case words. With focus `MU` held, "Your stop was hit at 3 PM.", "Your stop moved up EOD.", "Your stop is fine, IMO.", "Your stop held after Q3 earnings." and "The stop is near the VIX spike level." now get no MU note and are counted `unattributed`, where v9.13 appended the note (checked against `_append_missing_stop_times()` at `0940c874`). The reply then quotes a stop with no recalculation time, which is the explainability gap the stop-time check exists to close.

**Scope**
- Add common time, chat and abbreviation words (AM, PM, EOD, EOW, IMO, FYI, NOTE, Q1–Q4, VIX and similar) to `_NON_TICKER_WORDS`, or give the focus rule its own exclusion list; confirm with the AI Compliance & Governance Officer that this stays within the ruling (condition 2 of `ESC-EXEC-20261027-02` (B) is a minimum list)
- Add the sentences above as focus-attributed cases

**Acceptance Criteria**
- Each sentence above, with focus `MU` held, gets the MU note
- "TSLA's stop was hit last week." still gets no MU note; all ST-16 and ST-17 tests pass

---

### BLG-AI-26 — Journal summary advisory check: do not flag "could/may help explain"
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Agent-mediated PR #2135 review (EPIC-03, cycle `2026-10-29__release-v9.14`, ST-15 / BLG-AI-20), Director of Quality finding 2 — 2026-10-30
**Effort:** XS (<1h plus tests)
**Provisional-Target:** TBD
**Depends on:** BLG-AI-24 (same pattern set; one ruling can cover both)

**Problem**
ST-15's form (4) treats "could/may/might/would help" after a subject as advisory. It also matches the descriptive "help explain": "Moving stops to breakeven after a 2R gain could help explain the lower drawdown." and "Smaller position size in May may help explain why losses were lower." both return `["trading_change"]` (checked at `0940c874`). A legitimate summary is then regenerated and may end as the withheld fallback. BLG-AI-24 covers the other known false positives ("can", reported speech); this case is separate.

**Scope**
- Exclude "help explain/account for/show" (help + an explanatory verb) from form (4)'s evaluative phrase, under the AI Compliance & Governance Officer's ruling for BLG-AI-24
- Add both sentences as negative cases in `tests/test_journal_summary_language_check.py` and B-JS-04

**Acceptance Criteria**
- Both sentences above return `[]`
- "Tighter stops could help." and the other six BLG-AI-20 sentences are still caught

---

### BLG-AI-27 — Read production briefing ticker-caveat tokens and add any non-tickers (carried from ST-24)
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** ST-24 (EPIC-04, cycle `2026-11-03__release-v9.15`, `BLG-AI-23`; `DEL-20261105-01`). The production log read was not available in-sprint, and the AI Compliance & Governance Officer chose to carry it post-merge — 2026-11-05
**Effort:** XS (<1h plus tests)
**Provisional-Target:** TBD

**Problem**
ST-24's acceptance criteria need the tokens the daily-briefing ticker check has caveated since 2026-10-30. They are on the production Render log lines `ticker check: endpoint=POST /ai/daily-briefing field=summary ticker=<TOKEN> action=caveat_appended`. The sandbox `DATABASE_URL` is staging and the engine has no production log access, so the review could not run in-sprint. ST-26 (v9.15) added AM, PM, EOD, EOW, EOM, IMO, IMHO, FYI, NOTE, TBD, ASAP, Q1–Q4, FY, YOY, VIX, GMT and BST to `_NON_TICKER_WORDS`, so those tokens no longer fire. Any other non-ticker word still gets the caveat and inflates the `ticker_outside_context_appended` count.

**Scope**
- The user supplies the token list with counts since 2026-10-30, or grants a one-off read
- Classify each token as ticker or non-ticker
- Add the non-tickers to `_NON_TICKER_WORDS` (ruling `ESC-EXEC-20261027-02` (B) condition 2 is a minimum list) and to the `ai_endpoints.md` check 3 list

**Acceptance Criteria**
- The token list with counts is recorded
- Each non-ticker found is added and covered by `test_non_ticker_words_ignored`, or the review records that none was found

---

### BLG-AI-28 — Handle `_NON_TICKER_WORDS` entries that are also real tickers deliberately
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Agent-mediated AI Compliance & Governance Officer review of ST-26 (EPIC-04, cycle `2026-11-03__release-v9.15`, `BLG-AI-25`), finding 2 — 2026-11-05
**Effort:** XS (<1h plus tests)
**Provisional-Target:** TBD

**Problem**
`_NON_TICKER_WORDS` contains words that are also listed tickers. MA (Mastercard) and ON (ON Semiconductor) were already on the list, and PM (Philip Morris, in `backend/tickers_full_list.csv`) was added by ST-26. AM, IMO, NOTE and BST are listed symbols outside the scan universe. A held one is still cited, because `_ticker_in` runs first. A non-held one is no longer caveated in the briefing summary. In chat, "PM's stop was hit last week." with focus `MU` held and PM not held now gets the MU note, which is the misattribution ruling `ESC-EXEC-20261030-03` exists to prevent. The case is unlikely and fails soft, because a note is added and model text is never edited. But neither ruling nor the contract says the collision was decided.

**Scope**
- Ask the AI Compliance & Governance Officer how to treat collisions: for example, AM/PM count as non-tickers only after a time digit, or a word that is in the scan universe goes to the focus rule's "other ticker" path
- Implement the ruling for PM, MA and ON (and any other universe collision), with tests
- State the collision handling in `ai_endpoints.md` check 3 and in the chat focus paragraph

**Acceptance Criteria**
- The ruling is recorded before the code change
- With focus `MU` held and PM not held, "PM's stop was hit last week." gets the result the ruling assigns, in a test; "Your stop was hit at 3 PM." still gets the MU note
- All ST-16, ST-17 and ST-26 tests pass

---

### BLG-AI-29 — Daily briefing and chat: check output against §13.2's AI-text sentence
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Agent-mediated Director of Quality review of EPIC-04 (cycle `2026-11-03__release-v9.15`, ST-28 / `BLG-GOV-194`), finding 2 — 2026-11-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`strategy_rules.md` v1.25 §13.2 states that AI-written text describing the user's data, including the daily briefing and chat, must not suggest changing stops, position sizing, setups or any other strategy parameter. The journal summary (`journal_summary_language_failures`), debrief and monthly P&L narrative (`scan_prescriptive`) have output checks. `POST /ai/daily-briefing` and `POST /ai/chat` check only tickers and stop times, and the briefing system prompt asks for "recommended actions" without forbidding advice to change stops or sizing. So nothing enforces the sentence for those two features.

**Scope**
- Ask the AI Compliance & Governance Officer which check forms apply to the briefing and chat (briefing actions such as EXIT/HOLD are deterministic outputs, not parameter changes), and how a failure is handled (note, regenerate or fallback)
- Implement the ruled check and log its result in `claude_audit_log.compliance_check_result`
- Add B-DB/B-CH scenarios to `ai_s13_boundary_test_suite.md`

**Acceptance Criteria**
- The ruling is recorded before the code change
- A briefing or chat output suggesting tightening stops gets the ruled handling, in a test; a deterministic EXIT/HOLD action does not
- Every existing briefing and chat test passes

---

### BLG-AI-30 — Journal summary check: form (6) noun false positives and reported-speech gaps
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Agent-mediated Director of Quality review of EPIC-04 (cycle `2026-11-03__release-v9.15`, ST-25 / `BLG-AI-24`), findings 4 and 5 — 2026-11-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD
**Depends on:** BLG-AI-24 (ruling `ESC-EXEC-20261105-01` (A″))

**Problem**
Form (6) of ruling (A″) treats a sentence-initial change verb as an imperative. It therefore also fails descriptive sentences that start with a noun spelled the same way, such as "Review notes mention stop placement several times.", "Change was made to stops in April." and "Increase from 1% risk lifted position size.". These fail safe (regeneration, then the fallback), but they hide legitimate summaries. The past-tense reported-speech exemption (A″ (ii)) does not check who is speaking: "Overall, the review concluded that position sizing should be reduced." passes. It also covers the rest of the sentence: "The trader noted that losses were small, so consider tightening stops." passes.

**Scope**
- Ask the AI Compliance & Governance Officer whether to narrow form (6) (e.g. require a determiner or object after the verb) and to limit (ii) to the trader or notes as speaker and to the reported clause only
- Implement the ruled forms; add the sentences above as cases

**Acceptance Criteria**
- The ruling is recorded before the code change
- Each sentence above gets the result the ruling assigns, in a test
- Every ST-15, v9.13 ST-18 and v9.15 ST-25/ST-27 case keeps its result

---

### BLG-AI-31 — Journal summary check: past-tense "cut" and abbreviation or line-break sentence ends
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Agent-mediated PR #2192 review (EPIC-04, cycle `2026-11-03__release-v9.15`, ST-25 / `BLG-AI-24`), Director of Quality findings 1–2 and Product Owner finding 1 — 2026-11-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD
**Depends on:** BLG-AI-30 (same form (6); one ruling can cover both)

**Problem**
Form (6) of ruling (A″) reads a sentence-initial change verb as an imperative, and "cut" is spelled the same in the past tense. These descriptive sentences now fail as `trading_change`, where they passed on `main` before v9.15:
- "Cut position size after the March drawdown, per the notes."
- "Cut size on setups twice in April."

`ai_endpoints.md` 1.39 says past tense passes, which is not true for "cut".

The sentence-boundary sets (`_TC_GAP`, the form (6) lookbehind, `_SENTENCE_END_RE`) also treat the "." in abbreviations such as "e.g." and any hard line break as a sentence end. This causes errors both ways:
- Descriptive text wrongly fails: "Exits varied, e.g. cut size on two setups after the March losses."
- Advisory text wrongly passes: "Stops, e.g. on breakouts, could be tightened." and "Consider tightening\nstops."
- The reported-speech exemption stops at a line break: "The trader noted that\nstops could be tightened." fails.

False positives fail safe, but they hide legitimate summaries, which is the opposite of BLG-AI-24's aim.

**Scope**
- Ask the AI Compliance & Governance Officer how form (6) treats verbs whose past tense matches the imperative, and whether abbreviations and single line breaks end a sentence
- Implement the ruling and correct the contract's past-tense statement

**Acceptance Criteria**
- The ruling is recorded before the code change
- Each sentence above gets the ruled result, in a test
- Every ST-15, v9.13 ST-18 and v9.15 ST-25/ST-27 case keeps its result

---

### BLG-AI-32 — Journal summary check: advisory phrasings outside the ruled forms, and attribution after the clause
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Source:** Agent-mediated PR #2192 review (EPIC-04, cycle `2026-11-03__release-v9.15`, ST-25 / `BLG-AI-24`), Director of Quality findings 3–4 and Product Owner findings 2–3 — 2026-11-05
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
The forms in rulings (A), (A′) and (A″) are a list of known phrasings, not a complete set. The v1.25 §13.2 sentence is broader than what the check enforces. These advisory sentences return `[]` both on `main` and on the branch:
- Second-person and option-style advice: "You may want to tighten your stops.", "It would be wise to revisit position sizing.", "You might reduce position size on breakout setups.", "I'd suggest reviewing setups.", "One option is to widen stops.", "Going forward, use smaller position sizes.", "Maybe use a tighter stop.", "A tighter stop might be worth considering."
- Close variants of the A″ forms: "It could help tighten stops.", "Moving forward, review stop placement weekly.", "Note: review position sizing."
- A purpose clause after a dropped "can": "Stops can be tightened to limit losses."

The reported-speech exemption also misses attribution placed after the clause. Both of these fail:
- "Stops placed below the 20-day low would benefit from tightening, the trader wrote."
- `You wrote: "stops could be tightened".`

**Scope**
- Ask the AI Compliance & Governance Officer to rule on each sentence above, and on recording that the regex forms are not a complete set (residual risk)
- Implement the ruled forms, and state the residual risk in `ai_endpoints.md` and B-JS-04

**Acceptance Criteria**
- The ruling is recorded before the code change
- Each sentence above gets the ruled result, in a test
- Every ST-15, v9.13 ST-18 and v9.15 ST-25/ST-27 case keeps its result

---

### BLG-AI-33 — Make the reported-speech check linear and close its test gaps
**Priority:** P3 (Low)
**Type:** AI Compliance / Correctness
**Owner:** Backend Engineering Patterns Owner; QA & Testing Owner
**Source:** Agent-mediated PR #2192 review (EPIC-04, cycle `2026-11-03__release-v9.15`, ST-25 / `BLG-AI-24`), Director of Quality findings 5–6 — 2026-11-05
**Effort:** XS (<1h plus tests)
**Provisional-Target:** TBD

**Problem**
`_in_reported_speech()` (`backend/services/ai_service.py`) rescans the text from position 0 for every regex match, so cost grows quadratically. The review measured 5.2 s on 98 KB of reported matches and 13.4 s on a 192 KB single sentence. This is not reachable today, because the summary is capped at `max_tokens=512` (about 2–3 KB), but the cost appears if the cap rises or the check is reused. Several A″ paths also have no test:
- the "maybe" prefix
- the "•" and "1)" bullets
- the of/in/to guard, apart from "Review of"
- "help to show/account for"
- a multi-paragraph summary with newline boundaries

**Scope**
- Find the last sentence end before the match in one pass (e.g. `max(text.rfind(c, 0, start) for c in ...)`) instead of `finditer` from 0
- Add tests for the untested paths above

**Acceptance Criteria**
- 100 KB of reported matches is checked in under 0.5 s, in a test
- Each untested path above has a test with the ruled (A″) result
- All existing journal-summary tests pass

---

### BLG-QA-221 — Real-Postgres tests for the ai_audit_log UUID[] path and the claude_audit_log daily cost sum
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner; Backend Engineering Patterns Owner
**Source:** PR #2022 agent-mediated review (EPIC-01, cycle `2026-10-12__release-v9.12`), Director of Quality finding 5 — 2026-10-13
**Effort:** S (~0.5d)
**Provisional-Target:** TBD (re-targeted from v9.13 by the PMO Lead 2026-10-29: v9.13 shipped without it; `ESC-CLOSE-20260923-01`, closure_record.md §6 row 5)

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
**Provisional-Target:** TBD (re-targeted from v9.13 by the PMO Lead 2026-10-29: v9.13 shipped without it; `ESC-CLOSE-20260923-01`, closure_record.md §6 row 5)

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
**Provisional-Target:** TBD (re-targeted from v9.13 by the PMO Lead 2026-10-29: v9.13 shipped without it; `ESC-CLOSE-20260923-01`, closure_record.md §6 row 5)

**Problem**
`tests/test_settings_change_log.py` mocks the cursor. The SQL that ST-26 added in `backend/database.py` is never executed in CI: the `SELECT ... FOR UPDATE`, the `INSERT INTO settings_change_log`, and the `batch_id` subquery in `get_last_settings_change()`. `ci-tests.yml` Pytest Phase B starts a real `postgres:15` service, but no test creates the DS-33 schema in it. A typo or type mismatch in that SQL would first show up on staging or production as a failed settings save, because the log insert shares the save's transaction.

**Scope**
- In Phase B, create `settings` and the DS-33 `settings_change_log` table (from `data_model.md` DS-33) and run `create_settings` / `update_settings` / `get_last_settings_change` against it
- Skip cleanly when no real `DATABASE_URL` is available, as the existing Phase A/B split expects

**Acceptance Criteria**
- A Phase B test saves settings twice against real Postgres and asserts the log rows (field, old, new, source, shared `batch_id`) and the `last_change` payload
- A deliberately broken column name in the insert makes that test fail in CI

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
**✅ COMPLETE — 2026-11-03 — Head of Specs Team action-now patch, user-directed ("apply the 5 patches needed"), outside a sprint — `shared_standards.md` v3.41 §2 step 3; §6 checklist complete (OPERATIONAL_GUIDE.md v4.250) — branch `governance/2026-11-03-roadmap-scheduled`, PR #2141**
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
- [x] §2 and each engine's state-write rule agree

---

### BLG-GOV-393 — File a backlog item for every deferred roadmap prompt patch so a sprint can seat it
**✅ COMPLETE — 2026-11-03 — Head of Specs Team action-now patch, user-directed ("apply the 5 patches needed"), outside a sprint — `roadmap_prompt.md` v9.37 STEP -1.5 + `roadmap_prompt_appendix.md` v1.2 STEP 11.2; §6 checklist complete (OPERATIONAL_GUIDE.md v4.250) — branch `governance/2026-11-03-roadmap-scheduled`, PR #2141**
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
- [x] Both prompt changes applied with the §6 checklist

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

### BLG-QA-229 — Repeat the Stop Freshness manual check with stamped positions
**Priority:** P3 (Low)
**Type:** QA / Staging Verification
**Owner:** Infrastructure & Operations Owner; QA & Testing Owner
**Source:** EPIC-02 agent-mediated DoQ review (Director of Quality role), ST-10, sprint execution `2026-10-16__release-v9.13` — 2026-10-27
**Effort:** XS (<1h)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
ST-10's AC 2 asks for the System Status Stop Freshness value to match a recorded manual check. The 2026-10-27 staging check (`qa_evidence_EPIC-02.md`, `DEL-20261017-01`) matched only the empty state: both open staging positions (BARC, LGEN) had a NULL `stop_calculated_at`, so the median and maximum age and the oldest ticker were never compared with the database. The age calculation on real `TIMESTAMPTZ` values from the driver is unchecked on a deployed environment. Staging stamps come only from the on-load path after grace, because `nightly-stop-update.yml` calls `API_URL`, not `STAGING_API_URL`.

**Scope**
- Once at least one (ideally two or more) open staging position has a non-NULL `stop_calculated_at` (for example after loading Positions for a position past day 10), read the panel and run the read-only query in `metrics_definitions.md` §Stop Freshness → Manual check at about the same time
- Record both in the QA evidence of the cycle that runs it

**Acceptance Criteria**
- The panel's median, oldest age and oldest ticker match the query's non-NULL `age_hours` median, maximum and ticker (allowing for the seconds between reads), with date and environment recorded
- Any mismatch is filed as a defect

---

### BLG-BE-191 — Monthly P&L narrative treats missing restatement fields as "not restated"
**Priority:** P3 (Low)
**Type:** Backend Engineering / AI Input Correctness
**Owner:** Backend Engineering Lead; Strategy Rules & System Intent Owner (§13 check)
**Source:** PR #2073 agent-mediated review (Director of Quality role), ST-09 / EPIC-02, sprint execution `2026-10-16__release-v9.13` — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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

### BLG-BE-195 — Write attributed provider calls off the response path and on shutdown
**Priority:** P3 (Low)
**Type:** Backend / Observability
**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Source:** PR #2075 review (EPIC-05, cycle `2026-10-16__release-v9.13`, ST-29/ST-31) — 2026-10-28
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
`api_attribution_middleware` (`backend/main.py`) awaits `api_attribution.flush()`, one database insert, before it returns the response of any request that made a provider call, so those requests wait for an extra database round trip. Calls a background task makes after the response is sent stay in the in-memory buffer until another request flushes it, and are lost if the process restarts or Render redeploys first, which under-counts the attribution report.

**Scope**
- Flush the buffer outside the response path (a background task or a short-interval flusher thread), not inline in the middleware
- Flush the buffer in a shutdown handler

**Acceptance Criteria**
- A request that made provider calls returns without waiting for the insert (test)
- Buffered rows are written on application shutdown (test)
- The attribution report's counts are unchanged for a request-scoped call (existing tests pass)

---

### BLG-FE-234 — Mark a position's price as stale when the live price fetch fails
**Priority:** P3 (Low)
**Type:** Frontend / Data Provider Resilience
**Owner:** Infrastructure & Operations Owner; Head of UX & Design
**Source:** ST-33 (BLG-OPS-77), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/operations/data_provider_risk_assessment.md` §2, §3 QW-4 — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

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

### BLG-OPS-195 — Alert when weekly market-data call volume exceeds 2× the baseline
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Source:** ST-30 (BLG-OPS-18), EPIC-05, cycle `2026-10-16__release-v9.13` — `docs/ops/data_pipeline_cost_baseline.md` §5 — 2026-10-27
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
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

### BLG-OPS-197 — Record the weekly market-data call-volume baseline from production
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** ST-30 (BLG-OPS-18) AC 1 and ST-31 (BLG-OPS-19) AC 2, EPIC-05, cycle `2026-10-16__release-v9.13` — post-merge remainder, `DEL-20261027-06` and the production half of `DEL-20261027-04` — 2026-10-28
**Effort:** XS (<1h)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
**Depends on:** EPIC-05 merged and deployed to production; 7 days of production data

**Problem**
ST-30 filed the combined weekly cost baseline ($0.00, every source free) and the 2× advisory threshold, but the per-source weekly call volumes in `docs/ops/data_pipeline_cost_baseline.md` §4 are pending: they need a week of production attribution data, which only exists after EPIC-05 deploys. ST-31's DS-36 columns were confirmed on staging; their production Live Confirmation is also outstanding. Without the volume baseline, the 2× advisory (and BLG-OPS-195's automated check) has nothing to compare with.

**Scope**
- After the production deploy, run DS-36's Verification query on production and record it in `data_model.md` DS-36
- 7 full days after deploy, call `GET /ops/api-call-attribution?window=weekly` on production and fill §4's calls and failures per source, with the date and `top_contributors`
- Close `DEL-20261027-04` and `DEL-20261027-06`

**Acceptance Criteria**
- DS-36 Live Confirmation for production is recorded: `api_call_log.feature` text YES, `screener_runs.duration_seconds` numeric YES, index `idx_acl_called_at_feature`
- `data_pipeline_cost_baseline.md` §4 has weekly calls and failures for each source and combined, from one production weekly report, with its date and `top_contributors` (3 features, or every feature with calls if fewer than 3 made any); the §6 volume sign-off line is ticked

---

### BLG-OPS-198 — Record the full screener run p50/p95 baseline from production
**Priority:** P3 (Low)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner
**Source:** ST-32 (BLG-OPS-23), EPIC-05, cycle `2026-10-16__release-v9.13` — post-merge remainder of AC 1, `DEL-20261027-05` — 2026-10-28
**Effort:** XS (<1h)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
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

### BLG-OPS-199 — Fail the staging smoke host check when the backend reports no Render service ID
**Priority:** P3 (Low)
**Type:** Operations / Deployment
**Owner:** Infrastructure & Operations Owner
**Source:** PR #2075 review (EPIC-05, cycle `2026-10-16__release-v9.13`, ST-29/ST-31) — 2026-10-28
**Effort:** XS (<1h)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
**Depends on:** BLG-OPS-196 (first green staging deploy on `main` showing the host check pass)

**Problem**
`scripts/staging_smoke_test.py` `check_host_is_staging_backend()` treats a missing `render_service_id` on `GET /health/detailed` as a warning, so deploys from before v9.13 do not fail the smoke test. Once staging runs v9.13, a missing value means `RENDER_SERVICE_ID` is not set or `STAGING_API_URL` points at another host, and the check would pass with only a warning, which is the silent wrong-host case ST-29 exists to catch. The script also repeats the staging backend's service ID as its own literal instead of reading `STAGING_SERVICES` in `check_staging_deploy_drift.py`.

**Scope**
- Make a missing `render_service_id` a failure, once BLG-OPS-196 has shown the field on staging
- Read the expected service ID from `STAGING_SERVICES`
- Update `tests/test_staging_smoke_test.py`

**Acceptance Criteria**
- A `/health/detailed` response without `render_service_id` fails the smoke test (test)
- The expected service ID has one definition in the repo

---

### BLG-QA-230 — Add Playwright coverage for 15 uncovered state-changing actions
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** ST-24 (EPIC-04, v9.13) state-changing action sweep — 2026-10-28
**Effort:** M (~1-2 days)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
The ST-24 sweep (`docs/testing/state_changing_action_coverage.md`) found 15 of 52 state-changing primary actions that no Playwright test sends, including the Positions-page Exit modal submit, the abandon-plan submit, reflection save, note and tag save, and single deletes. A wrong route or method on any of them would ship unseen, which is how `PATCH /positions/{id}` (BLG-FE-226) went unnoticed.

**Scope**
- A test per uncovered action (inventory rows 2, 6, 7, 8, 11, 16, 17, 19, 24, 26, 30, 34, 39, 46, 52) asserting method, path and body
- Mock `/positions/{id}/mark-reviewed` in `position-review-cadence-nudge.spec.js` SC-RCN-06, whose PATCH is unanswered today

**Acceptance Criteria**
- Each listed action is Covered in the regenerated inventory
- SC-RCN-06's PATCH receives a mocked response

---

### BLG-FE-235 — Remove five uncalled state-changing client methods
**Priority:** P3 (Low)
**Type:** Frontend / Code Hygiene
**Owner:** Base44 Frontend Prompt Owner
**Source:** ST-24 (EPIC-04, v9.13) state-changing action sweep — 2026-10-28
**Effort:** XS (<1h)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
`base44Client.js` keeps `Signal.delete`, `Signal.generate`, `createSnapshot`, `trades.updateCosts` and the strategy benchmark `importData`, none with a caller. They are outside BLG-FE-230's scope, which covers only the methods whose route does not exist.

**Scope**
- Delete the five methods

**Acceptance Criteria**
- grep finds no definition or caller for any of them
- Frontend and e2e suites pass

---

### BLG-QA-231 — Fix the intermittent viewport check in the grace-panel deep-link test
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** EPIC-04 (v9.13) CI run 40784100342 and local full runs — 2026-10-29
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
`tests/e2e/grace-panel-position-link.spec.js` SC-GPL-01 fails intermittently on `expect(card).toBeInViewport()` ("viewport ratio 0"). It failed on both tries of attempt 1 in Playwright E2E run 40784100342 (shard 3/8, `2f5cc56a`), then passed on the re-run and on `5e8b6f04` with the same code. It also failed once locally on a build of unchanged `main`. It is the first demonstrated flaky test under `docs/testing/flaky_test_quarantine_process.md`, which is BLG-QA-75's gate condition. It has not been quarantined.

**Scope**
- Find why the highlighted card is sometimes not scrolled into view (scroll timing vs. layout settling after the Positions list renders) and fix the test or the scroll
- Decide quarantine per the Flaky-Test Disposition Addendum if the fix is not immediate, and record the incident against BLG-QA-75's gate

**Acceptance Criteria**
- SC-GPL-01 passes in 20 consecutive local runs under `--repeat-each=20 --workers=4`
- The quarantine process doc's Currently-Known Flaky Tests section reflects the outcome

---

### BLG-QA-232 — Assert the ST-25 colour changes that have no Playwright coverage
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** EPIC-04 (v9.13) agent-mediated DoQ review of ST-25, frontend testing gate (CLAUDE.md §2) — 2026-10-29
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
ST-25 changed colours that no Playwright test or staging run checks: the destructive-button hover from rose-500 to rose-700 on seven confirm buttons (decision record §2.2), the Cash Management deposit fill (emerald-700) and `text-white` on its submit button, and `text-white` on System Status "Refresh Health". AC 2's listed sites are asserted in `coloured-button-fills.spec.js`; these addendum states are not.

**Scope**
- Extend `tests/e2e/coloured-button-fills.spec.js`: hover each of the seven rose-600 confirm buttons and assert `rgb(190, 18, 60)`; assert the deposit and withdraw submit fills and white text; assert Refresh Health's white text in dark theme
- Scoped axe colour-contrast on each, both themes

**Acceptance Criteria**
- Each listed state has a passing Playwright assertion in CI
- No `color-contrast` violation on those buttons in either theme

---

### BLG-QA-233 — Assert the Post-Trade Debrief button text colour directly
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality; QA & Testing Owner
**Source:** EPIC-04 (v9.13) ST-25 consequence fix in `TradeDebrief.js` (`2f5cc56a`) — 2026-10-29
**Effort:** XS (<1h)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
ST-25 gave the Post-Trade Debrief Generate and Regenerate buttons `text-slate-800 dark:text-slate-300`, fixing a 1.48:1 light-theme contrast failure that axe had missed while the buttons sat off-screen. Today only the section's axe scans (SC-DBF-06a, SC-DBF-10b) cover it, and they depend on the buttons being on screen at 1280px. A layout change that pushes them off-screen again would hide a regression.

**Scope**
- Add `toHaveCSS('color', …)` assertions for both buttons in `tests/e2e/trade-debrief.spec.js`, in both themes

**Acceptance Criteria**
- Generate and Regenerate assert slate-800 (`rgb(30, 41, 59)`) in light and slate-300 (`rgb(203, 213, 225)`) in dark, passing in CI

---

### BLG-QA-234 — Stop the frontend route check passing a literal path through a parameter route
**Priority:** P3 (Low)
**Type:** QA / Contract Tooling
**Owner:** Director of Quality; API Contracts & Documentation Owner
**Source:** PR #2076 (EPIC-04, v9.13) agent-mediated Director of Quality / Product Owner review — 2026-10-29
**Effort:** XS (<1h)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
`scripts/check_frontend_api_calls.py` (ST-23) matches a call against openapi paths with each `{param}` treated as "any segment". A literal call with a mistyped segment therefore passes when a parameter route has the same shape: `GET /positions/complainse` passes via `GET /positions/{position_id}`, and `DELETE /trade-plans/bluk` via `DELETE /trade-plans/{id}`. No current call depends on this; it is a latent false negative in the check meant to catch exactly this class of mistake.

**Scope**
- A call whose resolved path has no `{param}` must match a literal openapi path, or be listed in an allow-list with its reason (e.g. a hard-coded parameter value)
- A test for each case

**Acceptance Criteria**
- `GET /positions/complainse` and `DELETE /trade-plans/bluk` fail the check (test)
- The check still passes on the real `src/` tree

---

### BLG-QA-236 — Keep the state-changing action inventory in step with the code
**Priority:** P3 (Low)
**Type:** QA / Contract Tooling
**Owner:** Director of Quality; QA & Testing Owner
**Source:** PR #2076 (EPIC-04, v9.13) agent-mediated Director of Quality / Product Owner review — 2026-10-29
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
`docs/testing/state_changing_action_coverage.md` (ST-24) is a point-in-time snapshot. A new POST/PUT/PATCH/DELETE call added to `src/` does not appear in it, so ST-24's "every action is covered or has a dated backlog item" stops being true the first time a feature ships without anyone updating the document.

**Scope**
- A CI check comparing the state-changing call sites from `check_frontend_api_calls.py`'s extractor with the inventory's call-site column, failing on a call site missing from the document

**Acceptance Criteria**
- Adding an unlisted state-changing call fails the check (test)
- The check passes on the current tree and document

---

### BLG-OPS-200 — Confirm the production GitHub Pages deploy succeeds after the ESLint config fix
**✅ COMPLETE — 2026-10-30 — cycle `2026-10-29__release-v9.14` (ST-01 post-merge AC 1, EPIC-01) — `deploy.yml` run 41024971887 on merge commit 48eab523; banner added 2026-11-03 by the Infrastructure & Operations Owner (agent-mediated per §5.3, user-directed 2026-11-03; closure_record.md `2026-10-29__release-v9.14` §6 row 7)**
**Priority:** P3 (Low)
**Type:** Operations / Deployment
**Owner:** Infrastructure & Operations Owner
**Source:** Sprint Planning `2026-10-29__release-v9.14` STEP 6.2 post-merge AC check (LL-v9.13-P3-03) — post-merge AC 1 of ST-01 (BLG-OPS-193), EPIC-01 — 2026-10-29
**Effort:** XS (<1h)
**Provisional-Target:** v9.14
**Depends on:** ST-01 (BLG-OPS-193) merged to `main`

**Problem**
ST-01 restores `eslint-config-react-app` so the frontend builds again. Only a `deploy.yml` run on `main` can show that production GitHub Pages receives a new build, so this AC cannot be met on the EPIC branch. Production has not received a frontend build since 2026-10-15.

**Scope**
- After ST-01 merges, check the `deploy.yml` run for the merge commit
- Confirm production serves the new build (for example, the asset hash in the served `index.html` matches the run's build output)

**Acceptance Criteria**
- `deploy.yml` succeeds on `main` for a commit that includes ST-01, with the run ID recorded
- Production serves that build, with the check and date recorded in the v9.14 QA evidence or delegation log

**Resolved (2026-10-30, after PR #2131 merged):** `deploy.yml` run 41024971887 on merge commit `48eab523` succeeded. GitHub Pages serves `main.c884033b.js`, which contains EPIC-01 strings. Recorded in `qa_evidence_EPIC-01.md` under Post-merge confirmations.

---

### BLG-GOV-399 — Review the first live quarterly AI output sample from production
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Source:** Sprint Planning `2026-10-29__release-v9.14` STEP 6.2 post-merge AC check (LL-v9.13-P3-03) — post-merge/production-data AC 1 of ST-23 (BLG-GOV-178), EPIC-03 — 2026-10-29
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
**Depends on:** ST-15–ST-18 merged and deployed; a production read credential

**Problem**
ST-23's first AC reviews 10 production AI outputs drawn from the `BLG-AI-06` sampling hook. It needs production data and a production credential, which the governed environment lacks, so it can only be met with production access, possibly after merge.

**Scope**
- Draw 10 production AI outputs from `ai_output_sampling_service`
- Check each against §13.2 and the §13.5 roster row for its feature (daily briefing + chat, Gemini thesis generation, post-trade debrief, monthly P&L narrative)

**Acceptance Criteria**
- A dated audit doc records the outcome for each of the 10 outputs, citing every §13 clause that names AI output
- Each finding is filed as a backlog item

---

### BLG-OPS-201 — Populate the cost-by-feature-area report with a full month of production data
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** Sprint Planning `2026-10-29__release-v9.14` STEP 6.2 post-merge AC check (LL-v9.13-P3-03) — production-data AC 2 of ST-39 (BLG-OPS-85), EPIC-06 — 2026-10-29
**Effort:** XS (<1h)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from v9.14, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)
**Depends on:** ST-39 (BLG-OPS-85) report merged; production read access

**Problem**
ST-39 produces a report in `docs/ops/` that partitions compute cost by feature area. Populating it for a complete month needs production `claude_audit_log` and API-call attribution data, which CI and the governed environment cannot reach.

**Scope**
- Run the report's method against at least one complete month of production data
- Record the populated figures in the ST-39 report

**Acceptance Criteria**
- The ST-39 report is populated for at least one complete calendar month of production data, with the month and the data date stated

---

### BLG-OPS-202 — Confirm ci-usage-report.yml commits its report from a run on main
**✅ COMPLETE — 2026-10-30 — cycle `2026-10-29__release-v9.14` (ST-42 post-merge ACs, EPIC-06) — `ci-usage-report.yml` run 41082206367 on `main`, report merged via PR #2134; banner added 2026-11-03 by the Infrastructure & Operations Owner (agent-mediated per §5.3, user-directed 2026-11-03; closure_record.md `2026-10-29__release-v9.14` §6 row 7)**
**Priority:** P3 (Low)
**Type:** Operations / CI
**Owner:** Infrastructure & Operations Owner
**Source:** Sprint Planning `2026-10-29__release-v9.14` STEP 6.2 post-merge AC check (LL-v9.13-P3-03) — post-merge AC 1 and AC 2 of ST-42 (BLG-OPS-188), EPIC-06 — 2026-10-29
**Effort:** XS (<1h)
**Provisional-Target:** v9.14
**Depends on:** ST-42 (BLG-OPS-188) merged to `main`

**Problem**
ST-42 fixes `ci-usage-report.yml`'s monthly commit, which failed on its only scheduled run. The workflow commits its report from the branch it runs on, so only a run on `main` (a `workflow_dispatch` with `year_month=2026-09`, or the next scheduled run) can show that the report reaches `docs/ops/ci_usage_reports/`.

**Scope**
- After ST-42 merges, dispatch `ci-usage-report.yml` on `main` with `year_month=2026-09`
- Confirm the commit lands

**Acceptance Criteria**
- A `ci-usage-report.yml` run on `main` succeeds, with the run ID recorded
- `docs/ops/ci_usage_reports/2026-09.md` exists on `main`

**Resolved (2026-10-30, after PR #2133 merged):** `ci-usage-report.yml` run 41082206367 (workflow_dispatch on `main` by the user, `year_month=2026-09`, 2026-10-30T15:36:04Z) succeeded. It committed the report to `ci-usage-report/2026-09` (`2919a2e5`) and warned, as expected, that Actions may not open pull requests. The engine opened PR #2134 from the user's account; all 22 checks passed; the user merged it at 15:50:47Z (merge commit `cc52d408`). `docs/ops/ci_usage_reports/2026-09.md` is on `main`. Recorded in `qa_evidence_EPIC-06.md` under Post-merge confirmations. The PR still had to be opened by hand; BLG-OPS-210 tracks automating it.

---

### BLG-SEC-44 — Record the staging and production CORS preflight checks after the allow-list change
**✅ COMPLETE — 2026-10-30 — cycle `2026-10-29__release-v9.14` (ST-43 post-merge AC 2, EPIC-06, `DEL-20261030-01`) — staging and production CORS preflights recorded; banner added 2026-11-03 by the Cybersecurity & Trust Lead with the Infrastructure & Operations Owner (agent-mediated per §5.3, user-directed 2026-11-03; closure_record.md `2026-10-29__release-v9.14` §6 row 7)**
**Priority:** P3 (Low)
**Type:** Security / Configuration
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** Sprint Planning `2026-10-29__release-v9.14` STEP 6.2 post-merge AC check (LL-v9.13-P3-03) — post-merge AC 2 of ST-43 (BLG-SEC-43), EPIC-06 — 2026-10-29
**Effort:** XS (<1h)
**Provisional-Target:** v9.14
**Depends on:** ST-43 (BLG-SEC-43) merged and deployed; the per-environment variable set on Render

**Problem**
ST-43 builds the CORS allow-list from a per-deployment environment variable. The preflight checks against the deployed staging and production services need the deployed code and the Render variable, so they cannot be met in CI.

**Scope**
- After deploy, send an `OPTIONS` preflight from the Pages origin and from `http://localhost:3000` to staging and to production

**Acceptance Criteria**
- Production rejects `http://localhost:3000` and accepts the Pages origin, with the commands, responses and date recorded
- The staging result is recorded the same way

**Resolved (2026-10-30, after PR #2133 merged):** the user set `DEPLOY_ENV=production` on the production API; staging already had `DEPLOY_ENV=staging`. Preflights at 15:18–15:19Z and 15:29Z: production rejects `http://localhost:3000` (400) and accepts the Pages origin (200); staging accepts localhost and its own frontend and rejects the Pages origin. Commands, results and the agent-mediated Cybersecurity & Trust Lead confirmation of the staging defaults are in `docs/infrastructure/cors_allow_list.md` §Deployed checks and `qa_evidence_EPIC-06.md`.

---

### BLG-GOV-400 — Confirm the gate scan no longer re-lists items whose gating item has shipped
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** Sprint Planning `2026-10-29__release-v9.14` STEP 6.2 post-merge AC check (LL-v9.13-P3-03) — post-merge AC 2 of ST-45 (BLG-GOV-398), EPIC-07 — 2026-10-29
**Effort:** XS (<1h)
**Provisional-Target:** v9.15
**Depends on:** ST-45 (BLG-GOV-398) merged; the next run of the engine ST-45 changes (`plan release` or `groom backlog`)

**Problem**
ST-45 gives the gate scan's "gating item shipped" findings a write-back path. Its second AC can only be checked on the next run of the chosen engine, after merge. `BLG-OPS-85` and `BLG-OPS-21`, the live cases, are themselves in v9.14 scope (ST-38, ST-39), so the check needs an item that is still open at that run.

**Scope**
- At the next run of the engine ST-45 changes, read the gate scan's "gating item shipped" list

**Acceptance Criteria**
- No item whose whole gate condition is a shipped item is re-listed, or each re-listed item is named with the reason the write-back did not apply

---

### BLG-OPS-203 — Live-confirm DS-37 fx_rate_last_good on staging and production
**Priority:** P3 (Low)
**Type:** Operations / Data Verification
**Owner:** Data Model & Domain Schema Owner; Infrastructure & Operations Owner
**Source:** Sprint execution `2026-10-29__release-v9.14`, ST-04 (BLG-BE-194), EPIC-01 — 2026-10-29
**Effort:** XS (<1h)
**Provisional-Target:** v9.15
**Depends on:** EPIC-01 of `2026-10-29__release-v9.14` merged and deployed

**Problem**
DS-37 (`data_model.md` v2.66) adds the `fx_rate_last_good` table, created at runtime by `ensure_fx_rate_last_good_table()`. Like DS-35, its Verification query has to be run on each environment and recorded as Live Confirmation; the engine has no authorisation to query the live databases.

**Scope**
- After deploy, run DS-37's Verification query on staging, then production (read-only, with the user's permission)
- Record the output in DS-37's sign-off as Live Confirmation

**Acceptance Criteria**
- Each environment shows 3 columns (`pair`, `rate`, `fetched_at`), none nullable, and one `GBPUSD` row with a recent `fetched_at`, recorded with the date

**Resolved (2026-10-30, after PR #2131 merged):** DS-37's Verification query was run on staging (by the execution session, read-only, with the user's permission) and on production (by the user, Supabase SQL editor). Both show `pair`, `rate` and `fetched_at`, none nullable, and one `GBPUSD` row at `1.341000`, fetched 2026-10-30 08:16:33+00 (staging) and 08:15:42+00 (production). Recorded as DS-37's Live Confirmation in `data_model.md`.

---

### BLG-OPS-204 — Point Render staging back at main and confirm its build from main
**✅ COMPLETE — 2026-10-30 — cycle `2026-10-29__release-v9.14` (ST-01 AC 2 evidence gap, EPIC-01) — Render staging pointed back at `main` and built from it; banner added 2026-11-03 by the Infrastructure & Operations Owner (agent-mediated per §5.3, user-directed 2026-11-03; closure_record.md `2026-10-29__release-v9.14` §6 row 7)**
**Priority:** P2 (Medium)
**Type:** Operations / Deployment
**Owner:** Infrastructure & Operations Owner
**Source:** Sprint execution `2026-10-29__release-v9.14`, ST-01 (BLG-OPS-193), EPIC-01 — agent-mediated DoQ review finding 2 — 2026-10-29
**Effort:** XS (<1h)
**Provisional-Target:** v9.14
**Depends on:** EPIC-01 of `2026-10-29__release-v9.14` merged to `main`

**Problem**
ST-01 AC 2 asks for the Render staging frontend to build from `main` with no dashboard-only ESLint workaround. Before merge it could only be shown on the EPIC branch: the user pointed `trading-assistant-staging` at `exec/2026-10-29__release-v9.14/EPIC-01`, removed `DISABLE_ESLINT_PLUGIN`, and the build of `4719c694` succeeded (`DEL-20261029-01`). Staging still points at the branch, so it will go stale unless it is pointed back at `main`. BLG-OPS-200 covers only `deploy.yml` and GitHub Pages.

**Scope**
- After EPIC-01 merges, set the `trading-assistant-staging` branch back to `main` in the Render dashboard
- Confirm the first staging build from `main` succeeds with no `DISABLE_ESLINT_PLUGIN` (the repo `.npmrc` supplies `legacy-peer-deps`)

**Acceptance Criteria**
- Staging's branch is `main`, recorded with date
- The staging build of a `main` commit containing `3fbfe5e3` succeeds, with its "Compiled" line and commit recorded in the v9.14 QA evidence for EPIC-01

**Resolved (2026-10-30, after PR #2131 merged):** the user confirmed on 2026-10-30 that `trading-assistant-staging` is pointed back at `main` and builds from it. The user then supplied the staging deploy log: the build finished 08:14:29Z with ESLint warnings only, and the site went live. It is recorded in `qa_evidence_EPIC-01.md` under Post-merge confirmations. The excerpt does not show the commit or the "Compiled" line; by timing it is a `main` commit at or after `48eab523`.

---

### BLG-SPEC-210 — Document the unknown-regime response shapes on three endpoints, and drop the unruled branches from two page specs
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner; Frontend Specifications & UX Documentation Owner
**Source:** Sprint execution `2026-10-29__release-v9.14`, ST-03 (BLG-BE-193), EPIC-01 — agent-mediated DoQ review findings 6 and 9 — 2026-10-29
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15

**Problem**
ST-03 made an unmeasured market regime `unknown` (`strategy_rules.md` v1.20). Three responses changed shape without contract updates: `POST /positions/risk-off-alerts` now returns `us_regime_status`/`uk_regime_status` and nullable `spy_risk_on`/`ftse_risk_on`, and leaves an unknown market's flags unchanged; `GET /positions/analyze`'s `market_regime` now carries `*_regime_status`, `spy_source`/`ftse_source` and null prices; the signals generate response's `market_regime.spy_risk_on`/`ftse_risk_on` can be null. Separately, `dashboard.md` v3.10 §Card 4 and `signals.md` v0.7 §Market Status Bar still describe all three ruling branches; the ruling was (a), and the decision record says the unused branches are deleted at implementation.

**Scope**
- Update `position_endpoints.md` (§POST /positions/risk-off-alerts, §GET /positions/analyze), `signal_endpoints.md` (generate response) and `openapi.yaml` for the nullable/added fields
- Remove branches (b) and (c) from `dashboard.md` §Card 4 and `signals.md` §Market Status Bar, keeping the ruling (a) sentence

**Acceptance Criteria**
- Each of the three contracts documents the unknown case, with `openapi.yaml` matching
- Neither page spec mentions "last known" or "risk-on with a warning" as a live behaviour

---

### BLG-SPEC-211 — Remove the retired generate-thesis endpoint from live documents
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner; AI Compliance & Governance Officer; Metrics Definitions & Analytics Canonical Owner
**Source:** Agent-mediated Director of Quality review of EPIC-03 (cycle `2026-10-29__release-v9.14`, ST-22 / BLG-BE-163), finding 4 — 2026-10-30
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
ST-22 retired `POST /trade-plans/{plan_id}/generate-thesis` (404 since v9.14) and fixed the code, OpenAPI, contracts and the key-rotation runbook. Several live documents still describe it as current. `docs/specs/metrics_definitions.md` (~L1057–1067) defines the thesis adoption rate's denominator on this endpoint, so the metric now stops changing. `docs/specs/api_contracts/ai_endpoints.md` (~L502) and `backend/services/ai_endpoint_anomaly_service.py` (~L35) still say "6 AI-invoking endpoints". `docs/governance/ai_feature_touchpoint_register.md` (~L24), `docs/governance/ai_model_version_pinning_policy.md` (~L39) and `docs/ops/external_api_credential_inventory.md` (~L59) still list it as live.

**Scope**
- Redefine the thesis adoption rate on `POST /trade-plans/generate-plan` (or retire it), as a metrics decision
- Update the anomaly check's endpoint list and its contract text to the 5 live AI endpoints; keep historical audit rows readable
- Mark the endpoint retired in the three registers

**Acceptance Criteria**
- `grep -rn "generate-thesis"` over `docs/specs`, `docs/governance`, `docs/ops` (excluding dated audit, decision and changelog records) and `backend/` finds only historical references
- The thesis adoption rate has a live denominator or is marked retired

---

### BLG-QA-239 — Test that live signal generation gives no entry signals for an unknown market
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Sprint execution `2026-10-29__release-v9.14`, ST-03 (BLG-BE-193), EPIC-01 — agent-mediated DoQ review finding 8 — 2026-10-29
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15

**Problem**
ST-03 changed `signal_service.generate_momentum_signals` so a market whose index data is unavailable is unknown (None) and gets no entry signals, as `strategy_rules.md` v1.20 §4.2.1 requires. Before, both indices were assumed risk-on when either was missing. The behaviour has no unit test; only the shared helpers and the pre-entry gate are covered.

**Scope**
- Add a test with SPY data unavailable and FTSE data available: no US signals, UK signals unaffected, and `market_regime.spy_risk_on` is None in the response

**Acceptance Criteria**
- The test fails if an unknown market is treated as risk-on again

---

### BLG-BE-196 — Decide how Regime Adherence counts a trade plan saved while the regime was unknown
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner
**Source:** PR #2131 (EPIC-01, `2026-10-29__release-v9.14`) agent-mediated DoQ/PO review, ST-03 (BLG-BE-193) — 2026-10-30
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15

**Problem**
ST-03 makes an unmeasured regime `unknown`. The Trade Plan page fills `regime_context_at_entry` from `GET /market/status` (`src/pages/TradePlan.js` `regimeFromHealth`), so a plan saved during an outage now stores `"unknown"`; before ST-03 it stored the defaulted `"risk_on"`. `behavioural_drift_service.py` counts only `risk_on`, `neutral`, null and `""` as valid, so each such plan counts as a Regime Adherence violation. `si02_drift_score.md` §3.4 counts an undeterminable regime (`neutral`) as not a violation, and does not mention `unknown`.

**Scope**
- Get a ruling: whether `unknown` counts like `neutral` (not a violation) or as a violation, given that `strategy_rules.md` v1.20 §4.2.1 blocks entries while the regime is unknown
- Apply it in `behavioural_drift_service.py` and `si02_drift_score.md` §3.4 (regime classification list), with a unit test

**Acceptance Criteria**
- `si02_drift_score.md` §3.4 names `unknown` and says how it is counted
- A unit test with one `regime_context_at_entry = "unknown"` trade gives the ruled Regime Adherence result

---

### BLG-BE-197 — Fire the risk-off regime alert for a measured market while the other market is unknown
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner
**Source:** PR #2131 (EPIC-01, `2026-10-29__release-v9.14`) agent-mediated DoQ/PO review, ST-03 (BLG-BE-193) — 2026-10-30
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15

**Problem**
`alerts_service._check_regime_change` combines both markets ("SPY and/or FTSE 100 is now below its 200-day moving average"). ST-03 returns early when either market is unknown, so the baseline is not moved. While FTSE is unknown, a measured SPY move to risk-off raises no `market_regime_change` alert; it fires only once FTSE is measured again. The nightly risk-off job still flags the US positions, so exits are not affected. Only the alert is delayed.

**Scope**
- Compare the markets that were measured: alert when a measured market moves from risk-on to risk-off, and leave an unknown market's baseline unchanged
- Add a test: FTSE unknown, SPY risk-on then risk-off, so the alert fires

**Acceptance Criteria**
- With one market unknown, a measured risk-on to risk-off move in the other market raises the alert on that call
- An unknown reading on its own still raises no alert and does not move that market's baseline (the existing ST-03 test still passes)

---

### BLG-OPS-205 — Seed staging's UK positions with the .L suffix so they get live prices
**Priority:** P3 (Low)
**Type:** Operations / Staging Data
**Owner:** Infrastructure & Operations Owner; QA & Testing Owner
**Source:** Staging backend log after PR #2131 (EPIC-01, `2026-10-29__release-v9.14`) merged, supplied by the user — 2026-10-30
**Effort:** XS (<1h)
**Provisional-Target:** v9.15

**Problem**
`scripts/seeds/seed_portfolio_trades.sql` inserts the two open staging positions as `LGEN` and `BARC` with `market = 'UK'`, without the `.L` suffix. The app adds the suffix when it creates a UK position (`position_service.py`, `if market == 'UK' and not ticker.endswith('.L')`). Pricing routes on the suffix (`utils/pricing._is_us_ticker`), so it treats the seeded tickers as US. Alpaca returns 0 bars, Yahoo has no price for the bare symbol, and every staging request shows both positions as stale (log 2026-10-30T08:16:39Z–08:16:52Z). Staging therefore never exercises a live UK price.

**Scope**
- Change the seed to `LGEN.L` and `BARC.L` (and any other UK ticker the seed scripts insert without the suffix)
- Correct the two existing staging rows, with the user's permission (staging write)

**Acceptance Criteria**
- No seed script inserts a `market = 'UK'` ticker without `.L`
- After a staging reseed or correction, `GET /positions` on staging returns `price_is_stale: false` for both UK positions while Yahoo Finance is reachable

### BLG-BE-198 — Store the native entry in trade_history for a US exit whose fill_price is NULL
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Backend Engineering Patterns Owner
**Source:** ST-13 / EPIC-02, sprint execution `2026-10-29__release-v9.14` (found while checking spec descriptions of `entry_price`) — 2026-10-30
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.15

**Problem**
`exit_position()` (`backend/services/position_service.py`, ~line 1269) sets the `trade_history.entry_price` it writes from `position.get('fill_price', position['entry_price'])` for US positions. When the `fill_price` column exists but is NULL, `.get` returns None, so the exit passes None for `trade_history.entry_price`, which `data_model.md` §3 documents as `NOT NULL`. Exiting such a position would fail at the insert. It is the same pattern as `BLG-BE-167` in `GET /portfolio` (fixed in v9.12, `cc7774e9`; test added v9.14 ST-12). Realised P&L does not read this value, so only the stored entry is affected.

**Scope**
- Use `fill_price or entry_price × fx_rate` for the US native entry in `exit_position()`, as `portfolio_service.py` and the lifecycle readers do

**Acceptance Criteria**
- A pytest exits a US position whose `fill_price` is None and asserts the `trade_history` row's `entry_price` is `entry_price × fx_rate` (native), with no error
- No `get('fill_price', ...)` default-argument read remains in `backend/`

---

### BLG-BE-199 — Reject a non-positive FX override in POST /portfolio/size
**Priority:** P3 (Low)
**Type:** Backend Engineering / Correctness
**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner
**Source:** PR #2132 agent-mediated Director of Quality review (EPIC-02, cycle `2026-10-29__release-v9.14`) — 2026-10-30
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.15

**Problem**
`size_position()` accepts any `fx_rate` override for a US position. `fx_rate: 0` raises `ZeroDivisionError` (HTTP 500), and a negative rate returns `valid: true` with negative `suggested_shares` (e.g. −12.7 for £100 risk, $10 stop, FX −1.27). Both are pre-existing (the pre-v9.14 formula failed the same way), but `strategy_rules.md` §4.1.4's validity rules do not cover the FX rate, and the property test only samples FX in 0.5–2.0, so nothing catches it.

**Scope**
- Return an invalid result with a deterministic reason code (e.g. `INVALID_FX_RATE`) when a US `fx_rate` override is ≤ 0, before any calculation
- Add the reason code to `portfolio_endpoints.md` §POST /portfolio/size and, if the Strategy Rules & System Intent Owner agrees, to §4.1.4

**Acceptance Criteria**
- `fx_rate` 0 and a negative `fx_rate` for a US position each return `valid: false` with the new reason code, never a 500 or negative shares (pytest)
- UK requests ignore `fx_rate` as today

---

### BLG-BE-200 — Run the remaining ensure_* DDL calls once per process
**Priority:** P3 (Low)
**Type:** Backend Engineering / Performance
**Owner:** Backend Engineering Patterns Owner
**Source:** ST-21 (EPIC-03, cycle `2026-10-29__release-v9.14`, BLG-BE-166), out-of-scope finding — 2026-10-30
**Effort:** XS (<1h plus tests)
**Provisional-Target:** TBD

**Problem**
ST-21 added `database.ensure_once` and made 28 of 34 `ensure_*`-before-write call sites run their DDL once per process; 3 already did (`docs/ops/ensure_ddl_insert_call_sites.md`). Three sites still run DDL on every call. `ensure_monthly_pnl_snapshots_table(conn)`, called from `database.insert_monthly_pnl_snapshot_if_absent` and `services/reports_service.get_monthly_pnl_report`, runs in the caller's connection and transaction, so recording success when it returns could record a DDL that later rolls back. `ensure_alerts_tables` (`services/alerts_service.evaluate_alerts`) is defined outside `database.py`, and tests replace `database` with a stub at import, so the decorator cannot be imported there.

**Scope**
- Record success for the `conn` variant only after the caller commits, or move its DDL to startup
- Give `ensure_alerts_tables` its own module-level once flag
- Update `docs/ops/ensure_ddl_insert_call_sites.md` rows 27 and 28

**Acceptance Criteria**
- A second call in the same process runs no DDL at each of the three sites (tests)
- A rolled-back first call is retried on the next call
- The listing doc shows all 34 sites as once per process

---

### BLG-FE-236 — Daily Position Monitor footer says "All positions healthy" while an in-grace position is below its stop
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Source:** PR #2132 agent-mediated Product Owner review (EPIC-02 ST-11, cycle `2026-10-29__release-v9.14`) — 2026-10-30
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.15

**Problem**
Since ST-11 (v9.14), an in-grace position priced at or below its trailing stop is a hold with the reason "In grace: stop not enforced". When no exit is suggested, `MonitorModal`'s footer reads "All positions healthy" even while such a row is listed, so the footer and the row disagree. `monitor-grace-aware-suggestions/decision_record.md` did not cover the footer.

**Scope**
- Decide the footer wording when one or more in-grace breaches are listed and nothing is suggested (e.g. "No exits suggested · 1 in grace below its stop"), via a design note
- Implement it and update `positions.md` §Monitor Suggestions

**Acceptance Criteria**
- With only an in-grace breach listed, the footer no longer reads "All positions healthy" (Playwright)
- With no breach at all, the footer is unchanged

---

### BLG-QA-240 — Make the execution-state consistency check count EPICs not yet initialised as pending
**Priority:** P3 (Low)
**Type:** QA / Test Automation (governance tooling)
**Owner:** Director of Quality; Head of Specs Team
**Source:** EPIC-02 merge-gate persist, sprint execution `2026-10-29__release-v9.14` — 2026-10-30
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.15
**Folded in (2026-11-03):** `BLG-GOV-401` (same defect, filed at ST-44) is killed as a duplicate of this item; its scope is covered here.

**Problem**
`scripts/check_execution_state_consistency.py` derives `merge_gate.epics_pending` from the EPICs present in `execution_state.json`'s `epics` object, and requires `all_merged` to be true exactly when that list is empty. In v9.14 each EPIC is added to `epics` when its own execution starts, so after EPIC-01 and EPIC-02 merged the script demanded `epics_pending: []` and `all_merged: true` while five EPICs were still unstarted. Following it would make the next `run sprint` treat the sprint as fully merged and run STEP 5 Sprint Close early. Both persisted merge states (EPIC-01 `eee3e2f9`, EPIC-02) fail the check, so the §9.2 read-back cannot pass at the moment it matters most.

**Scope**
- Derive the expected pending set from the sprint's full EPIC list (`merge_order`, or `sprint_backlog_index.json`), not only from initialised EPICs
- Add a test with a partially initialised state (two merged, five not yet initialised)

**Acceptance Criteria**
- The check passes for `epics_merged` = EPIC-01, EPIC-02, `epics_pending` = the other five, `all_merged: false`
- It fails when `epics_pending` is empty while `merge_order` lists an unmerged EPIC

---

### BLG-OPS-206 — Build the E2E React bundle once per Playwright run and share it with the shards
**Priority:** P3 (Low)
**Type:** Operations / CI
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** ST-40 (BLG-OPS-105), EPIC-06, cycle `2026-10-29__release-v9.14` — CI runtime audit `docs/ops/ci_runtime_audit_2026-10-30.md` §5 candidate 1 — 2026-10-30
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
Each of `playwright.yml`'s 8 E2E shards runs `CI=false PUBLIC_URL=/ npm run build` through `playwright.config.js`'s `webServer` before its first test. That build took about 45s per shard on 3 recent `main` runs, about 360 runner-seconds per run, and it sits on the critical path of every shard. The bundle is identical across shards.

**Scope**
- Add one build job that produces the E2E bundle (same `REACT_APP_*` env as `webServer.env`) and uploads it as an artifact
- Have each shard download it and run only `npx serve -s build -l 3000`; keep the local `npm start` path unchanged

**Acceptance Criteria**
- The 8 shards no longer run `npm run build`, and the E2E suite still passes in CI
- The before and after Playwright E2E wall time and runner time are recorded in `docs/ops/ci_runtime_audit_2026-10-30.md` or `ci_pipeline_baseline.md`

---

### BLG-QA-241 — Rebalance the Playwright shards: shard 1 sets the E2E critical path
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner; Head of Engineering
**Source:** ST-40 (BLG-OPS-105), EPIC-06, cycle `2026-10-29__release-v9.14` — CI runtime audit `docs/ops/ci_runtime_audit_2026-10-30.md` §5 candidate 2 — 2026-10-30
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
Playwright shards by file, and shard 1 holds `accessibility-axe-scan.spec.js` (73s), `chart-interactivity.spec.js` (60s) and `arc5-compliance-section.spec.js` (45s). Its summed test time was 385s against 202–338s for the other shards, and its test phase was 131s against a 68–90s mean elsewhere. Shard 1 (224s job) is therefore the critical path of the 235s E2E workflow.

**Scope**
- Split the two largest shard-1 specs (for example the axe scan's light and dark describe blocks into separate files), or turn on `fullyParallel` if the suite tolerates it
- Re-measure per-shard test time on 3 `main` runs

**Acceptance Criteria**
- The slowest shard's test phase is within 20% of the mean shard test phase on 3 `main` runs, recorded with run IDs
- No spec's scenarios are lost (the scenario count before and after is the same)

---

### BLG-QA-242 — Stub the backoff sleep in the retry tests instead of sleeping for real
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner; Backend Engineering Patterns Owner
**Source:** ST-40 (BLG-OPS-105), EPIC-06, cycle `2026-10-29__release-v9.14` — CI runtime audit `docs/ops/ci_runtime_audit_2026-10-30.md` §5 candidate 3 — 2026-10-30
**Effort:** XS (<0.5d)
**Provisional-Target:** TBD

**Problem**
Pytest Phase B's test phase was 79–89s on 3 recent `main` runs, and about 35s of it is real retry backoff: `test_gemini_claude_retry_backoff.py` (12.0s), `test_upstream_call_helper.py` (7.6s), `test_regime_retry_backoff.py` (6.5s), `test_alpaca_paper_sync_close_positions_backoff.py` (4.0s), `test_alpaca_paper_sync_idempotent_retry.py` (2.5s) and `test_retry_backoff.py` (2.0s). Single tests take exactly 1.5s or 3.0s, the configured backoff.

**Scope**
- Patch the sleep used by `bounded_upstream_call` and the other backoff helpers in these files (or a shared fixture), keeping assertions on the number of attempts and the delays requested

**Acceptance Criteria**
- The six files' summed Phase B time falls below 5s on a CI run, with the run ID recorded
- Each test still asserts the attempt count, and at least one asserts the requested backoff delays

---

### BLG-OPS-207 — Record the production Render invoice each month in the hosting cost trend
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** ST-38 (BLG-OPS-21), EPIC-06, cycle `2026-10-29__release-v9.14` — Arc 2 compute cost review `docs/ops/arc2_compute_cost_review.md` §6 recommendation 1 — 2026-10-30
**Effort:** XS (<1h per month)
**Provisional-Target:** TBD

**Problem**
The production Render dyno is the only recurring paid line Arc 2 compute runs on, but no dollar figure for it exists in the repository: production is dashboard-managed, and `render_hosting_cost_trend_dashboard_2026-08-21.md` uses an endpoint-count proxy. ST-39's cost-by-feature-area report allocates this charge, so it needs the real figure.

**Scope**
- Each month, read the Render invoice and append the month, plan and amount to `render_hosting_cost_trend_dashboard_2026-08-21.md` §3
- Pass the same amount as `--render-monthly-usd` when running `scripts/cost_by_feature_area.py`

**Acceptance Criteria**
- At least 2 consecutive months of invoiced Render amounts are recorded, each with its date read

---

### BLG-OPS-208 — Re-run the production database storage snapshot quarterly
**Priority:** P3 (Low)
**Type:** Operations / Capacity
**Owner:** Infrastructure & Operations Owner
**Source:** ST-38 (BLG-OPS-21), EPIC-06, cycle `2026-10-29__release-v9.14` — Arc 2 compute cost review `docs/ops/arc2_compute_cost_review.md` §6 recommendation 2 — 2026-10-30
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
Production runs on Supabase's Free plan (confirmed 2026-07-31), so storage growth, not dollars, is the database's limit. The only size reading is 16 MB on 2026-08-08 (`cloud_infra_spend_by_epic.md`). Since then `api_call_log` records every market-data call (v9.13) and the Arc 2 to Arc 5 tables have grown, with no second reading.

**Scope**
- Add a quarterly `schedule` to `db-storage-size-snapshot.yml` (it is `workflow_dispatch` only), or a calendar reminder, and run it now
- Append each reading, with the largest tables, to `cloud_infra_spend_by_epic.md`

**Acceptance Criteria**
- A second production size reading is recorded with its run ID, and the next quarterly run is scheduled

---

### BLG-OPS-209 — Log the nightly screener run's server-side duration
**Priority:** P3 (Low)
**Type:** Operations / Monitoring
**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner
**Source:** ST-38 (BLG-OPS-21), EPIC-06, cycle `2026-10-29__release-v9.14` — Arc 2 compute cost review `docs/ops/arc2_compute_cost_review.md` §6 recommendation 3 — 2026-10-30
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
The nightly screener batch (`POST /screener/run`) is the largest single compute job on the shared Starter dyno, but its only measured duration is the `screener-refresh.yml` workflow's wall time (37s mean, 80s max over 30 runs), which includes runner start-up and caps at the 120s `curl --max-time`. Without a server-side duration and ticker count per run, dyno headroom cannot be tracked as the ticker universe grows.

**Scope**
- Record each run's start, end, ticker count and market-data call count (for example in the screener run's result row or a structured log line)
- Add the median and maximum to the cost review when re-run

**Acceptance Criteria**
- Each `POST /screener/run` records its server-side duration and ticker count, and a test covers the recording

---

### BLG-OPS-210 — Choose an automated path for the monthly CI usage report's pull request
**Priority:** P3 (Low)
**Type:** Operations / CI
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Source:** PR #2133 review (EPIC-06, cycle `2026-10-29__release-v9.14`), ST-42 (BLG-OPS-188) — 2026-10-30
**Effort:** S (~0.5d)
**Provisional-Target:** TBD
**Depends on:** BLG-OPS-202 (first run on `main` confirmed)

**Problem**
After ST-42, `ci-usage-report.yml` commits each month's report to `ci-usage-report/<YYYY-MM>` and tries to open a PR to `main`. This repository does not let GitHub Actions create pull requests (`can_approve_pull_request_reviews: false`), so every month the run only prints a compare link. Even when a PR is opened with `GITHUB_TOKEN`, its required checks do not start until a person closes and reopens it. So each monthly report still needs three manual steps before it reaches `main`, and a missed month goes unnoticed.

**Scope**
- Decide between: allowing Actions to create PRs (repository setting), a GitHub App or fine-grained token with only `contents` and `pull-requests` on this repository, or keeping the manual step and adding a reminder when a report branch has no PR
- Record the decision and its security review in `docs/ops/scheduled_workflows_inventory.md`
- Apply the chosen path to `ci-usage-report.yml` and record the next scheduled run's result

**Acceptance Criteria**
- The decision and the Cybersecurity & Trust Lead's review of the token or setting are recorded
- The next scheduled `ci-usage-report.yml` run opens a PR whose required checks start without a manual close and reopen, or the manual path is documented with a reminder that fires when a report branch has no open PR

---

### BLG-QA-243 — Add pytest --durations output to the CI Pytest Suite
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality; Infrastructure & Operations Owner
**Source:** PR #2133 review (EPIC-06, cycle `2026-10-29__release-v9.14`), ST-40 (CI runtime audit) — 2026-10-30
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-40's AC names pytest `--durations` as the per-test timing source, but no CI workflow runs pytest with `--durations`. The audit (`docs/ops/ci_runtime_audit_2026-10-30.md` §4) therefore estimated per-file time from the gaps between consecutive `-v` result lines. Those gaps put fixture setup and teardown time on the next test, and the audit cross-checked them with one local `--durations` run. The next audit, and any check that BLG-QA-242 saved time, should be able to read the slowest tests straight from CI logs.

**Scope**
- Add `--durations=25` (or similar) to the CI Pytest Suite's pytest invocations
- Note the change in `docs/ops/ci_pipeline_baseline.md`

**Acceptance Criteria**
- A CI Pytest Suite run on `main` prints the slowest 25 tests with their setup, call and teardown times
- `ci_pipeline_baseline.md` says where to read per-test timing

---

### BLG-SEC-45 — Drop the unused allow_credentials flag from the API's CORS middleware
**Priority:** P3 (Low)
**Type:** Security / Configuration
**Owner:** Cybersecurity & Trust Lead; Backend Engineering Patterns Owner
**Source:** BLG-SEC-44 agent-mediated Cybersecurity & Trust Lead review of the staging CORS defaults (ST-43, EPIC-06, cycle `2026-10-29__release-v9.14`) — 2026-10-30
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`backend/main.py` configures `CORSMiddleware` with `allow_credentials=True`, which lets allowed origins send cookies and HTTP authentication with cross-origin requests. The frontend authenticates with an `X-API-Key` header (`src/api/base44Client.js`) and never sends cookies or uses `credentials: 'include'`, so the flag grants a capability nothing uses. Removing it narrows what an allowed origin can do if a cookie-based mechanism is ever added without a security review.

**Scope**
- Set `allow_credentials=False` (or remove it) in `backend/main.py`
- Update `tests/test_cors_allow_list.py`, which currently asserts the credentials header, and `docs/infrastructure/cors_allow_list.md`
- Confirm the Pages frontend still loads data after deploy

**Acceptance Criteria**
- A preflight from the Pages origin to production returns `200` with `access-control-allow-origin` and no `access-control-allow-credentials: true`, recorded with the date
- The Pages frontend loads data after the change, confirmed with the date

---

### BLG-BE-201 — Use the typographic minus in the monthly P&L summary fallback
**Priority:** P3 (Low)
**Type:** Backend / Copy
**Owner:** Financial Reporting & Records Owner; Frontend Specifications & UX Documentation Owner
**Source:** Sprint Execution, ST-26 (EPIC-04, cycle `2026-10-29__release-v9.14`), found while checking the §AI Summary template wording against the code — 2026-11-02
**Effort:** XS (<1h)
**Provisional-Target:** v9.15

**Problem**
The Monthly P&L summary's code-written fallback (`backend/services/monthly_pnl_narrative_service.py` `_money()`) writes a negative amount with an ASCII hyphen ("-£120.40"). `reports.md` §AI Summary's standard summary template and the v9.11 decision record say signed values use the canonical money format, which `design_system.md` §Number and Currency Formatting defines with the typographic minus U+2212 before the symbol ("−£120.40"). The fallback therefore disagrees with every other money figure on the page.

**Scope**
- Make `_money()` write U+2212 for negative values
- Confirm the §13 Condition 3 value check (`source_values` / `signed_money_values` and the parser that reads numbers from the text) still accepts the fallback, and accepts U+2212 in model output
- Update the expected template in `tests/test_monthly_pnl_narrative.py`

**Acceptance Criteria**
- The fallback for a month with a loss reads "−£120.40" (U+2212), asserted in `tests/test_monthly_pnl_narrative.py`
- The fallback text still passes the value check and the language scan (test)

---

### BLG-FE-237 — Stop the Reports tab bar and Monthly table overflowing at phone width
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Sprint Execution, ST-24 (EPIC-04, cycle `2026-10-29__release-v9.14`), found while hardening SC-MEC-07 at a 375px viewport after the agent-mediated DoQ review — 2026-11-02
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15

**Problem**
At a 375px viewport the Reports page scrolls sideways: `document.documentElement.scrollWidth` is 393 with no Monthly rows at all, because the tab bar's last button (`reports-tab-reconciliation`) ends at x=393. On the Monthly tab, the Monthly Realised P&L table also extends to x=426 inside a card with `overflow-hidden`, so the Avg P&L/Trade column is clipped rather than scrollable. Neither is caused by v9.14's exit-condition card, which scrolls inside itself.

**Scope**
- Let the Reports tab bar wrap or scroll inside itself at narrow widths
- Give the Monthly Realised P&L table the same `overflow-x-auto` treatment as the exit-condition card (sticky Month column optional)
- Add a 375px Playwright check

**Acceptance Criteria**
- At 375px on the Monthly tab, `document.documentElement.scrollWidth` ≤ 375 (Playwright)
- At 375px the Avg P&L/Trade column can be scrolled into view inside its card (Playwright)

---

### BLG-BE-202 — Reuse one connection for the monthly P&L exit-condition breakdown
**Priority:** P3 (Low)
**Type:** Backend engineering
**Owner:** Head of Engineering
**Source:** PR #2137 agent-mediated review (EPIC-04, cycle `2026-10-29__release-v9.14`), Director of Quality finding: ST-24 — 2026-11-02
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15

**Problem**
ST-24's `get_monthly_pnl_by_exit_reason()` (`backend/database.py`) opens its own `get_db()` connection, and `get_db()` is a fresh `psycopg2.connect` with no pool. A `GET /reports/monthly-pnl` request now opens three connections (month rows, snapshot check, breakdown), where ST-12 (v9.7, BLG-BE-126) bounded it at two. The ST-12 test (`tests/test_monthly_pnl_snapshot.py`, `get_db_mock.assert_called_once()`) did not catch this, because it patches only `reports_service.get_db` and the new query connects inside the stubbed `database` module. The rolling-window SQL clause is also now written out in three functions (`get_monthly_pnl`, `get_monthly_pnl_by_tax_year`'s sibling, and the new query), so the reconciliation guarantee depends on keeping them byte-identical by hand.

**Scope**
- Give `get_monthly_pnl_by_exit_reason()` an optional `conn` (as `get_monthly_pnl_snapshot()` has) and run it on a connection the report already holds
- Share the window clause between the month-row and breakdown queries so they cannot drift
- Extend the connection-count test to count connections opened by every database call in the request, not only `reports_service.get_db`

**Acceptance Criteria**
- A `GET /reports/monthly-pnl` request with closed months opens at most two connections in total (test)
- The month-row and breakdown queries take their window clause from one definition (code review), and `tests/test_monthly_pnl_exit_condition_breakdown.py` still passes

---

### BLG-GOV-401 — Count not-yet-initialised EPICs as pending in `check_execution_state_consistency.py`
**❌ Killed — 2026-11-03 — superseded by `BLG-QA-240` (duplicate: the same `check_execution_state_consistency.py` `merge_gate` defect, filed 2026-10-30 as `BLG-QA-240` and again 2026-11-02 at ST-44; `verification_report.md` §5 and `lessons_learnt_cycle.md` Phase 3 FI-1 direct the fold) — decision: Product Owner with the Head of Specs Team (agent-mediated per §5.3, user-directed 2026-11-03)**
**Priority:** P3 (Low)
**Type:** Governance Process / Tooling
**Owner:** Head of Specs Team; Head of Engineering
**Source:** Sprint Execution `2026-10-29__release-v9.14`, EPIC-07 STEP 0 / ST-44 (out-of-scope finding while editing the script) — 2026-11-02
**Effort:** XS (<1h)
**Provisional-Target:** v9.15

**Problem**
`scripts/check_execution_state_consistency.py` derives the expected `merge_gate.epics_pending` only from EPICs that already have an `epics.<EPIC-xx>` record. EPICs are initialised lazily at their own STEP 0, so mid-cycle any EPIC still listed in `merge_order`/`epics_pending` but not yet started is reported as unexpected, and the §9.2 read-back exits non-zero on a correct file. At v9.14 EPIC-07 STEP 0 it reported `merge_gate.epics_pending: expected ['EPIC-07'], found ['EPIC-05', 'EPIC-07']` (and `expected []` before EPIC-07 was initialised). A read-back that always fails mid-cycle trains readers to ignore it.

**Scope**
- Treat an EPIC named in `merge_order` (or already in `epics_pending`) that has no `epics.<EPIC-xx>` record as pending
- Add a test for a state with an uninitialised EPIC in `merge_order`

**Acceptance Criteria**
- The script exits 0 on a consistent mid-cycle state whose later EPICs are listed in `merge_order` but not yet initialised
- It still fails, naming the field, when an initialised unmerged EPIC is missing from `epics_pending`
- A unit test covers the uninitialised-EPIC case

---

### BLG-FE-238 — Add `aria-expanded` and `aria-controls` to the SI-02 Gate Status toggle
**Priority:** P3 (Low)
**Type:** Frontend / UX (Accessibility)
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Source:** Sprint Execution `2026-10-29__release-v9.14`, EPIC-07 / ST-46 (out-of-scope finding while documenting the gate-status indicator pattern) — 2026-11-02
**Effort:** XS (<1h)
**Provisional-Target:** v9.15

**Problem**
The collapse toggle of `SI02GateStatusSection` (`src/pages/Reports.js`) is a `<button>` but sets neither `aria-expanded` nor `aria-controls`, so a screen reader user is not told whether the section is open. `docs/specs/frontend/patterns/gate_status_indicator.md` (ST-46) now requires both for any gate status indicator and names this component as its reference implementation, so the reference does not meet its own pattern.

**Scope**
- Set `aria-expanded={!collapsed}` on the toggle and `aria-controls` pointing at an `id` on the section body
- Extend `tests/e2e/reports-si02-gate-status.spec.js` SC-SI02-01 to assert `aria-expanded` before and after the click

**Acceptance Criteria**
- The toggle reports `aria-expanded="false"` collapsed and `"true"` expanded, and `aria-controls` names the body element's `id` (Playwright)
- `gate_status_indicator.md` §Accessibility item 2 drops its "reference does not set either yet" note

---

### BLG-GOV-402 — Footnote the corrected v9.1–v9.5 and v9.3–v9.7 effort-weighted readings in `product_value_ratio_history.md`
**Priority:** P3 (Low)
**Type:** Governance Process / Metrics record
**Owner:** Head of Specs Team; Metrics Definitions & Analytics Owner
**Source:** Sprint Execution `2026-10-29__release-v9.14`, EPIC-07 / ST-48 (out-of-scope finding: the corrected readings live in a `claude/roadmap/*` file the story's AC does not name) — 2026-11-02
**Effort:** XS (<1h)
**Provisional-Target:** v9.15

**Problem**
ST-48 fixed `scripts/compute_effort_weighted_pvr.py`'s parse of band parentheticals: it read any number in the note, so `XS (~15min)` (v9.5) weighed 15 days and `M (~2 days, 3 small sub-items)` weighed 2.5. The two backfilled readings these stories fall in were wrong: v9.1–v9.5 is 0.024, not 0.021, and v9.3–v9.7 is 0.104, not 0.093. `metrics_definitions.md` Appendix F now carries the corrected values, but `claude/roadmap/product_value_ratio_history.md` rows `2026-09-19__scheduled` and `2026-09-28__scheduled` still record 0.021 and 0.093. That file is append-only, so the rows must not be rewritten, but Appendix F's own rule (2) asks for known staleness to be footnoted rather than left silent.

**Scope**
- At the next `run roadmap` (STEP 2.4), add a dated footnote beneath the History table naming both rows, the old and corrected effort-weighted readings, and ST-48 as the cause. Do not edit the rows themselves

**Acceptance Criteria**
- `product_value_ratio_history.md` has a footnote stating 0.021 → 0.024 (v9.1–v9.5) and 0.093 → 0.104 (v9.3–v9.7), citing ST-48 / `BLG-SPEC-191`
- The two History rows are unchanged

---

### BLG-FE-239 — Trade History counts a break-even trade as a win
**Priority:** P2 (Medium)
**Type:** Frontend / Correctness
**Owner:** Metrics Definitions & Analytics Canonical Owner; Frontend Specifications & UX Documentation Owner
**Source:** Sprint Execution `2026-10-29__release-v9.14`, EPIC-07 / ST-50 (win rate surface consistency check, `docs/specs/metrics/win_rate_surface_consistency_2026-11-02.md`) — 2026-11-02
**Effort:** XS (<1h)
**Provisional-Target:** v9.15
**Owner ruling (2026-11-03, Metrics Definitions & Analytics Owner):** a `pnl = 0` trade belongs in neither Avg Win nor Avg Loss, nor in the W or L count (§Win Rate, §Risk/Reward Ratio; `metrics_definitions.md` v1.34.2 Appendix E Backlog Item 3). This answers the Scope's first bullet.

**Problem**
`src/pages/TradeHistory.js` computes its summary win rate with `winningTrades = filteredTrades.filter((t) => t.pnl >= 0)`. `metrics_definitions.md` §Win Rate counts a win only when `pnl > 0`, and every other surface (analytics, P&L report, Performance Analytics) follows it. When the filtered set contains a trade with `pnl = 0`, the Trade History win rate is higher than the one the same trades show elsewhere, and the zero is averaged into Avg Win.

**Scope**
- Change the win test to `t.pnl > 0`, matching §Win Rate, and decide (with the owner) whether `pnl = 0` belongs in Avg Loss or neither
- Add a Playwright case with one break-even trade asserting the summary win rate

**Acceptance Criteria**
- With trades of P&L +10, 0 and −10, the Trade History summary shows a 33.3% win rate (Playwright)
- The page's win test matches `metrics_definitions.md` §Win Rate

---

### BLG-FE-240 — Dashboard win-rate widgets are fed from open positions only
**Priority:** P2 (Medium)
**Type:** Frontend / Correctness
**Owner:** Metrics Definitions & Analytics Canonical Owner; Frontend Specifications & UX Documentation Owner
**Source:** Sprint Execution `2026-10-29__release-v9.14`, EPIC-07 / ST-50 (win rate surface consistency check, `docs/specs/metrics/win_rate_surface_consistency_2026-11-02.md`) — 2026-11-02
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.15

**Problem**
`src/pages/Dashboard.js` builds `closedPositions` by filtering `GET /positions` for `status = "closed"`, but that endpoint returns open positions only, so the list is always empty. The `win_rate` widget (`WinRateWidget`) therefore always shows 0%, and the `win_rate_chart` widget is rendered as `<WinRateChart trades={closedPositions} />` although `WinRateChart.js` reads `winRate`, `wins` and `losses` props, so it renders from undefined values. Both are user-selectable dashboard widgets.

**Scope**
- Feed both widgets from closed trades (e.g. the `GET /trades` summary `win_rate`, or `trade_history` rows), computed per `metrics_definitions.md` §Win Rate
- Pass `WinRateChart` the props it reads
- Playwright coverage of both widgets with closed trades present

**Acceptance Criteria**
- With closed trades of P&L +10 and −10, both widgets show 50% (Playwright)
- Neither widget reads `GET /positions` for closed trades

**Notes:** 2026-11-04 (ST-12, EPIC-02, v9.15): the defect leaves with the page. ST-12 removed `src/pages/Dashboard.js` with `WinRateWidget` and `WinRateChart`, which it alone rendered; the Dashboard home renders no win-rate widget, so no surface carries this defect. ST-16 was deferred at planning as superseded by ST-12 (`sprint_backlog.md` Items Deferred This Sprint).

---

### BLG-SPEC-212 — Strategy version comparison contract defines `win_rate` by R, the code by P&L
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner; Metrics Definitions & Analytics Canonical Owner
**Source:** Sprint Execution `2026-10-29__release-v9.14`, EPIC-07 / ST-50 (win rate surface consistency check, `docs/specs/metrics/win_rate_surface_consistency_2026-11-02.md`) — 2026-11-02
**Effort:** XS (<1h)
**Provisional-Target:** v9.15

**Problem**
`GET /analytics/strategy-version-comparison`'s contract (`docs/specs/api_contracts/analytics_endpoints.md`) defines `win_rate` as the "proportion of trades that closed positive (R > 0)". The code (`backend/database.py`, the version-window `_fetch`) counts `pnl > 0` over all closed trades, including those with no determinable R, which matches `metrics_definitions.md` §Win Rate. The field is also a 0.0–1.0 proportion, unlike the canonical percentage, which the contract states but `metrics_definitions.md` does not mention.

**Scope**
- Correct the contract's `win_rate` definition to `pnl > 0` over all closed trades in the window, citing §Win Rate, and keep the 0.0–1.0 scale note
- Add a one-line note to `metrics_definitions.md` §Win Rate naming this endpoint's proportion scale

**Acceptance Criteria**
- The contract's `win_rate` definition matches the code and §Win Rate
- §Win Rate names the endpoint's 0.0–1.0 scale

---

### BLG-GOV-403 — Wire the spec debt aging report into Release Planning §1.1 or `groom backlog`
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Sprint Execution `2026-10-29__release-v9.14`, EPIC-07 / ST-54 (`BLG-GOV-191` scope split: "wiring it into a governance prompt is filed separately") — 2026-11-02
**Effort:** XS (~0.25 day)
**Provisional-Target:** v9.15

**Problem**
`scripts/report_spec_debt_aging.py` (ST-54) lists open `BLG-SPEC-*` items by release cycles without a story, the measure `release_planning_prompt.md` §1.1 warns on. No prompt runs it, so §1.1 is still applied by hand and only to items already in the release's slice. The first recorded run (`docs/governance/spec_debt_aging_report_2026-11-02.md`) found 13 ungated items at or over the threshold.

**Scope**
- Choose where the report runs: `release_planning_prompt.md` §1.1 (replace the by-hand count) or a standing `groom backlog` step, or both
- Close the two estimation gaps ST-54 disclosed: per-item ready-pool membership is not recorded, so the script counts every release cycle on or after filing (gated items flagged); and a cycle starting on the filing date is counted, which can overstate by one. Either record ready-pool membership per item at Release Planning §1.4c, or keep the estimate and state it in the prompt
- Apply the choice with the CLAUDE.md §6 checklist

**Acceptance Criteria**
- The chosen prompt names `scripts/report_spec_debt_aging.py` and what to do with its ⚠ rows
- The next run of that engine records the report's ⚠ count in its manifest

---

### BLG-SPEC-213 — Effort-weighted PVR weighs every hour-scale estimate at 0.15 days, including `M (~10 hrs)`
**Priority:** P3 (Low)
**Type:** Spec Debt (metric definition)
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** PR #2138 agent-mediated review (Director of Quality), EPIC-07 / ST-48 of `2026-10-29__release-v9.14` — 2026-11-02
**Effort:** XS (<1h)
**Provisional-Target:** Unscheduled (latent; see Problem)

**Problem**
ST-48 made `metrics_definitions.md` Appendix F and `scripts/compute_effort_weighted_pvr.py` agree that a band whose parenthetical starts with an hour- or minute-scale quantity weighs 0.15 days, whatever the number. That is right for `XS (<1h)` but not for larger hour estimates: `S (~3 hrs)` (9 uses), `S (~4 hrs)` (12), `S (~5 hrs)` (6) and `M (~10 hrs)` (6) would all weigh 0.15, although 10 hours is more than a day. Every such value is in a v2.1–v6.8 sprint backlog, outside the five backfilled windows and any rolling window STEP 2.4 now reads (recent cycles state effort as numeric days), so no recorded or upcoming reading is affected. The defect is latent: it matters only if a window over those cycles is computed, or if hour-scale estimates return. A minute value written `~30m` is also not recognised (only `min`/`mins`/`minutes`), so it takes the band midpoint.

**Scope**
- Change the hour-scale row to convert hours to days (e.g. hours ÷ 8, minimum 0.15) and accept `m` as minutes; update the script and table together
- Update `tests/test_compute_effort_weighted_pvr.py` with `M (~10 hrs)`, `S (~4 hrs)` and `XS (~30m)` cases
- Appendix D changelog row

**Acceptance Criteria**
- `M (~10 hrs)` weighs 1.25 days and `XS (<1h)` still weighs 0.15 (tests)
- Appendix F's table and the script still weight exactly the same values (parity test passes)
- The five backfilled readings are unchanged on re-run

---

### BLG-FE-241 — Show a failed Positions-page exit inside the Exit modal, as the Monitor queue does
**Priority:** P3 (Low)
**Type:** Frontend / UX (error handling)
**Owner:** Frontend Specifications & UX Owner
**Source:** Sprint Execution, ST-29 / EPIC-05 of `2026-10-29__release-v9.14` (writing the Positions-page Exit modal Playwright coverage, `tests/e2e/positions-exit-modal.spec.js`) — 2026-11-02
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`src/pages/Positions.js`'s `handleExit` calls `exitMutation.mutate()` and returns nothing. So ExitModal's promise path (v9.13 ST-01) never runs on the Positions page. That path shows "Exiting…" while the request is in flight, and on failure an inline `role="alert"` `exit-error` block ("Could not record the exit for {ticker}. Nothing was changed for this position." plus the API `detail`). Instead, a failed exit on the Positions page shows `window.alert("Failed to exit position: <detail>")`; the modal does stay open. The Daily Position Monitor path uses the inline error, so the two surfaces report the same failure differently. Because the Positions modal has no in-flight state, a second click on Confirm Exit can also send a second exit request.

**Scope**
- Return `exitMutation.mutateAsync(exitData)` from `handleExit` and drop the `onError` alert for this path, so the modal shows the inline error and the in-flight state
- Update `tests/e2e/positions-exit-modal.spec.js` SC-PEM-02 to assert the `exit-error` block instead of the alert

**Acceptance Criteria**
- On the Positions page, a failed exit keeps the modal open with the `exit-error` block showing the API `detail`, and no `window.alert` appears
- Confirm Exit reads "Exiting…" and is disabled while the request is in flight
- SC-PEM-02 asserts both and passes in CI

---

### BLG-FE-242 — Give the Trade History filter fields and Exit dialog fields a light-theme fill
**Priority:** P3 (Low)
**Type:** Frontend / UX (light-theme contrast)
**Owner:** Frontend Specifications & UX Owner
**Source:** Sprint Execution, ST-30 / EPIC-05 of `2026-10-29__release-v9.14` (staging visual check of the tailwind-merge `cn()` change, before/after screenshots of `2f5cc56a~1` and `42bec3ce`); Product Owner chose to backlog rather than fix in-sprint — 2026-11-02
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
Since `cn()` runs `tailwind-merge` (v9.13 ST-25, `2f5cc56a`), a caller's `bg-slate-800/50` now beats the input and select default `bg-transparent`. The Trade History saved-filter picker, the Trade History filter selects and date inputs, and the Exit Position dialog fields all set this fill with no light-theme pair, so the light theme renders a dark fill. On the saved-filter picker the placeholder text "No saved filters" (`#737373`) measures 1.45:1 against that fill, down from 4.32:1 before the change (axe `color-contrast`, light theme). This is the dark-only-token defect class `design_system.md` warns about (BLG-FE-87/88/95).

**Scope**
- Replace the bare `bg-slate-800/50` on these fields with an explicit light+dark pair from `design_system.md` §Light-Theme Colour Tokens, with a light-theme text colour that meets 4.5:1 on it
- Sites: the saved-filter picker in `src/components/trades/SavedFiltersControl.js`; the Trade History filter selects and date inputs; the Exit Position dialog inputs, Exit Reason select and note field
- Add a light-theme axe `color-contrast` check of Trade History to `tests/e2e/accessibility-axe-scan.spec.js` that covers the saved-filter picker

**Acceptance Criteria**
- In the light theme, "No saved filters" and every Trade History filter field meet 4.5:1 text contrast (axe `color-contrast` passes for those elements)
- The dark theme is unchanged: the fields keep the `bg-slate-800/50` fill
- The new light-theme Trade History scan passes in CI

---

### BLG-FE-243 — Default trade, exit and cash dates to the user's local date, not the UTC date
**Priority:** P2 (Medium)
**Type:** Frontend / UX (date handling)
**Owner:** Frontend Specifications & UX Owner
**Source:** PR #2139 review (EPIC-05 of `2026-10-29__release-v9.14`, reviewing ST-29's `positions-exit-modal.spec.js`, which asserts the same UTC expression the app uses) — 2026-11-02
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15 (retargeted 2026-11-03 from TBD, PMO Lead with the item owners, user-directed; post-ship closure `2026-10-29__release-v9.14` §6 row 5)

**Problem**
The Exit Position dialog (`src/components/positions/ExitModal.js:31,56`), Trade Entry (`src/pages/TradeEntry.js:41`) and Cash Management (`src/components/cash/CashManagementModal.js:57`) prefill their date with `new Date().toISOString().split("T")[0]`. That is the UTC date, not the user's local date. For a UK user between 00:00 and 01:00 BST, every one of these forms prefills yesterday's date. An exit or entry saved without correcting it lands on the wrong day: holding days and grace-period day counts are off by one, and an exit just after midnight on 6 April falls in the previous UK tax year.

**Scope**
- Add one shared helper that returns today's date as `YYYY-MM-DD` in the browser's local timezone, and use it for the four prefill sites above
- Check the other `toISOString().split` date uses (`Dashboard.js` peak date, `ExportModal.js`, `PortfolioGrowthChart.js`, `RedFlagsCard.js`, `base44Client.js`, `SystemStatus.js`) and switch any that mean "today for the user"
- Update `tests/e2e/positions-exit-modal.spec.js` SC-PEM-01, which asserts the UTC expression, to assert the local date. Add a Playwright case under `timezoneId: 'Europe/London'` with the clock set to 00:30 BST that checks the Exit, Trade Entry and Cash Management date fields prefill the local date

**Acceptance Criteria**
- At 00:30 BST under Europe/London, the Exit dialog, Trade Entry and Cash Management date fields prefill the local date, not the previous day
- The new Playwright case passes in CI
- No user-facing "today" date in `src/` comes from `toISOString().split("T")[0]`

---

### BLG-GOV-404 — Gate scan treats a shipped roadmap feature ID (PT-xx, SI-xx, PO-xx) as a met gate
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** Head of Specs Team; PMO Lead
**Source:** Post-ship closure `2026-10-29__release-v9.14` STEP 8 — deferred lessons-learnt action, Release Planning Friction Item 2 (`LL-v9.14-Release-02`); script change outside the closure write scope, so filed with a sprint target (`LL-v9.12-Release-01`) — 2026-11-03
**Effort:** S (~0.5d)
**Provisional-Target:** v9.15

**Problem**
`scripts/scan_backlog_gate_conditions.py` detects only `BLG-*` IDs in gate text, so a gate on a roadmap feature ID is never reported as met. `BLG-FE-39`, `BLG-QA-21`, `BLG-QA-22`, `BLG-QA-23` and `BLG-GOV-26` are gated only on "PT-04 shipped" (shipped v6.1, 2026-06-23), and `BLG-FEAT-26` has the same limb, so they have sat gated for 18 releases. `release_planning_prompt.md` §1.3a's "gating item shipped" write-back (v2.66) cannot clear a gate the scan never reports.

**Scope**
- Treat a roadmap feature ID (PT-xx, SI-xx, PO-xx) as shipped when `claude/roadmap/current_roadmap.md` or `roadmap_archive.md` marks it ✅ Shipped/Complete
- Report such gates in the "gating item shipped — verify" list so the §1.3a write-back can clear them
- Add tests for a shipped and an unshipped feature ID

**Acceptance Criteria**
- A gate reading "PT-04 shipped" is reported as gating item shipped (test)
- A gate on an unshipped feature ID is not reported (test)
- The six items named above appear in the scan output on the live backlog

---

---

<!-- UX programme "Site Structure & Usability" — filed by roadmap rebalance 2026-11-03__scheduled (DL-088) from IW-20261103-01. Phase 1 = v9.15 (Now), Phase 2 = v9.16, Phase 3 = v9.17, close-out re-review = v9.18. -->

### BLG-FE-244 — Show the pre-entry checks on every route into Trade Entry, not only from a Trade Plan
**Priority:** P1 (High)
**Type:** Frontend / UX (strategy integrity) [U]
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Source:** IDEA-head-of-ux-20261103-01 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088 — STEP 8.0 Correctness Fast-Track. Strategy Rules & System Intent Owner confirmation (in session, 2026-11-03): §4.2 applies to every manual entry, planned or not; display-only.
**Effort:** M (~2-3 days)
**Provisional-Target:** v9.15
**Related:** `BLG-FE-54` (gated Arc 5 gateway exploration — keeps its gate; this item delivers the unchecked-path slice now)

**Problem**
The §4.2 pre-entry advisory checks (regime gate incl. §4.2.1 unknown regime, sector concentration, earnings proximity, cash, sizing validity) run only on `src/pages/TradePlan.js` (Pre-Entry Checks panel, `EntryChecklist`, acknowledgement box). The sidebar "Trade Entry" link, the Positions "New Position" button and the `n` shortcut (Positions and Trade History, `src/Layout.js` global key handler) open `src/pages/TradeEntry.js`, which runs none of them. An entry in a risk-off or unknown-regime market can be recorded without the gate being shown.

**Scope**
- When Trade Entry is opened without a linked Trade Plan that already passed its checks, show the same pre-entry check panel and acknowledge-to-proceed step the plan uses, reusing the existing validation endpoint and components
- Plan-linked entries keep their current flow
- Record overrides from this path the same way the plan path does, so the Red Flag Journal and SI-05 digest count them
- No new check logic and no automatic blocking beyond what §4.2 already defines

**Acceptance Criteria**
- From each of the three routes (sidebar, "New Position", `n`), Trade Entry shows the pre-entry check results before save
- With a risk-off or unknown regime for the selected market, the regime check shows its FAIL/unknown state and save requires the acknowledgement
- A plan-linked entry does not show the panel twice
- Playwright coverage for each of the above passes in CI

---

### BLG-FE-245 — Pre-fill Trade Entry's FX rate from the live rate, not a fixed 1.27
**Priority:** P1 (High)
**Type:** Frontend / correctness (sizing) [U]
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20261103-02 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088 — STEP 8.0 Correctness Fast-Track
**Effort:** S (~0.5-1 day)
**Provisional-Target:** v9.15

**Problem**
`src/pages/TradeEntry.js:45` and `:213` pre-fill the FX field with `"1.27"` for US trades. The Exit dialog already uses `position.live_fx_rate` (`ExitModal.js:54`), and the backend serves the live or last-good rate with source and age (`BLG-BE-194`). Since `BLG-BE-190` (§4.1.3 v1.21) US share counts scale with FX², so an untouched default distorts the suggested size (about 13% at FX 1.35) and the recorded GBP cost.

**Scope**
- Pre-fill from the live (or last-good) rate the backend already serves; show its source and age next to the field; keep it editable
- Fall back to the backend's flagged fallback only when no rate is available, and say so

**Acceptance Criteria**
- With a mocked live rate of 1.35, a new US entry pre-fills 1.35 with its source and age shown
- With no rate available, the field shows the fallback and a visible "fallback rate" note
- No `"1.27"` literal remains in `TradeEntry.js`
- Playwright coverage passes in CI

---

### BLG-FE-246 — Label the FX rate the same way on entry and exit
**Priority:** P2 (Medium)
**Type:** Frontend / UX (terminology, correctness risk) [U]
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20261103-01 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.15

**Problem**
The same quantity (USD per £1, §4.1.3 v1.21) is labelled "FX Rate (USD/GBP)" on Trade Entry (`TradeEntry.js:475`) and "FX Rate (GBP/USD)" on the Exit dialog (`ExitModal.js:380`). A label that flips direction invites an inverted input.

**Scope**
- One label on every FX input: "FX rate — USD per £1 (GBP/USD)", with a one-line hint
- Grep `src/` for other FX input labels and align them

**Acceptance Criteria**
- Every FX input label in `src/` uses the same wording
- Code review of the static label text is sufficient (wording-only AC, FI-P3-02)

---

### BLG-FE-247 — Remove the legacy widget Dashboard route and its duplicate command-palette entry
**Priority:** P3 (Low)
**Type:** Frontend / navigation clean-up [U]
**Owner:** Head of Engineering
**Source:** IDEA-head-of-ux-20261103-03 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.15

**Problem**
`src/pages/Dashboard.js` (the pre-v7.3 widget dashboard) is still routed at `/Dashboard`, and `src/components/CommandPalette.js` `PAGE_LABELS` lists both `DashboardHome` and `Dashboard` as "Dashboard", so the palette shows two identical entries. Open items reference it (`BLG-FE-240`).

**Scope**
- Confirm no live surface links to `/Dashboard` and that `BLG-FE-240`'s fix belongs on `DashboardHome` instead (update that item's scope note if so)
- Remove the route, the page and its palette label; redirect `/Dashboard` to `/`
- Remove components used only by the legacy page

**Acceptance Criteria**
- The command palette shows exactly one "Dashboard" entry
- `/#/Dashboard` lands on the Dashboard home page
- CI passes with the legacy page's specs removed or retargeted

---

### BLG-FE-248 — Use one name per page and action across sidebar, page headings and command palette
**Priority:** P2 (Medium)
**Type:** Frontend / UX (terminology) [U]
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20261103-01 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** S (~1 day)
**Provisional-Target:** v9.15
**Depends on:** `BLG-SPEC-214` (UI-label section of `docs/reference/glossary.md`)

**Problem**
Seven pages carry different names in the sidebar, the page heading and the command palette (e.g. Analytics / "Performance Analytics" / "Performance Analytics Report"; Trade Entry / "Enter New Position" / "New Position" button / "New trade" shortcut; Reflections / "Trade Reflections" / "Trade Reflection"; Signals / "Monthly Signals"; Replay / "Replay Mode"; Notifications / "Alert History"). "Trade" and "position" name the same act.

**Scope**
- Apply the glossary's canonical labels to `NAV_GROUPS` (`Layout.js`), every `PageHeader` title, `CommandPalette.js` `PAGE_LABELS`, primary buttons and the shortcut legend
- Add Replay and Notifications to the palette labels

**Acceptance Criteria**
- For every page, sidebar label = page heading = palette label (or the glossary records the deliberate difference)
- Existing nav/palette Playwright specs updated and passing

---

### BLG-FE-249 — Set a browser-tab title for each page
**Priority:** P3 (Low)
**Type:** Frontend / wayfinding [U]
**Owner:** Head of Engineering
**Source:** IDEA-head-of-ux-20261103-03 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.15

**Problem**
No page sets `document.title`; every tab reads "Position Manager" (`public/index.html`), so several open tabs cannot be told apart.

**Scope**
- Set `<page label> · Position Manager` from the layout using the glossary label; Research pages include the ticker

**Acceptance Criteria**
- Each routed page sets a distinct title; a Playwright check covers three pages

---

### BLG-SPEC-214 — Navigation spec v2: job-based areas, plus a UI-label section in the glossary
**Priority:** P2 (Medium)
**Type:** Spec / UX design
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-03, IDEA-frontend-specs-20261103-01 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2 days)
**Provisional-Target:** v9.15

**Problem**
`docs/specs/frontend/pages/navigation.md` v1.7 groups 18 entries by feature type (Trading, Analytics, Tools, System), collapses 3 groups by default, and omits Trade Plans and Research. The v8.5 exploration (`claude/cycles/2026-08-08__release-v8.5/st15_nav_bar_redesign_exploration.md`) kept the sidebar pattern on real-estate grounds but did not assess grouping, labels or discoverability. `docs/reference/glossary.md` has no UI-label section.

**Scope**
- Revise `navigation.md`: about five job-based areas (Today · Portfolio · Find trades · Review · Settings), item placement for all 25 pages, default-expanded groups, Trade Plans and Research surfaced, legacy Dashboard removed, parent links for detail pages, onward-link rule for every page, browser-tab title rule
- Add a UI-label section to `glossary.md`: one canonical label per page and primary action, and "trade" vs "position" usage
- Keep the collapsible-sidebar pattern (per the v8.5 recommendation)

**Acceptance Criteria**
- `navigation.md` revised (version bumped) and `glossary.md` gains the UI-label section, both reviewed by the Head of UX & Design
- Every page in `src/pages/` has a placement and a canonical label

---

### BLG-SPEC-215 — Dashboard spec: a prioritised "Today" action list
**Priority:** P2 (Medium)
**Type:** Spec / UX design
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-02 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2 days)
**Provisional-Target:** v9.15

**Problem**
`docs/specs/frontend/pages/dashboard.md` v3.10 specifies 13 blocks of near-equal weight; the regime sits in row 4 (Signal Status) and a quiet day shows 11 empty-state boxes. The page reports status rather than the decisions due.

**Scope**
- Revise `dashboard.md` (Class 1, Head of Specs Team approval): a "Today" list first — regime per market, then exits and stop changes due, then qualifying entries — each item linking to its action (reusing `/Positions?exit=<id>` and similar deep links); a single-line quiet-day state; status cards, What's New and gate progress below
- Define ordering, empty, loading and error states, and which existing cards move or merge

**Acceptance Criteria**
- `dashboard.md` revised and approved; every observable behaviour has a testable AC for `BLG-FE-254`

---

### BLG-SPEC-216 — Spec for one Journal area combining reflections, red flags and position notes
**Priority:** P3 (Low)
**Type:** Spec / UX design
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-05 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2 days)
**Provisional-Target:** v9.15

**Problem**
Journaling is split across Trade Reflections (`TradeReflection.js`), the Red Flag Journal (`RedFlagJournal.js`) and the Journal view inside Positions (which retitles the page "Trade Journal"). None links to the others.

**Scope**
- Specify one Journal area: sections or filters for reflections, red flags and position notes; routes and redirects for the old pages; what happens to the Positions journal view
- Strategy Rules & System Intent Owner confirms the merge moves no §13 boundary for AI-summarised journal surfaces (PO-02 roster rows)

**Acceptance Criteria**
- Spec filed and approved; §13 confirmation recorded; ACs ready for `BLG-FE-258`

---

### BLG-FE-250 — Build the job-based sidebar and surface Trade Plans and Research
**Priority:** P2 (Medium)
**Type:** Frontend / navigation [U]
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-03 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2-3 days)
**Provisional-Target:** v9.16
**Depends on:** `BLG-SPEC-214`

**Problem**
`NAV_GROUPS` in `src/Layout.js` holds 18 entries in 4 type-based groups, 3 collapsed by default; Trade Plans has no sidebar entry and is reachable only through the command palette.

**Scope**
- Implement `navigation.md` v2's areas, placement and default-expanded groups on desktop and the mobile drawer
- Add Trade Plans and Research entry points

**Acceptance Criteria**
- Sidebar matches `navigation.md` v2 on desktop and mobile
- Trade Plans is reachable from the sidebar in one click
- `alert-nav-badge.spec.js`, `command-palette.spec.js`, `keyboard-shortcuts.spec.js` updated and passing

---

### BLG-FE-251 — Add a parent link on detail pages
**Priority:** P3 (Low)
**Type:** Frontend / wayfinding [U]
**Owner:** Head of Engineering
**Source:** IDEA-head-of-ux-20261103-03 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** S (~1 day)
**Provisional-Target:** v9.16
**Depends on:** `BLG-SPEC-214`

**Problem**
Trade Plan, Research (`/research/:ticker`), Notification Preferences and Notification History have no link back to their parent page; the user relies on the browser's back button.

**Scope**
- A parent link (or breadcrumb) on each detail page per `navigation.md` v2

**Acceptance Criteria**
- Each listed page shows a parent link that navigates correctly; Playwright coverage passes

---

### BLG-FE-252 — Give each dead-end page an onward next-step link
**Priority:** P3 (Low)
**Type:** Frontend / wayfinding [U]
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-03 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2 days)
**Provisional-Target:** v9.16
**Depends on:** `BLG-SPEC-214`

**Problem**
Eight pages have no link to any other page: Reports, Red Flag Journal, Trade Reflections, Replay, Strategy Benchmark, Ticker Universe, System Status, Notification History (inter-page link scan, 2026-11-03).

**Scope**
- Add the onward link(s) `navigation.md` v2 assigns to each (e.g. Red Flag Journal → the flagged trade; Reports → Performance detail; Ticker Universe → Screener)

**Acceptance Criteria**
- A re-run of the inter-page link scan finds 0 dead-end pages; each new link has Playwright coverage

---

### BLG-FE-253 — Anchor the digest's Risk Dashboard link to the right section
**Priority:** P3 (Low)
**Type:** Frontend / wayfinding [U]
**Owner:** Head of Engineering
**Source:** IDEA-head-of-ux-20261103-03 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088; `docs/ux/si05_user_journey_map.md` F-04
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.16

**Problem**
The SI-05 digest's Risk Dashboard link lands at the top of `RiskDashboard.js`; for "Top rule breach" the user must find the pre-entry validation section by hand (journey map F-04, unfiled until now).

**Scope**
- Support a section query (e.g. `?section=pre-entry-validation`) that scrolls to the section; use it in the digest's deep link

**Acceptance Criteria**
- Opening the section link scrolls the named section into view; Playwright coverage passes; digest link updated

---

### BLG-FE-254 — Build the "Today" action list on the Dashboard
**Priority:** P2 (Medium)
**Type:** Frontend / UX [U]
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-02 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** L (~3-4 days)
**Provisional-Target:** v9.16
**Depends on:** `BLG-SPEC-215`

**Problem**
See `BLG-SPEC-215`: `DashboardHome.js` shows 13 equal-weight blocks, the regime in row 4 and 11 empty-state boxes on a quiet day.

**Scope**
- Implement `dashboard.md`'s revised "Today" list, ordering, quiet-day state and the moved/merged cards

**Acceptance Criteria**
- Every observable AC in the revised `dashboard.md` has Playwright coverage that passes, in light and dark themes

---

### BLG-FE-255 — Add "Plan this" to Signals and Screener rows
**Priority:** P2 (Medium)
**Type:** Frontend / UX (entry journey) [U]
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-04 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2-3 days)
**Provisional-Target:** v9.16
**Related:** `BLG-FE-54` (keeps its Arc 5 gate)

**Problem**
From a signal to an entered, checked trade takes 5 pages (Signals → Add to Watchlist → Watchlist → Research → Trade Plan → Trade Entry). Signals rows offer only "Add to Watchlist"; Screener rows offer Research or watchlist only (`Screener.js:525–532`).

**Scope**
- A "Plan this" action on Signals and Screener rows that opens Trade Plan pre-filled with ticker, market, price and signal context (`SignalContextPanel` already exists)

**Acceptance Criteria**
- From a Signals row and a Screener row, "Plan this" opens a pre-filled Trade Plan in one click; Playwright coverage passes

---

### BLG-FE-256 — On Trade Plan, show the suggested size before asking for shares
**Priority:** P2 (Medium)
**Type:** Frontend / UX (sizing) [U]
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Source:** IDEA-head-of-ux-20261103-04 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** S (~1 day)
**Provisional-Target:** v9.16

**Problem**
`TradePlan.js` asks for "Planned Shares (for pre-entry checks)" (line 976) before showing the §4.1 suggested size (`WhatIfSizingPreview`, line 1215), so the user types a number the system could suggest.

**Scope**
- Show the §4.1 suggested size above the shares field and pre-fill the field from it once entry and stop are known; keep it editable

**Acceptance Criteria**
- With entry and stop entered, the shares field pre-fills with the §4.1 suggestion; Playwright coverage passes

---

### BLG-FE-264 — Semantic colour tokens for the base, card and table shells
**Priority:** P2 (Medium)
**Type:** Frontend / design system [U]
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Source:** IDEA-frontend-specs-20261103-03 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2-3 days)
**Provisional-Target:** v9.16

**Problem**
`src/index.css` sets `body` to `bg-slate-950 text-white` in both themes; `DashboardCard.js:21` and `ui/DataTable.js` use dark-only fills. Light baselines show an invisible Positions empty-state heading, illegible RISK-ON badges and a black gate strip. `src/` has 376 bare `text-white` and 331 bare `bg-slate-800/900` classes, fixed one element at a time (`BLG-FE-87/88/95/200/224/242`).

**Scope**
- Define semantic tokens (surface, surface-raised, text, text-muted, border, positive, negative, warning) for light and dark in `tailwind.config.js`/`index.css`
- Convert the body base, `DashboardCard`, `DataTable` and `PageHeader` shells to them; update `design_system.md`

**Acceptance Criteria**
- axe `color-contrast` passes in the light theme on Dashboard, Positions (empty and populated), Trade Plan and Settings
- Visual baselines regenerated for both themes

---

### BLG-FE-257 — Show grace period in one place, linked from the others
**Priority:** P3 (Low)
**Type:** Frontend / UX (consolidation) [U]
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Source:** IDEA-head-of-ux-20261103-05 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2 days)
**Provisional-Target:** v9.17

**Problem**
Grace period appears in 4 places (Dashboard "In Grace Today", Dashboard "Positions to Watch", Positions `GracePeriodAlertZone`, Risk Dashboard `GracePeriodPanel`); surfaces have disagreed before (`BLG-BE-183`).

**Scope**
- One grace view on Positions; the Dashboard and Risk Dashboard show a count and link to it; short spec note in the affected page specs

**Acceptance Criteria**
- Grace detail renders in one component on one page; the other surfaces link to it; Playwright coverage passes

---

### BLG-FE-258 — Build the single Journal area
**Priority:** P3 (Low)
**Type:** Frontend / UX (consolidation) [U]
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-05 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** L (~3-4 days)
**Provisional-Target:** v9.17
**Depends on:** `BLG-SPEC-216`

**Problem**
See `BLG-SPEC-216`: three journaling surfaces with no links between them.

**Scope**
- Implement the Journal spec, redirects from the old routes and the Positions journal view change

**Acceptance Criteria**
- Every observable AC in the Journal spec has Playwright coverage that passes; old routes redirect

---

### BLG-FE-259 — Merge Reports and Performance Analytics into one Performance page
**Priority:** P3 (Low)
**Type:** Frontend / UX (consolidation) [U]
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Source:** IDEA-head-of-ux-20261103-05 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** L (~3-4 days)
**Provisional-Target:** v9.17
**Related:** `BLG-FE-237` (Reports tab bar overflow at phone width)

**Problem**
Win rate, profit factor and total P&L appear on both `Reports.js` (1,287 lines) and `PerformanceAnalytics.js`; neither links to the other.

**Scope**
- A short spec for one Performance page (sections: summary, monthly/tax-year reports, analytics, compliance), then the build with redirects; Metrics Definitions & Analytics Owner confirms each KPI keeps its canonical definition

**Acceptance Criteria**
- One Performance page; old routes redirect; each KPI appears once; Playwright coverage passes

---

### BLG-FE-260 — Decision-first Positions table
**Priority:** P2 (Medium)
**Type:** Frontend / UX [U]
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-06 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2-3 days)
**Provisional-Target:** v9.17

**Problem**
The Positions table (`Positions.js`) has 14 equal-weight columns; stop proximity and fired exit conditions (§7, §8) are split across Stop, State and Alerts.

**Scope**
- Sort by urgency (exit fired → stop breached → near stop → rest); lead with ticker, distance to stop (R and %), action needed; remaining columns in an expandable row; positions page spec updated

**Acceptance Criteria**
- Default view shows about 6 columns in urgency order; expanding a row shows the rest; Playwright coverage passes

---

### BLG-FE-261 — Card layout for Positions on narrow screens
**Priority:** P3 (Low)
**Type:** Frontend / responsive [U]
**Owner:** Head of Engineering
**Source:** IDEA-head-of-ux-20261103-06 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2 days)
**Provisional-Target:** v9.17

**Problem**
Below the `md` breakpoint the Positions table scrolls sideways (`DataTable` `overflow-x-auto`); the SI-05 digest sends the user into the app from a phone.

**Scope**
- A card layout below `md` with the same urgency order and leading fields as `BLG-FE-260`

**Acceptance Criteria**
- At 390px width, Positions shows cards with no horizontal page scroll; Playwright coverage passes

---

### BLG-FE-262 — Combine the four banners above the Positions table into one summary strip
**Priority:** P3 (Low)
**Type:** Frontend / UX [U]
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-06 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** S (~1 day)
**Provisional-Target:** v9.17

**Problem**
`MetricsStalenessIndicator`, `DrawdownReviewPrompt`, `ConcentrationLimitsWarning` and `GracePeriodAlertZone` stack between the Positions header and the table.

**Scope**
- One summary strip listing the active warnings, each expandable to its current content

**Acceptance Criteria**
- With all four conditions active, one strip shows four entries and each expands; Playwright coverage passes

---

### BLG-FE-263 — Use tabs or sections on the long single-scroll pages
**Priority:** P3 (Low)
**Type:** Frontend / UX (progressive disclosure) [U]
**Owner:** Head of Engineering; Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-05 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** M (~2-3 days)
**Provisional-Target:** v9.17

**Problem**
Trade Plan (1,313 lines) and Strategy Benchmark (1,149) are long single scrolls with no tabs or section navigation; Reports is handled by `BLG-FE-259`.

**Scope**
- Section tabs or an in-page section index on Trade Plan and Strategy Benchmark, keeping the current content

**Acceptance Criteria**
- Each page shows its sections as tabs or an index; each section is reachable in one click; Playwright coverage passes

---

### BLG-FE-265 — Move the remaining pages onto the semantic colour tokens
**Priority:** P3 (Low)
**Type:** Frontend / design system [U]
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Source:** IDEA-frontend-specs-20261103-03 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** L (~3-4 days)
**Provisional-Target:** v9.17
**Depends on:** `BLG-FE-264`
**Supersedes on completion:** `BLG-FE-224`, `BLG-FE-242` (close them when this ships, if not shipped earlier)

**Problem**
After `BLG-FE-264` converts the shells, page-level code still carries bare dark-only classes (376 `text-white`, 331 `bg-slate-800/900` at filing).

**Scope**
- Replace page-level dark-only colour classes with the tokens; remove redundant `dark:` pairs; update `design_system.md`

**Acceptance Criteria**
- axe `color-contrast` passes in the light theme on every routed page; no bare `text-white` remains outside coloured fills

---

### BLG-FE-266 — Fix three small chrome defects: version label, What's New heading, sidebar height
**Priority:** P3 (Low)
**Type:** Frontend / polish [U]
**Owner:** Head of Engineering
**Source:** IDEA-frontend-specs-20261103-04 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.15

**Problem**
The sidebar footer shows a hard-coded `v1.0.0` (`Layout.js:814`) while the product is at v9.14; `WhatsNewCard.js:41` renders "What's New — undefined" when the changelog payload has no `version`; the desktop sidebar background stops part-way down long pages.

**Scope**
- Show the real release version; omit the version suffix when absent; make the sidebar background full height

**Acceptance Criteria**
- Footer shows the current release; no "undefined" in the What's New heading; sidebar background spans the page; Playwright coverage passes

---

### BLG-UX-08 — First-principles UX re-review when the Site Structure & Usability programme completes
**Priority:** P2 (Medium)
**Type:** UX review (programme close-out)
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20261103-07 (IW-20261103-01), roadmap rebalance `2026-11-03__scheduled`, DL-088. User request, 2026-11-03: "Once the last change is done I want you to review the site again and confirm that nothing has changed your view."
**Effort:** S (~1 day)
**Provisional-Target:** v9.18
**Gate criteria:** Every other Site Structure & Usability programme item is ✅ COMPLETE or explicitly closed: `BLG-FE-244` to `BLG-FE-266` and `BLG-SPEC-214` to `BLG-SPEC-216`.

**Problem**
The 2026-11-03 review set a first-principles target and an IA verdict ("modify substantially, don't redesign") with a top 5. Nothing would otherwise trigger a check that the shipped changes reached that target, or that the verdict still holds.

**Scope**
- Repeat the review with the same method: label audit (sidebar vs heading vs palette), inter-page link scan, page-section order, the four journey walkthroughs (daily review, exit, signal → entry, weekly review) with step and input counts, light and dark screenshots (staging if available)
- Compare each metric with the 2026-11-03 baseline: unchecked entry routes 3, sidebar entries 18 / 4 groups, undiscoverable pages 2, dead-end pages 8, signal → entry pages 5, Positions default columns 14, grace surfaces 4, journal surfaces 3, mismatched page names 7, tab titles 0
- State whether the IA verdict and the top 5 still stand; file any new finding as a backlog item

**Acceptance Criteria**
- A review document in `docs/ux/` records before/after values for every baseline metric and an explicit confirm-or-revise statement on the verdict
- Every new finding is filed (or the document says none was found)

---

### BLG-GOV-405 — Size-budget headroom rule for action-now prompt patches
**✅ COMPLETE — 2026-11-03 — Head of Specs Team action-now patch, user-directed ("apply the 5 patches needed"), outside a sprint — `shared_standards.md` v3.41 §11; §6 checklist complete (OPERATIONAL_GUIDE.md v4.250) — branch `governance/2026-11-03-roadmap-scheduled`, PR #2141**
**Priority:** P3 (Low)
**Type:** Governance / prompt process [G]
**Owner:** Head of Specs Team
**Source:** Roadmap rebalance `2026-11-03__scheduled` lessons learnt, Friction Item 2 (deferred patch); scope gap of AUD-2026-11-03-003
**Effort:** XS (<1h)
**Provisional-Target:** v9.15

**Problem**
`scripts/check_prompt_size_budget.py` blocks any prompt over its baseline. The STEP -1.5 action-now patch to `post_ship_closure.md` (31 bytes of headroom) had to be cut four times to fit; `shared_standards.md` §11 gives no rule for small action-now patches to a prompt at its baseline.

**Scope**
- `shared_standards.md` §11: an action-now patch to a prompt at or within 1 KB of its baseline moves an equal amount of existing rationale to the prompt's companion changelog or appendix in the same commit; raising the baseline needs a Head of Specs Team reason in the `prompt_change_log.md` row
- CLAUDE.md §6 checklist for the file

**Acceptance Criteria**
- §11 states the rule; `check_prompt_size_budget.py` passes

---

### BLG-GOV-406 — Carry an unfinished programme plan forward when its Now section retires
**✅ COMPLETE — 2026-11-03 — Head of Specs Team action-now patch, user-directed ("apply the 5 patches needed"), outside a sprint — `roadmap_management_prompt.md` v1.7 STEP 5.2; §6 checklist complete (OPERATIONAL_GUIDE.md v4.250) — branch `governance/2026-11-03-roadmap-scheduled`, PR #2141**
**Priority:** P2 (Medium)
**Type:** Governance / prompt process [G]
**Owner:** Head of Specs Team
**Source:** Roadmap rebalance `2026-11-03__scheduled` lessons learnt, Friction Item 3 (deferred patch)
**Effort:** S (~0.5 day)
**Provisional-Target:** v9.15

**Problem**
The v9.15 Now section in `current_roadmap.md` carries the Site Structure & Usability programme plan for v9.16–v9.18. `roadmap_management_prompt.md` STEP 5 retires a Now section wholesale when its items ship, so at v9.15 post-ship closure the plan would be archived and the programme would survive only in backlog `Provisional-Target` fields.

**Scope**
- `roadmap_management_prompt.md` STEP 5: when a retired Now section contains a "Programme plan" table with unshipped phases, move the table (minus shipped rows) into a `### Programme plan — <name>` subsection under `## 3. Delivery Plan — Horizon: Now`, retired only when its last phase ships
- CLAUDE.md §6 checklist for the file

**Acceptance Criteria**
- The rule is in `roadmap_management_prompt.md`; applied at v9.15 post-ship closure, the programme plan stays on the roadmap with Phases 2–4

---

### BLG-GOV-407 — Exclude template agent files from the idea-intake roster
**✅ COMPLETE — 2026-11-03 — Head of Specs Team action-now patch, user-directed ("apply the 5 patches needed"), outside a sprint — `idea_intake_prompt.md` v2.13 STEP 0; §6 checklist complete (OPERATIONAL_GUIDE.md v4.250) — branch `governance/2026-11-03-roadmap-scheduled`, PR #2141**
**Priority:** P3 (Low)
**Type:** Governance / prompt process [G]
**Owner:** Head of Specs Team
**Source:** Roadmap rebalance `2026-11-03__scheduled` lessons learnt, Friction Item 4 (deferred patch)
**Effort:** XS (<1h)
**Provisional-Target:** v9.15

**Problem**
`idea_intake_prompt.md` STEP 0 populates `eligible_agents` from every `**Role:**` line in `claude/agents/*.md`, which includes the placeholder in `claude/agents/_role_charter_template.md` (23 entries instead of §4's 22) — `IW-20261103-01` shipped that wrong list in its intake commit.

**Scope**
- STEP 0: exclude files whose name starts with `_` and the Facilitator; check the result against §4's list
- CLAUDE.md §6 checklist for the file

**Acceptance Criteria**
- STEP 0 states the exclusion; a re-extraction gives §4's 22 roles

---

### BLG-OPS-211 — Confirm on main that governance-only PRs skip the five code-test suites
**Priority:** P3 (Low)
**Type:** Operations / CI
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Source:** Sprint Planning `2026-11-03__release-v9.15` STEP 6.2: post-merge tracker for ST-31 (`BLG-OPS-191`) AC 1, user-authorised — 2026-11-03
**Effort:** XS (<1h)
**Provisional-Target:** v9.16
**Depends on:** `BLG-OPS-191` (v9.15 ST-31) merged to `main`

**Problem**
ST-31 adds `paths-ignore: ['claude/**', 'docs/**']` and pass-through jobs to the five code-test workflows. Its AC 1 says a governance-only PR completes with every required check reported and none of the five suites run. That can only be seen on a real governance-only or docs-only PR opened against `main` after EPIC-05 merges, so it is outside the sprint.

**Scope**
- On the first governance-only or docs-only PR to `main` after ST-31 merges, read the PR's checks
- Record the PR number, the required checks reported and the suites skipped in ST-31's QA evidence or `docs/ops/`

**Acceptance Criteria**
- One governance-only PR on `main` shows every required check reported (pass-through) and none of the five code-test suites run, with its PR number recorded
- If a required check is missing or a suite still runs, a defect item is filed

---

### BLG-SPEC-217 — Record the production NOT NULL confirmation for positions.portfolio_id and total_cost
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** Sprint Planning `2026-11-03__release-v9.15` STEP 6.2: post-merge tracker for ST-35 (`BLG-SPEC-196`) AC 1 (production half), user-authorised — 2026-11-03
**Effort:** XS (<1h)
**Provisional-Target:** v9.16
**Depends on:** `BLG-SPEC-196` (v9.15 ST-35) migration merged and deployed

**Problem**
ST-35 re-applies NOT NULL on `positions.portfolio_id` and `positions.total_cost`. Its AC 1 needs `information_schema.columns` to report `is_nullable = NO` in production as well as staging. The production check can only run after deploy, and only the user can run it, so it falls after the sprint.

**Scope**
- After the production migration, the user runs `SELECT column_name, is_nullable FROM information_schema.columns WHERE table_name = 'positions' AND column_name IN ('portfolio_id', 'total_cost');` on production
- Record the output, with its date, in the DS-xx Live Confirmation in `docs/specs/data_model.md`

**Acceptance Criteria**
- The DS-xx Live Confirmation shows production `is_nullable = NO` for both columns, dated
- Both Fields rows carry no "nullable" note for either environment

---

### BLG-GOV-408 — Feed the v9.15 strategic-exclusions and deferred-initiatives decisions into the next roadmap rebalance
**Priority:** P3 (Low)
**Type:** Governance / roadmap process
**Owner:** Product Owner; PMO Lead
**Source:** Sprint Planning `2026-11-03__release-v9.15` STEP 6.2: post-merge tracker for ST-45 (`BLG-GOV-196`) AC 2, plus ST-44's (`BLG-GOV-195`) §2 follow-up, user-authorised — 2026-11-03
**Effort:** XS (<1h)
**Provisional-Target:** next `run roadmap` after v9.15
**Depends on:** `BLG-GOV-195` and `BLG-GOV-196` (v9.15 ST-44, ST-45) decision records filed

**Problem**
ST-44 and ST-45 file dated decision records re-confirming or flagging the four product-scope exclusions (`current_roadmap.md` §2) and the seven Priority 3 deferred initiatives (`initiative_register.md`). Both leave any change to those files to the next `run roadmap`. The decision records must be linked as that run's input, which happens after the sprint.

**Scope**
- At the next `run roadmap`, cite both decision records as inputs in its run record
- Apply any flagged exclusion or initiative change there, or record why none is needed

**Acceptance Criteria**
- The next roadmap rebalance's run record links both decision records
- Every item flagged in either record has a recorded disposition in that run

---

### BLG-FE-267 — Make the Signals "Rebalance Exit" badge meet WCAG AA contrast
**Priority:** P3 (Low)
**Type:** Frontend / UX (accessibility)
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Source:** Design gate `2026-11-03__release-v9.15` (`design_gate.md` § Observations for filing), filed at Sprint Planning, user-authorised — 2026-11-03
**Effort:** S (~0.5d)
**Provisional-Target:** v9.16

**Problem**
`signals.md` §Signal Type Badge Styling specifies `#0891B2` (cyan-600) with white text for the "Rebalance Exit" badge. That pair measures 3.68:1, below WCAG AA's 4.5:1 for 11px text. The shipped badge has not been checked against it.

**Scope**
- Measure the shipped Rebalance Exit badge in `src/`
- Move it to a passing token (measured first) and update `signals.md` §Signal Type Badge Styling
- Add a scoped axe color-contrast check on the Signals page badge in both themes

**Acceptance Criteria**
- The Rebalance Exit badge passes a scoped axe color-contrast scan in both themes (Playwright)
- `signals.md` names the shipped colour

---

### BLG-FE-268 — Fix or remove the sidebar footer's dead "Docs" link
**Priority:** P4 (Very Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Design gate `2026-11-03__release-v9.15` (`design_gate.md` § Observations for filing), filed at Sprint Planning, user-authorised — 2026-11-03
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.16

**Problem**
The sidebar footer's "Docs" link in `src/Layout.js` (next to the version label v9.15 ST-14 changes) has `href="#"` and goes nowhere. A link that does nothing looks broken.

**Scope**
- Point the link at the real documentation, or remove it
- Record the decision in `navigation.md` §Sidebar Footer and Height

**Acceptance Criteria**
- No `href="#"` remains on the sidebar footer link (or the link is gone), and a Playwright check asserts its target or absence
- `navigation.md` matches the shipped footer

---

### BLG-FE-269 — Reset the pre-entry acknowledgement when the checks change
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Agent-mediated Director of Quality review of `2026-11-03__release-v9.15` EPIC-01 (ST-01), non-blocking observation, user-authorised — 2026-11-04
**Effort:** S (~0.5d)
**Provisional-Target:** v9.16

**Problem**
In the shared `src/components/trades/PreEntryValidationPanel.js` (Trade Entry and Trade Plan), the acknowledgement tick survives edits to ticker, market, shares or entry price. A new WARN/FAIL that appears after the box was ticked is therefore accepted without a fresh acknowledgement. When the panel is collapsed the checkbox is hidden, while Trade Entry's helper line still says "Tick the acknowledgement in Pre-Entry Checks to save."

**Scope**
- Clear the acknowledgement whenever the set of WARN/FAIL check results changes
- Expand the panel automatically while an acknowledgement is required
- Update `position_form.md` §Pre-Entry Checks and `trade_plan.md` to match

**Acceptance Criteria**
- Changing an input so the WARN/FAIL set changes clears the tick and re-disables Submit (Playwright, Trade Entry and Trade Plan)
- While an acknowledgement is required, the checkbox is visible without the user expanding the panel (Playwright)
- Both specs describe the reset and auto-expand behaviour

---

### BLG-FE-270 — Make the Trail Stop footnote cover positions at a loss
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** Agent-mediated Director of Quality review of `2026-11-03__release-v9.15` EPIC-01 (ST-06), non-blocking observation, user-authorised — 2026-11-04
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.16

**Problem**
The Trail Stop modal footnote in `src/pages/Positions.js` describes only the profit-multiplier formula ("current price − (profit multiplier × 14-day ATR), never below your entry price"). Since v9.15 ST-06, `GET /positions/{id}/stop-trail` uses the initial multiplier for a position at a loss, so the footnote is wrong for those positions. Candidate to fold into v9.15 ST-17, which rewrites this modal.

**Scope**
- Reword the footnote to cover both the profitable and the at-loss case, with no literal multiplier
- Update `positions.md` §Trail Stop Action

**Acceptance Criteria**
- The footnote is correct for both a profitable and an at-loss position (code review of wording, FI-P3-02)
- No literal multiplier appears in the footnote
- `positions.md` §Trail Stop Action matches the shipped wording

---

### BLG-FE-271 — Require the acknowledgement on plan-linked Trade Entry when the plan's checks were WARN/FAIL
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Source:** Agent-mediated Product Owner review of PR #2189 (`2026-11-03__release-v9.15` EPIC-01, ST-01), user-authorised — 2026-11-04
**Effort:** S (~0.5-1d)
**Provisional-Target:** v9.16

**Problem**
Trade Entry hides the pre-entry panel when the linked plan has a stored `pre_entry_validation_snapshot`, per the locked `trade-entry-pre-entry-checks/decision_record.md` (AC 3, "not shown twice"). The Trade Plan form's acknowledgement is advisory only (`strategy_rules.md` §4.2.6 v1.23). A plan saved over a risk-off or unknown-regime FAIL can therefore become a position with no acknowledgement and no `pre_entry_override` event. That reads against §4.2.1 v1.23 ("an entry is blocked by requiring the user to acknowledge the FAIL before it can be saved"). The snapshot can also be days old, so it may not reflect today's regime.

**Scope**
- Get a Strategy Rules & System Intent Owner ruling on whether §4.2.1 v1.23 applies to the plan-linked route
- If it does: when the snapshot holds a WARN/FAIL with no recorded acknowledgement, or is older than a set age, show the panel on Trade Entry (re-run the checks) instead of the on-plan line, with the same Branch A gating and override event
- Update `position_form.md` §Pre-Entry Checks and the design record

**Acceptance Criteria**
- A dated ruling is recorded
- If the ruling applies the rule: a plan-linked entry whose snapshot has an unacknowledged WARN/FAIL (or is stale) shows the panel once and disables Submit until it is acknowledged, and a plan whose checks all passed still shows only the on-plan line (Playwright)
- Saving after the acknowledgement writes one `pre_entry_override` event (`source: trade_entry`) (backend test)

---

### BLG-QA-244 — Suppress the ⌘K tip toast in Playwright by default
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** Director of Quality
**Source:** Agent-mediated Director of Quality review of PR #2189 (`2026-11-03__release-v9.15` EPIC-01), user-authorised — 2026-11-04
**Effort:** XS (<1h plus test)
**Provisional-Target:** v9.16

**Problem**
The Layout "Press ⌘K…" tip toast appears 1.2 s after load and can intercept clicks on lower buttons. During EPIC-01 it caused a one-off SC-STP-06 failure and a repeatable SC-TEFX-07 failure on the now-taller Trade Entry page. Specs suppress it one at a time with `addInitScript` (`command-palette-tooltip-seen`), so each new spec rediscovers the flake.

**Scope**
- Set `command-palette-tooltip-seen` in the shared `tests/e2e/fixtures/api-status-guard` fixture (or a base fixture) for every test
- Let the command-palette specs that test the tip opt back in
- Remove the per-spec `addInitScript` copies

**Acceptance Criteria**
- No spec outside the command-palette tests sets `command-palette-tooltip-seen` itself
- The tip-toast tests still pass, and the full Playwright suite is green in CI

---

### BLG-BE-203 — Move strategy v1.17 and v1.20 effective dates to their deploy dates
**Priority:** P3 (Low)
**Type:** Backend Engineering / Strategy Records
**Owner:** Strategy Rules & System Intent Owner; Financial Reporting & Records Owner
**Source:** ST-20/EPIC-03, cycle `2026-11-03__release-v9.15` — out-of-scope finding under the deploy-date rule (`ESC-EXEC-20261104-03`); the seal's case (c) authorisation covered Change Log row 1.15 only — 2026-11-04
**Effort:** XS (<1h, plus a production read)
**Provisional-Target:** v9.16

**Problem**
ST-20 ruled that a behavioural strategy version takes effect on the date its code reaches production, and moved v1.15 to its deploy date (12 October 2026). v1.17 (Change Log 16 October 2026, PR #2071 merged 17 October) and v1.20 (29 October 2026, PR #2131 merged 30 October) have the same one-day lag. Their registry windows open a day before `strategy_version_at_entry` changes, so a trade entered on 16 or 29 October is stamped with the previous version but attributed to the new one. No trade list has been checked against production, because the execution environment has only the staging database.

**Scope**
- Move v1.17's and v1.20's `STRATEGY_VERSION_REGISTRY` `effective_date` and their `strategy_rules.md` Change Log Dates to the deploy dates (needs a sealed case (c) named-file authorisation with the Strategy Rules & System Intent Owner's confirmation)
- List production positions/trades entered 9–11 October, 16 October and 29 October 2026 with their `strategy_version_at_entry`, and confirm attribution
- Extend `tests/test_strategy_version_registry.py`'s window/stamp agreement test to those dates

**Acceptance Criteria**
- v1.17's and v1.20's windows open on their deploy dates, and the registry test passes
- The production listing is recorded, with every listed trade's stamp matching its window (or the exceptions named, such as a trade entered on a deploy day before the deploy finished)

---

### BLG-SPEC-218 — Open-position unrealised pnl uses a different basis from realised pnl
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner; Metrics Definitions & Analytics Owner
**Source:** ST-23/EPIC-03, cycle `2026-11-03__release-v9.15` — Data Model & Domain Schema Owner ruling `ESC-EXEC-20261104-04` (spec follows code), basis difference recorded as a follow-up — 2026-11-04
**Effort:** S (~0.5d, plus a design pass if the code changes)
**Provisional-Target:** TBD

**Problem**
After ST-23, open-position `pnl` is documented as it is computed: native P&L converted at the live GBP/USD rate, not net of `fees_paid`. Realised P&L on a closed trade is `exit_proceeds_gbp − total_cost_gbp`, which is fee-netted and includes currency movement on the principal since entry. A US position closed at today's price and rate would therefore book a realised P&L that differs from the unrealised figure shown a moment before, by the entry fees plus the FX movement on its cost.

**Scope**
- Decide whether open-position `pnl` should move to the realised basis (`current value in GBP at the live rate − total_cost`)
- If yes: change `calculate_position_pnl()` and its callers (`get_positions_with_prices()`, `portfolio_service.py`, the nightly stored `pnl`), with a design pass, because displayed P&L changes on Positions, Dashboard and Portfolio
- If no: record the decision and the reason in `data_model_positions_dictionary.md` §5.2 and `metrics_definitions.md` §Realized / Unrealized P&L Split

**Acceptance Criteria**
- The decision is recorded with its rationale by the Data Model & Domain Schema Owner
- Either the two bases agree in code and spec, or the dictionary states why they differ

---

### BLG-SPEC-219 — positions.pnl_pct is the native price change, not pnl / total_cost as the dictionary says
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner; Metrics Definitions & Analytics Owner
**Source:** ST-23/EPIC-03, cycle `2026-11-03__release-v9.15` — found while aligning §5.2 `pnl` with the code; outside ST-23's AC — 2026-11-04
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`data_model_positions_dictionary.md` §5.3 and the `pnl_pct` row define `pnl_pct = pnl / total_cost × 100`. The live value from `calculate_position_pnl()` (`backend/utils/calculations.py`), returned by `GET /positions` and stored by the on-load and nightly update, is `(current_price − native_entry) / native_entry × 100`: the native price change, ignoring fees and FX. For a US position the two differ by the fee drag and the currency move, so a reader of the dictionary cannot reproduce the displayed percentage.

**Scope**
- Data Model & Domain Schema Owner decides which is canonical
- Align the losing side; a code change that alters the displayed percentage needs a design pass

**Acceptance Criteria**
- §5.3 and the `pnl_pct` row state the same formula as the code that produces the displayed figure, or a code change brings the code to the spec
- The decision is recorded with its rationale

---

### BLG-BE-204 — Compute days_until_earnings on the US market date, not the server date
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Strategy Rules
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Source:** PR #2190 agent-mediated Director of Quality review (EPIC-03, cycle `2026-11-03__release-v9.15`), finding on ST-22's shared `earnings_service` change — 2026-11-04
**Effort:** XS (<1h plus tests)
**Provisional-Target:** v9.15 (fix in PR #2190 before merge, recommended); otherwise v9.16

**Problem**
ST-22 (`ee3460ee`) dates an `earningsTimestamp` on its America/New_York date, but `get_earnings()` still computes `days_until_earnings` against the server's `date.today()` (UTC on Render). The two bases now differ for a release in the ET evening. Example: a 21:00 EST release on 5 November, viewed at 00:30 UTC on 6 November (19:30 ET, before the release), gives `days_until_earnings = -1`. Before ST-22 it was `0`. `_check_earnings_proximity()` (`backend/routers/pre_entry_validation.py`, `strategy_rules.md` §4.2.3) then returns PASS ("Next earnings 2026-11-05 (-1 days) — outside 5-day proximity window") instead of WARN. A strategy check goes quiet in that window. The gap-risk flag is unaffected, because it computes its own days on the US market date.

**Scope**
- In `get_earnings()`, compute `days_until_earnings` from `us_market_date()` (`services/us_market_calendar.py`) instead of `date.today()`, so the date and the day count share one basis
- Unit test: the 00:30 UTC / 19:30 ET case above gives `0` and the §4.2.3 check WARNs
- `earnings_endpoints.md`: state that `next_earnings_date` is the America/New_York date and `days_until_earnings` is counted from the US market date (also covers the Positions earnings column and the morning Earnings Alert card)

**Acceptance Criteria**
- For a release on ET day D, `days_until_earnings` is `0` at every moment of ET day D, whatever the UTC date
- `_check_earnings_proximity()` WARNs at 00:30 UTC for a 21:00 ET release the same ET evening (test)
- `earnings_endpoints.md` states both bases

---

### BLG-QA-245 — Cover the Strategy Benchmark unmapped exit-reason fallback in the Trade Log contrast scan
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner; Frontend Specifications & UX Documentation Owner
**Source:** PR #2190 agent-mediated Director of Quality review (EPIC-03 ST-18, cycle `2026-11-03__release-v9.15`), DoQ pass 1 finding 5 — 2026-11-04
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-18's SC-SB-08a/b axe scans cover the four mapped exit-reason badges on the Strategy Benchmark Trade Log. The unmapped-reason fallback (`text-xs text-slate-600 dark:text-slate-400`) has the same `benchmark-exit-reason` test ID, but no mocked trade has an unmapped reason, so the fallback is never scanned. `strategy_benchmark.md` §7.3 lists it as one of the exit-reason treatments.

**Scope**
- Add a seeded trade with an unmapped `exit_reason` (e.g. `'Manual Exit'`) to `tests/e2e/strategy-benchmark.spec.js`, updating the SC-SB-04b/c row and badge counts it changes
- Assert the fallback renders and include it in SC-SB-08a/b

**Acceptance Criteria**
- SC-SB-08a/b scan five exit-reason elements, including the fallback, with no color-contrast violation in either theme

---

### BLG-FE-272 — Decide whether a failed Regenerate should keep the existing AI monthly summary
**Priority:** P3 (Low)
**Type:** Frontend / UX (product decision)
**Owner:** Product Owner; Financial Reporting & Records Owner; Head of UX & Design
**Source:** PR #2190 agent-mediated Product Owner review (EPIC-03 ST-21, cycle `2026-11-03__release-v9.15`) — 2026-11-04
**Effort:** XS (decision) to S (if behaviour changes)
**Provisional-Target:** TBD

**Problem**
When the user presses Regenerate on a stored AI monthly P&L summary and the new attempts fail their checks, the stored AI text is replaced by the code-written fallback. ST-21 extends this to a failed regeneration call. Before ST-21, a failed model call returned 503 and `reports.md` §AI Summary's "Failed" state kept the previous text. Both behaviours meet their ACs, but a user who asks for a refresh can lose a checked AI summary to a transient model error or a stricter re-check, with no way back except another Regenerate.

**Scope**
- Product Owner decides whether a `regenerate=true` request that ends in the fallback should keep the previously stored checked AI summary (returning it with a notice) or replace it as today
- If keep: change `generate_narrative()` and `reports.md` §AI Summary with a design pass; update tests

**Acceptance Criteria**
- The decision is recorded with its rationale in `reports.md` §AI Summary
- Code and tests match the decision

---

### BLG-BE-205 — Record when the nightly job last moved each position's stop
**Priority:** P3 (Low)
**Type:** Backend / data model
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Source:** Sprint Execution `2026-11-03__release-v9.15`, EPIC-02 / ST-09 (`dashboard.md` v4.0 §1B Today list, "Stops moved" group; Product Owner ruling 2026-11-04 to keep both stop groups) — 2026-11-04
**Effort:** M (~1 day)
**Provisional-Target:** v9.16

**Problem**
`GET /positions` does not record when a position's stop last moved: `compliance_service.py` notes the positions table has no `stop_updated_at` column, and `stop_calculated_at` is stamped on every nightly run whether or not the stop moved. The Dashboard Today list's "Stops moved" group (`dashboard.md` §1B) needs it, and its ACs TL-09/TL-10 cannot be tested until it exists. `RecentActivityCard.js` also reads a `stop_updated_date` that the API never sends, so its "Stop updated" entry is dead code.

**Scope**
- Migration: `stop_last_moved_date` and `previous_stop` on positions (`data_model.md`)
- `run_nightly_trailing_stop_update()` writes both only when the stop actually moves (the §7.3 ratchet raises it)
- Return both fields read-only on `GET /positions`; update `position_endpoints.md` and `docs/reference/openapi.yaml`
- Remove `RecentActivityCard.js`'s dead `stop_updated_date` branch

**Acceptance Criteria**
- After a nightly run that raises a stop, the position's `stop_last_moved_date` is that run's date and `previous_stop` is the stop before the move (pytest)
- A run that leaves the stop unchanged leaves both fields unchanged (pytest)
- Contract and OpenAPI document the fields; drift checks pass

---

### BLG-GOV-409 — Settle the clash between the no-IDs-in-headings rule and DEV-xxx deviation headings
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Sprint Execution `2026-11-03__release-v9.15`, EPIC-02 / ST-08 (agent-mediated Head of UX & Design review, non-blocking finding) — 2026-11-04
**Effort:** XS (<1h)
**Provisional-Target:** v9.16

**Problem**
CLAUDE.md §2 says task, story and ticket IDs must never appear in document headings. Known Deviations sections use `### DEV-xxx — <title>` headings (e.g. `navigation.md` `### DEV-NAV-ST06-01`), and engines have kept them under that convention. The two rules contradict each other, so each story touching a spec decides case by case.

**Scope**
- Rule whether deviation-record headings are exempt or must move the ID into the body
- Record the ruling in `shared_standards.md` (and CLAUDE.md §2 if the rule text changes)

**Acceptance Criteria**
- One written rule covers `DEV-*` headings, and CLAUDE.md §2 and `shared_standards.md` agree with it

---

### BLG-SPEC-220 — List "Daily Monitor" as a secondary button in design_system.md
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Sprint Execution `2026-11-03__release-v9.15`, EPIC-02 / ST-12 (agent-mediated Head of UX & Design review, non-blocking finding) — 2026-11-04
**Effort:** XS (<1h)
**Provisional-Target:** v9.16

**Problem**
`design_system.md` §Buttons lists "Daily Monitor" under Primary actions, from when it was a Dashboard Quick Actions tile. Since ST-12 (v9.15) it is an outline (secondary) button in the Positions header next to the primary "New Position", so the spec no longer matches the UI.

**Scope**
- Move "Daily Monitor" to the secondary actions list in `design_system.md` §Buttons, citing `positions.md` v2.24

**Acceptance Criteria**
- `design_system.md` §Buttons lists "Daily Monitor" as a secondary action and no longer as primary

---

### BLG-QA-246 — Retarget the removed popover and border token tests to a live dialog
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA & Testing Owner
**Source:** Sprint Execution `2026-11-03__release-v9.15`, EPIC-02 / ST-12 (agent-mediated Head of Specs Team review, non-blocking finding) — 2026-11-04
**Effort:** XS (<1h)
**Provisional-Target:** v9.16

**Problem**
SC-TOK-04 (`shadcn-token-remaining-families.spec.js`) and SC-MTC-05/06 (`modal-theming-token-conversion.spec.js`) tested the `border` and `popover` token families through `WidgetLibrary.js`, which ST-12 deleted with the legacy Dashboard. No live dialog consumer of `bg-popover` / `border-border` is under test now, although `ExportModal.js` and `WatchlistModal.js` still use them.

**Scope**
- Re-add the border and popover token checks against `ExportModal.js` or `WatchlistModal.js`, light and dark

**Acceptance Criteria**
- A Playwright scenario asserts the dialog's border and background resolve to the `--border` and `--popover` tokens (non-transparent) in both themes, and passes in CI

---

### BLG-FE-273 — Stop a malformed Research URL from blanking the app (tab-title decode)
**Priority:** P2 (Medium)
**Type:** Frontend / Correctness
**Owner:** Head of Engineering
**Source:** PR #2191 agent-mediated Director of Quality review (EPIC-02, v9.15, ST-13) — 2026-11-05
**Effort:** XS (<1h)
**Provisional-Target:** v9.15

**Problem**
`documentTitle()` in `src/lib/pageLabels.js` calls `decodeURIComponent` on the `/research/:ticker` segment with no guard. A malformed percent-escape (e.g. `/#/research/%E0%A4%A`) throws `URIError: URI malformed` inside `Layout.js`'s title effect, and the whole app renders blank (reproduced in Playwright against the PR build). On `main` the same URL renders, because react-router decodes params safely, so this is a regression introduced by ST-13.

**Scope**
- Wrap the decode in try/catch and fall back to the raw segment (or the plain Research title)
- Playwright scenario for a malformed Research URL

**Acceptance Criteria**
- `/#/research/%E0%A4%A` renders the Research page with no page error, and the tab title falls back without throwing (Playwright)
- Existing SC-BTT-01..06 still pass

---

### BLG-FE-274 — Decide whether the portfolio value and allocation charts removed with the legacy Dashboard should return
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Product Owner; Head of UX & Design
**Source:** PR #2191 agent-mediated Product Owner review (EPIC-02, v9.15, ST-12) — 2026-11-05
**Effort:** S (~0.5 day, decision; any build is separate)
**Provisional-Target:** v9.16

**Problem**
ST-12 removed the legacy widget Dashboard and the components only it rendered, as scoped. Two of those widgets have no equivalent elsewhere: the portfolio value chart (`PortfolioChart`, from `GET /portfolio/history`) and the allocation chart (`AllocationChart`). Analytics has a drawdown chart (`UnderwaterChart`) but no equity curve or allocation view. The legacy page had no sidebar entry, so use was likely low, but the views are now unavailable.

**Scope**
- Decide whether an equity-curve and/or allocation view is needed, and where (Analytics, Risk Dashboard, or the Dashboard status cards per `dashboard.md` v4.0)
- If yes, file the design and build items; fold into the BLG-UX-08 first-principles re-review if timing fits

**Acceptance Criteria**
- A dated Product Owner decision is recorded on this item, with follow-up items filed if the views return

---
