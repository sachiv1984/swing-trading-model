**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-21

---

# Lessons Learnt — Release Planning

Feature / Trigger: v2.2 Security, Alert Maturity & Quality (release planning cycle)
Run: 2026-03-21__release-v2.2
Reviewed by: PMO Lead
Date filed: 2026-03-21
Prior cycle checked: 2026-03-18__release-v2.1

---

## What Worked Well

- **Clean preflight:** All -1.x gates passed on first check. No stale locks, no amendment in progress, no open escalations from prior cycle. The v2.1 post-ship closure left a clean handoff state.
- **Backlog richness:** The 2026-03-21__item-3.5 roadmap rebalance populated 12 well-specified backlog items targeting v2.2, making scope selection straightforward. Items had effort estimates, priorities, and dependencies already documented.
- **Natural thematic coherence:** Three threads (security, alert maturity, quality) emerged from the backlog without artificial grouping. The EPIC structure followed from the items, not the other way around.
- **Capacity WARN handled cleanly:** 3-sprint phasing recommendation written inline in release_plan.md §Capacity Check. Sprint planning can adopt the phasing recommendation directly without rediscovering capacity overrun.
- **Zero escalations:** All scope decisions were straightforward; no unresolvable conflicts between agents. Zero items opened in open_escalations.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type D — Cognitive Fatigue: BLG-BE-02 duplicate ID not surfaced during backlog grooming

**Recurrence:** No

**What happened:**
During Stage 1 readiness review, the run manifest advisory ADV-RP-v22-02 surfaced that BLG-BE-02 appears in both the closed items table (v2.0, "Spec and implement GET /portfolio/prospective-heat" — shipped) and the active backlog (v2.1, "R-Multiple Analysis: stop price unavailable from trade_history" — still open). This duplicate ID was not caught during the 2026-03-21 backlog grooming run (`groom backlog` cycle).

**Where in the routine:** STEP 1 — Release Readiness Validation (advisory scan)

**Root cause:** The `groom backlog` engine's health check does not include an ID uniqueness scan across the closed items table and the active items. The duplicate arose when a new defect was assigned an already-used ID.

**Blast radius analysis:**
- What would have propagated: Sprint planning and execution would reference "BLG-BE-02" ambiguously. The active defect would be confused with the closed item in any cross-reference.
- When it would have surfaced: At sprint planning or execution when the story is assigned.
- Recovery cost if uncaught: Low — rename the active item's ID; update any references.

**Process patch:**

→ Deferred patch:
- File: `claude/system/backlog_management_prompt.md`
- Section: Health Check step
- Change: Add an ID uniqueness scan: for each item ID in the active backlog, verify it does not appear in the Closed Items table. Flag any duplicate as a ⚠ Advisory. Include the ID scan output in the groom backlog run report.
- Owner: Head of Specs Team
- Target: Before next `groom backlog` run

---

## Recurrence Escalations

None.

---

## Process Improvements Actioned This Run

None — no action-now patches required. Friction Item 1 is deferred with low blast radius.

---

## New Files Created This Run

| File | Rationale |
|------|-----------|
| `claude/cycles/2026-03-21__release-v2.2/run_manifest.md` | Standard cycle artefact |
| `claude/cycles/2026-03-21__release-v2.2/state.json` | Standard cycle artefact |
| `claude/cycles/2026-03-21__release-v2.2/release_plan.md` | STEP 1–3, 3.5, 4.5, 5.5, 5.7 combined release plan |
| `claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md` | STEP 4 — 15-story backlog slice |
| `claude/cycles/2026-03-21__release-v2.2/stage4_issue_manifest.json` | STEP 4 — issue manifest (IMP-24) |
| `claude/cycles/2026-03-21__release-v2.2/backlog_txn.json` | Backlog transaction record |
| `claude/cycles/2026-03-21__release-v2.2/roadmap_txn.json` | Roadmap annotation transaction record |
| `claude/cycles/2026-03-21__release-v2.2/cycle_summary.md` | STEP 7 cycle summary |
| `claude/cycles/2026-03-21__release-v2.2/lessons_learnt.md` | This file |
| `docs/product/scope/scope--2026-03-21__release-v2.2-security-alert-maturity-quality.md` | STEP 2 scope document |
| `docs/product/decisions/decisions--2026-03-21__release-v2.2.md` | STEP 3 decisions record |

---

## Outstanding Deferred Patches

| Ref | File | Change | Owner | Target |
|-----|------|--------|-------|--------|
| LL-RP-v22-01 | `claude/system/backlog_management_prompt.md` | Add ID uniqueness scan to health check step — flag active items with IDs matching closed items table | Head of Specs Team | Before next `groom backlog` run |

---

## Escalations

None.

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-03-21__release-v2.2",
  "phase": "Release",
  "filed_utc": "2026-03-21T00:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 1,
  "escalation_count": 0,
  "recurrence_escalations": 0,
  "overdue_patches": 0,
  "status": "Complete — 1 deferred patch (LL-RP-v22-01: backlog_management_prompt.md ID uniqueness scan)"
}
```
