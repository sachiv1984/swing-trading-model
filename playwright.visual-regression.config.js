// Dedicated Playwright config for visual-regression-baselines.spec.js
// (ST-18, BLG-QA-81, EPIC-04, v9.0).
//
// The base config (playwright.config.js) testIgnores this spec file — see
// that file's comment — because pixel-level toHaveScreenshot() baselines
// generated locally are not guaranteed to byte-match CI's ubuntu-latest
// Chromium rendering (font/anti-aliasing variance), and this repo has
// already learned that lesson once (visual-snapshots.spec.js was converted
// away from pixel snapshots for its own blocking gate for the same reason).
//
// This config re-includes exactly that one file, unmodified otherwise
// (spreads the base config), for use in a dedicated, non-blocking
// (continue-on-error: true) CI job — see .github/workflows/playwright.yml's
// playwright-visual-regression job — and for local baseline regeneration:
//   npx playwright test --config=playwright.visual-regression.config.js --update-snapshots

const baseConfig = require('./playwright.config.js');

module.exports = {
  ...baseConfig,
  testIgnore: undefined,
  testMatch: ['**/visual-regression-baselines.spec.js'],
};
