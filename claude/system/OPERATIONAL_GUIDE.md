# Sprint Planning Operational Playbook

**Owner:** Head of Specs Team
**Status:** Active
**Version:** 3.25
**Last Updated:** 2026-03-17
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
| Decision log (`claude/roadmap/decision_log.md`) is append-only — governance convention, not a hard gate; deletions or edits to prior entries are process violations | Phase 1 |
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

**Source prompt:** `claude/system/idea_intake_prompt.md` (v2.0)
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

All agent roles defined in `claude/agents/` — including Facilitator and Challenger. Minimum 2 net-new ideas per agent per window. A resubmitted parked idea counts as net-new only if materially updated.

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
| Archived submissions | `claude/ideas/submissions/archive/*.md` | PMO Lead | Read-only — prior per-file submissions migrated 2026-03-17 |

### 5.6 Exit Criteria

- `ideas_window.json` status = `Closed`
- All agent submission rows appended to `ideas_register.md` (or gaps recorded)
- `window_summary_<window_id>.md` exists
- Commit complete

---

## 6. Phase 1 — Roadmap Rebalance (Optional)

**Source prompt:** `claude/system/roadmap_prompt.md` (v4.0)
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

**Source prompts:** `claude/system/roadmap_management_prompt.md` (v1.2), `claude/system/backlog_management_prompt.md` (v1.3)  
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

### 6M.3 Phase 1M Exit Criteria

- `roadmap_archive.md` updated (if any items retired)
- `backlog_archive.md` updated (if any items archived)
- Stale items flagged in `current_roadmap.md` (if any identified)
- Orphans and stale blockers flagged in `backlog.md` (if any identified)
- Manage roadmap run log written (`claude/roadmap/manage_roadmap_log_<YYYYMMDD>.md`)
- Backlog health report written (`claude/backlog/backlog_health_<YYYYMMDD>.md`)
- No ambiguous items left unresolved
- Backlog lock released
- Commits complete for both engines

---

## 6.5 Phase 1.5 — Design Gate (Required*)

**Source prompt:** `claude/system/design_gate_prompt.md` (v1.1)  
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
6. Gate record written; global state updated (`design_gate_status = Passed` written to `state.json` by the Design Gate Engine; reserved as a read-only field by the Release Planning Engine, which initialises it to `not_started` at STEP 0)

**Gate passes only when:** all Design Required items have approved artefacts AND updated frontend specs.

### 6.5.3 Sprint Planning Pre-Condition

`plan sprint` may not be issued until `design_gate_status = Passed` in `state.json`.

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

**Source prompt:** `claude/system/release_planning_prompt.md` (v2.20)
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

**Source prompt:** `claude/system/amendment_cycle_prompt.md` (v1.6)

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

**Source prompt:** `claude/system/sprint_planning_prompt.md` (v2.2)
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

---

## 8. Phase 3 — Sprint Execution & Close

**Source prompt:** `claude/system/execution_prompt.md` (v2.4)

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
- `qa_evidence_EPIC-xx.md` exists and sign-off block complete (Director of Quality — review conducted against staging: `https://trading-assistant-staging.onrender.com`)
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

**Source prompt:** `claude/system/delivery_verification_prompt.md` (v1.5)

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

**Source prompt:** `claude/system/post_ship_closure.md` (v2.0)
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

> **Phase 1M enforcement:** `manage roadmap` and `groom backlog` are invoked as mandatory STEP 11 and STEP 12 of every Post-Ship Closure run. Both run at every cycle close regardless of whether Phase 1 was executed. Standalone invocation remains supported for teams that want an additional pre-roadmap clean-up pass.

---

## 13. Artefact Register

All artefacts must be lifecycle-compliant per `claude/charter/document_lifecycle_guide.md`.

| Artefact | Location | Class | Owner | Phase |
|----------|----------|-------|-------|-------|
| Team Charter | `claude/charter/team_charter.md` | 1 | Head of Specs Team | Governance |
| Document Lifecycle Guide | `claude/charter/document_lifecycle_guide.md` | 1 | Head of Specs Team | Governance |
| Strategy Rules | `claude/strategy/strategy_rules.md` | 1 | Strategy Rules Owner | Governance |
| Roadmap Rebalance Prompt | `claude/system/roadmap_prompt.md` | 7 | Head of Specs Team | Governance |
| Release Planning Prompt | `claude/system/release_planning_prompt.md` | 6 | Head of Specs Team | Governance |
| Idea Intake Engine | `claude/system/idea_intake_prompt.md` | 6 | Head of Specs Team | Governance |
| Idea Template | `claude/system/idea_template.md` | 6 | Head of Specs Team | Governance |
| Amendment Cycle Prompt | `claude/system/amendment_cycle_prompt.md` | 6 | Head of Specs Team | Governance |
| Delivery Verification Prompt | `claude/system/delivery_verification_prompt.md` | 6 | Head of Specs Team | Governance |
| Shared Standards | `claude/system/shared_standards.md` | 6 | Head of Specs Team | Governance |
| Governance Invariants | `claude/system/invariants.md` | 6 | Head of Specs Team | Governance |
| Lessons Learnt Prompt | `claude/system/lessons_learnt_prompt.md` | 6 | Head of Specs Team | Governance |
| Prompt Change Log | `claude/system/prompt_change_log.md` | 6 | Head of Specs Team | Governance |
| Current Roadmap | `claude/roadmap/current_roadmap.md` | 4 | Product Owner | 1 |
| Backlog | `claude/backlog/backlog.md` | 4 | Product Owner | 1, 1B, 4, Post-Ship |
| Initiative Register | `claude/roadmap/initiative_register.md` | 4 | Product Owner | 1 |
| Workforce Capacity | `claude/roadmap/workforce_capacity.md` | 4 | FinOps & Resource Architect | 1 |
| Decision Log | `claude/roadmap/decision_log.md` | 4 | PMO Lead | 1 |
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
| Amendment Manifest | `claude/cycles/<id>/amendments/<AMD-id>/amendment_manifest.md` | 3 | PMO Lead | Amendment |
| Amendment State | `claude/cycles/<id>/amendments/<AMD-id>/amendment_state.json` | — | PMO Lead | Amendment |
| Amendment Ratification | `claude/cycles/<id>/amendments/<AMD-id>/amendment_ratification.md` | 4 | PMO Lead | Amendment |
| Amended Backlog Slice | `claude/cycles/<id>/amendments/<AMD-id>/amended_backlog_slice.md` | 4 | PMO Lead | Amendment |
| Amendment Lessons | `claude/cycles/<id>/amendments/<AMD-id>/amendment_lessons.md` | 3 | PMO Lead | Amendment |

---

## 14. Playbook Governance

| Field | Value |
|-------|-------|
| Owner | Head of Specs Team |
| Status | Active |
| Version | 3.25 |
| Last Updated | 2026-03-17 |
| Review Cadence | After every 3 completed cycles, or on any governance gap escalation |
| Idea Intake Engine | `claude/system/idea_intake_prompt.md` v2.0 |
| Idea Template | `claude/system/idea_template.md` |
| Roadmap Management Engine | `claude/system/roadmap_management_prompt.md` v1.2 |
| Backlog Management Engine | `claude/system/backlog_management_prompt.md` v1.3 |
| Design Gate Engine | `claude/system/design_gate_prompt.md` v1.1 |
| Roadmap Engine Source | `claude/system/roadmap_prompt.md` v4.1 |
| Release Engine Source | `claude/system/release_planning_prompt.md` v2.20 |
| Sprint Planning Engine | `claude/system/sprint_planning_prompt.md` v2.2 |
| Amendment Cycle Engine | `claude/system/amendment_cycle_prompt.md` v1.6 |
| Execution Engine Source | `claude/system/execution_prompt.md` v2.4 |
| Verification Engine Source | `claude/system/delivery_verification_prompt.md` v1.5 |
| Post-Ship Closure Engine | `claude/system/post_ship_closure.md` v2.0 |
| Post-Ship Closure Process | `docs/team_skills/pmo/processess/post-ship_closure.md` v2.0 |
| Shared Standards | `claude/system/shared_standards.md` v2.3 |
| Governance Invariants | `claude/system/invariants.md` v1.0 |
| Lessons Learnt Prompt | `claude/system/lessons_learnt_prompt.md` v1.7 |
| Prompt Change Log | `claude/system/prompt_change_log.md` |
| Lifecycle Guide | `claude/charter/document_lifecycle_guide.md` v2.5 |
| Team Charter | `claude/charter/team_charter.md` v1.5 |

This playbook is subordinate to and must remain consistent with all governing documents above. In any conflict, governance documents prevail. Update this playbook to reflect the change — do not operate with a known divergence.

**Version control:** All changes require approval by the Head of Specs Team and must be version-bumped per lifecycle rules. Patch = typo/formatting. Minor = structural change. Major = scope change or authority boundary change.

**Standing rule:** whenever a prompt version is updated in the §14 governance table, the corresponding phase section source prompt header (§5–§10, §6B, §6B.8, §6M) must be updated in the same edit. A mismatch between a phase section header and §14 is a non-compliant state.

---

### Change Log

| Version | Date | Change Summary |
|---------|------|----------------|
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
