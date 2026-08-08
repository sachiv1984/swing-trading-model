**Owner:** Metrics Definitions & Analytics Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-08
**Cycle:** 2026-08-07__release-v8.4 (ST-28 — BLG-QA-70)

---

# BLG-BE-40 Impact Measurement — Findings

## 1. Background

`BLG-BE-40` (v6.4, commit `4d56dc42`, 2026-07-02) fixed `signal_service.generate_momentum_signals()` to source its ticker scan universe from `services.ticker_universe_service.get_all_tickers(active_only=True)` instead of the deprecated `database.get_all_tickers()` (the `tickers` table). This is a **scan-universe-membership** fix — it does not change the `suggested_shares` sizing formula for any ticker eligible under either source. The only possible impact is signals that were generated, before the fix, for tickers present in the deprecated `tickers` table but **not** in the current active `ticker_universe` — those scans should not have happened under the corrected logic at all.

This item runs the impact measurement query (`docs/ops/blg_be_40_impact_measurement_query.sql`) against production to identify the count and magnitude of any such affected signals, per the story's own scope: informational only, no remediation implied unless a material discrepancy is found.

## 2. Method

Query run directly against production Postgres by the Infrastructure & Operations Owner (user), in-session, 2026-08-08. Cutoff timestamp used: `2026-07-02 08:31:07` (commit `4d56dc42`'s authored timestamp — used as-is; no more precise deploy timestamp was available or flagged as materially different).

## 3. Results

| Query | Result |
|-------|--------|
| Step 1 — affected signal rows (tickers not in active `ticker_universe`, `created_at` before the fix) | **0 rows returned** |
| Step 3 — total pre-fix signals in the same window | **300** |
| Step 3 — affected pre-fix signals | **0** |

**0 of 300 pre-fix signals were affected.** This is a genuine, non-vacuous zero: 300 signals existed in the pre-fix window to potentially be affected, and none of them were generated for a ticker outside the current active `ticker_universe`.

## 4. Interpretation

Per this story's own scope ("informational — no remediation implied unless a material discrepancy is found"): **no material discrepancy was found.** The practical explanation is that the deprecated `tickers` table and the current active `ticker_universe` set had substantial or complete overlap for the tickers actually scanned during the pre-fix window — i.e. the bug was real (wrong source table) but did not, in practice, cause the scan universe to differ meaningfully from what the corrected logic would have produced, at least not for any ticker that actually generated a signal in this window.

**No `status='entered'`/`'already_held'` review is needed** — there is no affected population to check for trading impact in the first place.

## 5. Conclusion

No remediation action is required. This closes the open question `BLG-BE-40`'s fix left unmeasured (how many historical `suggested_shares` values, if any, were affected by the deprecated-table bug) with a clean, verified answer: none.

---

## Review

**Reviewed by (agent-mediated, on behalf of Metrics Definitions & Analytics Owner):** Query methodology confirmed sound — the affected-population definition (pre-fix signal, ticker absent from active `ticker_universe`) correctly isolates the actual behavioural difference the `BLG-BE-40` fix introduced (scan membership), not a spurious wider population. The zero-result is corroborated by a non-zero denominator (300 pre-fix signals), ruling out a vacuous "empty table" false negative. No further metrics-definition concern.

- Signed off by: Sprint Execution Engine (agent-mediated, Metrics Definitions & Analytics Owner role — §5.3)
- Date: 2026-08-08
- Comments: Query results supplied directly by a human (Infrastructure & Operations Owner) with production DB access; the query design and its interpretation are code/data-review-verifiable.

**Reviewed by (Product Owner — human):** Accepted — zero remediation needed, closes `BLG-QA-70` as informational-only per the story's own scope.

- Signed off by: Product Owner
- Date: 2026-08-08
- Comments: Confirmed directly in-session — 0 of 300 pre-fix signals affected is a genuine, non-vacuous zero-impact result. No further action required.
