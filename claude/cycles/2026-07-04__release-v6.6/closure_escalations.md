Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-06

---

## ESC-CLOSE-20260706-01

- **Raised at:** 2026-07-06T13:00:00Z
- **Routine:** Post-Ship Closure
- **Cycle ID:** 2026-07-04__release-v6.6
- **Step:** STEP 8 — Lessons Learnt Review and Application
- **ST/EPIC item:** N/A (cross-cycle governance-tooling item, not a sprint story)
- **Trigger type:** Lifecycle
- **Blocking statement:** The `/commit-check` skill's proposed diff-verification patch (diff `git add`'s staged target list against the intended file set before multi-file governance commits) has now been deferred across 3 consecutive cycles without resolution — first identified v6.4 Phase 3 (target v6.5), still unapplied at v6.5 (target reset to v6.6), and confirmed still unapplied this cycle (`.claude/skills/commit-check/SKILL.md` checked directly this session — no diff-verification step exists). No governed routine's declared write scope includes `.claude/skills/` (checked: `execution_prompt.md` §7, `post_ship_closure.md` §5 — neither lists it), so no routine can apply this patch as an in-scope immediate action. Per `lessons_learnt_prompt.md` §3.7, a deferred patch carried 2+ cycles without a `prompt_change_log.md` entry is an automatic recurrence escalation — this item crossed that threshold at v6.6.
- **Owning authority:** Head of Specs Team
- **Unblock criteria:** Either (a) Head of Specs Team applies the patch directly to `.claude/skills/commit-check/SKILL.md` outside any single governed routine (a discrete authorized edit, not a routine invocation), or (b) a routine's write scope is formally amended to include `.claude/skills/` maintenance, with that amendment itself logged in `prompt_change_log.md`.
- **SLA due-by:** 2026-07-07T13:00:00Z (24 hours — Lifecycle/Process Integrity trigger per `shared_standards.md §4`)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:** *(complete when closing; include evidence links)*
