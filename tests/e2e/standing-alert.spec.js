/**
 * Standing Alert Component — Acceptance Tests — ST-04 (EPIC-04, v7.7, BLG-FE-120)
 *
 * Covers non-visual AC only. Visual AC (exact severity colours in light/dark)
 * matches design_system.md's documented light+dark class pairs, reused from
 * the existing semantic palette (no new tokens) — code-review verifiable.
 *
 * Scenarios:
 *   SC-SA-01  Component renders each severity variant with distinct icon/testid
 *   SC-SA-02  Manual dismissal removes the alert (no auto-dismiss timer)
 *   SC-SA-03  Alert does not auto-dismiss after a delay (behavioural distinction from toast)
 *   SC-SA-04  Stack caps at 3 visible with a "+N more" overflow row
 *   SC-SA-05  Clicking "+N more" expands the rest inline (no modal)
 *   SC-SA-06  role="alert" and aria-live are set correctly per severity
 *
 * Spec refs:
 *   docs/design/2026-07-21__release-v7.7/standing-alert-component/ux_spec.md
 *   docs/specs/frontend/design_system.md v1.3 §Shared UI Components → Standing Alert
 *
 * Infrastructure: test-only harness route /__test/standing-alert
 * (src/pages/__StandingAlertHarness.js) — no live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

async function gotoHarness(page) {
  await page.goto('/#/__test/standing-alert');
  await page.waitForLoadState('domcontentloaded');
}

test('SC-SA-01: renders each severity variant with distinct testid', async ({ page }) => {
  await gotoHarness(page);
  const alerts = page.getByTestId('standing-alert');
  await expect(alerts).toHaveCount(3); // capped at 3 visible (4 seeded)

  await expect(page.locator('[data-testid="standing-alert"][data-severity="info"]').first()).toBeVisible();
  await expect(page.locator('[data-testid="standing-alert"][data-severity="warning"]').first()).toBeVisible();
  await expect(page.locator('[data-testid="standing-alert"][data-severity="critical"]').first()).toBeVisible();
});

test('SC-SA-02: manual dismissal removes the alert', async ({ page }) => {
  await gotoHarness(page);
  const before = await page.getByTestId('standing-alert').count();
  await page.getByTestId('standing-alert-dismiss').first().click();
  await expect(page.getByTestId('standing-alert')).toHaveCount(before - 1);
});

test('SC-SA-03: alert persists without auto-dismissing (distinct from toast)', async ({ page }) => {
  await gotoHarness(page);
  const before = await page.getByTestId('standing-alert').count();
  // Wait past sonner's typical ~4s auto-dismiss window
  await page.waitForTimeout(5000);
  await expect(page.getByTestId('standing-alert')).toHaveCount(before);
});

test('SC-SA-04: stack caps at 3 visible with a "+N more" overflow row', async ({ page }) => {
  await gotoHarness(page);
  await expect(page.getByTestId('standing-alert')).toHaveCount(3);
  await expect(page.getByTestId('standing-alert-overflow')).toHaveText('+1 more');
});

test('SC-SA-05: clicking "+N more" expands the rest inline (no modal)', async ({ page }) => {
  await gotoHarness(page);
  await page.getByTestId('standing-alert-overflow').click();
  await expect(page.getByTestId('standing-alert')).toHaveCount(4);
  // No modal/dialog element introduced
  await expect(page.getByRole('dialog')).toHaveCount(0);
});

test('SC-SA-06: role=alert and aria-live set correctly per severity', async ({ page }) => {
  await gotoHarness(page);
  const critical = page.locator('[data-testid="standing-alert"][data-severity="critical"]').first();
  await expect(critical).toHaveAttribute('role', 'alert');
  await expect(critical).toHaveAttribute('aria-live', 'assertive');

  const info = page.locator('[data-testid="standing-alert"][data-severity="info"]').first();
  await expect(info).toHaveAttribute('aria-live', 'polite');

  const dismissBtn = page.getByTestId('standing-alert-dismiss').first();
  await expect(dismissBtn).toHaveAttribute('aria-label', 'Dismiss alert');
});
