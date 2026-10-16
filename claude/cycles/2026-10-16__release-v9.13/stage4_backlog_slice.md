Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-16
Cycle: 2026-10-16__release-v9.13
Release: v9.13

# Backlog Slice — v9.13

<!-- release-plan-marker: RP:v9.13:2026-10-16__release-v9.13 -->

40 stories across 6 EPICs, 28.00 estimated days. The acceptance criteria below are the source of truth for Sprint Planning and Execution. Scope is sized to the top of the confirmed ~24–28 day capacity band, per the explicit user instruction "use full capacity" (2026-10-16).

**Ready pool:** 124 items, 64.65 days (after the STEP 4 calibration raises, applied to the whole pool before selection).

**Selection method** (`release_planning_prompt.md` §1.4c):
1. The 1 ready P1 item.
2. All 11 seatable P2 items, in ascending ID order (`BLG-TECH-21` deferred by override, as at v9.10–v9.12).
3. A category-balanced, oldest-first round-robin over P3/P4, run until 0.00 days were left.

The three roadmap-committed items (`BLG-FE-226`, `BLG-FE-227`, `BLG-BE-182`; rebalance `2026-10-16__scheduled`, DL-086) seat mechanically in the P1 and P2 passes.

**Where an item's own AC is stale, untestable or depends on an item outside this release, the AC below restates it.** Any change from the source backlog item is marked *(restated)* with the reason.

**§13 clause-citation rule (v2.61):** no AC in this slice requires a §13 review, determination or sign-off. ST-38 and ST-39 edit §13.3/§13.5 text to match already-reviewed behaviour; they do not review it.

---

## EPIC-01 — Exit Flow, Exit Reasons & Red Flag Journal (build-and-ship)

**Maps to:** S2-01 – S2-05
**Owner:** Head of Engineering; Head of UX & Design; Strategy Rules & System Intent Owner; Data Model & Domain Schema Owner
**Description:** Make the Daily Position Monitor's exit confirmation record real exits (P1: it has returned 405 since 2026-01-24), give exit reasons one allowed list mapped to §8, render Trade Reflections badges from that list, record skipped checklists in the Red Flag Journal, and settle whether month-end rebalance exits belong in §8. Carries all three roadmap-committed items (DL-086).
**Estimated days:** 5.50

### ST-01 — Make the Daily Position Monitor's exit confirmation open the real exit flow
**Source:** BLG-FE-226
**Priority:** P1
**Effort:** S (~1-1.5 days)
**Sequencing:** First in EPIC-01 (P1, roadmap-committed, STEP 8.0 fast-track). Before ST-03 (exit-reason module) and before ST-23/ST-24 (EPIC-04), whose checks fail while `PATCH /positions/{id}` is still called.
**UI-facing:** Yes (Monitor exit queue, ExitModal, error message)
**Acceptance Criteria:**
- No code path calls `PATCH /positions/{id}`; `Position.update` is removed from `base44Client.js`
- Confirming a Monitor exit opens ExitModal for each selected position with the reason pre-selected ("Stop Loss Hit" for a stop suggestion, "Risk-Off Signal" for a regime suggestion) and records the exit through `POST /positions/{id}/exit`, with fees, fill price and FX captured as in every other exit
- A failed exit shows an error message and keeps the queue; the modal does not silently clear
- Both Playwright tests pass in CI: a suggested exit completes and the position leaves the open list; a failed request shows the error

### ST-02 — Define the allowed exit reasons and map each to one of §8's three exit conditions
**Source:** BLG-SPEC-186
**Priority:** P3
**Effort:** S (~1 day; calibrated to 1.5d — CHECK constraint plus live backfill on staging and production)
**Delegation note:** The backfill and constraint must run on staging and production. Expected Human-Delegation to the Data Model & Domain Schema Owner with the Infrastructure & Operations Owner (RISK-01).
**Sequencing:** Before ST-03, which takes each reason's §8 category from this story.
**UI-facing:** No (spec, data model and constraint)
**Acceptance Criteria:**
- The allowed `exit_reason` values and the §8 condition each maps to are listed in `data_model.md` and `metrics_definitions.md`; every stored value maps to exactly one §8 condition
- A CHECK constraint rejects unlisted values; legacy spellings are backfilled first, with the pre-check counts and the DS-xx migration's Live Confirmation recorded for staging and production *(restated: the item's Scope made testable; live steps follow the DS-23 pattern)*

### ST-03 — One shared exit-reason module so Trade Reflections badges and labels match stored values
**Source:** BLG-FE-227
**Priority:** P2
**Effort:** S (~0.5-1 day)
**Sequencing:** After ST-02 (takes the §8 category from it) and ST-01 (ExitModal edits).
**UI-facing:** Yes (badge labels and colours)
**Acceptance Criteria:**
- `src/constants/exitReasons.js` holds the 6 stored values with label, colour and §8 category, keeping legacy keys as aliases
- Each of the 6 stored values renders its own label and colour on Trade Reflections cards and in the modal
- No frontend file keeps its own exit-reason map (ExitModal, TradeReflection, TradeReflectionModal, PerformanceAnalytics and TradeHistoryTable import the module)
- Playwright colour tests pass

### ST-04 — Record checklist_skipped events and stop offering journal filters that can never match
**Source:** BLG-BE-182
**Priority:** P2
**Effort:** S (~1-1.5 days)
**Sequencing:** Independent within EPIC-01.
**UI-facing:** Yes (journal filter labels and empty state)
**Acceptance Criteria:**
- Saving a plan with a non-empty, incomplete checklist writes one non-blocking `checklist_skipped` event (ticker, plan id, unchecked item count), visible in the Red Flag Journal (Playwright)
- Filter options for event types with no writer are labelled "not yet recorded" (or hidden), and the empty state says which types are recorded
- A writer-coverage test passes, and fails if a declared event type loses its writer (dated allow-list entries for the two prompt types)

### ST-05 — Strategy determination on month-end rebalance exits, which are live but not in strategy_rules.md
**Source:** BLG-GOV-391
**Priority:** P2
**Effort:** S (~0.5-1 day, determination)
**Delegation note:** The determination is the first sub-step (`delegated_decision`). A §8 amendment writes `claude/strategy/strategy_rules.md` (RISK-02).
**Sequencing:** Independent. Any `strategy_rules.md` edit follows RISK-02's route.
**UI-facing:** Yes (interim "outside §8 — informational" label on the signal)
**Acceptance Criteria:**
- The Strategy Rules & System Intent Owner records a dated determination: rebalance exit enters §8 under §12.3 change control, or the signal is withdrawn
- Until the determination is applied, the rebalance-exit signal is labelled "outside §8 — informational" in the UI (Playwright)
- If §8 is amended, the edit is made under RISK-02's authorised route with a Change Log row; if withdrawn, `rebalance-exit.yml` and the signal path are retired *(restated: both outcomes made testable)*

---

## EPIC-02 — Stop, Sizing & Position Data Correctness

**Maps to:** S2-06 – S2-14
**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; Metrics Definitions & Analytics Owner
**Description:** Stop a fetched ATR producing a stop at or below zero, align the legacy position manager with §6.3, stop the Settings API silently accepting fixed strategy fields, keep the Monthly P&L report up when the snapshot store fails, define stop freshness, correct a fee-netting claim, and strengthen three sizing and entry tests.
**Estimated days:** 2.75

### ST-06 — Reject a fetched ATR that puts the initial stop at or below zero
**Source:** BLG-BE-180
**Priority:** P2
**Effort:** S (~0.5 day)
**Delegation note:** The rule decision is the first sub-step (`delegated_decision`).
**Sequencing:** Ruling first. Independent of other stories.
**UI-facing:** Yes (Trade Entry inline message)
**Acceptance Criteria:**
- The Strategy Rules & System Intent Owner rules between rejecting with 400 and applying a floor; if the ruling changes stop behaviour, it is recorded in `strategy_rules.md` §5 under RISK-02's route
- A backend test with a mocked fetched (and fallback) ATR where 5 × ATR ≥ entry does not store a stop ≤ 0
- Playwright: with a mocked preview ATR where 5 × ATR ≥ entry, Trade Entry shows no negative stop and explains why

### ST-07 — Align the standalone position_manager.py with §6.3 (no stop ratchet during grace)
**Source:** BLG-BE-161
**Priority:** P3
**Effort:** XS (<0.5d)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `backend/position_manager.py` no longer trails the stop during the 10-day grace period (with a unit test), or `strategy_rules.md` names it as an exception next to the §7.2 one, with the Owner's sign-off (RISK-02 route)

### ST-08 — Reject or flag the four fixed strategy-parameter fields on Settings writes
**Source:** BLG-API-07
**Priority:** P4
**Effort:** S (~0.5 day)
**Sequencing:** Independent. Contract and `openapi.yaml` change in the same commit (RISK-04).
**UI-facing:** No (API response only)
**Acceptance Criteria:**
- The API Contracts & Documentation Owner chooses between a 400 naming the §11 rule and a deprecation warning field
- A `POST /settings` or `PATCH /settings/{settings_id}` write that includes any of `min_hold_days`, `atr_period`, `atr_multiplier_initial` or `atr_multiplier_trailing` is rejected or flagged (backend test)
- `settings_endpoints.md` and `openapi.yaml` describe the behaviour in the same commit

### ST-09 — Keep the Monthly P&L report up when the snapshot store fails
**Source:** BLG-BE-156
**Priority:** P4
**Effort:** S (~0.5d)
**Sequencing:** Independent.
**UI-facing:** Yes ("Restatement check unavailable." becomes reachable)
**Acceptance Criteria:**
- With the snapshot read mocked to fail, `GET /reports/monthly-pnl` returns 200 with realised P&L for every month and no `restated` field, and the failure is logged with `exc_info` (unit test)
- Playwright: that response shows the table and "Restatement check unavailable."
- `reports_endpoints.md` notes the behaviour and `reports.md` drops its Known limitation note

### ST-10 — Define a stop-freshness metric and show it on System Status
**Source:** BLG-SPEC-188
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** Independent. If a new endpoint is added, RISK-04's endpoint-count rules apply.
**UI-facing:** Yes (new value on System Status)
**Acceptance Criteria:**
- The median and maximum age of `stop_calculated_at` across open positions are defined in `metrics_definitions.md` with formula and source
- System Status shows the metric, and the displayed value matches a manual check (recorded)

### ST-11 — Correct metrics_definitions.md's claim about NULL positions.fees_paid
**Source:** BLG-SPEC-180
**Priority:** P4
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- The Fee-Netting Basis paragraph no longer cites a NULL `positions.fees_paid` as a reachable cause of a NULL `trade_history` fee leg; it names legacy or manually inserted `trade_history` rows and cross-references DS-23
- No change to the `null_fee_trade_count` contract or computation

### ST-12 — Mock get_settings() so the stored ATR multiplier is asserted exactly
**Source:** BLG-QA-204
**Priority:** P4
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- The test mocks `get_settings()` to the real multiplier values
- The assertion checks `active_atr_multiplier` equals 2.0 (profitable) and 5.0 (losing), not merely `> 0`

### ST-13 — Test the entry required-field set and the non-blocking advisory panel at their boundary
**Source:** BLG-QA-208
**Priority:** P4
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No (tests only)
**Acceptance Criteria:**
- A contract test shows each required entry field, when omitted, is rejected (C4-01)
- A Playwright scenario submits a trade plan while the pre-entry panel shows FAIL/WARN (C4.2.6)
- The traceability matrix rows are updated

### ST-14 — Give the valid-input sizing property a lower bound
**Source:** BLG-QA-210
**Priority:** P4
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `shares` is asserted within one 4dp floor step of `RiskAmount / (StopDistance × FX)`
- A deliberately zeroed or halved `suggested_shares` falsifies the property

---

## EPIC-03 — AI Output Safety, Debrief & Chat

**Maps to:** S2-15 – S2-22
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner
**Description:** Close the gaps left by v9.12's briefing work: UK ticker matching, chat stop-citation attribution, unknown tickers in the briefing summary, an output-language check on the journal summary and the chat cash label. Fix two debrief display defects and instrument the chat answer rating that the AI usage review needs.
**Estimated days:** 3.10

### ST-15 — Treat UK .L and bare tickers as the same instrument in the briefing ticker filter
**Source:** BLG-AI-17
**Priority:** P2
**Effort:** XS (<1h plus tests)
**Sequencing:** First in EPIC-03; before ST-16 (both touch ticker matching in `ai_service.py`).
**UI-facing:** No
**Acceptance Criteria:**
- A fixture action for `VOD` is kept when `VOD.L` is held, and the reverse
- The stop-time check's ticker attribution uses the same normalisation; tests cover the suffixed case

### ST-16 — Attribute chat stop citations to the focused ticker and case-normalise action tickers
**Source:** BLG-AI-18
**Priority:** P3
**Effort:** S (~0.5d)
**Delegation note:** AI Compliance & Governance Officer sign-off is the first sub-step.
**Sequencing:** After ST-15.
**UI-facing:** No (the styling question is answered as a decision; any styling change is filed separately)
**Acceptance Criteria:**
- The AI Compliance & Governance Officer signs off passing `context_opts.ticker` as `own_ticker` for chat (extending the `ESC-EXEC-20261013-01` ruling)
- A ticker-focused chat reply citing a stop without the ticker gets the recalculation-time note
- An action with a lower-case held ticker gets the note; tests cover both
- The Head of UX & Design's answer on visible "system-added" styling is recorded *(restated: the Scope's question given a recorded outcome)*

### ST-17 — Check the briefing summary text for tickers outside the context
**Source:** BLG-AI-16
**Priority:** P3
**Effort:** S (~0.5d)
**Delegation note:** AI Compliance & Governance Officer sign-off is the first sub-step.
**Sequencing:** After ST-15 (same normalisation).
**UI-facing:** No
**Acceptance Criteria:**
- The AI Compliance & Governance Officer signs off the action (log and count, a code-written caveat, or regenerate)
- A fixture summary naming an unknown ticker is caught and the chosen action is applied and tested
- A summary naming only context tickers passes unchanged
- The result is recorded alongside the stop-time result in `claude_audit_log.compliance_check_result`

### ST-18 — Add an output-language check to the journal summary
**Source:** BLG-AI-15
**Priority:** P3
**Effort:** S (~0.5d)
**Delegation note:** AI Compliance & Governance Officer sign-off is the first sub-step.
**Sequencing:** Independent within EPIC-03.
**UI-facing:** No
**Acceptance Criteria:**
- The AI Compliance & Governance Officer signs off the failure action (regenerate once then a code-written fallback, or return the text with the result logged)
- A fixture summary containing "stop placements need adjustment", and a plainly prescriptive one, are caught and the chosen action is applied and tested
- A descriptive fixture summary passes unchanged
- Each call's check result is recorded in `claude_audit_log.compliance_check_result`; `ai_endpoints.md` and `ai_s13_boundary_test_suite.md` are updated, and `JOURNAL_SUMMARY_PROMPT_VERSION` is bumped if the prompt text changes

### ST-19 — Label available cash and starting capital separately in the AI chat context
**Source:** BLG-AI-14
**Priority:** P4
**Effort:** XS (<1h plus tests)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- The chat context no longer uses "of £{initial_cash}", and omits starting capital when it is 0
- Golden-fixture and chat tests pass with any recorded prompt-version bump; `ai_endpoints.md` §POST /ai/chat context list updated

### ST-20 — Keep the debrief card populated when Regenerate returns no data
**Source:** BLG-FE-211
**Priority:** P3
**Effort:** XS (<1h plus test)
**Sequencing:** Before ST-21 (same file).
**UI-facing:** Yes (debrief card state)
**Acceptance Criteria:**
- Playwright: a mocked 200 with no `data` leaves the previous debrief (or the empty state) visible
- SC-DBF-06a/07a/08a still pass

### ST-21 — Give the debrief error text a light-theme colour that passes contrast
**Source:** BLG-FE-212
**Priority:** P3
**Effort:** XS (<1h plus test)
**Sequencing:** After ST-20.
**UI-facing:** Yes (colour)
**Acceptance Criteria:**
- Playwright: the axe scan of the debrief section in its error state reports no colour-contrast violations in either theme

### ST-22 — Add a useful / not-useful rating to each AI chat answer
**Source:** BLG-FE-208
**Priority:** P3
**Effort:** S (~0.5d plus a live migration; calibrated to 1.0d)
**Delegation note:** The migration must run on staging and production (RISK-01).
**Sequencing:** Independent. A new route follows RISK-04's endpoint rules (contract, `openapi.yaml`, `routers/test.py`, `SystemStatus.js` fallback count, `SC-SS-01b`).
**UI-facing:** Yes (rating control on each chat answer)
**Acceptance Criteria:**
- A user can rate each chat answer once, and the rating persists (Playwright + unit test)
- The rating is stored against the answer it rates, with a `data_model.md` DS entry and its Live Confirmation on staging and production
- The Response Acceptance Rate query in `metrics_definitions.md` § AI Chat Engagement returns a value from stored ratings, and `null` when none exist; its "not instrumented" status is removed

---

## EPIC-04 — API Call Integrity & UI Rendering

**Maps to:** S2-23 – S2-27
**Owner:** Director of Quality; API Contracts & Documentation Owner; Head of Engineering
**Description:** Make CI catch a frontend call to a route that does not exist, both statically (against `openapi.yaml`) and in Playwright (any 404/405), sweep state-changing actions for coverage, fix coloured buttons that never render their colour, fix the Replay page's light-theme contrast and settle a test-isolation question.
**Estimated days:** 6.25

### ST-23 — CI check that every frontend API call exists in openapi.yaml
**Source:** BLG-QA-228
**Priority:** P2
**Effort:** S (~1 day)
**Sequencing:** After ST-01 (EPIC-01), which removes the `PATCH /positions/{id}` call.
**UI-facing:** No (CI tooling)
**Acceptance Criteria:**
- A script extracts every `doFetch`/`apiFetch` method and path in `src/`, compares them with `docs/reference/openapi.yaml` (allow-list for external calls) and runs in the quality gate
- The check fails on a call to a non-existent route (test)
- It passes on `main` once ST-01 lands. Dead Base44 methods that the unseated `BLG-FE-230` will remove (for example `POST /signals`) sit on a dated allow-list naming `BLG-FE-230` *(restated: the source AC waits on `BLG-FE-230`, which is not in this release)*

### ST-24 — Fail Playwright on any 404/405 from the app's API and sweep state-changing actions
**Source:** BLG-QA-227
**Priority:** P2
**Effort:** M (~2-3 days; calibrated to 3.5d — sweep of 59 state-changing calls in 22 `src/` files, grep-confirmed 2026-10-16)
**Sequencing:** After ST-01 (EPIC-01) and ST-23.
**UI-facing:** No (test infrastructure)
**Acceptance Criteria:**
- A shared Playwright fixture fails a test on any 404/405 from the app's own API origin (allow-list for intentional probes); it is applied suite-wide and fails on a deliberate 405
- The list of state-changing primary actions is recorded in `docs/testing/` with coverage status; every listed action is covered or has a dated backlog item
- Defects the fixture exposes are filed as backlog items, not fixed inside this story *(restated: bounds the sweep, RISK-05)*

### ST-25 — Make coloured Buttons render their colour (fix cn() at the root)
**Source:** BLG-FE-221
**Priority:** P2
**Effort:** S (~0.5 day)
**Sequencing:** Independent.
**UI-facing:** Yes (button colours)
**Acceptance Criteria:**
- `cn()` gains `tailwind-merge` (or coloured buttons get a variant with no background); ST-24 (v9.12)'s `!bg-` workaround is removed
- Every `<Button>` with a colour `bg-*` className renders that colour, asserted with `toHaveCSS('background-color', …)` or a scoped axe check for the listed sites (Screener ~333/~1065, TradePlans ~385, Trade Plan "Abandon Plan")

### ST-26 — Fix the Replay page's light-theme colour contrast
**Source:** BLG-FE-209
**Priority:** P3
**Effort:** S (~0.5-1 day)
**Sequencing:** Independent. Uses the light-mode tokens v9.12 ST-23 introduced.
**UI-facing:** Yes (colour)
**Acceptance Criteria:**
- The light-theme Replay axe scans (Date Range, Trade Set, populated result) pass
- The three `Replay*:light` `color-contrast` entries are removed from `KNOWN_VIOLATIONS` in the same commit

### ST-27 — Decide how real-database-bound modules may persist across pytest files
**Source:** BLG-QA-211
**Priority:** P4
**Effort:** S (~0.5d)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- Either a documented, reviewed decision in `tests/_real_database.py` (with the conftest guard's docstring stating what it does not cover), or no backend module bound to the real database survives past the importing file

---

## EPIC-05 — Operations, Cost & Platform

**Maps to:** S2-28 – S2-34
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect; Head of Engineering
**Description:** Stop the daily AI cost alert reporting $0 on failure, deploy both staging services from `staging-deploy.yml`, produce the data-pipeline cost baseline and per-feature attribution, benchmark the screener, assess data-provider risk and assess the major dependency upgrades.
**Estimated days:** 8.50

### ST-28 — Make the daily AI cost alert fail loudly on query or workflow failure
**Source:** BLG-OPS-187
**Priority:** P2
**Effort:** S (~0.5d)
**Delegation note:** A real failed-run Telegram receipt may need Human-Delegation to the Infrastructure & Operations Owner (RISK-01).
**Sequencing:** Independent. A response-shape change to `POST /ai/check-daily-cost` updates its contract and `openapi.yaml` in the same commit.
**UI-facing:** No
**Acceptance Criteria:**
- A simulated cost-query failure is logged, reported as an error status and fails the workflow step
- A failed `ai-daily-cost-check.yml` run sends a notification beyond GitHub's default email (Telegram)

### ST-29 — Deploy both staging services from staging-deploy.yml and wait on each
**Source:** BLG-OPS-189
**Priority:** P2
**Effort:** S (~0.5d; calibrated to 1.0d — two Render dashboard hooks, GitHub secrets and a live staging run)
**Delegation note:** Copying the deploy hooks from the Render dashboard and setting the secrets needs Human-Delegation to the Infrastructure & Operations Owner (RISK-01).
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `RENDER_STAGING_BACKEND_DEPLOY_HOOK` and `RENDER_STAGING_FRONTEND_DEPLOY_HOOK` replace `RENDER_STAGING_DEPLOY_HOOK`; the workflow calls both and checks each returned deploy ID belongs to the expected service
- A `staging-deploy.yml` run on `main` succeeds, with both staging services live on the run's commit
- A test fails if the workflow calls only one hook or waits on a service it did not deploy
- The smoke test confirms the host behind `STAGING_API_URL` is `srv-d6rtdg94tr6s73ce2j6g`; `staging_deploy_notes.md` §4 and `github_actions_secrets_ownership_map.md` updated

### ST-30 — Produce the combined data-pipeline cost baseline
**Source:** BLG-OPS-18
**Priority:** P3
**Effort:** S (~1 day)
**Delegation note:** Usage figures come from live instrumentation; read access may need Human-Delegation (RISK-01).
**Sequencing:** Before ST-31.
**UI-facing:** No
**Acceptance Criteria:**
- A combined weekly cost baseline across Alpaca, Yahoo Finance and the news API is filed in `docs/ops/`
- The alert threshold (>2× baseline → advisory) is defined
- Gate condition met: `BLG-OPS-17` shipped in v9.3 (verified at Release Planning 2026-10-16, `run_manifest.md`) *(restated: the gate check moved from sprint planning to Release Planning)*

### ST-31 — Attribute each external API call to the feature that triggered it
**Source:** BLG-OPS-19
**Priority:** P3
**Effort:** M (~2 days)
**Sequencing:** After ST-30.
**UI-facing:** No
**Acceptance Criteria:**
- Each outbound external API call is tagged with its triggering endpoint or feature (tests)
- An attribution report (cost by feature) is computable and names the top 3 contributors
- Gate condition met: `BLG-OPS-17` shipped in v9.3 (verified at Release Planning 2026-10-16) *(restated)*

### ST-32 — Benchmark the full screener run
**Source:** BLG-OPS-23
**Priority:** P3
**Effort:** S (~1 day)
**Delegation note:** Runs against a deployed environment's full ticker universe (500+ tickers); may need Human-Delegation (RISK-01).
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- The full-universe screener run's p50/p95 duration is measured and filed in `docs/ops/api_performance_baseline.md`
- The regression threshold (>1.5× baseline duration) is defined
- Gate condition met: `BLG-OPS-13` shipped in v8.8 (verified at Release Planning 2026-10-16) *(restated)*

### ST-33 — Assess data-provider risk and failover options
**Source:** BLG-OPS-77
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `data_provider_risk_assessment.md` covers every active external data provider, with failure modes and impact per provider
- Quick-win failover paths and re-evaluation conditions are documented
- The accepted-risk statement is signed off by the Infrastructure & Operations Owner and the FinOps & Resource Architect

### ST-34 — Assess the major and breaking dependency upgrades from the October 2026 review
**Source:** BLG-TECH-23
**Priority:** P3
**Effort:** M (~2-3 days across items; assess first, then split)
**Sequencing:** Independent. Assessment only: approved upgrades are filed as separate backlog items, not done here.
**UI-facing:** No
**Acceptance Criteria:**
- A dated assessment covers all 8 packages (anthropic, SQLAlchemy, reportlab, uvicorn, framer-motion, lucide-react, eslint, moment), each with breaking changes, effort and an upgrade-or-hold decision
- Each approved upgrade has its own backlog item; tailwindcss 4 stays with `BLG-TECH-21`

---

## EPIC-06 — Governance & Spec Tooling

**Maps to:** S2-35 – S2-40
**Owner:** Head of Specs Team; PMO Lead; Strategy Rules & System Intent Owner; Data Model & Domain Schema Owner
**Description:** Fix the gate scan's handling of `Gate criteria: None` and add its known-false-positive allow-list, bring `strategy_rules.md` §13.3/§13.5 text in line with shipped behaviour, correct one role-share figure and teach the data-model drift check to compare defaults.
**Estimated days:** 1.90

### ST-35 — Treat Gate criteria: None/N/A as ungated in the gate scan
**Source:** BLG-GOV-390
**Priority:** P2
**Effort:** XS (<1h, ~0.25d)
**Sequencing:** First in EPIC-06; before ST-36 (same script).
**UI-facing:** No
**Acceptance Criteria:**
- `classify_item()` treats `None`, `N/A`, `-` or `—` (case-insensitive, trimmed, optional trailing period) as ungated and reports them as an informational "explicitly ungated" count
- The 17 named items no longer appear in the gated list and the gated count drops by 17 (124 → 107 on the 2026-10-16 scan); `BLG-GOV-382` is still reported as gated
- New tests pass under `backend/.venv/bin/python3 -m pytest`; the PR records whether each of the 17 still deserves a ready-pool slot

### ST-36 — Known-false-positive allow-list for the gate scan
**Source:** BLG-GOV-373
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** After ST-35 (same script).
**UI-facing:** No
**Acceptance Criteria:**
- An allow-list of item IDs, each with a reason and a review date, is reported separately as "known non-gate dates"
- Items whose embedded date is a counting start or provenance date (for example `BLG-OPS-53`'s ship-date mention) do not appear in the date-lapsed list *(restated: the 2026-10-16 scan's date-lapsed list is empty, so the AC is tested with a fixture)*

### ST-37 — Compare documented column defaults in check_data_model_drift.py
**Source:** BLG-SPEC-184
**Priority:** P4
**Effort:** S (~0.5d)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- A doc showing `DEFAULT 0` against a live `column_default = NULL` is reported as a default mismatch, and vice versa
- Equivalent forms (`0` vs `0::numeric`, `'[]'::jsonb` vs `'[]'`) do not produce false positives
- The tool stays read-only (`SELECT` on `information_schema` only) and the existing drift/orphan/dashboard tests still pass

### ST-38 — Update strategy_rules.md §13.3 now the Gap Risk Flag's weekend-hold trigger is gone
**Source:** BLG-GOV-376
**Priority:** P3
**Effort:** XS (~0.25 day)
**Delegation note:** Writes `claude/strategy/strategy_rules.md`, which Sprint Execution may not write without the RISK-02 authorisation.
**Sequencing:** Before ST-39; one version bump may cover both. Written under RISK-02's route.
**UI-facing:** No
**Acceptance Criteria:**
- §13.3's third paragraph is replaced with the "Proposed §13.3 third paragraph" text from the v9.10 addendum of `decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`
- The §13.5 roster row records Binding Condition 6 as met (v9.10)
- Version bump, Change Log row (documentation only) and §15 grep recorded

### ST-39 — Correct strategy_rules.md §13.5's PO-05 roster row
**Source:** BLG-GOV-377
**Priority:** P3
**Effort:** XS (~0.25 day)
**Delegation note:** Writes `claude/strategy/strategy_rules.md` (RISK-02).
**Sequencing:** After ST-38 (may share its commit and version bump).
**UI-facing:** No
**Acceptance Criteria:**
- §13.5's PO-05 row no longer says PO-05 reuses IT-06; it reads as set out in the item's Scope
- Change Log row (documentation only) and §15 grep recorded

### ST-40 — Correct the v9.8–v9.10 compound Owner count in role_share_history.md
**Source:** BLG-GOV-387
**Priority:** P3
**Effort:** XS (<1h)
**Delegation note:** Named-file write to `claude/roadmap/role_share_history.md`, classified `delegated_decision` under the named-file rule (`ESC-CLOSE-20261006-01`).
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- The v9.8–v9.10 rolling line's compound count matches `scripts/compute_role_share_history.py`'s output for v9.10 (17 of 21)
