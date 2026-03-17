**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-17

---

# Stage 4 — Structured Debate (Zero-Sum)

**Cycle:** 2026-03-17__item-v1.10
**Date:** 2026-03-17
**Authorities:** Product Owner (chair) + Challenger (non-decision challenge)

---

## Pre-Debate Anchoring (STEP 5)

*Per roadmap_prompt.md §5 requirement — Facilitator restates top 2 constraints most likely to block "easy yes":*

1. **Zero-sum displacement rule (mode-independent — IMP-33):** Any roadmap-level Add requires a named Kill of equal or greater value. This applies in both strict and standard mode. It is a governance constraint, not a UX preference.

2. **§13.2 boundary enforcement (4.3 scope constraint):** Only `top_n` and `lookback_days` are cleared by PoG POG-20260304-01. Any parameter beyond these two requires a new §13 review. The Challenger must lead with a §13-referenced counter-argument for any candidate touching signal or strategy scope.

---

## STEP 5.0 Pre-Debate Gate Checks

**A) PoG validity check:**
- POG-20260304-01 (item 4.3): references strategy_rules.md v1.3. Current version: v1.3. **PoG is valid.** ✅

**B) Score-5 presence check:**
No candidate in this debate round has a Strategy Proximity Score of 5. Highest SPS is 4 (item 4.3, ongoing — not a new debate candidate). No Score-5 items in STEP 5 debate. ✅

---

## Debate — Candidate 1: Production Deployment Runbook

**Idea:** IDEA-infra-ops-20260304-01
**Backlog-level candidate** (not roadmap-level — no displacement required)

### 5.0 Required Case (Product Owner):
1. **Problem:** v1.10 shipped the staging environment (BLG-OPS-01), but there is no documented procedure for deploying to production. The deployment process is informal — an undocumented developer workflow. With staging now separate from production, the deployment runbook bridges the two environments with a repeatable, governed process.
2. **Strategy intent served:** §4 (operational reliability) — a production deployment runbook directly supports system availability and reduces risk of a production incident from an undocumented deployment step.
3. **What if we don't do it:** The staging environment's value is partially unrealised. A developer could deploy incorrectly and there would be no documented recovery path. This is a structural operational gap, not a UX inconvenience.
4. **Displacement:** Not applicable — backlog-level addition. Per DL-005/DL-006 precedent, backlog items do not require roadmap-level stops.

### 5.1 Challenger Counter-Argument:
**Challenger position:** Clearance Statement
**Evidence reviewed:** strategy_rules.md §4 (operational reliability), §13 (system boundaries — no contact). Backlog-level addition with no roadmap displacement required.
**Clearance:** "Cleared — strategy_rules.md §4 supports operational reliability investment. §13 is not engaged; this is a documentation item with no impact on strategy execution. No economic constraint violated — effort is S (1–2 days documentation). No governance concern."

### 5.2 Product Owner Response:
Product Owner confirms ✅ Advance. Challenger clearance accepted. Backlog-level addition (BLG-OPS-02).

---

## Debate — Candidate 2: Positions Table Data Dictionary

**Idea:** IDEA-data-model-owner-20260304-01
**Backlog-level candidate**

### 5.0 Required Case (Product Owner):
1. **Problem:** The positions table has no formal data dictionary defining field-by-field semantics, constraints, and derivation rules. BLG-BE-01 (GET /portfolio missing 4 fields) surfaced in v1.10 — a spec/implementation divergence that could have been caught earlier with better data documentation. A data dictionary provides the authoritative reference for field naming, types, and derivation.
2. **Strategy intent served:** System integrity — canonical data definitions prevent implementation drift. BLG-BE-01 is the direct evidence.
3. **What if we don't do it:** Continued risk of spec/implementation divergence (BLG-BE-01 pattern). Fields get added to the backend without canonical reference. Integration tests may miss field-level requirements.
4. **Displacement:** Not applicable — backlog-level.

### 5.1 Challenger Counter-Argument:
**Challenger position:** Counter-argument (Type A)
**Evidence:** BLG-NEW-13 (Spec Coverage Inventory) is already in the backlog and targeted at v2.0. The Spec Coverage Inventory will produce a cross-spec coverage map. Advancing a Positions Table Data Dictionary risks creating overlapping documentation work and splitting attention between two complementary spec tasks.
**Challenger position:** Park
**Reason:** BLG-NEW-13 covers the spec coverage intent at the system level. A data dictionary is a lower-level artefact — until BLG-NEW-13 identifies positions data documentation as the highest-priority gap, advancing this idea creates premature specialisation.
**Consequence:** If advanced now, the Data Dictionary and BLG-NEW-13 may produce inconsistent coverage approaches, requiring later reconciliation.

### 5.2 Product Owner Response:
**Rebuttal accepted — with scope distinction:** The Challenger's concern is valid at the surface level, but the two artefacts serve different purposes. BLG-NEW-13 is a coverage audit (which spec sections are tested/untested). A Positions Table Data Dictionary is a canonical field-level reference (what each field means, its type, constraints, and derivation). These are complementary, not overlapping. BLG-BE-01 is the specific evidence that field semantics are under-documented — that gap is what the data dictionary addresses. BLG-NEW-13 would identify the gap but not fill it.

**Decision: ✅ Advance.** Scope constrained: the Positions Table Data Dictionary covers the `positions` table fields only (not all tables), as a Class 2 Supporting document. BLG-NEW-13 proceeds independently as the coverage audit. The two are complementary.

---

## Debate — Candidate 3: Database Migration Governance Standard

**Idea:** IDEA-backend-engineering-20260304-02
**Backlog-level candidate**

### 5.0 Required Case (Product Owner):
1. **Problem:** No documented process exists for how database schema migrations are created, reviewed, applied, and rolled back. The current practice is undocumented. With v2.0 adding new features (4.1b Tax-Year P&L will require schema changes for a new report table), database governance is now timely.
2. **Strategy intent served:** Operational safety — §4 operational reliability. A migration governance standard prevents the class of incident where a partial migration leaves the database in an inconsistent state.
3. **What if we don't do it:** v2.0 schema changes proceed without a documented review or rollback process. If a migration fails mid-apply, there is no documented recovery path.
4. **Displacement:** Not applicable — backlog-level.

### 5.1 Challenger Counter-Argument:
**Challenger position:** Clearance Statement
**Evidence reviewed:** strategy_rules.md §4 (operational reliability), §13 (no contact — pure governance documentation). Low effort (S — days). No economic constraint violated.
**Clearance:** "Cleared — §4 operational reliability applies directly. §13 is not engaged. Effort is bounded (S). The timing rationale (v2.0 schema changes incoming) is sound evidence. No governance concern."

### 5.2 Product Owner Response:
✅ Advance. Challenger clearance accepted. Backlog-level addition (BLG-TECH-07).

---

## Debate — Candidate 4: Lessons Learnt Action Item Register

**Idea:** IDEA-pmo-lead-20260304-01
**Backlog-level candidate**

### 5.0 Required Case (Product Owner):
1. **Problem:** Deferred patches from lessons learnt are tracked in individual lessons_learnt.md files per cycle, making it difficult to see outstanding actions across cycles. The proposal: a centralised register (`claude/cycles/action_register.md`) tracking all open deferred patches and lessons learnt actions with owner, target date, and status.
2. **Strategy intent served:** Process governance quality — reduces the risk of deferred patches being lost or carried forward beyond STEP -1.5 grace period.
3. **What if we don't do it:** Deferred patches may be missed (as happened with LL-02 in prior cycles before LL-02-patch was formalised).
4. **Displacement:** Not applicable — backlog-level.

### 5.1 Challenger Counter-Argument:
**Challenger position:** Counter-argument (Type B)
**Evidence:** BLG-GOV-01 (Roadmap stage document consolidation) and BLG-GOV-02 (Ideas register redesign) are already in the backlog and targeted at v2.0 governance prep. These two items already constitute a significant governance improvement workload for the Head of Specs Team. Advancing a third governance process item risks creating a governance workload spike in v2.0 that delays the actual product features (4.1b, 4.3). Additionally, the STEP -1.5 mechanism in roadmap_prompt.md already provides a structured deferred patches check — a separate register may duplicate this rather than improve it.
**Challenger position:** Park
**Reason:** Head of Specs Team capacity is committed to BLG-GOV-01 and BLG-GOV-02 for v2.0. Adding a third governance improvement item before those are resolved increases governance workload without proportionate benefit — the existing STEP -1.5 mechanism is functional.
**Consequence:** If advanced, Head of Specs Team governance capacity in v2.0 may be insufficient to complete BLG-GOV-01 and BLG-GOV-02 alongside the action register, delaying all three.

### 5.2 Product Owner Response:
**Challenger argument accepted.** BLG-GOV-01 and BLG-GOV-02 are already the right governance improvement investments for v2.0. The STEP -1.5 mechanism does provide a functional (if manual) deferred patches check. Advancing a third governance item at the same time creates a sequencing risk for the Head of Specs Team.

**Decision: 🅿 Park.** Status: Promoting → Promoted-Rejected (debated at STEP 5, PO accepted argument). If BLG-GOV-01 and BLG-GOV-02 deliver the register redesign (BLG-GOV-02), an action item register may become naturally integrated into the ideas register redesign scope. Revisit after BLG-GOV-01/02 close.

---

## STEP 8.6 Guardrail Check

Rule: guardrail passes if ANY of the following is true:
1. At least one candidate was classified 🅿 Parked or ❌ Rejected: **YES** — Candidate 4 (Lessons Learnt Action Item Register) was Parked at STEP 5. ✅

**Guardrail passes. No pivot loop required.**

---

## Summary of STEP 5 Outcomes

| Candidate | STEP 4 Classification | STEP 5 Outcome | Notes |
|-----------|----------------------|----------------|-------|
| Production Deployment Runbook (IDEA-infra-ops-20260304-01) | ✅ Advance | ✅ Advance | Challenger cleared. BLG-OPS-02. |
| Positions Table Data Dictionary (IDEA-data-model-owner-20260304-01) | ✅ Advance | ✅ Advance | PO rebutted overlap concern; scope constrained to positions table only. BLG-DATA-01. |
| Database Migration Governance Standard (IDEA-backend-engineering-20260304-02) | ✅ Advance | ✅ Advance | Challenger cleared. BLG-TECH-07. |
| Lessons Learnt Action Item Register (IDEA-pmo-lead-20260304-01) | ✅ Advance | 🅿 Park (PO accepted Challenger) | Promoted-Rejected. Revisit after BLG-GOV-01/02. |

---

## Hard Gates — None Active

No advancing candidate carries an uncleared hard gate. No PoG issuance required this cycle (the 4.3 PoG POG-20260304-01 is from a prior cycle and remains valid — no new PoG needed).
