**Owner:** QA Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-29
**Cycle:** 2026-07-28__release-v7.10 (ST-09 — BLG-QA-127)

---

# Playwright E2E: Production Build Instead of CRA Dev Server

## Purpose

ST-09 (BLG-QA-127): serve a production build for the Playwright E2E `webServer` in CI instead of the CRA dev server, since the dev server's compile/serve overhead is paid on every one of the 382 `page.goto()` navigations across the 677-test suite.

## Change

- `package.json`: added `serve` as a pinned (exact version, no caret) devDependency — `14.2.6`.
- `playwright.config.js`: `webServer.command` is now CI-conditional — `CI=false PUBLIC_URL=/ npm run build && npx serve -s build -l 3000` in CI, `npm start` otherwise (local dev keeps live-reload, unaffected). `webServer.timeout` raised to 300000ms in CI (a fresh production build takes materially longer than dev-server startup).

## Two build-breaking issues found and fixed during implementation (not present in the naive `npm run build && serve` approach)

Both were confirmed via a real local build+serve dry run (`npm run build`, then `curl` against the served output) before being wired into CI — this is not theoretical.

**1. `CI=true` makes CRA treat ESLint warnings as build-breaking errors.** `react-scripts build` checks `process.env.CI` and, when truthy, escalates every ESLint warning to a compile error. GitHub Actions sets `CI=true` on every job automatically. This repo has a substantial number of pre-existing `no-unused-vars`/`jsx-a11y` warnings across many files, unrelated to this story — with a naive `npm run build` inside a CI job, **every single CI run would fail to build**, regardless of the actual test suite. Confirmed by direct reproduction: `CI=true npm run build` → exit code 1, "Failed to compile" with a full ESLint error dump; `CI=false npm run build` → exit code 0, identical output otherwise. **Fix:** the build sub-command in `webServer.command` explicitly sets `CI=false` for that one process only — the outer `CI=true` (used by this same config file's own `retries`/`workers`/`reuseExistingServer` checks, and by the shard-selection logic in `playwright.yml`) is untouched.

**2. `package.json`'s `homepage` field breaks asset paths when served at a different root.** `"homepage": "https://sachiv1984.github.io/swing-trading-model"` makes an unqualified `react-scripts build` emit all asset URLs under `/swing-trading-model/...` (correct for the real gh-pages deploy, where the app IS hosted at that subpath). Serving that same build at `http://localhost:3000/` (webServer's actual root) would 404 on every JS/CSS asset — the page would load an empty shell with no bundle, silently breaking every single Playwright test that needs the app rendered. Confirmed by inspecting the built `index.html`'s `<script src>`/`<link href>` before and after the fix. **Fix:** `PUBLIC_URL=/` on the build sub-command overrides the `homepage`-derived public path for this throwaway E2E build only — verified via `curl` that `index.html`, the JS bundle, and the CSS bundle all resolve with HTTP 200 at their emitted root-relative paths after the fix.

## Verification performed

- Local dry run of the exact CI command string (`CI=false PUBLIC_URL=/ npm run build && npx serve -s build -l <port>`): build succeeds (exit 0), server starts, `index.html` returns 200, JS/CSS bundles resolve at their emitted paths (200), and an arbitrary client-side route (`/some/spa/route`) correctly falls back to `index.html` (200) — confirming `serve -s` (SPA mode) is compatible with `react-router-dom`.
- Confirmed `REACT_APP_API_URL`/`REACT_APP_DEV_FAKE_AUTH`/`REACT_APP_ANTHROPIC_API_KEY` are baked into the built bundle (grepped the compiled JS for the injected value).
- **Not performed locally:** running the actual 677-test Playwright suite against the served build (RISK-04) — this sandbox's OS is not supported by Playwright's browser installer (`ERROR: Playwright does not support chromium on ubuntu26.04-x64`), so `npx playwright install --with-deps chromium` cannot succeed here. This is verified instead by the real `playwright.yml` CI workflow, which runs on a supported `ubuntu-latest` GitHub-hosted runner and is triggered automatically by this change (both `playwright.config.js` and any `src/**`/`tests/e2e/**` changes are in that workflow's path filters).

## Disposition

No P0/P1 gap — both issues found were fixed within this story before the change was pushed, not deferred. `playwright.yml` itself required no changes: `webServer.command`'s CI branch is invoked automatically by Playwright's own `webServer` lifecycle when `npx playwright test` runs inside the existing CI job, using the `CI: true` env var the workflow already sets.
