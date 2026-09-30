Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-30
Cycle: 2026-09-30__release-v9.9
Release: v9.9

# Backlog Slice — v9.9

<!-- release-plan-marker: RP:v9.9:2026-09-30__release-v9.9 -->

35 stories across 6 grouped EPICs, 27.85 estimated days. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope set to the top of the confirmed ~24-28 day/sprint capacity band per explicit user "full capacity" instruction (2026-09-30). Ready pool: 53 items / 36.20 days (after excluding 2 substantively gate-blocked items with no formal Gate field — `BLG-FEAT-73`/`76`). Selection method: 0 ready P1 items; all 4 ready P2 items seated first per §1.4c, then category-balanced round-robin oldest-first for remaining P3/P4 — per `release_planning_prompt.md` §1.4c. EPIC-01 leads the table (`BLG-BE-135`, this cycle's PO Modify-recommended build-and-ship candidate and largest single item). EPIC-06's single item (`BLG-FE-192`) carries an observable UI acceptance criterion — `design_gate_required: true`.

---

## EPIC-01 — Backend Reliability & Data Integrity

**Maps to:** S2-01, S2-02, S2-03, S2-04, S2-05
**Owner:** Head of Engineering; Backend Engineering Patterns Owner

### ST-01 — Consolidate 4 duplicate ATR implementations; persist stop/ATR recalculation timestamp; expose atr/multiplier/timestamp on GET /positions
**Source:** BLG-BE-135
**Priority:** P2
**Effort:** L (~6-10d)
**Acceptance Criteria:**
- ATR implementation count reduced from 4 (5 including dead code) to 1 canonical source across `backend/utils/pricing.py`, `strategy_engine.py`, `screener_engine.py`, `database.py`; `position_manager.py`'s dead copy removed or explicitly documented as an exempt standalone tool
- `stop_calculated_at`/`atr_calculated_at` persisted alongside `current_stop`/`atr` in both the on-load recompute path and the nightly job
- `atr`, active multiplier, and the timestamp exposed on `GET /positions` and documented in `position_endpoints.md` + `openapi.yaml` (same commit)
- Spec query raised and resolved with the Strategy Rules & System Intent Owner (RISK-01); `strategy_rules.md` §7.1 and `position_endpoints.md` updated to reflect the actual recompute cadence (or engineering constrained to match the documented cadence, per the Owner's ruling)

### ST-02 — GET /reports/monthly-pnl's year param has no bounds check, unlike its sibling GET /reports/tax-year
**Source:** BLG-BE-131
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `GET /reports/monthly-pnl?year=0` (and other out-of-range values) returns a clean `400` with a validation message, not a `404` with a raw Python error string
- Regression test added confirming the bounds check, mirroring the existing `GET /reports/tax-year` bounds-check test pattern

### ST-03 — gemini_service.py's daily-cost Telegram alert still uses a hardcoded timeout, not utils.upstream_call
**Source:** BLG-BE-132
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `gemini_service.py`'s Telegram alert timeout is sourced from `get_timeout("telegram")`; no behaviour change to the existing alert logic

### ST-04 — utils/pricing.py's ATR-fallback Yahoo Finance call still uses a hardcoded timeout, not utils.upstream_call
**Source:** BLG-BE-133
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- The ATR-fallback Yahoo Finance call's timeout is sourced from `get_timeout("yfinance")`; no behaviour change to the existing fallback logic

### ST-05 — alpaca_paper_sync_service.py's 3 Alpaca calls still use hardcoded timeouts, not utils.upstream_call
**Source:** BLG-BE-134
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- All 3 Alpaca call sites in `alpaca_paper_sync_service.py` source their timeout from `get_timeout("alpaca")`; no behaviour change to existing sync/retry logic

---

## EPIC-02 — Operational Reliability & Security Hardening

**Maps to:** S2-06, S2-07, S2-08, S2-09
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead

### ST-06 — Two residual gaps in the just-hardened non-registry dependency guard
**Source:** BLG-SEC-40
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `-e .` and `-e ..` (no trailing slash) are rejected by a test
- A synthetic npm-workspace-local `file:` lockfile entry is confirmed NOT flagged by a test, while a genuine non-workspace `file:`/git resolved URL is still flagged

### ST-07 — POST /ai/check-daily-cost has no de-duplication guard against a double-submitted Telegram alert
**Source:** BLG-OPS-172
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A second call on the same UTC day, after an alert has already been sent for a still-exceeded threshold, does not send a second Telegram message

### ST-08 — POST /ai/check-endpoint-anomalies has no de-duplication guard against a double-submitted Telegram alert
**Source:** BLG-OPS-173
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A second call within the same firing window, with the same anomalies still firing, does not send a second Telegram message

### ST-09 — POST /price-alerts has no de-duplication guard against a double-submitted duplicate alert
**Source:** BLG-OPS-174
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A double-submit of the same `(ticker, condition, threshold_price)` while the first alert is still active does not create a second active alert (or, if guarding is deemed unnecessary, the disposition is recorded as accepted with rationale)

---

## EPIC-03 — QA & Test Coverage

**Maps to:** S2-10, S2-11, S2-12, S2-13, S2-14, S2-15, S2-16, S2-17, S2-18
**Owner:** Director of Quality; QA & Testing Owner

### ST-10 — GET /reports/tax-year returns HTTP 500 against its own test fixture
**Source:** BLG-QA-203
**Priority:** P2
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `backend/.venv/bin/python3 -m pytest tests/test_api_contracts.py::TestReportsEndpoints::test_get_tax_year_report_returns_ok` passes when run alone
- `backend/.venv/bin/python3 -m pytest tests/ -q --ignore=tests/e2e` continues to pass (confirms the fix didn't just move the order-dependency elsewhere)
- Root cause (genuine endpoint defect vs. test-isolation gap) is documented in the fix's commit message or a linked deviation record

### ST-11 — Strategy-rule → test traceability matrix for strategy_rules.md §4–§8
**Source:** BLG-QA-185
**Priority:** P3
**Effort:** M (~2d)
**Acceptance Criteria:**
- Matrix published
- % of clauses with an asserting test reported

### ST-12 — Property-based tests for 'stop never decreases' and sizing validity rules
**Source:** BLG-QA-186
**Priority:** P3
**Effort:** S (~1d)
**Acceptance Criteria:**
- Both properties pass over generated inputs in CI
- A deliberately broken ratchet fails the property

### ST-13 — Real-Postgres integration test for the reflection-reminder evaluation step
**Source:** BLG-QA-189
**Priority:** P3
**Effort:** S (~0.5-1d)
**Acceptance Criteria:**
- The test runs in Phase B CI and fails if the partial-index conflict target or an eligibility clause is broken
- Phase A remains fully mocked

### ST-14 — Convert remaining test files sharing test_trade_plan_audit_log.py's unrestored sys.modules["database"] swap pattern
**Source:** BLG-QA-190
**Priority:** P3
**Effort:** M (~1-2d)
**Acceptance Criteria:**
- Re-run `grep -rln 'sys.modules.pop("database", None)' tests/*.py` to confirm the current file list
- Every Category A file converted to the isolated-copy pattern; every Category B file given a restore-based fix; Category C files reviewed and either left as-is with rationale reconfirmed, or fixed if the review finds a live gap
- Full backend test suite passes with no new failures (only the pre-existing `test_schema*.py` live-staging-DB-permission failures remain)
- A manual reordering check confirms no cross-file leakage remains from this pattern anywhere in `tests/`

### ST-15 — Add automated test coverage for the I/O-boundary functions in EPIC-04's staleness/CI-usage scripts
**Source:** BLG-QA-191
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Both scripts' I/O-boundary functions have unit tests using mocked external calls (no live network/`gh` CLI dependency)
- A deliberate regression in the pagination loop is confirmed to fail the new tests

### ST-16 — test_null_fee_trade_audit.py's inspect.getsource() call fails against the database module stub
**Source:** BLG-QA-192
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- The test passes when run both in isolation and as part of the full suite
- No other test in the file is affected

### ST-17 — Prove the non-registry dependency check fails a real PR, and confirm it is a required status check on main
**Source:** BLG-QA-193
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A recorded failing CI run (run URL) for a PR adding a `git+ssh` dependency
- The required-status-check state on `main` is recorded, either way

### ST-18 — Harden the UI-copy boundary lint against obfuscation-grade and cross-node phrase splits
**Source:** BLG-QA-194
**Priority:** P4
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Each bypass is either detected by a regression test or listed in the script docstring as an accepted limit with rationale
- The `@babel/parser` differential still reports no missed phrase hit over `src/`

---

## EPIC-04 — Governance Process & Strategy Boundary

**Maps to:** S2-19, S2-20, S2-21, S2-22, S2-23, S2-24, S2-25, S2-26, S2-27
**Owner:** Head of Specs Team; PMO Lead

### ST-19 — Conduct the overdue 90-day AI feature usage review (BLG-GOV-74/140/141/142 cluster)
**Source:** BLG-GOV-356
**Priority:** P2
**Effort:** M (~1-2d)
**Acceptance Criteria:**
- A dated review artefact exists assessing AI feature adoption rate, cost per use, and continued-investment justification
- All 8 downstream gated items listed in the source item have an explicit disposition recorded against this review's finding
- Note: may require Human-Delegation for live production data (RISK-03) — this sandboxed environment has no production credential

### ST-20 — gap_risk_service.py (BLG-FEAT-65) shipped without a recorded §13 review or §13.5 roster row
**Source:** BLG-GOV-358
**Priority:** P2
**Effort:** S (~1-2d)
**Acceptance Criteria:**
- A dated determination is recorded (new `docs/product/decisions/` file, or a `strategy_rules.md` §13.3/§13.5 wording update, as appropriate to the outcome)
- If the determination is CONDITIONAL or finds a genuine gap, binding conditions or a remediation item are filed

### ST-21 — Split roadmap_prompt.md into a core plus an appendix so it fits a single read
**Source:** BLG-GOV-343
**Priority:** P3
**Effort:** M (~1.5-2d)
**Acceptance Criteria:**
- Core ≤25,000 tokens
- No procedural step lost (diff-verified)
- CLAUDE.md §6 checklist complete

### ST-22 — Parameter-change ledger for strategy_rules.md §11 production parameters
**Source:** BLG-GOV-344
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Ledger backfilled from the strategy_rules change log
- §12.3 change control references it

### ST-23 — scan_backlog_gate_conditions.py date-disambiguation gap can produce false negatives
**Source:** BLG-GOV-347
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A `gate_condition` with an early future date and a later past date is correctly flagged as lapsed (or explicitly flagged for manual disambiguation, not silently resolved wrong)
- A test file exists and passes in CI covering the cases described in the source item

### ST-24 — Five near-duplicate "AI adoption window" gate-criteria texts should be one canonical shared reference
**Source:** BLG-GOV-350
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A single canonical statement of the 2026-09-24 AI adoption review gate exists
- All 5 affected items reference it rather than restating it

### ST-25 — Rebalance diagnostic tallies (STEP 2.4/7.1/7.2) are recomputed by hand each cycle
**Source:** BLG-GOV-352
**Priority:** P3
**Effort:** M (~2d)
**Acceptance Criteria:**
- The script reproduces the cited cycle's STEP 2.4/7.1 figures exactly, given the same input files
- `roadmap_prompt.md` references the script as an optional acceleration, not a hard dependency

### ST-26 — role_share_history.md has no governance-authorized home under claude/roadmap/
**Source:** BLG-GOV-353
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `claude/roadmap/role_share_history.md` exists, seeded with the 3-cycle backfill already computed
- `roadmap_prompt.md` §7.2 reads from it instead of re-deriving the tally by hand
- Note: requires a routing/authority decision before implementation (RISK-02)

### ST-27 — .claude_current_state.json's execution_state_path points to the prior cycle, not the active one
**Source:** BLG-GOV-354
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `execution_state_path` matches `active_cycle`'s own `execution_state.json`
- Root cause of the missed update at cycle transition is identified and, if a real reader depends on it, fixed so it can't drift again

---

## EPIC-05 — Spec & Data-Model Debt Clearance

**Maps to:** S2-28, S2-29, S2-30, S2-31, S2-32, S2-33, S2-34
**Owner:** Data Model & Domain Schema Owner; Head of Specs Team

### ST-28 — Read-only live-schema vs data_model.md drift detector
**Source:** BLG-SPEC-157
**Priority:** P3
**Effort:** M (~2d)
**Acceptance Criteria:**
- The five known divergences (per the source item) are reproduced by the tool
- Output lists undocumented and missing objects

### ST-29 — Drop 4 confirmed-orphaned, always-NULL columns from the live positions table
**Source:** BLG-SPEC-164
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- All 4 columns (`atr_value`, `stop_price`, `fees`, `pnl_percent`) no longer exist on the live `positions` table
- `data_model.md` reflects the drop in its Migration History

### ST-30 — Reconcile positions.fees_paid NOT NULL constraint (re-apply live, or confirm nullable is intentional)
**Source:** BLG-SPEC-165
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Disposition recorded (constraint re-applied, or nullable confirmed intentional with a stated reason)
- `data_model.md` and the live schema agree, with the reasoning documented

### ST-31 — Cross-reference current_roadmap.md's SI-02 field to the canonical "linked trade plan" definition
**Source:** BLG-SPEC-166
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `current_roadmap.md`'s SI-02 field cross-references the canonical "linked trade plan" definition
- ST-23's (v9.7) originally-scoped acceptance criteria are fully met

### ST-32 — data_model.md DS-19 "Verification status" still says the migration was never run against a live PostgreSQL
**Source:** BLG-SPEC-167
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- DS-19 no longer claims the migration has never run against a live database, and states what was confirmed, where (staging) and when
- `data_model.md` header/footer versions stay in sync

### ST-33 — Correct the BLG-BE-128 citation to BLG-BE-129 for the latency_ms composition decision
**Source:** BLG-SPEC-168
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- No reference to `BLG-BE-128` remains where `BLG-BE-129` is meant, in `ai_endpoints.md` or the dependency register
- `BLG-BE-128`'s own legitimate references are untouched

### ST-34 — Correct notifications.md and the alert-thresholds empty-state scenario doc to the no-trailing-period headings now shipped
**Source:** BLG-SPEC-169
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `notifications.md` and `alert_thresholds_empty_state_scenarios.md` state "No alert rules configured" and "No alert history yet" without a trailing period, matching shipped code and `design_system.md` §Data States
- DEV-v9.7-ST05-01 is marked resolved with this item's ID

---

## EPIC-06 — Frontend & UX Debt

**Maps to:** S2-35
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner

### ST-35 — RecentTradesWidget icon-background badge uses two-way (>=0) colour logic for zero P&L
**Source:** BLG-FE-192
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A trade with `pnl === 0` renders the icon badge in a neutral (non-green, non-rose) colour, consistent with the adjacent P&L text's own zero-P&L treatment
- Winning (`pnl > 0`) and losing (`pnl < 0`) trades retain their existing emerald/rose badge colours
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)
