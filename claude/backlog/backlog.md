# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-05-18 (release planning v3.7 — §12 release slice added; BLG-GOV-24 added — gh_issue_template.md §14 tracking gap)
**Last rebalance:** 2026-05-15 (cycle 2026-05-15__scheduled — DL-029 backlog add × 1 BLG-QA-19)

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

*No active items in this section — BLG-TECH-05 deferred to §9 (DL-023, 2026-04-24).*

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

### BLG-FE-34 — Trade plan form: surface signal context to guide entry rationale and confirmation criteria
**Priority:** P1 (High)
**Type:** Frontend / UX + Backend
**Owner:** Head of Engineering
**Source:** Product intent alignment session (production_strategy.py) — 2026-05-18
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.7
**Depends on:** BLG-FE-33 (signal → watchlist linkage required to pass signal data through)

**Problem**
The trade plan form asks users to fill in entry rationale and confirmation criteria but surfaces no technical data to support these fields. The strategy's entry rules are fully computable at signal time (momentum rank, price vs 200-day MA, regime status, ATR, suggested stop) and already live on the signal object — yet none of this reaches the trade plan form. Users are left with blank fields and must context-switch to reconstruct information the system already holds.

**Scope**
- Surface a read-only "Signal Context" panel in the trade plan creation form when a linked signal exists for the ticker: rank, momentum %, price vs 200-day MA (% above/below), regime on/off, ATR value, suggested initial stop (entry − 5 × ATR)
- Pre-populate entry rationale with a structured template derived from signal data: "Rank {N} momentum signal. Price {above/below} 200-day MA by {x}%. {US/UK} regime on." (user-editable)
- Pre-populate confirmation criteria with strategy defaults: "Price above 200-day MA at entry. Regime on. Spare cash available." (user-editable)
- Pre-fill stop field with suggested stop: entry price − (5 × ATR)
- Signal Context panel hidden and fields blank when no linked signal exists — no regression to current behaviour
- Entry timing: Signal Context panel notes entry is triggered at current price when spare cash is available (not month-end)

**Acceptance Criteria**
- Signal Context panel shown in trade plan form when a linked signal exists for the ticker, displaying: rank, momentum %, price vs 200-day MA, regime on/off, ATR, suggested stop
- Entry rationale pre-populated with structured template from signal data; user can edit
- Confirmation criteria pre-populated with strategy defaults; user can edit
- Stop field pre-filled with entry price − (5 × ATR) matching initial_atr_mult=5
- No Signal Context panel and no pre-population when no linked signal exists
- Signal Context data is read-only within the form

---

### BLG-FE-33 — Signals page: replace Add Position CTA with Add to Watchlist
**Priority:** P1 (High)
**Type:** Frontend / UX + Backend
**Owner:** Head of Engineering
**Source:** Head of UX & Design + Head of Specs Team alignment session — 2026-05-17
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.7

**Problem**
The Signals page shows "Add Position" as the primary CTA on new signal cards. The user guide (§4→5) explicitly defines the workflow as signal → watchlist → research → plan → entry. The current UI bypasses this entirely, pushing users toward immediate trade entry and undermining the discipline the system is designed to enforce.

**Scope**
- Replace "Add Position" button with "Add to Watchlist" (primary CTA) on new signal cards
- "Dismiss" retained as secondary action; "Add Position" removed from signal cards entirely
- Add to Watchlist action: silent POST /watchlist pre-filled with ticker, market, initial_stop_price; then PATCH /signals/{id} status=watchlisted on success
- Add watchlisted signal card state: shows "View in Watchlist" link (→ /watchlist), no action buttons
- Add `watchlisted` to signals table CHECK constraint
- PATCH /signals/{id} updated to accept `watchlisted` as a valid status value
- signal_endpoints.md and data_model.md updated (version bumped, changelog entry, OPERATIONAL_GUIDE §14, prompt_change_log.md) in same commit as backend change

**Acceptance Criteria**
- Signal card "Add Position" button replaced with "Add to Watchlist" (primary CTA)
- Clicking "Add to Watchlist" calls POST /watchlist with ticker, market, initial_stop_price pre-filled; PATCH /signals/{id} status=watchlisted on success
- Signal card transitions to watchlisted state: "View in Watchlist" link shown, no action buttons
- Dismiss button retained as secondary action on new signals
- `watchlisted` added to signals table CHECK constraint; PATCH endpoint accepts it
- signal_endpoints.md and data_model.md updated in same commit as backend change
- Duplicate add (ticker already on watchlist): toast "Already on your watchlist"; signal still transitions to watchlisted

---

*BLG-FE-32 (Research view SC-RV-18/SC-RV-19 Playwright coverage) — ✅ COMPLETE v3.6 — archived to backlog_archive.md 2026-05-17*

---

### BLG-FE-35 — ST-08 AC-02: Human staging sign-off for Research page font conformance
**Priority:** P3 (Low)
**Type:** Frontend / QA Verification
**Owner:** Head of UX & Design
**Source:** v3.6 EPIC-03 ST-08 — AC-02 deferred from sprint execution; delivery verification 2026-05-17 — item filed as required by CLAUDE.md §2 frontend testing gate (referenced in qa_evidence_EPIC-03.md as BLG-UX-ST08-staging); renamed from BLG-FE-33 to BLG-FE-35 (ID collision resolved 2026-05-18)
**Effort:** XS (~0.5 hour staging run)
**Provisional-Target:** v3.7 or next sprint touching Research page

**Problem**
ST-08 (v3.6 EPIC-03) fixed regime lozenge wrapping (AC-01) and targeted font conformance (AC-02). Code review confirmed `text-xs font-medium` (SignalBadge), section headings `text-xs font-medium text-slate-400 uppercase tracking-wider`, and data values `text-xl font-semibold text-white` all match design_system.md. However, CLAUDE.md §2 requires either Playwright coverage or human staging with date recorded — code review alone is not a valid evidence method. Staging was deferred at sprint execution and not performed at delivery verification.

**Acceptance Criteria**
- Head of UX & Design performs side-by-side comparison of Research page rendering against `docs/frontend/design_system.md` typography scale in a live/staging environment
- Date of staging run recorded in this item (or in the QA evidence file for the sprint in which it is performed)
- If conformant: archive BLG-FE-26 (parent item, partially closed by ST-08 AC-01) and this item
- If non-conformant: file a new backlog item with specific font deviation details

---

## 4. Backend & Data Backlog


---

*BLG-AI-02 (Model version contract for AI Journal) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-AI-03 (AI Journal Summarisation quarterly review cadence) — ✅ COMPLETE v3.4 — archived to backlog_archive.md 2026-05-14*

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

### BLG-QA-20 — Consolidate database stub files into a shared pytest conftest fixture
**Priority:** P2 (Medium)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner
**Source:** v3.6 sprint execution 2026-05-17 — recurring stub-sync CI failure (ST-01 root-cause analysis)
**Effort:** S (~0.5 day)
**Provisional-Target:** v3.7 or next sprint touching backend service tests

**Problem**
Four test files (`test_alerts_service.py`, `test_watchlist_service.py`, `test_trade_service.py`, `test_service_coverage.py`) each maintain their own hand-rolled `types.ModuleType("database")` stub injected into `sys.modules`. Whenever a new function is added to `position_service.py`'s `database` imports, it must be manually added to all four stubs or CI fails with `ImportError: cannot import name '...' from 'database' (unknown location)`. This has caused at least one multi-hour CI debugging session.

**Scope**
- Create `tests/conftest.py` with a session-scoped database stub fixture that includes all current database function mocks
- Remove the redundant per-file stub injection blocks from the four test files
- Verify 69+ tests still collected and pass

**Acceptance Criteria**
- Single source of truth for database stub in `tests/conftest.py`
- The four test files no longer each define their own `types.ModuleType("database")` block
- All existing tests pass; no new collection errors

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

*BLG-OPS-14 (AI Journal monitoring metrics) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*
*BLG-OPS-12 (External API health check extension) — ✅ COMPLETE v3.0 — archived to backlog_archive.md 2026-04-28*

---

*BLG-OPS-15 (Research endpoint latency monitoring) — ✅ COMPLETE v3.3 — archived to backlog_archive.md 2026-05-13*

---

### BLG-OPS-16 — Remove tracked `backend/__pycache__` files from git and add to .gitignore
**Priority:** P3 (Low)
**Type:** Operations / Repository Hygiene
**Owner:** Infrastructure & Operations Owner
**Source:** v3.6 sprint execution 2026-05-17 — stale pyc files caused spurious CI debugging (red herring during ST-01 stub investigation)
**Effort:** XS (~0.5 hour)
**Provisional-Target:** Next available sprint with repository hygiene slot

**Problem**
Compiled Python bytecode files (`backend/__pycache__/*.pyc`) are tracked in git. Stale pyc files (e.g. `database.cpython-310.pyc` lacking recently added functions) cause misleading CI diagnostics: they appear to be the cause of import errors when the real cause is `sys.modules` stub contamination. Additionally, pyc files built for Python 3.10 are silently ignored by CI (Python 3.11), making them pure noise.

**Scope**
- Run `git rm -r --cached backend/__pycache__/` to untrack all pyc files
- Add `__pycache__/` and `*.pyc` to `.gitignore`
- Commit; verify CI is unaffected

**Acceptance Criteria**
- No `*.pyc` or `__pycache__/` files tracked in git
- `.gitignore` updated
- CI green after change

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

## 8. Governance Backlog

### BLG-GOV-23 — scored_initiatives.md comprehensive refresh
**Priority:** P3 (Low)
**Type:** Governance / Planning Infrastructure
**Owner:** Facilitator
**Source:** v3.5 post-ship closure OA-05; v3.6 release planning LL observation #5; 2026-05-18__scheduled roadmap rebalance
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before next roadmap rebalance with advancing candidates

**Problem**
scored_initiatives.md was last updated 2026-03-31. Arc 3 features (IT-01–IT-06) and Arc 4–6 initiatives (PO-01–05, SI-01–05, PS-01–05) are absent. All STEP 6 effort-band estimates for current roadmap items have been falling to Tier 3 inline inference for 10+ cycles. This deferred action has carried through v3.5 and v3.6 without a backlog item (OA-05).

**Scope**
- Add scored rows for Arc 3 shipped items (IT-01–IT-06): SPS and effort bands for historical completeness
- Add scored rows for active Arc 4–6 roadmap initiatives with current SPS and effort bands per STEP 6 criteria
- Update file header Last Updated date
- Preserve all existing entries intact

**Acceptance Criteria**
- scored_initiatives.md header Last Updated updated to date of refresh
- Arc 3 items (IT-01–IT-06) have scored rows with SPS and effort bands
- Active Arc 4–6 roadmap items (PO-01–05, SI-01–05, PS-01–05) have scored rows
- All existing scored rows preserved

---

### BLG-GOV-24 — Add gh_issue_template.md to §14 governance table
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Governance-drift check during preflight consolidation branch gov/2026-05-17__preflight-consolidation — 2026-05-17
**Effort:** XS (<1h)
**Provisional-Target:** v3.7

**Problem**
`claude/system/gh_issue_template.md` carries a `**Version:** 1.0` header and is a Class 6 governance file, but it is absent from the §14 governance table in `OPERATIONAL_GUIDE.md`. This means `/governance-drift` flags it as UNTRACKED on every check, creating noise and risking the version being silently bumped without a §14 update. Pre-existing gap — not introduced by the preflight consolidation refactor.

**Acceptance Criteria**
- `gh_issue_template.md` entry added to §14 governance table in `OPERATIONAL_GUIDE.md` with current version (v1.0)
- `/governance-drift` no longer flags the file as UNTRACKED

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

## 12. Release Slice — v3.7 (cycle: 2026-05-18__release-v3.7)

<!-- release-plan-marker: RP:v3.7:2026-05-18__release-v3.7 -->

*This section is ephemeral — remove during next `groom backlog` run after v3.7 closes.*

| ST-ID | EPIC | Backlog Item | Priority | Sprint |
|-------|------|--------------|----------|--------|
| ST-01 | EPIC-01 | BLG-FE-33 backend: signals `watchlisted` status + PATCH endpoint | P1 | 1 |
| ST-02 | EPIC-01 | BLG-FE-33 frontend: Add to Watchlist CTA on signal cards | P1 | 1 |
| ST-03 | EPIC-01 | BLG-FE-34: Trade plan form signal context panel | P1 | 1 |
| ST-04 | EPIC-02 | PT-04 spec authoring + gate confirmation (conditional) | P2 | 2 |
| ST-05 | EPIC-02 | PT-04 backend: quality score endpoint (conditional) | P2 | 2 |
| ST-06 | EPIC-02 | PT-04 frontend: quality score display (conditional) | P2 | 2 |
| ST-07 | EPIC-03 | execution_prompt.md patches ×3 (deviations_filed + backlog verify + spec_references) | P1 | 1 |
| ST-08 | EPIC-03 | qa_evidence_template.md BLG-GOV-19 criterion 3 fail-path | P1 | 1 |
| ST-09 | EPIC-04 | BLG-QA-20: database stub conftest consolidation | P2 | 1 |
| ST-10 | EPIC-04 | BLG-OPS-16 + BLG-FE-35: pycache git hygiene + Research page font staging | P3 | 1 |
| ST-11 | EPIC-04 | BLG-GOV-23: scored_initiatives.md comprehensive refresh | P3 | 1 |

---


