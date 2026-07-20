Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-20

# QA Evidence Log — EPIC-07 (v7.6)

## Consolidation Block

**EPIC:** EPIC-07 — Consolidated monthly AI cost view (reframed to single-provider Claude view)
**Cycle:** 2026-07-20__release-v7.6
**Sprint goal:** Ship print/PDF export for WeeklyDigest and TradePlan (BLG-FE-119) and clear six ready backend/QA/documentation items to fully utilise this sprint's confirmed capacity.
**Test scenarios used:** `tests/e2e/ai-usage-costs.spec.js` (5 scenarios) + `tests/test_monthly_ai_cost.py` (4 scenarios).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-07 | `docs/design/.../consolidated-ai-cost-view/ux_spec.md#7`, `docs/specs/frontend/pages/settings.md#6`, `docs/specs/api_contracts/ai_endpoints.md#GET /ai/monthly-cost` | Reframed the story per `ESC-EXEC-20260720-01`: new `GET /ai/monthly-cost` endpoint (Claude-only, sourced from `claude_audit_log`); new Settings §6 "Claude API Usage & Costs" SectionCard (single figure, independent query, loading/error states) | Consolidated view shows both providers' costs and a combined total for the current month, added to an existing settings/reports surface; combined total matches the sum of the two existing per-provider sources — **superseded by the v1.1 addendum**: shows the current month's Claude API total (the only real provider), sourced correctly from `claude_audit_log` | Pass | Design-artefact deviation — see below |

**QA test coverage:**
- Scenarios run: `tests/e2e/ai-usage-costs.spec.js` (5/5 passing) — loaded state with correct figure, explicit regression guard confirming no "Gemini" or "Combined Total" text renders anywhere, zero-spend renders `$0.00` not blank, fetch failure shows "AI cost data unavailable" with no numeric fallback, a failed cost fetch does not block the rest of the Settings page (Strategy Parameters section and Save button still render)
- Backend unit tests: `tests/test_monthly_ai_cost.py` (4/4 passing) — SQL aggregation correctness, zero-spend case, current-calendar-month filter, DB-failure fail-safe (returns zeros, never raises)
- Regression areas checked: `tests/test_daily_cost_alert.py` (5/5) and `tests/test_claude_audit_log_filters.py` (6/6) re-run — confirmed the new `get_monthly_claude_cost()` function and `GET /ai/monthly-cost` endpoint did not affect the existing daily-cost-alert or claude-audit-log query paths
- Known deviations filed: **Design-artefact deviation, not a code deviation.** The original UX spec (v1.0, PO-approved) and backlog item `BLG-FEAT-77` were both premised on Gemini and Claude being two separate cost-generating providers — a factually incorrect premise discovered during implementation (`gemini_service.py` calls only the Anthropic API; no Gemini integration exists anywhere in this codebase). This was escalated as `ESC-EXEC-20260720-01` (Quality trigger) rather than silently implemented or silently redesigned. Product Owner resolved it in-session (option (a), single-provider reframe). Documented as `docs/design/.../consolidated-ai-cost-view/ux_spec.md` §7 v1.1 addendum — the addendum *is* the deviation record for the design artefact, per `document_lifecycle_guide.md` §9 treatment of design-artefact corrections.

## CLAUDE.md §2 Same-Commit Compliance Check

- `docs/reference/openapi.yaml` — `/ai/monthly-cost` path added, same commit as the router change — confirmed present
- `docs/specs/api_contracts/ai_endpoints.md` — `## GET /ai/monthly-cost` heading (canonical `##` level, not `###`) — confirmed present, v1.7
- `backend/routers/test.py` — endpoint registered — confirmed present (line ~188)
- `src/pages/SystemStatus.js` hardcoded fallback count — updated 102 → 103 — confirmed, matches actual `"name":` count in `test.py` (103)
- `tests/e2e/system-status.spec.js` SC-SS-01b — updated to match the new fallback value — confirmed present

## Frontend Testing Gate (CLAUDE.md §2 / execution_prompt.md §3.2.A)

This EPIC introduces a frontend-visible change (new SectionCard in `Settings.js`) — the BLG-GOV-19 autonomous sign-off class is **not** available (criterion 3 fails: `src/pages/Settings.js` modified). Every observable AC has Playwright coverage per `tests/e2e/ai-usage-costs.spec.js` (rendering, loading skeleton, error message, page-independence) — no AC was deferred to "code review only."

## Agent-Mediated Director of Quality Sign-Off (§5.3)

Per `claude/agents/director_of_quality.md`, a subagent reviewed the reframe against the role's quality bar and the acceptance criteria above, with instructions to independently execute (not just read) both test suites.

**First pass: Blocked.** Findings:
1. `tests/e2e/ai-usage-costs.spec.js` failed to load (`Cannot find module './fixtures/api-mocks'`) — the EPIC-07 branch had not merged `main` since EPIC-05 landed the shared fixture library, so the spec file existed but could not run. **Fixed:** merged `main` into `exec/2026-07-20__release-v7.6/EPIC-07` per `CLAUDE.md §8`; re-ran and confirmed 5/5 pass.
2. `docs/specs/frontend/pages/settings.md` §Purpose & User Goals retained a stale "combined monthly AI provider (Gemini + Claude) spend" bullet that was not updated when §6 itself was reframed — directly contradicted the new §6 content two sections later. **Fixed:** corrected to "View Claude API spend for the current month at a glance."

Non-blocking: `backend/routers/ai.py` module docstring cited a stale contract version (v1.4, should be v1.7) — fixed in the same pass.

**Second pass (implicit — findings applied in the same commit before re-submission):** All blocking findings resolved; both fixes verified (Playwright re-run 5/5 passing, `settings.md` confirmed to have no remaining stale Gemini/Combined-Total references outside the explanatory reframe narrative and changelog history, which correctly describe what changed).

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-07-20
- Comments: Approved after the two findings above were fixed and re-verified. Backend implementation (`get_monthly_claude_cost`, `GET /ai/monthly-cost` endpoint) confirmed correct on first pass — canonical envelope, fails safe, no side effects. Frontend confirmed to contain zero "Gemini" or "Combined Total" references (the entire point of the reframe) once the stale spec bullet was corrected. All CLAUDE.md §2 same-commit requirements verified present.

**Post-sign-off CI gate finding (not covered by the DoQ review scope above):** PR #1035's "API Performance Baseline Drift Detection (ST-12)" check failed — the review prompt did not ask the subagent to check this gate. `docs/ops/api_performance_baseline.md` §29 added (registration-only entry, `GET /ai/monthly-cost`, following the established §26–28 pattern) in a follow-up commit. This is a documentation-only, mechanical fix (no functional or test-scenario change), so it did not require a further DoQ re-review pass — noted here for a complete record.
