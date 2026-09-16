**Owner:** QA & Testing Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-16
**Story:** ST-15 (BLG-QA-59, EPIC-03, v9.5 sprint execution)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Arc 4 E2E Test Strategy — PO-02, PO-03, PO-04

> **This document is not a feature specification or implementation commitment.** It is a pre-design reference for whoever picks up PO-02, PO-03, or PO-04 sprint planning — mirroring `docs/product/arc4_data_requirements.md`'s role for data requirements, but for E2E test approach. No PO-02/03/04 UI, endpoint, or contract exists in this codebase yet; every proposed selector, endpoint path, and fixture shape below is a **placeholder for design-time planning**, not a committed API surface. Actual endpoint paths, request/response shapes, and UI structure will be decided by each feature's own sprint planning and API-contract-authoring step, at which point this document should be revised to match reality (or superseded by real Playwright specs directly).

---

## 1. Purpose

`BLG-QA-59`: produce an E2E test strategy for Arc 4's remaining post-trade-intelligence features (PO-02 Journal Pattern Recognition, PO-03 Behavioural Error Taxonomy, PO-04 Reflection ↔ Outcome Correlation) ahead of their eventual sprint planning, and define a Claude-mocking approach for their AI calls consistent with the existing, already-approved strategy (`docs/team_skills/quality/claude_api_playwright_mock_strategy.md`, BLG-QA-37, v4.2).

**Why now, while all three remain gate-blocked:** per `docs/product/roadmap_unlock_tracker.md` (2026-08-13 confirmation), none of PO-02/03/04's gates are currently met — PO-02's 6-month AI-journal-volume gate has no formal live re-verification tracking at all (flagged there as a tracking gap), and PO-04's 50-trades gate reads 20 total closed trades, well short. Pre-designing the test strategy now means whichever of these unblocks first does not also need to design its E2E approach from a blank page under sprint-planning time pressure — the same rationale `arc4_data_requirements.md` (PO-01, v3.5) already established for data requirements one arc-feature earlier.

---

## 2. Feature Summaries and Current Gate Status

| Feature | Roadmap ID | Summary | Gate (per `current_roadmap.md` / `roadmap_unlock_tracker.md`) | Status as of this document |
|---------|-----------|---------|------|------|
| Journal Pattern Recognition | PO-02 | Cross-entry AI analysis: recurring themes, emotional patterns, setup types, conditions present at winning vs. losing entries | 6+ months of AI-summarised journal entries (`BLG-FEAT-16` — `POST /ai/journal-summary` — must be live and actively used) | `BLG-FEAT-16` is live (shipped, see §3 below); volume gate has no formal tracking field yet — flagged as a gap in `roadmap_unlock_tracker.md` §3, not confirmed met |
| Behavioural Error Taxonomy | PO-03 | Auto-classify journal entries and Plan vs Reality deviations by error type (entered too early, held too long, sized incorrectly, ignored regime, etc.); track frequency over time; feeds Arc 5 drift detection | Requires PO-01 and PO-02 data foundation | PO-01 data foundation shipped (v3.5–v3.6); PO-02 not yet built — PO-03 is transitively blocked on PO-02 |
| Reflection ↔ Outcome Correlation | PO-04 | Does journal depth correlate with trade quality? Does plan completion score predict win rate? | Requires PO-01 + PO-02 data; 50+ trades with plans | **NOT MET** — 20 total closed trades recorded (last confirmed 2026-07-28), far short of 50 |

All three are AI-invoking (journal-text analysis for PO-02, classification for PO-03, correlation analysis that may or may not require an LLM call depending on implementation — treated as AI-invoking here as the conservative assumption for mock-strategy purposes) and depend on PO-01's already-shipped data foundation to varying degrees.

---

## 3. Existing Foundation to Build On

| Asset | Location | Relevance |
|-------|----------|-----------|
| `POST /ai/journal-summary` (BLG-FEAT-16) | `backend/routers/ai.py`, `backend/services/ai_service.py::summarise_journal_notes()` | PO-02's stated gate condition; also the most likely existing endpoint PO-02 extends or reads from, rather than building a wholly separate ingestion path |
| AI journal summary UI (`TradeHistory.js`) | `src/pages/TradeHistory.js` (`data-testid="ai-journal-summary-*"`) | Existing Playwright coverage: `tests/e2e/trade-history-ai-journal-summary.spec.js` — the most direct UI precedent for where a PO-02 pattern-recognition panel would plausibly live (same page, or a linked drill-down) |
| Plan vs Reality service + UI (PO-01) | `backend/services/plan_vs_reality_service.py`, `GET /trades/{id}/plan-vs-reality`, `PlanVsReality` component | Direct architectural precedent for PO-03/PO-04: a backend calculation service producing a structured JSON record, surfaced via a dedicated frontend component with its own Playwright spec (`plan-vs-reality` scenarios in `tests/e2e/trade-plan.spec.js` region — see `regression_test_suite_baseline.md`) |
| `trade_reflections` table | `docs/specs/data_model.md` | Existing post-trade reflection data (`trade_rationale`, discipline fields) — a plausible PO-03 classification input alongside `plan_vs_reality` deviations |
| `docs/product/arc4_data_requirements.md` §3.4/§3.5 | — | `confidence_at_entry`, `deviation_note`, `thesis_confirmed`, `exit_quality` — fields flagged as required-but-not-yet-captured for PO-02/04. **These must land before PO-02/03/04 E2E tests can exercise real data paths** — this is a build-order dependency this test strategy cannot route around. |
| Existing Claude mock strategy (BLG-QA-37) | `docs/team_skills/quality/claude_api_playwright_mock_strategy.md` | The approach this document's §5 extends, not replaces |

---

## 4. Proposed E2E Test Scenarios (Pre-Design — Placeholder Endpoint Names)

Scenario IDs follow the existing `SC-<AREA>-<NN>` convention (e.g. `SC-PVR-01` for PO-01's Plan vs Reality scenarios). Proposed prefixes below are placeholders pending each feature's own sprint planning naming.

### 4.1 PO-02 — Journal Pattern Recognition (proposed `SC-JPR-*`)

| # | Scenario (proposed) | Notes |
|---|---------------------|-------|
| 1 | Pattern panel renders with `available: true` and a non-empty pattern list, given a mocked backend response | Happy path — mirrors `SC-PVR-01a`'s "renders when data present" shape |
| 2 | Pattern panel shows an empty/insufficient-data state when fewer than the gate threshold's worth of journal entries exist | Directly exercises the gate condition itself as a UI state, not just a backend check |
| 3 | Pattern panel shows the graceful-degradation message when the backend reports `available: false` (AI unavailable) | Mirrors §3.4 of the mock strategy doc (unavailable/degraded state) |
| 4 | "Advisory-only" / non-signal-feeding disclosure is visible wherever pattern output renders | Every AI-output surface in this codebase carries this per SRB-v1.7 (§13) — PO-02 is not expected to be an exception, and this should be asserted, not assumed |

### 4.2 PO-03 — Behavioural Error Taxonomy (proposed `SC-BET-*`)

| # | Scenario (proposed) | Notes |
|---|---------------------|-------|
| 1 | Error-type badges/tags render on a closed trade with a classified deviation | Precedent: `PlanVsReality` component's existing deviation display |
| 2 | Frequency-over-time view (however implemented — table or chart) renders with mocked classification data across multiple trades | If chart-based, follows `docs/skills/dataviz`-equivalent chart conventions already used elsewhere in this app (e.g. `chart-interactivity.spec.js`) |
| 3 | A trade with `plan_vs_reality` present but no journal entry still classifies (PO-01-only data path) — confirms PO-03 doesn't hard-require PO-02 data despite the roadmap's stated "requires PO-01 and PO-02" framing being about foundation *maturity*, not a literal per-trade AND requirement | Worth confirming explicitly once PO-03 is designed — flagged here as an open question, not asserted as fact |
| 4 | Zero-classified-trades empty state | Standard empty-state pattern already used throughout this app (`loading-states.spec.js`, `alert-thresholds-empty-state.spec.js` precedent) |

### 4.3 PO-04 — Reflection ↔ Outcome Correlation (proposed `SC-ROC-*`)

| # | Scenario (proposed) | Notes |
|---|---------------------|-------|
| 1 | Correlation view renders below the 50-trade gate threshold with an explicit "insufficient data" state, not a misleading/noisy correlation figure | High-priority scenario — this is exactly the kind of small-sample-size honesty issue this codebase has been burned by before (e.g. `GET /analytics/strategy-version-comparison`'s `insufficient_data` gate, §"AI Endpoint Anomaly" `MIN_*_BASELINE` noise floors elsewhere in this sprint) |
| 2 | Correlation view renders a real figure once above threshold, with the figure sourced from mocked backend data (never computed client-side from raw trade data in the test, to keep the test a UI-behaviour check, not a statistics re-implementation) | |
| 3 | Correlation claim is presented as descriptive/advisory ("trades with X show Y in this sample"), not as a predictive signal feeding any recommendation — same SRB-v1.7 boundary-language concern as PO-02, arguably sharper here since "correlation" language is closer to a predictive claim than a pattern-recognition summary is | |

**Open question flagged, not resolved, by this document:** whether PO-04's correlation calculation is itself an LLM call (Claude asked to reason about the correlation qualitatively) or a plain statistical computation the backend performs directly (with an LLM only used to phrase the result in prose, if at all). This materially affects whether PO-04 needs a Claude-endpoint mock at all, or only a plain-data-endpoint mock. §5 below covers both possibilities.

---

## 5. Mocking Approach — Extends BLG-QA-37

Per this story's AC, the mocking approach for all 3 features' AI calls must be **consistent with**, not a departure from, the existing `claude_api_playwright_mock_strategy.md` (BLG-QA-37). All conventions from that document carry forward unchanged:

- **Intercept at the backend API surface** via `page.route()`, never the Anthropic SDK (§2 of BLG-QA-37).
- **LIFO registration order** — catch-all first, specific Claude-backed endpoint mocks after (§3.1).
- **Realistic-but-clearly-fake fixture values**, prefixed `"Mock:"` where the field is free text (§4's existing rule).
- **A degraded/unavailable-state mock for every AI-invoking endpoint**, not just the happy path (§3.4).
- Mocks registered in each test file's `mockBaseEndpoints()` helper or inline, per scope, matching `playwright_patterns.md` (§6 of BLG-QA-37).

**Placeholder endpoint mocks (illustrative shape only — actual paths TBD at each feature's own contract-authoring step):**

```js
const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// PO-02 — proposed GET /journal/pattern-analysis (placeholder path)
await page.route(`${API}/journal/pattern-analysis`, async (route) => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      available: true,
      patterns: [
        { theme: 'Mock: Early exits on winning trades', trade_count: 4, sentiment: 'caution' },
        { theme: 'Mock: Consistent stop discipline on breakout setups', trade_count: 7, sentiment: 'positive' },
      ],
      model_version: 'claude-haiku-4-5',
      journal_entry_count: 24,
    }),
  });
});

// PO-03 — proposed GET /trades/{id}/error-classification (placeholder path)
await page.route(new RegExp(`${API}/trades/[^/]+/error-classification`), async (route) => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      available: true,
      error_types: ['Mock: sized_incorrectly'],
      confidence: 0.8,
    }),
  });
});

// PO-04 — proposed GET /analytics/reflection-outcome-correlation (placeholder path)
await page.route(`${API}/analytics/reflection-outcome-correlation`, async (route) => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      available: true,
      insufficient_data: false,
      sample_size: 62,
      correlation_summary: 'Mock: trades with completed pre-entry checklists show a higher realised R-multiple in this sample',
    }),
  });
});

// Insufficient-data variant (PO-04 §4.3 scenario 1) — same endpoint, gate-not-met shape
await page.route(`${API}/analytics/reflection-outcome-correlation`, async (route) => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      available: true,
      insufficient_data: true,
      sample_size: 20,
      required_sample_size: 50,
      correlation_summary: null,
    }),
  });
});
```

**Degraded-state mocks** (Claude unavailable) follow the exact §3.4 BLG-QA-37 pattern: same endpoint, `available: false`, an explanatory `error`/`message` field, HTTP 200 (not 500) — consistent with every other AI-invoking endpoint in this codebase never propagating a raw 500 for an upstream LLM failure.

**If PO-04 turns out to be plain statistics with no LLM call** (§4.3's open question): the `correlation_summary` field's mock simply becomes a static string generated by the mock, not a Claude-attributed one, and no degraded/unavailable-state mock is needed for that field specifically — the rest of this section (endpoint-level `page.route()` interception, LIFO order, realistic-fake fixtures) is unaffected either way, since it applies to backend-API mocking generally, not specifically to AI-backed endpoints.

---

## 6. Fixture Response Format (Placeholder)

| Endpoint (placeholder) | Anticipated contract file | Key fields (placeholder) |
|------------------------|---------------------------|---------------------------|
| `GET /journal/pattern-analysis` | Not yet authored — would land in a new or extended `docs/specs/api_contracts/ai_endpoints.md` section | `available`, `patterns[]`, `model_version`, `journal_entry_count` |
| `GET /trades/{id}/error-classification` | Not yet authored — likely `trade_endpoints.md`, alongside `GET /trades/{id}/plan-vs-reality` | `available`, `error_types[]`, `confidence` |
| `GET /analytics/reflection-outcome-correlation` | Not yet authored — likely `analytics_endpoints.md` if one exists, or a new file | `available`, `insufficient_data`, `sample_size`, `required_sample_size`, `correlation_summary` |

**This table must be replaced with real contract references once each feature's own API contract is authored** — per CLAUDE.md's same-commit `openapi.yaml` rule, the real contract is the source of truth from that point forward, not this pre-design placeholder.

---

## 7. Dependencies and Sequencing Notes

- PO-03 and PO-04 are both transitively gated on PO-02 shipping first (PO-03 explicitly; PO-04 on "PO-01 + PO-02 data foundation"). Test-strategy pre-design for PO-03/PO-04 is therefore necessarily more speculative than PO-02's — flagged throughout §4.2/§4.3 rather than presented with false confidence.
- The §3.4/§3.5 data-capture gaps in `arc4_data_requirements.md` (`confidence_at_entry`, `deviation_note`, `thesis_confirmed`, `exit_quality`) are a build-order prerequisite, not merely a nice-to-have — several of the scenarios in §4 assume these fields exist. Whoever picks up PO-02 sprint planning should re-check `arc4_data_requirements.md`'s status before assuming this test strategy's scenarios are directly implementable.
- This document does not attempt to pre-design PO-05 (Lightweight Replay Mode) — that feature's own gate (IT-06 Alpaca paper trading, already shipped) and shape are sufficiently different (a replay/simulation surface, not an AI-text-analysis surface) that its mock strategy is unlikely to extend BLG-QA-37 in the same way; out of this story's scope (PO-02/03/04 only, per AC).

---

## 8. Director of Quality Sign-Off

- Signed off by: Director of Quality (agent-mediated, QA & Testing Owner role — §5.3)
- Date: 2026-09-16
- Comments: Mocking approach (§5) correctly extends BLG-QA-37 without deviating from any of its established conventions (backend-API-level interception, LIFO registration, realistic-fake fixtures, mandatory degraded-state mocks) — consistency confirmed by direct side-by-side comparison against `claude_api_playwright_mock_strategy.md`. Proposed scenarios (§4) and placeholder endpoint shapes (§5, §6) are clearly and repeatedly labelled as pre-design placeholders, not committed contracts, avoiding the risk of this document being mistaken for an authoritative spec by a future reader. Open questions (PO-03 per-trade data requirement, PO-04 LLM-vs-statistics implementation) are correctly flagged rather than silently assumed. Build-order dependency on `arc4_data_requirements.md`'s uncaptured fields is explicitly surfaced (§7), preventing this document from implying PO-02/03/04 test scenarios are implementable today. No gaps identified for a pre-design document of this kind.
