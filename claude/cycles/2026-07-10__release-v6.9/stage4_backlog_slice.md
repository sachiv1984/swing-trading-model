**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.9
**Cycle:** 2026-07-10__release-v6.9
**Last Updated:** 2026-07-10
**Sprint Backlog Source:** This slice is authoritative. Sprint Planning Engine reads this file at Phase 2.

---

# v6.9 Backlog Slice — 2026-07-10__release-v6.9

<!-- release-plan-marker: RP:v6.9:2026-07-10__release-v6.9 -->

---

## EPIC-01 — On-Demand Pre-Entry (SI-01) Compliance Recheck

**Purpose:** Mandatory response to the 2026-07-10 rebalance's Product Value Alert (ratio 0.18, 2nd consecutive alert) — primary named pull-forward anchor.

**Sprint assignment:** Sprint 1

**Maps to:** S2-01

---

### ST-01 — On-demand pre-entry rule recheck for open positions (BLG-FEAT-64)

**Type:** Firm
**Effort:** M (~2–3 days)
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Backlog ref:** BLG-FEAT-64
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** SI-01 validates the 5 strategy checks only at entry time; once a position is open there is no way to see whether it would still pass those checks against current conditions. This is a manual, on-demand, single-position check — it explicitly does not replace or duplicate SI-02 (which remains gated; see Readiness §1.4). Pure re-application of SI-01's existing deterministic rule set — no new statistical model or scoring. New endpoint — must be registered in `docs/reference/openapi.yaml` and a `## GET /positions/{position_id}/compliance-recheck` entry in `docs/specs/api_contracts/` in the same commit (CLAUDE.md hard rule), and the new route registered in `backend/routers/test.py` in the same commit (representative value: an open position's ID).

**Acceptance criteria:**
- AC-01: `GET /positions/{position_id}/compliance-recheck` returns pass/fail for each of the 5 SI-01 rules (`strategy_rules.md` §4.2) evaluated against the position's current state (current regime, current signal conditions, current heat/sizing) rather than the entry-time snapshot
- AC-02: Frontend "Recheck compliance" action available on open positions (Positions page / position detail view); renders using the same visual pattern as `PreEntryValidationPanel` (pass/fail/override-acknowledged states) [visual rendering — Playwright coverage or staging sign-off required per CLAUDE.md §2]
- AC-03: Recheck is on-demand only (no automatic polling/background job) — user-triggered
- AC-04: §13 sign-off (Strategy Rules & System Intent Owner) confirming re-running existing deterministic rules on demand introduces no new automation/prediction surface

**Staging-only ACs:** None — AC-02 is coverable by Playwright (rendering + pass/fail/override states are all deterministic given API response fixtures).

---

## EPIC-02 — Overnight/Weekend Gap Risk Flag

**Purpose:** Mandatory response to the 2026-07-10 rebalance's Product Value Alert — secondary named pull-forward anchor.

**Sprint assignment:** Sprint 1

**Maps to:** S2-02

---

### ST-02 — Overnight/weekend gap risk flag for open positions (BLG-FEAT-65)

**Type:** Firm
**Effort:** M (~2–3 days)
**Owner:** Head of UX & Design; Head of Engineering
**Backlog ref:** BLG-FEAT-65
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** Swing positions held overnight/over weekends are exposed to gap risk from earnings releases or major macro events. The system already has an earnings calendar (DS-04, shipped v3.1) and historical OHLCV data; this surfaces the two together as a proactive risk flag. Deterministic only — flags a known calendar event plus historical statistics, no directional prediction. No new endpoint contract changes anticipated beyond an existing-data read path — if a new endpoint is introduced during implementation, the same same-commit `openapi.yaml` / `docs/specs/api_contracts/` / `backend/routers/test.py` registration rules apply per CLAUDE.md.

**Acceptance criteria:**
- AC-01: Position flagged when an earnings date falls before the next trading session
- AC-02: Weekend-hold positions flagged at Friday close [interaction timing — Playwright coverage or staging sign-off required per CLAUDE.md §2]
- AC-03: Flag displays historical average overnight/weekend gap magnitude for that ticker (or "insufficient history" if fewer than N historical events) [visual rendering — Playwright coverage or staging sign-off required per CLAUDE.md §2]
- AC-04: §13 sign-off (Strategy Rules & System Intent Owner) confirming no prediction of gap direction or magnitude — informational only

**Staging-only ACs:** None — AC-01–03 are coverable by Playwright using mocked earnings-calendar/OHLCV fixtures and mocked Friday-close date context.

---

## Capacity Summary (preview — confirmed at Sprint Planning STEP 1)

| Metric | Value |
|--------|-------|
| Total scope items | 2 ST / 2 EPIC |
| Total estimated effort | M + M (~4–6 days combined) |
| Firm items | 2 |
| Conditional items | 0 |

## Items Deferred This Release

None — both named mandatory pull-forwards are in scope. See `release_plan.md §Scope → Items explicitly deferred` for backlog items considered and not selected.
