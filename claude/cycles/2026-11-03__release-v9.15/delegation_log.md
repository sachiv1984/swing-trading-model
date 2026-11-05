Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-05

# Delegation Log — 2026-11-03__release-v9.15

## DEL-20261105-01

- **ST Item:** ST-24 — Review logged briefing ticker-caveat tokens for further non-tickers
- **EPIC:** EPIC-04
- **Classification:** delegated_backend (production log read, Human-Delegation — `sprint_backlog.md` ST-24 Notes, RISK-01; LL-v8.0-P3-01 infra/ops pattern)
- **Assigned to:** AI Compliance & Governance Officer
- **GitHub Issue:** #2167
- **Branch:** exec/2026-11-03__release-v9.15/EPIC-04
- **Delegated at:** 2026-11-05T08:26:16Z
- **What is needed:** The briefing check logs one warning per caveated token: `ticker check: endpoint=POST /ai/daily-briefing field=summary ticker=<TOKEN> action=caveat_appended prompt_version=<v>`. The sandbox `DATABASE_URL` is staging and the engine has no production log access. From the production API's Render logs (or a log export), list every `ticker=<TOKEN>` on those lines since 2026-10-30 with its count, or grant the engine a one-off read. The engine then classifies each token as ticker or non-ticker, adds the non-tickers to `_NON_TICKER_WORDS` with `test_non_ticker_words_ignored` coverage, and records the list in `qa_evidence_EPIC-04.md`. If no line was logged, say so and the review records that none was found.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Render log read only; no GitHub Actions run is involved.
- **Spec reference:** `docs/specs/api_contracts/ai_endpoints.md#POST /ai/daily-briefing` (check 3); `stage4_backlog_slice.md#ST-24`
- **Unblock criteria:** the token list with counts (or "no lines logged") supplied in session or in this record.
- **Commit format required:** `[EPIC-04][ST-24] <description>` on `exec/2026-11-03__release-v9.15/EPIC-04`
- **Status:** In Progress — carried to post-merge (2026-11-05T08:50:24Z). The AI Compliance & Governance Officer (the user, in session) said the production token list is not available in-sprint and chose to carry it post-merge. Tracked by `BLG-AI-27`, filed before the PR opens. ST-24 is graded Pass_with_deviation.

## DEL-20261105-02

- **ST Item:** ST-35 — Re-apply NOT NULL on positions.portfolio_id and positions.total_cost
- **EPIC:** EPIC-06
- **Classification:** delegated_backend (staging and production DDL, Human-Delegation — `sprint_backlog.md` ST-35 Notes, RISK-01; LL-v8.0-P3-01 infra/ops pattern)
- **Assigned to:** Data Model & Domain Schema Owner (the user, live write access)
- **GitHub Issue:** #2178
- **Branch:** exec/2026-11-03__release-v9.15/EPIC-06
- **Delegated at:** 2026-11-05T09:46:22Z
- **What is needed:** The sandbox credential is `readonly_staging` and the engine has no production access. On **staging**: run the DS-38 pre-check (`portfolio_id IS NULL` / `total_cost IS NULL` counts) and, only if both are 0, the Up Migration and the Verification query; paste all three outputs. If a count is non-zero, paste the row IDs (id, ticker, status, entry_date) instead and do not migrate. Production: same three steps after the EPIC-06 PR merges (post-merge, tracked by BLG-SPEC-217).
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Direct SQL by the user; no GitHub Actions run is involved.
- **Spec reference:** `docs/specs/data_model.md#DS-38` (drafted in-sprint); `stage4_backlog_slice.md#ST-35`
- **Unblock criteria:** staging pre-check, Up Migration and Verification outputs supplied in session (`is_nullable = NO` for both columns), or the NULL row list for a backfill decision.
- **Commit format required:** `[EPIC-06][ST-35] <description>` on `exec/2026-11-03__release-v9.15/EPIC-06`
- **Sign-off:** sign_off_cleared — staging outputs supplied by the user in session 2026-11-05 (pre-check 0 / 0; before YES/YES; after NO/NO); drift check clean on both columns.
- **Commit SHA:** e5a7f45f379336954c07205a668f5a9e5c6a78d4
- **Status:** Unblocked (2026-11-05T10:03:34Z) — Unblocked in-session — staging pre-check, migration and verification outputs, supplied by the user (Data Model & Domain Schema Owner), same session as delegation. Production half carried post-merge as planned at seal, tracked by BLG-SPEC-217. Production half completed 2026-11-05 after the PR #2193 merge (user-run in session: pre-check 0/0, YES/YES → NO/NO); recorded in DS-38 on `main`.

## DEL-20261105-03

- **ST Item:** ST-36 — Apply DS-17's open-position unique index to staging
- **EPIC:** EPIC-06
- **Classification:** delegated_backend (staging DDL, Human-Delegation — `sprint_backlog.md` ST-36 Notes, RISK-01; LL-v8.0-P3-01 infra/ops pattern)
- **Assigned to:** Data Model & Domain Schema Owner (the user, live write access)
- **GitHub Issue:** #2179
- **Branch:** exec/2026-11-03__release-v9.15/EPIC-06
- **Delegated at:** 2026-11-05T09:46:33Z
- **What is needed:** On **staging**: run DS-17's Up Migration (its `DO` block is the duplicate pre-check and aborts with the offending groups listed if any exist), then DS-17's Verification query; paste both outputs. If the migration aborts, paste the abort message instead.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Direct SQL by the user; no GitHub Actions run is involved.
- **Spec reference:** `docs/specs/data_model.md#DS-17`; `stage4_backlog_slice.md#ST-36`
- **Unblock criteria:** DS-17 Verification output from staging listing `idx_positions_open_ticker_entry_date_unique` with DS-17's definition, supplied in session.
- **Commit format required:** `[EPIC-06][ST-36] <description>` on `exec/2026-11-03__release-v9.15/EPIC-06`
- **Sign-off:** sign_off_cleared — staging migration ran without abort and pg_indexes output supplied by the user in session 2026-11-05; matches DS-17.
- **Commit SHA:** dfee397be4f255352436538845afe5780b428b45
- **Status:** Unblocked (2026-11-05T10:20:33Z) — Unblocked in-session — staging DS-17 Up Migration and Verification output, supplied by the user (Data Model & Domain Schema Owner), same session as delegation.
