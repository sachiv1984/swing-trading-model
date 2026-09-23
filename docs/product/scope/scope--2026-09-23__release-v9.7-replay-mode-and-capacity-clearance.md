Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.7
Cycle: 2026-09-23__release-v9.7
Last Updated: 2026-09-23

## Release Scope — v9.7 PO-05 Replay Mode & Full-Capacity Debt Clearance

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-FEAT-74` — PO-05 Lightweight Replay Mode (§13-cleared this week; backend historical replay + frontend date-range/trade-set selector and retrospective output view) |
| S2-02 | EPIC-02 | `BLG-FE-186` — Cloned trade plan can silently get the wrong Setup Type |
| S2-03 | EPIC-02 | `BLG-FE-187` — Monthly P&L's NULL-fee audit flag has no frontend surfacing |
| S2-04 | EPIC-02 | `BLG-FE-188` — Month-end P&L restatement diff has no frontend surfacing |
| S2-05 | EPIC-02 | `BLG-FE-178` — AlertThresholdsSection.js empty-state heading trailing-period fix |
| S2-06 | EPIC-02 | `BLG-FE-179` — NotificationsHistory.js empty-state heading trailing-period fix |
| S2-07 | EPIC-02 | `BLG-FE-183` — CI lint of static UI copy for forbidden predictive/advice-crossing phrases |
| S2-08 | EPIC-03 | `BLG-BE-127` — UK stamp duty / US FX fee rounding: float `round()` → Decimal |
| S2-09 | EPIC-03 | `BLG-BE-123` — Reflection reminder step over-reporting after rollback / NULL-portfolio gap |
| S2-10 | EPIC-03 | `BLG-BE-124` — Generic alert re-delivery ignores read state |
| S2-11 | EPIC-03 | `BLG-BE-125` — Month-closure check and Monthly P&L clock-source mismatch |
| S2-12 | EPIC-03 | `BLG-BE-126` — Monthly P&L snapshot lookup connection-per-month fix |
| S2-13 | EPIC-03 | `BLG-BE-129` — `latency_ms`/`elapsed_ms` includes retry backoff sleep time |
| S2-14 | EPIC-04 | `BLG-QA-188` — Backend test suite real-database connection support |
| S2-15 | EPIC-04 | `BLG-QA-174` — CI check flagging merged `.skip()`/`.only()` Playwright specs |
| S2-16 | EPIC-04 | `BLG-QA-175` — Recurring pre-sprint endpoint test coverage audit |
| S2-17 | EPIC-04 | `BLG-QA-176` — Negative-path test backfill, 3 newest v9.2/v9.3 routers |
| S2-18 | EPIC-04 | `BLG-QA-177` — `get_claude_endpoint_cost_windows()` SQL validation against real Postgres |
| S2-19 | EPIC-05 | `BLG-GOV-327` — Quarterly "governance overhead ratio" metric |
| S2-20 | EPIC-05 | `BLG-GOV-330` — SI-02 gate threshold cadence-scaling review |
| S2-21 | EPIC-05 | `BLG-GOV-331` — Document `ensure_ascii=False` convention for governance JSON writes |
| S2-22 | EPIC-05 | `BLG-GOV-333` — Reconcile `sprint_planning_prompt.md` status-vocabulary wording vs `shared_standards.md` §10.1 |
| S2-23 | EPIC-06 | `BLG-SPEC-147` — Formal definition of "linked trade plan" counting for the SI-02 gate |
| S2-24 | EPIC-06 | `BLG-SPEC-149` — `positions.exit_note` documented but not live on table |
| S2-25 | EPIC-06 | `BLG-SPEC-150` — 4 orphaned, undocumented, always-NULL `positions` columns |
| S2-26 | EPIC-06 | `BLG-SPEC-151` — `positions.fees_paid` documented NOT NULL but live column nullable |
| S2-27 | EPIC-07 | `BLG-OPS-168` — Post-deploy staging verification of reflection-reminder migration/SQL |
| S2-28 | EPIC-07 | `BLG-OPS-167` — External-dependency failure-mode matrix |
| S2-29 | EPIC-07 | `BLG-SEC-38` — CI guard rejecting non-registry dependency specifiers |

29 items across 7 EPICs, sized to 28.00 estimated days (top of the confirmed ~24–28 day capacity band per explicit user "use full capacity" instruction). Selected via `release_planning_prompt.md` §1.4c (P1-then-P2-first, category-balanced round-robin, oldest-filed-first) from a 68-item / 61.35-day ready pool, per `run_manifest.md`'s Scope Construction section.

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| `BLG-FE-184`, `BLG-FE-185`, `BLG-BE-128` | Ready but would overshoot the 28.00d capacity ceiling on their category's round-robin turn | v9.8 candidate |
| 36 further ready P3/P4 items across all categories | Capacity-exhausted after 29 items reached 28.00d | v9.8 candidate — see `run_manifest.md` for full ready-pool accounting |
| `BLG-FEAT-59`, `BLG-FEAT-60`, `BLG-FEAT-63`, `BLG-FE-84` | Within-sprint date gate (§1.4b) — owner verification due at the 2026-09-24 AI feature usage review, which falls inside this sprint's plausible execution window; classified conditional, not seated | Re-eligible at v9.8 planning once the review lands |
| `BLG-FEAT-73`, `BLG-FEAT-76` | Still gate-blocked (SI-02 linkage / hard `Depends on` chain) | Re-check per each item's own gate condition |
| `BLG-FE-189` | Already resolved same-session (2026-09-22, hotfix branch) — no longer open work; recommend `groom backlog` archive it | N/A — closure housekeeping only |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-09-23__release-v9.7
