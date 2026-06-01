**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.8
**Cycle:** 2026-06-01__release-v4.8
**Last Updated:** 2026-06-01

---

# Release Plan — v4.8

**Theme:** Governance Hardening, Ops/Security Debt & SI-05 Phase 1

---

## Readiness

### Prior Cycle Status

- v4.7 post-ship closure: ✅ Closed_with_actions (2026-06-01)
- Verification status: ✅ Verified (zero deviations)
- next_cycle_unblocked: true
- Rebalance: ✅ 2026-06-01__scheduled (Standard tier; DL-036; 11 backlog adds)

### Backlog Age Advisory (STEP 1.1)

Scanning for spec/documentation debt items in the v4.8 slice aged 2+ cycles without story assignment:
- BLG-GOV-69 (§13 register gap): filed 2026-06-01 (NEW — v4.8 first assignment)
- BLG-GOV-70 (agent charter headers): filed 2026-06-01 (NEW)
- BLG-GOV-72 (AUD gap resolution): filed 2026-06-01 (NEW)
- BLG-OPS-46 (build minutes monitoring): filed 2026-06-01 (NEW)
- BLG-OPS-47 (dependency audit): filed 2026-06-01 (NEW)
- BLG-QA-39 (coverage matrix): filed 2026-06-01 (NEW)
- BLG-SPEC-43 (SI-04 contract): filed 2026-06-01 (NEW)
- BLG-GOV-67 (SI-05 Phase 1): filed 2026-05-27 (1 cycle — gate-conditional)

No items aged 2+ cycles without story assignment in this slice. ✅ No advisory.

### Provisional-Target Advisory (STEP 1.2)

Items with `Provisional-Target: v4.8`: 6 items (BLG-GOV-69, BLG-GOV-70, BLG-GOV-72, BLG-OPS-46, BLG-OPS-47, BLG-QA-39).
Items with `Provisional-Target: v4.8` (conditional): 1 item (BLG-SPEC-43).
Items without v4.8 Provisional-Target in slice: 1 item (BLG-GOV-67 — `Unscheduled`, gate-conditional).
ℹ 6 items carry `Provisional-Target: v4.8` — horizon-planned for this release. 1 item (BLG-GOV-67) has gate-conditional Provisional-Target but is appropriate for this release given gate proximity (2026-06-21).

### Design-Gate Language Scan (STEP 1.3)

Scanning slice candidates for design-gate language:
- BLG-GOV-67 (SI-05 Phase 1): "BLG-FE-43 frontend component spec — Gate: SI-05 sprint planning imminent"
  → SI-05 Phase 1 is Telegram-only (no new UI). BLG-FE-43 is for potential in-app display (not Phase 1). Design dependency: NONE for Phase 1 scope.
- All other items: documentation/governance work. No design dependency.

Design dependency scan: 0 items flagged for Phase 1 scope. ✅

**Design gate assessment:** NOT required. v4.8 scope is governance/ops/documentation + Telegram-only SI-05 Phase 1. No new UI surfaces introduced.

### Gate-Condition Proximity Scan (STEP 1.4)

| Item | Gate condition | Current trajectory | Projected clear date |
|------|----------------|-------------------|---------------------|
| BLG-GOV-67 (SI-05 Phase 1) | SI-01 + SI-03 live ≥ 30 days | SI-03 shipped 2026-05-22 → 30 days = 2026-06-21 | **2026-06-21** (within sprint window) |
| BLG-FE-41 (RFJ visual design review) | SI-03 live ≥ 30 days | Same as above | 2026-06-21 |
| BLG-FE-40 (RFJ filter state persistence) | RFJ in use ≥ 30 days | 2026-05-22 + 30 days | 2026-06-21 |
| BLG-FEAT-25 (PT-04 Setup Quality Score) | 20+ closed trades | 6 closed trades at ~0.5/month | ~Sep 2026 |
| SI-02 frontend | 20+ closed trades with plans | 6 closed trades, 0 with plans | ~Nov 2026 |
| PO-02 | 6+ months AI journal entries | AI journals since ~Apr 2026 | ~Oct 2026 |
| PO-04 | 50+ trades with plans | 6 trades, ~0.5/month | ~2028 (long horizon) |

**Arc 4 data density sub-check:**
- Closed trade count: 6 (v4.6 audit, 2026-05-31). Monthly rate: ~0.5/month.
- AI journal entries: active since AI thesis feature (v4.0, 2026-05-25). ~5 weeks of entries.
- Trade plan creation rate: ~0.5 plans/month (tied to closed trade rate).
- PO-02 gate (6+ months): projected ~Oct/Nov 2026.
- PO-04 gate (50+ trades with plans): projected ~2027+ at current rate. Gate condition may need review.
- SI-02 gate (20+ trades with plans): projected ~Nov 2026.

**Key proximity finding:** SI-05 Phase 1 gate clears 2026-06-21. Sprint window should overlap — BLG-GOV-67 included as conditional EPIC-03. PO to confirm gate check at sprint planning.

---

## Scope

### In Scope

| ID | Item | Backlog Ref | Priority | Effort | Conditional |
|----|------|-------------|----------|--------|-------------|
| S2-01 | Governance & Compliance Hardening | BLG-GOV-69, BLG-GOV-70, BLG-GOV-72 | P2 | S | No |
| S2-02 | Operations, Security & QA Debt | BLG-OPS-46, BLG-OPS-47, BLG-QA-39, BLG-SPEC-43 | P2 | S–M | BLG-SPEC-43 conditional |
| S2-03 | SI-05 Phase 1 — Weekly Strategy Integrity Digest | BLG-GOV-67 | P2 | M | Yes (gate 2026-06-21) |

**Firm items:** S2-01 (3 stories) + S2-02 (3 firm + 1 conditional stories) = 6 firm stories
**Conditional items:** EPIC-02 ST-07 (BLG-SPEC-43 — if SI-04 confirmed) + EPIC-03 ST-08 (BLG-GOV-67 — gate 2026-06-21)

**PO capacity model confirmation:** Standard capacity (~12–14 dev-days). Double capacity not required (v4.8 scope ~7–10 dev-days firm+conditional). Carry-forward OA-1 from v4.7 resolved.

### Explicitly Deferred

| Item | Reason |
|------|--------|
| BLG-FE-41 — RFJ visual design review | P3; gate 2026-06-21 but lower priority vs SI-05; defer to v4.9 |
| BLG-FE-40 — RFJ filter state persistence | P3; gate 2026-06-21; defer to v4.9 |
| SI-02 frontend | Gate not met (6 closed trades, need 20+; ~Nov 2026) |
| BLG-FEAT-25 (PT-04) | Gate not met (6 closed trades, need 20+; ~Sep 2026) |
| SI-04 implementation | BLG-SPEC-43 pre-authors the contract; implementation gated on Arc 2 data |
| Arc 4 features (PO-02/03/04) | Data density gates not met |
| Arc 6 features | Gate: 100+ trades with plans |

### Items NOT in Scope

- Any code changes to backend or frontend (non-code sprint)
- New API endpoints
- Database migrations

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Specs Team | RISK-03 | No constraint |
| EPIC-02 | S2-02 | Head of Specs Team; Infrastructure & Operations Owner | RISK-02 | No constraint (parallel with EPIC-01) |
| EPIC-03 | S2-03 | Head of Specs Team | RISK-01 | After STEP -1 gate check at sprint planning; conditional on 2026-06-21 gate |

**EPIC-01 note:** 3 governance compliance items. All document-edits. BLG-GOV-72 may discover untracked patches (RISK-03) — if found, file new BLG-GOV items rather than expanding sprint scope.

**EPIC-02 note:** BLG-OPS-47 (dependency audit) may reveal CVEs; if HIGH/CRITICAL found, file as P0/P1 backlog items for immediate remediation. BLG-SPEC-43 is conditional on PO confirming SI-04 in the next planning cycle — if not confirmed, defer to v4.9.

**EPIC-03 note:** Gate clears 2026-06-21. Sprint planning must check gate before sealing. If gate not met at sprint planning seal, EPIC-03 defers to v4.9.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-03 | SI-05 gate (2026-06-21) clears after sprint planning seal | Medium | Sprint planning gate check; defer EPIC-03 to v4.9 if gate not met at seal | null |
| RISK-02 | EPIC-02 | BLG-OPS-47 dependency audit finds HIGH/CRITICAL CVEs | Medium | File P0/P1 backlog items; handle as hot-fix outside sprint scope | null |
| RISK-03 | EPIC-01 | BLG-GOV-72 audit gap analysis finds untracked items | Low | File new BLG-GOV items; do not expand sprint scope inline | null |

---

## Capacity Check

### Effort Estimates

| EPIC | Items | Effort Band (inline) | scored_initiatives.md | Notes |
|------|-------|---------------------|----------------------|-------|
| EPIC-01 | ST-01 + ST-02 + ST-03 | S + S + S = ~1.5 days | No matching rows | Document edits |
| EPIC-02 | ST-04 + ST-05 + ST-06 + ST-07 | S + S + S + S-M = ~3–4 days | No matching rows | ST-07 conditional |
| EPIC-03 | ST-08 (conditional) | M = ~2–3 days | No matching rows | Gate-conditional |

**Total (firm only):** 4–5.5 dev-days
**Total (all including conditional):** 6–8.5 dev-days
**Available capacity (standard):** ~12–14 dev-days
**Utilisation (firm):** ~35–40%
**Utilisation (all):** ~50–60%

### Capacity Verdict: **PASS**

Well within standard capacity. No phasing required. All items fit in a single sprint.

---

## Integrity Validation — 3.5 Local Model Integrity

### Cross-Stage ID Check

- All S2 IDs (S2-01, S2-02, S2-03) have corresponding EPIC mappings: ✅
- EPIC-01 maps to S2-01 ✅; EPIC-02 maps to S2-02 ✅; EPIC-03 maps to S2-03 ✅
- All RISK IDs (RISK-01, RISK-02, RISK-03) appear in the Risk Register ✅
- No orphaned scope items ✅

Local model integrity: **PASS**

---
