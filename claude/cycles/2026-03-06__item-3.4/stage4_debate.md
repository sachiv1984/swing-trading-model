**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-06

---

# Stage 4 — Structured Debate

**Cycle:** 2026-03-06__item-3.4
**Date:** 2026-03-06
**Authorities:** Product Owner (chair), Challenger (non-decision challenge)

---

## Pre-Debate Context Re-Anchoring

Constraints most likely to block an "easy yes":
1. **No addition without displacement** — Stops ≥ Adds at roadmap level. All candidates this cycle are backlog-level items only. No roadmap-level displacement required, but capacity competition with v1.9 core scope (5.1, 5.2, 5.3, BLG-FEAT-08, BLG-RD items) is real.
2. **§13.2 configurable strategy builder boundary** — no candidates this cycle touch signal parameters or strategy execution logic. Not the primary risk in this debate.

---

## STEP 5.0 Pre-Debate Gate Checks

**A) PoG validity check:**
- All candidates this cycle are newly advancing ideas (carry-forwards from IW-20260304-01). No prior PoG documents exist for any of these candidates.
- PoG POG-20260304-01 (item 4.3) is valid (strategy_rules.md still at v1.3) — but 4.3 is not a candidate this cycle. No PoG validity issue.

**B) Score-5 presence check:** No Score-5 candidates. No Score-4 candidates this cycle. Standard Challenger arguments apply; no §13-specific lead required.

---

## Candidates Evaluated

1. IDEA-metrics-analytics-20260304-01 — R-Multiple Distribution Report
2. IDEA-qa-testing-20260304-01 — Canonical Test Scenario Library
3. IDEA-head-of-specs-20260304-01 — Canonical Terms Glossary
4. IDEA-backend-engineering-20260304-01 — Service Layer Test Coverage Standard
5. IDEA-cybersecurity-20260304-01 — System Threat Model Document

---

## Candidate 1: R-Multiple Distribution Report

### 5.0 Required Case (Product Owner)

1. **Problem:** The analytics page shows P&L and drawdown but has no visualisation of R-multiple distribution across closed trades. R-multiple (profit in units of initial risk) is the canonical measure of trade quality in this strategy — yet users cannot see whether their trades are performing at R > 1 or R < 1 on average.
2. **Strategy intent served:** §2 — "Capture medium- to long-term momentum trends; defend profits aggressively once momentum is confirmed." R-multiple directly measures whether the strategy's core intent is being executed — are profits large enough relative to losses? §11 — consistent analytics must be available.
3. **What if we don't:** Users cannot self-assess trade quality against the strategy's core expectation (R > 1 on winning trades). Discipline gaps go unseen.
4. **Displacement:** No roadmap displacement — this is a backlog-level analytics feature for the analytics page (existing page). Can be scoped as an extension to the Performance Analytics page (item 3.1, delivered v1.5). No roadmap-level stop required.

### 5.1 Challenger Counter-Argument

**Challenger position:** Park

**Evidence:** §2 — the strategy governs trade selection and exit rules; it does not prescribe R-multiple as a required analytics metric. The metrics_definitions.md (v1.6.0) would need to be updated to canonicalise R-multiple before any display is authoritative — that is pre-work that competes with BLG-FEAT-08 (Metrics Definitions owner already committed to compliance metrics as the v1.9 pre-work gate for 5.1).

**Reason:** The Metrics Definitions & Analytics Owner is the capacity constraint. BLG-FEAT-08 (compliance metrics definitions) is the v1.9 gate for 5.1. Adding R-multiple definitions in the same cycle creates concurrent demand on the Metrics Definitions owner — specifically, two separate metrics canonicalisation tasks before implementation of either. This risks BLG-FEAT-08 being delayed, which would delay 5.1.

**Consequence:** R-multiple report implementation begins without canonical definition, creating spec debt immediately. Or BLG-FEAT-08 is delayed, breaking the v1.9 gate sequence for 5.1.

### 5.2 Product Owner Response

Rebut. The Challenger correctly identifies the Metrics Definitions owner capacity constraint. However, R-multiple is already computable from existing trade data (profit / initial_risk) — the formula is deterministic and the data is available. The Metrics Definitions owner task for R-multiple is definitional (one metric, one formula, one section in metrics_definitions.md) — much smaller than BLG-FEAT-08 (three new metrics with operational definitions). The LL-05 capacity check (metrics owner availability) applies to v1.9 pre-alignment: if the owner is available for BLG-FEAT-08, the marginal cost of R-multiple definition is small. Sequence: (1) BLG-FEAT-08 definition first, (2) R-multiple definition second. If Metrics owner unavailable, R-multiple defers automatically — but that is a v1.9 release planning decision, not a rebalance block. Advance to backlog. Release planning determines v1.9 slice.

**Outcome: ✅ Advance** — promoted to backlog as BLG-NEW-09. Constraint: Metrics Definitions owner must define R-multiple in metrics_definitions.md before implementation. Sequence constraint: after BLG-FEAT-08 definitions.

---

## Candidate 2: Canonical Test Scenario Library

### 5.0 Required Case (Product Owner)

1. **Problem:** Test scenarios are currently ad-hoc per feature (e.g., risk_dashboard_scenarios.md was created for v1.8, but no systematic library covers all canonical endpoints and user-facing behaviours). TEST-GAP-EPIC-01 highlights that 17 Risk Dashboard scenarios cannot be executed — a canonical library with infrastructure preconditions would prevent this gap recurring.
2. **Strategy intent served:** §14 — "if a rule can change outcomes, it must be explicit, intentional, and owned." Canonical test scenarios make the acceptance criteria machine-verifiable and owned. The golden output baseline (BLG-NEW-01, now COMPLETE) covers calculation correctness — this covers behavioural acceptance.
3. **What if we don't:** Every release will discover scenario coverage gaps during delivery verification. The TEST-GAP-EPIC-01 pattern recurs indefinitely.
4. **Displacement:** Backlog-level QA infrastructure task. No roadmap displacement. Extends existing QA scenario work.

### 5.1 Challenger Counter-Argument

**Challenger position:** Park

**Evidence:** §14 — canonical specs already define acceptance criteria. Per document_lifecycle_guide.md §8, the QA & Testing Owner owns test scenario documents (Class 1 Canonical). Building a library is the right structure — but the golden baseline (BLG-NEW-01) was scoped to stop/sizing calculations only, and the test scenario library scope is undefined (all endpoints? all user-facing features?).

**Reason:** Without a defined scope boundary, a "canonical test scenario library" is an open-ended commitment. All 30+ endpoints could be in scope. The effort estimate jumps from days to weeks if taken to its logical conclusion. An undefined scope advancing to the backlog will be treated as a full-coverage mandate.

**Consequence:** Engineering and QA time is absorbed into an unbounded library task, delaying v1.9 user value delivery.

### 5.2 Product Owner Response

Accept partial concern. The Challenger's scope concern is valid. Modify: advance with an explicit scope constraint. The Canonical Test Scenario Library is scoped to: (1) all Risk Dashboard components (addresses TEST-GAP-EPIC-01 directly), (2) the Position Sizing Calculator (BLG-NEW-01 prerequisite area), and (3) any new feature delivered in v1.9. It does NOT require backfilling scenarios for all historical endpoints. Scope is additive per release, not retroactive. This is a manageable commitment. Advance with scope constraint.

**Outcome: ✅ Advance** — promoted to backlog as BLG-NEW-10. Scope constraint: Risk Dashboard scenarios first (resolves TEST-GAP-EPIC-01 infrastructure dependency); new v1.9 feature scenarios added at release time; no retroactive full-coverage mandate.

---

## Candidate 3: Canonical Terms Glossary

### 5.0 Required Case (Product Owner)

1. **Problem:** Terms like "portfolio heat", "grace period", "stop distance", "R-multiple", "trailing stop" are used across multiple specifications without a single canonical definition point. When specs are authored independently, term interpretations drift (e.g., "stop distance" as absolute value vs percentage). The v1.8 delivery verification revealed terminology ambiguity in risk_dashboard.md (§4.1 drawdown data source — BLG-RD-08).
2. **Strategy intent served:** §14 — "if a rule can change outcomes, it must be explicit, intentional, and owned." Terms that appear in canonical specs affect decisions — they must be defined once. Head of Specs Team charter: "domain spec ecosystem governance."
3. **What if we don't:** Term drift continues. BLG-RD-08-class ambiguities recur in every new spec. Spec authors use different definitions without realising it.
4. **Displacement:** Governance document task. ~1 day effort. No roadmap displacement.

### 5.1 Challenger Counter-Argument

**Challenger position:** Park

**Evidence:** strategy_rules.md §2 defines strategy intent; metrics_definitions.md defines all analytical metrics canonically. Both are Class 1. A separate glossary creates a third authoritative source for some of the same definitions — violating the "single source of truth" principle in document_lifecycle_guide.md §1.

**Reason:** If R-multiple is defined in metrics_definitions.md AND in a glossary, and they ever diverge, there are two Class 1 documents in conflict. The governance system is designed to prevent exactly this. A glossary risks fragmenting canonical truth.

**Consequence:** Two canonical sources for the same term. Head of Specs Team must resolve conflicts. Governance overhead increases rather than decreases.

### 5.2 Product Owner Response

Rebut. The Challenger's concern is about conflicting canonical sources — a real risk, but solvable by design. The glossary is NOT a second canonical source for metric formulas. It is a reference for term usage: what does "portfolio heat" mean when used in a spec? Answer: "as defined in metrics_definitions.md §X." The glossary is a cross-reference index, not a formula owner. Document class: Class 2 — Supporting, referencing Class 1 canonical documents as its source. It adds no new canonical rules — it points to them. This design explicitly prevents the "two canonical sources" concern. Advance with Class 2 classification constraint.

**Outcome: ✅ Advance** — promoted to backlog as BLG-NEW-11. Design constraint: document class must be Class 2 (Supporting), referencing Class 1 sources for all definitions. Head of Specs Team is owner. No new canonical rules may be introduced — only cross-references.

---

## Candidate 4: Service Layer Test Coverage Standard

### 5.0 Required Case (Product Owner)

1. **Problem:** The golden output baseline (BLG-NEW-01, COMPLETE) covers end-to-end calculation correctness. But the service layer (portfolio_service.py, trade_service.py, analytics_service.py) has no documented test coverage standard. Business logic at the service layer is the most critical code path — errors here produce wrong stop recommendations without being caught by the API-level golden tests.
2. **Strategy intent served:** §7.3 — "Stops must never move downwards. This rule is absolute." Service layer standards enforce that this rule is tested at the correct layer. §14 — explicit and owned. A standard is the mechanism of ownership.
3. **What if we don't:** Service layer test coverage remains ad-hoc. The golden baseline catches output errors but not logic errors that happen to produce the same output on golden inputs.
4. **Displacement:** Standards document. ~0.5 day. No roadmap displacement. Prerequisite (golden baseline BLG-NEW-01) now COMPLETE.

### 5.1 Challenger Counter-Argument

**Challenger position:** Park

**Evidence:** §13.1 — "a deterministic decision-support engine." The current service layer IS deterministic and already tested by the POST /validate/calculations endpoint (14 validated metrics) and now BLG-NEW-01 golden baseline. Adding a standard prescribes HOW engineers write tests — which is engineering judgement, not governance.

**Reason:** A coverage standard without enforcement tooling (e.g., coverage thresholds in CI) is a document that gets written once and ignored. If it cannot be enforced automatically, it creates documentation debt rather than quality improvement.

**Consequence:** Engineering overhead in maintaining a standard; no improvement in actual test coverage without a CI enforcement step.

### 5.2 Product Owner Response

Rebut. The Challenger raises a valid enforcement concern. Modify: the Service Layer Test Coverage Standard must include a minimum coverage threshold requirement that is verifiable in CI (e.g., pytest-cov with a minimum % threshold on the services/ directory). This is not just a document — it is a document + CI gate definition. The engineering judgement argument is noted but the concern is: without a defined standard, coverage gaps are not discovered until they cause production errors. The standard is the prompt that triggers the CI step definition. Advance with the CI enforcement constraint.

**Outcome: ✅ Advance** — promoted to backlog as BLG-NEW-12. Constraint: standard must include a minimum coverage threshold enforced via CI (pytest-cov or equivalent); document alone without CI enforcement is incomplete.

---

## Candidate 5: System Threat Model Document

### 5.0 Required Case (Product Owner)

1. **Problem:** No threat model exists. The system handles real financial data (entry prices, stop levels, P&L) and is hosted on internet-accessible infrastructure (GitHub Pages, FastAPI). Threat models are foundational security artefacts — without one, there is no systematic basis for evaluating security controls.
2. **Strategy intent served:** §13.1 — "a deterministic decision-support engine" handling financial data. System integrity is a foundational requirement.
3. **What if we don't:** Security controls are evaluated on an ad-hoc basis. A compromised or exploited system could expose or corrupt financial decision data without a prior analysis of attack surfaces.
4. **Displacement:** Medium-effort security document. No roadmap displacement.

### 5.1 Challenger Counter-Argument

**Challenger position:** Park

**Evidence:** §13.2 — "not a real-time streaming or execution system." §13.2 — "single-user." The attack surface of a single-user, non-execution system is materially smaller than a multi-user trading platform. The dependency vulnerability scan (BLG-NEW-05, COMPLETE) already addresses the primary software supply chain risk. Threat modelling is highest value when: (a) multiple users are at risk, (b) the system executes trades automatically, or (c) a new infrastructure decision expands the attack surface.

**Reason:** The v1.9 cycle is capacity-constrained with Risk Dashboard deviation fixes (BLG-RD-01–11, TEST-GAP-EPIC-01) plus four user-value features (5.1, 5.2, 5.3, BLG-FEAT-08). A medium-effort security artefact without a specific triggering security event competes directly with user value delivery and deviation resolution. The Cybersecurity & Trust Lead recommended "park for security-focused cycle" — this cycle is not security-focused.

**Consequence:** User value delivery delayed; deviation fixes delayed; threat model produced in a cycle where no infrastructure change is occurring — producing a document that will need immediate revision when infrastructure changes do happen.

### 5.2 Product Owner Response

Accept. The Challenger's argument is well-reasoned: (1) no new infrastructure trigger event has occurred, (2) v1.9 is not security-focused, and (3) capacity is constrained by v1.8 deviation resolution and core v1.9 user value. The threat model remains high-value and should be scheduled for a cycle where an infrastructure decision or multi-user consideration is the trigger. Park: reassess when a new infrastructure change (e.g., deployment to cloud infrastructure, webhook endpoints, or external API consumption) provides the triggering event. Keep in submissions for the next cycle.

**Outcome: 🅿 Park** — retained in submissions. Trigger for advancement: infrastructure change, new external dependency, or explicit security-focused cycle.

---

## STEP 8.6 Guardrail Check

Candidates evaluated: 5
- ✅ Advance: 4 (Candidates 1–4)
- 🅿 Park: 1 (Candidate 5 — System Threat Model)

Guardrail: at least one must be 🅿 Parked or ❌ Rejected. **SATISFIED** (Candidate 5 Parked). No Pivot Loop required.

---

## Outcomes Summary

| Candidate | STEP 5 Outcome | Backlog ID | Notes |
|-----------|---------------|------------|-------|
| R-Multiple Distribution Report | ✅ Advance | BLG-NEW-09 | Sequence after BLG-FEAT-08 definitions |
| Canonical Test Scenario Library | ✅ Advance | BLG-NEW-10 | Scoped to Risk Dashboard + new v1.9 features only |
| Canonical Terms Glossary | ✅ Advance | BLG-NEW-11 | Class 2 (Supporting); no new canonical rules |
| Service Layer Test Coverage Standard | ✅ Advance | BLG-NEW-12 | Must include CI-enforceable coverage threshold |
| System Threat Model Document | 🅿 Park | — | Trigger: infrastructure change or security-focused cycle |
