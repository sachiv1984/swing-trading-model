**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-14
**Cycle:** 2026-08-14__release-v8.8

# Sprint Planning Notes — 2026-08-14__release-v8.8

## Preflight Findings (Advisory)

- **Release plan sealing gap (self-caught, resolved before this run):** `claude/cycles/2026-08-14__release-v8.8/state.json` was found at `status: "Validated"` with an empty `sealed` block (Publish Sealing Checklist, `shared_standards/publish_gate.md` steps 1–5, had not executed despite the STEP 9/10 commit being titled "Published Release Plan"). Design Gate's own preflight doesn't check this field so it passed through undetected. Resolved out-of-band (commit `eb8c1bc3`, PMO Lead authorised) before this Sprint Planning run began: `sealed_utc` stamped, `status → Published`, matching the v8.4/v8.6/v8.7 precedent (`state_snapshot_hash` left empty, consistent with all three prior published cycles — this field is not populated in practice in this repo despite the checklist's literal text). Sprint Planning STEP -1 Hard Gate #2 passed cleanly on re-check.
- **STEP -1 Hard Gate #1 prose is stale relative to `lifecycle_schema.json`:** the gate's status-value list (`Published`/`Validated`/`Committed`) predates the Design Gate engine's addition of the `Design_Gate_Passed` root-pointer state. `lifecycle_schema.json`'s transition table (source of truth per `shared_standards.md §10.6`) explicitly defines `Design_Gate_Passed → Sprint_Planning_Complete` via `plan sprint`, entry condition `design_gate_status = Passed AND sprint_sealed = false` — both true here. Treated as satisfied; flagged here as a prompt-text drift for a future `BLG-GOV-*` filing, not a blocker.
- **Vulnerability scan (STEP -1 advisory 6):** `pip-audit` not installed in this environment (`command not found`). Recommend installing before/during sprint execution. Advisory only — does not block planning.
- **Hygiene advisories (STEP -1 advisory 7):** Prompt change log gap scan (date-scan method) run against `sprint_planning_prompt.md`, `design_gate_prompt.md`, `release_planning_prompt.md`, `shared_standards.md` — all four current header versions match their latest `prompt_change_log.md` row exactly. No gaps. No `backlog.md` items carry `Provisional-Target: Before v8.8 sprint planning` — no Pre-Sprint Backlog Advisory section required.
- **Endpoint test coverage audit (STEP -1 advisory 8):** `scripts/audit_endpoint_test_coverage.py` exit 0 — clean.

## Carry-Forward Items

Most recently completed cycle (`post_ship_complete = true`): `2026-08-11__release-v8.6`. `lessons_learnt_closure.md` carries 2 Carry-Forward items:

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `scripts/check_api_performance_baseline_drift.py`'s substring-matching false-negative fix has carried 3 consecutive cycles unresolved (out of Post-Ship Closure's write scope). | PMO Lead should file a `BLG-OPS-*` story directly rather than relying on closure-to-closure deferral. | Release Planning / Roadmap |
| 2 | `reports.md`'s cross-cycle deviation register concentration signal unchanged; 3rd deviation consolidation review not yet due. | No action needed next cycle either. | Delivery Verification / Post-Ship |

Neither item is addressed to Sprint Planning directly; no action taken here. Item 1 is a candidate for a follow-up backlog filing (out of this engine's write scope).

## Backlog Slice Source

Original — `claude/cycles/2026-08-14__release-v8.8/stage4_backlog_slice.md`. `.claude_current_state.json.amended_backlog_slice_path` is empty — no amendment in effect.

## Deferred Items

None. All 29 ST items across 7 EPICs are `include` — within capacity (20.50 / ~24–28 days), all owned, all AC-confirmed, none blocked.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-17 | ST-15 | Internal | Resolved — design gate decision record names the `secondary` Badge's first live call site as ST-15's new "Clear filters" control; ST-17's coverage AC for that half of scope is not actionable until ST-15 ships. |

No other cross-item dependencies identified. No circular dependencies.

## Execution Sequence

Multi-EPIC scope (7 EPICs) — sequence follows `release_plan.md ## Execution Plan` table order, which also reflects natural precedence (EPIC-02's ST-07 was found while investigating EPIC-01's ST-02):

1. **EPIC-01** — Live Data-Integrity & Scheduled Job Coverage (leads; 2 live P1 fixes; `execution_state.json` owner — see Multi-EPIC Execution Notes below)
2. **EPIC-02** — Backend Engineering Hardening (sequenced after EPIC-01 — ST-07 consolidation touches regime-check code adjacent to EPIC-01's ST-02 fix)
3. **EPIC-03** — Frontend UX & Dead-Code Cleanup (independent; design gate cleared; within-EPIC: ST-15 before ST-17)
4. **EPIC-04** — Quality & Test-Coverage Debt (independent)
5. **EPIC-05** — Security Hardening (independent)
6. **EPIC-06** — API & Spec Debt Closure (independent)
7. **EPIC-07** — Governance Correctness Fixes (independent; ST-29 touches `release_planning_prompt.md` STEP 9 area — no other EPIC touches that file this cycle, per RISK-07)

Within each EPIC, autonomous items are grouped ahead of delegated items where sequencing allows, per §5.2 guidance — see delegation classes in `sprint_backlog.md`.

## Multi-EPIC Execution Notes

**`execution_state.json` owner:** EPIC-01 (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, append their EPIC's section rather than overwrite.

**Shared file ownership advisory:**

| File | EPICs touching it | Owner (creates canonical version) | Note |
|------|--------------------|-------------------------------------|------|
| `docs/ops/api_performance_baseline.md` | EPIC-01 (ST-04, ST-05, ST-06) and EPIC-02 (ST-11, §36) | EPIC-01 | EPIC-02 must rebase onto `main` after EPIC-01 merges before finalising its §36 edit. |
| Backend market-regime code path (feeds `risk_off_exit` / `check_market_regime()`) | EPIC-01 (ST-02) and EPIC-02 (ST-07) | EPIC-01 | EPIC-02's consolidation (ST-07) must rebase onto `main` after EPIC-01 merges to avoid re-diverging the two regime-check implementations mid-consolidation. |

No `openapi.yaml` conflict expected — no story in this scope adds a new API endpoint (all touch existing endpoints or are non-API work).

## Delegation Classes (set at planning time — §12 invariant)

| Item | EPIC | Delegation Class | Rationale |
|------|------|-------------------|-----------|
| ST-01 | EPIC-01 | autonomous | Scheduled CI workflow addition, no UX, Design Not Applicable |
| ST-02 | EPIC-01 | autonomous | Backend data-refresh fix feeding an already-specified badge, Design Pre-Approved |
| ST-03 | EPIC-01 | delegated_backend | Root cause unconfirmed (RISK-01) — requires live GitHub Actions/Render log review at a specific step |
| ST-04 | EPIC-01 | delegated_backend | Baseline row requires live-measured timing consistent with existing methodology — `[staging-only evidence]` |
| ST-05 | EPIC-01 | delegated_backend | Same as ST-04 — `[staging-only evidence]` |
| ST-06 | EPIC-01 | delegated_backend | Explicitly requires ≥5 live staging samples — `[staging-only evidence]` |
| ST-07 | EPIC-02 | autonomous | Backend consolidation refactor, no UX, no behavioural regression permitted by AC |
| ST-08 | EPIC-02 | autonomous | Backend append-only table + migration, no UX |
| ST-09 | EPIC-02 | delegated_backend | Full linkage scope confirmed by Product Owner this session (schema + backend + frontend); backend-dominant, coordinate with Frontend Specs owner for the frontend wiring half |
| ST-10 | EPIC-02 | autonomous | Backend field population only |
| ST-11 | EPIC-02 | delegated_backend | AC requires verification against the next real scheduled/manual invocation — `[staging-only evidence]` |
| ST-12 | EPIC-02 | delegated_backend | Requires Head of Engineering sign-off at a specific step |
| ST-13 | EPIC-03 | delegated_frontend | Design Required, decision record exists |
| ST-14 | EPIC-03 | delegated_frontend | Design Required, decision record exists |
| ST-15 | EPIC-03 | delegated_frontend | Design Required — new interaction flow (filter controls, debounce timing) |
| ST-16 | EPIC-03 | autonomous | Design decision already resolved at design gate (Option B — remove); implementation is now straightforward deletion, no new UX to build |
| ST-17 | EPIC-03 | delegated_qa | Playwright test authoring; depends on ST-15's call site |
| ST-18 | EPIC-04 | delegated_qa | Audit + QA & Testing Owner sign-off required |
| ST-19 | EPIC-04 | delegated_qa | Report + QA & Testing Owner sign-off required |
| ST-20 | EPIC-04 | delegated_qa | Audit + QA Lead sign-off required |
| ST-21 | EPIC-04 | delegated_qa | Re-audit + QA & Testing Owner sign-off required |
| ST-22 | EPIC-05 | autonomous | Backend-only change; §13 pre-check already cleared at design gate (non-functional hardening of an existing cleared call site) |
| ST-23 | EPIC-05 | delegated_decision | Cybersecurity & Trust Lead sign-off required |
| ST-24 | EPIC-05 | delegated_decision | 16 baseline findings each need an explicit fix-or-accept-risk decision |
| ST-25 | EPIC-05 | autonomous | Documentation-only |
| ST-26 | EPIC-06 | autonomous | Documentation-only backfill |
| ST-27 | EPIC-06 | autonomous | Mechanical anchor correction + lightweight Head of Specs Team sign-off |
| ST-28 | EPIC-07 | autonomous | Mechanical governance doc correction + lightweight Head of Specs Team sign-off |
| ST-29 | EPIC-07 | delegated_decision | Governance prompt/ownership documentation change; must not conflict with STEP 9's own write to `.claude_current_state.json` this cycle (RISK-07) |

**LL-v2.0-P4-2 (test scenario gap):** ST-15 introduces new user-facing controls (filter bar) on an existing page. Flag for Sprint Execution engine to set `epics.EPIC-03.test_scenarios = "pending — QA & Testing Owner to author before next sprint on this domain"` in `execution_state.json` at initialisation.

**LL-v2.2-SP-01 (blocked-decision design artefact check, advisory):** For `delegated_decision` items ST-09, ST-23, ST-24, ST-29 — no HoST design-session artefact exists for any (none are UX decisions; they are backend-scope, security-risk-acceptance, and governance-ownership decisions respectively, outside the Head of UX & Design's remit). Recorded per the letter of the advisory; no action taken — these decisions belong to their named sign-off roles (Backend/Head of Engineering, Cybersecurity & Trust Lead, Head of Specs Team), not UX.

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-03) | Valid — sequenced first within EPIC-01 per original mitigation; delegation class `delegated_backend` reflects the live-log-review dependency |
| RISK-02 | EPIC-02 (ST-09) | Resolved at sprint planning — Product Owner confirmed full linkage scope (schema + backend + frontend) this session; see Outstanding Actions |
| RISK-03 | EPIC-03 (ST-13) | Valid — authoring-convention documentation update is in ST-13's own AC, not a separate follow-up |
| RISK-04 | EPIC-04 | Valid — no material risk, standard review |
| RISK-05 | EPIC-05 (ST-23, ST-24) | Valid — scans run as read-only audits first per original mitigation |
| RISK-06 | EPIC-06 | Valid — no material risk |
| RISK-07 | EPIC-07 (ST-29) | Valid — sequenced last, no other EPIC touches `release_planning_prompt.md`/`.claude_current_state.json` STEP 9 area this cycle |

No risk has materialised since release planning. No new escalations raised.

## Pre-Sprint Vulnerability Scan

`pip-audit` unavailable in this environment (`command not found`). Recommend installing before sprint execution begins. Advisory only — does not block sprint planning.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Install `pip-audit` in the execution environment | PMO Lead / Head of Engineering | No |
| File a `BLG-OPS-*` story for the carried-forward `check_api_performance_baseline_drift.py` false-negative fix (Carry-Forward item 1) | PMO Lead | No |
| Coordinate ST-09's frontend wiring half with Frontend Specs & UX Documentation Owner during execution | Backend Engineering Patterns Owner | No |

No outstanding action is marked `Blocker? Yes`. No `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders exist. No deferred execution blockers were present in the release plan (`deferred_execution_blockers: []`).
