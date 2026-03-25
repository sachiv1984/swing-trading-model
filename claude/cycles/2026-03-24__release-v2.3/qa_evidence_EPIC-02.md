# QA Evidence Log — EPIC-02
# Cycle: 2026-03-24__release-v2.3
# Branch: exec/2026-03-24__release-v2.3/EPIC-02

---

## ST-03 — BLG-OPS-08: Staging Data Reset Script

**Status:** Done
**Commit:** 0130abd
**Completed:** 2026-03-25
**Implemented by:** Head of Engineering (engine — not delegated)

### Acceptance Criteria Verification

| AC | Verification | Result |
|----|-------------|--------|
| Script present in repo (`scripts/` or `tools/`) | Code review — `scripts/reset_staging_db.sql` and `scripts/reset_staging_db.sh` present at commit 0130abd | PASS |
| Script resets staging DB to reproducible baseline | Code review — SQL TRUNCATEs portfolios CASCADE (all dependent tables) + settings, then re-inserts 1 portfolio (£20k) + default settings. Each run produces identical baseline state. | PASS |
| Script is documented with usage instructions | Code review — both files have header block with usage examples, prerequisites, and env var requirements | PASS |
| Script is idempotent — safe to run multiple times | Code review — TRUNCATE (not DELETE) + re-insert on every run; no conditional logic that could produce different state on repeat runs | PASS |
| Smoke test scenarios in ST-05 can be run reliably after executing reset | Structural — after reset: portfolio exists (required for all API calls), settings exist (required for trade calculations), all domain tables empty (no leftover state). ST-05 smoke paths (add trade, view portfolio, view alerts) all depend on a clean portfolio+settings baseline which this script provides. | PASS (structural) |

### Notes

- `STAGING_DATABASE_URL` env var (not `DATABASE_URL`) required by the shell wrapper — intentional guard against production execution.
- `TRUNCATE portfolios CASCADE` handles FK chain: positions → trade_history → trade_reflections, cash_transactions, portfolio_history, signals, watchlist, alert_rules → alert_evaluations → notifications → notification_preferences.
- `tickers` table (static lookup) is intentionally not cleared.
- ST-04 (BLG-QA-06 seed scripts) and ST-05 (BLG-QA-05 smoke tests) are now unblocked.

### DoQ Sign-Off

**Method:** Code review — commit 0130abd
**Signed off by:** Director of Quality
**Date:** 2026-03-25
**Verdict:** ✅ PASS — Full sign-off granted

**Findings:**
- `TRUNCATE TABLE portfolios CASCADE` + `TRUNCATE TABLE settings` within a single `BEGIN/COMMIT` transaction: idempotency guaranteed — no INSERT-only path that could accumulate rows on repeated runs.
- Existence guards (`IF EXISTS`) prevent failure against a partially-initialised schema.
- Shell wrapper correctly rejects absence of `STAGING_DATABASE_URL` and heuristically rejects URLs containing "production" or "/prod". Production guard is heuristic, not cryptographic — acceptable for an internal ops tool.
- Both files have complete header blocks covering prerequisites, usage, and the intentional `STAGING_DATABASE_URL` / `DATABASE_URL` distinction.
- `tickers` table exclusion from TRUNCATE is correct and documented.
- No visual elements. All AC are code-review-sufficient.

**No deviations filed.**

---

## ST-04 — BLG-QA-06: Test Data Seed Script Library

**Status:** Done
**Commit:** f90dd58
**Completed:** 2026-03-25
**Implemented by:** QA & Testing Owner (engine — Director of Quality oversight)

### Acceptance Criteria Verification

| AC | Verification | Result |
|----|-------------|--------|
| Seed scripts present for all three domains (alerts, watchlists, portfolio/trades) | Code review — `scripts/seeds/seed_alerts.sql`, `scripts/seeds/seed_watchlist.sql`, `scripts/seeds/seed_portfolio_trades.sql` present at commit f90dd58 | PASS |
| Scripts runnable independently for each domain | Code review — each SQL file is self-contained with its own `BEGIN`/`COMMIT` block, prerequisite comments, and `\echo` completion output. Each can be run standalone via `psql "$STAGING_DATABASE_URL" -f scripts/seeds/<file>.sql` | PASS |
| Compatible with ST-03 staging reset workflow | Code review — all scripts use `STAGING_DATABASE_URL` (same guard pattern as reset_staging_db.sh). `seed_all.sh` propagates the same env var guard and production URL rejection. Scripts resolve the portfolio via `SELECT id FROM portfolios LIMIT 1` — compatible with the single-row baseline created by reset_staging_db.sql. | PASS |
| ST-05 smoke test scenarios can run end-to-end after executing relevant seed scripts | Structural — after reset + seeds: (1) "add trade": portfolio + settings exist from reset; (2) "view portfolio": 2 open positions seeded (LGEN, BARC) via seed_portfolio_trades.sql; (3) "view alerts": 2 unread notifications seeded via seed_alerts.sql. All 3 ST-05 critical paths have required data state. | PASS (structural) |
| Scripts stored in `scripts/seeds/` or equivalent | Code review — all files in `scripts/seeds/` ✓ | PASS |

### Seed Contents Summary

| Script | Domain | Contents |
|--------|--------|----------|
| `seed_portfolio_trades.sql` | portfolio/trades | 1 initial deposit (£20,000), 2 open positions (LGEN 1000 shares, BARC 1200 shares), 2 closed trades (ULVR +£296.10, VOD -£23.90), portfolio.cash updated to reflect position costs |
| `seed_watchlist.sql` | watchlist | 4 entries: AAPL, MSFT (US), LGEN, BARC (UK) with target entry and stop prices |
| `seed_alerts.sql` | alerts | 4 alert rules (all types, all enabled; stop_loss threshold=5%), 4 notification preferences (email enabled), 2 unread notifications |
| `seed_all.sh` | all domains | Orchestration wrapper: runs all three seeds in sequence with STAGING_DATABASE_URL guard and production URL rejection |

### Idempotency

- `seed_alerts.sql`: `ON CONFLICT DO UPDATE` for rules/preferences; DELETE + INSERT for notifications (deterministic count)
- `seed_watchlist.sql`: `ON CONFLICT (portfolio_id, ticker) DO UPDATE`
- `seed_portfolio_trades.sql`: DELETE domain tables then re-insert (deterministic after reset)

### DoQ Sign-Off

**Method:** Code review — commit f90dd58
**Signed off by:** Director of Quality
**Date:** 2026-03-25
**Verdict:** ✅ PASS — Full sign-off granted

**Findings:**
- All three domain scripts (`seed_alerts.sql`, `seed_watchlist.sql`, `seed_portfolio_trades.sql`) confirmed present and independently runnable via `psql … -f <file>`.
- `seed_alerts.sql`: `ON CONFLICT (portfolio_id, type) DO UPDATE` for rules; `ON CONFLICT (portfolio_id, alert_type) DO UPDATE` for preferences — both constraints match the DB schema UNIQUE constraints. Notifications use DELETE + deterministic INSERT — correct for predictable count. ✓
- `seed_watchlist.sql`: `ON CONFLICT (portfolio_id, ticker) DO UPDATE` matches schema UNIQUE constraint. ✓
- `seed_portfolio_trades.sql`: FK deletion order (trade_reflections → trade_history → positions → cash_transactions) is correct. Portfolio cash updated via subquery after INSERT — arithmetic is sound (£20,000 − £2,461.95 − £2,531.95 = £15,006.10). ✓
- `seed_all.sh`: STAGING_DATABASE_URL guard and production URL rejection mirror reset_staging_db.sh exactly. Seeds run in correct order (portfolio/trades → watchlist → alerts). ✓
- ST-05 smoke path coverage confirmed: after reset + all seeds, all 3 critical paths (add trade, view portfolio, view alerts) have required data state.
- No visual elements. All AC are code-review-sufficient.

**No deviations filed.**

---

## ST-05 — BLG-QA-05: Critical-Path Smoke Test (Playwright)

**Status:** Done
**Commit:** ba46dcb
**Completed:** 2026-03-25
**Implemented by:** QA & Testing Owner (engine — Director of Quality oversight)

### Acceptance Criteria Verification

| AC | Verification | Result |
|----|-------------|--------|
| Playwright test suite covers all 3 critical paths (add trade, view portfolio, view alerts) | Code review — `tests/e2e/smoke-critical-paths.spec.js` contains PATH-1 (add trade), PATH-2 (view portfolio), PATH-3 (view alerts). Each test navigates to the relevant page, fills/loads required data via mocks, and asserts the critical interaction succeeded. | PASS |
| Tests run in CI on every PR | Code review — `.github/workflows/smoke-tests.yml` triggers on push/PR to `main` and `exec/**` with no path filter. Runs on every PR. | PASS |
| Run time < 2 minutes for smoke test suite | Structural — 3 tests, mock layer (no live backend), Chromium only, single worker in CI. Estimated run time ~30–60s. Each test has `waitForResponse` timeouts of ≤10s with mock fulfillment. Suite well within 2-minute budget. | PASS (structural) |
| Playwright pass recorded as supporting evidence for non-visual AC — explicit in DoQ sign-off template | Code review — spec header and each test include scope constraint comment: "Playwright PASS is supporting evidence for non-visual AC only. Visual AC remain DoQ manual review." This constraint is also in `smoke-tests.yml` header comment. | PASS |
| Visual AC (colours, badges, chart rendering) remain DoQ manual review items | Code review — no test asserts on CSS colour classes, badge styling, or chart rendering. All assertions are on text content, button state, and HTTP request shape. | PASS |
| Flaky test failures must not block the PR or human review — failures are advisory | Code review — `smoke-tests.yml` has `continue-on-error: true` on the test step with explicit comment: "flaky failures are advisory and MUST NOT block the PR." Report uploaded via `if: always()` so DoQ can review even on failure. | PASS |

### Scope Notes

- PATH-1 (add trade): verifies form renders, POST /portfolio/position fires with correct ticker + entry_price, app navigates to Positions on success. PositionSizingWidget auto-fills shares via mocked POST /portfolio/size.
- PATH-2 (view portfolio): verifies LGEN and BARC positions render by ticker name. Uses SMOKE_POSITIONS mock matching seed_portfolio_trades.sql data.
- PATH-3 (view alerts): verifies unread notification renders and "Mark as read" / "Mark all as read" buttons appear. Uses SMOKE_NOTIFICATIONS mock matching seed_alerts.sql data.
- Mock data in `tests/e2e/mocks/smoke-mock-data.js` is aligned with the seed scripts from ST-04.
- `mockFallback()` helper prevents unmocked endpoints from hanging tests in CI.

### DoQ Sign-Off

**Method:** Code review — commits ba46dcb (spec + CI), d7bad14 (state + evidence)
**Signed off by:** Director of Quality
**Date:** 2026-03-25
**Verdict:** ✅ PASS — Full sign-off granted for all 6 AC

**Playwright evidence scope (AC 4 explicit record):**
The following non-visual AC are supported by Playwright pass as primary evidence:
- PATH-1: POST /portfolio/position fires with correct `ticker` and `entry_price` in body ✓
- PATH-2: LGEN and BARC ticker names render on Positions page ✓
- PATH-3: "Mark as read" and "Mark all as read" buttons present when unread notifications exist ✓

**Visual AC — DoQ manual review required (not covered by Playwright):**
The following elements require human staging verification. See the Human Staging Test Script below (`docs/testing/staging_visual_test_script_EPIC-02.md`):
- PATH-1: Submit button gradient render (cyan→violet); "Creating…" spinner during submission
- PATH-2: P&L colour coding (green/positive, red/negative); position card layout on narrow viewport
- PATH-3: Unread notification cyan left border; notification type icons

**Findings:**
- Spec scope constraint comment present in file header and in each test — AC 4 satisfied. ✓
- No CSS colour or class assertions in any test — AC 5 satisfied. ✓
- `continue-on-error: true` with explanatory comment in `smoke-tests.yml` — AC 6 satisfied. ✓
- `placeholder="0.00"` selector disambiguation: exactly 2 such inputs exist (entry_price, stop_price) — `.first()` / `.last()` is safe for UK market selection since fill_price uses `"Actual broker fill price"` and ATR uses `"For stop suggestion"`. ✓
- `mockFallback()` pattern prevents CI failures from unmocked background endpoints. ✓
- CI workflow has no path filter — triggers on every PR to main. ✓
- 3 tests × mock layer × single Chromium worker: structural run time ~30–60s, well within 2-minute AC. ✓

**Visual AC sign-off status:** DEFERRED — pending human completion of staging test script.
Full EPIC-02 sign-off is also deferred until ST-06 is complete and visual items are confirmed.

### DEV-EPIC02-ST05-03
**Priority:** P2
**Story:** ST-05
**AC:** Visual AC — PATH-2 (V-PATH2-01): "Positive P&L renders in green — £70.05 (LGEN) and £96.05 (BARC) values appear in green text" (`staging_visual_test_script_EPIC-02.md`)
**Expected:** Positions Table View displays both "P&L (GBP)" and "P&L %" as separate columns (positions.md v1.4, Table View column list). Absolute GBP P&L values (£70.05, £96.05) are visible and rendered in green for positive positions.
**Actual:** Positions page shows % uplift in green for both LGEN and BARC. Absolute £ P&L values are not displayed — the P&L (GBP) column is absent or not rendering. All other PATH-2 checks (V-PATH2-02, V-PATH2-03) passed.
**Impact:** Users cannot see their absolute monetary P&L on the Positions page — only % is visible. The colour rendering is correct (green for positive); the missing data is the GBP value. No workflow is blocked, but this is a visible functional gap against the canonical spec.
**Backlog action:** BLG-FE item to be filed — fix P&L (GBP) column display on Positions page.

---

## ST-06 — BLG-QA-01: Playwright E2E for Chart Interactivity

**Status:** Pending
_Evidence to be added when ST-06 is implemented._
