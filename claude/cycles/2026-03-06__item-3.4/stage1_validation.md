**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-06

---

# Stage 1 — Roadmap Re-Validation

**Cycle:** 2026-03-06__item-3.4
**Date:** 2026-03-06
**Authorities:** Product Owner + Strategy Rules & System Intent Owner

---

## Context Since Prior Cycle (2026-03-04__item-3.4)

The following material changes have occurred since 2026-03-04:

1. **v1.8 shipped (2026-03-06)** — all 4 EPICs complete and verified. Risk Dashboard live.
2. **Item 3.4 Risk Dashboard: COMPLETE** — the triggering event for this cycle.
3. **v1.8 deviation backlog created** — BLG-RD-01 through BLG-RD-11 filed; all target v1.9.
4. **TEST-GAP-EPIC-01 filed** — 17/27 Risk Dashboard scenarios not executable; QA infrastructure gap identified.
5. **BLG-NEW-01, 02, 03, 05, 07, 08 COMPLETE** — all delivered in v1.8 sprint.
6. **BLG-NEW-04 still open** — AI-Assisted Workflow Governance Policy not yet delivered.
7. **PoG POG-20260304-01 (item 4.3) still valid** — `strategy_rules.md` remains at v1.3; no increment since PoG was issued.
8. **v1.9 path is unblocked** — capacity freed, pre-alignment may begin.

---

## Active Initiatives Reviewed

---

### 3.4 — Risk Dashboard (v1.8)

**Classification:** ✅ COMPLETE — Shipped 2026-03-06

This item is complete and removed from active initiative tracking. All residual work (deviations, test gaps) is captured in the backlog targeting v1.9. No further re-validation required.

---

### 5.1 — Structured Trade Reflection Template (v1.9)

**Classification:** 🔥 Must continue

**What has changed:**
- No change to strategic fit. BLG-FEAT-08 (pre-work gate) is still on track.
- v1.8 ship frees capacity for v1.9 pre-alignment.
- No AI involvement — fully deterministic, built on existing journal system.

**Would we still choose this if starting today?** Yes. Discipline reinforcement through structured reflection is high-value and low-risk. All inputs available from existing trade records.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §3 human-in-the-loop — supports human decision-making; does not automate, predict, or adapt the strategy. No boundary proximity.

---

### BLG-FEAT-08 — Basic Compliance Metrics (v1.9 pre-work gate)

**Classification:** 🔥 Must continue

**What has changed:**
- LL-05 capacity check note from v1.7 planning remains active: Metrics Definitions & Analytics Owner availability must be confirmed before v1.9 pre-alignment opens.
- No other changes.

**Would we still choose this?** Yes. Gate-keeper for 5.1. ~1 day effort. Without this, 5.1 cannot proceed.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §10 Risk management summary — compliance metrics describe adherence to existing strategy rules. No new strategy behaviour introduced.

---

### 5.2 — Cohort Analysis (v1.9)

**Classification:** 🔥 Must continue

**What has changed:**
- Trade history has accumulated through v1.8 cycle. Cohort analysis becomes more valuable over time.
- No data dependency changes.

**Would we still choose this?** Yes. High-insight, low-complexity analytics from existing data.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — read-only analytics from existing trade data. No contact with strategy boundaries.

---

### 5.3 — Dashboard Homepage / Session Summary (v1.9)

**Classification:** 🔥 Must continue

**What has changed:**
- v1.8 adds Risk Dashboard data (heat, grace, deviations) to the daily workflow. Homepage value has increased.
- All required endpoints live: GET /portfolio, GET /positions, GET /signals.

**Would we still choose this?** Yes. Product completion feature. All data available.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — pure composite display from existing deterministic endpoints.

---

### BLG-RD Deviation Bundle (v1.9 — new scope)

**Classification:** 🔥 Must continue (at P2–P3 priority per individual items)

**What has changed:**
- NEW since prior cycle: 11 Risk Dashboard deviation items (BLG-RD-01 through BLG-RD-11) filed from v1.8 delivery verification.
- All target v1.9. All are display-layer or backend currency conversion corrections.
- P2 items: BLG-RD-01, 03, 04, 08, 10, 11 — highest priority deviations.
- P3 items: BLG-RD-02, 05, 06, 07, 09 — cosmetic/minor.

**Would we still choose this?** Yes. Deviations from canonical spec must be resolved. P2 items affect risk visibility accuracy.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — correctness and display compliance. No contact with strategy boundaries.

---

### TEST-GAP-EPIC-01 — Risk Dashboard Scenario Execution Infrastructure (v1.9)

**Classification:** 🔥 Must continue

**What has changed:**
- NEW since prior cycle: 17/27 Risk Dashboard acceptance scenarios are not executable without seeded test data infrastructure.
- Target v1.9.

**Would we still choose this?** Yes. Quality gate for Risk Dashboard completeness.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — QA infrastructure. No contact with strategy boundaries.

---

### 3.5 — Alerts & Notifications (v2.0 — deferred)

**Classification:** ⚠ Re-evaluate (confirmed defer)

**What has changed:**
- No change since DL-003. Third gate (QA planning session for notification delivery) remains uncleared.
- Auto-advance trigger from DL-003 remains active.

**Would we still choose this?** Yes when gate is cleared. Status unchanged.

**Resolution:** Confirm ⏸ defer. Gate condition unchanged.

**Strategy Proximity Score: 3**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §3, §8.1–8.3 — notifications are advisory only; all actions remain human-initiated. Score 3 because market regime change notification touches §8.2 but remains read-only.

---

### 4.1b — Tax-Year P&L Statement (v2.0)

**Classification:** 🔥 Must continue

**What has changed:**
- No change. Canonical spec pre-work required before implementation.
- P&L labelling pre-work (merged from BLG-NEW-06) is part of scope.

**Would we still choose this?** Yes. High-value financial record requirement.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — financial reporting, no contact with strategy boundaries.

---

### 4.1c — Server-Side PDF Report (v2.0)

**Classification:** 🔥 Must continue

**What has changed:**
- No change. Browser-print approach remains brittle.

**Would we still choose this?** Yes. Medium value, clean technical solution. Lowest-value active item; displacement candidate if a future roadmap Add requires a stop.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — pure infrastructure replacement.

---

### 4.3 — Signal Exposure Enhancement (v2.0 — active planning)

**Classification:** 🔥 Must continue

**What has changed:**
- No change since DL-004. PoG POG-20260304-01 remains valid (`strategy_rules.md` still at v1.3).
- Item is in active v2.0 planning scope.

**PoG validity check (STEP 5.0.A):** POG-20260304-01 references `strategy_rules.md v1.3`. Current version is v1.3 — **PoG is valid**. No re-issuance required.

**Would we still choose this?** Yes. Gate cleared, backend already supports.

**Strategy Proximity Score: 4**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §13.2 — scope boundary enforced by PoG POG-20260304-01. Score 4 retained; scope containment remains critical.

---

### 4.2 — Watchlists & Screening (Priority 2)

**Classification:** 🔥 Must continue (at Priority 2 — do not pull forward)

**What has changed:** None. Still at Priority 2.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — monitoring tickers for entry signals using existing strategy logic.

---

### Chart Interactivity Enhancements (Priority 2)

**Classification:** 🔥 Must continue (at Priority 2)

**What has changed:** None. Scope boundary (no new technical indicators) unchanged.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §13.2 noted — scope boundary enforced in item definition.

---

## Summary Table

| Initiative | Classification | SPS | Action required |
|-----------|----------------|-----|-----------------|
| 3.4 Risk Dashboard | ✅ COMPLETE | — | None — item retired |
| 5.1 Trade Reflection | 🔥 Must continue | 2 | None — v1.9 pre-alignment next |
| BLG-FEAT-08 Compliance Metrics | 🔥 Must continue | 2 | Confirm Metrics owner availability at v1.9 pre-alignment |
| 5.2 Cohort Analysis | 🔥 Must continue | 2 | None |
| 5.3 Dashboard Homepage | 🔥 Must continue | 1 | None |
| BLG-RD Deviation Bundle | 🔥 Must continue | 1 | v1.9 backlog — release planning determines slice |
| TEST-GAP-EPIC-01 | 🔥 Must continue | 1 | v1.9 backlog — QA infrastructure required |
| 3.5 Alerts & Notifications | ⚠ Re-evaluate | 3 | Confirm ⏸ defer — QA gate still open |
| 4.1b Tax-Year P&L | 🔥 Must continue | 1 | Canonical spec required before implementation |
| 4.1c Server-Side PDF | 🔥 Must continue | 1 | Lowest-value item; displacement candidate |
| 4.3 Signal Exposure | 🔥 Must continue | 4 | PoG valid; v2.0 active planning |
| 4.2 Watchlists | 🔥 Must continue | 2 | Hold at Priority 2 |
| Chart Interactivity | 🔥 Must continue | 2 | Hold at Priority 2 |

---

## Cycle Proximity Score (CPS)

| Initiative | SPS |
|-----------|-----|
| 5.1 Trade Reflection | 2 |
| BLG-FEAT-08 Compliance Metrics | 2 |
| 5.2 Cohort Analysis | 2 |
| 5.3 Dashboard Homepage | 1 |
| BLG-RD Deviation Bundle | 1 |
| TEST-GAP-EPIC-01 | 1 |
| 3.5 Alerts & Notifications | 3 |
| 4.1b Tax-Year P&L | 1 |
| 4.1c Server-Side PDF | 1 |
| 4.3 Signal Exposure | 4 |
| 4.2 Watchlists | 2 |
| Chart Interactivity | 2 |
| **CPS (mean, 12 items)** | **1.8** |

**Prior cycle CPS:** 2.0 (from cycle 2026-03-04__item-3.4, 11 items including 3.4)

**Trend:** −0.2 (slight decrease — expected, as item 3.4 SPS=2 is removed and lower-SPS maintenance items BLG-RD/TEST-GAP added)

**Drift alert rule:** Change is −0.2, well below +0.5 threshold. **No Strategy Drift Alert required.**

**Facilitator note:** CPS=1.8 reflects a maintenance-heavy v1.9 (Risk Dashboard deviation fixes) balanced with moderate-SPS user value features (5.1, 5.2, 5.3). The SPS=4 on item 4.3 requires the Challenger to lead with a §13-referenced counter-argument in any STEP 5 debate involving 4.3 (not applicable this cycle — 4.3 is not a STEP 5 candidate). No Score-5 items present. No Strategy Drift Alert required.
