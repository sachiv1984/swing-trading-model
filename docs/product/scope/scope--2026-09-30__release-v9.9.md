Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.9
Cycle: 2026-09-30__release-v9.9
Last Updated: 2026-09-30

## Release Scope — v9.9

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-BE-135` — Consolidate 4 duplicate ATR implementations; persist stop/ATR recalculation timestamp; expose atr/multiplier/timestamp on GET /positions |
| S2-02 | EPIC-01 | `BLG-BE-131` — GET /reports/monthly-pnl's year param has no bounds check, unlike its sibling GET /reports/tax-year |
| S2-03 | EPIC-01 | `BLG-BE-132` — gemini_service.py's daily-cost Telegram alert still uses a hardcoded timeout, not utils.upstream_call |
| S2-04 | EPIC-01 | `BLG-BE-133` — utils/pricing.py's ATR-fallback Yahoo Finance call still uses a hardcoded timeout, not utils.upstream_call |
| S2-05 | EPIC-01 | `BLG-BE-134` — alpaca_paper_sync_service.py's 3 Alpaca calls still use hardcoded timeouts, not utils.upstream_call |
| S2-06 | EPIC-02 | `BLG-SEC-40` — Two residual gaps in the just-hardened non-registry dependency guard |
| S2-07 | EPIC-02 | `BLG-OPS-172` — POST /ai/check-daily-cost has no de-duplication guard against a double-submitted Telegram alert |
| S2-08 | EPIC-02 | `BLG-OPS-173` — POST /ai/check-endpoint-anomalies has no de-duplication guard against a double-submitted Telegram alert |
| S2-09 | EPIC-02 | `BLG-OPS-174` — POST /price-alerts has no de-duplication guard against a double-submitted duplicate alert |
| S2-10 | EPIC-03 | `BLG-QA-203` — GET /reports/tax-year returns HTTP 500 against its own test fixture |
| S2-11 | EPIC-03 | `BLG-QA-185` — Strategy-rule → test traceability matrix for strategy_rules.md §4–§8 |
| S2-12 | EPIC-03 | `BLG-QA-186` — Property-based tests for 'stop never decreases' and sizing validity rules |
| S2-13 | EPIC-03 | `BLG-QA-189` — Real-Postgres integration test for the reflection-reminder evaluation step |
| S2-14 | EPIC-03 | `BLG-QA-190` — Convert remaining test files sharing test_trade_plan_audit_log.py's unrestored sys.modules["database"] swap pattern |
| S2-15 | EPIC-03 | `BLG-QA-191` — Add automated test coverage for the I/O-boundary functions in EPIC-04's staleness/CI-usage scripts |
| S2-16 | EPIC-03 | `BLG-QA-192` — test_null_fee_trade_audit.py's inspect.getsource() call fails against the database module stub |
| S2-17 | EPIC-03 | `BLG-QA-193` — Prove the non-registry dependency check fails a real PR, and confirm it is a required status check on main |
| S2-18 | EPIC-03 | `BLG-QA-194` — Harden the UI-copy boundary lint against obfuscation-grade and cross-node phrase splits |
| S2-19 | EPIC-04 | `BLG-GOV-356` — Conduct the overdue 90-day AI feature usage review (BLG-GOV-74/140/141/142 cluster) |
| S2-20 | EPIC-04 | `BLG-GOV-358` — gap_risk_service.py (BLG-FEAT-65) shipped without a recorded §13 review or §13.5 roster row |
| S2-21 | EPIC-04 | `BLG-GOV-343` — Split roadmap_prompt.md into a core plus an appendix so it fits a single read |
| S2-22 | EPIC-04 | `BLG-GOV-344` — Parameter-change ledger for strategy_rules.md §11 production parameters |
| S2-23 | EPIC-04 | `BLG-GOV-347` — scan_backlog_gate_conditions.py date-disambiguation gap can produce false negatives |
| S2-24 | EPIC-04 | `BLG-GOV-350` — Five near-duplicate "AI adoption window" gate-criteria texts should be one canonical shared reference |
| S2-25 | EPIC-04 | `BLG-GOV-352` — Rebalance diagnostic tallies (STEP 2.4/7.1/7.2) are recomputed by hand each cycle |
| S2-26 | EPIC-04 | `BLG-GOV-353` — role_share_history.md has no governance-authorized home under claude/roadmap/ |
| S2-27 | EPIC-04 | `BLG-GOV-354` — .claude_current_state.json's execution_state_path points to the prior cycle, not the active one |
| S2-28 | EPIC-05 | `BLG-SPEC-157` — Read-only live-schema vs data_model.md drift detector |
| S2-29 | EPIC-05 | `BLG-SPEC-164` — Drop 4 confirmed-orphaned, always-NULL columns from the live positions table |
| S2-30 | EPIC-05 | `BLG-SPEC-165` — Reconcile positions.fees_paid NOT NULL constraint (re-apply live, or confirm nullable is intentional) |
| S2-31 | EPIC-05 | `BLG-SPEC-166` — Cross-reference current_roadmap.md's SI-02 field to the canonical "linked trade plan" definition |
| S2-32 | EPIC-05 | `BLG-SPEC-167` — data_model.md DS-19 "Verification status" still says the migration was never run against a live PostgreSQL |
| S2-33 | EPIC-05 | `BLG-SPEC-168` — Correct the BLG-BE-128 citation to BLG-BE-129 for the latency_ms composition decision |
| S2-34 | EPIC-05 | `BLG-SPEC-169` — Correct notifications.md and the alert-thresholds empty-state scenario doc to the no-trailing-period headings now shipped |
| S2-35 | EPIC-06 | `BLG-FE-192` — RecentTradesWidget icon-background badge uses two-way (>=0) colour logic for zero P&L |

35 items across 6 EPICs, sized to 27.85 estimated days (near top of the confirmed ~24–28 day capacity band per explicit user "full capacity" instruction). Selected via `release_planning_prompt.md` §1.4c (0 ready P1; P2-first; category-balanced round-robin, oldest-filed-first) from a 53-item / 36.20-day ready pool, per `run_manifest.md`'s Scope Construction section.

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| 18 further ready P3/P4 items across all categories (8.35 days) | Capacity-exhausted after 35 items reached 27.85d | v9.10 candidate — see `run_manifest.md` for full ready-pool accounting |
| `BLG-FE-193` | Gated on `BLG-BE-135` (S2-01, this release) shipping and its fields being live on `GET /positions` — a same-cycle sequencing dependency is not equivalent to "shipped and available" | Natural `v9.10` lead candidate once `BLG-BE-135` ships |
| `BLG-FEAT-59`, `BLG-FEAT-60`, `BLG-FEAT-63`, `BLG-FE-84`, `BLG-OPS-88`, `BLG-GOV-140`, `BLG-GOV-141`, `BLG-GOV-142` | Date-lapsed gate (90-day AI feature usage review, due 2026-09-24, not yet conducted) — remains gated; the review itself is seated this cycle (`BLG-GOV-356`, S2-19) | Re-eligible once the review is conducted |
| `BLG-FEAT-73`, `BLG-FEAT-76` | Still gate-blocked (SI-02 linkage / hard `Depends on` chain) | Re-check per each item's own gate condition (no earlier than 2026-11-09 for `BLG-FEAT-73`) |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-09-30__release-v9.9
