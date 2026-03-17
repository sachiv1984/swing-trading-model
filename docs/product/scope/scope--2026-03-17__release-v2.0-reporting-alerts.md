Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v2.0
Cycle: 2026-03-17__release-v2.0
Last Updated: 2026-03-17

---

## Release Scope — v2.0 Reporting & Alerts

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-03 | 3.5 Alerts & Notifications — email/SMS alerts, in-app notification feed, configurable user notification preferences. **Conditional: EPIC-03 may not enter sprint execution until QA gate 3 (DL-003) is cleared.** |
| S2-02 | EPIC-02 | 4.1b Tax-Year P&L Statement — server-side generated GBP-adjusted tax-year report covering all realised gains and losses. Realised vs unrealised P&L distinction (BLG-NEW-06 pre-work merged). Dedicated report endpoint required. |
| S2-03 | EPIC-01 | 4.3 Signal Exposure Enhancement — expose existing top_n and lookback_days parameters as user-facing controls on the signals page. Frontend and spec task only; backend already supports parameters (PoG POG-20260304-01 — strategy_rules.md v1.3). |
| S2-04 | EPIC-04 | BLG-BE-01 P1: GET /portfolio missing 4 fields (initial_value, net_deposits, current_drawdown_percent, peak_portfolio_value). BLG-BE-02 stretch: GET /portfolio/prospective-heat spec and implementation. |
| S2-05 | EPIC-05 | Documentation Pack: BLG-OPS-02 (production deployment runbook), BLG-DATA-01 (positions table data dictionary), BLG-TECH-07 (database migration governance standard), BLG-NEW-13 (spec coverage inventory), TEST-GAP-EPIC-02 (CohortAnalysis regression scenario — stretch). |
| S2-06 | EPIC-06 | Governance Tooling: BLG-GOV-01 (roadmap stage document consolidation — roadmap_prompt.md rewrite), BLG-GOV-02 (ideas register — replace per-file submission model). |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| 4.2 Watchlists & Screening | Roadmap Priority 2 — not to be pulled forward | post-v2.0 |
| Chart Interactivity Enhancements | Roadmap Priority 2 | post-v2.0 |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-03-17__release-v2.0
