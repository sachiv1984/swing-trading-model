**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-12__release-v9.12
**Story:** ST-22 (EPIC-03, BLG-FE-207)

# Decision Record — Grace Period Panel: Link Rows to Positions and Align the Text

## 1. Problem

The Risk Dashboard's Grace Period panel lists grace positions with no route to the position. Its text has also drifted from `risk_dashboard.md` §5.2:

| Element | Shipped | Spec |
|---------|---------|------|
| Heading | "Grace Period" | "Grace Period Positions" |
| Badge | "N positions" | "N positions in grace period" |
| Entry date | `dd MMM yy` | DD MMM YYYY |

The Positions page has no deep link that brings one position into view. Its only deep link, `?exit={id}`, opens the exit dialog, which is the wrong action for a grace position.

## 2. Decision

### 2.1 Text: the spec wins

The shipped text is aligned to §5.2. The spec's wording is more specific, and the four-digit year matches the canonical date format used elsewhere on the Risk Dashboard.
- Heading: "Grace Period Positions".
- Badge: "1 position in grace period" / "{N} positions in grace period".
- Entry date: `dd MMM yyyy`.

§5.2 is also amended to describe the shipped row layout (one row per position, not a table). The fields and the order are unchanged.

### 2.2 Row link

- Each row is a link to `/#/Positions?position={id}` with `aria-label="Open {TICKER} on Positions"`. A trailing `ChevronRight` icon (14 px, `text-slate-600 dark:text-slate-400`, `aria-hidden`) shows that the row is a link.
- Hover: `hover:bg-slate-200/60 dark:hover:bg-slate-700/40` (a light+dark pair, per `design_system.md`). Focus: the default `focus-visible` ring (§Focus indicator contrast).

### 2.3 Positions deep link `?position={id}`

- On load, Positions finds the position in the current view (Table or Grid), scrolls it to the centre of the viewport, and applies `ring-2 ring-cyan-500` with `data-highlighted="true"`.
- **Timing:** the highlight holds for 2000 ms, then is removed with no transition. This is a new timing parameter, recorded here per §6's motion and timing rule. 2 s is long enough to locate the row after the scroll, and short enough not to look like a persistent state.
- The parameter is then stripped with `replace`, as `?exit=` is. If the position is not in the list (closed, or filtered out by market), the parameter is stripped and nothing else happens.
- Under `prefers-reduced-motion`, the scroll is instant rather than smooth. The highlight is unchanged.

## 3. §13 Compliance

Navigation and text only. No AI. No action is taken on the position.

## 4. Frontend Spec Impact

- `risk_dashboard.md` v0.1.12 → v0.1.13: §5.2 (text, row layout, link).
- `positions.md` v2.15 → v2.16: new §Position Deep Link.

## 5. Testability (CLAUDE.md §2)

- Playwright: clicking a grace row lands on Positions with that position's row visible and `data-highlighted="true"` (AC 1).
- Heading, badge and date format: wording only (FI-P3-02). Code review of the static text is sufficient, and the Playwright test above can also assert them at no extra cost.

## 6. Approval

Head of UX & Design: confirmed, 2026-10-12.
Product Owner: confirmed, 2026-10-12. The Product Owner prefers the spec's wording to the shipped text, so §5.2 is not amended to the shipped wording.
