**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-06__release-v9.10
**Stories:** ST-08 (EPIC-02, BLG-FE-198), ST-09 (EPIC-02, BLG-FE-199)

# Decision Record — Exit Dialog Pre-Selection and Morning Briefing Exit-Conditions Card

One record covers both stories because the slice requires them to share one predicate (ST-09 sequencing note).

## 1. Problem

The system already knows when a position meets a `strategy_rules.md` §8 exit condition: a post-grace stop breach (§8.1) or a risk-off regime (§8.2). Two places ignore that:

- **`ExitModal.js`** always opens with "Manual Exit" selected.
- **The Morning Briefing** has no place that lists these positions.

The existing "Positions to Watch" card (`ExitZoneCard.js`) counts grace-period alerts, which is a different signal.

## 2. Decision

### 2.1 Shared predicate (one implementation, used by both)

`getExitCondition(position)` is a pure function in a shared `src/lib/` module. It returns `{ reason, note } | null`:

| Priority | Condition | `reason` (matches existing `ExitModal` values) |
|----------|-----------|------------------------------------------------|
| 1 | `risk_off_exit === true` | `"Risk-Off Signal"` |
| 2 | `grace_period === false` **and** `current_trailing_stop > 0` **and** `current_price <= current_trailing_stop` | `"Stop Loss Hit"` |
| — | otherwise | `null` |

- Risk-off ranks first because §8.2 "applies regardless of stop position".
- The breach comparison uses the same GBP-basis fields as the existing breach badge (`Positions.js`), so the badge, the dialog and the card can never disagree.
- The grace check is the difference from the badge: §6.3 says no stop-based exit recommendation may be generated during grace.

### 2.2 Exit dialog pre-selection (ST-08)

- On open, `exit_reason` is seeded with `getExitCondition(position)?.reason ?? "Manual Exit"`. The user can change it freely.
- A one-line note appears directly under the Exit Reason select (`text-xs text-slate-600 dark:text-slate-400`, `Info` icon, `data-testid="exit-reason-preselect-note"`):
  - Risk-off: **"Pre-selected because the {US|UK} market is in a risk-off regime (index below its 200-day average)."**
  - Stop: **"Pre-selected because the price is at or below the trailing stop and the grace period has ended."**
  - Both conditions: the risk-off text, followed by **"The price is also at or below the trailing stop."**
- The note is hidden once the user picks a different reason, because it would no longer describe the selection. It is not shown at all for the Manual Exit default.

### 2.3 Deep link into the exit dialog

The Positions page reads `?exit={position_id}` on load (HashRouter: `/#/Positions?exit=…`). It opens `ExitModal` for that position, with the §2.2 pre-selection, then removes the parameter with `replace` so that Back does not reopen the dialog. An unknown or closed `position_id` is ignored silently. This follows the same pattern as Trade History's `?reflect=` (v9.6 `reflection-reminder`).

### 2.4 Morning Briefing card: "Exit Conditions Met" (ST-09)

- **Visibility:** rendered only when at least one open position returns a non-null `getExitCondition`. While loading, on error, or with no qualifying position, the card is **absent**: no empty state and no skeleton. This satisfies the "absent otherwise" AC, and grace-period errors already surface through Positions to Watch.
- **Placement:** a full-width row inside the Morning Briefing section, **above** the existing five-card grid. The five-column grid layout is therefore unchanged on desktop, and on mobile the card sits first in the stack.
- **Container:** the shared `DashboardCard` styling with a 4px left border in orange-600 `#EA580C`, reusing the existing breach colour. `data-testid="exit-conditions-card"`.
- **Header:** "Exit Conditions Met", with the count beside it.
- **Sub-line:** **"These positions meet a strategy exit condition (§8). Nothing is exited automatically."**
- **Rows:** up to 5, each showing the ticker, a reason pill and a link:
  - Reason pills reuse existing styles: "RISK OFF" (`#1E40AF`) or "STOP REACHED" (`#EA580C`).
  - The link reads **"Review exit"**, targets `/#/Positions?exit={id}` (§2.3), and has `aria-label="Review exit for {TICKER}"`.
- **Overflow:** "+N more", linking to `/#/Positions`.
- **Copy rules:** all copy is descriptive and must pass `scripts/check_ui_copy_forbidden_phrases.py`. The wording deliberately avoids "exit now", "consider…" and "you should".

## 3. §13 Compliance

Display-only. The predicate restates conditions the system already computes and the Positions page already shows (breach badge, RISK OFF badge). Pre-selection is a default the user must confirm; no exit is submitted automatically. No AI call.

## 4. Frontend Spec Impact

- `positions.md` v2.11: new §Exit Dialog Pre-Selection and Deep Link (v9.10).
- `dashboard.md` v3.6 → v3.7: §1A gains "Exit Conditions Met Row (v9.10)", and the layout diagram notes the conditional row.

## 5. Testability (CLAUDE.md §2)

Playwright, with mocked `GET /positions`:

- **Dialog pre-selection:** a risk-off position opens with "Risk-Off Signal" and its note. A post-grace breached position opens with "Stop Loss Hit". An in-grace breached position and an ordinary position both open with "Manual Exit" and no note. Changing the selection hides the note.
- **Deep link:** `?exit=` opens the right dialog and the parameter is cleared afterwards.
- **Card:** present with the correct rows and links when positions qualify; absent when none do.

Predicate unit tests cover the priority order and the grace boundary.

## 6. Approval

Head of UX & Design: confirmed, 2026-10-06.
Product Owner: confirmed, 2026-10-06. Approved: the card is placed as a conditional full-width row rather than a sixth grid card, and risk-off takes priority over stop breach.
