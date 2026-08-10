Owner: Head of UX & Design
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-10
Cycle: 2026-08-08__release-v8.5
Story: ST-14 (BLG-FE-133, EPIC-04)

# ST-14 — Ad Hoc Component Inventory: Candidates for Shared Design-System Extraction

## 1. Purpose

Inventory of ad hoc/duplicated component patterns across the app, ranked by duplication count, per this story's AC. Audit-only deliverable (RISK-02) — no code changed by this story; extraction decisions and any resulting implementation work are follow-up items pending the sign-off this document requires.

## 2. Method

`grep`-based scan of `src/**/*.js` for repeated inline `className` strings and repeated structural patterns (label+value+subtitle stacks, status-to-colour config-object maps), cross-referenced against existing shared components in `src/components/ui/` to measure adoption rate — a pattern with an existing shared component and low adoption is a stronger, more actionable finding than a pattern with no shared component at all (the former needs migration; the latter needs extraction first).

## 3. Findings, ranked by duplication count

**Correction (post agent-mediated Head of UX & Design review, 2026-08-10):** the first draft of this document claimed no shared `Card` component existed. This was wrong — `src/components/ui/card.js` exists (a full `Card`/`CardHeader`/`CardTitle`/`CardDescription`/`CardContent`/`CardFooter` set) with **zero** importers anywhere in `src/`. Caught before sign-off; corrected below. This is actually the *most severe* adoption gap of the four findings (0/23, worse than badge's 9/33 or stat-tile's 2/9), not a "no component exists" case — the ranking and recommended actions are updated accordingly.

### 3a. Card wrapper — `rounded-2xl bg-slate-800/50 border border-slate-700/50` (23 files ad hoc; existing `Card` component has 0 adopters)

The single most duplicated pattern found, and the worst adoption gap: 23 files repeat this exact class string (or a near-identical variant) as an ad hoc card container. A shared `Card`/`CardHeader`/`CardTitle`/`CardDescription`/`CardContent`/`CardFooter` set already exists at `src/components/ui/card.js` — but is imported by **zero** files. Every one of the 23 ad hoc sites is independently maintained — a future visual change to the card treatment requires editing all 23 call sites individually, when a fully-built component to prevent exactly that already sits unused.

**Candidate action:** reconcile the 23 ad hoc sites onto the existing `Card` component (or, if its API doesn't fit this app's actual card usage patterns, formally document why and either adapt it or deprecate it — leaving a fully-built, zero-adoption component in the tree is itself a maintenance liability).

### 3b. Badge / status-pill — inline `rounded-full ... text-xs font-semibold` styling (~31-33 files ad hoc; 9 use an existing shared component)

Files rendering badge-like pills (rounded-full background + small bold text) via inline `className`, cross-referenced against the two existing shared components — `src/components/ui/badge.js` (4 importers: `SignalCard.js`, `SystemStatus.js`, `TagPerformance.js`, `RMultipleAnalysis.js`) and `StatusBadge.js` (5 importers: `TradePlan.js`, `TradePlans.js`, `MonitorModal.js`, `Research.js`, `CustomPriceAlertsSection.js`) — 9 unique files combined. The ad hoc-vs-adopted ratio (~9 of ~31-33) is the second-worst adoption gap, behind 3a.

### 3c. Metric/stat tile — label + large value + subtitle stack (9 files; 2 use the existing `StatsCard`)

9 files render a repeated three-line stack (uppercase `text-xs` label, large bold value, small subtitle) for dashboard/summary metrics, but a shared `StatsCard` component already exists (`src/components/ui/StatsCard.js`) and is used by only 2 of those 9. Same shape as 3b — existing component, low adoption.

### 3d. Status-to-colour config map — `{ label, bg, text }`-shaped objects (7 files; pattern-level duplication, not content duplication)

7 files (`WatchlistBadges.js`, `PlanVsReality.js`, `RedFlagJournal.js`, `Positions.js`, `TradePlans.js`, `StrategyCompliancePanel.js`, `StandingAlert.js`) each define their own `{status: {label, bg, text}}`-shaped lookup map for badge colouring. Checked and confirmed: each map's *content* is legitimately domain-specific (trade status, watchlist status, compliance status, alert status are genuinely different enums) — this is not literal duplication of the same data. The *shape* of the pattern repeats, though, which is a weaker case for extraction (a generic "config-map-driven badge" helper could reduce boilerplate per file, but wouldn't eliminate the need for each domain to define its own map).

## 4. Ranking summary

| Rank | Pattern | Files using ad hoc form | Files using shared component | Extraction need |
|------|---------|--------------------------|-------------------------------|------------------|
| 1 | Card wrapper | 23 | 0 (`Card` exists, unused) | Reconcile onto existing `Card`, or justify/deprecate it |
| 2 | Badge / status-pill | ~31-33 | 9 (`badge.js` + `StatusBadge.js`) | Migrate to existing `Badge`/`StatusBadge` |
| 3 | Metric/stat tile | 9 | 2 (`StatsCard`) | Migrate to existing `StatsCard` |
| 4 | Status-colour config map | 7 | N/A (pattern-level only) | Lower priority — genuinely domain-specific content |

## 5. Disposition

This inventory is submitted for Head of UX & Design sign-off per this story's AC. No extraction or migration work is performed in this story — ranking and prioritisation of any follow-up work is the sign-off authority's call.

**Reproducibility note:** counts in §3a and §3d were confirmed via exact-string `grep` and independently reproduced during agent-mediated review. §3b's ad hoc-instance count (~31-33) is an approximate range from a broader structural-pattern match (`rounded-full` + `text-xs` + `font-semibold` co-occurring) rather than one exact string, since badge markup varies more across call sites than the card wrapper's near-verbatim repetition — the adopted-component count (9) is exact.

## 6. Sign-Off

**Agent-mediated Head of UX & Design review (§5.3, independent subagent, 2 passes):**
- First pass: **BLOCKED** — §3a's central claim was factually wrong (asserted no `Card` component existed; `src/components/ui/card.js` actually exists with 0 importers, making it the *worst* adoption gap of the four findings, not a no-component case). Also flagged non-blocking variance in §3b's raw counts.
- Corrected in-session: §3a reclassified (0/23 adoption gap on an existing-but-unused component), §3b's combined-adopter count corrected to an exact, independently-reproducible 9 files, ranking table and reproducibility note updated.
- Second pass: **APPROVED** — all corrected claims independently verified against the codebase, no remaining discrepancies.

- Signed off by: Sprint Execution Engine (agent-mediated, Head of UX & Design role — §5.3)
- Date: 2026-08-10
- Comments: Inventory is submitted as a design-system audit deliverable per this story's AC. Ranking and prioritisation of any follow-up extraction/migration work remains the sign-off authority's call — this document does not itself authorise or schedule implementation.
