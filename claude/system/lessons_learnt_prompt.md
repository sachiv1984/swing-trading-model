**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.3
**Last Updated:** 2026-03-04

---

# Lessons Learnt Governance Prompt (Internal, Reusable)

## Invocation Rule

This prompt is **NOT user-invoked.**

It may only be invoked internally by a governed routine step (e.g., "STEP 11 — Lessons Learnt", "STEP 8 — Lessons Learnt", "STEP 5.4 — Lessons Learnt").

If a user attempts to run this directly, refuse and instruct them to run the appropriate routine (e.g., `run roadmap`, `run sprint`, `run delivery verification`, `run post-ship`).

---

## 1. Purpose

Generate a structured, filed lessons learnt record that:
- Captures what improved or degraded process integrity
- Classifies each friction item by type so patterns are visible across cycles
- Requires a blast radius analysis for every friction item (what breaks if this goes uncaught?)
- Produces concrete, file-specific process patches — not commentary
- Detects recurrence against the prior cycle's lessons learnt

This is governance learning, not a retrospective. Value is measured by the patches actioned, not the observations recorded.

---

## 2. Authorities

Primary authority: PMO Lead (process improvement ownership)

Enforcement authority:
- Head of Specs Team enforces lifecycle compliance for any modified governed document
- Facilitator ensures the step is executed and recorded
- Challenger may demand clarity on ambiguity but does not propose changes

Non-decision roles have no "voice" on outcomes.

---

## 3. Inputs (Read Only)

Read the inputs appropriate to the invoking routine:

### 3.1 Roadmap Rebalance inputs

- `claude/cycles/<cycle_id>/run_manifest.md`
- `claude/cycles/<cycle_id>/stage1_validation.md`
- `claude/cycles/<cycle_id>/stage2_backlog_health.md`
- `claude/cycles/<cycle_id>/stage3_ideas.md`
- `claude/cycles/<cycle_id>/stage4_debate.md`
- `claude/cycles/<cycle_id>/stage5_rebalance.md`
- `claude/cycles/<cycle_id>/cycle_summary.md`

### 3.2 Release Planning inputs

- `claude/cycles/<cycle_id>/run_manifest.md`
- `claude/cycles/<cycle_id>/stage1_readiness.md`
- `claude/cycles/<cycle_id>/stage2_scope_extraction.md`
- `claude/cycles/<cycle_id>/stage3_execution_plan.md`
- `claude/cycles/<cycle_id>/stage3_5_model_integrity.md`
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md`
- `claude/cycles/<cycle_id>/stage4_5_capacity_check.md`
- `claude/cycles/<cycle_id>/stage5_5_cross_stage_integrity.md`
- `claude/cycles/<cycle_id>/escalations.md` (if present)
- `claude/cycles/<cycle_id>/cycle_summary.md`

### 3.3 Sprint Execution inputs

- `claude/cycles/<cycle_id>/sprint_goal.md`
- `claude/cycles/<cycle_id>/sprint_backlog.md`
- `claude/cycles/<cycle_id>/execution_state.json`
- `claude/cycles/<cycle_id>/delegation_log.md`
- `claude/cycles/<cycle_id>/execution_escalations.md` (if present)
- `claude/cycles/<cycle_id>/sprint_close.md`

### 3.4 Delivery Verification inputs

- `claude/cycles/<cycle_id>/verification_report.md`
- `claude/cycles/<cycle_id>/sprint_close.md`
- `claude/cycles/<cycle_id>/execution_state.json`
- `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` (one per merged EPIC)
- `claude/cycles/<cycle_id>/verification_escalations.md` (if present)

Focus areas: gate sequencing friction (was QA evidence ready when needed?), deviation severity assessment patterns (were P0/P1/P2 calls contested?), test scenario coverage gaps (recurring or systemic?), sign-off coordination friction between Director of Quality and Product Owner.

### 3.5 Post-Ship Closure inputs

- `claude/cycles/<cycle_id>/closure_record.md`
- `claude/cycles/<cycle_id>/lessons_learnt.md` (Release Planning — read for cross-cycle pattern detection)
- `claude/cycles/<cycle_id>/lessons_learnt_execution.md` (Sprint Execution — read for cross-cycle pattern detection)
- `docs/product/changelog.md` (confirm entry quality)
- `docs/specs/Specs_Index.md` (confirm open items were reconciled)

Focus areas: document closure friction (which documents were hardest to locate or update?), lessons learnt action application rate (how many immediate actions were actually applied vs deferred?), whether any closure steps revealed gaps that should have been caught earlier.

### 3.6 Cross-Cycle Recurrence Check (All routines — Mandatory)

Before writing the output record, load the previous cycle's lessons learnt file for the same routine type:

| Invoking routine | Prior cycle file to load |
|-----------------|--------------------------|
| Roadmap Rebalance | `claude/cycles/<prior_cycle_id>/lessons_learnt.md` |
| Release Planning | `claude/cycles/<prior_cycle_id>/lessons_learnt.md` |
| Sprint Execution | `claude/cycles/<prior_cycle_id>/lessons_learnt_execution.md` |
| Delivery Verification | `claude/cycles/<prior_cycle_id>/lessons_learnt_verification.md` |
| Post-Ship Closure | `claude/cycles/<prior_cycle_id>/lessons_learnt_closure.md` |

If the prior cycle file does not exist: record "No prior cycle file found — recurrence check not possible" and continue.

For each friction item identified in this run: check whether the same or substantially similar item appeared in the prior cycle's lessons learnt. If it did, mark it as a **Recurrence** (see §5 record structure). A friction item that recurs with an open outstanding action from the prior cycle is an automatic escalation trigger — do not record it as a new outstanding action. Escalate immediately to Head of Specs Team (§6.4).

If some files are missing:
- Record the absence as a process failure
- Do not invent content

---

## 4. Output (Filed Record)

### 4.1 Output path

The output path depends on the invoking routine:

| Invoked by | Output file |
|-----------|-------------|
| Roadmap Rebalance (STEP 11) | `claude/cycles/<cycle_id>/lessons_learnt.md` |
| Release Planning (STEP 8) | `claude/cycles/<cycle_id>/lessons_learnt.md` |
| Sprint Execution (STEP 5.4) | `claude/cycles/<cycle_id>/lessons_learnt_execution.md` |
| Delivery Verification | `claude/cycles/<cycle_id>/lessons_learnt_verification.md` |
| Post-Ship Closure | `claude/cycles/<cycle_id>/lessons_learnt_closure.md` |

The execution, verification, and closure routines use distinct filenames because multiple routines share the same `cycle_id` folder and their lessons learnt records must remain separate and traceable to their source routine.

### 4.2 Header block

```
Owner: Infrastructure & Operations Documentation Owner
Status: Operational Record
Deployment Version: N/A
Report Date: <today>
Environment: Governance
Generated By: PMO Lead
Filed: <today>
```

---

## 5. Record Structure (Must Use)

The lessons learnt record MUST follow this structure exactly. Do not omit sections, do not merge sections, do not add free-form commentary outside the defined fields.

---

```
# Lessons Learnt — <Routine Name>

Feature / Trigger: <feature name or sprint goal if present, else "N/A">
Run: <cycle_id>
Reviewed by: PMO Lead
Date filed: <today>
Prior cycle checked: <prior_cycle_id | "None — first cycle" | "File not found">

---

## What worked well
[2–4 bullets. Specific — name the step, the artefact, or the role interaction that worked.]

---

## Friction Log

[One entry per friction item identified. Use the full template below for each.]

---

### Friction Item <n>

**Classification:**
[Select exactly one:]
- Type A — Governance Drift: A documented rule or header requirement was ignored or missed
- Type B — Semantic Mismatch: The same concept was named or interpreted differently across documents or roles
- Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced
- Type D — Cognitive Fatigue: A detail was missed due to prompt length, context overload, or accumulated complexity
- Type E — Authority Gap: A decision was needed and no role was clearly empowered to make it

**Recurrence:** Yes — appeared in <prior_cycle_id> | No | Not checkable (no prior file)

**What happened:**
[One paragraph. Factual. Name the step, the artefact, the role. No editorialising.]

**Where in the routine:**
[Step/stage reference, e.g., "STEP 4.1 — Classification" or "Stage 3 — Execution Plan"]

**Root cause:**
[Select one or more: process gap / template omission / missing artefact / authority ambiguity / naming inconsistency / context window pressure / delegation classification error / severity classification error / document staleness]

**Blast radius analysis:**
- What would have propagated: [which document, rule, or phase would have been affected]
- When it would have surfaced: [next gate / next sprint / next cycle / never — silent failure]
- Recovery cost if uncaught: [low (single file fix) / medium (cycle rework) / high (release impact) / critical (shipped incorrect behaviour)]

**Process patch:**
[Select one:]

→ Immediate patch applied this run:
  - File: <exact file path>
  - Section: <§ reference>
  - Change: <one sentence — specific enough that a different agent could apply it independently>
  - Version: <old version → new version>

→ Deferred patch (cannot apply this run):
  - File: <exact file path>
  - Section: <§ reference or "New section required">
  - Change required: <one sentence — specific enough to action without further clarification>
  - Owner: <role>
  - Target: <next run of this routine | specific cycle_id | date>

[A patch entry of "we should improve X" with no file and section named is not valid. If no specific file can be identified, this item must be escalated to Head of Specs Team — record it under Escalations, not here.]

---

[Repeat for each friction item]

---

## Recurrence Escalations

[List any friction items marked Recurrence = Yes where the prior cycle's outstanding action was not resolved. These are automatic escalations — do not re-record as new outstanding actions.]

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| <description> | <cycle_id> | <action from prior record> | Head of Specs Team |

If none: "None."

---

## Process improvements actioned this run

[Summary table of all immediate patches applied.]

| File | Section | Change | Version |
|------|---------|--------|---------|
| <path> | <§ ref> | <change> | <old → new> |

If none: "None applied this run."

---

## New files created this run

[List any new files created as part of improvements, with rationale.]
If none: "None."

---

## Outstanding deferred patches

[One row per deferred patch.]

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| <path> | <§ ref> | <change> | <role> | <target> |

If none: "None."

---

## Escalations

[Any items requiring Head of Specs Team or Product Owner resolution: governance gaps, authority boundary ambiguity, recurring conflicts, deferred patches with no identifiable file, recurrence escalations.]

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| <description> | Governance gap / Authority ambiguity / Recurrence | Head of Specs Team / Product Owner | <one sentence> |

If none: "None."
```

---

## 6. Action Rules (Non-Negotiable)

**6.1 Do not re-litigate decisions**
Do not argue whether roadmap outcomes, sprint scope selections, delegation decisions, deviation severity calls, or closure document updates were "right". Focus only on process quality and governance integrity.

**6.2 Every friction item requires a process patch**
Every friction item must have a process patch entry. There are only two valid states:
- **Immediate patch:** applied this run with file, section, change, and version recorded
- **Deferred patch:** specific file and section named, owner assigned, target date set

"We should improve X" with no file and section is not a valid deferred patch. It is an escalation to the Head of Specs Team. Record it under Escalations.

**6.3 Apply immediate patches now**
If a friction point can be resolved by updating a template or governance prompt during this run: apply the change immediately. Lifecycle compliance is required:
- correct owner
- correct status
- version increment when meaning changes
- Last Updated date updated

Record the change in the "Process improvements actioned" table.

**6.4 Escalate what is outside PMO remit**
Escalate to Head of Specs Team and/or Product Owner when:
- No specific file or section can be identified for a patch
- The issue is a governance gap or authority boundary ambiguity
- A recurring conflict between domain owners is unresolved
- A friction item is marked Recurrence = Yes with an open prior outstanding action
- A delegation classification fails repeatedly (execution routine)
- A deviation severity call is consistently contested (verification routine)
- A closure document is consistently missing or stale at post-ship (closure routine)

**6.5 Blast radius is mandatory**
Every friction item must have all three blast radius fields completed. "Unknown" is not valid for recovery cost. If the propagation path is genuinely unclear, that itself is a Type E — Authority Gap or Type C — Dependency Stall and should be named as the friction item's root cause.

**6.6 Friction classification is mandatory and singular**
Every friction item must have exactly one classification (Type A–E). If a friction item could be classified as more than one type, classify by the root cause — not the symptom. Example: a missing header that caused a pipeline failure is Type A (Governance Drift) at root, not Type C (Dependency Stall), even though it caused a stall.

---

## 7. Lifecycle Compliance Gate

Before writing the lessons learnt file and before modifying any template or prompt:
- Verify lifecycle compliance per `claude/charter/document_lifecycle_guide.md`
- If compliance cannot be satisfied, halt and report the blocker

---

## 8. Completion Condition

This prompt completes only when:
- The output file exists at the correct path for the invoking routine (§4.1)
- It follows the required structure (§5) with no omitted sections
- Every friction item has a classification, blast radius, and process patch
- Recurrence check is recorded (even if prior file not found)
- Recurrence escalations table is present (even if empty)
- Any immediate patches are reflected in updated files with correct lifecycle versioning
- All deferred patches name a specific file, section, owner, and target
- Escalations table is present (even if empty)

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.3 | 2026-03-04 | Added §3.6 Cross-Cycle Recurrence Check (mandatory for all routines). Added Friction Classification system (Type A–E) as required field on every friction item. Added Blast Radius Analysis as required field on every friction item (what propagates / when surfaces / recovery cost). Added Process Patch requirement (immediate or deferred — both require specific file + section; vague patches become escalations). Added Type E — Authority Gap to classification taxonomy. Rewrote §5 record structure with full templated friction item format. Added Recurrence Escalations section to record structure. Added Outstanding Deferred Patches table to record structure. Rewrote §6 action rules to enforce patch specificity and blast radius. Updated completion condition (§8) to reflect all new required fields. |
| 1.2 | 2026-03-03 | Added §3.4 (Delivery Verification inputs) and §3.5 (Post-Ship Closure inputs) with focus areas for each. Added output path entries for Delivery Verification and Post-Ship Closure to §4.1. Updated §4.1 note to cover all three distinct-filename routines. Added verification and closure escalation triggers to §6.4. Updated invocation rule examples. Fixed header formatting. Moved Change Log to end. |
| 1.1 | 2026-03-02 | Added §3.3 (Execution routine inputs) and §4.1 (Output path override) to support invocation from Sprint Execution Engine. |
| 1.0 | 2026-03-02 | Initial version. Roadmap Rebalance and Release Planning routines. |