Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-10
Cycle: 2026-08-08__release-v8.5

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Post-ship closure of v8.5 — Frontend Correctness, Design Consistency & Security Hardening (25/25 stories shipped, Verified, no deviations)
Run: 2026-08-08__release-v8.5
Reviewed by: PMO Lead
Date filed: 2026-08-10
Prior cycle checked: 2026-08-07__release-v8.4 (`lessons_learnt_closure.md`)

---

## What worked well

- Zero-deviation, zero-QA-fail, zero-traceability-gap delivery across 25 stories and 6 EPICs made STEP 3 (Backlog Reconciliation) and STEP 5 (Deviation Compliance) mechanically simple — 25/25 backlog items located and marked complete on the first pass via the `v8.5 Release Slice` table's exact Item/Epic/ST mapping, no missing-entry gaps.
- The prior cycle's (`v8.4`) `lessons_learnt_closure.md` Carry-Forward item #2 — flagging `post_ship_closure.md` STEP 7.3's hardcoded "§27" reference as stale — was independently and exactly reproduced live during this cycle's own STEP 7 execution (the real §27 is "Test Coverage Gaps — v5.0"; the one genuinely Open TSG entry sits at §19.3). The carry-forward mechanism worked as designed: the prediction was specific enough to confirm on contact, and per §3.7's 2-cycle-unapplied rule this was actioned as an immediate patch this run rather than deferred a 3rd time.
- STEP 6's Endpoint Coverage Drift Check found 0 drift (0 of 133 `openapi.yaml` method+path entries missing from `api_performance_baseline.md` after path-parameter normalisation) — ST-21's own commit correctly updated the baseline doc for the new `GET /screener/regime-distribution` endpoint in the same commit as the contract, per `CLAUDE.md`'s non-negotiable.

---

## Friction Log

### Friction Item 1

**Classification:** Type C — Dependency Stall

**Recurrence:** Yes — appeared in `2026-08-07__release-v8.4` (Carry-Forward #2)

**What happened:** STEP 7.3's instruction to reconcile "§27 (Technical Specification Gaps)" no longer matches `Specs_Index.md`'s actual structure — the document's Test Coverage Gap register is append-only and chronologically numbered, so a new `## N. Test Coverage Gaps — vX.Y` section is appended (and the fixed "§27" reference drifts further stale) essentially every cycle the condition fires. This cycle's actual §27 is "Test Coverage Gaps — v5.0"; the one genuinely `Status: Open` TSG entry (`TSG-v33-03`) is located at §19.3, unrelated to any number near 27.

**Where in the routine:** STEP 7.3 — TSG backlog reconciliation.

**Root cause:** document staleness (fixed section-number reference against an append-only, renumbering document structure).

**Blast radius analysis:**
- What would have propagated: a 3rd consecutive Post-Ship Closure would locate and reconcile the wrong section (or none), silently missing genuinely resolved TSG entries and letting stale `Status: Open` markers accumulate undetected.
- When it would have surfaced: only when a future closure run happened to manually notice the mismatch, as this cycle and the prior cycle's carry-forward both did independently — not systematically caught by the routine itself.
- Recovery cost if uncaught: low (single-file fix) but compounding — each cycle it remains unfixed is one more manual-catch dependency rather than a reliable instruction.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 7.3
  - Change: Replaced the hardcoded "§27 (Technical Specification Gaps)" reference with an instruction to scan the full document for `**Status:** Open` fields on `TSG-*`-prefixed entries, looking up each entry's own `**Backlog item:**` field rather than relying on any fixed section number.
  - Version: 2.25 → 2.26
  - Confirmed by: Head of Specs Team (post-ship closure STEP 8 immediate-action rule)
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|----------------|---------------------------|--------------|
| `scripts/check_api_performance_baseline_drift.py`'s substring-based endpoint matching produces false negatives for endpoints mentioned in prose without an actual measurement row. | `2026-08-07__release-v8.4` closure (Friction Item 1 / Outstanding deferred patch) | Require table-row context, not bare substring match, for an endpoint to count as "documented" — deferred, target "next revision of the script," owner Infrastructure & Operations Owner. `prompt_change_log.md` checked: no matching entry since `2026-08-08`. Unapplied after 2 consecutive cycles. | Infrastructure & Operations Owner |
| `execution_prompt.md`'s STEP 3.1.A/STEP 5 has no explicit cross-reference requiring the EPIC-level `execution_state.json.test_scenarios` array to be backfilled from story-level `spec_references`. | `2026-08-07__release-v8.4` Phase 4 (already flagged as a Recurrence Escalation within this cycle's own `lessons_learnt_cycle.md` §Phase 4) | Add explicit cross-reference in `execution_prompt.md` STEP 3.1.A/STEP 5 — deferred, target "next `execution_prompt.md` revision touching STEP 3.1.A or STEP 5," owner Head of Specs Team. Unapplied after 2 consecutive cycles (symptom itself did not recur this cycle — every EPIC's `test_scenarios` field was independently populated or validly short-circuited — but the prompt-level fix making this reliable by construction remains outstanding). | Head of Specs Team |

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/post_ship_closure.md` | STEP 7.3 | Replaced hardcoded "§27" TSG reference with a full-document `Status: Open`/`TSG-*` scan | 2.25 → 2.26 | Yes |

---

## New files created this run

- `claude/cycles/2026-08-08__release-v8.5/closure_state.json`
- `claude/cycles/2026-08-08__release-v8.5/lessons_learnt_closure.md` (this file)
- `claude/cycles/2026-08-08__release-v8.5/closure_record.md` (STEP 9, filed immediately after this record per the documented sequencing note)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | §3.2.A or §5.3 (agent-mediated sign-off protocol) | Add an explicit instruction to invoke the `governance-drift` skill's Step 1b self-consistency check whenever a story's own work bumps `OPERATIONAL_GUIDE.md`'s version — closes the gap between "a check exists" and "the check is mandatorily run," per this cycle's ST-23 sign-off catching a 9th recurrence of the same drift class by inspection rather than mandatory tooling. | Head of Specs Team | Next `execution_prompt.md` revision touching §3.2.A or §5.3 |
| `claude/system/execution_prompt.md` (§5.3) or `docs/qa/qa_evidence_template.md` | DoQ sign-off protocol | Require the sign-off block to explicitly restate the final CI run confirming green (run ID or "all N checks green" + `head_sha` match) whenever a story's PR needed a post-open CI-triggered fix, not just record that the fix was applied — closes an inconsistency this cycle's own EPIC-06 sign-off exhibited relative to EPIC-03/EPIC-04's more rigorous restatement. | Head of Specs Team | Next `execution_prompt.md` §5.3 or `qa_evidence_template.md` revision |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| `BLG-GOV-292` (bracket-delimited gate-language detection gap in `scan_backlog_gate_conditions.py`) is the 5th distinct failure mode in the same gate-detection problem class since `BLG-GOV-286`'s `v8.4` fix covered 4 named modes — surfacing again in the very next cycle — and carries `Provisional-Target: TBD` (no named target release). | Missing target / Recurrence pattern | Head of Specs Team | A deferred patch with no target date is an invalid deferred patch per lessons-learnt §6.2 and must be escalated. Separately, this cycle's own `lessons_learnt.md` Carry-Forward explicitly asked this closure to assess whether the pattern (a new mode surfacing every cycle since the fix shipped) now warrants firmly scheduling `BLG-GOV-292` or considering a structural redesign of the gate-detection approach rather than continued one-off patches. Decision needed within 72 hours (by 2026-08-13): assign a firm target release for `BLG-GOV-292`, or explicitly accept the residual risk at current low priority. |
| `DEV-EPIC02-ST03-01` (Cohort Analysis client-side-computation deviation, filed `v1.9`) stale-target re-triage, carried from `v8.4` closure with an explicit deadline of "before next `plan release`." Next release planning (`v8.5`, `2026-08-08`) has already run without a recorded re-triage — the deadline has passed. | Missing target / Deadline missed | Head of Specs Team | Both this cycle's own `sprint_planning_notes.md` and `sprint_backlog.md` independently flagged this as unresolved and instructed it to "surface again at this cycle's Post-Ship Closure if still open" — confirmed still open (`analytics.md`'s Change Log has no entry beyond the original `1.4` filing). Decision needed within 72 hours (by 2026-08-13): accept client-side cohort computation as canonical (update `analytics.md` §15's hard rule) or schedule the backend-migration fix. |

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `scripts/check_api_performance_baseline_drift.py`'s substring-matching false-negative fix and the `execution_prompt.md` `test_scenarios` roll-up cross-reference have now both carried forward 2 consecutive cycles (`v8.4`→`v8.5`) without a `prompt_change_log.md` entry, per the Recurrence Escalations table above. | If either remains unapplied at the next Post-Ship Closure, per `shared_standards.md §6.4` this pattern (2+ cycles unapplied) itself becomes evidence that the deferred-patch mechanism alone is insufficient for these two items — the next closure should consider applying them directly as immediate actions rather than deferring a 3rd time, as this cycle did for the §27 TSG reference. | All |
| 2 | `reports.md` still carries exactly 2 of the 10-record cross-cycle deviation register (`DEV-REPORTS-ST06-01`, `DEV-REPORTS-ST01-02`) — unchanged from `v8.4`'s light concentration signal, since 0 deviations were filed this cycle. | The next (3rd) deviation consolidation review run (STEP 5.1, not due this cycle — 1 of 3 cycles since the `2026-08-08` run) should re-check whether a 3rd `reports.md` deviation has been filed before escalating to a dedicated audit. | All |
| 3 | `BLG-GOV-292`'s escalation (see Escalations above) and the underlying 5-failure-mode gate-detection pattern remain open pending Head of Specs Team's 72-hour decision. | If unresolved by the next Roadmap Rebalance or Release Planning run, surface this as a still-open decision rather than re-deriving the pattern from scratch. | Roadmap |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-08-08__release-v8.5",
  "phase": "Post-Ship",
  "filed_utc": "2026-08-10T16:45:00Z",
  "friction_item_count": 1,
  "action_now_count": 1,
  "deferred_count": 2,
  "escalation_count": 2,
  "overdue_patches": 0,
  "status": "Complete"
}
```
