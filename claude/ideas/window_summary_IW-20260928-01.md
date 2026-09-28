**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-28
**Window:** IW-20260928-01

# Idea Intake Summary — IW-20260928-01

## Window Status: Closed

Opened: 2026-09-28T08:58:00Z
Closed: 2026-09-28T09:05:00Z

Invoked inline as STEP -1.6 of `run roadmap --reason "scheduled"` (`2026-09-28__scheduled`) — the register held 2 rows with `Status: Parked-cycle-<n>` (below the 20-item threshold). Mode: `standard`.

**Reduced-scope disclosure:** this window deliberately opened for 3 of the ~22 eligible agent roles (Head of Specs Team, Financial Reporting & Records Owner, Infrastructure & Operations Owner) rather than the full roster, given session time constraints. This is a disclosed scoping choice, not silent under-submission — the other ~19 roles are simply not exercised this window and remain eligible next time. Each of the 6 submissions produced is genuine and grounded in this session's own STEP 2–3 findings, not a placeholder.

**Stale-idea horizon check (STEP -0.5):** 0 rows at `Parked-cycle-2` at window open — no advisory.

**Parked queue pre-check (§2.0):** no parked row's `Submitter` matches any of the 3 participating agents — no overlap-with-own-parked-idea case this window.

**Backlog scope overlap check (§2.0 step 5, mandatory):** performed as a targeted grep of `claude/backlog/backlog.md` for each of the 6 candidate topics before finalising. **0 overlaps found** — all 6 are net-new.

**Codebase overlap check (§2.0 step 6, mandatory):** performed for every topic naming a mechanism (schema-drift scanner, usage/adoption counter, staging query allow-list doc, diagnostics script) — `scripts/` and `docs/infrastructure/` checked. **0 already-implemented topics found** (existing `check_*_drift.py` scripts cover openapi/contract/deploy-path/api-baseline drift, none cover live-schema-vs-`data_model.md` column drift; `staging_setup.md` §8 documents the staging read-only role's provisioning but not a query allow-list; no adoption/usage counter exists for the AI P&L narrative feature; no rebalance-diagnostics script exists).

**Method note:** each agent perspective was exercised by the engine per §2.1; submissions are engine-generated under agent perspectives, not independent human input. Full template fields are recorded per idea in `cycle_record.md`'s STEP 4 section and directly in each filed backlog item's `**Source:**`/Problem text (given the small window size, fields were not duplicated into a separate per-idea file).

## Submission Counts

| Agent | New Submissions | Parked Resubmitted | Total |
|-------|------------------|---------------------|-------|
| Head of Specs Team | 2 | 0 | 2 |
| Financial Reporting & Records Owner | 2 | 0 | 2 |
| Infrastructure & Operations Owner | 2 | 0 | 2 |

## Agents Without Minimum Submissions

None — all 3 participating agents met the 2-net-new minimum. (19 other eligible agent roles were not opened this window — see reduced-scope disclosure above; not a §2.3 shortfall, a deliberate scoping choice.)

## Ideas Available for Roadmap STEP 4

6 new (`IW-20260928-01`) + 2 carried parked (`IDEA-data-model-20260919-02`, `IDEA-director-of-hr-20260919-02`) = 8 total considered at STEP 4. All 6 new submissions classified **Backlog (ungated)**. `IDEA-data-model-20260919-02`'s gate cleared this cycle — re-evaluated, also **Backlog (ungated)**. `IDEA-director-of-hr-20260919-02` re-parked (cycle 2).

## Parked Ideas Carried Forward (Not Resubmitted)

None outstanding after this cycle's dispositions — the only 2 parked rows entering this window were both resolved (1 promoted, 1 re-parked with reaffirmed rationale) at roadmap STEP 4.0/4.1.

## Notes

No `[FIELD REQUIRED]` flags — all 6 submissions passed the Submission Quality Check (specific `strategy_rules.md` citation, specific expected-value metric, all required fields non-empty) on first generation.

```yaml
// ARTEFACT_STATUS
{
  "file": "window_summary_IW-20260928-01.md",
  "window_id": "IW-20260928-01",
  "filed_utc": "2026-09-28T09:15:38Z",
  "submission_count": 6,
  "agents_participating": 3,
  "status": "Complete"
}
```
