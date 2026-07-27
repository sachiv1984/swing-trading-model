Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v7.8
Cycle: 2026-07-24__release-v7.8
Last Updated: 2026-07-27

Superseded by: v7.8 ship — 2026-07-27
Changelog: docs/product/changelog.md#v7.8
Verification report: claude/cycles/2026-07-24__release-v7.8/verification_report.md
Cycle: 2026-07-24__release-v7.8

## Release Scope — v7.8 Release Visibility & Engineering Hardening

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | BLG-FE-128 — In-app "what's new" panel for most recent release |
| S2-02 | EPIC-02 | BLG-FEAT-84 — Automated Telegram changelog digest after each release |
| S2-03 | EPIC-03 | BLG-FE-127 — Accessibility pass on v7.7 notification UX components |
| S2-04 | EPIC-04 | BLG-FE-125 — Dark-mode contrast audit across Base44-generated pages |
| S2-05 | EPIC-05 | BLG-FEAT-81 — Monthly realized P&L CSV export |
| S2-06 | EPIC-06 | BLG-FEAT-82 — AI usage spend trend dashboard (Gemini/Claude, per release cycle) |
| S2-07 | EPIC-07 | BLG-SEC-20 — Scheduled rotation-and-audit cadence for third-party API keys |
| S2-08 | EPIC-08 | BLG-SEC-21 — Rate-limiting review of public-facing endpoints |
| S2-09 | EPIC-09 | BLG-BE-71 — Shared retry/backoff decorator for external data calls |
| S2-10 | EPIC-10 | BLG-QA-117 — Flaky-test quarantine process for the Playwright suite |
| S2-11 | EPIC-11 | BLG-QA-119 — Contract tests for highest-traffic frontend/backend endpoints |
| S2-12 | EPIC-12 | BLG-OPS-117 — Automated lint check for API contract `##` heading level |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-73 — SI-02 Behavioural Drift Detection frontend build | 2nd consecutive perennial return; SI-02 gate remains NOT MET; PO disposition Option (b) — removed from horizon | Reopen only on new gate evidence |
| BLG-FEAT-74 — PO-05 Lightweight Replay Mode | 2nd consecutive perennial return; §13 pre-clearance never run; VH effort exceeds single-cycle sizing; PO disposition Option (b) — removed from horizon | Reopen only after §13 pre-clearance review |
| BLG-QA-122 — Broker statement reconciliation | Gate-conditional — no broker statement import mechanism exists | Deferred until broker integration or manual upload path exists |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-07-24__release-v7.8
