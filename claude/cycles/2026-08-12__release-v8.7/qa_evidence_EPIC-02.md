Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-13

---

## Consolidation Block

**EPIC:** EPIC-02 — Trade-Plan Data Integrity Closure
**Cycle:** 2026-08-12__release-v8.7
**Sprint goal:** Deliver v8.7's user-facing feature and theme-consistency completion work while closing the mandatory trade-plan data-integrity carryover from v8.6, backed by expanded test, security, reliability, and governance coverage across the release's remaining six EPICs.
**Test scenarios used:** `tests/test_position_trade_plan_link.py` (existing regression coverage for AC-01's code path; no new test file added by this story)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-07 | `docs/specs/data_model.md#DS-12` (Verification note, ST-07, EPIC-02, v8.7) | No code change. Best-available-proxy verification of ST-03/v8.6's trade-plan-linkage enforcement, executed and documented per Product Owner (agent-mediated) authority at sprint planning: AC-01 confirmed via `position_service.py::add_position()` code path + `tests/test_position_trade_plan_link.py`; AC-03 confirmed via `ensure_trade_plans_active_requires_position_constraint()`'s unconditional startup invocation in `backend/main.py`; AC-02 (legacy-row live query) not proxyable — disclosed as residual gap, not asserted met. | See `stage4_backlog_slice.md#ST-07` (AC-01, AC-02, AC-03) | Pass with notes | None — this is a verification story, not an implementation change; no deviation from spec, but AC-02 is explicitly unmet this cycle (see notes) |

**Requirement (OA-3/ST-03) AC coverage check:** AC-01 and AC-03 — covered in the row above (Pass, via best-available proxy). AC-02 — covered in the row above (unmet, disclosed residual gap, not silently absent). The P1-escalation condition on AC-02 (any of the 11 known legacy rows found `status='active'` escalates to its own P0 immediately) remains open and independent of this story's own timeline; no such finding was made or could be made this cycle (no live DB access).

**QA test coverage:**
- Scenarios run: `tests/test_position_trade_plan_link.py` (pre-existing; re-reviewed, not re-authored, as part of this story's code-path proxy evidence)
- Regression areas checked: `position_service.py::add_position()` auto-link step; `backend/main.py` startup migration invocation sequence; `docs/specs/data_model.md#DS-12`
- Known deviations: None found — all stories' deviation checks completed with nothing to file

---

## AC-02 Residual Gap — Disposition

**Status:** Open, carried forward. Not a story failure — an explicitly PO-accepted scope limitation.

`BLG-BE-96` (this story) is not closed by this cycle's best-available-proxy execution. The live legacy-row query (`SELECT ... WHERE status='active' AND position_id IS NULL` against the 11 known pre-`BLG-BE-46` rows) requires genuine staging or production database access, which remains unavailable in this sandbox (confirmed unchanged at sprint planning, 2026-08-12, and re-confirmed at execution, 2026-08-13). No new backlog item is required — `BLG-BE-96` itself already tracks this gap and remains open at P1 pending a future session with live DB access.

The standing safeguard is unaffected by this gap: DS-12's `NOT VALID` CHECK constraint (confirmed applied on every deploy via startup invocation, see table above) prevents *new* orphaned-active rows going forward regardless of whether the legacy 11 rows are ever audited. If any of those 11 rows are later found to carry `status='active'`, that finding escalates to its own P0 immediately per the standing v8.6 condition — independent of this or any future sprint's timeline.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec — AC-01/AC-03 verified via best-available proxy; AC-02 explicitly not verified (see AC-02 Residual Gap Disposition above), disclosed rather than silently treated as met
- [x] No unresolved P0 or P1 deviations — AC-02's gap is a disclosed scope limitation on a verification-only story, not a spec deviation; no P0 finding was made
- [x] Regression areas checked
- [x] No frontend component in this EPIC (backend/documentation-only story) — URL-base-variable check not applicable
- Signed off by: Sprint Execution Engine (agent-mediated, Head of Engineering role — §5.3)
  Sprint Execution Engine (agent-mediated, Data Model & Domain Schema Owner role — §5.3)
- Date: 2026-08-13
- Comments: Backend-only, delegated_backend, single-story EPIC. Both required sign-off authorities (Head of Engineering, Data Model & Domain Schema Owner) reviewed and accepted the best-available-proxy evidence for AC-01/AC-03 and the explicit non-verification of AC-02 — see `docs/specs/data_model.md#DS-12` Verification note sign-off block, and the AC-02 Residual Gap Disposition section above. `BLG-BE-96` remains open (not closed) pending genuine live DB access in a future cycle.

