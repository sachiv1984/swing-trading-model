Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-12

# QA Evidence Log — EPIC-02 (Trade-Plan Data Integrity Foundation)

**EPIC:** EPIC-02 — Trade-Plan Data Integrity Foundation
**Cycle:** 2026-08-11__release-v8.6
**Sprint goal:** Ship all 26 scoped v8.6 stories — trade-plan completion-rate tracking and an AI-assisted order-placement thesis digest, trade-plan-to-position linkage enforced with a DB-level integrity safeguard, the remaining shadcn design-token and secondary-text drift debt closed, and the financial-correctness, QA-coverage, and governance-debt carryover from v8.5 fully resolved
**Test scenarios used:** `tests/test_position_trade_plan_link.py`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-03 | `docs/specs/frontend/pages/trade_plan.md#10`, `docs/specs/data_model.md#DS-12`, `docs/specs/api_contracts/portfolio_endpoints.md`, `docs/specs/api_contracts/trade_plan_endpoints.md` | (1) `POST /portfolio/position` now returns `trade_plan_linked`/`trade_plan_id`, surfacing the entry-flow linkage outcome instead of a silent server-side log line. (2) `trade_plans_active_requires_position_check` CHECK constraint (`NOT VALID`, going-forward only) as a DB-level backstop against orphaned "active" plans, plus router-level 400 guards in both `create_plan()` and `update_plan()` as the primary defense (the actual live gap: `PUT`/`POST /trade-plans` previously accepted `status='active'` with no `position_id` validation at all). Documented as `data_model.md` DS-12. | (1) Entry-flow linkage confirmed enforced (staging-verified); (2) DB-level safeguard implemented and tested against a deliberately orphaned row; (3) Data Model, Domain & Schema Owner + Product Owner sign-off recorded | Pass with notes | None (pre-existing gap, not a new deviation) — `BLG-BE-96` filed for the staging-verification and legacy-row gaps noted below |

**QA test coverage:**
- Scenarios run: `tests/test_position_trade_plan_link.py` (32 tests: existing `add_position()` auto-link/explicit-link coverage extended with `trade_plan_linked`/`trade_plan_id` assertions; new `TestUpdatePlanActiveStatusRequiresPosition` (5 tests), `TestCreatePlanActiveStatusRequiresPosition` (3 tests), `TestEnsureTradePlansActiveRequiresPositionConstraint` (1 test)); full backend suite `tests/` (1071 passed, 5 skipped, 0 failed) confirmed no regressions.
- Regression areas checked: `tests/test_api_contracts.py::test_update_trade_plan_returns_ok` required a fixture update (the pre-existing mock represented exactly the now-invalid state this story closes — status='active' with no position_id — fixed to represent a realistic already-linked plan). A genuine cross-file test-pollution bug was found and fixed during this work: an early version of the new router-level test class did `sys.modules.pop("main", None)` in `setup_method`, which silently broke `@patch("main.X", ...)`/`@patch("routers.trade_plans.X", ...)` string-path resolution for other test files collected later in the same pytest session (15 failures in `test_st04_implicit_200_error_paths_fixed.py` traced to this before being fixed) — removed; the fix and its root cause are documented inline in the test file.
- Known deviations filed: None new. **Explicitly flagged, not silently closed:** staging verification of the entry-flow enforcement was not performed (no live staging/Postgres access in this sandbox) — the delegation's literal "staging-verified" unblock criterion is not met by test-suite evidence alone. An unverified interaction between the new CHECK constraint and the 11 known legacy orphaned `trade_plans` rows was also identified. Both tracked as `BLG-BE-96`.

**Agent-mediated review trail (2026-08-12):**
1. **Data Model, Domain & Schema Owner** (domain-correctness review, independent subagent invocation): first pass **NOT CONFIRMED** — found (a) `docs/specs/api_contracts/portfolio_endpoints.md` and `trade_plan_endpoints.md` were edited (new response fields, new error rows) with no version bump or changelog row in either file, and (b) `POST /trade-plans` (`create_plan()`) had no equivalent guard to the one added in `update_plan()`, an untested gap. Both remediated in-session: version bumps + changelog rows added to both contract files; `create_plan()` guard added with 3 new tests; a stale cross-reference in `trade_plan_endpoints.md` corrected; `BLG-BE-96` filed for the staging-verification and legacy-row gaps the reviewer also raised. The reviewer's other findings (CHECK constraint correctness, `NOT VALID` rationale, response-field wiring, DS-12 structure) were confirmed sound with no changes needed.
2. **Director of Quality** (this sign-off): confirms the remediation is complete and consistent — both contract files now carry matching version bumps (`portfolio_endpoints.md` 2.6.0→2.6.1, `trade_plan_endpoints.md` 0.9→0.10) with changelog rows referencing this story; `create_plan()`'s new guard has full test coverage (`TestCreatePlanActiveStatusRequiresPosition`); the full backend suite is green post-remediation. The staging-verification gap and legacy-row-audit gap are genuinely open (not resolvable in this sandbox) and are correctly tracked as a filed backlog item rather than implied-closed anywhere in the code, docs, or execution_state.json.

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec — with one explicitly-flagged exception (staging verification), tracked as `BLG-BE-96`, not silently treated as met
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked — full backend suite green (1071 passed, 5 skipped), including a real cross-file test-pollution bug found and fixed along the way
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, backend-only story
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-12
- Comments: Standard sign-off block used (BLG-GOV-19 autonomous class does not apply — the EPIC's sole story is `delegated_backend`, failing Criterion 1). Sign-off is joint with the Data Model, Domain & Schema Owner's domain-correctness review above (agent-mediated, §5.3) — both required for this EPIC per the delegation's own unblock criteria.

### Product Owner Decision — Risk Acceptance for BLG-BE-96's Disclosed Staging Gap (2026-08-12)

**Question raised:** an agent-mediated Director of Quality + Product Owner dual review of PR #1362 flagged the disclosed deviation — ST-03's delegation named "staging-verified" confirmation as one of three co-equal unblock criteria, and that criterion is not met (this sandbox has no live Postgres/staging access) — and asked whether the risk should be accepted and the PR merged with `BLG-BE-96` as a fast-follow, or whether the PR should wait for staging verification first.

**Decision: Accept the risk. Merge with `BLG-BE-96` (P1) as a mandatory fast-follow, not a someday item.**

**Reasoning:**
- The two defenses this story ships are not equally exposed to the staging gap. The **primary defense** — router-level 400 guards in `create_plan()`/`update_plan()` — is ordinary application code with no live-DB-specific behaviour; it's exercised by 32 unit tests and its correctness doesn't depend on anything staging verification would additionally confirm. The **DB CHECK constraint** is defense-in-depth, and it is the piece staging verification is actually about.
- The constraint's blast radius is deliberately bounded by its own design: `NOT VALID` means it never retroactively validates existing rows — the only failure mode is a **future** `UPDATE` to one of the 11 already-known legacy orphaned rows, if that specific row also happens to carry `status='active'`. That's an explicit, recoverable DB error on at most 11 identified rows, not silent data corruption or a systemic outage.
- Not merging doesn't reduce this risk to zero — the 11 legacy rows exist in production today regardless of this PR. Not merging only delays shipping the actual fix for a previously-identified, real data-integrity problem (0/11 trade plans linked) that this story exists to close, while the underlying exposure (new orphaned rows continuing to be created) keeps accruing in the meantime.
- `BLG-BE-96` is concretely scoped (~0.5–1 day), has named owners (Head of Engineering + Data Model, Domain & Schema Owner), and clear acceptance criteria — this is a genuine fast-follow, not an open-ended deferral.

**Condition attached to this acceptance:** if `BLG-BE-96`'s legacy-row audit finds that any of the 11 known orphaned rows do carry `status='active'`, that specific finding must be triaged as its own P0 immediately — not absorbed into `BLG-BE-96`'s own more leisurely P1 timeline. `BLG-BE-96` itself should be scheduled promptly (this cycle or the very next), not left to drift.

- Signed off by: Sprint Execution Engine (acting as Product Owner, per explicit user direction)
- Date: 2026-08-12
