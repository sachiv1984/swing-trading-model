Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-03
Cycle: 2026-08-21__release-v9.0

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Ship v9.0: close out the correctness/follow-through items surfaced directly by v8.9's own PR-review process (nightly-backtest rebalance-date bug, breakeven-floor stop audit, root logging config), consolidate the ported backtest algorithm into one canonical `strategy_engine.py`, close the What-If Sizing Preview FX-rate gap, and harden operational resilience (deploy-path/staging safeguards) and QA/cost-capacity hygiene coverage across the full 27-item backlog slice.
Run: 2026-08-21__release-v9.0
Reviewed by: PMO Lead
Date filed: 2026-09-03
Prior cycle checked: 2026-08-17__release-v8.9 (`lessons_learnt_closure.md`)

---

## What worked well

- STEP 0's parallel reads of `verification_report.md`, `execution_state.json`, and `sprint_close.md` again produced a single, internally consistent picture of the cycle (27/27 stories done, 0 deviations filed this sprint, 0 delegations/escalations outstanding) with no contradictions across the three sealed sources.
- The Release Slice table in `backlog.md` (ST → BLG source mapping, `RP:v9.0:...` marker) made STEP 3 Backlog Reconciliation fully mechanical — all 27 items traced to exactly one source backlog entry each, all 27 marked ✅ COMPLETE with a consistent resolution-note format, no special-case handling needed this cycle (contrast with v8.9's one split-achievability case, `BLG-GOV-264`).
- The STEP 5.1 cross-cycle deviation consolidation review (cadence-triggered, 4th run) caught a real, live instance of the resolution-status-drift pattern (`DEV-EPIC03-ST09-01`) on its first pass — the pattern is now well-understood enough that the review's own "Method" section reliably surfaces it without ad hoc investigation.
- `post_ship_closure.md` v2.30's velocity_metrics.md header self-consistency check (added at the prior cycle's lifecycle audit, `AUD-2026-08-21-007`, directly from this cycle's own Friction Item 1) worked exactly as designed — the header was confirmed self-consistent with the table before this cycle's row was appended, with zero drift found.

---

## Friction Log

### Friction Item 1

**Classification:**
Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** Yes — 3rd confirmed instance of the same resolution-status-drift pattern across 4 consolidation review runs (`DEV-ST14-01` run 1; none run 2; `DEV-v8.6-ST02-01` run 3; `DEV-EPIC03-ST09-01` this run).

**What happened:**
`DEV-EPIC03-ST09-01` was genuinely resolved this cycle (ST-02, `BLG-BE-107`, real Render-log confirmation obtained 2026-09-03) — `api_performance_baseline.md §36.7` records the resolution in full narrative form. Its own labelled `Known Deviation fields` block at §36.5, however, was not updated in the same commit that resolved it — it still read "Superseded once `BLG-BE-107` lands ... no fixed release targeted yet" at the start of this closure run. Found and corrected during STEP 5.1 (see `docs/governance/deviation_consolidation_review_2026-09-03.md` Finding 1).

**Where in the routine:**
STEP 5.1 — Cross-Cycle Deviation Consolidation Review (would also have been caught by STEP 5 if this deviation had been newly filed this sprint, but it was filed at v8.9 and resolved at v9.0, outside STEP 5's "filed this sprint" scope).

**Root cause:**
Same root cause identified at runs 1 and 3: no step in the normal `plan release → sprint execution` flow re-visits a *pre-existing* deviation's own labelled fields when a *later* story (in a *different* cycle than the one that filed it) closes its root cause. The resolving story's own evidence (§36.7 narrative) gets written; the deviation's own tracking fields do not.

**Blast radius analysis:**
- What would have propagated: a reader consulting `DEV-EPIC03-ST09-01`'s own labelled fields (rather than reading the full §36 narrative) would see a stale "not yet resolved" status for a deviation that has, in fact, closed.
- When it would have surfaced: next `run audit` or next consolidation review (3 cycles away) — the same delay pattern as runs 1 and 3.
- Recovery cost if uncaught: low (single-field correction, no data loss) — but the *pattern itself* not being structurally fixed is the recurring cost.

**Process patch:**
→ Deferred patch (cannot apply this run — outside this engine's judgement to design the exact mechanism):
  - File: `claude/system/execution_prompt.md` (most likely home — STEP 3.1.A's existing deviation-filing checklist)
  - Change required: require any story/engine action that closes a *pre-existing* deviation's root cause to also update that deviation's own labelled Known Deviation fields in the same commit — mirroring the existing `deviations_filed` atomic-write discipline for *filing* a deviation, but for *closing* one.
  - Owner: Head of Specs Team
  - Target: **escalated this run** — 3rd instance across 4 runs with zero backlog item filed despite 3 prior soft recommendations (see `deviation_consolidation_review_2026-09-03.md` Recommendation 1). Recorded as an escalated Outstanding Action in `closure_record.md §6`, requesting the `BLG-GOV-*` tracking item be filed before the *next* Post-Ship Closure review.

---

### Friction Item 2

**Classification:**
Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** No — first time this specific entry (`TSG-v40-01`) was found stale-but-actually-resolved; structurally the same class of gap as v8.6's own Friction Log finding (2 stale TSG entries, §39).

**What happened:**
`Specs_Index.md` §23.1's `TSG-v40-01` (Arc5ComplianceSection staging verification, `BLG-QA-28`) was still marked "Partially resolved" at the start of this run, despite `BLG-QA-28` having shipped and been retired to `backlog_archive.md` on 2026-05-29 (v4.3) — over 3 months and 16+ cycles earlier. No closure between v4.3 and this one had re-run the full-document TSG sweep that would have caught it (the per-cycle §7.3 note only checks entries the closure engine already knows to look at; the full-scan convention, `post_ship_closure.md` v2.26, was applied inconsistently — it caught 2 stale entries at v8.6 but was evidently not re-run, or not run as a genuine full sweep, at v8.7/v8.8/v8.9, none of which produced a numbered TSG section despite the convention implying one should be added each cycle).

**Where in the routine:**
STEP 7.3 — TSG backlog reconciliation (full-document sweep)

**Root cause:**
Same class as v8.6's Friction Item — the full-document sweep is conducted at the executing engine's discretion each cycle rather than being a structurally-enforced step, so 3 consecutive cycles (v8.7, v8.8, v8.9) apparently skipped it or applied it only partially (no new `## NN. Test Coverage Gaps` section was added for any of those 3 releases, breaking the one-section-per-cycle pattern established through v8.6).

**Blast radius analysis:**
- What would have propagated: continued reliance on a stale "Partially resolved" status for a fully-shipped item, and — more importantly — a 3-cycle gap in the TSG register's own section sequence (v8.6 → v9.0, skipping v8.7/v8.8/v8.9) that a future reader might mistake for "no test coverage gaps existed in those 3 cycles" rather than "the section wasn't added."
- When it would have surfaced: never automatically.
- Recovery cost if uncaught: low for this specific entry (single-field correction); the 3-cycle section-numbering gap itself is not retroactively fixable without re-deriving those 3 cycles' actual §6 findings from their own verification reports — out of scope for this closure.

**Process patch:**
→ Deferred patch (cannot apply this run):
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 7 / STEP 7.3
  - Change required: make the full-document TSG sweep a mandatory, checkable sub-step (not a "when convenient" convention) — e.g. require the closure record to explicitly state "STEP 7.3 full-document sweep: N Open entries checked, M resolved" every cycle, so a skipped sweep is visible as a gap in the closure record itself rather than only discoverable by a future sweep noticing a stale entry.
  - Owner: Head of Specs Team
  - Target: next `post_ship_closure.md` revision touching STEP 7

---

## Recurrence Escalations

None raised this cycle. `lessons_learnt_cycle.md`'s own Phase 3/Phase 4 sections report 0 active recurrence escalations (the 2 formal escalations from the prior cycle, `ESC-CLOSE-20260821-01`/`-02`, were both resolved before this cycle began — see `.claude_current_state.json.open_escalations` = `{}` and commit `23d9fd8c`).

Friction Item 1 above (deviation labelled-field drift) is escalated as an **Outstanding Action** rather than a formal `ESC-CLOSE-*` — it is a request to file a backlog item, not a governance-prompt-edit request subject to the `shared_standards.md §6.4` 2-cycle threshold (which tracks deferred *prompt* patches specifically).

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `docs/ops/api_performance_baseline.md` | §36.5 (Known Deviation fields) | Corrected `DEV-EPIC03-ST09-01`'s `Target resolution release` field to state its actual resolution (v9.0, ST-02, `BLG-BE-107`) instead of the stale "not yet resolved" text | 2.31 → 2.32 | Not applicable (Class 3 operational record; own Document History table updated instead) |
| `docs/specs/Specs_Index.md` | §23.1 (`TSG-v40-01`) | Marked ✅ RESOLVED — `BLG-QA-28`'s remaining staging-verification ACs confirmed shipped v4.3 | n/a (no version field on this doc) | Not applicable |
| `docs/specs/Specs_Index.md` | §40 (new) | Added `Test Coverage Gaps — v9.0` section (2 `not_applicable` findings) and full-document TSG sweep record | n/a | Not applicable |

---

## New files created this run

- `docs/governance/deviation_consolidation_review_2026-09-03.md` — 4th cadence-triggered run of the STEP 5.1 cross-cycle `DEV-*` consolidation review (16 records catalogued, 4 new since the 3rd run, 1 resolution-status drift found and corrected).

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target | Carried since |
|------|---------|----------------|-------|--------|---------------|
| `claude/system/execution_prompt.md` | STEP 3.1.A step 10a | Same-step self-verification read-back after the `deviations_filed` write, converting the "do not defer" instruction into a mechanically-checkable gate (this cycle's Phase 3 friction item, `lessons_learnt_cycle.md`) | Head of Specs Team | Next `execution_prompt.md` revision touching STEP 3.1.A | v9.0 (new) |
| `claude/system/execution_prompt.md` | STEP 3 (`test_scenarios` write step) | Completeness check requiring new test files under `tests/` to be reflected in the owning EPIC's `test_scenarios` array in the same write (this cycle's Phase 4 friction item, `lessons_learnt_cycle.md`) | Head of Specs Team | Next `execution_prompt.md` revision touching STEP 3 | v9.0 (new) |
| `claude/cycles/2026-08-21__release-v9.0/qa_evidence_EPIC-01.md` | ST-02 row | Update `Result` from "Returned to backlog" to `Pass` — ST-02 reached final `done` resolution after the evidence log was last touched (this cycle's Phase 4 friction item, `lessons_learnt_cycle.md`); outside post-ship closure's write scope (qa evidence logs are not a STEP 5 permitted path) | Director of Quality | Next touch of `qa_evidence_EPIC-01.md` | v9.0 (new) |
| `claude/system/execution_prompt.md` | Deviation-closure discipline (STEP 3.1.A) | Require a story/engine action that closes a *pre-existing* deviation's root cause to also update that deviation's own labelled fields in the same commit (this run's Friction Item 1 — 3rd confirmed instance across 4 consolidation review runs) | Head of Specs Team | **Escalated** — file as `BLG-GOV-*` before next Post-Ship Closure review | v8.1 (run 1), recurred v8.7 (run 3), recurred v9.0 (run 4) |
| `claude/system/post_ship_closure.md` | STEP 7 / STEP 7.3 | Make the full-document TSG sweep a mandatory, explicitly-reported sub-step rather than a discretionary convention (this run's Friction Item 2 — 3-cycle gap in TSG section numbering, v8.7–v8.9) | Head of Specs Team | Next `post_ship_closure.md` revision touching STEP 7 | v9.0 (new) |
| `claude/system/post_ship_closure.md` | STEP 3.1 (Mark shipped items complete) | Carve-out for split-achievability stories before marking a backlog item ✅ COMPLETE (v8.9's Friction Item 3 — did not recur this cycle, no split-achievability stories in the v9.0 slice, but the prompt gap itself remains unpatched) | Head of Specs Team | Next `post_ship_closure.md` revision touching STEP 3.1 | v8.9 (1 cycle carried, no recurrence this cycle) |

---

## Escalations

None formally raised this cycle (no item crossed the `shared_standards.md §6.4` 2-cycle prompt-patch threshold). Friction Item 1's structural-fix request is tracked as a closure-record Outstanding Action, not a formal `ESC-CLOSE-*`, per the Recurrence Escalations section above.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The resolution-status-drift pattern (a deviation resolved via a later story/cycle doesn't propagate back to its own labelled fields) has now recurred 3 times across 4 consolidation review runs with zero structural fix filed despite 3 soft recommendations. | The next Roadmap Rebalance or Release Planning session should confirm a `BLG-GOV-*` tracking item now exists for this before treating it as routine carry-forward again — a 4th silent re-defer would itself be a process violation of the same kind `shared_standards.md §6.4` exists to catch for prompt patches. | Roadmap \| Release Planning |
| 2 | `Specs_Index.md`'s per-cycle TSG full-document sweep was apparently skipped or only partially applied for 3 consecutive cycles (v8.7, v8.8, v8.9) — no new numbered TSG section was added for any of them, breaking the one-section-per-cycle pattern in place through v8.6. | Future post-ship closures should treat "no new TSG section this cycle" as requiring an explicit "0 new gaps" record (as v8.6 did) rather than silently omitting the section — an omitted section is indistinguishable from a skipped sweep. | Post-Ship Closure |
| 3 | v9.0 shipped with 0 immediate lessons-learnt actions applied and 0 decision-required escalations — all 3 action items from `lessons_learnt_cycle.md` required deferral either because they need Head of Specs Team design input on exact placement/wording, or because the target file (`qa_evidence_EPIC-01.md`) is outside this engine's write scope. | Not itself a problem, but worth tracking: if this pattern (loop learnings identified but never a) unambiguous enough to apply immediately, or b) within any engine's write scope) continues across cycles, the deferred-patch backlog will keep growing with no execution path — worth a dedicated review of whether `execution_prompt.md`'s deferred-patch list needs its own periodic clearance pass, analogous to the deviation consolidation review. | Roadmap \| Release Planning |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt_closure.md",
  "cycle_id": "2026-08-21__release-v9.0",
  "phase": "Post-Ship Closure",
  "filed_utc": "2026-09-03T00:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 3,
  "deferred_count": 6,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Active"
}
```
