**Owner:** Director of Quality
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-22
**Sprint Item:** ST-18 (BLG-QA-171, EPIC-05, v9.6)

---

# Quarterly Full-Suite Playwright Re-Run — Procedure and Run Log

## Purpose

The full Playwright suite is currently only re-run when a story touches the relevant surface, so a regression introduced by an unrelated change (data drift, dependency bump) between touches could go undetected for a long stretch. This document defines a quarterly cadence to close that gap.

## Architecture finding (must be read before running this procedure)

**The existing Playwright E2E suite (`tests/e2e/`, `playwright.config.js`) is entirely mock-based, not live-backend-based, by original design.** Per `playwright.config.js`'s own header and `use:`/`webServer:` blocks:
- `webServer` builds and serves the React app **locally** (`npm run build && npx serve -s build -l 3000`), against a **local** backend base URL (`REACT_APP_API_URL: 'http://localhost:8000'`).
- Every test intercepts its own API calls via Playwright's `page.route()` network interception — the suite's own comment states this explicitly: *"API calls go to API_BASE_URL (localhost:8000 by default). Tests intercept these via page.route() — no live backend required."*
- No test in this suite makes a real network call to any backend, staging or production, or reads from any live database.

This means **"a fresh staging seed" does not literally apply to this suite as currently built** — there is no live staging data for it to be seeded with or run against; every fixture is synthetic, defined per-test via `page.route()` mocks. The idea that produced this story (`IDEA-director-of-quality-20260914-01`) named "staging seed" without qualification; this finding is disclosed here rather than silently building new staging-hitting infrastructure that the suite's actual architecture doesn't call for, or silently reinterpreting the story's own wording without saying so.

**Two genuinely distinct things can each be quarterly-cadenced, and this procedure defines both:**

1. **Full Playwright suite re-run against a fresh CI build** (catches suite/dependency/environment drift — the problem statement's actual concern: "a regression introduced by an unrelated change... between touches"). This needs no staging seed; a fresh `npm ci` + fresh production build on a real GitHub-hosted runner (this suite cannot run in this sandbox at all — `npx playwright install --with-deps chromium` fails here, confirmed by `docs/ops/e2e_production_build_migration_2026-07-29.md`) is the correct "fresh" unit.
2. **Full backend suite's Phase-B real-Postgres-backed tests re-run against a freshly reset-and-seeded staging database** (the actual place a live "staging seed" is meaningful in this codebase — see `tests/test_schema.py`'s Phase A/Phase B split and `BLG-QA-189`'s own precedent, `tests/test_reflection_reminder.py`'s planned Phase-B companion). This is a **separate** suite from Playwright, already has a real Postgres CI service, and already runs on every PR — the quarterly value here is specifically re-running it against a **freshly reset** staging schema (via `.github/workflows/reset-and-seed-staging.yml`), not against whatever accumulated state staging happens to be in, to catch seed-data or migration drift the routine PR-time run wouldn't exercise.

**Disposition needed from Director of Quality (not decided by the engine):** whether to (a) adopt this two-part redefinition as satisfying the story's intent, (b) additionally build new CI infrastructure to point the mock-based Playwright suite at a live staging backend (a materially larger undertaking — would require parameterising `playwright.config.js`'s hardcoded `baseURL`/`REACT_APP_API_URL`, replacing every test's `page.route()` mock with real staging requests or a hybrid mode, and accepting live-staging side effects from an 851-test run), or (c) something else. This procedure documents (a) as the recommended, immediately actionable path; (b) is out of scope for this story's effort estimate.

## Procedure

### Part 1 — Full Playwright suite, fresh CI build (quarterly)

**Cadence:** quarterly.
**Trigger:** `workflow_dispatch` on `.github/workflows/playwright.yml` (the existing CI gate — this part needs no new tooling, only a scheduled/logged re-run of what already exists).
**Steps:**
1. Trigger a fresh run: `gh workflow run playwright.yml --ref main`.
2. Wait for completion; confirm all shards pass (`gh run list --workflow=playwright.yml --limit 1`).
3. Record the result in this file's Run Log below (run URL, date, shard count, pass/fail).

**Next scheduled run:** 2026-12-22 (quarterly from this first run).

### Part 2 — Phase-B backend suite against a freshly reset staging seed (quarterly)

**Cadence:** quarterly, aligned with Part 1.
**Trigger:** two sequential manual steps (kept separate, not auto-chained, since `reset-and-seed-staging.yml` is destructive and should not fire without an explicit human-observed step immediately before the read-only test run that follows it):
1. `gh workflow run reset-and-seed-staging.yml --ref main` — resets and seeds the staging schema fresh.
2. Once confirmed complete, run the Phase-B-eligible backend tests against the freshly-seeded `STAGING_DATABASE_URL` (or the equivalent CI service, if a staging-targeted Phase-B job exists by the time this runs — none does yet; today this step is a local/CI run with `DATABASE_URL` pointed at the reset staging database, matching `docs/infrastructure/staging_setup.md` §8's read-only role for query-only tests, or a role with the access each specific test needs).
3. Record the result in this file's Run Log below.

**Next scheduled run:** 2026-12-22 (aligned with Part 1).

## Run Log

### First run — Part 1 (Playwright, fresh CI build)

**Status: not yet executed.** Per the architecture finding above, this genuinely requires a real GitHub-hosted CI runner (this sandbox cannot install Chromium — confirmed structural limitation, not a credentials gap) and is delegated to Director of Quality to trigger and confirm, per `execution_prompt.md` §3.1.C's `delegated_qa` flow. See `qa_evidence_EPIC-05.md` for the open item.

### First run — Part 2 (Phase-B backend suite, freshly reset staging)

**Status: not yet executed.** Requires the Director of Quality (or a session with live staging write access) to run the reset-and-seed step, which is destructive and must not be triggered without an explicit human-observed decision to do so on the actual staging environment. See `qa_evidence_EPIC-05.md` for the open item.

## Disposition of a future finding

If either part's run surfaces a real regression (not a flake — see `docs/testing/flaky_test_quarantine_process.md` and the Flaky-Test Disposition Addendum in `qa_evidence_template.md` for how to tell the difference): file a `BLG-QA-*`/`BLG-FE-*`/`BLG-BE-*` follow-up as appropriate to the surface affected, and fix directly if trivial.

---

## Acceptance

- Accepted by: _pending — cadence/procedure drafted by Sprint Execution Engine (ST-18, ac-01), the two-part redefinition and first-run execution both need Director of Quality disposition/sign-off._
- Date: _pending_
