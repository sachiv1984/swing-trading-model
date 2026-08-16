**Owner:** QA Lead; Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-16
**Story:** ST-20 (BLG-QA-145, EPIC-04, v8.8)

# Test-Environment Parity Check — Local vs CI vs Staging

## 1. Purpose

No check previously confirmed local dev, CI, and staging environments remain configuration-consistent (env vars, dependency versions). Drift here can cause "works locally, fails in CI/staging" (or the reverse) defects. This audit compares the three environments across the dimensions most likely to cause silent behavioural drift.

**Scope note (production):** `render.yaml`'s own header states production services are "managed separately in the Render dashboard — this file only defines staging." Production env vars are therefore not repo-visible at all — the same dashboard-only-config blind spot flagged previously for Render's build/deploy path filters (`docs/ops/render_build_deploy_path_filter_audit.md`). This audit compares **local vs CI vs staging** (all three repo-visible); production is out of reach for a repo-based comparison and would require direct Render dashboard access.

## 2. Findings

### 2.1 Python version — real drift found

| Environment | Version | Source |
|---|---|---|
| Local (this session's `backend/.venv`) | **3.14.4** | `backend/.venv/bin/python3 --version` |
| CI (all workflows) | **3.11** | `python-version: '3.11'` in `ci-tests.yml`, `integration-tests.yml`, `quality_gate.yml` (7 occurrences across 4 workflows, all consistent with each other) |
| Staging | **3.11.0** | `render.yaml` (`PYTHON_VERSION: "3.11.0"`, staging API service) |

Local dev is running 3 minor versions ahead of both CI and staging, which agree with each other. The full backend suite (1159 passed / 5 skipped) currently passes identically on 3.14 locally and 3.11 in CI, so this is not an active bug — but it is an undocumented, previously-unaudited gap: a 3.11-vs-3.14 stdlib/syntax difference could pass locally and fail in CI (or vice versa) with no warning, and nothing in the repo told a developer setting up locally which version to target. No `.python-version` file, `pyproject.toml` version pin, or local-setup doc specifies an intended version anywhere in the repo (checked `docs/team_skills/`, `docs/ops/`).

**Disposition:** Documented here (this is itself the "documented as intentional" — or rather, "documented as a gap" — outcome named in the AC). Filed `BLG-OPS-146` to add a `.python-version` (or equivalent) pin so future local `venv` setups target 3.11 to match CI/staging, rather than defaulting to whatever `python3` happens to be on the machine setting it up.

### 2.2 Node version — no drift

| Environment | Version | Source |
|---|---|---|
| Local | v22.23.1 | `node --version` |
| CI (`deploy.yml`) | 22 | `node-version: '22'` |

Consistent (patch-level difference is expected and immaterial). `package.json` has no `engines` field pinning this explicitly — a minor hardening opportunity, not filed separately (low value relative to the Python gap, which is the real risk).

### 2.3 Database engine — no drift

CI's integration-test tier (`ci-tests.yml` Phase B) runs a real `postgres:15` service container (`DATABASE_URL: postgresql://ci:ci@localhost:5432/ci_test`), matching production/staging's Postgres-backed (Supabase) database — confirmed via `backend/database.py`'s `psycopg2` usage. CI's Phase A (clean/unit tests) uses a dummy `DATABASE_URL` string purely to satisfy the import-time presence check, with all real DB calls mocked — this is a deliberate, documented two-tier design, not drift.

### 2.4 Frontend env vars — one likely-inconsequential gap

Comparing `.env`, `.env.staging`, `.env.production` (repo templates) and `render.yaml`'s staging `envVars` block:

- `REACT_APP_API_URL`, `REACT_APP_APP_ID`: correctly differ per environment (expected — each points at its own backend/app ID).
- `REACT_APP_DEV_FAKE_AUTH=true`: set identically in all three. Traced to `src/api/base44Client.js:6` — the constant is **computed but never referenced anywhere else in the codebase** (confirmed via full-`src/` grep). It is dead/vestigial, so its identical "true" value everywhere has no behavioural effect in any environment. Not filed as a drift risk (nothing to drift); could be filed as a separate dead-code cleanup item if desired, but that's a different story's scope (BLG-TECH, not this parity check).
- `PUBLIC_URL`: present in `.env.staging` and `render.yaml`'s staging block (`"/"`, with a comment explaining it overrides `package.json`'s `homepage` field so asset paths resolve at root), **absent from `.env.production`**. Given production's real env vars live in the Render dashboard (not this repo — §1 scope note) and the production site is known to serve correctly today, this is very likely already set in the dashboard and the repo's `.env.production` template is simply incomplete/stale relative to it — but this cannot be confirmed without dashboard access. Filed as an advisory item (`BLG-OPS-146`, same item as §2.1 — both are "local repo template drifted from the source of truth" findings) rather than a hard gap, since there's no evidence of an actual production defect.

## 3. Gaps Filed

| Ref | Item | Disposition |
|-----|------|-------------|
| BLG-OPS-146 | (a) Pin local dev Python version (`.python-version` or equivalent) to 3.11 to match CI/staging; (b) add missing `PUBLIC_URL=/` to `.env.production`'s repo template, or confirm/document it's set in the Render dashboard | Filed — Infrastructure & Operations Owner |

## 4. Sign-Off

- [x] All three repo-visible environments (local, CI, staging) compared across Python, Node, DB engine, and frontend env vars
- [x] Production scope limitation disclosed (dashboard-only, not repo-comparable) rather than silently skipped
- [x] Real drift (Python version) documented; one advisory-only gap (PUBLIC_URL) filed, not asserted as a confirmed defect without dashboard evidence
- Signed off by: PENDING — see agent-mediated review
- Date: PENDING
