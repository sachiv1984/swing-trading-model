**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner
**Approved date:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Items:** ST-14 (BLG-FEAT-03)
**Frontend spec target:** docs/specs/frontend/pages/trade_history.md (update — v1.1 → v1.2)

---

# UX Spec — Slippage Tracking (ST-14)

## 1. Purpose & User Goal

The user wants to understand the quality of their trade execution — specifically, whether their fills are consistently above or below the market price at time of entry. Slippage is a measure of execution discipline.

**User goal:** See per-trade slippage at a glance in the trade history table, and understand their average slippage across all trades without having to calculate it manually.

**Formula (canonical):** `Slippage = (Fill Price − Market Price) / Market Price`

- Negative slippage = filled below market (favourable for buys)
- Positive slippage = filled above market (unfavourable for buys)

---

## 2. UX Design Decision: Display Location

### Decision
- **Per-trade slippage:** new column in the **Trade History table** (trade_history.md)
- **Portfolio average slippage:** new metric in the **Trade History summary stats bar**

### Rationale
The Trade History page is where the user already reviews individual trades with P&L, R-multiple, and exit details. Slippage is a trade-execution metric — it belongs alongside the other per-trade metrics, not on the Analytics page (which focuses on strategy performance). The summary stats bar on Trade History already aggregates trade-quality metrics (win rate, total P&L, averages), making it the natural home for the portfolio average.

---

## 3. Per-Trade Slippage Column — Trade History Table

### 3.1 Column Specification

| Property | Value |
|----------|-------|
| Column header | **Slippage** |
| Source field | Backend-provided `slippage_pct` per trade (computed from Fill Price and Market Price) |
| Format | Signed percentage to 2dp: e.g. `+0.12%`, `–0.08%`, `0.00%` |
| Colour coding | Negative (favourable): green tone (profit colour per design system). Positive (unfavourable): red tone (loss colour). Zero: neutral. |
| Null handling | If `slippage_pct` is null (Fill Price not captured for historical trades): display `—` (em dash, muted, no colour) |
| Position in table | After "P&L %" column, before "Tags" |
| Sortable | Yes — ascending and descending. Null values sort to end. |

### 3.2 Tooltip on Column Header

A small info icon (ⓘ) next to the "Slippage" column header. Hover tooltip:
> **"Slippage = (Fill Price − Market Price) / Market Price"**
> "Negative slippage means you filled below market price (favourable). Positive means above (unfavourable)."

---

## 4. Portfolio Average Slippage — Summary Stats Bar

### 4.1 New Stat

A new metric card added to the summary stats bar at the top of the Trade History page.

| Property | Value |
|----------|-------|
| Label | **Avg Slippage** |
| Value source | Backend-provided `avg_slippage_pct` (computed across all trades with Fill Price captured) |
| Format | Signed percentage to 2dp: e.g. `–0.05%` |
| Colour coding | Same as per-trade: negative = green, positive = red, zero = neutral |
| Null handling | If no trades have Fill Price captured: display `—` with a tooltip: "No Fill Price data available yet." |

### 4.2 Placement

Appended to the right of the existing summary stats:

```
Total Trades | Win Rate | Total P&L | Avg Winner | Avg Loser | Avg Slippage
```

On narrow screens: wraps to a second row.

---

## 5. Historical Trade Handling

Fill Price will not be available for trades entered before this feature is deployed. The frontend handles this gracefully:
- Per-trade: show `—` in the Slippage column for trades without Fill Price.
- Portfolio average: computed from trades that have Fill Price only. The summary stat tooltip (if avg is shown) may note: "Based on [n] trades with Fill Price recorded."

The frontend does not calculate or impute slippage for historical trades. It displays only what the backend provides.

---

## 6. UX Decisions Recorded

| Decision | Rationale |
|----------|-----------|
| Trade History as display location (not Analytics) | Slippage is execution quality per trade; it belongs alongside P&L and R-multiple in the trade record, not on the strategy analytics page |
| Negative slippage = green (favourable) | Counterintuitive naming, but consistent with how traders interpret slippage; tooltip on column header explains the convention |
| `—` for missing Fill Price (not `0.00%`) | Zero would imply perfect execution; `—` correctly signals data absence |
| Signed format with `+`/`–` prefix | Immediately communicates direction without requiring the user to interpret the sign separately |
| Info icon tooltip on column header | The slippage formula and sign convention need one-time explanation; a header tooltip is non-intrusive and discoverable |
