**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-08-08
**Cycle:** 2026-08-08__release-v8.5
**Story:** ST-10 (BLG-FE-92, EPIC-04)

# UX Decision Record — Empty-State Microcopy Pattern

## 1. Problem

`BLG-FE-92`'s problem statement ("empty states across pages use inconsistent copy tone and layout — no shared pattern") predates a closer look at the current state of the app. The **mechanism** is already shared and consistently applied: `src/components/ui/DataState.js`'s `empty` branch (icon + heading + body, per `design_system.md` §Data States) is already the canonical wrapper, and is already in use across at least 10 pages (`Watchlist.js`, `Positions.js`, `TradePlans.js`, `Notifications.js`, `Screener.js`, `PerformanceAnalytics.js`, `TickerUniverse.js`, `TradePlan.js`, `WeeklyDigest.js`, `Dashboard.js`). The actual gap is narrower than the backlog item assumed: **microcopy tone/punctuation** is not consistent across call sites. This is classified Design Required per `design_gate_prompt.md` §6 (the AC ships a documented pattern applied live this cycle) — scoped as a lightweight decision record, since the layout/component question is already settled.

## 2. Audit findings

| Page | `emptyHeading` | `emptyBody` |
|------|----------------|-------------|
| Watchlist | "Your watchlist is empty" | "Add tickers you're monitoring for entry opportunities." |
| Positions | "No open positions" | "Enter a trade to see your positions here." |
| Notifications | "No notifications yet" | "Alert notifications will appear here when triggered." |
| TradePlans | "No trade plans yet." | "Create a trade plan before opening your next position." |

Three of four already conform to a consistent shape. `TradePlans.js`'s heading is the one outlier — it carries a trailing period; the other three don't.

## 3. Decision — the shared pattern

- **Heading:** 2–5 words, sentence case, **no trailing period** (it's a label, not a sentence), states what's missing — either `"No <noun>"` / `"No <noun> yet"` (when the content is something that accrues over time — notifications, positions, trade plans) or `"Your <noun> is empty"` (when the content is something the user actively curates — the watchlist).
- **Body:** exactly one sentence, present tense, states the concrete next action the user can take to populate the view (not a generic "nothing here"). Ends with a full stop.
- **Icon:** contextual to the content type (already the case at all four existing sites — no change needed).

## 4. Application (AC: "applied to at least 3 pages")

The pattern is already satisfied, as written, at **3 of the 4 audited pages** (Watchlist, Positions, Notifications) — no change needed there. The one non-conforming site is fixed as part of this story's implementation:

- `TradePlans.js`: `emptyHeading` changes from `"No trade plans yet."` to `"No trade plans yet"` (drop the trailing period only — wording otherwise unchanged).

Any additional `empty=`/`emptyHeading` call sites found during implementation beyond the four audited here should be checked against this pattern and aligned in the same PR; none are currently known to deviate beyond the one listed above.

## 5. Scope boundary

Covers `DataState`'s `empty` branch microcopy only — not `error` or `loading` copy (different, already-covered states per `design_system.md` §Data States), not the `compact`/`inline` variants' sizing (unchanged), and not a new component (none needed).

## §13 check

Static copy convention; no automated decision or AI call. Not applicable.
