**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-23
**Cycle:** 2026-07-21__release-v7.7

# Sprint Planning Notes — 2026-07-21__release-v7.7

## Backlog Slice Source

Original — `claude/cycles/2026-07-21__release-v7.7/stage4_backlog_slice.md` (`amended_backlog_slice_path` is empty for this cycle; no amendment cycle has run).

## Carry-Forward Items

Reviewed 2 items from `claude/cycles/2026-07-20__release-v7.6/lessons_learnt_closure.md` (most recently `post_ship_complete` cycle):

| # | Observation | Applied this cycle |
|---|-------------|---------------------|
| 1 | Three consecutive cycles have needed an ad hoc PO-directed bypass for a routine, non-emergency, same-session scope change on an already-Published/formalized cycle — no governed engine currently accepts this class of request. Implication targets Release Planning. | Not applicable at Sprint Planning — this cycle's release plan was Published cleanly with no post-publish reopen (`state.json` shows a single `Published` transition, `mutation_seq: 0`). Noted for awareness only; no action required here. |
| 2 | The empty-Now-horizon roadmap formalization direct-write pattern needs a distinct confirmation step for the scope-selection case vs. pure relabel. Implication targets Roadmap. | Not applicable at Sprint Planning — out of this engine's scope. |

## Scope Selection and Delegation Classification (STEP 3)

All 11 items in the authoritative backlog slice are classified `include` — within confirmed capacity (~19.5 of ~24–28 days), each has a named owner in `release_plan.md ## Execution Plan`, and none is blocked by an unresolved dependency or escalation. No items classified `defer` or `flag`.

**Delegation class: `autonomous` for all 11 items.** This mirrors the prior cycle's own outcome (`2026-07-20__release-v7.6`: 8/8 autonomous) and reflects that:
- The 4 design-gated items (EPIC-01–04) each have a locked frontend spec and a Head of UX & Design-confirmed design artefact from `design_gate.md` — satisfying `BLG-GOV-72` fast-path (c) ("new section/component against a locked spec where Playwright feasibility has been confirmed").
- The 7 non-UI items (EPIC-05–11) are backend/CI/governance-review work with fully specified, engine-executable ACs. Named role sign-offs (e.g. EPIC-07's "Sign-off recorded by Head of Specs Team") sit in the Verification field, not the delegation class — per the `2026-07-20__release-v7.6` EPIC-08 precedent (a named-sign-off AC was still classified `autonomous`).
- Two items carry a sub-decision or a staging-only AC (EPIC-01's `compliance_rate` sourcing formula; EPIC-03's staging light-theme check) — both are handled as an Outstanding Action / `[staging-only evidence]` flag respectively, not as a delegation-class override, per the same v7.6 precedent (EPIC-03's production-reconciliation run and EPIC-07's endpoint-decision were both `autonomous` with an outstanding action attached).

No `delegated_frontend`/`delegated_backend`/`delegated_qa`/`delegated_decision` override was applied. No EPIC introduces a new page or new user-facing controls under a `delegated_frontend` classification, so `LL-v2.0-P4-2` (test-scenario-gap `execution_state.json` flag) does not apply this cycle. No item is classified `delegated_decision`, so `LL-v2.2-SP-01` (HoST design-artefact check) does not apply this cycle.

## Deferred Items

None. All 11 items in `stage4_backlog_slice.md` are `include`.

| Item | Reason | Next Sprint Candidate? |
|------|--------|------------------------|
| — | — | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-10 (EPIC-10) | ST-09 (EPIC-09) | Internal | Unresolved until EPIC-09 merges — `stage4_backlog_slice.md`/`release_plan.md` state EPIC-10 is "After EPIC-09" (monitoring/alerting for the nightly backtest job should observe the idempotency-audited version of the job, not a pre-audit baseline) |
| ST-02 (EPIC-02) | ST-01 (EPIC-01) | Shared-file (soft) | Not a hard AC dependency, but both touch `docs/reference/openapi.yaml` / `docs/specs/api_contracts/` — see Shared File Ownership Advisory below |
| ST-01, ST-03, ST-04, ST-05, ST-06, ST-07, ST-08, ST-09, ST-11 | None | — | N/A — standalone per `release_plan.md ## Execution Plan` |

No circular dependencies.

## Execution Sequence

1. **EPIC-01** (ST-01, `BLG-FEAT-75`) — design-gated; sequenced first per `stage4_backlog_slice.md`'s own sequencing note (largest effort, H >5d); `execution_state.json` owner (designated below)
2. **EPIC-02** (ST-02, `BLG-FE-114`) — design-gated; sequenced after EPIC-01 so its own `openapi.yaml`/contract touch rebases cleanly onto EPIC-01's (see Shared File Ownership Advisory)
3. **EPIC-03** (ST-03, `BLG-FE-113`) — design-gated; standalone
4. **EPIC-04** (ST-04, `BLG-FE-120`) — design-gated; standalone; sole owner of `design_system.md` this sprint
5. **EPIC-06** (ST-06, `BLG-OPS-108`) — P1, no Design Gate dependency, no cross-item dependency
6. **EPIC-07** (ST-07, `BLG-GOV-28`) — P1, no Design Gate dependency, no cross-item dependency
7. **EPIC-09** (ST-09, `BLG-BE-63`) — no Design Gate dependency; must precede EPIC-10
8. **EPIC-10** (ST-10, `BLG-OPS-110`) — depends on EPIC-09 (see Dependency Map)
9. **EPIC-05** (ST-05, `BLG-FEAT-80`) — investigation-only, no Design Gate dependency, no cross-item dependency
10. **EPIC-08** (ST-08, `BLG-QA-104`) — no Design Gate dependency, no cross-item dependency
11. **EPIC-11** (ST-11, `BLG-QA-102`) — no Design Gate dependency, no cross-item dependency; standing CI lint step, sequenced last as a housekeeping capstone

### Multi-EPIC Execution Notes (Required — 11 EPICs in scope)

**`execution_state.json` owner: EPIC-01** (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite. Apply `shared_standards.md §12` (Parallel EPIC Branch Merge Sequencing) for merge order and conflict resolution if any branches run concurrently.

### Shared File Ownership Advisory (Required — 11 EPICs in scope)

- **`docs/reference/openapi.yaml` / `docs/specs/api_contracts/*`:** EPIC-01 (adds `compliance_rate` to `strategy_version_comparison_contract.md`, 0.1.0→0.2.0, per the API contract gap flagged in `design_gate.md`) and EPIC-02 (adds `since_days`/`read` optional query params to the Notification Feed endpoint in `alerts_endpoints.md`) both touch API contract documentation and `openapi.yaml` this sprint. EPIC-01 is sequenced first; EPIC-02 must rebase onto `main` after EPIC-01 merges before finalising its own `openapi.yaml` diff, per CLAUDE.md §8 conflict-resolution convention.
- **`design_system.md`:** EPIC-04 is the sole owner this sprint (Standing Alert component transcription, target v1.2→v1.3, per the v7.5 command-palette precedent noted in `design_gate.md`). No other EPIC touches this file.
- **Nightly backtest job surface (backend service + CI trigger):** EPIC-09 (idempotency audit, sole owner) and EPIC-10 (monitoring/alerting, consumes EPIC-09's findings) share this surface — sequenced via the hard dependency above, not merely an advisory.
- **`SystemStatus.js` / `quality_gate.yml`:** EPIC-11 is the sole owner of the new drift-check lint step itself. Per CLAUDE.md §2, if any other EPIC in this sprint adds a new backend route, that EPIC's own commit (not EPIC-11's) must update `SystemStatus.js`'s hardcoded fallback count and `SC-SS-01b` in `tests/e2e/system-status.spec.js` — flagged here so it is not missed if EPIC-01 or EPIC-02 end up requiring a new endpoint (see Outstanding Actions).

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|------------------|--------------------|
| RISK-01 | EPIC-01 | Valid — mitigation ("sequence first; confirm a bounded MVP slice before any stretch scope") executed at STEP 3: MVP slice confirmed as win rate / average R / compliance rate compare only, no stretch scope, per `stage4_backlog_slice.md` ST-01 AC. |
| RISK-02 | EPIC-01, EPIC-02, EPIC-03, EPIC-04 | Valid — mitigation ("Design Gate must run and PASS before `plan sprint`") fully executed; `design_gate_status: Passed`, all 4 items cleared. |
| RISK-03 | EPIC-04 | Valid — no mitigation required this cycle per release plan; unchanged. |
| RISK-04 | Release-level | Valid — `stage4_backlog_slice.md` used as the sole authoritative scope source throughout this routine, not the roadmap anchor list; `BLG-FEAT-73`/`BLG-FEAT-74` correctly excluded from this sprint. |

No risk has materialised since release planning (same-session cycle — no elapsed time for drift).

## Pre-Sprint Vulnerability Scan

`pip-audit` is not installed in this execution environment (`pip-audit -r backend/requirements.txt --format=json` failed — command not found, and no `backend/.venv` present). **Tool unavailable — advisory only, does not block sprint planning.** Recommend installing `pip-audit` before or at sprint execution kickoff; CI is unaffected (each GitHub Actions workflow installs `requirements.txt` fresh into its own runner, per CLAUDE.md §9).

## Pre-Sprint Backlog Advisory

No backlog items found with `Provisional-Target: Before v7.7 sprint planning` (`grep` against `claude/backlog/backlog.md` returned no matches).

## Hygiene Advisories (Non-Blocking)

Prompt change log gap check (`grep "\`claude/system/<filename>\`" prompt_change_log.md | head -1`, exact filename-column match) found 3 Class 6 prompts whose current header version exceeds their most recently logged transition target:

| File | Current version | Last logged target | Gap |
|------|------------------|---------------------|-----|
| `sprint_planning_prompt.md` | v3.13 | v3.12 | 1 version undocumented |
| `shared_standards.md` | v3.18 | v3.14 | 4 versions undocumented (grew from 3 at last cycle's check — no backfill has occurred since) |
| `release_planning_prompt.md` | v2.42 | v2.41 | 1 version undocumented |

`design_gate_prompt.md` (v1.4) had no gap — current version matches its last logged target. These gaps are pre-existing (not introduced by this session), carried forward unchanged from `2026-07-20__release-v7.6`'s own sprint planning notes (`shared_standards.md`'s gap has widened by one version since). Recorded as advisory per STEP -1 point 7; they do not block this sprint's seal.

**Lifecycle Guard wording note (advisory, non-blocking):** `sprint_planning_prompt.md` STEP -1 Hard Gate 1's literal text ("status must be Published, Validated, or Committed") does not enumerate `Design_Gate_Passed` as an allowed value, even though `shared_standards.md §10.1` (the authoritative lifecycle guard table, which this prompt's own §2 Invocation Rule and the STEP -1 heading both defer to) explicitly lists `Design_Gate_Passed` as a valid from-state for `plan sprint`. This session entered from `.claude_current_state.json` status `Design_Gate_Passed` and proceeded on the authority of §10.1 per its own precedence rule ("in any conflict, `lifecycle_schema.json` prevails" / §10 is authoritative over the human-readable prose in this prompt body). Recommend a Head of Specs Team pass to update STEP -1 Hard Gate 1's prose to match §10.1 now that Design Gate is a standing phase between Release Planning and Sprint Planning.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|------------------------|
| Confirm `compliance_rate` sourcing formula (journal-completion-rate vs. Arc 5 composite score) for `strategy_version_comparison_contract.md` 0.1.0→0.2.0, before/during EPIC-01 execution | Strategy Rules & System Intent Owner | No |
| Confirm at EPIC-01/EPIC-02 execution kickoff whether either item requires a genuinely new backend endpoint (vs. additive fields/params on existing endpoints); if so, apply the same-commit OpenAPI/contract/`backend/routers/test.py`/`SystemStatus.js` fallback-count requirements (CLAUDE.md §2) | Head of Engineering | No |
| Backfill `prompt_change_log.md` entries for `sprint_planning_prompt.md` (v3.13), `shared_standards.md` (v3.14→v3.18), `release_planning_prompt.md` (v2.42) | Head of Specs Team | No |
| Update `sprint_planning_prompt.md` STEP -1 Hard Gate 1 prose to enumerate `Design_Gate_Passed` explicitly, matching `shared_standards.md §10.1` | Head of Specs Team | No |

No outstanding action is marked `Blocker? Yes`.
