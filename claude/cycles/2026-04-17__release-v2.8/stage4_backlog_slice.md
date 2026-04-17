**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.8
**Cycle:** 2026-04-17__release-v2.8
**Last Updated:** 2026-04-17

---

# Backlog Slice — v2.8 Frontend Completion, Test Quality & AI Journal Feature

<!-- release-plan-marker: RP:v2.8:2026-04-17__release-v2.8 -->

---

## EPIC-01 — Market Correlation Frontend

**Maps to:** S2-01 (BLG-FE-14)
**Owner:** Frontend Specifications & UX Owner
**Sprint:** Sprint 2
**Theme:** Completing v2.7 deferred frontend work

---

### ST-01 — Market Correlation View

**Maps to:** EPIC-01 / S2-01
**Source:** BLG-FE-14; v2.7 ST-08 AC-6 deferred
**Effort:** M (~1–2 days)
**Canonical spec ref:** `docs/specs/api_contracts/analytics_endpoints.md v2.1.0`

**Acceptance Criteria:**
- [ ] A market correlation view is added to the Analytics page (Head of UX & Design to confirm final page placement at sprint planning; fallback: Analytics page)
- [ ] Per-position Pearson correlation coefficient displayed for each position with colour-coded severity badge (`high` = red, `moderate` = amber, `low` = green) matching classifications in analytics_endpoints.md v2.1.0
- [ ] Portfolio-level weighted average correlation displayed with severity badge
- [ ] Positions with `null` correlation (Yahoo Finance unavailable) render gracefully — display "N/A" or equivalent; no error state
- [ ] Data sourced exclusively from `GET /analytics/market-correlation`; no hardcoded values
- [ ] No regression to existing Analytics page content
- [ ] DoQ sign-off with Date field populated

---

## EPIC-02 — Test Scenario Coverage

**Maps to:** S2-02 (BLG-QA-13)
**Owner:** QA & Testing Owner
**Sprint:** Sprint 1
**Theme:** Filling v2.7 test gaps before further feature work

---

### ST-02 — Market Correlation Endpoint Scenarios

**Maps to:** EPIC-02 / S2-02 (market correlation)
**Source:** BLG-QA-13 (SC-CORR-01–04)
**Effort:** S–M (~0.5–1 day)
**Canonical spec ref:** `docs/specs/api_contracts/analytics_endpoints.md v2.1.0`

**Acceptance Criteria:**
- [ ] `docs/testing/analytics_scenarios.md` updated to include:
  - SC-CORR-01: `GET /analytics/market-correlation` returns per-position Pearson correlation with correct fields
  - SC-CORR-02: portfolio-level weighted average correlation included in response
  - SC-CORR-03: 8h cache returns same result on second call within TTL
  - SC-CORR-04: graceful partial response when Yahoo Finance unavailable for one ticker
- [ ] All scenarios reference `analytics_endpoints.md v2.1.0` as canonical spec
- [ ] Existing scenarios in analytics_scenarios.md not modified or removed
- [ ] DoQ sign-off with Date field populated

---

### ST-03 — Supplementary Indicator Field Scenarios

**Maps to:** EPIC-02 / S2-02 (supplementary indicators)
**Source:** BLG-QA-13 (SC-SIG-IND-01–02)
**Effort:** S (~0.5 day)
**Canonical spec ref:** `docs/specs/api_contracts/signal_endpoints.md v1.1`

**Acceptance Criteria:**
- [ ] `docs/testing/signals_scenarios.md` updated to include:
  - SC-SIG-IND-01: `POST /signals/generate` response includes all four supplementary fields (`relative_strength_pct`, `week52_high_proximity_pct`, `avg_daily_volume_20d`, `price_vs_50d_ma`) per signal object
  - SC-SIG-IND-02: `relative_strength_pct` is None (not an error) when benchmark data unavailable
- [ ] All new scenarios reference `signal_endpoints.md v1.1` as canonical spec
- [ ] Existing scenarios in signals_scenarios.md not modified or removed
- [ ] DoQ sign-off with Date field populated

---

## EPIC-03 — Governance Process Hardening

**Maps to:** S2-03 (CF-1), S2-04 (CF-2), S2-05 (BLG-GOV-13)
**Owner:** Head of Specs Team + PMO Lead
**Sprint:** Sprint 1
**Theme:** Closing v2.7 carry-forward governance obligations

---

### ST-04 — DoQ Date Field Reminder Patch

**Maps to:** EPIC-03 / S2-03 (carry-forward CF-1)
**Source:** v2.7 Phase 3 Obs 2 / Phase 4 Obs 1 — DoQ sign-off blocks missing Date field
**Effort:** S (~0.5 day)
**Governed file:** `claude/system/execution_prompt.md`

**Acceptance Criteria:**
- [ ] `execution_prompt.md §3.2.A` updated: add explicit reminder that the DoQ sign-off block `Date:` field must be non-blank before PR can be opened (per §3.2.B pre-condition already in v3.5+)
- [ ] Version bumped: execution_prompt.md vX.Y → vX.Y+1
- [ ] `OPERATIONAL_GUIDE.md` §8 source prompt header and §14 Execution Engine Source updated to new version
- [ ] `claude/system/prompt_change_log.md` entry appended (same commit)
- [ ] CLAUDE.md §6 checklist fully applied
- [ ] DoQ sign-off with Date field populated (self-referential — this story is itself evidence the patch works)

---

### ST-05 — Sprint Close Terminology Clarification

**Maps to:** EPIC-03 / S2-04 (carry-forward CF-2)
**Source:** v2.7 Phase 4 Obs 3 — deviation register "Deviations filed" terminology confusion
**Effort:** S (~0.5 day)
**Target file:** Sprint close template (execution_prompt.md or sprint_close.md as applicable)

**Acceptance Criteria:**
- [ ] Sprint close template clarified: "Deviations filed" refers to spec deviations only (filed via /dev-file); process notations and execution observations belong in execution_state.json notes column, not the deviation register
- [ ] If the fix is in a governed prompt file, CLAUDE.md §6 checklist applied (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry)
- [ ] If the fix is in a non-governed template file only, update the file and add a comment/note; no CLAUDE.md §6 checklist required
- [ ] DoQ sign-off with Date field populated

---

### ST-06 — Backlog Archive Deduplication

**Maps to:** EPIC-03 / S2-05 (BLG-GOV-13)
**Source:** BLG-GOV-13 — ID uniqueness FAIL since v2.4
**Effort:** S (~0.5 day)
**Prerequisite:** Product Owner confirmation of deduplication approach (retain most recent entry per ID; earlier copies removed)

**Acceptance Criteria:**
- [ ] Product Owner has confirmed deduplication approach: retain most recent entry per duplicated ID; remove earlier copies
- [ ] `claude/backlog/backlog_archive.md` contains no duplicate `###` item headers after deduplication
- [ ] No active backlog IDs present in the archive post-deduplication
- [ ] `groom backlog` ID uniqueness scan returns PASS after this story
- [ ] `backlog_archive.md` Last Updated header updated
- [ ] DoQ sign-off with Date field populated

---

## EPIC-04 — AI Journal Summarisation

**Maps to:** S2-06 (BLG-FEAT-16)
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Sprint:** Sprint 2
**Theme:** First AI feature delivery — gate-cleared, conditionally compliant

**§13 Status:** CONDITIONALLY COMPLIANT — SRB-v1.7 (2026-03-02). Mandatory conditions must appear in AC verbatim.

---

### ST-07 — AI Journal Summary Backend

**Maps to:** EPIC-04 / S2-06 (backend)
**Source:** BLG-FEAT-16
**Effort:** M (~1–2 days)
**External dependency:** LLM API (provider TBD; key via env var)

**Acceptance Criteria:**
- [ ] Backend endpoint: `POST /ai/journal-summary` — accepts trade IDs or date range; calls external LLM API to summarise journal entry/exit notes from closed trades; returns summarised text
- [ ] External LLM API key and configuration managed via environment variable; no secrets in code
- [ ] AI summary output is NOT used as input to any signal, scoring, compliance, or recommendation calculation
- [ ] Endpoint returns a clear error/unavailable response when LLM API is unreachable (no 500 propagation)
- [ ] API endpoint added to `docs/reference/openapi.yaml` in the same commit as the contract
- [ ] `## POST /ai/journal-summary` heading added to an API contract spec file at `##` level (not `###`)
- [ ] DoQ sign-off with Date field populated

---

### ST-08 — AI Journal Summary Frontend

**Maps to:** EPIC-04 / S2-06 (frontend)
**Source:** BLG-FEAT-16
**Effort:** M (~1–2 days)
**Depends on:** ST-07 (backend endpoint live)

**Acceptance Criteria:**
- [ ] AI summary displayed on Trade History page (or dedicated summary view) alongside raw journal entries — raw entries remain the source of truth and are visible
- [ ] UI displays label: *"AI-generated summary — for reference only. Not a trading recommendation."* — label must be visible whenever the summary is shown, without requiring user interaction
- [ ] AI summary output is NOT used as input to any signal, scoring, compliance, or recommendation calculation
- [ ] Strategy Rules owner has reviewed and confirmed the implementation does not integrate AI output into any signal pipeline (sign-off required before PR merge; recorded in DoQ sign-off block)
- [ ] Any future scope expansion beyond read-only display triggers a new §13 review before pre-alignment (documented in AC of that story)
- [ ] `null`/error response from backend renders gracefully — display "Summary unavailable" or equivalent
- [ ] No regression to existing Trade History page functionality
- [ ] DoQ sign-off with Date field populated
