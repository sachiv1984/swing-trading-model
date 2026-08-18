Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-17

# QA Evidence Log — EPIC-01 (Live Risk-Management Correctness)

**EPIC:** EPIC-01 — Live Risk-Management Correctness
**Cycle:** 2026-08-17__release-v8.9
**Sprint goal:** Ship v8.9: eliminate the two live risk-management stop-price defects on open positions (breakeven-floor ratchet, currency-basis mismatch) and deliver the sector-aware position sizing, pre-commit risk simulator, AI post-trade debrief, and in-app backtesting foundations of the Trade Intelligence Expansion — while clearing this cycle's reliability, QA, ops, and governance debt.
**Test scenarios used:** tests/test_trailing_stop_breakeven_floor.py (7 scenarios); tests/test_position_currency_basis.py (2 scenarios); tests/e2e/position-stop-currency-basis.spec.js (2 scenarios, V-CURR-01/V-CURR-02)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `backend/utils/calculations.py#calculate_trailing_stop`; `tests/test_trailing_stop_breakeven_floor.py` | Confirmed (code-path audit) both live production stop-writing paths already call the shared, floored `calculate_trailing_stop()` — `position_manager.py`'s unfloored inline calc is a backtest-tool-only path, never invoked live. Added 7 regression tests including the exact BLG-BE-102 WDC worked example, plus 2 structural tests confirming the single-calc-path claim. | Only one trailing-stop calculation path is used in production (nightly job and any on-demand recompute); No open profitable position has `current_stop` below its own `entry_price` (staging-only — live-position DB query, not CI-reproducible); Regression test added and passing, covering the breakeven-floor case; Backend Engineering Patterns Owner sign-off | Pass with notes | None |
| ST-02 | `docs/specs/api_contracts/position_endpoints.md#Field notes`; `docs/specs/frontend/pages/positions.md#Trailing Stop Column`; `tests/test_position_currency_basis.py`; `tests/e2e/position-stop-currency-basis.spec.js` | Added `current_trailing_stop_native` to `GET /positions` (native-currency counterpart of the GBP-converted `current_trailing_stop`); `PositionCard.js`/`Positions.js` now render it on both Card and Table views; corrected a related native-fallback bug in the Trail Stop modal. Filed and resolved same-story as `DEV-EPIC01-ST02-01` in `positions.md#Known Deviations`. | `initial_stop`, `current_trailing_stop`, and `stop_price` are all in the same currency basis (native) for a given position, or are unambiguously suffixed and the frontend consumes the correct one; A US-market profitable position test case shows a single consistent stop value across Init and live-stop tiles; Backend Engineering Patterns Owner and Frontend Specifications & UX Documentation Owner sign-off | Pass | DEV-EPIC01-ST02-01 (resolved same-story) |
| ST-03 | `docs/specs/metrics_definitions.md#Trailing Stop Action Rate` | Added `## Validation Tolerances` subsection to the pre-existing Trailing Stop Action Rate section: numeric bounds for insufficient-sample, expected range, anomalously low/high, and stale-capture conditions. Version 1.16.1 → 1.17.0. | Entry added to `metrics_definitions.md`; tolerances stated numerically, not qualitatively | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_trailing_stop_breakeven_floor.py` (7/7 pass), `tests/test_position_currency_basis.py` (2/2 pass) — full backend suite `backend/.venv/bin/python3 -m pytest tests/` 1170 passed / 5 skipped, 0 failed, 0 regressions. `tests/e2e/position-stop-currency-basis.spec.js` (2/2 pass, new). Full trailing-stop-adjacent Playwright sweep (6 pre-existing spec files touching `current_trailing_stop`/`trailStop`/`displayTrailStop`) re-run in full: 57/57 pass, including the 2 pre-existing fixtures (`epic01-v62-stops-alerts.spec.js`, `epic01-v70-grid-badge-parity.spec.js`) updated to populate `current_trailing_stop_native`.
- Regression areas checked: `backend/services/position_service.py::get_positions_with_prices()` response shape (additive field only, no existing field changed); `PositionCard.js`/`Positions.js` Trail Stop tile rendering (Card + Table views); Trail Stop modal fallback; all Positions-page e2e coverage touching trailing-stop/breach-badge display.
- Known deviations: DEV-EPIC01-ST02-01 (positions.md#Known Deviations) — filed and resolved in the same story, per BLG-BE-103. No other deviations found — ST-01 and ST-03 deviation checks completed with nothing to file.

**Frontend testing gate (execution_prompt.md §3.2.A):** ST-02 introduces a frontend-visible change (Trail Stop tile value on `PositionCard.js`/`Positions.js`). Covered by new Playwright scenarios V-CURR-01 (Card view) and V-CURR-02 (Table view) in `tests/e2e/position-stop-currency-basis.spec.js`, both passing in this session's local run. The BLG-GOV-19 autonomous class sign-off does not apply to this EPIC (criterion 3 unmet — `src/components/positions/PositionCard.js` and `src/pages/Positions.js` both modified) — Standard Sign-Off Block with Mixed-Class Signer Format used below.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no story in this EPIC constructs URLs directly

> **Mixed-Class EPIC Signer Format (ST-11 / LL-v5.2-P4-01):** EPIC-01 contains both `delegated_backend` stories (ST-01, ST-02) and an `autonomous` story (ST-03) — agent-mediated format required.

- Signed off by: Sprint Execution Engine (agent-mediated, Backend Engineering Patterns Owner role — §5.3)
  Sprint Execution Engine (agent-mediated, Frontend Specifications & UX Documentation Owner role — §5.3)
- Date: 2026-08-17
- Comments: Story-level sign-offs provided by Backend Engineering Patterns Owner (ST-01, ST-02) and Frontend Specifications & UX Documentation Owner (ST-02), agent-mediated per §5.3 — see below. All three stories Approved on first pass; reviewed and acknowledged in aggregate — all acceptance criteria met (ST-01's live-DB backfill AC remains staging-only, tracked separately, per its own Notes field), no unresolved P0/P1 gaps.

### Story-level authority sign-off (BLG-GOV-14 — required in addition to, not instead of, the EPIC-level block above)

**Backend Engineering Patterns Owner** (ST-01, ST-02):
- Signed off by: Sprint Execution Engine (agent-mediated, Backend Engineering Patterns Owner role — §5.3)
- Date: 2026-08-17
- Comments: ST-01 Approved — confirmed via `git blame` that both live stop-writing entry points (`analyze_positions()`, `run_nightly_trailing_stop_update()`) have called the floored `calculate_trailing_stop()` since commit `b410cfa3c` (2026-02-12), predating this cycle; this story's deliverable is verification + regression coverage of an already-correct live path, not a behavioural fix. `position_manager.py` confirmed not on the live path (only live cross-import is `check_market_regime`, unrelated to stop calc); its unfloored formula is deliberately reconciled without the floor by the pre-existing `test_stop_reconciliation.py` (backtest-tool parity, not a live-path requirement). WDC worked example reproduced exactly: `max(163.31, 508.80−2×54.1986, 434.30) = 434.30`. One AC (no open profitable position below entry_price) remains a deferred live-DB backfill/recompute action per the story's own Notes field and sprint_backlog.md's staging-only-AC flag — not covered by this commit, tracked as a post-merge ops follow-up. ST-02 Approved — `current_trailing_stop_native` correctly computed as the raw unconverted `current_stop` value, matching the pre-existing `stop_price_native` pattern; verified across all three frontend consumers including the Trail Stop modal's fallback fix; `trailBreached` GBP-vs-GBP comparisons correctly unaffected.
- Known deviations: None found for ST-01 beyond the staging-only AC noted above (not a code deviation).

**Frontend Specifications & UX Documentation Owner** (ST-02):
- Signed off by: Sprint Execution Engine (agent-mediated, Frontend Specifications & UX Documentation Owner role — §5.3)
- Date: 2026-08-17
- Comments: Approved. Verified the two pre-existing e2e fixture updates (`epic01-v62-stops-alerts.spec.js`, `epic01-v70-grid-badge-parity.spec.js`) preserve original test intent — both files assert only badge/label text (breach pill, RISK OFF badge), never the numeric stop display value, so mirroring `current_trailing_stop_native` to `current_trailing_stop` by default is a legitimate schema-completion, not a forced pass. New regression tests are non-trivial: the pytest test dynamically derives the expected GBP value from `live_fx_rate` and asserts inequality with the native value; the Playwright test uses deliberately distinct native ($100.00) vs GBP ($76.92) fixture values and asserts zero occurrences of the wrong-basis value. `position_endpoints.md` and `positions.md` version bumps, changelogs, and `DEV-EPIC01-ST02-01` filing all correctly formatted and cross-referenced.

**Metrics Definitions & Analytics Owner** (ST-03):
- Signed off by: Sprint Execution Engine (agent-mediated, Metrics Definitions & Analytics Owner role — §5.3)
- Date: 2026-08-17
- Comments: Validation Tolerances subsection reviewed against the pre-existing Trailing Stop Action Rate definition (bounded 0.0–1.0, existing 24h capture window) — numeric bounds (insufficient-sample <5, expected range 0.05–0.95, anomalous <0.05/>0.95 at N≥10, stale capture >30 days) are internally consistent and satisfy the "numerically, not qualitatively" AC.
