# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-04-03 (delivery verification 2026-03-31__release-v2.4 — 3 items added: BLG-FE-08, BLG-GOV-10, TEST-GAP-EPIC-01-v24; prior session 4 items: BLG-OPS-12, BLG-OPS-13, BLG-BE-07, BLG-FE-07)
**Last rebalance:** 2026-03-24 (cycle 2026-03-24__scheduled — DL-012)

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

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

### BLG-TECH-05 — Prometheus metrics endpoint
**Priority:** P3 (Low)
**Type:** Observability
**Owner:** Infrastructure & Operations Owner
**Source:** Original backlog — target updated to v2.3 per backlog health scan GROOM-20260324-01
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.4 (or when system becomes multi-user)

**Problem**
No Prometheus-compatible metrics endpoint exists. As the system grows toward multi-user operation, there is no way to monitor validation run counts, failure rates, or duration without instrumenting the application directly. Observability cannot be added retroactively without significant rework.

**Scope**
- Add `GET /metrics` Prometheus endpoint exposing: validation run count, failure count by metric and severity, validation duration
- Optional Grafana dashboard

**Acceptance Criteria**
- Metrics scrape successfully in Prometheus format
- Counters and histograms are correct

---

## 2. Product Feature Backlog (User-Facing)

---

## 3. Frontend & UX Backlog

---

### BLG-FE-06 — Fix missing P&L (GBP) column on Positions page
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** DEV-EPIC02-ST05-03 — V-PATH2-01 staging QA — 2026-03-25
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.4

**Problem**
The Positions page Table View does not display the "P&L (GBP)" absolute value column. `positions.md` v1.4 explicitly lists both "P&L (GBP)" and "P&L %" as separate columns in the Table View. During EPIC-02 staging QA (2026-03-25), only % uplift was visible — the absolute £ values (£70.05 for LGEN, £96.05 for BARC) were absent. Colour rendering works correctly (% shown in green for positive positions), confirming the issue is the missing GBP column rather than a colour bug. Users cannot see their monetary P&L on the primary portfolio view.

**Scope**
- Investigate whether the P&L (GBP) column is missing from the component or rendered but hidden
- Add or unhide the P&L (GBP) column in the Positions Table View component
- Ensure the GBP value is colour-coded correctly (green for positive, red for negative) per `positions.md`
- Verify both "P&L (GBP)" and "P&L %" columns are visible side by side in the default Table View at staging

**Acceptance Criteria**
- Positions Table View displays a P&L column showing the absolute GBP value (e.g. £70.05 for LGEN, £96.05 for BARC from seed data)
- Positive GBP P&L values render in green; negative values render in red
- P&L % column remains present alongside the GBP column
- V-PATH2-01 passes on staging: £70.05 and £96.05 visible in green after seeding

---

### BLG-FE-03 — User-facing error message mapping layer
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend Prompt Owner
**Source:** IW-20260304-01 (IDEA-base44-frontend-20260304-02 — gate cleared: BLG-SPEC-G2 Error Response Standard shipped v2.1)
**Effort:** S–M (~1–2 days)
**Provisional-Target:** v2.4
**Depends on:** BLG-SPEC-G2 (✅ shipped v2.1)

**Problem**
Backend API errors surface as raw status codes or technical messages in the UI. Users see "500" or "undefined" instead of actionable guidance. The Error Response Standard (BLG-SPEC-G2) defines the error envelope — this item consumes it on the frontend.

**Scope**
- Create a frontend error mapping layer: HTTP status code + error code → user-readable message
- Cover all known error codes defined in the BLG-SPEC-G2 Error Response Standard
- Apply consistently across all API-consuming components
- Log raw error details to console for debugging; surface friendly message to user

**Acceptance Criteria**
- API errors display a user-readable message rather than a raw code or "undefined"
- Error mapping covers all error codes defined in the Error Response Standard
- Raw technical details logged to console (not shown to user)
- No regression to existing error display behaviour

---

## 4. Backend & Data Backlog

---

### BLG-BE-05 — Fix ATR pence→GBP conversion for all UK (.L) tickers
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Bug Fix
**Owner:** Head of Engineering
**Source:** V-PATH1-04 staging test failure — server log ATR=-48.69 for LGEN at £2.45 — 2026-03-25
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.4

**Problem**
`calculate_atr()` in `backend/utils/pricing.py` applies the pence→GBP conversion (`atr / 100`) only when `atr > 100`, but Yahoo Finance returns ATR in pence for all LSE `.L` tickers regardless of magnitude. For most UK stocks (ATR typically 5–30p), the guard is never triggered, leaving ATR in pence while all other price values are in GBP. This causes `calculate_initial_stop()` (multiplier=5.0) to produce deeply negative stop prices (e.g. -48.69 for LGEN at £2.45, ATR=10.23p), which the backend rejects and the position creation call fails.

**Scope**
- In `backend/utils/pricing.py` `calculate_atr()`, remove the `> 100` guard and always divide by 100 for `.L` tickers
- Verify `calculate_initial_stop()` produces a sane positive stop for LGEN (£2.45 entry, expected stop ≈ £1.94 at 5× ATR of ~10p)

**Acceptance Criteria**
- `calculate_atr('LGEN.L', ...)` returns ATR in GBP (e.g. ~0.10) not pence (e.g. ~10.23)
- `calculate_initial_stop(2.45, atr)` returns a positive value in the range £1.80–£2.40 for LGEN
- No regression: existing unit tests for ATR pass; high-ATR stocks (e.g. TSLA) are unaffected

---

### BLG-BE-04 — R-Multiple Analysis: stop price unavailable from trade_history
**Priority:** P3 (Low)
**Type:** Backend / Data
**Owner:** Head of Engineering
**Source:** ST-11 post-merge staging sign-off — 2026-03-19
**Effort:** S (~2–3 hours)
**Provisional-Target:** v2.4

**Problem**
`RMultipleAnalysis.js` filters trades using `t.stop_price`. The analytics page passes trades from `trade_history`, which does not carry `initial_stop` (stop price lives on `positions`). As a result, the R-Multiple Analysis section shows "R-Multiple requires stop prices to be defined for all trades" even when all positions had stop prices set at entry. The R-Multiple Distribution histogram only renders when `tradesWithR.length >= 10`.

**Scope**
- Extend the analytics endpoint (or trade history endpoint) to JOIN `positions.initial_stop` into the `trade_history` response, or expose `initial_stop` as `stop_price` on closed trade objects returned to the frontend
- Update `RMultipleAnalysis.js` filter if the field name changes
- Update `docs/specs/api_contracts/analytics_endpoints.md` and `openapi.yaml` if response shape changes

**Acceptance Criteria**
- Closed trades returned to the analytics page include a `stop_price` (or `initial_stop`) field where available
- R-Multiple Analysis section renders correctly for trades where stop prices were set at entry
- `RMultipleAnalysis.js` filter produces correct `tradesWithR` count
- `openapi.yaml` updated in same commit if response shape changes

---

## 5. QA & Test Automation Backlog

---

### TEST-GAP-EPIC-05-SLIP — Create slippage tracking test scenarios
**Priority:** P3 (Low)
**Type:** QA Coverage
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-18__release-v2.1 — TSG-v21-03
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.4

**Problem**
No scenario file covers slippage tracking (ST-14). Manual coverage is unstructured and not repeatable. Without documented scenarios, QA runs against slippage features cannot be signed off consistently across cycles.

**Scope**
- Author SC-SLIP-01 through SC-SLIP-04 covering: fill price input on trade entry, slippage % column display (colour-coded), avg slippage StatsCard update, null fill price shows "—"
- Add to `docs/testing/reports_scenarios.md` or a new `slippage_scenarios.md`

**Acceptance Criteria**
- Scenario file present covering all four slippage tracking scenarios
- Scenarios executable against staging without additional setup
- Referenced in the test scenario index

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-05 — API endpoint performance baseline
**Priority:** P3 (Low)
**Type:** Operational / Observability
**Owner:** Head of Engineering + Infrastructure & Operations Owner
**Source:** IDEA-head-of-engineering-20260304-02 (IW-20260321-01 — gate cleared: API surface stable post-v2.1)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v2.4

**Problem**
No baseline exists for endpoint response times. As features are added (alert evaluation, chart queries), performance regressions cannot be detected. The alert evaluation endpoint and analytics queries are the most likely candidates for slowdown.

**Scope**
- Instrument and document p50/p95 response times for all currently active API endpoints
- Use existing integration test infrastructure or a simple timing script
- Produce a baseline document in `docs/` or as a test artefact
- Identify any endpoint already outside acceptable thresholds

**Acceptance Criteria**
- Response time baseline documented for all endpoints defined in `openapi.yaml`
- p50 and p95 values recorded
- Any endpoint with p95 > 500ms flagged for investigation

---

## 7. Spec Debt Backlog

---

### BLG-SPEC-D16 — Reconcile data_model.md trade_history table with database.py column names
**Priority:** P2 (Medium)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner + Head of Engineering
**Source:** ST-04 seed script / database.py divergence discovered 2026-03-25
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.4

**Problem**
`data_model.md` documents `trade_history` with a single exit value column `exit_proceeds DECIMAL(12,2) NOT NULL`. `database.py:create_trade_history()` inserts into `gross_proceeds`, `net_proceeds`, `entry_fees`, `exit_fees` — none of which appear in the spec. It is unknown which is canonical: if the spec is right, `database.py` is broken and live trade closures fail; if `database.py` is right, the spec is wrong and seed scripts using `exit_proceeds` will be rejected. Until resolved, any new seed, test, or analytics query against `trade_history` exit values carries column name uncertainty.

**Scope**
- Run `\d trade_history` against the live staging DB to confirm actual column names
- Determine canonical set: `exit_proceeds` (spec) vs `gross_proceeds`/`net_proceeds`/`entry_fees`/`exit_fees` (code)
- Update `data_model.md` §3 trade_history table to match actual schema
- If DB has `exit_proceeds` only: update `database.py:create_trade_history()` to use it
- If DB has `gross_proceeds`/`net_proceeds`: update `data_model.md` to match and remove `exit_proceeds`
- Update seed scripts (`seed_portfolio_trades.sql`) to use confirmed column names
- Bump `data_model.md` version; apply §6 checklist

**Acceptance Criteria**
- `data_model.md` trade_history CREATE TABLE matches `\d trade_history` on staging
- `database.py:create_trade_history()` column list matches the spec
- `seed_portfolio_trades.sql` trade_history INSERT uses confirmed column names and succeeds without error
- `data_model.md` version bumped; §6 checklist applied

---

### BLG-SPEC-D15 — Reconcile data_model.md portfolios table with actual deployed schema
**Priority:** P2 (Medium)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** ST-04 seed script failure — reset_staging_db.sql INSERT rejected `initial_cash` column — 2026-03-25
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.4

**Problem**
`data_model.md` documents the `portfolios` table with columns `id`, `cash`, `initial_cash`, `created_at`, `last_updated`. The actual deployed DB has `id`, `cash`, `created_date`, `last_updated` — `initial_cash` does not exist and `created_at` is `created_date`. Any seed script, migration, or integration test written against the spec will fail silently or with a column-not-found error. This mismatch was not caught before ST-04 shipped because seeds were reviewed against the spec, not the live schema.

**Scope**
- Run `\d portfolios` against the live staging DB to confirm actual column names and types
- Update `data_model.md` §1 Portfolios Table CREATE TABLE statement and Fields table to match actual schema
- Remove `initial_cash` from the spec or add a migration to create it if it is genuinely required
- Bump `data_model.md` version and apply §6 checklist

**Acceptance Criteria**
- `data_model.md` portfolios CREATE TABLE matches the output of `\d portfolios` on staging
- `initial_cash` either removed from spec or present in DB — no divergence
- `created_date` vs `created_at` discrepancy resolved
- `data_model.md` version bumped; §6 checklist applied

---

## 8. Governance Backlog

---

### BLG-GOV-08 — Engine prompt compression: roadmap_prompt and release_planning_prompt
**Priority:** P3 (Low)
**Type:** Governance Process / Technical Debt
**Owner:** Head of Specs Team
**Source:** AUD-2026-03-21 Tier 3 — engine prompt compression deferred (roadmap_prompt 1,581 lines; release_planning_prompt 1,534 lines)
**Effort:** L (~3–5 days)
**Provisional-Target:** v2.4

**Problem**
`claude/system/roadmap_prompt.md` (1,581 lines) and `claude/system/release_planning_prompt.md` (1,534 lines) are the two largest engine prompts in the governance system. Inline schemas, repeated examples, and verbose explanatory prose are opportunities for extraction and tightening without removing instructional precision or hard gate logic.

**Scope**
- Reduce both files by at least 10% in line count without removing governance intent or hard gate logic
- Extract schemas or reference material to `shared_standards.md` with cross-references added in-engine
- Update OPERATIONAL_GUIDE §14 and §6/§6B source prompt headers accordingly

**Acceptance Criteria**
- Both files reduced by at least 10% in line count
- No governance intent or hard gate logic removed
- Extracted material moved to `shared_standards.md` with cross-reference
- §6 checklist applied per CLAUDE.md for both files
- OPERATIONAL_GUIDE §14 and §6/§6B headers updated

---

### BLG-GOV-03 — Simplify cycle artefact sealing (remove SHA-256, retain sealed flag)
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Direct session architectural review — 2026-03-18
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.4

**Problem**
The current release planning engine computes and verifies SHA-256 hashes for sealed artefacts on every run. For a 2-person team, the primary threat (accidental writes by Claude) is already covered by write scope restrictions in STEP 5. Hash recomputation adds schema complexity and verification overhead for a failure mode that `git diff` would catch anyway.

**Scope**
- Remove `sealed_hashes` and `artifact_hashes` fields from `state.json` schema
- Remove hash computation and drift detection steps from the release planning engine
- Retain `sealed: true` flag as the sole sealing mechanism
- Retain `state_snapshot_hash` on `state.json` only (single lightweight checksum)

**Acceptance Criteria**
- Release planning engine no longer computes or verifies per-artefact SHA-256 hashes
- `state.json` schema updated; `sealed_hashes` and `artifact_hashes` blocks removed
- `sealed: true` flag check remains and is enforced as a hard gate
- All references to hash drift detection removed from prompt and shared_standards

---

## 9. Deferred / Future Candidates

- Daily email portfolio summary
- FX rate history tracking
- Prometheus validation observability (BLG-TECH-05)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system

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
- Any shipped feature must be backed by: a canonical specification, updated validation where applicable
- Once implemented, backlog items are superseded by canonical documentation

---

## 12. Active Release Slice — v2.4 Correctness, Insight & Governance Hardening

<!-- release-plan-marker: RP:v2.4:2026-03-31__release-v2.4 -->

**Cycle:** 2026-03-31__release-v2.4
**Published:** 2026-03-31
**Backlog slice:** claude/cycles/2026-03-31__release-v2.4/stage4_backlog_slice.md

| EPIC-ID | Scope | Sprint |
|---------|-------|--------|
| EPIC-01 | Backend Correctness & Alert Reliability (ST-01, ST-02, ST-03) | Sprint 2 |
| EPIC-02 | Frontend & UX Polish (ST-04, ST-05) | Sprint 2 |
| EPIC-03 | Spec Debt Resolution (ST-06, ST-07) | Sprint 1 |
| EPIC-04 | Weekly Trading Digest (ST-08, ST-09) | Sprint 3 |
| EPIC-05 | Operational Readiness (ST-10, ST-11, ST-12, ST-13) | Sprint 1/2 |
| EPIC-06 | Governance Engine Maintenance (ST-14, ST-15, ST-16, ST-17) | Sprint 1 |

**Deferred from v2.4:** BLG-GOV-08 (prompt compression, L effort → v2.5); BLG-FEAT-13 (gated rollout → v2.5); BLG-TECH-05 (Prometheus → conditional)

---

## 13. New Backlog Items — Roadmap Rebalance 2026-03-31

*Items from roadmap rebalance cycle 2026-03-31__scheduled (DL-013 to DL-016) and prior session addition (BLG-FEAT-13). Target releases are indicative.*

---

### BLG-FEAT-13 — Add gated feature rollout capability
**Priority:** P3 (Low)
**Type:** Product Feature / Platform
**Owner:** Head of Engineering + Product Owner
**Source:** User request — 2026-03-31
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5

**Problem**
The application has no mechanism to roll out new features to a subset of users or environments. Any new capability ships immediately to all users with no ability to stage a rollout, run a controlled trial, or roll back a single feature without reverting the entire deployment. As the product grows this creates risk for experimental features and makes it impossible to validate new UI flows with a limited audience before full release.

**Scope**
- Define a feature flag schema (flag name, enabled boolean, optional env/user scope)
- Implement a lightweight flag evaluation mechanism driven by config file or environment variables — no external service dependency required at first
- Wrap at least one new feature behind a flag as a proof-of-concept on first use
- Document the gating pattern in a spec file or OPERATIONAL_GUIDE

**Acceptance Criteria**
- A feature can be toggled on/off without a code change (env var or config file)
- Flag state is auditable (logged at startup or accessible via a lightweight admin check)
- At least one shipped feature uses a gate as proof-of-concept
- Gating pattern documented for use in future story authoring

---
### BLG-FEAT-14 — Weekly trading review digest
**Priority:** P2 (Medium)
**Type:** Product Feature
**Owner:** Backend Engineering Patterns Owner + Frontend Specs & UX Documentation Owner
**Source:** Roadmap rebalance cycle 2026-03-31__scheduled (IDEA-product-owner-20260321-02 advancing) — 2026-03-31
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.4

**Problem**
The user must manually navigate to multiple pages (positions, alerts, compliance score) to perform a weekly portfolio review. There is no structured summary endpoint or view that aggregates the past 7 days of P&L, alert activity, and compliance metrics in one place. Following the v2.3 launch of BLG-FEAT-11 (compliance score) and BLG-FEAT-09 (staleness indicator), sufficient data exists to produce a meaningful weekly digest with no additional data collection.

**Scope**
- New backend endpoint returning: 7-day realised P&L, unrealised P&L delta, alerts fired vs dismissed count, compliance score (current + 7-day trend), staleness indicator summary
- Frontend digest component rendering the above as a structured data table (no generated text or interpretive commentary)
- Spec: define response schema in api_contracts

**Acceptance Criteria**
- Endpoint returns all specified fields for the past 7 days
- Response contains raw numeric/boolean fields only — no generated text, narrative, or interpretation
- Frontend renders digest as a data table (not commentary format)
- AC explicitly confirmed: no generated text or interpretation present in any response field
- Spec entry added to relevant api_contracts document

---

### BLG-OPS-10 — Render hosting tier review
**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** FinOps & Resource Architect + Infrastructure & Operations Owner
**Source:** Roadmap rebalance cycle 2026-03-31__scheduled (IDEA-finops-20260321-01 advancing) — 2026-03-31
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.4

**Problem**
BLG-OPS-04 (cron alert scheduling) has been running in production since v2.2 (2026-03-24). A full sprint cycle (v2.3) of alert scheduling has now elapsed. There is no documented assessment of whether the daily scheduling workload fits within Render's free tier limits (CPU minutes, bandwidth, DB connections). Without a review, cost/capacity issues may surface without warning.

**Scope**
- Document current Render plan tier and free tier limits (CPU minutes, bandwidth, sleep/wake behaviour)
- Review BLG-OPS-04 cron workload: evaluate actual daily execution against limits
- Record a decision: free tier sufficient | paid tier warranted now | monitor for N sprints before deciding
- File as an operational record (Class 3) in `docs/` or `claude/cycles/`

**Acceptance Criteria**
- Review document exists and records: current tier, limit values, observed scheduling workload, and a documented decision
- Decision is signed off by FinOps & Resource Architect and Infrastructure & Operations Owner
- If paid tier is warranted: a follow-up backlog item is created (not part of this scope)

---

### BLG-BE-06 — Alert evaluation idempotency
**Priority:** P2 (Medium)
**Type:** Backend Engineering
**Owner:** Backend Engineering Patterns Owner
**Source:** Roadmap rebalance cycle 2026-03-31__scheduled (IDEA-backend-engineering-20260321-02 advancing) — 2026-03-31
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.4

**Problem**
BLG-OPS-04 (cron scheduling) runs the alert evaluation endpoint daily. If the scheduler retries, misfires, or is manually triggered on a day already evaluated, users receive duplicate alert notifications. There is no deduplication mechanism on the notification dispatch layer to prevent a second notification being sent for the same rule on the same trading day.

**Scope**
- Add a deduplication key (rule_id + trading_day) on the notification dispatch layer only
- Before sending a notification, check: was a notification for this rule already dispatched today?
- If yes: skip dispatch (log as deduplicated); if no: send and record
- The evaluation pipeline itself is NOT affected — evaluation continues to run regardless
- Scope is strictly notification dispatch deduplication, not evaluation suppression

**Acceptance Criteria**
- If alert evaluation runs twice on the same trading day, only one notification is sent per rule per day
- The evaluation pipeline executes both times (no evaluation is suppressed)
- Deduplication is logged (identifiable in logs that a dispatch was skipped as duplicate)
- Explicitly confirmed: evaluation pipeline is not locked or suppressed by this change
- Spec: deduplication behaviour documented in alert evaluation spec

---

### BLG-GOV-09 — Cycle velocity metric
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead + Head of Engineering
**Source:** Roadmap rebalance cycle 2026-03-31__scheduled (IDEA-pmo-lead-20260321-01 advancing) — 2026-03-31
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.4

**Problem**
The roadmap and release planning engines lack longitudinal throughput data. Each release planning cycle estimates capacity from scratch without reference to historical story completion rates. v2.3 triggered a capacity warn that an earlier baseline might have predicted. Without a velocity metric, recurring over-planning patterns are invisible until they manifest as sprint slippage.

**Scope**
- Define a simple velocity metric: stories completed / stories planned per sprint, per cycle
- Back-fill metric values for the last 6 cycles from existing cycle artefacts (run manifests, execution_state.json)
- Add a "Cycle Velocity" section to the run_manifest.md template (update roadmap_prompt.md STEP 1.1)
- Surface the last 3 cycles' velocity figures as context at the start of each roadmap rebalance run manifest

**Acceptance Criteria**
- Velocity metric is defined and documented (stories completed / planned per sprint)
- Last 6 cycles' velocity figures are recorded in a persistent document or manifest section
- run_manifest.md template includes a velocity section populated at each rebalance run
- Release planning can reference velocity data without re-deriving it from cycle artefacts each time

---

---

### BLG-FEAT-15 — Fee drag metric on Trade History
**Priority:** P3 (Low)
**Type:** Feature — Analytics
**Owner:** Metrics Definitions & Analytics Owner + Head of Engineering
**Source:** PO/Challenger debate 2026-04-02 — action A3 from slippage metric re-scope decision
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v2.5

**Problem**
The current "entry deviation" metric (fill price vs limit price at entry) is null for most trades because the fill price field is optional and only available at entry. There is no always-available metric that captures the friction cost of executing a trade. Traders cannot see how much of their proceeds are consumed by broker fees (commission, stamp duty, FX fee) without manually inspecting individual trade records.

**Scope**
- Add a **Fee Drag %** metric: `exit_fees / gross_proceeds × 100` — the percentage of gross exit proceeds consumed by transaction costs at exit
- Surface as a new StatsCard on Trade History ("Avg Fee Drag") — distinct from existing Avg Entry Dev. card
- Surface as a new column in TradeHistoryTable ("Fee Drag %") — always populated (exit_fees and gross_proceeds always stored)
- Avg Fee Drag: mean of fee_drag_pct across all trades with non-zero gross_proceeds
- Update `docs/specs/metrics_definitions.md` to define the formula canonically
- Update `docs/specs/frontend/pages/trade_history.md` to spec the new column and StatsCard
- Update `docs/specs/api_contracts/trade_endpoints.md` to add `fee_drag_pct` and `avg_fee_drag_pct` response fields
- Update `docs/reference/openapi.yaml` for the new fields
- No data model migration required — `exit_fees` and `gross_proceeds` already stored on `trade_history`

**Acceptance Criteria**
- `fee_drag_pct` field returned per trade in GET /trades response: `exit_fees / gross_proceeds × 100`, rounded to 2 dp
- `avg_fee_drag_pct` field returned at response envelope level: mean across all trades with gross_proceeds > 0
- "Avg Fee Drag" StatsCard visible on Trade History; displays `avg_fee_drag_pct` formatted as `+X.XX%`
- Fee Drag % column present in TradeHistoryTable; always populated (no `—` for missing data)
- `docs/specs/metrics_definitions.md` contains canonical definition of fee_drag_pct formula
- Metric is labelled clearly as "Fee Drag %" throughout — never called "slippage"

**Out of scope**
- Entry-side fee drag (entry_fees / total_cost) — defer to future item
- Round-trip friction (entry + exit fees combined) — defer to future item
- Any change to existing entry deviation / slippage_pct metric

---

## 14. New Backlog Items — Session 2026-04-02

*User-raised items from session review. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

### BLG-OPS-11 — Add `--max-time` to GitHub Actions cron curl calls
**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** InfraOps review of ST-10 Render tier decision record — 2026-04-02
**Effort:** XS (<1h)
**Provisional-Target:** v2.5

**Problem**
`alert-evaluation.yml` and `daily-snapshot.yml` both invoke `curl` with no `--max-time` flag. On Render free tier, the web service spins down after 15 minutes of inactivity. When the GitHub Actions cron fires and the service is cold, the curl call stalls silently for ~50–60 seconds before the cold start completes and the request is served. This is not a failure — the request eventually succeeds — but it creates confusing workflow logs with no visible progress and unpredictable job duration.

**Scope**
- Add `--max-time 120` to every `curl` call in `.github/workflows/alert-evaluation.yml`
- Add `--max-time 120` to every `curl` call in `.github/workflows/daily-snapshot.yml`
- No other changes required

**Acceptance Criteria**
- Both workflow files have `--max-time 120` on all curl invocations
- The flag gives curl a 120-second hard ceiling — accommodating the worst-case cold start (~60s) plus endpoint execution time, with margin
- If the service fails to respond within 120s the workflow step fails with a non-zero exit code rather than hanging indefinitely

---

---

## 15. New Backlog Items — Session 2026-04-03

*Items raised from ST-11 performance baseline and System Status page review. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

### BLG-OPS-12 — Fix auth forwarding in POST /test/endpoints internal calls
**Priority:** P2 (High)
**Type:** Operational / Infrastructure
**Owner:** Head of Engineering + Infrastructure & Operations Owner
**Source:** ST-11 performance baseline review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5

**Problem**
`backend/services/health_service.py` `test_all_endpoints()` makes internal HTTP calls to each endpoint without forwarding the `X-API-Key` header. All auth-protected endpoints return 401 and are reported as "fail". The System Status page "Run Tests" button currently shows 1/17 pass rate, making the system appear critically broken when all endpoints are in fact operational. This makes the monitoring tool unreliable and misleading.

**Scope**
- Modify `test_all_endpoints()` to accept and forward the API key in internal calls (e.g. accept `api_key: str = None` parameter, add `X-API-Key` header when provided)
- Update `POST /test/endpoints` route in `main.py` to extract the `X-API-Key` from the incoming request and pass it through
- Alternatively: add a middleware bypass for server-internal calls (e.g. `X-Internal: true` header checked before auth)

**Acceptance Criteria**
- `POST /test/endpoints` returns pass/fail based on actual endpoint response, not auth rejection
- All correctly implemented endpoints report "pass" when the system is healthy
- Success rate shown on System Status page reflects actual endpoint health

---

### BLG-OPS-13 — Keep endpoint test list in sync with openapi.yaml
**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** ST-11 performance baseline review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5

**Problem**
The endpoint test list in `backend/services/health_service.py` `test_all_endpoints()` was last updated for v2.2 (12 endpoints). Endpoints added in v2.3 (`/positions/compliance`, `/alerts/rules`, `/alerts/history`, `/notifications`, `/notifications/preferences`) and v2.4 (`/digest/weekly`, analytics endpoints) are not being tested. This coverage gap will worsen each sprint if not addressed structurally.

**Scope**
- Add all missing parameterless GET endpoints to the test list in `test_all_endpoints()`:
  - `/positions/compliance`
  - `/alerts/rules`
  - `/alerts/history`
  - `/notifications`
  - `/notifications/preferences`
  - `/digest/weekly`
  - `/analytics/cohort?period=month`
  - `/analytics/r-multiple-distribution`
  - `/analytics/compliance-metrics`
  - `/health/detailed`
- Add a comment block above the list referencing `docs/reference/openapi.yaml` as the source of truth
- Update the System Status page placeholder text ("Tests 17 endpoints") to match actual count

**Acceptance Criteria**
- All parameterless GET endpoints in `openapi.yaml` are present in the test list
- A comment in `health_service.py` documents the sync obligation (update when endpoints are added)
- System Status page "Run Tests" button tests the complete current endpoint set

---

### BLG-BE-07 — Investigate high external baseline latency on DB-backed endpoints
**Priority:** P2 (High)
**Type:** Backend / Infrastructure
**Owner:** Head of Engineering
**Source:** ST-11 performance baseline — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5

**Problem**
The ST-11 performance baseline shows all DB-backed endpoints have p50 response times of 1.2–6.0 seconds when measured from an external client against staging. The consistent latency floor of ~1,100ms across unrelated endpoints suggests this is Supabase free tier DB connection establishment overhead (no persistent pool), not query-level slowness. Two outliers warrant query-level investigation: `GET /portfolio` (p50=5,979ms) and `GET /notifications/preferences` (p50=4,631ms) are significantly slower than peers with similar expected query complexity.

**Scope**
- Profile `GET /portfolio` to identify why it is ~2× slower than other multi-query endpoints — likely involves ATR calculation or multiple sequential DB round-trips; optimise or parallelise
- Profile `GET /notifications/preferences` to identify why a single-row lookup takes 4.6s — check for N+1 queries or missing index
- Investigate Supabase connection pooling options for Render free tier (e.g. PgBouncer on Supabase, SQLAlchemy `pool_size`/`pool_pre_ping` settings)
- Re-run the performance baseline after any fixes and update `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- Root cause of `GET /portfolio` and `GET /notifications/preferences` outlier latency identified and documented
- Either a fix is applied that brings the outliers within 2× of peer endpoint latency, OR a documented architectural constraint explains why optimisation is not feasible on free tier
- Updated baseline document filed if connection pooling or query optimisation changes are made

---

### BLG-FE-07 — Fix System Status endpoint categorisation for v2.3/v2.4 routes
**Priority:** P4 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Engineer
**Source:** System Status page review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5

**Problem**
`src/pages/SystemStatus.js` `categorizeEndpoint()` does not cover routes added in v2.3/v2.4. Endpoints matching `/alerts`, `/notifications`, and `/digest` all fall through to the "Other" category instead of being correctly grouped. When BLG-OPS-12 and BLG-OPS-13 are resolved and the test runner covers these endpoints, they will appear under a generic "Other" group rather than meaningful categories.

**Scope**
- Add categorisation rules to `categorizeEndpoint()` in `SystemStatus.js`:
  - `/alerts` → "Alerts"
  - `/notifications` → "Notifications"
  - `/digest` → "Digest"
  - `/health` → "Core" (already covered but verify `/health/detailed` maps correctly)
  - `/validate` → should map to "Validation" (already covered)
  - `/analytics` → "Analytics" (already covered — verify)
- Add matching `categoryConfig` entries for "Alerts" and "Notifications" with appropriate icons and colours

**Acceptance Criteria**
- Alert endpoints appear under "Alerts" category in System Status Endpoint Tests panel
- Notification endpoints appear under "Notifications" category
- Digest endpoints appear under "Digest" category
- No endpoints fall into "Other" except `/` (root) and any future unclassified additions

---

### BLG-FE-08 — Fix Avg Slippage StatsCard gradient rendering
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** DEV-ST14-01 — delivery verification 2026-03-31__release-v2.4 — 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5
**Deviation ref:** DEV-ST14-01 (P3 cosmetic — pre-accepted by Director of Quality 2026-03-20)

**Problem**
The Avg Slippage StatsCard on the Reports/Slippage Tracking page renders without a gradient background. The functional value is correct and colour-coded. The cosmetic deviation (gradient missing) was accepted as P3 by Director of Quality 2026-03-20 and recorded in `docs/testing/slippage_scenarios.md §5`. Note: prior reference BLG-FE-01 in the deviation note was stale (BLG-FE-01 is an archived v2.2 item). This item supersedes that reference.

**Scope**
- Apply the correct Tailwind gradient class to the Avg Slippage StatsCard component
- Confirm rendering matches other StatsCard components on the Reports page

**Acceptance Criteria**
- Avg Slippage StatsCard renders with gradient background matching other StatsCard components
- No regression to functional slippage value display or colour coding

---

### BLG-GOV-10 — Fix governance_sync.yml batch push issue closure
**Priority:** P2 (Medium)
**Type:** Governance Process / DevOps
**Owner:** DevOps
**Source:** EPIC-06 merge observation — delivery verification 2026-03-31__release-v2.4 — 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5

**Problem**
`governance_sync.yml` uses `git log -1` to extract the issue number from a push event, so only the most recent commit's GitHub issue is closed automatically. When EPIC-06 was pushed as a 4-commit batch (ST-14, ST-15, ST-16, ST-17), only ST-17's issue (#164) was closed. Issues #161/162/163 remained open and required manual closure with explanatory comments. Any multi-commit push to an exec branch will silently leave earlier issues unclosed.

**Scope**
- Update `governance_sync.yml` to extract all commit messages in the push using `git log $BEFORE..$AFTER` (not `git log -1`)
- Close every issue referenced in the push range, not just the last

**Acceptance Criteria**
- Multi-commit batch push to an exec branch closes all referenced GitHub issues
- Single-commit push behaviour unchanged
- Tested with a 2+ commit push on a test branch

---

### TEST-GAP-EPIC-01-v24 — Create test scenarios for EPIC-01 backend correctness fixes
**Priority:** P2 (Medium)
**Type:** QA Coverage
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-31__release-v2.4 — TSG-v24-01 — 2026-04-03
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.5

**Problem**
EPIC-01 shipped three backend correctness fixes (ST-01 ATR conversion, ST-02 notification deduplication, ST-03 initial stop price join) with no automated test scenarios. These are correctness-critical behaviours — ATR calculation errors caused the original BLG-BE-05 defect, and deduplication logic is invisible to manual review. Without scenarios, regressions in these areas will only be caught at staging observation or by user reports.

**Scope**
- Author test scenarios covering:
  - SC-ATR-01: ATR pence→GBP conversion for .L tickers (always-on, no guard)
  - SC-DEDUP-01: Notification dispatch deduplication (same rule, same day)
  - SC-DEDUP-02: Evaluation pipeline not suppressed when dedup fires
  - SC-STOP-01: stop_price field present on analytics endpoint response for trades with a known initial_stop
- Add to appropriate scenario file(s) in `docs/testing/`
- Reference in test scenario index

**Acceptance Criteria**
- Scenario file(s) present covering all four scenarios
- Each scenario specifiable as executable against staging or unit test suite
- Referenced in test scenario index

---
