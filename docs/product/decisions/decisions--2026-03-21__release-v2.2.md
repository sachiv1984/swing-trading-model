Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v2.2
Cycle: 2026-03-21__release-v2.2
Last Updated: 2026-03-23

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

---

### ST-03 Execution Decisions — Alert Scheduling: Trigger Mechanism and Rule Behaviour

**Date:** 2026-03-23
**Made by:** Product Owner
**Challenger review:** Completed — 4 must-answer challenges raised and resolved; 3 worth-noting items acknowledged
**Status:** Final — unblocks ST-04 and ST-05
**Delegation record:** DEL-20260322-02 (resolved)

---

#### Decision A — Evaluation Frequency

**Decision:** Daily evaluation at 21:30 UTC (16:30 ET), Monday–Friday, triggered automatically by a Render cron job calling `POST /alerts/evaluate`.

**Scope boundary (explicit):** This is end-of-day evaluation only. Intraday stop breach alerts are **out of scope for v2.2**. If a stop is breached intraday and the position recovers before close, no alert fires that day. If a stop is breached and the position closes below it, the alert fires at 21:30 UTC that evening. Future intraday coverage requires a separate backlog item.

**Lock-in acknowledgement:** Changing evaluation frequency requires a `render.yaml` edit and redeploy, not a config-only change. This is accepted for v2.2 given evaluation frequency is not expected to change and cron-native simplicity outweighs the overhead of a configurable schedule at this stage.

---

#### Decision B — Cooldown Policy

**Intent:** One notification per (position, rule type) per UTC calendar day.

**What this means:** The policy prevents duplicate alerts being generated for the same position and rule type within a single calendar day. It does **not** suppress repeat alerts across consecutive days — a position near its stop for five days produces five alerts (one each day). That is expected and correct behaviour; the system is doing its job. The mechanism for realising this intent (schema, query strategy, deduplication implementation) is delegated to the Head of Specs Team for encoding in the ST-04/ST-05 implementation spec.

**Terminology note:** The term "cooldown" is retired. The policy is **calendar-day deduplication** keyed on UTC calendar day boundary (not a sliding 24-hour window).

---

#### Decision C — market_regime_change Source of Truth

**Decision:** `GET /market/status` remains the source of truth for market regime. The evaluation fires on **transition to `risk_off`** (state change), not on sustained `risk_off` state.

**Implementation constraint (mandatory for HoST to encode as AC):** The last-known regime value must be persisted to the database, not held in application memory. On service restart, the evaluation service must read persisted regime state from the database. A cold start must not assume a regime change has occurred. Explicit AC required: "Service restart does not trigger a spurious `market_regime_change` alert."

---

#### Decision D — Trigger Mechanism

**Decision:** Render cron job (defined in `render.yaml`) calling `POST /alerts/evaluate` at 21:30 UTC Monday–Friday.

**Auth:** After ST-01 ships, `POST /alerts/evaluate` requires `X-API-Key`. The Render cron service must have the API key configured as an environment variable and must pass it as the `X-API-Key` header on every call. This is the intended authentication approach — simpler than an external credential store but not absent. Explicit AC required in the implementation spec.

**Scope clarification:** The `render.yaml` modification is an **implementation-story artefact**, not a ST-03 output. The decision names the mechanism; the file modification lands in ST-04 or ST-05 (Head of Specs Team to assign). The cron modification must be in the same PR as the implementation of `POST /alerts/evaluate` going live — do not merge the schedule without the endpoint being live.

---

#### Mandatory Pre-Conditions for Implementation Spec

The Head of Specs Team must encode the following as named acceptance criteria in ST-04/ST-05:

| # | Pre-condition | Owner |
|---|---------------|-------|
| 1 | Intraday scope boundary stated explicitly in spec: end-of-day evaluation only; no intraday alert path in v2.2 | Head of Specs Team |
| 2 | Render cron service must have API key env var configured; `POST /alerts/evaluate` call must pass `X-API-Key` header | Head of Specs Team + Head of Engineering |
| 3 | Cold-start protection: service startup reads persisted market regime from DB; no spurious `market_regime_change` alert on restart | Head of Specs Team |
| 4 | Calendar-day deduplication: one notification per (position, rule type) per UTC calendar day — mechanism designed by HoST, testable AC required | Head of Specs Team |
| 5 | `render.yaml` modification lands in same PR as `POST /alerts/evaluate` going live | Head of Engineering |

---

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-03-21__release-v2.2
