Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-15 (initial filing)
Cycle: 2026-09-14__release-v9.4

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Ship v9.4: close all 28 backlog-driven debt items in scope — backend & platform engineering debt (5 items), QA & test-coverage debt (3 items), operations & security debt (4 items), spec/documentation & financial-reporting debt (5 items), governance-process & AI-compliance debt (6 items), and frontend/UX/product debt (5 items).
Run: 2026-09-14__release-v9.4
Reviewed by: PMO Lead
Date filed: 2026-09-15
Prior cycle checked: 2026-09-09__release-v9.3 (`lessons_learnt_closure.md`) — 3 deferred patches remained open: (1) `release_planning_prompt.md` §1.4c over-capacity ready-pool selection method, Head of Specs Team, target "next revision touching §1.4" — re-checked this run, still not applied (this cycle's own release-planning fix landed at §1.3/STEP 4.1, a different section; carried forward again below, now 1 cycle carried, not yet due for escalation); (2) `shared_standards.md §16.4`/`execution_prompt.md` mid-sprint SLA-breach surfacing rule, Head of Specs Team — re-checked, still not applied, carried forward again below, 1 cycle carried; (3) `qa_evidence_EPIC-02.md`/`qa_evidence_EPIC-03.md` (`2026-09-07__release-v9.2`) stale pre-merge caveat sentence — re-checked directly: both files' own headers confirm Director of Quality struck the caveat 2026-09-09, predating `v9.3`'s own closure record that (stale, as of its own filing) still listed it open. Fully resolved — not carried forward.

---

## What worked well

- STEP 0's parallel reads of `verification_report.md`, `execution_state.json`, and `sprint_close.md` again produced a single, internally consistent picture of the cycle (28/28 stories done across 6 EPICs, 0 formal `DEV-*` deviations filed, 1 open non-blocking prior-cycle escalation correctly left `Deferred`) with no contradictions across the three sealed sources.
- The `stage4_backlog_slice.md` ST→BLG source mapping made STEP 3 Backlog Reconciliation for all 28 items fully mechanical via a single scripted pass — every `### BLG-*` heading matched, every COMPLETE marker inserted in one run, 0 not-found.
- STEP 5.1's Cross-Cycle Deviation Consolidation Review (due this cycle, 3rd invocation since the 4th run) found 0 new formally-ID'd `DEV-*` records and 0 resolution-status drift — but its full-text search (beyond the heading-pattern scan) surfaced a genuinely new gap (see Friction Item 6 below), demonstrating the value of not relying on the heading scan alone.
- The Governance File Edit Checklist (CLAUDE.md §6) was applied cleanly across all 3 same-cycle prompt fixes (release_planning_prompt.md, shared_standards.md, qa_evidence_template.md) in a single consolidated `OPERATIONAL_GUIDE.md` bump (v4.188→v4.189) rather than 3 separate bumps — confirmed the header/§14-self-row/Change-Log-top-row 3-way consistency held before and after the edit (governance-drift self-check).

---

## Friction Log

### Friction Item 1 (Release Planning — closed-loop verification, no action needed)

**Classification:**
Type D — Minor Process Friction (confirms an existing fix works; not a new gap)

**Recurrence:** N/A — this is a positive confirmation, not a friction finding.

**What happened:**
`release_planning_prompt.md`'s STEP -1.6 SLA-breach carry-forward hard gate (`AUD-2026-09-14-001`, added at v9.3's own post-ship closure) fired cleanly on its first live trigger — halting the first `plan release --version "v9.4"` invocation on `ESC-EXEC-20260910-01` (~26h past SLA, carried through v9.3's own Delivery Verification and Post-Ship Closure unhalted). Confirms the exact gap the gate was built to close is now closed at the one checkpoint that reliably runs before a new cycle opens.

**Process patch:** None needed.

### Friction Item 2 (Release Planning — applied this run)

**Classification:**
Type A — Process/Prompt Gap (a scan procedure existed but had an incomplete input scope)

**Recurrence:** New this cycle — first cycle this design-gate scan miss was caught.

**What happened:**
`release_planning_prompt.md` §1.3/STEP 4.1's design-gate-triggering scan initially undercounted by one item: `BLG-AI-05`'s own `Acceptance Criteria` text named no UI/test method at all ("documented in a canonical frontend spec"), reading as spec-debt work, while its `Scope` text described shipping a new visible disclosure/badge component. Caught and corrected within the same Release Planning session before publication — no incorrect gate value shipped.

**Where in the routine:**
`release_planning_prompt.md` §1.3/STEP 4.1 (Design Gate Classification).

**Root cause:**
The scan read `Acceptance Criteria` text only; an item's AC framing can read as spec/governance-only even when its `Scope` text describes shipping a visible element.

**Process patch:**
→ Applied this run (STEP 8 same-cycle application pattern, `LL-v9.4-Release-02`): STEP 4.1's classification rule now explicitly instructs scanning each candidate's `Scope` text for UI-shipping verbs/nouns ("apply to," "add to the," "component," "badge," "banner") in addition to `Acceptance Criteria` text, classifying `design_gate_required = true` if found there. `release_planning_prompt.md` v2.50→v2.51.

### Friction Item 3 (Release Planning, deferred — carried from `lessons_learnt.md`)

**Classification:**
Type D — Minor Process Friction (a standing watch-item, not a defect)

**Recurrence:** New — first cycle the ready pool doubled (61→74 items) purely from one idea-intake window's ungated-heavy composition.

**What happened:**
The largest ready pool on record (74 items / ~65.05 days) is a mechanical consequence of `IW-20260914-01` promoting 42 items directly to backlog with no gate conditions. Not itself a process gap, but a widening capacity-vs-ready-pool gap (46 items/~37.5 days unselected this cycle, up from 34/~13.1 at v9.3) that strengthens the case for either raising the capacity ceiling or a secondary P3-tier prioritisation pass.

**Process patch:**
→ Deferred (not applied this run) — flagged for the next rebalance's own backlog-health review, per the originating record's own disposition.
  - File: N/A (rebalance-cycle review item, not a specific prompt section)
  - Change required: assess whether the ready-pool-vs-capacity gap trend warrants a capacity ceiling change or P3 sub-tiering
  - Owner: PMO Lead / Head of Specs Team
  - Target: next scheduled roadmap rebalance

### Friction Item 4 (Phase 3 — applied this run)

**Classification:**
Type A — Process/Prompt Gap (a known-good pattern existed but was not codified as a standard)

**Recurrence:** New this cycle — first occurrence of this specific failure mode.

**What happened:**
`test_ai_output_sampling_service.py`'s module-level `sys.modules.pop("database", None); import database` permanently overwrote the shared stub for the rest of the pytest session, leaking a real Postgres connection attempt into the alphabetically-later `test_alerts_service.py` — invisible locally, surfaced only as a live CI Phase B failure post-push. Root-caused and fixed correctly (isolated-copy + scoped `patch.dict`, the pattern already used by `test_position_audit_log.py`); the same latent pattern was proactively found and filed for a twin case (`test_trade_plan_audit_log.py`, `BLG-QA-178`, not yet fixed).

**Where in the routine:**
`shared_standards.md §18` (Playwright/pytest authoring standard).

**Root cause:**
Nothing in the authoring standard told a story author up front to use the isolated-copy pattern whenever a new test needs to reimport `database` — the hazard was only discoverable after a live CI failure.

**Process patch:**
→ Applied this run (STEP 8 same-cycle application pattern, `LL-v9.4-P3-01`): `shared_standards.md §18` gains a new subsection requiring the isolated-copy pattern for any pytest file reimporting `backend/database.py`, citing `test_position_audit_log.py` as the canonical example. `shared_standards.md` v3.32→v3.33.

### Friction Item 5 (Phase 4 — applied this run)

**Classification:**
Type B — Enumeration Gap (the enumerated value's own definition was clear but incompletely scoped)

**Recurrence:** Related to, but distinct from, `2026-09-09__release-v9.3`'s own Phase 4 friction item (adding the `Pass, escalation open` value) — that fix shipped and works correctly for its own originating case; this is a second-order gap in the same value's definition, not a repeat of the same defect.

**What happened:**
`qa_evidence_EPIC-01.md`'s ST-05 row used the newly-formalised `Pass, escalation open` Result value (v3.11), naming `BLG-OPS-160` — a backlog item, not an open escalation (`ESC-*`) — in its Deviations column. ST-05's own AC was independently fully met; this was an incidental out-of-scope finding, structurally identical to a routine "AC met, secondary finding filed separately" case that other rows this same cycle correctly recorded as plain `Pass`.

**Where in the routine:**
`claude/system/templates/qa_evidence_template.md` (Result column guidance) / `delivery_verification_prompt.md` §2.1.

**Root cause:**
The v3.11 enumeration closed the original label-shape gap but did not add guidance distinguishing "AC met, adjacent open escalation" from "AC met, incidental backlog-item finding filed."

**Process patch:**
→ Applied this run (STEP 8 same-cycle application pattern, `LL-v9.4-P4-01`): `qa_evidence_template.md` gains a disambiguation note restricting `Pass, escalation open` to a named, open `ESC-*` record only. `qa_evidence_template.md` v1.14→v1.15.

### Friction Item 6 (Post-Ship Closure, STEP 5.1 — deferred)

**Classification:**
Type A — Process/Prompt Gap (a documentation standard's required fields were complete, but its discoverability join-key was not)

**Recurrence:** New — first cycle this specific gap (Known Deviation Standard fields complete, but no `DEV-<id>` assigned) was observed.

**What happened:**
The 5th Cross-EPIC Deviation Consolidation Review (`docs/governance/deviation_consolidation_review_2026-09-15.md`) found 2 deviation-shaped entries filed since the 4th run (`BLG-FE-172` at v9.1/v9.2, `BLG-BE-112` +1 unnamed at v9.3) that are fully compliant with `document_lifecycle_guide.md §9`'s required fields but were never assigned a `DEV-<id>` — making them invisible to this review's heading-based scan method. Found only via a full-text grep for their backlog IDs.

**Where in the routine:**
`claude/charter/document_lifecycle_guide.md §9` (Known Deviation Documentation Standard) and/or the consolidation review's own scan method.

**Root cause:**
No rule requires a `DEV-<id>` be assigned at the point a `## Known Deviations` entry is filed — only that its fields be complete.

**Process patch:**
→ Deferred (not applied this run) — recommends a `BLG-GOV-*` filing, not a direct prompt edit; outside this routine's write scope for net-new process-debt items beyond the Phase 4 traceability set.
  - File: `claude/charter/document_lifecycle_guide.md §9` (or a companion check in the deviation consolidation review's own method)
  - Change required: require every `## Known Deviations` entry to carry a `DEV-<id>` from the point of filing, regardless of heading vs. table-row format
  - Owner: Head of Specs Team
  - Target: next `document_lifecycle_guide.md` revision touching §9, or next consolidation review

---

## Recurrence Escalations

None raised this cycle. Two deferred patches carried from `2026-09-09__release-v9.3`'s own closure (`release_planning_prompt.md` §1.4c over-capacity selection; `shared_standards.md §16.4`/`execution_prompt.md` SLA mid-sprint surfacing) remain unapplied but are only at their 1st carry-forward cycle — below the 2-cycle automatic-escalation threshold (`lessons_learnt_prompt.md §3.7`). The consolidation review's own structural-fix recommendation (resolving-commit-must-update-canonical-spec discipline, carried since the 4th run) found no new drift instance this window (Finding 3 of the review), so it is re-flagged as a standing outstanding action rather than escalated with new urgency.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/release_planning_prompt.md` | §1.3/STEP 4.1 | Design-gate scan now also checks `Scope` text for UI-shipping verbs, not `Acceptance Criteria` text alone (`LL-v9.4-Release-02`) | 2.50 → 2.51 | Yes — `prompt_change_log.md` 2026-09-15 |
| `claude/system/shared_standards.md` | §18 | New subsection requiring the isolated-copy `database` stub-isolation pattern for pytest (`LL-v9.4-P3-01`) | 3.32 → 3.33 | Yes — `prompt_change_log.md` 2026-09-15 |
| `claude/system/templates/qa_evidence_template.md` | Result column guidance | Disambiguation note restricting `Pass, escalation open` to a named open `ESC-*` record (`LL-v9.4-P4-01`) | 1.14 → 1.15 | Yes — `prompt_change_log.md` 2026-09-15 |
| `claude/system/OPERATIONAL_GUIDE.md` | §6B, §14 (×3), document header, Change Log | Source-prompt header and governance table synced for the 3 bumps above | 4.188 → 4.189 | Yes — `prompt_change_log.md` 2026-09-15 |
| `docs/specs/Specs_Index.md` | §44 (new) | Test Coverage Gaps — v9.4 section added (0 new gaps); endpoint coverage drift check cross-referenced (0 gaps — new endpoint registered same-commit); full-document TSG sweep explicitly reported (0 Open entries, 0 resolved) per `LL-v9.0-Closure-01`'s mandatory-reporting requirement | n/a (Changelog-table document, no header version field) | Not applicable |
| `docs/governance/deviation_consolidation_review_2026-09-15.md` | New file (5th run) | Cadence-triggered cross-cycle `DEV-*` consolidation review — 16 formal records unchanged, 1 new finding (DEV-ID convention gap) | n/a (new Class 3 record) | Not applicable |

---

## New files created this run

- `docs/governance/deviation_consolidation_review_2026-09-15.md` — 5th cadence-triggered Cross-EPIC Deviation Consolidation Review (STEP 5.1, due this cycle).
- `claude/cycles/2026-09-14__release-v9.4/closure_state.json` — created at STEP 0.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target | Carried since |
|------|---------|----------------|-------|--------|---------------|
| `claude/system/release_planning_prompt.md` | §1.4 (new §1.4c) | Canonical over-capacity ready-pool selection method (category-balanced, oldest-first) | Head of Specs Team | Next `release_planning_prompt.md` revision touching §1.4 | v9.3 (1 cycle carried) |
| `claude/system/shared_standards.md §16.4` / `claude/system/execution_prompt.md` | Escalation SLA tracking | Mid-sprint surfacing of open, SLA-breached, non-blocking escalations at any `run sprint` invocation | Head of Specs Team | Next revision touching escalation SLA tracking | v9.3 (1 cycle carried) |
| `claude/system/release_planning_prompt.md` §1.4 | Over-capacity ready-pool watch-item (Friction Item 3) | Assess capacity ceiling / P3 sub-tiering given widening ready-pool-vs-capacity gap | PMO Lead / Head of Specs Team | Next scheduled roadmap rebalance | v9.4 (new) |
| `claude/charter/document_lifecycle_guide.md §9` | Known Deviation Documentation Standard | Require a `DEV-<id>` on every `## Known Deviations` entry from point of filing (Friction Item 6) | Head of Specs Team | Next `document_lifecycle_guide.md` revision touching §9 | v9.4 (new) |
| Structural fix: resolving-commit-must-update-canonical-spec discipline | Cross-cutting (any engine closing a pre-existing deviation's root cause) | Require the closing commit to also update that deviation's own labeled fields | Head of Specs Team | Before a 4th drift instance can accrue | Carried since the review's 4th run (`2026-09-03__release-v9.1` era), no new instance this window |

---

## Escalations

None raised by this closure. `ESC-EXEC-20260910-01` (ST-22/EPIC-05, prior-cycle) remains `Deferred` per `.claude_current_state.json.deferred_escalations` — correctly not reopened or falsely closed by this cycle's ST-23 (its own AC 4/6 disclosed staging-only, not met).

---

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Both deferred patches carried from `v9.3`'s own closure (release-planning over-capacity selection method, SLA mid-sprint surfacing) remain unapplied at their 1st carry-forward cycle — neither was superseded by this cycle's own, differently-scoped release-planning fix. | Watch for a 2nd carry-forward cycle without a `prompt_change_log.md` entry — that would cross `lessons_learnt_prompt.md §3.7`'s automatic recurrence-escalation threshold. | Release Planning / Post-Ship Closure |
| 2 | The 3rd carried item from `v9.3`'s closure (stale QA-evidence caveat sentence) was found, on direct re-check, to have already been resolved 2026-09-09 — 5 days before `v9.3`'s own closure ran and recorded it as still open. `v9.3`'s closure record's own carry-forward claim was itself stale at the moment it was written. | Confirms `lessons_learnt_prompt.md §3.7`'s "re-verify against current state, not the prior record" rule (`LL-v9.1-Closure-01`) is worth applying even to a closure's *own* same-session carry-forward claims, not only claims inherited from an earlier cycle. | Post-Ship Closure |
| 3 | This is the first cycle a Post-Ship Closure STEP 5.1 finding (DEV-ID convention gap) surfaced from the deviation consolidation review's own full-text-search fallback rather than its primary heading-based scan — the scan method itself cannot detect the class of gap it just found. | Worth a standing watch: if a future review keeps finding new deviation-shaped entries only via full-text search rather than the heading scan, the review's own Method section should be revised to make full-text search-by-backlog-ID a primary step, not a fallback. | Post-Ship Closure |
| 4 | All 3 of this cycle's applied same-cycle fixes (release-planning scan scope, pytest stub-isolation pattern, QA-evidence disambiguation) had concrete, unambiguous recommended wording already spelled out in their own originating friction-item records, despite 2 of the 3 records not explicitly flagging themselves as "ready to apply now." | Confirms the same-cycle application pattern (`v2.32`, carried from `v9.1`) continues to correctly favour applying an unambiguous fix now over deferring it merely because the record's own framing doesn't explicitly invite immediate application. | Post-Ship Closure |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-09-14__release-v9.4",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-09-15T13:45:00Z",
  "friction_item_count": 6,
  "action_now_count": 3,
  "deferred_count": 3,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Active"
}
```
