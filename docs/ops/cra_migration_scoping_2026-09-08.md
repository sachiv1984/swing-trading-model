**Owner:** Head of Engineering
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-08 (ST-50, EPIC-05, v9.2, BLG-TECH-11 — scoping document created)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Migration Off Create React App (`react-scripts` v5) — Scoping Document

## 1. Purpose

Scope a future migration off `react-scripts` v5 (Create React App). **This document is scoping only — no migration is implemented this cycle.** Filed from `BLG-TECH-11`, itself filed at ST-24 (v8.7) when the npm-audit review found 14 accept-risk advisories all confined to the `react-scripts` build-toolchain (never imported by application source), each carrying a 2027-02-16 review-by date. The durable fix for that whole advisory class is retiring the toolchain, not re-reviewing it every cycle — this document is that fix's scoping step.

## 2. Current State

- `react-scripts@^5.0.1` — CRA's last major version; upstream CRA has had no active feature development for an extended period and Meta's own React documentation no longer recommends it for new projects, recommending framework-based (Next.js/Remix) or build-tool-based (Vite) starts instead.
- Node runtime: v22.x in this environment (`node -v` → v22.23.1). CRA v5's webpack 4/5-generation tooling still runs on it but with the deprecation warnings and slow rebuild times typical of an unmaintained toolchain on a newer Node major.
- **Dual deploy targets**, each with its own asset-path handling built on CRA conventions:
  - **GitHub Pages** (`homepage: https://sachiv1984.github.io/swing-trading-model`, `npm run deploy` → `gh-pages -d build`) — relies on CRA's `PUBLIC_URL` env var and the `public/404.html` SPA-routing workaround (present in this repo, tracked in git).
  - **Render** static site — `.github/workflows/deploy.yml` explicitly overrides `PUBLIC_URL: /swing-trading-model` for the domain-root case, with an in-workflow regression check for a real past incident (`BLG-OPS-148`, 2026-08-21 GitHub Pages white-page incident) where a wrong `PUBLIC_URL` broke asset paths in production.
- Test runner: `react-scripts test` (Jest, CRA's bundled config) — only 1 `*.test.js` file exists at the top level (the Playwright E2E suite under `tests/e2e/` is the primary test investment and is toolchain-independent).
- 32 source files reference `process.env.REACT_APP_*` (37 total call sites) — CRA's required env-var prefix convention.
- No existing `craco.config.js`/webpack-eject/customization — this is an unmodified, un-ejected CRA app, which is the best-case starting position for a clean migration (no custom webpack config to port).

## 3. Target Toolchain Recommendation

**Vite**, for a React + JS (non-TypeScript) SPA of this shape:

- Most widely adopted CRA-replacement path in the current React ecosystem, with first-party "migrating from CRA" guidance and broad plugin support for everything this app already uses (React, Tailwind/PostCSS via `autoprefixer`, React Router).
- Dev-server and rebuild speed are the primary practical win — CRA's webpack-based dev server is materially slower on a codebase this size (`src/pages/` alone is dozens of route-level components).
- Does not require adopting a full meta-framework (Next.js/Remix) — this app has no SSR/server-routing requirement (it's a client-only SPA calling a separate FastAPI backend), so a meta-framework would add migration surface with no corresponding benefit; a build-tool-only swap (CRA → Vite) is the right-sized target.

## 4. Effort Estimate

**M (2–3 days)**, broken down:

| Area | Estimate | Notes |
|------|----------|-------|
| Vite project scaffold + dependency swap (`react-scripts` → `vite` + `@vitejs/plugin-react`) | 0.5d | Mechanical; `package.json` scripts (`start`/`build`/`test`) rewritten to Vite equivalents. |
| Env var rename (`REACT_APP_*` → `VITE_*`, `process.env.X` → `import.meta.env.X`) | 0.5d | 32 files, 37 call sites — mechanical find/replace but each site needs a manual look (some are conditional on `NODE_ENV` which Vite also exposes differently: `import.meta.env.MODE`/`.DEV`/`.PROD`). |
| `public/index.html` → Vite's `index.html`-as-entry-point convention; asset-path/PUBLIC_URL → Vite `base` config parity across **both** deploy targets | 0.5d | Highest-risk area — this is exactly the class of defect that caused `BLG-OPS-148`'s white-page incident under the current CRA/`PUBLIC_URL` setup. Must be verified against both GitHub Pages and Render before merge, not just one. |
| Test runner: `react-scripts test` (Jest) → decide keep-Jest-standalone vs. adopt Vitest | 0.25d | Low volume (1 top-level `*.test.js`) — low risk either way; recommend Vitest for consistency with the new build tool, but this is not a blocking decision. |
| ESLint config decoupling from `eslint-config-react-app` (currently supplied by `react-scripts`) | 0.25d | Needs its own flat-config or reuse of the project's existing top-level `eslint@9.x` devDependency directly instead of via the CRA-bundled config. |
| CI workflow updates (`.github/workflows/*.yml` referencing `npm run build`/`react-scripts`) + full staging verification pass on both deploy targets | 0.5–1d | Must re-run the full Playwright E2E suite against a Vite-built bundle before this is considered done, not just a local `npm run build` smoke check. |

## 5. Risk Areas

1. **Dual-deploy-target asset-path parity (highest risk).** GitHub Pages and Render each need correct base-path resolution under Vite's `base` config; `BLG-OPS-148` is direct, recent precedent for how easy this class of regression is to ship unnoticed (it passed `npm run build` locally and only broke in the deployed environment).
2. **Env var migration correctness.** A missed `process.env.REACT_APP_X` → `import.meta.env.VITE_X` rename fails silently (the variable reads as `undefined` rather than throwing), so this needs an explicit post-migration audit (e.g. a grep-based check with 0 remaining `REACT_APP_`/`process.env.` matches in `src/`) rather than relying on manual review alone to catch every site.
3. **CI secret/env var provisioning.** Any GitHub Actions secret or Render environment variable currently provisioned under a `REACT_APP_*` name needs a parallel `VITE_*` entry added before the cutover, not after — a mid-migration gap here breaks the build in CI/deploy even if local dev works.
4. **`eslint-config-react-app` removal side effects.** This config currently supplies React-specific lint rules (hooks rules, JSX a11y) bundled with `react-scripts` — removing `react-scripts` removes this transitively; the replacement flat-config must explicitly re-add `eslint-plugin-react-hooks` and `eslint-plugin-jsx-a11y` (or equivalents) rather than silently losing that coverage.
5. **`react-scripts` accept-risk npm-audit findings become moot, not urgently resolved, by this migration** — the 14 accept-risk advisories from `BLG-TECH-11`'s origin (ST-24) are confined to the CRA toolchain being replaced; their 2027-02-16 review-by dates can be closed once this migration ships, but only once shipped, not as a precondition of scoping it.

## 6. Recommendation

Schedule as a dedicated single-EPIC migration story (not folded into a mixed-scope sprint) once capacity allows, given the highest-risk area (§5.1) needs a full staging verification pass on both live deploy targets before merge — this is not a change that can be safely delegated as `autonomous` without a human-verified staging run on each target (per `CLAUDE.md`'s Playwright/staging-sign-off rule for observable behaviour — a broken deployed asset path is about as observable as a regression gets).

## 7. Sign-Off

**Head of Engineering:** Confirmed — scoping complete, target toolchain (Vite) and effort estimate (M, 2–3d) recorded, risk areas identified with the dual-deploy-target asset-path concern flagged as the dominant risk given direct recent precedent (`BLG-OPS-148`). No migration implementation performed this cycle, per this story's AC. 2026-09-08.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-09-08 | 1.0 | Scoping document created (ST-50, EPIC-05, v9.2, BLG-TECH-11). |
