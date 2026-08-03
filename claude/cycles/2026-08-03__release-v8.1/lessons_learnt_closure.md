Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-03
Cycle: 2026-08-03__release-v8.1

# Lessons Learnt — Post-Ship Closure — v8.1

Feature / Trigger: Ship v8.1's operational-safety, governance-process, QA-debt, spec-debt, and backend-hardening scope — including the cross-EPIC execution-state structural fix and the release's one ready user-facing accessibility fix.
Run: 2026-08-03__release-v8.1
Reviewed by: PMO Lead
Date filed: 2026-08-03
Prior cycle checked: 2026-07-30__release-v8.0

---

## What worked well

- The v2.22-added Endpoint Coverage Drift Check (STEP 6) "script-derived tracking-item handoff" mechanism (AUD-2026-08-03-003) worked as designed on its first live exercise: it correctly detected that `BLG-OPS-13`'s own recorded endpoint list (last updated 2026-05-31) has drifted entirely out of sync with the current 19-endpoint normalised gap, and produced a fresh, copy-paste-ready re-derived list rather than requiring a manual re-diff.
- All three source lessons-learnt records (`lessons_learnt.md`, `lessons_learnt_cycle.md` Phase 3 + Phase 4) arrived with every action item pre-classified with a disposition; closure review confirmed each against current file state rather than performing first-pass triage from raw prose. One item (`execution_prompt.md`'s `completed_items` cross-EPIC reconciliation check, carried forward as "not directly testable" in the Phase 4 record) was confirmed already landed (`LL-v7.10-P4-01`, present at `execution_prompt.md` lines 1009–1010) by direct grep rather than re-deferred on faith.
- The one unambiguous, well-specified Phase 4 friction item (STEP -1.3A PR-recovery write target, surfaced proactively by EPIC-07's own agent-mediated reviewer before it could cause a failure) was applied immediately within this routine's write scope, consistent with the non-deferrable immediate-action rule.

---

## Friction Log

### Friction Item 1

**Classification:** Type C — Dependency Stall (a precondition was ambiguous, not enforced)

**Recurrence:** No — first cycle `post_ship_closure.md` STEP 5.1 (Cross-Cycle Deviation Consolidation Review) has executed since being added at v2.23 this same cycle.

**What happened:** STEP 5.1's cadence is tracked via `last_deviation_consolidation_review_utc` / `deviation_consolidation_review_cycle_count` in `.claude_current_state.json`, but both fields were still `null` at this closure's STEP 0 read — the review itself was produced during sprint execution (EPIC-04/ST-12, per the STEP 5.1 text's own "(first run, ST-12)" note) rather than by this closure step, and no step anywhere writes the cadence-tracking fields. STEP 5.1's text describes *when* to run the review but not *who* initializes or advances the two state fields that govern its own cadence.

**Where in the routine:** STEP 5.1 — Cross-Cycle Deviation Consolidation Review (cadence check).

**Root cause:** Template omission — STEP 5.1 was added this cycle (v2.23) already assuming a prior baseline for its own cadence fields that does not exist on a first run, and did not specify a write step for them.

**Blast radius analysis:**
- What would have propagated: without an explicit initialization, the next post-ship closure's modulo-3 cadence check would have compared against `null` indefinitely, silently never firing the "due" condition.
- When it would have surfaced: 2–3 cycles from now, as a missing/never-triggered recurring review with no error to flag it.
- Recovery cost if uncaught: low — a single state write, but easy to miss precisely because nothing fails loudly.

**Process patch:**
→ Deferred patch (cannot apply this run — see rationale below):
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 5.1
  - Change required: add an explicit instruction to write/advance `last_deviation_consolidation_review_utc` and `deviation_consolidation_review_cycle_count` in `.claude_current_state.json` whenever the review runs (first-run initialization, or increment on skip / reset on run).
  - Owner: Head of Specs Team
  - Target: next `post_ship_closure.md` revision cycle

This run's own closure resolves the immediate gap operationally (state fields initialized directly at STEP 10, recorded below) without waiting for the prompt patch, since the fields already exist in the schema and only need a value.

---

## Recurrence Escalations

None. Friction Item 1 above is a first-occurrence template gap in a step added this same cycle, not a recurrence of a prior open action.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/delivery_verification_prompt.md` | STEP -1.3A — PR Number Recovery | Recovered `pr_number` write redirected from the disposable/regenerate-on-read `execution_state.json` to the owning `execution_state/EPIC-xx.json` file (per `shared_standards.md §12.1`), with regeneration via `generate_execution_summary.py`; legacy direct-write fallback retained for pre-per-EPIC-mechanism cycles (LL-v8.1-P4-01). | v3.6→v3.7 | Yes |

This change additionally required an `OPERATIONAL_GUIDE.md` §14 governance-table update (v4.131→v4.132, also correcting a pre-existing 4-version self-row drift from 4.127) and its dedicated changelog file (`changelogs/delivery_verification_changelog.md`), per CLAUDE.md §6.

---

## New files created this run

- `claude/cycles/2026-08-03__release-v8.1/closure_state.json`
- `claude/cycles/2026-08-03__release-v8.1/lessons_learnt_closure.md` (this file)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/post_ship_closure.md` | STEP 5.1 | Add explicit cadence-field write instruction (see Friction Item 1). | Head of Specs Team | Next `post_ship_closure.md` revision cycle |
| `claude/backlog/backlog.md` (`BLG-OPS-13` entry body) | Endpoint list | Reconcile against the current live gap — 19 endpoints in `openapi.yaml` absent from `api_performance_baseline.md` (normalised): `GET /analytics/market-correlation`, `GET /analytics/metrics`, `GET /analytics/tag-performance`, `GET /portfolio/pre-entry-validation`, `GET /positions/analyze`, `GET /positions/grace-period-alerts`, `GET /positions/tags`, `GET /positions/{id}`, `GET /positions/{id}/stop-trail`, `PATCH /notifications/preferences`, `PATCH /watchlist/{id}`, `POST /ai/check-daily-cost`, `POST /alerts/rules`, `POST /positions/nightly-stop-update`, `POST /positions/risk-off-alerts`, `POST /positions/{id}/refresh-state`, `POST /settings`, `POST /signals/rebalance-exit`, `POST /test/endpoints`. `BLG-OPS-13`'s own list (last updated 2026-05-31) names an entirely different, now-stale set of endpoints. Outside Post-Ship Closure's backlog write scope (mark-shipped-complete / add-missing-Phase-4-items only — not existing-item body edits). | Infrastructure & Operations Owner | Next `groom backlog` or endpoint performance baseline review |
| Release Planning scope-selection guidance (`release_planning_prompt.md`) | Ungated-pool scan procedure | Recurrence Escalation 1 (from `lessons_learnt.md` this cycle): 2nd consecutive Release Planning cycle with a self-caught ungated-candidate scan miss (v8.0: gate-field-name variant; v8.1: scan line-window bounds), both from the same "no canonical scan procedure" root cause. File a `BLG-GOV-*` item: canonical, scripted (full-block) gate-detection procedure covering all observed gate-field variants (`Gate criteria`, `Gate`, `Gate date`). Outside Post-Ship Closure's write scope (new-item filing is not a Phase 4 addition). | PMO Lead / Head of Specs Team | Next `groom backlog` or `run roadmap` session |
| `CLAUDE.md` §8 (Cross-EPIC Merge Conflict Resolution) | Named check | Phase 3 friction item this cycle: add an explicit "identical-text masks differing semantics" check — two branches independently bumping a shared prompt file to the same literal version number for different changes is not flagged by git as conflicting. Caught manually this cycle (EPIC-03/EPIC-04 `sprint_planning_prompt.md` v3.14 collision); no structural guard exists yet. | Head of Specs Team | Next `sprint_planning_prompt.md` / `CLAUDE.md` §8 revision cycle |

`BLG-GOV-285` (`governance_sync.yml` auto-close false-positive regex fix) was already filed during sprint execution (Phase 3) — no further closure action required beyond the priority note already recorded in `lessons_learnt_cycle.md`'s Phase 3 Recurrence Notes (2+ fires this cycle alone; recommend prioritising ahead of routine backlog debt).

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Exactly 1 of 19 scoped items this cycle was genuinely user-facing (`BLG-FE-137`), despite explicit user instruction to prioritise user features — every other `BLG-FEAT-*`/`BLG-FE-*` candidate is gate-blocked, largely on the SI-02 trade-plan-linkage data-density gate. (Carried from `lessons_learnt.md` this cycle.) | The next `run roadmap` rebalance should treat this cycle's Product Value Ratio reading as high-signal, and Product Owner should consider whether any near-term, ungated action could accelerate SI-02 data-density clearance rather than only re-deferring the same cluster a further cycle. | Roadmap |
| 2 | `post_ship_closure.md` STEP 5.1's cross-cycle deviation consolidation review is now live but has no formal cadence-field write step of its own (Friction Item 1 this cycle) — its cadence fields were initialized operationally at this closure's STEP 10 rather than by the step's own text. | Confirm at the 3rd-cycle-due check (roughly `2026-08-09`–`2026-08-13` depending on cycle pace) that the modulo-3 cadence actually fires as expected against the values initialized this run, before assuming the deferred prompt patch is merely cosmetic. | Post-Ship Closure |
