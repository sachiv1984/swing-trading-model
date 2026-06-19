**Owner:** Product Owner
**Class:** Planning Document (Class 3)
**Status:** Active
**Last Updated:** 2026-06-19
**Cycle:** 2026-06-19__scheduled

---

# Cycle Record — Roadmap Rebalance 2026-06-19__scheduled

---

## STEP 2 — Roadmap Re-Validation

### STEP 2.1 — Initiative Register Review

Active initiatives: **0**

The initiative register contains no active initiatives as of 2026-04-03. All prior initiatives (Arc 1–5 delivery programmes) were completed or their scope absorbed into the delivery backlog. No new initiative candidates emerged from the prior cycle.

**CPS:** N/A (0 active initiatives — arithmetic mean undefined). No CPS-triggered horizon mutation.

### STEP 2.2 — Horizon Review

| Horizon | Status | Items |
|---------|--------|-------|
| **Now** | EMPTY — RA:v5.9 retired 2026-06-18 | 0 committed non-shipped items |
| **Next** | PT-04 (parked, data gate — 13/20 closed trades) | 1 item |
| **Later** | Arc 3–6 features, most gated | Multiple items |

**Empty Now Horizon soft gate (STEP 8.1) armed.** PO must select Option (a) or (b) before STEP 8 concludes.

### STEP 2.3 — Roadmap Item Health Check

No roadmap items have been in a non-shipped, non-gated state for > 3 cycles without progress. PT-04 is formally parked with a data gate (20+ closed trades; currently ~13). All other Next/Later items are gated or waiting on Arc dependency sequencing. No stale items requiring action.

### STEP 2.4 — Product Value Ratio Diagnostic

**PRODUCT VALUE ALERT — user_value_ratio = 0.093 (< 0.30 threshold)**

Full diagnostic recorded in `run_manifest.md` §Product Value Ratio Diagnostic.

| Cycle | Stories | U | G | D | P |
|-------|---------|---|---|---|---|
| v5.5 | 10 | 1 | 3 | 5 | 1 |
| v5.6 | 10 | 2 | 0 | 8 | 0 |
| v5.7 | 10 | 0 | 1 | 9 | 0 |
| v5.8 | 2 | 0 | 1 | 1 | 0 |
| v5.9 | 11 | 1 | 5 | 5 | 0 |
| **Total** | **43** | **4** | **10** | **28** | **1** |

`user_value_ratio = 4/43 = 0.093`

**Mandatory consequences (per STEP 2.4 rules):**
1. Challenger treats this as equivalent weight to a §13 concern at STEP 5
2. Explicit PO written response required before STEP 8 concludes
3. Pull-forward of a user-facing backlog item is mandatory unless PO provides written rationale

**Context note:** v5.5–v5.9 represent the post-v4.x governance consolidation phase. The structural cause is 28 D-classified stories (governance, debt, ops) across 5 cycles — a deliberate phase of investment that has now been substantially completed (v5.9 governance simplification, STEP-8.1 skill-silo ceiling at 40%). The Product Value Alert signals this investment phase should now close.

**Skill-Silo Alert (correlated):** G+D+P share across last 5 cycles = 90.7% — well above the 40% ceiling introduced in roadmap_prompt.md v7.4. This provides structural enforcement going forward in addition to the Product Value Alert retrospective signal.

---

## STEP 3 — Backlog Health Review

### STEP 3.1 — Actionable Assessment

Full categorisation recorded in `run_manifest.md` §Actionable Backlog Assessment.

| Category | Count | Representative items |
|----------|-------|---------------------|
| **A** — Actionable now | ~47 | BLG-BE-36 (P0), BLG-FEAT-46/47/20 (P1), most GOV/SPEC/OPS/BE with no gate |
| **T** — Time-gated (< 3 months) | ~16 | BLG-FE-64/41 (gate 2026-06-21); BLG-OPS-70 (~2026-06-23); BLG-GOV-112/113/115/130, BLG-OPS-59 (gate 2026-07-04) |
| **D** — Data-density gated | ~12 | PT-04 (~13/20 closed trades); PO-02 (6-month AI journal gate ~2026-10); SI-02 frontend |
| **L** — Long-horizon gated | ~26 | PO-03/04/05, PS-01–PS-05, SI-04, Arc 6 |

**A-item ratio: ~47/101 = 46.5% → above 30% floor. No Backlog Accessibility Warning.**

### STEP 3.2 — Obsolescence and Alignment Scan

Scan of all 101 items against current strategy, team charter, and §13 boundaries:

- **No obsolete items found.** All active items align with strategy_rules.md v1.4 scope boundaries.
- **No §13 boundary violations found** in existing backlog items. New items with potential §13 relevance (PO-02 arc, AI features) are gated and will require §13 pre-assessment before sprint planning.
- **BLG-GOV-112/113/115/130, BLG-OPS-59** — all carry 2026-07-04 gates. Gate dates are per design (SI-05 Phase 1 effectiveness review period). No action needed.
- **BLG-FE-64 / BLG-FE-41** — gate 2026-06-21 = 2 days from today. Gate clears imminently. Both should be included in v6.0 Now horizon as T-conditional scope.
- **BLG-FEAT-20** — P1 promoted 2026-06-18 (net-of-costs tracking; costs ignored in R-multiples = correctness concern). No hard gate. Confirm inclusion in v6.0.

### STEP 3.3 — D-gated Progress Check

| Gate | Current state | Est. clear |
|------|---------------|------------|
| PT-04 (20 closed trades) | ~13/20 (7 more needed) | ~2026-07-20 to 2026-08-10 |
| PO-02 (6-month AI journal) | AI journal activated; 0/6 months elapsed | ~2026-10-20 |
| SI-02 frontend (meaningful drift scores) | SI-02 backend shipped v4.6; awaiting data volume | ~2026-09 (est.) |

PT-04 approaching; est. 4–7 weeks. Should appear on radar at next scheduled rebalance.

---

## STEP 4 — Idea Review and Document Management

Source window: `IW-20260619-01` — 16 submissions from 8 agents.

### STEP 4.1 — Duplicate and §13 Screening

| Idea ID | Title | Duplicate? | §13 risk? |
|---------|-------|------------|-----------|
| IDEA-strategy-owner-20260619-01 | §13 pre-assessment for Arc 4 AI features (PO-02/03) | **DUPLICATE — BLG-SPEC-35 (active, P1)** | N/A |
| IDEA-head-of-specs-20260619-01 | Arc 4 API contract pre-authoring | No | Low (pre-authoring, no build) |
| IDEA-head-of-specs-20260619-02 | Data model v3 pre-definition | No | Low (design doc only) |
| IDEA-director-of-quality-20260619-01 | Arc 4 E2E test strategy pre-design | No | Low (test pre-design only) |
| IDEA-finops-20260619-01 | AI API cost model for Arc 4 | No | Low (planning doc) |
| IDEA-infra-ops-20260619-01 | Database index audit for Arc 4 | No | Low (backend assessment) |
| IDEA-challenger-20260619-02 | Governance overhead ceiling metric | No | None |
| IDEA-product-owner-20260619-01 | Portfolio sector heat-map | No | Low (frontend visualisation) |
| All others | Various | No | None |

### STEP 4.2 — Idea Classification

| Idea ID | Title | Classification | Rationale | Assigned ID |
|---------|-------|---------------|-----------|-------------|
| IDEA-strategy-owner-20260619-01 | §13 pre-assessment for Arc 4 AI features | ❌ **Rejected** | Exact duplicate of BLG-SPEC-35 (P1, active) | — |
| IDEA-head-of-specs-20260619-01 | Arc 4 API contract pre-authoring (PO-02/03/04) | 📋 **Promoted-Backlog** | Pre-authoring Arc 4 contracts before PO-02 gate clears is a high-leverage, low-risk investment. Aligns with Head of Specs Team charter. No debate needed. | BLG-SPEC-56 |
| IDEA-head-of-specs-20260619-02 | Data model v3 pre-definition for Arc 4 | 📋 **Promoted-Backlog** | Pre-definition reduces execution risk when PO-02 gate clears. Pairs with BLG-SPEC-56. | BLG-SPEC-57 |
| IDEA-director-of-quality-20260619-01 | Arc 4 E2E test strategy pre-design | 📋 **Promoted-Backlog** | Allows test strategy decisions before sprint planning pressure exists. Complements SPEC-56/57. | BLG-QA-59 |
| IDEA-finops-20260619-01 | AI API cost model for Arc 4 journal intelligence | 📋 **Promoted-Backlog** | FinOps charter item. Arc 4 AI features will have material API cost; model should precede build. | BLG-OPS-72 |
| IDEA-infra-ops-20260619-01 | Database index audit for Arc 4 cross-table queries | 📋 **Promoted-Backlog** | Arc 4 introduces significant cross-table query patterns not present in current schema. Pre-audit prevents post-ship latency surprises. | BLG-BE-37 |
| IDEA-challenger-20260619-02 | Governance overhead ceiling metric and accountability mechanism | 📋 **Promoted-Backlog** | Elevated: directly addresses the structural driver of the Product Value Alert (G+D+P = 90.7% over last 5 cycles). Governance accountability mechanism is load-bearing given Skill-Silo Alert. | BLG-GOV-131 |
| IDEA-product-owner-20260619-01 | Portfolio sector heat-map visualization | ➡️ **Advance → STEP 5** | Meaningful product investment warranting structured debate. Directly addresses Product Value Alert pull-forward obligation. Arc context: all Arc 1 delivery complete; Arc 2/3 items gated; heat-map fills user-value gap. | — → BLG-FE-76 (post-debate) |
| IDEA-product-owner-20260619-02 | Trade tagging and tag-based performance filtering | 🅿 **Park Cycle 1** | Product velocity concern acknowledged. However: (a) data model change is non-trivial; (b) heat-map (IDEA-PO-01) already provides portfolio visualisation investment this cycle; (c) P1 items (FEAT-46/47/20) plus BLG-BE-36 already absorb v6.0 user-value quota. Revisit after BLG-FE-76 ships. | — |
| IDEA-pmo-lead-20260619-01 | Automated governance health score computation script | 🅿 **Park Cycle 1** | Useful but not urgent; governance health status is already reported accurately in run_manifest.md. Script would reduce manual effort but this is not a bottleneck cycle. | — |
| IDEA-pmo-lead-20260619-02 | Sprint velocity trend chart (last 10 cycles) | 🅿 **Park Cycle 1** | Velocity data exists in velocity_metrics.md; visualisation adds value for trend spotting but is low urgency. Park for later tooling sprint. | — |
| IDEA-director-of-quality-20260619-02 | Automated accessibility testing (axe-core) in Playwright CI | 🅿 **Park Cycle 1** | Accessibility testing is valuable but not on critical path. No Arc or product item currently at the stage where axe-core would gate delivery. Park for later Arc 4+ design work. | — |
| IDEA-strategy-owner-20260619-02 | Formal strategy rules effectiveness review cadence | 🅿 **Park Cycle 1** | strategy_rules.md v1.4 is stable and effective. Formal cadence would add governance overhead — contradicts governance simplification direction from v5.9. Park; revisit if §4–§13 ambiguities accumulate. | — |
| IDEA-finops-20260619-02 | Alpaca API tier and cost optimization assessment | 🅿 **Park Cycle 1** | BLG-OPS-37 (Anthropic API tier assessment) was completed with "no upgrade" outcome. Alpaca tier is likewise stable at current usage levels. Park; trigger if usage spikes. | — |
| IDEA-infra-ops-20260619-02 | Enhanced health check with external dependency verification | 🅿 **Park Cycle 1** | Current health check is adequate for operational needs. External dependency probing would be valuable if we had SLA monitoring requirements. Park for v6.1+ ops sprint. | — |
| IDEA-challenger-20260619-01 | Data provider diversity risk assessment and failover strategy | 🅿 **Park Cycle 1** | Valid risk framing. However: Alpaca is deeply integrated and switching cost is high; failover strategy requires significant architecture work. Single-provider dependency is a known, accepted risk at current product stage. Park; trigger if Alpaca reliability degrades. | — |

**Summary:**
- Rejected: 1 (duplicate)
- Promoted-Backlog (immediate): 6 → BLG-SPEC-56, BLG-SPEC-57, BLG-QA-59, BLG-OPS-72, BLG-BE-37, BLG-GOV-131
- Advanced to STEP 5: 1 (heat-map → BLG-FE-76 post-debate)
- Parked Cycle 1: 8

---

## STEP 5 — Structured Debate

### STEP 5.1 — Debate: Portfolio Sector Heat-Map (IDEA-product-owner-20260619-01)

**Motion:** Advance IDEA-product-owner-20260619-01 (Portfolio sector heat-map visualization) to Promoted-Backlog as BLG-FE-76.

**Challenger — Product Velocity Concern (mandatory, STEP 2.4):**
> "The product value ratio is 0.093. That means 90.7% of the last 43 stories delivered zero direct user-observable value. The heat-map is the only idea in this window that directly adds user-observable value beyond items already in the backlog. Challenger formally endorses advancing the heat-map as mandatory to address the Product Value Alert. Rejecting or parking the heat-map this cycle would leave the only structural response to the Product Value Alert as items already in the pipeline (FEAT-46/47/20, BE-36) — which is defensible if and only if those items fully absorb the pull-forward obligation. They do. But adding BLG-FE-76 further strengthens the user-value case for v6.1."

**Head of Specs Team:**
> "The heat-map needs a spec before sprint planning. The sector classification data already exists (DS-03 shipped v2.9). The frontend data model (sector_name, portfolio_weight) is derivable from existing endpoints. I do not foresee a §13 issue — this is portfolio visualisation within the existing application scope. Pre-authoring the contract is feasible and low-risk."

**Strategy Rules & System Intent Owner:**
> "No §13 boundary concerns. Sector heat-map does not introduce AI features, external data providers, or new user data categories. Standard frontend feature."

**PMO Lead:**
> "FEAT-46 (M) + FEAT-47 (S) + FEAT-20 (M) + BE-36 (S) in v6.0 already commits significant effort. BLG-FE-76 at M effort belongs in v6.1, not v6.0. Adding it to the backlog now with Provisional-Target v6.1 is the right framing."

**Product Owner:**
> "Agreed. Heat-map advances to Promoted-Backlog. Target v6.1. The v6.0 user-value case is satisfied by FEAT-46/47/20 and the correctness fix BE-36. BLG-FE-76 will be the lead item in v6.1 planning."

**Facilitator resolution:**
> IDEA-product-owner-20260619-01 advances. No blocking objections. No §13 concerns raised. Assigned BLG-FE-76, P2, Provisional-Target v6.1.
> IDEA-product-owner-20260619-02 (trade tagging) also raised under Product Velocity Concern. Debate: Product Owner notes that BLG-FE-76 addresses the portfolio-visualisation gap and that FEAT-46/47/20 absorb the v6.0 pull-forward. Trade tagging is a larger data model change (2–3 sprint story). Park Cycle 1 is correct. Challenger accepts.

**Outcome:**
- IDEA-product-owner-20260619-01 → **Promoted-Backlog: BLG-FE-76** (P2, M, Provisional-Target v6.1)
- IDEA-product-owner-20260619-02 → **Park Cycle 1** confirmed (no debate outcome changes initial classification)

---

## STEP 6 — Scoring Matrix Overlay

Scoring applied to the one item that required structured debate:

| Item | User Value (U) | Risk (R) | Effort (E) | Strategic Fit (S) | Score | Decision |
|------|---------------|---------|------------|-------------------|-------|---------|
| BLG-FE-76 Heat-map | High (4) | Low (4) | Medium (3) | High (4) | 15/16 | ADVANCE |

No competing ideas required scoring comparison. All other promoted-backlog items were direct-advance with unanimous support.

---

## STEP 7 — Workforce Economics Gate

### STEP 7.1 — Skill-Silo Check

**Skill-Silo Alert fires: G+D+P = 90.7% of last 5 cycles — well above 40% ceiling.**

v6.0 composition must achieve U/(U+G+D+P) ≥ 0.30 for the next cycle to begin correcting the ratio.

| v6.0 story | Type |
|-----------|------|
| BLG-BE-36 (suggested_shares fix) | U (user-observable correctness fix on every signal card) |
| BLG-FEAT-47 (screener telemetry) | G (internal observability — not user-facing product feature) |
| BLG-FEAT-46 (morning briefing dashboard) | U (directly user-facing) |
| BLG-FEAT-20 (net-of-costs tracking) | U (user-facing analytics) |
| BLG-OPS-70 (deep link AC-04 staging) | D (staging verification) |
| BLG-FE-64 (RFJ design pre-brief) | G (design/spec pre-work) |
| BLG-FE-41 (RFJ visual design review) | G (design review) |
| BLG-GOV-113 (SI-05 effectiveness review) | G (governance review, 2026-07-04 gate) |
| BLG-GOV-112 (cadence review) | G (governance review, gate) |
| BLG-GOV-115 (actionability metric) | G (governance review, gate) |
| BLG-GOV-130 (Phase 2 activation scope) | G (governance review, gate) |
| BLG-OPS-59 (p99 latency baseline) | G (ops review, gate) |

v6.0 U-count: 3 of 12 = 25%. Below the 40% ceiling (not the ratio target — v6.0 is moving in the right direction). **Skill-Silo Alert acknowledged. The 40% ceiling in roadmap_prompt.md v7.4 applies to story classification during sprint planning — sprint planning must not accept a sprint where G+D+P > 60%. This is enforced at sprint planning gate, not roadmap gate.**

The roadmap gate (STEP 7) advisory is: v6.0 must not be planned with > 60% G+D+P stories in any single sprint. PMO Lead to flag this constraint during sprint planning.

### STEP 7.2 — Workforce Composition Check

Team composition unchanged. No role gaps identified. All 9 roles present in `claude/agents/`. No escalation.

---

## STEP 8 — Final Rebalance Decision

### STEP 8.0 — Production Correctness Fast-Track

**BLG-BE-36 (P0 — Correctness Bug)** — `signal_service.py` uses cash-allocation model for `suggested_shares` instead of canonical risk-based sizing from `strategy_rules.md §4.1`. Every signal card shows wrong share counts.

Decision: **BLG-BE-36 is the first story in v6.0.** No override. Correctness fast-track applies.

### STEP 8.1 — Empty Now Horizon (Soft Gate)

Now horizon is empty (RA:v5.9 retired 2026-06-18). Soft gate armed.

**Product Owner selects Option (a):** Add v6.0 release section to Now horizon.

**PO written response to Product Value Alert (mandatory per STEP 2.4):**
> "The product value ratio of 0.093 reflects a deliberate governance consolidation phase now completed. I accept the mandatory pull-forward obligation. v6.0 Now horizon will include BLG-BE-36 (visible correctness fix — every signal card), BLG-FEAT-46 (Trader's Morning Briefing dashboard), and BLG-FEAT-20 (net-of-costs performance tracking) as firm U-classified user-facing items, alongside BLG-FEAT-47 (screener telemetry). BLG-FE-76 (heat-map) targets v6.1 as the first dedicated user-value cycle post-consolidation. The Skill-Silo ceiling of 40% in roadmap_prompt.md v7.4 provides structural enforcement going forward. Pull-forward obligation is satisfied. No further rationale required."

### STEP 8.2 — v6.0 Now Horizon Composition

**Firm scope (no gate or gate cleared/imminent):**

| BLG-ID | Title | Priority | Effort | Classification |
|--------|-------|----------|--------|---------------|
| BLG-BE-36 | Align signal_service suggested_shares to risk-based sizing model | P0 | S | U — Correctness Fast-Track (FIRST STORY) |
| BLG-FEAT-47 | Screener data quality telemetry | P1 | S | G |
| BLG-FEAT-46 | Trader's Morning Briefing dashboard | P1 | M | U |
| BLG-FEAT-20 | Net-of-costs performance tracking | P1 | M | U |
| BLG-OPS-70 | SI-05 deep link AC-04 staging confirmation | P2 | XS | D — gate ~2026-06-23 |

**Conditional scope — gate 2026-06-21 (2 days):**

| BLG-ID | Title | Priority | Effort | Gate |
|--------|-------|----------|--------|------|
| BLG-FE-64 | RFJ design review pre-brief | P2 | S | SI-03 live ≥ 30 days (2026-06-21) |
| BLG-FE-41 | Red Flag Journal visual design review | P3 | M | SI-03 live ≥ 30 days (2026-06-21); depends on BLG-FE-64 |

**Conditional scope — gate 2026-07-04:**

*Note: BLG-GOV-96 (effectiveness criteria, v5.2) and BLG-GOV-113 (effectiveness review protocol, v5.3) are both shipped and archived. The items below become actionable once the 2026-07-04 review event has been conducted (pre-work protocols already complete).*

| BLG-ID | Title | Priority | Effort | Gate |
|--------|-------|----------|--------|------|
| BLG-GOV-112 | SI-05 digest weekly cadence review | P2 | S | 2026-07-04 (BLG-GOV-96 shipped v5.2) |
| BLG-GOV-115 | SI-05 digest actionability metric definition | P2 | S | 2026-07-04 (BLG-GOV-113 shipped v5.3) |
| BLG-GOV-130 | SI-05 Phase 2 activation decision scope | P2 | S | 2026-07-04 review conducted |
| BLG-OPS-59 | SI-05 service production p99 latency baseline review | P2 | S | 2026-07-04 |

**Total v6.0 horizon:** 11 items (5 firm + 2 gate-conditional June + 4 gate-conditional July)

**Decision Log entries (DL-048 to DL-051):**
- DL-048: v6.0 Now horizon opened — 12-item scope per above
- DL-049: BLG-FE-76 (heat-map) added to backlog — P2, v6.1 target
- DL-050: IDEA-strategy-owner-20260619-01 rejected (duplicate BLG-SPEC-35)
- DL-051: 6 ideas promoted to backlog (SPEC-56/57, QA-59, OPS-72, BE-37, GOV-131); 8 parked Cycle 1

### STEP 8.3 — Product Velocity Commitment

Given Skill-Silo Alert and Product Value Alert, the following constraint is recorded for sprint planning:

> **Sprint planning gate (v6.0):** No sprint in v6.0 may be sealed with G+D+P > 60% of total stories. PMO Lead must enforce at sprint planning gate. This is non-negotiable per roadmap_prompt.md v7.4 §Skill-Silo ceiling.

### STEP 8.5.B — Write Plan

The following canonical writes will be executed in STEP 9:

| File | Action | Decision authority |
|------|--------|--------------------|
| `claude/roadmap/current_roadmap.md` | Add RA:v6.0 section to Now horizon; update §8 release summary row placeholder | Product Owner |
| `claude/backlog/backlog.md` | Add 7 new items: BLG-SPEC-56, BLG-SPEC-57, BLG-QA-59, BLG-OPS-72, BLG-BE-37, BLG-GOV-131, BLG-FE-76 | PMO Lead |
| `claude/backlog/backlog.md` | Update BLG-BE-36 sprint history / provisional-target note (already correct) | No change needed |
| `claude/roadmap/decision_log.md` | Append DL-048 to DL-051 | Product Owner |
| `claude/ideas/ideas_register.md` | Update all 16 idea rows with final Step 4 / Step 5 outcomes | PMO Lead |
| `claude/roadmap/initiative_register.md` | Confirm no changes (0 active; no new initiatives) | Strategy Rules & System Intent Owner |

---

*Cycle record written per STEP 1.1 instruction. STEP 9 canonical writes follow.*
