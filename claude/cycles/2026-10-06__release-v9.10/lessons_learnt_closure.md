Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-07

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Make every live stop come from one `strategy_rules.md` §11 parameter source (`BLG-BE-138`, P1 Correctness Fast-Track). Show the ATR, multiplier, recalculation source and already-known exit conditions behind each position (`BLG-FE-193`, `BLG-FE-198`, build-and-ship). Clear v9.10's lifecycle and gap-risk rulings and its AI-governance, ops and QA hygiene items. 21 stories across 4 EPICs.
Run: 2026-10-06__release-v9.10
Reviewed by: PMO Lead
Date filed: 2026-10-07
Prior cycle checked: 2026-09-30__release-v9.9 (`lessons_learnt_closure.md`)

---

## What worked well

- **Tracing.** All 21 shipped stories traced to their `BLG-*` source items in one scripted pass (STEP 3), using each slice entry's `**Source:**` field. Every COMPLETE banner carries the EPIC PR and story commit SHA from `execution_state.json`.
- **Split-achievability carve-out.** Two candidates were checked, ST-18 (AC 1 narrowed) and ST-20 (AC 2 partly met). Neither has an open escalation, and each remainder has its own new tracking item (`BLG-OPS-182`, `BLG-GOV-377`). So the source items `BLG-OPS-171` and `BLG-SPEC-171` were correctly marked COMPLETE.
- **v9.9 carry-forward items all closed.**
  - `ESC-CLOSE-20261006-01` was resolved at Sprint Planning.
  - `BLG-FE-193` was seated and shipped (ST-06).
  - The `BLG-GOV-362` §3.7 recurrence was cleared by `execution_prompt.md` v3.83 and `sprint_planning_prompt.md` v3.20/v3.21, after sprint close and before this closure.
- **Test-coverage weaknesses.** The cycle's own PR reviews caught and backlogged all 3 (`BLG-QA-214/215/216`), as in v9.9. STEP 7 only had to register them in §50.
- **Endpoint coverage drift (STEP 6).** 0 gaps, 147 endpoints, no new routes.
- **The STEP 5.1 consolidation review (due this cycle) found two genuine problems** that no per-cycle step could have seen (see Friction Log). This confirms the cadence review is still doing real work.

---

## Friction Log

**Closure-phase finding: the STEP 1.5 digest command still does not run as written.**
- What happened: system `python3` failed at `import psycopg2`, the same failure recorded at v9.9.
- Workaround this run: it ran under `PYTHONPATH=backend backend/.venv/bin/python3` and returned `sent: false`, because no Telegram credentials are set in this sandbox. The step is non-blocking.
- Status: this was carried from v9.9 as a deferred patch. It is now applied (`post_ship_closure.md` v2.38).

**Closure-phase finding: an open deviation lost its only tracking item.**
- What happened: STEP 5.1 found that `DEV-REPORTS-ST06-01`'s backlog reference, `BLG-SPEC-87`, was archived at the `2026-08-03__release-v8.1` closure. It sits under `BLG-SPEC-86`'s retirement block, never shipped, and has `Provisional-Target: TBD`. The deviation is still live in code.
- Why it went unseen: the sixth review checked only that a reference was present, not that it was active.
- Status: the method fix is applied (`post_ship_closure.md` v2.38 STEP 5.1 active-reference check). Restoring the item is outside this routine's backlog write scope, so it is an Outstanding Action.

**Closure-phase finding: earlier consolidation registers undercounted.** The heading-only scan missed 6 records written as bold paragraphs or `## Known Deviations` table rows. One of them, `DEV-v3.4-01`, shows resolution-status drift: its backlog item `BLG-SPEC-31` is COMPLETE in v3.5, but the spec row is unchanged. The scan fix is applied in v2.38. The spec-row correction is an Outstanding Action for the spec owner.

**Closure-phase finding: placeholders in the scope and decisions documents.** Both v9.10 documents carry a `Superseded by: [TBD]` / `Changelog: [TBD]` block marked "To be completed at Post-Ship Closure". STEP 4 only names the header supersession note. They were filled this run. The v9.9 documents still show `[TBD]` in the same block. That is a one-off miss already covered by the block's own instruction, so no new action is needed.

**Deviation consolidation review (STEP 5.1):** due and run (seventh run, `docs/governance/deviation_consolidation_review_2026-10-07.md`). The counter resets to `0` at STEP 10.

---

## Recurrence Escalations

No new `§3.7` recurrence escalation was raised this closure.

- **Phase 3 recurrence: `BLG-GOV-362` prompt patches, 2nd carry.** Already cleared by `execution_prompt.md` v3.83 and `sprint_planning_prompt.md` v3.20/v3.21 (commits `0a123c52`, `090bb0ea`, 2026-10-07). Closed.
- **`delivery_verification_prompt.md` STEP 2.1/2.3 "no remainder" path (v9.9 Phase 4 Friction Item 1, 1st carry).** Applied this run before it could reach a 2nd carry.

One **decision_required** item was escalated. It is not a recurrence: Release Planning Friction Item 2 is tracked as `ESC-CLOSE-20261007-01` (see Escalations).

---

## Process improvements actioned this run

Seven immediate actions were applied under the same-cycle application pattern (`post_ship_closure.md` STEP 8).

**`claude/system/execution_prompt.md` v3.83→v3.84:**
1. **LL-v9.10-P3-01 (Phase 3 Friction Item 1).** New §3.1.B step 2a: a workflow-viability pre-check before raising a live-fire or workflow-dispatch delegation. Record the last successful run, and raise any prerequisite fix in the same delegation.
2. **LL-v9.10-P3-02 (Phase 3 Friction Item 2).** §3.2.A gains a `Pass_with_deviation` self-check over every consolidation row before DoQ sign-off is requested.
3. **LL-v9.10-P3-03 (Phase 3 Friction Item 3).** New §3.1.A step 4c: record the Playwright CI conclusion for a story commit that adds or changes a Playwright spec before setting `done`. Pending runs carry a `ci_pending` note that STEP 3.2.A must clear.
4. **LL-v9.10-P4-01 (Phase 4 Friction Item 1).** STEP 5.1 gains a `spec_references` path-existence check at sprint close. Its own target was "next revision touching STEP 5.1", which this revision is.

**`claude/system/delivery_verification_prompt.md` v3.13→v3.14:**

5. **LL-v9.9-P4-01 (carried, 1st carry).** STEP 2.1/2.3 gain a `Pass_with_deviation` no-remainder variant: the comment may cite an Owner ruling that fully disposes of the narrowing in place of a backlog item.

**`claude/system/post_ship_closure.md` v2.37→v2.38:**

6. **Carried v9.9 closure action.** The STEP 1.5 digest command now runs as written (venv plus `PYTHONPATH=backend`).
7. **Closure-phase finding (seventh consolidation review, Findings 1 and 2).** The STEP 5.1 scan now covers bold-paragraph and table-row `DEV-*` records, and adds an active-backlog-reference check for open records.

The CLAUDE.md §6 checklist is complete:
- Component changelogs updated (`execution_prompt_changelog.md` 3.84, `delivery_verification_changelog.md` 3.14, `post_ship_closure_changelog.md` 2.38).
- `OPERATIONAL_GUIDE.md` v4.225→v4.226: §8/§9/§10 source-prompt headers, §14 rows and self-row, Change Log row.
- 4 rows added to `prompt_change_log.md`.
- `governance-drift`: all in sync.

**Application rate:** 7 of the 10 action items reviewed were applied immediately. That counts this cycle's 7 friction items plus the 3 open v9.9 deferred patches, excluding resolved and closed carries.

---

## New files created this run

- `claude/cycles/2026-10-06__release-v9.10/closure_state.json`
- `claude/cycles/2026-10-06__release-v9.10/closure_escalations.md`: 1 decision-required escalation (`ESC-CLOSE-20261007-01`)
- `claude/cycles/2026-10-06__release-v9.10/closure_record.md`
- `claude/cycles/2026-10-06__release-v9.10/lessons_learnt_closure.md` (this file)
- `docs/governance/deviation_consolidation_review_2026-10-07.md`: seventh cross-cycle `DEV-*` consolidation review

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target | Cycles carried |
|------|---------|----------------|-------|--------|-----------------|
| `scripts/scan_backlog_gate_conditions.py` | Gate parsing | Treat a literal `Gate criteria: None`/`N/A` as ungated (or require "Opportunistic"/"Cadence" plus a date). Then have `groom backlog` confirm that each of the 17 affected P3 items still deserves a slot (Release Planning Friction Item 1). The natural vehicle is `BLG-GOV-373`. | Head of Specs Team / Head of Engineering | `BLG-GOV-373` / next `groom backlog` | 1st cycle (new) |
| `claude/system/roadmap_prompt.md` / `backlog_management_prompt.md` | Gate clearance | When a gate is cleared, the same edit refreshes any AC that names the gate's date or the gating item (Release Planning Friction Item 3). Deferred because which engine owns gate-clearance edits depends on the `ESC-CLOSE-20261007-01` ruling. | Head of Specs Team | After `ESC-CLOSE-20261007-01` is resolved | 1st cycle (new) |
| `shared_standards.md` §16.4.1 / `.github/workflows/` | SLA-breach surfacing | Scheduled reminder for `Open` escalations past `sla_due_utc` (v9.9 Phase 3 Friction Item 3). | PMO Lead | Next lifecycle audit (`run audit`, now due at `completed_cycle_count` 87) | 2nd cycle (deferred to a named date, not yet due) |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| Release Planning §1.3a in-place gate-text edits of existing `backlog.md` items are outside the `BLG-GOV-362` / `ESC-CLOSE-20261006-01` named-file rule (Release Planning Friction Item 2). | Decision required: write-scope authority gap | Head of Specs Team (with Product Owner) | Options: authorise directly, route to `groom backlog`, or keep read-only with an allow-list via `BLG-GOV-373`. Tracking: `ESC-CLOSE-20261007-01`, SLA 2026-10-10T12:00:00Z. Non-blocking. |

---

## Carry-Forward
Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `ESC-CLOSE-20261007-01` is open (SLA 2026-10-10). | Until it is ruled on, the next `plan release` should keep v9.10's read-only practice for §1.3a date-lapsed items. `BLG-FEAT-62` and `BLG-OPS-53` will re-surface as false-positive lapses. | Release Planning / any next-invoked routine |
| 2 | `completed_cycle_count` becomes 87 at this closure. That is a multiple of 3, and also the v9.9 SLA-reminder patch's named target. | Run `run audit` before the next Phase 1B opens. The audit should pick up the deferred SLA-breach reminder patch. | Lifecycle audit |
| 3 | `completed_cycle_count` was even (86) at this closure's STEP 0. | A scheduled rebalance is due (`run roadmap --reason scheduled`) before `plan release`. It should also confirm or close `BLG-GOV-355` (carried v9.9 action). | Roadmap Rebalance |
| 4 | `BLG-BE-147` (P2, filed in-cycle): the grace alert, the "Day N of 10" label and review-cadence suppression still count `days_in_state`, not calendar days since entry. ST-12 fixed only the Positions badge. | This is a ready P2 correctness follow-up on the same §6 grace window v9.10 just corrected. It should be weighed for v9.11 seating. | Roadmap Rebalance / Release Planning |
