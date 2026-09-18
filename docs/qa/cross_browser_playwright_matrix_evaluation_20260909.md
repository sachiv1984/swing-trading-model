**Owner:** QA & Testing Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-09-16 (ST-19, BLG-QA-168, v9.5 — corrected stale pre-sharding CI baseline citation); prior — 2026-09-09 (ST-09, BLG-QA-91, v9.3, initial evaluation).
**Source:** ST-19 (BLG-QA-168, EPIC-03, v9.5 sprint execution — correction); ST-09 (BLG-QA-91, EPIC-02, v9.3 sprint execution — original)

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
- Extrapolated to the full suite (102 spec files as of this review — see `BLG-QA-167` for the exact current count vs. the stale count in `playwright_coverage_matrix.md`): **corrected (ST-19, BLG-QA-168, v9.5)** — the current CI critical path is `docs/ops/ci_pipeline_baseline.md` §9's 163.0s (8-way shard, 2-run sample, 2026-09-10), not §3.1's ~133s single-sample figure (2026-05-29, *before* sharding existed at all — the "4 parallel workers" framing originally attached to that number described `playwright.config.js`'s per-shard `workers` setting, which wasn't yet in effect for a pre-sharding measurement). Adding 2 more browsers without adding proportional runner parallelism would scale this critical-path workflow toward **~3×** its current duration (163.0s → ~489s, ≈8.2 min), since GitHub-hosted public-repo runners are already at the shard/worker configuration (8-way shard × 4 workers/shard) this repo is tuned to.
- Browser binaries (Firefox + WebKit, ~200MB combined) must be installed in every CI run (`npx playwright install`), adding fixed per-run setup time on top of the multiplied test time.

**Benefit:**
- This evaluation found 0 cross-browser-specific bugs in a real run against 2 critical-path specs.
- No historical precedent exists in this repo's changelog/backlog of a bug ever being caught specifically by a non-Chromium browser (a keyword search of `docs/product/changelog.md` and `claude/backlog/backlog_archive.md` for "firefox"/"webkit"/"safari" cross-browser bug reports returned nothing).
- The suite's assertion style is already cross-browser-friendly: `playwright.config.js`'s own comments note this repo deliberately moved away from pixel-snapshot testing (`visual-snapshots.spec.js`'s header: "Chromium version differences cause pixel mismatches") toward CSS class/attribute assertions specifically because pixel-level rendering already varies across environments — meaning the existing test style already targets browser-agnostic DOM/CSS state rather than pixel-exact rendering, which is precisely the category of bug a second rendering engine is best at catching. This partially reduces (does not eliminate) the marginal value of adding real cross-browser coverage on top.
- No user-analytics/telemetry data on real-world non-Chromium browser usage share exists for this app to weight the benefit side further (same gap already flagged elsewhere for endpoint-traffic ranking, `docs/testing/pilot_contract_test_approach.md` §Priority Candidates) — so benefit is judged from this evaluation's direct evidence alone, not usage data.

## Recommendation: **Defer**

Adding Firefox/WebKit to the CI matrix is not recommended at this time. Rationale: the demonstrated cost (~3× the CI critical path — 163.0s → ~489s against the current 8-way-shard baseline, corrected ST-19 — a workflow already identified in `ci_pipeline_baseline.md` as the pipeline's bottleneck) is not justified by demonstrated risk — this evaluation's own direct test run found zero cross-browser-specific failures, there is no historical precedent of a cross-browser bug in this app, and the suite's assertion style is already inherently more portable than a pixel-based suite would be. **This recommendation is unchanged by the ST-19 correction** — a higher current baseline strengthens, not weakens, the case against adding 2 more unsharded browsers.

**Revisit if:**
- A real user-reported bug is ever traced to non-Chromium rendering/behaviour (the single highest-signal trigger — direct evidence beats this evaluation's necessarily-small sample).
- CI runner capacity increases (e.g., a paid runner tier, or GitHub Actions matrix parallelism across more concurrent jobs) such that adding 2 browsers no longer extends the critical path.
- The frontend adopts any browser-specific API or CSS feature with known cross-engine behaviour differences (none currently in use, per this review).

## Acceptance

- Evaluated by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — a cost/benefit evaluation deliverable, no observable UI behaviour change)
- Date: 2026-09-09

## Correction (ST-19, BLG-QA-168, EPIC-03, v9.5)

- Corrected by: Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3)
- Date: 2026-09-16
- Comments: The Cost/Benefit and Recommendation sections cited `ci_pipeline_baseline.md` §3.1's pre-sharding 2026-05-29 single-sample figure (~133s), paired with a "4 parallel workers" framing that was not actually in effect for that pre-sharding measurement. Corrected to cite §9's current 163.0s (8-way shard, 2026-09-10) baseline — the most recent measurement in that document, superseding even §8.5's intermediate 198.5–210.6s (4-way shard) figure. The ~3× multiplier and the "Defer" recommendation are unchanged: a higher, correct current baseline strengthens rather than weakens the case against adding 2 more unsharded browsers. `BLG-QA-168` closed.
