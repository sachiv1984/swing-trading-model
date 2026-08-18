Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-17

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

## DEL-20260818-02

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
