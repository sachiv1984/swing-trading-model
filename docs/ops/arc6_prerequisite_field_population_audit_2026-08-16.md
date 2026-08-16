**Owner:** Data Model & Domain Schema Owner; QA & Testing Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-16
**Story:** ST-18 (BLG-QA-140, EPIC-04, v8.8)

# Arc 6 Prerequisite Field Population Completeness Audit

## 1. Purpose

Arc 6 features (PS-01–05, `current_roadmap.md` §5) require `trade_plans.regime_context_at_entry` and `trade_plans.setup_type` to be populated on every new trade before the 50/100-trade gates are reached, so the eventual Edge Analysis / Regime-Conditional Performance / Monte Carlo / Strategy Decay views have complete data to work with. No audit had previously confirmed population completeness ahead of those gates. This closes that gap.

## 2. Method

Two-part audit, per the constraints of this session (sandboxed execution — see §3 for the live-data caveat):

1. **Live data check** — `GET /trade-plans` against the production API (`https://trading-assistant-api-c0f9.onrender.com`, no authentication required for this endpoint) to measure actual current population.
2. **Code-path analysis** — traced every write path that can set `regime_context_at_entry` or `setup_type` on `trade_plans`, to assess whether population is structurally guaranteed going forward, not just true of today's snapshot.

## 3. Live Data Finding

`GET /trade-plans` (production, 2026-08-16): **0 rows**. Production currently has zero trade plans — this session found no historical rows to compute a population percentage against. (`GET /trades` and `GET /positions` returned `401 Unauthorized` — no credential available in this session to check executed-trade volume by comparison; the `/trade-plans` result alone is sufficient to confirm there is currently nothing to audit for population *rate*, so the remainder of this audit is a forward-looking code-path assessment instead.)

This itself is a notable data point: Arc 6's 50/100-trade gates (and the nearer SI-02 gate, per `roadmap_unlock_tracker.md`) are far from met by trade-plan volume alone, independent of field completeness — consistent with prior rebalance findings (`decision_log.md`: "0/11 linked trade_plans" as of the last live re-check this cycle, referring to `position_id` linkage rather than these two fields specifically, and likely against a different environment/point in time than this zero-row snapshot).

## 4. Code-Path Analysis

### 4.1 `regime_context_at_entry` — structurally near-guaranteed

- `POST /trade-plans` (`backend/routers/trade_plans.py`) accepts it as an `Optional[str]` request field — **not server-derived**, purely client-supplied.
- The only production write path is `TradePlan.js` (`src/pages/TradePlan.js:597`): `regime_context_at_entry: form.regime_context_at_entry || regimeFromHealth || null`. `regimeFromHealth` (line 384) derives from `GET /market/status` with a 3-level fallback chain: `healthData.data.regime_status` → `healthData.regime_status` → SPY/FTSE `is_risk_on` flag by market. The field is also rendered read-only in the form UI (line 761) — the user cannot blank it out once the health fetch succeeds.
- **Population is only at risk if `GET /market/status` itself returns no usable regime data at the moment of plan creation** (a live-data outage, not a code gap). No code path creates a trade plan through the UI while silently skipping this field.
- `behavioural_drift_service.py` and `si02_drift_score.md` already treat `NULL` here as `"neutral"` (not a violation) specifically to account for pre-feature-era rows — confirming this is a known, already-handled legacy-data case, not an active gap.
- **Assessment: no gap found.** No fix or backlog filing needed for this field.

### 4.2 `setup_type` — real, disclosed gap

- Also `Optional[str]`, client-supplied, **no server-side default**.
- `TradePlan.js` renders it as a free-choice `<select>` (line 842-843) defaulting to blank (`value={form.setup_type || ""}`).
- The **only** code path that pre-populates a value is the linked-watchlisted-signal pre-population effect (line 495-508): when a plan is created from a ticker with a matching `watchlisted` signal, `setup_type` defaults to `"Momentum Continuation"` if not already set. **Any trade plan created without a linked watchlisted signal — the majority of realistic creation paths (manual entry from Ticker Universe, Research page CTA with no matching signal, direct API use) — has no default and will save `setup_type: null` unless the user manually selects one.**
- `ai_thesis_generation.md`/`gemini_service.py` already treat a missing value as `"Not specified"` for thesis-generation prompt purposes — but that fallback string is not one of the 6 canonical `setup_type` enum values (`trade_plan_endpoints.md`: `Breakout | Pullback to MA | Momentum Continuation | Mean Reversion | Catalyst-driven | Other`), so it would not group meaningfully in a future `win_rate_by_setup_type` query (`si02_query_predesign.md` §pre-design queries) — a null/unclassified row would simply be excluded or bucketed separately, undercounting the classified sample.
- **Assessment: real completeness gap for Arc 6/SI-02's `win_rate_by_setup_type` query.** Not fixed directly in this audit — the right fix (should `setup_type` become a required field at submission, or should an explicit "Unclassified" enum value be added so it groups predictably rather than nulling silently?) is a product/UX decision outside this audit's S-effort scope, not a mechanical code change. Filed as `BLG-QA-150` (see §5) for Product Owner / Frontend Specifications & UX Documentation Owner disposition.

## 5. Gaps Filed

| Ref | Field | Gap | Disposition |
|-----|-------|-----|-------------|
| BLG-QA-150 | `trade_plans.setup_type` | No default/required-field guarantee outside the linked-signal pre-population path; plans created any other way save `null`, undercounting future Arc 6 `win_rate_by_setup_type` analysis | Filed — Product Owner / Frontend Specifications & UX Documentation Owner to decide requirement-vs-default treatment |

No gap filed for `regime_context_at_entry` — code path already guarantees population outside of a live external-data outage, which is an operational condition, not a completeness defect.

## 6. Sign-Off

- [x] Live data checked (production `GET /trade-plans`, 2026-08-16 — 0 rows, disclosed as a finding in its own right)
- [x] Both named prerequisite fields' write paths traced end-to-end
- [x] Gap found (setup_type) filed, not silently accepted
- Signed off by: PENDING — see agent-mediated review
- Date: PENDING
