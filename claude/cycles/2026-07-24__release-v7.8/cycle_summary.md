Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v7.8
Cycle: 2026-07-24__release-v7.8
Design Gate Required: true
Last Updated: 2026-07-24

# Cycle Summary — v7.8 Release Visibility & Engineering Hardening

## Overview

12 EPICs, all firm scope (no conditional/gate-blocked items). Scoped entirely from the `IW-20260724-01` idea-intake backlog addition (34 standalone items), per the `2026-07-24__scheduled` rebalance's own STEP 8.1 Option (b) rationale: no roadmap-named anchor set existed this cycle, so this routine performed the version-naming and scope-selection deferred by that decision.

## Scope Selection

No P0/P1 production-correctness items existed to fast-track (STEP 8.0 found 0 this rebalance). Selection favoured P2 items and user-facing/accessibility value given the Product Value Ratio Advisory (0.42), balanced against overdue security/engineering hardening. Full rationale: `run_manifest.md`, decisions: `decisions--2026-07-24__release-v7.8.md`.

## Perennial-Return Disposition

`BLG-FEAT-73` (SI-02 frontend) and `BLG-FEAT-74` (PO-05 Replay Mode) reached a 2nd consecutive return (STEP 1.4a threshold) and are **excluded** from v7.8, with PO disposition Option (b) — removed from horizon. Neither gate has moved since v7.7's own exclusion of these same items. See `run_manifest.md` STEP 1.4a for full detail.

## Scope

| EPIC-ID | Backlog source | Title | Effort | Midpoint (days) |
|---------|-----------------|-------|--------|------------------|
| EPIC-01 | `BLG-FE-128` | In-app "what's new" panel | M | 2.0 |
| EPIC-02 | `BLG-FEAT-84` | Automated Telegram changelog digest | S | 1.0 |
| EPIC-03 | `BLG-FE-127` | Accessibility pass on v7.7 notification UX | S | 1.0 |
| EPIC-04 | `BLG-FE-125` | Dark-mode contrast audit (Base44 pages) | M | 2.0 |
| EPIC-05 | `BLG-FEAT-81` | Monthly realized P&L CSV export | S | 1.0 |
| EPIC-06 | `BLG-FEAT-82` | AI usage spend trend dashboard | M | 2.0 |
| EPIC-07 | `BLG-SEC-20` | API key rotation-and-audit cadence | S | 1.0 |
| EPIC-08 | `BLG-SEC-21` | Rate-limiting review, public endpoints | M | 2.0 |
| EPIC-09 | `BLG-BE-71` | Shared retry/backoff decorator | M | 2.0 |
| EPIC-10 | `BLG-QA-117` | Flaky-test quarantine process | M | 2.0 |
| EPIC-11 | `BLG-QA-119` | Contract tests, pilot endpoints | M | 2.0 |
| EPIC-12 | `BLG-OPS-117` | API contract heading-level CI lint | S | 1.0 |

**Total: ~19.0 days midpoint against ~24–28 day capacity ≈ 68–79% utilisation.** No over-allocation, no capacity WARN.

EPIC-01, 03, 04, 05, 06 conditional pending Design Gate (RISK-01: 5 have observable UI ACs). EPIC-02, 07–12 have no Design Gate dependency.

## Design Gate

`design_gate_required = true` — EPIC-01, 03, 04, 05, 06 have observable UI acceptance criteria. Must run `run design-gate --cycle 2026-07-24__release-v7.8` and PASS (or record a bypass) before `plan sprint` may seal.

## Risks

RISK-01 (Release-level, Medium): Design Gate hard prerequisite, 5 UI-facing EPICs. RISK-02 (EPIC-09, Low): shared decorator touches live external call sites — bounded to proof-of-pattern on one call site. RISK-03 (EPIC-11, Low): pilot endpoint selection needs Head of Engineering confirmation before implementation. RISK-04 (EPIC-08, Low): rate-limiting findings could exceed remaining capacity — bounded by remediate-or-accept-risk AC.

## Escalations

None raised this cycle.

## Governance Note

`.claude_current_state.json.status` set to `Release_Planning_Complete` (canonical `lifecycle_schema.json` enum value) rather than this prompt's literal STEP 9 wording (`Published`) — see `run_manifest.md` §"STEP 7/9 — Global State Sync: Status-Value Conflict Resolution" for the conflict and resolution rationale. Flagged as a deferred prompt-maintenance patch, not an open escalation.

## Next Steps

1. `run design-gate --cycle 2026-07-24__release-v7.8` (required — 5 UI-facing EPICs)
2. `plan sprint --cycle 2026-07-24__release-v7.8` (only after Design Gate PASS or recorded bypass)

```yaml
artifacts.cycle_summary: present
```
