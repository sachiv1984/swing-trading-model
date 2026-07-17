Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-17

## ESC-20260717-01

- **Raised at:** 2026-07-17T13:00:00Z
- **Routine:** Release Planning
- **Cycle ID:** 2026-07-17__release-v7.4
- **Step:** Design Gate — STEP 1/2 (Item Classification / Artefact Review)
- **ST/EPIC item:** ST-02 (BLG-FE-115, EPIC-02), ST-03 (BLG-FE-116, EPIC-03), ST-04 (BLG-FE-117, EPIC-04), ST-05 (BLG-FE-118, EPIC-05)
- **Trigger type:** Lifecycle
- **Blocking statement:** 4 of 5 v7.4 sprint items are classified Design Required with no approved design artefact and no updated frontend spec. Three of the four (EPIC-02/04/05) have artefact production scheduled inside EPIC-01/ST-01's own acceptance criteria, but ST-01 is itself sprint-execution work sequenced *after* Sprint Planning seals — it cannot satisfy a gate that must clear *before* Sprint Planning. The fourth (EPIC-03, price alerts) has no design-artefact production scheduled anywhere in the v7.4 plan.
- **Owning authority:** Head of UX & Design (artefact production), Product Owner (scope/sequencing remedy)
- **Unblock criteria:** Either (a) approved design artefacts + updated frontend specs are produced for all four items and design gate is re-run, or (b) the release plan is amended (via `amend cycle`) to descope EPIC-02/03/04/05 from this Sprint Planning pass — e.g. a phased plan scoping Sprint 1 to EPIC-01 only, with EPIC-02–05 gated behind a follow-up `run design-gate` pass once ST-01 ships.
- **SLA due-by:** 2026-07-18T13:00:00Z (24 hours — Lifecycle/Process Integrity)
- **Blocks execution:** Yes
- **Disposition:** Open
- **Resolution summary:** —
