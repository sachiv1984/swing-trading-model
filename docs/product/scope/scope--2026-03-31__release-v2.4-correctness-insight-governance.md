Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v2.4
Cycle: 2026-03-31__release-v2.4
Last Updated: 2026-04-03

Superseded by: v2.4 ship — 2026-04-03
Changelog: docs/product/changelog.md#v24
Verification report: claude/cycles/2026-03-31__release-v2.4/verification_report.md
Cycle: 2026-03-31__release-v2.4

---

## Release Scope — v2.4 Correctness, Insight & Governance Hardening

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Backend correctness & alert reliability — ATR pence→GBP fix (BLG-BE-05), alert notification deduplication (BLG-BE-06), R-Multiple stop price exposure (BLG-BE-04) |
| S2-02 | EPIC-02 | Frontend & UX polish — P&L (GBP) column fix (BLG-FE-06), user-facing error message mapping (BLG-FE-03) |
| S2-03 | EPIC-03 | Spec debt resolution — portfolios table reconciliation (BLG-SPEC-D15), trade_history table reconciliation (BLG-SPEC-D16) |
| S2-04 | EPIC-04 | Weekly trading digest — backend endpoint + frontend component (BLG-FEAT-14) |
| S2-05 | EPIC-05 | Operational readiness — Render tier review (BLG-OPS-10), API performance baseline (BLG-OPS-05), slippage test scenarios (TEST-GAP-EPIC-05-SLIP), cycle velocity metric (BLG-GOV-09) |
| S2-06 | EPIC-06 | Governance engine maintenance — action-now execution_prompt.md patches (LL-v2.2-EX-01/02/04), deviation compliance patch (v2.3 Friction Item 1), delegation model update + delegation log check (v2.3 Friction Items 2 and CF-2), sealing simplification (BLG-GOV-03) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-08 — Engine prompt compression (roadmap_prompt + release_planning_prompt) | L effort (~3–5 days); exceeds available sprint bandwidth given backend capacity ceiling and action-now governance priority | v2.5 |
| BLG-FEAT-13 — Gated feature rollout capability | Provisional-Target v2.5; not horizon-planned for v2.4 | v2.5 |
| BLG-TECH-05 — Prometheus metrics endpoint | P3; deferred until multi-user scale or explicit operational need | v2.x (conditional) |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-03-31__release-v2.4
