**Owner:** Infrastructure & Operations Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-08-21 (ST-13, EPIC-03, v9.0, BLG-OPS-25 — added post-deploy smoke test suite to `deploy-staging`, plus a new independent scheduled smoke test workflow; §3 build minute assessment updated)
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
