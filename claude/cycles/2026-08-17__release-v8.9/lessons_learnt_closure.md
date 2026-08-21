Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-21
Cycle: 2026-08-17__release-v8.9

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Ship v8.9: eliminate the two live risk-management stop-price defects on open positions (breakeven-floor ratchet, currency-basis mismatch) and deliver the sector-aware position sizing, pre-commit risk simulator, AI post-trade debrief, and in-app backtesting foundations of the Trade Intelligence Expansion — while clearing this cycle's reliability, QA, ops, and governance debt.
Run: 2026-08-17__release-v8.9
Reviewed by: PMO Lead
Date filed: 2026-08-21
Prior cycle checked: 2026-08-14__release-v8.8 (`lessons_learnt_closure.md`)

---

## What worked well

- The backlog-slice-to-story mapping in `stage4_backlog_slice.md` (`Source: BLG-xx` on every `ST-xx`) made STEP 3 Backlog Reconciliation unambiguous — all 22 backlog-slice items plus the gate story traced cleanly to exactly one source backlog entry each, so 21 of 22 could be marked ✅ COMPLETE with full confidence and only one (`BLG-GOV-264`) needed special handling.
- STEP 0's parallel reads of `verification_report.md`, `execution_state.json`, and `sprint_close.md` produced a single, internally consistent picture of the cycle (23/23 stories done, one open P3 deviation, one open non-blocking escalation) with no contradictions across the three sealed sources — closure required no clarifying back-and-forth with any role.
- `docs/ops/api_performance_baseline.md`'s narrative-plus-sign-off convention for `DEV-EPIC03-ST09-01`, while not literally matching the tabular Known Deviation Standard format used in spec files, already contained every substantive fact STEP 5 needed (root cause, priority context, owner, backlog reference) — closing the field-presence gap required additive labelling, not new investigation.

---

## Friction Log

### Friction Item 1

**Classification:**
Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** No — first time this specific gap (header vs. table content divergence) was surfaced as friction, though the underlying omission itself occurred silently across two prior closures.

**What happened:**
`claude/cycles/velocity_metrics.md`'s `**Last Updated:**` header, at the start of this run, still read "2026-08-12 (post-ship closure 2026-08-11__release-v8.6)" as its most recent entry, despite the Velocity History table already containing rows for `v8.7` and `v8.8` — meaning the header field was not bumped at either of the two most recent post-ship closures even though STEP 6 was presumably run and a row was appended each time. This was only caught because this run's own STEP 6 write required reading the existing header chain before appending a new entry.

**Where in the routine:**
STEP 6 — Operational Documents Reconciliation (`velocity_metrics.md` append)

**Root cause:**
process gap — no step in `post_ship_closure.md` verifies that a target document's own header (specifically the `**Last Updated:**` chain) was actually advanced at the previous invocation before trusting it as the base for this run's new chained entry.

**Blast radius analysis:**
- What would have propagated: an inaccurate "Last Updated" audit trail on `velocity_metrics.md` (Class 3 Operational Record), understating how current the document actually is, and risking a fabricated "prior — 2026-08-1X (post-ship closure vX.Y)" entry if this run had blindly chained onto the stale header without checking.
- When it would have surfaced: never automatically — only a manual header-vs-table cross-check (as performed this run) would catch it.
- Recovery cost if uncaught: low (single-file header fix; the table rows themselves were accurate and not affected).

**Process patch:**
→ Deferred patch (cannot apply this run):
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 6 (Operational Documents Reconciliation)
  - Change required: Add an explicit self-consistency check for `velocity_metrics.md` (and other Class 3 operational records this STEP appends to) mirroring `shared_standards.md §9.1`'s existing check for prompt files — before appending a new row/entry, confirm the document's own header was actually advanced at the document's most recent prior append; if not, correct the header honestly (do not fabricate the missing intermediate entries) as part of this run's own write.
  - Owner: Head of Specs Team
  - Target: next `post_ship_closure.md` revision touching STEP 6

---

### Friction Item 2

**Classification:**
Type B — Semantic Mismatch: The same concept was named or interpreted differently across documents or roles

**Recurrence:** No — first time STEP 5 examined field-level format for an ops-doc-hosted deviation rather than a spec-doc-hosted one.

**What happened:**
`DEV-EPIC03-ST09-01`'s entry in `docs/ops/api_performance_baseline.md` §36.5 satisfied every substantive requirement of `§3 Known Deviation Standard` (description, canonical requirement, priority, target resolution, owner, backlog reference) but expressed them as narrative prose and a sign-off block rather than the explicit labelled-field format used by spec files like `positions.md`/`trade_plan.md`'s `## Known Deviations` tables. A literal field-presence check would have flagged this as non-compliant despite the substance being genuinely present.

**Where in the routine:**
STEP 5 — Canonical Spec Deviation Compliance Check

**Root cause:**
template omission — no distinct Known Deviation format guidance exists for Class 3 operational-record-hosted deviations (which use narrative/sign-off conventions) versus Class 1/4 spec-hosted deviations (which use the labelled table format).

**Blast radius analysis:**
- What would have propagated: a future deviation compliance check finding the same substance-present-but-label-absent pattern would have to redo this same judgment call from scratch each time, with no documented precedent to point to.
- When it would have surfaced: the next post-ship closure with an ops-doc-hosted deviation.
- Recovery cost if uncaught: low (this run applied a direct, additive fix).

**Process patch:**
→ Immediate patch applied this run:
  - File: `docs/ops/api_performance_baseline.md`
  - Section: §36.5
  - Change: Added an explicit labelled-fields block (Description, Canonical requirement, Priority, Target resolution release, Owner, Backlog reference) for `DEV-EPIC03-ST09-01` immediately after the interim-measurement table, closing the field-presence gap without altering the existing narrative/sign-off content.
  - Version: 2.30 → 2.31 (Document History row added in the same edit)
  - Confirmed by: Post-Ship Closure Engine (agent-mediated, Infrastructure & Operations Owner role — §5.3, per this document's own Owner field)
  - Prompt change log entry: Not applicable — this is a Class 3 operational record with its own Document History table (updated in the same edit), not a governance prompt or `OPERATIONAL_GUIDE.md`; CLAUDE.md §6 and `prompt_change_log.md` do not apply.

---

### Friction Item 3

**Classification:**
Type C — Dependency Stall: A gate or pre-condition was invisible, ambiguous, or not enforced

**Recurrence:** No — first cycle where a split-achievability story's own backlog item interacted with STEP 3.1's completion-marking instruction.

**What happened:**
`post_ship_closure.md` STEP 3.1 instructs: "For every ST item in `execution_state.json` with status `done` or `merged`: ... Mark it ✅ COMPLETE." Applied literally, this would have marked `BLG-GOV-264` (ST-21's source item) as ✅ COMPLETE, since ST-21 itself reached `status: done`. But ST-21's own `execution_state.json` notes and `sprint_close.md`/`verification_report.md §5(a)` all record that ST-21 was only half-achieved — the prompt-wiring action landed, but the file-creation action (`claude/roadmap/displacement_debt_register.md`) remains genuinely outstanding, architecturally outside Sprint Execution's write scope, and carried forward via an open, non-blocking escalation (`ESC-EXEC-20260818-02`). Marking `BLG-GOV-264` COMPLETE would have been factually wrong and — since STEP 12 (`groom backlog`) runs later in this same routine — would likely have caused the still-open item to be archived this same session, silently dropping its escalation cross-reference from active tracking.

**Where in the routine:**
STEP 3.1 — Mark shipped items complete

**Root cause:**
process gap — STEP 3.1 has no carve-out for split-achievability/partially-resolved stories, unlike STEP 3.4 (stale parked items) or STEP 4.2's Note on Accepted Risk records, both of which do have explicit non-default handling instructions.

**Blast radius analysis:**
- What would have propagated: `BLG-GOV-264` marked falsely COMPLETE and archived by this same run's own STEP 12, dropping the still-open Displacement Debt Register file-creation obligation from active backlog visibility.
- When it would have surfaced: not until the next `run roadmap`/`manage roadmap` invocation looked for the register file and found neither an active nor a traceably-complete backlog item explaining its absence.
- Recovery cost if uncaught: medium (would require un-archiving the item, re-establishing its escalation cross-reference, and explaining the false-complete state to whoever next reviewed it).

**Process patch:**
→ Deferred patch (cannot apply this run):
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 3.1 (Mark shipped items complete)
  - Change required: Add an explicit carve-out: before marking a backlog item ✅ COMPLETE, check whether the corresponding ST item's own `execution_state.json` notes record a partial/split-achievability outcome, or whether `sprint_close.md`/`verification_report.md` carries an open, carried-forward escalation referencing that backlog item's ID. If so, leave the backlog item's status as-is (do not mark COMPLETE) and instead record the split-achievability disposition under the closure record's §6 Outstanding Actions — consistent with how this run handled `BLG-GOV-264`.
  - Owner: Head of Specs Team
  - Target: next `post_ship_closure.md` revision touching STEP 3.1

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| CI-green restatement requirement (`qa_evidence_template.md`/`execution_prompt.md §5.3`) should be clarified as per-fix, not per-EPIC | `2026-08-12__release-v8.7` Phase 4 | Deferred — Head of Specs Team, next revision touching either file. Carried 2 consecutive cycles (v8.7→v8.8→v8.9) with no `prompt_change_log.md` entry. | Head of Specs Team — formally raised this run as `ESC-CLOSE-20260821-01` (SLA 2026-08-24) |
| Canonical "Sandbox Access Constraint" disclosure block for `shared_standards.md` | `2026-08-12__release-v8.7` Phase 4 | Deferred — Head of Specs Team, next `shared_standards.md` revision. Carried 2 consecutive cycles with no `prompt_change_log.md` entry and no such block found. | Head of Specs Team — formally raised this run as `ESC-CLOSE-20260821-02` (SLA 2026-08-24) |

These two items were already identified as recurrence escalations in this cycle's `lessons_learnt_cycle.md §Phase 4` (Delivery Verification, 2026-08-21); this closure run's own action is formalising them as tracked escalations (`closure_escalations.md`, `.claude_current_state.json.open_escalations`) rather than letting them sit as prose-only observations with no SLA or state-pointer visibility.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `docs/ops/api_performance_baseline.md` | §36.5 | Added explicit labelled Known Deviation fields for `DEV-EPIC03-ST09-01` (Description, Canonical requirement, Priority, Target resolution release, Owner, Backlog reference) | 2.30 → 2.31 | Not applicable (Class 3 operational record; own Document History table updated instead) |

---

## New files created this run

- `claude/cycles/2026-08-17__release-v8.9/closure_escalations.md` — created to formally raise the two §6.4 recurrence escalations (CI-green restatement clarification, Sandbox Access Constraint block) identified in this cycle's `lessons_learnt_cycle.md §Phase 4`, per `shared_standards.md §4`'s escalation record format, with the mandatory `.claude_current_state.json.open_escalations` state-pointer sync applied in the same write.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | STEP 5.1 (Acceptance Summary) or STEP -1.4 (Backlog Slice Integrity) | Add an item-count reconciliation check comparing `sprint_backlog.md`'s full declared story count (including gated/Sprint-2 sections) against the count of story entries actually present in `execution_state.json`; halt or flag Sprint Close if they don't match | Head of Specs Team | Next `execution_prompt.md` revision |
| `claude/system/execution_state_schema.json` / `claude/system/execution_prompt.md §3.2.B` | Multi-sprint EPIC tracking | Document a convention for tracking an additional PR against an EPIC whose original PR has already merged (generalise this cycle's ad hoc `epics.EPIC-02.sprint2` sub-object into a named schema field, or mandate an EPIC-suffix convention instead) | Head of Specs Team | Next revision touching multi-sprint EPIC tracking |
| `claude/system/execution_prompt.md` | STEP 8 / merge-gate sync | Structural fix for mid-session `merge_gate`/`pr_status` staleness between individual PR merges (carried from v8.7→v8.8→v8.9, 2 cycles so far — not yet at the 2-cycle-without-application escalation threshold since the specific mid-session mechanism did not recur this cycle) | Head of Specs Team | Next `execution_prompt.md` revision |
| `claude/system/execution_prompt.md` | STEP 5 (Sprint Close) | Require an open/carried-forward escalation's source backlog item to carry a live cycle cross-reference before Sprint Close seals, rather than leaving it for Delivery Verification STEP 4.1 to catch | Head of Specs Team | Next `execution_prompt.md` revision touching STEP 5 |
| `claude/system/execution_prompt.md` | `test_scenarios` field population (STEP 0 step 6) | Explicitly prohibit a descriptive string in place of `[]` (carried from v8.8, 1 cycle so far — not yet at the 2-cycle threshold) | Head of Specs Team | Next `execution_prompt.md` revision touching `test_scenarios` |
| `claude/system/backlog_management_prompt.md` | Item-authoring template / health check | Require `Effort`/`Provisional-Target` fields for mid-sprint out-of-scope backlog filings, or add a `groom backlog` completeness check (carried from v8.8, 1 cycle so far — not yet at the 2-cycle threshold; confirmed via `prompt_change_log.md` search that no entry has applied this) | Head of Specs Team | Next `backlog_management_prompt.md` revision |
| `claude/system/post_ship_closure.md` | STEP 6 (Operational Documents Reconciliation) | Self-consistency check for `velocity_metrics.md`'s (and similar Class 3 records') `Last Updated` header vs. its own table content, mirroring `shared_standards.md §9.1` (this cycle's Friction Item 1) | Head of Specs Team | Next `post_ship_closure.md` revision touching STEP 6 |
| `claude/system/post_ship_closure.md` | STEP 3.1 (Mark shipped items complete) | Carve-out for split-achievability stories before marking a backlog item ✅ COMPLETE (this cycle's Friction Item 3) | Head of Specs Team | Next `post_ship_closure.md` revision touching STEP 3.1 |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| CI-green restatement requirement clarification carried 2 consecutive cycles without a `prompt_change_log.md` entry | Recurrence | Head of Specs Team | Crosses `shared_standards.md §6.4`'s 2-cycle automatic-escalation threshold — see `closure_escalations.md#ESC-CLOSE-20260821-01` |
| Canonical "Sandbox Access Constraint" disclosure block carried 2 consecutive cycles without a `prompt_change_log.md` entry | Recurrence | Head of Specs Team | Crosses `shared_standards.md §6.4`'s 2-cycle automatic-escalation threshold — see `closure_escalations.md#ESC-CLOSE-20260821-02` |

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Two Phase 4-originated deferred patches (CI-green restatement clarification, Sandbox Access Constraint block) crossed the `shared_standards.md §6.4` 2-cycle threshold this run and are now formally tracked as `ESC-CLOSE-20260821-01`/`-02` (SLA 2026-08-24). | The next Roadmap Rebalance and/or Release Planning session should confirm Head of Specs Team has actually dispositioned these before treating them as routine carry-forward again — a 3rd silent re-defer would itself be a process violation of §6.4's own intent. | Roadmap \| Release Planning |
| 2 | `velocity_metrics.md`'s own `Last Updated` header fell out of sync with its table content across 2 consecutive post-ship closures (v8.7, v8.8) before this run caught and honestly disclosed the gap rather than fabricating the missing intermediate entries. | Future post-ship closures should verify a target document's header actually reflects its most recent table append before chaining a new entry onto it — not just assume the header is current. | Post-Ship Closure |
| 3 | `post_ship_closure.md` STEP 3.1's literal "mark ST-done items' backlog entry COMPLETE" instruction has no carve-out for split-achievability stories; this run improvised one for `BLG-GOV-264` (leave open, note in closure record §6) rather than following the letter of STEP 3.1. | Worth formalising before the next cycle produces a similar case, so future closure runs don't have to re-derive the same judgment call from scratch. | Post-Ship Closure |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-08-17__release-v8.9",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-08-21T00:00:00Z",
  "friction_item_count": 3,
  "action_now_count": 1,
  "deferred_count": 8,
  "escalation_count": 2,
  "overdue_patches": 0,
  "status": "Active"
}
```
