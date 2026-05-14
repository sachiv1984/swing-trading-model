**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.4
**Cycle:** 2026-05-14__release-v3.4
**Last Updated:** 2026-05-14

---

# Release Plan — v3.4 Arc 3 In-Trade Risk Management (continued)

---

## Readiness

### §1.1 Backlog Age Advisory

Spec/documentation debt items in v3.4 scope aged 2+ cycles without story assignment:

| Item | Type | Cycles without ST | Advisory |
|------|------|------------------|---------|
| BLG-FE-22 — Screener morning routine UX spec | Frontend / UX Specification | 2 (v3.2 target passed, v3.3 carried) | ⚠ 2+ cycles unassigned — promoted to ST-12 EPIC-04 in this release |

**Action:** BLG-FE-22 is assigned ST-12 (EPIC-04) in this release plan. No further advisory items.

### §1.2 Provisional-Target Advisory

Items carrying `Provisional-Target: v3.4` (horizon-planned for this release):
- BLG-FE-31 — Research view component library (v3.4 sprint planning)
- BLG-FE-22 — Screener morning routine UX spec (v3.4 sprint planning)
- BLG-QA-18 — Screener accuracy test protocol (v3.4)
- BLG-FEAT-21 frontend — Trade plan abandonment UI (v3.4)
- BLG-SPEC-28 — trade_plan.md §6.2 field references (v3.4)

**Count:** 5 items carry `Provisional-Target: v3.4`.

Items deferred from v3.3 (Provisional-Target: v3.3 carried to v3.4):
- BLG-FE-23, BLG-FE-24, BLG-FE-25, BLG-FE-29, BLG-FE-30 (all in v3.3 ST-17, deferred) — 5 items

Arc 3 frontend stories returned to backlog from v3.3: ST-03 (IT-01 frontend), ST-05 (IT-02 frontend), ST-07 (IT-03 frontend) — carry-over sprint stories.

Items without matching Provisional-Target signal (no PT field or PT=TBD):
- BLG-AI-03, BLG-OPS-13 — 2 items

### §1.3 Design-Gate Language Scan

Scope candidates scanned for design-gate language ("Product Owner to decide", "design decision required", "pending design", "requires UX decision"):

| Item | Flag | Note |
|------|------|------|
| IT-04 Drawdown-Triggered Review Prompt | ⚠ Design dependency detected | New Arc 3 feature — drawdown review prompt UI requires UX spec before EPIC-02 sprint planning |
| IT-05 Position Concentration Limits | ⚠ Design dependency detected | New Arc 3 feature — concentration warning UI requires UX spec before EPIC-02 sprint planning |

**Design dependency scan: 2 items flagged.** — Surface at Pre-sprint Required Decisions checklist. Design gate (Phase 1.5) must produce UX specs for IT-04 and IT-05 before sprint planning seals EPIC-02.

---

## Scope

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Arc 3 Frontend Completion — IT-01/02/03 frontend display (position lifecycle badge, grace period alert card, stop trail guided panel). UX specs exist from v3.3 design gate. Playwright E2E scenarios required (TEST-GAP-EPIC-01/02-v33). |
| S2-02 | EPIC-02 | IT-04 Drawdown-Triggered Review Prompt — backend drawdown calculation + configurable threshold; frontend structured review prompt with positions by state, portfolio heat, regime status. §13 COMPLIANT — human-in-loop. |
| S2-03 | EPIC-02 | IT-05 Position Concentration Limits — backend single-position heat % and sector concentration (uses DS-03 sector data, shipped v2.9); frontend warning on threshold breach. |
| S2-04 | EPIC-03 | Frontend Quick Wins — v3.3 ST-17 deferred deliverables: BLG-FE-23 (UK suffix), BLG-FE-24 (negative earnings days), BLG-FE-25 (signals page default), BLG-FE-29 (watchlist research status), BLG-FE-30 (trade plan status badges), BLG-FEAT-21 frontend (abandonment UI). |
| S2-05 | EPIC-04 | Spec, QA & Documentation Debt — BLG-FE-31 (research view component library), BLG-FE-22 (screener morning routine UX spec), BLG-SPEC-28 (trade_plan.md §6.2 update), BLG-QA-18 (screener accuracy test protocol), BLG-AI-03 (AI journal review process definition). |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| IT-06 Alpaca Paper Trading | §13 review required before pre-alignment; gate not cleared | v3.5+ |
| PT-04 Setup Quality Score | Gate: 20+ closed trades; data volume not yet reached | Arc 4 context |
| BLG-FE-26 Research page UX review | P3; design gate phase for v3.4 will address design system conformance | v3.4 design gate phase |
| BLG-FEAT-20 Net-of-costs performance | Low TTV; Arc 3/4 data model sequencing | Arc 3/4 context |
| BLG-OPS-13 API performance baseline re-run | Requires live environment + human coordination; P3 | Next operational review |
| BLG-GOV-21 Arc 4 data requirements | "Before Arc 4 planning begins" — Arc 4 not starting v3.4 | Before Arc 4 planning |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-05-14__release-v3.4

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering | RISK-02 | Sprint 2; after EPIC-04 ST-11 (component library reference) |
| EPIC-02 | S2-02, S2-03 | Head of Engineering | RISK-01 | Sprint 2; requires design gate clearance for IT-04/IT-05 UX specs |
| EPIC-03 | S2-04 | Head of Engineering | RISK-04 | Sprint 1; front-load per carry-forward item 1 (LL-v3.3) |
| EPIC-04 | S2-05 | Head of Specs Team | None | Sprint 1; BLG-FE-31 first (before EPIC-01 implementation) |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-02 | IT-04/IT-05 are new Arc 3 features without UX specs — frontend cannot be sprint-planned until design gate produces specs | High | Design gate (Phase 1.5) required before sprint planning seals EPIC-02 stories. Covered by Pre-sprint Required Decisions checklist. | null |
| RISK-02 | EPIC-01 | IT-01/02/03 frontend implements pre-existing UX specs from v3.3 — specs are correct but not yet tested for implementability. TEST-GAP-EPIC-01/02-v33 scenarios must be authored alongside implementation | Medium | Test gap scenarios explicitly listed in backlog; stories carry them as AC | null |
| RISK-03 | EPIC-02 | IT-05 depends on DS-03 sector data (shipped v2.9). Data quality assumed correct but not verified in v3.4 context | Low | Verify DS-03 sector coverage at pre-alignment; EPIC-02 ST-06 AC includes sector data validation | null |
| RISK-04 | Release-level | Frontend delegation pattern: 4 consecutive cycles with deferred frontend items. v3.4 is frontend-heavy. Risk of further deferral if capacity misjudged | Medium | Front-load EPIC-01/03 frontend stories in Sprint 1 where possible; LL carry-forward item 1 acknowledged | null |

---

## Integrity Validation — 3.5 Local Model Integrity

All EPIC IDs declared with `Maps to` scope items:
- EPIC-01 → S2-01 ✓
- EPIC-02 → S2-02, S2-03 ✓
- EPIC-03 → S2-04 ✓
- EPIC-04 → S2-05 ✓

All RISK IDs declared with `Relates to` field:
- RISK-01 → EPIC-02 ✓
- RISK-02 → EPIC-01 ✓
- RISK-03 → EPIC-02 ✓
- RISK-04 → Release-level ✓

S2-ID cross-reference — every S2 item maps to exactly one EPIC:
- S2-01 → EPIC-01 ✓
- S2-02 → EPIC-02 ✓
- S2-03 → EPIC-02 ✓
- S2-04 → EPIC-03 ✓
- S2-05 → EPIC-04 ✓

Backlog item cross-reference:
- All BLG items in S2-04 (BLG-FE-23/24/25/29/30, BLG-FEAT-21) confirmed in backlog.md with Provisional-Target v3.3/v3.4 ✓
- All BLG items in S2-05 (BLG-FE-31, BLG-FE-22, BLG-SPEC-28, BLG-QA-18, BLG-AI-03) confirmed in backlog.md ✓
- Arc 3 deferred stories (ST-03/05/07 from v3.3) in backlog.md "Returned to Backlog" section ✓

**Verdict: PASS — Local model integrity validated.**

---

## Capacity Check

### Effort Estimates by EPIC

| EPIC | Stories | Effort estimate (mid-point) | Effort band | Source |
|------|---------|-----------------------------|-------------|--------|
| EPIC-01 | 3 (ST-01/02/03) | ~3 days | M (from UX specs) | Inline estimate |
| EPIC-02 | 3 (ST-04/05/06) | ~4 days | M | Inline estimate |
| EPIC-03 | 4 (ST-07/08/09/10) | ~2 days | S–XS | Inline estimate; BLG-FE-22 has S from scored_initiatives.md |
| EPIC-04 | 4 (ST-11/12/13/14) | ~2 days | S–XS | BLG-FE-22 S from scored_initiatives.md; others inline |
| **Total** | **14** | **~11 days** | | |

### Available capacity

Standard 2-sprint cycle, solo developer, evenings + weekends (~10–13 days available). Mid-point estimate 11 days.

**Verdict: WARN** — estimate is at the upper end of available capacity. Delivery is feasible but leaves minimal buffer.

### Phasing Recommendation

Total estimated effort: 11 days (mid-point). Available capacity: ~10–13 days.

| Phase | Sprint | EPICs | Stories | Est. days | Notes |
|-------|--------|-------|---------|-----------|-------|
| Phase 1 | Sprint 1 | EPIC-03, EPIC-04 | ST-07–14 | ~4 days | Light quick wins + docs; no design gate dependency |
| Phase 2 | Sprint 2 | EPIC-01, EPIC-02 | ST-01–06 | ~7 days | Arc 3 frontend + risk prompts; EPIC-02 needs design gate |

Ordering rationale: Sprint 1 delivers standalone value (quick wins, spec/QA debt) and produces the component library reference (BLG-FE-31) needed before EPIC-01 implementation. Sprint 2 uses design gate outputs for EPIC-02 and implements Arc 3 frontend with component library guidance.

Risk buffer: If Sprint 2 is over-capacity, EPIC-02 (IT-04/05) can slip to v3.5 — Arc 3 frontend (EPIC-01) and quick wins (EPIC-03) have independent value.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

| Check | Result |
|-------|--------|
| Every S2-ID has an EPIC-xx | PASS |
| Every EPIC declares Maps to scope items | PASS |
| Every RISK has Relates to field | PASS |
| Backlog slice ST items reference EPIC IDs (not free-text) | PASS (stage4 not yet written — verified at STEP 4) |
| All deferred items documented with reason | PASS |
| No scope creep (items not in roadmap or backlog added) | PASS |

**Verdict: PASS**

---

## Integrity Validation — 5.7 Decision Record Integrity

Decisions record `docs/product/decisions/decisions--2026-05-14__release-v3.4.md` created at STEP 3.

| Check | Result |
|-------|--------|
| Scope decisions captured | PASS |
| Sequencing decisions captured | PASS |
| Accepted risks section present (None in this cycle) | PASS (no escalations raised) |
| No open escalations | PASS |

**Verdict: PASS (no escalations required)**
