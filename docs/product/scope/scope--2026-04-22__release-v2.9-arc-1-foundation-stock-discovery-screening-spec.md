Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v2.9
Cycle: 2026-04-22__release-v2.9
Last Updated: 2026-04-22

## Release Scope — v2.9 Arc 1 Foundation — Stock Discovery & Screening Spec & Infrastructure

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-02 | DS-03 — Sector & Industry Classification (Yahoo Finance enrichment; prerequisite for DS-01 concentration filter) |
| S2-02 | EPIC-02 | DS-05 — Alpaca US Market Data Integration (replace Yahoo for US OHLCV; higher quality ATR inputs) |
| S2-03 | EPIC-02 | DS-06 — Alpaca News Panel (display-only news context; §13 COMPLIANT; requires BLG-GOV-16 gate) |
| S2-04 | EPIC-01 | BLG-SPEC-21 — Screener results schema spec (canonical spec for Arc 1 screener output data structure) |
| S2-05 | EPIC-01 | BLG-SPEC-22 — Alpaca API integration contract (formal contract for DS-05 endpoint usage, fallback, error handling) |
| S2-06 | EPIC-01 | BLG-SPEC-23 — Screener internal API contract (GET /screener/results, POST /screener/run; in openapi.yaml) |
| S2-07 | EPIC-01 | BLG-FE-17 — Screener results page UX spec (DS-02 interaction patterns, empty states, freshness indicator, promotion flow) |
| S2-08 | EPIC-03 | BLG-GOV-16 — §13 review record for DS-06 Alpaca News Panel (required governance gate before DS-06 implementation) |
| S2-09 | EPIC-03 | BLG-QA-08 — External API mock harness for CI (deterministic CI for Alpaca + Yahoo Finance) |
| S2-10 | EPIC-03 | BLG-QA-09 — Screener test data library (min 10 synthetic tickers; edge case coverage for screener filters) |
| S2-11 | EPIC-04 | BLG-GOV-14 — execution_prompt.md §3.2 patches (2 deferred patches from v2.8; DoQ counter-sign + EPIC consolidation) |
| S2-12 | EPIC-04 | BLG-GOV-15 — execution_prompt.md STEP 5.1.B (System_status_report cross-check advisory) |
| S2-13 | EPIC-04 | BLG-FE-15 — SystemStatus.js /ai prefix fix (cosmetic; AI endpoints appear in named category) |
| S2-14 | EPIC-04 | BLG-AI-01 — AI Journal summary audit log (persistent audit record for every AI summary run) |
| S2-15 | EPIC-04 | TEST-GAP-EPIC-04 — AI Journal test scenario coverage (ai_scenarios.md with 4 scenarios) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| DS-01 — Strategy-Rules Screener Engine | H effort; requires BLG-SPEC-21/23 specs (in this sprint) first; implement in v3.0 | v3.0 |
| DS-02 — Screener Results Page | Requires DS-01 + BLG-FE-17; defer until DS-01 ships | v3.0 |
| DS-04 — Earnings Calendar Integration | M effort; can parallel DS-02 but defer to v3.0 to keep scope | v3.0 |
| DS-07 — Watchlist Promotion Flow | Depends on DS-02; defer to v3.0 | v3.0 |
| BLG-GOV-08 — Engine prompt compression | 5 consecutive deferrals; retirement review triggered at v2.9 planning; recommend retire | Retire (next groom) |
| BLG-GOV-11 — Cycle artefact inventory | P3, M effort; defer to v3.0 | v3.0 |
| BLG-FEAT-13 — Feature flag rollout | P3, M effort; no Arc 1 dependency | v3.0 |
| BLG-FEAT-18 — Consecutive losing streak | P2, S; not Arc 1 prerequisite | v3.0 |
| BLG-FEAT-19 — Monthly P&L summary | P2, S; not Arc 1 prerequisite | v3.0 |
| BLG-OPS-12 — External API health check | P2, S; useful but not critical path | v3.0 |
| BLG-FE-16 — React component inventory | P3, M; deferrable Arc 1 reference | v3.0 |
| BLG-AI-02 — Model version contract | P3, S; BLG-AI-01 covers urgent gap | v3.0 |
| BLG-SPEC-20 — Spec front-matter standard | P3, S; apply inline when creating Arc 1 specs | v3.0 |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-04-22__release-v2.9
