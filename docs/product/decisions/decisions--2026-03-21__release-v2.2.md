Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v2.2
Cycle: 2026-03-21__release-v2.2
Last Updated: 2026-03-21

## Planning Decisions — v2.2 Security, Alert Maturity & Quality

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| BLG-SEC-01 (API Key Auth) included as P1 must-have | The publicly accessible Render deployment has no authentication; financial data (portfolio, trades, P&L) is readable without auth. HTTPS + unguessable URL is obscurity, not security. Must ship before further feature additions. | Product Owner | 2026-03-21 |
| BLG-FEAT-11 (Strategy Compliance Score) deferred to v2.3 | SPS=4 boundary-adjacent item; the display-only constraint must be formally documented in AC and signed off by Strategy Rules & System Intent Owner. Scoping in a focused v2.2 release without full review creates risk of boundary drift. | Strategy Rules & System Intent Owner (advisory), Product Owner (decision) | 2026-03-21 |
| BLG-UX-01 (Sidebar navigation) deferred to v2.3 | Product Owner design decision on grouping/pattern is not yet made. Implementation without a design decision would produce a first-attempt that may need immediate revision. | Product Owner | 2026-03-21 |
| BLG-QA-01 (Playwright E2E) deferred to v2.3 | BLG-QA-02 (Test Automation Readiness Assessment) is in v2.2 scope to scope the Playwright investment. Sequencing is: assess (v2.2) → implement (v2.3). | Director of Quality (advisory), Product Owner (decision) | 2026-03-21 |
| EPIC-05 governance items (BLG-GOV-04/05/06) included in v2.2 scope | These address documented friction across 2–3 release cycles: effort sizing handoff, provisional target signal, lessons learnt carry-forward. Applying them now improves all subsequent releases. Low blast radius (governance process only, no user impact). | Head of Specs Team (advisory), Product Owner (decision) | 2026-03-21 |
| v2.2 theme: Security, Alert Maturity & Quality | Three natural threads: (1) auth gap created by v2.1 API surface growth; (2) alert engine incomplete without scheduling + thresholds + history; (3) QA scenario gaps flagged in v2.1 delivery verification (TSG-v21-01/02). | Product Owner | 2026-03-21 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (Security) is Sprint 1 priority #1 | API Key Auth (BLG-SEC-01) is P1 and should ship before additional features are added on top of an unauth'd API surface. | Product Owner | 2026-03-21 |
| EPIC-03 (Bug Fixes) bundled into a single PR alongside EPIC-01 Sprint 1 | XS items (BLG-BE-03, BLG-FE-01, BLG-OPS-06) have no dependencies and negligible effort; bundling avoids PR overhead. | PMO Lead (advisory), Product Owner (decision) | 2026-03-21 |
| BLG-OPS-04 (alert scheduling design, ST-03) as Sprint 1 design task | Product Owner decision task (scheduler mechanism, cooldown, trigger frequency) must be completed before any BLG-FEAT-10 or BLG-FEAT-12 engineering begins. Sprint 1 positions ST-03 as a design output, enabling Sprint 2 implementation. | PMO Lead | 2026-03-21 |
| EPIC-04 (QA Coverage) in Sprint 2; EPIC-05 (Governance) in Sprint 3 | QA tasks are not blocked by security work and can overlap Sprint 2. Governance changes have no external dependency and can slip to Sprint 3 without blocking delivery. | PMO Lead | 2026-03-21 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | | | | |

*(No escalations raised requiring formal Accepted Risk decisions.)*

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-03-21__release-v2.2
