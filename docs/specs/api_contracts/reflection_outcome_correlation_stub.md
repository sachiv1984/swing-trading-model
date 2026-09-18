# Reflection ↔ Outcome Correlation — Arc 4 PO-04 (Pre-Authoring Stub)

**Version:** 0.1.0 (stub — not implemented)
**Last Updated:** 2026-09-18
**Spec Owner:** API Contracts & Documentation Owner
**Governed by:** docs/specs/api_contracts/conventions.md
**Story:** ST-23 (BLG-SPEC-56, EPIC-04, v9.5 sprint execution)

---

> **This is a pre-authoring stub, not a canonical contract.** No `PO-04` endpoint exists in `backend/routers/` and no entry for it exists in `docs/reference/openapi.yaml` — both correctly absent, since nothing has been built yet. Headings below intentionally do **not** use the canonical `## METHOD /path` form (see `CLAUDE.md` §2 / `scripts/openapi_3way_drift_sweep.py`) so this stub is not picked up by the OpenAPI Drift Detection gate as a documented-but-missing endpoint. When PO-04 is actually built, its real contract entry must use the canonical `## GET /analytics/reflection-outcome-correlation` form in this same file (or a renamed non-stub file) with a matching `openapi.yaml` entry added in the same commit, per `CLAUDE.md` §2.
>
> Path, method, and field names below are **placeholders for design-time planning** — chosen to match `docs/qa/arc4_e2e_test_strategy_po02_03_04.md` §4.3's already-published mock fixture shape, not a committed API surface. Revise or supersede at PO-04's own sprint planning / contract-authoring step.

---

## Proposed — GET /analytics/reflection-outcome-correlation

**Description:** Does journal/reflection depth correlate with trade quality? Does plan-completion score predict win rate? A portfolio-wide statistical view over `trade_reflections` completeness, `trade_plans.checklist_items` completion, and `trade_history.pnl`/`r_multiple`. Display-only, descriptive/advisory — presented as "trades with X show Y in this sample", never as a predictive signal feeding any recommendation (this distinction is sharper here than for PO-02/PO-03, since "correlation" language reads closer to a predictive claim — flagged per `arc4_e2e_test_strategy_po02_03_04.md` §4.3 item 3). Roadmap ID: `PO-04`.

**Gate condition (roadmap):** Requires PO-01 + PO-02 data; 50+ trades with plans. **Not currently met** — 20 total closed trades recorded (last confirmed 2026-07-28, per `arc4_e2e_test_strategy_po02_03_04.md` §2).

**No persisted storage proposed** — see `docs/product/arc4_data_model_pre_definition_po02_03_04.md` §3.3: this is recommended as an on-demand aggregate computed from already-stored data, not a new table, matching the existing `GET /strategy/benchmark`/`GET /analytics/strategy-version-comparison` pattern.

**Open question, not resolved by this stub** (carried from `arc4_e2e_test_strategy_po02_03_04.md` §4.3): whether the correlation calculation itself is an LLM call (Claude reasoning qualitatively about the correlation) or a plain statistical computation with an LLM only used to phrase the result in prose, if at all. This materially affects whether a real implementation needs a Claude-endpoint mock at all in its own E2E tests, or only a plain-data-endpoint mock — left to PO-04's own sprint planning.

### Request

| Param | Type | Notes |
|-------|------|-------|
| `portfolio_id` | query, string (UUID) | Standard portfolio scoping. |

### Response (proposed shape)

```json
{
  "status": "ok",
  "data": {
    "available": true,
    "insufficient_data": false,
    "sample_size": 62,
    "correlation_summary": "string"
  }
}
```

| Field | Type | Notes |
|-------|------|-------|
| `available` | boolean | `false` on AI/computation degradation, mirroring the standing convention. |
| `insufficient_data` | boolean | `true` below the 50-trades-with-plans gate — must render an explicit "insufficient data" state, never a misleading low-sample-size figure. Matches the existing `has_enough_data`/`insufficient_data` convention already used by `GET /analytics/strategy-version-comparison` and `analytics.md`'s "Empty & Null Safety" section. |
| `sample_size` | integer | The actual trade count the correlation was computed over — always present, even when `insufficient_data` is true, so the UI can show "62 of 50 needed" style progress. |
| `correlation_summary` | string | Descriptive prose, not a numeric coefficient alone — per the §13 boundary note below. |

**§13 note (display-only, sharper than PO-02/PO-03):** "correlation" language is closer to a predictive claim than a pattern-recognition summary — the eventual real contract's AC must explicitly require descriptive/advisory framing (e.g. "trades with X show Y in this sample") and must not present this as a forward-looking prediction. Not assumed resolved here; flagged for the real contract-authoring step and — per this codebase's standing pattern for AI-adjacent statistical output — worth a `BLG-SPEC-35`-style §13 check of its own rather than assuming PO-02's §13 clearance (if it lands first) automatically covers this endpoint too, since the boundary risk profile differs.

---

## Sign-off

Per `BLG-SPEC-56`'s own Owner field (Head of Specs Team):

| Role | Status | Notes |
|------|--------|-------|
| Head of Specs Team | ✅ Accepted | Agent-mediated (§5.3) — see sign-off record for ST-23 in this cycle's `execution_state.json`. Stub-only; no implementation commitment made. |
| API Contracts & Documentation Owner | ✅ Accepted | Agent-mediated (§5.3) — file lives in this role's directory and follows its conventions; co-sign alongside the AC-named Head of Specs Team, not a substitute for it. |
