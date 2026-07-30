**Owner:** QA & Testing Owner
**Class:** Team Skills Reference (Class 4)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-07-30
**Created by:** Post-ship closure 2026-04-13__release-v2.7 — ST-06 fix codified (Phase 3 lessons learnt, Obs 4)

---

# Playwright Testing Patterns — Momentum Trading Assistant

This document codifies tested Playwright patterns for the e2e test suite. All new Playwright spec files should follow these patterns.

---

## 1. Route Registration Order (LIFO Fix — ST-06 root cause)

**Pattern: Register catch-all routes FIRST, specific mocks AFTER.**

Playwright uses a Last-In-First-Out (LIFO) registration order for `page.route()`. Routes registered last take priority. This means:

- If you register a catch-all route (`**`) LAST, it intercepts all requests and overrides all specific mocks.
- If you register a catch-all route FIRST, specific mocks registered after it take priority (because they were registered later → higher LIFO priority).

### Correct pattern

```js
// CORRECT: catch-all registered FIRST (lower LIFO priority)
await page.route('**', route => route.abort()); // catch-all: block all unmocked requests

// Specific mocks registered AFTER (higher LIFO priority — takes precedence)
await page.route('**/api/portfolio', route => {
  route.fulfill({ status: 200, body: JSON.stringify(mockPortfolio) });
});

await page.route('**/api/trades', route => {
  route.fulfill({ status: 200, body: JSON.stringify(mockTrades) });
});
```

### Incorrect pattern (DO NOT USE)

```js
// INCORRECT: catch-all registered LAST (highest LIFO priority — overrides all specific mocks)
await page.route('**/api/portfolio', route => {
  route.fulfill({ status: 200, body: JSON.stringify(mockPortfolio) });
});

await page.route('**', route => route.abort()); // THIS WILL INTERCEPT EVERYTHING — mocks above are ignored
```

### Root cause (ST-06 investigation)

Discovered during v2.7 EPIC-03 (ST-06). All Playwright specs using `page.route()` were failing because the catch-all was registered last, causing it to intercept requests before specific mock routes could handle them. The React app received no mock data and rendered empty/zero state.

**Fix applied to all specs:** `reports-performance-tab.spec.js`, `slippage-tracking.spec.js`, `fee-drag-trade-history.spec.js`, `signals-cash-balance.spec.js`, `system-status.spec.js`. All 46 tests pass after fix.

---

## 2. HashRouter Navigation

Use `page.goto()` with the full hash path for HashRouter-based apps:

```js
await page.goto('http://localhost:3000/#/trade-history');
```

Not just `http://localhost:3000/` — the hash route must be explicit.

---

## 3. Cache Clearing Between Tests

To avoid stale React Query cache between tests in the same spec file, navigate to `about:blank` before the next test:

```js
afterEach(async ({ page }) => {
  await page.goto('about:blank');
});
```

This ensures React Query's in-memory cache is cleared between test cases.

---

## 4. waitForSelector Before Assertions

Always wait for a reliable selector before asserting table or dynamic content:

```js
await page.waitForSelector('table');
// then assert specific rows/cells
```

This prevents race conditions where assertions run before the component has rendered.

---

## 5. Strict Mode Violations

If Playwright's strict mode fires (multiple elements match a locator), use `first()` or a more specific selector:

```js
// Strict mode violation — multiple elements match
await page.getByRole('cell', { name: 'AAPL' }).click(); // FAILS if multiple rows

// Fix: use .first() or more specific context
await page.getByRole('row').filter({ hasText: 'AAPL' }).getByRole('cell', { name: 'AAPL' }).click();
```

---

## 6. Test Tagging Convention (smoke / regression / critical)

**Origin:** ST-11 (BLG-QA-120, EPIC-03, v8.0) — introduced to enable selective CI runs instead of always executing the full suite.

Every Playwright test should carry exactly one tier tag, passed as the second argument to `test()`:

```js
test('PATH-1: add trade — form submits and POST /portfolio/position fires', { tag: '@smoke' }, async ({ page }) => {
  // ...
});
```

Multiple tags are allowed where a test also serves another designated purpose (e.g. the existing `@epic-merge-smoke` designation from `shared_standards.md §12` Rule 3):

```js
test('...', { tag: ['@epic-merge-smoke', '@smoke'] }, async ({ page }) => { ... });
```

### Tiers

| Tag | Meaning | When it runs |
|-----|---------|---------------|
| `@smoke` | Minimal, fast, critical-path subset — must stay green on every push. Currently `tests/e2e/smoke-critical-paths.spec.js`'s 3 tests. | Every push to `main`/`exec/**` (`.github/workflows/smoke-tests.yml`) |
| `@critical` | Business-critical flows beyond the smoke tier (e.g. compliance gating, risk checks) that should never regress silently. | Every PR to `main` |
| `@regression` | The remainder of the suite — full behavioural coverage. Untagged tests are treated as this tier by default. | Every PR to `main` (`.github/workflows/playwright.yml`, sharded) |

### Selective run

Filter by tag with Playwright's built-in `--grep`:

```bash
npx playwright test --grep @smoke
npx playwright test --grep @critical
npx playwright test --grep "@smoke|@critical"
```

`.github/workflows/smoke-tests.yml` runs `--grep @smoke` rather than a hardcoded spec path, so any spec file that adds a `@smoke`-tagged test is picked up automatically without a workflow edit.

**Retroactive tagging is not required.** Apply `@critical`/`@regression` tags at next-touch of a spec file, following the same incremental-adoption pattern as the Array Guard Standard (`shared_standards.md §19`) — this is not retroactively enforced as a blanket requirement across the existing suite.

---

*For defect lifecycle guidance, see `docs/team_skills/quality/defect_lifecycle.md`.*
