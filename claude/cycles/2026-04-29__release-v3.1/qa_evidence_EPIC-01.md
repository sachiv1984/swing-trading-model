# QA Evidence Log — EPIC-01: Trade Plan Object

**Cycle:** 2026-04-29__release-v3.1
**EPIC:** EPIC-01
**Branch:** exec/2026-04-29__release-v3.1/EPIC-01
**Owner:** Director of Quality
**Class:** Class 2 — Feature delivery
**Status:** Signed Off

---

## ST-01 — Trade Plan spec authoring: data model schema + API contract

**Verification method:** Code review

| AC | Description | Result |
|----|-------------|--------|
| AC-1 | `docs/specs/data_model.md` updated with `trade_plans` table DDL (id, portfolio_id, position_id nullable, ticker, market, all text fields, r_target NUMERIC, checklist_items JSONB, status CHECK constraint) | Pass |
| AC-2 | `docs/specs/api_contracts/trade_plan_endpoints.md` created v0.1 with 6 endpoint specs | Pass |
| AC-3 | `docs/reference/openapi.yaml` updated with 7 path entries for trade-plans routes | Pass |
| AC-4 | Data Model Domain & Schema Owner and Head of Specs Team sign-off present in data_model.md | Pass |
| AC-5 | data_model.md version bumped v2.4→v2.5 | Pass |

**Sign-off:** Director of Quality — 2026-04-30 (code review)

---

## ST-02 — Trade Plan backend: migration, CRUD endpoints, test registration

**Verification method:** Code review

| AC | Description | Result |
|----|-------------|--------|
| AC-1 | `backend/database.py` — `ensure_trade_plans_table()` idempotent (CREATE TABLE IF NOT EXISTS) with 3 indexes | Pass |
| AC-2 | CRUD functions: `create_trade_plan`, `get_trade_plans`, `get_trade_plan_by_id`, `update_trade_plan`, `delete_trade_plan`, `get_trade_plans_by_position` all present | Pass |
| AC-3 | `backend/routers/trade_plans.py` — 6 routes, Pydantic models, `_serialize` helper (datetime isoformat, JSONB list, Decimal float), 201 on POST | Pass |
| AC-4 | `backend/main.py` — trade_plans router registered | Pass |
| AC-5 | `backend/routers/test.py` — 3 new entries added (GET /trade-plans, POST /trade-plans, GET /trade-plans/by-position/…), total 43 | Pass |
| AC-6 | `src/pages/SystemStatus.js` fallback count updated to 43 | Pass |

**Sign-off:** Director of Quality — 2026-04-30 (code review)

---

## ST-03 — Trade Plan frontend: creation flow and detail view

**Verification method:** Code review
**Reclassification:** DEL-20260430-02 (delegated_frontend → autonomous)

| AC | Description | Result |
|----|-------------|--------|
| AC-1 | `src/pages/TradePlan.js` created — ticker, market, status, r_target, regime_context_at_entry (auto-populated from GET /market/status), setup_thesis, entry_rationale, confirmation_criteria, early_exit_conditions, checklist_completed fields present | Pass |
| AC-2 | Create mode: POST /trade-plans mutation on submit | Pass |
| AC-3 | Edit mode: `?edit=<id>` URL param triggers GET /trade-plans/{id} and PUT mutation | Pass |
| AC-4 | Position linking: `?position_id=` param auto-sets position_id; existing plan banner with "Edit it instead" link shown if position already has a plan | Pass |
| AC-5 | `src/pages.config.js` — TradePlan imported and registered in PAGES object | Pass |
| AC-6 | `src/pages/Positions.js` — BookOpen icon button in actions column navigates to `/TradePlan?position_id=…&ticker=…&market=…` | Pass |

**Post-merge staging verification required:** Observable UI behaviour (form submission, edit mode population, plan-exists banner) cannot be fully verified by code review. Staging verification to be completed by QA & Testing Owner post-merge.

**Sign-off:** Director of Quality — 2026-04-30 (code review; staging verification pending post-merge)

---

## Consolidation

| Story | AC Status | Sign-off |
|-------|-----------|----------|
| ST-01 | All pass | Director of Quality 2026-04-30 |
| ST-02 | All pass | Director of Quality 2026-04-30 |
| ST-03 | All pass (staging TBD) | Director of Quality 2026-04-30 |

**EPIC-01 QA: APPROVED for PR merge.**
