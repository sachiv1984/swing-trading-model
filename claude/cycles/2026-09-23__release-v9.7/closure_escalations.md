Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-28
Cycle: 2026-09-23__release-v9.7

---

# Closure Escalations — 2026-09-23__release-v9.7

Format per `claude/system/shared_standards.md §4`.

---

## ESC-CLOSE-20260928-01

| Field | Value |
|-------|-------|
| Issue | `execution_prompt.md §3.2.A` needs a same-EPIC cross-story testing-gap disclosure consistency check. First deferred at `2026-09-15__release-v9.5` closure, carried unapplied through `2026-09-21__release-v9.6` closure (flagged there as "2nd cycle — watch: if still unapplied at the next post-ship closure, this crosses the `lessons_learnt_prompt.md §3.7` two-cycle threshold"), and confirmed still unapplied at this closure (`execution_prompt.md` remains at v3.79 with no §3.2.A change of this shape; `prompt_change_log.md` searched by topic, no matching entry found). |
| Type | Recurrence escalation — `lessons_learnt_prompt.md §3.7` mandatory trigger (deferred patch carried 2+ cycles without a `prompt_change_log.md` entry) |
| Escalated to | Head of Specs Team |
| Reason | No concrete replacement wording was ever locked down for this patch across its 2 prior deferrals (unlike Release Planning lessons_learnt.md Friction Item 1, which had unambiguous wording and was applied immediately at this same closure) — implementing it now without that wording risks guessing at scope. A ruling is needed on: (a) the exact §3.2.A check text, or (b) an explicit decision to retire this deferred patch if it is no longer considered worth implementing. |
| Tracking | SLA 2026-10-01 (72h from filing) |
| Disposition | Open |

---

## ESC-CLOSE-20260928-02

| Field | Value |
|-------|-------|
| Issue | Release Planning lessons_learnt.md Friction Item 3 (`2026-09-23__release-v9.7`): `2026-09-19__scheduled`'s STEP 8.1 Option(b) rebalance-equivalence rationale explicitly named only `v9.6` as the release it justified opening, but has now been cited a second time (unmodified) to open `v9.7`, since no rebalance has run since. |
| Type | Governance-prompt scope ambiguity — decision required |
| Escalated to | Head of Specs Team |
| Reason | Ruling needed on whether `release_planning_prompt.md §-1.2` should require the cited Option(b) record to postdate the *immediately prior* release-planning cycle (forcing a fresh rebalance every 2 releases at minimum), or whether unlimited reuse until the next rebalance runs is the intended design. Not actioned in this closure — no unambiguous fix wording exists yet, unlike Friction Item 1 (applied same-cycle, see `prompt_change_log.md` 2026-09-28 entry). |
| Tracking | SLA 2026-10-01 (72h from filing) |
| Disposition | Resolved — 2026-10-05, Head of Specs Team ruling (agent-mediated, §5.3, user-directed). A STEP 8.1 Option(b) record clears `release_planning_prompt.md` §-1.2 for one release only. It must have been created after the `release_plan.md` of the most recent `Published` release; otherwise §-1.2 halts and a scheduled rebalance must run first. Unlimited reuse is not the intended design. Applied as `release_planning_prompt.md` v2.58→v2.59 (see `prompt_change_log.md` 2026-10-05). Was not triggered at v9.8 or v9.9, because both cited fresh same-day rebalance records. |

---
