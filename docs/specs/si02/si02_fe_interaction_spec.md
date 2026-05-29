**Owner:** Frontend Specs & UX Documentation Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.4 (EPIC-03, ST-11, BLG-FE-53)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# SI-02 Drift Detection Interaction Specification

> **Gate verified (AC-05):** ST-10 output `docs/specs/si02/si02_fe_component_predesign.md` committed at 070a4663 on exec/2026-05-29__release-v4.4/EPIC-03. Option B (Percentage Deviation Display) adopted as selected. Data contract in §6.1 of that document is the binding API response shape for `GET /analytics/behavioural-drift`. Any divergence from that shape before SI-02 sprint planning seals requires a version bump to both documents.

---

## 1. Purpose

This document formalises the interaction behaviour of the SI-02 Behavioural Drift Detection frontend component (`DriftAnalysisPanel` and `DriftMetricCard`). It covers state transitions, dismissal model, drill-down behaviour, severity thresholds, and the period filter binding.

This spec is the binding source of truth for the implementation sprint. Where this document conflicts with ST-10 (`si02_fe_component_predesign.md`), this document takes precedence for interaction behaviour; ST-10 takes precedence for visual layout and component data contract shape.

All §13 advisory constraints defined in `docs/specs/si02/section13_criteria.md §3.2` apply throughout this document. They are summarised in §2 and must not be relaxed by any implementation decision.

---

## 2. §13 Advisory Constraints (Carried Forward)

The following constraints from `section13_criteria.md §3.2` are binding on all interaction decisions in this spec:

1. The "Advisory" badge must be visible at all times — including loading and insufficient-data states — without hover or expansion.
2. No UI affordance (button, link, action prompt) may imply automated remediation of any detected drift.
3. Drift detection results must not gate, block, or modify any trade plan, position entry, or exit workflow.
4. SI-02 drift findings are read-only displays. Users act on findings manually.

These constraints are non-negotiable. Any implementation PR that adds a "Fix" button, an automated correction prompt, or any gating behaviour on the basis of drift state is a §13 violation and must be blocked at code review.

---

## 3. Component State Transitions

### 3.1 States Overview

The `DriftAnalysisPanel` renders in exactly one of five states at any time. The rendering state is derived from the combination of the query fetch lifecycle and the `status` field in the API response:

| State | Trigger condition | Priority |
|-------|-------------------|----------|
| `loading` | Query is in-flight (fetch pending) | Highest |
| `error` | Query returned a network error or HTTP 5xx | 2 |
| `insufficient_data` | Response received; `status === "insufficient_data"` | 3 |
| `no_drift` | Response received; `status === "no_drift"` | 4 |
| `drift_detected` | Response received; `status === "drift_detected"` | 5 |

Priority is relevant only when state conditions could be ambiguous (e.g. a stale error result while a new fetch is in-flight). The `loading` state always takes priority.

### 3.2 Fetch and Re-Fetch Triggers

The `DriftAnalysisPanel` uses a `useQuery` hook (React Query / TanStack Query). The query key is:

```js
['behavioural-drift', period]
```

where `period` is the `period` prop passed from `PerformanceAnalytics` (see §7 for period binding).

**Automatic re-fetch triggers:**

| Trigger | Behaviour |
|---------|-----------|
| Component mount | Always fetches on mount (no cached data assumed for first render) |
| `period` prop change | Re-fetches immediately; returns to `loading` state during in-flight |
| Window regain focus | Re-fetches if data is older than 5 minutes (standard TanStack Query `staleTime: 5 * 60 * 1000`) |
| Retry button (error state) | User-triggered re-fetch; returns to `loading` state |
| Automatic background refresh | Disabled — drift metrics change only when new trades are added; polling adds no value for a single-user context |

**No automatic re-fetch on:** component scroll into view, tab switch, or hover. These are consistent with the behaviour of `DisciplineComplianceSection` and `Arc5ComplianceSection`.

### 3.3 State Transition Diagram

```
                    +-----------------------------------------+
                    |                                         |
       mount / period change / retry                          |
                    |                                         |
                    v                                         |
              +----------+                                    |
              | loading  |                                    |
              +----------+                                    |
               /   |   \                                      |
   network    /    |    \                                     |
   error     /     |     \                                    |
            /      |      \                                   |
           v       |       v                                  |
      +-------+    |  +----------------+                      |
      | error |    |  | insufficient_  |                      |
      +-------+    |  |    data        |                      |
          |        |  +----------------+                      |
       retry       |         |                                |
          |        |    trade_count                           |
          +--------+    reaches 20                            |
                   |    (next mount)                          |
                   |         |                                |
                   |         v                                |
             +-----+--+  +----------+                        |
             |no_drift|  | no_drift |                        |
             +--------+  +----------+                        |
                   |                                          |
         metric status    period change                       |
         changes to       or focus refetch                    |
         approaching/     (staleTime expired) ----------------+
         breached
                   |
                   v
          +----------------+
          | drift_detected |
          +----------------+
                   |
         all metrics         period change
         return to ok        or focus refetch -----------------+
                   |                                          |
                   v                                          |
             +----------+                                     |
             | no_drift |<------------------------------------+
             +----------+
```

**Key transition notes:**

- `insufficient_data` to `no_drift` or `drift_detected`: This transition does not happen within a session (it requires new trade data to be added). The panel activates on the next component mount after trade_count reaches 20.
- `drift_detected` to `no_drift`: Happens automatically when the next fetch returns all metrics with `status: "ok"`. No user action required.
- `error` to any: Only via user-triggered retry or a new mount.

---

## 4. Dismissal Model

### 4.1 Decision

**Adopted approach: Non-dismissable with session-collapse.**

The drift panel is non-dismissable as a whole — it does not disappear when drift is detected. Drift information persists until the underlying metrics return to within-threshold values (i.e. the dismissal condition is resolved data, not user action).

However, a **collapse affordance** is provided: the panel section heading includes a chevron toggle that allows the user to collapse the metric card grid. This follows the established collapsible section pattern used elsewhere in `PerformanceAnalytics`. The collapsed state is persisted to `localStorage` under the key `si02.driftPanel.collapsed`.

**Rationale for non-dismissable approach:**

- **Advisory integrity:** Allowing full dismissal would let the user hide active drift warnings indefinitely. For a §13-compliant advisory feature, the drift state should remain visible to fulfil its informational purpose.
- **MVP complexity:** Snooze (N-day dismissal) requires backend persistence and a `settings` field schema change — out of scope for MVP.
- **Session-dismissable alternative rejected:** A pure session-dismissable approach (dismiss until next page load) provides no information durability. If the user reloads the page during an active trading session, they would see the drift warning again with no indication they had already reviewed it.
- **Collapse is sufficient:** The user has acknowledged the drift when they collapse the panel. The section heading remains visible with a compact status indicator (see §4.2) to surface the drift state even when collapsed.

### 4.2 Collapsed State Heading

When the panel is collapsed, the section heading renders a compact status indicator alongside the "Advisory" badge:

```
Behavioural Drift   [Advisory]   [! 2 metrics drifting]   >
```

Where:
- `! N metrics drifting` is shown when `status === "drift_detected"` — N is the count of metrics with `status: "approaching"` or `status: "breached"`
- No indicator shown when `status === "no_drift"` (the absence of indicator communicates the positive state)
- Loading spinner shown when `status === "loading"` (collapsed with in-flight data)
- The chevron toggles collapse

The compact indicator must not include a dismiss or close affordance. It is informational only.

### 4.3 localStorage Persistence

The collapse state is persisted to `localStorage` under the key `si02.driftPanel.collapsed` (boolean). This survives page reloads but not browser profile changes. The collapse state is independent of the drift status — a user who collapses the panel when drift is detected will see the collapsed heading with the compact indicator on reload.

**Re-appearance logic:** The panel never re-appears automatically (it is always mounted). If the user has collapsed the panel and drift resolves, the compact status indicator in the collapsed heading changes to reflect the no-drift state. The user may expand to confirm.

---

## 5. Drill-Down Behaviour

### 5.1 Decision

**Adopted approach: No drill-down for MVP.**

The `DriftMetricCard` displays metric value, threshold, deviation percentage, and the advisory note (for breached metrics). No link to underlying trades is provided.

**Rationale:**

- **Trade History filter dependency:** Linking to `/trades?filter=<metric>` requires the Trade History page to support parameterised filters on metric-specific fields (e.g. `setup_type`, `entry_lag_days`). This filter capability is not currently available and would constitute a cross-EPIC dependency that extends SI-02's scope.
- **Inline table complexity:** An inline expanded table within a `DriftMetricCard` would require the API to return per-trade records as part of the drift response, significantly increasing response payload size and backend complexity for an MVP feature.
- **Advisory note sufficiency:** The `advisory_note` field from the API provides targeted, actionable language for each breached metric (e.g. "Entries are averaging 2.4 days after signal — review entry execution timing."). This addresses the user's immediate need without requiring navigation to underlying data.
- **Future path preserved:** The `metric_id` field in the API response is a stable identifier. A future story can add a "View trades" link that passes `metric_id` as a filter parameter to Trade History once filter support is added.

### 5.2 Future Drill-Down Path (Deferred)

When Trade History parameterised filter support is available, the drill-down interaction will be:

- Each breached `DriftMetricCard` gains a "View contributing trades" link at the bottom.
- The link navigates to `/trades?drift_metric=<metric_id>&window=<analysis_window_days>`.
- The Trade History page filters to trades within the analysis window that contributed to the metric breach.
- This is a backlog item and must not be implemented within SI-02 without a separate story and §13 review for the Trade History filter.

---

## 6. Severity Thresholds

### 6.1 Per-Metric Status Values

Each metric in the API response carries a `status` field with one of three values:

| Status | Meaning | Card border colour |
|--------|---------|-------------------|
| `ok` | Measured value is within threshold | `border-emerald-500/60` (green) |
| `approaching` | Measured value is within 20% of threshold breach | `border-amber-500/60` (amber) |
| `breached` | Measured value has exceeded the threshold | `border-rose-500/60` (red) |

The `status` values are computed server-side. The frontend does not re-derive status from `deviation_pct` — it renders the status exactly as returned by the API. This ensures determinism (§13 criterion 3.1) and single source of truth.

### 6.2 Approaching Threshold Definition

**For MVP, the "approaching" threshold is hard-coded at 20% of remaining headroom:**

- For `lte` metrics (measured value should be <= threshold):
  - `approaching` when `measured_value > threshold * 0.8` AND `measured_value <= threshold`
  - Example: threshold = 1.0 days; approaching window = [0.8, 1.0] days
- For `gte` metrics (measured value should be >= threshold):
  - `approaching` when `measured_value < threshold * 1.2` AND `measured_value >= threshold`
  - Example: threshold = 90%; approaching window = [90%, 108%]

**Rationale for hard-coded thresholds:**

- Configurable thresholds require a `settings` field and a schema migration — out of scope for MVP.
- The 20% approaching window is a reasonable general-purpose signal: it gives the user advance notice without generating excessive amber warnings.
- The `section13_criteria.md §5.3` challenger point flags that hard-coded thresholds require documented rationale. This paragraph constitutes that rationale.
- The approaching threshold values must be formally documented in `docs/specs/metrics_definitions.md` SI-02 section before SI-02 sprint planning seals (per `section13_criteria.md §3.1` binding condition).

### 6.3 Top-Level Component Status Derivation

The `DriftAnalysisPanel` derives its top-level status from the API response's top-level `status` field — not from re-aggregating metric statuses. The server-side derivation rule is:

- `no_drift`: all metrics `status === "ok"`
- `drift_detected`: one or more metrics `status === "approaching"` OR `status === "breached"`

The frontend surfaces this distinction in the collapsed heading (§4.2) and in the section heading styling:

| Top-level status | Section heading accent |
|-----------------|----------------------|
| `no_drift` | Subdued green text: "All metrics within threshold" |
| `drift_detected` | Amber/red accent consistent with highest-severity metric present |
| `loading` | No accent; static heading only |
| `insufficient_data` | No accent; muted heading only |
| `error` | No accent; muted heading only |

### 6.4 Advisory Note Visibility

Advisory notes (`advisory_note`) are shown only for `breached` metrics. `approaching` metrics show amber card styling but no advisory note text. This avoids over-warning for metrics that have not yet breached threshold.

---

## 7. Period Filter Binding

### 7.1 Decision

**The `period` prop drives the backend analysis window.**

The `DriftAnalysisPanel` receives a `period` prop from the parent `PerformanceAnalytics` component (e.g. `"last_30_days"`, `"last_90_days"`, `"all_time"`). This prop is passed as a query parameter to `GET /analytics/behavioural-drift`:

```
GET /analytics/behavioural-drift?period=last_90_days
```

The backend must respect this parameter and return drift calculations over the specified window. The `analysis_window_days` field in the API response confirms the window applied.

**Rationale:** All panels in `PerformanceAnalytics` use the same time period selector. Drift metrics that do not respond to the period selector would create a confusing inconsistency — a user selecting "last 30 days" expects all panels to reflect that window.

### 7.2 Period Parameter Mapping

The frontend maps the period selector values to query parameter values as follows:

| Selector value | Query parameter |
|---------------|-----------------|
| Last 30 days | `period=last_30_days` |
| Last 90 days | `period=last_90_days` |
| All time | `period=all_time` |

The default period (on first mount, before user selection) is `last_90_days`, consistent with the default used by other analytics panels.

### 7.3 Backend Constraint

The backend API contract for `GET /analytics/behavioural-drift` must document:

- The `period` query parameter is required (or has a documented default of `last_90_days`).
- The `analysis_window_days` field in the response reflects the actual window applied, not the requested period string.
- The minimum trade count check (`data_sufficient: boolean`, `trade_count: integer`) is evaluated within the requested period window — i.e. if fewer than 20 trades exist in the last 30 days, `status: "insufficient_data"` is returned for that period even if 50+ trades exist overall.

This constraint must be reflected in the SI-02 API contract document authored before sprint planning seals.

### 7.4 No Dedicated Panel Period Selector

The drift panel does not have its own period selector widget. It consumes the period from the parent component exclusively. Adding a panel-local selector would diverge from the `PerformanceAnalytics` unified period pattern and is deferred unless a specific use case arises.

---

## 8. Tooltip and Hover Interactions

### 8.1 Metric Card Tooltip

Each `DriftMetricCard` renders a tooltip on hover of the metric label (top-left text). The tooltip content is the `description` field from the API response (e.g. "Average days from signal date to trade entry"). This provides context for users unfamiliar with the metric without cluttering the card face.

Implementation: use the existing Tooltip component from the shared component library, matching the pattern in `DisciplineComplianceSection.js`. Tooltip trigger: hover on the metric label text (not the entire card).

### 8.2 Deviation Percentage Tooltip

The deviation percentage line (e.g. "+140% above threshold") renders a tooltip on hover showing the calculation formula:

```
((measured - threshold) / threshold) x 100
= ((2.4 - 1.0) / 1.0) x 100
= +140.0%
```

For `gte` metrics where a negative deviation is favourable (e.g. "-2.2% below threshold"), the tooltip renders:

```
((threshold - measured) / threshold) x 100
= ((90.0 - 92.0) / 90.0) x 100
= -2.2% (favourable)
```

This satisfies the §13 determinism criterion (3.1) by making the calculation transparent to the user.

### 8.3 Advisory Badge Tooltip

The "Advisory" badge in the section heading renders a tooltip on hover:

> "Behavioural drift detection is advisory only. Results are for self-review and do not affect trade plan submission or position management."

This text reinforces the §13 constraint at the point of user contact.

### 8.4 No Hover Action Affordances

No hover state on any card or element reveals an action button. Hover states are informational only (tooltips, subtle background shade change matching the established card hover pattern). This is a hard constraint per §13 advisory-only binding.

---

## 9. Keyboard and Accessibility

### 9.1 Keyboard Navigation

- The collapse/expand chevron in the section heading is keyboard-focusable (`tabIndex={0}`) and responds to Enter and Space.
- The metric label (tooltip trigger) is keyboard-focusable and tooltip appears on focus.
- The deviation percentage (tooltip trigger) is keyboard-focusable and tooltip appears on focus.
- The retry button (error state) is keyboard-focusable and responds to Enter.
- Tab order within the panel: chevron toggle, then metric cards (left-to-right, top-to-bottom), then metric labels, then deviation percentages.

### 9.2 ARIA

- `DriftAnalysisPanel` root element: `role="region"` with `aria-label="Behavioural Drift Analysis — Advisory"`
- Each `DriftMetricCard`: `role="article"` with `aria-label="{metric.label} — {metric.status}"`
- The "Advisory" badge: `aria-label="Advisory: this panel is informational only"`
- Skeleton cards (loading state): `aria-busy="true"` on the panel root; skeleton cards have `aria-hidden="true"`
- Collapsed state: section heading includes `aria-expanded={!collapsed}` on the chevron button

### 9.3 Colour Contrast

Card border colours (`border-emerald-500/60`, `border-amber-500/60`, `border-rose-500/60`) must not be the sole differentiator for metric status. The status text ("Within threshold", "Approaching threshold", "Threshold breached") must also be rendered on the card face for screen reader and colour-blind accessibility. This text is visually subtle (`text-xs text-slate-400`) but must be present in the DOM.

---

## 10. Playwright Test Coverage Specification

Per CLAUDE.md §2, all observable AC (visible rendering, element presence/absence, colour, interaction, timing) require either Playwright test coverage or human staging sign-off before the PR merges. The following test cases must be covered before the SI-02 implementation sprint closes.

### Test Case Reference Table

| Test ID | State | Observable behaviour | Coverage method |
|---------|-------|---------------------|-----------------|
| DFT-01 | Loading | Four skeleton cards visible; "Behavioural Drift — Advisory" heading visible | Playwright |
| DFT-02 | Insufficient data | Single muted panel visible; trade_count in message matches API response | Playwright |
| DFT-03 | No drift | Four metric cards rendered; all green borders; "All metrics within threshold" visible | Playwright |
| DFT-04 | Drift detected — approaching | Amber border on approaching metric card; no advisory note visible | Playwright |
| DFT-05 | Drift detected — breached | Red border on breached metric card; advisory note text visible | Playwright |
| DFT-06 | Error state | Error message visible; Retry button present and focusable | Playwright |
| DFT-07 | Collapse/expand | Chevron click collapses panel; compact heading indicator visible; expand restores cards | Playwright |
| DFT-08 | Period change | Re-fetch triggered on period prop change; loading state re-entered | Playwright |
| DFT-09 | Tooltip — metric label | Hover/focus on metric label shows description tooltip | Playwright |
| DFT-10 | Tooltip — deviation | Hover/focus on deviation line shows formula tooltip | Playwright |
| DFT-11 | Tooltip — Advisory badge | Hover/focus on Advisory badge shows advisory-only disclaimer | Playwright |
| DFT-12 | Accessibility | Panel has `role="region"` with correct `aria-label`; chevron has `aria-expanded` | Playwright |
| DFT-13 | localStorage collapse | Collapse state persists across page reload | Playwright |

These test IDs must be referenced in the implementation story's DoQ sign-off block. Any DFT test not covered by automated Playwright tests before the PR opens must have a backlog item filed via `/backlog-add` with Playwright coverage deferred to post-merge.

---

## 11. Deferred Items

The following items are explicitly deferred to the implementation sprint or a later story:

| Item | Deferred to | Notes |
|------|-------------|-------|
| Exact icon per metric (Lucide) | Implementation sprint | Icons must be consistent with existing section patterns |
| Gradient colour assignments per metric | Implementation sprint | Follow `DisciplineComplianceSection` gradient scheme |
| Formal drift formula documentation in `metrics_definitions.md` | Before SI-02 sprint planning seals | Required by `section13_criteria.md §3.1` binding condition |
| Configurable approaching/breached thresholds | Post-MVP | Requires `settings` schema change |
| Drill-down to Trade History | Post-MVP | Requires Trade History parameterised filter support |
| Summary badge (Option A composite) above metric grid | Post-MVP | Composable from Option B data without API rework |
| Telegram notification for drift | Post-MVP | Must be advisory-only `drift_alert` type; separate §13 review required |
| Placement of panel within `PerformanceAnalytics.js` | Implementation sprint | Engineering decision subject to UX review |

---

## 12. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Frontend Specs & UX Documentation Owner | Active | 2026-05-29 |
| Head of Frontend Engineering | Pending | — |
| Product Owner | Pending | — |
