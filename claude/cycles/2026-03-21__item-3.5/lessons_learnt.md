**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-21

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: 3.5 Alerts & Notifications (completion event 2026-03-21; v2.1 shipped)
Run: 2026-03-21__item-3.5
Reviewed by: PMO Lead
Date filed: 2026-03-21
Prior cycle checked: 2026-03-18__item-4.3

---

## What Worked Well

- **Idea intake at scale:** 44 new submissions from 22 agents processed cleanly in a single intake window (IW-20260321-01). The register model (ideas_register.md row-per-idea) handled bulk status transitions efficiently — 44 new + 11 stale = 55 ideas classified without individual file operations.
- **STEP 8.6 guardrail satisfied organically:** With 9 items advancing unanimously, the Challenger issued two Type A counter-arguments (BLG-FEAT-11 SPS=4 scope, BLG-SEC-01 single-user threat model). Both were well-grounded. The PO rebuttals were substantive. The guardrail pattern is working as intended.
- **Zero-sum trivially satisfied:** All completions were at the backlog level (not roadmap); 0 roadmap Adds ≤ 0 roadmap Kills. With no active initiatives at run start, the rebalance focussed entirely on enriching the backlog and resolving accumulated idea debt — appropriate given the v2.1 completion event.
- **LL-01-patch-4.3 partial mitigation:** The initiative_register.md Active table was stale at run start (same root cause as prior cycle). This cycle corrected it in STEP 9 — the correction is now within write scope for the roadmap engine, so it can be applied inline when encountered. This reduces the blast radius even though the underlying prompt gap persists.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type D — Cognitive Fatigue: Advancing STEP 4 idea omitted from STEP 5 debate

**Recurrence:** No (not in 2026-03-18__item-4.3)

**What happened:**
IDEA-base44-frontend-20260304-02 (User-Facing Error Message Mapping Layer) was classified as ✅ Advancing in STEP 4 (gate cleared: BLG-SPEC-G2 shipped v2.1). However, the idea was not included in the STEP 5 debate section of `cycle_record.md`. The omission was detected when applying the STEP 8.5.B write plan (LL-02-patch register row verification requirement), which mandates terminal statuses for all rows marked Advancing in §4.2. The item was treated as Promoted-Added with implied Challenger clearance (SPS=2, gate cleared, no §13 proximity) per the LL-02-patch recovery protocol.

**Where in the routine:** STEP 5 — Structured Debate (omission during authoring of cycle_record.md)

**Root cause:** Context window pressure — with 9 debates to author across stale and new advancing ideas, one item was lost in the transition from STEP 4 classification to STEP 5 debate. The register was partially updated before the session context was exhausted (only IDEA-base44-frontend-20260304-01 was completed before compaction).

**Blast radius analysis:**
- What would have propagated: IDEA-base44-frontend-20260304-02 would have ended the cycle with Status=Advancing (non-terminal) in ideas_register.md, violating the STEP 8.5.B write plan requirement. The backlog item BLG-FE-03 would not have been created. The error would have been carried silently into the next idea window — the row would re-surface as a stale idea without a clear origin trace.
- When it would have surfaced: At next roadmap run STEP 4 (stale idea review), where it would appear as a row in Advancing status — an invalid state between cycles.
- Recovery cost if uncaught: Low-medium — one backlog item lost; register in inconsistent state until caught at next cycle.

**Process patch:**

→ Deferred patch:
- File: `claude/system/roadmap_prompt.md`
- Section: STEP 4 advancing idea classification output format
- Change: After marking any idea as ✅ Advancing in STEP 4, the engine must append its IDEA ID to an explicit "STEP 5 debate queue" list within `cycle_record.md`. STEP 5 must open by reading this queue and confirming one debate entry exists per queue item before proceeding. This makes omissions detectable rather than silent.
- Owner: Head of Specs Team
- Target: Before next roadmap rebalance run (next release planning cycle or scheduled roadmap run)

---

### Friction Item 2 (Recurrence)

**Classification:** Type D — Cognitive Fatigue: initiative_register.md Active table stale at run start (second occurrence)

**Recurrence:** Yes — appeared in 2026-03-18__item-4.3 as Friction Item 2. Prior outstanding action LL-01-patch-4.3 was NOT resolved.

**What happened:**
At the start of this run, `initiative_register.md` showed 3.5, 4.2, and CHART-IX as Active initiatives. All three had shipped in v2.1 (2026-03-21). The same class of stale state occurred in cycle 2026-03-18__item-4.3 (4.1b and 4.3 were stale-Active after shipping in v2.0). The deferred patch LL-01-patch-4.3 — requiring `roadmap_management_prompt.md` to update the register when retiring items — was issued in 2026-03-18__item-4.3 but has not been applied. This is the second consecutive cycle in which this friction item has fired.

**Where in the routine:** STEP 0 / STEP 9 — initiative register load and correction

**Root cause:** Deferred patch LL-01-patch-4.3 carried forward without a `prompt_change_log.md` entry for 2 cycles (2026-03-18__item-4.3 → this cycle). Per §6.4 of lessons_learnt_prompt.md: this is an automatic recurrence escalation. The `manage roadmap` engine's retirement step does not include an explicit `initiative_register.md` write.

**Blast radius analysis:**
- What would have propagated: initiative_register.md would persistently show shipped items as Active, leading to distorted CPS at every subsequent roadmap run. Any agent reading the register to understand active scope would have an incorrect picture.
- When it would have surfaced: Every roadmap run until the patch is applied.
- Recovery cost if uncaught: Medium — CPS computation distorted each cycle; register loses integrity as canonical inventory; correcting it manually each cycle is overhead.

**Process patch:**

→ This is a recurrence escalation — see Recurrence Escalations below. Not recording as a standard deferred patch: this is the second occurrence and requires Head of Specs Team resolution.

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| initiative_register.md Active table stale at run start — `roadmap_management_prompt.md` retirement step does not update register | 2026-03-18__item-4.3 (Friction Item 2) | LL-01-patch-4.3: update roadmap_management_prompt.md retirement step to move completed items from Active to Completed in initiative_register.md. Deferred with target: "Before next `manage roadmap` run". Not applied. No prompt_change_log entry exists. | Head of Specs Team |

---

## Process Improvements Actioned This Run

Applied post-cycle by explicit user instruction (2026-03-21):

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/roadmap_management_prompt.md` | §5 Write Scope + STEP 5.4 (new) + STEP 6 commit | STEP 5.4 added: retirement step now also updates initiative_register.md (move Active→Completed with ship date + release); initiative_register.md added to write scope and commit. Resolves LL-01-patch-4.3 recurrence escalation. | v1.2→v1.3 | Yes — appended to prompt_change_log.md |
| `claude/system/roadmap_prompt.md` | STEP 4.4 Write Summary + STEP 5 preflight | STEP 5 Debate Queue table added to STEP 4.4 output template; STEP 5 preflight reads queue and verifies debate coverage before proceeding. Resolves Friction Item 1. | v4.2→v4.3 | Yes — appended to prompt_change_log.md |
| `claude/system/OPERATIONAL_GUIDE.md` | §6, §6M, §14, changelog | Source prompt versions updated: roadmap_prompt v4.2→v4.3, roadmap_management_prompt v1.2→v1.3. §14 table and changelog entry updated. | v3.33→v3.34 | Yes — appended to prompt_change_log.md |

---

## New Files Created This Run

| File | Rationale |
|------|-----------|
| `claude/cycles/2026-03-21__item-3.5/run_manifest.md` | Standard cycle artefact — roadmap run manifest |
| `claude/cycles/2026-03-21__item-3.5/cycle_record.md` | Standard cycle artefact — STEP 2–8 working content |
| `claude/cycles/2026-03-21__item-3.5/cycle_summary.md` | Standard cycle artefact — STEP 10 summary |
| `claude/cycles/2026-03-21__item-3.5/lessons_learnt.md` | This file |
| `claude/ideas/ideas_window.json` | Updated for IW-20260321-01 (rewrite) |
| `claude/ideas/window_summary_IW-20260321-01.md` | New window summary for IW-20260321-01 |

---

## Outstanding Deferred Patches

None. Both patches actioned post-cycle by explicit user instruction (2026-03-21). See Process Improvements Actioned table above.

---

## Escalations

| Issue | Type | Escalated to | Reason | Resolution |
|-------|------|-------------|--------|------------|
| LL-01-patch-4.3 carried forward 2 cycles without prompt_change_log entry — `roadmap_management_prompt.md` retirement step does not update initiative_register.md Active→Completed | Recurrence / Missing patch_change_log entry (2+ cycles) | Head of Specs Team | §6.4: deferred patch carried 2+ cycles without corresponding prompt_change_log entry is an automatic recurrence escalation. | **Resolved 2026-03-21** — patch applied (roadmap_management_prompt.md v1.3, STEP 5.4 added); prompt_change_log.md updated. ESC-LL01-4.3-RECUR closed. |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-03-21__item-3.5",
  "phase": "Roadmap",
  "filed_utc": "2026-03-21T00:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 2,
  "deferred_count": 0,
  "escalation_count": 0,
  "recurrence_escalations": 1,
  "overdue_patches": 0,
  "status": "Complete — all patches applied 2026-03-21 by explicit user instruction"
}
```
