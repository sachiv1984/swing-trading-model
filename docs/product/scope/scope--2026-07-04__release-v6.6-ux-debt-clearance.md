Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v6.6
Cycle: 2026-07-04__release-v6.6
Last Updated: 2026-07-06

## Release Scope — v6.6 UX & QA Debt Clearance

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Colour contrast audit sweep (BLG-FE-82) |
| S2-02 | EPIC-01 | Red Flag Journal filter state persistence (BLG-FE-40) |
| S2-03 | EPIC-02 | Audit colliding backlog IDs in backlog.md (BLG-QA-72) |
| S2-04 | EPIC-02 | database.py / _DB_STUB_FUNCTIONS manual-sync risk investigation (BLG-QA-73) |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-52 (Trade tagging) | Own gate condition (PO-02 sprint planning imminent) not met | Re-review each cycle until PO-02 becomes imminent |
| SI-02 (Behavioural Drift Detection) | Gate condition (1) not formally re-verified as cleared despite user report of 20 closed trades | Re-check once PMO Lead confirms via production query |
| PO-02/PO-04 (Arc 4 remainder) | Data-density gates not met | Re-check at next release planning readiness scan |

### Supersession note
Superseded by: v6.6 ship — 2026-07-06
Changelog: docs/product/changelog.md#v6.6
Verification report: claude/cycles/2026-07-04__release-v6.6/verification_report.md
Cycle: 2026-07-04__release-v6.6
