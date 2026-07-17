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

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-07-17__release-v7.4
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-07-17
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-07-15__release-v7.2 (`lessons_learnt_cycle.md` `## Phase 3`) — see Recurrence Notes below.

### What went well

- LL-v7.2-P3-01's fix (session-start `git fetch origin` + local-vs-`origin/main` divergence check, applied to `execution_prompt.md` STEP -1 at v3.57 during v7.2's post-ship closure) worked as intended on this cycle's very first `run sprint` invocation — local `main` was confirmed up to date with `origin/main` before any state file was trusted, avoiding the duplicate-initialisation failure mode v7.2 hit.
- Single autonomous story (ST-01), single EPIC, delivered end-to-end in one pass: dependency pre-flight, two UX specs, a design review, a Playwright baseline scope, an analytics event schema, and a CI tagging scheme all produced in one consolidated document. Zero delegation records, zero items returned to backlog, zero escalations, zero spec deviations.
- The post-merge HARD GATE halt (STEP 4.4) and its required re-invocation worked cleanly across the session boundary: the prior session merged PR #1011, committed the persist-state commit (`5a9e91c1`), and halted; this session's re-invocation correctly detected `merge_gate.all_merged = true` with `epics_pending` empty and proceeded directly to STEP 5 (Sprint Close) without re-evaluating already-merged EPIC conditions.
- A genuine out-of-scope finding (react-day-picker v8→v9 API break in the currently-unused `src/components/ui/calendar.js`, affecting the deferred EPIC-05) was correctly routed to a backlog filing (`BLG-FE-122`) rather than a spec deviation, per the STEP 3.1.A step-10 deviation-type distinction — the finding concerns a future, currently out-of-scope EPIC, not a divergence from this story's own spec.
- The amendment (`AMD-20260717-01`) that reduced this sprint's scope from 5 stories to 1 (Design Gate blocking ST-02/03/04/05 pre-seal) is fully accounted for at the Amendment section above — no separate Phase 3 friction item duplicates it.

### Friction Log

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| Clean execution — 1/1 story autonomous, delivered in 1 EPIC; 0 delegations; 0 escalations; 0 deviations; 0 backlog returns (mid-sprint); `delegation_log.md` was not needed. Sprint goal 100% achieved for the amended scope. | Phase 3 | A | monitor | Continue pattern — the amendment-before-seal path (blocking Design-Gate-blocked stories pre-sprint rather than discovering the gap mid-execution) kept this execution phase itself friction-free. No action required. | PMO Lead | — |

**Recurrence Notes:**
None carried forward. v7.2's Phase 3 friction item (LL-v7.2-P3-01, stale local state at session start) was resolved via its own action-now patch during v7.2's post-ship closure and did not recur this cycle — see "What went well" above.
