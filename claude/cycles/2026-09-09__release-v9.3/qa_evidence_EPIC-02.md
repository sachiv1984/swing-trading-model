Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-10

---

## Consolidation Block

**EPIC:** EPIC-02 — QA & Test Infrastructure Debt
**Cycle:** 2026-09-09__release-v9.3
**Sprint goal:** Clear a full-capacity, cross-category slate of 27 debt items — backend reliability/correctness, QA/test infrastructure, operations/cost monitoring, spec/documentation, and governance-process/security — exhausting the confirmed ~24–28 day capacity band at 27.50 days, with zero P1/P2 debt items deferred on capacity grounds this cycle.
**Test scenarios used:** `tests/e2e/signal-card.spec.js`, `tests/test_pilot_contract_schemas.py`, `tests/e2e/watchlist.spec.js` (pre-existing baseline)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-05 | `tests/e2e/signal-card.spec.js` | Consolidated 3 overlapping SignalCard Playwright specs (`signals-add-to-watchlist.spec.js`, `signals-cash-balance.spec.js`, `signals-allocation-insufficient.spec.js`) into 1 file, namespaced helpers to avoid collision | 3 files audited/consolidated into 1; full scenario coverage retained; suite runtime reduced | Pass | None |
| ST-06 | `tests/test_pilot_contract_schemas.py`; `docs/reference/openapi.yaml#components/schemas/{CashSummary,Signal}` | Extended the ST-11/v7.8 contract-test pilot from 3 to 5 endpoints (added GET /cash/summary, GET /signals sourced from openapi.yaml); fixed 2 field-level drifts found (Signal.momentum_score→momentum_percent rename, CashSummary.current_cash added) | Contract tests pass for ≥5 endpoints against documented openapi.yaml schema; documented extension pattern exists; drift beyond the sample filed not resolved inline | Pass | None (drift within the 5-endpoint sample fixed inline per RISK-02, not filed; none found beyond the sample) |
| ST-07 | `docs/testing/doq_signoff_template_freshness_review_20260909.md` | Reviewed qa_evidence_template.md and the record-visual-qa skill against sampled actual staging sign-off practice across full cycle history | Template/skill confirmed to reflect current practice; drift documented and filed as follow-on if actionable | Pass | None (finding filed as BLG-GOV-319 per AC's own "if actionable" clause — this is documentation of a process gap, not a spec deviation) |
| ST-08 | `docs/specs/frontend/pages/watchlist.md` | No code change — this item IS the staging verification task itself (v6.8 ESLint refactor, BLG-OPS-61, confirming no rendered-behaviour regression) | Visual QA pass performed on Watchlist page confirming no regression; findings recorded (pass, or FAIL with follow-on) | **Pass — staging-confirmed 2026-09-10** | None |
| ST-09 | `docs/qa/cross_browser_playwright_matrix_evaluation_20260909.md` | Cost/benefit evaluation of adding Firefox/WebKit to the CI matrix — real local run of 2 critical-path specs (36 tests) against Chromium/Firefox/WebKit | Cost/benefit evaluated for a small critical-path set; recommendation (adopt/defer) documented | Pass | None |
| ST-10 | `docs/ops/backend_test_suite_runtime_baseline.md` | Backend pytest suite runtime baseline recorded (1385 passed, 10 skipped, 60.57s) with a `--durations=15` breakdown | Current baseline runtime documented for future regression comparison | Pass | None |

**Staging confirmation — ST-08 (2026-09-10):** Human staging visual QA performed directly by the session user (sachiv.patel@hotmail.co.uk), who built and ran commit `158df7c7` locally. Reported: "watchlist page looks as expected" — no visual regressions found from the v6.8 ESLint refactor (`BLG-OPS-61`). Free-form confirmation, matching current staging sign-off practice per the ST-07 finding above (no pre-authored check-ID script existed for this story). Combined with the supporting automated evidence already gathered (see below), this closes ST-08 with no follow-on required.

**Supporting evidence for ST-08 (gathered by the engine ahead of the human pass):** the pre-existing baseline suite `tests/e2e/watchlist.spec.js` (6 scenarios: SC-WL-01 through SC-WL-06 — entry rendering, news toggle expand/collapse, non-US no-toggle, Add Ticker modal, validation error text/colour, WatchlistModal DialogDescription colour cascade) was re-run locally against current `main` and passes 6/6.

**QA test coverage:**
- Scenarios run: `tests/e2e/signal-card.spec.js` (12/12 pass, local run), `tests/test_pilot_contract_schemas.py` + `tests/test_api_contracts.py` (64/64 pass, local `backend/.venv` run), `scripts/openapi_3way_drift_sweep.py` (clean, 140/140 aligned), `tests/e2e/watchlist.spec.js` (6/6 pass, local run — pre-existing baseline, supporting evidence for ST-08), `backend/.venv/bin/python3 -m pytest` (1385 passed, 10 skipped — ST-10 baseline run)
- Regression areas checked: SignalCard rendering (watchlist CTA, cash balance, allocation-insufficient badge — all still pass post-consolidation), openapi.yaml path/heading registration (no drift introduced), Watchlist.js rendering (human-confirmed no regression, ST-08)
- Known deviations: None found — all 6 stories' deviation checks completed with nothing to file

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend component created/modified this EPIC (ST-08 is a verification-only story, no code touched)
- Signed off by: Director of Quality
- Date: 2026-09-10
- Comments: **BLG-GOV-19 autonomous class is not available for this EPIC** — ST-08 is classified `delegated_qa`, so Criterion 1 ("all stories `autonomous`") is unmet regardless of the other 5 stories being autonomous. Standard Sign-Off Block used instead, per the Delegated-QA sign-off pattern (BLG-GOV-69/74) Format (i) — Individual sign-off: ST-08's story-level sign-off was the session user's direct staging confirmation recorded above; reviewed and acknowledged in aggregate with the other 5 stories' evidence in the consolidation table. **This document's own DoQ block does not itself satisfy the STEP 4 merge gate's "QA sign-off" or "Product Owner acceptance" conditions** — those remain always-human per `execution_prompt.md` §5.3 and CLAUDE.md §2, and must be given directly on the pull request before merge.
