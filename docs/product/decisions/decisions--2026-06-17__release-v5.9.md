**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Release:** v5.9
**Cycle:** 2026-06-17__release-v5.9
**Last Updated:** 2026-06-17

---

# Planning Decisions — v5.9

## Scope Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| BLG-FE-64/41 classified conditional (not firm) despite carry-forward advisory suggesting firm | STEP 1.4b mandatory rule: gate date 2026-06-21 falls within sprint window; cannot classify as firm regardless of near-certainty. Carry-forward from v5.8 closure was advisory; STEP 1.4b is mandatory. | Head of Specs Team |
| BLG-GOV-125–129 all classified firm | All five SC items are Ready now with no gate conditions. Confirmed by GCA-2026-06-17 assessment (ST-04, v5.8). | Product Owner |
| BLG-OPS-70 classified conditional | Gate ~2026-06-23 (next SI-05 digest delivery) falls within sprint window per STEP 1.4b. | Head of Specs Team |
| BLG-GOV-113 included as separate conditional story | Roadmap lists BLG-GOV-113 as "SI-05 effectiveness review protocol execution" as a discrete story separate from BLG-GOV-112/115. Gate 2026-07-04. | PMO Lead |
| BLG-GOV-124 (SC-02) deferred | Higher implementation risk (removing a guard with complex extraction constraint); P3 priority; no sprint urgency. | Product Owner |

## Sequencing Decisions

| Decision | Rationale |
|----------|-----------|
| EPIC-01 merges first | All items ready now; governance-only; no dependencies. Can close before sprint 1 ends. |
| EPIC-02 split across Sprint 1 and Sprint 2 | S2-02/S2-03 items clear by ~2026-06-23 (Sprint 1); S2-04 items clear 2026-07-04 (Sprint 2). Sprint planning engine to manage this split within a single EPIC. |
| Sprint 2 start: after 2026-07-04 gate confirmed | Gate owner (Infrastructure & Operations Owner / Director of Quality for SI-05 review) must explicitly confirm gate cleared before Sprint 2 items enter execution. |

## Accepted Risks

None.

## Escalations

None.

## Supersession note

*(Completed at Post-Ship Closure)*
