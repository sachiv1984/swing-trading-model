Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v3.0
Cycle: 2026-04-25__release-v3.0
Last Updated: 2026-04-28

Superseded by: v3.0 ship — 2026-04-27
Changelog: docs/product/changelog.md#v30
Verification report: claude/cycles/2026-04-25__release-v3.0/verification_report.md
Cycle: 2026-04-25__release-v3.0

---

## Release Scope — v3.0 Arc 1 Remainder: Screener Engine & Results Page

### Items in scope

| S2-ID | EPIC | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | DS-01 Strategy-Rules Screener Engine — ticker universe data model, OHLCV data pipeline, ATR + regime detection + signal scoring engine, batch orchestration, screener API endpoints (GET /screener/results, POST /screener/run) |
| S2-02 | EPIC-02 | DS-02 Screener Results Page — frontend implementation of screener results view per screener_results.md |
| S2-03 | EPIC-02 | DS-07 Watchlist Promotion Flow — one-click promotion from screener result to watchlist |
| S2-04 | EPIC-02 | BLG-FE-18 Screener News Panel Attachment — wire GET /news/{ticker} to screener results page per screener_results.md §9 |
| S2-05 | EPIC-03 | BLG-OPS-12 External API Health Check Extension — Alpaca + Yahoo Finance status in GET /health |
| S2-06 | EPIC-03 | BLG-OPS-14 AI Journal Monitoring Metrics — AI usage/error/latency section in GET /health |
| S2-07 | EPIC-03 | TEST-GAP-ST14 AI Audit Service Unit Tests — ai_audit_service.py unit test coverage |
| S2-08 | EPIC-03 | BLG-FE-19 Keyboard Shortcuts — 'n', 'w', 'r' shortcut keys for trading actions |
| S2-09 | EPIC-04 | v2.9 Deferred Patch: execution_prompt.md §2 EPIC execution_state.json owner designation |
| S2-10 | EPIC-04 | v2.9 Deferred Patch: execution_prompt.md §3.1.A test_scenarios field population note |
| S2-11 | EPIC-04 | OA-v29-01: prompt_change_log.md retrospective entries for sprint_planning_prompt.md |
| S2-12 | EPIC-04 | BLG-FEAT-18 Consecutive Losing Streak Metric — analytics computation + metrics spec entry |
| S2-13 | EPIC-04 | BLG-AI-02 Model Version Contract for AI Journal — Claude model version specification document |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| DS-04 Earnings Calendar Integration | No spec exists; independent of screener engine flow; M effort | v3.1 |
| BLG-FEAT-13 Feature Flags | P3, M effort; lower priority than Arc 1 delivery | v3.1 |
| BLG-FEAT-19 Monthly P&L Summary Report | P2, S effort; Arc 2 reporting scope; deferred to keep v3.0 focused on Arc 1 | v3.1 |
| BLG-FE-16 React Component Inventory | P3, M effort; capacity constraint given DS-01 H effort | v3.1 |
| BLG-GOV-11 Cycle Artefact Inventory | P3, M effort; capacity constraint | v3.1 |
| BLG-OPS-13 API Performance Baseline Update | Requires live environment and human coordination — cannot be automated | Ops OA |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-04-25__release-v3.0
