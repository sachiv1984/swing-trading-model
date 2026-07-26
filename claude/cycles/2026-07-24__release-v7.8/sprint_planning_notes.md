**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-26
**Cycle:** 2026-07-24__release-v7.8

# Sprint Planning Notes — 2026-07-24__release-v7.8

## Backlog Slice Source

Original — `claude/cycles/2026-07-24__release-v7.8/stage4_backlog_slice.md` (`.claude_current_state.json.amended_backlog_slice_path` is absent/empty — no amendment in effect).

## Design Gate / Lifecycle Note (Process Deviation — Advisory)

The design gate genuinely ran and Passed (`design_gate.md`, this cycle: 12/12 items cleared, 0 blocked; PMO Lead, Head of UX & Design, and Product Owner all confirmed; cycle-level `state.json.design_gate_status = "Passed"`). However, `design_gate_prompt.md` v1.4's write scope (§5) does not include `.claude_current_state.json` — it only writes the cycle-level `state.json`. As a result the root state pointer's `status` field was never advanced from `Release_Planning_Complete` to `Design_Gate_Passed`, and `design_gate_status`/`design_gate_record`/`design_gate_completed_utc` in `.claude_current_state.json` remained stale (`not_started` / empty / empty) even though the cycle-level record shows the gate passed.

STEP -1.3's bypass audit is keyed off the literal `.claude_current_state.json.status` value and would treat entry from `Release_Planning_Complete` as "design gate skipped entirely," requiring `design_gate_bypass_authority`/`design_gate_bypass_reason`. Per Product Owner decision this session: this is a state-pointer sync gap in `design_gate_prompt.md`, not an actual bypass — gate 3 was independently verified directly against the authoritative cycle-level `state.json` (`design_gate_status = Passed`), and sprint planning proceeds on that basis rather than populating bypass-authority fields for a gate that was not, in fact, bypassed.

**Recommended backlog item (file separately via `/backlog-add`):** add a STEP to `design_gate_prompt.md` STEP 5 that also syncs `.claude_current_state.json` (`status`, `design_gate_status`, `design_gate_record`, `design_gate_completed_utc`) atomically with the cycle-level `state.json` write, closing this gap for future cycles.

## Carry-Forward Items

Carry-forward items reviewed: 3 items from cycle `2026-07-21__release-v7.7` (`lessons_learnt_closure.md ## Carry-Forward`). All 3 are scoped to Roadmap/Release Planning/All engines (empty-Now-horizon scope-selection governance, `run roadmap --reason "scheduled"` bypass pattern, `Specs_Index.md` STEP 7 maintenance lapse) — none has a direct Sprint Planning action. No changes made to this routine as a result.

## Deferred Items

None. All 12 EPICs / ST items are within confirmed capacity (~19.0 days vs ~24-28 day ceiling, ~68-79% utilisation) and all 5 conditionally-gated EPICs (EPIC-01/03/04/05/06) cleared the Design Gate with 0 blocked. Full backlog slice enters the sprint.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-03 | ST-04 (shared file: `docs/specs/frontend/design_system.md`) | Internal (soft — sequencing only) | Resolved — merge order below |
| ST-05 | ST-01 (shared files: `docs/reference/openapi.yaml`, `docs/specs/api_contracts/*.md`, `backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js`) | Internal (soft — sequencing only) | Resolved — merge order below |
| ST-06 | ST-05 (same shared files as above) | Internal (soft — sequencing only) | Resolved — merge order below |
| ST-11 | RISK-03 — Head of Engineering pilot-endpoint confirmation | External (human decision) | Open — must resolve before EPIC-11 implementation begins; does not block sprint seal |
| ST-01 / ST-05 / ST-06 | New backend endpoint/aggregation (not yet built) + same-commit API contract entry (CLAUDE.md §2) | Spec | Resolved — same-commit requirement carried into sprint backlog Notes for each story |

No circular dependencies identified.

## Execution Sequence

Ordered to respect shared-file ownership and to unblock the (fully autonomous) items first, per STEP 5.2 grouping guidance:

1. EPIC-04 — Dark-mode contrast audit (owns `docs/specs/frontend/design_system.md`)
2. EPIC-03 — Accessibility pass, notification UX (rebases onto EPIC-04's `design_system.md` changes)
3. EPIC-09 — Shared retry/backoff decorator (independent)
4. EPIC-07 — API key rotation-and-audit cadence (independent, no code)
5. EPIC-08 — Rate-limiting review, public endpoints (independent)
6. EPIC-12 — API contract heading-level CI lint (independent)
7. EPIC-10 — Flaky-test quarantine process (independent)
8. EPIC-02 — Telegram changelog digest (independent)
9. EPIC-01 — In-app "what's new" panel (owns `openapi.yaml`, `docs/specs/api_contracts/*.md`, `backend/routers/test.py`, `SystemStatus.js`, `system-status.spec.js` for this cluster)
10. EPIC-05 — Monthly CSV export (rebases onto EPIC-01's shared-file changes before adding its own endpoint)
11. EPIC-06 — AI spend trend chart (rebases onto EPIC-05's shared-file changes before adding its own endpoint)
12. EPIC-11 — Pilot contract tests (sequenced last; gated on RISK-03 confirmation, otherwise independent of the EPIC-01/05/06 cluster)

**Multi-EPIC Execution Notes (Required — 12 EPICs in scope):**

- **`execution_state.json` owner:** EPIC-04 (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.
- **Shared file ownership advisory:**

| Shared file | Owning EPIC (merges first) | Later EPICs that must rebase |
|---|---|---|
| `docs/specs/frontend/design_system.md` | EPIC-04 | EPIC-03 |
| `docs/reference/openapi.yaml` | EPIC-01 | EPIC-05, EPIC-06 |
| `docs/specs/api_contracts/*.md` | EPIC-01 | EPIC-05, EPIC-06 |
| `backend/routers/test.py` | EPIC-01 | EPIC-05, EPIC-06 |
| `src/pages/SystemStatus.js` (endpoint-count fallback, CLAUDE.md §2) | EPIC-01 | EPIC-05, EPIC-06 |
| `tests/e2e/system-status.spec.js` (`SC-SS-01b`, CLAUDE.md §2) | EPIC-01 | EPIC-05, EPIC-06 |

Each of EPIC-05 and EPIC-06 must rebase onto `main` after the preceding EPIC in this cluster merges, and increment (not overwrite) the `SystemStatus.js` fallback count and `SC-SS-01b` expected value from whatever the prior EPIC left them at.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01/03/04/05/06 | Materialised and resolved — Design Gate ran and Passed this cycle (12/12 cleared, 0 blocked); no longer a live risk for execution |
| RISK-02 | EPIC-09 | Valid — mitigation (bounded to highest-traffic call site as proof-of-pattern) unchanged since release planning |
| RISK-03 | EPIC-11 | Valid, not yet resolved — Head of Engineering confirmation of the 3 pilot endpoints (positions/trades/dashboard candidates) required before implementation begins; recorded as Outstanding Action below |
| RISK-04 | EPIC-08 | Valid — mitigation (remediate-or-accept-risk per endpoint, no open-ended scope) unchanged since release planning |

**LL-v2.2-SP-01 (Blocked-decision design artefact check):** EPIC-11 is classified `delegated_decision` (see `sprint_backlog.md`). No HoST design session or equivalent artefact exists for the RISK-03 endpoint-selection decision (design gate classified EPIC-11 "Design Pre-Approved" — no UX artefact expected, but no separate technical-decision record exists either). Advisory: a brief Head of Engineering confirmation of the 3 pilot endpoints should occur at sprint kickoff before EPIC-11 implementation begins.

## Pre-Sprint Vulnerability Scan

Unavailable — `pip-audit` is not installed in `backend/.venv`. Recommend installing (`backend/.venv/bin/pip install pip-audit`) and running before EPIC-09 (retry/backoff decorator, touches live external call sites — Yahoo Finance/Alpaca) begins execution. Advisory only — does not block sprint planning.

## Frontend Playwright / Staging-Evidence Advisory

EPIC-01, EPIC-03, EPIC-04, EPIC-05, EPIC-06 all carry observable, frontend-visible acceptance criteria (new panel, contrast/focus-state fixes, new export control, new chart). Per CLAUDE.md §2, each observable AC needs either Playwright coverage or a recorded human staging run before its PR opens; if any AC is deferred to post-merge staging, a backlog item must be filed first. None of the ACs in `stage4_backlog_slice.md` carry an explicit `[staging-only evidence]` tag, and Playwright feasibility was not separately confirmed at the Design Gate — confirm feasibility at each EPIC's kickoff.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Confirm 3 pilot endpoints for EPIC-11 (RISK-03) | Head of Engineering | No — blocks EPIC-11 kickoff, not sprint seal |
| Install and run `pip-audit` before EPIC-09 execution | Head of Engineering | No — advisory |
| Prompt change log gap: `sprint_planning_prompt.md` current v3.13, last logged transition v3.11→v3.12 — add a prepended row per CLAUDE.md §6 | Head of Specs Team | No — pre-existing gap, not introduced this session |
| File backlog item for `design_gate_prompt.md` STEP 5 root-pointer sync gap (see Design Gate / Lifecycle Note above) | Head of Specs Team | No — advisory |
| Confirm Playwright feasibility (or arrange staging sign-off) for each of EPIC-01/03/04/05/06's observable ACs at kickoff | Director of Quality | No — execution-time responsibility per CLAUDE.md §2 |

No outstanding action is marked `Blocker? Yes`.
