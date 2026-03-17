**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-17

---

# Stage 1 — Roadmap Re-Validation

**Cycle:** 2026-03-17__item-v1.10
**Date:** 2026-03-17
**Authorities:** Product Owner + Strategy Rules & System Intent Owner

---

## Context Since Prior Cycle (2026-03-15__item-5.3)

The following material changes have occurred since 2026-03-15:

1. **v1.10 shipped (2026-03-16)** — all 6 EPICs complete: EPIC-01 (dev environment ST-01–ST-03), EPIC-02 (CohortAnalysis backend refactor ST-04), EPIC-03 (API integration tests ST-05–ST-06), EPIC-03 (QA scenario gaps ST-07), plus design gate and sprint 2 items (ST-12 multi-sprint carryover). Verified: verification_status = Verified_with_deviations.
2. **BLG-OPS-01 delivered (2026-03-16)** — Development/staging environment now live. P1 infrastructure gap resolved. The Director of Quality sign-off workflow can now run against staging before merging to production.
3. **New backlog items raised during v1.10 execution:** BLG-BE-01 (P1 — GET /portfolio missing 4 fields, v1.11 target), TEST-GAP-EPIC-02 (P3 — CohortAnalysis integration regression scenario), BLG-BE-02 (P3 — prospective-heat endpoint spec+implementation).
4. **PoG POG-20260304-01 (item 4.3):** Still valid — strategy_rules.md remains at v1.3. No re-issuance required.
5. **BLG-GOV-01 and BLG-GOV-02 added to backlog (2026-03-16)** — Governance process improvement items (roadmap stage consolidation; ideas register redesign). P2, v2.0 governance prep.
6. **v2.0 planning window now fully open:** v1.10 closed and verified; capacity freed. v2.0 scope: 4.1b Tax-Year P&L, 4.3 Signal Exposure (gate cleared), 3.5 Alerts (QA gate still pending).

---

## Active Initiatives Reviewed

---

### BLG-OPS-01 — Development Environment (v1.10)

**Classification:** ✅ COMPLETE — Shipped 2026-03-16

Delivered as EPIC-01 in v1.10 Sprint 2 (ST-01–ST-03). Staging environment live. Director of Quality can now test against staging before production merge. P1 infrastructure gap resolved. Removed from active initiative tracking.

---

### 3.5 — Alerts & Notifications (v2.0)

**Classification:** ⚠ Defer confirmed (QA gate still pending)

**What has changed:**
- No change since DL-003. Third gate (QA planning session for notification delivery) remains uncleared as of 2026-03-17.
- Auto-advance trigger from DL-003 remains active: once QA planning session is completed and documented, 3.5 auto-advances to active v2.0 planning.
- v1.10 complete; v2.0 planning window now open — however, 3.5 gate must clear before pre-alignment opens for this item.

**Would we still choose this?** Yes when gate is cleared. Email and market-regime alerts are high user value. Async delivery complexity requires QA design first — gate is architecturally sound.

**Strategy Proximity Score: 3**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §3 (human-in-loop), §8.1–8.3 — notifications are advisory only; all trade actions remain human-initiated. Score 3 because market regime change notification touches §8.2 (risk-off signal delivery) but remains strictly read-only. No automation of action.

**Resolution:** Confirm ⏸ defer. Gate condition unchanged. No workforce allocation until QA gate clears.

---

### 4.1b — Tax-Year P&L Statement (v2.0)

**Classification:** 🔥 Must continue

**What has changed:**
- No change since prior cycle. v1.10 shipped; no pre-work dependency on v1.10 items.
- Canonical spec for P&L Statement still required before implementation begins. Financial record requiring its own spec.
- BLG-NEW-06 P&L labelling pre-work scope remains merged into 4.1b.

**Would we still choose this?** Yes. The only formal per-tax-year financial record output in the product. High value for a trading tool. Required for tax compliance purposes.

**Strategy Proximity Score: 1**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — financial reporting. Pure output generation from existing trade data. No contact with strategy execution boundaries.

---

### 4.3 — Signal Exposure Enhancement (v2.0 — active planning)

**Classification:** 🔥 Must continue

**What has changed:**
- No change since DL-004. PoG POG-20260304-01 remains valid (strategy_rules.md still at v1.3).
- v2.0 planning window fully open — 4.3 is a confirmed executable v2.0 item.
- Frontend-only; backend already supports `top_n` and `lookback_days`.

**PoG validity check (STEP 5.0.A):** POG-20260304-01 references strategy_rules.md v1.3. Current version: v1.3. **PoG is valid.** No re-issuance required.

**Would we still choose this?** Yes. Low effort, gate cleared, backend already ready. Natural v2.0 item.

**Strategy Proximity Score: 4**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §13.2 — scope boundary enforced by PoG POG-20260304-01. Score 4 retained; this item remains boundary-adjacent regardless of gate clearance. Challenger must lead with §13-referenced counter-argument if any scope expansion beyond `top_n` and `lookback_days` is proposed.

---

### 4.2 — Watchlists & Screening (Priority 2)

**Classification:** 🔥 Must continue (at Priority 2 — do not pull forward)

**What has changed:** None. Hold at Priority 2 until v2.0 items clear.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: None — monitoring tickers for entry signals using existing strategy logic. Standard product scope, no boundary proximity.

---

### Chart Interactivity Enhancements (Priority 2)

**Classification:** 🔥 Must continue (at Priority 2)

**What has changed:** None. Scope boundary (no new technical indicators without §13 review) unchanged.

**Strategy Proximity Score: 2**
*Assigned by: Strategy Rules & System Intent Owner*
Section reference: §13.2 noted in item definition — new indicators blocked without review. Hover, zoom, drill-down on existing charts are display-only enhancements with no strategy contact.

---

## Summary Table

| Initiative | Classification | SPS | Action |
|-----------|----------------|-----|--------|
| BLG-OPS-01 Dev Environment | ✅ COMPLETE | — | Remove from active (shipped v1.10) |
| 3.5 Alerts & Notifications | ⚠ Defer confirmed | 3 | Confirm ⏸ defer — QA gate still open |
| 4.1b Tax-Year P&L | 🔥 Must continue | 1 | Spec required before implementation |
| 4.3 Signal Exposure | 🔥 Must continue | 4 | PoG valid; v2.0 active |
| 4.2 Watchlists | 🔥 Must continue (P2) | 2 | Hold at Priority 2 |
| Chart Interactivity | 🔥 Must continue (P2) | 2 | Hold at Priority 2 |

---

## Cycle Proximity Score (CPS)

**Active initiatives (post-rebalance, excluding BLG-OPS-01 completed):**

| Initiative | SPS |
|-----------|-----|
| 3.5 Alerts & Notifications | 3 |
| 4.1b Tax-Year P&L | 1 |
| 4.3 Signal Exposure | 4 |
| 4.2 Watchlists | 2 |
| Chart Interactivity | 2 |
| **CPS (5 items)** | **2.40** |

**Prior cycle CPS:** 2.17 (6 items post-rebalance, cycle 2026-03-15__item-5.3)
**Delta:** +0.23 — driven by removal of BLG-OPS-01 (SPS=1), which raises the mean slightly as the lower-SPS item exits.
**Delta alert threshold:** +0.5. **No delta Strategy Drift Alert required.**
**Absolute alert threshold:** 2.5. CPS 2.40 < 2.5. **No absolute Strategy Drift Alert required.**

**Tier confirmation:** Standard. (CPS < 2.5; no extended conditions met.)

**Facilitator note:** CPS trending slightly upward cycle-by-cycle as delivered low-SPS items are retired and higher-SPS items (particularly 4.3 at SPS=4) remain. The upward drift is structural — not driven by scope expansion — and will correct once 4.3 ships. The Challenger role is particularly relevant to 4.3 (SPS=4, boundary-adjacent) at every v2.0 discussion. §13.2 scope constraint must be enforced at every pre-alignment discussion for 4.3.

---

## Horizon Review

**Horizon structure per STEP 2.3:**

The current roadmap uses §3/§4/§5 structure rather than explicit Now/Next/Later labels. Mapping:

| Horizon | Current roadmap section | Items |
|---------|------------------------|-------|
| Now | §3 Delivery Plan (v2.0) | 4.1b, 4.3 (executable); 3.5 (deferred-gated, in-plan) |
| Next | §4 Priority 2 — Next Phase (post v2.0) | 4.2 Watchlists, Chart Interactivity |
| Later | §5 Priority 3 — Deferred | Position Correlation, Backtesting, Mobile, etc. |

The explicit Now/Next/Later labels are not yet in the roadmap. Recorded as required lifecycle update in STEP 9 Write Plan.

**Horizon movements review:**

*Later → Now/Next promotions considered:*
- No later items have context changes that warrant promotion. Backtesting, Multi-Portfolio, Mobile remain correctly deferred. BLG-TECH-05 Prometheus remains at v2.1 target.

*Next → Now promotions considered:*
- 4.2 Watchlists: No context change — hold at Next. v2.0 items have priority.
- Chart Interactivity: No context change — hold at Next. Effort is low but scope is bounded to existing charts.

**Outcome:** No horizon movements recommended. Mapping formalised in STEP 9 roadmap update.
