**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.4
**Cycle:** 2026-03-31__release-v2.4
**Last Updated:** 2026-03-31

---

# Release Backlog Slice — v2.4 Correctness, Insight & Governance Hardening

17 stories across 6 EPICs | 3 sprints planned

---

## EPIC-01 — Backend Correctness & Alert Reliability

Maps to: S2-01

Owner: Head of Engineering + Backend Engineering Patterns Owner

**Sprint assignment:** Sprint 2

---

### ST-01 — Fix ATR pence→GBP conversion for UK (.L) tickers

**EPIC:** EPIC-01
**Backlog ref:** BLG-BE-05
**Priority:** P2 (Medium)
**Effort:** XS (<1 hour)
**Sprint:** Sprint 2

**Description**
`calculate_atr()` in `backend/utils/pricing.py` applies the pence→GBP conversion (`atr / 100`) only when `atr > 100`. Yahoo Finance returns ATR in pence for all LSE `.L` tickers regardless of magnitude. Remove the guard condition and always divide by 100 for `.L` tickers.

**Acceptance Criteria**
- `calculate_atr('LGEN.L', ...)` returns ATR in GBP (e.g. ~0.10) not pence (~10.23)
- `calculate_initial_stop(2.45, atr)` returns a positive value in range £1.80–£2.40 for LGEN
- No regression: existing unit tests for ATR pass; high-ATR stocks (e.g. TSLA) unaffected

---

### ST-02 — Add notification dispatch deduplication for alert evaluation

**EPIC:** EPIC-01
**Backlog ref:** BLG-BE-06
**Priority:** P2 (Medium)
**Effort:** M (~1–2 days)
**Sprint:** Sprint 2

**Description**
Add a deduplication key (rule_id + trading_day) on the notification dispatch layer. Before sending a notification, check whether a notification for this rule was already dispatched today. If yes: skip dispatch (log as deduplicated); if no: send and record. Evaluation pipeline is NOT affected — it continues to run regardless.

**Acceptance Criteria**
- If alert evaluation runs twice on the same trading day, only one notification is sent per rule per day
- The evaluation pipeline executes both times (no evaluation is suppressed)
- Deduplication is logged (identifiable in logs that a dispatch was skipped as duplicate)
- Explicitly confirmed: evaluation pipeline is not locked or suppressed by this change
- Spec: deduplication behaviour documented in alert evaluation spec

---

### ST-03 — Expose initial stop price on analytics trade endpoint

**EPIC:** EPIC-01
**Backlog ref:** BLG-BE-04
**Priority:** P3 (Low)
**Effort:** S (~2–3 hours)
**Sprint:** Sprint 2

**Description**
Extend the analytics endpoint (or trade history endpoint) to JOIN `positions.initial_stop` into the `trade_history` response, or expose `initial_stop` as `stop_price` on closed trade objects returned to the frontend. Update `RMultipleAnalysis.js` filter if the field name changes.

**Acceptance Criteria**
- Closed trades returned to analytics page include a `stop_price` (or `initial_stop`) field where available
- R-Multiple Analysis section renders correctly for trades where stop prices were set at entry
- `RMultipleAnalysis.js` filter produces correct `tradesWithR` count
- `openapi.yaml` updated in same commit if response shape changes

---

## EPIC-02 — Frontend & UX Polish

Maps to: S2-02

Owner: Frontend Specs & UX Documentation Owner

**Sprint assignment:** Sprint 2

---

### ST-04 — Fix missing P&L (GBP) column on Positions page

**EPIC:** EPIC-02
**Backlog ref:** BLG-FE-06
**Priority:** P2 (Medium)
**Effort:** S (~0.5 day)
**Sprint:** Sprint 2

**Description**
The Positions page Table View does not display the "P&L (GBP)" absolute value column. `positions.md` v1.4 lists both "P&L (GBP)" and "P&L %" as separate columns. Investigate whether the column is missing or rendered but hidden; add or unhide it. Ensure GBP value is colour-coded per spec.

**Acceptance Criteria**
- Positions Table View displays a P&L column showing the absolute GBP value (e.g. £70.05 for LGEN, £96.05 for BARC from seed data)
- Positive GBP P&L values render in green; negative values render in red
- P&L % column remains present alongside the GBP column
- V-PATH2-01 passes on staging: £70.05 and £96.05 visible in green after seeding

---

### ST-05 — Add user-facing error message mapping layer

**EPIC:** EPIC-02
**Backlog ref:** BLG-FE-03
**Priority:** P3 (Low)
**Effort:** S-M (~1 day)
**Sprint:** Sprint 2

**Description**
Backend API errors currently surface as raw status codes or technical messages in the UI. Create a frontend error mapping layer: HTTP status code + error code → user-readable message. Apply consistently across all API-consuming components.

**Acceptance Criteria**
- API errors display a user-readable message rather than a raw code or "undefined"
- Error mapping covers all error codes defined in the Error Response Standard (BLG-SPEC-G2, shipped v2.1)
- Raw technical details logged to console (not shown to user)
- No regression to existing error display behaviour

---

## EPIC-03 — Spec Debt Resolution

Maps to: S2-03

Owner: API Contracts & Documentation Owner + Head of Engineering

**Sprint assignment:** Sprint 1

---

### ST-06 — Reconcile portfolios table schema in data_model.md

**EPIC:** EPIC-03
**Backlog ref:** BLG-SPEC-D15
**Priority:** P2 (Medium)
**Effort:** XS (<1 hour)
**Sprint:** Sprint 1

**Description**
`data_model.md` documents `portfolios` with `id, cash, initial_cash, created_at, last_updated`. The deployed DB has `id, cash, created_date, last_updated` — `initial_cash` doesn't exist and `created_at` is `created_date`. Run `\d portfolios` on staging to confirm, then update the spec.

**Acceptance Criteria**
- `data_model.md` portfolios CREATE TABLE matches `\d portfolios` output on staging
- `initial_cash` either removed from spec or present in DB — no divergence
- `created_date` vs `created_at` discrepancy resolved
- `data_model.md` version bumped; §6 checklist applied

---

### ST-07 — Reconcile trade_history table schema in data_model.md

**EPIC:** EPIC-03
**Backlog ref:** BLG-SPEC-D16
**Priority:** P2 (Medium)
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1

**Description**
`data_model.md` documents `trade_history` with `exit_proceeds`. `database.py:create_trade_history()` uses `gross_proceeds, net_proceeds, entry_fees, exit_fees`. Run `\d trade_history` on staging. Determine canonical column set and update spec and code to match.

**Acceptance Criteria**
- `data_model.md` trade_history CREATE TABLE matches `\d trade_history` on staging
- `database.py:create_trade_history()` column list matches the spec
- `seed_portfolio_trades.sql` trade_history INSERT uses confirmed column names and succeeds
- `data_model.md` version bumped; §6 checklist applied

---

## EPIC-04 — Weekly Trading Digest

Maps to: S2-04

Owner: Backend Engineering Patterns Owner + Frontend Specs & UX Documentation Owner

**Sprint assignment:** Sprint 3

*Scope constraint: Raw data only. No generated text, narrative, or interpretation in any response field. This constraint was confirmed in Challenger debate (roadmap rebalance 2026-03-31).*

---

### ST-08 — Implement weekly digest backend endpoint

**EPIC:** EPIC-04
**Backlog ref:** BLG-FEAT-14 (BE component)
**Priority:** P2 (Medium)
**Effort:** M (~1–2 days)
**Sprint:** Sprint 3

**Description**
New backend endpoint returning: 7-day realised P&L, unrealised P&L delta, alerts fired vs dismissed count, compliance score (current + 7-day trend), staleness indicator summary. Response must contain raw numeric/boolean fields only — no generated text, narrative, or interpretation.

**Acceptance Criteria**
- Endpoint returns all specified fields for the past 7 days
- Response contains raw numeric/boolean fields only — no generated text, narrative, or interpretation
- Spec entry added to relevant api_contracts document
- AC explicitly confirmed: no generated text or interpretation present in any response field
- `openapi.yaml` updated in same commit as contract definition

---

### ST-09 — Add weekly digest frontend component

**EPIC:** EPIC-04
**Backlog ref:** BLG-FEAT-14 (FE component)
**Priority:** P2 (Medium)
**Effort:** M (~1–2 days)
**Sprint:** Sprint 3
**Depends on:** ST-08

**Description**
Frontend digest component rendering the weekly digest endpoint data as a structured data table. Must not include any commentary, interpretation, or generated text — display raw numeric fields from the API only.

**Acceptance Criteria**
- Frontend renders digest as a data table (not commentary format)
- All fields from ST-08 endpoint are displayed
- No generated text or interpretive copy rendered in the component
- Component accessible from main navigation or dashboard

---

## EPIC-05 — Operational Readiness

Maps to: S2-05

Owner: Infrastructure & Operations Owner + PMO Lead + QA & Testing Owner

**Sprint assignment:** Sprint 1 (ST-10, ST-12, ST-13) + Sprint 2 (ST-11)

---

### ST-10 — Render hosting tier review and decision record

**EPIC:** EPIC-05
**Backlog ref:** BLG-OPS-10
**Priority:** P3 (Low)
**Effort:** XS (<1 hour)
**Sprint:** Sprint 1

**Description**
Document current Render plan tier and free tier limits. Review BLG-OPS-04 cron scheduling workload against those limits. Record a decision: free tier sufficient | paid tier warranted now | monitor for N sprints.

**Acceptance Criteria**
- Review document exists recording: current tier, limit values, observed scheduling workload, and a documented decision
- Decision is signed off by FinOps & Resource Architect and Infrastructure & Operations Owner
- If paid tier warranted: a follow-up backlog item is created (not part of this scope)

---

### ST-11 — Document API endpoint performance baseline

**EPIC:** EPIC-05
**Backlog ref:** BLG-OPS-05
**Priority:** P3 (Low)
**Effort:** S (~0.5–1 day)
**Sprint:** Sprint 2

**Description**
Instrument and document p50/p95 response times for all currently active API endpoints using existing integration test infrastructure or a simple timing script. Produce a baseline document. Flag any endpoint already outside acceptable thresholds.

**Acceptance Criteria**
- Response time baseline documented for all endpoints defined in `openapi.yaml`
- p50 and p95 values recorded
- Any endpoint with p95 > 500ms flagged for investigation
- Baseline document filed in `docs/` or as a test artefact

---

### ST-12 — Create slippage tracking test scenario file

**EPIC:** EPIC-05
**Backlog ref:** TEST-GAP-EPIC-05-SLIP
**Priority:** P3 (Low)
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1

**Description**
Author SC-SLIP-01 through SC-SLIP-04 covering: fill price input on trade entry, slippage % column display (colour-coded), avg slippage StatsCard update, null fill price shows "—". Add to `docs/testing/reports_scenarios.md` or a new `slippage_scenarios.md`.

**Acceptance Criteria**
- Scenario file present covering all four slippage tracking scenarios
- Scenarios executable against staging without additional setup
- Referenced in the test scenario index

---

### ST-13 — Define cycle velocity metric and backfill 6 cycles

**EPIC:** EPIC-05
**Backlog ref:** BLG-GOV-09
**Priority:** P3 (Low)
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1

**Description**
Define a simple velocity metric: stories completed / stories planned per sprint, per cycle. Back-fill metric values for the last 6 cycles from existing cycle artefacts. Add a "Cycle Velocity" section to the run_manifest.md template (update roadmap_prompt.md STEP 1.1).

**Acceptance Criteria**
- Velocity metric is defined and documented (stories completed / planned per sprint)
- Last 6 cycles' velocity figures are recorded in a persistent document or manifest section
- run_manifest.md template includes a velocity section populated at each rebalance run
- Release planning can reference velocity data without re-deriving from cycle artefacts each time

---

## EPIC-06 — Governance Engine Maintenance

Maps to: S2-06

Owner: Head of Specs Team

**Sprint assignment:** Sprint 1

*Non-deferrable: Contains action-now priority items from v2.3 carry-forward (CF-1, CF-3). Must complete in Sprint 1.*

---

### ST-14 — Apply action-now execution_prompt.md patches (second recurrences)

**EPIC:** EPIC-06
**Backlog ref:** v2.3 lessons_learnt_closure.md outstanding deferred patches (LL-v2.2-EX-01/02/04, second recurrence)
**Priority:** P2 (Medium — governance non-compliance risk)
**Effort:** S (~0.5–1 day)
**Sprint:** Sprint 1

**Description**
Apply stronger gate language to `execution_prompt.md` for three items that recurred a second time in v2.3 despite v2.2 patches:

1. **LL-v2.2-EX-01**: STEP 3.1.A — delegation log must be updated in-flight at unblock, not batched at STEP 5.0. Strengthen gate language from advisory to required check.
2. **LL-v2.2-EX-02**: STEP 4 merge gate completion block — add explicit guard preventing delivery verification invocation before STEP 5 completion (all_merged=true session advisory insufficient; needs a formal check).
3. **LL-v2.2-EX-04**: §9.1 schema note — `spec_references` may be explicitly empty for tooling/infrastructure items where no prior spec is applicable; add a clear positive-assertion rule so the traceability gap check does not false-positive on empty spec_references for these item types.

Update OPERATIONAL_GUIDE.md and prompt_change_log.md per §6 checklist.

**Acceptance Criteria**
- All three items addressed in `execution_prompt.md`
- `execution_prompt.md` version bumped; §6 checklist applied (OPERATIONAL_GUIDE + prompt_change_log updated)
- No governance intent or hard gate logic removed

---

### ST-15 — Apply delivery_verification_prompt.md deviation compliance patch

**EPIC:** EPIC-06
**Backlog ref:** v2.3 lessons_learnt_closure.md Friction Item 1 (deferred patch)
**Priority:** P2 (Medium — governance gap)
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1

**Description**
`delivery_verification_prompt.md` STEP 3 (Deviation Register): after creating a backlog item for a P1/P2/P3 deviation, verify that the canonical spec named in the deviation record has a Known Deviations section with an entry for this deviation. If absent: create the section and entry in the same session. This closes the gap where v2.3 post-ship closure was the first gate to enforce canonical spec propagation.

Update OPERATIONAL_GUIDE.md and prompt_change_log.md per §6 checklist.

**Acceptance Criteria**
- `delivery_verification_prompt.md` STEP 3 updated with canonical spec Known Deviations check
- `delivery_verification_prompt.md` version bumped; §6 checklist applied
- OPERATIONAL_GUIDE.md + prompt_change_log.md updated in same commit

---

### ST-16 — Update execution_prompt.md delegation model and add delegation log line count check

**EPIC:** EPIC-06
**Backlog ref:** v2.3 lessons_learnt_closure.md Friction Item 2 + carry-forward CF-2
**Priority:** P3 (Low)
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1

**Description**
Two related changes to `execution_prompt.md`:

1. **Friction Item 2 (delegation log check)**: Before STEP 7 sprint close commit, verify that `delegation_log.md` line count is consistent with `execution_state.json.delegated_items` count. If suspiciously low (fewer than 10 lines when delegated_items is non-empty), surface a warning and require confirmation before proceeding with `git add`.

2. **CF-2 (delegation model update)**: Update `execution_prompt.md` §5.1 Delegation Classification table `delegated_frontend` entry — description still references "Base44 code generation pattern". This model is superseded by engine-autonomous delivery (decision 2026-03-26). Update description to reflect autonomous/engine delivery model.

Update OPERATIONAL_GUIDE.md and prompt_change_log.md per §6 checklist.

**Acceptance Criteria**
- `execution_prompt.md` STEP 7 includes pre-commit delegation_log.md line count check
- `execution_prompt.md` §5.1 `delegated_frontend` entry updated to reflect autonomous engine delivery model
- `execution_prompt.md` version bumped; §6 checklist applied
- OPERATIONAL_GUIDE.md + prompt_change_log.md updated in same commit

---

### ST-17 — Simplify release planning cycle artefact sealing

**EPIC:** EPIC-06
**Backlog ref:** BLG-GOV-03
**Priority:** P3 (Low)
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1

**Description**
Remove per-artefact SHA-256 hash computation from the release planning engine. For a 2-person team, the primary threat (accidental writes) is already covered by write scope restrictions; `git diff` catches post-publish modifications. Retain `sealed: true` flag as the sole sealing mechanism. Retain `state_snapshot_hash` as a single lightweight checksum.

Update OPERATIONAL_GUIDE.md and prompt_change_log.md per §6 checklist.

**Acceptance Criteria**
- Release planning engine no longer computes or verifies per-artefact SHA-256 hashes
- `state.json` schema updated — `sealed_hashes` and `artifact_hashes` blocks removed
- `sealed: true` flag check remains and is enforced as a hard gate
- All references to hash drift detection removed from prompt and shared_standards
- `release_planning_prompt.md` version bumped; §6 checklist applied
