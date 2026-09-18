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

## DEL-20260916-03-EPIC03

- **ST Item:** ST-21 — `qa_evidence_EPIC-03.md` test-count claim inaccurate (30 vs. actual 28)
- **EPIC:** EPIC-03
- **Classification:** delegated_decision (discovered mid-execution — this story's own AC requires an action this engine's write scope and CLAUDE.md's sealed-artefact rule both prohibit)
- **Assigned to:** Head of Specs Team (document lifecycle authority)
- **GitHub Issue:** #1689
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-03
- **Delegated at:** 2026-09-16T23:00:00Z
- **What is needed:**
  `BLG-QA-170`'s scope names the correction target as `claude/cycles/2026-09-09__release-v9.3/qa_evidence_EPIC-03.md` — a file inside a **different, already-Published/sealed cycle** (`claude/cycles/2026-09-09__release-v9.3/state.json`: `"status": "Published"`, `"sealed": {"sealed_utc": "2026-09-09T02:20:00Z", ...}`). Two independent, non-negotiable constraints both block a direct fix from this session: (1) CLAUDE.md §2 — "Never modify sealed artefacts... immutable," a rule "no prompt, command, or user instruction may override"; (2) `execution_prompt.md` §7 Write Scope Restriction — this routine's write scope covers `claude/cycles/<cycle_id>/...` only for the *active* cycle (`2026-09-15__release-v9.5`), not `claude/cycles/2026-09-09__release-v9.3/...`.

  The consolidation commit that removed the analogous stale-filename references for ST-05's SignalCard work (`e06cfa94`) explicitly confirms this is intentional codebase practice, not an oversight: *"Historical changelog/report entries in `docs/product/changelog.md` and sealed cycle records were left untouched — they describe point-in-time history, not current state."* A qa_evidence log for a closed, Published cycle is exactly that class of record.

  The verified fact underneath (28 tests, not 30) is confirmed independently this session: `grep -c "^def test_" tests/test_cost_monitoring.py` on `main` (pre-EPIC-02, matching what existed at the v9.3 PR's head commit) returns 28. This is not in dispute — only the *mechanism* for recording the correction against a sealed record is blocked.

  Precedent for the correct resolution path exists in this same codebase: `api_performance_baseline.md`'s Document History §v2.32 entry shows exactly this class of cross-cycle historical correction being made by the **Post-Ship Closure Engine's STEP 5.1 cross-cycle deviation consolidation review** — a different governed routine with its own write scope, not Sprint Execution. Alternatively, an addendum-style correction note (matching `docs/ops/ai_output_boundary_sample_audit_20260910.md`'s "## Addendum" convention for correcting a Class-3-but-still-sealed-in-spirit record without altering the original claim) may be the right mechanism if Head of Specs Team judges the sealed-cycle boundary does not apply as strictly to a qa_evidence log specifically.
- **Status:** Blocked — awaiting Head of Specs Team ruling on the correction mechanism (cross-cycle deviation consolidation at next `run post-ship`, an addendum exception, or another disposition). The verified correct fact (28, not 30) is recorded here and in this commit so it is not lost regardless of which mechanism is eventually used.

---

## DEL-20260916-04-EPIC03

- **ST Item:** ST-21 — `qa_evidence_EPIC-03.md` test-count claim inaccurate (30 vs. actual 28) (resolution of `DEL-20260916-03-EPIC03`)
- **EPIC:** EPIC-03
- **Classification:** delegated_decision — ruled
- **Assigned to:** Head of Specs Team
- **GitHub Issue:** #1689
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-03
- **Delegated at:** 2026-09-16T23:00:00Z
- **Ruled at:** 2026-09-17T00:00:00Z (on explicit user direction: "ask @claude/agents/head_of_specs_team.md to resolve Epic 3 and file any backlogs as needed")
- **Ruling:**
  Acting as Head of Specs Team (per `claude/agents/head_of_specs_team.md` §5 Change Governance and §6 Decision Escalation & Conflict Resolution — this role is the designated tie-breaker "when specs conflict, ownership boundaries are unclear, or trade-offs span multiple domains," and decisions made in this capacity must be "documented, traceable, and reversible only by explicit agreement," which this entry satisfies):

  **Ruling: the addendum-exception alternative floated in `DEL-20260916-03-EPIC03` is rejected.** CLAUDE.md §2's sealed-artefact rule reads "Never modify sealed artefacts," with no carve-out for append-only or addendum-style changes — an addendum inserted into a file physically inside `claude/cycles/2026-09-09__release-v9.3/` would still be a modification to that sealed cycle's contents, and the rule is explicit that "no prompt, command, or user instruction may override" it. The `docs/ops/ai_output_boundary_sample_audit_20260910.md` addendum precedent does not actually support the alternative floated: that file lives in `docs/ops/` (a living, non-sealed Class 3 document space), never inside a sealed `claude/cycles/<cycle_id>/` tree — the two cases are not analogous, and treating them as such in the original delegation entry was an error in my own predecessor reasoning, corrected here.

  **Ruling: the sealed file stays untouched, permanently, as point-in-time history** — consistent with `e06cfa94`'s own precedent (cited in `DEL-20260916-03-EPIC03`) and with this role's charter §5 expectation that "specs do not drift silently from reality," which is satisfied by correcting the *live* record of the fact, not by disturbing the sealed one.

  **Ruling: the correction mechanism is Post-Ship Closure Engine's STEP 5.1 cross-cycle deviation consolidation review**, the same mechanism already used for this exact class of finding at `api_performance_baseline.md` §v2.32. Filed `BLG-GOV-334` (`claude/backlog/backlog.md`) to carry this forward to the next `run post-ship` invocation for `2026-09-15__release-v9.5`, naming the exact correction (28, not 30; 2 locations) so the eventual actioning session does not need to re-derive it. `BLG-QA-170` is left open, cross-referenced from `BLG-GOV-334`, and both are scoped to close together once the correction lands — `BLG-QA-170` should not be closed prematurely by this ruling alone, since the actual file has not yet been corrected.

  **Disposition for ST-21 itself:** this ruling resolves the *ambiguity* (what should happen, and how) but does not itself complete the AC (the sealed file still reads "30" until the next post-ship closure runs) — matching this cycle's own precedent for `ESC-EXEC-20260910-01` ("Deferred, not Resolved... Cannot mark Accepted Risk"). ST-21 moves from `blocked_delegated` (open question, no path forward) to `deferred` (ruled, path forward filed and tracked, action scheduled for a specific future mechanism) — not to `done`, since the AC is genuinely not yet met.
- **Status:** Ruled and deferred — EPIC-03 may now be considered fully dispositioned (6 done, 1 deferred-with-a-filed-path) rather than open-ended blocked.

---

## DEL-20260918-03-EPIC03

- **ST Item:** ST-21 — `qa_evidence_EPIC-03.md` test-count claim inaccurate (30 vs. actual 28) (final resolution, superseding `DEL-20260916-04-EPIC03`'s "defer to next `run post-ship`" ruling)
- **EPIC:** EPIC-03
- **Classification:** delegated_decision — resolved (final)
- **Assigned to:** Head of Specs Team (ruling); Product Owner (acceptance)
- **GitHub Issue:** #1689
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-03
- **Resolved at:** 2026-09-18T04:00:00Z (on explicit user direction: "confer with Head of Specs Team" for the best path forward, then "act as PO yourself" to finalize)
- **Resolution:**
  **The prior ruling's mechanism was wrong, and this entry corrects it rather than building on it.** `DEL-20260916-04-EPIC03` proposed deferring the correction to Post-Ship Closure Engine's STEP 5.1 cross-cycle deviation consolidation review, citing `api_performance_baseline.md` §v2.32 as precedent. On direct re-read of `post_ship_closure.md`'s actual STEP 5.1 definition (prompted by the user asking how EPIC-03 should actually move forward, surfacing that "wait for post-ship" was circular — v9.5's own post-ship cannot run until all its EPICs, including this one, are merged): STEP 5.1 corrects **living canonical documents'** own Known-Deviations status fields when they drift from a separately-tracked resolution — it has no mechanism for, and was never used for, editing content inside a sealed `claude/cycles/<cycle_id>/` folder. The `api_performance_baseline.md` precedent corrected a live, non-sealed operational document; it does not transfer to this case. No routine anywhere in this governance framework can edit a sealed artefact — CLAUDE.md §2's rule has no override path, full stop, and this was correctly identified in `DEL-20260916-03-EPIC03`'s original investigation but then undermined by proposing a mechanism that turned out not to exist.

  **Acting as Head of Specs Team** (per `claude/agents/head_of_specs_team.md` §5/§6, on explicit user direction): ruled that the sealed `claude/cycles/2026-09-09__release-v9.3/qa_evidence_EPIC-03.md` is never edited, in any form, permanently. The correction is not "pending" — it is **complete now**, in the form of a permanent, discoverable record: `BLG-GOV-334` itself, rewritten from "action pending at next post-ship" to "Resolved — true fact recorded here, sealed source intentionally untouched." This mirrors the audit/erratum pattern already established elsewhere in this codebase (`e06cfa94`'s precedent for historical records) rather than treating the sealed-artefact constraint as a problem still waiting to be solved.

  **Acting as Product Owner** (per `claude/agents/product_owner.md` §6 "accepts or rejects outcomes based on spec-defined behaviour," on explicit user direction: "act as PO yourself"): accepted this disposition as satisfying `ST-21`'s underlying intent. The AC's literal wording ("test count in `qa_evidence_EPIC-03.md`... matches the actual number") can never be met once the sealed-artefact constraint is factored in — no future action, however patient, makes that literally true. The AC's actual purpose — don't let a known-wrong number stand permanently uncorrected with nothing pointing at the truth — is fully served by `BLG-GOV-334` standing as that permanent correction. This is a reinterpretation of AC completion under discovered constraints, not a waiver of the AC's intent; the reinterpretation itself is documented, traceable, and reversible only by explicit agreement (per Head of Specs Team's own charter §6), same as the interpretation itself.

  Both `BLG-QA-170` and `BLG-GOV-334` closed on this disposition (`claude/backlog/backlog.md`, this same session). `qa_evidence_EPIC-03.md` updated: ST-21 row changed from "Deferred" to "Pass (accepted disposition)," sign-off block changed from partial (ST-15–20 only) to full (all 7 stories), Product Owner sign-off line added.
- **Status:** Resolved (final) — unblocking ST-21, marking done. EPIC-03 is now 7/7 done, satisfying `execution_prompt.md` §3.2 in full.

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

## DEL-20260918-02

- **ST Item:** ST-14 — Provision read-only staging `DATABASE_URL` for sprint-execution sessions (resolution of `DEL-20260916-04`)
- **EPIC:** EPIC-02
- **Classification:** delegated_decision — resolved
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1682
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-02
- **Resolved at:** 2026-09-18T02:00:00Z (user provisioned the credential and worked through several real infrastructure issues interactively to get it connecting)
- **Resolution:**
  User created a `readonly_staging` Postgres role on the staging Supabase project (`GRANT SELECT` only, `ALTER DEFAULT PRIVILEGES` for future tables too) and worked through delivering it into this session's environment. Several genuine issues surfaced and were resolved along the way, each worth recording since they'll recur for any future credential handoff of this kind:
  1. **A tool-use mistake on this session's part leaked the connection string into the transcript** (`${DATABASE_URL:-no}` substitutes the actual value when set, not a fallback "no" — a scripting error, not the user's). Password was rotated in response; flagged immediately and transparently.
  2. **`STAGING_DATABASE_URL` (a different, pre-existing GitHub secret) was also briefly overwritten with a read-only value**, which would have broken `reset-and-seed-staging.yml`, `seed-preview.yml`, and `scripts/reset_staging_db.sh` (all three need write access). Resolved by leaving `STAGING_DATABASE_URL` alone and using the bare `DATABASE_URL` secret name (freed up by repointing `backtest.yml` at `PROD_DATABASE_URL` instead — see the `[EPIC-02][ST-14]` commit `26d5b2b1`) for the read-only staging credential, with no new secret name needed.
  3. **Environment variables only take effect for genuinely new processes** — multiple rounds of "still not picked up" traced back to: (a) duplicate `export DATABASE_URL=` lines accumulating in `~/.bashrc` from repeated `>>` appends, and (b) this Claude Code session itself needing to be fully restarted (`claude --continue` from the corrected terminal), not just a new terminal tab opened alongside the same still-running process. Verified at each step via a safe length/sha256-fingerprint check (never printing the value) to confirm whether the environment had actually changed before retrying.
  4. **An unescaped `@` in the password broke `postgresql://` URI parsing** (`psql` tried to resolve part of the password as a hostname). Fixed by choosing a new password without URI-reserved characters (`@`, `:`, `/`, `?`, `#`).

  Once correctly delivered, verified live end-to-end (this story's own AC-03): connects as `readonly_staging`; `SELECT count(*) FROM portfolios` returned real data; `UPDATE portfolios SET last_updated = now()` correctly rejected with `permission denied for table portfolios` (retried against a real column after an initial attempt against a nonexistent column, which wasn't a valid permission test). Documented in `docs/infrastructure/staging_setup.md` §8.

  `BLG-OPS-162` closed. This also retires the recurring "no live DB access" disclosure pattern that has appeared across v9.2–v9.5 sprint execution — future stories with a staging-data-verification AC can now run a real query instead of disclosing a synthetic-fixture substitute.
- **Status:** Resolved — unblocking ST-14, marking done. EPIC-02 is now 10/10 done.

---
## DEL-20260918-04

- **ST Item:** ST-35 — File a Product Owner decision record for ST-20's trade-tagging "no closed taxonomy" call
- **EPIC:** EPIC-05
- **Classification:** delegated_decision — resolved
- **Assigned to:** Product Owner
- **GitHub Issue:** #1703
- **Branch:** exec/2026-09-15__release-v9.5/EPIC-05
- **Resolved at:** 2026-09-18T18:11:06Z (agent-mediated Product Owner sign-off, §5.3 — a genuine open product decision, but one where the correct answer was fully determined by re-checking ST-20's own already-shipped, independently-verified implementation review against the codebase, not a fresh judgment call requiring new information)
- **Resolution:**
  Re-read `docs/specs/trade_tagging_taxonomy.md`'s existing Purpose section (ST-20, EPIC-04, v9.3) — it already documents, with a specific citation to the original UX spec and a confirmed backend/frontend constant match, that `trade_plans.trade_tags` was always intentionally free-text/format-constrained, never a closed taxonomy. Filed `docs/product/decisions/trade-tagging-taxonomy-scope-reframing-decision--2026-09-18.md` ratifying that finding as a formal decision record, following this codebase's established precedent pattern (`setup-type-other-conflation-decision--2026-08-21.md`), and cross-referenced it from the spec (`trade_tagging_taxonomy.md` v1.0→v1.1).
  `BLG-GOV-320` closed.
- **Status:** Resolved — unblocking ST-35, marking done.

---
