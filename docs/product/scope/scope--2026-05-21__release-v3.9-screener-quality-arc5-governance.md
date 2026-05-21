Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v3.9
Cycle: 2026-05-21__release-v3.9
Last Updated: 2026-05-21

## Release Scope — v3.9 Screener Quality & Reliability + Arc 5 Red Flag Journal + Governance Patches

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Screener data quality fixes — Yahoo Finance crumb/401 rate-limiting (BLG-TECH-10), sector/industry null bug (BLG-BE-10), invalid ticker removal — DAY / PHNX.L (BLG-BE-11) |
| S2-02 | EPIC-01 | Screener UX — degraded-run warning banner when OHLCV failure rate exceeds 20% (BLG-FE-38) |
| S2-03 | EPIC-02 | Ticker Universe enhancements — strip .L suffix from display labels (BLG-FE-37); add company_name column and display (BLG-BE-12) |
| S2-04 | EPIC-03 | Arc 5 Red Flag Journal (SI-03) — auto-populated log of strategy overrides, skipped checklists, dismissed prompts; backend + frontend display |
| S2-05 | EPIC-04 | Governance & process carry-forward patches — execution_prompt.md test_scenarios + createPageUrl guidance (CF-2, CF-4); sprint_planning_prompt.md planning-deferred status (CF-5); BLG-GOV-25 dry-run support for plan release + delivery verification; DoQ QA evidence pre-merge enforcement (CF-3) |

### Conditional scope

| S2-ID | Epic | Description | Gate |
|-------|------|-------------|------|
| S2-06 | EPIC-05 | PT-04 Setup Quality Score — backend endpoint + frontend display (BLG-FEAT-25) | Product Owner confirms 20+ closed trades before sprint planning seals |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| SI-02 Behavioural Drift Detection | Gate: requires PO-01 + PO-03 data foundation not yet established | v4.0 horizon |
| BLG-FEAT-26–35 | Gate: screener/PT-04 history requirements (30–60 days) not met | TBD |
| BLG-QA-21–23 | Gate: PT-04 shipped (Arc 2 complete) | TBD |
| BLG-OPS-17–24 | Gate: 30–60 days operational history | TBD |
| BLG-GOV-26–29 | Gate conditions not met | TBD |
| PT-04 (if gate unmet) | Gate not met at sprint planning — deferred_at_planning | v3.10+ |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-05-21__release-v3.9
