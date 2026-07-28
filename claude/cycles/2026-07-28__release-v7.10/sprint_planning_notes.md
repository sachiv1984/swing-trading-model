**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-28
**Cycle:** 2026-07-28__release-v7.10

# Sprint Planning Notes — 2026-07-28__release-v7.10

## Backlog Slice Source

Original — `claude/cycles/2026-07-28__release-v7.10/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty in both `.claude_current_state.json` and `state.json` — no amendment sealed for this cycle).

## Carry-Forward Items

Reviewed from most recently completed cycle `2026-07-27__release-v7.9` (`lessons_learnt_closure.md ## Carry-Forward`, 2 items):

1. `BLG-OPS-111` endpoint-coverage drift item has a 4-endpoint delta accumulated since original filing — targeted at Post-Ship Closure, not this sprint. No in-scope v7.10 item actions `BLG-OPS-111`. No action required here.
2. `BLG-FEAT-73`/`BLG-FEAT-74` SI-02 live re-check should use the now-provisioned staging credential (`BLG-OPS-121`, resolved 2026-07-28) rather than citing the stale 2026-07-17 field — targeted at the next `plan release`/roadmap rebalance, not Sprint Planning. No in-scope v7.10 item actions this. No action required here.

Neither carry-forward item is actionable by this sprint's scope; both are correctly targeted at other engines. Recorded for traceability only.

## Deferred Items

None. All 23 ST items in the authoritative backlog slice are classified `include` — none deferred at Sprint Planning. (Items excluded from the *release* scope entirely — `BLG-FEAT-73`/`74`, the Arc 5 UX cluster, and ~157 ungated P3 candidates — were excluded at Release Planning, not here; see `release_plan.md ## Scope — Items explicitly deferred`. They are out of scope for this document.)

## Scope Selection (STEP 3.1)

All 23 items reviewed against: within confirmed capacity (yes — see `sprint_capacity.md`, ~26.15d midpoint vs ~24-28d band, outcome `pass`), has an owner (yes, all — per `release_plan.md ## Execution Plan`), has acceptance criteria (yes, all — per `stage4_backlog_slice.md`, no `[AC REQUIRED]` placeholders), not blocked by unresolved dependency/escalation (yes — `open_escalations = []`, `deferred_execution_blockers = []` in `state.json`).

**Classification: `include` — all 23 items.** No `defer` or `flag` items this sprint.

## Delegation Classification (STEP 3.1, §12 invariant)

All 23 items classified **`autonomous`**. Rationale: `design_gate.md` classified every item either `Design Pre-Approved`, `Design Not Applicable`, or `Design Required`-but-cleared-without-new-design-work (ST-17, ST-19 — both implement an already-locked/existing spec/visual reference, per `design_gate.md` Notes). No item in this slice requires a new UX design decision, external stakeholder input, or a human-only execution step:

- EPIC-01/02/03/04/06 (19 items): backend/security/QA/spec/governance code, doc, audit, and test changes with no UI surface — fits the standard autonomous profile.
- EPIC-05 (ST-17, ST-18, ST-19, ST-20): fits the BLG-GOV-72 fast-path by analogy — ST-18 is a prop/branch addition with no UX change (fast-path (a)/(b)); ST-17 and ST-19 are UI changes implemented against an existing/locked reference (fast-path (c) — no new design decisions per `design_gate.md`); ST-20 is an audit producible via scripted/automated keyboard-navigation checks, consistent with the other audit items in scope (ST-04, ST-07, ST-11).

No `delegated_decision` items — no risk register entry defers a genuine either/or choice to execution kickoff (see Risk Flags below). No `delegated_frontend` items — LL-v2.0-P4-2 test-scenario-gap rule therefore does not apply this sprint. No `delegated_backend`/`delegated_qa` items — no LL-v2.2-SP-01 design-artefact check triggered.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-12 (BLG-QA-128, EPIC-03) | ST-13, ST-14, ST-15 (EPIC-04) | Internal (cross-EPIC) | Resolved — sequence EPIC-04 before EPIC-03's ST-12 so the consumer-driven contract check runs against corrected contract docs, not stale ones |
| ST-11 (BLG-QA-133, EPIC-03) | ST-10 (BLG-QA-96, EPIC-03) | Internal (same-EPIC) | Resolved — sequence ST-10 before ST-11 so the endpoint test-suite coverage audit accounts for the newly-added Red Flag Journal auth regression test |

No external dependencies (no delegated items, no third-party blockers) and no spec-lock dependencies beyond the two above identified this sprint. No circular dependencies detected.

## Execution Sequence

1. **EPIC-04** — API Contract & Spec Debt Cleanup (ST-13, ST-14, ST-15, ST-16) — sequenced first: lightweight (XS×3 + M), unblocks ST-12's contract baseline.
2. **EPIC-01** — Backend Reliability & Error-Handling Hardening (ST-01, ST-02, ST-03, ST-04)
3. **EPIC-02** — Security Hardening (ST-05, ST-06, ST-07, ST-08)
4. **EPIC-03** — QA & Test Infrastructure Hardening (ST-09, ST-10, ST-11, ST-12) — internal order ST-09 → ST-10 → ST-11 → ST-12 per Dependency Map
5. **EPIC-05** — Frontend Technical Debt & Accessibility (ST-17, ST-18, ST-19, ST-20)
6. **EPIC-06** — Governance Process Hardening (ST-21, ST-22, ST-23)

All items classified `autonomous` — no grouping adjustment needed for delegation-unblocking purposes (LL-v1.10-P3-3 / BLG-GOV-72 note: ordering here is driven purely by the one identified cross-EPIC dependency, not by delegation class).

### Multi-EPIC Execution Notes (Required — 6 EPICs in scope)

**`execution_state.json` owner: EPIC-04** (first in execution order above). All other EPIC branches (EPIC-01, 02, 03, 05, 06) must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite, per CLAUDE.md / `execution_prompt.md` multi-EPIC handling.

**Shared file ownership advisory:** No source files are touched by more than one EPIC this sprint — each EPIC's scope items operate on distinct files/directories (EPIC-01: `portfolio_risk.py` and provider call sites; EPIC-02: `backend/main.py`, `.githooks/`; EPIC-03: `playwright.config.js`, `backend/routers/test.py`; EPIC-04: `docs/specs/api_contracts/position_endpoints.md`, `trade_endpoints.md`, OpenAPI CI linter; EPIC-05: `calendar.js`, `SystemStatus.js`, `StrategyBenchmark.js`; EPIC-06: `design_gate_prompt.md`, `roadmap_prompt.md`). The only shared artefact across all EPICs is `execution_state.json` itself (ownership designated above). No merge-order rebase risk beyond the standard multi-EPIC sequencing this implies.

## Risk Flags (STEP 5.3)

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-05 (ST-17, ST-19) | Valid — Design Gate has since passed (`design_gate.md`, 2026-07-28); Playwright coverage or recorded staging sign-off remains required at delivery verification per CLAUDE.md §2 (both ACs carry `[staging-only evidence]` in `stage4_backlog_slice.md`) |
| RISK-02 | EPIC-01 (ST-03) | Valid — mitigation (additive/opt-in dedup check only, no behaviour change when key absent) unchanged since release planning |
| RISK-03 | EPIC-02 (ST-08) | Valid — mitigation (AC explicitly excludes safe 4xx messages; QA to spot-check a 4xx sample) unchanged |
| RISK-04 | EPIC-03 (ST-09) | Valid — mitigation (land on feature branch, confirm full 677-test suite against production-served build before merge, keep `npm start` local fallback) unchanged |
| RISK-05 | Release-level | Valid — full-capacity-band scope accepted per explicit user instruction, recorded in `docs/product/decisions/decisions--2026-07-28__release-v7.10.md`; `sprint_capacity.md` confirms no over-allocation against the ~28-day ceiling |

No risk has materialised since release planning (all mitigations still apply as originally scoped).

**Multi-vehicle fix-choice risk check (LP-14):** Not applicable this cycle — no Risk Register item above names two or more alternative fix vehicles deferred to execution kickoff; each risk carries a single, already-scoped mitigation approach. No cross-reference to a Phasing Recommendation is required (none exists — `release_plan.md ## Capacity Check` outcome was `pass`, not `warn`).

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json` (run via `backend/.venv/bin/python3 -m pip_audit`, per CLAUDE.md §9): **clean** — 0 known vulnerabilities across all resolved dependencies (fastapi 0.135.1, starlette 1.3.1, anthropic 0.105.2, and all transitive dependencies).

## Pre-Sprint Backlog Advisory

No `claude/backlog/backlog.md` items found with `Provisional-Target: Before v7.10 sprint planning` (grep returned zero matches).

## Hygiene Advisory — Prompt Change Log

`sprint_planning_prompt.md` current `**Version:** 3.13` — most recent `prompt_change_log.md` entry confirms `v3.12→v3.13` (2026-07-14). No gap.

## Staging-Only AC Pre-Stage (informational — enforced at STEP 6.2 seal gate)

Two ACs carry `[staging-only evidence]` in `stage4_backlog_slice.md`: ST-17 (visual rendering spot-check) and ST-19 (visual rendering match). Both are recorded explicitly in each story's `**Staging-only ACs:**` field in `sprint_backlog.md` (see STEP 6.2 seal check below) — not left as `None`.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Confirm sprint goal (`sprint_goal.md`) | Product Owner | Yes |
| Confirm sprint backlog Product Owner Sign-Off block (`sprint_backlog.md`) | Product Owner | Yes |

No outstanding action is marked `Blocker? Yes` beyond the two explicit sign-off items above, both resolved by the same PO confirmation step.
