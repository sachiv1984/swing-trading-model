Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-20 (EPIC-05 merge reconciliation — DEL-20260818-03 renumbered to DEL-20260818-07, collided with EPIC-02's own DEL-20260818-03)

# Delegation Log — 2026-08-17__release-v8.9

Append-only. Do not edit previous entries.

---

## DEL-20260817-01

- **ST Item:** ST-01 — Fix nightly trailing-stop ratchet to apply breakeven floor for profitable positions
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Backend Engineering Patterns Owner
- **GitHub Issue:** #1429
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-01
- **Delegated at:** 2026-08-17T17:15:00Z
- **What is needed:** Confirm which trailing-stop calculation path runs in production for the nightly job and any on-demand recompute (BLG-BE-102 scope item 1); consolidate on `backend/utils/calculations.py::calculate_trailing_stop` (has the breakeven floor) if a second, unfloored path is found live; add a regression test covering the breakeven-floor case using BLG-BE-102's own WDC worked example.
- **Spec reference:** `backend/utils/calculations.py#calculate_trailing_stop` (pre-existing canonical implementation; no prior dedicated spec doc — bug/correctness investigation per execution_prompt.md STEP 3.1.A Case E pattern, closed with a regression test as the traceable artefact instead)
- **Unblock criteria:** Code-path audit complete and documented; regression test added and passing; Backend Engineering Patterns Owner sign-off.
- **Commit format required:** `[EPIC-01][ST-01] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-01`
- **Status:** Unblocked — in-session credential/action provisioning not applicable (no external credential needed); engine completed the investigation and regression test directly within this session per execution_prompt.md §5.2 (engine may write and commit code where the spec/AC is unambiguous). Agent-mediated Backend Engineering Patterns Owner sign-off (§5.3) cleared Approved 2026-08-17; regression test suite (7/7) passing. No multi-session parking occurred (LL-v8.2-P3-04 in-session completion pattern).

---

## DEL-20260817-02

- **ST Item:** ST-02 — Fix currency basis of current_trailing_stop/stop_price for US-market positions
- **EPIC:** EPIC-01
- **Classification:** delegated_backend
- **Assigned to:** Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner
- **GitHub Issue:** #1430
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-01
- **Delegated at:** 2026-08-17T17:15:00Z
- **What is needed:** `initial_stop`, `current_trailing_stop`, and `stop_price` must be in a consistent currency basis for a given position, or unambiguously suffixed with the frontend consuming the correct one. Add `current_trailing_stop_native` to `GET /positions` (backend/services/position_service.py::get_positions_with_prices) and update PositionCard.js/Positions.js to render it instead of the GBP-converted `current_trailing_stop`. Add a regression test case for a US-market profitable position showing a single consistent stop value across Init and live-stop tiles.
- **Spec reference:** `docs/specs/api_contracts/position_endpoints.md#Field notes`; `docs/specs/frontend/pages/positions.md#Trailing Stop Column`
- **Unblock criteria:** Backend field added; frontend consumers updated on both Card and Table views; regression tests (pytest + Playwright) added and passing; pre-existing e2e fixtures re-verified against the corrected field; Backend Engineering Patterns Owner and Frontend Specifications & UX Documentation Owner sign-off.
- **Commit format required:** `[EPIC-01][ST-02] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-01`
- **Status:** Unblocked — same in-session completion pattern as DEL-20260817-01. Agent-mediated Backend Engineering Patterns Owner and Frontend Specifications & UX Documentation Owner sign-offs (§5.3) both cleared Approved 2026-08-17; regression suite (pytest 2/2, Playwright 2/2) passing, pre-existing e2e fixtures re-verified.

---

## DEL-20260818-01

- **ST Item:** ST-23 — §13 System Boundary Review: Automated AI Post-Trade Debrief
- **EPIC:** EPIC-02
- **Classification:** delegated_decision
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1451
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-02
- **Delegated at:** 2026-08-18T00:00:00Z
- **What is needed:** Produce a §13 pre-assessment document per `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-gate-story-scoping.md` §2's 5 acceptance criteria, addressing determinism/own-data-only/non-predictive/decision-support-only against ST-06's "one suggested focus area" output specifically, with binding conditions and an explicit Determination.
- **Spec reference:** `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-gate-story-scoping.md` (scoping); deliverable is `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` itself
- **Unblock criteria:** Determination reaches PASS or CONDITIONAL; Strategy Rules & System Intent Owner sign-off.
- **Commit format required:** `[EPIC-02][ST-23] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-02`
- **Status:** Unblocked — in-session completion, no external credential needed. Agent-mediated Strategy Rules & System Intent Owner sign-off (§5.3) required 2 retries (3 review passes total, within the 2-retry cap): Pass 1 Blocked (Conditions 1/2 prompt-instruction-only, no output-side verification — fixed by adding Condition 9); Pass 2 Blocked (Condition 9 sound but Determination section not updated to match — fixed, count and sequencing corrected); Pass 3 Approved 2026-08-18. Determination: CONDITIONAL, 9 binding conditions. Commit: `cdc27936aa2f06151ab9ed4a50f859dd9795e69b`.

---

## DEL-20260818-02

- **ST Item:** ST-04 — Correlation/sector-concentration-aware position sizing
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Backend Engineering Patterns Owner
- **GitHub Issue:** #1432
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-02
- **Delegated at:** 2026-08-18T01:00:00Z
- **What is needed:** Extend `POST /portfolio/size` (sizing_service.py) to reduce or flag suggested size when it would push sector exposure past the existing §4.2.2 canonical 30% concentration threshold, reusing (not redefining) that threshold; expose `concentration_adjusted`/`concentration_reason` per `docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md`; add a regression test confirming two same-sector positions produce a smaller second size than two uncorrelated ones would.
- **Spec reference:** `docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md`
- **Unblock criteria:** Backend adjustment implemented and reusing the canonical threshold; `portfolio_endpoints.md` + `openapi.yaml` updated same-commit; regression test added and passing; frontend display wired per the design record; Backend Engineering Patterns Owner sign-off.
- **Commit format required:** `[EPIC-02][ST-04] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-02`
- **Status:** Unblocked — engine implemented directly this session (backend + frontend), no external credential needed. Commit `97e6c407e4a20437451f6a11cbfec0b81c0b0b7b`. Agent-mediated Backend Engineering Patterns Owner sign-off (§5.3) cleared Approved 2026-08-18; regression suite (9 pytest, full backend suite 1179/1179) and Playwright suite (3 tests, run live) passing.

---

## DEL-20260818-03

- **ST Item:** ST-05 — Pre-commit "what-if" sizing/risk simulator on the trade-plan form
- **EPIC:** EPIC-02
- **Classification:** delegated_frontend (sprint_backlog.md) — reclassified to engine-completed per LL-v2.3-CL-01 autonomous default
- **Assigned to:** Head of Engineering; Frontend Specifications & UX Documentation Owner
- **GitHub Issue:** #1433
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-02
- **Delegated at:** 2026-08-18T02:00:00Z
- **What is needed:** New "What-If Sizing Preview" panel on the Trade Plan form (`WhatIfSizingPreview.js`), reusing `POST /portfolio/size`; extract `calculate_prospective_heat` from `prospective_heat.py` into `portfolio_service.py` and wire `heat_impact_percent` into `sizing_service.py` so both call sites share one calculation.
- **Spec reference:** `docs/design/2026-08-17__release-v8.9/what-if-sizing-risk-simulator/ux_spec.md`; `docs/specs/frontend/pages/trade_plan.md#5d`
- **Unblock criteria:** Panel implemented per design contract; backend heat field shared, not duplicated; regression tests (pytest + Playwright) added and passing; Head of Engineering and Frontend Specifications & UX Documentation Owner sign-off.
- **Commit format required:** `[EPIC-02][ST-05] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-02`
- **Status:** Unblocked — engine implemented directly this session, no external credential needed. Commits `cb328805` (implementation) and `86cfc078` (FX-conversion fix from sign-off review). Agent-mediated Head of Engineering sign-off (§5.3) cleared Approved 2026-08-18 first pass. Agent-mediated Frontend Specifications & UX Documentation Owner sign-off required 1 retry (within the 2-retry cap): first pass Blocked (R at Risk missing FX conversion for US-market plans, DEV-v8.9-ST05-02 filed and fixed same-day); second pass Approved 2026-08-18.

---

## DEL-20260818-04

- **ST Item:** ST-07 — In-app backtesting engine for strategy rule changes
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Strategy Rules & System Intent Owner; Head of Engineering
- **GitHub Issue:** #1435
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-02
- **Delegated at:** 2026-08-18T04:00:00Z
- **What is needed:** Run a candidate `strategy_rules.md` parameter change against historical data entirely in-app (no external script step), compare it against the live rule set, and persist each run for audit. RISK-02: largest single item this cycle — confirm `production_strategy.py` simulation-logic reuse feasibility early; scope may narrow to a smaller candidate-comparison surface if infeasible.
- **Spec reference:** `docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md`; `docs/specs/frontend/pages/strategy_benchmark.md#7.6`; `docs/specs/api_contracts/strategy_benchmark_endpoints.md`
- **Unblock criteria:** Backend engine implemented (full production_strategy.py reuse found infeasible for a synchronous web request — RISK-02's contingency exercised, bounded-universe/window scope applied instead, both sides of the comparison run identically); 3 new endpoints registered with all CLAUDE.md same-commit requirements; regression tests (pytest + Playwright) added and passing; Strategy Rules & System Intent Owner (AC-04) and Head of Engineering sign-off.
- **Commit format required:** `[EPIC-02][ST-07] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-02`
- **Status:** Unblocked — engine implemented directly this session, no external credential needed. Commits `967e77f4` (implementation) and `0b0a8caf` (sign-off review fixes). Agent-mediated Strategy Rules & System Intent Owner sign-off (§5.3, AC-04) cleared Approved 2026-08-18 first pass — LIVE_PARAMS fidelity independently re-verified against `strategy_rules.md`/`production_strategy.py`, no drift. Agent-mediated Head of Engineering sign-off cleared Approved 2026-08-18 first pass — port fidelity confirmed line-by-line, 2 minor fast-follow items applied same-day (error-code doc correction, dead-code removal).

---

## DEL-20260818-05

*(Renumbered at CLAUDE.md §8 cross-EPIC merge reconciliation, 2026-08-19 — originally filed as `DEL-20260818-01` on the EPIC-03 branch, independently of and colliding with EPIC-02's own `DEL-20260818-01` above, which merged into `main` first via PR #1453. Content unchanged from the original EPIC-03 filing; only the ID changed. `execution_state.json`'s EPIC-03/ST-09 `delegation_record_id` updated to match in the same commit.)*

- **ST Item:** ST-09 — Verify ST-11 duration logging against a real post-merge invocation
- **EPIC:** EPIC-03
- **Classification:** delegated_backend
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1437
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-03
- **Delegated at:** 2026-08-18T07:35:00Z
- **What is needed:** A real, post-merge production invocation's Render log line confirming the `"SI-05 digest sent... in %.2fs"` (or failure-path equivalent) log statement fires with a genuine elapsed-time value, then `docs/ops/api_performance_baseline.md` §36 updated with that real timing. (Note: the story's title references "ST-11 duration logging" — this is an inherited label from its source item BLG-BE-99, predating this cycle's own ST-11; the AC's actual subject is the `"SI-05 digest sent"` log line, unrelated to this cycle's ST-11 dead-code-removal story.)
- **Spec reference:** `docs/ops/api_performance_baseline.md#§36` (target update location; no other canonical spec exists for this staging-only verification)
- **Unblock criteria:** A live Render production log excerpt showing the digest-timing line with a real `%.2fs` value; `api_performance_baseline.md` §36 updated to match; Infrastructure & Operations Owner sign-off.
- **Commit format required:** `[EPIC-03][ST-09] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-03`
- **Status:** Blocked — genuinely cannot be completed by the Sprint Execution Engine in-session: the AC requires a real Render production log line from a *post-merge* invocation, which by definition postdates this branch's own merge and is not reproducible in CI or locally (per the story's own note in `stage4_backlog_slice.md`: "not CI-reproducible"). Parked per execution_prompt.md §5.2/§6 "continue to the next ST item, do not stall" — `blocked_since_utc` set in `execution_state.json`; EPIC-03's other stories proceed independently. Requires human/ops action post-merge to unblock.

---

## DEL-20260818-06

*(Renumbered at CLAUDE.md §8 cross-EPIC merge reconciliation, 2026-08-19 — originally filed as `DEL-20260818-02` on the EPIC-03 branch, independently of and colliding with EPIC-02's own `DEL-20260818-02` above, which merged into `main` first via PR #1453. Content unchanged from the original EPIC-03 filing; only the ID changed. `execution_state.json`'s EPIC-03/ST-08 `delegation_record_id` updated to match in the same commit.)*

- **ST Item:** ST-08 — Investigate GET /trade-plans/tags ~10s p50 latency
- **EPIC:** EPIC-03
- **Classification:** delegated_backend
- **Assigned to:** Backend Engineering Patterns Owner
- **GitHub Issue:** #1436
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-03
- **Delegated at:** 2026-08-18T07:40:00Z
- **What is needed:** Identify why `GET /trade-plans/tags` runs ~10s p50 vs. the ~4x-faster sibling `GET /positions/tags`; apply a fix (or file a documented follow-up); re-measure p50 within the same order of magnitude as the sibling endpoint (staging-only, see note below); Backend Engineering Patterns Owner sign-off.
- **Spec reference:** `docs/ops/db_index_audit_arc4_2026-08-06.md` (prior related index-audit finding for this same table); no dedicated canonical spec exists for endpoint latency budgets beyond `docs/ops/api_performance_baseline.md`
- **Unblock criteria:** Root cause identified and documented; fix applied with regression test coverage; Backend Engineering Patterns Owner sign-off. (The re-measured-p50 AC sub-item is staging-only per `sprint_backlog.md`'s own note — "requires production/staging latency measurement, not CI-reproducible" — and does not block this item's completion, consistent with the sprint's pre-authorized QA-criteria review.)
- **Commit format required:** `[EPIC-03][ST-08] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-03`
- **Status:** Unblocked — same in-session completion pattern as DEL-20260817-01/02. Root cause identified (11 per-request call sites of the DDL-heavy `ensure_trade_plans_table()` vs. 0 for the sibling endpoint); fix applied (process-global memoization flag) with regression coverage. Agent-mediated Backend Engineering Patterns Owner sign-off (§5.3) required 2 retries (2 independent vacuous-test-assertion bugs found and fixed in the pre-existing `test_trade_plans_ticker_index.py` suite, each empirically re-verified via temporary regression injection) before clearing Approved 2026-08-18 on the 3rd/final attempt (within the 2-retry cap). Full backend suite (1174 passed, 5 skipped, 0 failed) confirmed clean after each round.

---

## DEL-20260818-05 — Status Update (Addendum)

*(Renumbered reference — originally titled "DEL-20260818-01 — Status Update (Addendum)" on the EPIC-03 branch; refers to the entry now filed as DEL-20260818-05 above, per the renumbering note there.)*

- **Refers to:** DEL-20260818-05 (ST-09) above. This file is append-only — recording the status transition as a new entry rather than editing the original.
- **Updated at:** 2026-08-18T08:05:00Z
- **New status:** Cancelled (per `execution_prompt.md` line 837: "If the item is `returned_to_backlog`: update the delegation log entry status to `Cancelled`").
- **Reason:** `execution_state.json`'s ST-09 status changed to `returned_to_backlog`, applying the in-flight transition (AUD-2026-05-27-003) rather than waiting for formal sprint close. Basis: the pre-existing, sealed `sprint_backlog.md` staging-only designation for this item, already reviewed and confirmed non-blocking by the sprint's own QA-criteria review — not a fresh live Product Owner exchange in this session. Flagged for human review; if judged insufficient, this can be reverted to `blocked_backend` and re-applied at formal STEP 5.2 with no change to the eventual outcome.

---

## DEL-20260818-05 — Status Update (Second Addendum)

- **Refers to:** DEL-20260818-05 (ST-09) above. This file is append-only — recording this status transition as a new entry rather than editing the original or the prior addendum.
- **Updated at:** 2026-08-20T07:20:00Z
- **New status:** Complete.
- **Reason:** EPIC-03 merged to `main` (PR #1454, 2026-08-20), clearing the original pre-merge structural blocker. A real post-merge invocation was triggered (`si05-weekly-digest.yml` `workflow_dispatch`, run 32342881081) and its Render log genuinely reviewed. The digest-timing line was found genuinely absent — root-caused to a separate, pre-existing platform gap (no root logging configuration in production's `uvicorn` process; filed as `BLG-BE-107`), not a re-occurrence of the original pre-merge blocker. Product Owner (human, real-time in-session, 2026-08-20) directed an interim GitHub Actions step-timing proxy resolution over blocking further or fixing the logging gap inline — see `docs/ops/api_performance_baseline.md` §36.5 and `DEV-EPIC03-ST09-01`.

---

## DEL-20260818-07

*(Renumbered from DEL-20260818-03 during EPIC-02/EPIC-05 merge reconciliation, CLAUDE.md §8 — collided with EPIC-02's own DEL-20260818-03 (ST-05), which merged to main first.)*

- **ST Item:** ST-16 — Local dev venv version-pin enforcement; confirm PUBLIC_URL parity on production
- **EPIC:** EPIC-05
- **Classification:** delegated_backend
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1444
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-05
- **Delegated at:** 2026-08-18T10:10:00Z
- **What is needed:** (a) Document a mechanism for local backend dev environments to actually honour the existing `backend/.python-version` pin (3.11.0) — a `pyenv install/local` step in a local-setup doc, since plain `python3 -m venv` silently ignores it; (b) confirm production `PUBLIC_URL` status and document it.
- **Spec reference:** `docs/ops/test_environment_parity_check_2026-08-16.md#§2.1, §2.4` (source audit)
- **Unblock criteria:** README.md local-setup instructions added, correctly using pyenv to honour the pin; `.env.production` template parity fix (or documented reason it's unneeded) for `PUBLIC_URL`; Infrastructure & Operations Owner sign-off. (Full production dashboard confirmation of AC-2 is staging-only per sprint_backlog.md — not required for this item's completion, matching the audit's own advisory, not-a-confirmed-defect disposition.)
- **Commit format required:** `[EPIC-05][ST-16] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-05`
- **Status:** Unblocked — same in-session completion pattern as DEL-20260817-01/02. Agent-mediated Infrastructure & Operations Owner sign-off (§5.3) cleared Approved 2026-08-18; confirmed pyenv command correctness, confirmed the `.env.production` disclosure does not overclaim dashboard confirmation it doesn't have. No multi-session parking occurred.

---

## DEL-20260820-01

- **ST Item:** ST-06 — Automated AI post-trade debrief
- **EPIC:** EPIC-02 (Sprint 2 subset)
- **Classification:** delegated_backend
- **Assigned to:** engine (per execution_prompt.md §5.2 — spec unambiguous, the §13 review's nine binding conditions constitute a locked spec); AI Compliance & Governance Officer required for sign-off (story AC5)
- **GitHub Issue:** #1434
- **Branch:** exec/2026-08-17__release-v8.9/EPIC-02 (Sprint 2 continuation — EPIC-02's Sprint 1 PR #1453 had already merged 2026-08-19 before this story was picked up; branch recreated from post-merge `main` for this story's own commit, not reusing the closed PR)
- **Delegated at:** 2026-08-18T00:00:00Z (blocked_since_utc — gated on ST-23; unblocked the same instant ST-23 reached `done`/CONDITIONAL; actual implementation picked up in a later session, 2026-08-20)
- **What is needed:** Every newly-closed trade has an AI-generated debrief available shortly after close (on-demand, per the story's own accepted real-time-or-on-demand AC); references plan-vs-reality data and any linked journal entries where present; generation logged to `claude_audit_log`; AI Compliance & Governance Officer sign-off. Bound by the §13 review's nine conditions — most materially Condition 9 (output-side prescriptive-language scan + numeric cross-check before display/persistence, not prompt-instruction alone).
- **Spec reference:** `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`; `docs/specs/data_model.md#DS-16`; `docs/specs/api_contracts/trade_endpoints.md#GET /trades/{trade_id}/debrief`
- **Unblock criteria:** ST-23 reaches `status: done` with PASS/CONDITIONAL (met 2026-08-18); implementation matches all nine §13 binding conditions with test coverage for Condition 9's compliance checks; AI Compliance & Governance Officer sign-off.
- **Commit format required:** `[EPIC-02][ST-06] <description>` pushed to `exec/2026-08-17__release-v8.9/EPIC-02`
- **Status:** Unblocked — engine-completed in-session (no external credential needed). Commit `53286f6c6e95ddb671938388f8192d443896297d`. Agent-mediated AI Compliance & Governance Officer sign-off (§5.3) cleared Approved 2026-08-20 on first pass — Condition 9's output-side checks confirmed as real, tested code (not documentation-only); Condition 6's required verbatim comment confirmed present in `debrief_service.py`; Condition 4's no-action-affordance requirement confirmed via a dedicated Playwright assertion (SC-DBF-02b). 21 new pytest cases + 6 new Playwright scenarios, all passing; full backend suite 1260 passed/5 skipped/0 regressions.
