**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-18__release-v9.18
**Stories:** ST-27 (BLG-BE-223), ST-30 (BLG-SPEC-203) — EPIC-05; ST-33 (BLG-FE-294) — EPIC-06

# Decision Record — Split Detected, Live Unrealised P&L on Reports, Earnings Unknown

## 1. Scope of this record

Three stories that each add or change one data state the user sees about a position or a figure. They are independent; one record keeps the new states consistent.

Spec impact: `positions.md` v2.29 → v2.30 (§Urgency Order tier 0, §Split Detected State, §Earnings Unknown); `reports.md` v0.27 → v0.28 (§Unrealised P&L Card basis); `screener_results.md` v1.11 → v1.12 and `watchlist.md` v0.10 → v0.11 (Earnings cell).

## 2. Split detected (ST-27)

The `strategy_rules.md` split rule (entry, quantity, stop, ATR, R) is ST-27's sub-step 1, approved by the Strategy Rules & System Intent Owner under §12.3 before the build. This record fixes only what the user sees; the arithmetic is the rule's.

### 2.1 Positions

- **Urgency:** a position with a detected, unconfirmed split goes in a new **tier 0, "Split to confirm"**, above tier 1. While unconfirmed, its stop-breach and exit tests are suppressed (slice AC), so without tier 0 the position would fall to tier 4 and look healthy, which is the wrong signal for a position whose figures are wrong.
- **Action needed:** "Split detected — confirm adjustment" as a link-styled button (`text-xs font-medium text-app-warning`, `data-testid="split-detected-{ticker}"`). It opens the confirmation dialog. Grid view and narrow-screen cards show the same line.
- **Stop and To-stop cells:** "Paused: split to confirm" (`text-xs text-app-muted`), no breach badge, no colour band. The P&L % cell shows its value with a muted "pre-split basis" second line.
- **Expanded row:** one line: "{ratio} split on {effective date} ({source}). Stop alerts and exit suggestions are paused for this position until you confirm."
- **Confirmation dialog** (shared `Dialog`; focus trap, Escape = Cancel): title "Confirm {TICKER} {ratio} split". A three-row table "Before → After" for Shares, Entry price and Stop, computed by the rule, plus "Cost unchanged: {cost}". Buttons: "Confirm adjustment" (primary) and "Cancel". Confirming applies the adjustment (one request) and the position returns to its normal tier at the next render.
- **No "Not a split" option** in v9.18: the provider's split history is the source, and an override would need its own rule. If the user cancels, the position stays in tier 0.

### 2.2 Worked example (fixture, matches the slice AC)

Position: 10 shares, entry 200.00 USD, stop 180.00, 2:1 split effective day D, price 104.00 on D.

| | Day D before confirm | After confirm |
|--|----------------------|---------------|
| Tier | 0 "Split to confirm" | 4 (stop distance (104 − 90) ÷ 104 = 13.5%) |
| Stop cell | "Paused: split to confirm" | 90.00 |
| Breach alert / exit suggestion | none | per normal tests |
| Shares × entry | 10 × 200.00 = 2,000.00 (stored, unchanged) | 20 × 100.00 = 2,000.00 (adjusted) |

Without the split state, 104.00 < 180.00 would read as "STOP REACHED" on day D: that is the defect.

UK (`.L`) position: the same table in GBP, from the rule's UK example.

### 2.3 §13

Display and a user-confirmed data correction. Suppression is a deterministic consequence of an unconfirmed data event, defined in `strategy_rules.md` (case (c) write). No AI. The dialog states the arithmetic and makes no recommendation.

## 3. Reports unrealised P&L basis (ST-30)

**Product Owner decision (the user, in session, 2026-11-18): option (a), compute live.**

- `get_estimated_unrealised_pnl()` sums live P&L from `get_positions_with_prices()`, the Positions page's path, so both pages match at the same moment (verified on staging, slice AC).
- **Card text:** the card shows `unrealised_note` verbatim (`reports.md`). The note keeps its tax-year caveat and gains a closing sentence: "Calculated live at current prices, on the same basis as the Positions page." The card header "Indicative Unrealised P&L (current positions)" is unchanged.
- **Failure:** if a price fetch fails for a position, the live path uses that position's last stored price and marks it stale (the Positions page's `price_is_stale` rule). The card then adds "{n} price(s) stale" in `text-app-warning`, the Dashboard Card 2 wording. It never silently mixes bases.
- **Data-source check:** `get_positions_with_prices()` returns `pnl` in GBP per position and `price_is_stale` (`position_endpoints.md`); the report sums `pnl` for open positions in the report's portfolio. No gap. Caller-units: the Positions total and the Reports total must use the same GBP field (first-time-right check 15); ST-30 names it in the commit.
- `DEV-REPORTS-ST06-01` is marked resolved by ST-30 (its AC 3).

## 4. Earnings unknown (ST-33)

### 4.1 Data-source check

`GET /earnings/{ticker}` returns the same null `days_until_earnings` for a failed lookup and for "no upcoming date". `useEarnings` caches the null for the session. ST-33 adds `data_status: "ok" | "unavailable"` (contract `earnings_endpoints.md`, `openapi.yaml`), and the gap-risk response gains the same field for its earnings input.

### 4.2 What the user sees

| `data_status` | `days_until_earnings` | Positions (Earnings cell, expanded row) | Screener (Earnings column) | Watchlist (Earnings cell) |
|---------------|-----------------------|------------------------------------------|----------------------------|---------------------------|
| ok | n ≥ 0 | unchanged | unchanged | unchanged ("Today", "{n}d") |
| ok | null | nothing (as today) | nothing | "—" (as today) |
| unavailable | null | "Earnings: unknown" | "Unknown" | "Unknown" |
| (UK row, Screener) | — | — | nothing; no lookup made | — |

- "Unknown"/"Earnings: unknown": `text-xs text-app-muted`, with a tooltip and `aria-describedby` text "The earnings date could not be fetched. It will be retried." Muted, not warning-coloured: it is a missing-data state, not a gap-risk flag.
- **Gap-risk warning:** when the gap-risk response's earnings input is `unavailable`, the badge is not shown (no data, no flag), and the Positions Alerts cell shows the same muted "Earnings: unknown". It must not use the GAP RISK badge's amber or its wording. The §13 gap-risk review (`decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`, CONDITIONAL) covers flags for known earnings events; an "unknown" line is not a new trigger. ST-33 cites the review's binding conditions in its commit and confirms none is touched.
- **Not cached:** an `unavailable` answer is not stored in the session cache, so the next render retries (slice AC).
- **UK rows on the Screener (scope decision):** the Screener stops looking up earnings for UK rows. `strategy_rules.md` §4.2.3 and the gap-risk flag are US-only, and about 44 of the failing symbols were UK. UK rows show nothing in the Earnings column. Positions and Watchlist keep their current UK behaviour (their badges already follow `days_until_earnings`); this gate does not change them.

## 5. Approvals

- Head of UX & Design: approved (agent-mediated, Design Gate Engine), 2026-11-18.
- Product Owner: approved (the user, in session, 2026-11-18); ST-30 option (a) chosen by the Product Owner.
- ST-27: the split rule itself needs the Strategy Rules & System Intent Owner's dated approval before the build (slice AC, RISK-05).
