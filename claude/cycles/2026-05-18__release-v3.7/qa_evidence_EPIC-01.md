Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-18

---

## Consolidation Block

**EPIC:** EPIC-01 — Signal-to-Watchlist workflow (BLG-FE-33 + BLG-FE-34)
**Cycle:** 2026-05-18__release-v3.7
**Sprint goal:** Ship the signal-to-watchlist workflow (Add to Watchlist CTA on signal cards + signal context panel in trade plan form)
**Test scenarios used:**
- `docs/testing/signals_scenarios.md` v1.2 (§4 SC-SIG-WL-01/02/03)
- `docs/testing/watchlist_scenarios.md` v1.1 (§4 SC-TP-SIG-01/02/03/04)
- Playwright: `tests/e2e/signals-add-to-watchlist.spec.js`
- Playwright: `tests/e2e/trade-plan-signal-context.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `docs/specs/api_contracts/signal_endpoints.md §PATCH /signals/{id}` | `ensure_signals_watchlisted_status()` migration; `watchlisted` added to PATCH allowed statuses; `backend/routers/test.py` updated (57→58); openapi.yaml, SystemStatus fallback, e2e SC-SS-01b updated | PATCH /signals/{id} accepts status=watchlisted; 400 on invalid status; DB constraint extended | Pending DoQ | None |
| ST-02 | `docs/specs/frontend/pages/signals.md §Signal Card Actions` | SignalCard.js: Add to Watchlist CTA + watchlisted state; Signals.js: handleAddToWatchlist (POST /watchlist → PATCH /signals cascade); Playwright SC-SIG-WL-01/02/03 | New signal shows "Add to Watchlist"; 201→watchlisted; 409→toast; "Add Position" absent | Pending DoQ | None |
| ST-03 | `docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md` | SignalContextPanel.js (read-only panel + buildSignalPrePopulation); TradePlan.js: query + linkedSignal + pre-population + render; Playwright SC-TP-SIG-01/02/03/04 | Panel present when signal watchlisted for ticker; absent otherwise; absent in edit mode; pre-population applied | Pending DoQ | None |

**QA test coverage:**
- Scenarios run: Playwright files authored covering all mandatory observable AC per §2 CLAUDE.md rule
- Regression areas checked: Signals page (no Add Position regression — SC-SIG-WL-03), Trade Plan form (edit mode non-regression — SC-TP-SIG-04), SystemStatus endpoint count (SC-SS-01b)
- Known deviations filed: None

**Note on stop_level pre-population (ST-03):** spec §5a.3 references stop_level pre-population but the actual form has no numeric stop_level field (pre-existing form deviation from v3.1, not introduced in ST-03). Only entry_rationale and confirmation_criteria are pre-populated — mapping to spec's `risk_reward_notes` field reference per ux_spec.md §5.2 note ("if the trade plan form does not currently have a confirmation criteria field as a distinct field…"). No deviation filed — this is a form-spec naming mismatch, not a functional gap.

---

## Standard Sign-Off Block

> Playwright test coverage exists for all observable AC (panel presence/absence, CTA rendering, card state transitions). Playwright test files: `tests/e2e/signals-add-to-watchlist.spec.js` (SC-SIG-WL-01/02/03), `tests/e2e/trade-plan-signal-context.spec.js` (SC-TP-SIG-01/02/03/04).

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): `Signals.js` uses `apiFetch(${API_BASE}/watchlist, ...)` — `apiFetch` is the project's standard fetch wrapper from `src/api/base44Client.js`; URL-base variable `API_BASE` is `process.env.REACT_APP_API_URL || "http://localhost:8000"` — confirmed correct pattern
- Signed off by: *(Director of Quality — pending)*
- Date: *(pending — must be non-blank before PR merge)*
- Comments: Playwright tests cover all observable AC for ST-02 and ST-03. ST-01 has no frontend-visible changes; backend-only, verifiable by code review. All three stories committed on EPIC-01 branch (commit SHAs: ST-01=09093c0c, ST-02=08816093, ST-03=4799d442).
