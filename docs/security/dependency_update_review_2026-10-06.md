**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-10-06 (quarterly review created)
**Source:** ST-17 (`BLG-OPS-92`), EPIC-04, cycle `2026-10-06__release-v9.10`

# Quarterly Dependency Update Review — October 2026

## 1. Purpose

Review every direct dependency of the backend (`backend/requirements.txt`, 17 entries) and the frontend (`package.json`, 38 direct entries: 25 runtime, 13 dev). For each one: the installed version against the latest release, known CVEs or deprecations, and a recommended action. This is the quarterly cadence `BLG-OPS-92` set up.

The npm vulnerability half reuses `docs/security/npm_audit_rescan_triage_2026-10-06.md` and does not repeat it. Findings pinned by `react-scripts` are referred to `BLG-TECH-21` (CRA → Vite) and are not re-triaged here.

## 2. Method

- **Versions:** `pip index versions <pkg>` against PyPI, and `npm outdated --json` against the npm registry, both run 2026-10-06.
- **Vulnerabilities:** `pip-audit -r backend/requirements.txt` (no known vulnerabilities across 60 resolved packages) and `npm audit --json`. The npm result was checked with `scripts/check_dependency_vuln_rescan.py` against `docs/security/dependency_vuln_baseline.json`: **0 new HIGH/CRITICAL findings**. All 55 HIGH packages are already dispositioned in the 2026-10-06 rescan triage. Most are inherited through `react-scripts` (jest, webpack-dev-server, svgo).
- **Action key:** *None* = current. *Batch* = an in-range patch or minor bump, grouped into `BLG-TECH-22`. *Assess* = a major version, or a minor bump with known breaking changes, filed separately as `BLG-TECH-23`. *BLG-TECH-21* = handled by the CRA → Vite migration.

No upgrade is applied in this story. Each bump changes the lockfile or the pinned requirements and needs its own full CI run (the 8 Playwright shards and the pytest suite). Batching them under one backlog item gives that change a single, reviewable PR. No current version carries a known vulnerability, so nothing here is urgent.

## 3. Backend — `backend/requirements.txt` (17)

| Package | Pinned | Latest | CVEs | Action |
|---------|--------|--------|------|--------|
| fastapi | 0.135.1 | 0.142.2 | None | Batch: move with starlette |
| starlette | 1.3.1 | 1.7.0 | None | Batch: pin to the version fastapi 0.142 requires |
| uvicorn[standard] | 0.24.0 | 0.54.0 | None | Assess: 30 minor releases behind on a pre-1.0 server; check the Render start command and `--reload`/worker flags |
| pandas | 3.0.5 | 3.0.6 | None | Batch (patch) |
| numpy | 2.4.6 | 2.5.3 | None | Batch: check `utils/formatting.py`'s numpy-scalar unwrapping |
| requests | 2.34.2 | 2.34.2 | None | None |
| python-dateutil | 2.9.0.post0 | 2.9.0.post0 | None | None |
| pydantic | 2.13.4 | 2.13.5 | None | Batch (patch) |
| psycopg2-binary | 2.9.12 | 2.9.13 | None | Batch (patch) |
| sqlalchemy | 2.0.52 | 2.1.3 | None | Assess: the 2.1 series drops deprecated 2.0 APIs |
| httpx | 0.28.1 | 0.28.1 | None | None |
| anthropic | 0.105.2 | 1.11.0 | None | Assess: SDK 1.x major. Used by `ai_service.py`, `debrief_service.py`, `gemini_service.py` |
| pytest | 9.1.1 | 9.1.1 | None | None |
| pytest-cov | 7.1.0 | 7.1.0 | None | None |
| hypothesis | 6.168.4 | 6.168.5 | None | Batch (patch) |
| reportlab | 4.2.5 | 5.0.1 | None | Assess: major; used for PDF report export |
| yfinance | 1.3.0 | 1.7.0 | None | Batch, with a staging price/ATR smoke check. yfinance tracks Yahoo's changing endpoints, so falling behind risks silent data failures (see `BLG-BE-139` / ST-02's ATR fallback) |

## 4. Frontend — `package.json` runtime dependencies (25)

| Package | Range | Installed | Latest | CVEs | Action |
|---------|-------|-----------|--------|------|--------|
| @hello-pangea/dnd | ^18.0.1 | current | — | None | None |
| @radix-ui/react-checkbox | ^1.3.7 | 1.3.11 | 1.3.12 | None | Batch |
| @radix-ui/react-dialog | ^1.1.15 | 1.1.23 | 1.2.0 | None | Batch: focus-restoration Playwright specs must pass (LL-v8.3-P3-02) |
| @radix-ui/react-label | ^2.1.8 | 2.1.15 | 2.1.16 | None | Batch |
| @radix-ui/react-select | ^2.2.6 | 2.3.7 | 2.3.8 | None | Batch |
| @radix-ui/react-slot | ^1.2.4 | 1.3.3 | 1.4.0 | None | Batch |
| @radix-ui/react-switch | ^1.2.6 | 1.3.7 | 1.3.8 | None | Batch |
| @radix-ui/react-tabs | ^1.1.13 | 1.1.21 | 1.1.22 | None | Batch |
| @radix-ui/react-tooltip | ^1.2.16 | 1.2.16 | 1.3.0 | None | Batch |
| @tanstack/react-query | ^5.90.20 | 5.102.8 | 5.104.1 | None | Batch |
| class-variance-authority | ^0.7.1 | current | — | None | None |
| clsx | ^2.1.1 | current | — | None | None |
| cmdk | ^1.1.1 | current | — | None | None |
| date-fns | ^4.1.0 | current | — | None | None |
| framer-motion | ^12.29.0 | 12.43.0 | 14.0.0 | None | Assess: major. The axe scan's entrance-animation wait depends on its inline-opacity behaviour |
| lucide-react | ^0.563.0 | 0.563.0 | 1.52.0 | None | Assess: 1.x renamed icons |
| moment | ^2.30.1 | current | — | Deprecated (maintenance mode) | Assess: replace with the already-present `date-fns` |
| react | ^19.2.3 | 19.2.8 | 19.3.0 | None | Batch: move with react-dom |
| react-day-picker | ^10.0.1 | 10.0.1 | 10.0.2 | None | Batch |
| react-dom | ^19.2.3 | 19.2.8 | 19.3.0 | None | Batch |
| react-hot-toast | ^2.6.0 | 2.6.0 | 2.6.1 | None | Batch |
| react-router-dom | ^7.18.2 | 7.18.2 | 7.18.4 | None | Batch |
| react-scripts | ^5.0.1 | current (unmaintained) | — | 50+ inherited HIGH, accept-risk | BLG-TECH-21 |
| recharts | ^3.7.0 | current | — | None | None |
| sonner | ^2.0.7 | current | — | None | None |

## 5. Frontend — `package.json` dev dependencies (13)

| Package | Range | Installed | Latest | CVEs | Action |
|---------|-------|-----------|--------|------|--------|
| @axe-core/playwright | ^4.13.0 | current | — | None | None |
| @playwright/test | ^1.58.2 | 1.62.1 | 1.63.0 | None | Batch: also update the CI browser-install step |
| autoprefixer | ^10.4.23 | 10.5.5 | 10.6.1 | None | Batch |
| eslint | ^9.39.4 | 9.39.4 | 10.12.0 | None | Batch to 9.39.5 now; assess 10.x with the flat-config plugins |
| eslint-plugin-better-max-params | ^1.0.0 | current | — | None | None |
| eslint-plugin-no-comments | ^1.2.1 | current | — | None | None |
| eslint-plugin-playwright | ^2.10.4 | 2.11.0 | 2.12.1 | None | Batch |
| gh-pages | ^6.3.0 | current | — | None | None |
| postcss | ^8.5.6 | 8.5.28 | 8.5.29 | None | Batch |
| serve | 14.2.6 (exact) | current | — | `compression` override in place (rescan triage §3.1) | None |
| supabase | ^2.78.1 | 2.116.0 | 2.119.0 | None | Batch |
| tailwindcss | ^3.4.19 | 3.4.19 | 4.3.3 | None | BLG-TECH-21: the 4.x major changes the build pipeline, so do it with or after the Vite migration |
| tailwindcss-animate | ^1.0.7 | current | — | None | None |

## 6. Backlog Items Filed

- `BLG-TECH-22`: batch the in-range patch/minor bumps (backend and frontend) in one PR with full CI.
- `BLG-TECH-23`: assess the major or breaking upgrades: anthropic 1.x, SQLAlchemy 2.1, reportlab 5, uvicorn 0.54, framer-motion 14, lucide-react 1.x, eslint 10, and moment → date-fns.
- tailwindcss 4 and `react-scripts` stay with `BLG-TECH-21`.

## 7. Next Review

Next quarterly review is due **2027-01-06**, or sooner if `dependency-vuln-rescan.yml` files a new HIGH/CRITICAL finding.

## 8. Sign-off

- [x] All 17 backend entries and 38 frontend entries reviewed (current vs latest, CVEs/deprecations, action)
- [x] The npm half reuses the 2026-10-06 rescan triage; `react-scripts`-pinned findings are referred to BLG-TECH-21
- [x] Upgrades worth doing are filed as BLG-TECH-22/23. None is applied in-story.
- Prepared by: Sprint Execution Engine (autonomous; ST-17)
- Date: 2026-10-06
