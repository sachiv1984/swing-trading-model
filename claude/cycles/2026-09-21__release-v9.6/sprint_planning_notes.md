**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-21
**Cycle:** 2026-09-21__release-v9.6

# Sprint Planning Notes — 2026-09-21__release-v9.6

## Backlog Slice Source

Original — `claude/cycles/2026-09-21__release-v9.6/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (`amended_backlog_slice_path` is empty in both `.claude_current_state.json` and `state.json` — no amendment cycle sealed). The addendum is the design gate's post-gate-correction record (7 corrections: ST-01–ST-06, ST-08); it is additive, changes no scope, priority or effort, and is cited from the affected stories in `sprint_backlog.md`.

## Preflight Findings

Two literal-text mismatches in STEP -1 Hard Gates 1–2, both already known and resolved the same way at `2026-09-15__release-v9.5`:

- **Gate 1 (root status):** literal list is `Published`/`Validated`/`Committed`; actual value is `Design_Gate_Passed`. Applied the Lifecycle Guard (`shared_standards.md §10.1`), which names `Design_Gate_Passed` as a valid `plan sprint` from-state.
- **Gate 2 (cycle status):** literal value is `Published`; actual cycle `state.json.status` is `Validated` with `publish_eligible: true`, `open_escalations: []`, `deferred_execution_blockers: []` — the same pattern as v9.4 and v9.5, and consistent with `release_planning_prompt.md`'s own vocabulary. Treated as satisfied.

Reconciliation is already filed as `BLG-GOV-333` (P3) — no new backlog item recommended. Design gate (Gate 3): `design_gate_required: true`, `design_gate_status: Passed` (`design_gate.md`, 32/32 cleared, 0 blocked) — bypass audit skipped (entered from `Design_Gate_Passed`). Gate 4: ≥1 EPIC with ≥1 ST item; all §5 inputs present (schema v2 — the Execution Plan and Capacity Check live in `release_plan.md`, so `stage3_execution_plan.md`/`stage4_5_capacity_check.md` are not separate files); all 5 authority role files and `lessons_learnt_prompt.md` present; write test passed; branch is `main`.

## Carry-Forward Items

Reviewed `claude/cycles/2026-09-15__release-v9.5/lessons_learnt_closure.md ## Carry-Forward` (most recently completed cycle, `post_ship_complete = true`): 2 items. Item 1 (`BLG-GOV-335`/`BLG-GOV-337` open decision-required items — now resolved, both marked complete at the `2026-09-19` follow-up and excluded from v9.6 scope as not-open work) and item 2 (governance-drift skill sibling-field check, `BLG-GOV-336` — also complete) are scoped to `Post-Ship Closure`, not `Sprint Planning` or `All`. No action required this run.

## Pre-Sprint Backlog Advisory

Scanned `claude/backlog/backlog.md` for `Provisional-Target: Before v9.6 sprint planning` — 0 matches. No unconverted items to surface. (Separate from this advisory: 12 items tagged `Provisional-Target: v9.6` were not seated at Release Planning — see Deferred Items.)

## Deferred Items

All 32 items in the authoritative backlog slice enter this sprint (`include`) — no item is deferred out of the sealed slice at Sprint Planning, so no `deferred_at_planning` entries are needed in `execution_state.json`. Items excluded from v9.6 scope entirely were dispositioned at Release Planning (not re-litigated here, per §1 — this routine does not alter the release plan):

| Item | Reason | Next Sprint Candidate? |
|------|--------|-------------------------|
| `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76` | Substantively gate-blocked by their own body text (`BLG-FEAT-74`'s route is ST-23's §13 determination) | Yes, once gate fields are normalised / ST-23 lands |
| `BLG-FEAT-59`/`60`/`63`, `BLG-FE-84`, `BLG-GOV-140`/`141`/`142`, `BLG-OPS-88` | Within-sprint date gate 2026-09-24 (AI review), classified conditional at Release Planning §1.4b | Yes — re-eligible at v9.7 |
| 12 `Provisional-Target: v9.6` items: `BLG-SPEC-149`–`155`, `BLG-FE-178`/`179`, `BLG-QA-179`/`180`/`181` (4.80 days) | Capacity — strict §1.4c selection seated 4 of 16 tagged items; no Product Owner override given | Yes — first call on v9.7. A scope change now would require `amend cycle` (emergency-only) |
| 121 further formally gated items; 44 further ready items (~33.75 days) | No gate clearance / capacity | Gate-dependent / yes |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 (`BLG-FE-180`) | ST-01 (`BLG-FEAT-96`) | Shared-file (`TradePlans.js`) | Sequence sequentially, not in parallel |
| ST-05 (`BLG-FE-181`) | ST-01, ST-02, ST-03 | Shared-file (empty-state call sites across pages incl. Trade Plans, Screener, Watchlist) | Rebase onto them; re-run the `emptyHeading` grep at build time |
| ST-06 (`BLG-FE-182`) | ST-01, ST-02, ST-04 | Shared-file (`TradePlans.js`, Trade History) + spec (convention in `design_system.md` v1.21, locked) | Last in EPIC-01 |
| ST-08 (`BLG-FR-05`) | ST-07 (`BLG-FR-04`) | Internal (semantic) | Net/gross basis must be documented before month-end snapshots freeze figures computed on it |
| ST-13 (`BLG-BE-122`) | ST-09 (`BLG-BE-119`) | Shared call path (nightly stop-update) | Land after ST-09 |
| ST-12 (`BLG-BE-121`) | ST-09 | Shared-file (advisory) | Only if the money-arithmetic audit touches `calculate_trailing_stop` / `position_service.py` |
| ST-30 (`BLG-GOV-325`) | ST-27 (`BLG-GOV-345`) | Shared-file (governed-prompt and `OPERATIONAL_GUIDE.md` version bumps) | RISK-07 — sequence ST-27 first; separate commit per bump; §8 step 2a collision check applied per file |
| ST-10 / ST-04 / ST-07 / ST-08 | each other | Cross-EPIC shared files (`openapi.yaml`, `api_changelog.md`, `docs/specs/api_contracts/*`) | EPIC-01 owns; EPIC-02 then EPIC-03 rebase |
| ST-22 (`BLG-SPEC-148`) | ST-08 | Cross-EPIC shared file (`data_model.md`) | EPIC-02 lands first; different sections, but rebase |
| ST-27 / ST-23 | each other | Cross-EPIC shared file (`claude/backlog/backlog.md`) and a write-scope question | See Outstanding Actions |
| ST-17 / ST-20 / ST-14 / ST-16 | each other | Cross-EPIC shared files (`.github/workflows/*`) | EPIC-04 lands first; EPIC-05 rebases |
| ST-01–ST-08 | Frontend specs locked at the design gate (`trade_plan.md` v1.15, `screener_results.md` v1.7, `watchlist.md` v0.8, `notifications.md` v0.9, `design_system.md` v1.21, `reports.md` v0.18) | Spec | Resolved — locked 2026-09-21 |

No circular dependencies identified.

## Execution Sequence

Per `release_plan.md ## Execution Plan`. Chosen execution order (also the merge order — see `sprint_backlog.md`):

1. **EPIC-01** — Product Features & Frontend Build-and-Ship (`execution_state.json` owner). Internal order ST-01 → ST-02 → ST-03 → ST-04 → ST-05 → ST-06 (ST-06 last so it rebases onto everything that touches those tables)
2. **EPIC-02** — Financial Reporting & Records Integrity (ST-07 → ST-08)
3. **EPIC-03** — Backend & Platform Engineering Debt (ST-09 first; ST-13 after it)
4. **EPIC-04** — Operations & Security Debt (independent)
5. **EPIC-05** — QA & Test Coverage Debt (independent; workflows rebase onto EPIC-04)
6. **EPIC-06** — Spec & Documentation Debt (ST-22 needs live-DB access)
7. **EPIC-07** — Governance Process Debt (ST-27 before ST-30; last because it bumps governed prompts and rebases onto everything)

**Delegation timing recommendation.** The seven delegated stories (ST-09, ST-16, ST-18, ST-22, ST-23, ST-28, ST-29) depend on people or access the engine cannot self-serve, and several sit late in the merge order. Raise all of those requests at sprint open, in parallel with EPIC-01 work, so a slow owner turnaround does not land on the critical path at the tail. Merge order is unaffected.

### Multi-EPIC Execution Notes

**`execution_state.json` ownership:** EPIC-01 (first in execution order) owns `execution_state.json`. EPIC-02 through EPIC-07 must check for its existence before creating their own version — if found, read it and append their own EPIC section rather than overwrite.

**Shared file ownership advisory:** canonical owner listed first; later EPICs rebase onto `main` after earlier EPICs merge, before finalising their edits to that file.

| Shared file | Canonical owner → later EPICs | Note |
|-------------|-------------------------------|------|
| `docs/reference/openapi.yaml`, `docs/reference/api_changelog.md`, `docs/specs/api_contracts/*` | EPIC-01 (ST-04) → EPIC-02 (ST-07, ST-08) → EPIC-03 (ST-10) | Any new `## METHOD /path` heading must be `##`-level and in `openapi.yaml` in the same commit (CLAUDE.md §2) |
| `backend/routers/test.py`, `src/pages/SystemStatus.js` fallback count, `SC-SS-01b` | EPIC-01 → EPIC-02 | Only if a new route is added (likely ST-04 and/or ST-08); update all three in the same commit |
| `data_model.md` | EPIC-02 (ST-08 migration entry) → EPIC-06 (ST-22 DS-17 disclosure) | Keep migration blocks in ascending order |
| `design_system.md` | EPIC-01 (v1.21 from the design gate) → EPIC-06 (ST-24 palette) | ST-24 adds its own version bump |
| `.github/workflows/*` | EPIC-04 (ST-14, ST-16, ST-17) → EPIC-05 (ST-20) | |
| `claude/backlog/backlog.md` | EPIC-06 (ST-23) → EPIC-07 (ST-27) | Existing-item edits are not permitted by `execution_prompt.md` §7 — see Outstanding Actions |
| `OPERATIONAL_GUIDE.md`, `prompt_change_log.md` | EPIC-07 only (ST-27, ST-30) | No other EPIC should bump governed prompts this cycle; if one must, run the CLAUDE.md §8 step 2a check per file first |
| `claude/roadmap/workforce_capacity.md` | EPIC-07 (ST-29) only | Named in ST-29's Notes per the `execution_prompt.md` §7 exception |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|------------------|--------------------|
| RISK-01 | EPIC-01 | Valid — sequence per the table above; one Playwright spec per observable AC. Its "design gate not yet run" clause is **resolved**: the gate passed 2026-09-21 (32/32 cleared). Follow-up call sites for ST-06 are listed as follow-ups, not scope |
| RISK-02 | EPIC-02 (ST-08) | Valid — ST-07 first; if ST-08 overruns, deliver persistence with a disclosed partial and file the remainder; file any discovered gross/net discrepancy as its own item. The design gate narrowed ST-08 to a per-month store (addendum), which lowers but does not remove the sizing risk |
| RISK-03 | EPIC-03 (ST-09, ST-13) | Valid — decision-first; no change to `calculate_trailing_stop` without the Strategy Rules & System Intent Owner's explicit sign-off. Not a sprint-planning-seal blocker (resolved in-sprint by the story). Delegation class `delegated_decision` |
| RISK-04 | EPIC-04 (ST-14, ST-16) | Valid — disclose unclosable ACs rather than fabricate; test the dead-man's-switch against a simulated marker. Re-confirmed this session: `gh` is authenticated here but the Actions-write scope is unverified |
| RISK-05 | EPIC-05 (ST-18) | Valid — AC-02 tagged `[staging-only evidence]` in `sprint_backlog.md`; pre-file the deferral item before any PR opens if staging sign-off is post-merge |
| RISK-06 | EPIC-06 (ST-22) | Valid — re-run the duplicate pre-check immediately before applying; disclose "confirmed-applied" as not closeable if write access is unavailable |
| RISK-07 | EPIC-07 (ST-27, ST-29, ST-30) | Valid, both mitigations applied — ST-27 sequenced before ST-30; `workforce_capacity.md` **is named in ST-29's Notes** in the sealed `sprint_backlog.md`, satisfying the write-scope exception |
| RISK-08 | Release-level | Valid — scope is exactly 100.0% of ceiling; buffer-floor acknowledgement recorded in `sprint_capacity.md §1.5`; return items in reverse selection order (last-selected first) if slippage occurs |

**Multi-vehicle fix-choice check (LP-14):** RISK-03 names two genuinely alternative vehicles for ST-09 — (a) ratify the floor, add it to `strategy_rules.md` §7.2 and bring `position_manager.py`'s backtest formula into line (this changes backtest results for profitable positions), or (b) remove the floor from live `calculate_trailing_stop` — with the choice deferred to the owner's decision at execution. The story is sized as one band (S ~0.5–1d) although its own text says code scope "depends on which side is chosen", and vehicle (a) plausibly costs more (spec edit through the owner's change route plus backtest regression baselines). No `### Phasing Recommendation` exists this cycle (capacity `pass`), so there is nothing to cross-reference; the consequence is that any overrun has no buffer to land in and falls under RISK-08's return rule. Recorded so the sizing uncertainty is visible at planning, not discovered at execution.

No risk has materialised since Release Planning. Findings new to this session (not in the release-planning register): (1) ST-23 and ST-27 have ACs that require editing existing `backlog.md` items, outside the engine's write scope — see Outstanding Actions; (2) ST-29's hold/raise call must be the Product Owner's, since `execution_prompt.md` §7 says `workforce_capacity.md` may be documented into "never used to decide"; (3) ST-05/ST-06 share call sites with ST-01–ST-04, which the release plan only stated for `TradePlans.js`.

## Delegation Classification

25 `autonomous`, 6 `delegated_decision`, 1 `delegated_qa`. Following the v9.5 precedent (live-access and owner-decision items were `delegated_decision`):

- **EPIC-01 (ST-01–ST-06) — `autonomous`.** All six are implemented against locked frontend specs cleared at the design gate (BLG-GOV-72 fast-path (c)), and existing Playwright specs cover the affected pages (`trade-plan.spec.js`, `screener.spec.js`, `watchlist.spec.js`, `notifications.spec.js`, `positions-pnl-columns.spec.js`, `net-r-trade-history.spec.js`, `trade-history-ai-journal-summary.spec.js`), so feasibility is plausible; Director of Quality confirms per-AC coverage (Outstanding Actions). No override of the default-autonomous classification was needed, so no justification entry is required. No `delegated_frontend` item exists, so the LL-v2.0-P4-2 test-scenario-gap rule does not fire.
- **`delegated_decision` — ST-09** (Strategy Rules & System Intent Owner ratifies the live-capital formula), **ST-16** (Actions-write token + real Telegram receipt), **ST-22** (live-DB write access), **ST-23** (§13 determination is the Strategy Rules & System Intent Owner's), **ST-28** (same owner's cadence decision), **ST-29** (Product Owner's capacity-band decision).
- **`delegated_qa` — ST-18** (live staging environment and fresh seed; Director of Quality).
- **LL-v2.2-SP-01 blocked-decision design artefact check:** for each `delegated_decision` item — ST-09 has the decision framing in `BLG-BE-119` and the design gate's §13 note; ST-23/ST-28 are themselves the review/decision artefacts; ST-29's framing is in `BLG-GOV-328`'s Scope (FinOps utilisation review → PO decision); ST-16/ST-22 are access hand-offs, not design decisions. No HoST design session is missing.

## Staging-Only AC Review (seal gate)

Every AC in `stage4_backlog_slice.md` was reviewed for `[staging-only evidence]` tags and for live external-system dependence. Listed in each story's `**Staging-only ACs:**` field: **ST-16** (AC-01, AC-02), **ST-17** (AC-01), **ST-18** (AC-02), **ST-22** (AC-01, AC-02). All other stories carry `None`. No AC in the slice carries a literal `[staging-only evidence]` tag — these were identified by content, as the seal gate requires. Per CLAUDE.md §2, if staging sign-off for any of these is deferred to post-merge, a backlog item must be filed before the PR opens.

Not listed, deliberately: ST-14's ACs (explicitly a *simulated* missed run), ST-13 (mocked upstream calls), and ST-01–ST-08 (Playwright-verifiable in CI; no live external dependence). ST-04's time-based AC is verifiable with an injected clock.

## Pre-Sprint Vulnerability Scan

`backend/.venv/bin/pip-audit -r backend/requirements.txt --format=json` — **clean**. 58 dependencies scanned, 0 known vulnerabilities, 0 fixes required. The bare `pip-audit` command is not on the system `PATH` here, so it was run from the project virtualenv (CLAUDE.md §9 pattern) — this is not an "unavailable" reading. Trend row appended to `docs/ops/pip_audit_trend_log.md` in this session.

## Recurring Endpoint Test Coverage Audit

`python3 scripts/audit_endpoint_test_coverage.py` — **clean**. 92 route decorators scanned across 26 router files; 8 documented `KNOWN_GAPS` exclusions; 0 undocumented gaps. (Baseline for this sprint: v9.5 read 91 — one route was added since. Any route added in v9.6 must register in `backend/routers/test.py`.)

## Prompt Change Log Gap Check

Applied the date-scan method (`shared_standards.md §11.1`) across all 13 Class 6 prompt files (12 `*_prompt.md` plus `post_ship_closure.md`): for each, collected every row whose Prompt column is that file, selected the latest-dated row, and compared its target version with the file's current `**Version:**`. All 13 match — 0 gaps. (Method note for future runs: the Prompt column holds the full path `claude/system/<file>`, and rows for `OPERATIONAL_GUIDE.md` mention prompt filenames in their Change text, so matching on the Prompt column rather than free text is required.)

## Pre-Seal Stale-Feature-Target Check

For all 32 candidates the source `BLG-*` item still has an open heading in `claude/backlog/backlog.md` and none has a completion entry in `claude/backlog/backlog_archive.md` (the five `BLG-GOV-90` archive hits are cross-references from other items, not a completion). Code check for the three new product features: no clone action in `src/pages/TradePlans.js`, no CSV export in the Screener/Watchlist pages, and no reflection-reminder code in `backend/` or `src/`. No item is `flag`ged for already-shipped work.

## Acceptance Criteria Confirmation

All 32 items carry acceptance criteria in the sealed slice (0 `[AC REQUIRED]`); design-gate corrections for ST-01–ST-06 and ST-08 are in the addendum. Structure against §7's four fields: Technical and Verification are present in every story; Quality and Security are carried at story level by the DoQ/QA-evidence process and the CLAUDE.md §2 obligations listed in each story's Notes (Playwright coverage, contract/`openapi.yaml`/`test.py` registration, §6 governance checklist). Security surface: no new AI-calling endpoint (design gate: `ai_endpoint_security_checklist.md` not triggered); ST-03's formula-injection guard is the one security-relevant behaviour and is in the addendum. Director of Quality readiness (STEP 4.3): agent-mediated confirmation that the QA criteria are sufficient for `qa_evidence_EPIC-xx.md`, subject to the Playwright-coverage action below.

## Capacity WARN Acknowledgement

Not applicable — capacity check outcome is `pass`, no WARN, no Phasing Recommendation. The separate buffer-floor acknowledgement is in `sprint_capacity.md §1.5`; `capacity_warn_acknowledged` stays `false`.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Buffer-floor-exceeded acknowledgement (100.0% of ceiling) — recorded, agent-mediated | Product Owner | No (done) |
| **Write-scope conflict, ST-23 AC-02 and ST-27 clear/re-gate legs:** both ACs edit existing `claude/backlog/backlog.md` items (`BLG-FEAT-74`'s gate line; the six lapsed-date items), but `execution_prompt.md` §7 permits only new-item additions to `backlog.md`, not edits to existing items. There is no precedent for handling this. **Recommended:** a Head of Specs Team + Product Owner ruling before execution reaches those stories, either a plan-authorised exception as `BLG-GOV-337` did for `workforce_capacity.md`, or acceptance of the fallback — the story records the determination / verification in a dated document, hands over the exact replacement gate-line text, and discloses the AC as partial rather than editing the item. Until ruled, the fallback applies | Head of Specs Team + Product Owner | No |
| ST-09: schedule the live trailing-stop formula decision at sprint open; without explicit sign-off ship only the golden-output case + recorded decision and disclose | Strategy Rules & System Intent Owner | No |
| ST-16 / ST-22 / ST-18: raise the Actions-write token, live-DB write access and live-staging requests at sprint open; disclose rather than fabricate if unavailable; file the deferral backlog item before the PR opens if staging sign-off is post-merge | Infrastructure & Operations Owner / Director of Quality | No |
| ST-28 and ST-29: decisions are the owners' — engine may draft options, not choose (ST-29's hold/raise is the Product Owner's) | Strategy Rules & System Intent Owner / Product Owner | No |
| Confirm Playwright coverage for every observable AC of ST-01–ST-08 (including ST-04's 48h reminder and ST-08's restatement-diff AC); file a backlog item before any PR opens if an AC is deferred to staging | Director of Quality | No |
| ST-04, ST-07, ST-08, ST-10 change API responses/contracts — contract, `openapi.yaml`, and (for any new route) `test.py` + `SystemStatus.js` count + `SC-SS-01b` in the same commit | Backend Engineering Patterns Owner / API Contracts & Documentation Owner | No |
| Decide whether any of the 12 unseated `Provisional-Target: v9.6` items should displace scope (only via `amend cycle`, emergency-only) or simply lead v9.7 planning | Product Owner | No |

No outstanding action is marked `Blocker? Yes`. No `sprint_escalations.md` was created — nothing raised requires halting planning.
