**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.9
**Cycle:** 2026-06-02__release-v4.9
**Published:** 2026-06-02

---

# Backlog Slice — v4.9

**Firm stories: 5 (ST-01–ST-05)**
**Conditional stories: 2 (ST-06–ST-07) — EPIC-04 gate: 2026-06-21**

---

## EPIC-01 — Security & Dependency Hardening

Maps to: S2-01

---

### ST-01 — npm devDependency HIGH CVE remediation

**Source:** BLG-OPS-49
**EPIC:** EPIC-01
**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Effort:** S (~0.5 day)
**Class:** autonomous
**Staging-only ACs:** None

**Description:** 21 HIGH severity vulnerabilities found in frontend devDependency chain via react-scripts (2026-06-01 audit). All are build toolchain CVEs (not production runtime). Remediate via npm audit fix.

**Acceptance Criteria:**
- AC-01: `npm audit fix` applied to project root package.json; build passes with no errors
- AC-02: HIGH vulnerability count = 0 after fix (`npm audit --audit-level=high` exits 0)
- AC-03: No regression in production bundle behaviour (app loads, existing Playwright CI suite passes)
- AC-04: Findings documented in security_register.md (remediation date, CVEs addressed)

---

### ST-02 — Anthropic SDK upgrade 0.40.0 → latest

**Source:** BLG-OPS-50
**EPIC:** EPIC-01
**Owner:** Head of Engineering
**Effort:** S–M (~0.5–1 day)
**Class:** autonomous
**Staging-only ACs:** AC-04

**Description:** Anthropic Python SDK pinned at v0.40.0 (65 minor versions behind as of 2026-06-01). Upgrade to latest stable (0.105.2 or current). Review changelog for breaking API changes affecting AI thesis generation and daily cost check endpoints.

**Acceptance Criteria:**
- AC-01: `backend/requirements.txt` updated: `anthropic==0.40.0` → `anthropic==0.105.2` (or latest stable at time of execution)
- AC-02: Full backend test suite passes post-upgrade (`pytest tests/` or equivalent)
- AC-03: SDK changelog reviewed for breaking changes in 0.40.0 → latest range; any breaking changes documented and addressed
- AC-04: [staging-only] POST /trade-plans/{plan_id}/generate-thesis and POST /ai/check-daily-cost functional on staging post-upgrade
- AC-05: Upgrade documented in security_register.md (version, date, rationale)

---

## EPIC-02 — CI/QA Infrastructure Strengthening

Maps to: S2-02

---

### ST-03 — Wire Phase B CI with real Postgres service

**Source:** BLG-QA-40
**EPIC:** EPIC-02
**Owner:** QA Lead; Head of Engineering
**Effort:** M (~1–2 days)
**Class:** autonomous
**Staging-only ACs:** None

**Description:** Phase A CI runs against stub DATABASE_URL with all DB calls mocked. Missing-schema columns are invisible to CI. When position_state, state_entered_at, state_history were never added to positions table via startup migration, all CI was green but endpoints returned 500 in production. Phase B (commented out in ci-tests.yml) requires real Postgres service container.

**Acceptance Criteria:**
- AC-01: Postgres service container added to ci-tests.yml GitHub Actions `services:` block with correct version
- AC-02: `DATABASE_URL` wired for the Phase B job step (uses repo secret)
- AC-03: Phase B test run enabled (currently commented out in workflow)
- AC-04: All existing integration tests pass against the real Postgres service container in CI (no collection errors)
- AC-05: A PR introducing a SQL query referencing a non-existent column causes the Phase B job to FAIL (verified via test in ST-04)
- AC-06: Phase A (stub/mock tests) continues to run without a real DB and passes

---

### ST-04 — Schema smoke test: lifecycle columns on positions table

**Source:** BLG-QA-41
**EPIC:** EPIC-02
**Owner:** QA Lead
**Effort:** S (~0.5 day)
**Class:** autonomous
**Staging-only ACs:** None
**Depends on:** ST-03 (Phase B CI must be wired)

**Description:** No test verifies that ensure_lifecycle_columns() creates the position_state, state_entered_at, state_history columns. A schema introspection test closes this class of silent missing-column bug permanently.

**Acceptance Criteria:**
- AC-01: Test added to `tests/test_position_lifecycle.py` (or new `tests/test_schema.py`): calls `ensure_lifecycle_columns()` then queries `information_schema.columns` and asserts all three columns (position_state, state_entered_at, state_history) are present on the positions table
- AC-02: Test fails if any of the three columns is absent from the positions table
- AC-03: Test is skipped/excluded when DATABASE_URL points to the stub (Phase A) — not run under Phase A
- AC-04: Test passes in Phase B CI environment (real Postgres service container from ST-03)

---

## EPIC-03 — Governance Debt Clearance

Maps to: S2-03

---

### ST-05 — roadmap_prompt.md STEP 8.1 Empty Now Horizon gate strengthening

**Source:** BLG-GOV-78, LL-RP-v4.8-01
**EPIC:** EPIC-03
**Owner:** Head of Specs Team; PMO Lead
**Effort:** S (~0.5 day)
**Class:** autonomous
**Staging-only ACs:** None

**Description:** When a roadmap rebalance runs as "No-change" and the Now horizon is empty, roadmap_prompt.md v6.7 STEP 8.1 fires an advisory only. In v4.8 release planning, this caused STEP -1.2 to flag no formal roadmap section (recurring LL-RP-v4.8-01). Convert the advisory to a soft gate requiring an explicit PO decision.

**Acceptance Criteria:**
- AC-01: roadmap_prompt.md STEP 8.1 updated: when Now horizon is empty AND no next-release section exists in current_roadmap.md, require explicit PO decision — options: (a) add the next-release section now, or (b) defer intentionally with written rationale recorded in cycle summary; non-blocking soft gate requiring documented PO choice
- AC-02: PO decision options documented clearly in the STEP 8.1 text with example format
- AC-03: roadmap_prompt.md **Version:** bumped (v6.7 → v6.8)
- AC-04: OPERATIONAL_GUIDE.md §6 Roadmap Engine source prompt header updated to new version
- AC-05: OPERATIONAL_GUIDE.md §14 governance table Roadmap Engine Source updated to new version; OPERATIONAL_GUIDE.md version bumped per §6 checklist
- AC-06: prompt_change_log.md entry appended: `| 2026-06-02 | roadmap_prompt.md | v6.7→v6.8 | BLG-GOV-78/LL-RP-v4.8-01: STEP 8.1 Empty Now Horizon gate strengthening... | Head of Specs Team + PMO Lead |`
- AC-07: Head of Specs Team + PMO Lead sign-off confirmed

---

## EPIC-04 — Arc 5 SI-05 Phase 1 (Conditional)

Maps to: S2-04

**Gate condition:** SI-01 (shipped v3.8, 2026-05-20) + SI-03 (shipped v3.9, 2026-05-22) live ≥ 30 days.
**Gate clears:** 2026-06-21 (30 days after SI-03 ship)
**Sprint planning must confirm gate before sealing EPIC-04 stories.**

---

### ST-06 — SI-05 Phase 1 backend service + Telegram delivery [conditional]

**Source:** BLG-GOV-67
**EPIC:** EPIC-04
**Owner:** Head of Backend Engineering
**Effort:** M (~1.5–2 days)
**Class:** autonomous
**Staging-only ACs:** AC-09
**Condition:** EPIC-04 gate confirmed cleared at sprint planning (2026-06-21)

**Description:** Implement SI-05 Phase 1: weekly strategy integrity digest delivered via existing Telegram notification infrastructure (v2.4 weekly_digest pattern). Phase 1 uses SI-01 + SI-03 data only — no SI-02 drift score. Includes new backend service, GET endpoint, API contract, and all CLAUDE.md §2 same-commit requirements.

**Acceptance Criteria:**
- AC-01: `backend/services/weekly_integrity_digest_service.py` created — computes: `validation_pass_rate` (7d window, from red_flag_events SI-01 overrides), `override_count` (7d), `red_flag_frequency_trend` (7d vs prior 7d delta); no SI-02 dependency
- AC-02: `GET /portfolio/weekly-integrity-digest` endpoint implemented; returns JSON with validation_pass_rate, override_count, red_flag_frequency_trend, period_start, period_end
- AC-03: Weekly Telegram delivery: scheduled job in existing weekly_digest infrastructure; message format includes SI-05 Phase 1 metrics; no-data state handled gracefully
- AC-04: API contract created at `docs/specs/api_contracts/weekly_integrity_digest_contract.md` with response schema documented
- AC-05: `docs/reference/openapi.yaml` updated with GET /portfolio/weekly-integrity-digest path in the same commit as the contract (CLAUDE.md §2)
- AC-06: `backend/routers/test.py` registration updated with GET /portfolio/weekly-integrity-digest entry (representative path test)
- AC-07: `src/pages/SystemStatus.js` hardcoded fallback endpoint count updated to reflect new total
- AC-08: `tests/e2e/system-status.spec.js` SC-SS-01b updated to match new fallback value (same commit as AC-07 per CLAUDE.md §2)
- AC-09: [staging-only] Weekly Telegram message confirmed received on staging with correct SI-05 Phase 1 metrics; Infrastructure & Operations Owner sign-off recorded
- AC-10: Unit tests for digest service: covers empty data state (no override events), single-week data, period boundary calculation

---

### ST-07 — SI-05 Phase 1 Playwright coverage [conditional]

**Source:** BLG-GOV-67 (companion)
**EPIC:** EPIC-04
**Owner:** QA Lead
**Effort:** S–M (~0.5–1 day)
**Class:** autonomous
**Staging-only ACs:** None
**Condition:** EPIC-04 gate confirmed; depends on ST-06

**Description:** Playwright coverage for the SI-05 Phase 1 endpoint. Since the weekly digest is Telegram-delivered (not a new frontend page), Playwright coverage targets the API endpoint response shape and the system status count.

**Acceptance Criteria:**
- AC-01: Playwright test `SC-SID-01`: `GET /portfolio/weekly-integrity-digest` returns HTTP 200 with JSON containing `validation_pass_rate`, `override_count`, `red_flag_frequency_trend`, `period_start`, `period_end`
- AC-02: Playwright test `SC-SID-02`: `GET /portfolio/weekly-integrity-digest` with no red_flag_events data returns valid JSON with 0/null values — graceful empty state
- AC-03: Playwright test `SC-SS-01b` (system-status): verifies SystemStatus.js endpoint count updated correctly (regression guard for ST-06 AC-07/08)
- AC-04: All 3 new Playwright scenarios pass in CI
- AC-05: Test file location: `tests/e2e/weekly-integrity-digest.spec.js` (or equivalent canonical location)

---

*Release Slice v4.9 | Cycle: 2026-06-02__release-v4.9 | Published: 2026-06-02*
<!-- release-plan-marker: RP:v4.9:2026-06-02__release-v4.9 -->
