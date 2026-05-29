**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.3
**Phase:** Release

---

# Lessons Learnt — Release Planning v4.3

Feature / Trigger: v4.3 Governance Consolidation, QA Debt Clearance & Ops Hardening
Run: 2026-05-29__release-v4.3
Reviewed by: PMO Lead
Date filed: 2026-05-29
Prior cycle checked: 2026-05-27__release-v4.2

---

## What worked well

- **Scope extraction was clean and comprehensive.** 18 stories identified without ambiguity across all four EPICs; all backlog sources were clearly traceable, and no items required reclassification after initial extraction.
- **Carry-forward integration from v4.2 closure was effective.** All 3 carry-forward items from v4.2's lessons_learnt_closure.md (execution_prompt.md STEP 3.2.A, STEP 5.3/8, and qa_evidence_template.md advisories) were cleanly assigned to ST-01/02/03 in EPIC-01 with specific acceptance criteria.
- **Gate analysis was decisive.** SI-02 pre-planning cluster (7 items) and BLG-GOV-67 were correctly excluded due to live gate conditions; deferral rationale was documented at first analysis without iteration.
- **Phasing recommendation was concrete.** The capacity WARN was handled by a well-reasoned Sprint 1 / Sprint 2 phasing proposal (EPIC-01+04 / EPIC-02+03) that sprint planning can adopt directly.

---

## Friction Log

---

### Friction Item 1

**Classification:**
- Type D — Cognitive Fatigue: A detail was missed due to prompt length, context overload, or accumulated complexity

**Recurrence:** Yes — appeared in 2026-05-27__release-v4.2

**What happened:**
The Extended-tier "no-change" rebalance (2026-05-27__scheduled) left the roadmap with `**Next planned release:** **[TBD]**`. When `plan release v4.3` was invoked, STEP -1.2 hard gate fired because no v4.3 section existed in `current_roadmap.md`. The Product Owner resolved this inline (Option A) by adding the v4.3 section under PO authority. This is the same resolution path used for v4.2. The v4.2 lessons_learnt disposition was "deferred advisory only; add to backlog if pattern recurs."

**Where in the routine:**
STEP -1.2 — Pre-flight check: confirm release section exists in roadmap.

**Root cause:**
Process gap — the Extended-tier rebalance engine records "no roadmap-level changes" and exits without creating a next-release placeholder. This is a correct outcome for its own governance, but creates a predictable planning dependency gap every time an Extended-tier no-change rebalance precedes a release planning invocation.

**Blast radius analysis:**
- What would have propagated: Without Option A resolution, release planning cannot proceed — hard gate blocks STEP -1.2 indefinitely.
- When it would have surfaced: Immediately — at every release planning invocation following an Extended-tier no-change rebalance.
- Recovery cost if uncaught: Low (single inline PO edit) — but the gate fire and resolution decision cost ~10 minutes of session time each cycle it occurs.

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 8.1 (or nearest Now horizon summary step)
  - Change required: Add an advisory note: "If Now horizon is empty after this rebalance and no planned release section exists in current_roadmap.md for the next anticipated release, the Product Owner should add one now — omitting it will trigger STEP -1.2 of the Release Planning Engine at every subsequent invocation until resolved."
  - Owner: Head of Specs Team
  - Target: v4.4 release planning (next run of roadmap_prompt.md, or when the backlog item is scheduled)

---

### Friction Item 2

**Classification:**
- Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** No

**What happened:**
STEP 7 requires an intermediate global state sync to `.claude_current_state.json` (setting `active_cycle`, `status`, and `backlog_slice_path`) before writing `cycle_summary.md`. This sync was not performed — the context was compacted mid-session and the session resumed at STEP 8. The `.claude_current_state.json` still points to `active_cycle: "2026-05-27__release-v4.2"` and `status: "Closed"`. The intermediate sync is effectively merged into the STEP 9 terminal update (applied this run), so there was no data loss.

**Where in the routine:**
STEP 7 — Cycle Summary — Intermediate global state sync (required before writing cycle_summary.md).

**Root cause:**
Context window pressure — the session was compacted mid-run and resumed from the summary. The STEP 7 intermediate sync requirement was not carried forward into the resumption scope.

**Blast radius analysis:**
- What would have propagated: If the session had been abandoned after STEP 7 without reaching STEP 9, `.claude_current_state.json` would still point to the prior cycle. Any subsequent engine invocation would read stale state and potentially misidentify the active cycle.
- When it would have surfaced: At next session start — CLAUDE.md §0 reads `.claude_current_state.json` and reports `active_cycle` and `status`.
- Recovery cost if uncaught: Low — a one-field file update. But the recovery must be deliberately triggered; silent stale state is a harder failure mode to detect.

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/release_planning_prompt.md`
  - Section: STEP 7 — Intermediate global state sync
  - Change required: Add a RESUME PRECHECK note: "If session was resumed via context compaction and STEP 7 has completed without the intermediate sync, perform the sync immediately before proceeding to STEP 8."
  - Owner: Head of Specs Team
  - Target: v4.4 release planning

---

## Recurrence Escalations

The Roadmap Section Gap (Friction Item 1) is a managed recurrence. The v4.2 lessons_learnt disposition was:
> "deferred — advisory only; add to backlog if pattern recurs"

The pattern has now recurred. Per that instruction, a backlog item must be added to track the deferred patch to `roadmap_prompt.md`. This is a **conditional action resolved** — not a new escalation to Head of Specs Team. The backlog item should be added by the PMO Lead at next `groom backlog` or during Sprint 1 execution.

| Friction item | First appeared | Prior outstanding action | Status |
|---------------|---------------|--------------------------|--------|
| Roadmap TBD gap (STEP -1.2 gate fires after Extended-tier no-change rebalance) | 2026-05-27__release-v4.2 | Deferred advisory — add to backlog if recurs | Managed recurrence — backlog item to be filed (BLG-GOV-type) |

---

## Process improvements actioned this run

None applied this run.

---

## New files created this run

None.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 8.1 (Now horizon summary) | Add advisory: if Now horizon empty and no planned release section exists, PO should add one now to prevent STEP -1.2 gate fire at next release planning invocation | Head of Specs Team | v4.4 release planning |
| `claude/system/release_planning_prompt.md` | STEP 7 — Intermediate global state sync | Add RESUME PRECHECK note: if session resumed via context compaction and STEP 7 completed without sync, perform sync immediately before STEP 8 | Head of Specs Team | v4.4 release planning |

---

## Escalations

None.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Roadmap TBD gap has now recurred twice (v4.2 and v4.3). A backlog item must be filed to patch `roadmap_prompt.md` STEP 8.1. If the pattern fires a third time in v4.4 without the patch applied, treat as a systemic failure and escalate to Head of Specs Team as a hard governance gap. | At v4.4 release planning: check `claude/backlog/backlog.md` for a BLG-GOV item targeting this patch. If absent, file it before proceeding past STEP -1.2. | Release Planning |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-05-29__release-v4.3",
  "phase": "Release",
  "filed_utc": "2026-05-29T07:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 0,
  "deferred_count": 2,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
