**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-07-24
**Cycle:** 2026-07-24__release-v7.8
**Backlog source:** BLG-FEAT-82
**Maps to:** EPIC-06, ST-06

---

# UX Spec — AI Spend Trend Chart (Claude API Usage & Costs)

## 1. Problem

`settings.md` §6 Claude API Usage & Costs (v7.6) shows only the current calendar month's spend as a single bold figure — no history, no trend visibility across releases. AC requires a trend chart showing at least the last 6 release cycles' spend.

**Naming note:** the story title says "Gemini/Claude" per its original backlog phrasing, but per `settings.md` §6's v1.5 reframing (`ESC-EXEC-20260720-01`), this codebase integrates only the Claude API — there is no separate Gemini cost stream. This chart shows Claude API spend only, consistent with the existing single-total section it extends. No naming/scope disagreement to escalate — the section is already correctly titled "Claude API Usage & Costs."

## 2. Placement

Added directly below the existing §6 read-only card (`settings.md` §6, current-month figure), inside the same `SectionCard` — not a new top-level Settings section. It is presented as an extension of the existing monitoring card, not a separate feature.

## 3. Chart Type & Data Mapping

Bar chart, following the same pattern as `analytics.md` §12 Win Rate by Month (bar chart, fixed-axis, no zoom/pan — this is a simple trend glance, not an interactive analysis tool like the Analytics page's equity curve).

- **X-axis:** release cycle labels (e.g. "v7.3", "v7.4" … "v7.8"), most recent 6 cycles, oldest to newest left to right
- **Y-axis:** spend in USD, auto-scaled to the max value in the displayed range (no fixed ceiling — unlike Win Rate's fixed 0–100%, spend has no natural upper bound)
- **Bar value:** total Claude API spend for that release cycle's date window
- **Bar colour:** single accent colour (`text-blue-500`/`bg-blue-500` dark, `bg-blue-600` light — reuses the existing informational/monitoring accent already used for read-only figures elsewhere in Settings, not the emerald/rose profit-loss convention which doesn't apply to a cost-only metric)
- **Tooltip (on hover/focus per bar):** cycle label + exact spend (`$X.XX`) — same hover-tooltip interaction convention as other bar charts in the app (`analytics.md` §12, §16)

No reference line (unlike Win Rate's 50% break-even line — spend has no natural target/threshold to mark).

## 4. Data Source & Backend Dependency

**AC states:** "sourced from existing `gemini_audit_log` / Claude cost tracking — no new data collection required." This is correct for the underlying data (spend events are already logged per-call in `claude_audit_log`, per `settings.md` §6's v1.5 note). However, **no existing endpoint aggregates spend by release-cycle window** — `GET /ai/monthly-cost` only returns the current calendar month. A new read endpoint (or query-param extension) is required to bucket `claude_audit_log.cost_usd` by release cycle date range, sourced from `claude/cycles/*/state.json` publish/close timestamps or an equivalent cycle-boundary source. This is an implementation detail for sprint execution — no new data *collection*, but a new aggregation *endpoint* — API contract entry required in `docs/specs/api_contracts/` in the same commit per `CLAUDE.md` §2.

## 5. States

| State | Rendering |
|-------|-----------|
| Loading | Inline skeleton within the chart area only (matches the existing card's §6 loading pattern — does not block the rest of Settings) |
| Error | "AI spend trend unavailable" text in place of the chart; the current-month figure above is unaffected and renders independently (each has its own query) |
| Fewer than 6 cycles of data available | Renders whatever cycles exist (no padding with zero/empty bars) — AC says "at least the last 6," not exactly 6; a newly-onboarded metric may have less history initially |
| Ready | Bar chart per §3 |

## 6. Compliance Check

No conflict with `strategy_rules.md §13` — a cost-monitoring display, not a trading-parameter or automated-decision surface. Not a canonical trading metric, so no canonical-metric-definition alignment required (AI spend is an operational/ops cost figure, not a strategy performance metric).

## 7. Sign-off

- **Head of UX & Design:** Approved — 2026-07-24 (naming resolved per §1, chart pattern reused per §3)
- **Product Owner:** Approved — 2026-07-24
