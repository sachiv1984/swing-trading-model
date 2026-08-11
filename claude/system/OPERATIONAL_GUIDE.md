# Sprint Planning Operational Playbook

**Owner:** Head of Specs Team
**Status:** Active
**Version:** 4.153
**Last Updated:** 2026-08-10
**Lifecycle Guide:** `claude/charter/document_lifecycle_guide.md`  
**Team Charter:** `claude/charter/team_charter.md`  

---

## Quick Reference Summary

> **The full cycle in one paragraph:** A completed roadmap item optionally triggers a **Roadmap Rebalance** (Phase 1), which reassesses priorities and decides what to add, stop, defer, or kill. The output (or a direct invocation) feeds **Release Planning** (Phase 1B), which translates an approved release into an execution-ready plan with a sequenced backlog slice. That backlog drives **Sprint Planning** (Phase 2), which selects scope within confirmed capacity, confirms acceptance criteria per item, maps dependencies, and seals a signed-off sprint backlog. **Sprint Execution & Close** (Phase 3) delivers the work, closes the sprint, and — when a roadmap item completes — may trigger the next cycle. **Delivery Verification** (Phase 4) confirms what was built matches what was scoped and unlocks the next cycle. **Post-Ship Closure** then closes all planning and operational documents, applies lessons learnt, and confirms the cycle is clean before the next one opens.

### Engine Commands & Aliases

```bash
# Phase 1 — Roadmap Rebalance (OPTIONAL — triggers on completed roadmap item OR scheduled)
# Idea intake runs automatically as STEP -1.6 when open idea count < 20.
# Standalone intake (run ideas) remains supported for explicit window control.
run roadmap --item-id "<id>" --item-name "<name>" [--date "YYYY-MM-DD"]
run roadmap --reason "scheduled" [--date "YYYY-MM-DD"]

# Phase 1M — Document Management (OPTIONAL — run after Post-Ship Closure OR before run roadmap)
manage roadmap [--dry-run]                        # retire completed items, flag stale
groom backlog [--dry-run]                         # archive completed items, health check
run ideas housekeeping [--dry-run]                # archive terminal ideas rows, revival review

# Phase 1.5 — Design Gate (run after Phase 1B Publish Gate, before Phase 2)
run design-gate --cycle "<cycle_id>" [--dry-run]

# Phase 1B — Release Planning (primary entry point)
plan release --version "<vX.Y>" [--date "YYYY-MM-DD"] [--timebox "<text>"] \
  [--capacity "<text>"] [--mode "strict|standard"] \
  [--issues "none|import|gh"] [--auto-escalate "true|false"]

# Alias (CLAUDE.md shorthand)
run planning v<version>     # equivalent to: plan release --version "v<version>"

# GitHub issue sync (run after Phase 1B publishes)
sync gh                     # parses active stage4_backlog_slice.md → creates/updates issues

# Phase 2 — Sprint Planning
plan sprint [--cycle "<cycle_id>"] [--mode "strict|standard"] [--dry-run]

# Amendment Cycle (emergency only — after Phase 1B published, before Phase 2 sealed)
amend cycle --cycle "<original_cycle_id>" --reason "<emergency-fix|hard-blocker>" [--mode "strict|standard"]

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
| No roadmap addition without an equal or greater stop (net-zero or net-negative initiative count enforced by Roadmap Engine STEP 5 — applies in both `strict` and `standard` modes) | Phase 1 |
| Delivery pressure never redefines strategy intent | All phases |
| Decision log (`claude/roadmap/decision_log.md`) is append-only — **structural hard gate enforced by Roadmap Engine STEP 9**; a decrease in entry count halts the engine and blocks commit | Phase 1 |
| Authority boundaries are absolute — no role merging | All phases |
| Non-decision roles enforce process only — no decisions | All phases |
| Strategy / Quality / Lifecycle risks may **never** be Accepted Risk | All phases |
| Publish Gate must pass before a release plan is sealed | Phase 1B |
| Backlog lock must be acquired before any backlog write | Phase 1B, 1M |
| No sprint starts without signed-off backlog and acceptance criteria | Phase 2 |
| No item enters the sprint without confirmed acceptance criteria and an explicit owner | Phase 2 |
| No autonomous merge — QA sign-off and Product Owner acceptance always required | Phase 3 |
| No cycle unlock without `Verified` or `Verified_with_deviations` status | Phase 4 |
| Post-Ship Closure must complete before the next cycle's Phase 1 or Phase 1B is invoked | Post-Ship |
| Amendment cycles are emergency-only — delivery pressure never qualifies | Amendment |
| Amendments require two-authority ratification — PMO Lead may never self-approve | Amendment |
| Amendments are not permitted after Phase 2 seals (`sprint_sealed = true`) | Amendment |
| Design gate bypass requires `design_gate_bypass_authority` + `design_gate_bypass_reason` in state | Phase 2 |
| Release cycle may not open unless `post_ship_complete = true` and `next_cycle_unblocked = true` | Phase 1B |
| Any prompt version increment must have a matching entry in `prompt_change_log.md` | All phases |
| Backlog lock must be acquired before Amendment Cycle reads `sprint_sealed` | Amendment |

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
  ✅ lessons_learnt.md filed (structure per lessons_learnt_prompt.md §5)
  ✅ All action-now prompt patches applied, version-incremented, logged in prompt_change_log.md
  ✅ All deferred patches have named owner and target date (or recorded as escalations)
  ✅ Meta-review conducted if due (every third cycle); meta_review.md filed if so
  ✅ Commit done (or commit manifest produced)

Phase 1M complete? (optional)
  ✅ roadmap_archive.md updated (if any items retired)
  ✅ backlog_archive.md updated (if any items archived)
  ✅ Stale items flagged in current_roadmap.md (if any identified)
  ✅ Orphans and stale blockers flagged in backlog.md (if any identified)
  ✅ Manage roadmap run log written
  ✅ Backlog health report written
  ✅ No ambiguous items left unresolved
  ✅ Backlog lock released
  ✅ Commits complete for both engines

Phase 1B complete?
  ✅ state.json status = Published
  ✅ publish_eligible = true
  ✅ stage4_backlog_slice.md committed to backlog.md (with idempotency marker)
  ✅ docs/product/scope/scope--{cycle_id}-{slug}.md created (scope document)
  ✅ docs/product/decisions/decisions--{cycle_id}.md created (decisions record)
  ✅ .claude_current_state.json updated (STEP 7 intermediate sync + STEP 9 terminal sync both complete)
  ✅ cycle_summary.md and lessons_learnt.md filed
  ✅ No open escalations
  ✅ deferred_execution_blockers is empty
  ✅ Backlog lock released

Phase 2 complete?
  ✅ Sprint goal documented and confirmed by Product Owner (sprint_goal.md)
  ✅ sprint_backlog.md status = Sealed with Product Owner sign-off
  ✅ Every in-scope item has confirmed acceptance criteria (no [AC REQUIRED] placeholders)
  ✅ Every in-scope item has an effort estimate (no [ESTIMATE REQUIRED] placeholders)
  ✅ Capacity confirmed — no unresolved over-allocation
  ✅ Dependency map and execution sequence documented (sprint_planning_notes.md)
  ✅ Delegation class recorded per ST item
  ✅ .claude_current_state.json status = Sprint_Planning_Complete, sprint_sealed = true
  ✅ Commit complete

Phase 3 complete?
  ✅ All items have a recorded outcome (Done / Returned / Deferred)
  ✅ Acceptance criteria verified for all Done items
  ✅ One qa_evidence_EPIC-xx.md per merged EPIC, consolidation block complete
  ✅ Sprint close summary filed with verification readiness statement
  ✅ docs/System_status_report.md updated with this sprint's section
  ✅ lessons_learnt_cycle.md Phase 3 section appended (idempotency guard applied)
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
5. [Idea Intake (Integrated — Phase 1 STEP -1.6)](#5-idea-intake-integrated--phase-1-step--16)
6. [Phase 1 — Roadmap Rebalance (Optional)](#6-phase-1--roadmap-rebalance-optional)
7. [Phase 1M — Document Management (Optional)](#6m-phase-1m--document-management-optional)
8. [Phase 1.5 — Design Gate](#65-phase-15--design-gate-required)
9. [Phase 1B — Release Planning](#6b-phase-1b--release-planning)
   - [Amendment Cycle (Emergency Only)](#6b8-amendment-cycle-emergency-only)
10. [Phase 2 — Sprint Planning](#7-phase-2--sprint-planning)
11. [Phase 3 — Sprint Execution & Close](#8-phase-3--sprint-execution--close)
12. [Phase 4 — Delivery Verification](#9-phase-4--delivery-verification)
13. [Post-Ship Closure](#10-post-ship-closure)
14. [Escalation & Accepted Risk Rules](#11-escalation--accepted-risk-rules)
15. [Cycle Trigger & Flow Reference](#12-cycle-trigger--flow-reference)
16. [Artefact Register](#13-artefact-register)
17. [Playbook Governance](#14-playbook-governance)

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
| Head of Specs Team | 1, 1B, 2 | Veto — lifecycle compliance; tie-breaker on spec conflicts; sign-off required for all action-now prompt patches |
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
| **8** | Proof of Gate | Clearing authority role | Immutable once issued; status field only may change to Superseded; permanent governance record. *Reserved — not currently produced by any engine in this cycle.* |

**Required header fields — quick reference:**

- **Class 1:** Owner, Status: Canonical, Version, Last Updated
- **Class 3:** Owner, Status: Operational Record, Deployment Version, Report Date, Environment, Generated By, Filed
- **Class 4:** Owner, Class: Planning Document (Class 4), Status (Draft/Active/Superseded), Last Updated
- **Class 6:** Owner, Status: Active, Version, Last Updated
- **Class 8:** Owner, Class: Proof of Gate (Class 8), Status: Active, Gate ID, Issued, Cycle, Initiative, Gate cleared, Versioned document referenced, Decision, Confirmed by, Checksum note

A document without a complete header is non-compliant and must not be treated as authoritative.

**Known Deviation Standard (Class 1 documents):** Any deviation from canonical behaviour documented in a spec must include: description, canonical requirement, priority (P0–P3), target resolution release, owner, and backlog reference. P0 deviations must resolve before the next release ships. Undated or unprioritised deviation notes are non-compliant.

---

## 4. Lifecycle Overview

Each cycle progresses through up to six phases. Idea intake is integrated into Phase 1 (STEP -1.6) and runs automatically when fewer than 20 open ideas exist:

| Phase | Name | Trigger | Output |
|-------|------|---------|--------|
| **Phase 1** | Roadmap Rebalance (incl. idea intake at STEP -1.6) | Roadmap item completed OR scheduled review | Updated roadmap + decision log + prompt change log (if patches applied) |
| **Phase 1M** | Document Management | After Post-Ship Closure **or** immediately before `run roadmap` | Clean roadmap + healthy backlog |
| **Phase 1B** | Release Planning | Phase 1 complete *or* direct invocation | Sequenced release plan + backlog slice |
| **Phase 1.5** | Design Gate | After Phase 1B Publish Gate | Design artefacts approved + frontend specs updated |
| **Phase 2** | Sprint Planning | Phase 1B Publish Gate passed | Sprint backlog + acceptance criteria |
| **Phase 3** | Sprint Execution & Close | Sprint start date reached (`Sprint_Planning_Complete` + `sprint_sealed = true`) | Delivered increments + sprint close record; intermediate status `Executing` set at STEP 0 |
| **Phase 4** | Delivery Verification | Phase 3 complete (`Sprint_Complete`) | Verification report + next cycle unlocked |
| **Post-Ship** | Post-Ship Closure | Phase 4 complete (`Verified`) | Closed documents + applied lessons learnt |
| **Amendment** | Amendment Cycle | Emergency post-publish (before Phase 2 sealed) | Amended backlog slice + ratification record |

Phase 1 is **optional**. Idea intake (STEP -1.6) runs automatically within Phase 1 when fewer than 20 open ideas exist; it may also be invoked standalone via `run ideas` for explicit window control. Phase 1M is **optional but strongly recommended** at both valid trigger windows (see §6M). Phase 1B may be invoked directly when a release is already approved. Phase 1.5 (Design Gate) is **required** unless all sprint items are classified Design Not Applicable. Phases 2, 3, and 4 are always required. Each phase must fully exit before the next begins.

**Phase 4 is a hard gate on the next cycle.** The Roadmap Rebalance and Release Planning engines will not run for a new cycle until `.claude_current_state.json` status is `Verified` or `Verified_with_deviations`. Post-Ship Closure must also be complete before the next cycle opens — `next_cycle_unblocked = true` is necessary but not sufficient.

### 4.1 Lifecycle State Machine

The lifecycle is a deterministic state machine. `.claude_current_state.json` (`status` field) is the single source of truth. State may only move forward along defined transitions; backward movement is prohibited except `Blocked` resolving to `prior_status`.

**Allowed transitions:**

| From | To | Engine | Entry condition |
|------|----|--------|-----------------|
| `Closed` | `Release_Planning_Complete` | Release Planning | `post_ship_complete = true` |
| `Release_Planning_Complete` | `Design_Gate_Passed` | Design Gate | `design_gate_required = true` AND `sprint_sealed = false` |
| `Release_Planning_Complete` | `Sprint_Planning_Complete` | Sprint Planning | design gate not required for cycle |
| `Design_Gate_Passed` | `Sprint_Planning_Complete` | Sprint Planning | `design_gate_status = Passed` |
| `Sprint_Planning_Complete` | `Executing` | Sprint Execution | `sprint_sealed = true` |
| `Closed` | `Executing` | Sprint Execution | **Multi-sprint exception only:** `sprint_planning.sprint2_deferred` non-empty AND `sprint_sealed = true` (from prior sprint) AND `post_ship_complete = true`. Same `cycle_id` continued across sprints. |
| `Sprint_Planning_Complete` | `Amendment_In_Progress` | Amendment Cycle | `sprint_sealed = false` |
| `Amendment_In_Progress` | `Sprint_Planning_Complete` | Amendment Cycle | two-authority ratification complete |
| `Executing` | `Sprint_Complete` | Sprint Execution (STEP 8) | all EPICs merged or dispositioned |
| `Sprint_Complete` | `Verified` | Delivery Verification | `execution_state.json sealed = true` |
| `Sprint_Complete` | `Verified_with_deviations` | Delivery Verification | `execution_state.json sealed = true` |
| `Verified` | `Closed` | Post-Ship Closure | DoQ sign-off + PO acceptance in `verification_report.md` |
| `Verified_with_deviations` | `Closed` | Post-Ship Closure | DoQ sign-off + PO acceptance in `verification_report.md` |
| Any | `Blocked` | Any (hard gate fires) | Hard gate condition not met — write `prior_status` before halting |
| `Blocked` | `<prior_status>` | Resolving authority | Escalation resolved and recorded |

**Guard enforcement:** Every engine applies the Lifecycle Guard (entry state check) before executing any step. An engine that cannot pass the entry check must halt with a Lifecycle hard gate report — see `claude/system/shared_standards.md §10`. The full machine definition is at `claude/system/lifecycle_schema.json`.

---

## 5. Idea Intake (Integrated — Phase 1 STEP -1.6)

**Source prompt:** `claude/system/idea_intake_prompt.md` (v2.8)
**Template:** `claude/system/idea_template.md`
**Owner:** PMO Lead
**Trigger:** Automatic — runs as STEP -1.6 of `run roadmap` when fewer than 20 open ideas (status `Submitted` or `Parked-cycle-<n>`) exist in `claude/ideas/ideas_register.md`. Also invocable standalone via `run ideas` for explicit window control.

Idea intake opens a submission window, solicits structured idea submissions from all agent roles, appends/updates rows in `claude/ideas/ideas_register.md`, and closes the window. It does not evaluate, score, or debate ideas — that is STEP 4 and STEP 5 of the roadmap engine.

### 5.1 Invocation

```
run ideas [--window-id "<id>"] [--mode "strict|standard"]
```

| Flag | Notes |
|------|-------|
| `--window-id` | Optional — auto-generated as `IW-<YYYYMMDD>-<nn>` if omitted |
| `--mode` | `strict`: halt if any agent fails minimum submissions; `standard` (default): note gaps and proceed |

**Order:** Idea intake runs automatically at STEP -1.6 before STEP 0 of `run roadmap`. If invoked standalone, run `run ideas` before `run roadmap`. Ideas submitted after STEP 0 begins are not eligible for the current run.

### 5.2 Who Submits

All 22 agent roles defined in `claude/agents/` except the Facilitator. The Facilitator manages the intake process and is permanently excluded from idea generation — an absent window count is expected, not a process error. Minimum 2 net-new ideas per eligible agent per window. A resubmitted parked idea counts as net-new only if materially updated.

### 5.3 Idea Lifecycle

Each idea is one row in `claude/ideas/ideas_register.md`, identified by Idea ID: `IDEA-<agent-slug>-<YYYYMMDD>-<nn>`. Schema: per `shared_standards.md §16.5`.

| Status | Set by | Meaning |
|--------|--------|---------|
| `Submitted` | Idea intake engine | Filed during open window; awaiting STEP 4 review |
| `Parked-cycle-<n>` | Roadmap STEP 4 | Not ready; `<n>` = consecutive cycles parked. At 3+ cycles, Product Owner must make an active disposition — silent re-park not permitted |
| `Advancing` | Roadmap STEP 4 | Progressing to STEP 5 debate |
| `Promoted-Added` | Roadmap STEP 9 | Promoted in debate and added to roadmap |
| `Promoted-Rejected` | Roadmap STEP 5 | Promoted to debate but lost |
| `Rejected` | Roadmap STEP 4 | Not viable; file retained as record |
| `Rejected-Strong` | Roadmap STEP 4 | Rejected but strong; core content appended to `rejected_but_strong.md` |
| `Withdrawn` | Agent or idea intake engine | Withdrawn by submitter |

Parked ideas carry forward with an incrementing cycle count. At 3 or more consecutive cycles parked, the idea is considered stale and requires an active Product Owner disposition. All terminal-status rows are retained as permanent records in the register.

### 5.4 Displacement

The idea template includes a "What Would You Stop?" field as a thinking prompt — not a required decision. An answer of "No view — leave to debate" is valid. Displacement is determined in STEP 5 of the roadmap engine (§6.3) where all candidates and constraints are visible simultaneously.

### 5.5 Artefacts

| Artefact | Location | Owner | Required? |
|----------|----------|-------|-----------|
| Window state | `claude/ideas/ideas_window.json` | PMO Lead | Yes — opened and closed by engine |
| Ideas register | `claude/ideas/ideas_register.md` | PMO Lead | Yes — single register; rows appended per submission |
| Window summary | `claude/ideas/window_summary_<IW-id>.md` | PMO Lead | Yes |
| Rejected-but-strong register | `claude/ideas/rejected_but_strong.md` | PMO Lead | Created if needed by roadmap STEP 4 |
| Ideas register archive | `claude/ideas/ideas_register_archive.md` | PMO Lead | Created by ideas_housekeeping engine — append-only |
| Archived submissions | `claude/ideas/submissions/archive/*.md` | PMO Lead | Read-only — prior per-file submissions migrated 2026-03-17 |

### 5.6 Exit Criteria

- `ideas_window.json` status = `Closed`
- All agent submission rows appended to `ideas_register.md` (or gaps recorded)
- `window_summary_<window_id>.md` exists
- Commit complete

---

## 6. Phase 1 — Roadmap Rebalance (Optional)

**Source prompt:** `claude/system/roadmap_prompt.md` (v9.14)
**Invoke when:** A roadmap item completes and a priority reassessment is warranted before proceeding to release planning, or on a scheduled review cadence without a completion event.

### 6.1 Invocation

```
# Completion-triggered
run roadmap --item-id "<id>" --item-name "<name>" [--date "YYYY-MM-DD"]

# Scheduled (no completion event required)
run roadmap --reason "scheduled" [--date "YYYY-MM-DD"]
```

**Completion-triggered:**
- `--item-id` required (e.g., `3.2`)
- `--item-name` must uniquely match an item in `current_roadmap.md`
- `--date` defaults to today

**Scheduled:**
- No completion event or item ID required
- STEP 1.2 (Capacity Release Registration) is skipped automatically
- `cycle_id` takes the form `YYYY-MM-DD__scheduled`

Any other input is treated as conversational — the Engine will not run.

### 6.2 Preflight Checklist

| Check | Requirement | Action if Fail |
|-------|-------------|----------------|
| Required files present | charter, lifecycle guide, strategy rules, roadmap, backlog, lessons_learnt_prompt, idea_intake_prompt, idea_template | Halt |
| Header compliance | Class 4 headers on roadmap + backlog | Apply Step 0.A header remediation (headers only) |
| Authority roles exist | All 9 required roles have agent files in `claude/agents/` | Halt |
| Write permission | `claude/cycles/` writable | Halt |
| Prior cycle outstanding actions | All actions from prior lessons_learnt resolved, or carried forward with named owner + new target date | Halt if any unresolved without carry-forward |

### 6.3 Engine Steps

| Step | Name | Gate | Output |
|------|------|------|--------|
| STEP -1 | Preflight (incl. prior cycle outstanding actions check) | **HARD** | Pass / Halt |
| STEP 0 | Load & Validate Inputs | **HARD** | Validated inputs; `cycle_id` defined |
| STEP 1 | Run Manifest & Capacity Release | — | `run_manifest.md` (capacity skipped for scheduled runs) |
| STEP 2 | Roadmap Re-Validation (incl. Strategy Proximity Scores + CPS) | — | `cycle_record.md` §STEP 2 section |
| STEP 3 | Backlog Health Review | — | `cycle_record.md` §STEP 3 section |
| STEP 4 | Idea Review & Document Management (incl. stale idea expiry) | — | `cycle_record.md` §STEP 4 section |
| STEP 5 | Structured Debate (Zero-Sum) | — | `cycle_record.md` §STEP 5 section |
| STEP 6 | Scoring Matrix Overlay (incl. effort banding S/M/L) | — | `scored_initiatives.md` |
| STEP 7 | Workforce Economics Gate (incl. Skill-Silo Alert) | **HARD** | `workforce_capacity.md` |
| STEP 8 | Final Rebalance Decision | — | `cycle_record.md` §STEP 8 section |
| STEP 8.5 | Stateless Write Safety Gate | **HARD** | Verified write plan |
| STEP 8.6/8.7 | Fatigue Detection + Pivot Loop | **HARD** | Guardrail check |
| STEP 9 | Canonical Write | — | Updated roadmap, backlog, decision log, initiative register |
| STEP 10 | Publish Delta Summary | — | `cycle_summary.md` |
| STEP 11 | Lessons Learnt + Prompt Change Classification + Prompt Change Log + Meta-Review (if due) | — | `lessons_learnt.md`; `prompt_change_log.md` (if patches applied); `meta_review.md` (if due) |
| STEP 12 | Stage & Commit (incl. `last_meta_review_cycle` state update) | **HARD** | Git commit or commit manifest |

**Key constraints:**
- STEP 5: No candidate advances without naming a displacement. No name = cannot proceed. **This rule is mode-independent** — it applies in both `strict` and `standard` modes. A named displacement that does not currently exist in the roadmap is not valid — displacement must be a real in-scope initiative. The Facilitator enforces this; the Challenger may demand evidence.
- STEP 8.6: At least one candidate per run must be Parked or Rejected. If all advance, Pivot Loop runs once. If all still advance, execution halts.
- STEP 9 write scope is restricted — no files outside the allowed list may be modified.
- STEP 11: Every friction item patch must be classified as action-now or defer. Action-now patches require Head of Specs Team sign-off and produce a `prompt_change_log.md` entry. Deferred patches without a named owner and target date are escalations, not valid outstanding actions.

### 6.4 Phase 1 Exit Criteria

- `current_roadmap.md` updated and lifecycle-compliant
- `backlog.md` reconciled (Add / Replace / Defer / Kill reflected)
- All decisions in `decision_log.md` (append-only)
- Stopped work explicitly named
- Workforce implications documented
- `lessons_learnt.md` filed with all friction items classified (Type A–E), blast radius recorded, and patches classified as action-now or deferred
- All action-now patches applied, version-incremented, and recorded in `claude/system/prompt_change_log.md`
- All deferred patches have a named owner (role) and target date — or are recorded as escalations
- Meta-review conducted and `meta_review.md` filed if due (every third cycle)
- STEP 12 commit complete

---

## 6M. Phase 1M — Document Management (Optional)

**Source prompts:** `claude/system/roadmap_management_prompt.md` (v1.4), `claude/system/backlog_management_prompt.md` (v1.13), `claude/system/ideas_housekeeping_prompt.md` (v1.2)  
**Owner:** PMO Lead / Product Owner  
**Trigger:** Optional — strongly recommended at either of the following windows:

| Window | Rationale |
|--------|-----------|
| After Post-Ship Closure is confirmed | Ensures planning documents reflect shipped state before any new cycle opens |
| Immediately before `run roadmap` | Gives the Roadmap Rebalance Engine clean, accurate inputs |

Both windows are equally valid. Either may be used independently. The two engines may also be run independently of each other.

**Known gap:** If Phase 1 is skipped and `plan release` is invoked directly, neither engine will have run since the last Post-Ship Closure. In this case, both should be run before `plan release` is issued. This is not yet a formal trigger — teams skipping Phase 1 regularly should raise this for promotion to a full trigger window.

Two independent engines that manage the lifecycle of the two primary planning documents. Neither makes product decisions — they enforce document hygiene only.

### 6M.1 Roadmap Management Engine (`manage roadmap`)

Keeps `claude/roadmap/current_roadmap.md` clean and readable.

| What it does | What it does NOT do |
|-------------|-------------------|
| Retires ✅ Complete and ❌ Killed items to `claude/roadmap/roadmap_archive.md` | Change priorities or scope |
| Flags stale Planned items with no cycle activity | Make product decisions |
| Updates the release summary table | Touch the backlog |
| Produces a run log | Retire items without evidence |

**Ambiguous items** (complete but no verification reference) require explicit Product Owner confirmation before retirement.

**Hard rules:**
- Archive is append-only — retired items are permanent records
- Stale items are flagged, not decided — only the Roadmap Rebalance Engine may park or kill them
- `--dry-run` is always safe — produces change plan without writing

### 6M.2 Backlog Management Engine (`groom backlog`)

Keeps `claude/backlog/backlog.md` healthy and aligned with the roadmap.

| What it does | What it does NOT do |
|-------------|-------------------|
| Archives ✅ Complete and ❌ Killed items to `claude/backlog/backlog_archive.md` | Change priorities |
| Flags orphaned items (no roadmap home, no cycle activity) | Add items to the roadmap |
| Flags blocked items with stale blockers (not updated in 2+ cycles) | Touch the roadmap document |
| Validates spec debt items (BLG-SPEC-*) against spec update status | Make promotion decisions |
| Produces a promotion shortlist for Product Owner consideration | Change item definitions |

**Note on promotion shortlist:** The shortlist is advisory only. No items are added to the roadmap by this engine. The Product Owner decides which candidates (if any) to advance, and the Roadmap Rebalance Engine executes any additions.

**Lock conflict:** `groom backlog` acquires `claude/backlog/.lock` during its run. If this lock is held by an active Phase 1B cycle, the engine will halt at preflight. Do not clear a live lock — wait for the owning cycle to release it, or confirm with the PMO Lead that the owning cycle is inactive before following the stale lock protocol.

**Hard rules:**
- Lock must be acquired before any write (`claude/backlog/.lock`) and released after commit
- Archive is append-only
- Promotion shortlist is advisory — Roadmap Rebalance Engine executes promotions
- `--dry-run` is always safe

### 6M.3 Ideas Housekeeping Engine (`run ideas housekeeping`)

Keeps `claude/ideas/ideas_register.md` lean and surfaces revival opportunities.

| What it does | What it does NOT do |
|-------------|-------------------|
| Archives terminal rows (`Promoted-Added`, `Promoted-Rejected`, closed `Rejected`) to `ideas_register_archive.md` | Change any idea's content or scope |
| Reviews `rejected_but_strong.md` revival conditions against the just-closed cycle | Promote ideas to the backlog or roadmap |
| Checks ideas pipeline health (near-empty backlog advisory) | Modify `rejected_but_strong.md` |
| Returns advisory block to calling engine | Commit — calling engine owns the commit |

**Invocation:** Mandatory as post_ship_closure.md STEP 12.5. Advisory pre-clean at roadmap_prompt.md STEP 4 if not already run at post-ship. Standalone `run ideas housekeeping [--dry-run]` supported.

**Hard rules:**
- Cross-reference `rejected_but_strong.md` before archiving any `Rejected` row — a match means keep, not archive
- Archive is append-only — archived entries are permanent records
- `--dry-run` is always safe
- When invoked as subroutine, calling engine owns the commit

### 6M.4 Phase 1M Exit Criteria

- `roadmap_archive.md` updated (if any items retired)
- `backlog_archive.md` updated (if any items archived)
- `ideas_register.md` terminal rows archived (if any identified)
- Stale items flagged in `current_roadmap.md` (if any identified)
- Orphans and stale blockers flagged in `backlog.md` (if any identified)
- Manage roadmap run log written (`claude/roadmap/manage_roadmap_log_<YYYYMMDD>.md`)
- Backlog health report written (`claude/backlog/backlog_health_<YYYYMMDD>.md`)
- Rejected-but-strong revival advisory produced (or "no action required" recorded)
- No ambiguous items left unresolved
- Backlog lock released
- Commits complete for all engines

---

## 6.5 Phase 1.5 — Design Gate (Required*)

**Source prompt:** `claude/system/design_gate_prompt.md` (v1.9)  
**Owner:** Head of UX & Design (artefacts), PMO Lead (gate record)  
**Pre-condition:** Phase 1B Publish Gate passed; `sprint_sealed = false`  
**\*Required** unless all sprint items are confirmed Design Not Applicable

The Design Gate runs between Release Planning and Sprint Planning. It classifies every sprint item by design requirement, routes items needing design through a structured review, and produces a gate record that Sprint Planning uses as a pre-condition.

### 6.5.1 Classification

| Classification | Meaning |
|----------------|---------|
| Design Required | User-facing UI change — new component, modified layout, new page, changed flow |
| Design Pre-Approved | Frontend spec already locked from prior cycle; no UI change |
| Design Not Applicable | Purely technical — CI/CD, database, logging, observability |

**Default:** When in doubt, classify as Design Required. Head of UX & Design may downgrade with explicit confirmation.

### 6.5.2 Gate Flow

1. PMO Lead invokes `run design-gate --cycle "<cycle_id>"`
2. Facilitator classifies all sprint items (Head of UX & Design confirms)
3. For Design Required items: Head of UX & Design produces artefacts; Product Owner approves
4. Frontend Specs & UX Documentation Owner updates frontend specs
5. Head of Specs Team confirms spec lifecycle compliance
6. Gate record written; global state updated (`design_gate_status = Passed` written to the cycle-level `state.json` by the Design Gate Engine; reserved as a read-only field by the Release Planning Engine, which initialises it to `not_started` at STEP 0). The same three values (`design_gate_status`, `design_gate_record`, `design_gate_completed_utc`) are additively mirrored into `.claude_current_state.json` (BLG-GOV-190); when `Passed`, the root pointer's `status` is also advanced to `Design_Gate_Passed`, per the transition `lifecycle_schema.json` defines for this engine.

**Gate passes only when:** all Design Required items have approved artefacts AND updated frontend specs.

### 6.5.3 Sprint Planning Pre-Condition

`plan sprint` may not be issued until `design_gate_status = Passed` in `state.json`. Once passed, the root pointer's `status` also reads `Design_Gate_Passed`, so `sprint_planning_prompt.md`'s STEP -1.3 bypass audit only fires when entry is genuinely from `Release_Planning_Complete` — i.e., the gate was not run, or not yet passed.

If the gate is bypassed (Sprint Planning run without a passing design gate), this is a **process deviation** — must be recorded in escalations and lessons learnt.

### 6.5.4 Phase 1.5 Artefacts

| Artefact | Location | Owner |
|----------|----------|-------|
| Design Gate Record | `claude/cycles/<id>/design_gate.md` | PMO Lead |
| Design Artefacts | `docs/design/<cycle_id>/<item-slug>/` | Head of UX & Design |
| Updated Frontend Specs | `docs/specs/frontend/pages/*.md` | Frontend Specs & UX Owner |

### 6.5.5 Phase 1.5 Exit Criteria

- All items classified
- All Design Required items: artefacts approved + frontend specs updated
- `design_gate_status = Passed` in `state.json`
- Gate record committed

---

## 6B. Phase 1B — Release Planning

**Source prompt:** `claude/system/release_planning_prompt.md` (v2.49)
**Purpose:** Translate an already-approved roadmap release into an execution-ready plan: sequencing, dependencies, acceptance gates, backlog slice, optional GitHub issues.

> **This routine does NOT rebalance the roadmap.** It may not add, replace, defer, or kill initiatives. Those remain reserved for Phase 1.

> **Amendment Cycle:** If an emergency is discovered after this phase publishes and before Phase 2 seals, use `amend cycle` — see §6B.8. Amendment cycles are emergency-only; delivery pressure never qualifies.

### 6B.1 Invocation

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

### 6B.2 State Machine

All progress is recorded in `claude/cycles/<cycle_id>/state.json`. The routine is resumable from the last completed step.

| Macro-State | Meaning |
|-------------|---------|
| `Initialized` | Run manifest + state created |
| `Planning` | Stage 3 (Execution Plan) exists and Stage 3.5 (Model Integrity) passed |
| `Committed` | Stage 4 (Backlog Slice) passed and committed to `backlog.md` |
| `Validated` | All gates passed; Publish Gate eligible |
| `Published` | Sealed; immutable; cycle summary + lessons filed |
| `Blocked` | One or more open escalations; Publish Gate cannot pass |

**Terminal state rule:** Once `Published`, the cycle folder is sealed. No step may re-run, no artefact may be modified, no escalation may be appended. Any post-publish backlog change requires an **Amendment Cycle** (`amend cycle --cycle "<cycle_id>" --reason "emergency-fix|hard-blocker"`). Amendment cycles are emergency-only and require two-authority ratification.

### 6B.3 Engine Steps

| Step | Name | Gate | Output |
|------|------|------|--------|
| STEP -1 | Preflight | **HARD** | Pass / Halt |
| STEP 0 | Run Manifest + Initialize State | **HARD** | `run_manifest.md`, `state.json` |
| STEP 1 | Release Readiness Validation | — | `release_plan.md` §Readiness |
| STEP 2 | Scope Extraction | — | `release_plan.md` §Scope (S2-xx IDs required); `docs/product/scope/scope--{cycle_id}-{slug}.md` created |
| STEP 3 | Execution Plan | — | `release_plan.md` §Execution Plan (EPIC-xx + Maps to + RISK-xx required); `docs/product/decisions/decisions--{cycle_id}.md` created |
| STEP 3.5 | Local Model Integrity Check | Conditional | `release_plan.md` §Integrity Validation — 3.5 |
| STEP 3.9 | Shared Write Lock Preflight | **HARD** | Backlog lock acquired |
| STEP 4 | Backlog Slice | **HARD** | `stage4_backlog_slice.md` + backlog updated |
| STEP 4.5 | Capacity Feasibility Sense Check | Conditional | `release_plan.md` §Capacity Check |
| STEP 5 | Roadmap Annotation | — | Roadmap execution notes updated |
| STEP 5.5 | Cross-Stage Integrity Validation | **HARD** | `release_plan.md` §Integrity Validation — 5.5 |
| STEP 5.7 | Decision Record Integrity Validation | **HARD** | `release_plan.md` §Integrity Validation — 5.7 (only if triggered) |
| STEP 7 | Cycle Summary + Intermediate State Sync | — | `cycle_summary.md`; `.claude_current_state.json` intermediate sync (must NOT set status = Published) |
| STEP 7.1 | Intermediate Global State Sync | **HARD** | `.claude_current_state.json` updated: `active_cycle`, `status` = current macro-state, `backlog_slice_path`, `last_sync_utc` — status must NOT be `Published` at this step |
| STEP 8 | Lessons Learnt | — | `lessons_learnt.md` |
| STEP 9 | Terminal Global State Synchronization | **HARD** | `.claude_current_state.json` terminal update — the only step that may set `status = Published`; verifies STEP 7.1 ran first |
| STEP 10 | Stage, Commit & Push | — | Git commit (includes scope document and decisions record); issues if `--issues gh` |

### 6B.4 Identifier Standards

All artefacts use stable IDs — missing IDs are a Process Integrity failure that halts execution.

| Type | Format | Required on |
|------|--------|-------------|
| Scope items | `S2-01`, `S2-02`, … | Stage 2 |
| Epics | `EPIC-01`, `EPIC-02`, … | Stage 3 |
| Stories / tasks | `ST-01`, `TASK-01`, … | Stage 3 (recommended) |
| Risks | `RISK-01`, `RISK-02`, … | Stage 3 |
| Escalations | `ESC-YYYYMMDD-nn` | Escalations file |

Every Stage 3 epic must declare `Maps to: S2-xx`. Every Stage 4 backlog slice must reference EPIC IDs exactly (no free-text epics).

### 6B.5 Backlog Concurrency Control

Only one governed cycle may modify `claude/backlog/backlog.md` at a time.

- Lock file: `claude/backlog/.lock` (created at STEP 3.9, released after STEP 4 commits)
- If the lock exists and is owned by a different `cycle_id`: **halt** — no auto-delete, no override
- Stale locks: PMO Lead must manually release under the stale protocol (timestamp threshold + evidence of inactive owning cycle); removal recorded in the current cycle's escalation record

### 6B.6 Publish Gate

The cycle may only be sealed `Published` if **all** of the following are true:

- `open_escalations` is empty
- Every deferred escalation has `Blocks execution: No`
- `deferred_execution_blockers` is empty
- `stage4_5_capacity_check` is `pass` or `warn` (`warn` allowed in `standard` mode only)
- `stage5_5_cross_stage_integrity` is `pass`
- `stage5_7_decision_record_integrity` is `pass` or `not_applicable`
- `stage1_readiness` and `stage3_5_model_integrity` are `pass`
- `plan_structured = true`, `plan_executable = true`, `backlog_committed = true`
- All locks are `released` or `not_checked` (none `acquired` or `prepared`)
- STEP 7.1 intermediate sync is confirmed complete (`last_sync_utc` is set)

### 6B.7 Phase 1B Exit Criteria

- `state.json` status = `Published`, `publish_eligible = true`
- `stage4_backlog_slice.md` committed to `backlog.md` with idempotency marker
- `docs/product/scope/scope--{cycle_id}-{slug}.md` exists and is committed
- `docs/product/decisions/decisions--{cycle_id}.md` exists and is committed
- `.claude_current_state.json` updated (STEP 7.1 intermediate sync + STEP 9 terminal sync both confirmed)
- `deferred_execution_blockers` is empty
- `cycle_summary.md` and `lessons_learnt.md` filed
- No open escalations
- Backlog lock released

### 6B.8 Amendment Cycle (Emergency Only)

**Source prompt:** `claude/system/amendment_cycle_prompt.md` (v1.9)

An amendment cycle may be opened after Phase 1B publishes and before Phase 2 seals (`sprint_sealed = true`). It is the only permitted mechanism for changing the backlog slice after the release plan is sealed.

```
amend cycle --cycle "<original_cycle_id>" --reason "<emergency-fix|hard-blocker>" [--mode "strict|standard"]
```

| Reason | Meaning | Ratifying Authorities |
|--------|---------|----------------------|
| `emergency-fix` | Security patch, regulatory requirement, or critical production issue that must enter this sprint | Product Owner + Director of Quality |
| `hard-blocker` | A planned item is confirmed undeliverable and must be replaced or removed | Product Owner + Head of Specs Team |

**Key constraints:**
- Backlog slice changes only — no AC edits, no EPIC restructuring, no capacity changes
- Original sealed cycle artefacts are never modified
- Amendment artefacts live in `claude/cycles/<original_cycle_id>/amendments/<AMD-id>/`
- Once sealed, `amended_backlog_slice_path` in `.claude_current_state.json` is the source of truth for Phase 2; this field is written by the Amendment Cycle Engine and read directly by Sprint Planning — the original `backlog_slice_path` is superseded for this cycle
- One active amendment at a time — seal or withdraw before opening another
- Delivery pressure never qualifies as an emergency

---

## 7. Phase 2 — Sprint Planning

**Source prompt:** `claude/system/sprint_planning_prompt.md` (v3.16)
**Owner:** PMO Lead  
**Trigger:** Phase 1B complete — `.claude_current_state.json` status = `Published` (or `Validated` / `Committed`)

Phase 2 converts the release-planned backlog slice into a time-boxed, executable sprint. It may only begin after Phase 1B exit criteria are satisfied and `state.json` status is `Published`.

### 7.1 Invocation

```
plan sprint [--cycle "<cycle_id>"] [--mode "strict|standard"] [--dry-run]
```

| Flag | Notes |
|------|-------|
| `--cycle` | Optional — loaded from `.claude_current_state.json` if omitted |
| `--mode` | `strict`: halt on any missing AC, unclear owner, or unresolved dependency; `standard` (default): flag and proceed |
| `--dry-run` | Preview only — no writes or state updates |

**Pre-condition:** `.claude_current_state.json` status must be `Published`, `Validated`, or `Committed`. `stage4_backlog_slice.md` must exist and `state.json` must be `Published`.

### 7.2 Planning Steps

| Step | Name | Key Output | Hard Gate? |
|------|------|-----------|-----------|
| -1 | Preflight | — | Yes — halts on any missing input or unsealed release plan |
| 0 | Load release context | Load summary | No |
| 1 | Capacity baseline | `sprint_capacity.md` | Yes — halts if estimates missing in strict mode |
| 2 | Sprint goal definition | `sprint_goal.md` | Yes — no planning proceeds without confirmed goal |
| 3 | Scope selection | Include/defer classification | Yes — over-allocation must be resolved or explicitly accepted |
| 4 | Acceptance criteria confirmation | AC confirmed per ST item | Yes — no AC-less items may be sealed |
| 5 | Dependency mapping and sequencing | `sprint_planning_notes.md` | Yes — circular dependencies halt |
| 6 | Sprint backlog production and sign-off | `sprint_backlog.md` (Sealed) | Yes — Product Owner sign-off required |
| 7 | Global state update | `.claude_current_state.json` | Hard requirement |
| 8 | Commit | — | Only if sprint_sealed = true |

### 7.3 Acceptance Criteria Standard

Every item entering the sprint must have all four dimensions confirmed:

| Dimension | Requirement |
|-----------|-------------|
| Technical | Observable behaviour — what must be built or changed |
| Quality | Specific test scenario — not just "tested" |
| Security | Explicit check or explicit N/A with justification |
| Verification | How the Director of Quality will confirm done |

Items without confirmed acceptance criteria may not enter the sprint. In `standard` mode they receive an `[AC REQUIRED]` placeholder that must be resolved before the backlog can be sealed.

### 7.4 Capacity and Scope Rules

- Sprint scope must not exceed confirmed available capacity
- Deferred items remain in `backlog.md` unchanged — sprint planning does not modify the backlog
- Over-allocation requires explicit Product Owner acceptance with a recorded rationale (`standard` mode only)
- Delegation class (`autonomous`, `delegated_backend`, `delegated_frontend`, `delegated_qa`, `delegated_decision`) is set per ST item at planning time so Phase 3 can load and act without re-classifying

### 7.5 Sprint Planning Artefacts

| Artefact | Location | Owner | Required? |
|----------|----------|-------|-----------|
| Sprint goal | `claude/cycles/<id>/sprint_goal.md` | Product Owner | Yes — hard gate |
| Sprint backlog (sealed) | `claude/cycles/<id>/sprint_backlog.md` | PMO Lead | Yes — hard gate |
| Sprint capacity | `claude/cycles/<id>/sprint_capacity.md` | PMO Lead | Yes |
| Sprint planning notes | `claude/cycles/<id>/sprint_planning_notes.md` | PMO Lead | Yes |
| Sprint escalations | `claude/cycles/<id>/sprint_escalations.md` | PMO Lead | If raised |

### 7.6 Phase 2 Exit Criteria

- `sprint_goal.md` exists with confirmed Product Owner sign-off
- `sprint_backlog.md` status = `Sealed` with Product Owner sign-off recorded
- All in-scope items have confirmed acceptance criteria (no `[AC REQUIRED]` placeholders)
- All in-scope items have effort estimates (no `[ESTIMATE REQUIRED]` placeholders)
- Capacity confirmed — no unresolved over-allocation
- Dependency map and execution sequence documented
- Delegation class recorded per ST item
- `.claude_current_state.json` status = `Sprint_Planning_Complete`, `sprint_sealed = true`

### 7.7 Escalation

Planning blockers that cannot be resolved by the PMO Lead are recorded in `sprint_escalations.md` (format: `ESC-PLAN-YYYYMMDD-nn`). The engine sets status to `Sprint_Planning_Blocked` and halts. Re-invoke `plan sprint` once resolved — the engine resumes from the first incomplete step.

### 7.8 Staging-Only AC Categories Reference (BLG-GOV-42 / ST-04 v4.3)

Use this table when designating `**Staging-only ACs:**` in sprint_backlog.md story entries. An AC is staging-only when it requires evidence that CI cannot reproduce.

| Category | Pattern | Example from history |
|----------|---------|----------------------|
| Live external API call | AC requires a real API response from Alpaca, Claude/Anthropic, Yahoo Finance, or any external service not mocked in CI | BLG-QA-29 (v4.0): Claude thesis generation — ANTHROPIC_API_KEY required on staging; CI has no live key |
| Staging-specific environment variables | AC requires env vars present on staging/prod but absent from CI (e.g. ANTHROPIC_API_KEY, Alpaca keys, TELEGRAM_BOT_TOKEN) | BLG-QA-35 (v4.1): Daily cost threshold alert — live TELEGRAM_BOT_TOKEN required for alert to fire |
| Non-mocked database state or live DB query | AC requires specific rows in staging DB (audit log entries, live trade data) that CI fixtures do not provide | BLG-QA-35 (v4.1): claude_audit_log rows required in staging for threshold check |
| Live network validation | AC requires internet access to validate external data (e.g. Yahoo Finance symbol validation) | BLG-QA-30 (v4.0): Ticker validation — SKIP_TICKER_VALIDATION must be unset and live Yahoo Finance must reject invalid ticker |
| Observable UI rendering without feasible Playwright mock | AC verifies UI rendering or interaction where `page.route()` mocking is not feasible for the required assertion | BLG-QA-24 (v3.7): Specific observable UI elements requiring staging browser run — note: if Playwright mocking IS feasible, this is NOT staging-only (confirmed at v4.3 sprint planning for BLG-QA-28 Arc5ComplianceSection) |

**Designation rule:** At sprint planning, sprint planners must inspect each story's acceptance criteria against this table. Any AC matching a category above must be tagged in the `**Staging-only ACs:**` field of the sprint_backlog.md story entry. `None` is only valid when no AC requires staging. A missing staging-only designation is a seal blocker (sprint_planning_prompt.md STEP 6.2 sign-off gate).

### 7.9 Staging URL Disambiguation (BLG-OPS-43)

The project uses **two separate Render services**: a frontend SPA and a backend API. These run as distinct deployments with different base URLs. Health checks, API calls, and QA test targets must always use the **backend API URL** — not the frontend SPA URL.

| Service | URL Pattern | Purpose |
|---------|-------------|---------|
| Frontend SPA | `https://trading-assistant-frontend.onrender.com` | Serves the React single-page application. Does NOT expose `/api/*` routes directly. |
| Backend API | `https://trading-assistant-api.onrender.com` | FastAPI service. Exposes all `/api/*` endpoints, `/healthz`, and `/metrics`. |

**Health check baseline:** Always target the backend API URL. For example:

```
# Correct — backend API health check
curl https://trading-assistant-api.onrender.com/api/healthz

# Incorrect — frontend SPA (will return HTML, not JSON)
curl https://trading-assistant-frontend.onrender.com/api/healthz
```

**QA test and staging verification:** Director of Quality should confirm which URL is being tested. Playwright tests and manual QA runs that exercise API-backed behaviour must target the backend API URL. Rendering-only checks that navigate the React app target the frontend SPA URL.

**Root cause (BLG-OPS-43):** v4.3 Phase 3 staging friction occurred when health check commands were run against the frontend SPA URL, returning HTML instead of the expected JSON health response. This subsection disambiguates the two service types to prevent recurrence.

---

## 8. Phase 3 — Sprint Execution & Close

**Source prompt:** `claude/system/execution_prompt.md` (v3.66)

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

**Pre-condition:** `.claude_current_state.json` status must be `Sprint_Planning_Complete` and `sprint_sealed = true`. If `Blocked`: resolve escalations first.

### 8.2 Execution Principles

- Scope is frozen at sprint start. New items require explicit Product Owner approval and a recorded decision.
- Blockers escalated same-day via escalation record (`ESC-EXEC-YYYYMMDD-nn`).
- Director of Quality QA gates apply to all EPICs before merge.
- **QA sign-off environment (v1.10+):** Director of Quality must review and test against the staging environment at `https://trading-assistant-staging.onrender.com` — not production. Staging is the canonical pre-merge QA environment as of v1.10 (LL-01 resolution, 2026-03-16).
- **Staging test data prerequisite for data-dependent scenarios (LL-v1.10-P4-3):** Before executing QA scenarios that require backend data records (e.g. scenarios involving closed trades, open positions, or portfolio history), confirm the staging database has at least one closed trade and at least one open position. If the staging DB lacks qualifying data, the scenario result is BLOCKED (not FAIL) — record the data gap as a friction item in the `qa_evidence_EPIC-xx.md` sign-off block.
- **Staging test data seeding — chart interactivity scenarios (ST-11+):** For scenarios requiring specific closed-trade data (e.g. `SC-CHART-IX-*`), run the **Seed Staging Database** workflow via GitHub Actions → Actions → `Seed Staging Database` → Run workflow. This executes `backend/test_data/seed_chart_test_data.sql` directly against the staging Supabase database via `psql`, inserting 12 closed trades (Jan×4 / Feb×6 / Mar×2, all 7 R-multiple buckets). An idempotency guard skips the run if `[SEED]` records already exist — safe to trigger multiple times. Prerequisite: `STAGING_DATABASE_URL` repository secret must be set (Supabase staging project → Settings → Database → Connection string → URI). DoQ runs scenarios against `https://trading-assistant-staging.onrender.com` after seeding. Note: PR preview environments are not used for data-dependent QA — the canonical staging environment is always the test target (LL-01, 2026-03-16; updated approach 2026-03-19).
- **PR preview environments (v2.1+, ST-15):** For EPICs with frontend changes, Render provisions a preview environment at `https://trading-assistant-api-staging-pr-{N}.onrender.com` (where `{N}` is the PR number). Preview environments use **manual mode** — they are only created when the PR has the `render-preview` label applied. When raising a PR for an EPIC with frontend changes, add the `render-preview` label so the preview environment is provisioned. Director of Quality may use the preview URL as the staging evidence method for frontend-interactive AC (hover behaviour, animations, zoom/pan, modal interactions) before merge.
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
| Lessons learnt | `claude/cycles/<id>/lessons_learnt_cycle.md` | Phase 3 section append — execution friction and improvement actions |

### 8.5 Merge Gate (Per EPIC — Hard Gate)

A PR may only be merged when all of the following are true:

- All ST items in EPIC: `done`
- `spec_references` populated for all `done` items
- `qa_evidence_EPIC-xx.md` exists and sign-off block complete (Director of Quality — review conducted against staging: `https://trading-assistant-staging.onrender.com` or PR preview URL `https://trading-assistant-api-staging-pr-{N}.onrender.com` for frontend-interactive AC)
- QA sign-off comment on PR from Director of Quality (must reference staging sign-off)
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
- `lessons_learnt_cycle.md` Phase 3 section appended (idempotency guard applied)
- `execution_state.json` sealed
- `.claude_current_state.json` status = `Sprint_Complete`
- STEP 8 commit complete

---

## 9. Phase 4 — Delivery Verification

**Source prompt:** `claude/system/delivery_verification_prompt.md` (v3.7)

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

**Source prompt:** `claude/system/post_ship_closure.md` (v2.26)
**Process document:** `docs/team_skills/pmo/processess/post-ship_closure.md` (v2.0)
**Owner:** PMO Lead
**Trigger:** Phase 4 complete — `.claude_current_state.json` status = `Verified` or `Verified_with_deviations`

Post-Ship Closure is the mandatory bridge between a verified sprint and a clean next cycle. It ensures all planning, operational, and governance documents reflect the shipped state before the next Phase 1 or Phase 1B is invoked.

> `next_cycle_unblocked = true` is a necessary but not sufficient condition for opening the next cycle. Post-Ship Closure must also be complete.

**Audit cadence:** `run audit` is due every 3 completed cycles. Post-Ship Closure STEP 0 surfaces an advisory when `completed_cycle_count % 3 == 0`. The audit is non-blocking but must complete before the next Phase 1B `plan release` invocation when the advisory fires.

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
- `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (Phase 3 + Phase 4 + Amendments — consolidated file)
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
| 9 | Lessons learnt (`lessons_learnt.md` + `lessons_learnt_cycle.md`) | Review all action items from both files; apply immediate process improvements (bump template/prompt versions); schedule deferred actions; escalate decisions to named owners | Lessons learnt filed but not reviewed — process debt compounds |

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

This release produces two lessons learnt files that must both be reviewed:

| Record | Location | Covers |
|--------|----------|--------|
| Release Planning lessons | `claude/cycles/<cycle_id>/lessons_learnt.md` | Phase 1B planning friction, escalation patterns, backlog quality |
| Sprint Execution + Verification + Amendment lessons | `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` | Phase 3 (delegation, GitHub integration, acceptance criteria gaps, gate friction), Phase 4 (gate sequencing, deviation severity patterns, test coverage gaps, sign-off coordination), Amendment sections if any |

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
| Scheduled review due | Phase 1 (`run roadmap --reason "scheduled"`) | Product Owner |
| Phase 1 exit criteria met | Phase 1B — Release Planning Engine | PMO Lead |
| **Before `run roadmap` is issued** | **Phase 1M: `manage roadmap` + `groom backlog` (optional — strongly recommended)** | **PMO Lead / Product Owner** |
| Phase 1B Publish Gate passed | Phase 1.5: Design Gate (`run design-gate`) | PMO Lead |
| Phase 2 complete (`Sprint_Planning_Complete`) | Phase 3 — Sprint Execution (`run sprint`) | PMO Lead |
| Phase 3 active (`Executing`) | Phase 3 resuming — re-invoke `run sprint --cycle <cycle_id>` after each EPIC merge | PMO Lead |
| Phase 3 complete (`Sprint_Complete`) | Phase 4 — Delivery Verification | PMO Lead |
| Phase 4 complete (`Verified`) | Post-Ship Closure | PMO Lead |
| Post-Ship Closure confirmed | Phase 1M: `manage roadmap` + `groom backlog` (optional — strongly recommended) | PMO Lead / Product Owner |
| Phase 1M complete (or skipped) | New Phase 1 (optional) or Phase 1B cycle | Product Owner |
| Phase 1B Publish Gate passed | Phase 1.5: Design Gate (`run design-gate`) | PMO Lead |
| Design Gate passed (`design_gate_status = Passed`) | Phase 2: Sprint Planning (`plan sprint`) | PMO Lead |
| Sprint item returned to backlog | Backlog reconciliation only (no new cycle) | Head of Specs Team |
| Emergency discovered post-publish (before Phase 2 sealed) | Amendment Cycle (`amend cycle`) | PMO Lead |
| Amendment sealed | Sprint Planning uses `amended_backlog_slice_path` | PMO Lead |
| Test scenario gap found (Phase 4) | Action written to QA & Testing Owner agent file | QA & Testing Owner |
| Third completed rebalance cycle since last meta-review | Meta-review triggered within STEP 11 | PMO Lead |

> **Loop rule:** Phase 1 is only triggered when a roadmap item completes and a rebalance is warranted, or when a scheduled review is due. Sprint items that are backlog items (not roadmap items) never trigger a rebalance.

> **Cycle gate:** Phase 1B (new cycle) may not open until Phase 4 of the previous cycle reaches `Verified` or `Verified_with_deviations` **and** Post-Ship Closure is confirmed complete.

> **Phase 1M enforcement:** `manage roadmap`, `groom backlog`, and `run ideas housekeeping` are invoked as mandatory STEPs 11, 12, and 12.5 of every Post-Ship Closure run. All three run at every cycle close regardless of whether Phase 1 was executed. Standalone invocation remains supported for teams that want an additional pre-roadmap clean-up pass.

---

## 13. Artefact Register

All artefacts must be lifecycle-compliant per `claude/charter/document_lifecycle_guide.md`.

| Artefact | Location | Class | Owner | Phase |
|----------|----------|-------|-------|-------|
| Team Charter | `claude/charter/team_charter.md` | 1 | Head of Specs Team | Governance |
| Document Lifecycle Guide | `claude/charter/document_lifecycle_guide.md` | 1 | Head of Specs Team | Governance |
| Strategy Rules | `claude/strategy/strategy_rules.md` | 1 | Strategy Rules Owner | Governance |
| Roadmap Rebalance Prompt | `claude/system/roadmap_prompt.md` | 6 (v9.10) | Head of Specs Team | Governance |
| Release Planning Prompt | `claude/system/release_planning_prompt.md` | 6 | Head of Specs Team | Governance |
| Idea Intake Engine | `claude/system/idea_intake_prompt.md` | 6 (v2.8) | Head of Specs Team | Governance |
| Idea Template | `claude/system/idea_template.md` | 6 | Head of Specs Team | Governance |
| Amendment Cycle Prompt | `claude/system/amendment_cycle_prompt.md` | 6 | Head of Specs Team | Governance |
| Delivery Verification Prompt | `claude/system/delivery_verification_prompt.md` | 6 | Head of Specs Team | Governance |
| Shared Standards | `claude/system/shared_standards.md` | 6 | Head of Specs Team | Governance |
| Governance Invariants | `claude/system/invariants.md` | 6 | Head of Specs Team | Governance |
| Shared Governance Modules | `claude/system/shared/*.md` | 6 (sub-type) | Head of Specs Team | Governance |
| Governance Changelogs | `claude/system/changelogs/*.md` | 6 (sub-type) | Head of Specs Team | Governance |
| Lessons Learnt Prompt | `claude/system/lessons_learnt_prompt.md` | 6 | Head of Specs Team | Governance |
| Sprint Planning Prompt | `claude/system/sprint_planning_prompt.md` | 6 | Head of Specs Team | Governance |
| Sprint Execution Prompt | `claude/system/execution_prompt.md` | 6 | Head of Specs Team | Governance |
| Post-Ship Closure Prompt | `claude/system/post_ship_closure.md` | 6 | Head of Specs Team | Governance |
| Design Gate Prompt | `claude/system/design_gate_prompt.md` | 6 | Head of Specs Team | Governance |
| Roadmap Management Prompt | `claude/system/roadmap_management_prompt.md` | 6 | Head of Specs Team | Governance |
| Backlog Management Prompt | `claude/system/backlog_management_prompt.md` | 6 | Head of Specs Team | Governance |
| Ideas Housekeeping Prompt | `claude/system/ideas_housekeeping_prompt.md` | 6 | PMO Lead | Governance |
| Prompt Change Log | `claude/system/prompt_change_log.md` | 6 | Head of Specs Team | Governance |
| Current Roadmap | `claude/roadmap/current_roadmap.md` | 4 | Product Owner | 1 |
| Backlog | `claude/backlog/backlog.md` | 4 | Product Owner | 1, 1B, 4, Post-Ship |
| Initiative Register | `claude/roadmap/initiative_register.md` | 4 | Product Owner | 1 |
| Workforce Capacity | `claude/roadmap/workforce_capacity.md` | 4 | FinOps & Resource Architect | 1 |
| Decision Log | `claude/roadmap/decision_log.md` | 4 | PMO Lead | 1 |
| Velocity Metrics | `claude/cycles/velocity_metrics.md` | 4 | PMO Lead | 1, 1B |
| Ideas Window State | `claude/ideas/ideas_window.json` | — | PMO Lead | 0 |
| Ideas Register | `claude/ideas/ideas_register.md` | 4 | PMO Lead | 0 |
| Window Summary | `claude/ideas/window_summary_<IW-id>.md` | 4 | PMO Lead | 0 |
| Rejected-but-Strong Register | `claude/ideas/rejected_but_strong.md` | 4 | PMO Lead | 0, 1 |
| Roadmap Archive | `claude/roadmap/roadmap_archive.md` | 4 | Product Owner | 1M |
| Roadmap Management Log | `claude/roadmap/manage_roadmap_log_<date>.md` | 4 | PMO Lead | 1M |
| Backlog Archive | `claude/backlog/backlog_archive.md` | 4 | Product Owner | 1M |
| Backlog Health Report | `claude/backlog/backlog_health_<date>.md` | 4 | PMO Lead | 1M |
| Design Gate Record | `claude/cycles/<id>/design_gate.md` | 4 | PMO Lead | 1.5 |
| Design Artefacts | `docs/design/<cycle_id>/<item-slug>/` | 4 | Head of UX & Design | 1.5 |
| Stage Outputs 1–5 | `claude/cycles/<id>/stage*.md` | 3 | PMO Lead | 1 |
| Cycle Summary (Rebalance) | `claude/cycles/<id>/cycle_summary.md` | 3 | PMO Lead | 1 |
| Lessons Learnt (Rebalance) | `claude/cycles/<id>/lessons_learnt.md` | 3 | PMO Lead | 1 |
| Meta-Review Record | `claude/cycles/<id>/meta_review.md` | 3 | PMO Lead | 1 |
| Scored Initiatives | `claude/scoring/scored_initiatives.md` | 4 | Facilitator | 1 |
| Run Manifest (Release) | `claude/cycles/<id>/run_manifest.md` | 3 | Infra & Ops Owner | 1B |
| State File | `claude/cycles/<id>/state.json` | — | PMO Lead | 1B |
| Backlog Lock | `claude/backlog/.lock` | — | PMO Lead | 1B, 1M |
| Backlog Transaction | `claude/cycles/<id>/backlog_txn.json` | — | PMO Lead | 1B |
| Release Plan (consolidated intermediate) | `claude/cycles/<id>/release_plan.md` | 4 | PMO Lead | 1B |
| Stage 4 Backlog Slice | `claude/cycles/<id>/stage4_backlog_slice.md` | 3 | PMO Lead | 1B |
| Escalations (Release) | `claude/cycles/<id>/escalations.md` | 4 | PMO Lead | 1B |
| AR / SRB Decision Records | `docs/product/decisions/AR-*.md` | 4 | Product Owner | 1B |
| Scope Document | `docs/product/scope/scope--{cycle_id}-{slug}.md` | 4 | PMO Lead | 1B, Post-Ship |
| Decisions Record | `docs/product/decisions/decisions--{cycle_id}.md` | 4 | PMO Lead | 1B, Post-Ship |
| Cycle Summary (Release) | `claude/cycles/<id>/cycle_summary.md` | 3 | PMO Lead | 1B |
| Lessons Learnt (Release) | `claude/cycles/<id>/lessons_learnt.md` | 3 | PMO Lead | 1B |
| Global State Pointer | `.claude_current_state.json` | — | PMO Lead | 1B, 2, 3, 4 |
| Sprint Goal | `claude/cycles/<id>/sprint_goal.md` | 4 | Product Owner | 2 |
| Sprint Backlog | `claude/cycles/<id>/sprint_backlog.md` | 4 | PMO Lead | 2 |
| Sprint Backlog Index | `claude/cycles/<id>/sprint_backlog_index.json` | — | PMO Lead | 2 |
| Sprint Capacity | `claude/cycles/<id>/sprint_capacity.md` | 4 | PMO Lead | 2 |
| Sprint Planning Notes | `claude/cycles/<id>/sprint_planning_notes.md` | 4 | PMO Lead | 2 |
| Sprint Escalations | `claude/cycles/<id>/sprint_escalations.md` | 4 | PMO Lead | 2 |
| Execution State | `claude/cycles/<id>/execution_state.json` | — | PMO Lead | 3 |
| QA Evidence Log | `claude/cycles/<id>/qa_evidence_EPIC-xx.md` | 4 | Director of Quality | 3 |
| Delegation Log | `claude/cycles/<id>/delegation_log.md` | 4 | PMO Lead | 3 |
| Escalations (Execution) | `claude/cycles/<id>/execution_escalations.md` | 4 | PMO Lead | 3 |
| Sprint Close Summary | `claude/cycles/<id>/sprint_close.md` | 3 | PMO Lead | 3 |
| Lessons Learnt (Cycle — Phase 3, 4, Amendment) | `claude/cycles/<id>/lessons_learnt_cycle.md` | 3 | PMO Lead | 3, 4, Amendment |
| Lessons Learnt (Closure) | `claude/cycles/<id>/lessons_learnt_closure.md` | 3 | PMO Lead | Post-Ship |
| System Status Report | `docs/System_status_report.md` | 3 | Director of Quality | 3, 4 |
| Verification Report | `claude/cycles/<id>/verification_report.md` | 3 | Director of Quality | 4 |
| Escalations (Verification) | `claude/cycles/<id>/verification_escalations.md` | 4 | PMO Lead | 4 |
| Changelog | `docs/product/changelog.md` | 3 | PMO Lead | Post-Ship |
| Post-Ship Closure Process | `docs/team_skills/pmo/processess/post-ship_closure.md` | 1 | PMO Lead | Post-Ship |
| Closure Record | `claude/cycles/<id>/closure_record.md` | 3 | PMO Lead | Post-Ship |
| Closure State | `claude/cycles/<id>/closure_state.json` | — | PMO Lead | Post-Ship |
| Escalations (Closure) | `claude/cycles/<id>/closure_escalations.md` | 4 | PMO Lead | Post-Ship |
| Audit Report | `claude/cycles/<id>/audit_report_AUD-<date>.md` | 3 | Head of Specs Team | Post-Ship |
| AI Journal Review Cadence | `docs/specs/compliance/ai_journal_review_cadence.md` | 2 | AI Compliance & Governance Officer | Governance |
| Amendment Manifest | `claude/cycles/<id>/amendments/<AMD-id>/amendment_manifest.md` | 3 | PMO Lead | Amendment |
| Amendment State | `claude/cycles/<id>/amendments/<AMD-id>/amendment_state.json` | — | PMO Lead | Amendment |
| Amendment Ratification | `claude/cycles/<id>/amendments/<AMD-id>/amendment_ratification.md` | 4 | PMO Lead | Amendment |
| Amended Backlog Slice | `claude/cycles/<id>/amendments/<AMD-id>/amended_backlog_slice.md` | 4 | PMO Lead | Amendment |
| Amendment Lessons | `claude/cycles/<id>/amendments/<AMD-id>/amendment_lessons.md` | 3 | PMO Lead | Amendment |

---

## 16. Artefact Lifecycle Model

**Added:** v3.67 (ST-17, BLG-GOV-11, v3.2)

All artefacts in this system have one of three lifecycle types. The authoritative inventory is maintained at `docs/operations/cycle_artefact_inventory.md`.

| Lifecycle Type | Definition | Examples |
|----------------|-----------|---------|
| **Point-in-time (PIT)** | Created for a specific cycle event; never modified after sealing. Closed cycles retain PIT artefacts as a historical record. | sprint_backlog.md, closure_record.md, verification_report.md, run_manifest.md |
| **Living Reference** | Must be updated when the domain they describe changes. Update obligation stated in the document's own header. Failure to update is a process deviation. | backlog.md, component_inventory.md, credential_policy.md, external_api_risk_register.md |
| **Operational State** | Machine-readable; updated programmatically by governance engines. Do not edit manually. | execution_state.json, .claude_current_state.json, closure_state.json |

**Update trigger rule for Living References:** Any PR touching a domain covered by a living reference must update that reference in the same PR, or explicitly document why the update is deferred (with a backlog item filed).

Living references introduced in v3.2: `component_inventory.md`, `design_system.md`, `credential_policy.md`, `external_api_risk_register.md`, `cycle_artefact_inventory.md`.

---

## 15. Governance Health Score

**Added:** v3.56 (ST-11, BLG-GOV-14, v2.7)
**Authority:** Head of Specs Team
**Usage:** Computed and surfaced as an advisory indicator at STEP -1.7 of each roadmap rebalance. Cannot halt or gate the routine.

The Governance Health Score is a three-component advisory indicator surfaced at each roadmap rebalance to give the team visibility into the operational health of the governance process. It is not a gate — a low score does not block the run. It is a signal that should inform the retrospective discussion and may generate backlog items.

### Components

#### Component 1 — Header Compliance %

Measures how many Class 4 and Class 5 documents have compliant headers (all required fields present and non-empty).

**Formula:**

```
Header Compliance % = (Class 4/5 docs with compliant headers / total Class 4/5 docs checked) × 100
```

**Documents checked:** All files in `claude/cycles/<active_cycle_id>/` with a `.md` extension that are Class 4 or Class 5 (planning documents, cycle records). Required fields: Owner, Class, Status, Last Updated.

**Score interpretation:**
- 100% — Fully compliant
- 80–99% — Minor gaps; surface as advisory
- <80% — Material gap; flag prominently in run manifest

#### Component 2 — Deferred Patch Indicator

Counts open deferred patches by age band, taken from the `deferred_patches` section of the current cycle's `lessons_learnt.md` (or the most recent prior cycle if the current cycle is not yet closed).

**Age bands:**

| Band | Age | Label |
|------|-----|-------|
| Green | < 1 cycle | Recent — monitor |
| Amber | 1–2 cycles | Aging — plan to apply |
| Red | > 2 cycles | OVERDUE — escalation required (B7 rule) |

**Score format:** `{Red count} Red / {Amber count} Amber / {Green count} Green`

Any Red count > 0 triggers automatic B7 escalation in STEP -1.5 (already enforced). The health score component makes the aggregate pattern visible.

#### Component 3 — Outstanding Action Count

Counts open outstanding actions across all active governance artefacts.

**Sources checked:**
- `.claude_current_state.json` key `open_escalations` (if present)
- Current execution_state.json `open_escalations` array (if in an active sprint)
- Prior cycle `lessons_learnt.md` unresolved outstanding actions section

**Score format:** `{N} open actions` (list item types: governance escalation / sprint action / lessons learnt carry-forward)

### Output Format

The health score is surfaced in the run manifest under a section titled `## Governance Health Score`:

```
## Governance Health Score (Advisory)
Source: OPERATIONAL_GUIDE.md §15 — roadmap_prompt.md v6.1 STEP -1.7

| Component | Score | Status |
|-----------|-------|--------|
| Header Compliance % | 95% (19/20 docs) | ✅ Advisory |
| Deferred Patch Indicator | 0 Red / 1 Amber / 1 Green | ⚠️ 1 aging patch |
| Outstanding Action Count | 2 open (0 escalation, 1 sprint, 1 carry-forward) | ⚠️ Review recommended |

Overall: Advisory — no gate action required. Review deferred patches and outstanding actions before close.
```

**This score is advisory only.** A low score does not halt the roadmap run. It informs the Head of Specs Team and PMO Lead of process debt that may warrant backlog items.

---

## 14. Playbook Governance

| Field | Value |
|-------|-------|
| Owner | Head of Specs Team |
| Status | Active |
| Version | 4.152 |
| Last Updated | 2026-08-10 |
| Review Cadence | After every 3 completed cycles, or on any governance gap escalation |
| Idea Intake Engine | `claude/system/idea_intake_prompt.md` v2.8 |
| Idea Template | `claude/system/idea_template.md` |
| Roadmap Management Engine | `claude/system/roadmap_management_prompt.md` v1.4 |
| Backlog Management Engine | `claude/system/backlog_management_prompt.md` v1.13 |
| Design Gate Engine | `claude/system/design_gate_prompt.md` v1.9 |
| Governance Preamble | `claude/system/shared/governance_preamble.md` v1.0 |
| Roadmap Engine Source | `claude/system/roadmap_prompt.md` v9.14 |
| Release Engine Source | `claude/system/release_planning_prompt.md` v2.49 |
| Sprint Planning Engine | `claude/system/sprint_planning_prompt.md` v3.16 |
| Amendment Cycle Engine | `claude/system/amendment_cycle_prompt.md` v1.9 |
| Execution Engine Source | `claude/system/execution_prompt.md` v3.66 |
| QA Evidence Template | `claude/system/templates/qa_evidence_template.md` v1.8 |
| Verification Engine Source | `claude/system/delivery_verification_prompt.md` v3.7 |
| Ideas Housekeeping Engine | `claude/system/ideas_housekeeping_prompt.md` v1.2 |
| Post-Ship Closure Engine | `claude/system/post_ship_closure.md` v2.26 |
| Post-Ship Closure Process | `docs/team_skills/pmo/processess/post-ship_closure.md` v2.0 |
| Shared Standards | `claude/system/shared_standards.md` v3.27 |
| Governance Invariants | `claude/system/invariants.md` v1.0 |
| Lessons Learnt Prompt | `claude/system/lessons_learnt_prompt.md` v1.10 |
| Prompt Change Log | `claude/system/prompt_change_log.md` |
| GitHub Issue Template | `claude/system/gh_issue_template.md` v1.0 |
| PR DoQ Enforcement Template | `.github/pull_request_template.md` v1.2 |
| Lifecycle Guide | `claude/charter/document_lifecycle_guide.md` v2.7 |
| Team Charter | `claude/charter/team_charter.md` v1.7 |

This playbook is subordinate to and must remain consistent with all governing documents above. In any conflict, governance documents prevail. Update this playbook to reflect the change — do not operate with a known divergence.

**Version control:** All changes require approval by the Head of Specs Team and must be version-bumped per lifecycle rules. Patch = typo/formatting. Minor = structural change. Major = scope change or authority boundary change.

**Standing rule:** whenever a prompt version is updated in the §14 governance table, the corresponding phase section source prompt header (§5–§10, §6B, §6B.8, §6M) must be updated in the same edit. A mismatch between a phase section header and §14 is a non-compliant state.

---

### Change Log

**Header-drift prevention (added v4.85, roadmap rebalance 2026-07-08__scheduled, Friction Item — 4th recurrence of this exact pattern per the 4.79/4.80/4.81 entries below):** Before bumping the top `**Version:**`/`**Last Updated:**` header fields, read the highest version number already present in this table's top row — do not increment from the header field alone, since it has drifted below the table's actual latest entry on at least 4 prior occasions.

| Version | Date | Change Summary |
| 4.153 | 2026-08-10 | **Post-ship closure `2026-08-08__release-v8.5` STEP 8, immediate lessons-learnt action — post_ship_closure.md v2.25→v2.26: STEP 7.3 hardcoded "§27" TSG reference replaced with a full-document scan.** §10 source prompt header v2.25→v2.26 (line 1062). §14 Post-Ship Closure Engine v2.25→v2.26. §14 Version 4.152→4.153/2026-08-10. Change: `Specs_Index.md`'s Test Coverage Gap register is append-only/chronologically-numbered, so a fixed section number drifts stale every cycle a new section is appended — STEP 7.3 now scans the full document for `**Status:** Open` fields on `TSG-*`-prefixed entries instead. Self-confirmed live during this same closure's own STEP 7 run (actual §27 is "Test Coverage Gaps — v5.0"; the one genuinely Open TSG entry, `TSG-v33-03`, sits at §19.3) — closes a deferred patch carried forward without a `prompt_change_log.md` entry for 2 consecutive cycles (`2026-08-07__release-v8.4` closure carry-forward #2), applied now per STEP 8's non-deferrable-immediate-action rule rather than deferred a 3rd time. Authority: Head of Specs Team (post-ship closure `2026-08-08__release-v8.5`, STEP 8 immediate-action rule). |
| 4.152 | 2026-08-10 | **Sprint execution `2026-08-08__release-v8.5` EPIC-06/ST-23 (BLG-GOV-288) — release_planning_prompt.md v2.48→v2.49: root `sprint_sealed` reset on new-cycle publish.** §6B source prompt header v2.48→v2.49 (line 623). §14 Release Engine Source v2.48→v2.49. §14 Version 4.151→4.152/2026-08-10. Change: STEP 7's intermediate `.claude_current_state.json` sync now resets `sprint_sealed: false` atomically with `active_cycle` switching to the new cycle_id — same single-write-site pattern already used for `design_gate_status`. Previously nothing reset this field between cycles, so it carried a stale `true` from the prior cycle's Sprint Planning seal (observed live at the `2026-08-07__release-v8.4` design gate). STEP 0 gains a cross-reference note (the originating backlog item named that step; the technically correct write site, matching the `design_gate_status` precedent, is STEP 7). Authority: Head of Specs Team (Sprint Execution Engine, ST-23, 2026-08-10). |
| 4.151 | 2026-08-10 | **Sprint execution `2026-08-08__release-v8.5` EPIC-06/ST-22 (BLG-FEAT-72) — roadmap_prompt.md v9.13→v9.14: STEP 2.4 gains a structured Product Value Ratio history record.** §6 source prompt header v9.13→v9.14 (line 399). §14 Roadmap Engine Source v9.13→v9.14. §14 Version 4.149→4.151/2026-08-10 (see cross-branch note below). Change: new `claude/roadmap/product_value_ratio_history.md` (backfilled DL-057 through DL-077 from `decision_log.md` prose) — STEP 2.4 now appends a structured row here every rebalance, and the sustained-Advisory-tier consecutive-readings check reads this file instead of re-deriving from `decision_log.md` prose. **Cross-branch version note:** this EPIC-06 branch was cut before `EPIC-02` (also `2026-08-08__release-v8.5`) merged to `main`; `EPIC-02`'s own governance edit (ST-04, `shared_standards.md` §20) independently claimed `4.150` for a different change on its own branch. Deliberately skipped `4.150` here and used `4.151` to avoid the identical-version-different-change collision CLAUDE.md §8 step 2a exists to catch — chosen proactively in the same session that authored both changes, rather than left for a future merge-time renumbering; confirmed correctly non-colliding at merge time below. Authority: Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-22, 2026-08-10). |
| 4.150 | 2026-08-10 | **Sprint execution `2026-08-08__release-v8.5` EPIC-02/ST-04 (BLG-SEC-15) — shared_standards.md v3.26→v3.27: new §20 Dependency Vulnerability Scan Cadence.** §14 Shared Standards v3.26→v3.27. §14 Version 4.149→4.150/2026-08-10. Change: documents the three-tier dependency vulnerability scan cadence (per-PR pip-audit-only gate, pre-sprint pip-audit-only check, and the new monthly scheduled combined pip-audit + npm audit re-scan — `.github/workflows/dependency-vuln-rescan.yml`) and its new-vs-known-baseline dedup mechanism (`docs/security/dependency_vuln_baseline.json`). **Self-caught header-drift correction in the same edit:** this document's own top `**Version:**` header had drifted to 4.147 while the table's actual latest row already read 4.149 (2 versions behind, same class of drift the v4.85 Change Log note above warns against) — corrected to 4.150 per that note's own instruction to read the table's top row, not the header field, before incrementing. Authority: Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-04, 2026-08-10). |
| 4.149 | 2026-08-08 | **Lifecycle audit AUD-2026-08-08 improvement 003 — post_ship_closure.md v2.24→v2.25: state-pointer sync rule for `open_escalations`.** §10 source prompt header v2.24→v2.25 (line 1062). §14 Post-Ship Closure Engine v2.24→v2.25. §14 Version 4.148→4.149/2026-08-08. Change: §5 Write Scope Restriction gains a mandatory rule — whenever an entry is appended to `closure_escalations.md`, the same STEP 8 write must also set `.claude_current_state.json.open_escalations.<ESC-ID>`, clearing it when the escalation resolves. Closes a gap first flagged at `AUD-2026-08-03`: `open_escalations` was checked as a gate precondition by 3 engines but never written by any of them (only the separate per-cycle `execution_state.json.open_escalations` was maintained), confirmed still open at a 2nd consecutive audit before being applied here. Authority: Head of Specs Team (lifecycle audit AUD-2026-08-08, resolved 2026-08-08). |
| 4.148 | 2026-08-08 | **Lifecycle audit AUD-2026-08-08 improvement 002 — self-header drift correction (no engine prompt content changed).** §14 Version 4.146→4.148/2026-08-08 (this document's own header field had drifted: it still read 4.146 after the 4.147 entry below was already logged, since that entry's own header-bump step was missed). Also reordered the 4.146 row (previously misfiled below the 4.145 row, breaking the table's descending-version order) to sit directly below this row. No engine source prompt or §14 table row changed by this entry — pure self-consistency correction, evidence in `audit_report_AUD-2026-08-08.md` Stage 1/Improvement 002. Authority: Head of Specs Team (lifecycle audit AUD-2026-08-08, resolved 2026-08-08). |
| 4.147 | 2026-08-08 | **Post-ship closure `2026-08-07__release-v8.4` STEP 8, two immediate lessons-learnt actions — execution_prompt.md v3.65→v3.66: commit-SHA-write reminder in the in-session provisioning sub-path + test_scenarios roll-up backstop.** §8 source prompt header v3.65→v3.66 (line 887). §14 Execution Engine Source v3.65→v3.66. §14 Version 4.146→4.147/2026-08-08. Changes: (1, LL-v8.4-P3-01) §3.1.B's in-session credential/action provisioning sub-path (LL-v8.2-P3-04) gains an explicit cross-reference back to step 4a's commit-SHA-write rule (`LL-v4.8-EX-01`) — its own step list ended at "re-run Unblock detection" with no pointer back, and 3 items this cycle (ST-20/ST-21/ST-23) reached `status: done` with `commit_sha: null` as a result. (2, LL-v8.4-P4-01) STEP 3.1.A step 12 "Post-story test files check" gains a roll-up backstop — before EPIC seal, cross-check the EPIC-level `test_scenarios` array against the union of test files already present in that EPIC's stories' own `spec_references`, backfilling any gap; EPIC-01 shipped with `test_scenarios: []` this cycle despite genuine, real-CI-confirmed coverage correctly recorded at story level. Authority: Head of Specs Team (post-ship closure STEP 8 immediate-action rule, 2026-08-08). |
| 4.146 | 2026-08-08 | **Sprint execution `2026-08-07__release-v8.4` EPIC-07/ST-29 (BLG-GOV-286) — release_planning_prompt.md v2.47→v2.48: new §1.3a Gate-Detection Procedure (scripted, mandatory).** §6B source prompt header v2.47→v2.48 (line 623). §14 Release Engine Source v2.47→v2.48. §14 Version 4.145→4.146/2026-08-08. Change: replaces ad hoc field-reading for detecting gate-blocked backlog candidates with a canonical script (`scripts/scan_backlog_gate_conditions.py`) run before §1.4a's Perennial-Return Check — fixes 3 self-caught scan misses across `v8.0`/`v8.1`/`v8.2` (gate-field-name variants, scan line-window bounds, `Provisional-Target`-embedded gate condition) plus a 4th failure mode self-caught this cycle (missing `---` separator between adjacent backlog entries, letting one item's body text bleed into the next item's field scan — confirmed live on 20 of 293 items in the current `backlog.md`). The script determines item boundaries by heading only, never `---`, structurally eliminating failure mode 4 rather than merely detecting it; covers `Gate criteria`/`Gate`/`Gate date` field variants; flags embedded-gate-language-with-no-formal-field as a data-quality warning (found 5 live instances on first run: `BLG-FEAT-74`, `BLG-FEAT-76`, `BLG-SPEC-56`, `BLG-SPEC-57`, `BLG-QA-59`). Authority: Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-29, 2026-08-08). |
| 4.145 | 2026-08-07 | **User-directed session review — shared_standards.md v3.25→v3.26: §16.14 Last Updated Header-History Retention Convention broadened from Class-4-only to universal scope.** §14 Shared Standards v3.25→v3.26. §14 Version 4.144→4.145/2026-08-07. Change: the chained `**Last Updated:**` header-bloat pattern (cap: current + 2 prior, 3 total) is no longer scoped to named Class 4 files — it applies to any document, any Class, using the chained pattern. Root cause: `backlog.md`'s header chain reached 56 entries/~32,000 characters despite being truncated once (2026-07-28) under the original narrower rule, because it was never named in that rule's "Applies to" list and nothing re-applied the cap on later touches. Companion `CLAUDE.md` §2 non-negotiable added (no version field, logged here per the established convention). 7 offending files' headers truncated to the 3-entry cap in the same session: `backlog.md`, `backlog_archive.md`, `docs/System_status_report.md`, `docs/specs/Specs_Index.md`, `roadmap_archive.md`, `ideas_register_archive.md`, `claude/cycles/velocity_metrics.md`. Follow-up backlog item filed for `Specs_Index.md` to gain a proper `## Changelog` table. Authority: Head of Specs Team (user-directed, 2026-08-07). |
| 4.144 | 2026-08-07 | **Lessons-learnt deferred patch resolution (Head of Specs Team acting as Base44 Frontend Prompt Owner + Head of Engineering, reviewing `2026-08-05__release-v8.3` lessons_learnt_closure.md) — execution_prompt.md v3.64→v3.65 + shared_standards.md v3.24→v3.25: environment-parity sub-clause + CI failure diagnosis/workflow-authoring guidance.** §8 source prompt header v3.64→v3.65 (line 887). §14 Execution Engine Source v3.64→v3.65; Shared Standards v3.24→v3.25. §14 Version 4.143→4.144/2026-08-07. Changes: (1, Base44 Frontend Prompt Owner) `execution_prompt.md` §5.1 Frontend testing gate gains an environment-parity sub-clause — for focus-restoration/interaction-timing ACs, DoQ sign-off must record a real GitHub Actions CI pass (not sandboxed-review-only), per the `SC-CR-11` real-CI catch at ST-11. (2, Head of Engineering) `shared_standards.md` new §6.1 — documents `scripts/check_ci_infra_outage.py` (classifies a failed run/job as infra-outage vs real via known signature strings; detects the "stuck rerun" symptom; recommends an empty retrigger commit rather than fighting a stuck run) and the `pipefail`/`tee` exit-code capture gap in GitHub Actions `run:` steps (declare `shell: bash` or capture via `${PIPESTATUS[0]}`) — both rooted in the 2026-08-06 GitHub Actions outage (PR #1259/#1260). Authority: Head of Specs Team (2026-08-07). |
| 4.143 | 2026-08-07 | **Lessons-learnt deferred patch resolution (Head of Specs Team, reviewing `2026-08-05__release-v8.3` lessons_learnt_closure.md, carried from `2026-08-04__release-v8.2` closure LL-v8.2-P3-04) — execution_prompt.md v3.63→v3.64: §3.1.B in-session credential/action provisioning sub-path.** §8 source prompt header v3.63→v3.64 (line 887). §14 Execution Engine Source v3.63→v3.64. §14 Version 4.142→4.143/2026-08-07. Change: distinguishes the standard cross-session park-and-wait delegation flow from the case where a human supplies the blocking credential/action directly within the current session — the delegation log entry is still created at the moment the need is identified (not retroactively at sprint close), and unblock detection re-runs immediately rather than waiting for a future resume, with an explicit `"Unblocked in-session — ..."` log note. Also `CLAUDE.md` §8 (no version field) gains new step 2a — identical-text-masks-differing-semantics check for cross-EPIC merges of shared governance prompts, logged in `prompt_change_log.md` per the established no-version-field convention for this file. Authority: Head of Specs Team (2026-08-07). |
| 4.142 | 2026-08-07 | **Post-ship closure `2026-08-05__release-v8.3` Recurrence Escalation resolution (Head of Specs Team, acting on the closure's §6 Outstanding Action, 72h deadline 2026-08-10, resolved same-day) — execution_prompt.md v3.62→v3.63: §7 Write Scope Restriction gains a narrow, explicit exception for `claude/backlog/backlog.md`.** §8 source prompt header v3.62→v3.63 (line 887). §14 Execution Engine Source v3.62→v3.63. §14 Version 4.141→4.142/2026-08-07. Change: after 3 consecutive cycles (`v8.1`→`v8.2`→`v8.3`) of mid-sprint `backlog.md` additions operating on informal precedent against the documented "must not modify" rule, formally sanctioned (not reaffirmed-and-closed) a narrow exception — new-item addition only, for genuinely out-of-scope findings surfaced mid-sprint, with a mandatory `**Source:**` attribution; editing existing items, scope/priority decisions, and the Release Slice/capacity tables remain off-limits. Authority: Head of Specs Team (post-ship closure `2026-08-05__release-v8.3` escalation, `lessons_learnt_prompt.md` §6.4 recurrence path, resolved 2026-08-07). |
| 4.141 | 2026-08-06 | **Sprint execution `2026-08-05__release-v8.3` EPIC-05/ST-26 (BLG-GOV-270) — roadmap_prompt.md v9.12→v9.13: new §7.2 Cross-Role Workload Balance Check.** §6 source prompt header v9.12→v9.13 (line 399). §14 Roadmap Engine Source v9.12→v9.13. §14 Version 4.140→4.141/2026-08-06. Change: new advisory check, distinct from §7.1's Skill-Silo Alert (which classifies story *shape*, governance-heavy vs execution-heavy) — tallies story *ownership by named role* (`sprint_backlog.md`'s `**Owner:**` field) over the same rolling 3-cycle window, flagging >40% single-role concentration (mirrors §7.1's ceiling for consistency). Advisory only, no mandatory-pull-forward escalation (role concentration can legitimately reflect a release's genuine thematic focus, not always a bottleneck). Authority: Director of HR (Sprint Execution Engine, agent-mediated, ST-26, 2026-08-06). |
| 4.140 | 2026-08-06 | **Sprint execution `2026-08-05__release-v8.3` EPIC-05/ST-22 (BLG-GOV-124) — release_planning_prompt.md v2.46→v2.47: RESUME PRECHECK mutation-detection block removed.** §6B source prompt header v2.46→v2.47 (line 623). §14 Release Engine Source v2.46→v2.47. §14 Version 4.139→4.140/2026-08-06. Change: removed the ~65-line mutation-detection/invalidation-map/efficiency-policy machinery (Purpose/Tracked items/Detection/Invalidation map/Safety policy/Efficiency policy subsections) — this path was never exercised in any recorded v4.x–v5.x cycle; the existing lightweight `state.json` not_started/fail/blocked resume rule provides sufficient resumability for the observed failure mode. The Terminal State Guard ("Published Is Immutable") and State File Immutability Rule hard gates were extracted intact into their own top-level `## Terminal State Guard` section (both continue to apply on every resume, unaffected by the removal — per the sign-off constraint from GCA-2026-06-17 SC-02). Two stale cross-references to the removed block's STEP 4.5 "safety policy" rerun rule and the RESUME PRECHECK heading name were also removed/relabelled. Dry-run validation pass: swept the full file for remaining `RESUME PRECHECK`/`invalidation`/`mutation_seq` references post-edit — none found outside the explanatory extraction note; `state.sealed.sealed_assumptions` (written by `publish_gate.md` at STEP 8, an unrelated seal-for-the-record step) and the `release_state_schema.json` template fields were confirmed to serve a purpose independent of the removed detection logic and were left unchanged. Authority: Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-22, 2026-08-06). |
| 4.139 | 2026-08-06 | **Sprint execution `2026-08-05__release-v8.3` EPIC-05/ST-25 (BLG-GOV-257) — sprint_planning_prompt.md v3.15→v3.16 + shared_standards.md v3.23→v3.24: prompt change log gap detection fixed from file-position to date-scan.** §7 source prompt header v3.15→v3.16 (line 766). §14 Sprint Planning Engine v3.15→v3.16, Shared Standards v3.23→v3.24. §14 Version 4.138→4.139/2026-08-06. Change: STEP -1 Hygiene advisories — "Prompt change log gaps" check rewritten from `grep \| head -1` to a date-scan method (collect every matching row, parse each row's Date column, select the latest date) — `prompt_change_log.md` is not uniformly ordered (a prepend-newest-first block sits above an older ascending-chronological historical backfill), so file position does not correlate with recency across the whole file. New `shared_standards.md` §11.1 documents the method for reuse by any future equivalent check. Root cause: confirmed false-positive during `plan sprint 2026-07-24__release-v7.8` (`sprint_planning_prompt.md` v3.13 already logged further down the file, `head -1` returned a stale v3.12 row). Authority: Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-25, 2026-08-06). |
| 4.138 | 2026-08-04 | **Sprint execution `2026-08-04__release-v8.2` EPIC-05/ST-25 (BLG-FE-131) — design_gate_prompt.md v1.8→v1.9: motion/timing-sensitive interaction classification note.** §6.5 source prompt header v1.8→v1.9 (line 570). §14 Design Gate Engine v1.8→v1.9. §14 Version 4.137→4.138/2026-08-04. Change: §6 Design Requirement Classification gains an explicit note that chart transition animations, tooltip delay timing, loading-state debounce/throttle windows, and other motion/timing parameter changes are always Design Required, even absent a new component or layout change — closes the gap where such changes fell through the cracks between the "visual rendering" and "interaction flow" criteria. Authority: Head of UX & Design (Sprint Execution Engine, agent-mediated, ST-25, 2026-08-04). |
| 4.137 | 2026-08-04 | **Sprint execution `2026-08-04__release-v8.2` EPIC-03/ST-18 (BLG-GOV-285) — shared_standards.md v3.22→v3.23: delegation-record auto-close false-positive fix documented.** §14 Shared Standards v3.22→v3.23. §14 Version 4.136→4.137/2026-08-04. Change: `.github/workflows/governance_sync.yml` now cross-checks a story's actual `execution_state` status (per-EPIC files or legacy single file) before auto-closing its GitHub issue, rather than trusting the presence of `[ST-xx]` in a commit message alone — fixes a false-positive that recurred twice (v8.0 EPIC-02/ST-08 issue #1148, v8.1 EPIC-02/ST-02 issue #1169). Documented in `shared_standards.md` §6. Authority: Head of Engineering (Sprint Execution Engine, agent-mediated, ST-18, 2026-08-04). |
| 4.136 | 2026-08-04 | **Sprint execution `2026-08-04__release-v8.2` EPIC-03/ST-15 (BLG-GOV-279) — roadmap_prompt.md v9.11→v9.12: SI-02 production credential provisioning decision.** §6 source prompt header v9.11→v9.12 (line 399). §14 Roadmap Engine Source v9.11→v9.12. §14 Version 4.135→4.136/2026-08-04. Change: STEP 2.3 Credential-fallback guidance gains a Standing-behaviour decision — Product Owner formally accepted the fallback-citation pattern as permanent, intended behaviour (option (b) of the two named in the backlog item), closing the recurring "next rebalance should attempt a genuine live re-check" carry-forward pattern that had appeared in 3+ consecutive cycles' lessons-learnt/carry-forward notes without resolution (no production credential was ever persisted into the gitignored `.env.production`/`.env.staging` files — confirmed empty again this session). Authority: Product Owner (Sprint Execution Engine, agent-mediated, ST-15, 2026-08-04). |
| 4.135 | 2026-08-04 | **Sprint execution `2026-08-04__release-v8.2` EPIC-03/ST-17 (BLG-GOV-283) — three source prompt version bumps.** §6 source prompt header `roadmap_prompt.md` v9.10→v9.11 (line 399). §6M `ideas_housekeeping_prompt.md` v1.1→v1.2 (line 478). §14: Roadmap Engine Source v9.10→v9.11, Ideas Housekeeping Engine v1.1→v1.2, Shared Standards v3.21→v3.22. §14 Version 4.134→4.135/2026-08-04. Change: new `shared_standards.md` §16.14 Last Updated Header-History Retention Convention (retain current + 2 prior entries, 3 total, in chained `**Last Updated:**` fields), applied at `roadmap_prompt.md` STEP 9 and `ideas_housekeeping_prompt.md` §1.4 (the actual write site for `ideas_register.md`'s header — the sprint backlog's AC named `idea_intake_prompt.md` but that file has no chained-header write step; verified by grep before assigning the fix to the correct file). Rule applied retroactively to `ideas_register.md`'s own header, truncated from 5 chained entries to 3. **Also backfilled two pre-existing drifts found during this edit's own pre-check:** `design_gate_changelog.md` missing v1.7 row (ST-16, same session) and `ideas_housekeeping_changelog.md` missing v1.1 row. Authority: Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-17, 2026-08-04). |
| 4.134 | 2026-08-04 | **Sprint execution `2026-08-04__release-v8.2` EPIC-03/ST-16 (BLG-GOV-281) — design_gate_prompt.md v1.7→v1.8: mandatory §13 boundary pre-check for AI-calling proposals.** §6.5 source prompt header v1.7→v1.8 (line 570). §14 Design Gate Engine v1.7→v1.8. §14 Version 4.133→4.134/2026-08-04. Change: STEP 1 (Classify Each Item) gains a mandatory §13 boundary pre-check for any item — Design Required or Design Pre-Approved — introducing/extending an AI provider call. Flags `§13 PRE-CHECK REQUIRED` when no covering §13 review decision record exists, gating design/implementation start until a `delegated_decision` §13 gate story clears it (per `execution_prompt.md` §5.1's existing pattern). **Also backfilled a pre-existing drift found during this edit's own pre-check:** `design_gate_changelog.md` was missing its v1.7 row despite the header already carrying v1.7 since v8.0/ST-05 (2026-07-30) — restored per `CLAUDE.md` §6. Authority: Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-16, 2026-08-04). |
| 4.133 | 2026-08-04 | **Sprint execution `2026-08-04__release-v8.2` EPIC-03/ST-11 (BLG-GOV-218) — post_ship_closure.md v2.23→v2.24: Rebalance Cadence Check corrected-skip logic.** §10 source prompt header v2.23→v2.24 (line 1062). §14 Post-Ship Closure Engine v2.23→v2.24. §14 Version 4.132→4.133/2026-08-04. Change: STEP 0's Rebalance Cadence Check now reads `current_roadmap.md` §1 before emitting the unconditional odd-cycle "REBALANCE SKIP" advisory — if `next_release` is `[TBD]`/unscoped, or already carries a non-`[TBD]` roadmap Status (already scoped/committed), a corrected "REBALANCE SKIP WITHHELD" advisory fires instead, since "proceed directly to `plan release`" would be stale or not-yet-actionable. A genuinely fresh, unconsumed `next_release` still gets the standard advisory (no regression). Authority: Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-11, 2026-08-04). |
| 4.132 | 2026-08-03 | **Post-ship closure `2026-08-03__release-v8.1` STEP 8 immediate action (LL-v8.1-P4-01) — delivery_verification_prompt.md v3.6→v3.7: STEP -1.3A PR-recovery write target redirected.** §9 source prompt header v3.6→v3.7. §14 Verification Engine Source v3.6→v3.7. §14 Version/Last Updated self-row corrected from stale 4.127 to 4.132 (drifted 4 versions behind the table's own top row — header-drift pattern per the standing v4.85 note, caught here). Change: STEP -1.3A PR Number Recovery no longer hand-writes a recovered `pr_number` into the disposable/regenerate-on-read `execution_state.json`; it now writes into the owning `execution_state/EPIC-xx.json` file (per `shared_standards.md §12.1`, added this same cycle by ST-19) and regenerates the summary, with a fallback to the legacy direct write for pre-per-EPIC-mechanism cycles. Closes a friction item surfaced proactively by EPIC-07's agent-mediated reviewer (not yet triggered in practice — no PR recovery was needed this run). Authority: Head of Specs Team (post-ship closure `2026-08-03__release-v8.1`, STEP 8 immediate lessons-learnt action rule). |
| 4.131 | 2026-08-03 | **Sprint execution `2026-08-03__release-v8.1` EPIC-04/ST-12 (BLG-QA-129) — post_ship_closure.md v2.22→v2.23: cross-cycle deviation consolidation review.** §10 source prompt header v2.22→v2.23 (line 1062). §14 Post-Ship Closure Engine v2.22→v2.23. §14 Version 4.130→4.131/2026-08-03. Change: new STEP 5.1 — periodic (every 3rd invocation) consolidation of `DEV-*` deviation records across recent cycles, Director of Quality sign-off required, produces `docs/governance/deviation_consolidation_review_<date>.md`. First run catalogued 9 records, found and fixed a resolution-status drift between `docs/testing/slippage_scenarios.md` and `docs/specs/frontend/pages/trade_history.md`'s sibling `DEV-ST14-01` entries. Authority: Director of Quality (Sprint Execution Engine, agent-mediated, ST-12, 2026-08-03). |
| 4.130 | 2026-08-03 | **Sprint execution `2026-08-03__release-v8.1` EPIC-04/ST-11 (BLG-QA-113) — sprint_planning_prompt.md v3.14→v3.15: recurring endpoint test coverage audit.** §7 source prompt header v3.14→v3.15 (line 766). §14 Sprint Planning Engine v3.14→v3.15. §14 Version 4.129→4.130/2026-08-03. Change: STEP -1 Advisory Checks gains item 8 — runs new `scripts/audit_endpoint_test_coverage.py` (full-repo backstop audit vs. the existing pre-commit diff-only check) before sprint scope work; first run: 78 routes scanned, 8 documented `KNOWN_GAPS` exclusions, 0 undocumented gaps. **Merge-order reconciliation:** this bump was made on `exec/2026-08-03__release-v8.1/EPIC-04`, cut before EPIC-03/ST-05's own `sprint_planning_prompt.md` v3.13→v3.14 bump merged to `main` — both branches independently landed on `3.14`; renumbered to `3.15` (and this row to `4.130`, was `4.129`) at EPIC-04's merge time, per the standing multi-EPIC shared-file merge-order convention (`CLAUDE.md` §8). Authority: Head of Specs Team (Sprint Execution Engine, ST-11, 2026-08-03). |
| 4.129 | 2026-08-03 | **Sprint execution `2026-08-03__release-v8.1` EPIC-03/ST-03/ST-04/ST-05/ST-07/ST-09 — four source prompt version bumps.** §6 source prompt headers: `roadmap_prompt.md` v9.8→v9.10 (line 399), `release_planning_prompt.md` v2.44→v2.46 (line 623), `sprint_planning_prompt.md` v3.13→v3.14 (line 766). §13 Artefact Register Roadmap Rebalance Prompt row v9.8→v9.10. §14 Roadmap Engine Source v9.8→v9.10, Release Engine Source v2.44→v2.46, Sprint Planning Engine v3.13→v3.14, Shared Standards v3.20→v3.21. §14 Version 4.128→4.129/2026-08-03. Changes: (ST-03, BLG-GOV-280) `release_planning_prompt.md` new §1.4a.1 Sunset Criteria for the Perennial-Return Check, applied retroactively to `BLG-FEAT-73`/`BLG-FEAT-74` (2 of 4, below trigger); (ST-07, BLG-GOV-246) same file's STEP 3 gains a Skill-Silo-tied execution-heavy rotation advisory (Director of HR); (ST-04, BLG-GOV-268) `roadmap_prompt.md` STEP 2.4 gains a mandatory-pull-forward clause for sustained Product Value Ratio Advisory-tier readings, mirroring §7.1's Skill-Silo clause; (ST-09, BLG-GOV-240) `shared_standards.md` §17 gains a companion provision — Head of Specs Team standing authority to relabel a resolved un-versioned Now-horizon carry-forward heading with its confirmed version without a full `run roadmap` invocation, cross-referenced from `roadmap_prompt.md` STEP 8.1; (ST-05, BLG-GOV-254) `sprint_planning_prompt.md` new §1.5 Minimum Capacity Buffer Floor (95% advisory target, FinOps & Resource Architect + PMO Lead). Authority: Head of Specs Team / Product Owner (Sprint Execution Engine, agent-mediated per §5.3 for each named authority, 2026-08-03). |
| 4.128 | 2026-08-03 | **Sprint execution `2026-08-03__release-v8.1` EPIC-07/ST-19 (BLG-GOV-284) — shared_standards.md v3.19→v3.20: §12 Rule 2 retired, new §12.1 Per-EPIC Execution State Mechanism added.** §14 Shared Standards v3.19→v3.20. §14 Version/Last Updated table row corrected from a stale 4.125/2026-07-31 to 4.128/2026-08-03 (the table's own top row had already reached 4.127/2026-08-03 — header-drift pattern per the standing v4.85 note, caught here). Change: each EPIC branch now owns `claude/cycles/<cycle_id>/execution_state/EPIC-xx.json` exclusively (schema: `claude/system/schemas/execution_state_epic_schema.json`); cycle-level fields live in `_cycle_meta.json`; the cycle-level `execution_state.json` is regenerated on demand by `claude/system/scripts/generate_execution_summary.py` rather than hand-merged, eliminating the structural merge-conflict source Rule 2 existed to resolve. Authority: Head of Engineering (agent-mediated sign-off per execution_prompt.md §5.3, RISK-02 mitigation), Sprint Execution Engine, 2026-08-03. |
| 4.127 | 2026-08-03 | **Lifecycle audit AUD-2026-08-03 improvements 003/005 — post_ship_closure.md v2.21→v2.22 + §13 Artefact Register.** §10 source prompt header v2.21→v2.22. §14 Post-Ship Closure Engine v2.21→v2.22. §13 Artefact Register — new "Escalations (Closure)" row for `claude/cycles/<id>/closure_escalations.md` (was missing despite being a real, actively-used Class 4 artefact with siblings for Release/Execution/Verification already registered). §14 Version 4.126→4.127/2026-08-03. Change (post_ship_closure v2.22): STEP 6 Endpoint Coverage Drift Check gains a "Script-derived tracking-item handoff" rule — when the existing stale-tracking-item delta rule fires, also emit the fully re-derived current-gap endpoint list into the closure record's Advisory Summary in copy-paste-ready form, so the next engine applies it verbatim rather than re-deriving the diff each cycle; closes the 3-cycle recurring `BLG-OPS-111` drift pattern (v7.9→v7.10→v8.0), which is itself retired as superseded by this fix. Authority: Head of Specs Team (lifecycle audit AUD-2026-08-03, resolved 2026-08-03). |
| 4.126 | 2026-08-03 | **ESC-CLOSE-20260731-01 (Option a) — delivery_verification_prompt.md v3.5→v3.6: named domain-authority sign-off class added to STEP -1.3 Tier 2.** §9 source prompt header v3.5→v3.6. §14 Verification Engine Source v3.5→v3.6. §14 Version 4.125→4.126/2026-08-03. Change: STEP -1.3 Tier 2 gains a fourth recognised sign-off format — a signer naming a specific human or agent-mediated domain-authority role (e.g. `Infrastructure & Operations Owner`, `Head of Engineering`, compound `<Role A> ... with <Role B> concurrence` forms, or execution_prompt.md §5.3's Infrastructure co-sign format) is accepted as compliant provided the EPIC contains no `autonomous`-class story. Closes the gap where execution_prompt.md's Infrastructure co-sign class claimed acceptance by this gate that the gate did not actually implement — surfaced when EPIC-04 and EPIC-06 both required one-off DoQ counter-signs at `2026-07-30__release-v8.0` delivery verification despite using legitimate domain-authority signers. Authority: Head of Specs Team (post-ship closure `2026-07-30__release-v8.0` escalation ESC-CLOSE-20260731-01, resolved 2026-08-03). |
| 4.125 | 2026-07-31 | **Post-ship closure `2026-07-30__release-v8.0` Phase 3 lessons learnt, action-now — execution_prompt.md v3.61→v3.62: infra/ops verification delegation sub-pattern added.** §8 source prompt header v3.61→v3.62. §14 Execution Engine Source v3.61→v3.62. §14 Version 4.124→4.125/2026-07-31. Change: §5.1 Delegation Classification "Classification rules" list gains a new bullet — an infrastructure/operations verification or configuration task requiring live external dashboard/production access the engine cannot perform (e.g. Render/Supabase dashboard reads, GitHub repo secret configuration) classifies as `delegated_backend`, regardless of whether any code is written. Root cause: v8.0 sprint execution recorded 6 of 19 stories (32% of scope — ST-13/14/15/16/17 in EPIC-04, ST-19 in EPIC-06) as stale `autonomous` at STEP 0, requiring mid-execution correction, because §5.1's existing `delegated_backend` pattern ("new router, service, or database function") had no explicit coverage for dashboard-access-only verification tasks. Authority: Head of Specs Team (post-ship closure `2026-07-30__release-v8.0`, STEP 8 — immediate lessons-learnt action rule). |
| 4.124 | 2026-07-30 | **ST-05 (BLG-SEC-23, EPIC-02, v8.0) — design_gate_prompt.md v1.6→v1.7: mandatory AI-endpoint security checklist reference added.** §6.5 source prompt header v1.6→v1.7. §14 Design Gate Engine v1.6→v1.7. §14 Version 4.123→4.124/2026-07-30. Change: STEP 2.2 (Design Required Items: Artefact Review, constraints list) gains a new constraint — any item introducing a new AI-calling endpoint must complete the mandatory security review checklist at the new `docs/specs/security/ai_endpoint_security_checklist.md` (rate limiting, cost gating, prompt-injection awareness) before its design artefact is approved. This new checklist is distinct from `docs/specs/api_contracts/ai_advisory_contract_checklist.md`'s contract-completeness checklist (documentation completeness, not security posture) — both are now required. Authority: Head of Specs Team (Sprint Execution Engine, ST-05, agent-mediated, 2026-07-30). |
| 4.123 | 2026-07-30 | **Post-ship closure `2026-07-28__release-v7.10` Phase 3 lessons learnt (LL-v7.10-P3-01), action-now — backlog_management_prompt.md v1.12→v1.13: Governance Prompt Duplicate Cross-Check added.** §6M source prompts updated (backlog_management_prompt.md v1.12→v1.13). §14 Backlog Management Engine v1.12→v1.13. §14 Version 4.122→4.123/2026-07-30. Change: STEP 1 gains a new §1.3 — before confirming any open `BLG-GOV-*` item as still-open, grep `claude/system/prompt_change_log.md` for entries against the same prompt file filed after the item's own filing date; flag a probable-duplicate candidate for owner review if a matching version-transition entry already covers the item's stated problem (does not auto-close). Root cause: v7.10 sprint execution pulled 3 of 23 stories (13% of scope) into scope that were already fully resolved by prior-sprint governance fixes, requiring the STEP 3.1.A pre-met path instead of fresh delivery — none were caught as stale/duplicate by backlog grooming beforehand. Authority: Head of Specs Team (post-ship closure `2026-07-28__release-v7.10`, Phase 3 lessons-learnt action-now rule). |
| 4.122 | 2026-07-30 | **Post-ship closure `2026-07-28__release-v7.10` Phase 4 lessons learnt (LL-v7.10-P4-01), action-now — execution_prompt.md v3.60→v3.61: pre-seal `completed_items` cross-EPIC union check added.** §8 source prompt header v3.60→v3.61. §14 Execution Engine Source v3.60→v3.61. §14 Version 4.121→4.122/2026-07-30. Change: STEP 7 (Seal Execution Record) gains a new pre-seal check, immediately before the existing delegation_log.md integrity check — before writing `sealed: true`, verify the top-level `completed_items` array is the full cross-EPIC union of `done`/`merged` story IDs (per `shared_standards.md §12` Rule 2 / `CLAUDE.md §8`), not just the first-merged EPIC's items. Root cause: v7.10's own sealed `execution_state.json` shipped with `completed_items` containing only EPIC-04's 4 stories instead of the full 23 — did not affect verification (per-story status fields were all correctly `done`), but the summary array was materially incomplete. Delivery Verification's write scope does not include `execution_prompt.md`, so the fix was deferred to Post-Ship Closure, which does. Authority: Head of Specs Team (post-ship closure `2026-07-28__release-v7.10`, Phase 4 lessons-learnt action-now rule). |
| 4.121 | 2026-07-29 | **ST-22 (EPIC-06, v7.10, BLG-GOV-216) — roadmap_prompt.md v9.7→v9.8: recent-rebalance recency advisory added.** §6 source prompt header v9.7→v9.8. §13 Artefact Register Roadmap Rebalance Prompt row v9.7→v9.8. §14 Roadmap Engine Source v9.7→v9.8. §14 Version 4.120→4.121/2026-07-29. Change: new STEP -1.5.5 — when a `--reason "scheduled"` invocation's `last_scheduled_rebalance_utc` is less than 24h old, surface a non-blocking confirmation advisory before proceeding, giving the invoking user/PO an explicit chance to confirm intent ahead of a same-day re-run, rather than only discovering the collision after `BLG-GOV-207`'s STEP 0 auto-suffix has already resolved the `cycle_id` mechanically. **Sign-off review (Head of Specs Team, agent-mediated) caught that no step actually wrote `last_scheduled_rebalance_utc`** — STEP 12.1's global-state write block never set this key (only `last_rebalance_utc`), so the new advisory (and the pre-existing Extended-tier ">90 days" check at §2.4) would have read a stale/never-set value. Fixed in the same commit: STEP 12.1 now sets `last_scheduled_rebalance_utc` = this run's `last_rebalance_utc` whenever `--reason` is `"scheduled"`. Authority: Head of Specs Team (Sprint Execution Engine, ST-22, 2026-07-29). |
| 4.120 | 2026-07-28 | **Post-ship closure `2026-07-27__release-v7.9` STEP 6 self-discovered friction, immediate action — post_ship_closure.md v2.20→v2.21: Endpoint Coverage Drift Check advisory gains a stale-tracking-item delta note.** §10 source prompt header v2.20→v2.21. §14 Post-Ship Closure Engine v2.20→v2.21. §14 Version 4.119→4.120/2026-07-28. Change: when an existing open `BLG-OPS-*` tracking item is referenced instead of filing a duplicate, and the current normalised gap has grown beyond that item's own recorded list, the routine must not edit the existing item's body (outside backlog write scope) but must record the delta explicitly in the closure record and Advisory Summary so the tracking item's owner can reconcile it. Found this run: `BLG-OPS-111` (filed at v7.2, 21 endpoints) now understates the true gap by 4 (25 endpoints found this run, including 1 new from this cycle's own EPIC-01 `PATCH /watchlist/{entry_id}`). Authority: Head of Specs Team (post-ship closure `2026-07-27__release-v7.9`, STEP 8 — immediate lessons-learnt action rule, self-discovered same-run friction). |
| 4.119 | 2026-07-28 | **Post-ship closure `2026-07-27__release-v7.9` STEP 8 immediate action (Release Planning lessons_learnt.md Friction Item 1) — roadmap_prompt.md v9.6→v9.7: candidate live-status cross-check added.** §6 source prompt header v9.6→v9.7. §14 Roadmap Engine Source v9.6→v9.7. §14 Version 4.118→4.119/2026-07-28. Change: added a "Candidate live-status cross-check" instruction immediately after the existing LP-05 gate-verification note — before naming any pull-forward candidate, the engine must confirm the item is still open in `backlog.md` (not archived/shipped), including checking any `groom backlog`/post-ship-closure action already taken earlier in the same session. Closes the gap where `2026-07-27__scheduled` named already-archived `BLG-FE-128` as a pull-forward candidate, caught only downstream at `plan release v7.9` via an appended correction. Authority: Head of Specs Team (post-ship closure `2026-07-27__release-v7.9`, STEP 8 — immediate lessons-learnt action rule). |
| 4.118 | 2026-07-27 | **User-directed follow-up to BLG-GOV-190 — design_gate_prompt.md v1.5→v1.6: root `status` enum transition implemented per `lifecycle_schema.json`.** `lifecycle_schema.json` already defined the transition `Release_Planning_Complete → Design_Gate_Passed` (engine: Design Gate, completion signal: `design_gate_status = Passed AND design_gate.md present`), but no engine ever implemented the write — this is the deeper root cause behind the recurring `sprint_planning_prompt.md` STEP -1.3 bypass-audit false positive (v7.8, v7.9), which is keyed off the root `status` enum, not the `design_gate_status` field that the v1.5 fix mirrored. §5 Write Scope Restriction: `.claude_current_state.json` write now additionally permits `status` set to exactly `"Design_Gate_Passed"`, only when `design_gate_status = Passed` (no transition defined for `Blocked` — root pointer correctly stays at `Release_Planning_Complete` until the gate clears). STEP 5: added the schema-defined transition write, with the pre-write unchanged-value check per `shared_standards.md` §10.3. §7 Completion Condition updated. No change required to `sprint_planning_prompt.md` — its existing bypass-audit logic ("entered from `Release_Planning_Complete` = design gate skipped") becomes correct once this engine actually performs the transition it was always supposed to. §6.5 source prompt header v1.5→v1.6. §14 Design Gate Engine v1.5→v1.6. §14 Version 4.117→4.118/2026-07-27. Authority: Head of Specs Team (direct action, user-invoked, 2026-07-27). |
| 4.117 | 2026-07-27 | **BLG-GOV-190 — design_gate_prompt.md v1.4→v1.5: root state pointer sync gap closed.** §5 Write Scope Restriction: added `.claude_current_state.json`, additive-only, restricted to `design_gate_status`/`design_gate_record`/`design_gate_completed_utc`. STEP 5: added a mirror write of those three fields into `.claude_current_state.json` immediately after the existing cycle-level `state.json` write — no other field (in particular `status`, `design_gate_bypass_authority`, `design_gate_bypass_reason`) is touched. STEP 6: `.claude_current_state.json` added to the commit's `git add` list. §7 Completion Condition updated to reference the mirrored write. §6.5 source prompt header v1.4→v1.5. §14 Design Gate Engine v1.4→v1.5. §14 Version 4.116→4.117/2026-07-27. Root cause: the root pointer's `design_gate_status` field was initialised `not_started` by Release Planning STEP 0 and never subsequently written by any engine, so it reported stale even after a gate genuinely passed (recurred `2026-07-24__release-v7.8` → `2026-07-27__release-v7.9`, each session verifying directly against the cycle-level `state.json` as a workaround rather than a fix). Authority: Head of Specs Team (direct action, user-invoked, 2026-07-27). |
| 4.116 | 2026-07-27 | **Roadmap rebalance `2026-07-27__scheduled` STEP 11 Friction Item 1 — idea_intake_prompt.md v2.7→v2.8: §2.0 step 5 backlog-scope-overlap check upgraded from prose-advisory to a mandatory act (still non-blocking outcome).** §5 source prompt header v2.7→v2.8. §14 Idea Intake Engine v2.7→v2.8. §14 Version 4.115→4.116/2026-07-27. Change: the pre-v2.8 check existed as advisory prose ("briefly scan... advisory only") but was not actually performed at submission-generation time — confirmed this cycle when a retroactive STEP 4 check found 23 of 44 (52%) of a single window's submissions duplicated existing open backlog items, a saturation-driven cost of skipping the check up front. v2.8 requires the submitting agent to grep-check and explicitly record the result before finalising each topic; a submission restating an existing item with no materially new angle no longer counts toward the agent's minimum. Authority: Head of Specs Team (roadmap rebalance `2026-07-27__scheduled`, STEP 11). |
| 4.115 | 2026-07-27 | **Roadmap rebalance `2026-07-27__scheduled` STEP -1.5 resolved the one outstanding deferred patch from `2026-07-24__scheduled` (Friction Item 2) — roadmap_prompt.md v9.5→v9.6: STEP 2.3 SI-02 gate read instruction gains explicit credential-fallback guidance.** §6 source prompt header v9.5→v9.6. §14 Roadmap Engine Source v9.5→v9.6. §14 Version 4.114→4.115/2026-07-27. Change: when production API credentials are unavailable or a live check returns an auth failure, the engine must cite the existing structured field unchanged and record in `run_manifest.md` that a live check was attempted and why it did not succeed — never write a "live re-confirmed" claim without an actual successful authenticated response. Authority: Head of Specs Team (roadmap rebalance `2026-07-27__scheduled`, STEP -1.5, target date matched). |
| 4.114 | 2026-07-27 | **Post-ship closure `2026-07-24__release-v7.8` §6 Outstanding Actions row 1 applied — release_planning_prompt.md v2.43→v2.44 + roadmap_prompt.md v9.4→v9.5: `next_release` field ownership made explicit.** §6B source prompt header v2.43→v2.44. §6 source prompt header v9.4→v9.5. §14 Release Engine Source v2.43→v2.44; §14 Roadmap Engine Source v9.4→v9.5. §14 Version 4.113→4.114/2026-07-27. Change: `.claude_current_state.json.next_release` was found 4 releases stale at the start of the v7.8 Release Planning session because no engine explicitly owned the field. `release_planning_prompt.md` STEP 9 now writes `next_release` unconditionally from its own `--version` argument on every seal — the authoritative source. `roadmap_prompt.md`'s existing STEP 8 advisory pre-fill is retained but its text now explicitly says it is non-authoritative and must yield to the last Release Planning STEP 9 write. Authority: Head of Specs Team (post-ship closure `2026-07-24__release-v7.8` §6 row 1, 2026-07-27). |
| 4.113 | 2026-07-27 | **Post-ship closure `2026-07-24__release-v7.8` §6 Outstanding Actions rows 2, 4, 5, 6 applied — execution_prompt.md v3.59→v3.60 (header drift also corrected: this row's own Version/Last Updated had lagged the table's actual latest entry, 4.112/2026-07-27, per the standing header-drift-prevention note below).** §8 source prompt header v3.59→v3.60. §14 Execution Engine Source v3.59→v3.60. §14 Version 4.112→4.113/2026-07-27. Four independent fixes bundled in one execution_prompt.md edit pass: (OA-2) §3.2.B API performance baseline pre-PR check converted from a prose `grep` advisory to an enforced script step (`scripts/check_api_performance_baseline_drift.py`, also now the single implementation `quality_gate.yml`'s CI job delegates to) — the prose form failed to prevent the same class of miss twice (v7.6/EPIC-07, v7.8/EPIC-06). (OA-4) STEP 4 — new step 3c added: after each EPIC merge, proactively sync `execution_state.json` from `main` onto every still-pending sibling branch immediately (per CLAUDE.md §8 conflict rules), instead of letting every pending branch accumulate an independently-diverging copy until its own eventual merge gate; recurred 2 consecutive cycles with cost scaling up each time (10/11 branches v7.7, 11/12 v7.8). (OA-5) §3.1.A step 3 — new advisory: any commit hardcoding a count/total also derivable via script/AST scan must be re-derived fresh immediately before commit and again before PR-open if `main` has moved, since a stale-but-matching literal is invisible to `git merge` (recurred identically v7.7 and v7.8 EPIC-01/EPIC-06). (OA-6) §5.1 — agent-mediated PR review comment labeling convention codified: permitted when reviewing on behalf of a named role (e.g. Product Owner, Director of Quality), but never labeled as if authored by the human role itself, and never itself satisfying the always-human merge-gate conditions; formalises the ad hoc convention already used successfully this cycle, closing a ruling carried unruled from v7.7. Authority: Head of Specs Team + Head of Engineering (post-ship closure `2026-07-24__release-v7.8` §6 rows 2/4/5/6, 72h-deadline decisions, 2026-07-27). |
| 4.112 | 2026-07-27 | **Post-ship closure `2026-07-24__release-v7.8` STEP 6 self-discovered friction, immediate action — post_ship_closure.md v2.19→v2.20: Endpoint Coverage Drift Check advisory strengthened with path-parameter normalisation and existing-tracking-item check.** §10 source prompt header v2.19→v2.20. §14 Post-Ship Closure Engine v2.19→v2.20. §14 Version 4.111→4.112/2026-07-27. Change: the STEP 6 advisory's `openapi.yaml`-vs-`api_performance_baseline.md` endpoint diff produced 15 apparent false-positive gaps this run because the two documents use different path-parameter placeholder names for the same parameter (e.g. `{position_id}` vs generic `{id}`) — added an explicit normalisation instruction before diffing. Also added a check for an existing open `BLG-OPS-*` tracking item covering the same gap class before filing a new one, since this cycle's normalised gap turned out to be identical, pre-existing drift already tracked by the still-open `BLG-OPS-111` (filed at `2026-07-15__release-v7.2` post-ship closure). Authority: Head of Specs Team (post-ship closure `2026-07-24__release-v7.8`, STEP 8 — immediate lessons-learnt action rule, self-discovered same-run friction). |
| 4.111 | 2026-07-27 | **Post-ship closure `2026-07-24__release-v7.8` STEP 8 immediate action (Release Planning lessons_learnt.md Friction Item 1) — release_planning_prompt.md v2.42→v2.43: STEP 9 status-value conflict corrected.** §6B source prompt header v2.42→v2.43. §14 Release Engine Source v2.42→v2.43. §14 Version 4.110→4.111/2026-07-27. Change: STEP 9's terminal `.claude_current_state.json` sync literally instructed writing `status: Published`, a value absent from `lifecycle_schema.json`'s canonical state enum (which names this terminal state `Release_Planning_Complete`) — following the prompt literally would have stranded the cycle at Design Gate's next Lifecycle Guard check (unrecognised status → self-halt to `Blocked`). Corrected to `status: Release_Planning_Complete` per `shared_standards.md` §10.6 (lifecycle_schema.json prevails on conflict); added an explanatory note distinguishing this field from the cycle-level `state.json.status = Published` value (§6B.6 Publish Gate), which is unrelated and unaffected. Authority: Head of Specs Team (post-ship closure `2026-07-24__release-v7.8`, STEP 8 — immediate lessons-learnt action rule). |
| 4.110 | 2026-07-26 | **v7.8 sprint execution ST-02 (EPIC-02, BLG-FEAT-84) — post_ship_closure.md v2.18→v2.19: new STEP 1.5 Telegram Changelog Digest added.** §10 source prompt header v2.18→v2.19. §14 Post-Ship Closure Engine v2.18→v2.19. §14 Version 4.109→4.110/2026-07-26. Change: new STEP 1.5 (between STEP 1 Changelog Entry and STEP 2 Roadmap Update) invokes `scripts/send_changelog_digest.py`, sending the release's `### Changes shipped` entries via the existing Telegram notification infrastructure (`backend/services/si05_digest_service.py`'s POST+JSON+retry helper, shipped v2.4/v5.1). Hard rule: `backend/services/changelog_digest_service.py`'s `send_changelog_digest()` never raises — a failed send (missing credentials, Telegram API error) is logged and does not block closure; STEP 2 proceeds regardless. New batch checkpoint 1.5 records the step as attempted, not delivery-conditional. Authority: Sprint Execution Engine (v7.8 sprint execution, ST-02, 2026-07-26). |
| 4.109 | 2026-07-24 | **Roadmap rebalance `2026-07-24__scheduled` STEP 11 (self-discovered same-cycle friction) — roadmap_prompt.md v9.3→v9.4: STEP -1.7 scan widened to also match `## Recurrence Escalations` tables.** §6 source prompt header v9.3→v9.4. §13 Artefact Register Roadmap Rebalance Prompt row v9.3→v9.4. §14 Roadmap Engine Source v9.3→v9.4. §14 Version 4.108→4.109/2026-07-24. Change: the v9.3 due-date scan (added earlier this same cycle) only matched the `^## ESC-`/`SLA due-by` pattern and would have missed the 3 recurrence escalations actually found this cycle via the separate §16.8 Carry-Forward mechanism, which used a `## Recurrence Escalations` table structure instead — widened to check both. Authority: Head of Specs Team (roadmap rebalance `2026-07-24__scheduled`, STEP 11). |
| 4.108 | 2026-07-24 | **Roadmap rebalance `2026-07-24__scheduled` STEP 0 Carry-Forward review — shared_standards.md v3.18→v3.19: new §19 Array Guard Standard for JSON API Response Fields.** §14 Shared Standards v3.18→v3.19. §14 Version 4.107→4.108/2026-07-24. Change: resolves a recurrence escalation carried across 3 Post-Ship Closure cycles (v7.5→v7.6→v7.7), whose named target ("next roadmap review") had not occurred since `2026-07-17__scheduled` — codifies the `Array.isArray(...)` guard requirement before `.map()`/`.filter()`/`.forEach()` over JSON API response fields. Authority: Head of Specs Team (roadmap rebalance `2026-07-24__scheduled`, STEP 0). |
| 4.107 | 2026-07-24 | **Roadmap rebalance `2026-07-24__scheduled` STEP -1.5 (resolving 2 deferred patches from `2026-07-17__scheduled`, both due at this cycle) — roadmap_prompt.md v9.2→v9.3: STEP -1.7 Governance Health Score Outstanding Action Count extended to a due-date-aware cross-routine scan.** §6 source prompt header v9.2→v9.3. §13 Artefact Register Roadmap Rebalance Prompt row v9.2→v9.3. §14 Roadmap Engine Source v9.2→v9.3. §14 Version 4.106→4.107/2026-07-24. Changes: (1) `roadmap_prompt.md` STEP -1.7 — Outstanding Action Count now also scans the last 3 completed cycles' `lessons_learnt_closure.md`/`lessons_learnt.md` files across all five routines for escalations whose deadline falls on or before the current cycle's date, regardless of owning routine, closing the gap that let a Release-Planning-filed escalation with a roadmap-window deadline go undetected except by ad hoc manual review (`2026-07-17__scheduled` Friction Item 2). (2) `changelogs/shared_standards_changelog.md` — backfilled missing rows 3.12–3.16 (deferred from `2026-07-17__scheduled` Friction Item 1 as disproportionate for that same-session action-now patch). Authority: Head of Specs Team (roadmap rebalance `2026-07-24__scheduled`, STEP -1.5). |
| 4.106 | 2026-07-21 | **Lifecycle audit AUD-2026-07-20, findings AUD-2026-07-20-001/003/004/005 applied — §14 self-metadata desync fixed (3rd recurrence) + shared_standards.md v3.17→v3.18 + execution_prompt.md v3.58→v3.59 + lessons_learnt_prompt.md v1.9→v1.10.** §14 Version/Last Updated table row corrected from a stale 4.102/2026-07-17 to 4.106/2026-07-21 (3 further version bumps — 4.103, 4.104, 4.105 — had all updated the document header and Change Log but never this row, a 3rd recurrence of the pattern the §9.1 guard exists to catch). §8 source prompt header v3.58→v3.59. §14 Execution Engine Source v3.58→v3.59; Shared Standards v3.17→v3.18; Lessons Learnt Prompt v1.9→v1.10. Changes: (1) `shared_standards.md` §9.1 — mechanical-enforcement note added pointing to the `commit-check` skill, since two successive prose-only strengthenings (v3.10, v3.16) both failed to prevent recurrence (AUD-2026-07-20-001); new §16.13 Sign-Off Record Schema added, canonicalising the block moved out of `execution_prompt.md` (AUD-2026-07-20-004). (2) `execution_prompt.md` §3 merge-order note — async-merge sibling notification added, closing a 3-cycle-OVERDUE deferred patch (AUD-2026-07-20-003); inline sign-off schema replaced with a reference to `shared_standards.md` §16.13 (AUD-2026-07-20-004). (3) `lessons_learnt_prompt.md` — `classification` field rule clarified to exclude undocumented values such as "monitor" (AUD-2026-07-20-005). `.github/workflows/sprint_close_reminder.yml` also extended with a sibling-PR rebase-notification step to make AUD-2026-07-20-003's prompt text true in practice. Authority: Head of Specs Team (audit AUD-2026-07-20 patch application, user-directed, 2026-07-21). |
| 4.105 | 2026-07-20 | **Post-ship closure `2026-07-20__release-v7.6` Phase 4 friction, immediate action — post_ship_closure.md v2.17→v2.18: amendment field reset rule (LL-v7.6-P4-01) added to STEP 10.** §10 source prompt header v2.17→v2.18. §14 Post-Ship Closure Engine v2.17→v2.18. §14 Version 4.104→4.105/2026-07-20. Change: STEP 10 (Global State Update) now checks whether `active_amendment` is non-empty and, if its originating cycle has already reached `Closed`/`Closed_with_actions`, clears `amended_backlog_slice_path`, `amendment_sealed_utc`, `active_amendment`, and `amendment_status` in the same write. Root cause: `.claude_current_state.json`'s `amended_backlog_slice_path` still pointed to the already-closed `2026-07-17__release-v7.4`/`AMD-20260717-01` amendment when this cycle's own delivery verification ran, requiring manual cross-referencing (checking for an `amendments/` folder under the current cycle, comparing against `execution_state.json.backlog_slice_source`) to correctly dismiss it as inapplicable — flagged as a Phase 4 friction item (`lessons_learnt_cycle.md` `2026-07-20__release-v7.6` §Phase 4) and applied now per the non-deferrable immediate-action rule rather than deferred a second time. Authority: Head of Specs Team (post-ship closure `2026-07-20__release-v7.6`, STEP 8 — immediate lessons-learnt action rule). |
|---------|------|----------------|
| 4.104 | 2026-07-20 | **Sprint execution `2026-07-20__release-v7.6` Phase 3 friction, action-now — execution_prompt.md v3.57→v3.58: API performance baseline pre-PR check added to STEP 3.2.B.** §8 source prompt header v3.57→v3.58. §14 Execution Engine Source v3.57→v3.58. §14 Version 4.103→4.104/2026-07-20. Change: new "API performance baseline pre-PR check (LL-v7.6-P3-01)" added alongside the existing qa_evidence commit advisory — if an EPIC's commits added a new `openapi.yaml` path, the engine must `grep` `docs/ops/api_performance_baseline.md` for that exact endpoint string before running `gh pr create`, registering it now (following the most recent `## N. vX.Y Endpoint Registration` section's pattern) rather than relying on the "API Performance Baseline Drift Detection (ST-12)" CI gate to catch the omission after the PR is already open. Root cause: the existing STEP 3.1.A advisory (AUD-2026-06-22-006) was insufficient under multi-file endpoint-addition load — `v7.6` ST-07 (EPIC-07) added a new `GET /ai/monthly-cost` endpoint across 8 files, missed the baseline doc specifically, and the omission was caught only by CI after PR #1035 was opened, requiring a follow-up commit before merge. Authority: PMO Lead (sprint execution `2026-07-20__release-v7.6`, STEP 5.4 Phase 3 lessons-learnt action-now rule). |
| 4.103 | 2026-07-20 | **Post-ship closure `2026-07-17__release-v7.5` STEP 8 immediate action — delivery_verification_prompt.md v3.4→v3.5 and qa_evidence_template.md v1.7→v1.8: staging-deferred Result value + agent-mediated DoQ signer provenance.** §9 source prompt header v3.4→v3.5. §14 Verification Engine Source v3.4→v3.5; QA Evidence Template v1.7→v1.8. §14 Version 4.102→4.103/2026-07-20. Changes: (1) `delivery_verification_prompt.md` STEP 2.1 — `Staging-deferred (per CLAUDE.md §2 / shared_standards.md §16.11)` added as an explicitly accepted `Result` value alongside `Pass`/`Pass with notes`/`Fail`, conditioned on a confirmed pre-PR backlog item; resolves ambiguity where the verifying pass had to reason by cross-reference that this recognised disposition was not equivalent to a blocking `Fail`. (2) `qa_evidence_template.md` Standard Sign-Off Block — new agent-mediated provenance requirement: when DoQ sign-off is performed by the engine acting in the Director of Quality role under explicit user direction, `Signed off by:` must use `Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)`, not the literal `Director of Quality` string, so true signer provenance is visible in the field itself rather than requiring cross-reference to `sprint_close.md` prose. Resolves both v7.5 Phase 4 friction items, applied now per post-ship closure's non-deferrable immediate-action rule rather than deferred. Authority: Head of Specs Team (post-ship closure `2026-07-17__release-v7.5`, STEP 8 — immediate lessons-learnt action rule). |
| 4.102 | 2026-07-17 | **Roadmap rebalance `2026-07-17__scheduled` STEP 11 Friction Item 1 — shared_standards.md v3.16→v3.17: new "Companion per-file changelog rule" added to §11.** §14 Shared Standards v3.16→v3.17. §14 Version 4.101→4.102/2026-07-17. Change: each Class 6 prompt's standalone `claude/system/changelogs/<prompt>_changelog.md` file must now be updated in the same commit as any version bump, alongside `prompt_change_log.md` — closes the gap where `changelogs/roadmap_prompt_changelog.md` fell 3 versions behind (missing 8.9, 9.0, 9.1) because no rule named it as a required companion write, even though `prompt_change_log.md` and `OPERATIONAL_GUIDE.md` §14 stayed correctly in sync throughout. Authority: Head of Specs Team (roadmap rebalance `2026-07-17__scheduled`, STEP 11). |
| 4.101 | 2026-07-17 | **Roadmap rebalance `2026-07-17__scheduled` STEP 11 — roadmap_prompt.md v9.1→v9.2: STEP 8.1 Empty Now Horizon Gate condition 1 extended to close BLG-GOV-240 (action-now).** §6 source prompt header v9.1→v9.2. §13 Artefact Register Roadmap Rebalance Prompt row v9.1→v9.2. §14 Roadmap Engine Source v9.1→v9.2. §14 Version 4.100→4.101/2026-07-17. Change: STEP 8.1 condition 1 now also fires when the Now horizon contains committed (non-shipped) items that sit only under an un-versioned carry-forward heading, not just when the horizon is fully empty — closing the gap where a non-empty-but-unversioned Now horizon (as left by `2026-07-15__release-v7.2` and `2026-07-16__release-v7.3` post-ship closures) had no governed write path to receive a formal version label. Carried forward from `2026-07-16__release-v7.3` `lessons_learnt_closure.md` Carry-Forward #1 (BLG-GOV-240), actioned at its named trigger point (next roadmap STEP 11 invocation). Authority: Head of Specs Team (roadmap rebalance `2026-07-17__scheduled`, STEP 11). |
| 4.100 | 2026-07-16 | **Post-ship closure `2026-07-16__release-v7.3` STEP 8 immediate action — qa_evidence_template.md v1.6→v1.7: OA-3/ST-03 Consolidation Block advisory elevated to a hard requirement.** §14 QA Evidence Template v1.6→v1.7. §14 Version 4.99→4.100/2026-07-16 (also corrects a found header-drift: the document's top `**Version:**`/`**Last Updated:**` fields were still at 4.98/2026-07-15 despite the 4.99 Change Log entry below and the §14 field-table already reading 4.99/2026-07-16 — that correction was never applied to the top header fields; both the missed 4.99 bump and this cycle's own change are reflected in this single 4.100 update). Change: every AC in the backlog slice must now appear in the QA evidence table — as its own row, or named explicitly in a consolidated row's Evidence column — with no AC permitted to be silently absent even when functionally addressed elsewhere in the log. Resolves the Phase 4 deferred patch recorded in `claude/cycles/2026-07-16__release-v7.3/lessons_learnt_cycle.md` (qa_evidence_EPIC-01.md ST-02's evidence table silently dropped AC-03), applied now per post-ship closure's non-deferrable immediate-action rule rather than deferred. Authority: Head of Specs Team (post-ship closure `2026-07-16__release-v7.3`, STEP 8 — immediate lessons-learnt action rule). |
| 4.99 | 2026-07-16 | **Roadmap rebalance `2026-07-16__scheduled` STEP 11 — roadmap_prompt.md v9.0→v9.1: STEP 3.1 Actionable Backlog Assessment scale-appropriate methodology codified (action-now, no longer deferred).** §6 source prompt header v9.0→v9.1. §13 Artefact Register Roadmap Rebalance Prompt row v9.0→v9.1. §14 Roadmap Engine Source v9.0→v9.1. §14 Version 4.98→4.99/2026-07-16. Change: `roadmap_prompt.md` STEP 3.1 — a grep-based structural heuristic (presence/absence of the `**Gate criteria:**` field for the A/gated split; keyword-pattern scan of gate-criteria text for the T/D/L split) is now the codified method once the active backlog reaches ~150 items, replacing the manual per-item read used below that scale; the run manifest must record which method was used so cross-cycle A% figures aren't compared across a silent methodology change. Confirmed on a 2nd consecutive occurrence at this cycle (319-item backlog) after the deferred patch from `2026-07-15__scheduled` Friction Item 2 named a 2nd occurrence as the trigger to codify rather than re-defer. Closes that deferred patch. Authority: Head of Specs Team (roadmap rebalance `2026-07-16__scheduled`, STEP 11). |
| 4.98 | 2026-07-15 | **Post-ship closure `2026-07-15__release-v7.2` STEP 8 — execution_prompt.md v3.56→v3.57 (LL-v7.2-P3-01, Phase 3 Friction Log deferred patch, action-now).** §8 source prompt header v3.56→v3.57. §14 Execution Engine Source v3.56→v3.57. Change: new "Session-start divergence check" added at the very top of STEP -1 (before the existing "First action" read), plus a companion step 0 in §10 Resumability — `git fetch origin` + local-vs-`origin/main` comparison must run before any local state file (`.claude_current_state.json`, `execution_state.json`) is trusted, generalising the existing LL-v3.9-P3-1 resume-sync pattern (previously scoped only to STEP 4's merge-gate) to the start of the routine. Root cause: this cycle's own first `run sprint` invocation read stale local state as if only the EPIC-01 planning stub existed, when 4 EPICs' worth of engine-autonomous work already existed on `origin/main` from an earlier unsynced session — causing a duplicate `execution_state.json` re-initialisation and 5 duplicate GitHub issues (#993–#997) before the mismatch was caught mid-session and reconciled. Closes the Phase 3 deferred patch recorded in `claude/cycles/2026-07-15__release-v7.2/lessons_learnt_cycle.md`. Authority: Head of Specs Team (post-ship closure `2026-07-15__release-v7.2`, STEP 8 — immediate lessons-learnt action rule). |
| 4.97 | 2026-07-15 | **Roadmap rebalance `2026-07-15__scheduled` STEP 11 — roadmap_prompt.md v8.9→v9.0: STEP 4.2 Idea Consolidation convention codified (action-now, no longer deferred).** §6 source prompt header v8.9→v9.0. §13 Artefact Register Roadmap Rebalance Prompt row v8.9→v9.0. §14 Roadmap Engine Source v8.9→v9.0. §14 Version 4.96→4.97/2026-07-15. Change: `roadmap_prompt.md` STEP 4.2 — the ad hoc "Idea Consolidation" convention used at `2026-07-13__scheduled` (invented without a governing rule, deferred pending a 2nd confirming clustering instance) is now formalised: when N idea submissions converge on the same feature/problem area, the Facilitator may file one consolidated backlog item (Source field lists every contributing Idea ID; each register row's Step 5 column names the consolidated item explicitly). Confirmed generalisable after a 2nd independent clustering event this cycle (22 of 44 `IW-20260715-01` submissions on 5 ad-hoc-added items, consolidated into 4 backlog items). Closes the deferred patch from `2026-07-13__scheduled` lessons learnt (STEP 4.2 Idea Consolidation). Authority: Head of Specs Team (roadmap rebalance `2026-07-15__scheduled`, STEP 11). |
| 4.96 | 2026-07-14 | **Lifecycle audit AUD-2026-07-14, finding AUD-2026-07-14-001 applied — §14 self-metadata desync fixed (recurrence) + shared_standards.md v3.15→v3.16.** §14 Version/Last Updated table row corrected from a stale 4.93/2026-07-13 to 4.96/2026-07-14 — the 4.94/4.95 entries below had bumped the top document header and Change Log but never updated the §14 table's own `Version`/`Last Updated` value row, a further recurrence of the exact header-drift pattern this section's own drift-prevention note (added v4.85) exists to catch, and which the `shared_standards.md` §9.1 guard (added 2026-07-10 specifically to prevent it) failed to stop since that note covered the Change Log top row but not the §14 field-table's own summary row. §14 Shared Standards v3.15→v3.16. Change: `shared_standards.md` §9.1 rewritten from a single prose paragraph into an explicit 3-step Before/After checklist, adding a distinct required check-point for a document's own self-referential summary table (e.g. this file's §14) separate from its Change Log top row — modelled on the §7.1 Structural Append-Verification Procedure. Closes AUD-2026-07-14-001. Authority: Head of Specs Team (audit AUD-2026-07-14 patch application, 2026-07-14). |
| 4.95 | 2026-07-14 | **PMO Lead direct action — resolved outstanding action #2 from `2026-07-14__release-v7.1` post-ship closure (Release Planning Carry-Forward #2: capacity check landed at top of band with zero buffer, and a genuine either/or risk fix-vehicle choice was deferred to execution kickoff).** §7 source prompt header v3.12→v3.13. §14 Sprint Planning Engine v3.12→v3.13. §14 Version 4.94→4.95/2026-07-14. Changes: `sprint_planning_prompt.md` STEP 0 — new "Phasing Recommendation as a live option" (LP-14) requiring the Product Owner's capacity-WARN acknowledgement to explicitly Adopt or Decline any `### Phasing Recommendation` present in `release_plan.md`, not merely acknowledge the WARN in the abstract. STEP 5.3 Risk Flags — new "Multi-vehicle fix-choice risk check" (LP-14) requiring Sprint Planning to identify risk-register items whose mitigation names multiple genuinely alternative fix vehicles with differing effort, and cross-reference them against the Phasing Recommendation at planning time rather than silently deferring the sizing uncertainty to execution. Closes outstanding action #2 from `claude/cycles/2026-07-14__release-v7.1/closure_record.md` §6. Authority: PMO Lead (direct action, user-invoked, 2026-07-14). |
| 4.94 | 2026-07-14 | **Head of Specs Team direct action — resolved escalated decision from `2026-07-14__release-v7.1` post-ship closure (Release Planning Friction Item 1: bare-letter backlog effort bands forcing capacity-check inference by analogy).** §6 source prompt header v8.8→v8.9. §6M source prompts updated (backlog_management_prompt.md v1.11→v1.12). §13 Artefact Register Roadmap Rebalance Prompt row v8.8→v8.9. §14 Roadmap Engine Source v8.8→v8.9; Backlog Management Engine v1.11→v1.12; Shared Standards v3.14→v3.15. §14 Version 4.93→4.94/2026-07-14. Decision: **Yes** — root-caused to `roadmap_prompt.md` STEP 4.2's `📋 Backlog (gate-conditional)` disposition path, which bypasses STEP 6 (Scoring Matrix Overlay) — the only place the existing S/M/L day-range convention (§16.7) was documented — so items filed via STEP 4.2 routinely landed with a bare letter and no range. Changes: (1) `shared_standards.md` new §16.12 — canonical day-range requirement for the backlog item `**Effort:**` field, required whenever `Provisional-Target` names a specific release. (2) `roadmap_prompt.md` STEP 4.2 and STEP 9 — day-range now required at write time when disposing/promoting an item with a specific `Provisional-Target`. (3) `backlog_management_prompt.md` STEP 1 — new §1.2 Effort Day-Range Validation pre-scan, flagging (not auto-backfilling) existing non-compliant items at grooming time. Closes outstanding action #1 from `claude/cycles/2026-07-14__release-v7.1/closure_record.md` §6. Authority: Head of Specs Team (direct action, user-invoked, 2026-07-14). |
| 4.93 | 2026-07-13 | **Roadmap rebalance `2026-07-13__scheduled` STEP 11 — roadmap_prompt.md v8.7→v8.8 — plus a live §14 table drift correction found this cycle.** §6 source prompt header v8.7→v8.8. §13 Artefact Register Roadmap Rebalance Prompt row v8.7→v8.8. §14 Roadmap Engine Source v8.7→v8.8. §14 **Version/Last Updated table row corrected from a stale 4.91/2026-07-10 to 4.93/2026-07-13** — the 4.92/2026-07-12 entry below had bumped the top document header and this Change Log but never actually updated the §14 table's own `Version`/`Last Updated` value rows, a 5th recurrence of the exact header-drift pattern this section's own drift-prevention note (added v4.85) exists to catch; caught this cycle by direct comparison against the top header rather than trusting the table row in isolation. Change: `roadmap_prompt.md` STEP -1.5 — "condition-gated defer exemption" clause added, exempting recurrence-conditioned deferred patches (Target = a condition, not a date/cycle_id) from the cycle-count OVERDUE mechanism; introduces a 6+-consecutive-carry "Stale Condition-Gated Defer" advisory instead. Closes an ambiguity that had been implicitly treated as an exemption across 3 prior scheduled cycles without ever being codified. Authority: Head of Specs Team (roadmap rebalance `2026-07-13__scheduled`, STEP 11). |
| 4.92 | 2026-07-12 | **Roadmap rebalance `2026-07-12__scheduled` STEP 11 — roadmap_prompt.md v8.6→v8.7.** §6 source prompt header v8.6→v8.7. §13 Artefact Register Roadmap Rebalance Prompt row v8.5→v8.7 (also corrects a pre-existing drift found this cycle: this table's row read v8.5 while §14's own row already read v8.6). §14 Roadmap Engine Source v8.6→v8.7. §14 Version 4.91→4.92/2026-07-12. Changes: (1) `roadmap_prompt.md` §6 — same-day `cycle_id` collision auto-suffix rule added, closing a confirmed live overwrite risk (a second same-day scheduled rebalance collided with the morning's already-`Filed` cycle folder; resolved ad hoc via user confirmation before this rule existed). (2) `roadmap_prompt.md` STEP -1.5 — "out-of-scope OVERDUE resolution" clause added: once a named authority holds a standing out-of-band write privilege for an OVERDUE patch's target file (`shared_standards.md` §17), that is no longer a valid reason to keep re-carrying the patch — the escalation must instruct direct application under that authority. Closes the gap where the `CLAUDE.md` §6 patch was correctly flagged OVERDUE for 6 consecutive cycles but never actually applied. Authority: Head of Specs Team (roadmap rebalance `2026-07-12__scheduled`, STEP 11). |
| 4.91 | 2026-07-10 | **Lifecycle audit AUD-2026-07-10, finding AUD-2026-07-10-001 applied — shared_standards.md v3.13→v3.14: new companion `CLAUDE.md` write authority provision added directly after §17.** §14 Shared Standards v3.13→v3.14. §14 Version 4.90→4.91/2026-07-10. Change: no governed routine's write scope included `CLAUDE.md` itself (confirmed absent from `roadmap_prompt.md`'s write-scope text), leaving a `CLAUDE.md` §6 Governance File Edit Checklist amendment carried unresolved across 5 consecutive scheduled-rebalance cycles (2026-07-01 through 2026-07-10) — the same shape as the `.claude/skills/` gap §17 already resolved. `shared_standards.md` §17 now also grants the Head of Specs Team standing write authority over `CLAUDE.md`, independent of any single engine's per-run Write Scope. Closes the 5-cycle carry-forward escalation. Authority: Head of Specs Team (audit AUD-2026-07-10 patch application, 2026-07-10). |
| 4.90 | 2026-07-10 | **Post-ship closure `2026-07-10__release-v6.9` STEP 8 — execution_prompt.md v3.55→v3.56.** §8 source prompt header v3.55→v3.56; §14 Execution Engine Source v3.55→v3.56. Change: STEP 3.1.A API performance baseline advisory (AUD-2026-06-22-006) path corrected `docs/operations/api_performance_baseline.md` → `docs/ops/api_performance_baseline.md` (the path that actually exists); reclassified from "advisory (not a hard gate)" since `quality_gate.yml`'s "API Performance Baseline Drift Detection (ST-12)" already hard-blocks the PR on this omission — confirmed this cycle when both EPIC-01 and EPIC-02 PRs failed CI on first push for exactly this reason. This entry backfills a row missed when the header was bumped without updating this table (found and corrected by lifecycle audit AUD-2026-07-10, AUD-2026-07-10-002 — §14 self-row and this table's top row were both left at 4.89 despite the header already reading 4.90). Authority: Head of Specs Team (post-ship closure 2026-07-10__release-v6.9, STEP 8; table backfill via AUD-2026-07-10-002). |
| 4.89 | 2026-07-10 | **Roadmap rebalance `2026-07-10__scheduled` — 1 due deferred patch resolved + 1 meta-review patch applied.** §6 source prompt header v8.5→v8.6. §14 Roadmap Engine Source v8.5→v8.6; Shared Standards v3.12→v3.13. §14 Version 4.88→4.89/2026-07-10. Changes: (1) `roadmap_prompt.md` STEP 6 — overwrite-verification instruction added (read-before-write + re-read-after-write check), resolving the deferred patch from `2026-07-08__scheduled` Friction Item 1 (target: "next `run roadmap` invocation"). (2) `shared_standards.md` §9 — new §9.1 version/state header cross-check note added via STEP 11.4 meta-review (3-cycle review, due at this cycle): generalises the recurring Type A Governance Drift pattern (`scored_initiatives.md` accumulation, `OPERATIONAL_GUIDE.md` header-vs-table lag ×4, backlog gate-field-label synonym) into one reusable pre-write check. The companion deferred patch to `CLAUDE.md` §6 (same root pattern, outside this engine's write scope) remains carried forward unchanged — no session with direct `CLAUDE.md` write authorisation has occurred yet. Authority: Head of Specs Team (roadmap rebalance `2026-07-10__scheduled`, STEP 11/11.4). |
| 4.88 | 2026-07-09 | **PMO Lead / Head of Specs Team direct action — resolved 5 outstanding items from `2026-07-08__release-v6.8` post-ship closure (3 recorded Outstanding Actions + 2 Advisory Summary findings).** §6 source prompt header v8.4→v8.5. §6M source prompts (`ideas_housekeeping_prompt.md`) v1.0→v1.1. §8 source prompt header v3.54→v3.55. §9 source prompt header v3.3→v3.4. §13 Artefact Register Roadmap Rebalance Prompt row v8.4→v8.5. §14 Roadmap Engine Source v8.4→v8.5; Execution Engine Source v3.54→v3.55; Verification Engine Source v3.3→v3.4; Ideas Housekeeping Engine v1.0→v1.1; Shared Standards v3.11→v3.12. §14 Version 4.87→4.88/2026-07-09. Changes: (1) `execution_prompt.md` STEP 4 — new step 3a0 checks out `main` before the 3a/3b state-sync and governance-file commits, which now push to `main` directly instead of the just-merged EPIC branch; closes the LL-v6.8-P3-01 root cause (Phase 3 friction item 2, v6.8). (2) `execution_prompt.md` STEP 3.1.A — new Case E + structured `spec_reference_not_applicable`/`spec_reference_not_applicable_reason` fields (also added to `execution_state_schema.json`), replacing the undocumented `notes: "no prior spec applicable"` convention; `delivery_verification_prompt.md` STEP 1.3 updated to check the structured field first, falling back to the legacy notes-string for pre-existing records (v6.8 Phase 4 friction item). (3) `shared_standards.md` §16.5 — formalised `Promoted-Backlog` as a canonical `ideas_register.md` status (found in continuous multi-cycle use by `roadmap_prompt.md` but absent from the enum); `ideas_housekeeping_prompt.md` §6.1 updated to classify it as archive-eligible; `roadmap_prompt.md` STEP -1.6 exclusion-list prose corrected to match. 40 previously-held-back `Promoted-Backlog` rows in `ideas_register.md` archived as a result. (4) `claude/backlog/backlog.md` — filed `BLG-BE-52` (LP-12: formal disposition for `BLG-BE-46`'s 11 permanently-unlinked historical `trade_plans` rows, which had no tracking item). (5) `claude/ideas/rejected_but_strong.md` — `IDEA-cybersecurity-20260304-01` (System Threat Model) marked Resolved; delivered as `BLG-OPS-71`/ST-17 in v6.8. Authority: PMO Lead + Head of Specs Team (direct action, user-invoked, 2026-07-09). |
| 4.87 | 2026-07-09 | **v6.8 sprint close (STEP 5.4 lessons learnt, LL-v6.8-P3-01) — execution_prompt.md v3.53→v3.54: orphaned post-merge commit check added to STEP 4.** §8 source prompt header v3.53→v3.54. §14 Execution Engine Source v3.53→v3.54. §14 Version 4.86→4.87/2026-07-09. Change: this sprint's close found that all three EPIC branches (v6.8) received one or more commits after their own PR had already merged into main — these orphaned commits never entered `main` via the merge diff. EPIC-03's orphaned `execution_state.json` merge-state commit had not reached `main` and required manual reconciliation at sprint close; EPIC-01/EPIC-02's orphaned commits (execution_state.json state-persist; two backlog.md filings, BLG-SPEC-71/72) were found to already be present on `main` in equivalent form, but only incidentally (via a later EPIC branch's rebase), not by any designed mechanism. STEP 4's existing LL-v3.9-P3-1 resync only covers `execution_state.json`'s own `merge_gate` fields. Added a new check (LL-v6.8-P3-01) immediately after it: on merge-gate resume, `git fetch origin` then diff `origin/main..origin/exec/<cycle_id>/<epic_id>` for every merged EPIC; reconcile any orphaned governance-file commit onto `main` directly (commit format `[EPIC-xx] Reconcile orphaned post-merge commit <sha> onto main`), recording each check in a new `execution_state.json.process_notes` array that STEP 5.3 rolls up into `sprint_close.md`'s Process Notes section (added a corresponding bullet to STEP 5.3's "Must include" list). Reviewed and confirmed non-duplicative of LL-v3.9-P3-1, LL-v2.0-P3-5, and CLAUDE.md §8 by Head of Specs Team (agent-mediated review, per execution_prompt.md §5.3) before being applied as an action-now patch. **Separate observation filed as a follow-up, not actioned this patch:** STEP 4's own steps 3a/3b instruct committing `execution_state.json`/governance files to the EPIC branch *after* the PR has already merged — this is the root cause generating an orphaned commit on essentially every merge, not an edge case; a future revision should have 3a/3b commit onto `main` directly instead. Authority: Head of Specs Team (agent-mediated sign-off, v6.8 sprint close, 2026-07-09). |
| 4.86 | 2026-07-09 | **v6.8 ST-16 (BLG-GOV-123, EPIC-03) — execution_prompt.md §14 Playwright Test Authoring Standard extracted to shared_standards.md §18.** §8 source prompt header v3.52→v3.53. §14 Execution Engine Source v3.52→v3.53. §14 Shared Standards v3.10→v3.11. §14 Version 4.85→4.86/2026-07-09. Change: the Playwright Test Authoring Standard (waitFor patterns, mock payload advisory) applies to Playwright tests written by any governed routine, not just sprint execution — moved to the cross-engine shared_standards.md as new §18, with execution_prompt.md §14 replaced by a reference line. Also folds in a new route-ordering advisory discovered during the same sprint's ST-11 (BLG-QA-64): page.route() handlers evaluate in reverse registration order; route.continue() sends to the real network rather than falling through to an earlier-registered handler — use route.fallback() to defer correctly. Authority: Head of Specs Team (v6.8 ST-16, 2026-07-09). |
| 4.85 | 2026-07-08 | **Roadmap rebalance 2026-07-08__scheduled — 2 further friction-item patches applied same cycle.** §14 Shared Standards v3.9→v3.10. §14 Version 4.84→4.85/2026-07-08. Changes: (1) `shared_standards.md` §16.5 — clarified that `Promoted-Added` status also covers a STEP 5 debate resolving into a process patch rather than a roadmap/backlog addition (this reuse had recurred twice, `2026-07-06__scheduled` and `2026-07-08__scheduled`, without being documented — Type B Semantic Mismatch). (2) This document — added a header-drift prevention note directly above this Change Log table (4th recurrence of the header-Version-field-lagging-the-table pattern, per the 4.79/4.80/4.81 entries below); future edits should read the table's own top row rather than trusting the header field. Authority: Head of Specs Team (roadmap rebalance 2026-07-08__scheduled, STEP 11). |
| 4.84 | 2026-07-08 | **Roadmap rebalance 2026-07-08__scheduled — resolved 2 deferred patches carried from `2026-07-06__scheduled` lessons learnt (one re-routed via `2026-07-06__release-v6.7` closure LP-09).** §6 source prompt header updated v8.3→v8.4. §6M source prompts updated (backlog_management_prompt.md v1.10→v1.11). §13 Artefact Register Roadmap Rebalance Prompt row updated v8.3→v8.4. §14 Roadmap Engine Source v8.3→v8.4; Backlog Management Engine v1.10→v1.11. §14 Version 4.83→4.84/2026-07-08 (also corrects a repeat of the header-drift pattern flagged in the 4.79/4.80/4.81 entries below: the top `**Version:**`/`**Last Updated:**` fields were still at 4.80 despite the 4.81/4.82/4.83 Change Log entries below recording that they had been bumped further — those corrections were never actually applied to the header fields; the missed bumps and this cycle's own change are reflected in this single 4.84 update). Changes: (1) `roadmap_prompt.md` STEP 2.3 — added SI-02 gate read instruction pointing to a new structured `**Last formally confirmed:**`/`**Unverified report:**` sub-field on the SI-02 row in `current_roadmap.md` §5, resolving the trade-count reconciliation gap (Friction Item 2, `2026-07-06__scheduled`; misrouted to `plan release v6.7` by that cycle, corrected to this engine by `2026-07-06__release-v6.7` closure LP-09). (2) `backlog_management_prompt.md` STEP 1 — new §1.1 Gate Field Label Normalization mandatory pre-scan, closing Friction Item 1 (`2026-07-06__scheduled`): 3 backlog items (`BLG-QA-63`, `BLG-OPS-76`, `BLG-OPS-77`) plus 1 ungated item (`BLG-QA-64`) were found still using the non-canonical `**Gate:**` label and silently excluded from the roadmap engine's STEP 3.1 gated-item scan; all 4 normalised to `**Gate criteria:**` directly in `backlog.md` this run. Authority: Head of Specs Team (roadmap rebalance 2026-07-08__scheduled, STEP -1.5 prior-cycle outstanding actions). |
| 4.83 | 2026-07-06 | **v6.7 ST-07 (EPIC-02, BLG-GOV-170) — delivery_verification_prompt.md v3.2→v3.3: STEP 6 now documents the System Status Report status-line update as an expected step.** §9 source prompt header v3.2→v3.3. §14 Verification Engine Source v3.2→v3.3. §14 Version 4.82→4.83/2026-07-06. Change: STEP 6 (System Status Report Reconciliation) — added explicit sub-step naming the `**Status:**` line transition (`Sprint_Complete — pending verification` → `Verified — <date>` / `Verified_with_deviations — <date>`) as routine, expected behaviour on every verification run; states this must not be logged as friction in `lessons_learnt_cycle.md`. This update was correctly performed every cycle but had gone undocumented in the engine's own STEP 6 text for 4+ consecutive cycles, repeatedly re-surfacing as a "new" friction item at lessons-learnt time instead of being recognised as expected. Authority: Head of Specs Team (v6.7 ST-07, BLG-GOV-170, 2026-07-06). |
| 4.82 | 2026-07-06 | **v6.7 ST-05 (EPIC-02, BLG-GOV-168) — shared_standards.md v3.8→v3.9: new §7.1 canonical Structural Append-Verification Procedure, applied to all 4 append-only governance logs.** §6B source prompt header v2.41→v2.42; §8 source prompt header v3.51→v3.52; §9 source prompt header v3.1→v3.2. §14 Shared Standards v3.8→v3.9; Release Engine Source v2.41→v2.42; Execution Engine Source v3.51→v3.52; Verification Engine Source v3.1→v3.2. §14 Version 4.81→4.82/2026-07-06. Change: closes BLG-GOV-168 — the prior §7 "structural verification requirement" note was prose-only and produced zero engine adoptions. `shared_standards.md` §7.1 now defines one reusable count-before/after + no-prior-entry-changed procedure (generalising the existing `decision_log.md` guard) with an explicit file→owning-engine table; `release_planning_prompt.md` (escalations.md), `execution_prompt.md` (execution_escalations.md §"ESCALATION HANDLING SUBROUTINE" + delegation_log.md §11), and `delivery_verification_prompt.md` (verification_escalations.md) each now carry an explicit "Apply the Structural Append-Verification Procedure per shared_standards.md §7.1" line at their write step — confirmed via direct read of each, not documentation alone. Authority: Head of Specs Team (v6.7 ST-05, BLG-GOV-168, 2026-07-06). |
| 4.81 | 2026-07-06 | **v6.7 ST-04 (EPIC-02, BLG-GOV-167) — shared_standards.md v3.7→v3.8: new §17 `.claude/skills/` write authority provision, naming Head of Specs Team.** §14 Shared Standards v3.7→v3.8. §14 Version 4.79→4.81/2026-07-06 (also corrects a repeat of the header-drift pattern: the top `**Version:**`/`**Last Updated:**` fields were still at 4.79 despite the 4.80 Change Log entry below claiming the header had been updated to 4.80 — that correction was never actually applied to the header fields; both the missed 4.80 bump and this cycle's own v6.7 ST-04 change are reflected in this single 4.81 update). Change: closes the 3-cycle-carried (v6.4→v6.5→v6.6) `.claude/skills/commit-check/SKILL.md` diff-verification patch escalation (`ESC-CLOSE-20260706-01`) — no governed engine's Write Scope covered `.claude/skills/`, so the deferred patch had no governed path to landing. `shared_standards.md` §17 now grants the Head of Specs Team standing write authority over `.claude/skills/**` independent of any single engine's per-run Write Scope; `.claude/skills/commit-check/SKILL.md` Check 9 (diff-verification: staged set vs. intended file set for multi-file governance commits) added in the same story. Authority: Head of Specs Team (v6.7 ST-04, BLG-GOV-167, 2026-07-06). |
| 4.80 | 2026-07-06 | **Roadmap rebalance 2026-07-06__scheduled — resolved deferred patch (`lessons_learnt_closure.md` v6.6, Carry-Forward #2) via STEP 5 debate — roadmap_prompt.md v8.2→v8.3.** §6 source prompt header updated v8.2→v8.3. §13 Artefact Register Roadmap Rebalance Prompt row updated v8.2→v8.3. §14 Roadmap Engine Source v8.2→v8.3. §14 Version 4.78→4.80/2026-07-06 (also corrects a found header-drift: this document's top `**Version:**` field was left at 4.78 when the 4.79 entry below was added at v6.6 post-ship closure — the Change Log table was updated but the header field was not; both the missed 4.79 bump and this cycle's own change are reflected in this single 4.80 update). Change: `roadmap_prompt.md` §7.1 — added "Mandatory pull-forward on sustained failure": after 3+ consecutive worsening/unresolved rolling-3-cycle Skill-Silo readings, the pull-forward recommendation becomes mandatory (PO must commit ≥2 build-and-ship-shaped U-items at the next release; audit/investigation-shaped stories do not count per the STEP 2.4 content-based test). Closes the gap where v6.5 and v6.6 each bundled 2 nominal U-items but only 1 resolved to genuine U at ship in both cases. Authority: Head of Specs Team (STEP 5.2 PO Modify decision, roadmap rebalance 2026-07-06__scheduled). |
| 4.79 | 2026-07-06 | **Post-ship closure 2026-07-04__release-v6.6 STEP 8 immediate actions — release_planning_prompt.md v2.40→v2.41 (LP-01) + roadmap_prompt.md v8.1→v8.2 (LP-05).** §6B source prompt header updated v2.40→v2.41. §6 source prompt header updated v8.1→v8.2. §13 Artefact Register Roadmap Rebalance Prompt row updated v8.1→v8.2. §14 Release Engine Source v2.40→v2.41. §14 Roadmap Engine Source v8.1→v8.2. §14 Version 4.78→4.79/2026-07-06. Changes: (LP-01, resolves 2-cycle recurrence v6.5→v6.6) release_planning_prompt.md STEP 4.1 no longer writes `design_gate_required`/`design_gate_status` directly to `.claude_current_state.json` — writes `state.json` only; STEP 7's intermediate sync now carries these fields into `.claude_current_state.json` atomically with `active_cycle`, closing the transient window where the new cycle's design-gate write could overwrite the just-closed prior cycle's own completed design-gate record before `active_cycle` had advanced. (LP-05) roadmap_prompt.md §7.1 Skill-Silo Alert — pull-forward candidate selection now requires reading the candidate's own `**Gate criteria:**` backlog line and confirming it is met/near-term before naming it; unmet-gate candidates must be flagged `[gate status unverified/unmet]` rather than named silently. Fixes the gap that let `2026-07-03__scheduled` name BLG-FEAT-52 as a candidate despite its own unmet PO-02 gate. Authority: Head of Specs Team (v6.6 post-ship closure, 2026-07-06). |
| 4.78 | 2026-07-06 | **v6.6 ST-03 (BLG-QA-72, EPIC-02) — backlog_management_prompt.md v1.9→v1.10: STEP 4.5 ID Uniqueness Scan §6.1 stub+verbatim exemption added.** §6M source prompt header updated v1.9→v1.10. §14 Backlog Management Engine v1.9→v1.10. §14 Version 4.77→4.78/2026-07-06. Change: STEP 4.5 now excludes the §6.1 archive format's compliant stub+verbatim header pair (same ID, same title, retirement stub immediately preceding the verbatim copy) from the duplicate-ID count — only flags IDs appearing >2 times, or twice with differing titles, or twice without the stub marker. Root cause: the prior scan flagged all §6.1-format archived entries as duplicates by design, producing a permanent false-positive baseline (~29 legitimate pairs) that made "0 unresolved duplicate IDs" unreachable; confirmed via direct audit that of the 39 IDs with >1 `###` header found across backlog.md/backlog_archive.md, 29 were compliant §6.1 pairs, 10 were genuine collisions (different items sharing one ID — renumbered in the same commit: BLG-FE-66/67, BLG-GOV-69/70/71/72/73/74, BLG-OPS-12/13 → new IDs BLG-FE-85/86, BLG-GOV-161–166, BLG-OPS-86/87), and a further 5 (BLG-FE-49, BLG-FEAT-38, BLG-OPS-28/31/37) were the same item archived twice under two different historical archive conventions — flagged as a follow-up dedup item, not renumbered (renumbering would incorrectly imply two different items). Authority: Head of Specs Team (v6.6 ST-03, BLG-QA-72, 2026-07-06). |
| 4.77 | 2026-07-03 | **Roadmap rebalance 2026-07-03__scheduled STEP 11.4 meta-review action-now — roadmap_prompt.md v8.0→v8.1: STEP 2.4 now reads the inline U/G/D/P ship-time tag (post_ship_closure.md v2.17) instead of re-deriving it, when present.** §6 source prompt header updated v8.0→v8.1. §13 Artefact Register Roadmap Rebalance Prompt row updated v8.0→v8.1. §14 Roadmap Engine Source v8.0→v8.1. §14 Version 4.76→4.77/2026-07-03. Change: closes the read-side gap left by the write-side patch applied earlier this same cycle (post_ship_closure.md v2.17) — without this, the newly-written ship-time tags would never actually be consulted, and STEP 2.4 would keep re-deriving classifications by judgment even for tagged cycles. Fall-back to judgment-based classification retained for untagged (pre-v6.6) cycles. Identified at STEP 11.4 meta-review (3-cycle trigger, `2026-06-26__scheduled` → this cycle) as a Type B (Semantic Mismatch) pattern spanning 2+ consecutive cycles. Authority: Head of Specs Team (roadmap rebalance 2026-07-03__scheduled meta-review). |
| 4.76 | 2026-07-03 | **Roadmap rebalance 2026-07-03__scheduled — resolved deferred patch (Friction Item 3, `2026-07-02__scheduled` lessons learnt) — post_ship_closure.md v2.16→v2.17: Tech backlog items shipped lines now require an inline `[U\|G\|D\|P]` classification tag.** §10 source prompt header updated v2.16→v2.17. §14 Post-Ship Closure Engine v2.16→v2.17. §14 Version 4.75→4.76/2026-07-03. Change: STEP 1.1 entry template and STEP 1.2 entry rules updated so each shipped story is tagged `U`/`G`/`D`/`P` at the point the changelog entry is written, using `roadmap_prompt.md` STEP 2.4's classification schema — removes the reconstruction-variance risk of re-deriving these tags from prose each time the Product Value Ratio Diagnostic runs. Deferred patch's own named target was "`2026-07-05__scheduled` or next roadmap rebalance, whichever comes first" — this cycle is that next rebalance, so applied action-now rather than deferred again. Authority: Head of Specs Team (roadmap rebalance 2026-07-03__scheduled, acting on the patch's own arrived target date). |
| 4.75 | 2026-07-03 | **Post-ship closure 2026-07-02__release-v6.5 self-identified closure-phase friction — post_ship_closure.md v2.15→v2.16: STEP 2/STEP 11 roadmap-retirement boundary clarified.** §10 source prompt header updated v2.15→v2.16. §14 Post-Ship Closure Engine v2.15→v2.16. §14 Version 4.74→4.75/2026-07-03. Change: STEP 2 (Roadmap Update) gained a clarifying note that the `*RA:<release> retired...*` annotation line is written by STEP 11 (roadmap_management_prompt.md), not STEP 2 — prevents a premature write recording an archival that has not yet happened. Caught and self-corrected during this cycle's own STEP 2 (v6.5 roadmap update) before commit; patched at source per the non-deferrable immediate-action rule rather than left as a one-off correction. See `claude/cycles/2026-07-02__release-v6.5/lessons_learnt_closure.md` Friction Log. Authority: Head of Specs Team (v6.5 post-ship closure, 2026-07-03). |
| 4.74 | 2026-07-03 | **Post-ship closure 2026-07-02__release-v6.5 STEP 8 immediate actions — release_planning_prompt.md v2.39→v2.40 (LP-02, LP-03).** §6B source prompt header updated v2.39→v2.40. §14 Release Engine Source v2.39→v2.40. §14 Version 4.73→4.74/2026-07-03. Changes: (LP-02, Release Planning lessons_learnt.md Friction Item 2) STEP 5 Roadmap Annotation — added explicit fallback wording: if no formal `## vX.Y` roadmap section exists for the release, annotate the `**Next planned release:**` line in §1 (Current Version) instead. (LP-03, Friction Item 3) §1.4a Perennial-Return Check — added a third named disposition option "(c) Resolve directly this cycle" for low-effort items where the cheapest fix is closure rather than further deferral or parking. LP-01 (STEP 4.1/STEP 7 state-sync sequencing) and LP-04 (Skill-Silo monitoring) deferred — see `claude/cycles/2026-07-02__release-v6.5/closure_record.md` §5. Authority: Head of Specs Team (v6.5 post-ship closure, 2026-07-03). |
| 4.73 | 2026-07-03 | **Sprint execution 2026-07-02__release-v6.5 STEP 5.4 action-now — execution_prompt.md v3.50→v3.51: STEP 4 resume-sync branch check added (LL-v6.4-P3-01).** §8 source prompt header v3.50→v3.51. §14 Execution Engine Source v3.50→v3.51. §14 Version 4.72→4.73/2026-07-03. Change: STEP 4's "on session resume — merge gate state sync" sub-step now requires an explicit `git branch --show-current` check (and `git checkout main && git pull` if not already on `main`) before performing the merge-gate sync write, mirroring STEP 5's branch-ordering gate. Resolves a deferred v6.4 Phase 3 lessons-learnt friction item targeted at v6.5 (this cycle) — a fresh session resuming after an EPIC merge could previously land on any `exec/**` branch and orphan the sync write there. Applied action-now during this cycle's own STEP 5.4 rather than deferred again, per §6.2. Authority: Head of Specs Team (sprint execution 2026-07-02__release-v6.5, 2026-07-03). |
| 4.72 | 2026-07-02 | **Roadmap rebalance 2026-07-02__scheduled — roadmap_prompt.md v7.9→v8.0: three lessons-learnt patches applied.** §6 source prompt header updated v7.9→v8.0. §13 Artefact Register Roadmap Rebalance Prompt row updated v7.9→v8.0. §14 Roadmap Engine Source v7.9→v8.0. §14 Version 4.71→4.72/2026-07-02. Changes: (1, Friction Item 2 deferred patch from `2026-07-01__scheduled`, due this cycle) STEP 11.2 — deferred-patch Target fields must name a cycle_id or absolute date, not a bare release version alone; if a release version is given, a concrete date estimate must also be recorded. (2, this cycle's Friction Item 1) STEP 4.0 gate-condition re-check — explicit two-step check added (grep `backlog.md`, then `backlog_archive.md` before concluding "not shipped"); corrects the false-negative that let `2026-07-01__scheduled` record BLG-GOV-131 as unshipped when it had in fact shipped v6.1. (3, this cycle's Friction Item 3) STEP 7.1 Skill-Silo Alert — wording clarified that a single U-item pull-forward is not guaranteed to correct the rolling ceiling breach across a heavy governance/debt window; PO should consider multiple U-items after 2+ consecutive Alert cycles. Authority: Head of Specs Team (roadmap rebalance 2026-07-02__scheduled). |
| 4.71 | 2026-07-02 | **Post-ship closure 2026-07-02__release-v6.4 STEP 8 immediate action — execution_prompt.md v3.49→v3.50: qa_signed_off elevated from advisory to hard merge-gate requirement (DF-02).** §8 source prompt header v3.49→v3.50. §14 Execution Engine Source v3.49→v3.50. §14 Version 4.70→4.71/2026-07-02. Change: §3.2.B `qa_signed_off` note upgraded from "Advisory (OA-1/ST-01)" to a hard requirement; STEP 4 merge gate table gained a new row — `qa_signed_off = true (execution_state.json)` must be set, independent of the PR-comment QA sign-off row. Resolves a deferred v6.3 Phase 3 lessons-learnt patch (DF-02) not applied at v6.4 planning time (1st missed target); applied now rather than re-deferred, per post-ship closure's non-deferrable immediate-action rule. Cross-check also confirmed DF-01 and DF-05 (v6.3 carry-forward) are already satisfied by pre-existing patches (LL-v3.7-EX-01 and AUD-2026-06-22-001 respectively) — no further action required; DF-06 confirmed applied in sprint_backlog.md this cycle. Authority: Head of Specs Team (v6.4 post-ship closure, 2026-07-02). |
| 4.70 | 2026-07-02 | **Post-ship closure 2026-07-02__release-v6.4 STEP 8 immediate action — qa_evidence_template.md v1.5→v1.6: signer format requirement made explicit.** §14 QA Evidence Template v1.5→v1.6. §14 Version 4.69→4.70/2026-07-02. Change: new authoring note added to the Standard Sign-Off Block specifying the exact set of compliant `Signed off by:` values (`Director of Quality`, `Sprint Execution Engine (autonomous class)`, `Sprint Execution Engine (agent-mediated, <Role Name> role — §X.Y)`, or the two delegated-QA aggregate formats). Resolves a deferred v6.3 Phase 4 lessons-learnt patch that was not applied at v6.4 planning time (1st missed target); applied now per post-ship closure's non-deferrable immediate-action rule rather than deferred a second time. Authority: Head of Specs Team (v6.4 post-ship closure, 2026-07-02). |
| 4.69 | 2026-07-02 | **v6.4 ST-07 (BLG-GOV-153, EPIC-02) — audit & governance process fixes.** §6 source prompt header updated v7.8→v7.9. §13 Artefact Register Roadmap Rebalance Prompt row updated v7.8→v7.9. §14 Roadmap Engine Source v7.8→v7.9. §14 Shared Standards v3.6→v3.7. §14 Team Charter v1.6→v1.7. §14 Version 4.68→4.69/2026-07-02. Changes: (AC-01/G5) `team_charter.md` new §5.7 "Design gate bypass disputes" added — codifies the dual-authority requirement (Head of UX & Design + Product Owner) already enforced procedurally at `sprint_planning_prompt.md` STEP -1, closing G5 FAIL. (AC-02) `shared_standards.md` §13 dry-run table — `run audit` row added (N/A, read-only by design). (AC-03) `claude/audit.py` FRICTION_LOAD formula — wording clarified to "since PRIOR_AUDIT_ID" rather than ambiguous "across all cycles" (comment/docstring only, no AUDIT_VERSION bump — scoring behaviour unchanged). (AC-04) `roadmap_prompt.md` STEP write instruction — `scored_initiatives.md` documented as intentionally current-cycle-only (overwritten each run, no cycle-dated copies); orphaned `claude/scoring/scored_initiatives_2026-03-06.md` removed. Authority: Head of Specs Team (v6.4 ST-07, 2026-07-02). |
| 4.68 | 2026-07-02 | **v6.4 ST-06 (BLG-GOV-152 + FI-P3-01/FI-P3-02/FI-P4-01 re-target, EPIC-02) — 4 structural reliability gaps closed.** §14 Shared Standards v3.5→v3.6. §14 Execution Engine Source v3.48→v3.49. §14 Amendment Cycle Engine v1.8→v1.9. §14 Version 4.67→4.68/2026-07-02. Changes: (AC-01) shared_standards.md §7 — structural verification requirement note added covering the 4 append-only files without a structural guard (`escalations.md`, `execution_escalations.md`, `verification_escalations.md`, `delegation_log.md`), referencing `decision_log.md`'s existing structural pattern as the model to apply. (AC-02/FI-P4-01/DF-10) execution_prompt.md `spec_references` policy — Case D (CI/infrastructure) added; trailing sentence corrected so `spec_references = []` no longer the recommended default for infra stories with an identifiable primary file. (AC-03/FI-P3-02) CLAUDE.md §2 frontend testing gate — wording-only vs visual/rendering AC exception added (not a Class 6 prompt, no version bump). (AC-04) amendment_cycle_prompt.md §9 completion condition — `amendment_lessons.md` bullet made explicitly conditional on file version <2.0, matching §8's deprecation framing. (AC-05/FI-P3-01) `claude/agents/base44_frontend_prompt_owner.md` v1.2→v1.3 (agent charter, not §14-tracked) — Playwright strict-mode `data-testid` advisory added to §3 "6. Expected outcome". Authority: Head of Specs Team (v6.4 ST-06, 2026-07-02). |
| 4.67 | 2026-07-02 | **v6.4 ST-05 (BLG-GOV-151, EPIC-02) — Class 6 header format fix: roadmap_prompt.md v7.7→v7.8, release_planning_prompt.md v2.38→v2.39, sprint_planning_prompt.md v3.11→v3.12.** §6 source prompt header updated v7.7→v7.8. §6B source prompt header updated v2.38→v2.39. §7 source prompt header updated v3.11→v3.12. §13 Artefact Register Roadmap Rebalance Prompt row updated v7.7→v7.8. §14 Roadmap Engine Source v7.7→v7.8. §14 Release Engine Source v2.38→v2.39. §14 Sprint Planning Engine v3.11→v3.12. §14 Version 4.66→4.67/2026-07-02. Change: all 3 files' `**Last Updated:**` header field changed from date-plus-change-description prose to date-only, per `document_lifecycle_guide.md` Class 6 spec (`Last Updated: [date]`); change descriptions already duplicated in `prompt_change_log.md` are not lost. Authority: Head of Specs Team (AUD-2026-07-01-011, v6.4 ST-05, 2026-07-02). |
| 4.66 | 2026-07-01 | **Roadmap rebalance 2026-07-01__scheduled — roadmap_prompt.md v7.6→v7.7 (FI-META-02 action-now patch) + drift correction.** §6 source prompt header updated v7.6→v7.7. §13 Artefact Register Roadmap Rebalance Prompt row updated v7.6→v7.7. §14 Roadmap Engine Source v7.5→v7.7 (corrects a pre-existing stale row that was never updated at the v7.6 bump on 2026-06-22 — §6/§13 already showed v7.6 but §14 still showed v7.5). §14 Version 4.63→4.66/2026-07-01 (catches up 2 versions of un-recorded drift — see 4.65 backfill entry below — plus this cycle's bump). Change: STEP -1.6 large-window budget note added — when the inline idea intake window produces >30 submissions, budget additional context depth for STEPs 4 and 5; if advancing idea count exceeds 15, prioritise advancing only the highest-scoring ideas (per STEP 6 criteria) and park the remainder. Root cause: IW-20260626-01 (44 submissions, 22 agents) flagged as a context-budget risk at meta-review (STEP 11.4, rebalance 2026-06-26__scheduled). Authority: Head of Specs Team (FI-META-02 deferred patch; applied action-now per STEP -1.5 stale-release-target rule since target release v6.3 had already shipped). |
| 4.65 | 2026-06-24 | **Backfill entry — v6.2 ST-10+ST-11 (BLG-GOV-135+136, EPIC-03), execution_prompt.md v3.47→v3.48.** This row documents a change already applied to the document header and §8 source prompt header at the time (see `prompt_change_log.md` 2026-06-24 entry) but never recorded in this Change Log table, leaving §14 Version stuck at 4.63 across two subsequent bumps. §8 source prompt header v3.47→v3.48. §14 Execution Engine Source v3.47→v3.48. §14 Version 4.64→4.65/2026-06-24 (recorded retroactively 2026-07-01). Changes: §3.2.A Autonomous DoQ sign-off class criterion 3 updated with detection rule (ST-10/BLG-GOV-135) — autonomous class path unavailable if any story modifies `src/components/**` or `src/pages/**`, regardless of Playwright coverage. STEP 0 instruction 6 updated with advisory (ST-11/BLG-GOV-136) — test_scenarios paths must be runnable test files under `tests/` or `tests/e2e/`, not `docs/testing/` scenario description artefacts. Authority: Head of Specs Team (BLG-GOV-135+136, v6.2 ST-10+ST-11, 2026-06-24). |
| 4.64 | 2026-06-22 | **v6.1 ST-01/ST-02 (BLG-GOV-132/133, EPIC-01) — release_planning_prompt.md v2.37→v2.38 + sprint_planning_prompt.md v3.10→v3.11.** §6B source prompt header updated v2.37→v2.38. §7 source prompt header updated v3.10→v3.11. §14 Release Engine Source v2.37→v2.38. §14 Sprint Planning Engine v3.10→v3.11. §14 Version 4.63→4.64/2026-06-22. Changes: (ST-01/BLG-GOV-132) release_planning_prompt.md STEP 4.1 Design Gate Classification added — after writing backlog slice, scans all ST items for UI-facing scope (delegated_frontend OR autonomous with observable UI ACs); sets design_gate_required=true/false in state.json and .claude_current_state.json; outputs advisory "⚠ DESIGN GATE REQUIRED" or "Design Gate: Not Required"; STEP 7 updated to include design_gate_required status line in cycle_summary.md header. (ST-02/BLG-GOV-133) sprint_planning_prompt.md STEP -1 check 3 updated — design gate hard gate now conditional on design_gate_required=true; reads attributes.design_gate_required from state.json; when false/not_required: skips gate with log note "Design gate: Not Required for this cycle"; when true/absent (safety default): applies full hard gate as before. Authority: Head of Specs Team (v6.1 EPIC-01 Sprint 1, 2026-06-22). |
| 4.61 | 2026-06-22 | **roadmap_prompt.md v7.5→v7.6 — STEP 8.2 Now Horizon Item Verification added (mandatory).** §6 source prompt header updated v7.5→v7.6. §14 Roadmap Rebalance Prompt v7.5→v7.6. §14 Version 4.60→4.61/2026-06-22. Change: STEP 8.2 inserted between STEP 8.1 and STEP 8.5 — for every item proposed for Now horizon inclusion (firm or conditional), grep backlog.md to confirm active status; if not found in active backlog, check backlog_archive.md; if archived/shipped, exclude and log; if found in neither, escalate. Distinct from STEP 8.0.5: catches items introduced via prose references (run_manifest text, sprint history) that bypass the STEP 3 formal candidate list. Root cause: 2026-06-19__scheduled included BLG-GOV-113 (archived v5.3) via context-window prose reference; error propagated to cycle_summary.md and DL-048 before correction at STEP 9. Authority: Head of Specs Team (LL-RP-01 deferred patch, rebalance 2026-06-22__scheduled). |
| 4.60 | 2026-06-22 | **AUD-2026-06-22 latent improvements — post_ship_closure.md v2.14→v2.15, delivery_verification_prompt.md v3.0→v3.1, execution_prompt.md v3.46→v3.47.** §8 source prompt header v3.46→v3.47. §9 source prompt header v3.0→v3.1. §10 source prompt header v2.14→v2.15. §14 Execution Engine Source v3.46→v3.47. §14 Verification Engine Source v3.0→v3.1. §14 Post-Ship Closure Engine v2.14→v2.15. §14 Version 4.59→4.60/2026-06-22. Changes: (AUD-2026-06-22-005) post_ship_closure.md STEP 7 — new sub-step 7.3 TSG backlog reconciliation added: for each §27 entry with status "Open", cross-check backlog.md; if BLG item is COMPLETE/DONE, update §27 to RESOLVED with resolution cycle; prevents stale TSG entries accumulating across cycles. (AUD-2026-06-22-006) execution_prompt.md STEP 3.1.A step 3 — API performance baseline advisory added: when committing a new entry to openapi.yaml, also add a row to api_performance_baseline.md in same commit; advisory-only, omission caught at post-ship STEP 6. (AUD-2026-06-22-007) delivery_verification_prompt.md STEP 5.1 — algorithm replacement advisory added: for stories replacing a core algorithm/model, cross-check that all test_scenarios entries were either run (confirmed in qa_evidence) or declared superseded in DoQ sign-off block; purpose-built unit test does not satisfy prior domain-level scenario file automatically. Authority: Head of Specs Team + PMO Lead (AUD-2026-06-22 latent improvements, 2026-06-22). |
| 4.59 | 2026-06-22 | **AUD-2026-06-22 Tier 2 patches — execution_prompt.md v3.45→v3.46: STEP 5.3A write+verify sub-step + STEP 4 step 3b pre-halt governance commit.** §8 source prompt header updated v3.45→v3.46. §14 Execution Engine Source v3.45→v3.46. §14 Version 4.58→4.59/2026-06-22. Changes (execution_prompt v3.46): (AUD-2026-06-22-001) STEP 5.3A — added "Write verification" block immediately after `git add docs/System_status_report.md`; `grep -c "Sprint: <cycle_id>" docs/System_status_report.md` must return ≥1 before proceeding to STEP 5.4; if count=0, the write step was skipped — re-run write now; resolves 3rd-cycle recurrence of silent SSR write skip (v3.45 patch staged a write that never happened). (AUD-2026-06-22-002) STEP 4 step 3b added before hard-gate halt — mandatory `git status --short` check; if any governance files (backlog.md, qa_evidence_EPIC-xx.md) are unstaged, commit and push to EPIC branch before outputting halt message; session-close advisory updated to reference 3b and remain active for non-governance changes only; resolves 4th-cycle recurrence of stash-at-branch-switch (v5.3/v5.4/v5.5/v6.0). Authority: Head of Specs Team (AUD-2026-06-22 Tier 2, 2026-06-22). |
| 4.58 | 2026-06-19 | **LL-P5-03 overdue resolution — roadmap_prompt.md v7.4→v7.5: STEP -1.5 stale release target check added.** §6 source prompt header updated v7.4→v7.5. §13 artefact register Roadmap Rebalance Prompt v7.4→v7.5. §14 Roadmap Engine Source v7.4→v7.5. §14 Version 4.57→4.58/2026-06-19. Change (roadmap v7.5): STEP -1.5 Prompt patch confirmation — third bullet added: if a deferred patch's target event is a named release (`plan release vX.Y`), verify whether that release has already shipped by checking release summary table in `current_roadmap.md`; if shipped → classify OVERDUE immediately without waiting for 2-cycle carry rule. Resolves LL-P5-03 (first filed 2026-06-17__scheduled; carried to 2026-06-19__scheduled as OVERDUE; root cause: LL-P5-02 patch itself had a stale release target that passed before the deferred patch was validated). Authority: Head of Specs Team (LL-P5-03 overdue resolution, rebalance 2026-06-19__scheduled). |
| 4.57 | 2026-06-18 | **roadmap_prompt.md v7.3→v7.4 — four diagnostic steps added + Skill-Silo ceiling lowered.** §6 source prompt header updated v7.3→v7.4. §14 Roadmap Engine Source v7.3→v7.4. §13 artefact register Roadmap Rebalance Prompt v7.1→v7.4. §14 Version 4.56→4.57/2026-06-18. Changes: STEP 2.4 Product Value Ratio Diagnostic (mandatory) — classifies last 5 cycles' stories as U/G/D/P; fires Product Value Alert if ratio < 0.30; Advisory if < 0.50. STEP 3.1 Actionable Backlog Assessment (mandatory) — categorises each active backlog item as A/T/D/L; surfaces Backlog Accessibility Warning if A-items < 30%. STEP 5 — Challenger Product Velocity Concern exception added: when STEP 2.4 ratio < 0.50, Challenger may raise a Product Velocity Concern without §13 basis. STEP 7.1 — Skill-Silo ceiling reduced from 60% to 40%; metric changed from governance FTE to story-count (solo-developer context). STEP 8.0 Production Correctness Fast-Track (mandatory) — before any horizon debate, scan backlog for P0/P1 correctness/security items; any found must appear in Now horizon ahead of governance/debt items. Authority: Head of Specs Team + Product Owner (strategic review 2026-06-18). |
| 4.56 | 2026-06-18 | **v5.9 post-ship closure (LL-v5.9-P4-01) — execution_prompt.md v3.44→v3.45: STEP 5.3A immediate staging instruction added for docs/System_status_report.md.** §8 source prompt header updated v3.44→v3.45. §14 Execution Engine Source v3.44→v3.45. §14 Version 4.55→4.56/2026-06-18. Change: STEP 5.3A — added "Immediate staging (LL-v5.9-P4-01)" block after SSR write; explicit `git add docs/System_status_report.md` staged before any branch switch; resolves multi-cycle commit discipline gap (SSR sections absent from committed file across v5.6/v5.7/v5.8/v5.9). Authority: Head of Specs Team (LL-v5.9-P4-01, v5.9 post-ship closure, 2026-06-18). |
| 4.47 | 2026-06-16 | **sprint_planning_prompt.md v3.9→v3.10 — STEP -1.7 prompt change log gap advisory: replaced `grep | tail` instruction with `grep | head -1` and explicit prepend-sort note.** §7 source prompt header updated v3.9→v3.10. §14 Sprint Planning Engine v3.9→v3.10. §14 Version 4.46→4.47/2026-06-16. Change (sprint_planning_prompt v3.10): STEP -1.7 hygiene advisory — prompt change log gap check rewritten to use `grep "<filename>" prompt_change_log.md | head -1` (file is prepended newest-first; `head -1` gives the most recent entry); explicit note added that `tail` must NOT be used; false-positive root cause: prior wording "not top-first — entries may be at the bottom" predated prepend-sort convention and caused engine to read oldest entries as most recent. Per-file changelogs (post_ship_closure_changelog.md, roadmap_management_changelog.md) backfilled with entries missed since 2026-05-09 refactor. Authority: Head of Specs Team (RCA + v5.7 sprint planning false-positive resolution, 2026-06-16). |
| 4.46 | 2026-06-16 | **backlog_management_prompt.md v1.8→v1.9 — §6 classification criteria and STEP 6.2 post-write verification extended to catch body-line ✅ COMPLETE markers.** §6M source prompt header updated v1.8→v1.9. §14 Backlog Management Engine v1.8→v1.9. §14 Version 4.45→4.46/2026-06-16. Changes (backlog_management v1.9): §6 Complete—Archive classification — criteria updated from "Status ✅ COMPLETE with delivery date" (ambiguous) to explicitly require checking the heading line OR the first body line immediately following the `### BLG-` heading; STEP 6.2 post-write verification — two-check grep added: (1) heading lines for ✅ COMPLETE/❌ Killed, (2) line immediately following each `### BLG-` heading for same markers. Root cause: the standard backlog format places ✅ COMPLETE on the body line, not the heading; prior single-grep check (v1.8) only caught heading-embedded markers, allowing ~100 completed items to accumulate across cycles before manual intervention on 2026-06-16. Authority: Head of Specs Team (post-groom root cause analysis, 2026-06-16). |
| 4.55 | 2026-06-17 | **v5.9 EPIC-01 sign-off remediation — OPERATIONAL_GUIDE §6/§6B/§8/§10 section body source prompt headers updated to match §14.** §6 source prompt header: roadmap_prompt.md v7.1→v7.3. §6B source prompt header: release_planning_prompt.md v2.36→v2.37. §8 source prompt header: execution_prompt.md v3.42→v3.44. §10 source prompt header: post_ship_closure.md v2.13→v2.14. §14 Version 4.54→4.55/2026-06-17. Root cause: CLAUDE.md §6 step 3 (update phase section source prompt header) was applied to §14 table only; section body headers were not updated in the same edit. Authority: Head of Specs Team (sign-off remediation, v5.9 EPIC-01, 2026-06-17). |
| 4.54 | 2026-06-17 | **v5.9 ST-02 SC-04 remediation — roadmap_prompt.md v7.2→v7.3: dangling STEP 8/8.7 reference in STEP 9 write rules corrected.** §6 source prompt header updated v7.2→v7.3. §14 Roadmap Engine Source v7.2→v7.3. §14 Version 4.53→4.54/2026-06-17. Change: STEP 9 bullet "Reflect STEP 8/8.7 decisions exactly" corrected to "Reflect STEP 8 decisions exactly" — STEP 8.7 was removed by SC-04 and this reference was a dangling pointer. Authority: Head of Specs Team (sign-off remediation, v5.9 ST-02, 2026-06-17). |
| 4.53 | 2026-06-17 | **v5.9 ST-05 (SC-07, EPIC-01) — post_ship_closure.md v2.13→v2.14: Advisory Summary Block format docs compressed to ≤5 lines.** Source prompt header updated v2.13→v2.14. §14 Post-Ship Closure Engine v2.13→v2.14. §14 Version 4.52→4.53/2026-06-17. Change: Advisory Summary Block section compressed from ~13 lines to 3 lines (heading + single-paragraph rule + format inline). All format elements preserved: separator strings, list-or-None instruction, source step references. Authority: Head of Specs Team (SC-07, v5.9 ST-05, 2026-06-17). |
| 4.52 | 2026-06-17 | **v5.9 ST-04 (SC-06, EPIC-01) — execution_prompt.md v3.43→v3.44: STEP 3.1.A step 13 cross-spec selector check made conditional on DOM changes.** §8 source prompt header updated v3.43→v3.44. §14 Execution Engine Source v3.43→v3.44. §14 Version 4.51→4.52/2026-06-17. Change: Step 13 condition tightened — scan is now explicitly skipped for governance-only and backend-only stories (no DOM changes possible); frontend EPICs retain full scan requirement with no exceptions. Authority: Head of Specs Team (SC-06, v5.9 ST-04, 2026-06-17). |
| 4.51 | 2026-06-17 | **v5.9 ST-03 (SC-05, EPIC-01) — release_planning_prompt.md v2.36→v2.37: STEP 5.7 conditional on escalations; STEP 1.3 reduced to single-line note.** §6B source prompt header updated v2.36→v2.37. §14 Release Engine Source v2.36→v2.37. §14 Version 4.50→4.51/2026-06-17. Changes: STEP 5.7 Decision Record Integrity now runs only when `artifacts.escalations = present` in state.json; STEP 1.3 Design-Gate Language Scan reduced from 6 lines to 2 lines (advisory note preserved). Authority: Head of Specs Team (SC-05, v5.9 ST-03, 2026-06-17). |
| 4.50 | 2026-06-17 | **v5.9 ST-02 (SC-04, EPIC-01) — roadmap_prompt.md v7.1→v7.2: STEPs 8.6–8.7 fatigue detection guardrail removed; STEP 5 Challenger failure rule updated to cover convergence bias.** §6 source prompt header updated v7.1→v7.2. §14 Roadmap Engine Source v7.1→v7.2. §14 Version 4.49→4.50/2026-06-17. Changes: STEP 5 Challenger failure rule updated — Clearance Statements across all advancing candidates with no substantive challenge classified as convergence bias / Challenger failure; STEPs 8.6 (Fatigue Detection Guardrail) and 8.7 (Pivot Loop) removed (never triggered; convergence bias now covered by STEP 5). Authority: Head of Specs Team (SC-04, v5.9 ST-02, 2026-06-17). |
| 4.49 | 2026-06-17 | **v5.9 ST-01 (SC-03, EPIC-01) — execution_prompt.md v3.42→v3.43: STEP 3.1.A steps 2a/2b/2c consolidated into single 3-case lookup table.** §8 source prompt header updated v3.42→v3.43. §14 Execution Engine Source v3.42→v3.43. §14 Version 4.48→4.49/2026-06-17. Change: Steps 2, 2a, 2b, 2c replaced by a single "Spec_references policy (SC-03)" rule with 3-case lookup table (Case A: path verify; Case B: documentation-creation; Case C: test-authoring). All three edge cases preserved; ~25 lines reduced to ~10 lines. Authority: Head of Specs Team (SC-03, v5.9 ST-01, 2026-06-17). |
| 4.48 | 2026-06-17 | **Rebalance 2026-06-17__scheduled action-now — release_planning_prompt.md v2.35→v2.36 (STEP 1.4b Within-Sprint Date Gate Classification, mandatory).** §6B source prompt header updated v2.35→v2.36. §14 Release Engine Source v2.35→v2.36. Change (release_planning v2.36): STEP 1.4b added between 1.4a and 1.4 — Within-Sprint Date Gate Classification is now mandatory (not advisory). Any candidate item whose gate clearing date falls within the planned sprint execution window must be classified as conditional (not firm) in the release plan; the gate must be explicitly confirmed cleared before promotion to firm scope; violation = P2 deviation filed as BLG-GOV type. Elevated from advisory to mandatory after pattern confirmed across 5 consecutive releases: v5.4 ST-03, v5.5 ST-11–14, v5.6 ST-03, v5.7 ST-09/12–14, v5.8 ST-01/02 — all returned to backlog due to within-sprint date gates not met. §14 Version 4.47→4.48/2026-06-17. Authority: Head of Specs Team (LL-P3-03-v55/LL-P4-01-v55 overdue — second consecutive roadmap cycle carry; action-now applied rebalance 2026-06-17__scheduled). |
| 4.45 | 2026-06-16 | **AUD-2026-06-16 Tier 1 patches — release_planning_prompt.md v2.34→v2.35 (STEP 1.4a Perennial-Return Check) + execution_prompt.md v3.41→v3.42 (§5.3 Infrastructure co-sign class).** §6B source prompt header updated v2.34→v2.35. §8 source prompt header updated v3.41→v3.42. §14 Release Engine Source v2.34→v2.35. §14 Execution Engine Source v3.41→v3.42. §14 Version 4.44→4.45/2026-06-16. Changes: (AUD-2026-06-16-001) release_planning STEP 1.4a added — Perennial-Return Check advisory: items returned at planning for 2+ consecutive cycles require PO active disposition (keep with updated gate evidence OR remove from horizon); prevents silent re-entry. (AUD-2026-06-16-002) execution_prompt §5.3 — Infrastructure co-sign class added: "Infrastructure & Operations Owner + Director of Quality: Confirmed" is a valid DoQ sign-off for backend-only EPICs; accepted by delivery_verification §-1.3 Tier 2 as agent-mediated with named domain role. Authority: Head of Specs Team (AUD-2026-06-16 Tier 1 closure, 2026-06-16). |
| 4.44 | 2026-06-16 | **Rebalance 2026-06-16__scheduled LL-RP-02 action-now patch — roadmap_prompt.md v7.0→v7.1: STEP 8.0.5 candidate list pre-clean elevated from Advisory to Mandatory; now fires at two points: STEP 3 candidate compilation AND before STEP 8.1 presentation.** §6 source prompt header updated v7.0→v7.1. §14 Roadmap Engine Source v7.0→v7.1. Change: STEP 8.0.5 retitled from "Advisory" to "Mandatory"; step description updated to fire at STEP 3 (when compiling candidate list from backlog) in addition to STEP 8.1 (before presenting to PO); root cause note added (two consecutive cycles v5.4+v5.5 saw complete items appear because candidate lists were compiled without running the grep). §14 Version 4.43→4.44/2026-06-16. Authority: Head of Specs Team (LL-RP-02, rebalance 2026-06-16__scheduled). |
| 4.43 | 2026-06-15 | **v5.5 sprint close lessons learnt action-now patches — execution_prompt.md v3.40→v3.41: branch ordering gate (STEP 5) + merge state persist before halt (STEP 4).** §8 source prompt header updated v3.40→v3.41. §14 Execution Engine Source v3.40→v3.41. Changes (execution_prompt v3.41): (LL-v5.5-EX-01, third recurrence git-stash-at-branch-switch) STEP 5 opening branch ordering gate added — before ANY STEP 5 writes, engine must confirm `git branch --show-current` is main and switch if not; prevents backlog.md/execution_state.json writes on EPIC branch. (LL-v5.5-EX-02, third recurrence stale-pr_status) STEP 4 step 3a added — immediately after merging, commit execution_state.json to EPIC branch before outputting halt message; prevents stale merged state at next session resume. §14 Version 4.42→4.43/2026-06-15. Authority: Head of Specs Team (v5.5 Phase 3 lessons learnt, 2026-06-15). |
| 4.42 | 2026-06-11 | **v5.5 ST-02+ST-03 (BLG-GOV-117+118, EPIC-01) — execution_prompt.md v3.39→v3.40: pr_status read-after-open improvement + qa_evidence commit advisory.** §8 source prompt header updated v3.39→v3.40. §14 Execution Engine Source v3.39→v3.40. Changes (execution_prompt v3.40): (ST-02/BLG-GOV-117) §3.2.B step 5 updated: `gh pr view` command expanded from `--json state` to `--json state,mergeStateStatus` — captures actual PR state including merge readiness immediately after open. (ST-03/BLG-GOV-118) §3.2.B — "qa_evidence commit advisory (BLG-GOV-118)" added before step 1: verify `qa_evidence_EPIC-xx.md` is committed to EPIC branch before running `gh pr create`; git status check required. §14 Version 4.41→4.42/2026-06-11. Authority: Head of Specs Team (BLG-GOV-117+118, v5.5 ST-02+ST-03, 2026-06-11). |
| 4.41 | 2026-06-11 | **v5.5 ST-01 (BLG-GOV-116, EPIC-01) — sprint_planning_prompt.md v3.8→v3.9: within-sprint date gate advisory.** §7 source prompt header updated v3.8→v3.9. §14 Sprint Planning Engine v3.8→v3.9. Change (sprint_planning_prompt v3.9): STEP 6.1 — "Within-sprint date gate advisory (BLG-GOV-116)" added: stories with within-sprint date gates must be marked `**Status at sprint open: conditional — gate <date>**` in sprint_backlog.md at planning time; `ready` only when no within-sprint date gate exists. Resolves v5.4 lessons-learnt carry-forward (ST-11–14 in v5.5 were the first correctly marked instances). §14 Version 4.40→4.41/2026-06-11. Authority: Head of Specs Team (BLG-GOV-116, v5.5 ST-01, 2026-06-11). |
| 4.40 | 2026-06-10 | **AUD-2026-06-10 Tier 1 patches (part 2): roadmap_prompt.md v6.9→v7.0 STEP 8.0.5 candidate list pre-clean + execution_prompt.md v3.38→v3.39 STEP 4 branch clean-state advisory.** §6 source prompt header updated v6.9→v7.0. §8 source prompt header updated v3.38→v3.39. §14 Roadmap Engine Source v6.9→v7.0. §14 Execution Engine Source v3.38→v3.39. Changes: (AUD-2026-06-10-003) roadmap_prompt.md STEP 8.0.5 added — candidate list pre-clean advisory: grep backlog.md for ✅ COMPLETE / RA: markers on each candidate BLG-ID before presenting to PO; removes already-shipped items from candidate list. (AUD-2026-06-10-002) execution_prompt.md STEP 4 halt output — session-close advisory added: operator must verify git status clean on EPIC branch before ending session (2nd recurrence: v5.3+v5.4 stash-at-branch-switch). §14 Version 4.39→4.40/2026-06-10. Authority: Head of Specs Team (AUD-2026-06-10 Tier 1 closure, 2026-06-10). |
| 4.39 | 2026-06-10 | **AUD-2026-06-10 Tier 1 patches (part 1): §14 self-metadata desync fixed (4th recurrence) + shared_standards.md v3.4→v3.5 amend cycle dry-run row added.** §14 self-metadata table Version corrected from 4.31→4.38/4.39 and Last Updated from 2026-06-21→2026-06-10 (entries v4.32–v4.37 had been added without updating the §14 self-metadata rows — recurring pattern). §14 Shared Standards updated v3.4→v3.5. §14 Version 4.38→4.39/2026-06-10. Authority: Head of Specs Team (AUD-2026-06-10 Tier 1 closure, 2026-06-10). |
| 4.38 | 2026-06-10 | **AUD-2026-06-10 Tier 1 patches: §14 self-metadata desync fixed (4th recurrence) + shared_standards.md v3.4→v3.5 amend cycle dry-run row added.** §14 self-metadata table Version corrected from 4.31→4.38 and Last Updated from 2026-06-21→2026-06-10 (entries v4.32–v4.37 had been added without updating the §14 self-metadata rows — recurring pattern, now also reinforced in §14 standing rule). §14 Shared Standards updated v3.4→v3.5. §14 Version 4.37→4.38/2026-06-10. Authority: Head of Specs Team (AUD-2026-06-10 Tier 1 closure, 2026-06-10). |
| 4.37 | 2026-06-09 | **Roadmap rebalance 2026-06-09__scheduled meta-review action-now — roadmap_prompt.md v6.8→v6.9: STEP 8.5.B BLG-ID collision advisory.** §6 source prompt header updated v6.8→v6.9. §14 Roadmap Engine Source v6.8→v6.9. Change (roadmap v6.9): STEP 8.5.B step 5 added — non-blocking advisory: before assigning new BLG-IDs in debate summaries or decision records, grep backlog.md for the highest existing ID in each series and assign from highest+1; prevents BLG-ID collision when an ID was added between rebalance date and write pass. Meta-review action-now — Type D recurring pattern (cycles 2026-06-07 and 2026-06-08). §14 Version 4.36→4.37/2026-06-09. Authority: Head of Specs Team (meta-review action-now, 2026-06-09__scheduled). |
| 4.36 | 2026-06-09 | **Roadmap rebalance 2026-06-09__scheduled STEP -1.5 overdue patch — idea_intake_prompt.md v2.4→v2.5: backlog scope advisory added to §2.0.** §5 source prompt header updated v2.4→v2.5. §14 Idea Intake Engine v2.4→v2.5. Change (idea_intake v2.5): §2.0 Parked Queue Pre-Check step 5 added — advisory (non-blocking): before finalising new submission topics, briefly scan active backlog.md items for scope overlap with planned submissions; if an active BLG-ID covers the same initiative, note it in the submission's Purpose/Rationale field. Patch originally filed 2026-06-07__scheduled, carried 2026-06-08__scheduled, classified OVERDUE at 2026-06-09__scheduled STEP -1.5. §14 Version 4.35→4.36/2026-06-09. Authority: Head of Specs Team (deferred patch overdue resolution, 2026-06-09). |
| 4.35 | 2026-06-09 | **v5.3 ST-12 (LL-v5.2-P4-02, EPIC-03) — execution_prompt.md v3.37→v3.38: STEP 5.3A SSR cycle_id section check sub-step.** §8 source prompt header updated v3.37→v3.38. §14 Execution Engine Source v3.37→v3.38. Change (execution_prompt v3.38): STEP 5.3A — new sub-step "cycle_id section check (LL-v5.2-P4-02)" added: before writing SSR section, check whether `docs/System_status_report.md` already contains `## Sprint: <cycle_id>` heading; if not present create it; if present update in-place. Prevents duplicate sprint sections and ensures every cycle has an SSR entry before commit. Resolves LL-v5.2-P4-02 carry-forward OA. §14 Version 4.34→4.35/2026-06-09. Authority: Head of Specs Team (LL-v5.2-P4-02, v5.3 ST-12, 2026-06-09). |
| 4.34 | 2026-06-09 | **v5.3 ST-11 (LL-v5.2-P4-01, EPIC-03) — qa_evidence_template.md v1.4→v1.5: mixed-class EPIC signer format note.** §14 QA Evidence Template v1.4→v1.5. Change (qa_evidence_template v1.5): new section "Mixed-Class EPIC Signer Format Note" added specifying the exact signer format `"Sprint Execution Engine (agent-mediated, <Role Name> role — §5.3)"` for EPICs with both delegated_backend and autonomous stories; clarifies that BLG-GOV-19 autonomous class is disqualified by any delegated_* story. Resolves LL-v5.2-P4-01 carry-forward OA. §14 Version 4.33→4.34/2026-06-09. Authority: Head of Specs Team (LL-v5.2-P4-01, v5.3 ST-11, 2026-06-09). |
| 4.33 | 2026-06-08 | **v5.2 ST-02 (OA-02, EPIC-01) — execution_prompt.md v3.36→v3.37: test-authoring spec_references guidance.** §8 source prompt header updated v3.36→v3.37. §14 Execution Engine Source v3.36→v3.37. Change (execution_prompt v3.37): §3.1.A step 2c added (OA-02): for test-authoring stories (sole deliverable is a new test file, no prior spec applicable), set `spec_references` to the created test file path rather than leaving empty with "no prior spec applicable" note; the test file IS a traceable artefact and its path must be recorded. Prevents traceability flags at delivery verification for test-creation stories. §14 Version 4.32→4.33/2026-06-08. Authority: Head of Specs Team (OA-02, v5.2 ST-02, 2026-06-08). |
| 4.32 | 2026-06-08 | **v5.2 ST-01 (OA-01, EPIC-01) — release_planning_prompt.md v2.33→v2.34: §-1.2 STEP 8.1 Option(b) acceptance clause.** §6B source prompt header updated v2.33→v2.34. §14 Release Engine Source v2.33→v2.34. Change (release_planning v2.34): §-1.2 gate expanded from hard halt to two-path check — if planned release section not found: also accept documented STEP 8.1 Option(b) decision (from most recent rebalance run_manifest.md or cycle_summary.md) as equivalent to formal planned release section; if neither exists: halt. Prevents recurring §-1.2 halt when PO intentionally deferred via Option(b). Root cause: OA-01 outstanding from v5.1 (LL-RP-v5.1-01). §14 Version 4.31→4.32/2026-06-08. Authority: Head of Specs Team (OA-01, v5.2 ST-01, 2026-06-08). |
| 4.31 | 2026-06-21 | **v5.1 ST-03 (EPIC-02) — delivery_verification_prompt.md v2.9→v3.0: agent-mediated signer format accepted in §-1.3 Tier 2.** §9 source prompt header updated v2.9→v3.0. §14 Verification Engine Source v2.9→v3.0. §14 Version 4.29→4.31/2026-06-21 (also corrects v4.30 header/§14 desync). Change (delivery_verification v3.0): §-1.3 Tier 2 — new agent-mediated class exception: `"Sprint Execution Engine (agent-mediated, <Role Name> role — §X.Y)"` accepted for mixed-class EPICs as equivalent to agent-mediated sign-off with named role. Prevents recurring Tier 2 advisory for EPICs that used agent-mediated DoQ sign-off (LL-RP-v5.0-D-2, EPIC-03 v5.0). Authority: Head of Specs Team (v5.1 ST-03, 2026-06-21). |
| 4.30 | 2026-06-03 | **Roadmap rebalance 2026-06-03__scheduled STEP -1.5 overdue patch — backlog_management_prompt.md v1.7→v1.8 post-write archive verification.** §6M source prompt header updated v1.7→v1.8. §14 Backlog Management Engine v1.7→v1.8. Change (backlog_management v1.8): STEP 6.2 post-write verification added — after completing STEP 6.2 writes, grep active §1–§8 sections of backlog.md for heading lines retaining `✅ COMPLETE` or `❌ Killed` status markers; if any found, archive move is incomplete — must be resolved before proceeding to STEP 6.3. Patch originally filed 2026-06-01__scheduled, carried 2026-06-02__scheduled, classified OVERDUE at 2026-06-03__scheduled STEP -1.5 (second consecutive cycle without application). §14 Version 4.29→4.30/2026-06-03. Authority: Head of Specs Team (deferred patch overdue resolution, 2026-06-03). |
| 4.29 | 2026-06-03 | **v5.0 ST-05 (BLG-GOV-82) — post_ship_closure.md v2.12→v2.13 AUDIT DUE dual-condition + last_audit_cycle_count state field.** §10 source prompt header updated v2.12→v2.13. §14 Post-Ship Closure Engine v2.12→v2.13. Changes (post_ship v2.13): STEP 0 Audit Cadence Check expanded to dual condition — fires if `completed_cycle_count % 3 == 0` OR `(completed_cycle_count - last_audit_cycle_count) >= 4` (null-safe: gap check skipped if last_audit_cycle_count is null); STEP 10 global state update — `last_audit_cycle_count` write rule added (set to new_completed_cycle_count when audit ran this cycle, else unchanged). `last_audit_cycle_count` field added to `.claude_current_state.json` (init value: 35, matching AUD-2026-06-02) and `lifecycle_schema.json` state_field_extensions. §14 Version 4.28→4.29/2026-06-03. Authority: Head of Specs Team + PMO Lead (BLG-GOV-82, v5.0 ST-05, 2026-06-03). |
| 4.28 | 2026-06-03 | **v5.0 ST-04 (BLG-GOV-80) — execution_prompt.md v3.35→v3.36 STEP 8 governance file edit check made STRUCTURAL.** §8 source prompt header updated v3.35→v3.36. §14 Execution Engine Source v3.35→v3.36. Change (execution_prompt v3.36): STEP 8 governance file edit check replaced with structural scan: runs `git diff --name-only HEAD` and `--cached` filtered by `claude/system/`, `claude/charter/`, `claude/agents/` paths; for each returned file, verifies prompt_change_log.md entry exists at the correct version; appends if missing; check runs against actual git diff rather than relying on operator memory. Root cause of BLG-GOV-79 (7 missing change log entries found at AUD-2026-06-02). §14 Version 4.27→4.28/2026-06-03. Authority: Head of Specs Team (BLG-GOV-80, v5.0 ST-04, 2026-06-03). |
| 4.27 | 2026-06-02 | **Rebalance 2026-06-02__scheduled meta-review action-now — idea_intake_prompt.md v2.3→v2.4.** §5 source prompt header updated v2.3→v2.4. §14 Idea Intake Engine v2.3→v2.4. Change (idea_intake v2.4): STEP 2 §2.0 Parked Queue Pre-Check added — before generating new submissions, each agent must check the ideas_register.md for their own parked ideas on similar topics and resubmit rather than create duplicates. Resolves recurring Type D friction (idea duplication rate: 34% cycle 2026-05-27; 2% cycle 2026-06-01; both cycles had 1+ duplicate). Deferred patch from 2026-06-01__scheduled — first carry cycle; escalated to action-now at meta-review (3rd rebalance since 2026-05-25__scheduled). §14 Version 4.26→4.27/2026-06-02. Authority: Head of Specs Team (meta-review action-now, rebalance 2026-06-02__scheduled). |
| 4.26 | 2026-06-02 | **BLG-GOV-78 resolved — roadmap_prompt.md v6.7→v6.8 STEP 8.1 Empty Now Horizon Soft Gate. AUD-2026-06-02-001: prompt_change_log.md 7 missing entries appended.** §6 source prompt header updated v6.7→v6.8. §14 Roadmap Engine Source v6.7→v6.8. Change (roadmap v6.8): STEP 8.1 strengthened from advisory-only to Soft Gate — Any Rebalance: PO must explicitly choose (a) add next-release section now or (b) defer intentionally and record rationale; "silent pass" path removed; condition broadened from Extended-tier no-change to all rebalances. Resolves BLG-GOV-78 (filed v4.8 post-ship, LL-RP-v4.8-01). Companion action (AUD-2026-06-02-001): 7 missing prompt_change_log.md entries appended covering delivery_verification_prompt.md v2.7→v2.8, post_ship_closure.md v2.11→v2.12, execution_prompt.md v3.33→v3.34, release_planning_prompt.md v2.32→v2.33, roadmap_prompt.md v6.6→v6.7, v6.7→v6.8, execution_prompt.md v3.34→v3.35. §14 Version 4.25→4.26/2026-06-02. Authority: Head of Specs Team (BLG-GOV-78, AUD-2026-06-02, 2026-06-02). |
| 4.25 | 2026-06-01 | **v4.8 Sprint Close — execution_prompt.md v3.34→v3.35 commit SHA record substep (LL-v4.8-EX-01).** §8 source prompt header updated v3.34→v3.35. §14 Execution Engine Source v3.34→v3.35. Change: STEP 3.1.A step 4a added — immediately after push, run `git rev-parse HEAD` and write the SHA to `execution_state.json` for all covered stories; do not defer to sprint close. Resolves first recurrence of null commit_sha pattern (first occurrence v4.7 Phase 3, monitor carried to v4.8, recurred in EPIC-02 autonomous batch commit). §14 Version 4.24→4.25/2026-06-01. Authority: Head of Specs Team (LL-v4.8-EX-01, v4.8 sprint close lessons learnt). |
| 4.24 | 2026-06-01 | **v4.8 ST-01 (BLG-GOV-69) — AUD-2026-05-30-001 gap verified closed; §14 self-metadata Version corrected; sprint_planning_prompt.md v3.6→v3.8 prompt_change_log entries appended.** Verification: §13 Artefact Register and §14 governance table confirmed to contain entries for all 7 Class 6 governance prompts (sprint_planning_prompt.md v3.8, execution_prompt.md v3.34, post_ship_closure.md v2.12, design_gate_prompt.md v1.4, roadmap_management_prompt.md v1.4, backlog_management_prompt.md v1.7, ideas_housekeeping_prompt.md v1.0); all were added to §13 by v4.20 and are tracked in the §14 metadata table. §14 self-metadata Version corrected from 4.20→4.24 (entries v4.21–v4.23 updated the document header and §14 engine rows but did not update the §14 self-metadata Version/Last Updated fields — same pattern as AUD-2026-05-27-001). sprint_planning_prompt.md v3.6→v3.7 and v3.7→v3.8 entries appended to prompt_change_log.md (sprint planning OA clearance). §14 Version 4.23→4.24/2026-06-01. Authority: Head of Specs Team (BLG-GOV-69, v4.8 ST-01, 2026-06-01). |
| 4.23 | 2026-05-30 | **v4.6 ST-22 (OA-02) — roadmap_prompt.md v6.6→v6.7 next_release advisory after DL decision.** §6 source prompt header updated v6.6→v6.7. §14 Roadmap Engine Source v6.6→v6.7. Change: STEP 12.1 Global State Update — advisory added: after DL decision sets next planned release label, update `next_release` in `.claude_current_state.json` to projected version label if determinable; reduces "version not on roadmap" annotation at next release planning invocation; advisory only, no hard gate. §14 Version 4.22→4.23/2026-05-30. Authority: Head of Specs Team (OA-02, v4.5 carry-forward item 1, v4.6 ST-22). |
| 4.22 | 2026-05-30 | **v4.6 ST-15 (BLG-GOV-32+43) — release_planning_prompt.md v2.32→v2.33 STEP 1.4 gate scan + data density checkpoint.** §6B source prompt header updated v2.32→v2.33. §14 Release Engine Source v2.32→v2.33. Change: STEP 1.4 Gate-Condition Proximity Scan added (advisory) — scans gate-conditional backlog items for proximity within 30–60 days; gate proximity table format documented; Arc 4 data density sub-check mandatory (PO-02/PO-04/SI-02 projected gate dates surfaced). §14 Version 4.21→4.22/2026-05-30. Authority: Head of Specs Team (BLG-GOV-32 + BLG-GOV-43, v4.6 ST-15). |
| 4.21 | 2026-05-30 | **v4.5 EPIC-01 (ST-01–04) — execution_prompt.md v3.33→v3.34 four governance patches.** §8 source prompt header updated v3.33→v3.34. §14 Execution Engine Source v3.33→v3.34. Changes: (ST-01/OA-01) §3.1.B + §3.1.D HARD GATE — DEL record write split into two-phase: (a) `status = "sign_off_cleared"` at sign-off time; (b) `commit_sha` at push step; terminal `Unblocked` requires both. (ST-02/OA-02) STEP 3.2.B — step 5 added: `gh pr view <pr_number> --json state` immediately after PR open to sync `pr_status`; EPIC.status sync rule: update `"done"` → `"merged"` if state is MERGED. (ST-03/OA-03) §3.2.A autonomous class criterion 1 — verification-class sub-criterion added (LL-v4.5-EX-01): satisfiable for pre-planning sprints where all VERIFICATION is document inspection only, criteria 2–4 met. (ST-04/BLG-GOV-70) §3.1.A step 2b added (LL-v4.5-EX-02): documentation-creation stories set `spec_references` to artefact path + `delivery_note` field; `spec_references = []` non-compliant for this story type. Authority: Head of Specs Team (v4.5 EPIC-01, 2026-05-30). |
| 4.20 | 2026-05-30 | **AUD-2026-05-30 Tier 1 patches — §13 register completed + §13 Class 7 fix + delivery_verification_prompt.md v2.8→v2.9 owner fix.** §13 artefact register: 7 missing Class 6 prompts added (sprint_planning_prompt.md, execution_prompt.md, post_ship_closure.md, design_gate_prompt.md, roadmap_management_prompt.md, backlog_management_prompt.md, ideas_housekeeping_prompt.md); roadmap_prompt.md Class 7 corrected to Class 6 (Class 7 does not exist in document_lifecycle_guide.md). §9 Phase 4 source prompt header updated v2.8→v2.9. §14 Verification Engine Source v2.8→v2.9. §14 Version 4.19→4.20/2026-05-30. Authority: Head of Specs Team (AUD-2026-05-30 Tier 1 closure, 2026-05-30). |
| 4.19 | 2026-05-29 | **v4.4 ST-13 (BLG-OPS-43) — Staging URL Disambiguation subsection added to §7.** New §7.9 "Staging URL Disambiguation" added after §7.8: distinguishes frontend SPA URL (`trading-assistant-frontend.onrender.com`) from backend API URL (`trading-assistant-api.onrender.com`); health check baseline guidance updated to always target backend API URL; example curl commands shown; root cause (v4.3 Phase 3 staging friction) documented. §14 Version 4.18→4.19/2026-05-29. Authority: Infrastructure & Operations Owner (BLG-OPS-43, v4.4 ST-13). |
| 4.18 | 2026-05-29 | **v4.4 ST-05 — release_planning_prompt.md v2.31→v2.32 RESUME PRECHECK patch.** §6B source prompt header updated v2.31→v2.32. §14 Release Engine Source v2.31→v2.32. Change: STEP 7 Intermediate global state sync — RESUME PRECHECK note added: if session resumed via context compaction and STEP 7 completed without intermediate sync, execute sync immediately before proceeding to STEP 8. Prevents stale `.claude_current_state.json` on session resume. Authority: Head of Specs Team (BLG-GOV-74 deferred, v4.3 LL-2, v4.4 ST-05). |
| 4.17 | 2026-05-29 | **v4.4 ST-04 — qa_evidence_template.md v1.3→v1.4 delegated_qa sign-off format.** §14 QA Evidence Template row added (new row). Change: Standard Sign-Off Block updated with delegated_qa pattern note (BLG-GOV-69/74): two valid sign-off formats documented — (i) individual DoQ sign-off with aggregate comment; (ii) DoQ aggregate acknowledgement format. Both valid; Date field non-blank requirement unchanged. Template clarifies both variants. Authority: Head of Specs Team (BLG-GOV-69 + BLG-GOV-74, v4.4 ST-04). |
| 4.16 | 2026-05-29 | **v4.4 ST-03 — execution_prompt.md v3.32→v3.33 deviations_filed auto-set on delegation clearance.** §8 source prompt header updated v3.32→v3.33. §14 Execution Engine Source v3.32→v3.33. Change: §5.3 Protocol step 5 — when setting `sign_off_record.status = "cleared"` for a delegated story with no DEV-* record filed, also set `deviations_filed = true` in the same operation (BLG-GOV-73). Eliminates batch-correction pattern at sprint close for cleared delegated stories. Authority: Head of Specs Team (BLG-GOV-73, v4.4 ST-03). |
| 4.15 | 2026-05-29 | **v4.4 ST-02 — sprint_planning_prompt.md v3.7→v3.8 frontend classification fast-path.** §7 source prompt header updated v3.7→v3.8. §14 Sprint Planning Engine v3.7→v3.8. Change: BLG-GOV-72 frontend classification fast-path added to §3.1 delegation class assignment — three story types default to `autonomous`: (a) prop/state bug fix; (b) variable rename; (c) new section/component against locked spec with Playwright feasibility confirmed. `delegated_frontend` only when engine genuinely cannot complete; justification required in sprint_planning_notes.md. Authority: Head of Specs Team (BLG-GOV-72, 3rd recurrence, v4.4 ST-02). |
| 4.14 | 2026-05-29 | **v4.4 ST-01 — roadmap_prompt.md v6.5→v6.6 STEP 8.1 empty Now horizon advisory.** §6 source prompt header updated v6.5→v6.6. §14 Roadmap Engine Source v6.5→v6.6. Change: STEP 8.1 added (between STEP 8 and STEP 8.5) — advisory for Extended-tier no-change rebalances where Now horizon is empty and no next-release section exists: PO advised to add next-release section to prevent repeated STEP -1.2 gate fires in Release Planning Engine. Non-blocking. Authority: Head of Specs Team (BLG-GOV-71, 3rd recurrence, v4.4 ST-01). |
| 4.10 | 2026-05-28 | **Branch safety hard gate added to delivery_verification_prompt.md v2.7→v2.8 and post_ship_closure.md v2.11→v2.12.** §9 source prompt header updated v2.7→v2.8. §10 source prompt header updated v2.11→v2.12. §14 Verification Engine Source v2.7→v2.8. §14 Post-Ship Closure Engine v2.11→v2.12. §14 Version 4.09→4.10/2026-05-28. Change: STEP -1 of both prompts now opens with a Branch Safety Check (Hard Gate) — `git branch --show-current` must return `main`; if not, halt with instructions to checkout main and re-invoke. Prevents governance artefacts from being committed to exec branches (root cause of v4.1 post-ship artefacts landing on exec/v4.1/EPIC-03 after PR merge). Authority: Head of Specs Team (2026-05-28). |
| 4.09 | 2026-05-27 | **Throughput improvement — post_ship_closure.md v2.10→v2.11 — rebalance cadence advisory.** §10 source prompt header updated v2.10→v2.11. §14 Post-Ship Closure Engine v2.10→v2.11. §14 Version 4.08→4.09/2026-05-27. Change: STEP 0 — Rebalance Cadence Check added (advisory, non-blocking): if `completed_cycle_count % 2 == 0` emit "REBALANCE DUE" advisory; if odd emit "REBALANCE SKIP — proceed directly to plan release". Rationale: rebalances run every 2nd cycle to reduce governance overhead and increase release throughput; PO may override on any cycle. Advisory Summary Block description updated to include rebalance cadence as a source. Authority: Product Owner (2026-05-27). |
| 4.08 | 2026-05-27 | **AUD-2026-05-27-002: execution_prompt.md v3.29→v3.30 — STEP 5.0A null pr_number recovery.** §8 source prompt header updated v3.29→v3.30. §14 Execution Engine Source v3.29→v3.30. §14 Version 4.07→4.08/2026-05-27. Change: STEP 5.0A extended with Step 1 (pr_number recovery): before pr_status sync, if EPIC.pr_number is null or 0, run `gh pr list --search "[EPIC-xx]" --state merged` to recover the PR number; if found, record it in execution_state.json; if not found, record "not_found" and log process gap in sprint_close.md (non-blocking). Resolves v4.1 P3-01 carry-forward (2nd recurrence: v4.0 EPIC-02 + v4.1 EPIC-03 required manual git log scan for null pr_number). Authority: Head of Specs Team (AUD-2026-05-27-002, 2026-05-27). |
| 4.07 | 2026-05-27 | **AUD-2026-05-27 Tier 1 improvements — §14 Version field fix + execution_prompt.md v3.28→v3.29 STEP 5.2 clarification.** §8 source prompt header updated v3.28→v3.29. §14 Execution Engine Source v3.28→v3.29. §14 Version field corrected 4.02→4.07 (4.02 was stale — entries 4.03–4.06 had updated the header but not the §14 metadata table rows; AUD-2026-05-27-001 fix). §14 Version 4.06→4.07/2026-05-27. Changes: (AUD-2026-05-27-001) §14 Version/Last Updated metadata table rows corrected from 4.02/2026-05-25 to 4.07/2026-05-27. (AUD-2026-05-27-003) execution_prompt.md STEP 5.2 — `returned_to_backlog` in-flight transition note added: clarifies that PO-authorized deferrals apply in-flight and do not require waiting until sprint close; records v4.1 P3-05 carry-forward resolved. Authority: Head of Specs Team (AUD-2026-05-27 Tier 1 closure, 2026-05-27). |
| 4.05 | 2026-05-27 | **ST-03 (EPIC-01, v4.1) OA-04: delivery_verification_prompt.md v2.5→v2.6 — STEP -1.3A PR number recovery null guard.** §9 source prompt header updated v2.5→v2.6. §14 Verification Engine Source v2.5→v2.6. §14 Version 4.04→4.05/2026-05-27. Change: STEP -1.3A (new sub-step) added to preflight: before any PR-dependent check proceeds, verify all EPICs in `epics_merged` have non-null `pr_number`; if null, recover via `gh pr view exec/<cycle_id>/EPIC-xx --json number,state,mergedAt`; record recovered number in execution_state.json; if no PR found, flag as process gap in report. Prevents delivery verification failure when `pr_number = null` in execution_state.json (OA-04, v4.0). Authority: Head of Specs Team (OA-04, v4.1 ST-03, 2026-05-27). |
| 4.04 | 2026-05-27 | **ST-02 (EPIC-01, v4.1) OA-02: sprint_planning_prompt.md v3.6→v3.7 + shared_standards.md v3.3→v3.4 — staging-only AC designation elevated to mandatory seal gate.** §7 source prompt header updated v3.6→v3.7. §14 Sprint Planning Engine v3.6→v3.7; Shared Standards v3.3→v3.4. §14 Version 4.03→4.04/2026-05-27. Changes: (sprint_planning_prompt.md v3.7) STEP 6.2 Sign-Off Gate — new mandatory condition added: "Staging-only AC check" requires `**Staging-only ACs:**` field to be populated for any story whose backlog slice ACs carry `[staging-only evidence]`; `None` when staging-only ACs exist is a seal blocker. Addresses 2nd-recurrence OA-02 (v3.9 + v4.0): staging-only ACs were reaching execution without tagging. (shared_standards.md v3.4) §16.11 ST-xx template — `**Staging-only ACs:**` field description updated from implied-optional to [REQUIRED] with explicit "None only when all ACs verifiable in CI" rule and seal-gate notice. Authority: Head of Specs Team (OA-02, v4.1 ST-02, 2026-05-27). |
| 4.03 | 2026-05-27 | **ST-01 (EPIC-01, v4.1) OA-01: execution_prompt.md v3.27→v3.28 — STEP 4 merge-gate re-invocation elevated to hard gate.** §8 source prompt header updated v3.27→v3.28. §14 Execution Engine Source v3.27→v3.28. §14 Version 4.02→4.03/2026-05-27. Change: STEP 4 item 4 — "Output user-facing re-invocation reminder" (advisory) replaced with "[HARD GATE — HALT after every EPIC merge]": engine must stop after each merge, output re-invocation block, and wait for user to re-invoke `run sprint`; engine may not auto-advance to next EPIC or STEP 5 within the same invocation. Addresses 2nd-recurrence OA-01 (v3.9 + v4.0): merge-gate re-invocation was advisory only, allowing engine to proceed without user confirmation. Authority: Head of Specs Team (OA-01, v4.1 ST-01, 2026-05-27). |
| 4.02 | 2026-05-25 | **BLG-GOV-55 (OA-01, 2026-05-25__scheduled): CLAUDE.md §2 — API contract same-sprint delivery rule.** New rule added: every new API endpoint added to `backend/routers/` must have a corresponding `## METHOD /path` entry in a file in `docs/specs/api_contracts/` in the same sprint; complements the existing same-commit `openapi.yaml` requirement; endpoints shipped without a contract constitute spec debt and must be resolved before the next sprint planning seals. §14 Version 4.01→4.02, Last Updated 2026-05-22→2026-05-25. Authority: Head of Specs Team (OA-01, 2026-05-25__scheduled, 2026-05-25). |
| 4.01 | 2026-05-22 | **BLG-GOV-31 (OA-01, 2026-05-22__scheduled): sprint_planning_prompt.md v3.4→v3.6 — staging-only AC designation + gate-conditional deferred items advisory.** §7 source prompt header updated v3.4→v3.6. §14 Sprint Planning Engine v3.4→v3.6. §14 Version 4.00→4.01/2026-05-22. Changes: (v3.5 LL-v3.9-P3-2) §7 — staging-only evidence designation paragraph added: flag ACs that cannot be verified in CI with `[staging-only evidence]` at planning time; designation pre-stages backlog filing and prevents surprise P3 notations at execution. (v3.6 BLG-GOV-31) STEP 1 — §1.4 Gate-Conditional Deferred Items subsection added: when items are deferred at planning with a gate_condition, sprint_capacity.md must include a Conditional (Deferred) table; mandatory re-invocation advisory added. Authority: Head of Specs Team (OA-01, 2026-05-22__scheduled, 2026-05-22). |
| 4.00 | 2026-05-22 | **BLG-GOV-30 (OA-01, 2026-05-22__scheduled): shared_standards.md v3.2→v3.3 — staging_only_evidence field in §16.11 sprint_backlog.md Schema.** §14 Shared Standards v3.2→v3.3. §14 Version 3.99→4.00/2026-05-22. Change: §16.11 ST-xx item template — `**Staging-only ACs:**` field added after `**Notes:**`; documents the `[staging-only evidence]` tag from sprint_planning_prompt.md §7 (LL-v3.9-P3-2) within the canonical sprint backlog schema so the Execution Engine can identify ACs requiring human staging sign-off. Authority: Head of Specs Team (OA-01, 2026-05-22__scheduled, 2026-05-22). |
| 3.99 | 2026-05-22 | **execution_prompt.md v3.26→v3.27 — STEP 4 merge gate state sync on session resume (OA-03, v3.9 post-ship closure LL-v3.9-P3-1).** §8 source prompt header updated v3.26→v3.27. §14 Execution Engine Source v3.26→v3.27. §14 Version 3.98→3.99/2026-05-22. Change: STEP 4 — merge gate state sync block added at section entry: when invoking in a fresh session, check `gh pr view` for each EPIC in `epics_pending`; if `mergedAt` non-null, update `epics_merged`/`epics_pending`/`pr_status` before proceeding; if all merged, skip to STEP 5 directly. Prevents stale merge_gate state when EPICs merge between sessions. Authority: Head of Specs Team (OA-03, v3.9 post-ship closure, 2026-05-22). |
| 3.98 | 2026-05-22 | **Governance patches v3.9 (EPIC-04 ST-09/ST-10/ST-11/ST-12) — dry-run support + PR template + prompt versions.** §6B source prompt header v2.30→v2.31; §9 source prompt header v2.4→v2.5. §14 Release Engine Source v2.30→v2.31; Verification Engine Source v2.4→v2.5; PR DoQ Enforcement Template v1.1→v1.2; Shared Standards v3.1→v3.2. §14 Version 3.97→3.98/2026-05-22. Changes: release_planning_prompt.md + delivery_verification_prompt.md — dry-run detection blocks added (ST-11); shared_standards.md §13 dry-run table extended (ST-11); pull_request_template.md v1.2 — combined QA evidence + DoQ Date checklist item (ST-12/CF-3). Authority: Head of Specs Team (EPIC-04 v3.9 governance patches, 2026-05-22). |
| 3.97 | 2026-05-21 | **roadmap_prompt.md v6.4→v6.5 — STEP 12.1 artefact existence precondition.** §6 source prompt header updated v6.4→v6.5. §14 Roadmap Engine Source v6.4→v6.5. §14 Version 3.96→3.97/2026-05-21. Change: STEP 12.1 Global State Update — artefact existence precondition added (hard gate): before updating `last_rebalance_cycle` in state file, verify `run_manifest.md`, `cycle_record.md`, `cycle_summary.md`, `lessons_learnt.md` exist in the cycle directory; halt and complete missing artefact if absent. Resolves Type D pattern (2 consecutive cycles with state file updated but no cycle artefacts committed). Authority: Head of Specs Team (cycle 2026-05-21__scheduled action-now, 2026-05-21). |
| 3.96 | 2026-05-21 | **AUD-2026-05-21 Tier 1 improvements applied — 4 governance prompt patches + §13 register + dry-run table.** `execution_prompt.md` v3.25→v3.26: STEP 1 gh issue create now uses structural `gh issue list` check before creating (eliminates duplicate issues, closes v3.8 OA-1); §3.1.A step 1 + step 12 test_scenarios scoped to EPIC-specific files only (closes AUD-003); §3.1.B delegated_frontend — createPageUrl map requirement added for new page route delegations (closes AUD-005/OA-2). `sprint_planning_prompt.md` v3.3→v3.4: STEP 5.2 planning-deferred item traceability rule added — all slice items not in sealed sprint backlog must be recorded as `deferred_at_planning` in execution_state.json with gate_condition note (closes AUD-002). `shared_standards.md` v3.0→v3.1: §13 dry-run table — `run ideas housekeeping` row added (closes AUD-007). `OPERATIONAL_GUIDE.md` §13: Shared Governance Modules and Governance Changelogs rows added as Class 6 sub-type artefacts (closes AUD-006). §7 source prompt header v3.3→v3.4; §8 source prompt header v3.25→v3.26; §14 Sprint Planning Engine v3.3→v3.4; Execution Engine Source v3.25→v3.26; Shared Standards v3.0→v3.1; §14 Version 3.95→3.96/2026-05-21. Authority: Head of Specs Team (AUD-2026-05-21 Tier 1 closure, 2026-05-21). |
| 3.95 | 2026-05-21 | **Prompt compression: governance_preamble.md v1.0 (new) + 6-engine version bumps.** New shared module `claude/system/shared/governance_preamble.md` consolidates Write Scope pattern, Agent Integrity verification procedure, and 8 cross-engine Governance Invariants previously duplicated across all 6 phase prompts. All 6 prompts updated to reference preamble sections — verbose inline blocks replaced with compact references + phase-specific additions only. preflight_common.md v1.0→v1.1: Roadmap Rebalance added to covered engines. YAML schema blocks replace narrative bullet lists for all state.json output descriptions in execution_prompt.md and release_planning_prompt.md. §6 source prompt header v6.3→v6.4; §6B v2.29→v2.30; §7 v3.2→v3.3; §8 v3.24→v3.25; §9 v2.3→v2.4; §10 v2.9→v2.10. §14 Governance Preamble row added; all 6 engine versions updated; §14 Version 3.94→3.95/2026-05-21. Authority: Head of Specs Team (prompt compression 2026-05-21). |
| 3.94 | 2026-05-21 | **OA-3 (v3.8 closure): `.github/pull_request_template.md` v1.0→v1.1 — QA evidence branch-commit enforcement.** §14 PR DoQ Enforcement Template v1.0→v1.1. §14 Version 3.93→3.94/2026-05-21. Changes: QA Evidence section — added explicit branch-commit checklist item requiring `git status`/`git log` verification that qa_evidence file is committed on the branch before PR opens; added explanatory callout block stating retroactive creation after PR open is a process deviation; DoQ Sign-Off Confirmation — split into two separate checklist items (branch-commit confirmation + Date non-blank confirmation). Authority: Director of Quality (OA-3, v3.8 post-ship closure, 2026-05-21). |
| 3.93 | 2026-05-20 | **roadmap_prompt.md v6.2→v6.3 — 3-cycle hard cap on parked ideas + Backlog (gate-conditional) classification.** §6 source prompt header updated v6.2→v6.3. §14 Roadmap Engine Source v6.2→v6.3. §14 Version 3.92→3.93/2026-05-20. Changes: §4.1 — new 📋 Backlog (gate-conditional) classification added (idea exits parked queue, added to backlog.md with gate criteria block); park rationale validation gate added (Facilitator must challenge vague rationales; second vague park defaults to Reject); stale idea note updated to reference §4.5 hard cap. §4.2 — Promoted-Backlog row added to document management table. §4.5 — "no cap on re-parks" removed; replaced with 3-cycle hard cap (cycles 1–2 allow re-park with valid rationale; cycle 3 forces terminal outcome: Advance, Reject, or Backlog gate-conditional). Authority: Head of Specs Team (2026-05-20). |
| 3.92 | 2026-05-19 | **ST-10 (EPIC-04, v3.8): gh_issue_template.md + DoQ enforcement mechanism.** §14 GitHub Issue Template row added (`claude/system/gh_issue_template.md` v1.0); PR DoQ Enforcement Template row added (`.github/pull_request_template.md` v1.0). `.github/pull_request_template.md` created with DoQ sign-off date enforcement checklist — prevents retrospective sign-off gaps by requiring non-blank Date in qa_evidence EPIC sign-off block before PR can merge. §14 Version 3.90→3.92/2026-05-19 (3.91 was applied to changelog 2026-05-18 but §14 self-metadata Version field was not updated at that time — corrected here). Authority: Head of Specs Team (ST-10, 2026-05-19). |
| 3.91 | 2026-05-18 | **execution_prompt.md v3.23→v3.24 — ST-07 (EPIC-03, v3.7): three lessons-learnt patches.** §8 source prompt header updated v3.23→v3.24. §14 Execution Engine Source v3.23→v3.24. §14 Version 3.90→3.91/2026-05-18. Changes: (LL-v3.7-EX-01) §3.1.A step 10a — deviations_filed atomic write: write `deviations_filed: true` immediately after step 10 deviation check; do not defer. (LL-v3.7-EX-02) §3.1.A step 10b — backlog verify guidance: verify backlog item appears in backlog.md before closing story when mandatory deferred staging AC is filed. (LL-v3.7-EX-03) §3.1.A step 2a — spec_references path verify: verify each path exists on disk before recording in execution_state.json; prevents false traceability from non-existent paths. Authority: Head of Specs Team (ST-07, 2026-05-18). |
| 3.90 | 2026-05-17 | **Governance pattern consolidation — preflight common checks extracted to `shared/preflight_common.md` v1.0.** §6B source prompt header updated v2.28→v2.29. §8 source prompt header updated v3.22→v3.23. §9 source prompt header updated v2.2→v2.3. §10 source prompt header updated v2.8→v2.9. §14 Release Engine Source v2.28→v2.29; Execution Engine Source v3.22→v3.23; Verification Engine Source v2.2→v2.3; Post-Ship Closure Engine v2.8→v2.9. §14 Version 3.89→3.90/2026-05-17. Changes: Required Files Present, Required Authority Roles Exist, and Write Permission Test blocks extracted from STEP -1 preflight sections of release_planning (−1.1/−1.3/−1.4), execution (−1.1/−1.6/−1.7), delivery_verification (−1.4), and post_ship_closure (−1.4/−1.5/−1.6) into new shared module `claude/system/shared/preflight_common.md`. Each engine now invokes the module with engine-specific parameter blocks; engine-specific advisories remain inline. Sprint Planning excluded (different numbered-list preflight style). Authority: Head of Specs Team (governance pattern consolidation 2026-05-17). |
| 3.89 | 2026-05-16 | **execution_prompt.md v3.21→v3.22 — ST-09/ST-10 (EPIC-04, v3.6): §13 gate story pattern + OA-RP-01–04 closure.** §8 source prompt header updated v3.21→v3.22. §14 Execution Engine Source v3.21→v3.22. §14 Version 3.88→3.89/2026-05-16. Changes: §5.1 — §13 gate story pattern (LL-v3.5-SP-01) added: when an arc feature requires a strategy/compliance review gate, scope the review as Sprint 1 `delegated_decision` story gating implementation stories to Sprint 2; validated in v3.5 IT-06. ST-10 patches (deviations_filed semantics, §5.3 three-field verification readiness block, §5.4 lessons_learnt_cycle.md reference) confirmed pre-met in v3.21 — no additional changes required. Authority: Head of Specs Team (ST-09+ST-10, 2026-05-16). |
| 3.88 | 2026-05-16 | **execution_prompt.md v3.20→v3.21 — STEP 1 simplified to verify-only.** §8 source prompt header updated v3.20→v3.21. §14 Execution Engine Source v3.20→v3.21. §14 Version 3.87→3.88/2026-05-16. Change: STEP 1 (GitHub Issue Preflight) changed from issue creator to verifier — `sync gh` at sprint planning seal is now the canonical issue creation point; STEP 1 records issue numbers and notes a process gap if any are missing, but does not halt; minimal fallback creation retained for resilience. Authority: Head of Specs Team (2026-05-16). |
| 3.87 | 2026-05-16 | **sprint_planning_prompt.md v3.1→v3.2 — `sync gh` integrated as final step of STEP 8.** §7 source prompt header updated v3.1→v3.2. §14 Sprint Planning Engine v3.1→v3.2. §14 Version 3.86→3.87/2026-05-16. Change: STEP 8 (Commit) — after successful push, `sync gh` (CLAUDE.md §4) is called to create GitHub issues for all ST items with correct `v<X.Y>`, `sprint-N`, and `EPIC-xx` labels. This makes sprint planning the canonical issue creation point; execution STEP 1 is now verify-only. Authority: Head of Specs Team (2026-05-16). |
| 3.86 | 2026-05-16 | **ideas_housekeeping_prompt.md v1.0 (new) + post_ship_closure.md v2.7→v2.8 + roadmap_prompt.md v6.1→v6.2.** New Ideas Housekeeping Engine added: archives terminal ideas register rows, reviews rejected-but-strong revival conditions, runs pipeline health check. Absorbs inline post-ship "Ideas Pipeline Health Check" advisory. §6M source prompts header updated to include ideas_housekeeping_prompt.md v1.0. §6M.3 Ideas Housekeeping Engine section added; former §6M.3 Exit Criteria renumbered §6M.4 (updated to include ideas housekeeping criteria). Quick Reference Phase 1M command block updated. §5.5 Artefacts table: ideas_register_archive.md row added. Phase 1M enforcement note updated (STEPs 11/12/12.5). §14: Ideas Housekeeping Engine v1.0 added; Post-Ship Closure Engine v2.7→v2.8; Roadmap Engine Source v6.1→v6.2. CLAUDE.md command table: `run ideas housekeeping` added. Authority: PMO Lead + Head of Specs Team (2026-05-16). |
| 3.85 | 2026-05-15 | **delivery_verification_prompt.md v2.1→v2.2 — Phase 4 token efficiency refactor.** §9 source prompt header updated v2.1→v2.2. §14 Verification Engine Source v2.1→v2.2. §14 Version/Last Updated 3.84→3.85/2026-05-15. Changes: (1) §1 "This routine does NOT" block removed — covered by write scope §5; (2) ESCALATION SUBROUTINE compressed to 4-line inline block; (3) STEP -1 parallel read instruction added (execution_state.json + sprint_close.md + all qa_evidence files in parallel); (4) STEP 4.3 stale parked detection short-circuited when zero parked items in backlog slice; (5) STEP 5.2 short-circuit added — autonomous/backend-only EPICs with no frontend-visible AC record not_applicable in TSG table, skip verbose feedback block; (6) STEP 8 §3 QA Evidence Summary mandated as table (was prose); (7) STEP 8 §5 Outstanding Items mandated as table-only; (8) STEP 8 §6 compressed instruction — "No test scenario gaps" one-liner when all not_applicable; (9) STEP 8 §8 Open Items — explicit omit instruction when status is not Not_Verified; (10) §8 Completion Condition compressed to 2-sentence rule; (11) §9 Governance Invariants reduced from 8 to 3 (removed 5 that restated step-level rules). All hard gates, severity policy, and invariants preserved. Authority: Head of Specs Team (2026-05-15). |
| 3.84 | 2026-05-15 | **execution_prompt.md v3.19→v3.20 — ST-12+ST-13 (EPIC-04, v3.5): deviation advisory patches + sprint close consistency checks.** §8 source prompt header updated v3.19→v3.20. §14 Execution Engine Source v3.19→v3.20. §14 Version/Last Updated 3.83→3.84/2026-05-15. Changes: (ST-12/LL item #3) §3.1.A step 10 — intent check advisory added: verify spec intent match before filing deviation; record as implementation note if intent agrees. (ST-12/LL item #4) §3.1.A step 10 — Known Deviations section advisory: add `## Known Deviations` section to canonical spec in same commit when filing deviation. (ST-12/LL item #5) §5.4 — backlog ID pre-assignment check: verify BLG ID unoccupied in backlog.md before assigning in lessons_learnt Phase 3. (ST-13/CF-01) §5.3 — deviation severity consistency check: verify deviation priorities in sprint_close.md match DoQ assessment in qa_evidence. (ST-13/CF-02) §5.3 — backlog ID completeness check: every "backlog item filed" note must include BLG ID. Authority: Head of Specs Team (ST-12+ST-13, 2026-05-15). |
| 3.83 | 2026-05-15 | **sprint_planning_prompt.md v3.0→v3.1 — BLG-GOV-22: multi-EPIC execution_state.json ownership + merge order advisory.** §7 source prompt header updated v3.0→v3.1. §14 Sprint Planning Engine v3.0→v3.1. §14 Version/Last Updated 3.80→3.83/2026-05-15. Changes: STEP 5.2 — multi-EPIC `execution_state.json` ownership rule added (first EPIC in execution order is owner; others check for existence before creating; record in sprint_planning_notes.md); shared file ownership advisory added (identify shared files across EPICs; record ownership and rebase advisory in sprint_planning_notes.md). STEP 6.1 — merge order section requirement added (sprint backlog must include EPIC merge sequence, execution_state.json owner designation, and shared file advisory when > 1 EPIC in scope). Authority: Head of Specs Team (ST-11, BLG-GOV-22, 2026-05-15). |
| 3.82 | 2026-05-15 | **execution_prompt.md v3.18→v3.19 — token efficiency refactor.** §8 source prompt header updated v3.18→v3.19. §14 Execution Engine Source v3.18→v3.19. |
| 3.81 | 2026-05-15 | **sprint_planning_prompt.md v2.9→v3.0 + shared_standards.md v2.9→v3.0 — Phase 2 token efficiency refactor.** §7 source prompt header updated v2.9→v3.0. §14 Sprint Planning Engine v2.9→v3.0. §14 Shared Standards v2.9→v3.0. Changes: (sprint_planning_prompt) STEP 5 inline sprint_planning_notes.md template replaced with `shared_standards.md §16.10` reference; STEP 6.1 inline sprint_backlog.md template replaced with `shared_standards.md §16.11` reference (~580 words removed from prompt). (shared_standards) §16.10 sprint_planning_notes.md schema added; §16.11 sprint_backlog.md schema added — canonical homes for both templates, reusable by other engines. Authority: Head of Specs Team (2026-05-15). |
| 3.80 | 2026-05-15 | **sprint_planning_prompt.md v2.8→v2.9 — Phase 1 token efficiency refactor.** §7 source prompt header updated v2.8→v2.9. §14 Sprint Planning Engine v2.8→v2.9. Changes: STEP -1 restructured from 12 sequential substeps to 2 categories (Hard Gates + Advisory Checks) — removes verbose rationale blocks and merges -1.4 through -1.8 into a single parallel-checkable block (~650 words saved); §8 Capacity Standard compressed (~50 words); STEP 3.1 LL-pattern blocks compressed in place (~140 words); §12 Governance Invariants compressed with cross-ref line (~70 words). All governance rules preserved. Authority: Head of Specs Team (2026-05-15). |
| 3.79 | 2026-05-15 | **roadmap_prompt.md v6.0→v6.1 — STEP 9 post-write park count verification added.** §6 source prompt header updated v6.0→v6.1. §14 Roadmap Engine Source v6.0→v6.1. §15 roadmap_prompt version reference updated v5.0→v6.1. Change: STEP 9 Post-write park count verification block added — after completing ideas_register.md park count updates, grep for rows with prior cycle's `Parked-cycle-N \| N` pattern and confirm zero rows remain with outdated counts; prevents context-compaction truncation artifacts from leaving stale park counts. Authority: Head of Specs Team (cycle 2026-05-15__scheduled lessons learnt action-now, 2026-05-15). |
| 3.78 | 2026-05-15 | **backlog_management_prompt.md v1.6→v1.7 — STEP 1.5 Ephemeral Section Cleanup added.** §6M source prompt header updated v1.6→v1.7. §14 Backlog Management Engine v1.6→v1.7. §14 Version/Last Updated 3.74→3.78/2026-05-15. Change: STEP 1.5 added — during each groom run, identify and queue removal of completed Release Slice sections, resolved Test Scenario Gap sections, and resolved "Returned to Backlog" sections; open items within ephemeral sections must be extracted to appropriate §1–§8 type section before parent section is removed. Companion: backlog.md Placement Rule updated to document ephemeral section lifecycle. Authority: PMO Lead (2026-05-15). |
| 3.77 | 2026-05-14 | **release_planning_prompt.md v2.27→v2.28 — token efficiency refactor.** §6B source prompt header already updated v2.28. §14 Release Engine Source v2.28. Prompt reduced from 1438 to 1041 lines (−397 lines, ~28%): extracted state.json schema to `claude/system/schemas/release_state_schema.json`; escalation subroutine to `claude/system/shared/escalation_subroutine.md`; lock recovery procedure to `claude/system/shared/lock_recovery_procedure.md`; publish gate to `claude/system/shared/publish_gate.md`; scope + decisions templates to `claude/system/templates/`; consolidated STEP 5.5+5.7; removed 5 trigger footnotes. All governance rules preserved. Authority: Head of Specs Team (2026-05-14). |
| 3.76 | 2026-05-14 | **BLG-AI-03 (ST-13, v3.4) — AI Journal Review Cadence added to §13 Artefact Register.** New artefact row: `docs/specs/compliance/ai_journal_review_cadence.md` (Class 2, AI Compliance & Governance Officer, Governance). Defines quarterly review checklist, §13 re-confirmation, model version check, error rate review, record format, escalation path. Authority: AI Compliance & Governance Officer (BLG-AI-03, 2026-05-14). |
| 3.75 | 2026-05-13 | **execution_prompt.md v3.17→v3.18 — AUD-2026-05-13-002 template fix.** §8 source prompt header updated v3.17→v3.18. §14 Execution Engine Source v3.17→v3.18. Change: §5.4 header advisory note added — when creating lessons_learnt_cycle.md, must use `Class: Operational Record (Class 3)` not `Planning Document (Class 4)`; prevents recurrence of class declaration mismatch (third instance: v2.7 fixed by AUD-2026-04-20-004; v3.3 discovered by AUD-2026-05-13). Authority: Head of Specs Team (AUD-2026-05-13-002, 2026-05-13). |
| 3.74 | 2026-05-13 | **roadmap_prompt.md v5.1→v6.0 — token efficiency refactor.** §6 source prompt header updated v5.1→v6.0. §14 Roadmap Engine Source v6.0. §15 roadmap_prompt version reference updated. Prompt reduced from ~1,651 to 738 lines (−913 lines); BLG-GOV-08 partially addressed. Authority: Head of Specs Team (2026-05-13). |
| 3.73 | 2026-05-10 | **sprint_planning_prompt.md v2.7→v2.8 + backlog_management_prompt.md v1.5→v1.6 — ST-14 (EPIC-04, v3.3): two OA patches.** §7 source prompt header updated v2.7→v2.8. §6M source prompt header updated v1.5→v1.6. §14 Sprint Planning Engine v2.7→v2.8. §14 Backlog Management Engine v1.5→v1.6. Changes: (OA-05) sprint_planning_prompt.md STEP -1.12 added — "Before Sprint Planning" Backlog Items Check: advisory scan for items with `Provisional-Target: Before v<X.Y> sprint planning`; surfaces unconverted items to Product Owner; recorded in sprint_planning_notes.md; non-blocking. (OA-03/CF-03) backlog_management_prompt.md STEP 3.5 added — Deferral Age Validation: flags items deferred 3+ consecutive cycles without named PO re-deferral; PO re-deferral format defined; health-check blocker until actioned. Policy document `docs/governance/backlog_deferral_policy.md` v1.0 created. Authority: Head of Specs Team (sprint_planning) + PMO Lead (backlog_management) (ST-14, 2026-05-10). |
| 3.72 | 2026-05-10 | **execution_prompt.md v3.16→v3.17 — ST-13 (EPIC-04, v3.3): two OA patches.** §8 source prompt header updated v3.16→v3.17. §14 Execution Engine Source v3.16→v3.17. Changes: (1) OA-01/CF-01 — STEP 0 Sealed-file integrity check added (hard gate): at each EPIC session start, `git diff --name-only HEAD` and `--cached` are checked against sealed cycle files (stage4_backlog_slice.md, release_plan.md, state.json, amended slice if present); if any sealed file appears in diff output, halt with `[HALT] Sealed file modified: {filename}`. No bypass. (2) OA-02/CF-02 — §14 Playwright Test Authoring Standard gains Mock payload advisory: mocks must match canonical openapi.yaml response shape; nested objects must not be flattened; mismatch = silent test failure in prod. Authority: Head of Specs Team (ST-13, 2026-05-10). |
| 3.71 | 2026-05-09 | **Modular prompt refactor — three missing Class 6 prompts updated.** `design_gate_prompt.md` v1.2→v1.3, `idea_intake_prompt.md` v2.2→v2.3, `lessons_learnt_prompt.md` v1.8→v1.9: §3 Canonical Governance Sources replaced with reference to `claude/system/shared/governance_stack.md`; Change Log sections replaced with references to `claude/system/changelogs/`; version headers bumped. §6.5 source prompt header updated v1.2→v1.3. §5 source prompt header updated v2.2→v2.3. §14 governance table: Design Gate Engine v1.2→v1.3, Idea Intake Engine v2.2→v2.3, Lessons Learnt Prompt v1.8→v1.9. Authority: Head of Specs Team (modular prompt refactor continuation, 2026-05-09). |
| 3.70 | 2026-05-09 | **Modular prompt refactor — changelog extraction and governance stack consolidation.** All 10 phase prompts refactored: (1) Historical change logs extracted to `claude/system/changelogs/` directory (one file per prompt). (2) §3 (or equivalent) Canonical Governance Sources block in each prompt replaced with reference to new `claude/system/shared/governance_stack.md` (shared canonical location). (3) roadmap_prompt.md §1 + §2 consolidated into single §1 governance reference. All phase prompt headers, §14 governance table, and phase section source prompt headers updated to new versions. New files created: `claude/system/shared/governance_stack.md`, 10 changelog files in `claude/system/changelogs/`. Authority: Head of Specs Team (modular prompt refactor 2026-05-09). |
| 3.69 | 2026-05-09 | **execution_prompt.md v3.14→v3.15 — post-ship closure v3.2: two action-now patches.** §8 source prompt header updated v3.14→v3.15. §14 Execution Engine Source v3.14→v3.15. §14 Version/Last Updated 3.68→3.69/2026-05-09. Changes: (1) LL-v3.2-P3-02 — §3.1.A step 13 Cross-spec selector check added: when a story modifies/removes/renames a DOM element, scan all existing Playwright specs for stale selectors and update in the same commit; prevents CI failures from UI changes in unrelated tests. (2) LL-v3.2-P4-01 — §3.2.A BLG-GOV-19 sign-off block template strengthened: explicit 4-criterion checklist with ✓/✗ markers added; Criterion 3 requires positive assertion checking src/pages/ and src/components/; prevents autonomous class misapplication on frontend EPICs. Authority: Head of Specs Team (post-ship closure v3.2, 2026-05-09). |
| 3.68 | 2026-05-06 | **execution_prompt.md v3.13→v3.14 — ST-08 + ST-09 + ST-10 (EPIC-03, v3.2): three OA patches.** §8 source prompt header updated v3.13→v3.14. §14 Execution Engine Source v3.13→v3.14. §14 Version/Last Updated 3.67→3.68. Changes: (1) ST-08/OA-03 — STEP 5.1 deviations_filed enforcement check; (2) ST-09/OA-04 — §3.1.A step 12 post-story test files check; (3) ST-10/OA-05 — §14 Playwright Test Authoring Standard: networkidle prohibited, waitFor/element patterns required; all networkidle usages in tests/e2e/ replaced. Authority: Head of Specs Team (ST-08+09+10, 2026-05-06). |
| 3.67 | 2026-05-06 | **sprint_planning_prompt.md v2.5→v2.6 — ST-07 (EPIC-03, v3.2): STEP 0 Branch Safety Check.** §7 source prompt header updated v2.5→v2.6. §14 Sprint Planning Engine v2.5→v2.6. §14 Version/Last Updated corrected to current (3.67/2026-05-06). Change: STEP 0 Branch Safety Check (Hard Gate) added — verifies `git branch --show-current` equals `main` before sprint planning proceeds; halts with branch name if not; prevents orphaned artefacts. Authority: Head of Specs Team (ST-07, 2026-05-06). |
| 3.66 | 2026-05-01 | **execution_prompt.md v3.12→v3.13 — frontend testing hard gate (LL-v3.1-EX-01).** §8 source prompt header updated v3.12→v3.13. §14 Execution Engine Source v3.12→v3.13. Change: §3.2.A Frontend testing gate added — observable AC on frontend EPICs requires Playwright test coverage or human staging sign-off with date; "code review only" without a filed backlog item blocks PR open. CLAUDE.md §2 frontend DoQ rule strengthened to match. Playwright tests `screener-uk-suffix.spec.js` (SC-UK-01–04) and `earnings-calendar.spec.js` (SC-EARN-01–09) authored to close ST-06/ST-08 gaps. Authority: Head of Specs Team (2026-05-01). |
| 3.65 | 2026-04-30 | **execution_prompt.md v3.11→v3.12 — ST-13 + ST-14 (EPIC-04, v3.1): two CF patches.** §8 source prompt header updated v3.11→v3.12. §14 Execution Engine Source v3.11→v3.12. Changes: (1) ST-13/CF-01 — §3.1.A Reclassification backfill instruction: when a story is reclassified from `delegated_frontend` to `autonomous` mid-sprint, engine must backfill `test_scenarios` at time of reclassification; must be populated before QA evidence log entry is written. (2) ST-14/CF-02 — §5.4 Output target note: explicit warning that output target is `lessons_learnt_cycle.md` NOT `lessons_learnt.md` (Release Planning artefact); create if absent. Authority: Head of Specs Team (ST-13 + ST-14, 2026-04-30). |
| 3.64 | 2026-04-25 | **execution_prompt.md v3.10→v3.11 — ST-12 + ST-13 (EPIC-04, v3.0): execution_state.json ownership rule + test_scenarios advisory.** §8 source prompt header updated v3.10→v3.11. §14 Execution Engine Source v3.10→v3.11. Changes: (1) §2 — EPIC execution_state.json owner designation rule added for multi-EPIC sprints; first EPIC in execution order is owner; others check for file existence before creating; merge conflict advisory references CLAUDE.md §8. (2) §3.1.A step 1 — test scenarios advisory: when tests are created, populate test_scenarios in execution_state.json with test file paths; non-blocking; must be complete before STEP 3.2.A. Closes OA-v29-02 and OA-v29-03. Authority: Head of Specs Team (ST-12 + ST-13, 2026-04-25). |
| 3.63 | 2026-04-21 | **AUD-2026-04-20-002 — §14 Lifecycle Guide version corrected v2.5→v2.6.** §14 Lifecycle Guide row updated to reflect actual document_lifecycle_guide.md version (v2.6 — Class 4 sub-type 3 Release Plan added 2026-03-07; §14 not updated at that time). Authority: Head of Specs Team (AUD-2026-04-20, 2026-04-21). |
| 3.62 | 2026-04-18 | **execution_prompt.md v3.7→v3.8 — ST-05 (EPIC-03, v2.8): sprint close deviation register terminology.** §8 source prompt header updated v3.7→v3.8. §14 Execution Engine Source v3.7→v3.8. Change: §5.3 sprint close "Deviations filed" clarified — spec deviations only (filed via /dev-file); process notations and execution observations belong in execution_state.json notes or execution_escalations.md. Closes CF-2. Authority: Head of Specs Team (ST-05, 2026-04-18). |
| 3.61 | 2026-04-18 | **execution_prompt.md v3.6→v3.7 — ST-04 (EPIC-03, v2.8): DoQ Date field PR-open pre-condition.** §8 source prompt header updated v3.6→v3.7. §14 Execution Engine Source v3.6→v3.7. Change: §3.2.A Date field requirement note updated — now explicitly states Date must be non-blank before PR can be opened (§3.2.B pre-condition, BLG-GOV-18) in addition to before the merge gate runs. Closes the loop between the sign-off block authoring step and the PR-opening enforcement step. Authority: Head of Specs Team (ST-04, 2026-04-18). |
| 3.60 | 2026-04-17 | **roadmap_prompt.md v4.9→v5.0 + post_ship_closure.md v2.4→v2.5 — three pipeline patches applied.** §6 source prompt header updated v4.9→v5.0. §10 source prompt header updated v2.4→v2.5. §14 Roadmap Engine Source v4.9→v5.0; Post-Ship Closure Engine v2.4→v2.5. §15 roadmap_prompt.md version reference updated v4.9→v5.0. Changes: (1) roadmap_prompt.md STEP 0.D — Empty Horizon Advisory: when Now horizon is empty post-ship and active backlog items exist, surface advisory directing PO to run `plan release` rather than a full rebalance debate; (2) roadmap_prompt.md STEP 4.0 — Gate-Condition Re-Check: before per-idea classification, verify whether BLG- items referenced in Park Rationales have shipped; gate-cleared ideas surfaced as mandatory re-evaluation; (3) post_ship_closure.md STEP 12 — Ideas Pipeline Health Check advisory: when active backlog ≤ 5 items, scan for parked ideas with shipped gate conditions and record advisory in closure record. Authority: Product Owner (2026-04-17). |
| 3.59 | 2026-04-16 | **post_ship_closure.md v2.3→v2.4 — STEP 6 endpoint coverage drift check added.** §10 Post-Ship source prompt header updated v2.3→v2.4. §14 Post-Ship Closure Engine updated v2.3→v2.4. Change: STEP 6 advisory block added — after all PRs merged, compare openapi.yaml path count vs api_performance_baseline.md measured paths; raise backlog item for gaps; check SystemStatus.js categorizeEndpoint() for unhandled new top-level prefixes. Advisory-only, non-blocking. Authority: Head of Engineering. |
| 3.58 | 2026-04-16 | **ST-11 (BLG-GOV-14, v2.7) — Governance Health Score.** §15 added: three-component advisory indicator (Header Compliance %, Deferred Patch Indicator, Outstanding Action Count) with formula, age bands, and output format. roadmap_prompt.md v4.8→v4.9: STEP -1.7 added to compute and surface the score at each roadmap rebalance (advisory only — cannot halt). §6 source prompt header updated v4.8→v4.9. §14 Roadmap Engine Source updated v4.8→v4.9. Authority: Head of Specs Team (ST-11, 2026-04-16). |
| 3.57 | 2026-04-14 | **execution_prompt.md v3.5→v3.6 + delivery_verification_prompt.md v1.9→v2.0 — ST-04 (BLG-GOV-19): Autonomous DoQ sign-off class.** §8 source prompt header updated v3.5→v3.6. §9 source prompt header updated v1.9→v2.0. §14 Execution Engine Source v3.5→v3.6; Verification Engine Source v1.9→v2.0. Changes: (1) execution_prompt.md §3.2.A — Autonomous DoQ sign-off class defined with four qualifying criteria; when all criteria met, engine populates sign-off block with "Sprint Execution Engine (autonomous class)"; (2) delivery_verification_prompt.md STEP -1.3 Tier 2 — autonomous class exception added: if signer is "Sprint Execution Engine (autonomous class)" and all four criteria are met, treated as compliant sign-off (Tier 2 does not fire). Authority: Head of Specs Team (ST-04, BLG-GOV-19, 2026-04-14). |
| 3.56 | 2026-04-14 | **execution_prompt.md v3.4→v3.5 — ST-03 (BLG-GOV-18): PR gate on QA sign-off Date.** §8 source prompt header updated v3.4→v3.5. §14 Execution Engine Source updated v3.4→v3.5. Change: §3.2.B pre-condition added — engine must not open a PR until `qa_evidence_EPIC-xx.md` DoQ sign-off block has a non-blank Date field. `commit-check` skill updated — Check 8 added: QA sign-off Date completeness check fires when `qa_evidence_EPIC-xx.md` is staged. Authority: Head of Specs Team (ST-03, BLG-GOV-18, 2026-04-14). |
| 3.55 | 2026-04-13 | **execution_prompt.md v3.3→v3.4 — BLG-GOV-17 sprint-close trigger fix (third recurrence).** §8 source prompt header updated v3.3→v3.4. §14 Execution Engine Source updated v3.3→v3.4. Changes: (1) STEP 3.2.D post-merge reminder — removed conditional qualifier; unconditional re-invocation required after every EPIC merge including the final one; (2) `.github/workflows/sprint_close_reminder.yml` created — posts mandatory PR comment on EPIC merge to main. Authority: Head of Specs Team (OA-1, BLG-GOV-17, 2026-04-13). |
| 3.54 | 2026-04-11 | **ST-12/CF-1 + ST-13/CF-2 + ST-14 (EPIC-04, v2.6) — four governance prompt patches applied.** (1) execution_prompt.md v3.2→v3.3: §8 source prompt header updated; §14 Execution Engine Source updated. Change: STEP 5.1 Unpushed-Commit Check added — before sprint close, verify `git log --not origin/<branch>` is empty; soft gate if any qa_evidence commit is unpushed. (2) design_gate_prompt.md v1.1→v1.2: §6.5 source prompt header updated; §14 Design Gate Engine updated. Change: STEP 7 governance file edit check added (CF-2 carry-forward). (3) amendment_cycle_prompt.md v1.6→v1.7: §6B.8 source prompt header updated; §14 Amendment Cycle Engine updated. Change: STEP 9 governance file edit check added (CF-2 carry-forward). (4) roadmap_prompt.md v4.7→v4.8: §6 source prompt header updated; §14 Roadmap Engine Source updated. Changes: STEP 12 governance file edit check added (CF-2 carry-forward); STEP 9 decision_log decrease upgraded to STRUCTURAL HARD GATE (ST-14/BLG-GOV-15). §1 Hard Rules table: decision_log row updated to reflect structural gate enforcement. Authority: Head of Specs Team (ST-12/13/14, 2026-04-11). |
| 3.53 | 2026-04-11 | **post_ship_closure.md v2.2→v2.3 — velocity_metrics.md added to STEP 6.** §10 Post-Ship source prompt header updated v2.2→v2.3. §14 Post-Ship Closure Engine updated v2.2→v2.3. Change: STEP 6 operational documents list now includes `claude/cycles/velocity_metrics.md` — engine must append velocity row (Planned/Completed/rolling average) per cycle. Fixes gap that caused v2.4 and v2.5 rows to be missed. |
| 3.52 | 2026-04-11 | **AUD-2026-04-11-009 — release_planning_prompt.md v2.25→v2.26.** §6B Phase 1B source prompt header updated v2.25→v2.26. §14 Release Engine Source updated v2.25→v2.26. Change: STEP 1 §1.3 Design-Gate Language Scan added (advisory) — scans scope candidates for design-gate keywords at STEP 1 rather than catching at Pre-sprint Required Decisions checklist; non-blocking; results recorded in run manifest. Closes 4-cycle deferred-monitor carry (filed v2.3, 2026-03-24). Authority: Head of Specs Team (AUD-2026-04-11, 2026-04-11). |
| 3.51 | 2026-04-11 | **AUD-2026-04-11-006 + AUD-2026-04-11-010 — shared_standards.md v2.7→v2.8.** §14 Shared Standards version updated v2.7→v2.8. Changes: §13 dry-run table — `run design-gate` row added (was absent despite v1.1 dry-run support since 2026-03-07); §16.9 ideas_window.json Schema added — canonicalises `per_agent_submission_count` field. Authority: Head of Specs Team (AUD-2026-04-11, 2026-04-11). |
| 3.50 | 2026-04-11 | **AUD-2026-04-11-005 — delivery_verification_prompt.md v1.8→v1.9.** §9 Phase 4 source prompt header updated v1.8→v1.9. §14 Verification Engine Source updated v1.8→v1.9. Change: STEP -1.3 sign-off check upgraded to two-tier STRUCTURAL — Tier 1 (BLANK) = HALT; Tier 2 (WRONG AUTHORITY) = FLAG + DoQ counter-sign required + compliance advisory in run_manifest. Resolves STALE 2-cycle deferred patch (v2.4 Phase 4 lessons learnt). Authority: Head of Specs Team (AUD-2026-04-11, 2026-04-11). |
| 3.49 | 2026-04-11 | **AUD-2026-04-11-003 + AUD-2026-04-11-004 — execution_prompt.md v3.1→v3.2.** §8 Phase 3 source prompt header updated v3.1→v3.2. §14 Execution Engine Source updated v3.1→v3.2. Changes in execution_prompt.md: STEP 5.0A pr_status Pre-Seal Sync added (STRUCTURAL) — before writing Sprint_Complete, sync pr_status for all EPICs in epics_merged via `gh pr view`; do not proceed to STEP 5.1 until all have pr_status = "merged" or "not_created" (resolves OVERDUE 3-cycle deferred patch AUD-003). Verification readiness statement upgraded to STRUCTURAL table block with explicit Yes/No fields — do not write any No entry before resolving gap (resolves STALE 2-cycle deferred patch AUD-004). Authority: Head of Specs Team (AUD-2026-04-11). |
| 3.48 | 2026-04-11 | **AUD-2026-04-11-001 — §13 artefact register: three missing artefacts added.** Sprint Backlog Index (`claude/cycles/<id>/sprint_backlog_index.json`, Class —, PMO Lead, Phase 2) inserted after Sprint Backlog row. Velocity Metrics (`claude/cycles/velocity_metrics.md`, Class 4, PMO Lead, Phase 1/1B) inserted after Decision Log row — read by roadmap_prompt.md STEP 0 since v4.7. Audit Report (`claude/cycles/<id>/audit_report_AUD-<date>.md`, Class 3, Head of Specs Team, Post-Ship) inserted after Closure State row — filed per audit SLA block. Authority: Head of Specs Team (AUD-2026-04-11). |
| 3.47 | 2026-04-11 | **AUD-2026-04-11-007 + AUD-2026-04-11-008 — §14 metadata fields corrected.** §14 Version field updated 3.41→3.47 (was stale since v3.41; five version bumps 3.44/3.45/3.46 applied without updating §14 self-metadata). §14 Last Updated updated 2026-03-31→2026-04-11. §14 Team Charter version updated v1.5→v1.6 (charter updated to v1.6 on 2026-03-16 per AUD-2026-03-13-006; §14 not updated at that time). Authority: Head of Specs Team (AUD-2026-04-11). |
| 3.46 | 2026-04-06 | **ST-12 (EPIC-04, v2.5) — deferred governance prompt patches applied.** §8 source prompt execution_prompt.md v3.0→v3.1; §9 source prompt delivery_verification_prompt.md v1.7→v1.8. §14 Execution Engine Source → v3.1; Verification Engine Source → v1.8. Patches: (CF-2a) execution_prompt STEP 8 — governance file edit check added: if any §6-governed file was modified during sprint execution, append to prompt_change_log.md in same session. (CF-2b) delivery_verification_prompt STEP 8 — pre-seal gate added (LL-v2.4-DV-01): verify §9 DoQ and PO Date fields are non-blank before proceeding to STEP 8.5; surface for completion if blank. Authority: Head of Specs Team (ST-12, 2026-04-06). |
| 3.33 | 2026-03-20 | **CLAUDE.md §8 — Cross-EPIC Merge Conflict Resolution added.** New section documents the sequential merge procedure for concurrent EPIC branches with shared-file conflicts: merge simpler EPIC first → merge updated main into remaining EPIC branch → resolve per-file rules (execution_state.json never revert done→blocked; openapi.yaml union + highest version; api_changelog.md combine descending; data_model.md all migrations ascending + highest version footer) → commit, push, confirm MERGEABLE, merge. §14 version 3.33. |
| 3.31 | 2026-03-19 | **Correct preview URL pattern.** §8.2 and §8.5: `trading-assistant-api-pr-{N}` → `trading-assistant-api-staging-pr-{N}` (confirmed from live Render deployment). §14 version 3.31. Merge conflict resolution: renumbered v3.28→3.29→3.30→3.31 to accommodate main's v3.28 (ST-11 staging seed). |
| 3.30 | 2026-03-18 | **ST-15 sign-off: preview environment mode clarified to manual + `render-preview` label.** §8.2 bullet updated — automatic provisioning corrected to manual mode; `render-preview` label required on PRs for EPICs with frontend changes. Infrastructure & Operations Owner sign-off recorded (enabled 2026-03-18). |
| 3.33 | 2026-03-21 | **execution_prompt.md v2.5→v2.6 — LL-v2.1-P4-3 guard.** §8 source prompt v2.5→v2.6. §14 Execution Engine Source → v2.6. Change: STEP 6 guard note added — do not emit `Sprint_Complete` until `execution_state.json.sealed = true`. Prevents Phase 4 preflight failure where sprint close completes but STEP 7 (seal) was not executed. |
| 3.32 | 2026-03-20 | **execution_prompt.md v2.4→v2.5 — agent-mediated sign-off.** §8 source prompt v2.4→v2.5. §14 Execution Engine Source → v2.5. Change: §5.3 Agent-Mediated Sign-Off added — when a seal condition names a role with an agent file, engine invokes a subagent acting in that role before surfacing to user; §3.1.A step 11 added; §9.1 `sign_off_record` field added to ST item schema. Always-human gates (Product Owner, merge gate) unchanged. |
| 3.29 | 2026-03-18 | **ST-15 (EPIC-05): Render PR preview environments documented.** §8.2 preview environment bullet added — Render provisions `https://trading-assistant-api-staging-pr-{N}.onrender.com` per PR; Director of Quality may use preview URL as staging evidence method for frontend-interactive AC. §8.5 merge gate QA sign-off line updated to reference preview URL option alongside staging URL. |
| 3.28 | 2026-03-19 | **ST-11 staging seed workflow updated to psql-based approach.** §8.2 staging test data seeding bullet added: `seed-preview.yml` workflow renamed to `Seed Staging Database`, trigger changed from `render-preview` label to `workflow_dispatch`, seeding mechanism changed from Python API script to `psql` against `STAGING_DATABASE_URL` secret, idempotency guard added. Documents that PR preview environments are not used for data-dependent QA — canonical staging is always the test target. |
| 3.45 | 2026-04-05 | **OA-01 (v2.5) closure — sprint_planning_prompt.md v2.4→v2.5.** §7 source prompt v2.4→v2.5. §14 Sprint Planning Engine → v2.5. Patch: STEP -1.11 added — Prompt Change Log Hygiene Advisory: scans full change log table (not top-first) for version gaps; surfaces as advisory with prepend-order reminder; advisory only, does not halt. Root cause addressed: execution engines were appending entries to bottom of change log table, causing release_planning_prompt STEP -1.7 top-first scan to report false gaps. Authority: Head of Specs Team (OA-01 closure 2026-04-05). |
| 3.44 | 2026-04-03 | **execution_prompt.md v2.9→v3.0 — v2.4 post-ship action-now patches.** §8 source prompt v2.9→v3.0. §14 Execution Engine Source → v3.0. Patches: (LL-v2.4-EX-01 third recurrence) §3.1.D delegated_decision unblock detection — hard gate added: update delegation log entry to Unblocked atomically with item status=done; applies equally to delegated_decision as to delegated_backend/frontend. (LL-v2.4-P4-01 second recurrence) STEP 5.1 — QA Evidence File Existence Check added: verify qa_evidence_EPIC-xx.md exists for every merged EPIC before sign-off date check; missing file is hard gate at sprint close. (LL-v2.4-P4-02) §3.1.A pre-met path — explicit note added: pre-met items still require qa_evidence entry with DoQ sign-off confirming verification; pre-met ≠ unverified. Authority: Head of Specs Team (post-ship closure 2026-03-31__release-v2.4). |
| 3.41 | 2026-03-31 | **Roadmap rebalance 2026-03-31__scheduled — OVERDUE patch applied.** §6 source prompt roadmap_prompt.md v4.5→v4.6. §14 Roadmap Engine Source → v4.6. Patch: (LL-v2.3-RP-01 — OVERDUE B7 escalation) roadmap_prompt.md STEP 8.5 — Extended-tier session advisory added: for Extended-tier runs (40+ ideas), confirm STEP 8.5.B write plan is complete in cycle_record.md before closing session; write plan is the resumption artefact for STEP 9. |
| 3.40 | 2026-03-31 | **v2.3 post-ship deferred lessons learnt applied.** §8 source prompt execution_prompt.md v2.8→v2.9; §9 source prompt delivery_verification_prompt.md v1.6→v1.7. §14 Execution Engine Source → v2.9; Verification Engine Source → v1.7. Patches: (LL-v2.3-CL-01) execution_prompt §5.1 delegated_frontend — Base44 model removed; autonomous default; classification rule + delegation note updated. (LL-v2.2-EX-01 2nd recurrence) execution_prompt STEP 3.1.A — delegation log update upgraded from advisory to hard gate: atomic with item done transition. (LL-v2.2-EX-02 2nd recurrence) execution_prompt STEP 4 — all_merged advisory upgraded to hard gate. (LL-v2.2-EX-04 2nd recurrence) execution_prompt §9.1 + §12 — "no prior spec applicable" named as exemption token; completion condition explicit. (LL-v2.3-CL-02) execution_prompt STEP 7 — delegation_log.md pre-seal line count check added. (LL-v2.3-CL-03) delivery_verification_prompt STEP 3 — canonical spec Known Deviations sync note added. |
| 3.39 | 2026-03-30 | **execution_prompt.md v2.7→v2.8 — LL-v2.3-EX-01/02 applied.** §8 source prompt v2.7→v2.8. §14 Execution Engine Source → v2.8. Two immediate-action patches from v2.3 post-ship lessons: (LL-v2.3-EX-01) Date field requirement note added to QA sign-off block template — Date must be non-blank when sign-off is completed, not at sprint close; checkboxes pre-checked in template. (LL-v2.3-EX-02) Mid-sprint reclassification guidance added to §5.1 — when a story's classification changes after a delegation record exists, cancel the delegation log entry immediately rather than waiting until STEP 5.0. |
| 3.38 | 2026-03-24 | **AUD-2026-03-21 tier 2 fixes applied.** §5 source prompt idea_intake_prompt.md v2.0→v2.2; §10 source prompt post_ship_closure.md v2.1→v2.2; §14 table: idea_intake_prompt v2.2, post_ship_closure v2.2. §10 audit cadence advisory added (non-blocking; fires when `completed_cycle_count % 3 == 0`). Patches: (AUD-001) idea_intake_prompt STEP 3 `per_agent_submission_count` computation instruction added; (AUD-002) post_ship_closure STEP 0 Audit Cadence Check block added + §10 audit cadence documented. |
| 3.37 | 2026-03-24 | **v2.2 post-ship lessons learnt applied.** §7 source prompt sprint_planning_prompt.md v2.3→v2.4; §8 source prompt execution_prompt.md v2.6→v2.7; §9 source prompt delivery_verification_prompt.md v1.5→v1.6. §14 table: sprint_planning_prompt v2.4, execution_prompt v2.7, delivery_verification_prompt v1.6. Patches: (sprint_planning) LL-v2.2-SP-01 blocked-decision advisory; (execution) LL-v2.2-EX-01–05 delegation log in-flight, all_merged advisory, backend branch invariant, spec_references schema note, QA evidence pending note; (delivery_verification) LL-CL-v22-01 backlog reference synchronisation at deviation filing. |
| 3.36 | 2026-03-23 | **ST-13/14/15 (EPIC-05): governance process enhancements.** §6 source prompt roadmap_prompt.md v4.3→v4.5; §6B source prompt release_planning_prompt.md v2.21→v2.24; §7 source prompt sprint_planning_prompt.md v2.2→v2.3; §10 source prompt post_ship_closure.md v2.0→v2.1; §14 table: roadmap_prompt v4.5, release_planning_prompt v2.24, sprint_planning_prompt v2.3, post_ship_closure v2.1, lessons_learnt_prompt v1.8, shared_standards v2.7. Changes: (ST-13) Provisional-Target field on backlog promotion (shared_standards §16.6, roadmap_prompt STEP 9, release_planning_prompt STEP 1.2); (ST-14) scored_initiatives.md effort band handoff contract (shared_standards §16.7, release_planning_prompt STEP 0 load + STEP 4.5 lookup); (ST-15) Carry-Forward block in lessons_learnt_closure.md (shared_standards §16.8, roadmap/release/sprint planning STEP 0 read advisory, post_ship_closure STEP 8.5 write requirement, lessons_learnt_prompt §3.5 + §5 schema). |
| 3.35 | 2026-03-22 | **AUD-2026-03-21 tier 1 fixes applied.** §13 Artefact Register: `closure_state.json` row added (Post-Ship, Class —, Owner PMO Lead). §6B source prompt release_planning_prompt.md v2.20→v2.21. §6M source prompt backlog_management_prompt.md v1.3→v1.4. §14 governance table: release_planning_prompt v2.21, backlog_management_prompt v1.4, shared_standards v2.4. |
| 3.34 | 2026-03-21 | **Lessons learnt patches applied (cycle 2026-03-21__item-3.5).** §6 source prompt roadmap_prompt.md v4.2→v4.3; §6M source prompt roadmap_management_prompt.md v1.2→v1.3; §14 Roadmap Engine Source → v4.3; Roadmap Management Engine → v1.3. Two patches: (1) roadmap_management_prompt.md v1.3: STEP 5.4 added — retirement step now also updates initiative_register.md (resolves LL-01-patch-4.3 recurrence escalation); (2) roadmap_prompt.md v4.3: STEP 4.4 debate queue + STEP 5 preflight check (resolves Friction Item 1 cycle 2026-03-21__item-3.5). |
| 3.27 | 2026-03-18 | **idea_intake_prompt.md v2.0→v2.1 — stale warning horizon check added.** §5 source prompt v2.0→v2.1; §14 Idea Intake Engine v2.0→v2.1. STEP -0.5 added: before opening intake window, Facilitator checks `ideas_register.md` for Parked-cycle-2 rows; if ≥15, surfaces stale warning advisory. Register-model-correct replacement for LL-01-patch (cycle 2026-03-18__item-4.3). |
| 3.26 | 2026-03-18 | **roadmap_prompt.md v4.1→v4.2 — register model consistency fixes.** §6 source prompt v4.0→v4.2; §14 Roadmap Engine Source → v4.2. Changes: STEP -1.6 count source updated from `submissions/` file scan to `ideas_register.md` row count; STEP 0.C Lightweight criterion 2 updated to register rows; STEP 8.5.B item 4 "idea file" language updated to "register row". |
| 3.25 | 2026-03-17 | **ST-19 (EPIC-06): Ideas register model.** §5 source prompt v1.3→v2.0; §5 trigger condition updated (count from `ideas_register.md`); §5.3 lifecycle updated (per-file → register rows); §5.5 artefacts table updated (Idea Submissions → Ideas Register; window summary path updated; archive entry added); §5.6 exit criteria updated. Artefact register: Idea Submissions → Ideas Register (`ideas_register.md`). §14: idea_intake_prompt v2.0; roadmap_prompt v4.1; shared_standards v2.3. |
| 3.25 | 2026-03-17 | **v2.0 post-ship lessons learnt applied.** §7 source prompt sprint_planning_prompt.md v2.1→v2.2. §8 source prompt execution_prompt.md v2.3→v2.4. §14 Sprint Planning Engine → v2.2; Execution Engine Source → v2.4. |
| 3.24 | 2026-03-17 | **ST-18 (EPIC-06): roadmap_prompt.md v3.0→v4.0 — `cycle_record.md` single-file pattern extended to all tiers.** §6 source prompt v3.0→v4.0. §6.3 Engine Steps table: STEP 2/3/4/5/8 output column updated from stage file names to `cycle_record.md` section references. §14 Roadmap Engine Source → v4.0. |
| 3.23 | 2026-03-16 | **Roadmap process governance improvements (v3.0).** §6 + §14 roadmap_prompt.md v2.8→v3.0. Five changes: STEP 0.C auto-tier determination (Lightweight/Standard/Extended, system-derived from objective criteria); STEP 2.3 horizon review always-on every run; STEP 4.1/4.2 first-park rationale required; STEP 5.1 Challenger clearance model; STEP 8.6 guardrail logic corrected. |
| 3.20 | 2026-03-16 | **v1.10 post-ship lessons learnt applied (LL-v1.10-P3-1, P3-3, P4-1, P4-2, P4-3).** §8.2 staging test data prerequisite bullet added (LL-P4-3). §8 + §14 source prompt versions updated: execution_prompt v2.1→v2.2, delivery_verification_prompt v1.4→v1.5. See prompt_change_log.md for full detail per prompt. |
| 3.22 | 2026-03-16 | **AUD-2026-03-13-005, 006, 017 applied.** §6 roadmap_prompt.md v2.7→v2.8 (AUD-005 Net-Zero halt block → prose ref; AUD-006 §9 invariants → reference). §6B release_planning_prompt.md v2.19→v2.20 (AUD-005 Amendment halt block → prose ref). §8 execution_prompt.md v2.2→v2.3 (AUD-017 §11 schema → §16.3 ref; SLA tracking → §16.4 ref; §13 invariants cross-ref). §14 shared_standards.md v2.1→v2.2 (AUD-017 §16.3+§16.4 added). New file: `claude/system/invariants.md` v1.0 (AUD-006 canonical invariants). §14 governance table: 5 version entries updated; Governance Invariants row added. |
| 3.21 | 2026-03-16 | **Post-ship closure v1.10 deferred patches applied.** §6 roadmap_prompt.md v2.6→v2.7 (STEP 8.5.B idea file status verification). §6M backlog_management_prompt.md v1.1→v1.3 (STEP 4 endpoint reference check); roadmap_management_prompt.md v1.1→v1.2 (already in §14). §7 sprint_planning_prompt.md v2.0→v2.1 (STEP -1.10 pre-sprint required decisions check; STEP 3.1 delegation class assignment note). §10 post_ship_closure.md v1.9→v2.0 (STEP 8.5 sequencing clarification). §14 governance table: 4 version entries updated. |
| 3.20 | 2026-03-16 | **ST-03 (v1.10 EPIC-01): staging environment documented as canonical pre-merge QA environment.** §8.2 QA sign-off environment bullet added — Director of Quality must test against `https://trading-assistant-staging.onrender.com`, not production (LL-01 resolution). §8.5 merge gate QA sign-off lines updated to reference staging URL explicitly. Closes governance gap LL-01. |
| 3.18 | 2026-03-15 | **AUD-2026-03-13-003 corrected — STEP -1.6 count-based trigger.** §5 renamed from "Phase 0 — Idea Intake" to "Idea Intake (Integrated — Phase 1 STEP -1.6)". Phase 0 removed from lifecycle table and quick-reference block. §4 narrative updated. STEP -1.6 now triggers on open idea count < 20 (not open window status). §14 roadmap_prompt → v2.6. |
| 3.17 | 2026-03-15 | **AUD-2026-03-13-003 applied.** §6 source prompt → roadmap_prompt.md (v2.5). §14 Roadmap Engine Source → v2.5. Change: STEP -1.6 Idea Window Check (conditional) added to roadmap_prompt.md — detects open ideas_window.json and invokes idea_intake_prompt.md inline; CLAUDE.md command table updated with *(auto)* row for STEP -1.6. |
| 3.16 | 2026-03-14 | **AUD-2026-03-13 third batch applied.** §6 source prompt → roadmap_prompt.md (v2.4). §10 source prompt → post_ship_closure.md (v1.9). §14 governance table: roadmap_prompt v2.4, shared_standards v2.1, post_ship_closure v1.9. AUD-002: run roadmap --dry-run added; §13 table updated. AUD-004: post_ship_closure STEP 11 (manage roadmap) + STEP 12 (groom backlog) added as mandatory; old STEP 11 (Commit) renumbered STEP 13; closure_state.json schema updated; §6M Known gap replaced with enforcement note. |
| 3.15 | 2026-03-14 | **AUD-2026-03-13 second batch applied.** §5 (idea intake) → v1.3. §6 source prompt → roadmap_prompt.md (v2.3). §6B source prompt → release_planning_prompt.md (v2.19). §7 source prompt → sprint_planning_prompt.md (v2.0). §14 governance table: shared_standards v2.0, lessons_learnt_prompt v1.7, idea_intake_prompt v1.3. Changes: lessons_learnt_prompt §1.1 invocation context hard gate; Phase 3/4 headers normalised to stable anchors; shared_standards §16 JSON schemas section added; sprint_planning inline schema replaced with §16.1 reference; roadmap + release planning lessons_learnt.md ARTEFACT_STATUS terminal block requirement; idea_intake per_agent_submission_count field. |
| 3.14 | 2026-03-14 | **AUD-2026-03-13 audit improvements applied.** §6 source prompt → `roadmap_prompt.md` (v2.2). §7 source prompt → `sprint_planning_prompt.md` (v1.9). §6B.8 source prompt → `amendment_cycle_prompt.md` (v1.6). §8 source prompt → `execution_prompt.md` (v2.1). §14 governance table versions updated accordingly. Changes: roadmap STEP -1.5 B7 auto-escalation + patch confirmation + state age advisory; STEP 5 Challenger failure halt; STEP 9 structural decision log enforcement + header formatting rule. Execution STEP 9 gate evidence requirement. Sprint Planning Amendment_In_Progress hard gate. Amendment cycle amendment_lessons.md deprecation notice. `run audit` added to CLAUDE.md command table. |
| 3.13 | 2026-03-11 | **Batch 7 governance decisions resolved.** §7 source prompt → `sprint_planning_prompt.md` (v1.8). §14 governance table: `sprint_planning_prompt.md` v1.8, `team_charter.md` v1.5. IMPs applied: IMP-30 (design gate bypass authority named — Head of UX & Design + Product Owner co-confirmation; charter updated; sprint planning STEP -1.3 reference added), IMP-17/31 (Class 8 deferred — no further action; Reserved annotation confirmed), IMP-60 (`v2_0_gates` block superseded — removed from `.claude_current_state.json`; decision recorded). |
| 3.12 | 2026-03-11 | **Batch 8 review.md governance and lifecycle completeness sweep.** §6 source prompt → `roadmap_prompt.md` (v2.1). §6B source prompt → `release_planning_prompt.md` (v2.18). §9 source prompt → `delivery_verification_prompt.md` (v1.4). §10 source prompt → `post_ship_closure.md` (v1.8). §14 governance table versions updated accordingly (shared_standards v1.9). IMPs applied: IMP-13 (roadmap STEP 9.0 net-zero gate), IMP-33 (roadmap STEP 5.0 mode-independence note), IMP-11 (release planning STEP -1.8 Amendment_In_Progress hard gate), IMP-16 (release planning STEP -1.9 stale lock preflight), IMP-22 (shared_standards §14 preflight field scope), IMP-43 (shared_standards §15 spec debt lifecycle), IMP-14 (delivery verification STEP 5.3 test_scenario_gaps table), IMP-15 (delivery verification STEP 4.3 stale parked detection; post_ship_closure STEP 3.4 stale parked disposition check). |
| 3.11 | 2026-03-10 | **Phase 3 lessons learnt stale references fixed.** §8 Quick Reference checklist (line ~157): `lessons_learnt_execution.md filed` → `lessons_learnt_cycle.md Phase 3 section appended`. §8.4 Key Artefacts table: `lessons_learnt_execution.md` → `lessons_learnt_cycle.md` (Phase 3 section append). §8.6 Phase 3 Exit Criteria: `lessons_learnt_execution.md filed` → `lessons_learnt_cycle.md Phase 3 section appended (idempotency guard applied)`. |
| 3.10 | 2026-03-10 | **Batch 5 alignment fixes.** §10.5 Lessons Learnt Application: table updated — `lessons_learnt_execution.md` and `lessons_learnt_verification.md` rows replaced with single `lessons_learnt_cycle.md` row (Phase 3 + Phase 4 + Amendment); section description updated to "two lessons learnt files". §13 Artefact Register: `Lessons Learnt (Execution)` and `Lessons Learnt (Verification)` rows replaced with single `Lessons Learnt (Cycle — Phase 3, 4, Amendment)` row pointing to `lessons_learnt_cycle.md`. |
| 3.9 | 2026-03-10 | **Batch 5 review.md lessons learnt consolidation.** §6B.8 source prompt → `amendment_cycle_prompt.md` (v1.5). §8 source prompt → `execution_prompt.md` (v2.0). §9 source prompt → `delivery_verification_prompt.md` (v1.3). §10 source prompt → `post_ship_closure.md` (v1.7). §14 governance table versions updated accordingly. §14 Lessons Learnt Prompt → v1.5. §10.2 inputs: `lessons_learnt_execution.md` and `lessons_learnt_verification.md` replaced with `lessons_learnt_cycle.md` (consolidated). §10.3 row 9: lessons learnt input updated to name both files. IMPs applied: IMP-28 (lessons_learnt_prompt restructured as append-only phase-tagging; Sprint Execution and Delivery Verification now append to `lessons_learnt_cycle.md`), IMP-35 gap 2 (idempotency guard now active in execution_prompt STEP 5.4), IMP-37 (amendment_cycle_prompt STEP 8 appends to `lessons_learnt_cycle.md`), IMP-53 (execution_prompt §7 write scope + STEP 5.4 updated), IMP-54 (delivery_verification_prompt STEP 8.5 added; post_ship_closure §4 and STEP 8 updated). |
| 3.8 | 2026-03-10 | **Batch 4 review.md token efficiency.** §6B source prompt → `release_planning_prompt.md` (v2.17). §7 source prompt → `sprint_planning_prompt.md` (v1.7). §8 source prompt → `execution_prompt.md` (v1.9). §10 source prompt → `post_ship_closure.md` (v1.6). §14 governance table versions updated accordingly. IMPs applied: IMP-26 (release_planning STEP 3 risk register `escalation_ref` field + ESC entry scope note), IMP-23 (sprint_planning AC reference in backlog template), IMP-25 (sprint_backlog_index.json produced at Phase 2; consumed at Phase 3 STEP -1/0), IMP-27 (post_ship_closure STEP 0 and STEP 8 field-level read targets). |
| 3.7 | 2026-03-10 | **Batch 3 review.md process gaps.** §6B source prompt → `release_planning_prompt.md` (v2.16). §6B.8 source prompt → `amendment_cycle_prompt.md` (v1.4). §8 source prompt → `execution_prompt.md` (v1.8). §14 governance table versions updated: release_planning_prompt v2.16, amendment_cycle_prompt v1.4, execution_prompt v1.8, shared_standards v1.8. |
| 3.6 | 2026-03-10 | **BATCH 2-PATCH: Playbook header drift and standing rule.** IMP-62 (1): §14 version control — standing rule added requiring phase section source prompt headers and §14 governance table to be updated in the same edit. IMP-62 (2): §9 source prompt → `delivery_verification_prompt.md` (v1.2). IMP-62 (3): §10 source prompt → `post_ship_closure.md` (v1.5); filename corrected (removed `_prompt` suffix). |
| 3.5 | 2026-03-10 | **Batch 0+1+2 review.md process gaps.** IMP-36: §6B source prompt → v2.15; §7 source prompt → v1.5; §8 source prompt → v1.7; §6B.8 amendment engine → v1.3; §14 governance table versions updated (release_planning_prompt v2.15, sprint_planning_prompt v1.5, amendment_cycle_prompt v1.3, execution_prompt v1.7, post_ship_closure v1.5, shared_standards v1.7). IMP-13: Hard Rules table — Rule 1 (net-zero) expanded with mode-independence note and enforcement agent; "Decision log" row clarified as governance convention with explicit violation note. IMP-17: §3 Document Classes — Class 8 row annotated "Reserved — not currently produced". IMP-33: §6.3 STEP 5 constraint — displacement rule explicitly stated as mode-independent; enforcement agents named. |
| 3.4 | 2026-03-10 | **Multi-sprint lifecycle exception.** §4.1 Lifecycle State Machine transition table: added `Closed` → `Executing` row (multi-sprint exception — valid only when `sprint_planning.sprint2_deferred` non-empty AND `sprint_sealed = true` AND `post_ship_complete = true`, same cycle_id continued across sprints). §14 Governance table: `shared_standards.md` → v1.6, `lifecycle_schema.json` → last_updated 2026-03-10. Triggered by closure_record §6 Actions #1 and #2, 2026-03-06__release-v1.9. |
| 3.3 | 2026-03-08 | **IMP-04–10 governance hardening (review.md backlog).** Hard Rules table: 4 new rules added (design gate bypass audit, release cycle preconditions, prompt version log, amendment lock). §14 Governance table: engine versions updated — release_planning_prompt v2.13, sprint_planning_prompt v1.4, amendment_cycle_prompt v1.2, shared_standards v1.4, roadmap_management_prompt v1.2, backlog_management_prompt v1.2, post_ship_closure v1.4. Quick Reference phase gate checklist unchanged (changes are in prompts, not checklist items). |
| 3.2 | 2026-03-07 | **Phase 1B artefacts consolidation.** §6B source prompt updated to v2.11. §6B.3 step table: Steps 1, 2, 3, 3.5, 4.5, 5.5, 5.7 now write sections into `release_plan.md` instead of separate stage files. §13 Artefact Register: Stage 1 Readiness, Stage 2 Scope Extraction, Stage 3 Execution Plan rows replaced with single `release_plan.md` (consolidated intermediate) row; Stage 4 Backlog Slice retained separately. §14 Governance table: all engine versions updated to current (release_planning_prompt v2.11, sprint_planning v1.3, amendment_cycle v1.1, execution v1.6, delivery_verification v1.2, post_ship_closure v1.3, shared_standards v1.2). |
| 3.1 | 2026-03-07 | **Lifecycle state machine hardening.** Added §4.1 Lifecycle State Machine — allowed transition table with from/to/engine/entry condition. Lifecycle Guard enforcement paragraph added referencing `shared_standards.md §10` and `lifecycle_schema.json`. |
| 3.0 | 2026-03-07 | **Aligned with `post_ship_closure_prompt.md` v1.2.** §10 source prompt updated to v1.2. §14 Post-Ship Closure Engine → v1.2. Key changes now documented in guide: `amended_backlog_slice_path` handling in closure (STEP 0 + STEP 3); `lessons_learnt_closure.md` created by explicit STEP 8.5 (invokes `lessons_learnt_prompt.md §3.5`); dry-run enforcement consistent with other engines in chain. |
| 2.9 | 2026-03-07 | **Aligned with `delivery_verification_prompt.md` v1.1.** §9 source prompt updated to v1.1. §14 Verification Engine Source → v1.1. `Not_Verified` confirmed as the canonical `.claude_current_state.json` status string for failed verification (not `Verification_Failed`). |
| 2.8 | 2026-03-07 | **Aligned with `execution_prompt.md` v1.5 and `design_gate_prompt.md` v1.1.** §8 source prompt updated to v1.5. §6.5 source prompt updated to v1.1. §14: Execution Engine → v1.5, Design Gate Engine → v1.1. **`Executing` status added to lifecycle.** §4 Phase 3 row updated: trigger condition and intermediate `Executing` status documented. §12 cycle trigger table: `Executing` row added (Phase 3 resume via re-invocation after each EPIC merge). **Note:** `execution_escalations.md` was already present in §13 Artefact Register (confirmed). |
| 2.7 | 2026-03-07 | **Aligned with `sprint_planning_prompt.md` v1.2.** §7 source prompt updated to v1.2. §14 Sprint Planning Engine version updated to v1.2. |
| 2.6 | 2026-03-07 | **Aligned with `release_planning_prompt.md` v2.9.** §6B source prompt updated to v2.9. §6B.3 engine steps table: STEP 2 output now includes scope document creation; STEP 3 output now includes decisions record creation; STEP 7 renamed to include intermediate state sync; STEP 7.1 added as explicit hard-requirement row; STEP 9 renamed terminal and clarified as the only step that may set `status = Published`; STEP 10 note updated to include scope + decisions record in commit. §6B.6 Publish Gate: added `deferred_execution_blockers is empty` and STEP 7.1 completion as required conditions. §6B.7 Exit Criteria: added scope document, decisions record, `deferred_execution_blockers`, and STEP 7.1/9 sync confirmation. Phase 1B checklist in Quick Reference updated to match. **§13 Artefact Register:** added Scope Document (`docs/product/scope/scope--{cycle_id}-{slug}.md`) and Decisions Record (`docs/product/decisions/decisions--{cycle_id}.md`) rows. **§6.5.2 Design Gate:** `design_gate_status` ownership clarified — Design Gate Engine writes it; Release Planning Engine initialises to `not_started`. **§6B.8 Amendment Cycle:** `amended_backlog_slice_path` field note expanded to name the writing engine and clarify supersession of `backlog_slice_path`. **§14 Governance table:** version → 2.6, Release Engine Source → v2.9. |
| 2.5 | 2026-03-06 | **Phase 1M trigger windows widened.** Both `manage roadmap` and `groom backlog` are now valid at two equally-weighted trigger points: after Post-Ship Closure and immediately before `run roadmap`. Updated: Quick Reference engine commands comment; §4 Lifecycle Overview trigger column; §6M intro replaced single trigger with explicit trigger table; §12 Cycle Trigger table added pre-`run roadmap` row (bolded); known gap note added for Phase 1 skipped path in §6M, §12, and both prompt files. **Phase 1M gaps closed.** Added Phase 1M block to Phase Gate Checklist. Expanded §6M.3 exit criteria to match other phases (full checklist format). Added stale blocker classification to §6M.2 table. Added lock conflict note to §6M.2. Added promotion shortlist advisory note to §6M.2. **Hard Rules table** updated: backlog lock row now includes Phase 1M. **§6B subsection numbering fixed**: 6.1–6.8 collision with Phase 1 resolved — renamed to 6B.1–6B.8 throughout. **Amendment Cycle discoverability** improved: added callout block at top of §6B; added Amendment Cycle as named sub-entry in Table of Contents. **Backlog Lock artefact** phase column updated to include 1M. **§14 Governance table** updated: Roadmap Management Engine → v1.1, Backlog Management Engine → v1.1. |
| 2.4 | 2026-03-06 | Updated to reflect `roadmap_prompt.md` v2.0 and `lessons_learnt_prompt.md` v1.4. Added scheduled run invocation, prior cycle outstanding actions check, engine steps updates, Phase 1 exit criteria updates, idea lifecycle status updates, roles update, lifecycle overview updates, cycle trigger table updates, artefact register updates, governance table updates. |
| 2.3 | 2026-03-04 | Added Class 8 (Proof of Gate) to §3. Fixed broken row in §12. Updated Phase 1 source prompt to v1.9. |
| 2.2 | 2026-03-04 | Added Phase 1M (Document Management) and Phase 1.5 (Design Gate). |
| 2.1 | 2026-03-03 | Added Phase 0 Idea Intake engine. |
| 1.9 | 2026-03-03 | Added Amendment Cycle Engine. |
| 1.8 | 2026-03-03 | Added Sprint Planning engine (Phase 2). |
| 1.7 | 2026-03-03 | Updated roadmap_prompt.md to v1.6. |
| 1.6 | 2026-03-03 | Updated shared_standards.md and lessons_learnt_prompt.md versions. Added lessons learnt artefact types. |
| 1.5 | 2026-03-03 | Added post_ship_closure_prompt.md as Phase 10 engine source. |
| 1.4 | 2026-03-03 | Added Post-Ship Closure (§10). |
| 1.3 | 2026-03-03 | Added execution_prompt.md and delivery_verification_prompt.md. |
| 1.2 | 2026-03-02 | Prior version. |
