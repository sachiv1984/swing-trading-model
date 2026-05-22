Owner: Product Owner
Class: Planning Document (Class 4)
Status: Published
Release: v4.0
Cycle: 2026-05-22__release-v4.0
Last Updated: 2026-05-22

## Planning Decisions — v4.0 Arc 5 Analytics Foundation + Spec Closure + Gemini Compliance

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Arc 5 analytics metrics (BLG-FEAT-36/37/39) in scope as EPIC-01 | SI-01 and SI-03 are both shipped and operational; these metrics are the natural analytics layer on top of existing infrastructure; no data gate; DL-033 Provisional-Target v4.0 | Product Owner; Metrics & Analytics Owner | 2026-05-22 |
| E2E Playwright coverage for SI-01→SI-03 (BLG-QA-25) in scope as part of EPIC-01 | Active coverage gap for the RFJ pipeline; SI-03 shipped in v3.9 but no integration test covers the full override→journal path; P2, S effort | Director of Quality | 2026-05-22 |
| Ticker symbol validation (BLG-BE-15) in scope as EPIC-02 | P1 priority; prevents junk entries in the ticker universe that degrade screener results; no gate; independent of other work | Head of Backend Engineering | 2026-05-22 |
| Red flag endpoint auth/PII review (BLG-GOV-37) in scope as EPIC-02 | XS security governance effort; post-v3.9 hygiene; red flag journal endpoint went live in v3.9 without explicit PII/auth review | Cybersecurity Lead | 2026-05-22 |
| Gemini audit trail + cost tracking (BLG-GOV-35, BLG-OPS-26) in scope as EPIC-03 | Gemini has been in production since v3.8 with no audit log or cost tracking; compliance debt is growing each cycle; P2 M+S | AI Compliance Officer; FinOps | 2026-05-22 |
| CI/CD staging auto-deploy (BLG-OPS-27) in scope as EPIC-03 | Reduces manual staging sync after each main merge; enables smoke test automation downstream (BLG-OPS-25); Render free-tier impact requires build-minute filter (RISK-03) | Infrastructure Owner | 2026-05-22 |
| PT-04 Setup Quality Score as conditional scope (EPIC-04) | Gate condition (20+ closed trades) must be confirmed by Product Owner before sprint planning seals; fifth consecutive conditional inclusion | Product Owner | 2026-05-22 |
| BLG-SPEC-33/34 excluded from sprint scope | Both API contracts were authored and committed in OA-01+OA-02 (b115b9b4, 2026-05-22); items are complete and should be archived at next backlog groom | Head of Specs Team | 2026-05-22 |
| SI-02/04/05 deferred | Data-gated: all three require PO-03 data which depends on PO-02 (6+ months AI journals); earliest gate-clear ~Nov 2026; including these now would be scope inflation with no delivery path | Product Owner; Strategy Rules & System Intent Owner | 2026-05-22 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Sprint 1: EPIC-01 (Arc 5 analytics) + EPIC-02 (ticker quality + security) | Both are self-contained and independent; analytics metrics are the highest-value v4.0 deliverable; ticker validation is P1; combined effort ~5-6 days | Product Owner; PMO Lead | 2026-05-22 |
| Sprint 2: EPIC-03 (AI governance + CI/CD) + conditional EPIC-04 (PT-04) | AI governance and CI/CD work is infrastructure-adjacent; staging auto-deploy (OPS-27) sequenced last as it affects all subsequent deploys; EPIC-04 gate must be confirmed before sprint seals | Product Owner | 2026-05-22 |
| Metrics & Analytics Owner sign-off required on FEAT-36 metric definition before Sprint 1 seals | BLG-FEAT-36 introduces a new metric (SI-01 pass/fail rate by rule) requiring canonical definition; design gate dependency | Metrics & Analytics Owner | 2026-05-22 |
| Head of UX & Design sign-off required on PT-04 score badge UX before Sprint 2 seals | EPIC-04 conditional; score badge component design needed for frontend implementation | Head of UX & Design | 2026-05-22 |

### Accepted risks

| Risk | Acceptance rationale | Accepted by | Date |
|------|---------------------|-------------|------|
| RISK-02 (FEAT-36 scope expansion) | Metrics & Analytics Owner pre-sprint sign-off on metric definition mitigates; sized as M with explicit note to flag if endpoint design is more complex | Metrics & Analytics Owner | 2026-05-22 |
| RISK-03 (Render free-tier cost) | Sprint story must include build-minute impact assessment and source-file-change filter; PO confirmation required before implementation | Infrastructure Owner; Product Owner | 2026-05-22 |

### Pre-sprint required decisions

| Decision | Owner | Required before | Status |
|----------|-------|-----------------|--------|
| Closed trade count audit (BLG-GOV-33) — confirm ≥ 20 trades to unlock EPIC-04 | Product Owner | Sprint planning seals | Open |
| FEAT-36 metric definition sign-off | Metrics & Analytics Owner | Sprint 1 planning seals | Open |
| PT-04 score badge UX design | Head of UX & Design | Sprint 2 planning seals (conditional) | Open (conditional on EPIC-04 gate) |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: —
Changelog: —
Cycle: 2026-05-22__release-v4.0
