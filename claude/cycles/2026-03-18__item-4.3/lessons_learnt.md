**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-18

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: 4.3 Signal Exposure Enhancement (completion event 2026-03-17; v2.0 shipped)
Run: 2026-03-18__item-4.3
Reviewed by: PMO Lead
Date filed: 2026-03-18
Prior cycle checked: 2026-03-17__item-v1.10

---

## What Worked Well

- **Stale idea disposal:** 19 Parked-cycle-3 ideas were disposed cleanly — 8 rejected, 11 re-parked with written PO rationale. The register model (single file, row-per-idea) made bulk classification significantly faster than the prior per-file model. The LL-01-patch concern (large stale burden) materialised as predicted, but the register model reduced the friction considerably.
- **Challenger debate quality:** The Challenger issued a well-grounded Type A counter-argument for BLG-FR-01 (PDF Export), citing DL-008 as evidence. The PO rebuttal was substantive (capacity-kill distinction). STEP 8.6 guardrail passed naturally.
- **Register model validation:** The ideas_register.md model (ST-19) proved its value — 19 bulk status updates that would have been 19 individual file edits in the old model were handled in a single targeted operation.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type B — Semantic Mismatch: A prior deferred patch referenced the old submission model

**Recurrence:** No (not in 2026-03-17__item-v1.10)

**What happened:**
LL-01-patch from 2026-03-17__item-v1.10 described adding a stale warning horizon note to `idea_intake_prompt.md` referencing "submissions folder" and file counts. The submissions folder model was replaced by the register model (ST-19) in the same cycle that issued the patch. The patch arrived at this cycle with an outdated description — it still references `claude/ideas/submissions/` and "file counts" rather than `ideas_register.md` row counts.

**Where in the routine:** STEP -1.5 prior cycle patch check

**Root cause:** The ST-19 and LL-01-patch were both applied in the same cycle (2026-03-17). The LL-01-patch was written before ST-19 landed in the same session and was not updated to reflect the new register model.

**Blast radius analysis:**
- What would have propagated: If applied verbatim, the patch would add instructions referencing a model that no longer exists. A confused or future Claude would scan `submissions/` folder (now read-only archive) instead of `ideas_register.md`. Stale warning logic would be inoperative.
- When it would have surfaced: At patch application time (next run)
- Recovery cost if uncaught: Low — the wrong instruction would be silently ineffective; the correct behaviour already happens via STEP -1.6 register scan.

**Process patch:**

→ Action-now (this run):
- File: `claude/system/idea_intake_prompt.md`
- Section: Add new guidance paragraph before STEP 1 (or within STEP 0 announce block)
- Change: Add stale warning horizon note updated for register model: "Before opening the window, the Facilitator should check `claude/ideas/ideas_register.md` for rows at `Parked-cycle-2`. If ≥15 rows are at `Parked-cycle-2`, surface a stale warning in the window summary: at the next roadmap run, all these ideas will reach the stale threshold (cycle-3) and require mandatory active PO disposition. Recommend the PO pre-emptively review and close stale candidates before the next roadmap run to reduce the STEP 4 burden."
- Confirmed by: Head of Specs Team (lifecycle-compliant instruction update; Class 6 prompt; version increment required)
- Version: idea_intake_prompt.md v2.0 → v2.1

→ Also: Mark LL-01-patch as superseded in the deferred patches table. The action-now above replaces it.

---

### Friction Item 2

**Classification:** Type D — Cognitive Fatigue: Artefact inconsistency carried forward undetected

**Recurrence:** No (not in 2026-03-17__item-v1.10)

**What happened:**
The `initiative_register.md` Active Initiatives table still showed 4.1b and 4.3 as active at the start of this run, despite both having been shipped in v2.0 and retired by the `manage roadmap` step of post-ship closure (2026-03-17). The `manage roadmap` step retired items from `current_roadmap.md` but did not update the Active Initiatives table in `initiative_register.md`. This was caught and corrected in STEP 9.

**Where in the routine:** STEP 0 / STEP 9 — initiative register load

**Root cause:** The `manage roadmap` engine's write scope covers `current_roadmap.md` primarily; its instructions for updating `initiative_register.md` may not have been applied. Alternatively, the post-ship closure ran `manage roadmap` as a step but the register was not fully synced.

**Blast radius analysis:**
- What would have propagated: initiative_register.md would show completed items as Active indefinitely. STEP 2 would score them as active initiatives, inflating CPS and distorting the strategic picture.
- When it would have surfaced: Next roadmap run would show 4.1b (SPS=1) and 4.3 (SPS=4) as active, giving a distorted CPS.
- Recovery cost if uncaught: Medium — CPS computation is distorted; STEP 2 re-validation becomes misleading; initiative register loses its integrity as a canonical inventory.

**Process patch:**

→ Deferred patch:
- File: `claude/system/roadmap_management_prompt.md`
- Section: Step that retires completed items
- Change: When retiring a completed item from `current_roadmap.md`, the engine must also update the item's row in `initiative_register.md` — move it from the Active Initiatives table to the Completed table with the ship date and release.
- Owner: Head of Specs Team
- Target date: Before next `manage roadmap` run

---

## Prior Cycle Deferred Lessons Status

| Patch | Status |
|-------|--------|
| LL-01-patch (idea_intake_prompt.md stale warning) | Superseded by action-now Friction Item 1 above — register-model-correct version applied this run |

No OVERDUE items. No escalations from prior cycle.

---

## Deferred Patches (for next governance session)

| Patch | Description | Prompt file | Section | Owner | Target |
|-------|------------|-------------|---------|-------|--------|
| LL-01-patch-4.3 | When retiring completed items from current_roadmap.md, also update initiative_register.md Active→Completed | `claude/system/roadmap_management_prompt.md` | Retirement step | Head of Specs Team | Before next `manage roadmap` run |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-03-18__item-4.3",
  "phase": "Roadmap",
  "filed_utc": "2026-03-18T00:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
