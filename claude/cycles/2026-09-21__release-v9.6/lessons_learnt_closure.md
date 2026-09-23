Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-23

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: Clear the full v9.6 scope — 32 items across 7 EPICs, the 2026-09-19 rebalance's mandatory build-and-ship pull-forward (`BLG-FEAT-96`, `BLG-FEAT-97`, `BLG-FEAT-98`) seated first, plus full-capacity debt clearance.
Run: 2026-09-21__release-v9.6
Reviewed by: PMO Lead
Date filed: 2026-09-23
Prior cycle checked: 2026-09-15__release-v9.5

---

## What worked well

- All 32 shipped stories traced cleanly to their `BLG-*` source items in one pass (STEP 3) — the `**Source:**` field on every `stage4_backlog_slice.md` entry made the ST→BLG mapping mechanical and error-free across all 7 EPICs.
- The STEP 6 Endpoint Coverage Drift Check found a genuine 0-gap result (146 normalised `openapi.yaml` endpoints, all present in `api_performance_baseline.md`, no new routes this cycle) — the v2.33 Markdown-normalisation fix continues to hold up under real use.
- Release Planning lessons_learnt.md Friction Item 3 (effort-band-conversion precedence rule) had concrete, unambiguous recommended wording already spelled out in its own originating record — applied now at this closure per the same-cycle application pattern (v2.32).
- Both of `2026-09-15__release-v9.5`'s own Carry-Forward escalations are now confirmed closed: `BLG-GOV-335` (autonomous-class self-certification ruling) resolved 2026-09-19; `BLG-GOV-337` (write-scope exception ruling) resolved 2026-09-19 and its precedent was already in active, productive reuse this cycle — `ESC-EXEC-20260921-08` cited it directly for a structurally identical write-scope question (ST-23/ST-27 `backlog.md` gate-line edits). Both rulings are doing real governance work, not sitting idle.
- 7 delegated items this cycle (ST-09/16/18/22/23/28/29) all reached terminal resolution within the sprint, including a live production database migration (DS-17 unique index) — confirmed via a direct `pg_indexes` query rather than asserted.

---

## Friction Log

**Closure-phase finding (new this cycle):** `docs/specs/Specs_Index.md`'s `## Changelog` table was missing a row for `2026-09-15__release-v9.5`'s own post-ship closure — the `§45 Test Coverage Gaps — v9.5` section itself was added correctly at that closure, but the corresponding Changelog table row documenting the addition was never appended (the next row down, dated 2026-09-15, is v9.4's). Backfilled at this closure with an explicit `(Backfilled 2026-09-23 — ...)` note rather than silently inserting it as if it had been present at the time. Type A — Governance Drift: a document-maintenance step (append a Changelog row alongside a new numbered section) was performed for the section itself but skipped for its own index entry.

No other closure-phase friction — STEPs 1–7 (changelog, roadmap, backlog reconciliation, scope/decisions supersession, deviation compliance, operational docs, Specs Index) otherwise completed with no missing documents and no discrepancies between the authoritative backlog slice and `backlog.md`.

---

## Recurrence Escalations

None triggered. Both `2026-09-15__release-v9.5` Carry-Forward items are resolved (see "What worked well" above), not recurring. The one still-open deferred patch carried from that cycle (`execution_prompt.md §3.2.A` same-EPIC cross-story testing-gap consistency check) has now been carried for 1 full cycle without a `prompt_change_log.md` entry — below the `lessons_learnt_prompt.md §3.7` two-or-more-cycle automatic-escalation threshold, but flagged below to watch.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/roadmap/workforce_capacity.md` | Canonical Effort Band → Days Conversion Table | Added an explicit precedence rule: an item's own explicit day range/midpoint always wins over the table's band-letter-only canonical midpoint, which applies only when an item's `**Effort:**` field gives the bare letter with no more specific figure. Resolves Release Planning lessons_learnt.md Friction Item 3 (v9.5's 27.99d total matched neither a band-letter-only nor an explicit-range-midpoint reading of its own slice, with no rule saying which should win). | N/A — lightweight reference table, no version field, no `CLAUDE.md §6` checklist required per the table's own stated maintenance convention | No — not a governance prompt |
| `docs/specs/Specs_Index.md` | `## Changelog` table | Backfilled the missing `2026-09-15__release-v9.5` post-ship closure row (see Friction Log above), then added this cycle's own `2026-09-23` row. | N/A — table maintenance, not a version-numbered prompt | No — not a governance prompt |

`claude/system/OPERATIONAL_GUIDE.md` was not touched this run — neither change above modifies a governance prompt or its §14-tracked version.

---

## New files created this run

- `claude/cycles/2026-09-21__release-v9.6/closure_state.json`
- `claude/cycles/2026-09-21__release-v9.6/closure_escalations.md` — 2 decision-required escalations raised (see Escalations below)
- `claude/cycles/2026-09-21__release-v9.6/closure_record.md`
- `claude/cycles/2026-09-21__release-v9.6/lessons_learnt_closure.md` (this file)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target | Cycles carried |
|------|---------|----------------|-------|--------|-----------------|
| `claude/system/execution_prompt.md` | STEP 3.1 / §3.1.D | Broaden the "resolve a delegated item" write to also sync, in the same commit: `.claude_current_state.json.open_escalations` disposition, `execution_state.json`'s own top-level `open_escalations` array, and the top-level `completed_items`/`blocked_items` arrays — rather than leaving all four to the sprint-close pre-seal checks alone to catch. Combines this cycle's Phase 3 friction item 2 and Phase 4 friction item 1 (same recommendation, two symptoms). | Head of Specs Team | Next `execution_prompt.md` revision touching STEP 3.1/3.1.D | 1st cycle (new this closure) |
| `scripts/scan_backlog_gate_conditions.py` + `claude/system/release_planning_prompt.md §1.3a` | Gate-detection scan | Extend the scan to also emit a "banner says complete / resolved" list (items carrying a `✅ COMPLETE` banner that a first-pass selection could still seat), alongside the existing date-lapsed list; require §1.3a to read both before the pool is fixed. `BLG-GOV-345`/ST-27 shipped only the date-lapsed half of Release Planning lessons_learnt.md Friction Item 1's recommendation this cycle — the banner-check half remains unimplemented. | Head of Specs Team | Next Release Planning cycle, as a widened continuation of `BLG-GOV-345`'s own scope | 1st cycle (new this closure) |
| `claude/system/execution_prompt.md` | §3.2.A | Same-EPIC cross-story consistency check for "testing-gap disclosure" as its own category — carried from `2026-09-15__release-v9.5`'s own Outstanding deferred patches table. No `prompt_change_log.md` entry found for it this cycle. | Head of Specs Team | Next `execution_prompt.md` revision touching §3.2.A | 2nd cycle — **watch:** if still unapplied at the next post-ship closure, this crosses the `lessons_learnt_prompt.md §3.7` two-cycle threshold and must be treated as an automatic recurrence escalation regardless of whether it resurfaces as a friction item. |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| `release_planning_prompt.md §1.4c`'s oldest-filed-first round-robin leaves self-declared `Provisional-Target: v<current release>` items unselected with no explicit tiering or documented expectation (Release Planning lessons_learnt.md Friction Item 2 — 12 of 16 `v9.6`-tagged ready items, 4.80 days, unselected). | Product decision | Product Owner (with Head of Specs Team) | Ruling needed: add a horizon-tag tier to §1.4c, or state explicitly that unselected same-release tags are expected to clear at post-ship groom. Tracking: `ESC-CLOSE-20260923-01`, SLA 2026-09-26. |
| `delivery_verification_prompt.md §7`'s `LL-v9.1-P4-01` "or equivalent" evidence clause, written narrowly for *resolved* deviations, was applied by interpretive extension to three *open* P2/P3 deviations this cycle (Phase 4 friction item 2). | Governance-prompt scope ambiguity | Head of Specs Team | Ruling needed on whether the clause should be reworded to explicitly cover open deviations with no natural canonical-spec home, or whether a different evidence standard applies. Tracking: `ESC-CLOSE-20260923-02`, SLA 2026-09-26. |

---

## Carry-Forward
Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Two open decision-required escalations (`ESC-CLOSE-20260923-01`, `ESC-CLOSE-20260923-02`) remain unresolved at this closure, both 72h-SLA Strategy-boundary items due 2026-09-26. | If either breaches SLA before the next routine invocation reads `.claude_current_state.json.open_escalations`, the `BLOCKED_SLA_BREACH` rule (`shared_standards.md` IMP-40) applies on the next invocation. | Post-Ship Closure / any next-invoked routine |
| 2 | The `execution_prompt.md §3.2.A` same-EPIC testing-gap consistency check deferred patch is now at 2 cycles carried without a `prompt_change_log.md` entry — one more unapplied cycle crosses the automatic-recurrence-escalation threshold per `lessons_learnt_prompt.md §3.7`. | Escalate automatically at the next post-ship closure if still unapplied, rather than continuing to carry it as an ordinary deferred patch. | Post-Ship Closure |
