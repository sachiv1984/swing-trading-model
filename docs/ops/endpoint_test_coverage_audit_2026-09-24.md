**Owner:** QA & Testing Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-24
**Cycle:** 2026-09-23__release-v9.7 (ST-16 — BLG-QA-175)

---

# Endpoint Test Suite Coverage Audit — Recurring Pre-Sprint Run

## Purpose

Establishes a **recurring** cadence for the coverage audit first performed as a one-off deep pass at `docs/ops/endpoint_test_coverage_audit_2026-07-29.md` (ST-11, BLG-QA-133, v7.10). That prior audit fixed 7 gaps and documented the exclusion set, but nothing re-ran it proactively before this story — a gap introduced since then would only be caught reactively (e.g. `BLG-OPS-156`, a same-class gap this cycle caught at post-ship closure instead of before sprint scope sealed).

## Method

Run `python3 scripts/audit_endpoint_test_coverage.py` (unchanged from the 2026-07-29 audit's tooling — no new script needed, this story establishes the *cadence*, not new detection logic). The script:
1. AST-adjacent regex-scans every `@router.get/post/put/delete/patch(...)` decorator across `backend/routers/*.py`, applying each file's `APIRouter(prefix=...)`.
2. Cross-references against `backend/routers/test.py`'s `test_cases` list `"name": "METHOD /path"` entries.
3. Excludes the documented `KNOWN_GAPS` set (real-data-mutating endpoints deliberately never smoke-tested, per `test.py`'s own disposition comment block).
4. Reports any route present in (1) but absent from both (2) and (3) as an undocumented gap.

**Recurring cadence (this story's own scope):** run this script at the start of every sprint's execution (`run sprint` STEP 0, alongside the existing test-scenario discovery step), or at minimum once per cycle before sprint scope seals. Any gap found is filed as its own backlog item (`BLG-QA-*`, Owner: QA & Testing Owner) — see Disposition below for this run's own result.

## First Run Result (2026-09-24)

```
Scanned 92 route decorator(s) across 26 router file(s).
8 route(s) are documented KNOWN_GAPS (deliberate exclusions, see test.py disposition comment).
No undocumented gaps -- every route is either registered or a documented, deliberate exclusion.
```

## Disposition

**0 undocumented gaps found.** No backlog item filed this run — the prior audit's fixes and exclusion documentation remain complete and in sync with the current router set (92 routes today vs 128 at the 2026-07-29 audit's own count basis, reflecting different scan scope — this run's script version scans `backend/routers/*.py` only, not `backend/main.py`'s own `@app.*` decorators, which the original one-off deep audit additionally covered; scanning `main.py`'s decorators too is out of this story's S-effort scope and is noted here as a candidate refinement for a future cadence run rather than expanded into this one).

This result satisfies this story's AC: "First run completed; any gap found filed as its own item" — none was found to file.

## Sign-off

- Reviewed against `stage4_backlog_slice.md#ST-16`'s acceptance criteria: audit method documented (above, and cross-referenced from the 2026-07-29 audit doc); first run completed (above); no gap found, so nothing to file.
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-09-24
