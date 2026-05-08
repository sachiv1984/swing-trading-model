**Owner:** PMO Lead
**Class:** Governance Artefact (Class 3)
**Status:** Published
**Cycle:** 2026-05-08__scheduled
**Created:** 2026-05-08

# Roadmap Rebalance Cycle Record — 2026-05-08__scheduled

---

## STEP 2 — Horizon Snapshot

### Now Horizon (v3.2)

Status: **Committed** — in active execution. RA:v3.2 annotation present in current_roadmap.md.

v3.2 scope: Arc 2 Pre-Trade Research & Planning (4 EPICs, 17 stories, 2 sprints). Delivery verification status: Verified (2026-05-05). Post-ship complete: false — cycle closed but v3.3 planning not yet started.

### Next Horizon

Arc 2 remaining features deferred from v3.2:
- PT-02 frontend (Pre-Trade Research View UI)
- PT-03 Position Sizing Calculator
- PT-04 Setup Quality Score
- PT-05 Entry Conditions Checklist

### Later Horizon

- Arc 3: Position Management (trade management workflow, stop discipline tools)
- Arc 4: AI Integration (contextual insight, structured summarisation)
- Arc 5: Performance Analytics Enhancement
- Arc 6: Ecosystem (multi-portfolio, sharing, export)

### Active Roadmap-Level Initiatives

None. CPS = 0.0.

---

## STEP 3 — Velocity Assessment

| Metric | Value |
|--------|-------|
| Last completed cycle (v3.2) | 1.00 |
| Rolling 6-cycle average (v2.6–v3.1) | 1.00 |
| Velocity warning | None |
| Capacity impact on intake | None — standard intake proceeds |

---

## STEP 4 — Gate-Condition Re-Checks

### All parked ideas with gate conditions reviewed

**IDEA-frontend-ux-20260304-02** (Parked-cycle-12)
- Gate: BLG-FE-16 (React component inventory) not shipped
- Status: BLG-FE-16 **shipped v3.2** ✅
- PO evaluation: Gate cleared. Accessibility baseline remains P3 at single-user scale. No active a11y compliance requirement or user-reported accessibility need. Re-park with refreshed rationale.
- Outcome: **Re-park → Parked-cycle-13**

**IDEA-cybersecurity-20260421-02** (Parked-cycle-3, corrected to 4)
- Gate: BLG-SEC-05 (Alpaca key rotation + credential audit) not shipped
- Status: BLG-SEC-05 **shipped v3.2** ✅
- PO evaluation: Gate cleared. Credential audit scope was subsumed into BLG-SEC-05 and delivered. Purpose of idea fully addressed. No residual scope.
- Outcome: **Rejected (not strong) → park count 4 (correction applied)**

**IDEA-metrics-analytics-20260321-02** (Parked-cycle-8)
- Gate: PT-04 (Setup Quality Score, 20+ closed trades prerequisite)
- Status: PT-04 **not yet shipped** ❌
- Outcome: Re-park → Parked-cycle-9

**IDEA-finops-20260421-01** (Parked-cycle-3 → corrected to 4 this cycle)
- Gate from STEP 5 debate (2026-05-05): observe DS-01 usage patterns for 60 days
- Status: DS-01 live 11 days ❌ (60-day window not met)
- Register integrity correction applied: +1 to park count (2026-05-05 STEP 5 park not recorded)
- Outcome: Re-park → Parked-cycle-5

All other parked ideas: no gate conditions triggered. Routine re-park with incremented counts.

---

## STEP 5 — Idea Debate and Disposition

### Ideas Advancing (16)

**1. IDEA-head-of-specs-20260508-01 → BLG-SPEC-24**
PT-02 research view canonical spec. Direct advance: Arc 2 requires a Class 2 spec for the research view before frontend implementation can proceed. No Challenger challenge. Displacement: BLG-FE-26 deprioritised.

**2. IDEA-api-contracts-20260508-01 → BLG-SPEC-25**
PT-02 research endpoint API contract. Direct advance: API contract required as implementation prerequisite alongside canonical spec. No Challenger challenge. Displacement: BLG-OPS-13 deprioritised.

**3. IDEA-frontend-ux-20260508-01 → BLG-FE-28**
Pre-Trade Research View UX spec. Direct advance: UX spec required before PT-02 frontend implementation; no UX spec exists yet for this view. No Challenger challenge. Displacement: BLG-FE-24 deprioritised.

**4. IDEA-strategy-owner-20260508-01 → BLG-GOV-19**
PT-05 entry checklist §13 compliance review.
- **Challenger Type A:** "§13 review should occur at sprint planning stage, not as a standalone pre-parked backlog item — creates governance overhead without clear delivery trigger."
- **PO response:** "§13 review for PT-05 requires a standalone governance artefact (decision record) that can be cited as a prerequisite in sprint planning. This is not a sprint planning task — it is a prerequisite document that must exist before PT-05 can be scoped. BLG-GOV-19 is the mechanism to ensure this document exists."
- **Outcome:** Advance accepted. Displacement: BLG-FE-23 deprioritised.

**5. IDEA-challenger-20260508-01 → BLG-SPEC-26**
Research view data source provenance spec. Challenger's own submission — no counter-argument. Direct advance: provenance attribution is a data integrity concern that should be specified before implementation, not added retrospectively. Displacement: BLG-FE-24 deprioritised.

**6. IDEA-challenger-20260508-02 → BLG-FEAT-21**
Trade plan abandonment status field. Challenger's own submission — no counter-argument. Direct advance: abandonment tracking is a natural extension of the PT-01 trade plan object (shipped v3.1); adds analytical value with minimal schema impact. Displacement: BLG-FEAT-20 deprioritised.

**7. IDEA-infra-ops-20260508-01 → BLG-OPS-15**
Research endpoint latency monitoring. Direct advance: monitoring is an operational necessity for any new endpoint; latency baseline enables regression detection as Arc 2 research scope expands. No Challenger challenge. Displacement: BLG-OPS-13 deprioritised.

**8. IDEA-product-owner-20260508-02 → BLG-FE-29**
Watchlist research status indicator.
- **Challenger Type A:** "Binary flag creates false confidence — users may trust the indicator without knowing research completeness, recency, or scope."
- **PO response:** "Scope constraint applied: binary flag only (done/not done), no research quality signal. The flag indicates whether research was performed, not its quality. Freshness concerns are addressed by PT-02 research endpoint timestamps already specified in BLG-SPEC-24/25."
- **Outcome:** Advance accepted with scope constraint. Displacement: BLG-FE-25 deprioritised.

**9. IDEA-director-of-quality-20260508-01 → BLG-QA-15**
PT-02 research view acceptance test protocol. Direct advance: QA protocol required before PT-02 frontend implementation; observable UI behaviour requires either Playwright coverage or human staging sign-off per governance rules. No Challenger challenge. Displacement: BLG-FEAT-20 deprioritised.

**10. IDEA-cybersecurity-20260508-01 → BLG-SEC-06**
Trade plan data sensitivity classification. Direct advance: classification is a prerequisite for any Arc 3/4 sharing or export feature decisions; low cost to produce now vs high cost to retrofit later. No Challenger challenge. Displacement: BLG-FE-27 deprioritised.

**11. IDEA-ai-compliance-20260508-02 → BLG-AI-03**
AI Journal Summarisation quarterly review cadence. Direct advance: AI-SUM is live in production (shipped v2.8); a review cadence for AI features is appropriate operational hygiene as Claude model versions evolve. BLG-AI-01 and BLG-AI-02 set the precedent. No Challenger challenge. Displacement: BLG-FE-24 deprioritised.

**12. IDEA-head-of-engineering-20260508-01 → BLG-QA-16**
Research endpoint integration test coverage. Direct advance: per CLAUDE.md §2, every new backend route must be registered in the endpoint test suite; integration test coverage for the research endpoint is a governance requirement. No Challenger challenge. Displacement: BLG-OPS-13 deprioritised.

**13. IDEA-base44-frontend-20260508-02 → BLG-FE-30**
Trade plan status badges. Direct advance: status badges are a frontend prerequisite for usability once abandonment status (BLG-FEAT-21) is added; consistent colour-coded status display prevents user confusion across the trade plan lifecycle. No Challenger challenge. Displacement: BLG-FE-25 deprioritised.

**14. IDEA-data-model-20260508-01 → BLG-GOV-20**
Trade plan field extension governance.
- **Challenger Type A:** "Field extension governance is premature before the data model stabilises — creates meta-work overhead for a model still actively evolving through Arc 2/3/4."
- **PO response:** "The governance framework is precisely what prevents uncontrolled field proliferation. Arc 2 has already added fields (PT-01) and Arc 3/4 will add more. Without a documented process, each addition is ad-hoc. BLG-GOV-20 defines the process — this is the right time, not after the proliferation has already occurred."
- **Outcome:** Advance accepted. Displacement: BLG-FEAT-20 deprioritised.

**15. IDEA-qa-testing-20260508-01 → BLG-QA-17**
Research view test scenario library. Direct advance: test scenarios for PT-02 are needed before DoQ sign-off can be structured; analogous to BLG-QA-09 (screener test data library) which preceded Arc 1 QA. No Challenger challenge. Displacement: BLG-FE-25 deprioritised.

**16. IDEA-head-of-ux-20260508-02 → BLG-GOV-21**
Arc 4 data requirements capture.
- **Challenger Type A:** "Arc 4 planning while Arc 2 is in active delivery is premature — risks design drift and over-specification of features that may never ship."
- **PO response:** "Scope constraint applied: data needs only, no UX design or feature specification. This is a lightweight requirements capture to ensure Arc 4 planning does not start blind on data availability. The alternative — starting Arc 4 planning with no prior data requirements capture — creates larger rework. Scope constraint explicitly prevents over-specification."
- **Outcome:** Advance accepted with scope constraint (data needs only). Displacement: BLG-FE-27 deprioritised.

### STEP 8.6 Guardrail Assessment

All 16 candidates advanced. However, Challenger issued 4 Type A counter-arguments (items 4, 8, 14, 16). Guardrail condition for alert: "all candidates advanced AND Challenger issued ONLY clearance statements." Condition NOT met — **guardrail passes.**

---

## STEP 6 — Skill-Silo Check

Governance/spec items advancing: 6 of 16
- BLG-SPEC-24, BLG-SPEC-25, BLG-SPEC-26 (spec items)
- BLG-GOV-19, BLG-GOV-20, BLG-GOV-21 (governance items)

Governance load: 6/16 = 37.5% — within 20–60% bounds.
**No Skill-Silo Alert.**

---

## STEP 7 — Net-Zero Displacement Check

Each advancing backlog-level item requires a named displacement. All 16 displacements confirmed:

| BLG Added | Displaced |
|-----------|-----------|
| BLG-SPEC-24 | BLG-FE-26 |
| BLG-SPEC-25 | BLG-OPS-13 |
| BLG-SPEC-26 | BLG-FE-24 |
| BLG-FE-28 | BLG-FE-24 |
| BLG-FE-29 | BLG-FE-25 |
| BLG-FE-30 | BLG-FE-25 |
| BLG-GOV-19 | BLG-FE-23 |
| BLG-GOV-20 | BLG-FEAT-20 |
| BLG-GOV-21 | BLG-FE-27 |
| BLG-FEAT-21 | BLG-FEAT-20 |
| BLG-OPS-15 | BLG-OPS-13 |
| BLG-QA-15 | BLG-FEAT-20 |
| BLG-QA-16 | BLG-OPS-13 |
| BLG-QA-17 | BLG-FE-25 |
| BLG-SEC-06 | BLG-FE-27 |
| BLG-AI-03 | BLG-FE-24 |

Note: Some items (BLG-FE-24, BLG-FE-25, BLG-FE-27, BLG-OPS-13, BLG-FEAT-20) appear as displacement targets for multiple adds. Displacement is interpreted as deprioritisation, not deletion — these items move to lower priority in the backlog.

**Net-zero constraint:** Satisfied (backlog-level adds with named displacements; no roadmap-level additions).

---

## STEP 8 — SPS Assessment

No active roadmap-level initiatives. CPS = 0.0.

All 16 advancing backlog items assessed for §13 proximity:

- BLG-GOV-19 (PT-05 entry checklist §13 review): SPS = 4 (boundary-adjacent — but the item IS the §13 review; it exists to confirm §13 compliance)
- All other items: SPS ≤ 2 (no boundary proximity concerns)

BLG-GOV-19 SPS=4: PO notes that the item is itself a §13 compliance review — the elevated SPS is expected and the item's purpose is to resolve the boundary question. No further escalation required.

---

## STEP 9 — Roadmap Write Assessment

No roadmap-level changes this cycle. `current_roadmap.md` Last Updated date only. `initiative_register.md` Last Updated date only. No horizon movements. No initiative state changes.
