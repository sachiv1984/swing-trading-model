Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-09

---

## Consolidation Block

**EPIC:** EPIC-02 — QA & Test Infrastructure Debt
**Cycle:** 2026-09-09__release-v9.3
**Sprint goal:** Clear a full-capacity, cross-category slate of 27 debt items — backend reliability/correctness, QA/test infrastructure, operations/cost monitoring, spec/documentation, and governance-process/security — exhausting the confirmed ~24–28 day capacity band at 27.50 days, with zero P1/P2 debt items deferred on capacity grounds this cycle.
**Test scenarios used:** `tests/e2e/signal-card.spec.js`, `tests/test_pilot_contract_schemas.py`, `tests/e2e/watchlist.spec.js` (pre-existing baseline)

*(This file is being built up incrementally as EPIC-02's stories complete — per execution_prompt.md §3.1.C. ST-08 is `delegated_qa` and awaiting human staging input; ST-09/ST-10 not yet started. EPIC-level consolidation/sign-off block will be completed once all 6 stories reach a terminal state.)*

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-05 | `tests/e2e/signal-card.spec.js` | Consolidated 3 overlapping SignalCard Playwright specs (`signals-add-to-watchlist.spec.js`, `signals-cash-balance.spec.js`, `signals-allocation-insufficient.spec.js`) into 1 file, namespaced helpers to avoid collision | 3 files audited/consolidated into 1; full scenario coverage retained; suite runtime reduced | Pass | None |
| ST-06 | `tests/test_pilot_contract_schemas.py`; `docs/reference/openapi.yaml#components/schemas/{CashSummary,Signal}` | Extended the ST-11/v7.8 contract-test pilot from 3 to 5 endpoints (added GET /cash/summary, GET /signals sourced from openapi.yaml); fixed 2 field-level drifts found (Signal.momentum_score→momentum_percent rename, CashSummary.current_cash added) | Contract tests pass for ≥5 endpoints against documented openapi.yaml schema; documented extension pattern exists; drift beyond the sample filed not resolved inline | Pass | None (drift within the 5-endpoint sample fixed inline per RISK-02, not filed; none found beyond the sample) |
| ST-07 | `docs/testing/doq_signoff_template_freshness_review_20260909.md` | Reviewed qa_evidence_template.md and the record-visual-qa skill against sampled actual staging sign-off practice across full cycle history | Template/skill confirmed to reflect current practice; drift documented and filed as follow-on if actionable | Pass | None (finding filed as BLG-GOV-319 per AC's own "if actionable" clause — this is documentation of a process gap, not a spec deviation) |
| ST-08 | `docs/specs/frontend/pages/watchlist.md` | No code change — this item IS the staging verification task itself (v6.8 ESLint refactor, BLG-OPS-61, confirming no rendered-behaviour regression) | Visual QA pass performed on Watchlist page confirming no regression; findings recorded (pass, or FAIL with follow-on) | **Pending — awaiting human staging input** | N/A pending |

**Supporting evidence for ST-08 (gathered by the engine ahead of the human pass, not a substitute for it):** the pre-existing baseline suite `tests/e2e/watchlist.spec.js` (6 scenarios: SC-WL-01 through SC-WL-06 — entry rendering, news toggle expand/collapse, non-US no-toggle, Add Ticker modal, validation error text/colour, WatchlistModal DialogDescription colour cascade) was re-run locally against current `main` and passes 6/6. This is real automated evidence that current rendering is correct against today's documented expectations, but per `sprint_backlog.md`'s explicit `delegated_qa` classification for this story ("the deliverable is the human/staging visual verification itself"), it does not substitute for the human confirmation this story specifically asks for — the sprint plan already decided this needs a human pass, not a Playwright substitution, and the engine is not overriding that classification unilaterally.

**QA test coverage:**
- Scenarios run: `tests/e2e/signal-card.spec.js` (12/12 pass, local run), `tests/test_pilot_contract_schemas.py` + `tests/test_api_contracts.py` (64/64 pass, local `backend/.venv` run), `scripts/openapi_3way_drift_sweep.py` (clean, 140/140 aligned), `tests/e2e/watchlist.spec.js` (6/6 pass, local run — pre-existing baseline, supporting evidence for ST-08 only)
- Regression areas checked: SignalCard rendering (watchlist CTA, cash balance, allocation-insufficient badge — all still pass post-consolidation), openapi.yaml path/heading registration (no drift introduced), Watchlist.js baseline rendering (unaffected by this cycle's changes)
- Known deviations: None found — ST-05/ST-06/ST-07 deviation checks completed with nothing to file

---

## Director of Quality Request — ST-08 (open)

**Requested of:** Director of Quality / Head of UX & Design (per `sprint_backlog.md`'s Owner field for ST-08)

**What's needed:** A human staging visual QA pass on the Watchlist page (`/#/Watchlist`), confirming the v6.8 ESLint refactor (`BLG-OPS-61`) introduced no rendered-behaviour regression. Since no pre-authored check-ID script exists for this specific story, a free-form confirmation is fine (matching current practice per the ST-07 finding above) — e.g. "Watchlist page renders correctly, entries/badges/news-toggle/Add-Ticker modal all behave as expected, no visual regressions found" (or details of anything that looks off). Report results and this will be recorded via the `record-visual-qa` skill (or directly in this file's sign-off block if free-form, per current practice).

**Not yet resolved — EPIC-02 cannot seal until this is answered** (ST-08 blocks the EPIC-level DoQ sign-off; ST-09/ST-10 remain independently outstanding).
