**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.7
**Cycle:** 2026-05-31__release-v4.7
**Published:** 2026-05-31
**Mode:** standard

---

# Release Plan — v4.7

**Theme:** Arc 5 Completion Pre-work, Staged Verifications & Aged Backlog Clearance

---

## Readiness

**Release gate:** PASS
- `post_ship_complete = true` (v4.6 closed 2026-05-31)
- `next_cycle_unblocked = true`
- No open escalations from prior cycle
- No amendment in progress

**Roadmap alignment:** v4.7 declared as "Next planned release" in current_roadmap.md. No specific scoped items exist on the roadmap for v4.7 — scope derived from backlog candidates following rebalance (2026-05-27, DL-035). This is consistent with prior recent cycles.

**OA carry-forward (advisory):**
- OA-01: SI-02 data density gate, 6th consecutive deferral — gate ~Nov 2026; monitor at v4.8
- OA-02: Endpoint baseline drift (BLG-OPS-13, 24 endpoints) — P3, not scoped; advisory

**Backlog age advisory:**
- BLG-FEAT-38 (Provisional-Target: v4.1) — 3+ cycles without story assignment → **promoted to scope**
- BLG-OPS-28 (Provisional-Target: v4.1) — 4+ cycles without story assignment → **promoted to scope**

**Gate proximity (BLG-GOV-67 SI-05 Phase 1):** Gate clears 2026-06-21 (~21 days). Included as conditional Sprint 2 item.

---

## Scope

**Release:** v4.7 — Arc 5 Completion Pre-work, Staged Verifications & Aged Backlog Clearance

| ID | Item | Source | Priority | Effort | Type |
|----|------|--------|----------|--------|------|
| S2-01 | SI-04 §13 formal pre-assessment (BLG-GOV-62) | Backlog P1 | P1 | S | Governance / §13 Compliance |
| S2-02 | Arc 5 compliance score in monthly P&L (BLG-FEAT-38) | Backlog P2, aged 3+ cycles | P2 | M | Product Feature |
| S2-03 | Staging deploy live verification (BLG-OPS-28) | Backlog P2, aged 4+ cycles | P2 | XS | Operations |
| S2-04 | DS-07 migration staging verification (BLG-OPS-44) | Backlog P3, Provisional-Target: v4.7 | P3 | XS | Operations |
| S2-05 | Severity field staging verification (BLG-OPS-45) | Backlog P3, Provisional-Target: v4.7 | P3 | XS | Operations |
| S2-06 | Render log retention policy (BLG-OPS-31) | Backlog P2 | P2 | S | Operations |
| S2-07 | Anthropic API tier cost assessment (BLG-OPS-37) | Backlog P2, gate cleared (BLG-OPS-36 complete) | P2 | S | FinOps |
| S2-08 | Pre-entry validation panel UX assessment (BLG-FE-49) | Backlog P2 | P2 | S | Frontend / UX |
| S2-09 | SI-05 Phase 1 implementation (BLG-GOV-67) | Backlog P2, gate clears 2026-06-21 | P2 | M | Product Feature (conditional) |

**Items explicitly deferred:**

| Item | Reason |
|------|--------|
| BLG-FEAT-25 / SI-02 Frontend (ST-06/07/08) | Gate NOT MET — 0 linked trade_plans; ~Nov 2026 |
| BLG-QA-26 — Arc 5 QA protocol | Gate NOT MET — not all 5 Arc 5 features shipped |
| BLG-GOV-68 — Backlog inter-dependency tracking | Gate NOT MET — 20+ concurrent items with dependency-blocking |
| BLG-OPS-13 — API performance baseline re-run | P3, M effort, requires live env coordination — defer |
| All Arc 4 PO-02–05 | Data density gates not met |
| All Arc 6 | Data density gates not met |

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-09 | Strategy Rules & System Intent Owner (ST-01); Head of Specs Team / Product Owner (ST-02 conditional) | RISK-01 | ST-01 Sprint 1 firm; ST-02 conditional Sprint 2 (gate 2026-06-21) |
| EPIC-02 | S2-02 | Head of Backend Engineering; Financial Reporting & Records Owner | RISK-02 | Sprint 1; no inter-EPIC dependency |
| EPIC-03 | S2-03, S2-04, S2-05, S2-06 | Infrastructure & Operations Owner; Data Model & Domain Schema Owner | RISK-03 | Sprint 1; staging environment required for S2-03/04/05 |
| EPIC-04 | S2-07, S2-08 | FinOps & Resource Architect (S2-07); Head of UX & Design (S2-08) | — | Sprint 1; independent of other EPICs |

**EPIC-02 note:** BLG-FEAT-38 requires adding a strategy compliance section to the existing monthly P&L report endpoint. GET /analytics/arc5-compliance (shipped v4.0) provides the data source. Backend + frontend change of M effort.

**EPIC-03 note:** S2-03 (BLG-OPS-28) requires RENDER_STAGING_DEPLOY_HOOK secret configuration — an external dependency. Infrastructure & Operations Owner must verify Render dashboard access before ST-04 begins.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | SI-05 Phase 1 gate (2026-06-21) may not be confirmed before Sprint 2 planning seal if sprint runs short | Medium | Treat ST-02 as conditional; PO confirms gate before Sprint 2 seals | null |
| RISK-02 | EPIC-02 | Monthly P&L compliance section requires GET /analytics/arc5-compliance on staging — if endpoint unavailable, frontend integration blocks | Low | Verify endpoint on staging before sprint planning seals; endpoint shipped v4.0, expected stable | null |
| RISK-03 | EPIC-03 | Staging deploy live verification (BLG-OPS-28) requires Render infrastructure access for webhook configuration | Low | Infrastructure & Operations Owner confirms Render dashboard access before ST-04 | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**Cross-check:**
- All S2 IDs (S2-01 through S2-09): unique, sequentially assigned ✅
- All EPICs (EPIC-01 through EPIC-04): unique IDs ✅
- EPIC-01 → Maps to S2-01, S2-09 ✅
- EPIC-02 → Maps to S2-02 ✅
- EPIC-03 → Maps to S2-03, S2-04, S2-05, S2-06 ✅
- EPIC-04 → Maps to S2-07, S2-08 ✅
- All S2 IDs mapped to an EPIC ✅
- All RISK IDs in EPIC table appear in Risk Register ✅
- No orphaned scope items ✅

**Stage 3.5 outcome:** PASS — plan is internally consistent and executable.

---

## Capacity Check

**Baseline:** Double capacity — ~24–28 days per sprint (same as v4.6 per user instruction).

**Effort Band Lookup:** No matching entries in scored_initiatives.md for BLG-* items (file covers arc-level features only). Using inline estimates.

### Sprint 1 (firm)

| EPIC | ST | Item | Effort |
|------|-----|------|--------|
| EPIC-01 | ST-01 | SI-04 §13 pre-assessment | S (~1 day) |
| EPIC-02 | ST-03 | Arc 5 compliance score in monthly P&L | M (~2 days) |
| EPIC-03 | ST-04 | Staging deploy live verification | XS (~0.5 day) |
| EPIC-03 | ST-05 | DS-07 migration staging verification | XS (~0.5 hr) |
| EPIC-03 | ST-06 | Severity field staging verification | XS (~0.5 hr) |
| EPIC-03 | ST-07 | Render log retention policy | S (~0.5 day) |
| EPIC-04 | ST-08 | Anthropic API tier cost assessment | S (~0.5 day) |
| EPIC-04 | ST-09 | Pre-entry validation panel UX assessment | S (~0.5 day) |
| **Sprint 1 total** | | | **~5–6 days** |

Sprint 1 utilisation: ~20–25% of 24–28 day capacity → **PASS**

### Sprint 2 (conditional)

| EPIC | ST | Item | Effort | Gate |
|------|-----|------|--------|------|
| EPIC-01 | ST-02 | SI-05 Phase 1 implementation | M (~2–3 days) | SI-01 + SI-03 live ≥30 days (2026-06-21) |
| **Sprint 2 conditional total** | | | **~2–3 days** | |

Sprint 2 conditional utilisation (if gate met): ~8–12% → **PASS**

### Phasing Recommendation

| Phase | EPICs | Estimated effort | Capacity |
|-------|-------|------------------|----------|
| Sprint 1 (firm) | EPIC-01 ST-01, EPIC-02, EPIC-03, EPIC-04 | ~5–6 days | ~24–28 days |
| Sprint 2 (conditional) | EPIC-01 ST-02 | ~2–3 days | ~24–28 days |
| **Total** | | **~7–9 days** | **~48–56 days** |

**Ordering rationale:** Staging verifications (EPIC-03) clear v4.6 OAs first. Feature work (EPIC-02) alongside assessments (EPIC-04). Arc 5 pre-work (EPIC-01) in both sprints.

**Capacity verdict: PASS** — well within doubled capacity. Scope is constrained by available actionable items, not capacity.

```yaml
state.json update:
  artifacts.stage4_5_capacity_check: pass
  attributes.capacity_feasible: pass
```
