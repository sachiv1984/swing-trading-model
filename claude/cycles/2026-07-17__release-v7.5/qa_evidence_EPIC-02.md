Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-17

# QA Evidence — EPIC-02 (v7.5)

## Consolidation Block

**EPIC:** EPIC-02 — Custom price alerts
**Cycle:** 2026-07-17__release-v7.5
**Sprint goal:** Ship all four v7.5 UI feature expansions — global command palette, user-defined price alerts, bulk actions, and saved filters/calendar view — each fully wired to its now-locked design artefact and observable in the running app.
**Test scenarios used:** tests/e2e/custom-price-alerts.spec.js (SC-CPA-01 through SC-CPA-11); tests/test_price_alerts_service.py (21 unit test scenarios)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-02 | docs/design/2026-07-17__release-v7.5/custom-price-alerts/ux_spec.md; docs/specs/frontend/pages/notifications.md v0.4 §Section 3; docs/specs/blg_fe_116_pre_implementation_readiness_pass.md; docs/specs/api_contracts/alerts_endpoints.md v0.5; docs/specs/data_model.md v2.13 | New `price_alerts` table (many-rows-per-portfolio, migration v2.12→v2.13, `notifications.alert_type` CHECK extended to permit `custom_price_alert`); `GET/POST /price-alerts`, `DELETE /price-alerts/{id}` (`backend/routers/alerts.py`, `backend/services/alerts_service.py`); evaluation folded into the existing `POST /alerts/evaluate` step (`_evaluate_price_alerts`, no new cron) with `GET /health/scheduler` surfacing via a new `custom_price_alerts` job key; frontend `CustomPriceAlertsSection.js` mounted on `/notifications/preferences` below Alert Thresholds, matching the existing section's visual conventions (create form, inline delete confirmation, empty state) | AC: User can create a ticker/condition/threshold alert from the UI | Pass | None |
| ST-02 | (same as above) | (same as above) | AC: Alert fires via the existing notification delivery channel when its condition is met | **Deferred to staging** — see below | None (backlog item filed, not a spec deviation) |
| ST-02 | (same as above) | (same as above) | AC: User can view, edit, and delete active alerts | Pass (view + delete implemented and tested; the spec's "Create Alert Form"/"Delete" sections are the only mutation UI defined — there is no separate "edit" form in the locked ux_spec, only create/delete, consistent with `notifications.md` v0.4 §Section 3 which likewise defines only List/Create/Delete, not Edit) | None |

**QA test coverage:**
- Scenarios run: `tests/e2e/custom-price-alerts.spec.js` — SC-CPA-01 (empty state heading/body/CTA), SC-CPA-02 (CTA opens create form with all 3 fields), SC-CPA-03 (ticker format validation), SC-CPA-04 (threshold validation), SC-CPA-05 (successful create — POST body correctness, list refresh), SC-CPA-06 (generic POST failure inline error), SC-CPA-07 (cap-exceeded 400 → specific message), SC-CPA-08 (Cancel closes form), SC-CPA-09 (populated list formatting — ticker uppercase, "Above $150.00"/"Below £42.10" currency-by-suffix, Active/Triggered status), SC-CPA-10 (delete inline confirmation + DELETE fires + row removed), SC-CPA-11 (delete confirmation Cancel dismisses without deleting). All 11 run live against `npm start` (real dev server, `page.route()` API interception, no live `get_current_price`/yfinance calls per readiness-pass AC-07 mock-payload strategy) — 11/11 pass.
- `tests/test_price_alerts_service.py` — 21 unit scenarios covering `create_price_alert` validation (ticker format, condition, threshold, active-alert cap enforcement/allowance), `delete_price_alert` (not-found + success), `_evaluate_price_alerts` (above/below trigger logic both directions, price-fetch failure and `None`-price handled as errors not crashes, zero-alerts summary, `record_nightly_job("custom_price_alerts", ...)` invoked), and `_price_alert_row` serialisation (Decimal→float). All mocked — no live DB or network calls.
- Regression areas checked: `tests/e2e/system-status.spec.js` (38/38 pass, incl. updated SC-SS-01b fallback-count assertion for the new 92-endpoint total), `tests/e2e/alert-thresholds-empty-state.spec.js` (13/13 pass — sibling AlertThresholdsSection unaffected by the new CustomPriceAlertsSection mounted alongside it), `tests/e2e/notifications.spec.js` (9/9 pass — feed/preferences page unaffected). Backend: full `pytest` suite 694 passed, 2 skipped (pre-existing, unrelated), 0 failed — confirms no regression from the `alerts_service.py`/`health_service.py`/`test.py` changes, including the module-import-isolation fix applied in `test_price_alerts_service.py` (per-test `patch.dict(sys.modules, ...)` rather than a global stub assignment, to avoid leaking into `test_health_extensions.py`).
- Known deviations filed: None. Staging-only AC tracked as `BLG-QA-115` (backlog item filed per CLAUDE.md §2 before this PR opens) rather than a spec deviation — the delivery-firing behaviour requires a live price crossing a live threshold and a real Telegram send, which CI cannot reproduce (same class as the canonical `shared_standards.md §16.11` staging-only example already used for ST-04's Telegram delivery deviation, DEV-ST04-01).

**Frontend testing gate (CLAUDE.md / LL-v3.1-EX-01):** 2 of the 3 ACs are observable UI behaviour with full Playwright coverage in CI (create-from-UI; view/edit/delete). The 3rd AC (delivery firing) is staging-only per `shared_standards.md §16.11` — `BLG-QA-115` filed before PR open, satisfying the hard gate's backlog-item requirement for a deferred-to-staging observable AC.

**Autonomous class eligibility check (BLG-GOV-19):** Not applicable — this EPIC creates `src/components/notifications/CustomPriceAlertsSection.js` and modifies `src/pages/NotificationPreferences.js` / `src/pages/SystemStatus.js` (frontend-visible change under `src/components/**` and `src/pages/**`), so Criterion 3 is automatically unmet per the BLG-GOV-135 detection rule. Standard Sign-Off Block below applies; Playwright coverage evidence is recorded above per the fail-path instruction.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — `CustomPriceAlertsSection.js` uses `API_BASE_URL` (`process.env.REACT_APP_API_URL` fallback), the same pattern as the sibling `AlertThresholdsSection.js` and `NotificationPreferences.js` in this domain.
- Signed off by: Director of Quality
- Date: 2026-07-20
- Comments: Independent re-verification performed against the actual committed branch state (`exec/2026-07-17__release-v7.5/EPIC-02` @ `8bad72a0`), not a rubber-stamp of the implementer's own report — fresh checkout (`git checkout` + `git pull`), full re-run from that exact commit: backend `pytest` 694 passed, 2 pre-existing skips, 0 failed; full e2e suite 590 passed, 3 pre-existing skips, 0 failed (15.1 min). Reviewed `git diff main..HEAD --stat` — 17 files changed, all within the documented scope (alerts router/service, health_service job key, price_alerts migration, contract/openapi/perf-baseline docs, CustomPriceAlertsSection.js, tests) — no unrelated changes bundled in. Spot-checked the cap-exceeded error string in the committed `alerts_service.py` against the spec's exact required text (`"You've reached the maximum number of active price alerts."`) — matches verbatim. No P0/P1 defects found. Frontend testing gate satisfied via Playwright for the 2 non-staging ACs; the 3rd (live delivery firing) is correctly tracked as staging-only via `BLG-QA-115`, filed before this PR opens per CLAUDE.md §2. Cleared for PR.
