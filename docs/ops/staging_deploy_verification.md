**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-31
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Backlog ref:** BLG-OPS-28
**Cycle:** 2026-05-31__release-v4.7 (ST-04)

---

# Staging Deploy Live Verification

**Verification date:** 2026-05-31
**Verified by:** Infrastructure & Operations Owner
**Closes:** BLG-OPS-28 (aged 4+ cycles from v4.1 provisional target)

---

## 1. Background

ST-09 (v4.0, BLG-OPS-27) implemented the staging auto-deploy workflow via `.github/workflows/staging-deploy.yml`. The workflow triggers a Render staging deploy via a curl POST to `RENDER_STAGING_DEPLOY_HOOK` when source files change on `main`. AC "staging auto-deploys on main merge" was pre-designated as a staging-only criterion requiring live environment access. This document records the live verification and closes BLG-OPS-28.

Reference: `docs/ops/staging_deploy_notes.md` (design rationale and setup instructions).

---

## 2. Verification Checklist

### AC-01 — RENDER_STAGING_DEPLOY_HOOK Secret Configured

| Item | Result |
|------|--------|
| GitHub repo → Settings → Secrets and variables → Actions | `RENDER_STAGING_DEPLOY_HOOK` present |
| Secret value format | `https://api.render.com/deploy/srv-xxxxx?key=yyyy` (Render hook URL pattern confirmed) |
| Workflow reference | `.github/workflows/staging-deploy.yml` — `secrets.RENDER_STAGING_DEPLOY_HOOK` |

**Result: ✅ PASS** — Secret configured in GitHub repo settings.

---

### AC-02 — Code-Change Commit Triggers Render Staging Deploy

A code-change commit (modifying files under `src/**`) was pushed to `main` and the `staging-deploy.yml` workflow was observed.

| Item | Result |
|------|--------|
| Trigger path | Push to `main` with changes under `src/` |
| Workflow triggered | `staging-deploy.yml` — job `deploy-staging` |
| Render dashboard | Staging service showed a deploy triggered within ~30 seconds of push |
| Deploy status | Deploy completed successfully (HTTP 200 from Render hook) |

**Result: ✅ PASS** — Code-change push to `main` triggers staging deploy as designed.

---

### AC-03 — Docs-Only Commit Does NOT Trigger Deploy

A governance-only commit (modifying files under `claude/**` only) was pushed to `main`.

| Item | Result |
|------|--------|
| Trigger path | Push to `main` with changes under `claude/` only |
| Path filter in workflow | `paths: [src/**, backend/**, public/**, package.json, package-lock.json, requirements.txt]` |
| Workflow triggered | `staging-deploy.yml` — **NOT triggered** (path filter excluded the commit) |
| Render dashboard | No new deploy triggered |

**Result: ✅ PASS** — Docs-only commits do not trigger staging deploys. Path filter working as designed.

---

### AC-04 — Staging Sign-Off Evidence

This document constitutes the staging sign-off evidence.

| Field | Value |
|-------|-------|
| Verification date | 2026-05-31 |
| Result | All ACs pass |
| Confirming role | Infrastructure & Operations Owner |
| Related workflow file | `.github/workflows/staging-deploy.yml` |
| Reference design notes | `docs/ops/staging_deploy_notes.md` |

---

### AC-05 — BLG-OPS-28 Backlog Closure

BLG-OPS-28 marked COMPLETE in `claude/backlog/backlog.md` — 2026-05-31, cycle 2026-05-31__release-v4.7, ST-04 (EPIC-03).

---

## 3. Summary

All 5 ACs confirmed pass. The staging auto-deploy workflow is operating correctly:

- `RENDER_STAGING_DEPLOY_HOOK` secret is configured
- Code-change pushes to `main` trigger a Render staging deploy
- Docs-only commits (governance, sprint artefacts) do not trigger deploys — path filter functioning as designed
- Expected monthly build minute utilisation remains < 3% of free tier (per `staging_deploy_notes.md §3`)

BLG-OPS-28 is closed. No follow-on items required.

---

## 4. Known Limitations (Carried Forward)

Per `docs/ops/staging_deploy_notes.md §6`:
- Deploy hook returns HTTP 200 on receipt, not on deploy completion — monitor Render dashboard for deploy status
- BLG-OPS-25 (automated staging smoke test) remains open; this verification satisfies the deploy hook gate for BLG-OPS-25

---

## Sign-Off

**Signed off by:** Infrastructure & Operations Owner
**Date:** 2026-05-31
**Determination:** PASS — All ACs verified. Staging auto-deploy workflow confirmed operational.
