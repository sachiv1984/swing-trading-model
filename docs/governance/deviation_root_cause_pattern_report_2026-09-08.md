**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Report Date:** 2026-09-08
**Filed:** 2026-09-08
**Cycle:** 2026-09-07__release-v9.2 (ST-13, EPIC-03, BLG-QA-141)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# DEV-* Deviation Root-Cause Recurrence Pattern Report

## Objective

`BLG-QA-141`: the existing cross-cycle deviation consolidation review (`BLG-QA-129`, `docs/governance/deviation_consolidation_review_*.md`, 4 runs so far) groups `DEV-*` records by **spec file** — it can tell you `reports.md` carries 2 records, `trade_plan.md` carries 3, and so on. It does not tell you whether the *same underlying defect class* recurs across different stories and different spec files. This report adds that second lens over the same register.

## Method

Source register: `docs/governance/deviation_consolidation_review_2026-09-03.md` (16 records, the most current consolidated register at time of writing). For each of the 16 records, read its own canonical-spec `### DEV-*` "Known Deviations" entry (not just the consolidated register's spec-file/priority/status columns) to characterise the actual engineering root cause, then grouped the 16 into root-cause classes. A class of 1 is reported as a singleton, not omitted — the point of this pass is to make recurrence (or its absence) visible, and a report that only showed the clusters would silently imply every excluded record was itself part of some cluster.

## Root-Cause Classes

### Class A — Currency/FX-conversion basis errors (2 records — self-confirmed recurrence within one cycle)

| DEV ID | Spec | What went wrong |
|--------|------|------------------|
| `DEV-EPIC01-ST02-01` | `positions.md` | Trail Stop tile rendered a GBP-converted value but labelled it with the *native* currency symbol for US-market positions (P0, `BLG-BE-103`). |
| `DEV-v8.9-ST05-02` | `trade_plan.md` | "R at Risk" implemented as a raw `(entry − stop) × shares` with **no** FX conversion applied for any market, despite the spec explicitly calling for FX conversion on US-market plans (P2, `BLG-FEAT-91`). |

**This is the strongest recurrence in the register, and it is self-confirmed in the source text, not an inference of this report:** `trade_plan.md`'s own `DEV-v8.9-ST05-02` entry states the fix was caught because it was "the same class of currency-basis bug already fixed once this cycle (ST-02, `BLG-BE-103`)" — both instances landed in the *same* release (`v8.9`), one in EPIC-01 (filed 2026-08-17), the other in EPIC-02 (caught 2026-08-18) — one day apart. The second instance's fix explicitly copied the first instance's now-established pattern (`fx_rate_used` from `POST /portfolio/size`, divided into the raw figure for US-market plans, matching `TradeEntry.js`'s `costs.totalRisk` convention).

**Finding A1:** the pattern that closed the recurrence (read `fx_rate_used` off the sizing/portfolio response, apply for US-market only) is now correctly implemented in the 2 known instances (`positions.md`'s Trail Stop tile, `trade_plan.md`'s R at Risk / `WhatIfSizingPreview.js`) and documented inline at each site, but there is no single named convention a *future* story author would find without already knowing to search for `fx_rate_used`. See Recommendation 1.

### Class B — Visual/theming token compliance drift (4 records — largest class by count)

| DEV ID | Spec | What went wrong |
|--------|------|------------------|
| `DEV-EPIC01-ST05-01` | `positions.md` | Table View's RISK OFF badge colour/label diverged from spec (v2.4). |
| `DEV-ST14-01` | `trade_history.md` | Avg Slippage StatsCard rendered without its spec'd gradient; needed two separate fix passes to land correctly across all data states (v2.5). |
| `DEV-REPORTS-ST01-02` | `reports.md` | Monthly Financial Table's zero-P&L colour rule diverged from the Tax Year Trades Table's (v8.5). |
| `DEV-NAV-ST06-01` | `navigation.md` | Dark theme not applying inside Radix-portaled dialogs, app-wide (v8.5, retroactively filed v8.6). |

**Finding B1 — recurring but declining, not accelerating:** all 4 instances predate `2026-08-12__release-v8.7`; zero new Class B records have been filed across the 4 most recent releases carrying new deviations (`v8.9`, `v9.0`, and this register's own 4th-run window). This lines up with `design_system.md`'s own growth over the same period — it picked up the Modal/Dialog Theming subsection (v1.9, `BLG-FE-150`, v8.6), the Focus Indicator contrast standard (v1.4, v7.8), and most recently the motion-vs-contrast guideline (v1.12, v9.2 ST-05, this cycle) — each closing off one more category of token drift before it could recur a second time. Read as a positive trend rather than a live concern: the mechanism that produced Class B (missing or ambiguous design-system coverage for a given visual property) has been getting closed off category-by-category, and the record volume reflects that.

### Class C — Computation-method ambiguity between spec and implementation (3 records)

| DEV ID | Spec | What went wrong |
|--------|------|------------------|
| `DEV-v51-EPIC01-01` | `si05-telegram-message-format-spec.md` | `pass_rate` computation method was ambiguous against `BLG-GOV-86` §5.2; resolved by explicitly adopting Option (a), volume-weighted ratio. |
| `DEV-EPIC02-ST03-01` | `analytics.md` | `CohortAnalysis.js` used client-side computation instead of the dedicated `GET /analytics/cohort` endpoint (later found to already be migrated — a tracking-only correction, not a live defect by the time it was reviewed). |
| `DEV-REPORTS-ST06-01` | `reports.md` | Unrealised P&L legitimately differs between the Reports page (nightly-batch-written `positions.pnl`) and the Positions page (computed fresh on every request) — an acknowledged data-path divergence, still **Open**, `BLG-SPEC-87`. |

**Finding C1:** this class is looser than A or B — each instance is a genuine spec/implementation gap, but the underlying mechanism differs per record (a metrics-definition choice, a stale-vs-current implementation-status question, and a still-open architectural data-freshness question). Grouped together because all three share the same *shape* (spec didn't pin down which of two legitimate computation paths is canonical, and the gap surfaced only once two paths were built), not because they share one fixable root cause. `DEV-REPORTS-ST06-01` remains the one open, unresolved record in this class — see Recommendation 2.

### Class D — Spec'd element missing from what actually shipped (3 records)

| DEV ID | Spec | What went wrong |
|--------|------|------------------|
| `DEV-EPIC02-ST04-01` | `notifications.md` | Alert Thresholds empty state shipped without the spec'd "Add alert rule" CTA button (v2.3). |
| `DEV-EPIC02-ST05-03` | `positions.md` | Table View's P&L (GBP) column was absent entirely — page showed % uplift only (v2.4). |
| `DEV-EPIC04-ST09-01` | `ticker_universe_api_contract.md` | `createPageUrl` routing map was missing the TickerUniverse entry specifically *at merge time* — a working feature dropped by a merge, not missing from the original implementation (v3.8). |

**Finding D1:** the first two (both from the same early `v2.x` window) are "built without one spec'd element," a build-completeness gap; the third is a distinct mechanism — a *regression introduced by merging two branches*, not an initial-build gap. Kept in one table for the shared surface symptom ("thing that should be there, isn't") but the fix classes differ: the first two need closer AC-vs-shipped review before a story is marked done; the third needs cross-EPIC merge review to catch a routing/registration entry silently dropped by a conflict resolution (`CLAUDE.md` §8 already covers the general merge-conflict-resolution procedure — no new mechanism recommended here since this is a single historical instance, not a recurring merge-time pattern).

### Class E — Self-contradictory literal spec wording caught at implementation (1 record, singleton)

`DEV-v8.9-ST05-01` (`trade_plan.md`): the design gate's literal wording ("hidden until both Planned Entry Price and Stop Level have valid positive values") was unsatisfiable as written, since Planned Entry Price is itself a field *inside* the panel it was supposedly gating. Caught and corrected same-story.

### Class F — Persisted-field gap for a spec'd UI cue (1 record, singleton)

`DEV-v8.6-ST02-01` (`trade_plan.md`): the AI-draft badge couldn't render because the underlying `isAiDraft` flag was ephemeral client-only state, never persisted server-side. Resolved a release later (`v8.7`, `BLG-BE-95`) once the persisted field was added.

### Class G — Spec claim ahead of live verification (1 record, singleton)

`DEV-EPIC03-ST09-01` (`api_performance_baseline.md`): a documented Render-log timing line wasn't actually present in a real invocation at time of filing. Resolved once a real invocation confirmed the line present with a real elapsed-time value.

### Not a defect — excluded from recurrence framing

`DEV-ST04-01` (`alerts_endpoints.md`): Telegram delivered in place of email, an explicit **Accepted** infrastructure-gated scope substitution, not an implementation defect. Retained in the consolidated register (per its own scope) but excluded here since "recurrence of a defect class" doesn't apply to a deliberate, signed-off substitution.

## Summary Table

| Class | Records | Status |
|-------|---------|--------|
| A — Currency/FX-conversion basis errors | 2 | Both Resolved; self-confirmed same-cycle recurrence, now closed with a repeatable pattern (see Recommendation 1) |
| B — Visual/theming token drift | 4 | All Resolved; zero new instances since v8.7 — declining trend |
| C — Computation-method ambiguity | 3 | 2 Resolved, 1 Open (`DEV-REPORTS-ST06-01`) |
| D — Spec'd element missing from shipped state | 3 | All Resolved |
| E — Self-contradictory spec wording | 1 | Resolved (singleton) |
| F — Persisted-field gap for a UI cue | 1 | Resolved (singleton) |
| G — Spec claim ahead of live verification | 1 | Resolved (singleton) |
| (excluded) Accepted scope substitution | 1 | Accepted, not a defect |
| **Total** | **16** | Matches the 4th-run consolidated register exactly |

## Recommendations

1. **Class A (currency/FX-conversion):** name the now-twice-independently-arrived-at pattern explicitly in `design_system.md` or a shared frontend-patterns note — "any GBP-basis financial figure computed from a form that can represent a US-market position must read `fx_rate_used` off the relevant sizing/portfolio response and divide by it before display; do not assume a figure is already GBP-basis just because its label says so." Both existing fixes already do this; the gap is discoverability for a *future* story that introduces a third such figure without knowing to search for the first two. Filed as `BLG-SPEC-137` (see backlog) rather than authored directly in this report — adding new content to `design_system.md` is outside this story's own scope (a root-cause *report*, not a spec change) and the design-system update in this cycle already went through its own dedicated story (ST-05).
2. **Class C:** `DEV-REPORTS-ST06-01` is the one still-open record in any class. No action recommended beyond what `metrics_definitions.md` already states (an acknowledged, intentional data-path difference) — flagged here only so a future Director of Quality reviewing this report doesn't have to re-derive that it's the sole open item across all 16 records.
3. **No structural fix recommended for Classes D/E/F/G** — each is either a singleton or (Class D) a low-volume class whose two sub-mechanisms already have adequate existing coverage (AC-vs-shipped review; `CLAUDE.md` §8 merge procedure) without a new backlog item being warranted on a 1-instance basis.
4. **Recurring-cadence note:** align this report's re-run cadence with the existing `deviation_consolidation_review_*.md` cadence (every 3rd Post-Ship Closure invocation) rather than establishing a separate schedule — the two are companion lenses over the same underlying register and should stay in sync so a reader always has both views current together.

## Sign-off

```
Director of Quality

Root-cause grouping pass complete over the current 16-record register (matching
docs/governance/deviation_consolidation_review_2026-09-03.md exactly). One
self-confirmed same-cycle recurrence found (Class A, currency/FX-conversion basis
errors, 2 instances, v8.9) — both resolved, pattern now named and referenced in a
filed backlog item (BLG-SPEC-137) for future discoverability. One declining class
(Class B, visual/theming drift, 4 instances, all pre-v8.7, zero since) — read as a
positive trend, design_system.md coverage closing the gap category by category. One
open record overall (DEV-REPORTS-ST06-01, Class C) — already acknowledged and
intentional per metrics_definitions.md, no new action. No structural fix warranted
for any class beyond Recommendation 1.

Signed: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3) — 2026-09-08
```
