**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-03
**Cycle:** 2026-06-03__release-v5.0

---

# Sprint Planning Notes — 2026-06-03__release-v5.0

## Backlog Slice Source

Original — `claude/cycles/2026-06-03__release-v5.0/stage4_backlog_slice.md` (no amendment active)

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| ST-14 (SI-05 Phase 1 implementation) | Gate condition: SI-01 + SI-03 live ≥ 30 days — clears 2026-06-21 | Yes — Sprint 2 via amendment cycle |

**Planning-deferred item traceability (AUD-2026-05-21-002):** When the execution engine initialises `execution_state.json` for this cycle, it must add:
```yaml
epics.EPIC-04.stories.ST-14:
  status: deferred_at_planning
  gate_condition: "BLG-GOV-67 gate: SI-01 + SI-03 live ≥ 30 days; clears 2026-06-21"
```

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-10 (SI-05 Telegram message format spec) | ST-09 (channel decision must confirm Telegram) | Internal / EPIC-04 | Resolved at execution — ST-09 must complete first within EPIC-04 |
| EPIC-02 (ST-04/05 prompt_change_log.md appends) | EPIC-01 (ST-01 prompt_change_log.md appends) | Cross-EPIC / shared file | Resolved by merge order EPIC-01 → EPIC-02 |
| EPIC-04 (backlog.md closures) | EPIC-03 (backlog.md closure: BLG-OPS-52) | Cross-EPIC / shared file | Resolved by merge order EPIC-03 → EPIC-04 |

**ST-10 dependency detail:** ST-10 scope is Telegram-format spec. If ST-09 confirms Telegram, engine proceeds per spec. If ST-09 confirms in-app notification, ST-10 scope shifts to in-app notification spec (per backlog slice note). PO to confirm scope at execution start of ST-10.

## Execution Sequence

### Sprint 1 (firm)

1. **EPIC-01** (3 stories — S+S+XS, ~7 hrs)
   - ST-01 → ST-02 → ST-03 (sequential within EPIC; ST-01 first to verify prompt_change_log.md before EPIC-02 appends)

2. **EPIC-02** (2 stories — M+M, ~12 hrs) — after EPIC-01 merges
   - ST-04 → ST-05 (sequential; ST-04 execution_prompt.md patch before ST-05 post_ship_closure.md patch)

3. **EPIC-03** (3 stories — S+S+XS, ~7 hrs) — after EPIC-02 merges
   - ST-06 → ST-07 → ST-08 (ST-06/ST-07 code changes; ST-08 staging verification can proceed in parallel after ST-06/ST-07 complete)

4. **EPIC-04** (5 firm stories — 5×S, ~15 hrs) — after EPIC-03 merges
   - ST-09 → ST-10 (ST-09 must confirm channel before ST-10 authors format spec)
   - ST-11, ST-12, ST-13 (independent — can proceed in any order alongside ST-09/10)

### Sprint 2 (conditional — gate 2026-06-21)

5. **EPIC-04 Sprint 2**: ST-14 (M, ~6 hrs) — via amendment cycle after gate confirmed

## Multi-EPIC Execution Notes

**execution_state.json owner:** EPIC-01 (first in execution order). EPIC-02, EPIC-03, and EPIC-04 must check for `execution_state.json` existence before creating their own version — if found, read and append their EPIC section rather than overwrite.

**Shared file ownership:**

| File | EPICs modifying | Owner EPIC | Rebase advisory |
|------|-----------------|------------|-----------------|
| `claude/system/prompt_change_log.md` | EPIC-01 (ST-01), EPIC-02 (ST-04, ST-05) | EPIC-01 | EPIC-02 must rebase onto main after EPIC-01 merges before finalising prompt_change_log.md changes |
| `claude/backlog/backlog.md` | EPIC-03 (ST-08: close BLG-OPS-52), EPIC-04 (ST-09–13: close BLG-FE-60/86/87/88/BE-26) | EPIC-03 | EPIC-04 must rebase onto main after EPIC-03 merges before finalising backlog.md closures |
| `execution_state.json` | All EPICs | EPIC-01 | Per above ownership rule |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-02 (ST-05 — last_audit_cycle_count schema evolution) | Valid — backward-compatible nullable field; null handling defined in story AC |
| RISK-02 | EPIC-04 (ST-14 — BLG-GOV-67 gate) | Valid — date-based gate (2026-06-21); ST-14 deferred to Sprint 2 pending confirmation |
| RISK-03 | EPIC-01 (ST-01 — prompt_change_log.md entries may already be present) | Valid — ST-01 verifies first; appends only if gaps confirmed; S-effort accommodates both outcomes |

## Pre-Sprint Vulnerability Scan

pip-audit result: **clean** — no known vulnerabilities (58 packages scanned; run 2026-06-03 pre-planning)

## Carry-Forward Items

Carry-forward items reviewed: 4 items from cycle `2026-06-02__release-v4.9`

| # | Item | Disposition |
|---|------|-------------|
| D-1 | Update BLG-GOV-74 Provisional-Target | Closed — confirmed actioned by DL-037 rebalance 2026-06-02 (cycle_summary advisory) |
| D-2 | Verify prompt_change_log.md completeness | Tracked — ST-01 (EPIC-01) addresses this sprint |
| D-3 | Document PO acceptance = GitHub review approval | Tracked — ST-03 (EPIC-01) addresses this sprint |
| D-4 | Monitor spec_references=[] for security audit stories | Open — first occurrence; monitor only; no action required this sprint |

## Delegation Classification Notes

All EPIC-04 autonomous classifications justified:
- ST-10: autonomous with ST-09 dependency. Engine authors Telegram format spec document after ST-09 records PO channel decision. PO + HoST sign-off captured in document sign-off block. Per BLG-GOV-72 conservative classification avoided — spec authoring is within engine scope.
- ST-11/12/13: autonomous — criteria/decisions/assessment documents authored by engine; sign-off blocks capture authority confirmations.

ST-09 classified `delegated_decision`: explicit PO channel choice (Telegram vs in-app) cannot be made by the engine; trade-off analysis produced, decision recorded by PO. LL-v2.2-SP-01 advisory: no HoST design session artefact found for ST-09. A HoST design session or equivalent channel review should be conducted before sprint start.

ST-08 classified `delegated_qa`: story is staging-environment verification only (no code to write); both ACs require human staging run; Infrastructure & Operations Owner must record sign-off.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Design gate bypass fields (`design_gate_bypass_authority`, `design_gate_bypass_reason`) must be populated in `.claude_current_state.json` | Head of UX & Design + Product Owner | Yes — blocks sign-off gate (IMP-04 standard mode) |
| ST-09 (EPIC-04): HoST design session or channel review advisory — no design artefact found for this delegated_decision item | Head of Specs Team | No — advisory only (LL-v2.2-SP-01) |
