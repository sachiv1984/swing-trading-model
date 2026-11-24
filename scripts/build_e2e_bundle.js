#!/usr/bin/env node
/*
 * ST-36 (BLG-OPS-206, EPIC-06, v9.18): build the production bundle the
 * Playwright E2E suite serves, with exactly the env in playwright.config.js's
 * webServer.env (the one source for it), plus CI=false and PUBLIC_URL=/.
 *
 * Used by:
 *   - .github/workflows/playwright.yml's build-e2e-bundle job, which builds
 *     once per run and uploads build/ for every Playwright job to serve;
 *   - playwright.config.js's CI webServer command when no prebuilt bundle is
 *     supplied (E2E_PREBUILT_BUNDLE unset), e.g. update-visual-snapshots.yml.
 * Local `npx playwright test` (no CI) still uses `npm start`.
 */
const { spawnSync } = require('child_process');
const path = require('path');

// Read the env without the CI-only command choice mattering: webServer.env is
// the same object either way.
const config = require(path.join(__dirname, '..', 'playwright.config.js'));
const env = {
  ...process.env,
  ...config.webServer.env,
  // react-scripts treats warnings as errors when CI=true; the E2E bundle never has.
  CI: 'false',
  // package.json's homepage is the GitHub Pages sub-path; the E2E server serves /.
  PUBLIC_URL: '/',
};

// npm is npm.cmd on Windows, which needs a shell to spawn.
const result = spawnSync('npm', ['run', 'build'], { stdio: 'inherit', env, shell: process.platform === 'win32' });
if (result.error) {
  console.error(`build_e2e_bundle: could not run npm: ${result.error.message}`);
}
process.exit(result.status === null ? 1 : result.status);
