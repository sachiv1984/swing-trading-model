Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-14 (initial filing)
Cycle: 2026-09-09__release-v9.3

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Ship v9.3: close all 27 backlog-driven debt items in scope — backend reliability/data-correctness debt (4 items), QA/test-infrastructure debt (6 items), operations/cost-monitoring debt (5 items), spec/documentation debt (5 items), and governance-process debt & security (7 items).
Run: 2026-09-09__release-v9.3
Reviewed by: PMO Lead
Date filed: 2026-09-14
Prior cycle checked: 2026-09-07__release-v9.2 (`lessons_learnt_closure.md`) — 0 deferred patches remained open from that closure (all 7 outstanding actions were resolved same-day via an Addendum) — nothing to re-verify as carried-in this cycle.

---

## What worked well

- STEP 0's parallel reads of `verification_report.md`, `execution_state.json`, and `sprint_close.md` again produced a single, internally consistent picture of the cycle (27/27 stories done, 0 formal `DEV-*` deviations filed, 2 P3 Known Deviations recorded in `structured_logging_standards.md`, 1 open non-blocking escalation carried past close) with no contradictions across the three sealed sources.
- The `stage4_backlog_slice.md` ST→BLG source mapping made STEP 3 Backlog Reconciliation for all 27 items fully mechanical via a single scripted pass — every `### BLG-*` heading matched, every status marker inserted in one run, 0 not-found.
- `2026-09-07__release-v9.2`'s own closure resolved every one of its 7 outstanding actions same-day; this cycle's own STEP 8 confirmed none of them recurred (the Phase 3/Phase 4 friction items reviewed below are all new, not repeats of previously-"fixed" gaps) — the closure-to-closure Carry-Forward mechanism continues to function as intended.
- The split-achievability carve-out (STEP 3.1, `LL-v8.9-P-Closure-01`) correctly identified `BLG-GOV-178` (ST-22's backlog source) as carrying an open, carried-forward escalation (`ESC-EXEC-20260910-01`) and left it unmarked rather than COMPLETE — preventing it from being silently archived by this same run's own STEP 12 groom-backlog pass while the escalation is still open, exactly the failure mode the carve-out was written to close.
- The endpoint coverage drift check (STEP 6 advisory), now carrying the v2.33 Markdown-formatting normalisation note (`LL-v9.2-P-Closure-01`, applied at the prior closure), correctly normalised both documents on the first pass this run — no false-positive gap, unlike the false 80-endpoint gap this same check produced at `2026-09-07__release-v9.2` before that fix shipped. Confirms the fix is working as designed.

---

## Friction Log

### Friction Item 1

**Classification:**
Type A — Process/Prompt Gap (a recognised-format validation existed only at the downstream Delivery Verification gate, not at the point the malformed data was written)

**Recurrence:** New this cycle — not carried from `2026-09-07__release-v9.2`.

**What happened:**
`qa_evidence_EPIC-05.md`'s Standard Sign-Off Block used `Signed off by: Sprint Execution Engine` — bare, with no role qualifier — which matched none of `delivery_verification_prompt.md` §-1.3's recognised sign-off formats. This was caught only when Delivery Verification ran (as a Tier 2 structural finding, not a halt), requiring an interactive Director of Quality counter-sign before that run could proceed to its own STEP 1.

**Where in the routine:**
Originates at Sprint Execution (`execution_prompt.md` §5.3, EPIC-05 sign-off); surfaced at Delivery Verification STEP -1.3.

**Root cause:**
No step validates a `qa_evidence_EPIC-xx.md` sign-off line's format against the recognised-format list until Delivery Verification reads it — by which point the EPIC's PR has already merged and the malformed line is baked into a sealed artefact, requiring an out-of-band correction rather than a same-session fix.

**Process patch:**
→ Applied this run (STEP 8 same-cycle application pattern, `LL-v9.3-P4-01`): `execution_prompt.md` §5.3 gains a pre-merge sign-off format lint — validate the `Signed off by:` line against the recognised-format list before the EPIC's PR opens, correcting it in-session if it matches none. `execution_prompt.md` v3.74→v3.75.

### Friction Item 2

**Classification:**
Type B — Enumeration Gap (a genuinely new, non-enumerated Result shape, not an oversight of an existing enum value)

**Recurrence:** Same underlying pattern as `2026-09-07__release-v9.2`'s own Phase 4 friction item 1 (an ad hoc, non-enumerated Result label), though not an exact recurrence — that item's specific fix (`Pass_with_deviation`) is confirmed applied and correct for its own shape; this is a third, distinct shape the enum still had no value for.

**What happened:**
ST-22/EPIC-05's `Result` cell read `Pass, with open escalation` — free text distinct from all four of §2.1's then-enumerated values. ST-22's actual situation (AC's literal wording fully met; a *stronger*, non-AC-mandated evidentiary bar tracked via an open escalation rather than a backlog item) does not fit `Pass_with_deviation` either, whose definition requires the AC itself to be narrowed or partially unmet.

**Where in the routine:**
`delivery_verification_prompt.md` §2.1 (QA Evidence Review — Per-Item Review), enumerated `Result` value set.

**Root cause:**
The enum has grown reactively, one value at a time, each time a new ad hoc label surfaces in live use — this is the second time (after `Pass_with_deviation`) that a genuinely distinct disposition shape was invented as free text before being formally recognised.

**Process patch:**
→ Applied this run (STEP 8 same-cycle application pattern, `LL-v9.3-P4-02`): `delivery_verification_prompt.md` §2.1 gains a `Pass, escalation open` Result value, semantics mirroring `Pass_with_deviation`'s treatment (functionally equivalent to `Pass with notes`, requires the escalation ID named in Comments, no backlog item required since nothing was narrowed or unmet). `delivery_verification_prompt.md` v3.10→v3.11; companion `qa_evidence_template.md` v1.13→v1.14.

### Friction Item 3 (Release Planning, deferred — carried from `lessons_learnt.md`)

**Classification:**
Type C — Design Gap Requiring Named-Authority Review (explicitly flagged by its own author as needing Head of Specs Team review before being unilaterally codified)

**Recurrence:** New — first cycle since `v8.5` where the ungated/ready backlog pool (61 items, ~41.0 days) exceeded the sprint capacity band by a wide margin rather than being fully consumable or falling short of it.

**What happened:**
`release_planning_prompt.md` §1.4 has no canonical method for selecting *which* ungated items to include when the ready pool exceeds capacity by a wide margin. This session adopted an ad hoc category-balanced, oldest-first round-robin (documented in `run_manifest.md`) — reasonable, but not backed by any documented rule, so a future cycle facing the same situation could legitimately reach a materially different scope via a different selection method with no way to tell which is "correct."

**Where in the routine:**
`release_planning_prompt.md` §1.4 (or a new §1.4c).

**Root cause:**
§1.4a's Perennial-Return Check governs *gate-conditional* items returning cycle-over-cycle, but has no sibling rule for the over-capacity-selection case.

**Process patch:**
→ Deferred (not applied this run) — Release Planning's own `lessons_learnt.md` explicitly frames this as needing Head of Specs Team review of the exact selection-method wording before being unilaterally codified by a single session's ad hoc choice, distinct from Friction Items 1–2 above (whose fixes were unambiguous once read closely). Respecting that explicit deferral rather than overriding it.
  - File: `claude/system/release_planning_prompt.md`
  - Section: §1.4 (new §1.4c)
  - Change required: canonical over-capacity selection method — category-balanced, oldest-first is a reasonable default to codify, per this session's and the general debt-clearance pattern since v8.5.
  - Owner: Head of Specs Team
  - Target: next `release_planning_prompt.md` revision touching §1.4

### Friction Item 4 (Phase 3, deferred — carried from `lessons_learnt_cycle.md`)

**Classification:**
Type C — Design Gap Requiring Named-Authority Review

**Recurrence:** New this cycle.

**What happened:**
`ESC-EXEC-20260910-01` (ST-22/EPIC-05, non-blocking, 72h SLA) remained `Open` roughly 22 hours past its own SLA due-by with no automated reminder or escalation-pressure mechanism firing in the interim. Its `Blocks execution: No` disposition correctly kept it from gating anything (no incorrect gate fired), but nothing in the routine surfaces an SLA breach on a non-blocking escalation to a human before the next session happens to touch it.

**Where in the routine:**
`claude/system/shared_standards.md §16.4` (SLA breach tracking) and/or `execution_prompt.md`'s escalation handling subroutine.

**Root cause:**
SLA state is only reconciled at whatever session happens to touch the escalation next (STEP 6's `blocked_sla_breached` flag), with no earlier trigger.

**Process patch:**
→ Deferred (not applied this run) — `lessons_learnt_cycle.md`'s own Phase 3 section explicitly frames this as needing Head of Specs Team confirmation of the wording before it lands, since it changes shared cross-engine escalation-handling behaviour, not a single prompt's local logic.
  - File: `claude/system/shared_standards.md` §16.4 and/or `claude/system/execution_prompt.md`
  - Change required: a lighter-weight mid-sprint surfacing rule — any open escalation whose SLA due-by has passed is called out explicitly the next time `run sprint` is invoked for any reason, even when non-blocking.
  - Owner: Head of Specs Team
  - Target: next `execution_prompt.md`/`shared_standards.md §16.4` revision touching escalation SLA tracking

### Friction Item 5 (Phase 4, deferred — carried unresolved from `2026-09-07__release-v9.2`)

**Classification:**
Type D — Minor Process Friction (target condition genuinely not yet met, not overdue)

**Recurrence:** Carried forward unresolved — not a new finding.

**What happened:**
A stale forward-looking caveat sentence in `2026-09-07__release-v9.2`'s own `qa_evidence_EPIC-02.md`/`qa_evidence_EPIC-03.md` (target: "next touch of either file", owner Director of Quality) remains unstruck — neither file was touched during `2026-09-09__release-v9.3`, so the target condition has simply not yet occurred.

**Process patch:**
→ Still deferred, unchanged. Owner: Director of Quality. Target: next touch of either file.

---

## Recurrence Escalations

None raised this cycle. `lessons_learnt_cycle.md`'s own Phase 3/Phase 4 sections report 0 active recurrence escalations — the 3 friction items there (1 Phase 3, 2 Phase 4) are first occurrences per the formal §3.7 check, and no carried-forward deferred patch from `2026-09-07__release-v9.2` was found still open at the start of this cycle (all 7 were resolved same-day at that closure).

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | §5.3 | Pre-merge sign-off format lint added — validate `Signed off by:` line before EPIC's PR opens (`LL-v9.3-P4-01`) | 3.74 → 3.75 | Yes — `prompt_change_log.md` 2026-09-14 |
| `claude/system/delivery_verification_prompt.md` | §2.1 | New `Pass, escalation open` Result value with defined semantics, distinct from `Pass_with_deviation` (`LL-v9.3-P4-02`) | 3.10 → 3.11 | Yes — `prompt_change_log.md` 2026-09-14 |
| `claude/system/templates/qa_evidence_template.md` | Result column guidance | Companion update matching the new Result value | 1.13 → 1.14 | Yes — `prompt_change_log.md` 2026-09-14 |
| `claude/system/OPERATIONAL_GUIDE.md` | §8, §9, §14 (×3), document header, Change Log | Source-prompt headers and governance table synced for the 3 bumps above | 4.184 → 4.185 | Yes — `prompt_change_log.md` 2026-09-14 |
| `docs/specs/Specs_Index.md` | §43 (new) | Test Coverage Gaps — v9.3 section added (0 new gaps); endpoint coverage drift check cross-referenced (1 genuine gap, `BLG-OPS-156` filed); full-document TSG sweep explicitly reported (0 Open entries, 0 resolved) per `LL-v9.0-Closure-01`'s mandatory-reporting requirement | n/a (Changelog-table document, no header version field) | Not applicable |

---

## New files created this run

None — this closure's document changes were all updates to existing artefacts (changelog, roadmap, backlog, velocity metrics, Specs Index, scope/decisions supersession, governance prompts), plus one new backlog item (`BLG-OPS-156`).

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target | Carried since |
|------|---------|----------------|-------|--------|---------------|
| `claude/system/release_planning_prompt.md` | §1.4 (new §1.4c) | Canonical over-capacity ready-pool selection method (category-balanced, oldest-first) | Head of Specs Team | Next `release_planning_prompt.md` revision touching §1.4 | v9.3 (new) |
| `claude/system/shared_standards.md §16.4` / `claude/system/execution_prompt.md` | Escalation SLA tracking | Mid-sprint surfacing of open, SLA-breached, non-blocking escalations at any `run sprint` invocation | Head of Specs Team | Next revision touching escalation SLA tracking | v9.3 (new) |
| `claude/cycles/2026-09-07__release-v9.2/qa_evidence_EPIC-02.md`, `qa_evidence_EPIC-03.md` | Sign-Off Block comments | Strike/update stale STEP-4-merge-gate-outstanding caveat sentence (both PRs long since merged) | Director of Quality | Next touch of either file | v9.2 |

3 deferred patches remain open from this closure — 2 new (this cycle's own Release Planning and Phase 3 friction items, both explicitly requiring Head of Specs Team design/wording confirmation before landing), 1 carried unchanged from `2026-09-07__release-v9.2` (target condition not yet met, not overdue).

---

## Escalations

None raised by this closure. `ESC-EXEC-20260910-01` (ST-22/EPIC-05) is carried forward past sprint close per `sprint_close.md`/`verification_report.md` — non-blocking, owned by AI Compliance & Governance Officer, SLA already breached before this closure ran. No new escalation action taken by Post-Ship Closure itself (outside its write scope beyond recording it — see closure record §6).

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `2026-09-07__release-v9.2`'s closure resolved all 7 of its outstanding actions same-day; none recurred this cycle. The closure-to-closure Carry-Forward mechanism continues to function as intended across a full cycle boundary. | No action needed; continue relying on the mechanism. | Post-Ship Closure |
| 2 | This is the second consecutive cycle (`v9.2` then `v9.3`) where a Delivery Verification Phase 4 friction item is "an ad hoc, non-enumerated Result label" — `Pass_with_deviation` (v9.2) and now `Pass, escalation open` (v9.3). Both were fixed same-cycle, but the pattern of evidence authors inventing new free-text labels for situations the enum doesn't yet cover may recur a third time with a fourth shape. | Worth a standing Head of Specs Team watch-item: if a third distinct ad hoc Result label surfaces, consider whether §2.1's enum needs a more general open-ended "Pass, see Comments" catch-all rather than continuing to enumerate every new shape one at a time. | Delivery Verification / Post-Ship Closure |
| 3 | 2 of this cycle's own friction-item fixes (Release Planning's over-capacity selection method, Phase 3's SLA-surfacing rule) were explicitly deferred by their own originating records as needing Head of Specs Team design confirmation, rather than applied same-cycle per the STEP 8 default. Both dispositions were respected here rather than overridden. | Confirms the same-cycle application pattern (`LL-v9.2-Closure-01`) correctly distinguishes "unambiguous fix, apply now" from "genuine design input needed, defer" rather than applying everything indiscriminately. | Post-Ship Closure |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-09-09__release-v9.3",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-09-14T10:30:00Z",
  "friction_item_count": 5,
  "action_now_count": 2,
  "deferred_count": 3,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Active"
}
```
