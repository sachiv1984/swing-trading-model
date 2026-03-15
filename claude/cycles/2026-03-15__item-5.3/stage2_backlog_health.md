**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-15

---

# Stage 2 — Backlog Health Check

**Cycle:** 2026-03-15__item-5.3
**Date:** 2026-03-15

---

## Purpose

Review the backlog for orphan items, stale assignments, and items that should be promoted, retired, or re-prioritised following v1.9 Sprint 2 completion.

---

## Items Reviewed

### P1 Items

---

**BLG-OPS-01 — Provision Development Environment**
**Current priority:** P1
**Status:** Open
**Assessment:** ELEVATE to roadmap — structural QA gap. No development environment means all QA runs against production. This is a governance-critical infrastructure gap that unblocks proper QA workflow. Propose roadmap-level inclusion (displacing 4.1c) in STEP 5. Target: v1.10.

---

### P2 Items

---

**BLG-TECH-06 — Fix CohortAnalysis client-side computation**
**Current priority:** P2
**Status:** Open
**Assessment:** VALID — filed 2026-03-13 from v1.9 QA. analytics.md §15 hard rule violation (client-side computation in CohortAnalysis.js). Numerical output currently correct, but divergence risk exists. Retain at P2 for v1.10. No promotion required.

**BLG-FEAT-03 — Slippage Tracking**
**Current priority:** P2
**Status:** Open — ⚠️ Orphan (no roadmap home)
**Assessment:** ORPHAN CONFIRMED — orphan notice has been present since the prior backlog review. Item has not been assigned a roadmap home or cycle. Product Owner action required: assign to a release (v1.10 or v2.1) or explicitly defer/retire. Flag for next release planning session.

---

### P3 Items

---

**BLG-TECH-05 — Prometheus Metrics Endpoint**
**Current priority:** P3
**Status:** Open — deferred to v2.1/multi-user
**Assessment:** VALID DEFER — no change in rationale. Defer until operational need or multi-user requirement.

---

### Completed Items (v1.9 Sprint 2)

The following backlog items shipped in v1.9 Sprint 2 and are now complete:

| Item | Shipped |
|------|---------|
| BLG-FEAT-08 — Basic Compliance Metrics | Sprint 2 ST-01 |
| BLG-SPEC-D1 — API Contracts README update | Sprint 1 ST-19 |
| BLG-SPEC-D3 — GET /market/status documentation | Sprint 1 ST-16 |

Completed items to be archived at next `groom backlog` run.

---

### Orphan Governance Notices

**TEST-GAP-EPIC-06 (§6 of backlog.md)**
Status: Still unresolved. QA & Testing Owner has not yet created scenarios for sharpe_ratio_trade_method, portfolio field alignment, or holding_days. This gap predates v1.9. Carry forward to v1.10 pre-alignment; assign BLG-ID at next sprint planning.

---

## New Item — BLG-NEW-13

**Source:** IDEA-head-of-specs-20260304-02 (Spec Coverage Inventory idea, advanced from idea pool)
**Proposed ID:** BLG-NEW-13
**Title:** Spec Coverage Inventory
**Priority:** P2
**Type:** Governance / Spec
**Owner:** Head of Specs Team
**Target release:** v2.0 (or v1.10 if capacity allows)

Audit which canonical spec sections have implementation coverage and which are untested or undocumented. Creates a living inventory of spec-to-implementation coverage gaps. Complements the existing Canonical Terms Glossary (BLG-NEW-11). Outputs a structured report that identifies coverage gaps for prioritisation.

**Acceptance Criteria:**
- Inventory document produced covering all docs/specs/ sections
- Each spec section rated: covered / partial / gap
- Gap items cross-referenced against open backlog items where possible
- Review cadence defined (e.g. per audit cycle)

---

## Backlog Health Summary

| Status | Count | Notes |
|--------|-------|-------|
| P1 Open | 1 | BLG-OPS-01 (propose elevate to roadmap) |
| P2 Open | 2 | BLG-TECH-06, BLG-FEAT-03 (orphan — action required) |
| P3 Open | 1 | BLG-TECH-05 (valid defer) |
| New this cycle | 1 | BLG-NEW-13 (Spec Coverage Inventory) |
| Completed this cycle | 3+ | BLG-FEAT-08, BLG-SPEC-D1, BLG-SPEC-D3 (+ Sprint 1 items) |

**Overall backlog health: GOOD** — post-v1.9 completion, the backlog is lean. Key risk is the BLG-FEAT-03 orphan (action required from Product Owner). BLG-OPS-01 elevation to roadmap is the primary structural action.
