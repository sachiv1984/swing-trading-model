Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-09
Cycle: 2026-09-09__release-v9.3
Release: v9.3

# Backlog Slice — v9.3

<!-- release-plan-marker: RP:v9.3:2026-09-09__release-v9.3 -->

27 stories across 5 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope set to the top of the confirmed ~24–28 day/sprint capacity band per explicit user "use full capacity" instruction (2026-09-09). No ungated build-and-ship U-item exists this cycle — the entire ready pool (61 items) is P3, except one P4 item not selected. Scope consolidates backend reliability/correctness debt, QA/test-infrastructure debt, operations/cost-monitoring debt, spec/documentation debt, and governance-process/security debt, selected round-robin across categories, oldest-first, to fill capacity.

---

## EPIC-01 — Backend Reliability & Data Correctness Debt

**Maps to:** S2-01
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner

### ST-01 — Screener result history table
**Source:** BLG-BE-13
**Priority:** P3
**Effort:** M (~2–3 days)
**Acceptance Criteria:**
- `screener_run_history` table created: run_id, run_timestamp, total_tickers, pass_count, regime_distribution JSON
- `GET /screener/history` endpoint returns paginated run history
- Backfill not required; populate from next run forward
- Product Owner sign-off on gate condition (screener live ≥60 days — confirmed cleared 2026-08-08)

### ST-02 — Signal write-path schema consolidation
**Source:** BLG-BE-44
**Priority:** P3
**Effort:** M (~2 days)
**Acceptance Criteria:**
- The 3 signal write paths are consolidated into a single validated path
- Regression coverage confirms no behavioural change across all 3 previously-separate paths
- Commences only after confirming the `BLG-SEC-02` v6.4 sanitisation fix's 30-day production stability window (cleared 2026-08-08, no incidents on record)

### ST-03 — Structured logging correlation-ID propagation across FastAPI request lifecycle
**Source:** BLG-BE-48
**Priority:** P3
**Effort:** M (~2 days)
**Acceptance Criteria:**
- A request-scoped correlation ID (middleware-generated or accepted via header) is included in all log lines emitted during that request
- Correlation ID present in logs for at least 2 representative multi-step endpoints
- Documented in `backend_engineering_patterns.md`

### ST-04 — Arc5 compliance total_closed_trades conflates DB schema error with genuine zero-trades state
**Source:** BLG-BE-111
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A missing/broken `trade_history` table no longer produces a `total_closed_trades` value indistinguishable from a genuine zero-trades portfolio (e.g. `null` on error vs. `0` on genuine empty)
- `docs/specs/api_contracts/arc5_compliance_analytics.md` updated to document the distinction
- Frontend low-trade-volume advisory (v9.2 ST-01, Arc5ComplianceSection) updated to match if its rendering depends on this field


## EPIC-02 — QA & Test Infrastructure Debt

**Maps to:** S2-02
**Owner:** QA Testing Owner; Director of Quality

### ST-05 — Consolidate 3 overlapping SignalCard Playwright specs
**Source:** BLG-QA-82
**Priority:** P3
**Effort:** S (~1 day)
**Acceptance Criteria:**
- The 3 overlapping spec files are audited and consolidated into 1
- Full scenario coverage confirmed retained (no coverage loss)
- Suite runtime reduced

### ST-06 — Contract test suite: openapi.yaml vs. actual route behaviour
**Source:** BLG-QA-85
**Priority:** P3
**Effort:** M (~2–3 days)
**Acceptance Criteria:**
- Contract tests pass for at least 5 representative endpoints, asserting actual response shape matches the documented `openapi.yaml` schema
- Documented pattern exists for extending coverage to further endpoints
- Any drift found beyond the 5-endpoint sample is filed as a new `BLG-SPEC-*` item, not resolved inline (RISK-02)

### ST-07 — DoQ sign-off template freshness check
**Source:** BLG-QA-88
**Priority:** P3
**Effort:** S (~0.5–2 days)
**Acceptance Criteria:**
- DoQ sign-off template and the `record-visual-qa` skill that populates it are confirmed to still reflect current staging sign-off practice
- Any drift found is documented and, if actionable, filed as a follow-on item

### ST-08 — Watchlist.js post-refactor visual QA
**Source:** BLG-QA-90
**Priority:** P3
**Effort:** S (~0.5–2 days)
**Acceptance Criteria:**
- Visual QA pass performed on the Watchlist page confirming the v6.8 ESLint refactor (`BLG-OPS-61`) introduced no rendered-behaviour regression
- Findings recorded (pass, or FAIL with a filed follow-on item)

### ST-09 — Cross-browser Playwright matrix evaluation
**Source:** BLG-QA-91
**Priority:** P3
**Effort:** S (~0.5–2 days)
**Acceptance Criteria:**
- Cost/benefit of adding Firefox/WebKit to the CI matrix evaluated for a small set of critical-path specs
- Recommendation (adopt / defer, with rationale) documented

### ST-10 — Backend test suite runtime baseline
**Source:** BLG-QA-92
**Priority:** P3
**Effort:** S (~0.5–2 days)
**Acceptance Criteria:**
- Current `backend/.venv/bin/python3 -m pytest` runtime recorded as a documented baseline for future regression comparison


## EPIC-03 — Operations & Cost Monitoring Debt

**Maps to:** S2-03
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect

### ST-11 — Alpaca API cost monitoring
**Source:** BLG-OPS-17
**Priority:** P3
**Effort:** S (~1 day)
**Acceptance Criteria:**
- Alpaca API call count logged per endpoint per run
- Daily/weekly aggregate report computable
- Sequenced first within EPIC-03 as the reference instrumentation pattern for ST-12/ST-14 (RISK-03)
- Infrastructure & Operations Owner sign-off

### ST-12 — Research endpoint cost monitoring
**Source:** BLG-OPS-20
**Priority:** P3
**Effort:** S (~1 day)
**Acceptance Criteria:**
- Research endpoint API call count (external calls triggered per request) logged per session
- Weekly cost-per-session baseline computable
- Anomaly detection: sessions with >2× baseline API call count flagged
- Reuses ST-11's logging approach rather than a separate mechanism (RISK-03)
- Infrastructure & Operations Owner sign-off

### ST-13 — Data retention policy for AI audit log tables
**Source:** BLG-OPS-94
**Priority:** P3
**Effort:** S (~0.5 day)
**Acceptance Criteria:**
- Retention window (e.g. 12–24 months) and an archival/deletion procedure defined for `gemini_audit_log` and the Claude audit log table
- First cleanup pass executed (if any rows exceed the window) or explicitly deferred with rationale

### ST-14 — Anthropic API cost per-feature attribution
**Source:** BLG-OPS-96
**Priority:** P3
**Effort:** M (~2 days)
**Acceptance Criteria:**
- Cost-tracking records tagged by feature/endpoint (thesis generation, chat, daily briefing)
- Per-feature monthly cost breakdown available for at least 1 reporting cycle
- Reuses ST-11's logging approach where applicable (RISK-03)

### ST-15 — CI pipeline build-time reduction via parallelized test jobs
**Source:** BLG-OPS-97
**Priority:** P3
**Effort:** M (~2 days)
**Acceptance Criteria:**
- Independent CI test jobs (backend/frontend at minimum) parallelized
- Measured CI wall-clock time reduced for a representative PR, with before/after evidence recorded


## EPIC-04 — Spec & Documentation Debt

**Maps to:** S2-04
**Owner:** Head of Specs Team; API Contracts & Documentation Owner

### ST-16 — Spec debt dashboard
**Source:** BLG-SPEC-69
**Priority:** P3
**Effort:** S (~1 day)
**Acceptance Criteria:**
- Single-page summary of all open `BLG-SPEC-*` items with age since filing produced
- Dashboard refreshable at future `groom backlog` runs

### ST-17 — Canonical spec cross-reference linter
**Source:** BLG-SPEC-70
**Priority:** P3
**Effort:** M (~2 days)
**Acceptance Criteria:**
- Script scans `docs/specs/**` for files not referenced by any backlog item or codebase comment
- Linter run once; any orphaned specs found are triaged (kept, merged, or archived) by Head of Specs Team within the sprint (RISK-04); unresolved individual specs filed as follow-on `BLG-SPEC-*` items rather than blocking this story's closure

### ST-18 — OpenAPI response examples for Arc 5 endpoints
**Source:** BLG-SPEC-74
**Priority:** P3
**Effort:** S (~0.5–2 days)
**Acceptance Criteria:**
- Representative example response payloads added to the Arc 5 endpoint definitions in `docs/reference/openapi.yaml`
- No new `## METHOD /path` heading added (examples-only change, not new endpoints — CLAUDE.md's same-commit OpenAPI rule does not apply since no new contract is introduced)

### ST-19 — Migration block consolidation review
**Source:** BLG-SPEC-75
**Priority:** P3
**Effort:** S (~0.5–2 days)
**Acceptance Criteria:**
- All migration blocks in `data_model.md` reviewed in ascending version order for consistency
- Footer version confirmed to match the highest block; any discrepancy corrected

### ST-20 — Trade tagging taxonomy documentation
**Source:** BLG-SPEC-76
**Priority:** P3
**Effort:** S (~0.5–2 days)
**Acceptance Criteria:**
- Canonical allowed-tag taxonomy for trade tagging (`BLG-FEAT-52`) documented
- Taxonomy referenced by both the UI and reporting logic


## EPIC-05 — Governance Process Debt & Security

**Maps to:** S2-05
**Owner:** Head of Specs Team; Cybersecurity & Trust Lead

### ST-21 — Database connection pool sizing review for AI endpoints
**Source:** BLG-GOV-145
**Priority:** P3
**Effort:** S (~0.5 day)
**Acceptance Criteria:**
- Current Supavisor pool configuration (connection count, timeout settings) reviewed against AI endpoint DB query volume
- Findings documented: "no change needed" or a specific adjustment filed as a separate item
- Gate condition (30+ days AI endpoint usage — cleared 2026-08-08) confirmed before review commences

### ST-22 — Quarterly AI output sampling audit (consolidated)
**Source:** BLG-GOV-178
**Priority:** P3
**Effort:** S (~0.5 day per quarter)
**Acceptance Criteria:**
- 10 random AI outputs sampled and checked against §13.2 boundary language (no autonomous-sounding directives, advisory framing preserved) and for determinism/no-prediction drift
- First quarterly sample conducted; any findings filed as backlog items

### ST-23 — Local pre-commit lint for OpenAPI contract completeness
**Source:** BLG-GOV-179
**Priority:** P3
**Effort:** S (~1 day)
**Acceptance Criteria:**
- Pre-commit hook added scanning `docs/specs/api_contracts/*.md` for new `## METHOD /path` headings without a matching `openapi.yaml` entry, mirroring the existing CI gate's logic
- Hook catches at least the same class of omission as the CI gate, locally, before commit

### ST-24 — Base44 prompt versioning changelog
**Source:** BLG-GOV-180
**Priority:** P3
**Effort:** S (~0.5 day)
**Acceptance Criteria:**
- Changelog file created tracking Base44 frontend scaffold prompt versions and what changed
- First entry backfilled from the most recent known prompt change

### ST-25 — Base44 component regeneration diff review checklist
**Source:** BLG-GOV-181
**Priority:** P3
**Effort:** S (~0.5 day)
**Acceptance Criteria:**
- Short checklist authored covering diff-review points to check when a Base44-generated component is regenerated (dropped props, changed class names, etc.)
- Checklist referenced from the Base44 Frontend Prompt Owner's charter

### ST-26 — Onboarding template for new agent role charters
**Source:** BLG-GOV-183
**Priority:** P3
**Effort:** S (~0.5 day)
**Acceptance Criteria:**
- Template charter file authored with required sections annotated
- Template referenced from `claude/agents/` documentation

### ST-27 — API key rotation drill
**Source:** BLG-SEC-11
**Priority:** P3
**Effort:** S (~0.5 day)
**Acceptance Criteria:**
- Rotation runbook exercised end-to-end for one non-critical key
- Runbook corrected if any step failed; findings documented
