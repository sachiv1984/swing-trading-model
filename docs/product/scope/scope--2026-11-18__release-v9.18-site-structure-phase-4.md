Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.18
Cycle: 2026-11-18__release-v9.18
Last Updated: 2026-11-18 (created)

## Release Scope — v9.18 Site Structure & Usability, Phase 4 (stages 1–2) and first-time-right

40 items across 7 EPICs, 27.95 estimated days (the top of the confirmed ~24–28 day band, per "use full capacity"). Acceptance criteria: `claude/cycles/2026-11-18__release-v9.18/stage4_backlog_slice.md`. Roadmap section: `current_roadmap.md` §3 v9.18 (DL-089); all 19 committed items are in scope.

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Make the four mouse-only controls keyboard-operable (`BLG-FE-311`, P2) |
| S2-02 | EPIC-01 | Link the Exit dialog's labels to their inputs (`BLG-FE-312`, P2) |
| S2-03 | EPIC-01 | Say Telegram, not email, and show when an alert was not sent (`BLG-FE-318`) |
| S2-04 | EPIC-01 | Fix Alert History compact values (`BLG-FE-228`) |
| S2-05 | EPIC-01 | Re-review the accepted open-access risk (`BLG-SEC-46`, P2) |
| S2-06 | EPIC-01 | Measure Core Web Vitals and update the performance budget (`BLG-QA-271`) |
| S2-07 | EPIC-02 | Revise navigation.md and design_system.md for the Phase 4 target state (`BLG-UX-21`) |
| S2-08 | EPIC-02 | Move Strategy Benchmark into Performance and Ticker Universe into Settings (`BLG-FE-323`) |
| S2-09 | EPIC-02 | Make the quiet-day Dashboard a single line (`BLG-UX-11`) |
| S2-10 | EPIC-02 | Use one grace-period definition across the Dashboard (`BLG-FE-308`) |
| S2-11 | EPIC-02 | Offer "Plan this" on the Today list's New signals rows (`BLG-UX-13`) |
| S2-12 | EPIC-02 | Show machine-checkable checklist items as automatic status (`BLG-UX-19`) |
| S2-13 | EPIC-02 | Filter Trade History and Journal by rules followed or broken (`BLG-FE-320`) |
| S2-14 | EPIC-03 | Rename the Weekly Digest's journal completion figure (`BLG-SPEC-204`) |
| S2-15 | EPIC-03 | Rewrite the Weekly Digest as a readable weekly summary (`BLG-UX-15`) |
| S2-16 | EPIC-03 | Link the Weekly Digest figures to their pages (`BLG-UX-12`) |
| S2-17 | EPIC-03 | Measure the core loop and show this week's loop on the Weekly Digest (`BLG-FEAT-103`) |
| S2-18 | EPIC-04 | Design gate data-source, writer and worked-example checks (`BLG-GOV-422`, P2) |
| S2-19 | EPIC-04 | Unit-test pure frontend logic in CI (`BLG-QA-262`, P2) |
| S2-20 | EPIC-04 | Fail the axe scan on incomplete colour-contrast results (`BLG-QA-260`) |
| S2-21 | EPIC-04 | Script the locator-collision check and run it from commit-check (`BLG-QA-268`) |
| S2-22 | EPIC-04 | Require the pre-commit code review in execution_prompt.md (`BLG-GOV-420`, P2) |
| S2-23 | EPIC-04 | Enforce the prompt size budget on direct commits to main (`BLG-GOV-421`, P2) |
| S2-24 | EPIC-04 | Count an item as shipped only on a ✅ COMPLETE banner line (`BLG-GOV-388`) |
| S2-25 | EPIC-05 | Use one native-entry function on every position path (`BLG-BE-208`, P2) |
| S2-26 | EPIC-05 | Use the live FX rate, not a hard-coded 1.27 (`BLG-BE-213`, P2) |
| S2-27 | EPIC-05 | Handle a stock split on an open position (`BLG-BE-223`, P2) |
| S2-28 | EPIC-05 | Tag lifecycle transitions caused by the v9.12 currency correction (`BLG-BE-179`) |
| S2-29 | EPIC-05 | Keep GET /settings working when the change-log read fails (`BLG-BE-181`) |
| S2-30 | EPIC-05 | Make the Reports unrealised P&L match the Positions basis (`BLG-SPEC-203`) |
| S2-31 | EPIC-05 | Cache the Trade Entry ATR preview per ticker and market (`BLG-FE-225`) |
| S2-32 | EPIC-06 | Finish the on-demand Yahoo failure diagnosis (remainder) (`BLG-OPS-217`, P2) |
| S2-33 | EPIC-06 | Show "earnings unknown" when an earnings or gap-risk lookup fails (`BLG-FE-294`, P2) |
| S2-34 | EPIC-06 | Let the visual-baseline workflow push regenerated snapshots (`BLG-OPS-220`) |
| S2-35 | EPIC-06 | Seed staging's UK positions with the .L suffix (`BLG-OPS-205`) |
| S2-36 | EPIC-06 | Build the E2E bundle once per Playwright run (`BLG-OPS-206`) |
| S2-37 | EPIC-06 | Keep a bare root pytest out of the mutmut pilot tests (`BLG-QA-225`) |
| S2-38 | EPIC-06 | Run the settings change-log SQL against real Postgres in CI (`BLG-QA-226`) |
| S2-39 | EPIC-07 | Check daily briefing and chat output against §13.2 (`BLG-AI-29`) |
| S2-40 | EPIC-07 | Decide whether the debrief may say more than one restating sentence (`BLG-GOV-378`) |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| Phase 4 stage 3 (Clarity, 12 items) and stage 4 (Speed and polish, 8 items), 16.25 days | Held by §1.4c step 0: provisional release v9.19 in the programme plan (DL-089) | v9.19 |
| `BLG-TECH-21` (P2) | Standing §1.4c override: needs a dedicated single-EPIC release | v10.0 |
| `BLG-FEAT-73` (P1) | Data-quality gate; its re-check needs a production `trade_plans` count the governed environment cannot read | Unscheduled |
| `BLG-GOV-200`, `BLG-GOV-201` | No acceptance criteria (v9.17 closure §6 row 6: add ACs or kill before seating) | Unscheduled |
| `BLG-GOV-419` (remainder) | AC 2 needs a Release Planning run that clears a gate; none this run | Next run that clears a gate |
| `BLG-OPS-201` | Needs a full calendar month of production data | Not before 2026-12-01 |
| 193 other ready items (82.40 days) | Capacity | Later releases |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-11-18__release-v9.18
