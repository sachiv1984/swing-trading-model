**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-12__release-v9.12
**Story:** ST-23 (EPIC-03, BLG-FE-200)
**Resolves:** RISK-03 (release plan, High — "must resolve before sprint planning seals")

# Decision Record — Light Mode Is a Supported Theme; Light-Theme Colour Tokens

## 1. Question

ST-23's first step is deciding whether light mode is a supported theme. The axe scan finds light-theme `color-contrast` failures on Reports (Monthly: 25 nodes, Tax Year: 14) and Notifications (Preferences: 3, History: 2). The dark theme passes.

The two design-system documents disagree:
- **`docs/specs/frontend/design_system.md`** v1.22 (Class 1, Canonical), §Theme Modes: "Optional: Light Mode toggle available in the header … Theme preference is persisted locally". Since v6.7 it has defined explicit light+dark token pairs: secondary text, form-error rose, skeletons, card hierarchy. v1.9 rules that modals are "not an intentional dark-only exception".
- **`docs/frontend/design_system.md`** v1.0 (Class 2, Living Reference, last updated 2026-05-06), §6: "The app is dark-only in practice … Arc 2 should not assume light mode support." BLG-FE-200 cites this line.

## 2. Decision

**Light mode is a supported theme.**

- The Class 1 canonical document already says so, and Class 1 prevails over Class 2.
- The toggle ships in `Layout.js` (`bg-slate-100 text-slate-900` in light), and its choice persists.
- Five design gates since v6.7 have fixed light-theme defects as defects, not as accepted gaps: `BLG-FE-87/88/95`, the v7.0 heading fix and the v9.1 badge fix.
- Withdrawing the toggle would remove a shipped user preference to avoid 44 nodes of colour fixes.

The Class 2 statement is stale. ST-23 corrects it, as part of AC 1's "tokens added to `design_system.md`".

**Consequence for Sprint Planning:** ST-23 takes its first AC branch. The 2.5-day estimate stands, and no re-estimate is needed (RISK-03's fallback does not fire).

## 3. Light-Theme Token Set

The light page background is `bg-slate-100` (`#f1f5f9`). Cards are white. Contrast was measured with the WCAG 2.1 relative-luminance formula. The dark values are the existing ones, unchanged.

| Role | Light | Dark | Light contrast (on white / on slate-100) |
|------|-------|------|------------------------------------------|
| Card surface | `bg-white border-slate-200` | `bg-slate-800/50 border-slate-700/50` | — |
| Nested row surface | `bg-slate-50` | `bg-slate-800/40` | — |
| Primary text (headings, figures) | `text-slate-900` | `text-white` | 17.85 / 16.30 |
| Strong body text | `text-slate-800` | `text-slate-200` | 14.63 / 13.35 |
| Secondary / label text (existing) | `text-slate-600` | `text-slate-400` | 7.58 / 6.92 |
| Positive P&L | `text-emerald-700` | `text-emerald-400` | 5.48 / 5.01 |
| Negative P&L | `text-rose-700` | `text-rose-400` | 6.29 / 5.74 |
| Warning / information text | `text-amber-700` | `text-amber-400` | 5.02 / 4.58 |
| Accent: active tab, link | `text-cyan-700` | `text-cyan-400` | 5.36 / 4.89 |

**Rules:**
1. Every themed surface uses the pair as `light dark:dark`, for example `text-emerald-700 dark:text-emerald-400`. A bare dark value is a defect.
2. The 700-shade colour tokens (emerald, amber, cyan) pass only on white, `slate-50` and `slate-100`. On `slate-200`, they measure 4.07–4.45:1 and fail. Any other light surface must be measured before use.
3. `text-amber-600` fails on white (3.19:1). The Reports restated marker's `text-amber-600 dark:text-amber-400` moves to `text-amber-700 dark:text-amber-400`.
4. Filled badges with white text keep their fixed, theme-independent background, for example `bg-amber-700` (5.02:1).

## 4. §13 Compliance

Visual only. No AI.

## 5. Frontend Spec Impact

- `reports.md` v0.22 → v0.23: new §Light Theme, and the restated marker token.
- `notifications.md` v0.10 → v0.11: new §Light Theme.
- `design_system.md` (Class 1) is outside this gate's write scope (`docs/specs/frontend/pages/` only). ST-23's AC 1 adds §3's table to it in-story.

## 6. Obligations for Sprint Execution

- Add §3's token table to `docs/specs/frontend/design_system.md` §Theme & Colors, and correct `docs/frontend/design_system.md` §6 to point to it (AC 1).
- Apply the tokens to Reports (Monthly, including the expanded restated row, and Tax Year) and to Notification Preferences and History.
- Remove the `color-contrast` entries for `ReportsMonthly:light`, `ReportsTaxYear:light`, `NotificationPreferences:light` and `NotificationsHistory:light` from `KNOWN_VIOLATIONS` in `tests/e2e/accessibility-axe-scan.spec.js`, in the same commit.
- Replay's light-theme baseline belongs to its own backlog item and is not in ST-23's scope.

## 7. Testability (CLAUDE.md §2)

The light-theme axe scans of the four pages pass with no `color-contrast` baseline entry (AC 1). The dark-theme scans still pass.

## 8. Approval

Head of UX & Design: confirmed, 2026-10-12. Decision: light mode supported.
Product Owner: confirmed, 2026-10-12.
