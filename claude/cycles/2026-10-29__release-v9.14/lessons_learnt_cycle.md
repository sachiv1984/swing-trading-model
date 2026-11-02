Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-02
Cycle: 2026-10-29__release-v9.14

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-10-29__release-v9.14
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-11-02
**Reviewed by:** PMO Lead
**Invocation context:** invoking_routine `execution_prompt.md` (STEP 5.4); cycle_id `2026-10-29__release-v9.14`; phase Phase 3; prior_cycle_id `2026-10-16__release-v9.13`.
**Prior cycle checked:** 2026-10-16__release-v9.13 (`lessons_learnt_cycle.md` `## Phase 3`). It filed 4 friction items. Each was re-checked by patch ID against `prompt_change_log.md` as of this run, and by reading the named target file directly (BLG-GOV-312, LL-v9.1-Closure-01):
1. **Pre-commit OpenAPI check reads the working tree (target `scripts/check_local_openapi_contract_completeness.py`).** **Applied:** ST-31 (`f1474aa4`, BLG-QA-238) added `--staged` mode, and `.githooks/pre-commit` passes it. Every EPIC-05 commit after `f1474aa4` ran the hook against staged content. **Resolved; not a recurrence.**
2. **`commit-check` skill row vs §3.2.B (target `.claude/skills/lessons_learnt.md`).** **Applied:** the 2026-04-28 row now reads "Open the PR at EPIC completion, once the DoQ sign-off `Date:` is set ... Do not open it after every push", corrected 2026-10-29 at the v9.13 post-ship closure. Each PR this cycle was opened after its DoQ sign-off. **Resolved; not a recurrence.**
3. **Post-merge ACs graded as deviations (`LL-v9.13-P3-03`, target `sprint_planning_prompt.md` STEP 6.2).** **Applied:** `sprint_planning_prompt.md` v3.22→v3.23 (2026-10-29). Six stories had seal-marked post-merge ACs this cycle (ST-01, ST-23, ST-39, ST-42, ST-43, ST-45). All were graded on their in-sprint ACs, so `Pass_with_deviation` fell from 6 stories (v9.13) to 2. **Resolved; not a recurrence.**
4. **`deviations_filed` and the escalation map not checked mechanically (target `scripts/check_execution_state_consistency.py` with `execution_prompt.md` §9.2).** **Applied:** ST-44 (`d6a4892d`, BLG-GOV-397), `execution_prompt.md` v3.90. Both fields were correct at this close, with no hand correction. **Resolved; not a recurrence.**

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `scripts/check_execution_state_consistency.py` derives `merge_gate.epics_pending` from the EPICs already in `execution_state.json`. This cycle initialised EPICs one at a time at their own STEP 0, as v9.13 did. So from EPIC-01 to EPIC-06, the script expected `epics_pending: []` and `all_merged: true` while later EPICs were still unstarted. The engine kept `epics_pending` from `merge_order` and overrode the finding deliberately at every persist. The same fix was then filed twice: `BLG-QA-240` (2026-10-30) and `BLG-GOV-401` (2026-11-02, ST-44). **Blast radius:** a session that trusted the script would have set `all_merged: true` and run STEP 5 Sprint Close with EPICs unmerged; this would have surfaced at the next `run sprint` after any persist; recovery cost medium (unwinding a premature close record and seal). | Phase 3 | B | defer | **Deferred patch:** File `scripts/check_execution_state_consistency.py`, section: the `merge_gate` check. When `merge_order` is present, expect `epics_pending` = `merge_order` minus the EPICs with `pr_status: merged`, not the initialised EPICs minus merged. Add a test with one EPIC initialised and merged and three not yet initialised. Update `execution_prompt.md` §9.2 (Mechanical form) to match, under the CLAUDE.md §6 checklist. `groom backlog` should fold `BLG-GOV-401` into `BLG-QA-240`. | Head of Specs Team | Next Sprint Execution run (the cycle after `2026-10-29__release-v9.14`) |
| The human merge-gate confirmations (Director of Quality QA sign-off, Product Owner acceptance) were recorded three different ways. EPIC-02, EPIC-06 and EPIC-07 have a `## Merge Gate Confirmations` section in their QA evidence. For EPIC-01 and EPIC-03, the confirmations are on the PR only, and the process notes point to them. For EPIC-04 and EPIC-05, the only PR review is the agent-mediated one, which §5.3 says never satisfies the always-human rows. The human developer's merge is therefore the only record. Neither STEP 4 nor STEP 5.1 says where these confirmations must be written, or what to record when a human merges before giving them. **Blast radius:** delivery verification and audit cannot show from the cycle folder that the always-human gate was met for 4 of 7 EPICs; this would surface at Phase 4 or the next lifecycle audit; recovery cost low per EPIC (reconstruct from PR history), medium if a confirmation cannot be reconstructed. | Phase 3 | C | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, sections STEP 4 (merge gate, including the resume-sync) and STEP 5.1. Require a `## Merge Gate Confirmations` section in every `qa_evidence_EPIC-xx.md`, written by the time the merge is recorded. It names the human QA sign-off and PO acceptance (who, where, when) and the merge (who, when, merge commit). If a human merged with no separately recorded confirmation, the section says so. STEP 5.1 checks that the section exists for every EPIC in `epics_merged`. Whether a merge alone satisfies the gate is escalated below. | Head of Specs Team | Next Sprint Execution run (the cycle after `2026-10-29__release-v9.14`) |
| During EPIC-01, the engine ran the production build, commit and push for ST-07/ST-08 as one chained command, without gating on the build result. `d83893b3` failed the new Frontend Production Build on `import/first`. `3fbfe5e3` was pushed on top before the failure was seen. It was fixed in `8f05e704` after a clean local `npm ci` and build. The §3.1.A step 4d CI check stopped either story reaching `done` on a red run. **Blast radius:** a broken frontend build on the EPIC branch blocks the staging deploy and every later story's CI; caught at the next CI run on the branch; recovery cost low (one fix commit). | Phase 3 | D | defer | **Deferred patch:** File `claude/system/execution_prompt.md`, section §3.1.A (autonomous item steps, before the commit step). For any commit touching `src/**`, `package.json` or `package-lock.json`, run `CI=false npm run build` as its own command and commit only after it exits 0. Never chain it with `git commit` or `git push`. | Head of Specs Team | Next Sprint Execution run (the cycle after `2026-10-29__release-v9.14`) |

**What worked well:**
- All four v9.13 Phase 3 deferred patches had shipped before or during this cycle, and each worked live. These were the staged-content pre-commit hook, the skill-file PR timing, the seal-marked post-merge ACs and the two new consistency checks. No `deviations_filed` or escalation-map correction was needed at close.
- Seal-marked post-merge ACs (LL-v9.13-P3-03) cut `Pass_with_deviation` grades from 6 to 2. Three of the six post-merge tracking items (BLG-OPS-200, BLG-OPS-202, BLG-SEC-44) closed within a day of their EPIC merging, as did BLG-OPS-203 and BLG-OPS-204.
- All five escalations were human rulings given in-session by the user. The longest took 54 minutes from raise to resolve, and every one was mirrored in both escalation maps.
- Running the EPICs one at a time again meant no cross-EPIC merge resolution. Planning the merge order put the route-removal chain (ST-22 before ST-28) and the PVR change (ST-24 before ST-48) in sequence by construction.
- Four of six delegations were unblocked within a day, two of them in-session: the Render dashboard workaround (ST-01) and the staging visual check (ST-30).

**Recurrence Notes:**
None against the prior cycle's Phase 3 friction items. All four v9.13 Phase 3 deferred patches are dispositioned **Applied** above, so no prior-cycle row is left without a disposition (AUD-2026-10-08-004 row-completeness). Friction Item 1 is new, although the script's `merge_gate` check has existed since v9.12 (ST-41). v9.13 recorded "exits 0 each time", so the one-at-a-time initialisation first produced this false positive here. Friction Item 2 has no prior filing. v9.13's EPIC-04 and EPIC-05 recorded human confirmations in their QA evidence, so the gap is new this cycle. Friction Item 3 has no prior filing.

## Recurrence Escalations

None.

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| Does a human developer's merge, with no separately recorded Director of Quality QA sign-off or Product Owner acceptance, satisfy the always-human merge-gate rows (`execution_prompt.md` §5.3, CLAUDE.md §2)? It occurred for PR #2137 (EPIC-04) and PR #2139 (EPIC-05) | Authority ambiguity | Head of Specs Team, Product Owner | Friction Item 2's patch makes such merges visible, but whether they meet the gate is an authority ruling the engine cannot make |

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Three P2 pre-existing defects were found this cycle: `BLG-FE-239` and `BLG-FE-240` (win rate, ST-50) and `BLG-FE-243` (UTC date prefill, PR #2139 review). The Product Owner recommended the first two for v9.15 | Weigh all three for the v9.15 slice, and record a reason if any is left out | Release Planning |
| 2 | ST-53 produced `docs/governance/governance_overhead_audit_2026-11-02.md` as an input to the next roadmap rebalance (AC 2). Per ST-53's Notes, nothing was written to `claude/roadmap/*` in-sprint | Link the audit as an input at the next `run roadmap` | Roadmap |
| 3 | Three post-merge remainders stay open at close. `BLG-OPS-201` needs a complete production month (November 2026, so after 2026-12-01). `BLG-GOV-399` needs a production read of AI outputs. `BLG-GOV-400` needs the next Release Planning gate scan | Check them at the next delivery verification and Release Planning, and do not re-grade ST-23, ST-39 or ST-45 for them | All |
