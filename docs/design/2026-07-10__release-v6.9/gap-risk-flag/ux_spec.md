**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.1
**Last Updated:** 2026-10-07 (v9.10 ST-14, BLG-BE-136 — §3–§6 trigger and timing aligned with the code after the ST-13 ruling: weekend-hold trigger removed; earnings US-only, after today and on or before the next trading day); prior — 2026-07-10
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
| Trigger | An earnings date falls after today and on or before the position's next trading day, for a US position (see §5). ~~Or a weekend-hold position flagged at Friday close~~ — removed v9.10 (ST-14). |
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

~~or, for weekend-only holds with no earnings proximity~~ — removed v9.10 (ST-14): there is no weekend-only flag. A Friday-to-Sunday view of Monday earnings shows the weekend gap statistic instead of the overnight one.

As shipped, the reason line reads "Earnings due by next trading session" (v9.10 label, `docs/design/2026-10-06__release-v9.10/gap-risk-trigger-label-alignment/decision_record.md`).

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
| Earnings proximity | When the earnings date (DS-04 calendar) is after today and on or before the next trading day: tomorrow when viewed Monday to Thursday, the following Monday when viewed Friday to Sunday. Not on the earnings day itself (day 0). US positions only. Server-computed; the frontend renders the flag as returned, with no client-side day-of-week logic. |
| ~~Weekend hold~~ | Removed v9.10 (ST-14, BLG-BE-136): it flagged every position each Friday, contrary to §13 Binding Condition 6. |

v9.10 (ST-13 ruling, `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md` addendum): day 0 is excluded because a before-open release has already gapped and the data cannot tell before-open from after-close; UK tickers are excluded because `strategy_rules.md` §4.2.3 is US-only.

## 6. States

| State | Alerts Column (Gap Risk) |
|-------|---------------------------|
| No flag | "—" |
| Flagged (earnings) | "GAP RISK" amber badge, tooltip with reason + historical stat |
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
