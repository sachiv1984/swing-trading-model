**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-04

---

# Stage 5 — Final Rebalance Decision

**Cycle:** 2026-03-04__item-3.4
**Date:** 2026-03-04
**Authority:** Product Owner (within all constraints and vetoes)

---

## Decision: 3.5 — Alerts & Notifications

**Decision type:** ⏸ Defer (confirmed — gate condition update)

**Rationale:** The third hard gate (QA planning session for notification delivery) remains uncleared. Two of three gates are now cleared (EPIC-04 logging ✅, EPIC-05 API versioning ✅). The QA planning session is required before v2.0 pre-alignment opens.

**New condition recorded:** Auto-advance trigger — once the QA planning session for notification delivery is completed and documented, 3.5 Alerts auto-advances to active v2.0 planning without requiring a new rebalance cycle. The session output must specify: test types required, notification delivery modes to be tested, expected test infrastructure.

**Displacement:** None. This is an existing roadmap item confirming its defer status.

**Decision log entry:** DL-003 (new — auto-advance condition is new)

---

## Decision: 4.3 — Signal Exposure Enhancement

**Decision type:** 🔁 Replace (gated → active v2.0 planning)

**Rationale:** §13 gate cleared by v1.7 SRB (EPIC-02). PoG POG-20260304-01 issued in STEP 5.3 of this cycle. The item may now enter v2.0 pre-alignment planning.

**Scope constraint (immutable):** Only `top_n` and `lookback_days` are cleared. Any additional parameters require a new §13 review before pre-alignment. PoG POG-20260304-01 is the authority record.

**Displacement:** No displacement required — gated item unblocked, not a new addition.

**Decision log entry:** DL-004 (new)

---

## Decision: 8 New Backlog Items (from IW-20260304-01)

**Decision type:** ➕ Add to backlog (not roadmap-level initiatives)

Items promoted to backlog:
1. **BLG-NEW-01** — Golden Output Regression Baseline for CI (Quality, P1)
2. **BLG-NEW-02** — Backtest vs Live Stop Reconciliation Report (Quality, P1; dependency: after BLG-NEW-01)
3. **BLG-NEW-03** — Define and Document Unavailability Failure Mode (Policy, P1; ~0.5 day)
4. **BLG-NEW-04** — AI-Assisted Workflow Governance Policy (Governance, P2)
5. **BLG-NEW-05** — Dependency Vulnerability Scanning in CI (Security/CI, P1)
6. **BLG-NEW-06** — Realised vs Unrealised P&L Labelling (merged into 4.1b pre-work scope — not a standalone backlog item)
7. **BLG-NEW-07** — Running API Changelog Document (Documentation/Governance, P1)
8. **BLG-NEW-08** — Automated OpenAPI Drift Detection in CI (CI/Governance, P1)

**Displacement at backlog level:** These items compete within v1.8 release capacity. The release planning engine will determine which items enter the v1.8 backlog slice. No roadmap-level displacement required.

**Stop candidate noted:** 4.1c Server-Side PDF Report is the lowest-value existing roadmap item and the natural displacement candidate if a future roadmap-level Add requires stops.

**Decision log entry:** DL-005 (new)

---

## Decision: All Other Roadmap Initiatives

| Initiative | Decision | Reason |
|-----------|----------|--------|
| 3.4 Risk Dashboard | ✅ Confirmed | Pre-req gate cleared; v1.8 start |
| 5.1 Trade Reflection | ✅ Confirmed | No change; BLG-FEAT-08 path intact |
| BLG-FEAT-08 Compliance Metrics | ✅ Confirmed | Gate for 5.1; LL-05 capacity check at v1.9 pre-alignment |
| 5.2 Cohort Analysis | ✅ Confirmed | No change |
| 5.3 Dashboard Homepage | ✅ Confirmed | No change |
| 4.1b Tax-Year P&L | ✅ Confirmed (scope note) | Scope updated: P&L labelling pre-work added as prerequisite |
| 4.1c Server-Side PDF | ✅ Confirmed | Lowest-value item; flagged as displacement candidate |
| 4.2 Watchlists (P2) | ✅ Confirmed | Hold at P2; do not pull forward |
| Chart Interactivity (P2) | ✅ Confirmed | Hold at P2 |

No formal decision entries required for confirmed items — no roadmap change.

---

## STEP 7.1 Skill-Silo Check (recorded here per completion condition)

Governance load %: ~21% (within 20–60% bounds)
- Ceiling alert: Not triggered
- Floor check: Product Owner confirmed adequate sign-off capacity
- No Skill-Silo Alert issued

---

## Net Roadmap Change Summary

| Type | Count | Items |
|------|-------|-------|
| ⏸ Defer (confirmed with new condition) | 1 | 3.5 Alerts |
| 🔁 Replace (status change) | 1 | 4.3 Signal Exposure (gated → active) |
| ➕ Add (backlog-level only) | 7 | BLG-NEW-01 through BLG-NEW-08 (BLG-NEW-06 merged into 4.1b) |
| ✅ Confirmed (no change) | 9 | All other roadmap items |
| ❌ Kill | 0 | — |

**Hard rule check:** Adds require stops. Roadmap-level Adds = 0 (all new items are backlog-level). Stops = 0. 0 ≥ 0 ✅

**Scarce skills check:** No scarce skill constraints. ✅

**Quality/Security/Financial Records blocking authority:** Not exercised. ✅
