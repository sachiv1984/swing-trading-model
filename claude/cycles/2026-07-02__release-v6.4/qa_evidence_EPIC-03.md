Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-02

# QA Evidence — EPIC-03 (Strategy Benchmark Enhancement & UX/QA Polish)

**EPIC:** EPIC-03 — Strategy Benchmark Enhancement & UX/QA Polish
**Cycle:** 2026-07-02__release-v6.4
**Sprint goal:** Deliver v6.4's mandatory production correctness fix, AI prompt-injection security hardening, full AUD-2026-07-01 lifecycle-audit remediation, and the Strategy Benchmark Open Positions panel (with accessibility contrast and Playwright coverage fixes) in a single sealed sprint.
**Test scenarios used:** `tests/e2e/epic02-v62-ai-briefing-chat.spec.js` (SC-AC-06, new — ST-10), `tests/e2e/trade-history-ai-journal-summary.spec.js` (new — ST-12), `tests/e2e/strategy-benchmark.spec.js` (new — ST-13)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-08 | `docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md`, `docs/specs/frontend/pages/strategy_benchmark.md`, `docs/specs/api_contracts/strategy_benchmark_endpoints.md`, `docs/reference/openapi.yaml` | New "Open Positions" Panel 0 on the Strategy Benchmark page (rendered only when ≥1 unrealized position exists, sorted by unrealized P&L% descending, independent loading/error state). New `backtest_open_positions` table (fully replaced, not upserted, on each nightly import — same pattern as `backtest_trades`). New `GET /strategy/benchmark/open-positions` endpoint (market filter only, no year). `import_backtest.py` now parses the "Open (Unrealized)" CSV rows it previously discarded. | AC-01 (panel renders conditionally with summary + table): Pass with notes — code review only, no Playwright coverage this sprint; backlog item TEST-GAP-EPIC-03-v64 filed before this PR opened, per CLAUDE.md §2. AC-02 (realized aggregates unaffected): Pass — `backtest_open_positions` is a fully separate table/query path from `backtest_trades`/`get_backtest_summary`; verified via code review. AC-03 (table fully replaced, not upserted): Pass — `upsert_backtest_data()` DELETEs `backtest_open_positions` before each import, same pattern as the existing two tables. AC-04 (endpoint ships with openapi.yaml, contract doc, test.py registration): Pass — all three shipped in the same commit; `backend/routers/test.py` now has 82 entries; `SystemStatus.js` fallback and `system-status.spec.js` SC-SS-01b updated to match. | Pass with notes | None (backlog item filed for the Playwright gap, not a spec deviation) |
| ST-09 | `docs/specs/qa/ai_disclaimer_visibility_assessment.md` | `AiDailyBriefing.js` disclaimer text `text-slate-500` → `text-slate-300`. Badge and layout unchanged. | AC-01 (contrast ≥4.5:1): Pass — matches the QA assessment's precomputed remediation class exactly. AC-02 (no visual regression): Pass — single class change, verified via code review. AC-03 (Head of UX & Design sign-off): Pass — agent-mediated, Approved, no findings. | Pass | None |
| ST-10 | `docs/specs/qa/ai_disclaimer_visibility_assessment.md`, `tests/e2e/epic02-v62-ai-briefing-chat.spec.js` | `AiChatWidget.js` footer disclaimer `text-slate-600` → `text-slate-400`; `data-testid="ai-chat-advisory-footer"` added. New Playwright test `SC-AC-06`. | AC-01 (contrast ≥4.5:1): Pass — matches QA assessment's remediation class. AC-02 (`data-testid` present): Pass. AC-03 (Playwright test asserts visibility + "advisory" text): Pass — `SC-AC-06`. AC-04 (Head of UX & Design sign-off): Pass — agent-mediated, Approved, no findings. | Pass | None |
| ST-11 | `docs/ops/api_performance_baseline.md` | Registered `GET /strategy/benchmark/summary`, `GET /strategy/benchmark/trades`, `GET /health/scheduler` in new §23. Staging returned 404 for all three (v6.3 not yet deployed there); measured live against production instead (5 warm samples each). | AC-01 (p50/p95 measured, min 5 warm requests): Pass — deviated from the sprint-planning assumption of "staging-only/deferred": production was live and had all 3 endpoints, so a real measurement was taken this sprint instead of deferring. summary p50=970.1ms p95=972.7ms; trades p50=1,198.1ms p95=1,240.3ms; health/scheduler p50=76.2ms p95=161.8ms. AC-02 (regression thresholds documented): Pass — §22.2/§22.3 dynamic 2x-p95 pattern applied per endpoint. AC-03 (Infrastructure & Operations Owner sign-off): Pass — agent-mediated, Approved after 1 revision round (2 citation-accuracy findings corrected: precedent section and threshold-methodology section). | Pass | None (2 citation corrections applied during agent-mediated review, not spec deviations) |
| ST-12 | `tests/e2e/trade-history-ai-journal-summary.spec.js` | New `data-testid` selectors added to the Trade History tab's AI Journal Summary component (none existed previously). New Playwright spec covering server-error and network-error message rendering. | AC-01 (specific error message on unavailable summary): Pass — `SC-TH-AI-01`. AC-02 (server-error and network-error message rendering): Pass — `SC-TH-AI-01`/`SC-TH-AI-02`. AC-03 (tests reference `data-testid` selectors on the component): Pass — all 3 new tests use the new testids. | Pass | None |
| ST-13 | `tests/e2e/strategy-benchmark.spec.js` | New Playwright spec covering the pre-existing v6.3 Strategy Benchmark page gap (Panels 1 and 3 only, per sprint scope — Panel 0 from ST-08 excluded, tracked separately via `TEST-GAP-EPIC-03-v64`). | AC-01 (page accessible from navigation): Pass — `SC-SB-01`. AC-02 (Year + Market filters apply simultaneously): Pass — `SC-SB-02`. AC-03 (Panel 1 "—" placeholder for null `actual_stats`): Pass — `SC-SB-03`. AC-04 (Panel 3 toggle modes + exit reason badge colours): Pass — `SC-SB-04`. AC-05 (tests in `tests/e2e/strategy-benchmark.spec.js`): Pass. | Pass | None |

*(Each row's Result column covers all listed ACs for that story; per-AC detail is inline given the small number of ACs per story this EPIC.)*

**QA test coverage:**
- Scenarios run (new/modified this EPIC): `SC-AC-06` (chat footer disclaimer), `SC-TH-AI-01/02/03` (AI journal summary error/success states), `SC-SB-01/02/03/04` (Strategy Benchmark page — Panels 1/3, filters, navigation).
- Regression areas checked: Strategy Benchmark realized-metric isolation (Panel 0 vs Panels 1/2 — no shared aggregates), API performance regression thresholds for 3 newly-registered endpoints, `backend/routers/test.py` endpoint count parity with `SystemStatus.js`/`system-status.spec.js`.
- Known deviations filed: None. One backlog item filed (`TEST-GAP-EPIC-03-v64`) for a deferred Playwright gap — this is the CLAUDE.md §2 backlog-item pathway operating as designed, not a spec deviation.

**Cross-spec selector check (SC-06):** ST-08 and ST-12 both added `data-testid` attributes to existing components (`StrategyBenchmark.js`, `TradeHistory.js`) without renaming or removing any existing DOM element — no stale-selector scan was required for either story.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, all API calls in this EPIC go through `api.strategyBenchmark.*` / `apiFetch()` wrappers
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-07-02
- Comments: EPIC-03 is not eligible for the BLG-GOV-19 autonomous class — it introduces frontend-visible changes under `src/pages/**` and `src/components/**` (ST-08, ST-09, ST-10), which automatically disqualifies criterion 3 (BLG-GOV-135 detection rule) regardless of Playwright coverage. Standard sign-off applied via agent-mediated Director of Quality review (§5.3) of the consolidated evidence above, including the story-level Head of UX & Design (ST-09, ST-10) and Infrastructure & Operations Owner (ST-11) sign-offs. One observable AC (ST-08/AC-01) uses the CLAUDE.md §2 backlog-item pathway (`TEST-GAP-EPIC-03-v64`, filed before this PR opened) rather than Playwright coverage or a staging run — confirmed correctly filed and referenced.

## Reclassification Counter-Sign (BLG-GOV-14 / LL-v2.3-EX-02)

ST-08, ST-09, and ST-10 were all originally classified `delegated_frontend` in `sprint_backlog.md`/`execution_state.json` and were reclassified to `autonomous` mid-sprint per LL-v2.3-CL-01 (engine completed each directly; no delegation record was ever created for any of the three). Because EPIC-03 as a whole introduces frontend-visible changes, the autonomous-class sign-off above is insufficient on its own for this EPIC per the reclassification counter-sign rule — a second, explicit Director of Quality counter-sign is required in addition to the engine sign-off block above.

- Counter-signed by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-07-02
- Comments: Reviewed all three reclassifications (ST-08 §5.1, ST-09/ST-10 same pattern) — each has an execution_state.json note documenting the reclassification reason and, for ST-09/ST-10, a separate story-level Head of UX & Design sign-off already on record. No delegation log entries required cancellation (none were ever created). Counter-sign: Approved.
