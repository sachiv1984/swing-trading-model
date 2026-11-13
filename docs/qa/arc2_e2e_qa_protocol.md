**Owner:** QA Lead; Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-11-13 (ST-11, EPIC-05, v9.17, BLG-BE-211 — M-04 expects the plan `closed` after a full exit; §6 row marked fixed); prior — 2026-11-10 (ST-24, EPIC-06, v9.16, BLG-QA-21 — initial arc-level protocol)
**Cycle:** 2026-11-06__release-v9.16 (ST-24 — BLG-QA-21)

---

# Arc 2 Pre-Trade Research & Planning — Arc-Level QA Protocol

## 1. Purpose

This is the arc-level QA protocol for Arc 2 (Pre-Trade Research & Planning), required by `BLG-QA-21`. Arc 2's features were each tested on their own as they shipped (v3.1–v6.1), and later cycles added to the flow (Signal Context v9.x, "Plan this" and the suggested size in v9.16). No document walked the whole flow until now.

This protocol:

- lists the Arc 2 features and the Playwright files that cover each one (§2, §3)
- defines the arc-level happy path and the two Playwright tests that automate it end to end (§4)
- gives a manual checklist for the edge cases Playwright does not cover, because they need the real backend, real data or a person's judgement (§5)
- records the defects found while writing it (§6)

It references the feature-level scenario tables rather than copying them. The house format follows `docs/qa/arc5_qa_protocol.md`.

---

## 2. Arc 2 Feature Inventory

Source: `claude/roadmap/current_roadmap.md` §2c, Arc 2 (✅ Fully Complete). The arc's entry surface, the Screener, is Arc 1's (SC-01); it is included because the arc's flow starts there.

| ID | Feature | Shipped | Page / component | Spec |
|----|---------|---------|------------------|------|
| (Arc 1) | Screener and Signals as the flow's entry | v2.x–v3.0 | `Screener.js`, `Signals.js` | `screener_results.md`, `signals.md` |
| PT-01 | Trade Plan object | v3.1 | `TradePlan.js`, `TradePlans.js` | `trade_plan.md`, `trade_plan_endpoints.md` |
| PT-02 | Pre-Trade Research View | v3.2 | `Research.js` (`/research/:ticker`) | `pre_trade_research.md`, `research_view.md` |
| PT-03 | Prospective heat at entry | v3.2 | Research View heat region | `pre_trade_research.md` |
| PT-04 | Setup Quality Score | v6.1 | `SetupQualityScorePanel` (Research View and Trade Plan) | `trade_plan_endpoints.md` §setup-quality-score |
| PT-05 | Pre-trade entry checklist | v3.x | `EntryChecklist` (Trade Plan) | `trade_plan.md` |
| — | Later additions to the flow: Signal Context panel, "Plan this", suggested size before shares, Start Trade from Plan, Plan vs Reality (Arc 4, the flow's end) | v7.3–v9.16 | `TradePlan.js`, `TradeEntry.js`, `PlanVsReality.js` | `trade_plan.md` v1.23 §2, §5a.1, §5f, §10 |

---

## 3. Feature-Level Playwright Coverage

All files are in `tests/e2e/` and run in the blocking Playwright CI job. Counts are `test(` calls in the file at 2026-11-10; theme loops run some tests twice.

| Stage | Files (tests) |
|-------|---------------|
| Screener / Signals entry | `screener.spec.js` (24), `screener-quality.spec.js` (5), `screener-uk-suffix.spec.js` (4), `screener-watchlist-csv-export.spec.js` (9), `plan-this.spec.js` (8), `watchlist.spec.js` (6), `watchlist-staleness-review.spec.js` (5) |
| Research View (PT-02, PT-03) | `pre-trade-research.spec.js` (16, incl. SC-RES-05/06 heat), `research-view-signal-type.spec.js` (4), `research-trade-plan-status-badge.spec.js` (2), `research-typography.spec.js` (5) |
| Setup Quality Score (PT-04) | `setup-quality-score.spec.js` (9: value, label, gate-not-met, expanded detail, ticker change) |
| Trade Plan (PT-01, PT-05) | `trade-plan.spec.js` (46), `entry-checklist.spec.js` (11), `trade-plan-signal-context.spec.js` (4), `trade-plan-suggested-size.spec.js` (7), `trade-plan-clone.spec.js` (9), `trade-plan-stale-marker.spec.js` (5), `trade-plan-tag-filter.spec.js` (5), `trade-plan-invalidation-link-toast-ai-badge.spec.js` (6) |
| Plan → position | `trade-plan-linkage-advisory.spec.js` (3), `setup-thesis-digest.spec.js` (4), `trade-entry-pre-entry-checks.spec.js` (15) |
| Plan vs Reality (Arc 4 end of flow) | `plan-vs-reality.spec.js` (12) |
| **Arc-level journeys (§4)** | `arc2-happy-path.spec.js` (1), `trade-plan-lifecycle.spec.js` (1) |

Every feature-level file mocks one page in isolation. Before this protocol, no test carried a plan from one page to the next, so a broken hand-off (for example Trade Entry not sending `trade_plan_id`) would pass every file above.

---

## 4. Arc-Level Happy Path

### 4.1 Flow

```
A1  Screener row ── "Research" ──▶ Research View (PT-02): signal, regime, heat (PT-03), quality score (PT-04)
A2  Research View ── "Create Trade Plan" ──▶ Trade Plan: quality score shown; entry + stop → suggested size → shares
A3  Trade Plan: thesis, R target, completed entry checklist (PT-05) ── Save ──▶ plan `draft`
A4  Research View shows the plan (Draft badge, "View full plan")
A5  Trade Plans ── "Start Trade" ──▶ Trade Entry pre-filled ── Create Position ──▶ plan `active`, position_id set
A6  Positions ── Exit ──▶ trade written
A7  Trade History ── expand ──▶ Plan vs Reality (R achieved vs target, entry delta, adherence, state at exit)
```

The alternative entry, Signals "Plan this" → Trade Plan pre-filled with the signal's entry price and Signal Context, joins at A2.

### 4.2 Automation

| Test | Covers | Notes |
|------|--------|-------|
| `tests/e2e/arc2-happy-path.spec.js` — SC-ARC2-01..05 | A1–A5 from the Screener | Asserts the saved plan's checklist items, thesis, R target and suggested shares, and the `draft` → `active` link |
| `tests/e2e/trade-plan-lifecycle.spec.js` — SC-TPL-01..05 (ST-26) | Signals "Plan this" → A2, A3, A5, A6, A7 | Asserts quality score on create and on reopen, the link, the exit, and Plan vs Reality values worked by hand |

Both tests drive the real UI against one stateful mock backend, `tests/e2e/mocks/trade-plan-lifecycle-backend.js`. Its write handlers copy the backend's rules: initial stop = entry − 5×ATR; an explicit `trade_plan_id` links the plan and sets `active`; the exit snapshots `planned_entry_price` from the ticker's signal; Plan vs Reality is a port of `plan_vs_reality_service.py`, whose formulas are unit-tested in `tests/test_plan_vs_reality.py`.

**What the automation does not prove:** that the real backend performs those writes. A mock that copies a rule cannot catch the backend breaking it. The write-through checks are in §5.1 and need staging.

### 4.3 When to run

- Every PR: both tests run in the blocking Playwright job.
- Arc-level regression (a change to any page in §2, or to the plan, position or trade endpoints): run both, then §5.1 on staging.

---

## 5. Manual Checklist — Edge Cases Not Covered by Playwright

Run on staging with a test portfolio. Record the date, tester and result per row in the QA evidence of the change being verified.

### 5.1 Backend write-through (needs the real API and database)

| # | Check | Expected |
|---|-------|----------|
| M-01 | Create a plan, Start Trade, Create Position | `trade_plans.position_id` set, `status = 'active'`; Trade Entry toast "Linked to trade plan for {TICKER}." |
| M-02 | Enter a position **without** Start Trade for a ticker that has one unlinked pre-entry plan | The plan auto-links (`get_unlinked_trade_plan_for_entry`); with no such plan the toast reads "No matching plan found — logged unlinked." |
| M-03 | Same as M-02 with **two** unlinked plans for the ticker | Exactly one links: the most recently created pre-entry plan (`ORDER BY created_at DESC LIMIT 1`) |
| M-04 | Fully exit the linked position | A `trade_history` row exists; Plan vs Reality returns 200. Plan status is `closed` and Trade Plans shows the "Closed" badge (fixed v9.17, ST-11, BLG-BE-211) |
| M-05 | Partially exit the linked position | A `trade_history` row is written for the exited shares and has its own Plan vs Reality; the position and the plan stay open/`active` |
| M-06 | Plan vs Reality for the closed trade | R achieved = (exit − entry) / (entry − initial stop); R target from the plan; stop discipline against the plan's stop. Entry delta: **known gap** (§6, BLG-BE-212) |

### 5.2 Data conditions

| # | Check | Expected |
|---|-------|----------|
| M-07 | Quality score for a ticker with < 20 closed trades | "Insufficient trade history (< 20 trades)" with the count; no score |
| M-08 | Quality score after a new trade on the ticker closes | The score is recomputed (it is not stored on the plan); a reopened plan shows the new value |
| M-09 | Research View for a UK ticker (`.L`), then "Create Trade Plan" | The plan's market is UK and amounts are in £. **Known gap — opens as US** (§6, BLG-FE-281) |
| M-10 | Suggested size when cash is short, and when the stop is above the entry | "Max affordable: … shares" / "Stop price must be below entry price"; shares not pre-filled |
| M-11 | Research View with earnings inside 7 days | Earnings proximity is shown; the checklist does not tick itself |
| M-12 | Research View when the prospective-heat call fails | Heat shows N/A; the rest of the page renders (SC-RES-06 covers the UI; check the real error path once) |

### 5.3 Judgement checks

| # | Check | Expected |
|---|-------|----------|
| M-13 | "Improve with AI" / generate thesis on a real ticker | Text is relevant, stays inside `strategy_rules.md` §13 (no buy/sell instruction), and is marked as an AI draft |
| M-14 | Walk A1–A7 once on a phone-width screen | Every step reachable without horizontal scrolling; buttons usable |
| M-15 | Walk A1–A7 in the light and the dark theme | All text readable; status badges distinguishable |

---

## 6. Defects Found While Writing This Protocol

| ID | Finding | Effect on this protocol |
|----|---------|-------------------------|
| `BLG-BE-211` (P2) | No backend code moves a linked plan from `active` to `closed` when its position closes, although `data_model.md` §Trade Plan Lifecycle says it does | Fixed v9.17 (ST-11): a full exit closes the linked plan; M-04 and the lifecycle test (SC-TPL-04) assert `closed` and the "Closed" badge |
| `BLG-FE-281` (P2) | Research View's "Create Trade Plan" passes only `ticker`, so the plan's market defaults to US; a UK ticker's plan is sized and priced as US | M-09 records the gap |
| `BLG-BE-212` (P3) | `trade_history.planned_entry_price` is snapshotted at exit from the ticker's current signal price, not from the plan's `planned_entry_price`, so Plan vs Reality's entry delta measures the fill against a later signal price (and is null when no signal exists) | M-06 records the gap; the lifecycle test asserts the formula as built |

---

## 7. Change Log

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2026-11-10 | Initial arc-level protocol (ST-24, BLG-QA-21) | QA Lead (Sprint Execution Engine) |
