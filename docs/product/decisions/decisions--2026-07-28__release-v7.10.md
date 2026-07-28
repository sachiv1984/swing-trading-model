Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v7.10
Cycle: 2026-07-28__release-v7.10
Last Updated: 2026-07-28

## Planning Decisions — v7.10 Reliability, Security & Contract Hardening

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Scope this release entirely from the ungated backlog pool (23 items), rather than waiting on any roadmap-scoped anchor | Roadmap Now horizon has been empty since `2026-07-24__scheduled`; STEP 8.1 Option (b) deferred again at `2026-07-28__scheduled`; no ungated P1/P2 user-facing item exists in the backlog. Same backlog-driven pattern as v7.8/v7.9. | Product Owner (via explicit user instruction) | 2026-07-28 |
| Size scope to the top of the confirmed ~24-28 day capacity band (~26.15 days midpoint, ~93-109% utilisation) rather than a conservative mid-band fill | Explicit user instruction: "use full capacity" | Product Owner (via explicit user instruction) | 2026-07-28 |
| Group the 23 stories into 6 thematic EPICs (Backend Reliability, Security Hardening, QA & Test Infrastructure, API Contract & Spec Debt, Frontend Technical Debt & Accessibility, Governance Process Hardening) rather than one EPIC per story | Explicit user instruction: "try to group stories into the right epics, no need for one epic per story" | Product Owner (via explicit user instruction) | 2026-07-28 |
| Exclude BLG-FEAT-73/BLG-FEAT-74 and the Arc 5 pre-entry/compliance-gateway UX cluster (12 items, escalated P3→P1 on 2026-07-27/28) from firm scope | All carry unmet gate criteria (SI-02 NOT MET, §13 pre-clearance not run, "Arc 5 fully complete", "SI-02/SI-04 sprint planning imminent", etc.); the P1 escalation was recorded as "a value-judgment override only, not a gate-clearance" in `backlog.md`'s own header — consistent with the standing perennial-return disposition | Product Owner | 2026-07-28 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| No hard cross-EPIC sequencing dependency declared | All 6 EPICs are independent workstreams touching disjoint code surfaces (backend resilience/error-handling, security, QA tooling, API contract docs, frontend, governance prompts) — no EPIC's acceptance criteria depends on another EPIC's output | Product Owner | 2026-07-28 |
| EPIC-05 (Frontend Technical Debt & Accessibility) routed through Design Gate before Sprint Planning seals | Two items (BLG-FE-106, BLG-FE-122) carry observable UI rendering acceptance criteria per CLAUDE.md's Playwright/staging-sign-off requirement | Product Owner | 2026-07-28 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations were raised this cycle; capacity outcome was `pass`, not `warn`/`fail` | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-28__release-v7.10
