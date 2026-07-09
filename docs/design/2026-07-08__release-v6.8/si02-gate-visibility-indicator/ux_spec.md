**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-08
**Approved by:** Product Owner — 2026-07-08
**Story:** ST-06 (BLG-FEAT-71) — SI-02 gate visibility indicator, Reports page
**Cycle:** 2026-07-08__release-v6.8

---

# UX Specification — SI-02 Gate Visibility Indicator (Reports Page)

## 1. Relationship to Existing Gate Progress Indicator

The Dashboard already shows a compact single-metric strip (`dashboard.md` §6, "Gate Progress" — `docs/design/2026-06-22__release-v6.1/gate-proximity-indicator/ux_spec.md`): closed-trade count vs the 20-trade threshold, sourced from `GET /portfolio/gate-metrics`.

This story adds a **more detailed** indicator to the Reports page, surfacing the discrepancy ST-01 (BLG-BE-46) investigates: total closed trades vs. trade-plan-**linked** closed trades are two distinct numbers, plus a per-condition MET/NOT MET breakdown across all 3 SI-02 gate conditions. The Dashboard strip is unchanged — it continues to show the single headline count. This is a Reports-page-only addition; no navigation or Dashboard change.

**Rationale:** The Dashboard strip intentionally stays simple (single glance, daily use). The gate discrepancy uncovered by BLG-BE-46 (20 total closed trades but 0 linked trade-plans) needs a place to show the fuller breakdown so users can see why the gate may show as not-met despite trade count alone appearing sufficient — Reports is where users already review compliance detail (Arc 5 Compliance Summary, §-adjacent).

## 2. Placement

**Page:** Reports (`docs/specs/frontend/pages/reports.md`)
**Position:** New section directly below "Arc 5 Compliance Summary" (§ Arc 5 Compliance Summary) and above "Gross vs Net Comparison". Same collapsible pattern as Arc 5 Compliance Summary — **collapsed by default**, consistent with existing compliance-detail sections on this page.

**Section header:** "SI-02 Gate Status"

## 3. Data Sources

Reads three existing endpoints (no new backend work per ST-06 context note):
- `GET /trades` → total closed trades
- `GET /trade-plans` → trade-plan-linked closed trades (count of closed trades with non-null `position_id` linkage)
- `GET /analytics/arc5-compliance` → `trade_plan_adherence_rate` and other gate-condition inputs

## 4. Layout

| Element | Source | Display |
|---------|--------|---------|
| Total closed trades | `GET /trades` count | "{N} total closed trades" |
| Linked closed trades | `GET /trade-plans` closed, `position_id` non-null count | "{N} linked to a trade plan" |
| Gate Condition 1 | SI-02 condition 1 (20-trade threshold) | MET / NOT MET badge |
| Gate Condition 2 | SI-02 condition 2 | MET / NOT MET badge |
| Gate Condition 3 | SI-02 condition 3 (trade plan adherence) | MET / NOT MET badge |

**Badge style:** reuse existing MET/NOT MET visual language already established for gate-adjacent display (green "MET" pill / amber "NOT MET" pill — consistent with Dashboard's green/amber gate treatment in `dashboard.md` §6).

**Values sourced live from the three endpoints above — never hardcoded.** If ST-01 (BLG-BE-46) remains unresolved at build time, the two count fields correctly show the discrepancy as-is (e.g. "20 total closed trades" / "0 linked to a trade plan") rather than being suppressed or approximated — this is the intended visibility purpose of the story.

## 5. States

| State | Behaviour |
|-------|-----------|
| Loading | Skeleton placeholder for the section body |
| Error (any of the 3 endpoints) | Section shows "Unable to load gate status" — does not block rest of Reports page |
| Empty (no closed trades) | All counts show 0; all conditions show NOT MET |

## 6. §13 Compliance

Display-only, no automated action. Not an advisory or recommendation — purely a status readout of existing gate mechanics.

## 7. Playwright Coverage Required

Per CLAUDE.md frontend-visible-change rule (ST-06 AC-05): section presence/collapse, two-count display, 3-condition MET/NOT MET rendering, loading/error states.
