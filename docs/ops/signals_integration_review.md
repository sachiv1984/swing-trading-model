Owner: Head of Engineering + Frontend Specifications & UX Owner
Class: Working Document (Class 3)
Status: Active
Last Updated: 2026-04-06
Cycle: 2026-04-05__release-v2.5 (ST-05)

---

# Signals Page — Backend Integration Review

## Summary

The Signals page (`src/pages/Signals.js`) has a mixed integration pattern. Core signal data and market status are fetched from the FastAPI backend via `apiFetch`. Position and portfolio data, signal dismissal, and position creation are handled via the legacy Base44 SDK.

---

## Section-by-Section Mapping

### Data Fetching

| Section | Hook / Handler | Data Source | Endpoint / Method | Status |
|---------|---------------|-------------|-------------------|--------|
| Signals list | `useQuery(["signals", topN, lookbackDays])` | FastAPI backend | `GET /signals?top_n=<n>&lookback_days=<n>` | Wired |
| Market status bar | `useQuery(["marketStatus"])` | FastAPI backend | `GET /market/status` | Wired |
| Open positions | `useQuery(["positions"])` | Base44 SDK | `base44.entities.Position.filter({ status: "open" })` | Legacy — not FastAPI |
| Portfolio (cash balance) | `useQuery(["portfolios"])` | Base44 SDK | `base44.entities.Portfolio.list()` | Legacy — not FastAPI |
| Dismiss signal | `dismissMutation` | Base44 SDK | `base44.entities.Signal.update(signalId, { status: "dismissed" })` | Legacy — not FastAPI |
| Create position from signal | `createPositionMutation` | Base44 SDK | `base44.entities.Position.create(positionData)` | Legacy — not FastAPI |
| Mark signal as entered | `handleConfirmPosition` | Base44 SDK | `base44.entities.Signal.update(signalId, { status: "entered" })` | Legacy — not FastAPI |

### UI Sections

| Section | Data | Notes |
|---------|------|-------|
| Market Status Bar (`MarketStatusBar`) | `GET /market/status` response | Correctly uses FastAPI data; auto-refreshes every 5 minutes |
| Summary stats row (New Signals, Total Capital, Avg Momentum, Distribution) | Derived client-side from `/signals` response | No separate backend call; computed from signal list |
| Signals grid (`SignalCard` per signal) | `/signals` response | Correctly wired; auto-refreshes every 60 seconds |
| Position Entry Modal (`PositionEntryModal`) | Base44 SDK on confirm | Uses Base44 for position creation — not FastAPI `POST /positions` |
| "Already held" status overlay | Cross-reference between signals and Base44 positions | Derived client-side: `positions.some(p => p.ticker === signal.ticker)` |

### Auto-Refresh Behaviour

| Query | Interval | Source |
|-------|----------|--------|
| `GET /signals` | 60 seconds | `refetchInterval: 60000` in useQuery |
| `GET /market/status` | 5 minutes | `refetchInterval: 300000` in useQuery |
| Positions / Portfolios | No auto-refresh | Only refreshed on mutation success |

---

## Integration Gaps

### GAP-S01: Signal dismissal and entry bypass FastAPI

**Severity:** High
**Description:** When a user dismisses a signal or converts it to a position, these mutations go through `base44.entities.Signal.update()` and `base44.entities.Position.create()` (Base44 SDK), not through the FastAPI backend. The FastAPI backend does not receive these state changes.

**Impact:**
- Signal status (`dismissed`, `entered`) is stored in Base44, not in the FastAPI database. Any backend logic that reads signal status (e.g. alert deduplication, analytics) will not see these changes.
- Position creation via the Signals page does not trigger the FastAPI `POST /positions` endpoint, so any server-side logic (e.g. ATR calculation, stop-price validation, initial_stop recording) is bypassed.

**Follow-up:** BLG-BE-09-GAP-01 — Wire signal dismissal to `PATCH /signals/<id>` or equivalent FastAPI endpoint. Wire position creation to `POST /positions`. Filed as follow-up backlog item (see below).

### GAP-S02: Portfolio cash balance sourced from Base44, not FastAPI

**Severity:** Medium
**Description:** The `availableCash` prop passed to `MarketStatusBar` is `portfolio.cash_balance` from `base44.entities.Portfolio.list()`. The FastAPI backend maintains its own cash balance via `GET /cash/summary`. These two sources may diverge.

**Impact:** The cash balance displayed on the Signals page may differ from the authoritative balance shown on the Portfolio and Cash pages.

**Follow-up:** BLG-BE-09-GAP-02 — Replace Base44 portfolio fetch with `GET /cash/summary` for the `availableCash` value. Estimated effort: XS.

### GAP-S03: "Already held" position check uses Base44 data

**Severity:** Low
**Description:** The check `positions.some(p => p.ticker === signal.ticker && p.status === "open")` runs against Base44 position data. If a position was created via the FastAPI backend (not via the Signals page), it will not be reflected in Base44 and the "already held" overlay will not trigger.

**Impact:** Signals for tickers with existing FastAPI-backend positions will not show the "already held" status.

**Follow-up:** Resolved automatically when GAP-S01 is fixed (positions will be sourced from FastAPI once the migration is complete). No separate backlog item required.

---

## Improvement Proposals (Prioritised)

1. **[P1] Wire signal state mutations to FastAPI** — Replace `base44.entities.Signal.update()` with calls to a FastAPI endpoint (e.g. `PATCH /signals/<id>`) for dismiss and enter actions. Replace `base44.entities.Position.create()` with `POST /positions`. This is the critical path for data consistency. *Estimated effort: M (requires FastAPI endpoint + frontend wiring).*

2. **[P2] Source cash balance from GET /cash/summary** — Replace the Base44 portfolio query with `apiFetch(${base44.baseUrl}/cash/summary)` to display the authoritative cash balance. *Estimated effort: XS.*

3. **[P3] Add signal count / last-run metadata to GET /signals response** — The page derives `latestSignalDate` from `signals[0].signal_date`. A dedicated metadata field (e.g. `run_at`, `signal_count`) in the response would make this more robust. *Estimated effort: XS (backend only).*

---

## Follow-up Backlog Items

| ID | Title | Priority |
|----|-------|----------|
| BLG-BE-09-GAP-01 | Wire Signals page dismissal and position creation to FastAPI endpoints | P1 |
| BLG-BE-09-GAP-02 | Replace Base44 cash balance on Signals page with GET /cash/summary | P2 |

---

## Conclusion

The core read path (signal list and market status) is correctly wired to the FastAPI backend with appropriate auto-refresh intervals. All write operations (signal dismissal, position creation) and the portfolio cash balance use the legacy Base44 SDK, creating a data consistency risk. GAP-S01 (signal/position mutations) is the highest-priority gap and should be addressed in a future sprint.
