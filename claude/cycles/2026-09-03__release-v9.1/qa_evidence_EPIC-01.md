Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-04

# QA Evidence — EPIC-01 (Frontend Accessibility & UI Consolidation)

**EPIC:** EPIC-01 — Frontend Accessibility & UI Consolidation
**Cycle:** 2026-09-03__release-v9.1
**Sprint goal:** Ship all 41 backlog-driven hygiene items in the v9.1 scope — frontend accessibility fixes, backend reliability/tech-debt cleanup, QA/test coverage, and governance/spec-process debt — so that every axe-core violation in `KNOWN_VIOLATIONS`, the npm build regression, and all 3 outstanding passed-target backlog items close clean with zero deviations.
**Test scenarios used:** `tests/e2e/accessibility-axe-scan.spec.js`, `tests/e2e/trade-plan.spec.js`, `tests/e2e/position-sizing-concentration.spec.js`, `tests/e2e/what-if-sizing-preview.spec.js`, `tests/e2e/smoke-critical-paths.spec.js`

## Evidence Table

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-01 | `docs/specs/frontend/pages/dashboard.md#Advisory Label`; `tests/e2e/accessibility-axe-scan.spec.js` | `AiDisclaimer.js` badge background changed `bg-amber-600` → `bg-amber-700` (5.02:1 contrast) per approved design decision record | axe-core no longer reports `color-contrast` for DashboardHome badge; `KNOWN_VIOLATIONS` entry removed | Pass | None |
| ST-02 | `docs/specs/frontend/pages/trade_plan.md`; `tests/e2e/accessibility-axe-scan.spec.js` | `aria-label` added to TradePlan's Market/Status/Setup Type `<select>` elements (the `Field` wrapper's `<label>` was visually adjacent but not programmatically associated) | axe-core no longer reports `select-name` on TradePlan; `KNOWN_VIOLATIONS` entry removed | Pass | None |
| ST-03 | `docs/specs/frontend/pages/settings.md`; `tests/e2e/accessibility-axe-scan.spec.js` | `aria-label` added to Settings' Default Currency and Theme `SelectTrigger` comboboxes | axe-core no longer reports `button-name` on Settings; `KNOWN_VIOLATIONS` entry removed | Pass | None |
| ST-04 | `docs/specs/frontend/pages/settings.md`; `tests/e2e/accessibility-axe-scan.spec.js` | `id`/`htmlFor` pairing added to all 12 Settings form `Label`+`Input` pairs | axe-core no longer reports `label` on Settings; `KNOWN_VIOLATIONS` entry removed | Pass | None |
| ST-05 | `docs/specs/frontend/pages/settings.md`; `tests/e2e/accessibility-axe-scan.spec.js` | No colour change — `PageHeader.js` description text already used the approved `text-slate-600 dark:text-slate-400` token. Root cause was a scan-timing race against the page's framer-motion fade-in; fixed at the test level (`runAxeScan` waits out the entrance animation before scanning) | axe-core no longer reports `color-contrast` for the Settings subtitle; `KNOWN_VIOLATIONS` entry removed | Pass | None |
| ST-06 | `src/hooks/usePositionSizingFetch.js`; `docs/specs/frontend/pages/trade_plan.md#5d.3` | Extracted `useSessionRiskPercent` + `useDebouncedSizing` shared hooks from `PositionSizingWidget.js` / `WhatIfSizingPreview.js`; `checkBeforeDebounce` option preserves each component's distinct pre-existing loading-timing behaviour | Both components share the debounce/fetch/session-storage logic via one hook; existing Playwright coverage passes unchanged; FE Specs & UX Documentation Owner sign-off | Pass | None |
| ST-07 | `docs/specs/frontend/pages/positions.md#Keyboard Navigation Requirements`; `docs/specs/frontend/pages/trade_history.md#Keyboard Navigation Requirements`; `docs/specs/frontend/pages/red_flag_journal.md#9. Keyboard Navigation Requirements` | Added "Keyboard Navigation Requirements" section to all 3 named specs (documentation only, no code change) | Section added to at least Positions, Trades, and Red Flag Journal specs | Pass | None |

**QA test coverage:**
- Scenarios run: `accessibility-axe-scan.spec.js` (4/4 pass, 5 consecutive clean runs on the Settings page specifically to confirm the ST-05 animation-timing fix), `trade-plan.spec.js` (41/41 pass), `position-sizing-concentration.spec.js` (3/3 pass), `what-if-sizing-preview.spec.js` (8/8 pass), `smoke-critical-paths.spec.js` (3/3 pass)
- Regression areas checked: TradePlan form (all select/input behaviour), Settings form (all field bindings, Select comboboxes), Position sizing (Widget + What-If Preview debounce/fetch behaviour, session-persisted risk %, FX override, concentration reason display), DashboardHome AI Advisory badge
- Known deviations: None found — all stories' deviation checks completed with nothing to file

## Frontend Testing Gate (LL-v3.1-EX-01)

Every observable AC in this EPIC (colour contrast, aria-label/discernible-name presence, form-label association) is covered by an automated Playwright scenario in `tests/e2e/accessibility-axe-scan.spec.js`, which asserts against real axe-core `serious`/`critical` violation output — not code review alone. No "code review only" AC exists in this EPIC; no backlog item is required under this gate.

## Autonomous Class Eligibility Check (BLG-GOV-19)

- Criterion 1 (all stories `autonomous`): ✓
- Criterion 2 (all AC code-review-verifiable, no observable UI behaviour): ✗ — ST-01 through ST-06 have observable UI/behavioural AC
- Criterion 3 (no frontend-visible change): ✗ — this EPIC modifies `src/pages/Settings.js`, `src/pages/TradePlan.js`, `src/components/shared/AiDisclaimer.js`, `src/components/trades/PositionSizingWidget.js`, `src/components/trades/WhatIfSizingPreview.js`
- Criterion 4: N/A (criteria 2 and 3 already fail)

**Autonomous class does not apply.** Standard Sign-Off Block used below, per criterion 3 fail-path.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no direct URL construction introduced this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-04
- Comments: All 7 stories verified against live Playwright runs (not just static code review) — 4/4 accessibility-axe-scan.spec.js, 41/41 trade-plan.spec.js, 3/3 position-sizing-concentration.spec.js, 8/8 what-if-sizing-preview.spec.js, 3/3 smoke-critical-paths.spec.js, all green on this branch's HEAD commit. ST-05's fix went beyond the literal AC (removing the KNOWN_VIOLATIONS grandfather entry) to resolve the actual root cause (animation-timing scan race) so the underlying flake does not resurface in CI. ST-06's cross-component behavioural-parity claim was independently reviewed by an FE Specs & UX Documentation Owner agent-mediated pass (Approved) rather than resting on this sign-off alone. This DoQ review itself was independently agent-mediated and re-ran all 5 test files live (59/59 passed) rather than trusting the evidence table — Approved, with 2 non-blocking findings both addressed same-session: (1) a cosmetic indentation defect on Settings.js's `settings-min-trades-for-analytics` Input (fixed); (2) a pre-existing, out-of-scope `moderate` `heading-order` axe finding on Settings, unrelated to this EPIC's diff (filed as BLG-FE-170 per the sprint execution write-scope's out-of-scope-finding exception). CI on `exec/2026-09-03__release-v9.1/EPIC-01` confirmed fully green across all 8 push-triggered checks (Governance Sync Loop, CI Pytest Suite, Endpoint Coverage Report, Golden Output Regression Gate, Service Layer Coverage Gate, Portfolio Integration Tests, Critical-Path Smoke Tests, Playwright E2E Acceptance Tests).
