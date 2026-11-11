Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-11 (ESC-CLOSE-20261111-01 filed)
Cycle: 2026-11-06__release-v9.16

---

# Closure Escalations — 2026-11-06__release-v9.16

Format per `claude/system/shared_standards.md §4`.

---

## ESC-CLOSE-20261111-01

| Field | Value |
|-------|-------|
| Issue | Release Planning Friction Item 1 (`LL-v9.16-Release-01`). `release_planning_prompt.md` v2.72 §1.4c step 0 holds out the later phases of a DL-recorded programme, but gives the current phase's P3/P4 items no tier. At v9.16, the oldest-first round-robin would not have reached Phase 2's P3 items `BLG-FE-251`, `252` and `253`, and the Product Owner had to seat them by override so Phase 2 shipped in the release named for it. The same will recur at v9.17 for Phase 3's six P3 items (`BLG-FE-257`–`263`, `265`, less the P2 `BLG-FE-260`). |
| Type | Decision required (`post_ship_closure.md` STEP 8 `decision_required` class): a change to §1.4c's selection order, which is a prioritisation rule |
| Escalated to | Head of Specs Team, with the Product Owner |
| Reason | Seating a phase's P3/P4 items ahead of other P3/P4 work changes how the ready pool is ordered. That is a prioritisation policy, not a wording fix, so this routine cannot apply it as an immediate action. |
| Decision question | When the release being planned is the provisional release of a DL-recorded programme phase, should §1.4c seat that phase's ready P3/P4 items as a tier after P1/P2? |
| Options | (a) Yes: add a §1.4c tier, after the P1/P2 step and before the round-robin, that seats the current phase's ready P3/P4 items, the counterpart of step 0's hold. (b) No: keep a per-release Product Owner override, recorded in `run_manifest.md` as at v9.16. (c) Yes, but only up to a share of capacity (for example 50%), with the rest of the phase left to the round-robin. |
| Proposed vehicle | After the ruling, apply it under the CLAUDE.md §6 checklist, or file it via `/backlog-add` with a sprint target (LL-v9.12-Release-01). Do not set a "before `plan release`" deadline. Until it is ruled, `plan release v9.17` needs the same PO override for Phase 3's P3 items. |
| Tracking | SLA 2026-11-14T16:55:20Z (72h from filing). Related: `lessons_learnt.md` Friction Item 1, `ESC-CLOSE-20261106-02` (step 0 hold), DL-088, `closure_record.md` §5 and §6. Non-blocking. |
| Disposition | Open |
| Filed | 2026-11-11T16:55:20Z |
