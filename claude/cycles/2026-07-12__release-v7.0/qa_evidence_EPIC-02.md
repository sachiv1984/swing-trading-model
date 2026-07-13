Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-13

# QA Evidence — EPIC-02 (v6.9 Carryover Fixes & Reconciliation)

**Cycle:** 2026-07-12__release-v7.0
**Sprint goal:** Close the Grid View/Table View position-risk badge and trailing-stop parity gap, resolve the v6.9-carried spec-reconciliation and data-correctness debt, and ship three new reporting and position-review features.

---

## ST-06 — Reports.js Tax Year P&L tab spec reconciliation (BLG-SPEC-71)

**Spec reference:** `docs/specs/frontend/pages/reports.md` (v0.7→v0.8)
**Commit:** 7f414052
**What was built:** Reconciled §Arc 5 Compliance Summary and §Gross vs Net Comparison to explicitly document "Design Only — Implementation Pending" — both had changelog entries worded as shipped features but were confirmed (via `git log -S`) never actually rendered in `Reports.js`. Documentation-only change, no code touched.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| AC-01: reports.md's description of the Tax Year P&L tab matches what Reports.js actually renders | Pass — both sections now explicitly marked pending, matching actual code |
| AC-02: If sections are subsequently implemented, Playwright coverage added per CLAUDE.md rule | Pass (forward-looking rule documented; N/A this sprint — no implementation) |
| AC-03: Root cause documented | Pass — restated inline in v0.8 changelog entry, full investigation already on file in BLG-SPEC-71 |

**Deviations:** None

---

## ST-07 — Instrument trailing-stop recommendation capture for trailing_stop_action_rate metric (BLG-BE-50)

**Spec reference:** `docs/specs/metrics_definitions.md#Trailing Stop Action Rate`
**Commit:** 9683319c
**What was built:** `trailing_stop_recommendation_log` table (exact DDL from spec) + `database.log_trailing_stop_recommendation()`, wired fire-and-forget into `GET /positions/{id}/stop-trail` (`backend/main.py`). Capture window (24h) confirmed by Product Owner delegated authority at sprint planning.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| `trailing_stop_recommendation_log` table created and populated on every `GET /positions/{id}/stop-trail` call | Pass |
| `trailing_stop_action_rate` computable via the query approach documented in `metrics_definitions.md` | Pass — join against `positions.stop_price`/`updated_at` documented, no new schema needed on PATCH side |
| Capture window (24-hour proposal) confirmed by Product Owner | Pass — delegated authority, recorded in sprint_backlog.md Outstanding Actions |

**Test scenarios:** `tests/test_trailing_stop_recommendation_log.py` (5 tests, all passing)

**Deviations:** None

---

## ST-08 — Dashboard/StrategyBenchmark page-title light-theme contrast gap (BLG-FE-95)

**Spec reference:** `docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md`
**Commit:** a3e441fb (fix), 62e2721f (Playwright coverage)
**What was built:** `text-white` → `text-slate-900 dark:text-white` on `DashboardHome.js` and `StrategyBenchmark.js` `<h1>` headings, per the locked design decision record. No layout/sizing change.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| Both named headings pass WCAG AA contrast (≥4.5:1) against both light and dark backgrounds | Pass — `text-slate-900` on `bg-slate-100` ≈17.9:1, `text-white` on dark unchanged ≈19:1, both AAA |
| No visual change on dark theme | Pass — dark-theme value (`text-white`) unchanged, verified by SC-HTC-01/03 |

**Test scenarios:** `tests/e2e/heading-light-theme-contrast.spec.js` (4 scenarios, all passing, verified locally)

**Deviations:** None

---

## ST-09 — Positions Table View breach badge does not match approved spec colour/label (BLG-FE-96)

**Spec reference:** `docs/specs/frontend/pages/positions.md#Trailing Stop Column`
**Commit:** 479c005a
**What was built:** Breach badge in `Positions.js` changed from `bg-rose-800/80 text-rose-200`/"Breach" to `bg-orange-600 text-white`/"⚠ BREACH" (`#EA580C` = Tailwind orange-600, confirmed exact hex match), `rounded-full` pill shape, `aria-label` added per spec text. `data-testid="breach-badge"` added for selector robustness (cross-spec selector check, LL-v3.2-P3-02) — existing selectors in `tests/e2e/epic01-v62-stops-alerts.spec.js` updated in the same commit.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| Breach badge renders with `#EA580C` background and "⚠ BREACH" label, matching positions.md §Trailing Stop Column | Pass |
| No other Table View styling changed | Pass — only the breach badge itself touched |

**Test scenarios:** `tests/e2e/epic01-v62-stops-alerts.spec.js` (16 scenarios updated/re-verified, all passing)

**Cross-EPIC note:** `tests/e2e/epic01-v70-grid-badge-parity.spec.js` (EPIC-01, PR #968, not yet merged at time of this commit) contains `SC-GVP-09`, which also asserts the pre-ST-09 breach badge title text. This could not be fixed from the EPIC-02 branch (file doesn't exist there yet — created fresh on EPIC-01's branch). **Action required at EPIC-02's post-EPIC-01-merge rebase:** update `SC-GVP-09` to use `[data-testid="breach-badge"]` before EPIC-02's own PR is finalised. Recorded in `execution_state.json.process_notes`.

**Deviations:** None (for this story's own scope)

---

## ST-10 — Gate Progress Indicator copy divergence (BLG-SPEC-73)

**Spec reference:** `docs/specs/frontend/pages/dashboard.md#6`
**Commit:** cd97af1d
**What was built:** `dashboard.md` §6 Display table updated to document the shipped `GateProgressStrip.js` copy verbatim as canonical; Known Deviations note removed (superseded). No code change — `GateProgressStrip.js` and its Playwright coverage (`tests/e2e/gate-progress.spec.js`) were already correct.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| dashboard.md §6 and GateProgressStrip.js use identical copy | Pass |
| Known Deviations note in dashboard.md §6 removed once resolved | Pass |
| Wording-only AC — code review may substitute for staging sign-off per FI-P3-02 | Applied — no visual/colour/layout change, code review sufficient |

**Deviations:** None

---

## ST-11 — Add endpoint and date-range filters to GET /ai/claude-audit-log (BLG-BE-51)

**Spec reference:** `docs/specs/api_contracts/ai_endpoints.md` (v1.5→v1.6)
**Commit:** 95c2a0e4
**What was built:** `endpoint`, `date_from`, `date_to` optional query filters added to `database.query_claude_audit_log()` and `GET /ai/claude-audit-log` router. `ai_endpoints.md` and `openapi.yaml` updated in the same commit.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| `GET /ai/claude-audit-log?endpoint=POST%20/ai/daily-briefing` returns only matching rows | Pass |
| `date_from`/`date_to` filters work independently and combined with `endpoint` | Pass |
| Existing unfiltered behaviour unchanged | Pass — verified by `test_no_filters_unfiltered_behaviour_unchanged` |
| `ai_endpoints.md` and `openapi.yaml` updated in same commit | Pass |

**Test scenarios:** `tests/test_claude_audit_log_filters.py` (6 tests, all passing)

**Deviations:** None

---

## ST-12 — Sector Concentration: join ticker_universe for sector data (BLG-BE-38)

**Spec reference:** `docs/specs/frontend/pages/risk_dashboard.md#8a. Component: Sector Concentration Heat Map`
**Commit:** e5ae2802
**What was built:** `_get_ticker_sector_map()` + `_lookup_sector()` added to `portfolio_risk.py`, wired into both `_get_portfolio_heat_and_positions()` (backs `/portfolio/concentration-status`) and `get_sector_weights()` (`/portfolio/sector-weights`). Pure DB read against `ticker_universe`, UK `.L` suffix handled, no yfinance call added.

**Acceptance criteria:**
| AC | Result |
|----|--------|
| AC-01: Sector Concentration panel shows correct sector tiles for positions whose tickers exist in ticker_universe with a non-null sector | Pass |
| AC-02: Positions with no sector in ticker_universe still render as "Unclassified" (fallback preserved) | Pass — verified by `test_unknown_ticker_returns_none` / `test_empty_map_returns_none` |
| AC-03: GET /portfolio/concentration-status sector breach calculation also reflects correct sectors | Pass — same `_lookup_sector` used in `_get_portfolio_heat_and_positions` |
| AC-04: No yfinance live-call added to the hot path | Pass — verified by `test_query_filters_null_sector_no_yfinance_call` (asserts SQL string, no yfinance import touched) |

**Test scenarios:** `tests/test_portfolio_risk_sector.py` (11 tests, all passing)

**Deviations:** None

---

## EPIC-02 Consolidation Block

**EPIC:** EPIC-02 — v6.9 Carryover Fixes & Reconciliation
**Cycle:** 2026-07-12__release-v7.0
**Sprint goal:** Close the Grid View/Table View position-risk badge and trailing-stop parity gap, resolve the v6.9-carried spec-reconciliation and data-correctness debt, and ship three new reporting and position-review features.
**Test scenarios used:** `tests/e2e/heading-light-theme-contrast.spec.js` (4), `tests/e2e/epic01-v62-stops-alerts.spec.js` (16, updated), `tests/test_portfolio_risk_sector.py` (11), `tests/test_claude_audit_log_filters.py` (6), `tests/test_trailing_stop_recommendation_log.py` (5). Full backend suite (627 tests) re-run clean after each backend change.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-06 | reports.md | Arc 5/Gross-vs-Net marked Design Only — Implementation Pending | All 3 AC | Pass | None |
| ST-07 | metrics_definitions.md | trailing_stop_recommendation_log capture | All 3 AC | Pass | None |
| ST-08 | heading-light-theme-contrast decision record | Dashboard/StrategyBenchmark contrast fix + Playwright | Both AC | Pass | None |
| ST-09 | positions.md §Trailing Stop Column | Breach badge colour/label fix | Both AC | Pass | None |
| ST-10 | dashboard.md §6 | Gate Progress copy reconciliation | All 3 AC | Pass | None |
| ST-11 | ai_endpoints.md | claude-audit-log endpoint/date filters | All 4 AC | Pass | None |
| ST-12 | risk_dashboard.md §8a | Sector Concentration ticker_universe join | All 4 AC | Pass | None |

**QA test coverage:**
- Scenarios run: see per-story test scenarios above (frontend: 20 Playwright scenarios across 2 files, local run all passing; backend: 22 pytest scenarios across 3 new files, plus full 627-test regression suite clean)
- Regression areas checked: Positions Table/Grid View (badge parity retained), Dashboard/StrategyBenchmark headings (dark theme unchanged), Sector Concentration/Portfolio Risk endpoints (existing tests unaffected — no dedicated pre-existing suite), claude-audit-log (unfiltered behaviour unchanged), Trail Stop recommendation endpoint (existing nightly-ratchet tests unaffected, different mechanism)
- Known deviations filed: None this EPIC

**Frontend testing gate check (CLAUDE.md, LL-v3.1-EX-01):** All observable ACs (ST-08 heading colour/contrast, ST-09 badge colour/label) have Playwright coverage. ST-10 is wording-only — FI-P3-02 code-review exception applies (no visual/colour/layout claim). No "code review only" ACs requiring a backlog exemption.

**Autonomous class eligibility check (BLG-GOV-19):**
- Criterion 1 (all stories autonomous): ✓
- Criterion 2 (all AC code-review-verifiable, no observable UI behaviour): ✗ — ST-08/ST-09 have observable UI behaviour (heading colour, badge colour/label)
- Criterion 3 (no frontend-visible change): ✗ — `src/pages/DashboardHome.js`, `src/pages/StrategyBenchmark.js`, `src/pages/Positions.js` modified (detection rule BLG-GOV-135)
- Criterion 4: N/A (fails at 2/3)

Autonomous class does **not** apply — Standard Sign-Off Block required, Director of Quality review.

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations (none filed this EPIC)
- [x] Regression areas checked (full 627-test backend suite clean; 20 Playwright scenarios clean)
- [x] No frontend component in this EPIC makes direct URL construction outside the `api.*` wrapper
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-07-13
- Comments: Spot-checked 4 of 7 story commits in full diff (ST-07, ST-09, ST-11, ST-12) plus stat-level checks on the remaining 3 — every diff matches the qa_evidence log's claims exactly. ST-09 breach badge colour/label verified against positions.md §Trailing Stop Column verbatim. ST-12 sector join confirmed as a pure DB read (no yfinance import touched, asserted directly in test). ST-07's log write confirmed genuinely fire-and-forget (try/except wrapping the full DB call). ST-11's filters are parameterized (no SQL injection risk). Independently re-ran the 3 new backend test files (22/22 passed). ST-09's cross-EPIC note re: SC-GVP-09 verified sound — confirmed the referenced test file genuinely does not exist on this branch (structural impossibility, not avoidance); the required post-EPIC-01-merge fix is correctly recorded in execution_state.json.process_notes.
