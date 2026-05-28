**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-28
**Cycle:** 2026-05-27__release-v4.2

---

# Sprint Planning Notes — v4.2

---

## Preflight Summary

| Gate | Result | Notes |
|------|--------|-------|
| Global state (status=Published) | PASS | No amended slice path |
| Release plan sealed | PASS | publish_eligible=true, 0 open escalations, 0 deferred blockers |
| Design gate (IMP-04 bypass audit) | FLAG — seal blocker | state.json design_gate_status=null; .claude_current_state.json=Not_Required; cycle_summary confirms no UX items. design_gate_bypass_authority and design_gate_bypass_reason must be populated before seal (per IMP-04/IMP-30 standard mode). |
| Backlog slice | PASS | 4 EPICs, 13 stories |
| Required files | PASS | All authority roles present; lessons_learnt_prompt.md present |
| Pre-sprint decisions | PASS | No blocking decisions required |
| pip-audit | PASS | 0 vulnerabilities (run 2026-05-28) |
| Prompt change log gaps | PASS | 0 gaps detected |
| Pre-sprint backlog items (Before v4.2) | PASS | None found |

---

## Carry-Forward Review (from 2026-05-26__release-v4.1 lessons_learnt_closure.md)

2 carry-forward items identified:

| # | Item | Status |
|---|------|--------|
| 1 | P3-01: EPIC PR number null recurrence — STEP 5.0A guard deferred to v4.2 (Head of Specs Team) | **RESOLVED** — AUD-2026-05-27-002 applied execution_prompt.md v3.29→v3.30 with STEP 5.0A null pr_number recovery guard on 2026-05-27, prior to this planning run |
| 2 | P3-05: STEP 5.2 returned_to_backlog wording implies sprint-close-only transition — deferred to v4.2 (Head of Specs Team) | **RESOLVED** — AUD-2026-05-27-003 applied execution_prompt.md clarification on 2026-05-27, prior to this planning run |

Both carry-forward items resolved by AUD-2026-05-27 before v4.2 planning commenced. No v4.2 story required.

Carry-forward items reviewed: 2 items from cycle `2026-05-26__release-v4.1`. Both resolved.

---

## Capacity WARN Acknowledgement

Release plan recorded a WARN for Sprint 2 (~7.75 days vs old 8–10 day baseline). Under the revised workforce_capacity.md baseline (12–14 days/sprint, effective 2026-05-27), Sprint 1 (~4.75 days) and Sprint 2 (~6.25 days) are both within capacity. No over-allocation. Product Owner acknowledgement: capacity_warn_acknowledged confirmed valid — WARN from release plan is superseded by revised baseline.

---

## Dependency Map

### Sprint 1 Dependencies

| Item | Depends on | Type | Notes |
|------|-----------|------|-------|
| ST-01 | None | — | Pure governance/security review |
| ST-02 | None | — | Policy document + code check; may reference ST-01 charter findings |
| ST-03 | None | — | Log hygiene policy; independent of ST-01/ST-02 |
| ST-04 | None (OA-3 standalone) | — | Live environment run coordination required |
| ST-05 | None | — | Can use "or equivalent" data source if claude_audit_log not yet live |
| ST-06 | None | — | Requires live environment; independent of ST-04/ST-05 |

No circular dependencies in Sprint 1. EPIC-01 and EPIC-02 are fully independent.

### Sprint 2 Dependencies

| Item | Depends on | Type | Notes |
|------|-----------|------|-------|
| ST-11 | None | — | Prerequisites checklist, independent |
| ST-12 | None | — | PO input required for SI-04 scope definition |
| ST-13 | None | — | Uses existing qa_evidence files and backlog.md |
| ST-07 | Ideally after ST-05 (EPIC-02) | Advisory | ST-05 monthly review benefits from audit trail data; however ST-05 is scoped "or equivalent" data source — not a hard dependency |
| ST-08 | None | — | Independent spec update |
| ST-09 | None | — | Strategy document, no implementation dependency |
| ST-10 | None | — | Optional assessment; independent |

No circular dependencies in Sprint 2. EPIC-03 and EPIC-04 are fully independent. Advisory: ST-05 (Sprint 1) should complete before ST-07 audit trail is queried for monthly review data — scoped as "or equivalent" so not a hard gate.

---

## Execution Sequencing

**Overall execution order:** EPIC-01 → EPIC-02 → EPIC-04 → EPIC-03

**Sprint 1:** EPIC-01 first (pure documentation/policy, unblocked), EPIC-02 second (OA-3 obligation + baselines — benefits from EPIC-01 governance groundwork)

**Sprint 2:** EPIC-04 first (SI-02 prerequisites + governance prep, fully independent), EPIC-03 second (backend implementation + spec debt — GOV-63 audit trail ideally ships last for data fidelity in future OPS-36 reviews)

Rationale for EPIC-04 before EPIC-03 in Sprint 2: EPIC-04 is documentation-only (S items), unblocked, can proceed immediately. EPIC-03 contains the M-effort backend implementation (ST-07) which benefits from running after EPIC-04 completes, allowing the sprint to close governance prep before heavier engineering work begins.

---

## Multi-EPIC Execution Notes

**execution_state.json owner (Sprint 1):** EPIC-01 creates `execution_state.json`. EPIC-02 must check for existence before creating — if found, append. Do not overwrite.

**execution_state.json owner (Sprint 2):** EPIC-04 creates its section in `execution_state.json` (appending to EPIC-01/EPIC-02 entries). EPIC-03 must check for existence and append. Do not overwrite.

**Overall:** EPIC-01 is the canonical `execution_state.json` owner for the full cycle. All subsequent EPICs (EPIC-02, EPIC-04, EPIC-03) append.

---

## Shared File Advisory

No files are shared between Sprint 1 EPICs (EPIC-01 and EPIC-02) that would create a conflict.

For Sprint 2:
- `docs/reference/openapi.yaml`: EPIC-03 owns (ST-07 audit trail route + ST-08 contract update). EPIC-04 does not touch this file.
- `docs/specs/api_contracts/ai_thesis_generation.md` or similar: EPIC-03 owns (ST-08). No conflict with EPIC-04.
- `claude/backlog/backlog.md`: No EPIC modifies this during execution.

No shared-file conflicts exist across EPICs. Standard rebase-onto-main advisory applies at merge time for each EPIC.

---

## Risk Confirmation

| RISK-ID | Mitigation status |
|---------|-----------------|
| RISK-01 (EPIC-01): Anthropic API key scope review may find broader-than-expected exposure | Low — all items advisory/documentation; no production changes if review passes ✅ |
| RISK-02 (EPIC-02): BLG-OPS-35 api_performance_baseline requires live environment run | Low — estimated baseline acceptable if live run not feasible; Infrastructure & Operations Owner coordinates ✅ |
| RISK-03 (EPIC-03): BLG-GOV-63 audit trail may surface schema migration requirement | Medium — scoped on BLG-GOV-35 Gemini pattern (shipped); migration overhead low ✅ |
| RISK-04 (EPIC-04): SI-02 prerequisites checklist requires consolidating 8+ items | Low — PMO Lead owns; 2-cycle pre-work context exists ✅ |

No new materialised risks since release planning.

---

## Scope Selection Summary

| Item | Classification | Reason |
|------|---------------|--------|
| ST-01 | include | P1/P2, within capacity, owned |
| ST-02 | include | P2, within capacity, owned |
| ST-03 | include | P2, within capacity, owned |
| ST-04 | include | P1/OA-3, within capacity, owned |
| ST-05 | include | P1, within capacity, owned |
| ST-06 | include | P2, within capacity, owned |
| ST-07 | include | P1, within capacity, owned |
| ST-08 | include | P1, within capacity, owned |
| ST-09 | include | P1, within capacity, owned |
| ST-10 | include (optional) | P2, within capacity; first deferral candidate if Sprint 2 overloads |
| ST-11 | include | P1, within capacity, owned |
| ST-12 | include | P2, within capacity, owned |
| ST-13 | include | P2, within capacity, owned |

All 13 items included. No items deferred at planning.

---

## Design Gate Bypass Advisory (IMP-04 Seal Blocker)

**Status:** SEAL BLOCKER — must be resolved before sprint backlog can be sealed.

`design_gate_status` is null in `state.json`; `.claude_current_state.json` records `Not_Required`. Cycle summary confirms: "Design Gate: Not required. No UX design decisions in v4.2 scope. All items are governance, operations, spec, or backend assessment type."

Per IMP-04/IMP-30 (standard mode): sprint cannot seal until the following fields are populated in `.claude_current_state.json`:
- `design_gate_bypass_authority`: must contain both "Head of UX & Design + Product Owner" (IMP-30)
- `design_gate_bypass_reason`: must explain why design gate not required

**Awaiting:** Product Owner + Head of UX & Design confirmation.

---

## Staging-Only AC Pre-Designations (per LL-v3.9-P3-2)

The following ACs require live environment access and cannot be verified in CI:

| Story | AC | Designation | Backlog item obligation |
|-------|-----|-------------|------------------------|
| ST-03 | AC-02 | [staging-only evidence] — Render prod log inspection required | File BLG item before PR opens if staging deferred to post-merge |
| ST-04 | AC-02 | [staging-only evidence] — live environment timing run required | BLG-OPS-35 already filed; coordinate with Infrastructure & Operations Owner |
| ST-05 | AC-01 | [staging-only evidence] — actual API call volume/cost data from live logging required | File BLG item before PR opens if actual data not obtainable in sprint |
| ST-06 | AC-01 | [staging-only evidence] — minimum 10 sample calls from live environment required | File BLG item before PR opens if live run deferred to post-merge |

These designations are recorded at planning time to prevent P3 surprise deviations at delivery verification.

---

## Pre-Sprint Backlog Advisory

No items found with `Provisional-Target: Before v4.2 sprint planning` in backlog.md.
