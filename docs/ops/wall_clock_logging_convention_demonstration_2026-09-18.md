**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-09-18

# Wall-Clock Cost Logging Convention — Live Demonstration (ST-32, BLG-GOV-316)

## Purpose

`shared_standards.md` §22 (Governance-Cycle Wall-Clock Cost Logging Convention) defines the `Session start (UTC)` / `Session end (UTC)` pair but, before this story, no governed routine's own STEP list explicitly instructed capturing them — `ST-32`'s STEP-list wiring landed in `roadmap_prompt.md` v9.22 (STEP 1.1 / STEP 12.1), since that engine already creates a `run_manifest.md` at a clean STEP 0-equivalent boundary and closes at a clean, unambiguous final STEP. `roadmap_prompt.md`'s own STEP list is not exercised again until the next `run roadmap` invocation, so this record demonstrates the same mechanics — real, shell-captured timestamps, never estimated or narrated — against this cycle's own live Sprint Execution session instead, satisfying ST-32's AC2 with genuine data rather than deferring the demonstration to a future session.

## Demonstration

| Field | Value | Source |
|-------|-------|--------|
| Session start (UTC) | `2026-09-18T18:04:29Z` | `git log -1 --format=%aI` on `69f436ea` — the first commit of this EPIC-05 execution sub-session (ST-31) |
| Session end (UTC) | `2026-09-18T18:06:49Z` | `date -u +%Y-%m-%dT%H:%M:%SZ`, captured live at the close of the ST-31/ST-32 sub-session |
| Elapsed | `00:02:20` | Computed (`end - start`), not re-typed by hand |

Both timestamps above were captured via the real shell commands §22 requires (`git log -1 --format=%aI <sha>` for a commit-anchored start, `date -u +%Y-%m-%dT%H:%M:%SZ` for a live-captured end) — no value here is estimated or narrated, per §22's own prohibition.

## Disposition

This is a mechanics demonstration only — it is not itself a `run_manifest.md` entry (this session is Sprint Execution, not Roadmap Rebalance, so §22's `run_manifest.md` target does not apply here). The convention's actual wiring lives in `roadmap_prompt.md` v9.22 STEP 1.1/STEP 12.1; its first real in-routine application will be the next `run roadmap` invocation's own `run_manifest.md`.
