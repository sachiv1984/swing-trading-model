Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-30

# Delegation Log — 2026-10-29__release-v9.14

## DEL-20261029-01

- **ST Item:** ST-01 — Restore eslint-config-react-app so the frontend builds and deploys again
- **EPIC:** EPIC-01
- **Classification:** delegated_backend (Render dashboard access, Human-Delegation — `sprint_backlog.md` ST-01 Notes, RISK-01; LL-v8.0-P3-01 infra/ops pattern)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #2078
- **Branch:** exec/2026-10-29__release-v9.14/EPIC-01
- **Delegated at:** 2026-10-29T14:55:56Z
- **What is needed:** The engine has fixed the lockfile and added the CI production-build step (`f5e48d78`, ACs 1 prep and 3). `render.yaml` sets no `DISABLE_ESLINT_PLUGIN` for `trading-assistant-staging`, so any such variable is dashboard-only and not visible to the engine. In the Render dashboard, for the `trading-assistant-staging` static site: (1) open Environment and report whether `DISABLE_ESLINT_PLUGIN` (or any other ESLint workaround, including a changed Build Command) is set; (2) if it is, remove it; (3) once EPIC-01 is on `main`, confirm the next staging frontend build from `main` succeeds (paste the build log's "Compiled" or "Compiled with warnings" line and the commit it built).
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Render dashboard read and edit plus a Render build; no GitHub Actions run is involved. `deploy.yml`'s last 3 runs all failed at Build (latest 40894097090, 2026-10-29), which is the fault this story fixes.
- **Spec reference:** `render.yaml#trading-assistant-staging`; `stage4_backlog_slice.md#ST-01` AC 2
- **Unblock criteria:** (1) and (2) reported; (3) a successful staging build from a `main` commit containing `f5e48d78`, recorded in `qa_evidence_EPIC-01.md` under ST-01.
- **Commit format required:** `[EPIC-01][ST-01] <description>` pushed to `exec/2026-10-29__release-v9.14/EPIC-01` (or a `[GOVERNANCE]` commit on `main` if EPIC-01 has merged)
- **Status:** Unblocked — 2026-10-29, unblocked in-session by the user (human, acting for the Infrastructure & Operations Owner), same session as the delegation. (1) `DISABLE_ESLINT_PLUGIN` was set on `trading-assistant-staging` in the Render dashboard; (2) removed by the user; staging pointed at `exec/2026-10-29__release-v9.14/EPIC-01` for the check. First deploy (`ea20658a`) failed at install (ERESOLVE, Render's plain `npm install`), fixed by the repo `.npmrc` in `3fbfe5e3` plus ST-08's import-order fix `8f05e704`. (3) Redeploy of `4719c694` built with ESLint enabled and no workaround: warnings only, "The build folder is ready to be deployed", "Your site is live" at 2026-10-29T16:04:44Z. (a) Sign-off: sign_off_cleared. (b) Commit SHA: `3fbfe5e3c3818f2dc22b30cca2047b10e492efc3` (`.npmrc`, the change that made the staging build work). Note: staging still points at the EPIC branch; repoint it to `main` after EPIC-01 merges. The `main` deploy check stays with BLG-OPS-200 (AC 1, post-merge).

## DEL-20261030-01

- **ST Item:** ST-43 — Per-environment CORS allow-list
- **EPIC:** EPIC-06
- **Classification:** delegated_backend (Render dashboard access, Human-Delegation — `sprint_backlog.md` ST-43 Notes, RISK-01; LL-v8.0-P3-01 infra/ops pattern)
- **Assigned to:** Infrastructure & Operations Owner (with the Cybersecurity & Trust Lead)
- **GitHub Issue:** #2120
- **Branch:** exec/2026-10-29__release-v9.14/EPIC-06
- **Delegated at:** 2026-10-30T09:39:16Z
- **What is needed:** The engine has shipped the code, test and docs (`4eb1e6cb`, AC 1). The allow-list now resolves at startup from `CORS_ALLOWED_ORIGINS`, else `DEPLOY_ENV`, else Render's own `RENDER`/`RENDER_SERVICE_NAME` (`docs/infrastructure/cors_allow_list.md`). `render.yaml` sets `DEPLOY_ENV=staging` on `trading-assistant-api-staging`. Production is not in `render.yaml`, and inference already resolves it to `production` unless its service name ends in `-staging`. After EPIC-06 merges and deploys: (1) in the Render dashboard, set `DEPLOY_ENV=production` on the production API and confirm `DEPLOY_ENV=staging` is present on the staging API (add it if the Blueprint has not synced it); (2) run the two preflight commands in `cors_allow_list.md` §Verifying a deployment against staging and production and paste the status codes and `access-control-allow-origin` lines.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. Render dashboard edit plus two `curl` preflights; no GitHub Actions run is involved.
- **Spec reference:** `docs/infrastructure/cors_allow_list.md`; `stage4_backlog_slice.md#ST-43` AC 2
- **Unblock criteria:** Seal-marked post-merge AC 2, tracked by BLG-SEC-44: production rejects `http://localhost:3000` (400) and accepts the Pages origin; the staging result recorded the same way, with commands, responses and date.
- **Commit format required:** `[GOVERNANCE] <description>` on `main` (EPIC-06 will have merged), or `[EPIC-06][ST-43] <description>` on `exec/2026-10-29__release-v9.14/EPIC-06` if before merge
- **Status:** Unblocked — 2026-10-30, after PR #2133 merged (`5e7351af`). The user (human, acting for the Infrastructure & Operations Owner) confirmed `5e7351af` live on production and set `DEPLOY_ENV=production` in the Render dashboard; `DEPLOY_ENV=staging` was already on the staging API. The engine ran the preflights at 15:18–15:19Z and 15:29Z: production rejects `http://localhost:3000` (400) and accepts the Pages origin (200); staging accepts localhost and its own frontend and rejects the Pages origin. Recorded in `cors_allow_list.md` §Deployed checks and `qa_evidence_EPIC-06.md`. (a) Sign-off: sign_off_cleared; staging defaults confirmed by an agent-mediated Cybersecurity & Trust Lead review (§5.3), accepted by the user. (b) Commit SHA: `4eb1e6cb` (ST-43). BLG-SEC-44 resolved.

## DEL-20261030-02

- **ST Item:** ST-39 — Compute cost trending by feature area
- **EPIC:** EPIC-06
- **Classification:** delegated_backend (production data access, Human-Delegation — `sprint_backlog.md` ST-39 Notes, RISK-01)
- **Assigned to:** FinOps & Resource Architect (with the Infrastructure & Operations Owner)
- **GitHub Issue:** #2116
- **Branch:** exec/2026-10-29__release-v9.14/EPIC-06
- **Delegated at:** 2026-10-30T09:53:24Z
- **What is needed:** The engine has shipped the report's method, allocation rule and generator (`c01e9805`, AC 1): `docs/ops/cost_by_feature_area.md` and `scripts/cost_by_feature_area.py`. After a complete calendar month of production data exists (November 2026 is the first full month after v9.13's `api_call_log.feature` attribution and v6.8's `claude_audit_log`): run `DATABASE_URL=<production URL> python3 scripts/cost_by_feature_area.py --month <YYYY-MM> --render-monthly-usd <invoice amount>` and paste the printed table into §6 with the date read. October 2026 also qualifies if attribution rows cover all of it.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch; a read-only script run against production by a human with access.
- **Spec reference:** `docs/ops/cost_by_feature_area.md` §5–§6; `stage4_backlog_slice.md#ST-39` AC 2
- **Unblock criteria:** Seal-marked post-merge AC 2, tracked by BLG-OPS-201: the report populated for at least one complete month of production data, with the month and the data date stated.
- **Commit format required:** `[GOVERNANCE] <description>` on `main` (EPIC-06 will have merged)
- **Status:** Pending — carried to post-merge (BLG-OPS-201). The story is graded on its in-sprint AC (LL-v9.13-P3-03).

## DEL-20261030-03

- **ST Item:** ST-42 — Make ci-usage-report.yml's monthly commit succeed
- **EPIC:** EPIC-06
- **Classification:** delegated_backend (a run on `main`, possible branch-rule handling, Human-Delegation — `sprint_backlog.md` ST-42 Notes, RISK-01)
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #2119
- **Branch:** exec/2026-10-29__release-v9.14/EPIC-06
- **Delegated at:** 2026-10-30T09:53:24Z
- **What is needed:** The engine has shipped the workflow fix (`c7e45c17`). Cause, confirmed from `main`'s branch protection via the GitHub API on 2026-10-30: a PR with 1 approving review and 5 required checks, which a `GITHUB_TOKEN` push cannot bypass. The report now goes to branch `ci-usage-report/<YYYY-MM>` and a 90-day artifact, and the workflow tries to open a `[GOVERNANCE]` PR. The repository does not allow Actions to create PRs (`can_approve_pull_request_reviews: false`), so expect a warning with a compare link rather than a PR, unless that setting is turned on (Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests"). After EPIC-06 merges: (1) dispatch `ci-usage-report.yml` on `main` with `year_month=2026-09`; (2) open the PR from the compare link if the bot could not, close and reopen it so checks run, review and merge it; (3) record the run ID and the merge commit.
- **Workflow viability (LL-v9.10-P3-01):** Last 10 runs: no success (one run, 36861580190, 2026-10-01, failed at "Commit report" — the fault this story fixes). The prerequisite (the push to `main`) is removed by the fix itself; the remaining prerequisite is the human PR merge above.
- **Spec reference:** `.github/workflows/ci-usage-report.yml`; `stage4_backlog_slice.md#ST-42` ACs 1–2
- **Unblock criteria:** Seal-marked post-merge ACs 1 and 2, tracked by BLG-OPS-202: a run on `main` succeeds (run ID recorded) and `docs/ops/ci_usage_reports/2026-09.md` exists on `main`.
- **Commit format required:** the bot's `[GOVERNANCE] Add monthly CI usage report 2026-09` PR, then a `[GOVERNANCE]` record on `main`
- **Status:** Unblocked — 2026-10-30, after PR #2133 merged (`5e7351af`). `ci-usage-report.yml` run 41082206367 (workflow_dispatch on `main` by the user, `year_month=2026-09`, 2026-10-30T15:36:04Z) succeeded. It committed the report to `ci-usage-report/2026-09` (`2919a2e5`) and warned, as expected, that Actions may not open pull requests. The engine opened PR #2134 from the user's account; all 22 checks passed; the user merged it at 15:50:47Z (merge commit `cc52d408`). `docs/ops/ci_usage_reports/2026-09.md` is on `main`. (a) Sign-off: sign_off_cleared. (b) Commit SHA: `c7e45c17` (ST-42). BLG-OPS-202 resolved. Opening the monthly PR by hand remains until BLG-OPS-210 is decided.
