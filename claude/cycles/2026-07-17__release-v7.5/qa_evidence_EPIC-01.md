Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-17

# QA Evidence — EPIC-01 (v7.5)

## Consolidation Block

**EPIC:** EPIC-01 — Global command palette / cross-page search
**Cycle:** 2026-07-17__release-v7.5
**Sprint goal:** Ship all four v7.5 UI feature expansions — global command palette, user-defined price alerts, bulk actions, and saved filters/calendar view — each fully wired to its now-locked design artefact and observable in the running app.
**Test scenarios used:** tests/e2e/command-palette.spec.js (SC-CP-01 through SC-CP-12)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-01 | docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md; docs/specs/frontend/pages/navigation.md v1.3; docs/specs/blg_fe_115_pre_implementation_readiness_pass.md | Global Cmd/Ctrl-K command palette (`src/components/CommandPalette.js`), wired into `Layout.js` with a desktop sidebar + mobile header mouse-fallback affordance, a first-session-only dismissible discoverability toast, and a new `DataState` `inline` empty-state variant (`design_system.md` v1.2). `cmdk` installed (readiness-pass-flagged pre-implementation blocker). | AC-1: Cmd/Ctrl-K opens the palette from any page in the app | Pass | None |
| ST-01 | (same as above) | (same as above) | AC-2: Typing a ticker surfaces matches across Watchlist/Positions/TradePlans and navigates to the selected result | Pass | None |
| ST-01 | (same as above) | (same as above) | AC-3: Typing a page name navigates to that page | Pass | None (fixed a pre-existing `createPageUrl` gap — TradePlan/TradePlans were missing from the route map — required for this AC to hold for all `pages.config.js` entries) |

**QA test coverage:**
- Scenarios run: `tests/e2e/command-palette.spec.js` — SC-CP-01 (Ctrl+K opens from Positions), SC-CP-02 (opens from Settings — "any page" coverage), SC-CP-03 (mouse-fallback affordance opens palette), SC-CP-04 (Escape closes without navigating), SC-CP-05 (Ctrl+K suppressed while focus is in a text input), SC-CP-06/07 (page-name typed → navigates, incl. Trade Plans), SC-CP-08/09/10 (ticker typed for open position / watchlist / trade plan → surfaces under "Your Data" and navigates), SC-CP-11 (no-match empty state), SC-CP-12 (empty-input frequent-pages state, no "Your Data" group). All 12 run live against `npm start` (real dev server, `page.route()` API interception) — 12/12 pass.
- Regression areas checked: `tests/e2e/keyboard-shortcuts.spec.js` (Layout.js's existing `n`/`w`/`r` shortcut handling — unaffected by the new Cmd/Ctrl-K listener), `tests/e2e/sidebar-nav-groups.spec.js` (desktop sidebar — new search-affordance row inserted without disturbing nav-group structure), `tests/e2e/smoke-critical-paths.spec.js` (critical paths unaffected). 20 passed, 2 pre-existing skips (unrelated to this change) — no regressions.
- Known deviations filed: None. One implementation note (not a filed deviation, per LL-v3.4-P3-03 intent-match): `ux_spec.md` assumed a `/trade-plans/{id}` path-param detail route for trade-plan results; the app's actual `TradePlan` detail route is query-param based (`/TradePlan?edit={id}&ticker=...&market=...`). Intent (navigate directly to that plan's detail, ID already known) matches; only the literal URL pattern differed. Recorded in `execution_state.json` notes for ST-01.

**Frontend testing gate (CLAUDE.md / LL-v3.1-EX-01):** All 3 ACs are observable UI behaviour (palette open, cross-entity search + navigate, page-name navigate) — sprint_backlog.md's "Staging-only ACs: None" for ST-01 is confirmed correct; all 3 are Playwright-covered in CI (`tests/e2e/command-palette.spec.js`), satisfying the hard gate without a staging run.

**Autonomous class eligibility check (BLG-GOV-19):** Not applicable — this EPIC modifies `src/components/CommandPalette.js` and `src/Layout.js` (both under `src/components/**` / project root component tree with frontend-visible change), so Criterion 3 (no frontend-visible change) is automatically unmet per the BLG-GOV-135 detection rule. Standard Sign-Off Block below applies; Playwright coverage evidence is recorded above per the fail-path instruction.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — `CommandPalette.js` uses `API_BASE_URL` exported from `src/api/base44Client.js`; `TradePlan.js` navigation constructs `/TradePlan?edit=...` using the existing app-relative-route convention (no external base), consistent with `TradePlans.js`'s existing Edit-button navigation.
- Signed off by: Director of Quality
- Date:
- Comments: Engine-side verification complete — all 3 AC Playwright-covered and passing live (12/12), regression suite clean (20/20, 2 unrelated pre-existing skips). Per `execution_prompt.md` §5.3, QA sign-off is an always-human gate (not agent-mediated) — awaiting Director of Quality review and Date entry before this EPIC's PR can be opened (§3.2.B) and before the merge gate (§4) can pass.
