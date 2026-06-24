**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-06-24
**Approved by:** Product Owner — 2026-06-24
**Story:** ST-05 — Risk-off exit alerts for existing positions (BLG-FEAT-49)
**Cycle:** 2026-06-24__release-v6.2

---

# UX Specification — Risk-Off Exit Alert (Per Position)

## 1. Placement

**Page:** Positions (`/positions`) — Table View
**New column:** "Alerts" added to Table View (rightmost column before Actions)

Risk-off alerts are regime-driven: they fire when SPY < MA200 (US positions) or FTSE < MA200 (UK positions). The alert must be visible inline per position to let the user identify which positions are affected without cross-referencing market regime status manually.

---

## 2. Alerts Column

### Column Identity

| Attribute | Spec |
|-----------|------|
| Column label | "Alerts" |
| Position | After "Trail Stop" column (ST-02), before "Actions" column |
| Data source | `risk_off_exit` flag from `GET /positions` (new boolean field per position) |
| No-alert display | "—" (dash) |

### Risk-Off Badge

| Element | Spec |
|---------|------|
| Trigger | `risk_off_exit = true` on this position |
| Label | "RISK OFF" |
| Background | `#1E40AF` (blue-800) |
| Text colour | White |
| Font weight | 500 |
| Font size | 11px |
| Shape | Rounded pill |
| `aria-label` | `"Risk-off exit alert: regime signal indicates exit this {US/UK} position"` (market-specific) |

### Market Isolation

- US market position (`market = "US"`) + `risk_off_exit = true`: badge shown (SPY < MA200)
- UK market position (`market = "UK"`) + `risk_off_exit = true`: badge shown (FTSE < MA200)
- US regime does NOT trigger badge on UK positions, and vice versa. Market isolation is enforced server-side (ST-05 AC-04); frontend renders the `risk_off_exit` flag as-is.

---

## 3. Colour Rationale

`#1E40AF` (blue-800) was chosen because:
- Deep blue communicates "institutional caution/regime signal" rather than a position-level error
- Distinct from: trailing stop breach orange (#EA580C), lifecycle state badges (blue-600 for GRACE, red/green/purple/grey), rebalance exit teal (#0891B2)
- Contrast with `#2563EB` (GRACE badge blue-600): RISK OFF uses blue-800 which is darker and structurally distinct in intensity — "RISK OFF" label text prevents colour-only confusion

---

## 4. Alert Clearing

When `risk_off_exit = false` (regime recovered): badge absent, cell shows "—". No manual dismiss needed — alert lifecycle is server-driven.

---

## 5. States

| State | Alerts Column |
|-------|--------------|
| No alert | "—" |
| Risk-off active (this position) | "RISK OFF" deep-blue badge |
| Multiple alert types (future) | Stack badges vertically in cell (this story introduces one type only) |
| Loading | Skeleton cell |

---

## 6. Interactions

Display-only. Alerts badge has no click interaction.

**§13 constraint:** The system presents the regime-derived alert. No automated exit is triggered. Human decides action.

---

## 7. Accessibility

- "RISK OFF" text label is the primary differentiator — colour is supplementary
- `aria-label` includes market context (US/UK) for screen readers

---

## 8. API Dependency

| Endpoint | New field | Type | Description |
|----------|-----------|------|-------------|
| `GET /positions` | `risk_off_exit` | boolean | `true` when this position's market index is below MA200. Set by nightly regime check (ST-05 backend). |
