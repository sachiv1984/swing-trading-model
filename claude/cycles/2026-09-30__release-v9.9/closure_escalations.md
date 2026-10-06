Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-06 (ESC-CLOSE-20261006-01 disposition set to Resolved — Head of Specs Team named-file ruling at v9.10 sprint planning)
Cycle: 2026-09-30__release-v9.9

---

# Closure Escalations — 2026-09-30__release-v9.9

Format per `claude/system/shared_standards.md §4`.

---

## ESC-CLOSE-20261006-01

| Field | Value |
|-------|-------|
| Issue | `lessons_learnt_cycle.md` Phase 3 Friction Item 2 (`2026-09-30__release-v9.9`). The `claude/roadmap/*` / existing-`backlog.md`-item write-scope boundary fired 3 more times this cycle (ESC-EXEC-20261001-01, -04, -05: ST-24, ST-26, ST-31). Each sealed AC named the exact target file, yet each needed a one-off Head of Specs Team write-scope ruling, and 3 stories sat blocked ~4 days. This is a `lessons_learnt_prompt.md §3.7` recurrence: v9.8 Phase 3 Friction Item 2 was deferred at the v9.8 closure, and its patch is still unapplied after 1 carry, with no `prompt_change_log.md` entry. The same boundary also keeps the v9.8 Release Planning Friction Item 3 `workforce_capacity.md` worked example unwritten (2nd carry), because Post-Ship Closure's §5 write scope does not name that file either. |
| Type | Recurrence escalation (`§3.7` mandatory) — authority gap |
| Escalated to | Head of Specs Team (with PMO Lead) |
| Reason | The concrete proposal already exists as `BLG-GOV-362`: widen `execution_prompt.md` §7's BLG-GOV-337 exception to a general "the sealed AC names this exact file/field" rule, and/or add a `sprint_planning_prompt.md` pre-seal check that classifies such ACs `delegated_decision` with a RISK entry. Choosing between those options, and setting how far the exception reaches, is a write-scope authority decision, not a mechanical text fix, so this closure cannot apply it. A ruling is needed before the next `plan sprint` seals, or the same per-story rulings will recur. |
| Tracking | SLA 2026-10-09 (72h from filing). Backlog: `BLG-GOV-362`. |
| Disposition | Resolved — 2026-10-06 |
| Resolved by | Head of Specs Team: the user gave the ruling under that role, with the role checked per the CLAUDE.md §2 role-ownership rule, during `plan sprint` for `2026-10-06__release-v9.10` |
| Resolution | `BLG-GOV-362`'s principle is adopted as a **named-file rule**: Sprint Execution may write a `claude/roadmap/*` file in-sprint when a sealed AC names that exact file, within what the AC names. The existing prioritisation, scope and capacity exclusions still apply. Proposal 2 is applied as practice from v9.10: a story whose AC names such a file is classified `delegated_decision` with a RISK entry at the seal (v9.10 ST-20, RISK-03). **Not covered:** edits to fields of existing `backlog.md` items, and Release Planning §1.3a's in-place gate-text edits. Both stay out of scope until `BLG-GOV-362`'s prompt patches ship. The `execution_prompt.md` §7 and `sprint_planning_prompt.md` text changes ship through `BLG-GOV-362` with the CLAUDE.md §6 checklist. The `workforce_capacity.md` worked example (2nd carry) is not unblocked by this ruling: its blocker is Post-Ship Closure's own write scope, so it stays with `BLG-GOV-362`. Full record: `claude/cycles/2026-10-06__release-v9.10/sprint_planning_notes.md` § Pre-Sprint Required Decisions. |
