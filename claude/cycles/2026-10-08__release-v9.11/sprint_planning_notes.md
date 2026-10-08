# Sprint Planning Notes — 2026-10-08__release-v9.11

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-08
**Cycle:** 2026-10-08__release-v9.11

## Backlog Slice Source

Original — `claude/cycles/2026-10-08__release-v9.11/stage4_backlog_slice.md` (`amended_backlog_slice_path` is empty; no amendment is active). Read together with `stage4_backlog_slice_addendum.md` (design gate post-gate-correction addendum: ST-25 §13 pre-check ordering), as the design gate requires.

## Preflight Summary (STEP -1)

- **Lifecycle guard:** `status = Design_Gate_Passed`, which is a valid Sprint Planning entry state (`shared_standards.md` §10.1). Not `Amendment_In_Progress`.
- **Release plan sealed:** `state.json` has `status = Published` and `publish_eligible = true`. `open_escalations` and `deferred_execution_blockers` are both empty.
- **Design gate:** required, `Passed` (2026-10-08T09:40:11Z, `design_gate.md`). 42 items cleared, ST-25 conditionally cleared (§13 pre-check). Entered from `Design_Gate_Passed`, so the bypass audit is skipped.
- **Files, roles and write access:** the slice has 6 EPICs and 43 ST items. The 5 required role files (Product Owner, Head of Specs Team, PMO Lead, Director of Quality, FinOps & Resource Architect) are present. `lessons_learnt_prompt.md` is present. The `.write_test` file was created and deleted.
- **§5 schema-v2 inputs:** no standalone `stage4_5_capacity_check.md` or `stage3_execution_plan.md`. The release plan is schema v2 (`prompt_schema_version: v2`), so these are read from `release_plan.md ## Capacity Check` and `## Execution Plan`.
- **Branch:** `main`. The first invocation this session halted at STEP 0 on `governance/2026-10-08-roadmap-scheduled`, because the design gate commit (`e5ea41c3`) was not yet on `main`. It was merged via PR #1924 and this run proceeded from `main`.

## Hygiene Advisories (STEP -1.7, -1.8)

- **Prompt change log gaps:** none. Every Class 6 prompt's current `**Version:**` matches its latest-dated `prompt_change_log.md` row (`OPERATIONAL_GUIDE.md` v4.227, `execution_prompt.md` v3.84, `sprint_planning_prompt.md` v3.21 and others).
- **Pre-sprint endpoint coverage audit:** clean. 93 route decorators across 27 router files; 8 are documented `KNOWN_GAPS` exclusions; no undocumented gap (`scripts/audit_endpoint_test_coverage.py`, exit 0).

## Carry-Forward Items

Carry-forward items reviewed: 4 items from cycle `2026-10-06__release-v9.10` (`lessons_learnt_closure.md ## Carry-Forward`):

1. `ESC-CLOSE-20261007-01` was open: resolved 2026-10-07 (`release_planning_prompt.md` v2.60), and used by v9.11 release planning's §1.3a re-gates. No action here.
2. `run audit` due (`completed_cycle_count` 87, last audit at 84): still outstanding. `cycle_summary.md` repeats the advisory. Not a Sprint Planning action; surfaced to the user.
3. Scheduled rebalance due before `plan release`: done (`2026-10-08__scheduled`, DL-084). `BLG-GOV-355` is seated as ST-34.
4. `BLG-BE-147` (grace calendar days): seated as ST-14.

## Pre-Sprint Required Decisions (STEP -1.5)

`cycle_summary.md ## Pre-sprint Planning Required Decisions` lists one item.

**RISK-06 — §13 standing of ST-25 (AI-assisted monthly P&L narrative, `BLG-FEAT-59`): RESOLVED 2026-10-08.**

The owning authority is the **Strategy Rules & System Intent Owner**. Sprint Planning runs as PMO Lead, so the role mismatch was flagged (CLAUDE.md §2 role-ownership rule), and the user gave the ruling explicitly under the Strategy Rules & System Intent Owner role.

- **Ruling: confirmation route.** ST-25 stays a build story. It is not re-scoped to a full §13 review. The narrative describes realised monthly results after the fact, with no forecast and no trade signal. That is the same advisory shape as the post-trade debrief, which the v8.9 review (`decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`, CONDITIONAL) covers. RISK-06's re-scope fallback is not taken.
- **Within ST-25 (unchanged from the addendum):** the first sub-step is the Strategy Rules & System Intent Owner's recorded §13 determination (PASS / CONDITIONAL / FAIL). It cites every §13 clause that names AI output or financial reporting (ST-25 AC 2), using ST-35's rule if that has landed. The AI endpoint security checklist, the design decision record (with Product Owner approval) and the `reports.md` update follow. No ST-25 implementation commit lands before these are recorded in `execution_state.json`.
- **Stop condition:** if the determination is FAIL, or finds that a full §13 review is needed after all, ST-25 and ST-26 stop. The scope change goes through `amend cycle`, not informal deferral.

There are no other unresolved pre-sprint decisions.

## Pre-Sprint Backlog Advisory

`backlog.md` has no items with `Provisional-Target: Before v9.11 sprint planning`.

## Pre-Seal Stale-Feature-Target Check (STEP 3.1)

All 43 source items are live in `claude/backlog/backlog.md`, and none is in `backlog_archive.md`. Release planning already excluded `BLG-FE-195` (delivered by v9.10 ST-01) and the done governance items. No candidate targets a feature that has already shipped, so no item is flagged.

## Named-File Write Check (STEP 3.1)

- Named-file write: `claude/roadmap/product_value_ratio_history.md` `## History` table (effort-weighted PVR column, 5-window backfill) — authorised under execution_prompt.md §7 named-file rule (ST-34, `delegated_decision`, RISK-07).

No other story's AC writes a `claude/roadmap/*` file or edits a field of an existing `backlog.md` item:
- ST-12, ST-26 and ST-28 were restated at release planning to file **new** backlog items, not edit existing ones.
- ST-24, ST-25 and ST-27's "Gate: satisfied — no action" lines need no write.
- ST-29's "DEV-v9.7-ST04-01 marked resolved" lands in `docs/specs/frontend/pages/reports.md` (§DEV-v9.7-ST04-01), a canonical spec, not `backlog.md`.

No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned, so no separate Product Owner confirmation line is needed (§6.2).

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | None. All 43 slice items are in sprint scope. | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | AI Compliance & Governance Officer Condition 2 sign-off | Governance (first sub-step) | RISK-01 — raise at sprint start |
| ST-02 | Staging deploy with a working Anthropic key, human exercising the UI | External — Human-Delegation, Infrastructure & Operations Owner | RISK-02 — raise at sprint start |
| ST-02 | ST-03, ST-04 (escaped-defect note cites them) | Internal | Open — sequenced (note closes after them) |
| ST-04 | ST-03 | Internal (pairing) | Open — sequenced |
| ST-05 | ST-01 (same debrief component) | Internal | Open — sequenced |
| ST-06 | Live migration (staging and production) | External — Human-Delegation, Data Model & Domain Schema Owner + Infrastructure & Operations Owner | RISK-03 — code and `data_model.md` proceed regardless |
| ST-08 | ST-07 (same prompt module, one `prompt_version` bump each) | Internal | Open — sequenced |
| ST-09 | ST-01, ST-07, ST-08 (same call sites) | Internal | Open — sequenced |
| ST-11 | ST-10 (same table and endpoint) | Internal | Open — sequenced |
| ST-12 | ST-10 (same service function) | Internal | Open — sequenced |
| ST-13 | ST-10, ST-11 (same endpoint and table) | Internal | Open — sequenced |
| ST-17 | ST-16 (grace ruling may affect the recorded source) | Internal | Open — sequenced |
| ST-17 | Live migration, if new `trade_history` columns | External — RISK-03 Human-Delegation | Conditional |
| ST-16 | Strategy Rules & System Intent Owner ruling | Governance (first sub-step) | RISK-05 — raise at sprint start |
| ST-20 | Live migration | External — RISK-03 Human-Delegation | Raise at sprint start |
| ST-25 | ST-23 (cost estimate is the cost-gating input), ST-24 (metric baseline) | Internal | Open — sequenced |
| ST-25 | Strategy Rules & System Intent Owner §13 determination, then AI endpoint security checklist, then design decision record + PO approval + `reports.md` | Governance / design (addendum) | RISK-06 route resolved 2026-10-08; determination is the first sub-step |
| ST-25 | ST-35 (§13 citation rule) | Cross-EPIC, advisory | Apply the rule if ST-35 has been pushed |
| ST-26 | ST-25 | Internal | Open — sequenced |
| ST-30 | ST-06 (EPIC-01), ST-17 and ST-20 (EPIC-03) add columns | Cross-EPIC | Open — EPIC-05 merges last |
| ST-34 | `BLG-GOV-339` Head of Specs Team + Product Owner sign-off (for the `roadmap_prompt.md` STEP 2.4 change only) | Governance | RISK-07 — raise at sprint start; the history-table backfill proceeds regardless |
| ST-36 | — (early, so EPIC-02/EPIC-03 qualifying stories can complete its DoQ line) | Cross-EPIC, advisory | Sequenced first in EPIC-06 |
| ST-39 | ST-41 (same pilot test file) | Internal | Open — sequenced |
| ST-42 | Repository admin access | External — Human-Delegation, Infrastructure & Operations Owner | RISK-08 — raise at sprint start |

**Spec dependencies:** the design gate locked the frontend specs for every Design Required item except ST-25 (`trade_history.md` v1.15, `risk_dashboard.md` v0.1.12, `dashboard.md` v3.8, `positions.md` v2.15). ST-25's design record and `reports.md` section are produced inside the story, before implementation (addendum).

**No circular dependencies.** Every edge points from a later-sequenced story to an earlier one.

## Execution Sequence

EPIC merge sequence: **EPIC-01 → EPIC-02 → EPIC-03 → EPIC-06 → EPIC-04 → EPIC-05**. The P1 fast-track and AI-reliability EPIC goes first and owns `execution_state.json`. The P2 build-and-ship EPIC-02 follows. EPIC-06 merges before EPIC-04 so ST-35's §13 citation rule and ST-36's DoQ line are on `main` early. EPIC-05 merges last because ST-30 annotates columns that EPIC-01 and EPIC-03 add.

1. **EPIC-01:** ST-01 (Condition 2 sign-off first) → ST-03 → ST-04 → ST-05 (after ST-01) → ST-07 → ST-08 → ST-09 → ST-06 (code first, live migration delegated) → ST-02 (delegated staging run raised at sprint start; note closes after ST-03/ST-04)
2. **EPIC-02:** ST-10 → ST-11 → ST-12 → ST-13; ST-14 and ST-15 in parallel
3. **EPIC-03:** ST-16 (ruling raised at sprint start) → ST-17; ST-18, ST-19, ST-21, ST-22 in parallel; ST-20 (code first, live migration delegated)
4. **EPIC-06:** ST-36 → ST-35 → ST-33 → ST-41 → ST-39; ST-37, ST-38, ST-40, ST-43 in parallel; ST-34 (sign-off raised at sprint start), ST-42 (delegated)
5. **EPIC-04:** ST-23 → ST-24 → ST-25 (§13 determination raised at sprint start) → ST-26; ST-27, ST-28 in parallel
6. **EPIC-05:** ST-29, ST-31, ST-32 → ST-30 (after EPIC-01/EPIC-03 columns land)

Autonomous items run before delegated items within each EPIC wherever dependencies allow. All Human-Delegation requests (ST-02 staging run; ST-06, ST-17 if needed, ST-20 live migrations; ST-42 branch protection) and all rulings and sign-offs (ST-01 Condition 2, ST-16 grace ruling, ST-25 §13 determination, ST-34 `BLG-GOV-339`) are raised at sprint start, so they can be answered while autonomous work proceeds.

## Multi-EPIC Execution Notes

- **`execution_state.json` owner:** EPIC-01, the first in execution order. Every other EPIC branch must check whether `claude/cycles/2026-10-08__release-v9.11/execution_state.json` exists before creating one. If it exists, the branch reads it and appends its own EPIC section; it never overwrites.
- **Cross-EPIC commit pre-PR check (LL-v9.9-P3-01):** each EPIC branch is cut from `main` and carries only its own `[EPIC-xx]` commits.

## Shared-File Ownership Advisory

| Shared file | EPICs touching it | Canonical owner | Advisory |
|-------------|-------------------|-----------------|----------|
| `docs/reference/openapi.yaml` | EPIC-02 (ST-10 `price_is_stale`, ST-13 `stop_distance_pct`), EPIC-03 (ST-19 new endpoint), EPIC-04 (ST-25 new AI endpoint), EPIC-05 (ST-31 enum, ST-32 examples if docs-side) | EPIC-02 | Union of path/field additions; take the highest version (CLAUDE.md §8). Same-commit contract + OpenAPI rule (CLAUDE.md §2). Later EPICs rebase after EPIC-02 merges. |
| `backend/routers/test.py`, `src/pages/SystemStatus.js` fallback count, `tests/e2e/system-status.spec.js` `SC-SS-01b` | EPIC-03 (ST-19), EPIC-04 (ST-25) | EPIC-03 | Both stories add a route. The fallback count is a single number: EPIC-04 must rebase after EPIC-03 merges and recompute the count from the merged route total, not add 1 to a stale value. |
| `docs/specs/data_model.md` | EPIC-01 (ST-06), EPIC-03 (ST-17, ST-20), EPIC-04 (ST-26), EPIC-05 (ST-30) | EPIC-01 | Keep all migration blocks in ascending version order; highest footer version (CLAUDE.md §8). ST-30 annotates after the others merge. |
| `backend/services/ai_service.py` and prompt modules | EPIC-01 (ST-01, ST-07, ST-08, ST-09), EPIC-02 (ST-12 stored-`holding_days` reader), EPIC-04 (ST-25 new call) | EPIC-01 | ST-25 must use ST-09's pinned model-ID module once EPIC-01 merges. EPIC-02 and EPIC-04 rebase after EPIC-01. |
| `backend/services/portfolio_service.py`, `docs/specs/api_contracts/portfolio_endpoints.md`, `docs/specs/frontend/pages/risk_dashboard.md` | EPIC-02 only | EPIC-02 | Single EPIC; ST-10 lands first (RISK-04). |
| `docs/specs/frontend/pages/reports.md` | EPIC-04 (ST-25 narrative section), EPIC-05 (ST-29 restatement marker) | EPIC-04 | Different sections. EPIC-05 rebases after EPIC-04 merges. Header version: take the next free version (CLAUDE.md §8 step 2a). |
| `tests/e2e/accessibility-axe-scan.spec.js` | EPIC-01 (ST-05 debrief section, if the scan lives here), EPIC-06 (ST-37 Replay page) | EPIC-01 | Combine scan targets; do not drop either. |
| `claude/system/OPERATIONAL_GUIDE.md`, `claude/system/prompt_change_log.md` | EPIC-06 (ST-33 `idea_intake_prompt.md`, ST-34 `roadmap_prompt.md`, ST-35 §13 rule, ST-36 QA evidence template if a governance file) | EPIC-06 | Within one EPIC, so bumps are sequential. Apply the CLAUDE.md §6 checklist per commit and the §8 step 2a per-file version-collision check against anything merged meanwhile. |
| `claude/backlog/backlog.md` (new items only) | EPIC-01 (ST-02 follow-ups), EPIC-02 (ST-12 readers), EPIC-04 (ST-28 review item), any EPIC filing Playwright-gap items | — | Append via `/backlog-add`; new IDs are taken at commit time, so re-check for an ID collision after rebasing. |
| `claude/roadmap/product_value_ratio_history.md` | EPIC-06 (ST-34 only) | EPIC-06 | Single EPIC; named-file write (see above). |
| `claude/strategy/strategy_rules.md` | EPIC-03 (ST-16, only if the ruling changes §6.3) | EPIC-03 | Edit only under the Strategy Rules & System Intent Owner's explicit authority (RISK-05). |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 / ST-01 | Valid. The Condition 2 sign-off is ST-01's first sub-step, raised at sprint start. Does not block the seal. |
| RISK-02 | EPIC-01 / ST-02 | Valid. Human-Delegation to the Infrastructure & Operations Owner at sprint start. The 2026-10-07 production debrief verification may be cited. |
| RISK-03 | EPIC-01 / ST-06; EPIC-03 / ST-17, ST-20 | Valid. DS-17 precedent (`ESC-EXEC-20260921-04`). Code and `data_model.md` proceed regardless. |
| RISK-04 | EPIC-02, EPIC-03, EPIC-04, EPIC-05 | **Changed — widened at planning.** ST-25 also adds an AI endpoint, so `openapi.yaml` and the route-registration chain (`test.py`, `SystemStatus.js`, `SC-SS-01b`) are shared with EPIC-04 too. See the Shared-File Ownership Advisory. |
| RISK-05 | EPIC-03 / ST-16, ST-19 | Valid. Ruling first; ST-19's AC lists every registration step. |
| RISK-06 | EPIC-04 / ST-25 | **Changed — resolved at planning.** Confirmation route ruled 2026-10-08 (see Pre-Sprint Required Decisions). The determination itself stays ST-25's first sub-step; FAIL or a full-review finding goes to `amend cycle`. |
| RISK-07 | EPIC-06 / ST-33, ST-34, ST-35, ST-36 | Valid. ST-34 is `delegated_decision` under the named-file rule; its prompt change waits for `BLG-GOV-339` sign-off. CLAUDE.md §6 checklist and §8 step 2a on every prompt edit. |
| RISK-08 | EPIC-06 / ST-42 | Valid. Human-Delegation to the Infrastructure & Operations Owner. |
| RISK-09 | Release-level | Valid. Product Owner chose a single sprint (2026-10-08). 20 stories are XS/≤0.5d and grouped by file. |

**Multi-vehicle fix-choice check (LP-14):**
- ST-16: the ruling may go either way, but both outcomes only align the on-load and nightly paths and add one test, so effort stays within the 0.5–1d band.
- ST-22: the disposition (client-side guard or accepted risk) is cheaper either way than its XS band.
- ST-21: both outcomes (gate on `send_alert` or a documented comment) are XS.

None materially changes effort. The capacity check is `pass`, so there is no Phasing Recommendation to cross-reference.

## Delegation Classification (set at planning time, per §12 invariant)

| Item | Delegation class | Justification |
|------|-------------------|----------------|
| ST-01 | delegated_decision | AI Compliance & Governance Officer sign-off on the Condition 2 interpretation (AC 4, RISK-01) |
| ST-02 | delegated_qa | A human must exercise all six AI features on a staging deploy with a working Anthropic key (AC 1–2, RISK-02) |
| ST-03, ST-04 | autonomous | Error handling and an import test with no human decision |
| ST-05 | autonomous | BLG-GOV-72 fast-path (c): locked spec (`trade_history.md` v1.15), Playwright listed in the decision record |
| ST-06 | delegated_backend | Live migration on staging and production needs DB write access (AC 3, RISK-03) |
| ST-07, ST-08, ST-09 | autonomous | Prompt text, fixture tests and a model-ID module with no mid-task decision |
| ST-10–ST-15 | autonomous | BLG-GOV-72 fast-path (c): locked specs (`risk_dashboard.md` v0.1.12, `dashboard.md` v3.8, `positions.md` v2.15), Playwright assertions in each decision record |
| ST-16 | delegated_decision | Strategy Rules & System Intent Owner ruling on in-grace behaviour (AC 1, RISK-05) |
| ST-17 | delegated_backend | AC 2 requires new columns applied live with verification output (RISK-03) |
| ST-18, ST-19, ST-21, ST-22 | autonomous | Fixture-tested monitor, new read-only endpoint with the full registration chain, and XS dispositions. ST-22's default is the client-side guard; an accepted-risk disposition would need a Product Owner line in QA evidence. |
| ST-20 | delegated_backend | Live migration (AC 2, RISK-03) |
| ST-23, ST-24, ST-26, ST-27, ST-28 | autonomous | Documents, metric definitions, a counter and a gated backlog item. ST-26: if the count needs a new table rather than existing audit rows, the live migration follows RISK-03 and is recorded as a delegation at that point. |
| ST-25 | delegated_decision | Strategy Rules & System Intent Owner §13 determination, then Product Owner approval of the design decision record (addendum, RISK-06) |
| ST-29–ST-32 | autonomous | Spec and contract reconciliation |
| ST-33, ST-35, ST-36 | autonomous | Governance prompt/template edits under the CLAUDE.md §6 checklist, with no ruling needed (RISK-07) |
| ST-34 | delegated_decision | Named-file write plus `BLG-GOV-339` Head of Specs Team + Product Owner sign-off for the STEP 2.4 change (RISK-07) |
| ST-37–ST-41, ST-43 | autonomous | Test-quality and build hygiene |
| ST-42 | delegated_backend | Branch protection needs repository admin access (RISK-08) |

**Blocked-decision design artefact check (LL-v2.2-SP-01):**
- ST-25 has its design and §13 artefacts scheduled inside the story by the addendum.
- ST-01 is covered by the v8.9 §13 review, and its UI effect is wording only.
- ST-16 and ST-34 have no dedicated HoST design session artefact. Each is scoped by its own AC to resolve the ruling or sign-off as its first sub-step.

Advisory only, not a blocker.

**Test scenario gap (LL-v2.0-P4-2):** this sprint has no `delegated_frontend` items, so the rule does not apply.

## Director of Quality Readiness Check (STEP 4.3)

Every story's AC in `stage4_backlog_slice.md` meets the §7 standard:
- **Technical:** observable outcomes.
- **Quality:** named unit tests, Playwright specs or recorded evidence.
- **Verification:** by recorded evidence or sign-off.
- **Security:** the subject of the AC for ST-03 and ST-06 (AI error/audit logging), ST-19 and ST-25 (new endpoints; ST-25 runs the AI endpoint security checklist), ST-20 and ST-22 (duplicate-write guards), and ST-42 and ST-43 (dependency and build supply chain). N/A for the rest, because no auth, input or data-exposure surface changes.

The Director of Quality confirms the criteria are sufficient for each EPIC's `qa_evidence_EPIC-xx.md`. This confirmation is agent-mediated, consistent with prior cycles. There are no `[AC REQUIRED]` placeholders.

Recorded as non-blocking outstanding actions:
- Two Playwright assertions from the design gate go beyond the slice ACs: the ST-10 Dashboard Card 2 stale notice, and the ST-14 "Day 10 of 10" ended state. Execution adds them, or files a backlog item before the PR opens (CLAUDE.md §2).
- ST-36's DoQ line applies to qualifying stories signed off after it lands: ST-10–ST-14, ST-16–ST-18 and ST-39.

## Pre-Sprint Vulnerability Scan

pre-sprint pip-audit: clean. 60 resolved dependencies scanned via the project virtualenv (`backend/.venv/bin/pip-audit -r backend/requirements.txt --format=json`), 0 vulnerabilities. Trend row appended to `docs/ops/pip_audit_trend_log.md`.

## Capacity Buffer Floor (STEP 1.5)

27.975 / 28.00 = 99.9%, above the 95% advisory floor. Product Owner: **proceed at ceiling**, 2026-10-08. The Product Owner also declined RISK-09's optional two-sprint split: **single sprint**, 2026-10-08.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| RISK-06 §13 route for ST-25 | Strategy Rules & System Intent Owner | Yes — **Done 2026-10-08 (confirmation route)** |
| Condition 2 sign-off for ST-01, raised at sprint start | AI Compliance & Governance Officer | No |
| In-grace recalculation ruling for ST-16, raised at sprint start | Strategy Rules & System Intent Owner | No |
| §13 determination for ST-25 (first sub-step), raised at sprint start | Strategy Rules & System Intent Owner | No |
| `BLG-GOV-339` sign-off for ST-34's STEP 2.4 change | Head of Specs Team; Product Owner | No |
| Human-Delegation: ST-02 staging AI run; ST-06, ST-20 (and ST-17 if needed) live migrations; ST-42 branch protection | Infrastructure & Operations Owner; Data Model & Domain Schema Owner | No |
| Add Playwright for the ST-10 Dashboard Card 2 stale notice and the ST-14 "Day 10 of 10" ended state, or file backlog items before the PR opens | QA & Testing Owner | No |
| `run audit` (v9.10 Carry-Forward #2) before the next Phase 1B | Head of Specs Team | No |
