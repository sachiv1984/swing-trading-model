# Backlog Health Report — 2026-04-10

**Run:** GROOM-20260410-01 (post-ship closure, inline — 2026-04-05__release-v2.5)
**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Complete

---

## 1. Run Summary

| Metric | Result |
|--------|--------|
| Run trigger | Post-ship closure — v2.5 shipped 2026-04-10 |
| Items in backlog (before archive) | 37 |
| Items archived (v2.5 shipped) | 12 |
| Items retained (active) | 25 |
| New items added since last groom | 0 (all Phase 4 additions already present) |
| Stale provisional targets updated | 10 (v2.5 → v2.6) |
| Orphan items detected | 0 |
| Stale blockers detected | 0 |
| ID uniqueness — active backlog | PASS (25 unique IDs, no duplicates) |
| ID uniqueness — archive | FAIL — 26 unique IDs with duplicate entries (pre-existing; see §4) |

---

## 2. Archived Items (v2.5 Post-Ship)

| ID | Title | Shipped cycle |
|----|-------|---------------|
| BLG-OPS-11 | Add `--max-time` to GitHub Actions cron curl calls | 2026-04-05__release-v2.5 |
| BLG-OPS-12 | Fix System Status auth header — include API key in health probe | 2026-04-05__release-v2.5 |
| BLG-OPS-13 | Investigate high external baseline latency on DB-backed endpoints | 2026-04-05__release-v2.5 |
| BLG-FE-07 | Fix System Status endpoint categorisation for v2.3/v2.4 routes | 2026-04-05__release-v2.5 |
| BLG-FE-08 | Fix Avg Slippage StatsCard gradient rendering | 2026-04-05__release-v2.5 |
| BLG-FEAT-15 | Fee drag metric on Trade History | 2026-04-05__release-v2.5 |
| BLG-GOV-10 | Fix governance_sync.yml batch push issue closure | 2026-04-05__release-v2.5 |
| BLG-GOV-12 | Formalise backlog entry placement standard | 2026-04-05__release-v2.5 |
| TEST-GAP-EPIC-01-v24 | Create test scenarios for EPIC-01 backend correctness fixes | 2026-04-05__release-v2.5 |
| BLG-BE-08 | Review and document Reports page backend integration | 2026-04-05__release-v2.5 |
| BLG-BE-09 | Review and document Signals page backend integration | 2026-04-05__release-v2.5 |
| BLG-BE-07 | Investigate high external baseline latency on DB-backed endpoints | 2026-04-05__release-v2.5 |

*Full archive entries in `claude/backlog/backlog_archive.md` — v2.5 Release Slice section.*

---

## 3. Active Backlog — 25 Items

### By Section

| Section | Count | Items |
|---------|-------|-------|
| §1 Platform & Validation | 1 | BLG-TECH-05 |
| §2 Product Feature | 0 | — |
| §3 Frontend & UX | 5 | BLG-FE-09, BLG-FE-10, BLG-FE-11, BLG-FE-12, BLG-FE-13 |
| §4 Backend & Data | 3 | BLG-BE-08-GAP-01, BLG-BE-09-GAP-01, BLG-BE-09-GAP-02 |
| §5 QA & Test Automation | 5 | BLG-QA-07, BLG-QA-08, BLG-QA-09, BLG-QA-10, BLG-QA-11 |
| §6 Operations | 0 | — |
| §7 Spec Debt | 1 | BLG-SPEC-D17 |
| §8 Governance | 3 | BLG-GOV-08, BLG-GOV-11, BLG-GOV-14 |
| §13 (2026-03-31 session) | 1 | BLG-FEAT-13 |
| §15 (2026-04-03 session) | 2 | BLG-OPS-14, BLG-BE-07-FIX |
| §16 (2026-04-04 session) | 4 | BLG-GOV-13, BLG-FEAT-16, BLG-BE-10, BLG-FEAT-17 |

### By Priority

| Priority | Count | Items |
|----------|-------|-------|
| P0 — Critical | 0 | — |
| P1 — High | 4 | BLG-BE-08-GAP-01, BLG-BE-09-GAP-01, BLG-QA-09, BLG-OPS-14 |
| P2 — Medium | 4 | BLG-BE-09-GAP-02, BLG-QA-07, BLG-QA-08, BLG-BE-07-FIX |
| P3 — Low | 17 | All remaining |

---

## 4. ID Uniqueness Scan

### Active backlog
- **Result: PASS** — 25 unique IDs; no duplicates detected in active backlog.

### Archive (`backlog_archive.md`)
- **Result: FAIL** — 26 unique IDs have duplicate entries.
- **Root cause:** Pre-existing condition; first flagged in GROOM-20260404-01 (v2.4 closure). The v2.5 archiving added 8 items that already had prior archive entries (BLG-FE-07, BLG-FE-08, BLG-FEAT-15, BLG-GOV-10, BLG-GOV-12, BLG-BE-07, BLG-BE-08, BLG-BE-09 plus BLG-OPS-11 from prior archiving), contributing to the pre-existing duplicate count.
- **Outstanding action:** BLG-GOV-13 (P3) — Product Owner confirmation required before deduplication proceeds.
- **No new unique-ID duplicates introduced in active backlog by this run.**

---

## 5. Stale Provisional Targets

10 items had `Provisional-Target: v2.5` while v2.5 has now shipped. Updated to v2.6 in this run:

BLG-TECH-05, BLG-FE-09, BLG-SPEC-D17, BLG-GOV-08, BLG-GOV-11, BLG-GOV-14, BLG-FEAT-13, BLG-GOV-13, BLG-FEAT-16, BLG-BE-10, BLG-FEAT-17

> Note: BLG-TECH-05's `v2.5 (or when system becomes multi-user)` notation also updated to `v2.6 (or when system becomes multi-user)`.

---

## 6. Orphan Check

No orphan items detected. All active items have:
- Valid owner field
- Valid source field referencing a known event, story, or session
- Provisional-Target pointing to v2.6 or open-ended qualifier

---

## 7. Stale Blockers

No stale blockers detected. No active items have hard blocking dependencies on unresolved v2.5 items.

BLG-BE-07-FIX depends on BLG-OPS-14 (sequencing recommendation, not a hard block) — both active.
BLG-QA-10 soft-depends on BLG-QA-09 — both active.

---

## 8. Promotion Candidates

None identified. All P1 items already have appropriate priority designations.

---

## 9. Outstanding Actions from This Run

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| OA-1 | Product Owner to confirm deduplication approach for `backlog_archive.md` (50+ duplicate entries) — required before BLG-GOV-13 can proceed | Product Owner | P3 |
| OA-2 | Next groom backlog run to validate ID uniqueness PASS after BLG-GOV-13 deduplication | PMO Lead | P3 |

---

*Prior groom: GROOM-20260404-01 (v2.4 post-ship closure)*
*Next scheduled groom: v2.6 post-ship closure or roadmap rebalance*
