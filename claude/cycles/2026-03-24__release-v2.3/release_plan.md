Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v2.3
Cycle: 2026-03-24__release-v2.3
Last Updated: 2026-03-24

---

# Release Plan — v2.3 Quality Automation & User Insight

---

## Readiness

**Prior cycle:** 2026-03-21__release-v2.2 — Status: Closed (post_ship_complete: true, next_cycle_unblocked: true)
**Roadmap status:** v2.3 listed as next planned release; §3 Delivery Plan clear for v2.3 planning
**Backlog status:** 23 active items targeting v2.3 (per `groom backlog` run 2026-03-24)
**Design gate:** Not started (Phase 1.5 — runs after this plan publishes)

**Readiness assessment (Product Owner):** PASS. Prior cycle fully closed, delivery plan clear, backlog groomed and health-checked 2026-03-24.

### Backlog Age Advisory (STEP 1.1)

Spec/documentation debt items aged 2+ cycles without story assignment: **None found**. BLG-SPEC-D14 is the only active spec debt item; it was added in the v2.2 cycle (1 cycle old). No advisory required.

### Provisional-Target Advisory (STEP 1.2)

ℹ 8 items carry `Provisional-Target: v2.3` — horizon-planned for this release: BLG-OPS-07, BLG-QA-03, BLG-QA-04, BLG-QA-05, BLG-OPS-08, BLG-OPS-09, BLG-FE-05, BLG-QA-06.
15 items have no matching Provisional-Target signal (target release set directly, no provisional-target field).

---

## Scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | User-visible features: Strategy Compliance Score (BLG-FEAT-11) + Metrics Staleness Indicator (BLG-FEAT-09) |
| S2-02 | EPIC-02 | QA automation foundation: Staging reset (BLG-OPS-08) + seed scripts (BLG-QA-06) + smoke test (BLG-QA-05) + chart E2E (BLG-QA-01) |
| S2-03 | EPIC-03 | Operational readiness: Health endpoint spec update (BLG-SPEC-D14) + DB size alert (BLG-OPS-09) + health playbook (BLG-OPS-07) |
| S2-04 | EPIC-04 | Frontend polish: Alert badge (BLG-FE-05) + Alert CTA button (BLG-FE-04) + Loading state standardisation (BLG-FE-02) + Sidebar nav overflow (BLG-UX-01) |
| S2-05 | EPIC-05 | Governance & QA process: Branch discipline fix (BLG-GOV-07) + Test execution template (BLG-QA-03) + Integration coverage report (BLG-QA-04) + Engine prompt compression (BLG-GOV-08, conditional) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-03 — Simplify cycle artefact sealing | L effort, P3; circularly affects the engine running this cycle; defer to stable release | v2.4 |
| BLG-FE-03 — User-Facing Error Message Mapping | P3, S–M; deprioritised by BLG-QA-04 displacement signal from v2.3 rebalance | v2.4 |
| BLG-BE-04 — R-Multiple stop price fix | P3, S; no urgent user impact | v2.4 |
| BLG-OPS-05 — API Performance Baseline | P3, S; displaced by seed scripts (BLG-QA-06) in priority queue | v2.4 |
| TEST-GAP-EPIC-05-SLIP — Slippage test scenarios | P3, S; displaced by BLG-OPS-08 in priority queue | v2.4 |
| BLG-TECH-05 — Prometheus metrics endpoint | P3; roadmap §5 "later" horizon | v2.4+ |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-03-24__release-v2.3

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Strategy Rules & System Intent Owner + Backend + Frontend | RISK-01 (SPS=4 sign-off required for BLG-FEAT-11) | Sprint 1 or 2; FEAT-11 requires Strategy Rules sign-off at DoQ |
| EPIC-02 | S2-02 | QA & Testing Owner + Infrastructure & Operations Owner | RISK-02 (BLG-OPS-08 prerequisite gates QA-06 and QA-05) | BLG-OPS-08 must precede BLG-QA-06 and BLG-QA-05; BLG-QA-01 independent |
| EPIC-03 | S2-03 | API Contracts Owner + FinOps & Resource Architect + Infrastructure Owner | RISK-03 (BLG-SPEC-D14 must precede BLG-OPS-07 which references v1.1 spec) | BLG-SPEC-D14 first; BLG-OPS-09 and BLG-OPS-07 can follow in same sprint |
| EPIC-04 | S2-04 | Base44 Frontend Owner + Product Owner | RISK-04 (BLG-UX-01 requires Product Owner design decision before engineering can spec) | BLG-FE-05, BLG-FE-04 independent quick wins; BLG-FE-02 and BLG-UX-01 after design gate |
| EPIC-05 | S2-05 | Head of Specs Team | RISK-05 (BLG-GOV-08 is L effort — conditional; may slip if capacity tight) | BLG-GOV-07 XS quick win; BLG-QA-03 and BLG-QA-04 independent; BLG-GOV-08 stretch/conditional |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | BLG-FEAT-11 is SPS=4 (strategy-boundary-adjacent); requires Strategy Rules & System Intent Owner DoQ sign-off at delivery verification | High | Strategy Rules owner must review implementation before sprint close; §13.3 scope constraint (display-only, no automated enforcement) documented in AC | null |
| RISK-02 | EPIC-02 | BLG-OPS-08 staging reset script is a hard prerequisite for BLG-QA-06 seed scripts and BLG-QA-05 smoke test; if OPS-08 slips, QA-05 and QA-06 cannot complete | Medium | Schedule OPS-08 in Sprint 1; QA-06 and QA-05 in Sprint 2; BLG-QA-01 has no dependency on OPS-08 and can proceed in parallel | null |
| RISK-03 | EPIC-03 | BLG-SPEC-D14 (health endpoint spec update) must precede BLG-OPS-07 (health playbook), which references health_endpoints.md v1.1 schema | Low | Schedule SPEC-D14 in Sprint 1; OPS-07 references confirmed v1.1 | null |
| RISK-04 | EPIC-04 | BLG-UX-01 requires Product Owner to make a design decision (grouping pattern for sidebar nav) before engineering can spec or implement | High | Product Owner must issue design decision before sprint planning seals for Sprint containing UX-01; if decision not made, UX-01 deferred to sprint N+1 | null |
| RISK-05 | EPIC-05 | BLG-GOV-08 (engine prompt compression) is L effort and may not complete within the cycle if capacity is constrained | Low | Mark as conditional/stretch in Sprint 3; does not block other epics or the publish gate | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**Validator:** Head of Specs Team + Challenger
**Date:** 2026-03-24

### S2-ID Completeness
All 5 S2 items have IDs (S2-01 through S2-05). ✓

### EPIC-ID Completeness
All 5 EPICs have IDs (EPIC-01 through EPIC-05) and declare `Maps to: S2-xx`. ✓

| EPIC | Maps to |
|------|---------|
| EPIC-01 | S2-01 |
| EPIC-02 | S2-02 |
| EPIC-03 | S2-03 |
| EPIC-04 | S2-04 |
| EPIC-05 | S2-05 |

### RISK-ID Completeness
All 5 RISKs (RISK-01 through RISK-05) have IDs and declare `Relates to: EPIC-xx`. ✓

### Scope Boundary Check
- No deferred items were promoted to scope without roadmap authority. ✓
- No strategic exclusions (§13) violated. BLG-FEAT-11 is display-only (§13.3 constraint explicitly in AC). ✓
- No new initiatives added that are not in the backlog. ✓

### Dependency Model Consistency
- EPIC-02: OPS-08 → QA-06 → QA-05 chain is consistent. QA-01 independent. ✓
- EPIC-03: SPEC-D14 → OPS-07 ordering is consistent. ✓
- EPIC-04: UX-01 design gate documented in RISK-04. ✓
- No circular dependencies. ✓

**Result: PASS**

---

## Capacity Check

**Capacity assumption:** Solo developer, evenings + focused sessions (not specified; default assumed).
**Timebox:** Not constrained (not specified).

### Effort Estimate by EPIC

| EPIC | Stories | Effort estimate | Notes |
|------|---------|----------------|-------|
| EPIC-01 | 2 (FEAT-11 M-L, FEAT-09 S-M) | 4–7 days | FEAT-11 has SPS=4 sign-off overhead |
| EPIC-02 | 4 (OPS-08 S, QA-06 S-M, QA-05 M, QA-01 M) | 4–6 days | OPS-08 prerequisite gates QA-06/05 |
| EPIC-03 | 3 (SPEC-D14 XS, OPS-09 S, OPS-07 S) | 1–2 days | Quick wins bundle |
| EPIC-04 | 4 (FE-05 S, FE-04 XS, FE-02 M, UX-01 M+design) | 3–5 days | UX-01 requires design decision first |
| EPIC-05 | 4 (GOV-07 XS, QA-03 S, QA-04 M, GOV-08 L conditional) | 3–6 days | GOV-08 conditional — 2 days or skip |

**Total estimated:** 15–26 days (mid-point ~20 days)

**Available capacity (solo-dev default):** ~6–8 days/sprint × 3 sprints = ~18–24 days

**Result: WARN** — Total mid-point estimate (~20 days) is within 3-sprint capacity range but tight at the upper end. BLG-GOV-08 (L) and BLG-UX-01 (design dependency) are the primary variables.

### Phasing Recommendation

| Phase | Sprint | EPICs / Stories | Estimated hrs |
|-------|--------|----------------|--------------|
| Phase 1 | Sprint 1 | EPIC-03 (all: SPEC-D14, OPS-09, OPS-07) + EPIC-02 partial (OPS-08 reset + QA-01 chart E2E) + EPIC-05 quick wins (GOV-07 XS, QA-03 S) | ~5–8 days |
| Phase 2 | Sprint 2 | EPIC-01 (FEAT-11 + FEAT-09) + EPIC-02 remainder (QA-06 seed + QA-05 smoke test) | ~8–13 days |
| Phase 3 | Sprint 3 | EPIC-04 (FE-05, FE-04, FE-02 + UX-01 conditional on design) + EPIC-05 remainder (QA-04 coverage report + GOV-08 conditional) | ~5–8 days |

**Rationale:**
- Sprint 1: Clears all XS/S quick wins and the OPS-08 prerequisite; QA-01 is independent and can start immediately.
- Sprint 2: Main feature EPICs — FEAT-11 requires most care (SPS=4); OPS-08 is already complete so QA-06/05 can run.
- Sprint 3: Polish and governance — UX-01 conditional on Product Owner design decision by Sprint 2; GOV-08 is stretch and may carry to v2.4 if capacity is consumed by UX-01.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**Validator:** Head of Specs Team + PMO Lead
**Date:** 2026-03-24

### S2 → EPIC Coverage
Every S2 item maps to exactly one EPIC. Every EPIC declares exactly one `Maps to` S2 item. No orphan S2 items. ✓

### EPIC → Story Coverage (Stage 4 → Stage 3 reconciliation)
All stories in `stage4_backlog_slice.md` reference a valid EPIC-ID. No story references an EPIC-ID not defined in the Execution Plan. ✓

### Backlog Marker Present
`<!-- release-plan-marker: RP:v2.3:2026-03-24__release-v2.3 -->` written to `claude/backlog/backlog.md`. ✓

### RISK → EPIC Coverage
All 5 RISKs reference a valid EPIC-ID. ✓

### Deferred Items
All 6 deferred items have explicit target versions (v2.4 or later). None deferred without stated reason. ✓

**Result: PASS**

---

## Integrity Validation — 5.7 Decision Record Integrity

**Trigger check:** Any accepted risk escalations or AR/SRB decision records created? No escalations opened in this cycle.

**Result: not_applicable** (no decision records required; no escalations raised)

---
