Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.15
Cycle: 2026-11-03__release-v9.15
Last Updated: 2026-11-06

Superseded by: v9.15 ship — 2026-11-06
Changelog: docs/product/changelog.md#v9.15
Verification report: claude/cycles/2026-11-03__release-v9.15/verification_report.md
Cycle: 2026-11-03__release-v9.15

## Release Scope — v9.15

45 items across 7 EPICs, 28.00 estimated days, at the top of the ~24–28 day band ("use full capacity"). The release opens Phase 1 of the Site Structure & Usability programme (DL-088). Acceptance criteria are in `claude/cycles/2026-11-03__release-v9.15/stage4_backlog_slice.md`. The ready pool, selection method and every disposition are in `claude/cycles/2026-11-03__release-v9.15/run_manifest.md` Scope Construction.

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-FE-244` — Show the pre-entry checks on every route into Trade Entry, not only from a Trade Plan |
| S2-02 | EPIC-01 | `BLG-FE-245` — Pre-fill Trade Entry's FX rate from the live rate, not a fixed 1.27 |
| S2-03 | EPIC-01 | `BLG-FE-246` — Label the FX rate the same way on entry and exit |
| S2-04 | EPIC-01 | `BLG-FE-243` — Default trade, exit and cash dates to the user's local date, not the UTC date |
| S2-05 | EPIC-01 | `BLG-FE-222` — Normalise the Trade Entry ticker the same way for the ATR preview and for save |
| S2-06 | EPIC-01 | `BLG-BE-173` — Trail Stop modal's ATR trail value uses a hardcoded 2.0 multiplier and no breakeven floor |
| S2-07 | EPIC-01 | `BLG-FE-219` — Label signal cost as including fees, and make the zero-ATR sizing reason plain English |
| S2-08 | EPIC-02 | `BLG-SPEC-214` — Navigation spec v2: job-based areas, plus a UI-label section in the glossary |
| S2-09 | EPIC-02 | `BLG-SPEC-215` — Dashboard spec: a prioritised "Today" action list |
| S2-10 | EPIC-02 | `BLG-SPEC-216` — Spec for one Journal area combining reflections, red flags and position notes |
| S2-11 | EPIC-02 | `BLG-FE-248` — Use one name per page and action across sidebar, page headings and command palette |
| S2-12 | EPIC-02 | `BLG-FE-247` — Remove the legacy widget Dashboard route and its duplicate command-palette entry |
| S2-13 | EPIC-02 | `BLG-FE-249` — Set a browser-tab title for each page |
| S2-14 | EPIC-02 | `BLG-FE-266` — Fix three small chrome defects: version label, What's New heading, sidebar height |
| S2-15 | EPIC-03 | `BLG-FE-239` — Trade History counts a break-even trade as a win |
| S2-16 | EPIC-03 | `BLG-FE-240` — Dashboard win-rate widgets are fed from open positions only |
| S2-17 | EPIC-03 | `BLG-FE-218` — Align the View Trail modal wording with the read-only ruling |
| S2-18 | EPIC-03 | `BLG-FE-220` — Fix the Strategy Benchmark Rebalance badge's contrast and settle tinted vs filled exit-reason badges |
| S2-19 | EPIC-03 | `BLG-BE-170` — Price-alert duplicate fallback returns 500 when the threshold has more than 4 decimal places |
| S2-20 | EPIC-03 | `BLG-BE-171` — Use the deploy date, not the ruling date, as strategy v1.15's effective date |
| S2-21 | EPIC-03 | `BLG-BE-172` — Show the code-written fallback when the monthly P&L summary's regeneration call fails |
| S2-22 | EPIC-03 | `BLG-BE-174` — Gap-risk weekend statistic: pick it by the exchange calendar and count ordinary weekends |
| S2-23 | EPIC-03 | `BLG-SPEC-198` — Open-position pnl: code uses the live FX rate and does not deduct fees; the dictionary says entry-time FX, fees deducted |
| S2-24 | EPIC-04 | `BLG-AI-23` — Review logged briefing ticker-caveat tokens for further non-tickers |
| S2-25 | EPIC-04 | `BLG-AI-24` — Journal summary advisory check: remaining false positives and misses |
| S2-26 | EPIC-04 | `BLG-AI-25` — Chat stop-time focus rule: ignore common upper-case non-ticker words |
| S2-27 | EPIC-04 | `BLG-AI-26` — Journal summary advisory check: do not flag "could/may help explain" |
| S2-28 | EPIC-04 | `BLG-GOV-194` — §13 boundary language clarity pass — AI journal summarisation |
| S2-29 | EPIC-05 | `BLG-OPS-48` — ANTHROPIC_API_KEY 6-month scope audit |
| S2-30 | EPIC-05 | `BLG-OPS-190` — Rebalance-exit generation should check that today's screener run completed |
| S2-31 | EPIC-05 | `BLG-OPS-191` — Skip the five code-test workflows on governance-only and docs-only pushes |
| S2-32 | EPIC-05 | `BLG-OPS-192` — Tell "no qualifying tickers" apart from "momentum run missing" in the month-end rebalance job |
| S2-33 | EPIC-05 | `BLG-OPS-197` — Record the weekly market-data call-volume baseline from production |
| S2-34 | EPIC-06 | `BLG-SPEC-194` — Clear the 8 pre-existing success-example drifts so check_contract_example_freshness.py exits 0 |
| S2-35 | EPIC-06 | `BLG-SPEC-196` — Re-apply NOT NULL on positions.portfolio_id and positions.total_cost |
| S2-36 | EPIC-06 | `BLG-SPEC-197` — Apply DS-17's open-position unique index to staging |
| S2-37 | EPIC-07 | `BLG-GOV-404` — Gate scan treats a shipped roadmap feature ID (PT-xx, SI-xx, PO-xx) as a met gate |
| S2-38 | EPIC-07 | `BLG-QA-240` — Make the execution-state consistency check count EPICs not yet initialised as pending |
| S2-39 | EPIC-07 | `BLG-QA-220` — Behavioural tests for live holding days in the compliance and AI briefing readers |
| S2-40 | EPIC-07 | `BLG-QA-221` — Real-Postgres tests for the ai_audit_log UUID[] path and the claude_audit_log daily cost sum |
| S2-41 | EPIC-07 | `BLG-QA-222` — Extend the utils.* leak guard to attributes patched on the real utils modules |
| S2-42 | EPIC-07 | `BLG-QA-224` — Make SC-TS-* Playwright scenario IDs unique across tests/e2e |
| S2-43 | EPIC-07 | `BLG-GOV-193` — Escalation SLA breach dry-run test |
| S2-44 | EPIC-07 | `BLG-GOV-195` — Strategic exclusions review cadence |
| S2-45 | EPIC-07 | `BLG-GOV-196` — Sunset review for Priority 3 — Deferred initiatives |

### Items explicitly deferred

| Item | Reason |
|------|--------|
| `BLG-FE-253`, `BLG-FE-255`, `BLG-FE-256`, `BLG-FE-257`, `BLG-FE-259`, `BLG-FE-260`, `BLG-FE-261`, `BLG-FE-262`, `BLG-FE-263`, `BLG-FE-264` | Site Structure & Usability Phase 2/3 items. Ungated, but held to their DL-088 provisional releases (v9.16/v9.17) by Product Owner override (2026-11-03). Four are P2 (`BLG-FE-255`, `256`, `260`, `264`; 8.5d), so the P2-first step would otherwise have seated them. |
| `BLG-FE-250`, `BLG-FE-251`, `BLG-FE-252`, `BLG-FE-254`, `BLG-FE-258`, `BLG-FE-265` | Not ready: each depends on a spec or item not yet shipped. `BLG-SPEC-214`, `215` and `216` are written in this release; `BLG-FE-264` is held. |
| `BLG-OPS-195` | Not ready: it alerts against the `data_pipeline_cost_baseline.md` §4 weekly baseline, which reads "Pending" until `BLG-OPS-197` (ST-33, conditional) records production data. |
| `BLG-OPS-201` | Not ready: it needs a complete calendar month of production data after the v9.14 ST-39 report merged (2026-10-30), so not before 2026-12-01. |
| `BLG-TECH-21` (P2) | Standing §1.4c override (dedicated single-EPIC release; `Provisional-Target: v10.0`), as at v9.10–v9.14. |
| `BLG-FEAT-73` (P1), `BLG-FEAT-76` | Data-quality warnings, read individually. `BLG-FEAT-73` is not re-checked before 2026-11-09 or 10 new linked `trade_plans`; `BLG-FEAT-76` is hard-blocked on it. |
| `BLG-GOV-185`, `BLG-GOV-192`, `BLG-GOV-400`, `BLG-OPS-203` | Already met or resolved, so excluded rather than seated. `BLG-GOV-185`: `metrics_definitions.md` Appendix D is the changelog (v9.14 ST-51, deferred at planning). `BLG-GOV-192`: `run audit` has run a §14 drift check every 3 cycles since 2026-03-13. `BLG-GOV-400`: met by this run. `BLG-OPS-203`: resolved 2026-10-30. All are for `groom backlog` to archive. |
| `BLG-GOV-399` | Ready, but the round-robin did not reach it (it needs a production read). It tracks `ESC-EXEC-20260910-01`'s deferred trigger. |
| 103 other ready items (47.55d) | Capacity. The largest unselected items are `BLG-GOV-379` (4.0d) and `BLG-GOV-380`, `BLG-BE-186` and `BLG-QA-230` (1.5d each). |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*
