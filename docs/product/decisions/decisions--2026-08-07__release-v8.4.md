Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v8.4
Cycle: 2026-08-07__release-v8.4
Last Updated: 2026-08-08

Superseded by: v8.4 ship — 2026-08-08
Changelog: docs/product/changelog.md#v8.4
Cycle: 2026-08-07__release-v8.4

## Planning Decisions — v8.4 User-Facing Reporting & Full-Capacity Debt Clearance

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Lead scope with `BLG-FE-141` (Avg P&L/Trade column) as the primary build-and-ship user feature | Directly ungated, ready, genuinely-user-facing feature-build item in the backlog this cycle; already carries an explicit 2026-08-06 PO acceptance decision and `Provisional-Target: v8.4` | Product Owner (delegated authority, per explicit user instruction "prioritise user features") | 2026-08-07 |
| Size scope to ~28 days (top of the confirmed ~24-28 day capacity band) | Explicit user instruction ("use full capacity") | Product Owner (delegated authority) | 2026-08-07 |
| Weight the remaining 29 stories toward execution/debt scope (API/spec debt, backend hardening, frontend code health, ops, QA) over governance-process scope | Most recent rebalance (`2026-07-28__scheduled`) reported the Skill-Silo Alert as a 2nd consecutive worsening reading (65.8%); `release_planning_prompt.md §3` rotation guideline recommends leading the next release's EPIC table with execution-heavy scope when the alert has worsened. Result: only 2 of 30 stories (`BLG-GOV-286`, `BLG-GOV-212`) are governance-process-shaped | Head of Specs Team / PMO Lead | 2026-08-07 |
| Promote `BLG-FEAT-78` into scope (EPIC-01/ST-31); correct its stale `Gate criteria` field | Gate condition (`BLG-FE-116` ships) confirmed met — `BLG-FE-116` shipped v7.5 (retired 2026-07-20). Field was never updated after shipping; same failure mode `BLG-GOV-286` (also in this cycle's scope) exists to prevent. This is a genuine 2nd user-facing item this cycle, directly strengthening the "prioritise user features" honouring | Head of Specs Team | 2026-08-07 |
| Exclude `BLG-OPS-51` despite otherwise qualifying on priority/readiness grounds | Gate genuinely not met — `claude_audit_log` 6-month-age threshold clears ~2026-11, still ~3 months out | Head of Specs Team | 2026-08-07 |
| Defer `BLG-FEAT-73`/`BLG-FEAT-74` again without a fresh live gate re-check | Both remain on their prior confirmed-unmet status from `2026-07-28__scheduled`; no sprint has executed since that reading to plausibly have changed the underlying data. Neither is in `returned_to_backlog` status from v8.3 (both were parked pre-candidate-stage at v8.3), so the STEP 1.4a Perennial-Return Check does not require a fresh active PO disposition this cycle | Product Owner (delegated authority) | 2026-08-07 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| `ST-02` (openapi.yaml structural fix) sequenced before `ST-20` (endpoint coverage baseline) | `ST-20`'s own acceptance criteria requires the endpoint list to be re-verified against the corrected `openapi.yaml`, per `ST-02`'s own AC #4 | PMO Lead | 2026-08-07 |
| `ST-11` (Alpaca close/positions backoff) noted as a same-pattern follow-on to `BLG-BE-80` (shipped v8.3, open-path backoff) | Consistent pattern extension, no new design decision required | Backend Engineering Patterns Owner | 2026-08-07 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| — | — | None — no escalation raised this cycle | — | — |

*(None)*

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-08-07__release-v8.4
