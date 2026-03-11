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

### Open — Lessons learnt architecture decisions (2026-03-08)

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

**IMP-30 — `design_gate_bypass_authority` has no named role; Head of UX & Design confirmed chartered** ⚠️ PARTIALLY RESOLVED
Area: Governance | Role Charter Completeness
Status: Gap (2) confirmed resolved — `team_charter.md` v1.4 §3.3 includes Head of UX & Design
with explicit authority scope: "Authority role in the Design Gate Engine (Phase 1.5)." The
playbook §2 authority table was the source of the original finding — the actual charter is
correct. No change needed to the charter for this role.
Gap (1) confirmed open: `sprint_planning_prompt.md` STEP -1.3 design gate bypass audit requires
`design_gate_bypass_authority` and `design_gate_bypass_reason` to be written to
`.claude_current_state.json`. The team charter §3.1–§3.3 has no role designated as the holder
of design gate bypass authority. The live `.claude_current_state.json` has `design_gate_required:
true` and `design_gate_status: "Passed"` for the current cycle — the bypass path was not taken —
so the gap has not yet been exercised. But if a cycle requires bypass, the engine halts waiting
for `design_gate_bypass_authority` to be populated with no guidance on which role is authorised
to do so.
Why it matters: An authority field that no role is chartered to fill cannot be self-consistently
enforced. Any agent could claim the authority, making the bypass audit meaningless.
Recommended change: Add to `team_charter.md` §3.3 Head of UX & Design entry: "Holds design
gate bypass authority for cycles where all sprint items are `Design Not Applicable`. Bypass must
be co-confirmed by the Product Owner. Both names are recorded in `.claude_current_state.json`
`design_gate_bypass_authority` field." Update Sprint Planning STEP -1.3 to reference this
authority assignment explicitly.
Expected benefit: Bypass authority is chartered and unambiguous. The audit becomes enforceable.
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

**IMP-32 — First-cycle guards missing across two engines; partially implemented in Release Planning**
Area: State | Lifecycle | First-Cycle Correctness
Problem: First-cycle handling is partially implemented. Release Planning STEP -1.5 has an explicit
skip ("If `prior_cycle` is absent... skip silently") and STEP -1.6 has an explicit exception ("If
this is the very first cycle... skip this check") — these are correctly guarded. Two gaps remain:
(1) IMP-29 meta-review reads `lessons_learnt_cycle.md` from the last 3 cycles — on cycle 1 there
    are zero prior cycles; on cycle 2 there is one. No handling defined for sub-threshold cycle
    counts. Meta-review trigger condition `completed_cycle_count % 3 == 0` would fire on cycle 0
    (before any cycle completes) if the counter starts at 0. Trigger must be `completed_cycle_count
    >= 3 AND completed_cycle_count % 3 == 0`.
(2) Phase 1M state fields (`last_manage_roadmap_utc`, `last_groom_backlog_utc`) will be null on
    first invocation. Any downstream engine that reads these fields without a null guard will either
    fail or treat null as "never run" — correct semantically, but must be explicitly handled.
Why it matters: First invocation is the highest-risk execution path. Silent failures or crashes on
cycle 1 undermine trust in the entire system before any value is delivered.
Recommended change: (1) Update IMP-29 meta-review trigger to `completed_cycle_count >= 3 AND
completed_cycle_count % 3 == 0`. Add explicit handling in Post-Ship Closure: if
`completed_cycle_count < 3`, log "meta-review pending — insufficient cycle history" and skip.
(2) Add null-guard documentation for Phase 1M fields to `shared_standards.md §10` or the Phase
1M engine comments.
Expected benefit: Eliminates remaining first-cycle failure points. Release Planning guards confirmed
correct — no change needed there.
Token impact: Neutral.
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

**IMP-38 — "One active amendment at a time" rule has no machine enforcement** ✅ RESOLVED (confirmed 2026-03-08)
Area: State | Governance | Idempotency
Resolution confirmed: `amendment_cycle_prompt.md` v1.2 STEP -1.3 explicitly checks
`claude/cycles/<original_cycle_id>/amendments/` for any existing amendment with
`amendment_state.json.status` not equal to `Sealed` or `Withdrawn`. This is a hard gate in
both modes. No change required.

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

---

### Open — Direct prompt audit findings (2026-03-08)

*Findings from release_planning_prompt.md v2.13, shared_standards.md v1.4, amendment_cycle_prompt.md v1.2.*

---

**IMP-46 — §10.1 issue_import references stale source for EPIC descriptions**
Area: Prompt | Cross-Document Consistency
Problem: `release_planning_prompt.md §10.1` states: "For EPIC descriptions, source from
`release_plan.md ## Execution Plan` section." Since v2.11, STEP 3 writes compact table rows to
`## Execution Plan` (per IMP-08) — not full descriptions. An issue import generated from §10.1
would contain one-line table cell content as the issue body — insufficient for a useful GitHub
issue. §10.2 (GitHub automation) iterates `stage4_backlog_slice.md` directly, which does contain
full descriptions. The two issue generation paths are now inconsistent with each other and §10.1
is stale relative to the v2.11 consolidation.
Why it matters: Issue import produces low-quality, incomplete issue bodies. The agent following
§10.1 faithfully will generate unusable content. Inconsistency between §10.1 and §10.2 means the
two issue generation paths produce materially different outputs for the same sprint.
Recommended change: Update §10.1: remove the line "For EPIC descriptions, source from
`release_plan.md ## Execution Plan` section." Replace with: "For EPIC descriptions, source from
`stage4_backlog_slice.md` (same source as §10.2 GitHub automation)." The backlog slice is the
canonical source for all issue content regardless of generation path.
Expected benefit: Both issue generation paths produce consistent, complete issue bodies.
Token impact: Neutral.
Effort: Low

---

---

### Open — Second direct prompt audit findings (2026-03-08)

*Findings from execution_prompt.md v1.6, post_ship_closure.md v1.4, sprint_planning_prompt.md v1.4.*

---

**IMP-55 — `next_cycle_unblocked` lifecycle confirmed correct; false positive resolved** ✅ RESOLVED
Area: State | Lifecycle
Resolution confirmed: `delivery_verification_prompt.md` STEP 9 explicitly sets
`next_cycle_unblocked = true` for BOTH `Verified` AND `Verified_with_deviations` status outcomes.
Only `Not_Verified` results in `next_cycle_unblocked = false`. The concern that
`Verified_with_deviations` might produce `false` and block Post-Ship Closure was a false positive
based on ambiguous playbook language — the actual prompt is unambiguous.
The `post_ship_closure.md` STEP -1.1 check (`next_cycle_unblocked must be true`) is therefore
correctly consistent with the delivery verification outcome. No change required to either prompt.
The only remaining question — Post-Ship Closure has no defined path if `next_cycle_unblocked`
is absent entirely (e.g. if Phase 4 was never run) — is covered by STEP -1.1's status check
(`status must be Verified or Verified_with_deviations`) which would catch this case first.

---

**IMP-57 — Sprint Planning sources-of-truth table references `stage3_execution_plan.md` and not `release_plan.md`; `next_cycle_unblocked` not set by Sprint Planning** *(combined gap note)*
Area: State | Lifecycle
Problem: Two small gaps identified from sprint_planning_prompt.md:
(1) §5 table lists `stage3_execution_plan.md` as a required input with no fallback for
    schema v2 cycles. This is the same issue as IMP-52 — noting here as a linked reference.
    IMP-52 covers the remediation.
(2) Sprint Planning STEP 7 sets `sprint_sealed = true` in `.claude_current_state.json` but
    does not set `next_cycle_unblocked`. `next_cycle_unblocked` is set by Delivery Verification
    (Phase 4) and checked by Release Planning (Phase 1B STEP -1.6) and Post-Ship Closure STEP
    -1.1. Sprint Planning correctly does not set this field. The lifecycle responsibility is
    correctly scoped — noting here to confirm the chain is intact and no gap exists in Sprint
    Planning for this field.
This IMP documents the confirmation that Sprint Planning's state writes are correctly scoped.
No change required to Sprint Planning for this field.
Token impact: N/A.
Effort: N/A — documentation only.

---

---

### Open — Third direct prompt audit findings (2026-03-09)

*Findings from delivery_verification_prompt.md v1.2, .claude_current_state.json (live), team_charter.md v1.4, prompt_change_log.md v1.0.*

---

**IMP-60 — `v2_0_gates` in `.claude_current_state.json` has a manually-tracked condition with no automation**
Area: State | Governance
Problem: The live `.claude_current_state.json` contains:
```json
"v2_0_gates": {
  "gate_1_logging": true,
  "gate_2_api_versioning": true,
  "gate_3_qa_planning": false,
  "gate_3_auto_advance": "Once QA planning session for notification delivery documented — see DL-003"
}
```
`gate_3_qa_planning` is `false` with an `auto_advance` condition expressed as a free-text string.
No engine reads this block, evaluates the condition, or advances the gate. The condition references
a document (`DL-003`) that is not in any reviewed prompt's required-files list. The gate block
follows a naming convention (`v2_0_gates`) suggesting it governs v2.0 requirements, but no prompt
references this block in its preflight checks.
Why it matters: Gates that are not machine-enforced are not gates — they are reminders. A
false-value gate with a text-only advance condition can remain `false` indefinitely with no
enforcement. If v2.0 has a quality or release readiness dependency on QA planning for notification
delivery, that dependency is invisible to every governed engine.
Recommended change: Decision required: (1) If `v2_0_gates` is a legitimate release readiness
gate, identify which engine should check it at preflight (likely Release Planning or Sprint
Planning for the relevant cycle) and add the check. Define `DL-003` in the artefact register.
(2) If the gate has already been superseded or is no longer relevant: remove the block from
`.claude_current_state.json` and document the decision in the decisions record. Free-text
`auto_advance` conditions must not remain in machine-read state files.
Expected benefit: State file reflects only machine-enforceable governance conditions. No silent
obligations carried invisibly across cycles.
Token impact: Neutral.
Effort: Low (decision) / Low (implementation once decided)

---

# Implementation Plan — Sprint Planning Operational Playbook
**Generated:** 2026-03-09 | **Updated:** 2026-03-10
**Source:** review.md (IMP-11 through IMP-62, resolved items removed)
**Principle:** Each file is touched exactly once. Batches are ordered by criticality × improvement value.

---

## How to read this plan

Each batch names every file that will be edited and lists every IMP that edit satisfies. Work one batch at a time, version-bump every modified file, and add a single `prompt_change_log.md` entry per file per batch. Do not start Batch N+1 until Batch N is committed and pushed.

Resolved items excluded: IMP-01–10, IMP-19, IMP-30 gap (2), IMP-38, IMP-55, IMP-57.

---

## ✅ BATCH 5 — COMPLETE (2026-03-10)

**IMPs resolved:** IMP-28, IMP-35 (gap 2), IMP-37, IMP-53, IMP-54
**Files updated:** `lessons_learnt_prompt.md` → v1.5, `execution_prompt.md` → v2.0, `delivery_verification_prompt.md` → v1.3, `post_ship_closure.md` → v1.7, `amendment_cycle_prompt.md` → v1.5, `OPERATIONAL_GUIDE.md` → v3.9, `prompt_change_log.md` (appended)
**Verified by:** §14 governance table and §6B.8, §8, §9, §10 phase headers in playbook v3.9.

### `lessons_learnt_prompt.md` (→ v_next)
| IMP | Change |
|-----|--------|
| IMP-26 | STEP 3 risk register entries: add `escalation_ref` field (null or ESC-id). Update escalation subroutine reference to §4: "ESC entries store decision/status only; risk context lives in `release_plan.md` via escalation_ref." |

### `sprint_planning_prompt.md` (→ v1.7)
| IMP | Change |
|-----|--------|
| IMP-23 | STEP 6 `sprint_backlog.md` template: ST item Acceptance Criteria field becomes a reference — "AC: see `stage4_backlog_slice.md#ST-xx`" instead of full AC duplication. Sprint backlog is a sequencing and ownership document. Add note: "Execution engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`." |
| IMP-25 | STEP 6: alongside `sprint_backlog.md`, produce `sprint_backlog_index.json` — `{EPIC-xx: {st_items: [ST-xx,...], backlog_slice_refs: [...]}}`. Add to §6 Write Scope. |

### `execution_prompt.md` (→ v1.9)
| IMP | Change |
|-----|--------|
| IMP-25 | STEP -1 and STEP 0: add instruction — "Load `sprint_backlog_index.json` to identify which ST items belong to the scoped EPIC. Read only the relevant slice of `sprint_backlog.md` using the index line ranges, not the full document." |

### `post_ship_closure.md` (→ v1.6)
| IMP | Change |
|-----|--------|
| IMP-27 | For each step, add field-level read target: STEP 0 — `verification_report.md`: read `§1 verification_status` and `§4 deviation register` only. `sprint_close.md`: read verification readiness statement and deviations list. `execution_state.json`: read `epics` outcome map. STEP 8 — `lessons_learnt.md` files: read action item sections only (not full prose). Add explicit "read target" notes to each step that loads a large input document. |

---

## BATCH 6 — Meta-review activation (depends on Batch 5 validated across one full cycle)

**Rationale:** Do not activate until `lessons_learnt_cycle.md` has been produced for at least one complete cycle with IMP-28 in effect. Attempting to scan a structured file that doesn't yet exist produces a first-cycle failure.

### `post_ship_closure.md` (→ v_next after one IMP-28 cycle)
| IMP | Change |
|-----|--------|
| IMP-29 | STEP 10 global state update: add meta-review trigger check — "If `completed_cycle_count >= 3 AND completed_cycle_count % 3 == 0`: invoke meta-review subroutine before finalising STEP 10." Meta-review reads `lessons_learnt_cycle.md` from the last 3 cycles. Scope: all phases. Pattern detection: friction items appearing in 2 of 3 cycles = mandatory action-now. |
| IMP-32 (gap 1) | Meta-review trigger: confirm trigger uses `completed_cycle_count >= 3 AND completed_cycle_count % 3 == 0` (not just `% 3 == 0`). Add explicit skip: "If `completed_cycle_count < 3`: log 'meta-review pending — insufficient cycle history' and skip." |

### `shared_standards.md` (→ v_next)
| IMP | Change |
|-----|--------|
| IMP-32 (gap 2) | §10 Lifecycle Guard or §10.1 first-cycle notes: add null-guard documentation for Phase 1M fields — "Fields `last_manage_roadmap_utc` and `last_groom_backlog_utc` will be null on first invocation. Engines reading these fields must treat null as 'never run' and continue without error." |

---

## BATCH 7 — Governance decisions required (cannot proceed without named-authority decision) ⏳ AWAITING DECISIONS

**Rationale:** These IMPs require a human decision before implementation. Each is documented as a decision prompt — the output of the decision determines the implementation.

### Decision 1: Class 8 / Proof of Gate (IMP-17, IMP-31)
**Owner decision required:** Head of Specs Team + Product Owner
**Question:** Activate Class 8 (Proof of Gate) documents, or formally defer?
- If activate: name clearing authority per gate type → add to `team_charter.md` §3 authority table + relevant agent charters. Add production steps to relevant engines. Add to Artefact Register.
- If defer: playbook §3 note already added in Batch 2 — no further action needed.

### Decision 2: `v2_0_gates` block (IMP-60)
**Owner decision required:** Product Owner + PMO Lead
**Question:** Is `gate_3_qa_planning` still a live release readiness gate?
- If active: identify which engine checks it; add preflight check; define DL-003 in artefact register.
- If superseded: remove block from `.claude_current_state.json`; file a decisions record closing it.

### Decision 3: Design gate bypass authority (IMP-30)
**Owner decision required:** Head of Specs Team
**Files (once decided):** `team_charter.md` §3.3 Head of UX & Design entry, `sprint_planning_prompt.md` STEP -1.3 note.
**Change:** Name the role(s) authorised to populate `design_gate_bypass_authority`. Recommendation: Head of UX & Design (primary) + Product Owner (co-confirmation required). Add to §3.3 charter entry.

---

## ✅ BATCH 8 — COMPLETE (2026-03-11)

**IMPs resolved:** IMP-11, IMP-13, IMP-14, IMP-15, IMP-16, IMP-22, IMP-33, IMP-43
**Files updated:** `shared_standards.md` → v1.9, `release_planning_prompt.md` → v2.18, `delivery_verification_prompt.md` → v1.4, `post_ship_closure.md` → v1.8, `roadmap_prompt.md` → v2.1, `OPERATIONAL_GUIDE.md` → v3.12, `prompt_change_log.md` (appended)
**Verified by:** §14 governance table and §6, §6B, §9, §10 phase headers in playbook v3.12.

## Batch 8 — Remaining governance and lifecycle completeness (no blocking dependencies)

**Rationale:** All medium-complexity, independent improvements. Can be done in any order within this batch but grouped here as the final completeness sweep.

### `shared_standards.md` (→ v_next)
| IMP | Change |
|-----|--------|
| IMP-22 | Add `shared_preflight_fields` list specifying minimum field set required from `.claude_current_state.json` per engine type (e.g. Release Planning needs: `status, active_cycle, next_cycle_unblocked, post_ship_complete`; Execution needs: `status, active_cycle, amended_backlog_slice_path, sprint_sealed`). Add section-scoped read instruction: "Engines must read only the fields specified in their shared_preflight_fields entry from `.claude_current_state.json`, not the full file, unless a field outside the set is explicitly required by a named step." |
| IMP-43 | Add §13 Spec Debt Item Lifecycle (or reference to `spec_debt_standard.md`): creation trigger, required fields (BLG-SPEC-* ID, spec file, section, description, canonical requirement, priority P0–P3, owner, target release), acceptance criteria for closure (spec updated, reviewed by Head of Specs Team), closing authority (Head of Specs Team sign-off). |

### `release_planning_prompt.md` (→ v_next)
| IMP | Change |
|-----|--------|
| IMP-11 | Lifecycle Guard (STEP -1 or Lifecycle Guard section): add `Amendment_In_Progress` to the explicit halt states. "If `status = Amendment_In_Progress`: halt — an amendment is in progress for the active cycle. Resolve the amendment before opening a new release plan." |
| IMP-16 | STEP -1 or §15 Shared Standards reference: add stale lock protocol — "If `claude/backlog/.lock` exists from a prior cycle: (1) verify lock timestamp against stale threshold. (2) If stale (owning cycle closed or >72 hrs inactive): PMO Lead records removal in current cycle's escalation log with stale evidence, then removes the lock. (3) PMO Lead approval required before removal." Reference team_charter §6 Shared Write Concurrency Constraint. |

### `delivery_verification_prompt.md` (→ v_next)
| IMP | Change |
|-----|--------|
| IMP-14 | STEP 5 (Test Scenario Coverage): add `test_scenario_gaps` structured table to `verification_report.md` — fields: gap_id, EPIC, description, qualifying_reason, disposition (`backlog_item_created | not_applicable | deferred`). Add to Phase 4 exit criteria: "All test scenario gaps must have a disposition recorded." STEP 4.2 completion condition: all gaps have disposition. |
| IMP-15 | Add stale idea detection note: "Items in the authoritative backlog slice with `status = parked` in 3 or more consecutive cycle backlog slices must be surfaced for mandatory PO disposition at Delivery Verification. Record in `verification_report.md` §5 as 'stale item requiring disposition.'" (Lightweight version: detection only; enforcement in backlog management engine.) |

### `post_ship_closure.md` (→ v_next)
| IMP | Change |
|-----|--------|
| IMP-15 | STEP 3 Backlog Reconciliation: add check — "Identify items in `backlog.md` marked `parked` with a `cycle_id` reference from 3 or more completed cycles. Surface these to the PMO Lead for mandatory PO disposition before the next release plan opens." Record in closure record §6 Outstanding Actions. |

### `roadmap_prompt.md` (→ v_next)
| IMP | Change |
|-----|--------|
| IMP-13 | STEP 9 (or equivalent net-zero verification step): add count check — "Count Add decisions vs. confirmed-Kill or confirmed-Defer decisions in this run. If additions > kills: halt and surface the displacement gap to the Product Owner. The net-zero rule is mode-independent." |
| IMP-33 | Add note to zero-sum displacement rule section: "This rule applies in both strict and standard mode. It is a governance constraint, not relaxed by `--mode standard`." (Mirrors the playbook §6B note added in Batch 2.) |

---

## Summary table

| Batch | Status | Files touched | IMPs addressed | Priority basis |
|-------|--------|--------------|----------------|----------------|
| 6 | — | `post_ship_closure.md`, `shared_standards.md` | 29, 32 | Meta-review; gated on one full Batch 5 cycle |
| 7 | ⏳ Awaiting decisions | `team_charter.md` + various (post-decision) | 17, 30, 31, 60 | Decision-gated; human input required |
| 8 | ✅ Complete (2026-03-11) | `shared_standards.md`, `release_planning_prompt.md`, `delivery_verification_prompt.md`, `post_ship_closure.md`, `roadmap_prompt.md` | 11, 13, 14, 15, 16, 22, 43 | Completeness sweep |

† IMP-40 and IMP-48 may already be present in `shared_standards.md` v1.7. Verify before re-applying in Batch 3.

**Open IMPs remaining: 37** (Batch 5 closed: IMP-28, 35(gap2), 37, 53, 54)
**IMPs requiring human decision before implementation: 4 (Batch 7)**
**Batch 6 is next — gated on one full Batch 5 cycle (first `lessons_learnt_cycle.md` produced).**

