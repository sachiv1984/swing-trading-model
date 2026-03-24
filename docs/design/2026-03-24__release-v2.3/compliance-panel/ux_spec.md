**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner — 2026-03-24
**Cycle:** 2026-03-24__release-v2.3
**Story:** ST-01 (BLG-FEAT-11)

---

# UX Spec — Strategy Compliance Score Panel

## Placement

Collapsible panel appended below the Positions table view (Table View only). Hidden in Grid View and Journal View — compliance is a monitoring surface, not a per-entry surface.

Label: **"Strategy Compliance"** with an expand/collapse chevron.

## Panel Layout

Compact header row:
- Overall compliance status: **"Compliant"** (green) / **"Needs Attention"** (amber) / **"Review Required"** (red) based on per-position flags below
- N of M positions fully compliant label (e.g. "3 of 4 positions compliant")

Per-position table (inside panel, expandable):

| Column | Source | Display |
|--------|--------|---------|
| Ticker | positions data | text |
| Stop Compliance | derived: stop_distance vs ATR ratio | ✅ / ⚠️ |
| Stop Age | days since last stop update | N days / "Not set" |
| Size Compliance | position size vs ATR recommendation | ✅ / ⚠️ |

## States

- **Loading:** spinner, no skeleton — panel collapses until data ready
- **No positions:** panel hidden (nothing to assess)
- **All compliant:** green header, panel collapsed by default
- **One or more non-compliant:** amber/red header, panel expanded by default

## Interactions

- User can manually expand/collapse regardless of default state
- No actions available from this panel — display-only
- No links to other pages from this panel

## Constraints

- §13.3: display-only. No automated notification, alert, or action from this panel.
- Strategy Rules & System Intent Owner DoQ sign-off required at delivery verification.
- Backend provides computed compliance flags — no frontend-side computation of ATR ratios.

## Scope exclusions

- No historical compliance trending
- No configurable thresholds from this panel
- No export
