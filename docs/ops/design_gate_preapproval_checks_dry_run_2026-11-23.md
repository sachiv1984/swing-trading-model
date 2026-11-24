**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-11-23
**Source:** ST-18 (BLG-GOV-422, EPIC-04, `2026-11-18__release-v9.18`)

---

# Design Gate Pre-Approval Checks: Dry Runs

`design_gate_prompt.md` v1.12 adds four pre-approval checks to STEP 2.2: data source, writers, worked examples (with time boundaries) and dependent states. ST-18's acceptance criteria ask for two dry runs against artefacts that already shipped with known gaps:

- the v9.17 `positions-decision-first` decision record, which should surface BLG-BE-215 and the BLG-SPEC-234/235 last-day contradiction;
- `dashboard.md` v4.0 §1B (the Today list, commit `b901ce91`), which should surface both v9.17 EPIC-04 gaps (BLG-SPEC-238).

Each dry run reads the artefact and the code **as they were when the gate ran**, not as they are now. The pre-ST-04 `main` commit `bafcbdab` is used for the v9.17 specs; `b901ce91` is used for §1B and the backend at that time.

## Dry run 1: v9.17 positions-decision-first

Artefact: `docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md` §5 (single grace view) and §6 (warning strip).

### Data sources

| Field shown | View and the population it lists | Endpoint | Contract line (quoted) | Whole population? | Found as |
|-------------|----------------------------------|----------|------------------------|-------------------|----------|
| Ticker, day label, days-left sentence | `GracePeriodView`: **every** open position in grace (§5.1) | `GET /positions` (`grace_period === true`) | `grace_period`, `grace_days_remaining` per open position | Yes | — |
| Trade plan block (Thesis, Stop, R-target), "View Trade Plan" link | Same list: every in-grace position | `GET /positions/grace-period-alerts` | `grace_period_alert_endpoint.md` line 12: "Returns positions in `GRACE` lifecycle state with `grace_days_remaining <= 2` … Includes linked trade plan summary if available." | **No.** A position with 3 or more days left has no plan data, so its row shows no plan block and no link | **Gap → BLG-BE-215** (found) |

### Writers

| Claim | Writers found | Claim holds? | Found as |
|-------|---------------|--------------|----------|
| None in scope: §5–§6 make no "written by" or "only X" claim | — | — | — |

### Worked examples: grace days remaining

Run-date source: not a "latest" rule. The value is `grace_days_remaining = max(0, 10 − calendar days since entry_date)`, returned by both `GET /positions` and the alert endpoint (contract line 58).

The surfaces that show the concept are the grace view row (`positions.md` §Grace Period View and §Grace Period Alert Zone), the Risk Dashboard panel (`risk_dashboard.md` v0.1.16 §5.2), the Positions warning strip (decision record §6), the Today list "Grace ends today" row (`dashboard.md` §1B) and the Positions "Action needed" cell (`positions.md` line 128).

| `grace_days_remaining` | Grace view row | Risk Dashboard §5.2 | Warning strip | Today list | Action needed |
|------------------------|----------------|---------------------|---------------|------------|---------------|
| 2 | "Day 9 of 10" | "Next ends in 2 days" | "… next ends {dd MMM}" | — | — |
| 1 | "Day 10 of 10" | "Ends today" | "… next ends {today}" | "Grace ends today — …" | "Grace ends today" |
| 0 | "Grace period has ended. Your position will transition …" | Not covered by the rule's text | Counted only if the row is listed (see below) | — | — |
| null | Sub-label and sentence omitted | Line omitted | No date | — | — |

**Contradictions found:**
- **Last day, row 2 against row 1.** At 2 days left the grace view says Day 9 of 10, so the last day is tomorrow, yet the Risk Dashboard says "Next ends in 2 days". The panel skips a day between 2 ("in 2 days") and 1 ("today"), and disagrees with the strip's "next ends" date. → **BLG-SPEC-234** (found).
- **Row 0.** The grace view keeps the `grace_days_remaining = 0` sentence, but §5.1 lists only positions with `grace_period === true`, and a position at 0 days has `grace_period === false` in `GET /positions`. The sentence can only show if the view also lists alert rows, and then the strip's count differs from the Risk Dashboard panel and Dashboard Card 3. → **BLG-SPEC-235** (found).

### Dependent states

| Rule | Depends on | State of the dependency | Rule result |
|------|------------|-------------------------|-------------|
| Strip entry 1 active | `DrawdownReviewPrompt` would render | renders / does not / its query fails | entry shown / hidden / not stated |
| Strip entry 3 active | "One or more positions in grace" | ≥ 1 with `grace_period === true` / only a 0-day alert row / none | shown / **not stated**: the same 0-day case as BLG-SPEC-235 / hidden |
| Strip entry 4 active | `MetricsStalenessIndicator` would render | renders / does not | entry shown / hidden |

The "query fails" state is also unstated for entries 1, 2 and 4, and today's `positions.md` §Warning Strip still does not state it. It is outside ST-18's acceptance criteria and is filed as **BLG-SPEC-244**.

**Result:** the checks find BLG-BE-215 (data source) and the BLG-SPEC-234/235 last-day contradiction (worked examples, confirmed by the dependent-state list). AC 2 is met.

## Dry run 2: dashboard.md v4.0 §1B (Today list)

Artefact: `docs/specs/frontend/pages/dashboard.md` at `b901ce91` (v4.0), §1B "Stops moved" group and TL-09.

### Writers

| Claim | Writers found (at `b901ce91`) | Claim holds? | Found as |
|-------|-------------------------------|--------------|----------|
| "stops are moved only by the nightly trailing-stop job" (§1B, "Stops moved, why it is here"); "written by the nightly job" (Data dependency) | `backend/services/position_service.py:576` in `analyze_positions()` (served by `GET /positions/analyze`, `backend/main.py:795`) writes `position_updates['current_stop']`; `run_nightly_trailing_stop_update()` (`position_service.py:645`) also writes it. The comment at line 253 names both. | **No.** Two paths move the stop | **Gap → BLG-SPEC-238** first half (found; v9.17 ST-09 ruling 2026-11-13, DEV-EPIC04-ST10-01) |

### Worked examples (time boundaries): "Stops moved since the last run"

Run-date source: TL-09 lists positions whose `stop_last_moved_date` "is the latest nightly run date". **No endpoint returns a nightly run date.** `GET /positions` has no run date field, so the rule has no source.

| Case | What TL-09 shows |
|------|------------------|
| Normal weekday, nightly ran | Cannot be computed: no run date to compare with |
| Stale data (no move for a week) | Not determinable: was there a run with no moves, or no run at all? |
| Quiet day (job ran, moved nothing) | Not determinable for the same reason |
| Weekend (Saturday and Sunday) | Not stated: is the latest run Friday's? |
| UTC midnight | Not stated: is a move written after 00:00 UTC "today" or the previous run? |
| On-load recompute moves a stop | Not covered: the move is not from a nightly run (the writer gap above) |
| Latest row closes (position exited) | Row drops out with the position: consistent |

**Gap → BLG-SPEC-238** second half (found). The run date had no source, so v9.17 ST-10 chose "today or the previous weekday (UTC)" in session; it lives only in code and DEV-EPIC04-ST10-01.

### Data sources and dependent states

The data-source check restates the Data dependency paragraph (`stop_last_moved_date` and `previous_stop` did not exist; `BLG-BE-205` was planned). That gap was already declared in v4.0, so it is not counted as a new finding. No dependent-state rule is in scope for the Stops moved group.

**Result:** the writer check and the time-boundary worked examples find both v9.17 EPIC-04 gaps behind BLG-SPEC-238. AC 5 is met.
