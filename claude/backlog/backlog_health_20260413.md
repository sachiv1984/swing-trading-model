**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-04-13
**Run ID:** GROOM-20260413-01

---

# Backlog Health Report — 2026-04-13

**Trigger:** Post-ship closure STEP 12 (2026-04-11__release-v2.6)
**Mode:** Standard

---

## Backlog Health Summary

```
Backlog Health Summary — 2026-04-13

Total items reviewed: ~38 (including section markers and release slice entries)
Complete — Archive: 13
Killed — Archive: 0
Active — Keep: 25
Orphans flagged: 0
Blocked — stale blocker flagged: 0
Spec debt items — resolved: 0 (BLG-SPEC-D17 still open)
Spec debt items — still open: 1 (BLG-SPEC-D17)
Priority misalignments flagged: 0
Promotion candidates: 0 (advisory — none meet threshold)
Ambiguous items resolved: 0
Stale provisional targets updated: 13 (11 open items + BLG-TECH-05 + BLG-GOV-08)
Duplicate IDs flagged: 1 (BLG-QA-11 — see §Flags)
```

---

## Items Archived (13)

| ID | Title | Cycle | ST |
|----|-------|-------|----|
| BLG-BE-08-GAP-01 | Migrate Reports Performance tab to FastAPI backend | 2026-04-11__release-v2.6 | ST-01 |
| BLG-BE-09-GAP-01 | Wire Signals page dismissal and position creation to FastAPI | 2026-04-11__release-v2.6 | ST-02 |
| BLG-BE-09-GAP-02 | Replace Base44 cash balance on Signals page with GET /cash/summary | 2026-04-11__release-v2.6 | ST-03 |
| BLG-QA-09 | Fix 4 pytest collection errors | 2026-04-11__release-v2.6 | ST-04 |
| BLG-QA-10 | Add CI test runner workflow | 2026-04-11__release-v2.6 | ST-05 |
| BLG-QA-07 | Fee drag Playwright spec | 2026-04-11__release-v2.6 | ST-06 |
| BLG-QA-08 | Pytest unit tests for fee drag backend logic | 2026-04-11__release-v2.6 | ST-07 |
| BLG-FE-10 | Add tooltip prop to StatsCard component | 2026-04-11__release-v2.6 | ST-08 |
| BLG-FE-11 | Trade History StatsCard bar layout | 2026-04-11__release-v2.6 | ST-09 |
| BLG-FE-12 | Trade History column header styling | 2026-04-11__release-v2.6 | ST-10 |
| BLG-FE-13 | Flexible column sorting | 2026-04-11__release-v2.6 | ST-11 |
| BLG-GOV-15 | Upgrade decision_log.md append-only rule to hard gate | 2026-04-11__release-v2.6 | ST-14 |
| BLG-FE-09 | Define Frontend Performance Budget | 2026-04-11__release-v2.6 | ST-15 |

---

## Active Items Retained (25)

BLG-TECH-05, BLG-QA-11 (×2 — duplicate ID flag below), BLG-SPEC-D17, BLG-GOV-08, BLG-GOV-11, BLG-GOV-14, BLG-GOV-17, BLG-GOV-18, BLG-GOV-19, BLG-FEAT-13, BLG-OPS-14, BLG-BE-07-FIX, BLG-GOV-13, BLG-FEAT-16, BLG-BE-10, BLG-FEAT-17, BLG-GOV-16, BLG-QA-11 (Playwright intercept — line 933).

---

## Stale Provisional Targets Updated

13 items had `Provisional-Target: v2.6` — all updated to `v2.7` (items not shipped in v2.6).

---

## ID Uniqueness Scan

**Active backlog:** Two entries with ID `BLG-QA-11`:
1. "System Status Playwright spec (endpoint list sync + category routing)" — original item
2. "Fix Playwright page.route() intercepts not firing" — filed during v2.6 deviation recording

**Status:** FAIL — duplicate ID in active backlog. Pre-existing conflict not introduced this cycle. Outstanding action OA-5 in closure_record.md requires PMO Lead to assign BLG-QA-12 to the System Status spec item and update references.

**Archive uniqueness:** Not re-scanned this run (pre-existing FAIL for archive noted in prior groom backlog runs).

---

## Promotion Shortlist

None — no items meet the promotion threshold at this time (all high-priority items already targeted for v2.7; no unplaced P1 items).

---

## Changes Made

| File | Action | Detail |
|------|--------|--------|
| `claude/backlog/backlog.md` | Archived 13 COMPLETE items | Replaced with comment markers |
| `claude/backlog/backlog.md` | Updated 13 stale provisional targets | v2.6 → v2.7 |
| `claude/backlog/backlog.md` | Updated Last Updated header | 2026-04-13 |
| `claude/backlog/backlog_archive.md` | Appended v2.6 release slice entry | 13 items in table |
| `claude/backlog/backlog_archive.md` | Updated Last Updated header | 2026-04-13 |
