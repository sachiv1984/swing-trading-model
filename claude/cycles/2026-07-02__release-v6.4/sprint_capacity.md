Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-02
Cycle: 2026-07-02__release-v6.4

---

# Sprint Capacity — 2026-07-02__release-v6.4

## 1.1 Capacity Inputs

```
Sprint duration:    Single sprint (Sprint 1 of 1 planned)
Available FTE:      1 (solo developer, evenings/weekends — workforce_capacity.md)
Total capacity:     ~12–14 working days (Sprint Capacity Baseline, effective 2026-05-27)
Skill constraints:  None — solo operator model, all roles fulfilled by a single developer
```

## 1.2 Item Effort Mapping

Source: `release_plan.md ## Capacity Check` (schema v2). All 13 items carry an explicit effort estimate — no `[ESTIMATE REQUIRED]` placeholders.

| EPIC | ST-ID | Story | Effort (days) | Class |
|------|-------|-------|----------------|-------|
| EPIC-01 | ST-01 | Signal generation ticker source fix (BLG-BE-40) | 0.15 | Firm |
| EPIC-01 | ST-02 | Sanitise context_opts.ticker (BLG-SEC-01) | 0.25 | Firm |
| EPIC-01 | ST-03 | Validate ticker/market at signal write (BLG-SEC-02) | 0.5 | Conditional |
| EPIC-02 | ST-04 | Fix governance version-sync drift (BLG-GOV-150) | 0.5 | Firm |
| EPIC-02 | ST-05 | Document hygiene cleanup (BLG-GOV-151) | 0.5 | Conditional |
| EPIC-02 | ST-06 | Structural reliability gaps + FI re-target (BLG-GOV-152) | 1.75 | Firm |
| EPIC-02 | ST-07 | Audit & governance process fixes (BLG-GOV-153) | 0.5 | Firm |
| EPIC-03 | ST-08 | Open Positions panel (BLG-FEAT-54) | 1.5 | Firm |
| EPIC-03 | ST-09 | Daily briefing disclaimer contrast (BLG-UX-01) | 0.25 | Conditional |
| EPIC-03 | ST-10 | Chat widget footer contrast + test (BLG-UX-02) | 0.25 | Firm |
| EPIC-03 | ST-11 | API performance baseline registration (BLG-OPS-82) | 0.15 | Conditional |
| EPIC-03 | ST-12 | Playwright coverage — AI journal summary errors (TEST-GAP-EPIC-01) | 0.5 | Conditional |
| EPIC-03 | ST-13 | Playwright coverage — Strategy Benchmark page (TEST-GAP-EPIC-03) | 1.0 | Firm |
| **Total** | | | **7.8** | 8 Firm / 5 Conditional |

## 1.3 Total Effort vs Capacity

Total estimated effort: **7.8 days** vs confirmed capacity **~12–14 working days**.

**Outcome: PASS.** No over-allocation. All 13 candidate items fit within a single sprint with headroom (~4.2–6.2 days of slack). No scope removal required at STEP 3.

## 1.4 Gate-Conditional Deferred Items

No `execution_state.json` exists yet for this cycle (`execution_state_path` empty in `.claude_current_state.json` — first sprint planning run). No items carry a pre-existing `status: deferred_at_planning` / `gate_condition` marker. No `## Conditional (Deferred)` section applies — all 13 items are candidates for inclusion (see `sprint_backlog.md` for final scope decision).
