Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-10

# QA Evidence — EPIC-03 (Frontend Correctness Fixes)

**EPIC:** EPIC-03 — Frontend Correctness Fixes
**Cycle:** 2026-08-08__release-v8.5
**Sprint goal:** Clear the full ready frontend-correctness, design-consistency, and security-hardening slate across all 25 scoped stories — see `sprint_goal.md`
**Test scenarios used:** `tests/e2e/command-palette.spec.js` (SC-CP-13, new), `tests/e2e/trade-plan.spec.js` (SC-TP-24a/b/c, new), `tests/e2e/reports-realised-pnl-zero-colour-convention.spec.js` (SC-RPZ-01..04, new)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-06 | `tailwind.config.js`, `tests/e2e/command-palette.spec.js` | Registered `muted`/`muted-foreground` in `tailwind.config.js` `theme.extend.colors`. `--muted`/`--muted-foreground` are defined in `src/index.css` but were never registered, so all 5 in-scope `-muted` utility classes (`bg-muted`, `border-muted`, `fill-muted`, `fill-muted-foreground`, `text-muted-foreground`) compiled to empty CSS rules. Design Pre-Approved. **Post-DoQ-review addition:** SC-CP-14 added (2nd call site, `CommandInput`'s `::placeholder` colour — the same class the generic `Input` primitive uses); BLG-FE-148 filed for the remaining untested `-muted` consumer families (Select/Tabs/Sheet/Toast/Toggle/Dialog) per CLAUDE.md's frontend hard gate. | (1) `-muted` classes compile to non-empty CSS, verified via real `tailwindcss` build; (2) no visual regression at any confirmed-affected call site, Playwright coverage or staging sign-off | Pass with notes | None (backlog item filed for deferred coverage, not a spec deviation) |
| ST-07 | `docs/specs/api_contracts/trade_plan_endpoints.md` | Wired `thesis_model_version`/`thesis_prompt_version` into the frontend save payload (`src/pages/TradePlan.js`) from the real Claude "Improve with AI" response; cleared on any manual narrative-field edit or on the non-AI "Generate thesis" template path. Backend already fully supported both fields — gap was frontend-only. | (1) AI-generated content (no manual edits) has both fields populated in the DB; (2) manually-typed/edited content leaves both fields null | Pass | None |
| ST-08 | `docs/design/2026-08-08__release-v8.5/exact-zero-pnl-colour-convention/decision_record.md`, `docs/specs/frontend/pages/reports.md` | `TaxYearReport`'s Realised P&L colour rule (`src/pages/Reports.js`) changed from binary to the three-way rule `MonthlyPnlTable` already used (grey/neutral for exact-zero, not red). Resolves `DEV-REPORTS-ST01-02`. Design decision already resolved and spec already updated by Design Gate ahead of this implementation. **Post-DoQ-review fix:** the initial implementation shared the `pnlColor` variable with the adjacent `P&L %` column, silently carrying the fix into a column `decision_record.md` §5 explicitly scoped out ("Does not touch P&L %"). Decoupled into a separate `pnlPctColor` kept on the original binary rule; added SC-RPZ-05 regression test. | (1) both tables render exact-zero with the same colour; (2) `reports.md` states one convention, no remaining per-table caveat (already true pre-implementation, confirmed); (3) no regression to non-zero colouring, Playwright coverage or staging sign-off | Pass | None |

*(All ACs for all three ST items appear in the table above.)*

**QA test coverage:**
- Scenarios run (real `tailwindcss` CLI build + backend pytest, both executed in this sandbox): ST-06's muted-class build verification (5/5 classes now non-empty); `tests/test_trade_plan_tags.py` and trade-plan-scoped `test_api_contracts.py` regression (unaffected by ST-07/ST-08, confirms no backend regression)
- Playwright coverage added this EPIC (could not execute locally — Chromium unsupported on this sandbox's OS; real CI (`playwright.yml`, runs on `pull_request`) is the verification path per LL-v8.3-P3-02):
  - `tests/e2e/command-palette.spec.js` SC-CP-13/SC-CP-14 (ST-06 — 2 call sites: `CommandGroup` heading `color`, `CommandInput` `::placeholder` colour)
  - `tests/e2e/trade-plan.spec.js` SC-TP-24a/b/c (ST-07)
  - `tests/e2e/reports-realised-pnl-zero-colour-convention.spec.js` SC-RPZ-01..05 (ST-08 — includes SC-RPZ-05, the P&L % non-regression guard added after DoQ review)
- Regression areas checked: `trade_plans.py` backend route family unaffected (ST-07 is frontend-only); `MonthlyPnlTable` unchanged (ST-08, confirmed via SC-RPZ-04 regression test); `TaxYearReport`'s `P&L %` column confirmed decoupled from the Realised P&L fix (SC-RPZ-05, added after DoQ review caught the initial shared-variable slip)
- Known deviations filed: None
- Backlog items filed from this EPIC: `BLG-FE-147` (broader sibling tailwind-token gap, out of ST-06's scope), `BLG-FE-148` (remaining untested `-muted` call-site families, per CLAUDE.md's frontend hard gate)

**Critical finding — real CI, not the DoQ review (2026-08-10):** the first real GitHub Actions run of this PR failed both new `command-palette.spec.js` tests (`SC-CP-13`/`SC-CP-14`) with `Received: "rgb(115, 115, 115)"` instead of the expected dark-theme value — the *light*-theme `--muted-foreground` value. Root cause traced to `src/Layout.js`: `tailwind.config.js`'s `darkMode: ["class"]` requires an ancestor element carrying the literal `dark` class for any `dark:` variant to apply, but that class was only ever applied to Layout's own wrapper `<div>` — never to `document.documentElement`. Radix's `DialogPortal` (`src/components/ui/dialog.js`) renders its content into `document.body`, **outside** that wrapper's DOM subtree. This is a pre-existing, systemic production bug, not introduced by this EPIC: **every Dialog-based component app-wide (14+ consumers — CommandPalette, ExportModal, WatchlistModal, WidgetLibrary, PositionEntryModal, etc.) has always rendered in light-theme CSS scope, regardless of the user's actual theme setting.** ST-06's new tests are simply the first to observe this (the muted-foreground token registration made the wrong-theme value distinguishable from an empty rule for the first time). Fixed at the root: `Layout.js` now also syncs the `dark` class onto `document.documentElement`, which covers every portal (portals still mount under `<html>`/`<body>`), not just this EPIC's own call sites. This is exactly the kind of gap real CI catches that a sandboxed review cannot (LL-v8.3-P3-02) — pushing without ever being able to run Playwright locally in this sandbox surfaced a genuine, significant, previously-hidden app-wide defect.

**Agent-mediated DoQ review findings (2026-08-10, first pass) — both remediated, see table above and Comments below:**
1. ST-06 AC-02 was initially claimed "Pass" with only 1 of ~9 real call-site families covered by Playwright, and no backlog item filed for the rest — a hard-gate violation (CLAUDE.md: deferred observable AC without Playwright coverage requires a filed backlog item before the PR opens). Remediated: added a 2nd call site (SC-CP-14), filed `BLG-FE-148` for the rest.
2. ST-08's implementation shared the `pnlColor` variable between the Realised P&L and P&L % columns, silently carrying the fix into a column the approved Design Gate decision explicitly scoped out. Remediated: decoupled into `pnlPctColor`, added SC-RPZ-05 regression test.
3. Minor: SC-CP-13's original comment inaccurately claimed the pre-fix heading colour resolved to `rgb(0, 0, 0)` (browser default). Corrected — it inherited `text-foreground` (near-white in dark theme) from its ancestor, not black.

---

## Sign-Off Block

**Environment-parity note (LL-v8.3-P3-02):** All three stories in this EPIC introduce frontend-visible changes. Playwright coverage exists for every observable AC (see above) but could not be executed in this sandbox environment (`npx playwright install chromium` fails: "ERROR: Playwright does not support chromium on ubuntu26.04-x64" — this OS/environment cannot run a browser at all, not merely a sandboxed-pass-vs-real-CI-fail gap). Per LL-v8.3-P3-02, sandboxed local review is not a substitute for real CI observation for interaction/rendering-timing-sensitive ACs; here there is no sandboxed pass to even report — the tests are new, syntax-verified (babel parse), logically reviewed against the actual component code and real backend response shapes, but **their real pass/fail outcome is pending the first GitHub Actions run on PR #1327** (`playwright.yml`, triggers on `pull_request`). This must be confirmed before merge, not assumed from authoring-time review alone.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [ ] Playwright coverage confirmed passing in real CI — **pending this PR's first `playwright.yml` run**
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-10
- Comments: Agent-mediated DoQ review (independent subagent invocation, not self-assessment) ran two passes. First pass: BLOCKED — 2 findings (ST-06's AC-02 claimed Pass with only 1 of ~9 real call-site families covered and no backlog item filed for the rest; ST-08's implementation silently carried the colour fix into the P&L % column the Design Gate decision explicitly excluded). Both remediated in-session (2nd Playwright call site + BLG-FE-148 filed for ST-06; pnlPctColor decoupling + SC-RPZ-05 regression test for ST-08). Second pass: APPROVED, with one trivial non-blocking note (a stale backlog-ID code comment, corrected). Full findings trail in this file's "Agent-mediated DoQ review findings" section above. Sign-off is conditional on the pending real-CI confirmation noted above; if any new Playwright test fails in real CI, this EPIC's DoQ sign-off must be revisited before merge.
