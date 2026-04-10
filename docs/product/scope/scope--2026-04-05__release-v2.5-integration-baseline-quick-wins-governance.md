Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v2.5
Cycle: 2026-04-05__release-v2.5
Last Updated: 2026-04-10

Superseded by: v2.5 ship — 2026-04-10
Changelog: docs/product/changelog.md#v25
Verification report: claude/cycles/2026-04-05__release-v2.5/verification_report.md
Cycle: 2026-04-05__release-v2.5

## Release Scope — v2.5 Integration Baseline, Quick Wins & Governance Debt

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | BLG-OPS-12 — Fix auth forwarding in POST /test/endpoints |
| S2-02 | EPIC-01 | BLG-OPS-13 — Sync endpoint test list with openapi.yaml |
| S2-03 | EPIC-01 | BLG-FE-07 — Fix System Status endpoint categorisation for v2.3/v2.4 routes |
| S2-04 | EPIC-02 | BLG-BE-08 — Review and document Reports page backend integration |
| S2-05 | EPIC-02 | BLG-BE-09 — Review and document Signals page backend integration |
| S2-06 | EPIC-02 | BLG-BE-07 — Investigate high external baseline latency on DB-backed endpoints |
| S2-07 | EPIC-03 | BLG-OPS-11 — Add --max-time to GitHub Actions curl calls |
| S2-08 | EPIC-03 | BLG-FE-08 — Fix Avg Slippage StatsCard gradient rendering |
| S2-09 | EPIC-03 | BLG-FEAT-15 — Fee drag metric on Trade History |
| S2-10 | EPIC-04 | BLG-GOV-10 — Fix governance_sync.yml batch push issue closure |
| S2-11 | EPIC-04 | BLG-GOV-12 — Formalise backlog entry placement standard |
| S2-12 | EPIC-04 | v2.4 deferred prompt patches (execution_prompt.md STEP 8 + delivery_verification_prompt.md STEP 8/9) |
| S2-13 | EPIC-04 | TEST-GAP-EPIC-01-v24 — Test scenarios for EPIC-01 correctness fixes |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-TECH-05 Prometheus endpoint | P3; requires multi-user scale | v3.0 or when multi-user |
| BLG-FE-09 Frontend Performance Budget | P3; new from rebalance; governance-heavy | v2.6 |
| BLG-SPEC-D17 Spec Dependency Map | P3; new from rebalance; governance-heavy | v2.6 |
| BLG-GOV-08 Engine prompt compression | P3; L effort; not urgent | v2.6+ |
| BLG-GOV-11 Cycle artefact inventory | P3; governance-heavy; deferred to avoid Skill-Silo imbalance | v2.6 |
| BLG-GOV-14 Governance Health Score | P3; new from rebalance; governance-heavy | v2.6 |
| BLG-FEAT-13 Feature rollout capability | P3; M effort; not urgent | v2.6 |
| Hook configuration fix (Friction Item 3, v2.4) | User configuration; not a sprint story | User action before sprint execution |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-04-05__release-v2.5
