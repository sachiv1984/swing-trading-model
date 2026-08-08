Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v8.5
Cycle: 2026-08-08__release-v8.5
Last Updated: 2026-08-08

## Release Scope — v8.5 Frontend Correctness, Design Consistency & Security Hardening

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Production Correctness Fixes — 2 live-staging-found P1 bugs (analytics 500, silently no-op'ing security workflow) |
| S2-02 | EPIC-02 | Security Hardening — false-positive assessment, recurring vuln re-scan cadence, key rotation runbook |
| S2-03 | EPIC-03 | Frontend Correctness Fixes — dead Tailwind muted-colour classes, AI-provenance field wiring, P&L colour convention reconciliation |
| S2-04 | EPIC-04 | Design System & Contrast Consistency Audit — 6 audit/consistency items across design tokens, empty states, theme persistence, mobile responsiveness |
| S2-05 | EPIC-05 | Frontend UX Review & Documentation — nav bar exploration, journey mapping, reusable spec authoring, deferred-trigger testing-gate closures |
| S2-06 | EPIC-06 | Analytics & Governance Process Fixes — 2 small analytics/metrics features, 2 self-caught governance-prompt gaps, 1 test-pollution fix |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-73 (SI-02 frontend build) | Gate unmet — BLG-GOV-107 conditions (≥20 closed trades with linked plans; p99 latency; score variance) not independently reconfirmed. Formally parked at `2026-08-05__release-v8.3` (STEP 1.4a.1 mandatory sunset trigger fired; PO chose Option (b)). No fresh Perennial-Return disposition required — item not in `returned_to_backlog` status, same treatment as `v8.4`. | Unscheduled — re-enters candidacy only if gate independently reconfirmed met |
| BLG-FEAT-74 (PO-05 Lightweight Replay Mode) | Gate unmet — §13 determinism pre-clearance not run; VH effort exceeds single-cycle sizing. Same `v8.3` park disposition as BLG-FEAT-73. | Unscheduled — re-enters candidacy only if §13 pre-clearance completes |
| BLG-FEAT-76 (SI-05 Phase 2 digest) | Hard-blocked on BLG-FEAT-73/BLG-FEAT-75 shipping first. | Unscheduled |
| ~119 other gate-blocked backlog items (per `scripts/scan_backlog_gate_conditions.py`) | Gate conditions not met — see `run_manifest.md §STEP 1` for the full scan output. | Various — gate-dependent |
| ~121 remaining ungated P3 items not selected this cycle | Capacity reached at ~27.15 days (top of the ~24-28 day band); this cycle's selection weighted toward P1/P2 items and the largest available ready user-facing/frontend pool. | Candidates for `v8.6` and beyond |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-08-08__release-v8.5
