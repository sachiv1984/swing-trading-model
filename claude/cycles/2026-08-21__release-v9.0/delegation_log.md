Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-21

# Delegation Log — 2026-08-21__release-v9.0

Append-only. Do not edit previous entries.

---

## DEL-20260821-01

- **ST Item:** ST-02 — Configure root/app logging so logger.info() calls actually reach Render's captured logs
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1463
- **Branch:** exec/2026-08-21__release-v9.0/EPIC-01
- **Delegated at:** 2026-08-21T14:22:43Z
- **What is needed:** The code fix (backend/main.py's `logging.basicConfig()` call, commit `186959a4`) is already implemented, tested (`tests/test_root_logging_config.py`), and pushed. Two ACs remain undeliverable from this execution sandbox because they require live Render dashboard/production access this sandbox does not have (no DATABASE_URL/Render credentials present):
  1. Once this branch's PR merges and deploys to production, trigger a real invocation that logs an INFO line (e.g. `si05-weekly-digest.yml`'s `workflow_dispatch`, same as `docs/ops/api_performance_baseline.md` §36.5's methodology) and confirm in the Render dashboard's log viewer that the `"SI-05 digest sent (%d chars) in %.2fs"` line (from `backend/services/si05_digest_service.py`) now actually appears — this is the AC's own required evidence that the fix works in the real deployed environment, not just in this sandbox's isolated-subprocess test.
  2. Update `docs/ops/api_performance_baseline.md` §36 with the real Render-log-derived duration value once obtained, marking the interim GitHub-Actions-proxy measurements (§36.3, §36.5) as superseded. This should also resolve `DEV-EPIC03-ST09-01`'s target condition (already recorded in §36.5 as "superseded once BLG-BE-107 lands and a real Render-log-derived value becomes obtainable").
- **Spec reference:** docs/ops/api_performance_baseline.md §36.5 (root cause finding this story fixes)
- **Unblock criteria:** Render dashboard log viewer confirms the digest-timing line present with a real elapsed-time value after a real post-deploy invocation; §36 updated with that value.
- **Commit format required:** `[EPIC-01][ST-02] <description>` pushed to `exec/2026-08-21__release-v9.0/EPIC-01` (if any further code/doc changes are needed) — the code fix itself is already committed (`186959a4`); this delegation covers only the remaining live-verification and doc-update ACs.
- **Status:** Pending

---

## DEL-20260821-02

- **ST Item:** ST-06 — Audit and backfill open positions against the breakeven-floor stop invariant
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Backend Engineering Patterns Owner (with Infrastructure & Operations Owner for DB access, if a direct connection is preferred over the API path below)
- **GitHub Issue:** #1467
- **Branch:** exec/2026-08-21__release-v9.0/EPIC-02
- **Delegated at:** 2026-08-21T15:00:00Z
- **What is needed:** This entirely requires live production database access this sandbox does not have (no `DATABASE_URL`/production credentials present), and — separately — correcting real open positions' stop values is a high-consequence action on live financial data that should be executed by a human operator regardless of sandbox access. Code-read investigation (this session) narrowed the work to a **verification-first** runbook rather than a build task:

  **Step 1 — BEFORE audit (read-only):**
  ```sql
  SELECT id, ticker, market, entry_price, current_stop, position_state, status
  FROM positions
  WHERE status = 'open'
    AND position_state = 'PROFITABLE'
    AND current_stop < entry_price;
  ```
  Record the row count and the full result set (for the traceability record below) before doing anything else.

  **Step 2 — Correction, only if Step 1 finds any rows:** Per this story's own scope note, do **not** write a bespoke correction script. `backend/services/position_service.py::analyze_positions()` already applies the breakeven-floor logic (`calculate_trailing_stop()`, fixed in commit `b410cfa3c`, 2026-02-12) and persists the corrected `current_stop` to the database — and this function already runs **every night** via `.github/workflows/daily-snapshot.yml`'s `GET /positions/analyze` call. This means any historical stale row should already have self-corrected on the first nightly run after 2026-02-12, *provided* `live_price` was available that night (the DB write is conditional on it — see `position_service.py` around the `if live_price:` block). So Step 1's count is very likely already 0 by ordinary nightly operation — but this must be **confirmed via the live query**, not assumed, which is exactly the gap `BLG-BE-102`'s original AC left open (a live-DB check no CI run can perform). If Step 1 does find rows: either trigger `POST /positions/nightly-stop-update` (`run_nightly_trailing_stop_update()`, same floor logic, immediate) or simply wait for that night's scheduled `GET /positions/analyze` run, then re-run Step 1's query to confirm those specific rows are now corrected.

  **Step 3 — AFTER audit (read-only, re-run Step 1's exact query):** confirm 0 rows (or, if Step 2's correction path was used, confirm the specific rows found in Step 1 no longer match).

  **Step 4 — Record the result:** count found (Step 1), count corrected (0 if Step 1 already returned 0 — record "0 found, correction not required, nightly job already current" as an equally valid, positive outcome, not a failure to find something), and the date — this closes the deferred `BLG-BE-102`/ST-01 (v8.9) AC. Suggested location: a new dated ops note under `docs/ops/` (e.g. `docs/ops/breakeven_floor_stop_audit_<date>.md`) following this repo's existing dated-audit-doc convention (see `docs/ops/render_starter_tier_headroom_reassessment_2026-08-13.md` for header/structure precedent), or appended directly to this delegation log entry's outcome if a human operator prefers a lighter-weight record.
- **Spec reference:** `claude/backlog/backlog.md` BLG-BE-105 (full problem statement and scope); `backend/services/position_service.py::analyze_positions()`/`run_nightly_trailing_stop_update()` (the existing floored calculation path)
- **Unblock criteria:** Step 1 query result recorded; if non-zero, Step 2 correction applied via the existing code path (no bespoke logic) and Step 3 re-verification recorded; Step 4 traceability record written.
- **Commit format required:** `[EPIC-02][ST-06] <description>` pushed to `exec/2026-08-21__release-v9.0/EPIC-02` for the Step 4 traceability record (and any doc file it lives in).
- **Status:** Pending
