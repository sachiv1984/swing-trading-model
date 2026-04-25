Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v3.0
Cycle: 2026-04-25__release-v3.0
Last Updated: 2026-04-25

---

## Planning Decisions — v3.0 Arc 1 Remainder: Screener Engine & Results Page

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| DS-04 Earnings Calendar deferred to v3.1 | No spec exists; independent feature not blocking screener engine flow; M effort would distract from core Arc 1 delivery | Product Owner | 2026-04-25 |
| BLG-FEAT-13 (feature flags) deferred to v3.1 | P3, M effort; lower priority than completing Arc 1 screener; can be addressed after Arc 1 ships | Product Owner | 2026-04-25 |
| BLG-FEAT-19 (monthly P&L) deferred to v3.1 | S effort but Arc 2 reporting scope; keeping v3.0 focused on Arc 1 screener delivery | Product Owner | 2026-04-25 |
| BLG-FE-16 (React component inventory) deferred to v3.1 | P3, M effort; EPIC-01 H effort means capacity is the binding constraint | Product Owner | 2026-04-25 |
| BLG-GOV-11 (cycle artefact inventory) deferred to v3.1 | P3, M effort; governance housekeeping that can follow Arc 1 completion | Product Owner | 2026-04-25 |
| BLG-OPS-13 (API performance baseline) as Ops OA | Requires live staging environment and human coordination; cannot be included in an automated sprint | Infrastructure & Operations Owner | 2026-04-25 |
| v2.9 deferred patches (execution_prompt.md §2 + §3.1.A) included as EPIC-04 Sprint 1 | Targeted at v3.0 sprint planning per lessons_learnt_closure.md; delivering before sprint planning ensures execution improvements are active for the v3.0 sprint | Head of Specs Team | 2026-04-25 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 in Sprint 1, EPIC-02 in Sprint 2 | EPIC-02 (screener frontend) has hard dependency on EPIC-01 ST-04 (GET /screener/results endpoint); serialised sprint order is required | Product Owner | 2026-04-25 |
| EPIC-04 governance in Sprint 1 (parallel to EPIC-01) | EPIC-04 is fully independent of Arc 1 EPICs; running it in Sprint 1 resolves v2.9 deferred patches before sprint execution begins | PMO Lead | 2026-04-25 |
| EPIC-03 ops/QA in Sprint 2 (parallel to EPIC-02) | EPIC-03 items are independent of both EPIC-01 and EPIC-02; Sprint 2 pairing avoids an overloaded Sprint 1 given EPIC-01 H effort | PMO Lead | 2026-04-25 |
| Design gate required between Sprint 1 and Sprint 2 | DS-02 frontend implementation (EPIC-02) requires design gate sign-off; screener_results.md spec is the gate artefact; gate should confirm spec is implementation-ready before Sprint 2 opens | Head of UX & Design + Product Owner | 2026-04-25 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | All risks mitigated at planning level; no Accepted Risk escalations raised | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-04-25__release-v3.0
