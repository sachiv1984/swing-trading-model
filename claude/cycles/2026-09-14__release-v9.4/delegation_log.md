Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-14

---

# Delegation Log — 2026-09-14__release-v9.4

Append-only. Do not edit previous entries.

---

## DEL-20260914-01

- **ST Item:** ST-01 — DB-level unique constraint on (ticker, entry_date) for open positions
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #1634
- **Branch:** exec/2026-09-14__release-v9.4/EPIC-01
- **Delegated at:** 2026-09-14T13:52:00Z
- **What is needed:**
  A migration adding a DB-level unique constraint on `(ticker, entry_date)` scoped to open positions (`positions.status = 'open'`), per `BLG-BE-115`. Per RISK-01 (no `DATABASE_URL` in this execution environment), the migration script must include its own duplicate pre-check that fails loudly with an offending-rows report — it cannot rely on a separate manual pre-check against a live DB. Draft below is ready to apply/adjust and land in `docs/specs/data_model.md` as the next `## DS-17` entry (current highest is `DS-16`, footer version `2.31` — note: `2.32` after this session's ST-02 commit, non-schema; this migration would be the first real schema-version bump since then):

  ```sql
  BEGIN;

  -- Pre-check (RISK-01): fail loudly, with the offending rows listed, if any
  -- existing open-position (ticker, entry_date) group already has >1 row —
  -- do not apply the constraint over live duplicate data.
  DO $$
  DECLARE
      dup_count INTEGER;
      dup_report TEXT;
  BEGIN
      SELECT COUNT(*) INTO dup_count
      FROM (
          SELECT ticker, entry_date
          FROM positions
          WHERE status = 'open'
          GROUP BY ticker, entry_date
          HAVING COUNT(*) > 1
      ) dups;

      IF dup_count > 0 THEN
          SELECT string_agg(format('  - %s / %s (%s rows)', ticker, entry_date, cnt), E'\n')
          INTO dup_report
          FROM (
              SELECT ticker, entry_date, COUNT(*) AS cnt
              FROM positions
              WHERE status = 'open'
              GROUP BY ticker, entry_date
              HAVING COUNT(*) > 1
          ) t;

          RAISE EXCEPTION E'DS-17 migration aborted: % existing open-position duplicate (ticker, entry_date) group(s) found -- resolve before applying this constraint:\n%', dup_count, dup_report;
      END IF;
  END $$;

  CREATE UNIQUE INDEX IF NOT EXISTS idx_positions_open_ticker_entry_date_unique
      ON positions (ticker, entry_date)
      WHERE status = 'open';

  COMMIT;
  ```

  **Open question for Head of Engineering to confirm, not resolved here:** `BLG-BE-115`'s AC and ST-01's own AC both literally scope the constraint to `(ticker, entry_date)` only, with no `portfolio_id`. The schema supports multiple portfolios (`positions.portfolio_id` FK). If two portfolios can legitimately hold the same ticker opened on the same date as two independent open positions, a bare `(ticker, entry_date)` partial unique index would incorrectly reject the second one. Confirm whether the constraint should be scoped per-portfolio (`(portfolio_id, ticker, entry_date)`) before applying — this repo currently operates single-user/effectively-single-portfolio in practice, but the schema does not enforce that, so this should be a deliberate confirmation, not an assumption baked silently into the migration.

  A synthetic/staging-shaped verification (not against production data) should also be run before landing — e.g. a `tests/` fixture inserting a duplicate open-position pair and asserting both the pre-check `DO` block and the unique index reject it — since AC-03 (live-DB duplicate pre-check against production-shaped data) is this story's staging-only AC per `sprint_backlog.md`: `DATABASE_URL` is unavailable in this execution environment, so the live step must be disclosed as pending, not claimed complete, once this lands.

- **Spec reference:** `docs/specs/data_model.md` — `positions` table definition (§"Database Overview" → positions `CREATE TABLE` block, currently lines 59–98); land as new `## DS-17` entry following the existing DS-12/DS-13 style (migration block, field/rationale prose, Up Migration, Verification query, Sign-off)
- **Unblock criteria:** Migration script finalised (portfolio_id question resolved), verified against synthetic/staging-shaped data (not production — `DATABASE_URL` unavailable in this environment), landed in `docs/specs/data_model.md` as `## DS-17` with Data Model & Domain Schema Owner sign-off, committed and pushed to `exec/2026-09-14__release-v9.4/EPIC-01` with commit message `[EPIC-01][ST-01] <description>`. AC-03's live-production pre-check remains explicitly disclosed as pending per RISK-01 until a session with `DATABASE_URL` access can run it — that disclosure itself, not a fabricated live confirmation, satisfies the sprint-sealed staging-only AC framing for this item.
- **Commit format required:** `[EPIC-01][ST-01] <description>` pushed to `exec/2026-09-14__release-v9.4/EPIC-01`
- **Status:** Unblocked — sign-off cleared (Head of Engineering resolved portfolio_id scoping and finalised the migration; Data Model & Domain Schema Owner agent-mediated Approved after 1 Blocked retry — see DS-17 sign-off block in `data_model.md`). Commit: `13597aedce2c309e5383a5c49974250ee0b4a4bd` (`[EPIC-01][ST-01] Land DS-17...`), pushed 2026-09-14T14:08:01Z.
