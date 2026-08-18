Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-18

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
