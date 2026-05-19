**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Published
**Last Updated:** 2026-05-19
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Meta-Review — Roadmap Rebalance

**Trigger:** 3 completed rebalance cycles since last meta-review (`2026-05-15__scheduled-2`)
**Cycles reviewed:**
- `2026-05-18__scheduled`: no cycle directory; no lessons_learnt — no data
- `2026-05-18__scheduled-2`: directory with only `.preflight_marker` (untracked); no committed lessons_learnt — no data
- `2026-05-19__scheduled`: this cycle (lessons_learnt filed as part of this run)

**Review date:** 2026-05-19

---

## Friction Item Aggregation

Only one cycle (`2026-05-19__scheduled`) has a lessons_learnt.md. The two prior cycles have no artefacts.

| Type | Cycle | Description | Recurring |
|------|-------|-------------|-----------|
| Type D — Artefact Discipline | 2026-05-18__scheduled + 2026-05-18__scheduled-2 | Two consecutive scheduled rebalances completed (state file updated) with no cycle artefacts committed to git. Decision log entries DL-031/032 cited in memory records are absent from decision_log.md. Park counts not applied for those cycles. | × 2 (consecutive) |

---

## Pattern Analysis

**Type D pattern identified:** Two consecutive cycles without committed artefacts.

The root cause is that the roadmap rebalance prompt's STEP 12 does not require artefact existence verification before updating the state file. The state file was updated as part of a broader governance commit (post-ship closure or other), but the actual rebalance artefacts (cycle_record, lessons_learnt, cycle_summary, decision_log update, ideas_register updates) were never committed.

**Consequences observed:**
- Decision log has a gap (DL-031/032 cited but absent)
- Ideas_register park counts were not incremented for two cycles
- `rebalance_cycles_since_meta_review` counter was incremented without corresponding process work
- Memory records describe "complete" runs that have no committed evidence

**Cross-cycle pattern check:**
- Type D (artefact discipline): ≥ 2 cycles ✓ — qualifies for meta-review action
- No other types identified (cycles 2026-05-18__scheduled/scheduled-2 have no LL data to analyse)
- No deferred patches from prior cycles carried forward > once (prior LL from 2026-05-15__scheduled-2 was clean)
- STEP 9 invariant: not triggered in available data

---

## Candidate Prompt Change

**File:** `claude/system/roadmap_prompt.md`
**Section:** `### STEP 12 — Stage, Commit & Global State Update` → `#### 12.1 Global State Update`
**Proposed change:** Add artefact existence precondition: "Before updating `last_rebalance_cycle` in `.claude_current_state.json`, verify the following files exist in `claude/cycles/<cycle_id>/`: `run_manifest.md`, `cycle_record.md`, `cycle_summary.md`, `lessons_learnt.md`. If any is absent, complete the missing artefact before updating the state file. Do not update state to reference a cycle with incomplete artefacts."
**Rationale:** The pattern (× 2) shows that the state file can be updated independently of the cycle artefacts, creating a misleading governance state where the file references a cycle that has no evidence.

**Head of Specs Team decision:** ⏸ Defer — target next rebalance cycle. The prompt change is clear and specific; defer to avoid mid-cycle edit. Owner: Head of Specs Team. Target: next roadmap rebalance (before `plan release v3.8` opens).

---

## Outstanding Actions from This Meta-Review

| # | Action | File | Owner | Target |
|---|--------|------|-------|--------|
| 1 | Apply artefact precondition patch to roadmap_prompt.md STEP 12.1 | `claude/system/roadmap_prompt.md` | Head of Specs Team | Next rebalance |

---

## Cycle Count Reset

`rebalance_cycles_since_meta_review` will be reset to 0 in `.claude_current_state.json` (STEP 12.1).
`last_meta_review_cycle` will be updated to `2026-05-19__scheduled`.
