# Sprint Planning Notes — 2026-10-06__release-v9.10

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-06
**Cycle:** 2026-10-06__release-v9.10

## Backlog Slice Source

Original — `claude/cycles/2026-10-06__release-v9.10/stage4_backlog_slice.md` (`amended_backlog_slice_path` is empty; no amendment is active).

## Preflight Summary (STEP -1)

- **Lifecycle guard:** `status = Design_Gate_Passed`, which is a valid Sprint Planning entry state (`shared_standards.md` §10.1). Not `Amendment_In_Progress`.
- **Release plan sealed:** `state.json` has `status = Published` and `publish_eligible = true`. `open_escalations` and `deferred_execution_blockers` are both empty.
- **Design gate:** required, `Passed` (2026-10-06T14:30Z, `design_gate.md`). Entered from `Design_Gate_Passed`, so the bypass audit is skipped.
- **Files, roles and write access:** the slice has 4 EPICs and 21 ST items. The 5 required role files (Product Owner, Head of Specs Team, PMO Lead, Director of Quality, FinOps & Resource Architect) are present with matching `**Role:**` lines. `lessons_learnt_prompt.md` is present. The `.write_test` file was created and deleted.
- **§5 schema-v2 inputs:** this cycle has no standalone `stage4_5_capacity_check.md` or `stage3_execution_plan.md`. The release plan is schema v2 (`prompt_schema_version: v2`), so these are read from `release_plan.md ## Capacity Check` and `## Execution Plan`, per §5 and STEP 0.
- **Branch:** `main`.

## Carry-Forward Items

There are 3 carry-forward items from cycle `2026-09-30__release-v9.9` (`lessons_learnt_closure.md ## Carry-Forward`):

1. `ESC-CLOSE-20261006-01` is open. It is resolved at this planning run; see Pre-Sprint Required Decisions below.
2. `BLG-FE-193`'s gate is met. It is seated as ST-06.
3. `BLG-GOV-368`'s prompt half is already applied. Release planning did not re-seat it, and it is for Backlog Management (`groom backlog`), not this routine.

## Pre-Sprint Required Decisions (STEP -1.5)

`cycle_summary.md ## Pre-sprint Planning Required Decisions` lists one item.

**RISK-03 — `ESC-CLOSE-20261006-01` write-scope ruling: RESOLVED 2026-10-06.**

Ruling given by the user acting as **Head of Specs Team**, the escalation's owning authority. The role was checked before acting, per the CLAUDE.md §2 role-ownership rule. Sprint Planning runs as PMO Lead, which is not the owning role, so the mismatch was flagged and the ruling was taken explicitly under the Head of Specs Team role. The ruling adopts `BLG-GOV-362`'s principle, the **named-file rule**:

- **Covered:** a sealed AC that names an exact `claude/roadmap/*` file may be written by Sprint Execution in-sprint. The write must stay within what that AC names. The existing prioritisation, scope and capacity exclusions on roadmap content still apply.
- **ST-20 delivery:** ST-20 edits `claude/roadmap/current_roadmap.md`'s PO-05 wording directly, in-sprint, within its sealed AC 2. It does not route through the Roadmap Rebalance Engine. ST-20 is classified `delegated_decision`, and RISK-03 stays on it as the tracking risk. This is the planning-time pre-seal classification check from `BLG-GOV-362` proposal 2, applied as practice now.
- **Not covered:** edits to fields of existing `backlog.md` items. Release Planning §1.3a's in-place gate-text edits are also not covered. Both stay out of scope, recorded in manifests only, until `BLG-GOV-362`'s prompt patches ship.
- **Prompt patches:** the `execution_prompt.md` §7 exception and the `sprint_planning_prompt.md` pre-seal check are **not** applied by this routine. Governance files are outside its write scope. They ship through `BLG-GOV-362`, with the full CLAUDE.md §6 checklist. Until then, this ruling is the cited authority for ST-20's `current_roadmap.md` write. Sprint Execution should quote it in ST-20's commit and QA evidence.
- **Escalation record:** the disposition in `claude/cycles/2026-09-30__release-v9.9/closure_escalations.md` and the `open_escalations` entry in `.claude_current_state.json` are both outside this routine's write scope. They are still recorded as `Open`, and their SLA is due 2026-10-09T00:00Z. That is a non-blocking outstanding action; see below.

There are no other unresolved pre-sprint decisions.

## Pre-Sprint Backlog Advisory

`backlog.md` has no items with `Provisional-Target: Before v9.10 sprint planning`.

## Pre-Seal Stale-Feature-Target Check (STEP 3.1)

All 21 source items (`BLG-BE-138` … `BLG-GOV-357`) are live in `claude/backlog/backlog.md`, and none is in `backlog_archive.md`. Release planning already deferred `BLG-GOV-368`, `BLG-GOV-142` and `BLG-GOV-360` as done. No candidate targets a feature that has already shipped, so no item is flagged.

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | None. All 21 slice items are in sprint scope. | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal (same `position_service.py` paths) | Open — sequenced |
| ST-03 | ST-01 (parameter-authority ruling, AC 2) | Internal (settings-change text depends on the ruling) | Open — sequenced |
| ST-05 | ST-01 (if the ruling bumps `strategy_rules.md`), ST-11, ST-13 | Internal / cross-EPIC (registry must match any qualifying `strategy_rules.md` Change Log row) | Open — see note 1 |
| ST-06 | ST-01 (ruling and the `stop_calculation_source` field) | Cross-EPIC | Open — sequenced |
| ST-06 | ST-02 (`atr_source`) | Cross-EPIC, optional | Not required |
| ST-07 | ST-01 (single fallback-multiplier source) | Cross-EPIC | Open — sequenced |
| ST-09 | ST-08 (shared exit-condition predicate) | Internal | Open — sequenced |
| ST-12 | ST-11 (post-grace badge copy only) | Internal, partial | In-grace work is unblocked |
| ST-14 | ST-13 (§13.3 ruling) | Internal | Open — sequenced |
| ST-01 | Production `settings` read (AC 1) | External — Human-Delegation, Infrastructure & Operations Owner | RISK-01 — raise at sprint start |
| ST-18 | Live Render/GitHub Actions control | External — Human-Delegation, Infrastructure & Operations Owner | RISK-04 — raise at sprint start |
| ST-16 | Live `claude_audit_log` read (only if needed) | External — Human-Delegation, conditional | RISK-04 — code-path audit proceeds regardless |
| ST-20 | `ESC-CLOSE-20261006-01` ruling | Governance | Resolved 2026-10-06 (named-file rule) |

**Spec dependencies:** the design gate has locked the frontend specs for every UI item (`positions.md` v2.11, `dashboard.md` v3.7, `settings.md` v1.7, `position_form.md` v1.7). The ruling-conditional designs for ST-01, ST-12 and ST-14 specify every outcome, so no spec lock is outstanding.

**Note 1 — strategy-version registry coupling:** ST-05's new test fails when a qualifying `strategy_rules.md` Change Log row has no registry entry. ST-01 (ruling b/c), ST-11 (overlay-canonical) and ST-13 can each add such a row. Whichever of those lands after ST-05 must add the matching registry entry in the same commit. Whichever lands before ST-05 is picked up by ST-05's own registry update.

**No circular dependencies.** Every edge points from a later-sequenced story to an earlier one.

## Execution Sequence

EPIC merge sequence: **EPIC-01 → EPIC-03 → EPIC-04 → EPIC-02**. EPICs carrying `delegated_decision` rulings are front-loaded so their external dependencies are raised early. EPIC-02, which is mostly autonomous UI work and depends on ST-01, merges last.

1. **EPIC-01:** ST-01 (ruling sub-step first; raise the RISK-01 production-read delegation at sprint start) → ST-04 (independent, runs in parallel with the ruling wait) → ST-02 → ST-03 → ST-05
2. **EPIC-03:** ST-11 (ruling) and ST-13 (ruling) raised at sprint start → ST-12 (in-grace work immediately; post-grace copy after ST-11) → ST-14 (after ST-13)
3. **EPIC-04:** ST-17, ST-19 and ST-21 (autonomous) → ST-15, ST-16 and ST-20 (`delegated_decision`) → ST-18 (`delegated_backend`; raise the RISK-04 delegation at sprint start)
4. **EPIC-02:** ST-10 and ST-08 (no ST-01 dependency) → ST-09 → ST-06 and ST-07 (after the ST-01 ruling)

Autonomous items run before delegated items within each EPIC wherever dependencies allow. All Human-Delegation requests (ST-01 production read, ST-18 live fire, and ST-16 if needed) and all Strategy Rules & System Intent Owner rulings (ST-01, ST-05, ST-11, ST-13) are raised at sprint start, so they can be answered while autonomous work proceeds.

## Multi-EPIC Execution Notes

- **`execution_state.json` owner:** EPIC-01, the first in execution order. Every other EPIC branch must check whether `claude/cycles/2026-10-06__release-v9.10/execution_state.json` exists before creating one. If it exists, the branch reads it and appends its own EPIC section; it never overwrites.
- **Cross-EPIC commit pre-PR check (LL-v9.9-P3-01):** each EPIC branch is cut from `main` and carries only its own `[EPIC-xx]` commits.

## Shared-File Ownership Advisory

| Shared file | EPICs touching it | Canonical owner | Advisory |
|-------------|-------------------|-----------------|----------|
| `claude/strategy/strategy_rules.md` | EPIC-01 (ST-01 §12 if ruling b/c), EPIC-03 (ST-11 §9, ST-13 §13.3/§4.2.3) | EPIC-01 | Requires Strategy Rules & System Intent Owner authority (RISK-02). EPIC-03 rebases onto `main` after EPIC-01 merges, before finalising its edit. Each edit carries its own Change Log row and the §15 grep. |
| `backend/strategy_version_registry.py` | EPIC-01 (ST-05), EPIC-03 (if ST-11/ST-13 add a qualifying Change Log row) | EPIC-01 | See Dependency Map note 1. |
| `docs/specs/api_contracts/position_endpoints.md`, `docs/reference/openapi.yaml` | EPIC-01 (ST-01 `stop_calculation_source`, ST-02 `atr_source`, ST-03 wording), EPIC-03 (ST-12 `lifecycle_reason`, ST-14 `reasons` enum) | EPIC-01 | Union of field additions; take the highest version (CLAUDE.md §8). Same-commit contract and OpenAPI rule applies (CLAUDE.md §2). |
| `docs/specs/data_model.md` | EPIC-01 (ST-02 `atr_source` migration, ST-05 DS-11) | EPIC-01 | Single EPIC; no contention. |
| `docs/specs/frontend/pages/positions.md` | EPIC-02 (ST-06, ST-08), EPIC-03 (ST-12, ST-14) | EPIC-03 (merges first) | The design gate already bumped it to v2.11. Execution spec-sync edits that remove unchosen ruling branches belong to EPIC-03. EPIC-02 rebases after EPIC-03 merges. |
| `src/pages/Positions.js`, `src/components/positions/PositionCard.js` | EPIC-02 (ST-06, ST-08), EPIC-03 (ST-12, ST-14) | EPIC-03 | EPIC-02 rebases onto `main` after EPIC-03 merges, before finalising. |
| `backend/services/position_service.py` | EPIC-01 (ST-01, ST-02), EPIC-03 (ST-12 lifecycle reason, if routed there) | EPIC-01 | EPIC-03 rebases after EPIC-01. |
| `claude/system/prompt_change_log.md` | Any EPIC touching a governance prompt | — | Append-only; low conflict risk. |
| `claude/roadmap/current_roadmap.md` | EPIC-04 (ST-20 only) | EPIC-04 | Single EPIC; written under the RISK-03 named-file ruling. |
| `tests/e2e/system-status.spec.js`, `src/pages/SystemStatus.js`, `backend/routers/test.py` | Only if any story adds a route (none planned) | — | The CLAUDE.md §2 registration rule applies if a route is added. |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 / ST-01 (gates ST-03, ST-06, ST-07) | Valid. The ruling is phased as ST-01's first sub-step. The production-read Human-Delegation (Infrastructure & Operations Owner) is raised at sprint start. Dependants are sequenced after the ruling. |
| RISK-02 | EPIC-03 / ST-11, ST-13 (and EPIC-01 / ST-01 under ruling b/c) | Valid. Each ruling names whether `strategy_rules.md` changes. Any edit needs explicit Strategy Rules & System Intent Owner authority and follows the v9.9 ST-20 precedent. |
| RISK-03 | EPIC-04 / ST-20 | **Changed — resolved at planning.** `ESC-CLOSE-20261006-01` was ruled on 2026-10-06 (named-file rule, see above). Kept on ST-20 as a tracking risk, which is why ST-20 is `delegated_decision`. |
| RISK-04 | EPIC-04 / ST-18, ST-16 | Valid. Expected Human-Delegation, as in v9.6–v9.9. |
| RISK-05 | EPIC-02 (ST-06–ST-10), EPIC-03 (ST-12, ST-14), EPIC-01 (ST-01 Settings fallbacks) | Valid. The design gate has passed. Each observable AC needs Playwright coverage or a recorded staging run. **Added at planning:** ST-01's Settings fallback assertion is not named in its slice AC (`design_gate.md` Playwright note), so execution must add Playwright for it or file a backlog item before EPIC-01's PR opens. |

**Multi-vehicle fix-choice check (LP-14):** ST-01's three ruling outcomes (a/b/c) and ST-14's two dispositions are alternative vehicles. None materially changes effort beyond the band midpoint already sized. Outcome (b) adds a §12 override record plus parity enforcement, which fits within ST-01's 3-5d band. Capacity check is `pass`, so there is no Phasing Recommendation to cross-reference. Resolve at kickoff.

## Delegation Classification (set at planning time, per §12 invariant)

| Item | Delegation class | Justification |
|------|-------------------|----------------|
| ST-01 | delegated_decision | Parameter-authority ruling (Strategy Rules & System Intent Owner) plus production read (Human-Delegation, RISK-01) plus a Product Owner correction decision for diverged stops (AC 6) |
| ST-02, ST-03, ST-04 | autonomous | Backend change, contract wording and tests with no human decision. ST-03 waits on ST-01's ruling as a dependency, not a decision of its own. |
| ST-05 | delegated_decision | Registry-coverage ruling by the Strategy Rules & System Intent Owner (AC 1) |
| ST-06, ST-07, ST-08, ST-09, ST-10 | autonomous | BLG-GOV-72 fast-path (c): implemented against specs the design gate locked, with Playwright assertions listed in each decision record §5 |
| ST-11, ST-13 | delegated_decision | Strategy Rules & System Intent Owner rulings |
| ST-12 | autonomous | Locked spec (`positions.md` v2.11), ruling-conditional copy pre-designed (fast-path c) |
| ST-14 | delegated_decision | AC 6 requires Strategy Rules & System Intent Owner sign-off that Binding Conditions 1-8 still hold. A signed alternative disposition is also possible. |
| ST-15 | delegated_decision | Product Owner and Strategy Rules & System Intent Owner sign-off (AC 3) |
| ST-16 | delegated_decision | AI Compliance & Governance Officer sign-off (AC 4). A live audit-log read may also be needed (RISK-04). |
| ST-17, ST-19, ST-21 | autonomous | Review, test coverage and documentation with no mid-task human decision |
| ST-18 | delegated_backend | Needs live Render/GitHub Actions control to create and restore a real stale-staging divergence (RISK-04, `ESC-EXEC-20260921-02` precedent) |
| ST-20 | delegated_decision | Strategy Rules & System Intent Owner acknowledgement and caption decision (AC 1). Also the `claude/roadmap/*` write under the RISK-03 ruling (BLG-GOV-362 proposal 2 applied as practice). |

**Blocked-decision design artefact check (LL-v2.2-SP-01):** ST-01 and ST-14 have design gate decision records covering every ruling outcome. ST-05, ST-11, ST-13, ST-15, ST-16 and ST-20 have no dedicated HoST design session artefact. Each is scoped by its own AC to resolve the ruling as its first sub-step. Advisory only, not a blocker.

**Test scenario gap (LL-v2.0-P4-2):** this sprint has no `delegated_frontend` items, so the rule does not apply.

## Director of Quality Readiness Check (STEP 4.3)

Every story's AC in `stage4_backlog_slice.md` meets the §7 standard: observable technical outcomes, named test scenarios or Playwright assertions, and verification by recorded evidence or sign-off. Security is N/A for every story except ST-16 (audit-logging completeness) and ST-17 (CVE review), where it is the subject of the AC. The Director of Quality confirms the criteria are sufficient for each EPIC's `qa_evidence_EPIC-xx.md`. This confirmation is agent-mediated, consistent with prior cycles. One gap is recorded as a non-blocking outstanding action: the ST-01 Settings Playwright assertion (RISK-05). There are no `[AC REQUIRED]` placeholders.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`, run via `backend/.venv/bin/pip-audit`: **clean**. No known vulnerabilities across 60 scanned dependencies. A row was appended to `docs/ops/pip_audit_trend_log.md`.

## Hygiene Advisories (STEP -1.7)

- **Prompt change log gap scan:** ran the date-scan method on every versioned `claude/system/*.md`. No gaps. A first pass flagged `OPERATIONAL_GUIDE.md` (v4.223 vs v4.221), but that was the script's same-date tie-break picking an older row. `prompt_change_log.md` line 16 records `v4.222→v4.223` on 2026-10-06. Same-date rows need file-position order as the tie-break, newest first within the prepend block.
- **Recurring endpoint test coverage audit** (`scripts/audit_endpoint_test_coverage.py`): exit 0. 93 routes across 27 router files, 8 documented `KNOWN_GAPS`, 0 undocumented gaps. "pre-sprint endpoint coverage audit: clean."

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Record `ESC-CLOSE-20261006-01`'s disposition as Resolved (named-file ruling, 2026-10-06) in `closure_escalations.md` and in `.claude_current_state.json` `open_escalations`. Both are outside Sprint Planning's write scope. | Head of Specs Team | No — ruling is recorded here and SLA is due 2026-10-09 |
| Ship `BLG-GOV-362`'s prompt patches (`execution_prompt.md` §7 named-file exception; `sprint_planning_prompt.md` pre-seal classification check) with the CLAUDE.md §6 checklist | Head of Specs Team | No |
| Raise the RISK-01 production `settings` read Human-Delegation at sprint start | Infrastructure & Operations Owner | No — phased at execution |
| Rulings for ST-01, ST-05, ST-11 and ST-13, raised at sprint start | Strategy Rules & System Intent Owner | No — phased at execution |
| Raise the RISK-04 live-fire Human-Delegation for ST-18 (and ST-16 if needed) | Infrastructure & Operations Owner | No — phased at execution |
| Add Playwright coverage for ST-01's Settings fallback values, or file a backlog item before EPIC-01's PR opens | QA & Testing Owner | No — phased at execution |
| ST-14 must also update the prior-cycle `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md` §5, which its own AC 3 names (design gate obligation) | Head of Engineering | No |

No outstanding action is marked `Blocker? Yes`. There are no `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders.
