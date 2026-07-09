**Owner:** Head of UX & Design
**Class:** Reference Document (Class 2)
**Status:** Published
**Version:** 1.0
**Last Updated:** 2026-07-09
**Story:** ST-07 (BLG-SPEC-58, EPIC-03, v6.8)

---

# Dashboard Homepage — Visual Hierarchy Review (Post-v6.2)

## Purpose

This document satisfies ST-07 AC-01: a review of `DashboardHome.js`'s visual hierarchy against the layout changes introduced since v6.2 (AI Daily Briefing card, v6.3 progressive disclosure, v6.4/v6.7 contrast fixes), confirming the rendered structure matches `docs/specs/frontend/pages/dashboard.md` and flagging any hierarchy or contrast gaps as follow-up items.

## Scope

Compared the current render order in `src/pages/DashboardHome.js` (as of commit `6c3bce08`, the v6.7 BLG-FE-88 fix) against `docs/specs/frontend/pages/dashboard.md` v2.6, section by section.

## Method

Direct code + spec read (no staging run required — this is a document-inspection review; no behavioural change is proposed by this story).

## Findings

### Render order matches spec — no hierarchy discrepancy

| Position | Rendered element | Spec section | Match |
|----------|------------------|---------------|-------|
| 1 | Page header (`h1` "Dashboard" + subtitle) | — (page chrome) | N/A |
| 2 | `MorningBriefing` | §1A | ✅ |
| 3 | 3-col grid: Open Positions / Portfolio Heat / Grace Period | §3 Row 1 | ✅ |
| 4 | 2-col grid: Signal Status / Recent Activity | §3 Row 2 | ✅ |
| 5 | `AiDailyBriefing` | §5 | ✅ |
| 6 | `GateProgressStrip` | §6 | ✅ |
| 7 | Hidden retry root (shown only on all-endpoints-failed) | §7 | ✅ |

The v6.2–v6.7 additions (AI Daily Briefing card, progressive disclosure, two contrast passes) were all layered in at their spec-defined positions without disturbing the original v6.0/v1.9 card ordering. Visual weight is correctly graded: session-summary cards (heaviest, card-framed) → AI Briefing (full-width card, advisory-labelled) → Gate Progress (lightest, frameless strip) — consistent with §6's explicit "lighter visual weight than session-summary cards" requirement.

### Gap identified: page title has no light-theme colour value (not a hierarchy defect, but visual-priority-adjacent)

`DashboardHome.js` line 36:
```jsx
<h1 className="text-2xl font-bold text-white tracking-tight">Dashboard</h1>
```

`text-white` is unconditional — no `dark:` companion pattern is needed here (this is the base/light value), but no light-theme-safe value is set at all, unlike the subtitle immediately below it on line 37 (`text-slate-600 dark:text-slate-400`), which correctly grades for both themes. Since the page title is the top of the visual hierarchy (the first thing establishing "where am I"), an unreadable title on light theme undermines the hierarchy this review is assessing, even though the root cause is a contrast defect rather than an ordering/layout defect.

This is the same class of defect as BLG-FE-88 (fixed this cycle in EPIC-01/ST-02 for the Advisory Label text) and BLG-FE-87 (v6.7), suggesting bare `text-white` without a light-theme value is a recurring pattern rather than isolated to the Dashboard. A repo-wide grep (`text-2xl font-bold text-white`, `text-lg font-semibold text-white`) shows the same pattern on `src/pages/StrategyBenchmark.js:497` and stat values on `src/pages/Signals.js` and `src/pages/SystemStatus.js` — out of scope for a single-page hierarchy review, so filed as a standalone follow-up covering the pattern generally rather than patched inline here.

**Follow-up filed:** BLG-FE-95 — Dashboard/StrategyBenchmark page-title light-theme contrast gap (`text-white` with no light-theme value on primary headings).

## Conclusion

Dashboard homepage visual hierarchy is sound and matches the canonical spec's intended layering for all v6.0–v6.7 additions. One adjacent contrast gap identified and filed as a follow-up (BLG-FE-95); no hierarchy/ordering defects found. No spec or code change required by this story.
