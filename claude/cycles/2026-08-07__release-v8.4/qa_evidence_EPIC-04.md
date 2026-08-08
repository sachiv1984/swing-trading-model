Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-08

# QA Evidence — EPIC-04: Frontend Code Health, Accessibility & Security

**EPIC:** EPIC-04 — Frontend Code Health, Accessibility & Security
**Cycle:** 2026-08-07__release-v8.4
**Sprint goal:** Ship both available user-facing reporting enhancements while clearing a full-capacity slate of API contract & spec debt, backend hardening, frontend code health & security, operational reliability & cost monitoring, QA/test infrastructure, and governance-process integrity work across all 31 scoped stories.
**Test scenarios used:** `tests/e2e/dialog-classname-override-fixes.spec.js` (6 scenarios, new), `tests/e2e/form-validation-error-color-fixes.spec.js` (6 scenarios, new), `tests/e2e/watchlist.spec.js` (5 scenarios, existing regression)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-15 | `docs/ops/dialog_classname_override_audit_2026-08-07.md`, `tests/e2e/dialog-classname-override-fixes.spec.js` | Audited every `Dialog*` consumer for the cn()-has-no-tailwind-merge same-property override-collision defect class, using a real `tailwindcss` build (not assumed from docs) to determine actual winners. 8 genuine collisions found and fixed across 6 files (`WidgetLibrary.js`, `MonitorModal.js`, `TradeReflectionModal.js`: max-w-2xl/flex losing to base's max-w-lg/grid; `WidgetLibrary.js`, `ExportModal.js`: font-bold losing to base's font-semibold; `TradePlan.js`: rounded-2xl losing to base's responsive sm:rounded-lg at ≥640px; `WatchlistModal.js`'s DialogFooter justify-between losing to base's responsive sm:justify-end — this last fix landed in the ST-17 commit, moved into the new `WatchlistModalFooter.js`) | Every `Dialog*` consumer audited; genuine collisions listed; each fixed; no visual regression | Pass | None |
| ST-16 | `tests/e2e/form-validation-error-color-fixes.spec.js` | 13 genuine form-validation/inline-save-error instances of the bare `text-rose-400` token closed to `text-rose-700 dark:text-rose-400` across the 6 named files (`StrategyBenchmark.js`, `AlertThresholdsSection.js`, `PreferenceRow.js`, `CustomPriceAlertsSection.js`, `ProspectiveHeatPanel.js`, `SavedFiltersControl.js`), scoped to true field/save-error text (excluded: P&L/status colour indicators, load-error banners — different, out-of-scope colour usage). A fresh full-repo grep found no additional genuine instances beyond these 6 files | All genuine instances closed to the canonical token; no dark-mode regression | Pass | None |
| ST-17 | *(not applicable — lint-only fix, no prior canonical spec; verified via `npx eslint` exit code)* | Refactored `WatchlistModal.js` to ESLint compliance (was 25 problems: `no-undef` process, `max-lines-per-function`, 16 `react/prop-types` warnings, a `no-magic-numbers` 409, 6 forbidden-comment violations). Split into `src/hooks/useWatchlistEntryForm.js` + `WatchlistDeleteConfirm.js` + `WatchlistEntryFields.js` + `WatchlistModalFooter.js`, matching the established Watchlist.js ESLint-compliance pattern (ST-14, EPIC-03, v6.8, BLG-FE-77) | `npx eslint src/components/watchlist/WatchlistModal.js` exits 0, zero warnings/errors; no functional/visual behaviour change | Pass | None |
| ST-18 | `docs/ops/csp_unsafe_inline_audit_2026-08-08.md` | Audited every inline-script/inline-style source. `script-src`'s `'unsafe-inline'` removed entirely, replaced with a content hash for the sole static inline script (the GitHub Pages SPA-redirect trick) — hash taken directly from a real browser's own CSP violation report. `style-src`'s `'unsafe-inline'` retained, narrowly justified (a dynamic, per-chart-config `<style>` block in the currently-unused `chart.js` primitive; `BLG-FE-146` filed for future rework) | CSP no longer includes a blanket `'unsafe-inline'` for `script-src`; `style-src` narrowed or explicitly justified; no functional regression | Pass | None |

**QA test coverage:**
- Scenarios run: `dialog-classname-override-fixes.spec.js` (6/6 pass), `form-validation-error-color-fixes.spec.js` (6/6 pass), `watchlist.spec.js` (5/5 pass, regression), `signals-add-to-watchlist.spec.js` (3/3 pass, regression), `reports-performance-tab.spec.js` (13/13 pass, regression, CSP check), `smoke-critical-paths.spec.js` (2/2 pass, regression, CSP check) — 35/35 across the full combined runs; a single additional flake (WidgetLibrary dev-server cold-start timing, unrelated to any code change) was independently reproduced and confirmed passing in isolation on the warm server, and again in the final consolidated 20/20 run below.
- Regression areas checked: watchlist add/edit/validation flows, dashboard modals (WidgetLibrary, MonitorModal), reports export/tab rendering, signals-to-watchlist flow, trade plan abandon modal, smoke critical paths — all under the ST-18-tightened CSP.
- Known deviations filed: None.
- **Environment note:** this sandbox's OS does not support Playwright's own bundled Chromium install (matches the constraint already documented in `docs/ops/keyboard_navigation_audit_2026-07-29.md`). Worked around by pointing Playwright at the system `chromium-browser` package (`/usr/bin/chromium-browser`) via a local config override — all Playwright evidence above is from a **real browser run**, not a static/code-review-only assessment.

**Final consolidated verification run** (`dialog-classname-override-fixes.spec.js` + `form-validation-error-color-fixes.spec.js` + `signals-add-to-watchlist.spec.js` + `watchlist.spec.js`, all together): **20/20 passed** (2.7 minutes).

## Verification Readiness

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes — none found; 2 out-of-scope findings filed as `BLG-FE-145`, `BLG-FE-146` |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes (this EPIC) |

## Sign-Off

- [x] All acceptance criteria verified against canonical spec (or documented as not-applicable per Case E)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — `useWatchlistEntryForm.js` uses the already-exported `API_BASE_URL` from `base44Client.js`

This EPIC has frontend-visible changes in every story (ST-15 CSS rendering fixes, ST-16 colour-token changes, ST-17 a full component refactor, ST-18 a CSP change affecting page rendering) — the BLG-GOV-19 autonomous-class sign-off (criterion 3: no frontend-visible change) is unavailable per its own detection rule. Sign-off performed per-story by the engine acting in the relevant domain-authority role under delegated authority (§5.3), per the Mixed-Class EPIC Signer Format convention:

Sprint Execution Engine (agent-mediated, Head of Engineering role — §5.3)
Sprint Execution Engine (agent-mediated, Frontend Specifications & UX Documentation Owner role — §5.3)
Sprint Execution Engine (agent-mediated, Cybersecurity & Trust Lead role — §5.3)

- Date: 2026-08-08
- Comments: All four stories' observable ACs are covered by real-browser Playwright evidence (not code-review-only) — see the per-story sign-off notes in `execution_state.json` and the two audit docs (`docs/ops/dialog_classname_override_audit_2026-08-07.md`, `docs/ops/csp_unsafe_inline_audit_2026-08-08.md`) for full method and findings. Product Owner acceptance and the merge-gate QA sign-off remain human gates per CLAUDE.md §2/§13 — not satisfied by this agent-mediated record.
