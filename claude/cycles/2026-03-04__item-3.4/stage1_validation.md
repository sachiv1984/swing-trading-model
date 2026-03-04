**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-04

---

# Stage 1 — Roadmap Re-Validation

**Cycle:** 2026-03-04__item-3.4
**Date:** 2026-03-04
**Authorities:** Product Owner + Strategy Rules & System Intent Owner

---

## Context Since Prior Cycle (2026-03-01__item-3.2)

The following material changes have occurred:

1. **v1.7 shipped (2026-03-03)** — all 6 EPICs complete and verified.
2. **v1.8 pre-alignment gate CLEARED** — `metrics_definitions.md` v1.6.0 now contains the Portfolio Heat formula and display thresholds (EPIC-03).
3. **v2.0 pre-alignment gates CLEARED** — structured logging standards (EPIC-04) and API versioning decision record (EPIC-05) both complete.
4. **§13 boundary review COMPLETE** — SRB decision record filed (`docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md`):
   - Signal Params: **COMPLIANT** (top_n and lookback_days may be exposed as user-facing controls)
   - AI Journal Summarisation: **CONDITIONALLY COMPLIANT** (non-determinism must be disclosed; requires formal §13 amendment before implementation)
   - New Indicators: **COMPLIANT if canonical** (strategy_rules.md must be updated before implementation)
5. **Spec debt resolved** — analytics_endpoints.md v1.9.0, portfolio_endpoints.md v1.9.0, trade_endpoints.md v1.9.0 — all OBS items cleared.
6. **First idea intake window closed** — IW-20260304-01: 44 submissions from 22 agents available for STEP 4.

---

## Active Initiatives Reviewed

---

### 3.4 — Risk Dashboard (v1.8)

**Classification:** 🔥 Must continue

**What has changed:**
- Pre-requisite gate (Portfolio Heat formula) is now CLEARED — `metrics_definitions.md` v1.6.0.
- v1.6.1 already shipped Current Drawdown Widget and Grace Period Indicator. Risk Dashboard scope must reconcile these in pre-alignment to avoid duplication.
- All endpoint data needed (GET /portfolio, GET /positions, GET /analytics/metrics) is live and stable.

**Would we still choose this if starting today?** Yes. Risk visibility is a core daily use case. The heat gauge and position-level risk table address a real daily workflow need. The pre-requisite gate clearance removes the only blocker.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §10 Risk management summary — these metrics (heat, drawdown, grace period) already exist in the strategy framework; this initiative surfaces them visually. No new strategy-relevant parameters introduced. No boundary proximity.

---

### 5.1 — Structured Trade Reflection Template (v1.9)

**Classification:** 🔥 Must continue

**What has changed:**
- No change to strategic fit. BLG-FEAT-08 (pre-work gate) is still on track.
- No AI involvement confirmed — fully deterministic, built on existing journal system.
- Still distinctly scoped from AI Journal Summarisation (which requires §13 amendment).

**Would we still choose this?** Yes. Discipline reinforcement through structured reflection is high-value and low-risk. The existing journal system (v1.4) and trade record provide all inputs.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §3 human-in-the-loop — the reflection template supports human decision-making; it does not automate, predict, or adapt the strategy. No boundary proximity.

---

### BLG-FEAT-08 — Basic Compliance Metrics (v1.9 pre-work gate)

**Classification:** 🔥 Must continue

**What has changed:**
- LL-05 note from v1.7 release planning remains active: Metrics Definitions & Analytics Owner must be confirmed available before v1.9 pre-alignment opens. This is a capacity check, not a blocker.
- Definitions must enter `metrics_definitions.md` before implementation begins.

**Would we still choose this?** Yes. This is the gate-keeper for 5.1. Low effort (~1 day). Without this, 5.1 cannot proceed.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §10 Risk management summary — compliance metrics (journal rate, stop-based exit rate, position size %) describe adherence to existing strategy rules. No new strategy behavior introduced.

---

### 5.2 — Cohort Analysis (v1.9)

**Classification:** 🔥 Must continue

**What has changed:**
- Trade history continues to accumulate; cohort analysis becomes more valuable over time.
- Deliverable from existing trade data. No new backend data dependencies.

**Would we still choose this?** Yes. Clean, high-insight feature that gets more valuable as trade history grows.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — read-only analytics from existing trade data. No contact with strategy boundaries.

---

### 5.3 — Dashboard Homepage / Session Summary (v1.9)

**Classification:** 🔥 Must continue

**What has changed:**
- v1.6.1 shipped 6 new user-facing features, enriching the data available on a homepage (grace period, drawdown, best/worst trades).
- All required endpoints already live: GET /portfolio, GET /positions, GET /signals.
- Value increased since prior cycle due to richer data.

**Would we still choose this?** Yes. Makes the product feel complete for daily use. All data available from existing endpoints.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — pure composite display from existing deterministic endpoints. No contact with strategy boundaries.

---

### 3.5 — Alerts & Notifications (v2.0)

**Classification:** ⚠ Re-evaluate

**What has changed:**
- Two of three hard gates are now CLEARED: structured logging (EPIC-04 ✅) and API versioning decision (EPIC-05 ✅).
- **Third gate — QA planning session for notification delivery — NOT YET COMPLETE.** The QA planning session was required before v2.0 pre-alignment opens. No evidence this session has been conducted.
- Workforce estimate (4–5 days) remains unchanged. Email/SMS delivery testing surface remains high.

**Would we still choose this?** The feature is strategically sound and the two technical pre-requisites are now met. However, the QA planning session gate remains open. This item stays ⚠ Re-evaluate until that gate is closed.

**Resolution required by STEP 8:** Re-commit 🔥 if the QA planning session gate can be documented or closed in this cycle; defer ⏸ if not.

**Strategy Proximity Score: 3**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §3 human-in-the-loop, §8.1–8.3 exit conditions — notifications are informational only (stop approach, grace period ending, regime change) and do not automate any exit or decision. All actions remain human-initiated. Standard feature; no boundary proximity. Score 3 because market regime change notification touches §8.2 regime change logic, but remains read-only and advisory.

---

### 4.1b — Tax-Year P&L Statement (v2.0)

**Classification:** 🔥 Must continue

**What has changed:**
- No change to strategic fit. Financial record requirement unchanged.
- Requires its own canonical spec and dedicated endpoint — this is a spec pre-work task.

**Would we still choose this?** Yes. High-value formal financial record for tax purposes. Canonical spec needed first.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — financial reporting, no contact with strategy boundaries.

---

### 4.1c — Server-Side PDF Report (v2.0)

**Classification:** 🔥 Must continue

**What has changed:**
- No change. Analytics page exists; browser-print approach remains brittle.

**Would we still choose this?** Yes. Medium value, clean technical solution.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — pure infrastructure replacement. No contact with strategy boundaries.

---

### 4.3 — Signal Exposure Enhancement (v2.0 — gated)

**Classification:** ⚠ Re-evaluate → Gate cleared; reclassification to 🔥 pending STEP 5 debate

**What has changed:**
- **§13 gate CLEARED.** SRB decision (EPIC-02, v1.7) explicitly confirmed Signal Params COMPLIANT: `top_n` and `lookback_days` may be exposed as user-facing controls. Decision record: `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md`.
- The scope boundary remains hard: ONLY these two parameters. Any additional parameter constitutes a §13 configurable strategy builder violation.
- Backend already supports these parameters — this is primarily a frontend and spec task.

**Would we still choose this?** Gate is cleared. The item advances to STEP 5 debate for formal reclassification.

**PoG status:** A Proof of Gate document is required before this item advances past debate (per roadmap_prompt §5.3). The SRB decision record exists. A Class 8 PoG document must be issued in STEP 5.3 citing the SRB decision record version.

**Strategy Proximity Score: 4**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §13.2 — "a multi-strategy or configurable strategy platform" is explicitly excluded. This item directly approaches that boundary. The SRB cleared the gate for exactly `top_n` and `lookback_days` — no other parameters may be included. Score 4 because the boundary is nearby and scope containment is critical. Any scope expansion post-SRB would be a §13 violation.

---

### 4.2 — Watchlists & Screening (Priority 2)

**Classification:** 🔥 Must continue (at Priority 2 — do not pull forward)

**What has changed:**
- No change to strategic fit or priority.
- Requires new data model tables and new endpoints. Significant scope.

**Would we still choose this?** Yes, at current priority. Not pulling forward.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — monitoring tickers for entry signals using existing strategy signal logic. No new strategy parameters. Standard feature.

---

### Chart Interactivity Enhancements (Priority 2)

**Classification:** 🔥 Must continue (at Priority 2)

**What has changed:**
- No change. The scope boundary (no new technical indicators) remains clear and enforced.

**Would we still choose this?** Yes, at current priority. Low-Medium effort, UX improvement.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §13.2 noted — scope boundary "no new technical indicators" explicitly enforces this constraint. Score 2 because the boundary is noted and enforced in scope definition.

---

## Summary Table

| Initiative | Classification | SPS | Action required |
|-----------|----------------|-----|-----------------|
| 3.4 Risk Dashboard | 🔥 Must continue | 2 | None — pre-alignment gate cleared |
| 5.1 Trade Reflection | 🔥 Must continue | 2 | None |
| BLG-FEAT-08 Compliance Metrics | 🔥 Must continue | 2 | Confirm Metrics owner availability at v1.9 pre-alignment |
| 5.2 Cohort Analysis | 🔥 Must continue | 2 | None |
| 5.3 Dashboard Homepage | 🔥 Must continue | 1 | None |
| 3.5 Alerts & Notifications | ⚠ Re-evaluate | 3 | QA planning session gate must close before 🔥 or ⏸ by STEP 8 |
| 4.1b Tax-Year P&L | 🔥 Must continue | 1 | Canonical spec required before implementation |
| 4.1c Server-Side PDF | 🔥 Must continue | 1 | None |
| 4.3 Signal Exposure | ⚠ Re-evaluate → debate | 4 | §13 gate cleared (SRB v1.7); PoG required at STEP 5.3; advance to STEP 5 debate |
| 4.2 Watchlists | 🔥 Must continue | 2 | Hold at Priority 2 |
| Chart Interactivity | 🔥 Must continue | 2 | Hold at Priority 2 |

---

## Cycle Proximity Score (CPS)

| Initiative | SPS |
|-----------|-----|
| 3.4 Risk Dashboard | 2 |
| 5.1 Trade Reflection | 2 |
| BLG-FEAT-08 Compliance Metrics | 2 |
| 5.2 Cohort Analysis | 2 |
| 5.3 Dashboard Homepage | 1 |
| 3.5 Alerts & Notifications | 3 |
| 4.1b Tax-Year P&L | 1 |
| 4.1c Server-Side PDF | 1 |
| 4.3 Signal Exposure | 4 |
| 4.2 Watchlists | 2 |
| Chart Interactivity | 2 |
| **CPS (mean)** | **2.0** |

**Prior cycle CPS:** No prior baseline — prior engine version (roadmap_prompt.md < v1.9) did not record CPS.

**Trend:** No prior baseline. Drift alert rule not applicable.

**Facilitator note:** No Strategy Drift Alert required. CPS = 2.0 is in the expected range for a system with one boundary-adjacent item (4.3 SPS=4) balanced against primarily execution-heavy features. The SPS=4 on item 4.3 requires the Challenger to lead with a §13-referenced counter-argument in STEP 5.1.
