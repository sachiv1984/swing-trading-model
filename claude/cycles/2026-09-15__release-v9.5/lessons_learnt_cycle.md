Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-18 (delivery verification — Phase 4 section appended); prior — 2026-09-18 (sprint close — Phase 3 section added)
Cycle: 2026-09-15__release-v9.5

---

## Phase 3

**Phase:** Sprint Execution
**Cycle:** 2026-09-15__release-v9.5
**Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
**Filed:** 2026-09-18
**Reviewed by:** PMO Lead

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| 25 stories (EPIC-02 ST-05–14, EPIC-03 ST-15–20, EPIC-04 ST-22–30) had `deviations_filed = false` in `execution_state.json` despite their `qa_evidence_EPIC-xx.md` entries explicitly confirming the deviation check was completed with nothing to file — a write-timing gap, not a missed check. | Phase 3 | Type A — Governance Drift: A documented rule or header requirement was ignored or missed | action-now | Corrected at STEP 5.1 sprint close per its own auto-correction rule (no deviation record existed to review, so the mechanical fix applied cleanly); see `execution_state.json` process_notes and `sprint_close.md` | PMO Lead | — |
| `OPERATIONAL_GUIDE.md` §14 quick-reference table's `Last Updated` cell was never actually updated across 6 consecutive `Version` bumps in PR #1716 (v4.190→v4.196), despite every one of the 6 commit messages explicitly claiming `"§14 self-row Version/Last Updated ...→...2026-09-18"`. The `governance-drift` skill's self-consistency check apparently only verifies the `Version` cell, not its sibling `Last Updated` cell in the same table row. | Phase 3 | Type A — Governance Drift: A documented rule or header requirement was ignored or missed | defer | Fixed the current cell value; filed `BLG-GOV-336` to extend the `governance-drift` skill's check to cover this 4th field so it doesn't silently drift again | Head of Specs Team | BLG-GOV-336 |
| ST-42 (EPIC-06) correctly filed `BLG-QA-180` when its own execution found no Playwright test asserts the specific `duration` values it introduced. ST-41, in the same EPIC, had the identical gap (no test asserts the 4 components' actual `delay`/`duration` transition-prop values) but no equivalent item was filed during that story's own execution — only caught by the later, independent PR review pass. No structural check in `execution_prompt.md` currently cross-checks sibling stories in the same EPIC for this class of gap. | Phase 3 | Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced | defer | Filed `BLG-QA-181` to close the immediate gap; the underlying systemic question (should `execution_prompt.md` §3.2.A gain a same-EPIC cross-story consistency check for "testing-gap disclosure" as a category, not just spec_references roll-up) is flagged here for Head of Specs Team consideration rather than speculatively added this cycle | Head of Specs Team | Next `execution_prompt.md` revision touching §3.2.A |
| ST-37/ST-38 (EPIC-05) wrote to `claude/roadmap/workforce_capacity.md`, a path `execution_prompt.md` §7 lists under "Must not modify: `claude/roadmap/*`" with no carve-out. The engine treated the sealed `sprint_backlog.md`'s own "Within-EPIC only: workforce_capacity.md" sequencing note as implicit authorization — a defensible but unstated inference, not an explicit exception in §7's own text (unlike the existing, explicitly-documented `backlog.md` new-item exception). | Phase 3 | Type E — Authority Gap: A decision was needed and no role was clearly empowered to make it | decision | Disclosed transparently in the PR's own agent-mediated review and filed `BLG-GOV-337` for a Product Owner + Head of Specs Team ruling on whether this should become a standing, narrow write-scope exception | Product Owner + Head of Specs Team | BLG-GOV-337 |

**Recurrence Notes:**
The cross-EPIC-branch `execution_state.json`/`backlog.md` merge-conflict pattern recurred twice this cycle (EPIC-04→`main`, and `main`→EPIC-06 after EPIC-05 merged) — both resolved cleanly using the already-established CLAUDE.md §8 union/main-authoritative rules with no new gap found; not logged as a fresh friction item since the existing mitigation worked as designed both times. This is the 3rd+ consecutive cycle this exact pattern has occurred and been handled correctly — worth noting as a stable, working control rather than a recurring problem.

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-09-15__release-v9.5
**Section anchor:** `## Phase 4` (stable — cycle_id in field above, not in header)
**Filed:** 2026-09-18
**Reviewed by:** PMO Lead
**Prior cycle checked:** 2026-09-14__release-v9.4 (`lessons_learnt_cycle.md` `## Phase 4`) — 1 friction item filed: `Pass, escalation open` misapplied to an incidental backlog-item finding rather than a genuine open escalation (ST-05/EPIC-01). Checked and confirmed not recurring this cycle — no `qa_evidence_EPIC-xx.md` row this cycle uses `Pass, escalation open` at all (the value did not arise; not applicable to assess recurrence either way).

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| `qa_evidence_EPIC-04.md`'s own autonomous-class eligibility check (ST-22) disclosed a genuine self-graded ambiguity in BLG-GOV-19 Criterion 1 and explicitly stated its own sign-off "should not be treated as final" without human Director of Quality confirmation — but PR #1715 merged, and this delivery verification run (also an autonomous engine run) reached this same EPIC's evidence without that confirmation having occurred. `BLG-GOV-335` was filed to obtain the ruling, but STEP -1.3's Tier 2 gate has no defined behaviour for the case where the *reviewing* engine (delivery verification) is itself the same class of self-certifying agent as the one that raised the doubt — there is currently no mechanism in this framework that forces a genuinely human decision point when both the authoring and the verifying steps are agent-mediated. | Phase 4 | Type E — Authority Gap: A decision was needed and no role was clearly empowered to make it | decision | Recorded as an open, non-blocking compliance advisory in `verification_report.md §1`/§3`; `BLG-GOV-335` remains the ruling vehicle (Owner: Head of Specs Team). Flagged here as a systemic gap for consideration: should `delivery_verification_prompt.md` STEP -1.3's Tier 2 treatment require an *actual* human signature (not an agent-mediated one) whenever the underlying EPIC's own evidence discloses self-doubt about its own gate eligibility, as distinct from routine agent-mediated sign-off? | Head of Specs Team | `BLG-GOV-335` |

**Recurrence Notes:**
No other Phase 4-relevant recurrence this cycle. Gate sequencing, deviation severity calls (none filed this cycle — zero `DEV-*` records), test scenario coverage (no gaps), and sign-off coordination all proceeded cleanly across all 6 EPICs.
