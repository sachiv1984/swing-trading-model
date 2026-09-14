**Owner:** QA & Testing Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-09-09
**Source:** ST-09 (BLG-QA-91, EPIC-02, v9.3 sprint execution)

---

# Cross-Browser Playwright Matrix Evaluation

## Purpose

ST-09's acceptance criteria: evaluate the cost/benefit of adding Firefox/WebKit to the CI matrix for a small set of critical-path specs, and document a recommendation (adopt/defer, with rationale).

## Method

1. Installed Firefox 153.0 and WebKit 26.5 browser binaries + OS-level dependencies locally (`npx playwright install firefox webkit` + `install-deps`) — neither ships in this environment by default; only Chromium (the sole configured project in `playwright.config.js`) is present.
2. Selected 2 critical-path specs as the "small set" (24 combined scenarios, 18 test cases total — see below): `tests/e2e/signal-card.spec.js` (Signals page — the app's primary trading-workflow entry point, consolidated this same sprint per ST-05) and `tests/e2e/watchlist.spec.js` (Watchlist page — the other core daily-use page).
3. Ran the same 18 tests against Chromium (baseline, already CI-standard) and, via a throwaway local-only config (not committed — mirrors `playwright.config.js`'s `testDir`/`use`/`webServer` settings), against Firefox and WebKit, measuring pass/fail and wall-clock time.

## Results

| Browser | Tests run | Pass | Fail | Wall-clock time |
|---------|-----------|------|------|-----------------|
| Chromium (existing CI baseline) | 18 | 18 | 0 | 50.4s |
| Firefox | 18 | 18 | 0 | included in combined run below |
| WebKit | 18 | 18 | 0 | included in combined run below |
| Firefox + WebKit combined (1 worker, sequential) | 36 | 36 | 0 | 120.0s (≈60s/browser) |

**Zero cross-browser-specific failures found.** Every scenario that passes on Chromium — SignalCard rendering (watchlist CTA, cash balance, allocation-insufficient badge) and Watchlist page rendering (entry display, news toggle, Add Ticker modal, validation error text/colour, dialog colour cascade) — also passes identically on Firefox and WebKit.

## Cost/Benefit Analysis

**Cost:**
- Per-browser wall-clock time for this 18-test sample is comparable across all 3 engines (~50-60s each) — no browser is dramatically slower.
- Extrapolated to the full suite (102 spec files as of this review — see `BLG-QA-167` for the exact current count vs. the stale count in `playwright_coverage_matrix.md`): `docs/ops/ci_pipeline_baseline.md` §3.1 records the Playwright E2E Acceptance Tests workflow as the CI critical path at ~133s (Chromium only, 4 parallel workers on GitHub-hosted `ubuntu-latest` runners — `workers: process.env.CI ? 4 : undefined` in `playwright.config.js`). Adding 2 more browsers without adding proportional runner parallelism would scale this critical-path workflow toward **~3×** its current duration, since GitHub-hosted public-repo runners are already at the 4-vCPU ceiling this repo's worker count is tuned to.
- Browser binaries (Firefox + WebKit, ~200MB combined) must be installed in every CI run (`npx playwright install`), adding fixed per-run setup time on top of the multiplied test time.

**Benefit:**
- This evaluation found 0 cross-browser-specific bugs in a real run against 2 critical-path specs.
- No historical precedent exists in this repo's changelog/backlog of a bug ever being caught specifically by a non-Chromium browser (a keyword search of `docs/product/changelog.md` and `claude/backlog/backlog_archive.md` for "firefox"/"webkit"/"safari" cross-browser bug reports returned nothing).
- The suite's assertion style is already cross-browser-friendly: `playwright.config.js`'s own comments note this repo deliberately moved away from pixel-snapshot testing (`visual-snapshots.spec.js`'s header: "Chromium version differences cause pixel mismatches") toward CSS class/attribute assertions specifically because pixel-level rendering already varies across environments — meaning the existing test style already targets browser-agnostic DOM/CSS state rather than pixel-exact rendering, which is precisely the category of bug a second rendering engine is best at catching. This partially reduces (does not eliminate) the marginal value of adding real cross-browser coverage on top.
- No user-analytics/telemetry data on real-world non-Chromium browser usage share exists for this app to weight the benefit side further (same gap already flagged elsewhere for endpoint-traffic ranking, `docs/testing/pilot_contract_test_approach.md` §Priority Candidates) — so benefit is judged from this evaluation's direct evidence alone, not usage data.

## Recommendation: **Defer**

Adding Firefox/WebKit to the CI matrix is not recommended at this time. Rationale: the demonstrated cost (~3× the CI critical path, a workflow already identified in `ci_pipeline_baseline.md` as the pipeline's bottleneck) is not justified by demonstrated risk — this evaluation's own direct test run found zero cross-browser-specific failures, there is no historical precedent of a cross-browser bug in this app, and the suite's assertion style is already inherently more portable than a pixel-based suite would be.

**Revisit if:**
- A real user-reported bug is ever traced to non-Chromium rendering/behaviour (the single highest-signal trigger — direct evidence beats this evaluation's necessarily-small sample).
- CI runner capacity increases (e.g., a paid runner tier, or GitHub Actions matrix parallelism across more concurrent jobs) such that adding 2 browsers no longer extends the critical path.
- The frontend adopts any browser-specific API or CSS feature with known cross-engine behaviour differences (none currently in use, per this review).

## Acceptance

- Evaluated by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — a cost/benefit evaluation deliverable, no observable UI behaviour change)
- Date: 2026-09-09
