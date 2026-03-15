**Owner:** Facilitator
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-15

---

# Stage 4 — Structured Debate

**Cycle:** 2026-03-15__item-5.3
**Date:** 2026-03-15
**Facilitator:** Facilitator persona
**Challenger:** Challenger persona

---

## Agenda

Single motion for debate:

**Motion A:** Kill 4.1c (Server-Side PDF Report) and Add BLG-OPS-01 (Development Environment) to the roadmap at v1.10.

---

## Pre-Debate Setup

**Net-zero check:** 1 Add (BLG-OPS-01) requires 1 Kill (4.1c). Net-zero satisfied if motion passes.

**STEP 8.6 guardrail check:**
- BLG-OPS-01 is an infrastructure/operations item (SPS 1). Not an AI Artefact Traceability or adjacent governance expansion item. STEP 8.6 (AI Artefact Traceability guard) is not triggered.

**Standing displacement candidate:** 4.1c has been explicitly noted as the standing displacement candidate since DL-005 (2026-03-04). This is not a surprise Kill.

---

## Motion A Debate — Kill 4.1c / Add BLG-OPS-01

### Proposer: Product Owner

**Case for Kill 4.1c:**
1. 4.1c (Server-Side PDF) was always the lowest-value item on the roadmap. The problem it solves — browser-print inconsistency — is a UX inconvenience, not a correctness or governance issue.
2. PDF output is not a daily workflow item. Users access the analytics page for operational decisions; PDF export is a periodic reporting task with low urgency.
3. Browser-print is functional. Not ideal, but not broken. Users are not blocked.
4. Since DL-005 this item has been explicitly documented as the natural displacement candidate. The time has come.

**Case for Add BLG-OPS-01:**
1. The absence of a development environment is not a nice-to-have gap — it is a structural failure in the QA governance process.
2. The Director of Quality sign-off rule requires testing a live running application. Currently, that means testing production. This is not acceptable risk management.
3. v1.9 Sprint 2 demonstrated the cost: a bug was discovered post-merge because no pre-merge environment existed. Post-merge bug discovery in production is the QA failure mode we most need to prevent.
4. BLG-OPS-01 is P1 in the backlog for this reason. It must be elevated to roadmap to ensure it gets capacity commitment in v1.10 planning, not squeezed out by feature work.
5. Effort is well-understood (CI/CD pipeline extension, staging environment provisioning). No canonical spec dependency. Can begin immediately once v1.10 planning opens.

---

### Challenger: Challenger persona

**Challenge to Kill 4.1c:**

*Counter-argument:* There may be a future where a PDF is the primary stakeholder artefact — e.g. if the product is used by a small fund reporting to LPs. Killing 4.1c now removes that path.

*Counter-counter-argument (Proposer):* The product is explicitly single-user (strategy_rules.md §2). Multi-stakeholder reporting is in the deferred/excluded category. This argument does not apply to the current product definition. A future multi-user product would require a full §13 boundary review anyway.

*Challenger verdict:* Challenge withdrawn. 4.1c Kill is supportable given the product's current strategic boundaries.

**Challenge to Add BLG-OPS-01:**

*Counter-argument 1:* BLG-OPS-01 is infrastructure, not a user-facing feature. Roadmap items should be user-visible value. Should BLG-OPS-01 remain a backlog-only item?

*Proposer response:* Roadmap items are not restricted to user-facing features. BLG-NEW-01/02/05/07/08 (CI infrastructure) and TEST-GAP-EPIC-01 (QA infrastructure) were all roadmap-eligible. The distinction is whether the item requires dedicated capacity commitment to land. A staging environment requires cross-cutting work (CI/CD changes, hosting provisioning, process updates) that will not happen without explicit roadmap commitment.

*Counter-argument 2:* Is the effort estimate reliable? Infrastructure provisioning can balloon.

*Proposer response:* Scope is well-defined: staging environment that mirrors production, CI/CD auto-deploy on merge to main. The hosting model already exists (production); replicating it for staging is a configuration task, not a novel engineering challenge. Risk of ballooning is low. If effort expands, release planning will surface this — not a reason to block roadmap inclusion.

*Challenger verdict:* Both challenges answered satisfactorily. BLG-OPS-01 Add is supportable.

---

### Facilitator Summary

**Motion A outcome:** ✅ APPROVED — unanimous (Proposer advanced, Challenger challenges withdrawn)

**Net-zero satisfied:** 1 Kill (4.1c) + 1 Add (BLG-OPS-01) = 0 net change ✅

**Decision log entry required:** DL-008 (Kill 4.1c + Add BLG-OPS-01)

---

## Additional Disposition (No Debate Required — Housekeeping)

**BLG-NEW-13 (Spec Coverage Inventory):** Advance to backlog from idea pool. Backlog-level addition only — no roadmap-level displacement required. No debate needed.

**Idea pool bulk re-park:** 30 Parked ideas → Parked-cycle-2. 12 stale Advancing/Promoted → Promoted-Added. Housekeeping; no debate needed.

---

## Scored Initiatives (Post-Debate)

| Initiative | SPS | Roadmap Status | Action |
|-----------|-----|----------------|--------|
| 3.5 Alerts & Notifications | 3 | Deferred (v2.0 gate pending) | Confirm defer |
| 4.1b Tax-Year P&L | 1 | Active (v2.0) | Continue |
| 4.1c Server-Side PDF | 1 | **Killed** | DL-008 |
| BLG-OPS-01 Dev Environment | 1 | **Added (v1.10)** | DL-008 |
| 4.3 Signal Exposure | 4 | Active (v2.0 planning) | Continue — PoG valid |
| 4.2 Watchlists | 2 | Priority 2 | Hold |
| Chart Interactivity | 2 | Priority 2 | Hold |
