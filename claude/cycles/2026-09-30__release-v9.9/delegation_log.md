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
