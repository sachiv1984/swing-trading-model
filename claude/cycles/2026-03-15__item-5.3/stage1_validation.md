**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-15

---

# Stage 1 — Roadmap Re-Validation

**Cycle:** 2026-03-15__item-5.3
**Date:** 2026-03-15
**Authorities:** Product Owner + Strategy Rules & System Intent Owner

---

## Context Since Prior Cycle (2026-03-06__item-3.4)

The following material changes have occurred since 2026-03-06:

1. **v1.9 Sprint 1 shipped (2026-03-09)** — Risk Dashboard deviation bundle (EPIC-04), Playwright test infrastructure + Service Layer Test Coverage Standard (EPIC-05 partial), full documentation hygiene backlog (EPIC-06). 13 ST items complete.
2. **v1.9 Sprint 2 shipped (2026-03-13)** — all 6 Sprint 2 items complete: ST-01 (BLG-FEAT-08 Compliance Metrics), ST-02 (5.1 Trade Reflection), ST-03 (5.2 Cohort Analysis), ST-04 (R-Multiple Distribution), ST-05 (5.3 Dashboard Homepage), ST-12 (Canonical Test Scenario Library Phase 2). Verified via sprint_close_sprint2.md.
3. **Items completing this cycle:** 5.1, 5.2, 5.3, BLG-FEAT-08 — all shipped and verified.
4. **BLG-RD Deviation Bundle:** COMPLETE — shipped Sprint 1.
5. **TEST-GAP-EPIC-01:** COMPLETE — shipped Sprint 1.
6. **BLG-OPS-01 raised (2026-03-13):** Structural QA gap identified post-merge — no development environment exists. All QA currently runs against production. Raised as P1 backlog item.
7. **PoG POG-20260304-01 (item 4.3):** Still valid — strategy_rules.md remains at v1.3.
8. **v2.0 path is unblocked for planning:** v1.9 fully closed; capacity freed.
9. **AUD-2026-03-13 governance audit applied** (2026-03-15): AUD-003 (idea intake integration), AUD-005, AUD-006, AUD-017 remain open (deferred).

---

## Active Initiatives Reviewed

---

### 5.1 — Structured Trade Reflection Template (v1.9)

**Classification:** ✅ COMPLETE — Shipped 2026-03-13 (v1.9 Sprint 2, ST-02)

Delivered as EPIC-01 in Sprint 2. Pre-work gate BLG-FEAT-08 shipped in the same sprint (ST-01). Removed from active initiative tracking.

---

### BLG-FEAT-08 — Basic Compliance Metrics (v1.9)

**Classification:** ✅ COMPLETE — Shipped 2026-03-13 (v1.9 Sprint 2, ST-01)

Definitions canonicalised in metrics_definitions.md. Metrics live in production. Gate-keeper function for 5.1 satisfied. Removed from active initiative tracking.

---

### 5.2 — Cohort Analysis (v1.9)

**Classification:** ✅ COMPLETE — Shipped 2026-03-13 (v1.9 Sprint 2, ST-03)

Delivered as EPIC-02/ST-03. Backend endpoint live; frontend cohort analysis tab/panel implemented. Note: BLG-TECH-06 filed (client-side computation residue in CohortAnalysis.js) — tracked separately in backlog at P2 for v1.10.

---

### 5.3 — Dashboard Homepage / Session Summary (v1.9)

**Classification:** ✅ COMPLETE — Shipped 2026-03-13 (v1.9 Sprint 2, ST-05)
**[TRIGGERING EVENT FOR THIS CYCLE]**

All endpoints live (GET /portfolio, GET /positions, GET /signals). Homepage composite view delivered. Full product home page functionality in production.

---

### 3.5 — Alerts & Notifications (v2.0 — deferred)

**Classification:** ⚠ Re-evaluate (confirmed defer)

**What has changed:**
- No change since DL-003. Third gate (QA planning session for notification delivery) remains uncleared.
- Auto-advance trigger from DL-003 remains active.
- With v1.9 complete, v2.0 planning window is opening — however, this gate must clear before pre-alignment opens.

**Would we still choose this?** Yes when gate is cleared. High user value; async delivery complexity requires QA design first.

**Strategy Proximity Score: 3**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §3, §8.1–8.3 — notifications are advisory only; all actions remain human-initiated. Score 3 because market regime change notification touches §8.2 but remains read-only.

**Resolution:** Confirm ⏸ defer. Gate condition unchanged.

---

### 4.1b — Tax-Year P&L Statement (v2.0)

**Classification:** 🔥 Must continue

**What has changed:**
- No change. v1.9 shipped; no pre-work dependency on v1.9 items.
- Canonical spec for P&L Statement still required before implementation can begin.
- BLG-NEW-06 P&L labelling pre-work scope remains merged into 4.1b.

**Would we still choose this?** Yes. High-value financial record; the only formal per-tax-year output in the product.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — financial reporting. No contact with strategy execution boundaries.

---

### 4.1c — Server-Side PDF Report (v2.0)

**Classification:** ⚠ Re-evaluate (Kill candidate)

**What has changed:**
- No change since prior cycle. Still the lowest-value active roadmap item.
- BLG-OPS-01 (Dev Environment) has been raised as P1 — structural QA gap requiring infrastructure investment. This creates a displacement demand.
- With v1.9 closed, v2.0 capacity is now visible. BLG-OPS-01 must enter v2.0 planning; 4.1c is the natural Kill to achieve net-zero.

**Would we still choose this over BLG-OPS-01?** No. Browser-print PDF is a UX inconvenience; lack of a development environment is a structural governance and quality failure. BLG-OPS-01 is categorically higher priority.

**Resolution:** Propose ❌ Kill in STEP 5 debate. Documented as standing displacement candidate since DL-005 (2026-03-04).

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — pure infrastructure replacement. No strategic contact.

---

### 4.3 — Signal Exposure Enhancement (v2.0 — active planning)

**Classification:** 🔥 Must continue

**What has changed:**
- No change since DL-004. PoG POG-20260304-01 remains valid (strategy_rules.md still at v1.3).
- v2.0 planning window opening — 4.3 is a confirmed active v2.0 item.

**PoG validity check (STEP 5.0.A):** POG-20260304-01 references strategy_rules.md v1.3. Current version: v1.3. **PoG is valid.** No re-issuance required.

**Would we still choose this?** Yes. Frontend-only, backend already supports. Low effort, gate cleared.

**Strategy Proximity Score: 4**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §13.2 — scope boundary enforced by PoG POG-20260304-01. Score 4 retained; scope containment remains critical. Challenger must lead with §13-referenced counter-argument if any expansion of 4.3 scope is proposed.

---

### 4.2 — Watchlists & Screening (Priority 2)

**Classification:** 🔥 Must continue (at Priority 2 — do not pull forward)

**What has changed:** None. Hold at Priority 2 until v2.0 items clear.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — monitoring tickers for entry signals using existing strategy logic.

---

### Chart Interactivity Enhancements (Priority 2)

**Classification:** 🔥 Must continue (at Priority 2)

**What has changed:** None. Scope boundary (no new technical indicators without §13 review) unchanged.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §13.2 noted — scope boundary enforced in item definition.

---

### BLG-OPS-01 — Dev Environment (new — Add candidate)

**Classification:** ➕ Add candidate (roadmap-level elevation from backlog)

**Context:**
Raised 2026-03-13 during v1.9 Sprint 2 post-merge QA. No development environment exists — all QA runs against production. This is a structural governance gap: Director of Quality sign-off requires testing a live application, but the only live application is production. Post-merge bug discovery (as occurred in Sprint 2) is the only available feedback loop.

**Would we choose this as a roadmap item?** Yes. This is not a nice-to-have. The quality gate process is structurally broken without it. P1 priority in backlog confirms urgency.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — operations/infrastructure. No contact with strategy boundaries.

**Note:** BLG-OPS-01 elevation to roadmap requires killing 4.1c to satisfy net-zero. See STEP 5 debate.

---

## Summary Table

| Initiative | Classification | SPS | Action |
|-----------|----------------|-----|--------|
| 5.1 Trade Reflection | ✅ COMPLETE | — | Remove from active |
| BLG-FEAT-08 Compliance Metrics | ✅ COMPLETE | — | Remove from active |
| 5.2 Cohort Analysis | ✅ COMPLETE | — | Remove from active |
| 5.3 Dashboard Homepage | ✅ COMPLETE | — | Remove from active (triggering event) |
| 3.5 Alerts & Notifications | ⚠ Defer confirmed | 3 | Confirm ⏸ defer — QA gate still open |
| 4.1b Tax-Year P&L | 🔥 Must continue | 1 | Canonical spec required before implementation |
| 4.1c Server-Side PDF | ⚠ Kill candidate | 1 | Propose Kill — displaced by BLG-OPS-01 |
| 4.3 Signal Exposure | 🔥 Must continue | 4 | PoG valid; v2.0 active planning |
| 4.2 Watchlists | 🔥 Must continue (P2) | 2 | Hold at Priority 2 |
| Chart Interactivity | 🔥 Must continue (P2) | 2 | Hold at Priority 2 |
| BLG-OPS-01 Dev Environment | ➕ Add candidate | 1 | Propose Add — structural QA gap |

---

## Cycle Proximity Score (CPS) — Pre-Rebalance

CPS before STEP 8 decisions (excluding completed items, including 4.1c, excluding BLG-OPS-01):

| Initiative | SPS |
|-----------|-----|
| 3.5 Alerts & Notifications | 3 |
| 4.1b Tax-Year P&L | 1 |
| 4.1c Server-Side PDF | 1 |
| 4.3 Signal Exposure | 4 |
| 4.2 Watchlists | 2 |
| Chart Interactivity | 2 |
| **CPS (pre-rebalance, 6 items)** | **2.17** |

**Prior cycle CPS:** 1.8 (12 items)
**Delta:** +0.37 — driven by removal of 8 low-SPS items (BLG-RD, TEST-GAP, 5.x, BLG-FEAT-08) and retention of 4.3 (SPS=4).
**Drift alert threshold:** +0.5. **No Strategy Drift Alert required.**

## Cycle Proximity Score (CPS) — Post-Rebalance (with STEP 8 decisions applied)

Kill 4.1c (SPS 1) → Remove; Add BLG-OPS-01 (SPS 1) → Add:

| Initiative | SPS |
|-----------|-----|
| 3.5 Alerts & Notifications | 3 |
| 4.1b Tax-Year P&L | 1 |
| BLG-OPS-01 Dev Environment | 1 |
| 4.3 Signal Exposure | 4 |
| 4.2 Watchlists | 2 |
| Chart Interactivity | 2 |
| **CPS (post-rebalance, 6 items)** | **2.17** |

CPS is unchanged post-rebalance (4.1c SPS=1 replaced by BLG-OPS-01 SPS=1). **No drift event from rebalance decisions.**

**Facilitator note:** CPS=2.17 is a modest increase from 1.8, caused by the removal of 8 maintenance-heavy low-SPS v1.9 items. The remaining portfolio is clean: one high-SPS item (4.3, gated by PoG), one high-priority infrastructure item (BLG-OPS-01), and balanced v2.0 deliverables. Challenger role is particularly relevant to 4.3 (SPS=4) — §13.2 scope constraint must be enforced at every pre-alignment discussion.
