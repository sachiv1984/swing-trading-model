**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-18
**Cycle:** 2026-05-18__release-v3.7

---

# Sprint Planning Notes — 2026-05-18__release-v3.7

## Backlog Slice Source

Original — `claude/cycles/2026-05-18__release-v3.7/stage4_backlog_slice.md`

No amended_backlog_slice_path set in `.claude_current_state.json`.

---

## Carry-Forward Items

From `cycle_summary.md` (prior cycle `lessons_learnt_closure.md` absent for 2026-05-16__release-v3.6 — no formal carry-forward section; carry-forward sourced from cycle_summary.md).

| # | Item | Source | Resolution |
|---|------|--------|------------|
| 1 | deviations_filed recurrence (LL-v3.6 item 1) — sub-step 10a atomic write | cycle_summary.md carry-forward | ST-07 delivers this fix; Execution Engine should use updated execution_prompt.md from Sprint 1 onwards |
| 2 | BLG-GOV-19 autonomous class (LL-v3.6 item 2) — observable AC flag | cycle_summary.md carry-forward | ST-08 delivers qa_evidence_template.md patch; flag BLG-GOV-19 class eligibility during execution |

---

## Capacity WARN Acknowledgement

**Outcome:** WARN — total in-scope effort (~8.5 days) exceeds single sprint capacity (~5 days).

**Product Owner acknowledgement (2026-05-18):** Over-capacity risk accepted. Proposed phasing — EPIC-04 (1.5 days) → EPIC-03 (1 day) → EPIC-01 (6 days) — accepted. Execution is sequential per merge order; wall-clock completion will span more than one sprint cadence.

**EPIC-02 gate decision (2026-05-18):** Product Owner confirmed < 20 closed trades. EPIC-02 (ST-04/ST-05/ST-06) deferred to v3.8. Sprint scope reduces to 8 stories across EPIC-04/03/01 — total ~8.5 days.

---

## Pre-Sprint Required Decisions

| Decision | Status | Owner | Resolution |
|----------|--------|-------|------------|
| RISK-01: PT-04 gate — confirm ≥ 20 closed trades | Resolved | Product Owner | DECLINED — < 20 closed trades confirmed 2026-05-18. EPIC-02 deferred to v3.8. |

---

## Deferred Items

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| ST-04 — PT-04 spec authoring + gate confirmation | EPIC-02 | EPIC-02 gate not met (< 20 closed trades) | Yes — v3.8 if gate met |
| ST-05 — PT-04 backend: quality score endpoint | EPIC-02 | EPIC-02 gate not met | Yes — v3.8 if gate met |
| ST-06 — PT-04 frontend: quality score display | EPIC-02 | EPIC-02 gate not met | Yes — v3.8 if gate met |

---

## Delegation Class Assignments

| Story | Backlog Slice Class | Sprint Planning Class | Rationale |
|-------|--------------------|-----------------------|-----------|
| ST-01 | autonomous | autonomous | Backend only — DB column, endpoint, spec update |
| ST-02 | standard | delegated_frontend | New user-facing control (Add to Watchlist CTA replaces Add Position). Playwright coverage included in AC. Per LL-v1.10-P3-3: not a "no UX change" refactor. |
| ST-03 | standard | delegated_frontend | New read-only Signal Context panel in trade plan form. Playwright coverage included in AC. |
| ST-07 | autonomous | autonomous | Governance doc patches — no UI change |
| ST-08 | autonomous | autonomous | Template update — no UI change |
| ST-09 | autonomous | autonomous | Test infrastructure refactor — no UI change |
| ST-10 | autonomous (BLG-OPS-16) / delegated_decision (BLG-FE-35) | delegated_decision | BLG-FE-35 requires HoUX staging run; story is composite — overall class = delegated_decision |
| ST-11 | delegated_decision | delegated_decision | Facilitator must perform scored_initiatives.md refresh |

**LL-v2.0-P4-2 note (delegated_frontend items):** ST-02 and ST-03 introduce new user-facing controls. Playwright scenarios are included as explicit ACs in the backlog slice — test_scenarios confirmed. No separate `test_scenarios = pending` flag required.

**LL-v2.2-SP-01 advisory:**
- ST-10 (BLG-FE-35): No pre-existing HoST design session artefact — the staging run itself is the artefact. Advisory noted; no blocker.
- ST-11: Facilitator task with no UX design artefact required. Advisory: Facilitator should schedule the scored_initiatives.md refresh session before sprint execution begins.

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal (EPIC-01) | Resolved — sequential within EPIC-01 |
| ST-03 | ST-01, ST-02 | Internal (EPIC-01) | Resolved — sequential; ST-03 starts after ST-02 merged |
| ST-07 | None | — | Independent |
| ST-08 | None | — | Independent |
| ST-09 | None | — | Independent |
| ST-10 | None | — | Independent |
| ST-11 | None | — | Independent |
| EPIC-03 | EPIC-04 merged | Cross-EPIC | EPIC-04 must merge before EPIC-03 branch rebases |
| EPIC-01 | EPIC-03 merged | Cross-EPIC | EPIC-03 must merge before EPIC-01 branch rebases |

---

## Execution Sequence

**Merge order:** EPIC-04 → EPIC-03 → EPIC-01

1. **EPIC-04** (execution_state.json owner)
   - ST-09 — Database stub conftest consolidation (autonomous)
   - ST-10 — Pycache hygiene + Research page font staging (delegated_decision)
   - ST-11 — scored_initiatives.md refresh (delegated_decision)
2. **EPIC-03** (rebases onto main after EPIC-04 merges)
   - ST-07 — execution_prompt.md patches ×3 (autonomous)
   - ST-08 — qa_evidence_template.md BLG-GOV-19 fail-path (autonomous)
3. **EPIC-01** (rebases onto main after EPIC-03 merges)
   - ST-01 — Signals backend: watchlisted status (autonomous)
   - ST-02 — Signals frontend: Add to Watchlist CTA (delegated_frontend)
   - ST-03 — Trade plan form: signal context panel (delegated_frontend)

---

## Multi-EPIC Execution Notes

**execution_state.json owner:** EPIC-04 (first in execution order). EPIC-03 and EPIC-01 branches must check for `claude/cycles/2026-05-18__release-v3.7/execution_state.json` existence before creating their own section — if found, read and append; do not overwrite.

**Shared files across EPICs:**

| File | Modified by | Owner | Advisory |
|------|-------------|-------|---------|
| `claude/system/execution_prompt.md` | EPIC-03 (ST-07) | EPIC-03 | No other EPIC modifies this file |
| `claude/system/prompt_change_log.md` | EPIC-03 (ST-07) | EPIC-03 | No other EPIC modifies this file |
| `docs/reference/openapi.yaml` | EPIC-01 (ST-01) | EPIC-01 | No other EPIC modifies this file |
| `backend/routers/test.py` | EPIC-01 (ST-01), EPIC-04 (ST-09 — conftest) | EPIC-04 (conftest changes) / EPIC-01 (new route test) | EPIC-01 must rebase onto `origin/main` after EPIC-04 merges before finalising test.py |
| `data_model.md` | EPIC-01 (ST-01 — signals table schema) | EPIC-01 | No other EPIC modifies this file |

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status | Notes |
|---------|----------------|------------------|-------|
| RISK-01 | EPIC-02 | Resolved — EPIC-02 deferred to v3.8 | Gate not met; no execution risk |
| RISK-02 | EPIC-01 (ST-03 depends on ST-01+ST-02) | Valid | Sequential dependency within EPIC-01 enforced in execution sequence |
| RISK-03 | EPIC-03 (prompt change log gaps) | Valid | Retroactive entries are advisory-only; ST-07 includes retroactive additions |

---

## Pre-Sprint Vulnerability Scan

pip-audit result: **clean** — 0 vulnerabilities in `backend/requirements.txt` (scanned 2026-05-18).

---

## Prompt Change Log Gap Advisory (STEP -1.7)

⚠️ The following prompts have version gaps not yet recorded in `claude/system/prompt_change_log.md`:

| Prompt | Current Version | Last Logged Version | Gap |
|--------|----------------|--------------------|----|
| `execution_prompt.md` | v3.23 | v3.21→v3.22 | v3.22→v3.23 missing |
| `delivery_verification_prompt.md` | v2.3 | v2.1→v2.2 | v2.2→v2.3 missing |
| `post_ship_closure.md` | v2.9 | v2.7→v2.8 | v2.8→v2.9 missing |
| `release_planning_prompt.md` | v2.29 | v2.27→v2.28 | v2.28→v2.29 missing |

ST-07 (EPIC-03) includes retroactive prompt_change_log.md entries — these additional gaps should be captured as part of ST-07 delivery or in a subsequent governance patch. Advisory only — does not block sprint planning seal.

---

## AC Format Advisory

Acceptance criteria in `stage4_backlog_slice.md` are written in narrative/bullet form rather than the explicit §7 structured table (Technical/Quality/Security/Verification). In standard mode: content covers all four required dimensions; Director of Quality confirmed sufficient for QA sign-off production. Advisory recorded; no blocker.

---

## Outstanding Actions

| Action | Owner | Blocker? |
|--------|-------|---------|
| Capture prompt_change_log.md gaps (v3.22→v3.23, v2.2→v2.3, v2.8→v2.9, v2.28→v2.29) | Head of Specs Team | No — advisory; ST-07 addresses related entries |
| Facilitator to schedule scored_initiatives.md refresh session before ST-11 execution | Facilitator | No — advisory |
