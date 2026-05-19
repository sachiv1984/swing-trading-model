**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Version:** 1.0
**Cycle:** 2026-05-19__release-v3.8
**Release:** v3.8
**Published:** 2026-05-19

---

# Release Plan — v3.8

**Theme:** Arc 5 Strategy Integrity Foundation + Trade Plan Form Enhancements + Ticker Universe Management

---

## Readiness

### 1.1 Backlog Age Advisory

Spec/documentation debt items in scope for v3.8:
- BLG-GOV-24 (gh_issue_template.md §14 entry): Appeared in v3.7 target, 1 cycle without story assignment → ⚠️ Advisory: 1 spec/governance debt item aged 1 cycle without story assignment. Promoted to ST-10 for v3.8.

No items aged 2+ cycles without story assignment.

### 1.2 Provisional-Target Advisory

Items with `Provisional-Target: v3.8`: 5 items — BLG-FEAT-22, BLG-FEAT-23, BLG-FEAT-24, BLG-FE-36, BLG-GOV-24.
Items with no matching Provisional-Target signal: SI-01, PT-04 (roadmap-level scope items, not backlog-style targets).
ℹ 5 item(s) carry `Provisional-Target: v3.8` — horizon-planned for this release. 2 items are roadmap arc items without Provisional-Target field (arc scope, not backlog items).

### 1.3 Design Dependency Scan

0 items flagged with explicit design-gate language. Minor UX decisions exist within arc feature implementation but none require pre-sprint PO design gate. Recorded in run_manifest.md.

---

## Scope

### S2 Scope Items

| ID | Scope Item | Source | Effort | Notes |
|----|-----------|--------|--------|-------|
| S2-01 | Arc 5 Foundation — SI-01 Pre-Entry Rule Validation Gate | Arc 5 roadmap; scored_initiatives.md SPS=4 | M+M+XS (gate+backend+frontend) | §13 review required; highest-priority unshipped item by Strat+Risk+Rev |
| S2-02 | Arc 2 Completion — PT-04 Setup Quality Score | Arc 2 roadmap; scored_initiatives.md SPS=3 | M+M (backend+frontend) | Conditional: 20+ closed trades gate; Product Owner decision due 2026-05-22 |
| S2-03 | Trade Plan Form Enhancements — setup type + news context + AI thesis | BLG-FEAT-23, BLG-FE-36, BLG-FEAT-24 | S+S+M | Dependency chain: BLG-FEAT-23 → BLG-FE-36 → BLG-FEAT-24 |
| S2-04 | Ticker Universe Management Page | BLG-FEAT-22 | M | Retires public.tickers startup sync; makes ticker_universe sole authoritative source |
| S2-05 | Governance Debt Clearance | BLG-GOV-24 + DoQ enforcement OA | XS+XS | §14 table gap fix + DoQ sign-off date mechanism |

### Items Explicitly Deferred

| Item | Rationale |
|------|-----------|
| SI-03 Red Flag Journal | Depends on SI-01 operational + data accumulation; deferred to v3.9 after SI-01 is live |
| PO-02 Journal Pattern Recognition | Gate not met: 6+ months AI-summarised journals required; SPS=1 |
| PO-03, PO-04, PO-05 | Data density gates not met; horizon items |
| SI-02 Behavioural Drift Detection | Requires PO-01 + PO-03 data foundation; SPS=1 |
| SI-04, SI-05 | Sequential dependencies on SI-01+SI-03 and data accumulation |
| BLG-FEAT-20 Net-of-costs tracking | Arc 3/4 data model sequencing constraint; still not blocking |

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Strategy Rules & System Intent Owner; Head of Backend Engineering; Head of UX & Design | RISK-02 | Sprint 1 gate story first; ST-02/ST-03 execute Sprint 2 after §13 PASS |
| EPIC-02 | S2-02 | Head of Backend Engineering; Metrics & Analytics Owner | RISK-01 | Conditional: PO confirms gate met before sprint planning seals; Sprint 2 only |
| EPIC-03 | S2-03 | Head of UX & Design; Backend Engineering Patterns Owner | RISK-03 | ST-06 → ST-07 → ST-08 sequential within EPIC; Sprint 1 |
| EPIC-04 | S2-04, S2-05 | Head of UX & Design; Head of Backend Engineering; Head of Specs Team | RISK-04 | Sprint 1; first to merge (fewest shared file conflicts) |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-02 | PT-04 gate (20+ closed trades) not confirmed met; two consecutive conditional defers (v3.6, v3.7) | High | PO decision due 2026-05-22 — park or conditional include; EPIC-02 removed from sprint if gate not confirmed | null |
| RISK-02 | EPIC-01 | SI-01 §13 review may impose binding conditions restricting feature scope (e.g., display-only advisory, no logging, specific override format) | Medium | §13 gate story (ST-01) in Sprint 1; implementation stories (ST-02/ST-03) blocked until PASS + binding conditions documented in decisions record | null |
| RISK-03 | EPIC-03 | BLG-FEAT-24 has two upstream dependencies (BLG-FE-36 + BLG-FEAT-23); sequencing failure would block ST-08 | Low | Strict story ordering ST-06 → ST-07 → ST-08 within EPIC-03; ST-08 implements template-engine phase only (no external API call required) | null |
| RISK-04 | EPIC-04 | Retiring public.tickers startup sync may cause screener/signal regression if ticker_universe not properly seeded at deployment | Medium | BLG-FEAT-22 AC requires `ticker_universe` populated with seed defaults before removing sync; Playwright coverage required for screener/signal correctness post-change | null |

### Sequencing Notes

**EPIC-01:** ST-01 (§13 gate — delegated_decision) executes in Sprint 1. ST-01 must reach `status: done` before ST-02 and ST-03 execute in Sprint 2. This is the established §13 gating pattern (established v3.5 IT-06, recorded in execution_prompt.md v3.22 §5.1).

**EPIC-02:** Conditional scope. Product Owner decision (PT-04 gate) due 2026-05-22. If gate confirmed met: EPIC-02 proceeds as Sprint 2 scope. If gate not met: EPIC-02 removed and sprint plan sealed without it. Sprint planning must confirm this gate explicitly at STEP -1.

---

## Capacity Check

### Effort Summary

| EPIC | Stories | Effort (low–high days) | Source |
|------|---------|----------------------|--------|
| EPIC-01 | 3 (ST-01 gate + ST-02 + ST-03) | 0.5 + 1–2 + 1–2 = 2.5–4.5 days | SI-01: scored_initiatives M band |
| EPIC-02 | 2 (ST-04 + ST-05) — conditional | 1–2 + 1–2 = 2–4 days | PT-04: scored_initiatives M band |
| EPIC-03 | 3 (ST-06 + ST-07 + ST-08) | 0.5 + 0.5 + 1–2 = 2–3 days | Inline: S+S+M |
| EPIC-04 | 2 (ST-09 + ST-10) | 1–2 + 0.5 = 1.5–2.5 days | Inline: M+XS |

**Total (EPIC-02 conditional):** 6–10 days (without PT-04) or 8–14 days (with PT-04)

**Rolling velocity (v3.2–v3.7):** 0.97 — all recent cycles delivered at full velocity.

**Capacity assessment:** ⚠️ WARN — Total mid-point ~12 days with PT-04 is at the high end for a 2-sprint release at solo-dev pace. Without PT-04 (~8 days mid-point) this is within comfortable range.

### Phasing Recommendation

**Phase 1 (Sprint 1):** EPIC-04 (ST-09, ST-10) + EPIC-03 (ST-06, ST-07, ST-08) + EPIC-01 ST-01 (gate) — 6 stories, estimated 4–6 days. All independent; no cross-EPIC dependencies. EPIC-04 first (fewest shared files).

**Phase 2 (Sprint 2):** EPIC-01 ST-02, ST-03 (after §13 PASS) + EPIC-02 ST-04, ST-05 (conditional, if gate met) — 2–4 stories, estimated 2–6 days. EPIC-01 implementation after gate, EPIC-02 conditional on PO confirmation.

**Ordering rationale:** EPIC-04 first (governance/platform, low risk, enables ticker universe correctness). EPIC-03 next (high user value, self-contained, improves trade plan UX immediately). EPIC-01 gate story runs concurrent in Sprint 1 as delegated_decision. Sprint 2 dedicated to SI-01 implementation and PT-04 (if gated).

---

## Integrity Validation — 3.5 Local Model Integrity

| Check | Result | Notes |
|-------|--------|-------|
| All S2 IDs mapped to EPICs | ✅ Pass | S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03, S2-04+S2-05→EPIC-04 |
| All EPIC IDs declared Maps-to | ✅ Pass | Each EPIC maps to at least one S2 item |
| All RISK IDs in EPIC table appear in Risk Register | ✅ Pass | RISK-01 through RISK-04 all present in both table and register |
| No orphaned S2 references | ✅ Pass | All 5 S2 items referenced in at least one EPIC |
| Conditional scope flagged | ✅ Pass | EPIC-02 conditional explicitly marked; gate mechanism defined |

**Model integrity: PASS. plan_executable = true.**
