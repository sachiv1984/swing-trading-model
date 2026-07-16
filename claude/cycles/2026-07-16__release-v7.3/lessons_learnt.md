Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-16__release-v7.3
Release: v7.3
Last Updated: 2026-07-16

---

# Lessons Learnt — Release Planning v7.3

## What worked well

1. **The v7.2 readiness-pass-before-implementation pattern (`BLG-SPEC-89`/`90` → `BLG-FE-109/110/111`) generalised cleanly to a second cycle.** This release's scope decision (ship the 4 new `BLG-SPEC-9x` readiness passes now, defer their paired `BLG-FE-11x` implementation items to v7.4) was a direct, low-ambiguity application of a precedent already proven once — STEP 2 scope structuring required no fresh invention this time.
2. **All 7 scope candidates carried explicit day-range effort estimates**, continuing the pattern noted favourably in v7.2's own lessons learnt (Friction Item 1) — the §4.5 capacity check again needed zero inference.
3. **The out-of-band v7.3 roadmap-section formalization, done immediately before this invocation, is fully traceable** (DL-068, `BLG-GOV-240`) rather than silently absorbed — STEP -1.2 preflight could cite it directly without ambiguity about provenance.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Governed-Process Gap (structural, not a single-run mistake)

**Recurrence:** First occurrence of this specific failure mode, but directly caused by a previously-known limitation (`roadmap_prompt.md` STEP 8.1's condition 1 only covers a fully-empty Now horizon).

**What happened:** This engine's own STEP -1.2 preflight gate (target version must exist as a formal roadmap release section, or have a documented STEP 8.1 Option(b) decision) could not be satisfied by any governed engine. `roadmap_prompt.md` STEP 8.1 did not fire at `2026-07-16__scheduled` because the Now horizon was non-empty (3 unversioned carried-forward items already present) — even though the PO had already named the v7.3 anchor scope that same cycle. Neither engine's write scope covered the gap: the roadmap engine's own gate structurally couldn't trigger, and this engine's write scope (§7) only permits annotating an *existing* release section, not creating one. Resolved via an out-of-band write under Head of Specs Team authority, by analogy to `shared_standards.md` §17.

**Where in the routine:** STEP -1.2 (Verify Release Exists on the Roadmap).

**Root cause:** `roadmap_prompt.md` STEP 8.1 condition 1 ("Now horizon contains no committed items") does not account for the case where the Now horizon contains committed items that are carried forward *without* a version label — a state that a partial post-ship retirement can produce (as it did at `2026-07-15__release-v7.2`'s own post-ship closure, which explicitly left `BLG-FE-109/110/111` "un-versioned").

**Suggested fix:** Already filed as `BLG-GOV-240` (P2, Governance Process) with two concrete remediation options: (a) a `shared_standards.md` §17-style standing-authority extension for `current_roadmap.md` in this narrow scenario, or (b) amend `roadmap_prompt.md` STEP 8.1 condition 1 to also fire when the horizon is non-empty but unversioned.

**Target:** `BLG-GOV-240` — Head of Specs Team, no fixed date (P2, next available governance-hardening slot).

### Friction Item 2

**Classification:** Type C — Scope Structuring Judgment Call (positive pattern reuse, not a defect)

**Recurrence:** N/A — second confirming instance of the v7.2 EPIC-grouping approach (spec-pass-paired-with-implementation), not itself a new pattern.

**What happened:** As at v7.2, the roadmap's v7.3 Now-horizon table lists items in a flat table with no EPIC grouping. This engine again had to decide the grouping at STEP 3 — this time choosing to group the 3 ready UI items into one EPIC-01 (since none of them individually depend on any of the 4 readiness passes) rather than mirroring v7.2's one-EPIC-per-readiness-pair structure exactly, because in this cycle none of the 3 UI items pair with a same-cycle readiness pass (their own passes already shipped in v7.2).

**Where in the routine:** STEP 3 — Execution Plan (EPIC table construction).

**Root cause:** Same as v7.2 Friction Item 2 — roadmap Now-horizon annotation groups by originating idea-consolidation/carry-forward status, not by execution EPIC.

**Suggested fix:** No prompt change recommended — consistent with v7.2's own disposition on this same friction type.

**Target:** Advisory only — no action item filed.

---

## Monitoring Carried Forward

- Design gate required for ST-01/02/03 — confirm whether `run design-gate` cites the prior v7.2 Passed record (per RISK-01) or re-runs fully; either way, confirm the 3 items are covered.
- Capacity check landed with a thin 0.75d buffer (13.25d midpoint / 14d threshold) — directly the pattern this cycle's own Carry-Forward Advisory (v7.1/v7.2 zero-buffer lesson) warned about. Sprint Planning should treat `BLG-SPEC-92`/`BLG-SPEC-94` as live phasing candidates, not wait for a formal WARN that this PASS outcome didn't trigger.
- RISK-03 (`BLG-SPEC-92`'s §13 pre-check) is the one risk in this release that could produce a genuine blocking finding rather than just a documentation output — monitor its outcome before assuming `BLG-FE-116` is a safe v7.4 candidate.

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-GOV-240` (STEP 8.1 empty-horizon gate structural gap) is now filed and traceable, but not yet resolved. | Head of Specs Team to disposition at the next available governance-hardening opportunity — Apply now or Defer with owner + date, per the standard `roadmap_prompt.md` STEP 11.2 process, next time this engine's own STEP 11 runs (roadmap rebalance, not release planning). | Roadmap |
| 2 | Capacity check landed at 13.25d midpoint / 15.5d pessimistic — a thinner buffer than v7.2's 10.5d/15.5d, with the same absolute pessimistic ceiling. This is the second consecutive release-planning cycle to land close to the top of the capacity band. | Sprint Planning should treat the Phasing Recommendation as a live option early, per the standing v7.1/v7.2 carry-forward practice — this cycle makes it a 3rd consecutive release exhibiting the pattern. | Sprint Planning |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-16__release-v7.3",
  "phase": "Release",
  "filed_utc": "2026-07-16T15:40:00Z",
  "friction_item_count": 2,
  "action_now_count": 0,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
