**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-29
**Cycle:** 2026-10-29__release-v9.14

# Design Gate Record — 2026-10-29__release-v9.14

## Gate Status: PASSED

Completed: 2026-10-29
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

All 54 items are classified and cleared. No item is conditionally cleared or blocked.

| Classification | Count | Items |
|----------------|-------|-------|
| Design Required | 10 | ST-03, ST-04, ST-05, ST-07, ST-08, ST-11, ST-14, ST-24, ST-26, ST-28 |
| Design Pre-Approved | 5 | ST-06, ST-09, ST-25, ST-27, ST-30 |
| Design Not Applicable | 39 | the remaining items |

**Classification notes:**
- The slice marks 15 stories UI-facing (including ST-09 "Conditional" and ST-30 "Verification only"). Five are Pre-Approved rather than Design Required:
  - **ST-06** shows its new status in the existing component-health card, which already has a `degraded` style (yellow) and shows `details` when expanded. No layout or new element.
  - **ST-09** corrects a computed value. If the Trade Entry risk display carries the same inversion, it shows the right number in the same place.
  - **ST-25** applies the rule `dashboard.md` §Card 5 already states: the glyph and colour follow the P&L *as displayed*. "−£0.01" therefore gets the down glyph. The defect is a rounding mismatch in code.
  - **ST-27** restores the state `reports.md` §AI Summary already specifies: "A stored summary for the current figures renders at once with no `POST`."
  - **ST-30** is a staging check of the v9.13 layout against its existing specs. It changes nothing.
- **ST-04 and ST-05** share one decision record, as do **ST-07 and ST-08**. Each pair is one indicator, built in sequence.
- **ST-26 and ST-28** need no new decision record. ST-26 is a wording fix (FI-P3-02), and its spec template was corrected at this gate. ST-28 follows the v9.8 navigation-taxonomy precedent that `SystemStatus.js` already applies to `/replay`.
- **ST-03** depends on an in-sprint ruling by the Strategy Rules & System Intent Owner. All three outcomes are designed (v9.13 ST-05/ST-06 precedent), and the unused branches are deleted at implementation.
- **ST-22** is not UI-facing. "Improve with AI" and the template button keep their behaviour (AC 3). ST-22's `SystemStatus.js` change is the fallback count only.
- **ST-46** documents an existing UI pattern in the frontend spec and changes no UI. It is Not Applicable, and its spec write is in-story.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-OPS-193) | Restore eslint-config-react-app so the frontend builds and deploys again | Design Not Applicable | Build and CI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 (BLG-BE-192) | Compute the SPY market regime from Alpaca bars when Yahoo Finance fails | Design Not Applicable | Backend data source. A regime from Alpaca displays as any measured regime. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-BE-193) | Show an unknown market regime instead of silently defaulting to risk-on | Design Required | New state on four regime surfaces. Today an unknown value renders as "Risk Off". Three ruling branches designed. | `docs/design/2026-10-29__release-v9.14/market-regime-unknown/decision_record.md` (new) | `dashboard.md` v3.9 → v3.10 (§Card 4); `signals.md` v0.6 → v0.7 (§Market Status Bar) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-04 (BLG-BE-194) | Use the last good GBP/USD rate, with its age, before the fixed 1.27 fallback | Design Required | New data displayed: the rate's source and age | `docs/design/2026-10-29__release-v9.14/fx-rate-source-indicator/decision_record.md` (new, shared with ST-05) | `dashboard.md` v3.10 (§Card 2); `risk_dashboard.md` v0.1.13 → v0.1.14 (§2a); `signals.md` v0.7 (§Market Status Bar) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-05 (BLG-BE-169) | Flag an FX fallback instead of applying it silently | Design Required | New indicator on the Dashboard and Risk Dashboard | `docs/design/2026-10-29__release-v9.14/fx-rate-source-indicator/decision_record.md` (new, shared with ST-04) | `dashboard.md` v3.10 (§Card 2); `risk_dashboard.md` v0.1.14 (§2a FX Rate Source Notice) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-06 (BLG-OPS-194) | Make the System Status Yahoo Finance check detect an outage | Design Pre-Approved | The existing component-health card already renders `degraded`/`unhealthy` and shows `details` when expanded. Only the values change. | N/A | `system_status.md` v1.4 (locked reference — §Individual Service Cards, §Degraded State) | ✅ Cleared | Head of UX & Design |
| ST-07 (BLG-BE-168) | Flag stale prices on GET /positions and the Positions page | Design Required | New marker on the Positions table and grid | `docs/design/2026-10-29__release-v9.14/stale-price-marker/decision_record.md` (new, shared with ST-08) | `positions.md` v2.20 → v2.21 (§Stale Price Marker) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-08 (BLG-FE-214) | Make the stale-price explanation reachable on touch, keyboard and screen readers | Design Required | Changed interaction (focusable marker, tooltip on hover, focus and tap) and new copy. The slice asks for design-gate review of the wording. | `docs/design/2026-10-29__release-v9.14/stale-price-marker/decision_record.md` (new, shared with ST-07) | `risk_dashboard.md` v0.1.14 (§6.6); `positions.md` v2.21; `dashboard.md` v3.10 (§Card 2) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-09 (BLG-BE-190) | US position sizing divides the stop distance by the GBP/USD rate | Design Pre-Approved | Value correction. If the Trade Entry risk display is also inverted, the same field shows the right number, with no layout change. | N/A | `components/position_form.md` v1.10 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-10 (BLG-BE-188) | POST /positions/{id}/exit returns its documented 404 and 400, not 500 | Design Not Applicable | API status codes. The Exit modal's error state already exists (`positions.md` v2.20 §Daily Position Monitor Exit Queue, Failure). | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 (BLG-FE-231) | Daily Position Monitor stops suggesting "Stop Loss Hit" during the grace period | Design Required | Changed suggestion logic and precedence, a new hold reason, and a corrected pre-selection note | `docs/design/2026-10-29__release-v9.14/monitor-grace-aware-suggestions/decision_record.md` (new) | `positions.md` v2.21 (§Monitor Suggestions; §Daily Position Monitor Exit Queue note) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-12 (BLG-BE-167) | GET /portfolio P&L handles a US position whose fill_price is NULL | Design Not Applicable | Backend | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 (BLG-SPEC-190) | Positions data dictionary states that entry_price is stored in GBP | Design Not Applicable | Spec text | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 (BLG-SPEC-192) | Review-cadence grace suppression and the grace alert agree once grace has ended | Design Required | The slice allows a code fix or a documented difference. Option (a), the code fix, was chosen, which changes when the flag shows. | `docs/design/2026-10-29__release-v9.14/last-reviewed-ended-grace/decision_record.md` (new) | `positions.md` v2.21 (§Last Reviewed Column, suppression rule) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-15 (BLG-AI-20) | Journal summary catches advisory phrasings the trading-change check misses | Design Not Applicable | Output check. §13: see the pre-check below. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 (BLG-AI-21) | Daily briefing ticker caveat ignores indicator and macro acronyms | Design Not Applicable | Output filter | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 (BLG-AI-22) | Chat stop-time note is not attributed to the focus ticker when a sentence names another ticker | Design Not Applicable | Validator attribution. The note's styling is unchanged. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 (BLG-AI-19) | Monthly P&L narrative scan stops flagging retrospective and discourse wording | Design Not Applicable | Output check | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 (BLG-BE-164) | A debrief that fails compliance then errors writes one audit row | Design Not Applicable | Audit logging | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 (BLG-BE-165) | Stop recalculation times in briefing and chat are converted to UTC | Design Not Applicable | Prompt-context time formatting. No UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 (BLG-BE-166) | Run the claude_audit_log column checks once per process | Design Not Applicable | Backend | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 (BLG-BE-163) | Retire the unused POST /trade-plans/{plan_id}/generate-thesis endpoint | Design Not Applicable | Unused endpoint removed. The two thesis buttons behave as before (AC 3). | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 (BLG-GOV-178) | First live quarterly AI output sample against the §13 boundary | Design Not Applicable | Audit | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 (BLG-FEAT-99) | Monthly P&L breakdown by §8 exit condition | Design Required | New table in the Monthly P&L report | `docs/design/2026-10-29__release-v9.14/monthly-pnl-exit-condition-breakdown/decision_record.md` (new) | `reports.md` v0.25 → v0.26 (§Exit Condition Breakdown) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-25 (BLG-FE-213) | Recent Trades glyph and amount agree at a half-penny loss | Design Pre-Approved | `dashboard.md` §Card 5 (v3.8) already requires the glyph to follow the P&L as displayed. Code fix only. | N/A | `dashboard.md` v3.10 (locked reference — §Card 5, "Zero means displays as £0.00") | ✅ Cleared | Head of UX & Design |
| ST-26 (BLG-FE-215) | Pluralise the month counts in the monthly P&L summary fallback | Design Required | Copy change to code-written text. Wording only, so the FI-P3-02 code-review exception applies. | Spec update only (no layout; copy rule in the spec) | `reports.md` v0.26 (§AI Summary, standard summary template) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-27 (BLG-FE-216) | Keep a generated monthly P&L summary visible after switching tax year and back | Design Pre-Approved | Restores the specified load behaviour. Cache fix. | N/A | `reports.md` v0.26 (locked reference — §AI Summary, Behaviour → Load) | ✅ Cleared | Head of UX & Design |
| ST-28 (BLG-FE-217) | Group /reports endpoints on the System Status page | Design Required | Changed grouping. `/reports` → Analytics, matching `src/Layout.js` and the `/replay` precedent. | Pre-existing precedent (`docs/design/2026-09-28__release-v9.8/system-status-replay-categorisation/decision_record.md`, as shipped) | `system_status.md` v1.3 → v1.4 (§Endpoint Test Category Labels) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-29 (BLG-QA-237) | Cover the Positions-page Exit modal submit in Playwright | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 (BLG-QA-235) | Staging visual check of the layout changed by tailwind-merge in cn() | Design Pre-Approved | Verification against v9.13's specs. No change. | N/A | v9.13 references: `docs/design/2026-10-16__release-v9.13/coloured-button-fills/decision_record.md`; `screener_results.md` v1.10; `components/cash_management_modal.md` v1.3 | ✅ Cleared | Head of UX & Design |
| ST-31 (BLG-QA-238) | Pre-commit OpenAPI contract check reads staged content | Design Not Applicable | Tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-32 (BLG-QA-93) | Confirm the conftest.py AST scan still covers every backend module | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-33 (BLG-QA-214) | Behaviour test: the grace warning ignores settings.min_hold_days | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-34 (BLG-QA-215) | Assert the stop-details tooltip time under a non-UTC browser timezone | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-35 (BLG-QA-216) | Assert the applied theme in every Reports/Notifications axe scan | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-36 (BLG-QA-218) | Stop test files adding backend/services/ to sys.path | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-37 (BLG-QA-219) | Stop the ⌘K hint toast intercepting the chat submit click in SC-AC-03 | Design Not Applicable | Tests only. The app is unchanged. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-38 (BLG-OPS-21) | Arc 2 compute cost review | Design Not Applicable | Ops documentation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-39 (BLG-OPS-85) | Compute cost trending by feature area | Design Not Applicable | Ops report | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-40 (BLG-OPS-105) | CI pipeline runtime audit | Design Not Applicable | Ops documentation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-41 (BLG-OPS-186) | Daily AI cost check covers the last hours of the day | Design Not Applicable | Ops monitoring | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-42 (BLG-OPS-188) | Make ci-usage-report.yml's monthly commit succeed | Design Not Applicable | CI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-43 (BLG-SEC-43) | Per-environment CORS allow-list | Design Not Applicable | Backend configuration | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-44 (BLG-GOV-397) | check_execution_state_consistency.py checks deviations_filed and the escalation map | Design Not Applicable | Governance tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-45 (BLG-GOV-398) | Give the gate scan's "gating item shipped" findings a write-back path | Design Not Applicable | Governance prompt | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-46 (BLG-SPEC-77) | Document the gate-status indicator as a reusable component pattern | Design Not Applicable | Documents the shipped SI-02 indicator. No UI change. | N/A | N/A (in-story write under `docs/specs/frontend/`) | ✅ Cleared | Head of UX & Design |
| ST-47 (BLG-SPEC-189) | risk_dashboard.md names only fields GET /portfolio returns | Design Not Applicable | Spec text correction with no UI change. It edits `risk_dashboard.md` §5.1/§6.1 on top of this gate's v0.1.14. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-48 (BLG-SPEC-191) | Align Appendix F's effort-weighted PVR table and status with the script | Design Not Applicable | Metrics documentation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-49 (BLG-SPEC-193) | Trade plan contract lists the 7 DS-21 statuses | Design Not Applicable | Contract text | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-50 (BLG-GOV-184) | Confirm "win rate" is computed the same way on every surface | Design Not Applicable | Audit. Discrepancies are filed, not fixed. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-51 (BLG-GOV-185) | Add a changelog section to metrics_definitions.md | Design Not Applicable | Metrics documentation. See Notes: the section may already exist. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-52 (BLG-GOV-186) | §13 boundary worked examples | Design Not Applicable | Governance documentation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-53 (BLG-GOV-189) | Governance overhead audit | Design Not Applicable | Governance documentation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-54 (BLG-GOV-191) | Spec debt aging report | Design Not Applicable | Governance tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |

## §13 Boundary Pre-Check

**No flags.** No item introduces a new AI-calling endpoint or a new AI feature. Each AI-adjacent item narrows, checks, formats, logs or removes an existing call that is already covered:

- **ST-15:** journal summary. Covered by `SRB-v1.7-2026-03-02__release-v1.7.md` (CONDITIONALLY COMPLIANT) and `decisions--2026-04-17__release-v2.8.md` (BLG-FEAT-16). Its AC 1 already makes the ruling extension a §13 determination answering §13.1/§13.2 (slice clause-citation rule).
- **ST-16, ST-17 and ST-20:** daily briefing and chat. Covered by `decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md` (PASS). ST-17's AC 1 cites §13.2 and the §13.5 "BLG-FEAT-50/51" roster row.
- **ST-18 and ST-26:** monthly P&L narrative. Covered by `decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md` (CONDITIONAL). ST-26 changes code-written fallback text only.
- **ST-19:** post-trade debrief audit logging. Covered by `decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (CONDITIONAL). There is no change to the call or its output.
- **ST-21:** audit-log DDL. Calls no provider.
- **ST-22:** removes an AI-calling endpoint and adds none. Its §13.5 roster row update is in AC 5.
- **ST-23:** reviews stored outputs and makes no new call. Its AC 1 cites §13.2 and each §13.5 roster row.
- **ST-03:** the regime ruling is a strategy determination (§4.2.1, §8.2), not an AI item.

The AI endpoint security checklist is not triggered: no new AI-calling endpoint.

## Blocked Items

None.

## Notes

### Post-gate-correction addendum

`claude/cycles/2026-10-29__release-v9.14/stage4_backlog_slice_addendum.md` was created with 2 entries covering 3 stories: ST-03, and ST-04 with ST-05. Sprint Planning and Sprint Execution must read it together with the sealed slice. Each entry clarifies a story within its own Scope and changes no scope. ST-03 flags a possible estimate check at Sprint Planning, because the unknown state covers four surfaces.

### Artefacts produced and specs updated

- **Design artefacts produced this run:** 6 decision records under `docs/design/2026-10-29__release-v9.14/`:
  - `market-regime-unknown` (ST-03)
  - `fx-rate-source-indicator` (ST-04, ST-05)
  - `stale-price-marker` (ST-07, ST-08)
  - `monitor-grace-aware-suggestions` (ST-11)
  - `last-reviewed-ended-grace` (ST-14)
  - `monthly-pnl-exit-condition-breakdown` (ST-24)
- **ST-26 and ST-28** have no new record (see Classification notes).
- **Frontend specs updated (6 files):** each is logged in `prompt_change_log.md`.
  - `dashboard.md` 3.9→3.10
  - `signals.md` 0.6→0.7
  - `risk_dashboard.md` 0.1.13→0.1.14
  - `positions.md` 2.20→2.21
  - `reports.md` 0.25→0.26
  - `system_status.md` 1.3→1.4
- **`system_status.md` correction:** the v1.2 table listed a separate Replay category (`RefreshCw`, pink). The shipped `categorizeEndpoint()` maps `/replay` to Analytics, and there is no Replay category in the code. The row is removed and the Analytics row lists `/analytics`, `/replay` and `/reports`.

### Obligations passed to Sprint Execution (outside this gate's write scope)

- **New response fields, each with its contract and `openapi.yaml` in the same commit (RISK-04):**
  - ST-03: `regime_status`, null `is_risk_on`/`price`/`ma200` on `GET /market/status`, and `status: "unknown"` on `GET /market/regime`. Under ruling (b), also `last_known_status` and `last_known_at`.
  - ST-04/ST-05: `fx_rate`, `fx_rate_source` and `fx_rate_as_of` on `GET /portfolio`, `GET /positions` and `GET /market/status`.
  - ST-07: `price_is_stale` on `GET /positions`.
  - ST-24: `by_exit_condition` per month on `GET /reports/monthly-pnl`.

  No new route is designed at this gate, so the `routers/test.py` / `SystemStatus.js` count / `SC-SS-01b` chain applies only to ST-22's removal.
- **ST-06** reads ST-04's `fx_rate_source` and ST-03's unknown flag. The check's `details` should carry a plain `reason` string, because the card shows `details` as-is.
- **ST-11:** the Monitor's `positions` must carry `grace_period`, `current_trailing_stop` and `risk_off_exit` (record §5).
- **ST-47** edits `risk_dashboard.md` after this gate's v0.1.14 bump. Its version bump is v0.1.15 or later.
- **`metrics_definitions.md`** is edited by ST-24, ST-48 and ST-51 (RISK-04, unchanged).

### Playwright coverage (CLAUDE.md §2)

Each Design Required decision record's testability section lists its assertions. These go beyond the slice's ACs, so execution must add them or file a backlog item before the PR opens:
- **ST-03:** the Signals bar's "Unknown" and "Price unavailable" state.
- **ST-04/ST-05:** the Signals FX tile's source line.
- **ST-08:** Dashboard Card 2's link carries the stale explanation as its accessible description. The marker has the same check on the Positions page.
- **ST-11:** the "In grace: stop not enforced" hold reason, and risk-off precedence when both conditions apply.
- **ST-24:** the "unavailable" state, and the light-theme axe scan with the card shown.

### Observation for Sprint Planning (not a design matter)

ST-51's AC ("a changelog section is added") may already be met. `docs/specs/metrics_definitions.md` has an `## Appendix D — Change Log` table, with rows back to v1.20.0 and up to v1.30.0 (2026-10-16). The source item (BLG-GOV-185, filed 2026-07-08) predates that table. ST-48's sequencing ("after ST-51, which adds the changelog section this story writes to") rests on the same premise. Changing ST-51's scope or estimate is outside this gate's authority. Sprint Planning should confirm the AC against the file and re-scope the story or close it as already met.
