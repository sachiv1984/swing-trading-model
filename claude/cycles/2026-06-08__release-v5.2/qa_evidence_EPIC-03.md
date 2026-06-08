Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-08

---

# QA Evidence — EPIC-03: SI-05 Security Reviews & Endpoint Compliance

## Per-Story Entries

### ST-09 — BLG-GOV-97: Claude API model deprecation compliance check

**Spec references:** `docs/governance/ai_model_deprecation_check_v52.md` (created this story)
**Commit SHA:** 139c6181

**What was built:** Compliance check record verifying that `claude-haiku-4-5-20251001` (pinned in `backend/services/ai_service.py:16`) is not deprecated. Model confirmed as current Claude 4.X / Haiku 4.5. Document includes model inventory, deprecation status, next review date (2026-09-08), and AI Compliance & Governance Officer sign-off.

**Acceptance criteria:**
- AC-01: Model lifecycle checked — `claude-haiku-4-5-20251001` in `backend/services/ai_service.py:16` ✓
- AC-02: Result documented with timestamp; model not deprecated — next review 2026-09-08 ✓
- AC-03: AI Compliance & Governance Officer sign-off ✓
- AC-04: Model found at expected location (ai_service.py:16 as `MODEL_VERSION`) ✓

**Result:** Pass

---

### ST-10 — BLG-GOV-98: Telegram bot token minimal-permission security review

**Spec references:** `docs/security/security_register.md` (Review 002 appended)
**Commit SHA:** 139c6181

**What was built:** Security review of Telegram bot token permissions. Confirmed from code that only `sendMessage` API is called (`backend/services/si05_digest_service.py:268`) and only to a fixed `TELEGRAM_CHAT_ID`. Documented in security_register.md Review 002 as PASS with recommendation for manual BotFather verification. Cybersecurity & Trust Lead sign-off recorded.

**Acceptance criteria:**
- AC-01: Telegram bot token permissions reviewed — send-only usage confirmed from code ✓
- AC-02: Findings documented: sendMessage only, fixed chat target, BotFather manual check recommended ✓
- AC-03: security_register.md Review 002 appended with date, scope, finding (PASS with recommendation) ✓
- AC-04: No overly permissive permissions identified from code; recommendation filed for BotFather verification ✓
- AC-05: Cybersecurity & Trust Lead sign-off ✓

**Result:** Pass with notes (BotFather manual verification recommended; code-level review complete)

---

### ST-11 — BLG-GOV-99: SI-05 digest endpoint authentication review

**Spec references:** `docs/specs/api_contracts/digest_endpoints.md`, `docs/security/security_register.md` (Review 003 appended)
**Commit SHA:** 139c6181

**What was built:** Authentication review of `POST /digest/si05/send`. Authentication gap found: endpoint is unauthenticated (bare `@router.post` decorator at `backend/routers/digest.py:227`). Documented in security_register.md Review 003 as GAP_FOUND. P2 backlog item BLG-BE-35 filed for auth fix. Does not block EPIC-03 merge per sprint_backlog.md notes.

**Acceptance criteria:**
- AC-01: Authentication status documented — endpoint callable without auth ✓
- AC-02: Gap found path followed — P2 backlog item BLG-BE-35 filed; gap documented in security_register.md ✓
- AC-03: security_register.md Review 003 appended with GAP_FOUND finding ✓
- AC-04: Cybersecurity & Trust Lead sign-off ✓
- AC-05: Head of Engineering sign-off (implementation sign-off N/A — fix out-of-scope for this EPIC) ✓

**Result:** Pass (review complete; gap documented; P2 filed; does not block EPIC-03)

---

### ST-12 — BLG-GOV-100: Backend endpoint documentation coverage audit post-v5.1

**Spec references:** `docs/ops/endpoint_coverage_audit_v52.md` (created this story)
**Commit SHA:** 139c6181

**What was built:** Full audit of 50 endpoints across 20 backend/routers/ files. Coverage check against openapi.yaml, test.py, and api_contracts/. 6 contract gaps identified; 4 BLG-SPEC items filed (BLG-SPEC-49/50/51/52). Audit document committed to docs/ops/. Note: POST /digest/si05/send (BLG-SPEC-48/ST-04) confirmed COVERED — contract in digest_endpoints.md, openapi.yaml entry present, test.py entry present.

**Acceptance criteria:**
- AC-01: All @router.get/post/put/delete decorators enumerated — 50 total routes ✓
- AC-02: Each route cross-checked against openapi.yaml, test.py, and api_contracts/ ✓
- AC-03: Coverage gaps documented by category ✓
- AC-04: BLG-SPEC-49/50/51/52 filed for contract gaps ✓
- AC-05: Head of Engineering and API Contracts & Documentation Owner sign-off ✓
- AC-06: Audit findings committed to docs/ops/endpoint_coverage_audit_v52.md ✓

**Result:** Pass

---

## EPIC-Level Consolidation Block

**EPIC:** EPIC-03 — SI-05 Security Reviews & Endpoint Compliance
**Cycle:** 2026-06-08__release-v5.2
**Sprint goal:** Deliver all SI-05 operational hardening and v5.1 spec compliance work so the weekly digest service is observable, audited, and compliant with all production and governance standards.
**Test scenarios used:** None — all stories are review/audit documents; AC verifiable by document inspection only.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-09 | docs/governance/ai_model_deprecation_check_v52.md | Model lifecycle compliance check document — Haiku 4.5 not deprecated | AC-01 to AC-04 | Pass | None |
| ST-10 | docs/security/security_register.md (Review 002) | Telegram bot token permission review — send-only confirmed | AC-01 to AC-05 | Pass with notes | None |
| ST-11 | docs/security/security_register.md (Review 003) | Digest endpoint auth review — GAP_FOUND; BLG-BE-35 P2 filed | AC-01 to AC-05 | Pass | None (gap documented, P2 filed, does not block) |
| ST-12 | docs/ops/endpoint_coverage_audit_v52.md | 50 routes audited; 6 contract gaps; 4 BLG-SPEC items filed | AC-01 to AC-06 | Pass | None (gaps filed as BLG-SPEC-49/50/51/52) |

**QA test coverage:**
- Scenarios run: Document inspection — no executable tests; all stories are review/audit deliverables
- Regression areas checked: Security register, api_contracts/ inventory, openapi.yaml coverage
- Known deviations filed: None (ST-11 auth gap filed as BLG-BE-35 P2 backlog item, not a sprint deviation)

---

## Sign-Off

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓
- [x] Criterion 2: All AC verifiable by document inspection alone — no observable UI behaviour, no staging run required — ✓
- [x] Criterion 3: No frontend-visible change — no React pages or UI components created or modified — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-06-08
- Comments: Autonomous class sign-off — all four qualifying criteria met. EPIC-03 produces review documents and audit records only. ST-11 auth gap (BLG-BE-35) is a documented finding filed as P2 backlog item; it does not constitute a sprint deviation as the review-only scope was defined in sprint_backlog.md. All 4 stories done; no P0/P1 deviations.
