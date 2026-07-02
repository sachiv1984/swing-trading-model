**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Seeded (to be completed at Post-Ship Closure)
**Cycle:** 2026-07-02__release-v6.4
**Last Updated:** 2026-07-02

---

# Lessons Learnt — Release Planning v6.4

## Planning Phase Observations

### LP-01 — Overdue friction items resolved by folding into existing scope, not re-carrying

FI-P4-01 and FI-P3-02 had each already missed one full re-target cycle (v6.3), and FI-P3-01 had missed two. Rather than re-carrying all three forward a third time with a fresh "action during sprint execution" note (the pattern that produced the overdue state in the first place — see v6.3's own LP items, which carried these same three items forward), this cycle folded all three into `BLG-GOV-152`'s (ST-06) concrete acceptance criteria. A carry-forward note with no owning story is structurally easy to drop; an AC on a scheduled story is not.

**Monitor:** At post-ship closure, confirm ST-06 actually closes all three (AC-02, AC-03, AC-05) rather than the FI items silently detaching from the story again.

### LP-02 — Lifecycle audit remediation absorbed as governance-load counterweight to a Skill-Silo Alert

The 2026-07-01__scheduled rebalance flagged a Skill-Silo Alert (governance load 53.2%, above the 40% ceiling) and surfaced `BLG-FEAT-54` as the pull-forward candidate. Rather than treating the audit's 4 remediation items (BLG-GOV-150/151/152/153) as a separate governance-heavy release, this cycle bundled them alongside `BLG-FEAT-54` and 4 other execution items in the same release, landing governance load at ≈38% of estimated effort — back within the healthy band without deferring the audit fixes.

**Monitor:** At post-ship closure, check whether the rolling-3-cycle Skill-Silo average returns below 40% following this release, confirming the bundling approach is an effective corrective, not just a one-cycle read.

### LP-03 — Design Gate scope (3 items) — third consecutive shrinking count

v6.2 design gate covered 5 stories; v6.3 covered 3; v6.4 also covers 3 (BLG-FEAT-54, BLG-UX-01, BLG-UX-02). This continues v6.3's LP-03 observation ("smaller design gate scope suggests more efficient design gate sessions are possible at lower item counts") — this is now the second data point at the 3-item scope. This directly informs the carried-forward DF-08 item (track design gate session efficiency at 3-item vs 5-item scope).

**Monitor:** Compare v6.4's design gate session duration/output quality against the v6.3 3-item session to build a proper efficiency comparison (DF-08).

### LP-04 — Standing AI safety checklist proposal remains un-actioned for a second cycle

v6.3's LP-04 raised "consider whether a standing AI safety checklist would eliminate the need to re-derive [the AI security] cluster at each release" and this was carried forward as DF-09 (Owner: PMO Lead) into v6.4 planning. This cycle's AI-adjacent security items (BLG-SEC-01, BLG-SEC-02) were derived individually again from the ST-04 risk assessment rather than from a standing checklist. DF-09 was not actioned this session (no scope item currently covers it).

**Monitor:** If a third consecutive release derives AI/security scope items ad hoc rather than from a standing checklist, escalate DF-09 from advisory to a scoped backlog item at the next release planning.

---

## Action Items (to be completed at Post-Ship Closure)

| ID | Source | Summary | Classification | Owner | Target |
|----|--------|---------|----------------|-------|--------|
| LP-01 | Release Planning | FI-P3-01/FI-P3-02/FI-P4-01 folded into ST-06 ACs — confirm all three actually close | monitoring | Head of Specs Team | Post-ship |
| LP-02 | Release Planning | Audit remediation + feature pull-forward as Skill-Silo corrective — monitor rolling average | monitoring | PMO Lead | Post-ship |
| LP-03 | Release Planning | Design gate 3-item scope (2nd consecutive) — feeds DF-08 efficiency comparison | monitoring | PMO Lead | Post-ship |
| LP-04 | Release Planning | Standing AI safety checklist (DF-09) still un-actioned — 2nd cycle | monitoring | PMO Lead | Post-ship |

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle": "2026-07-02__release-v6.4",
  "release": "v6.4",
  "status": "seeded",
  "completed_at": ""
}
