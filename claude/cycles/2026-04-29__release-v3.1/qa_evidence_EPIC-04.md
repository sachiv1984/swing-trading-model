**Owner:** Director of Quality
**Class:** Execution Artefact (Class 3)
**Status:** Signed Off
**Cycle:** 2026-04-29__release-v3.1
**EPIC:** EPIC-04 — Operations, Governance & Quick Wins
**Branch:** exec/2026-04-29__release-v3.1/EPIC-04
**Last Updated:** 2026-04-30

---

# QA Evidence Log — EPIC-04

## Sprint 1 Stories

### ST-11 — Monthly P&L summary report

**Classification:** autonomous
**GitHub Issue:** #319

**Acceptance Criteria Verification:**

| AC | Description | Status | Evidence Method |
|----|-------------|--------|-----------------|
| AC-1 | `GET /reports/monthly-pnl` endpoint returns `[{ year, month, realised_pnl_gbp, trade_count }]` sorted descending | Pass | Code review — `backend/main.py` endpoint + `backend/database.py` `get_monthly_pnl()` SQL with `ORDER BY year DESC, month DESC` |
| AC-2 | Endpoint registered in `backend/routers/test.py`; `openapi.yaml` updated; `reports_endpoints.md` v0.4 updated | Pass | Code review — test.py entry for `GET /reports/monthly-pnl` (total 36); openapi.yaml `/reports/monthly-pnl` path block added; reports_endpoints.md bumped v0.3→v0.4 |
| AC-3 | Frontend: monthly breakdown table displayed in financial reporting section, consistent with existing P&L formatting | Pass | Code review — `src/pages/Reports.js` `MonthlyPnlTable` component added with emerald/rose colouring consistent with existing P&L formatting; third tab "Monthly P&L" added |
| AC-4 | No regression to annual tax-year P&L report | Pass | Code review — tax-year endpoint and component untouched; new endpoint is additive |

**Frontend AC note:** AC-3 (UI table rendering, tab switching, colour) verified by code review. Local run not available in this execution environment. AC remains subject to post-merge staging verification per DoQ standing instruction.

**Deviations:** None.

---

### ST-12 — External API security policy docs & dependency risk register

**Classification:** autonomous
**GitHub Issue:** #320

**Acceptance Criteria Verification:**

| AC | Description | Status | Evidence Method |
|----|-------------|--------|-----------------|
| AC-1 | `docs/ops/alpaca_key_rotation_policy.md` created with rotation schedule, trigger conditions, step-by-step procedure, Cybersecurity & Trust Lead acceptance | Pass | Code review — file created with 90-day schedule, trigger conditions (compromise, offboarding, Render breach), 5-step procedure referencing Render env vars; accepted by Cybersecurity & Trust Lead 2026-04-30 |
| AC-2 | `docs/ops/external_api_credential_inventory.md` created with Alpaca + News API entries; no sensitive values; Cybersecurity & Trust Lead acceptance | Pass | Code review — file created with both credential entries, metadata only (no key values), security note explicitly warning against storing values; accepted by Cybersecurity & Trust Lead 2026-04-30 |
| AC-3 | `docs/ops/external_api_dependency_register.md` created with failure modes (Alpaca null bars, hyphenated tickers), mitigations, monitoring; PMO Lead acceptance | Pass | Code review — file created with AFM-01 (null bars, v3.0 incident), AFM-02 (hyphenated tickers), AFM-03 (rate limiting) plus mitigations MIT-01/02/03; News API NFM-01/02/03 with mitigations; monitoring approach documented; accepted by PMO Lead 2026-04-30 |

**Deviations:** None.

---

### ST-13 — Execution prompt patch CF-01 (reclassification backfill instruction)

**Classification:** autonomous
**GitHub Issue:** #321

**Acceptance Criteria Verification:**

| AC | Description | Status | Evidence Method |
|----|-------------|--------|-----------------|
| AC-1 | `execution_prompt.md` §3.1.A updated with reclassification backfill instruction | Pass | Code review — instruction added after Pre-met path in §3.1.A: "If a story is reclassified from `delegated_frontend` to `autonomous` mid-sprint, the accepting engine must backfill `test_scenarios` in `execution_state.json` at the time of reclassification." |
| AC-2 | `execution_prompt.md` version bumped (v3.11→v3.12) | Pass | Code review — header version updated to v3.12; changelog entry v3.12 appended |
| AC-3 | `OPERATIONAL_GUIDE.md` §8 source prompt header and §14 entry updated | Pass | Code review — OPERATIONAL_GUIDE v3.64→v3.65; §8 updated to v3.12; §14 Execution Engine Source updated to v3.12 |
| AC-4 | `prompt_change_log.md` entry appended | Pass | Code review — row appended: `2026-04-30 \| execution_prompt.md \| v3.11→v3.12 \| ST-13 (CF-01) + ST-14 (CF-02) combined \| Head of Specs Team` |
| AC-5 | All 4 §6 checklist steps verified complete | Pass | Code review — all 4 steps completed in single commit (version bump + OPERATIONAL_GUIDE §8/§14 + prompt_change_log) |

**Deviations:** ST-13 and ST-14 committed together per sprint notes instruction ("Can combine with ST-14 into single version bump").

---

### ST-14 — Execution prompt patch CF-02 (output target clarification)

**Classification:** autonomous
**GitHub Issue:** #322

**Acceptance Criteria Verification:**

| AC | Description | Status | Evidence Method |
|----|-------------|--------|-----------------|
| AC-1 | `execution_prompt.md` §5.4 updated with output target note (lessons_learnt_cycle.md, not lessons_learnt.md) | Pass | Code review — note added in §5.4 after Output path line: "Output target (CF-02): Output target is `lessons_learnt_cycle.md` — do NOT append to `lessons_learnt.md` (that is the Release Planning artefact)..." |
| AC-2 | Version bumped (combined with ST-13 into single v3.11→v3.12 bump) | Pass | Code review — single version bump per sprint notes intent |
| AC-3 | `OPERATIONAL_GUIDE.md` and `prompt_change_log.md` updated (combined with ST-13) | Pass | Code review — same commit as ST-13 updates covers both |
| AC-4 | All 4 §6 checklist steps verified complete | Pass | Combined with ST-13 — all steps satisfied |

**Deviations:** Combined with ST-13 into single commit per sprint backlog notes.

---

## Consolidation

| Story | Classification | Sprint | AC Status | Deviations |
|-------|---------------|--------|-----------|------------|
| ST-11 | autonomous | 1 | All Pass | None |
| ST-12 | autonomous | 1 | All Pass | None |
| ST-13 | autonomous | 1 | All Pass | None (combined with ST-14) |
| ST-14 | autonomous | 1 | All Pass | None (combined with ST-13) |

**Overall EPIC-04 status: Pass**

---

## Sign-off

**Verification method:** Code review for all backend and governance stories. ST-11 frontend component verified by code review; post-merge staging verification recommended for AC-3 visual rendering.

**Director of Quality sign-off:** Granted — 2026-04-30

All EPIC-04 stories meet their acceptance criteria. No blocking deviations. EPIC-04 ready for PR and merge.
