**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-06-24
**Approved by:** Product Owner — 2026-06-24
**Story:** ST-03 — Month-end rebalance exit signal generation (BLG-FEAT-47) — UI styling component
**Cycle:** 2026-06-24__release-v6.2

---

# UX Specification — Exit Rebalance Signal Styling

## 1. Placement

**Page:** Signals (`/signals`) — Signals Table

The signals table shows results from `GET /signals`. The `exit_rebalance` signal type introduced by ST-03 must be visually distinct from other signal types, particularly stop exit signals, so the user can instantly distinguish a month-end rebalance action from a stop-triggered exit.

---

## 2. Signal Type Badge

The Signal Type column in the Signals Table renders signal types as styled badges. AC-05 requires `exit_rebalance` to be visually distinct from stop exits.

### Badge Specification by Signal Type

| Signal Type (API value) | Display Label | Badge Colour | Rationale |
|------------------------|--------------|-------------|-----------|
| `exit_rebalance` | "Rebalance Exit" | `#0891B2` (cyan-600) | Teal communicates a planned/scheduled exit — distinct from urgency red of stop exits |
| `stop_exit` | "Stop Exit" | `#DC2626` (red-600) | Red signals an automated stop trigger — consistent with stop/risk loss convention |
| Entry/momentum signal types | Existing label (no change) | No badge (plain text) or existing style | Not affected by this story |

**Badge format:**
- Background: as specified per type
- Text: white
- Font weight: 500
- Font size: 11px
- Shape: rounded pill
- Placement: inline in Signal Type column cell

### Colour Rationale

`#0891B2` (cyan-600) for `exit_rebalance` was chosen because:
- Teal/cyan is not used elsewhere in the signal table or position indicators
- It suggests a scheduled/planned action (contrasted with the urgency of red stop exits)
- It is visually distinct from: stop exit red (#DC2626), lifecycle badge colors, trailing stop breach orange (#EA580C), risk-off deep blue (#1E40AF)

---

## 3. Signal Table Column Impact

No new columns. Only the rendering of the Signal Type column cell changes:
- When signal type is `exit_rebalance`: render teal "Rebalance Exit" pill
- When signal type is `stop_exit`: render red "Stop Exit" pill
- Other types: no change to existing rendering

---

## 4. States

| State | Behaviour |
|-------|-----------|
| `exit_rebalance` signal present | Teal "Rebalance Exit" badge in Signal Type column |
| `stop_exit` signal present | Red "Stop Exit" badge in Signal Type column |
| Mixed types in table | Each row renders its own badge — no interaction between rows |
| Loading | Existing loading skeleton for full table |

---

## 5. Interactions

Display-only. Signal type badge has no click interaction.

---

## 6. Accessibility

Badges use text labels ("Rebalance Exit", "Stop Exit") as the primary differentiator — colour is not the sole means of distinction.

---

## 7. API Dependency

The `exit_rebalance` signal type value is introduced by the ST-03 backend (month-end rebalance logic). Frontend maps API value `exit_rebalance` → display label "Rebalance Exit". The mapping is defined in a client-side constant, not derived at runtime.
