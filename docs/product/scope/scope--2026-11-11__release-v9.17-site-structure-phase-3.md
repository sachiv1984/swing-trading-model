Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.17
Cycle: 2026-11-11__release-v9.17
Last Updated: 2026-11-11

## Release Scope — v9.17 Site Structure & Usability, Phase 3

20 items across 7 EPICs, 27.95 estimated days (the top of the confirmed ~24–28 day band, per "use full capacity"). Acceptance criteria: `claude/cycles/2026-11-11__release-v9.17/stage4_backlog_slice.md`.

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Decision-first Positions table (`BLG-FE-260`, P2) |
| S2-02 | EPIC-01 | Card layout for Positions on narrow screens (`BLG-FE-261`) |
| S2-03 | EPIC-01 | One warning strip in place of the four banners above the Positions table (`BLG-FE-262`) |
| S2-04 | EPIC-01 | Grace period shown in one place, linked from the others (`BLG-FE-257`) |
| S2-05 | EPIC-02 | Single Journal area (`BLG-FE-258`) |
| S2-06 | EPIC-02 | One Performance page from Reports and Performance Analytics (`BLG-FE-259`) |
| S2-07 | EPIC-02 | Tabs or a section index on Trade Plan and Strategy Benchmark (`BLG-FE-263`) |
| S2-08 | EPIC-03 | Remaining pages moved onto the semantic colour tokens (`BLG-FE-265`) |
| S2-09 | EPIC-04 | Record when the nightly job last moved each position's stop (`BLG-BE-205`) |
| S2-10 | EPIC-04 | Today list "Stops moved" group, TL-09/TL-10 (`BLG-FE-254` remainder, P2) |
| S2-11 | EPIC-05 | Close a linked trade plan when its position closes, with backfill (`BLG-BE-211`, P2) |
| S2-12 | EPIC-05 | Reset the Trade Plan pre-entry acknowledgement when the check result changes (`BLG-FE-278`, P2) |
| S2-13 | EPIC-05 | Research View "Create Trade Plan" carries the market (`BLG-FE-281`, P2) |
| S2-14 | EPIC-05 | Pre-fill the Trade Plan stop from §5 and flag a differing typed stop (`BLG-FE-282`, P2) |
| S2-15 | EPIC-06 | Find and fix the on-demand Yahoo failures on production (`BLG-OPS-217`, P2) |
| S2-16 | EPIC-06 | Weekly alert when market-data call volume passes 2× baseline (`BLG-OPS-195`) |
| S2-17 | EPIC-06 | Batch signal sizing stays within available cash after fees (`BLG-BE-178`) |
| S2-18 | EPIC-07 | §1.3a gate clearance may set a gate-worded Provisional-Target to TBD (`BLG-GOV-419`) |
| S2-19 | EPIC-07 | Define or remove the Positions page's 2R Exit Zone threshold (`BLG-SPEC-202`) |
| S2-20 | EPIC-07 | Drift detector ignores rollback-only index names (`BLG-QA-223`, P4) |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| `BLG-TECH-21` (P2) | Standing §1.4c override: needs a dedicated single-EPIC release | v10.0 |
| `BLG-UX-08` (P2) | Gated on every other Site Structure & Usability programme item being complete | v9.18 (programme Close-out) |
| `BLG-FEAT-73` (P1) | Data-quality gate; its re-check needs a production `trade_plans` count the governed environment cannot read | Unscheduled |
| `BLG-GOV-200`, `BLG-GOV-201` | No acceptance criteria (v9.16 closure §6 row 5: add ACs or kill before seating) | Unscheduled |
| `BLG-OPS-201` | Needs a full calendar month of production data | Not before 2026-12-01 |
| 160 other ready items (62.80 days) | Capacity | Later releases |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-11-11__release-v9.17
