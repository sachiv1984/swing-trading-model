**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v5.2
**Cycle:** 2026-06-08__release-v5.2
**Last Updated:** 2026-06-08

---

# Backlog Slice — v5.2 Governance Debt, SI-05 Ops & Spec Compliance

<!-- release-plan-marker: RP:v5.2:2026-06-08__release-v5.2 -->

---

## EPIC-01 — Governance Prompt Patches & Spec Compliance

**Maps to:** S2-01, S2-02, S2-03, S2-04
**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Estimated effort:** ~2.5 days
**Risk IDs:** RISK-01
**Execution sequence:** 4 (merge last)

This EPIC closes the two outstanding OA patches (OA-01 and OA-02) carried forward from v5.1, resolves the P3 spec deviation (DEV-v51-EPIC01-01) from v5.1, and closes the P1 spec debt (BLG-SPEC-48) for the POST /digest/si05/send API contract. All governance file edits must follow CLAUDE.md §6 checklist (version bump, OPERATIONAL_GUIDE.md §14 update, prompt_change_log.md entry). Head of Specs Team signs off on all stories.

---

### ST-01 — OA-01: release_planning_prompt.md §-1.2 STEP 8.1 Option(b) patch

**EPIC:** EPIC-01
**Backlog ID:** OA-01 (v5.1 D-1 carry-forward LL-RP-v5.1-01)
**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Patch release_planning_prompt.md §-1.2 to explicitly accept a roadmap section created via STEP 8.1 Option(b) PO decision as a valid §-1.2 gate substitute. Prevents recurring advisory at each release planning invocation when Option(b) is used.

**Acceptance Criteria:**
- AC-01: release_planning_prompt.md §-1.2 updated with explicit clause accepting STEP 8.1 Option(b) PO-documented roadmap metadata as equivalent to a formal planned release section; wording must be unambiguous
- AC-02: release_planning_prompt.md version bumped (v2.33 → v2.34)
- AC-03: OPERATIONAL_GUIDE.md §6B source prompt header and §14 Release Engine Source updated to v2.34 in the same commit
- AC-04: prompt_change_log.md row appended: date=2026-06-08, prompt=release_planning_prompt.md, v2.33→v2.34, change summary, authority=Head of Specs Team
- AC-05: Head of Specs Team sign-off on patch content
- AC-06: OPERATIONAL_GUIDE.md version bumped and §14 changelog entry added per CLAUDE.md §6 requirements

**Dependencies:** None
**Notes:** CLAUDE.md §6 checklist mandatory for all governance file edits.

---

### ST-02 — OA-02: execution_prompt.md §3.1.A test-authoring spec_references guidance

**EPIC:** EPIC-01
**Backlog ID:** OA-02 (v5.1 D-2 carry-forward)
**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Add guidance to execution_prompt.md §3.1.A clarifying that for test-authoring stories (stories whose sole deliverable is a new test file), `spec_references` should be populated with the created test file path (e.g., `tests/e2e/signals-allocation-insufficient.spec.js`) rather than left empty. This prevents traceability flags at delivery verification.

**Acceptance Criteria:**
- AC-01: execution_prompt.md §3.1.A updated with explicit note: for test-authoring stories (sole deliverable is a test file, no prior spec applicable), spec_references should reference the created test file path, not be left empty
- AC-02: execution_prompt.md version bumped (v3.36 → v3.37)
- AC-03: OPERATIONAL_GUIDE.md §8 source prompt header and §14 Execution Engine Source updated to v3.37 in the same commit
- AC-04: prompt_change_log.md row appended: date=2026-06-08, prompt=execution_prompt.md, v3.36→v3.37, change summary, authority=Head of Specs Team
- AC-05: Head of Specs Team sign-off on patch wording
- AC-06: OPERATIONAL_GUIDE.md version bumped and §14 changelog entry added per CLAUDE.md §6 requirements

**Dependencies:** None
**Notes:** CLAUDE.md §6 checklist mandatory.

---

### ST-03 — BLG-SPEC-47: Align SI-05 pass_rate computation with BLG-GOV-86 §5.2

**EPIC:** EPIC-01
**Backlog ID:** BLG-SPEC-47
**Owner:** Head of Specs Team; Head of Backend Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous (spec determination) + delegated_backend (if implementation required)
**Staging-only ACs:** None (spec decision; if implementation: AC-05 staging test)

**Objective:** Resolve DEV-v51-EPIC01-01: determine whether `validation_pass_rate` in si05_digest_service.py should use (a) volume-weighted overall ratio or (b) mean of per-rule pass rates per BLG-GOV-86 §5.2. Update spec and/or implementation to make them consistent.

**Acceptance Criteria:**
- AC-01: Head of Specs Team makes canonical determination: Option (a) — amend BLG-GOV-86 §5.2 to accept volume-weighted ratio, OR Option (b) — require mean-of-per-rule-rates approach
- AC-02: BLG-GOV-86 §5.2 (si05-telegram-message-format-spec.md) and digest_endpoints.md v0.2 are internally consistent and match the chosen computation method after resolution
- AC-03: If Option (b) chosen — si05_digest_service.py `validation_pass_rate` computation corrected to iterate `validation_pass_rate_by_rule` entries and compute arithmetic mean
- AC-04: If governance files modified: CLAUDE.md §6 checklist applied (version bump, OPERATIONAL_GUIDE §14, prompt_change_log.md)
- AC-05: DEV-v51-EPIC01-01 resolved and closed; BLG-SPEC-47 marked complete in backlog
- AC-06: Head of Specs Team sign-off on canonical determination

**Dependencies:** None
**Notes:** P3 deviation but must resolve before next SI-05 feature increment. Head of Specs Team determination is the key deliverable.

---

### ST-04 — BLG-SPEC-48: POST /digest/si05/send API contract gap check and authoring

**EPIC:** EPIC-01
**Backlog ID:** BLG-SPEC-48
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Estimated effort:** XS–S (~1–2 hours if exists; ~0.5 day if authoring needed)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Verify whether docs/specs/api_contracts/ contains a `## POST /digest/si05/send` entry. If missing, author the contract covering request/response schema, error cases (503 Telegram unavailable), and authentication requirements. Add to openapi.yaml if missing. Confirm backend/routers/test.py entry exists.

**Acceptance Criteria:**
- AC-01: docs/specs/api_contracts/ contains a file with `## POST /digest/si05/send` as a `##`-level heading (not `###`)
- AC-02: openapi.yaml has a corresponding POST /digest/si05/send path entry
- AC-03: backend/routers/test.py confirms POST /digest/si05/send endpoint exists in the test coverage
- AC-04: API contract document covers: request body (none required or minimal), response schema (200 + error cases), authentication requirements, Telegram failure error (503 or equivalent)
- AC-05: API Contracts & Documentation Owner and Head of Specs Team sign-off
- AC-06: If new contract document authored: version history and Last Updated fields populated; openapi.yaml version bumped if applicable

**Dependencies:** None
**Notes:** CLAUDE.md §2 same-sprint contract rule retroactively applied for v5.1 spec debt.

---

## EPIC-02 — SI-05 Backend Reliability & Operations

**Maps to:** S2-05, S2-06, S2-07, S2-08
**Owner:** Backend Engineering Patterns Owner; Infrastructure & Operations Owner
**Estimated effort:** ~2.5 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

This EPIC implements backend reliability improvements for the SI-05 weekly digest service (retry handling, delivery log), and documents the operational environment requirements (deployment runbook, health check procedure). BLG-BE-33 (delivery log table) is a prerequisite for BLG-OPS-56 (health check references the log). Both backend stories require DB migration with staging verification.

---

### ST-05 — BLG-BE-32: SI-05 Telegram delivery retry and failure handling

**EPIC:** EPIC-02
**Backlog ID:** BLG-BE-32
**Owner:** Backend Engineering Patterns Owner; Infrastructure & Operations Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** delegated_backend
**Staging-only ACs:** AC-04 (verify retry observable in Render logs)

**Objective:** Document the current si05_digest_service.py failure mode for Telegram delivery failures. Define and implement a retry policy: at minimum, ensure delivery failures are logged at ERROR level. If no retry exists, implement simple exponential backoff (max 2 retries: 30s/60s delays). Document in code or ops runbook.

**Acceptance Criteria:**
- AC-01: Current Telegram delivery failure mode documented (exception raised, logged, or swallowed — which one)
- AC-02: At minimum, delivery failure is logged at ERROR level and not silently swallowed in si05_digest_service.py
- AC-03: Retry policy defined and documented: either (a) simple exponential backoff (max 2 retries, 30s/60s) implemented, or (b) explicit no-retry decision documented with rationale
- AC-04: Infrastructure & Operations Owner confirms failure mode is observable in Render logs (staging-only evidence acceptable)
- AC-05: Unit tests cover the documented failure path (ERROR log emitted on Telegram API failure) — at minimum 1 test

**Dependencies:** None
**Notes:** Spec reference: si05_digest_service.py in backend/services/; BLG-GOV-86 §6 failure modes section (if present).

---

### ST-06 — BLG-BE-33: SI-05 digest delivery log table

**EPIC:** EPIC-02
**Backlog ID:** BLG-BE-33
**Owner:** Data Model & Domain Schema Owner; Backend Engineering Patterns Owner
**Estimated effort:** S (~1 day)
**Delegation class:** delegated_backend
**Staging-only ACs:** AC-04 (confirm table present in staging DB)

**Objective:** Create si05_digest_log table to durably record each weekly digest delivery attempt. Write a row on each send attempt (success and failure). Optional: expose GET /digest/si05/log endpoint if scoped.

**Acceptance Criteria:**
- AC-01: New table `si05_digest_log` created via DB migration: id, sent_at, status (sent/failed), event_count, telegram_message_id, error_message, created_at
- AC-02: si05_digest_service.py writes a log row on each send attempt (both success and failure paths)
- AC-03: Migration added to database startup script (database.py or equivalent) with CREATE TABLE IF NOT EXISTS guard
- AC-04: Migration confirmed present in staging DB (staging-only evidence; Infrastructure & Operations Owner sign-off)
- AC-05: Data Model & Domain Schema Owner sign-off on schema
- AC-06: If GET /digest/si05/log endpoint implemented: registered in backend/routers/test.py, openapi.yaml entry added, API contract document authored per CLAUDE.md §2

**Dependencies:** None (but BLG-OPS-56 depends on this table existing)
**Notes:** If optional endpoint deferred, file BLG-OPS item for follow-up.

---

### ST-07 — BLG-OPS-55: Deployment runbook update for SI-05 operational environment

**EPIC:** EPIC-02
**Backlog ID:** BLG-OPS-55
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (~1–2 hours)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Update deployment runbook (docs/operations/ or equivalent) with SI-05 Phase 1 operational requirements: Telegram bot token environment variable name, cron schedule configuration, service health check approach, failure detection reference.

**Acceptance Criteria:**
- AC-01: Deployment runbook updated with: (a) environment variable name for Telegram bot token, (b) purpose and where to obtain the token, (c) how the weekly digest schedule is configured (cron job configuration in Render or APScheduler), (d) how to verify the digest service is running
- AC-02: Failure detection reference included (points to BLG-BE-33 delivery log once available, or Render log pattern as interim)
- AC-03: Infrastructure & Operations Owner sign-off on updated runbook
- AC-04: Runbook file committed to docs/operations/ or equivalent existing path

**Dependencies:** None
**Notes:** Referenced by BLG-OPS-56 health check procedure.

---

### ST-08 — BLG-OPS-56: SI-05 service scheduled run health check procedure

**EPIC:** EPIC-02
**Backlog ID:** BLG-OPS-56
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** XS (~1–2 hours)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Define and document the health check procedure for verifying the SI-05 weekly digest ran successfully. Choose the simplest observable check and document it in the ops runbook.

**Acceptance Criteria:**
- AC-01: Health check procedure documented: what to check, where to find the evidence, what constitutes PASS; must reference at least one of: (a) si05_digest_log table (from ST-06), (b) Render service logs INFO entry, (c) Telegram chat history
- AC-02: Procedure specifies: check cadence (weekly, after expected send time), evidence format, responsible role
- AC-03: If no observable check is possible without si05_digest_log: document that BLG-BE-33 is prerequisite and procedure is interim until ST-06 ships
- AC-04: Infrastructure & Operations Owner and Head of Engineering sign-off on procedure
- AC-05: Procedure committed to docs/operations/ alongside ST-07 runbook update

**Dependencies:** Logically depends on ST-06 (si05_digest_log) for best observability; can proceed without it using Render logs or Telegram history
**Notes:** If BLG-BE-33 endpoint is implemented in ST-06, reference it here.

---

## EPIC-03 — SI-05 Security Reviews & Endpoint Compliance

**Maps to:** S2-09, S2-10, S2-11, S2-12
**Owner:** AI Compliance & Governance Officer; Cybersecurity & Trust Lead; Head of Engineering; API Contracts & Documentation Owner
**Estimated effort:** ~2.0 days
**Risk IDs:** RISK-03
**Execution sequence:** 1 (merge first)

This EPIC conducts mandatory security and compliance reviews for SI-05 Phase 1 capabilities and performs a post-v5.1 endpoint documentation audit. All four stories produce review/audit documents with sign-offs — no code changes unless a gap is found. If BLG-GOV-99 finds an authentication gap, the fix is filed as a separate P2 backlog item rather than blocking this EPIC.

---

### ST-09 — BLG-GOV-97: Claude API model deprecation compliance check

**EPIC:** EPIC-03
**Backlog ID:** BLG-GOV-97
**Owner:** AI Compliance & Governance Officer; Head of Engineering
**Estimated effort:** XS (~30 minutes)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Check Anthropic model lifecycle page for the currently pinned model's deprecation status. Record result with timestamp and next review date. If deprecated, file P0 sprint story immediately.

**Acceptance Criteria:**
- AC-01: Anthropic model lifecycle page checked for the model pinned in ai_service.py (or equivalent BLG-GOV-64 location) — specific model name and current deprecation status recorded
- AC-02: Check result documented with timestamp: (a) if not deprecated: record check date, next review date (per BLG-GOV-90 quarterly procedure); (b) if deprecated: file P0 sprint story to update pinned model immediately
- AC-03: AI Compliance & Governance Officer sign-off on check result
- AC-04: If model pinning found in a different location than expected: record actual file path and variable name for future reference

**Dependencies:** None
**Notes:** If deprecated, P0 story takes priority over all other v5.2 work. BLG-GOV-90 defines the quarterly procedure this check initiates.

---

### ST-10 — BLG-GOV-98: Telegram bot token minimal-permission security review

**EPIC:** EPIC-03
**Backlog ID:** BLG-GOV-98
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Verify the Telegram bot token used by SI-05 is configured with minimal permissions (send-only to designated chat; cannot read messages, list chats, or send to arbitrary chats). Document findings in security_register.md.

**Acceptance Criteria:**
- AC-01: Telegram bot token permissions verified via BotFather settings or Telegram API check: confirm send-only access to designated digest chat
- AC-02: Review findings documented: what permissions were verified, how verified, whether bot is properly scoped
- AC-03: security_register.md updated with review entry: date, scope, finding (PASS / REQUIRES_MITIGATIONS), evidence method
- AC-04: If overly permissive: request token rotation with appropriate scope restriction; file P1 backlog item; record in security_register.md
- AC-05: Cybersecurity & Trust Lead sign-off on review

**Dependencies:** None

---

### ST-11 — BLG-GOV-99: SI-05 digest endpoint authentication review

**EPIC:** EPIC-03
**Backlog ID:** BLG-GOV-99
**Owner:** Cybersecurity & Trust Lead; Head of Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous (review) + delegated_backend (if fix required)
**Staging-only ACs:** None (review); AC-04 staging if fix implemented

**Objective:** Review POST /digest/si05/send authentication status. Determine whether API key authentication is required per the existing auth pattern (v2.2 BLG-SEC-01). Document finding and apply fix if gap found, or file separate story if fix is out of scope for this EPIC.

**Acceptance Criteria:**
- AC-01: Authentication status of POST /digest/si05/send documented: whether it requires API key auth, how auth is enforced (middleware, decorator, etc.)
- AC-02: If authentication gap found (endpoint callable without auth): either (a) fix inline in this story and confirm with unit test + security_register.md update, or (b) file P2 backlog item with full fix spec and document gap in security_register.md
- AC-03: security_register.md updated with review entry (PASS or GAP_FOUND)
- AC-04: Cybersecurity & Trust Lead sign-off on review outcome
- AC-05: Head of Engineering sign-off if fix is implemented

**Dependencies:** None
**Notes:** Per RISK-03 — if auth gap found and fixed inline, add unit test verifying 401 on unauthenticated call.

---

### ST-12 — BLG-GOV-100: Backend endpoint documentation coverage audit post-v5.1

**EPIC:** EPIC-03
**Backlog ID:** BLG-GOV-100
**Owner:** Head of Engineering; API Contracts & Documentation Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Enumerate all routes in backend/routers/ and verify each has: (a) openapi.yaml entry, (b) test.py entry, (c) API contract document in docs/specs/api_contracts/. Document gaps; file BLG-SPEC items for contract gaps.

**Acceptance Criteria:**
- AC-01: All @router.get/post/put/delete decorators in backend/routers/ enumerated (total count recorded)
- AC-02: Each route cross-checked against openapi.yaml (path present), backend/routers/test.py (endpoint present), and docs/specs/api_contracts/ (## METHOD /path heading present)
- AC-03: Coverage gaps documented per category: openapi.yaml gaps, test.py gaps, contract document gaps
- AC-04: BLG-SPEC items filed in backlog.md for each identified contract gap (follow existing BLG-SPEC format)
- AC-05: Head of Engineering and API Contracts & Documentation Owner sign-off on audit findings
- AC-06: Audit findings committed as a document in docs/ops/ or docs/governance/ (or noted in qa_evidence for this EPIC)

**Dependencies:** Logically after ST-04 (which may close one contract gap) — can run in parallel if ST-04 check completes first
**Notes:** This audit covers v5.1 deliverables specifically; establish as routine check for future post-ship closures.

---

## EPIC-04 — SI-05 QA, Verification & Product Governance

**Maps to:** S2-13, S2-14, S2-15, S2-16, S2-17 (firm); S2-18 (conditional: gate 2026-06-21)
**Owner:** Director of Quality; QA & Testing Owner; QA Lead; Product Owner; Head of UX & Design
**Estimated effort:** ~3.0–3.5 days
**Risk IDs:** RISK-04
**Execution sequence:** 3

This EPIC produces QA, verification, and product governance documents that enable the SI-05 staged verification sprint and Phase 2 planning. Three items (BLG-QA-47, BLG-GOV-94, BLG-GOV-96) have external coordination dependencies but produce self-contained documents. The conditional item (BLG-FE-64) gates on 2026-06-21; sprint planning must confirm gate cleared.

---

### ST-13 — BLG-QA-46: SI-05 digest service edge case test gap analysis

**EPIC:** EPIC-04
**Backlog ID:** BLG-QA-46
**Owner:** QA Lead; Backend Engineering Patterns Owner
**Estimated effort:** XS (~1–2 hours)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Review the 21 existing unit tests in si05_digest_service.py test file against 5 edge cases: (a) zero events in 7-day window, (b) Telegram API connection failure, (c) message at character limit boundary, (d) partial send, (e) service invocation with no SI-01 data. Document gap analysis. Author missing tests if found.

**Acceptance Criteria:**
- AC-01: Gap analysis document produced listing all 5 edge cases with coverage status (covered/missing) and test file reference
- AC-02: If gaps found: missing tests authored in the appropriate test file and confirmed passing
- AC-03: If all 5 edge cases covered: document as verified with test file references
- AC-04: QA Lead and Backend Engineering Patterns Owner sign-off on gap analysis

**Dependencies:** None

---

### ST-14 — BLG-QA-47 + BLG-GOV-94: SI-05 Phase 1 acceptance test protocol and delivery verification protocol

**EPIC:** EPIC-04
**Backlog ID:** BLG-QA-47; BLG-GOV-94
**Owner:** QA & Testing Owner; Director of Quality
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Produce both the acceptance test protocol (BLG-QA-47) and delivery verification protocol (BLG-GOV-94) for SI-05 Phase 1 staged verification sprint. These are companion documents covering the same deferred ACs. Combine into a single story for efficiency.

**Acceptance Criteria:**
- AC-01 (BLG-QA-47): Acceptance test protocol document produced covering v5.1 deferred ACs: ST-01 AC-09 (Telegram digest delivery confirmed on staging) and ST-05 AC-01 (compliance_summary live data on staging); each AC has: test steps, expected outcome, evidence format, sign-off authority
- AC-02 (BLG-GOV-94): Delivery verification protocol produced for both deferred ACs; references BLG-GOV-89 (staged verification sprint protocol) for format; specifies what constitutes pass/fail for each AC
- AC-03: Both documents reference each other as companion inputs
- AC-04: Director of Quality sign-off on both documents
- AC-05: Documents filed in docs/operations/ or docs/qa/ alongside BLG-GOV-89 protocol

**Dependencies:** None (does not depend on BLG-BE-33 or BLG-OPS-55 — produces planning documents)
**Notes:** BLG-QA-47 and BLG-GOV-94 combined as companion stories per scope plan.

---

### ST-15 — BLG-QA-48: Regression test suite baseline refresh post-v5.1

**EPIC:** EPIC-04
**Backlog ID:** BLG-QA-48
**Owner:** QA Lead
**Estimated effort:** XS (~1–2 hours)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Update regression test baseline to include v5.1 additions: POST /digest/si05/send endpoint and signals-allocation-insufficient.spec.js Playwright scenarios.

**Acceptance Criteria:**
- AC-01: POST /digest/si05/send confirmed in backend/routers/test.py (or noted as gap if absent)
- AC-02: signals-allocation-insufficient.spec.js 5 Playwright scenarios confirmed in CI regression run
- AC-03: Regression baseline document (if exists) updated to include v5.1 additions; if no formal document exists, file BLG-QA item for its creation as a follow-on
- AC-04: QA Lead sign-off on baseline refresh

**Dependencies:** None

---

### ST-16 — BLG-GOV-96: SI-05 Phase 1 effectiveness measurement criteria

**EPIC:** EPIC-04
**Backlog ID:** BLG-GOV-96
**Owner:** Product Owner; PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Staging-only ACs:** None

**Objective:** Define SI-05 Phase 1 effectiveness criteria and schedule the 30-day review (2026-07-04). Criteria must be defined before the review date. Record criteria in a governance note.

**Acceptance Criteria:**
- AC-01: Effectiveness criteria defined and documented: frequency criteria (PO reviews ≥ N of last M digests), action criteria (≥ 1 digest-triggered app action/month), and 30-day self-assessment criteria
- AC-02: 30-day review date scheduled: 2026-07-04 (30 days from SI-05 Phase 1 ship date 2026-06-04)
- AC-03: Product Owner explicitly acknowledges criteria and review date
- AC-04: PMO Lead confirms criteria check is included in Phase 2 activation criteria (BLG-GOV-92) when that item is scheduled
- AC-05: Criteria documented in a governance note committed to claude/cycles/2026-06-08__release-v5.2/ or docs/product/decisions/

**Dependencies:** None

---

### ST-17 — BLG-FE-64: BLG-FE-41 Red Flag Journal visual design review pre-brief (CONDITIONAL)

**EPIC:** EPIC-04
**Backlog ID:** BLG-FE-64
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Staging-only ACs:** None
**Gate:** SI-03 Red Flag Journal live ≥ 30 days (gate clears 2026-06-21)

**Objective:** Produce a design review brief for BLG-FE-41 (Red Flag Journal visual design review). The brief defines review scope, evaluation criteria, and expected deliverable. Input to BLG-FE-41 sprint planning when gate clears.

**Acceptance Criteria:**
- AC-01: Design review brief produced for BLG-FE-41 covering: scope definition (filters UX, severity visual hierarchy, event type colour coding, timeline vs list layout), evaluation criteria, deliverable format
- AC-02: Brief reviewed and signed off by Head of UX & Design before 2026-06-21
- AC-03: Gate condition verified: SI-03 Red Flag Journal shipped 2026-05-22; gate clears 2026-06-21 ✓ (must confirm at sprint planning)
- AC-04: Brief committed to docs/product/ux/ or equivalent

**Dependencies:** Gate clears 2026-06-21 — sprint planning must confirm before including this story
**Notes:** CONDITIONAL story. If gate not confirmed clear at sprint planning, defer to v5.3. All other EPIC-04 stories are gate-free.
