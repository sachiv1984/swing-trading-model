# Sprint Planning Notes — 2026-10-29__release-v9.14

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-29
**Cycle:** 2026-10-29__release-v9.14

## Backlog Slice Source

Original: `claude/cycles/2026-10-29__release-v9.14/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-03, ST-04 and ST-05). `amended_backlog_slice_path` is empty: no amendment.

## Preflight Summary (STEP -1)

- **Lifecycle guard:** `status = Design_Gate_Passed`, a valid Sprint Planning entry state. Not `Amendment_In_Progress`.
- **Release plan:** `state.json` has `status = Published`, `publish_eligible = true`, empty `open_escalations` and empty `deferred_execution_blockers`.
- **Design gate:** `design_gate_required = true`, `design_gate_status = Passed` (`design_gate.md`, 2026-10-29T13:11:54Z). 54 cleared, 0 blocked. The bypass audit was skipped (entered from `Design_Gate_Passed`).
- **Files, roles and write access:** the slice has 7 EPICs and 54 ST items. Every §5 input is present; the capacity check is in `release_plan.md ## Capacity Check` (schema v2), outcome `pass`. All five §4 role files are present, and `lessons_learnt_prompt.md` exists. The `.write_test` file was created and removed.
- **Root escalations:** every `.claude_current_state.json` `open_escalations` entry is Resolved.
- **Branch:** `main`.

## Hygiene Advisories (STEP -1.7, -1.8)

- **Prompt change log gaps (date-scan method):** none. Every Class 6 prompt's current `**Version:**` matches its latest-dated `prompt_change_log.md` row. `agent_onboarding_runbook.md` and `invariants.md` (both v1.0) have no row, which is informational only: there is no later version to compare.
- **Endpoint test coverage audit:** `scripts/audit_endpoint_test_coverage.py` exited 0 with 95 route decorators across 27 router files and 8 documented `KNOWN_GAPS`. Pre-sprint endpoint coverage audit: clean.

## Carry-Forward Items

Carry-forward items reviewed: 4 items from cycle `2026-10-16__release-v9.13`.
1. `next_release` / roadmap "Next planned release": answered at Release Planning (DL-087 named v9.14).
2. Human confirmation of the v9.13 DoQ and PO sign-offs: confirmed 2026-10-29 (closure outstanding actions rows 1–5).
3. The `BLG-BE-190` `strategy_rules.md` write route: answered by `ESC-CLOSE-20261029-02` case (c). ST-09's line is confirmed at this seal.
4. The STEP 6.2 post-merge AC check: **applied at this seal** (first application). Six stories carry post-merge ACs, each with a named tracking item (see Staging-Only and Post-Merge ACs).

## Pre-Sprint Required Decisions (STEP -1.5)

| Decision | Status | Resolution |
|----------|--------|-----------|
| RISK-02: Strategy Rules & System Intent Owner confirmation of the three case (c) `strategy_rules.md` AC lines (ST-03 §4.2.1/§8.2, conditional; ST-09 §4.1.5 and §4.1.3 if ambiguous; ST-22 §13.5 roster row) | **Resolved** | All three confirmed by the user acting with the Strategy Rules & System Intent Owner, 2026-10-29. Each confirmation is dated in `sprint_backlog.md` § Named-file writes. |

## Pre-Sprint Backlog Advisory

No `backlog.md` item carries `Provisional-Target: Before v9.14 sprint planning`.

## Pre-Seal Stale-Feature-Target Check (STEP 3.1)

- **ST-51 (`BLG-GOV-185`): flagged as already met.** `docs/specs/metrics_definitions.md` (v1.33.0) has `## Appendix D — Change Log`, with rows to v1.33.0 (2026-10-27). The source item (filed 2026-07-08) predates the table, as the design gate's observation noted. **Product Owner decision, 2026-10-29: defer at planning as already met.** The 0.50d moved to ST-03. ST-48's "after ST-51" dependency is void, and ST-48 writes its row to Appendix D. Close `BLG-GOV-185` at the next `groom backlog`.
- No other candidate targets a feature already shipped on `main`. ST-38 and ST-39's gates were verified at Release Planning (`run_manifest.md` §1.3a).

## Named-File Write Check (STEP 3.1)

- Named-file write: `claude/strategy/strategy_rules.md` §4.2.1 and/or §8.2 (regime-unknown behaviour, conditional on the ruling) — authorised under execution_prompt.md §7 named-file rule, case (c) (ST-03). Strategy Rules & System Intent Owner confirmed, 2026-10-29. The determination itself is ST-03's `delegated_decision` first sub-step; the write records it.
- Named-file write: `claude/strategy/strategy_rules.md` §4.1.5 Known Deviation for `BLG-BE-190` closed; §4.1.3 US formula if ambiguous — authorised under execution_prompt.md §7 named-file rule, case (c) (ST-09). Strategy Rules & System Intent Owner confirmed, 2026-10-29.
- Named-file write: `claude/strategy/strategy_rules.md` §13.5 "Gemini thesis generation" roster row — authorised under execution_prompt.md §7 named-file rule, case (c) (ST-22). Strategy Rules & System Intent Owner confirmed, 2026-10-29.

There are no `claude/roadmap/*` writes. ST-53's link to the next rebalance is recorded as a closure carry-forward, not a roadmap write. No existing `backlog.md` item is edited.

**Governance prompt edits (outside the named-file rule):** ST-44 (`execution_prompt.md` §9.2) and ST-45 (`release_planning_prompt.md` §1.3a or `backlog_management_prompt.md`) are governance changes made as sprint story execution under CLAUDE.md §6.

**Planning-time backlog writes (STEP 6.2):** six new tracking items were added via `/backlog-add` on the user's instruction (2026-10-29): BLG-OPS-200, BLG-GOV-399, BLG-OPS-201, BLG-OPS-202, BLG-SEC-44 and BLG-GOV-400. These are new items only. `check_backlog_item_integrity.py` passed. §6's write scope lists no `backlog.md` path, but §6.2's post-merge rule requires filing before seal. This was surfaced to the user, who authorised it, and it is recorded here as a prompt observation for post-ship closure: §6 should name the new-item exception.

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| ST-51 (`BLG-GOV-185`) | Already met (Appendix D change log exists); Product Owner, 2026-10-29. `deferred_at_planning` | No. Close at `groom backlog` |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-03 | ST-02 | Internal (same function) | Open, sequenced |
| ST-03 | Strategy Rules & System Intent Owner ruling | Decision (first sub-step) | Raise at sprint start |
| ST-05 | ST-04 | Internal (stored rate, source, age) | Open, sequenced |
| ST-06 | ST-03, ST-04 | Internal (fallback signals) | Open, sequenced |
| ST-08 | ST-07 | Internal (marker) | Open, sequenced |
| ST-09 | Strategy Rules & System Intent Owner FX confirmation | Decision (first sub-step) | Raise at sprint start |
| ST-13 | ST-09 | Internal (convention) | Open, sequenced |
| ST-29 | ST-10 | Cross-EPIC (EPIC-02 → EPIC-05) | Open; merge order enforces |
| ST-30 | ST-01 | Cross-EPIC (EPIC-01 → EPIC-05), plus a human staging pass | Open; merge order enforces |
| ST-15 | AI Compliance & Governance Officer ruling extension | Decision (first sub-step) | Raise at sprint start |
| ST-18 | ST-15 | Internal (shared test-suite doc) | Open, sequenced |
| ST-17 | ST-16; AI Compliance & Governance Officer ruling amendment | Internal + Decision | Open, sequenced |
| ST-17 | ST-20 | Internal (formatter; ST-20 first or rebase) | Open, sequenced |
| ST-21 | ST-19 | Internal (audit writes) | Open, sequenced |
| ST-22 ↔ ST-28 | — | Cross-EPIC coordination (`SystemStatus.js`, `system-status.spec.js`) | EPIC-03 merges first; EPIC-04 rebases |
| ST-23 | ST-15–ST-18; production credential | Internal + External | Human-Delegation at sprint start |
| ST-27 | ST-26 | Internal (same card) | Open, sequenced |
| ST-36 | ST-32 | Internal (`tests/conftest.py`) | Open, sequenced |
| ST-39 | ST-38; production cost data | Internal + External | Human-Delegation |
| ST-42 | Run on `main` | External (post-merge) | BLG-OPS-202 |
| ST-43 | Render environment variable | External | Human-Delegation |
| ST-01 | Render dashboard access | External | Human-Delegation |
| ST-45 | ST-44; Head of Specs Team option choice | Internal + Decision | Open, sequenced |
| ST-48 | ST-24 (`metrics_definitions.md`) | Cross-EPIC (EPIC-04 → EPIC-07) | Merge order enforces; the ST-51 dependency is void |

Spec dependencies: every Design Required story has its decision record and frontend spec locked at the design gate (`design_gate.md`). No circular dependency.

## Execution Sequence

1. **EPIC-01:** ST-01 (first in sprint; raise the Render delegation) → ST-02 → ST-03 (ruling first) → ST-04 → ST-05 → ST-06 → ST-07 → ST-08
2. **EPIC-02:** ST-09 (confirmation first) → ST-13; ST-10, ST-11, ST-12, ST-14 independent
3. **EPIC-06:** ST-38 → ST-39 (delegation); ST-40, ST-41, ST-42, ST-43 independent (ST-42 and ST-43 delegations raised at start)
4. **EPIC-03:** ST-15 (ruling) → ST-18; ST-16 → ST-20 → ST-17 (ruling); ST-19 → ST-21; ST-22; ST-23 last (delegation)
5. **EPIC-04:** ST-24 → ST-25; ST-26 → ST-27; ST-28 (after rebasing on ST-22)
6. **EPIC-07:** ST-44 → ST-45 (option choice); ST-46, ST-47, ST-48, ST-49, ST-50, ST-52, ST-53, ST-54 independent
7. **EPIC-05:** ST-31 (first on the branch) → ST-29 (after ST-10 is on `main`), ST-32 → ST-36 (late), ST-33, ST-34, ST-35, ST-37; ST-30 after ST-01 is deployed (delegation)

Raise all rulings (ST-03, ST-09, ST-15, ST-17, ST-45) and Human-Delegations (ST-01, ST-23, ST-30, ST-39, ST-42, ST-43) at sprint start, so they resolve while the autonomous items run.

## Multi-EPIC Execution Notes

`execution_state.json` owner: **EPIC-01** (first in execution order). Every other EPIC branch checks for `claude/cycles/2026-10-29__release-v9.14/execution_state.json` before creating it. If it exists, the branch reads it and appends its own EPIC section; it never overwrites. At initialisation, add `epics.EPIC-07.stories.ST-51: {status: deferred_at_planning, gate_condition: "AC already met by metrics_definitions.md Appendix D — Change Log; Product Owner, 2026-10-29"}` (STEP 5.2 traceability).

## Shared-File Ownership Advisory

| Shared file | EPICs / stories | Owner EPIC | Rule |
|-------------|----------------|-----------|------|
| `claude/strategy/strategy_rules.md`, `backend/strategy_version_registry.py` | EPIC-01 ST-03 (conditional), EPIC-02 ST-09, EPIC-03 ST-22 | EPIC-01 | Case (c) writes. Bumps in merge order; the later branch takes the next free version. CLAUDE.md §8 step 2a, checked per file |
| `docs/reference/openapi.yaml`, `api_changelog.md` | EPIC-01 ST-03/04/05/07, EPIC-02 ST-10, EPIC-03 ST-22, EPIC-04 ST-24 | EPIC-01 | Same commit as each contract. Union of additions; highest version |
| `backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js` (`SC-SS-01b`) | EPIC-03 ST-22, EPIC-04 ST-28 | EPIC-03 | EPIC-04 rebases and recomputes the fallback count from the merged `test.py` |
| `docs/specs/metrics_definitions.md` | EPIC-04 ST-24, EPIC-07 ST-48 (ST-50 reads) | EPIC-04 | §8 step 2a version check; one Appendix D row per change |
| `docs/specs/frontend/risk_dashboard.md` | EPIC-01 ST-05/ST-08 (read v0.1.14), EPIC-07 ST-47 (edit) | EPIC-07 | ST-47 bumps to v0.1.15+ |
| `backend/services/position_service.py`, portfolio and market services | EPIC-01 ST-02 to ST-07, EPIC-02 ST-09, ST-12 | EPIC-01 | EPIC-02 rebases after EPIC-01 merges |
| `backend/services/ai_service.py`, `ai_s13_boundary_test_suite.md` | EPIC-03 ST-15 to ST-20 | EPIC-03 | In-EPIC order |
| `OPERATIONAL_GUIDE.md`, `prompt_change_log.md`, governance prompts | EPIC-07 ST-44, ST-45 | EPIC-07 | CLAUDE.md §6 checklist; §8 step 2a per co-bumped file |
| `tests/conftest.py` | EPIC-05 ST-32, ST-36 | EPIC-05 | ST-32 first |
| `claude/backlog/backlog.md` | Any (new items only) | — | `/backlog-add`; `check_backlog_item_integrity.py` after each §8 merge |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 ST-01; EPIC-03 ST-23; EPIC-05 ST-30; EPIC-06 ST-39, ST-42, ST-43 | Valid. Human-Delegations raised at sprint start; post-merge parts tracked (BLG-OPS-200, BLG-GOV-399, BLG-OPS-201, BLG-OPS-202, BLG-SEC-44) |
| RISK-02 | EPIC-01 ST-03, EPIC-02 ST-09, EPIC-03 ST-22 | **Resolved at seal.** All three lines confirmed, 2026-10-29. Version collision handled by merge order + §8 step 2a |
| RISK-03 | EPIC-01 ST-02 to ST-07 | Valid. One branch, fixed order; ST-05 reuses ST-04 |
| RISK-04 | EPIC-01, 02, 03, 04, 05, 07 shared files | Valid. Ownership table above; merge order EPIC-01 → 02 → 06 → 03 → 04 → 07 → 05 |
| RISK-05 | ST-03, ST-09, ST-15, ST-17, ST-45 | Valid. Each a first sub-step; the ST-09 fix is needed regardless; ST-45's options are pre-specified |
| RISK-06 | EPIC-01 ST-01 | Valid. The CI production-build step surfaces a second cause before merge; production AC post-merge (BLG-OPS-200) |

**Multi-vehicle fix-choice check (LP-14):** ST-45 (options (a) and (b)) and ST-14 (already chosen at the design gate: option (a)) are the only multi-vehicle items. ST-45's two options carry similar effort (XS, both a single prompt edit under §6). There is no Phasing Recommendation (capacity `pass`), so no capacity cross-reference is needed. ST-03's three ruling branches are all designed in the decision record, and the raised 1.00d covers the widest branch.

## Delegation Classification (set at planning time, per §12 invariant)

- **autonomous (42):** ST-02, ST-04 to ST-08, ST-10 to ST-14, ST-16, ST-18 to ST-22, ST-24 to ST-29, ST-31 to ST-38, ST-40, ST-41, ST-44, ST-46 to ST-50, ST-52 to ST-54. Frontend stories use the BLG-GOV-72 fast-path (c): each has a locked design record or a pre-approved locked spec from the design gate, and Playwright feasibility is named in its AC.
- **delegated_decision (5):** ST-03, ST-09 (Strategy Rules & System Intent Owner); ST-15, ST-17 (AI Compliance & Governance Officer); ST-45 (Head of Specs Team). LL-v2.2-SP-01 design artefact check: ST-03 has `market-regime-unknown/decision_record.md` (three ruling branches designed). ST-09 is Design Pre-Approved. ST-15 and ST-17 rest on existing rulings `ESC-EXEC-20261027-03`/`-01`, which they extend. ST-45's two options are pre-specified in `BLG-GOV-398`. No HoST session is needed.
- **delegated_backend (5):** ST-01 (Render dashboard), ST-23 (production credential), ST-39 (production cost data), ST-42 (run on `main`, possible branch-rule bypass), ST-43 (Render variable). Code and docs proceed autonomously in each.
- **delegated_qa (1):** ST-30 (human staging pass in both themes).
- **delegated_frontend:** none, so the LL-v2.0-P4-2 test-scenario note does not apply.

## Staging-Only and Post-Merge ACs (STEP 6.2)

| Story | AC | Kind | Tracking item |
|-------|----|------|---------------|
| ST-01 | AC 1 | post-merge | BLG-OPS-200 |
| ST-01 | AC 2 | staging-only (Render staging build) | Delegation; file before PR if deferred |
| ST-23 | AC 1 | post-merge / production data | BLG-GOV-399 |
| ST-30 | AC 1 | staging-only (human run) | Delegation; file before PR if deferred |
| ST-39 | AC 2 | post-merge / production data | BLG-OPS-201 |
| ST-42 | AC 1, AC 2 | post-merge | BLG-OPS-202 |
| ST-43 | AC 2 | staging-only + post-merge | BLG-SEC-44 |
| ST-45 | AC 2 | post-merge (next engine run) | BLG-GOV-400 |

The slice header lists "ST-43 AC 1", but the post-merge AC is AC 2, so AC 2 is marked. ST-42 and ST-45 were added at this check: the slice did not list them, but both can be met only after merge.

## Acceptance Criteria Confirmation and Director of Quality Readiness Check (STEP 4)

- **AC source:** every story's AC is in `stage4_backlog_slice.md` (restated where stale, marked *(restated)*), plus the addendum for ST-03/04/05. No AC was drafted at this step, and there are no `[AC REQUIRED]` placeholders. The Technical/Quality/Security/Verification fields are carried by the slice's AC lists and the design records' testability sections. Security is N/A for all stories except ST-43 (CORS allow-list, test of production configuration) and ST-22 (attack-surface reduction: an AI-calling endpoint is removed). The §13 clause-citation rule is in the ACs of ST-15, ST-17, ST-22, ST-23 and ST-52.
- **Head of Specs Team (agent-mediated, §5.3):** ACs confirmed testable and observable. Each UI AC names Playwright, or the FI-P3-02 exception (ST-26).
- **Director of Quality (agent-mediated, §5.3), per EPIC:** QA criteria are sufficient to produce `qa_evidence_EPIC-xx.md` for all 7 EPICs. Known extra Playwright assertions from the design records (ST-03, ST-04/05, ST-08, ST-11, ST-24) must be added or filed before the PR opens (CLAUDE.md §2). No blocking coverage gap.

## Pre-Sprint Vulnerability Scan

Pre-sprint pip-audit: clean. `backend/.venv/bin/pip-audit -r backend/requirements.txt --format=json` scanned 53 dependencies and found 0 vulnerabilities. The trend log row was appended to `docs/ops/pip_audit_trend_log.md`.

## Capacity Buffer Floor (STEP 1.5)

28.00 / 28.00 = 1.00 > 0.95. Buffer floor exceeded. Product Owner acknowledgement, 2026-10-29: proceed at the ceiling (single sprint, with ST-51 deferred and ST-03 raised to keep the total at 28.00).

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| RISK-02 confirmation of three case (c) lines | Strategy Rules & System Intent Owner | Yes. **Resolved 2026-10-29** |
| File tracking items for post-merge ACs | PMO Lead | Yes. **Done 2026-10-29** (six items) |
| Raise rulings at sprint start: ST-03, ST-09, ST-15, ST-17, ST-45 | Sprint Execution Engine | No |
| Raise Human-Delegations at sprint start: ST-01, ST-23, ST-30, ST-39, ST-42, ST-43 | Sprint Execution Engine | No |
| Initialise ST-51 `deferred_at_planning` in `execution_state.json` | Sprint Execution Engine | No |
| Close `BLG-GOV-185` as already met | Backlog Management (`groom backlog`) | No |
| Post-ship observation: §6 write scope should name the STEP 6.2 tracking-item filing exception for `backlog.md` | Head of Specs Team | No |
