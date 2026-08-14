Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-14

# Delegation Log — 2026-08-14__release-v8.8

## DEL-20260814-01

- **ST Item:** ST-03 — Investigate nightly backtest import failure (Strategy Benchmark "data as of" line never populates)
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1395
- **Branch:** exec/2026-08-14__release-v8.8/EPIC-01
- **Delegated at:** 2026-08-14T19:00:00Z
- **What is needed:** Review the next scheduled `.github/workflows/backtest.yml` run's Actions log and the corresponding Render backend log to identify why `backtest_trades.imported_at` never advances. Confirm root cause (workflow failure, silent no-op, or import-path bug), apply the fix at the identified layer (workflow config / router / service / database, per what the log review finds), then confirm on the next scheduled run that `backtest_trades.imported_at` reflects a current timestamp and the "Benchmark data as of ..." line renders on the Strategy Benchmark page with a recent date.
- **Spec reference:** No governing canonical spec — this is a live-environment root-cause investigation (RISK-01 per `sprint_backlog.md`); acceptance criteria per `stage4_backlog_slice.md#ST-03`.
- **Unblock criteria:** A commit tagged `[EPIC-01][ST-03]` pushed to `exec/2026-08-14__release-v8.8/EPIC-01` containing the fix, with the next scheduled `backtest.yml` run confirmed producing a current `imported_at` timestamp and the Strategy Benchmark page showing a recent "data as of" date.
- **Commit format required:** `[EPIC-01][ST-03] <description>` pushed to `exec/2026-08-14__release-v8.8/EPIC-01`
- **Status:** Pending

---

## DEL-20260814-02

- **ST Item:** ST-04 — Add remaining pre-v4.6 endpoint (GET /v1beta1/news) to api_performance_baseline.md
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1396
- **Branch:** exec/2026-08-14__release-v8.8/EPIC-01
- **Delegated at:** 2026-08-14T19:00:00Z
- **What is needed:** Run a live p50/p95 latency measurement for `GET /v1beta1/news` against staging (≥5 samples, same methodology as existing `docs/ops/api_performance_baseline.md` rows), re-confirming the endpoint's correct canonical path/shape post `BLG-SPEC-116`, then add the registration entry to `docs/ops/api_performance_baseline.md` following the most recent `## N. vX.Y Endpoint Registration` section's format.
- **Spec reference:** `docs/ops/api_performance_baseline.md` (living operational document — canonical measurement methodology per §32/§37 precedent).
- **Unblock criteria:** A commit tagged `[EPIC-01][ST-04]` pushed to `exec/2026-08-14__release-v8.8/EPIC-01` adding the endpoint's p50/p95 row with real staging-measured values.
- **Commit format required:** `[EPIC-01][ST-04] <description>` pushed to `exec/2026-08-14__release-v8.8/EPIC-01`
- **Status:** Pending

---

## DEL-20260814-03

- **ST Item:** ST-05 — Add GET /trade-plans/tags to api_performance_baseline.md
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1397
- **Branch:** exec/2026-08-14__release-v8.8/EPIC-01
- **Delegated at:** 2026-08-14T19:00:00Z
- **What is needed:** Run a live p50/p95/max latency measurement for `GET /trade-plans/tags` against staging (≥5 samples, same methodology as existing baseline rows), then add the registration entry to `docs/ops/api_performance_baseline.md`.
- **Spec reference:** `docs/ops/api_performance_baseline.md` (living operational document).
- **Unblock criteria:** A commit tagged `[EPIC-01][ST-05]` pushed to `exec/2026-08-14__release-v8.8/EPIC-01` adding the endpoint's p50/p95/max row with real staging-measured values.
- **Commit format required:** `[EPIC-01][ST-05] <description>` pushed to `exec/2026-08-14__release-v8.8/EPIC-01`
- **Status:** Pending

---

## DEL-20260814-04

- **ST Item:** ST-06 — Live timing measurement for GET /analytics/strategy-version-comparison in api_performance_baseline.md
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1398
- **Branch:** exec/2026-08-14__release-v8.8/EPIC-01
- **Delegated at:** 2026-08-14T19:00:00Z
- **What is needed:** `docs/ops/api_performance_baseline.md` §34 already has a `GET /analytics/strategy-version-comparison` row marked "Pending live timing run" with estimated values (added v8.4). Run ≥5 live staging samples and replace the estimated p50/p95 with measured values in the existing §34 row.
- **Spec reference:** `docs/ops/api_performance_baseline.md` §34 (existing row to be updated, not created).
- **Unblock criteria:** A commit tagged `[EPIC-01][ST-06]` pushed to `exec/2026-08-14__release-v8.8/EPIC-01` replacing §34's estimated values with real staging-measured p50/p95.
- **Commit format required:** `[EPIC-01][ST-06] <description>` pushed to `exec/2026-08-14__release-v8.8/EPIC-01`
- **Status:** Pending

---
