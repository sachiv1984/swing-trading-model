Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-22 (DEL-20260921-01 Unblocked — ST-09 trailing-stop entry-floor decision ratified); prior — 2026-09-21 (cycle open, 6 delegation records created)

---

# Delegation Log - 2026-09-21__release-v9.6

Append-only. Do not edit previous entries.

---

## DEL-20260921-01

- **ST Item:** ST-09 - calculate_trailing_stop's entry-price floor for profitable positions diverges from strategy_rules.md §7.2/§7.3 and from the backtest tool
- **EPIC:** EPIC-03
- **Classification:** delegated_decision
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1726
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-03
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Confirm/rule on the trailing-stop entry-price-floor decision (options i/ii/iii in ESC-EXEC-20260921-01); engine will add the golden-output case autonomously.
- **Unblock criteria:** see ESC-EXEC-20260921-01
- **Commit format required:** `[EPIC-03][ST-09] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-03` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Unblocked — in-session credential/action provisioning not applicable (no external credential needed); Strategy Rules & System Intent Owner ruling obtained directly within this session (agent-mediated, §5.3, on explicit user direction) per execution_prompt.md §5.2. Ruling: Option (i) — see ESC-EXEC-20260921-01 Resolution (Addendum) for full rationale. Sign-off cleared 2026-09-22T08:14:51Z; commit `f771d5c9` pushed same timestamp (golden-output case + implementation cross-check). No multi-session parking occurred (LL-v8.2-P3-04 in-session completion pattern).

---

## DEL-20260921-02

- **ST Item:** ST-16 - Confirm synthetic uptime monitor live-fire and notification delivery (ST-11 follow-up)
- **EPIC:** EPIC-04
- **Classification:** delegated_decision
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1733
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-04
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Perform/enable the Actions-write live-fire run and confirm real Telegram receipt (ESC-EXEC-20260921-02).
- **Unblock criteria:** see ESC-EXEC-20260921-02
- **Commit format required:** `[EPIC-04][ST-16] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-04` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Sign-off:** cleared — user (Infrastructure & Operations Owner) triggered the live-fire run via the Actions UI directly, bypassing the engine's own Actions-write token blocker, and independently confirmed Telegram receipt. See ESC-EXEC-20260921-02 Resolution and `docs/ops/synthetic_uptime_monitor_confirmation_2026-09-16.md` §7.
- **Commit SHA:** `1f483d0a905498ce1b6d1e541b40425f5358a34b`
- **Status:** Unblocked

---

## DEL-20260921-03

- **ST Item:** ST-22 - DS-17 unique index migration not yet applied to live positions table
- **EPIC:** EPIC-06
- **Classification:** delegated_decision
- **Assigned to:** Data Model & Domain Schema Owner + Infrastructure & Operations Owner
- **GitHub Issue:** #1739
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-06
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Apply the DS-17 up-migration to the live positions table after re-running the duplicate pre-check, and confirm (ESC-EXEC-20260921-04).
- **Unblock criteria:** see ESC-EXEC-20260921-04
- **Commit format required:** `[EPIC-06][ST-22] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-06` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Pending

---

## DEL-20260921-04

- **ST Item:** ST-23 - PO-05 (Lightweight Replay Mode) §13 determinism pre-clearance review, standalone
- **EPIC:** EPIC-06
- **Classification:** delegated_decision
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1740
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-06
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Issue the dated §13 determination for PO-05 (ESC-EXEC-20260921-05).
- **Unblock criteria:** see ESC-EXEC-20260921-05
- **Commit format required:** `[EPIC-06][ST-23] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-06` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Pending

---

## DEL-20260921-05

- **ST Item:** ST-28 - Re-confirm §13 boundary review cadence
- **EPIC:** EPIC-07
- **Classification:** delegated_decision
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1745
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-07
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Decide schedule-now vs defer-with-concrete-trigger for the §13 boundary review (ESC-EXEC-20260921-06).
- **Unblock criteria:** see ESC-EXEC-20260921-06
- **Progress (2026-09-23T00:00:00Z):** 2 concrete options drafted per this story's own "engine may draft options but must not choose" note — see `decisions--2026-09-21__release-v9.6.md` ST-28 section. Option A: schedule the ATR review now. Option B: defer, trigger = `strategy_rules.md` §12.2's existing 100-closed-trades-since-last-review threshold (engine's lean, not a decision). Awaiting Strategy Rules & System Intent Owner's pick.
- **Commit format required:** `[EPIC-07][ST-28] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-07` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Pending — options drafted, decision outstanding

---

## DEL-20260921-06

- **ST Item:** ST-29 - Revisit sprint capacity band given sustained ≥90% utilisation
- **EPIC:** EPIC-07
- **Classification:** delegated_decision
- **Assigned to:** Product Owner
- **GitHub Issue:** #1746
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-07
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Supply the hold/raise decision on the sprint capacity band (ESC-EXEC-20260921-07).
- **Unblock criteria:** see ESC-EXEC-20260921-07
- **Progress (2026-09-23T00:00:00Z):** FinOps & Resource Architect utilisation review completed and recorded in `workforce_capacity.md` §Sprint Capacity Band Utilisation Review (agent-mediated, §5.3) — full history reconstructed (23 cycles), recommendation to reconfirm the band recorded. The hold/raise/reconfirm disposition itself remains the Product Owner's own call per this file's ownership note — not made here.
- **Commit format required:** `[EPIC-07][ST-29] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-07` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Pending — review complete, decision outstanding

---


## DEL-20260921-07

- **ST Item:** ST-18 - Quarterly full-suite Playwright re-run against a fresh staging seed
- **EPIC:** EPIC-05
- **Classification:** delegated_qa
- **Assigned to:** Director of Quality
- **GitHub Issue:** #1735
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-05
- **Delegated at:** 2026-09-22T12:15:00Z
- **What is needed:** AC-01 (cadence and seed procedure documented) is complete - see `docs/testing/quarterly_playwright_staging_reseed_procedure.md`. That document also surfaces an architecture finding needing disposition: the existing Playwright suite is entirely mock-based (no live backend/DB dependency by design), so "a fresh staging seed" doesn't literally apply to it - a two-part redefinition (Part 1: Playwright re-run on a fresh CI build; Part 2: Phase-B backend suite against a freshly reset staging seed) is proposed as the recommended path. Needs: (a) Director of Quality disposition on the redefinition, (b) Part 1's run triggered via `gh workflow run playwright.yml` on a real GitHub-hosted runner (this sandbox cannot install Chromium - confirmed structural limitation), (c) Part 2's run triggered via `reset-and-seed-staging.yml` then a Phase-B test run against the freshly-seeded staging DB (destructive step, must not be triggered without explicit human-observed decision).
- **Unblock criteria:** Director of Quality confirms the redefinition (or specifies an alternative) and either performs both first runs or authorises the engine to trigger them in a future session, with results recorded in `docs/testing/quarterly_playwright_staging_reseed_procedure.md`'s Run Log.
- **Progress (2026-09-22T12:50:27Z):** Part 1 completed - Director of Quality triggered `playwright.yml` directly (run `35729627868`), all 8 E2E shards + Visual Snapshots green (Visual Regression Baselines is advisory-only, `continue-on-error: true`, not counted). Triggering it is treated as implicit acceptance of the two-part redefinition. Part 2 (Phase-B backend suite against a freshly reset staging seed) still outstanding - remains destructive and not triggered without a further explicit human-observed decision.
- **Progress (2026-09-22T13:23:18Z):** Part 2 step 1 (reset-and-seed) completed - Director of Quality fixed `STAGING_DATABASE_URL` (was pointed at Supabase's direct IPv6-only host, unreachable from GitHub-hosted runners; corrected to the Transaction pooler URI) and triggered `reset-and-seed-staging.yml` directly. First attempt (run `35730287893`) failed on the stale secret (`Network is unreachable`); second attempt after the fix (run `35733092701`) succeeded - fresh baseline, schema v2.0, QA data seeded.
- **Sign-off:** cleared — Part 2 step 2 corrected: "run the Phase-B backend suite against staging" was found (while attempting it) to conflate `ci-tests.yml`'s own unrelated, always-fresh ephemeral-Postgres Phase B job with a genuine staging test; running the real write-heavy suite against shared staging risked damaging the schema/seed data just established (`test_schema_rollback_verification.py` applies/rolls back real migrations). Corrected to a safe, read-only independent verification instead — on explicit user direction ("do both": accept Part 2 as done at step 1, and separately run read-only checks) — 7 `SELECT COUNT(*)`/spot-check queries run against the freshly-seeded staging DB via the `readonly_staging` role, every value matched the reset workflow's own claimed summary exactly (see `docs/testing/quarterly_playwright_staging_reseed_procedure.md` §Run Log for the full table).
- **Commit SHA:** see `[EPIC-05][ST-18]` commits on this branch (multiple, cumulative)
- **Commit format required:** `[EPIC-05][ST-18] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-05`
- **Status:** Unblocked
