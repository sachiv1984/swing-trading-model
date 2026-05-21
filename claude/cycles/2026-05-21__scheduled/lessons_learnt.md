**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Published
**Cycle:** 2026-05-21__scheduled

---

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: Scheduled rebalance — no completion event
Run: 2026-05-21__scheduled
Reviewed by: PMO Lead
Date filed: 2026-05-21
Prior cycle checked: 2026-05-19__scheduled (1 deferred patch — applied this run)

---

## What worked well

- Gate-condition re-check (STEP 4.0) correctly identified IDEA-pmo-lead-20260508-01 as gate-cleared (Arc 3 complete). PO re-evaluation applied correctly; Rejected (not strong).
- 3-cycle hard cap enforcement proceeded cleanly: all 33 ideas systematically classified with clear rationale. 29 gate-conditional backlog items well-formed. 4 rejections with clear reasoning.
- Prior cycle deferred patch (STEP 12.1 artefact precondition) applied as action-now this run — target date met.

---

## Friction Log

### Friction Item #1 — Type D: prompt_change_log.md missing v6.3→v6.4 entry

**Description:** roadmap_prompt.md v6.3→v6.4 (prompt compression, 2026-05-21) was recorded in OPERATIONAL_GUIDE.md v3.95 changelog but is absent from `claude/system/prompt_change_log.md`. The prompt_change_log.md last entry is v6.2→v6.3 (2026-05-20).

**Root cause:** The prompt compression commit (gov/2026-05-21__prompt-compression branch) updated OPERATIONAL_GUIDE.md changelog but skipped the prompt_change_log.md append step for roadmap_prompt.md.

**Blast radius:** Low — documentation gap only; does not affect execution. The change is fully traceable via OPERATIONAL_GUIDE.md v3.95.

**Classification:** Type D — Artefact Discipline

**Process patch:** Deferred — Head of Specs Team to review and append the missing entry to prompt_change_log.md in the next governance commit that touches that file.

---

### Friction Item #2 — Type B: One-time 3-cycle-cap migration cost (29 backlog items)

**Description:** The first rebalance under v6.3+ rules required classifying 33 ideas that had accumulated beyond the 3-cycle cap under old rules (pre-v6.3). This resulted in 29 new backlog (gate-conditional) items added in a single run — a significant one-time backlog expansion.

**Root cause:** The 3-cycle hard cap was introduced in v6.3 (2026-05-20) and applied to all existing parked ideas retrospectively at the first run under the new rule. Prior parking cycles under v6.2 were compliant with those rules.

**Blast radius:** Medium (one-time): backlog grows from 11 → 40 active items; future groom backlog runs will manage gate-conditional items. No execution impact.

**Classification:** Type B — Process Compliance (expected migration cost of new governance rule)

**Process patch:** None required. Backlog grooming engine (groom backlog) will maintain gate-conditional items. Consider: at next `groom backlog`, review whether gate-conditional items with similar gates can be grouped or summarised in a note.

---

## Recurrence Escalations

None.

---

## Process improvements actioned this run

| # | Patch | File | Version | Authority |
|---|-------|------|---------|-----------|
| 1 | STEP 12.1 artefact existence precondition | `claude/system/roadmap_prompt.md` | v6.4→v6.5 | Head of Specs Team |

---

## New files created this run

- `claude/cycles/2026-05-21__scheduled/run_manifest.md`
- `claude/cycles/2026-05-21__scheduled/cycle_record.md`
- `claude/cycles/2026-05-21__scheduled/cycle_summary.md`
- `claude/cycles/2026-05-21__scheduled/lessons_learnt.md`

---

## Outstanding deferred patches

| # | Patch | File | Section | Owner | Target |
|---|-------|------|---------|-------|--------|
| 1 | Append missing v6.3→v6.4 entry to prompt_change_log.md | `claude/system/prompt_change_log.md` | — (append) | Head of Specs Team | Next governance commit touching prompt_change_log.md |

---

## Escalations

None.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | prompt_change_log.md missing v6.3→v6.4 entry | Append in next governance commit that touches the file | Governance |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-05-21__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-05-21T00:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
