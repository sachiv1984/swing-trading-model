**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-31
**Backlog ref:** BLG-GOV-34
**Cycle:** 2026-05-30__release-v4.6 (ST-16 audit trigger)

---

# Arc 4 Data Density Trajectory Assessment

> This document is the formal trajectory assessment for Arc 4 data-gated features. It was triggered by the ST-16 closed trade count audit conducted during v4.6 sprint execution. It satisfies BLG-GOV-34 (Arc 4 data density risk trajectory assessment) and provides input to all future release planning cycles for Arc 4 features.

---

## 1. Purpose

Arc 4 features (PO-02, PO-04/PT-04) and the SI-02 EPIC-02 frontend gate each require minimum volumes of production data before they can deliver meaningful output. This assessment:

1. States what is known from the ST-16 production audit (2026-05-31).
2. Records confirmed usage rates and expectations from the Product Owner.
3. Projects gate-clearing dates under confirmed assumptions.
4. Records a Product Owner recommendation on whether to proceed, revise gates, or re-scope.

---

## 2. Features Under Assessment

| Feature | Backlog Item | Gate Condition | What the gate protects |
|---------|-------------|---------------|----------------------|
| SI-02 Frontend (BehaviouralDriftPanel) | EPIC-02, v4.6 S2-02 | ≥20 closed trades with linked `trade_plans` | Drift metrics are statistically meaningful |
| PT-04 Setup Quality Score | BLG-FEAT-25 | ≥20 closed trades (any; sub-gate) | Score computed from sufficient history |
| PT-04 Setup Quality Score (full gate) | BLG-FEAT-25 | ≥50 closed trades with linked `trade_plans` | Score reflects regime/ATR pattern matching |
| PO-02 Journal Pattern Recognition | BLG-SPEC-35 / roadmap | ≥6 months of AI journal entries | Cross-journal pattern detection has temporal depth |

---

## 3. Current Production Metrics (ST-16 Audit + PO Confirmation, 2026-05-31)

| Metric | Value | Source |
|--------|-------|--------|
| Total closed trades with P&L (`trade_history WHERE pnl IS NOT NULL`) | **6** | ST-16 production audit, 2026-05-31 |
| Closed trades with linked `trade_plans` (JOIN query) | **0** | ST-16 production audit, 2026-05-31 |
| AI journal entries total | **0** | PO confirmed — no closed trades have generated post-trade AI reflections |
| Trade plans created (all statuses) | Minimal — not in consistent use prior to v4.6 | PO confirmed |
| Open positions (active) | Estimated ~2–4 (consistent with 4–5 opens/month, ~1-month average hold) | PO estimate |

**Key finding:** 0 linked closed trades because the `trade_plans` feature was not in consistent use prior to v4.6. The PO has confirmed that from v4.6 onward, a trade plan will be created for every new position. All new closes from v4.6+ will therefore be linked, making the gate trajectory computable from the v4.6 ship date.

---

## 4. Rate Estimates (PO Confirmed)

### 4.1 Trade Creation and Close Rate

- **New positions per month:** ~4–5 (influenced by 10-day grace period logic — positions are entered actively within regime conditions)
- **Projected close rate per month:** ~4 (approximate, assuming most positions resolve within 4–8 weeks)
- **Basis:** PO estimate from observed trading pattern

### 4.2 Trade Plan Linkage Rate

- **Going forward:** 100% — PO commits to creating a trade plan for every new position from v4.6 onward
- **Historical (pre-v4.6):** Not consistently used — explains 0 closed trades with linked plans

### 4.3 AI Journal Entry Rate

- **Current total:** 0 entries (no closed trades have yet generated reflections)
- **Going forward:** Entries generated upon trade close via IT-01/IT-02. At ~4 closes/month, expect ~4 journal entries/month once trading resumes with plan linkage
- **First entry expected:** Next closed trade (~June 2026)

### 4.4 System Live Date for PO-02 Gate

- **First expected AI journal entry:** ~June 2026 (next closed trade post-v4.6)
- **Gate clock start:** June 2026 (6 months of consistent entries required)

---

## 5. Projected Gate-Clearing Dates

All projections are calculated from the audit baseline of 2026-05-31. Confirmed rate: ~4 closes/month with 100% linkage going forward.

### 5.1 SI-02 EPIC-02 Frontend Gate (≥20 closed trades with linked trade_plans)

**Current position:** 0 linked closed trades. Gap: 20 trades.

| Scenario | Monthly rate (closed + linked) | Projected gate-clearing date |
|----------|-------------------------------|------------------------------|
| Confirmed (PO rate) | 4 trades/month | **~2026-11 (November 2026, ~5 months)** |

**Implication:** SI-02 EPIC-02 frontend is ~5 months away at current rate. Plan for v4.9–v5.0 sprint window (release planning to check gate status).

### 5.2 PT-04 Sub-Gate (≥20 closed trades, any)

**Current position:** 6 closed trades. Gap: 14 more. (This gate does not require linked trade_plans.)

| Scenario | Monthly rate (closed trades, any) | Projected gate-clearing date |
|----------|----------------------------------|------------------------------|
| Confirmed (PO rate) | 4 trades/month | **~2026-09 (September 2026, ~3.5 months)** |

**Gate threshold:** Kept at 20 (PO confirmed — threshold is appropriate).

### 5.3 PT-04 Full Gate (≥50 closed trades with linked trade_plans)

**Current position:** 0 linked closed trades. Gap: 50 trades.

| Scenario | Monthly rate (closed + linked) | Projected gate-clearing date |
|----------|-------------------------------|------------------------------|
| Confirmed (PO rate) | 4 trades/month | **~2027-06 (June 2027, ~12.5 months)** |

**Implication:** PT-04 full gate is ~12.5 months away. Realistic target: v5.3–v5.5 range. Proceed on trajectory; review at v5.0 planning.

### 5.4 PO-02 Gate (≥6 months of AI journal entries)

**Current position:** 0 entries. First entry expected ~June 2026 (next closed trade).

| Scenario | Journal start date | Gate-clearing date |
|----------|--------------------|--------------------|
| Confirmed | ~2026-06 (first close post-v4.6) | **~2026-12 (December 2026, 6 months)** |

**Implication:** PO-02 is the nearest Arc 4 gate to clearing — December 2026 is achievable if journal entries accumulate consistently from the next closed trade. Plan PO-02 for v5.0–v5.1 sprint window.

---

## 6. Gate Condition Review

| Gate | Current condition | PO Decision |
|------|-----------------|-------------|
| SI-02 EPIC-02 frontend | ≥20 closed trades with linked `trade_plans` | **Keep at 20** — proceed on current trajectory (~Nov 2026) |
| PT-04 sub-gate | ≥20 closed trades (any) | **Keep at 20** — clears Sep 2026 at confirmed rate |
| PT-04 full gate | ≥50 closed trades with linked plans | **Keep at 50** — proceed on trajectory (~Jun 2027) |
| PO-02 journal gate | ≥6 months AI journal entries | **Proceed** — gate clears Dec 2026 if consistent use from next close |

---

## 7. Recommendation

**Option A — Proceed on current trajectory (no gate changes)**

All gate thresholds are retained at their documented values. No revisions required.

**Rationale:**
- The gate conditions are appropriate for the intended feature quality (statistically meaningful drift scores, pattern recognition depth).
- At 4 closes/month with 100% linkage going forward, all gates are on reasonable timelines: SI-02 EPIC-02 frontend ~Nov 2026, PT-04 sub-gate ~Sep 2026, PO-02 ~Dec 2026, PT-04 full ~Jun 2027.
- The historical 0-linkage situation is resolved by the v4.6 DS-07 migration and the PO commitment to 100% trade plan creation going forward. It does not reflect a design flaw; it reflects that the workflow was not yet adopted.
- No §13 implications — no gate revisions that would change the analytical scope of any feature.

**Actions for release planning:**
1. Add Arc 4 data density gate check to each release planning kickoff (PMO Lead — BLG-GOV-35 scope).
2. Check SI-02 EPIC-02 gate at v4.9 planning (expected gate clear ~Nov 2026).
3. Check PT-04 sub-gate at v4.8 planning (expected gate clear ~Sep 2026).
4. Check PO-02 gate at v5.0 planning (expected gate clear ~Dec 2026).
5. Update BLG-FEAT-25 note with confirmed trajectory at each applicable planning cycle.

---

## 8. Actions Required Before Next Release Planning

| Action | Owner | Due |
|--------|-------|-----|
| Maintain 100% trade plan creation for all new positions | Product Owner | Ongoing from v4.6 |
| Add Arc 4 data density checkpoint to release planning prompt | PMO Lead | v4.7 planning |
| Check SI-02 EPIC-02 gate (target ~Nov 2026) | PMO Lead | v4.9 planning |
| Check PT-04 sub-gate (target ~Sep 2026) | PMO Lead | v4.8 planning |
| Check PO-02 gate (target ~Dec 2026) | PMO Lead | v5.0 planning |

---

## 9. Sign-Off

| Role | Sign-off | Date |
|------|----------|------|
| Product Owner | Confirmed — trajectory assessed, gate conditions retained at 20/50/6-months, Option A (proceed on current trajectory) selected. | 2026-05-31 |
| Challenger | Confirmed — projections reviewed, rate assumptions reasonable (4 closes/month, 100% linkage from v4.6), recommendation appropriate. | 2026-05-31 |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-05-31 | Initial draft — engine-authored from ST-16 audit data. |
| 1.0 | 2026-05-31 | Finalised — PO metric inputs confirmed, projections computed, Option A selected, sign-off recorded. |
