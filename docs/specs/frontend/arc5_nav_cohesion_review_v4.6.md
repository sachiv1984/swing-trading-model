**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-30
**Story:** ST-11 (BLG-FE-42, EPIC-03, v4.6)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Arc 5 Nav Cohesion Review — v4.6

## 1. Purpose

This document reviews the current sidebar navigation structure against the projected full Arc 5 complete state (SI-01 through SI-05 all shipped), with specific attention to SI-02 BehaviouralDriftPanel placement in v4.6. It assesses navigability, grouping logic, naming clarity, and page depth, and states a recommendation.

---

## 2. Current Nav Inventory

The sidebar nav (`src/Layout.js`) uses a collapsible 4-group model introduced in v2.3 (navigation.md v1.2):

```
Dashboard                           [ungrouped home link]

TRADING
  Positions
  Trade Entry
  Trade History
  Reflections
  Red Flag Journal                  [v3.9, SI-03]

ANALYTICS
  Analytics                         [PerformanceAnalytics — contains SI-01 panel]
  Risk Dashboard
  Signals
  Reports
  Weekly Digest                     [SI-05 output target]

TOOLS
  Screener
  Watchlist
  Ticker Universe
  Alerts

SYSTEM
  Settings
  System Status
  Notifications
```

**Arc 5 signal mapping (current):**

| Signal | Feature | Nav location | Pattern |
|--------|---------|-------------|---------|
| SI-01 | Pre-Entry Validation | Analytics → Analytics (PerformanceAnalytics §19) | Embedded panel |
| SI-02 | Behavioural Drift Detection | Analytics → Analytics (PerformanceAnalytics §20, v4.6) | Embedded panel |
| SI-03 | Red Flag Journal | Trading → Red Flag Journal | Dedicated page |
| SI-04 | TBD | TBD | TBD |
| SI-05 | Weekly Digest | Analytics → Weekly Digest | Existing page, new content |

---

## 3. Navigability Assessment

### 3.1 SI-01 + SI-02: Co-located in PerformanceAnalytics

Both SI-01 (Arc5ComplianceSection) and SI-02 (BehaviouralDriftPanel) live as embedded sections within `PerformanceAnalytics.js`, accessed via **Analytics → Analytics**. This is consistent with the existing analytics page model and requires no additional navigation steps.

**Assessment: Clear.** Users who want compliance or drift data know to go to Analytics. Two Arc 5 panels on the same page is acceptable at current count — there is no cognitive overload at 2 panels within a larger analytics page.

**Risk to monitor:** If SI-04 adds a third embedded panel to PerformanceAnalytics, the page will require section navigation (tab bar, anchor links, or collapsible headers) to remain usable. Flag at SI-04 planning.

### 3.2 SI-03: Dedicated Page in Trading Group

Red Flag Journal (SI-03) lives under **Trading → Red Flag Journal** — a standalone page. This placement is intentional: the Red Flag Journal is a deviation audit log reviewed as part of the trading workflow (reviewing past override events when assessing plan discipline). It is not an analytical metric — it is an event record.

**Assessment: Correct.** The Trading vs Analytics split is semantically meaningful. Deviation events belong with trading workflow; compliance scores belong with analytics. This distinction should be maintained as Arc 5 scales.

### 3.3 SI-05: Weekly Digest

SI-05 Phase 1 will add Arc 5 summary content (SI-01 + SI-03 metrics) to the existing **Weekly Digest** page under Analytics. No new nav item required.

**Assessment: Clear.** The Weekly Digest is an established destination for summary content. SI-05 adds to it without requiring a new nav item.

---

## 4. Grouping Logic

The current grouping is:

| Group | Purpose |
|-------|---------|
| Trading | Workflow tools: manage positions, record trades, review deviation events |
| Analytics | Analytical views: performance metrics, compliance panels, digest |
| Tools | Discovery and configuration tools: screener, watchlist, alerts |
| System | Infrastructure: settings, status, notifications |

Arc 5 signals sit correctly across Trading and Analytics:
- **SI-03 in Trading:** Deviation events are workflow artefacts — part of the trading review process
- **SI-01, SI-02 in Analytics:** Compliance and drift scores are analytical outputs — summary views for assessment
- **SI-05 in Analytics:** Weekly digest is a summary — belongs in Analytics, not Tools

**Assessment: Grouping is coherent.** No regrouping required at the current Arc 5 phase.

---

## 5. Naming Clarity

| Element | Current label | Assessment |
|---------|-------------|-----------|
| Nav group | "Analytics" | Appropriately broad; contains both performance analytics and compliance panels |
| Nav item | "Analytics" (links to PerformanceAnalytics) | Slightly ambiguous — the nav item and group share the word "Analytics". Acceptable at current scale; may warrant renaming to "Performance" if the group expands further |
| Page section | "Behavioural Drift" (SI-02 panel heading) | Descriptive and distinct; consistent with "Arc 5 Compliance" heading pattern |
| Nav item | "Red Flag Journal" (SI-03) | Specific and memorable; matches the product concept |
| Nav item | "Weekly Digest" (SI-05 target) | Clear; users understand this is a summary view |

**Naming improvement opportunity (non-blocking):** The nav item "Analytics" under the "Analytics" group creates mild redundancy. Renaming the nav item to "Performance" (linking to `PerformanceAnalytics.js`) would disambiguate the group label from the item label. This is a low-priority cosmetic improvement — file as a backlog item if the analytics group expands. Not recommended for immediate action.

---

## 6. Page Depth

All Arc 5 signals are accessible within **1 nav click** from any page:
- SI-01, SI-02: 1 click to Analytics group → Analytics item → scroll to section
- SI-03: 1 click to Trading group → Red Flag Journal
- SI-05: 1 click to Analytics group → Weekly Digest

**Page depth is appropriate.** All Arc 5 content is reachable in one click. No deep nesting exists or is planned.

---

## 7. Full Arc 5 Complete State (SI-01 – SI-05) Projection

When all 5 Arc 5 signals are shipped, the projected nav inventory is:

```
TRADING
  ...
  Red Flag Journal       ← SI-03 (deviation audit log)

ANALYTICS
  Analytics              ← SI-01 (pre-entry compliance panel)
                         ← SI-02 (behavioural drift panel)
  ...
  Weekly Digest          ← SI-05 (weekly summary digest using SI-01 + SI-03 data)
```

SI-04 placement is unknown. If SI-04 produces another embedded analytics panel, PerformanceAnalytics would contain 3 Arc 5 panels. At that point, a section anchor bar (tab strip or jump links) within PerformanceAnalytics becomes advisable.

**No structural nav change is triggered by SI-04 alone.** The 4-group collapsible model is still appropriate at full Arc 5 with the current signals.

---

## 8. Recommendation

**Maintain current nav structure.** No structural changes are recommended at this phase.

Rationale:
1. SI-01 and SI-02 in PerformanceAnalytics (Analytics group) is correct and consistent
2. SI-03 (Red Flag Journal) in Trading group is semantically correct and should remain there
3. SI-05 in Weekly Digest (Analytics group) requires no nav changes
4. Page depth is 1 click for all Arc 5 signals — no depth problem exists
5. The Trading / Analytics split correctly separates workflow tools from analytical panels

**Deferred actions (non-blocking):**

| Action | Trigger | Recommended sprint |
|--------|---------|-------------------|
| Add section anchor bar to PerformanceAnalytics | SI-04 adds a 3rd embedded panel | SI-04 sprint or before |
| Rename "Analytics" nav item to "Performance" | Analytics group exceeds 6 items | Next nav review cycle |

**No UX spec or implementation backlog item is required for the current state.**

---

## 9. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Head of UX & Design | ✅ Approved | 2026-05-30 |

**Head of UX & Design notes:** Current 4-group collapsible nav is well-suited for the Arc 5 complete inventory. The Trading/Analytics split for SI-03 vs SI-01/SI-02 is the correct UX taxonomy — deviation events are workflow, compliance panels are analytical. PerformanceAnalytics remains navigable at 2 embedded Arc 5 panels. Monitor at SI-04 for section depth trigger.
