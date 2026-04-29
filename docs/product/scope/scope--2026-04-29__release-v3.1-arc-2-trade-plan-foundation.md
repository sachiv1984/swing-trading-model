Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v3.1
Cycle: 2026-04-29__release-v3.1
Last Updated: 2026-04-29

## Release Scope — v3.1 Arc 2 Start: Trade Plan Object & Pre-Trade Research Foundation

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Arc 2 Foundation — Trade Plan Object: data model spec authoring, backend CRUD endpoints, frontend creation flow and detail view |
| S2-02 | EPIC-02 | Pre-Trade Research View Foundation: API contract spec authoring + backend data-aggregation endpoint (frontend deferred to v3.2) |
| S2-03 | EPIC-03 | Arc 1 Completion — Earnings Calendar Integration (DS-04): backend endpoint + frontend display on screener results, watchlist, and open positions |
| S2-04 | EPIC-03 | Screener Quality & Bug Fix: UK ticker display and watchlist promotion bug (BLG-FE-20, P1), screener accuracy test protocol (BLG-QA-11), screener scenario library (BLG-QA-10) |
| S2-05 | EPIC-04 | External API Security & Governance: Alpaca key rotation policy (BLG-SEC-03), external API credential audit (BLG-SEC-04), API dependency risk register (BLG-GOV-17) |
| S2-06 | EPIC-04 | Monthly P&L Summary Reporting: month-by-month P&L breakdown complementing annual tax-year report (BLG-FEAT-19) |
| S2-07 | EPIC-04 | Governance Prompt Patches: execution_prompt.md §3.1.A reclassification backfill instruction (CF-01), execution_prompt.md STEP 8.5 output target fix (CF-02) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| PT-02 Frontend (Pre-Trade Research View UI) | Design gate required before new frontend page implementation; backend foundation delivered in v3.1 | v3.2 |
| PT-03 (Prospective Heat at Entry integration) | Depends on PT-02 frontend being live | v3.2 |
| PT-04 (Setup Quality Score) | Gate: 20+ closed trades required — data precondition not yet met | v3.2+ |
| PT-05 (Pre-Trade Entry Checklist) | Embedded in Trade Plan flow (PT-02); deferred with PT-02 frontend | v3.2 |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-04-29__release-v3.1
