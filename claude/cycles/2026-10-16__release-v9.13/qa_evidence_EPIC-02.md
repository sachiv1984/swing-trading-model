Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-27 (ST-10 staging manual check recorded, DEL-20261017-01)

# QA Evidence — EPIC-02: Stop, Sizing & Position Data Correctness

**EPIC:** EPIC-02 — Stop, Sizing & Position Data Correctness
**Cycle:** 2026-10-16__release-v9.13
**Branch:** `exec/2026-10-16__release-v9.13/EPIC-02`

The consolidation block and DoQ sign-off block are added at STEP 3.2.A.

## Staging Manual Check — Stop Freshness

Story: ST-10, AC 2 (manual-check half), `DEL-20261017-01`. Method: `docs/specs/metrics_definitions.md` v1.32.0 §Stop Freshness → Manual check.

- **Date:** 2026-10-27
- **Environment:** staging. Both Render services (`trading-assistant-api-staging`, `trading-assistant-staging`) were deployed by the user from `exec/2026-10-16__release-v9.13/EPIC-02` at `826ee17a` (Render branch switch; staging otherwise deploys from `main`). The frontend build needed `DISABLE_ESLINT_PLUGIN=true` on the Render static site, because `eslint-config-react-app` is missing from the lockfile since `2909e67e`; that variable stops build-time linting only and does not change the bundle. Filed as BLG-OPS-193.
- **Checked by:** the user (human, acting for the Infrastructure & Operations Owner), who read the panel and ran the read-only query in the staging Supabase SQL editor.

**System Status panel (As of 08:12, 27 Oct 2026):**

| Field | Shown |
|-------|-------|
| Median stop age | — |
| Oldest stop | — |
| Coverage | 0 of 2 open positions |
| Never recalculated | 2 never recalculated |

**Query output** (`positions WHERE status = 'open'`, ordered `stop_calculated_at NULLS FIRST`):

| ticker | stop_calculated_at | age_hours |
|--------|--------------------|-----------|
| BARC | null | null |
| LGEN | null | null |

**Comparison:** match. The query returns 2 open positions, both with a NULL `stop_calculated_at`. That equals the panel's coverage (0 recalculated of 2) and "2 never recalculated". With no non-NULL row there is no median or maximum age and no oldest ticker, so the panel's "—" for median and oldest is the defined empty value. NULL rows do not depend on when they are read, so the gap between the panel read and the query does not matter.

**Note:** this check confirms the panel and the database agree. It does not show a non-empty median or oldest on a deployed environment; those formatted values are covered by Playwright SC-SS-09a and `tests/test_stop_freshness_service.py`. The two NULLs mean neither stop-recalculation path has stamped these positions on staging: the on-load path skips positions in their grace period, and the scheduled nightly update (`nightly-stop-update.yml`) calls the `API_URL` secret, not `STAGING_API_URL`.

**Result:** Pass. `DEL-20261017-01` sign-off cleared.
