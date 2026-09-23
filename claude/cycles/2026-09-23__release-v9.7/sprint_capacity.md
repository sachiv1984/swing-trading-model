Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-23
Cycle: 2026-09-23__release-v9.7

# Sprint Capacity — 2026-09-23__release-v9.7

## 1.1 Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (solo developer, evenings/weekends) — cadence per workforce_capacity.md Effective 2026-07-17
Available FTE:      1 (solo developer) + agent-mediated execution
Total capacity:     ~24-28 working days (confirmed band, workforce_capacity.md, reconfirmed unchanged 2026-09-23 per ESC-EXEC-20260921-07)
Skill constraints:  None flagged — no scarce/role-locked skill named in workforce_capacity.md for this cycle's scope
```

## 1.2 Item Effort Mapping

Effort days derived per `workforce_capacity.md`'s Canonical Effort Band → Days Conversion Table, applying the precedence rule (item's own explicit range midpoint takes precedence over the bare band-letter canonical midpoint). All 29 backlog-slice items carry a defined effort figure — no `[ESTIMATE REQUIRED]` placeholders.

`BLG-FEAT-74`/ST-01 (12.0d PO ad hoc estimate — no canonical VH midpoint exists) is phased into three sprint sub-stories per `release_plan.md`'s EPIC-01 sequencing note and RISK-01's resolution path (see `sprint_planning_notes.md` Risk Flags and Outstanding Actions). The 12.0d is allocated across the three phases as follows, reflecting relative complexity (backend replay-mechanics integration > frontend selector/output view > scope-confirmation write-up):

| EPIC | ST | Title | Effort field | Days |
|------|----|-------|--------------|------|
| EPIC-01 | ST-01a | PO-05 — Scope confirmation sub-story | (derived split) | 1.0 |
| EPIC-01 | ST-01b | PO-05 — Backend replay mechanics | (derived split) | 6.0 |
| EPIC-01 | ST-01c | PO-05 — Frontend selector + output view | (derived split) | 5.0 |
| EPIC-02 | ST-02 | Clone trade plan Setup Type fix | S (~0.5-1d) | 0.75 |
| EPIC-02 | ST-03 | Monthly P&L NULL-fee flag surfacing | S (~0.5-1d) | 0.75 |
| EPIC-02 | ST-04 | Month-end restatement diff surfacing | S (~1d) | 1.0 |
| EPIC-02 | ST-05 | AlertThresholdsSection.js empty-state period | XS (<1h) | 0.15 |
| EPIC-02 | ST-06 | NotificationsHistory.js empty-state period | XS (<1h) | 0.15 |
| EPIC-02 | ST-07 | CI lint of predictive/advice-crossing copy | S (~0.5-1d) | 0.75 |
| EPIC-03 | ST-08 | Fee rounding float→Decimal | S (~0.5d) | 0.5 |
| EPIC-03 | ST-09 | Reflection reminder over-report / NULL-portfolio | XS (<1h) | 0.15 |
| EPIC-03 | ST-10 | Alert re-delivery ignores read state | S (~0.5d) | 0.5 |
| EPIC-03 | ST-11 | Month-closure / Monthly P&L clock-source mismatch | XS (<1h) | 0.15 |
| EPIC-03 | ST-12 | Monthly P&L snapshot — per-month connection | S (~0.5d) | 0.5 |
| EPIC-03 | ST-13 | latency_ms retry-backoff semantics | XS (<1h) | 0.15 |
| EPIC-04 | ST-14 | Backend suite real-DB isolation | S (~0.5d) | 0.5 |
| EPIC-04 | ST-15 | CI check for merged .skip()/.only() | S | 0.5 |
| EPIC-04 | ST-16 | Recurring endpoint coverage audit (documented) | S | 0.5 |
| EPIC-04 | ST-17 | Negative-path test backfill (3 routers) | M | 2.5 |
| EPIC-04 | ST-18 | Validate cost-windows SQL vs real Postgres | S (~0.5d) | 0.5 |
| EPIC-05 | ST-19 | Governance overhead ratio metric | M | 2.5 |
| EPIC-05 | ST-20 | SI-02 gate threshold-vs-cadence review | S | 0.5 |
| EPIC-05 | ST-21 | Document ensure_ascii=False convention | XS | 0.15 |
| EPIC-05 | ST-22 | Reconcile STEP -1 status-vocabulary wording | XS (~0.5-1h) | 0.15 |
| EPIC-06 | ST-23 | Formal "linked trade plan" definition | S | 0.5 |
| EPIC-06 | ST-24 | positions.exit_note doc correction | XS (<1h) | 0.15 |
| EPIC-06 | ST-25 | 4 orphaned NULL columns disposition | S (~0.5-1d) | 0.75 |
| EPIC-06 | ST-26 | positions.fees_paid nullability doc fix | XS (<1h) | 0.15 |
| EPIC-07 | ST-27 | Staging verification — reflection-reminder migration | XS (<1h) | 0.15 |
| EPIC-07 | ST-28 | External-dependency failure-mode matrix | S (~0.5d) | 0.5 |
| EPIC-07 | ST-29 | CI guard — non-registry dependency specifiers | S (~0.5d) | 0.5 |

**Total: 28.00 days** — reproduces `release_plan.md`'s published total exactly.

## 1.3 Total Effort vs Capacity

Total estimated effort: **28.00 days**. Confirmed capacity band: **~24-28 working days**. 28.00 / 28.00 = **100.0% of the band's top edge** — matches `release_plan.md ## Capacity Check` (`stage4_5_capacity_check: pass`, not `warn`). No over-allocation; no scope removal required at STEP 3.2.

## 1.4 Gate-Conditional Deferred Items

No items in this sprint carry `status: deferred_at_planning` with a `gate_condition` in `execution_state.json` — this is a fresh cycle (`execution_state_path` in `.claude_current_state.json` still points to the prior cycle, `2026-09-21__release-v9.6`; this sprint's own `execution_state.json` will be created fresh at Sprint Execution STEP 0). Section omitted; no re-invocation advisory needed.

## 1.5 Minimum Capacity Buffer Floor (Advisory)

`scope_effort ÷ confirmed_capacity` = 28.00 / 28.00 = **100%**, exceeding the recommended ~95% buffer floor (`workforce_capacity.md §Sprint Capacity Baseline`, `sprint_planning_prompt.md §1.5`).

**Buffer floor exceeded — advisory note, not a seal blocker.** Surfaced to the Product Owner: this sprint runs with zero standing slippage buffer. Disposition: **Proceed** — this is not a fresh judgment call at Sprint Planning; the Product Owner already explicitly instructed "use full capacity" at Release Planning (`cycle_summary.md`, 2026-09-23), scoping the slice deliberately to the top of the band. Sprint Planning records the ratio and carries the pre-existing PO decision forward rather than re-opening it. If in-sprint slippage occurs, the smallest/lowest-priority P4 items (ST-05, ST-06, ST-13, ST-26, ST-27, ST-29 — all ≤0.15-0.5d) are the natural first candidates to defer to next sprint without touching the EPIC-01 flagship item.

**Capacity WARN acknowledgement:** Not applicable — `capacity_check` outcome is `pass`, not `warn`. `capacity_warn_acknowledged` remains unset/false in the STEP 7 state write.

**Sign-off:** PMO Lead (agent-mediated, §5.3) — capacity baseline confirmed against `workforce_capacity.md` and `release_plan.md`, 2026-09-23.
