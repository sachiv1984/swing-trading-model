Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06

# Delegation Log — 2026-10-06__release-v9.10

## DEL-20261006-01

- **ST Item:** ST-01 — One source for §11 stop parameters across the on-load and nightly stop paths
- **EPIC:** EPIC-01
- **Classification:** delegated_decision (sub-step: production read, Human-Delegation, RISK-01)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1894
- **Branch:** exec/2026-10-06__release-v9.10/EPIC-01
- **Delegated at:** 2026-10-06T15:08:11Z
- **What is needed:** Two read-only queries against **production** (this sandbox's `DATABASE_URL` is staging). (1) `SELECT id, min_hold_days, atr_period, atr_multiplier_initial, atr_multiplier_trailing, updated_at FROM settings;` for ST-01 AC 1. (2) For AC 6, the open positions whose stored stop may already differ from a 5×/2× recompute: `SELECT id, ticker, market, entry_date, entry_price, fill_price, atr, current_stop, initial_stop, active_atr_multiplier, stop_calculated_at FROM positions WHERE status = 'open';`. Paste both outputs back.
- **Spec reference:** `claude/strategy/strategy_rules.md` §11; `stage4_backlog_slice.md#ST-01` AC 1 and AC 6
- **Unblock criteria:** Both outputs recorded in `qa_evidence_EPIC-01.md` under ST-01. If query (1) shows multipliers other than 5/2 or a hold length other than 10, any open position recomputed with those values gets a Product Owner correction decision (AC 6). Under §7.3 a stop is never silently loosened.
- **Commit format required:** `[EPIC-01][ST-01] <description>` pushed to `exec/2026-10-06__release-v9.10/EPIC-01`
- **Status:** Unblocked — 2026-10-06T17:34:46Z. Unblocked in-session: both production query outputs were supplied by the user (human, with production access), in the same session as the delegation. The settings row equals §11 (10/14/5.00/2.00, unchanged since 2026-06-03). None of the 4 open positions (MU, SNDK, WDC, DELL) has a diverged stop, so no AC 6 correction is owed. Recorded in `qa_evidence_EPIC-01.md` §ST-01.

## DEL-20261006-02

- **ST Item:** ST-02 — Remove silent ATR fallbacks and record ATR provenance
- **EPIC:** EPIC-01
- **Classification:** delegated_backend (reclassified from `autonomous` at execution: the code, tests and docs are done, but the DS-25 migration needs live DB write access, as with v9.9 ST-01/DS-22)
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #1895
- **Branch:** exec/2026-10-06__release-v9.10/EPIC-01
- **Delegated at:** 2026-10-06T15:11:24Z
- **What is needed:** Run DS-25's Up Migration (`docs/specs/data_model.md` §DS-25) against **staging, then production**: `ALTER TABLE positions ADD COLUMN IF NOT EXISTS atr_source VARCHAR(10) CHECK (atr_source IN ('fetched', 'user', 'fallback'));`, then its Verification query. This sandbox's `DATABASE_URL` is read-only staging. `add_position()`'s INSERT now names `atr_source`, so EPIC-01 must not deploy before the column exists in each environment.
- **Spec reference:** docs/specs/data_model.md#DS-25
- **Unblock criteria:** The Verification query returns 1 row (`atr_source`, `character varying`, `10`, `YES`) in both environments. Its output is recorded in DS-25's Live Confirmation, and DS-25's status moves from PENDING APPLICATION to applied.
- **Commit format required:** `[EPIC-01][ST-02] <description>` pushed to `exec/2026-10-06__release-v9.10/EPIC-01`
- **Status:** Open

## DEL-20261006-04

- **ST Item:** ST-01 — One source for §11 stop parameters across the on-load and nightly stop paths
- **EPIC:** EPIC-01
- **Classification:** delegated_decision (sub-step: DS-26 migration needs live DB write access)
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #1894
- **Branch:** exec/2026-10-06__release-v9.10/EPIC-01
- **Delegated at:** 2026-10-06T17:30:09Z
- **What is needed:** Run DS-26's Up Migration (`docs/specs/data_model.md` §DS-26) on **staging, then production**: `ALTER TABLE positions ADD COLUMN IF NOT EXISTS stop_calculation_source VARCHAR(10) CHECK (stop_calculation_source IN ('on_load', 'nightly'));`, then its Verification query. Both recompute paths now write this column, so EPIC-01 must not deploy before it exists. It can be run in the same session as DS-25 (`DEL-20261006-02`).
- **Spec reference:** docs/specs/data_model.md#DS-26
- **Unblock criteria:** The Verification query returns 1 row (`stop_calculation_source`, `character varying`, `10`, `YES`) in both environments. Its output is recorded in DS-26's Live Confirmation.
- **Commit format required:** `[EPIC-01][ST-01] <description>` pushed to `exec/2026-10-06__release-v9.10/EPIC-01`
- **Status:** Open
