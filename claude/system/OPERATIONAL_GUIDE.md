# Sprint Planning Operational Playbook

**Owner:** Head of Specs Team  
**Status:** Active  
**Version:** 1.6  
**Last Updated:** 2026-03-03  
**Lifecycle Guide:** `claude/charter/document_lifecycle_guide.md`  
**Team Charter:** `claude/charter/team_charter.md`  

---

## Quick Reference Summary

> **The full cycle in one paragraph:** A completed roadmap item optionally triggers a **Roadmap Rebalance** (Phase 1), which reassesses priorities and decides what to add, stop, defer, or kill. The output (or a direct invocation) feeds **Release Planning** (Phase 1B), which translates an approved release into an execution-ready plan with a sequenced backlog slice. That backlog drives **Sprint Planning** (Phase 2), which scopes and capacity-confirms a time-boxed sprint. **Sprint Execution & Close** (Phase 3) delivers the work, closes the sprint, and — when a roadmap item completes — may trigger the next cycle. **Delivery Verification** (Phase 4) confirms what was built matches what was scoped and unlocks the next cycle. **Post-Ship Closure** then closes all planning and operational documents, applies lessons learnt, and confirms the cycle is clean before the next one opens.

### Engine Commands & Aliases

```bash
# Phase 1 — Roadmap Rebalance (OPTIONAL — triggers on completed roadmap item)
run roadmap --item-id "<id>" --item-name "<name>" [--date "YYYY-MM-DD"]

# Phase 1B — Release Planning (primary entry point)
plan release --version "<vX.Y>" [--date "YYYY-MM-DD"] [--timebox "<text>"] \
  [--capacity "<text>"] [--mode "strict|standard"] \
  [--issues "none|import|gh"] [--auto-escalate "true|false"]

# Alias (CLAUDE.md shorthand)
run planning v<version>     # equivalent to: plan release --version "v<version>"

# GitHub issue sync (run after Phase 1B publishes)
sync gh                     # parses active stage4_backlog_slice.md → creates/updates issues

# Phase 3 — Sprint Execution
run sprint [--cycle "<cycle_id>"] [--epic "<EPIC-xx>"] [--item "<ST-xx>"] [--mode "strict|standard"] [--dry-run]

# Phase 4 — Delivery Verification
run delivery verification [--cycle "<cycle_id>"] [--mode "strict|standard"]

# Post-Ship Closure
run post-ship [--cycle "<cycle_id>"] [--mode "strict|standard"] [--dry-run]
```

### Git Standards

```
Branch naming:  exec/<cycle_id>/<epic_id>
Commit prefix:  [EPIC-xx][ST-xx] <message>
State pointer:  .claude_current_state.json  (always check for active_cycle before invoking)
```

### Hard Rules (Never Override)

| Rule | Applies To |
|------|-----------|
| No roadmap addition without an equal or greater stop | Phase 1 |
| Delivery pressure never redefines strategy intent | All phases |
| Decision log is append-only | Phase 1 |
| Authority boundaries are absolute — no role merging | All phases |
| Non-decision roles enforce process only — no decisions | All phases |
| Strategy / Quality / Lifecycle risks may **never** be Accepted Risk | All phases |
| Publish Gate must pass before a release plan is sealed | Phase 1B |
| Backlog lock must be acquired before any backlog write | Phase 1B |
| No sprint starts without signed-off backlog and acceptance criteria | Phase 2 |
| No autonomous merge — QA sign-off and Product Owner acceptance always required | Phase 3 |
| No cycle unlock without `Verified` or `Verified_with_deviations` status | Phase 4 |
| Post-Ship Closure must complete before the next cycle's Phase 1 or Phase 1B is invoked | Post-Ship |

### Conflict Resolution — Who Wins What

| Dispute Type | Decider | Can PO Override? |
|-------------|---------|-----------------|
| Lifecycle compliance, document class | Head of Specs Team | No |
| Strategy intent / §13 boundary | Strategy Rules Owner | No — requires versioned strategy revision |
| Quality / release readiness | Director of Quality | No |
| Workforce economics constraint | FinOps & Resource Architect | No — PO chooses *which* work stops, not whether the constraint applies |
| Prioritisation / value trade-offs | Product Owner (tie-breaker) | Yes — dissent recorded |
| Process halt | Facilitator halt stands until gate remediated | No |

### Phase Gate Checklist

```
Phase 1 complete? (optional)
  ✅ current_roadmap.md updated and lifecycle-compliant
  ✅ backlog.md reconciled (Add/Replace/Defer/Kill reflected)
  ✅ decision_log.md appended
  ✅ lessons_learnt.md filed
  ✅ Commit done (or commit manifest produced)

Phase 1B complete?
  ✅ state.json status = Published
  ✅ publish_eligible = true
  ✅ stage4_backlog_slice.md committed to backlog.md (with idempotency marker)
  ✅ .claude_current_state.json updated
  ✅ cycle_summary.md and lessons_learnt.md filed
  ✅ No open escalations
  ✅ Backlog lock released

Phase 2 complete?
  ✅ Sprint goal approved by Product Owner
  ✅ Sprint backlog with acceptance criteria per item
  ✅ Capacity confirmed — no over-allocation
  ✅ Product Owner sign-off recorded in sprint_backlog.md

Phase 3 complete?
  ✅ All items have a recorded outcome (Done / Returned / Deferred)
  ✅ Acceptance criteria verified for all Done items
  ✅ One qa_evidence_EPIC-xx.md per merged EPIC, consolidation block complete
  ✅ Sprint close summary filed with verification readiness statement
  ✅ docs/System_status_report.md updated with this sprint's section
  ✅ lessons_learnt_execution.md filed
  ✅ execution_state.json sealed
  ✅ .claude_current_state.json status = Sprint_Complete
  ✅ STEP 8 commit complete

Phase 4 complete?
  ✅ verification_report.md status = Verified or Verified_with_deviations
  ✅ Director of Quality sign-off recorded in verification_report.md
  ✅ Product Owner acceptance recorded in verification_report.md
  ✅ docs/System_status_report.md updated
  ✅ All outstanding items backlogged or confirmed done
  ✅ Test scenario gaps sent to QA & Testing Owner
  ✅ .claude_current_state.json status = Verified
  ✅ next_cycle_unblocked = true

Post-Ship Closure complete?
  ✅ Changelog entry written and complete (docs/product/changelog.md)
  ✅ Roadmap entry marked ✅ Complete with ship date and cycle_id (claude/roadmap/current_roadmap.md)
  ✅ All shipped backlog items marked COMPLETE; Phase 4 additions confirmed present (claude/backlog/backlog.md)
  ✅ Scope document updated to Superseded
  ✅ Decisions record updated to Superseded
  ✅ Canonical spec deviation notes confirmed compliant (all required fields present)
  ✅ Supporting operational documents current (System_status_report.md, validation_system.md)
  ✅ Specs Index open items reviewed (resolved items closed, new gaps added)
  ✅ Both lessons learnt records reviewed and actions applied or scheduled
  ✅ Closure confirmation communicated to Product Owner and Head of Specs Team
```

---

## Table of Contents

1. [Purpose & Scope](#1-purpose--scope)
2. [Roles & Authorities](#2-roles--authorities)
3. [Document Classes Reference](#3-document-classes-reference)
4. [Lifecycle Overview](#4-lifecycle-overview)
5. [Phase 1 — Roadmap Rebalance (Optional)](#5-phase-1--roadmap-rebalance-optional)
6. [Phase 1B — Release Planning](#6-phase-1b--release-planning)
7. [Phase 2 — Sprint Planning](#7-phase-2--sprint-planning)
8. [Phase 3 — Sprint Execution & Close](#8-phase-3--sprint-execution--close)
9. [Phase 4 — Delivery Verification](#9-phase-4--delivery-verification)
10. [Post-Ship Closure](#10-post-ship-closure)
11. [Escalation & Accepted Risk Rules](#11-escalation--accepted-risk-rules)
12. [Cycle Trigger & Flow Reference](#12-cycle-trigger--flow-reference)
13. [Artefact Register](#13-artefact-register)
14. [Playbook Governance](#14-playbook-governance)

---

## 1. Purpose & Scope

This playbook governs the repeating cycle through which product releases are planned, sprinted, and delivered. It is the single source of operational truth for:

- When and how to invoke the Roadmap Rebalance Engine (optional)
- When and how to invoke the Release Planning Engine
- How planning artefacts feed into sprint scope
- How to execute, review, and close a sprint
- How to verify delivery before the next cycle opens
- What records must be maintained at each stage
- Which role resolves which dispute

**Out of scope:** Day-to-day task management, individual engineering decisions, and tooling configuration.

---

## 2. Roles & Authorities

All authority is defined in `claude/charter/team_charter.md`. The table below summarises decision-making rights. Domain blocks (Quality, Strategy, Lifecycle) **cannot be overridden by the Product Owner**.

| Role | Phase | Authority Type |
|------|-------|----------------|
| Product Owner | 1, 1B, 2, 3, 4 | Final decision — prioritisation, rebalance, scope; acceptance of deviations |
| Strategy Rules & System Intent Owner | 1, 1B | Veto — strategy alignment and §13 boundaries |
| Head of Specs Team | 1, 1B, 2 | Veto — lifecycle compliance; tie-breaker on spec conflicts |
| PMO Lead | 1, 1B, 2, 3, 4 | Process enforcement; gate validation; lessons learnt; verification invoker |
| FinOps & Resource Architect | 1, 1B | Binding constraint — workforce economics gate |
| Infrastructure & Operations Owner | 1, 1B | Run manifest and cycle artefact filing |
| Director of Quality | 1, 1B, 3, 4 | Veto — quality gates, QA evidence sign-off, verification report sign-off |
| QA & Testing Owner | 3, 4 | Test scenario creation; receives coverage gap actions from Phase 4 |
| Facilitator | All | Non-decision: process orchestration, hard gate enforcement, halt authority |
| Challenger | 1 | Non-decision: evidence-based counter-arguments, delay authority |

**Governance stack (precedence order):**

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

No document may override the above without a formal versioned update to the relevant governing document.

---

## 3. Document Classes Reference

All artefacts in this system belong to exactly one class, which determines required headers, valid lifecycle states, and who may create or modify them.

| Class | Name | Owner | Key Rule |
|-------|------|-------|----------|
| **1** | Canonical | Domain owner | Source of truth; all others must not contradict it |
| **2** | Supporting | Domain owner or designated maintainer | Derives authority from its Class 1 source; must stay aligned |
| **3** | Operational Record | Infra & Ops Documentation Owner | Immutable after filing; permanent; never superseded |
| **4** | Planning Document | Product Owner | Pre-canonical; may not be cited as canonical intent |
| **5** | Role Charter | Head of Specs Team / functional lead | Every decision-authority role must have one |
| **6** | Governance Prompt | Head of Specs Team | Stored in `claude/system/`; defines invocation, write scope, governance steps |

**Required header fields — quick reference:**

- **Class 1:** Owner, Status: Canonical, Version, Last Updated
- **Class 3:** Owner, Status: Operational Record, Deployment Version, Report Date, Environment, Generated By, Filed
- **Class 4:** Owner, Class: Planning Document (Class 4), Status (Draft/Active/Superseded), Last Updated
- **Class 6:** Owner, Status: Active, Version, Last Updated

A document without a complete header is non-compliant and must not be treated as authoritative.

**Known Deviation Standard (Class 1 documents):** Any deviation from canonical behaviour documented in a spec must include: description, canonical requirement, priority (P0–P3), target resolution release, owner, and backlog reference. P0 deviations must resolve before the next release ships. Undated or unprioritised deviation notes are non-compliant.

---

## 4. Lifecycle Overview

Each cycle progresses through up to five phases:

| Phase | Name | Trigger | Output |
|-------|------|---------|--------|
| **Phase 1** | Roadmap Rebalance | Roadmap item completed | Updated roadmap + decision log |
| **Phase 1B** | Release Planning | Phase 1 complete *or* direct invocation | Sequenced release plan + backlog slice |
| **Phase 2** | Sprint Planning | Phase 1B Publish Gate passed | Sprint backlog + acceptance criteria |
| **Phase 3** | Sprint Execution & Close | Sprint start date reached | Delivered increments + sprint close record |
| **Phase 4** | Delivery Verification | Phase 3 complete (`Sprint_Complete`) | Verification report + next cycle unlocked |
| **Post-Ship** | Post-Ship Closure | Phase 4 complete (`Verified`) | Closed documents + applied lessons learnt |

Phase 1 is **optional**. Phase 1B may be invoked directly when a release is already approved on the roadmap. Phases 2, 3, and 4 are always required. Each phase must fully exit before the next begins.

**Phase 4 is a hard gate on the next cycle.** The Roadmap Rebalance and Release Planning engines will not run for a new cycle until `.claude_current_state.json` status is `Verified` or `Verified_with_deviations`. Post-Ship Closure must also be complete before the next cycle opens — `next_cycle_unblocked = true` is necessary but not sufficient.

---

## 5. Phase 1 — Roadmap Rebalance (Optional)

**Source prompt:** `claude/system/roadmap_prompt.md` (v1.5)  
**Invoke when:** A roadmap item completes and a priority reassessment is warranted before proceeding to release planning.

### 5.1 Invocation

```
run roadmap --item-id "<id>" --item-name "<name>" [--date "YYYY-MM-DD"]
```

- `--item-id` required (e.g., `3.2`)
- `--item-name` must uniquely match an item in `current_roadmap.md`
- `--date` defaults to today
- Any other input is treated as conversational — the Engine will not run

### 5.2 Preflight Checklist

| Check | Requirement | Action if Fail |
|-------|-------------|----------------|
| Required files present | charter, lifecycle guide, strategy rules, roadmap, backlog | Halt |
| Header compliance | Class 4 headers on roadmap + backlog | Apply Step 0.A header remediation (headers only) |
| Authority roles exist | All 9 required roles have agent files in `claude/agents/` | Halt |
| Write permission | `claude/cycles/` writable | Halt |

### 5.3 Engine Steps

| Step | Name | Gate | Output |
|------|------|------|--------|
| STEP -1 | Preflight | **HARD** | Pass / Halt |
| STEP 0 | Load & Validate Inputs | **HARD** | Validated inputs; `cycle_id` defined |
| STEP 1 | Run Manifest & Capacity Release | — | `run_manifest.md` |
| STEP 2 | Roadmap Re-Validation | — | `stage1_validation.md` |
| STEP 3 | Backlog Health Review | — | `stage2_backlog_health.md` |
| STEP 4 | Idea Intake & Eligibility Gate | — | `stage3_ideas.md` |
| STEP 5 | Structured Debate (Zero-Sum) | — | `stage4_debate.md` |
| STEP 6 | Scoring Matrix Overlay | — | `scored_initiatives.md` |
| STEP 7 | Workforce Economics Gate | **HARD** | `workforce_capacity.md` |
| STEP 8 | Final Rebalance Decision | — | `stage5_rebalance.md` |
| STEP 8.5 | Stateless Write Safety Gate | **HARD** | Verified write plan |
| STEP 8.6/8.7 | Fatigue Detection + Pivot Loop | **HARD** | Guardrail check |
| STEP 9 | Canonical Write | — | Updated roadmap, backlog, decision log |
| STEP 10 | Publish Delta Summary | — | `cycle_summary.md` |
| STEP 11 | Lessons Learnt | — | `lessons_learnt.md` |
| STEP 12 | Stage & Commit | **HARD** | Git commit or commit manifest |

**Key constraints:**
- STEP 5: No candidate advances without naming a displacement. No name = cannot proceed.
- STEP 8.6: At least one candidate per run must be Parked or Rejected. If all advance, Pivot Loop runs once. If all still advance, execution halts.
- STEP 9 write scope is restricted — no files outside the allowed list may be modified.

### 5.4 Phase 1 Exit Criteria

- `current_roadmap.md` updated and lifecycle-compliant
- `backlog.md` reconciled (Add / Replace / Defer / Kill reflected)
- All decisions in `decision_log.md` (append-only)
- Stopped work explicitly named
- Workforce implications documented
- `lessons_learnt.md` filed
- STEP 12 commit complete

---

## 6. Phase 1B — Release Planning

**Source prompt:** `claude/system/release_planning_prompt.md` (v2.7)  
**Purpose:** Translate an already-approved roadmap release into an execution-ready plan: sequencing, dependencies, acceptance gates, backlog slice, optional GitHub issues.

> **This routine does NOT rebalance the roadmap.** It may not add, replace, defer, or kill initiatives. Those remain reserved for Phase 1.

### 6.1 Invocation

```
plan release --version "<vX.Y>" [--date "YYYY-MM-DD"] [--timebox "<text>"] \
  [--capacity "<text>"] [--mode "strict|standard"] \
  [--issues "none|import|gh"] [--auto-escalate "true|false"]

# Shorthand alias:
run planning v<version>
```

| Flag | Required | Notes |
|------|----------|-------|
| `--version` | Yes | Must match a planned release label in `current_roadmap.md` |
| `--date` | No | Defaults to today |
| `--timebox` | No | e.g., `"1 week"`, `"2 sprints"` |
| `--capacity` | No | e.g., `"solo-dev evenings"`, `"full-time"` |
| `--mode` | No | `strict`: halt on any gap; `standard`: proceed with flagged assumptions |
| `--issues` | No | `none` / `import` (creates `issue_import.md`) / `gh` (uses `gh` CLI, falls back to `import`) |
| `--auto-escalate` | No | `true` (default): routes and attempts resolution; `false`: records only, halts |

**Before invoking:** Check `.claude_current_state.json` for `active_cycle` and `status`. Do not invoke if status is `Blocked` without first resolving open escalations. Do not invoke if status is anything other than `Verified`, `Verified_with_deviations`, or a fresh cycle start — Phase 4 must complete before Phase 1B opens a new cycle.

### 6.2 State Machine

All progress is recorded in `claude/cycles/<cycle_id>/state.json`. The routine is resumable from the last completed step.

| Macro-State | Meaning |
|-------------|---------|
| `Initialized` | Run manifest + state created |
| `Planning` | Stage 3 (Execution Plan) exists and Stage 3.5 (Model Integrity) passed |
| `Committed` | Stage 4 (Backlog Slice) passed and committed to `backlog.md` |
| `Validated` | All gates passed; Publish Gate eligible |
| `Published` | Sealed; immutable; cycle summary + lessons filed |
| `Blocked` | One or more open escalations; Publish Gate cannot pass |

**Terminal state rule:** Once `Published`, the cycle folder is sealed. No step may re-run, no artefact may be modified, no escalation may be appended. Any post-publish change requires a new **amendment cycle** referencing the original `cycle_id`.

### 6.3 Engine Steps

| Step | Name | Gate | Output |
|------|------|------|--------|
| STEP -1 | Preflight | **HARD** | Pass / Halt |
| STEP 0 | Run Manifest + Initialize State | **HARD** | `run_manifest.md`, `state.json` |
| STEP 1 | Release Readiness Validation | — | `stage1_readiness.md` |
| STEP 2 | Scope Extraction | — | `stage2_scope_extraction.md` (S2-xx IDs required) |
| STEP 3 | Execution Plan | — | `stage3_execution_plan.md` (EPIC-xx + Maps to + RISK-xx required) |
| STEP 3.5 | Local Model Integrity Check | Conditional | `stage3_5_model_integrity.md` |
| STEP 3.9 | Shared Write Lock Preflight | **HARD** | Backlog lock acquired |
| STEP 4 | Backlog Slice | **HARD** | `stage4_backlog_slice.md` + backlog updated |
| STEP 4.5 | Capacity Feasibility Sense Check | Conditional | `stage4_5_capacity_check.md` |
| STEP 5 | Roadmap Annotation | — | Roadmap execution notes updated |
| STEP 5.5 | Cross-Stage Integrity Validation | **HARD** | `stage5_5_cross_stage_integrity.md` |
| STEP 5.7 | Decision Record Integrity Validation | **HARD** | `stage5_7_decision_record_integrity.md` |
| STEP 7 | Cycle Summary | — | `cycle_summary.md` |
| STEP 8 | Lessons Learnt | — | `lessons_learnt.md` |
| STEP 9 | Global State Synchronization | **HARD** | `.claude_current_state.json` updated |
| STEP 10 | Stage, Commit & Push | — | Git commit; issues if `--issues gh` |

### 6.4 Identifier Standards

All artefacts use stable IDs — missing IDs are a Process Integrity failure that halts execution.

| Type | Format | Required on |
|------|--------|-------------|
| Scope items | `S2-01`, `S2-02`, … | Stage 2 |
| Epics | `EPIC-01`, `EPIC-02`, … | Stage 3 |
| Stories / tasks | `ST-01`, `TASK-01`, … | Stage 3 (recommended) |
| Risks | `RISK-01`, `RISK-02`, … | Stage 3 |
| Escalations | `ESC-YYYYMMDD-nn` | Escalations file |

Every Stage 3 epic must declare `Maps to: S2-xx`. Every Stage 4 backlog slice must reference EPIC IDs exactly (no free-text epics).

### 6.5 Backlog Concurrency Control

Only one governed cycle may modify `claude/backlog/backlog.md` at a time.

- Lock file: `claude/backlog/.lock` (created at STEP 3.9, released after STEP 4 commits)
- If the lock exists and is owned by a different `cycle_id`: **halt** — no auto-delete, no override
- Stale locks: PMO Lead must manually release under the stale protocol (timestamp threshold + evidence of inactive owning cycle); removal recorded in the current cycle's escalation record

### 6.6 Publish Gate

The cycle may only be sealed `Published` if **all** of the following are true:

- `open_escalations` is empty
- Every deferred escalation has `Blocks execution: No`
- `stage4_5_capacity_check` is `pass` or `warn` (`warn` allowed in `standard` mode only)
- `stage5_5_cross_stage_integrity` is `pass`
- `stage5_7_decision_record_integrity` is `pass` or `not_applicable`
- `stage1_readiness` and `stage3_5_model_integrity` are `pass`
- `plan_structured = true`, `plan_executable = true`, `backlog_committed = true`
- All locks are `released` or `not_checked` (none `acquired` or `prepared`)

### 6.7 Phase 1B Exit Criteria

- `state.json` status = `Published`, `publish_eligible = true`
- `stage4_backlog_slice.md` committed to `backlog.md` with idempotency marker
- `.claude_current_state.json` updated
- `cycle_summary.md` and `lessons_learnt.md` filed
- No open escalations
- Backlog lock released

---

## 7. Phase 2 — Sprint Planning

Phase 2 converts the release-planned backlog into a time-boxed, executable sprint. It may only begin after Phase 1B exit criteria are satisfied.

### 7.1 Inputs

- Updated `claude/roadmap/current_roadmap.md`
- Committed `stage4_backlog_slice.md` and reconciled `backlog.md`
- `claude/roadmap/workforce_capacity.md`
- `cycle_summary.md` from the completed Phase 1B cycle

### 7.2 Sprint Planning Steps

1. **Define sprint goal** — One sentence describing the sprint's primary outcome. Owned by Product Owner.
2. **Capacity confirmation** — PMO Lead confirms available FTE, skills, and duration.
3. **Backlog grooming** — Head of Specs Team confirms each entering item has acceptance criteria, effort estimate, and explicit owner.
4. **Sprint scope selection** — Product Owner selects items from the release backlog slice within confirmed capacity. No item enters without acceptance criteria.
5. **Dependency check** — PMO Lead identifies cross-item dependencies and adjusts ordering.
6. **Sprint backlog sign-off** — Product Owner signs off. This is the Phase 2 exit gate.

### 7.3 Sprint Planning Artefacts

| Artefact | Location | Owner | Required? |
|----------|----------|-------|-----------|
| Sprint goal | `claude/cycles/<id>/sprint_goal.md` | Product Owner | Yes |
| Sprint backlog | `claude/cycles/<id>/sprint_backlog.md` | PMO Lead | Yes |
| Acceptance criteria | Per item in `sprint_backlog.md` | Head of Specs Team | Yes (per item) |
| Capacity confirmation | `claude/cycles/<id>/sprint_capacity.md` | PMO Lead | Yes |

### 7.4 Phase 2 Exit Criteria

- Sprint goal documented and approved by Product Owner
- Sprint backlog contains only items with defined acceptance criteria
- Capacity confirmed — no over-allocation
- Product Owner sign-off recorded in `sprint_backlog.md`

---

## 8. Phase 3 — Sprint Execution & Close

**Source prompt:** `claude/system/execution_prompt.md` (v1.3)

### 8.1 Invocation

```
run sprint [--cycle "<cycle_id>"] [--epic "<EPIC-xx>"] [--item "<ST-xx>"] [--mode "strict|standard"] [--dry-run]
```

| Flag | Notes |
|------|-------|
| `--cycle` | Optional — loaded from `.claude_current_state.json` if omitted |
| `--epic` | Optional — scope to a single EPIC |
| `--item` | Optional — scope to a single ST item |
| `--mode` | `strict`: halt on any ambiguity; `standard` (default): proceed with flags |
| `--dry-run` | Plan only — no writes, commits, or GitHub operations |

**Pre-condition:** `.claude_current_state.json` status must be `Committed`, `Validated`, or `Published` (release plan complete). If `Blocked`: resolve escalations first.

### 8.2 Execution Principles

- Scope is frozen at sprint start. New items require explicit Product Owner approval and a recorded decision.
- Blockers escalated same-day via escalation record (`ESC-EXEC-YYYYMMDD-nn`).
- Director of Quality QA gates apply to all EPICs before merge.
- Partial completion does not count — items must satisfy all acceptance criteria.
- The engine is fully resumable — re-invoke with the same command to resume from last state.
- **No autonomous merge.** QA sign-off and Product Owner acceptance are always required.

### 8.3 Delegation Model

Every ST item is classified on load. The engine acts autonomously where possible and delegates to humans where required.

| Class | Assigned To | Engine Action |
|-------|-------------|---------------|
| `autonomous` | Engine | Execute directly |
| `delegated_backend` | Head of Engineering | Assign with spec reference, park, continue |
| `delegated_frontend` | Base44 Frontend Prompt Owner | Assign with Base44 prompt draft, park, continue |
| `delegated_qa` | Director of Quality | Complete autonomous work, then await QA gate |
| `delegated_decision` | Named authority | Escalate, park, continue |

Delegated items are tracked in `delegation_log.md`. Nothing is silently skipped.

**Backend delegation:** Spec must be locked before delegating. If no lockable spec reference exists, classify as `delegated_decision` and surface to Head of Specs Team.

**Frontend delegation:** Engine must produce a complete Base44 prompt draft (all six sections: context, change, API contract, behaviour rules, non-functional rules, expected outcome) as part of the delegation record.

### 8.4 Key Artefacts Produced

| Artefact | Location | Purpose |
|----------|----------|---------|
| Execution state | `claude/cycles/<id>/execution_state.json` | Per-item progress, spec references, delegation status |
| QA evidence log | `claude/cycles/<id>/qa_evidence_EPIC-xx.md` | What was tested, Director of Quality sign-off (one per EPIC) |
| Delegation log | `claude/cycles/<id>/delegation_log.md` | All delegated task records |
| Sprint close record | `claude/cycles/<id>/sprint_close.md` | Outcomes, deviations filed, verification readiness statement |
| System status report | `docs/System_status_report.md` | Capabilities now live (updated at close) |
| Lessons learnt | `claude/cycles/<id>/lessons_learnt_execution.md` | Execution friction and improvement actions |

### 8.5 Merge Gate (Per EPIC — Hard Gate)

A PR may only be merged when all of the following are true:

- All ST items in EPIC: `done`
- `spec_references` populated for all `done` items
- `qa_evidence_EPIC-xx.md` exists and sign-off block complete (Director of Quality)
- QA sign-off comment on PR from Director of Quality
- Product Owner acceptance recorded
- `quality_gate.yml` CI passed
- No open escalations for items in this EPIC
- No unresolved P0 deviations in referenced specs

### 8.6 Phase 3 Exit Criteria

- All in-scope ST items have a recorded outcome (`done`, `merged`, or `returned_to_backlog`)
- All `done` items have `spec_references` populated and `deviations_filed = true`
- One `qa_evidence_EPIC-xx.md` per merged EPIC, consolidation block complete
- `sprint_close.md` filed with verification readiness statement
- `docs/System_status_report.md` updated with this sprint's section
- `lessons_learnt_execution.md` filed
- `execution_state.json` sealed
- `.claude_current_state.json` status = `Sprint_Complete`
- STEP 8 commit complete

---

## 9. Phase 4 — Delivery Verification

**Source prompt:** `claude/system/delivery_verification_prompt.md` (v1.0)

Phase 4 is a **mandatory gate** between sprint close and the next planning cycle. It verifies that what was built matches what was scoped, specified, and accepted.

### 9.1 Invocation

```
run delivery verification [--cycle "<cycle_id>"] [--mode "strict|standard"]
```

**Invoker:** PMO Lead. This command should be issued after the Director of Quality has confirmed (via QA evidence sign-offs in `qa_evidence_EPIC-xx.md`) that the sprint evidence is ready for verification. The readiness gate will fail fast if it is not.

**Pre-condition:** `.claude_current_state.json` status = `Sprint_Complete`. If not: Phase 3 must complete first.

### 9.2 What This Engine Verifies

| Check | Hard Gate? |
|-------|-----------|
| Sprint close verification readiness statement all `Yes` | Yes |
| Every ST item has a recorded outcome and spec reference | Yes |
| QA evidence logs exist and sign-off blocks are complete | Yes |
| No `Fail` results in any QA evidence table | Yes |
| P0 deviations: no open, no acceptance path | Yes |
| P1 deviations: hard block unless explicitly accepted by PO + DoQ in writing | Yes |
| P2 deviations: hard block unless explicitly accepted by PO in writing | Yes |
| Outstanding delegated items: confirmed done, pending ETA, or backlogged | No (recorded) |
| Test scenario coverage gaps: sent to QA & Testing Owner | No (actioned) |
| P3 deviations: recorded, backlogged | No (recorded) |

### 9.3 Deviation Severity Policy

| Priority | Condition | Verification outcome |
|----------|-----------|---------------------|
| P0 | System-breaking, data loss, or security issue | `Not_Verified` — no acceptance path |
| P1 | Material functional deviation | `Not_Verified` unless PO + DoQ both accept in writing |
| P2 | Degraded behaviour affecting significant user subset | `Not_Verified` unless PO accepts in writing |
| P3 | Minor / cosmetic / edge case | `Verified_with_deviations` — backlog item added |

### 9.4 Verification Outcomes

| Status | Meaning | Next cycle? |
|--------|---------|-------------|
| `Verified` | Clean pass — no open deviations | Unlocked |
| `Verified_with_deviations` | Accepted P1/P2 or P3 deviations only | Unlocked |
| `Not_Verified` | P0/P1/P2 blocks remain open | **Blocked** — re-run required |

### 9.5 Outstanding Delegated Items

Any ST item still blocked at sprint close must be resolved by Phase 4:

| Situation | Action |
|-----------|--------|
| Completed since sprint seal | Verified if acceptance criteria met |
| In progress with confirmed ETA | Recorded in report; Product Owner acknowledges |
| Stalled — no ETA | Added to `backlog.md` with context |
| `delegated_decision` never resolved | Added to `backlog.md` with decision question intact |

### 9.6 Test Scenario Coverage

If test scenario gaps are found (scenarios that exist in `docs/testing/` but were not run, or acceptance criteria with no scenario at all): the engine writes specific creation instructions directly to the QA & Testing Owner's agent file. These become backlog items for the next sprint if they cover core user journeys.

### 9.7 Phase 4 Artefacts Produced

| Artefact | Location | Owner |
|----------|----------|-------|
| Verification report | `claude/cycles/<id>/verification_report.md` | Director of Quality |
| System status report (updated) | `docs/System_status_report.md` | Director of Quality |
| Test scenario gap actions | `claude/agents/qa_testing_owner.md` (appended) | QA & Testing Owner |
| Backlog additions | `claude/backlog/backlog.md` (appended) | PMO Lead |
| Global state | `.claude_current_state.json` | Engine |

### 9.8 Phase 4 Exit Criteria

- `verification_report.md` status = `Verified` or `Verified_with_deviations`
- Director of Quality sign-off recorded in report
- Product Owner acceptance recorded in report
- `docs/System_status_report.md` updated to final verification status
- All outstanding items backlogged or confirmed done
- Test scenario gaps actioned to QA & Testing Owner
- `.claude_current_state.json` status = `Verified`, `next_cycle_unblocked = true`
- Commit complete

---

## 10. Post-Ship Closure

**Source prompt:** `claude/system/post_ship_closure_prompt.md` (v1.0)  
**Process document:** `docs/team_skills/pmo/processess/post-ship_closure.md` (v2.0)  
**Owner:** PMO Lead  
**Trigger:** Phase 4 complete — `.claude_current_state.json` status = `Verified` or `Verified_with_deviations`

Post-Ship Closure is the mandatory bridge between a verified sprint and a clean next cycle. It ensures all planning, operational, and governance documents reflect the shipped state before the next Phase 1 or Phase 1B is invoked.

> `next_cycle_unblocked = true` is a necessary but not sufficient condition for opening the next cycle. Post-Ship Closure must also be complete.

### 10.1 Invocation

```
run post-ship [--cycle "<cycle_id>"] [--mode "strict|standard"] [--dry-run]
```

| Flag | Notes |
|------|-------|
| `--cycle` | Optional — loaded from `.claude_current_state.json` if omitted |
| `--mode` | `strict`: halt on any missing document or incomplete field; `standard` (default): proceed with flags |
| `--dry-run` | Read all inputs and produce a closure plan without making any writes or commits |

**Pre-condition:** `.claude_current_state.json` status must be `Verified` or `Verified_with_deviations` and `next_cycle_unblocked = true`.

### 10.2 Inputs Required

- `.claude_current_state.json` — `status = Verified`, `next_cycle_unblocked = true`
- `claude/cycles/<cycle_id>/verification_report.md`
- `claude/cycles/<cycle_id>/sprint_close.md`
- `claude/cycles/<cycle_id>/execution_state.json` (sealed)
- `claude/cycles/<cycle_id>/lessons_learnt.md` (Phase 1B)
- `claude/cycles/<cycle_id>/lessons_learnt_execution.md` (Phase 3)
- `claude/cycles/<cycle_id>/lessons_learnt_verification.md` (Phase 4, if produced)
- `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` (one per merged EPIC)
- `docs/System_status_report.md`

### 10.3 Closure Steps

| Step | Document | Action | Failure Condition |
|------|----------|--------|-------------------|
| 1 | `docs/product/changelog.md` | Write versioned entry (EPIC IDs, spec versions updated, deviations accepted, verification report ref, `cycle_id`) | Missing entry — ship not recorded |
| 2 | `claude/roadmap/current_roadmap.md` | Mark feature ✅ Complete with ship date and `cycle_id`; update Current Version and Next planned release headers | Roadmap still shows Planned or In Progress |
| 3 | `claude/backlog/backlog.md` | Mark all shipped items COMPLETE; confirm Phase 4 additions present (returned items, P2/P3 deviations, test scenario gaps) | Shipped item still open; Phase 4 additions missing |
| 4 | Scope document | Status → Superseded; reference changelog entry, `verification_report.md`, and `cycle_id` | Scope document still Active after ship |
| 5 | Decisions record | Status → Superseded; reference changelog entry and `cycle_id` | Decisions record still Active after ship |
| 6 | Canonical specs | Confirm all deviation entries have required fields: description, canonical requirement, priority (P0–P3), target resolution release, owner, backlog reference | Deviation note missing required fields — spec non-compliant |
| 7 | `docs/System_status_report.md`, `docs/operations/validation_system.md` | Confirm current; update any stale "planned" or "backlog" notes | Operational docs reference superseded behaviour |
| 8 | `docs/specs/Specs_Index.md` | Mark resolved items closed with date and `cycle_id`; add new gaps identified during delivery | Index not reconciled with delivery |
| 9 | Lessons learnt (both records) | Review all action items; apply immediate process improvements (bump template/prompt versions); schedule deferred actions; escalate decisions to named owners | Lessons learnt filed but not reviewed — process debt compounds |

### 10.4 Changelog Entry Structure

```
## v<X.Y> — <feature name> — <ship date>
Cycle: <cycle_id>
Verified: <Verified | Verified_with_deviations>
Verification report: claude/cycles/<cycle_id>/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-xx | <description> | <spec file#section> |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-ref | P1/P2/P3 | <one line> | PO / PO + DoQ |

### Tech backlog items shipped
- [ST-xx] <title> — <one line description>

Sign-off: Product Owner — <date>
QA sign-off: Director of Quality — <date>
```

### 10.5 Lessons Learnt Application

This release produces two lessons learnt records that must both be reviewed:

| Record | Location | Covers |
|--------|----------|--------|
| Release Planning lessons | `claude/cycles/<cycle_id>/lessons_learnt.md` | Phase 1B planning friction, escalation patterns, backlog quality |
| Sprint Execution lessons | `claude/cycles/<cycle_id>/lessons_learnt_execution.md` | Delegation patterns, GitHub integration, acceptance criteria gaps, gate friction |
| Delivery Verification lessons | `claude/cycles/<cycle_id>/lessons_learnt_verification.md` | Gate sequencing, deviation severity patterns, test coverage gaps, sign-off coordination |

For each record: actions that can be resolved by updating a template or prompt must be applied immediately with a version bump. Actions requiring a role decision must be surfaced to the relevant owner with a deadline. Filing without reviewing is equivalent to skipping.

### 10.6 Closure Status Values

| Status | Meaning | Next cycle? |
|--------|---------|-------------|
| `Closed` | All steps complete; no outstanding actions | Open immediately |
| `Closed_with_actions` | All steps complete; minor outstanding actions carried forward | Open — actions tracked in closure record |

### 10.7 Escalation

If a document owner has not made their required update and it is blocking closure:

- PMO Lead notifies the owner directly with the specific item and a 24-hour deadline
- If unresolved within 24 hours: escalate to Product Owner
- PMO Lead does not make content changes to documents outside their ownership — they coordinate and escalate
- The next cycle does not open until closure is confirmed, regardless of delivery pressure

### 10.8 Closure Confirmation

When all steps are complete, PMO Lead communicates to Product Owner and Head of Specs Team:

```
Post-ship closure complete — <cycle_id> — <date>
Release: v<X.Y> — <feature name>
Verification status: <Verified | Verified_with_deviations>
Lessons learnt applied: <N immediate> | <N deferred> | <N escalated>
Outstanding actions carried forward: <list or "none">
Next cycle may now open.
```

---

## 11. Escalation & Accepted Risk Rules

### 11.1 When an Escalation Is Mandatory

An escalation record must be created when:
- A hard gate halts execution
- A domain authority applies a block (Strategy, Quality, Workforce, Lifecycle)
- An unresolved cross-domain dispute cannot be resolved within the routine

Escalation ID prefixes by phase:
- Release Planning: `ESC-YYYYMMDD-nn`
- Sprint Execution: `ESC-EXEC-YYYYMMDD-nn`
- Delivery Verification: `ESC-VERIF-YYYYMMDD-nn`

### 11.2 Escalation SLAs

| Trigger Type | SLA | Can Be Accepted Risk? |
|-------------|-----|-----------------------|
| Lifecycle / Process Integrity | 24 hours | **Never** |
| Strategy boundary | 72 hours | **Never** |
| Quality | Before execution begins | **Never** |
| Workforce / Capacity | Next planning checkpoint | Yes — Product Owner only |
| Schedule / Delivery | Next planning checkpoint | Yes — Product Owner only |

### 11.3 Accepted Risk — Hard Constraints

The following domains may **never** be marked Accepted Risk:

- **Strategy Risk**
- **Quality Risk**
- **Lifecycle / Governance Risk**

These may only be Open or Deferred until resolved. Any attempt to mark them Accepted Risk is a governance violation and must result in a routine halt.

Workforce and Schedule/Delivery risks may be accepted by the Product Owner **only if**:
- No Strategy Risk is implicated
- No Quality gate is bypassed
- No Lifecycle compliance requirement is violated
- No scope change is introduced (scope changes require Phase 1)

### 11.4 Accepted Risk Decision Record (Hard Gate)

Any Accepted Risk disposition requires a durable decision record:

- Location: `docs/product/decisions/AR-<release>-<cycle_id>-<esc_id>.md`
- Class: Planning Document (Class 4)
- Owner: Product Owner
- Must include: decision title, escalation ID reference, risk domain, risk statement, impact statement, rationale, guardrails, time boundary (this release only), accepting authority
- Must be linked from the escalation entry and cycle summary

If the decision record cannot be created, the escalation remains Open/Deferred and the routine halts.

> **Note:** Decision records in Release Planning are only valid for Accepted Risk (Workforce/Schedule) and Strategy Rules Boundary confirmation. All other uses are non-compliant.

---

## 12. Cycle Trigger & Flow Reference

| Event | Triggers | Owner |
|-------|----------|-------|
| Roadmap item completed | Phase 1 (optional) or direct Phase 1B | Product Owner |
| Phase 1 exit criteria met | Phase 1B — Release Planning Engine | PMO Lead |
| Phase 1B Publish Gate passed | Phase 2 — Sprint Planning | PMO Lead |
| Sprint backlog signed off | Phase 3 — Sprint Execution | PMO Lead |
| Phase 3 complete (`Sprint_Complete`) | Phase 4 — Delivery Verification | PMO Lead |
| Phase 4 complete (`Verified`) | Post-Ship Closure | PMO Lead |
| Post-Ship Closure confirmed | New Phase 1 (optional) or Phase 1B cycle | Product Owner |
| Sprint item returned to backlog | Backlog reconciliation only (no new cycle) | Head of Specs Team |
| Governance gap detected | Escalation → Product Owner + Head of Specs Team | PMO Lead |
| Test scenario gap found (Phase 4) | Action written to QA & Testing Owner agent file | QA & Testing Owner |

> **Loop rule:** Phase 1 is only triggered when a roadmap item completes and a rebalance is warranted. Sprint items that are backlog items (not roadmap items) never trigger a rebalance.

> **Cycle gate:** Phase 1B (new cycle) may not open until Phase 4 of the previous cycle reaches `Verified` or `Verified_with_deviations` **and** Post-Ship Closure is confirmed complete.

---

## 13. Artefact Register

All artefacts must be lifecycle-compliant per `claude/charter/document_lifecycle_guide.md`.

| Artefact | Location | Class | Owner | Phase |
|----------|----------|-------|-------|-------|
| Team Charter | `claude/charter/team_charter.md` | 1 | Head of Specs Team | Governance |
| Document Lifecycle Guide | `claude/charter/document_lifecycle_guide.md` | 1 | Head of Specs Team | Governance |
| Strategy Rules | `claude/strategy/strategy_rules.md` | 1 | Strategy Rules Owner | Governance |
| Roadmap Rebalance Prompt | `claude/system/roadmap_prompt.md` | 6 | Head of Specs Team | Governance |
| Release Planning Prompt | `claude/system/release_planning_prompt.md` | 6 | Head of Specs Team | Governance |
| Sprint Execution Prompt | `claude/system/execution_prompt.md` | 6 | Head of Specs Team | Governance |
| Delivery Verification Prompt | `claude/system/delivery_verification_prompt.md` | 6 | Head of Specs Team | Governance |
| Shared Standards | `claude/system/shared_standards.md` | 6 | Head of Specs Team | Governance |
| Lessons Learnt Prompt | `claude/system/lessons_learnt_prompt.md` | 6 | Head of Specs Team | Governance |
| Current Roadmap | `claude/roadmap/current_roadmap.md` | 4 | Product Owner | 1 |
| Backlog | `claude/backlog/backlog.md` | 4 | Product Owner | 1, 1B, 4, Post-Ship |
| Initiative Register | `claude/roadmap/initiative_register.md` | 4 | Product Owner | 1 |
| Workforce Capacity | `claude/roadmap/workforce_capacity.md` | 4 | FinOps & Resource Architect | 1 |
| Decision Log | `claude/roadmap/decision_log.md` | 4 | PMO Lead | 1 |
| Run Manifest (Rebalance) | `claude/cycles/<id>/run_manifest.md` | 3 | Infra & Ops Owner | 1 |
| Stage Outputs 1–5 | `claude/cycles/<id>/stage*.md` | 3 | PMO Lead | 1 |
| Cycle Summary (Rebalance) | `claude/cycles/<id>/cycle_summary.md` | 3 | PMO Lead | 1 |
| Lessons Learnt (Rebalance) | `claude/cycles/<id>/lessons_learnt.md` | 3 | PMO Lead | 1 |
| Scored Initiatives | `claude/scoring/scored_initiatives.md` | 4 | Facilitator | 1 |
| Run Manifest (Release) | `claude/cycles/<id>/run_manifest.md` | 3 | Infra & Ops Owner | 1B |
| State File | `claude/cycles/<id>/state.json` | — | PMO Lead | 1B |
| Backlog Lock | `claude/backlog/.lock` | — | PMO Lead | 1B |
| Backlog Transaction | `claude/cycles/<id>/backlog_txn.json` | — | PMO Lead | 1B |
| Stage 1 Readiness | `claude/cycles/<id>/stage1_readiness.md` | 3 | PMO Lead | 1B |
| Stage 2 Scope Extraction | `claude/cycles/<id>/stage2_scope_extraction.md` | 3 | PMO Lead | 1B |
| Stage 3 Execution Plan | `claude/cycles/<id>/stage3_execution_plan.md` | 3 | PMO Lead | 1B |
| Stage 4 Backlog Slice | `claude/cycles/<id>/stage4_backlog_slice.md` | 3 | PMO Lead | 1B |
| Escalations (Release) | `claude/cycles/<id>/escalations.md` | 4 | PMO Lead | 1B |
| AR / SRB Decision Records | `docs/product/decisions/AR-*.md` | 4 | Product Owner | 1B |
| Cycle Summary (Release) | `claude/cycles/<id>/cycle_summary.md` | 3 | PMO Lead | 1B |
| Lessons Learnt (Release) | `claude/cycles/<id>/lessons_learnt.md` | 3 | PMO Lead | 1B |
| Global State Pointer | `.claude_current_state.json` | — | PMO Lead | 1B, 3, 4 |
| Sprint Goal | `claude/cycles/<id>/sprint_goal.md` | 4 | Product Owner | 2 |
| Sprint Backlog | `claude/cycles/<id>/sprint_backlog.md` | 4 | PMO Lead | 2 |
| Sprint Capacity | `claude/cycles/<id>/sprint_capacity.md` | 4 | PMO Lead | 2 |
| Execution State | `claude/cycles/<id>/execution_state.json` | — | PMO Lead | 3 |
| QA Evidence Log | `claude/cycles/<id>/qa_evidence_EPIC-xx.md` | 4 | Director of Quality | 3 |
| Delegation Log | `claude/cycles/<id>/delegation_log.md` | 4 | PMO Lead | 3 |
| Escalations (Execution) | `claude/cycles/<id>/execution_escalations.md` | 4 | PMO Lead | 3 |
| Sprint Close Summary | `claude/cycles/<id>/sprint_close.md` | 3 | PMO Lead | 3 |
| Lessons Learnt (Execution) | `claude/cycles/<id>/lessons_learnt_execution.md` | 3 | PMO Lead | 3 |
| Lessons Learnt (Verification) | `claude/cycles/<id>/lessons_learnt_verification.md` | 3 | PMO Lead | 4 |
| Lessons Learnt (Closure) | `claude/cycles/<id>/lessons_learnt_closure.md` | 3 | PMO Lead | Post-Ship |
| System Status Report | `docs/System_status_report.md` | 3 | Director of Quality | 3, 4 |
| Verification Report | `claude/cycles/<id>/verification_report.md` | 3 | Director of Quality | 4 |
| Escalations (Verification) | `claude/cycles/<id>/verification_escalations.md` | 4 | PMO Lead | 4 |
| Changelog | `docs/product/changelog.md` | 3 | PMO Lead | Post-Ship |
| Post-Ship Closure Process | `docs/team_skills/pmo/processess/post-ship_closure.md` | 1 | PMO Lead | Post-Ship |
| Closure Record | `claude/cycles/<id>/closure_record.md` | 3 | PMO Lead | Post-Ship |

---

## 14. Playbook Governance

| Field | Value |
|-------|-------|
| Owner | Head of Specs Team |
| Status | Active |
| Version | 1.5 |
| Last Updated | 2026-03-03 |
| Review Cadence | After every 3 completed cycles, or on any governance gap escalation |
| Roadmap Engine Source | `claude/system/roadmap_prompt.md` v1.5 |
| Release Engine Source | `claude/system/release_planning_prompt.md` v2.7 |
| Execution Engine Source | `claude/system/execution_prompt.md` v1.3 |
| Verification Engine Source | `claude/system/delivery_verification_prompt.md` v1.0 |
| Post-Ship Closure Engine | `claude/system/post_ship_closure_prompt.md` v1.0 |
| Post-Ship Closure Process | `docs/team_skills/pmo/processess/post-ship_closure.md` v2.0 |
| Shared Standards | `claude/system/shared_standards.md` v1.1 |
| Lessons Learnt Prompt | `claude/system/lessons_learnt_prompt.md` v1.2 |
| Lifecycle Guide | `claude/charter/document_lifecycle_guide.md` v2.4 |
| Team Charter | `claude/charter/team_charter.md` v1.3 |

This playbook is subordinate to and must remain consistent with all governing documents above. In any conflict, governance documents prevail. Update this playbook to reflect the change — do not operate with a known divergence.

**Version control:** All changes require approval by the Head of Specs Team and must be version-bumped per lifecycle rules. Patch = typo/formatting. Minor = structural change. Major = scope change or authority boundary change.

---

### Change Log

| Version | Date | Change Summary |
|---------|------|----------------|
| 1.6 | 2026-03-03 | Updated `shared_standards.md` to v1.1 and `lessons_learnt_prompt.md` to v1.2 in §14 governance table. Added Lessons Learnt Prompt to Artefact Register. Added `lessons_learnt_verification.md` (Phase 4) and `lessons_learnt_closure.md` (Post-Ship) to Artefact Register. |
| 1.5 | 2026-03-03 | Added `post_ship_closure_prompt.md` (v1.0) as the engine source for §10. Added `run post-ship` invocation command to Quick Reference. Added invocation subsection (§10.1), flags table, and pre-condition to §10. Added closure status values (§10.6). Added Closure Record to Artefact Register. Added Post-Ship Closure Engine to §14 governance table. |
| 1.4 | 2026-03-03 | Added §10 Post-Ship Closure. Updated Quick Reference summary, Hard Rules, Phase Gate Checklist, Lifecycle Overview table, Cycle Trigger & Flow table, Artefact Register, and §14 governance table to reflect post-ship_closure.md (v2.0). Renumbered §10–13 to §11–14. Updated cycle gate rule to require Post-Ship Closure before next cycle opens. |
| 1.3 | 2026-03-03 | Added `execution_prompt.md` (v1.3) and `delivery_verification_prompt.md` (v1.0) to governance. Updated Quick Reference to include Phase 3 & 4 invocation commands. Added "no autonomous merge" and "no cycle unlock without Verified status" to Hard Rules. Expanded Phase 3 checklist to match execution prompt exit criteria. Aligned §8 (Phase 3) and §9 (Phase 4) detail with prompt content. Resolved header/§13 version discrepancy (both now 1.3). |
| 1.2 | 2026-03-02 | Prior version. |