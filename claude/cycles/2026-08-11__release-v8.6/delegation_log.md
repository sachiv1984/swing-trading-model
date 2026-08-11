Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-11

# Delegation Log — 2026-08-11__release-v8.6

---

## DEL-20260811-01

- **ST Item:** ST-03 — Enforce trade-plan linkage at position entry + DB-level safeguard against orphaned trade_plans rows
- **EPIC:** EPIC-02
- **Classification:** delegated_backend
- **Assigned to:** Head of Engineering
- **GitHub Issue:** #1334
- **Branch:** exec/2026-08-11__release-v8.6/EPIC-02
- **Delegated at:** 2026-08-11T18:45:00Z
- **What is needed:**
  1. **Router/service layer:** Strengthen `backend/services/position_service.py::add_position()` so that trade-plan linkage is the enforced default path at position creation, not merely best-effort: when `trade_plan_id` is not supplied and `get_unlinked_trade_plan_for_entry()` finds no match, the entry flow must surface this (e.g. a warning/confirmation field in the `POST /positions` response) rather than silently proceeding unlinked — per `docs/specs/frontend/pages/trade_plan.md` §10 "Start Trade from Plan"'s already-approved default-path intent (`BLG-FE-109`, v7.3).
  2. **Database layer:** Add a DB-level safeguard against new orphaned `trade_plans` rows going forward — a constraint, trigger, or scheduled integrity check against the `trade_plans` table (`docs/specs/data_model.md` §"Table: trade_plans", lines 927–954). Given `trade_plans.position_id` is nullable by design (a plan may legitimately exist before a position is opened, or be abandoned), a hard NOT NULL constraint is not viable — the safeguard must instead flag/prevent rows that go orphaned *after* the position-entry decision point (e.g. a scheduled check for `trade_plans` rows with `status = 'active'` and `position_id IS NULL` beyond a reasonable time window, or a trigger constraining direct SQL writes that bypass `add_position()`/`create_plan()`). Design the specific mechanism and document the choice.
  3. Add/extend tests in `tests/test_position_trade_plan_link.py` (existing file, extend) covering: enforced-linkage entry flow, and the new DB-level safeguard firing correctly on a deliberately orphaned row.
  4. Staging verification that the entry-flow linkage is confirmed enforced (per AC).
- **Spec reference:** `docs/specs/frontend/pages/trade_plan.md#10 "Start Trade from Plan"` (entry-flow default, locked); `docs/specs/data_model.md#Table: trade_plans` (schema, locked) — no canonical spec yet exists for the specific DB-safeguard mechanism; document the chosen approach as a new `data_model.md` migration entry (`DS-xx`) in the same commit per document_lifecycle_guide.md, which then becomes the locked reference.
- **Unblock criteria:** Entry-flow linkage confirmed enforced (staging-verified); DB-level safeguard implemented and tested against a deliberately orphaned row; Data Model, Domain & Schema Owner + Product Owner sign-off recorded.
- **Commit format required:** `[EPIC-02][ST-03] <description>` pushed to `exec/2026-08-11__release-v8.6/EPIC-02`
- **Status:** Pending
