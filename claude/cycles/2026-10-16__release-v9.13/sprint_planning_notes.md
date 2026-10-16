# Sprint Planning Notes — 2026-10-16__release-v9.13

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-16
**Cycle:** 2026-10-16__release-v9.13

## Backlog Slice Source

Original: `claude/cycles/2026-10-16__release-v9.13/stage4_backlog_slice.md`. `amended_backlog_slice_path` is empty, so no amendment is active. As the design gate requires, the slice is read together with `stage4_backlog_slice_addendum.md`, the post-gate-correction addendum for ST-03, ST-21 and ST-25.

## Preflight Summary (STEP -1)

- **Lifecycle guard:** `status = Design_Gate_Passed`. That is a valid Sprint Planning entry state (`shared_standards.md` §10.1), and the status is not `Amendment_In_Progress`.
- **Release plan sealed:** `state.json` has `status = Published` and `publish_eligible = true`. `open_escalations` and `deferred_execution_blockers` are both empty.
- **Design gate:** required, and `Passed` at 2026-10-16T09:43:20Z (`design_gate.md`). All 40 items are cleared: 10 Design Required, 3 Pre-Approved, 27 Not Applicable. Entry was from `Design_Gate_Passed`, so the bypass audit is skipped.
- **Files, roles and write access:**
  - The slice has 6 EPICs and 40 ST items.
  - The 5 required role files are present: Product Owner, Head of Specs Team, PMO Lead, Director of Quality, FinOps & Resource Architect.
  - `lessons_learnt_prompt.md` and `workforce_capacity.md` are present.
  - `.write_test` was created and deleted.
- **§5 schema-v2 inputs:** the capacity check and execution plan are read from `release_plan.md ## Capacity Check` and `## Execution Plan`.
- **Branch:** `main`.

## Hygiene Advisories (STEP -1.7, -1.8)

- **Prompt change log gaps:** none. Using the date-scan method, every Class 6 prompt's current `**Version:**` is at or below the target version of its latest-dated `prompt_change_log.md` row. Examples: `sprint_planning_prompt.md` v3.22, `execution_prompt.md` v3.87, `roadmap_prompt.md` v9.35, `release_planning_prompt.md` v2.65.
- **Pre-sprint endpoint coverage audit:** clean. `scripts/audit_endpoint_test_coverage.py` exited 0: 93 route decorators across 27 router files, 8 of them documented `KNOWN_GAPS` exclusions, and no undocumented gap.

## Carry-Forward Items

Carry-forward items reviewed: 3 items from cycle `2026-10-12__release-v9.12` (`lessons_learnt_closure.md ## Carry-Forward`):

1. **`next_release` / roadmap "Next planned release":** resolved. Rebalance `2026-10-16__scheduled` committed v9.13 (DL-086), and `next_release = v9.13`.
2. **Stale `Provisional-Target: v9.12` tags:** still open. Release Planning flagged 20 unselected items for `groom backlog`; the tags carry no selection weight. Sprint execution sets `Provisional-Target: TBD` on any new follow-up item unless the roadmap commits it.
3. **Agent-mediated v9.12 DoQ and PO sign-offs:** resolved 2026-10-15 (`release_plan.md` Readiness). For v9.13, the PO decisions recorded at this planning run were made by the user in session.

## Pre-Sprint Required Decisions (STEP -1.5)

`cycle_summary.md ## Pre-sprint Planning Required Decisions` lists one item.

**RISK-02: write route for `claude/strategy/strategy_rules.md`. RESOLVED 2026-10-16 at sprint planning, option (a).**

The user, as Product Owner and with the Strategy Rules & System Intent Owner, authorised named `strategy_rules.md` writes for five stories only:
- **Certain:** ST-38 (§13.3 third paragraph and §13.5 roster row) and ST-39 (§13.5 PO-05 row).
- **Ruling-dependent:** ST-05 (§8, only if the determination amends it), ST-06 (§5, only if the ruling changes stop behaviour) and ST-07 (named exception next to §7.2, only if the exception branch is taken).

Execution conditions:
- Each commit cites the authorisation line in the story's `sprint_backlog.md` Notes.
- EPIC-06 owns the file. ST-38 and ST-39 share one version bump.
- Bumps are taken in merge order, and a later-merging branch rebases and takes the next free version, after CLAUDE.md §8 step 2a's per-file collision check.
- Each edit adds a Change Log row and records the §15 grep where its AC requires one.

This authorisation does not widen `execution_prompt.md` §7's named-file rule. It applies only to these five stories, as an explicit user instruction (v9.9 ST-20 precedent).

No other pre-sprint decision is unresolved.

## Pre-Sprint Backlog Advisory

`backlog.md` has no items with `Provisional-Target: Before v9.13 sprint planning`.

## Pre-Seal Stale-Feature-Target Check (STEP 3.1)

Each of the 40 source items has exactly one live heading in `claude/backlog/backlog.md`, and none appears in `backlog_archive.md`. Release Planning had already excluded the done or resolved items (`BLG-GOV-142`, `-360`, `-361`, `-368`, `-374`, `BLG-SPEC-199`, `BLG-FE-195`). No item is classified `flag`.

## Named-File Write Check (STEP 3.1)

- Named-file write: `claude/roadmap/role_share_history.md` (v9.8–v9.10 rolling line, compound count) — authorised under execution_prompt.md §7 named-file rule (ST-40, `delegated_decision` as the slice states).

Other governed writes, which are not named-file writes under the `claude/roadmap/*` / `backlog.md` rule:
- **`claude/strategy/strategy_rules.md`:** ST-05, ST-06, ST-07 (ruling-dependent), ST-38 and ST-39. The named-file rule excludes this file. These writes are covered by the RISK-02 option (a) authorisation above.
- **New backlog items:** added via `/backlog-add` under execution's new-item exception, by ST-24 (exposed defects and uncovered actions), ST-34 (approved upgrades), ST-16 (any styling change) and any story filing a Playwright-gap or staging-deferral item. No existing item is edited.
- **ST-35:** the per-item ready-pool view goes in the PR description, not `backlog.md`.
- **Class 1 rule:** ST-25 adds the coloured-button rule to `design_system.md`, as the addendum directs.
- **Governance prompts:** no story edits a file under `claude/system/`, so the CLAUDE.md §6 checklist is not triggered this sprint.

No write to an existing `backlog.md` item's `Scope`, `Acceptance Criteria` or `Gate criteria` field is planned, so no separate Product Owner confirmation line is needed (§6.2).

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | None. All 40 slice items are in sprint scope. | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | Live backfill and CHECK constraint on staging and production | External: Human-Delegation, Data Model & Domain Schema Owner + Infrastructure & Operations Owner | RISK-01, raise at sprint start. Docs proceed regardless |
| ST-03 | ST-02 (§8 category), ST-01 (ExitModal) | Internal | Open, sequenced |
| ST-05 | Strategy Rules & System Intent Owner determination | Governance (first sub-step) | Raise at sprint start. The interim label proceeds regardless |
| ST-06 | Strategy Rules & System Intent Owner ruling (reject or floor) | Governance (first sub-step) | Raise at sprint start |
| ST-07 | Strategy Rules & System Intent Owner choice (align or exception) | Governance (first sub-step) | Raise at sprint start; default is to align the code |
| ST-08 | API Contracts & Documentation Owner choice (400 or warning) | Governance (first sub-step) | Raise at sprint start; default 400 |
| ST-05, ST-06, ST-07 `strategy_rules.md` edits | ST-38/ST-39 bump, if EPIC-06 merges first | Cross-EPIC (version sequencing) | Merge-order bumps, CLAUDE.md §8 step 2a |
| ST-10 | Manual check against a deployed environment | External: user permission for live DB read | Raise when the panel is built |
| ST-16 | ST-15; AI Compliance & Governance Officer sign-off | Internal + Governance | Open, sequenced; raise at sprint start |
| ST-17 | ST-15; AI Compliance & Governance Officer sign-off | Internal + Governance | Open, sequenced; raise at sprint start |
| ST-18 | AI Compliance & Governance Officer sign-off | Governance (first sub-step) | Raise at sprint start |
| ST-21 | ST-20 (same file) | Internal | Open, sequenced |
| ST-22 | Live migration on staging and production | External: Human-Delegation, Data Model & Domain Schema Owner | RISK-01, raise at sprint start |
| ST-22 | EPIC-02 registration chain on `main` | Cross-EPIC (endpoint count) | Recompute the count after rebasing |
| ST-23 | ST-01 (EPIC-01) on `main` | Cross-EPIC | EPIC-01 merges first |
| ST-24 | ST-01 (EPIC-01) on `main`; ST-23 | Cross-EPIC + Internal | EPIC-04 merges last |
| ST-27 | Director of Quality review | Governance (first sub-step) | Raise at sprint start |
| ST-28 | Real failed-run Telegram receipt | External: Human-Delegation, Infrastructure & Operations Owner | RISK-01, raise at sprint start |
| ST-29 | Render dashboard hooks, GitHub secrets, live staging run | External: Human-Delegation, Infrastructure & Operations Owner | RISK-01, raise at sprint start (other stories' staging checks rely on it) |
| ST-30 | Live usage figures | External: possible Human-Delegation | RISK-01, raise at sprint start |
| ST-31 | ST-30; live usage data for the top-3 report | Internal + External | Open, sequenced |
| ST-32 | Full-universe screener run on a deployed environment | External: possible Human-Delegation | RISK-01, raise at sprint start |
| ST-33 | Infrastructure & Operations Owner + FinOps & Resource Architect sign-off | Governance (closing sub-step) | Open |
| ST-36 | ST-35 (same script) | Internal | Open, sequenced |
| ST-39 | ST-38 (shared version bump) | Internal | Open, sequenced |

**Spec dependencies:** the design gate locked every Design Required and Pre-Approved frontend spec:
- `positions.md` v2.20
- `trade_history.md` v1.16
- `reflections.md` v0.3
- `trade_reflection.md` v0.4
- `red_flag_journal.md` v1.4
- `signals.md` v0.5
- `components/position_form.md` v1.10
- `system_status.md` v1.3
- `screener_results.md` v1.10
- `components/cash_management_modal.md` v1.3
- `replay_mode.md` v0.4
- `reports.md` v0.24
- `trade_plan.md` v1.19

Eight decision records are in place under `docs/design/2026-10-16__release-v9.13/`. For ST-05 and ST-06, the specs are conditional on the ruling, and the branch not taken is deleted in the story's own commit.

**No circular dependencies.** Every edge runs from a later-sequenced story to an earlier one. The cross-EPIC edges (ST-23/ST-24 → ST-01, ST-22 → EPIC-02's registration chain, and the `strategy_rules.md` bump sequence) all run one way.

## Execution Sequence

EPIC merge sequence: **EPIC-01 → EPIC-06 → EPIC-02 → EPIC-03 → EPIC-05 → EPIC-04.**

- **EPIC-01** goes first because it carries the P1 anchor and ST-23/ST-24 need ST-01 on `main`. It owns `execution_state.json`.
- **EPIC-06** goes second. It is small, its gate-scan fixes help the next Release Planning run, and it takes the certain `strategy_rules.md` bump early.
- **EPIC-02** and then **EPIC-03** follow. EPIC-02 owns `openapi.yaml` and the registration chain. EPIC-03's ST-22 rebases onto them and recomputes the endpoint count.
- **EPIC-05** goes fifth because its live delegations run longest.
- **EPIC-04** goes last. ST-24's fixture and ST-23's check then run over the final tree, and ST-25's global `cn()` change lands once (RISK-05).

**Fallback:** if EPIC-05 is still waiting on delegations, EPIC-04 may merge ahead of it. EPIC-05 then rebases and must pass ST-23's check and ST-24's fixture before its PR merges.

1. **EPIC-01:** ST-01 → ST-03 (after ST-02's spec half); ST-02 (live half delegated at sprint start); ST-04 in parallel; ST-05 (interim label first; determination raised at sprint start)
2. **EPIC-06:** ST-35 → ST-36; ST-38 → ST-39 (one bump); ST-37, ST-40 in parallel
3. **EPIC-02:** ST-09, ST-10, ST-11, ST-12, ST-13, ST-14 (autonomous) first; ST-06, ST-07, ST-08 as their rulings arrive
4. **EPIC-03:** ST-15 → ST-16 → ST-17; ST-19; ST-20 → ST-21; ST-18 (sign-off); ST-22 (migration delegated, registration chain after EPIC-02)
5. **EPIC-05:** ST-29 first (restores staging deploys); ST-28; ST-30 → ST-31; ST-32; ST-33; ST-34
6. **EPIC-04:** ST-25, ST-26, ST-27 (decision raised at sprint start); ST-23 → ST-24 last, over the final tree

Autonomous items run before delegated ones within each EPIC wherever dependencies allow. Every Human-Delegation request and every ruling or sign-off is raised at sprint start, so answers can come in while autonomous work proceeds:
- **Human-Delegation:** ST-02 and ST-22 live changes; ST-28 Telegram receipt; ST-29 Render dashboard and live run; ST-30/ST-31 live usage; ST-32 full-universe run; ST-10 manual check.
- **Rulings and sign-offs:** ST-05, ST-06, ST-07, ST-08, ST-16, ST-17, ST-18, ST-27, ST-33, plus ST-16's AC 4 styling answer from the Head of UX & Design.

## Multi-EPIC Execution Notes

- **`execution_state.json` owner:** EPIC-01, the first in execution order. Every other EPIC branch must check whether `claude/cycles/2026-10-16__release-v9.13/execution_state.json` exists before creating one. If it exists, the branch reads it and appends its own EPIC section, and never overwrites it.
- **Cross-EPIC commit pre-PR check (LL-v9.9-P3-01):** each EPIC branch is cut from `main` and carries only its own `[EPIC-xx]` commits.
- **Escalation mirroring (LL-v9.11-P3-02):** every `ESC-EXEC-*` record raised for a delegation above is mirrored into `.claude_current_state.json.open_escalations`.
- **Backlog integrity (CLAUDE.md §8 step 2c):** run `scripts/check_backlog_item_integrity.py` after every merge that touches `backlog.md`.

## Shared-File Ownership Advisory

| Shared file | EPICs touching it | Canonical owner | Advisory |
|-------------|-------------------|-----------------|----------|
| `claude/strategy/strategy_rules.md` | EPIC-06 (ST-38, ST-39), EPIC-01 (ST-05, ruling-dependent), EPIC-02 (ST-06, ST-07, ruling-dependent) | EPIC-06 | Writes authorised for these five stories only (RISK-02 option (a)). Bumps go in merge order, and a later branch takes the next free version. Apply CLAUDE.md §8 step 2a per file. |
| `docs/reference/openapi.yaml` | EPIC-02 (ST-08; ST-10 if a route is added), EPIC-03 (ST-22), EPIC-05 (ST-28), EPIC-04 (ST-23 reads it) | EPIC-02 | Take the union of path and field additions and the highest version (CLAUDE.md §8). The contract and OpenAPI change go in the same commit (CLAUDE.md §2). |
| `backend/routers/test.py`, `src/pages/SystemStatus.js` fallback count, `tests/e2e/system-status.spec.js` `SC-SS-01b` | EPIC-03 (ST-22), EPIC-02 (ST-10 if a route is added) | EPIC-02 | The fallback count is one number. EPIC-03 rebases after EPIC-02 merges and recomputes the count from the merged `test.py`; it does not add 1 to a stale value. |
| `docs/specs/data_model.md` | EPIC-01 (ST-02), EPIC-03 (ST-22); EPIC-06 ST-37 reads it | EPIC-01 | Keep migration blocks in ascending version order, with the highest footer version. |
| `docs/specs/metrics_definitions.md` | EPIC-01 (ST-02), EPIC-02 (ST-10, ST-11), EPIC-03 (ST-22) | EPIC-01 | Three EPICs bump it. Apply CLAUDE.md §8 step 2a's version-collision check on every merge. |
| `docs/specs/api_contracts/ai_endpoints.md` | EPIC-03 (ST-18, ST-19, ST-22), EPIC-05 (ST-28) | EPIC-03 | EPIC-05 rebases after EPIC-03. |
| `src/lib/utils.js` `cn()` / `Button`, `tests/e2e/accessibility-axe-scan.spec.js` `KNOWN_VIOLATIONS` | EPIC-04 (ST-25, ST-26), EPIC-03 (ST-21), and any new coloured button in EPIC-01 (ST-01 queue) or EPIC-03 (ST-22 rating control) | EPIC-04 (`cn()`); EPIC-03 (`KNOWN_VIOLATIONS` until EPIC-04 merges) | New coloured buttons in earlier EPICs follow the existing `!bg-` workaround. ST-25 removes it everywhere in its own commit, over the final tree. |
| `src/api/base44Client.js` | EPIC-01 (ST-01 removes `Position.update`), EPIC-04 (ST-23 allow-lists dead methods) | EPIC-01 | ST-23 is written against `main` after EPIC-01 merges. |
| `src/components/positions/ExitModal.js`, `src/constants/exitReasons.js` | EPIC-01 only (ST-01, ST-03) | EPIC-01 | Single EPIC. |
| `backend/services/ai_service.py` | EPIC-03 only (ST-15–ST-19) | EPIC-03 | Single EPIC. Sequence ST-15 → ST-16 → ST-17. |
| Gate-scan script (Release Planning §1.3a tooling) | EPIC-06 only (ST-35, ST-36) | EPIC-06 | Single EPIC. |
| `.github/workflows/` | EPIC-05 (ST-28 `ai-daily-cost-check.yml`, ST-29 `staging-deploy.yml`), EPIC-04 (ST-23 quality gate) | — | Different files. No conflict expected. |
| Playwright suite fixtures | EPIC-04 (ST-24 suite-wide 404/405 fixture); every EPIC adding specs | EPIC-04 | ST-24 applies the fixture to the merged suite. Specs added earlier are covered when it lands. |
| `claude/backlog/backlog.md` | Any EPIC (new items only) | — | Append via `/backlog-add`. Re-check new IDs after rebasing. Run the integrity check (§8 step 2c). |
| `claude/roadmap/role_share_history.md` | EPIC-06 (ST-40 only) | EPIC-06 | Named-file write (above). |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 / ST-02; EPIC-03 / ST-22; EPIC-05 / ST-28–ST-32; EPIC-02 / ST-10 | Valid. Human-Delegation at sprint start (v9.11/v9.12 precedent); code and docs proceed regardless. ST-10 is added because AC 2's manual check needs a live read, which the user must permit. |
| RISK-02 | EPIC-01 / ST-05; EPIC-02 / ST-06, ST-07; EPIC-06 / ST-38, ST-39 | **Changed: resolved 2026-10-16, option (a).** Named writes are authorised for these five stories. EPIC-06 owns the file, and bumps go in merge order. |
| RISK-03 | EPIC-02 / ST-06, ST-07, ST-08; EPIC-03 / ST-16, ST-17, ST-18; EPIC-04 / ST-27; EPIC-01 / ST-05 | Valid. Each ruling is a first sub-step, and those stories are classed `delegated_decision`. ST-07 and ST-08 have no-strategy-change defaults. |
| RISK-04 | All EPICs | Valid. `ai_endpoints.md` is added to the shared set (EPIC-03 and EPIC-05 ST-28). See the Shared-File Ownership Advisory. |
| RISK-05 | EPIC-04 / ST-24 | Valid. ST-24 runs after ST-01 and ST-23, and EPIC-04 merges last. The Product Owner kept it as one story (2026-10-16). Exposed defects are filed, not fixed. |

**Multi-vehicle fix-choice check (LP-14):**
- **ST-05:** a §8 amendment (strategy edit, Change Log row, signal kept) and a withdrawal (retire `rebalance-exit.yml` and the signal path) have similar effort. The pessimistic case adds about 0.25d.
- **ST-06:** reject (400 with submit disabled) or floor. Both are designed and of similar effort.
- **ST-07:** aligning the code is the 0.15d default. The exception branch is text only.
- **ST-08:** 400 is the default. A deprecation warning field adds a response-shape change, about +0.25d.

If every pessimistic case hit at once, the total would be about 28.5d, just over the 28d ceiling. The capacity check is `pass`, so there is no Phasing Recommendation to cross-reference. If more than one pessimistic case materialises, raise it at the mid-sprint review. Out-of-scope work goes through `amend cycle`, not informal deferral.

## Delegation Classification (set at planning time, per §12 invariant)

| Item | Delegation class | Justification |
|------|-------------------|----------------|
| ST-01, ST-03, ST-04, ST-25, ST-26 | autonomous | BLG-GOV-72 fast-path (c): locked frontend specs and decision records from the design gate, with Playwright in each AC |
| ST-09, ST-13, ST-20 | autonomous | Design Pre-Approved against locked references |
| ST-10 | autonomous | Locked spec and decision record. AC 2's manual check is staging-only evidence that needs the user's permission for a live read |
| ST-21 | autonomous | Applies the v9.12 light-theme token rule; the tokens are fixed in the addendum |
| ST-11, ST-12, ST-14, ST-15, ST-19 | autonomous | Spec text, tests and prompt-context changes covered by fixtures |
| ST-23, ST-24 | autonomous | CI and test tooling. Exposed defects are filed, not fixed |
| ST-34 | autonomous | Assessment; approved upgrades are filed as new items |
| ST-35, ST-36, ST-37 | autonomous | Governance and spec tooling, tested with fixtures |
| ST-38, ST-39 | autonomous | Text-only edits authorised under RISK-02 option (a) at this planning run; no further decision is needed |
| ST-05, ST-06, ST-07 | delegated_decision | Strategy Rules & System Intent Owner ruling first (RISK-03) |
| ST-08 | delegated_decision | API Contracts & Documentation Owner choice first; default 400 |
| ST-16, ST-17, ST-18 | delegated_decision | AI Compliance & Governance Officer sign-off first |
| ST-27 | delegated_decision | Director of Quality reviews the isolation decision |
| ST-33 | delegated_decision | Infrastructure & Operations Owner and FinOps & Resource Architect sign off the accepted-risk statement |
| ST-40 | delegated_decision | Named-file write; kept as the slice states (`ESC-CLOSE-20261006-01`) |
| ST-02, ST-22 | delegated_backend | Live constraint/backfill and migration on staging and production (RISK-01) |
| ST-28, ST-29 | delegated_backend | Real Telegram receipt; Render dashboard hooks, secrets and a live run (RISK-01) |
| ST-30, ST-31, ST-32 | delegated_backend | Live usage data and a full-universe run on a deployed environment (RISK-01) |

Totals: 23 autonomous, 10 `delegated_decision`, 7 `delegated_backend`. No `delegated_frontend` and no `delegated_qa`.

**Blocked-decision design artefact check (LL-v2.2-SP-01):**
- ST-05 and ST-06 have design artefacts with both branches designed (`rebalance-exit-interim-label/`, `initial-stop-at-or-below-zero/`).
- ST-07, ST-08, ST-16, ST-17, ST-18, ST-27, ST-33 and ST-40 have no dedicated HoST design session artefact. Each is a ruling or sign-off with no UI design surface, which its own AC scopes as a sub-step.

Advisory only, not a blocker.

**Test scenario gap (LL-v2.0-P4-2):** no `delegated_frontend` items, so the rule does not apply.

## Acceptance Criteria Confirmation and Director of Quality Readiness Check (STEP 4)

Every story's AC in `stage4_backlog_slice.md`, read with the addendum, meets the §7 standard:
- **Technical:** observable outcomes.
- **Quality:** named unit tests, Playwright specs, CI checks or recorded evidence.
- **Verification:** by recorded evidence, a run URL or a sign-off.
- **Security:** the subject of the AC for:
  - ST-02: a CHECK constraint rejects unlisted values.
  - ST-06: no stored stop ≤ 0.
  - ST-08: fixed strategy fields rejected or flagged on write.
  - ST-15–ST-18: AI output safety (unknown tickers, stop citations, prescriptive language).
  - ST-22: a new write route; not an AI-calling endpoint, so the AI endpoint checklist is not triggered (design gate §13 pre-check).
  - ST-23/ST-24: calls to missing routes caught in CI.
  - ST-29: each deploy ID checked against the expected service.
  - ST-34: dependency supply chain (assessment).
  - Elsewhere N/A, because no auth, input or data-exposure surface changes.

There are no `[AC REQUIRED]` placeholders. Three design gate clarifications (ST-03, ST-21, ST-25) are carried in the sprint backlog's Notes from the addendum. They do not change the sealed AC.

The Director of Quality confirms that the criteria are sufficient for each EPIC's `qa_evidence_EPIC-xx.md`. As in prior cycles, this confirmation is agent-mediated.

**Staging-only ACs** are listed per story in `sprint_backlog.md`: ST-02, ST-10, ST-22, ST-28, ST-29, ST-30, ST-31 and ST-32. If a staging sign-off is deferred past merge, a backlog item is filed before the PR opens.

## Pre-Sprint Vulnerability Scan

Pre-sprint pip-audit: clean. The scan ran through the project virtualenv (`backend/.venv/bin/pip-audit -r backend/requirements.txt --format=json`), with 0 vulnerabilities across 53 resolved dependencies (52 at v9.12). A trend row was appended to `docs/ops/pip_audit_trend_log.md`.

## Capacity Buffer Floor (STEP 1.5)

28.00 / 28.00 = 100%, above the 95% advisory floor. Product Owner: **proceed at ceiling**, single sprint, ST-24 not split, 2026-10-16. Both addendum estimate checks (ST-03, ST-21) are held; see `sprint_capacity.md`.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| RISK-02 write route for `strategy_rules.md` | Strategy Rules & System Intent Owner; Product Owner | Yes. **Done 2026-10-16 (option (a))** |
| Addendum estimate checks for ST-03 and ST-21 | PMO Lead; Product Owner | Yes. **Done 2026-10-16 (both held)** |
| Determination for ST-05, rulings for ST-06 and ST-07, raised at sprint start | Strategy Rules & System Intent Owner | No |
| Behaviour choice for ST-08 | API Contracts & Documentation Owner | No |
| Sign-offs for ST-16, ST-17 and ST-18, and ST-16 AC 4's styling answer | AI Compliance & Governance Officer; Head of UX & Design | No |
| Isolation decision review for ST-27 | Director of Quality | No |
| Accepted-risk sign-off for ST-33 | Infrastructure & Operations Owner; FinOps & Resource Architect | No |
| Human-Delegation: ST-02 and ST-22 live changes; ST-28 Telegram receipt; ST-29 Render dashboard and live run; ST-30/ST-31 live usage; ST-32 full-universe run; ST-10 live read (user permission) | Infrastructure & Operations Owner; Data Model & Domain Schema Owner | No |
| For staging-only ACs deferred past merge, file backlog items before the PR opens | QA & Testing Owner | No |
