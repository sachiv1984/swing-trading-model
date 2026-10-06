Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-06
Cycle: 2026-09-30__release-v9.9

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-09-30__release-v9.9
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-10-06
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-09-28__release-v9.8 (`lessons_learnt_cycle.md` `## Phase 3`). It filed 2 friction items, and each was re-checked against `prompt_change_log.md` as of this run, searching by patch scope and reading the named target files directly:
1. **`execution_state.json` summary-field staleness.** This was escalated at v9.8, its 2nd carry. **Applied this cycle:** `execution_prompt.md` v3.80→v3.81 (2026-10-05, `ESC-CLOSE-20260930-02`, `prompt_change_log.md` row dated 2026-10-05) added §9.2 projection-recompute + 4-equality read-back and §10 step 3a pushed-commit reconciliation. The fault still showed up once after the patch: EPIC-05 PR #1892 was merged by a human at 10:06Z on 2026-10-06, after v3.81 went live, and `pr_status` was still `open` when this session started. That path is a merge made outside any engine session, so no engine write existed to recompute. The STEP 4 resume-sync caught and corrected it as designed. **Not a recurrence of the patched defect; no new action.**
2. **`claude/roadmap/*` write-scope boundary.** Deferred to PMO Lead and Head of Specs Team, with target "next cycle scoping `sprint_planning_prompt.md`'s pre-sprint classification step, or `BLG-GOV-355`'s resolution". **Recurrence, still unapplied (1st carry).** There is no `sprint_planning_prompt.md` or `execution_prompt.md` §7 change in `prompt_change_log.md` since 2026-09-30, and the same shape fired 3 times this cycle (Friction Item 2 below). Under §3.7 this is a recurrence with an open prior outstanding action, so it is escalated to Head of Specs Team and not re-recorded as a fresh action.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| EPIC-02's branch was cut on top of the EPIC-04/EPIC-05 linear history rather than from `main`. Merging PR #1886 therefore also merged 19 other-EPIC commits into `main` (12 `[EPIC-04]`, 7 `[EPIC-05]`), which bypassed those EPICs' STEP 4 merge gate and broke the CLAUDE.md §2 branch-matching rule. Recovery took a retroactive gate for 2 EPICs: post-hoc `qa_evidence_EPIC-04/05.md`, agent-mediated DoQ, Product Owner acceptance through 2 more PRs, and 3 CLAUDE.md §8 conflict resolutions. STEP 2 step 3 ("verify it is based on `main`") passes a branch based on `main` *plus* unrelated commits, and no pre-PR step checks the branch's actual commit set. Blast radius: 2 EPICs and 9 stories ungated on `main` for ~1 day; recovery cost ~1 session; propagation path is the PR merge diff. | Phase 3 | Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced | defer | `execution_prompt.md` STEP 3.2.B: add a hard pre-PR check, `git log origin/main..HEAD --format='%H %s'`, that halts if any commit carries an `[EPIC-yy]` tag other than this EPIC's (`[GOVERNANCE]` merge-resolution commits excepted). Optionally mirror it in `quality_gate.yml`. Filed as `BLG-GOV-368` (P2). | Head of Specs Team | Next cycle scoping `execution_prompt.md` (`BLG-GOV-368`) |
| The `claude/roadmap/*` / existing-`backlog.md`-item write-scope boundary fired 3 more times this cycle. ESC-EXEC-20261001-01 (ST-24, existing `backlog.md` gate-criteria fields), -04 (ST-26, `claude/roadmap/role_share_history.md`) and -05 (ST-31, `current_roadmap.md` SI-02 field) each needed a one-off Head of Specs Team write-scope ruling, and each AC named the exact target file. Sprint Planning also classified ST-24 and ST-31 `autonomous` despite both needing out-of-scope writes. Blast radius: 3 stories blocked ~4 days (2026-10-01→2026-10-05); recovery cost 3 rulings; propagation path is sealed AC → §7 write-scope halt. | Phase 3 | Type E — Authority Gap: A decision was needed and no role was clearly empowered to make it | defer | No prompt change applied this run. The concrete proposal is filed as `BLG-GOV-362`: widen `execution_prompt.md` §7's BLG-GOV-337 exception to a general "sealed AC names this exact file/field" rule, and/or add a `sprint_planning_prompt.md` pre-seal check that classifies such ACs `delegated_decision` with a RISK entry. **Escalated per §3.7** (recurrence of v9.8 Friction Item 2, with its prior deferred patch still unapplied). | Head of Specs Team; PMO Lead | Escalated, not a fresh target. `BLG-GOV-362` ruling due before the next `plan sprint` seal |
| All 5 escalations this cycle (ESC-EXEC-20261001-01..05) were resolved 1–3 days after their SLA (24h Lifecycle ×3, 72h Human-Delegation/Strategy ×2). No session ran 2026-10-02→2026-10-04, and the §-1.2A SLA-breach advisory only fires when `run sprint` is invoked, so nothing reached a human during the gap. All were non-blocking and all were resolved in one session on 2026-10-05 once the user directed role-mediated resolution. Blast radius: 7 stories (ST-19/20/24/26/29/30/31) idle ~3 days; recovery cost was low (one session); propagation path is an open escalation that is invisible between sessions. | Phase 3 | Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced | defer | `shared_standards.md` §16.4.1 (SLA-breach surfacing): consider a scheduled reminder (e.g. extend `.github/workflows/sprint_close_reminder.yml`, or a daily workflow that reads `.claude_current_state.json.open_escalations`) that posts or notifies when an `Open` escalation passes `sla_due_utc`, so a breach surfaces without waiting for the next engine invocation. | PMO Lead | Next lifecycle audit (`run audit`, due at cycle count 87) |

**Recurrence Notes:**
Friction Item 2 is a confirmed §3.7 recurrence escalation: v9.8 Phase 3 Friction Item 2, 1st carry, prior deferred patch unapplied with no `prompt_change_log.md` entry. It is escalated to Head of Specs Team per the table below. Friction Items 1 and 3 are new this cycle. v9.8's Friction Item 1 (summary-field staleness) is resolved by `execution_prompt.md` v3.81. Its one post-patch instance, a human-performed merge outside any engine session, was caught by the designed STEP 4 resume-sync backstop and is not a recurrence.

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|-----------------|---------------------------|---------------|
| `claude/roadmap/*` / existing-`backlog.md`-item write-scope boundary needs a per-story ruling whenever a sealed AC names such a file | 2026-09-28__release-v9.8 (earlier single instances at v9.7 and v8.5, per `BLG-GOV-362`) | Deferred to PMO Lead; Head of Specs Team: `sprint_planning_prompt.md` pre-sprint classification check or `BLG-GOV-355` resolution. Unapplied after 1 carry. Proposal now consolidated in `BLG-GOV-362` | Head of Specs Team |

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-09-30__release-v9.9
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-10-06
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-09-28__release-v9.8 (`lessons_learnt_cycle.md` `## Phase 4`). It filed 2 friction items. Both were re-checked against the current state of `prompt_change_log.md`, searching by patch scope and reading the named target files directly (`LL-v8.6-P4-01b`, `BLG-GOV-312`, `LL-v9.1-Closure-01`).
1. **Known Deviations sync scope for QA-evidence `Pass_with_deviation` items.** **Applied:** `delivery_verification_prompt.md` v3.12→v3.13 (2026-10-05, `ESC-CLOSE-20260930-03`, Option b plus a narrow exception), with a companion change in `post_ship_closure.md` v2.36→v2.37. It was exercised cleanly this run. ST-01's `Pass_with_deviation` was read as exempt directly from the prompt text, with no interpretation needed. Closed.
2. **The agent-mediated signer-format mandate is missing from `execution_prompt.md` §3.2.A.** Filed at v9.7 and carried at v9.8; this run is the 2nd carry.
   - The named target file was read directly. `execution_prompt.md` has no explicit mandate.
   - The substance already exists elsewhere. `claude/system/templates/qa_evidence_template.md`'s "Agent-mediated provenance requirement (v7.5 Phase 4 LL, applied v7.5 post-ship closure)" requires `Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)` and reserves the literal `Director of Quality` string for a human. `execution_prompt.md`'s pre-merge sign-off format lint (`LL-v9.3-P4-01`) validates against the recognised formats.
   - The symptom has not recurred for 2 consecutive cycles. All 6 v9.9 signer fields match their actual review method.
   - This meets §3.7's mechanical ≥2-carry trigger, so it is escalated below. The recommendation is to close it as already covered by the template rule.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `delivery_verification_prompt.md` STEP 2.3 requires a `Pass_with_deviation` comment to name "the confirmed backlog item tracking" the remaining gap. That assumes a remainder always exists. ST-01's narrowing (AC-1 "1 canonical source across all 4 files") was fully disposed of by an Owner ruling (RISK-01, `st01_atr_consolidation_ruling.md`): the formulas are deliberately distinct, so nothing is left to implement. The evidence comment correctly cited the ruling record instead of a backlog item. The prompt has no stated path for this "narrowed by ruling, no remainder" shape, so the verifying engine had to construct the reading and ask the DoQ to confirm it at §9. A secondary point: the evidence comment called the narrowing permitted by the AC, but the "per the Owner's ruling" carve-out sits on AC-4 (cadence), not on AC-1 (count). | Phase 4 | Type B — Semantic Mismatch: The same concept was named or interpreted differently across documents or roles | defer | Recorded as a §3 advisory, accepted at agent-mediated DoQ sign-off. Recommendation for Head of Specs Team: extend STEP 2.1/2.3 so a `Pass_with_deviation` whose gap is fully disposed of by a recorded Owner/authority ruling can cite that decision record in place of a backlog item. Alternatively, require such items to be recorded as `Pass with notes`. | Head of Specs Team | Next `delivery_verification_prompt.md` revision touching STEP 2.1/2.3 |
| `execution_prompt.md` §3.2.A has no explicit agent-mediated signer-format mandate. Carried from v9.7; this is the 2nd carry, with no `prompt_change_log.md` entry. The substance is already enforced by `qa_evidence_template.md` (v7.5 provenance requirement) and the `LL-v9.3-P4-01` pre-merge lint. No symptom for 2 consecutive cycles. | Phase 4 | Type B — Semantic Mismatch: The same concept was named or interpreted differently across documents or roles | escalate | §3.7 recurrence escalation (≥2 carries without a `prompt_change_log.md` entry). Recommend that Head of Specs Team close it as already covered by the template rule, or add a one-line cross-reference from §3.2.A to the template rule. Either option stops the item being carried mechanically. | Head of Specs Team | Next post-ship closure (`2026-09-30__release-v9.9`) |

**Recurrence Notes:**
Gate sequencing was clean.
- All 6 QA evidence logs were signed and dated before invocation, including the two retroactive-gate EPICs (04, 05), whose PO acceptance landed on 2026-10-06 shortly before sprint close.
- The pre-seal gate (`LL-v2.4-DV-01`) held. The report was assembled with blank §9 dates, and the run went no further until the user was asked (`AskUserQuestion`) and chose agent-mediated DoQ and PO sign-off (2026-10-06).

No severity calls were contested: 0 P0/P1/P2, with one P3-default `Pass_with_deviation`.

The 4 test-coverage weaknesses were all caught and backlogged by the cycle's own PR reviews (`BLG-QA-204`/`210`/`212`/`213`) before verification. Verification only had to register them, which is a positive pattern.

The cross-EPIC merge through PR #1886 is the cycle's main process deviation. It is a Phase 3 friction item (Phase 3 Friction Item 1, `BLG-GOV-368`) and is not re-recorded here.

New this phase: the `Pass_with_deviation` "no remainder" path. v9.8 Phase 4 Item 1 is closed (v3.13). v9.8 Phase 4 Item 2 is escalated under the §3.7 ≥2-carry rule.

## Recurrence Escalations — Phase 4

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|-----------------|---------------------------|---------------|
| Agent-mediated signer-format mandate absent from `execution_prompt.md` §3.2.A | 2026-09-23__release-v9.7 (Phase 4) | Deferred to Head of Specs Team: "next `execution_prompt.md` revision touching §3.2.A". Unapplied after 2 carries (v9.8, v9.9), but its substance already exists in `qa_evidence_template.md` | Head of Specs Team. Recommend closing as already covered |
