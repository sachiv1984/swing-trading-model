**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-09-10
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Trade Tagging Taxonomy

## Purpose

ST-20 (BLG-SPEC-76, EPIC-04, v9.3): single canonical source for the trade-plan tagging taxonomy (`trade_plans.trade_tags`, `BLG-FEAT-52`), referenced by both the UI (tag creation/editing) and reporting logic (`GET /analytics/tag-performance`). Consolidates rules that were previously stated independently (and, before this story, consistently but without a shared canonical source) in `docs/specs/api_contracts/trade_plan_endpoints.md` and `docs/specs/frontend/components/journal_components.md` §3/§4 — this document is now the source of truth those two defer to, and the one `analytics_endpoints.md`'s reporting-side documentation points to as well (previously it referenced neither).

## The Taxonomy Is Intentionally Open, Not a Closed Value List

**There is no fixed enum of canonical tag names.** `trade_plans.trade_tags` is free-text tagging, constrained only by the format rules below — not a closed taxonomy of specific permitted tag strings (e.g. there is no fixed list like `["breakout", "earnings-play", "momentum", ...]` that the system validates against). This was a deliberate design decision, confirmed in the original UX spec (`docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md` §1): "tagging the plan (e.g. 'breakout', 'earnings-play') lets a user classify a setup at the point of decision" — the examples given there are illustrative, not an exhaustive canonical list, and no component of the implementation (backend validator, frontend input, autocomplete source) ever enforces a closed set.

This section exists because ST-20's own acceptance criteria ("canonical allowed-tag taxonomy... documented") could be read as assuming a closed taxonomy exists or should be introduced. It doesn't, and this document does not introduce one — inventing a fixed tag vocabulary now would be a genuine, larger design change (affecting UX, existing user-entered tags, and the autocomplete/reporting model) well beyond this `S`-effort documentation story's scope. What follows documents the taxonomy as it actually exists: a **format-constrained free-text namespace**, which is itself the canonical, referenceable ruleset both the UI and reporting logic already implement identically.

## Canonical Format Rules

| Rule | Value | Enforced by |
|------|-------|-------------|
| Character set | Lowercase letters, digits, hyphens only (`^[a-z0-9-]+$`) | `backend/routers/trade_plans.py::_validate_trade_tags` (`_TAG_PATTERN`); `src/pages/TradePlan.js` (inline regex, same pattern) |
| Max length per tag | 20 characters | `backend/routers/trade_plans.py` (`_TAG_MAX_LENGTH`); `src/pages/TradePlan.js` (`TRADE_TAG_MAX_LENGTH`) |
| Max tags per plan | 10 | `backend/routers/trade_plans.py` (`_TAG_MAX_COUNT`); `src/pages/TradePlan.js` (`TRADE_TAG_MAX_COUNT`) |
| Deduplication | Case-insensitive; a tag already present on the plan is not added again | `backend/routers/trade_plans.py::_validate_trade_tags` |
| Invalid-tag handling | Silently dropped/filtered server-side, not rejected with an error (matches `POST /trade-plans`, `PUT /trade-plans/{id}`, and `POST /trade-plans/bulk-tag`'s existing documented behaviour in `trade_plan_endpoints.md`) | `backend/routers/trade_plans.py::_validate_trade_tags` |

**Confirmed consistent (this story's review):** the backend validator's constants (`_TAG_MAX_LENGTH=20`, `_TAG_MAX_COUNT=10`, `_TAG_PATTERN=^[a-z0-9-]+$`) and the frontend's own independently-declared constants (`TRADE_TAG_MAX_LENGTH=20`, `TRADE_TAG_MAX_COUNT=10`, inline regex `^[a-z0-9-]+$`) match exactly — no drift found between UI-side and backend-side enforcement.

## Data Independence Note

`trade_plans.trade_tags` (this taxonomy) is a **separate, data-independent field** from the pre-existing position/journal tags documented in `journal_components.md` (backed by `GET /positions/tags`). The two tag systems share the same format rules and the same visual component (Tag Editor / Tag List, reused for consistency) but are stored independently and never merged — tagging a trade plan does not tag its eventual position or journal entry, and vice versa. See `docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md` §1 for the original scope-separation decision.

## Where This Taxonomy Is Referenced

| Consumer | Reference |
|----------|-----------|
| Trade plan creation/editing (UI) | `docs/specs/api_contracts/trade_plan_endpoints.md` — `trade_tags` field row and `POST /trade-plans/bulk-tag` |
| Tag component behaviour (UI) | `docs/specs/frontend/components/journal_components.md` §3 (Tag List), §4 (Tag Editor) — shared component, same rules |
| Reporting logic | `docs/specs/api_contracts/analytics_endpoints.md` — `GET /analytics/tag-performance` (win rate / average R-multiple per tag; reads whatever free-text tags exist on closed-trade-linked plans, no taxonomy validation of its own — this document is its canonical reference for what a "tag" is) |
| Autocomplete source | `GET /trade-plans/tags` (`docs/specs/api_contracts/trade_plan_endpoints.md`) — returns the portfolio's own previously-used tags, not a canonical list |

## Acceptance

- Documented by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — documentation consolidation, no observable UI behaviour change)
- Date: 2026-09-10
