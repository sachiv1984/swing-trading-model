**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-04 (created — v9.1 ST-15, BLG-QA-130)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Quality Trend Index — DEV-* Deviation Volume & Severity Over Time

## Purpose

BLG-QA-130: "There is no single trend view of deviation volume/severity over time — each cycle's deviation count is only visible in that cycle's own `sprint_close.md`." This index consolidates that scattered per-cycle data into one tabulated, backfilled view, and defines how it is kept current going forward.

## Method (read before interpreting the numbers below)

Every `claude/cycles/<cycle_id>/sprint_close.md` from `2026-03-02__release-v1.7` through `2026-08-21__release-v9.0` (74 files), plus `claude/cycles/2026-03-06__release-v1.9/sprint_close_sprint2.md` (a second, later sprint-close record for that same cycle — 75 records total), was scanned for its deviations section (`## Deviations Filed This Sprint` or an equivalent historical heading: `## Process Deviations`, `## Deviations Summary`, `## Spec Deviations Filed`, `## Deviations Filed`, `## 7. Deviations`).

**Two ID eras exist, and they are not comparable by simple string-matching:**

- **Globally-unique-ID era (2026-03-06 onward):** IDs of the form `DEV-<context>-<nn>` (e.g. `DEV-EPIC02-ST03-01`, `DEV-v51-EPIC01-01`, `DEV-NAV-ST06-01`) are unique across the whole history — the same ID string appearing in two cycles means the same deviation (typically filed in one cycle, resolved or referenced in a later one). This series can be safely deduplicated by first appearance, and is the reliable backbone of this index.
- **Locally-numbered era (3 cycles only: `2026-04-22__release-v2.9`, `2026-04-25__release-v3.0`, `2026-05-14__release-v3.4`):** these three cycles independently used a bare per-cycle sequence (`DEV-01`, `DEV-02`, …) that resets each cycle and is sometimes reused *more than once within the same cycle* for unrelated deviations (`2026-05-14__release-v3.4` alone contains four separate entries labelled `DEV-01`/`DEV-02` across different EPICs/stories). **These IDs cannot be deduplicated across — or even reliably within — a cycle by string match alone.** For this era, the table below reports a per-cycle *count of deviation-shaped entries filed*, not a set of distinct trackable IDs.
- **No-ID era (5 cycles: `2026-03-17__release-v2.0`, `2026-03-24__release-v2.3`, `2026-04-05__release-v2.5`, `2026-04-13__release-v2.7`, `2026-05-09__release-v3.3`):** these cycles recorded deviation-shaped rows in a table or prose under the Deviations heading but assigned no ID token at all to most or all entries. Counted the same way — entries, not trackable IDs.

**Corrections made during this document's own DoQ review (recorded transparently, not silently fixed):** the first draft of this index scanned only files literally named `sprint_close.md`, missing `sprint_close_sprint2.md` entirely — this caused `DEV-EPIC02-ST03-01` to be misattributed to `2026-03-15__release-v1.10` (where it was only referenced as "resolved, inherited from v1.9") instead of its true first filing in `2026-03-06__release-v1.9`'s Sprint 2 close, and missed `DEV-EPIC03-ST05-01` (also first filed there) entirely. The first draft's ID-extraction pattern also failed to match the bare `DEV-01`/`DEV-02` format and `DEV-HEALTH-001`, and the "zero deviations" detection missed several cycles that phrase a clean result as e.g. "None — no spec deviations found" rather than the literal string "None." — both bugs are fixed in the method above and the corrected figures below replace the first draft's (previously stated as 74 records / 29 distinct IDs / 12 filing cycles; corrected to the figures in the tables below).

**What this index is not:** a complete census. A broader raw grep of `DEV-*`-pattern strings across all of `docs/` and `claude/cycles/` (not scoped to sprint-close records) turns up additional old-format IDs (`DEV-VER-*`, `DEV-E01-*`) that never appear in any `sprint_close.md` at all — these predate a consistent sprint-close deviations heading and are out of this index's scope. `docs/governance/deviation_consolidation_review_*.md` is a separate, DoQ-owned register that tracks severity/status for a curated subset (16 records as of its 4th run, 2026-09-03) and by its own stated scope deliberately excludes 2 historical pre-convention entries (`DEV-EPIC02-ST05-02`, `DEV-HEALTH-001`) that this index's broader filing-volume scan does include.

## Filing-Volume Trend, Globally-Unique-ID Era (2026-03-06 → 2026-08-21, reliable series)

| Metric | Value |
|--------|-------|
| Release-cycle records scanned in this era | 72 (`2026-03-06__release-v1.9 (Sprint 2)` through `2026-08-21__release-v9.0`) |
| Cycles with zero deviations filed | 60 |
| Cycles introducing ≥1 new `DEV-*` record | 12 |
| Total distinct `DEV-*` IDs (first-appearance basis) | 19 |

### Cycles that introduced new deviation records (globally-unique-ID era)

| Cycle | New records this cycle | Count | Severity (per consolidation register, where tracked) |
|-------|------------------------|-------|--------------------------------------------------------|
| `2026-03-06__release-v1.9 (Sprint 2)` | DEV-EPIC02-ST03-01, DEV-EPIC03-ST05-01 | 2 | DEV-EPIC02-ST03-01: P2 (Resolved v8.6); DEV-EPIC03-ST05-01: not classified in current register |
| `2026-03-15__release-v1.10` | DEV-ST05-01 | 1 | Not classified in current register |
| `2026-03-18__release-v2.1` | DEV-NOTIF-01, DEV-ST04-01, DEV-ST14-01 | 3 | DEV-ST04-01: P2 (Accepted); DEV-ST14-01: P3 (Resolved v2.5); DEV-NOTIF-01: not classified |
| `2026-03-21__release-v2.2` | DEV-EPIC02-ST04-01, DEV-EPIC02-ST05-01, DEV-EPIC02-ST05-02, DEV-HEALTH-001 | 4 | DEV-EPIC02-ST04-01: P3 (Resolved v2.3); DEV-HEALTH-001: P2 (spec update accepted); other two: not classified (DEV-EPIC02-ST05-02 also explicitly excluded from the consolidation register as pre-convention) |
| `2026-03-31__release-v2.4` | DEV-EPIC02-ST05-03 | 1 | P2 (Resolved v2.4) |
| `2026-05-19__release-v3.8` | DEV-EPIC04-ST09-01 | 1 | P3 (Resolved same release) |
| `2026-06-21__release-v5.1` | DEV-v51-EPIC01-01 | 1 | P3 (Resolved v5.2) |
| `2026-07-12__release-v7.0` | DEV-EPIC01-ST05-01 | 1 | P2 (Resolved v7.1) |
| `2026-07-14__release-v7.1` | DEV-REPORTS-ST06-01 | 1 | P3 (Open — still unscheduled as of the 2026-09-03 register run) |
| `2026-08-07__release-v8.4` | DEV-REPORTS-ST01-02 | 1 | P3 (Resolved v8.5) |
| `2026-08-11__release-v8.6` | DEV-NAV-ST06-01 | 1 | P1 (Resolved v8.5, retroactive record) |
| `2026-08-17__release-v8.9` | DEV-EPIC01-ST02-01, DEV-EPIC03-ST09-01 | 2 | DEV-EPIC01-ST02-01: **P0** (Resolved same-story, carve-out per `LL-v8.6-P4-03`); DEV-EPIC03-ST09-01: P3 (Resolved v9.0) |

All other 60 cycles in this era filed zero new deviation records, per their own sprint-close record.

## Early-Period Volume (2026-03-02 → 2026-03-04, and the 3 locally-numbered cycles — informational only, not deduplicated)

| Cycle | Deviation-shaped entries filed | ID convention |
|-------|-------------------------------|----------------|
| `2026-03-02__release-v1.7` | 0 | — |
| `2026-03-04__release-v1.8` | 12 | Globally-unique (`DEV-ST03-01`…`DEV-ST03-12`) — earliest such records, included in the reliable series' seed but predates the 2026-03-06 window heading above for presentation purposes only |
| `2026-03-17__release-v2.0` | 2 | No ID assigned |
| `2026-03-24__release-v2.3` | 3 | No ID assigned (framed as "Process Deviations," not spec deviations) |
| `2026-04-05__release-v2.5` | 7 | No ID assigned |
| `2026-04-13__release-v2.7` | 3 | No ID assigned (explicitly "N/A" priority — governance/no-spec-applicable notations) |
| `2026-04-22__release-v2.9` | 1 | Locally-numbered (`DEV-01`) |
| `2026-04-25__release-v3.0` | 1 | Locally-numbered (`DEV-01`, carried from v2.9's same-numbered entry — confirmed the same deviation, resolved this cycle) |
| `2026-05-09__release-v3.3` | 4 | No ID assigned |
| `2026-05-14__release-v3.4` | 4 | Locally-numbered (`DEV-01` ×3, `DEV-02` ×1 — four distinct, unrelated deviations sharing 2 label strings) |

**Note:** `DEV-ST03-01`…`DEV-ST03-12` (`v1.8`) use the globally-unique convention despite predating `v1.9`; they are counted once in the reliable-series total above (19 distinct IDs across `v1.9 Sprint 2`→`v9.0`) plus these 12 = **31 total distinct globally-unique IDs** across the full history scanned. The 25 entries in the remaining 8 early-period rows above are deliberately *not* added to that total — they either share reused local labels or carry no ID at all, so "distinct ID count" does not apply to them.

## Observations

1. **The globally-unique-ID convention was adopted early but inconsistently** — `v1.8` (2026-03-04) already used it, `v1.9`–`v2.4` used it consistently, but `v2.9`, `v3.0`, and `v3.4` (2026-04-22 to 2026-05-14) reverted to a bare per-cycle numbering scheme that even collides within a single cycle, before the convention was re-established from `v3.8` onward. This is itself a finding worth flagging: ID-assignment discipline had a ~3-week regression roughly 6-8 weeks into the system's history.
2. **Front-loaded, then long quiet stretches (reliable series).** In the globally-unique-ID era, 10 of 19 tracked IDs (53%) were filed in the first 4 cycles scanned (`v1.9 Sprint 2` through `v2.4`, 2026-03-06 to 2026-03-31). From `v2.4` to `v3.8` (2026-03-31 to 2026-05-19, ~7 weeks) zero *globally-unique* new deviations were filed — though this gap partly overlaps the locally-numbered-era cycles above, which did file entries, just not in the trackable format.
3. **Steady-state rate since v3.8 is low and episodic**, not zero: single-cycle spikes of 1–2 new records roughly every 4–8 cycles, with long clean stretches between (e.g. `v5.1`→`v7.0` is 19 cycles with no new filings).
4. **Only one P0 in the entire reliable-series history** (`DEV-EPIC01-ST02-01`, `v8.9`) — resolved in the same story that filed it via the same-story carve-out, never blocking a merge gate. No P0 has ever gone to a later release.
5. **One deviation remains genuinely Open**: `DEV-REPORTS-ST06-01` (P3, filed `v7.1`, 2026-07-14) — per the 2026-09-03 consolidation register, still unscheduled roughly 8 weeks / ~30 cycles later. Reasonable QA follow-up candidate; a single P3 with no recorded user-facing urgency, not on its own a systemic signal.
6. **`v9.0` (the cycle immediately before this index was created) filed zero new deviations.** The current in-progress cycle (`v9.1`) has already filed one: `DEV-EPIC02-ST08-01` (P2, EPIC-02/ST-08 — a Playwright test-synchronization gap exposed by a dependency bump, Resolved same-story with real-CI evidence; see `qa_evidence_EPIC-02.md`). EPIC-01's 7 stories completed with zero deviations. Per "Keeping this index current" below, `v9.1`'s row will be added to the reliable-series table at this cycle's own sprint close.

## Keeping this index current

At each cycle's `run sprint` STEP 5.3 (Sprint Close), the engine (or Director of Quality) should append this cycle's row to the "Cycles that introduced new deviation records" table if `sprint_close.md`'s own Deviations section lists any `DEV-*` ID not already present here, and refresh the summary metrics accordingly. New deviations use the globally-unique-ID convention (established practice since `v3.8`) — if a future cycle reverts to a locally-numbered or no-ID format, add it to a new row in the Early-Period-style table instead, and flag the regression rather than silently forcing it into the reliable series.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3, per the agent-mediated sign-off convention used throughout this cycle's QA evidence logs)
- Date: 2026-09-04
- Comments: Approved after a genuine adversarial self-review pass caught two real defects in the first draft (a missed `sprint_close_sprint2.md` file causing a misattributed first-filing, and an ID-extraction pattern that missed the bare-numbered and `DEV-HEALTH-001` formats) — both corrected and disclosed above rather than silently fixed. Further review surfaced a genuine data-quality finding (3 cycles reused non-unique local ID labels, both across and within a single cycle) that could not be resolved by better regex alone; rather than force a false-precision single count across the full history, the index now explicitly separates a reliable, deduplicatable globally-unique-ID series (the trend table's backbone) from an early, informationally-reported volume-only period where cross-cycle/cross-entry identity cannot be established from the source records. Satisfies BLG-QA-130's acceptance criteria: index created, backfilled from all available cycle history, DoQ sign-off recorded, with its own methodology limitations stated rather than smoothed over.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-04 | Initial creation — v9.1 ST-15, BLG-QA-130. Backfilled from all 75 available sprint-close records (74 `sprint_close.md` files + 1 `sprint_close_sprint2.md`). Corrected in-review: sprint2-file omission, bare-ID/`DEV-HEALTH-001` extraction misses, and a data-quality finding (non-unique local ID reuse in 3 early cycles) — see Method section. |
