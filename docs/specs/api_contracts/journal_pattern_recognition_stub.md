# Journal Pattern Recognition — Arc 4 PO-02 (Pre-Authoring Stub)

**Version:** 0.1.0 (stub — not implemented)
**Last Updated:** 2026-09-18
**Spec Owner:** API Contracts & Documentation Owner
**Governed by:** docs/specs/api_contracts/conventions.md
**Story:** ST-23 (BLG-SPEC-56, EPIC-04, v9.5 sprint execution)

---

> **This is a pre-authoring stub, not a canonical contract.** No `PO-02` endpoint exists in `backend/routers/` and no entry for it exists in `docs/reference/openapi.yaml` — both correctly absent, since nothing has been built yet. Headings below intentionally do **not** use the canonical `## METHOD /path` form (see `CLAUDE.md` §2 / `scripts/openapi_3way_drift_sweep.py`) so this stub is not picked up by the OpenAPI Drift Detection gate as a documented-but-missing endpoint. When PO-02 is actually built, its real contract entry must use the canonical `## GET /journal/pattern-analysis` form in this same file (or a renamed non-stub file) with a matching `openapi.yaml` entry added in the same commit, per `CLAUDE.md` §2.
>
> Path, method, and field names below are **placeholders for design-time planning** — chosen to match `docs/qa/arc4_e2e_test_strategy_po02_03_04.md` §4.1's already-published mock fixture shape, not a committed API surface. Revise or supersede at PO-02's own sprint planning / contract-authoring step.

---

## Proposed — GET /journal/pattern-analysis

**Gate:** Blocked on `BLG-SPEC-35`'s §13 boundary review (P1, still open as of this session — see backlog) — this endpoint must not ship until that review passes. This stub does not attempt to resolve §13 itself; it documents the shape a passing design would plausibly take, per that review's own binding-conditions pattern (analogous to IT-06's §13 PASS conditions).

**Description:** Cross-journal-entry AI analysis surfacing recurring themes across a portfolio's AI journal entries (`ai_journal_entries`, externally-provisioned — see `data_model.md`). Display-only, advisory — never feeds a signal, recommendation, or automated action. Roadmap ID: `PO-02`.

**Gate condition (roadmap):** 6+ months of AI-summarised journal entries (`POST /ai/journal-summary`, `BLG-FEAT-16`, must be live and actively used). Per `docs/product/roadmap_unlock_tracker.md`, this has no formal live-verification tracking field yet — flagged there as a pre-existing gap, not something this stub resolves.

### Request

| Param | Type | Notes |
|-------|------|-------|
| `portfolio_id` | query, string (UUID) | Standard portfolio scoping, matching existing endpoints' convention. |

### Response (proposed shape)

```json
{
  "status": "ok",
  "data": {
    "available": true,
    "patterns": [
      { "theme": "string", "trade_count": 4, "sentiment": "caution | positive | neutral" }
    ],
    "model_version": "string",
    "journal_entry_count": 24
  }
}
```

| Field | Type | Notes |
|-------|------|-------|
| `available` | boolean | `false` when the gate condition is unmet or the AI call degrades — mirrors the existing `available`/graceful-degradation convention used by other AI-invoking endpoints (`docs/team_skills/quality/claude_api_playwright_mock_strategy.md` §3.4). |
| `patterns` | array of objects | Kept schemaless at the storage layer (`journal_pattern_analyses.patterns` JSONB — see `docs/product/arc4_data_model_pre_definition_po02_03_04.md` §3.1); this response shape is this stub's proposal for how that JSONB should be structured on read, not a commitment. |
| `model_version` | string | AI provenance, per this codebase's standing per-record model/prompt-version convention. |
| `journal_entry_count` | integer | The journal volume the analysis was run over — lets the frontend distinguish "thin but real" pattern sets from richly-supported ones. |

**§13 note (display-only):** per every other AI-output surface in this codebase (SRB-v1.7), the eventual real contract must carry an explicit advisory-only disclosure requirement in its AC — not assumed here, flagged for the real contract-authoring step.

### Data model reference

`journal_pattern_analyses` table (proposed, not created) — see `docs/product/arc4_data_model_pre_definition_po02_03_04.md` §3.1.

---

## Sign-off

Per `BLG-SPEC-56`'s own Owner field (Head of Specs Team):

| Role | Status | Notes |
|------|--------|-------|
| Head of Specs Team | ✅ Accepted | Agent-mediated (§5.3) — see sign-off record for ST-23 in this cycle's `execution_state.json`. Stub-only; no implementation commitment made. |
| API Contracts & Documentation Owner | ✅ Accepted | Agent-mediated (§5.3) — file lives in this role's directory and follows its conventions; co-sign alongside the AC-named Head of Specs Team, not a substitute for it. |
