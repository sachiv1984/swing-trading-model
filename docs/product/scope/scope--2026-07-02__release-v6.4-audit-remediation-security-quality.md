Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v6.4
Cycle: 2026-07-02__release-v6.4
Last Updated: 2026-07-02

## Release Scope — v6.4 Audit Remediation, Security Hardening & Strategy Benchmark Enhancement

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | BLG-BE-40 — Signal generation reads deprecated `tickers` table instead of `ticker_universe` |
| S2-02 | EPIC-01 | BLG-SEC-01 — Sanitise `context_opts.ticker` before system prompt injection (POST /ai/chat) |
| S2-03 | EPIC-01 | BLG-SEC-02 — Validate ticker/market strings at signal write time (screener pipeline) |
| S2-04 | EPIC-02 | BLG-GOV-150 — Fix governance version-sync drift |
| S2-05 | EPIC-02 | BLG-GOV-151 — Document hygiene cleanup |
| S2-06 | EPIC-02 | BLG-GOV-152 — Close structural reliability gaps (incl. FI-P3-01/FI-P3-02/FI-P4-01 re-target) |
| S2-07 | EPIC-02 | BLG-GOV-153 — Audit & governance process fixes |
| S2-08 | EPIC-03 | BLG-FEAT-54 — Add Open Positions panel to Strategy Benchmark page |
| S2-09 | EPIC-03 | BLG-UX-01 — Improve AI daily briefing disclaimer text contrast |
| S2-10 | EPIC-03 | BLG-UX-02 — Improve AI chat widget footer disclaimer contrast and add test coverage |
| S2-11 | EPIC-03 | BLG-OPS-82 — Add v6.3 endpoints to `api_performance_baseline.md` |
| S2-12 | EPIC-03 | TEST-GAP-EPIC-01 — Playwright coverage for ST-01 observable UI ACs (AI journal summary error states) |
| S2-13 | EPIC-03 | TEST-GAP-EPIC-03 — Playwright scenario coverage for Strategy Benchmark page |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| None | All `Provisional-Target: v6.4` candidates are in scope | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-07-02__release-v6.4
