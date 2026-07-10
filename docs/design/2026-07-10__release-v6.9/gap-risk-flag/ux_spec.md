**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-10
**Approved by:** Product Owner — 2026-07-10
**Story:** ST-02 — Overnight/weekend gap risk flag for open positions (BLG-FEAT-65)
**Cycle:** 2026-07-10__release-v6.9

---

# UX Specification — Overnight/Weekend Gap Risk Flag (Per Position)

## 1. Purpose

Swing positions held overnight/over weekends are exposed to gap risk from earnings releases or major macro events. This surfaces the existing earnings calendar (DS-04) and historical OHLCV statistics together as a proactive, informational risk flag — deterministic only, no directional prediction (§13).

## 2. Placement

**Page:** Positions (`/positions`) — Table View

**Column:** Reuses the existing **"Alerts"** column (introduced v6.2 — ST-05, `risk_off_exit`). Gap Risk is a second, independent alert type in the same cell — badges stack vertically when both are present, per the existing "future alert types" placeholder already documented in `positions.md` §Alerts Column States.

**Grid View:** Gap Risk badge added to the position card, in the same row as the existing Trail/Alerts icons.

**Journal View:** Not shown — read/reflection surface only, consistent with existing convention.

## 3. Gap Risk Badge

| Element | Spec |
|---------|------|
| Trigger | Either (a) an earnings date falls before the position's next trading session, or (b) it is a weekend-hold position flagged at Friday close |
| Label | "GAP RISK" |
| Background | `#D97706` (amber-600) |
| Text colour | White |
| Font weight | 500 |
| Font size | 11px |
| Shape | Rounded pill (matches RISK OFF / BREACH badge shape) |
| No-flag display | "—" (dash), consistent with existing Alerts column convention |

**Colour rationale:** Amber-600 (`#D97706`) is distinct from trail-stop breach orange (`#EA580C`), RISK OFF blue-800 (`#1E40AF`), and all lifecycle-state colours. It reuses the same amber hue family already established for advisory/informational warnings elsewhere on this page (Grace Period Alert Zone, Concentration Limits Warning) — signalling "informational caution," not an action-required or breach state. The "GAP RISK" text label is the primary differentiator; colour is supplementary (§7 Accessibility).

## 4. Tooltip / Expanded Detail

Hover or focus on the badge reveals a tooltip:

```
Gap Risk — AAPL
Earnings: 2026-07-14 (before next session)
Avg overnight gap: ±2.3% (14 historical events)
```

or, for weekend-only holds with no earnings proximity:

```
Gap Risk — AAPL
Weekend hold (flagged at Friday close)
Avg weekend gap: ±1.1% (31 historical events)
```

or, when history is insufficient:

```
Gap Risk — AAPL
Earnings: 2026-07-14 (before next session)
Avg gap: insufficient history (< N events)
```

`N` (minimum event threshold) is a backend-defined constant — frontend renders whatever the API returns verbatim; no client-side threshold logic.

## 5. Trigger Timing

| Trigger | When flag appears |
|---------|-------------------|
| Earnings proximity | As soon as the earnings date falls before the position's next trading session (per DS-04 calendar) |
| Weekend hold | At Friday close (server-computed; frontend renders the flag as returned — no client-side day-of-week logic) |

Both conditions are independent and can co-occur (e.g. Friday close + earnings Monday morning) — tooltip lists both reasons stacked when applicable.

## 6. States

| State | Alerts Column (Gap Risk) |
|-------|---------------------------|
| No flag | "—" |
| Flagged (earnings and/or weekend) | "GAP RISK" amber badge, tooltip with reason(s) + historical stat |
| Insufficient history | Badge still shown (flag condition is independent of history availability); tooltip shows "insufficient history" in place of the average |
| Loading | Skeleton cell (shared with existing Alerts column loading state) |

## 7. Accessibility

- `aria-label="Gap risk flag: {reason}, average gap {value or insufficient history}"`.
- Text label "GAP RISK" is present at all times the badge is shown — colour is never the sole differentiator.
- Tooltip content is also exposed via `aria-describedby` for keyboard/screen-reader access (not hover-only).

## 8. §13 Compliance

Display-only. The flag surfaces a known calendar event (earnings date) and a historical statistic (average gap magnitude) — it does not predict gap direction or magnitude for the upcoming event. No automated action is triggered. Strategy Rules & System Intent Owner sign-off (AC-04) confirms no directional/magnitude prediction is introduced.

## 9. API Dependency

| Endpoint | Field(s) | Description |
|----------|----------|--------------|
| `GET /positions` (existing) | `gap_risk: { flagged: bool, reasons: [...], avg_gap_pct: float \| null, event_count: int, insufficient_history: bool }` | New field on existing read path. If implementation requires a new endpoint instead, the same same-commit `openapi.yaml` / `docs/specs/api_contracts/` / `backend/routers/test.py` registration rules apply per CLAUDE.md. |

## 10. Out of Scope

- No gap direction or magnitude prediction (§13, AC-04).
- No dismiss/acknowledge action — flag lifecycle is fully server-driven, consistent with RISK OFF badge precedent.
- No change to the existing RISK OFF badge or Trail Stop breach badge behaviour.
