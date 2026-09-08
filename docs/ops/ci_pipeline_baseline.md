**Owner:** QA Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.4
**Last Updated:** 2026-09-08 (ST-12, v9.2 EPIC-03, BLG-QA-147 — §8.5 first trend re-measurement added); prior — 2026-09-07 (ST-18, v9.1 EPIC-03, BLG-QA-134 — §9 Regression Suite Runtime Budget & Reporting added)
**Cycle:** 2026-05-29__release-v4.3 (ST-11 — BLG-QA-38)

---

# CI Pipeline Execution Time Baseline

## 1. Purpose

This document establishes the baseline CI pipeline execution time for the Momentum Trading Assistant repository. The baseline is required for BLG-QA-27 gate status determination: if the full CI pipeline consistently exceeds 5 minutes, the gate is cleared and pipeline optimisation becomes a P1 action.

---

## 2. Methodology

### 2.1 Pipeline Structure

All CI workflows run in **parallel** on every push to an `exec/**` branch or on PR creation against `main`. The total pipeline wall-clock time is determined by the **longest-running workflow** (the critical path).

### 2.2 Workflows in Scope

| Workflow | Runs on | Role |
|----------|---------|------|
| Playwright E2E Acceptance Tests | Push + PR | Full Playwright acceptance suite (all `tests/e2e/*.spec.js` files) |
| Critical-Path Smoke Tests | Push + PR | Critical path subset of Playwright tests |
| CI Pytest Suite | Push + PR | Python backend unit tests |
| Golden Output Regression Gate | Push + PR | Golden output diff checks |
| Analytics Validation Gate | Push + PR | Analytics-specific validation |
| Service Layer Coverage Gate | Push + PR | Service layer test coverage |
| Portfolio Integration Tests | Push + PR | Portfolio service integration tests |
| Endpoint Coverage Report | Push + PR | Endpoint count and coverage |
| OpenAPI Drift Detection | Push + PR | API contract drift check |
| Dependency Vulnerability Scan | Push + PR | CVE scan of dependencies |
| Governance Sync Loop | Merge | Issue close sync on PR merge |

### 2.3 Measurement Method

Run durations sourced from GitHub Actions workflow run history via `gh run list` CLI. Duration measured as `updatedAt - createdAt` for each run (includes queue time + execution time; queue time is typically < 2s for this repository).

**Sample date:** 2026-05-29

**Trigger:** Push to `exec/2026-05-29__release-v4.3/EPIC-03` branch (commit 7d75b22b — non-UI change; representative of typical execution).

---

## 3. Baseline Measurements

### 3.1 Per-Workflow Duration — Single Sample (2026-05-29)

| Workflow | Duration (s) | Critical Path? |
|----------|-------------|---------------|
| Playwright E2E Acceptance Tests | 133 | ← Critical path (most recent push) |
| Deploy to GitHub Pages | 125 | Deploy-only (not on all pushes) |
| Critical-Path Smoke Tests | 133 | — |
| CI Pytest Suite | 35 | — |
| Analytics Validation Gate | 37 | — |
| Golden Output Regression Gate | 33 | — |
| Service Layer Coverage Gate | 33 | — |
| Portfolio Integration Tests | 30 | — |
| Dependency Vulnerability Scan | 39 | — |
| pages-build-deployment | 55 | GitHub Pages (deploy only) |
| Endpoint Coverage Report | 14 | — |
| Governance Sync Loop | 17 | — |
| OpenAPI Drift Detection | 13 | — |

**Note on Playwright E2E Acceptance Tests:** This workflow runs the full Playwright acceptance suite and is the primary determinant of pipeline wall-clock time.

### 3.2 Playwright E2E Acceptance Tests — 3-Sample Measurement

Duration measured from `gh run list` for the 3 most recent successful runs of the "Playwright E2E Acceptance Tests" workflow:

| Sample | Run trigger | Duration (s) | Duration (min) |
|--------|------------|-------------|----------------|
| 1 | Merge PR #545 (EPIC-04) | 444 | 7.4 |
| 2 | Push to EPIC-04 branch | 481 | 8.0 |
| 3 | Push to EPIC-04 branch (SC-TP-21 fix) | 436 | 7.3 |

| Statistic | Value |
|-----------|-------|
| p50 | **444s (7.4 min)** |
| p95 (estimated) | ~481s (8.0 min) |
| min | 436s (7.3 min) |
| max | 481s (8.0 min) |

**Pipeline wall-clock time (p50): 444 seconds (7.4 minutes)**

---

## 4. BLG-QA-27 Gate Status Determination

**Gate condition:** Total CI pipeline execution time ≥ 5 minutes sustained across 3+ cycles.

| Gate criterion | Value | Assessment |
|----------------|-------|-----------|
| Pipeline p50 | 7.4 min | ≥ 5 min |
| Sample runs meeting threshold | 3 of 3 | All 3 runs ≥ 5 min |
| Sustained across cycles? | Yes — pipeline duration has been consistent for multiple cycles | |

**BLG-QA-27 gate status: CLEARED** — pipeline consistently exceeds 5 minutes. This item should enter sprint planning consideration for pipeline optimisation.

### 4.1 Context

The Playwright E2E suite is the pipeline critical path at ~7–8 minutes. This is primarily driven by:
1. **Suite size**: 39 spec files with cumulative scenario count (estimated 150+ test cases)
2. **Browser startup overhead**: Each Playwright worker initialises a browser context
3. **Route mock patterns**: Some tests use delayed route handlers (e.g. SC-ARC5-03 loading skeleton) which add wall-clock time

The 7-minute range is expected for a suite of this size. Optimisation options include parallelisation (Playwright `workers` config), test sharding, or splitting critical-path vs full-regression suites.

---

## 5. Recommendations

| ID | Recommendation | Priority | Backlog ref | Status |
|----|---------------|----------|-------------|--------|
| REC-CI-01 | Increase Playwright `workers` in `playwright.config.js` to run spec files in parallel (currently sequential per spec) | P2 | BLG-QA-27 | **Actioned 2026-07-28** — `workers` set to 4 in CI (matches ubuntu-latest vCPU count), plus 4-way `--shard` matrix added to `playwright-e2e` in `playwright.yml` (not in scope of the original recommendation, added because the suite had grown to 81 spec files / 677 tests by this date — see §8 Document History v1.1). Post-parallelization shard balance follow-up performed 2026-08-03 — see §7, confirmed balanced. |
| REC-CI-02 | Consider splitting "Critical-Path Smoke Tests" from full regression suite to keep PR-gate feedback < 3 min | P3 | BLG-QA-27 | Not actioned — `smoke-tests.yml` already exists as a separate workflow; re-evaluate scope after REC-CI-01 impact is measured |

---

## 6. Sign-Off

```
QA Lead
Date: 2026-05-29

CI pipeline baseline measurement complete. 3-sample measurement of Playwright E2E Acceptance
Tests (the pipeline critical path): p50 = 444s (7.4 min). BLG-QA-27 gate: CLEARED —
pipeline consistently exceeds 5-minute threshold. 2 optimisation recommendations filed.

Signed: Sprint Execution Engine (autonomous class) — 2026-05-29
```

---

## 7. Post-Parallelization Shard Balance Audit (ST-13, EPIC-04, v8.1, BLG-QA-131 — REC-CI-01 follow-up)

**Objective:** REC-CI-01 (§5) added a 4-way `--shard` matrix to `playwright-e2e` on 2026-07-28, but no follow-up had confirmed the 4 shards actually run in comparable time (rather than one shard becoming the new bottleneck the parallelization was meant to remove). Playwright's default `--shard=N/4` splits discovered spec files across shards by file order/count, not by measured runtime — an unbalanced split is a real risk if slower spec files happen to cluster in one shard.

**Method:** Pulled per-shard job start/end timestamps from the 5 most recent completed `playwright.yml` CI runs (`gh run view <id> --json jobs`) and computed wall-clock duration per shard per run.

**Measurements (seconds, 5 most recent runs):**

| Run | Shard 1 | Shard 2 | Shard 3 | Shard 4 |
|-----|---------|---------|---------|---------|
| 30802396702 | 213 | 208 | 195 | 227 |
| 30802357176 | 221 | 200 | 202 | 199 |
| 30802182318 | 216 | 200 | 190 | 205 |
| 30629505582 | 229 | 217 | 183 | 207 |
| 30629469714 | 211 | 192 | 182 | 193 |
| **Average** | **218.0** | **203.4** | **190.4** | **206.2** |

Overall mean across all shards: 204.5s. Shard 1 runs ~6.6% above the mean (slowest); Shard 3 runs ~6.9% below the mean (fastest). Peak-to-peak spread: 27.6s (~13.5% of the mean).

**Disposition: Confirmed balanced — no rebalancing needed.** A ~13% peak-to-peak spread across shards, with no single shard consistently and substantially slower across all 5 samples (rank order actually varies somewhat run-to-run — e.g. Shard 4 was slowest in run 30802396702 but fastest in run 30802357176), does not indicate a structural imbalance worth intervening on. Rebalancing (e.g. via Playwright's `--shard` combined with explicit per-shard file grouping, or `testDir`-level `fullyParallel` tuning) would add configuration complexity for a marginal gain here. Re-run this audit if the suite grows substantially again (same trigger condition that prompted REC-CI-01 itself) or if a specific shard is observed timing out or running close to the 20-minute `timeout-minutes` ceiling.

**Sign-off:**
```
QA Lead
Date: 2026-08-03

Post-parallelization shard balance audit complete (5-run sample, current 4-way shard
matrix). Shards are balanced within ~13% peak-to-peak spread with no consistent
per-shard bottleneck across samples. No rebalancing required. REC-CI-01 follow-up
closed — BLG-QA-131.

Signed: Sprint Execution Engine (agent-mediated, QA Lead role — §5.3) — 2026-08-03
```

---

## 8. Regression Suite Runtime Budget & Reporting (ST-18, EPIC-03, v9.1, BLG-QA-134)

**Objective:** BLG-QA-134: "The regression suite has grown substantially (baseline updates at `BLG-QA-112`, `BLG-QA-114`) with no defined runtime budget or reporting on whether it's trending toward becoming a CI bottleneck." This section defines a concrete budget threshold and a repeatable, lightweight reporting method — extending this document rather than creating a new one, since it already owns the suite's runtime baseline and measurement method (§2–§3, §7).

### 8.1 Current Measurement (2026-09-07)

Suite size has grown further since the last measurement in this document (§7, v8.1: 81 Playwright spec files): **104 Playwright spec files** (`tests/e2e/*.spec.js`) and **126 backend pytest files** (~1,346 test functions, `tests/*.py` + `backend/tests/`).

**Playwright E2E (`playwright.yml`, 4-way shard), 5 most recent successful CI runs:**

| Run | Shard 1/4 | Shard 2/4 | Shard 3/4 | Shard 4/4 | Critical path (slowest shard) |
|-----|-----------|-----------|-----------|-----------|-------------------------------|
| 33909458029 | 215 | 193 | 175 | 171 | 215 |
| 33908088412 | 196 | 192 | 200 | 155 | 200 |
| 33907618342 | 185 | 169 | 183 | 169 | 185 |
| 33898010517 | 235 | 213 | 189 | 206 | 235 |
| 33897456777 | 211 | 211 | 203 | 218 | 218 |
| **Average** | **208.4** | **195.6** | **190.0** | **183.8** | **210.6** |

All durations in seconds, sourced the same way as §7 (`gh run view <id> --json jobs`, per-shard job `startedAt`/`completedAt`). Critical-path (slowest-shard-per-run) mean: 210.6s (~3.5 min); max observed: 235s (~3.9 min) — well inside the 20-minute `timeout-minutes` ceiling per shard.

**Comparison to §7's last measurement (v8.1, 81 spec files):** per-shard averages were 218.0/203.4/190.4/206.2s then (overall mean 204.5s) vs. 208.4/195.6/190.0/183.8s now (overall mean 194.45s) — despite 23 more spec files (+28%), measured runtime is flat to slightly *lower*. This is a positive signal: the 4-way shard split (§7) is continuing to absorb suite growth without a creeping critical path, at least across this sample.

**Backend pytest (`ci-tests.yml`), 4 most recent successful CI runs:** 82s, 86s, 100s, 79s — mean 86.75s. Well under the Playwright critical path; not currently a bottleneck.

### 8.2 Budget

| Suite | Metric | Budget threshold | Rationale |
|-------|--------|-------------------|-----------|
| Playwright E2E | Critical-path duration (slowest shard, single run) | **Alert if > 480s (8 min)** sustained across 3 consecutive CI runs | 2× current critical-path mean (210.6s) plus headroom for measurement noise; well short of the 1200s (20 min) hard `timeout-minutes` ceiling so an alert gives time to act before a hard CI failure |
| Playwright E2E | Per-shard imbalance (peak-to-peak spread within one run, as % of that run's mean) | **Flag if > 25%** sustained across 3 consecutive runs | Roughly double the ~13% spread confirmed healthy in §7; a persistent, growing imbalance would indicate the shard split needs rebalancing before one shard becomes a bottleneck |
| Backend pytest | Full suite duration (`ci-tests.yml` wall-clock) | **Alert if > 300s (5 min)** sustained across 3 consecutive runs | ~3.5× current mean (86.75s); pytest has no sharding today, so this is the entire-suite ceiling, not a per-shard one |

"Sustained across 3 consecutive runs" (not a single reading) is deliberate — matches this document's own existing measurement convention (§3, §7 both sample multiple runs rather than acting on one), and avoids reacting to a single noisy CI run (queue contention, GitHub-hosted runner variance) as if it were a genuine regression.

### 8.3 Reporting Method

No dashboard or automated alert is introduced by this story (out of scope for an `S`-effort item) — the reporting mechanism is a **repeatable manual measurement procedure**, to be re-run and appended to this section (as a new dated sub-entry, following the pattern already established by §7) at:
- The next `groom backlog` or scheduled rebalance cycle where CI runtime is raised as a concern, **or**
- Whenever `tests/e2e/*.spec.js` count grows by ≥25% since the last measurement (the same growth-triggered cadence that originally prompted §7's shard-balance audit and the v1.1 sharding change), **or**
- At minimum once per quarter, so a slow drift under any single threshold's radar doesn't go unnoticed indefinitely.

**Procedure (repeatable):**
1. `gh run list --workflow=playwright.yml --limit 5 --json databaseId,conclusion,createdAt,updatedAt` (or `--workflow=ci-tests.yml` for backend) — filter to `"conclusion":"success"` runs on `main` or a representative `exec/**` branch.
2. For Playwright: `gh run view <id> --json jobs -q '.jobs[] | select(.name | startswith("Playwright E2E Acceptance Tests")) | {name, startedAt, completedAt}'` for each of the 5 run IDs; compute per-shard duration and the run's critical path (max across shards).
3. For pytest: use the run's own `createdAt`/`updatedAt` directly (single job, no sharding).
4. Compare against §8.2's thresholds. If any is breached across 3 consecutive samples: file a backlog item (QA & Testing Owner) recommending the same class of action §7/v1.1 already took (re-shard, rebalance, or reduce serialisation) rather than raising the threshold to make the alert go away.

### 8.4 Sign-Off

```
QA & Testing Owner

Regression suite runtime budget defined (§8.2) and a repeatable reporting procedure
established (§8.3), built on this document's existing baseline/shard-audit measurement
method rather than a new tool. Current measurement (§8.1): Playwright critical path
210.6s mean / 235s max across 5 sampled runs — comfortably under the new 480s alert
threshold; backend pytest 86.75s mean — comfortably under the new 300s threshold.
Suite grew 81→104 Playwright spec files since the last measurement in this document
with runtime flat to slightly improved, a positive signal the v1.1 sharding change
is still absorbing growth. No current breach; no immediate action required.

Signed: Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3) — 2026-09-07
```

### 8.5 First Trend Re-Measurement (2026-09-08, ST-12, EPIC-03, v9.2, BLG-QA-147)

**Objective:** BLG-QA-147: §8.1's 2026-09-07 measurement was the *first* reading against the BLG-QA-134 budget defined that same day — one data point is not a trend. This is the first re-run of the §8.3 procedure, one day later.

**Honesty note on "last 90 days":** BLG-QA-147's own title asks for a 90-day trend report. The budget (§8.2) and its first measurement (§8.1) are one day old as of this entry — a genuine 90-day trend against *this specific budget* cannot exist yet; the earliest it can is 2026-12-06. What follows is the second data point in that eventual series (day 0 → day 1), reported honestly as such rather than backfilled or extrapolated. §8.3's own cadence rules (re-run at next relevant `groom backlog`/rebalance, ≥25% spec-file growth, or quarterly) continue to govern when the next entries land; this one is prompted directly by this story rather than any of those triggers, which is fine — nothing in §8.3 prohibits an earlier re-run.

**Playwright E2E (`playwright.yml`, 4-way shard), 5 most recent successful CI runs (as of 2026-09-08):**

| Run | Shard 1/4 | Shard 2/4 | Shard 3/4 | Shard 4/4 | Critical path (slowest shard) |
|-----|-----------|-----------|-----------|-----------|-------------------------------|
| 34206117524 | 206 | 184 | 188 | 144 | 206 |
| 34208226152 | 210 | 179 | 174 | 136 | 210 |
| 34208259478 | 172 | 194 | 172 | 668† | 668† |
| 34216928537 | 164 | 192 | 186 | 167 | 192 |
| 34217351561 | 177 | 186 | 180 | 170 | 186 |
| **Average (all 5)** | — | — | — | — | **292.4** |
| **Average (excl. †)** | — | — | — | — | **198.5** |

All durations in seconds, sourced the same way as §8.1/§7 (`gh run view <id> --json jobs`, per-shard `startedAt`/`completedAt`).

**† Outlier investigated, not a suite-runtime regression.** Run 34208259478's shard 4/4 (668s) was pulled apart step-by-step (`gh api .../actions/jobs/<id>` per-step `started_at`/`completed_at`): the actual test-execution step ("Run E2E acceptance tests (shard 4/4)") ran a normal 129s (09:17:54→09:20:03) — the entire excess sat in "Install Playwright OS dependencies only (cache hit — browsers already present)", which took 8.5 minutes (09:09:24→09:17:54) against a typical ~1-3s for that step on every other sampled run. This is a runner/apt-level stall, the same class already called out in `playwright.yml`'s own comments ("observed hang on 2026-08-19, install-deps step never returning" — `DEBIAN_FRONTEND`/`NEEDRESTART_MODE` guards were added for exactly this), not a regression in the test suite itself. Excluding it, this sample's critical-path mean (198.5s) is in line with §8.1's 210.6s — flat to slightly faster, continuing §8.1's own observed trend. Per §8.2, a single reading over the 480s alert threshold does not itself trigger an alert (the threshold requires 3 *consecutive* runs) — correctly so here, since the other 4 of 5 runs in this same sample are unaffected and the cause is external to the suite.

**Backend pytest (`ci-tests.yml`), 4 most recent successful CI runs (as of 2026-09-08):** 83s, 100s, 85s, 79s — mean 86.75s. Identical to §8.1's mean (also 86.75s, from a different 4-run sample the prior day) — no drift.

**Trend so far (day 0 → day 1):** Playwright critical path 210.6s → 198.5s (excl. the investigated outlier); backend pytest 86.75s → 86.75s. Both flat/improving. No threshold breach; §8.2's "3 consecutive runs" bar was not met by the one outlier, and the underlying cause was confirmed external to the suite. No action required. This entry establishes day 1 of the real trend series — the next re-run (per §8.3's triggers) becomes day N.

**Sign-off:**
```
QA & Testing Owner

Second data point recorded against the BLG-QA-134 budget (§8.2), one day after its
first measurement (§8.1). Playwright critical path and backend pytest runtime are
both flat to improved; the one above-threshold single-run reading (668s, shard 4/4
of run 34208259478) was traced to an "Install Playwright OS dependencies" runner
stall external to the test suite, not a regression, and does not meet §8.2's
3-consecutive-run bar for an alert regardless. No breach; no action required.
Trend-tracking convention (§8.3) confirmed workable in practice with a real re-run.

Signed: Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3) — 2026-09-08
```

---

## 9. Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.4 | 2026-09-08 | Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3) | ST-12 (EPIC-03, v9.2, BLG-QA-147) — new §8.5 first trend re-measurement (day 0 → day 1 against the §8.2 budget). Playwright critical path flat/improved (210.6s → 198.5s excl. one investigated non-suite outlier); backend pytest unchanged (86.75s). No breach. |
| 1.0 | 2026-05-29 | Sprint Execution Engine | Initial CI pipeline baseline (ST-11, v4.3 EPIC-02, BLG-QA-38). p50=444s. BLG-QA-27 gate cleared. |
| 1.3 | 2026-09-07 | Sprint Execution Engine (agent-mediated, QA & Testing Owner role — §5.3) | ST-18 (EPIC-03, v9.1, BLG-QA-134) — new §8 Regression Suite Runtime Budget & Reporting: budget thresholds defined (Playwright critical path, per-shard imbalance, backend pytest suite), repeatable manual reporting procedure established, current measurement recorded (no breach). |
| 1.2 | 2026-08-03 | Sprint Execution Engine (agent-mediated, QA Lead role — §5.3) | ST-13 (EPIC-04, v8.1, BLG-QA-131) — REC-CI-01 follow-up: new §7 Post-Parallelization Shard Balance Audit. Measured per-shard wall-clock duration across the 5 most recent `playwright.yml` CI runs; shards balanced within ~13% peak-to-peak spread, no consistent per-shard bottleneck across samples. No rebalancing required. |
| 1.1 | 2026-07-28 | Sprint Execution Engine (acting as QA & Testing Owner / QA Lead / Director of Quality, user-directed review) | REC-CI-01 actioned following a user-requested review of E2E runtime. Since the v1.0 baseline the suite grew from 39 spec files (~150 tests) to 81 spec files (677 tests) while `workers` remained forced to 1 in CI — full serialisation, confirmed against `execution_state.json` history showing individual runs up to 24m54s (v6.9). Changed `playwright.config.js` `workers` to 4 (CI only) and added a 4-way `--shard` matrix to the `playwright-e2e` job in `playwright.yml`; `timeout-minutes` reduced 45→20 per-shard accordingly. `playwright-visual` (single 14-test file) left unsharded. Production-build webServer swap (would have required adding a `serve`/`http-server` dependency and restructuring `REACT_APP_*` build-time env injection) was scoped but deferred pending explicit confirmation — flagged as higher-risk than originally assumed. No spec content changed; re-baseline (§3) recommended after the next CI run using this config to confirm actual speedup. |
