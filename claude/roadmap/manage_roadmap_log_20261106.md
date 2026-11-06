**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-06

# Roadmap Management Run Log — 2026-11-06

Invoked as `post_ship_closure.md` STEP 11 for `2026-11-03__release-v9.15` (not a dry run).

## Summary

Items retired: 1 (the "v9.15 — Site Structure & Usability, Phase 1" Now-horizon section: 10 committed items)
Items flagged stale: 0
Items kept active: all remaining §2/§4+ horizon items (no status change)
Ambiguous items resolved: 0
RA: markers pruned: 1 (`*RA:v9.11-committed-items retired...*` pointer; v9.11 is 4 releases older than v9.15, past the >3 threshold)

## Retired Items

| Item | Status | Cycle | Archive ref |
|------|--------|-------|-------------|
| v9.15 — Committed items (Now horizon): `BLG-FE-244`, `245`, `246`, `247`, `248`, `249`, `266`, `BLG-SPEC-214`, `215`, `216` | Complete (verification report `claude/cycles/2026-11-03__release-v9.15/verification_report.md`, PO acceptance §9, 2026-11-06) | 2026-11-03__release-v9.15 | roadmap_archive.md 2026-11-06 |

**Programme plan carry-forward (STEP 5.2, BLG-GOV-406):** the retired section's "Programme plan" table has unshipped phases (Phase 2 v9.16, Phase 3 v9.17, close-out v9.18). It was moved to `current_roadmap.md` §3 `### Programme plan — Site Structure & Usability (DL-088)`, with Phase 1 marked ✅ v9.15, keeping the DL-088 reference. It retires when the close-out (`BLG-UX-08`) ships.

**RA:v9.15 execution notes:** moved from §3 to §1 above RA:v9.14, matching the placement of the RA:v9.10–v9.14 blocks.

**`initiative_register.md` (STEP 5.4):** no row exists for these items. They are backlog items committed by DL-088, not initiatives, and the register has had 0 active initiatives since 2026-04-03. Gap recorded; no write.

## Stale Items Flagged

None.

## Ambiguous Items

None.

## Write Scope Verification

- All writes within Section 5 scope: Yes (`current_roadmap.md`, `roadmap_archive.md`, this log; `.claude_current_state.json` Phase 1M fields at post-ship STEP 10)
- No content changes beyond status and location: Yes (the programme plan table moved verbatim, except the Phase 1 row marked shipped)
- No backlog modifications: Yes

**§5.5 Governance version-table audit:** not due (1st `manage roadmap` invocation since the marker `2026-10-29__release-v9.14`; due at the 3rd). The post-ship STEP 8 governance-drift run this session was clean anyway: 28 tracked files, OPERATIONAL_GUIDE.md self-consistent at 4.253.
