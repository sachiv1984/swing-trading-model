# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-04-17 (roadmap rebalance cycle 2026-04-17__scheduled — no-change; DL-020)
**Last rebalance:** 2026-04-17 (cycle 2026-04-17__scheduled — DL-020)

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
**Provisional-Target:** v2.8+ (or when system becomes multi-user)

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

### BLG-FE-14 — Market Correlation frontend view
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** BLG-FEAT-17 / ST-08 (v2.7 EPIC-04) AC-6 deferred — `analytics_endpoints.md v2.1.0` specifies full response shape
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.8

**Problem**
`GET /analytics/market-correlation` was delivered in v2.7 (ST-08). The backend returns per-position Pearson correlation coefficients and a portfolio-level weighted average, each with severity classifications (`high`/`moderate`/`low`). AC-6 of ST-08 required a frontend view displaying this data with colour-coded severity; it was deferred because no frontend story was in EPIC-04 scope. The endpoint contract is fully specified in `analytics_endpoints.md v2.1.0` and data is live with 8h cache TTL.

**Scope**
- Add a market correlation view (Head of UX to confirm page placement — Analytics or Portfolio page)
- Display per-position correlation coefficient and severity (colour-coded: `high`, `moderate`, `low`)
- Display portfolio-level weighted average correlation with severity badge
- Source data from `GET /analytics/market-correlation`
- Handle partial results gracefully (positions with unavailable Yahoo Finance data return `null` correlation)

**Acceptance Criteria**
- Per-position correlation and severity rendered; colour-coding matches severity classifications in `analytics_endpoints.md v2.1.0`
- Portfolio-level weighted average correlation displayed with severity badge
- `null` correlation values render gracefully (e.g. "N/A")
- Data sourced exclusively from `GET /analytics/market-correlation`; no hardcoded values
- No regression to existing Analytics page content

---

## 4. Backend & Data Backlog

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
**Provisional-Target:** v2.8 (deprioritised in v2.5 planning queue by BLG-FE-09 — 2026-04-05)

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
**Provisional-Target:** v2.8

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

## 12. Last Release Slice

## Active Release Slice — v2.7

<!-- release-plan-marker: RP:v2.7:2026-04-13__release-v2.7 — COMPLETE -->

**Cycle:** 2026-04-13__release-v2.7 | **Status:** Closed | **Published:** 2026-04-13 | **Shipped:** 2026-04-16 (Verified)
**Backlog slice:** `claude/cycles/2026-04-13__release-v2.7/stage4_backlog_slice.md`

| Epic | Stories | Theme |
|------|---------|-------|
| EPIC-01 | ST-01, ST-02, ST-03 | Backend Integration Completion |
| EPIC-02 | ST-04, ST-05, ST-06, ST-07 | Test Automation & CI Hardening |
| EPIC-03 | ST-08, ST-09, ST-10, ST-11 | Frontend UX Polish |
| EPIC-04 | ST-12, ST-13, ST-14, ST-15 | Governance & Spec Debt |

**Theme:** Integration Baseline, Quick Wins & Governance Debt

| EPIC | Sprint | Stories | Theme |
|------|--------|---------|-------|
| EPIC-01 | Sprint 1 | ST-01, ST-02, ST-03 | System Status Reliability |
| EPIC-02 | Sprint 2 | ST-04, ST-05, ST-06 | Backend Integration & Performance |
| EPIC-03 | Sprint 2 | ST-07, ST-08, ST-09 | Frontend & Operations Quick Wins |
| EPIC-04 | Sprint 1 | ST-10, ST-11, ST-12, ST-13 | Governance, Process & QA Hardening |

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
**Provisional-Target:** v2.8

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

## 14. New Backlog Items — Session 2026-04-04

*Items raised from v2.4 post-ship closure. Not yet processed through a roadmap rebalance cycle. Target releases are indicative.*

---

### BLG-GOV-13 — Deduplicate backlog_archive.md duplicate item headers
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead
**Source:** Groom backlog v2.4 post-ship (2026-04-04) — ID uniqueness scan FAIL
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.8

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
**Provisional-Target:** v2.8
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

### BLG-QA-13 — Test scenario coverage gap: market correlation and supplementary indicators (v2.7)
**Priority:** P3 (Low)
**Type:** Test Coverage
**Owner:** QA & Testing Owner
**Source:** v2.7 delivery verification (TEST-GAP-v27-EPIC04-01) — EPIC-04 ST-08 and ST-09 delivered new backend functionality verified by code review; registered test_scenarios (analytics_scenarios.md v1.0, signals_scenarios.md v1.0) cover prior cohort analysis and signals page frontend, not the new v2.7 endpoints and fields
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.8

**Gap description**
Two scenario files were registered in execution_state.json for EPIC-04 (`docs/testing/analytics_scenarios.md`, `docs/testing/signals_scenarios.md`) but these predate v2.7 and cover different functionality:
- `analytics_scenarios.md` v1.0 (2026-03-17) — covers `GET /analytics/cohort`, not the new `GET /analytics/market-correlation` endpoint
- `signals_scenarios.md` v1.0 (2026-03-18) — covers Signals page frontend behaviour, not the four new supplementary indicator fields

No scenarios exist that exercise:
1. `GET /analytics/market-correlation` happy path, cache behaviour, fallback on Yahoo Finance unavailability, or severity classification
2. `POST /signals/generate` with the four new supplementary fields (`relative_strength_pct`, `week52_high_proximity_pct`, `avg_daily_volume_20d`, `price_vs_50d_ma`)

**Recommended scenarios**
- SC-CORR-01: `GET /analytics/market-correlation` returns per-position Pearson correlation with correct fields
- SC-CORR-02: portfolio-level weighted average correlation included in response
- SC-CORR-03: 8h cache returns same result on second call within TTL
- SC-CORR-04: graceful partial response when Yahoo Finance unavailable for one ticker
- SC-SIG-IND-01: `POST /signals/generate` response includes all four supplementary fields per signal object
- SC-SIG-IND-02: `relative_strength_pct` is None when benchmark data unavailable (not error)

**Acceptance Criteria**
- [ ] `docs/testing/analytics_scenarios.md` updated (or new file created) to include SC-CORR-01 through SC-CORR-04
- [ ] `docs/testing/signals_scenarios.md` updated (or new file created) to include SC-SIG-IND-01 and SC-SIG-IND-02
- [ ] All new scenarios reference `analytics_endpoints.md v2.1.0` and `signal_endpoints.md v1.1` as canonical spec
