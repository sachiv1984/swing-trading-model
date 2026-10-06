**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-06
**Window:** IW-20261006-01

# Idea Intake Summary — IW-20261006-01

## Window Status: Closed

Opened: 2026-10-06T11:40:42Z
Closed: 2026-10-06T11:45:21Z

*(Real shell timestamps: open = the window-state write immediately after STEP -1.6 found 0 open ideas; close = this file's write.)*

Invoked inline as STEP -1.6 of `run roadmap --reason "scheduled"` (`2026-10-06__scheduled`). The register held 0 rows with `Status: Submitted`/`Parked-cycle-<n>` (below the 20-item threshold; only 1 `Rejected` row present). No standalone window had run beforehand, so the v9.27 standalone pre-run exception does not apply. Mode: `standard`.

**Full roster.** All 22 eligible roles were opened, per `2026-09-30__scheduled/lessons_learnt.md` Carry-Forward #3 (the two previous windows, `IW-20260928-01` and `IW-20260930-01`, were disclosed reduced-roster windows). The §2.1 step 2a roster rule therefore does not apply; the build-and-ship requirement for user-facing roles does.

**Stale-idea horizon check (STEP -0.5):** 0 rows at `Parked-cycle-2` — no advisory.

**Parked queue pre-check (§2.0 steps 1–4):** no `Parked-cycle-<n>` rows exist — nothing to resubmit.

**Backlog scope overlap check (§2.0 step 5, mandatory):** every topic was grepped against `claude/backlog/backlog.md` (185 active items) and `backlog_archive.md` before it was finalised. **Dropped for overlap (5 candidate topics):** `should_exit_position` boundary tests (active item at `backlog.md` line ~3574), Claude model deprecation monitoring (`BLG-GOV-90`, shipped v9.6), scheduled-rebalance cadence (`BLG-GOV-73`), npm accept-risk re-review (triaged today in `npm_audit_rescan_triage_2026-10-06.md`), and an AI-adoption follow-up already answered by `docs/ops/ai_feature_usage_review_2026-09-24.md`. **Kept as stated refinements of an existing item (6):** `IDEA-ai-compliance-20261006-01` (refines `BLG-GOV-90`), `IDEA-head-of-engineering-20261006-01` and `IDEA-qa-testing-20261006-01` (refine `BLG-QA-204`), `IDEA-director-of-hr-20261006-01` (refines `BLG-GOV-353` and the deferred Owner-field canonicalisation patch), `IDEA-financial-reporting-20261006-02` (refines `BLG-BE-135`), `IDEA-pmo-lead-20261006-01` (refines `BLG-GOV-347`). Each names the related item and the new angle.

**Codebase overlap check (§2.0 step 6, mandatory):** every mechanism-naming topic was checked against `backend/`, `src/`, `.github/workflows/` and `scripts/`. Code read directly this window: `backend/services/position_service.py` (`add_position`, `analyze_positions`, `run_nightly_trailing_stop_update`), `backend/utils/calculations.py`, `backend/services/position_lifecycle_service.py`, `backend/services/grace_service.py`, `backend/services/compliance_service.py`, `backend/services/ai_service.py`, `backend/main.py` (`GET /positions/analyze`), `src/api/base44Client.js`, `src/pages/Settings.js`, `src/pages/TradeEntry.js`, `src/pages/Positions.js`, `src/components/positions/ExitModal.js`, `src/components/trades/TradeHistoryTable.js`, `src/components/dashboard/home/morning/`, `.github/workflows/daily-snapshot.yml`, `.github/workflows/nightly-stop-update.yml`, `docs/specs/api_contracts/position_endpoints.md`, `docs/specs/api_contracts/settings_endpoints.md`, `docs/specs/position_lifecycle_states_registry.md`. **0 topics found already implemented.**

**Method note:** each agent perspective was exercised by the engine per §2.1, the same convention every prior window used; submissions are engine-generated under agent perspectives, not independent human input. Full template fields (problem / strategy § / solution / expected value / effort / reversibility / stop / recommendation / overlap result) are recorded per idea in `claude/cycles/2026-10-06__scheduled/cycle_record.md` `## STEP 4 — Ideas`, following the `IW-20260919-01` precedent (the register carries titles, the cycle record carries the fields).

## Submission Counts

| Agent | New Submissions | Parked Resubmitted | Total |
|-------|-----------------|--------------------|-------|
| AI Compliance & Governance Officer | 2 | 0 | 2 |
| API Contracts & Documentation Owner | 2 | 0 | 2 |
| Backend Engineering Patterns Owner | 2 | 0 | 2 |
| Base44 Frontend Prompt Owner | 2 | 0 | 2 |
| Challenger | 2 | 0 | 2 |
| Cybersecurity & Trust Lead | 2 | 0 | 2 |
| Data Model & Domain Schema Owner | 2 | 0 | 2 |
| Director of HR | 2 | 0 | 2 |
| Director of Quality | 2 | 0 | 2 |
| Financial Reporting & Records Owner | 2 | 0 | 2 |
| FinOps & Resource Architect | 2 | 0 | 2 |
| Frontend Specifications & UX Documentation Owner | 2 | 0 | 2 |
| Head of Engineering | 2 | 0 | 2 |
| Head of Specs Team | 2 | 0 | 2 |
| Head of UX & Design | 2 | 0 | 2 |
| Infrastructure & Operations Owner | 2 | 0 | 2 |
| Metrics Definitions & Analytics Canonical Owner | 2 | 0 | 2 |
| PMO Lead | 2 | 0 | 2 |
| Product Owner | 2 | 0 | 2 |
| QA Lead | 2 | 0 | 2 |
| QA & Testing Owner | 2 | 0 | 2 |
| Strategy Rules & System Intent Owner | 2 | 0 | 2 |
| **Total** | **44** | **0** | **44** |

## Agents Without Minimum Submissions

None — all 22 eligible agents met the 2-net-new minimum. (Facilitator excluded by design.)

## Ideas Available for Roadmap STEP 4

All 44 submissions below were `Submitted` at window close and available to the roadmap engine's STEP 4. Classification is performed there — see `claude/ideas/ideas_register.md` (window `IW-20261006-01`) for the dispositions. The Recommendation column is the submitter's own view.

| Idea ID | Agent | Title | Recommendation | Status |
|---------|-------|-------|----------------|--------|
| IDEA-ai-compliance-20261006-01 | AI Compliance & Governance Officer | Pin every Claude model ID in one backend module; two call sites use the floating `claude-haiku-4-5` alias while `ai_service.py` pins `claude-haiku-4-5-20251001` | Later | Submitted |
| IDEA-ai-compliance-20261006-02 | AI Compliance & Governance Officer | AI daily briefing and chat should state when the stop they quote was last recalculated, using v9.9's `stop_calculated_at` | Later | Submitted |
| IDEA-api-contracts-20261006-01 | API Contracts & Documentation Owner | Correct the documented losing-position stop formula: `position_endpoints.md` and the nightly job docstring say `entry − 5×ATR`, the code and §7.2 use `current price − 5×ATR` | Now | Submitted |
| IDEA-api-contracts-20261006-02 | API Contracts & Documentation Owner | `GET /positions/analyze` contract says 'safe to refresh' and settings changes 'do not affect open positions'; the endpoint actually rewrites stops for every open position using the current settings | Now | Submitted |
| IDEA-backend-engineering-20261006-01 | Backend Engineering Patterns Owner | Remove the silent ATR fallbacks: `add_position` invents ATR as 2% of entry, and `analyze_positions` sets a losing position's stop to its entry price when ATR is missing | Now | Submitted |
| IDEA-backend-engineering-20261006-02 | Backend Engineering Patterns Owner | Consolidate the grace-period length: it is hardcoded as 10 in four places and also read from the user-editable `settings.min_hold_days` (form default 5) by the alerts service | Now | Submitted |
| IDEA-base44-frontend-20261006-01 | Base44 Frontend Prompt Owner | Settings › Strategy Parameters shows wrong defaults (2×/3× ATR, 5 hold days) and helper text that contradicts §7.2 | Now | Submitted |
| IDEA-base44-frontend-20261006-02 | Base44 Frontend Prompt Owner | Put strategy numbers the UI displays in one frontend constants module instead of literals in each page | Later | Submitted |
| IDEA-challenger-20261006-01 | Challenger | Challenge: STEP 8.1's empty-Now-horizon soft gate has been cleared with Option (b) 'defer' 8 times running — is it still forcing a decision, or recording a default? | Later | Submitted |
| IDEA-challenger-20261006-02 | Challenger | Challenge: nine debt-clearance releases did not catch that the Settings page can seed 2×/3× ATR into live stops — debt slices should prioritise strategy-behaviour conformance over governance paperwork | Now | Submitted |
| IDEA-cybersecurity-20261006-01 | Cybersecurity & Trust Lead | Audit trail for strategy-parameter changes in Settings — who changed a multiplier, when, from what, to what | Later | Submitted |
| IDEA-cybersecurity-20261006-02 | Cybersecurity & Trust Lead | Re-assess the 'low-sensitivity' classification of the bundled `REACT_APP_API_KEY` now that it authorises writes that move live stops | Later | Submitted |
| IDEA-data-model-20261006-01 | Data Model & Domain Schema Owner | Record how each position's ATR was obtained (`atr_source`: fetched / user-entered / fallback) so invented ATRs are visible | Later | Submitted |
| IDEA-data-model-20261006-02 | Data Model & Domain Schema Owner | Constrain `exit_reason` to a defined set mapped to §8's three exit conditions | Later | Submitted |
| IDEA-director-of-hr-20261006-01 | Director of HR | Add a split-credit secondary tally to `compute_role_share_history.py` — at v9.9 every one of 35 stories had a compound Owner string, so the raw tally names no single role | Later | Submitted |
| IDEA-director-of-hr-20261006-02 | Director of HR | Name an owner for checking that UI copy restating strategy rules matches `strategy_rules.md` | Later | Submitted |
| IDEA-director-of-quality-20261006-01 | Director of Quality | Add a DoQ sign-off line for stories that touch stop math or strategy parameters: values checked against §5–§11 | Later | Submitted |
| IDEA-director-of-quality-20261006-02 | Director of Quality | Post-deploy synthetic check: every post-grace open position reports a non-null stop and an `active_atr_multiplier` in the §11 set | Later | Submitted |
| IDEA-financial-reporting-20261006-01 | Financial Reporting & Records Owner | Monthly P&L breakdown by §8 exit condition (stop / risk-off / manual) | Later | Submitted |
| IDEA-financial-reporting-20261006-02 | Financial Reporting & Records Owner | Snapshot the strategy parameters in force onto each closed trade so historical P&L stays attributable if §11 values change | Later | Submitted |
| IDEA-finops-20261006-01 | FinOps & Resource Architect | Stop page views from triggering a full price/ATR fetch and stop rewrite: `MarketRegime.list` calls `GET /positions/analyze` just to read the regime | Later | Submitted |
| IDEA-finops-20261006-02 | FinOps & Resource Architect | Inventory the 20 scheduled GitHub workflows: owner, purpose, cron, side effects, minutes | Later | Submitted |
| IDEA-frontend-specs-20261006-01 | Frontend Specifications & UX Documentation Owner | Trade Entry shows a stop and risk the system will not use: the Stop Price field is ignored by the backend, and the preview uses a 2× fallback instead of §5's 5× | Now | Submitted |
| IDEA-frontend-specs-20261006-02 | Frontend Specifications & UX Documentation Owner | Fix the UNKNOWN lifecycle tooltip: it only says 'set a stop and R-target', but UNKNOWN also appears after grace when price sits within ±0.5 ATR | Now | Submitted |
| IDEA-head-of-engineering-20261006-01 | Head of Engineering | One source for §11 stop parameters: the on-load stop recompute reads user-editable settings (form default 2×/3×) while the nightly job hard-codes 5×/2×, and the ratchet keeps whichever is tighter | Now | Submitted |
| IDEA-head-of-engineering-20261006-02 | Head of Engineering | Separate the regime read from the stop-writing analyze call, so viewing a page never moves a stop | Later | Submitted |
| IDEA-head-of-specs-20261006-01 | Head of Specs Team | Reconcile `position_lifecycle_states_registry.md` (5 states, trading days, ±0.5 ATR bands) with `strategy_rules.md` §9 (4 states, 10 calendar days) | Now | Submitted |
| IDEA-head-of-specs-20261006-02 | Head of Specs Team | Lint that flags UI text restating strategy formulas or numbers that differ from `strategy_rules.md` | Later | Submitted |
| IDEA-head-of-ux-20261006-01 | Head of UX & Design | Positions: the lifecycle badge and the Grace column disagree — a position inside §6's grace window can show a red LOSING badge, and grace copy says 'trading days' where §6 says calendar days | Now | Submitted |
| IDEA-head-of-ux-20261006-02 | Head of UX & Design | Separate governed strategy parameters from personal preferences on the Settings page | Later | Submitted |
| IDEA-infra-ops-20261006-01 | Infrastructure & Operations Owner | Two scheduled jobs write `current_stop` with different parameter sources (`daily-snapshot.yml` → analyze with settings; `nightly-stop-update.yml` → constants) | Now | Submitted |
| IDEA-infra-ops-20261006-02 | Infrastructure & Operations Owner | Record side effects for each scheduled workflow (which tables each one writes) | Later | Submitted |
| IDEA-metrics-20261006-01 | Metrics Definitions & Analytics Canonical Owner | Define how each stored exit reason maps to §8's three exit conditions for analytics | Later | Submitted |
| IDEA-metrics-20261006-02 | Metrics Definitions & Analytics Canonical Owner | Define a stop-freshness metric: hours since `stop_calculated_at` for each open position at view time | Later | Submitted |
| IDEA-pmo-lead-20261006-01 | PMO Lead | Add a known-false-positive allow-list to `scan_backlog_gate_conditions.py` — BLG-OPS-53 and BLG-FEAT-92 have been excluded by hand three rebalances running | Later | Submitted |
| IDEA-pmo-lead-20261006-02 | PMO Lead | Record each release's ready-pool / selected / leftover days in a structured history file, so STEP 7.3 reads it instead of being skipped | Now | Submitted |
| IDEA-product-owner-20261006-01 | Product Owner | Exit dialog should pre-select the exit reason the system already knows (stop breached after grace, or risk-off) instead of always defaulting to 'Manual Exit' | Now | Submitted |
| IDEA-product-owner-20261006-02 | Product Owner | Morning briefing: add a card for §8 exit recommendations (post-grace stop breach, risk-off) — it currently shows the non-§8 'Exit Zone' but not the strategy's own exit conditions | Now | Submitted |
| IDEA-qa-lead-20261006-01 | QA Lead | Playwright: Settings page with no settings row must show §11 defaults (5×, 2×, 10 days) | Now | Submitted |
| IDEA-qa-lead-20261006-02 | QA Lead | Unit test asserting every frontend strategy constant equals the §11 value | Later | Submitted |
| IDEA-qa-testing-20261006-01 | QA & Testing Owner | Parity test: for the same position inputs, the on-load analyze path and the nightly job must compute the same stop | Now | Submitted |
| IDEA-qa-testing-20261006-02 | QA & Testing Owner | Pin `add_position`'s handling of `stop_price` in a test, so the Trade Entry contract is explicit | Now | Submitted |
| IDEA-strategy-owner-20261006-01 | Strategy Rules & System Intent Owner | Ruling needed: are §11 parameters user-tunable through Settings at all? | Now | Submitted |
| IDEA-strategy-owner-20261006-02 | Strategy Rules & System Intent Owner | Ruling needed: is the five-state lifecycle badge a §9 state machine, or a separate display overlay that must defer to §9? | Now | Submitted |

## Parked Ideas Carried Forward (Not Resubmitted)

None.

## Notes

Build-and-ship candidates (§2.1 step 2a): 6 — `IDEA-base44-frontend-20261006-01` (Base44 Frontend Prompt Owner); `IDEA-frontend-specs-20261006-01` (Frontend Specifications & UX Documentation Owner); `IDEA-head-of-engineering-20261006-01` (Head of Engineering); `IDEA-head-of-ux-20261006-01` (Head of UX & Design); `IDEA-product-owner-20261006-01` (Product Owner); `IDEA-product-owner-20261006-02` (Product Owner). User-facing roles with none: None.

**Theme of this window.** A single read of the stop-loss surfaces (Settings, Trade Entry, Positions, Exit dialog) found that several things the UI tells the user about stops contradict `strategy_rules.md` §4–§9 or the code that actually runs. The most serious: `GET /positions/analyze`, which page loads call, computes stops from the user-editable settings row, while the nightly job uses fixed 5×/2× values, and the Settings form seeds 2×/3× when no row exists. The production settings row's values could not be read from this environment, so whether live stops have actually diverged from §7.2 is **unverified**. 19 of the 44 submissions converge on this stop-conformance theme from different roles; they are consolidated at STEP 4 along the backend/frontend/spec seams.

No `[FIELD REQUIRED]` flags — all 44 submissions passed the Submission Quality Check (specific `strategy_rules.md` citation, specific expected-value measure, all required fields non-empty).

```yaml
// ARTEFACT_STATUS
{
  "file": "window_summary_IW-20261006-01.md",
  "window_id": "IW-20261006-01",
  "filed_utc": "2026-10-06T11:45:21Z",
  "submission_count": 44,
  "agents_participating": 22,
  "status": "Complete"
}
```
