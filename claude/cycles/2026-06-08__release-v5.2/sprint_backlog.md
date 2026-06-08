**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2
**Release:** v5.2
**Sprint Goal:** Deliver all SI-05 operational hardening (reliability, security reviews, runbooks) and v5.1 spec compliance work (OA-01, OA-02, BLG-SPEC-47, BLG-SPEC-48), and produce the QA and governance documents that enable the staged verification sprint, so the weekly digest service is observable, audited, and compliant with all production and governance standards.
**Backlog Slice Source:** original — `claude/cycles/2026-06-08__release-v5.2/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-06-08__release-v5.2

## Merge Order

**Execution sequence:** EPIC-03 → EPIC-02 → EPIC-04 → EPIC-01

**execution_state.json owner:** EPIC-03 (first in merge order). EPIC-02, EPIC-04, and EPIC-01 branches must check for `execution_state.json` existence before creating — if found, append their EPIC section rather than overwrite.

**Shared files:** `docs/reference/openapi.yaml` and `backend/routers/test.py` are touched by multiple EPICs; later EPICs (EPIC-02, EPIC-01) must rebase onto `main` after EPIC-03 merges before finalising their changes to these files. `docs/specs/api_contracts/` touched by EPIC-01 (ST-04) and EPIC-03 (ST-12 audit); EPIC-01 rebases after EPIC-03 merges. Full shared-file advisory: `sprint_planning_notes.md` Multi-EPIC Execution Notes section.

---

## Sprint Scope

### EPIC-03 — SI-05 Security Reviews & Endpoint Compliance

**Maps to:** S2-09, S2-10, S2-11, S2-12
**Owner:** AI Compliance & Governance Officer; Cybersecurity & Trust Lead; Head of Engineering; API Contracts & Documentation Owner
**Estimated effort:** ~2.0 days
**Risk IDs:** RISK-03
**Execution sequence:** 1 (merge first)

---

#### ST-09 — BLG-GOV-97: Claude API model deprecation compliance check

**Owner:** AI Compliance & Governance Officer; Head of Engineering
**Estimated effort:** XS (~30 minutes)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** XS priority — complete first in EPIC-03. If deprecated model found: file P0 sprint story immediately (takes priority over all other v5.2 work per AC-02).

**Staging-only ACs:** None

---

#### ST-10 — BLG-GOV-98: Telegram bot token minimal-permission security review

**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Findings documented in security_register.md. If overly permissive: request token rotation and file P1 backlog item before seal.

**Staging-only ACs:** None

---

#### ST-11 — BLG-GOV-99: SI-05 digest endpoint authentication review

**Owner:** Cybersecurity & Trust Lead; Head of Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous (review) + delegated_backend (if fix required)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Per RISK-03 — if auth gap found and fixed inline: add unit test verifying 401 on unauthenticated call. If fix out-of-scope: file P2 backlog item. Does not block EPIC-03 merge.

**Staging-only ACs:** None (review phase); if fix is implemented inline, staging verification for AC-02 fix path may be required — document at execution time.

---

#### ST-12 — BLG-GOV-100: Backend endpoint documentation coverage audit post-v5.1

**Owner:** Head of Engineering; API Contracts & Documentation Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** Logically after ST-04 (EPIC-01) which may close one contract gap — can run in parallel if ST-04 check completes first. In merge order, ST-12 is in EPIC-03 (merges first) while ST-04 is in EPIC-01 (merges last). Run ST-12 audit after EPIC-03 execution starts; note any gap ST-04 will close.

**Notes:** Audit findings committed as document in docs/ops/ or docs/governance/. BLG-SPEC items filed for each contract gap per AC-04.

**Staging-only ACs:** None

---

### EPIC-02 — SI-05 Backend Reliability & Operations

**Maps to:** S2-05, S2-06, S2-07, S2-08
**Owner:** Backend Engineering Patterns Owner; Infrastructure & Operations Owner
**Estimated effort:** ~2.5 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

---

#### ST-05 — BLG-BE-32: SI-05 Telegram delivery retry and failure handling

**Owner:** Backend Engineering Patterns Owner; Infrastructure & Operations Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Minimum AC: delivery failures logged at ERROR level (not silently swallowed). Retry policy is defined by the implementer — either exponential backoff (max 2 retries, 30s/60s) or explicit no-retry decision documented with rationale.

**Staging-only ACs:** AC-04 (Infrastructure & Operations Owner confirms failure mode observable in Render logs — staging-only evidence; CI cannot reproduce Telegram API failure mode in production log stream)

---

#### ST-06 — BLG-BE-33: SI-05 digest delivery log table

**Owner:** Data Model & Domain Schema Owner; Backend Engineering Patterns Owner
**Estimated effort:** S (~1 day)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None (but ST-08 health check references this table for best observability)

**Notes:** DB migration requires `CREATE TABLE IF NOT EXISTS` guard per RISK-02. Per CLAUDE.md §2: if GET /digest/si05/log endpoint implemented — register in backend/routers/test.py, add openapi.yaml entry, author API contract document, update SystemStatus.js fallback count and SC-SS-01b in tests/e2e/system-status.spec.js in the same commit. Data Model & Domain Schema Owner signs off on schema.

**Staging-only ACs:** AC-04 (Infrastructure & Operations Owner confirms migration present in staging DB — staging-only evidence; CI integration tests cannot verify production database migration state)

---

#### ST-07 — BLG-OPS-55: Deployment runbook update for SI-05 operational environment

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (~1–2 hours)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Committed to docs/operations/ or equivalent existing path. Referenced by ST-08 health check procedure.

**Staging-only ACs:** None

---

#### ST-08 — BLG-OPS-56: SI-05 service scheduled run health check procedure

**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** XS (~1–2 hours)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** Logically depends on ST-06 (si05_digest_log) for best observability; can proceed using Render logs or Telegram history as interim if ST-06 not yet merged.

**Notes:** If SI-05 delivery log not yet available at time of authoring, document interim procedure and reference BLG-BE-33 as prerequisite for full observability.

**Staging-only ACs:** None

---

### EPIC-04 — SI-05 QA, Verification & Product Governance

**Maps to:** S2-13, S2-14, S2-15, S2-16
**Owner:** Director of Quality; QA & Testing Owner; QA Lead; Product Owner; PMO Lead
**Estimated effort:** ~1.5–2.0 days
**Risk IDs:** RISK-04 (closed — ST-17 deferred)
**Execution sequence:** 3

---

#### ST-13 — BLG-QA-46: SI-05 digest service edge case test gap analysis

**Owner:** QA Lead; Backend Engineering Patterns Owner
**Estimated effort:** XS (~1–2 hours)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Review 21 existing tests against 5 edge cases. Gap analysis document required; missing tests authored if found. QA Lead and Backend Engineering Patterns Owner sign-off.

**Staging-only ACs:** None

---

#### ST-14 — BLG-QA-47 + BLG-GOV-94: SI-05 Phase 1 acceptance test protocol and delivery verification protocol

**Owner:** QA & Testing Owner; Director of Quality
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None (produces planning documents; independent of EPIC-02 backend stories)

**Notes:** Combined as companion documents per scope plan. Both documents reference each other. Filed in docs/operations/ or docs/qa/ alongside BLG-GOV-89 staged verification sprint protocol. Director of Quality signs off on both.

**Staging-only ACs:** None

---

#### ST-15 — BLG-QA-48: Regression test suite baseline refresh post-v5.1

**Owner:** QA Lead
**Estimated effort:** XS (~1–2 hours)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** If POST /digest/si05/send absent from backend/routers/test.py — note as gap and align with ST-04 (EPIC-01) which verifies this. QA Lead sign-off.

**Staging-only ACs:** None

---

#### ST-16 — BLG-GOV-96: SI-05 Phase 1 effectiveness measurement criteria

**Owner:** Product Owner; PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** 30-day review date = 2026-07-04 (30 days from SI-05 Phase 1 ship date 2026-06-04). Criteria committed to claude/cycles/2026-06-08__release-v5.2/ or docs/product/decisions/. Product Owner explicitly acknowledges criteria and review date.

**Staging-only ACs:** None

---

### EPIC-01 — Governance Prompt Patches & Spec Compliance

**Maps to:** S2-01, S2-02, S2-03, S2-04
**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Estimated effort:** ~1.75–2.0 days
**Risk IDs:** RISK-01
**Execution sequence:** 4 (merge last)

---

#### ST-01 — OA-01: release_planning_prompt.md §-1.2 STEP 8.1 Option(b) patch

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** CLAUDE.md §6 checklist mandatory — version bump, OPERATIONAL_GUIDE §14 update, prompt_change_log.md entry in same commit. Head of Specs Team sign-off required.

**Staging-only ACs:** None

---

#### ST-02 — OA-02: execution_prompt.md §3.1.A test-authoring spec_references guidance

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** CLAUDE.md §6 checklist mandatory. Head of Specs Team sign-off on patch wording.

**Staging-only ACs:** None

---

#### ST-03 — BLG-SPEC-47: Align SI-05 pass_rate computation with BLG-GOV-86 §5.2

**Owner:** Head of Specs Team; Head of Backend Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous (spec determination) + delegated_backend (if Option(b) implementation required)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Head of Specs Team canonical determination is the key deliverable. If Option(b) chosen and implementation required in si05_digest_service.py, escalate to delegated_backend. CLAUDE.md §6 checklist if governance files modified. DEV-v51-EPIC01-01 must be resolved and closed at completion.

**Staging-only ACs:** None (spec determination path); if Option(b) implementation required: AC-03 execution testing should include a unit test for the corrected computation (no staging-only evidence required for unit tests).

---

#### ST-04 — BLG-SPEC-48: POST /digest/si05/send API contract gap check and authoring

**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Estimated effort:** XS–S (~1–2 hours if exists; ~0.5 day if authoring needed)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Per CLAUDE.md §2 — new contract document requires `##`-level heading (not `###`). openapi.yaml entry required if contract is new or missing. backend/routers/test.py entry must exist for the endpoint. API Contracts Owner and HoST sign-off.

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 working days (workforce_capacity.md) |
| Total estimated effort (in-scope, 16 stories) | ~7.9 days (mid-point) |
| Utilisation | ~56–66% |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-17 (BLG-FE-64) | EPIC-04 | Gate: SI-03 Red Flag Journal live ≥ 30 days — gate clears 2026-06-21 but sprint planning seals 2026-06-08 (13 days before gate clear). Deferred to v5.3 per stage4_backlog_slice.md AC-03 and RISK-04 mitigation plan. |

## Deferred Execution Blockers Accepted

*(No deferred execution blockers — `deferred_execution_blockers` is empty in state.json.)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| delivery_verification_prompt.md v3.0 log entry verification | PMO Lead | RESOLVED — confirmed in prompt_change_log.md (2026-06-21) |
| BLG-FE-64 gate status confirmation | Product Owner | RESOLVED — gate not clear; ST-17 deferred to v5.3 |
| OA-01 and OA-02 in sprint scope | PMO Lead | RESOLVED — ST-01 (OA-01) and ST-02 (OA-02) confirmed in EPIC-01 |

No blockers remain at seal.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — "Deliver all SI-05 operational hardening and v5.1 spec compliance work so the weekly digest service is observable, audited, and compliant"
**Scope confirmed:** Confirmed — 16 stories across 4 EPICs; ST-17 deferred to v5.3 (gate not clear)
**Capacity confirmed:** Confirmed — ~7.9 days estimated effort within 12–14 day capacity; WARN acknowledged
**Deferred execution blockers accepted (if any):** N/A — no deferred execution blockers
**Signed off by:** Product Owner
**Date:** 2026-06-08
