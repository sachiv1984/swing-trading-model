**Owner:** Head of UX & Design
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-15
**Cycle:** 2026-05-15__release-v3.5
**Story:** ST-03 — IT-06 Frontend: Paper Positions Display Panel
**Sign-off:** Head of UX & Design — 2026-05-15 (design gate v3.5)
**Product Owner approval:** Product Owner — 2026-05-15

---

# UX Spec — Paper Account Panel (IT-06)

## 1. Purpose

Display Alpaca paper account positions for US-market tickers alongside the user's real positions on the Positions page. The panel gives users a side-by-side view of how their US positions would have tracked in a paper account against actual market conditions.

§13 constraint: Display-only. No automated order execution. Positions are created in the paper account only via the primary system workflow (human-initiated position open). This panel is a tracking view only.

---

## 2. Placement

**Location:** Positions page — Table View only. Appended below the Strategy Compliance Panel (or below the main table if the Strategy Compliance Panel is collapsed/absent).

**Hidden in:** Grid View, Journal View — consistent with Strategy Compliance Panel scoping.

**Conditional rendering:** Panel is rendered only when `ALPACA_PAPER_API_KEY` is configured. The backend controls this — `GET /portfolio/paper-positions` returns an HTTP 200 response with data when credentials are present; if credentials are absent, the endpoint returns `{"paper_tracking_enabled": false}` and the panel is not rendered. No empty or unconfigured state is visible to the user.

---

## 3. Panel Structure

### 3.1 Panel Header

- Label: **"Paper Account"**
- Sub-label (static, muted): "Hypothetical tracking — US market positions only. Not real capital."
- Expand/collapse chevron control
- Default: **expanded** when credentials are configured and paper positions are present; **collapsed** when no paper positions exist

### 3.2 Panel Body: Paper Positions Table

Rendered when `GET /portfolio/paper-positions` returns one or more positions.

| Column | Source Field | Format |
|--------|-------------|--------|
| Ticker | `ticker` | Uppercase |
| Paper Entry | `paper_entry_price` | USD to 2dp (e.g. `$142.30`) |
| Current Price | `current_market_price` | USD to 2dp |
| Paper P&L ($) | `paper_pnl_usd` | Signed USD, 2dp; green if positive, red if negative |
| Paper P&L (%) | `paper_pnl_pct` | Signed percentage, 2dp; green if positive, red if negative |
| Date Opened | `date_opened` | `DD MMM YYYY` |
| Size | `position_size` | Integer (shares) or decimal (fractional) |

### 3.3 Empty State (credentials configured, no paper positions)

Rendered when `GET /portfolio/paper-positions` returns an empty positions array.

- Message: "No paper positions tracked. Open a US market position to begin tracking."
- Panel: collapsed by default in this state

### 3.4 Error State (sync active, API unavailable)

Rendered when `GET /portfolio/paper-positions` returns an error (5xx or timeout).

- Message: **"Paper tracking temporarily unavailable."**
- Muted, no icon. Does not break or hide the Positions page.
- Retry not required — next page refresh will re-attempt.

---

## 4. Behaviour Rules

- Panel does not appear at all when `ALPACA_PAPER_API_KEY` is not configured.
- Panel is US-market only: non-US tickers never appear in this panel.
- Sync is best-effort: if a paper sync failed silently, the panel may show stale data. A "Last synced" timestamp is not required for v3.5 (out of scope).
- No interaction with real positions: the panel is read-only display. No action buttons (no exit, no plan buttons).

---

## 5. §13 Compliance Note

Paper trading integration is §13 compliant:
- Positions created only by human action via the primary system position-open workflow
- This panel is display-only — no automated recommendation or order execution
- Hypothetical P&L shown is for tracking purposes only; no signal is generated from it

---

## 6. API Dependency

| Endpoint | Purpose |
|----------|---------|
| `GET /portfolio/paper-positions` | Returns paper account positions with P&L comparison vs system positions. Returns `{"paper_tracking_enabled": false}` when credentials absent. |

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-15 | Initial design — v3.5 design gate. Head of UX & Design approved. Product Owner approved 2026-05-15. |
