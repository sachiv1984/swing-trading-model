Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v4.5
Cycle: 2026-05-30__release-v4.5
Last Updated: 2026-05-30

## Planning Decisions — v4.5 Governance Prompt Hardening, Audit Debt & SI-02 Spec Pre-Planning

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-GOV-70 in Sprint 1 | Stale (2+ cycles, 3+ phase recurrences); audit AUD-003 mandates v4.5 entry; v4.4 carry-forward item 1 requires resolution before sprint planning seals | Product Owner | 2026-05-30 |
| Defer BLG-GOV-32 (gate-condition tracker) to v4.6 | Modifies release planning prompt mid-cycle; not urgent vs. execution_prompt.md OAs; lower priority than audit Tier 2 debt | Product Owner | 2026-05-30 |
| Mark BLG-GOV-30/31/55 as resolved (not in scope) | Confirmed resolved per prompt_change_log.md (2026-05-22 entries); backlog grooming will archive | Head of Specs Team | 2026-05-30 |
| EPIC-03 (SI-02 spec pre-sprint) is conditional | SI-02 20-closed-trades gate status unknown; Sprint 2 gated on PO explicit confirmation; prevents wasted pre-planning work if gate not imminent | Product Owner | 2026-05-30 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 in Sprint 1, must complete before sprint planning seals | v4.4 OA deadline: "Before v4.5 sprint planning" | PMO Lead | 2026-05-30 |
| EPIC-02 in Sprint 1 parallel to EPIC-01 | Agent header changes are cosmetic and independent; no version bump overhead; fast delivery | Head of Specs Team | 2026-05-30 |
| EPIC-03 in Sprint 2, conditional | SI-02 gate not yet confirmed; sequenced after Sprint 1 firm work; avoids sprint planning seal dependency | PMO Lead | 2026-05-30 |
| No design gate required | No new frontend features, no new API endpoints, no UX design decisions required; v4.5 is governance/spec sprint only | Head of UX & Design + Product Owner | 2026-05-30 |

### Accepted risks

None.

*(Supersession note: to be completed at post-ship closure.)*
