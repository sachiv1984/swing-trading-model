Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-20

# Delegation Log — 2026-11-18__release-v9.18

## DEL-20261120-01

- **ST Item:** ST-40 — Decide whether the debrief may say more than one restating sentence
- **EPIC:** EPIC-07
- **Classification:** delegated_decision
- **Assigned to:** Infrastructure & Operations Owner; AI Compliance & Governance Officer (Human-Delegation named at the sprint backlog seal)
- **GitHub Issue:** #2305
- **Branch:** exec/2026-11-18__release-v9.18/EPIC-07
- **Delegated at:** 2026-11-20T08:49:02Z
- **What is needed:** a sample of real production post-trade debriefs generated since BLG-BE-152 shipped (v9.11, 2026-10-12), so the ST-40 keep-or-amend decision is made against current output. For each debrief: the plan-vs-reality summary, the focus-area sentence (or its absence), and `compliance_check_result` from `trade_debriefs`. About 10 debriefs, including at least a few trades that went to plan, is enough. Paste them in session or supply an export. The execution environment can reach only the staging database (`DATABASE_URL`), so the engine cannot read production.
- **Workflow-viability pre-check (LL-v9.10-P3-01):** not applicable; no GitHub Actions workflow is involved.
- **Unblock criteria:** the sample is supplied (in session or as a file), or the owners confirm it is not available in-sprint, in which case ST-40 AC 1 is `post-merge` and BLG-GOV-378 stays open (sealed `sprint_backlog.md` ST-40 Staging-only ACs).
- **Commit format required:** `[EPIC-07][ST-40] <description>` pushed to `exec/2026-11-18__release-v9.18/EPIC-07`
- **Status:** Unblocked — unblocked in-session: sample supplied by the user (AI Compliance & Governance Officer), same session as delegation, 2026-11-20T14:14:19Z. Production held 2 v1.0 debriefs and no trade had closed since 2026-10-12, so the user generated 10 v1.1 debriefs on older closed trades and pasted them. Sign-off cleared on ESC-EXEC-20261120-02; commit SHA: see ST-40 `commit_sha` in execution_state.json.

## DEL-20261124-01

- **ST Item:** ST-32 — Finish the on-demand Yahoo failure diagnosis (remainder)
- **EPIC:** EPIC-06
- **Classification:** delegated_backend (Human-Delegation named at the sprint backlog seal: production weekly report)
- **Assigned to:** Infrastructure & Operations Owner (the user)
- **GitHub Issue:** #2297
- **Branch:** exec/2026-11-18__release-v9.18/EPIC-06
- **Delegated at:** 2026-11-24T09:42:13Z
- **What is needed:** one production weekly report from after PR #2259 (merged 2026-11-13T15:11:51Z): `GET /ops/api-call-attribution?window=weekly` on production, or the per-feature on-demand Yahoo calls and failures from it (earnings badge, gap-risk, positions prices, research), for a week ending on or after 2026-11-20. The engine can reach only staging. With it, the engine records AC 2 (each feature below 10% failures, or the rest documented as expected) and AC 3 (`docs/ops/data_pipeline_cost_baseline.md` §4 re-recorded).
- **Workflow-viability pre-check (LL-v9.10-P3-01):** the report is supplied by hand, so no workflow is needed. Related: `market-data-volume-check.yml` (the scheduled reader of the same report) has no success in its last 10 runs. Both runs (43925655395, 2026-11-16; 45254364709, 2026-11-23) failed with a 60 s read timeout on the production report call; filed as BLG-OPS-223.
- **Unblock criteria:** the report is pasted in session or supplied as a file; or the owner confirms it is not available in-sprint, in which case ST-32 returns to backlog at sprint close (sealed plan: conditional, §1.4b; BLG-OPS-217 stays open).
- **Commit format required:** `[EPIC-06][ST-32] <description>` pushed to `exec/2026-11-18__release-v9.18/EPIC-06`
- **Status:** Unblocked — unblocked in-session: the user (Infrastructure & Operations Owner) supplied the production weekly attribution report and a production `api_call_log` read of `GET /positions` Yahoo calls, same session as delegation, 2026-11-24. Sign-off cleared on the supplied evidence; commit SHA: see ST-32 `commit_sha` in execution_state.json.

## DEL-20261124-02

- **ST Item:** ST-35 — Seed staging's UK positions with the .L suffix
- **EPIC:** EPIC-06
- **Classification:** delegated_backend (staging write needs the user's permission)
- **Assigned to:** Infrastructure & Operations Owner; QA & Testing Owner (the user)
- **GitHub Issue:** #2300
- **Branch:** exec/2026-11-18__release-v9.18/EPIC-06
- **Delegated at:** 2026-11-24T09:42:13Z
- **What is needed:** (1) permission to read and correct staging `positions` rows with `market = 'UK'` and no `.L`; (2) an authenticated staging `GET /positions` showing `price_is_stale: false` for both UK positions. Staging returns 401 to the engine, which has no staging token.
- **Workflow-viability pre-check (LL-v9.10-P3-01):** not applicable; no GitHub Actions workflow is involved.
- **Unblock criteria:** AC 2 evidence: the authenticated `GET /positions` output (or its two UK rows) pasted in session; otherwise AC 2 is deferred past merge with a backlog item filed before the PR opens (sealed `sprint_backlog.md` ST-35 Staging-only ACs).
- **Commit format required:** `[EPIC-06][ST-35] <description>` pushed to `exec/2026-11-18__release-v9.18/EPIC-06`
- **Status:** Unblocked — unblocked in-session: (1) permission granted by the user, 2026-11-24 ("Yes, run all three"); the read found no UK position without `.L` (`BARC.L`, `LGEN.L` already corrected), so no UPDATE was run. (2) The user ran an authenticated staging `GET /positions` and supplied the UK rows at 2026-11-24T10:44:36Z: `BARC` and `LGEN` (display tickers; `position_service.py:260` strips `.L`), both `price_is_stale: false`. Sign-off cleared on that evidence; commit SHA: see ST-35 `commit_sha` in execution_state.json (`e0879873`).
