Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v3.7
Cycle: 2026-05-18__release-v3.7
Last Updated: 2026-05-18

## Release Scope — v3.7 Signal-to-Watchlist Workflow + Arc 2 Completion + Governance Hardening

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Signals-to-Watchlist workflow: replace Add Position CTA with Add to Watchlist on signal cards (BLG-FE-33); trade plan form signal context panel (BLG-FE-34) |
| S2-02 | EPIC-02 | Arc 2 PT-04 Setup Quality Score — deterministic 0–100 score from own trade history; gate: Product Owner must confirm 20+ closed trades (conditional) |
| S2-03 | EPIC-03 | Governance hardening patches deferred from v3.6: execution_prompt.md sub-step 10a (deviations_filed atomic write), backlog.md verify guidance, spec_references path verify guidance; qa_evidence_template.md BLG-GOV-19 criterion 3 fail-path |
| S2-04 | EPIC-04 | Tech debt clearance: BLG-QA-20 (database stub conftest), BLG-OPS-16 (pycache git hygiene), BLG-FE-35 (Research page font staging sign-off), BLG-GOV-23 (scored_initiatives.md refresh) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| PO-02 Journal Pattern Recognition | Data density gate not met: requires 6+ months AI-summarised journal entries; AI Journal live ~1 month (since v2.8 2026-04-20) | v3.8+ when gate met |
| PO-03 Behavioural Error Taxonomy | Requires PO-01 + PO-02 data foundation | v3.8+ |
| PO-04 Reflection ↔ Outcome Correlation | Requires PO-01 + PO-02; gate: 50+ trades with plans | v3.8+ |
| EPIC-02 (S2-02 PT-04) | Conditional defer: if Product Owner cannot confirm 20+ closed trades at design gate, EPIC-02 defers to v3.8 | v3.8 (if gate not met) |
| BLG-FE-27 | Nav bar redesign exploration — P3, non-blocking, design exploration only | Arc 3/4 context |
| BLG-FEAT-20 | Net-of-costs performance tracking — Arc 3/4 data model context | Arc 3/4 context |
| BLG-OPS-13 | API performance baseline re-run — requires live staging environment | Before next baseline review |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-05-18__release-v3.7
