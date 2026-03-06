**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-06

---

# Backlog Health Report — 2026-03-06

## Summary

```
Total items reviewed:           39
Complete — Archive:              8
Killed — Archive:                0
Active — Keep:                  31
Orphans already flagged:         2  (BLG-FEAT-03, TEST-GAP-EPIC-06 — flags confirmed, no new action)
Blocked — stale blocker:         0
Spec debt resolved this run:     2  (BLG-SPEC-D2, BLG-SPEC-D7)
Spec debt still open:           10  (D1, D3, D4, D8, D9, G1, G2, G3, G4, G5)
Priority misalignments flagged:  3
Promotion candidates:            6
Ambiguous items resolved:        0
```

---

## Archived Items

| Item ID | Title | Priority | Shipped | Evidence |
|---------|-------|----------|---------|----------|
| BLG-SPEC-D2 | settings_endpoints.md spec/implementation mismatch | P1 | v1.8 | ST-09, 2026-03-04__release-v1.8 |
| BLG-SPEC-D7 | openapi.yaml frozen at v1.8.1 | P2 | v1.8 | ST-10, 2026-03-04__release-v1.8 |
| BLG-NEW-01 | Golden Output Regression Baseline for CI | P1 | v1.8 | ST-05, 2026-03-04__release-v1.8 |
| BLG-NEW-02 | Backtest vs Live Stop Reconciliation Report | P1 | v1.8 | ST-06, 2026-03-04__release-v1.8 |
| BLG-NEW-03 | Define and Document Unavailability Failure Mode | P1 | v1.8 | ST-11, 2026-03-04__release-v1.8 |
| BLG-NEW-05 | Dependency Vulnerability Scanning in CI | P1 | v1.8 | ST-07, 2026-03-04__release-v1.8 |
| BLG-NEW-07 | Running API Changelog Document | P1 | v1.8 | ST-12, 2026-03-04__release-v1.8 |
| BLG-NEW-08 | Automated OpenAPI Drift Detection in CI | P1 | v1.8 | ST-08, 2026-03-04__release-v1.8 |

---

## Promotion Candidates

Advisory only. Release planning engine assigns v1.9 backlog slice.

| Item ID | Title | Priority | Why | Target | Pre-work |
|---------|-------|----------|-----|--------|----------|
| BLG-NEW-09 | R-Multiple Distribution Report | P2 | v1.9 analytics candidate; extends §3.1 | v1.9 | BLG-FEAT-08 must precede (Metrics owner constraint) |
| BLG-NEW-10 | Canonical Test Scenario Library | P1 | Directly resolves TEST-GAP-EPIC-01 | v1.9 | BLG-NEW-01 ✅ complete |
| BLG-NEW-11 | Canonical Terms Glossary | P2 | Low-risk governance; Head of Specs Team | v1.9 | None |
| BLG-NEW-12 | Service Layer Test Coverage Standard | P1 | BLG-NEW-01 prerequisite complete | v1.9 | BLG-NEW-01 ✅ complete |
| BLG-SPEC-G1 | settings_model.md missing | P2 | 3 cycles open; v1.9 spec authoring pre-work | v1.9 | BLG-SPEC-D2 ✅ archived |
| BLG-SPEC-G2 | Error Response Standard | P2 | 3 cycles open; v1.9 spec authoring pre-work | v1.9 | None |

---

## Priority Alignment Notes

No priority changes applied — advisory only. Product Owner to review at v1.9 pre-alignment.

| Item | Current Priority | Flag |
|------|-----------------|------|
| BLG-FEAT-08 | P2 | Hard pre-work gate for 5.1 (v1.9 roadmap). Consider P1 upgrade — if definitions are not complete, 5.1 cannot enter sprint. |
| BLG-SPEC-G1 | P2 | Open since 2026-02-21 (3 cycles). Cycle summary flags for P1 escalation ahead of v1.9 spec authoring. |
| BLG-SPEC-G2 | P2 | Open since 2026-02-21 (3 cycles). Cycle summary flags for P1 escalation ahead of v1.9 spec authoring. |

---

## Orphans Flagged

No new orphans flagged. Two existing orphan notices confirmed:

| Item ID | Title | Last activity | Flag status |
|---------|-------|--------------|-------------|
| BLG-FEAT-03 | Slippage Tracking | None on record | Existing notice confirmed |
| TEST-GAP-EPIC-06 | v1.7 test coverage gap (no BLG-ID) | None on record | Existing notice confirmed |

---

## Spec Debt Status

| Item ID | Spec | Status | Action taken |
|---------|------|--------|-------------|
| BLG-SPEC-D2 | settings_endpoints.md | ✅ Resolved | Archived (ST-09, v1.8) |
| BLG-SPEC-D7 | openapi.yaml | ✅ Resolved | Archived (ST-10, v1.8) |
| BLG-SPEC-D1 | api_contracts/README.md | Open | No change |
| BLG-SPEC-D3 | market_endpoints.md (missing) | Open | No change |
| BLG-SPEC-D4 | GET /positions/search/tags | Open | No change |
| BLG-SPEC-D8 | System_status_report.md header | Open | No change |
| BLG-SPEC-D9 | process_index.md wrong path | Open | No change |
| BLG-SPEC-G1 | settings_model.md (missing) | Open — 3 cycles | Priority flag raised |
| BLG-SPEC-G2 | Error Response Standard (missing) | Open — 3 cycles | Priority flag raised |
| BLG-SPEC-G3 | logging_standards not in Specs_Index | Open | No change |
| BLG-SPEC-G4 | ADR-002 wrong location | Open | No change |
| BLG-SPEC-G5 | validation_system.md owner field | Open | No change |

---

## Items Requiring Product Owner Decision

1. **BLG-FEAT-08 priority** — currently P2, but is a hard pre-work gate for 5.1 (v1.9). Recommend confirming P1 or P2 at v1.9 pre-alignment before sprint planning opens.
2. **BLG-SPEC-G1 and BLG-SPEC-G2** — open 3 cycles. Cycle summary (2026-03-06__item-3.4) recommended escalating to P1 ahead of v1.9 spec authoring. Product Owner to confirm at v1.9 pre-alignment.
3. **TEST-GAP-EPIC-06** — no BLG-ID assigned. Cycle summary (2026-03-06__item-3.4) flagged: "assign a BLG-ID and roadmap home at next Roadmap Rebalance, or close if addressed." No action taken this run.

---

## Write Scope Verification

- All writes within §5 scope: Yes
- No roadmap document modified: Yes
- No item definitions changed (status and flags only): Yes
- Archive is append-only: Yes
