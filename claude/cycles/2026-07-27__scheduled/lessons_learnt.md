# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: N/A — scheduled rebalance
Run: 2026-07-27__scheduled
Reviewed by: PMO Lead
Date filed: 2026-07-27
Prior cycle checked: 2026-07-24__scheduled

---

## What worked well

- **STEP -1.5 correctly identified the single inherited deferred patch as due at this exact cycle** (target "2026-07-25__scheduled or next scheduled cycle" — this cycle) and resolved it as action-now rather than letting it lapse.
- **STEP -1.7's v9.4 widened cross-routine scan (applied at the end of the prior cycle) worked exactly as designed** — it caught a real previously-missed outstanding action (a cross-EPIC `execution_state.json` structural-fix escalation, first raised at `2026-07-17__release-v7.5` closure) that the pre-widening scan structurally could not have caught. The prior cycle's own STEP -1.7 had already executed (using the pre-widening scan) before that same session applied the v9.4 patch at STEP 11, so the fix could only take effect starting this cycle — an expected one-cycle lag, not a new gap.
- **Idea intake ran cleanly at full scale** — 44 submissions across 22 agents, 0 below minimum, 0 `[FIELD REQUIRED]` flags.
- **The structural backlog-assessment heuristic (v9.1) continued to scale correctly** at 341+ active items.
- **The BLG-ID collision-avoidance grep (§8.5.B) and the net-zero displacement check both passed cleanly** with no manual correction needed.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type A — Governance Drift

**Recurrence:** No — not previously flagged as a measured friction item, though the underlying condition (the same idea-intake pattern run for 20+ consecutive cycles) has been building silently.

**What happened:**
At STEP 4.0.5 (a backlog-scope-overlap check applied retroactively, since `idea_intake_prompt.md`'s own §2.0 step 5 check is advisory and evidently was not performed at submission-generation time), 23 of this window's 44 submissions (52%) were found to duplicate or be substantially covered by an existing open backlog item. This is a materially higher rate than recent cycles (typically ~20% reject rate, mostly for reasons other than duplication). Cross-checking confirmed the `idea_intake_prompt.md` §2.0 step 5 backlog-scope advisory existed in the prompt text (added v2.5, `2026-06-09__scheduled`) but its wording ("briefly scan... advisory only — does not block submission") did not require the check to actually be performed or its result recorded — it was possible, and in this case actual, for the check to be skipped entirely at submission time and only surface the resulting duplication cost much later, at STEP 4 classification.

**Where in the routine:**
STEP 4.0.5 (Backlog Scope Advisory, applied at classification time) / `idea_intake_prompt.md` §2.0 step 5 (Backlog scope advisory, at submission time).

**Root cause:**
Process gap — an advisory-only check with no required record of having been performed is not a reliable control, especially once the target backlog has grown large enough (341+ items, 20+ prior idea-intake windows) that genuinely novel governance/process-improvement ideas are increasingly rare. The check existed but had no teeth.

**Blast radius analysis:**
- What would have propagated: continued high duplicate-submission rates at every future idea-intake window as the backlog keeps growing, wasting agent-generation effort and STEP 4 classification time on submissions that were foreseeably redundant.
- When it would have surfaced: gradually, as a slow rise in reject-rate noise across cycles rather than a single sharp failure — the kind of drift that's easy to rationalize cycle-by-cycle ("just a slightly higher reject count this time") without ever being traced to its root cause.
- Recovery cost if uncaught: low-medium — a process-yield/efficiency issue, not a decision-correctness issue (all 23 duplicates were correctly caught and rejected, not wrongly promoted).

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/idea_intake_prompt.md`
  - Section: §2.0 Parked Queue Pre-Check, step 5 (Backlog scope check)
  - Change: upgraded from prose-advisory ("briefly scan... advisory only") to a mandatory act (outcome remains non-blocking) — the submitting agent must grep-check `backlog.md` for each planned topic before finalising it and explicitly record the result (no overlap found / overlap found + relationship noted / topic dropped). A submission restating an existing item with no materially new angle no longer counts toward the agent's minimum.
  - Version: 2.7 → 2.8
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

## Recurrence Escalations

None — Friction Item 1 is newly identified this cycle (not previously flagged, "Not checkable"/"No" per the recurrence check against `2026-07-24__scheduled`'s lessons_learnt.md).

**Advisory note (non-blocking, not itself an escalation):** While applying the Friction Item 1 patch, `claude/system/changelogs/idea_intake_changelog.md` was found to be missing rows for versions 2.6 and 2.7 (2.3, 2.4, 2.5 confirmed present in `prompt_change_log.md`/`OPERATIONAL_GUIDE.md` history; 2.6/2.7 not found by a quick search of either). This is the same class of companion-changelog-lag pattern that `shared_standards.md §11`'s v3.17 rule exists to prevent going forward — but the specific 2.6/2.7 gap predates that rule (added 2026-07-17) and was not backfilled this cycle (out of the immediate scope of the Friction Item 1 patch; flagged in the changelog file itself with an inline note rather than silently left unremarked).

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|--------------------------|
| `claude/system/roadmap_prompt.md` | STEP 2.3 | SI-02 credential-fallback guidance added (resolving `2026-07-24__scheduled` Friction Item 2 deferred patch) | 9.5 → 9.6 | Yes |
| `claude/system/idea_intake_prompt.md` | §2.0 step 5 | Backlog-scope-overlap check upgraded from advisory prose to a mandatory, recorded act (this cycle's own Friction Item 1) | 2.7 → 2.8 | Yes |

---

## New files created this run

- `claude/cycles/2026-07-27__scheduled/run_manifest.md`
- `claude/cycles/2026-07-27__scheduled/cycle_record.md`
- `claude/cycles/2026-07-27__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-27__scheduled/lessons_learnt.md` (this file)
- `claude/ideas/window_summary_IW-20260727-01.md` (committed separately, commit `4672b5b7`)

---

## Outstanding deferred patches

None — the one inherited patch was resolved this cycle; the one new patch identified this cycle was applied action-now.

---

## Escalations

None.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `claude/system/changelogs/idea_intake_changelog.md` is missing historical rows for v2.6/v2.7 (found while applying this cycle's own v2.8 patch) — not backfilled this cycle. | If a future governance-drift audit (`run audit`) or meta-review touches this file, backfill the missing 2.6/2.7 rows from `prompt_change_log.md`/`OPERATIONAL_GUIDE.md` §14 cross-references if they can be located, or note them as genuinely undocumented if not. | Roadmap |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-27__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-27T15:10:00Z",
  "friction_item_count": 1,
  "action_now_count": 1,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
