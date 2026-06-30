**Filed by:** Base44 Frontend Prompt Owner
**Feature slug:** r-multiple-reflection-fix
**Version:** v1
**Story:** ST-02 (BLG-FE-79, EPIC-01, v6.3)
**Filed:** 2026-06-30
**Integration status:** Implemented directly (agent-mediated — no Base44 platform submission)

---

# Base44 Prompt — Fix R-multiple on Trade Reflection Page

## Context

File: `src/pages/TradeReflection.js`

The Reflection page displays a card grid of closed trades. Each card has three data cells: P&L, R-Multiple, and Hold. The R-Multiple cell currently shows "—" for every trade.

Root cause: `src/api/base44Client.js` — `TradeReflection.list()` maps `r_multiple: t.r_multiple ?? null` from the `/trades` API response. The backend (`trade_service.py`) does not return a field named `r_multiple`; it returns `net_r_multiple`. So `t.r_multiple` is always `undefined`, always falling back to `null`, always rendering "—".

## The change

### 1. `src/api/base44Client.js` — fix field name in TradeReflection.list()

In the `.map()` inside `TradeReflection.list()`, change:

```js
r_multiple: t.r_multiple ?? null,
```

to:

```js
r_multiple: t.net_r_multiple ?? null,
```

`net_r_multiple` is the exact field name returned by `GET /trades`. It is null when the trade has no stop price on record (the backend returns `null` from `_compute_net_r()` when `stop_price_at_entry` is None).

### 2. `src/pages/TradeReflection.js` — display and colour for null R-multiple

Current code (lines 101–102):

```jsx
<div className={cn("text-sm font-semibold", (r.r_multiple ?? 0) >= 0 ? "text-emerald-400" : "text-rose-400")}>
  {r.r_multiple != null ? `${r.r_multiple >= 0 ? "+" : ""}${r.r_multiple.toFixed(2)}R` : "—"}
</div>
```

Replace with:

```jsx
<div className={cn("text-sm font-semibold", r.r_multiple == null ? "text-slate-400" : r.r_multiple >= 0 ? "text-emerald-400" : "text-rose-400")}>
  {r.r_multiple != null ? `${r.r_multiple >= 0 ? "+" : ""}${r.r_multiple.toFixed(2)}R` : "N/A"}
</div>
```

Changes:
- "—" → "N/A" for trades with no stop loss recorded (AC-02: clearly labelled, not a silent dash)
- Colour when null: `text-slate-400` (neutral) instead of `text-emerald-400` (the old `?? 0 >= 0` always evaluated true)

## API contract

`GET /trades` — returns `{ trades: [...] }`

Each trade object includes:

| Field | Type | Notes |
|-------|------|-------|
| `net_r_multiple` | `float \| null` | R-multiple net of transaction costs. `null` when `stop_price_at_entry` is not recorded for the trade. Computed as `(exit_price - entry_price) / (entry_price - stop_price_at_entry)` adjusted for costs. |

No new endpoints required.

## Behaviour rules

- When `net_r_multiple` is a positive float: display `+{value}R` in `text-emerald-400`
- When `net_r_multiple` is a negative float: display `{value}R` in `text-rose-400`
- When `net_r_multiple` is null: display `N/A` in `text-slate-400`
- Values formatted to 2 decimal places (`toFixed(2)`)

## Non-functional rules

- No other columns on the Reflection page are affected (P&L, Hold, exit reason badge, ticker, market badge, exit date)
- `TradeReflection.filter()` (the per-trade reflection modal) is not modified
- No new imports required

## Acceptance criteria

- AC-01: R-multiple is displayed as a numeric value for all closed trades with sufficient data
- AC-02: Trades with no stop loss recorded show "N/A" (not "—")
- AC-03: No regression to other Reflection page columns
