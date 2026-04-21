# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-04-21 (AUD-2026-04-20: BLG-GOV-15 added — Tier 2 execution_prompt STEP 5.1.B)
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

### BLG-FE-15 — SystemStatus.js: add `/ai` prefix to `categorizeEndpoint()`
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** OA-v28-02 — v2.8 post-ship closure 2026-04-20; endpoint drift check confirmed 0 drift but `/ai` prefix unhandled
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9

**Problem**
`SystemStatus.js` `categorizeEndpoint()` does not handle the `/ai` prefix introduced by EPIC-04 (AI Journal Summarisation). The `POST /api/ai/journal-summary` and `GET /api/ai/journal-summary/history` endpoints fall to the `'Other'` category in the System Status UI. This is a cosmetic issue only — no functional impact, but the AI endpoints should appear in a named category for clarity and future maintenance.

**Scope**
- Add `/ai` prefix case to `categorizeEndpoint()` in `SystemStatus.js`
- Assign AI endpoints to an appropriate category (e.g. `'AI'` or `'Features'`)
- Verify no regression to other endpoint categories in System Status UI

**Acceptance Criteria**
- `POST /api/ai/journal-summary` and `GET /api/ai/journal-summary/history` appear in a named category (not `'Other'`) in the System Status page
- No regression to categorisation of existing endpoints
- Change verified by code review (no observable UI behaviour change required beyond category label)

---

## 4. Backend & Data Backlog

---

## 5. QA & Test Automation Backlog

---

### TEST-GAP-EPIC-04 — AI Journal Summarisation test scenario coverage
**Priority:** P3 (Low)
**Type:** Test Automation / Scenario Documentation
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-04-17__release-v2.8 (TSG-v28-01) — see verification_report.md §6
**Effort:** S (~0.5 day)
**Provisional-Target:** Before next sprint that modifies AI journal feature

**Problem**
EPIC-04 (AI Journal Summarisation) shipped with no test scenario documentation in `docs/testing/`. The POST /ai/journal-summary graceful failure path and the frontend collapsed-by-default/non-dismissible-disclaimer behaviours are untested by any formal scenario.

**Scope**
Create `docs/testing/ai_scenarios.md` covering:
- AI summary happy path (POST with trade_ids returns summarised text)
- AI summary graceful LLM failure (LLM unreachable → HTTP 200 with summary:null)
- Frontend collapsed by default on page load
- Disclaimer always visible when section is expanded (all states)

**Acceptance Criteria**
- `docs/testing/ai_scenarios.md` created with at minimum 4 scenarios covering the above
- All scenarios reference `ai_endpoints.md` and `trade_history.md v1.7` as canonical specs
- DoQ sign-off with Date field populated

---

## 6. Operations & Infrastructure Backlog

---


## 7. Spec Debt Backlog

---

## 8. Governance Backlog

---

### BLG-GOV-15 — execution_prompt.md STEP 5.1.B — System_status_report capability count cross-check
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** AUD-2026-04-20-001 — OBSERVED; blast radius 3; priority weight 9; Tier 2
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9 planning sprint

**Problem**
`System_status_report.md` capability row counts (SC-CORR, SC-SIG-IND) were incorrect at v2.8 delivery verification entry — counts were set at sprint planning time and not updated post-execution. This required a Type A action-now correction at Phase 4 and was the highest-impact friction item in v2.8. There is no prompt-enforced cross-check in STEP 5.1 (sprint close) to catch this before Phase 4.

**Scope**
Insert STEP 5.1.B advisory in `claude/system/execution_prompt.md` immediately after the existing "QA Evidence File Existence Check":

> **STEP 5.1.B — System_status_report Capability Row Cross-Check (advisory):**
> Before writing Sprint_Complete, open `docs/System_status_report.md` and locate the row for the current release. For each `SC-*` scenario count cell, verify the count matches the actual number of scenario entries in the referenced test file. If any cell value was set at sprint planning time and not updated post-execution, correct it now. Record any corrections in `sprint_close.md` notes column. Also verify `execution_prompt.md` version reference matches the actual current version. Non-blocking: if discrepancies are found, correct in-session; do not halt sprint close.

**Acceptance Criteria**
- `execution_prompt.md` STEP 5.1 contains STEP 5.1.B advisory as above
- §6 CLAUDE.md checklist applied: version bump (v3.8→v3.9), OPERATIONAL_GUIDE §14 row updated, phase section header updated, prompt_change_log entry appended
- Head of Specs Team sign-off on the patch

---

### BLG-GOV-08 — Engine prompt compression: roadmap_prompt and release_planning_prompt
**Priority:** P3 (Low)
**Type:** Governance Process / Technical Debt
**Owner:** Head of Specs Team
**Source:** AUD-2026-03-21 Tier 3 — engine prompt compression deferred (roadmap_prompt 1,581 lines; release_planning_prompt 1,534 lines)
**Effort:** L (~3–5 days)
**Provisional-Target:** v2.9 (was v2.8 — 5 consecutive deferrals; retirement review at v2.9 planning)

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


### BLG-GOV-14 — execution_prompt.md §3.2 governance patches (2 deferred from v2.8)
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** OA-v28-03 — v2.8 post-ship closure lessons_learnt_closure.md Friction Items 3 & 4
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.9 planning sprint

**Problem**
Two process gaps were identified at v2.8 delivery verification (STEP -1.3) that caused mid-verification remediation stalls. Both require patches to `claude/system/execution_prompt.md` under Head of Specs Team sign-off and cannot be applied without a governed prompt-edit session.

**Scope — Patch 1 (§3.2.A reclassification note):**
When a `delegated_frontend` story is reclassified to `autonomous` per LL-v2.3-EX-02 but the EPIC contains frontend-visible changes, the autonomous class DoQ criteria (criterion 3: no frontend-visible change) is not fully met at EPIC level. A Director of Quality counter-sign is required at sprint close (STEP 5), not deferred to delivery verification STEP -1.3. Add this note near the LL-v2.3-EX-02 reference in §3.2.A.

**Scope — Patch 2 (§3.2 DoQ EPIC template):**
When a `delegated_frontend` story has a domain-specific gate authority (Strategy Rules, Security, etc.) as its primary sign-off, the qa_evidence file must also include a Director of Quality EPIC-level consolidation block summarising all story sign-offs. The template should note: "EPIC-level DoQ sign-off block required regardless of story-level authority delegation."

**Acceptance Criteria**
- `execution_prompt.md` §3.2.A contains note: when delegated_frontend→autonomous reclassification involves frontend-visible changes, Director of Quality counter-sign required at STEP 5 sprint close
- `execution_prompt.md` §3.2 DoQ template contains explicit note: EPIC-level DoQ consolidation block required when story-level authority is domain-specific (Strategy Rules, Security, etc.)
- §6 CLAUDE.md checklist applied (version bump, OPERATIONAL_GUIDE §14 + phase section updated, prompt_change_log entry)
- Head of Specs Team sign-off on both patches

---

### BLG-GOV-11 — Cycle artefact inventory and maintenance review
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead + Head of Specs Team
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.9 (was v2.8 — deferred)

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

## Active Release Slice — v2.8

<!-- release-plan-marker: RP:v2.8:2026-04-17__release-v2.8 -->

**Cycle:** 2026-04-17__release-v2.8 | **Status:** Closed | **Published:** 2026-04-17 | **Shipped:** 2026-04-20 (Verified)
**Backlog slice:** `claude/cycles/2026-04-17__release-v2.8/stage4_backlog_slice.md`

| EPIC | Sprint | Stories | Theme |
|------|--------|---------|-------|
| EPIC-01 | Sprint 2 | ST-01 | Market Correlation Frontend |
| EPIC-02 | Sprint 1 | ST-02, ST-03 | Test Scenario Coverage |
| EPIC-03 | Sprint 1 | ST-04, ST-05, ST-06 | Governance Process Hardening |
| EPIC-04 | Sprint 2 | ST-07, ST-08 | AI Journal Summarisation |

**Theme:** Frontend Completion, Test Quality & AI Journal Feature

---

## Prior Release Slice — v2.7

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
**Provisional-Target:** v2.9 (was v2.8 — deferred)

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

*Items from §13 (BLG-FEAT-13) remain active. All §14 items (BLG-GOV-13, BLG-FEAT-16, BLG-QA-13) shipped in v2.8 — archived to backlog_archive.md 2026-04-20 (GROOM-20260420-01).*
