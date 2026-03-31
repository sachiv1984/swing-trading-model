Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v2.4
Cycle: 2026-03-31__release-v2.4
Last Updated: 2026-03-31

---

## Planning Decisions — v2.4 Correctness, Insight & Governance Hardening

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| BLG-GOV-08 (prompt compression, L) deferred to v2.5 | Too large for this cycle given backend capacity ceiling (identified rebalance 2026-03-31) and action-now governance priority (EPIC-06). A dedicated sprint in v2.5 is more appropriate than absorbing it mid-v2.4. | Product Owner | 2026-03-31 |
| EPIC-06 governance patches designated Sprint 1 non-deferrable | Three second-recurrence items (LL-v2.2-EX-01/02/04) and v2.3 Friction Items 1/2 carry "action-now priority" per v2.3 carry-forward CF-1/CF-3. A third cycle of deferral constitutes a governance process failure. Sprint planning may not move EPIC-06 stories to Sprint 2+. | Product Owner + Head of Specs Team | 2026-03-31 |
| BLG-FEAT-14 weekly digest scope constrained to raw data only | Challenger debate in roadmap rebalance 2026-03-31 accepted scope constraint: no generated text, narrative, or interpretation in any response field. This constraint is carried into the EPIC-04 AC and is a DoQ-verified acceptance criterion. | Product Owner (Challenger debate accepted) | 2026-03-31 |
| Spec debt items (BLG-SPEC-D15/16) scheduled Sprint 1 | These are foundational correctness items that may inform other work (EPIC-01 ST-03 joins trade_history). Resolving them early avoids downstream assumption risk. | PMO Lead | 2026-03-31 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (backend) in Sprint 2, EPIC-04 (weekly digest BE) in Sprint 3 | Backend engineering is the capacity ceiling for v2.4. Separating BE-heavy EPICs across sprints prevents bandwidth conflict. | PMO Lead | 2026-03-31 |
| EPIC-03 (spec debt) before EPIC-01 (backend) | BLG-SPEC-D16 reconciliation may inform EPIC-01 ST-03 (stop price join). Resolving the trade_history schema before implementing analytics changes reduces rework risk. | Head of Specs Team | 2026-03-31 |

### Accepted risks

None. No Accepted Risk (AR) escalations were raised during this cycle.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-03-31__release-v2.4
