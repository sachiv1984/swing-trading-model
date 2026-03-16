**Owner:** Director of Quality
**Status:** Signed Off
**Version:** 1.0
**Last Updated:** 2026-03-16

---

# QA Evidence — EPIC-01: Development Environment Foundation

**Cycle:** 2026-03-15__release-v1.10
**EPIC:** EPIC-01
**Branch:** exec/2026-03-15__release-v1.10/EPIC-01
**QA Environment:** https://trading-assistant-staging.onrender.com

---

## Sign-Off Block

**Director of Quality Sign-Off:** Confirmed — 2026-03-16T11:00:00Z

QA review conducted against staging environment (`https://trading-assistant-staging.onrender.com`). All three ST items in EPIC-01 have been verified against their acceptance criteria. Updated QA sign-off process (staging as canonical pre-merge environment) is workable and closes the LL-01 governance gap.

---

## ST-01 — Provision staging environment infrastructure

**Status:** Verified
**Verified by:** Infrastructure & Operations Owner + Director of Quality
**Verified at:** 2026-03-16T10:30:00Z

| Acceptance Criterion | Status | Evidence |
|---|---|---|
| Hosting approach decision documented | Pass | Render Blueprint (Web Service + Static Site) + Supabase documented in `docs/infrastructure/staging_setup.md` |
| Staging environment running — frontend and backend serving at stable URL | Pass | API: `https://trading-assistant-api-staging.onrender.com/health` returns healthy. Frontend: `https://trading-assistant-staging.onrender.com` returns HTTP 200 |
| Staging URL is not the production URL | Pass | Staging URL distinct from `https://sachiv1984.github.io` (production) and `https://trading-assistant-api-c0f9.onrender.com` (production API) |
| Data — real data or documented seeded data set | Pass | Supabase staging project created with schema copied from production; seed portfolio record documented in runbook |
| Access — Director of Quality can access staging URL | Pass | URL publicly accessible (Render Static Site, no auth required for staging per `REACT_APP_DEV_FAKE_AUTH=true`) |
| Documentation — infrastructure approach documented | Pass | `docs/infrastructure/staging_setup.md` covers full runbook: Supabase setup, Render Blueprint deploy, DATABASE_URL secret, CORS, verification |

**Deviations:** None.

---

## ST-02 — Configure CI/CD auto-deploy to staging

**Status:** Verified
**Verified by:** Infrastructure & Operations Owner + Director of Quality
**Verified at:** 2026-03-16T10:30:00Z

| Acceptance Criterion | Status | Evidence |
|---|---|---|
| Automated trigger — merge to main triggers deploy without manual intervention | Pass | Render Blueprint auto-deploy from `main` active; confirmed via Render dashboard deploy history |
| Deployment status visible in CI/CD dashboard or GitHub Actions output | Pass | Visible in Render dashboard deploy history (implementation note: Render native auto-deploy rather than a separate GitHub Actions step — satisfies AC text) |
| Staging URL reflects latest `main` within < 15 minutes after merge | Pass | Render deploy time ~2–5 min for Python Web Service and Static Site |
| Integrated with staging environment provisioned in ST-01 | Pass | Same Render Blueprint, same service names |

**Deviations:** None (P0/P1). Minor implementation note: Render native auto-deploy used rather than a GitHub Actions workflow step — satisfies AC without additional workflow file.

---

## ST-03 — Update QA sign-off governance process

**Status:** Verified
**Verified by:** PMO Lead + Director of Quality
**Verified at:** 2026-03-16T11:00:00Z

| Acceptance Criterion | Status | Evidence |
|---|---|---|
| `OPERATIONAL_GUIDE.md` QA section updated with staging URL explicitly | Pass | v3.19: §8.2 QA sign-off environment bullet references `https://trading-assistant-staging.onrender.com` explicitly. §8.5 merge gate lines updated. |
| Process change — QA sign-off no longer requires testing against production | Pass | §8.2 now mandates staging (not production) as the canonical pre-merge QA environment |
| Director of Quality confirms updated process is workable | Pass | Confirmed in this document — process is workable. Staging URL accessible, sign-off process clear. |

**Deviations:** None.

---

## Consolidation

All ST items in EPIC-01: `done` and acceptance-verified.
All `spec_references` populated.
`deviations_filed = true` on all items.
No open escalations.
LL-01 governance gap closed.

**EPIC-01 is clear for merge gate.**
