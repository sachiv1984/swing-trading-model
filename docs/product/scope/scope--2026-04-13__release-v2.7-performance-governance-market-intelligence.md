Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v2.7
Cycle: 2026-04-13__release-v2.7
Last Updated: 2026-04-13

## Release Scope — v2.7 Performance, Governance Hardening & Market Intelligence

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | BLG-OPS-14 — Enable Supabase Supavisor connection pooling on staging and production |
| S2-02 | EPIC-01 | BLG-BE-07-FIX — Refactor get_portfolio_summary() to use a single DB connection |
| S2-03 | EPIC-02 | BLG-GOV-18 — Require QA evidence sign-off block to be complete before PR is raised |
| S2-04 | EPIC-02 | BLG-GOV-19 — Define formal autonomous DoQ sign-off class for code-review-only EPICs |
| S2-05 | EPIC-02 | BLG-GOV-16 — Extend governance_sync.yml to trigger on push to main |
| S2-06 | EPIC-03 | BLG-QA-11 — Fix Playwright page.route() intercepts not firing in local test environment |
| S2-07 | EPIC-03 | BLG-QA-12 — System Status Playwright spec (endpoint list sync + category routing) |
| S2-08 | EPIC-04 | BLG-FEAT-17 — Market Correlation Analysis (per-position and portfolio-level vs. SPY/FTSE) |
| S2-09 | EPIC-04 | BLG-BE-10 — Add supplementary indicator fields to signal generation (display-only, §13 compliant) |
| S2-10 | EPIC-05 | BLG-SPEC-D17 — Spec Dependency Map (read-only reference document) |
| S2-11 | EPIC-05 | BLG-GOV-14 — Governance Health Score formula and roadmap rebalance advisory check |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-08 — Engine prompt compression | L effort; deprioritised v2.5 and v2.6; advisory governance item | v2.8 |
| BLG-GOV-11 — Cycle artefact inventory | P3; no user-facing value; advisory only | v2.8 |
| BLG-GOV-13 — Deduplicate backlog_archive.md | P3; requires Product Owner confirmation (OA pending) | v2.8 post-PO confirm |
| BLG-FEAT-13 — Gated feature rollout capability | P3; no current use case; speculative complexity | v2.8+ |
| BLG-FEAT-16 — AI Journal Summarisation | P3; §13 conditions require Strategy Rules owner pre-alignment before scoping | v2.8+ |
| BLG-TECH-05 — Prometheus metrics endpoint | P3; single-user system; defer until multi-user scale | TBD |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-04-13__release-v2.7
