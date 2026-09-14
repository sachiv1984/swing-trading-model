**Owner:** Head of Engineering
**Class:** Reference Document (Class 2)
**Status:** Published
**Version:** 1.0
**Last Updated:** 2026-09-14 (ST-05, EPIC-01, v9.4, BLG-TECH-20 — investigation created)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Story:** ST-05 (EPIC-01, v9.4) — `BLG-TECH-20`

---

# Scheduled Job Runner Consolidation — Investigation

Spec-only investigation per `BLG-TECH-20`. No migration performed this cycle.

## 1. Purpose

`BLG-TECH-20` names 3 separate scheduled-job runners ("nightly backtest rebalance, screener refresh / risk-off alerts, and a third minor job runner"), each with its own registration/wiring, and asks whether consolidating them onto one orchestrator is worth the migration cost. This document inventories the 3 runners and makes a recommendation.

## 2. Inventory

Scope note: this repo has ~15 cron-scheduled GitHub Actions workflows in total (`.github/workflows/*.yml`), most of which are ops/CI maintenance jobs (dependency scanning, DB backup, staleness/drift checks) rather than trading-strategy job runners. The 3 in scope here are the ones `BLG-TECH-20`'s own title names — the trading-strategy-facing nightly runners.

| # | Runner | Workflow file | Schedule (UTC) | Architecture | Job-registry tracked? |
|---|--------|---------------|-----------------|---------------|------------------------|
| 1 | Nightly Backtest | `backtest.yml` | `0 1 * * *` (daily) | Heavy compute **in CI**: runs `production_strategy.py` on the runner, then pushes results via `import_backtest.py` against the live API. Has its own data-integrity smoke test and Telegram failure alert built in. | No — not registered via `record_nightly_job`/`GET /health/scheduler`; has its own independent alerting instead |
| 2 | Screener Refresh | `screener-refresh.yml` | `0 22 * * 1-5` (weekdays) | Thin trigger: `curl -X POST ${API_URL}/screener/run`. All compute happens API-side. | Yes — `record_nightly_job("screener_refresh", ...)` in `backend/routers/screener.py` |
| 3 | Risk-Off Alerts | `risk-off-alerts.yml` | `15 22 * * 1-5` (weekdays, 15 min after #2) | Thin trigger: `curl -X POST ${API_URL}/positions/risk-off-alerts`. All compute happens API-side. | Yes — `record_nightly_job("risk_off_alerts", ...)` in `backend/main.py` |

Adjacent but explicitly out of this inventory's scope (not named in `BLG-TECH-20`'s title, and structurally different — general portfolio maintenance / alerting rather than one of the "3" named runners): `alert-evaluation.yml` (`POST /alerts/evaluate`), `daily-snapshot.yml` (position analyze / portfolio snapshot / signal generation / audit-log purge, 4 steps in one workflow).

**Related finding, filed separately (`BLG-OPS-160`, not this story's scope):** while tracing runner #1's trigger mechanism, `docs/specs/qa/scheduler_architecture_review_v6.3.md` was found to already document, as of v6.3 (2026-06-29), that two other job endpoints — `POST /positions/nightly-stop-update` and `POST /signals/rebalance-exit` — have **no live scheduled trigger at all**. Re-confirmed still true today via repo-wide search. This is a correctness gap, not a consolidation question, and is out of scope for this investigation; see `BLG-OPS-160` for the full finding and its Render-dashboard-config caveat.

## 3. Trigger Mechanism Detail

All 3 runners in scope use the same base architecture: an external GitHub Actions `schedule:` cron trigger. None use an in-process scheduler (no APScheduler/Celery Beat) — this matches the finding already recorded in `scheduler_architecture_review_v6.3.md` §"Architecture type" for the wider job set. Where they differ:

- **Runner #1 (Backtest)** does its heavy computation in the CI runner itself and pushes results to the API afterward. It is architecturally the odd one out — the other two are pure "trigger an API-side job" calls with no CI-side computation.
- **Runners #2 and #3** are near-identical in shape (single `curl -X POST` step, no other logic) and are already deliberately sequenced 15 minutes apart in the same workflow family style.

## 4. Consolidation Cost/Benefit

**What consolidation onto one orchestrator would look like:** a single scheduled workflow (or a lightweight in-process scheduler if moved server-side) that sequences all 3 triggers, replacing 3 separate `on: schedule:` blocks with one.

**Benefit case (per `BLG-TECH-20`'s stated problem):** reduces the surface area for job-registration wiring gaps — each runner currently needs its own workflow file kept in sync with its endpoint, which is exactly the class of gap `BLG-QA-149` (v8.9) added test coverage for after one such gap was found and fixed, and which `BLG-OPS-160` (filed above) shows can still occur even with that test coverage in place, because the gap there is "never wired up" rather than "wiring broke."

**Cost case:**
- Runner #1's architecture (heavy compute in CI, own smoke test, own Telegram alerting) is not a natural fit for the same orchestrator shape as #2/#3's thin API triggers — consolidating would mean either forcing #1 into the thin-trigger shape (losing its in-CI compute model, a larger and riskier change than this story's scope) or running a heterogeneous orchestrator that still has 2 different execution shapes internally, which captures little of the simplification benefit.
- #2 and #3 are already a near-identical, already-sequenced pair — merging just these two into one workflow file would be a small, low-risk win, but it only removes 1 of 3 workflow files (not a full consolidation), and the current 15-minute stagger between them is itself a deliberate dependency ordering already working correctly.
- No incident to date has been caused by 3 separate files being out of sync with each other (as opposed to a file being out of sync with its endpoint, which is the `BLG-QA-149`/`BLG-OPS-160` class of gap — orthogonal to whether there are 1 or 3 files).

## 5. Recommendation

**Defer — not worth full consolidation at current scope.** Rationale:
1. Runner #1's heavy-compute-in-CI architecture is a poor structural fit for one orchestrator with #2/#3's thin-trigger shape; forcing it in would be a larger, separate migration with its own risk, not a byproduct of this story.
2. The actual wiring-gap risk `BLG-TECH-20` cites is already mitigated by job-registration test coverage (`BLG-QA-149`) for the 2 runners that use the registry pattern, and — as `BLG-OPS-160` demonstrates — the higher-risk failure mode in this codebase is a job never being wired up at all, which a consolidated orchestrator would not have prevented any more than 3 separate files did (the missing `daily-snapshot.yml` calls would have been just as easy to omit from a merged file).
3. At 3 runners, the wiring-surface-area argument is modest; the migration cost (re-architecting runner #1, re-testing all 3 schedules, updating `GET /health/scheduler`'s architecture assumptions) is not clearly justified by the benefit at this scale.

**Smaller, lower-cost alternative worth a future look (not this story's scope):** merging just runners #2 and #3 (the already-similar, already-sequenced pair) into one workflow file, since they share the same thin-trigger shape and are already logically paired. Not scoped or actioned here — spec-only per `BLG-TECH-20`'s own Notes field.

## 6. Sign-Off

**Head of Engineering:** Confirmed — inventory accurate against current `.github/workflows/*.yml` and `backend/` job-registration call sites; recommendation (defer full consolidation) and rationale reviewed. 2026-09-14 (agent-mediated, Head of Engineering role — §5.3).
