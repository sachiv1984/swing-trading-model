Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-29 (ESC-CLOSE-20261029-01 and ESC-CLOSE-20261029-02 filed — strategy_rules.md write routes)
Cycle: 2026-10-16__release-v9.13

---

# Closure Escalations — 2026-10-16__release-v9.13

Format per `claude/system/shared_standards.md §4`.

---

## ESC-CLOSE-20261029-01

| Field | Value |
|-------|-------|
| Issue | STEP 5 found two `strategy_rules.md` Known Deviations entries that this routine cannot write. (1) `BLG-BE-190` (P2, ST-14 found defect, accepted by PO + DoQ on 2026-10-29) has no entry. `verification_report.md` §4 routed it to Post-Ship Closure STEP 5, and adding the entry is a written condition of the acceptance. (2) The ST-05 §8.4 entry ("Known deviation (v1.17)") has a description and canonical requirement, but no Priority, Target resolution release, Owner or backlog ID. It says only "Tracked in the backlog", where the item is `BLG-BE-187`. |
| Type | Write-scope conflict — decision required |
| Escalated to | Strategy Rules & System Intent Owner |
| Reason | STEP 5's deviation-compliance carve-out allows canonical-spec edits, but `post_ship_closure.md` §5 lists `claude/strategy/strategy_rules.md` as sealed for this routine, and CLAUDE.md §2 forbids edits to `claude/strategy/` unless the prompt instructs them. The edit would also make the file v1.19, and `tests/test_strategy_version_registry.py` then requires `"1.19"` in `DOCUMENTATION_ONLY_VERSIONS` in `backend/strategy_version_registry.py`, a code change outside this routine's scope. The user chose to escalate rather than edit (2026-10-29). |
| Proposed entry text | **Under §4.1.5:** "Known deviation (v1.19): US position sizing in `sizing_service.py` `size_position()` multiplies the stop distance by the GBP/USD rate instead of dividing, so US share counts are wrong in proportion to the FX rate squared. Canonical requirement: §4.1.2 risk basis in GBP, with native-currency prices converted at the effective FX rate (§4.1.5). Priority: P2. Target resolution: v9.14. Owner: Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner. Backlog: `BLG-BE-190`." **§8.4 bullet completed:** "... the backtest does. Priority: P3. Target resolution: TBD. Owner: Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner. Backlog: `BLG-BE-187`." |
| Options | (a) Apply both entries as a documentation-only v1.19, registering 1.19 in `DOCUMENTATION_ONLY_VERSIONS`, as a standalone `[GOVERNANCE]` commit. (b) Fold both into `BLG-BE-190`'s v9.14 fix, which already scopes stating the US formula in `strategy_rules.md`. The deviation stays undocumented in the spec until then. (c) Authorise a named post-ship write for this class of entry. The standing rule for future cases is `ESC-CLOSE-20261029-02`. |
| Tracking | SLA 2026-11-01T12:12:02Z (72h from filing). Related: `verification_report.md` §4 acceptance conditions, `closure_record.md` §6 row 1, `BLG-BE-190`, `BLG-BE-187`. Non-blocking: `BLG-BE-190` stays P2 for v9.14, so the next `plan release` can proceed. |
| Disposition | Open |
| Filed | 2026-10-29T12:12:02Z |

---

## ESC-CLOSE-20261029-02

| Field | Value |
|-------|-------|
| Issue | No engine except the file owner has a standing write route into `claude/strategy/strategy_rules.md`, so every cycle that needs one asks for a fresh ruling. v9.13 Release Planning Friction Item 1 (`LL-v9.13-Release-03`): `BLG-GOV-376` and `BLG-GOV-377` said in their own Problem text that Sprint Execution cannot write the file, and ST-05/ST-06/ST-07 might also need to. The question was carried as pre-sprint decision RISK-02 and settled by a one-off user ruling (named writes for ST-05/06/07/38/39). This closure hit the same wall from the other side: Post-Ship Closure STEP 5 is told to create routed Known Deviations entries, but its own §5 seals `strategy_rules.md` (`ESC-CLOSE-20261029-01`). |
| Type | Decision required — authority boundary (`post_ship_closure.md` STEP 8 `decision_required` class) |
| Escalated to | Head of Specs Team, with the Strategy Rules & System Intent Owner |
| Reason | Granting another engine write access to a §7 governance-hierarchy document is an authority decision, not a prompt fix this routine can apply. |
| Decision question | Should `strategy_rules.md` get a named-file rule, like the one `ESC-CLOSE-20261006-01` gave `claude/roadmap/*`? Under it, a sealed AC (Sprint Execution), or a Delivery Verification routing (Post-Ship Closure STEP 5, Known Deviations entries only), names the exact section. The Strategy Rules & System Intent Owner signs off, the write is classed `delegated_decision`, and the version-registry step (`DOCUMENTATION_ONLY_VERSIONS`) is part of the same commit. Options: (a) adopt it for both engines; (b) adopt it for Sprint Execution only, and route Known Deviations entries to the owner by default; (c) keep per-cycle rulings. |
| Proposed vehicle | If (a) or (b): `execution_prompt.md` §7 and `post_ship_closure.md` §5/STEP 5 under the CLAUDE.md §6 checklist, applied by the Head of Specs Team or filed via `/backlog-add` with a sprint target (`post_ship_closure.md` STEP 8, `LL-v9.12-Release-01`). |
| Tracking | SLA 2026-11-01T12:19:42Z (72h from filing). Related: `ESC-CLOSE-20261029-01`, v9.13 `sprint_planning_notes.md` RISK-02, `closure_record.md` §6 row 2. Non-blocking: per-cycle rulings still work. |
| Disposition | Open |
| Filed | 2026-10-29T12:19:42Z |
