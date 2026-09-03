**Owner:** QA Lead; Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-21 (ST-15, EPIC-03, v9.0, BLG-OPS-146 remainder — §2.4 PUBLIC_URL finding resolved: confirmed no production gap exists, on any service); prior — 2026-08-16 (ST-20, EPIC-04, v8.8, BLG-QA-145 — initial parity check)
**Story:** ST-20 (BLG-QA-145, EPIC-04, v8.8); ST-15 (BLG-OPS-146 remainder, EPIC-03, v9.0)

# Test-Environment Parity Check — Local vs CI vs Staging

## 1. Purpose

No check previously confirmed local dev, CI, and staging environments remain configuration-consistent (env vars, dependency versions). Drift here can cause "works locally, fails in CI/staging" (or the reverse) defects. This audit compares the three environments across the dimensions most likely to cause silent behavioural drift.

**Scope note (production):** `render.yaml`'s own header states production services are "managed separately in the Render dashboard — this file only defines staging." Production env vars are therefore not repo-visible at all — the same dashboard-only-config blind spot flagged previously for Render's build/deploy path filters (`docs/ops/render_build_deploy_path_filter_audit.md`). This audit compares **local vs CI vs staging** (all three repo-visible); production is out of reach for a repo-based comparison and would require direct Render dashboard access.

## 2. Findings

### 2.1 Python version — pin exists but is not honoured by this session's local venv

| Environment | Version | Source |
|---|---|---|
| Local (this session's `backend/.venv`) | **3.14.4** | `backend/.venv/bin/python3 --version` |
| Local pin (declared, not enforced) | **3.11.0** | `backend/.python-version` (git-tracked, committed 2026-01-25, `244ffe40` — predates this audit) |
| CI (all workflows) | **3.11** | `python-version: '3.11'` — **21 occurrences across 16 distinct workflow files** (`grep -rn python-version .github/workflows/*.yml`, re-counted after an initial undercounted pass), all consistent with each other |
| Staging | **3.11.0** | `render.yaml` (`PYTHON_VERSION: "3.11.0"`, staging API service) |

**Correction (QA Lead review, first pass Blocked):** this section originally claimed "no `.python-version` file... specifies an intended version anywhere in the repo," checking only `docs/team_skills/` and `docs/ops/` — it never looked in `backend/`, where the venv it tested actually lives. `backend/.python-version` exists and correctly declares `3.11.0`, matching CI/staging exactly. The real finding is not "no pin exists" — it's that **a correct pin exists but this session's local venv doesn't honour it**: `backend/.venv/pyvenv.cfg` shows it was created via plain `python3 -m venv` against whatever `python3` resolved to on `PATH` (`/usr/bin/python3.14`, confirmed via `readlink -f backend/.venv/bin/python3`); no `pyenv` (or equivalent version-manager shim that would read `.python-version`) is present on `PATH` in this environment, and no `python3.11` binary is installed here to switch to even if one were. The original "7 occurrences across 4 workflows" CI citation was also undercounted (~4x) — corrected above.

The full backend suite (1160 passed / 5 skipped) currently passes identically on 3.14 locally and 3.11 in CI, so this is not an active bug — but a 3.11-vs-3.14 stdlib/syntax difference could still pass locally and fail in CI (or vice versa) with no warning, since the declared pin is silently unenforceable in at least this environment.

**Disposition:** Documented here. `BLG-OPS-146` filed and re-scoped (see below) — the fix is not "add a pin" (one already exists correctly) but "ensure local venv setup actually honours the existing `backend/.python-version` pin" (e.g. document a `pyenv install $(cat backend/.python-version) && pyenv local` step, or an equivalent enforcement mechanism, in a local-setup doc).

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

**Resolved (ST-15, `BLG-OPS-146` remainder, 2026-08-21):** the hedge above ("very likely already set in the dashboard") was checked against the wrong service and needed correcting. A human confirmed `PUBLIC_URL` is genuinely absent from the production **backend API** service's (`trading-assistant-api`) environment variables — but that is not the gap this finding was actually worried about. `PUBLIC_URL` is a Create React App **frontend build-time** variable; it has no meaning to a FastAPI backend process and its absence there is correct, not a defect. The real question — does the actual live production **frontend** resolve its static asset paths correctly? — was already answered independently of any Render dashboard config: this repo's production frontend is **GitHub Pages** (`.github/workflows/deploy.yml`), not a Render-hosted static site (`render.yaml` defines only a *staging* frontend; there is no production Render Static Site at all). `deploy.yml`'s build step sets `PUBLIC_URL: /swing-trading-model` as an explicit GitHub Actions env var (CRA env-var precedence: an explicit build-step var wins over any `.env.production` value), and a dedicated CI safeguard (`ST-16`, `BLG-OPS-148`, this same cycle) fails the deploy fast if that override ever stops taking effect — the exact regression class behind the 2026-08-21 white-page incident. **Net finding: no production PUBLIC_URL gap exists anywhere** — `.env.production`'s missing key is genuinely inconsequential (as originally hedged, now confirmed rather than assumed), the backend correctly has no such variable, and the frontend's actual asset-path correctness is independently verified in-repo on every deploy.

## 3. Gaps Filed

| Ref | Item | Disposition |
|-----|------|-------------|
| BLG-OPS-146 | (a) Document/enforce a mechanism for local venv setup to actually honour the existing `backend/.python-version` pin (3.11.0) — e.g. a `pyenv install $(cat backend/.python-version)` step in a local-setup doc — rather than defaulting to whatever `python3` happens to be on `PATH`; (b) add missing `PUBLIC_URL=/` to `.env.production`'s repo template, or confirm/document it's set in the Render dashboard | Filed — Infrastructure & Operations Owner |

## 4. Sign-Off

- [x] All three repo-visible environments (local, CI, staging) compared across Python, Node, DB engine, and frontend env vars
- [x] Production scope limitation disclosed (dashboard-only, not repo-comparable) rather than silently skipped
- [x] Real drift (declared Python pin not locally enforced) documented and correctly root-caused after a QA Lead review correction (first pass Blocked — the report initially and incorrectly claimed no pin file existed at all, having searched only `docs/team_skills/` and `docs/ops/`, not `backend/`); one advisory-only gap (PUBLIC_URL) filed, not asserted as a confirmed defect without dashboard evidence
- Signed off by: PENDING — see agent-mediated review
- Date: PENDING
