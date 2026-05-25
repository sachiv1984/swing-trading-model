**Owner:** Infrastructure & Operations Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-24
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

| Factor | Value |
|--------|-------|
| GitHub-hosted runner | ubuntu-latest |
| Job runtime per trigger | ~1 minute (curl call only; no build step) |
| Expected code-change merges per sprint | 5–15 |
| Expected monthly minutes consumed | ~15–45 minutes |
| GitHub free tier (private repos) | 2,000 minutes/month |
| Projected monthly utilisation | < 3% of free-tier quota |

**Conclusion:** Impact is negligible. The workflow job (`deploy-staging`) performs only a `curl` POST to the Render deploy hook — no Node.js build, no Python install. The GitHub Actions runner shuts down as soon as the HTTP response is received.

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
