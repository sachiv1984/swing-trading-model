Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.11
Cycle: 2026-10-08__release-v9.11
Last Updated: 2026-10-08

## Release Scope — v9.11

43 items across 6 EPICs, 27.975 estimated days, at the top of the ~24–28 day band ("use full capacity"). Acceptance criteria are in `claude/cycles/2026-10-08__release-v9.11/stage4_backlog_slice.md`.

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-BE-152` — Give the post-trade debrief R achieved, the stop at exit and entry slippage |
| S2-02 | EPIC-01 | `BLG-BE-150` — Verify all six AI features after the PR #1921 import fix, and file the escaped-defect note |
| S2-03 | EPIC-01 | `BLG-BE-151` — Keep the AI-output sampling hook from breaking or hiding errors in AI responses |
| S2-04 | EPIC-01 | `BLG-QA-217` — Test that every backend module imports with only backend/ on the path |
| S2-05 | EPIC-01 | `BLG-FE-205` — Make the debrief Regenerate button recognisable, and show failures and the generated time |
| S2-06 | EPIC-01 | `BLG-AI-08` — claude_audit_log: add prompt_hash and response_length, and log failed model calls |
| S2-07 | EPIC-01 | `BLG-AI-09` — State in the daily-briefing system prompt that output is advisory and cannot execute trades |
| S2-08 | EPIC-01 | `BLG-BE-141` — AI briefing and chat state when a quoted stop was last recalculated |
| S2-09 | EPIC-01 | `BLG-BE-142` — Pin every Claude model ID in one backend module |
| S2-10 | EPIC-02 | `BLG-BE-154` — Remove the hard-coded ×1.38 US price fallback from GET /portfolio, and flag stale prices |
| S2-11 | EPIC-02 | `BLG-FE-206` — Position Risk table: GBP entry prices, and grace-period stops shown as not enforced |
| S2-12 | EPIC-02 | `BLG-BE-153` — GET /portfolio computes holding_days live from entry_date |
| S2-13 | EPIC-02 | `BLG-BE-155` — Stop Dist % computed in native currency for US positions |
| S2-14 | EPIC-02 | `BLG-BE-147` — Grace alert filter and "Day N of 10" label use calendar days since entry |
| S2-15 | EPIC-02 | `BLG-FE-204` — Recent Trades glyph treats a P&L that rounds to £0.00 as break-even |
| S2-16 | EPIC-03 | `BLG-BE-143` — Rule on and test stop recalculation during grace |
| S2-17 | EPIC-03 | `BLG-FR-06` — Snapshot the strategy parameters in force onto each closed trade |
| S2-18 | EPIC-03 | `BLG-OPS-179` — Post-deploy synthetic check for post-grace stops and §11 multipliers |
| S2-19 | EPIC-03 | `BLG-BE-140` — Read-only market-regime source, so viewing regime no longer runs the stop-writing analyze call |
| S2-20 | EPIC-03 | `BLG-OPS-175` — DB-level unique constraint for active price alerts |
| S2-21 | EPIC-03 | `BLG-OPS-176` — Make the anomaly-check fingerprint-clear path respect send_alert, or document why not |
| S2-22 | EPIC-03 | `BLG-API-06` — Guard POST /trade-plans against a double-submitted duplicate plan |
| S2-23 | EPIC-04 | `BLG-FEAT-63` — Cost estimate for the AI monthly P&L narrative |
| S2-24 | EPIC-04 | `BLG-FEAT-60` — Define the AI chat engagement metric set |
| S2-25 | EPIC-04 | `BLG-FEAT-59` — AI-assisted monthly P&L narrative |
| S2-26 | EPIC-04 | `BLG-SPEC-174` — Usage counter for the AI monthly P&L narrative |
| S2-27 | EPIC-04 | `BLG-FE-84` — AI chat UI interaction study protocol |
| S2-28 | EPIC-04 | `BLG-GOV-366` — Track the 2027-01-03 AI feature usage review |
| S2-29 | EPIC-05 | `BLG-SPEC-170` — Reconcile the Monthly Restatement Marker spec with GET /reports/monthly-pnl |
| S2-30 | EPIC-05 | `BLG-SPEC-173` — Column provenance annotations in data_model.md |
| S2-31 | EPIC-05 | `BLG-SPEC-177` — Correct the TradePlan status enum in openapi.yaml |
| S2-32 | EPIC-05 | `BLG-SPEC-175` — Fix the 5 error-response examples that diverge from the canonical envelope |
| S2-33 | EPIC-06 | `BLG-GOV-375` — Write-time check that sprint_backlog.md Owner values use canonical role names |
| S2-34 | EPIC-06 | `BLG-GOV-355` — Give the effort-weighted PVR column its home in product_value_ratio_history.md |
| S2-35 | EPIC-06 | `BLG-GOV-359` — §13 sign-off ACs must cite every §13 clause that names the feature's subject |
| S2-36 | EPIC-06 | `BLG-GOV-370` — DoQ sign-off line for stories touching stop, grace, ATR or exit logic |
| S2-37 | EPIC-06 | `BLG-QA-196` — Extend the axe accessibility scan to the Replay page |
| S2-38 | EPIC-06 | `BLG-QA-197` — Fix SC-REP-04a's signed "+£0.00" expectation |
| S2-39 | EPIC-06 | `BLG-QA-199` — Mutation-test the US-market and batch-sizing paths |
| S2-40 | EPIC-06 | `BLG-QA-200` — Make the ceiling/count regression tests read the source they claim to verify |
| S2-41 | EPIC-06 | `BLG-QA-201` — Reset the pilot test file's shared database mocks between tests |
| S2-42 | EPIC-06 | `BLG-OPS-177` — Make the Non-Registry Dependency Check a required status check on main |
| S2-43 | EPIC-06 | `BLG-OPS-178` — Move test-only Python packages out of the production build |

### Items explicitly deferred

| Item | Reason |
|------|--------|
| `BLG-TECH-21` (P2) | Its own scope requires a dedicated single-EPIC release, and it carries `Provisional-Target: v10.0`. Recorded as a §1.4c override, as at v9.10. |
| `BLG-GOV-142`, `BLG-GOV-360` (P2) | Already resolved in v9.9 (ST-19, ST-20). Archive at the next `groom backlog`. |
| `BLG-GOV-368` (P2) | Prompt half applied in `execution_prompt.md` v3.82. Narrow at the next `groom backlog` (v9.9 closure carry-forward). |
| `BLG-GOV-361` (P4) | Met in-run: the §1.3a re-gate of `BLG-SPEC-65` dropped the met adoption-window half and kept the §13 half, which is this item's scope. Archive at the next `groom backlog`. |
| `BLG-FE-195` (P2, gated) | Gate met (`BLG-BE-138` ruling (a), v9.10). Its defaults and read-only panel were delivered by v9.10 ST-01. The helper-text half is `BLG-FE-201` (in the pool, unselected). Archive or narrow at the next `groom backlog`. |
| `BLG-FEAT-73`, `BLG-FEAT-76` | Substantively gate-blocked (no formal Gate field; their own text blocks sprint entry). |
| `BLG-OPS-180`, `BLG-GOV-362` | Marked ✅ COMPLETE. |
| `BLG-FEAT-55`, `BLG-SPEC-65`, `BLG-GOV-121`, `BLG-FEAT-62`, `BLG-OPS-53`, `BLG-FEAT-92` | Date-lapsed gates re-gated on unchanged, unmet conditions (§1.3a). |
| 54 further ready items (~34.55 days) | Capacity. Includes `BLG-GOV-367`, `BLG-GOV-363`/`364`, `BLG-BE-144`/`145`/`146`, `BLG-FE-200`–`203`, `BLG-FE-207`, `BLG-SPEC-189`, `BLG-QA-218`, `BLG-TECH-22`/`23`. |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
