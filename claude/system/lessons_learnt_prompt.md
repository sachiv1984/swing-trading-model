**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.11
**Last Updated:** 2026-08-12 (§3.7 gains a patch-ID matching requirement, LL-v8.6-P4-01b — closes a false-positive recurrence-claim gap)

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
- Classifies every patch as action-now or defer, with Head of Specs Team sign-off required for action-now
- Records every applied patch in the prompt change log so every prompt version is traceable to its triggering friction
- Detects recurrence against the prior cycle's lessons learnt

This is governance learning, not a retrospective. Value is measured by the patches actioned and logged, not the observations recorded.

---

## 1.1 Required Invocation Context (Hard Gate)

This prompt must be invoked with a structured context block. If context is absent: halt and output: "LESSONS LEARNT INVOCATION ERROR — missing context. Invoking engine must supply structured block."

Required context fields:
```
invoking_routine: <engine name — e.g. "roadmap_prompt.md">
cycle_id: <active cycle_id>
phase: <Phase 3 | Phase 4 | Post-Ship | Amendment | Roadmap | Release>
prior_cycle_id: <prior cycle_id or "none — first cycle">
```

If any field is absent: output error listing missing fields. Do not proceed. Calling engines must pass all four fields explicitly at invocation.

---

## 2. Authorities

Primary authority: PMO Lead (process improvement ownership)

Enforcement authority:
- Head of Specs Team enforces lifecycle compliance for any modified governed document, and must explicitly confirm every action-now prompt patch before it is applied
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

- `claude/cycles/<cycle_id>/release_plan.md` (consolidated intermediate — contains readiness, scope extraction, execution plan, model integrity, and capacity check sections; replaces pre-v2.11 stage files)
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md`
- `claude/cycles/<cycle_id>/escalations.md` (if present)
- `claude/cycles/<cycle_id>/cycle_summary.md`
- `claude/cycles/<cycle_id>/run_manifest.md` (if present)

### 3.3 Sprint Execution — Phase 3 Append (IMP-28)

**Output target:** Append to `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (Phase 3 section). The standalone `lessons_learnt_execution.md` file is retired.

**Idempotency guard:** Before appending, check for a `## Phase 3` section with `**Cycle:** <cycle_id>` field in `lessons_learnt_cycle.md`. If present: skip append (already complete for this cycle).

**Inputs to read:**
- `claude/cycles/<cycle_id>/sprint_goal.md`
- `claude/cycles/<cycle_id>/sprint_backlog.md`
- `claude/cycles/<cycle_id>/execution_state.json`
- `claude/cycles/<cycle_id>/delegation_log.md`
- `claude/cycles/<cycle_id>/execution_escalations.md` (if present)
- `claude/cycles/<cycle_id>/sprint_close.md`

**Phase 3 focus areas:**
- Delegation patterns (which classification kept needing humans — could any become autonomous?)
- GitHub integration friction (CI behaviour, issue/PR lifecycle)
- Acceptance criteria gaps (items that lacked criteria and had to be parked as `delegated_decision`)
- Governance process friction (gates that fired unexpectedly, SLA misses)

**Output format:** Append a Phase 3 section to `lessons_learnt_cycle.md` using the structured table block format (§4.2). Use stable header `## Phase 3` with `**Cycle:** <cycle_id>` as a metadata field (not in the header).

### 3.4 Delivery Verification — Phase 4 Append (IMP-28)

**Output target:** Append to `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (Phase 4 section). The standalone `lessons_learnt_verification.md` file is retired.

**Idempotency guard:** Before appending, check for a `## Phase 4` section with `**Cycle:** <cycle_id>` field in `lessons_learnt_cycle.md`. If present: skip append (already complete for this cycle).

**Inputs to read:**
- `claude/cycles/<cycle_id>/verification_report.md`
- `claude/cycles/<cycle_id>/sprint_close.md`
- `claude/cycles/<cycle_id>/execution_state.json`
- `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` (one per merged EPIC)
- `claude/cycles/<cycle_id>/verification_escalations.md` (if present)

**Phase 4 focus areas:** gate sequencing friction (was QA evidence ready when needed?), deviation severity assessment patterns (were P0/P1/P2 calls contested?), test scenario coverage gaps (recurring or systemic?), sign-off coordination friction between Director of Quality and Product Owner.

**Output format:** Append a Phase 4 section to `lessons_learnt_cycle.md` using the structured table block format (§4.2). Use stable header `## Phase 4` with `**Cycle:** <cycle_id>` as a metadata field (not in the header).

### 3.5 Post-Ship Closure inputs

- `claude/cycles/<cycle_id>/closure_record.md`
- `claude/cycles/<cycle_id>/lessons_learnt.md` (Release Planning — read for cross-cycle pattern detection)
- `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (Phase 3 Sprint Execution + Phase 4 Delivery Verification + any Amendments — single structured file replacing per-phase standalone files; read for cross-cycle pattern detection)
- `docs/product/changelog.md` (confirm entry quality)
- `docs/specs/Specs_Index.md` (confirm open items were reconciled)

Focus areas: document closure friction (which documents were hardest to locate or update?), lessons learnt action application rate (how many immediate actions were actually applied vs deferred?), whether any closure steps revealed gaps that should have been caught earlier.

**Output requirement (ST-15):** The `lessons_learnt_closure.md` produced by this section must include a `## Carry-Forward` section per `shared_standards.md §16.8`. Zero rows is valid; absence of the section is not.

### 3.6 Amendment — Amendment Section Append (IMP-37)

**Output target:** Append to `claude/cycles/<original_cycle_id>/lessons_learnt_cycle.md` (Amendment section). The standalone `amendment_lessons.md` in the amendment sub-folder is retained for backward compatibility.

**Idempotency guard:** Before appending, check for existing section header `## Amendment — <AMD-id>` in `lessons_learnt_cycle.md`. If present: skip append (already complete for this amendment).

**Inputs to read:** amendment manifest and ratification record from `claude/cycles/<original_cycle_id>/amendments/<amendment_id>/`.

**Amendment focus areas:**
- What caused the emergency that forced the amendment
- Whether the amendment process was proportionate and efficient
- Any process improvements for earlier detection of hard blockers or emergencies
- Any improvements to the release planning engine's readiness checks that could catch this class of issue earlier

**Output format:** Append an Amendment section to `lessons_learnt_cycle.md` using the structured table block format (§4.2). Use phase tag `## Amendment — <AMD-id>`.

---

### 3.7 Cross-Cycle Recurrence Check (All routines — Mandatory)

Before writing the output record, load the previous cycle's lessons learnt file for the same routine type:

| Invoking routine | Prior cycle file to load |
|-----------------|--------------------------|
| Roadmap Rebalance | `claude/cycles/<prior_cycle_id>/lessons_learnt.md` |
| Release Planning | `claude/cycles/<prior_cycle_id>/lessons_learnt.md` |
| Sprint Execution | `claude/cycles/<prior_cycle_id>/lessons_learnt_cycle.md` (`## Phase 3` section where `**Cycle:** <prior_cycle_id>`) |
| Delivery Verification | `claude/cycles/<prior_cycle_id>/lessons_learnt_cycle.md` (`## Phase 4` section where `**Cycle:** <prior_cycle_id>`) |
| Amendment | `claude/cycles/<prior_cycle_id>/lessons_learnt_cycle.md` (`## Amendment — <AMD-id>` section(s), if amendments occurred in prior cycle) |
| Post-Ship Closure | `claude/cycles/<prior_cycle_id>/lessons_learnt_closure.md` |

If the prior cycle file does not exist: record "No prior cycle file found — recurrence check not possible" and continue.

For each friction item identified in this run: check whether the same or substantially similar item appeared in the prior cycle's lessons learnt. If it did, mark it as a **Recurrence** (see §5 record structure). A friction item that recurs with an open outstanding action from the prior cycle is an automatic escalation trigger — do not record it as a new outstanding action. Escalate immediately to Head of Specs Team (§6.4).

Also load `claude/system/prompt_change_log.md` if it exists. For each deferred patch in the prior cycle's outstanding actions table: confirm whether the corresponding prompt change was subsequently applied and logged. If a deferred patch has been carried forward without a prompt_change_log entry for two or more cycles, treat it as a recurrence escalation regardless of whether it appeared as a friction item this cycle.

**Patch-ID matching requirement (LL-v8.6-P4-01b):** When checking whether a deferred patch was subsequently applied, search `prompt_change_log.md` by the friction item's own patch-ID tag (e.g. `LL-v8.4-P4-01`) if one was assigned at filing — not by date range or filename alone. A date/filename-only search can miss an entry whose prose describes the same fix in different words, producing a false-positive "still unapplied" recurrence claim that then propagates into later cycles' own carry-forward records. Confirmed live at `2026-08-11__release-v8.6`: `2026-08-08__release-v8.5`'s own closure record claimed the `execution_prompt.md` `test_scenarios` roll-up patch (`LL-v8.4-P4-01`) was "still unapplied after 2 consecutive cycles" when it had in fact already shipped the same day that claim's own record was filed — the recurrence check had not searched by the patch's own ID tag.

If some files are missing:
- Record the absence as a process failure
- Do not invent content

---

## 4. Output (Filed Record)

### 4.1 Output path

The output path depends on the invoking routine:

| Invoked by | Output file | Notes |
|-----------|-------------|-------|
| Roadmap Rebalance (STEP 11) | `claude/cycles/<cycle_id>/lessons_learnt.md` | Standalone prose file (§5 record structure) |
| Release Planning (STEP 8) | `claude/cycles/<cycle_id>/lessons_learnt.md` | Standalone prose file (§5 record structure) |
| Sprint Execution (STEP 5.4) | `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` — append `## Phase 3` section | Structured table append (§4.2); idempotency guard required; cycle_id as field |
| Delivery Verification (STEP 8.5) | `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` — append `## Phase 4` section | Structured table append (§4.2); idempotency guard required; cycle_id as field |
| Amendment Cycle (STEP 8) | `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` — append `## Amendment — <AMD-id>`; AND `amendments/<amendment_id>/amendment_lessons.md` | Both outputs required; `amendment_lessons.md` retained for backward compat |
| Post-Ship Closure | `claude/cycles/<cycle_id>/lessons_learnt_closure.md` | Standalone prose file (§5 record structure); meta-consumer of `lessons_learnt_cycle.md` |

Sprint Execution and Delivery Verification append phase-tagged sections to a shared `lessons_learnt_cycle.md` file in the cycle folder. Roadmap Rebalance, Release Planning, and Post-Ship Closure write standalone files. Amendment Cycle appends to both `lessons_learnt_cycle.md` and a standalone `amendment_lessons.md` in the amendment sub-folder.

### 4.2 Structured Table Block Format

When appending to `lessons_learnt_cycle.md`, use the following structure.

If `lessons_learnt_cycle.md` does not yet exist: create it with a lifecycle header before appending the first section:

```
Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: <date>
Cycle: <cycle_id>
```

Each phase append uses this structure:

```
## Phase 3

*(or ## Phase 4, or ## Amendment — <AMD-id>)*

**Phase:** Sprint Execution | Delivery Verification | Amendment
**Cycle:** <cycle_id>
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** <today>
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| <description> | Phase 3/4/Amendment | A/B/C/D/E | action-now / defer / decision | <action taken, or change required if deferred> | <role> | <date or cycle ID> |

**Recurrence Notes:**
[Any recurrence items identified for this phase. If none: "None."]
```

**Field rules:**
- `friction_item`: brief description (one line); enough to identify the friction without the full prose record
- `phase`: `Phase 3`, `Phase 4`, or `Amendment — <AMD-id>`
- `type`: exactly one of A–E (Type A through Type E per §5 classification)
- `classification`: `action-now` (applied this run), `defer` (target owner/cycle required), or `decision` (named authority required). A cycle with zero friction items must not file a placeholder row using any other value (e.g. "monitor") — write "No friction items identified this run" as prose in the Friction Log section instead, per the existing v7.2 Phase 4 precedent. (AUD-2026-07-20-005)
- `action`: the specific change made or required — file and section where possible
- `owner`: role name (required; no owner = escalation to Head of Specs Team)
- `target_date`: date or cycle ID (required for `defer` and `decision`; `—` for `action-now` already applied)

For `action-now` rows: the change must be applied during this run, version-bumped, and logged in `prompt_change_log.md`. Record the log entry reference in the `action` column.

For `defer` rows: owner and target_date are both required. A row without either is not valid — escalate to Head of Specs Team.

---

### 4.3 Header block

```
Owner: Infrastructure & Operations Documentation Owner
Status: Operational Record
Deployment Version: N/A
Report Date: <today>
Environment: Governance
Generated By: PMO Lead
Filed: <today>
```

### 4.4 Prompt Change Log (Separate Output — Append-Only)

When action-now patches are applied to any governed prompt or template, the PMO Lead must append an entry to `claude/system/prompt_change_log.md`.

If `claude/system/prompt_change_log.md` does not exist: create it now as Class 6 — Governance Prompt, owned by Head of Specs Team, Status: Active, Version: 1.0, before appending.

Each entry format:

```markdown
## <date> — <file path> v<old> → v<new>

- **Triggering friction item:** <friction item description from this lessons_learnt record>
- **Cycle:** <cycle_id>
- **Change applied:** <one sentence — what changed and why>
- **Confirmed by:** Head of Specs Team
```

This log is append-only. It is the canonical record of why every governed prompt version exists. It must be committed as part of the same cycle commit that includes the modified prompt file.

---

## 5. Record Structure (Must Use)

**Scope:** This structure applies to standalone lessons learnt files only — Roadmap Rebalance, Release Planning, and Post-Ship Closure outputs. For Sprint Execution (Phase 3), Delivery Verification (Phase 4), and Amendment outputs, use the Structured Table Block Format (§4.2) and append to `lessons_learnt_cycle.md`.

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
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to claude/system/prompt_change_log.md

→ Deferred patch (cannot apply this run):
  - File: <exact file path>
  - Section: <§ reference or "New section required">
  - Change required: <one sentence — specific enough to action without further clarification>
  - Owner: <role — required; no owner = escalation>
  - Target: <next run of this routine | specific cycle_id | date — required; no date = escalation>

[A patch entry of "we should improve X" with no file and section named is not valid. If no specific file can be identified, this item must be escalated to Head of Specs Team — record it under Escalations, not here.]

[A deferred patch with no named owner or no target date is not a valid deferred patch. It must be escalated to Head of Specs Team and recorded under Escalations.]

---

[Repeat for each friction item]

---

## Recurrence Escalations

[List any friction items marked Recurrence = Yes where the prior cycle's outstanding action was not resolved. These are automatic escalations — do not re-record as new outstanding actions.]
[Also list any deferred patch carried forward for 2+ cycles without a prompt_change_log entry.]

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| <description> | <cycle_id> | <action from prior record> | Head of Specs Team |

If none: "None."

---

## Process improvements actioned this run

[Summary table of all immediate patches applied.]

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| <path> | <§ ref> | <change> | <old → new> | Yes / Not applicable |

If none: "None applied this run."

---

## New files created this run

[List any new files created as part of improvements, with rationale.]
If none: "None."

---

## Outstanding deferred patches

[One row per deferred patch. Every row must have a named owner (role) and a target date. Rows without both are not valid and must instead appear in Escalations.]

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| <path> | <§ ref> | <change> | <role> | <target> |

If none: "None."

---

## Escalations

[Any items requiring Head of Specs Team or Product Owner resolution: governance gaps, authority boundary ambiguity, recurring conflicts, deferred patches with no identifiable file, deferred patches with no owner or no target date, recurrence escalations, deferred patches carried 2+ cycles without prompt_change_log entry.]

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| <description> | Governance gap / Authority ambiguity / Recurrence / Missing owner / Missing target | Head of Specs Team / Product Owner | <one sentence> |

If none: "None."

---

## Carry-Forward

Items: N

[List 0–5 items with clear engine-actionable implications for the next cycle. Fewer is better. Zero rows is valid. See `shared_standards.md §16.8` for schema and rules.]

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| <n> | <one-sentence observation from this cycle> | <what the engine should do differently next cycle> | Roadmap \| Release Planning \| Sprint Planning \| All |

If none: leave table empty (0 rows) — do not omit the section.
```

---

## 6. Action Rules (Non-Negotiable)

**6.1 Do not re-litigate decisions**
Do not argue whether roadmap outcomes, sprint scope selections, delegation decisions, deviation severity calls, or closure document updates were "right". Focus only on process quality and governance integrity.

**6.2 Every friction item requires a process patch with valid fields**
Every friction item must have a process patch entry. There are only two valid states:
- **Immediate patch:** applied this run. Requires: file, section, change, version — all four fields. Requires Head of Specs Team explicit confirmation. Requires a prompt change log entry in `claude/system/prompt_change_log.md`.
- **Deferred patch:** not applied this run. Requires: file, section, change, named owner (role), target date — all five fields. A deferred patch missing owner or target date is not a valid deferred patch.

"We should improve X" with no file and section is not a valid entry in either category. It is an escalation to the Head of Specs Team. Record it under Escalations.

A deferred patch with no named owner is an escalation. A deferred patch with no target date is an escalation. Record both under Escalations, not in the outstanding deferred patches table.

**6.3 Apply immediate patches now — with sign-off**
If a friction point can be resolved by updating a template or governance prompt during this run: apply the change immediately, but only after the Head of Specs Team explicitly confirms the patch. Lifecycle compliance is required:
- correct owner
- correct status
- version increment when meaning changes
- Last Updated date updated
- entry appended to `claude/system/prompt_change_log.md`

Record the change in the "Process improvements actioned" table with the prompt change log column completed.

**6.4 Escalate what is outside PMO remit**
Escalate to Head of Specs Team and/or Product Owner when:
- No specific file or section can be identified for a patch
- The issue is a governance gap or authority boundary ambiguity
- A recurring conflict between domain owners is unresolved
- A friction item is marked Recurrence = Yes with an open prior outstanding action
- A deferred patch has no named owner
- A deferred patch has no target date
- A deferred patch has been carried forward for 2 or more cycles without a corresponding prompt_change_log entry
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
- Head of Specs Team must confirm lifecycle compliance for any modified governed document before it is written

---

## 8. Completion Condition

This prompt completes only when:
- The output file exists at the correct path for the invoking routine (§4.1)
- It follows the required structure (§5) with no omitted sections
- Every friction item has a classification, blast radius, and process patch
- Every process patch is either immediate (with file, section, change, version, Head of Specs Team confirmation, and prompt change log entry) or deferred (with file, section, change, named owner, and target date) — or is recorded as an escalation
- Recurrence check is recorded (even if prior file not found)
- Recurrence escalations table is present (even if empty)
- Any immediate patches are reflected in updated files with correct lifecycle versioning
- All prompt change log entries have been appended to `claude/system/prompt_change_log.md`
- All deferred patches in the outstanding actions table have a named owner (role) and a target date — rows without both are invalid and must be in Escalations instead
- Escalations table is present (even if empty)

---

## Change Log

See: [`claude/system/changelogs/lessons_learnt_changelog.md`](changelogs/lessons_learnt_changelog.md)