**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-27__release-v4.2
**Release:** v4.2

---

# Backlog Slice — v4.2

## Overview

| Metric | Value |
|--------|-------|
| Release | v4.2 |
| Theme | Claude API Governance, SI-02 Pre-Work Readiness & Spec Debt |
| EPICs | 4 |
| Stories | 13 |
| Sprints | 2 |
| Merge order | EPIC-01 → EPIC-02 (Sprint 1); EPIC-04 → EPIC-03 (Sprint 2) |

---

## EPIC-01 — Claude API Compliance & Security

**Maps to:** S2-01  
**Owner:** Cybersecurity & Trust Lead; AI Compliance & Governance Officer  
**Sprint:** 1  
**Description:** Establish Claude API compliance and security baseline — accountability ownership, API key security review, model version pinning policy, and log hygiene policy. Completes the Claude API governance posture introduced in v4.1.

---

### ST-01 — Anthropic API Accountability & Key Security

**EPIC:** EPIC-01  
**Backlog items:** BLG-GOV-66, BLG-GOV-65  
**Effort:** XS (~0.75 day combined)  
**Owner:** Director of HR; Cybersecurity & Trust Lead  
**Type:** Governance / Security  

**Scope:**
- BLG-GOV-66: Review AI Compliance & Governance Officer charter for explicit Anthropic coverage; update charter if gap found; document ownership confirmation
- BLG-GOV-65: Confirm ANTHROPIC_API_KEY has minimum required permissions; confirm stored as env var only; confirm not exposed in application logs or error traces; document in api_key_register.md (BLG-GOV-50 scope)

**Acceptance Criteria:**
- AC-01: AI Compliance Officer charter explicitly covers Anthropic API — updated or confirmed as sufficient
- AC-02: Anthropic API key security posture confirmed: minimum permissions, env var only, no log exposure
- AC-03: Security confirmation documented in ops/security notes
- AC-04: Director of HR and AI Compliance Officer sign-off recorded

---

### ST-02 — Anthropic Model Version Pinning Policy

**EPIC:** EPIC-01  
**Backlog items:** BLG-GOV-64  
**Effort:** S (~0.5 day)  
**Owner:** AI Compliance & Governance Officer; Head of Specs Team  
**Type:** Governance / AI Compliance  

**Scope:**
- Define policy: all Claude-backed features must pin to a specific model ID (e.g., claude-3-5-sonnet-20241022), never "latest"
- Define change management: model version update requires AI Compliance sign-off and QA re-test
- Apply immediately: confirm thesis generation endpoint uses pinned model ID
- Document in AI governance notes or CLAUDE.md §2 extension

**Acceptance Criteria:**
- AC-01: Policy document produced (or CLAUDE.md §2 section) — model version pinning rule defined
- AC-02: Thesis generation endpoint (POST /trade-plans/{plan_id}/generate-thesis) confirmed to use pinned model ID
- AC-03: Change management procedure documented
- AC-04: Reviewed by AI Compliance Officer and Head of Specs Team

---

### ST-03 — Claude API Log Hygiene Policy

**EPIC:** EPIC-01  
**Backlog items:** BLG-OPS-38  
**Effort:** S (~0.5 day)  
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead  
**Type:** Operations / Security Hygiene  

**Scope:**
- Confirm Render production logs do not capture ANTHROPIC_API_KEY or full prompt text
- Define log level policy: INFO for request metadata (model, tokens, endpoint); DEBUG for full prompt — never in production
- Define log retention policy pre-SI-02
- Document findings and policy in ops notes

**Acceptance Criteria:**
- AC-01: Log hygiene policy document produced
- AC-02: API key and full prompt non-exposure in production logs confirmed (or remediated)
- AC-03: Log level policy for Claude API trace events defined
- AC-04: Log retention policy defined pre-SI-02

---

## EPIC-02 — Operational Monitoring & Baselines

**Maps to:** S2-02  
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner  
**Sprint:** 1  
**Description:** Complete outstanding OA-3 (api_performance_baseline.md) and establish Claude API operational monitoring baseline — first monthly cost review and latency baseline for the thesis generation endpoint.

---

### ST-04 — API Performance Baseline Update (OA-3)

**EPIC:** EPIC-02  
**Backlog items:** BLG-OPS-35  
**Effort:** S (~0.5 day)  
**Owner:** Infrastructure & Operations Owner  
**Type:** Operations / Performance Baseline  
**Outstanding Action:** OA-3 from v4.1 post-ship closure  

**Scope:**
- Add POST /ai/check-daily-cost to api_performance_baseline.md measurement table
- Record at minimum estimated p50 latency from a live environment run
- Coordinate with Infrastructure & Operations Owner for live environment timing

**Acceptance Criteria:**
- AC-01: POST /ai/check-daily-cost appears in api_performance_baseline.md with p50 latency data
- AC-02: Live environment timing run confirmed (or estimated with note if live run not feasible in sprint)
- AC-03: Reviewed by Infrastructure & Operations Owner

---

### ST-05 — Claude API First Monthly Cost Review

**EPIC:** EPIC-02  
**Backlog items:** BLG-OPS-36  
**Effort:** S (~1 day)  
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner  
**Type:** Operations / Cost Monitoring  

**Scope:**
- Review actual Claude API call volume and cost from existing logging (gemini_audit_log → claude equivalent or Render logs)
- Establish monthly monitoring cadence and cost alert threshold
- Update BLG-OPS-30 scope reference to Claude API instead of Gemini
- Produce first monthly review report

**Acceptance Criteria:**
- AC-01: First monthly review report produced with actual call volume and cost data
- AC-02: Monthly monitoring cadence defined
- AC-03: Cost alert threshold defined and documented
- AC-04: BLG-OPS-30 scope update confirmed (Gemini → Claude reference)

---

### ST-06 — Claude API Thesis Generation Latency Baseline

**EPIC:** EPIC-02  
**Backlog items:** BLG-OPS-39  
**Effort:** S (~1 day)  
**Owner:** Head of Engineering; Infrastructure & Operations Owner  
**Type:** Operations / Performance Baseline  

**Scope:**
- Establish p50/p95 latency baseline for POST /trade-plans/{plan_id}/generate-thesis (Claude-backed)
- Minimum 10 sample calls
- Record in api_performance_baseline.md
- Define regression threshold (e.g., p95 > 2× baseline triggers review)

**Acceptance Criteria:**
- AC-01: p50/p95 latency measured from minimum 10 sample calls
- AC-02: Baseline recorded in api_performance_baseline.md
- AC-03: Regression threshold defined and documented

---

## EPIC-03 — Claude API Implementation & Spec Debt

**Maps to:** S2-03  
**Owner:** Head of Backend Engineering; AI Compliance & Governance Officer; Head of Specs Team  
**Sprint:** 2  
**Description:** Implement the Claude API audit trail (backend), clear the AI thesis API contract spec debt from the Gemini→Claude switch, define the Claude API Playwright mock strategy, and assess prompt caching opportunity.

---

### ST-07 — Claude API Audit Trail Implementation

**EPIC:** EPIC-03  
**Backlog items:** BLG-GOV-63  
**Effort:** M (~2 days)  
**Owner:** Head of Backend Engineering; AI Compliance & Governance Officer  
**Type:** Backend / Governance  

**Scope:**
- Implement per-request Claude API audit log (claude_audit_log table or equivalent)
- Log fields: request_id, endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd, generated_at
- Analogous to existing gemini_audit_log pattern
- Endpoint registered in backend/routers/test.py and openapi.yaml per CLAUDE.md §2
- `## POST /ai/claude-audit-log` (or equivalent internal endpoint) added to api contract if queryable

**Acceptance Criteria:**
- AC-01: claude_audit_log table (or equivalent) implemented and populated on each thesis generation call
- AC-02: All required log fields captured: request_id, endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd, generated_at
- AC-03: Log queryable for BLG-OPS-36/OPS-37 cost reviews
- AC-04: Backend route registered in backend/routers/test.py and openapi.yaml
- AC-05: Reviewed by AI Compliance & Governance Officer

---

### ST-08 — AI Thesis API Contract Update for Claude

**EPIC:** EPIC-03  
**Backlog items:** BLG-SPEC-42  
**Effort:** S (~0.5 day)  
**Owner:** API Contracts Documentation Owner; Head of Specs Team  
**Type:** Spec Debt / API Contract  

**Scope:**
- Update docs/specs/api_contracts/ai_thesis_generation.md to reflect Claude API response fields (model_id, usage.input_tokens, usage.output_tokens, cache_hit)
- Update openapi.yaml to match updated contract schema
- Verify no drift between contract and current v4.1 implementation

**Acceptance Criteria:**
- AC-01: api_contracts/ai_thesis_generation.md updated with Claude API response fields
- AC-02: openapi.yaml updated and consistent with contract
- AC-03: No drift between contract and implementation (verified via openapi drift gate)

---

### ST-09 — Claude API Playwright Mock Strategy

**EPIC:** EPIC-03  
**Backlog items:** BLG-QA-37  
**Effort:** S (~0.5 day)  
**Owner:** QA & Testing Owner; Director of Quality  
**Type:** QA / Test Infrastructure  

**Scope:**
- Define strategy for mocking Claude API calls in Playwright E2E tests
- Document: intercept patterns, fixture response format, how to avoid real API calls in CI
- Align with existing Playwright infrastructure; no implementation required — strategy document and test infrastructure recommendation

**Acceptance Criteria:**
- AC-01: Claude API Playwright mock strategy document produced
- AC-02: Intercept patterns and fixture response format defined
- AC-03: Strategy reviewed and approved by Director of Quality

---

### ST-10 — Claude API Prompt Caching Assessment (Optional)

**EPIC:** EPIC-03  
**Backlog items:** BLG-BE-22  
**Effort:** S (~0.5 day)  
**Owner:** Head of Backend Engineering  
**Type:** Backend / Cost Optimisation  
**Note:** Optional — defer to post-v4.2 if Sprint 2 overloads  

**Scope:**
- Assess feasibility of Anthropic prompt caching for thesis generation
- Review: cache hit rate potential, eligible prompt segments, implementation complexity
- Output: assessment note with recommendation (implement / defer / not applicable)

**Acceptance Criteria:**
- AC-01: Prompt caching feasibility assessment produced
- AC-02: Cache hit rate estimate provided
- AC-03: Recommendation (implement / defer / not applicable) made with rationale

---

## EPIC-04 — Governance Preparation & Pre-Planning

**Maps to:** S2-04  
**Owner:** PMO Lead; Head of Specs Team; Product Owner  
**Sprint:** 2  
**Description:** Prepare for SI-02 sprint planning (prerequisites checklist), define SI-04 scope (pre-planning), review v4.1 staging sign-off effectiveness, and audit backlog ID namespace integrity.

---

### ST-11 — SI-02 Sprint Planning Prerequisites Checklist

**EPIC:** EPIC-04  
**Backlog items:** BLG-GOV-60  
**Effort:** S (~0.5 day)  
**Owner:** PMO Lead; Head of Specs Team  
**Type:** Governance / Sprint Planning Gate  

**Scope:**
- Produce SI-02 sprint planning prerequisites checklist consolidating all pre-sprint items: BLG-GOV-39, BLG-SPEC-37/39/41, BLG-BE-17/20/23, BLG-GOV-44/46/51 (per prior backlog)
- Define integration point in sprint_planning_prompt.md or release_planning_prompt.md as gated advisory step
- Checklist must be complete before SI-02 sprint planning seals

**Acceptance Criteria:**
- AC-01: Prerequisites checklist produced covering all SI-02 pre-sprint items
- AC-02: Each checklist item has: owner, status (complete/open/gate-conditional), target
- AC-03: Integration point in planning engine defined
- AC-04: PMO Lead and Head of Specs Team sign-off

---

### ST-12 — SI-04 Strategy Version Comparison Pre-Planning

**EPIC:** EPIC-04  
**Backlog items:** BLG-GOV-57  
**Effort:** S (~1 day)  
**Owner:** Product Owner; Head of Specs Team  
**Type:** Governance / Pre-Sprint Planning  

**Scope:**
- Define SI-04 feature scope: which strategy versions to compare, how performance delta is computed (metric definitions)
- Define UI view concept: layout, data source, interaction model
- Output: SI-04 scope definition document (input to SI-04 sprint planning and BLG-GOV-62 §13 review)

**Acceptance Criteria:**
- AC-01: SI-04 scope definition document produced
- AC-02: Performance comparison methodology defined (deterministic — not adaptive or predictive)
- AC-03: UI view concept sketch included
- AC-04: Reviewed by Product Owner and Head of Specs Team

---

### ST-13 — v4.1 Staging Sign-Off Review & Backlog Namespace Audit

**EPIC:** EPIC-04  
**Backlog items:** BLG-GOV-61, BLG-GOV-59  
**Effort:** S (~1.25 days combined)  
**Owner:** Director of Quality; PMO Lead; Head of Specs Team  
**Type:** Governance / Process Review + Hygiene  

**Scope:**
- BLG-GOV-61: Count P3 staging deviations in v4.1 vs v3.9/v4.0 baseline; assess whether BLG-GOV-30 staging-only AC designation reduced surprise deviations; produce findings note
- BLG-GOV-59: Audit all BLG IDs in backlog.md and backlog_archive.md; verify no sequence gaps or ID collisions; produce namespace count summary

**Acceptance Criteria:**
- AC-01: v4.1 deviation count comparison produced (v4.1 vs v3.9/v4.0 baseline)
- AC-02: Effectiveness finding documented (improved / no change / insufficient data)
- AC-03: BLG namespace audit complete — gaps or collisions documented (or "none found")
- AC-04: Namespace count summary table produced per BLG type
- AC-05: Reviewed by Director of Quality (GOV-61) and Head of Specs Team (GOV-59)
