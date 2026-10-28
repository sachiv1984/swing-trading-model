/**
 * Suite-wide API status guard (ST-24, EPIC-04, v9.13, BLG-QA-227).
 *
 * Every spec in tests/e2e/ takes `test` and `expect` from this module, not
 * from '@playwright/test' directly (tests/test_e2e_api_status_guard_applied.py
 * enforces that). This module re-exports all of '@playwright/test' and
 * extends `test` with an automatic fixture that fails the test when any
 * response from the app's own API origin is a 404 or 405.
 *
 * Why: the Daily Position Monitor called `PATCH /positions/{id}`, a route
 * that does not exist (BLG-FE-226). Mocks answered it, or nothing asserted
 * on it, so the suite stayed green. A 404/405 from the API now fails the
 * test that caused it, whether the response came from a page.route() mock
 * or a catch-all handler.
 *
 * Scope: responses on any page in the test's `context` whose origin is
 * API_ORIGIN. Pages opened from a separately created browser context
 * (browser.newContext()) are not covered.
 *
 * Intentional probes: a test that expects a 404/405 (for example "no trade
 * plan for this trade" is a 404 by contract) declares it with
 *
 *   test.use(allowApiErrors({ status: 404, method: 'GET', path: /^\/trades\/[^/]+\/plan$/ }));
 *
 * at file or describe level. allowApiErrors wraps the entries in an object
 * because Playwright reads an array passed to test.use() as a
 * [value, options] tuple, which would drop the second entry. `status` and
 * `path` are required; `path` is a
 * RegExp tested against the URL pathname, or an exact pathname string.
 * `method` is optional. Keep each entry as narrow as the probe it covers.
 *
 * Coverage log: with API_CALL_LOG=<file> set, every POST/PUT/PATCH/DELETE
 * request the app sends to API_ORIGIN is appended to <file> as a JSON line
 * ({ method, path, spec, title }), whether or not a mock answers it. This is
 * how the state-changing action inventory in
 * docs/testing/state_changing_action_coverage.md is regenerated. It is off by
 * default and never fails a test.
 */
const fs = require('fs');
const path = require('path');
const base = require('@playwright/test');

// Matches REACT_APP_API_URL in playwright.config.js's webServer env.
const API_ORIGIN = 'http://localhost:8000';
const GUARDED_STATUSES = new Set([404, 405]);
const STATE_CHANGING = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

function allowApiErrors(...entries) {
  return { allowedApiErrors: { entries } };
}

function isAllowed(allowList, status, method, pathname) {
  return allowList.entries.some((entry) =>
    entry.status === status &&
    (!entry.method || entry.method.toUpperCase() === method) &&
    (entry.path instanceof RegExp ? entry.path.test(pathname) : entry.path === pathname)
  );
}

const test = base.test.extend({
  allowedApiErrors: [{ entries: [] }, { option: true }],

  apiStatusGuard: [
    async ({ context, allowedApiErrors }, use, testInfo) => {
      const violations = [];
      const onRequest = (request) => {
        const url = new URL(request.url());
        if (url.origin !== API_ORIGIN || !STATE_CHANGING.has(request.method())) return;
        fs.appendFileSync(process.env.API_CALL_LOG, JSON.stringify({
          method: request.method(), path: url.pathname,
          spec: path.basename(testInfo.file), title: testInfo.title,
        }) + '\n');
      };
      const onResponse = (response) => {
        const status = response.status();
        const url = new URL(response.url());
        if (url.origin !== API_ORIGIN) return;
        const method = response.request().method();
        if (!GUARDED_STATUSES.has(status)) return;
        if (isAllowed(allowedApiErrors, status, method, url.pathname)) return;
        violations.push(`${status} ${method} ${url.pathname}`);
      };
      if (process.env.API_CALL_LOG) context.on('request', onRequest);
      context.on('response', onResponse);
      await use(violations);
      context.off('response', onResponse);
      if (process.env.API_CALL_LOG) context.off('request', onRequest);
      if (violations.length) {
        throw new Error(
          `API status guard (ST-24): the app received ${violations.length} 404/405 response(s) ` +
          `from ${API_ORIGIN}:\n  ${violations.join('\n  ')}\n` +
          'Fix the call or the mock. If the status is an intentional probe, declare it with ' +
          "test.use(allowApiErrors(...)) — see tests/e2e/fixtures/api-status-guard.js."
        );
      }
    },
    { auto: true },
  ],
});

module.exports = { ...base, test, expect: base.expect, API_ORIGIN, allowApiErrors };
