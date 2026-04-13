Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v2.6
Cycle: 2026-04-11__release-v2.6
Last Updated: 2026-04-13
Superseded by: v2.6 ship — 2026-04-13
Changelog: docs/product/changelog.md#v2.6
Verification report: claude/cycles/2026-04-11__release-v2.6/verification_report.md
Cycle: 2026-04-11__release-v2.6

---

## Planning Decisions — v2.6 Backend Integration Completion, Test Automation & Governance Hardening

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include EPIC-01 backend integration (Reports + Signals) | P1 backlog items — data consistency risk between Base44 SDK and FastAPI backend; P&L figures may diverge between pages | Product Owner | 2026-04-11 |
| Include EPIC-02 test automation & CI | P1 (BLG-QA-09 collection errors) and P2 (CI workflow) — unblocks automated regression detection; fee drag specs complete outstanding SC-FEE-01–06 coverage | Product Owner | 2026-04-11 |
| Include EPIC-03 frontend UX polish | P3 items with meaningful UX value — 6-card Trade History bar squeeze, column header legibility, flexible sort — all identified at staging; grouped as polish epic | Product Owner | 2026-04-11 |
| Include EPIC-04 governance & spec debt | Two v2.5 carry-forward action items (CF-1, CF-2) require prompt patches; BLG-GOV-15 addresses medium-priority decision_log.md guard gap found in audit; BLG-FE-09 frontend performance budget is a spec-only item | Product Owner | 2026-04-11 |
| Defer BLG-GOV-08 (engine compression) | P3, L effort — would consume disproportionate sprint capacity vs. user/governance value; defer to v2.7 | Product Owner | 2026-04-11 |
| Defer BLG-GOV-11, BLG-GOV-14 | P3 — complex governance scope; deprioritised vs. concrete P1/P2 delivery | Product Owner | 2026-04-11 |
| Defer BLG-SPEC-D17, BLG-QA-11 | P3 — both useful but not urgent vs. higher-priority items | Product Owner | 2026-04-11 |
| Defer CF-3 (exec_state schema) | Low priority — execution_state.json test_scenarios ambiguity does not block any current workflow | PMO Lead | 2026-04-11 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 + EPIC-02 in Sprint 1 | P1 items deliver highest user-facing and infra value; larger effort EPICs scheduled first per capacity phasing recommendation | PMO Lead | 2026-04-11 |
| EPIC-03 + EPIC-04 in Sprint 2 | P3 polish and governance patches have lower urgency; UX design decisions for EPIC-03 can be obtained pre-sprint | PMO Lead | 2026-04-11 |
| ST-05 (CI workflow) depends on ST-04 (collection errors) | Phase B of CI workflow (pytest tests/) requires collection errors to be fixed first; Phase A can ship without ST-04 but full value requires it | QA & Testing Owner | 2026-04-11 |

### Accepted risks

None.

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-04-11__release-v2.6
