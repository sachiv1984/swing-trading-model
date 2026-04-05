**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Release:** v2.5
**Cycle:** 2026-04-05__release-v2.5
**Last Updated:** 2026-04-05

---

# Lessons Learnt — Release Planning v2.5

## What Worked Well

- **CF-2 carry-forward resolved at release planning:** The delivery_verification_prompt.md seal gate patch (deferred from v2.4 closure) was successfully scheduled as ST-12 in v2.5, fulfilling the carry-forward obligation from lessons_learnt_closure.md. The carry-forward mechanism is working as intended.
- **Skill-Silo Alert applied to scope selection:** The Skill-Silo Alert from the 2026-04-05 rebalance (100% governance-heavy new additions) was directly applied to scope decisions: the 4 new governance items (BLG-FE-09, BLG-SPEC-D17, BLG-GOV-11, BLG-GOV-14) were deferred to v2.6 to avoid compounding the governance-heavy load. Skill balance at 23% governance for in-scope items — within bounds.
- **Backlog provisional targets in good shape:** 19 items with `Provisional-Target: v2.5` allowed confident scope selection. Stale target updates from the rebalance (BLG-TECH-05, BLG-GOV-08) were already applied.

## Friction Items

### Friction Item 1 — Prompt change log gaps for 4 Class 6 prompts

**What happened:** STEP -1.7 identified 4 governed prompts with version numbers not recorded in `claude/system/prompt_change_log.md`:
- `release_planning_prompt.md` v2.25 (last logged v2.21)
- `design_gate_prompt.md` v1.1 (no entry)
- `amendment_cycle_prompt.md` v1.6 (no entry)
- `roadmap_prompt.md` v4.7 (last logged v4.3)

**Impact:** Advisory only — no release blocker. But the gap means the change history for these prompts is unrecoverable from the log alone.

**Root cause:** The simultaneity rule (prompt change log entry in the same commit as the version bump) is not always followed. CLAUDE.md §6 requires it but the enforcement is advisory-only at STEP -1.7.

**Action:** Head of Specs Team should audit and backfill entries for the gap versions, or document why versions changed without entries. Outstanding action recorded in run manifest.

**Recommended preventive action:** ST-12 in this cycle patches `execution_prompt.md` to include a reminder at STEP 8 — this addresses one recurrence vector. The other prompts (design_gate, amendment_cycle, roadmap) should receive a similar reminder in their respective engines or via a CLAUDE.md §6 audit reminder at each post-ship closure.

---

## Outstanding Actions (carry-forward to Sprint Planning)

| ID | Action | Owner | When | Status |
|----|--------|-------|------|--------|
| OA-01 | CF-1: Sprint planning governance hygiene — in-sprint prompt edits must log to prompt_change_log.md | Head of Specs Team | Sprint Planning preflight | **Closed 2026-04-05** — sprint_planning_prompt.md v2.4→v2.5: STEP -1.11 added (Prompt Change Log Hygiene Advisory). Reminder enforced in engine with full-table scan and prepend-order guidance. |
| OA-02 | Prompt change log audit: backfill entries for release_planning_prompt.md v2.22–v2.25, design_gate_prompt.md v1.1, amendment_cycle_prompt.md v1.6, roadmap_prompt.md v4.4–v4.7 | Head of Specs Team | Before or during sprint execution | **Closed 2026-04-05 — No backfill required.** Full audit confirmed all entries ARE present in `prompt_change_log.md` (lines 94–169). The STEP -1.7 gap report was a false positive: those entries were appended to the bottom of the table by execution commits (4998373, 3de8fd4, c89bff0, 519c192) and missed by a top-first scan. Root cause fixed by OA-01 (STEP -1.11). |
| OA-03 | Hook configuration fix: review user-prompt-submit-hook write target before sprint execution | User / Infrastructure & Operations Owner | Before sprint execution begins | Open |

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-04-05__release-v2.5",
  "release": "v2.5",
  "status": "Published",
  "generated_utc": "2026-04-05T00:09:00Z",
  "artifacts": {
    "run_manifest": "present",
    "release_plan": "present",
    "scope_document": "present",
    "decisions_record": "present",
    "stage4_backlog_slice": "present",
    "stage4_issue_manifest": "present",
    "cycle_summary": "present",
    "lessons_learnt": "present"
  }
}
