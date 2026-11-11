Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.16
Cycle: 2026-11-06__release-v9.16
Last Updated: 2026-11-11

Superseded by: v9.16 ship — 2026-11-11
Changelog: docs/product/changelog.md#v9.16
Verification report: claude/cycles/2026-11-06__release-v9.16/verification_report.md
Cycle: 2026-11-06__release-v9.16

## Release Scope — v9.16

30 items across 7 EPICs, 27.95 estimated days, at the top of the ~24–28 day band ("use full capacity"). The release delivers Phase 2 of the Site Structure & Usability programme (DL-088) in full: navigation, the Dashboard "Today" list, the signal-to-entry flow and the first semantic colour tokens. Acceptance criteria are in `claude/cycles/2026-11-06__release-v9.16/stage4_backlog_slice.md`. The ready pool, selection method and every disposition are in `claude/cycles/2026-11-06__release-v9.16/run_manifest.md` Scope Construction.

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-FE-250` — Build the job-based sidebar and surface Trade Plans and Research |
| S2-02 | EPIC-01 | `BLG-FE-251` — Add a parent link on detail pages |
| S2-03 | EPIC-01 | `BLG-FE-252` — Give each dead-end page an onward next-step link |
| S2-04 | EPIC-01 | `BLG-FE-253` — Anchor the digest's Risk Dashboard link to the right section |
| S2-05 | EPIC-02 | `BLG-FE-271` — Require the acknowledgement on plan-linked Trade Entry when the plan's checks were WARN/FAIL |
| S2-06 | EPIC-02 | `BLG-FE-254` — Build the "Today" action list on the Dashboard |
| S2-07 | EPIC-02 | `BLG-FE-255` — Add "Plan this" to Signals and Screener rows |
| S2-08 | EPIC-02 | `BLG-FE-256` — On Trade Plan, show the suggested size before asking for shares |
| S2-09 | EPIC-03 | `BLG-FE-264` — Semantic colour tokens for the base, card and table shells |
| S2-10 | EPIC-03 | `BLG-FE-223` — Inputs apply dark:text-slate-400 to typed text instead of the placeholder |
| S2-11 | EPIC-04 | `BLG-OPS-214` — Rotate the Anthropic API key (overdue since 2026-08-25) and revoke the old key |
| S2-12 | EPIC-04 | `BLG-OPS-213` — Stop injecting REACT_APP_ANTHROPIC_API_KEY into the public GitHub Pages build |
| S2-13 | EPIC-04 | `BLG-OPS-197` — Record the weekly market-data call-volume baseline from production |
| S2-14 | EPIC-04 | `BLG-OPS-198` — Record the full screener run p50/p95 baseline from production |
| S2-15 | EPIC-04 | `BLG-OPS-199` — Fail the staging smoke host check when the backend reports no Render service ID |
| S2-16 | EPIC-05 | `BLG-BE-175` — Exiting a US position with a NULL fill_price fails in the P&L arithmetic |
| S2-17 | EPIC-05 | `BLG-BE-176` — Lifecycle badge and Risk page disagree for a US row with no fill_price and no fx_rate |
| S2-18 | EPIC-05 | `BLG-BE-177` — Frozen-stop marker is not written when the on-load recompute has no live price |
| S2-19 | EPIC-05 | `BLG-AI-27` — Read production briefing ticker-caveat tokens and add any non-tickers |
| S2-20 | EPIC-05 | `BLG-AI-28` — Handle `_NON_TICKER_WORDS` entries that are also real tickers deliberately |
| S2-21 | EPIC-05 | `BLG-SPEC-195` — Journal summary: remove the stale AI_MODEL override line, or cost the model actually used |
| S2-22 | EPIC-05 | `BLG-SPEC-200` — Add the 11 missing positions columns to the positions data dictionary |
| S2-23 | EPIC-05 | `BLG-SPEC-201` — Point settings.md at the moved strategy constants module |
| S2-24 | EPIC-06 | `BLG-QA-21` — Arc 2 end-to-end QA protocol |
| S2-25 | EPIC-06 | `BLG-QA-22` — Arc 2 DoQ standards review |
| S2-26 | EPIC-06 | `BLG-QA-23` — Trade plan lifecycle end-to-end test |
| S2-27 | EPIC-06 | `BLG-FE-39` — Arc 2 user journey map |
| S2-28 | EPIC-07 | `BLG-GOV-413` — Split-achievability carve-out: close a source item whose whole remainder has its own backlog items |
| S2-29 | EPIC-07 | `BLG-GOV-26` — Arc velocity tracking dashboard |
| S2-30 | EPIC-07 | `BLG-GOV-198` — Base44 prompt versioning convention |

### Items explicitly deferred

| Item(s) | Reason |
|---------|--------|
| `BLG-FE-257`, `258`, `259`, `260` (P2), `261`, `262`, `263`, `265` | Site Structure & Usability Phase 3, provisional v9.17. Held by `release_planning_prompt.md` §1.4c step 0 (programme-phase hold, first use). 20.50d. |
| `BLG-UX-08` | Programme close-out (v9.18). Gated on every other programme item. |
| `BLG-BE-205` | The Today list's "Stops moved" data. Ready, but the round-robin did not reach it; ST-06 ships without that group (`dashboard.md` §1B). |
| `BLG-TECH-21` (P2) | Dedicated-release constraint; `Provisional-Target: v10.0`. Standing §1.4c override. |
| `BLG-OPS-48`, `BLG-AI-23` | Split-achievability: seated at v9.15, with their remainders tracked by `BLG-OPS-214`/`213`/`BLG-SPEC-223` and `BLG-AI-27`. ST-28 (`BLG-GOV-413`) fixes the pattern; the next `groom backlog` banners them. |
| `BLG-GOV-178`, `BLG-GOV-192` | `BLG-GOV-178`'s remainder is `BLG-GOV-399`. `BLG-GOV-192` is already met (v9.15 finding). |
| `BLG-GOV-408` | A `run roadmap` input (v9.15 Carry-Forward #3). |
| `BLG-OPS-195`, `BLG-OPS-201` | Dependencies unmet: `BLG-OPS-197`'s baseline (ST-13); one full month of production data (not before 2026-12-01). |
| `BLG-FEAT-73` (P1), `BLG-FEAT-76` | Data-quality warnings, read individually. `BLG-FEAT-73` is not re-checked before 2026-11-09 or 10 new linked `trade_plans`; `BLG-FEAT-76` is hard-blocked on it. |
| `BLG-GOV-200`, `BLG-FE-224`, `BLG-AI-29`, `BLG-BE-178`, `BLG-QA-223`, `BLG-OPS-205`, `BLG-SPEC-207` | Displaced by the Product Owner's Phase 2 override (3.55d); otherwise the mechanical selection would have seated them. |
| 122 other ready items (53.20d, including `BLG-BE-205` above) | Capacity. The largest unselected items are `BLG-GOV-379` (4.0d) and `BLG-GOV-380`, `BLG-BE-186`, `BLG-QA-230` and `BLG-BE-205` (1.5d each). |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*
