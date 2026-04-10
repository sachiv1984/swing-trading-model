**Owner:** PMO Lead
**Class:** Sprint Record (Class 3)
**Status:** Sealed
**Last Updated:** 2026-04-10
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Sprint Close Record — 2026-04-05__release-v2.5

**Date:** 2026-04-10
**Mode:** Standard
**Cycle:** 2026-04-05__release-v2.5
**Release:** v2.5

---

## Sprint Goal

Establish an operational baseline for v2.5 by sealing Sprint 1 governance debt (prompt patches, batch push fix, backlog placement rule) and System Status reliability, then completing backend integration documentation and targeted quick-win features in Sprint 2.

---

## Items Done (13 of 13)

| ST Item | Title | Commit SHA | Spec References | Deviations |
|---------|-------|-----------|-----------------|------------|
| ST-01 | Fix auth forwarding in POST /test/endpoints | 230643b | backend/services/health_service.py, backend/routers/test.py | None (multi-story commit bundled with ST-02 AC items, documented in notes) |
| ST-02 | Sync endpoint test list with openapi.yaml | a6a74c0 | docs/reference/openapi.yaml, backend/services/health_service.py, backend/routers/test.py, src/pages/SystemStatus.js | ST-03 changes bundled in same commit |
| ST-03 | Fix System Status endpoint categorisation for v2.3/v2.4 routes | a6a74c0 | src/pages/SystemStatus.js | Committed under ST-02 commit ID (no independent commit) |
| ST-04 | Review and document Reports page backend integration | 3a645e3 | src/pages/Reports.js, docs/ops/reports_integration_review.md | None |
| ST-05 | Review and document Signals page backend integration | 3a645e3 | src/pages/Signals.js, docs/ops/signals_integration_review.md | Multi-story commit with ST-04 |
| ST-06 | Investigate high external baseline latency on DB-backed endpoints | 3f31b1d | docs/ops/api_performance_baseline.md, claude/cycles/2026-04-05__release-v2.5/delegation_log.md | Initially delegated (DEL-01); completed by Head of Engineering 2026-04-10 |
| ST-07 | Add --max-time to GitHub Actions curl calls | ce3775a | .github/workflows/alert-evaluation.yml, .github/workflows/daily-snapshot.yml | Multi-story commit with ST-08/09 |
| ST-08 | Fix Avg Slippage StatsCard gradient rendering | ce3775a | docs/testing/slippage_scenarios.md | Documentation-only closure; code fix was prior-cycle |
| ST-09 | Fee drag metric on Trade History | ce3775a | docs/specs/metrics_definitions.md, docs/specs/frontend/pages/trade_history.md, docs/specs/api_contracts/trade_endpoints.md, docs/reference/openapi.yaml | DataTable.js TableHead onClick bug found and fixed in staging (e65e023); 3 P3 UX observations filed (BLG-FE-11/12/13) |
| ST-10 | Fix governance_sync.yml batch push issue closure | 01f5e9c | (no prior spec) | Live multi-commit push test not executed in CI this cycle — code review only |
| ST-11 | Formalise backlog entry placement standard | dbb4551 | (pre-met on main) | AC pre-met; no new commit required |
| ST-12 | Apply v2.4 deferred governance prompt patches | 21bb453 | claude/system/execution_prompt.md, claude/system/delivery_verification_prompt.md, claude/system/OPERATIONAL_GUIDE.md, claude/system/prompt_change_log.md | None |
| ST-13 | Create test scenarios for EPIC-01 correctness fixes | aacbb50 | docs/testing/atr_scenarios.md, docs/testing/dedup_scenarios.md, docs/testing/stop_price_scenarios.md | None |

---

## Items Returned to Backlog

None. All 13 planned stories delivered.

---

## Items Delegated and Outstanding

| DEL ID | ST Item | Status at Close |
|--------|---------|----------------|
| DEL-01 | ST-06 | Unblocked — completed 2026-04-10 (commit 3f31b1d) |

All delegated items resolved before sprint close.

---

## QA Evidence Logs Produced

- `claude/cycles/2026-04-05__release-v2.5/qa_evidence_EPIC-01.md` — DoQ 2026-04-10
- `claude/cycles/2026-04-05__release-v2.5/qa_evidence_EPIC-02.md` — DoQ 2026-04-10
- `claude/cycles/2026-04-05__release-v2.5/qa_evidence_EPIC-03.md` — DoQ 2026-04-10 (visual staging sign-off)
- `claude/cycles/2026-04-05__release-v2.5/qa_evidence_EPIC-04.md` — DoQ 2026-04-10

---

## Deviations Filed This Sprint

| Story | Spec File | Deviation / Observation | Priority |
|-------|-----------|------------------------|---------|
| ST-09 | DataTable.js | TableHead dropped onClick — sort broken for all sortable columns (fixed in staging, commit e65e023) | P2 (fixed before close) |
| ST-09 | Trade History page | Card layout squeeze (BLG-FE-11) | P3 UX observation |
| ST-09 | Trade History page | Table header styling (BLG-FE-12) | P3 UX observation |
| ST-09 | Trade History page | Flexible column sorting (BLG-FE-13) | P3 UX observation |
| ST-10 | governance_sync.yml | Live multi-commit batch push test not executed in CI this cycle | P3 observation |
| ST-06 | api_performance_baseline.md | GET /portfolio structural latency (4 sequential connections) — architectural constraint documented, not fixed | P3 (architectural) |
| ST-01/02 | CLAUDE.md | Multi-story commit IDs must all appear — lesson added to CLAUDE.md and lessons_learnt.md | Process observation |

---

## Open Escalations

None.

---

## Net Outcome vs Sprint Goal

**Goal:** Establish an operational baseline for v2.5 by sealing Sprint 1 governance debt and System Status reliability, then completing backend integration documentation and targeted quick-win features.

**Outcome:** Fully achieved.

- Sprint 1 governance debt (CF-2): execution_prompt.md STEP 8 edit check + delivery_verification_prompt.md pre-seal gate applied (ST-12)
- batch push fix: governance_sync.yml updated to process all commits in push range (ST-10)
- Backlog placement standard: formalised and documented (ST-11)
- System Status reliability: auth forwarding fixed (ST-01), 26 endpoints synced (ST-02), categories corrected (ST-03)
- Backend integration docs: Reports page (ST-04), Signals page (ST-05) documented
- Latency investigation: root causes identified, one fix applied, architectural constraints documented (ST-06)
- Quick-win features: --max-time curl flags (ST-07), slippage gradient fix closure (ST-08), Fee Drag % metric end-to-end (ST-09)
- Governance: test scenarios filed for EPIC-01 fixes (ST-13)

**Sprint velocity:** 13/13 (1.00)

---

## Verification Readiness Statement

All spec references populated: Yes
All deviations filed: Yes
QA evidence logs complete: Yes
