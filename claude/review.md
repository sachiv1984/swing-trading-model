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

**IMP-18 — Sprint Planning goal confirmation has no state file; §11 partially addresses via file-based resume**
Area: State | Failure Handling
Status: Confirmed from `sprint_planning_prompt.md` §11 Resumability — a three-condition resume
check exists:
- If `sprint_goal.md` exists with sign-off: STEP 2 complete, skip
- If `sprint_goal.md` exists without sign-off: resume at STEP 2 sign-off gate
- If `sprint_goal.md` absent: fresh run from STEP 2
This is better than the playbook implied. File existence + sign-off presence is a reasonable
proxy for `drafted | confirmed` state. The gap narrows to: if the engine crashes after creating
`sprint_goal.md` but before populating the `[AWAITING SIGN-OFF]` fields, the file exists with
incomplete content — the §11 check would branch to "exists without sign-off" and re-run STEP 2
correctly. This is correct behaviour. The gap is effectively closed for normal crash-resume
paths.
One smaller gap remains: `.claude_current_state.json` confirmed from the live file has no
`sprint_goal_status` field. The state file has `sprint_goal_path` pointing to the file, but no
`confirmed`/`drafted` flag. If the state JSON is used as the source of truth by a downstream
engine (e.g. a future dashboard or status query), it cannot determine whether the sprint goal
is pending confirmation without reading the file.
Recommended change (narrowed): No structural change required — §11 file-based resume is
correct for the engine's own resume path. Add `sprint_goal_status: "confirmed"` to the
`.claude_current_state.json` STEP 7 write block in `sprint_planning_prompt.md`. This provides
a machine-readable confirmation signal for downstream consumers without requiring a separate
state file. Values: `not_started | awaiting_po | confirmed`.
Expected benefit: Machine-readable sprint goal status in global state. Downstream queries don't
require reading `sprint_goal.md` to determine planning completeness.
Token impact: Neutral — trivial field addition to an existing write.
Effort: Low

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

**IMP-33 — Mode parity: AC contradiction confirmed resolved; two gaps remain**
Area: Governance | Prompt–Playbook Alignment | Mode Parity
Problem: Originally three mode parity failures. Gap (1) is confirmed resolved:
(1) ✅ RESOLVED — Sprint Planning: `sprint_planning_prompt.md` §7 and STEP 6.2 are internally
    consistent. Standard mode permits `[AC REQUIRED]` placeholders during planning but explicitly
    blocks sealing until all are resolved ("The sprint backlog may not be signed off while any item
    has an unresolved `[AC REQUIRED]` placeholder"). STEP 6.2 sign-off gate lists this as a required
    condition. The contradiction described was between the playbook §7.3 summary and the prompt —
    the prompt itself is correct. No change needed to the prompt.
Two gaps remain:
(2) Roadmap Engine STEP 5 zero-sum displacement rule ("no candidate advances without naming a
    displacement") has no mode variant defined. It is written as an absolute rule but lives in a
    prompt that accepts `--mode`. It is unclear whether standard mode relaxes or enforces this rule.
(3) Execution Engine STEP -1.5 and STEP 3 use `strict` vs `standard` behaviour distinctions. The
    `execution_prompt.md` STEP -1.5 states: "In `strict` mode: halt and report which items are
    missing criteria. In `standard` mode: flag as a blocker, classify the item as
    `delegated_decision`, and continue." This is well-defined. However §2 Invocation Rule states
    "`strict`: halt on any ambiguity" — "ambiguity" is still undefined. Section 5.1 classification
    rules do provide guidance ("If classification is ambiguous: classify as `delegated_decision`")
    but this is not a substitute for defining what constitutes ambiguity in the strict-mode halt
    context. Agents in strict mode must make a judgment call about what constitutes an ambiguous item
    beyond classification ambiguity.
Why it matters: The zero-sum rule ambiguity (gap 2) makes the Roadmap Engine non-deterministic
across modes. The "ambiguity" definition gap (gap 3) is less severe now that classification
fallback is documented, but the strict-mode halt trigger remains underspecified.
Recommended change: (2) Declare the zero-sum rule as mode-independent (hard rule regardless of
`--mode` value) in the roadmap prompt. Add a note: "This rule applies in both strict and standard
mode — it is a governance constraint, not a quality gate." (3) Add a definition block to
`execution_prompt.md` §2 or §8: "Ambiguity: a condition in which the engine cannot determine with
confidence which action to take from the acceptance criteria, spec, and execution state alone.
Examples: missing spec reference for a `delegated_backend` item; AC field present but not
testable; dependency chain that cannot be resolved from `execution_state.json`." This makes the
strict-mode halt trigger explicit rather than judgment-dependent.
Expected benefit: Deterministic mode behaviour for the two remaining gaps. Agents resolve
conditions consistently across runs.
Token impact: Neutral.
Effort: Low

---

**IMP-34 — Post-Ship Closure write scope exists but Class 1 writes are not field-scoped** ⚠️ PARTIALLY RESOLVED
Area: Governance | Write Scope Enforcement
Status: `post_ship_closure.md` §5 Write Scope Restriction exists and is detailed — better than the
playbook implied and on par with Release Planning §7 and Amendment §8. The following writes are
explicitly permitted with constraints:
- `docs/product/changelog.md` (append new version entry)
- `claude/roadmap/current_roadmap.md` (status update + version headers only)
- `claude/backlog/backlog.md` (mark shipped items complete; add missing Phase 4 items; no other changes)
- Scope and decisions documents (status → Superseded only)
- Canonical spec files (deviation note compliance fixes only)
- Operational docs (reconciliation only)
- `Specs_Index.md` (mark resolved items; add new gaps)
The two remaining gaps:
(1) `current_roadmap.md` write is scoped to "status update + version headers only" but does not
    define which fields constitute "version headers." STEP 2 expands this to "mark ✅ Complete,
    update Current Version header, update Next planned release header, update release summary table"
    — the write scope is narrower than what STEP 2 actually does. The write scope says "version
    headers only" but the step writes to summary tables and completion flags.
(2) Canonical spec writes are scoped to "deviation note compliance fixes only — missing required
    fields per §3 Known Deviation Standard." The scope restriction correctly excludes new spec
    edits. However, STEP 5 "standard mode" permits adding missing fields — this is a write to
    a canonical spec that was not present in the original Phase 3 deviation record. The authority
    for Post-Ship Closure to add fields to canonical specs that were missed in Phase 3 is not
    established in the team charter.
Recommended change: (1) Expand the `current_roadmap.md` write scope entry to match STEP 2 exactly:
"status update, ✅ Complete marker, version header updates, release summary table status column."
Any write beyond this list is a violation. (2) Add a note to canonical spec write scope: "Deviation
compliance corrections require Head of Specs Team awareness. In standard mode corrections: notify
Head of Specs Team via sprint_escalations or closure record §6 — do not silently add fields."
Expected benefit: Write scope and step behaviour are aligned. Class 1 document writes are
transparent to the owning authority.
Token impact: Neutral.
Effort: Low

---

**IMP-35 — Idempotency guards absent or undefined for three write operations (one confirmed resolved)**
Area: State | Failure Handling | Idempotency
Problem: Originally four idempotency gaps identified. Gap (1) is now confirmed resolved:
(1) ✅ RESOLVED — Backlog slice commit: `release_planning_prompt.md` STEP 4 defines the marker
    format explicitly (`<!-- release-plan-marker: RP:<release>:<cycle_id> -->`), performs a
    pre-write check, and skips the write if the marker is already present. True idempotency
    confirmed. Amendment STEP 5 follows the same pattern with its own marker. No change needed.
Three gaps remain:
(2) Lessons learnt append: the playbook references an "idempotency marker" but does not define its
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
Recommended change: (2) Lessons learnt append: check for existing section
header `## Phase <X> — <cycle_id>` before appending; skip if present. (3) Prompt change log:
check for existing entry with matching prompt name + version before appending; skip if present.
(4) `sync gh`: use GitHub issue labels containing cycle_id as the idempotency key — check label
before create; update if label exists.
Expected benefit: All three remaining write operations become safe to re-run. Resumability
guarantee is restored for these paths.
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

**IMP-37 — Amendment lessons learnt feeds a standalone file rather than the consolidated cycle record**
Area: Lifecycle | Governance
Problem: STEP 8 of `amendment_cycle_prompt.md` exists and produces `amendment_lessons.md` —
better than the playbook implied. However, it invokes `lessons_learnt_prompt.md §3` to produce a
standalone file rather than appending to `lessons_learnt_cycle.md` (IMP-28 consolidated record).
Amendment lessons are therefore invisible to the meta-review (IMP-29), which reads
`lessons_learnt_cycle.md` from the last 3 cycles. Amendment friction — the highest-signal events
in the lifecycle — never enters the improvement loop.
Why it matters: Amendment cycles are emergency events — exactly the situations most likely to
generate actionable process improvements. A standalone file that is not scanned by meta-review
means amendment patterns (recurring blocker types, ratification delays, capacity ceiling
violations) are never surfaced systemically.
Recommended change: Update STEP 8 of `amendment_cycle_prompt.md`: after producing
`amendment_lessons.md`, append a `## Amendment — <AMD-id>` section to
`lessons_learnt_cycle.md` using the same structured table schema as other phases. If
`lessons_learnt_cycle.md` does not yet exist for this cycle (IMP-28 not yet implemented):
produce `amendment_lessons.md` as before. When IMP-28 is implemented, migrate to append-only.
Expected benefit: Amendment friction enters the meta-review improvement loop. Amendment patterns
become detectable across cycles.
Token impact: Costs slightly — one additional structured append per amendment cycle.
Effort: Low
Dependency: IMP-28 (for full integration; partial value without it)

---

**IMP-38 — "One active amendment at a time" rule has no machine enforcement** ✅ RESOLVED (confirmed 2026-03-08)
Area: State | Governance | Idempotency
Resolution confirmed: `amendment_cycle_prompt.md` v1.2 STEP -1.3 explicitly checks
`claude/cycles/<original_cycle_id>/amendments/` for any existing amendment with
`amendment_state.json.status` not equal to `Sealed` or `Withdrawn`. This is a hard gate in
both modes. No change required.

---

**IMP-39 — Amendment withdrawal has no defined procedure, state transition, or record** ⚠️ PARTIALLY RESOLVED
Area: Lifecycle | State | Failure Handling
Status: `amendment_cycle_prompt.md` §10 Withdrawal section exists with an explicit procedure —
better than the playbook implied. State transition, `.claude_current_state.json` update, and
permanent record requirement are all defined. One gap remains unaddressed:
If the amendment reached STEP 5 (backlog update) before withdrawal, `backlog.md` contains
amendment changes that are no longer active. §10 defines no rollback of the backlog write.
The original `stage4_backlog_slice.md` is stated as "the active source of truth" but `backlog.md`
has been modified and the amendment marker is present. Sprint Planning reads `backlog.md` — it
would see the withdrawn amendment's changes.
Recommended change: Add to §10 Withdrawal: if `backlog_txn.json` state = `committed` (STEP 5
completed), a backlog rollback step is required before withdrawal can complete. Rollback: remove
the amendment marker section from `backlog.md` using the same lock/transaction protocol, then
update `backlog_txn.json` state = `rolled_back`. The withdrawal procedure should be invoked via
`amend cycle --withdraw` only after rollback completes.
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

**IMP-41 — Capacity `warn` acknowledged via `over_allocation_accepted` but no dedicated audit field** ⚠️ PARTIALLY RESOLVED
Area: Lifecycle | Governance
Status: Confirmed from live `.claude_current_state.json` — the current cycle has:
- `release_plan.capacity_check: "warn"` (set at Release Planning)
- `sprint_planning.over_allocation_accepted: true` (set at Sprint Planning)
The `warn` was acknowledged — the Product Owner accepted over-allocation, recorded in the sprint
planning block. The practical risk described (entering execution without any acknowledgement) did
not materialise in this cycle. The acknowledgement mechanism used was `over_allocation_accepted`
rather than a dedicated `capacity_warn_acknowledged` field.
Remaining gap: The two fields serve overlapping but distinct purposes. `over_allocation_accepted`
confirms capacity was discussed and accepted. `capacity_check: "warn"` is the Release Planning
engine's output before sprint scope was selected. After sprint scope selection, the actual
utilisation may be lower than the warn threshold (e.g. if under-capacity items were deferred).
The `over_allocation_accepted` flag tells you the PO accepted the scope, not that the warn was
specifically reviewed and acknowledged as a known risk. No `capacity_warn_acknowledged` field
exists in the state file — the distinction is not captured.
The second gap: Sprint Planning STEP -1 has no check on `release_plan.capacity_check`. The
`warn` is only surfaced in STEP 0 ("If the check result was `warn`: surface the warning to the
user before proceeding") — advisory, not gated. In strict mode it should halt pending explicit
PO acceptance; in standard mode it should require acknowledgement before seal.
Recommended change (narrowed): Sprint Planning STEP -1 (or STEP 0) should read
`release_plan.capacity_check` from `.claude_current_state.json` and, if `warn`, require the
Product Owner to provide a one-line acknowledgement before proceeding to scope selection (not
just before seal). Add `capacity_warn_acknowledged: true` to the STEP 7 state write when the
PO acknowledgement is recorded. This separates the risk acknowledgement from the scope
acceptance decision. The field already named in `sprint_planning_notes.md` structure should
be the canonical capture point.
Expected benefit: Clear audit trail distinguishing "capacity risk acknowledged" from "scope
accepted." Downstream queries can identify which cycles entered execution with an unresolved
capacity signal.
Token impact: Neutral — one additional field read at Sprint Planning preflight.
Effort: Low

---

**IMP-42 — Phase 4 corroborating checks confirmed; Post-Ship STEP -1 has one remaining gap** ⚠️ PARTIALLY RESOLVED
Area: State | Failure Handling
Status: `delivery_verification_prompt.md` STEP -1 provides strong corroborating checks — better
than the playbook implied:
- STEP -1 (first action): reads `execution_state.json`, confirms `sealed = true`
- STEP -1.2: reads `sprint_close.md` verification readiness statement; halts if any of the three
  fields (`spec references populated`, `deviations filed`, `QA evidence logs complete`) are `No`
- STEP -1.3: confirms `qa_evidence_EPIC-xx.md` exists for every merged EPIC with DoQ sign-off
These three checks precisely match the recommendations in this IMP. Phase 4 entry is
well-governed — the corroborating checks exist and are hard gates. One narrower gap remains:
`post_ship_closure.md` STEP -1.2 checks only `execution_state.json.sealed = true`. It does not
verify the verification readiness statement within `sprint_close.md`. An execution record sealed
against a close record with readiness gaps would pass Post-Ship preflight even though Phase 3
documented an incomplete state.
Recommended change: Add to `post_ship_closure.md` STEP -1 (after the sealed check):
"Read `sprint_close.md` — verify the verification readiness statement: all three fields must be
`Yes`. If any field is `No`: halt. A close record that documented readiness gaps should not
proceed to Post-Ship Closure without a PMO Lead note explaining how they were resolved."
Expected benefit: Post-Ship Closure only runs against cycles where Phase 3 confirmed readiness.
Token impact: Neutral — one field check at preflight.
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

**IMP-44 — `run sprint` resume algorithm is partially defined; sub-item resume not specified**
Area: State | Failure Handling | Lifecycle
Status: `execution_prompt.md` §10 Resumability and §10.1 Block Re-Evaluation define the resume
pattern more explicitly than the playbook implied:
- On invocation: reads `execution_state.json`, resumes from first item with status
  `not_started`, `in_progress`, or `blocked_*`
- Never re-executes items already marked `done` or `merged`
- Block re-evaluation explicitly defined: checks unblock criteria on each resume
- STEP -1 explicitly reads `execution_state.json` as first action and branches on whether
  it exists (resume) or not (fresh run)
This is substantially better than the playbook summary suggested. The EPIC-level resume pattern
is handled by §10's item-status-based resume. One gap remains:
The STEP 4 merge gate outputs a re-invocation reminder: "re-invoke `run sprint --cycle <cycle_id>`
after each subsequent EPIC merge." On re-invocation, the engine resumes from the first item with
status not in `{done, merged}`. This is correct for inter-EPIC resume. However, for mid-EPIC
crash (engine fails mid-STEP-3 loop for a specific ST item), the resume is from the first ST item
with status `in_progress`. The `in_progress` status is set at item start but there is no record
of which sub-step within STEP 3.1 was last completed. If the crash occurred after commit but
before `execution_state.json` update, the resume algorithm will re-attempt the commit — the
idempotency is provided by the existing git commit format (`[EPIC-xx][ST-xx]`) but only if the
issue and branch state can be re-read to determine whether the commit already exists.
Why it matters: The most common crash point is between write-to-disk and state-file-update. The
existing resume pattern handles this for items, not for the operations within an item execution.
Recommended change: Narrow the IMP to the sub-item gap only. Add `last_completed_substep` field
to each ST item entry in `execution_state.json` with values: `not_started | commit_pending |
committed | issue_updated | done`. The resume algorithm for `in_progress` items reads this field
to determine the safe re-entry point within STEP 3.1. This prevents duplicate commits and
duplicate issue updates on crash recovery.
Expected benefit: Mid-item crashes produce deterministic, correct resume. Existing EPIC-level and
item-level resume confirmed correct — no change needed there.
Token impact: Neutral — reads one additional field per `in_progress` item on resume.
Effort: Low

---

**IMP-45 — Dry-run is defined in three engines but lacks a shared standard; execution dry-run has a state initialisation gap**
Area: Governance | Failure Handling | Automation
Status: Confirmed from actual prompt text — better than the playbook summary suggested:
(1) ✅ Post-Ship Closure: §2 defines "read all inputs and produce a full closure plan — listing
    every write that would be made, every step outcome, and any flags — without making any writes,
    state updates, or commits. Dry-run output is the deliverable; the routine ends after producing
    it." §5 adds "dry-run exception: none of the permitted writes below may be made." STEP 0
    exits after producing the closure plan. STEP -1.6 skips the write test. §9 invariant: "dry-run
    produces no side effects." This is a complete, well-defined dry-run implementation.
(2) ✅ Sprint Planning: §2 defines "read all inputs and produce a planning preview without writing
    any artefacts or updating state. The pip-audit scan (STEP -1.8) still runs — it is a read-only
    operation." This is adequate — pip-audit exception is explicitly noted.
(3) ✅ Sprint Execution: §2 defines "--dry-run optional: plan execution without performing writes,
    commits, or GitHub operations. Produce a dry-run report only." Less detailed than Post-Ship
    but functionally clear.
One gap confirmed: Sprint Planning and Sprint Execution dry-run produce a "preview" or "report"
(free-form prose implied), while Post-Ship produces a structured closure plan. There is no common
output schema across the three. Additionally, the Sprint Execution dry-run says "no writes,
commits, or GitHub operations" but does not address `execution_state.json` initialisation —
the engine needs to know what items are in scope to produce the plan, which normally requires
reading or creating the execution state. If execution_state.json does not exist, the dry-run
cannot work without at least a read-only parse of the backlog slice.
Recommended change: Add a dry-run standard to `shared_standards.md` §12 defining:
(1) No writes to any governance, cycle, or source file. (2) No lock acquisition. (3) No
external API calls (no `gh` CLI, no `git` writes). (4) Reads all inputs required for the live
run. (5) Output schema: a structured `dry_run_plan.md` (or inline structured report) listing
engine name, invocation timestamp, planned writes (file | step | content summary), planned
state transitions, planned GitHub operations, and a SAFE TO PROCEED: Y/N summary. (6) For
engines with state initialisation (Sprint Execution): dry-run parses the backlog slice
read-only; it does not write execution_state.json. Update Sprint Execution §2 to note: "In
dry-run mode, execution_state.json is not created — the plan is produced from the backlog slice
directly." Update Sprint Planning §2 to reference §12 standard for output format.
Expected benefit: Dry-run output becomes structured and machine-readable across all engines.
The execution dry-run state initialisation gap is resolved.
Token impact: Neutral — dry-run reads the same inputs; structured output replaces ad-hoc prose.
Effort: Low (standard definition) / Low (updating the three affected prompts — all already have dry-run support)

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

**IMP-47 — STEP -1.4 temp file has no defined cleanup step and may leave an unclassed artefact**
Area: Governance | Write Scope
Problem: `release_planning_prompt.md` STEP -1.4 creates a temp file under `claude/cycles/<cycle_id>/`
and states: "Remove it if possible; if not, keep it and record it in the run manifest." The Write
Scope (§7) allows writes to `claude/cycles/<cycle_id>/*`, so the temp file is technically
within scope. However if it cannot be removed it becomes a permanent unclassed artefact in the
cycle folder — no document class, no header, no owner — non-compliant under the lifecycle guide.
No defined cleanup step exists after STEP 0.
Why it matters: A sealed cycle folder containing an unclassed file contaminates the historical
record. Drift detection may flag unknown files in sealed cycles on future reads.
Recommended change: Define a fixed temp filename: `.write_test` (hidden file, no class required).
Add a cleanup obligation to STEP 0: "Delete `.write_test` if it exists in the cycle folder before
proceeding. If deletion fails: halt — the environment is not safe to write to." This converts an
ambiguous "remove if possible" into a deterministic pre-STEP 0 cleanup gate.
Expected benefit: Cycle folders remain clean. Hidden file naming removes any class obligation.
Token impact: Neutral.
Effort: Low

---

**IMP-48 — `gh_issue_template.md` is referenced in shared_standards but ungoverned and unpreflight-checked**
Area: Governance | Prompt–Playbook Alignment
Problem: `shared_standards.md §6` states: "Use `claude/system/gh_issue_template.md` as the body
template" for GitHub issue creation, with a full variable mapping table. This file is not listed
in: the Artefact Register (§13 of the playbook), the Release Planning STEP -1.1 required files
check, or any engine's preflight. No document class, owner, or version is assigned.
If the file is missing: `--issues gh` silently produces malformed issue bodies or fails without
a clear error path.
Why it matters: A missing template causes silent failure of the most visible external output the
system produces (GitHub issues). The file has no governance record and could drift from the
shared_standards §6 variable mapping without detection.
Recommended change: (1) Add `claude/system/gh_issue_template.md` to the Artefact Register as
Class 6 (Governance Prompt), Owner: Head of Specs Team. (2) Add it to Release Planning STEP -1.1
required files check when `--issues gh` or `--issues import` is specified (conditional preflight).
(3) Add to `shared_standards.md §11` prompt version list so version drift is caught by STEP -1.7.
Expected benefit: Missing template causes a clean preflight halt. Template is versioned,
governed, and drift-detected.
Token impact: Neutral.
Effort: Low

---

**IMP-49 — Amendment STEP -1.4 requires `stage3_execution_plan.md` which no longer exists post-v2.11** ⚠️ BLOCKING
Area: Lifecycle | Prompt–Playbook Alignment | Failure Handling
Problem: `amendment_cycle_prompt.md` STEP -1.4 required files check includes:
`claude/cycles/<original_cycle_id>/stage3_execution_plan.md`. Since `release_planning_prompt.md`
v2.11, Stage 3 content is written as a section within the consolidated `release_plan.md` — the
separate `stage3_execution_plan.md` file is no longer produced. Any amendment invoked against a
cycle produced by release_planning_prompt v2.11+ will fail STEP -1.4 with "required file missing"
even though the cycle is valid and complete. The amendment changelog shows v1.0 was released
2026-03-07, the same day as release_planning_prompt v2.11 — this reference was already stale
at initial release of the amendment engine.
Why it matters: Every amendment cycle against any modern release plan will fail at preflight.
This is a hard gate failure that blocks all amendment capability for the system's entire working
history of cycles.
Recommended change: Update amendment STEP -1.4 required files:
- Remove: `claude/cycles/<original_cycle_id>/stage3_execution_plan.md`
- Add: `claude/cycles/<original_cycle_id>/release_plan.md`
- Add version detection: read `original_cycle state.json.prompt_schema_version`. If `v2`:
  require `release_plan.md`. If `v1` or absent: require `stage3_execution_plan.md`.
  This preserves backward compatibility with any pre-v2.11 cycle that may still be
  referenced by an amendment.
Similarly update the §4 amendment scope restriction ("may not change `stage3_execution_plan.md`")
to reference `release_plan.md ## Execution Plan` section for schema v2 cycles.
Expected benefit: Amendment cycles work against all modern release plans. Legacy cycles retained
via version detection.
Token impact: Neutral.
Effort: Low

---

**IMP-50 — Closure escalations have an irreconcilable class conflict**
Area: Governance | State
Problem: `shared_standards.md §4` lists `claude/cycles/<cycle_id>/closure_record.md §6` as a
file that receives escalation entries (append-only, Class 4 behaviour). `shared_standards.md §3`
defines `ESC-CLOSE-YYYYMMDD-nn` identifiers for Post-Ship Closure escalations. However,
`closure_record.md` is Class 3 (Operational Record) — the lifecycle guide defines Class 3 as
"immutable after filing." Escalation entries by definition require appending after the initial
filing (they are raised, then resolved). A document cannot be both immutable-after-filing and
append-only-for-escalations.
Why it matters: Post-Ship Closure that raises an escalation must either: (a) violate Class 3
immutability by appending to `closure_record.md`, or (b) have no compliant place to record
closure escalations. Either path is non-compliant. The conflict makes the current escalation
routing for Post-Ship Closure formally unenforceable.
Recommended change: Create `closure_escalations.md` (Class 4, append-only) as a distinct
Post-Ship Closure escalation file, consistent with every other phase. Update `shared_standards.md
§4` to replace `closure_record.md §6` with `claude/cycles/<cycle_id>/closure_escalations.md`.
Remove the §6 escalation section from the `closure_record.md` template. `closure_record.md`
documents the outcome; `closure_escalations.md` documents the process.
Expected benefit: Class 3 immutability is preserved. Closure escalations have a proper Class 4
home. Pattern is consistent with all phases.
Token impact: Neutral.
Effort: Low

---

**IMP-51 — Amendment backlog lock is held across human ratification wait with no release mechanism**
Area: State | Failure Handling
Problem: `amendment_cycle_prompt.md` STEP -1.1 acquires `claude/backlog/.lock` with marker
`AMEND-CHECK:<original_cycle_id>` and states: "Release this lock after STEP 5 completes or on
any halt path below. Do not hold the lock across human confirmation steps (STEP 3 ratification)."
This is a parenthetical instruction — there is no procedural lock release step between STEP -1
and STEP 3, and no mechanism by which the engine releases and re-acquires the lock around the
ratification gap. The instruction cannot be self-enforced: the engine pauses awaiting human
input, the lock file exists on disk, and there is no defined action that releases it mid-process
without abandoning the amendment.
Why it matters: Ratification may take hours or days. During this window, `claude/backlog/.lock`
is held with no timeout, blocking Release Planning (STEP 3.9), any Phase 1M engine that needs
the lock, and any future amendment attempt. Resolution requires manual lock deletion — a
governance violation under the no-auto-delete rule.
Recommended change: Add an explicit STEP 2.5 between STEP 2 (Proposed Changes) and STEP 3
(Ratification):

"**STEP 2.5 — Release Lock Before Ratification (Hard Requirement)**
Release `claude/backlog/.lock` before invoking STEP 3. Update `amendment_state.json`:
`backlog_lock_status = released_pending_ratification`. The lock will be re-acquired at
STEP 5.1 under the standard protocol with marker `AMD:<release>:<original_cycle_id>:<amendment_id>`.
Do not proceed to STEP 3 with the lock held."

Update §11 governance invariants: "`sprint_sealed` check is atomic — but the full backlog lock
is not held across human confirmation steps. Lock released at STEP 2.5, re-acquired at STEP 5.1."
Expected benefit: Backlog lock is not held during ratification. Eliminates the soft deadlock
risk for all other engines during the amendment ratification window.
Token impact: Neutral.
Effort: Low

---

---

### Open — Second direct prompt audit findings (2026-03-08)

*Findings from execution_prompt.md v1.6, post_ship_closure.md v1.4, sprint_planning_prompt.md v1.4.*

---

**IMP-52 — Sprint Planning reads `stage3_execution_plan.md` which no longer exists post-v2.11**
Area: Lifecycle | Prompt–Playbook Alignment | Failure Handling
Problem: `sprint_planning_prompt.md` §5 Source-of-Truth Planning Inputs lists
`claude/cycles/<cycle_id>/stage3_execution_plan.md` as a Required input. Since
`release_planning_prompt.md` v2.11, Stage 3 content is written as a section within the
consolidated `release_plan.md` — `stage3_execution_plan.md` is no longer produced. This is the
same class of defect as IMP-49 (amendment preflight). Sprint Planning STEP -1.5 would fail on
`stage3_execution_plan.md` with "required file missing" for every modern cycle.
Furthermore, STEP 0 reads "From `stage3_execution_plan.md`: sequencing dependencies, risk IDs
associated with EPICs, estimated effort per EPIC." This data now lives in `release_plan.md ##
Execution Plan` section.
Why it matters: Same as IMP-49 — this blocks Sprint Planning for all cycles produced after
v2.11. Sprint Planning and Amendment are both broken by the same v2.11 consolidation. This may
have been caught already (sprint_planning_prompt.md was updated to v1.4 on 2026-03-08, same as
today), but the §5 reference was not updated.
Recommended change: Update `sprint_planning_prompt.md` §5 and STEP 0:
- Remove `stage3_execution_plan.md` from required inputs
- Add `release_plan.md` as a required input (already implicitly needed for scope data)
- Add version detection: if `state.json.prompt_schema_version = "v2"`, read
  `release_plan.md ## Execution Plan` for sequencing, risk IDs, and effort estimates.
  If `v1` or absent, read `stage3_execution_plan.md`.
Update STEP -1.5 required files check to match.
Expected benefit: Sprint Planning works for all modern cycles. Legacy compatibility preserved.
Token impact: Neutral.
Effort: Low

---

**IMP-53 — Execution Engine write scope lists `lessons_learnt_execution.md` but IMP-28 retires it**
Area: Lifecycle | Cross-Document Consistency
Problem: `execution_prompt.md` §7 Write Scope Restriction permits creating
`claude/cycles/<cycle_id>/lessons_learnt_execution.md`. STEP 5.4 writes it via the
lessons_learnt_prompt. IMP-28 proposes retiring this file and replacing it with a phase-tagged
section in `lessons_learnt_cycle.md`. If IMP-28 is implemented, STEP 5.4 and §7 need updating.
Current gap: STEP 5.4 invokes `lessons_learnt_prompt.md §3.3` — this subsection reference is
specific to the current Sprint Execution inputs. If the lessons learnt prompt is restructured as
part of IMP-28, this reference will be stale.
Why it matters: IMP-28 implementation without corresponding updates to execution_prompt.md will
leave the engine writing a retired artefact to a retired path.
Recommended change: Flag as an IMP-28 dependency. When IMP-28 is implemented: update
`execution_prompt.md` STEP 5.4 to append to `lessons_learnt_cycle.md ## Phase 3` section
instead of creating a separate file. Update §7 write scope: remove `lessons_learnt_execution.md`,
add `lessons_learnt_cycle.md` (append-only, Phase 3 section only).
Token impact: Saves slightly — one file append vs one file create; no change to read operations.
Effort: Low
Dependency: IMP-28

---

**IMP-54 — Post-Ship Closure reads three lessons learnt files; IMP-28 consolidates to one**
Area: Token Efficiency | Cross-Document Consistency
Problem: `post_ship_closure.md` §4 lists three separate required lessons learnt inputs:
- `lessons_learnt.md` (Release Planning)
- `lessons_learnt_execution.md` (Sprint Execution)
- `lessons_learnt_verification.md` (Delivery Verification, "if produced")
STEP 8 reads all three explicitly. IMP-28 proposes replacing these three with one
`lessons_learnt_cycle.md` with phase-tagged sections. If IMP-28 is implemented, Post-Ship
Closure STEP 8 and §4 need updating.
Why it matters: This is the primary token saving from IMP-28 — the three-file read at Post-Ship
Closure is the highest-cost lessons learnt operation in the system. IMP-28 without Post-Ship
updates would produce the single file but still require reading the old three.
Recommended change: Flag as an IMP-28 dependency. When IMP-28 is implemented: update §4 to list
only `lessons_learnt_cycle.md` as required. Update STEP 8 to read the single structured file.
Remove the three per-phase entries from §4 and the write scope (must-not-modify list). The
consolidated file becomes the single source for STEP 8 review and STEP 8.5 closure record.
Token impact: Saves — three full file reads replaced by one structured file read.
Effort: Low
Dependency: IMP-28

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

**IMP-56 — Execution engine STEP -1.7 temp file has the same cleanup gap as IMP-47**
Area: Governance | Write Scope
Problem: `execution_prompt.md` STEP -1.7 (Write Permission Test) creates a temporary marker
file in `claude/cycles/<cycle_id>/` with the same "Remove it. If write fails: halt." instruction
as Release Planning STEP -1.4. The execution engine's write scope (§7) permits
`claude/cycles/<cycle_id>/execution_state.json` and similar — a stray temp file has the same
unclassed artefact risk as IMP-47. The sprint_planning_prompt.md STEP -1.8 has the same pattern.
All three prompts share the same temp file gap — IMP-47's fix (fixed name `.write_test`, cleanup
at STEP 0) should be applied uniformly.
Recommended change: Apply IMP-47's fix to `execution_prompt.md` STEP -1.7 and
`sprint_planning_prompt.md` STEP -1.8 simultaneously with the release_planning_prompt fix.
Use `.write_test` as the consistent temp filename across all engines.
Expected benefit: Consistent temp file handling across all three engines. No unclassed artefacts
in cycle folders.
Token impact: Neutral.
Effort: Low (apply IMP-47 fix uniformly across three prompts)

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

**IMP-58 — `prompt_change_log.md` is missing entries for `execution_prompt.md` v1.4 and v1.5**
Area: Governance | Cross-Document Version Consistency
Problem: `prompt_change_log.md` records `execution_prompt.md` v1.5→v1.6 (Lifecycle Guard added,
2026-03-07). There is no entry for v1.4→v1.5 or any prior version. `execution_prompt.md` v1.5
introduced substantial changes (the prompt's own changelog shows: pre-condition status check
corrected, sprint backlog sealed check added, `amended_backlog_slice_path` handling, `Executing`
status documented, STEP numbering adjusted). These changes are not recorded in
`prompt_change_log.md`. There is also no entry for any version before v1.5→v1.6. The
`delivery_verification_prompt.md` v1.0→v1.1 entry IS present (2026-03-07), so the gap is
specifically `execution_prompt.md` pre-v1.5 history.
Why it matters: `prompt_change_log.md` is the authoritative record of all governance prompt
changes per §11 of `shared_standards.md`. Missing entries mean IMP-10's version compliance
check will not detect drift if someone manually reverts `execution_prompt.md` to a pre-v1.5
state — the change log provides no baseline for comparison. The v1.5 changes were the most
significant correctness-affecting changes in the execution prompt's history.
Recommended change: Append the missing entries to `prompt_change_log.md` retroactively
(append-only file — add entries at the end with historical dates and a note "retroactively
recorded"):
- `execution_prompt.md` v1.4→v1.5: list the five major changes from the prompt's internal
  changelog (status check correction, sprint backlog sealed check, amended_backlog_slice_path,
  Executing status, STEP renumbering).
Add a standing rule to `shared_standards.md §11`: "Prompt change log entries must be created
simultaneously with prompt file updates, not retrospectively. A prompt version with no change
log entry is non-compliant until the entry is filed."
Expected benefit: Audit completeness for the most change-dense period of prompt evolution.
Change log becomes a reliable compliance baseline.
Token impact: Neutral.
Effort: Low

---

**IMP-59 — `completed_cycle_count` field does not exist in `.claude_current_state.json`; IMP-29 meta-review trigger has no data source**
Area: State | Lifecycle
Problem: IMP-29 (meta-review at Post-Ship Closure, triggered by `completed_cycle_count >= 3 AND
completed_cycle_count % 3 == 0`) requires a field `completed_cycle_count` in
`.claude_current_state.json`. The live state file has no such field — confirmed by reviewing
every field in the current JSON. The state file has `prior_cycle` (pointer to the previous
cycle ID) and `last_rebalance_cycle`, but no counter of completed cycles.
No engine currently sets or increments this counter. Post-Ship Closure STEP 10 updates
`status = Closed` and `post_ship_complete = true` but does not increment a cycle count.
Why it matters: IMP-29 cannot be implemented without this field. More broadly, the system has
no canonical record of how many cycles have been completed. Operations that depend on cycle
history (meta-review, trend analysis, backlog health scoring over time) all lack a foundation.
Recommended change: Add `completed_cycle_count` to the `post_ship_closure.md` STEP 10 global
state update — increment by 1 each time Post-Ship Closure completes successfully. Initial
value: if `prior_cycle` is absent, set to 1; if present but field has never existed, derive from
the `prior_cycle` chain depth or start at 1 with a note. Add the field to `.claude_current_state.json`
schema documentation in `shared_standards.md §10` or `lifecycle_schema.json` (if that file
exists — see IMP-61). This is a prerequisite for IMP-29 implementation.
Expected benefit: Provides the cycle counter required by IMP-29. Enables any future
cycle-count-dependent operations. Establishes a canonical lifecycle completion record.
Token impact: Neutral — one field increment at Post-Ship Closure STEP 10.
Effort: Low
Dependency: Required by IMP-29 before meta-review can be activated.

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

**IMP-61 — `lifecycle_schema.json` is referenced in `.claude_current_state.json` but not validated or documented**
Area: State | Governance
Problem: The live `.claude_current_state.json` contains:
```json
"lifecycle_schema": "claude/system/lifecycle_schema.json",
"schema_version": "1.0"
```
No reviewed prompt reads `lifecycle_schema.json`, validates against it, or references it. It is
not in any engine's required-files list or preflight check. `shared_standards.md §10` defines the
Lifecycle Guard with a valid-from-states table, but does not reference `lifecycle_schema.json` as
the source of truth for that table. If the file exists, it is orphaned from the governance stack.
If it does not exist, the reference is a dangling pointer — a state file field that points to a
non-existent document undermines the "no silent failures" guarantee.
Why it matters: A schema file that is never validated provides no protection against state drift.
A dangling pointer in the primary state file is a silent failure mode.
Recommended change: (1) Verify whether `claude/system/lifecycle_schema.json` exists. (2) If it
exists: add it to `shared_standards.md §10` as the machine-readable source for the Lifecycle
Guard valid-from-states table. Add a preflight read to `shared_standards.md §10` Lifecycle Guard:
"validate active_cycle status against lifecycle_schema.json valid_transitions before executing."
(3) If it does not exist: create a minimal schema defining the valid status values and
transitions, or remove the reference from `.claude_current_state.json` and document that the
Lifecycle Guard is defined in `shared_standards.md §10` prose.
Expected benefit: The lifecycle schema reference is either validated and enforced, or removed.
No dangling pointer in the primary state file.
Token impact: Neutral — schema validation is a one-read preflight check.
Effort: Low

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

## ✅ BATCH 0 — COMPLETE (2026-03-10)

**IMPs resolved:** IMP-49, IMP-51, IMP-52
**Files updated:** `amendment_cycle_prompt.md` → v1.3, `sprint_planning_prompt.md` → v1.5
**Verified by:** §14 governance table and §6B.8, §7 phase headers in playbook v3.5.

---

## ✅ BATCH 1 — COMPLETE (2026-03-10)

**IMPs resolved:** IMP-12, IMP-18, IMP-20, IMP-33 (gap 3), IMP-34, IMP-41, IMP-42, IMP-44, IMP-45, IMP-47, IMP-50, IMP-56, IMP-58, IMP-59, IMP-61
**Files updated:** `shared_standards.md` → v1.7, `execution_prompt.md` → v1.7, `sprint_planning_prompt.md` → v1.5, `release_planning_prompt.md` → v2.15, `post_ship_closure.md` → v1.5
**Verified by:** §14 governance table and §8 phase header in playbook v3.5.

> ⚠️ **VERSION ANOMALY — read before starting Batch 3:** `shared_standards.md` reached v1.7 rather than the planned v1.5. Two extra minor bumps indicate IMP-40 (SLA breach rule) and IMP-48 (gh_issue_template governance) — both planned for Batch 3 — were implemented in the same pass. **Before touching `shared_standards.md` in Batch 3: verify IMP-40 and IMP-48 are already present in v1.7.** If confirmed, remove those two items from Batch 3 scope. Batch 3's `shared_standards.md` entry becomes a no-op and the file is not re-touched.

---

## ✅ BATCH 2 — COMPLETE (2026-03-10)

**IMPs resolved:** IMP-13, IMP-17, IMP-33 (gap 2), IMP-36 (§6B, §7, §8 headers reconciled)
**File updated:** `operational_playbook.md` → v3.5
**Verified by:** direct audit of playbook v3.5.

---

## ✅ BATCH 2-PATCH — COMPLETE (2026-03-10)

**IMPs resolved:** IMP-62 (1), IMP-62 (2), IMP-62 (3)
**File updated:** `OPERATIONAL_GUIDE.md` → v3.6
**Verified by:** §9 source prompt → v1.2; §10 source prompt → v1.5 (filename corrected); §14 standing rule appended; prompt_change_log.md entry appended.

---

## BATCH 3 — Idempotency, GitHub, and state consistency fixes (medium complexity, high reliability value)

**Rationale:** These changes touch multiple prompts but are logically cohesive. All address the "resumability guarantee." Group them to avoid a second pass over the same files.

> ⚠️ **PRE-EMPTION CHECK REQUIRED before starting Batch 3:**
> - `shared_standards.md` is already at v1.7. IMP-40 and IMP-48 (the two Batch 3 shared_standards items) may already be implemented. **Read `shared_standards.md` v1.7 before touching it.** If IMP-40 (SLA breach rule in §4) and IMP-48 (gh_issue_template in §11 governed list) are present: skip the shared_standards section entirely — do not re-touch.
> - `release_planning_prompt.md` is already at v2.15. The Batch 3 release_planning changes (IMP-24, IMP-35 gap 4, IMP-48) were planned for v2.15 but Batch 1 already consumed that version number. These changes must go to **v2.16**. The Batch 4 release_planning change (IMP-26) then goes to **v2.17**. Update version targets accordingly.

### `release_planning_prompt.md` (→ v2.16, was planned as v2.15)
| IMP | Change |
|-----|--------|
| IMP-24 | STEP 4: add `stage4_issue_manifest.json` production alongside `stage4_backlog_slice.md`. Schema: `[{id, title, epic, description, ac_summary, labels, assignee}]`. §10.2 `sync gh`: update to consume `stage4_issue_manifest.json` instead of parsing markdown. |
| IMP-35 (gap 4) | §10.2 `sync gh`: add idempotency key — use GitHub issue label containing `cycle_id` as the check-before-create key. If label exists: update; do not create duplicate. |
| IMP-48 | STEP -1.1 required files: add conditional check — "if `--issues gh` or `--issues import` is specified: verify `claude/system/gh_issue_template.md` exists. If missing: halt with 'gh_issue_template.md not found — issue creation will fail.'" |

### `execution_prompt.md` (→ v1.8)
| IMP | Change |
|-----|--------|
| IMP-35 (gap 2) | STEP 5.4 lessons learnt append (when IMP-28 implemented): add pre-write check — "Before appending Phase 3 section to `lessons_learnt_cycle.md`, check for existing section header `## Phase 3 — <cycle_id>`. If present: skip append." Note: this guard activates with IMP-28; current prose record is unaffected. |
| IMP-40 | Add SLA tracking to escalation records in `execution_escalations.md`: maximum 72 hours before mandatory escalation to Product Owner regardless of type. At 72 hours: engine writes `BLOCKED_SLA_BREACH` notice and sets `.claude_current_state.json.blocked_sla_breached = true` on next invocation. Add `blocked_sla_breached` to STEP 6 global state write schema. |

### `amendment_cycle_prompt.md` (→ v1.4)
| IMP | Change |
|-----|--------|
| IMP-35 (gap 3) | Prompt change log append step (wherever action-now patches are applied): add pre-write check — "Before appending to `prompt_change_log.md`, check for existing entry with matching prompt name + version string. If present: skip." |
| IMP-39 | §10 Withdrawal procedure: add backlog rollback instruction — "If STEP 5 (backlog update) completed before withdrawal: the `backlog.md` amendment marker introduced at STEP 5 must be explicitly reversed. Append a reversal entry to `backlog.md` noting the withdrawn AMD-id, original state, and date. Update `amendment_state.json.backlog_rollback_required = true` and `backlog_rollback_completed = <date>` once done." |

### `shared_standards.md` (→ v1.8 if changes needed; skip entirely if IMP-40 + IMP-48 already present in v1.7)
| IMP | Change |
|-----|--------|
| IMP-40 | §4 Escalation format: add SLA breach rule — "Any escalation open for 72 hours without resolution triggers a mandatory `BLOCKED_SLA_BREACH` notice. Engine writes notice to active cycle escalations file and sets `blocked_sla_breached = true` in `.claude_current_state.json` on next invocation." **Skip if already present in v1.7.** |
| IMP-48 | §11 Prompt Version Control: add `claude/system/gh_issue_template.md` to the governed prompt list with Owner: Head of Specs Team, Class: 6. **Skip if already present in v1.7.** |

### `prompt_change_log.md` (→ append)
| IMP | Change |
|-----|--------|
| IMP-58 | Append retroactive entries for `execution_prompt.md` v1.4→v1.5 (status check corrected, sprint backlog sealed check added, amended_backlog_slice_path, Executing status documented, STEP renumbering). Mark with note: "Retroactively recorded 2026-03-09." **Skip if already present — check before appending (IMP-35 gap 3 idempotency rule applies here too).** |

---

## BATCH 4 — Token efficiency (highest token savings, medium effort, no cross-dependencies within batch)

**Rationale:** These changes are independent of each other and independent of Batches 0–3. Ordered by token saving magnitude. IMP-25 is a prerequisite for IMP-23 (if sprint_backlog becomes a reference-only document, the index is the bridge). Do IMP-25 → IMP-24 companion → IMP-23 → IMP-26 → IMP-27.

### `release_planning_prompt.md` (→ v2.16)
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

## BATCH 5 — Lessons learnt consolidation (high impact, medium effort, must precede IMP-29 and IMP-37)

**Rationale:** IMP-28 is the prerequisite for three other IMPs (IMP-29, IMP-37, IMP-53, IMP-54). It requires coordinated changes across four prompt files. Do it as a single atomic batch.

### `lessons_learnt_prompt.md` (→ v_next)
| IMP | Change |
|-----|--------|
| IMP-28 | Restructure as append-only phase-tagging prompt. Each phase section call appends a structured table block to `lessons_learnt_cycle.md` for the active cycle. Table schema: `friction_item | phase | type (A–E) | classification | action | owner | target_date`. Retire §3.3 (Sprint Execution standalone) and §3.4 (Delivery Verification standalone) section references. Retain §3.5 (Post-Ship Closure consolidation) as the meta-consumer of the structured file. Add §3.6 (Amendment): phase tag `## Amendment — <AMD-id>`. |
| IMP-35 (gap 2) | Idempotency guard now built into the prompt's append logic (pre-write section header check). Replaces the guard added in Batch 3 execution_prompt change if IMP-28 is implemented before Batch 3 is applied. |

### `execution_prompt.md` (→ v_next after IMP-28)
| IMP | Change |
|-----|--------|
| IMP-53 | STEP 5.4: change from "invoke lessons_learnt_prompt.md §3.3 → lessons_learnt_execution.md" to "append Phase 3 section to `lessons_learnt_cycle.md` via lessons_learnt_prompt.md §3." §7 Write Scope: remove `lessons_learnt_execution.md`, add `lessons_learnt_cycle.md` (append-only, Phase 3 section). |

### `delivery_verification_prompt.md` (→ v_next after IMP-28)
| IMP | Change |
|-----|--------|
| IMP-54 | Lessons learnt step (wherever it exists): change to append Phase 4 section to `lessons_learnt_cycle.md`. |

### `post_ship_closure.md` (→ v_next after IMP-28)
| IMP | Change |
|-----|--------|
| IMP-54 | §4 required inputs: replace three per-phase lessons learnt files with single `lessons_learnt_cycle.md`. STEP 8: read single structured file instead of three separate documents. §5 must-not-modify: update accordingly. |

### `amendment_cycle_prompt.md` (→ v_next after IMP-28)
| IMP | Change |
|-----|--------|
| IMP-37 | STEP 8: after producing `amendment_lessons.md` (retained for backward compat), also append `## Amendment — <AMD-id>` section to `lessons_learnt_cycle.md` using the IMP-28 table schema. |

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

## BATCH 7 — Governance decisions required (cannot proceed without named-authority decision)

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

## BATCH 8 — Remaining governance and lifecycle completeness (no blocking dependencies)

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
| 0 | ✅ COMPLETE | `amendment_cycle_prompt.md` v1.3, `sprint_planning_prompt.md` v1.5 | 49, 51, 52 | Hard blockers |
| 1 | ✅ COMPLETE | `shared_standards.md` v1.7, `execution_prompt.md` v1.7, `sprint_planning_prompt.md` v1.5, `release_planning_prompt.md` v2.15, `post_ship_closure.md` v1.5 | 12, 18, 20, 33(gap3), 34, 40†, 41, 42, 44, 45, 47, 48†, 50, 56, 58, 59, 61 | Correctness + state hygiene |
| 2 | ✅ COMPLETE | `operational_playbook.md` v3.5 | 13, 17, 33(gap2), 36(partial) | Playbook hygiene |
| 2-PATCH | **NEXT** | `operational_playbook.md` v3.6 | 62 | IMP-36 residuals |
| 3 | — | `release_planning_prompt.md` v2.16, `execution_prompt.md` v1.8, `amendment_cycle_prompt.md` v1.4, `shared_standards.md` v1.8 (if needed), `prompt_change_log.md` | 24, 35(gaps 2–4), 39, 40†(verify), 48†(verify), 58(verify) | Idempotency + GitHub reliability |
| 4 | — | `release_planning_prompt.md` v2.17, `sprint_planning_prompt.md` v1.7, `execution_prompt.md` v1.9, `post_ship_closure.md` v1.6 | 23, 25, 26, 27 | Token savings — highest volume reduction |
| 5 | — | `lessons_learnt_prompt.md`, `execution_prompt.md`, `delivery_verification_prompt.md`, `post_ship_closure.md`, `amendment_cycle_prompt.md` | 28, 37, 53, 54 | Structural — lessons learnt consolidation; prerequisite for Batch 6 |
| 6 | — | `post_ship_closure.md`, `shared_standards.md` | 29, 32 | Meta-review; gated on one full Batch 5 cycle |
| 7 | — | `team_charter.md` + various (post-decision) | 17, 30, 31, 60 | Decision-gated; human input required |
| 8 | — | `shared_standards.md`, `release_planning_prompt.md`, `delivery_verification_prompt.md`, `post_ship_closure.md`, `roadmap_prompt.md` | 11, 13, 14, 15, 16, 22, 43 | Completeness sweep |

† IMP-40 and IMP-48 may already be present in `shared_standards.md` v1.7. Verify before re-applying in Batch 3.

**Open IMPs remaining: 46** (including IMP-62)
**IMPs requiring human decision before implementation: 4 (Batch 7)**
**Batches 2-PATCH through 4 can proceed immediately with no decision gates.**

