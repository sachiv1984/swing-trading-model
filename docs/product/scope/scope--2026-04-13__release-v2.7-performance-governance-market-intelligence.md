Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v2.7
Cycle: 2026-04-13__release-v2.7
Last Updated: 2026-04-16

---

## Release Scope — v2.7 Performance, Governance Hardening & Market Intelligence

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Infrastructure — BLG-OPS-14: Enable Supabase Supavisor connection pooling on staging and production |
| S2-02 | EPIC-01 | Backend Engineering — BLG-BE-07-FIX: Refactor get_portfolio_summary() to use single DB connection |
| S2-03 | EPIC-02 | Governance Process — BLG-GOV-18: Require QA evidence sign-off block complete before PR raised |
| S2-04 | EPIC-02 | Governance Process — BLG-GOV-19: Define formal autonomous DoQ sign-off class for code-review-only EPICs |
| S2-05 | EPIC-02 | Governance / CI — BLG-GOV-16: Extend governance_sync.yml to trigger on push to main |
| S2-06 | EPIC-03 | Test Infrastructure — BLG-QA-11: Fix Playwright page.route() intercepts not firing in local environment |
| S2-07 | EPIC-03 | Test Automation — BLG-QA-12: System Status Playwright spec (category routing + endpoint count) |
| S2-08 | EPIC-04 | Product Feature — BLG-FEAT-17: Market Correlation Analysis (GET /analytics/market-correlation) |
| S2-09 | EPIC-04 | Backend Engineering — BLG-BE-10: Add supplementary indicator fields to signal generation (display-only, §13 COMPLIANT) |
| S2-10 | EPIC-05 | Spec Debt — BLG-SPEC-D17: Spec Dependency Map |
| S2-11 | EPIC-05 | Governance Process — BLG-GOV-14: Governance Health Score |

**Total in scope:** 11 items (1 P1, 5 P2, 5 P3)

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-08 — Engine prompt compression | L effort; advisory only — deprioritised | v2.8 |
| BLG-GOV-11 — Cycle artefact inventory | P3; advisory; no user-facing value | v2.8 |
| BLG-GOV-13 — Deduplicate backlog_archive.md | Requires Product Owner confirmation (OA outstanding) | v2.8 post-PO confirm |
| BLG-FEAT-13 — Gated feature rollout capability | P3; no current use case | v2.8+ |
| BLG-FEAT-16 — AI Journal Summarisation | Complex §13 conditions; Strategy Rules owner pre-alignment required | v2.8+ |
| BLG-TECH-05 — Prometheus metrics endpoint | Single-user system; defer until multi-user | TBD |
| AC-6 (ST-08) — Market Correlation frontend rendering | Backend contract specified in analytics_endpoints.md v2.1.0; frontend story deferred | v2.8 |

### Supersession note

Superseded by: `docs/product/changelog.md` — v2.7 entry (2026-04-16)
Changelog: v2.7 shipped 2026-04-16 — all 11 scope items delivered; verified status: Verified
Verification report: `claude/cycles/2026-04-13__release-v2.7/verification_report.md`
Cycle: 2026-04-13__release-v2.7
