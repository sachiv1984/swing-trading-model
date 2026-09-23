**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-23
**Cycle:** 2026-09-23__release-v9.7

# Sprint Planning Notes — 2026-09-23__release-v9.7

## Backlog Slice Source

Original — `claude/cycles/2026-09-23__release-v9.7/stage4_backlog_slice.md`. `.claude_current_state.json.amended_backlog_slice_path` is empty; no amendment has sealed for this cycle.

## Preflight Summary (STEP -1)

- **Global state & amendment slice:** `.claude_current_state.json.status` = `Design_Gate_Passed` (entry state per Lifecycle Guard §2/§10.1 for a design-gate-required cycle). `amended_backlog_slice_path` empty — used `stage4_backlog_slice.md` directly.
- **Release plan sealed:** `claude/cycles/2026-09-23__release-v9.7/state.json` — `status: "Validated"`, `publish_eligible: true`, `open_escalations: []`, `deferred_execution_blockers: []`. **Status-field note:** `sprint_planning_prompt.md` STEP -1.2's literal check text ("`status = Published`") does not match this cycle's schema-v2 vocabulary — `release_planning_prompt.md` (the engine that owns this field, lines ~1053/1061) explicitly documents that the cycle-local `state.json.status` is set to `Validated` at publish and is **never** written as `"Published"`; only the root `.claude_current_state.json` advances through `Published`/`Release_Planning_Complete` naming. Treated `status: Validated` + `publish_eligible: true` + empty escalations as satisfying STEP -1.2's intent. This exact drift is already this sprint's own **ST-22** (`BLG-GOV-333`, EPIC-05) — no new backlog item needed; noted here only so the discrepancy is visible at the point it was found, not silently absorbed.
- **Design gate:** `design_gate_required: true`, `design_gate_status: Passed` (`design_gate.md`, 29/29 cleared, 0 blocked) — ✅ passed cleanly, entered from `Design_Gate_Passed` so the bypass-audit branch does not apply.
- **Files, roles & write access:** All §5 source files present (`state.json`, `stage4_backlog_slice.md`, `backlog.md`, `release_plan.md` schema v2, `cycle_summary.md`, `workforce_capacity.md`). All 5 required authority role files present in `claude/agents/`. `lessons_learnt_prompt.md` present. Backlog slice contains 7 EPICs / 29 ST items.
- **Branch Safety Check (STEP 0):** `git branch --show-current` → `main`. Confirmed.

## Carry-Forward Items

2 items reviewed from `claude/cycles/2026-09-21__release-v9.6/lessons_learnt_closure.md` (`post_ship_complete: true`, most recently completed cycle):

| # | Observation | Sprint Planning disposition |
|---|-------------|------------------------------|
| 1 | Two `ESC-CLOSE-*` escalations were open at that closure, both 72h-SLA due 2026-09-26. | Already resolved — `git log` shows `995ceb2b` "Resolve ESC-CLOSE-20260923-01/-02" prior to this session. No action needed. |
| 2 | `execution_prompt.md §3.2.A` same-EPIC testing-gap consistency check deferred patch — 2 cycles carried, one more crosses the auto-escalation threshold. | Owned by Post-Ship Closure / `execution_prompt.md`'s own engine, not Sprint Planning's write scope. Flagged here for visibility only; no sprint-planning action taken. |

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt --format=json`: **clean** — 0 known vulnerabilities across all scanned dependencies (including transitive). Trend log row to be appended to `docs/ops/pip_audit_trend_log.md` in this session per STEP -1.6 (cycle: `2026-09-23__release-v9.7`, result: clean).

## Recurring Endpoint Coverage Audit (STEP -1.8)

`python3 scripts/audit_endpoint_test_coverage.py`: exit 0. 92 route decorators across 26 router files scanned; 8 documented `KNOWN_GAPS` exclusions; 0 undocumented gaps. Clean.

## Hygiene Advisories (STEP -1.7)

- **Prompt change log gaps:** Full date-scan performed across all Class 6 prompts with a `**Version:**` header in `claude/system/*.md`. All clean — every file's current header version matches its own latest-dated row in `prompt_change_log.md`. (`OPERATIONAL_GUIDE.md` and `release_planning_prompt.md` each carry multiple same-day 2026-09-23 rows; the true latest row for each — v4.204 and v2.55 respectively — matches the current header exactly once same-date rows are read in full rather than by first-match.)
- **"Before Sprint Planning" backlog items:** `grep -c "Provisional-Target: Before v9.7 sprint planning" claude/backlog/backlog.md` → 0 matches. No `## Pre-Sprint Backlog Advisory` section needed.

## Pre-Sprint Planning Required Decisions (cycle_summary.md)

| Decision | Resolution | Blocker? |
|----------|-----------|----------|
| **RISK-01** — `BLG-FEAT-74`'s exact scope (replay granularity, output format) undefined | **Resolved via the scope-confirmation sub-story path** (RISK-01's own first-listed mitigation option). `ST-01` phased into `ST-01a` (Scope confirmation — Head of Specs Team, referencing `po05_section13_preassessment.md`'s 6 binding conditions and `decision_record.md §2.7`'s 3 deferred questions), `ST-01b` (Backend replay mechanics, depends on ST-01a), `ST-01c` (Frontend selector/output view, depends on ST-01b). See Sprint Scope EPIC-01 in `sprint_backlog.md`. | **No** — sub-story created and sequenced ahead of implementation work, satisfying the pre-sprint decision's own stated resolution method. |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01b | ST-01a | Internal | Unresolved — sequenced, not yet started |
| ST-01c | ST-01b | Internal | Unresolved — sequenced, not yet started |
| ST-04 | ST-03 (soft) | Internal (shared file, `Reports.js` Monthly Financial Table) | Sequencing advisory, not a hard blocker — per `design_gate.md`'s sequencing reminder |
| ST-07 | EPIC-01 output copy (soft, RISK-02) | Internal (coordination) | Advisory — author the predictive-language lint rule with awareness of EPIC-01's retrospective-banner copy so it doesn't false-positive |

No circular dependencies detected.

## Execution Sequence

1. **EPIC-01** (flagship, longest lead time — start first): ST-01a → ST-01b → ST-01c
2. **EPIC-02**: ST-05, ST-06 (autonomous, trivial) → ST-02 → ST-03 → ST-04 (sequenced, shared file) → ST-07 (aware of EPIC-01 copy)
3. **EPIC-03**: ST-08, ST-09, ST-10, ST-11, ST-12 (autonomous, independent) → ST-13 (delegated_decision — Head of Engineering disposition call)
4. **EPIC-04**: ST-14, ST-15, ST-16, ST-17 (autonomous) → ST-18 (delegated_qa — real/staging Postgres run, see Risk Flags)
5. **EPIC-05**: ST-21, ST-22 (autonomous, governance wording/doc) → ST-19 (autonomous, metric spec) → ST-20 (delegated_decision — Strategy Rules & System Intent Owner ruling)
6. **EPIC-06**: ST-23, ST-24, ST-26 (autonomous, doc corrections) → ST-25 (delegated_decision — Data Model & Domain Schema Owner disposition, drop vs document)
7. **EPIC-07**: ST-28, ST-29 (autonomous) → ST-27 (delegated_backend — real/staging DB+SQL run, RISK-03)

Autonomous items are front-loaded within each EPIC ahead of delegated items, to unblock delegation round-trips early, per §12 invariant.

### Multi-EPIC Execution Notes (Required — 7 EPICs in scope)

- **`execution_state.json` owner:** **EPIC-01** — first in execution order (flagship item, longest runway, starts day one). All other EPIC branches must check for `execution_state.json` existence before creating their own version; if found, read and append their EPIC's section rather than overwrite.
- **Merge order:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06 → EPIC-07 (matches execution order above; no dependency requires reordering — `release_plan.md ## Execution Plan`'s sequencing constraint column reads "None" for every EPIC except EPIC-01's own internal phasing and EPIC-07's staging-slot timing note).
- **Shared-file ownership advisory:**
  - `Reports.js` (Monthly Financial Table): owned within EPIC-02 by ST-03, then ST-04 — same-EPIC sequencing only, no cross-EPIC conflict.
  - `.github/workflows/*.yml`: touched by both **EPIC-04** (ST-15 — CI check for merged `.skip()`/`.only()`) and **EPIC-07** (ST-29 — CI guard for non-registry dependency specifiers). EPIC-04 merges first in the sequence above; EPIC-07 must rebase onto `main` after EPIC-04 merges before finalising its own CI workflow change, per CLAUDE.md §8.
  - No other cross-EPIC shared-file overlap identified (EPIC-01's new files, EPIC-03's backend fee/alert modules, EPIC-05/06's governance/spec docs, and EPIC-07's ops docs/migration SQL are each EPIC-exclusive).

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01) | Valid — mitigated via ST-01a/b/c phasing (see Pre-Sprint Planning Required Decisions above) |
| RISK-02 | EPIC-02 (ST-07) | Valid — no hard ordering required; noted in Execution Sequence and Dependency Map as a soft coordination point |
| RISK-03 | EPIC-07 (ST-27) | Valid — routed to Infrastructure & Operations Owner for a delegated staging run at execution, same pattern as `ESC-EXEC-20260921-02`/`-03`/`-04`. This sandbox has no live database connection (`SBX-NO-LIVE-DB`, `shared_standards.md §16.16`) — code review alone does not satisfy ST-27's AC per its own Notes field. |

No risk has materialised since release planning; all three remain in their release-planning-assessed state.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| ST-13 disposition call (won't-fix-document vs. split latency_ms) | Head of Engineering | No — delegated_decision, resolved at execution kickoff |
| ST-18 real/staging Postgres validation run | Director of Quality | No — delegated_qa, `SBX-NO-LIVE-DB` applies; route to a delegated staging slot at execution |
| ST-20 SI-02 gate threshold disposition (re-examine vs confirm-closed) | Strategy Rules & System Intent Owner | No — delegated_decision, resolved at execution kickoff |
| ST-25 orphaned-columns disposition (drop vs document) | Data Model & Domain Schema Owner | No — delegated_decision, may require a staging schema read (`SBX-NO-LIVE-DB` applies if live confirmation is sought) |
| ST-27 staging verification of reflection-reminder migration/SQL | Infrastructure & Operations Owner | No — delegated_backend, `SBX-NO-LIVE-DB` applies; route to a delegated staging slot at execution (RISK-03) |

No outstanding action is marked `Blocker? Yes`. No `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders exist anywhere in this sprint's scope.

## Director of Quality Readiness Check (STEP 4.3)

Confirmed (agent-mediated, §5.3): QA criteria across all 29 items (7 EPICs) are sufficient to produce `qa_evidence_EPIC-xx.md` per EPIC at sprint close. No known test coverage gap blocks sign-off. Two items (ST-18, ST-27) require live/staging execution beyond this sandbox's reach (`SBX-NO-LIVE-DB`) — tracked above as Outstanding Actions, not coverage gaps.
