Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-18

# Execution Escalations — 2026-08-17__release-v8.9

Append-only. Never edit a previous entry.

---

## ESC-EXEC-20260818-01

- **Raised at:** 2026-08-18T08:35:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-08-17__release-v8.9
- **Step:** 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-13 / EPIC-04
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-13 (BLG-QA-150) requires a Product Owner decision on treatment for `trade_plans.setup_type`, which currently has no server-side default or required-field guarantee outside the linked-signal pre-population path in `TradePlan.js`. Any creation path other than "ticker with a matching watchlisted signal" (manual entry, Ticker Universe, Research CTA with no matching signal, direct API use) saves `setup_type: null`, undercounting Arc 6/SI-02's future `win_rate_by_setup_type` analysis. Three treatment options are on the table: (a) make `setup_type` a required form field, (b) add an explicit "Unclassified"/"Other" default so null rows still group predictably, (c) accept as-is with documented rationale.
- **Owning authority:** Product Owner (co-consulted: Frontend Specifications & UX Documentation Owner, per BLG-QA-150's dual ownership and sprint_backlog.md's RISK-04 note)
- **Unblock criteria:** A decision recorded (one of the three options above, or a reasoned variant) with rationale; if a fix is chosen, implemented; Product Owner sign-off.
- **SLA due-by:** 2026-08-19T08:35:00Z (24h — Human-Delegation trigger)
- **Blocks execution:** No — EPIC-04's other stories (ST-12, ST-14, ST-15) proceed independently per execution_prompt.md §3.1.D step 4 ("Continue to next item").
- **Disposition:** Open
- **Resolution summary:** (to be completed on resolution)
