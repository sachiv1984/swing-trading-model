**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-11
**Cycle:** 2026-04-11__release-v2.6

# Sprint Planning Notes — 2026-04-11__release-v2.6

---

## Backlog Slice Source

Original — `claude/cycles/2026-04-11__release-v2.6/stage4_backlog_slice.md`
No amendment in effect (`amended_backlog_slice_path` is empty).

---

## Carry-Forward Items (v2.5)

Source: `claude/cycles/2026-04-05__release-v2.5/lessons_learnt_closure.md ## Carry-Forward` — 3 items

| # | Item | In-Scope Resolution |
|---|------|-------------------|
| 1 | execution_prompt.md STEP 5.1 unpushed-commit check | ST-12 (EPIC-04, Sprint 2) ✅ |
| 2 | Prompt log hygiene §6 edit reminders for 3 engines | ST-13 (EPIC-04, Sprint 2) ✅ |
| 3 | execution_state.json test_scenarios schema clarification | Deferred to v2.7 (noted in cycle_summary.md) |

---

## Pre-Sprint Required Decisions (from cycle_summary.md)

All 3 decisions listed resolved before sprint seal — design gate completed 2026-04-11.

| Decision | Status | Evidence |
|----------|--------|---------|
| Trade History StatsCard bar layout spec (ST-09) | ✅ Resolved | `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md` |
| Trade History column header styling spec (ST-10) | ✅ Resolved | `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md` |
| Trade History flexible column sorting strategy (ST-11) | ✅ Resolved | `docs/design/2026-04-11__release-v2.6/trade-history-ux/ux_spec.md` |

---

## Pre-Sprint Vulnerability Scan

`pip-audit -r backend/requirements.txt` run 2026-04-11: **CLEAN** — no CVEs found.

---

## Prompt Change Log Hygiene Advisory (STEP -1.11)

Advisory scan performed for planning-cycle relevant prompts:
- `sprint_planning_prompt.md`: current v2.5 = last logged v2.5 ✅
- `design_gate_prompt.md`: current v1.1 = last logged v1.1 ✅

No gaps detected for prompts directly involved in this planning cycle. Full scan of all governed prompts: advisory only — does not block planning.

---

## Deferred Items

None. All 15 items from `stage4_backlog_slice.md` are included in this sprint.

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-05 Phase B | ST-04 | Internal — ST-04 must fix collection errors before ST-05 Phase B test runner is expanded | Managed in execution sequence |
| ST-09, ST-10, ST-11 | Design artefact | Design gate | Resolved — `ux_spec.md` approved 2026-04-11 |
| All others | None | — | — |

---

## Execution Sequence

### Sprint 1 — EPIC-01 and EPIC-02

Recommended sequence:

1. **ST-04** — Fix Pytest Collection Errors (prerequisite for ST-05 Phase B; also unblocks ST-06 and ST-07 CI integration)
2. **ST-05** — Add CI Test Runner Workflow (Phase A can run immediately; Phase B after ST-04)
3. **ST-07** — Fee Drag Backend Pytest Unit Tests (run after collection errors resolved for clean CI validation)
4. **ST-01** — Migrate Reports Performance Tab to FastAPI (can proceed in parallel with EPIC-02 above)
5. **ST-02** — Wire Signals Dismissal and Position Creation to FastAPI (after ST-01 validates integration pattern)
6. **ST-03** — Replace Base44 Cash Balance on Signals Page (XS, can proceed in any order)
7. **ST-06** — Fee Drag Playwright Spec (can run after collection errors resolved; independent of backend migration)

### Sprint 2 — EPIC-03 and EPIC-04

Recommended sequence:

1. **ST-08** — StatsCard Tooltip Prop (foundational component change; unlocks ST-09 Avg Fee Drag tooltip wiring)
2. **ST-09** — Trade History StatsCard Bar Layout (after ST-08 for Avg Fee Drag tooltip)
3. **ST-10** — Trade History Column Header Styling (independent; can run in parallel with ST-09)
4. **ST-11** — Flexible Column Sorting (requires existing sort infrastructure; independent otherwise)
5. **ST-12** — execution_prompt.md STEP 5.1 Unpushed-Commit Check (governance-only; any order)
6. **ST-13** — Prompt Log Hygiene §6 Reminders (governance-only; any order; implements §6 reminder in 3 engines)
7. **ST-14** — Upgrade decision_log.md Hard Gate (governance-only; any order)
8. **ST-15** — Frontend Performance Budget Spec (documentation-only; any order)

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | Valid — Base44 divergence documented in GAP files; ST-01/ST-02 AC include integration review |
| RISK-02 | ST-05 (EPIC-02) | Valid — Phase A CI starts minimal (no DATABASE_URL secret); Phase B gated on ST-04 |
| RISK-03 | EPIC-03 | Resolved — design gate cleared 2026-04-11; `trade_history.md` v1.6 locked |
| RISK-04 | ST-13 (EPIC-04) | Valid — CLAUDE.md §6 checklist will be applied at execution; commit-check skill available |

---

## Acceptance Criteria Notes

All 15 items have technical AC defined in `stage4_backlog_slice.md`. The Section 7 4-field structure (Technical/Quality/Security/Verification) is partially implicit:

- **Security**: N/A for all items in this sprint — no new security surfaces created. No authentication changes, no new API endpoints exposed externally, no PII handling changes.
- **Quality**: Embedded in technical AC (test file existence, test pass criteria). Playwright and pytest items have explicit pass criteria.
- **Verification**: Director of Quality to confirm per standard process from `qa_evidence_EPIC-xx.md` at sprint close.

No `[AC REQUIRED]` placeholders. No items blocked at seal.

---

## Outstanding Actions

None. All pre-sprint decisions resolved. No blockers at planning seal.
