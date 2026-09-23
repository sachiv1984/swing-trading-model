**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved — Correction & Carry-Forward
**Cycle:** 2026-09-23__release-v9.7
**Story:** ST-03 (EPIC-02, BLG-FE-187)
**Supersedes (data contract only):** `docs/design/2026-09-21__release-v9.6/monthly-pnl-fees-not-recorded/decision_record.md` §2.4

# Decision Record — Monthly P&L NULL-Fee Frontend Surfacing (Field-Name Correction)

## 1. Problem

`BLG-FR-04`'s (v9.6, ST-07) design record specified an additive API shape of `fees_missing_count` (per month) and a top-level `fees_missing_total`. The backend that actually shipped (`backend/database.py` `get_monthly_pnl()`, `backend/services/reports_service.py` `get_monthly_pnl_report()`) instead returns `null_fee_trade_count` per month and **no top-level aggregate field at all**. The canonical API contract (`docs/specs/api_contracts/reports_endpoints.md` v0.13) already documents the real shape correctly. `reports.md` (the frontend page spec) was never corrected to match — it still references `fees_missing_count`/`fees_missing_total` (§Fees-Not-Recorded Visibility, v0.18). `BLG-FE-187` is the frontend-surfacing story; building against the spec's stale field names would build against a response shape that does not exist.

## 2. Decision

### 2.1 Field names corrected

Every reference to `fees_missing_count` in `reports.md` is corrected to `null_fee_trade_count`, matching `reports_endpoints.md` v0.13 and the live backend.

### 2.2 Aggregate notice — derived client-side, not a new backend field

No top-level aggregate field exists or is being added. The aggregate notice's `N` is the **sum of `null_fee_trade_count` across all months currently loaded in the table**, computed client-side from already-fetched row values — the same convention already established for the Monthly Financial Table's "Avg P&L/Trade" column (`reports.md` §Monthly Financial Table: "Client-side display arithmetic on already-fetched row values, not a P&L recalculation"). This is not a scope reduction from the AC (`ST-03`'s AC only requires the per-month indicator); it is a correction that keeps the v9.6-approved aggregate-notice UX intact without inventing a backend field this story does not otherwise need.

### 2.3 Per-month indicator and basis caption — unchanged in substance

§2.2 and §2.3 of the v9.6 decision record (per-month `"{trade_count} · {k} no fees"` indicator; the mandatory net/gross basis caption) are unchanged except for the field-name correction in 2.1. `ST-03`'s AC is satisfied by the per-month indicator alone; the aggregate notice and basis caption remain part of the already-approved UX and are not re-litigated here.

### 2.4 CSV — unchanged

Confirmed unchanged: `reports_endpoints.md` v0.13 explicitly states the audit/snapshot fields are JSON-only, excluded from the CSV byte shape.

## 3. §13 Compliance

Reports counts about existing data. No AI call, no recommendation. §13 pre-check does not apply (same determination as the v9.6 original).

## 4. Frontend Spec Impact

`reports.md` v0.18 → v0.19: §Fees-Not-Recorded Visibility corrected to `null_fee_trade_count`; aggregate notice documented as a client-side sum, not a backend field.

## 5. Testability (CLAUDE.md §2)

Playwright with a mocked `monthly-pnl` response using the real field name `null_fee_trade_count`: aggregate notice shows the correct summed count across loaded months; per-month indicator matches the existing v9.6 AC; a month with `null_fee_trade_count = 0` renders unchanged.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-23 — correction only; no UX change from what was already approved at v9.6.
Product Owner: confirmed, 2026-09-23.
