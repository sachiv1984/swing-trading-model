**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-06-22
**Approved by:** Product Owner — 2026-06-22
**Story:** ST-07 (BLG-FE-78) — Trade gate proximity indicator on dashboard
**Cycle:** 2026-06-22__release-v6.1

---

# UX Specification — Trade Gate Proximity Indicator

## 1. Placement

**Page:** Dashboard Homepage (`/`)
**Position:** Below the 5 session-summary cards (existing layout rows 1 and 2), as a new full-width compact strip (`§5 Gate Progress`). Does not displace or modify the Morning Briefing section or the existing 5 session-summary cards.

**Rationale:** The dashboard is viewed daily and represents the user's primary operational entry point. The trade gate (PT-04/SI-02: 20 closed trades required) is a user milestone that directly affects feature availability. Daily visibility on the dashboard gives the user a natural progress reminder without requiring navigation to a separate page. The System Status page is appropriate for infrastructure health; the dashboard is appropriate for user milestone progress.

---

## 2. Component Identity

**Section label:** "Gate Progress" — rendered as a left-aligned label in muted text (consistent with "Trader's Morning Briefing" label weight in §1A).

---

## 3. Data Source

**Endpoint:** `GET /portfolio/gate-metrics` (existing endpoint, BLG-BE-34, live since v5.5)

**Key fields used:**
```json
{
  "closed_trades": 13,
  "gate_threshold": 20,
  "gate_met": false
}
```

No new backend work required for this indicator.

---

## 4. Layout

Full-width compact strip. Single row. No card frame — visually lighter than the session-summary cards. Appears as an inline status line.

**Format (gate not met):**
```
[Gate Progress]  [N]/20 trades  (PT-04/SI-02 gate)   [progress bar: N/20]
```

**Format (gate met):**
```
[Gate Progress]  Gate cleared ✓  (PT-04/SI-02 gate)
```

### Progress Bar

- Slim horizontal bar (4px height), full width of the strip content area
- Fill: proportional to `closed_trades / gate_threshold`
- Colour: green when `gate_met = true`; amber progress otherwise

---

## 5. Element Specification

| Element | Content | Condition |
|---------|---------|-----------|
| Label | "Gate Progress" | Always visible |
| Count | `{closed_trades}/20 trades` | When `gate_met = false` |
| Gate cleared | "Gate cleared ✓" | When `gate_met = true` |
| Gate name | "(PT-04/SI-02 gate)" — muted sub-label | Always visible |
| Progress bar | Proportional fill, amber → green on gate clear | Always visible |

---

## 6. States

| State | Behaviour |
|-------|-----------|
| Gate not met | Count `{N}/20 trades`, amber progress bar, gate name muted |
| Gate met | "Gate cleared ✓" in green, full green progress bar |
| Loading | Single-line skeleton placeholder |
| Error | Strip hidden silently (does not block Dashboard). Does not show error state to user — gate-metrics is non-critical display-only context. |

**Error handling rationale:** If the gate-metrics endpoint fails, the indicator is hidden rather than showing an error, to avoid page-level noise. The dashboard's primary content (session-summary cards, morning briefing) must remain unaffected by this component's failure.

---

## 7. Interactions

- Strip is **display-only**. No click interaction, no navigation link.
- Display updates on page refresh (no polling, consistent with Dashboard data refresh behaviour).

---

## 8. Constraints

- Uses existing `GET /portfolio/gate-metrics` endpoint. No new backend endpoint.
- `§13 compliance`: display-only, informational. No recommendation or automated action.
- Strip should not dominate the Dashboard layout. Visual weight must be lighter than the session-summary cards.
- Threshold (20 trades) is sourced from `gate_threshold` field in the API response — not hardcoded client-side.
