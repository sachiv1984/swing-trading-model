**Owner:** Infrastructure & Operations Owner
**Class:** Reference Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-22 (ST-15, BLG-OPS-163, EPIC-04, v9.6 — initial version)

---

# GitHub Actions Secrets Ownership Map

## Why this document exists

During ST-14's staging DB credential provisioning (`2026-09-15__release-v9.5`, EPIC-02), the bare `DATABASE_URL` GitHub Actions repo secret was repointed at a new read-only staging role — but it was also `backtest.yml`'s sole consumer at the time, which needs write access (`production_strategy.py` upserts backtest results directly), breaking that nightly workflow until caught and fixed (`[EPIC-02][ST-14]` commit `26d5b2b1`; `backtest.yml` now reads `PROD_DATABASE_URL` instead — see the Aliasing note below). The same session came within one message of doing the same thing to `STAGING_DATABASE_URL`, which `reset-and-seed-staging.yml`, `seed-preview.yml`, and `scripts/reset_staging_db.sh` all depend on for write access. Both incidents happened because nothing in the repo documented which secret is used by which workflow(s), what access level each needs, or which secrets are safe to rotate independently.

This document is that inventory. **Before rotating any repo secret, check its row below for every consuming workflow and the access level each one needs** — rotating to a narrower-scoped credential than the most demanding consumer requires will silently break that workflow.

## Inventory

Every `secrets.*` reference across `.github/workflows/*.yml`, current as of this document's Last Updated date. Re-derive with `grep -rhoE "secrets\.[A-Z0-9_]+" .github/workflows/*.yml | sort -u` if this list may be stale.

| Secret | Consuming workflow(s) | Environment | Required access level |
|---|---|---|---|
| `API_KEY` | `ai-endpoint-anomaly-check.yml`, `alert-evaluation.yml`, `api-key-cross-environment-check.yml`, `backtest.yml`, `daily-snapshot.yml`, `nightly-stop-update-staleness-check.yml`, `nightly-stop-update.yml`, `rebalance-exit.yml`, `risk-off-alerts.yml`, `screener-refresh.yml`, `si05-weekly-digest.yml` | Production | Read-write — the production `X-API-Key`; several consumers call mutating `POST` endpoints (e.g. `nightly-stop-update.yml`, `rebalance-exit.yml`) |
| `API_URL` | `ai-endpoint-anomaly-check.yml`, `alert-evaluation.yml`, `api-key-cross-environment-check.yml`, `backtest.yml`, `daily-snapshot.yml`, `health-check-alert.yml`, `nightly-stop-update-staleness-check.yml`, `nightly-stop-update.yml`, `rebalance-exit.yml`, `risk-off-alerts.yml`, `screener-refresh.yml`, `si05-weekly-digest.yml`, `st08-proxy-ip-verification.yml` | Production | N/A — a config value (the production API base URL), not a credential; stored as a secret only to avoid publishing the internal hostname |
| `DATABASE_URL` | *(none live — see Aliasing note)* | — | Retired alias; superseded by `PROD_DATABASE_URL` |
| `GITHUB_TOKEN` | `audit-cadence-reminder.yml`, `deploy.yml`, `execution-state-schema-check.yml`, `governance_sync.yml`, `secret-scanning.yml`, `update-visual-snapshots.yml` | N/A (GitHub-internal) | Auto-provisioned per run by GitHub Actions; scope is set per-workflow via that workflow's own `permissions:` block (e.g. `governance_sync.yml`: `issues: write`; `deploy.yml`: `contents: write`, `pages: write`, `id-token: write`) — not manually managed or rotated |
| `GITLEAKS_LICENSE` | `secret-scanning.yml` | N/A | License key (Gitleaks Pro) — no data access; loss of this secret degrades scan coverage, not a security exposure |
| `PROD_DATABASE_URL` | `backtest.yml`, `db-storage-size-snapshot.yml`, `production-db-backup.yml`, `si05-digest-staleness-check.yml` | Production | Read-write — `backtest.yml` requires write access (`production_strategy.py` upserts backtest results directly); `db-storage-size-snapshot.yml` and `si05-digest-staleness-check.yml` are read-only queries; `production-db-backup.yml` performs a `pg_dump` (read). **Do not narrow this secret to read-only** — that is exactly the mistake that originally broke `backtest.yml` (see Why this document exists, above) |
| `REACT_APP_ANTHROPIC_API_KEY` | `deploy.yml` | Production | Build-time only, but becomes **publicly visible** once built: CRA bakes `REACT_APP_*` env vars into the static JS bundle served to every browser. Treat as public, not secret, once deployed |
| `REACT_APP_API_KEY` | `deploy.yml` | Production | Same exposure profile as `REACT_APP_ANTHROPIC_API_KEY` above — publicly visible in the deployed frontend bundle |
| `RENDER_PLATFORM_API_KEY` | `render-si05-log-query.yml`, `staging-deploy-drift-check.yml`, `staging-deploy.yml` | Render account (spans staging + production services) | Read-write — Render platform API access; `staging-deploy.yml` uses it to poll deploy status (read), but it is account-scoped, not deploy-scoped, so treat rotation as affecting all three consumers together |
| `RENDER_STAGING_DEPLOY_HOOK` | `staging-deploy.yml` | Staging | Write — a deploy webhook URL; triggers a staging deploy when POSTed to |
| `STAGING_API_KEY` | `api-key-cross-environment-check.yml`, `api-performance-baseline-measurement.yml`, `staging-deploy.yml`, `staging-smoke-test.yml` | Staging | Read-write — the staging `X-API-Key` |
| `STAGING_API_URL` | `staging-deploy.yml`, `staging-smoke-test.yml` | Staging | N/A — config value (staging API base URL), not a credential |
| `STAGING_DATABASE_URL` | `reset-and-seed-staging.yml`, `seed-preview.yml` (also consumed outside GitHub Actions by `scripts/reset_staging_db.sh`) | Staging | Read-write — both consuming workflows run destructive resets and seed inserts/updates against the staging schema |
| `TELEGRAM_BOT_TOKEN` | `api-key-cross-environment-check.yml`, `backtest.yml`, `csv-export-content-regression-check.yml`, `health-check-alert.yml`, `nightly-stop-update-staleness-check.yml`, `si05-digest-staleness-check.yml`, `staging-deploy-drift-check.yml`, `staging-smoke-test.yml` | N/A (Telegram) | Write-only to the Telegram Bot API — sends alert messages; no read access to any application data |
| `TELEGRAM_CHAT_ID` | *(same consumer list as `TELEGRAM_BOT_TOKEN`)* | N/A (Telegram) | N/A — a destination chat identifier, not a credential |

## Aliasing relationships

- **`DATABASE_URL` / `PROD_DATABASE_URL`:** no workflow currently reads `secrets.DATABASE_URL` (the one remaining textual reference is a historical comment in `backtest.yml` explaining the ST-14/v9.5 rename — see Why this document exists, above). `scripts/check_si05_digest_staleness.py`'s `get_database_url()` helper still falls back from `DATABASE_URL` to `PROD_DATABASE_URL` at the environment-variable level (not the repo-secret level) — `si05-digest-staleness-check.yml` sets only `PROD_DATABASE_URL`, so that fallback is currently dormant, not live-exercised.
- No other secret in this inventory has a same-purpose alias under a different name.

## Cross-references

- `docs/infrastructure/staging_setup.md` §8 (Read-Only Access for Sprint-Execution Sessions) references this document for the full staging-secret inventory.
- `docs/ops/production_deployment_runbook.md` §7 (Cross-References) references this document for the full production-secret inventory.

## Sign-off

**Infrastructure & Operations Owner:** Approved (agent-mediated, execution_prompt.md §5.3) — 2026-09-22. Inventory verified against a fresh `grep -rhoE "secrets\.[A-Z0-9_]+" .github/workflows/*.yml` scan (14 distinct secret names, all accounted for above) plus a per-secret read of each consuming workflow's actual usage (not inferred from name alone) to determine access level and the `DATABASE_URL` retired-alias finding.
