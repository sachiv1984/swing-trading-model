**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-18
**Cycle:** 2026-04-17__release-v2.8

---

# Sprint Planning Notes — 2026-04-17__release-v2.8

## Backlog Slice Source

Original — `claude/cycles/2026-04-17__release-v2.8/stage4_backlog_slice.md`

No amended backlog slice (`amended_backlog_slice_path` is empty).

## Carry-Forward Advisory (from v2.7 — cycle 2026-04-13__release-v2.7)

7 carry-forward items reviewed from `lessons_learnt_closure.md`:

| # | Item | Status |
|---|------|--------|
| 1 | DoQ sign-off `Date:` field reminder → `execution_prompt.md §3.2.A` | In scope as ST-04 ✓ |
| 2 | Deviation register terminology → `sprint_close.md` template | In scope as ST-05 ✓ |
| 3 | BLG-GOV-08 engine prompt compression — PO promotion/retire decision | PO decided: defer to v2.9 as final deferral ✓ |
| 4 | AC-6 (ST-08 v2.7): Market Correlation frontend backlog item filed | In scope as EPIC-01 / ST-01 ✓ |
| 5 | BLG-QA-13: scenario coverage for SC-CORR and SC-SIG-IND | In scope as EPIC-02 / ST-02, ST-03 ✓ |
| 6 | Scope document created at planning time (not deferred) | Confirmed fixed: scope doc created at release planning ✓ |
| 7 | Sprint planning should add BLG items to backlog.md at backlog-slice creation time | **Carry-forward note:** PMO Lead to add BLG-FE-14, BLG-QA-13 entries to backlog.md as "Completed" during this sprint (if not already present) |

## Preflight Notes

**stage4_5_capacity_check.md:** Not present — this is a schema v2 cycle; capacity check is embedded in `release_plan.md ## Capacity Check`. Confirmed: `state.json` attributes.capacity_feasible = "pass". No process gap.

**pip-audit (STEP -1.9):** Clean — 0 vulnerabilities found across 60 packages (2026-04-18). Pre-sprint pip-audit: clean.

**Design gate:** Passed (2026-04-17). RISK-01 resolved (Analytics page §18 placement, PO-approved, UX spec produced). RISK-04 clarified: Strategy Rules sign-off deferred to merge-time AC in ST-08 per design gate Outstanding Pre-Sprint Actions.

## Pre-Sprint Required Decisions (STEP -1.10)

| Decision | Status | Notes |
|----------|--------|-------|
| [RISK-01] UX placement for ST-01 (Analytics vs Portfolio page) | **RESOLVED** | Design gate (2026-04-17): Analytics page §18, after §17, PO-approved ✓ |
| [RISK-04] Strategy Rules owner sign-off on AI Journal scope (before sprint planning seal) | **RESOLVED 2026-04-18** | PO confirmed: design gate classification (Strategy Rules sign-off as merge AC in ST-08) satisfies cycle_summary requirement. Merge-AC is a hard blocker — satisfies intent with higher assurance (sign-off against actual implementation). |

## Deferred Items

None — all 8 backlog slice stories included in scope.

## Scope Selection (STEP 3)

All 8 stories classified `include`:

| Story | Classification | Delegation Class | Rationale |
|-------|---------------|-----------------|-----------|
| ST-01 | include | delegated_frontend | New UI section (Analytics §18); UX spec locked; requires visual QA; no pure data-fetch refactor |
| ST-02 | include | autonomous | Test scenario doc authoring; no UI surface; no human decision required |
| ST-03 | include | autonomous | Test scenario doc authoring; no UI surface; no human decision required |
| ST-04 | include | autonomous | Governed prompt patch; well-defined AC; CLAUDE.md §6 checklist enforced by AC |
| ST-05 | include | autonomous | Governance terminology patch; well-defined AC; §6 checklist conditional |
| ST-06 | include | autonomous | Backlog deduplication; scripted file edit; PO confirmation of approach in AC |
| ST-07 | include | autonomous | Backend API endpoint; clear spec; openapi.yaml update in AC; external API key via env var |
| ST-08 | include | delegated_frontend | New UI section (Trade History); Strategy Rules sign-off required before merge |

**Test scenario gap flags (LL-v2.0-P4-2):**
- EPIC-01 (ST-01): New page section on Analytics (§18) — `test_scenarios` flagged as `pending — QA & Testing Owner to author before next sprint on this domain`. Record in execution_state.json.
- EPIC-04 (ST-08): New section on Trade History page — `test_scenarios` flagged as `pending — QA & Testing Owner to author before next sprint on this domain`. Record in execution_state.json.

**Blocked-decision advisory (LL-v2.2-SP-01):** ST-07 and ST-08 are not classified `delegated_decision`. Design artefact present for ST-08 (`docs/design/2026-04-17__release-v2.8/ai-journal-summary/ux_spec.md`). No advisory triggered.

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-08 | ST-07 | Internal (backend endpoint must be live before frontend can consume it) | Resolved — sequential execution order enforced |
| ST-01 | Design gate UX decision (RISK-01) | Design dependency | Resolved — Analytics page §18 confirmed |
| ST-04 | CLAUDE.md §6 checklist | Governance | Resolved — checklist is mandatory per AC |
| ST-05 | Determine target file (execution_prompt.md vs sprint_close.md) | Spec dependency | Resolved during execution — AC covers both cases |
| ST-06 | PO confirmation of deduplication approach | Product decision | To be confirmed at sprint planning sign-off |
| ST-07 | External LLM API key (env var) | External | API key must be set in env before execution |
| All | — | None circular | No circular dependencies detected |

## Execution Sequence

**Sprint 1:**
1. EPIC-03 (ST-04, ST-05, ST-06) — governance hardening, quick wins, can run in any order internally
2. EPIC-02 (ST-02, ST-03) — test scenario coverage, independent, can run in any order internally

*Sprint 1 stories are all independent of each other. Governance patches (EPIC-03) preferred first as they reduce drift risk for execution engine; test scenarios (EPIC-02) follow.*

**Sprint 2:**
3. EPIC-04 / ST-07 — AI Journal backend (implement endpoint, openapi.yaml, deploy)
4. EPIC-04 / ST-08 — AI Journal frontend (depends on ST-07 endpoint live)
5. EPIC-01 / ST-01 — Market Correlation frontend (independent of EPIC-04; can run in parallel with ST-07 if time allows)

*EPIC-04 ST-07 must precede ST-08. EPIC-01 ST-01 is independent and can start Sprint 2 concurrently with ST-07.*

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 / ST-01 | Mitigated — design gate resolved placement; analytics.md v1.7 locked |
| RISK-02 | EPIC-02 / ST-02, ST-03 | Mitigated — analytics_endpoints.md v2.1.0 and signal_endpoints.md v1.1 confirmed from v2.7 |
| RISK-03 | EPIC-03 / ST-04, ST-05, ST-06 | CLAUDE.md §6 checklist mandatory per each story's AC; enforced at execution |
| RISK-04 | EPIC-04 / ST-07, ST-08 | Strategy Rules sign-off is AC in ST-08 (merge pre-condition); external LLM API key via env var; timeout/fallback required in implementation |

## Pre-Sprint Vulnerability Scan

pip-audit (2026-04-18): **clean** — 0 vulnerabilities across 60 packages. No CVEs requiring Product Owner acceptance.

## Outstanding Actions

| Action | Owner | Required Before Seal? | Resolution |
|--------|-------|----------------------|------------|
| PO to confirm: does design gate's classification of RISK-04 (Strategy Rules sign-off as merge AC) satisfy cycle_summary "before sprint planning seal" requirement? | Product Owner | **Yes** | **RESOLVED 2026-04-18** — Confirmed by PO |
| PO to confirm deduplication approach for ST-06: retain most recent entry per duplicated ID; remove earlier copies | Product Owner | Yes (can be confirmed at sprint planning sign-off) | **RESOLVED 2026-04-18** — Confirmed by PO |
| LLM API key to be set in env var before ST-07 execution begins | Head of Engineering | No (pre-execution requirement, not planning seal) |
| PMO Lead: add BLG-FE-14, BLG-QA-13, and other BLG-GOV-13 references to backlog.md as "Completed" during this sprint (carry-forward CF-7) | PMO Lead | No |
| Prompt change log hygiene: no gaps detected across all governed prompts (2026-04-18 scan) | — | Informational — no action required |
