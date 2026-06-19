**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-19
**Cycle:** 2026-06-19__release-v6.0

---

# Sprint Planning Notes — 2026-06-19__release-v6.0

---

## Backlog Slice Source

Original — `claude/cycles/2026-06-19__release-v6.0/stage4_backlog_slice.md`

No amendment was sealed. `amended_backlog_slice_path` is empty in `.claude_current_state.json`.

---

## Carry-Forward Items

2 carry-forward items from prior cycle `2026-06-17__release-v5.9` reviewed (source: `lessons_learnt_closure.md ## Carry-Forward`):

| # | Item | Target Engine | Status at Sprint Planning |
|---|------|--------------|--------------------------|
| 1 | BLG-FE-64 gate 2026-06-21 — 6th consecutive carry-forward; gate should have cleared | Release Planning | Addressed: ST-06 included as conditional (EPIC-04 Cluster A, gate 2026-06-21). Perennial-return advisory applied per STEP 1.4b. |
| 2 | BLG-OPS-70 SI-05 deep link trailing obligation (gate ~2026-06-23) | Release Planning | Addressed: ST-05 included as conditional (EPIC-03, gate ~2026-06-23). |

Both carry-forward items were targeted at the Release Planning engine and have been addressed in v6.0 release planning. No carry-forward actions outstanding for Sprint Planning.

---

## Design Gate IMP-04 Bypass — Resolved

**Status:** RESOLVED — design gate ran and Passed 2026-06-19.

`design_gate_status = "Passed"` in both `state.json` and `.claude_current_state.json`. The sprint planning prompt §STEP -1.3 specifies: "If entered from `Design_Gate_Passed`: skip bypass audit." The IMP-04/IMP-30 bypass authority requirement is not applicable for this cycle.

Design gate artefact: `claude/cycles/2026-06-19__release-v6.0/design_gate.md`. 3 UX specs produced (morning-briefing, net-of-costs-tracking, screener-quality-telemetry). 4 frontend specs updated (dashboard.md v2.1, trade_history.md v1.10, reports.md v0.5, screener_results.md v1.3).

---

## Capacity WARN Acknowledgement

**Status:** RESOLVED — Product Owner acknowledged capacity WARN 2026-06-19.

Capacity check outcome: WARN (all-conditional scenario ~10.85 days, within ~12–14 day ceiling but approaching it). Firm scope (6.5 days): PASS.

Product Owner acknowledgement: Confirmed — 10.85-day all-conditional scenario accepted; phased gate-cluster structure is the risk management mechanism — 2026-06-19.

---

## Gate Tracking — Sprint Planning Checklist

| Gate | Date | Items | Sprint Planning Status |
|------|------|-------|----------------------|
| SI-03 ≥ 30 days | 2026-06-21 | ST-06, ST-07 | Gate date within sprint; 2 days from planning date (2026-06-19). SI-03 live since ~2026-05-22; gate clears 2026-06-21 if ≥ 30 days hold. Execution Engine to confirm at gate date. |
| SI-05 next digest | ~2026-06-23 | ST-05 | Gate date within sprint; FRONTEND_URL set 2026-06-17. Await confirmed digest delivery with working deep links. |
| SI-05 effectiveness review | 2026-07-04 | ST-08, ST-09, ST-10, ST-11 | Gate date within sprint (final days). Review scheduled; Execution Engine to confirm date held before scheduling Cluster B work. |
| SI-02 gate re-check | At sprint planning | (conditional add) | Gate NOT met. ~13 closed trades as of 2026-06-16 at ~1.5/week; ~13–14 trades as of 2026-06-19. Need ≥20. Projected ~2026-07-02. If gate clears during sprint, invoke amendment cycle. |

---

## Deferred Items

No items from the authoritative backlog slice (ST-01 through ST-11) are deferred at planning. All 11 items are included in the sprint backlog (4 firm + 7 conditional).

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| PT-04 (BLG-FEAT-25) | N/A — not in backlog slice | Gate not met: ~13–14 closed trades, need ≥20 (trajectory ~2026-07-02). Not in backlog slice — excluded at release planning. | Yes (amendment if gate clears during sprint) |
| SI-02 frontend (BLG-FE-52/53) | N/A — not in backlog slice | Gate not met: <20 closed trades. Not in backlog slice — excluded at release planning. | Yes (amendment if gate clears during sprint) |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-07 | ST-06 | Internal (EPIC-04) | Within-sprint — ST-06 must complete first |
| ST-07 | Gate 2026-06-21 | External (date gate) | Gate not yet clear; clears 2 days into sprint |
| ST-06 | Gate 2026-06-21 | External (date gate) | Same as ST-07 |
| ST-05 | SI-05 digest delivery | External (event gate) | Gate ~2026-06-23; depends on Telegram delivery |
| ST-08 | 2026-07-04 effectiveness review | External (event gate) | Gate ~end of sprint |
| ST-09 | 2026-07-04 effectiveness review | External (event gate) | Same as ST-08; also depends on BLG-GOV-113 protocol |
| ST-10 | 2026-07-04 effectiveness review | External (event gate) | Same gate; also requires BLG-GOV-121 §13 pre-clearance status |
| ST-11 | SI-05 ≥ 4 weeks production | External (date gate) | Gate 2026-07-04 (SI-05 live 2026-06-04) |
| EPIC-02 | EPIC-01 | Sequential | Execution sequence constraint: EPIC-02 after EPIC-01 |
| EPIC-03 (firm) | EPIC-01 | Sequential | After EPIC-01; parallel with EPIC-02 possible |
| EPIC-04 | Gate clearance | External | Activates cluster-by-cluster as gates clear |

No circular dependencies. ✅

---

## Execution Sequence

### Firm Scope (Phase 1 — Days 1–7)

1. **ST-01** (EPIC-01) — P0 first; unblocked; autonomous
2. **ST-04** (EPIC-03 firm) — after EPIC-01; can parallel with EPIC-02 work; autonomous
3. **ST-02** (EPIC-02) — after EPIC-01; autonomous
4. **ST-03** (EPIC-02) — after/parallel with ST-02; autonomous

### Conditional Scope (Phase 2 — as gates clear)

5. **ST-06** (EPIC-04 Cluster A, gate 2026-06-21) — delegated_decision; schedule immediately when gate confirmed
6. **ST-07** (EPIC-04 Cluster A, depends ST-06) — delegated_decision; after ST-06
7. **ST-05** (EPIC-03 conditional, gate ~2026-06-23) — autonomous; after digest delivery confirmation
8. **ST-08** (EPIC-04 Cluster B, gate 2026-07-04) — delegated_decision; independent within cluster
9. **ST-09** (EPIC-04 Cluster B, gate 2026-07-04) — autonomous; independent
10. **ST-10** (EPIC-04 Cluster B, gate 2026-07-04) — delegated_decision; independent
11. **ST-11** (EPIC-04 Cluster B, gate 2026-07-04) — autonomous; independent

---

## Multi-EPIC Execution Notes

**EPICs in sprint:** 4 (EPIC-01, EPIC-02, EPIC-03, EPIC-04)

**execution_state.json owner:** EPIC-01 (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

**Merge order:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04

**Rationale:** EPIC-01 is standalone (signal_service.py only; no shared file conflicts). EPIC-02 contains the larger data model change (trade cost fields in data_model.md). EPIC-03 shares API contract files with EPIC-02. EPIC-04 is documentation/design with no code conflicts.

**Shared file ownership advisory:**

| Shared File | EPIC Owner | Advisory for Later EPICs |
|-------------|------------|--------------------------|
| `docs/specs/api_contracts/` | EPIC-02 (ST-03 trade history contract), EPIC-03 (ST-04 screener results contract) | EPIC-03 must rebase onto `main` after EPIC-02 merges before finalising screener contract changes |
| `docs/reference/openapi.yaml` | EPIC-02 (first to potentially add endpoints) | EPIC-03 must rebase onto `main` after EPIC-02 merges; take union of all path additions |
| `data_model.md` | EPIC-02 (ST-03 trade cost fields) | EPIC-03 and EPIC-04 should not modify data_model.md — if needed, rebase after EPIC-02 merges |

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01, ST-01 | Valid — Strategy Rules & System Intent Owner sign-off is AC-01 of ST-01; blocking condition explicit in acceptance criteria |
| RISK-02 | EPIC-02, ST-02 | Valid — 5 composing endpoints confirmed live at release planning; low risk |
| RISK-03 | EPIC-02, ST-03 | Valid — optional fields only; backward-compatible migration; existing R-multiple unaffected |
| RISK-04 | EPIC-03, ST-05 | Valid — classified conditional per STEP 1.4b; returns to backlog if digest not confirmed by sprint close |
| RISK-05 | EPIC-04, all | Valid HIGH — multiple within-sprint date gates; if gates missed, 7th consecutive deferral for BLG-FE-64. Mitigated by explicit gate tracking. PO has made explicit disposition (retain conditional). Gate 2026-06-21 is 2 days from planning date. Time-critical: schedule ST-06 promptly on gate confirmation to avoid same-cycle miss. |

---

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt` was attempted but the tool is not installed in this environment. Advisory: install `pip-audit` before sprint execution begins to establish a pre-execution baseline. PO and Head of Engineering to accept this advisory gap.

---

## Prompt Change Log Advisory

| File | Current Version | Last Log Entry | Status |
|------|----------------|----------------|--------|
| `sprint_planning_prompt.md` | v3.10 | v3.9→v3.10 (2026-06-16) | ✅ No gap |
| `execution_prompt.md` | v3.45 | v3.44→v3.45 (2026-06-18) | ✅ No gap |

Only the most recently invoked prompts checked (advisory). Full governance drift check available via `/governance-drift` skill.

---

## LL-v2.2-SP-01 Design Artefact Check

Delegated_decision items in scope:
- ST-06 (BLG-FE-64, delegated_decision): Design review brief IS the deliverable — ST-06 produces the artefact. No prior artefact required. ✅
- ST-07 (BLG-FE-41, delegated_decision): Depends on ST-06 brief. ST-06 brief serves as design input. ✅
- ST-08 (BLG-GOV-112, delegated_decision): Effectiveness review outputs (BLG-GOV-113 protocol) serve as input. ✅
- ST-10 (BLG-GOV-130, delegated_decision): Effectiveness review outputs + BLG-GOV-121 §13 pre-clearance serve as inputs. ✅

No missing design artefacts. ✅

---

## BLG-GOV-72 Frontend Classification Fast-Path

| Story | Default Classification | Applied Classification | Justification |
|-------|----------------------|----------------------|---------------|
| ST-02 | autonomous (frontend composition, no new design) | autonomous | Composes from 5 existing live endpoints; follows DashboardHome extension pattern ✅ |
| ST-04 | autonomous (backend + frontend, existing patterns) | autonomous | Screener panel enhancement following existing patterns ✅ |
| ST-06 | delegated_decision (UX document production) | delegated_decision | Document production owned by Head of UX & Design; engine produces brief under delegation ✅ |
| ST-07 | delegated_decision (UX design review) | delegated_decision | Design review and recommendation document; Head of UX & Design owns ✅ |

---

## Outstanding Actions

| Action | Owner | Required Before Seal? | Blocker? |
|--------|-------|----------------------|---------|
| Set `design_gate_bypass_authority = "Head of UX & Design + Product Owner"` in `.claude_current_state.json` (IMP-04, IMP-30) | Head of UX & Design + Product Owner jointly | Yes | Yes |
| Set `design_gate_bypass_reason` in `.claude_current_state.json` with justification (IMP-04) | Head of UX & Design + Product Owner jointly | Yes | Yes |
| Product Owner acknowledge capacity WARN (IMP-41) — all-conditional scenario ~10.85 days, within 14-day ceiling | Product Owner | Yes | Yes |
| Product Owner confirm sprint goal in `sprint_goal.md` | Product Owner | Yes | Yes |
| Product Owner sign off sprint backlog (scope, capacity, deferred blockers N/A) | Product Owner | Yes | Yes |
| Verify SI-03 ≥ 30 days at gate date 2026-06-21 before scheduling ST-06/ST-07 | PMO Lead / Execution Engine | No | No |
| Monitor PT-04/SI-02 trade count gate (~2026-07-02 trajectory); invoke amendment if gate clears | PMO Lead | No | No |
| Install pip-audit before sprint execution for vulnerability baseline | Head of Engineering | No | No |
