# Sprint Planning Notes — 2026-11-06__release-v9.16

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-09
**Cycle:** 2026-11-06__release-v9.16

## Backlog Slice Source

Original: `claude/cycles/2026-11-06__release-v9.16/stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design gate corrections to ST-03, ST-04, ST-05, ST-07 and ST-12; no scope change). No amendment (`amended_backlog_slice_path` empty).

## Preflight Record

- Lifecycle guard: `Design_Gate_Passed` → valid entry state. No `Amendment_In_Progress`.
- Release plan `state.json`: `status = Published`, `publish_eligible = true`, `open_escalations` empty, `deferred_execution_blockers` empty.
- Design gate: `design_gate_required = true`, `design_gate_status = Passed` ✅ (2026-11-06T17:43:15Z). Entered from `Design_Gate_Passed`, so the bypass audit is skipped.
- Files and roles: slice holds 7 EPICs / 30 ST items. Schema v2 cycle: capacity check and execution plan live in `release_plan.md`, so `stage4_5_capacity_check.md`/`stage3_execution_plan.md` are not expected. All five §4 role charters present; `lessons_learnt_prompt.md` present; write test passed and cleaned up.
- Branch: `main`.
- Open root escalations: `ESC-EXEC-20260910-01` (Deferred, `blocks_execution: false`) — not a blocker for this sprint.

## Pre-Sprint Required Decisions

| Decision | Owner | Outcome |
|----------|-------|---------|
| RISK-02: ST-05 AC 4 case (c) `strategy_rules.md` §4.2.1 Known deviation closure | Strategy Rules & System Intent Owner | **Resolved 2026-11-09: confirmed for in-sprint write** (the user, in session). Recorded in `sprint_backlog.md` sign-off. |

## Carry-Forward Items

Carry-forward items reviewed: 4 items from cycle `2026-11-03__release-v9.15` (`lessons_learnt_closure.md ## Carry-Forward`).
1. `BLG-OPS-214`/`BLG-OPS-213` — seated as ST-11/ST-12 and lead the sprint (delegations raised first).
2. Post-merge remainders — `BLG-OPS-197` seated (ST-13), `BLG-AI-27` seated (ST-19); `BLG-OPS-211`, `BLG-GOV-408`, `BLG-OPS-201`, `BLG-GOV-399` remain outside scope as recorded at Release Planning.
3. Roadmap inputs — a `run roadmap` action, not a sprint item.
4. Programme-phase hold — applied at Release Planning (§1.4c step 0).

## Pre-Sprint Vulnerability Scan

pre-sprint pip-audit: clean. `pip-audit` 2.10.1 run via the project virtualenv (`backend/.venv/bin/python3 -m pip_audit -r backend/requirements.txt --format=json`; the system `pip-audit` binary is not installed): 53 dependencies scanned, 0 known vulnerabilities. Trend log row appended to `docs/ops/pip_audit_trend_log.md`.

## Pre-Sprint Endpoint Coverage Audit

pre-sprint endpoint coverage audit: clean. `scripts/audit_endpoint_test_coverage.py` exit 0 — 94 route decorators across 27 router files; 8 documented `KNOWN_GAPS`; no undocumented gaps.

## Hygiene Advisories

- **Prompt change log gaps:** none. Every Class 6 prompt's current `**Version:**` has a matching latest-dated row in `prompt_change_log.md` (date-scan method, `shared_standards.md` §11.1).
- **Pre-Sprint Backlog Advisory:** no `Provisional-Target: Before v9.16 sprint planning` items found in `backlog.md`.

## Scope Review (STEP 3.1)

All 30 items classified `include`. None `defer` or `flag`.

**Stale-feature-target check:** none of the 30 targets has already shipped. Spot checks: `settings.md:121` still names `src/lib/strategyParameters.js` (ST-23); `scripts/staging_smoke_test.py` still treats a missing `render_service_id` as a known limit (ST-15); `TradePlan.js:122` still reads `REACT_APP_ANTHROPIC_API_KEY` and `deploy.yml:33` still injects it (ST-12); `strategy_rules.md` §4.2.1 still carries the v1.26 Known deviation (ST-05).

**Cleared-gate evidence (restated ACs ST-24 to ST-27, ST-29):** `current_roadmap.md` records PT-04 ✅ Shipped v6.1 (2026-06-23) and "Arc 2 ✅ Fully Complete (v3.1–v6.1)". Confirmed at seal by the Product Owner (ST-24, ST-26, ST-27; the user, 2026-11-09) and by the QA Lead (ST-24, ST-25, ST-26) and PMO Lead (ST-29), agent-mediated (§5.3).

### Delegation class assignment

| Story | Class | Justification |
|-------|-------|---------------|
| ST-01 to ST-04 | autonomous | BLG-GOV-72 fast-path (c): locked `navigation.md` v2.0 / `analytics.md` v2.3 and the `digest-section-link` design record |
| ST-05 | autonomous | Locked `position_form.md` v1.14, `trade_plan.md` v1.22 §5e, design record. Its case (c) `strategy_rules.md` write is confirmed at seal, so it adds no decision step |
| ST-06 | autonomous | Locked `dashboard.md` v4.0 §1B (TL-01..TL-29) |
| ST-07, ST-08 | autonomous | Locked `signal-to-plan-flow` design record and specs |
| ST-09, ST-10 | autonomous | Locked `semantic-colour-tokens` design record, `design_system.md` v1.25 |
| ST-11 | delegated_backend | Human-Delegation: Anthropic console, Render env (precedent v9.15 ST-29) |
| ST-12 | delegated_backend | Code change autonomous; secret deletion and console revocation are Human-Delegation |
| ST-13, ST-14 | delegated_backend | Human-Delegation: production reads after gate dates (precedent v9.15 ST-33) |
| ST-15 to ST-18 | autonomous | Test and backend fixes with unit-test ACs |
| ST-19 | delegated_backend | Human-Delegation: production Render log token list (precedent v9.15 ST-24) |
| ST-20 | delegated_decision | AI Compliance & Governance Officer collision ruling before code |
| ST-21 to ST-23 | autonomous | Spec/contract text; each AC accepts either named option |
| ST-24 to ST-27 | autonomous | QA protocol, DoQ review, Playwright test, journey map; no human decision mid-task |
| ST-28, ST-29 | autonomous | Governance text under the CLAUDE.md §6 checklist |
| ST-30 | delegated_decision | Base44 Frontend Prompt Owner chooses the convention first |

No override of the BLG-GOV-72 default-autonomous classification. No `delegated_frontend` item, so no LL-v2.0-P4-2 `test_scenarios` placeholder applies.

**LL-v2.2-SP-01 (delegated_decision design artefacts):** ST-20 and ST-30 have no HoST design session artefact. Advisory: neither changes UI; each ruling is a single first sub-step (ST-20 against `ESC-EXEC-20261027-02` (B); ST-30 against the item's Proposed solution). No session scheduled.

### Named-file writes (STEP 3.1)

- Named-file write: `claude/strategy/strategy_rules.md` §4.2.1 Known deviation (v1.26) marked resolved as a documentation-only version, with its Change Log row and `backend/strategy_version_registry.py` `DOCUMENTATION_ONLY_VERSIONS` entry (ST-05 AC 4) — authorised under execution_prompt.md §7 named-file rule, case (c). Strategy Rules & System Intent Owner confirmation recorded in the sign-off.

No `claude/roadmap/*` write and no write to an existing `backlog.md` item is planned. ST-27 files new items via `/backlog-add` (new items are not named-file edits).

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | None. All 30 slice items are in scope. | — |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02, ST-03 | ST-01 | Internal (v2 areas in `Layout.js`) | Open |
| ST-07 navigation rows | ST-03 (`navigation.md` §Onward Links) | Cross-EPIC (spec rows) | Open — ST-07 rebases on EPIC-01 |
| ST-08 | ST-07 | Internal (`TradePlan.js` entry path) | Open |
| ST-09 baselines | EPIC-01, EPIC-02 on `main` | Cross-EPIC (RISK-03) | Open |
| ST-10 | ST-09 (if adopting text token) | Internal | Open |
| ST-11 key revocation | — | External (Anthropic console) | Open — safe in-sprint: the Pages build only tests the secret's presence (`BLG-OPS-213` Problem) |
| ST-12 AC 2 secret deletion, AC 4 production check | ST-12 merged and Pages redeployed | Post-merge | Tracked by `BLG-OPS-215` |
| ST-13 | 2026-11-09 gate (7 days of production data) | External date | Conditional |
| ST-14 | ≥10 nightly production runs (~2026-11-12) | External date | Conditional |
| ST-17 | ST-16 (`native_entry_price()` fallback) | Internal | Open |
| ST-20 | ST-19 (tokens), AI Compliance ruling | Internal + decision | Open |
| ST-24 | ST-26 (reuses lifecycle test) | Internal | Open |
| ST-26, ST-27 | EPIC-02 ST-07, ST-08 merged | Cross-EPIC (RISK-06) | Open |
| ST-28 AC 2 | Next `groom backlog` after merge | Post-merge | Tracked by `BLG-GOV-414` |
| ST-30 | Base44 Frontend Prompt Owner decision | Decision | Open |

No circular dependency.

## Execution Sequence

**At sprint start (before any code):** raise the Human-Delegations and rulings in this order: ST-11 (P1, console + Render) with ST-12's console revocation; ST-19 (production log tokens); ST-20 ruling; ST-30 decision; ST-13 (production read, gate today); ST-14 (from ~2026-11-12).

Then, in EPIC order (= merge order):
1. **EPIC-01** — ST-01 → ST-02, ST-03; ST-04 independent.
2. **EPIC-02** — ST-05 first; ST-06; ST-07 → ST-08.
3. **EPIC-05** — ST-16 → ST-17; ST-18; ST-19 → ST-20; ST-21, ST-22, ST-23.
4. **EPIC-07** — ST-28 first; ST-29; ST-30 after its decision.
5. **EPIC-06** — ST-26 (after EPIC-02 merges) → ST-24; ST-25; ST-27 (after ST-07).
6. **EPIC-03** — ST-09 (after EPIC-01, EPIC-02 on `main`) → ST-10.
7. **EPIC-04** — ST-15, ST-12 code, ST-11 docs; ST-13/ST-14 as their gates clear.

## Multi-EPIC Execution Notes

**`execution_state.json` owner:** EPIC-01 (first in execution order). Every other EPIC branch checks whether the file exists before creating its own; if it exists, append its EPIC section and never overwrite.

**Why EPIC-04 merges last:** ST-13 and ST-14 are conditional on dates inside the sprint (2026-11-09, ~2026-11-12). ST-11's P1 work (rotation, revocation) is console and Render work raised at sprint start and is not merge-dependent. **Fallback:** EPIC-04 may merge first if ST-13 and ST-14 have both cleared or been returned by then; this brings `BLG-OPS-215` (secret deletion) forward.

## Shared-File Ownership Advisory

- **`src/pages/TradePlan.js`** (EPIC-02 ST-05 snapshot write, ST-07, ST-08; EPIC-04 ST-12 `HAS_AI`; EPIC-03 ST-10 input classes): EPIC-02 owns. EPIC-03 and EPIC-04 rebase onto `main` after EPIC-02 merges.
- **`src/Layout.js` and nav Playwright specs** (`alert-nav-badge`, `command-palette`, `keyboard-shortcuts`): within EPIC-01.
- **`docs/specs/frontend/pages/navigation.md` §Onward Links** (EPIC-01 ST-03; EPIC-02 ST-07 adds Signals/Screener → Trade Plan rows): EPIC-01 owns; ST-07 rebases and takes the next version (CLAUDE.md §8 step 2a).
- **`DashboardHome`, `DashboardCard`, `DataTable`, `PageHeader`, visual baselines** (EPIC-02 ST-06; EPIC-03 ST-09): EPIC-02 owns the components; EPIC-03 regenerates both themes' baselines last.
- **`src/` input class strings** (EPIC-03 ST-10, 18 sites in 8 files): EPIC-03, rebased on everything else.
- **`claude/strategy/strategy_rules.md`, `backend/strategy_version_registry.py`** (EPIC-02 ST-05 only): EPIC-02.
- **`backend/services/ai_service.py` `_NON_TICKER_WORDS`, `ai_endpoints.md` check 3** (ST-19, ST-20): within EPIC-05.
- **`docs/specs/api_contracts/*`, `openapi.yaml`, `api_changelog.md`** (EPIC-05 ST-18 if documented, ST-21): within EPIC-05. Any new endpoint follows the same-commit openapi and `test.py` rules.
- **`docs/specs/data_model.md`** (EPIC-05 ST-22 dictionary; EPIC-04 ST-13 DS-36 Live Confirmation): EPIC-05 owns; EPIC-04 rebases.
- **`OPERATIONAL_GUIDE.md`, `prompt_change_log.md`, governance prompts** (EPIC-07 ST-28 `post_ship_closure.md`, ST-29 if any, ST-30 `execution_prompt.md`/OG; EPIC-06 ST-25 `shared_standards.md`): EPIC-07 owns. EPIC-06 rebases and renumbers under CLAUDE.md §6 and §8 step 2a, checked per co-bumped file.
- **`claude/backlog/backlog.md`** (ST-27 new items; any `/backlog-add` follow-ups): run `scripts/check_backlog_item_integrity.py` after each §8 merge (step 2c).
- **`docs/ux/`** (ST-04 `si05_user_journey_map.md` F-04; ST-27 new Arc 2 map): separate files, no conflict.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | ST-11, ST-12, ST-13, ST-14, ST-19 | Valid. Delegations raised at sprint start; production/post-merge ACs marked with trackers |
| RISK-02 | ST-05 | **Resolved at seal** — Strategy Rules & System Intent Owner confirmed, 2026-11-09 |
| RISK-03 | EPIC-01, EPIC-02, EPIC-03 | Valid. EPIC-03 merges after EPIC-01/02; ownership above |
| RISK-04 | ST-06 | Valid. TL-09/TL-10 excluded; no-placeholder AC tested |
| RISK-05 | ST-13, ST-14 | Valid. ST-13's gate date is today; promote on dated confirmation in execution |
| RISK-06 | EPIC-06 | Valid. ST-26/ST-27 after EPIC-02; gate evidence confirmed at seal |
| RISK-07 | ST-20, ST-25, ST-28, ST-29, ST-30 | Valid. Rulings first sub-steps; §6 checklist; per-file §8 2a check |

**Multi-vehicle fix-choice check:** ST-17 (all-UNKNOWN vs all-live-rate), ST-18 (write marker vs document exclusion), ST-21 (remove line vs cost by model) and ST-22 (`exit_note` row) each name alternatives, all XS with equal effort either way. No Phasing Recommendation exists (capacity `pass`). No capacity risk.

## Capacity Buffer Floor

27.95 / 28.00 = 99.8% > 95% floor. Product Owner acknowledged and chose to proceed with full scope, 2026-11-09.

## Pre-Seal Backlog Filings

Authorised by the Product Owner, 2026-11-09, filed via `/backlog-add`:
- `BLG-OPS-215` — post-merge tracker for ST-12 AC 2 and AC 4 (production).
- `BLG-GOV-414` — post-merge tracker for ST-28 AC 2 (next `groom backlog`).
- `BLG-SPEC-224`, `BLG-SPEC-225` — design gate observations (`trade_plan.md` §5.1/§5d.4 fields; §2 routes).

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| RISK-02 confirmation of ST-05 AC 4 | Strategy Rules & System Intent Owner | Yes — **Resolved 2026-11-09** |
| Raise delegations at sprint start: ST-11, ST-12 (console), ST-13, ST-14, ST-19; rulings ST-20, ST-30 | Cybersecurity & Trust Lead; Infrastructure & Operations Owner; FinOps & Resource Architect; AI Compliance & Governance Officer; Base44 Frontend Prompt Owner | No |
| For any other staging-only AC deferred past merge, file a backlog item before the PR opens (CLAUDE.md §2) | QA & Testing Owner | No |
| Delete `REACT_APP_ANTHROPIC_API_KEY` secret only after ST-12 is on `main` and Pages redeployed (`BLG-OPS-215`) | Cybersecurity & Trust Lead | No |
