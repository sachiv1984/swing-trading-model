Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Release: v2.3
Cycle: 2026-03-24__release-v2.3
Last Updated: 2026-03-24

---

# Lessons Learnt — Release Planning

Feature / Trigger: v2.3 Quality Automation & User Insight — release planning
Run: 2026-03-24__release-v2.3
Reviewed by: PMO Lead
Date filed: 2026-03-24

---

## What Worked Well

- **Carry-forward visibility:** The v2.2 lessons_learnt_closure.md Carry-Forward section (3 items) was consumed at STEP 0 and explicitly recorded in the run manifest, giving the sprint planning engine advance notice of the items requiring attention (particularly carry-forward item 3 — ID uniqueness scan).
- **Provisional-Target advisory was useful:** 8 items had `Provisional-Target: v2.3`, which gave a clean horizon signal for scope selection. Items without the field required more manual effort to assess, confirming the value of the provisional-target convention.
- **Dependency chain was cleanly specified:** The OPS-08 → QA-06 → QA-05 chain was identified early, enabling the phasing recommendation to schedule OPS-08 in Sprint 1 to avoid sprint 2 blocking. This avoids the mid-sprint blocking pattern seen in v2.2.
- **Deferred item rationale was explicit:** Each of the 6 deferred items has a named displacement signal traceable to the roadmap rebalance priority queue — no arbitrary deferrals.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type B — Advisory Signal: Design-dependency risk not detected until scope decision

**What happened:**
BLG-UX-01 (Sidebar Navigation Overflow) is P2 and within scope, but requires a Product Owner design decision before engineering can proceed. This dependency is documented in the backlog item but was only explicitly surfaced during scope selection at STEP 2, not during the readiness validation at STEP 1.

**Root cause:**
STEP 1 (Readiness Validation) does not include a scan for items where the backlog entry explicitly notes "Product Owner to decide" or similar design-gate language. These items can enter scope without the planning engine proactively surfacing the design dependency.

**Blast radius analysis:**
- Low: the design dependency is documented in both the backlog item and the risk register (RISK-04), and the Pre-sprint Planning Required Decisions checklist will surface it to sprint planning.
- Recovery cost if uncaught at planning: Medium — sprint planning could schedule UX-01 without the design gate, only discovering the blocker during sprint execution.

**Process patch:**

→ Advisory for next release planning:
  - STEP 1 (Readiness Validation) could include a pass over scope candidates for backlog items containing "Product Owner to decide" or "design decision required" language, and surface as a readiness advisory.
  - This is not blocking — the Pre-sprint Required Decisions checklist handles it adequately for now.
  - File: `claude/system/release_planning_prompt.md`
  - Section: STEP 1 — Release Readiness Validation
  - Action: advisory only; deferred unless it recurs
  - Owner: Head of Specs Team
  - Target: Deferred (not action-now)

---

## Recurrence Escalations

None.

---

## Process improvements actioned this run

None. All observations are advisory with no immediate prompt changes required.

---

## New files created this run

| File | Purpose |
|------|---------|
| `claude/cycles/2026-03-24__release-v2.3/run_manifest.md` | Run manifest |
| `claude/cycles/2026-03-24__release-v2.3/state.json` | Cycle state |
| `claude/cycles/2026-03-24__release-v2.3/release_plan.md` | Consolidated release plan |
| `claude/cycles/2026-03-24__release-v2.3/stage4_backlog_slice.md` | v2.3 backlog slice (17 stories) |
| `claude/cycles/2026-03-24__release-v2.3/stage4_issue_manifest.json` | Issue manifest (IMP-24) |
| `claude/cycles/2026-03-24__release-v2.3/backlog_txn.json` | Backlog transaction record |
| `claude/cycles/2026-03-24__release-v2.3/roadmap_txn.json` | Roadmap transaction record |
| `claude/cycles/2026-03-24__release-v2.3/cycle_summary.md` | Cycle summary |
| `claude/cycles/2026-03-24__release-v2.3/lessons_learnt.md` | This file |
| `docs/product/scope/scope--2026-03-24__release-v2.3-quality-automation-user-insight.md` | Scope document |
| `docs/product/decisions/decisions--2026-03-24__release-v2.3.md` | Planning decisions record |

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/release_planning_prompt.md` | STEP 1 — Readiness Validation | Advisory: scan scope candidates for design-gate language ("Product Owner to decide", "design decision required") and surface as readiness advisory | Head of Specs Team | Deferred — monitor for recurrence |

---

## Escalations

None.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | BLG-UX-01 design dependency was not detected at STEP 1 — only surfaced at scope selection. The Pre-sprint Required Decisions checklist catches it, but earlier detection would improve planning confidence | Release Planning STEP 1 readiness check could scan for design-gate language in scope candidates and surface as advisory before scope selection | Release Planning |

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-03-24__release-v2.3",
  "release": "v2.3",
  "status": "Published",
  "artefacts_present": [
    "run_manifest",
    "state",
    "release_plan",
    "stage4_backlog_slice",
    "stage4_issue_manifest",
    "backlog_txn",
    "roadmap_txn",
    "cycle_summary",
    "lessons_learnt",
    "scope_document",
    "decisions_record"
  ],
  "open_escalations": 0,
  "capacity_check": "warn",
  "stories": 17,
  "epics": 5,
  "deferred_items": 6
}
