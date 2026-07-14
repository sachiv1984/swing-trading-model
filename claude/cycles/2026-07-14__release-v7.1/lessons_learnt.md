Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-14__release-v7.1
Release: v7.1
Last Updated: 2026-07-14

---

# Lessons Learnt — Release Planning v7.1

## What worked well

1. **v7.0's carry-forward lesson was applied directly, closing the loop for the first time.** v7.0's post-ship closure flagged that its capacity-filling heuristic (favour product/bug-fix value over debt) had been applied ad hoc rather than checked against the live Product Value Ratio. This cycle, the ratio (0.33, Advisory tier, alert streak ended) was checked explicitly before selecting the 4 capacity-filling hardening items, and the reasoning was recorded in `run_manifest.md` rather than left implicit.
2. **Roadmap-mandatory anchor naming (STEP 8.0 fast-track) made scope extraction unambiguous.** The prior rebalance named `BLG-BE-59`, `BLG-BE-60`, `BLG-FE-107` directly in `current_roadmap.md` §3, so STEP 2 required no inference about which items constituted the release's non-negotiable floor.
3. **The design-gate language scan (STEP 1.3) correctly caught a design dependency in a capacity-filling item, not just the obvious anchor.** `BLG-FE-107`'s design-gate need was expected (explicit in its own backlog text), but `BLG-QA-106`'s UX consistency review sub-item was only surfaced by systematically scanning all 7 candidate items rather than just the roadmap-named ones.

---

## Friction Log

### Friction Item 1

**Classification:** Type C — Scope/Estimation Judgment Call

**Recurrence:** Not confirmed as recurring — no cross-cycle search performed this session; flagging for the next session to check.

**What happened:** The capacity check (STEP 4.5) landed at exactly 14.0 days against a ~12–14 day capacity band, with a pessimistic-case reading (~15.5 days) that exceeds the warn threshold. Two of the four capacity-filling hardening items (`BLG-BE-61`, `BLG-QA-106`, `BLG-SPEC-83`, `BLG-SPEC-84`) carry only a letter effort band (`M`) with no explicit day range in their backlog entries, unlike the two mandatory anchors (`BLG-BE-59`: "M (~1-2 days)", `BLG-BE-60`: "L (~3-5 days)") which do. The capacity check had to assume a day-range for bare-letter `M` items by analogy to unrelated prior-cycle items (v7.0's `BLG-FEAT-69`/`BLG-FEAT-70`, both "M (~2 days)"), rather than reading it directly off the item.

**Where in the routine:** STEP 4.5 — Capacity Feasibility Sense Check.

**Root cause:** Backlog item authoring convention is inconsistent — some items include an explicit day range alongside the S/M/L/XS letter band, others don't. This isn't enforced at idea-intake or backlog-grooming time.

**Suggested fix:** Consider whether `backlog_management_prompt.md` (`groom backlog`) or idea-intake disposition should require an explicit day-range estimate alongside the letter effort band for any item carrying a `Provisional-Target` value (i.e., items likely to be pulled into a release soon), so Release Planning STEP 4.5 doesn't have to infer ranges by analogy. Not applied this cycle — flagging as a defer candidate for Head of Specs Team review, not an in-flight patch.

**Target:** Defer — Head of Specs Team to assess whether to add this as a `backlog_management_prompt.md` or `idea_intake_prompt.md` requirement; no target date fixed yet, revisit at next `groom backlog` or `run ideas` invocation if this recurs.

### Friction Item 2

**Classification:** Type C — Scope Ambiguity

**Recurrence:** First occurrence.

**What happened:** `BLG-BE-60`'s "Proposed solution" field lists three genuinely alternative fix vehicles ((a) persist/cache prices, (b) append-only ledger, (c) wire the existing drift-check to an alert) without the backlog entry recommending one. This is a true either/or engineering decision, not a checklist of sub-items to complete (contrast with `BLG-SPEC-84`'s 7-part scope list, which is additive, not alternative). It was tracked as RISK-01 in the execution plan with a mitigation of "resolve at EPIC-01 kickoff," but this defers real effort-sizing uncertainty into execution rather than resolving it at planning time.

**Where in the routine:** STEP 3 — Execution Plan (Risk Register).

**Root cause:** No convention distinguishes "additive scope checklist" backlog items from "alternative approaches, pick one" backlog items — both render as a lettered list in the same "Proposed solution"/"Scope" field.

**Suggested fix:** No prompt change recommended this cycle — RISK-01's mitigation (resolve at kickoff, record in sprint planning notes) is an adequate execution-phase handling. Flagging only as a naming-convention observation for future backlog authoring: alternative-approach items could be phrased "candidate fix vehicles (pick one)" vs. additive items phrased "sub-items (all required)" to disambiguate at a glance.

**Target:** Advisory only — no action item filed.

---

## Monitoring Carried Forward

- SI-02 gate condition 1 remains NOT MET (0/11 linked trade plans, `insufficient_data` drift status) — monitor at next release planning readiness scan.
- PO-02 / PO-04 data-density gates: still no queryable live signal found this session (same as v6.9) — Product Owner should confirm whether a journal-entry-count endpoint exists or needs to be added.
- RISK-03 (`BLG-FE-107` design-gate decision) and RISK-04 (`BLG-QA-106` UX consistency review) are both routed to `run design-gate` — confirm both are actually resolved there before `plan sprint` is invoked; if the design gate only classifies `BLG-FE-107` and misses `BLG-QA-106`'s sub-item, escalate.

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Bare letter effort bands (`M` with no day range) on backlog items force Release Planning STEP 4.5 to infer day ranges by analogy to unrelated prior items rather than reading them directly, reducing capacity-check precision right when the total lands close to a WARN threshold. | Consider requiring an explicit day range alongside the letter band for any item carrying a `Provisional-Target` value, enforced at `groom backlog` or idea-intake disposition time. | Roadmap |
| 2 | This cycle's capacity check landed at exactly the top of the capacity band (14.0d midpoint, ~15.5d pessimistic) after combining 3 mandatory anchors with 4 capacity-filling items — a WARN outcome with zero buffer. | Sprint Planning should treat the `release_plan.md §Capacity Check` Phasing Recommendation as a live option, not just an artefact, and confirm early in Sprint 1 whether `BLG-BE-60`'s fix-vehicle choice (RISK-01) is trending toward the pessimistic estimate before committing to a single-sprint delivery of all 7 items. | Sprint Planning |

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-07-14__release-v7.1",
  "phase": "Release",
  "status": "present",
  "generated_utc": "2026-07-14T00:55:00Z"
}
```
