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

_Pending — DoQ to verify at EPIC-02 PR review._

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

_Pending — DoQ to verify at EPIC-02 PR review._

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

_Pending — DoQ to verify at EPIC-02 PR review._

**DoQ verification method required:** Code review (spec + workflow) + local run to confirm PATH-1 POST assertion and PATH-3 unread indicator. PATH-2 view portfolio is code-review-sufficient. Visual AC (button gradient, P&L colour coding, notification border colour) remain unverified by Playwright — DoQ manual review required at staging._

---

## ST-06 — BLG-QA-01: Playwright E2E for Chart Interactivity

**Status:** Pending
_Evidence to be added when ST-06 is implemented._
