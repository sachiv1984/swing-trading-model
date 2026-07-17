Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-17
Cycle: 2026-07-17__release-v7.4

## Amendment — AMD-20260717-01

**Phase:** Amendment
**Cycle:** 2026-07-17__release-v7.4
**Section anchor:** `## Amendment — AMD-20260717-01` (stable)
**Filed:** 2026-07-17
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Release plan sequenced EPIC-01/ST-01 (a sprint-execution story) to produce the design artefacts EPIC-02/04/05 needed to clear Design Gate, but Design Gate must clear before Sprint Planning seals — the artefacts structurally could never exist in time. | Amendment | A | action-now | Amended `2026-07-17__release-v7.4` (`AMD-20260717-01`) to remove ST-02/03/04/05, reducing Sprint Planning scope to EPIC-01/ST-01 only (already Design Pre-Approved). `BLG-FE-115/116/117/118` remain valid backlog scope for a future release once real design artefacts exist. | PMO Lead / Product Owner | 2026-07-17 |
| EPIC-03 (`BLG-FE-116`, price alerts) had zero design-artefact production scheduled anywhere in the v7.4 plan — not even deferred to in-sprint work like the other three. | Amendment | B | decision | No action needed this cycle (item removed); flag for whoever re-scopes `BLG-FE-116` into a future release: assign Head of UX & Design artefact production explicitly, don't assume it's covered by a readiness-pass story. | Product Owner | Next release scoping BLG-FE-116 |
| Release planning and Design Gate engines have no cross-check preventing a release plan from scheduling a Design Required item's artefact production as in-sprint work — this is a structural pattern that could recur in any future release that reuses the "readiness pass gates implementation EPICs" sequencing idea. | Amendment | C | defer | Consider a Release Planning STEP check: if a Design Required item's UX-spec production is scheduled inside another item's acceptance criteria rather than as a pre-sprint deliverable, flag it explicitly as a Design Gate risk at release-planning time, not first discovered at Design Gate. | Head of Specs Team | Unscheduled — candidate backlog item |

**Recurrence Notes:**
None — first occurrence of this specific sequencing conflict (readiness-pass-gates-implementation-EPICs pattern) in the project's amendment history.
