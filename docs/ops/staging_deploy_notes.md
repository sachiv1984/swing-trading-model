**Owner:** Infrastructure & Operations Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-10-07 (ST-18, EPIC-04, v9.10, BLG-OPS-171 — §7 stale-deploy check now compares staging against the latest staging-deploying commit, not main's tip); prior — 2026-09-29 (ST-17, EPIC-04, v9.8, BLG-OPS-169 — added §7, stale-staging detection via `staging-smoke-test.yml` + `deployed_commit_sha`); prior — 2026-08-21 (ST-13, EPIC-03, v9.0, BLG-OPS-25 — added post-deploy smoke test suite to `deploy-staging`, plus a new independent scheduled smoke test workflow; §3 build minute assessment updated); prior history retained — see prior entries in version control.
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Staging Deploy Notes

---

## 1. Overview

Automated staging re-deployment is configured via `.github/workflows/staging-deploy.yml` (BLG-OPS-27, ST-09, v4.0). This document records the design rationale, build minute impact assessment, and operational notes.

---

## 2. Design: Path-Filter Approach (RISK-03)

The deploy workflow triggers only on pushes to `main` that include changes to source files:

| Trigger paths | Effect |
|---------------|--------|
| `src/**`, `backend/**`, `public/**` | Trigger staging deploy |
| `package.json`, `package-lock.json`, `requirements.txt` | Trigger staging deploy |
| `docs/**`, `claude/**`, `*.md` | **No trigger** — docs-only commits are filtered out |

This ensures governance-only commits (sprint artefacts, changelogs, audit records) do not consume build minutes or cause unnecessary staging restarts.

**Decision authority:** Product Owner accepted RISK-03 (path-filter approach) 2026-05-24. ESC-RISK-03 resolved.

---

## 3. Build Minute Impact Assessment

**Updated (ST-13, BLG-OPS-25, EPIC-03, v9.0):** the `deploy-staging` job now polls for the new deploy to actually go live (`scripts/wait_for_staging_deploy_live.py`, via the Render platform API — same mechanism `staging-deploy-drift-check.yml` already uses, not a fixed sleep) and then runs a post-deploy smoke test suite (`scripts/staging_smoke_test.py`). A second, independent workflow (`staging-smoke-test.yml`) runs the same smoke suite on a schedule. All additions are still well within free-tier budget.

| Factor | Value |
|--------|-------|
| GitHub-hosted runner | ubuntu-latest |
| `deploy-staging` job runtime per trigger | ~1–3 minutes typically (curl call + deploy-status poll, usually well under its 8-minute timeout for a free-tier build + smoke test suite, ST-13) |
| Expected code-change merges per sprint | 5–15 |
| Expected monthly minutes from `deploy-staging` | ~30–135 minutes (wider range than a fixed-sleep design, since actual build time varies) |
| `staging-smoke-test.yml` schedule | every 6 hours (4×/day) |
| `staging-smoke-test.yml` job runtime per run | well under 1 minute typically (4 GET requests + wake-up ping) |
| Expected monthly minutes from `staging-smoke-test.yml` | ~120 runs/month × <1 min ≈ well under 120 minutes |
| Combined expected monthly minutes | ~150–255 minutes |
| GitHub free tier (private repos) | 2,000 minutes/month |
| Projected monthly utilisation | ~8–13% of free-tier quota |

**Conclusion:** Impact remains well within free-tier budget even with both additions. `deploy-staging`'s smoke test only runs on real deploy-triggering pushes (same path-filter as before, §2); `staging-smoke-test.yml`'s cadence (every 6 hours) was chosen to catch a between-deploys regression within a reasonable window without approaching a meaningful fraction of the quota — if usage patterns ever warrant tightening it, the cron expression is the only thing that needs to change. The deploy-status poll's 8-minute timeout is a worst-case ceiling, not a typical runtime — it only consumes that much if the build genuinely takes that long or gets stuck, in which case the job correctly fails fast rather than running the smoke test against an unconfirmed deploy (see `staging-deploy.yml`'s own comments).

---

## 4. Render Deploy Hook Setup

1. Open the Render dashboard → staging service → **Settings** → **Deploy Hook**
2. Copy the deploy hook URL (format: `https://api.render.com/deploy/srv-xxxxx?key=yyyy`)
3. Add to GitHub repository secrets as `RENDER_STAGING_DEPLOY_HOOK`:
   - Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

The workflow reads this secret at runtime. If the secret is absent, the job fails with an explicit error message.

---

## 5. BLG-OPS-25 Dependency (Smoke Test Integration)

BLG-OPS-25 (automated staging smoke test) requires a deployed staging environment as a trigger. The deploy hook mechanism introduced by this workflow (BLG-OPS-27) satisfies BLG-OPS-25's gate condition. When BLG-OPS-25 is implemented, the smoke test workflow can trigger after `staging-deploy` completes using `workflow_run` event:

```yaml
on:
  workflow_run:
    workflows: ["Deploy to Staging (Render)"]
    types: [completed]
    branches: [main]
```

---

## 6. Known Limitations

| Limitation | Notes |
|------------|-------|
| Deploy hook does not confirm deploy success | Render returns HTTP 200 on hook receipt, not on deploy completion. Monitor Render dashboard for deploy status. |
| Staging-only AC deferred | Live deploy verification requires a configured Render environment with `RENDER_STAGING_DEPLOY_HOOK` set. Tracked in BLG-OPS-28. |
| Render auto-deploy may conflict | If Render's own GitHub integration auto-deploy is also enabled, deploys may double-trigger. Disable Render's native auto-deploy if using this hook approach. |

---

## 7. Stale-Staging Detection (Post-Merge Redeploy Verification) (ST-17, BLG-OPS-169, EPIC-04, v9.8)

**Background:** Staging was found on 2026-09-24 still running pre-v9.6 code — a merged schema change (`alert_type` CHECK constraint gaining `reflection_reminder`) had not actually taken effect on staging, because this application applies schema changes via startup-run `ensure_*()` functions rather than a separate migration step, and nothing checked that staging had actually restarted with the new code. The only thing that surfaced it was a manual verification story.

**Decision (Infrastructure & Operations Owner, ESC-EXEC-20260929-01, 2026-09-29):** Extend the existing `staging-smoke-test.yml` scheduled workflow, rather than a new dedicated workflow or a cycle-close verification step. This workflow already runs every 6 hours against the same staging environment, so no new infrastructure is needed, and it keeps the build-minute footprint change to zero new jobs (§3 above).

**Mechanism:**
1. `backend/services/health_service.py`'s `get_deployed_commit_sha()` reads Render's `RENDER_GIT_COMMIT` environment variable (auto-set for every Render service, no `render.yaml` change needed), falling back to a local `git rev-parse HEAD` for non-Render environments. Exposed as `deployed_commit_sha` on `GET /health/detailed` (contract: `docs/specs/api_contracts/health_endpoints.md` v1.7).
2. `staging-smoke-test.yml` passes `EXPECTED_COMMIT_SHA: ${{ github.sha }}` (the tip of `main` this scheduled run checked out) to `scripts/staging_smoke_test.py`.
3. `staging_smoke_test.py`'s `check_deployed_commit()` compares the two. A mismatch fails the job (same Telegram-alert mechanism as any other smoke-test failure, §5) with a `STALE STAGING DEPLOY` message naming both SHAs.
4. **Comparison target (ST-18, BLG-OPS-171, v9.10):** the script first narrows `EXPECTED_COMMIT_SHA` to the latest commit at or before it that touches a `staging-deploy.yml` `on.push.paths` entry (`latest_deploy_commit()`; the workflow checks out with `fetch-depth: 0` for this). A commit outside those paths, such as a governance-only commit, never redeploys staging, so comparing against `main`'s tip reported a false `STALE STAGING DEPLOY` (run 37596800197, 2026-10-07). Staging running a descendant of the target (e.g. after a manual `staging-deploy.yml` dispatch) also counts as current (`git merge-base --is-ancestor`). If git cannot resolve either step, the check falls back to the strict tip comparison.

**Known limits (what can't be verified from the repo alone):**
- **Detection lag:** bounded by the scheduled workflow's 6-hour cadence, not immediate — a stale deploy can go undetected for up to ~6 hours after the merge that should have redeployed staging.
- **Schema-bearing changes are not distinguished from any other change.** The check has no way to inspect *which* merged commits changed a startup-applied schema function versus any other code — it flags *any* commit divergence between staging and `main` identically. This is the deliberate, conservative choice: treating every divergence as worth alerting on always covers the schema-bearing case too, at the cost of also alerting on non-schema staleness (which is itself still useful signal, just not the specific failure mode this story was filed for).
- **A `null`/missing `deployed_commit_sha`** (e.g. an older staging deploy from before this field existed) is reported as a `::warning::`, not a failure — the check cannot distinguish "genuinely stale" from "field not populated yet" without more information than it has.
- **Confirming the alert fires on a real stale-staging condition is a staging-only AC** — this cannot be reproduced in CI (there is no way to genuinely desynchronize a CI sandbox's "staging" from "main"). Tracked as `BLG-OPS-171`; see the ST-17 QA evidence log for this cycle for disposition.

---
