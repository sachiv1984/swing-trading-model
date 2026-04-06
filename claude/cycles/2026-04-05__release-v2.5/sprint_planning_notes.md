**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-06
**Cycle:** 2026-04-05__release-v2.5

---

# Sprint Planning Notes — 2026-04-05__release-v2.5

## Backlog Slice Source

Original — `claude/cycles/2026-04-05__release-v2.5/stage4_backlog_slice.md`
(No amendment active — `amended_backlog_slice_path` field is empty)

---

## Carry-Forward Items (from cycle 2026-03-31__release-v2.4)

3 items reviewed from `claude/cycles/2026-03-31__release-v2.4/lessons_learnt_closure.md ## Carry-Forward`:

| # | Item | Disposition |
|---|------|-------------|
| CF-1 | v2.4 prompt change log hygiene gap — deferred patches applied mid-sprint without log entries | Surfaced as Sprint Planning advisory: any in-sprint prompt edits (including ST-12 deferred patch application) must log to `prompt_change_log.md` in the same session as the edit. |
| CF-2 | `delivery_verification_prompt.md` seal gate patch (blank sign-off dates) | Resolved — scheduled as ST-12 ✅ |
| CF-3 | `trade_history.md` Known Deviations entry for DEV-ST14-01 absent | Resolved 2026-04-04 ✅ |

---

## Design Gate Bypass (IMP-04 Outstanding Action)

**Status: BLOCKER for sprint seal**

`design_gate_status` is `not_started` in `state.json`. Sprint Planning entered from `Release_Planning_Complete` — design gate was not run for this cycle. Per IMP-04 and `team_charter.md §3.3`:

- `design_gate_bypass_authority` is absent from `.claude_current_state.json`
- `design_gate_bypass_reason` is absent from `.claude_current_state.json`

Per IMP-30, bypass authority must record both: **Head of UX & Design (primary) + Product Owner (co-confirmation)**.

**Action required before sprint seal:**
1. Head of UX & Design (primary) and Product Owner (co-confirmation) must confirm design gate bypass
2. `design_gate_bypass_authority` field must be written to `.claude_current_state.json` (value: `"Head of UX & Design + Product Owner"`)
3. `design_gate_bypass_reason` field must be written to `.claude_current_state.json` (one sentence: reason design gate is not required for this cycle)

Items with frontend/UX changes in scope: ST-03 (SystemStatus.js categorisation), ST-08 (StatsCard gradient cosmetic), ST-09 (new Avg Fee Drag StatsCard + TradeHistoryTable column). None introduce new pages or navigation; changes are additive to existing components.

---

## Prompt Change Log Hygiene (Advisory — STEP -1.11)

The following prompts have version gaps between their current `**Version:**` header and their last `prompt_change_log.md` entry. Advisory only — does not block planning.

| Prompt | Last logged version | Current version | Gap |
|--------|--------------------|-----------------|----|
| `release_planning_prompt.md` | v2.21 (2026-03-22) | v2.25 | ⚠ v2.21→v2.25 unlogged |
| `design_gate_prompt.md` | (no entry found) | v1.1 | ⚠ v1.1 unlogged |
| `amendment_cycle_prompt.md` | v1.5 (2026-03-10) | v1.6 | ⚠ v1.5→v1.6 unlogged |
| `roadmap_prompt.md` | v4.3 (2026-03-21) | v4.7 | ⚠ v4.3→v4.7 unlogged |

Head of Specs Team to audit and backfill per advisory from `cycle_summary.md`. (Previously surfaced as advisory in v2.5 release planning — not yet actioned.)

---

## Pre-Sprint Vulnerability Scan (STEP -1.9)

`pip-audit -r backend/requirements.txt --format=json` executed 2026-04-06.

**Result: CLEAN** — 0 vulnerabilities found across 56 packages.

No CVE backlog items required. Pre-sprint pip-audit: clean.

---

## Deferred Items

No items deferred at sprint planning. All 13 items are within confirmed capacity and have defined acceptance criteria.

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | — | — |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal (Sprint 1) | Sequencing constraint — auth forwarding must work first for sync results to be meaningful. ST-02 can proceed independently but testing depends on ST-01 merged. |
| ST-03 | ST-01 | Advisory (Sprint 1) | ST-03 frontend categorisation is independent of backend fix, but testing is most meaningful after ST-01. Can execute in parallel. |
| ST-09 | None | — | Spec updates (metrics_definitions.md, trade_history.md, trade_endpoints.md, openapi.yaml) must land in same commit as implementation per CLAUDE.md. EPIC-03 branch should branch from up-to-date main after EPIC-01 merges to avoid openapi.yaml conflicts (RISK-03). |
| ST-13 | ST-01 (advisory) | Advisory (Sprint 1) | ST-13 test scenarios benefit from referencing ST-01 implementation; can proceed once ST-01 is merged. No hard dependency. |
| ST-04, ST-05 | None | — | Parallel reviews, independent. |
| ST-06 | ST-04, ST-05 (advisory) | Advisory (Sprint 2) | Latency investigation benefits from knowing integration state from ST-04/ST-05. No hard dependency. |

No circular dependencies detected.

---

## Execution Sequence

### Sprint 1

1. **ST-12** — Apply v2.4 deferred governance prompt patches (EPIC-04, autonomous)
   *Rationale: patches must govern remaining sprint execution; seal early.*
2. **ST-10** — Fix governance_sync.yml batch push closure (EPIC-04, autonomous)
3. **ST-11** — Formalise backlog entry placement standard (EPIC-04, autonomous)
4. **ST-01** — Fix auth forwarding in POST /test/endpoints (EPIC-01, autonomous)
   *Dependency anchor: ST-02, ST-03, ST-13 benefit from ST-01 merging first.*
5. **ST-02** — Sync endpoint test list with openapi.yaml (EPIC-01, autonomous) — after ST-01
6. **ST-03** — Fix System Status endpoint categorisation (EPIC-01, autonomous) — after ST-01
7. **ST-13** — Create test scenarios for EPIC-01 correctness (EPIC-04, autonomous) — after ST-01 merged

### Sprint 2

1. **ST-04** — Review and document Reports page backend integration (EPIC-02, autonomous)
2. **ST-05** — Review and document Signals page backend integration (EPIC-02, autonomous) — parallel with ST-04
3. **ST-07** — Add --max-time to GitHub Actions curl calls (EPIC-03, autonomous) — any time
4. **ST-08** — Fix Avg Slippage StatsCard gradient rendering (EPIC-03, autonomous) — any time
5. **ST-06** — Investigate high external latency on DB-backed endpoints (EPIC-02, delegated_backend) — after ST-04, ST-05 advisory
6. **ST-09** — Fee drag metric on Trade History (EPIC-03, delegated_frontend) — branch from main after EPIC-01 merges (RISK-03 note)

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01) | Valid — AC explicitly requires API key forwarding (not middleware bypass). Security surface constraint recorded in ST-01 AC. |
| RISK-02 | EPIC-02 (ST-04, ST-05, ST-06) | Valid — review scope is documentation only; gaps produce backlog items, not in-scope fixes. No sprint overrun risk. |
| RISK-03 | EPIC-03 (ST-09) | Valid — EPIC-03 branch must be created from up-to-date main after EPIC-01 merges to avoid openapi.yaml conflicts. Sequencing note in execution sequence above. |
| RISK-04 | EPIC-04 (ST-12) | Valid — ST-12 sequenced first in Sprint 1. EPIC-04 targeted for Sprint 1 seal before Sprint 2 execution begins. |

---

## Test Scenario Gap Flag (LL-v2.0-P4-2)

ST-09 (EPIC-03, delegated_frontend) introduces new user-facing controls on an existing page (new "Avg Fee Drag" StatsCard + "Fee Drag %" column in TradeHistoryTable).

**Flag:** EPIC-03 `test_scenarios` field in execution_state.json: **pending** — QA & Testing Owner to author visual/functional test scenarios for ST-09 before delivery verification. Scenarios should cover: StatsCard renders with correct value, column always populated (no `—`), formula correctness check (exit_fees / gross_proceeds × 100).

---

## Blocked-Decision Advisory (LL-v2.2-SP-01)

No items classified `delegated_decision` in this sprint. Advisory not applicable.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? | Status |
|--------|-------|----------------------|--------|
| Provide `design_gate_bypass_authority` (value: `"Head of UX & Design + Product Owner"`) and `design_gate_bypass_reason` (one sentence) — write to `.claude_current_state.json` | Head of UX & Design (primary) + Product Owner (co-confirmation) | **Yes** — IMP-04, IMP-30 | Open |
| Confirm sprint goal in `sprint_goal.md` | Product Owner | **Yes** | Open |
| Confirm sprint scope in `sprint_backlog.md` | Product Owner | **Yes** | Open |
| Backfill `prompt_change_log.md` entries for release_planning_prompt.md, design_gate_prompt.md, amendment_cycle_prompt.md, roadmap_prompt.md version gaps | Head of Specs Team | No (advisory) | Open |
