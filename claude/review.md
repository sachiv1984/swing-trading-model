You are performing a full operational audit of the development lifecycle defined in this repository.

Primary document under review:
Sprint Planning Operational Playbook

Your objective is to determine whether the playbook and supporting prompts collectively provide a **complete, low-friction, low-token, and reliable development cycle** when executed by Claude Code agents.

You must review:

1. The full Sprint Planning Operational Playbook.
2. All referenced governance prompts under:
   claude/system/
3. Charter and governance documents:
   claude/charter/
4. Strategy constraints:
   claude/strategy/
5. Agent role definitions:
   claude/agents/
6. Shared standards and lifecycle rules.

Your goal is to identify **improvements that will:**

• Reduce execution friction for agents
• Reduce token usage across the lifecycle
• Reduce process ambiguity
• Reduce failure states
• Reduce escalation noise
• Prevent governance drift
• Ensure every phase is operationally complete
• Ensure the system remains deterministic and resumable

Focus especially on:

- Missing lifecycle coverage
- Unclear state transitions
- Redundant artefacts
- Excess document generation
- Prompt or phase overlap
- Steps that require human interpretation
- Steps that could be automated
- Steps that create unnecessary tokens
- Gaps between playbook expectations and prompt capabilities
- Any governance rule that is unenforceable in practice
- Any place where Claude could accidentally violate a hard rule

---

## Token Efficiency Audit (Primary Focus)

Token efficiency is a first-class concern. Treat it with equal weight to correctness and governance.

For every phase and every prompt, audit:

**1. Prompt Loading Scope**
- Which files does each engine load at STEP -1 / STEP 0?
- Are all loaded files actually read or referenced in subsequent steps?
- Flag any file loaded "for context" but never cited in a decision or output.
- Recommend lazy loading or per-step scoping where a file is only needed at one step.

**2. Artefact Read Redundancy**
- Which artefacts are read by multiple engines across phase boundaries?
- Is the same content re-parsed in full each time, or is a summary/pointer sufficient?
- Flag cases where a downstream engine reads a full artefact when only a status field or
  a single section is needed.
- Recommend structured state fields or index pointers to replace full-document reads.

**3. Output Verbosity**
- Which engine outputs are narrative prose when a table or structured list would suffice?
- Which outputs duplicate content already present in another artefact from the same cycle?
- Flag any artefact that is generated, then read back in full by the next engine, when a
  state pointer would be sufficient.
- Target line-count ceilings for the highest-volume outputs (release_plan.md, backlog
  slice, sprint_backlog.md, verification_report.md).

**4. Cross-Phase Duplication**
- List every piece of information that is written to more than one artefact.
- For each: determine the canonical location and recommend removing it from secondary
  locations, replacing with a reference.
- Pay particular attention to: acceptance criteria (appear in release plan, backlog slice,
  sprint backlog), risk entries (appear in release plan and escalations), and EPIC
  descriptions (appear in release plan, backlog slice, sprint goal, sprint backlog).

**5. State File Efficiency**
- Are `.claude_current_state.json` and cycle `state.json` read in full when only one or
  two fields are needed?
- Recommend field-level read instructions in prompts where full-file reads are unnecessary.
- Flag any field that is written at one step but never read by any downstream step or engine.

**6. Lessons Learnt Token Cost**
- Three lessons learnt records are produced per cycle (Phase 1B, Phase 3, Phase 4) plus
  a closure record. All are separate prose documents read independently by Post-Ship
  Closure and meta-review.
- The resolved architecture decision is: consolidate all per-phase lessons learnt into a
  single `lessons_learnt_cycle.md` with phase-tagged structured table sections. Each phase
  appends on completion rather than generating a new document. Audit for any remaining
  gaps or implementation risks in this model.
- Meta-review runs at cycle level (every 3rd completed delivery cycle) at Post-Ship
  Closure, not at Phase 1 only. Scope covers all phases across the last 3 cycles.
  Audit for any prompts or playbook sections that still reference the old Phase 1-scoped
  meta-review model and flag them for update.

**7. Preflight Redundancy**
- Every engine runs a preflight (STEP -1). List what each preflight reads.
- Identify checks that are duplicated across consecutive engines (e.g., Phase 1B preflight
  and Phase 2 preflight both checking the same state fields).
- Recommend a shared preflight result that downstream engines can consume rather than
  re-running the same checks.

**8. GitHub Issue Sync**
- `sync gh` parses `stage4_backlog_slice.md` to create/update issues.
- The resolved architecture decision is: Phase 1B STEP 4 produces a companion
  `stage4_issue_manifest.json` for `sync gh` consumption. Audit for any remaining
  gaps or implementation risks in this model.

---

## Additional Audit Dimensions

Also check for:

1. **Prompt–Playbook Alignment**
   - Does every playbook phase have a corresponding prompt?
   - Do prompts enforce the same gates described in the playbook?
   - Are any rules declared but not enforced?

2. **State Management Integrity**
   - `.claude_current_state.json`
   - cycle `state.json`
   - lock files

   Identify:
   - race conditions
   - missing guards
   - duplicate state sources
   - unnecessary sync points

3. **Lifecycle Completeness**
   Ensure the lifecycle fully covers:

   idea → roadmap → release plan → sprint → execution → verification → closure → next cycle

4. **Failure Handling**
   Identify where the system could:

   - deadlock
   - halt unnecessarily
   - escalate too often
   - require manual recovery

5. **Agent Execution Reliability**
   Identify:

   - steps that are fragile for LLMs
   - steps likely to produce inconsistent outputs
   - steps that could drift over multiple cycles

6. **Operational Simplification**
   Suggest ways to:

   - reduce number of artefacts
   - simplify prompts
   - collapse phases where appropriate
   - reduce governance overhead while preserving safety

7. **Known Gap Review**
   Pay particular attention to:

   - the known Phase 1M trigger gap
   - amendment cycle constraints
   - design gate timing
   - backlog lock management
   - lessons learnt feedback loop
   - meta-review cadence and scope (now cycle-level at Post-Ship Closure, not Phase 1-scoped)
   - consolidated lessons learnt record consistency across phases
   - `stage4_issue_manifest.json` production and sync gh consumption

8. **Role Charter Completeness**
   - For every decision-authority role named in the playbook, confirm a corresponding agent
     charter exists in `claude/agents/`.
   - For every authority boundary declared in the playbook (veto rights, hard gate authority,
     sign-off requirements), confirm the matching agent charter grants that authority explicitly.
   - Flag any role that has authority in the playbook but whose charter is absent, incomplete,
     or grants narrower authority than the playbook assumes.
   - Flag any authority granted in a charter that is not reflected in the playbook — these
     represent undeclared powers that could be exercised without governance coverage.
   - Flag any role referenced in engine prompts that does not appear in either the playbook
     or any charter — ghost roles with no defined authority boundary.

9. **First-Cycle Correctness**
   - Every engine that reads `.claude_current_state.json` must handle the case where the file
     does not yet exist or contains null/absent fields.
   - Every engine that checks a prior cycle field (prior_cycle_id, last_meta_review_cycle,
     lessons_learnt_closure.md path, etc.) must explicitly handle the zero-state case.
   - Audit each engine's STEP -1 and STEP 0 for explicit first-cycle guards. Flag any engine
     that would fail, produce incorrect output, or silently skip a check on first invocation.
   - Pay particular attention to: Release Planning STEP -1.5 (reads prior cycle lessons learnt),
     STEP -1.6 (checks next_cycle_unblocked), Post-Ship Closure (reads prior cycle artefacts),
     and meta-review (reads last 3 cycles — what happens on cycles 1 and 2?).

10. **Mode Parity (`strict` vs `standard`)**
    - Every engine accepts `--mode strict|standard`. For each engine, audit whether the
      behavioural difference is explicitly and consistently defined.
    - For every condition that is a hard halt in strict mode, confirm the standard mode
      behaviour is one of: warn-and-proceed, warn-and-block-seal, or warn-and-escalate.
      Silent pass in standard mode is never acceptable for a governance condition.
    - Flag any condition where strict mode halts but standard mode behaviour is undefined,
      inconsistent with other engines, or more permissive than the governance rule allows.
    - Flag any condition that should always halt regardless of mode (hard gates) but is
      incorrectly mode-gated.

11. **Write Scope Enforcement**
    - The playbook declares write scope restrictions per engine (most explicitly for the
      Roadmap Engine STEP 9: "no files outside the allowed list may be modified").
    - For each engine, list: (a) the declared write scope, (b) every file the engine's steps
      actually write to, (c) any file written that is not on the declared allowed list.
    - Flag any engine that writes to a file owned by a different phase (e.g. a Phase 3 engine
      modifying a sealed Phase 1B artefact).
    - Flag any engine whose write scope is undeclared — if there is no explicit allowed list,
      the engine has unconstrained write access, which is a governance gap.
    - Flag any step that writes to `.claude_current_state.json` outside of the designated
      sync steps (STEP 7.1 and STEP 9 for Release Planning; equivalent designated steps for
      other engines).

12. **Idempotency**
    - The system is designed to be resumable. Resumability only works if re-invoking an engine
      at any step produces the same result as first invocation for that step.
    - For each engine, audit every write operation: appends to log files, state file updates,
      backlog commits, artefact creation. Flag any operation that would produce duplicate or
      corrupted output if the step were re-run.
    - Pay particular attention to: lessons learnt append operations (would re-run append a
      duplicate section?), backlog slice commit (idempotency marker — is it checked before
      write or only after?), `sync gh` (create vs update — what happens if run twice?),
      escalation log appends, and `prompt_change_log.md` entries.
    - Flag any step that is declared resumable but has no idempotency guard on its write
      operation.

13. **Cross-Document Version Consistency**
    - §14 of the playbook declares expected versions for every engine prompt and governance
      document (e.g. `release_planning_prompt.md v2.13`, `shared_standards.md v1.4`).
    - Audit whether the version numbers declared in §14 match the actual version headers in
      the corresponding prompt files.
    - Flag any divergence as governance drift — the playbook and the prompt are out of sync.
    - Flag any prompt referenced in §14 that does not exist at the declared path.
    - Flag any prompt that exists but is not listed in §14 — undeclared prompts have no
      version governance.

14. **Amendment Cycle as a Complete Sub-Lifecycle**
    The amendment cycle is currently described as a minor variant of Phase 1B. Audit it as
    a fully independent sub-lifecycle with its own correctness requirements:

    - **State completeness:** Does `amendment_state.json` define all valid states and
      transitions, or is it a partial record with gaps? Does the amendment cycle have an
      explicit state machine comparable to the main lifecycle state machine in §4.1?
    - **First-amendment correctness:** What happens on the first amendment to a cycle?
      Are there any field or path assumptions that only hold after a prior amendment exists?
    - **Lessons learnt integration:** `amendment_lessons.md` is listed in the Artefact
      Register but §6B.8 defines no step that produces it, no format, and no connection
      to the lessons learnt feedback loop (consolidated or otherwise). Flag as a
      disconnected artefact.
    - **Idempotency:** "One active amendment at a time — seal or withdraw before opening
      another" is declared. Audit whether the engine enforces this as a hard gate or
      relies on the PMO Lead to self-enforce without a machine check.
    - **Write scope:** Confirm whether the amendment engine's write scope is declared and
      whether it is permitted to write to any file beyond `amended_backlog_slice.md` and
      `.claude_current_state.json`.
    - **Mode parity:** Audit whether two-authority ratification is mode-independent (as it
      should be for a governance control) or whether standard mode can bypass or defer it.
    - **Withdrawal path:** The playbook mentions "seal or withdraw" but defines no
      withdrawal procedure — no state transition, no `.claude_current_state.json` update,
      no permanent record requirement. Flag as a lifecycle gap.
    - **Sprint Planning integration:** Sprint Planning reads `amended_backlog_slice_path`
      if present. Audit whether Sprint Planning explicitly guards the case where an
      amendment is in progress but not yet sealed — the path should be unambiguous about
      which source takes precedence at every possible amendment state.

15. **Dry-Run Output Standard**
    - Multiple engines support `--dry-run` (Post-Ship Closure, Sprint Planning, Execution,
      Phase 1M engines). No document defines what a dry-run output must contain, which
      files it may read, which files (if any) it may write, or whether it may acquire locks.
    - Audit each engine supporting `--dry-run` for: (a) files read, (b) files written
      (should be zero), (c) locks acquired (should be zero), (d) external calls made
      (should be zero), (e) output produced to confirm the planned changes.
    - Flag any engine where dry-run behaviour is undefined, or where dry-run could produce
      side effects (lock acquisition, state file writes, API calls).
    - Recommend a dry-run output standard in `shared_standards.md`: no writes, no locks,
      no external calls permitted; mandatory "dry-run complete — N changes planned, N files
      affected" summary; output sufficient for a human or downstream agent to validate
      before committing to a live run.

---

## Output Format

Return your findings as a **prioritized list of improvements only**.

For each improvement include:

Title
Area (Lifecycle | Prompt | State | Governance | Token Efficiency | Automation)
Problem
Why it matters
Recommended change
Expected benefit
Token impact (Saves | Neutral | Costs — with brief justification)
Implementation effort (Low / Medium / High)

Sort findings by a combined priority score that weights token savings and correctness
failures equally above governance clarifications and cosmetic improvements.

Focus on **practical improvements that can be implemented in this repository**.

Avoid commentary or praise.
Do not restate the playbook.

The output should read like an **engineering improvement backlog for the lifecycle system itself**.

---

## Improvement Backlog

---

### Completed

---

**IMP-01 — Post-Ship Closure has no state.json** ✅ COMPLETE (2026-03-07)
Area: State
Problem: Resumability relies on `closure_record.md` content rather than a structured state file.
Partial writes leave no reliable resume point; every other engine has `state.json`.
Why it matters: A session crash mid-closure requires manual inspection of prose to determine what
completed.
Recommended change: Add `claude/cycles/<id>/closure_state.json` with step completion flags, mirroring
the pattern used in release planning and execution.
Expected benefit: Reliable resume, deterministic halts, consistent state model across all phases.
Effort: Low
Resolution: `post_ship_closure.md` v1.3→v1.4 — `closure_state.json` schema added to STEP 0
(create/resume/already-closed logic); step completion flags written after each of STEP 0–11;
`closure_state.json` added to §4 inputs, §5 write scope, and STEP 11 commit list.
`shared_standards.md` v1.2→v1.3 — §8 resumability note updated. `prompt_change_log.md` updated.

---

**IMP-02 — Phase 1M has no lifecycle state value** ✅ COMPLETE (2026-03-07)
Area: State | Lifecycle
Problem: `manage roadmap` and `groom backlog` leave no trace in `.claude_current_state.json`. No
field records whether Phase 1M ran or when.
Why it matters: The playbook says Phase 1M is "strongly recommended" but there is no enforcement or
auditability. Future agents cannot tell if it was skipped.
Recommended change: Add `last_1m_utc` and `last_1m_outcome` fields to `.claude_current_state.json`,
written by Phase 1M engines on completion.
Effort: Low
Resolution: Per-engine fields used: `last_manage_roadmap_utc`/`last_manage_roadmap_outcome` and
`last_groom_backlog_utc`/`last_groom_backlog_outcome`. `roadmap_management_prompt.md` v1.1→v1.2:
state write added to STEP 6. `backlog_management_prompt.md` v1.1→v1.2: state write added to STEP 7.

---

**IMP-03 — Sealed hash key mismatch between schema versions** ✅ COMPLETE (2026-03-07)
Area: State | Governance
Problem: `state.json` `sealed_hashes` keys from pre-consolidation cycles (`stage2_scope_extraction`,
`stage3_execution_plan`) diverge from post-consolidation key (`release_plan`). Drift detection
behaves differently across schema versions with no transition guidance.
Why it matters: False drift or silent mismatch across cycle boundaries.
Recommended change: Add `schema_version` to `state.json`. Document drift detection uses the keys
present in `sealed_hashes` for that cycle's schema version.
Effort: Low
Resolution: `release_planning_prompt.md` v2.11→v2.12: `prompt_schema_version: "v2"` added to
state.json schema template; §18.1 tracked artifact list corrected; drift detection schema migration
table added.

---

**IMP-04 — Design gate bypass has no audit trail** ✅ COMPLETE (2026-03-08)
Area: Governance | State
Problem: `design_gate_required = false` and the `Release_Planning_Complete →
Sprint_Planning_Complete` shortcut path have no recorded authority. Any agent can set
`design_gate_required = false` without attribution.
Why it matters: Silent bypass of a required gate with no accountability.
Recommended change: Require `design_gate_bypass_authority` and `design_gate_bypass_reason` fields
in `.claude_current_state.json` when the shortcut transition is taken.
Effort: Low
Resolution: `sprint_planning_prompt.md` v1.3→v1.4: STEP -1.3 extended — bypass fields required;
strict mode halts if absent, standard mode flags and blocks seal. `shared_standards.md` v1.3→v1.4:
§10.1 Sprint Planning row updated.

---

**IMP-05 — Lessons learnt action-now items not verified before next cycle** ✅ COMPLETE (2026-03-08)
Area: Lifecycle | Governance
Problem: No pre-flight check in Release Planning confirms that action-now items from the prior
cycle's `lessons_learnt_closure.md` were applied and appear in `prompt_change_log.md`.
Why it matters: Process improvements silently skip when sessions are interrupted.
Recommended change: Add STEP -1 advisory check in `release_planning_prompt.md`.
Effort: Low
Resolution: `release_planning_prompt.md` v2.12→v2.13: STEP -1.5 added — reads prior cycle
`lessons_learnt_closure.md`, checks action-now items against `prompt_change_log.md`; warns if
missing; records gap as outstanding action in run manifest.

---

**IMP-06 — `next_cycle_unblocked` not verified by Release Planning hard gate** ✅ COMPLETE (2026-03-08)
Area: State | Lifecycle
Problem: The lifecycle guard checks `status = Closed` but not `next_cycle_unblocked = true`. A
session crash between the two writes passes the gate on an incomplete prior cycle close.
Why it matters: Next cycle opens on a corrupt prior cycle close.
Recommended change: Add `next_cycle_unblocked = true` as an explicit condition in the Release
Planning lifecycle guard.
Effort: Low
Resolution: `release_planning_prompt.md` v2.12→v2.13: STEP -1.6 added as a hard gate — checks
both fields; exception for first cycle. `shared_standards.md` v1.3→v1.4: §10.1 updated.

---

**IMP-07 — Escalation subroutine duplicated across prompts** ✅ COMPLETE (2026-03-08)
Area: Token Efficiency | Governance
Problem: Each engine prompt contains its own escalation format rules, SLA table, and freeze rules —
duplicates of `shared_standards.md §4`. The subroutine in `release_planning_prompt.md` alone is
~60 lines.
Why it matters: Maintenance drift risk; token cost on every engine load; updates replicated to 6
prompts.
Recommended change: Remove inline escalation subroutines. Replace with reference to
`shared_standards.md §4`. Retain only engine-specific trigger conditions inline.
Effort: Medium
Resolution: `release_planning_prompt.md` v2.12→v2.13: inline escalation subroutine removed and
replaced with single reference line. Engine-specific rules retained.

---

**IMP-08 — release_plan.md generates excessive prose** ✅ COMPLETE (2026-03-08)
Area: Token Efficiency
Problem: `release_plan.md` retains full narrative prose for scope items, risk register, and
dependency map — most of which is restated in `stage4_backlog_slice.md`.
Why it matters: Token cost on every read; content duplicated between artefacts.
Recommended change: Replace EPIC narrative sections with compact tables. Move full acceptance
criteria exclusively to `stage4_backlog_slice.md`. Target <200 lines for `release_plan.md`.
Effort: Medium
Resolution: `release_planning_prompt.md` v2.12→v2.13: STEP 3 compact table format required;
AC directed to backlog slice only; <200 line target stated.

---

**IMP-09 — Amendment cycle `sprint_sealed` guard is not atomic** ✅ COMPLETE (2026-03-08)
Area: State | Failure Handling
Problem: Amendment cycle checks `sprint_sealed = false` but Sprint Planning writes `sprint_sealed =
true` to the same file. No lock prevents concurrent execution.
Why it matters: Amended backlog slice and sealed sprint backlog could diverge silently.
Recommended change: Amendment cycle acquires `claude/backlog/.lock` before reading `sprint_sealed`.
Effort: Low
Resolution: `amendment_cycle_prompt.md` v1.1→v1.2: STEP -1.1 — lock acquired before read; held
until STEP 5; halt if lock held by another process.

---

**IMP-10 — No automated check that `prompt_change_log.md` is updated when prompts are versioned** ✅ COMPLETE (2026-03-08)
Area: Governance | Automation
Problem: `prompt_change_log.md` is manually maintained. Agents can increment prompt versions without
adding an entry.
Why it matters: Governance drift — version numbers increment but changes are not recorded.
Recommended change: Add rule to `shared_standards.md`; STEP -1 of release planning verifies log
entries exist for current prompt versions.
Effort: Low
Resolution: `shared_standards.md` v1.3→v1.4: §11 Prompt Version Control added.
`release_planning_prompt.md` v2.12→v2.13: STEP -1.7 added — advisory check; warns if missing.

---

### Open — Governance audit (2026-03-08, v3.3)

---

**IMP-11 — No state guard prevents Phase 1B from opening while an Amendment is in progress**
Area: State | Lifecycle
Problem: The Release Planning lifecycle guard does not halt on `Amendment_In_Progress`. A
mis-invoked `plan release` during an amendment could corrupt `active_cycle` and strand the
amendment with no owning cycle pointer.
Why it matters: Low-probability but unrecoverable corruption scenario.
Recommended change: Add `Amendment_In_Progress` to the explicit halt states in the Release Planning
lifecycle guard (STEP -1).
Expected benefit: Eliminates an unrecoverable corruption path. Zero new artefacts.
Token impact: Neutral.
Effort: Low

---

**IMP-12 — `closure_record.md` structure is undefined**
Area: Lifecycle | Governance
Problem: `closure_record.md` (Class 3) is listed in the Artefact Register but its required fields
are not defined anywhere. Every other Class 3 artefact has a defined schema or explicit format in
its producing engine.
Why it matters: Agents produce inconsistent closure records across cycles. Class 3 artefacts are
permanent records — inconsistency makes retrospective audits unreliable.
Recommended change: Define required fields in `post_ship_closure_prompt.md`: cycle_id, ship_date,
verification_status, steps_completed, outstanding_actions_carried_forward, lessons_learnt_summary
(N immediate | N deferred | N escalated), confirmed_by, confirmed_date.
Expected benefit: Deterministic, auditable closure records across all cycles.
Token impact: Neutral — replaces free-form prose with equivalent structured content.
Effort: Low

---

**IMP-13 — Hard Rules table contains rules not enforced by any engine**
Area: Governance | Prompt–Playbook Alignment
Problem: Two declared Hard Rules have no engine enforcement: (1) "No roadmap addition without an
equal or greater stop" — no engine counts additions vs. kills. (2) "Decision log is append-only"
— no engine verifies prior entries before appending.
Why it matters: Rules that appear enforced but are not create false confidence and governance
theatre.
Recommended change: (1) Add net-zero verification to Roadmap STEP 9: count items added vs.
confirmed-killed; halt if additions > kills. (2) Either add a line-count pre-read to the decision
log append step, or reclassify rule 2 as a governance convention rather than a hard rule.
Expected benefit: Hard rules are actually hard.
Token impact: Neutral (rule 2) / Costs slightly (rule 1 — one additional file read per Phase 1 run).
Effort: Low (rule 2) / Medium (rule 1)

---

**IMP-14 — Phase 4 test scenario gap actions have no completion tracking**
Area: Lifecycle | State
Problem: §9.6 specifies gap instructions are written to the QA agent file and become backlog items
"if they cover core user journeys." No field in the verification report or state tracks whether
actions were converted to backlog items or silently dropped.
Why it matters: Test coverage gaps identified in Phase 4 are the primary QA feedback loop. Silent
dropout means the same gaps recur each cycle.
Recommended change: Add a `test_scenario_gaps` array to `verification_report.md` with fields:
gap_id, description, qualifying_reason, disposition. Phase 4 exit criteria: all gaps must have a
disposition. Post-Ship Closure STEP 3 confirms gap backlog items are present in `backlog.md`.
Expected benefit: Closes the QA feedback loop. Makes gap handling auditable and resumable.
Token impact: Neutral — replaces unstructured agent-file append with an equivalent structured table.
Effort: Low

---

**IMP-15 — Stale idea mandatory-PO-disposition rule is unenforceable**
Area: Automation | Lifecycle
Problem: The "3+ consecutive parks = mandatory PO disposition" rule (§5.3) is declared but not
enforced. The Roadmap Engine STEP 4 only reviews ideas in the current window — it has no guard
that reads prior-cycle statuses to detect silent re-parks.
Why it matters: Stale ideas accumulate without forcing a decision. The mandatory disposition
requirement is governance theatre.
Recommended change: Add a stale-idea detection sub-step to Roadmap STEP 4: read all submission
files, count consecutive park cycles per idea, halt (strict) or surface (standard) any idea at
Parked-cycle-3 or beyond without an explicit PO disposition in the current run.
Expected benefit: PO disposition rule becomes enforceable.
Token impact: Costs slightly — one additional directory scan of `claude/ideas/submissions/` per
Phase 1 run.
Effort: Low

---

**IMP-16 — Backlog lock stale protocol is underspecified**
Area: State | Failure Handling
Problem: §6B.5 references a "stale protocol (timestamp threshold + evidence of inactive owning
cycle)" that is not defined anywhere in the playbook or `shared_standards.md`. Threshold and
evidence criteria are undefined.
Why it matters: Agents either refuse to clear any lock (deadlock) or clear on insufficient evidence
(data corruption). The protocol preventing both outcomes does not exist.
Recommended change: Define the stale lock protocol in `shared_standards.md`: (1) stale threshold =
4 hours from `lock_acquired_utc` with no active session; (2) evidence = `state.json` macro-state
not updated since lock acquisition AND no active `execution_state.json` step-in-progress markers;
(3) PMO Lead records release in `escalations.md` with timestamp and evidence before clearing.
Expected benefit: Lock recovery is deterministic. Eliminates the deadlock/corruption dilemma.
Token impact: Neutral.
Effort: Low

---

**IMP-17 — Class 8 (Proof of Gate) is defined but no engine produces it**
Area: Governance | Prompt–Playbook Alignment
Problem: §3 defines Class 8 with a detailed required header. §13 Artefact Register lists no Class
8 document. No engine produces one. The class is defined but orphaned.
Why it matters: Either Class 8 is vestigial and causes agent confusion, or it represents an
unimplemented governance mechanism that was intended to formalise gate sign-offs.
Recommended change: Decision required: (a) Activate — specify which gate produces it, add to
Artefact Register, add production steps to the relevant engine. (b) Defer — add note to §3:
"Reserved — not currently produced by any engine" to prevent agents generating orphaned documents.
Expected benefit: Eliminates governance confusion.
Token impact: Saves slightly — removes ambiguity that could cause agents to generate unrequested
documents.
Effort: Low

---

**IMP-18 — Sprint Planning goal confirmation step has no resumability guarantee**
Area: State | Failure Handling
Problem: STEP 2 (sprint goal) is a hard gate requiring PO confirmation. `sprint_goal.md` existence
is the only resume signal — the engine cannot distinguish "goal drafted" from "goal confirmed." A
crash after drafting but before PO sign-off leaves the engine in an ambiguous state.
Why it matters: Re-invocation may re-draft the goal (token waste) or skip confirmation (governance
violation).
Recommended change: Add `sprint_goal_status` field to a lightweight `sprint_plan_state.json` with
values: `not_started | drafted | confirmed`. STEP 2 resumes only from `confirmed`; any earlier
state re-runs the confirmation request.
Expected benefit: Reliable resume for the most common human-in-the-loop sync point.
Token impact: Saves — prevents full STEP 2 re-execution on recovery.
Effort: Low

---

**IMP-19 — Meta-review trigger and scope** ⚠️ SUPERSEDED BY IMP-29 (2026-03-08)
Original finding: Meta-review trigger undefined, untracked, and suppressed when Phase 1 is skipped.
Superseded: IMP-29 relocates meta-review to Post-Ship Closure at cycle level and expands scope to
all phases, making the Phase 1-scoped trigger redundant. Partial recommendations (clarify cycle
definition, add field to Phase 1 exit checklist) are absorbed into IMP-29.

---

**IMP-20 — Delegation log has no exit-criteria check in Phase 3**
Area: Lifecycle | Failure Handling
Problem: Phase 3 exit criteria (§8.6) do not include a check that all entries in
`delegation_log.md` have a resolved outcome. The sprint close commit can complete with open
delegation log entries, producing a silent mismatch between `delegation_log.md` and
`execution_state.json`.
Why it matters: Phase 4 inherits an inconsistent picture. The "nothing is silently skipped"
guarantee (§8.3) is violated.
Recommended change: Add to Phase 3 exit criteria: "All entries in `delegation_log.md` have a
recorded outcome (done | returned_to_backlog | pending_with_ETA | escalated)." Add a corresponding
check to the execution engine sprint close step before writing `Sprint_Complete`.
Expected benefit: `delegation_log.md` and `execution_state.json` are always consistent at Phase 3
close.
Token impact: Neutral — one additional file read at sprint close.
Effort: Low

---

### Open — Token efficiency audit (2026-03-08)

---

**IMP-21 — Lessons learnt produced per-phase as prose; no cross-cycle pattern detection possible**
Area: Token Efficiency | Lifecycle
Problem: Three separate narrative lessons learnt documents are produced per cycle (Phase 1B,
Phase 3, Phase 4) plus a closure record. Each is written in full prose, filed independently, and
read separately by Post-Ship Closure. The same friction pattern can appear in five consecutive
execution records with no systemic flag. Post-Ship Closure reads three full documents where one
structured file would suffice.
Why it matters: Highest sustained token cost in the lessons learnt system. Prose format makes
cross-cycle pattern detection intractable. Four separate file reads at closure when one suffices.
Recommended change: Replace the three per-phase records with a single `lessons_learnt_cycle.md`
with phase-tagged sections (## Phase 1B | ## Phase 3 | ## Phase 4 | ## Post-Ship). Each phase
appends a structured table on completion. Table schema: `friction_item | phase | type (A–E) |
classification (action-now/defer) | action | owner | target_date`. Post-Ship Closure and
meta-review read one file. Legacy per-phase records (`lessons_learnt_execution.md`,
`lessons_learnt_verification.md`) retired from the Artefact Register.
Expected benefit: 40–60% reduction in lessons learnt write and read tokens per cycle. Single read
at Post-Ship Closure. Structured format makes meta-review pattern scanning tractable.
Token impact: Saves significantly — one structured file vs. three prose files; single read at
closure.
Effort: Medium
Prerequisite for: IMP-28, IMP-29

---

**IMP-22 — Every engine preflight re-reads the same governance files in full**
Area: Token Efficiency | Automation
Problem: Every engine STEP -1 reads `.claude_current_state.json`, `team_charter.md`,
`document_lifecycle_guide.md`, and `strategy_rules.md` in full. These files are stable within a
cycle. The combined cost of loading these four files is paid six or more times per cycle (Phase 1B,
1.5, 2, 3, 4, Post-Ship).
Why it matters: Governance reference documents are unlikely to be needed in their entirety at every
preflight. Engines reference specific sections, not full documents.
Recommended change: Add section-scoped read instructions to each engine preflight. Define a
`shared_preflight_fields` list in `shared_standards.md` specifying the minimum field set required
from `.claude_current_state.json` per engine.
Expected benefit: Reduces repeated governance document loading across the full cycle.
Token impact: Saves — governance documents loaded in full 6+ times per cycle; section-scoping
reduces this materially.
Effort: Medium

---

**IMP-23 — Acceptance criteria duplicated in full across three artefacts**
Area: Token Efficiency | Cross-Phase Duplication
Problem: Full acceptance criteria (all four dimensions: technical, quality, security, verification)
appear in: (1) `stage4_backlog_slice.md`, (2) `sprint_backlog.md` — Phase 2 copies them in full,
(3) `execution_state.json` — Phase 3 loads them per item. For a 30-item sprint, full AC appears
three times. Each AC set is 4–8 lines per item.
Why it matters: Sprint backlog production re-reads and re-writes AC that already exists in the
backlog slice. Execution engine re-loads AC that it could read directly from the backlog slice.
Largest volume duplication in the system.
Recommended change: `sprint_backlog.md` references AC by item ID only (`AC: see
stage4_backlog_slice.md#ST-01`). Execution engine reads AC from `stage4_backlog_slice.md` directly.
`sprint_backlog.md` becomes a sequencing and ownership document, not an AC store.
Expected benefit: Largest single token saving available in the system.
Token impact: Saves significantly — eliminates full AC rewrite at Phase 2 and reload at Phase 3
for every sprint item.
Effort: Medium

---

**IMP-24 — `sync gh` parses markdown rather than consuming structured output**
Area: Token Efficiency | Automation
Problem: `sync gh` parses `stage4_backlog_slice.md` (markdown) to extract issue fields. Markdown
parsing by an LLM is fragile and token-expensive. Phase 1B already has all item data in structured
form at generation time.
Why it matters: Parse failures cause silent issue mismatches. Token cost is higher than necessary.
Recommended change: Phase 1B STEP 4 produces a companion `stage4_issue_manifest.json` alongside
`stage4_backlog_slice.md`. Fields: `[{id, title, epic, description, ac_summary, labels, assignee}]`.
`sync gh` consumes the JSON directly. Markdown backlog slice retained for human readability only.
Expected benefit: Reliable issue sync with no parse ambiguity. Lower token cost for sync operation.
Token impact: Saves — JSON consumption vs. full markdown parse; small additional cost at Phase 1B
to produce the JSON (net positive overall).
Effort: Low

---

**IMP-25 — Sprint backlog loaded in full on every EPIC invocation during Phase 3**
Area: Token Efficiency | State File Efficiency
Problem: `run sprint --epic EPIC-xx` loads `sprint_backlog.md` in full to extract items for the
targeted EPIC. For a 30-item sprint, the full document is loaded even when only 4–6 items are
relevant. A 5-EPIC sprint loads the full backlog 5 times.
Why it matters: Sprint backlog is the highest-frequency read document in Phase 3. Full loads
multiply token cost linearly with EPIC count.
Recommended change: Phase 2 produces a companion `sprint_backlog_index.json` mapping each EPIC to
its ST item IDs and line ranges in `sprint_backlog.md`. Execution Engine uses the index to load
only the relevant slice per EPIC invocation.
Expected benefit: Reduces Phase 3 token cost proportionally to EPIC count.
Token impact: Saves — targeted reads vs. full document loads per EPIC invocation.
Effort: Low

---

**IMP-26 — Risk register content duplicated between `release_plan.md` and `escalations.md`**
Area: Token Efficiency | Cross-Phase Duplication
Problem: RISK-xx entries are written in `release_plan.md` STEP 3, then if escalated, re-written
as ESC entries in `escalations.md`. Downstream engines load both files to get a complete risk
picture, reading the same risk content twice in different formats.
Why it matters: Every risk that escalates is written and read twice. Sprint Planning and Execution
preflights load `escalations.md` for open items, but the underlying risk context lives in
`release_plan.md`.
Recommended change: RISK-xx entries in `release_plan.md` include an `escalation_ref` field (null
or ESC-id). `escalations.md` stores only the escalation decision and status — not the full risk
re-statement. Downstream engines read risk context from `release_plan.md` via the ref.
Expected benefit: Eliminates risk content duplication. Single source of truth for risk descriptions.
Token impact: Saves — `escalations.md` becomes a lightweight status/decision log rather than a
full risk re-statement.
Effort: Low

---

**IMP-27 — Post-Ship Closure reads six input documents in full; most need only one field**
Area: Token Efficiency | Artefact Read Redundancy
Problem: Post-Ship Closure §10.2 lists eight required inputs, most read in full. Actual field usage
per step:
- `verification_report.md` — needs verification_status and deviation list only
- `sprint_close.md` — needs readiness statement only
- `execution_state.json` — needs item outcome list only
- `lessons_learnt.md` (Phase 1B) — needs action item list only
- `lessons_learnt_execution.md` — needs action item list only
- `qa_evidence_EPIC-xx.md` — needs deviation entries only
Full document reads taken where field reads would suffice.
Why it matters: Post-Ship Closure is the most input-heavy engine. Full reads of 6–8 documents on
every invocation is the highest single-invocation token cost in the lifecycle. Note: IMP-21
reduces two of these reads to one; IMP-27 addresses the remainder.
Recommended change: Define field-level read targets for each Post-Ship Closure step in
`post_ship_closure_prompt.md`. Where field-level reads are not possible (prose documents), add a
structured summary block to the producing engine's output as the canonical read target for closure.
Expected benefit: Largest single-invocation token saving in the system.
Token impact: Saves significantly — targeted field reads vs. full document loads for 6–8 inputs.
Effort: Medium

---

### Open — Lessons learnt architecture decisions (2026-03-08)

---

**IMP-28 — Consolidate per-phase lessons learnt into a single structured cycle record**
Area: Token Efficiency | Lifecycle
Problem: Three separate narrative lessons learnt documents are produced per cycle (Phase 1B,
Phase 3, Phase 4) plus a closure record. All written in full prose, filed independently, read
separately by Post-Ship Closure and meta-review. The same friction pattern can appear across five
consecutive cycles with no systemic detection. Post-Ship Closure reads three full documents where
one structured file would suffice.
Why it matters: Highest sustained token cost in the lessons learnt system. Prose format makes
cross-cycle pattern detection intractable. Four separate file reads at closure when one suffices.
Recommended change: Replace the three per-phase records with a single `lessons_learnt_cycle.md`
with phase-tagged sections (## Phase 1B | ## Phase 3 | ## Phase 4 | ## Post-Ship). Each phase
appends a structured table on completion rather than generating a new document. Table schema:
`friction_item | phase | type (A–E) | classification (action-now/defer) | action | owner |
target_date`. Post-Ship Closure and meta-review read one file. Existing per-phase prompts
(release_planning_prompt.md, execution_prompt.md, delivery_verification_prompt.md,
post_ship_closure_prompt.md) updated to append to the shared record. Legacy records
(`lessons_learnt_execution.md`, `lessons_learnt_verification.md`) retired from the Artefact
Register.
Expected benefit: 40–60% reduction in lessons learnt write and read tokens per cycle. Single read
at Post-Ship Closure. Structured format makes meta-review pattern scanning tractable without full
document summarisation.
Token impact: Saves significantly — one structured file vs. three prose files; single read at
closure.
Effort: Medium
Hard prerequisite for: IMP-29

---

**IMP-29 — Move meta-review to cycle level at Post-Ship Closure; trigger every 3rd completed cycle across all phases**
Area: Lifecycle | Governance | Token Efficiency
Problem: Meta-review currently lives inside Roadmap Engine STEP 11 and only fires during Phase 1
(roadmap rebalance) runs. If Phase 1 is routinely skipped, meta-review never fires. Scope is
limited to planning friction only — execution, verification, and closure patterns are invisible to
it. The trigger counter (`last_meta_review_cycle`) increments on Phase 1 runs, not completed
delivery cycles, making cadence unpredictable and suppressible.
Why it matters: The meta-review is the system's only cross-cycle structural improvement mechanism.
Limiting scope to Phase 1 means execution delegation failures, recurring verification deviations,
escalation patterns, and closure gaps are never surfaced systemically. A system that routinely
skips Phase 1 effectively disables its own improvement loop.
Recommended change:
(1) Remove meta-review from Roadmap Engine STEP 11. Roadmap Engine retains per-run lessons learnt
    (appended to `lessons_learnt_cycle.md` if active, or standalone if Phase 1 runs outside a full
    cycle).
(2) Add meta-review as STEP 10 of Post-Ship Closure, conditional on cycle count.
(3) Trigger condition: `completed_cycle_count % 3 == 0` where `completed_cycle_count` is a new
    field in `.claude_current_state.json`, incremented at each Post-Ship Closure.
(4) Meta-review scope: reads `lessons_learnt_cycle.md` from the last 3 cycles, identifies
    recurring patterns across all phases, produces `meta_review.md` in `claude/cycles/<id>/`.
(5) Any friction pattern appearing in 2 of 3 cycles is a mandatory action-now candidate —
    not advisory.
(6) `last_meta_review_cycle` field renamed to `last_meta_review_completed_cycle` to reflect the
    new counter basis.
(7) Playbook updates required: §6.3 STEP 11, §10 Post-Ship Closure, §12 Cycle Trigger table,
    §14 Governance table.
Expected benefit: Meta-review fires reliably every 3 cycles regardless of Phase 1 cadence.
Full-cycle scope captures execution, verification, and closure friction systemically for the first
time. With IMP-28's structured input, token cost is lower than the current Phase 1-scoped version
despite broader scope.
Token impact: Saves net — structured input (IMP-28) reduces per-review cost below current version.
Small addition to Post-Ship Closure on trigger cycles only. Meta-review moves from
unpredictable/suppressed to reliable and cheaper.
Effort: Medium
Hard prerequisite: IMP-28 must be implemented and validated across at least one complete cycle
before IMP-29 is activated. Attempting both simultaneously risks meta-review firing on incomplete
structured input during the transition cycle.

---

### Open — Six-dimension audit (2026-03-08)

---

**IMP-30 — `design_gate_bypass_authority` has no named role and Head of UX & Design has no authority row**
Area: Governance | Role Charter Completeness
Problem: Two role gaps identified in the playbook: (1) §1 Hard Rules require `design_gate_bypass_authority`
to be recorded in `.claude_current_state.json` when the design gate is bypassed, but no role in §2
Roles & Authorities is declared as holding this authority — any agent could self-assign it. (2) §6.5.1
states "Head of UX & Design may downgrade" design classifications from Design Required, but this role
has no row in the §2 authority table and no declared authority type, meaning its decisions have no
governance backing.
Why it matters: An authority field with no named authority holder is unenforceable. A role that acts
without a charter entry has no defined boundary — it can neither be held accountable nor overruled
by a defined mechanism.
Recommended change: (1) Add `design_gate_bypass_authority` to §2 as an explicit authority held by
a named role (Head of Specs Team or Product Owner — decision required). (2) Add Head of UX & Design
to the §2 Roles & Authorities table with authority type: "Design classification decisions; design
artefact approval; downgrade authority for Design Required items." Update team_charter.md to match.
Expected benefit: Both authority gaps become enforceable and auditable.
Token impact: Neutral.
Effort: Low

---

**IMP-31 — Class 8 "clearing authority role" is unnamed and unmapped**
Area: Governance | Role Charter Completeness
Problem: §3 Document Classes defines Class 8 (Proof of Gate) with Owner field: "Clearing authority
role." No role in §2 is designated as a clearing authority for any gate. No engine produces a Class 8
document (IMP-17). The combination means Class 8 is doubly orphaned — no producer and no owner.
Why it matters: If Class 8 is ever activated (IMP-17 recommendation a), the clearing authority role
must be defined before the engine can be built. Leaving it undefined means activation requires
simultaneous role creation, prompt update, playbook update, and charter update — high coordination
cost and high risk of inconsistency.
Recommended change: Resolve IMP-17 first (activate or formally defer Class 8). If activated: name
the clearing authority role per gate type (e.g. Director of Quality clears the Merge Gate; PMO Lead
clears the Publish Gate). Add to §2 authority table and relevant agent charters.
Expected benefit: Eliminates the double-orphan. Makes Class 8 activation a single-step decision
rather than a multi-document coordination effort.
Token impact: Neutral.
Effort: Low (decision) / Medium (if activating Class 8)
Dependency: IMP-17

---

**IMP-32 — First-cycle guards missing across four engines**
Area: State | Lifecycle | First-Cycle Correctness
Problem: Four specific first-cycle failure points identified:
(1) Release Planning STEP -1.5 reads `prior_cycle/lessons_learnt_closure.md` — this path does not
    exist on cycle 1. No guard defined; engine will fail or skip silently.
(2) Release Planning STEP -1.6 checks `next_cycle_unblocked = true` — this field does not exist in
    `.claude_current_state.json` on cycle 1. The exception note says "exception for first cycle"
    but does not define what the exception condition is or how the engine detects it.
(3) IMP-29 meta-review reads `lessons_learnt_cycle.md` from the last 3 cycles — on cycle 1 there
    are zero prior cycles; on cycle 2 there is one. No handling defined for sub-threshold cycle
    counts. Meta-review either fires on insufficient data or the trigger condition fails silently.
(4) Phase 1M state fields (`last_manage_roadmap_utc`, `last_groom_backlog_utc`) will be null on
    first invocation. Any downstream engine that reads these fields without a null guard will either
    fail or treat null as "never run" — which is correct, but must be explicitly handled rather than
    assumed.
Why it matters: First invocation is the highest-risk execution path. Silent failures or crashes on
cycle 1 undermine trust in the entire system before any value is delivered.
Recommended change: Define explicit first-cycle detection across all engines: a field
`is_first_cycle` (bool) derived from `completed_cycle_count == 0` in `.claude_current_state.json`.
Each guard that depends on prior cycle data checks `is_first_cycle` first and skips gracefully with
a logged note rather than attempting to read a non-existent path. For IMP-29 meta-review: trigger
only when `completed_cycle_count >= 3`; on cycles 1 and 2 log "meta-review pending — insufficient
cycle history" and skip.
Expected benefit: Eliminates all known first-cycle failure points. Single `is_first_cycle` field
makes the guard pattern consistent and auditable.
Token impact: Neutral — minimal additional field check per engine.
Effort: Low

---

**IMP-33 — Standard mode behaviour undefined or contradictory for three conditions**
Area: Governance | Prompt–Playbook Alignment | Mode Parity
Problem: Three mode parity failures identified:
(1) Sprint Planning §7.3 states "items without confirmed acceptance criteria may not enter the
    sprint" (absolute prohibition), but also states "in standard mode they receive an [AC REQUIRED]
    placeholder." These two statements directly contradict — the first is mode-independent, the
    second makes it mode-dependent. The backlog cannot be sealed with [AC REQUIRED] placeholders
    per §7.6 exit criteria, creating an irresolvable conflict in standard mode.
(2) Roadmap Engine STEP 5 zero-sum displacement rule ("no candidate advances without naming a
    displacement") has no mode variant defined. It is written as an absolute rule but lives in a
    prompt that accepts `--mode`. It is unclear whether standard mode relaxes or enforces this rule.
(3) Execution Engine §8.2 defines `strict` as "halt on any ambiguity" but "ambiguity" is not
    defined. Standard mode behaviour for ambiguous items is not specified — agents must infer it,
    producing inconsistent behaviour across runs.
Why it matters: Contradictory mode rules produce unpredictable engine behaviour. Agents will resolve
contradictions differently on each invocation, making the system non-deterministic.
Recommended change: (1) Resolve the AC contradiction: [AC REQUIRED] placeholders are permitted in
standard mode as a draft state only — the backlog cannot be sealed until all are resolved, in both
modes. Standard mode does not allow sealing with open placeholders; it only allows proceeding to
the next planning step while flagging the gap. (2) Declare the zero-sum rule as mode-independent
(hard rule) explicitly in the roadmap prompt. (3) Define "ambiguity" for the execution engine:
list the specific conditions that constitute ambiguity (missing spec reference, missing owner,
missing AC, unresolved dependency).
Expected benefit: Deterministic mode behaviour. Agents resolve conditions consistently across runs.
Token impact: Neutral.
Effort: Low

---

**IMP-34 — Release Planning and Post-Ship Closure have no declared write scope lists**
Area: Governance | Write Scope Enforcement
Problem: The Roadmap Engine STEP 9 explicitly restricts writes to an allowed list. Release Planning
and Post-Ship Closure have no equivalent declared write scope. Audit of their steps reveals:
Release Planning writes to: `backlog.md`, `state.json`, `.claude_current_state.json`,
`release_plan.md`, `escalations.md`, `run_manifest.md`, `cycle_summary.md`, `lessons_learnt.md`,
`backlog_txn.json`, `stage4_backlog_slice.md`, `stage4_issue_manifest.json` (IMP-24),
`docs/product/scope/scope--*.md`, `docs/product/decisions/decisions--*.md`,
`current_roadmap.md` (execution notes, STEP 5).
Post-Ship Closure writes to: `changelog.md`, `current_roadmap.md`, `backlog.md`,
scope document (status update), decisions record (status update), canonical spec files
(deviation entries), `System_status_report.md`, `validation_system.md`, `Specs_Index.md`,
`closure_record.md`, `closure_state.json`, `lessons_learnt_cycle.md` (IMP-28).
Neither engine has a formal write scope declaration. `.claude_current_state.json` is written by
Phase 1M engines outside the designated sync steps, with no declared scope entry for Phase 1M.
Why it matters: Without a declared write scope, there is no governance check against an engine
writing to a file it should not touch. Post-Ship Closure writing to `current_roadmap.md` and
canonical spec files is high-risk — these are Class 1 documents with strict ownership rules.
Recommended change: Add a `## Write Scope` section to each engine prompt listing every file the
engine is permitted to write, grouped by step. Any write outside this list is a hard gate violation.
For `.claude_current_state.json`: declare which fields each engine may write (not just that it may
write the file). Post-Ship Closure writes to Class 1 documents must be explicitly scoped to
specific fields/sections only (e.g. "roadmap entry status field only — no structural changes").
Expected benefit: Write scope becomes auditable and enforceable. Eliminates the risk of an engine
modifying a sealed or Class 1 artefact outside its authority.
Token impact: Neutral.
Effort: Medium

---

**IMP-35 — Idempotency guards absent or undefined for four write operations**
Area: State | Failure Handling | Idempotency
Problem: Four idempotency gaps identified:
(1) Backlog slice commit: the playbook references an "idempotency marker" but does not define its
    format, where it lives, or whether it is checked before write (preventing duplicate) or after
    write (detecting duplicate). A pre-write check is required for true idempotency; a post-write
    check only detects the problem after corruption has occurred.
(2) Lessons learnt append (IMP-28 consolidated record): each phase appends a table section to
    `lessons_learnt_cycle.md` on completion. No guard defined for what happens if the phase step
    is re-run — the same friction items would be appended twice, producing duplicate rows.
(3) `prompt_change_log.md` entries: action-now patches write entries to this log. No guard against
    a duplicate entry if the patch step is re-run during resume. Duplicate entries would cause
    IMP-10's version check to find multiple matches and potentially misreport compliance.
(4) `sync gh` issue creation: declared as "creates/updates" but no defined behaviour for partial
    runs. If `sync gh` creates 8 of 12 issues then fails, re-invocation must update the 8 already
    created and create the remaining 4. If the create/update distinction relies on issue existence
    checks, a race condition between check and create could produce duplicates.
Why it matters: Resumability is a core system guarantee. Any write operation without an idempotency
guard silently breaks that guarantee. Duplicate log entries and duplicate backlog items compound
across cycles.
Recommended change: (1) Define the backlog slice idempotency marker format explicitly: a comment
line `<!-- committed: <cycle_id> <timestamp> -->` checked at STEP 3.9 before any write — halt if
marker already present for this cycle_id. (2) Lessons learnt append: check for existing section
header `## Phase <X> — <cycle_id>` before appending; skip if present. (3) Prompt change log:
check for existing entry with matching prompt name + version before appending; skip if present.
(4) `sync gh`: use GitHub issue labels containing cycle_id as the idempotency key — check label
before create; update if label exists.
Expected benefit: All four write operations become safe to re-run. Resumability guarantee is
restored for these paths.
Token impact: Costs slightly — one additional read check per write operation; negligible.
Effort: Low

---

**IMP-36 — Playbook body version references lag §14 governance table**
Area: Governance | Cross-Document Version Consistency
Problem: Three internal version inconsistencies identified within the playbook itself (visible
without accessing prompt files):
(1) §6B opening line: "Source prompt: `claude/system/release_planning_prompt.md` (v2.11)" —
    §14 Governance table and the v3.3 change log both declare v2.13 as current. The body reference
    is two minor versions behind.
(2) §7 Sprint Planning opening line: "Source prompt: `claude/system/sprint_planning_prompt.md`
    (v1.2)" — §14 declares v1.4 as current. Two minor versions behind.
(3) §8 Execution opening line: "Source prompt: `claude/system/execution_prompt.md` (v1.5)" —
    §14 declares v1.6 as current. One minor version behind.
These are the three prompts most recently updated per the v3.3 change log. The pattern suggests
§14 is updated correctly but phase section headers are not updated in the same edit.
Why it matters: Agents reading a phase section to understand the governing prompt will load an
outdated version reference. If a prompt file has multiple versions in the repository, the agent
may load the wrong one. In single-version repositories the risk is confusion rather than
operational failure, but it still constitutes governance drift.
Recommended change: Add a standing rule to the Playbook Governance section (§14): "When a prompt
version is updated in the §14 Governance table, the corresponding phase section source prompt
reference must be updated in the same edit. A version mismatch between a phase header and §14
is a non-compliant state." Perform a one-time reconciliation pass to align all three identified
phase headers with §14 current versions.
Expected benefit: Eliminates version reference drift. Single-edit discipline prevents recurrence.
Token impact: Neutral.
Effort: Low

---

### Open — Amendment cycle, dry-run, and miscellaneous gaps (2026-03-08)

---

**IMP-37 — Amendment lessons learnt is a disconnected artefact**
Area: Lifecycle | Governance
Problem: `amendment_lessons.md` is listed in the Artefact Register (§13, Class 3, Phase Amendment)
but §6B.8 defines no step that produces it, no required format, and no connection to the lessons
learnt feedback loop — consolidated (IMP-28) or otherwise. It is the only Class 3 artefact in the
register with no producing step.
Why it matters: Amendment cycles are emergency events — exactly the situations most likely to
generate actionable process improvements. A lessons learnt record that is declared but never
produced means amendment friction is never captured, never fed into the meta-review, and never
improves the process.
Recommended change: Add an explicit lessons learnt step to the amendment cycle engine
(`amendment_cycle_prompt.md`), positioned after ratification and before commit. Format: append
a `## Amendment — <AMD-id>` section to `lessons_learnt_cycle.md` (IMP-28 consolidated record)
with fields: trigger reason, ratification friction, backlog slice change summary, time cost,
recurrence risk (Y/N), recommended process change. If IMP-28 is not yet implemented, produce
a standalone `amendment_lessons.md` using the same schema. Update the Artefact Register to
reference the producing step.
Expected benefit: Amendment friction enters the improvement loop for the first time. Meta-review
(IMP-29) gains visibility into emergency cycle patterns.
Token impact: Costs slightly — one additional structured append per amendment cycle.
Effort: Low

---

**IMP-38 — Amendment cycle "one active at a time" rule has no machine enforcement**
Area: State | Governance | Idempotency
Problem: §6B.8 declares "one active amendment at a time — seal or withdraw before opening
another." This is enforced entirely by the PMO Lead reading the instruction and self-complying.
No engine check exists. The amendment engine has no step that reads `amendment_state.json` for
existing active amendments before proceeding. A second `amend cycle` invocation could create a
second amendment folder and begin writing before any conflict is detected.
Why it matters: Two concurrent amendments to the same backlog slice would produce divergent
`amended_backlog_slice.md` files with no merge path. The original cycle's Sprint Planning would
have no defined source of truth.
Recommended change: Add to amendment engine STEP -1: scan `claude/cycles/<original_cycle_id>/
amendments/` for any `amendment_state.json` with status not in `{sealed, withdrawn}`. If found,
halt with: "Active amendment <AMD-id> exists. Seal or withdraw before opening a new amendment."
This is a hard gate in both modes.
Expected benefit: Machine enforcement of the single-amendment rule. Eliminates concurrent
amendment corruption risk.
Token impact: Neutral — one directory scan at preflight.
Effort: Low

---

**IMP-39 — Amendment withdrawal has no defined procedure, state transition, or record**
Area: Lifecycle | State | Failure Handling
Problem: §6B.8 mentions "seal or withdraw" as the two terminal states for an amendment but
defines no withdrawal procedure. There is no defined: state value for withdrawal in
`amendment_state.json`, update to `.claude_current_state.json` on withdrawal, permanent record
requirement, or effect on the backlog lock (which IMP-09 established is held during amendment).
Why it matters: A withdrawn amendment leaves the system in an undefined state. If the backlog
lock is held and the withdrawal procedure doesn't release it, the lock becomes stale. If
`.claude_current_state.json` is not updated, Sprint Planning may still look for
`amended_backlog_slice_path` and find a withdrawn artefact.
Recommended change: Define the withdrawal procedure in `amendment_cycle_prompt.md` as an
explicit command path (`amend cycle --withdraw --cycle <cycle_id> --amendment <AMD-id>`).
Steps: (1) set `amendment_state.json` status = `withdrawn`, (2) clear
`amended_backlog_slice_path` from `.claude_current_state.json`, (3) release backlog lock,
(4) append withdrawal record to `amendment_lessons.md` (IMP-37), (5) commit. Withdrawal is a
permanent record — `amendment_state.json` is retained, not deleted.
Expected benefit: Withdrawal is deterministic and leaves no orphaned state. Backlog lock is
always released on withdrawal.
Token impact: Neutral.
Effort: Low

---

**IMP-40 — `Blocked` state has no maximum duration, SLA, or auto-escalation path**
Area: Lifecycle | Failure Handling
Problem: §4.1 defines `Blocked → prior_status` as a valid transition when an escalation is
resolved. However, nothing defines what happens if a blocked state is never resolved. There is
no maximum duration, no SLA, no auto-escalation to a higher authority, and no mechanism to
prevent a cycle from sitting in `Blocked` indefinitely. The escalation SLA table in §11.2
covers escalations by type, not the blocked state itself.
Why it matters: A permanently blocked cycle is an invisible system failure. No downstream phase
can run, no new cycle can open, and the system silently stalls. Without a timeout or escalation
path, detection relies entirely on a human noticing that nothing has progressed.
Recommended change: Add a `blocked_since_utc` field to `.claude_current_state.json`, written
when status transitions to `Blocked`. Define a `Blocked` SLA in `shared_standards.md`: 72
hours maximum before mandatory escalation to Product Owner regardless of escalation type. At
72 hours: engine writes a `BLOCKED_SLA_BREACH` notice to the active cycle's escalations file
and flags `.claude_current_state.json` with `blocked_sla_breached = true`. Post-Ship Closure
checks this field and requires resolution note before proceeding.
Expected benefit: Blocked cycles are surfaced within 72 hours. Eliminates the silent stall
failure mode.
Token impact: Neutral.
Effort: Low

---

**IMP-41 — Capacity feasibility `warn` state is never resolved or acknowledged after Phase 1B**
Area: Lifecycle | Governance
Problem: Release Planning STEP 4.5 produces a capacity feasibility check with possible result
`warn`. The Publish Gate allows `warn` in standard mode. After Phase 1B publishes, nothing in
Phase 2 (Sprint Planning), Phase 3, or Phase 4 requires the `warn` to be acknowledged, recorded
as an accepted risk, or resolved. A `warn` representing significant over-allocation carries
forward invisibly into sprint execution.
Why it matters: A capacity `warn` is a signal that the sprint plan may be undeliverable. If it
is never acknowledged, the team enters execution knowing (at the planning engine level) that
capacity is strained, but with no formal record that this was accepted. When items are not
delivered, there is no audit trail connecting the outcome to the known risk.
Recommended change: Sprint Planning STEP -1 reads `stage4_5_capacity_check` from `state.json`.
If value is `warn`: require explicit Product Owner acknowledgement before proceeding (standard
mode) or halt (strict mode). Acknowledgement recorded in `sprint_planning_notes.md` and
`.claude_current_state.json` as `capacity_warn_acknowledged = true`. This converts a silent
carry-forward into a deliberate accepted risk with an audit trail.
Expected benefit: Capacity warnings are always acknowledged before sprint execution begins.
Creates an audit trail connecting capacity risk to delivery outcomes.
Token impact: Neutral — one additional field read at Sprint Planning preflight.
Effort: Low

---

**IMP-42 — `execution_state.json sealed = true` is a single unverified boolean gate for Phase 4**
Area: State | Failure Handling
Problem: Phase 4 entry requires `.claude_current_state.json` status = `Sprint_Complete` and
`execution_state.json sealed = true`. The sealed flag is a single boolean with no corroborating
fields — it could be manually set to bypass Phase 3 completion without any of the Phase 3 exit
criteria being met. Every other critical state transition has multiple corroborating checks.
Why it matters: Phase 4 is the verification gate for the entire sprint. If it can be entered by
manually setting a single boolean, the verification guarantee is meaningless. A compromised or
mistaken flag produces a verification report against an incomplete sprint with no detection.
Recommended change: Phase 4 STEP -1 adds corroborating checks beyond `sealed = true`:
(1) `sprint_close.md` exists and contains a verification readiness statement,
(2) at least one `qa_evidence_EPIC-xx.md` exists with a completed sign-off block,
(3) all ST items in `execution_state.json` have a recorded outcome (not null).
These three checks confirm that Phase 3 actually ran rather than being bypassed. None require
reading large documents in full — they are existence and field checks only.
Expected benefit: Phase 4 entry requires genuine Phase 3 completion. Manual bypass via single
boolean is no longer sufficient.
Token impact: Neutral — three lightweight existence/field checks at preflight.
Effort: Low

---

**IMP-43 — Spec debt item lifecycle is undefined in the playbook**
Area: Lifecycle | Governance
Problem: §6M.2 states the backlog management engine "validates spec debt items (BLG-SPEC-*)
against spec update status." The playbook never defines: what constitutes a spec debt item,
who creates them, what the acceptance criteria for closing one are, who has authority to mark
one resolved, or what "spec update status" means in practice. Spec debt items appear in the
backlog with no defined lifecycle.
Why it matters: Items with no defined closure criteria accumulate indefinitely. The backlog
management engine validates them against an undefined standard, producing meaningless results.
Spec debt is one of the highest-friction recurring sources of technical debt in governed systems.
Recommended change: Define spec debt item lifecycle in `shared_standards.md` or a dedicated
`spec_debt_standard.md`. Minimum definition: (1) creation trigger (deviation noted during
Phase 3 or Phase 4), (2) required fields (BLG-SPEC-* ID, affected spec file, section,
deviation description, canonical requirement, priority P0–P3, owner, target release),
(3) acceptance criteria for closure (spec file updated, canonical requirement met, reviewed
by Head of Specs Team), (4) closing authority (Head of Specs Team sign-off required).
Add a reference from §6M.2 to this definition.
Expected benefit: Spec debt items have a defined lifecycle. Backlog management engine
validation becomes meaningful. Debt accumulation is bounded.
Token impact: Neutral.
Effort: Low

---

**IMP-44 — `run sprint` resume after EPIC merge has no defined state read pattern**
Area: State | Failure Handling | Lifecycle
Problem: §12 instructs "re-invoke `run sprint --cycle <cycle_id>` after each EPIC merge" but
does not define how the engine determines which EPICs are complete and which to start next.
`execution_state.json` presumably holds per-EPIC status, but this is implied rather than
stated. If a session crashes mid-EPIC, it is undefined whether re-invocation resumes the
current EPIC from the last completed ST item or restarts the EPIC from the beginning.
Why it matters: Mid-EPIC crashes are the most common failure mode in a long-running execution.
Without a defined resume pattern, re-invocation may duplicate work, skip completed items, or
restart from an incorrect position — all of which produce inconsistent `execution_state.json`
and `qa_evidence_EPIC-xx.md` records.
Recommended change: Define in `execution_prompt.md` (and reference in §8): on invocation
without `--epic` flag, engine reads `execution_state.json` and selects the first EPIC with
status not in `{merged, returned_to_backlog}`. On invocation with `--epic` flag, engine reads
the EPIC's ST item list from `execution_state.json` and resumes from the first ST item with
status not in `{done, returned_to_backlog}`. Both paths are explicitly documented as the
canonical resume algorithm. Add `last_completed_step` field to each ST item entry in
`execution_state.json` to support sub-item resume.
Expected benefit: Mid-EPIC crashes produce deterministic, correct resume. No work is
duplicated or skipped.
Token impact: Neutral — resume reads existing `execution_state.json` rather than re-reading
full sprint backlog.
Effort: Low

---

**IMP-45 — Dry-run behaviour is undefined and inconsistent across engines**
Area: Governance | Failure Handling | Automation
Problem: Five engines support `--dry-run` (Post-Ship Closure, Sprint Planning, Execution,
`manage roadmap`, `groom backlog`) but no document defines what dry-run must and must not do.
Specific gaps identified from the playbook:
(1) Post-Ship Closure `--dry-run`: "Read all inputs and produce a closure plan without making
    any writes or commits" — this is the only engine with an explicit dry-run definition, and
    it is in the playbook body rather than a shared standard.
(2) Sprint Planning `--dry-run`: "Preview only — no writes or state updates" — minimal
    definition, does not address lock acquisition.
(3) Execution `--dry-run`: "Plan only — no writes, commits, or GitHub operations" — does not
    address `execution_state.json` initialisation, which may be required for the plan to be
    produced.
(4) Phase 1M engines: `--dry-run` described as "always safe — produces change plan without
    writing" — does not address whether the backlog lock is acquired.
No engine defines whether dry-run produces a structured output or free-form prose, what a
downstream agent or human needs to see to validate the plan, or whether dry-run output is
committed or ephemeral.
Why it matters: Dry-run is the primary safety mechanism before committing destructive or
irreversible operations (Post-Ship Closure writes to Class 1 documents; Execution writes
code). An inconsistent or underspecified dry-run undermines this safety mechanism.
Recommended change: Define a dry-run standard in `shared_standards.md` §12 (or new §13):
(1) No writes to any file, (2) No lock acquisition, (3) No external API calls, (4) Reads all
inputs required for the live run, (5) Produces a structured `dry_run_plan.md` in the cycle
folder with: engine name, invocation timestamp, planned writes (file | operation | content
summary), planned state transitions, estimated token cost, and a "SAFE TO PROCEED: Y/N"
summary. Update each engine's dry-run description to reference this standard. Make
`dry_run_plan.md` an entry in the Artefact Register (Class 4, ephemeral — not committed).
Expected benefit: Dry-run becomes a reliable, consistent safety mechanism across all engines.
Agents and humans can validate plans before execution with confidence.
Token impact: Neutral — dry-run already reads all inputs; structured output replaces ad-hoc
prose.
Effort: Low (standard definition) / Medium (updating all five engine prompts)

---

*Session notes:*
*IMP-01–10: Complete as of 2026-03-08.*
*IMP-11–20: Identified 2026-03-08 (v3.3 governance audit). IMP-19 superseded by IMP-29.*
*IMP-21–29: Identified 2026-03-08 (token efficiency audit + lessons learnt architecture).*
*IMP-30–36: Identified 2026-03-08 (six-dimension audit: role charters, first-cycle, mode*
*parity, write scope, idempotency, version consistency).*
*IMP-37–45: Identified 2026-03-08 (amendment sub-lifecycle, dry-run standard, and*
*miscellaneous lifecycle gaps).*
*Recommended implementation order:*
*Tier 1 — Low effort, high correctness value, no dependencies:*
*IMP-36 (version drift) → IMP-33 (mode parity) → IMP-35 (idempotency guards) →*
*IMP-32 (first-cycle guards) → IMP-38 (amendment machine enforcement) →*
*IMP-39 (amendment withdrawal) → IMP-40 (blocked SLA) → IMP-41 (capacity warn) →*
*IMP-42 (execution_state corroboration) → IMP-44 (sprint resume algorithm) →*
*IMP-45 (dry-run standard — definition only)*
*Tier 2 — Medium effort, high token saving:*
*IMP-24 → IMP-25 → IMP-26 (token savings, no dependencies) →*
*IMP-28 (prerequisite for IMP-29) → IMP-23 → IMP-27 → IMP-34 (write scope)*
*Tier 3 — Requires prior decisions or cross-cutting changes:*
*IMP-29 (requires IMP-28 validated) → IMP-17 → IMP-30 → IMP-31 (requires IMP-17) →*
*IMP-43 (spec debt) → IMP-37 (amendment lessons, requires IMP-28 or standalone) →*
*IMP-22 (preflight scope — broad) → IMP-45 (engine updates)*