**Owner:** QA & Testing Owner
**Class:** Team Skills Reference (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-16
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

*For defect lifecycle guidance, see `docs/team_skills/quality/defect_lifecycle.md`.*
