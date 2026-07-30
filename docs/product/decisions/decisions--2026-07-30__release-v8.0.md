Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v8.0
Cycle: 2026-07-30__release-v8.0
Last Updated: 2026-07-30

## Planning Decisions — v8.0 Data Integrity, Security Follow-Through & Operational Hardening

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Scope this release entirely from the ungated backlog pool (19 items), rather than waiting on any roadmap-scoped anchor | Roadmap Now horizon has been empty since `2026-07-24__scheduled`; STEP 8.1 Option (b) deferred again at `2026-07-28__scheduled`; no ungated P1 user-facing feature item exists in the backlog (the 4 ungated P1 items are all narrow accessibility/security follow-through fixes surfaced by v7.10's own delivery). Same backlog-driven pattern as v7.8/v7.9/v7.10. | Product Owner (via Release Planning Engine, delegated authority) | 2026-07-30 |
| Remove `BLG-OPS-48` from the initially-selected 20-item scope | Self-caught during write-up: the item carries a real `**Gate date:** 2026-11-01` that the automated ungated-pool scan missed (it only matched `**Gate criteria:**`/`**Gate:**` field names). The gate clears ~3 months after this cycle's date — not ready. See `run_manifest.md` for the full detection account. | Product Owner (via Release Planning Engine, delegated authority) | 2026-07-30 |
| Size scope to the top of the confirmed ~24-28 day capacity band (~26.25 days midpoint, ~94-109% utilisation) by default | No explicit user capacity/timebox instruction was given this session; the engine applied the same full-capacity pattern used at the three most recent prior releases (v7.8, v7.9, v7.10) in the absence of a contrary instruction | Product Owner (via Release Planning Engine, delegated authority) | 2026-07-30 |
| Group the 19 stories into 6 thematic EPICs (Data Model & Spec Integrity, Security Hardening, QA & Test Infrastructure, Operations & Reliability, Frontend Technical Debt, Governance & Engineering Process Hardening) rather than one EPIC per story | No explicit grouping instruction was given this session; applied the same thematic-grouping pattern used at v7.10 | Product Owner (via Release Planning Engine, delegated authority) | 2026-07-30 |
| Include `BLG-GOV-263` (governance-classified, but a genuine engineering fix) in EPIC-06 despite the Product Value Ratio advisory generally favouring non-process scope | Item has recurred and compounded across 3 consecutive multi-EPIC cycles (v7.6/v7.7/v7.8: 10/11 → 11/12 branches affected) per its own backlog entry's escalation history; resolving it now removes a standing recurring-friction source rather than deferring it further | Product Owner (via Release Planning Engine, delegated authority) | 2026-07-30 |
| Exclude BLG-FEAT-73/BLG-FEAT-74 and the Arc 5 pre-entry/compliance-gateway UX cluster (12 items, escalated P3→P1 on 2026-07-27/28) from firm scope | All carry unmet gate criteria (SI-02 NOT MET, §13 pre-clearance not run, etc.); the P1 escalation was recorded as "a value-judgment override only, not a gate-clearance" — consistent with the standing perennial-return disposition | Product Owner | 2026-07-30 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| No hard cross-EPIC sequencing dependency declared | All 6 EPICs are independent workstreams touching disjoint code surfaces (data model/spec, security, QA tooling, operations, frontend, governance prompts) — no EPIC's acceptance criteria depends on another EPIC's output | Product Owner | 2026-07-30 |
| Within EPIC-04, S2-14 (Telegram GitHub Actions secrets) sequenced before/alongside S2-13 (5xx health-check alerting) | Both rely on the same `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` credential pair; S2-13's alert cannot be confirmed to actually reach anyone until S2-14's secrets are configured | Product Owner | 2026-07-30 |
| EPIC-02 (Security Hardening) routed through Design Gate before Sprint Planning seals | Two items (BLG-FE-135, BLG-FE-136) carry observable UI interaction acceptance criteria per CLAUDE.md's Playwright/staging-sign-off requirement | Product Owner | 2026-07-30 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations were raised this cycle; capacity outcome was `pass`, not `warn`/`fail` | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-30__release-v8.0
