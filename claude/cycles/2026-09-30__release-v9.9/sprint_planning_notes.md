**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-01
**Cycle:** 2026-09-30__release-v9.9

# Sprint Planning Notes — 2026-09-30__release-v9.9

## Backlog Slice Source

Original — `claude/cycles/2026-09-30__release-v9.9/stage4_backlog_slice.md`. `amended_backlog_slice_path` is absent/empty in `.claude_current_state.json` — no amendment has sealed for this cycle.

## Carry-Forward Items

Carry-forward items reviewed: 3 items from cycle `2026-09-28__release-v9.8` (`lessons_learnt_closure.md ## Carry-Forward`):

| # | Observation | Applicable to this routine? |
|---|-------------|------------------------------|
| 1 | Four open decision-required/recurrence escalations outstanding at v9.8 closure; `ESC-CLOSE-20260928-02`'s SLA (`2026-10-01T00:00:00Z`) is now past (current time `2026-10-01T10:28:58Z`) with no `disposition` recorded. | Not a Sprint Planning gate — `BLOCKED_SLA_BREACH` (IMP-40) is wired only into `execution_prompt.md` §3.1.D, not this engine. Noted here as advisory; will surface again at Phase 3 entry if still unresolved. |
| 2 | Phase 3 Friction Item 2 (`claude/roadmap/*` write-scope near-misses), 1st carry. | Execution-phase concern, not a planning-phase write. No action here. |
| 3 | Phase 4 Friction Item 2 (agent-mediated signer format mandate), 1st carry. | Delivery-verification-phase concern. No action here. |

No item requires action within this engine's write scope.

## Pre-Sprint Backlog Advisory

No `backlog.md` items found with `Provisional-Target: Before v9.9 sprint planning` (STEP -1.7 scan: zero matches).

## Deferred Items

None. All 35 items from the authoritative backlog slice are included in sprint scope (see `sprint_capacity.md` — 27.85 / ~24–28 day band, `pass`, no over-allocation, Product Owner acknowledged proceeding at ceiling).

## Pre-Seal Stale-Feature-Target Check (STEP 3.1)

All 35 `Source:` IDs checked against `claude/backlog/backlog_archive.md`. Two incidental matches (`BLG-QA-190`, `BLG-QA-191`) are references *to* these same not-yet-shipped items inside a `shared_standards.md` §... friction-log entry (the items were filed as follow-ups from a past sprint, not shipped themselves) — confirmed not already-shipped. No item is `flag`ged under this check.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | Strategy Rules & System Intent Owner ruling on RISK-01 (§7.1 cadence wording vs. actual recompute cadence) | External | Open — phased as an internal design-decision sub-step ahead of implementation, per `release_plan.md` Risk Register mitigation |
| ST-04 | ST-01 (both touch `backend/utils/pricing.py`; ST-01's ATR consolidation should land first to avoid rework on ST-04's timeout-sourcing fix) | Internal | Unresolved — sequence ST-01 before ST-04 |
| ST-19 | Possible Human-Delegation for live production AI-feature-usage data (RISK-03) | External | Open — same structural gap as `ESC-EXEC-20260921-02/03/04`, `ESC-EXEC-20260910-01` |
| ST-26 | Head of Specs Team / Roadmap Engine routing-and-authority decision on a new `claude/roadmap/*` file (RISK-02) | External | Open — phased as an internal design-decision sub-step ahead of implementation, per `release_plan.md` Risk Register mitigation |
| ST-25 | ST-21 (both touch `roadmap_prompt.md`; ST-21's core/appendix split should land first so ST-25's script-reference addition targets the restructured file, not the pre-split one) | Internal | Unresolved — sequence ST-21 before ST-25 |
| ST-29, ST-30 | Live-DB write access (Human-Delegation) to apply the column-drop and constraint reconciliation against the live `positions` table | External | Open — same precedent as `ESC-EXEC-20260921-04` (DS-17 migration) |
| ST-29, ST-30, ST-32 | Shared file: `data_model.md` (all three touch its Migration History / DS-19) | Internal | No strict order required — all within EPIC-05, same owner |

No circular dependencies detected.

## Execution Sequence

**Multi-EPIC Execution Notes:** This sprint spans 6 EPICs. Execution order below designates **EPIC-01 as the `execution_state.json` owner** — all other EPIC branches must check for its existence before creating their own and append their section rather than overwrite (per `sprint_planning_prompt.md` §5.2).

Order (front-loads EPICs carrying `delegated_decision` / `delegated_backend` items so their external dependencies are raised as early as possible, letting autonomous work proceed in parallel while awaiting response):

1. **EPIC-01** — Backend Reliability & Data Integrity (ST-01 → ST-04 → ST-02, ST-03, ST-05) — owns `execution_state.json`
2. **EPIC-04** — Governance Process & Strategy Boundary (ST-19, ST-26 raised first; ST-21 → ST-25; ST-20, ST-22, ST-23, ST-24, ST-27 unordered)
3. **EPIC-05** — Spec & Data-Model Debt Clearance (ST-29, ST-30 raised first; ST-28, ST-31, ST-32, ST-33, ST-34 unordered)
4. **EPIC-02** — Operational Reliability & Security Hardening (ST-06, ST-07, ST-08, ST-09 — all autonomous, unordered)
5. **EPIC-03** — QA & Test Coverage (ST-10 through ST-18 — all autonomous, unordered)
6. **EPIC-06** — Frontend & UX Debt (ST-35 — autonomous, design-cleared)

**Shared-file ownership advisory (Required, >1 EPIC in scope):**

| Shared file | Touched by | Canonical-version owner | Note |
|-------------|-----------|--------------------------|------|
| `strategy_rules.md` | EPIC-01 (§7.1, ST-01) and EPIC-04 (§11/§12.3 ledger, ST-22) | EPIC-01 (merges first) | EPIC-04 must rebase onto `main` after EPIC-01 merges before finalising its §11/§12.3 edits |
| `claude/system/prompt_change_log.md` | EPIC-01, EPIC-04 (and possibly EPIC-05 if a Class 6 file is touched) | Append-only — low conflict risk | Each EPIC appends its own rows; no single "owner" needed, but EPICs merging later must re-check for prepend-vs-append ordering conventions (per the date-scan method, not file position) |
| `data_model.md` | EPIC-05 only (ST-29, ST-30, ST-32) | EPIC-05 | No cross-EPIC contention this cycle |
| `openapi.yaml` / `docs/specs/api_contracts/position_endpoints.md` | EPIC-01 only (ST-01) | EPIC-01 | No cross-EPIC contention this cycle |
| `current_roadmap.md`, `ai_endpoints.md` | EPIC-05 only (ST-31, ST-33) | EPIC-05 | No cross-EPIC contention this cycle |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01) | Valid — phased as internal design-decision sub-step ahead of implementation, per release plan |
| RISK-02 | EPIC-04 (ST-26) | Valid — phased as internal design-decision sub-step (routing/authority decision) ahead of implementation |
| RISK-03 | EPIC-04 (ST-19) | Valid — likely Human-Delegation at execution time, consistent with existing precedent; no new materialisation this cycle |

No multi-vehicle fix-choice risks identified this cycle (all three risks are single-path: a decision/authorisation gate, not a choice among alternative fix approaches) — the Multi-vehicle fix-choice risk check (§5.3) does not apply.

## Delegation Classification (set at planning time, per §12 invariant)

| Item | Delegation class | Justification |
|------|-------------------|----------------|
| ST-01 | delegated_decision | RISK-01 spec query to Strategy Rules & System Intent Owner required before the item is complete; internal design-decision sub-step sequenced ahead of implementation (same convention as prior-cycle RISK-01/RISK-02 precedent) |
| ST-02, ST-03, ST-04, ST-05 | autonomous | Backend bug fix / timeout-sourcing refactor, no UX change, no human decision (BLG-GOV-72 default) |
| ST-06 – ST-09 | autonomous | CI guard hardening / de-duplication logic, no UX change |
| ST-10 – ST-18 | autonomous | Backend/test/tooling coverage work, no UX change, no human decision required |
| ST-19 | delegated_decision | May require Human-Delegation for live production AI-usage data (RISK-03) |
| ST-20 | delegated_decision | Governance §13 determination requires Head of Specs Team / Strategy Rules Owner judgement, not mechanical execution |
| ST-21 – ST-25, ST-27 | autonomous | Governance prompt restructuring / tooling / documentation, no human decision gate |
| ST-26 | delegated_decision | RISK-02 routing/authority decision required before any `claude/roadmap/*` file may be created, per `execution_prompt.md` §7 write-scope restriction; internal design-decision sub-step sequenced ahead of implementation |
| ST-28 | autonomous | Read-only tooling |
| ST-29, ST-30 | delegated_backend | Requires live-DB write access (Human-Delegation), same precedent as `ESC-EXEC-20260921-04` |
| ST-31 – ST-34 | autonomous | Documentation-only corrections |
| ST-35 | autonomous | Visual fix against an already-locked, already-published canonical rule (`design_system.md` v1.21) with confirmed Playwright feasibility (`design_gate.md`) — BLG-GOV-72 fast-path (c): implementing against a locked spec with confirmed Playwright feasibility |

**Blocked-decision design artefact check (LL-v2.2-SP-01):** For each `delegated_decision` item (ST-01, ST-19, ST-20, ST-26) — no dedicated HoST design session artefact exists yet; each is explicitly scoped by the release plan's own risk mitigation to resolve its decision at/during execution kickoff rather than before sprint start. Advisory noted, not a blocker — consistent with `release_plan.md`'s own Low-priority, phaseable framing of RISK-01/02/03.

**Test scenario gap (LL-v2.0-P4-2):** No `delegated_frontend` items in this sprint — rule does not apply.

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — no known vulnerabilities found across all 58 scanned dependencies. Row appended to `docs/ops/pip_audit_trend_log.md`.

## Hygiene Advisories (STEP -1.7)

- **Prompt change log gap scan:** Spot-checked `sprint_planning_prompt.md` itself (the governing prompt for this invocation) — current `**Version:** 3.19` matches `prompt_change_log.md`'s latest row for this file (`2026-09-24 | v3.18→v3.19`). No gap. (Full enterprise-wide Class 6 version-table audit most recently run by `manage roadmap` on 2026-09-30, 0 mismatches across 22 tracked files — not re-run here.)
- **Recurring endpoint test coverage audit** (`scripts/audit_endpoint_test_coverage.py`): exit 0 — 93 routes scanned across 27 router files, 8 documented `KNOWN_GAPS` exclusions, 0 undocumented gaps. "pre-sprint endpoint coverage audit: clean."

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Resolve RISK-01 spec query (strategy_rules.md §7.1 cadence wording) | Strategy Rules & System Intent Owner | No — phased at execution |
| Resolve RISK-02 routing/authority decision for new `claude/roadmap/*` file | Head of Specs Team | No — phased at execution |
| RISK-03 Human-Delegation disposition for ST-19 (if confirmed needed) | AI Compliance & Governance Officer / Product Owner | No — phased at execution |
| Live-DB write access delegation for ST-29/ST-30 | Data Model & Domain Schema Owner + Infrastructure & Operations Owner | No — phased at execution |

No outstanding action is marked `Blocker? Yes`. No `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders exist — all 35 items have defined acceptance criteria (`stage4_backlog_slice.md`) and effort estimates (`sprint_capacity.md`).
