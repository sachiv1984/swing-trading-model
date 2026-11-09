/**
 * Parent Links on Detail Pages — ST-02 (EPIC-01, v9.16, BLG-FE-251)
 *
 * navigation.md v2.0 §Parent Links: every page without a sidebar entry shows a
 * parent link above its page heading — a left chevron and the parent's
 * canonical label, linking to the parent route.
 *
 * Scenarios:
 *   SC-PAR-01  Trade Plan → "Trade Plans" (/TradePlans)
 *   SC-PAR-02  Research /research/:ticker → "Research" (/Research)
 *   SC-PAR-03  Notification History → "Notifications" (/notifications)
 *   SC-PAR-04  Notification Preferences → "Notifications" (/notifications)
 *   SC-PAR-05  Research error state still shows the parent link
 *   SC-PAR-06  Pages with a sidebar entry show no parent link
 *
 * Each of SC-PAR-01..04 checks: link text, href, sits above the h1, and a
 * click lands on the parent page with its heading.
 *
 * Infrastructure: page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate with page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

test.beforeEach(async ({ page }) => {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(/localhost:8000\/alerts\/history/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { evaluations: [], total: 0 } }) })
  );
  await page.route(/localhost:8000\/notifications\?/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { notifications: [], has_more: false } }) })
  );
  await page.route(/localhost:8000\/notifications\/preferences/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { preferences: [] } }) })
  );
  await page.route(/localhost:8000\/research\/AAPL/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { ticker: 'AAPL' } }) })
  );
});

const CASES = [
  { id: 'SC-PAR-01', hash: '/#/TradePlan', heading: 'Trade Plan', parent: 'Trade Plans', href: '#/TradePlans', lands: /#\/TradePlans$/, parentHeading: 'Trade Plans' },
  { id: 'SC-PAR-02', hash: '/#/research/AAPL', heading: 'AAPL — Research', parent: 'Research', href: '#/Research', lands: /#\/Research$/, parentHeading: 'Research' },
  { id: 'SC-PAR-03', hash: '/#/notifications/history', heading: 'Notification History', parent: 'Notifications', href: '#/notifications', lands: /#\/notifications$/, parentHeading: 'Notifications' },
  { id: 'SC-PAR-04', hash: '/#/notifications/preferences', heading: 'Notification Preferences', parent: 'Notifications', href: '#/notifications', lands: /#\/notifications$/, parentHeading: 'Notifications' },
];

for (const c of CASES) {
  test(`${c.id}: ${c.heading} shows a "${c.parent}" parent link that navigates correctly`, async ({ page }) => {
    await page.goto(c.hash);
    const h1 = page.getByRole('heading', { level: 1, name: c.heading, exact: true });
    await expect(h1).toBeVisible({ timeout: 15000 });

    const link = page.locator('main').getByTestId('parent-link');
    await expect(link).toHaveCount(1);
    await expect(link).toHaveText(c.parent);
    await expect(link).toHaveAttribute('href', c.href);
    await expect(link.locator('svg')).toHaveCount(1); // left chevron

    const linkBox = await link.boundingBox();
    const h1Box = await h1.boundingBox();
    expect(linkBox.y + linkBox.height).toBeLessThanOrEqual(h1Box.y + 1);

    await link.click();
    await expect(page).toHaveURL(c.lands);
    await expect(page.getByRole('heading', { level: 1, name: c.parentHeading, exact: true })).toBeVisible({ timeout: 15000 });
  });
}

test('SC-PAR-05: the Research error state still shows the parent link', async ({ page }) => {
  await page.route(/localhost:8000\/research\/ZZZZ/, (route) =>
    // 503, not 404: the api-status-guard fixture fails any test that sees a 404.
    route.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({ detail: 'unavailable' }) })
  );
  await page.goto('/#/research/ZZZZ');
  await expect(page.locator('main').getByRole('button', { name: 'Retry' })).toBeVisible({ timeout: 15000 });
  const link = page.locator('main').getByTestId('parent-link');
  await expect(link).toHaveText('Research');
  await expect(link).toHaveAttribute('href', '#/Research');
});

test('SC-PAR-06: pages with a sidebar entry show no parent link', async ({ page }) => {
  for (const [hash, heading] of [['/#/TradePlans', 'Trade Plans'], ['/#/Research', 'Research'], ['/#/notifications', 'Notifications']]) {
    await page.goto(hash);
    await expect(page.getByRole('heading', { level: 1, name: heading, exact: true })).toBeVisible({ timeout: 15000 });
    await expect(page.locator('main').getByTestId('parent-link')).toHaveCount(0);
  }
});
