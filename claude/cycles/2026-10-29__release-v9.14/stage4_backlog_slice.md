Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-29
Cycle: 2026-10-29__release-v9.14
Release: v9.14

# Backlog Slice — v9.14

<!-- release-plan-marker: RP:v9.14:2026-10-29__release-v9.14 -->

54 stories across 7 EPICs, 28.00 estimated days. The acceptance criteria below are the source of truth for Sprint Planning and Execution. Scope is sized to the top of the confirmed ~24–28 day capacity band, per the explicit user instruction "use full capacity" (2026-10-29).

**Ready pool:** 156 items, 81.55 days (after the STEP 4 calibration raises, applied to the whole pool before selection).

**Selection method** (`release_planning_prompt.md` §1.4c):
1. The 1 ready P1 item.
2. All 11 seatable P2 items, in ascending ID order (`BLG-TECH-21` deferred by override, as at v9.10–v9.13).
3. A Product Owner override (2026-10-29) seating v9.13's three deferred lessons-learnt patches (`BLG-QA-238`, `BLG-GOV-397`, `BLG-GOV-398`).
4. A category-balanced, oldest-first round-robin over P3/P4, run until 0.00 days were left.

No items are roadmap-committed (DL-087 names v9.14 without committing items).

**Where an item's own AC is stale, untestable, missing or depends on an item outside this release, the AC below restates it.** Any change from the source backlog item is marked *(restated)* with the reason.

**`strategy_rules.md` writes (case (c), `execution_prompt.md` v3.89 §7):** ST-03, ST-09 and ST-22 name exact `strategy_rules.md` sections. Each write needs a Strategy Rules & System Intent Owner confirmation for that AC line in the sealed `sprint_backlog.md` sign-off summary (RISK-02). The write must ship in one commit with its Change Log row, its `strategy_version_registry.py` entry and the §15 re-run.

**§13 clause-citation rule (v2.61):** ST-15, ST-17, ST-22, ST-23 and ST-52 require a §13 review, determination or sign-off. Each cites every §13 clause that names its subject, or says no clause does.

**Post-merge and production-data ACs (Sprint Planning STEP 6.2):** ST-01 AC 1, ST-23 AC 1, ST-39 AC 2 and ST-43 AC 1 can be met only on `main` after merge or with production data. Sprint Planning marks them `post-merge` with a named tracking item before seal.

---

## EPIC-01 — Production Deploy & Market-Data Resilience (build-and-ship)

**Maps to:** S2-01 – S2-08
**Owner:** Infrastructure & Operations Owner; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; Head of UX & Design
**Description:** Restore the production frontend deploy (P1: GitHub Pages has failed on every `main` push since 2026-10-15). Stop a Yahoo Finance outage from silently defaulting the market regime to risk-on and freezing FX at 1.27. Make System Status detect that outage, and mark stale prices on the Positions page as `/risk` already does.
**Estimated days:** 4.15

### ST-01 — Restore eslint-config-react-app so the frontend builds and deploys again
**Source:** BLG-OPS-193
**Priority:** P1
**Effort:** S (~0.5d; calibrated to 1.0d — production deploy re-run plus Render staging dashboard check)
**Delegation note:** Removing or recording the Render dashboard `DISABLE_ESLINT_PLUGIN` workaround may need the Infrastructure & Operations Owner's Render dashboard access (RISK-01).
**Sequencing:** First in the sprint. Every frontend story's staging or production check depends on a working build.
**UI-facing:** No (build and CI)
**Acceptance Criteria:**
- `deploy.yml` succeeds on `main` and production serves the new build *(post-merge: only a `main` run can meet this; Sprint Planning names the tracking item)*
- The Render staging frontend builds from `main` with no dashboard-only ESLint workaround, or the workaround is in `render.yaml`
- A PR that removes `eslint-config-react-app` from the lockfile fails CI (a CI step runs the production build without `DISABLE_ESLINT_PLUGIN`)

### ST-02 — Compute the SPY market regime from Alpaca bars when Yahoo Finance fails
**Source:** BLG-BE-192
**Priority:** P2
**Effort:** S (~0.5d)
**Sequencing:** Before ST-03 (same function, `check_market_regime()`).
**UI-facing:** No
**Acceptance Criteria:**
- With Yahoo mocked to fail and Alpaca mocked to return bars, the SPY regime is computed from the Alpaca bars, not defaulted to risk-on (test)
- The regime result records which source produced it
- With both failing, behaviour is unchanged until ST-03 applies its ruling (test) *(restated: the item names BLG-BE-193, which is ST-03 in this release)*

### ST-03 — Show an unknown market regime instead of silently defaulting to risk-on
**Source:** BLG-BE-193
**Priority:** P2
**Effort:** S (~0.5d, plus a strategy ruling)
**Sequencing:** After ST-02. Before ST-06 (System Status reads the defaulted-regime signal). The ruling is the first sub-step (`delegated_decision` to the Strategy Rules & System Intent Owner).
**UI-facing:** Yes (regime shown as unknown on the dashboard)
**Acceptance Criteria:**
- A dated Strategy Rules & System Intent Owner ruling is recorded on what "regime unknown" means for entries (§4.2.1) and the risk-off job (§8.2): block entries, keep the last known regime, or risk-on with a warning
- If the ruling changes the behaviour §4.2.1 or §8.2 describes, the matching text in `claude/strategy/strategy_rules.md` §4.2.1 and/or §8.2 is updated under case (c), with a `STRATEGY_VERSION_REGISTRY` entry *(restated: names the exact sections for the standing write rule, `ESC-CLOSE-20261029-02`)*
- With regime data mocked unavailable, the result is marked unknown and the ruled behaviour applies (tests)
- The dashboard shows the regime as unknown in that case (Playwright)

### ST-04 — Use the last good GBP/USD rate, with its age, before the fixed 1.27 fallback
**Source:** BLG-BE-194
**Priority:** P2
**Effort:** S (~0.5d)
**Sequencing:** Before ST-05 and ST-06, which build on the stored rate and the fallback signal.
**UI-facing:** Yes (rate age shown)
**Acceptance Criteria:**
- With Yahoo mocked to fail, the last stored rate is used, not 1.27 (test)
- The constant is used only when no stored rate exists (test)
- The rate's age is shown when it is older than one trading day (Playwright)

### ST-05 — Flag an FX fallback instead of applying it silently
**Source:** BLG-BE-169
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** After ST-04. Reuses ST-04's stored rate, source and age instead of adding a second staleness mechanism.
**UI-facing:** Yes (indicator on the Dashboard and Risk Dashboard)
**Acceptance Criteria:**
- `GET /portfolio` and `GET /positions` expose whether the FX rate is live, last-known-good (with its timestamp) or the constant. Both contracts and `openapi.yaml` are updated in the same commit *(restated: aligned with ST-04's last-good rate, which the item's Scope offers as an alternative)*
- A unit test with the FX fetch mocked to fail sets the flag and never presents 1.27 as a live rate
- Playwright shows the indicator

### ST-06 — Make the System Status Yahoo Finance check detect an outage
**Source:** BLG-OPS-194
**Priority:** P2
**Effort:** XS (~1-2h)
**Sequencing:** After ST-03 and ST-04 (reads their fallback signals).
**UI-facing:** Yes (check status and reason on System Status)
**Acceptance Criteria:**
- With the Yahoo FX fetch mocked to fail, the health check reports Yahoo Finance unhealthy or degraded, not healthy (test)
- With the fetch succeeding, it reports healthy with the live rate (test)
- With the regime fetch mocked to fail, the check is not reported healthy (test)
- The reason is shown in the check's details

### ST-07 — Flag stale prices on GET /positions and the Positions page
**Source:** BLG-BE-168
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** Before ST-08 (same marker pattern).
**UI-facing:** Yes (stale marker on Positions table and grid)
**Acceptance Criteria:**
- `GET /positions` returns `price_is_stale`, with the contract and `openapi.yaml` updated in the same commit
- A unit test with the fetch mocked to fail returns `price_is_stale: true`
- Playwright shows the marker on a stale row and none on a live row

### ST-08 — Make the stale-price explanation reachable on touch, keyboard and screen readers
**Source:** BLG-FE-214
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** After ST-07. Applies to the Positions marker as well as `/risk` and Dashboard Card 2.
**UI-facing:** Yes (design-gate review of the wording)
**Acceptance Criteria:**
- axe passes on `/risk` with a stale row
- The explanation is reachable by keyboard focus and exposed as the marker's accessible description (Playwright `toHaveAccessibleDescription`)
- The Positions-page marker from ST-07 uses the same explanation *(restated: ST-07 adds a third marker in this release)*

---

## EPIC-02 — Sizing, Exit & Position Correctness

**Maps to:** S2-09 – S2-14
**Owner:** Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner; Head of UX & Design; Data Model & Domain Schema Owner
**Description:** Fix US position sizing, which risks about 53–62% of the budget because it multiplies by the FX rate instead of dividing. Give exit errors their documented status codes. Stop the Monitor suggesting stop exits during grace. Correct the positions data dictionary.
**Estimated days:** 2.30

### ST-09 — US position sizing divides the stop distance by the GBP/USD rate
**Source:** BLG-BE-190
**Priority:** P2
**Effort:** S (~0.5d)
**Sequencing:** First in EPIC-02. The FX-convention confirmation is the first sub-step.
**UI-facing:** Conditional (only if the Trade Entry risk display carries the same inversion)
**Acceptance Criteria:**
- The Strategy Rules & System Intent Owner confirms the FX convention against `strategy_rules.md` §4.1.2/§4.1.5 (dated)
- For a US position, `suggested_shares × StopDistance / fx` is within one 4dp floor step of `RiskAmount`, with a worked test (£100 risk, $10 stop distance, fx 1.27 → 12.7 shares)
- The property test asserts the corrected relationship and fails against the old formula
- `claude/strategy/strategy_rules.md` §4.1.5's Known Deviations entry for `BLG-BE-190` (added in v1.19) is closed, and §4.1.3 states the US formula if the owner finds it ambiguous. This is written under case (c) with its registry entry *(restated: the item's "RISK-02 route" is replaced by the standing rule, `ESC-CLOSE-20261029-02`)*
- Any other inverted calculation found (Trade Entry risk display, heat impact, `MaxAffordableShares`) is fixed or filed, and `portfolio_endpoints.md` §POST /portfolio/size's example is corrected if it shows the old value

### ST-10 — POST /positions/{id}/exit returns its documented 404 and 400, not 500
**Source:** BLG-BE-188
**Priority:** P2
**Effort:** XS (~0.5 day)
**Sequencing:** Independent within EPIC-02. Before ST-29 (EPIC-05) asserts the Exit modal's error path.
**UI-facing:** No
**Acceptance Criteria:**
- Each `ValueError` from `exit_position` maps to its documented 404 or 400 with a `detail` string
- One pytest per error case asserts the status and `detail`

### ST-11 — Daily Position Monitor stops suggesting "Stop Loss Hit" during the grace period
**Source:** BLG-FE-231
**Priority:** P2
**Effort:** XS (~0.5 day)
**Sequencing:** Independent within EPIC-02.
**UI-facing:** Yes (Monitor suggestions)
**Acceptance Criteria:**
- The Monitor's suggestions use `getExitCondition()` (`src/lib/exitCondition.js`)
- An in-grace breached position is not suggested (Playwright)
- Post-grace breaches and risk-off positions still are (Playwright)

### ST-12 — GET /portfolio P&L handles a US position whose fill_price is NULL
**Source:** BLG-BE-167
**Priority:** P3
**Effort:** XS (<1h plus test)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- A unit test with a US position whose `fill_price` is None and a live price: `GET /portfolio` returns the row using `entry_price`

### ST-13 — Positions data dictionary states that entry_price is stored in GBP
**Source:** BLG-SPEC-190
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** After ST-09, so the dictionary and the corrected sizing describe the same convention.
**UI-facing:** No
**Acceptance Criteria:**
- `data_model_positions_dictionary.md` and `data_model.md` §2 agree with `add_position()` for every price field (`entry_price`, `fill_price`, `user_fill_price`) and for the `total_cost` and `pnl` derivations
- No spec describes `positions.entry_price` as native currency for US positions

### ST-14 — Review-cadence grace suppression and the grace alert agree once grace has ended
**Source:** BLG-SPEC-192
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** Yes (Last Reviewed flag)
**Acceptance Criteria:**
- Either the suppression predicate handles stored GRACE with null `grace_days_remaining` and holding days ≥ 10, or `positions.md` §Last Reviewed Column documents the difference
- A Playwright case (stored GRACE, `grace_days_remaining` null, holding days ≥ 10, stale review) behaves as the spec states

---

## EPIC-03 — AI Output Safety & Audit Hygiene

**Maps to:** S2-15 – S2-23
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner
**Description:** Close the AI compliance-scan gaps found in v9.12/v9.13 review: advisory journal phrasings that pass, ticker caveats on acronyms, chat stop notes misattributed to another ticker, and retrospective narrative wording that is flagged. Tidy audit logging, and retire the unused paid `generate-thesis` endpoint. Draw the first live AI output sample now that `BLG-AI-06`'s sampling hook exists.
**Estimated days:** 3.60

### ST-15 — Journal summary catches advisory phrasings the trading-change check misses
**Source:** BLG-AI-20
**Priority:** P2
**Effort:** S (~0.5d)
**Sequencing:** The ruling extension is the first sub-step (`delegated_decision` to the AI Compliance & Governance Officer). Shares `ai_s13_boundary_test_suite.md` with ST-18; land ST-15 first.
**UI-facing:** No
**Acceptance Criteria:**
- The AI Compliance & Governance Officer's extension of ruling `ESC-EXEC-20261027-03` (A) is recorded before the code change. It is a §13 determination: no §13 clause names the journal summary, so §13.1/§13.2 apply, and the ruling answers both *(restated: §13 clause-citation rule)*
- Each sentence listed in the item's Problem is reported as `trading_change` (or `prescriptive`)
- All ST-18 (v9.13) positive and descriptive test cases keep their current results; `ai_s13_boundary_test_suite.md` (B-JS) is updated

### ST-16 — Daily briefing ticker caveat ignores indicator and macro acronyms
**Source:** BLG-AI-21
**Priority:** P2
**Effort:** XS (<1h plus tests)
**Sequencing:** Before ST-17 (ST-17 reuses `_NON_TICKER_WORDS`).
**UI-facing:** No
**Acceptance Criteria:**
- The four example summaries in the item's Problem get no caveat
- `NEW_SIGNAL` and `TSLA` (ST-17 v9.13 fixtures) are still caught
- `test_non_ticker_words_ignored` covers every added word
- The live-log review of further tokens is not part of this story; if the user grants a read, its findings are added, otherwise it is filed *(restated: the second Scope bullet needs a live log/DB read, which the item itself conditions on the user's permission)*

### ST-17 — Chat stop-time note is not attributed to the focus ticker when a sentence names another ticker
**Source:** BLG-AI-22
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Sequencing:** After ST-16 (reuses `_TICKER_TOKEN_RE` and `_NON_TICKER_WORDS`). The ruling amendment is the first sub-step.
**UI-facing:** No
**Acceptance Criteria:**
- The AI Compliance & Governance Officer's amendment of `ESC-EXEC-20261027-01` (B) condition 3 is recorded before the code change. As a §13 determination it answers §13.2 and §13.5's "BLG-FEAT-50/51 (AI Advisory Layer — daily briefing + chat)" roster row, confirming that the change stays within that clearance *(restated: §13 clause-citation rule)*
- With focus `MU`, "TSLA's stop was hit last week." gets no MU note
- All ST-16 (v9.13) tests (`tests/test_ai_stop_time_focus_attribution.py`) still pass

### ST-18 — Monthly P&L narrative scan stops flagging retrospective and discourse wording
**Source:** BLG-AI-19
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** After ST-15 (shared test-suite document).
**UI-facing:** No
**Acceptance Criteria:**
- The listed retrospective and discourse sentences are not reported
- All ST-05 (v9.12) positive cases are still reported
- The representative output and the fallback still scan clean; the examples are added as B-MPN-04 negative cases in `ai_s13_boundary_test_suite.md`

### ST-19 — A debrief that fails compliance then errors writes one audit row
**Source:** BLG-BE-164
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Sequencing:** Before ST-21 (both touch `claude_audit_log` writes).
**UI-facing:** No
**Acceptance Criteria:**
- A fail-then-raise debrief writes exactly one audit row, marked `model_call_failed`
- Existing debrief audit tests still pass

### ST-20 — Stop recalculation times in briefing and chat are converted to UTC
**Source:** BLG-BE-165
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Sequencing:** Before ST-17 lands, or rebased on it (same `ai_service.py` stop-time formatter).
**UI-facing:** No
**Acceptance Criteria:**
- A `stop_calculated_at` of `2026-10-12 09:00+01:00` is rendered as `2026-10-12 08:00 UTC`; a naive value is treated as UTC (tests)
- Existing ST-08 (v9.11) tests still pass

### ST-21 — Run the claude_audit_log column checks once per process
**Source:** BLG-BE-166
**Priority:** P3
**Effort:** S (~0.5d; calibrated to 1.0d — sweep of other `ensure_*`-before-insert call sites)
**Sequencing:** After ST-19.
**UI-facing:** No
**Acceptance Criteria:**
- A second audit insert in the same process runs no DDL (asserted by a test)
- The first insert still adds missing columns
- The other `ensure_*`-before-insert call sites are listed with their count, and each is fixed or filed *(restated: the Scope's listing step made checkable)*

### ST-22 — Retire the unused POST /trade-plans/{plan_id}/generate-thesis endpoint
**Source:** BLG-BE-163
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** Coordinate with ST-28 (EPIC-04), which also edits `SystemStatus.js` and `tests/e2e/system-status.spec.js`. Whichever merges second rebases.
**UI-facing:** No ("Improve with AI" and the template button behave as before)
**Acceptance Criteria:**
- `POST /trade-plans/{plan_id}/generate-thesis` returns 404, and the OpenAPI drift gate passes
- Its `backend/routers/test.py` entry is removed, and the `SystemStatus.js` fallback count and `SC-SS-01b` are updated in the same commit (CLAUDE.md §2)
- "Improve with AI" and the template "Generate thesis" button behave as before (Playwright `trade-plan.spec.js` passes)
- One thesis-generation contract file remains, documenting `generate-plan`; the retirement is in `api_changelog.md`
- `claude/strategy/strategy_rules.md` §13.5's "Gemini thesis generation" roster row is updated to cite the surviving contract or record the endpoint's retirement, under case (c). This is a §13.5 roster change, not a new §13 review *(restated: the row cites `gemini_thesis_generation.md`, which this story merges away)*

### ST-23 — First live quarterly AI output sample against the §13 boundary
**Source:** BLG-GOV-178
**Priority:** P3
**Effort:** S (~0.5 day per quarter)
**Delegation note:** Reading production samples needs a production credential. Expected Human-Delegation to the AI Compliance & Governance Officer with the Infrastructure & Operations Owner (RISK-01).
**Sequencing:** After ST-15–ST-18, so the sample is judged against the updated scans.
**UI-facing:** No
**Acceptance Criteria:**
- 10 production AI outputs, drawn from the `BLG-AI-06` sampling hook (`ai_output_sampling_service`), are reviewed. Each is checked against §13.2 and against the §13.5 roster row for its feature (daily briefing + chat, Gemini thesis generation, ST-06 post-trade debrief, ST-25 monthly P&L narrative), with the outcome recorded in a dated audit doc *(post-merge/production data; restated: the v9.3 dry run met the item's literal AC with illustrative examples; this is the live sample the item exists for, citing every §13 clause that names AI output)*
- Each finding is filed as a backlog item
- `ESC-EXEC-20260910-01` is re-acknowledged: its deferred trigger ("`BLG-AI-06` ships") has been met, so it is resolved with this sample or re-deferred with a reason

---

## EPIC-04 — Reports, Dashboard & System Status UI (build-and-ship)

**Maps to:** S2-24 – S2-28
**Owner:** Financial Reporting & Records Owner; Frontend Specifications & UX Documentation Owner; Head of Engineering
**Description:** Show monthly realised P&L by §8 exit condition, now that exit reasons map to §8 (v9.13). Fix the Recent Trades half-penny glyph, the monthly summary's pluralisation and its lost state after switching tax year, and group `/reports` endpoints on System Status.
**Estimated days:** 2.60

### ST-24 — Monthly P&L breakdown by §8 exit condition
**Source:** BLG-FEAT-99
**Priority:** P3
**Effort:** M (~2 days)
**Sequencing:** First in EPIC-04. Gate met: `BLG-SPEC-186` shipped in v9.13 (ST-02).
**UI-facing:** Yes (new table in the Monthly P&L report)
**Acceptance Criteria:**
- A per-month table shows realised P&L and trade count for each §8 category in `metrics_definitions.md` §Exit Condition Category, taken from `backend/exit_reasons.py`
- Table totals reconcile to the month's realised P&L (test)
- Playwright asserts the table renders with the categories and a reconciling total, in both themes *(restated: CLAUDE.md §2 requires Playwright for visible rendering)*

### ST-25 — Recent Trades glyph and amount agree at a half-penny loss
**Source:** BLG-FE-213
**Priority:** P3
**Effort:** XS (<1h plus test)
**Sequencing:** Independent.
**UI-facing:** Yes (glyph and colour)
**Acceptance Criteria:**
- Playwright: `pnl −0.005` shows the down glyph and rose colour matching "−£0.01"; SC-RTB-06 (0.004 neutral, 0.01 up) still passes

### ST-26 — Pluralise the month counts in the monthly P&L summary fallback
**Source:** BLG-FE-215
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Before ST-27 (same card).
**UI-facing:** Yes (wording only; the FI-P3-02 code-review exception applies)
**Acceptance Criteria:**
- With one profitable month, the fallback text reads "1 month ended above zero" (asserted in `tests/test_monthly_pnl_narrative.py`)
- The `reports.md` §AI Summary template wording matches the code

### ST-27 — Keep a generated monthly P&L summary visible after switching tax year and back
**Source:** BLG-FE-216
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** After ST-26.
**UI-facing:** Yes (card state)
**Acceptance Criteria:**
- After Generate, switching tax year and back shows the generated summary immediately, with no empty-state render in between (Playwright)
- No extra POST is made by the round trip

### ST-28 — Group /reports endpoints on the System Status page
**Source:** BLG-FE-217
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Coordinate with ST-22 (EPIC-03), which also edits `SystemStatus.js` and `system-status.spec.js`.
**UI-facing:** Yes (System Status grouping)
**Acceptance Criteria:**
- On the System Status page, no `/reports/*` endpoint appears under "Other"
- A Playwright test asserting the grouping passes in CI

---

## EPIC-05 — Test Coverage & Test Tooling

**Maps to:** S2-29 – S2-37
**Owner:** Director of Quality; QA & Testing Owner; API Contracts & Documentation Owner
**Description:** Cover the main Positions-page exit in Playwright. Record the staging visual check that v9.13's `tailwind-merge` change still owes. Make the pre-commit contract check read staged content. Close smaller test gaps: the conftest AST scan, the grace warning's behaviour, tooltip timezones, theme assertions, `sys.path` leakage, and a flaky chat test.
**Estimated days:** 4.50

### ST-29 — Cover the Positions-page Exit modal submit in Playwright
**Source:** BLG-QA-237
**Priority:** P2
**Effort:** S (~0.5 day)
**Sequencing:** After ST-10 (EPIC-02), whose error codes the error-path scenario asserts.
**UI-facing:** No (test only)
**Acceptance Criteria:**
- The inventory's row 2 reads Covered with the new scenario IDs
- Both scenarios (successful exit; failed exit keeps the modal open with the error) pass in CI under the API status guard

### ST-30 — Staging visual check of the layout changed by tailwind-merge in cn()
**Source:** BLG-QA-235
**Priority:** P2
**Effort:** S (~0.5 day)
**Delegation note:** A human staging pass in both themes (Head of UX & Design or Director of Quality); Human-Delegation (RISK-01).
**Sequencing:** After ST-01 (a working staging and production build to compare).
**UI-facing:** Verification only (no layout change)
**Acceptance Criteria:**
- The staging run date and pages checked are recorded in this cycle's QA evidence *(restated: v9.13's `qa_evidence_EPIC-04.md` is sealed)*
- Each unintended layout change found is fixed or has a backlog item

### ST-31 — Pre-commit OpenAPI contract check reads staged content
**Source:** BLG-QA-238
**Priority:** P3 (Product Owner override, deferred lessons-learnt patch `LL-v9.13-P3-01`)
**Effort:** XS (<1h)
**Sequencing:** Early in the sprint, so the other stories' commits benefit.
**UI-facing:** No
**Acceptance Criteria:**
- An undocumented route present only in unstaged working-tree changes does not fail the hook
- An undocumented route in staged content still fails the hook
- A manual run without the hook mode still checks the working tree

### ST-32 — Confirm the conftest.py AST scan still covers every backend module
**Source:** BLG-QA-93
**Priority:** P3
**Effort:** S (~0.5-2 days)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:** *(restated: the item has a Proposed solution but no AC)*
- A test asserts that the AST scan in `tests/conftest.py` discovers every `from database import (...)` in `backend/` (vendored and virtualenv paths excluded), including subpackages added since v6.8
- Any missed subpackage is added to the scan
- The confirmation and date are recorded in the scan's docstring

### ST-33 — Behaviour test: the grace warning ignores settings.min_hold_days
**Source:** BLG-QA-214
**Priority:** P4
**Effort:** XS (<0.5 day)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- With a settings row of `min_hold_days = 5`, the warning fires on days 8–9 of the 10-day window, not days 3–4. The test fails if `alerts_service` reads `min_hold_days` from the settings row again

### ST-34 — Assert the stop-details tooltip time under a non-UTC browser timezone
**Source:** BLG-QA-215
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No (test only)
**Acceptance Criteria:**
- A new SC-SCP case asserts "Last recalculated 5 Oct 2026, 22:15 — nightly update" for a `21:15+00:00` input under Europe/London, passing in CI

### ST-35 — Assert the applied theme in every Reports/Notifications axe scan
**Source:** BLG-QA-216
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No (test only)
**Acceptance Criteria:**
- All 8 Reports/Notifications axe tests assert the applied theme before scanning, and pass in CI

### ST-36 — Stop test files adding backend/services/ to sys.path
**Source:** BLG-QA-218
**Priority:** P3
**Effort:** M (~1–2d; count named: 9 files per the item, 12 candidates by a loose grep, 2026-10-29)
**Sequencing:** Independent. Touches many test files, so it merges late in EPIC-05.
**UI-facing:** No
**Acceptance Criteria:**
- No file under `tests/` adds `backend/services` to `sys.path`, and a guard (conftest or lint) enforces it
- The full suite still passes

### ST-37 — Stop the ⌘K hint toast intercepting the chat submit click in SC-AC-03
**Source:** BLG-QA-219
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No (test only; the app is unchanged)
**Acceptance Criteria:**
- SC-AC-03 passes 10 of 10 with `--repeat-each=10` locally
- No `test.fixme` quarantine is needed

---

## EPIC-06 — Operations, Cost & Security

**Maps to:** S2-38 – S2-43
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect; Head of Engineering; Cybersecurity & Trust Lead
**Description:** Review Arc 2 compute cost and trend cost by feature area, now that the v9.13 baselines exist. Audit CI runtime. Close the daily AI cost check's end-of-day blind spot. Repair the monthly CI usage report. Stop production accepting `localhost:3000` as a CORS origin.
**Estimated days:** 4.05

### ST-38 — Arc 2 compute cost review
**Source:** BLG-OPS-21
**Priority:** P3
**Effort:** S (~1 day)
**Sequencing:** Before ST-39 (shares the cost baseline reading).
**UI-facing:** No
**Acceptance Criteria:**
- An Arc 2 compute cost comparison is produced in `docs/ops/`, covering screener batch, research endpoints and AI-assisted plan features, against the Arc 1 baseline. If no Arc 1 baseline exists, the doc says so and uses the v9.13 baseline (`docs/ops/data_pipeline_cost_baseline.md`) *(restated: the Arc 1 baseline's existence is unconfirmed)*
- The top 3 cost drivers are named, and recommendations for Arc 3 infrastructure are filed
- The gate was verified at Release Planning: PT-04 shipped v6.1 and `BLG-OPS-18` shipped v9.13 *(restated: "verified before sprint planning" is done in `run_manifest.md`)*

### ST-39 — Compute cost trending by feature area
**Source:** BLG-OPS-85
**Priority:** P3
**Effort:** S (~1 day)
**Delegation note:** Populating the report needs production cost data (Human-Delegation, RISK-01).
**Sequencing:** After ST-38.
**UI-facing:** No
**Acceptance Criteria:** *(restated: "view implemented and populated" made concrete; the gate, `BLG-OPS-74` shipped v6.8, was verified at Release Planning)*
- A report in `docs/ops/` partitions cost by feature area (AI endpoints, screener, core CRUD) from `claude_audit_log` and the API-call attribution data, and states how shared Render dyno cost is allocated
- The report is populated for at least one complete month of production data *(production data)*

### ST-40 — CI pipeline runtime audit
**Source:** BLG-OPS-105
**Priority:** P3
**Effort:** S (~0.5-2 days)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:** *(restated: the item has a Proposed solution but no AC)*
- CI runtime is profiled by workflow and by test file (pytest `--durations`, Playwright per-spec timing) from at least 3 recent `main` runs, and the slowest 10 contributors are recorded in `docs/ops/`
- Each optimisation or parallelisation candidate is filed as a backlog item

### ST-41 — Daily AI cost check covers the last hours of the day
**Source:** BLG-OPS-186
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- Spend between the last run and midnight is checked against its own day's threshold, and `ai_endpoints.md` §POST /ai/check-daily-cost is updated
- A test covers the day-boundary case

### ST-42 — Make ci-usage-report.yml's monthly commit succeed
**Source:** BLG-OPS-188
**Priority:** P3
**Effort:** XS (<0.5d)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- A `ci-usage-report.yml` run succeeds and its report reaches `docs/ops/ci_usage_reports/` (or the agreed destination)
- `docs/ops/ci_usage_reports/2026-09.md` exists

### ST-43 — Per-environment CORS allow-list
**Source:** BLG-SEC-43
**Priority:** P3
**Effort:** S (~0.5 day)
**Delegation note:** Setting the per-environment variable on Render needs dashboard access (Human-Delegation, RISK-01).
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- The allowed origins are built from a per-deployment environment variable with documented defaults. A test shows that, in production configuration, `http://localhost:3000` is rejected and the Pages origin is accepted
- The staging and production preflight checks are recorded *(post-merge: the production check needs the deployed service)*

---

## EPIC-07 — Specs & Governance

**Maps to:** S2-44 – S2-54
**Owner:** Head of Specs Team; PMO Lead; Metrics Definitions & Analytics Owner; Strategy Rules & System Intent Owner; API Contracts & Documentation Owner; Frontend Specifications & UX Documentation Owner; Challenger
**Description:** Land v9.13's two deferred governance patches: execution-state consistency checks, and a write-back path for gating-item-shipped findings. Clear spec debt in specs, contracts and metrics. Add the long-waiting governance aids: §13 worked examples, governance overhead and spec-debt aging.
**Estimated days:** 6.80

### ST-44 — check_execution_state_consistency.py checks deviations_filed and the escalation map
**Source:** BLG-GOV-397
**Priority:** P3 (Product Owner override, deferred lessons-learnt patch `LL-v9.13-P3-04`)
**Effort:** S (~0.5 day)
**Sequencing:** Before ST-45 (both bump `OPERATIONAL_GUIDE.md`; apply CLAUDE.md §8 step 2a per file).
**UI-facing:** No
**Acceptance Criteria:**
- The script exits non-zero, naming the story, when a `done` story has `deviations_filed: false`
- The script exits non-zero, naming the ID, when an `ESC-EXEC-*` heading has no `open_escalations` key
- Unit tests cover both failure cases and the passing case
- `execution_prompt.md` §9.2 names both checks, with the CLAUDE.md §6 governance edit checklist complete

### ST-45 — Give the gate scan's "gating item shipped" findings a write-back path
**Source:** BLG-GOV-398
**Priority:** P3 (Product Owner override, deferred lessons-learnt patch `LL-v9.13-Release-01`)
**Effort:** XS (~0.25 day)
**Sequencing:** After ST-44. The Head of Specs Team's choice between (a) the `release_planning_prompt.md` §1.3a carve-out and (b) a `groom backlog` standing step is the first sub-step.
**UI-facing:** No
**Acceptance Criteria:**
- The chosen prompt names the "gating item shipped" list and the write it permits, with the CLAUDE.md §6 checklist complete
- After the next run of that engine, no item whose whole gate condition is a shipped item is re-listed by the scan (`BLG-OPS-85` and `BLG-OPS-21` are the live cases)

### ST-46 — Document the gate-status indicator as a reusable component pattern
**Source:** BLG-SPEC-77
**Priority:** P3
**Effort:** S (~0.5-2 days)
**Sequencing:** Independent.
**UI-facing:** No (documentation)
**Acceptance Criteria:** *(restated: the item has a Proposed solution but no AC)*
- The frontend spec documents the gate-status indicator pattern (states, copy rules, props, accessibility), with the SI-02 indicator (`BLG-FEAT-71`) as the reference implementation
- The Frontend Specifications & UX Documentation Owner records the review

### ST-47 — risk_dashboard.md names only fields GET /portfolio returns
**Source:** BLG-SPEC-189
**Priority:** P3
**Effort:** XS (~0.25 day)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- §5.1 and §6.1 name only fields that `GET /portfolio` returns (`grace_period`, `display_status`)

### ST-48 — Align Appendix F's effort-weighted PVR table and status with the script
**Source:** BLG-SPEC-191
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** After ST-51 (adds the changelog section this story writes to).
**UI-facing:** No
**Acceptance Criteria:**
- The table and `scripts/compute_effort_weighted_pvr.py` weight exactly the same set of effort values
- Appendix F names `roadmap_prompt.md` STEP 2.4 (v9.32) as where the effort-weighted reading is recorded; the other two sub-metrics still read proposal-only
- A changelog row is added in `metrics_definitions.md`

### ST-49 — Trade plan contract lists the 7 DS-21 statuses
**Source:** BLG-SPEC-193
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `trade_plan_endpoints.md` and `trade_plan_data_sensitivity.md` list the same 7 statuses as `openapi.yaml` and `data_model.md` DS-21
- `grep` finds no current-state spec listing the 3- or 4-value set (historical migration notes excepted)

### ST-50 — Confirm "win rate" is computed the same way on every surface
**Source:** BLG-GOV-184
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- Every surface showing a win rate (dashboard, P&L report, drift analytics, journal, and any other found by grep) is checked against `metrics_definitions.md`. The result is recorded, and any discrepancy is filed as a correctness backlog item

### ST-51 — Add a changelog section to metrics_definitions.md
**Source:** BLG-GOV-185
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** Before ST-48.
**UI-facing:** No
**Acceptance Criteria:**
- A changelog section is added with at least the most recent known formula change recorded, plus the known recent changes the history shows (`git log -p`)

### ST-52 — §13 boundary worked examples
**Source:** BLG-GOV-186
**Priority:** P3
**Effort:** S (~1 day)
**Sequencing:** Independent. Reviewed by the Strategy Rules & System Intent Owner.
**UI-facing:** No
**Acceptance Criteria:**
- A companion document, `docs/product/decisions/section13_boundary_examples.md`, gives 1–2 right/wrong examples for each §13 sub-clause: §13.1, §13.2, §13.3 (including the gap-risk display-only carve-out), §13.4, §13.5 and §13.6 *(restated: the item allows a companion doc; choosing it keeps `strategy_rules.md` out of this story's writes)*
- The Strategy Rules & System Intent Owner's review is recorded, answering each cited clause

### ST-53 — Governance overhead audit
**Source:** BLG-GOV-189
**Priority:** P3
**Effort:** S (~1 day)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- A retrospective estimate of PMO, spec and governance effort against the shipped-story count over the last 10 release cycles is produced in `docs/governance/`, using the cycles' run manifests and sprint backlogs as the proxy. The method is stated
- The findings are linked from the next rebalance's input (recorded as a carry-forward for the next `run roadmap`)

### ST-54 — Spec debt aging report
**Source:** BLG-GOV-191
**Priority:** P3
**Effort:** S (~0.5-2 days)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:** *(restated: the item has a Proposed solution but no AC)*
- A script lists open `BLG-SPEC-*` items by the number of release cycles they have been in a ready pool without a story (the `release_planning_prompt.md` §1.1 measure), with a test
- One run's output is recorded; wiring it into a governance prompt is filed separately, not done here
