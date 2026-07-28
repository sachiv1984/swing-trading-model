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
    command: 'npm start',
    port: 3000,
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
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
