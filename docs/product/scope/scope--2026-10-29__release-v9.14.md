Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.14
Cycle: 2026-10-29__release-v9.14
Last Updated: 2026-10-29

## Release Scope — v9.14

54 items across 7 EPICs, 28.00 estimated days, at the top of the ~24–28 day band ("use full capacity"). Acceptance criteria are in `claude/cycles/2026-10-29__release-v9.14/stage4_backlog_slice.md`. Ready pool, selection method and every disposition: `claude/cycles/2026-10-29__release-v9.14/run_manifest.md` Scope Construction.

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-OPS-193` — Restore eslint-config-react-app so the frontend builds and deploys again |
| S2-02 | EPIC-01 | `BLG-BE-192` — Compute the SPY market regime from Alpaca bars when Yahoo Finance fails |
| S2-03 | EPIC-01 | `BLG-BE-193` — Show an unknown market regime instead of silently defaulting to risk-on |
| S2-04 | EPIC-01 | `BLG-BE-194` — Use the last good GBP/USD rate, with its age, before the fixed 1.27 fallback |
| S2-05 | EPIC-01 | `BLG-BE-169` — Flag an FX fallback instead of applying it silently |
| S2-06 | EPIC-01 | `BLG-OPS-194` — Make the System Status Yahoo Finance check detect an outage |
| S2-07 | EPIC-01 | `BLG-BE-168` — Flag stale prices on GET /positions and the Positions page |
| S2-08 | EPIC-01 | `BLG-FE-214` — Make the stale-price explanation reachable on touch, keyboard and screen readers |
| S2-09 | EPIC-02 | `BLG-BE-190` — US position sizing divides the stop distance by the GBP/USD rate |
| S2-10 | EPIC-02 | `BLG-BE-188` — POST /positions/{id}/exit returns its documented 404 and 400, not 500 |
| S2-11 | EPIC-02 | `BLG-FE-231` — Daily Position Monitor stops suggesting "Stop Loss Hit" during the grace period |
| S2-12 | EPIC-02 | `BLG-BE-167` — GET /portfolio P&L handles a US position whose fill_price is NULL |
| S2-13 | EPIC-02 | `BLG-SPEC-190` — Positions data dictionary states that entry_price is stored in GBP |
| S2-14 | EPIC-02 | `BLG-SPEC-192` — Review-cadence grace suppression and the grace alert agree once grace has ended |
| S2-15 | EPIC-03 | `BLG-AI-20` — Journal summary catches advisory phrasings the trading-change check misses |
| S2-16 | EPIC-03 | `BLG-AI-21` — Daily briefing ticker caveat ignores indicator and macro acronyms |
| S2-17 | EPIC-03 | `BLG-AI-22` — Chat stop-time note is not attributed to the focus ticker when a sentence names another ticker |
| S2-18 | EPIC-03 | `BLG-AI-19` — Monthly P&L narrative scan stops flagging retrospective and discourse wording |
| S2-19 | EPIC-03 | `BLG-BE-164` — A debrief that fails compliance then errors writes one audit row |
| S2-20 | EPIC-03 | `BLG-BE-165` — Stop recalculation times in briefing and chat are converted to UTC |
| S2-21 | EPIC-03 | `BLG-BE-166` — Run the claude_audit_log column checks once per process |
| S2-22 | EPIC-03 | `BLG-BE-163` — Retire the unused POST /trade-plans/{plan_id}/generate-thesis endpoint |
| S2-23 | EPIC-03 | `BLG-GOV-178` — First live quarterly AI output sample against the §13 boundary |
| S2-24 | EPIC-04 | `BLG-FEAT-99` — Monthly P&L breakdown by §8 exit condition |
| S2-25 | EPIC-04 | `BLG-FE-213` — Recent Trades glyph and amount agree at a half-penny loss |
| S2-26 | EPIC-04 | `BLG-FE-215` — Pluralise the month counts in the monthly P&L summary fallback |
| S2-27 | EPIC-04 | `BLG-FE-216` — Keep a generated monthly P&L summary visible after switching tax year and back |
| S2-28 | EPIC-04 | `BLG-FE-217` — Group /reports endpoints on the System Status page |
| S2-29 | EPIC-05 | `BLG-QA-237` — Cover the Positions-page Exit modal submit in Playwright |
| S2-30 | EPIC-05 | `BLG-QA-235` — Staging visual check of the layout changed by tailwind-merge in cn() |
| S2-31 | EPIC-05 | `BLG-QA-238` — Pre-commit OpenAPI contract check reads staged content |
| S2-32 | EPIC-05 | `BLG-QA-93` — Confirm the conftest.py AST scan still covers every backend module |
| S2-33 | EPIC-05 | `BLG-QA-214` — Behaviour test: the grace warning ignores settings.min_hold_days |
| S2-34 | EPIC-05 | `BLG-QA-215` — Assert the stop-details tooltip time under a non-UTC browser timezone |
| S2-35 | EPIC-05 | `BLG-QA-216` — Assert the applied theme in every Reports/Notifications axe scan |
| S2-36 | EPIC-05 | `BLG-QA-218` — Stop test files adding backend/services/ to sys.path |
| S2-37 | EPIC-05 | `BLG-QA-219` — Stop the ⌘K hint toast intercepting the chat submit click in SC-AC-03 |
| S2-38 | EPIC-06 | `BLG-OPS-21` — Arc 2 compute cost review |
| S2-39 | EPIC-06 | `BLG-OPS-85` — Compute cost trending by feature area |
| S2-40 | EPIC-06 | `BLG-OPS-105` — CI pipeline runtime audit |
| S2-41 | EPIC-06 | `BLG-OPS-186` — Daily AI cost check covers the last hours of the day |
| S2-42 | EPIC-06 | `BLG-OPS-188` — Make ci-usage-report.yml's monthly commit succeed |
| S2-43 | EPIC-06 | `BLG-SEC-43` — Per-environment CORS allow-list |
| S2-44 | EPIC-07 | `BLG-GOV-397` — check_execution_state_consistency.py checks deviations_filed and the escalation map |
| S2-45 | EPIC-07 | `BLG-GOV-398` — Give the gate scan's "gating item shipped" findings a write-back path |
| S2-46 | EPIC-07 | `BLG-SPEC-77` — Document the gate-status indicator as a reusable component pattern |
| S2-47 | EPIC-07 | `BLG-SPEC-189` — risk_dashboard.md names only fields GET /portfolio returns |
| S2-48 | EPIC-07 | `BLG-SPEC-191` — Align Appendix F's effort-weighted PVR table and status with the script |
| S2-49 | EPIC-07 | `BLG-SPEC-193` — Trade plan contract lists the 7 DS-21 statuses |
| S2-50 | EPIC-07 | `BLG-GOV-184` — Confirm "win rate" is computed the same way on every surface |
| S2-51 | EPIC-07 | `BLG-GOV-185` — Add a changelog section to metrics_definitions.md |
| S2-52 | EPIC-07 | `BLG-GOV-186` — §13 boundary worked examples |
| S2-53 | EPIC-07 | `BLG-GOV-189` — Governance overhead audit |
| S2-54 | EPIC-07 | `BLG-GOV-191` — Spec debt aging report |

### Items explicitly deferred

| Item | Reason |
|------|--------|
| `BLG-TECH-21` (P2) | §1.4c override, as at v9.10–v9.13: a dedicated single-EPIC release (`Provisional-Target: v10.0`) |
| `BLG-FEAT-73` (P1), `BLG-FEAT-76` | Data-quality warnings; re-checks suspended until 2026-11-09 or 10 new linked `trade_plans` (§1.4a.1 count 2 of 4) |
| `BLG-QA-220`, `BLG-OPS-190`, `BLG-SPEC-195` | Seated by the mechanical selection, then displaced by the Product Owner override that seated `BLG-QA-238`, `BLG-GOV-397`, `BLG-GOV-398` |
| 99 further ready items (52.75d) | Capacity. The largest are `BLG-GOV-379` (4.0d) and `BLG-GOV-380`, `BLG-BE-186`, `BLG-SPEC-206`, `BLG-QA-230` (1.5d each). Includes 27 unselected items tagged `Provisional-Target: v9.14` (no selection weight, `ESC-CLOSE-20260923-01`) |
| `BLG-FE-39`, `BLG-QA-21`, `BLG-QA-22`, `BLG-QA-23`, `BLG-GOV-26`, `BLG-FEAT-26` | Gated on "PT-04 shipped" (met at v6.1), but not on any scan list, so outside §1.3a's disposition authority. Routed to `groom backlog` |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
