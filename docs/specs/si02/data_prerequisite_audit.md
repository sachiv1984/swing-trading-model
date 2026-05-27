**Owner:** Strategy Rules & System Intent Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-26__release-v4.1 (ST-13, BLG-GOV-46)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# SI-02 Data Prerequisite Audit

## 1. Purpose

This document audits the data prerequisites required for SI-02 (Behavioural Drift Detection) to be implementable and useful, and confirms whether the data density gate is currently met.

SI-02 detects behavioural drift from trade history and trade plan data. Without sufficient trade history, drift patterns cannot be distinguished from normal variation.

---

## 2. Data Prerequisites

### 2.1 Trade History Density

**Gate requirement:** A minimum baseline of closed trades is needed to:
- Establish a "normal" sizing pattern to detect drift against
- Identify consecutive loss sequences (requires at least 3–5 consecutive trades)
- Calculate entry timing distribution relative to signal dates

| Metric | Minimum Required | Current Status (2026-05-27) |
|--------|-----------------|----------------------------|
| Closed trades in `trade_history` | 20 | < 20 (PT-04 gate not met) |
| Trades with linked `trade_plans` | 10 | Not assessed (requires PT-04 gate first) |
| Trades with `signal_id` linkage | 10 | 0 (field not yet added — Gap 1 from gap analysis) |

**Assessment:** The data density gate is **NOT MET** as of v4.1. SI-02 sprint planning should not proceed until PT-04 gate is confirmed met (≥ 20 closed trades).

### 2.2 Trade Plan Coverage

**Gate requirement:** Drift detection using trade plan data requires that a sufficient proportion of trades have associated `trade_plan` records.

| Metric | Minimum Required | Current Status |
|--------|-----------------|----------------|
| % of closed trades with linked trade_plans | ≥ 50% | Unknown (insufficient closed trades to assess) |
| trade_plans with `checklist_completed = true` | ≥ 10 | Unknown |

**Assessment:** Cannot be assessed until PT-04 gate is met.

### 2.3 Signal Linkage Coverage

**Gate requirement:** Entry timing drift analysis requires `signal_id` linkage from `trade_plans` to `signals`. This field does not currently exist (Gap 1 in `si02_gap_analysis.md`).

**Assessment:** Zero signal-linked plans currently. The DS-07 schema migration (documented in `si02_gap_analysis.md §6`) must run before this gate can be assessed.

### 2.4 Portfolio History Coverage

**Gate requirement:** Sizing adherence analysis requires `portfolio_history` snapshots for each trade's entry date to reconstruct portfolio value at entry (needed if `portfolio_value_at_entry` column is not added to `trade_plans`).

| Metric | Minimum Required | Current Status |
|--------|-----------------|----------------|
| portfolio_history rows | ≥ 1 snapshot per entry day in analysis window | Unknown |
| Gap in portfolio_history | < 30 consecutive days | Unknown |

---

## 3. Dependency Map

```
PT-04 gate (≥20 closed trades)
    └─ Required before: data density assessment
           └─ Required before: drift baseline establishment
                  └─ Required before: SI-02 sprint planning can seal

DS-07 migration (signal_id + risk fields in trade_plans)
    └─ Must ship before: SI-02 frontend plan creation captures signal linkage
           └─ Required before: entry timing drift data starts accumulating
```

SI-02 implementation sprint planning requires PT-04 gate AND DS-07 migration to be in place before planning seals, so that:
- Implementation can be tested with real data at staging
- The data fields the implementation writes to actually exist

---

## 4. Audit Findings

| Prerequisite | Status | Blocker? |
|-------------|--------|----------|
| ≥ 20 closed trades | ❌ Not met | Yes — PT-04 gate |
| ≥ 10 plan-linked trades | ❓ Unknown | Pending PT-04 |
| signal_id field in trade_plans | ❌ Not present | Yes — DS-07 migration needed |
| portfolio_history coverage | ❓ Unknown | Pending PT-04 |
| §13 review criteria defined | ✅ Done | No (defined in `section13_criteria.md`) |
| Schema gap analysis complete | ✅ Done | No (completed in `si02_gap_analysis.md`) |

**Overall gate status: NOT MET.**

---

## 5. Recommended Next Steps

1. Continue accumulating trade history until PT-04 gate is met (≥ 20 closed trades)
2. At next sprint planning after PT-04 gate confirmed: include DS-07 schema migration as Sprint 1 item
3. Re-run this audit after DS-07 migration ships to confirm trade_plans start capturing required fields
4. Schedule SI-02 sprint planning at the sprint planning cycle where data density confirms ≥ 20 plan-linked trades with signal linkage

---

## 6. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Challenger | Pending | — |
| Product Owner | Pending | — |
