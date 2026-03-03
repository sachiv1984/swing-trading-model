**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-03-03

---

# Lessons Learnt Governance Prompt (Internal, Reusable)

## Invocation Rule

This prompt is **NOT user-invoked.**

It may only be invoked internally by a governed routine step (e.g., "STEP 11 — Lessons Learnt", "STEP 8 — Lessons Learnt", "STEP 5.4 — Lessons Learnt").

If a user attempts to run this directly, refuse and instruct them to run the appropriate routine (e.g., `run roadmap`, `run sprint`, `run delivery verification`, `run post-ship`).

---

## 1. Purpose

Generate a short, filed lessons learnt record that:
- Captures what improved or degraded process integrity
- Produces concrete actions on templates/prompts where possible
- Avoids re-litigating decisions

This is governance learning, not a retrospective.

Value is measured by the changes actioned, not the commentary produced.

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

Focus areas for Delivery Verification lessons: gate sequencing friction (was QA evidence ready when needed?), deviation severity assessment patterns (were P0/P1/P2 calls contested?), test scenario coverage gaps (recurring or systemic?), and sign-off coordination friction between Director of Quality and Product Owner.

### 3.5 Post-Ship Closure inputs

- `claude/cycles/<cycle_id>/closure_record.md`
- `claude/cycles/<cycle_id>/lessons_learnt.md` (Release Planning — read for cross-cycle pattern detection)
- `claude/cycles/<cycle_id>/lessons_learnt_execution.md` (Sprint Execution — read for cross-cycle pattern detection)
- `docs/product/changelog.md` (confirm entry quality)
- `docs/specs/Specs_Index.md` (confirm open items were reconciled)

Focus areas for Post-Ship Closure lessons: document closure friction (which documents were hardest to locate or update?), lessons learnt action application rate (how many immediate actions were actually applied vs deferred?), and whether any closure steps revealed gaps that should have been caught earlier in the cycle.

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

Use the following header block at the top of the record:

```
Owner: Infrastructure & Operations Documentation Owner
Status: Operational Record
Deployment Version: N/A
Report Date: <today>
Environment: Governance
Generated By: PMO Lead
Filed: <today>
```

Note:
- "Owner" is the filing owner per lifecycle rules for Operational Records.
- "Generated By" identifies the accountable process role.

---

## 5. Record Structure (Must Use)

The lessons learnt record MUST follow this structure:

```
# Lessons Learnt — <Routine Name>

Feature / Trigger:
- <feature name or sprint goal if present, else "N/A">

Run:
- <cycle_id>

Reviewed by:
- PMO Lead

Date filed:
- <today>

## What worked well
- 2–4 bullets only

## What created friction
For each item include:
- What happened
- Where in the routine (step/stage)
- Root cause (process, template, missing artefact, authority ambiguity, delegation gap)
- Impact (delay, rework, quality risk, decision ambiguity, blocked item)

## Process improvements actioned (this run)
For each item include:
- What changed
- Which file was updated
- Version change applied (if applicable)
- Why it resolves the friction

## New skills or templates created (this run)
- List new files created (if any) and why

## Outstanding actions
For each item include:
- Action
- Owner role
- Target date or target run

## Escalations
List any escalations raised to:
- Product Owner
- Head of Specs Team
Include the reason (governance gap, boundary ambiguity, systemic conflict).
```

---

## 6. Action Rules (Non-Negotiable)

**6.1 Do not re-litigate decisions**
Do not argue whether roadmap outcomes, sprint scope selections, delegation decisions, deviation severity calls, or closure document updates were "right".
Focus only on process quality and governance integrity.

**6.2 Action improvements immediately when safe**
If a friction point can be resolved by updating a template or governance prompt during this run:
- Apply the change immediately
- Ensure lifecycle compliance:
  - correct owner
  - correct status
  - version increment when meaning changes
  - Last Updated date updated
- Record the change under "Process improvements actioned"

**6.3 Do not create fake structure**
Do not create empty templates "for later".
If a needed template does not exist, record it as an outstanding action unless explicitly instructed to create it.

**6.4 Escalate what is outside PMO remit**
If the issue is:
- a governance gap
- an authority boundary ambiguity
- a recurring conflict between domain owners
- a delegation classification that repeatedly fails (execution routine only)
- a deviation severity pattern that is consistently contested (verification routine only)
- a closure document that is consistently missing or stale at post-ship (closure routine only)

Then escalate to Product Owner and Head of Specs Team and record it.

---

## 7. Lifecycle Compliance Gate

Before writing the lessons learnt file and before modifying any template or prompt:
- Verify lifecycle compliance per `claude/charter/document_lifecycle_guide.md`
- If compliance cannot be satisfied, halt and report the blocker

---

## 8. Completion Condition

This prompt completes only when:
- The output file exists at the correct path for the invoking routine (§4.1)
- It follows the required structure (§5)
- Any actioned improvements are reflected in updated files with correct lifecycle versioning
- Any outstanding actions and escalations are explicitly listed

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.2 | 2026-03-03 | Added §3.4 (Delivery Verification inputs) and §3.5 (Post-Ship Closure inputs) with focus areas for each. Added output path entries for Delivery Verification (`lessons_learnt_verification.md`) and Post-Ship Closure (`lessons_learnt_closure.md`) to §4.1. Updated §4.1 note to cover all three distinct-filename routines. Added verification and closure escalation triggers to §6.4. Updated invocation rule examples to include `run delivery verification` and `run post-ship`. Fixed header to use bold formatting consistent with other governance prompts. Moved Change Log to end of document. |
| 1.1 | 2026-03-02 | Added §3.3 (Execution routine inputs) and §4.1 (Output path override) to support invocation from Sprint Execution Engine. No changes to structure, action rules, or lifecycle requirements. |
| 1.0 | 2026-03-02 | Initial version. Roadmap Rebalance and Release Planning routines. |