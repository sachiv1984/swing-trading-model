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

**Status:** Pending (unblocked by ST-03)
_Evidence to be added when ST-04 is implemented._

---

## ST-05 — BLG-QA-05: Critical-Path Smoke Test (Playwright)

**Status:** Pending (blocked on ST-03 + ST-04)
_Evidence to be added when ST-05 is implemented._

---

## ST-06 — BLG-QA-01: Playwright E2E for Chart Interactivity

**Status:** Pending
_Evidence to be added when ST-06 is implemented._
