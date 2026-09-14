**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-14
**Cycle:** 2026-09-14__release-v9.4

# Sprint Planning Notes — 2026-09-14__release-v9.4

## Backlog Slice Source

Original — `claude/cycles/2026-09-14__release-v9.4/stage4_backlog_slice.md` (`amended_backlog_slice_path` empty in both `.claude_current_state.json` and `state.json` — no amendment sealed this cycle).

## Carry-Forward Items

Reviewed `claude/cycles/2026-09-09__release-v9.3/lessons_learnt_closure.md ## Carry-Forward` (most recently completed cycle, `post_ship_complete = true`): 3 items present, all scoped to `Post-Ship Closure` or `Delivery Verification / Post-Ship Closure` engines — none targets `Sprint Planning` or `All`. No action required this run.

## Pre-Sprint Backlog Advisory

Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v9.4 sprint planning` — 0 matches. No unconverted items to surface.

## Deferred Items

All 28 items in the authoritative backlog slice enter this sprint (`include`) — see STEP 3 Scope Selection below. No item is deferred out of the sealed slice at Sprint Planning. Items excluded from v9.4 scope entirely were dispositioned at Release Planning (not re-litigated here, per §1 — this routine does not alter the release plan):

| Item | Reason | Next Sprint Candidate? |
|------|--------|-------------------------|
| `BLG-GOV-178` | Literal AC already shipped at v9.3; retained un-archived only for escalation-tracking (`ESC-EXEC-20260910-01`, now `Deferred`) | No — tracking-only |
| `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76`, `BLG-SPEC-56`, `BLG-SPEC-57`, `BLG-QA-59` | Data-quality-flagged (embedded gate-like free text, no formal `Gate` field) — not-ready | Yes, once gate fields are normalised |
| 130 formally gated/conditional items | No clearance evidence this cycle (data-density/AI-adoption/§13-review gates unchanged) | Gate-dependent |
| 46 further ungated P3/P4 items (~37.50d) | Capacity — ready pool (74 items/~65.05d) exceeds the confirmed band even at full-capacity selection | Yes — available for `plan release v9.5` |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-23 (`BLG-AI-06`) | — | Internal (soft sequencing) | N/A — ST-22 sequenced after it, not the reverse |
| ST-22 (`BLG-AI-05`) | ST-23 (`BLG-AI-06`) | Internal | To be resolved at execution — RISK-05 mitigation: sequence after ST-23 if both touch the same AI-response wrapper, to avoid the disclosure badge and sampling hook colliding on the same shared chokepoint |
| ST-16 (`BLG-FR-02`) | `BLG-QA-122` (backlog, blocked — no broker-import mechanism) | External | Not blocking — ST-16's own AC scopes this cycle to spec/dependency-mapping only |
| EPIC-05 (design_system.md, dashboard.md) | EPIC-04 (design_system.md) | Shared-file (spec) | Sequence EPIC-04 before EPIC-05 — see Shared File Ownership below |
| EPIC-06 (dashboard.md) | EPIC-05 (dashboard.md) | Shared-file (spec) | Sequence EPIC-05 before EPIC-06 — design gate confirms EPIC-06's own dashboard.md touch (ST-25) is "conformant, no change", so risk is low, but ownership order still applies |

No circular dependencies identified.

## Execution Sequence

Per `release_plan.md ## Execution Plan`: EPIC-01 through EPIC-04 have "No UI ACs; independent of other EPICs" — no forced inter-EPIC ordering among them. EPIC-05 and EPIC-06 carry the shared-spec-file sequencing above. Chosen execution order (also the merge order — see `sprint_backlog.md`):

1. **EPIC-01** — Backend & Platform Engineering Debt (no dependencies; `execution_state.json` owner)
2. **EPIC-02** — QA & Test Coverage Debt (no dependencies)
3. **EPIC-03** — Operations & Security Debt (no dependencies)
4. **EPIC-04** — Spec, Documentation & Financial Reporting Debt (touches `design_system.md` — must land before EPIC-05)
5. **EPIC-05** — Governance Process & AI Compliance Debt (touches `design_system.md`, `dashboard.md`; internally, ST-23 before ST-22)
6. **EPIC-06** — Frontend, UX & Product Debt (touches `dashboard.md`, `screener_results.md`, `red_flag_journal.md`, `position_form.md`)

**Multi-EPIC `execution_state.json` ownership:** EPIC-01 (first in execution order) owns `execution_state.json`. EPIC-02 through EPIC-06 must check for its existence before creating their own version — if found, read and append their own EPIC section rather than overwrite.

**Shared file ownership advisory:**

| File | EPICs touching it | Owner (first to land) | Note |
|------|--------------------|-----------------------|------|
| `design_system.md` | EPIC-04 (ST-13, ST-27), EPIC-05 (ST-22) | EPIC-04 | EPIC-05 must rebase onto `main` after EPIC-04 merges before finalising its `design_system.md` change |
| `dashboard.md` | EPIC-05 (ST-22), EPIC-06 (ST-25 — confirmed conformant, no change expected) | EPIC-05 | EPIC-06 should rebase after EPIC-05 merges as a precaution even though its own touch is expected to be a no-op |
| `reports.md` | EPIC-04 (ST-17) only | EPIC-04 | No cross-EPIC contention |
| `openapi.yaml` / `data_model.md` | Not touched by any story this cycle (no new API endpoints or schema fields in scope) | N/A | No cross-EPIC contention |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|------------------|--------------------|
| RISK-01 | EPIC-01 (ST-01) | Valid — pre-check to be written into the migration script itself; live-DB pre-check disclosed as pending a DB-accessible environment if unavailable |
| RISK-02 | EPIC-02 (ST-07) | Valid — confirm current `get_arc5_trade_plan_adherence_rate` signature before writing tests |
| RISK-03 | EPIC-03 (ST-09, ST-10) | Valid — re-confirmed this session (`DATABASE_URL` still unset in this execution environment); implement/wire fully regardless, disclose rather than fabricate the "runs against real data" sub-criterion if it cannot execute here |
| RISK-04 | EPIC-04 (ST-16) | Valid — no mitigation action needed beyond following ST-16's own spec-only scoping as written |
| RISK-05 | EPIC-05 (ST-22, ST-23) | Valid — sequencing (ST-23 before ST-22) adopted in Dependency Map above as the primary mitigation |
| RISK-06 | EPIC-06 (ST-25, ST-28) | **Resolved** — `run design-gate --cycle 2026-09-14__release-v9.4` passed (`design_gate.md`, 2026-09-14); `sprint_planning_pre_condition` met |

No risk has materialised since Release Planning; all mitigation approaches remain valid as stated.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json` — **clean**. 58 dependencies scanned, 0 known vulnerabilities, 0 fixes required. Trend row appended to `docs/ops/pip_audit_trend_log.md` in this session (see that file for the full row).

## Recurring Endpoint Test Coverage Audit

`python3 scripts/audit_endpoint_test_coverage.py` — **clean**. 90 route decorators scanned across 26 router files; 8 documented `KNOWN_GAPS` exclusions; 0 undocumented gaps.

## Prompt Change Log Gap Check

Spot-checked `sprint_planning_prompt.md` (the prompt governing this run): header `v3.18` matches the latest logged transition in `prompt_change_log.md` (`v3.17→v3.18`, 2026-09-08) — no gap. No other Class 6 prompt was modified or newly relied upon in a way that would surface a fresh gap this session; a full 17-file cross-reference was not re-run in full (advisory-only check; no gate impact).

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|-------------------------|
| Buffer-floor-exceeded acknowledgement (27.55d / 28d = 98.4%) | Product Owner | No — advisory only; acknowledged via the standing "use full capacity" instruction (see `sprint_capacity.md §1.5`) |
| ST-23 (`BLG-AI-06`) should land, and `ESC-EXEC-20260910-01` should be re-acknowledged, before ST-22 (`BLG-AI-05`) if a shared AI-response chokepoint exists | PMO Lead / execution sequencing | No — soft sequencing, not a hard blocker |

No outstanding action is marked `Blocker? Yes`.

---

## Change Log

| Date | Change |
|------|--------|
| 2026-09-14 | Initial publication — dependency map, execution/merge sequence, risk flags, and hygiene checks for 2026-09-14__release-v9.4. |
