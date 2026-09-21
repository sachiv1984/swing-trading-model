**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-21__release-v9.6
**Story:** ST-02 (EPIC-01, BLG-FE-180)

# Decision Record — Stale Marker for Unactioned Trade Plans

## 1. Problem

Trade plans that never progress accumulate on the list with no cue that they are old. The Watchlist already solved the same problem for watchlist entries (`watchlist.md` §Staleness Indicator, v7.9); the Trade Plans list has no equivalent.

## 2. Decision

### 2.1 Which plans (status vocabulary correction)

The sealed slice says "`planned` status" — **no such status exists** (see `trade-plan-clone/decision_record.md` §2.4). The intent — plans *not yet acted on* — maps to the four pre-entry statuses that have no linked position:

`draft`, `research_pending`, `research_complete`, `entry_conditions_set`.

`active`, `closed` and `abandoned` are never marked (already acted on or terminal).

### 2.2 Age basis and threshold

- **Age = whole days since `updated_at`** (`N = floor((now − updated_at) / 24h)`). A plan being edited is being worked; "stale" means untouched. The list already shows and sorts by `updated_at`.
- **Threshold: `N > 14`** — the marker first appears at `N = 15`. The value lives in one named constant (`STALE_PLAN_THRESHOLD_DAYS = 14`) in the list page; not user-editable this cycle.
- Client-side derivation from fields the list already receives. No backend or schema change.

### 2.3 Presentation — reuse the Watchlist staleness language

Placed in the **Status** column, on a second line beneath (or, at wide widths, beside) the existing status badge — the badge is never replaced or recoloured.

| Element | Spec |
|---------|------|
| Text | `"Stale ({N} days)"` |
| Icon | `Clock` (lucide-react) prefix — same icon as the Watchlist marker |
| Style | `text-amber-600 dark:text-amber-400` (explicit light+dark pair) — same tokens as `watchlist.md` §Staleness Indicator |
| Shape | Plain text + icon, **not** a filled pill — keeps it visually distinct from the filled `research_pending` amber status badge (§9) |
| `aria-label` | `"Last updated {N} days ago — plan is stale"` |
| Tooltip (`title`) | `"Last updated {absolute date}. Display only — nothing happens automatically."` |
| `data-testid` | `stale-plan-marker` |

Colour is never the sole carrier: icon + label text together state the condition.

### 2.4 Explicitly out of scope

Display-only (`strategy_rules.md` §3 human-in-the-loop): **no "Keep" action, no auto-abandon, no sweep.** The Watchlist's "Keep" button is deliberately *not* mirrored — a possible follow-up if the marker proves useful.

### 2.5 Motion / timing

None.

## 3. §13 Compliance

Deterministic display rule on existing fields; no AI call. §13 pre-check does not apply.

## 4. Frontend Spec Impact

`docs/specs/frontend/pages/trade_plan.md` v1.14 → v1.15: new §4.6 Stale Plan Marker (with the §4.2 Status-column note).

## 5. Testability (CLAUDE.md §2)

Playwright, with `updated_at` mocked: pre-entry plan at 15 days → marker with "Stale (15 days)"; same status at 10 days → no marker; `active`/`abandoned` plan at 30 days → no marker; boundary at exactly 14 days → no marker.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-21.
Product Owner: confirmed, 2026-09-21 (status set and `updated_at` age basis).
