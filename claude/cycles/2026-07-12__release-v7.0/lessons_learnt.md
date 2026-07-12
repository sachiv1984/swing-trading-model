Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Filed
Release: v7.0
Cycle: 2026-07-12__release-v7.0
Last Updated: 2026-07-12

---

# Lessons Learnt — Release Planning: v7.0

## Carry-Forward Item Closed

v6.9's Release Planning lessons-learnt filed exactly one carry-forward item: "Release Planning should consider explicitly surfacing capacity headroom as a question to the Product Owner when scope is silent on appetite, rather than defaulting to the narrowest mandatory-only scope." This cycle's invocation was *not* silent on appetite — the user explicitly flagged the governance-overhead-to-story-count ratio and asked for the release to be maximised — but the engine still surfaced an explicit multi-choice question on *how* to maximise (fill capacity with ready backlog items vs. named-mandatory-only vs. user-specified), rather than silently guessing. PO selected "fill capacity with ready backlog items," directly producing this cycle's 15-story, 3-EPIC scope (~9.5 of ~12-14 estimated days) versus v6.9's 2 stories (~4-6 of ~12-14 days).

**Observation:** Asking a single structured question at invocation time — rather than deferring the ambiguity to a lessons-learnt advisory after the fact — resolved the exact gap flagged last cycle in one round-trip. No prompt change is recommended; this confirms the existing "ask when scope appetite is genuinely ambiguous" judgment call is sound and should be repeated, not just documented as an aspiration.

**Target:** No action item — carry-forward item closed by direct resolution this cycle.

## Selection Methodology Note

When filling capacity beyond named-mandatory items, this cycle deliberately favoured genuinely ungated, product/bug-fix-value backlog items over additional P3 governance/process/tooling debt, because the backlog carries an active 🔴 3rd-consecutive Product Value Alert (ratio 0.21, below the 0.30 floor per the `2026-07-12__scheduled` rebalance). Padding scope with low-value tooling items to hit a larger story count would have worked directly against that alert. This is worth carrying forward as an explicit selection heuristic for any future "maximise scope" instruction: **more stories is not automatically better if the additional stories are process debt rather than product value** — check the Product Value Ratio state before treating "add more" as "add anything ungated."

## Monitoring Carried Forward

- SI-02 gate condition 1 remains NOT MET; monitor forward-linkage accrual at next release planning readiness scan.
- PO-02 / PO-04 data-density gates: no queryable live signal found this session; unchanged from v6.9.
- Design Gate is required this cycle (8 of 15 items UI-facing) — `run design-gate` must complete before `plan sprint` seals (see `cycle_summary.md` Pre-sprint Planning Required Decisions).

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Selection heuristic (favour product/bug-fix value over governance/tooling debt when filling scope headroom) was applied ad hoc this cycle based on the live Product Value Ratio state, not a codified rule. | Consider whether `release_planning_prompt.md` STEP 2 should explicitly instruct checking the current Product Value Ratio/Alert state before selecting capacity-filling candidates, so this isn't left to session-specific judgment each time. | Release Planning |

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-07-12__release-v7.0",
  "phase": "Release",
  "status": "present",
  "generated_utc": "2026-07-12T22:30:00Z"
}
```
