/**
 * E2E: API status guard self-test — ST-24 (EPIC-04, v9.13, BLG-QA-227)
 *
 * Proves the suite-wide fixture in fixtures/api-status-guard.js fails a test
 * on a 404/405 from the app's API origin, honours its allow-list, and
 * ignores the same statuses from other origins.
 *
 * Scenarios: SC-ASG-01 through SC-ASG-05
 */
const { test, expect, API_ORIGIN, allowApiErrors } = require('./fixtures/api-status-guard');

async function fetchFromPage(page, url, method) {
  return page.evaluate(
    async ([u, m]) => (await fetch(u, { method: m })).status,
    [url, method]
  );
}

test.describe('API status guard (ST-24)', () => {
  test.beforeEach(async ({ page }) => {
    await page.route(`${API_ORIGIN}/guard-probe/**`, (route) =>
      route.fulfill({ status: 405, contentType: 'application/json', body: JSON.stringify({ detail: 'Method Not Allowed' }) })
    );
    await page.route('http://other-origin.test/**', (route) =>
      route.fulfill({ status: 404, contentType: 'application/json', body: '{}' })
    );
    // about:blank has an opaque origin; load a page from the app so fetch() is a normal CORS request.
    await page.route('http://localhost:3000/guard-host', (route) =>
      route.fulfill({ status: 200, contentType: 'text/html', body: '<html><body>guard host</body></html>' })
    );
    await page.goto('/guard-host');
  });

  test('SC-ASG-01: a deliberate 405 from the API origin fails the test', async ({ page }) => {
    // test.fail(): this test passes only if the guard fails it.
    test.fail();
    expect(await fetchFromPage(page, `${API_ORIGIN}/guard-probe/positions/1`, 'PATCH')).toBe(405);
  });

  test('SC-ASG-02: the guard records the method, path and status of the violation', async ({ page, apiStatusGuard }) => {
    await fetchFromPage(page, `${API_ORIGIN}/guard-probe/signals`, 'POST');
    expect(apiStatusGuard).toEqual(['405 POST /guard-probe/signals']);
    // Clear it so this test, which asserts on the record, does not itself fail.
    apiStatusGuard.length = 0;
  });

  test.describe('with an allow-list entry', () => {
    test.use(allowApiErrors({ status: 405, method: 'PATCH', path: /^\/guard-probe\/positions\/[^/]+$/ }));

    test('SC-ASG-03: an allow-listed probe does not fail the test', async ({ page, apiStatusGuard }) => {
      expect(await fetchFromPage(page, `${API_ORIGIN}/guard-probe/positions/1`, 'PATCH')).toBe(405);
      expect(apiStatusGuard).toEqual([]);
    });
  });

  test.describe('with two allow-list entries', () => {
    // Regression: an array passed straight to test.use() is read as a [value, options]
    // tuple, which silently dropped the second entry. allowApiErrors() keeps both.
    test.use(allowApiErrors(
      { status: 405, method: 'PATCH', path: /^\/guard-probe\/positions\/[^/]+$/ },
      { status: 405, method: 'POST', path: '/guard-probe/signals' }
    ));

    test('SC-ASG-05: every entry of a multi-entry allow-list is honoured', async ({ page, apiStatusGuard }) => {
      expect(await fetchFromPage(page, `${API_ORIGIN}/guard-probe/positions/1`, 'PATCH')).toBe(405);
      expect(await fetchFromPage(page, `${API_ORIGIN}/guard-probe/signals`, 'POST')).toBe(405);
      expect(apiStatusGuard).toEqual([]);
    });
  });

  test('SC-ASG-04: a 404 from another origin is ignored', async ({ page, apiStatusGuard }) => {
    expect(await fetchFromPage(page, 'http://other-origin.test/x', 'GET')).toBe(404);
    expect(apiStatusGuard).toEqual([]);
  });
});
