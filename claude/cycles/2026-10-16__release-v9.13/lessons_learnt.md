Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-16

---

# Lessons Learnt — Release Planning 2026-10-16__release-v9.13

## Friction Items

**Friction Item 1: the gating-item-shipped list is read, but its findings cannot be written back.** This was the first run under ST-40's mandatory read of the "gating item shipped — verify" list. Five items (`BLG-OPS-18`, `-19`, `-23`, `-77`, `-85`) have gates whose whole condition is a shipped item, so this run treated them as ungated. §1.3a's gate-field carve-out covers only the date-lapsed list, so their stale gate text stays until `groom backlog`, and the next scan will list them again. Two more items need a split or clarification rather than a clearance (`BLG-QA-75`, `BLG-GOV-103`). Recommendation: either let §1.3a's carve-out clear a gate whose whole condition is a cited shipped item (same evidence bound as option (a)), or have `groom backlog` read this list as a standing step. Deferred to the Head of Specs Team (`release_planning_prompt.md` §1.3a / `backlog_management_prompt.md`).

**Friction Item 2: P2-first ordering can lower the build-and-ship share while Skill-Silo is above ceiling.** The three Product-Owner-committed U-items are seated, which meets the §7.1 sustained-failure clause. But §1.4c seated `BLG-QA-227` (P2, 3.5d after calibration, test infrastructure) before any P3, and four of the five newly ungated Ops items took 4.5d of the round-robin. The U share fell from 42% (v9.12) to 31%. STEP 3's rotation guideline is advisory, and §1.4c has no step that weighs it. Recommendation: no prompt change yet. Watch the next rebalance's §7.1 reading. If it worsens, consider a §1.4c step that seats ready U-items ahead of the round-robin while the sustained-failure clause is active. Observation only.

**Friction Item 3: `strategy_rules.md` edits keep entering sprints with no write route.** `BLG-GOV-376` and `BLG-GOV-377` say in their own Problem text that Sprint Execution cannot write `strategy_rules.md`. ST-05, ST-06 and ST-07 may also need to. The only precedent (v9.9 ST-20) relied on an explicit user instruction given in-session. This run carried the question as RISK-02, a pre-sprint decision. Recommendation: give `strategy_rules.md` a named-file rule like the one `ESC-CLOSE-20261006-01` gave `claude/roadmap/*` (sealed AC names the exact section; Strategy Rules & System Intent Owner sign-off; `delegated_decision` classification), so these items stop needing a per-cycle ruling. Deferred to the Head of Specs Team with the Strategy Rules & System Intent Owner (`execution_prompt.md` §7).

## Prompt Change Classification

No action-now patches. Friction Items 1 and 3 are deferred patches (Head of Specs Team). Friction Item 2 is an observation for the next rebalance.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-10-16__release-v9.13",
  "phase": "Release",
  "filed_utc": "2026-10-16T08:15:13Z",
  "friction_item_count": 3,
  "action_now_count": 0,
  "deferred_count": 2,
  "status": "Active"
}
```
