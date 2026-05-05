**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-05

---

# Cycle Record — Roadmap Rebalance 2026-05-05__scheduled

Cycle ID: 2026-05-05__scheduled
Run type: Scheduled — no completion event
Tier: Standard

---

## STEP 0 — Load and Validate Inputs

### Carry-Forward Advisory

Most recently completed cycle with `post_ship_complete = true`: `2026-04-29__release-v3.1`
Carry-forward source: `claude/cycles/2026-04-29__release-v3.1/lessons_learnt_closure.md §Carry-Forward`

**Carry-forward items (3):**

| # | Observation | Engine |
|---|-------------|--------|
| 1 | sprint_planning_prompt.md has no branch verification step — artefacts can be committed to non-main branch | Sprint Planning |
| 2 | execution_prompt.md §3.1.A post-story test_scenarios advisory missing — recurring TSG gaps (v3.0 + v3.1) | Sprint Execution |
| 3 | Playwright `waitFor` adoption deferred from v3.0 CF-03 — `networkidle` pattern remains in existing specs | Sprint Execution / QA |

**Action:** Recorded. These are sprint-engine deferred patches (OA-02, OA-03, OA-04 in closure record §6), targeted for v3.2 delivery. No roadmap-level impact.

### Step 0.D — Empty Horizon Advisory

**Now horizon status:** EMPTY. All v3.1 items shipped and RA: annotations retired.

**Active backlog items:** 3 confirmed (BLG-FE-16, BLG-OPS-13, BLG-GOV-11) plus any test-gap items.

> **⚠ Now horizon is empty.** 3+ active backlog items are candidate scope for the next release. If no new strategic initiative is needed, run `plan release --version v3.2` directly. Continue this roadmap run to review 32 parked ideas (many gate-cleared by Arc 1 ship) and confirm Arc 2 continuation plan is correctly positioned.

**Product Owner decision:** Proceed with scheduled rebalance. Arc 1 completing triggers a gate-cleared idea sweep. Arc 2 horizon placement should be validated. Release planning will follow this run.

### Cycle ID and Tier

- Cycle ID: `2026-05-05__scheduled`
- Tier: **Standard** (scheduled run; < 90 days since last scheduled; CPS expected 0.0 with no active initiatives)

---

## STEP 2 — Re-Validation

*Authorities: Product Owner + Strategy Rules & System Intent Owner*

### Active Initiatives Review

**Active initiatives in initiative_register.md as of 2026-05-05:** None.

The initiative register shows:
- Active Initiatives: "No active initiatives as of 2026-04-03"
- Priority 2 (Next Phase): "No active Priority 2 initiatives as of 2026-05-05. PT-02 frontend, PT-03, PT-05 deferred to v3.2."

The roadmap's **Priority 2 — Horizon: Next Phase** section contains Arc 2 continuation items (PT-02 frontend, PT-03, PT-04, PT-05) but these are not registered as active initiatives — they are planned but uncommitted. No formal initiative is consuming active resources.

**Force classification:** N/A — no active initiatives to classify. No items to mark 🔥 / ⚠ / ❌.

### 2.1 Strategy Proximity Scores

No active initiatives to score. CPS = 0.0.

### 2.2 Cycle Proximity Score (CPS)

| Metric | Value |
|--------|-------|
| CPS (this cycle) | 0.0 — no active initiatives |
| Prior cycle CPS | 0.0 (2026-04-24__scheduled — also no active initiatives) |
| Delta | 0.0 — no drift |
| Strategy Drift Alert | None required |

**CPS: 0.0. No drift. No alert.**

### Horizon Review (STEP 2.3)

**Now horizon:** EMPTY. All v3.1 items shipped and retired. No uncommitted items.

**Next Phase — Horizon: Next (Arc 2):**

| Feature | ID | Status | Assessment |
|---------|----|--------|------------|
| Pre-Trade Research View (frontend) | PT-02 | Deferred to v3.2 | ✅ Correctly placed — backend shipped v3.1; frontend is Arc 2 primary v3.2 commitment |
| Prospective Heat at Entry | PT-03 | Deferred to v3.2 | ✅ Correctly placed — `GET /portfolio/prospective-heat` shipped v2.0; frontend integration into PT-02 only |
| Pre-Trade Entry Checklist | PT-05 | Deferred to v3.2+ | ✅ Correctly placed — embedded in Trade Plan flow; depends on PT-02 |
| Setup Quality Score | PT-04 | Pending (gate: 20+ closed trades) | ✅ Correctly placed — data gate not yet met |

**Later horizon — Arc 3–6:** All correctly placed. IT-06 (Alpaca Paper Trading) gate open (§13 review required). SI-01/SI-03 noted as pull-forward candidates for Arc 3.

**Horizon movement recommendations:** None. Arc 2 continuation (PT-02, PT-03, PT-05) is correctly positioned in Next horizon. No promotions or demotions warranted.

---

## STEP 3 — Backlog Health Review

*Authority: Head of Specs Team (process), Product Owner (planning ownership)*

**Active backlog items reviewed:**

| ID | Title | Priority | Target | Assessment |
|----|-------|----------|--------|------------|
| BLG-FE-16 | React component inventory | P3 | v3.2 | Still valid — Arc 2 frontend (PT-02) will benefit from this inventory. No obsolescence. |
| BLG-OPS-13 | Add v2.8–v3.1 endpoints to api_performance_baseline.md | P3 | Before next perf review | Still valid — now 18 endpoints. Scope correctly extended in v3.1 closure. |
| BLG-GOV-11 | Cycle artefact inventory and maintenance review | P3 | v3.2 | Still valid — now 3 consecutive deferrals (v3.0, v3.1, now v3.2 target). Not stale enough to retire; genuine gap. |

**§9 Deferred items check:**
- BLG-TECH-05 (Prometheus): No urgency change. Stays deferred.
- BLG-SPEC-20 (Machine-readable spec front-matter): No urgency change. Stays deferred.
- Others: No change.

**Obsolete items:** None identified.
**Duplicates:** None identified.
**Strategic alignment:** All 3 active items remain aligned (operations hygiene, governance quality, frontend documentation).
**Quick wins ignored:** BLG-OPS-13 and BLG-GOV-11 are both P3 quick wins that could be scheduled. They are candidates for v3.2 alongside Arc 2 features.
**Technical debt:** BLG-OPS-13 represents 18 endpoints without performance baseline — minor operational debt accumulating. BLG-GOV-11 represents artefact lifecycle gap.

**Backlog health: GOOD.** 3 active items; all valid; no obsolescence; no duplicates; no strategic misalignment.

---

## STEP 4 — Ideas

*Authority: Facilitator (review), Product Owner (classification)*

**Ideas register loaded:** claude/ideas/ideas_register.md
**Open ideas (Submitted or Parked-cycle-N):** 32 (0 Submitted + 32 Parked-cycle-N)

### Gate-Condition Re-Check (STEP 4.0)

The Facilitator performed a gate-condition re-check on all 32 parked ideas for BLG- references in Park Rationale.

**Key context for gate-cleared items:**
- Arc 1 is now fully complete: DS-01 (v3.0), DS-02 (v3.0), DS-06 (v3.0), DS-07 (v3.0), DS-04 (v3.1) all shipped.
- BLG-QA-08 (mock harness) shipped v2.9. BLG-QA-10 (screener test coverage) and BLG-QA-11 (screener acceptance tests) shipped v3.1.
- BLG-FE-17 (screener UX spec) shipped v2.9. BLG-FE-16 (React component inventory) is still in backlog (NOT shipped).
- BLG-SPEC-21 (screener engine spec) shipped v2.9. BLG-SPEC-22 (Alpaca API contract) shipped v2.9.
- BLG-AI-01 (AI journal audit log) shipped v2.9.

**Gate-Condition Re-Check Results:**

| Idea ID | Gate Referenced | Gate Status | Action Required |
|---------|----------------|-------------|-----------------|
| IDEA-frontend-ux-20260304-02 | BLG-FE-16 (React component inventory) | ❌ NOT cleared — still in backlog | Normal park |
| IDEA-head-of-ux-20260321-02 | Arc 1 screener frontend shipping (v3.0/v3.1) | ✅ CLEARED — Arc 1 complete (DS-04 shipped v3.1) | Mandatory re-evaluation |
| IDEA-product-owner-20260421-01 | DS-01/DS-02 ship | ✅ CLEARED — DS-01/02 shipped v3.0 | Mandatory re-evaluation |
| IDEA-pmo-lead-20260421-01 | Arc 1 ships ("premature before Alpaca integrated") | ✅ CLEARED — Arc 1 complete | Mandatory re-evaluation |
| IDEA-director-of-quality-20260421-02 | DS-01 screener engine | ✅ CLEARED — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-finops-20260421-01 | DS-01 driving real call volume | ✅ CLEARED — DS-01 live since v3.0 | Mandatory re-evaluation |
| IDEA-finops-20260421-02 | DS-01/Arc 1 ships | ✅ CLEARED — Arc 1 complete | Mandatory re-evaluation |
| IDEA-infra-ops-20260421-02 | v3.0 sprint planning (screener scheduling decision) | ✅ CLEARED — v3.0 sprint planning complete; decision made | Mandatory re-evaluation |
| IDEA-challenger-20260421-01 | BLG-FE-17 shipping | ✅ CLEARED — BLG-FE-17 shipped v2.9; concern resolved per park rationale | Mandatory re-evaluation |
| IDEA-backend-engineering-20260421-01 | DS-01 design in progress at v3.0 | ✅ CLEARED — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-cybersecurity-20260421-01 | Arc 1 ships + key usage patterns established | ✅ CLEARED — Arc 1 shipped; 4+ months Alpaca usage | Mandatory re-evaluation |
| IDEA-cybersecurity-20260421-02 | Arc 1 complete | ✅ CLEARED — Arc 1 complete | Mandatory re-evaluation |
| IDEA-metrics-analytics-20260421-01 | DS-01 live | ✅ CLEARED — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-metrics-analytics-20260421-02 | DS-01 live | ✅ CLEARED — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-head-of-engineering-20260421-01 | v3.0 sprint planning when DS-01 scoped | ✅ CLEARED — v3.0 sprint planning complete | Mandatory re-evaluation |
| IDEA-head-of-engineering-20260421-02 | BLG-QA-08 shipped; data pipeline tests in DS-01 sprint | ✅ CLEARED — DS-01 shipped with BLG-QA-10/11 | Mandatory re-evaluation |
| IDEA-data-model-20260421-01 | DS-01 extension at v3.0 sprint planning | ✅ CLEARED — v3.0 sprint planning complete | Mandatory re-evaluation |
| IDEA-data-model-20260421-02 | BLG-SPEC-21 shipped; ticker universe in DS-01 scope | ✅ CLEARED — DS-01 + ticker universe endpoints shipped | Mandatory re-evaluation |
| IDEA-financial-reporting-20260421-01 | DS-01 live + attributed trades | 🟡 PARTIAL — DS-01 live but attribution data insufficient (10 days) | Mandatory re-evaluation (partial gate) |
| IDEA-financial-reporting-20260421-02 | DS-01 live | ✅ CLEARED — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-director-of-hr-20260421-02 | Post-Arc 1 re-evaluate if integration failures surface | ✅ CLEARED — Arc 1 shipped; no failures | Mandatory re-evaluation |
| IDEA-qa-testing-20260421-02 | BLG-SPEC-21 shipped; DS-01 scoped at v3.0 | ✅ CLEARED — DS-01 shipped at v3.0 | Mandatory re-evaluation |
| IDEA-qa-lead-20260421-02 | DS-01 scoped at sprint planning | ✅ CLEARED — DS-01 shipped at v3.0 | Mandatory re-evaluation |
| IDEA-head-of-ux-20260421-01 | DS-01 live | ✅ CLEARED — DS-01 shipped v3.0 | Mandatory re-evaluation |

**No-gate items (park rationale does not reference a BLG- item that shipped):**
- IDEA-challenger-20260321-01 (references roadmap_prompt.md governance mechanism)
- IDEA-ai-compliance-20260321-01 (governance volume timing — no specific shipped gate)
- IDEA-metrics-analytics-20260321-02 (references PT-04 — not yet shipped)
- IDEA-financial-reporting-20260321-02 (data model expansion timing — no specific shipped gate; but stale)
- IDEA-product-owner-20260421-02 (screener + attribution data — screener live but attribution insufficient)
- IDEA-head-of-specs-20260421-01 (needs 2 integrations — still only 1)
- IDEA-pmo-lead-20260421-02 (general improvement)
- IDEA-director-of-hr-20260421-01 (general process overhead)

### Stale Ideas Identified (≥ 3 consecutive cycles parked)

| Idea ID | Cycles Parked | Gate Status |
|---------|--------------|-------------|
| IDEA-frontend-ux-20260304-02 | 11 | Not cleared (BLG-FE-16) |
| IDEA-challenger-20260321-01 | 7 | No gate |
| IDEA-ai-compliance-20260321-01 | 7 | No gate |
| IDEA-metrics-analytics-20260321-02 | 7 | PT-04 not shipped |
| IDEA-financial-reporting-20260321-02 | 7 | No gate |
| IDEA-head-of-ux-20260321-02 | 7 | Gate CLEARED (Arc 1 complete) |

All 6 stale ideas surfaced to Product Owner for mandatory disposition.

### 4.1 Per-Idea Classification

**Stale ideas — mandatory disposition first:**

**IDEA-frontend-ux-20260304-02** (Accessibility Baseline, 11 cycles)
Gate: BLG-FE-16 not shipped. Park rationale remains valid. PO decision: **🅿 Park** — BLG-FE-16 is still in backlog targeted for v3.2; the dependency gate remains valid; re-park with updated rationale.

**IDEA-challenger-20260321-01** (SPS≥4 mandatory §13 review gate, 7 cycles)
No gate. Roadmap_prompt.md Score-4 soft rule already enforces SPS≥4 handling. 7 consecutive cycles; no evidence the existing mechanism is insufficient. PO decision: **❌ Reject (not strong)** — existing governance mechanism in roadmap_prompt.md STEP 5 adequately handles SPS≥4 items; dedicated gate is redundant.

**IDEA-ai-compliance-20260321-01** (Governed decision audit log, 7 cycles)
No gate. decision_log.md provides strong coverage. Searchable audit log would add value in principle but overhead not justified. 17 completed cycles; no searchability incident. PO decision: **❌ Reject (strong)** — decision_log.md provides adequate coverage at current scale; a searchable audit log system would be genuinely valuable at larger team/governance volume; retained as rejected-strong.

**IDEA-metrics-analytics-20260321-02** (ATR-normalised sizing retrospective, 7 cycles)
Gate: PT-04 (Setup Quality Score, depends on 20+ closed trades) not shipped. Re-park rationale: PT-01 Trade Plan Object shipped v3.1; PT-04 depends on PT-01 + 20+ closed trades; ATR sizing retrospective remains premature until PT-04 baseline quality scoring exists; park pending PT-04 completion. PO decision: **🅿 Park** — new rationale: depends on PT-04 which is gate-blocked by 20+ closed trade requirement.

**IDEA-financial-reporting-20260321-02** (Net-of-costs performance tracking, 7 cycles)
No gate. Arc 2 data model (PT-01) now shipped. Fee tracking at trade level now feasible. Accurate R-multiples for Arc 4 analysis require net-of-costs data. 7 cycles; context has changed with PT-01 ship. PO decision: **✅ Advance** — PT-01 data model unlocks net-of-costs tracking; Arc 4 plan vs reality analysis benefits from accurate R-multiples; advance to STEP 5.

**IDEA-head-of-ux-20260321-02** (Design system document, 7 cycles, gate CLEARED)
Gate cleared: Arc 1 screener frontend (v3.0/v3.1) has shipped; design inconsistencies are now observable. Arc 2 frontend (PT-02) coming in v3.2 will add more UI surface. MANDATORY re-evaluation. PO decision: **✅ Advance** — gate cleared; Arc 2 frontend delivery makes design system documentation timely; advance to STEP 5.

**Gate-cleared ideas — mandatory re-evaluation:**

**IDEA-product-owner-20260421-01** (Screener morning routine UX — guided daily flow)
Gate cleared: DS-01/DS-02 shipped v3.0. The Arc 1→Arc 2 junction UX (screener results → shortlist → watchlist → pre-trade research) is now relevant to design. PT-02 (Pre-Trade Research View) is the next Arc 2 deliverable. PO decision: **✅ Advance** — DS-01/02 shipped; this UX spec is needed to inform Arc 2 design; advance to STEP 5.

**IDEA-pmo-lead-20260421-01** (External API dependency risk register)
Gate cleared: Arc 1 complete; Alpaca in production since v2.9. Yahoo Finance also production-critical. No formal register tracks reliability, fallback status, SLA concerns. Lightweight governance hygiene. PO decision: **✅ Advance** — Alpaca now production-critical for daily screener; governance register warranted; advance to STEP 5.

**IDEA-director-of-quality-20260421-02** (Screener accuracy test protocol)
Gate cleared: DS-01 shipped v3.0. BLG-QA-10 screener test coverage and BLG-QA-11 screener acceptance tests shipped v3.1. Basic coverage addressed. Formal accuracy protocol (comparison against manually verified expected outputs) adds value but lower urgency than Arc 2 delivery. PO decision: **🅿 Park** — new rationale: BLG-QA-10/11 delivered screener test coverage v3.1; formal accuracy protocol is a P3 enhancement warranted for v3.3+ QA planning once screener is in stable production; park without BLG- reference.

**IDEA-finops-20260421-01** (Alpaca API cost monitoring)
Gate cleared: DS-01 live since v3.0 (2026-04-27 — 10 days). Alpaca calls are real. However, Alpaca is on free tier; no evidence of approaching limits in first 10 days. PO decision: **✅ Advance** — screener driving real Alpaca volume; monitoring warranted before approaching tier limits; advance to STEP 5.

**IDEA-finops-20260421-02** (Data pipeline cost baseline)
Gate cleared: DS-01 shipped. However: Alpaca on free tier; no observed cost concern. This is lower urgency than finops-20260421-01. PO decision: **🅿 Park** — new rationale: Alpaca free tier has no material cost pressure after 10 days of DS-01 operation; cost baseline relevant only after monitoring (IDEA-finops-20260421-01) surfaces an actual trend; park for v3.3+.

**IDEA-infra-ops-20260421-02** (Screener run scheduler decision record)
Gate cleared: v3.0 sprint planning complete. The scheduler decision was made at v3.0 sprint planning (on-demand approach implemented in DS-01). This item is SUPERSEDED. PO decision: **❌ Reject (not strong)** — scheduler decision was made during DS-01 implementation; on-demand architecture implemented; no separate decision record needed.

**IDEA-challenger-20260421-01** (Screener result stale data risk)
Gate: BLG-FE-17 shipped v2.9; concern addressed in spec. Park rationale already stated concern was resolved. MANDATORY re-evaluation. PO decision: **❌ Reject (not strong)** — freshness indicator requirement captured in BLG-FE-17 spec and implemented in screener frontend; concern fully addressed; no residual item needed.

**IDEA-backend-engineering-20260421-01** (Screener result caching strategy)
Gate cleared: DS-01 shipped v3.0. The caching architectural decision was made during DS-01 implementation (on-demand approach: screener runs on-demand, no persistent result caching needed at current scale). SUPERSEDED by implementation decision. PO decision: **❌ Reject (not strong)** — DS-01 caching approach determined during implementation; no separate caching spec item warranted at current scale.

**IDEA-cybersecurity-20260421-01** (Alpaca API key rotation policy)
Gate cleared: Arc 1 shipped; Alpaca key in production for 4+ months. No formal rotation policy exists. Low effort (S). PO decision: **✅ Advance** — Alpaca key is production-critical; key rotation policy is security hygiene; advance to STEP 5.

**IDEA-cybersecurity-20260421-02** (External API credential audit)
Gate cleared: Arc 1 complete. Overlaps with IDEA-cybersecurity-20260421-01 in scope. If key rotation policy advances, the credential audit scope can be incorporated. PO decision: **✅ Advance** — independent value from rotation policy (inventory vs policy); advance to STEP 5; Challenger will be asked to assess overlap.

**IDEA-metrics-analytics-20260421-01** (Screener hit rate metric)
Gate cleared: DS-01 live. However, screener only live 10 days — insufficient promotion-to-trade data. PO decision: **🅿 Park** — new rationale: screener live 10 days since v3.0 (2026-04-27); insufficient data to define or measure hit rate meaningfully; park until 60+ days of screener usage establishes a baseline.

**IDEA-metrics-analytics-20260421-02** (Regime distribution metric)
Gate cleared: DS-01 live. Same data maturity constraint as above. PO decision: **🅿 Park** — new rationale: screener data volume insufficient at 10 days; regime distribution requires representative screener run history; park until v3.3+ once 60+ days of screener data exists.

**IDEA-head-of-engineering-20260421-01** (Screener engine performance benchmark)
Gate cleared: v3.0 sprint planning complete. BLG-OPS-13 already tracks API performance baseline including screener endpoints. PO decision: **🅿 Park** — new rationale: screener endpoints should be included in BLG-OPS-13 scope (which tracks all new endpoints); separate benchmark item is redundant with BLG-OPS-13; park and incorporate into BLG-OPS-13 review.

**IDEA-head-of-engineering-20260421-02** (Data pipeline integration test suite)
Gate cleared: DS-01 shipped. BLG-QA-08 (mock harness) shipped v2.9. BLG-QA-10 screener test coverage shipped v3.1. Data pipeline integration testing addressed. SUPERSEDED. PO decision: **❌ Reject (not strong)** — addressed by BLG-QA-08 (mock harness) + BLG-QA-10 (screener test coverage, v3.1).

**IDEA-data-model-20260421-01** (Screener result history table)
Gate cleared: DS-01 shipped. Screener results persist results on-demand but no historical table exists. This would enable day-over-day comparison of screener output. Arc 1.5 extension. PO decision: **🅿 Park** — new rationale: useful Arc 1.5 extension but requires real screener usage data to validate whether day-over-day comparison is a workflow users (me) actually want; park for v3.3+ once screener usage patterns are understood.

**IDEA-data-model-20260421-02** (Ticker universe management data model)
Gate cleared: DS-01 shipped. Ticker universe management endpoints (GET/POST/DELETE /ticker-universe) implemented as part of DS-01. SUPERSEDED. PO decision: **❌ Reject (not strong)** — ticker universe management data model implemented in DS-01; `GET /ticker-universe`, `POST /ticker-universe`, `DELETE /ticker-universe/{ticker}` endpoints shipped v3.0.

**IDEA-financial-reporting-20260421-01** (Screener-to-trade attribution)
Partial gate: DS-01 live but only 10 days of screener usage; attribution data insufficient. PO decision: **🅿 Park** — new rationale: screener live 10 days; insufficient screener-promoted→watchlist→position attribution chain to measure; park until 60+ screener-attributed positions exist (estimated v3.4+).

**IDEA-financial-reporting-20260421-02** (External API cost attribution)
Gate cleared: DS-01 live. Alpaca on free tier; no material cost concern observed. FinOps item. PO decision: **🅿 Park** — new rationale: Alpaca free tier; no material API cost observed post-Arc 1 launch; attribution premature until actual cost data motivates analysis; park until cost monitoring (finops-20260421-01, advancing) surfaces a trend.

**IDEA-director-of-hr-20260421-02** (External API expertise register)
Gate cleared: Arc 1 shipped; no integration failures observed. Agent charters define ownership implicitly. Overhead not justified. PO decision: **❌ Reject (not strong)** — no API integration failures in Arc 1; ownership clear through agent charters; overhead not justified at solo-dev scale.

**IDEA-qa-testing-20260421-02** (Screener scenario library)
Gate cleared: DS-01 shipped at v3.0. BLG-QA-10 screener test coverage shipped v3.1 providing the scenario library foundation. SUPERSEDED. PO decision: **❌ Reject (not strong)** — BLG-QA-10 screener test coverage shipped v3.1; test scenarios are now defined and in use; no separate item needed.

**IDEA-qa-lead-20260421-02** (Screener QA sign-off criteria)
Gate cleared: DS-01 shipped at v3.0. QA sign-off criteria were established through the DoQ sign-off process in v3.1 (EPIC-03 QA evidence). Addressed by process. PO decision: **❌ Reject (not strong)** — screener QA sign-off criteria established through v3.1 DoQ sign-off process; criteria now embedded in governance practice; no separate formal document needed.

**IDEA-head-of-ux-20260421-01** (Arc 1 daily workflow journey map)
Gate cleared: DS-01 live. Journey map for the morning workflow is research. Related to IDEA-product-owner-20260421-01 (screener morning routine UX) which is advancing. PO decision: **🅿 Park** — new rationale: IDEA-product-owner-20260421-01 (screener morning routine UX) is advancing in this cycle and covers the actionable UX spec form of this research; journey map level of analysis premature before UX spec is defined; park pending outcome of PO-20260421-01 debate.

**Non-gate-cleared, non-stale items:**

**IDEA-product-owner-20260421-02** (Candidate quality retrospective — screener hit rate → position performance)
Park rationale: requires screener live + multiple attributed trades. Screener is live but attribution data minimal (10 days). Re-park: "Screener live since v3.0 (2026-04-27); screener-to-trade attribution chain requires 60+ attributed positions for meaningful retrospective; park until v3.4+ once data foundation established." **🅿 Re-park.**

**IDEA-head-of-specs-20260421-01** (External API integration spec template)
Park rationale: needs 2 integrations. Still only 1 (Alpaca). Gate not cleared. Re-park: "Only one external API integration in production (Alpaca); reusable template justified only with ≥2 integrations; park until second external API integration materializes." **🅿 Re-park.**

**IDEA-pmo-lead-20260421-02** (Arc velocity tracking by Arc theme)
Park rationale: velocity_metrics.md adequate. No urgency change. Re-park: "velocity_metrics.md provides adequate cycle-level velocity tracking; Arc-level breakdown is a P3 enhancement; park for v3.4+." **🅿 Re-park.**

**IDEA-director-of-hr-20260421-01** (Arc 1 team readiness assessment)
Park rationale: overhead not warranted. Arc 1 delivered successfully without this process. Re-park: "Arc 1 delivered successfully at 1.00 velocity without formal readiness assessment; process overhead not justified at solo-dev scale; park indefinitely pending team scale change." **🅿 Re-park.**

### 4.2 Document Management Summary

All register row updates applied after classification. See ideas_register.md for terminal state.

### 4.3 Idea Participation Check

No window summary for this cycle (idea intake engine was not run — count ≥ 20 ideas, intake skipped per STEP -1.6).

### 4.4 Idea Intake Summary

```
Window: not run this cycle (32 open ideas ≥ 20 threshold — intake skipped)
Total submissions loaded: 32 (all Parked-cycle-N)
Advancing to STEP 5: 7
Re-parked with new rationale: 15
Rejected: 10 (1 strong, 9 not strong)
Stale ideas (≥3 cycles parked) surfaced: 6
Stale ideas closed this cycle: 2 (IDEA-challenger-20260321-01, IDEA-ai-compliance-20260321-01)
```

**Ideas Advancing to STEP 5**

| Idea ID | Agent | Title | Displacement Named |
|---------|-------|-------|--------------------|
| IDEA-head-of-ux-20260321-02 | Head of UX & Design | Design system document | TBD at STEP 5 |
| IDEA-financial-reporting-20260321-02 | Financial Reporting & Records Owner | Net-of-costs performance tracking | TBD at STEP 5 |
| IDEA-product-owner-20260421-01 | Product Owner | Screener morning routine UX | TBD at STEP 5 |
| IDEA-pmo-lead-20260421-01 | PMO Lead | External API dependency risk register | TBD at STEP 5 |
| IDEA-cybersecurity-20260421-01 | Cybersecurity & Trust Lead | Alpaca API key rotation policy | TBD at STEP 5 |
| IDEA-cybersecurity-20260421-02 | Cybersecurity & Trust Lead | External API credential audit | TBD at STEP 5 |
| IDEA-finops-20260421-01 | FinOps & Resource Architect | Alpaca API cost monitoring | TBD at STEP 5 |

**Rejected Ideas**

| Idea ID | Agent | Title | Strong? |
|---------|-------|-------|---------|
| IDEA-challenger-20260321-01 | Challenger | SPS≥4 mandatory §13 review gate | No |
| IDEA-ai-compliance-20260321-01 | AI Compliance & Governance Officer | Governed decision audit log | Yes |
| IDEA-infra-ops-20260421-02 | Infrastructure & Operations Owner | Screener run scheduler decision record | No |
| IDEA-challenger-20260421-01 | Challenger | Screener result stale data risk | No |
| IDEA-backend-engineering-20260421-01 | Backend Engineering Patterns Owner | Screener result caching strategy | No |
| IDEA-head-of-engineering-20260421-02 | Head of Engineering | Data pipeline integration test suite | No |
| IDEA-data-model-20260421-02 | Data Model & Domain Schema Owner | Ticker universe management data model | No |
| IDEA-director-of-hr-20260421-02 | Director of HR | External API expertise register | No |
| IDEA-qa-testing-20260421-02 | QA & Testing Owner | Screener scenario library | No |
| IDEA-qa-lead-20260421-02 | QA Lead | Screener QA sign-off criteria | No |

**Stale Idea Dispositions**

| Idea ID | Agent | Cycles Parked | Disposition | Rationale |
|---------|-------|--------------|-------------|-----------|
| IDEA-frontend-ux-20260304-02 | Frontend Specs & UX Documentation Owner | 11 | Re-park | BLG-FE-16 gate still valid |
| IDEA-challenger-20260321-01 | Challenger | 7 | Reject (not strong) | Existing governance mechanism adequate |
| IDEA-ai-compliance-20260321-01 | AI Compliance & Governance Officer | 7 | Reject (strong) | decision_log.md adequate at current scale |
| IDEA-metrics-analytics-20260321-02 | Metrics Definitions & Analytics Canonical Owner | 7 | Re-park | Depends on PT-04 (not yet shipped) |
| IDEA-financial-reporting-20260321-02 | Financial Reporting & Records Owner | 7 | ✅ Advance | PT-01 data model now shipped; context changed |
| IDEA-head-of-ux-20260321-02 | Head of UX & Design | 7 | ✅ Advance | Gate cleared — Arc 1 complete; mandatory re-evaluation |

## STEP 5 Debate Queue

| IDEA ID | Title | Source |
|---------|-------|--------|
| IDEA-head-of-ux-20260321-02 | Design system document | stale + gate-cleared |
| IDEA-financial-reporting-20260321-02 | Net-of-costs performance tracking | stale |
| IDEA-product-owner-20260421-01 | Screener morning routine UX | gate-cleared |
| IDEA-pmo-lead-20260421-01 | External API dependency risk register | gate-cleared |
| IDEA-cybersecurity-20260421-01 | Alpaca API key rotation policy | gate-cleared |
| IDEA-cybersecurity-20260421-02 | External API credential audit | gate-cleared |
| IDEA-finops-20260421-01 | Alpaca API cost monitoring | gate-cleared |

**Queue count: 7. Advancing count: 7. ✅ Match confirmed.**

---

## STEP 5 — Debate

*Authorities: Product Owner (chair) + Challenger (non-decision challenge)*

**Prerequisite restatement (per Section 8):**
1. The system is a deterministic, human-in-the-loop tool — no automated decisions (§3).
2. Zero-sum displacement: no item advances without naming what it replaces in the priority queue. (No active roadmap initiatives exist; displacement applies to backlog priority ordering and capacity.)

**STEP 5.0 Pre-Debate Gate Checks:**
- PoG validity check: No candidates carry hard gates from prior cycles requiring PoG re-check. ✅ Pass.
- Score-5 presence check: No candidate has an SPS of 5. ✅ Pass.

---

### Debate: IDEA-head-of-ux-20260321-02 — Design System Document

**5.0 Required Case (Product Owner):**
1. *Problem:* The system's UI has accumulated organically across 17 releases. Arc 1 added significant new components (screener results, watchlist promotion, news panel). Arc 2 will add more (pre-trade research view, trade plan form, checklist). Without a documented design system, each new UI surface risks inconsistent patterns — different spacing, colour usage, component behaviour.
2. *Strategy intent served:* §3 (human-in-the-loop) — quality of decision support depends partly on the clarity and consistency of the UI presenting information. Not a §13 boundary item.
3. *If we don't:* Design inconsistencies compound across Arc 2/3. Technical debt accumulates in the frontend. Re-standardisation later costs more.
4. *Displacement:* BLG-FE-16 (React component inventory, P3, M) is already in the backlog. This item is complementary — the design system captures the implicit design language, BLG-FE-16 catalogs the components. They could be merged or sequenced (BLG-FE-16 first, then design system). Displacement: this item takes the next available P3 FE slot.

**5.1 Challenger Counter-Argument:**
- Challenger position: **Park**
- Evidence: `strategy_rules.md §3` — the system is a single-user, human-in-the-loop decision support tool. Design system documents are organizational tools for teams with multiple designers and developers. No external contributors. No design team.
- Reason: The implicit design system is maintained by one developer who created it. A formal design system document adds maintenance overhead without providing coordination value — coordination is implicit in a solo project. The risk of "design inconsistency compounding" is present but manageable by the developer without formalisation. At this scale, a CLAUDE.md UI note is more proportionate than a full design system document.
- Consequence: Advancing creates a governance document with maintenance obligations that exceed its value at current scale.

**5.2 Product Owner Response:**
The Challenger's argument is well-formed but underestimates the problem. The developer (me) is not always consistent across sessions — I have returned to the UI after weeks and made inconsistent decisions. A design system document is not for a team; it is for the developer across time. BLG-FE-16 (component inventory) explicitly acknowledges this problem. With Arc 2/3 adding substantial new UI, a design reference prevents the "what did I decide about X last time" problem. M effort is a one-time cost; the maintenance overhead is minimal (update when system-wide patterns change, not per-feature).

Counter-argument does not apply: the value is not coordination between team members but consistency across time for a single developer. **Maintain ✅ Advance.** Displacement: takes next P3 FE backlog slot (BLG-FE-21).

**Outcome: ✅ Advance** — promoted to backlog as BLG-FE-21.

---

### Debate: IDEA-financial-reporting-20260321-02 — Net-of-Costs Performance Tracking

**5.0 Required Case (Product Owner):**
1. *Problem:* The system calculates P&L including fees (Fee Drag % metric, shipped v2.4). But performance metrics (R-multiple, win rate, expectancy) use gross figures. When evaluating edge (Arc 4, Arc 6), inaccurate R-multiples that ignore transaction costs will overstate performance, potentially masking a genuinely unprofitable strategy.
2. *Strategy intent served:* Arc 4 (Post-Trade Intelligence) — plan vs reality analysis and expectancy calculations require accurate per-trade net returns.
3. *If we don't:* Arc 4 analytics will be built on gross R-multiples. When trade history is large enough for statistical analysis (Arc 6), the conclusions may be distorted.
4. *Displacement:* P3 product feature slot. No active items displaced; adds to backlog below current Arc 2 priorities.

**5.1 Challenger Counter-Argument:**
- Challenger position: **Park**
- Evidence: `strategy_rules.md §2` — "enforce asymmetric risk: losses are tolerated; gains are defended." The strategy is evaluated on R-multiples and win rate. Current `Fee Drag %` metric surfaces the aggregate cost impact.
- Reason: UK stock trading fees (IBKR, Freetrade) are typically flat or tiered — not per-share. A 0.1% fee on a typical position is immaterial to a strategy requiring 2R+ to justify a trade. The impact on R-multiple accuracy is small. Arc 4 is 3–4 releases away. Building the data model for net-of-costs tracking now, before Arc 4, is premature — Arc 4 may redesign the data model entirely around trade plans (PT-01), making this backlog item redundant.
- Consequence: Advancing adds a data model change to v3.2+ scope ahead of the arc that will benefit from it, potentially creating rework when Arc 4 defines its data model.

**5.2 Product Owner Response:**
The Challenger raises a valid timing concern. The data model change required for net-of-costs tracking (adding brokerage cost fields per trade) is small and PT-01 (Trade Plan Object, shipped v3.1) already extended the trade data model. Adding cost fields at v3.3+ alongside Arc 3 data model work is more efficient than standalone. However, the Challenger is right that Arc 4 will be the primary beneficiary — and if Arc 4 redesigns the model, this item may be redundant.

**Accept Challenger partially:** Advance to backlog as P2 (important for edge analysis accuracy) but flagged as "deliver alongside Arc 3/4 data model work, not as a standalone sprint item." **Maintain ✅ Advance.** Displacement: P2 feature backlog slot (BLG-FEAT-20). Delivery note: deliver when Arc 3 or Arc 4 data model work provides a natural change context.

**Outcome: ✅ Advance** — promoted to backlog as BLG-FEAT-20 (P2, delivery note: defer until Arc 3/4 data model context).

---

### Debate: IDEA-product-owner-20260421-01 — Screener Morning Routine UX

**5.0 Required Case (Product Owner):**
1. *Problem:* The screener is live (v3.0). The current flow — screener results → manual add to watchlist → separate watchlist view → pre-trade research — requires multiple context switches. A guided morning routine UX would unify: view screener results, shortlist candidates, promote to watchlist, and navigate to pre-trade research for top candidates, all in a coherent flow. This informs the Arc 2 PT-02 UX design.
2. *Strategy intent served:* Arc 1→Arc 2 funnel — the "end state" of Arc 1 is "each morning you open the screener and see a ranked list." The UX for acting on that list is not yet fully designed.
3. *If we don't:* Arc 2 PT-02 (Pre-Trade Research View) design proceeds without a clear picture of how users move from screener discovery to research. Risk: PT-02 UX is designed in isolation rather than as a natural next step from the screener flow.
4. *Displacement:* P2 UX spec backlog slot (BLG-FE-22). S effort — this is a spec/research task, not a build.

**5.1 Challenger Counter-Argument:**
- Challenger position: **Park**
- Evidence: `strategy_rules.md §3` (human-in-the-loop model). DS-07 (Watchlist Promotion Flow) shipped v3.0 — direct screener-to-watchlist promotion exists. The pre-trade research surface (PT-02) is the Arc 2 feature that addresses the "what next" question.
- Reason: The watchlist promotion flow (DS-07) already handles the primary Arc 1→Arc 2 transition (screener → watchlist). PT-02 will define its own UX based on what information is needed for pre-trade research. A separate "morning routine UX spec" adds a documentation artefact that will be superseded when PT-02 UX is designed. The risk of Arc 2 UX being designed in isolation is addressed by running `plan release --version v3.2` where UX context is carried into sprint planning.
- Consequence: Advancing creates a UX spec that may constrain PT-02 design before that design process has even started.

**5.2 Product Owner Response:**
The Challenger correctly identifies that DS-07 addresses the mechanical transition (screener → watchlist) and that PT-02 will have its own UX design phase. However, the "morning routine UX" spec is about the WORKFLOW across the two surfaces — not the UI of either. It answers: "After I promote 3 candidates to my watchlist, how should I navigate to research each one? Should the screener remember what I shortlisted? What information should I carry between screens?" This workflow design IS needed before PT-02 UX, not redundant with it.

Accept advance: this is a pre-design UX research spec, not a feature spec. P2 UX slot. **Maintain ✅ Advance.** Displacement: takes BLG-FE-22 slot (P2, UX spec).

**Outcome: ✅ Advance** — promoted to backlog as BLG-FE-22.

---

### Debate: IDEA-pmo-lead-20260421-01 — External API Dependency Risk Register

**5.0 Required Case (PMO Lead / Product Owner):**
1. *Problem:* Alpaca Markets API is now production-critical — the screener engine depends on it for daily OHLCV bars. Yahoo Finance is also in the data pipeline. No formal register tracks: which endpoints are used, reliability record, known failure modes, fallback status, SLA concerns, and what happens if the API is deprecated. The GET /health endpoint provides real-time health but not risk assessment.
2. *Strategy intent served:* Operational resilience. §14 of strategy_rules.md (if applicable — not a strategy boundary item).
3. *If we don't:* An Alpaca API deprecation or rate limit change could disable the screener without a documented response plan.
4. *Displacement:* Small governance slot. S effort — lightweight register doc, updated at each rebalance. Displaces a lower-priority governance item (BLG-GOV-18 slot).

**5.1 Challenger Counter-Argument:**
- Challenger position: **Clearance Statement**
- *Cleared* — the Challenger has assessed this against `strategy_rules.md` boundaries and economic constraints. Specific sections reviewed: §3 (human-in-loop), §13 (system boundaries, external dependency). This item does not engage any §13 boundary or strategic constraint — it is a governance housekeeping document for an existing production dependency. No grounds for challenge. Cleared.

**5.2 Product Owner Response:**
Challenger Clearance Statement accepted. Item advances. Displacement: BLG-GOV-18 slot in governance backlog. **Maintain ✅ Advance.**

**Outcome: ✅ Advance** — promoted to backlog as BLG-GOV-18.

---

### Debate: IDEA-cybersecurity-20260421-01 — Alpaca API Key Rotation Policy

**5.0 Required Case (Cybersecurity & Trust Lead / Product Owner):**
1. *Problem:* Alpaca API key is in production, stored in Render environment variables. No documented rotation policy exists — no specification of: rotation frequency, rotation procedure (how to rotate without service disruption), validation after rotation, or incident response if key is compromised.
2. *Strategy intent served:* Security hygiene for production system. Not a §13 item.
3. *If we don't:* An API key compromise (unlikely but possible) has no documented response. No scheduled rotation discipline.
4. *Displacement:* S effort, security backlog slot (BLG-SEC-05). Displaces a lower-priority security item or adds to the existing 3 active items.

**5.1 Challenger Counter-Argument:**
- Challenger position: **Park**
- Evidence: `strategy_rules.md §3` (human-in-the-loop). Alpaca key is stored in environment variables on Render (not in code). Risk of compromise is low — no shared access, no codebase exposure. Formal rotation policies are standard for systems with multiple operators. For a solo-developer system, "rotate if compromised, change annually if security hygiene warrants" is sufficient without a formal document.
- Reason: S effort is still effort. At current scale, the overhead of maintaining a rotation policy document is disproportionate to the actual security risk.
- Consequence: Creates a policy document that adds compliance overhead with minimal security gain over the existing implicit practice.

**5.2 Product Owner Response:**
The Challenger's argument applies correctly to formal compliance regimes. However, the purpose here is different: the rotation policy document exists so WHEN I forget the procedure (in 6 months), I don't have to research it from scratch. This is documentation-for-memory, not documentation-for-compliance. The "overhead" of maintaining it is near-zero — it's a one-page document updated only when the rotation procedure changes. S effort to create. Security events don't announce themselves, and an undocumented procedure is the worst time to improvise one.

Rebuttal: the Challenger's argument does not apply because the value is procedural memory, not compliance. **Maintain ✅ Advance.** Displacement: BLG-SEC-05 slot.

**Outcome: ✅ Advance** — promoted to backlog as BLG-SEC-05.

---

### Debate: IDEA-cybersecurity-20260421-02 — External API Credential Audit

**5.0 Required Case (Cybersecurity & Trust Lead / Product Owner):**
1. *Problem:* Multiple API credentials now in production: Alpaca (screener), Anthropic/Claude (AI journal), potentially Yahoo Finance (if key-authenticated). No inventory documents which credentials exist, where stored, when last rotated, and which systems depend on them.
2. *Strategy intent served:* Security hygiene baseline. Not a §13 item.
3. *If we don't:* Credential sprawl without oversight. A compromised credential may not be detected promptly if there's no inventory to cross-check.
4. *Displacement:* S effort, overlapping with IDEA-cybersecurity-20260421-01 scope. May be combined with key rotation policy.

**5.1 Challenger Counter-Argument:**
- Challenger position: **Park**
- Evidence: Scope overlap with IDEA-cybersecurity-20260421-01 (Alpaca key rotation policy). Both items are about credential management. If the rotation policy (IDEA-cybersecurity-20260421-01) is advancing, it should include a credential inventory section as part of its scope definition. A separate "credential audit" backlog item creates parallel governance artefacts for the same problem domain.
- Reason: Two overlapping credential management items in the backlog simultaneously risks: (a) duplicated effort, (b) inconsistent scope definitions. The Challenger recommends that the credential audit be rolled into the rotation policy scope rather than advancing as a separate item.
- Consequence: Advancing creates two items where one, well-scoped item is sufficient.

**5.2 Product Owner Response:**
The Challenger's overlap argument is well-grounded. IDEA-cybersecurity-20260421-01 (key rotation policy) is advancing. The credential audit scope CAN be incorporated into the rotation policy backlog item by broadening its scope to cover: (1) credential inventory, (2) rotation policy, (3) validation procedure. This is more efficient than two separate items.

**Accept Challenger: ❌ do not advance as separate item.** The scope of BLG-SEC-05 (from IDEA-cybersecurity-20260421-01) will be broadened to include a credential audit component. IDEA-cybersecurity-20260421-02 is parked pending BLG-SEC-05 delivery. Register update: Park with new rationale (scope to be subsumed into BLG-SEC-05).

**Outcome: 🅿 Park** — scope subsumed into BLG-SEC-05 (advancing from IDEA-cybersecurity-20260421-01); park until BLG-SEC-05 delivered.

---

### Debate: IDEA-finops-20260421-01 — Alpaca API Cost Monitoring

**5.0 Required Case (FinOps & Resource Architect / Product Owner):**
1. *Problem:* DS-01 screener engine runs daily (or on-demand) making real Alpaca API calls. Alpaca's free tier has limits. Without monitoring, approaching a tier limit is invisible until the screener fails. No alert exists for call volume thresholds.
2. *Strategy intent served:* Operational resilience. Screener engine availability is now a daily workflow dependency.
3. *If we don't:* The screener could silently degrade or fail if Alpaca API quota is exceeded with no advance warning.
4. *Displacement:* S effort. BLG-OPS backlog slot.

**5.1 Challenger Counter-Argument:**
- Challenger position: **Park**
- Evidence: DS-01 has been live for 10 days. Alpaca's free tier provides historical data access at no cost for typical usage patterns (bulk historical download + daily updates). The screener runs on-demand — not continuously. In 10 days of operation, no rate limit issues have surfaced.
- Reason: The concern is valid but premature. Monitoring is warranted when (a) usage patterns are established (currently unknown), or (b) when approaching a limit. 10 days is insufficient to understand call volume patterns. Adding monitoring now may over-engineer the solution before the problem is real.
- Consequence: Advancing adds an operations item for a risk that has not materialised and may not be material. BLG-OPS-13 already extends the performance baseline — the same work touchpoint could include API call volume monitoring if warranted.

**5.2 Product Owner Response:**
The Challenger's timing argument is strong. 10 days is insufficient to characterise usage patterns. The correct approach is: observe Alpaca API call volume for 30–60 days naturally through the Alpaca dashboard, then assess if monitoring tooling is warranted. This is the "only validate at system boundaries" principle — don't add monitoring infrastructure for a risk that hasn't materialised.

**Accept Challenger: 🅿 Park.** New rationale: Alpaca call volume patterns too early to characterise at 10 days; observe for 60 days and assess at the v3.3+ rebalance; park pending evidence of tier-limit approach.

**Outcome: 🅿 Park** — premature; observe usage patterns for 60 days before actioning.

---

### STEP 5 Outcomes Summary

| Idea ID | Title | Outcome |
|---------|-------|---------|
| IDEA-head-of-ux-20260321-02 | Design system document | ✅ Advance → BLG-FE-21 |
| IDEA-financial-reporting-20260321-02 | Net-of-costs performance tracking | ✅ Advance → BLG-FEAT-20 |
| IDEA-product-owner-20260421-01 | Screener morning routine UX | ✅ Advance → BLG-FE-22 |
| IDEA-pmo-lead-20260421-01 | External API dependency risk register | ✅ Advance → BLG-GOV-18 |
| IDEA-cybersecurity-20260421-01 | Alpaca API key rotation policy | ✅ Advance → BLG-SEC-05 |
| IDEA-cybersecurity-20260421-02 | External API credential audit | 🅿 Park (scope subsumed into BLG-SEC-05) |
| IDEA-finops-20260421-01 | Alpaca API cost monitoring | 🅿 Park (premature; 10 days insufficient) |

**Advancing items count: 5 (to backlog). Parked in STEP 5: 2.**

---

## STEP 6 — Scoring Matrix

*Authority: Facilitator*

*Scoring scale: 1 (low/poor) → 5 (high/excellent). WF Intensity: 1=high effort, 5=hours only.*
*SPS assigned by Strategy Rules & System Intent Owner. Effort band: S/M/L.*

| Item | Strat | Fin | Risk | WF | TTV | Rev | SPS | Effort |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|--------|
| BLG-FE-21: Design system doc | 3 | 1 | 2 | 5 | 4 | 5 | 1 | M |
| BLG-FEAT-20: Net-of-costs tracking | 3 | 4 | 2 | 3 | 2 | 3 | 2 | M |
| BLG-FE-22: Screener morning routine UX | 4 | 2 | 3 | 5 | 5 | 5 | 2 | S |
| BLG-GOV-18: External API risk register | 2 | 1 | 4 | 5 | 4 | 5 | 1 | S |
| BLG-SEC-05: Alpaca key rotation policy + credential audit | 2 | 1 | 4 | 5 | 4 | 5 | 1 | S |

**Notes:**
- BLG-FEAT-20 (net-of-costs): Financial impact 4/5 because it enables accurate R-multiple calculation for Arc 4 edge analysis; TTV 2/5 because value realised at Arc 4 delivery, not immediately.
- BLG-FE-22 (morning routine UX): TTV 5/5 because value is immediate (Arc 2 design context); WF 5/5 (S effort, pure spec work).
- All items SPS 1–2: no §13 boundary contact.

---

## STEP 7 — Workforce Economics

*Authority: FinOps & Resource Architect*

**FTE load per advancing item:**

| Item | Estimated FTE load | Primary skill | Duration |
|------|--------------------|---------------|----------|
| BLG-FE-21: Design system doc | 1–2 days | Frontend Spec / UX Documentation | 1 sprint |
| BLG-FEAT-20: Net-of-costs tracking | 2–3 days | Backend Engineering + Product | Defer to Arc 3/4 context |
| BLG-FE-22: Screener morning routine UX | 0.5–1 day | UX Spec / Product | Before v3.2 sprint planning |
| BLG-GOV-18: External API risk register | 0.5 day | PMO Lead | 1 sprint slot |
| BLG-SEC-05: Alpaca key rotation policy + credential audit | 0.5–1 day | Cybersecurity / Ops | 1 sprint slot |

**Total estimated:** ~5–8 FTE-days across all 5 items.

**Skill constraints:** None. All items are documentation/spec/governance tasks. No scarce engineering skills consumed.

**Opportunity cost:** These items are P2–P3 and will slot into v3.2/v3.3 behind primary Arc 2 features (PT-02 frontend, PT-03, PT-05). No conflict with Arc 2 delivery.

### 7.1 Skill-Silo Check

**Governance-heavy items:** BLG-GOV-18 (PMO Lead) = ~0.5 FTE-day governance
**Execution-heavy items:** BLG-FE-21, BLG-FEAT-20, BLG-FE-22 (engineering/design/product) = ~5.5 FTE-days; BLG-SEC-05 (security/ops) = ~0.75 FTE-day

**Governance load %:** ~0.5 / 8.0 ≈ 6% — below 20% floor.

**Sign-Off Capacity Floor check:** Governance load 6% is below 20% floor. FinOps & Resource Architect verifies: these items are all backlog additions, not active sprint deliverables; no spec approval or decision records are deferred without acknowledgement. All items documented with clear scope. Product Owner sign-off capacity confirmed adequate for this set.

**Result: No Skill-Silo Alert. Sign-Off Capacity: PASS (PO confirms adequate review capacity).**

---

## STEP 8 — Final Rebalance Decision

*Authority: Product Owner (within all constraints)*

### Per-Initiative Decisions

| Item | Decision | Notes |
|------|----------|-------|
| BLG-FE-21: Design system document | ➕ Add to backlog (P3) | BLG-FE-21; Owner: Frontend Specs & UX Documentation Owner |
| BLG-FEAT-20: Net-of-costs performance tracking | ➕ Add to backlog (P2) | BLG-FEAT-20; Owner: Financial Reporting & Records Owner; delivery: Arc 3/4 context |
| BLG-FE-22: Screener morning routine UX spec | ➕ Add to backlog (P2) | BLG-FE-22; Owner: Frontend Specs & UX Documentation Owner; deliver before v3.2 sprint planning |
| BLG-GOV-18: External API dependency risk register | ➕ Add to backlog (P3) | BLG-GOV-18; Owner: PMO Lead + Infrastructure & Operations Owner |
| BLG-SEC-05: Alpaca API key rotation policy + credential audit | ➕ Add to backlog (P2) | BLG-SEC-05; Owner: Cybersecurity & Trust Lead; scope: rotation policy + credential inventory |

**Roadmap initiative changes: None.** No initiatives added, replaced, deferred, or killed at the roadmap level. Now horizon remains empty (correctly reflecting post-v3.1 state). Arc 2 continuation in Next horizon confirmed as-is.

**Net-zero verification (STEP 9.0):**
- Roadmap additions: 0 (no new roadmap initiatives)
- Roadmap kills: 0
- Net: 0 — Net-zero satisfied (additions = kills = 0).

**Skill-Silo check result:** Governance load 6% — below floor but confirmed adequate by PO sign-off.

**Displacement confirmation:**
- BLG-FE-21, BLG-FE-22: Added as P3/P2 FE items; displace no existing items (BLG-FE-16 remains as-is).
- BLG-FEAT-20: Added as P2 FEAT; delivery deferred to Arc 3/4 context (no current sprint impact).
- BLG-GOV-18: Added as P3 GOV; no items displaced (BLG-GOV-11 remains as-is).
- BLG-SEC-05: Added as P2 SEC; no existing SEC items in active backlog.

### STEP 8.6 — Disagreement Guardrail

- More than 1 candidate in debate: 7 items
- Items parked/rejected during debate: 2 (IDEA-cybersecurity-20260421-02, IDEA-finops-20260421-01)
- **Guardrail criterion 1: PASS** — at least 1 candidate was parked.
- Challenger issued Type A counter-arguments for both parked items (cybersecurity-02 and finops-01).
- **Guardrail criterion 2: PASS** — substantive Type A counter-arguments issued.

**STEP 8.6: PASS — proceeding to STEP 8.5.**

---

## STEP 8.5 — Stateless Write Safety Gate

### 8.5.A Context Re-Anchoring

Discarding all debate prose. Re-anchoring to:
- STEP 8 decisions: 5 backlog additions (BLG-FE-21, BLG-FEAT-20, BLG-FE-22, BLG-GOV-18, BLG-SEC-05)
- No roadmap initiative changes
- Ideas register: 32 ideas need status updates (7 Advancing→terminal, 15 re-park, 10 reject)

### 8.5.B Stateless Verification — Write Plan

**Cycle: 2026-05-05__scheduled**
**Context refresh: Yes (STEP 8.5.A)**

| File | Action | Reason | Traceability |
|------|--------|--------|--------------|
| claude/cycles/2026-05-05__scheduled/run_manifest.md | Created (STEP 1.1) | Required before any other writes | STEP 1.1 |
| claude/cycles/2026-05-05__scheduled/cycle_record.md | Create | STEP 2–8 working content | All steps |
| claude/backlog/backlog.md | Modify (add 5 items) | Reflect STEP 8 Add decisions | STEP 8 decisions × 5 |
| claude/roadmap/decision_log.md | Append-only | Record STEP 8 decisions | DL-024 |
| claude/roadmap/current_roadmap.md | Modify (header update) | Last Updated + Last rebalance annotation | Lifecycle compliance |
| claude/roadmap/initiative_register.md | Modify (Last Updated) | No initiative changes; header currency | Lifecycle compliance |
| claude/ideas/ideas_register.md | Modify (32 row status updates) | STEP 4.2 document management | STEP 4.2 decisions |
| claude/scoring/scored_initiatives.md | Modify (add 5 items) | Effort bands for new backlog items | STEP 6 |
| claude/cycles/2026-05-05__scheduled/cycle_summary.md | Create | STEP 10 output | STEP 10 |
| claude/cycles/2026-05-05__scheduled/lessons_learnt.md | Create | STEP 11 output | STEP 11 |
| .claude_current_state.json | Modify | STEP 12.1 rebalance keys | STEP 12 |

**Register row status verification (LL-02-patch):**
All 7 advancing ideas will receive terminal status:
- BLG-FE-21, BLG-FEAT-20, BLG-FE-22, BLG-GOV-18 → `Promoted-Added`
- IDEA-cybersecurity-20260421-01 → `Promoted-Added` (as BLG-SEC-05)
- IDEA-cybersecurity-20260421-02 → `Parked-cycle-N` (accepted Challenger in STEP 5; re-parked with new rationale)
- IDEA-finops-20260421-01 → `Parked-cycle-N` (accepted Challenger in STEP 5; re-parked with new rationale)

Wait: IDEA-cybersecurity-20260421-02 and IDEA-finops-20260421-01 were classified as ✅ Advancing in STEP 4, then parked in STEP 5. Their register rows were set to `Advancing` in STEP 4.2. Per LL-02-patch, they need terminal status in STEP 9. They were not promoted (PO accepted Challenger), so they should be set to `Parked-cycle-N` (updated park count). ✅ Confirmed in write plan.

### 8.5.C Verification Rules Check

- All files within Section 5 write scope: ✅ Yes
- Every write traceable to STEP 8 decision or lifecycle compliance: ✅ Yes
- No formatting-only edits: ✅ Yes
- Decision log append-only: ✅ Yes (will verify pre/post count)
- Backlog edits reconciliation-only: ✅ Yes (no grooming; 5 additions per STEP 8)
- PoG documents: N/A (no hard gates)
- Hard gate "complete" markings: N/A
- Displacement candidate flags: N/A (no new initiative register changes)
- Effort bands: ✅ Yes (in STEP 6 scoring)

### 8.5.D Decision-to-Write Traceability

All 5 backlog additions: traceable to STEP 8 Add decisions.
All register row updates: traceable to STEP 4.2 document management decisions.
Header updates to roadmap and initiative_register: lifecycle compliance (Last Updated currency).
Appended scoring: traceable to STEP 6 effort band requirement.

**STEP 8.5 Write Plan: PASS — proceeding to STEP 9.**
