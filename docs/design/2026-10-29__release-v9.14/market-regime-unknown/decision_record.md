**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-29__release-v9.14
**Story:** ST-03 (EPIC-01, BLG-BE-193)

# Decision Record — Unknown Market Regime State

## 1. Problem

When SPY or FTSE data cannot be fetched, `check_market_regime()` sets that market to risk-on with price and MA 0. Every surface then shows "Risk On", so a regime that was never measured looks like a measured one. ST-03 returns an explicit unknown state. The Strategy Rules & System Intent Owner rules what it means for entries (§4.2.1) and the risk-off job (§8.2), and the UI must show it as unknown.

## 2. Decision

### 2.1 Surfaces

The regime is shown in four places. All four get the unknown state:

| Surface | Component | Source |
|---------|-----------|--------|
| Dashboard Card 4 — Signal Status (the AC surface) | `SignalStatusCard.js` `RegimeRow` | `GET /market/status` |
| Signals page market status bar | `MarketStatusBar.js` | `GET /market/status` |
| Customisable Dashboard regime widgets (`market_regime_us`, `market_regime_uk`) | `MarketRegimeCard.js` | `GET /market/regime` |
| Daily Position Monitor | `MonitorModal.js` | `GET /market/regime` (until ST-11 moves it to `getExitCondition()`) |

Today an unknown value already falls through to "RISK-OFF ✗" in `RegimeRow`, and to "Risk Off" in `MarketStatusBar` and `MarketRegimeCard`, because each tests only `=== risk_on`. Both wrong readings are removed.

### 2.2 Display

A third, neutral state. It is never green or red, because neither reading has been measured.

| Surface | Unknown display |
|---------|-----------------|
| Card 4 badge | "UNKNOWN ?" — `bg-slate-200 text-slate-800 dark:bg-slate-500/20 dark:text-slate-300`, `data-testid="regime-unknown-{SPY\|FTSE}"` |
| Signals bar | `HelpCircle` icon + "Unknown" in `text-slate-700 dark:text-slate-300`. The price line reads "Price unavailable", not "$0.00 vs MA200" |
| Regime widget | Slate gradient and border (`from-slate-500/10 to-slate-500/5 border-slate-500/30`), `HelpCircle` icon, pill "Unknown" |
| Monitor | An unknown market produces no "Market risk off" suggestion |

Each unknown display has the same explanation as its accessible description and its hover/focus tooltip (stale-price marker pattern, `docs/design/2026-10-29__release-v9.14/stale-price-marker/decision_record.md` §2.2):

> "{US|UK} market regime could not be measured: index data is unavailable." + the ruling sentence below.

### 2.3 Ruling branches

ST-03's first sub-step is the ruling. All three outcomes are designed, and the unused sentences are deleted at implementation (v9.13 ST-05/ST-06 precedent):

| Ruling | Ruling sentence | Extra display |
|--------|-----------------|---------------|
| (a) Block entries | "New entries in this market are blocked until it is measured." | None |
| (b) Keep the last known regime | "Entries and the risk-off check use the last measured regime: {Risk On\|Risk Off}, {dd MMM, HH:mm}." | Card 4 adds a muted second line "last known: {RISK-ON\|RISK-OFF}" under the badge |
| (c) Risk-on with a warning | "Entries and the risk-off check treat this market as risk-on until it is measured." | None |

The badge always reads "UNKNOWN", whichever branch is ruled. Branch (b) shows the last known value only as secondary text. This meets ST-03 AC 4 ("shows the regime as unknown") under every branch.

### 2.4 States

- **Loading / both queries failed:** unchanged (`DashboardCard` loading and error states).
- **One market unknown, the other measured:** each row shows its own state.

## 3. §13 Compliance

Display only. The badge reports a missing measurement and recommends no action. What the system *does* with an unknown regime is the strategy ruling, not this design.

## 4. Frontend Spec Impact

- `dashboard.md` v3.9 → v3.10: §Card 4 — Signal Status, unknown state.
- `signals.md` v0.6 → v0.7: new §Market Status Bar (records the bar for the first time, with the unknown state and the ST-04/ST-05 FX tile).

The regime widgets and the Monitor have no page spec. Their unknown behaviour is recorded here.

## 5. Obligations for Sprint Execution

- `GET /market/status` returns `is_risk_on: null` and a `regime_status` of `"risk_on" | "risk_off" | "unknown"` per market. `GET /market/regime` returns `status: "unknown"`. Under branch (b) both also carry `last_known_status` and `last_known_at`. Contract (`market_endpoints.md`) and `openapi.yaml` in the same commit.
- `price` and `ma200` are `null` when unknown, not 0, so no surface renders "$0.00".
- The frontend's local fallbacks (`MarketRegime.list()` returns `risk_on` on error; `Dashboard.js` uses `|| "risk_on"`) must default to `"unknown"`, not `"risk_on"`.

## 6. Testability (CLAUDE.md §2)

- Playwright (AC 4): with `/market/status` mocked to return SPY unknown and FTSE risk-on, Card 4 shows `regime-unknown-SPY` with "UNKNOWN" and FTSE "RISK-ON ✓", and the badge has the §2.2 accessible description.
- Playwright: the Signals bar shows "Unknown" and "Price unavailable" for the same mock.
- Unit: `RegimeRow` never renders "RISK-OFF" for `unknown`.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-29.
Product Owner: confirmed, 2026-10-29.
