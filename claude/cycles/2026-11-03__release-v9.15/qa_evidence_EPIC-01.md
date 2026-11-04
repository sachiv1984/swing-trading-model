Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-04

# QA Evidence — EPIC-01 — Trade Entry Integrity & Sizing

**EPIC:** EPIC-01 — Trade Entry Integrity & Sizing (build-and-ship)
**Cycle:** 2026-11-03__release-v9.15
**Branch:** `exec/2026-11-03__release-v9.15/EPIC-01`
**Sprint goal:** Make every route into Trade Entry show the §4.2 pre-entry checks and pre-fill the live FX rate (BLG-FE-244, BLG-FE-245, P1). Deliver Site Structure & Usability Phase 1: navigation v2/glossary, Dashboard "Today" and Journal area specs approved, one name per page, legacy Dashboard route removed, per-page tab titles. Ship v9.15's metric-correctness, AI-check, operations, data-model and governance items alongside.
**Test scenarios used:** `tests/test_trade_entry_pre_entry_override.py`, `tests/test_market_atr_preview_endpoint.py`, `tests/test_strategy_version_registry.py`, `tests/test_stop_trail_value.py`, `tests/e2e/trade-entry-pre-entry-checks.spec.js`, `tests/e2e/trade-entry-fx-rate.spec.js`, `tests/e2e/local-date-prefill.spec.js`, `tests/e2e/positions-exit-modal.spec.js`, `tests/e2e/signal-card.spec.js`

## Story-Level Authority Records

- **ST-01 strategy ruling:** `ESC-EXEC-20261104-01`, Strategy Rules & System Intent Owner, Branch A (acknowledge to proceed), given in session by the user acting in that role, 2026-11-04. Applied as the case (c) `strategy_rules.md` v1.23 write (§4.2.1, §4.2.6) with its Change Log row and `STRATEGY_VERSION_REGISTRY` entry, commit `e0a78667`. Owner confirmation of the named-file line at seal: 2026-11-03 (`sprint_backlog.md` Named-file writes).

## Evidence Table

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `position_form.md` v1.13 §Pre-Entry Checks; `trade-entry-pre-entry-checks/decision_record.md`; `portfolio_endpoints.md` v2.15.0; `strategy_rules.md` v1.23 §4.2.1, §4.2.6 | Shared `PreEntryValidationPanel` (moved from `TradePlan.js`) on Trade Entry for every route; on-plan line when a linked plan has a stored snapshot; Branch A Submit gating with helper line; `pre_entry_override_acknowledged` writes a `pre_entry_override` event (`source: trade_entry`). Commit `e0a78667`. | AC 1 (three routes show results before save): SC-TEPC-01 sidebar, SC-TEPC-02 "New Position", SC-TEPC-03 `n`. AC 2 (risk-off/unknown FAIL, save requires acknowledgement): SC-TEPC-04, SC-TEPC-05; also SC-TEPC-09 (endpoint failure never blocks), SC-TEPC-10 (all pass: no flag). AC 3 (plan-linked not shown twice): SC-TEPC-07, SC-TEPC-08. AC 4 (Playwright in CI): Playwright E2E run 41820859317 on `a4914ce9` (contains `e0a78667`) success. Backend: `test_trade_entry_pre_entry_override.py` (event written once, no event when unticked, failed write does not fail save). | Pass | None |
| ST-02 | `position_form.md` v1.12 §FX Rate; `trade-entry-fx-rate/decision_record.md` §2.2–§2.3 | US FX field pre-filled at 4 dp from `GET /market/status`; source line (live / last known / fallback / entered by you / request failed); typed value never overwritten; Market select now resets FX. Commit `a4914ce9`. | AC 1 (mocked 1.35 pre-fills with source and age): SC-TEFX-01. AC 2 (no rate: fallback shown with a visible fallback note): SC-TEFX-02 ("Fallback rate: no live rate is available"); SC-TEFX-03 (request failed). AC 3 (no `"1.27"` in `TradeEntry.js`): grep count 0. AC 4 (Playwright in CI): run 41820859317 on `a4914ce9` success. Also SC-TEFX-04/05/06. | Pass with notes | None. Note: the spec cites an "FX rate missing for US trades" client validation that `TradeEntry.js` never had; an empty US rate is sent as `null` and the server uses its live rate (implementation note, intent unchanged). |
| ST-03 | `position_form.md` v1.12 §FX Rate; `exit_modal.md` v1.2 §FX Rate; `trade_plan.md` v1.21 §5d.2 | Label "FX rate — USD per £1 (GBP/USD)" and hint "How many US dollars £1 buys." (aria-describedby) on all three FX inputs: Trade Entry, Exit dialog, What-If Sizing Preview. Commit `4c7b10ee`. | AC 1 (every FX input label in `src/` uses the same wording): grep of `src/` finds three FX rate inputs, all changed; no old label remains. AC 2: Pass — text-only change, no rendered-output difference beyond the label text; verified by code review per CLAUDE.md §2's FI-P3-02 exception. | Pass | None |
| ST-04 | BLG-FE-243 (Design Pre-Approved); `src/lib/localDate.js` | `localDateString`/`todayLocal` helper; 15 sites reviewed, every user-facing "today" or user-picked day switched (Trade Entry, Exit dialog ×2, Cash Management, exit-date fallback, Dashboard peak date ×4, two CSV file names, Red Flags 7-day filter, Trade History calendar day). Commit `98314abf`. | AC 1 (00:30 BST Europe/London: Exit, Trade Entry, Cash Management prefill the local date): SC-LDP-01..03 (Cash Management has no visible date field; SC-LDP-03 checks the date sent with a deposit). AC 2 (new Playwright case passes in CI): pending CI on `cbaaecd2`. AC 3 (no user-facing "today" from `toISOString().split`): grep — only `PortfolioGrowthChart.js` remains, which walks a stored period's dates. SC-PEM-01 now asserts the local date. | Pass (CI pending) | None |
| ST-05 | `portfolio_endpoints.md` v2.15.0; `positions.md` v2.23 §Exit Dialog deep link | Ticker trimmed and upper-cased in `AddPositionRequest`, `add_position()` and Trade Entry (preview, checks, submit); `?exit=` and `?position=` share `isOpenPosition`. Commit `e0a78667`. | AC 1 (untrimmed/lower-case: preview stop equals saved `initial_stop`): four new parametrised cases in `test_market_atr_preview_endpoint.py`, plus the endpoint-level normalisation test. AC 2 (same open-position test): code review of `Positions.js`. CI Pytest 41820859397 on `a4914ce9` success. | Pass | None |
| ST-06 | `positions.md` v2.22 §Trail Stop Action; `stop_trail_endpoint.md` v1.1.0; `trail-stop-modal-wording/decision_record.md` §2.2 | `GET /positions/{id}/stop-trail` computes `atr_trail_stop` with `calculate_trailing_stop` and `stop_multiplier_settings()` (breakeven floor); modal footnote reworded with no literal multiplier. Commit `5906bfa7`. | AC 1 (equals `calculate_trailing_stop` for a profitable position, incl. floor binding): `test_stop_trail_value.py` (profit case, floor case, parametrised equality). AC 2 (no literal multiplier in handler or footnote): source-scan test + code review of the footnote (FI-P3-02 wording). | Pass with notes | None. Note: the candidate is not ratcheted against `current_stop` (`-inf`), so `trail_difference` stays signed; it equals `calculate_trailing_stop`'s result whenever the stored stop is below the candidate. The contract is `stop_trail_endpoint.md`, not the `position_endpoints.md` the slice named. |
| ST-07 | `signals.md` v0.8; `signal_endpoints.md` v1.10; `signal-card-cost-and-sizing-reason/decision_record.md` | "Total cost (incl. fees)" label; two zero-ATR `reason` strings reworded in `sizing_service.py`. Commit `cbaaecd2`. | AC (label and reason changed; Playwright asserts the reason line for a zero-ATR signal): SC-SIG-ZA-01, SC-SIG-ZA-02. CI pending on `cbaaecd2`. | Pass (CI pending) | None |

## QA Test Coverage

- **Scenarios run (local, 2026-11-04, against a production build):** SC-TEPC-01..10, SC-TEFX-01..06, SC-LDP-01..03, SC-PEM-01/02, SC-SIG-* (14), and the other Trade Entry specs (121 tests across 18 files). Backend: the four test files above, `test_add_position_stop_handling.py`, `test_trailing_stop_recommendation_log.py`, sizing/signal tests, `backend/mutmut_pilot_tests/test_pilot.py`.
- **CI:** all 9 workflows success on `a4914ce9` (ST-01, ST-02, ST-05). Runs on `cbaaecd2` (ST-03, ST-04, ST-06, ST-07) pending at time of writing; must be cleared before DoQ sign-off.
- **Regression areas checked:** Trade Plan form (shared panel; `pre-entry-panel-badge.spec.js` passes), Trade Entry stop/ATR preview, Positions exit and deep links, Cash Management, Signals page.
- **Flake observed:** `v7.2-dashboard-tradeplan-ux-hardening.spec.js` SC-STP-06 failed once locally when the Layout "⌘K" tip toast covered Create Position on the now-taller Trade Entry page; passed 3/3 on repeat. Single, unreproduced occurrence (Flaky-Test Disposition step 1): not quarantined.
- **Known deviations:** None found — all stories' deviation checks completed with nothing to file. Implementation notes for ST-02 and ST-06 are recorded in their rows.

## Frontend Testing Gate

Every observable AC has Playwright coverage (ST-01, ST-02, ST-04, ST-07). ST-03 and the ST-06 footnote are wording-only (FI-P3-02). No AC is "code review only" for visual rendering, colour, layout or interaction timing, so no backlog item is required.

## Standard Sign-Off Block

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- [ ] **Strategy values checked:** ST-01 — §4.2.1 regime gate, §4.2.6 non-blocking principle (v1.23); ST-02 — §4.1.3/§4.1.5 FX as USD per £1 for US sizing; ST-05 — §5 initial stop (`entry − 5 × ATR`) preview equals save; ST-06 — §7.2 profitable stop with breakeven floor, §11 `PROFIT_ATR_MULTIPLIER`/`INITIAL_ATR_MULTIPLIER`; ST-07 — §4.1 inverse-volatility sizing reason only (no value changed).
- Signed off by:
- Date:
- Comments:
