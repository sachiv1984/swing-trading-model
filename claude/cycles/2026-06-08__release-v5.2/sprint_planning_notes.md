**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2

---

# Sprint Planning Notes — 2026-06-08__release-v5.2

## Backlog Slice Source

Original — `claude/cycles/2026-06-08__release-v5.2/stage4_backlog_slice.md`

No amendment sealed. `amended_backlog_slice_path` is empty in `.claude_current_state.json`.

## Carry-Forward Items

Carry-forward items reviewed: **2 items** from cycle `2026-06-21__release-v5.1`

| # | Observation | Implication | Engine | Disposition in v5.2 |
|---|-------------|-------------|--------|---------------------|
| 1 | STEP 8.1 Option(b) PO decision creates §-1.2 ambiguity at release planning invocation | Release Planning should accept STEP 8.1 Option(b) metadata as valid §-1.2 gate substitute | Release Planning | RESOLVED by ST-01 (OA-01) in this sprint |
| 2 | Test-authoring stories have spec_references = [] but no current guidance; triggers traceability flag | Sprint Execution should populate spec_references with created test file path for test-authoring stories | Sprint Planning | RESOLVED by ST-02 (OA-02) in this sprint |

## Deferred Items

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| ST-17 (BLG-FE-64) | EPIC-04 | Gate: SI-03 Red Flag Journal live ≥ 30 days — gate clears 2026-06-21; sprint planning seals 2026-06-08 (13 days before gate clear). Per stage4_backlog_slice.md: "If gate not confirmed clear at sprint planning, defer to v5.3." | Yes — v5.3 (gate clears 2026-06-21; confirm at v5.3 sprint planning) |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-08 (BLG-OPS-56 health check) | ST-06 (BLG-BE-33 delivery log) | Logical — best observability with log table | Soft: can proceed using Render logs or Telegram history if ST-06 not complete; document interim procedure |
| ST-12 (endpoint audit) | ST-04 (API contract authoring) | Logical — ST-04 may close one contract gap ST-12 would otherwise flag | Soft: can run in parallel if ST-04 check completes first |
| All EPIC-04 stories | None | Independent of EPIC-02 backend stories | Resolved — EPIC-04 produces planning documents only |
| All EPIC-03 stories | None | Security reviews; no code dependencies | Resolved |
| EPIC-01 prompt patches | No other EPIC in execution | Sequenced last to avoid affecting engine mid-sprint | Resolved |

No circular dependencies identified.

## Execution Sequence

**Merge order: EPIC-03 → EPIC-02 → EPIC-04 → EPIC-01**

### Sprint 1 (single sprint — all EPICs)

**Phase A — EPIC-03 (merge 1st): SI-05 Security Reviews & Endpoint Compliance**
1. ST-09 (BLG-GOV-97) — Claude API model deprecation check (XS; autonomous)
2. ST-10 (BLG-GOV-98) — Telegram bot token security review (S; autonomous)
3. ST-11 (BLG-GOV-99) — SI-05 digest endpoint auth review (S; autonomous/delegated_backend)
4. ST-12 (BLG-GOV-100) — Backend endpoint documentation audit (S; autonomous)

**Phase B — EPIC-02 (merge 2nd): SI-05 Backend Reliability & Operations**
5. ST-05 (BLG-BE-32) — Telegram delivery retry and failure handling (S; delegated_backend)
6. ST-06 (BLG-BE-33) — SI-05 digest delivery log table (S; delegated_backend)
7. ST-07 (BLG-OPS-55) — Deployment runbook update (XS; autonomous)
8. ST-08 (BLG-OPS-56) — Health check procedure (XS; autonomous; logically after ST-06)

**Phase C — EPIC-04 (merge 3rd): SI-05 QA, Verification & Product Governance**
9. ST-13 (BLG-QA-46) — Edge case test gap analysis (XS; autonomous)
10. ST-14 (BLG-QA-47 + BLG-GOV-94) — Acceptance + delivery verification protocols (S; autonomous)
11. ST-15 (BLG-QA-48) — Regression test baseline refresh (XS; autonomous)
12. ST-16 (BLG-GOV-96) — SI-05 effectiveness measurement criteria (S; autonomous)

**Phase D — EPIC-01 (merge last): Governance Prompt Patches & Spec Compliance**
13. ST-01 (OA-01) — release_planning_prompt.md §-1.2 patch (S; autonomous)
14. ST-02 (OA-02) — execution_prompt.md §3.1.A guidance (S; autonomous)
15. ST-03 (BLG-SPEC-47) — SI-05 pass_rate computation alignment (S; autonomous spec + delegated_backend if impl.)
16. ST-04 (BLG-SPEC-48) — POST /digest/si05/send API contract (XS-S; autonomous)

## Multi-EPIC Execution Notes

**execution_state.json owner:** EPIC-03 (first in merge order). EPIC-02, EPIC-04, and EPIC-01 branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

**Shared files across EPICs:**

| File | EPICs touching | Owner EPIC | Advisory |
|------|---------------|------------|---------|
| `docs/reference/openapi.yaml` | EPIC-01 (ST-04), EPIC-02 (ST-06 optional endpoint) | EPIC-03 first; EPIC-02 second | Later EPICs must rebase onto main after EPIC-03 merges before finalising openapi.yaml changes |
| `backend/routers/test.py` | EPIC-01 (ST-04 AC-03), EPIC-02 (ST-06 optional endpoint), EPIC-04 (ST-15) | EPIC-03 first | Later EPICs rebase after earlier EPICs merge |
| `docs/specs/api_contracts/` | EPIC-01 (ST-04), EPIC-03 (ST-12 audit may file new contracts) | EPIC-03 first | EPIC-01 must rebase after EPIC-03 merges |
| `docs/operations/` | EPIC-02 (ST-07, ST-08), EPIC-04 (ST-14 docs/qa/ or docs/operations/) | Separate files; no conflict expected | Confirm path separation at execution |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (prompt patches) | Valid — CLAUDE.md §6 checklist enforced; HoST sign-off required; sequenced last to protect engine |
| RISK-02 | EPIC-02 (ST-06 DB migration) | Valid — IF NOT EXISTS guard required; staging verification per AC-04 (staging-only evidence) |
| RISK-03 | EPIC-03 (ST-11 auth review) | Valid — auth review produces finding document first; if gap found, file P2 item and not blocking EPIC-03 merge; Cybersecurity Lead signs off |
| RISK-04 | EPIC-04 (ST-17 gate) | Closed — ST-17 deferred to v5.3; RISK-04 gate timing risk no longer applies for this sprint |

## Pre-Sprint Vulnerability Scan

pre-sprint pip-audit: **clean** — 0 vulnerabilities across 60 packages (fastapi 0.135.1, starlette 1.0.1, uvicorn 0.24.0, anthropic 0.105.2, and 56 others). No CVEs found. Scan run 2026-06-08.

## Capacity WARN Acknowledgement

**Capacity check outcome:** `warn` (set at release planning)

**Context:** The warn was computed against 17–18 stories including ST-17 conditional, with an earlier capacity estimate of 7–10 days. With ST-17 deferred (16 stories in-scope), estimated effort is ~7.9 days mid-point, within the 12–14 day capacity baseline (workforce_capacity.md, revised 2026-05-27).

**Product Owner acknowledgement:** Capacity WARN acknowledged. 16 stories in-scope at ~7.9 days — under capacity. No scope reduction required. `capacity_warn_acknowledged = true` set in STEP 7 state write.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| delivery_verification_prompt.md v3.0 log entry | PMO Lead | Yes — VERIFIED: confirmed in prompt_change_log.md line 408 (2026-06-21). Advisory cleared. |
| BLG-FE-64 gate confirmation | Product Owner | Yes — RESOLVED: gate not clear at 2026-06-08; ST-17 deferred to v5.3. |
| OA-01 and OA-02 scoped in sprint backlog | PMO Lead | Yes — CONFIRMED: ST-01 (OA-01) and ST-02 (OA-02) in EPIC-01 scope. |

All outstanding actions resolved at planning seal. No remaining blockers.
