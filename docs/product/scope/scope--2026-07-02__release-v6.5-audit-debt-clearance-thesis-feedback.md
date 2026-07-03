Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v6.5
Cycle: 2026-07-02__release-v6.5
Last Updated: 2026-07-03

Superseded by: v6.5 ship — 2026-07-03
Changelog: docs/product/changelog.md#v6.5
Verification report: claude/cycles/2026-07-02__release-v6.5/verification_report.md
Cycle: 2026-07-02__release-v6.5

## Release Scope — v6.5 Audit Debt Clearance, Backlog Debt Clearance & AI Thesis Feedback Loop

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-02 | BLG-OPS-83 — Add v6.4 endpoint (`GET /strategy/benchmark/open-positions`) to `api_performance_baseline.md` |
| S2-02 | EPIC-02 | TEST-GAP-EPIC-03-v64 — Playwright coverage for Strategy Benchmark Panel 0 (Open Positions) rendering |
| S2-03 | EPIC-02 | BLG-QA-61 — Review `signals_scenarios.md` against ST-01 signal sizing model changes |
| S2-04 | EPIC-03 | BLG-FE-46 — Claude thesis generation user feedback mechanism |
| S2-05 | EPIC-03 | BLG-FEAT-41 — Claude thesis adoption rate metric |
| S2-06 | EPIC-01 | BLG-GOV-157 — Lifecycle/prompt/state wording and consistency fixes (AUD-007, -012, -013) |
| S2-07 | EPIC-01 | BLG-GOV-158 — README.md document hygiene sweep (AUD-006, -009, -010, -015) |
| S2-08 | EPIC-01 | BLG-GOV-159 — OPERATIONAL_GUIDE/prompt version-sync drift (AUD-001, -003, -016) |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| BLG-SPEC-35 (PO-02 §13 boundary review) | Gate condition ("PO-02 sprint planning imminent") not met | Re-review each release planning cycle |
| SI-02 (Behavioural Drift Detection) | Data-density gate not met (last checkpoint 6/11 closed trades vs 20 required; stale) | Re-check at next release planning readiness scan |
| PO-02/PO-04 (Arc 4 remainder) | Data-density gates not met | Re-check at next release planning readiness scan |
| Remaining actionable-now backlog items not listed above | Scope sized to items with clearest immediate justification (audit SLA, explicit v6.5 provisional targets, 3-cycle carry-forward, Skill-Silo pull-forward mandate) | Available for v6.6 scoping |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-07-02__release-v6.5
