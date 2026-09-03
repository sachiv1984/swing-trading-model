// Playwright configuration for Risk Dashboard acceptance tests
// ST-11: Canonical Test Scenario Library Phase 1 (Risk Dashboard)
// Approach: Mock Layer (page.route network interception) — agreed 2026-03-09

const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  retries: process.env.CI ? 1 : 0,
  // REC-CI-01 (docs/ops/ci_pipeline_baseline.md): CI previously forced workers to 1,
  // running all specs serially. Tests are independent (page.route() mocking, no shared
  // backend/DB state), so they parallelize safely. 4 matches the vCPU count on
  // GitHub-hosted ubuntu-latest runners for this public repo.
  workers: process.env.CI ? 4 : undefined,

  // All spec files under tests/e2e/ are CI-registered — none excluded.
  // (BLG-QA-64, ST-11 EPIC-03 v6.8: last 12 dark/ignored specs resolved — 11 fixed, 1 deleted.)
  //
  // Exception (ST-18, BLG-QA-81, EPIC-04, v9.0): visual-regression-baselines.spec.js
  // uses pixel-level toHaveScreenshot(), which this repo has already found unreliable
  // as a hard-blocking gate — visual-snapshots.spec.js itself was originally
  // pixel-snapshot based and was deliberately converted to CSS class/attribute
  // assertions for exactly this reason (see that file's header comment: "Chromium
  // version differences cause pixel mismatches" across local/CI environments).
  // Baselines here are generated locally, not on the actual CI runner, so a first
  // CI run is likely to diff on font-rendering/anti-aliasing even with the 2%
  // tolerance below. Excluded from the default/blocking glob; run explicitly via
  // playwright.visual-regression.config.js in a dedicated advisory-only CI job
  // (.github/workflows/playwright.yml's playwright-visual-regression job) instead.
  testIgnore: ['**/visual-regression-baselines.spec.js'],

  // Visual snapshot configuration
  // Baseline PNGs live in tests/e2e/__snapshots__/ (committed to repo).
  // To generate or refresh baselines: npx playwright test tests/e2e/visual-snapshots.spec.js --update-snapshots
  snapshotDir: 'tests/e2e/__snapshots__',
  snapshotPathTemplate: '{snapshotDir}/{testFilePath}/{arg}-{projectName}{ext}',
  expect: {
    toHaveScreenshot: {
      // 2% pixel difference tolerance — handles minor font-rendering and
      // anti-aliasing variation across OS/CI environments.
      maxDiffPixelRatio: 0.02,
      // Disable CSS animations before capturing so shimmer/spin states
      // produce consistent pixel output.
      animations: 'disabled',
    },
  },

  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    viewport: { width: 1280, height: 900 },
    // API calls go to API_BASE_URL (localhost:8000 by default).
    // Tests intercept these via page.route() — no live backend required.
    // bypassCSP: public/index.html has connect-src 'self' https: which blocks
    // http://localhost:8000 (cross-port, non-https). Playwright must bypass CSP
    // so page.route() interceptors can fulfill API requests in tests.
    bypassCSP: true,
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  webServer: {
    // ST-09 (BLG-QA-127, EPIC-03, v7.10): CI serves a production build instead
    // of the CRA dev server. CRA bakes REACT_APP_* vars into the bundle at
    // build time (not serve time), so the same `env` block below applies to
    // both the `npm run build` step and the `serve` step in the CI command —
    // build reads them via webpack DefinePlugin substitution, serve ignores
    // them (static assets already built). Local/non-CI dev keeps `npm start`
    // for live-reload, unaffected.
    //
    // Two build-only overrides, both confirmed necessary by a real local
    // build+serve dry run before this was wired into CI:
    // - `CI=false` on the build sub-command only: react-scripts treats ESLint
    //   warnings as build-breaking errors whenever process.env.CI is truthy
    //   (GitHub Actions sets CI=true on every job) — this repo has many
    //   pre-existing warnings, unrelated to this story, that would otherwise
    //   fail every build. The outer CI=true (used by this file's own
    //   `process.env.CI` checks below, and by retries/workers) is untouched.
    // - `PUBLIC_URL=/`: package.json's `homepage` field
    //   (https://sachiv1984.github.io/swing-trading-model) makes an
    //   unqualified build emit asset URLs under `/swing-trading-model/...`
    //   (for the real gh-pages deploy) — which 404s when served at the
    //   webServer's actual root (http://localhost:3000/). PUBLIC_URL=/
    //   overrides this for the throwaway E2E build only.
    command: process.env.CI
      ? 'CI=false PUBLIC_URL=/ npm run build && npx serve -s build -l 3000'
      : 'npm start',
    port: 3000,
    reuseExistingServer: !process.env.CI,
    // CI needs a longer timeout: a fresh production build (react-scripts build)
    // takes materially longer to become ready than the dev server's fast-refresh
    // startup that the 120000ms default was tuned for.
    timeout: process.env.CI ? 300000 : 120000,
    env: {
      // Ensure deterministic API base URL for route interception
      REACT_APP_API_URL: 'http://localhost:8000',
      REACT_APP_DEV_FAKE_AUTH: 'true',
      // Gates the "Improve with AI" button's client-side HAS_AI check
      // (src/pages/TradePlan.js) so it renders in tests. The real
      // POST /trade-plans/generate-plan call is always intercepted via
      // page.route() — this value is never used to call a live API.
      REACT_APP_ANTHROPIC_API_KEY: 'playwright-ui-gate-only',
      BROWSER: 'none',
      // eslint.config.mjs (ESLint v9 flat config) conflicts with react-scripts'
      // eslint-config-react-app loader; disabling prevents the webpack error
      // overlay from blocking Playwright pointer events in all tests.
      DISABLE_ESLINT_PLUGIN: 'true',
    },
  },

  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['list'],
  ],
});
