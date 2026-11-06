Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-06 (ESC-CLOSE-20261106-01 and -02 Resolved — strategy_rules.md v1.26; release_planning_prompt.md v2.72); prior — 2026-11-06 (both filed)
Cycle: 2026-11-03__release-v9.15

---

# Closure Escalations — 2026-11-03__release-v9.15

Format per `claude/system/shared_standards.md §4`.

---

## ESC-CLOSE-20261106-01

| Field | Value |
|-------|-------|
| Issue | `verification_report.md` §4 routed `BLG-FE-271` (P2, ST-01 found gap, accepted by PO 2026-11-04 and re-confirmed by PO + DoQ 2026-11-06) to Post-Ship Closure STEP 5. Plan-linked Trade Entry does not require the WARN/FAIL acknowledgement when the plan's stored checks were WARN/FAIL. That matches `position_form.md` §Pre-Entry Checks and the locked `trade-entry-pre-entry-checks` design record (AC 3, "not shown twice"). It may contradict `strategy_rules.md` §4.2.1 v1.23, which says an unknown-regime entry "is blocked by requiring the user to acknowledge the FAIL before it can be saved". Whether a Known Deviations entry is needed depends on whether §4.2.1 covers the plan-linked route, and no ruling has been made. |
| Type | Write-scope routing (`post_ship_closure.md` STEP 5 `strategy_rules.md` owner route, `ESC-CLOSE-20261029-02` option (b)) with a scope ruling needed first |
| Escalated to | Strategy Rules & System Intent Owner |
| Reason | `strategy_rules.md` is sealed for Post-Ship Closure (§5). The entry is conditional on a ruling that only the owner can give, and that ruling is `BLG-FE-271` Scope bullet 1 and its first AC. |
| Decision question | Does `strategy_rules.md` §4.2.1 v1.23's acknowledge-before-save rule apply to a position created from a Trade Plan whose stored pre-entry checks were WARN/FAIL? |
| Proposed entry text | Only if the ruling is "applies". **Under §4.2.1:** "Known deviation (v1.2x): a position created from a Trade Plan whose stored pre-entry snapshot holds a WARN/FAIL is saved without the acknowledgement this section requires, because Trade Entry shows only the on-plan summary line for a plan-linked entry (`position_form.md` §Pre-Entry Checks; `trade-entry-pre-entry-checks` decision record AC 3). No `pre_entry_override` event is written for that route. Canonical requirement: §4.2.1, an unknown-regime or risk-off entry is blocked until the user acknowledges the FAIL. Priority: P2. Target resolution: v9.16. Owner: Strategy Rules & System Intent Owner; Frontend Specifications & UX Documentation Owner. Backlog: `BLG-FE-271`." Apply as a documentation-only version with its `DOCUMENTATION_ONLY_VERSIONS` registry entry. |
| Options | (a) Rule "applies": add the entry above as a documentation-only version; `BLG-FE-271` proceeds to its fix. (b) Rule "does not apply": state in §4.2.1 that the acknowledgement is taken on the Trade Plan form for a plan-linked entry. No Known Deviations entry is needed, and `BLG-FE-271` closes at its first AC. (c) Defer the ruling to `BLG-FE-271`'s own sprint (v9.16). The possible divergence stays undocumented in the spec until then. |
| Tracking | SLA 2026-11-09T16:18:41Z (72h from filing). Related: `verification_report.md` §4 Known Deviations Sync, `closure_record.md` §4 and §6, `BLG-FE-271`, `ESC-EXEC-20261104-01` (Branch A ruling). Non-blocking: `BLG-FE-271` is accepted P2 and targeted at v9.16. |
| Disposition | Resolved — 2026-11-06T16:51:48Z |
| Resolved by | Strategy Rules & System Intent Owner (agent-mediated per `execution_prompt.md` §5.3, on explicit user direction 2026-11-06: "act as relevant agents and close ESC-CLOSE-20261106-01 / ESC-CLOSE-20261106-02"; role ownership checked per the CLAUDE.md §2 role-ownership rule: this escalation's owner is the Strategy Rules & System Intent Owner) |
| Resolution | **Option (a): §4.2.1 applies to the plan-linked route.** §4.2.6 v1.23 already says Trade Entry applies acknowledge-to-proceed to "every route in", and a plan-linked entry is a route into Trade Entry. The Trade Plan form's acknowledgement is advisory only and writes no `pre_entry_override` event. A stored snapshot can also be stale against the live regime at entry time. The shipped v9.15 behaviour therefore diverges. Applied as documentation-only `strategy_rules.md` v1.26: a §4.2.1 Known deviation entry with all six fields (P2, target v9.16, owners, `BLG-FE-271`), a §16-template Change Log row, `"1.26"` in `DOCUMENTATION_ONLY_VERSIONS` (`tests/test_strategy_version_registry.py` passes) and a §15 re-run with 0 actionable findings. `BLG-FE-271`'s first AC (a dated ruling) is met. Its fix scope (show the panel on Trade Entry when the snapshot holds an unacknowledged WARN/FAIL or is stale, and update `position_form.md` and the design record) now applies, at v9.16. |
| Filed | 2026-11-06T16:18:41Z |

---

## ESC-CLOSE-20261106-02

| Field | Value |
|-------|-------|
| Issue | Release Planning Friction Item 1 (`LL-v9.15-Release-01`). DL-088 placed the Site Structure & Usability programme's Phase 2/3 items at v9.16/v9.17 as provisional targets. Four of them (`BLG-FE-255`, `256`, `260`, `264`; 8.5d) are P2 with no gate. `release_planning_prompt.md` §1.4c's P2-first step would seat them ahead of the Phase 1 specs they depend on. The Product Owner held them to their phases by override. The same will recur at v9.16 for `BLG-FE-260` (Phase 3 P2). |
| Type | Decision required (`post_ship_closure.md` STEP 8 `decision_required` class): two design options across two owners' prompts |
| Escalated to | Head of Specs Team, with the Product Owner |
| Reason | The fix is either a gating convention in the rebalance (`roadmap_prompt.md` STEP 8.1, recording) or a standing override in selection (`release_planning_prompt.md` §1.4c). Choosing between them changes how a DL-recorded programme binds Release Planning, so this routine cannot pick one. |
| Decision question | How should a phased roadmap programme bind §1.4c selection? |
| Options | (a) The rebalance gates each later-phase item on its phase's release (Gate criteria: "not before `plan release v9.16`"), so §1.4c needs no change. (b) §1.4c treats a DL-recorded programme phase as a standing override: an item placed in a later phase is not seated earlier without a dated PO reason. (c) Both: (a) for new programmes, plus a one-time gate write for the current programme's Phase 2/3 items at the next `run roadmap`. |
| Proposed vehicle | After the ruling, apply under the CLAUDE.md §6 checklist, or file it via `/backlog-add` with a sprint target (LL-v9.12-Release-01). Do not set a "before `plan release`" deadline. Until then, the next `plan release` needs the same PO override for `BLG-FE-260`. |
| Tracking | SLA 2026-11-09T16:18:41Z (72h from filing). Related: `lessons_learnt.md` Friction Item 1, DL-088, `closure_record.md` §5 and §6. Non-blocking. |
| Disposition | Resolved — 2026-11-06T16:51:48Z |
| Resolved by | Head of Specs Team, with the Product Owner (agent-mediated per `execution_prompt.md` §5.3, on explicit user direction 2026-11-06; role ownership checked per the CLAUDE.md §2 role-ownership rule: this escalation's owners are the Head of Specs Team and the Product Owner) |
| Resolution | **Option (b): a standing programme-phase hold in §1.4c.** `release_planning_prompt.md` v2.72 §1.4c step 0: before selection, Release Planning reads every `### Programme plan` subsection under `current_roadmap.md` §3 and holds out every P2/P3 item listed in a phase later than the release being planned. A held item is seated early only with a dated PO reason in `run_manifest.md`. P1 items are not held. Option (b) was chosen over (a) because, since `roadmap_management_prompt.md` v1.7 (BLG-GOV-406), the programme plan survives as a standing §3 subsection that Release Planning can read directly. One rule in one prompt then covers every programme, with no gate text to write on each item. (a) and (c) would need a gate edit on each of the 17 Phase 2/3 items and the same convention at every future rebalance. CLAUDE.md §6 checklist complete (OPERATIONAL_GUIDE.md v4.254). This also removes the PO override that v9.16 would otherwise need for `BLG-FE-260`. |
| Filed | 2026-11-06T16:18:41Z |
