**Owner:** Frontend Specs & UX Documentation Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.4 (EPIC-03, ST-10, BLG-FE-52)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# SI-02 Drift Detection Result Component Pre-Design

> **Note:** This document is explicitly labelled as input to ST-11 (BLG-FE-53 — SI-02 interaction spec). The interaction spec must reference the component interface and data contract defined here.

---

## 1. Purpose

This document defines the frontend component design for the SI-02 Behavioural Drift Detection display. It covers three candidate interface options, the rationale for the selected option, the component data contract (input shape, states), and the constraints imposed by the §13 advisory-only requirement.

This is a pre-planning artefact for the v4.4 sprint. No React implementation is produced here. The output feeds directly into the interaction spec (ST-11) and the backend API contract work that will seal at SI-02 sprint planning.

---

## 2. §13 Advisory Constraint

Per `docs/specs/si02/section13_criteria.md §3.2`, the drift display must:

- Be labelled "Advisory" or equivalent — the label must be visible without hover or expansion
- Not gate, block, or modify any trade plan, position entry, or exit workflow
- Not present any UI affordance (button, link, or action prompt) that implies automated remediation

These constraints apply to all three candidate options evaluated below and must be carried forward verbatim into the interaction spec (ST-11) and the implementation story.

---

## 3. Drift Metrics in Scope

The following four drift metrics are in scope for the initial SI-02 display, drawn from `docs/specs/si02/query_performance_assessment.md` and `docs/specs/si02/data_prerequisite_audit.md`:

| Metric | What It Measures | Data Source |
|--------|-----------------|-------------|
| Entry timing drift | Days from signal date to actual entry date — are entries lagging signals? | `trade_history.entry_date` − `signals.signal_date` (requires DS-07 migration) |
| Sizing adherence | Is `risk_percent_used` staying within stated plan limits per trade? | `trade_plans.risk_percent_used` vs. strategy max |
| Consecutive loss context | Is position sizing adjusted appropriately after a run of losses? | Rolling loss window self-join on `trade_history` |
| Regime context | Are trades being entered in the correct declared market regime? | `trade_plans.regime_context_at_entry` |

---

## 4. Component Interface Options

### Option A — Score Badge

**Description:** A single composite score (e.g. "Drift Score: 72/100") displayed as a badge or pill. Each sub-metric contributes a weighted component to the score. The badge changes colour (green / amber / red) based on threshold bands.

**Pros:**
- Extremely compact — can sit inline as a page header indicator or alongside an existing summary card
- Easy to scan at a glance; one number signals overall state

**Cons:**
- The composite formula must be documented and deterministic (per §13 criterion 3.1) — adds spec burden
- Hides which specific metric is drifting; the user must expand or navigate elsewhere to understand the cause
- Weighting decisions are opaque unless a tooltip or modal explains them
- Risk of misreading: a score of "72" conveys false precision about a nuanced multi-metric state
- For a single-user trading assistant the number alone does not tell the user what to review

### Option B — Percentage Deviation Display

**Description:** One card per drift metric showing the measured value, the expected threshold, and the deviation as a percentage. Example: "Avg entry lag: 2.4 days (threshold: ≤1 day) — +140% above threshold."

**Pros:**
- Directly legible: the user sees the specific metric and the magnitude of drift without needing to interpret a composite
- Percentage deviation is deterministic and formula-simple — no weighting decisions required
- Status at a glance per metric (colour-coded card border: green = within threshold, amber = approaching, red = breached)
- Naturally handles "no drift detected" (all rows green) without a separate view mode

**Cons:**
- Four cards take more vertical space than a badge
- Requires the user to mentally synthesise across metrics; no single overall summary

### Option C — Rule List Format

**Description:** A checklist-style list where each drift rule is shown as a pass/fail line item. Example: "✓ Entry timing — within threshold" / "✗ Sizing adherence — breached (avg 2.1%, limit 1.5%)."

**Pros:**
- Maximum transparency: each rule is explicit, binary, and readable
- Familiar pattern for compliance/checklist contexts (consistent with the trade plan checklist UX)

**Cons:**
- Most verbose; four rules displayed as a list is not meaningfully more compact than Option B cards but provides less quantitative detail
- Pass/fail binary loses the degree of drift (how far over threshold?) — the user cannot gauge urgency without an additional value column
- Adding a value column to each rule line item reproduces most of Option B's structure with less visual clarity

---

## 5. Selected Option and Rationale

**Selected: Option B — Percentage Deviation Display**

**Rationale:**

The primary goal of SI-02 in a single-user trading assistant context is actionable insight: the user needs to know *which* behaviour is drifting and *by how much* in order to self-correct. A score badge (Option A) compresses this into a single opaque number, requiring additional interaction to understand the cause. A rule list (Option C) achieves transparency but sacrifices the quantitative magnitude that tells the user how urgently a metric needs attention.

Option B — one card per drift metric with value, threshold, and percentage deviation — provides the right balance:

- It is immediately legible for a single-user context where screen real estate is not the primary constraint
- The percentage deviation figure is deterministic and requires no weighting formula, directly satisfying §13 criterion 3.1 (determinism)
- The per-metric card structure matches the established pattern in `DisciplineComplianceSection.js` and `Arc5ComplianceSection.js`, which use a 3–4 card grid with colour-coded gradient borders — no new UI pattern is introduced
- Colour-coded card borders (green / amber / red) make the overall state scannable at a glance while preserving the per-metric detail
- The "Advisory" label is naturally placed as a section heading badge without cluttering the individual metric cards

A summary badge variant of Option A can be composed on top of Option B in a future story if a header-level indicator is needed — the underlying data contract supports this without rework.

---

## 6. Component Data Contract

### 6.1 API Response Shape

The component expects the response from `GET /analytics/behavioural-drift` (endpoint to be formally specified in the SI-02 API contract). The canonical shape is:

```json
{
  "status": "ok | insufficient_data | no_drift | drift_detected",
  "trade_count": 24,
  "analysis_window_days": 90,
  "generated_at": "2026-05-29T10:00:00Z",
  "metrics": [
    {
      "metric_id": "entry_timing_drift",
      "label": "Entry Timing",
      "description": "Average days from signal date to trade entry",
      "measured_value": 2.4,
      "measured_unit": "days",
      "threshold_value": 1.0,
      "threshold_direction": "lte",
      "deviation_pct": 140.0,
      "status": "breached",
      "advisory_note": "Entries are averaging 2.4 days after signal — review entry execution timing."
    },
    {
      "metric_id": "sizing_adherence",
      "label": "Sizing Adherence",
      "description": "Average risk % used vs. plan maximum",
      "measured_value": 2.1,
      "measured_unit": "pct_of_portfolio",
      "threshold_value": 1.5,
      "threshold_direction": "lte",
      "deviation_pct": 40.0,
      "status": "breached",
      "advisory_note": "Average position size exceeds plan maximum. Review recent entries."
    },
    {
      "metric_id": "consecutive_loss_sizing",
      "label": "Post-Loss Sizing",
      "description": "Risk % used in trades following 2+ consecutive losses",
      "measured_value": 1.8,
      "measured_unit": "pct_of_portfolio",
      "threshold_value": 1.0,
      "threshold_direction": "lte",
      "deviation_pct": 80.0,
      "status": "breached",
      "advisory_note": "Sizing after consecutive losses is above reduced-risk threshold."
    },
    {
      "metric_id": "regime_context",
      "label": "Regime Adherence",
      "description": "% of trades entered in declared valid regime",
      "measured_value": 92.0,
      "measured_unit": "pct",
      "threshold_value": 90.0,
      "threshold_direction": "gte",
      "deviation_pct": -2.2,
      "status": "ok",
      "advisory_note": null
    }
  ]
}
```

**Field definitions:**

| Field | Type | Description |
|-------|------|-------------|
| `status` | string enum | Top-level component render mode (see §6.2) |
| `trade_count` | integer | Number of closed trades in the analysis window |
| `analysis_window_days` | integer | Rolling window used for drift calculations |
| `generated_at` | ISO 8601 string | Timestamp of analysis computation |
| `metrics` | array | One object per drift metric; always present when status is `ok`, `no_drift`, or `drift_detected` |
| `metrics[].metric_id` | string | Stable snake_case identifier — used as React key |
| `metrics[].label` | string | Human-readable metric name for display |
| `metrics[].description` | string | Tooltip / subtitle text |
| `metrics[].measured_value` | float | Computed value for this metric |
| `metrics[].measured_unit` | string | Unit label for display (days, pct_of_portfolio, pct) |
| `metrics[].threshold_value` | float | Threshold the measured value is compared against |
| `metrics[].threshold_direction` | string (lte or gte) | Whether measured value should be <= or >= threshold |
| `metrics[].deviation_pct` | float | ((measured - threshold) / threshold) * 100; negative means favourable deviation for gte metrics |
| `metrics[].status` | string enum (ok, approaching, breached) | Per-metric breach status |
| `metrics[].advisory_note` | string or null | Human-readable advisory text shown on breach; null when status is ok |

### 6.2 Component State Modes

The component renders one of four states based on the `status` field:

#### Loading State

Triggered: while the `useQuery` fetch is in-flight.

Render: four skeleton cards in the same 2×2 grid layout. Each card shows an animated pulse placeholder where the metric value would appear (matching the pattern in `Arc5ComplianceSection.js`). The section heading "Behavioural Drift — Advisory" is visible and static during loading to prevent layout shift.

#### Insufficient Data State (status: "insufficient_data")

Triggered: when `trade_count < 20` (per the PT-04 gate defined in `data_prerequisite_audit.md §2.1`).

Render: a single muted panel (no metric cards) with the message:

> "Behavioural drift analysis requires at least 20 closed trades. Currently {trade_count} trade(s) recorded. This panel will activate automatically once the threshold is reached."

No metric cards are rendered. The advisory label remains visible. No error styling — this is an expected transitional state, not a failure.

#### No Drift Detected State (status: "no_drift")

Triggered: when all metrics have `status: "ok"`.

Render: metric cards are shown in their green (ok) state, with deviation values displayed. The section heading includes a subdued "All metrics within threshold" indicator. This is a positive state and must not be styled as empty or neutral-grey to avoid creating the impression that the feature is non-functional.

#### Drift Detected State (status: "drift_detected")

Triggered: when one or more metrics have `status: "breached"` or `status: "approaching"`.

Render: metric cards with colour-coded borders:
- `ok` — green border (`border-emerald-500/60`)
- `approaching` — amber border (`border-amber-500/60`)
- `breached` — red border (`border-rose-500/60`)

Breached cards show the `advisory_note` below the deviation value. Approaching cards show no advisory note but use amber styling. The advisory label is prominent.

#### Error / Fetch Failure State

Triggered: when the query returns an error (network failure, 5xx).

Render: a single panel with the message "Unable to load drift analysis." and a Retry button. Matches the error pattern in `DisciplineComplianceSection.js`.

---

## 7. Advisory Label Specification

The component section heading must include a visible "Advisory" badge at all times (including in loading and insufficient-data states). Proposed heading structure:

```
Behavioural Drift   [Advisory]
```

Where `[Advisory]` is a small pill badge using amber/yellow styling (consistent with advisory indicators elsewhere in the app) — not red (red implies error/block) and not green (green implies approval). The badge must be visible without hover interaction.

This satisfies the §13 display-only binding condition from `section13_criteria.md §3.2`.

---

## 8. Visual Layout Specification

The component renders within the existing `PerformanceAnalytics` page as a new section, consistent with the sectional pattern (`DisciplineComplianceSection`, `Arc5ComplianceSection`).

**Grid:** 2 columns on `sm+`, 1 column on mobile — matching `Arc5ComplianceSection`'s layout for four-metric groups. Use `grid-cols-1 sm:grid-cols-2 gap-4`.

**Card structure per metric (Option B):**

```
+----------------------------------------------+
| ENTRY TIMING                         [icon]  |
|                                              |
| 2.4 days                                     |
| Threshold: <= 1.0 days                       |
| Deviation: +140% above threshold             |
|                                              |
| Advisory: Entries are averaging 2.4 days     |
| after signal -- review entry execution.      |
+----------------------------------------------+
  border-rose-500/60 (breached)
```

Card anatomy:
- Top-left: metric label (uppercase, `text-xs text-slate-400 tracking-wider`)
- Top-right: Lucide icon (`w-4 h-4`)
- Primary value: measured value + unit (`text-2xl font-bold text-white`)
- Sub-line 1: threshold statement (`text-xs text-slate-400`)
- Sub-line 2: deviation percentage, coloured by status (`text-sm font-medium`)
- Advisory note (breached only): `text-xs text-amber-400 mt-2`
- Card background: `bg-slate-800/50 border border-slate-700/50 rounded-2xl p-6 backdrop-blur-sm` (matching established pattern)
- Coloured border overlay: driven by metric `status`

---

## 9. Props Interface (Pre-Design)

This section defines the expected React props for ST-11 to formalise into a full interaction spec.

```js
// DriftAnalysisPanel -- top-level component
// Props:
{
  period: string,  // e.g. "last_90_days" -- passed from PerformanceAnalytics time period selector
}

// DriftMetricCard -- per-metric sub-component
// Props:
{
  metric: {
    metric_id: string,
    label: string,
    description: string,
    measured_value: number,
    measured_unit: string,
    threshold_value: number,
    threshold_direction: "lte" | "gte",
    deviation_pct: number,
    status: "ok" | "approaching" | "breached",
    advisory_note: string | null,
  },
  isLoading: boolean,
}
```

The `period` prop connects the drift analysis window to the existing time period selector on the `PerformanceAnalytics` page, ensuring all analytics panels use a consistent analysis window. Whether the backend respects the `period` parameter for drift analysis (vs. using a fixed 90-day window) is a decision for the backend API contract — this pre-design documents the expected prop; the interaction spec (ST-11) must resolve the binding behaviour.

---

## 10. Out of Scope for This Document

The following are explicitly deferred to ST-11 (BLG-FE-53 — interaction spec) or the SI-02 implementation sprint:

- Full interaction specification (hover states, tooltip content, keyboard navigation)
- Exact icon selection per metric
- Gradient colour assignments per metric (consistent with existing `DisciplineComplianceSection` gradient scheme but not defined here)
- Whether a top-level summary badge (Option A composite) is added above the metric grid
- Exact threshold values for `approaching` vs. `breached` (these come from `docs/specs/metrics_definitions.md` SI-02 section, which must be authored before SI-02 sprint planning seals per `section13_criteria.md §3.1`)
- Playwright automated test coverage (required per CLAUDE.md §2 for any frontend-visible change — deferred to implementation sprint)
- Placement decision within `PerformanceAnalytics.js` (before or after existing compliance sections)

---

## 11. Input to ST-11 (BLG-FE-53)

This document is the primary input to ST-11. The interaction spec (ST-11) must:

1. Adopt the selected option (Option B — Percentage Deviation Display) or document the rationale for overriding it
2. Formalise the data contract in §6.1 as the binding API response shape for the `GET /analytics/behavioural-drift` endpoint
3. Define the exact hover, tooltip, and keyboard interaction behaviours for each card state
4. Define the gradient and icon assignments per metric
5. Confirm whether the `period` prop drives the backend analysis window or is decorative
6. Specify Playwright test cases for the four component states (loading, insufficient data, no drift, drift detected)

The data contract in §6.1 should be treated as provisional until the backend API contract is formally authored. Any divergence from this shape must be reflected back into this document as a version bump before the SI-02 sprint planning seals.

---

## 12. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Frontend Specs & UX Documentation Owner | Active | 2026-05-29 |
| Head of Frontend Engineering | Pending | — |
| Product Owner | Pending | — |
