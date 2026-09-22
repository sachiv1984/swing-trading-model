**Owner:** Director of Quality
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.3
**Last Updated:** 2026-09-22 (ST-18, BLG-QA-171, EPIC-05, v9.6 — both parts now complete: Part 2 corrected from "run the Phase-B suite against staging" — a naming conflation with ci-tests.yml's own unrelated, always-fresh ephemeral-Postgres Phase B job — to a safe reset-and-seed + independent read-only verification design, run and confirmed; both parts' Run Log entries closed out); prior — 2026-09-22 (Part 2 step 1 (reset-and-seed) completed with real evidence; also fixed a duplicate section heading left by the previous edit); prior — 2026-09-22 (Part 1's first run completed with real evidence); prior history retained — see prior entries in version control.
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

### Part 2 — Staging reset-and-seed, with independent read-only verification (quarterly)

**Correction (2026-09-22, made while executing this procedure's own first run):** this part was originally scoped as "run the Phase-B backend suite against the freshly-seeded database." That conflated two different things sharing the word "Phase B": `.github/workflows/ci-tests.yml`'s Phase B job runs the full `pytest tests/` suite against a **disposable, ephemeral `postgres:15` container spun up inside that CI run** — it has nothing to do with the staging Supabase project, and it already runs continuously on every push/PR against an always-fresh database, so there is no quarterly value in "re-running" it. The Phase A/B split in `tests/test_schema.py` is decided purely by `"stub" in DATABASE_URL` — pointing `DATABASE_URL` at the real `STAGING_DATABASE_URL` and running that same suite would exercise every Phase-B-gated test for real, including `test_schema_rollback_verification.py`, which applies and rolls back schema migrations. Running that against the shared, persistent staging project would very likely have damaged the schema and QA seed data this procedure exists to establish, not verified anything meaningfully. Corrected to a narrower, safe design instead:

**Cadence:** quarterly, aligned with Part 1.
**Trigger:** two sequential manual steps (kept separate, not auto-chained, since `reset-and-seed-staging.yml` is destructive and should not fire without an explicit human-observed step):
1. `gh workflow run reset-and-seed-staging.yml --ref main` — resets and seeds the staging schema fresh.
2. Once confirmed complete, run a small set of **read-only** verification queries against `STAGING_DATABASE_URL` (row counts per seeded table, spot-checking specific values against the reset workflow's own claimed summary) using the `readonly_staging` role (`docs/infrastructure/staging_setup.md` §8) — never the write-capable suite.
3. Record the result in this file's Run Log below.

**Next scheduled run:** 2026-12-22 (aligned with Part 1).

## Run Log

### First run — Part 1 (Playwright, fresh CI build) — completed 2026-09-22

**Status: ✅ Completed.** Director of Quality triggered `gh workflow run playwright.yml --ref main` directly — run [`35729627868`](https://github.com/sachiv1984/swing-trading-model/actions/runs/35729627868), `workflow_dispatch` on `main`, 2026-09-22T12:50:27Z.

**Result — all shards green:**
- `Playwright E2E Acceptance Tests` — 8/8 shards: success
- `Playwright Visual Snapshots` — success (13 passed)
- `Playwright Visual Regression Baselines (pixel-level, advisory)` — job conclusion success; its own step reported 6 failed / 4 passed, but this job runs with `continue-on-error: true` by design (locally-generated baselines are expected to diff on the real CI runner's font-rendering — see `playwright.yml`'s own header comment) and is explicitly advisory, not part of the blocking suite. Not counted as a regression.

No suite/dependency/environment drift found — the concern Part 1 exists to catch (per the Purpose section above) did not manifest this run.

**Next scheduled run:** 2026-12-22 (unchanged).

### First run — Part 2 (staging reset-and-seed + read-only verification) — completed 2026-09-22

**Status: ✅ Completed.**

**Step 1 (reset-and-seed).** Director of Quality updated the `STAGING_DATABASE_URL` secret (it had been pointed at Supabase's direct, IPv6-only host — `db.<ref>.supabase.co:5432` — which GitHub-hosted runners cannot reach; corrected to the Transaction pooler URI, `aws-0-<region>.pooler.supabase.com:6543`, matching this repo's own documented connection-string convention) and triggered `gh workflow run reset-and-seed-staging.yml --ref main` directly. First attempt (run [`35730287893`](https://github.com/sachiv1984/swing-trading-model/actions/runs/35730287893)) failed at the "Reset staging database to baseline" step with `Network is unreachable` — root-caused to the wrong connection-string format, not a permissions or code issue. Second attempt, after the secret fix — run [`35733092701`](https://github.com/sachiv1984/swing-trading-model/actions/runs/35733092701) — succeeded end to end, reporting: reset (all domain tables cleared, baseline inserted), migrate (schema up to date, v2.0), seed (2 open positions [LGEN, BARC] + 2 closed trades; watchlist 4 entries; alerts 4 rules + 2 unread notifications; analytics 12 closed trades [Jan–Mar 2026]; signals 2 active/new + 1 dismissed + 1 entered).

**Step 2 (independent read-only verification).** Using the `readonly_staging` role already available in the sprint-execution sandbox (`docs/infrastructure/staging_setup.md` §8), ran a set of `SELECT COUNT(*)`/spot-check queries directly against the freshly-seeded staging database — independent of, not derived from, the workflow's own claimed summary:

| Table | Claimed | Verified |
|---|---|---|
| `portfolios` | 1 baseline | 1 |
| `positions` | 2 open (LGEN, BARC) | 2 — `[('BARC','open'), ('LGEN','open')]` |
| `trade_history` | 2 + 12 = 14 closed | 14 |
| `watchlist` | 4 entries | 4 — `AAPL, BARC, LGEN, MSFT` |
| `alert_rules` | 4 rules | 4 |
| `notifications` | 2 unread | 2, both `read = False` |
| `signals` | 2 new + 1 dismissed + 1 entered | `{'dismissed': 1, 'entered': 1, 'new': 2}` |
| `positions.user_fill_price` / `trade_history.fill_price` (v2.0 migration columns) | present | both present (`information_schema.columns` confirms) |

Every value matched exactly — no discrepancy found. This is real, independently-obtained evidence, not a restatement of the workflow's own log.

**Next scheduled run:** 2026-12-22 (aligned with Part 1).

## Disposition of a future finding

If either part's run surfaces a real regression (not a flake — see `docs/testing/flaky_test_quarantine_process.md` and the Flaky-Test Disposition Addendum in `qa_evidence_template.md` for how to tell the difference): file a `BLG-QA-*`/`BLG-FE-*`/`BLG-BE-*` follow-up as appropriate to the surface affected, and fix directly if trivial.

---

## Acceptance

- Accepted by: Director of Quality — the two-part redefinition was accepted implicitly by triggering Part 1 and Part 2 step 1 directly rather than specifying an alternative; both parts' first runs completed with real, independently-verified evidence (see Run Log above).
- Date: 2026-09-22
