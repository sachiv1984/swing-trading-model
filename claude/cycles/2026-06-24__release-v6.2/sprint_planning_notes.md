**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-24
**Cycle:** 2026-06-24__release-v6.2

---

# Sprint Planning Notes — 2026-06-24__release-v6.2

---

## Backlog Slice Source

Original — `claude/cycles/2026-06-24__release-v6.2/stage4_backlog_slice.md`

No amendment file present (`amended_backlog_slice_path` is empty in `.claude_current_state.json`).

---

## Carry-Forward Items

Carry-forward items reviewed: 5 items from cycle `2026-06-22__release-v6.1`.

| # | Item | Status in v6.2 |
|---|------|----------------|
| 1 | BLG-GOV-135 — execution_prompt autonomous class hard gate | In scope as ST-10 (EPIC-03) ✅ |
| 2 | BLG-GOV-136 — execution_prompt test_scenarios path validation | In scope as ST-11 (EPIC-03) ✅ |
| 3 | BLG-OPS-75 — api_performance_baseline.md 2 new v6.1 endpoints | In scope as ST-12 (EPIC-03) ✅ |
| 4 | BLG-QA-61 — signals_scenarios.md review vs ST-01 sizing model changes | **Not in v6.2 scope** — advisory: review during EPIC-01 ST-03/04 execution to ensure signal scenario coverage remains accurate after inv-vol sizing changes |
| 5 | BLG-QA-62 — Playwright spec auto-registration via glob pattern | In scope as ST-13 (EPIC-03) ✅ |

Advisory on BLG-QA-61: The v6.2 inv-vol sizing changes (ST-04) affect signal entry calculations. The execution team should cross-check `tests/` signal scenario coverage against the new sizing model during ST-04 execution to confirm no scenario gaps. No new backlog item required if coverage is confirmed adequate.

---

## Capacity WARN Acknowledgement

Release planning recorded capacity_check = `warn` (12.5 days total vs single-sprint baseline). With the 2-sprint phasing plan (Sprint 1: ~8.5 days, Sprint 2: ~4 days), per-sprint effort is within the 12–14 day/sprint capacity baseline. The 2-sprint plan resolves the WARN.

Product Owner acknowledgement: [AWAITING SIGN-OFF] (captured in sprint_backlog.md PO sign-off block)

---

## Pre-Sprint Vulnerability Scan

pip-audit unavailable — `requirements.txt` not found or pip-audit not installed. Recommend running `pip-audit -r backend/requirements.txt` before sprint execution begins to confirm clean dependency state.

---

## Deferred Items

No items deferred from the authoritative backlog slice. All 13 stories are included in the sprint plan:
- Sprint 1: ST-01 through ST-05 (EPIC-01) + ST-10 through ST-13 (EPIC-03)
- Sprint 2: ST-06 through ST-09 (EPIC-02) — conditional on §13 review

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | No items deferred | — |

Note: BLG-QA-61 is not in any EPIC of this sprint (see Carry-Forward advisory above).

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal (EPIC-01) — `current_trailing_stop` field must be available from backend | Resolved — sequence ST-01 before ST-02 |
| ST-06 | ST-01, ST-03, ST-05 | Cross-sprint (EPIC-01→EPIC-02) — trailing stop data, rebalance exit signals, risk-off alerts must be live | Resolved — EPIC-02 in Sprint 2 after EPIC-01 verified |
| ST-07 | ST-06 | Internal (EPIC-02) — AI daily briefing endpoint required | Resolved — sequence ST-06 before ST-07 |
| ST-08 | ST-06 | Internal (EPIC-02) — shared context assembly pattern from ST-06 | Resolved — sequence ST-06 before ST-08 |
| ST-09 | ST-08 | Internal (EPIC-02) — POST /ai/chat endpoint required | Resolved — sequence ST-08 before ST-09 |
| ST-11 | ST-10 (advisory) | Internal (EPIC-03) — ST-11 may batch with ST-10; not a hard dependency | Advisory — can commit together |

Independent items (no blocking dependencies): ST-01, ST-03, ST-04, ST-05, ST-10, ST-12, ST-13

---

## Execution Sequence

### Sprint 1

**Phase A — Autonomous governance patches (EPIC-03):**
1. ST-10 + ST-11 (batch commit — both autonomous, < 0.5 day total; execution_prompt.md patches)
2. ST-12 (autonomous — api_performance_baseline.md update)
3. ST-13 (delegated_qa — Playwright yml glob pattern; no dependencies)

**Phase B — Strategy parity backend (EPIC-01, parallel with Phase A where possible):**
4. ST-01 (delegated_backend — independent; establishes `current_trailing_stop` field)
5. ST-03 (delegated_backend — independent; month-end rebalance logic)
6. ST-04 (delegated_backend — independent; inv-vol sizing replaces signal entry path)
7. ST-05 (delegated_backend — independent; risk-off nightly check)

**Phase C — Frontend (EPIC-01, after Phase B backend):**
8. ST-02 (delegated_frontend — after ST-01 complete; trailing stop display + breach badge)

### Sprint 2 (after Sprint 1 verified)

**Phase D — AI backend (EPIC-02):**
9. ST-06 (delegated_backend — after ST-01, ST-03, ST-05 live)
10. ST-08 (delegated_backend — after ST-06; shares context assembly pattern)

**Phase E — AI frontend (EPIC-02):**
11. ST-07 (delegated_frontend — after ST-06; daily briefing card)
12. ST-09 (delegated_frontend — after ST-08; chat widget)

---

## Multi-EPIC Execution Notes

**Sprints 1 has 2 EPICs (EPIC-01 and EPIC-03). Merge order and execution_state.json ownership:**

- **execution_state.json owner: EPIC-01** (primary Sprint 1 EPIC — largest scope, owns API and database changes)
- EPIC-03 must check for `execution_state.json` existence before creating its own copy; if found (EPIC-01 created it first), append EPIC-03's section rather than overwrite
- EPIC-01 should initialise `execution_state.json` on its first commit

**Sprint 1 merge order: EPIC-03 → EPIC-01**
- EPIC-03 is autonomous-class and faster to complete; merge first to clean main before EPIC-01 PR opens
- EPIC-01 must verify no merge conflicts with EPIC-03 changes before finalising its PR (EPIC-03 touches governance files only — no overlap with EPIC-01 backend/frontend)

**Sprint 2 merge order: EPIC-02** (after Sprint 1 fully merged)
- EPIC-02 branch must rebase onto `main` after EPIC-01 + EPIC-03 merge before finalising implementation
- ST-06 context assembly reads from EPIC-01's new data fields (`current_trailing_stop`, `exit_rebalance` signals, `risk_off_exit` alerts) — confirm these are live in staging before ST-06 backend implementation

**Shared files across EPICs:**
- `docs/reference/openapi.yaml`: EPIC-01 adds `current_trailing_stop` to GET /positions response schema; EPIC-02 adds POST /ai/daily-briefing and POST /ai/chat. No Sprint 1 conflict. EPIC-02 must rebase to include EPIC-01's openapi additions before adding its own.
- `docs/specs/api_contracts/`: EPIC-01 and EPIC-02 will each add contract entries. Same rebase advisory applies.
- `backend/routers/`: EPIC-01 may extend existing router(s); EPIC-02 adds new routers. Low conflict risk but EPIC-02 must rebase.
- EPIC-03 governance files (`execution_prompt.md`, `OPERATIONAL_GUIDE.md`, `prompt_change_log.md`) are not modified by EPIC-01 or EPIC-02.

---

## Test Scenario Gap Advisories (LL-v2.0-P4-2)

The following `delegated_frontend` stories introduce new user-facing controls and require test scenario authoring:

| Story | New UI Element | Advisory |
|-------|---------------|----------|
| ST-02 | Trailing stop column + breach badge (Positions page) | `test_scenarios` for EPIC-01 = "pending — QA & Testing Owner to author Playwright specs for trailing stop display and breach badge before next sprint on this domain" |
| ST-07 | AI Daily Briefing card (Dashboard page) | `test_scenarios` for EPIC-02 = "pending — QA & Testing Owner to author Playwright specs for briefing card before next sprint on this domain" |
| ST-09 | AI chat widget (Positions page) | `test_scenarios` for EPIC-02 = "pending — QA & Testing Owner to author Playwright specs for chat widget before next sprint on this domain" |

Note: Playwright ACs for all three stories are defined in the backlog slice and will be implemented as part of the frontend delegation. The above advisory applies to any additional scenario coverage beyond what's captured in the ACs.

---

## Design Gate Notes Carry-Forward (from design_gate.md)

The following implementation advisories were recorded by the Head of UX & Design at the design gate:

1. **ST-03 — `stop_exit` signal type badge (conditional):** Implementation team must confirm `stop_exit` is a live API value returned by `GET /signals` before applying the red badge. If not yet a live signal type, the red badge is deferred. This is a pre-check, not a gate blocker.

2. **ST-09 — Signals page placement (stretch goal):** ST-09 canonical target is the **Positions page**. Signals page placement is a capacity-dependent stretch goal — do not treat as in-scope unless explicitly capacity-confirmed at sprint execution. If deferred, file a follow-on backlog item.

3. **ST-02 — Table column density:** If layout testing reveals excessive horizontal scroll with ~15 columns, Initial Stop + Trail Stop may be combined into a two-line cell without a spec amendment — this is an implementation-level layout decision within the spec's intent.

---

## Risk Flags

| Risk ID | Associated Items | Mitigation Status | Notes |
|---------|-----------------|------------------|-------|
| RISK-01 | EPIC-02 (ST-06–09) | **Open — OA (Blocker? Yes)** | §13 compliance review for BLG-FEAT-50/51 not yet recorded. Sprint planning seal blocked until completed by Strategy Rules & System Intent Owner. |
| RISK-02 | Release-level | **Mitigated** | 2-sprint plan confirmed; per-sprint effort within 12–14d capacity. |
| RISK-03 | ST-04 (EPIC-01) | **Mitigated — monitor at execution** | Inv-vol sizing replaces core signal entry sizing path. Regression test required: manual sizing path must remain unchanged (ST-04 AC-04). Execution team must confirm existing sizing unit tests pass. |

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| §13 compliance review for BLG-FEAT-50 (AI daily briefing) and BLG-FEAT-51 (AI chat advisor) — confirm advisory-only, no automated execution; record in `docs/product/decisions/decisions--2026-06-24__release-v6.2.md` | Strategy Rules & System Intent Owner | **Yes** |
| Product Owner sprint goal sign-off (Sprint 1 + Sprint 2 goals) | Product Owner | **Yes** |
| Product Owner capacity WARN acknowledgement (2-sprint plan) | Product Owner | **Yes** |
| Run pip-audit before sprint execution begins | Head of Engineering | No (advisory) |
