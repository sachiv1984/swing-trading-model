**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-23
**Cycle:** 2026-05-22__release-v4.0

---

# Sprint Planning Notes — 2026-05-22__release-v4.0

## Backlog Slice Source

Amended — `claude/cycles/2026-05-22__release-v4.0/amendments/AMD-20260523-01/amended_backlog_slice.md`

Original `stage4_backlog_slice.md` superseded by AMD-20260523-01 (ratified 2026-05-23). Two additions: ST-12 (BLG-BE-19 Gemini wiring, EPIC-03) and ST-13 (starlette CVE fix, EPIC-02).

## Deferred Items

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| ST-10 | EPIC-04 | PT-04 gate not met — <20 closed trades confirmed by PO | Yes — re-evaluate at v4.1 planning |
| ST-11 | EPIC-04 | PT-04 gate not met — same gate condition as ST-10 | Yes — re-evaluate at v4.1 planning |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-07 | ST-12 | Internal (EPIC-03) | Resolved — ST-12 sequenced first in EPIC-03 |
| ST-08 | ST-12 | Internal (EPIC-03) | Resolved — ST-12 sequenced first in EPIC-03 |
| ST-03 | SI-01 shipped (v3.8) + SI-03 shipped (v3.9) | External (prior releases) | Resolved — both shipped |
| ST-02 | ST-01 (optional) | Advisory — ST-02 frontend can proceed independently; ST-01 backend endpoint provides the data source | Independent |
| ST-04 | None | — | Independent |
| ST-09 | None (independent of ST-07/ST-08) | — | Independent within EPIC-03 |
| ST-13 | None | — | Independent |

## Execution Sequence

### Sprint 1

1. EPIC-01: ST-01 → ST-02 → ST-04 → ST-03 (analytics foundation; ST-03 E2E test last to cover full pipeline)
2. EPIC-02: ST-13 → ST-05 → ST-06 (security patch first, then validation, then review)

Merge order Sprint 1: **EPIC-01 → EPIC-02**

### Sprint 2

3. EPIC-03: ST-12 → ST-07 → ST-08 → ST-09 (Gemini wiring first; then audit; then cost tracking; CI/CD independent but last)

Merge order Sprint 2: **EPIC-03**

## Multi-EPIC Execution Notes

- **execution_state.json owner:** EPIC-01 (first in execution order)
- EPIC-02 and EPIC-03 must check for `execution_state.json` existence before creating their own; if found, append their EPIC section rather than overwrite
- Shared files requiring ownership discipline:

| File | Owner EPIC | Subsequent EPICs must rebase |
|------|-----------|------------------------------|
| `docs/reference/openapi.yaml` | EPIC-01 | EPIC-02, EPIC-03 must rebase onto main after EPIC-01 merges |
| `backend/routers/test.py` | EPIC-01 | EPIC-02, EPIC-03 must rebase |
| `src/pages/SystemStatus.js` (test count) | EPIC-01 | EPIC-02, EPIC-03 must update count |

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-04 | Resolved — gate not met; EPIC-04 deferred at planning |
| RISK-02 | EPIC-01 ST-01 | Resolved — metric definition confirmed by Metrics & Analytics Owner 2026-05-23: `validation_pass_rate_by_rule = pass_count / (pass_count + fail_count) per rule_type, rolling 7d/30d configurable` |
| RISK-03 | EPIC-03 ST-09 | Open — OPS-27 build-minute impact assessment still needed before ST-09 implementation begins; PO to confirm acceptable free-tier impact during Sprint 2 execution |

## Pre-Sprint Vulnerability Scan

**pip-audit result (2026-05-23):** 1 finding — starlette v0.49.1, PYSEC-2026-161 (medium — URL reconstruction auth bypass). Fix: upgrade to ≥1.0.1. Addressed: ST-13 added via AMD-20260523-01. Risk accepted by PO + DoQ.

All other dependencies: clean. No additional CVEs requiring sprint action.

## Carry-Forward Items

All carry-forward items from v3.9 were applied before v4.0 execution begins (confirmed in cycle_summary.md). No carry-forward items requiring sprint-planning action.

## Capacity WARN Acknowledgement

Capacity WARN acknowledged by Product Owner (2026-05-23). Firm sprint scope (~13 days) slightly exceeds solo-dev 2-sprint capacity (~10 days). Risk accepted because:
1. BLG-BE-19 effort was implicit in original EPIC-03 estimates (already required for delivery)
2. Sprint 1 stories include 2 XS items (ST-06, ST-13) which will execute quickly
3. If Sprint 1 runs long, EPIC-03 Sprint 2 stories can slip to v4.1 without blocking Sprint 1 deliverables
`capacity_warn_acknowledged = true` written to state.

## Pre-Sprint Backlog Advisory

No items with `Provisional-Target: Before v4.0 sprint planning` found in backlog.md.

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| RISK-03 OPS-27 build-minute impact assessment | Infrastructure Owner | No — Sprint 2 pre-work; required before ST-09 implementation |
| BLG-SPEC-33 + BLG-SPEC-34 backlog archive (noted in cycle_summary OA-4) | PMO Lead | No — next groom backlog run |
| Verify prompt_change_log entries for sprint_planning_prompt v3.4→v3.6 and execution_prompt v3.26→v3.27 | Head of Specs Team | No — hygiene advisory |
