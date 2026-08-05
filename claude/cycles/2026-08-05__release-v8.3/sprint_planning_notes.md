**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-05
**Cycle:** 2026-08-05__release-v8.3

# Sprint Planning Notes — 2026-08-05__release-v8.3

## Backlog Slice Source

Original — `claude/cycles/2026-08-05__release-v8.3/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty in both `state.json` and `.claude_current_state.json`).

## Stale Backlog Slice Text (ST-11)

`stage4_backlog_slice.md` is sealed (Release Planning-owned; not editable by this engine per §6 Write Scope Restriction). Its ST-11 entry still carries the **pre-correction** title/AC/effort ("Shared modal shell for compliance/checklist components," "`ComplianceRecheckModal.js` and the PT-05 checklist modal both migrated," Effort M) from before design-gate escalation `ESC-20260805-01` was resolved.

`ESC-20260805-01`'s resolution (Base44 Frontend Prompt Owner, 2026-08-05, commit `85172aab`) corrected the canonical committed backlog item `BLG-FE-103` in `claude/backlog/backlog.md` — title, problem, scope, AC, and effort (M→S) all rewritten to a single-file migration of `ComplianceRecheckModal.js` onto the existing shared `Dialog`/`DialogContent` primitive. `design_gate.md` re-ran against this corrected item and cleared ST-11 to `Design Pre-Approved` using the corrected text.

**Resolution for this sprint:** ST-11's acceptance criteria for execution purposes are the corrected `claude/backlog/backlog.md#BLG-FE-103` text (reproduced below), not the stale `stage4_backlog_slice.md#ST-11` text. `sprint_backlog.md`'s ST-11 entry points to both sources explicitly and records the corrected AC/effort inline (a deliberate, documented exception to the "do not duplicate AC" rule, justified by the sealed source being stale) so the Execution Engine does not read the withdrawn "both modals" premise.

> **Corrected AC (source: `backlog.md#BLG-FE-103`):** `ComplianceRecheckModal.js` renders via the shared `Dialog`/`DialogContent` primitive (no bespoke overlay markup remaining); focus trap + restoration and Escape-to-close match the existing shared-primitive convention (`TradePlan.js` Abandon modal precedent); no visual/behavioural regression (Playwright coverage confirms). **Effort:** S.

**Advisory for a future engine:** `stage4_backlog_slice.md` has no correction mechanism once sealed and a design-gate escalation changes an item's scope after the fact — this is a process gap (the corrected text lives only in `backlog.md` and `design_gate.md`, never propagated back to the slice document sprint planning is told to treat as source-of-truth). Recommend filing a backlog item (`BLG-GOV-*`, P3) proposing that `design_gate_prompt.md` append a `## Post-Gate Corrections` addendum section to the cycle's `stage4_backlog_slice.md` (additive, not a mutation of sealed content) whenever a gate-blocking escalation changes an item's AC/effort/scope, so Sprint Planning does not have to reconstruct the correction from `backlog.md` + `design_gate.md` + `escalations.md` by hand next time.

## Carry-Forward Items

3 items reviewed from `claude/cycles/2026-08-04__release-v8.2/lessons_learnt_closure.md §Carry-Forward`:

1. Release Planning ungated-candidate scan gap (3 consecutive self-caught misses `v8.0`–`v8.2`) — routed to `groom backlog`/`run roadmap`, not Sprint Planning. No action here.
2. `BLG-FEAT-73`/`BLG-FEAT-74` sunset-trigger watch — already resolved this cycle at Release Planning (Option (b), formally parked; see `release_plan.md §Readiness`). No action here.
3. `post_ship_closure.md` STEP 10 field-list omission pattern — routed to Post-Ship Closure engine. No action here.

None of the three carry-forward items name an action for Sprint Planning. Recorded per `shared_standards.md §16.8` read protocol.

## Pre-Sprint Backlog Advisory

None. No `claude/backlog/backlog.md` items carry `Provisional-Target: Before v8.3 sprint planning`.

## Hygiene Advisories (STEP -1.7)

- **Prompt change log:** `sprint_planning_prompt.md` current `v3.15` matches the latest logged transition in `prompt_change_log.md` (`v3.14→v3.15`). No gap.
- **Endpoint test coverage audit** (`scripts/audit_endpoint_test_coverage.py`): clean — 78 routes scanned across 23 router files, 8 documented `KNOWN_GAPS` exclusions, 0 undocumented gaps.

## Deferred Items

None. All 27 items in the authoritative backlog slice are classified `include` — none deferred at Sprint Planning (capacity confirmed `pass` at every point in the confirmed band; see `sprint_capacity.md`).

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal (EPIC-01) | Resolved — sequenced consecutively within EPIC-01 |
| ST-08 | — | N/A (self-sequencing constraint) | RISK-01: apply across multiple sequenced commits/PRs, not one large diff — not a cross-item dependency |
| ST-12 | — (forward reference only) | External, non-blocking | `BLG-FE-116`/`BLG-FE-117` (not in this sprint's scope) are expected to reference ST-12's output in a future sprint. Does not block ST-12 itself; no action required this sprint. |

No circular dependencies identified. No cross-EPIC dependencies identified — all 6 EPICs can execute independently of one another (subject to the shared-file note below).

## Execution Sequence

All 27 `include` items are classified `autonomous` (see `sprint_backlog.md` per-story `Delegation class` fields; rationale: no item in this slice requires literal external/human-only action such as production credential provisioning — the bar established at `2026-08-04__release-v8.2`, where `delegated_backend` was reserved for exactly that case). With no delegation-tier grouping needed, sequencing follows thematic/priority order:

1. **EPIC-01 — Operational Reliability & Security** (ST-01 → ST-02 → ST-03 → ST-04) — leads per `cycle_summary.md`'s "led by two P1 operational items" framing; Design Gate already fully cleared (Design Not Applicable, all 4 items).
2. **EPIC-02 — Backend Engineering Hardening** (ST-05 → ST-06 → ST-07 → ST-08 → ST-09 → ST-10) — ST-08 (RISK-01, ~17-file mechanical change) sequenced last within the EPIC to apply incrementally without blocking the smaller items.
3. **EPIC-03 — Frontend & Design-System Debt** (ST-11 → ST-15 → ST-14 → ST-12 → ST-13) — Design Pre-Approved items (ST-11, ST-15, ST-14) sequenced first to unblock Playwright-coverage work early; Design Required items (ST-12, ST-13) follow, each against its own already-produced decision record.
4. **EPIC-04 — QA & Spec Debt** (ST-16 → ST-19 → ST-17 → ST-18 → ST-20 → ST-21) — ST-21 sequenced last within the EPIC because it shares `design_system.md` with EPIC-03 (see Shared File Ownership below) and should land after EPIC-03 merges.
5. **EPIC-05 — Governance Process** (ST-25 → ST-22 → ST-24 → ST-26 → ST-23) — ST-25 (fixes `prompt_change_log.md`'s prepend/append ordering) sequenced first within the EPIC so ST-22's own required `prompt_change_log.md` append (per CLAUDE.md §6 Governance File Edit Checklist) lands in the corrected format, not the defective one.
6. **EPIC-06 — Product Retrospective** (ST-27) — single item, no sequencing constraint.

**EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06 (thematic/priority order; EPIC-04 after EPIC-03 for the `design_system.md` shared-file reason above; no other cross-EPIC ordering constraint exists).

## Multi-EPIC Execution Notes

**`execution_state` owner:** Per the current per-EPIC mechanism (`shared_standards.md §12.1`), each EPIC branch owns and writes only its own `claude/cycles/2026-08-05__release-v8.3/execution_state/EPIC-xx.json`. **EPIC-01** is designated the structural-transition owner of `execution_state/_cycle_meta.json` (cycle-level fields: `sprint_goal`, `backlog_slice_source`, `invoked_utc`, `mode`, `open_escalations`, `process_notes`, `sealed`, `sealed_utc`) — it is the first EPIC in execution order. All other EPIC branches must check for `_cycle_meta.json` existence before creating their own version.

**Shared file ownership advisory:** `docs/specs/frontend/design_system.md` is touched by **EPIC-03** (ST-12, ST-13 — both Design Required, both already covered by decision records produced at Design Gate, combined into a single planned `1.6→1.7` version bump per `design_gate.md` Notes) and **EPIC-04** (ST-21 — also Design Required, also part of that same planned `1.6→1.7` combined bump). **EPIC-03 owns the canonical version bump** (sequenced first in EPIC merge order). EPIC-04 must rebase onto `main` after EPIC-03 merges before finalising its own `design_system.md` edit for ST-21, to avoid a double version-bump collision.

No other shared files identified across EPIC boundaries for this sprint (EPIC-05's `prompt_change_log.md` / `release_planning_prompt.md` touches from ST-22/ST-25 are both within EPIC-05 itself — an intra-EPIC sequencing matter, not a cross-EPIC file-ownership one; see Execution Sequence above for the ST-25-before-ST-22 rationale).

## Planning-Deferred Item Traceability

None. All 27 items in `stage4_backlog_slice.md` are included in the sealed sprint backlog — no items require an `execution_state.json` `deferred_at_planning` entry.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-02 (ST-08) | Valid — mitigation (incremental sequenced commits/PRs) restated in Execution Sequence above; no change since release planning |
| RISK-02 | EPIC-03 (ST-11, ST-15) | Valid — both items Design Gate PASSED (ST-11 re-classified Design Pre-Approved this cycle, ST-15 Design Pre-Approved); mitigation is Playwright coverage per each item's own AC, confirmed still required (see Staging-Only AC note below — neither is staging-only; both are CI-verifiable via Playwright, matching the RISK-02 mitigation as written) |
| RISK-03 | Release-level (BLG-FEAT-73/74) | Not associated with any `include` item this sprint — informational only |
| RISK-04 | Release-level (capacity sizing) | Superseded by this document's own capacity re-check (`sprint_capacity.md`) — effort recalculated to ~24.25d after the ST-11 correction, comfortably within the confirmed band; no phasing recommendation triggered |

No multi-vehicle fix-choice risks (LP-14 check) identified in the risk register — none of RISK-01 through RISK-04 name alternative fix vehicles requiring an execution-kickoff choice.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: clean — 0 known vulnerabilities across 57 scanned dependencies.

## Staging-Only AC Note (cross-reference for STEP 6.2 seal gate)

Only **ST-01** carries a staging-only-evidence AC this sprint: "SI-05 digest delivery confirmed working again (at least one successful send observed post-fix)" requires an actual live Telegram send, which is not CI-reproducible. Flagged `[staging-only evidence]` in `sprint_backlog.md`. All other items' ACs are either CI-verifiable (Playwright, mocked regression tests, synthetic lint/test cases) or documentation/process deliverables with no live-environment dependency — see per-story `Staging-only ACs` fields in `sprint_backlog.md` for the full accounting.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| File a `BLG-GOV-*` item proposing a `stage4_backlog_slice.md` post-gate-correction addendum mechanism (see Stale Backlog Slice Text note above) | Head of Specs Team | No — advisory, filed via `/backlog-add` post-seal |

No outstanding action is marked `Blocker? Yes`. No `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders remain unresolved.
