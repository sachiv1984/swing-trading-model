**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-06-22__scheduled
**Last Updated:** 2026-06-22

---

# Cycle Summary — Roadmap Rebalance 2026-06-22__scheduled

**Run type:** Scheduled
**Tier:** Standard
**Date:** 2026-06-22
**Prior rebalance:** 2026-06-19__scheduled (3 days ago)

---

## What Changed

### Governance Patch (STEP -1.5)

`roadmap_prompt.md` v7.5→v7.6: **STEP 8.2 — Now Horizon Item Verification** added (mandatory). For every item proposed for the Now horizon, grep `backlog.md` to confirm active status; if found only in `backlog_archive.md`, exclude from scope. Distinct from STEP 8.0.5 — catches prose-referenced items that bypass the formal STEP 3 candidate list.

*This patch fired correctly on its first use: BLG-FE-52 and BLG-FE-53 (referenced in prior session context as SI-02 frontend candidates) were found in the archive, not the active backlog, and excluded from the v6.1 Now section.*

---

### Roadmap — Now Horizon (v6.1 section added)

**v6.1 — Governance Correctness, CI Quality & User Value Foundation**

| # | BLG ID | Title | Priority | Status |
|---|--------|-------|----------|--------|
| 1 | BLG-GOV-132 | Release planning: emit Design Gate Required flag | P1 | Firm |
| 2 | BLG-GOV-133 | Sprint planning: hard gate on design_gate_status | P1 | Firm |
| 3 | BLG-QA-60 | Playwright CI registration gap (2 spec files) | P2 | Firm |
| 4 | BLG-FE-76 | Portfolio sector heat-map visualization | P2 | Firm |
| 5 | BLG-GOV-131 | Governance overhead ceiling metric | P2 | Firm |
| 6 | BLG-FE-78 | Trade gate proximity indicator on dashboard | P3 | Firm |
| 7 | BLG-OPS-73 | api_performance_baseline update (PATCH /costs) | P3 | Firm |
| 8 | BLG-FEAT-25/PT-04 | Setup Quality Score | P1 | Conditional (≥20 trades ~2026-07-02) |

User-value composition (firm): 2/7 = 28.6% (BLG-FE-76, BLG-FE-78). Conditional adds PT-04 (U) if gate clears. Named commitment from STEP 5 Challenger PVC: BLG-FE-76 and BLG-FE-78 must not be deferred at v6.1 sprint planning.

---

### Backlog (4 new items)

| BLG ID | Title | Priority | Effort | Source |
|--------|-------|----------|--------|--------|
| BLG-FE-78 | Trade gate proximity indicator | P3 | S | IW-20260622-01 / DL-054 |
| BLG-GOV-134 | CI OpenAPI drift detection (api_performance_baseline) | P2 | S | IW-20260622-01 / DL-055 |
| BLG-QA-62 | Playwright spec glob registration | P2 | S | IW-20260622-01 / DL-055 |
| BLG-OPS-74 | Anthropic API cost-per-briefing logging | P3 | S | IW-20260622-01 / DL-055 |

**Active backlog:** 104 → 108 items

---

### Ideas Register (updated)

- IW-20260622-01 opened and closed (16 submissions, 4 promoted, 11 parked-C1)
- 8 IW-20260619-01 ideas incremented Parked-C1 → Parked-C2
- Total open ideas: 19 (8 Parked-C2 + 11 Parked-C1)

---

### Decision Log (DL-052 through DL-055)

- **DL-052:** BLG-GOV-132/133 fast-tracked to Now horizon (P1 correctness)
- **DL-053:** v6.1 Now section added (STEP 8.1 Option a; STEP 8.2 excluded BLG-FE-52/53)
- **DL-054:** BLG-FE-78 added to Now horizon (Challenger PVC outcome)
- **DL-055:** IW-20260622-01: 4 Promoted-Backlog, 11 Parked-C1

---

## Alerts

| Alert | Status |
|-------|--------|
| Product Value Alert (ratio = 0.136) | 🔴 ACTIVE — mitigated by 2 firm U-stories + PT-04 conditional |
| Skill-Silo Alert (86.4% G+D+P) | 🔴 ACTIVE — v6.1 Now composition improves ratio |
| Empty Now Horizon (STEP 8.1) | ✅ CLEARED — v6.1 Now section added |

---

## What's Next

- **v6.1 release planning:** `plan release --version v6.1` — confirm firm scope from Now section; verify PT-04 gate count (≥20 trades); confirm BLG-FE-76 and BLG-FE-78 as firm (Challenger commitment)
- **Design gate:** BLG-FE-76 (heat-map, M effort) will require design gate — release planning engine should flag this (BLG-GOV-132 aims to enforce this at STEP 1.3)
- **PT-04 gate re-check:** PMO Lead to verify closed trade count at v6.1 sprint planning; ~2026-07-02 if current trajectory holds
- **SI-02 frontend:** No BLG items yet — assess at v6.1 release planning after PT-04 gate review; create BLG items at that point if gate clears
