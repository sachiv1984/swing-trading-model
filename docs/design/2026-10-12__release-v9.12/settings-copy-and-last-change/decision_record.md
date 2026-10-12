**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-12__release-v9.12
**Stories:** ST-20 (EPIC-03, BLG-FE-201), ST-26 (EPIC-04, BLG-SEC-41)

# Decision Record — Settings: Strategy Parameter Helper Text and the Last-Change Line

## 1. Problem

**ST-20:** the four read-only Strategy Parameters on Settings keep helper text that contradicts `strategy_rules.md`:
- "Days before stop can trail": during grace the stop is not enforced at all (§6.3).
- "e.g., 5 = Entry − 5×ATR": after entry, the losing stop is current price − 5× ATR (§7.2).
- "e.g., 2 = High − 2×ATR": the code uses current price, with an entry-price floor (§7.2).
- The "e.g." framing no longer fits values that are fixed.

**ST-26:** settings writes are now logged, and the page must show the last change.

## 2. Decision

### 2.1 Helper text (ST-20)

| Field | New helper text |
|-------|-----------------|
| Minimum Hold Days (10) | "Grace period in calendar days. Stops are not enforced or recalculated during grace (§6)." |
| ATR Period (14) | "Lookback for the ATR calculation, in days (§7.1)." |
| Initial Stop (5.0) | "Stop = price − 5×ATR for new and losing positions (§5, §7.2)." |
| Trailing Stop (2.0) | "Stop = price − 2×ATR for profitable positions, never below entry (§7.2)." |

Each line ends with a period and states the rule in force. The numbers come from the strategy constants module that ST-21 introduces, not from literals. Until ST-21 lands, they come from the existing `src/lib/strategyParameters.js`. This is wording only, so code review of the static text may substitute for staging sign-off (CLAUDE.md §2, FI-P3-02). The Playwright text assertions are updated in the same story (AC).

### 2.2 Last-change line (ST-26)

- **Placement:** in the save bar, to the left of the Save button. `text-xs text-slate-600 dark:text-slate-400`, `data-testid="settings-last-change"`.
- **Format:** "Last change: {Field label} {old} → {new} · {d MMM yyyy, HH:mm} · {source}". Values use the canonical number format. The time is the viewer's local time.
- **Multiple fields in one save:** "Last change: {first field label} {old} → {new} and {n} more · {time} · {source}". The full list is in a `title` tooltip.
- **Source labels:** `settings_page` → "Settings page"; anything else → "API".
- **Empty state:** "No changes recorded yet."
- **After a save,** the line updates from the refetched settings. Nothing is computed client-side.
- **Narrow screens:** the line wraps above the Save button, full width.
- **Data:** recommended as a `last_change` object on `GET /settings`, so no new route is needed. A separate route would bring the full CLAUDE.md §2 registration chain.

## 3. §13 Compliance

Display-only. The audit trail records changes. It does not gate or automate anything.

## 4. Frontend Spec Impact

`settings.md` v1.8 → v1.9: §1 helper text (ST-20) and a new §Last Change Line under §Saving Settings (ST-26).

## 5. Obligations for Sprint Execution

- ST-26 is sequenced after ST-16, ST-20 and ST-21 (RISK-05).
- ST-26's migration is recorded in `data_model.md` and applied on staging and production (Human-Delegation, RISK-01).
- `settings_endpoints.md` and `openapi.yaml` describe `last_change` in the same commit.

## 6. Testability (CLAUDE.md §2)

- ST-20: Playwright text assertions on all four helper lines.
- ST-26: Playwright, mocked `GET /settings` with `last_change` → the line text. With `last_change: null` → "No changes recorded yet."

## 7. Approval

Head of UX & Design: confirmed, 2026-10-12.
Product Owner: confirmed, 2026-10-12.
