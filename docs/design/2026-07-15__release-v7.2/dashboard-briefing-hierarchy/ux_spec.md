**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-15
**Approved by:** Product Owner — 2026-07-15
**Story:** ST-06 — Dashboard briefing visual hierarchy (BLG-FE-111)
**Depends on:** ST-04 spec & instrumentation pass (BLG-SPEC-90) — primary vs secondary dashboard card treatment definition
**Cycle:** 2026-07-15__release-v7.2

---

# UX Specification — Dashboard Briefing Visual Hierarchy

## 1. Context

`MorningBriefing`'s five sub-cards (`ScreenerHitsCard`, `ExitZoneCard`, `RedFlagsCard`, `EarningsAlertCard`, `ComplianceCard`) each reuse the plain `DashboardCard` shell (`bg-slate-800/50 border border-slate-700/50`) — the identical container used by the five session-summary status cards below them. The only differentiator today is a small muted uppercase label above the row ("Trader's Morning Briefing"), easy to miss. On page load a user sees ten visually-identical bordered cards in a row with no cue that the first five are start-of-day intelligence and the next five are live position/portfolio status — two different kinds of information presented as one undifferentiated block.

`AiDailyBriefing` already has more inherent distinction (`bg-slate-900` vs the grid's `bg-slate-800/50`, an explicit "Today's Briefing" header, and the amber "AI Advisory" badge), but shares no common visual language with `MorningBriefing` that would let a user recognise both as the same category of content ("intelligence/briefing sections," as opposed to "status cards").

**Interpretation of AC-01 ("without scrolling past other cards first"):** this is read as a self-evidence requirement — the distinction must be apparent at the point the user reaches each section, not dependent on scrolling back to compare against the status grid — rather than an above-the-fold/reordering requirement. Document order is unchanged (`MorningBriefing` stays first, `AiDailyBriefing` stays directly after the status grid, before `GateProgressStrip`); reordering was considered and rejected as unnecessary structural risk for a purely visual-hierarchy story.

## 2. Decision

### 2.1 Morning Briefing — enclosing panel + upgraded label

Wrap the existing `<section>` (label + 5-card grid) in a distinctly-toned panel so the row reads as one grouped "shelf," visually separate from the plain grid below:

```
<section className="rounded-2xl border border-slate-300/60 dark:border-slate-800 bg-slate-100/60 dark:bg-slate-900/40 p-4">
```

Both light and dark values are explicit pairs (not a bare dark-only token) — this project has twice shipped a dark-only-token-on-light-theme contrast defect (`BLG-FE-87/88`, `BLG-FE-95`), so any new background/border token introduced here must ship with both halves from the start.

Section label upgraded from a plain caption to a section-heading weight, with a leading icon to establish the shared "intelligence section" visual language (§2.2):

```
<Sunrise className="w-4 h-4 text-amber-500 dark:text-amber-400" />
<span className="text-sm font-semibold text-slate-700 dark:text-slate-300">Trader's Morning Briefing</span>
```

The child cards themselves (`ScreenerHitsCard` etc.) are unchanged — same `DashboardCard` shell, same queries, same click targets. The differentiation is carried entirely by the new enclosing panel and label, not by altering the cards.

### 2.2 AI Daily Briefing — shared icon language

No structural or container change (its `bg-slate-900`/badge/header treatment already provides sufficient distinction from the grid). Add a matching leading icon to the "Today's Briefing" header, reusing `Sparkles` — the same icon already used for the "AI draft" badge convention elsewhere in the app (`trade_plan.md` §5b) — so the two briefing sections read as one family at a glance:

```
<Sparkles className="w-4 h-4 text-violet-500 dark:text-violet-400" />
<span className="text-sm font-semibold text-white">Today's Briefing</span>
```

### 2.3 Explicitly out of scope

`AiDailyBriefing`'s existing `bg-slate-900 border-slate-700` container and its nested `Section` component's `border-slate-700` (both bare, no `dark:` pair) were reviewed for the same class of light-theme defect noted in §2.1. Whether this is a live bug or an intentional theme-independent surface could not be confirmed without a staging check, and fixing it is a larger scope than "add an icon" — **not actioned in this story**. Flagged for Head of Specs Team to confirm at execution time; file as a follow-up backlog item (spec-debt class) if a staging check confirms it renders incorrectly in light theme, rather than folding an unrelated fix into ST-06.

## 3. §13 Compliance

Purely presentational (panel background, label weight, icon). No change to `AiDailyBriefing`'s advisory content, disclaimer, or §13-required non-dismissible label. No change to any query, data source, or the `dashboard-retry-root` retry behaviour (AC-02).

## 4. States

| State | Behaviour |
|-------|-----------|
| Page load, any theme | Morning Briefing panel and AI Daily Briefing header both carry the new icon+label treatment immediately — no interaction required |
| Morning Briefing card loading/error/empty | Unchanged (per `dashboard-empty-states/ux_spec.md`, ST-05) — panel wrapper is a static container, does not participate in any card's data state |
| AI Daily Briefing states (no briefing / loading / normal / empty actions / error) | Unchanged — `dashboard.md` §5 States table applies as-is; only the header icon is new |
| Light theme | New panel/border/label tokens render with the light-mode half of each pair; no bare dark-only class introduced |
| Dark theme | Unchanged visual weight from before, plus the new panel tint and icons |

## 5. Playwright / Dual-Theme Note

Per ST-04 AC-04, this story requires explicit dual-theme (light/dark) verification of: the Morning Briefing panel background/border pair, the upgraded label text colour pair, and both new icons' colour pairs. Shared spec file named per ST-08 (EPIC-05 combined Playwright suite plan).

## 6. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-15
- **Product Owner:** Approved — 2026-07-15
