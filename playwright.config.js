// Playwright configuration for Risk Dashboard acceptance tests
// ST-11: Canonical Test Scenario Library Phase 1 (Risk Dashboard)
// Approach: Mock Layer (page.route network interception) — agreed 2026-03-09

const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 1 : undefined,

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
