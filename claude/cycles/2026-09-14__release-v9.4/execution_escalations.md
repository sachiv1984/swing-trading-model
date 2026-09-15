Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-15

---

## ESC-EXEC-20260915-01

- **Raised at:** 2026-09-15T07:03:02Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-14__release-v9.4
- **Step:** STEP 3.1.D (EPIC-04)
- **ST/EPIC item:** ST-15 / EPIC-04
- **Trigger type:** Other
- **Blocking statement:** ST-15 (BLG-SPEC-138) requires an explicit placement decision — does Appendix D's governance-process metrics content belong in `docs/governance/` instead of `metrics_definitions.md` (a Class 1, API-facing canonical spec)? The AC names this as a joint decision for Product Owner + Metrics Definitions & Analytics Canonical Owner; it is a content-placement/governance-classification question, not a UI design decision (design gate already confirmed Design Not Applicable) and not reviewable against existing documented criteria the engine can apply agent-mediated sign-off to per §5.3 — it is genuinely undecided which class of document Appendix D belongs in.
- **Owning authority:** Product Owner; Metrics Definitions & Analytics Canonical Owner
- **Unblock criteria:** Product Owner and Metrics Definitions & Analytics Canonical Owner record an explicit placement decision (keep in `metrics_definitions.md` as-is, or relocate Appendix D to `docs/governance/`). If relocation is chosen, the content move itself still needs to happen before ST-15 can be marked done.
- **SLA due-by:** 2026-09-16T07:03:02Z (24h, Lifecycle/Process default — no Strategy-boundary question is in play)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:** _(complete when closing)_

---

## ESC-EXEC-20260915-01 — Resolution

- **Resolves:** ESC-EXEC-20260915-01 (ST-15 — Review placement of Appendix D governance metrics in `metrics_definitions.md`, EPIC-04). Appended as a new entry rather than editing the original (append-only per this file's header) — original entry above is left unmodified.
- **Resolved by:** Product Owner + Metrics Definitions & Analytics Canonical Owner (acting, explicit user direction to resolve in these roles' capacity)
- **Resolved at:** 2026-09-15T09:00:00Z
- **What was decided:** Governance-process metrics content (PVR rolling-window handling, Skill-Silo taxonomy) stays in `metrics_definitions.md` Appendix F — no relocation to `docs/governance/`. Full reasoning: `docs/product/decisions/decisions--2026-09-14__release-v9.4--ST-15-appendix-f-governance-metrics-placement.md`. Cross-referenced from Appendix F's own scope note in the same commit.
- **Status:** Resolved — `execution_state.json` ST-15 set to `done` in the same commit as this entry.
