Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-15__release-v7.2
Release: v7.2
Last Updated: 2026-07-15

---

# Lessons Learnt — Release Planning v7.2

## What worked well

1. **All 8 scope candidates carried explicit day-range effort estimates, not just bare letter bands.** This directly addresses v7.1's Friction Item 1 (bare `M`/`S` letters forcing the capacity check to infer ranges by analogy). Every item this cycle — `BLG-FE-55/109/110/111/112`, `BLG-SPEC-89/90`, `BLG-QA-111` — already carried a day range in its backlog entry, per `scored_initiatives.md`'s own note. The §4.5 capacity check needed zero inference this cycle.
2. **The `BLG-SPEC-89`/`BLG-SPEC-90` readiness-pass pairing made sequencing constraints explicit and traceable directly from backlog item text.** Both spec items name their dependent implementation item(s) by ID and state the "must complete before sprint planning" constraint in their own AC — STEP 3 execution-plan sequencing required no inference, just transcription.
3. **§1.3 Design-Gate Language Scan cleanly classified all 3 UI-facing items (`BLG-FE-109/110/111`) on a single systematic pass**, correctly excluding the 2 assessment/audit-only items (`BLG-FE-55`, `BLG-FE-112`) that read as UX work but produce no shipped UI change this release.

---

## Friction Log

### Friction Item 1

**Classification:** Type C — Scope/Estimation Judgment Call (positive data point, not a defect)

**Recurrence:** N/A — this is evidence relevant to an already-open escalation, not a new friction pattern.

**What happened:** v7.1's `lessons_learnt_closure.md` escalated (deadline 2026-07-17, owner Head of Specs Team) the question of whether `groom backlog`/`idea_intake_prompt.md` should mandate an explicit day-range alongside the S/M/L/XS letter band for any item carrying `Provisional-Target`. This cycle's 8 items — all filed at the same 2026-07-15__scheduled rebalance the escalation originated from — already comply with that would-be requirement in practice, without a prompt change forcing it.

**Where in the routine:** STEP 4.5 — Capacity Feasibility Sense Check (context only; not itself a gate failure).

**Root cause:** N/A.

**Suggested fix:** Feed this data point back to the open escalation before its 2026-07-17 deadline: the day-range convention is already being followed voluntarily by whoever filed these 8 items (idea intake / STEP 8.1 direct filing), which may argue for documenting it as guidance rather than adding a hard `idea_intake_prompt.md` gate. Not a recommendation to close the escalation outright — just supporting evidence for Head of Specs Team's disposition.

**Target:** Informational — surfaced for Head of Specs Team ahead of the 2026-07-17 escalation deadline; no action taken by this engine.

### Friction Item 2

**Classification:** Type C — Scope Structuring Judgment Call

**Recurrence:** First occurrence.

**What happened:** The roadmap's v7.2 Now-horizon table (`current_roadmap.md §3`) lists all 8 items in a single flat table with no EPIC grouping — unlike some prior release cycles where the roadmap or a prior fast-track already named EPIC boundaries. This engine had to invent the 5-EPIC structure (grouping each `BLG-SPEC-*` readiness pass with its dependent `BLG-FE-*` implementation item(s), and giving `BLG-FE-112`/`BLG-QA-111` their own EPICs) at STEP 3, rather than transcribing an existing grouping.

**Where in the routine:** STEP 3 — Execution Plan (EPIC table construction).

**Root cause:** Roadmap Now-horizon annotation format (as codified by the STEP 4.2 Idea Consolidation convention) groups by originating idea-consolidation, not by execution EPIC — the two groupings coincide for the `BLG-SPEC-*` pairs but not for the standalone items.

**Suggested fix:** No prompt change recommended — EPIC grouping is core Release Planning STEP 3 authority and the roadmap should not pre-empt it. Flagging only as a "this took a scope-structuring decision, not a lookup" note, in case a future release wants a very different grouping (e.g. all 3 spec items as one EPIC-05 rather than paired with implementation) and that choice should be visible as a decision, not assumed identical.

**Target:** Advisory only — no action item filed.

---

## Monitoring Carried Forward

- Design gate is required (3 UI-facing items: `BLG-FE-109/110/111`) — confirm `run design-gate` covers all 3, and specifically that `BLG-FE-112` (audit-only, correctly excluded) doesn't get pulled in by mistake since it shares a page family with the other UX items.
- `EPIC-05` (`BLG-QA-111`, combined design review + shared Playwright plan) is a soft cross-EPIC dependency covering EPIC-02/03/04 — confirm at Sprint Planning that it is actually scheduled ahead of sprint planning as its own AC requires, not silently deferred.
- SI-02 gate condition 1 remains NOT MET (0/11 linked trade plans, `insufficient_data` drift status) — `BLG-FE-109` in this release directly targets the UX-side cause; monitor whether the gate begins moving once ST-03 ships.

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | All 8 v7.2 scope items already carried explicit day-range effort estimates without a prompt-level mandate — supporting evidence for the open v7.1 escalation (Head of Specs Team, deadline 2026-07-17) on whether to formalise this as a requirement. | Head of Specs Team to factor this data point into the escalation disposition before 2026-07-17. | Roadmap / Idea Intake |
| 2 | `BLG-QA-111`'s combined design review + shared Playwright plan (EPIC-05) is a soft dependency across 3 other EPICs with no hard gate enforcing it runs first — if it slips, EPIC-02/03/04 could each get independent design reviews/Playwright files, defeating its purpose. | Sprint Planning should explicitly confirm EPIC-05 is scheduled and completing ahead of EPIC-02/03/04 sprint planning, not just noted as a recommendation. | Sprint Planning |

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-07-15__release-v7.2",
  "phase": "Release",
  "status": "present",
  "generated_utc": "2026-07-15T22:45:00Z"
}
```
