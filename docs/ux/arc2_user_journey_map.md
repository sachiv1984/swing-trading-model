**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-10 (ST-27, EPIC-06, v9.16, BLG-FE-39 — initial map)
**Source:** ST-27 (EPIC-06, v9.16) — BLG-FE-39

---

# User Journey Map: Arc 2 — Screener Discovery → Trade Plan → Execution

## Overview

This maps the Arc 2 journey (Pre-Trade Research & Planning) from finding a candidate to entering the position, as built on `main` after EPIC-01 and EPIC-02 of v9.16 (job-based sidebar, "Plan this", suggested size before shares). It sits alongside `si05_user_journey_map.md`.

**Method:** the journey was walked in the running app against the mock backend used by the arc-level Playwright tests (`tests/e2e/arc2-happy-path.spec.js`, `tests/e2e/trade-plan-lifecycle.spec.js`), and each hand-off was read in source (`Screener.js`, `Signals.js`, `Watchlist`, `Research.js`, `TradePlan.js`, `TradePlans.js`, `TradeEntry.js`). No live staging session was used, so this map covers flow and hand-offs, not visual polish or real-data edge cases (those are in `docs/qa/arc2_e2e_qa_protocol.md` §5).

---

## 1. Entry Points

| Entry | Where | Action offered | Lands on |
|-------|-------|----------------|----------|
| E1 Signals card (new, watchlisted) | Signals | "Plan this" | Trade Plan, pre-filled: ticker, market, entry price, Signal Context panel |
| E2 Screener row | Screener | "Plan this" | Trade Plan, pre-filled: ticker, market, entry price (panel only if a watchlisted signal exists) |
| E3 Screener row | Screener | "Research" | Research View |
| E4 Watchlist row | Watchlist | "Research" | Research View |
| E5 Research View, no plan | Research | "Create Trade Plan" | Trade Plan with **ticker only** |
| E6 Research View, plan exists | Research | "View full plan" | Trade Plan in edit mode |
| E7 Positions row | Positions | Plan icon | Trade Plan linked to that position |

---

## 2. Journey Stages

```
 Discover            Research               Plan                          Execute
┌──────────┐  1   ┌───────────────┐  1   ┌──────────────────────┐   2   ┌──────────────┐  1  ┌───────────┐
│ Screener │─────▶│ Research View │─────▶│ Trade Plan            │──────▶│ Trade Plans  │────▶│ Trade     │──▶ Positions
│ Signals  │      │ signal, heat, │      │ quality score, stop,  │ (Save,│ "Start Trade"│     │ Entry     │
│ Watchlist│      │ quality score │      │ size, thesis, checklist│ list) └──────────────┘     │ (prefill) │
└──────────┘      └───────────────┘      └──────────────────────┘                             └───────────┘
      │                                          ▲
      └──────────── "Plan this" (E1/E2) ─────────┘   1 step, skips Research
```

| Stage | Steps (clicks between pages) | What the user does | What carries over |
|-------|------------------------------|--------------------|-------------------|
| Discover → Plan via "Plan this" | 1 | Clicks "Plan this" on a signal or screener row | Ticker, market, entry price; signal context (E1) |
| Discover → Research | 1 | Clicks "Research" | Ticker |
| Research → Plan | 1 | Clicks "Create Trade Plan" | **Ticker only** — market, entry price and signal are dropped (F-01) |
| Plan | 0 | Enters stop (entry if not carried), reads the suggested size and quality score, writes thesis and R target, ticks the checklist, saves | — |
| Plan → Execute | **2** | Opens Trade Plans, clicks "Start Trade" on the new plan (F-02) | Ticker, market, entry, planned stop (shown for reference), planned shares, plan link |
| Execute | 0 | Enters ATR if not fetched, checks the system stop and risk, creates the position | Plan becomes `active` and linked |

**Shortest path, discovery to entered position:** 4 page changes via "Plan this" (Signals → Trade Plan → Trade Plans → Trade Entry → Positions). Via Research: 5. Before v9.16's "Plan this", `BLG-FE-255` recorded the signal-to-entry path as Signals → Watchlist → Research → Trade Plan → Trade Entry, with the entry price retyped.

---

## 3. Friction Points

### F-01 — Research View's "Create Trade Plan" drops market, entry price and signal (HIGH for UK tickers, MEDIUM otherwise)

`Research.js` navigates to `/TradePlan?ticker={ticker}`. The Trade Plan defaults the missing market to US, so a UK ticker's plan is created as US (wrong currency and FX in the suggested size). The Research View already holds the signal's entry and suggested stop and the signal ID, but none is passed, so the user retypes the entry and gets the Signal Context panel only if the signal happens to be watchlisted. "Plan this" (E1/E2) already carries all of these through `planThisUrl`.

**Backlog:** `BLG-FE-281` (market, P2 — filed by ST-24); `BLG-FE-283` (use the "Plan this" route parameters for entry price and signal, P3).

### F-02 — No way to start the trade from a plan just saved (MEDIUM)

After "Save Plan" on a new plan the page shows "Trade plan saved successfully." but no "Start Trade from Plan": that button renders only in edit mode (`?edit=`), and a newly created plan stays on the create URL. The user must open Trade Plans and find the plan. This is the only stage with 2 steps, and it sits at the decision point.

**Backlog:** `BLG-FE-284` (P3).

### F-03 — The planned stop is free and not pre-filled, but execution stores the formula stop (HIGH — risk)

`trade_plan.md` §5a.3 says Stop Level is pre-filled from the signal's suggested stop (entry − 5×ATR). The code pre-fills only the thesis, entry rationale and confirmation criteria (`TradePlan.js` signal pre-population); the Signal Context panel shows "Suggested stop" but the field stays empty. The suggested size (§4.1) is computed from whatever stop the user types. Trade Entry ignores the planned stop and stores entry − 5×ATR (§5), showing the planned stop "for reference" only. A plan typed with a tighter stop than §5 gives a larger suggested size than §4.1 allows at the stop that will be stored, so the entered position can risk more than the configured percentage unless the user notices Trade Entry's risk figure. `strategy_rules.md` §4.1.1 defines the Stop used in sizing as the entry-time initial stop (§5), so the plan's size should rest on that stop too.

**Backlog:** `BLG-FE-282` (P2).

### F-04 — Watchlist offers Research but not "Plan this" (LOW — maintain)

From the Watchlist the plan is 2 page changes away (Research → Create Trade Plan), against 1 from Signals or Screener. The Research View is the intended stop for a watchlisted candidate (Arc 2's "research then plan" order), so this is kept. Once F-01 is fixed the Research route carries the same data as "Plan this". No item filed.

### F-05 — Plan status after the trade closes (MEDIUM — data)

After the position closes, the plan still shows **Active** on Trade Plans, so the list no longer separates open plans from finished ones. The backend never writes `closed`.

**Backlog:** `BLG-BE-211` (P2 — filed by ST-26).

### What works

- "Plan this" removed the old 5-page path and the retyped entry price (E1/E2).
- The Setup Quality Score appears on both Research and Trade Plan, so the score is visible at both decision points.
- The suggested size sits above Planned Shares and pre-fills it without overwriting a typed value.
- "Start Trade from Plan" pre-fills Trade Entry and links the plan automatically, with a toast naming the linked ticker.

---

## 4. Design Recommendation

**Maintain the current structure; file targeted fixes.** The stage order (discover → research → plan → execute) matches Arc 2's intent, and v9.16's "Plan this" gives a fast path that does not bypass the plan. The friction is at the hand-offs, not in the structure: fix F-03 first (a risk issue), then F-01 and F-02, which each remove a step or a retype. No page needs adding or merging.

---

## 5. Backlog Items Filed

| ID | Title | Priority | Friction |
|----|-------|----------|----------|
| `BLG-FE-282` | Pre-fill the Trade Plan stop from the §5 suggested stop and flag a typed stop that differs | P2 | F-03 |
| `BLG-FE-283` | Carry entry price and signal from Research View's "Create Trade Plan" | P3 | F-01 |
| `BLG-FE-284` | Offer "Start Trade from Plan" right after a new plan is saved | P3 | F-02 |

Already filed this cycle and referenced, not re-filed: `BLG-FE-281` (F-01, market), `BLG-BE-211` (F-05).

**Duplicate cross-check:** checked against the Site Structure & Usability programme items, including the held Phase 3 items `BLG-FE-257` (grace period in one place), `BLG-FE-258` (Journal area), `BLG-FE-259` (Performance page), `BLG-FE-260` (decision-first Positions table), `BLG-FE-261` (Positions cards on narrow screens), `BLG-FE-262` (Positions banner strip), `BLG-FE-263` (tabs on long pages), `BLG-FE-265` (colour tokens); the shipped `BLG-FE-250` (sidebar), `BLG-FE-255` ("Plan this" on Signals and Screener), `BLG-FE-256` (suggested size); and the open `BLG-UX-08` (programme re-review), `BLG-UX-09` ("Plan this" placement on watchlisted cards, §4.1 wording), `BLG-FE-279` (Signal Context follows the Ticker field), `BLG-QA-254` (UK tickers in "Plan this"), `BLG-FEAT-61` (screener-to-watchlist friction audit, gated) and `BLG-FEAT-101` (Dashboard "Plan this"). None covers F-01's entry/signal carry-over, F-02 or F-03.

---

## 6. Sign-Off

- **Head of UX & Design:** Approved (review passes 1 and 2). Sprint Execution Engine (agent-mediated, Head of UX & Design role — §5.3), 2026-11-10. Pending human confirmation at the merge gate.
