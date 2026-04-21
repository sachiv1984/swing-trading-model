**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-04-21__scheduled
**Last Updated:** 2026-04-21

---

# Cycle Record — Roadmap Rebalance 2026-04-21__scheduled

---

## STEP 2 — Re-Validation

**Authorities:** Product Owner + Strategy Rules & System Intent Owner

### Active Initiatives

**No active initiatives as of 2026-04-21.** v2.8 shipped 2026-04-20. The six-arc model defines the strategic roadmap. No initiative currently sits in the "Now" horizon consuming active workforce allocation.

The roadmap is structured around six named arcs (Arc 1–6), each with a purpose, defined end state, and sequencing rationale. This structure was established at the 2026-04-17__scheduled rebalance and is the current strategic anchor.

### Force Classification — Zero Active Initiatives

No items to classify 🔥/⚠/❌ — all prior arc items were committed to the backlog in the arc structure. No standing initiatives are consuming workforce allocation.

*Record: "No active initiatives requiring re-validation — all v2.8 items shipped; arc model stable."*

### Strategy Proximity Scores (STEP 2.1)

**No active initiatives to score.** CPS = N/A (no items in numerator or denominator).

| Item | SPS | Rationale |
|------|-----|-----------|
| (none) | — | No active initiatives |

**Cycle Proximity Score (CPS):** 0.0
**Prior cycle CPS:** 0.0 (cycle 2026-04-17__scheduled — also no active initiatives)
**Delta:** 0.0 — no drift
**Strategy Drift Alert:** None required (CPS = 0.0, delta = 0.0).

### Horizon Review (STEP 2.3)

**Now horizon:** Empty. All v2.8 shipped annotations. No uncommitted items.

**Next Phase — Horizon: Next (Arcs 1 & 2):**

| Feature | ID | Horizon placement | Review outcome |
|---------|----|-------------------|---------------|
| Sector & Industry Classification | DS-03 | Next — v2.9 | Correctly placed. Arc 1 first-sequence prerequisite. No movement. |
| Alpaca US Market Data Integration | DS-05 | Next — v2.9 | Correctly placed. Arc 1 infrastructure prerequisite. No movement. |
| Strategy-Rules Screener Engine | DS-01 | Next — v2.9 | Correctly placed. Core Arc 1 deliverable. No movement. |
| Screener Results Page | DS-02 | Next — v2.9 | Correctly placed. Depends on DS-01. No movement. |
| Alpaca News Panel | DS-06 | Next — v2.9 | Correctly placed. §13 review record (per IDEA-strategy-owner-20260421-02) proposed as prerequisite gate before implementation. No horizon movement. |
| Earnings Calendar Integration | DS-04 | Next — v2.9 | Correctly placed. Parallel with DS-02. No movement. |
| Watchlist Promotion Flow | DS-07 | Next — v2.9 | Correctly placed. Depends on DS-02. No movement. |
| Trade Plan Object | PT-01 | Next — v3.1 | Correctly placed. Arc 2 data model prerequisite. No movement. |
| Pre-Trade Research View | PT-02 | Next — v3.1 | Correctly placed. Depends on PT-01. No movement. |
| Prospective Heat at Entry | PT-03 | Next — v3.1 | Correctly placed. Frontend integration only. No movement. |
| Pre-Trade Entry Checklist | PT-05 | Next — v3.1 | Correctly placed. No movement. |
| Setup Quality Score | PT-04 | Next — v3.1 | Correctly placed. Gate: 20+ closed trades. No movement. |

**Later horizon (Arcs 3–6):** No movements recommended. Arc sequencing rationale remains valid. SI-01 (Pre-Entry Rule Validation Gate) and SI-03 (Red Flag Journal) retain their pull-forward candidacy note for Arc 3 review — no action needed at this rebalance.

**Horizon Review Outcome:** No movements recommended. The arc sequencing is correct. Arc 1 planning can proceed immediately now that v2.8 is closed.

---

## STEP 3 — Backlog Health

**Authority:** Head of Specs Team (process), Product Owner (planning ownership)

### Active Backlog Items

| ID | Title | Priority | Observation |
|----|-------|----------|-------------|
| BLG-TECH-05 | Prometheus metrics endpoint | P3 | Long-standing deferral. Correct at current single-user scale. |
| BLG-FE-15 | SystemStatus.js /ai prefix | P3 | v2.9 target. Small cosmetic fix, straightforward. |
| TEST-GAP-EPIC-04 | AI Journal test coverage | P3 | Before next sprint touching AI feature. Correct placement. |
| BLG-GOV-15 | execution_prompt STEP 5.1.B | P2 | v2.9 planning sprint. Critical process gap. BLG-GOV-14 also P2 (related). |
| BLG-GOV-08 | Engine prompt compression | P3 | **FINAL DEFERRAL** — retirement review at v2.9 planning. 5 consecutive deferrals. Product Owner must make a final decision at v2.9 release planning: implement, reduce scope, or retire. |
| BLG-GOV-14 | execution_prompt §3.2 patches | P2 | v2.9 planning sprint. Backed by CF-1/CF-2 from v2.8 lessons_learnt_closure. |
| BLG-GOV-11 | Cycle artefact inventory | P3 | v2.9. Deferred from v2.8. Still valid; no urgency increase. |
| BLG-FEAT-13 | Feature flag rollout | P3 | v2.9. Deferred from v2.8. Single-user scale; low urgency. |

**Observations:**
- **No obsolete items.** All 8 active backlog items remain strategically aligned.
- **No duplicates.** IDs are unique (BLG-GOV-13 dedup shipped v2.8).
- **Quick wins available:** BLG-FE-15 (S effort, ~0.5 day) is a near-trivial v2.9 candidate.
- **Technical debt accumulating:** BLG-GOV-08 (engine prompt compression) has reached 5 deferrals — the stale-notice flag correctly calls out that this needs a final decision at v2.9 planning.
- **Arc 1 prerequisite gaps visible:** The backlog has no Arc 1 specification items yet. The new idea window (IW-20260421-01) has generated the candidate specification ideas (Alpaca API contract, screener schema spec, screener API contract, mock harness, etc.) that will address this gap if advanced in STEP 5.

**Backlog health verdict:** Healthy, lean, and well-aligned. The critical gap is Arc 1 pre-work documentation that will be addressed by STEP 4/5 idea advancement.

---

## STEP 4 — Idea Review and Document Management

**Authority:** Facilitator (review), Product Owner (classification decisions)

### Gate-Condition Re-Check (STEP 4.0)

Four parked ideas have park rationales that reference specific shipped items or rejected ideas:

| Idea ID | Referenced Item | Status | Action |
|---------|----------------|--------|--------|
| IDEA-head-of-specs-20260321-02 | BLG-SPEC-T01 | Shipped v2.2 | **Gate cleared — mandatory re-evaluation** |
| IDEA-base44-frontend-20260321-01 | BLG-FE-02, BLG-FE-03 | Shipped v2.3, v2.4 | **Gate cleared — mandatory re-evaluation** |
| IDEA-frontend-ux-20260321-02 | BLG-FE-02, BLG-FE-03 | Shipped v2.3, v2.4 | **Gate cleared — mandatory re-evaluation** |
| IDEA-head-of-ux-20260321-02 | IDEA-head-of-ux-20260304-02 | Rejected (Design Tokens) | **Gate reference invalid — mandatory re-evaluation** |

All other parked ideas: park rationales are time-based or capacity-based — no BLG- item reference that has shipped.

### STEP 4.1 — Per-Idea Classification

**Total ideas for classification:** 60 (16 stale parked + 44 new from IW-20260421-01)

---

#### Stale Parked Ideas (16) — Mandatory Active PO Disposition

**IDEA-frontend-ux-20260304-02** (Accessibility Baseline, cycle-9)
- PO disposition: 🅿 **Park**
- Rationale: IDEA-frontend-ux-20260321-02 (React component inventory) — which was this idea's dependency gate — is now advancing in this cycle. If the component inventory lands in v2.9, this gate will clear in the next rebalance. Re-park with updated dependency reference. Cycle count: 9 → 10.

**IDEA-head-of-specs-20260321-02** (Machine-readable spec front-matter, gate-cleared)
- PO disposition: ✅ **Advance**
- Rationale: BLG-SPEC-T01 shipped v2.2; CI tooling mature through v2.8. Arc 1 introduces new spec files (screener schema, Alpaca contract) — consistent YAML front-matter on all canonical specs would enable header compliance checking in CI at scale.

**IDEA-strategy-owner-20260321-02** (§13 boundary review cadence)
- PO disposition: ✅ **Advance**
- Rationale: Arc 1 DS-06 (Alpaca News Panel) and IT-06 (Alpaca Paper Trading gate) both require §13 reviews. A formal cadence for §13 reviews (triggered at each major release) is now timely and addresses a real operational pattern rather than a hypothetical one.

**IDEA-challenger-20260321-01** (SPS≥4 mandatory §13 review gate)
- PO disposition: 🅿 **Park**
- Rationale: roadmap_prompt already handles SPS≥4 via STEP 5 debate with Challenger obligation. Adding a formal gate would be redundant process overhead. No new evidence of the gap in 5 cycles. Cycle count: 5 → 6.

**IDEA-challenger-20260321-02** (Complexity budget tracking)
- PO disposition: 🅿 **Park**
- Rationale: Arc 1 adds external API dependencies and new endpoints — the system is growing. However, no concrete metric or measurement approach has been identified. Still no implementation path. Revisit once Arc 1 ships and the system has a stable new endpoint surface area. Cycle count: 5 → 6.

**IDEA-ai-compliance-20260321-01** (Governed decision audit log)
- PO disposition: 🅿 **Park**
- Rationale: decision_log.md continues to provide a comprehensive narrative record. No evidence of decision-volume growth that would require a structured searchable format. Re-park. Cycle count: 5 → 6.

**IDEA-ai-compliance-20260321-02** (Model version contract)
- PO disposition: ✅ **Advance**
- Rationale: AI Journal Summarisation (EPIC-04) shipped v2.8. The system now has an AI-generating feature in production. Knowing which Claude model version produced which summary is now a real audit trail need, not just governance hygiene. The trigger event has occurred.

**IDEA-metrics-analytics-20260321-01** (Consecutive losing streak metric)
- PO disposition: ✅ **Advance**
- Rationale: Sufficient trade history has accumulated through multiple releases (v1.6.1 through v2.8). Metrics definitions spec is stable. This is a well-defined, low-risk metric that adds measurable risk-management value.

**IDEA-metrics-analytics-20260321-02** (ATR-normalised sizing retrospective)
- PO disposition: 🅿 **Park**
- Rationale: Requires a specific trade history dataset structure (ATR at entry, recommended size, actual size). Arc 2 (Pre-Trade Research & Planning) will introduce the Trade Plan object (PT-01) which captures entry-time ATR. This metric becomes more meaningful once PT-01 data exists. Park until Arc 2 is in progress. Cycle count: 5 → 6.

**IDEA-base44-frontend-20260321-01** (Keyboard shortcuts, gate-cleared)
- PO disposition: 🅿 **Park**
- Rationale: BLG-FE-02/03 gate cleared — the dependency has shipped. However, with Arc 1 as the next delivery theme, keyboard shortcuts are a workflow-optimisation item best addressed after the core screener flow is established. Re-park with Arc 1 timing rationale. Cycle count: 5 → 6.

**IDEA-data-model-owner-20260321-02** (Position tags normalisation)
- PO disposition: 🅿 **Park**
- Rationale: No tag-based filtering feature is planned in Arc 1 or Arc 2. Schema refactor cost not justified until a concrete feature requires it. Cycle count: 5 → 6.

**IDEA-financial-reporting-20260321-01** (Monthly P&L summary)
- PO disposition: ✅ **Advance**
- Rationale: Sufficient trade history has accumulated since the tax year report shipped v2.0. Monthly granularity provides meaningful patterns for in-year performance tracking. Low-effort (S) incremental extension of the existing P&L framework.

**IDEA-financial-reporting-20260321-02** (Net-of-costs performance tracking)
- PO disposition: 🅿 **Park**
- Rationale: Requires adding cost fields to the trade data model — a non-trivial schema change. Arc 2 trade plan object (PT-01) may create a natural entry point. Park until Arc 2 data model design is in progress. Cycle count: 5 → 6.

**IDEA-qa-lead-20260321-02** (Bug severity classification matrix)
- PO disposition: 🅿 **Park**
- Rationale: No bug classification inconsistency incidents in 5 cycles. QA turnaround has been consistently acceptable. Arc 1 introduces new complexity but also new test protocols (mock harness, scenario library from this cycle). Formal matrix is premature. Cycle count: 5 → 6.

**IDEA-frontend-ux-20260321-02** (React component inventory, gate-cleared)
- PO disposition: ✅ **Advance**
- Rationale: BLG-FE-02/03 shipped. Arc 1 will add significant new frontend components (screener results page DS-02, news panel DS-06, promotion flow DS-07). A component inventory now would serve as a living document from which Arc 1 components can be added systematically, reducing duplication and enabling consistent reuse.

**IDEA-head-of-ux-20260321-02** (Design system document, gate-cleared)
- PO disposition: 🅿 **Park**
- Rationale: IDEA-head-of-ux-20260304-02 (design tokens) was the dependency — it was rejected in v2.4 planning. The rationale for rejecting it still applies: single-user system with no design team. The implicit design system is workable at current scale. Re-park with standalone rationale (previous dependency reference removed). Cycle count: 5 → 6.

---

#### New Ideas from IW-20260421-01 (44) — Product Owner Classification

**Advancing (10):**

1. **IDEA-head-of-specs-20260421-02** (Screener results schema spec) — ✅ **Advance**. Arc 1 prerequisite. DS-01 cannot be implemented without a canonical spec for its output. What would you stop? BLG-GOV-11 (cycle artefact inventory, P3) deprioritised.

2. **IDEA-api-contracts-20260421-01** (Alpaca API integration contract) — ✅ **Advance**. DS-05 prerequisite. Required before any Alpaca API code is written. What would you stop? BLG-GOV-08 (engine prompt compression, P3) deferred further.

3. **IDEA-api-contracts-20260421-02** (Screener internal API contract) — ✅ **Advance**. Arc 1 API contract prerequisite. GET /screener/results contract needed before frontend/backend work splits. What would you stop? BLG-TECH-05 (Prometheus metrics, P3) deprioritised.

4. **IDEA-director-of-quality-20260421-01** (External API mock harness for CI) — ✅ **Advance**. Arc 1 CI prerequisite. Flaky screener tests against live APIs will block CI reliability. What would you stop? BLG-FEAT-13 (feature flag rollout, P3) deprioritised.

5. **IDEA-strategy-owner-20260421-02** (§13 review record for DS-06 Alpaca News Panel) — ✅ **Advance**. Required pre-implementation gate. DS-06 is labelled §13 COMPLIANT in the roadmap but has no formal review record. A named §13 review decision record is required before DS-06 begins. What would you stop? BLG-FE-09 (Frontend Performance Budget, P3) deprioritised.

6. **IDEA-ai-compliance-20260421-01** (AI Journal summary audit log) — ✅ **Advance**. AI Journal is live in production. An audit log of AI-generated content is an immediate operational hygiene need. What would you stop? TEST-GAP-EPIC-04 (AI test coverage, P3) deprioritised in v2.9 planning queue (note: still tracked; just lower priority slot).

7. **IDEA-infra-ops-20260421-01** (External API health check extension) — ✅ **Advance**. Arc 1 operational need. GET /health currently covers DB and market status; adding external API connectivity checks is a natural extension needed before Arc 1 is in production. What would you stop? BLG-OPS-11 not an existing item — displacement: BLG-FEAT-13 already displaced above; use BLG-GOV-11 (P3) as dual displacement. *(Note: two items advanced against BLG-GOV-11 displacement — both are S effort; combined effort is still below the displaced M effort.)*

8. **IDEA-challenger-20260421-02** (Alpaca API fallback governance spec) — ✅ **Advance**. DS-05 pre-work. Undefined fallback behaviour (silent Yahoo Finance fallback vs explicit error) is a data quality risk. The fallback must be specified in the Alpaca API contract (IDEA-api-contracts-20260421-01) but warrants a separate spec note. What would you stop? BLG-FE-15 (SystemStatus /ai prefix, P3) deprioritised.

9. **IDEA-qa-testing-20260421-01** (Screener test data library) — ✅ **Advance**. Arc 1 CI prerequisite. Deterministic test data is required for reliable screener engine tests. What would you stop? BLG-GOV-15 remains P2 and is unaffected — use BLG-FEAT-13 (already displaced) as the shared displacement.

10. **IDEA-frontend-ux-20260421-01** (Screener results page UX spec) — ✅ **Advance**. DS-02 prerequisite. Arc 1 frontend implementation cannot begin without a UX spec for the screener results page. What would you stop? BLG-FEAT-13 is already the primary displacement; use BLG-TECH-05 (P3, already displaced) as dual displacement.

**Parked (34):** All remaining 34 ideas classified 🅿 Park with the following rationales:

| Idea ID | Rationale |
|---------|-----------|
| IDEA-product-owner-20260421-01 | Screener morning routine UX: timing — defined after DS-01/DS-02 ship; park for next rebalance once Arc 1 UX spec is live |
| IDEA-product-owner-20260421-02 | Candidate quality retrospective: requires screener live + trade history with screener attribution; Arc 4/5 level; park |
| IDEA-head-of-specs-20260421-01 | External API integration spec template: Alpaca-specific contract advancing in this cycle; template level is premature; park until 2 integrations exist |
| IDEA-pmo-lead-20260421-01 | External API dependency risk register: premature before Alpaca is actually integrated; operational register after Arc 1 ships |
| IDEA-pmo-lead-20260421-02 | Arc velocity tracking: useful but no urgent gap; velocity_metrics.md is functional; park |
| IDEA-director-of-quality-20260421-02 | Screener accuracy test protocol: needs DS-01 screener engine built first; advance once DS-01 spec exists |
| IDEA-finops-20260421-01 | Alpaca API cost monitoring: premature before Alpaca integration is live; park post-Arc 1 |
| IDEA-finops-20260421-02 | Data pipeline cost baseline: same timing as above; park post-Arc 1 |
| IDEA-infra-ops-20260421-02 | Screener run scheduler decision record: decision needed but at v2.9 sprint planning, not roadmap rebalance |
| IDEA-challenger-20260421-01 | Screener result stale data risk: valid concern; addressed within DS-02 spec as a UX requirement (freshness indicator); no separate backlog item needed |
| IDEA-backend-engineering-20260421-01 | Screener result caching strategy: architectural decision at DS-01 implementation; park until screener engine design is in progress |
| IDEA-backend-engineering-20260421-02 | External API rate limit manager: good Arc 1 infrastructure item; however Alpaca API contract (advancing) already includes rate limit spec; implementation pattern is a backend decision at DS-05 time; park |
| IDEA-ai-compliance-20260421-02 | AI feature monitoring: AI Journal audit log (IDEA-ai-compliance-20260421-01) advancing; monitoring metrics naturally follow once audit log is live; park until audit log lands |
| IDEA-cybersecurity-20260421-01 | Alpaca API key rotation policy: premature until Alpaca key is actively in use; park for Arc 1 completion |
| IDEA-cybersecurity-20260421-02 | External API credential audit: same timing; park post-Arc 1 |
| IDEA-metrics-analytics-20260421-01 | Screener hit rate metric: requires screener live + multiple promotion-to-trade cycles; park |
| IDEA-metrics-analytics-20260421-02 | Regime distribution metric: requires screener live; park |
| IDEA-head-of-engineering-20260421-01 | Screener engine performance benchmark: establish at DS-01 sprint planning; not roadmap-level backlog item |
| IDEA-head-of-engineering-20260421-02 | Data pipeline integration test suite: overlaps with mock harness (IDEA-director-of-quality-20260421-01, advancing); park to avoid duplication |
| IDEA-base44-frontend-20260421-01 | Screener progressive loading: frontend implementation pattern; defined within DS-02 UX spec (advancing); not a separate backlog item |
| IDEA-base44-frontend-20260421-02 | Screener result refresh indicator: same — defined within DS-02 UX spec |
| IDEA-data-model-20260421-01 | Screener result history table: Arc 1 extension; storage concern; define at v2.9 sprint planning as DS-01 extension item |
| IDEA-data-model-20260421-02 | Ticker universe management data model: fundamental Arc 1 data model need, BUT this is properly defined within DS-01 screener engine spec (screener needs a universe definition); park — define as part of DS-01 spec work |
| IDEA-financial-reporting-20260421-01 | Screener-to-trade attribution: requires screener live + multiple attributed trades; Arc 4/5 level |
| IDEA-financial-reporting-20260421-02 | External API cost attribution: premature; park post-Arc 1 |
| IDEA-director-of-hr-20260421-01 | Arc 1 team readiness assessment: process overhead not warranted at solo-dev scale; ownership is implicit |
| IDEA-director-of-hr-20260421-02 | External API expertise register: small team; ownership clear through agent charters |
| IDEA-qa-testing-20260421-02 | Screener scenario library: specific test scenarios come after screener spec is written; park until DS-01 spec exists |
| IDEA-qa-lead-20260421-01 | External API integration QA protocol: mock harness (advancing) addresses the core need; formal protocol overhead not warranted |
| IDEA-qa-lead-20260421-02 | Screener QA sign-off criteria: defined at sprint planning with the DoQ; not a roadmap backlog item |
| IDEA-frontend-ux-20260421-02 | Watchlist promotion UX spec: DS-07 detail defined within DS-02 UX spec (advancing); not a separate item |
| IDEA-head-of-ux-20260421-01 | Arc 1 daily workflow journey map: UX research; useful but not blocking Arc 1 sprint; park |
| IDEA-head-of-ux-20260421-02 | Screener empty states design: defined within DS-02 UX spec (advancing); not a separate item |
| IDEA-strategy-owner-20260421-01 | Screener parameter audit trail: good idea; addressed within screener schema spec (advancing) as a logging requirement; not a separate backlog item |

### STEP 4.2 — Document Management (Register Row Updates)

To apply after STEP 5:

**Stale ideas — park updates (cycle count increment):**
- IDEA-frontend-ux-20260304-02: Parked-cycle-9 → Parked-cycle-10 (Park Count: 10)
- IDEA-challenger-20260321-01: Parked-cycle-5 → Parked-cycle-6
- IDEA-challenger-20260321-02: Parked-cycle-5 → Parked-cycle-6
- IDEA-ai-compliance-20260321-01: Parked-cycle-5 → Parked-cycle-6
- IDEA-metrics-analytics-20260321-02: Parked-cycle-5 → Parked-cycle-6
- IDEA-base44-frontend-20260321-01: Parked-cycle-5 → Parked-cycle-6
- IDEA-data-model-owner-20260321-02: Parked-cycle-5 → Parked-cycle-6
- IDEA-financial-reporting-20260321-02: Parked-cycle-5 → Parked-cycle-6
- IDEA-qa-lead-20260321-02: Parked-cycle-5 → Parked-cycle-6
- IDEA-head-of-ux-20260321-02: Parked-cycle-5 → Parked-cycle-6 (park rationale updated: removed reference to rejected IDEA-head-of-ux-20260304-02; new rationale: "single-user system with no design team; implicit design system is workable at current scale; revisit when Arc 1 frontend work reveals design inconsistencies")

**Advancing (from stale pool):**
- IDEA-head-of-specs-20260321-02: → Advancing
- IDEA-strategy-owner-20260321-02: → Advancing
- IDEA-ai-compliance-20260321-02: → Advancing
- IDEA-metrics-analytics-20260321-01: → Advancing
- IDEA-financial-reporting-20260321-01: → Advancing
- IDEA-frontend-ux-20260321-02: → Advancing

**Advancing (from IW-20260421-01 new ideas):**
- IDEA-head-of-specs-20260421-02: → Advancing
- IDEA-api-contracts-20260421-01: → Advancing
- IDEA-api-contracts-20260421-02: → Advancing
- IDEA-director-of-quality-20260421-01: → Advancing
- IDEA-strategy-owner-20260421-02: → Advancing
- IDEA-ai-compliance-20260421-01: → Advancing
- IDEA-infra-ops-20260421-01: → Advancing
- IDEA-challenger-20260421-02: → Advancing
- IDEA-qa-testing-20260421-01: → Advancing
- IDEA-frontend-ux-20260421-01: → Advancing

**New ideas — parked (34):** All 34 parked ideas receive Status: Parked-cycle-1 in the register.

### STEP 4.3 — Idea Participation Check

Window summary IW-20260421-01: 22/22 agents submitted (Facilitator excluded by charter). No agent below minimum. No innovation debt.

### STEP 4.4 — Write Summary

**Idea Intake Summary — 2026-04-21__scheduled**

Window: IW-20260421-01
Total ideas loaded: 60 (16 stale parked + 44 new)
Advancing to STEP 5: 16
Parked: 44 (10 stale re-parked + 34 new parked)
Rejected: 0 this cycle
Stale ideas surfaced (≥3 cycles parked): 16
Stale ideas closed this cycle: 0

**STEP 5 Debate Queue**

| IDEA ID | Title | Source |
|---------|-------|--------|
| IDEA-head-of-specs-20260321-02 | Machine-readable spec front-matter standard | stale (gate-cleared) |
| IDEA-strategy-owner-20260321-02 | §13 boundary review cadence | stale |
| IDEA-ai-compliance-20260321-02 | Model version contract | stale |
| IDEA-metrics-analytics-20260321-01 | Consecutive losing streak metric | stale |
| IDEA-financial-reporting-20260321-01 | Monthly P&L summary report | stale |
| IDEA-frontend-ux-20260321-02 | React component inventory | stale (gate-cleared) |
| IDEA-head-of-specs-20260421-02 | Screener results schema spec | new |
| IDEA-api-contracts-20260421-01 | Alpaca API integration contract | new |
| IDEA-api-contracts-20260421-02 | Screener internal API contract | new |
| IDEA-director-of-quality-20260421-01 | External API mock harness for CI | new |
| IDEA-strategy-owner-20260421-02 | §13 review record for DS-06 | new |
| IDEA-ai-compliance-20260421-01 | AI Journal summary audit log | new |
| IDEA-infra-ops-20260421-01 | External API health check extension | new |
| IDEA-challenger-20260421-02 | Alpaca API fallback governance spec | new |
| IDEA-qa-testing-20260421-01 | Screener test data library | new |
| IDEA-frontend-ux-20260421-01 | Screener results page UX spec | new |

**Debate queue count: 16. Advancing to STEP 5 count: 16. Match confirmed ✅**

---

## STEP 5 — Structured Debate (Zero-Sum)

**Authorities:** Product Owner (chair) + Challenger (non-decision challenge)

**STEP 5 preflight:**
- Debate queue verified: 16 items, all accounted for below.
- No PoG validity checks required (no candidates carry prior hard gates from this queue).
- Score-5 presence check: No candidate has been assigned SPS=5 (no active initiatives; new idea SPS will be assigned in STEP 6).

**Strategy constraints restated (top 2 most likely to block):**
1. §13: The system must not be an automated trading bot or ML-based prediction system. Screening, alerting, and analytics must remain deterministic and human-confirmed.
2. Zero-sum: Every roadmap-level Add requires a Kill. Backlog-level adds require naming a displaced lower-priority item.

**STEP 5.0 — Pre-Debate Gate Checks**

A) PoG validity: No prior-cycle PoG documents covering any candidate in this queue. Not applicable.
B) Score-5 presence: No advancing candidate involves §13 boundary engagement. No Score-5 items.

---

**Debate 1: IDEA-head-of-specs-20260321-02** — Machine-readable spec front-matter standard

**5.0 Required Case:**
- Problem: Spec files have inconsistent or absent YAML front-matter; header compliance checking in CI is manual today.
- Strategy alignment: §2 deterministic system principles; canonical specs are the quality anchor for all implementation.
- If we don't do it: Growing spec library (Arc 1 will add multiple new spec files) will have inconsistent headers; CI cannot automate compliance checks; audit overhead increases.
- Displacement: BLG-SPEC-T01 already shipped (canonical source). No active initiative displaced. Backlog-level: BLG-GOV-11 (P3) deprioritised.

**5.1 Challenger Counter-Argument:**
- Challenger position: 🅿 Park
- Evidence: strategy_rules.md §2 (system boundaries) — this is a meta-governance item, not a product feature. The system boundary is the trading intelligence function, not spec tooling automation.
- Reason: CI-based header checks are governance tooling overhead. The current manual process (prompt-level compliance checks at preflight) has functioned adequately for 13 cycles without a CI gate failure attributable to missing front-matter. Adding CI-checked YAML front-matter is process investment that does not reduce strategy risk or improve user outcomes.
- Consequence: If we proceed, we invest M effort in tooling that automates a check that has not failed — opportunity cost vs Arc 1 spec work.

**5.2 Product Owner Response:**
- Response: Rebut — proceed ✅ Advance.
- Reasoning: The Challenger correctly notes this is governance tooling, not user-facing value. However, the specific trigger is Arc 1 starting now: DS-01 screener spec, DS-05 Alpaca contract, DS-06 §13 review record, and the screener schema spec (all advancing in this cycle) will each be new Class 2 canonical documents. If front-matter is not standardised before they are authored, they will join the existing inconsistent corpus. The cost of retrofitting is proportional to the number of docs added. S effort spec-standard document now prevents M effort retrofit after Arc 1 ships 7 new spec files.
- **Outcome: ✅ Advance**

---

**Debate 2: IDEA-strategy-owner-20260321-02** — §13 boundary review cadence

**5.0 Required Case:**
- Problem: §13 reviews happen ad-hoc (triggered by individual items). No formal cadence exists.
- Strategy alignment: strategy_rules.md §13 — the boundary definitions require ongoing validation as the system scope evolves.
- If we don't do it: §13 reviews occur only when a specific item triggers concern; gradual boundary erosion through individually small decisions may go undetected.
- Displacement: BLG-FE-09 (Frontend Performance Budget, P3) deprioritised.

**5.1 Challenger Counter-Argument:**
- Challenger position: 🅿 Park
- Evidence: strategy_rules.md §13 — boundaries have remained stable across 13 cycles without a cadenced review. The roadmap_prompt STEP 2.1 already assigns SPS scores at every rebalance cycle, and any SPS=4/5 item triggers Challenger §13 review in STEP 5.
- Reason: A formal cadence for §13 reviews adds governance overhead to a process that already has three organic trigger points: (1) every advancing item is SPS-scored, (2) Score-4 items require specific §13 counter-arguments, (3) Score-5 items require Strategy Owner presence with veto authority. The existing mechanism has prevented §13 violations. A formal cadence adds ceremony without adding protection.
- Consequence: If we proceed, we create a review process for a boundary that has not been challenged — governance activity for its own sake.

**5.2 Product Owner Response:**
- Response: Accept downgrade — 🅿 **Park**
- Reasoning: The Challenger's argument is persuasive. The existing SPS scoring mechanism does provide §13 visibility at every rebalance. The trigger for advancing this idea was DS-06 Alpaca News requiring a §13 review — but that is already addressed by IDEA-strategy-owner-20260421-02 (§13 review record for DS-06, advancing separately). A cadenced review process on top of the existing SPS mechanism is redundant. Park with rationale: SPS mechanism provides sufficient §13 visibility; specific DS-06 review addressed by IDEA-strategy-owner-20260421-02 advancing separately.
- **Outcome: 🅿 Park** (update register: Parked-cycle-6; rationale updated)

---

**Debate 3: IDEA-ai-compliance-20260321-02** — Model version contract

**5.0 Required Case:**
- Problem: AI Journal (EPIC-04, v2.8) is now live; the Claude model version used for summarisation is not recorded against each summary run.
- Strategy alignment: strategy_rules.md §3 human-in-the-loop model; AI Journal is display-only with human review — but the AI-generated content's provenance should be auditable.
- If we don't do it: If model behaviour changes (e.g. model upgrade), there is no way to identify which summaries were generated under which capability level.
- Displacement: BLG-FEAT-13 (feature flag rollout, P3) deprioritised.

**5.1 Challenger Counter-Argument:**
- Challenger position: 🅿 Park
- Evidence: strategy_rules.md §3 — AI Journal summaries are display-only with explicit human disclaimer. The model version is already recorded in the application logs and the Anthropic API response includes model metadata.
- Reason: The model version contract is solved at the infrastructure level (logs) rather than requiring a new backlog item. The Anthropic API response already contains model version metadata; if this is logged, no additional artefact is needed.
- Consequence: If we proceed, we create a document whose content is already available from existing log infrastructure.

**5.2 Product Owner Response:**
- Response: Rebut — proceed ✅ Advance.
- Reasoning: The Challenger assumes the model version metadata is being logged. The EPIC-04 implementation (ST-07/08) did not include an explicit model version audit log requirement. Without a specific logging spec, the version may be present in application logs but not queryable or durable in a way that supports audit. The backlog item (IDEA-ai-compliance-20260421-01, also advancing) will define this explicitly. IDEA-ai-compliance-20260321-02 is the specification document; IDEA-ai-compliance-20260421-01 is the audit log implementation. Both are needed.
- **Outcome: ✅ Advance**

---

**Debate 4: IDEA-metrics-analytics-20260321-01** — Consecutive losing streak metric

**5.0 Required Case:**
- Problem: No current metric tracks the longest consecutive losing streak.
- Strategy alignment: strategy_rules.md §2 (defend profits, manage risk asymmetrically) — tracking losing streaks is a direct risk management discipline metric.
- If we don't do it: Behavioural drift into extended losing streaks is not surfaced as a risk signal.
- Displacement: BLG-GOV-08 already deprioritised by other advancing items; use BLG-DATA-01 (Positions Table Data Dictionary, P2) deprioritised in v2.9 planning queue.

**5.1 Challenger Counter-Argument:**
- Challenger position: 🅿 Park
- Evidence: strategy_rules.md §2 item 3 — "give losing trades time to resolve." Surfacing consecutive losing streak as a prominent metric may create psychological pressure to exit positions during grace period, contradicting §2 intent.
- Reason: A consecutive losing streak metric is psychologically loaded. Users who see "5 consecutive losses" may feel compelled to exit open positions prematurely, violating the strategy's explicit "give losing trades time" principle. The metric conflates outcome (loss) with process compliance (whether the strategy was followed). The existing compliance score and grace period indicator already address process compliance.
- Consequence: If we proceed, we may add a metric that creates pressure for the opposite of the intended strategy behaviour.

**5.2 Product Owner Response:**
- Response: Rebut — proceed ✅ Advance.
- Reasoning: The Challenger raises a valid psychological risk. However, this risk is mitigated by: (1) the metric being historical (closed trades only, not open positions), (2) it being displayed in the analytics/dashboard context alongside expectancy and win rate metrics — not as an alert or active prompt. A historical losing streak count is informational context for strategy review, not a trigger for position management. The scope constraint must be documented: historical closed-trade data only; not surfaced in active position views or as an alert. This constraint addresses the §2 concern.
- **Outcome: ✅ Advance** (scope constraint: historical closed-trade data only; not surfaced in active position views or alert flows)

---

**Debate 5: IDEA-financial-reporting-20260321-01** — Monthly P&L summary report

**5.0 Required Case:**
- Problem: Only annual (tax-year) P&L is available; no monthly granularity.
- Strategy alignment: strategy_rules.md §2 — strategy review at appropriate granularity is part of compounding edge.
- If we don't do it: In-year performance patterns are only visible through the analytics page; no structured monthly summary exists.
- Displacement: BLG-GOV-11 (cycle artefact inventory, P3) deprioritised.

**5.1 Challenger:**
- Cleared — *"Cleared — reviewed strategy_rules.md §13 exclusions (not engaged), §3 human-in-loop model (display-only financial data, no automated action), and §2 strategy intent (supporting periodic review is within intent). This is a low-SPS additive analytics item with no boundary proximity. No grounds for challenge."*

**5.2 Product Owner:** ✅ Advance confirmed.

---

**Debate 6: IDEA-frontend-ux-20260321-02** — React component inventory

**5.0 Required Case:**
- Problem: No catalogue of UI components exists; Arc 1 will add significant new components.
- Strategy alignment: §2 system boundary (supporting user decision-making through consistent UI) — inconsistent components degrade the quality of decision-support surfaces.
- If we don't do it: Arc 1 frontend work risks duplicating existing components; design inconsistency compounds.
- Displacement: BLG-FE-15 (SystemStatus /ai prefix, P3) deprioritised.

**5.1 Challenger:**
- Cleared — *"Cleared — reviewed strategy_rules.md §13 exclusions (not engaged), §3 (no automated action), and component-count proxy for complexity (§13 does not restrict frontend architecture). This is frontend documentation; no boundary proximity. No grounds for challenge."*

**5.2 Product Owner:** ✅ Advance confirmed.

---

**Debate 7: IDEA-head-of-specs-20260421-02** — Screener results schema spec

**5.0 Required Case:**
- Problem: No canonical spec exists for screener output data structure before DS-01 implementation begins.
- Strategy alignment: strategy_rules.md §11 parameters define the filters; the schema spec documents how §11 parameters translate to screener output fields.
- If we don't do it: DS-01 implementation risks schema inconsistency between backend output and frontend consumption; API contracts cannot be written.
- Displacement: BLG-GOV-11 (P3) deprioritised. (dual displacement with IDEA-financial-reporting-20260321-01)

**5.1 Challenger:**
- Cleared — *"Cleared — reviewed strategy_rules.md §13 (screener output is deterministic rule-based filtering, not prediction — §13 COMPLIANT per roadmap annotation), §11 parameter alignment (the spec must be anchored to §11 — noted in scope). No boundary concerns. Advance."*

**5.2 Product Owner:** ✅ Advance confirmed. Scope constraint: spec must explicitly reference strategy_rules.md §11 as the parameter source.

---

**Debate 8: IDEA-api-contracts-20260421-01** — Alpaca API integration contract

**5.0 Required Case:**
- Problem: DS-05 Alpaca integration has no API contract document.
- Strategy alignment: strategy_rules.md §2 — data quality is foundational to decision-support integrity.
- If we don't do it: DS-05 implementation begins without a formal spec; API behaviour assumptions are undocumented; fallback strategy is undefined.
- Displacement: BLG-GOV-08 (engine prompt compression, P3) further deferred.

**5.1 Challenger:**
- Cleared — *"Cleared — reviewed strategy_rules.md §13 (Alpaca is a data source, not execution integration; broker API integration is excluded but data integration is within scope), §3 (no automated order placement), and §2 (data quality). Alpaca data integration is fully within §13 bounds for price/ATR/signal data. COMPLIANT. No grounds for challenge."*

**5.2 Product Owner:** ✅ Advance confirmed.

---

**Debate 9: IDEA-api-contracts-20260421-02** — Screener internal API contract

**5.0 Required Case:**
- Problem: Screener API endpoints (GET /screener/results, POST /screener/run) have no formal contract before implementation.
- Strategy alignment: Strategy rules §2 — canonical API contracts are the quality anchor.
- If we don't do it: Frontend and backend work on DS-02 and DS-01 respectively proceed without shared interface spec; risks integration friction.
- Displacement: BLG-TECH-05 (Prometheus metrics, P3) deprioritised.

**5.1 Challenger:**
- Cleared — *"Cleared — reviewed strategy_rules.md §13 (internal API; no external boundary engagement), §3 (screener results are decision support, not automated action). Standard API contract documentation. No boundary concerns. Advance."*

**5.2 Product Owner:** ✅ Advance confirmed.

---

**Debate 10: IDEA-director-of-quality-20260421-01** — External API mock harness for CI

**5.0 Required Case:**
- Problem: CI tests that depend on live Alpaca/Yahoo Finance APIs are flaky.
- Strategy alignment: §2 system reliability — a deterministic, trustworthy system requires deterministic CI.
- If we don't do it: Arc 1 CI reliability degrades; false CI failures from API downtime erode confidence in the CI gate.
- Displacement: BLG-FEAT-13 (feature flag rollout, P3) deprioritised.

**5.1 Challenger:**
- Cleared — *"Cleared — reviewed strategy_rules.md §13 (test infrastructure; no boundary engagement), §3 (mocking external APIs in CI is standard practice, no automated trading concern), §2 (directly supports reliability). No grounds for challenge. Advance."*

**5.2 Product Owner:** ✅ Advance confirmed.

---

**Debate 11: IDEA-strategy-owner-20260421-02** — §13 review record for DS-06 Alpaca News Panel

**5.0 Required Case:**
- Problem: DS-06 is labelled §13 COMPLIANT in the roadmap but has no formal review decision record.
- Strategy alignment: strategy_rules.md §13 — any item touching information display that could be construed as advisory requires explicit §13 sign-off.
- If we don't do it: DS-06 ships without a Strategy Rules owner sign-off record; auditable governance gap.
- Displacement: BLG-FE-09 (Frontend Performance Budget, P3) deprioritised.

**5.1 Challenger (Score-4 — boundary-adjacent):**
- Note: This idea concerns the §13 boundary itself. Assigning SPS = 4 — boundary-adjacent (DS-06 displays external news context which could be interpreted as advisory signal).
- Counter-argument: 🅿 Park
- Evidence: strategy_rules.md §13 — "Not an ML-based prediction system." Alpaca news is display-only (count + headlines), explicitly scoped as "no sentiment scoring" in the roadmap.
- Reason (§13-boundary specific): The Challenger's concern is not that DS-06 violates §13, but that creating a formal §13 review record before DS-06 even has a spec creates a governance artefact anchored to an unscoped item. The review record would need to be re-issued once DS-06 is fully specified. A review-before-spec risks being stale immediately.
- Consequence: If we advance now, the §13 review record is written against a roadmap description, not a finished spec. Any DS-06 spec change would require re-issuance.

**5.2 Product Owner Response:**
- Response: Rebut — ✅ Advance.
- Reasoning: The Challenger correctly identifies that the review record should be anchored to a spec. However, the review record's purpose here is to confirm the *principle* (display-only headlines, no sentiment scoring, no ML) rather than the specific implementation detail. The review record creates a documented baseline of what §13-compliance requires for DS-06. If the spec later diverges from the display-only constraint, the review record is the reference that triggers a re-review. Writing it now is a governance forcing function — it prevents scope creep into sentiment scoring during implementation. Scope constraint: the §13 review record must explicitly state that DS-06 compliance is conditioned on display-only headlines with no sentiment scoring or automated advisory generation.
- **Outcome: ✅ Advance** (SPS = 4; scope constraint noted; Strategy Rules & System Intent Owner must sign off)

---

**Debate 12: IDEA-ai-compliance-20260421-01** — AI Journal summary audit log

**5.0 Required Case:**
- Problem: AI Journal is live in production; no persistent audit record of which summaries were generated, for which trades, at what time, by which model version.
- Strategy alignment: strategy_rules.md §3 human-in-the-loop — AI-generated content with human review requires an audit trail.
- If we don't do it: AI-generated content in production with no provenance record; compliance gap if the provenance of any summary is questioned.
- Displacement: TEST-GAP-EPIC-04 (AI test coverage, P3) deprioritised in v2.9 planning queue.

**5.1 Challenger:**
- Cleared — *"Cleared — reviewed strategy_rules.md §3 (human-in-loop; audit log directly supports §3 compliance by making human review of AI content auditable), §13 exclusions (AI Journal is display-only decision support; audit log is infrastructure, not a new capability). This idea directly strengthens §3 compliance. No grounds for challenge. Advance."*

**5.2 Product Owner:** ✅ Advance confirmed.

---

**Debate 13: IDEA-infra-ops-20260421-01** — External API health check extension

**5.0 Required Case:**
- Problem: GET /health currently covers only internal services; Arc 1 introduces external API dependencies.
- Strategy alignment: §2 — operational reliability requires monitoring external dependencies.
- If we don't do it: External API failures are invisible until screener results fail; no proactive operational alerting.
- Displacement: BLG-GOV-11 (P3) dual displacement (shared with screener schema spec).

**5.1 Challenger:**
- Cleared — *"Cleared — reviewed strategy_rules.md §13 (health check infrastructure; no boundary engagement), §3 (no automated action; health status is display-only monitoring). Advance."*

**5.2 Product Owner:** ✅ Advance confirmed.

---

**Debate 14: IDEA-challenger-20260421-02** — Alpaca API fallback governance spec

**5.0 Required Case:**
- Problem: Undefined fallback (silent Yahoo Finance vs explicit error) is a data quality risk for screener results.
- Strategy alignment: §2 — deterministic, reliable system requires documented and predictable failure modes.
- If we don't do it: DS-05 ships with undefined fallback; screener could silently return different-quality data depending on API availability.
- Displacement: BLG-FE-15 (SystemStatus /ai prefix, P3) deprioritised.

**5.1 Challenger:**
- Note: This idea was submitted by the Challenger — self-assessment required. Challenger issues Type A counter-argument for completeness.
- Counter-argument: 🅿 Park
- Evidence: strategy_rules.md §2 — "data quality is foundational." However, the Alpaca API integration contract (IDEA-api-contracts-20260421-01, advancing) is the correct home for fallback strategy specification. A separate backlog item for fallback governance creates duplication.
- Reason: The fallback specification is a section of the Alpaca API contract, not a standalone backlog item. Advancing both creates two backlog items with overlapping scope.
- Consequence: If we advance, we create a duplicate spec item that will likely be merged into the contract anyway.

**5.2 Product Owner Response:**
- Response: Accept — 🅿 **Park**
- Reasoning: The Challenger's self-assessment is correct. Fallback governance is explicitly in scope for the Alpaca API integration contract (IDEA-api-contracts-20260421-01). Advancing a separate item creates duplication. Park with rationale: scope covered by IDEA-api-contracts-20260421-01 (Alpaca API integration contract); fallback specification is a required section of that contract.
- **Outcome: 🅿 Park**

---

**Debate 15: IDEA-qa-testing-20260421-01** — Screener test data library

**5.0 Required Case:**
- Problem: No synthetic ticker test data library exists; screener engine tests would require live market data without it.
- Strategy alignment: §2 deterministic system — CI test determinism requires deterministic test data.
- If we don't do it: Screener CI tests are either live-API-dependent (flaky) or have no test coverage.
- Displacement: BLG-FEAT-13 (P3) deprioritised (shared with external API mock harness).

**5.1 Challenger:**
- Cleared — *"Cleared — reviewed strategy_rules.md §13 (test infrastructure; no boundary engagement), §3 (deterministic test data supports deterministic system principle). The mock harness (IDEA-director-of-quality-20260421-01) and test data library are complementary items — the harness mocks the API, the library provides the test data fed through it. No overlap concern. Advance."*

**5.2 Product Owner:** ✅ Advance confirmed.

---

**Debate 16: IDEA-frontend-ux-20260421-01** — Screener results page UX spec

**5.0 Required Case:**
- Problem: DS-02 (Screener Results Page) has no UX spec; frontend work cannot begin without one.
- Strategy alignment: §2 — decision-support quality depends on how information is presented.
- If we don't do it: DS-02 frontend implementation begins without a formal UX spec; design decisions are made ad-hoc during implementation; inconsistencies arise.
- Displacement: BLG-TECH-05 (P3) deprioritised (shared with screener API contract).

**5.1 Challenger:**
- Cleared — *"Cleared — reviewed strategy_rules.md §13 (UX specification for a screener display page; no boundary engagement), §3 (display-only decision support; no automated action). Standard UX spec requirement. Advance."*

**5.2 Product Owner:** ✅ Advance confirmed.

---

### STEP 8.6 — Disagreement Guardrail Check

- Total candidates evaluated: 16
- Parked during debate: 2 (IDEA-strategy-owner-20260321-02 PO accepted Challenger; IDEA-challenger-20260421-02 PO accepted self-assessment)
- Challenger issued Type A counter-arguments for: IDEA-head-of-specs-20260321-02 (advanced), IDEA-metrics-analytics-20260321-01 (advanced), IDEA-strategy-owner-20260421-02 (advanced), IDEA-challenger-20260421-02 (parked)
- Guardrail check: More than one candidate evaluated AND at least one candidate was parked ✅

**Guardrail: PASSED.** No pivot loop required.

---

## STEP 6 — Scoring Matrix

**Authority:** Facilitator

Note: Candidates that were parked (IDEA-strategy-owner-20260321-02, IDEA-challenger-20260421-02) are not scored.

| Idea ID | Strategic Alignment | Financial Impact | Risk Reduction | Workforce Intensity | Time to Value | Reversibility | SPS | Effort Band |
|---------|--------------------|--------------------|----------------|--------------------|--------------|-----------|----|------------|
| IDEA-head-of-specs-20260321-02 | 4 | 2 | 3 | 2 | 4 | 5 | 2 | S |
| IDEA-ai-compliance-20260321-02 | 3 | 2 | 4 | 2 | 4 | 5 | 2 | S |
| IDEA-metrics-analytics-20260321-01 | 4 | 3 | 4 | 2 | 4 | 5 | 2 | S |
| IDEA-financial-reporting-20260321-01 | 3 | 3 | 2 | 2 | 4 | 5 | 1 | S |
| IDEA-frontend-ux-20260321-02 | 3 | 2 | 3 | 3 | 3 | 4 | 1 | M |
| IDEA-head-of-specs-20260421-02 | 5 | 4 | 5 | 1 | 5 | 5 | 2 | S |
| IDEA-api-contracts-20260421-01 | 5 | 4 | 5 | 1 | 5 | 5 | 2 | S |
| IDEA-api-contracts-20260421-02 | 5 | 4 | 5 | 1 | 5 | 5 | 1 | S |
| IDEA-director-of-quality-20260421-01 | 4 | 3 | 5 | 3 | 4 | 5 | 1 | M |
| IDEA-strategy-owner-20260421-02 | 5 | 3 | 5 | 1 | 5 | 5 | 4 | S |
| IDEA-ai-compliance-20260421-01 | 4 | 2 | 5 | 2 | 5 | 5 | 2 | S |
| IDEA-infra-ops-20260421-01 | 4 | 3 | 5 | 2 | 4 | 5 | 1 | S |
| IDEA-qa-testing-20260421-01 | 4 | 3 | 5 | 3 | 4 | 5 | 1 | M |
| IDEA-frontend-ux-20260421-01 | 5 | 4 | 5 | 2 | 5 | 5 | 1 | M |

Note on IDEA-strategy-owner-20260421-02 (SPS=4): Strategy Rules & System Intent Owner is active for this run and confirmed advance with the scope constraint: §13 review record conditioned on display-only headlines with no sentiment scoring.

---

## STEP 7 — Workforce Economics Gate

**Authority:** FinOps & Resource Architect

### Workforce Load Estimate

| Item | Effort | Skill domain |
|------|--------|-------------|
| IDEA-head-of-specs-20260321-02 | S (~0.5 day) | Governance — Head of Specs |
| IDEA-ai-compliance-20260321-02 | S (~0.5 day) | Governance — AI Compliance |
| IDEA-metrics-analytics-20260321-01 | S (~0.5 day) | Backend + Metrics |
| IDEA-financial-reporting-20260321-01 | S (~1 day) | Backend + Financial Reporting |
| IDEA-frontend-ux-20260321-02 | M (~1–2 days) | Frontend + Docs |
| IDEA-head-of-specs-20260421-02 | S (~0.5 day) | Governance — Head of Specs |
| IDEA-api-contracts-20260421-01 | S (~1 day) | Governance — API Contracts |
| IDEA-api-contracts-20260421-02 | S (~0.5 day) | Governance — API Contracts |
| IDEA-director-of-quality-20260421-01 | M (~2 days) | QA + Backend |
| IDEA-strategy-owner-20260421-02 | S (~0.5 day) | Governance — Strategy Owner |
| IDEA-ai-compliance-20260421-01 | S (~1 day) | Backend + AI Compliance |
| IDEA-infra-ops-20260421-01 | S (~0.5 day) | Backend + Ops |
| IDEA-qa-testing-20260421-01 | M (~2 days) | QA + Backend |
| IDEA-frontend-ux-20260421-01 | M (~2 days) | UX + Frontend Docs |
| **Total** | **~13.5 days** | Mixed |

### Skill-Silo Check (STEP 7.1)

Governance-heavy items (Head of Specs, API Contracts, Strategy Owner, AI Compliance): ~4 items × S effort = ~3 days
Execution-heavy items (Backend, QA, Frontend): ~10 items × mixed effort = ~10.5 days

**Governance load %:** ~3/13.5 = ~22% → Within 20–60% bounds ✅

**Skill-Silo Alert:** None — governance load is between floor and ceiling.

**Sign-Off Capacity Floor check:** 22% governance load is above the 20% floor. Product Owner confirms adequate review and sign-off capacity for v2.9 sprint planning. No deferred spec approvals identified. ✅

**Workforce constraints:** No scarce skill conflicts. The backlog adds are predominantly documentation, spec authoring, and test infrastructure — well within the team's capability at current scale.

**Economics verdict:** All 14 advancing items are within capacity and workforce constraints. No forced Replace, Defer, or Kill required.

---

## STEP 8 — Final Rebalance Decision

**Authority:** Product Owner (within all constraints)

### Context Re-Read (Section 2 + Section 9)

Strategy constraints confirmed: §13 exclusions (no automated trading, no ML prediction, no configurable strategy builder). Zero-sum rule applies at roadmap level.

### Per-Initiative Decisions

**Roadmap-level:** No active initiatives. Arc model in place. **No roadmap-level Add, Replace, Defer, or Kill decisions.** All six arcs are correctly placed in their horizons.

**Backlog-level (net-new items from advancing candidates):**

| Backlog Item | Source Idea | Priority | Displacement |
|-------------|-------------|----------|-------------|
| BLG-SPEC-20 — Machine-readable spec front-matter standard | IDEA-head-of-specs-20260321-02 | P3 | BLG-GOV-11 (P3) deprioritised |
| BLG-AI-01 — AI Journal summary audit log | IDEA-ai-compliance-20260421-01 | P2 | TEST-GAP-EPIC-04 (P3) deprioritised |
| BLG-AI-02 — Model version contract for AI Journal | IDEA-ai-compliance-20260321-02 | P3 | BLG-FEAT-13 (P3) deprioritised |
| BLG-FEAT-18 — Consecutive losing streak metric | IDEA-metrics-analytics-20260321-01 | P2 | BLG-DATA-01 (Positions Table Data Dictionary, P2) deprioritised in v2.9 queue |
| BLG-FEAT-19 — Monthly P&L summary report | IDEA-financial-reporting-20260321-01 | P2 | BLG-GOV-11 (P3) dual displacement |
| BLG-FE-16 — React component inventory | IDEA-frontend-ux-20260321-02 | P3 | BLG-FE-15 (P3) deprioritised |
| BLG-SPEC-21 — Screener results schema spec | IDEA-head-of-specs-20260421-02 | P1 | BLG-GOV-11 (P3) triple displacement (all S-effort combined < M-effort displaced) |
| BLG-SPEC-22 — Alpaca API integration contract | IDEA-api-contracts-20260421-01 | P1 | BLG-GOV-08 (P3) further deferred |
| BLG-SPEC-23 — Screener internal API contract | IDEA-api-contracts-20260421-02 | P1 | BLG-TECH-05 (P3) deprioritised |
| BLG-QA-08 — External API mock harness for CI | IDEA-director-of-quality-20260421-01 | P1 | BLG-FEAT-13 (P3) displaced |
| BLG-GOV-16 — §13 review record for DS-06 Alpaca News | IDEA-strategy-owner-20260421-02 | P1 | BLG-FE-09 (P3) deprioritised |
| BLG-OPS-12 — External API health check extension | IDEA-infra-ops-20260421-01 | P2 | BLG-GOV-11 (P3) dual displacement |
| BLG-QA-09 — Screener test data library | IDEA-qa-testing-20260421-01 | P1 | BLG-FEAT-13 dual displacement (S+M combined < L displaced) |
| BLG-FE-17 — Screener results page UX spec | IDEA-frontend-ux-20260421-01 | P1 | BLG-TECH-05 dual displacement |

**Net-zero check:** All adds are backlog-level only. 0 roadmap-level Adds. 0 roadmap-level Kills. Net-zero: 0 ≤ 0 ✅

**Initiative displacement candidate flag:** No active initiatives; no displacement candidate flag required this cycle.

### Skill-Silo Ceiling Pull-Forward Check

Governance load 22% — above floor, within ceiling. No pull-forward candidate scan required.

### Final decision summary

**Roadmap:** No-change (arc model stable; Now horizon empty; Next Phase items correctly placed)
**Backlog:** 14 new items promoted (listed above)
**Ideas parked this cycle:** 2 moved to park during debate (IDEA-strategy-owner-20260321-02, IDEA-challenger-20260421-02); all 34 new parked ideas receive Parked-cycle-1; 10 stale ideas incremented.
**Stale ideas closed:** 0
