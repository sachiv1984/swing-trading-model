**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved (brief); the spec it governs is approved in the sprint
**Cycle:** 2026-11-11__release-v9.17
**Stories:** ST-06 (BLG-FE-259) — EPIC-02

# Decision Record — One Performance Page (Brief)

## 1. Scope of this record

ST-06 writes a short spec for one Performance page as its first sub-step, then builds it (slice Sequencing; RISK-04). The Product Owner chose at this gate (the user, in session, 2026-11-11) to follow the v9.15 Journal precedent (`site-structure-phase1` §2.3): this gate fixes the brief the spec must meet, and the Head of UX & Design approves the spec in the sprint before any build commit. The gate does not write the spec.

**Gate condition:** ST-06's build sub-step may not start until a new `docs/specs/frontend/pages/performance.md` (Class 1) exists, meets §2, and carries a dated Head of UX & Design approval in its Change Log. Sprint Planning records this as an in-story sequencing gate, not a blocker on the seal.

## 2. Brief for the in-sprint spec

`pages/performance.md` must:

1. **Route and label.** One page at `/Performance`, label "Performance" everywhere (sidebar, heading, palette, browser tab) from the single label source (`navigation.md` v2 §Page Placement; `glossary.md` §UI Labels). It takes the Review area slot that Analytics holds today.
2. **Sections,** in this order: Summary · Reports (monthly and tax-year) · Analytics · Compliance. Each section is reachable in one click through the in-page section index defined for ST-07 (`long-page-section-index` record §2), and each has a `?section=` deep link. The spec names which current card or table lands in which section.
3. **One home per KPI.** List every KPI shown today on `Reports.js` and `PerformanceAnalytics.js` (win rate, profit factor, total P&L, expectancy, average R, and the rest), name the one section that shows it, and remove the duplicate. The Summary section may show a KPI only if no other section repeats it.
4. **Canonical definitions.** Each KPI cites its definition in `docs/specs/metrics_definitions.md` (or the canonical metric source it uses today). The Metrics Definitions & Analytics Canonical Owner confirms, with a date, that every KPI keeps that definition (slice ST-06 AC 2). A KPI whose two current pages compute it differently is listed, and the canonical one is kept.
5. **Redirects.** `/Reports` and `/PerformanceAnalytics` redirect to `/Performance` with a replace navigation (Back does not loop). Any existing tab or query parameter on the old routes maps to the matching `?section=`. `navigation.md`'s placement table, the command palette and `glossary.md` §UI Labels are revised in the same story. ST-05 also edits these, so the two stories merge one after the other (RISK-04).
6. **States.** Loading, empty (no closed trades) and error states per section, taken from the current pages where they exist.
7. **Phone width.** No horizontal page scroll at 390 px. This absorbs `BLG-FE-237` (the Reports tab bar overflow); the spec says so, and `groom backlog` can then close it.
8. **What does not change.** Report generation, tax-year boundaries, exports and every calculation stay as they are. This is a consolidation, not a recalculation.
9. **Testable ACs** for every observable behaviour (route, redirects, section order, section index, one-KPI rule, 390 px), ready for the build sub-step's Playwright coverage.
10. **Design-system conformance.** New markup uses the `app-*` tokens (`design_system.md` §Semantic Colour Tokens), so ST-08's sweep has nothing to convert on this page.

## 3. §13 Compliance

Display of existing deterministic metrics only. No AI call, no new score and no recommendation is added. The spec states this in a §13 note.

## 4. Spec impact

No spec is changed at this gate. ST-06 creates `pages/performance.md` v1.0 and retires `reports.md` (v0.26) and the Performance Analytics part of `analytics.md` (v2.3) to "Superseded by `performance.md`" headers, per the document lifecycle guide.

## 5. Approval

Head of UX & Design: confirmed (brief), 2026-11-11 (agent-mediated, Design Gate Engine). The spec needs its own Head of UX & Design approval in the sprint (§1).
Product Owner: confirmed, 2026-11-11 (the user, in session; chose brief-now, spec-in-sprint).
