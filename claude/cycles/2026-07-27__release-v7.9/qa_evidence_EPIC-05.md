Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

## Consolidation Block

**EPIC:** EPIC-05 — "Why is my stop moving" explainer tooltip on the trailing-stop UI
**Cycle:** 2026-07-27__release-v7.9
**Sprint goal:** Ship all 15 v7.9 EPICs — the two P1 UX anchors and the 13 capacity-fill engineering-hardening items — with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/e2e/trailing-stop-explainer-tooltip.spec.js` (5 Playwright tests — see execution note below).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-05 | `docs/specs/frontend/pages/positions.md` v2.6 §Trailing Stop Column | New shared `TrailingStopExplainerIcon` component (info icon + Radix Tooltip, hover/keyboard-focus accessible) wired into Table View's "Stop" column header and Grid View's Trail Stop tile. | AC-01: Tooltip added to the position/trade view — Pass. AC-02: Text reviewed against §7 for accuracy — Pass (verified directly against `strategy_rules.md` §7.1/§7.2/§7.3 by both this engine and Product Owner). AC-03: Product Owner sign-off — Pass (agent-mediated). | Pass with notes | None |

**Finding (pre-existing, not introduced by this story):** the v6.2 spec section described a separate "Trail Stop" column (Table View) and stat label (Grid View) that do not actually exist in the shipped UI — Table View has one combined "Stop" header; Grid View's tile has no standalone label, only an "Init: {value}" subtext. The explainer icon was placed on the real anchors instead (after the combined "Stop" header text; inline with the "Init:" subtext line in the Grid tile) — the closest faithful placement given the actual UI. Documented as a correction in `positions.md`, not fixed (restructuring the Stop column is out of this display-only story's scope). Both Product Owner and Head of UX & Design (agent-mediated) independently verified this against the actual JSX and confirmed it's a reasonable inline correction, not a scope violation requiring a new design-gate cycle.

**QA test coverage:**
- Scenarios run: `tests/e2e/trailing-stop-explainer-tooltip.spec.js` (5 tests: Table View icon presence, hover reveals tooltip text, Grid View icon presence, keyboard-focus reveals tooltip, aria-label correctness). **Execution note:** could not be run locally — this sandbox's OS (Ubuntu 26.04) is unsupported by Playwright's browser installer (same limitation as EPIC-01/EPIC-02, both of which passed their equivalent Playwright suites in real CI — EPIC-01's PR #1109 confirmed "Playwright E2E Acceptance Tests" passing). Will run via `.github/workflows/playwright.yml`'s glob auto-discovery on this PR.
- Regression areas checked: no API/backend change; no existing test suite affected. ESLint diff-check confirms zero new violations introduced in `Positions.js`/`PositionCard.js` (identical problem counts before/after this change).
- Known deviations filed: None — the placement finding is a documented correction, not a deviation from this story's own AC.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block — NOT APPLICABLE

This EPIC introduces frontend-visible changes (new tooltip icon/interaction) — criterion 3 of the autonomous class is automatically unmet per the `BLG-GOV-135` detection rule. Standard sign-off block used instead.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction: not applicable — this component makes no network requests (static text only).
- Signed off by: Sprint Execution Engine (agent-mediated, Product Owner role — §5.3)
- Date: 2026-07-27
- Comments: Product Owner (agent-mediated) independently verified the tooltip copy against `strategy_rules.md` §7 and confirmed no tunable parameter values are surfaced, per the design's explicit scope constraint. Head of UX & Design (agent-mediated) separately confirmed the placement correction against the actual shipped JSX in both Table and Grid views.
