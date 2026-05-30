**Owner:** Metrics Definitions & Analytics Canonical Owner; Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.5 (EPIC-03, ST-07, BLG-SPEC-41)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**§13 gate:** PASS — `docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md`

---

# SI-02 Drift Detection Score — Metric Definition

## 1. Purpose

This document defines the canonical metric definitions for SI-02 Behavioural Drift Detection. It covers four drift metrics, their formulas, rolling windows, threshold bands (green/amber/red), warning state triggers, and SI-05 weekly digest integration points.

All formulas are deterministic. Per §13 PASS (decision record above), no ML inference, no probabilistic scoring, and no automated actions are permitted from these metrics.

---

## 2. Common Definitions

### 2.1 Analysis Window

**Default rolling window:** 90 calendar days

**Rationale:** 90 days provides a meaningful sample of trading activity for a solo swing trader operating on momentum signals. Shorter windows (30 days) produce statistically noisy signals when trade frequency is low; longer windows (180 days) reduce the sensitivity of drift detection to recent behavioural changes.

**Minimum trade threshold:** 10 closed trades within the analysis window. Below this threshold, the endpoint returns `status: "insufficient_data"` and no metric values are computed. This prevents false drift signals from a single outlier trade.

**Override:** The analysis window is hard-coded in the backend service at 90 days. It is not user-configurable in Sprint 1. If future configurability is required, a `settings` field addition requires a separate sprint and schema change.

### 2.2 Metric Status States

Each metric is classified into one of three states:

| State | Value | Card colour | Meaning |
|-------|-------|-------------|---------|
| `ok` | Within threshold | Green | Measured value is within the acceptable range |
| `approaching` | Within 20% of threshold breach | Amber | Measured value is approaching the breach threshold — review warranted |
| `breached` | Beyond threshold | Red | Measured value has exceeded the acceptable threshold |

**Approaching band calculation:**

For `lte` metrics (measured value should be ≤ threshold):
- `ok`: measured ≤ threshold × 0.80
- `approaching`: threshold × 0.80 < measured ≤ threshold
- `breached`: measured > threshold

For `gte` metrics (measured value should be ≥ threshold):
- `ok`: measured ≥ threshold × 1.20
- `approaching`: threshold ≤ measured < threshold × 1.20
- `breached`: measured < threshold

**Rationale for 20% approaching band:** Gives the user an early warning before a threshold is breached. Consistent with the amber/warn pattern used in SI-01 pre-entry validation (sector concentration, earnings proximity).

### 2.3 Deviation Percentage Formula

```
deviation_pct = ((measured_value - threshold_value) / threshold_value) × 100
```

For `gte` metrics (higher is better), a positive deviation_pct is favourable; a negative deviation_pct indicates breach. The frontend displays the absolute magnitude with directional language ("below threshold" or "above threshold") rather than raw signed percentage.

---

## 3. Metric Definitions

### 3.1 Entry Timing Drift

**metric_id:** `entry_timing_drift`
**Label:** Entry Timing
**Description:** Average days from signal date to actual trade entry date across the analysis window

**What it measures:** How promptly the user acts on signals. A large average lag suggests the user is entering late relative to the signal, which can reduce the quality of entries (missed breakouts, higher entry prices relative to the setup).

**Formula:**

```
entry_timing_drift = AVG(positions.entry_date - signals.signal_date)
                     WHERE trade_plans.signal_id IS NOT NULL
                       AND positions.entry_date >= NOW() - INTERVAL '90 days'
```

**Prerequisite:** DS-07 migration must be deployed (adds `signal_id` column to `trade_plans` and `idx_trade_plans_signal` index).

**Measured unit:** days (positive = lag; negative = entry before signal, which is anomalous and should surface as a data quality flag)

**Handling entries without linked signal:** Entries where `trade_plans.signal_id IS NULL` are excluded from this metric calculation. The `advisory_note` must include the count of excluded entries: "X of Y trades in the window have no linked signal and are excluded from timing analysis."

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| Green (ok) | avg ≤ 0.80 days | Entries within 1 day of signal (same-day or next morning), no approaching band |
| Amber (approaching) | 0.80 < avg ≤ 1.0 days | Entering same-day to next-day — within acceptable range but trending toward late |
| Red (breached) | avg > 1.0 days | Consistently entering more than 1 day after signal — meaningful momentum loss possible |

**Rationale for 1-day threshold:** Momentum signals are time-sensitive. A 1-day entry lag is operationally unavoidable (signals generated after market close, entered next morning). A consistent lag beyond 1 day suggests either hesitation (waiting for additional confirmation not in the strategy rules) or systematic delay in workflow. This aligns with the strategy's intent to capture breakout momentum promptly.

**SI-05 integration:** Weekly digest surfaces: "Entry timing: X days avg (within threshold / approaching / breached)." If breached: "Consider reviewing your entry workflow — you are averaging X days after signal date."

---

### 3.2 Sizing Adherence

**metric_id:** `sizing_adherence`
**Label:** Sizing Adherence
**Description:** Average risk % used per trade vs. the strategy-defined maximum

**What it measures:** Whether the user is consistently applying their stated risk per trade. Sizing above the stated maximum indicates a systematic over-risk pattern; sizing significantly below may indicate hesitation or position sizing calculator avoidance.

**Formula:**

```
sizing_adherence = AVG(trade_plans.risk_percent_used)
                   WHERE trade_plans.risk_percent_used IS NOT NULL
                     AND positions.entry_date >= NOW() - INTERVAL '90 days'
```

**Prerequisite:** DS-07 migration must be deployed (adds `risk_percent_used` column to `trade_plans`).

**Handling entries without risk_percent_used:** Entries where `risk_percent_used IS NULL` are excluded and counted in the advisory note.

**Reference value:** The threshold uses `settings.default_risk_percent` at query time. Note: this is the current setting, not the historical setting at entry time. For entries with `effective_settings_snapshot` captured (post DS-07), the snapshot value is used instead. For pre-migration entries, `settings.default_risk_percent` is the proxy.

**Measured unit:** pct_of_portfolio (e.g. 1.5 = 1.5% of portfolio value per trade)

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| Over-sizing (lte threshold) | measured ≤ settings.default_risk_percent × 1.20 | Within 20% of plan max is acceptable — approaching band applies |
| Under-sizing advisory | measured < settings.default_risk_percent × 0.50 | Consistently sizing at less than 50% of plan rate — not a breach, but flagged as a note |
| Amber | plan_max × 0.80 < measured ≤ plan_max | Approaching the plan maximum |
| Red (breached) | measured > plan_max | Consistently over plan maximum |

**Under-sizing treatment:** Under-sizing is advisory only (a separate `advisory_note` field), not a threshold breach. Consistent under-sizing may reflect appropriate caution or may indicate the position sizing calculator is not being used. It is surfaced as informational text, not as an amber/red state.

**SI-05 integration:** Weekly digest: "Sizing adherence: avg X% vs plan max Y% (within threshold / approaching / breached)." If breached: "Average risk per trade is above your plan maximum. Review recent entry sizing."

---

### 3.3 Post-Loss Sizing

**metric_id:** `consecutive_loss_sizing`
**Label:** Post-Loss Sizing
**Description:** Average risk % used in trades entered after 2 or more consecutive losing trades

**What it measures:** Whether the user increases or maintains position size after a run of losses — a common behavioural drift pattern ("sizing up to recover losses") that increases drawdown risk during unfavourable periods.

**Formula:**

```
-- Step 1: classify each trade as win/loss based on pnl
-- Step 2: identify trades entered after ≥2 consecutive losses
-- Step 3: compute avg risk_percent_used for those trades

WITH ranked_trades AS (
  SELECT
    tp.id,
    tp.risk_percent_used,
    p.entry_date,
    th.pnl,
    ROW_NUMBER() OVER (PARTITION BY p.portfolio_id ORDER BY p.entry_date) AS rn
  FROM positions p
  JOIN trade_plans tp ON tp.position_id = p.id
  LEFT JOIN trade_history th ON th.position_id = p.id
  WHERE p.entry_date >= NOW() - INTERVAL '90 days'
),
loss_streaks AS (
  SELECT
    r.id,
    r.risk_percent_used,
    r.entry_date,
    -- count consecutive losses immediately preceding this trade
    (
      SELECT COUNT(*)
      FROM ranked_trades r2
      WHERE r2.rn BETWEEN r.rn - 3 AND r.rn - 1
        AND r2.pnl < 0
        AND r2.rn = (
          SELECT MAX(r3.rn) FROM ranked_trades r3
          WHERE r3.rn < r.rn AND r3.pnl >= 0
        ) + ROW_NUMBER() OVER (PARTITION BY r.id ORDER BY r2.rn)
    ) AS preceding_losses
  FROM ranked_trades r
)
SELECT AVG(risk_percent_used) AS post_loss_sizing
FROM loss_streaks
WHERE preceding_losses >= 2
  AND risk_percent_used IS NOT NULL
```

**Implementation note:** The exact SQL implementation may be simplified at the backend engineering level (the pattern above is the intent). The key invariant: trades entered after 2+ consecutive closed losing trades (by entry date order). The threshold is 2 consecutive losses — not 2 total losses in the window.

**Minimum sample requirement:** This metric requires at least 3 post-loss-streak trades in the window to compute. Below this, `measured_value: null` and `status: "insufficient_data"` for this metric only (not the full endpoint).

**Measured unit:** pct_of_portfolio

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| Reference | `settings.default_risk_percent` | The plan-stated risk maximum |
| Green (ok) | post_loss_avg ≤ plan_max × 0.80 | Sizing down or maintaining conservative sizing after losses |
| Amber (approaching) | plan_max × 0.80 < post_loss_avg ≤ plan_max | Near plan max after losses — borderline acceptable |
| Red (breached) | post_loss_avg > plan_max | Sizing above plan max after losses — classic recovery-seeking pattern |

**Rationale:** The strategy's §7 (trailing stop framework) and §10 (risk summary) establish that losses are tolerated and recoveries are defended — the strategy does not prescribe increasing risk to recover losses. Sizing above plan max during a loss streak is inconsistent with the strategy's risk management intent.

**SI-05 integration:** Weekly digest: "Post-loss sizing: X% avg after consecutive losses (within threshold / breached)." If breached: "You are sizing above plan maximum after consecutive losses. This increases drawdown risk during unfavourable periods."

---

### 3.4 Regime Adherence

**metric_id:** `regime_context`
**Label:** Regime Adherence
**Description:** Percentage of trades entered in a regime declared valid at entry time

**What it measures:** Whether the user is consistently applying the regime gate rule (§8.2 — risk-off regime is an exit condition and advisory caution at entry via §4.2.1). A user who enters positions during risk-off regimes is drifting from the strategy's market-awareness intent.

**Formula:**

```
regime_adherence_pct =
  (COUNT(*) FILTER (WHERE regime_context_at_entry IN ('risk_on', 'neutral', null))
   / NULLIF(COUNT(*), 0)) * 100
FROM positions p
JOIN trade_plans tp ON tp.position_id = p.id
WHERE p.entry_date >= NOW() - INTERVAL '90 days'
```

**Measured unit:** pct (e.g. 92 = 92% of trades entered in valid regime)

**Regime classification:**
- `risk_on`: market index above 200-day MA — strategy-aligned entry
- `neutral`: regime not determinable at entry (e.g. regime_context_at_entry is null due to pre-feature trades) — counted as not a violation
- `risk_off`: market index below 200-day MA — entry during risk-off (flag as potential drift)

**Direction:** `gte` — higher is better (more trades in valid regime)

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| Green (ok) | ≥ 95% valid regime | Occasional risk-off entry acceptable — signal ambiguity, multi-market portfolios |
| Amber (approaching) | 90% ≤ regime_pct < 95% | Noticeably entering positions during risk-off — worth reviewing |
| Red (breached) | < 90% | More than 1 in 10 trades entered during risk-off — systematic drift from strategy intent |

**Rationale for 90% threshold:** A 100% threshold would be unrealistic for multi-market portfolios (US and UK regimes are independent; a position in a risk-on market while the other is risk-off is valid). 90% allows a 1-in-10 tolerance for market ambiguity while flagging systematic risk-off entry patterns.

**SI-05 integration:** Weekly digest: "Regime adherence: X% of trades in valid regime (within threshold / breached)." If breached: "Review recent entries — X% of trades in the window were entered during a risk-off regime signal."

---

## 4. Overall Endpoint Status Logic

The top-level `status` field in the API response is determined as follows:

| Status | Condition |
|--------|-----------|
| `insufficient_data` | Fewer than 10 closed trades in the 90-day window |
| `no_drift` | All metrics with sufficient data are in `ok` state |
| `drift_detected` | At least one metric is in `approaching` or `breached` state |
| `error` | Service computation failure — response includes error details; no metrics returned |

---

## 5. SI-05 Weekly Digest Integration Points

SI-05 (Weekly Digest — scheduled for a future arc) will consume drift data. The following integration contract is defined here so SI-05 sprint planning can reference it without re-deriving.

### 5.1 Digest data source

SI-05 should consume from a pre-computed `drift_snapshots` table (if implemented as a background job per `si02_background_job_adr.md`) OR call `GET /analytics/behavioural-drift` directly at digest generation time.

Recommended path: direct API call at digest generation time (simpler, no snapshot staleness). The background job is a performance optimisation for high-frequency use, not a requirement for SI-05.

### 5.2 Digest content per metric

For each metric, SI-05 should include:
1. **Status badge** — green/amber/red indicator (single word: "On track" / "Approaching limit" / "Drifting")
2. **Current value vs threshold** — "X days avg vs 1.0 day limit" (with unit)
3. **Trend note** (if data available from prior week) — "improved from X / unchanged / worsened from X"
4. **Advisory note** — from `metrics[].advisory_note` (only when status is `approaching` or `breached`)

### 5.3 Digest section heading

Suggested: "Behavioural Drift — Weekly Summary" with an "Advisory" badge consistent with the main panel.

### 5.4 Digest minimal viable output (when `insufficient_data`)

When fewer than 10 closed trades exist: "Behavioural drift analysis requires 10 or more closed trades in the last 90 days. Currently X trades recorded — no drift analysis available."

---

## 6. Threshold Rationale Summary

| Metric | Threshold | Value | Source |
|--------|-----------|-------|--------|
| Entry timing drift | Max lag | 1.0 day | Operational constraint: same-day/next-morning entry is expected; lag beyond 1 day suggests systematic hesitation |
| Sizing adherence | Max risk% | `settings.default_risk_percent` (live) | Directly from user's stated plan; over-sizing is a risk management deviation |
| Post-loss sizing | Max risk% after losses | `settings.default_risk_percent` (live) | Consistent with general sizing rule; no additional tolerance granted for recovery-seeking |
| Regime adherence | Min valid entry % | 90% | Tolerates 1-in-10 multi-market ambiguity; flags systematic risk-off entry patterns |

All thresholds are deterministic and documented. No configurable thresholds in Sprint 1. Future configurability requires a settings schema change and a new sprint.

---

## 7. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Metrics Definitions & Analytics Canonical Owner | ✅ Approved | 2026-05-30 |
| Head of Specs Team | ✅ Approved | 2026-05-30 |

**Metrics Definitions & Analytics Canonical Owner sign-off notes:** All four metrics are deterministic aggregations against stored trade data. Formulas reference explicit strategy rules (§4.2.1 regime gate, §7 risk framework, §10 risk management summary). Threshold values are calibrated for a solo swing trader operating on a daily cadence with 10–30 trades per 90-day window. The approaching band (20% of threshold) provides actionable early warning without generating excessive amber states during normal operation.

**Head of Specs Team sign-off notes:** AC-01–04 from `stage4_backlog_slice.md#ST-07` are met: (AC-01) user-facing format (Option B — percentage deviation display, per `si02_fe_component_predesign.md §5`), rolling window (90 days), threshold bands (green/amber/red per §2.2), and warning state triggers defined; (AC-02) SI-05 integration points documented in §5; (AC-03) both owners signed; (AC-04) document filed at canonical path `docs/specs/metrics/si02_drift_score.md`.
