
Release Planning Engine — Governance Prompt

Owner: Head of Specs Team
Status: Active
Version: 2.4
Last Updated: 2026-03-02
Lifecycle Guide: claude/charter/document_lifecycle_guide.md
Team Charter: claude/charter/team_charter.md

Cycle-Based · Reusable · Escalation-Aware · State-Driven · Mutation-Safe · Concurrency-Safe · Terminal-Sealed · Assumption-Frozen · Tamper-Evident

⸻

1. Purpose

Translate an already-approved roadmap release (e.g., v1.7, v1.8) into an execution-ready plan:
	•	Sequencing
	•	Dependencies
	•	Acceptance gates
	•	Verification approach
	•	Release backlog slice
	•	Optional GitHub issue plan

This routine:
	•	❌ May NOT rebalance the roadmap
	•	❌ May NOT add/replace/defer/kill initiatives
	•	❌ May NOT alter strategy boundaries

⸻

2. Delegated Authority Model

The user delegates operational decision-making to defined role agents.

During this routine:
	•	Each authority role may decide within its domain
	•	Strategy / Quality / Lifecycle blocks cannot be overridden
	•	Missing authority or required evidence → HALT

Facilitator and Challenger have no decision authority.

⸻

3. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues:

plan release --version "<vX.Y>" \
             [--date "YYYY-MM-DD"] \
             [--timebox "<text>"] \
             [--capacity "<text>"] \
             [--mode "<strict|standard>"] \
             [--issues "<none|import|gh>"] \
             [--auto-escalate "<true|false>"]

Requirements
	•	Must start with plan release
	•	--version is required
	•	Version must exist in roadmap
	•	strict → halt on any unclear prerequisite
	•	standard → allow explicit assumptions (except hard gates)
	•	auto-escalate default = true

If invocation is not exact → conversational mode only.

⸻

4. Canonical Governance Sources (Binding)
	•	claude/charter/team_charter.md
	•	claude/charter/document_lifecycle_guide.md
	•	claude/strategy/strategy_rules.md

This routine may NOT override these.

⸻

5. Write Scope Restriction (Hard Gate)

Allowed Writes
	•	claude/cycles/<cycle_id>/*
	•	claude/backlog/backlog.md (release slice only)
	•	claude/roadmap/current_roadmap.md (execution notes only)
	•	docs/product/decisions/* (AR / SRB only)
	•	claude/scoring/* (if explicitly requested)

Forbidden
	•	Source code
	•	Strategy rules
	•	Initiative register
	•	Roadmap decision log

Violation → HALT

⸻

6. Authoritative Source Model (v2.4)

The cycle folder:

claude/cycles/<cycle_id>/

is the authoritative historical planning record.

Shared files (backlog.md, roadmap.md) are operational mirrors only.

Post-publish modifications to shared files do NOT alter the sealed record.

Amendments require a new cycle.

⸻

7. Identifier Standards (Hard Requirement)
	•	S2-xx
	•	EPIC-xx
	•	RISK-xx
	•	ESC-YYYYMMDD-nn

Exact mapping required.

Missing IDs → Process Integrity Blocker

⸻

8. Cycle Folder & State

cycle_id Format

{date}__release-{vX.Y}

State File

claude/cycles/<cycle_id>/state.json

State-driven execution is mandatory.

⸻

9. Canonicalization Rules (Hashing — Hard Requirement)

For markdown artefacts:
	1.	Normalize line endings to LF
	2.	Strip trailing whitespace
	3.	Collapse >2 blank lines → exactly 2
	4.	Trim leading/trailing blank lines
	5.	Do NOT reorder content

Hash method: SHA-256

Filesystem timestamps are forbidden.

⸻

10. Macro States
	•	Initialized
	•	Planning
	•	Committed
	•	Validated
	•	Published
	•	Blocked

⸻

11. Resume Precheck — Mutation Detection (Hard Gate)

Tracked items:
	•	stage2_scope_extraction.md
	•	stage3_execution_plan.md
	•	stage4_backlog_slice.md
	•	escalations.md
	•	assumptions.timebox
	•	assumptions.capacity

If change detected:
	•	mutation_seq += 1
	•	Record in mutations[]
	•	Apply invalidation map
	•	Re-run dependent steps

Safety Rule

Always re-run STEP 4.5 if:
	•	Timebox changed
	•	Capacity changed
	•	Workforce escalation resolved

⸻

12. Terminal State Guard — Published Is Immutable

If:

state.status == "Published"

Then:
	•	No stage steps may execute
	•	No artefact may be modified
	•	No escalation entry may be appended
	•	No assumptions may change
	•	No lock acquisition allowed

Only permitted action: drift detection

⸻

13. Drift Detection (v2.4)

Recompute and compare:
	•	sealed_hashes
	•	sealed_assumptions
	•	state_snapshot_hash

If mismatch:

state.drift_detected = true

Append to drift_notes:
	•	timestamp
	•	changed component
	•	old value
	•	new value

HALT with instruction:

Published cycle has drift. Create amendment cycle.

No repair allowed in published cycle.

⸻

14. Escalation Freeze Rule (NEW v2.4)

If status == Published:
	•	escalations.md becomes read-only
	•	Any modification → HALT

⸻

15. Escalation Handling
	•	Append-only
	•	Typed: AR / SRB
	•	Deferred requires:
	•	Trigger
	•	Execution flag
	•	Strategy / Quality / Lifecycle cannot be AR
	•	Mutation rule enforced

⸻

16. Execution Steps

Unchanged from v2.3:
	•	Stage 1 — Readiness
	•	Stage 2 — Scope Extraction
	•	Stage 3 — Execution Plan
	•	Stage 3.5 — Integrity
	•	Stage 3.9 — Backlog Lock
	•	Stage 4 — Backlog Slice (transaction + marker)
	•	Stage 4.5 — Capacity
	•	Stage 4.95 — Roadmap Lock
	•	Stage 5 — Roadmap Annotation (transaction + marker)
	•	Stage 5.5 — Cross-Stage Integrity
	•	Stage 5.7 — Decision Record Integrity
	•	Stage 7 — Summary
	•	Stage 8 — Lessons

All locking and recovery logic unchanged.

⸻

17. Publish Gate (Hard Constraint)

Must satisfy:
	•	open_escalations empty
	•	No Deferred where “Blocks execution = Yes”
	•	stage4_5 = pass OR warn
	•	warn allowed only in standard mode
	•	stage5_5 = pass
	•	stage5_7 = pass OR not_applicable

If satisfied:
	1.	status = Validated
	2.	publish_eligible = true

Sealing must occur before Published.

⸻

18. Publish Sealing (v2.4 Hardened)

Before setting status = Published:

⸻

18.1 Recompute Canonical Hashes

For:
	•	stage2_scope_extraction.md
	•	stage3_execution_plan.md
	•	stage4_backlog_slice.md
	•	escalations.md

Write into:

state.sealed.sealed_hashes


⸻

18.2 Seal Assumptions (NEW)

Capture:

sealed_assumptions = {
  timebox,
  capacity
}

Write into:

state.sealed.sealed_assumptions

These become immutable.

⸻

18.3 Seal Canonical State Snapshot (Tamper-Evident)

Create canonical JSON excluding:
	•	last_transition_utc
	•	Drift flags
	•	locks.*
	•	Dynamic artefact lock states

Include:
	•	cycle_id
	•	release
	•	date
	•	mode
	•	assumptions
	•	artifact_hashes
	•	mutation_seq
	•	escalation lists
	•	attributes
	•	sealed_hashes
	•	sealed_assumptions

Canonicalize key order.

Hash using SHA-256.

Write into:

state.sealed.state_snapshot_hash


⸻

18.4 Finalize Seal

Set:

sealed_utc = now (UTC)
drift_detected = false
drift_notes = []


⸻

18.5 Final Transition

After successful sealing:

status = "Published"
last_transition_utc = now
publish_eligible = true

It is forbidden to mark Published before sealing completes.

If sealing fails → halt and remain Validated.

⸻

19. State Integrity Rule (NEW v2.4)

If:
	•	status == Published
	•	Sealed fields missing OR
	•	state_snapshot_hash mismatch

Treat as drift.

Do NOT repair.

Require amendment cycle.

⸻

20. Completion Condition

Run is complete only if:
	•	Cycle folder exists
	•	state.json valid
	•	publish_eligible = true
	•	status = Published
	•	Summary + Lessons exist
	•	No open escalations

⸻
