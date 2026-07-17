**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-17
**Cycle:** 2026-07-17__release-v7.5

# Sprint Planning Notes — 2026-07-17__release-v7.5

## Backlog Slice Source

Original — `claude/cycles/2026-07-17__release-v7.5/stage4_backlog_slice.md`. Cycle-local `state.json` `amended_backlog_slice_path` is empty — no amendment sealed for v7.5.

**Data hygiene flag (not a hard gate — advisory):** The top-level `.claude_current_state.json` field `amended_backlog_slice_path` is currently non-empty, but it points to `claude/cycles/2026-07-17__release-v7.4/amendments/AMD-20260717-01/amended_backlog_slice.md` — a **v7.4** artefact, left over from that cycle's amendment and never cleared when v7.4 closed. Per §5's rule this field gates which slice is authoritative "for this sprint," so it was cross-checked against the current cycle's own `state.json` (`amended_backlog_slice_path: ""`) rather than trusted blindly — confirming no amendment applies to v7.5 and the original `stage4_backlog_slice.md` is correct. Recommend Post-Ship Closure or a future hygiene pass clear this stale top-level field on cycle transition to prevent a future session from misreading it as applying to the active cycle.

## Carry-Forward Items

Reviewed `claude/cycles/2026-07-17__release-v7.4/lessons_learnt_closure.md ## Carry-Forward` (most recently completed cycle with `post_ship_complete = true`, per `.claude_current_state.json last_post_ship_cycle`). 3 items:

1. **Governance-input due-date tracking mechanism:** Not directly actionable by Sprint Planning — no such item is present in this cycle's scope. Noted for awareness.
2. **`BLG-FE-116` design-artefact production:** **Closed this cycle.** Design artefact (`docs/design/2026-07-17__release-v7.5/custom-price-alerts/ux_spec.md`) was produced as a Design Gate precursor step before this sprint planning run — exactly the pattern the carry-forward asked for. Confirmed via `design_gate.md`.
3. **Structural cross-check between Release Planning and Design Gate:** **Addressed this cycle** via the explicit sequencing fix described in `release_plan.md` RISK-01 and confirmed in `design_gate.md` Notes (design-artefact production run as Design Gate's own STEP 2 work, not scheduled as in-sprint work of another item). No further Sprint Planning action required.

## Deferred Items

None. All 4 items from the authoritative backlog slice are classified `include` — full scope proceeds within capacity (11.0d midpoint vs. ~24–28d band, PASS, ~46% utilisation at midpoint).

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 (`BLG-FE-115`) | None | — | Ready |
| ST-02 (`BLG-FE-116`) | None | — | Ready |
| ST-03 (`BLG-FE-117`) | None | — | Ready |
| ST-04 (`BLG-FE-118`) | None | — | Ready |

No cross-item dependencies. Per `release_plan.md` Execution Plan: "All 4 EPICs may execute in parallel once unblocked — no cross-EPIC data-model dependency."

## Execution Sequence

1. **EPIC-01** (ST-01, command palette) — `delegated_frontend`, no backend dependency, smallest scope (M, ~1–2 days). Sequenced first — simplest EPIC, per `CLAUDE.md` §8 "merge simplest EPIC first" convention; also designated `execution_state.json` owner (see Multi-EPIC Execution Notes below).
2. **EPIC-02** (ST-02, custom price alerts) — `delegated_frontend` (+ backend data-model work, RISK-03). Largest effort (L, ~3–5 days) and only item with backend scope. Sequenced 2nd (not last) to leave runway if the pre-scoped backend integration surfaces a genuine issue during implementation — same rationale as the v7.3 RISK-03 sequencing precedent.
3. **EPIC-03** (ST-03, bulk actions) — `delegated_frontend`, no backend dependency (M, ~1–2 days).
4. **EPIC-04** (ST-04, saved filters + calendar) — `delegated_frontend`, no backend dependency (L, ~3–5 days).

No circular dependencies detected.

**Multi-EPIC Execution Notes:** 4 EPICs in scope (> 1). Per `sprint_planning_prompt.md` §5.2:
- `execution_state.json` owner: **EPIC-01** (first in execution order). EPIC-02/03/04 branches must check for `execution_state.json` existence before creating their own and append their EPIC's section rather than overwrite.
- **Shared file ownership advisory:** No source file is modified by more than one EPIC. The one plausible overlap — EPIC-03 (Watchlist/TradePlans multi-select) vs. EPIC-04 (saved filters) both touching `Watchlist.js` — was resolved by the Design Gate's explicit placement decision: ST-04's saved filters and calendar view were placed on **Trade History only** (`trade_history.md` v1.11), not split across Screener/TradeHistory/Watchlist as the original backlog scope wording suggested (`design_gate.md` Notes, "Placement decisions requiring explicit call"). EPIC-03 remains confined to `Watchlist.js`/`TradePlans.js`; EPIC-04 is confined to `TradeHistory.js`. No cross-EPIC file conflict identified. Standard `CLAUDE.md` §8 procedure still applies proactively if concurrent PRs report `CONFLICTING/DIRTY` on governance files (`execution_state.json`, `openapi.yaml`, `api_changelog.md`, `data_model.md`) — RISK-02.

**Planning-deferred item traceability (AUD-2026-05-21-002):** Not applicable — no ST item from the authoritative backlog slice is excluded from the sealed sprint backlog; all 4 are `include`.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | Release-level | **Resolved** — Design Gate passed 2026-07-17, 4/4 items cleared, 0 blocked (`design_gate.md`). The structural fix (artefact production sequenced as a Design Gate precursor, not in-sprint work) is confirmed applied — the v7.4 `AMD-20260717-01` recurrence pattern did not repeat. |
| RISK-02 | Release-level | Valid — cross-EPIC merge conflict risk remains live with 4 EPICs open concurrently. `CLAUDE.md` §8 procedure to be applied proactively if `CONFLICTING/DIRTY` is reported. Execution sequence and merge order above are the primary mitigation. |
| RISK-03 | EPIC-02 | Valid, but pre-scoped — `blg_fe_116_pre_implementation_readiness_pass.md` (filed 2026-07-16) already covers schema, evaluation-pipeline extension, health-check surfacing, with §13 PASS, confirmed sufficient and unchanged by the Design Gate. No outstanding backend-scoping gap blocks this sprint. EPIC-02 sequenced 2nd to preserve runway per Execution Sequence above. |

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json` (via `backend/.venv`): **clean** — 61 dependencies scanned, 0 known vulnerabilities.

## Hygiene Advisories (non-blocking)

**Prompt change log gap** (per STEP -1 advisory 7 — current version ahead of last logged transition):
- ⚠ `sprint_planning_prompt.md` current v3.13 — last log entry (`prompt_change_log.md` line 49) targets v3.12. This is a long-standing, previously-flagged gap (identical finding recorded at `2026-07-16__release-v7.3` sprint planning) — advisory only, does not block this sprint. Head of Specs Team to add the missing prepended row when convenient.

**Pre-Sprint Backlog Advisory:** No `claude/backlog/backlog.md` items found with `Provisional-Target: Before v7.5 sprint planning`.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Add missing `sprint_planning_prompt.md` v3.13 prompt-change-log row | Head of Specs Team | No |
| Clear stale top-level `.claude_current_state.json amended_backlog_slice_path` (v7.4 leftover) | PMO Lead / Head of Specs Team | No |
| Apply `CLAUDE.md` §8 procedure proactively if concurrent EPIC PRs report `CONFLICTING/DIRTY` | PMO Lead | No |

No outstanding action is a Blocker.
