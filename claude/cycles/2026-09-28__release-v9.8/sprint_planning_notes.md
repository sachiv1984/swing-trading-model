**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-28
**Cycle:** 2026-09-28__release-v9.8

# Sprint Planning Notes — 2026-09-28__release-v9.8

## Backlog Slice Source

Original — `claude/cycles/2026-09-28__release-v9.8/stage4_backlog_slice.md` (`.claude_current_state.json.amended_backlog_slice_path` is empty; no amendment in effect this cycle).

## Carry-Forward Items

3 items reviewed from `claude/cycles/2026-09-23__release-v9.7/lessons_learnt_closure.md` (most recently completed cycle, `post_ship_complete = true`):

1. Two open decision-required/recurrence escalations (`ESC-CLOSE-20260928-01`, `ESC-CLOSE-20260928-02`) — both since resolved per `.claude_current_state.json.open_escalations` (`ESC-CLOSE-20260928-01` closed by lifecycle audit `AUD-2026-09-28`; `ESC-CLOSE-20260928-02` remains open, not yet SLA-due (2026-10-01), non-blocking). No sprint-planning action required.
2. `execution_prompt.md` STEP 3.1/§3.1.D sync-gap watch item (1st carry at v9.7 closure) — actionable at the next `execution_prompt.md` revision, not at sprint planning. No action here.
3. `DEV-<id>`-assignment-at-filing-time process gap (3rd recurrence) — actionable at `groom backlog`/Post-Ship Closure, not sprint planning. No action here.

None of the 3 carry-forward items fall within Sprint Planning's write scope or require a scope/sequencing change to this cycle's backlog.

## Deferred Items

None. All 39 items in the authoritative backlog slice enter the sprint backlog as `include` — scope sits at exactly 28.00/28.00 days (100% of the confirmed band's top edge), no over-allocation, no blocked/missing-owner/missing-estimate items found at STEP 3.1 candidate review.

## Pre-seal Stale-Feature-Target Check

All 39 `BLG-*` source IDs checked against `claude/backlog/backlog_archive.md` — none already shipped. Clear.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-26 (BLG-SPEC-161, EPIC-05) | ST-02 (BLG-FE-185, EPIC-01) | Shared-file (Screener.js / SCREENER_COLUMNS) | Sequencing constraint — see Execution Sequence |

No other cross-item dependencies identified among the 39 items. No circular dependencies. No spec-lock prerequisites outstanding (no item in this slice depends on a backend wire contract or design decision made by another item in the slice — RISK-01/RISK-02 below are internal-to-story design-decision sub-steps, not cross-item dependencies).

## Delegation Class Assignment

| Class | Items |
|-------|-------|
| `autonomous` | ST-01, ST-02, ST-03, ST-04, ST-05, ST-06, ST-07, ST-08, ST-09, ST-10, ST-11, ST-12, ST-13, ST-14, ST-16, ST-19, ST-20, ST-21, ST-22, ST-23, ST-24, ST-25, ST-26, ST-27, ST-28, ST-30, ST-31, ST-32, ST-33, ST-34, ST-35, ST-36, ST-37, ST-39 (34 items) |
| `delegated_decision` | ST-17 (BLG-OPS-169, RISK-01), ST-18 (BLG-OPS-170), ST-29 (BLG-SPEC-172), ST-38 (BLG-GOV-351, RISK-02) (4 items) |
| `delegated_qa` | ST-15 (BLG-QA-184, mutation-testing survivor triage) (1 item) |

**Justifications for non-default classification:**
- **ST-17** — RISK-01: BLG-OPS-169's own Scope text names three genuinely alternative implementation vehicles (existing `staging-smoke-test.yml`, a new post-merge workflow, or a cycle-close verification step) with the choice explicitly deferred to implementation time; requires an Infrastructure & Operations Owner decision before the build proceeds.
- **ST-18** — establishing a pre-approved staging-DB query-pattern allow-list is a security-sensitive policy call (what may run without further confirmation against a production-adjacent environment), not a mechanical documentation task; requires Infrastructure & Operations Owner / Cybersecurity & Trust Lead judgment.
- **ST-29** — AC explicitly requires "the disposition recorded by the Strategy Rules & System Intent Owner" — a named-authority decision, not an engine-determinable outcome.
- **ST-38** — RISK-02: BLG-GOV-351's own Scope text defers "which governed routine owns firing the review" to a decision at build time; requires Head of Specs Team / PMO Lead judgment (post-ship closure's own cadence checks are the most natural fit per the item's own Problem statement, but this is not treated as pre-decided here — see Risk Flags below).
- **ST-15** — mutation-testing survivor triage requires QA judgment on which surviving mutants represent genuine test gaps vs. acceptable equivalence; kept with Director of Quality rather than autonomous engine disposition.

No `delegated_frontend` items this cycle — EPIC-01's UI-visible items (ST-01–ST-04) are refactors/bug fixes against existing behaviour with no new UX design decisions (LL-v1.10-P3-3 / BLG-GOV-72 fast-path default: autonomous), and ST-05/ST-06 are spec-authoring tasks documenting existing or well-scoped behaviour, not new UX design.

**LL-v2.2-SP-01 (delegated_decision design-artefact check):** No HoST design session artefact exists for ST-17, ST-18, ST-29, or ST-38 — advisory only, per prompt. Recommend Head of Specs Team schedule a brief design/decision session ahead of each item's execution kickoff, sequenced early within its EPIC (see Execution Sequence).

## Execution Sequence

Per `release_plan.md ## Execution Plan`'s stated table order (EPIC-01 leads — Skill-Silo rotation guideline honouring, most execution-heavy category, no ready build-and-ship U-item exists this cycle):

1. **EPIC-01** — Frontend & UX Debt Clearance (ST-01 → ST-02 → ST-03 → ST-04 → ST-05 → ST-06). ST-02 sequenced ahead of ST-26 (EPIC-05) — see Shared File Ownership Advisory below.
2. **EPIC-02** — Backend Reliability & Financial Correctness (ST-07 → ST-08)
3. **EPIC-03** — QA & Test Coverage (ST-09 → ST-10 → ST-11 → ST-12 → ST-13 → ST-14 → ST-15 → ST-16)
4. **EPIC-04** — Operations & Security Hardening (ST-17 [design-decision sub-step, then implementation] → ST-18 [design-decision sub-step, then implementation] → ST-19)
5. **EPIC-05** — Spec & API Contract Debt (ST-20 → ST-21 → ST-22 → ST-23 → ST-24 → ST-25 → ST-26 [after EPIC-01 merges] → ST-27 → ST-28 → ST-29)
6. **EPIC-06** — Governance & Process Debt (ST-30 → ST-31 → ST-32 → ST-33 → ST-34 → ST-35 → ST-36 → ST-37 → ST-38 [design-decision sub-step, then implementation] → ST-39)

Within each EPIC, autonomous items are sequenced ahead of `delegated_decision`/`delegated_qa` items where no other constraint applies, to unblock delegation early (EPIC-04 and EPIC-06 are exceptions — ST-17/ST-18 and ST-38 respectively are early in their own EPIC's natural numeric/thematic order and their design-decision sub-steps do not block sibling items in the same EPIC, so no reordering was needed to satisfy this rule).

No circular dependencies detected.

**Multi-EPIC `execution_state.json` ownership:** EPIC-01 is designated `execution_state.json` owner (first EPIC in execution order). EPIC-02 through EPIC-06 branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

**Shared file ownership advisory:**

| Shared file | Owning EPIC (canonical version) | Later EPIC(s) — must rebase after owner merges |
|-------------|----------------------------------|--------------------------------------------------|
| `src/pages/Screener.js` (`SCREENER_COLUMNS`) | EPIC-01 (ST-02 drives Screener/Watchlist cells from shared column definitions) | EPIC-05 (ST-26 verifies `screener_results.md` §5.3 matches the post-ST-02 `SCREENER_COLUMNS`) |

No other cross-EPIC shared-file collisions identified (`execution_state.json`, `openapi.yaml`, `api_changelog.md`, and `data_model.md` are each touched by items within a single EPIC — EPIC-05 — this cycle, so no cross-EPIC contention on those files).

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-04 (ST-17, BLG-OPS-169) | Valid — mitigation (phase as a short design-decision sub-step ahead of implementation, per its own Scope text) confirmed still applicable at sprint planning; no new information since release planning. Delegation class set to `delegated_decision` (see above). |
| RISK-02 | EPIC-06 (ST-38, BLG-GOV-351) | Valid — mitigation (phase as a design-decision sub-step on routine ownership, per its own Scope text) confirmed still applicable; no new information since release planning. Delegation class set to `delegated_decision` (see above). |

**Multi-vehicle fix-choice risk check (LP-14):** Both RISK-01 and RISK-02 name multiple genuinely alternative fix vehicles with the choice deferred to execution kickoff (RISK-01: 3 vehicles; RISK-02: "most natural fit" named but not pre-decided). Effort impact checked: all named alternatives for both risks sit within the same Effort S (~0.5–1d) band already estimated for their parent story — no alternative meaningfully changes the day estimate, so no capacity cross-reference is needed (no Phasing Recommendation exists this cycle regardless, per `release_plan.md ## Capacity Check` — outcome is `pass`, not `warn`). Recorded per LP-14 even though the final decision remains "resolve at kickoff."

## Pre-Sprint Vulnerability Scan

Clean — `pip-audit` (via `backend/.venv/bin/python3 -m pip_audit -r backend/requirements.txt --format=json`, project virtualenv per CLAUDE.md §9) reports 58 resolved dependencies, 0 known vulnerabilities. Trend row appended to `docs/ops/pip_audit_trend_log.md`.

## Hygiene Advisories

- **Prompt change log gaps:** none. All 15 versioned Class 6 files in `claude/system/` checked against `prompt_change_log.md` by latest-dated matching row (not file position) — every file's current `**Version:**` matches its most recent logged bump.
- **"Before Sprint Planning" backlog items:** none found — `grep "Provisional-Target: Before v9.8 sprint planning" claude/backlog/backlog.md` returned no matches.
- **Recurring endpoint test coverage audit:** clean — `scripts/audit_endpoint_test_coverage.py` exit 0; 93 route decorators scanned across 27 router files, 8 documented `KNOWN_GAPS` exclusions, 0 undocumented gaps.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| None — no `[AC REQUIRED]`/`[ESTIMATE REQUIRED]` placeholders, no `Blocker? Yes` items, no unresolved pre-sprint decisions (`cycle_summary.md` carries no `## Pre-sprint Planning Required Decisions` section this cycle). | — | No |
