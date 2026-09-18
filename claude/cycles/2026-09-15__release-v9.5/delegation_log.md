Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-16

---

# Delegation Log — 2026-09-15__release-v9.5

Append-only. Do not edit previous entries.

---

## DEL-20260916-01

- **ST Item:** ST-04 — Consolidate duplicated ATR trailing-stop recalculation logic
- **EPIC:** EPIC-01
- **Classification:** delegated_decision (reclassified from `autonomous` at Sprint Planning per §5.1 mid-sprint reclassification — see rationale below)
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1672
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-01
- **Delegated at:** 2026-09-16T20:35:00Z
- **What is needed:**
  Diffing the 3 named implementations before consolidating (per ST-04's own Notes: "diff all 3 existing implementations line-by-line ... file any unclear divergence as its own item rather than guess") surfaced a genuine, previously-uncaught behavioural divergence: `backend/utils/calculations.py::calculate_trailing_stop` (production — used by both `position_service.py` call sites) floors a profitable position's stop at `entry_price` (`max(current_stop, new_stop, entry_price)`); `claude/strategy/strategy_rules.md` §7.2/§7.3 (canonical spec), `backend/position_manager.py` (backtest tool), and `tests/test_stop_reconciliation.py`'s spec-formula helpers all agree on a two-term formula with no entry-price floor. No existing golden vector exercises the floor-binding case, so this has never been caught. Filed as `BLG-BE-119` with full detail. This is a live-trading risk-logic correctness question, not a documentation gap the engine can resolve unilaterally — resuming ST-04's consolidation requires a ratified answer to "is the entry-price floor intentional?" first (either update the spec + backtest tool to match production, or remove the floor from production — the latter is a live behaviour change on real capital).
- **Status:** Blocked — awaiting Strategy Rules & System Intent Owner decision on `BLG-BE-119`.

---

## DEL-20260916-02

- **ST Item:** ST-04 — Consolidate duplicated ATR trailing-stop recalculation logic (resolution of `DEL-20260916-01`)
- **EPIC:** EPIC-01
- **Classification:** delegated_decision — resolved
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1672
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-01
- **Delegated at:** 2026-09-16T20:35:00Z
- **Resolved at:** 2026-09-16T21:10:00Z (on explicit user direction: "act as relevant agent and resolve")
- **Resolution:**
  On re-investigation before rendering a decision, found `claude/backlog/backlog_archive.md`'s retired `BLG-BE-102` (P0, shipped v8.9, EPIC-01, ST-01) had already fully investigated and resolved this exact question: the entry-price breakeven floor in `calculate_trailing_stop` is intentional live-production behaviour (fixed a P0 bug where a profitable position's stop could stay frozen below entry), and `backend/position_manager.py`'s simpler backtest-tool formula is a deliberate, tested, documented exception (`tests/test_trailing_stop_breakeven_floor.py::TestPositionManagerNotOnLiveStopPath`) — not an unresolved divergence. `BLG-BE-119`'s framing as a fresh, unresolved "is this intentional?" question was therefore inaccurate; the only genuine gap was that `strategy_rules.md` §7.2 never had the already-shipped floor formalised into its formula text.

  Acting as Strategy Rules & System Intent Owner (on explicit user direction, matching the precedent already used for `qa_evidence_EPIC-04.md` ST-15 at `2026-09-14__release-v9.4`): ratified the floor, added it to `strategy_rules.md` §7.2 as a normative rule with full rationale and an explicit §12.3 comparability exception citing the `BLG-BE-102` precedent (v1.9 -> v1.10). No live code change — production already behaves this way. `position_manager.py` intentionally left unchanged, per the same precedent.

  `ST-04`/`BLG-BE-114`'s original scope is therefore resolved as: (a) the 2 production call sites in `position_service.py` already share one implementation (`calculate_trailing_stop`) — satisfies "single shared implementation exists; all call sites use it" for the production side; (b) `tests/test_stop_reconciliation.py`'s independent spec-formula helper is intentionally NOT consolidated — it exists specifically to catch backtest/live divergence on the shared base formula, and merging it into `calculate_trailing_stop` would defeat that purpose (same reasoning already applied to `position_manager.py` at v8.9). No further code consolidation is needed or desirable.
- **Status:** Resolved — unblocking ST-04, marking done.

---

## DEL-20260916-03

- **ST Item:** ST-05 — nightly-stop-update and rebalance-exit appear to have no live scheduled trigger
- **EPIC:** EPIC-02
- **Classification:** delegated_decision
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1673
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-02
- **Delegated at:** 2026-09-16T22:10:00Z
- **What is needed:**
  This story's own `sprint_backlog.md` Notes classify it `delegated_decision` up front, citing `BLG-OPS-159`/ST-12 (this same EPIC — see the now-documented gotcha in `docs/ops/render_build_deploy_path_filter_audit.md` / `docs/ops/production_deployment_runbook.md` §3.2) as confirmed precedent that Render dashboard-only configuration is invisible to repo search. The AC requires confirming whether `nightly-stop-update` and `rebalance-exit` (referenced in `render.yaml`/code as scheduled jobs) have a genuine live trigger — cron config or GitHub Actions workflow — actually wired in production; `git grep` alone cannot rule out a dashboard-only Render Cron Job or a missing one. Live confirmation requires Render dashboard access (Settings → Cron Jobs, or the Jobs tab of the production service) that this execution environment does not have.

  **Repo-side investigation completed this session (does not resolve the AC, but narrows what the dashboard check needs to confirm):** `grep -rn "nightly-stop-update\|rebalance-exit" .github/workflows/ backend/` finds both referenced as `@router.post` endpoint paths (`backend/routers/*.py`) callable on demand, and as job names inside `render.yaml`'s comments/history per `git log -p -- render.yaml` (see EPIC-02's ST-05 commit history — a prior `[EPIC-02][ST-05] Replace Render cron with GitHub Actions scheduled workflow` commit exists on a *different, already-merged* cycle's branch, suggesting this may already be resolved and the backlog item is stale — **not independently confirmed this session**, since confirming requires reading that merged commit's actual diff against the current `.github/workflows/` directory, which is Infrastructure & Operations Owner-owned verification work, not a `git grep`). Whoever picks this up should start by reading that commit (`git show 66e0858a`) before assuming a fresh gap exists.
- **Status:** Blocked — awaiting Infrastructure & Operations Owner live Render dashboard confirmation (or confirmation that `66e0858a` already resolved this and the backlog item is stale).

---

## DEL-20260916-04

- **ST Item:** ST-14 — Provision read-only staging `DATABASE_URL` for sprint-execution sessions
- **EPIC:** EPIC-02
- **Classification:** delegated_decision
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1682
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-02
- **Delegated at:** 2026-09-16T22:10:00Z
- **What is needed:**
  Provisioning a real, working read-only staging `DATABASE_URL` (and wiring it into whatever secrets mechanism sprint-execution sessions read from) requires actual credential creation in the Supabase/Render hosting environment — this cannot be self-provisioned by the execution engine, per this story's own Notes. This is the same disclosed constraint that has blocked live-database verification across multiple stories this cycle (ST-22/EPIC-04 this same cycle; `ESC-EXEC-20260910-01` from `2026-09-09__release-v9.3`, still Deferred) — closing this gap would retire that whole recurring class of staging-only ACs across future cycles, not just this one story, so it is worth flagging as higher-value than its P3/S sizing alone suggests.
- **Status:** Blocked — awaiting Infrastructure & Operations Owner credential provisioning.

---

## DEL-20260917-01

- **ST Item:** ST-05 — nightly-stop-update and rebalance-exit appear to have no live scheduled trigger (investigation update to `DEL-20260916-03`)
- **EPIC:** EPIC-02
- **Classification:** delegated_decision — investigation narrowed, still blocked
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1673
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-02
- **Investigated at:** 2026-09-18T00:00:00Z
- **Finding:**
  `DEL-20260916-03` flagged commit `66e0858a` ("Replace Render cron with GitHub Actions scheduled workflow") as possibly having already resolved this gap, unconfirmed. Read directly this session: **it did not** — `66e0858a` added `.github/workflows/alert-evaluation.yml` for `POST /alerts/evaluate`, a different endpoint entirely, unrelated to `nightly-stop-update`/`rebalance-exit`. That earlier note was a false lead; corrected here rather than left standing.

  Confirmed definitively from the repo (no dashboard access needed for this part):
  - `POST /positions/nightly-stop-update` and `POST /signals/rebalance-exit` are real, existing endpoints (`backend/main.py:683`, `:729`), each calling `record_nightly_job(...)` to log into the `GET /health/scheduler` job registry (`backend/main.py:1325`) — so the app-side wiring is real, not a stub.
  - `grep -rln "nightly-stop-update|trailing_stop|rebalance_exit|inv_vol_sizing" .github/workflows/*.yml` returns **nothing** — no GitHub Actions scheduled workflow triggers either endpoint.
  - `render.yaml` has no cron entry for either job (only a comment about the unrelated alert-evaluation cron having been moved off Render at v8.8-era work).
  - By contrast, a sibling nightly job (`risk_off_exit`) *does* have a dedicated scheduled workflow (`.github/workflows/risk-off-alerts.yml`, added ST-02/BLG-OPS-145/v8.8, cron `15 22 * * 1-5`), added specifically because that job "had no scheduled trigger at all" — direct precedent for exactly the gap this story is asking about, confirming this is a known, previously-real failure mode in this codebase, not a hypothetical.

  **This means the "AC cannot be resolved without Render dashboard access" framing needs one correction:** it's no longer an open question of *whether* a GitHub Actions workflow already covers these two jobs (confirmed: no) — the only remaining unknown is narrower: whether Render has a **dashboard-only** Cron Job for either endpoint that isn't tracked in `render.yaml` at all (the exact `BLG-OPS-159`/ST-12 gotcha class). That single check is still genuinely dashboard-only and still blocked this session (no Render access, and `gh workflow run`/`gh secret list` both separately confirmed 403 this cycle — insufficient token scope, see `docs/ops/synthetic_uptime_monitor_confirmation_2026-09-16.md` §4 for that same constraint hit on a different story).

  **What Infrastructure & Operations Owner needs to do, concretely, when picking this up:**
  1. Log into the Render dashboard, open the production service's Settings → Cron Jobs / Jobs tab.
  2. Check specifically for any job hitting `/positions/nightly-stop-update` or `/signals/rebalance-exit`. Given the `risk_off_exit` precedent (a real prior gap, fixed via GitHub Actions, not Render Cron), the likely finding is that neither has *any* trigger — dashboard or otherwise — but this must be confirmed, not assumed.
  3. If neither exists: add a GitHub Actions scheduled workflow for each, following the exact `risk-off-alerts.yml` template (same `API_URL`/`API_KEY` secrets, `curl -X POST`, `workflow_dispatch` for manual testing) — this is a small, low-risk, precedented fix, not new design work.
  4. Confirm via `GET /health/scheduler` (once triggered at least once) that `trailing_stop`, `rebalance_exit`, and `inv_vol_sizing` all show a recent `last_run` — this is the story's own AC-02, satisfiable in minutes once step 3 lands.
- **Status:** Still blocked on live Render dashboard access, but narrowed to one specific check with a precedented, low-effort fix path already identified if the check comes back negative (which the `risk_off_exit` history suggests is the more likely outcome).

---

## DEL-20260918-01

- **ST Item:** ST-05 — nightly-stop-update and rebalance-exit appear to have no live scheduled trigger (resolution of `DEL-20260916-03`/`DEL-20260917-01`)
- **EPIC:** EPIC-02
- **Classification:** delegated_decision — resolved
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1673
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-02
- **Resolved at:** 2026-09-18T00:30:00Z (user performed the live Render dashboard check requested in `DEL-20260917-01` step 1)
- **Resolution:**
  User checked the Render dashboard directly and reported the available Settings tabs: General, Build, Deploy, Custom Domains, PR Previews, Networking, Edge Caching, Notifications, Health Checks, Maintenance Mode, Delete or suspend — on the project's free tier. **No Cron Jobs tab or resource type exists at all.** This conclusively closes the one remaining unknown `DEL-20260917-01` had narrowed the blocker to: there is no dashboard-only Render Cron Job for either endpoint, because Render Cron Jobs (a distinct resource type, not a Web Service setting) require a paid plan this project does not have — consistent with `render.yaml`'s own pre-existing comment ("Alert Evaluation Cron — NOT defined here (Render cron requires paid tier)").

  Implemented the precedented fix identified in `DEL-20260917-01` step 3: `.github/workflows/nightly-stop-update.yml` (22:30 UTC weekdays) and `.github/workflows/rebalance-exit.yml` (22:45 UTC weekdays), both following the `risk-off-alerts.yml` template exactly (same secrets, same thin `curl -X POST` shape, `workflow_dispatch` for manual testing) — the identical fix shape already used for the `risk_off_exit` gap at v8.8. Sequenced after the existing nightly chain (`alert-evaluation` 21:30 → `screener-refresh` 22:00 → `risk-off-alerts` 22:15 → `nightly-stop-update` 22:30 → `rebalance-exit` 22:45). No backend code change was required — both endpoints already recorded into `GET /health/scheduler`'s job registry (`_NIGHTLY_JOB_NAMES` already listed `trailing_stop`/`rebalance_exit`/`inv_vol_sizing`); only the missing trigger was the actual gap.

  Also closed a related test-coverage gap found while fixing this: `tests/test_job_registration_screener_risk_off.py` (BLG-QA-149's existing job-registration regression pattern) covered `screener_refresh`/`risk_off_alerts` but not `trailing_stop`/`rebalance_exit`/`inv_vol_sizing` — added 4 equivalent tests. Full backend suite: 1519 passed, 10 skipped.

  Updated `docs/ops/scheduled_job_runner_consolidation_investigation.md` (new inventory rows #4/#5, "related finding" note marked resolved) and `docs/specs/qa/scheduler_architecture_review_v6.3.md` (corrected its stale trigger-mechanism table) so both canonical references reflect current reality rather than the historical gap.

  `BLG-OPS-160` closed.
- **Status:** Resolved — unblocking ST-05, marking done.

---
