**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-07-17
**Amendment ID:** AMD-20260717-01
**Original Cycle:** 2026-07-17__release-v7.4

# Amendment Lessons — AMD-20260717-01

**Note:** `amendment_cycle_prompt.md` is v1.9; this standalone record is produced for backward compatibility only. The canonical record is the `## Amendment — AMD-20260717-01` section in `claude/cycles/2026-07-17__release-v7.4/lessons_learnt_cycle.md`.

## What caused the emergency

`run design-gate --cycle 2026-07-17__release-v7.4` (2026-07-17) found ST-02/03/04/05 (`BLG-FE-115/116/117/118`) had no approved design artefact. Three had artefact production scheduled inside EPIC-01/ST-01 — sprint-execution work sequenced after Sprint Planning seals, which structurally cannot satisfy a gate required to clear before Sprint Planning. The fourth (price alerts, EPIC-03) had no design-artefact production scheduled anywhere in the v7.4 plan at all. This left 4 of 5 sprint items confirmed undeliverable within this Sprint Planning pass, per `design_gate_prompt.md` STEP 3's hard rule.

## Was the amendment process proportionate and efficient?

Yes. The alternative (fabricating four UX artefacts, including one — price alerts — with zero prior design input, outside Head of UX & Design's authority) would have been a larger governance violation than a scope-reduction amendment. Removing the four blocked items and retaining only the already-cleared EPIC-01/ST-01 is the minimal change that unblocks Sprint Planning without overriding the design gate's intent.

## Process improvements for earlier detection

- Release Planning should flag, at scoping time, any Design Required item whose artefact production is scheduled as an in-sprint deliverable rather than a pre-sprint one — this is a Design Gate failure waiting to happen, detectable before the release plan even publishes.
- `BLG-FE-116` (price alerts) should have had its own §13-style pre-check flag extended to cover "design artefact scheduled: yes/no" so gaps like this surface at roadmap/backlog grooming time, not first at Design Gate.

## Improvements to Release Planning's readiness checks

Recommend a new release-planning check: for every item classified (or likely to be classified) Design Required, confirm its design-artefact production is either (a) already complete, or (b) explicitly scheduled as pre-Sprint-Planning work — not merely referenced inside another sprint story's acceptance criteria. Filed as a candidate backlog item (see `lessons_learnt_cycle.md` Amendment section, friction item C).
