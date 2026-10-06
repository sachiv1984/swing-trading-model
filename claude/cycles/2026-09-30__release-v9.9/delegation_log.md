Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-01

# Delegation Log — 2026-09-30__release-v9.9

## DEL-20261001-01

- **ST Item:** ST-01 — Consolidate 4 duplicate ATR implementations; persist stop/ATR recalculation timestamp; expose atr/multiplier/timestamp on GET /positions
- **EPIC:** EPIC-01
- **Classification:** delegated_decision (sub-step: live DB write access required to complete)
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #1849
- **Branch:** exec/2026-09-30__release-v9.9/EPIC-01
- **Delegated at:** 2026-10-01T11:30:00Z
- **What is needed:** Run DS-22's Up Migration (`docs/specs/data_model.md` §DS-22) against the live staging `positions` table: `ALTER TABLE positions ADD COLUMN IF NOT EXISTS stop_calculated_at TIMESTAMPTZ, ADD COLUMN IF NOT EXISTS atr_calculated_at TIMESTAMPTZ, ADD COLUMN IF NOT EXISTS active_atr_multiplier DECIMAL(4, 2);`. This sandbox's `DATABASE_URL` is `readonly_staging` (SELECT only) — `ALTER TABLE` was attempted and rejected with `InsufficientPrivilege: must be owner of table positions`. All application code (position_service.py, GET /positions, position_endpoints.md, openapi.yaml) is written assuming these 3 columns exist; it will raise a real DB error on first recompute until the migration is applied.
- **Spec reference:** docs/specs/data_model.md#DS-22
- **Unblock criteria:** Migration applied to staging; verification query (DS-22) confirms all 3 columns present (2 nullable TIMESTAMPTZ, 1 nullable DECIMAL(4,2)). Update DS-22's sign-off block from "pending" to "Confirmed applied" with the verification output once run.
- **Commit format required:** `[EPIC-01][ST-01] <description>` pushed to `exec/2026-09-30__release-v9.9/EPIC-01`
- **Status:** Unblocked — 2026-10-01T12:29:32Z. Data Model & Domain Schema Owner ran the migration against both staging and production directly; verification output pasted back and independently re-confirmed by this session against staging. See `data_model.md` §DS-22 Live Confirmation.

## DEL-20261001-02

- **ST Item:** ST-29 — Drop 4 confirmed-orphaned, always-NULL columns from the live positions table
- **EPIC:** EPIC-05
- **Classification:** delegated_backend
- **Assigned to:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **GitHub Issue:** #1877
- **Branch:** exec/2026-09-30__release-v9.9/EPIC-05
- **Delegated at:** 2026-10-01T15:25:04Z
- **What is needed:** Run `ALTER TABLE positions DROP COLUMN IF EXISTS atr_value, DROP COLUMN IF EXISTS stop_price, DROP COLUMN IF EXISTS fees, DROP COLUMN IF EXISTS pnl_percent;` against the live `positions` table (staging, then production once confirmed). Disposition was already recommended at v9.7 (`data_model.md` §"4 orphaned, always-NULL, undocumented live columns", ST-25/BLG-SPEC-150) — confirmed via static grep that no read or write path in `backend/` references any of the 4 column names. This sandbox's `DATABASE_URL` is `readonly_staging` (SELECT only) — no write access exists here to apply the drop.
- **Spec reference:** docs/specs/data_model.md §"4 orphaned, always-NULL, undocumented live columns" (BLG-SPEC-150/BLG-SPEC-164)
- **Unblock criteria:** Columns dropped on staging (then production); a verification query (`SELECT column_name FROM information_schema.columns WHERE table_name = 'positions' AND column_name IN ('atr_value','stop_price','fees','pnl_percent');` returns 0 rows) confirms. Add a new Migration History entry to `data_model.md` recording the drop.
- **Commit format required:** `[EPIC-05][ST-29] <description>` pushed to `exec/2026-09-30__release-v9.9/EPIC-05`
- **Status:** Unblocked — 2026-10-05T12:45:37Z. Unblocked in-session — the user (human, with live write access, acting for the Data Model & Domain Schema Owner) ran the NULL pre-check (staging 2/2 rows, production 27/27 all NULL), the drop and the verification query (0 rows) on staging then production, same session as the walkthrough. Sign-off cleared; commit `bd89ed49` records it as `data_model.md` DS-24.

## DEL-20261001-03

- **ST Item:** ST-30 — Reconcile positions.fees_paid NOT NULL constraint (re-apply live, or confirm nullable is intentional)
- **EPIC:** EPIC-05
- **Classification:** delegated_backend
- **Assigned to:** Data Model & Domain Schema Owner
- **GitHub Issue:** #1878
- **Branch:** exec/2026-09-30__release-v9.9/EPIC-05
- **Delegated at:** 2026-10-01T15:25:04Z
- **What is needed:** A binding disposition on `positions.fees_paid`'s nullability — the live column has been nullable since at least v9.7 (`data_model.md` §"fees_paid nullability reconciled to nullable", ST-26/BLG-SPEC-151), which only reconciled the *documentation* to match live state without deciding whether that drift from the original v1.6 `NOT NULL` intent should be accepted going forward or reversed. Two valid outcomes: (a) re-apply `ALTER TABLE positions ALTER COLUMN fees_paid SET NOT NULL` live (requires confirming no existing row has a NULL `fees_paid` first), or (b) formally confirm nullable is the intentional, permanent disposition with a stated reason (e.g. historical rows predating fee tracking). This is a data-model decision, not inferable from the drift alone.
- **Spec reference:** docs/specs/data_model.md §"fees_paid nullability reconciled to nullable" (BLG-SPEC-151/BLG-SPEC-165)
- **Unblock criteria:** Disposition recorded in `data_model.md` with the stated reason either way; if re-applying `NOT NULL`, the live schema and `data_model.md` must agree after the `ALTER TABLE` runs (pre-checked for 0 violating rows).
- **Commit format required:** `[EPIC-05][ST-30] <description>` pushed to `exec/2026-09-30__release-v9.9/EPIC-05`
- **Status:** Unblocked — 2026-10-05T12:55:48Z. Unblocked in-session — the user (human, with live write access, acting for the Data Model & Domain Schema Owner) ran DS-23's pre-check (0/0 NULL rows in both environments), `SET NOT NULL` and verification (`is_nullable = NO`, `column_default = NULL`) on staging then production, same session as the walkthrough. Both environments had no column default (documented `DEFAULT 0` was wrong); Product Owner chose no default. Sign-off cleared; commit `425dcd89` records it as `data_model.md` DS-23 Live Confirmation.
