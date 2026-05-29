**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.3
**Release:** v4.3
**Sprint Goal:** Deliver v4.3 by resolving all 3 outstanding v4.2 governance patches, clearing the QA backlog, completing operations and security hardening documentation, and shipping the Arc 5 P&L compliance section and frontend fixes — establishing a clean, well-tested baseline before the next feature arc.
**Backlog Slice Source:** original — claude/cycles/2026-05-29__release-v4.3/stage4_backlog_slice.md

---

# Sprint Backlog — 2026-05-29__release-v4.3

---

## Sprint Scope

### Merge Order

| Sprint | Sequence | Rationale |
|--------|---------|-----------|
| Sprint 1 | EPIC-01 → EPIC-04 | EPIC-01 (governance OA) must merge before EPIC-04 (frontend); EPIC-04 may rebase on EPIC-01 merge |
| Sprint 2 | EPIC-03 → EPIC-02 | EPIC-03 ST-13 staging parity must complete before EPIC-02 staging verifications; EPIC-02 rebases on EPIC-03 merge |

**execution_state.json owner:** EPIC-01 (first EPIC in execution order for the cycle).

All other EPIC branches: check for `execution_state.json` existence before creating — read and append your EPIC section. Do not overwrite.

**Shared files advisory:** `execution_state.json` only shared file. No cross-EPIC source code overlap in v4.3 (EPIC-01/02/03 = documentation; EPIC-04 = isolated frontend/backend components).

---

### Sprint 1

---

#### EPIC-01 — Governance Patch Resolution

**Maps to:** S2-01, S2-02
**Owner:** Head of Specs Team
**Estimated effort:** ~4 hrs (3 × XS + 2 × S)
**Risk IDs:** RISK-01
**Execution sequence:** 1 (Sprint 1, first)

---

##### ST-01 — execution_prompt.md STEP 3.2.A: qa_signed_off advisory patch

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Staging-only ACs:** None

**Notes:** Carry-forward OA-1 from v4.2 closure record. Sprint-seal prerequisite — must be in Sprint 1 scope. Governance file edit checklist (CLAUDE.md §6) applies: version bump, OPERATIONAL_GUIDE.md §14 update, prompt_change_log.md entry.

---

##### ST-02 — execution_prompt.md STEP 5.3/STEP 8: sprint close branch safety advisory

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** HoST decision on gate (halt if not on main) vs advisory (warn if not on main) required before implementation (AC-01 must be resolved first)

**Staging-only ACs:** None

**Notes:** Carry-forward OA-2 from v4.2 closure record. Sprint-seal prerequisite. HoST decision determines implementation form — gate hard-halts if not on main; advisory warns but continues. Decision must be recorded in AC-01 before implementation begins. Governance file edit checklist applies.

---

##### ST-03 — qa_evidence_template.md: AC mapping 1:1 advisory

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Staging-only ACs:** None

**Notes:** Carry-forward OA-3 from v4.2 closure record. Sprint-seal prerequisite. If qa_evidence_template.md is Class 6, governance file edit checklist applies.

---

##### ST-04 — Staging-only AC pre-designation reference table

**Owner:** Head of Specs Team; Director of Quality
**Estimated effort:** S (~1 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Staging-only ACs:** None

**Notes:** Backlog source BLG-GOV-42. Reference table must draw from v3.7–v4.2 deliveries (BLG-QA-24/28/29/30). HoST decides integration location (sprint_planning_prompt.md advisory or OPERATIONAL_GUIDE.md). If integrated into a Class 6 prompt: governance file edit checklist applies.

---

##### ST-05 — AI feature inventory document

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** S (~0.5 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Staging-only ACs:** None

**Notes:** Backlog source BLG-GOV-47. Covers 3 AI-touching endpoints: POST /trade-plans/{plan_id}/generate-thesis, POST /ai/journal-summary, POST /ai/check-daily-cost. Filed at docs/ai/ai_feature_inventory.md (or equivalent). Requires AICGO + Strategy Rules & System Intent Owner review.

---

#### EPIC-04 — Frontend Polish & Arc 5 Feature

**Maps to:** S2-05
**Owner:** Frontend Engineer; Financial Reporting & Records Owner
**Estimated effort:** ~4 hrs (1 × XS + 1 × S + 1 × M)
**Risk IDs:** RISK-04
**Execution sequence:** 2 (Sprint 1, after EPIC-01 merges; rebase on main before starting)

---

##### ST-16 — Pre-entry check entry price bug fix

**Owner:** Frontend Engineer
**Estimated effort:** XS (~0.25 hr)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None (independent of EPIC-01)

**Staging-only ACs:** None

**Notes:** Backlog source BLG-FE-50. Root cause investigation required — entry_price param writing/formatting in pre-entry validation panel. Unit test or Playwright test covers the fixed path (AC-04). No regression to other pre-entry checks.

---

##### ST-17 — Claude thesis generation UI copy audit

**Owner:** Base44 Frontend; Head of UX & Design
**Estimated effort:** S (~0.5 hr)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Staging-only ACs:** None

**Notes:** Backlog source BLG-FE-51. Audit all AI thesis generation UI copy for "Gemini" references. Playwright or unit test confirms no "Gemini" text in AI thesis generation flow (AC-05). HoUX review required (AC-04).

---

##### ST-18 — Arc 5 compliance score in monthly P&L report

**Owner:** Financial Reporting & Records Owner; Base44 Frontend
**Estimated effort:** M (~2 hrs)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None (arc5-compliance API exists from v3.9)

**Staging-only ACs:** None

**Notes:** Backlog source BLG-FE-38. **AC-04 Playwright designation (confirmed at sprint planning 2026-05-29):** Playwright mocking IS feasible — `page.route()` can mock `GET /analytics/arc5-compliance`. AC-04 is NOT staging-only. Evidence path: Playwright CI test. Backend modification: add "Strategy Compliance" section to GET /reports/monthly-pnl response, sourced from arc5-compliance data. Frontend: add "Strategy Compliance" section to Monthly P&L view. Per CLAUDE.md §2: observable AC — Playwright test required (path confirmed feasible). No regression to existing P&L financial sections.

---

### Sprint 2

---

#### EPIC-03 — Operations & Security Hardening

**Maps to:** S2-04
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Estimated effort:** ~4 hrs (1 × XS + 1 × S + 1 × M)
**Risk IDs:** RISK-03
**Execution sequence:** 3 (Sprint 2, first — ST-13 is prerequisite for EPIC-02 staging verifications)

---

##### ST-13 — Staging environment parity audit

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** M (~2 hrs)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None (first story in Sprint 2)

**Staging-only ACs:** AC-01 (staging env vars verification), AC-02 (database schema parity), AC-03 (endpoint health check on staging)

**Notes:** Backlog source BLG-OPS-33. **Must execute before ST-06/07/08** (EPIC-02 staging verifications). Confirms ANTHROPIC_API_KEY, Alpaca keys, DB connection, Telegram keys parity. Confirms claude_audit_log/red_flag_events tables in staging. Parity report filed at docs/ops/. Infra Owner sign-off required.

---

##### ST-14 — claude-audit-log performance baseline

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (~0.25 hr)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** ST-13 preferred first (staging env confirmed)

**Staging-only ACs:** AC-01 (live environment timing run required)

**Notes:** Backlog source BLG-OPS-42. Add GET /ai/claude-audit-log to docs/ops/api_performance_baseline.md with estimated p50 latency from staging or prod run.

---

##### ST-15 — API key rotation policy and external API key security register

**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Estimated effort:** S (~1 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None (can run parallel to ST-13/14)

**Staging-only ACs:** None

**Notes:** Backlog sources BLG-GOV-36, BLG-GOV-50. Two documents: (1) docs/ops/api_key_rotation_policy.md covering Alpaca + ANTHROPIC_API_KEY; (2) docs/security/api_key_security_register.md covering all external keys. Cybersecurity & Trust Lead review required.

---

#### EPIC-02 — QA Debt & Test Coverage

**Maps to:** S2-03
**Owner:** Director of Quality; QA Lead
**Estimated effort:** ~8 hrs (3 × XS + 2 × S + 2 × M)
**Risk IDs:** RISK-02
**Execution sequence:** 4 (Sprint 2, after EPIC-03 merges; ST-06/07/08 gated on ST-13 completion; rebase on main after EPIC-03 merges)

---

##### ST-06 — Staging verification: Claude thesis generation

**Owner:** QA Lead
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** ST-13 (staging parity confirmed — hard prerequisite)

**Staging-only ACs:** AC-01 (live API response), AC-02 (button visible with key configured), AC-03 (button generates thesis), AC-04 (sign-off date recorded)

**Notes:** Backlog source BLG-QA-29. Deferred from v4.0/v4.1. Requires ANTHROPIC_API_KEY on staging and "Improve with AI" button on TradePlan edit page. Note: uses Claude API (not Gemini) as of v4.1. Sign-off evidence in qa_evidence file.

---

##### ST-07 — Staging verification: ticker validation live Yahoo Finance rejection path

**Owner:** Director of Quality; Head of Engineering
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** ST-13 (staging parity confirmed — hard prerequisite)

**Staging-only ACs:** AC-01 (invalid ticker → 422 on staging), AC-02 (valid ticker → 201 on staging)

**Notes:** Backlog source BLG-QA-30. Deferred from v4.0. Requires live internet on staging with SKIP_TICKER_VALIDATION unset.

---

##### ST-08 — Staging verification: Claude API daily cost threshold alert

**Owner:** QA Lead; Infrastructure & Operations Owner
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** ST-13 (staging parity confirmed — hard prerequisite)

**Staging-only ACs:** AC-01 (POST /ai/check-daily-cost → 200 on staging), AC-02 (Telegram alert fires when threshold exceeded)

**Notes:** Backlog source BLG-QA-35. Deferred from v4.1. Requires live TELEGRAM_BOT_TOKEN and claude_audit_log rows in staging DB. Sign-off evidence in qa_evidence file.

---

##### ST-09 — Playwright E2E coverage for Arc5ComplianceSection

**Owner:** QA Lead
**Estimated effort:** S (~0.5 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None (can run parallel to staging verifications)

**Staging-only ACs:** None

**Notes:** Backlog source BLG-QA-28. New Playwright test in tests/e2e/ for PerformanceAnalytics page. Test: "Arc 5 Signal Compliance" heading + 4 stat card titles visible; loading skeleton shown (page.route() mock); error state shown on 500. Must pass in CI.

---

##### ST-10 — Arc 5 end-to-end integration test specification

**Owner:** Director of Quality; QA Lead
**Estimated effort:** M (~2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Staging-only ACs:** None

**Notes:** Backlog source BLG-QA-36. Formal spec covering SI-01 pre-entry validation → override acknowledgement → SI-03 red flag event → Arc5ComplianceSection metrics update. Filed in docs/qa/ or tests/e2e/. DoQ + QA Lead review.

---

##### ST-11 — CI pipeline execution time baseline measurement

**Owner:** QA Lead
**Estimated effort:** XS (~0.25 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Staging-only ACs:** None

**Notes:** Backlog source BLG-QA-38. 3 sample runs, p50 noted. Gate status for BLG-QA-27 determined (< 5 min → defer; ≥ 5 min → gate cleared). Recorded in docs/ops/ or QA notes.

---

##### ST-12 — Playwright scenario coverage matrix and Arc 5 coverage audit

**Owner:** Director of Quality; QA Lead
**Estimated effort:** M (~2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** ST-09 preferred first (provides Arc 5 coverage data point)

**Staging-only ACs:** None

**Notes:** Backlog sources BLG-QA-32 (coverage matrix), BLG-QA-33 (Arc 5 audit). Coverage matrix: feature/story → Playwright spec → scenario count → staging-only ACs. Covers v3.7–v4.2. Arc 5 audit: SC-PEV-*, SC-RFJ-*, SC-AC5-* scenarios assessed. Both filed in docs/qa/. DoQ review.

---

## Capacity Summary

| Metric | Sprint 1 | Sprint 2 | Total |
|--------|----------|----------|-------|
| Confirmed capacity | ~10–12 hrs | ~10–12 hrs | ~20–24 hrs |
| Estimated effort | ~6.25–8 hrs | ~9.5–12 hrs | ~15.75–20 hrs |
| Utilisation | ~52–80% | ~79–120% | ~66–100% |
| Over-allocation | No | At limit (⚠ WARN) | WARN accepted |

**Over-allocation:** WARN acknowledged by Product Owner at sprint planning. Sprint 2 staging tasks (ST-06/07/08/13/14) are human-delegate with minimal engine effort, reducing effective Sprint 2 engine load.

---

## Items Deferred This Sprint

No items deferred. All 18 stories from `stage4_backlog_slice.md` are included in this sprint backlog.

| Item | EPIC | Reason |
|------|------|--------|
| *(none)* | — | — |

---

## Deferred Execution Blockers Accepted

*(omitted — `deferred_execution_blockers` was empty in state.json)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Sprint goal sign-off | Product Owner | Yes |
| Sprint backlog sign-off | Product Owner | Yes |
| Head of Specs Team ST-02 gate/advisory decision (before EPIC-01 execution begins) | Head of Specs Team | No (pre-execution, not pre-seal) |

---

## Product Owner Sign-Off

Product Owner: Confirmed
Date: 2026-05-29
