**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-20
**Cycle:** 2026-07-20__release-v7.6

# Sprint Planning Notes — 2026-07-20__release-v7.6

## Backlog Slice Source

Original — `claude/cycles/2026-07-20__release-v7.6/stage4_backlog_slice.md` (`amended_backlog_slice_path` is empty for this cycle; the file itself was amended in-place by the PO-directed post-publish reopen, DL-073, before Sprint Planning ran — no separate amendment-cycle artefact exists or is required for this).

## Carry-Forward Items

Reviewed 2 items from `claude/cycles/2026-07-17__release-v7.5/lessons_learnt_closure.md` (most recently `post_ship_complete` cycle):

| # | Observation | Applied this cycle |
|---|-------------|---------------------|
| 1 | Two consecutive multi-EPIC sprints hit the same shared-file cross-EPIC merge-conflict pattern (`backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js`, `docs/specs/data_model.md`, `docs/ops/api_performance_baseline.md`, `docs/reference/openapi.yaml`) when ≥3 EPICs each register new endpoints. | This sprint has 8 EPICs, but only EPIC-07 is plausibly at risk of adding a new endpoint (to expose a combined cost figure) — see Shared File Ownership Advisory below. EPIC-04's error-envelope standardisation is flagged separately as the dominant shared-file risk this sprint (broad edits across nearly all router files, not a new-endpoint collision). |
| 2 | `SystemStatus.js` `categorizeEndpoint()` lacks branches for v7.5's new path prefixes (`/price-alerts`, `/saved-filters`) — not a hard gate, degrades gracefully to `'Other'`. | Not in this sprint's scope; not actioned here. Still open — candidate for a future frontend housekeeping story. |

## Deferred Items

None. All 8 items in `stage4_backlog_slice.md` are `include`.

| Item | Reason | Next Sprint Candidate? |
|------|--------|------------------------|
| — | — | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 (EPIC-02) | ST-01 (EPIC-01) | Internal | Unresolved until EPIC-01 merges — ST-02's AC requires cross-referencing "the corresponding Playwright spec file(s)" for the new print/export interaction surface, which does not exist until ST-01 is implemented |
| ST-01, ST-03, ST-04, ST-05, ST-06, ST-07, ST-08 | None | — | N/A — standalone per `release_plan.md ## Execution Plan` |

No circular dependencies.

## Execution Sequence

1. **EPIC-01** (ST-01, `BLG-FE-119`) — anchor; no dependencies; `execution_state.json` owner (designated below)
2. **EPIC-04** (ST-04, `BLG-BE-65`) — sequenced early: touches nearly every file in `backend/routers/`; later EPICs should not need to rebase router-file edits onto a standard that lands after their own work
3. **EPIC-02** (ST-02, `BLG-QA-112`) — depends on EPIC-01
4. **EPIC-03** (ST-03, `BLG-FEAT-79`)
5. **EPIC-05** (ST-05, `BLG-QA-114`)
6. **EPIC-06** (ST-06, `BLG-BE-62`)
7. **EPIC-07** (ST-07, `BLG-FEAT-77`) — sequenced after EPIC-04 in case it introduces a new backend endpoint (see Shared File Ownership Advisory), so any new endpoint conforms to the freshly-merged error envelope standard
8. **EPIC-08** (ST-08, `BLG-QA-69`) — sequenced after EPIC-04 to avoid the regression suite being written against pre-standardisation error shapes in `signal_service.py` / `database.py` / `ai_service.py`

### Multi-EPIC Execution Notes (Required — 8 EPICs in scope)

**`execution_state.json` owner: EPIC-01** (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite. Apply `shared_standards.md §12` (Parallel EPIC Branch Merge Sequencing) for merge order and conflict resolution if any branches run concurrently.

### Shared File Ownership Advisory (Required — 8 EPICs in scope)

- **`backend/routers/*.py` (broad):** EPIC-04 is the canonical owner of the error-response envelope standard this sprint — it will touch the majority of router files to audit/document (and, where trivial, correct) response shapes. Any other EPIC modifying a router file after EPIC-04 merges must rebase onto `main` and conform to the newly-documented envelope in `backend_engineering_patterns.md`.
- **`backend/services/signal_service.py`, `database.py`, `ai_service.py`:** touched by both EPIC-04 (envelope audit, if any of these expose HTTP-facing error responses indirectly via routers) and EPIC-08 (new regression suite reading these same paths). EPIC-08 is sequenced after EPIC-04 to avoid writing tests against a response shape that changes underneath it.
- **Potential new-endpoint collision surface** (`backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js`, `docs/reference/openapi.yaml` — the pattern flagged by the v7.5 carry-forward advisory above): only **EPIC-07** is plausibly at risk of introducing a new endpoint (to expose a combined Gemini+Claude cost figure, if no existing read endpoint already covers this — to be confirmed at execution kickoff against `settings.md` v1.4 §6 and the existing `gemini_audit_log` / `POST /ai/check-daily-cost` surfaces). If EPIC-07 does add a new endpoint: per CLAUDE.md, the `docs/reference/openapi.yaml` entry, `docs/specs/api_contracts/` `## METHOD /path` heading, `backend/routers/test.py` registration, and the `SystemStatus.js`/`system-status.spec.js SC-SS-01b` fallback-count updates are all required in the same commit. No other EPIC in this sprint's scope is expected to touch this collision surface, so the ≥3-EPIC pattern from the carry-forward advisory is not expected to recur this sprint even if EPIC-07 does add an endpoint.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|------------------|--------------------|
| RISK-01 | EPIC-01, EPIC-07 | Valid — mitigation ("Design Gate pass before sprint planning") fully executed; `design_gate_status: Passed`, both items cleared. Remaining half of mitigation ("Playwright coverage or human staging sign-off required per AC at sprint execution") carried into STEP 4 AC drafting below — satisfied via Playwright coverage for both items, no staging-only AC identified for either. |
| RISK-02 | EPIC-02 | Valid — documentation-only, no gate dependency; unchanged. |
| RISK-03 | EPIC-03 | Valid — no UI surface, no gate dependency; unchanged. Note: this item's own AC requires a one-time production-data run — flagged `[staging-only evidence]` at STEP 4 (CI cannot execute a live production reconciliation), distinct from RISK-01's UI-staging concern. |
| RISK-04 | EPIC-04 | Valid — no UI surface, no gate dependency; unchanged. |
| RISK-05 | EPIC-05 | Valid — test infrastructure, no gate dependency; unchanged. |
| RISK-06 | EPIC-06 | Valid — audit/documentation, no gate dependency; unchanged. |
| RISK-08 | EPIC-08 | Valid — backend test suite, no gate dependency; unchanged. |

No risk has materialised since release planning (same-day cycle — no elapsed time for drift).

## Pre-Sprint Vulnerability Scan

`pip-audit` is not installed in this execution environment (`pip-audit -r backend/requirements.txt --format=json` failed to run — command not found). **Tool unavailable — advisory only, does not block sprint planning.** Recommend installing `pip-audit` before or at sprint execution kickoff; CI is unaffected (each GitHub Actions workflow installs `requirements.txt` fresh into its own runner, per `CLAUDE.md §9`).

## Pre-Sprint Backlog Advisory

No backlog items found with `Provisional-Target: Before v7.6 sprint planning` (`grep` against `claude/backlog/backlog.md` returned no matches).

## Hygiene Advisories (Non-Blocking)

Prompt change log gap check (`grep "\`claude/system/<filename>\`" prompt_change_log.md | head -1`, exact filename-column match) found 3 Class 6 prompts whose current header version exceeds their most recently logged transition target:

| File | Current version | Last logged target | Gap |
|------|------------------|---------------------|-----|
| `sprint_planning_prompt.md` | v3.13 | v3.12 | 1 version undocumented |
| `shared_standards.md` | v3.17 | v3.14 | 3 versions undocumented |
| `release_planning_prompt.md` | v2.42 | v2.41 | 1 version undocumented |

`design_gate_prompt.md` (v1.4) had no gap — current version matches its last logged target. These gaps are pre-existing (not introduced by this session) and are recorded here as advisory per STEP -1 point 7; they do not block this sprint's seal. Recommend a Head of Specs Team backfill pass on `prompt_change_log.md` for these three files.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|------------------------|
| Backfill `prompt_change_log.md` entries for `sprint_planning_prompt.md` (v3.13), `shared_standards.md` (v3.14→v3.17), `release_planning_prompt.md` (v2.42) | Head of Specs Team | No |
| Confirm at EPIC-07 execution kickoff whether a new backend endpoint is required for the consolidated cost view; if so, apply the same-commit OpenAPI/contract/test-registration requirements (CLAUDE.md §2) | FinOps & Resource Architect; Head of Engineering | No |
| `BLG-QA-115` (v7.5 staging sign-off, custom price alert live delivery) remains open — unrelated to this sprint's scope, not actioned here | Director of Quality | No |

No outstanding action is marked `Blocker? Yes`.
