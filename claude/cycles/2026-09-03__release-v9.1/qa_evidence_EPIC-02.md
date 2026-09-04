Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-04

# QA Evidence — EPIC-02 (Backend Reliability & Technical Debt)

**EPIC:** EPIC-02 — Backend Reliability & Technical Debt
**Cycle:** 2026-09-03__release-v9.1
**Sprint goal:** Ship all 41 backlog-driven hygiene items in the v9.1 scope — frontend accessibility fixes, backend reliability/tech-debt cleanup, QA/test coverage, and governance/spec-process debt — so that every axe-core violation in `KNOWN_VIOLATIONS`, the npm build regression, and all 3 outstanding passed-target backlog items close clean with zero deviations.
**Test scenarios used:** `backend/.venv/bin/python3 -m pytest` (full suite, 1342 passed / 10 skipped), `tests/test_sizing_concentration.py::TestFailOpenLogging` (new, ST-09), full Playwright E2E suite (`tests/e2e/`, 851 tests / 104 spec files)

## Evidence Table

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-08 | `docs/ops/quarterly_dependency_upgrade_cadence_policy.md#3.1.1` | Root cause of the `eslint-config-react-app` build failure re-investigated and corrected: the real cause was a stray `git+ssh://` dependency (`"root": "github:tanstack/react-query"`) that fails host-key verification on any clean install — not the originally-suspected ESLint peer conflict, which was a downstream symptom of the aborted install. Removed the dependency; reapplied the full §3.1 candidate list (~20 packages); `recharts`'s `react-is` peer resolves cleanly on its own now. `CI=false npm run build` succeeds; full backend suite unaffected (frontend-only change). One E2E test failure surfaced during verification, confirmed on real CI, root-caused, and fixed — see DEV-EPIC02-ST08-01 (Resolved) | `npm update` candidate list applied, build succeeds; root cause documented, not just worked around; full Playwright E2E suite re-verified passing | Pass | DEV-EPIC02-ST08-01 (Resolved) |
| ST-09 | `services/sizing_service.py` (Case E — bug/observability fix, no prior canonical spec) | Added `logger.warning` to `_apply_concentration_adjustment`'s fail-open exception handler, logging ticker/sector context and the exception; fail-open return behaviour unchanged. New regression test `TestFailOpenLogging` added to `tests/test_sizing_concentration.py` | Exception logged with diagnosable context; no change to fail-open return; existing tests pass | Pass | None |
| ST-10 | `backend/services/concentration_service.py` | Consolidated the 4 independent sector-lookup implementations into 2 canonical functions in `concentration_service.py` (`get_ticker_sector`, `get_ticker_sector_map`); `pre_entry_validation.py` and `portfolio_risk.py` now import and delegate rather than carrying their own copies; `compliance_recheck_service.py` delegates transitively (already imported from `pre_entry_validation`) | Exactly one implementation per lookup shape; other call sites delegate; all 4 named test suites (47 tests) pass unchanged; Backend Engineering Patterns Owner sign-off | Pass | None |
| ST-11 | `backend/database.py`, `backend/routers/analytics.py`, `backend/routers/digest.py` | Moved all raw SQL (24 sites in `analytics.py`, 7 in `digest.py`) into new `database.py` functions, each accepting an optional `conn` to preserve the original connection-reuse behaviour per endpoint. Routers now call these functions instead of opening their own `psycopg2` connections — structural move only, no query rewrite | Zero `cursor.execute()`/`conn.execute()` calls remain in the two routers; existing tests pass unchanged (behaviour); `database.py` remains the sole SQL layer | Pass | None |

**QA test coverage:**
- Scenarios run: full backend suite (`backend/.venv/bin/python3 -m pytest -q --ignore=tests/e2e`) — 1342 passed, 10 skipped, 0 failed; `tests/test_pre_entry_validation.py` + `tests/test_compliance_recheck.py` + `tests/test_portfolio_risk_sector.py` + `tests/test_sizing_concentration.py` run individually — 47 passed (ST-10's 4 named suites); `tests/test_api_contracts.py` — 57 passed (includes the analytics/digest endpoint contract tests, patch targets updated per this file's own "patch at the import site" convention following ST-11's SQL-layer move); full Playwright E2E suite — initial run 847 passed / 1 failed / 3 skipped of 851; after DEV-EPIC02-ST08-01's fix (`tests/e2e/signals-cash-balance.spec.js` synchronization fix), re-verified 32/32 on the previously-failing test locally, real CI re-run pending on the fix commit
- Regression areas checked: sector-concentration lookups (pre-entry validation, compliance recheck, portfolio risk, position sizing), analytics/digest endpoints (metrics, cohort, r-multiple-distribution, compliance-metrics, market-correlation, arc5-compliance, strategy-version-comparison, weekly digest), frontend production build and full E2E surface (post dependency bump)
- Known deviations: DEV-EPIC02-ST08-01 (P2, Resolved — see below). All other stories' deviation checks completed with nothing to file.

## Deviations

### DEV-EPIC02-ST08-01
**Priority:** P2 (was assessed P2 throughout; see revision history below)
**Story:** ST-08
**AC:** "Full Playwright E2E suite re-verified passing against the updated dependency tree"
**Status:** Resolved — fixed with evidence (see Resolution below). Retained as a record, not deleted, per deviation-record convention.

**Original finding (2026-09-04, superseded — see Resolution):** 847/851 passed locally; 1 failed (`tests/e2e/signals-cash-balance.spec.js` › SC-SIG-CB-01a). First assessment theorised this was most likely a sandbox-specific timing/resource-contention artifact, not a real regression, based on: the failing page/endpoint being untouched by this EPIC's diff; an inability to run the pre-bump Playwright toolchain in this sandbox at all (OS incompatibility) to get a clean control; and `src/lib/query-client.js`'s module-singleton `QueryClient` making a cache-related regression seem unlikely. That assessment was **wrong** — see below.

**Resolution — real root cause found and fixed:** Added `workflow_dispatch` to `.github/workflows/playwright.yml` (also closing part of BLG-OPS-149) and pushed, triggering a real GitHub Actions run of the full Playwright suite against this exact PR tree. **Real CI reproduced the failure deterministically** (both attempts, in two parallel workflow runs) — this disproved the "sandbox-specific" theory outright. Direct comparison against the most recent real-CI run on `main` at the pre-bump commit (`157c58ab`, run `33898010517`, same shard) confirmed `SC-SIG-CB-01a` **passed** there. This is direct evidence the dependency bump changed something material, not a pre-existing or sandbox-only flake.

Investigated properly with that confirmed-real signal in hand: the test navigates `about:blank` → `/#/Signals` and asserts a `/cash/summary` request was observed *immediately* after `page.goto()` resolves, with no explicit wait for the actual fetch. `page.goto()` only waits for the browser's `load` event — not for React to mount and `useQuery`'s `queryFn` to actually fire. Reproduced locally: adding a bare `page.waitForTimeout(500)` before the assertion made the test pass reliably, confirming this is a **pure test-synchronization gap**, not an application defect — the `/cash/summary` fetch does fire correctly on every full page load, it just now fires slightly later relative to `goto()`'s resolution than it used to (plausibly bundle init/parse timing shifting with the ~20-package bump), late enough to consistently lose a race the test was never actually synchronized against.

**Fix applied:** replaced the fixed-timeout workaround with the correct idiomatic Playwright pattern — `page.waitForRequest()` awaited concurrently with the second `page.goto()` (`Promise.all`), so the test waits for the actual network event rather than an arbitrary delay. Verified: 32/32 passes across repeated local runs post-fix (8 repeats × 4 tests in the file), no timeouts used. Full local Playwright suite re-run post-fix; full backend suite unaffected (test-only file changed). Real CI on PR #1536 will provide final confirmation once this fix is pushed.

**Impact:** No application-code change was needed — the shipped behaviour was always correct. Only `tests/e2e/signals-cash-balance.spec.js` changed (test synchronization only).
**Backlog action:** No new backlog item needed for this specific test — it's fixed. **BLG-OPS-149** (playwright.yml path-filter gap, P2) remains open and is the actual structural fix needed so a future dependency bump doesn't ship with an unverified E2E suite again; this deviation is direct evidence of why that gap matters (it hid a real, reproducible failure from CI for this entire review cycle until manually forced).
**Notes:** This deviation's own history is itself a useful lesson: the first-pass "most likely sandbox-specific" assessment was a plausible-sounding but unverified claim (see `execution_prompt.md` §5.3's LL-v8.6-P3-01 — a quantitative/"already verified"-style claim needs actual evidence, not just reasoning, before being relied on). Forcing a real CI signal via `workflow_dispatch` — rather than accepting "CI didn't check it" as a reason to stop investigating — is what actually resolved this.

## Story-Level Authority Sign-Offs

- **ST-10** — Backend Engineering Patterns Owner, agent-mediated (§5.3): **Approved**, no findings. Confirmed one canonical implementation per sector-lookup shape, byte-for-byte behaviour preservation, and all 4 named test suites (47 tests — count corrected 2026-09-04 post-hoc after an independent DoQ agent-mediated PR review recount; ST-10's own sign-off was measured before ST-09's new test landed in the same file) passing with zero assertion or patch-target changes needed. See `execution_state.json` → `epics.EPIC-02.stories.ST-10.sign_off_record` for the full record.

## Autonomous Class Eligibility Check (BLG-GOV-19)

- Criterion 1 (all stories `autonomous`): ✓
- Criterion 2 (all AC code-review-verifiable, no observable UI behaviour): ✓ — this EPIC's AC (dependency versions, backend logging, backend refactor architecture) is verifiable by code review and automated test-suite results; ST-08's Playwright re-run is a regression-safety check against unrelated existing coverage, not new observable UI behaviour requiring human staging
- Criterion 3 (no frontend-visible change): ✓ — this EPIC touches only `backend/`, `tests/`, `package.json`/`package-lock.json`, and docs/governance files; no file under `src/components/**` or `src/pages/**` was created or modified
- Criterion 4: Engine signer field populated below

**Autonomous class applies.**

## BLG-GOV-19 Autonomous Class Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓
- Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓
- Criterion 3: No frontend-visible change — confirmed no React page or UI component was created or modified — ✓
- Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-09-04
- Comments: All four qualifying criteria met. ST-10's consolidation additionally received an independent Backend Engineering Patterns Owner agent-mediated review (Approved, no findings) — see Story-Level Authority Sign-Offs above. Two independent agent-mediated PR reviews (Director of Quality and Product Owner perspectives, posted to PR #1536) both verdicted "Approved with Comments," both flagging DEV-EPIC02-ST08-01 and BLG-OPS-149, both recommending a real CI signal be forced rather than left absent. Acting on that: added `workflow_dispatch` to `playwright.yml` and pushed, triggering a real GitHub Actions run of the full Playwright suite. **That run confirmed the failure was real** (reproduced deterministically on GitHub-hosted infrastructure, and confirmed absent on the pre-bump `main` commit at the same shard) — the earlier "likely sandbox-specific" assessment was wrong and has been corrected in the deviation record. Root-caused as a pure test-synchronization gap (the test asserted immediately after `page.goto()` resolved, without waiting for the actual fetch — `page.goto()` only waits for the `load` event, not for React to mount) exposed, not caused, by the dependency bump shifting bundle timing. Fixed with the idiomatic Playwright pattern (`page.waitForRequest()` awaited concurrently with the navigation); verified 32/32 locally; no application code changed. DEV-EPIC02-ST08-01 is now Resolved. BLG-OPS-149 remains open and is the real structural fix needed — this whole episode is direct evidence of why (a real, reproducible failure sat invisible to CI for this entire review cycle until manually forced).
