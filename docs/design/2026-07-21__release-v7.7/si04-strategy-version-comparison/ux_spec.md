**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-07-21
**Cycle:** 2026-07-21__release-v7.7
**Story:** ST-01 (EPIC-01, BLG-FEAT-75)

---

# UX Decision Record — SI-04 Strategy Version Performance Comparison

## 1. Problem

ST-01 requires a side-by-side performance comparison between two `strategy_rules.md` versions, at minimum surfacing win rate, average R, and compliance rate per version. The backlog item's AC offers two placement options: "a new panel in the Arc 5 compliance UI (via `BLG-FE-59`'s shared extension point) and/or a dedicated comparison view."

## 2. Placement Decision

**Chosen: dedicated comparison view — a new tab on the existing Strategy Benchmark page (`/strategy/benchmark`).**

**Rejected: embedding in `Arc5ComplianceSection` via `BLG-FE-59`'s extension point.**

**Rationale:** `BLG-FE-59` (Arc5ComplianceSection extension spec for SI-02/SI-04) is not in this cycle's `stage4_backlog_slice.md` — it remains an unscheduled backlog item (`claude/backlog/backlog.md`). Its gate criteria ("SI-02 frontend + SI-04 sprint planning imminent") is technically met by this cycle, but committing SI-04's design gate to a dependency that itself has not cleared sprint planning would either block EPIC-01 or require silently pulling an out-of-scope item into v7.7. The AC's explicit "and/or" gives latitude to resolve this now: the dedicated-view path avoids the dependency entirely, ships this cycle, and does not preclude an `Arc5ComplianceSection` card being added later once `BLG-FE-59` is actually executed.

**Why Strategy Benchmark and not a new top-level nav item:** Strategy Benchmark (`strategy_benchmark.md`) already owns "compare strategy execution against expectation" framing (live vs. backtest). Version-to-version comparison is a close conceptual sibling. Adding a tab reuses the existing nav entry rather than growing the sidebar — consistent with EPIC-02's nav-consolidation goal landing in the same release; adding one new top-level item while EPIC-02 removes a duplicate one would be a net contradiction of this cycle's own intent.

## 3. API Contract Gap (flagged, not blocking)

`docs/specs/api_contracts/strategy_version_comparison_contract.md` (v0.1.0, pre-sprint draft, 2026-06-01) defines `GET /analytics/strategy-version-comparison` with `trade_count`, `win_rate`, `avg_R`, `performance_delta` per version — **it does not include a compliance-rate field**, which ST-01's AC requires ("win rate, average R, and compliance rate per version").

This routine's write scope excludes `docs/specs/api_contracts/` (§5, design gate prompt), so the contract cannot be amended here. **Flagged for Sprint Execution:** the contract needs a `compliance_rate` field added to `version_from_metrics`/`version_to_metrics` (0.1.0 → 0.2.0), most naturally sourced the same way as `analytics.md` §17's existing "Discipline & Compliance" panel (journal completion rate) or the Arc 5 composite score (`GET /analytics/arc5-compliance`) — whichever the Strategy Rules & System Intent Owner confirms is the intended "compliance rate" reading for a per-version historical slice. This is a contract/backend decision, not a frontend design decision, so it is not resolved in this artefact. The frontend spec below (§4, `strategy_benchmark.md`) renders the field as present-but-pending until the contract is updated, so the UI does not need rework once it lands.

This does not block Design Gate PASS: the frontend UX and layout are fully specifiable against the existing contract shape, with the compliance-rate row rendering `—` until the contract/backend catches up.

## 4. Layout

New tab on Strategy Benchmark page, added to the page's existing sub-navigation alongside its current single view:

**Tab label:** "Version Comparison"
**Route:** `/strategy/benchmark?tab=version-comparison` (client-side tab state, no new top-level route)

### Controls row
Two version-select dropdowns ("Compare" / "Against"), populated from the strategy version registry (per contract §Implementation Notes 2). Labelled **"From"** and **"To"**. A **"Compare"** button triggers the fetch (not auto-fetch on dropdown change, to avoid firing requests on every intermediate selection).

### Comparison table
Three columns: Metric | `{version_from}` | `{version_to}`. Rows, in order:

| Metric | Source field |
|--------|-------------|
| Trades Compared | `trade_count` |
| Win Rate | `win_rate` (formatted `XX.X%`) |
| Average R | `avg_R` (formatted `X.XXR`) |
| Compliance Rate | *pending contract update — render `—` with tooltip "Not yet available" until `compliance_rate` ships* |

Below the table: a **"Comparison Summary"** strip showing `win_rate_delta`, `avg_R_delta`, `trade_count_delta` as signed values (`+0.05`, `-0.12R`) with directional colour (green = improvement, red = degradation, per `performance_delta` sign convention in the contract), and the `assessment` value ("Improved" / "Degraded" / "Insufficient data") as a badge.

### States

| State | Trigger | Behaviour |
|-------|---------|-----------|
| Idle | Initial load, no comparison run yet | Controls row only; empty-state copy: "Select two strategy versions to compare." |
| Loading | Compare clicked | Table area shows skeleton rows; Compare button disabled |
| Loaded | 200 response | Table + summary strip populated |
| Insufficient data (422) | `insufficient_data` | Table area replaced with: "Not enough trades to compare — {version} has {trade_count} trades (minimum 10 required)." No partial table. |
| Version not found (404) | `version_not_found` | Inline error under the offending dropdown: "Version not found." |
| Invalid order (400) | `version_order_error` | Inline error under "To" dropdown: "Must be chronologically after the 'From' version." |
| Error (other) | Network/5xx | "Unable to load comparison. Please try again." with Retry |

## 5. Constraints

- Read-only. No action can be taken from this view that modifies strategy configuration or live positions (per contract §13 binding conditions 2, 4, 5).
- No trade-volume gate on the feature itself (PO decision, `decisions--2026-07-21__release-v7.7.md`) — the per-version 10-trade minimum is the contract's own `insufficient_data` threshold, not a feature-level gate.

## 6. Approval

Product Owner: approved 2026-07-21 (dedicated-view placement, contract-gap flag accepted as a Sprint Execution follow-up rather than a design-gate blocker).
Head of UX & Design: approved 2026-07-21.
