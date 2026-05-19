**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Published
**Cycle:** 2026-05-19__release-v3.8
**Release:** v3.8
**Published:** 2026-05-19

---

# Cycle Summary — v3.8

**Theme:** Arc 5 Strategy Integrity Foundation + Trade Plan Form Enhancements + Ticker Universe Management

---

## Release Overview

| Field | Value |
|-------|-------|
| Release | v3.8 |
| Cycle ID | 2026-05-19__release-v3.8 |
| Plan date | 2026-05-19 |
| EPICs | 4 (EPIC-01 through EPIC-04) |
| Stories | 10 (8 confirmed + 2 conditional on PT-04 gate) |
| Sprints | 2 |
| Capacity check | ⚠️ WARN — see phasing recommendation |
| Velocity baseline | 0.97 rolling 6-cycle average |

---

## Scope Summary

| EPIC | Stories | Theme | Sprint |
|------|---------|-------|--------|
| EPIC-04 | ST-09, ST-10 | Platform & Governance — Ticker Universe UI + governance debt | 1 |
| EPIC-03 | ST-06, ST-07, ST-08 | Trade Plan Form Enhancements — setup type + news panel + AI thesis | 1 |
| EPIC-01 | ST-01 (gate), ST-02, ST-03 | Arc 5 Foundation — SI-01 Pre-Entry Rule Validation | 1 (gate) / 2 (impl) |
| EPIC-02 | ST-04, ST-05 (conditional) | Arc 2 Completion — PT-04 Setup Quality Score | 2 (conditional) |

---

## Key Decisions

1. **SI-01 as primary arc feature** — highest-priority unshipped item by scored_initiatives.md (Strat=5, Risk=5, Rev=5, SPS=4). Arc 5 begins with v3.8.
2. **SI-03 deferred to v3.9** — depends on SI-01 operational first; attempting both risks SI-01 quality.
3. **PT-04 carried as conditional EPIC-02** — third conditional defer attempt. Product Owner decision required by 2026-05-22: park or carry. Gate: 20+ closed trades.
4. **Trade plan form suite (EPIC-03)** — BLG-FEAT-23/BLG-FE-36/BLG-FEAT-24 form a dependency chain that enhances the trade plan creation UX; all Provisional-Target: v3.8.
5. **Ticker Universe Management (EPIC-04)** — retires the public.tickers startup sync; makes ticker_universe the sole authoritative source.

---

## Risks

| RISK-ID | Description | Priority | Resolution path |
|---------|-------------|----------|-----------------|
| RISK-01 | PT-04 gate condition not confirmed | High | PO decision due 2026-05-22; EPIC-02 removed if gate not met |
| RISK-02 | SI-01 §13 binding conditions may restrict scope | Medium | §13 gate story (ST-01) in Sprint 1 |
| RISK-03 | EPIC-03 dependency chain ST-06→ST-07→ST-08 | Low | Strict story ordering; ST-08 Phase 1 template-only (no external API) |
| RISK-04 | Ticker sync retirement may cause regression | Medium | Playwright coverage required; seed defaults verified before sync removal |

---

## Pre-sprint Planning Required Decisions

The following decisions must be resolved before sprint planning seals (`sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] PT-04 gate decision — Product Owner to confirm whether 20+ closed trades gate is met. If met: EPIC-02 included as Sprint 2 scope. If not met: EPIC-02 removed. — Owner: Product Owner — Deadline: 2026-05-22

---

## Outstanding Actions Carried Forward

| # | Action | Owner | Deadline |
|---|--------|-------|----------|
| 1 | Reconstruct missing v3.6 changelog entry in `docs/product/changelog.md` | PMO Lead | Before v3.8 closes |
| 2 | PT-04 gate decision (confirmed above as pre-sprint planning required decision) | Product Owner | 2026-05-22 |
| 3 | DoQ sign-off date enforcement mechanism (addressed in ST-10) | Director of Quality | v3.8 |
| 4 | Smoke-tests.yml timeout monitoring | QA & Testing Owner | v3.8 if recurrence |

---

## Design Gate

**Required:** Yes — v3.8 includes frontend-facing changes (EPIC-01 frontend panel, EPIC-03 form enhancements, EPIC-04 new page). Design gate must run before sprint planning seals.

Design gate record location: `claude/cycles/2026-05-19__release-v3.8/design_gate.md` (to be created by Design Gate Engine).

---

## Next Steps

1. Product Owner: PT-04 gate decision (due 2026-05-22) → determines EPIC-02 inclusion
2. Strategy Rules & System Intent Owner: §13 review for SI-01 (delegated as ST-01 in Sprint 1)
3. Run design gate (`run design-gate --cycle 2026-05-19__release-v3.8`)
4. Run sprint planning (`plan sprint --cycle 2026-05-19__release-v3.8`)
