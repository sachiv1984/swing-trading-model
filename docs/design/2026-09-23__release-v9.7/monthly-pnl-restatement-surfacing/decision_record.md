**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved — Correction & Carry-Forward
**Cycle:** 2026-09-23__release-v9.7
**Story:** ST-04 (EPIC-02, BLG-FE-188)
**Supersedes (data contract only):** `docs/design/2026-09-21__release-v9.6/monthly-pnl-restatement-diff/decision_record.md` §2.7

# Decision Record — Monthly P&L Restatement Diff Frontend Surfacing (Field-Name Correction)

## 1. Problem

`BLG-FR-05`'s (v9.6, ST-08) design record specified a nested per-month `restatement` object (`snapshot_date`, snapshot/live `realised_pnl_gbp`/`trade_count`) present only when they differ. The backend that actually shipped (`backend/services/reports_service.py` `_snapshot_month()`/`get_monthly_pnl_report()`) instead returns **flat** per-month fields — `snapshotted`, `restated`, `snapshot_realised_pnl_gbp`, `restated_diff_gbp` — always present (not gated on differing), with no nested object and **no snapshot `trade_count` field at all**. The canonical API contract (`reports_endpoints.md` v0.13) documents this real, flat shape correctly. `reports.md`'s §Monthly Restatement Marker (v0.18) still describes the nested `restatement` object and a two-metric (Realised P&L + Trades) detail row that the live data cannot fully populate. `BLG-FE-188` is the frontend-surfacing story; it must build against the shape that exists.

## 2. Decision

### 2.1 Field names corrected

Every reference to the nested `restatement` object in `reports.md` is corrected to the flat fields: `snapshotted`, `restated`, `snapshot_realised_pnl_gbp`, `restated_diff_gbp` — matching `reports_endpoints.md` v0.13 and the live backend. The marker shows when `restated = true` (not "when a `restatement` object is present").

### 2.2 Detail row reduced to Realised P&L only

The original design's detail row specified two metrics (Realised P&L and Trades), each with a snapshot value. The live API returns a snapshot value only for Realised P&L (`snapshot_realised_pnl_gbp`) — there is no `snapshot_trade_count` or equivalent field, so a "Trades: as-reviewed vs now" row cannot be populated. The detail row is corrected to show **Realised P&L only**: As reviewed (`snapshot_realised_pnl_gbp`) | Now (`realised_pnl_gbp`) | Change (`restated_diff_gbp`).

### 2.3 Trade-count-only restatement edge case

`restated` can be `true` while `restated_diff_gbp = 0.00` — this happens when only the month's trade count changed (e.g. a trade was added or removed) without moving the realised P&L total. Per 2.2, the single Realised P&L row would otherwise read as "Restated, £0.00 change," which understates that something changed. The detail row adds a muted line beneath the Realised P&L metric, shown **only when** `restated_diff_gbp = 0` and the marker is showing: `"Trade count for this month has also changed since it was reviewed."` No exact before/after count is shown (no snapshot trade-count field exists to show it against).

### 2.4 Tax Year notice — unchanged

`summary.restated_month_count` / the Tax Year Summary Bar notice (§Summary Bar) already matches the live API exactly — no correction needed there.

### 2.5 Exports — unchanged

Confirmed unchanged: `reports_endpoints.md` v0.13 states the audit/snapshot fields are JSON-only, excluded from CSV.

## 3. §13 Compliance

A record-integrity display over the user's own realised figures. No AI call, no recommendation. §13 pre-check does not apply (same determination as the v9.6 original).

## 4. Frontend Spec Impact

`reports.md` v0.18 → v0.19: §Monthly Restatement Marker corrected to the flat field set; detail row reduced to Realised P&L with the trade-count-only-change fallback line from §2.3.

## 5. Testability (CLAUDE.md §2)

Playwright with a mocked `monthly-pnl` response using the real field names: marker shown when `restated = true`; detail row shows the correct snapshot/live/change values; the trade-count-only fallback line appears when `restated = true` and `restated_diff_gbp = 0`, and does not appear otherwise; failure fallback line unchanged from v9.6.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-23 — the §2.3 fallback line is a genuine (small) new UX decision closing a gap the field-name correction surfaced; everything else is correction only.
Product Owner: confirmed, 2026-09-23.
