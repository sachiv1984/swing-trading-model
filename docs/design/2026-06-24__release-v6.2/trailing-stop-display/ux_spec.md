**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-06-24
**Approved by:** Product Owner — 2026-06-24
**Story:** ST-02 — Trailing stop display and breach badge (BLG-FEAT-46)
**Cycle:** 2026-06-24__release-v6.2

---

# UX Specification — Trailing Stop Display and Breach Badge

## 1. Placement

**Page:** Positions (`/positions`) — Table View and Grid View
**New column:** "Trail Stop" added to Table View
**Grid View:** Trailing stop value added to position card summary

The trailing stop is a new computed field that supplements the existing `initial_stop`. Both values must be visible simultaneously so the user can see the ratchet relationship.

---

## 2. Table View — Trail Stop Column

### Column Identity

| Attribute | Spec |
|-----------|------|
| Column label | "Trail Stop" |
| Position | After existing "Stop" column (renamed "Initial Stop" for clarity) |
| Data source | `current_trailing_stop` from `GET /positions` |
| Format | Native currency, 2dp (£ or $, matching `initial_stop` format) |
| Null display | "—" (dash) when `current_trailing_stop` is null (not yet computed) |

### Rename of Existing "Stop" Column

The existing Stop column is renamed to "Initial Stop" to distinguish it from the new Trail Stop column. Label text change only — no data or behaviour change.

---

## 3. Breach Badge

**Trigger condition:** `current_price ≤ current_trailing_stop`

**Display:** Amber-orange badge below the trailing stop value in the Trail Stop column cell.

| Element | Spec |
|---------|------|
| Label | "⚠ BREACH" |
| Background | `#EA580C` (orange-600) |
| Text colour | White |
| Font weight | 500 |
| Font size | 11px |
| Shape | Rounded pill |
| Placement | Below the stop value in the same table cell |
| `aria-label` | `"Trailing stop breach: current price is at or below trailing stop level"` |

**Non-breach state:** Stop value only, no badge. No empty space reserved for the badge.

### Colour Rationale

`#EA580C` (orange-600) was chosen to be visually distinct from:
- Lifecycle state badges: blue (#2563EB), red (#DC2626), green (#16A34A), purple (#7C3AED), grey (#6B7280)
- Grace Period Alert Zone: amber panel background (#FEF3C7 / #D97706)
- Risk-off exit badge: deep blue (#1E40AF) — specified in risk-off-exit-alert/ux_spec.md

Orange is also an appropriate colour for a breach condition — it conveys urgency without the red/danger tone reserved for lifecycle states.

---

## 4. Grid View

In the position card summary, display both stop values:
- "Stop" → initial stop value (existing)
- "Trail" → trailing stop value (new; null: "—")
- Breach indicator: when breach condition met, append ⚠ icon inline after the trailing stop value

Grid View breach indicator is a lighter treatment (icon only, no pill) to avoid cluttering compact card layout.

---

## 5. States

| State | Table View | Grid View |
|-------|------------|-----------|
| Normal (no breach) | Trail Stop value only | Trail value in summary |
| Breach | Value + "⚠ BREACH" orange badge | Value + ⚠ icon |
| Null stop | "—" dash | "—" dash |
| Loading | Skeleton cell | Skeleton in card |

---

## 6. Interactions

Display-only. No click interaction on the trail stop value or breach badge.

**§13 constraint:** The system presents the trailing stop computation. No automated action is taken on breach. Human decides all exit actions.

---

## 7. Accessibility

- Badge uses `aria-label` (specified above) — colour is not the sole differentiator
- "⚠" icon is decorative (role="presentation") — text label carries the meaning
- Stop value and badge are co-located in the same cell for screen reader linearity

---

## 8. API Dependency

| Endpoint | New field | Type | Description |
|----------|-----------|------|-------------|
| `GET /positions` | `current_trailing_stop` | number \| null | ATR-based trailing stop, updated nightly by ST-01 service |
