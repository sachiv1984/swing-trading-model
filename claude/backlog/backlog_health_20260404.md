**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-04

# Backlog Health Report — 2026-04-04

## Summary

```
Backlog Health Summary — 2026-04-04

Total items reviewed: 29
Complete — Archive: 13
Killed — Archive: 0
Active — Keep: 16
Orphans flagged: 0
Blocked — stale blocker flagged: 0
Spec debt items — resolved: 2 (BLG-SPEC-D15, BLG-SPEC-D16)
Spec debt items — still open: 0
Priority misalignments flagged: 0
Promotion candidates: 4 (advisory only)
Ambiguous items resolved: 0
ID uniqueness: FAIL — 50 pre-existing duplicate ### headers in backlog_archive.md (pre-dates this run; no new duplicates introduced by this archiving run)
```

---

## Items Archived (13)

| ID | Title | Type | Shipped | Evidence |
|----|-------|------|---------|----------|
| BLG-BE-05 | Fix ATR pence→GBP conversion for all UK (.L) tickers | Backend Bug Fix | v2.4 (ST-01) | changelog.md v2.4 |
| BLG-BE-06 | Alert evaluation idempotency | Backend Engineering | v2.4 (ST-02) | changelog.md v2.4 |
| BLG-BE-04 | R-Multiple stop price unavailable from trade_history | Backend / Data | v2.4 (ST-03) | changelog.md v2.4 |
| BLG-FE-06 | Fix missing P&L (GBP) column on Positions page | Frontend / UX | v2.4 (ST-04) | changelog.md v2.4 |
| BLG-FE-03 | User-facing error message mapping layer | Frontend / UX | v2.4 (ST-05) | changelog.md v2.4 |
| BLG-SPEC-D15 | Reconcile data_model.md portfolios table | Spec Debt | v2.4 (ST-06) | changelog.md v2.4 |
| BLG-SPEC-D16 | Reconcile data_model.md trade_history table | Spec Debt | v2.4 (ST-07) | changelog.md v2.4 |
| BLG-FEAT-14 | Weekly trading review digest | Product Feature | v2.4 (ST-08+09) | changelog.md v2.4 |
| BLG-OPS-10 | Render hosting tier review | Operational | v2.4 (ST-10) | changelog.md v2.4 |
| BLG-OPS-05 | API endpoint performance baseline | Operational | v2.4 (ST-11) | changelog.md v2.4 |
| TEST-GAP-EPIC-05-SLIP | Create slippage tracking test scenarios | QA Coverage | v2.4 (ST-12) | changelog.md v2.4 |
| BLG-GOV-09 | Cycle velocity metric | Governance | v2.4 (ST-13) | changelog.md v2.4 |
| BLG-GOV-03 | Simplify cycle artefact sealing | Governance | v2.4 (ST-17) | changelog.md v2.4 |

---

## Active Items (16)

| ID | Title | Priority | Target |
|----|-------|----------|--------|
| BLG-TECH-05 | Prometheus metrics endpoint | P3 | v2.4+ (conditional) |
| BLG-FE-07 | Fix System Status endpoint categorisation | P4 | v2.5 |
| BLG-FE-08 | Fix Avg Slippage StatsCard gradient rendering | P3 | v2.5 |
| BLG-GOV-08 | Engine prompt compression (roadmap_prompt, release_planning_prompt) | P3 | v2.5 |
| BLG-GOV-10 | Fix governance_sync.yml batch push issue | P2 | v2.5 |
| BLG-GOV-11 | Cycle artefact inventory and maintenance review | P3 | v2.5 |
| BLG-GOV-12 | Formalise backlog entry placement standard | P2 | v2.5 |
| BLG-OPS-11 | Add --max-time to GitHub Actions cron curl calls | P3 | v2.5 |
| BLG-OPS-12 | Fix auth forwarding in POST /test/endpoints | P2 | v2.5 |
| BLG-OPS-13 | Keep endpoint test list in sync with openapi.yaml | P3 | v2.5 |
| BLG-BE-07 | Investigate high external baseline latency on DB-backed endpoints | P2 | v2.5 |
| BLG-BE-08 | Review and document Reports page backend integration | P2 | v2.5 |
| BLG-BE-09 | Review and document Signals page backend integration | P2 | v2.5 |
| BLG-FEAT-13 | Add gated feature rollout capability | P3 | v2.5 |
| BLG-FEAT-15 | Fee drag metric on Trade History | P3 | v2.5 |
| TEST-GAP-EPIC-01-v24 | Create test scenarios for EPIC-01 backend correctness fixes | P2 | v2.5 |

---

## Promotion Candidates (advisory — Product Owner decision required)

| ID | Title | Priority | Why Promote | Pre-work |
|----|-------|----------|-------------|----------|
| BLG-OPS-12 | Fix auth forwarding in POST /test/endpoints | P2 | XS effort; makes System Status page reliable; no dependencies | None |
| BLG-GOV-10 | Fix governance_sync.yml batch push | P2 | XS effort; recurring manual work to close issues; no dependencies | None |
| TEST-GAP-EPIC-01-v24 | EPIC-01 backend correctness test scenarios | P2 | Correctness-critical coverage gap; S effort; no dependencies | None |
| BLG-FEAT-15 | Fee drag metric on Trade History | P3 | Well-specified; no data model changes needed; S effort | trade_history.md spec update required in same cycle |

---

## Duplicate IDs in backlog_archive.md

**Status: FAIL — pre-existing, not introduced this run.**

50 duplicate `###` item headers detected in `backlog_archive.md`. These are pre-existing from prior groom backlog cycles (items archived multiple times across separate grooming passes). None of the 13 items archived in this run are duplicated.

**Required action:** Product Owner to confirm whether duplicates should be deduplicated (retain most recent entry) or left as historical record. Do not archive further copies of any duplicated ID without Product Owner confirmation. Tracked as outstanding action.

Duplicate IDs (representative sample): BLG-API-01, BLG-BE-02, BLG-FEAT-01 through BLG-FEAT-08, BLG-GOV-01, BLG-GOV-02, BLG-NEW-01 through BLG-NEW-12, BLG-OPS-01, BLG-RD-01 through BLG-RD-11, BLG-SPEC-D1 through BLG-SPEC-D9, BLG-SPEC-G1 through BLG-SPEC-G5, BLG-TECH-01, BLG-TECH-04, BLG-TECH-06, TEST-GAP-EPIC-01, TEST-GAP-EPIC-02.

---

## Priority Alignment Notes

All 16 active items have Provisional-Target v2.5. No misalignments with the current roadmap (v2.5 planning not yet started). No priority anomalies detected.

---

## Orphan Detection

No orphans. All active items have Provisional-Target and named owners.

---

## Stale Blockers

None. No items have stated blockers that are unresolved or stale.
