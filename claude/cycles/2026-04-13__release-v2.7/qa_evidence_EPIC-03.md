# QA Evidence — EPIC-03: Test Infrastructure
**Cycle:** 2026-04-13__release-v2.7
**Branch:** exec/2026-04-13__release-v2.7/EPIC-03
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Status:** Complete — awaiting PR merge

---

## Story Sign-off Blocks

---

### ST-06 — Fix Playwright page.route() intercepts not firing

**Commit:** `3489bb4` + `975fe6f` (SC-SIG-CB-01a fix in ST-06/ST-07 combined commit)
**Verification method:** Playwright headless Chromium run — `npx playwright test tests/e2e/fee-drag-trade-history.spec.js tests/e2e/slippage-tracking.spec.js tests/e2e/signals-cash-balance.spec.js tests/e2e/reports-performance-tab.spec.js`
**Result:** 30/30 pass

| AC | Result | Evidence |
|----|--------|----------|
| Root cause identified and documented | Pass | Root cause: Playwright `page.route()` uses LIFO (last-in-first-out) handler ordering. The catch-all `mockFallback` was registered _last_ in all 4 specs, causing it to fire _first_ and override every specific mock. Fix: register catch-all _first_ so specific mocks registered after take precedence. Documented as inline comments in each fixed spec file. |
| `reports-performance-tab.spec.js` — all 11 tests pass | Pass | Playwright run output: 11/11 pass. Additional fixes applied: `waitForSelector('button')` → `waitForLoadState('networkidle')` (first disabled sidebar button causes false timeout); `getByText('8')` → `getByText('8', { exact: true }).first()` (strict-mode violation); XPath sibling locator for SC-REP-04c Profit Factor value; delayed-route ordering for SC-REP-03a loading state. |
| `slippage-tracking.spec.js` — all 8 tests pass | Pass | Playwright run output: 8/8 pass. Additional fixes: mock trade `pnl_percent` → `pnl_pct` (component calls `.toFixed()` on `trade.pnl_pct`; undefined caused render crash); `getByRole('button', { name: /slippage/i })` → `getByRole('columnheader', { name: /slippage/i })` (`TableHead` renders as `<th>`, ARIA role `columnheader` not `button`); `.first()` on em-dash locators to resolve strict-mode violation. |
| `fee-drag-trade-history.spec.js` — all 7 tests pass | Pass | Playwright run output: 7/7 pass. Same `pnl_pct` and `columnheader` fixes applied. SC-FEE-02b `.first()` added; SC-FEE-04b scoped to `page.locator('table')` to resolve strict-mode violation. |
| `signals-cash-balance.spec.js` — all 4 tests pass | Pass | Playwright run output: 4/4 pass. SC-SIG-CB-01a rewritten: `page.goto('about:blank')` before `goto('/#/Signals')` to fully clear React Query cache (hash-only navigation keeps SPA mounted, preventing re-fetch); `page.on('request')` listener replaces `waitForRequest` for more reliable capture. SC-SIG-CB-02a/02b: `getByText('£0', { exact: true }).first()`. |
| Fix pattern documented for future specs | Pass | Pattern documented in all 4 spec file header comments: "LIFO ordering: catch-all registered FIRST so specific mocks take precedence." Pattern reused in ST-07 spec without deviation. |

**DoQ Sign-off:** Pass — all 5 AC verified by Playwright headless Chromium execution. Root cause fully explained and reproducible fix applied consistently across all 4 spec files.

---

### ST-07 — System Status Playwright spec

**Commit:** `975fe6f`
**Spec file:** `tests/e2e/system-status.spec.js`
**Verification method:** Playwright headless Chromium run — `npx playwright test tests/e2e/system-status.spec.js`
**Result:** 16/16 pass

| AC | Result | Evidence |
|----|--------|----------|
| `tests/e2e/system-status.spec.js` exists covering category routing and count display | Pass | File created at `tests/e2e/system-status.spec.js` (354 lines). Covers SC-SS-01 through SC-SS-07. |
| Mock `POST /test/endpoints` with ≥1 endpoint per: `/alerts/rules`, `/notifications`, `/digest/weekly` | Pass | `TEST_RESULTS_RESPONSE` (lines 41–103) contains 28 endpoints including `GET /alerts/rules`, `POST /alerts/rules`, `DELETE /alerts/rules/1`, `GET /notifications`, `POST /notifications`, `PUT /notifications/1`, `GET /digest/weekly`, `POST /digest/weekly`, `GET /digest/monthly`. |
| Assert: Alerts section visible after tests run | Pass | SC-SS-03a: `getByRole('button', { name: /^alerts/i })` visible. SC-SS-03b: button accessible name includes "3/3" badge — asserted via `/^alerts.*3\/3/i`. |
| Assert: Notifications section visible after tests run | Pass | SC-SS-04a/04b: same pattern, accessible name `/^notifications.*3\/3/i`. |
| Assert: Digest section visible after tests run | Pass | SC-SS-05a/05b: same pattern, accessible name `/^digest.*3\/3/i`. |
| Assert: total endpoint count shown ≥ 26 | Pass | SC-SS-06a: `summary.total = 28` — `span.filter('Total:')` sibling text asserted as "28". SC-SS-06b: sub-header text "Testing 28 endpoints across all system modules" asserted. |
| Assert: none of alerts/notifications/digest endpoints appear under "Other" | Pass | SC-SS-07a: `getByRole('button', { name: /^other/i })` asserted not visible (no endpoints fall through to Other). SC-SS-07b–07d: specific endpoint texts `GET /alerts/rules`, `GET /notifications`, `GET /digest/weekly` visible in page (within their correct category sections). |
| All assertions pass in headless Chromium using ST-06 fix pattern | Pass | 16/16 pass. Catch-all LIFO pattern applied: `mockFallback` registered first in `mockBaseEndpoints`; `mockHealth` and `mockTestEndpoints` registered after. |

**Deviation noted:** Category toggle button accessible name includes the count badge (e.g. "Alerts 3/3"), not just the category name. Tests use prefix-match regex `/^alerts/i` instead of exact match. This is correct behaviour — the badge is part of the button's accessible content. No spec deviation.

**DoQ Sign-off:** Pass — all 6 AC verified by Playwright headless Chromium execution. 16/16 tests pass in headless Chromium. ST-06 fix pattern applied without deviation.

---

## Consolidation

| Story | Status | Commit SHA | Tests |
|-------|--------|------------|-------|
| ST-06 | Pass | 3489bb4, 975fe6f | 30/30 |
| ST-07 | Pass | 975fe6f | 16/16 |

**EPIC-03 QA Sign-off:** ✅ All stories pass. 46 Playwright scenarios verified in headless Chromium. Ready for PR.

---

## QA Sign-off Block

- [x] All acceptance criteria verified against canonical spec (Playwright headless execution)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (existing scenarios pass with ST-06 fix applied)
- [x] For any frontend component making direct URL construction: N/A — test infrastructure changes only
- Signed off by: Director of Quality
- Date: 2026-04-15
- Comments: ST-06: 30/30 Playwright scenarios pass; root cause (LIFO route ordering) fixed across all 4 spec files. ST-07: 16/16 scenarios pass; 28-endpoint mock verified. ST-06 fix pattern applied consistently.
