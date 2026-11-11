Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-11 (ESC-CLOSE-20261111-01 Resolved — release_planning_prompt.md v2.74); prior — 2026-11-11 (ESC-CLOSE-20261111-01 filed)
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
| Disposition | Resolved — 2026-11-11T17:15:20Z |
| Resolved by | Head of Specs Team, with the Product Owner (agent-mediated per `execution_prompt.md` §5.3, on explicit user direction 2026-11-11: "reslove ESC-CLOSE-20261111-01 with relevant agent"; role ownership checked per the CLAUDE.md §2 role-ownership rule: this escalation's owners are the Head of Specs Team and the Product Owner) |
| Resolution | **Option (a): a current-phase tier in §1.4c.** `release_planning_prompt.md` v2.74 adds step 1b. After the P1/P2 items and step 1a, it seats every ready P3/P4 item listed in the programme phase whose provisional release is this release (and any earlier unfinished phase), in ascending ID order, while capacity remains. It is the counterpart of step 0's hold: step 0 keeps later phases out, step 1b brings the current phase in, so the release named for a phase ships that phase without a per-release override. Option (b) was rejected because it repeats the v9.16 override every cycle, which is the friction being fixed. Option (c) was rejected because the DL-088 phases are sized to fit one release (Phase 3 ≈20.5d against the ~24–28d band), so a cap adds a parameter with no current case. The Product Owner keeps a dated per-item override, and gated or not-ready items are never seated by this step. First use: `plan release v9.17` (Phase 3: `BLG-FE-257`–`259`, `261`–`263`, `265`; `BLG-FE-260` is P2 and seats at step 1). CLAUDE.md §6 checklist applied: `OPERATIONAL_GUIDE.md` v4.259, `prompt_change_log.md`, `release_planning_changelog.md`. |
| Filed | 2026-11-11T16:55:20Z |
