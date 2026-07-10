**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-10
**Approved by:** Product Owner — 2026-07-10
**Story:** ST-01 — On-demand pre-entry rule recheck for open positions (BLG-FEAT-64)
**Cycle:** 2026-07-10__release-v6.9

---

# UX Specification — On-Demand Compliance Recheck (Per Position)

## 1. Purpose

SI-01 validates the 5 strategy checks only at entry time. Once a position is open there is currently no way to see whether it would still pass those checks against current conditions (current regime, current signal conditions, current heat/sizing). This introduces a manual, on-demand, single-position recheck — re-applying the existing deterministic SI-01 rule set against current state. It does not replace or duplicate SI-02 (drift detection), which remains gated.

## 2. Placement

**Page:** Positions (`/positions`)

**Trigger:** "Recheck Compliance" action, available per open position in:
- **Table View** — icon button in the Actions column (alongside existing Trail Stop action)
- **Grid View** — action button on the position card footer

**Not available in:** Journal View (read/reflection surface — no live actions per existing UX Notes convention).

## 3. Interaction Flow

1. User clicks "Recheck Compliance" on a position.
2. Frontend calls `GET /positions/{position_id}/compliance-recheck`.
3. Loading state: button shows inline spinner, disabled during request.
4. On response: a modal opens — **Compliance Recheck Panel** — reusing the visual pattern of `PreEntryValidationPanel` (`src/pages/TradePlan.js`).
5. User closes the modal to dismiss (✕ or click-outside). No state persists after close — this is a point-in-time check, not a stored flag.

## 4. Compliance Recheck Panel (Modal)

### 4.1 Layout

```
┌─────────────────────────────────────────────────────────┐
│ ⚡ COMPLIANCE RECHECK — AAPL              [Fail]    [✕] │ ← header
├─────────────────────────────────────────────────────────┤
│ Checked against current conditions, not entry-time.     │ ← context line
├─────────────────────────────────────────────────────────┤
│ ✓  Regime Gate                                          │ ← check item (pass)
│ ⚠  Sector Concentration — 2 positions in Energy sector  │ ← check item (warn + detail)
│ ✗  Cash Constraint — Insufficient buying power           │ ← check item (fail + detail)
│ ✓  Earnings Proximity                                   │
│ ✓  Sizing Validity                                       │
│                                                           │
│ ☐  I acknowledge the advisory result                    │ ← override checkbox (warn/fail only)
└─────────────────────────────────────────────────────────┘
```

Reuses the exact 5 SI-01 rule keys, labels, and pass/warn/fail badge colours already canonical in `PreEntryValidationPanel` (`strategy_rules.md` §4.2):

| Rule Key | Display Label |
|----------|---------------|
| `regime_gate` | Regime Gate |
| `cash_constraint` | Cash Constraint |
| `sector_concentration` | Sector Concentration |
| `earnings_proximity` | Earnings Proximity |
| `sizing_validity` | Sizing Validity |

### 4.2 Header Status Badge

| Status | Badge colour | Condition |
|--------|--------------|-----------|
| Pass | Emerald (green) | All 5 checks pass |
| Warn | Amber (yellow) | 1+ warn, 0 fail |
| Fail | Red | 1+ fail |

Matches `PreEntryValidationPanel`'s existing badge palette exactly — no new colour introduced.

### 4.3 Context Line

Fixed text under the header: **"Checked against current conditions, not entry-time."** — this disambiguates the recheck from the original entry-time validation shown on the trade plan, preventing user confusion about which snapshot is being displayed.

### 4.4 Override Acknowledgement

Shown only when overall status is Warn or Fail — identical checkbox pattern to `PreEntryValidationPanel`. Checking it does not change position state or trigger any action; it is a display-only acknowledgement local to the modal session (not persisted), consistent with AC-03 (on-demand only, no automation).

### 4.5 States

| State | Panel |
|-------|-------|
| Loading | Spinner in modal body, header shows position ticker only |
| Success | Full check list as above |
| Error (API failure) | "Recheck unavailable — try again" with retry button |

## 5. §13 Compliance

Display-only. This is a re-application of the existing deterministic SI-01 rule set against current inputs — no new statistical model, scoring, or prediction is introduced. No automated action (exit, alert, notification) is triggered by a Fail result; the user reviews and decides. Strategy Rules & System Intent Owner sign-off (AC-04) confirms this introduces no new automation/prediction surface.

## 6. Accessibility

- Modal is keyboard-navigable (focus trap, Esc to close).
- Status badge and each check-item icon carry `aria-label` text equivalents (e.g. `aria-label="Cash Constraint: fail — Insufficient buying power"`) — colour/icon is never the sole differentiator, consistent with existing Positions page convention.

## 7. API Dependency

| Endpoint | Response | Description |
|----------|----------|--------------|
| `GET /positions/{position_id}/compliance-recheck` | `{ overall_status, checks: [{ rule_key, status, detail }] }` | New endpoint. Must be added to `docs/reference/openapi.yaml` and `docs/specs/api_contracts/` (`## GET /positions/{position_id}/compliance-recheck`) in the same commit, and registered in `backend/routers/test.py` per CLAUDE.md hard rules. |

## 8. Out of Scope

- No polling or background automation (AC-03).
- No change to the original entry-time validation display on the trade plan.
- No interaction with SI-02 (drift detection) — that remains a separate, gated capability.
