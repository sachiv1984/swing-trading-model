**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-09
**Cycle:** 2026-06-08__release-v5.3
**Release:** v5.3
**Sprint Goal:** Ship all 6 known API contract gaps, API key authentication on the SI-05 digest endpoint, and CI secret scanning in Sprint 1 — then deliver the carry-forward governance patches, AI policy documents, and QA coverage needed to sustain v5.x operations sustainably through Sprint 2.
**Backlog Slice Source:** claude/cycles/2026-06-08__release-v5.3/stage4_backlog_slice.md (original)

---

# Sprint Backlog — 2026-06-08__release-v5.3

## Sprint Scope

### Merge Order

**Sprint 1:** EPIC-02 → EPIC-01
**Sprint 2:** EPIC-03 → EPIC-04

**execution_state.json owner:** EPIC-02 (Sprint 1); EPIC-03 (Sprint 2 — appends to existing Sprint 1 state)

**Shared files across EPICs:**
- `docs/reference/openapi.yaml`: EPIC-01 owns; EPIC-04 must rebase onto main after EPIC-01 merges
- `backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js`: EPIC-01 owns via ST-07; EPIC-04 rebase advisory applies
- `claude/system/execution_prompt.md`, `claude/system/templates/qa_evidence_template.md`: EPIC-03 owns; CLAUDE.md §6 compliance required at commit

---

## Sprint 1 — API Contract Debt + Security Hardening

### EPIC-02 — Security & Ops Hardening

**Maps to:** S2-08, S2-09, S2-10
**Owner:** Head of Engineering; Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Estimated effort:** ~15 hrs
**Risk IDs:** RISK-04
**Execution sequence:** 1 (merges first — execution_state.json owner)
**Sprint:** 1

---

#### ST-08 — BLG-BE-35: POST /digest/si05/send API key authentication

**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Estimated effort:** S (~4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Must follow existing API key auth pattern (Depends injection). Docs update to digest_endpoints.md required in same commit.

**Staging-only ACs:** None — 401 behaviour verifiable via unit test; no staging environment required

---

#### ST-09 — BLG-OPS-57: SI-05 Telegram delivery failure alerting

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~6 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Alert must fire AFTER retry logic (BLG-BE-32 pattern). Render log ERROR level is CI-testable via mock. Deployment runbook update required.

**Staging-only ACs:** None — ERROR-level log verifiable via unit test mock; runbook doc verifiable by reading

---

#### ST-10 — BLG-OPS-58: CI secret scanning gate

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** S (~6 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** gitleaks or trufflehog acceptable. Include allowlist for test fixtures. RISK-04: false positives expected in test fixtures — allowlist calibration is part of scope.

**Staging-only ACs:** None — CI gate verifiable by running action; dummy token test verifiable in CI

---

### EPIC-01 — API Contract & Spec Debt Resolution

**Maps to:** S2-01, S2-02, S2-03, S2-04, S2-05, S2-06, S2-07
**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Estimated effort:** ~26 hrs
**Risk IDs:** RISK-01
**Execution sequence:** 2 (merges after EPIC-02)
**Sprint:** 1

---

#### ST-01 — BLG-SPEC-53: API contract gap resolution plan

**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Estimated effort:** M (~10 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (first in EPIC-01 — defines scope for ST-04–07)

**Notes:** Resolution plan should be produced in docs/specs/api_contracts/ or claude/cycles/2026-06-08__release-v5.3/. ST-02 audit may surface additional gaps not in scope — file as BLG-SPEC-55+ if found.

**Staging-only ACs:** None — document deliverable; verifiable by reading

---

#### ST-02 — BLG-SPEC-54: openapi.yaml completeness audit

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** S (~6 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** Can run parallel with ST-01

**Notes:** Enumerate all 50 routes from backend/routers/. Update openapi.yaml for any confirmed additional gaps. File new BLG-SPEC items if needed.

**Staging-only ACs:** None — audit and openapi.yaml update verifiable via file inspection

---

#### ST-03 — BLG-QA-51: QA acceptance criteria for SPEC-49–52

**Owner:** Director of Quality
**Estimated effort:** S (~4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** Can run parallel with ST-01/ST-02; must complete before ST-04/ST-05/ST-06/ST-07

**Notes:** QA readiness document must define the "complete contract" template that ST-04–07 use. Reusable for future contract gap stories.

**Staging-only ACs:** None — document deliverable; verifiable by reading

---

#### ST-04 — BLG-SPEC-49: GET /ai/journal-summary/history contract

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** XS (~2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** ST-03 (QA AC template must be complete)

**Notes:** `## GET /ai/journal-summary/history` at ## level (not ###) in docs/specs/api_contracts/ai_endpoints.md. CLAUDE.md §2: openapi.yaml entry required in same commit.

**Staging-only ACs:** None

---

#### ST-05 — BLG-SPEC-50: GET /analytics/compliance-metrics contract

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** XS (~2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** ST-03 (QA AC template must be complete)

**Notes:** `## GET /analytics/compliance-metrics` at ## level in docs/specs/api_contracts/analytics_endpoints.md. CLAUDE.md §2: openapi.yaml entry required in same commit.

**Staging-only ACs:** None

---

#### ST-06 — BLG-SPEC-51: GET /news/{ticker} contract

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** XS (~2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** ST-03 (QA AC template must be complete)

**Notes:** New file acceptable if no existing news_endpoints.md; `## GET /news/{ticker}` at ## level. CLAUDE.md §2: openapi.yaml entry required.

**Staging-only ACs:** None

---

#### ST-07 — BLG-SPEC-52: Watchlist endpoint contracts + test.py

**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Estimated effort:** S (~4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** ST-03 (QA AC template must be complete)

**Notes:** Three endpoints (GET/POST/DELETE /watchlist) at ## level. Must also update backend/routers/test.py, SystemStatus.js fallback count, and SC-SS-01b in tests/e2e/system-status.spec.js — all in same commit per CLAUDE.md §2. Cross-references EPIC-04 ST-20 (coverage matrix update needs these commits on main first).

**Staging-only ACs:** None — all verifiable via file inspection and CI

---

## Sprint 2 — Governance Patches + QA/Testing

### EPIC-03 — Governance Patches & Policy

**Maps to:** S2-11, S2-12, S2-13, S2-14, S2-15, S2-16, S2-17, S2-C1, S2-C2
**Owner:** Head of Specs Team; Strategy Rules & System Intent Owner; AI Compliance Governance Officer
**Estimated effort:** ~41 hrs (including ST-23/ST-24)
**Risk IDs:** RISK-02
**Execution sequence:** 3 (Sprint 2, merges first — reads Sprint 1 execution_state.json and appends)
**Sprint:** 2

---

#### ST-11 — LL-v5.2-P4-01: qa_evidence_template.md signer format note

**Owner:** Head of Specs Team
**Estimated effort:** S (~2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None (P1 carry-forward — complete early in EPIC-03)

**Notes:** CLAUDE.md §6 governance compliance required: version bump, OPERATIONAL_GUIDE §14 update, prompt_change_log.md entry — all in same commit.

**Staging-only ACs:** None

---

#### ST-12 — LL-v5.2-P4-02: execution_prompt.md STEP 5.3A SSR sub-step

**Owner:** Head of Specs Team
**Estimated effort:** S (~2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None (P1 carry-forward — complete early in EPIC-03)

**Notes:** CLAUDE.md §6 governance compliance required: version bump, OPERATIONAL_GUIDE §14 update, prompt_change_log.md entry — all in same commit.

**Staging-only ACs:** None

---

#### ST-13 — BLG-GOV-107: SI-02 frontend activation criteria precision

**Owner:** Head of Specs Team; PMO Lead; Product Owner
**Estimated effort:** S (~5 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** 2–3 specific, checkable gate conditions required (e.g. ≥20 closed trades, drift API p99 <2s, drift scores confirmed meaningful). Updates current_roadmap.md SI-02 entry.

**Staging-only ACs:** None — document deliverable; verifiable by reading

---

#### ST-14 — BLG-GOV-108: AI model pin update policy

**Owner:** AI Compliance Governance Officer; Head of Engineering
**Estimated effort:** S (~5 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Append to BLG-GOV-64 policy document or companion doc. 30-day deprecation notice timeline required.

**Staging-only ACs:** None

---

#### ST-15 — BLG-GOV-109: AI audit log retention policy

**Owner:** AI Compliance Governance Officer; Infrastructure & Operations Owner
**Estimated effort:** S (~4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Recommended 12 months or aligned with Supabase retention (BLG-OPS-53). Cleanup mechanism required (scheduled job or row-level TTL).

**Staging-only ACs:** None

---

#### ST-16 — BLG-GOV-110: Arc 4 trade_plan data completeness audit

**Owner:** Data Model & Domain Schema Owner; Product Owner
**Estimated effort:** S (~5 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Per-field null% for: entry_rationale, confirmation_criteria, r_target, setup_type, pre_entry_validation_snapshot. Fields >50% null = data gaps. File BLG-FE-68+ if Arc 4 dependency risk is critical.

**Staging-only ACs:** None — data audit document; verifiable by reading

---

#### ST-17 — BLG-GOV-104: strategy_rules.md §11 parameter validation

**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Estimated effort:** M (~10 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None (but most likely outcome = "insufficient data" given last known count of 6 trades)

**Notes:** RISK-02: last known closed trade count is 6 (v4.6 audit 2026-05-31). "Insufficient data" is a valid and expected AC outcome. Pull from production database. PO ratifies any parameter changes.

**Staging-only ACs:** None — parameter validation document; verifiable by reading

---

#### ST-23 — BLG-GOV-113: SI-05 effectiveness review protocol

**Owner:** Product Owner; Director of Quality
**Estimated effort:** S (~5 hrs)
**Delegation class:** autonomous

**Acceptance Criteria (from backlog slice conditional):** SI-05 effectiveness review protocol document produced specifying: participants (Product Owner + Director of Quality), evidence sources (si05_digest_log, BLG-GOV-96 criteria, RFJ view counts post-delivery), output format, decision authority. Must complete by 2026-07-01.

**Dependencies:** None

**Notes:** Gate "Before 2026-07-01" — included at planning time 2026-06-09. Protocol document only — not an actual review execution.

**Staging-only ACs:** None

---

#### ST-24 — BLG-GOV-114: si05_digest_log schema validation

**Owner:** Director of Quality; Data Model & Domain Schema Owner
**Estimated effort:** S (~4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria (from backlog slice conditional):** si05_digest_log schema validated against BLG-GOV-96 effectiveness criteria fields (send_at, status, recipient, content hash). PASS or urgent gap stories filed. Must complete before 2026-07-01.

**Dependencies:** None

**Notes:** Gate "Before 2026-07-01" — included at planning time 2026-06-09. If schema gaps found: file BLG-BE-36+ before sprint close.

**Staging-only ACs:** None

---

### EPIC-04 — QA, Testing & Frontend Review

**Maps to:** S2-18, S2-19, S2-20, S2-21, S2-22
**Owner:** Director of Quality; QA Lead; Base44 Frontend Prompt Owner
**Estimated effort:** ~28 hrs
**Risk IDs:** RISK-03 (partially resolved)
**Execution sequence:** 4 (Sprint 2, merges after EPIC-03; ST-20 requires EPIC-01 on main)
**Sprint:** 2

---

#### ST-18 — BLG-QA-52: Tax year P&L boundary edge case validation

**Owner:** Financial Reporting & Records Owner; QA Lead
**Estimated effort:** S (~5 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** UK tax year boundary: April 6. Scenarios: Dec 31 → Apr 7 (straddle); Apr 4 → Apr 8. File BLG-BE-36+ if bugs found.

**Staging-only ACs:** None — test data scenarios verifiable in test suite

---

#### ST-19 — BLG-QA-53: SI-05 digest Playwright E2E coverage

**Owner:** QA Lead
**Estimated effort:** M (~10 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** Telegram API must be mocked/stubbed — no real API calls in CI. ≥3 scenarios required: happy path, empty red flag, compliance score in digest.

**Staging-only ACs:** None — Playwright tests run in CI with mocked Telegram

---

#### ST-20 — BLG-QA-54: Playwright coverage matrix update post-v5.2

**Owner:** Director of Quality
**Estimated effort:** S (~4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** EPIC-01 (ST-04–ST-07) must be merged to main before this story — coverage matrix must capture new contract docs

**Notes:** Schedule ST-20 last in EPIC-04 (after ST-19 Playwright scenarios are written) to capture all new v5.3 scenarios in the matrix count.

**Staging-only ACs:** None

---

#### ST-21 — BLG-FE-66: Red Flag Journal post-launch UX review

**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Estimated effort:** S (~5 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** P3 — **deferrable to v5.4 if Sprint 2 capacity tightens**. File BLG-FE-68+ for any significant friction found. UX review document only.

**Staging-only ACs:** None

---

#### ST-22 — BLG-FE-67: BLG-FE-64 visual design review scope definition

**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** S (~4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None (gate: BLG-FE-64 clears 2026-06-21 — scope definition should complete by or at that date)

**Notes:** One-page scope document for BLG-FE-64. Must clearly distinguish from BLG-FE-66 (visual vs interaction design).

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Available capacity | ~100–120 hrs total (2 sprints × ~50–60 hrs) |
| Sprint 1 estimated effort | ~39 hrs |
| Sprint 2 estimated effort | ~71 hrs |
| Total estimated effort | ~110 hrs |
| Utilisation | ~92–110% |
| Over-allocation | ⚠️ Sprint 2 at upper bound — PO accepts per WARN acknowledgement |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-25 — BLG-FE-64 (conditional) | EPIC-04 | Gate date 2026-06-21 not yet reached at planning time 2026-06-09; add via amendment cycle if gate clears |

## Deferred Execution Blockers Accepted

*(deferred_execution_blockers was empty in state.json — section omitted)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| OA-RP-01: PT-04 trade count gate re-verification — `SELECT COUNT(*) FROM trade_history WHERE pnl IS NOT NULL`; if ≥20 add PT-04 via amendment cycle; update current_roadmap.md + BLG-FEAT-25 with count | PMO Lead; Product Owner | **Yes** |
| Capacity WARN acknowledgement — PO must explicitly accept Sprint 2 upper-bound WARN and confirm deferral policy for ST-21/ST-17 | Product Owner | **Yes** |
| Sprint goal sign-off — Product Owner confirms or replaces candidate sprint goal | Product Owner | **Yes** |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — Product Owner, 2026-06-09
**Scope confirmed:** Confirmed — Product Owner, 2026-06-09
**Capacity WARN acknowledged:** Confirmed — Sprint 2 upper bound accepted; ST-21 (BLG-FE-66, P3) and/or ST-17 (BLG-GOV-104) may defer to v5.4 if capacity tightens — Product Owner, 2026-06-09
**OA-RP-01 resolved:** Confirmed — PT-04 gate NOT MET (6 closed trades / 11 total, re-verified 2026-06-09); PT-04 remains parked; current_roadmap.md + BLG-FEAT-25 updated — PMO Lead, 2026-06-09
**Date:** 2026-06-09
