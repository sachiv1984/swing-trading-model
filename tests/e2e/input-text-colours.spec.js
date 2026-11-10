/**
 * Input Text Colours — ST-10 (EPIC-03, v9.16) — BLG-FE-223
 *
 * Inputs carried `placeholder:text-slate-600 dark:text-slate-400`. The `dark:`
 * variant there colours the typed text, not the placeholder, so typed values
 * rendered dim slate-400 in the dark theme. ST-10 moves every such site to the
 * design_system.md v1.25 §Input Text Colours pair: placeholder
 * `placeholder:text-slate-600 dark:placeholder:text-slate-400`, typed text
 * `text-app-fg` (the ST-09 semantic token).
 *
 *   SC-ITC-01  Trade Entry ticker input, dark theme: typed text computes to
 *              white rgb(255, 255, 255), and passes 4.5:1 against the
 *              input's rendered background
 *   SC-ITC-02  Trade Entry ticker input, light theme: typed text computes to
 *              slate-900 rgb(15, 23, 42), and passes 4.5:1 against the
 *              input's rendered background
 *   SC-ITC-03  Edit Position modal notes textarea, light theme: slate-900,
 *              passes 4.5:1 against the modal
 *   SC-ITC-04  Exit modal notes textarea, light theme: slate-900, passes 4.5:1
 *
 * The grep half of the AC (`grep -rnE 'placeholder:text-[a-z]+-[0-9]+ +dark:text-' src/`
 * returns nothing) is code-level and is recorded in qa_evidence_EPIC-03.md.
 *
 * Design source: docs/design/2026-11-06__release-v9.16/semantic-colour-tokens/decision_record.md §2.3, §6
 * Spec ref: docs/specs/frontend/design_system.md §Input Text Colours (v1.25)
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) => {
    const url = route.request().url();
    if (/\/positions(\?|$)/.test(url)) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
  });
}

// Reads the input's typed-text colour and composites every background layer
// from the page root down to the input, so a translucent input fill (e.g.
// bg-slate-800/50) is measured as it actually renders. A gradient
// background-image paints over its element's background colour, so each of its
// colour stops is carried forward as a candidate background (EPIC-03 review
// pass 1: the first version skipped background-image and measured the light
// page instead of the dark Trade Entry card). Returns the WCAG 2.1 contrast
// ratio against the worst candidate.
async function typedTextContrast(input) {
  return input.evaluate((el) => {
    const parse = (c) => {
      const m = c.match(/rgba?\(([^)]+)\)/);
      if (!m) return null;
      const parts = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
      return { r: parts[0], g: parts[1], b: parts[2], a: parts.length > 3 ? parts[3] : 1 };
    };
    const over = (c, bg) => ({
      r: c.r * c.a + bg.r * (1 - c.a),
      g: c.g * c.a + bg.g * (1 - c.a),
      b: c.b * c.a + bg.b * (1 - c.a),
    });
    const chain = [];
    for (let n = el; n; n = n.parentElement) chain.unshift(n);
    let candidates = [{ r: 255, g: 255, b: 255 }];
    for (const n of chain) {
      const cs = getComputedStyle(n);
      const c = parse(cs.backgroundColor);
      if (c && c.a > 0) candidates = candidates.map((bg) => over(c, bg));
      const stops = (cs.backgroundImage.match(/rgba?\([^)]+\)/g) || []).map(parse).filter(Boolean);
      if (stops.length > 0) {
        candidates = stops.flatMap((s) => candidates.map((bg) => over(s, bg)));
      }
    }
    const fgRaw = getComputedStyle(el).color;
    const fg = parse(fgRaw);
    const lum = ({ r, g, b }) => {
      const ch = (v) => {
        const s = v / 255;
        return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
      };
      return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b);
    };
    const ratio = (bg) => {
      const [hi, lo] = [lum(fg), lum(bg)].sort((a, b) => b - a);
      return (hi + 0.05) / (lo + 0.05);
    };
    return { color: fgRaw, ratio: Math.min(...candidates.map(ratio)) };
  });
}

for (const [id, theme, expected] of [
  ['SC-ITC-01', 'dark', 'rgb(255, 255, 255)'],
  ['SC-ITC-02', 'light', 'rgb(15, 23, 42)'],
]) {
  test(`${id}: Trade Entry typed text uses the app-fg token in the ${theme} theme`, async ({ page }) => {
    await mockFallback(page);
    await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    await page.goto('/#/TradeEntry');

    const input = page.getByPlaceholder('e.g., AAPL or VOD.L');
    await expect(input).toBeVisible({ timeout: 10000 });
    if (theme === 'dark') {
      await expect(page.locator('html')).toHaveClass(/\bdark\b/);
    } else {
      await expect(page.locator('html')).not.toHaveClass(/\bdark\b/);
    }
    await input.fill('AAPL');

    await expect(input).toHaveCSS('color', expected);
    const { ratio } = await typedTextContrast(input);
    expect(ratio).toBeGreaterThanOrEqual(4.5);
  });
}

// SC-ITC-03/04 (EPIC-03 review pass 1): the Position and Exit modals had the
// same defect as the Trade Entry card - a dark-only DialogContent around the
// inputs. Both are opened from the Positions table and checked in light.
const ITC_POSITION = {
  id: 'pos-itc-1', ticker: 'WDC', market: 'US', entry_price: 100, current_price: 92.31,
  current_price_native: 120, initial_stop: 80, current_trailing_stop: 76.92,
  current_trailing_stop_native: 100, stop_price: 76.92, stop_price_native: 100, shares: 10,
  pnl: 153.85, pnl_percent: 20, holding_days: 15, grace_days_remaining: null, status: 'open',
  entry_date: '2026-07-25', tags: null,
};

for (const [id, button, placeholder] of [
  ['SC-ITC-03', 'Edit WDC', "Why are you entering this trade? What's your thesis?"],
  ['SC-ITC-04', 'Exit WDC', 'How did the trade play out? What did you learn?'],
]) {
  test(`${id}: ${button.split(' ')[0]} modal typed text passes contrast in the light theme`, async ({ page }) => {
    await mockFallback(page);
    await page.route(new RegExp(`${API}/positions(\\?|$)`), (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([ITC_POSITION]) })
    );
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
    await page.goto('/#/positions');
    const tableBtn = page.locator('[aria-label="Table view"]');
    await tableBtn.waitFor({ state: 'visible', timeout: 10000 });
    await tableBtn.click();
    await page.getByRole('button', { name: button }).click();
    if (button.startsWith('Edit')) {
      // The Edit Position modal shows the journal read-only until its Edit toggle.
      await page.getByRole('dialog').getByRole('button', { name: 'Edit', exact: true }).click();
    }

    const input = page.getByPlaceholder(placeholder);
    await expect(input).toBeVisible({ timeout: 10000 });
    await input.fill('Typed note');

    await expect(input).toHaveCSS('color', 'rgb(15, 23, 42)');
    const { ratio } = await typedTextContrast(input);
    expect(ratio).toBeGreaterThanOrEqual(4.5);
  });
}
