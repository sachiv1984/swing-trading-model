# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-03-31 (session — 1 new item added: BLG-FEAT-12)
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

## 12. Active Release Slice

*v2.3 shipped 2026-03-30. v2.3 release slice archived. v2.4 scope TBD — pending roadmap rebalance and release planning.*

---

## 13. New Backlog Items — Session 2026-03-31

*User-raised items from session review. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

### BLG-FEAT-12 — Add gated feature rollout capability
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
