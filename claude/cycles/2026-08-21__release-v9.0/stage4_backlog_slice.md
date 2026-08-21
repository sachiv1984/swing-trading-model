Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-21
Cycle: 2026-08-21__release-v9.0
Release: v9.0

# Backlog Slice — v9.0

<!-- release-plan-marker: RP:v9.0:2026-08-21__release-v9.0 -->

27 stories across 5 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope widened to the top of the confirmed ~24–28 day/sprint capacity band per Product Owner decision (2026-08-21, explicit "use full capacity" instruction). Led by 5 correctness/follow-through items surfaced directly by v8.9's own PR-review process, including one live production data-correctness bug.

---

## EPIC-01 — AI Post-Trade Debrief & Backtest Correctness Follow-Through

**Maps to:** S2-01
**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; AI Compliance & Governance Officer

### ST-01 — Fix nightly backtest rebalance-date computation to exclude the current in-progress month
**Source:** BLG-BE-109
**Priority:** P1 (High)
**Effort:** S
**Acceptance Criteria:**
- `rebalance_dates` never includes a date from the current, incomplete calendar month in either `production_strategy.py` or `backend/services/backtest_rule_service.py`
- Regression test added and passing for the mid-month case
- `tests/backtest_data_integrity_smoke_test.py`-class checks re-verified passing (no new invariant broken)
- Backend Engineering Patterns Owner sign-off

### ST-02 — Configure root/app logging so logger.info() calls actually reach Render's captured logs
**Source:** BLG-BE-107
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- Root logging is configured such that `logger.info()` calls from any `backend/` module reach stdout/stderr in the running process
- A real post-deploy production invocation confirms at least the `si05_digest_service.py` duration line is now captured in Render logs
- No regression to uvicorn's own existing access/error log formatting or duplicate log lines
- `docs/ops/api_performance_baseline.md` §36 updated with the real log-derived timing

### ST-03 — Decide "linked journal entries" data source for the AI Post-Trade Debrief
**Source:** BLG-BE-108
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- Product Owner decision recorded (keep `red_flag_events`-only, add entry/exit notes, or both)
- If implementation changes: `tests/test_debrief_service.py` covers the new data source; full backend suite re-verified passing
- Spec updated to reflect the confirmed interpretation of "linked journal entries"

### ST-04 — Fix debrief-generation prompt's unverifiable cross-trade pattern language
**Source:** BLG-TECH-17
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- The prompt's encouraged phrasing style matches what the numeric cross-check can actually verify — no encouraged claim type is systematically un-verifiable
- `tests/test_debrief_service.py` covers the chosen fix (either an added-source-value verification case, or a removed-phrasing regression test)
- Backend Engineering Patterns Owner sign-off

### ST-05 — Consolidate backtest_rule_service.py's ported algorithm functions with production_strategy.py
**Source:** BLG-TECH-15
**Priority:** P2 (Medium)
**Effort:** M
**Depends on:** ST-01 (same rebalance-date computation surface)
**Acceptance Criteria:**
- Exactly one implementation of `compute_signals`/`compute_atr`/`compute_risk_on`/`transaction_fee`/`backtest` exists; both `production_strategy.py` and `backend/services/backtest_rule_service.py` use it
- Nightly backtest and the in-app Backtest Rule Change endpoint both continue to produce the same historical results as before the consolidation (regression-verified against a fixed historical run)
- Backend Engineering Patterns Owner and Strategy Rules & System Intent Owner sign-off

---

## EPIC-02 — Live Risk-Management & Trade-Plan Data-Integrity Closure

**Maps to:** S2-02
**Owner:** Backend Engineering Patterns Owner; Product Owner; Frontend Specifications & UX Documentation Owner; Director of Quality

### ST-06 — Audit and backfill open positions against the breakeven-floor stop invariant
**Source:** BLG-BE-105
**Priority:** P1 (High)
**Effort:** S
**Acceptance Criteria:**
- Live-DB query confirms the count of open profitable positions with `current_stop < entry_price`, before and after correction
- Any positions found are corrected via the existing floored calculation path (no new inline stop-adjustment logic)
- Result recorded (count found, count corrected, date) — closes the deferred v8.9 ST-01 AC from `BLG-BE-102`
- Backend Engineering Patterns Owner sign-off

### ST-07 — Decide and apply treatment for trade_plans.setup_type="Other" conflating user-chosen-Other with never-classified
**Source:** BLG-FEAT-93
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Decision recorded (distinguish explicit-Other from never-classified, or accept the conflation with documented rationale)
- If implemented, `win_rate_by_setup_type`'s future query logic (or its predesign doc) is updated to reflect the distinction
- Product Owner sign-off

### ST-08 — Add a lock around ensure_trade_plans_table()'s memoization flag
**Source:** BLG-BE-106
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- The flag check-and-set is guarded by a lock
- A regression test demonstrates two concurrent calls only execute the DDL block once (or confirms serialization)
- No behaviour change to callers

### ST-09 — Add down-migration rollback verification tests for the 5 most recent schema migrations
**Source:** BLG-BE-49
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- 5 migrations have passing rollback tests
- Pattern documented for future migrations

### ST-10 — Close the What-If Sizing Preview FX-rate reproducibility gap for US-market plans
**Source:** BLG-FE-164
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- `trade_plan.md` §5d.3's reproducibility claim is either made accurate (FX override field added) or explicitly scoped to note the US-market live-rate caveat
- Frontend Specifications & UX Documentation Owner sign-off

### ST-11 — Add Playwright coverage for UK-market position on current_trailing_stop_native
**Source:** BLG-QA-153
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- New Playwright test(s) cover a UK-market position's Trail Stop tile/cell rendering
- Test passes against current implementation
- Director of Quality sign-off

---

## EPIC-03 — Operational Resilience & Deploy-Path Safeguards

**Maps to:** S2-03
**Owner:** Infrastructure & Operations Owner; Director of Quality

### ST-12 — Production database backup/restore drill
**Source:** BLG-OPS-103
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- Current backup mechanism documented
- One full restore drill performed against a non-production target confirming the procedure works

### ST-13 — Automated staging smoke test on deploy/merge
**Source:** BLG-OPS-25
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- Smoke test suite authored and triggered on staging deploy / merge to main
- Suite covers minimum 3 critical endpoints
- Failure prevents "staging ready" signal from being issued
- Suite also runs on a scheduled cadence and alerts on failure independent of deploy events
- Confirmed to fail correctly on a deliberately-broken staging deploy (dry run)

### ST-14 — Staging environment drift detector
**Source:** BLG-OPS-90
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- Automated drift detection built covering both confirmed incident shapes (missing-deploy per `BLG-OPS-82`; dashboard-only build-path filter per this item's own gate-clearing incident)
- Infrastructure & Operations Owner sign-off

### ST-15 — Confirm production PUBLIC_URL is actually set in the Render dashboard
**Source:** BLG-OPS-147
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- Production `PUBLIC_URL` dashboard value confirmed one way or the other, documented in this item's resolution

### ST-16 — Add CI safeguard to catch future PUBLIC_URL/asset-path regressions on GitHub Pages deploy
**Source:** BLG-OPS-148
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- `deploy.yml` fails fast if a future build produces root-relative (or otherwise wrong-subpath) asset paths in `build/index.html`
- A deliberate local test (temporarily unsetting the `PUBLIC_URL` override) confirms the new step actually catches the regression
- Infrastructure & Operations Owner sign-off

---

## EPIC-04 — QA Coverage & Process Hardening

**Maps to:** S2-04
**Owner:** Director of Quality; QA Lead; QA & Testing Owner; Financial Reporting & Records Owner

### ST-17 — Arc 5 QA protocol
**Source:** BLG-QA-26
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- Arc-level E2E test protocol document produced and filed at `docs/qa/arc5_qa_protocol.md`, covering the full Arc 5 flow: validation gate → override event → red flag journal → drift detection review → strategy version comparison → weekly digest
- Core happy path covered by Playwright
- QA Lead and Product Owner sign-off

### ST-18 — Visual regression baseline snapshots (contrast-sensitive + chart-heavy components)
**Source:** BLG-QA-81
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- Baselines captured for at least the components touched by `BLG-FE-87/88/89`
- Baselines captured for at least one chart-heavy component end-to-end as proof of pattern

### ST-19 — R-multiple calculation regression test
**Source:** BLG-QA-89
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- Automated test asserting R-multiple output against a small set of known trade fixtures, locking the v6.8 R-multiple FX spec's behaviour

### ST-20 — Playwright coverage gap audit for Arc5ComplianceSection
**Source:** BLG-QA-144
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Audit of current Playwright coverage of `Arc5ComplianceSection` complete
- Gaps found filed as backlog items
- QA Lead sign-off

### ST-21 — Standalone axe-core accessibility CI scan
**Source:** BLG-QA-83
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- axe-core scan running in CI for at least 3 pages
- Results visible in CI output

### ST-22 — Publish backend test coverage report to PR comments
**Source:** BLG-QA-84
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- CI step posts a coverage summary (and delta vs. base branch, if feasible) as a PR comment
- Coverage summary posted automatically on the next PR after this ships

---

## EPIC-05 — Backend Architecture & Cost/Capacity Hygiene

**Maps to:** S2-05
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; FinOps & Resource Architect

### ST-23 — Backend service-layer boundary review
**Source:** BLG-BE-56
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Recent backend changes reviewed for layering-boundary drift (e.g. business logic leaking into routers)
- Any drift found corrected

### ST-24 — Database connection pool tuning review
**Source:** BLG-BE-54
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Current concurrent connection usage measured and compared against the configured pool size
- Pool size adjusted if warranted

### ST-25 — Render hosting tier review
**Source:** BLG-OPS-101
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Current Render service tier cost/limits compared against actual measured usage since v6.8
- Tier confirmed as still fitting, or right-sized

### ST-26 — Render hosting cost trend dashboard
**Source:** BLG-OPS-95
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Monthly cost-vs-request-volume trend chart built, sourced from existing monthly review data
- At least 3 months of historical data points shown

### ST-27 — Quarterly dependency minor-version upgrade cadence policy
**Source:** BLG-OPS-98
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Quarterly minor-version upgrade window policy documented
- First pass applying safe minor bumps across `requirements.txt`/`package.json` completed
