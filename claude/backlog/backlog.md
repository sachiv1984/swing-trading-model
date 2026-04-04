# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-04-04 (session — 2 new items added: BLG-GOV-13, BLG-FEAT-16)
**Last rebalance:** 2026-03-24 (cycle 2026-03-24__scheduled — DL-012)

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

> 📋 Placement Rule
> New items must be appended to the correct existing type section (§1–§8). Do not create new numbered session sections. The backlog is organised by type, not by session date.

*Completed and killed items are recorded in `claude/backlog/backlog_archive.md`.*

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

---

### BLG-TECH-05 — Prometheus metrics endpoint
**Priority:** P3 (Low)
**Type:** Observability
**Owner:** Infrastructure & Operations Owner
**Source:** Original backlog — target updated to v2.3 per backlog health scan GROOM-20260324-01
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.4 (or when system becomes multi-user)

**Problem**
No Prometheus-compatible metrics endpoint exists. As the system grows toward multi-user operation, there is no way to monitor validation run counts, failure rates, or duration without instrumenting the application directly. Observability cannot be added retroactively without significant rework.

**Scope**
- Add `GET /metrics` Prometheus endpoint exposing: validation run count, failure count by metric and severity, validation duration
- Optional Grafana dashboard

**Acceptance Criteria**
- Metrics scrape successfully in Prometheus format
- Counters and histograms are correct

---

## 2. Product Feature Backlog (User-Facing)

---

## 3. Frontend & UX Backlog

---


## 4. Backend & Data Backlog

---


### BLG-BE-08 — Review and document Reports page backend integration
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Frontend Integration
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5

**Problem**
The Reports page is not fully integrated with the backend. Some sections may be using placeholder or hardcoded data rather than live API calls. There is no documentation mapping which Reports components are wired to which backend endpoints, making it impossible to assess coverage, diagnose gaps, or plan improvements systematically.

**Scope**
- Review each section of the Reports page to confirm which data is sourced live from the backend vs. placeholder/hardcoded
- Document the current integration state: endpoint used per section, data flow, any missing connections
- Identify any Reports sections not connected to a backend endpoint and define what is needed
- Propose improvements (additional endpoints, data quality improvements, UI enhancements) as a prioritised list

**Acceptance Criteria**
- A review document exists mapping each Reports page section to its backend endpoint (or flagging a missing connection)
- All identified gaps have either a follow-up backlog item filed or are addressed within this scope
- Improvement proposals are recorded and available for roadmap input

---

### BLG-BE-09 — Review and document Signals page backend integration
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Frontend Integration
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5

**Problem**
The Signals page is not fully integrated with the backend. Some sections may be rendering without live data, and there is no documentation of which signals components are wired to which endpoints. Without this review, integration gaps are invisible until a user encounters incorrect or missing data.

**Scope**
- Review each section of the Signals page to confirm which data is sourced live from the backend vs. placeholder/hardcoded
- Document current integration state: endpoint per section, data flow, missing connections
- Identify any Signals sections not connected to a backend endpoint and define what endpoint/data is needed
- Propose improvements as a prioritised list

**Acceptance Criteria**
- A review document exists mapping each Signals page section to its backend endpoint (or flagging a missing connection)
- All identified gaps have a follow-up backlog item filed or are addressed within this scope
- Improvement proposals are recorded and available for roadmap input

---

## 5. QA & Test Automation Backlog

---


## 6. Operations & Infrastructure Backlog

---


## 7. Spec Debt Backlog

---


## 8. Governance Backlog

---

### BLG-GOV-08 — Engine prompt compression: roadmap_prompt and release_planning_prompt
**Priority:** P3 (Low)
**Type:** Governance Process / Technical Debt
**Owner:** Head of Specs Team
**Source:** AUD-2026-03-21 Tier 3 — engine prompt compression deferred (roadmap_prompt 1,581 lines; release_planning_prompt 1,534 lines)
**Effort:** L (~3–5 days)
**Provisional-Target:** v2.4

**Problem**
`claude/system/roadmap_prompt.md` (1,581 lines) and `claude/system/release_planning_prompt.md` (1,534 lines) are the two largest engine prompts in the governance system. Inline schemas, repeated examples, and verbose explanatory prose are opportunities for extraction and tightening without removing instructional precision or hard gate logic.

**Scope**
- Reduce both files by at least 10% in line count without removing governance intent or hard gate logic
- Extract schemas or reference material to `shared_standards.md` with cross-references added in-engine
- Update OPERATIONAL_GUIDE §14 and §6/§6B source prompt headers accordingly

**Acceptance Criteria**
- Both files reduced by at least 10% in line count
- No governance intent or hard gate logic removed
- Extracted material moved to `shared_standards.md` with cross-reference
- §6 checklist applied per CLAUDE.md for both files
- OPERATIONAL_GUIDE §14 and §6/§6B headers updated

---


### BLG-GOV-11 — Cycle artefact inventory and maintenance review
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead + Head of Specs Team
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5

**Problem**
As cycles accumulate, documents are created in each cycle directory but there is no consolidated inventory of what exists across all closed cycles, nor a documented lifecycle for each artefact type (maintained vs. point-in-time). Without this review it is impossible to audit historical artefacts, identify stale documents, or enforce consistent maintenance practices going forward.

**Scope**
- Inventory all documents created across all closed cycles (`claude/cycles/`)
- Categorise by type: planning, execution, QA evidence, governance, run manifests, etc.
- Document the expected lifecycle for each type: point-in-time artefact vs. living document
- Identify any maintenance gaps, stale artefacts, or documents that should be archived
- Produce a reference document or update the OPERATIONAL_GUIDE with the artefact lifecycle model

**Acceptance Criteria**
- A consolidated artefact inventory exists covering all closed cycles
- Each document type has a documented lifecycle (point-in-time vs. maintained)
- Any maintenance gaps are identified; each either resolved or filed as a follow-up backlog item
- Reference document or OPERATIONAL_GUIDE section added

---

### BLG-GOV-12 — Formalise backlog entry placement standard
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** User session review ��� 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5

**Problem**
New backlog items have been added to new numbered session sections (`## N. New Backlog Items — Session YYYY-MM-DD`) instead of under the existing type-based sections (§1–§8). This fragments the backlog, makes it hard to see all items of a given type, and creates unnecessary heading proliferation. The intended structure is one section per item type, not one section per session.

**Scope**
- Update `backlog-add` skill (via `lessons_learnt.md`) to enforce the rule: new items must be appended to the correct existing type section, not a new session section
- Add a placement rule note to the top of `backlog.md` (below the standing notice)
- No structural changes to existing session sections required (they remain as-is)

**Acceptance Criteria**
- `lessons_learnt.md` has an entry for `backlog-add` recording the placement rule
- Future backlog-add runs append to the correct type section
- Placement rule is visible at the top of `backlog.md`

---

## 9. Deferred / Future Candidates

- Daily email portfolio summary
- FX rate history tracking
- Prometheus validation observability (BLG-TECH-05)
- Position correlation analysis
- Backtesting module
- Multi-portfolio support
- Mobile app
- Full compliance scoring system

---

## 10. Explicitly Out of Scope (Product-Level)

These are deliberate product decisions, not deferrals:

- Broker API integration
- Automated trading execution
- Configurable strategy builder
- ML-based predictions
- Social / community features
- Options and futures trading support

---

## 11. Lifecycle Governance Notes

- This backlog is not canonical and must never override: strategy rules, metrics definitions, API contracts
- Any shipped feature must be backed by: a canonical specification, updated validation where applicable
- Once implemented, backlog items are superseded by canonical documentation

---

## 12. Last Release Slice — v2.4 (Archived)

<!-- release-plan-marker: RP:v2.4:2026-03-31__release-v2.4 — ARCHIVED 2026-04-03 -->

**Cycle:** 2026-03-31__release-v2.4 | **Shipped:** 2026-04-03 | **Status:** Verified_with_deviations
**Archived to:** `claude/backlog/backlog_archive.md` — v2.4 Release Slice entry

*No active release slice. Awaiting `plan release --version v2.5`.*

---

## 13. New Backlog Items — Roadmap Rebalance 2026-03-31

*Items from roadmap rebalance cycle 2026-03-31__scheduled (DL-013 to DL-016) and prior session addition (BLG-FEAT-13). Target releases are indicative.*

---

### BLG-FEAT-13 — Add gated feature rollout capability
**Priority:** P3 (Low)
**Type:** Product Feature / Platform
**Owner:** Head of Engineering + Product Owner
**Source:** User request — 2026-03-31
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5

**Problem**
The application has no mechanism to roll out new features to a subset of users or environments. Any new capability ships immediately to all users with no ability to stage a rollout, run a controlled trial, or roll back a single feature without reverting the entire deployment. As the product grows this creates risk for experimental features and makes it impossible to validate new UI flows with a limited audience before full release.

**Scope**
- Define a feature flag schema (flag name, enabled boolean, optional env/user scope)
- Implement a lightweight flag evaluation mechanism driven by config file or environment variables — no external service dependency required at first
- Wrap at least one new feature behind a flag as a proof-of-concept on first use
- Document the gating pattern in a spec file or OPERATIONAL_GUIDE

**Acceptance Criteria**
- A feature can be toggled on/off without a code change (env var or config file)
- Flag state is auditable (logged at startup or accessible via a lightweight admin check)
- At least one shipped feature uses a gate as proof-of-concept
- Gating pattern documented for use in future story authoring

---
---

### BLG-FEAT-15 — Fee drag metric on Trade History
**Priority:** P3 (Low)
**Type:** Feature — Analytics
**Owner:** Metrics Definitions & Analytics Owner + Head of Engineering
**Source:** PO/Challenger debate 2026-04-02 — action A3 from slippage metric re-scope decision
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v2.5

**Problem**
The current "entry deviation" metric (fill price vs limit price at entry) is null for most trades because the fill price field is optional and only available at entry. There is no always-available metric that captures the friction cost of executing a trade. Traders cannot see how much of their proceeds are consumed by broker fees (commission, stamp duty, FX fee) without manually inspecting individual trade records.

**Scope**
- Add a **Fee Drag %** metric: `exit_fees / gross_proceeds × 100` — the percentage of gross exit proceeds consumed by transaction costs at exit
- Surface as a new StatsCard on Trade History ("Avg Fee Drag") — distinct from existing Avg Entry Dev. card
- Surface as a new column in TradeHistoryTable ("Fee Drag %") — always populated (exit_fees and gross_proceeds always stored)
- Avg Fee Drag: mean of fee_drag_pct across all trades with non-zero gross_proceeds
- Update `docs/specs/metrics_definitions.md` to define the formula canonically
- Update `docs/specs/frontend/pages/trade_history.md` to spec the new column and StatsCard
- Update `docs/specs/api_contracts/trade_endpoints.md` to add `fee_drag_pct` and `avg_fee_drag_pct` response fields
- Update `docs/reference/openapi.yaml` for the new fields
- No data model migration required — `exit_fees` and `gross_proceeds` already stored on `trade_history`

**Acceptance Criteria**
- `fee_drag_pct` field returned per trade in GET /trades response: `exit_fees / gross_proceeds × 100`, rounded to 2 dp
- `avg_fee_drag_pct` field returned at response envelope level: mean across all trades with gross_proceeds > 0
- "Avg Fee Drag" StatsCard visible on Trade History; displays `avg_fee_drag_pct` formatted as `+X.XX%`
- Fee Drag % column present in TradeHistoryTable; always populated (no `—` for missing data)
- `docs/specs/metrics_definitions.md` contains canonical definition of fee_drag_pct formula
- Metric is labelled clearly as "Fee Drag %" throughout — never called "slippage"

**Out of scope**
- Entry-side fee drag (entry_fees / total_cost) — defer to future item
- Round-trip friction (entry + exit fees combined) — defer to future item
- Any change to existing entry deviation / slippage_pct metric

---

## 14. New Backlog Items — Session 2026-04-02

*User-raised items from session review. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

### BLG-OPS-11 — Add `--max-time` to GitHub Actions cron curl calls
**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** InfraOps review of ST-10 Render tier decision record — 2026-04-02
**Effort:** XS (<1h)
**Provisional-Target:** v2.5

**Problem**
`alert-evaluation.yml` and `daily-snapshot.yml` both invoke `curl` with no `--max-time` flag. On Render free tier, the web service spins down after 15 minutes of inactivity. When the GitHub Actions cron fires and the service is cold, the curl call stalls silently for ~50–60 seconds before the cold start completes and the request is served. This is not a failure — the request eventually succeeds — but it creates confusing workflow logs with no visible progress and unpredictable job duration.

**Scope**
- Add `--max-time 120` to every `curl` call in `.github/workflows/alert-evaluation.yml`
- Add `--max-time 120` to every `curl` call in `.github/workflows/daily-snapshot.yml`
- No other changes required

**Acceptance Criteria**
- Both workflow files have `--max-time 120` on all curl invocations
- The flag gives curl a 120-second hard ceiling — accommodating the worst-case cold start (~60s) plus endpoint execution time, with margin
- If the service fails to respond within 120s the workflow step fails with a non-zero exit code rather than hanging indefinitely

---

---

## 15. New Backlog Items — Session 2026-04-03

*Items raised from ST-11 performance baseline and System Status page review. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

### BLG-OPS-12 — Fix auth forwarding in POST /test/endpoints internal calls
**Priority:** P2 (High)
**Type:** Operational / Infrastructure
**Owner:** Head of Engineering + Infrastructure & Operations Owner
**Source:** ST-11 performance baseline review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5

**Problem**
`backend/services/health_service.py` `test_all_endpoints()` makes internal HTTP calls to each endpoint without forwarding the `X-API-Key` header. All auth-protected endpoints return 401 and are reported as "fail". The System Status page "Run Tests" button currently shows 1/17 pass rate, making the system appear critically broken when all endpoints are in fact operational. This makes the monitoring tool unreliable and misleading.

**Scope**
- Modify `test_all_endpoints()` to accept and forward the API key in internal calls (e.g. accept `api_key: str = None` parameter, add `X-API-Key` header when provided)
- Update `POST /test/endpoints` route in `main.py` to extract the `X-API-Key` from the incoming request and pass it through
- Alternatively: add a middleware bypass for server-internal calls (e.g. `X-Internal: true` header checked before auth)

**Acceptance Criteria**
- `POST /test/endpoints` returns pass/fail based on actual endpoint response, not auth rejection
- All correctly implemented endpoints report "pass" when the system is healthy
- Success rate shown on System Status page reflects actual endpoint health

---

### BLG-OPS-13 — Keep endpoint test list in sync with openapi.yaml
**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** ST-11 performance baseline review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5

**Problem**
The endpoint test list in `backend/services/health_service.py` `test_all_endpoints()` was last updated for v2.2 (12 endpoints). Endpoints added in v2.3 (`/positions/compliance`, `/alerts/rules`, `/alerts/history`, `/notifications`, `/notifications/preferences`) and v2.4 (`/digest/weekly`, analytics endpoints) are not being tested. This coverage gap will worsen each sprint if not addressed structurally.

**Scope**
- Add all missing parameterless GET endpoints to the test list in `test_all_endpoints()`:
  - `/positions/compliance`
  - `/alerts/rules`
  - `/alerts/history`
  - `/notifications`
  - `/notifications/preferences`
  - `/digest/weekly`
  - `/analytics/cohort?period=month`
  - `/analytics/r-multiple-distribution`
  - `/analytics/compliance-metrics`
  - `/health/detailed`
- Add a comment block above the list referencing `docs/reference/openapi.yaml` as the source of truth
- Update the System Status page placeholder text ("Tests 17 endpoints") to match actual count

**Acceptance Criteria**
- All parameterless GET endpoints in `openapi.yaml` are present in the test list
- A comment in `health_service.py` documents the sync obligation (update when endpoints are added)
- System Status page "Run Tests" button tests the complete current endpoint set

---

### BLG-BE-07 — Investigate high external baseline latency on DB-backed endpoints
**Priority:** P2 (High)
**Type:** Backend / Infrastructure
**Owner:** Head of Engineering
**Source:** ST-11 performance baseline — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5

**Problem**
The ST-11 performance baseline shows all DB-backed endpoints have p50 response times of 1.2–6.0 seconds when measured from an external client against staging. The consistent latency floor of ~1,100ms across unrelated endpoints suggests this is Supabase free tier DB connection establishment overhead (no persistent pool), not query-level slowness. Two outliers warrant query-level investigation: `GET /portfolio` (p50=5,979ms) and `GET /notifications/preferences` (p50=4,631ms) are significantly slower than peers with similar expected query complexity.

**Scope**
- Profile `GET /portfolio` to identify why it is ~2× slower than other multi-query endpoints — likely involves ATR calculation or multiple sequential DB round-trips; optimise or parallelise
- Profile `GET /notifications/preferences` to identify why a single-row lookup takes 4.6s — check for N+1 queries or missing index
- Investigate Supabase connection pooling options for Render free tier (e.g. PgBouncer on Supabase, SQLAlchemy `pool_size`/`pool_pre_ping` settings)
- Re-run the performance baseline after any fixes and update `docs/ops/api_performance_baseline.md`

**Acceptance Criteria**
- Root cause of `GET /portfolio` and `GET /notifications/preferences` outlier latency identified and documented
- Either a fix is applied that brings the outliers within 2× of peer endpoint latency, OR a documented architectural constraint explains why optimisation is not feasible on free tier
- Updated baseline document filed if connection pooling or query optimisation changes are made

---

### BLG-FE-07 — Fix System Status endpoint categorisation for v2.3/v2.4 routes
**Priority:** P4 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Engineer
**Source:** System Status page review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5

**Problem**
`src/pages/SystemStatus.js` `categorizeEndpoint()` does not cover routes added in v2.3/v2.4. Endpoints matching `/alerts`, `/notifications`, and `/digest` all fall through to the "Other" category instead of being correctly grouped. When BLG-OPS-12 and BLG-OPS-13 are resolved and the test runner covers these endpoints, they will appear under a generic "Other" group rather than meaningful categories.

**Scope**
- Add categorisation rules to `categorizeEndpoint()` in `SystemStatus.js`:
  - `/alerts` → "Alerts"
  - `/notifications` → "Notifications"
  - `/digest` → "Digest"
  - `/health` → "Core" (already covered but verify `/health/detailed` maps correctly)
  - `/validate` → should map to "Validation" (already covered)
  - `/analytics` → "Analytics" (already covered — verify)
- Add matching `categoryConfig` entries for "Alerts" and "Notifications" with appropriate icons and colours

**Acceptance Criteria**
- Alert endpoints appear under "Alerts" category in System Status Endpoint Tests panel
- Notification endpoints appear under "Notifications" category
- Digest endpoints appear under "Digest" category
- No endpoints fall into "Other" except `/` (root) and any future unclassified additions

---

### BLG-FE-08 — Fix Avg Slippage StatsCard gradient rendering
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** DEV-ST14-01 — delivery verification 2026-03-31__release-v2.4 — 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5
**Deviation ref:** DEV-ST14-01 (P3 cosmetic — pre-accepted by Director of Quality 2026-03-20)

**Problem**
The Avg Slippage StatsCard on the Reports/Slippage Tracking page renders without a gradient background. The functional value is correct and colour-coded. The cosmetic deviation (gradient missing) was accepted as P3 by Director of Quality 2026-03-20 and recorded in `docs/testing/slippage_scenarios.md §5`. Note: prior reference BLG-FE-01 in the deviation note was stale (BLG-FE-01 is an archived v2.2 item). This item supersedes that reference.

**Scope**
- Apply the correct Tailwind gradient class to the Avg Slippage StatsCard component
- Confirm rendering matches other StatsCard components on the Reports page

**Acceptance Criteria**
- Avg Slippage StatsCard renders with gradient background matching other StatsCard components
- No regression to functional slippage value display or colour coding

---

### BLG-GOV-10 — Fix governance_sync.yml batch push issue closure
**Priority:** P2 (Medium)
**Type:** Governance Process / DevOps
**Owner:** DevOps
**Source:** EPIC-06 merge observation — delivery verification 2026-03-31__release-v2.4 — 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5

**Problem**
`governance_sync.yml` uses `git log -1` to extract the issue number from a push event, so only the most recent commit's GitHub issue is closed automatically. When EPIC-06 was pushed as a 4-commit batch (ST-14, ST-15, ST-16, ST-17), only ST-17's issue (#164) was closed. Issues #161/162/163 remained open and required manual closure with explanatory comments. Any multi-commit push to an exec branch will silently leave earlier issues unclosed.

**Scope**
- Update `governance_sync.yml` to extract all commit messages in the push using `git log $BEFORE..$AFTER` (not `git log -1`)
- Close every issue referenced in the push range, not just the last

**Acceptance Criteria**
- Multi-commit batch push to an exec branch closes all referenced GitHub issues
- Single-commit push behaviour unchanged
- Tested with a 2+ commit push on a test branch

---

### TEST-GAP-EPIC-01-v24 — Create test scenarios for EPIC-01 backend correctness fixes
**Priority:** P2 (Medium)
**Type:** QA Coverage
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-31__release-v2.4 — TSG-v24-01 — 2026-04-03
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.5

**Problem**
EPIC-01 shipped three backend correctness fixes (ST-01 ATR conversion, ST-02 notification deduplication, ST-03 initial stop price join) with no automated test scenarios. These are correctness-critical behaviours — ATR calculation errors caused the original BLG-BE-05 defect, and deduplication logic is invisible to manual review. Without scenarios, regressions in these areas will only be caught at staging observation or by user reports.

**Scope**
- Author test scenarios covering:
  - SC-ATR-01: ATR pence→GBP conversion for .L tickers (always-on, no guard)
  - SC-DEDUP-01: Notification dispatch deduplication (same rule, same day)
  - SC-DEDUP-02: Evaluation pipeline not suppressed when dedup fires
  - SC-STOP-01: stop_price field present on analytics endpoint response for trades with a known initial_stop
- Add to appropriate scenario file(s) in `docs/testing/`
- Reference in test scenario index

**Acceptance Criteria**
- Scenario file(s) present covering all four scenarios
- Each scenario specifiable as executable against staging or unit test suite
- Referenced in test scenario index

---

## 16. New Backlog Items — Session 2026-04-04

*Items raised from v2.4 post-ship closure. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

### BLG-GOV-13 — Deduplicate backlog_archive.md duplicate item headers
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead
**Source:** Groom backlog v2.4 post-ship (2026-04-04) — ID uniqueness scan FAIL
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.5

**Problem**
`claude/backlog/backlog_archive.md` contains 50 duplicate `###` item headers — items that were archived in multiple separate grooming passes across prior cycles. The ID uniqueness scan in `backlog_management_prompt.md §4.5` flags this as FAIL every run. Duplicate headers create ambiguity about which archived entry is authoritative and make the archive unreliable as a historical record. Product Owner confirmation is required before deduplication can proceed (per the health report outstanding action).

**Scope**
- Product Owner to confirm deduplication approach: retain most recent entry per ID, or leave as historical record
- If deduplication approved: for each duplicated ID, retain the most recent (lowest in the file = latest archived) entry and remove earlier copies
- Validate that no active IDs are present in the archive after deduplication
- Run ID uniqueness scan post-deduplication and confirm PASS
- Update `backlog_archive.md` Last Updated header

**Acceptance Criteria**
- `backlog_archive.md` contains no duplicate `###` item headers
- ID uniqueness scan in next groom backlog run returns PASS
- Product Owner has confirmed the deduplication approach prior to execution

---

### BLG-FEAT-16 — AI Journal Summarisation
**Priority:** P3 (Low)
**Type:** Product Feature
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** Initiative AI-SUM — gate cleared by Product Owner 2026-04-04 (SRB-v1.7)
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5
**§13 Status:** CONDITIONALLY COMPLIANT — SRB-v1.7 (2026-03-02). Mandatory conditions below are non-negotiable and must appear in AC verbatim.
**Depends on:** Strategy Rules owner sign-off before any signal pipeline integration (SRB-v1.7 condition 3)

**Problem**
Trade journals accumulate over time and users must scroll through individual entries to extract patterns or themes from their past trading behaviour. A read-only AI-generated summary of a user's journal entries would reduce that effort and surface recurring themes or reflections without replacing the raw journal record. This is a UX convenience feature only — it does not affect the signal pipeline or any trading calculation.

**Scope**
- Backend: call an external LLM API to summarise a user's journal entries (entry/exit notes from closed trades); return summarised text
- Frontend: display the AI summary alongside (not instead of) the raw journal content on the Trade History page or a dedicated summary view
- Display an explicit disclaimer label per SRB-v1.7 condition 2 (see AC)
- AI summary output must not be persisted as a canonical record or used as a calculation input

**Acceptance Criteria**
- [ ] AI summary is displayed as a UX convenience view only — raw journal entries remain the source of truth and are visible alongside or accessible from the summary view
- [ ] AI summary output is NOT used as input to any signal, scoring, compliance, or recommendation calculation
- [ ] UI displays label: *"AI-generated summary — for reference only. Not a trading recommendation."* — label must be visible whenever the summary is shown, without requiring user interaction
- [ ] Strategy Rules owner has reviewed and confirmed the implementation does not integrate AI output into any signal pipeline (sign-off required before merge)
- [ ] Any future scope expansion beyond read-only display triggers a new §13 review before pre-alignment (documented in AC of that story)
- [ ] External LLM API key and configuration are managed via environment variable; no secrets in code

---
