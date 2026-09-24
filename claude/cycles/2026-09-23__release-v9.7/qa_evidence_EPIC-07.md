Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-24

# QA Evidence — EPIC-07 (Ops, Security & Verification) — 2026-09-23__release-v9.7

**EPIC:** EPIC-07 — Ops, Security & Verification
**Cycle:** 2026-09-23__release-v9.7
**Sprint goal:** Ship PO-05 Lightweight Replay Mode end-to-end and clear the full-capacity, category-balanced debt-clearance slice across Frontend/UX correctness, Backend financial reliability, QA coverage, Governance process debt, Spec/data-model debt, and Ops/security verification — 29 stories, 28.00 days.
**Test scenarios used:** `tests/test_non_registry_dependency_check.py` (ST-29, 12 tests, re-run 2026-09-24: 12 passed); ST-27 was verified live against STAGING by a human operator (see below), not by an automated test file.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-27 | `docs/specs/data_model.md` DS-19; `docs/specs/api_contracts/alerts_endpoints.md` (reflection_reminder) | Human-run staging verification (delegated, `DEL-20260924-02`, completed in-session): see "ST-27 staging evidence" below | (a) Both CHECK constraints and `uq_notifications_reflection_reminder_trade` confirmed present on staging, with evidence recorded; (b) a second evaluation run creates 0 duplicate reminders; (c) the look-back and close-timestamp decisions are recorded | Pass | None (a stale-staging-deploy finding was resolved during verification — see below) |
| ST-28 | `docs/ops/external_api_dependency_register.md` | External-dependency failure-mode matrix added to the register | All 5 dependencies (yfinance, Alpaca, Anthropic, Supabase, Render) documented | Pass | None |
| ST-29 | `.github/workflows/non-registry-dependency-check.yml` (spec_reference_not_applicable for the script itself: new CI guard, no prior spec) | `scripts/check_non_registry_dependencies.py` + workflow (runs on `pull_request`/`push` to main/develop) + `tests/test_non_registry_dependency_check.py` | A test PR adding a `git+ssh` dependency fails CI | Pass with notes | None — see note below |

**ST-27 staging evidence** (all queries and calls run by the operator against the STAGING Supabase project and `trading-assistant-api-staging` only; no production access; no credential is recorded in this repository):

1. **Constraints and index.** The first check found *both* `alert_type` CHECK constraints (`notifications`, `notification_preferences`) **lacking** `reflection_reminder`. Cause: staging was still running pre-v9.6 code — the DS-19 DDL is applied by `ensure_alerts_tables()` at backend startup, so it only reaches a database once a v9.6 backend boots against it (a stale staging deploy, not a code defect; the function was read and is correct/idempotent). After the operator redeployed staging: both constraints list `reflection_reminder`, and `uq_notifications_reflection_reminder_trade` exists as `CREATE UNIQUE INDEX ... ON public.notifications USING btree (((context ->> 'trade_id'::text))) WHERE ((alert_type)::text = 'reflection_reminder'::text)` — matching DS-19.
2. **Idempotency.** An earlier evaluation attempt created 0 reminders and was correctly discarded as vacuous: the 14 seeded closed trades (created 2026-09-22 13:23 UTC) had not yet reached the 48 h mark. Once eligible (age 2d 00:09, all with no reflection): first `POST /alerts/evaluate` → `reflection_reminders` `{candidates: 14, notifications_created: 14, delivery_tasks_enqueued: 0, error: null}`; `COUNT(*)` of `reflection_reminder` rows = 14. Second call → `{candidates: 0, notifications_created: 0, delivery_tasks_enqueued: 0, error: null}`; count still 14. Duplicate-per-`trade_id` query (`GROUP BY context->>'trade_id' HAVING COUNT(*) > 1`) → no rows. (Delivery tasks 0 because the `reflection_reminder` email preference defaults to off, as designed.)
3. **Decisions (Product Owner, human, 2026-09-24):** keep `REFLECTION_REMINDER_LOOKBACK_DAYS = 30`; keep `trade_history.created_at` (falling back to `exit_date`) as the close timestamp. No change to code or spec. Supporting observation from staging: the seeded trades' `exit_date` values (Jan–Mar 2026) would all have been excluded under `exit_date`, but qualified under `created_at` — the intended behaviour.

**ST-29 note (`Pass with notes`):** the AC's literal wording is "a test PR adding a `git+ssh` dependency fails CI." What is evidenced: the guard script's rejection logic for `git+ssh`, `git+https` and `file:` specifiers is unit-tested (12 passed), and the workflow runs that same script on every PR. What has **not** been observed: a live GitHub Actions run failing on a deliberately-introduced non-registry dependency. A Director of Quality should decide whether the unit-level evidence is sufficient or whether a throwaway test PR should be run before sign-off.

**QA test coverage:**
- Scenarios run: `tests/test_non_registry_dependency_check.py` (12 passed); ST-27 live staging verification as above.
- Regression areas checked: no application code changed in this EPIC (docs, a CI workflow, a script, and a test file), so no backend regression surface; the full-suite baseline on `main` is unchanged.
- Known deviations: None found — all stories' deviation checks completed with nothing to file. Two follow-ups are noted for the backlog rather than as deviations: `data_model.md` DS-19's "Verification status" paragraph still says it was never run against live PostgreSQL (now stale — a spec edit outside Sprint Execution's write scope), and there was no check that staging actually redeployed after v9.6 merged.

**Autonomous-class eligibility note (BLG-GOV-19):** not applicable — ST-27 is `delegated_backend` (Criterion 1 fails) and required live staging interaction. Standard Sign-Off Block below.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend component in this EPIC
- Signed off by: Director of Quality
- Date: 2026-09-24
- Comments: Pending human Director of Quality sign-off. Points to look at: the ST-29 note above (no live failing-PR run observed), and that ST-27's evidence is operator-reported (pasted query/API output), not independently re-executed by the engine.
