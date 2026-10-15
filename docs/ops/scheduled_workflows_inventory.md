**Owner:** Infrastructure & Operations Owner
**Class:** Reference Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-15 (ST-32, BLG-GOV-371, EPIC-04, v9.12 — initial version)
**Co-owner:** FinOps & Resource Architect (minutes/month column)

---

# Scheduled GitHub Workflows Inventory

## Why this document exists

23 workflows under `.github/workflows/` run on a `schedule:` trigger, and until now nothing listed what each one writes or what it costs. Two of them, `daily-snapshot.yml` (through `GET /positions/analyze`) and `nightly-stop-update.yml`, both write position stops; that was found only by reading code (BLG-GOV-371). This table gives one place to check before adding, moving or retiring a scheduled job.

**Review cadence:** this inventory is reviewed at each `run audit` (CLAUDE.md §1, every 3 cycles). The reviewer re-derives the workflow list, updates any changed row and bumps the version. A scheduled workflow added between audits should add its own row in the same commit.

## Inventory

All times are UTC. **Writes** names the database tables a run changes (through the endpoint or script it calls), plus any non-database side effect. `api_call_log` rows written by outbound market-data calls are listed where the path makes them. "Telegram" means a message is sent only on a failure or alert condition. The in-memory `GET /health/scheduler` job registry (`record_nightly_job`) is not a table and is not listed.

| Workflow | Owner | Cron | Writes | Runs (30d) | Avg min/run | Minutes/month |
|---|---|---|---|---:|---:|---:|
| `ai-daily-cost-check.yml` | FinOps & Resource Architect | `15 */6 * * *` (4×/day) | `scheduled_alert_dedup`; Telegram | 5 † | 0.98 | 119.3 † |
| `ai-endpoint-anomaly-check.yml` | FinOps & Resource Architect | `0 7 * * *` | `scheduled_alert_dedup`; Telegram | 30 | 1.01 | 30.3 |
| `alert-evaluation.yml` | Infrastructure & Operations Owner | `30 21 * * 1-5` | `alert_evaluations`, `alert_rules`, `price_alerts`, `notifications`, `api_call_log` | 21 | 1.02 | 21.4 |
| `api-key-cross-environment-check.yml` | Cybersecurity & Trust Lead | `0 6 * * *` | None (read-only); Telegram | 30 | 0.76 | 22.8 |
| `audit-cadence-reminder.yml` | PMO Lead | `17 6 * * *` | GitHub issue (open/update/close); no database | 30 | 0.23 | 6.9 |
| `backtest.yml` | Infrastructure & Operations Owner | `0 1 * * *` | `backtest_trades`, `backtest_yearly_performance`, `backtest_open_positions`, `backtest_import_history` (via `POST /strategy/benchmark/import`; `production_strategy.py` only reads `ticker_universe`); Telegram | 30 | 2.85 | 85.5 |
| `ci-usage-report.yml` | FinOps & Resource Architect | `0 6 1 * *` (monthly) | Commits `docs/ops/ci_usage_reports/<YYYY-MM>.md` to the repo; no database | 1 | 1.88 | 1.9 |
| `csv-export-content-regression-check.yml` | Director of Quality | `0 6 1 1,4,7,10 *` (quarterly) | None (read-only); Telegram | 1 | 0.33 | 0.3 |
| `daily-snapshot.yml` | Infrastructure & Operations Owner | `0 16 * * 1-5` | `positions` (stops, via `GET /positions/analyze`); `portfolio_history`, `sector_regime_history` (`POST /portfolio/snapshot`); `signals` (`POST /signals/generate`); deletes from `api_call_log`, `claude_audit_log`, `gemini_audit_log` (`POST /ops/purge-audit-logs`); `api_call_log` | 22 | 5.37 | 118.1 |
| `dependency-vuln-rescan.yml` | Cybersecurity & Trust Lead | `0 7 1 * *` (monthly) | GitHub issue; no database | 1 | 0.86 | 0.9 |
| `escalation-sla-reminder.yml` | PMO Lead | `23 7 * * *` | GitHub issue (`escalation-sla`); no database | 6 † | 0.22 | 6.7 † |
| `health-check-alert.yml` | Infrastructure & Operations Owner | `*/15 * * * *` | None (read-only); Telegram | 159 ‡ | 1.20 | 190.8 |
| `nightly-stop-update-staleness-check.yml` | Infrastructure & Operations Owner | `0 */6 * * *` | None (reads `GET /health/scheduler`); Telegram | 79 ‡ | 0.73 | 57.7 |
| `nightly-stop-update.yml` | Infrastructure & Operations Owner | `30 22 * * 1-5` | `positions` (trailing stops), `api_call_log` | 18 § | 0.23 | 4.1 |
| `post-deploy-stop-health.yml` | Infrastructure & Operations Owner | `30 7 * * 1-5` (also after each production deploy) | None (read-only); Telegram | 2 † | 0.73 | 15.8 † |
| `production-db-backup.yml` | Infrastructure & Operations Owner | `0 3 * * *` | GitHub Actions artifact (`pg_dump` of production); no database writes | 30 | 1.58 | 47.4 |
| `rebalance-exit.yml` | Infrastructure & Operations Owner | `45 22 * * 1-5` | `signals` (`exit_rebalance`) | 18 § | 0.39 | 7.0 |
| `risk-off-alerts.yml` | Infrastructure & Operations Owner | `15 22 * * 1-5` | `positions` (`risk_off_exit` alert) | 22 | 0.91 | 20.0 |
| `screener-refresh.yml` | Infrastructure & Operations Owner | `0 22 * * 1-5` | `screener_runs`, `screener_results`, `api_call_log` | 22 | 0.47 | 10.3 |
| `si05-digest-staleness-check.yml` | Infrastructure & Operations Owner | `0 8 * * *` | None (reads `si05_digest_log`); Telegram | 30 | 0.25 | 7.5 |
| `si05-weekly-digest.yml` | Infrastructure & Operations Owner | `0 19 * * 0` (weekly) | `si05_digest_log`; Telegram (the digest itself) | 4 | 0.94 | 3.8 |
| `staging-deploy-drift-check.yml` | Infrastructure & Operations Owner | `0 * * * *` (hourly) | None (read-only); Telegram | 143 ‡ | 0.32 | 45.8 |
| `staging-smoke-test.yml` | Infrastructure & Operations Owner | `0 */6 * * *` | None (GET-only against staging); Telegram | 106 ‡ | 1.96 | 207.8 |
| **Total** | | | | | | **≈1,032** |

† Added within the 30-day window (`ai-daily-cost-check.yml` 2026-10-13, `escalation-sla-reminder.yml` and `post-deploy-stop-health.yml` 2026-10-08). Minutes/month is projected at the full cron cadence (121.7, 30.4 and 21.7 runs/month), not taken from the partial count.

‡ GitHub Actions delays and drops scheduled runs under load, so high-frequency crons run far less often than the cron implies (`health-check-alert.yml`: 159 runs against about 2,900 cron slots). The actual count is used.

§ 18 runs against 22 weekdays in the window. See Observations.

## Method

- **Workflow list:** every file in `.github/workflows/` with a `schedule:` trigger (`grep -l '^\s*schedule:' .github/workflows/*.yml`), 23 files on 2026-10-15.
- **Owner:** the role that owns the domain of the backlog item that created the workflow (named in each workflow's header comment): FinOps for AI cost and CI usage, Cybersecurity & Trust Lead for key and vulnerability checks, PMO Lead for governance reminders, Director of Quality for the CSV regression check, Infrastructure & Operations Owner otherwise.
- **Writes:** traced from the endpoint or script each workflow calls through to the SQL `INSERT`, `UPDATE` and `DELETE` statements it reaches in `backend/` (an AST call-graph walk from the route handler), plus GitHub side effects read from each workflow's `permissions:` block and steps.
- **Runs (30d):** scheduled-event runs created 2026-09-15 to 2026-10-14 (`gh api repos/<repo>/actions/workflows/<file>/runs?event=schedule&created=...`). Deploy-triggered and manual runs are excluded.
- **Avg min/run:** mean wall-clock time (`updatedAt − startedAt`) of up to the 20 most recent scheduled runs.
- **Minutes/month:** runs × average. These are run minutes, not billable minutes: the repository is public and GitHub does not bill Actions minutes for it (see `docs/ops/ci_usage_reports/2026-08.md`).

## Observations

- **Two jobs write stops.** `daily-snapshot.yml` calls `GET /positions/analyze`, which recomputes and stores stops at 16:00 UTC; `nightly-stop-update.yml` recomputes them at 22:30 UTC. Both reach the same `positions` stop columns. This is the overlap BLG-GOV-371 named; this inventory records it and does not change it.
- **Missed weekday runs.** `nightly-stop-update.yml` and `rebalance-exit.yml` each ran 18 times against 22 weekdays, while `risk-off-alerts.yml` and `screener-refresh.yml` in the same 22:00–22:45 slot ran 22 times. `nightly-stop-update-staleness-check.yml` exists to catch a missed stop run. The cause is not investigated here.
- **CI usage report not produced.** `ci-usage-report.yml`'s only scheduled run (2026-10-01, run 36861580190) failed at its "Commit report" step, so `docs/ops/ci_usage_reports/` holds only the hand-committed `2026-08.md`. Filed as BLG-OPS-188.
