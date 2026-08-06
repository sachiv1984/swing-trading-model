Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-06

# QA Evidence — EPIC-02: Backend Engineering Hardening

**EPIC:** EPIC-02 — Backend Engineering Hardening
**Cycle:** 2026-08-05__release-v8.3
**Sprint goal:** Restore and harden the SI-05 weekly digest pipeline (fix plus delivery-failure alerting) while clearing a curated slate of backend resilience, frontend design-system, QA/spec, and governance-process debt — leaving no ungated P1 operational gap open and no item below its stated acceptance bar.
**Test scenarios used:**
- `tests/test_regime_retry_backoff.py`
- `tests/test_alpaca_paper_sync_idempotent_retry.py`
- `tests/test_position_lifecycle_states_registry.py`
- `tests/test_router_error_envelope_conformance.py`
- `tests/e2e/custom-price-alerts.spec.js` (SC-CPA-07, updated)
- `tests/e2e/si04-version-comparison.spec.js` (SC-SI04-03/04/05, updated)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-05 | `docs/ops/db_index_audit_arc4_2026-08-06.md` | Arc 4 cross-table query index audit across trade_plans, red_flag_events, pre_entry_validation_log (arc5-compliance proxy), ai_journal_entries (out of scope, externally provisioned) | Audit doc produced; missing indexes filed separately; reviewed by Infra & Ops Owner | Pass | None — 1 gap found (trade_plans ticker index), filed as `BLG-BE-82` per AC |
| ST-06 | `docs/ops/alpaca_backoff_audit_2026-08-06.md` | Alpaca API rate-limit backoff audit across all 3 call-site files (`alpaca_service.py`, `news_service.py`, `alpaca_paper_sync_service.py`) | Audit findings documented; gaps filed as follow-ups | Pass | None — 1 gap found (paper-sync close/positions endpoints), filed as `BLG-BE-83` per AC |
| ST-07 | `docs/specs/position_lifecycle_states_registry.md`, `backend/utils/position_lifecycle_states.py` | Canonical `position_state` registry; 5 backend call sites (`position_lifecycle_service.py`, `position_service.py`, `portfolio_service.py`, `portfolio_risk.py`, `main.py`) migrated to import from it; frontend reconciliation documented (values already consistent, no drift) | Canonical registry exists; backend/frontend confirmed consistent | Pass | None |
| ST-08 | `docs/specs/api_contracts/conventions.md §13`, `docs/specs/api_contracts/backend_engineering_patterns.md` | All 17 listed routers conformed to `{status, message}` canonical error envelope at correct HTTP status; 2 bare-200-error-body bugs fixed (digest.py); 5 additional 429 rate-limit envelope-key bugs found and fixed beyond the audit's original list; earnings/news/strategy_benchmark given try/except wrapping (previously none) | All listed router error paths return canonical envelope; no success-path change; no frontend behaviour change without a corresponding frontend check; applied incrementally (RISK-01) | Pass | None — see Frontend Impact note below; applied across 7 incremental commits |
| ST-09 | `backend/utils/retry.py`, `tests/test_regime_retry_backoff.py` | `retry_with_backoff` applied to both regime-check call sites (`pricing.py::check_market_regime`/`get_ma200`, `screener_batch_service.py::_fetch_index_regime`) | Both call sites use `retry_with_backoff`; fallback unchanged; regression test confirms retries before fallback | Pass | None |
| ST-10 | `backend/services/alpaca_paper_sync_service.py`, `tests/test_alpaca_paper_sync_idempotent_retry.py` | Deterministic `client_order_id` from position id; `retry_with_backoff` on `sync_open_paper_position` | `client_order_id` deterministic; retry applied; test confirms no duplicate order on retry | Pass | None |

**Frontend Impact Note (ST-08 — Frontend Testing Gate, LL-v3.1-EX-01):**
ST-08's router-level fix changed the error-response JSON shape for the 17 listed endpoints. A frontend check (required by ST-08's own 3rd acceptance criterion) found 4 call sites reading the old `.detail` field directly (bypassing the `doFetch` API wrapper, which already preferred `.message`): `src/pages/TickerUniverse.js`, `src/pages/Signals.js`, `src/components/notifications/CustomPriceAlertsSection.js`, and `src/pages/StrategyBenchmark.js` (the latter reading a nested `detail.code`/`detail.version` structure for `/analytics/strategy-version-comparison` — this endpoint's structured error fields moved from nested-under-`detail` to flat top-level, matching the endpoint's own documented contract in `strategy_version_comparison_contract.md`). All 4 were corrected to read the new field locations — **text/data-source-only, no rendered output, layout, or colour change** (same message strings render either way once the source field is correct).

**Observable AC disposition:** 2 Playwright spec files directly exercise these exact error-message-display paths and were updated in the same commits to mock the new response shape: `tests/e2e/custom-price-alerts.spec.js` (SC-CPA-07) and `tests/e2e/si04-version-comparison.spec.js` (SC-SI04-03/04/05). Per the frontend testing gate's option 1 ("Check Playwright coverage... if yes, record the test file and scenario ID"), this satisfies the gate — coverage exists and was kept in sync. **Local execution limitation (disclosed, not a skipped step):** this environment cannot execute Playwright (`npx playwright install chromium` fails — "Playwright does not support chromium on ubuntu26.04-x64", a pre-existing platform incompatibility unrelated to this change). Verification was performed by exact code-review data-flow trace instead (`doFetch`/`apiFetch` response shape confirmed against the new backend envelope), which CLAUDE.md §2's FI-P3-02 exception permits for changes with zero rendered-output difference. CI will execute both updated spec files for real on push — this is the actual gate, and it was not bypassed, only locally unavailable.

**QA test coverage:**
- Scenarios run: `tests/` full backend suite (1002 passed, 5 skipped — unaffected pre-existing skips) after every incremental commit; `tests/test_router_error_envelope_conformance.py` (18 new tests, representative sample per router per `test_main_500_no_raw_exception_text.py`'s established "spot-check" precedent — not all ~90 individual call sites, since the fix is one mechanical pattern applied identically)
- Regression areas checked: alerts, analytics, digest, ai, paper trading, plan-vs-reality, portfolio sizing, red flag journal, saved filters, screener, strategy benchmark, ticker universe, trade plans, trades export, validation, watchlist, earnings, news (all 17 ST-08 routers); position lifecycle / display_status (ST-07); Yahoo Finance regime checks (ST-09); Alpaca paper sync (ST-10)
- Known deviations filed: None (0 P0–P3 spec deviations this EPIC) — 2 audit-finding backlog items filed per their stories' own AC (`BLG-BE-82`, `BLG-BE-83`, both P3, not deviations from spec)

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no new URL construction introduced; 4 files touched only change which existing response field is read
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-06
- Comments: BLG-GOV-19 autonomous class does not apply — Criterion 3 automatically unmet per the BLG-GOV-135 detection rule (ST-08 modified files under `src/pages/**` and `src/components/**`). Standard sign-off block used instead. All 6 stories are `autonomous` classification with no `delegated_*` items, so the Mixed-Class Signer Format note does not otherwise apply — single agent-mediated Director of Quality line covers the EPIC. See per-story rows above and the Frontend Impact Note for the one cross-cutting finding (frontend `.detail`→`.message` fix) spanning ST-08.
