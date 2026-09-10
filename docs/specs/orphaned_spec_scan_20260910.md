**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-09-10
**Source:** ST-17 (BLG-SPEC-70, EPIC-04, v9.3 sprint execution)

---

# Orphaned Spec Scan — 2026-09-10

## Purpose

ST-17's acceptance criteria: run `scripts/check_orphaned_specs.py` once against `docs/specs/**` (133 files at time of this scan); any orphaned specs found are triaged (kept, merged, or archived) by Head of Specs Team within the sprint (RISK-04); unresolved individual specs filed as follow-on `BLG-SPEC-*` items rather than blocking this story's closure.

## Method

`scripts/check_orphaned_specs.py` flags a `docs/specs/**/*.md` file as orphaned when its basename appears nowhere else — not in `claude/backlog/backlog.md`/`backlog_archive.md`, and not in any other tracked repo file (`.py`, `.js`, `.jsx`, `.md`, `.yml`, `.yaml`, vendored directories excluded). A file's own self-mention (e.g. its filename in its own header) does not count. 10 unit tests (`tests/test_check_orphaned_specs.py`) verify the detector genuinely catches an unreferenced fixture file, not just that it passes on well-referenced ones, including a "deliberately orphaned" case per this codebase's established `test_lint_api_contract_headings.py`-style precedent.

## Result

**0 orphaned specs found.** Every one of the 133 files under `docs/specs/` is referenced by at least one backlog item or another repo file.

Since no orphans were found, **no triage was required** — RISK-04's triage/follow-on-filing step is conditional on orphans existing, and none do.

## Known Limitation (disclosed, not blocking)

The detector matches by **basename only**, not full path. 2 basename pairs are duplicated across different directories in `docs/specs/`:

| Basename | Locations |
|----------|-----------|
| `README.md` | `docs/specs/frontend/README.md`, `docs/specs/api_contracts/README.md` |
| `red_flag_journal.md` | `docs/specs/frontend/pages/red_flag_journal.md`, `docs/specs/api_contracts/red_flag_journal.md` |

For a duplicated basename, a reference to *either* file clears *both* from being flagged — the detector cannot currently distinguish "spec A of this name is referenced" from "spec B of this name is referenced" when they share a filename. This is a genuine blind spot, not fixed in this story: full path-aware matching would need to handle the common real-world pattern of specs being cross-referenced by bare filename without a directory prefix (observed throughout this codebase, e.g. `` `research_endpoint.md` `` cited without `docs/specs/api_contracts/`), which is a larger disambiguation problem than this `M`-effort (~2 day) story's scope. Manually spot-checked: both `README.md` files are directory-index files (a low-risk category — directory READMEs are conventionally discovered via their containing directory, not required to be individually cross-referenced), and both `red_flag_journal.md` files are independently live, actively-referenced specs (frontend page spec and API contract respectively) — neither pair shows any sign of being a genuine orphan masked by its duplicate. Filed as **BLG-SPEC-140** for a future path-aware iteration of the linter, not treated as a live finding requiring triage now.

## Acceptance

- Run by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — a detection script run + result documentation, no observable UI behaviour). No delegated_decision escalation to Head of Specs Team was raised, since 0 orphans means RISK-04's triage step has nothing to act on.
- Date: 2026-09-10
