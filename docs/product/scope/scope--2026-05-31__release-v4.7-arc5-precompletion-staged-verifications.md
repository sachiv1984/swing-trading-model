**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Release:** v4.7
**Cycle:** 2026-05-31__release-v4.7
**Last Updated:** 2026-06-01

Superseded by: v4.7 ship — 2026-06-01
Changelog: docs/product/changelog.md#v47
Verification report: claude/cycles/2026-05-31__release-v4.7/verification_report.md
Cycle: 2026-05-31__release-v4.7

---

# Scope — v4.7: Arc 5 Completion Pre-work, Staged Verifications & Aged Backlog Clearance

---

## Items in Scope

| S2-ID | Item | Source | Priority | Effort | Type | Status |
|-------|------|--------|----------|--------|------|--------|
| S2-01 | SI-04 §13 formal pre-assessment (BLG-GOV-62) | Backlog P1 | P1 | S | Governance / §13 Compliance | Firm |
| S2-02 | Arc 5 compliance score in monthly P&L (BLG-FEAT-38) | Backlog P2, aged 3+ cycles | P2 | M | Product Feature | Firm |
| S2-03 | Staging deploy live verification (BLG-OPS-28) | Backlog P2, aged 4+ cycles | P2 | XS | Operations | Firm |
| S2-04 | DS-07 migration staging verification (BLG-OPS-44) | Backlog P3, Provisional-Target v4.7 | P3 | XS | Operations | Firm |
| S2-05 | Severity field staging verification (BLG-OPS-45) | Backlog P3, Provisional-Target v4.7 | P3 | XS | Operations | Firm |
| S2-06 | Render log retention policy (BLG-OPS-31) | Backlog P2 | P2 | S | Operations | Firm |
| S2-07 | Anthropic API tier cost assessment (BLG-OPS-37) | Backlog P2, gate cleared | P2 | S | FinOps | Firm |
| S2-08 | Pre-entry validation panel UX assessment (BLG-FE-49) | Backlog P2 | P2 | S | Frontend / UX | Firm |
| S2-09 | SI-05 Phase 1 implementation (BLG-GOV-67) | Backlog P2, gate clears 2026-06-21 | P2 | M | Product Feature | Conditional |

**Firm items:** S2-01 through S2-08 (8 items)
**Conditional items:** S2-09 (1 item — gate: SI-01 + SI-03 live ≥30 days, clearing 2026-06-21)

---

## Items Explicitly Deferred

| Item | Reason |
|------|--------|
| BLG-FEAT-25 / SI-02 Frontend | Gate NOT MET — 0 closed trades with linked trade_plans; ~Nov 2026 |
| BLG-QA-26 — Arc 5 QA protocol | Gate NOT MET — not all Arc 5 features shipped |
| BLG-GOV-68 — Backlog inter-dependency tracking | Gate NOT MET — 20+ concurrent dependency-blocking items |
| BLG-OPS-13 — API performance baseline re-run | P3, M effort, live env required — defer |
| PO-02 through PO-05 | Data density gates not met (earliest: Oct 2026) |
| All Arc 6 features | Data density gates not met |

---

## Supersession Note

*(Completed at Post-Ship Closure — leave blank.)*
