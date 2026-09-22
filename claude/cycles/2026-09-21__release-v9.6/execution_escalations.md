Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-22 (ESC-EXEC-20260921-01 resolved — ST-09 trailing-stop entry-floor decision ratified, option (i)); prior — 2026-09-21 (cycle open, 8 escalations raised)

---

# Execution Escalations - 2026-09-21__release-v9.6

Append-only. Do not edit previous entries.

---

## ESC-EXEC-20260921-01

- **Raised at:** 2026-09-21T15:51:14Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-21__release-v9.6
- **Step:** Sprint open (raised per sprint_backlog.md Outstanding Actions at Planning Seal; STEP 3.1.D)
- **ST/EPIC item:** ST-09 / EPIC-03
- **Trigger type:** Strategy
- **Blocking statement:** ST-09 (BLG-BE-119) is a decision-first story on live-capital stop logic (RISK-03, High). Since the backlog item was filed, v9.5 ST-04 resolved most of its scope: `strategy_rules.md` is now v1.10 and §7.2 contains the `max(..., EntryPrice)` breakeven floor (documentation-only; sign-off 'Strategy Rules & System Intent Owner - Approved, agent-mediated on explicit user direction, 2026-09-16'), and `backend/position_manager.py` was deliberately left un-floored as a documented, tested exception (`tests/test_trailing_stop_breakeven_floor.py::TestPositionManagerNotOnLiveStopPath`; `strategy_rules.md` §12.3 exception note). AC-1 (decision recorded) and AC-2 (implementations and spec agree) therefore read as substantially met, but whether an agent-mediated ruling is the 'formal decision' and whether a documented exception satisfies 'all three agree' is the owner's call, not the engine's. AC-3 (a new golden-output case for the floor-binding scenario) and AC-4 (BLG-BE-114 unblocked) still need confirming against `tests/golden_outputs.json`. The engine will not change `calculate_trailing_stop`. Options for the owner: (i) confirm the 2026-09-16 ruling as the formal decision and accept the documented backtest exception as satisfying AC-2 - engine then adds only the golden-output case; (ii) rule that AC-2 requires `position_manager.py` to adopt the floor (changes backtest results - needs its own sign-off); (iii) reverse the decision (removes the floor from live code - live-capital behaviour change).
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** Owner records a decision on options (i)/(ii)/(iii) in writing (PR comment, decision record or this file's resolution). Without one by the time EPIC-03 reaches ST-09, the engine ships only the golden-output case + this recorded state, leaves `calculate_trailing_stop` unchanged, and discloses (per sprint_backlog.md ST-09 Notes).
- **SLA due-by:** 2026-09-24T15:51:14Z (72h)
- **Blocks execution:** No (blocks only ST-09; sprint continues per STEP 3.1.D)
- **Disposition:** Open
- **Resolution summary:** 

---

## ESC-EXEC-20260921-01 — Resolution (Addendum)

- **Resolved at:** 2026-09-22T08:14:51Z (well within the 72h SLA due 2026-09-24T15:51:14Z)
- **Disposition:** Resolved
- **Resolution summary:** Strategy Rules & System Intent Owner ruling (agent-mediated, §5.3, on explicit user direction): **Option (i)**. The 2026-09-16 ruling (`strategy_rules.md` v1.10, ST-04/EPIC-01/v9.5) stands as the formal decision — the entry-price breakeven floor is intentional live behaviour (production behaviour since `BLG-BE-102`/v8.9's P0 fix), and `position_manager.py`'s documented, tested exception (`strategy_rules.md` §12.3 note; `tests/test_trailing_stop_breakeven_floor.py::TestPositionManagerNotOnLiveStopPath`) satisfies "all three agree" for a decision-first story — the decision itself defines what agreement means, and a deliberate, reasoned, tested divergence recorded in the spec is agreement, not drift. **Option (ii)** rejected: retrofitting the floor into the backtest tool would silently change historical backtest results across the whole strategy validation history — a materially bigger, separately-risked change than this story's scope, and not required by a literal reading of "agree" that the spec's own exception note already resolves. **Option (iii)** rejected: reversing the floor would reintroduce the `BLG-BE-102` P0 bug (a profitable position's stop staying frozen below entry) on live capital. AC-1/AC-2 therefore confirmed already met. The one genuinely outstanding item, AC-3 (a golden-output case exercising the floor-binding scenario), is closed: `tests/golden_outputs.json` gains `SL-08` (profitable position, unfloored ATR trail below entry_price — same worked example as `test_trailing_stop_breakeven_floor.py::test_profitable_stop_never_below_entry_price`), `spec_trailing_stop()` in `test_golden_outputs.py` gains the floor formula (was stale relative to the ratified §7.2 text), and a new implementation cross-check (`test_SL08_implementation_matches_spec`) confirms the real `calculate_trailing_stop()` against the same vector. No change made to `calculate_trailing_stop` or `position_manager.py` — both already match the ratified decision. AC-4 (`BLG-BE-114`/ST-04 unblocked): already resolved at v9.5's own closure (`delegation_log.md` `2026-09-15__release-v9.5:44`) — nothing further needed this cycle. Full stop-loss/sizing suite re-run: `tests/test_golden_outputs.py` + `tests/test_trailing_stop_breakeven_floor.py` + `tests/test_stop_reconciliation.py`, 45/45 passed. Commit `f771d5c9` (EPIC-03). ST-13 (`BLG-BE-122`), which was held pending this decision to avoid an uncoordinated second change on the same nightly stop-update call path, is now unblocked. See `execution_state.json` ST-09 for the full record.

---

## ESC-EXEC-20260921-02

- **Raised at:** 2026-09-21T15:51:14Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-21__release-v9.6
- **Step:** Sprint open (raised per sprint_backlog.md Outstanding Actions at Planning Seal; STEP 3.1.D)
- **ST/EPIC item:** ST-16 / EPIC-04
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-16 (BLG-OPS-164) needs (1) a token or session with Actions-write access to dispatch the synthetic-uptime-monitor live-fire run (the prior session's `gh workflow run` returned HTTP 403) and (2) a human to confirm a real Telegram notification was received. Neither is available to the engine. AC-01 and AC-02 cannot be closed without them; AC-03 (docs/ops/synthetic_uptime_monitor_confirmation_2026-09-16.md §7/§8) depends on both. The engine will not fabricate evidence (precedent ESC-EXEC-20260910-01; cite SBX-NO-LIVE-STAGING / SBX-NO-LIVE-EXTERNAL-API if it stays unavailable).
- **Owning authority:** Infrastructure & Operations Owner
- **Unblock criteria:** Owner either performs the live-fire run and confirms Telegram receipt (run URL/ID + confirmation supplied), or accepts a disclosed not-closeable outcome so the item can return to backlog.
- **SLA due-by:** 2026-09-24T15:51:14Z (72h)
- **Blocks execution:** No (blocks only ST-16; sprint continues per STEP 3.1.D)
- **Disposition:** Open
- **Resolution summary:** 

---

## ESC-EXEC-20260921-03

- **Raised at:** 2026-09-21T15:51:14Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-21__release-v9.6
- **Step:** Sprint open (raised per sprint_backlog.md Outstanding Actions at Planning Seal; STEP 3.1.D)
- **ST/EPIC item:** ST-18 / EPIC-05
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-18 (BLG-QA-171) AC-02 needs a live staging environment and a fresh staging seed to complete the first quarterly full-suite Playwright run (RISK-05). The engine has no live staging access. AC-01 (cadence and seed procedure documented) is verifiable in CI and will be done autonomously; AC-02 is staging-only. Per CLAUDE.md §2 / sprint planning §7, if staging sign-off is post-merge the deferral backlog item must be filed before the EPIC-05 PR opens.
- **Owning authority:** Director of Quality
- **Unblock criteria:** Director of Quality supplies a live staging run with a fresh seed and recorded results, or agrees the disclosed-partial + deferral backlog item route.
- **SLA due-by:** 2026-09-24T15:51:14Z (72h)
- **Blocks execution:** No (blocks only ST-18; sprint continues per STEP 3.1.D)
- **Disposition:** Resolved
- **Resolution summary:** Director of Quality supplied both parts of the redefined procedure (`docs/testing/quarterly_playwright_staging_reseed_procedure.md`) with recorded results. Part 1: triggered `playwright.yml` directly, run `35729627868`, all 8 E2E shards + Visual Snapshots green. Part 2: fixed a real infra bug (`STAGING_DATABASE_URL` pointed at an IPv6-only Supabase host unreachable from GitHub runners) and triggered `reset-and-seed-staging.yml`, run `35733092701`, succeeded end to end. Part 2's original "run the Phase-B suite against staging" step was corrected mid-execution — found to conflate `ci-tests.yml`'s own unrelated ephemeral-Postgres Phase B job with staging, and running the real write-heavy suite against shared staging risked damaging the just-established schema/seed data. Replaced with independent read-only verification (7 `SELECT COUNT(*)`/spot-check queries via the `readonly_staging` role), every value matching the reset workflow's own claimed summary exactly. Resolved 2026-09-22, well within the 72h SLA.

---

## ESC-EXEC-20260921-04

- **Raised at:** 2026-09-21T15:51:14Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-21__release-v9.6
- **Step:** Sprint open (raised per sprint_backlog.md Outstanding Actions at Planning Seal; STEP 3.1.D)
- **ST/EPIC item:** ST-22 / EPIC-06
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-22 (BLG-SPEC-148) needs the DS-17 up-migration applied to the LIVE `positions` table (creating `idx_positions_open_ticker_entry_date_unique`). The staging credential is read-only and the engine has no live-DB write access; this is a human/delegated step. The duplicate pre-check (0 groups at 2026-09-18) must be re-run immediately before applying (RISK-06). The `data_model.md` 'confirmed-applied' text must not be written without a real confirmation (SBX-NO-LIVE-DB).
- **Owning authority:** Data Model & Domain Schema Owner (with Infrastructure & Operations Owner)
- **Unblock criteria:** Owner applies the migration and supplies confirmation (index present on the live table + date), or accepts a disclosed not-closeable outcome.
- **SLA due-by:** 2026-09-24T15:51:14Z (72h)
- **Blocks execution:** No (blocks only ST-22; sprint continues per STEP 3.1.D)
- **Disposition:** Open
- **Resolution summary:** 

---

## ESC-EXEC-20260921-05

- **Raised at:** 2026-09-21T15:51:14Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-21__release-v9.6
- **Step:** Sprint open (raised per sprint_backlog.md Outstanding Actions at Planning Seal; STEP 3.1.D)
- **ST/EPIC item:** ST-23 / EPIC-06
- **Trigger type:** Strategy
- **Blocking statement:** ST-23 (BLG-SPEC-160) requires a dated §13 determinism pre-clearance determination for PO-05 (Lightweight Replay Mode). The determination belongs to the Strategy Rules & System Intent Owner (precedents: PS-03 Monte Carlo framing; IT-06's four binding conditions); the engine may draft the analysis but must not decide. AC-02 (BLG-FEAT-74's gate line reflects the outcome) is also subject to the write-scope question in ESC-EXEC-20260921-08.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** Owner issues the dated §13 determination (cleared / conditions / not cleared).
- **SLA due-by:** 2026-09-24T15:51:14Z (72h)
- **Blocks execution:** No (blocks only ST-23; sprint continues per STEP 3.1.D)
- **Disposition:** Open
- **Resolution summary:** 

---

## ESC-EXEC-20260921-06

- **Raised at:** 2026-09-21T15:51:14Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-21__release-v9.6
- **Step:** Sprint open (raised per sprint_backlog.md Outstanding Actions at Planning Seal; STEP 3.1.D)
- **ST/EPIC item:** ST-28 / EPIC-07
- **Trigger type:** Strategy
- **Blocking statement:** ST-28 (BLG-GOV-329) requires an explicit decision on the §13 boundary review cadence: schedule now, or defer with a trigger more concrete than the prior one (STEP 8.1.5 finding; the defer option has been taken 6 consecutive times). The engine may draft options but must not choose for the owner.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** Owner records 'schedule now' or 'defer' with a concrete, testable trigger.
- **SLA due-by:** 2026-09-24T15:51:14Z (72h)
- **Blocks execution:** No (blocks only ST-28; sprint continues per STEP 3.1.D)
- **Disposition:** Open
- **Resolution summary:** 

---

## ESC-EXEC-20260921-07

- **Raised at:** 2026-09-21T15:51:14Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-21__release-v9.6
- **Step:** Sprint open (raised per sprint_backlog.md Outstanding Actions at Planning Seal; STEP 3.1.D)
- **ST/EPIC item:** ST-29 / EPIC-07
- **Trigger type:** Workforce
- **Blocking statement:** ST-29 (BLG-GOV-328) requires the Product Owner's explicit hold/raise decision on the sprint capacity band given sustained >=90% utilisation (FinOps & Resource Architect reviews the history; the engine documents into `claude/roadmap/workforce_capacity.md` under the BLG-GOV-337 plan-authorised exception, citing sprint_backlog.md ST-29). The engine never decides the band. Any change applies from the next planning run, not this sealed sprint.
- **Owning authority:** Product Owner
- **Unblock criteria:** Product Owner supplies an explicit hold or raise decision (not 'revisit next cycle').
- **SLA due-by:** 2026-09-24T15:51:14Z (next planning checkpoint (72h notional))
- **Blocks execution:** No (blocks only ST-29; sprint continues per STEP 3.1.D)
- **Disposition:** Open
- **Resolution summary:** 

---

## ESC-EXEC-20260921-08

- **Raised at:** 2026-09-21T15:51:14Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-21__release-v9.6
- **Step:** Sprint open (raised per sprint_backlog.md Outstanding Actions at Planning Seal; STEP 3.1.D)
- **ST/EPIC item:** ST-23 / ST-27 / EPIC-06 / EPIC-07
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-23 AC-02 (edit BLG-FEAT-74's gate line) and ST-27's clear/re-gate legs (edit the gate lines of BLG-FEAT-59/60/63 and BLG-FE-84) edit EXISTING `claude/backlog/backlog.md` items, which `execution_prompt.md` §7 does not permit (new-item addition only). The sealed plan asks for either a plan-authorised exception (as BLG-GOV-337 did for `workforce_capacity.md`) or acceptance of the disclosed-partial fallback. Until ruled, the engine will take the fallback: record the determination/verification in dated documents and hand over exact replacement gate-line text, and disclose those legs as partial.
- **Owning authority:** Head of Specs Team + Product Owner
- **Unblock criteria:** Head of Specs Team + Product Owner rule on a plan-authorised exception for these named backlog items (or confirm the fallback).
- **SLA due-by:** 2026-09-24T15:51:14Z (72h)
- **Blocks execution:** No (blocks only ST-23 / ST-27; sprint continues per STEP 3.1.D)
- **Disposition:** Open
- **Resolution summary:** 

---

