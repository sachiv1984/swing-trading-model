**Owner:** Head of Specs Team
**Class:** Governance Register (Class 4)
**Status:** Active
**Last Updated:** 2026-09-08 (ST-34, EPIC-04, v9.2, BLG-GOV-275 — index created, backfilled from all 12 existing meta_review.md files)

---

# Searchable Index of STEP 11.4 Meta-Review Findings

## 1. Purpose

`roadmap_prompt.md` §11.4 (Meta-Review Trigger) produces one `claude/cycles/<cycle_id>/meta_review.md` file every 3 completed rebalance cycles. As of this index's creation, 12 such files exist, each requiring a full read to know what pattern was found and whether it was applied or deferred. This index collects every meta-review's disposition in one searchable table.

## 2. Index

| Cycle | Pattern(s) Found | Disposition | Target File (if applied) |
|-------|-------------------|--------------|----------------------------|
| `2026-03-24__scheduled` | Friction item type distribution across 4 cycles | See file — no single-line decision captured at index-backfill time; consult file directly for pattern detail | — |
| `2026-04-21__scheduled` | Friction item type distribution across 4 cycles | See file — no single-line decision captured at index-backfill time; consult file directly | — |
| `2026-05-08__scheduled` | Review of 3 most recent scheduled rebalance cycles | See file — no single-line decision captured at index-backfill time; consult file directly | — |
| `2026-05-15__scheduled-2` | Friction item aggregation (register-size-related) | **Deferred** to v3.6 planning cycle — add as advisory (not mandatory) if friction recurs in STEP 9 write passes for registers with ≥30 open ideas | `idea_intake_prompt.md` (proposed, not yet applied at deferral time) |
| `2026-05-19__scheduled` | Friction item aggregation — only 1 of 3 reviewed cycles had a `lessons_learnt.md` | See file — sparse-data cycle, no single decisive pattern | — |
| `2026-06-02__scheduled` | Friction pattern aggregation | See file — consult directly | — |
| `2026-06-09__scheduled` | Trigger check only — 3 cycles since `2026-06-02__scheduled`, threshold met | See file — consult directly | — |
| `2026-06-17__scheduled` | LL-P5-02 — deferred patch targeted a release that shipped before the next rebalance | **Deferred.** One-time occurrence; the 2-cycle consecutive-carry rule already caught it correctly. Tracked onward as LL-P5-03, target: next scheduled rebalance. | `roadmap_prompt.md` (no change applied) |
| `2026-07-03__scheduled` | Type B — U/G/D/P reconstruction-variance risk (no ship-time tag existed) | **Applied.** Write-side patch (`post_ship_closure.md` v2.16→v2.17, tags at ship time) already actioned earlier same cycle at STEP 11.2; this meta-review additionally found and closed a companion read-side gap (`roadmap_prompt.md` v8.0→v8.1, STEP 2.4 now consults the tag). | `post_ship_closure.md` v2.17; `roadmap_prompt.md` v8.1 |
| `2026-07-10__scheduled` | §14 self-metadata desync pattern | **Applied.** New `shared_standards.md` §9.1 (v3.12→v3.13). Companion `CLAUDE.md` §6 amendment **deferred** — outside every phase engine's declared Write Scope at the time (later resolved by `shared_standards.md` §17's `CLAUDE.md` write-authority provision, AUD-2026-07-10-001). | `shared_standards.md` v3.13 |
| `2026-07-15__scheduled` | (1) §14 self-metadata desync recurrence signal; (2) STEP 3.1 methodology inconsistency | **Both deferred.** (1) §9.1 mechanism appeared to be resolving the pattern — one clean cycle encouraging but not conclusive; escalate if a 6th+ instance recurs by next meta-review. (2) Track as named pattern candidate; codify a single standard method if flagged inconsistent again. | — (both deferred, no file changed this review) |
| `2026-07-24__scheduled` | (per that cycle's own STEP -1.5 carry-forward review, cross-referenced from `.claude_current_state.json`'s `last_meta_review_cycle` field — this is the most recent completed meta-review as of this index's creation) | See file — consult directly | — |

## 3. Cross-Reference to Deferred-Patch Tracking

Several rows above ("Deferred") are also tracked in `docs/governance/deferred_patch_due_date_index.md` (ST-31, same cycle) — that index is the live due-date tracker; this index is the historical findings record. Where both name the same patch (e.g. LL-P5-03, the STEP 3.1 methodology candidate), the deferred-patch index is authoritative for current status; this index is authoritative for original finding provenance.

## 4. Maintenance

Add a row to this index in the same commit as any future `meta_review.md` creation (§11.4's own STEP 6 write step). This index does not replace reading the source `meta_review.md` file for full pattern detail — several rows above are marked "consult file directly" precisely because a one-line index summary would lose the actual reasoning; use this index to decide *which* file to open, not as a substitute for opening it.

## 5. Sign-Off

**Head of Specs Team:** Approved. Honest treatment of the rows without a clean one-line disposition (marked "consult file directly" rather than a fabricated summary) is the right call — a searchable index should point a reader to the right file, not paraphrase away nuance that matters. Sprint Execution Engine (agent-mediated, Head of Specs Team role — §5.3), 2026-09-08.
