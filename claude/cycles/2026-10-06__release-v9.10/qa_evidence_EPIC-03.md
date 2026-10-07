Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-07 (agent-mediated DoQ sign-off, user-directed); prior — 2026-10-07 (pre-PR review findings recorded); prior — 2026-10-07 (EPIC-03 consolidation, STEP 3.2.A)

# QA Evidence — EPIC-03 — Lifecycle & Gap-Risk Strategy Rulings

**EPIC:** EPIC-03 — Lifecycle & Gap-Risk Strategy Rulings
**Cycle:** 2026-10-06__release-v9.10
**Sprint goal:** Make every live stop come from one §11 parameter source, and show the ATR, multiplier, recalculation source and already-known exit conditions behind each position (BLG-BE-138, BLG-FE-193, BLG-FE-198), while clearing v9.10's lifecycle/gap-risk rulings and AI-governance, ops and QA hygiene items.
**Test scenarios used:** `tests/test_position_lifecycle.py`, `tests/e2e/lifecycle-badge-grace-calendar-days.spec.js`, `tests/e2e/epic01-v34-lifecycle.spec.js`, `tests/test_gap_risk.py`, `tests/e2e/gap-risk-flag.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-11 | `position_lifecycle_states_registry.md` v1.2 §Relationship to strategy_rules.md §9; `data_model.md` v2.52 Position Lifecycle; `position_endpoints.md` v2.11.0 | Ruling (ESC-EXEC-20261006-03): the badge is a display overlay that defers to §9, with no §9 amendment. `classify_position` now uses §9's native P&L sign after grace (LOSING ≤ entry, PROFITABLE > entry, EXIT ZONE a PROFITABLE sub-state at 2R). The ±0.5 ATR bands and `flat_after_grace` are removed from code, contract, OpenAPI 3.21.0, positions.md v2.13 and the Positions.js tooltip map. The LOSING tooltip no longer describes the removed 0.5 ATR rule. Commit `05ad3ecf`. | AC 1: ruling recorded with Strategy Rules & System Intent Owner sign-off (escalation record, registry). AC 2: registry and §9 no longer conflict; no §9 amendment needed. | Pass | None found |
| ST-12 | `positions.md` §Grace Precedence and UNKNOWN Reasons; `position_endpoints.md` v2.9.0 | GRACE takes precedence for 10 calendar days; label `GRACE — {n}d left`; UNKNOWN tooltip by `lifecycle_reason`. Commit `0e8a431b`. | AC 1–3 met (SC-LBG-01..04, SC-LS-02, SC-GP-02). The post-grace `flat_after_grace` copy it shipped is retired by ST-11, as its design record anticipated. | Pass | None found |
| ST-13 | v9.10 addendum to `decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`; `strategy_rules.md` §4.2.3, §13.3 | Ruling (ESC-EXEC-20261006-04), recorded as a dated addendum: the earnings trigger applies to US positions only; day 0 is not flagged; the window runs to the next trading day. No `strategy_rules.md` wording change. Commit `05ad3ecf`. | AC 1: dated addendum recorded. AC 2: code, §13.3/§4.2.3 and the record agree on markets and day offsets. AC 3: `test_gap_risk.py` covers a UK position (`test_uk_position_never_flagged_and_earnings_not_fetched`) and day 0 (`test_day_0_not_flagged`). | Pass | None found (§13.3 descriptive text follow-up: BLG-GOV-376) |
| ST-14 | `position_endpoints.md` v2.12.0 §GET /positions/{position_id}/gap-risk; `openapi.yaml` 3.22.0; `positions.md` v2.14 §Gap Risk Reason Labels; v6.9 `ux_spec.md` v1.1 §3–§6 | `weekend_hold` trigger removed (`reasons` enum is now `["earnings"]`). Trading-session window (`_days_to_next_trading_day`). Label "Earnings due by next trading session" in both views. Module docstring cites the §13 record. Binding Conditions 1–8 re-confirmed in the addendum. Commit `05ad3ecf`. | AC 1: no uniform trigger (`test_no_trigger_flags_every_position_identically`). AC 2: Friday view flags Monday earnings (`test_friday_view_flags_monday_earnings`). AC 3: labels, ux_spec §5, positions.md and code agree (SC-GR-03/04/06/08). AC 4: docstring citation (`test_module_docstring_cites_section13_review_record`). AC 5: unit and Playwright updated and passing; contract and OpenAPI updated in the same commit. AC 6: Strategy Rules & System Intent Owner sign-off on BC 1–8 (addendum table). | Pass | None found (BLG-GOV-376) |

**Story-level domain sign-offs (BLG-GOV-14):** ST-11, ST-13 and ST-14 AC 6 were signed by the Strategy Rules & System Intent Owner (agent-mediated, `execution_prompt.md` §5.3, on the user's explicit direction, 2026-10-07). The record is `execution_escalations.md` ESC-EXEC-20261006-03/04, plus the gap-risk addendum's sign-off. All three are cleared in `execution_state.json` `sign_off_record`.

**QA test coverage:**
- Scenarios run: `tests/test_position_lifecycle.py` + `tests/test_position_lifecycle_states_registry.py` (41), `tests/test_gap_risk.py` (19), full pytest suite 2192 passed / 14 skipped; Playwright `gap-risk-flag.spec.js` SC-GR-01..08 and `lifecycle-badge-grace-calendar-days.spec.js` SC-LBG-01..05 (15/15). All local.
- Regression areas checked: `epic01-v34-lifecycle`, `epic01-v70-grid-badge-parity`, `plan-vs-reality`, `position-review-cadence-nudge`, `positions-pnl-columns`, `compliance-recheck` (54/54). Drift checks: OpenAPI drift, local OpenAPI/contract completeness, contract heading lint, API performance baseline, UI copy lint, all passing.
- Cross-spec selector updates (STEP 3.1.A step 13): `gap-risk-flag.spec.js` SC-GR-03/06 moved off the removed `weekend_hold` payloads; SC-LBG-04's `flat_after_grace` case now asserts the null fallback.
- Known deviations: None found.

**Frontend testing gate (CLAUDE.md §2, LL-v3.1-EX-01):** every observable AC is covered by a named Playwright scenario: the LOSING tooltip by SC-LBG-05, the UNKNOWN tooltips by SC-LBG-04, the gap-risk label in both views by SC-GR-04/06/08, and the absence of a weekend label by SC-GR-03. The tooltip changes are wording-only (FI-P3-02). No AC is "code review only". No focus or interaction-timing AC is introduced, so the environment-parity sub-clause does not apply. CI confirmation will be recorded once the branch's GitHub Actions run completes.

**Same-EPIC cross-story testing-gap consistency check:** no story in this EPIC filed a testing-gap backlog item. BLG-BE-147 (below) is a behaviour gap specific to ST-12's alert path, and no sibling story shares it. Nothing to propagate.

**Real CI confirmation (pre-PR, branch push):** all workflows green on `05ad3ecf` (code head), including Playwright E2E Acceptance Tests, CI Pytest Suite, Critical-Path Smoke, Service Layer Coverage, Golden Output Regression, Portfolio Integration and Endpoint Coverage. Also green on `ab73ad2f` (state and evidence only).

**Pre-PR agent-mediated review (2026-10-07, on behalf of Director of Quality and Product Owner, §5.3 / OA-6, pending human confirmation):** both verdicts ⚠️ Approved with Comments, with no blocking defects. Non-blocking findings, filed:
- **BLG-BE-147** (P2): the grace alert filter, the "Day N of 10" label and review-cadence suppression still use `days_in_state`, not calendar days since entry. A post-deploy state reset can hide the day-8/9 alert.
- **BLG-BE-148** (P3): the gap-risk next session is weekday-only in UTC. It misses a flag before a Monday holiday and in the 00:00–05:00 UTC window, failing safe.
- **BLG-BE-149** (P3): the Risk page's `display_status` uses GBP P&L, while the badge uses native P&L.

Product Owner comments: the v9.10 changelog should state the visible gap-flag changes (no UK flag, no Friday-only flag, no day-0 flag). The human should confirm the UK and day-0 rulings, which were agent-mediated. BLG-GOV-376 tracks the stale §13.3 text. The combined comment is drafted for posting when the PR opens. The DoQ sign-off block is still blank, so the PR is not opened (§3.2.B).

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object (N/A: no new URL construction; `useGapRisk.js` and the Positions page fetches are unchanged)
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-10-07
- Comments: Performed on the user's explicit direction (2026-10-07) to sign off EPIC-03 as Director of Quality; pending human confirmation. Verdict: **⚠️ Approved with Comments**, with no blocking defects. All ACs across ST-11 to ST-14 pass. Every observable AC is covered by a named Playwright scenario (SC-LBG-01..05, SC-LS-02, SC-GP-02, SC-GR-01..08), and every backend rule by a unit test (`test_position_lifecycle.py`, `test_gap_risk.py`). None is code-review only. There are no focus or interaction-timing ACs, so the environment-parity sub-clause does not apply. Real CI is green on `05ad3ecf` (code head), including Playwright E2E Acceptance Tests and CI Pytest Suite. Later commits (`ab73ad2f`, `f9408cad`) are state, evidence and backlog only. Story-level Strategy Rules & System Intent Owner sign-offs (ST-11, ST-13, ST-14 AC 6) were agent-mediated and are cleared (BLG-GOV-14). Non-blocking follow-ups: BLG-BE-147 (P2, grace alert basis), BLG-BE-148 (P3, holiday/US-date calendar), BLG-BE-149 (P3, Risk page `display_status` basis), BLG-GOV-376 (`strategy_rules.md` §13.3 text). The governance-drift self-consistency check is N/A: no story bumped `OPERATIONAL_GUIDE.md`.
