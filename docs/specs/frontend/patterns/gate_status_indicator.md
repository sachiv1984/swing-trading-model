**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-11-02 (created — ST-46, EPIC-07, v9.14, BLG-SPEC-77)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Reference implementation:** `SI02GateStatusSection` in `src/pages/Reports.js` (`reports.md` §SI-02 Gate Status, BLG-FEAT-71)
**Design Source:** docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md
**Release:** v9.14 — ST-46 (BLG-SPEC-77)

---

# Frontend Pattern — Gate Status Indicator

## Purpose

Some features stay locked until the user's own data meets a set of conditions, for example "at least 20 closed trades". A gate status indicator shows the user how far each condition has got and whether it is met. This document turns the SI-02 Gate Status section on the Reports page (`BLG-FEAT-71`) into a reusable pattern, so the next gated feature uses the same states, copy and badge instead of designing a new one.

Use this pattern when a page needs to show **two or more conditions**, each with its own met/not-met result. For a single headline count with a progress bar, use the Dashboard's Gate Progress strip instead (`dashboard.md` §6). The two are deliberately different: the strip answers "how close am I?", the indicator answers "which conditions are still open?".

## Anatomy

A gate status indicator has four parts, top to bottom:

| Part | Content | Reference (SI-02) |
|------|---------|-------------------|
| Header | Section title plus a chevron toggle. The whole header is one button. | "SI-02 Gate Status" |
| Count cards | One stat card per raw input the conditions are computed from, shown as a live number with its unit. | "{N} total closed trades", "{N} linked to a trade plan" |
| Condition rows | One row per condition: a label on the left, a status badge on the right. | "Gate Condition 1" … "Gate Condition 3" |
| Supplementary row (optional) | Context that explains why a condition is not yet met. Shown only when it applies. | Insufficient-data streak and trade count trend (`BLG-FEAT-86`) |

## States

The indicator has five states. Each one must be implemented and covered by a test.

| State | When | What is shown |
|-------|------|---------------|
| Collapsed | Default on page load | Header only, chevron pointing down |
| Loading | Expanded, any data request in flight | One skeleton block in place of the body |
| Error | Expanded, any data request failed | One line: "Unable to load gate status". The rest of the page keeps working |
| Loaded, not all met | Expanded, data loaded | Count cards with live values; each condition row shows MET or NOT MET |
| Empty | Expanded, data loaded, no qualifying records | Counts show 0, every condition shows NOT MET. No separate empty message |

The indicator never hides a condition because its value is 0 or missing. A missing input (for example a null rate) makes that condition NOT MET; it is not shown as an error.

## Badge

| Result | Text | Colour treatment |
|--------|------|------------------|
| Met | MET | Emerald pill: `bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border border-emerald-500/30` |
| Not met | NOT MET | Amber pill: `bg-amber-500/20 text-amber-700 dark:text-amber-400 border border-amber-500/30` |

Both pills use `px-2.5 py-1 rounded-full text-xs font-semibold`. Amber, not red, is used for "not met": an unmet gate is a normal waiting state, not an error. The same pill classes are reused by the Reports page reconciliation badge (`reports.md` §Reconciliation), so a third use should copy them rather than define new colours.

## Props

The reference implementation is a page-local component. When a second gated feature needs it, extract it to `src/components/` with this interface:

| Prop | Type | Required | Meaning |
|------|------|----------|---------|
| `title` | string | Yes | Header text, e.g. "SI-02 Gate Status" |
| `counts` | `{ label: string, value: number, unit: string }[]` | Yes | Count cards, in display order |
| `conditions` | `{ id: string, label: string, met: boolean }[]` | Yes | Condition rows, in display order |
| `isLoading` | boolean | Yes | Selects the Loading state |
| `isError` | boolean | Yes | Selects the Error state |
| `supplementary` | React node | No | Optional row below the conditions |
| `defaultCollapsed` | boolean | No (default `true`) | Initial collapse state |
| `testIdPrefix` | string | Yes | Prefix for `data-testid` values, e.g. `si02-gate-status` |

The component computes nothing. Thresholds and met/not-met results are worked out by the caller, from API data, and passed in as `met` booleans.

## Copy Rules

1. **Counts state the unit in the value line**, e.g. "12 total closed trades", not a bare "12" under a label.
2. **Badges say MET or NOT MET only.** No percentages or "almost there" wording in the badge itself; progress belongs in the count cards.
3. **Condition labels are stable and numbered** ("Gate Condition 1"). The threshold each condition checks is documented in the page spec's Fields table, which is where it must be kept up to date.
4. **The error message is fixed:** "Unable to load gate status".
5. **No advice.** The indicator states facts about the user's records. It never tells the user what to trade or how to change their behaviour to unlock a feature (`strategy_rules.md` §13; see `docs/product/decisions/section13_boundary_examples.md` for worked examples).
6. **Internal codes in titles:** the SI-02 indicator lives on the Reports page, an analytics surface, and keeps its "SI-02" title. A gate indicator on a primary-workflow page (Dashboard, Positions) uses benefit-oriented wording instead, as the Dashboard Gate Progress strip does (`dashboard.md` §6, BLG-SPEC-73).

## Data Rules

- Every count and threshold input comes from a live API response. Nothing is hardcoded except a documented fallback default.
- The thresholds are listed in the page spec, with the product decision that set each one. A threshold change is a spec change first.
- All inputs load in one query (the reference uses one `useQuery` with `Promise.all`), so the indicator moves from Loading to Loaded or Error once, not row by row.
- An optional input that fails on its own (the reference's behavioural-drift call) is caught and simply hides the supplementary row. Only a failure of a required input selects the Error state.

## Accessibility

1. The header toggle is a `<button type="button">` that contains the section heading, so it is reachable by keyboard and announced with its title.
2. The toggle must carry `aria-expanded` reflecting the collapse state, and `aria-controls` pointing at the body's `id`. **The reference implementation does not set either yet** — tracked by `BLG-FE-238`. New implementations must include them.
3. Met/not-met is carried by the badge text, not by colour alone, so it is readable without colour vision and in both themes.
4. Each badge sits in the same row as its condition label, so a screen reader reads label then result in order. Do not separate them into different grid columns that read out of order.
5. Badge and label colours must meet WCAG 2.1 AA contrast in light and dark themes. The reference's theme classes are checked in both themes by `tests/e2e/reports-theme-fix-si02-unrealised-pnl.spec.js`, but no axe scan covers the expanded section yet; a new implementation should add one.

## Testing

A new gate status indicator needs Playwright coverage of every state in the States table, plus a boundary test for each numeric threshold (just below and exactly at the threshold). The reference suite is `tests/e2e/reports-si02-gate-status.spec.js` (SC-SI02-01 to SC-SI02-11).

## Owner Review

**Frontend Specifications & UX Documentation Owner — review recorded 2026-11-02** (Sprint Execution Engine, agent-mediated in the Frontend Specifications & UX Documentation Owner role per `execution_prompt.md` §5.3, against the role charter §5–§6; ST-46 AC 2). Checked against `reports.md` §SI-02 Gate Status, `dashboard.md` §6 and `SI02GateStatusSection` in `src/pages/Reports.js`:
- States, badge classes, copy and data sources match the shipped SI-02 component and its spec.
- The extracted-component props are a forward interface and are labelled as such; no existing code is changed by this document.
- The missing `aria-expanded`/`aria-controls` on the reference toggle is a real gap, filed as `BLG-FE-238`, and the pattern requires both for new use.
- The contrast claim is limited to what a test checks (theme classes, not an axe scan).
- Outcome: **Approved.**

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-11-02 | Created (ST-46, EPIC-07, v9.14, BLG-SPEC-77): SI-02 Gate Status documented as a reusable pattern — anatomy, states, badge, props, copy, data and accessibility rules, testing. |
