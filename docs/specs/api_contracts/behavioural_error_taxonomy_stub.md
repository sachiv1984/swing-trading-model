# Behavioural Error Taxonomy — Arc 4 PO-03 (Pre-Authoring Stub)

**Version:** 0.1.0 (stub — not implemented)
**Last Updated:** 2026-09-18
**Spec Owner:** API Contracts & Documentation Owner
**Governed by:** docs/specs/api_contracts/conventions.md
**Story:** ST-23 (BLG-SPEC-56, EPIC-04, v9.5 sprint execution)

---

> **This is a pre-authoring stub, not a canonical contract.** No `PO-03` endpoint exists in `backend/routers/` and no entry for it exists in `docs/reference/openapi.yaml` — both correctly absent, since nothing has been built yet. Headings below intentionally do **not** use the canonical `## METHOD /path` form (see `CLAUDE.md` §2 / `scripts/openapi_3way_drift_sweep.py`) so this stub is not picked up by the OpenAPI Drift Detection gate as a documented-but-missing endpoint. When PO-03 is actually built, its real contract entry must use the canonical `## GET /trades/{trade_id}/error-classification` form in this same file (or a renamed non-stub file) with a matching `openapi.yaml` entry added in the same commit, per `CLAUDE.md` §2.
>
> Path, method, and field names below are **placeholders for design-time planning** — chosen to match `docs/qa/arc4_e2e_test_strategy_po02_03_04.md` §4.2's already-published mock fixture shape, not a committed API surface. Revise or supersede at PO-03's own sprint planning / contract-authoring step.

---

## Proposed — GET /trades/{trade_id}/error-classification

**Description:** Per-trade behavioural error classification (e.g. "entered too early", "held too long", "sized incorrectly", "ignored regime") derived from a closed trade's linked `plan_vs_reality` deviations and/or `trade_reflections` entry. Display-only, advisory. Feeds Arc 5 drift detection as an input signal, per the roadmap's own PO-03 description — this stub does not attempt to define that Arc 5 consumption contract, only PO-03's own output. Roadmap ID: `PO-03`.

**Gate condition (roadmap):** Requires PO-01 (shipped) and PO-02 data foundation. **Open question, not resolved by this stub** (carried verbatim from `arc4_e2e_test_strategy_po02_03_04.md` §4.2 item 3): whether PO-03 strictly requires both a linked trade plan *and* a PO-02 pattern-analysis run per trade, or can classify from `plan_vs_reality` deviations alone when PO-02 data is absent for that trade. The proposed `source_inputs` response/storage field below exists specifically so this can be answered empirically once real data exists, rather than needing a schema change later.

### Path Parameters

| Param | Type | Notes |
|-------|------|-------|
| `trade_id` | string (UUID) | Matches `trade_history.id`. |

### Response (proposed shape)

```json
{
  "status": "ok",
  "data": {
    "available": true,
    "error_types": ["sized_incorrectly"],
    "confidence": 0.8,
    "source_inputs": ["plan_vs_reality"]
  }
}
```

| Field | Type | Notes |
|-------|------|-------|
| `available` | boolean | `false` if the trade has no classifiable inputs yet (e.g. no linked plan and no reflection) — a distinct state from an empty `error_types` array (which would mean "classified, no errors found"). |
| `error_types` | array of strings | Array, not a single value — a trade can plausibly carry more than one classified error simultaneously (per the roadmap's own PO-03 description listing multiple error categories). |
| `confidence` | number (0.00–1.00) | Per-classification AI confidence score. |
| `source_inputs` | array of strings | Which underlying data the classification actually used this call (e.g. `plan_vs_reality`, `trade_reflection`) — see the Gate condition note above. |

**§13 note (display-only):** per every other AI-output surface in this codebase (SRB-v1.7), the eventual real contract must carry an explicit advisory-only disclosure requirement in its AC, and must not itself gate or block any trade action — not assumed here, flagged for the real contract-authoring step.

### Data model reference

`trade_error_classifications` table (proposed, not created) — see `docs/product/arc4_data_model_pre_definition_po02_03_04.md` §3.2.

---

## Sign-off

Per `BLG-SPEC-56`'s own Owner field (Head of Specs Team):

| Role | Status | Notes |
|------|--------|-------|
| Head of Specs Team | ✅ Accepted | Agent-mediated (§5.3) — see sign-off record for ST-23 in this cycle's `execution_state.json`. Stub-only; no implementation commitment made. |
| API Contracts & Documentation Owner | ✅ Accepted | Agent-mediated (§5.3) — file lives in this role's directory and follows its conventions; co-sign alongside the AC-named Head of Specs Team, not a substitute for it. |
