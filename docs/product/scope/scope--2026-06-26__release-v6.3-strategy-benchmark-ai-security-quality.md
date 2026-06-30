Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v6.3
Cycle: 2026-06-26__release-v6.3
Last Updated: 2026-06-30

## Release Scope — v6.3 Strategy Benchmark, AI Security & Quality Infrastructure

### Items in scope

| S2-ID | Epic | Description | Class |
|-------|------|-------------|-------|
| S2-01 | EPIC-01 | Fix AI journal summary on Trade History tab — silent failure (BLG-BE-39) | Firm |
| S2-02 | EPIC-01 | Fix R-multiple not displaying on Reflection page — shows "—" (BLG-FE-79) | Firm |
| S2-03 | EPIC-01 | AI endpoint per-endpoint rate limiting hardening — POST /ai/daily-briefing and POST /ai/chat (BLG-OPS-81) | Firm |
| S2-04 | EPIC-01 | AI response injection risk assessment threat model (BLG-GOV-146) | Firm |
| S2-05 | EPIC-01 | AI feature advisory disclaimer visibility assessment — §13 compliance (BLG-GOV-147) | Conditional |
| S2-06 | EPIC-01 | API contract review checklist for AI advisory endpoints (BLG-GOV-148) | Conditional |
| S2-07 | EPIC-02 | Nightly stop computation CI simulation tests — trailing stop, rebalance exit, inv-vol sizing (BLG-QA-65) | Firm |
| S2-08 | EPIC-02 | Strategy signal regression test specification document (BLG-QA-66) | Firm |
| S2-09 | EPIC-02 | AI chat response schema validation tests (BLG-QA-67) | Conditional |
| S2-10 | EPIC-02 | §13 boundary test suite for AI advisory endpoints (BLG-QA-68) | Conditional |
| S2-11 | EPIC-03 | Strategy Benchmark page: compare live trades against backtest — 2 DB tables, 3 endpoints, full frontend page (BLG-FEAT-53) | Firm |
| S2-12 | EPIC-03 | Morning briefing progressive disclosure — expand/collapse sections with localStorage persistence (BLG-FE-80) | Firm |
| S2-13 | EPIC-03 | Background scheduler health monitoring endpoint GET /health/scheduler (BLG-OPS-79) | Conditional |
| S2-14 | EPIC-03 | Measure live latency for POST /ai/daily-briefing and POST /ai/chat (BLG-OPS-78) | Conditional |
| S2-15 | EPIC-03 | Render deployment rollback procedure documentation (BLG-OPS-80) | Conditional |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-52 (Trade tagging) | Gate-conditional: Arc 4 PO-02 (6+ months AI journal entries) — gate clears ~2026-12 | ~v6.5+ |
| BLG-QA-63 (axe-core a11y) | Gate-conditional: Arc 5 frontend feature set not yet fully stabilised | TBD |
| BLG-OPS-76 (Enhanced health check) | Gate-conditional: BLG-OPS-25 (automated staging smoke test) not complete | TBD |
| BLG-OPS-77 (Data provider risk assessment) | Gate-conditional: BLG-OPS-71 (system threat model) not complete | TBD |
| BLG-GOV-137 (API contract version tagging) | Gate-conditional: tooling assessment confirming drift detection value | TBD |
| BLG-GOV-138 (Sprint velocity trend alert) | Gate-conditional: velocity_metrics.md path deviation not yet resolved | TBD |
| BLG-GOV-139 (Regression impact analysis at sprint planning) | Gate-conditional: tooling approach identification needed | TBD |
| BLG-GOV-149 (AI response caching evaluation) | Provisional-Target: Unscheduled — not v6.3 scope | Unscheduled |
| SI-02 frontend (Behavioural Drift Detection UI) | Gate not met: ~15 closed trades; gate requires 20; estimated ~2026-09 | ~v6.5+ |
| All other backlog items below P2 or gate-blocked | Priority or gate condition not met for v6.3 | Future |

### Supersession note

Superseded by: v6.3 ship — 2026-06-30
Changelog: docs/product/changelog.md#v63--strategy-benchmark-ai-security--quality-infrastructure--2026-06-30
Verification report: claude/cycles/2026-06-26__release-v6.3/verification_report.md
Cycle: 2026-06-26__release-v6.3
