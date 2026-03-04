# Product Backlog — Momentum Trading Assistant

Owner: Product Owner
Status: Active
Class: Planning Document (Class 4)
Last Updated: 2026-03-04

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

*Completed and killed items are recorded in `claude/backlog/backlog_archive.md`.*

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

These items ensure analytical correctness, validation integrity, and operational safety.
They are not user-facing, but they directly affect trust in outputs and release confidence.

---

### BLG-TECH-05 — Prometheus metrics endpoint
**Priority:** P3 (Low — v2.1 candidate)
**Type:** Observability

**Scope**
- Add `GET /metrics` Prometheus endpoint exposing:
  - Validation run count
  - Failure count by metric and severity
  - Validation duration
- Optional Grafana dashboard.

**Acceptance Criteria**
- Metrics scrape successfully in Prometheus format.
- Counters and histograms are correct.

**Target**
- v2.1 or when system becomes multi-user.

---

## 2. Product Feature Backlog (User-Facing)

---

### BLG-FEAT-03 — Slippage Tracking
**Priority:** P2
**Effort:** 1-2 hours

> ⚠️ **Orphan Notice:** No roadmap home or cycle activity detected. Review at next Roadmap Rebalance.

Track and display trade slippage and average slippage summary.

**Indicative Formula**

`(Fill Price - Market Price) / Market Price`

Requires data model update.

---

### BLG-FEAT-08 — Basic Compliance Metrics
**Priority:** P2
**Effort:** ~1 day
**Target release:** v1.9 (pre-work gate for Structured Trade Reflection Template)

Lightweight discipline metrics:
- Journal completion rate
- Stop-based exit rate
- Average position size (% of portfolio)

Definitions must be canonicalised in `metrics_definitions.md` first.

---

## 3. Deferred / v2.1 Candidates

- Daily email portfolio summary
- FX rate history tracking
- Prometheus validation observability (BLG-TECH-05)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system

---

## 4. Explicitly Out of Scope (Product-Level)

These are deliberate product decisions, not deferrals:

- Broker API integration
- Automated trading execution
- Configurable strategy builder
- ML-based predictions
- Social / community features
- Options and futures trading support

---

## 5. Lifecycle Governance Notes

- This backlog is not canonical and must never override:
  - Strategy rules
  - Metrics definitions
  - API contracts
- Any shipped feature must be backed by:
  - Canonical specification
  - Updated validation where applicable
- Once implemented, backlog items are superseded by canonical documentation.

---

## 6. Test Coverage Gaps (from Delivery Verification)

> ⚠️ **Orphan Notice:** No BLG-ID assigned; no explicit roadmap home or cycle activity. Assign a BLG-ID and roadmap home at next Roadmap Rebalance, or close if addressed.

- [TEST-GAP-EPIC-06] Test scenario coverage gap from 2026-03-02__release-v1.7: QA & Testing Owner to create scenarios per verification_report.md §6 (Test Coverage Assessment). Gaps: no scenarios asserting sharpe_ratio_trade_method presence in /validate/calculations response (14 metrics); no scenario asserting portfolio_endpoints.md field alignment; no scenario asserting holding_days in GET /trades. Target: pre-next sprint on analytics, portfolio, or trade endpoint domains.

---

## 7. Spec & Documentation Debt (Head of Specs Review — 2026-03-03)

Review performed: 2026-03-03 by Head of Specs Team.
Scope: all docs/specs/, docs/reference/, docs/governance/, docs/product/, claude/roadmap/, claude/backlog/, backend/main.py cross-referenced against live contracts.

Items are classified as **DRIFT** (spec and implementation/document diverged) or **GAP** (spec section required but absent).

---

### DRIFT Items

---

**BLG-SPEC-D1** — API Contracts README.md version frozen at v1.8.4
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/specs/api_contracts/README.md` header and changelog list contract version as 1.8.4 / 1.8.2.
Three contracts were incremented to v1.9.0 during EPIC-06 (analytics_endpoints.md, portfolio_endpoints.md, trade_endpoints.md).
README.md was not updated.

**Acceptance Criteria**
- README.md version header reflects v1.9.0
- Changelog includes a v1.9.0 entry referencing EPIC-06 changes (sharpe_ratio_trade_method, portfolio field alignment, holding_days)

---

**BLG-SPEC-D2** — settings_endpoints.md spec/implementation mismatch
**Priority:** P1 (High)
**Type:** Spec–Implementation Drift
**Owner:** API Contracts & Documentation Owner + Head of Engineering
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/specs/api_contracts/settings_endpoints.md` specifies `PUT /settings` (replace all settings).
Live implementation in `backend/main.py` uses `PATCH /settings/{settings_id}` (update single setting by ID).
Additionally, `POST /settings` is implemented but not documented anywhere.
This is a P1 drift: clients relying on the spec will call the wrong method and path.

**Decision Required**
Product Owner + API Contracts owner to choose:
(a) Update spec to document `PATCH /settings/{settings_id}` and `POST /settings` as the canonical interface, or
(b) Align backend to implement `PUT /settings` as specced (breaking change to existing frontend).

**Acceptance Criteria**
- settings_endpoints.md accurately documents the live HTTP method, path, and request/response schema
- No divergence between spec and implementation
- Decision record filed if option (b) chosen (breaking change)

---

**BLG-SPEC-D3** — GET /market/status completely undocumented live endpoint
**Priority:** P2 (Medium)
**Type:** Documentation Gap / Drift
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`GET /market/status` is implemented in `backend/main.py` (router tag: `market`), called by the frontend MarketStatusBar component, and appears in `docs/System_status_report.md` test results.
No spec document exists. No entry in Specs_Index.md. No openapi.yaml path.

**Scope**
- Create `docs/specs/api_contracts/market_endpoints.md` (or equivalent) documenting GET /market/status: request, response schema (SPY/FTSE regime, live FX rate), error behaviour
- Register in Specs_Index.md §3
- Add to openapi.yaml

**Acceptance Criteria**
- GET /market/status has a canonical spec section
- Response schema matches live implementation
- Registered in Specs_Index.md

---

**BLG-SPEC-D4** — GET /positions/search/tags undocumented
**Priority:** P3 (Low)
**Type:** Documentation Gap
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`GET /positions/search/tags` is implemented in `backend/main.py` (router: positions).
Not documented in `docs/specs/api_contracts/position_endpoints.md`.

**Acceptance Criteria**
- position_endpoints.md includes GET /positions/search/tags with request parameters and response schema

---

**BLG-SPEC-D7** — openapi.yaml frozen at v1.8.1; not updated for v1.9.0 contracts
**Priority:** P2 (Medium)
**Type:** Documentation Drift / Reference Artefact Staleness
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/reference/openapi.yaml` is at version 1.8.1 (1193 lines).
Three contracts were bumped to v1.9.0 in EPIC-06:
- `sharpe_ratio_trade_method` absent from /validate/calculations validated metrics list
- portfolio positions response schema not aligned to v1.9.0 field list
- `holding_days` absent from GET /trades trade object schema
Specs_Index.md §4 states: "openapi.yaml must be reviewed inline with every contract change; markdown contracts take precedence on conflict."
This was not done during EPIC-06.

**Acceptance Criteria**
- openapi.yaml version field updated to 1.9.0
- /validate/calculations response includes sharpe_ratio_trade_method (14 validated metrics total)
- GET /trades trade object includes holding_days (integer)
- GET /portfolio positions objects reflect v1.9.0 field list
- No conflicts between openapi.yaml and markdown contracts

---

**BLG-SPEC-D8** — docs/System_status_report.md missing governance lifecycle header
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Drift
**Owner:** Director of Quality
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/System_status_report.md` has no governance lifecycle header (Owner, Class, Status, Version, Last Updated).
Per `document_lifecycle_guide.md`, all documents must carry a compliant header.
Current document begins directly with `# System Status Verification Report` with no metadata block.

**Acceptance Criteria**
- Lifecycle header added to docs/System_status_report.md: Owner, Class, Status, Version, Last Updated fields
- Class and Status assigned consistently with document_lifecycle_guide.md definitions

---

**BLG-SPEC-D9** — process_index.md and Specs_Index.md reference wrong path for document_lifecycle_guide.md
**Priority:** P3 (Low)
**Type:** Documentation Drift / Broken Cross-Reference
**Owner:** Head of Specs Team
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/governance/process_index.md` references `docs/governance/document_lifecycle_guide.md`.
`docs/specs/Specs_Index.md` §5 references `docs/governance/document_lifecycle_guide.md`.
Actual file location: `claude/charter/document_lifecycle_guide.md`.
The docs/governance/ path does not exist.

**Acceptance Criteria**
- process_index.md updated to reference `claude/charter/document_lifecycle_guide.md`
- Specs_Index.md §5 updated to reference `claude/charter/document_lifecycle_guide.md`

---

### GAP Items

---

**BLG-SPEC-G1** — settings_model.md missing (Specs_Index §6.1, open since 2026-02-21)
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** Head of Specs Team
**Raised:** Specs_Index §6.1, 2026-02-21 (carried forward to 2026-03-03 review)

**Problem**
`docs/specs/data_model/settings_model.md` is listed as an open gap in Specs_Index.md §6.1 since 2026-02-21.
The settings schema is referenced by settings_endpoints.md but no canonical model document exists.
This gap pre-dates v1.7 and remains unresolved.

**Acceptance Criteria**
- settings_model.md created in docs/specs/data_model/ covering: settings schema, field names, types, validation rules, defaults
- Registered in Specs_Index.md §3
- Cross-referenced from settings_endpoints.md

**Note**
Resolution of BLG-SPEC-D2 (PUT vs PATCH method drift) should be decided first, as the resolved API shape will determine the model document scope.

---

**BLG-SPEC-G2** — Error Response Standard not defined (Specs_Index §6.2, open since 2026-02-21)
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** API Contracts & Documentation Owner
**Raised:** Specs_Index §6.2, 2026-02-21 (carried forward to 2026-03-03 review)

**Problem**
No canonical Error Response Standard exists.
Specs_Index.md §6.2 has listed this as an open gap since 2026-02-21.
Without a standard, error shapes across endpoints are inconsistent and untestable against a single schema.

**Acceptance Criteria**
- Error Response Standard document created (or section added to an existing canonical spec)
- Covers: standard error envelope shape, required fields (status_code, error_code, message, detail), HTTP status code mapping
- All existing API contract docs updated to reference the Error Response Standard for their error sections
- Registered in Specs_Index.md

---

**BLG-SPEC-G3** — structured_logging_standards.md not registered in Specs_Index.md
**Priority:** P3 (Low)
**Type:** Index Gap
**Owner:** Head of Specs Team
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/specs/structured_logging_standards.md` was created in EPIC-04 (2026-03-02) as a Class 1 Canonical Specification.
It is not registered in `docs/specs/Specs_Index.md` §3 (Domain Specifications).
New canonical specs must be registered in Specs_Index.md per document_lifecycle_guide.md.

**Acceptance Criteria**
- Specs_Index.md §3 updated to include structured_logging_standards.md with Owner (Head of Engineering), Class (1), Status (Active), Version (0.1.0)

---

**BLG-SPEC-G4** — ADR-002 in wrong location
**Priority:** P3 (Low)
**Type:** Governance Organisation Gap
**Owner:** Head of Specs Team
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
ADR-002 (if it exists) is located in `docs/decisions/` rather than `docs/product/decisions/` where all other decision records are filed (e.g., SRB-v1.7-*.md, api-versioning-v1.7.md).
Inconsistent location breaks navigation and cross-reference from Specs_Index.md.

**Acceptance Criteria**
- ADR-002 moved or copied to `docs/product/decisions/`
- Any cross-references updated
- `docs/decisions/` directory removed or documented if intentionally separate

---

**BLG-SPEC-G5** — validation_system.md owner field non-compliant (Specs_Index §7.1, open since 2026-02-21)
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Gap
**Owner:** Infrastructure & Operations Owner
**Raised:** Specs_Index §7.1, 2026-02-21 (carried forward to 2026-03-03 review)

**Problem**
`docs/specs/validation_system.md` lists owner as `Platform Team` — a team name, not a named role.
Specs_Index.md §7.1 has flagged this as open since 2026-02-21.
Per document_lifecycle_guide.md, Owner must be a named governance role (e.g., Head of Engineering, Director of Quality).

**Acceptance Criteria**
- validation_system.md owner field updated to a named governance role consistent with document_lifecycle_guide.md
- Specs_Index.md §7.1 notation updated to reflect resolved

---

**Review Summary (active items)**
- Active items: 7 DRIFT (D1–D4, D7–D9), 5 GAP (G1–G5) = 12 total
- P1: 1 (D2 — settings endpoint method mismatch — decision required)
- P2: 4 (D3, D7, G1, G2)
- P3: 7 (D1, D4, D8, D9, G3, G4, G5)
- Oldest open items: G1, G2, G5 — open since 2026-02-21 (2 cycles; flag for upgrade review)
- Recommended resolution order: D2 → G1 → D7 → D3 → G2

---

## 8. New Backlog Items — IW-20260304-01 (Cycle 2026-03-04__item-3.4)

Items promoted to backlog from Idea Intake Window IW-20260304-01 (2026-03-04). Decision log: DL-005.
All items compete within v1.8 release capacity. Release planning engine determines v1.8 backlog slice.

---

### BLG-NEW-01 — Golden Output Regression Baseline for CI
**Priority:** P1 (High)
**Type:** Quality / CI
**Owner:** Engineering + QA
**Source:** IDEA-director-of-quality-20260304-02 — Director of Quality, IW-20260304-01
**Cycle added:** 2026-03-04__item-3.4

**Problem**
The current CI gate (`POST /validate/calculations`, EPIC-01) checks only that `critical_failed > 0` blocks the merge. It does not verify that specific calculations return the correct numeric values. A change that silently alters the trailing stop formula from `CurrentPrice - (2 × ATR)` to `CurrentPrice - (2.1 × ATR)` would pass the current gate. Numeric regressions are the highest-risk defect class in a trading system.

**Scope**
- Define a set of deterministic golden test cases: known inputs (entry_price, ATR, risk_percent, etc.) with expected output values derived directly from the canonical strategy spec
- Store as `tests/golden_outputs.json` — treated as a canonical artefact; updated only via spec-linked PR
- Scope limited to stop/sizing calculations only (per STEP 5 scoping from IW-20260304-01)
- Add a CI step that calls the backend with each golden input and asserts output matches to required precision
- Any numeric divergence from golden values fails the build

**Acceptance Criteria**
- `tests/golden_outputs.json` exists with spec-derived golden values for stop and sizing calculations
- CI step added that runs golden output assertions on every PR
- Build fails on any numeric deviation from golden values
- Precision tolerance documented (e.g., 4 decimal places for share counts)
- Golden values derived from canonical spec, not from current implementation

**Dependencies**
- None (prerequisite: BLG-NEW-02 must follow, not precede)

---

### BLG-NEW-02 — Backtest vs Live Stop Reconciliation Report
**Priority:** P1 (High)
**Type:** Quality / CI
**Owner:** Engineering + QA
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Dependency:** After BLG-NEW-01 (golden output baseline must be in place first)

**Problem**
There is no automated verification that the trailing stop formula used in backtests and the formula used in the live system produce identical results for the same inputs. Silent divergence between backtest and live logic is a category of defect that cannot be caught by either gate independently.

**Scope**
- Report or CI assertion that compares backtest stop calculations vs live system stop calculations for a set of known inputs
- Output: reconciliation result confirming parity or flagging divergence

**Acceptance Criteria**
- Automated check exists that verifies backtest and live stop logic produce identical results for all golden inputs
- Any divergence between backtest and live calculation fails the check

---

### BLG-NEW-03 — Define and Document Unavailability Failure Mode
**Priority:** P1 (High)
**Type:** Policy / Governance
**Owner:** Infrastructure & Operations Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day

**Problem**
There is no documented policy for what happens when the system is unavailable during a trading session (e.g., backend down, market data feed unavailable). The system has no documented failure modes or fallback procedures for the user.

**Scope**
- Define and document the unavailability failure mode: what the user should do, what the system state is, and any manual fallback procedures
- Document where this policy lives (e.g., OPERATIONAL_GUIDE.md or a new docs/ops/ document)

**Acceptance Criteria**
- Unavailability failure mode documented: system states covered, user action required, data integrity implications
- Document registered in appropriate governance index

---

### BLG-NEW-04 — AI-Assisted Workflow Governance Policy
**Priority:** P2 (Medium)
**Type:** Governance
**Owner:** Product Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day

**Problem**
The project uses AI-assisted workflows (Claude Code) for governed routines. There is no documented policy governing: which decisions may be taken by AI, which require human override, and how AI output is reviewed before it becomes a canonical record.

**Scope**
- Author an AI-Assisted Workflow Governance Policy document
- Define: AI authority scope, human-in-the-loop requirements, escalation triggers, record-keeping obligations

**Acceptance Criteria**
- Policy document authored and filed under appropriate governance path
- Policy covers: scope of AI authority, mandatory human review checkpoints, record-keeping requirements

---

### BLG-NEW-05 — Dependency Vulnerability Scanning in CI
**Priority:** P1 (High)
**Type:** Security / CI
**Owner:** Engineering (CI)
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day

**Problem**
There is no automated scanning of Python dependencies for known vulnerabilities in the CI pipeline. A compromised or vulnerable dependency could be introduced silently.

**Scope**
- Add a CI step that scans Python dependencies (e.g., using `pip-audit` or `safety`) for known CVEs
- Block merge (or warn at configurable severity) on high/critical vulnerabilities
- Integrate with existing `.github/workflows/` structure

**Acceptance Criteria**
- Dependency vulnerability scan runs on every PR
- High/critical CVEs block merge (or produce a required review comment)
- Scan tool and severity threshold documented

---

### BLG-NEW-07 — Running API Changelog Document
**Priority:** P1 (High)
**Type:** Documentation / Governance
**Owner:** API Contracts & Documentation Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day

**Problem**
There is no single running changelog document for API contract changes. Changes to endpoint contracts (new fields, removed fields, version bumps) are recorded in individual spec files but there is no centralised, human-readable history of API evolution across versions.

**Scope**
- Create a running API Changelog document that summarises contract changes per version
- Cover all contracts under `docs/specs/api_contracts/`
- Backfill from v1.8.x → v1.9.0 changes (EPIC-06 scope)
- Document maintainer obligation: must be updated alongside every contract version bump

**Acceptance Criteria**
- API Changelog document exists and is registered in Specs_Index.md
- All v1.9.0 contract changes (EPIC-06) are backfilled
- Maintenance obligation documented alongside contract spec authoring workflow

---

### BLG-NEW-08 — Automated OpenAPI Drift Detection in CI
**Priority:** P1 (High)
**Type:** CI / Governance
**Owner:** Engineering (CI)
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day

**Problem**
`docs/reference/openapi.yaml` was not updated during EPIC-06 when three contracts were bumped to v1.9.0 (BLG-SPEC-D7). There is no CI check that detects drift between the markdown API contracts and openapi.yaml. Drift will recur without an automated gate.

**Scope**
- Add a CI step that detects drift between `openapi.yaml` and the markdown API contracts
- Approach: either (a) generate openapi.yaml from contracts and compare, or (b) run a custom lint/diff check against known contract fields
- Block merge on detected drift

**Acceptance Criteria**
- CI step detects drift between openapi.yaml and markdown contracts
- Merge blocked if drift is detected
- Approach documented (generation vs diff) — approach decision to be made in pre-alignment

---

**Section Summary (IW-20260304-01 active items)**
- Active: 7 standalone (BLG-NEW-01–05, 07, 08)
- P1: 6 (BLG-NEW-01, 02, 03, 05, 07, 08)
- P2: 1 (BLG-NEW-04)
- Archived: BLG-NEW-06 (merged into 4.1b — see backlog_archive.md)

---

## v1.8 Release Slice — 2026-03-04

<!-- release-plan-marker: RP:v1.8:2026-03-04__release-v1.8 -->

**Cycle:** 2026-03-04__release-v1.8
**Release:** v1.8 — Risk Dashboard
**Planned:** 2026-03-04
**Backlog slice:** `claude/cycles/2026-03-04__release-v1.8/stage4_backlog_slice.md`

Items in v1.8 sprint: EPIC-01 (ST-01–ST-04), EPIC-02 (ST-05–ST-08), EPIC-03 (ST-09–ST-10), EPIC-04 (ST-11–ST-12)
