**Owner:** Infrastructure & Operations Owner
**Class:** Planning Document (Class 3)
**Status:** Active
**Last Updated:** 2026-06-19
**Cycle:** 2026-06-19__scheduled

---

# Run Manifest — Roadmap Rebalance 2026-06-19__scheduled

## Run Type

Scheduled rebalance — no completion event. `--reason "scheduled"`.
Cycle ID: `2026-06-19__scheduled`
Run tier: **Standard** (scheduled; 2 days since last scheduled rebalance; not Extended; not Lightweight)

## Canonical Inputs

| File | Status |
|------|--------|
| `claude/charter/team_charter.md` | Present |
| `claude/charter/document_lifecycle_guide.md` | Present |
| `claude/strategy/strategy_rules.md` | v1.4 (2026-05-20) |
| `claude/roadmap/current_roadmap.md` | Active — Class 4 compliant |
| `claude/backlog/backlog.md` | Active — Class 4 compliant |
| `claude/roadmap/initiative_register.md` | Active — 0 active initiatives |
| `claude/system/lessons_learnt_prompt.md` | Present |
| `claude/system/idea_intake_prompt.md` | v2.5 (2026-06-09) |
| `claude/system/idea_template.md` | Present |

## Decision Authorities and Roles

All 9 required roles verified present in `claude/agents/`:
Product Owner · Strategy Rules & System Intent Owner · Head of Specs Team · PMO Lead · FinOps & Resource Architect · Infrastructure & Operations Owner · Director of Quality · Facilitator · Challenger

## Prior Cycle Outstanding Actions

Prior rebalance cycle: `2026-06-17__scheduled`
Prior lessons_learnt.md: loaded — 1 friction item, 1 deferred patch, 1 outstanding action.

| ID | Action | Status | Notes |
|----|--------|--------|-------|
| LL-P5-03 | Apply roadmap_prompt.md STEP -1.5 stale release target check | **RESOLVED** | Action-now patch applied: roadmap_prompt.md v7.4→v7.5 STEP -1.5 third bullet added. Head of Specs Team authorised. Committed. |

Deferred patches checked: 1 (LL-P5-03 target). Stale release target check also applied (the meta-fix itself): no release targets present in the patch — N/A. No remaining OVERDUE patches.

## Cycle Velocity

Source: `claude/cycles/velocity_metrics.md`

| Metric | Value |
|--------|-------|
| Last cycle (v5.9) | 11/11 = 1.00 |
| Rolling 6-cycle average (v5.4–v5.9) | 0.74 |

## Governance Health Score (Advisory)

| Dimension | Value | Status |
|-----------|-------|--------|
| Header Compliance % | 5/5 docs in prior rebalance cycle = 100% | Green |
| Deferred Patch Indicator | 0 active deferred patches (LL-P5-03 resolved) | Green |
| Outstanding Action Count | 0 (LL-P5-03 resolved; open_escalations empty) | Green |

Overall: **Green** across all dimensions.

## Carry-Forward Advisory (from v5.9 post-ship lessons_learnt_closure.md)

2 items for Release Planning:
1. BLG-FE-64 gate 2026-06-21 should now have cleared. v6.0 release planning must confirm gate clearance and include BLG-FE-64 as firm scope.
2. BLG-OPS-70 (SI-05 deep link AC-04) trailing obligation: gate ~2026-06-23. Check at v6.0 planning.

**Carry-forward count:** 2 items. Advisory only.

## Empty Now Horizon Advisory (STEP 0.D)

`## 3. Delivery Plan — Horizon: Now` in `current_roadmap.md` contains no committed non-shipped items (RA:v5.9 retired 2026-06-18). 98+ active backlog items exist. Advisory: `plan release v6.0` may be the right next step immediately following this rebalance. PO decision recorded at STEP 8.1.

---

## Product Value Ratio Diagnostic (STEP 2.4)

Last 5 completed cycles: v5.5, v5.6, v5.7, v5.8, v5.9

| Cycle | Stories | U | G | D | P |
|-------|---------|---|---|---|---|
| v5.5 | 10 | 1 | 3 | 5 | 1 |
| v5.6 | 10 | 2 | 0 | 8 | 0 |
| v5.7 | 10 | 0 | 1 | 9 | 0 |
| v5.8 | 2 | 0 | 1 | 1 | 0 |
| v5.9 | 11 | 1 | 5 | 5 | 0 |
| **Total** | **43** | **4** | **10** | **28** | **1** |

**U-story classifications:**
- v5.5 ST-05: Trade data density progress tracker (digest display) — U
- v5.6 ST-01: Add deep links from SI-05 digest to app screens — U
- v5.6 ST-02: Clarify N/A pass rate reason in SI-05 digest — U
- v5.9 ST-11: Pre-entry panel warning/fail count badge when collapsed — U

`user_value_ratio = 4 / 43 = 0.093`

**Status: PRODUCT VALUE ALERT (< 0.30)**

Per STEP 2.4 rules: Challenger must treat this as equivalent weight to a §13 concern. Explicit PO written response required before STEP 8 concludes. Pull-forward of a user-facing backlog item is mandatory unless PO provides written rationale.

**Context:** Cycles v5.5–v5.9 represent the post-v4.x governance consolidation phase (governance hardening, QA debt, ops baselines, staging verifications). The governance simplification work (v5.9) specifically aimed to reduce ongoing governance overhead. This context is relevant but does not negate the pull-forward obligation.

**Facilitator note:** This pattern is structurally linked to the 2026-06-18 Skill-Silo ceiling reduction to 40% (roadmap_prompt.md v7.4). G+D+P share across last 5 cycles = 90.7% — well above the 40% ceiling. Challenger Product Velocity Concern is expected at STEP 5 (if ideas advance); independently, STEP 8 pull-forward is mandatory.

---

## Actionable Backlog Assessment (STEP 3.1)

Total active items: 101 (98 post-groom + 3 added 2026-06-19: BLG-FEAT-46, BLG-FEAT-47, BLG-OPS-71)

| Category | Count | Notes |
|----------|-------|-------|
| **A** — Actionable now | ~47 | BLG-BE-36 (P0), BLG-FEAT-46/47 (P1), most BLG-GOV/SPEC/OPS/BE items with no stated gate |
| **T** — Time-gated (clears < 3 months) | ~16 | BLG-FE-64/41 (gate 2026-06-21 — 2 days); BLG-OPS-70 (~2026-06-23); SI-05 effectiveness items BLG-GOV-112/113/115/BLG-OPS-59 (gate 2026-07-04 = 15 days); BLG-FEAT-20 provisional-target v6.0 (no hard gate) |
| **D** — Data-density gated | ~12 | PT-04/SI-02 frontend (gate: 20+ closed trades; current ~13; est. ~4–7 weeks at current trading rate); PO-02 (gate: 6+ months AI journal; est. ~4 months from now); SI-04 (version-tagged history) |
| **L** — Long-horizon gated | ~26 | PO-03/04/05 (need PO-02 live + 50+ trades); PS-01–PS-05 (need 50–100+ trades + 12–18 months history); SI-02 full (needs drift scores meaningful); Arc 6 features |

**A-item ratio:** ~47/101 = 46.5% → above 30% floor. No Backlog Accessibility Warning.

**D-gated detail:**
- PT-04 / SI-02 frontend: ~13/20 closed trades (7 more needed; est. 4–7 weeks at current rate — ~2026-07-20 to 2026-08-10)
- PO-02 (Journal Pattern Recognition): requires 6+ months of AI-summarised journal entries; gate clears approximately 2026-10-20 (6 months post-AI journal activation)
- BLG-FEAT-20: no hard data gate; P1 provisional v6.0

**L-gated items (top 5 by priority):**
1. PO-03 Behavioural Error Taxonomy — depends on PO-02 live + 50+ trades (~2027+)
2. PS-01 Edge Analysis Dashboard — needs 100+ trades with plans (~2027+)
3. PS-02 Regime-Conditional Performance — needs 50+ trades (~late 2026+)
4. PS-03 Monte Carlo Simulation — needs 50+ trades (~late 2026+)
5. PS-04 Strategy Decay Detection — needs 18+ months history (~2028)

No L-gated items with conditions > 12 months flagged for archival (data density gates are approaching; only PS-04 at 18+ months is borderline).

---

## Production Correctness Fast-Track (STEP 8.0)

Scan complete. Items found:

| BLG-ID | Priority | Type | Description |
|--------|----------|------|-------------|
| BLG-BE-36 | P0 — Critical Correctness Bug | Backend correctness | `signal_service.py` uses cash-allocation model for suggested_shares; canonical model is risk-based sizing from strategy_rules.md §4.1. Every signal card shows wrong share counts. |

**Decision (per STEP 8.0):** BLG-BE-36 must appear in the v6.0 Now horizon as the first story. PO override requires written safety rationale (not applicable — this is a wrong calculation showing incorrect share counts on every signal card, directly affecting trading decisions).

No P0/P1 security issues found.

**Classification:** Correctness Fast-Track Promotion — BLG-BE-36 to v6.0 Now horizon (net-zero: displaces a non-product item of equal or lower priority if needed).

---

*Run manifest written before STEP 2 onwards per STEP 1.1 requirement.*
