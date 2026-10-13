# Sprint Planning Notes — 2026-10-12__release-v9.12

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-13
**Cycle:** 2026-10-12__release-v9.12

## Backlog Slice Source

Original: `claude/cycles/2026-10-12__release-v9.12/stage4_backlog_slice.md`. `amended_backlog_slice_path` is empty, so no amendment is active. The slice is read together with `stage4_backlog_slice_addendum.md`, the design gate's post-gate-correction addendum covering ST-23, ST-24, ST-10 and ST-22, as the design gate requires.

## Preflight Summary (STEP -1)

- **Lifecycle guard:** `status = Design_Gate_Passed`. That is a valid Sprint Planning entry state (`shared_standards.md` §10.1), and the status is not `Amendment_In_Progress`.
- **Release plan sealed:** `state.json` has `status = Published` and `publish_eligible = true`. `open_escalations` and `deferred_execution_blockers` are both empty.
- **Design gate:** required, and `Passed` at 2026-10-12T17:59:31Z (`design_gate.md`). All 48 items are cleared: 9 Design Required, 7 Pre-Approved, 32 Not Applicable. Entry was from `Design_Gate_Passed`, so the bypass audit is skipped.
- **Root escalations:** every `open_escalations` entry in `.claude_current_state.json` is `Resolved`.
- **Files, roles and write access:**
  - The slice has 6 EPICs and 48 ST items.
  - The 5 required role files are present: Product Owner, Head of Specs Team, PMO Lead, Director of Quality, FinOps & Resource Architect.
  - `lessons_learnt_prompt.md` and `workforce_capacity.md` are present.
  - `.write_test` was created and deleted.
- **§5 schema-v2 inputs:** `prompt_schema_version: v2`, so the capacity check and execution plan are read from `release_plan.md ## Capacity Check` and `## Execution Plan`.
- **Branch:** `main`.

## Hygiene Advisories (STEP -1.7, -1.8)

- **Prompt change log gaps:** none. Every Class 6 prompt's current `**Version:**` is at or below the target version of its latest-dated `prompt_change_log.md` row (date-scan method). Examples: `sprint_planning_prompt.md` v3.22, `execution_prompt.md` v3.85, `roadmap_prompt.md` v9.32, `release_planning_prompt.md` v2.61.
- **Pre-sprint endpoint coverage audit:** clean. `scripts/audit_endpoint_test_coverage.py` exited 0: 93 route decorators across 27 router files, 8 of them documented `KNOWN_GAPS` exclusions, and no undocumented gap.

## Carry-Forward Items

Carry-forward items reviewed: 3 items from cycle `2026-10-08__release-v9.11` (`lessons_learnt_closure.md ## Carry-Forward`):

1. **`next_release` / roadmap "Next planned release":** resolved. v9.12 was named by Product Owner direction at the closure (DL-085). No action.
2. **`BLG-BE-162` stays P1 and is seated in v9.12:** seated as ST-01, at P1, first in EPIC-01 and first in the merge order.
3. **Diff EPIC/story records and `backlog.md` item bodies against both parents after every CLAUDE.md §8 merge until `BLG-GOV-385` lands:** still in force. `BLG-GOV-385` is ST-39. EPIC-06 merges second, so the scripted check is on `main` before four of the six merges (RISK-07).

## Pre-Sprint Required Decisions (STEP -1.5)

`cycle_summary.md ## Pre-sprint Planning Required Decisions` lists one item.

**RISK-03: whether light mode is a supported theme (ST-23, `BLG-FE-200`). RESOLVED 2026-10-12 at the design gate.**

The Head of UX & Design, with the Product Owner, ruled that light mode **is supported**. The ruling is in `docs/design/2026-10-12__release-v9.12/light-theme-support/decision_record.md` and in the addendum. ST-23 takes AC 1 at its 2.5d estimate, so RISK-03's re-estimate fallback does not fire.

No other pre-sprint decision is unresolved.

## Pre-Sprint Backlog Advisory

`backlog.md` has no items with `Provisional-Target: Before v9.12 sprint planning`.

## Pre-Seal Stale-Feature-Target Check (STEP 3.1)

All 48 source items have exactly one live heading in `claude/backlog/backlog.md`, and none appears in `backlog_archive.md`. Release planning already excluded the done or resolved items (`BLG-GOV-142`, `-360`, `-361`, `-368`).

ST-35 is a partial case. The design gate notes that `positions.md` v2.16 §Gap Risk Badge already names `GET /positions/{position_id}/gap-risk`. A gap remains, though: the AC also requires confirming that no other reference claims a `gap_risk` field on `GET /positions`, plus a version bump and a changelog row. So ST-35 stays `include`, not `flag`.

## Named-File Write Check (STEP 3.1)

- Named-file write: `claude/roadmap/role_share_history.md` (split-credit column) — authorised under execution_prompt.md §7 named-file rule (ST-44, `delegated_decision`, RISK-06).
- Named-file write: `claude/backlog/backlog.md` `BLG-OPS-181` `Notes` line (the cause found by the investigation) — authorised under execution_prompt.md §7 named-file rule (ST-29). Redrafted at STEP 4: the slice AC's "recorded against this item" names the item but not the field. The sprint backlog's ST-29 Notes name the field.

Other governed writes, which are not named-file writes under the `claude/roadmap/*` / `backlog.md` rule:
- **New backlog items:** ST-34 (genuine drift gaps) and any story filing a Playwright-gap item. These are added via `/backlog-add` under execution's new-item exception. No existing item is edited.
- **Governance prompts:** ST-40 (`release_planning_prompt.md` §1.3a), ST-41 (`execution_prompt.md` §9.2), ST-42 (`roadmap_prompt.md` §7.1, including any method-break note, not `decision_log.md`) and ST-43 (`idea_intake_prompt.md` or `roadmap_prompt.md` STEP -1.6, if adopted). Each runs the CLAUDE.md §6 checklist.
- **CLAUDE.md §8:** ST-39, under Head of Specs Team authority.
- **Role charter:** ST-21 (`claude/agents/frontend_specs_ux_documentation_owner.md`), under Director of HR authority.
- **Decision record:** ST-14 adds a dated addendum and ST-37 refreshes the body of `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`. Neither edits `strategy_rules.md`.

No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned, so no separate Product Owner confirmation line is needed (§6.2).

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | None. All 48 slice items are in sprint scope. | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | Live `INTEGER[]`→`UUID[]` migration on staging and production; Trade History staging run | External: Human-Delegation, Data Model & Domain Schema Owner + Infrastructure & Operations Owner | RISK-01, raise at sprint start. Code and docs proceed regardless |
| ST-03 | ST-02 | Internal (same prompt module) | Open, sequenced |
| ST-04 | ST-02, ST-03 | Internal (same briefing module) | Open, sequenced |
| ST-04 | AI Compliance & Governance Officer failure-action sign-off | Governance (first sub-step) | Raise at sprint start |
| ST-06 | ST-01 (`ai_endpoints.md`) | Internal | Open, sequenced |
| ST-08 | ST-07 (same function) | Internal | Open, sequenced |
| ST-09 | ST-07, ST-08 (same service module) | Internal | Open, sequenced |
| ST-10 | Strategy Rules & System Intent Owner §7.3 ruling | Governance (first sub-step) | RISK-02, raise at sprint start |
| ST-12 | ST-11 (same recompute paths) | Internal | Open, sequenced |
| ST-14 | ST-37 (EPIC-05, same §13 record) | Cross-EPIC | Open. The addendum is appended after ST-37's body refresh |
| ST-14 | Strategy Rules & System Intent Owner dated §13 addendum | Governance | RISK-02, raise at sprint start |
| ST-15 | ST-10 (Positions stop area) | Internal | Open, sequenced |
| ST-18 | ST-17 (same page) | Internal | Open, sequenced |
| ST-19 | ST-17, ST-18 (tests the changed page) | Internal | Open, sequenced |
| ST-21 | ST-20, ST-18 | Internal | Open, sequenced |
| ST-21 | Director of HR authority for the charter change | Governance | RISK-06, raise at sprint start |
| ST-26 | ST-16 (EPIC-02), ST-20 and ST-21 (EPIC-03) | Cross-EPIC | Open. EPIC-04 merges last (RISK-05) |
| ST-26 | Live migration on staging and production | External: RISK-01 Human-Delegation | Raise at sprint start |
| ST-27 | Narrower key or Product Owner accept-risk | Governance | Raise at sprint start |
| ST-28 | All other EPIC-03/EPIC-04 frontend changes | Cross-EPIC (final tree) | Open. Last story before the EPIC-04 PR |
| ST-28 | Staging check of the bumped build | External: Human-Delegation if needed | Conditional |
| ST-29 | Render dashboard access | External: Human-Delegation, Infrastructure & Operations Owner | RISK-01, raise at sprint start |
| ST-30 | ST-29; staging deploy control and a Telegram receipt | Internal + External: Human-Delegation | RISK-01, raise at sprint start |
| ST-34 | Production `pg_indexes` read (finding 1 only) | External: Human-Delegation, Data Model & Domain Schema Owner | RISK-01, raise at sprint start |
| ST-38 | ST-34 (`data_model.md`) | Internal | Open, sequenced |
| ST-38 | Data Model & Domain Schema Owner sign-off; read-only live sample (staging needs the user's permission) | Governance + External | Raise at sprint start |
| ST-40 | ST-39 (EPIC-06 order) | Internal | Open, sequenced |
| ST-41 → ST-42 → ST-43 | Previous governance bump | Internal (sequential `OPERATIONAL_GUIDE.md` versions) | Open, sequenced |
| ST-43 | Head of Specs Team + Product Owner ruling | Governance (first sub-step) | Raise at sprint start |
| ST-44 | ST-45 (extends its test file) | Internal | Open, sequenced |

**Spec dependencies:** the design gate locked every Design Required and Pre-Approved frontend spec:
- `positions.md` v2.16
- `components/position_form.md` v1.9
- `settings.md` v1.9
- `risk_dashboard.md` v0.1.13
- `reports.md` v0.23
- `notifications.md` v0.11
- `dashboard.md` v3.9
- `trade_plan.md` v1.18
- `strategy_benchmark.md` v0.8
- `signals.md` v0.4

Six decision records are in place under `docs/design/2026-10-12__release-v9.12/`. ST-10's spec is conditional on its ruling, and the branch not taken is deleted in the story's own commit.

**No circular dependencies.** Every edge points from a later-sequenced story to an earlier one, and the two cross-EPIC edges (ST-26 → EPIC-02/03, ST-14 → ST-37) run one way.

## Execution Sequence

EPIC merge sequence: **EPIC-01 → EPIC-06 → EPIC-05 → EPIC-02 → EPIC-03 → EPIC-04.**

- **EPIC-01** goes first because it carries the P1 anchor, and it owns `execution_state.json`.
- **EPIC-06** goes second, so ST-39's backlog-integrity check, ST-41's read-back script and ST-46's `utils.*` stub guard are on `main` before the four larger merges. This answers RISK-07.
- **EPIC-05** precedes EPIC-02, so ST-37's §13 record refresh lands before ST-14's addendum. Its `data_model.md` edits also sit between EPIC-01's migration and EPIC-04's.
- **EPIC-04** goes last, because ST-26 follows EPIC-02/03 and ST-28 needs the final tree.

**Fallback:** if EPIC-05 is waiting on the ST-34 or ST-38 delegations, EPIC-02 may merge ahead of it. EPIC-05 then rebases, and ST-37's body refresh must keep ST-14's appended addendum intact.

1. **EPIC-01:** ST-01 (code first; live migration and staging run delegated at sprint start) → ST-02 → ST-03 → ST-04 (failure-action sign-off raised at sprint start) → ST-06 (after ST-01); ST-05 in parallel
2. **EPIC-06:** ST-39 → ST-40 → ST-41 → ST-42 → ST-43 (ruling raised at sprint start); ST-45 → ST-44; ST-46, ST-47, ST-48 in parallel
3. **EPIC-05:** ST-37 first (ahead of ST-14) → ST-34 (finding 1 delegated) → ST-38 (sign-off and sample); ST-33, ST-35, ST-36 in parallel
4. **EPIC-02:** ST-07 → ST-08 → ST-09; ST-11 → ST-12; ST-10 (ruling at sprint start) → ST-15; ST-13, ST-16 in parallel; ST-14 (addendum after ST-37)
5. **EPIC-03:** ST-17 → ST-18 → ST-19; ST-20 → ST-21 (charter authority at sprint start); ST-22, ST-23, ST-24 in parallel
6. **EPIC-04:** ST-25 → ST-26 (after EPIC-02/03 are on `main`; migration delegated) → ST-29 → ST-30; ST-27, ST-31, ST-32 in parallel; ST-28 last

Autonomous items run before delegated ones within each EPIC wherever dependencies allow. Every Human-Delegation request and every ruling or sign-off is raised at sprint start, so answers can come in while autonomous work proceeds:
- **Human-Delegation:** ST-01 and ST-26 migrations; ST-28 staging check; ST-29 Render dashboard; ST-30 live fire; ST-34 production read; ST-38 sample.
- **Rulings and sign-offs:** ST-04, ST-10, ST-14, ST-21, ST-27, ST-38, ST-43.

## Multi-EPIC Execution Notes

- **`execution_state.json` owner:** EPIC-01, the first in execution order. Every other EPIC branch must check whether `claude/cycles/2026-10-12__release-v9.12/execution_state.json` exists before creating one. If it exists, the branch reads it and appends its own EPIC section, and never overwrites it.
- **Cross-EPIC commit pre-PR check (LL-v9.9-P3-01):** each EPIC branch is cut from `main` and carries only its own `[EPIC-xx]` commits.
- **Escalation mirroring (LL-v9.11-P3-02):** every `ESC-EXEC-*` record raised for a delegation above is mirrored into `.claude_current_state.json.open_escalations`.

## Shared-File Ownership Advisory

| Shared file | EPICs touching it | Canonical owner | Advisory |
|-------------|-------------------|-----------------|----------|
| `docs/reference/openapi.yaml` | EPIC-01 (ST-01 `trade_ids`), EPIC-02 (ST-10 Branch A route, ST-15 `stop_frozen_reason`), EPIC-03 (ST-17 `GET /market/atr/{ticker}`), EPIC-04 (ST-26 `last_change`), EPIC-05 (ST-33 if migrated) | EPIC-01 | Union of path and field additions, highest version (CLAUDE.md §8). Same-commit contract + OpenAPI rule (CLAUDE.md §2). |
| `backend/routers/test.py`, `src/pages/SystemStatus.js` fallback count, `tests/e2e/system-status.spec.js` `SC-SS-01b` | EPIC-02 (ST-10, Branch A only), EPIC-03 (ST-17) | EPIC-02 | The fallback count is one number. EPIC-03 rebases after EPIC-02 merges and recomputes the count from the merged `test.py`. It does not add 1 to a stale value. |
| `docs/specs/data_model.md` | EPIC-01 (ST-01), EPIC-05 (ST-34, ST-38), EPIC-04 (ST-26) | EPIC-01 | Keep migration blocks in ascending version order, with the highest footer version (CLAUDE.md §8). |
| `docs/specs/api_contracts/ai_endpoints.md` | EPIC-01 only (ST-01, ST-06) | EPIC-01 | ST-06 lands after ST-01. |
| `src/pages/Positions.js`, `src/components/positions/PositionCard.js` | EPIC-02 (ST-10, ST-15), EPIC-03 (ST-21 literals, ST-22 deep link, ST-24 Gap Risk badge colour) | EPIC-02 | EPIC-03 rebases after EPIC-02 and keeps both sides' changes. |
| `src/pages/Settings.js`, settings create path (`create_settings`), `settings_endpoints.md` | EPIC-02 (ST-16), EPIC-03 (ST-20, ST-21), EPIC-04 (ST-26) | EPIC-03 (page); EPIC-02 (create path) | ST-26 is written against `main` after EPIC-02 and EPIC-03 merge (RISK-05). |
| `docs/specs/api_contracts/position_endpoints.md`, `portfolio_endpoints.md` | EPIC-02 (ST-10, ST-13, ST-15) | EPIC-02 | Single EPIC. |
| `backend/services/position_service.py` | EPIC-02 (ST-11, ST-12 recompute paths), EPIC-03 (ST-17 preview parity, ST-18 ATR validation), EPIC-05 (ST-38 if a code fix), EPIC-06 (ST-47 tests read it) | EPIC-02 | ST-17's backend test pins preview == `initial_stop`. Re-run it after any rebase over EPIC-02. |
| `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md` | EPIC-05 (ST-37 body), EPIC-02 (ST-14 addendum) | EPIC-05 | ST-37 first; the addendum is appended. |
| `tests/e2e/accessibility-axe-scan.spec.js` / `KNOWN_VIOLATIONS` | EPIC-03 (ST-23 light-theme entries, ST-24 badge scans) | EPIC-03 | Single EPIC. Remove the four `:light` entries in ST-23's commit. |
| `src/lib/strategyParameters.js` → `src/constants/strategy.js`, `tests/test_strategy_parameter_parity.py` | EPIC-03 (ST-21) | EPIC-03 | Move, don't duplicate (Head of Specs Team AC interpretation, 2026-10-13). Any later EPIC importing the old path must use the new one after EPIC-03 merges. |
| `tests/` files that install `utils.*` stubs | EPIC-06 (ST-46 guard), any EPIC adding tests | EPIC-06 | After EPIC-06 merges, new tests must scope their `utils.*` stubs or the guard fails them. |
| `claude/system/OPERATIONAL_GUIDE.md`, `claude/system/prompt_change_log.md` | EPIC-06 (ST-40, ST-41, ST-42, ST-43) | EPIC-06 | One EPIC, so bumps are sequential. Run the CLAUDE.md §6 checklist per commit and the §8 step 2a per-file version-collision check against anything merged meanwhile, including the open v9.11 closure action #8(b) if it lands separately. |
| `CLAUDE.md` | EPIC-06 (ST-39 §8), EPIC-04 (ST-31 §9, optional) | EPIC-06 | ST-31's §9 mention is optional and needs Head of Specs Team agreement. |
| `claude/backlog/backlog.md` | Any EPIC (new items); EPIC-04 (ST-29 `BLG-OPS-181` Notes line) | — | Append via `/backlog-add`. Re-check new IDs after rebasing. Run ST-39's integrity check once it is on `main`. |
| `claude/roadmap/role_share_history.md` | EPIC-06 (ST-44 only) | EPIC-06 | Named-file write (above). |
| `package.json` / lockfile, `backend/requirements.txt` | EPIC-04 (ST-28) | EPIC-04 | Last story in the last EPIC, so one CI run covers the final tree. |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 / ST-01; EPIC-04 / ST-26, ST-28, ST-29, ST-30; EPIC-05 / ST-34, ST-38 | Valid. Human-Delegation at sprint start (DS-27/28/29 precedent). Code and docs proceed regardless. ST-28 is added to the list because its AC 2 needs a staging deploy of the bumped build. |
| RISK-02 | EPIC-02 / ST-10, ST-14 (ST-25 only under option (b)) | **Changed: ST-14's addendum moves from "may" to "expected".** The slice AC states that the story changes §13.3's "next trading session" limb, so ST-14 is classed `delegated_decision`. ST-10's ruling is its first sub-step. ST-25 defaults to option (a). |
| RISK-03 | EPIC-03 / ST-23 | **Changed: resolved at the design gate (2026-10-12).** Light mode is supported. The 2.5d estimate stands. |
| RISK-04 | EPIC-01, EPIC-02, EPIC-03, EPIC-04, EPIC-05 | **Changed: widened at the design gate.** ST-15 (`stop_frozen_reason`) and ST-26 (`last_change`) add response fields to `openapi.yaml`, so EPIC-04 shares it too. ST-17's route is certain; ST-10's depends on Branch A. See the Shared-File Ownership Advisory. |
| RISK-05 | EPIC-02 / ST-16; EPIC-03 / ST-20, ST-21; EPIC-04 / ST-26 | Valid. EPIC-04 merges last. |
| RISK-06 | EPIC-03 / ST-21; EPIC-06 / ST-39–ST-44 | Valid. ST-21's charter change needs Director of HR authority and ST-39's needs Head of Specs Team authority. ST-44 is `delegated_decision` under the named-file rule. ST-40–ST-43 each run the CLAUDE.md §6 checklist in sequence. |
| RISK-07 | Release-level | Valid. EPIC-06 merges second, so ST-39 is on `main` early. Until then, apply v9.11 Carry-Forward #3 by hand after the EPIC-01 merge. |
| RISK-08 | Release-level | Valid. The Product Owner chose a single sprint on 2026-10-13. 34 stories are XS or ≤0.5d and are grouped by file. |

**Multi-vehicle fix-choice check (LP-14):**
- **ST-10:** Branch A (manual raise via `PATCH /positions/{id}/stop`) needs a route, the full registration chain and Playwright, about 1d. Branch B (read-only modal, "View Trail") is about 0.5d. The plan uses the 0.75d midpoint, so the pessimistic case adds 0.25d.
- **ST-27:** a narrower frontend key (a new key plus a backend scope check) costs more than an accept-risk record. The pessimistic case may run to about 1d, adding about 0.5d.
- **ST-38:** a code fix to `create_position()` costs more than a doc fix and may need a design pass if displayed values change. The pessimistic case adds about 0.5d.
- **ST-25:** option (a) is the default. Option (b) needs a ruling but similar effort.

If every pessimistic case hit at once, the total would be about 29.2d, over the 28d ceiling. The capacity check is `pass`, so there is no Phasing Recommendation to cross-reference. If more than one pessimistic case materialises, raise it at the mid-sprint review. Out-of-scope work goes through `amend cycle`, not informal deferral.

## Delegation Classification (set at planning time, per §12 invariant)

| Item | Delegation class | Justification |
|------|-------------------|----------------|
| ST-01 | delegated_backend | Live migration on staging and production, and a Trade History staging run (AC 1, AC 4; RISK-01) |
| ST-02, ST-03, ST-05 | autonomous | Output filter, context label and scan, each tested by fixtures |
| ST-04 | delegated_decision | AI Compliance & Governance Officer signs off the failure action first |
| ST-06 | autonomous | Cost aggregation and docs. If the scheduler's run history is not readable, AC 2's run record becomes a Human-Delegation at that point |
| ST-07–ST-09, ST-11–ST-13, ST-16 | autonomous | Backend fixes and tests. ST-07, ST-08 and ST-13 are Design Pre-Approved against locked specs |
| ST-10 | delegated_decision | Strategy Rules & System Intent Owner §7.3 ruling (RISK-02) |
| ST-14 | delegated_decision | Dated §13 addendum by the Strategy Rules & System Intent Owner, expected per the AC (RISK-02) |
| ST-15, ST-17, ST-18, ST-22, ST-23, ST-24 | autonomous | BLG-GOV-72 fast-path (c): locked frontend specs and decision records from the design gate, with Playwright listed in each. ST-22's and ST-23's product calls were made at the gate |
| ST-19, ST-20 | autonomous | Playwright coverage; ST-20 is wording only (FI-P3-02) |
| ST-21 | delegated_decision | Director of HR authority over the charter change (RISK-06). The module interpretation was settled at planning |
| ST-25 | autonomous | Option (a) by default. Reclassify if option (b) is chosen |
| ST-26 | delegated_backend | Live migration (AC 3, RISK-01) |
| ST-27 | delegated_decision | Narrower key vs Product Owner accept-risk |
| ST-28 | delegated_qa | AC 2 staging check of the bumped build |
| ST-29, ST-30 | delegated_backend | Render dashboard; staging deploy control and a Telegram receipt (RISK-01) |
| ST-31, ST-32, ST-33, ST-35, ST-36, ST-37 | autonomous | Docs, spec and contract reconciliation |
| ST-34 | delegated_backend | Production `pg_indexes` read for finding 1 (RISK-01) |
| ST-38 | delegated_decision | Data Model & Domain Schema Owner signs off doc fix vs code fix; the live sample is supporting evidence |
| ST-39–ST-42 | autonomous | Governance tooling and prompt edits under the CLAUDE.md §6 checklist, with no ruling needed; ST-39's CLAUDE.md edit is named in its AC |
| ST-43 | delegated_decision | Head of Specs Team + Product Owner ruling |
| ST-44 | delegated_decision | Named-file write; kept per the release plan's RISK-06 mitigation |
| ST-45–ST-48 | autonomous | Tests and configuration hygiene |

Totals: 34 autonomous, 8 `delegated_decision`, 5 `delegated_backend`, 1 `delegated_qa`. No `delegated_frontend`.

**Blocked-decision design artefact check (LL-v2.2-SP-01):**
- ST-10 has its design artefact: `trail-stop-action/decision_record.md`, with both branches designed.
- ST-04, ST-14, ST-21, ST-27, ST-38, ST-43 and ST-44 have no dedicated HoST design session artefact. Each is a ruling or sign-off that its own AC scopes as a first sub-step, with no UI design surface.

Advisory only, not a blocker.

**Test scenario gap (LL-v2.0-P4-2):** no `delegated_frontend` items, so the rule does not apply.

## Acceptance Criteria Confirmation and Director of Quality Readiness Check (STEP 4)

Every story's AC in `stage4_backlog_slice.md`, read with the addendum, meets the §7 standard:
- **Technical:** observable outcomes.
- **Quality:** named unit tests, Playwright specs, CI runs or recorded evidence.
- **Verification:** by recorded evidence, a run URL or a sign-off.
- **Security:** the subject of the AC for:
  - ST-01: UUID input typing; integer IDs rejected with 422.
  - ST-02: unknown-ticker actions dropped.
  - ST-18: implausible ATR rejected with 400.
  - ST-10 AC 3: supplied stop rejected, not ignored.
  - ST-26: audit trail.
  - ST-27: credential scope.
  - ST-28: dependency supply chain.
  - ST-17 (and ST-10 under Branch A): new routes; no AI call and not an AI endpoint, so the AI endpoint checklist is not triggered.
  - Elsewhere N/A, because no auth, input or data-exposure surface changes.

There are no `[AC REQUIRED]` placeholders. Two clarifications are recorded in the sprint backlog's Notes, as STEP 4 redrafts:
- **ST-29:** AC 1's target is the `BLG-OPS-181` `Notes` field (named-file write above).
- **ST-21:** the constants-module interpretation. Head of Specs Team, 2026-10-13: create `src/constants/strategy.js` and move `src/lib/strategyParameters.js` into it, so one source remains.

The Director of Quality confirms that the criteria are sufficient for each EPIC's `qa_evidence_EPIC-xx.md`. As in prior cycles, this confirmation is agent-mediated.

Non-blocking outstanding actions:
- **Design gate Playwright assertions beyond the slice ACs:**
  - ST-10: the no-raise note when `trail_difference ≤ 0`.
  - ST-15: no indicator during grace.
  - ST-22: `data-highlighted` on the target row.

  Execution adds them, or files a backlog item before the PR opens (CLAUDE.md §2).
- **Staging-only ACs:** these are listed per story in `sprint_backlog.md`: ST-01, ST-06, ST-26, ST-28, ST-29, ST-30, ST-34 and ST-38. If a staging sign-off is deferred past merge, a backlog item is filed before the PR opens.

## Pre-Sprint Vulnerability Scan

Pre-sprint pip-audit: clean. The scan ran through the project virtualenv (`backend/.venv/bin/pip-audit -r backend/requirements.txt --format=json`), with 0 vulnerabilities across 52 resolved dependencies.

The count is down from 60 at v9.11, with no change to `backend/requirements.txt` this cycle. That makes it a transitive-resolution change; it was not investigated here, and ST-28's bumps will move it again. A trend row was appended to `docs/ops/pip_audit_trend_log.md`.

## Capacity Buffer Floor (STEP 1.5)

27.95 / 28.00 = 99.8%, above the 95% advisory floor. Product Owner: **proceed at ceiling**, 2026-10-13. The Product Owner also declined RISK-08's optional two-sprint split: **single sprint**, 2026-10-13.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| RISK-03 light-mode decision (ST-23) | Head of UX & Design; Product Owner | Yes. **Done 2026-10-12 (supported, at the design gate)** |
| ST-21 constants-module interpretation | Head of Specs Team | Yes. **Done 2026-10-13 (move the mirror into `src/constants/strategy.js`)** |
| §7.3 ruling for ST-10 and the §13 addendum for ST-14, raised at sprint start | Strategy Rules & System Intent Owner | No |
| Failure-action sign-off for ST-04, raised at sprint start | AI Compliance & Governance Officer | No |
| Charter-change authority for ST-21 | Director of HR | No |
| Key decision for ST-27 | Cybersecurity & Trust Lead; Product Owner | No |
| Doc fix vs code fix sign-off for ST-38 | Data Model & Domain Schema Owner | No |
| Reduced-roster idea-window ruling for ST-43 | Head of Specs Team; Product Owner | No |
| Human-Delegation: ST-01 and ST-26 live migrations; ST-28 staging check; ST-29 Render dashboard; ST-30 live fire; ST-34 production `pg_indexes` read; ST-38 live sample | Infrastructure & Operations Owner; Data Model & Domain Schema Owner | No |
| Playwright for the ST-10 no-raise note, ST-15 no-indicator-in-grace and ST-22 `data-highlighted`, or backlog items filed before the PR opens | QA & Testing Owner | No |
| File a backlog item (via `/backlog-add`, at execution) for the design gate observation: `strategy_benchmark.md` §7 tinted exit-reason badges vs the shipped filled ones, and `bg-teal-600 text-white` (Rebalance) at about 3.7:1. Sprint Planning's write scope excludes `backlog.md` | Frontend Specifications & UX Documentation Owner | No |
| v9.11 closure action #8(b), overdue (deadline was "before `plan release v9.12`"): extend `release_planning_prompt.md` §1.3a bound 5 to gates removed by a Product Owner decision outside Release Planning. This was **not** bundled into ST-40, because Sprint Planning cannot add to a sealed AC. It is a separate Head of Specs Team change. If it lands while EPIC-06 is open, ST-40 applies the CLAUDE.md §8 step 2a version check | Head of Specs Team | No |
| Manual backlog/execution-state diff after each §8 merge until ST-39 is on `main` (RISK-07) | PMO Lead | No |
