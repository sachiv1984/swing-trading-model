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
