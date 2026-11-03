# Sprint Planning Notes — 2026-11-03__release-v9.15

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-03
**Cycle:** 2026-11-03__release-v9.15

## Backlog Slice Source

Original: `claude/cycles/2026-11-03__release-v9.15/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-01 and ST-16). `amended_backlog_slice_path` is empty: no amendment.

## Preflight Summary (STEP -1)

- **Lifecycle guard:** `status = Design_Gate_Passed`, a valid Sprint Planning entry state. Not `Amendment_In_Progress`.
- **Release plan:** `state.json` has `status = Published`, `publish_eligible = true`, empty `open_escalations` and empty `deferred_execution_blockers`.
- **Design gate:** `attributes.design_gate_required = true`, `design_gate_status = Passed` (`design_gate.md`, 2026-11-03T15:39:57Z). 41 cleared, 4 conditionally cleared (ST-08 to ST-11), 0 blocked. The bypass audit was skipped (entered from `Design_Gate_Passed`).
- **Files, roles and write access:** the slice has 7 EPICs and 45 ST items. Every §5 input is present; the capacity check is in `release_plan.md ## Capacity Check` (schema v2), outcome `pass`. All five §4 role files are present, and `lessons_learnt_prompt.md` exists. The `.write_test` file was created and removed.
- **Root escalations:** `ESC-EXEC-20260910-01` remains Deferred (non-blocking; trigger tracked by `BLG-GOV-399`). Every other entry is Resolved.
- **Branch:** `main`.

## Hygiene Advisories (STEP -1.7, -1.8)

- **Prompt change log gaps (date-scan method):** none. Every Class 6 prompt's current `**Version:**` matches its highest-version row on its latest date in `prompt_change_log.md`. `decisions_record_template.md` and `scope_document_template.md` (both v1.0) have no row, which is informational only: there is no later version to compare.
- **Endpoint test coverage audit:** `scripts/audit_endpoint_test_coverage.py` exited 0 with 94 route decorators across 27 router files and 8 documented `KNOWN_GAPS`. Pre-sprint endpoint coverage audit: clean.

## Carry-Forward Items

Carry-forward items reviewed: 4 items from cycle `2026-10-29__release-v9.14`.
1. Run a rebalance before `plan release v9.15`: done (`2026-11-03__scheduled`, DL-088).
2. Weigh `BLG-FE-239`, `BLG-FE-240`, `BLG-FE-243` for v9.15: all three were seated (ST-15, ST-16, ST-04). ST-16 (`BLG-FE-240`) is now deferred at planning as superseded by ST-12, with the reason recorded (see Deferred Items).
3. `BLG-GOV-404` selection tier: seated by §1.4c step 1a (ST-37).
4. Post-merge remainders `BLG-OPS-201`, `BLG-GOV-399`, `BLG-GOV-400`: not in v9.15 scope except as noted; `BLG-GOV-400` is met per the release plan. Check them again at delivery verification.

## Pre-Sprint Required Decisions (STEP -1.5)

| Decision | Status | Resolution |
|----------|--------|-----------|
| RISK-03: Strategy Rules & System Intent Owner confirmation of ST-28 AC 3 (case (c) §13 write) | **Resolved** | Confirmed by the user acting as Strategy Rules & System Intent Owner, 2026-11-03. Dated in `sprint_backlog.md` § Named-file writes. |
| ST-01 Branch A case (c) line (addendum, "same treatment as RISK-03") | **Resolved** | Confirmed, 2026-11-03. The ruling itself remains ST-01's first sub-step. |
| ST-16 disposition (addendum: Product Owner decides at Sprint Planning) | **Resolved** | Deferred as superseded by ST-12 (Product Owner, 2026-11-03). |

## Pre-Sprint Backlog Advisory

No `backlog.md` item carries `Provisional-Target: Before v9.15 sprint planning`.

## Pre-Seal Stale-Feature-Target Check (STEP 3.1)

- No source item of the 45 stories is archived or bannered ✅ COMPLETE in `backlog.md`/`backlog_archive.md` (checked by script, 2026-11-03).
- **ST-16 (`BLG-FE-240`): flagged.** The target (Dashboard win-rate widgets) exists only on legacy `Dashboard.js`, which ST-12 deletes in this sprint (addendum). **Product Owner decision, 2026-11-03: defer at planning as superseded.**
- ST-12's Scope bullet 1 ("confirm `BLG-FE-240`'s fix belongs on `DashboardHome`") is answered by the addendum: there is no `DashboardHome` site.

## Named-File Write Check (STEP 3.1)

- Named-file write: `claude/strategy/strategy_rules.md` §13.1/§13.2 clarified text and/or §13.5 roster row (AI journal summary, conditional on the re-read) — authorised under execution_prompt.md §7 named-file rule, case (c) (ST-28). Strategy Rules & System Intent Owner confirmed, 2026-11-03.
- Named-file write: `claude/strategy/strategy_rules.md` §4.2.6 and/or §4.2.1 (acknowledgement vs hard submission gate; unknown-regime "are blocked" wording; conditional on Branch A) — authorised under execution_prompt.md §7 named-file rule, case (c) (ST-01). Strategy Rules & System Intent Owner confirmed, 2026-11-03.
- Named-file write: `claude/strategy/strategy_rules.md` Change Log row 1.15 Date → production deploy date (conditional on ST-20's ruling) — authorised under execution_prompt.md §7 named-file rule, case (c) (ST-20). Strategy Rules & System Intent Owner confirmed, 2026-11-03. Found at this check: the slice does not flag ST-20 as a `strategy_rules.md` write, but `tests/test_strategy_version_registry.py::test_registered_effective_dates_match_change_log` requires the Change Log date to match the registry's `effective_date`.
- Named-file write: `claude/backlog/backlog.md` `BLG-FE-240` Notes line (defect leaves with the legacy page) — authorised under execution_prompt.md §7 named-file rule (ST-12). Redrafted at planning from the slice's "update that item's scope note" so that it does not touch the `Scope` field.

There are no `claude/roadmap/*` writes: ST-44 and ST-45 leave `current_roadmap.md` §2 and `initiative_register.md` to the next `run roadmap` (BLG-GOV-408).

**Governance prompt edits (outside the named-file rule):** ST-37, ST-38, ST-43 and ST-44 may change governance prompts or `OPERATIONAL_GUIDE.md` as sprint story execution under CLAUDE.md §6.

**Planning-time backlog writes (STEP 6.2, user-authorised 2026-11-03):** five new items were added via `/backlog-add`: BLG-OPS-211, BLG-SPEC-217, BLG-GOV-408 (post-merge trackers for ST-31, ST-35, ST-45) and BLG-FE-267, BLG-FE-268 (the design gate's two "Observations for filing"). New items only. `check_backlog_item_integrity.py` passed. The v9.14 observation that §6's write scope should name this exception still applies.

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| ST-16 (`BLG-FE-240`) | Superseded by ST-12 (widgets leave with the legacy page); Product Owner, 2026-11-03. `deferred_at_planning` | No. Close at `groom backlog` once ST-12 ships |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | Strategy Rules & System Intent Owner ruling (§4.2.6) | Decision (first sub-step) | Raise at sprint start |
| ST-03 | ST-02 | Internal (same FX field) | Open, sequenced |
| ST-11 | ST-08 approval | Internal + Decision | Open, sequenced; returns not-ready if ST-08 is not approved |
| ST-08, ST-09, ST-10 | Head of UX & Design approval (Head of Specs Team for ST-09) | Decision (named sub-step) | Raise drafts early |
| ST-10 | Strategy Rules & System Intent Owner §13 confirmation | Decision | Coordinate with ST-28 |
| ST-17 | ST-06 (`positions.md`, Trail Stop modal) | Cross-EPIC (EPIC-01 → EPIC-03) | Merge order enforces |
| ST-42 | ST-17 (SC-TS-* assertions) | Cross-EPIC (EPIC-03 → EPIC-07) | Merge order enforces |
| ST-04 ↔ ST-12 | `Dashboard.js` | Cross-EPIC coordination | ST-12 deletes the file after EPIC-01 merges |
| ST-20 | Strategy Rules & System Intent Owner ruling | Decision (first sub-step) | Raise at sprint start |
| ST-23 | Data Model & Domain Schema Owner ruling | Decision (first sub-step) | Raise at sprint start |
| ST-24 | Production log read | External | Human-Delegation |
| ST-26 | ST-24 (`_NON_TICKER_WORDS`) | Internal (rebase) | Open, sequenced |
| ST-27 | ST-25 ruling | Internal + Decision | Open, sequenced |
| ST-28 | Strategy Rules & System Intent Owner re-read | Decision | Raise at sprint start |
| ST-29 | Anthropic console | External | Human-Delegation |
| ST-33 | 2026-11-09 and production read | External, date gate | Conditional |
| ST-35, ST-36 | Staging (and production for ST-35) access | External | Human-Delegation |
| ST-44, ST-45 | Strategy Rules & System Intent Owner / Product Owner decisions | Decision | Raise at sprint start |

The ST-16 → ST-12 dependency in the slice is void (ST-16 deferred). Spec dependencies: every Design Required story has its decision record or brief locked at the design gate; ST-08 to ST-10 produce their specs in-sprint (conditional clearance). No circular dependency.

## Execution Sequence

1. **EPIC-01:** ST-01 (raise ruling first) → ST-02 → ST-03; ST-04, ST-05, ST-06, ST-07 independent
2. **EPIC-03:** ST-15; ST-17 (after ST-06 on `main`); ST-18, ST-19, ST-21, ST-22 independent; ST-20 and ST-23 (rulings first)
3. **EPIC-02:** ST-08 (first; approval sub-step) → ST-11; ST-09, ST-10 in parallel; ST-12 → ST-13, ST-14
4. **EPIC-04:** ST-25 (ruling) → ST-27; ST-24 (delegation) → ST-26; ST-28 (re-read)
5. **EPIC-06:** ST-34; ST-35 and ST-36 in either order (delegations)
6. **EPIC-07:** ST-37, ST-38 early (deferred patches); ST-39, ST-40, ST-41, ST-43 independent; ST-42 after ST-17 is on `main`; ST-44, ST-45 (decisions)
7. **EPIC-05:** ST-30, ST-32 independent; ST-29 (delegation); ST-31 last on the branch; ST-33 only after its gate clears (2026-11-09)

Raise all rulings and approvals (ST-01, ST-08, ST-09, ST-10, ST-20, ST-23, ST-25, ST-28, ST-44, ST-45) and Human-Delegations (ST-24, ST-29, ST-35, ST-36; ST-33 from 2026-11-09) at sprint start, so they resolve while the autonomous items run.

## Multi-EPIC Execution Notes

`execution_state.json` owner: **EPIC-01** (first in execution order). Every other EPIC branch checks for `claude/cycles/2026-11-03__release-v9.15/execution_state.json` before creating it. If it exists, the branch reads it and appends its own EPIC section; it never overwrites. At initialisation, add `epics.EPIC-03.stories.ST-16: {status: deferred_at_planning, gate_condition: "Superseded by ST-12: both win-rate widgets exist only on legacy Dashboard.js, which ST-12 deletes; Product Owner, 2026-11-03"}` (STEP 5.2 traceability).

## Shared-File Ownership Advisory

| Shared file | EPICs / stories | Owner EPIC | Rule |
|-------------|----------------|-----------|------|
| `claude/strategy/strategy_rules.md`, `backend/strategy_version_registry.py` | EPIC-01 ST-01, EPIC-03 ST-20, EPIC-04 ST-28 (all conditional) | EPIC-01 | Case (c) writes. Bumps in merge order; the later branch takes the next free version. CLAUDE.md §8 step 2a, checked per file |
| `docs/reference/openapi.yaml`, `api_changelog.md` | EPIC-01 ST-01, ST-06, ST-07; EPIC-03 ST-21; EPIC-06 ST-34 | EPIC-01 | Same commit as each contract. Union of additions; highest version |
| `docs/specs/frontend/pages/positions.md`, Trail Stop modal in `Positions.js` | EPIC-01 ST-06, EPIC-03 ST-17 | EPIC-01 | ST-17 rebases; next version |
| SC-TS-* Playwright scenarios | EPIC-03 ST-17, EPIC-07 ST-42 | EPIC-03 | ST-42 renames after ST-17 is on `main` |
| `src/pages/Dashboard.js` | EPIC-01 ST-04, EPIC-02 ST-12 | EPIC-02 | ST-12 deletes the file |
| `docs/specs/metrics_definitions.md` | EPIC-03 ST-15, ST-21, ST-23 | EPIC-03 | One Appendix D row per change |
| `docs/specs/data_model.md` | EPIC-06 ST-35, ST-36; EPIC-05 ST-33 | EPIC-06 | EPIC-05 rebases |
| `Layout.js`, `CommandPalette.js`, `navigation.md`, `glossary.md`, nav/palette specs | EPIC-02 ST-08, ST-11 to ST-14 | EPIC-02 | In-EPIC order; ST-12 before ST-11 on the palette |
| `ai_service.py`, `_NON_TICKER_WORDS`, `ai_s13_boundary_test_suite.md` | EPIC-04 ST-24 to ST-27 | EPIC-04 | In-EPIC order |
| `OPERATIONAL_GUIDE.md`, `prompt_change_log.md`, governance prompts | EPIC-07 ST-37, ST-38, ST-43, ST-44 | EPIC-07 | CLAUDE.md §6 checklist; §8 step 2a per co-bumped file |
| `tests/conftest.py` | EPIC-07 ST-41 (ST-40 if fixtures) | EPIC-07 | In-EPIC |
| `.github/workflows/*` | EPIC-05 ST-31 | EPIC-05 | Merges last |
| `claude/backlog/backlog.md` | Any (new items); ST-12 Notes line | — | `/backlog-add`; `check_backlog_item_integrity.py` after each §8 merge |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-05 ST-29, ST-33; EPIC-06 ST-35, ST-36; also EPIC-04 ST-24 (production read, found at this planning) | Valid. Human-Delegations raised at sprint start; post-merge parts tracked (BLG-SPEC-217, BLG-OPS-197) |
| RISK-02 | EPIC-02 ST-08 to ST-11 | Valid. Spec stories start first; approval named in each AC; unapproved spec returns with a reason |
| RISK-03 | EPIC-04 ST-28 | **Resolved at seal.** Line confirmed, 2026-11-03 |
| RISK-04 | Shared files across EPICs | Valid. Ownership table above; merge order EPIC-01 → 03 → 02 → 04 → 06 → 07 → 05. The ST-16 → ST-12 order is void (ST-16 deferred); new cross-EPIC pairs ST-06 → ST-17 and ST-17 → ST-42 are enforced by merge order |
| RISK-05 | EPIC-05 ST-33 | Valid. Conditional; `Status at sprint open: conditional — gate 2026-11-09` |
| RISK-06 | EPIC-01 ST-01 | Valid. Reuse the panel and endpoint; Playwright per route; one branch |
| RISK-07 | ST-01, ST-20, ST-23, ST-25, ST-28, ST-44, ST-45 | Valid. Each a first sub-step; ST-27 waits on ST-25 |

**Multi-vehicle fix-choice check (LP-14):** ST-01 (Branch A / Branch B) and ST-23 (spec-to-code or code-to-spec) are the multi-vehicle items. ST-01's two branches are both designed and differ by a disabled-state rule, so the effort is similar within the 2.50d M midpoint. ST-23's code-change branch could need a design pass for any new display element; the design gate limited it to same-field changes. There is no Phasing Recommendation (capacity `pass`), so no capacity cross-reference is needed.

## Delegation Classification (set at planning time, per §12 invariant)

- **autonomous (29):** ST-02 to ST-07, ST-11 to ST-15, ST-17 to ST-19, ST-21, ST-22, ST-26, ST-27, ST-30 to ST-32, ST-34, ST-37 to ST-43. Frontend stories use the BLG-GOV-72 fast-path (c): each has a locked decision record or locked spec from the design gate (ST-11 once ST-08 is approved), and Playwright feasibility is named in its AC (ST-03 and the wording-only parts of ST-06, ST-17 use FI-P3-02).
- **delegated_decision (10):** ST-01, ST-20, ST-28, ST-44 (Strategy Rules & System Intent Owner); ST-08, ST-09, ST-10 (Head of UX & Design approval; Head of Specs Team for ST-09; Strategy Rules & System Intent Owner §13 line for ST-10); ST-23 (Data Model & Domain Schema Owner); ST-25 (AI Compliance & Governance Officer); ST-45 (Product Owner). LL-v2.2-SP-01 design artefact check: ST-01 has `trade-entry-pre-entry-checks/decision_record.md` (both branches); ST-08 to ST-10 have the `site-structure-phase1` briefs. ST-20, ST-23, ST-25, ST-28, ST-44 and ST-45 are rulings or decision records with no design surface (ST-23 limited by the design gate to same-field changes). No HoST session is needed.
- **delegated_backend (5):** ST-24 (production log read), ST-29 (Anthropic console), ST-33 (production read, conditional), ST-35 (staging and production constraints), ST-36 (staging index). Code and docs proceed autonomously in each.
- **delegated_frontend / delegated_qa:** none, so the LL-v2.0-P4-2 test-scenario note does not apply.

## Staging-Only and Post-Merge ACs (STEP 6.2)

| Story | AC | Kind | Tracking item |
|-------|----|------|---------------|
| ST-24 | AC 1 | production read (Human-Delegation, in-sprint) | File before PR if deferred |
| ST-29 | AC 1, AC 2 | Anthropic console (Human-Delegation, in-sprint) | File before PR if deferred |
| ST-31 | AC 1 | post-merge (governance-only PR on `main`) | BLG-OPS-211 |
| ST-33 | AC 1, AC 2 | post-merge / production data | BLG-OPS-197 (source item) |
| ST-35 | AC 1 | staging-only (in-sprint) + production post-merge | BLG-SPEC-217 |
| ST-36 | AC 1, AC 2 | staging-only (Human-Delegation, in-sprint) | File before PR if deferred |
| ST-45 | AC 2 | post-merge (next `run roadmap`) | BLG-GOV-408 |

The slice header names ST-33, ST-35 and ST-29. ST-24, ST-31, ST-36 and ST-45 were added at this check: ST-31's AC 1 and ST-45's AC 2 can be met only after merge, and ST-24 and ST-36 need live-environment access.

## Acceptance Criteria Confirmation and Director of Quality Readiness Check (STEP 4)

- **AC source:** every story's AC is in `stage4_backlog_slice.md` (restated where stale, marked *(restated)*), plus the addendum for ST-01. No AC was drafted at this step, and there are no `[AC REQUIRED]` placeholders. The Technical/Quality/Security/Verification fields are carried by the slice's AC lists and the design records' testability sections. Security is N/A for all stories except ST-29 (API key scope and rotation audit) and ST-01 (new optional request field: validated as boolean, no auth change). The §13 clause-citation rule is in the ACs of ST-10 and ST-28.
- **Head of Specs Team (agent-mediated, §5.3):** ACs confirmed testable and observable. Each UI AC names Playwright, or the FI-P3-02 exception (ST-03; the wording-only parts of ST-06, ST-07, ST-17).
- **Director of Quality (agent-mediated, §5.3), per EPIC:** QA criteria are sufficient to produce `qa_evidence_EPIC-xx.md` for all 7 EPICs. ST-08 to ST-10 are evidenced by the approval record, not tests. Known extra Playwright assertions from the design records (ST-01 per route and no-double-panel, ST-02 source/age, ST-18 axe in both themes) must be added or filed before the PR opens (CLAUDE.md §2). No blocking coverage gap.

## Pre-Sprint Vulnerability Scan

Pre-sprint pip-audit: clean. `backend/.venv/bin/pip-audit -r backend/requirements.txt --format=json` scanned 53 dependencies and found 0 vulnerabilities. The trend log row was appended to `docs/ops/pip_audit_trend_log.md`.

## Capacity Buffer Floor (STEP 1.5)

27.50 / 28.00 = 0.982 > 0.95. Buffer floor exceeded. Product Owner acknowledgement, 2026-11-03: proceed (single sprint; ST-16's released 0.50d is not reassigned).

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| RISK-03 confirmation of ST-28's case (c) line | Strategy Rules & System Intent Owner | Yes. **Resolved 2026-11-03** |
| ST-16 disposition | Product Owner | Yes. **Resolved 2026-11-03** |
| File tracking items for post-merge ACs | PMO Lead | Yes. **Done 2026-11-03** (BLG-OPS-211, BLG-SPEC-217, BLG-GOV-408) |
| File design gate observations | PMO Lead | No. **Done 2026-11-03** (BLG-FE-267, BLG-FE-268) |
| Raise rulings and approvals at sprint start: ST-01, ST-08, ST-09, ST-10, ST-20, ST-23, ST-25, ST-28, ST-44, ST-45 | Sprint Execution Engine | No |
| Raise Human-Delegations at sprint start: ST-24, ST-29, ST-35, ST-36; ST-33 from 2026-11-09 | Sprint Execution Engine | No |
| Initialise ST-16 `deferred_at_planning` in `execution_state.json` | Sprint Execution Engine | No |
| Close `BLG-FE-240` as superseded once ST-12 ships | Backlog Management (`groom backlog`) | No |
| Post-ship observation: the slice did not flag ST-20 as a `strategy_rules.md` write, though the registry test forces one under a deploy-date ruling. Release Planning's case (c) scan could check stories that touch `strategy_version_registry.py` | Head of Specs Team | No |
