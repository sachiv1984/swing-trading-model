**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Draft — awaiting Product Owner metric confirmation and sign-off
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
2. Identifies where the Product Owner must confirm or estimate actual usage metrics.
3. Projects gate-clearing dates under two scenarios.
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

## 3. Current Production Metrics (ST-16 Audit, 2026-05-31)

The following metrics were established by the ST-16 audit query run against the production database as part of v4.6 Sprint 1 execution.

| Metric | Value | Source |
|--------|-------|--------|
| Total closed trades with P&L (`trade_history WHERE pnl IS NOT NULL`) | **6** | ST-16 production audit, 2026-05-31 |
| Closed trades with linked `trade_plans` (JOIN query) | **0** | ST-16 production audit, 2026-05-31 |
| AI journal entries (PO-02 input) | [PO TO CONFIRM: total count of AI-generated journal summaries in production as of 2026-05-31] | Requires PO query or UI review |
| Trade plans created (all statuses) | [PO TO CONFIRM: total `trade_plans` row count in production] | Requires PO query |
| Open positions (active, not yet closed) | [PO TO CONFIRM: count of positions WHERE status = 'open'] | Requires PO query |

**Key finding:** The 0-linked-trade-plans figure is the most critical constraint. Even though 6 trades have been closed with P&L, none were linked to a `trade_plans` record. This may reflect:
- (a) the `trade_plans` feature not being in use yet, or
- (b) linkage between `positions` and `trade_plans` not being established before close.

[PO TO CONFIRM: Is the `trade_plans` feature actively being used in production? If yes, why are 0 closed trades linked? If no, when is consistent trade-plan creation expected to begin?]

---

## 4. Rate Estimates (Product Owner Input Required)

The projections in Section 5 depend on the following rates. The Product Owner must confirm or estimate each value based on their actual usage pattern.

### 4.1 Trade Creation Rate

[PO TO CONFIRM: How many new trade plans are created per month, on average? (e.g., "I typically plan 2–4 trades per month")]

**For projection purposes, two scenarios are modelled below:**
- Conservative: 1 trade plan created per month, 0.5 closed per month
- Optimistic: 3 trade plans created per month, 2 closed per month

### 4.2 Trade Plan Linkage Rate

[PO TO CONFIRM: Going forward, what proportion of new positions will have a linked `trade_plans` record? Is trade plan creation now a consistent step in the workflow, or still sporadic?]

**For projection purposes, both scenarios assume 100% linkage going forward** (i.e., the DS-07 migration and SI-02 backend, shipped in v4.6 Sprint 1, ensure all new entries link correctly). If linkage is less than 100%, all projected dates shift later proportionally.

### 4.3 AI Journal Entry Rate

[PO TO CONFIRM: How frequently are AI journal entries generated in production? (e.g., "once per closed trade", "weekly", "rarely used"). Total AI journal entries to date: see §3 above.]

**For projection purposes:**
- Conservative: 1 AI journal entry per 2 closed trades
- Optimistic: 1 AI journal entry per closed trade

### 4.4 System Live Date (For PO-02 6-Month Gate)

The PO-02 gate requires 6+ months of AI journal entries. The gate clock starts from the date the first AI journal entry was generated.

[PO TO CONFIRM: When was the first AI journal entry generated in production? (e.g., "around v3.3, approximately 2026-05-09")]

**For projection purposes, the conservative scenario assumes the journal feature began 2026-05-09 (v3.3 ship date, when IT-01/02/03 shipped). The optimistic scenario assumes first consistent use began 2026-05-30 (v4.5 ship, post-SI-02 spec).**

---

## 5. Projected Gate-Clearing Dates

All projections are calculated from the audit baseline of 2026-05-31.

### 5.1 SI-02 EPIC-02 Frontend Gate (≥20 closed trades with linked trade_plans)

**Current position:** 0 linked closed trades. Gap: 20 trades.

| Scenario | Monthly rate (closed + linked) | Projected gate-clearing date | Notes |
|----------|-------------------------------|------------------------------|-------|
| Conservative | 0.5 trades/month | ~2028-01 (approx. 20 months) | At 0.5 closed/month with 100% linkage going forward |
| Optimistic | 2 trades/month | ~2027-09 (approx. 10 months) | At 2 closed/month with 100% linkage going forward |

**Implication for v4.6:** The SI-02 EPIC-02 frontend (Sprint 2 conditional) will **not** be delivered in v4.6. The gate cannot clear within the current sprint cycle regardless of scenario. The EPIC-02 sprint is expected to be deferred, as already noted in the scope document.

### 5.2 PT-04 Sub-Gate (≥20 closed trades, any)

**Current position:** 6 closed trades (not linked). Gap: 14 trades. Note: this sub-gate does not require linked trade_plans.

| Scenario | Monthly rate (closed trades, any) | Projected gate-clearing date | Notes |
|----------|----------------------------------|------------------------------|-------|
| Conservative | 0.5 trades/month | ~2028-09 (approx. 28 months) | Very slow close rate |
| Optimistic | 2 trades/month | ~2027-05 (approx. 7 months) | Moderate close rate |

[PO TO CONFIRM: Is the sub-gate of 20 closed trades (regardless of plan linkage) a meaningful threshold, or should it be revised downward given the low trading frequency?]

### 5.3 PT-04 Full Gate (≥50 closed trades with linked trade_plans)

**Current position:** 0 linked closed trades. Gap: 50 trades.

| Scenario | Monthly rate (closed + linked) | Projected gate-clearing date | Notes |
|----------|-------------------------------|------------------------------|-------|
| Conservative | 0.5 trades/month | ~2030-09 (approx. 52 months) | Gate unlikely to clear within product lifetime at this rate |
| Optimistic | 2 trades/month | ~2028-11 (approx. 30 months) | Still a multi-year horizon |

**Implication:** The 50-trade gate for PT-04 full capability is extremely unlikely to clear within 4–6 cycles under any realistic scenario. This is a structural gap between gate design and actual usage frequency.

### 5.4 PO-02 Gate (≥6 months of AI journal entries)

**Current position:** [PO TO CONFIRM AI journal entry count — see §3]. The gate is temporal (6 months of entries) not volumetric, but requires consistent journal usage throughout that period.

| Scenario | Journal start date (assumed) | Gate-clearing date | Notes |
|----------|-----------------------------|--------------------|-------|
| Conservative | 2026-05-30 (consistent use starts now) | ~2026-11-30 (6 months) | If journals are generated consistently from today |
| Optimistic | 2026-05-09 (IT-01/02/03 ship, v3.3) | ~2026-11-09 (6 months from v3.3) | If journal feature has been in active use since v3.3 |

**Implication:** PO-02 is the most achievable Arc 4 gate. If the AI journal feature has been in consistent use since v3.3 (2026-05-09), the 6-month gate clears approximately 2026-11-09 — within 5–6 cycles from now. If journal use only began in earnest recently, the gate clears approximately 2026-11-30. Either way, PO-02 is on a 6-month horizon and should be planned for v4.9–v5.1.

[PO TO CONFIRM: Has the AI journal feature (IT-01 Post-Trade AI Reflection) been used consistently since v3.3 ship? Or is it used sporadically? Consistent use is required for the 6-month gate to hold.]

---

## 6. Gate Condition Review

Given the projections above, the following gate conditions warrant Product Owner review:

| Gate | Current condition | Problem | Options |
|------|-----------------|---------|---------|
| SI-02 EPIC-02 frontend | ≥20 closed trades with linked trade_plans | Conservative: ~20 months away. Feature meaningfulness at low counts is real concern. | (a) Keep gate at 20 — defer EPIC-02 until gate clears. (b) Lower gate to ≥10 with explicit disclaimer in UI. (c) Ship frontend with a "not enough data" placeholder state that activates at gate. |
| PT-04 sub-gate | ≥20 closed trades (any) | Conservative: ~28 months. Optimistic: ~7 months. | (a) Keep gate. (b) Lower to ≥10 closed trades. (c) Ship a "seeding mode" that shows projected score with a data-sparse warning. |
| PT-04 full gate | ≥50 closed trades with linked plans | 30–52 months away — effectively a multi-year deferral. | (a) Retain as long-term aspirational gate. (b) Redesign PT-04 to function with ≥10 linked trades using a Bayesian-adjusted score. (c) Defer PT-04 to Arc 6 or beyond and remove from near-term roadmap. |
| PO-02 journal gate | ≥6 months AI journal entries | Achievable 2026-11 if consistent use confirmed. | (a) Proceed on current trajectory — plan PO-02 for v4.9–v5.1. (b) Add a formal journal-entry count checkpoint to each release planning cycle. |

---

## 7. Recommendation

Based on the ST-16 audit data and the projections above, the Product Owner recommendation is:

**[PO TO COMPLETE: Select one or more of the following and add rationale]**

**Option A — Proceed on current trajectory (no gate changes)**
> Rationale: [PO to complete]. Expected: PO-02 planned v4.9–v5.1; PT-04 and SI-02 frontend deferred indefinitely pending gate.

**Option B — Revise gate conditions for PT-04 and SI-02 EPIC-02**
> Rationale: [PO to complete]. Proposed revised gates: [PO to specify]. §13 implications of lower-count scoring to be assessed before implementation.

**Option C — Re-scope / defer PT-04 full gate features**
> Rationale: [PO to complete]. PT-04 full gate (50+ linked trades) is unlikely to clear within the product's current user base. Defer PT-04 full capability to Arc 6+; retain PT-04 sub-gate (20 closed trades) as the near-term gate for a reduced-scope score. PO-02 proceeds on current trajectory.

**Engine Recommendation (for PO consideration):**
The engine recommends a hybrid of Options B and C:
- For **SI-02 EPIC-02 frontend**: ship with a graceful degradation state (empty panel + "Drift analysis requires 20 closed trades" message). Lower gate to ≥10 linked trades for initial panel activation, with a statistical disclaimer. This avoids a multi-year hold on a feature whose backend is already shipped.
- For **PT-04 full gate (50 trades)**: re-scope as a long-term aspirational gate. Advance a reduced PT-04 ("setup quality heuristic") with the ≥10 closed trades threshold.
- For **PO-02**: proceed on current trajectory. Add a formal journal-entry count checkpoint to each release planning kickoff (BLG-GOV-35 scope).

---

## 8. Actions Required Before Next Release Planning

| Action | Owner | Due |
|--------|-------|-----|
| Confirm AI journal entry count and start date (§3, §4.4) | Product Owner | Before v4.7 planning |
| Confirm trade plan creation and close rate per month (§4.1) | Product Owner | Before v4.7 planning |
| Confirm trade plan linkage workflow compliance going forward (§4.2) | Product Owner | Before v4.7 planning |
| Record gate revision decisions (if any) in this document | Product Owner + Challenger | Before v4.7 planning |
| Update BLG-FEAT-25 gate condition if PT-04 full gate is revised | PMO Lead | After PO decision |
| Update SI-02 EPIC-02 gate condition in scope artefact if revised | Head of Specs Team | After PO decision |
| Add Arc 4 data density checkpoint to release planning prompt (BLG-GOV-35) | PMO Lead | v4.7 planning |

---

## 9. Sign-Off

| Role | Sign-off | Date |
|------|----------|------|
| Product Owner | [PENDING — PO must confirm metric inputs (§3–4) and record decision (§7) before signing] | |
| Challenger | [PENDING — Challenger review of projections and gate revision options] | |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-05-31 | Initial draft — engine-authored from ST-16 audit data (6 closed trades, 0 linked). Sections 3–4 contain PO confirmation markers. Sections 5–7 contain engine projections and options. Awaiting PO metric confirmation and decision sign-off. |
