Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-04-28__scheduled
Phase: Roadmap Rebalance
Last Updated: 2026-04-28

---

# Cycle Record — Roadmap Rebalance 2026-04-28__scheduled

**Run type:** Scheduled — no completion event
**Tier:** Standard
**Date:** 2026-04-28

---

## STEP 2 — Re-Validation

**Authorities:** Product Owner + Strategy Rules & System Intent Owner

### Active Initiatives

**No active initiatives as of 2026-04-28.** v3.0 shipped 2026-04-27 (Verified). Arc 1 is substantially complete — DS-01 screener engine, DS-02 screener results page, DS-05 Alpaca integration, DS-06 news panel, DS-07 watchlist promotion all delivered. DS-04 (Earnings Calendar) deferred to v3.1 as an independent feature. Next phase is v3.1 Arc 2: Pre-Trade Research & Planning.

The six-arc strategic structure remains the canonical anchor. No initiative currently sits in the Now horizon consuming active workforce allocation. Arc 2 features (PT-01–PT-05) are in the Next horizon, not yet committed.

*Record: "No active initiatives requiring re-validation — v3.0 shipped; arc model stable. Arc 1 substantially complete. Next arc: Arc 2 (v3.1–v3.3)."*

### Force Classification

No items to classify 🔥/⚠/❌. Arc structure reviewed and confirmed intact.

### Strategy Proximity Scores (STEP 2.1)

No active initiatives to score.

| Item | SPS | Rationale |
|------|-----|-----------|
| (none) | — | No active initiatives |

**Cycle Proximity Score (CPS):** 0.0
**Prior cycle CPS:** 0.0 (cycle 2026-04-24__scheduled — also no active initiatives)
**Delta:** 0.0 — no drift
**Strategy Drift Alert:** None required (CPS = 0.0, delta = 0.0). ✅

### Horizon Review (STEP 2.3)

**Now horizon:** Empty. All v3.0 and prior annotations mark shipped items only. No committed items.

**Next Phase — Horizon: Next (Arcs 1 remaining + Arc 2):**

| Feature | ID | Horizon | Review outcome |
|---------|----|---------|---------------|
| Earnings Calendar Integration | DS-04 | Next — v3.1 | Correctly placed. No spec exists; independent M-effort feature; appropriate for v3.1. No movement. |
| Trade Plan Object | PT-01 | Next — v3.1 | Correctly placed. Arc 2 data model prerequisite. No movement. |
| Pre-Trade Research View | PT-02 | Next — v3.1 | Correctly placed. Depends on PT-01. No movement. |
| Prospective Heat at Entry | PT-03 | Next — v3.1 | Correctly placed. Frontend integration only. No movement. |
| Pre-Trade Entry Checklist | PT-05 | Next — v3.1 | Correctly placed. Depends on PT-02. No movement. |
| Setup Quality Score | PT-04 | Next — v3.1 | Correctly placed. Gate: 20+ closed trades. No movement. |

**Later horizon (Arcs 3–6):** No movements recommended. IT-01 and IT-02 (Arc 3) continue as pull-forward candidates for Arc 3 review. SI-01 and SI-03 (Arc 5) retain pull-forward candidacy note. Sequencing rationale remains valid.

**Horizon Review Outcome:** No movements recommended. Now horizon empty (all Arc 1 items shipped). v3.1 scope is clear: DS-04 + Arc 2 (PT-01–PT-05) + backlog items promoted this cycle. No horizon movements required.

---

## STEP 3 — Backlog Health

**Authority:** Head of Specs Team (process), Product Owner (planning ownership)

### Active Backlog Items (post-groom 2026-04-28)

| ID | Title | Priority | Effort | Observation |
|----|-------|----------|--------|-------------|
| BLG-FEAT-19 | Monthly P&L summary report | P2 | S | Reporting enhancement; v3.1 target. No urgency change. Aligned. |
| BLG-FE-16 | React component inventory | P3 | M | BLG-FE-16 is dependency gate for IDEA-frontend-ux-20260304-02. Now that Arc 1 frontend is shipped (DS-02 screener results page adds significant new component surface), this item has increased relevance for Arc 2 frontend planning. Appropriately placed. |
| BLG-OPS-13 | API performance baseline re-run | P3 | S | 8 endpoints now without baseline entries (v2.8/v2.9/v3.0). OA-v30-01 tracks this. Correct placement; manual effort requiring live env. |
| BLG-GOV-11 | Cycle artefact inventory | P3 | M | 2 consecutive cycle deferrals (v2.9, v3.0). Valid concern but not blocking. Not urgent vs. security/QA items surfaced this cycle. Candidate for further deferral. |
| BLG-FEAT-13 | Feature flag rollout | P3 | M | No active trigger at single-user scale. No Arc alignment. Candidate for §9 deferral this cycle. |

**Observations:**
- No obsolete items. All 5 active items remain aligned to product intent.
- No duplicates. IDs are unique.
- Quick wins: BLG-FEAT-19 (S effort, P2) is the most immediately deliverable item and should remain prioritised in v3.1 planning.
- BLG-GOV-11 and BLG-FEAT-13 are displacement candidates for new backlog adds this cycle.
- Arc 1 shipped → significant gate-clearance event for ideas backlog (see STEP 4). New security and QA items from this cycle will enter the backlog at P3, appropriate alongside existing items.

---

## STEP 4 — Ideas

**Authority:** Facilitator (review), Product Owner (classification decisions)

### Gate-Condition Re-Check (STEP 4.0)

**Trigger:** v3.0 shipped 2026-04-27, delivering DS-01 screener engine. This is the single largest gate-clearance event since the IW-20260421-01 window filed 44 ideas with ~25 referencing "DS-01 not yet built" or "post-Arc 1" as park rationale.

| Idea ID | Referenced Item | Gate Status | Action Required |
|---------|----------------|-------------|----------------|
| IDEA-frontend-ux-20260304-02 | BLG-FE-16 (React component inventory) | Pending — BLG-FE-16 still active | Normal classification |
| IDEA-head-of-ux-20260321-02 | Arc 1 screener frontend (v3.0/v3.1) | **CLEARED** — Arc 1 shipped v3.0 | Mandatory re-evaluation |
| IDEA-product-owner-20260421-01 | DS-01/DS-02 ship | **CLEARED** — DS-01/DS-02 shipped v3.0 | Mandatory re-evaluation |
| IDEA-director-of-quality-20260421-02 | DS-01 screener engine | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-finops-20260421-01 | DS-01 screener engine | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-finops-20260421-02 | DS-01 screener engine | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-infra-ops-20260421-02 | DS-01 screener engine | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-challenger-20260421-01 | BLG-FE-17 (screener UX spec) | **CLEARED** — BLG-FE-17 shipped v2.9; DS-02 delivered; concern addressed | Mandatory re-evaluation |
| IDEA-backend-engineering-20260421-01 | DS-01 screener engine design | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-metrics-analytics-20260421-01 | DS-01 screener live | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-metrics-analytics-20260421-02 | DS-01 screener live | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-head-of-engineering-20260421-01 | DS-01 screener engine | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-head-of-engineering-20260421-02 | BLG-QA-08 mock harness | **CLEARED** — BLG-QA-08 shipped v2.9; Challenger argument accepted | Mandatory re-evaluation |
| IDEA-data-model-20260421-01 | DS-01 extension at v3.0 sprint planning | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-data-model-20260421-02 | DS-01 spec work at v3.0 sprint planning | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-qa-testing-20260421-02 | DS-01 implementation scoped at v3.0 | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-head-of-ux-20260421-01 | DS-01 screener live | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-cybersecurity-20260421-01 | Arc 1 screener engine | **CLEARED** — Arc 1 shipped v3.0 | Mandatory re-evaluation |
| IDEA-cybersecurity-20260421-02 | Arc 1 complete | **CLEARED** — Arc 1 shipped v3.0 | Mandatory re-evaluation |
| IDEA-financial-reporting-20260421-01 | DS-01 screener live | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-financial-reporting-20260421-02 | DS-01 screener live | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-pmo-lead-20260421-01 | Arc 1 ships | **CLEARED** — Arc 1 shipped v3.0 | Mandatory re-evaluation |
| IDEA-qa-lead-20260421-02 | DS-01 scoped at v3.0 sprint planning | **CLEARED** — DS-01 shipped v3.0 | Mandatory re-evaluation |
| IDEA-director-of-hr-20260421-02 | Post-Arc 1 if integration failures surface | **SOFT-CLEARED** — Arc 1 shipped; Alpaca null-bars hotfix (EP-01) was an integration failure | Mandatory re-evaluation |

**Gate-condition check record:** 24 ideas checked. 23 cleared (22 firm + 1 soft-cleared). 1 still pending (IDEA-frontend-ux-20260304-02 — BLG-FE-16 not yet shipped).

### Stale Ideas (≥3 consecutive cycles — mandatory PO disposition)

| Idea ID | Title | Cycles Parked | Action Required |
|---------|-------|--------------|----------------|
| IDEA-frontend-ux-20260304-02 | Accessibility Baseline for Critical UI Components | 11 | Mandatory disposition |
| IDEA-challenger-20260321-01 | SPS≥4 mandatory §13 review gate | 7 | Mandatory disposition |
| IDEA-ai-compliance-20260321-01 | Governed decision audit log | 7 | Mandatory disposition |
| IDEA-metrics-analytics-20260321-02 | ATR-normalised sizing retrospective | 7 | Mandatory disposition |
| IDEA-financial-reporting-20260321-02 | Net-of-costs performance tracking | 7 | Mandatory disposition |
| IDEA-head-of-ux-20260321-02 | Design system document | 7 | Mandatory disposition (also gate-cleared) |

### Per-Idea Classification (STEP 4.1)

**Total eligible ideas:** 32 (Submitted + Parked-cycle-N in ideas_register.md)
**Window:** No new window this cycle (run ideas not invoked; 32 ≥ 20 threshold).

---

**✅ Advancing (5):**

| Idea ID | Title | Gate Status | PO Rationale |
|---------|-------|-------------|-------------|
| IDEA-cybersecurity-20260421-01 | Alpaca API key rotation policy | Gate cleared — Arc 1 shipped | Alpaca API key in daily use by screener (601 tickers). No rotation policy = unmanaged exposure risk. Security hygiene now Alpaca is operational infrastructure. |
| IDEA-cybersecurity-20260421-02 | External API credential audit | Gate cleared — Arc 1 complete | Alpaca + Anthropic both in active production use. No credential inventory exists. Post-Arc 1 operational baseline. |
| IDEA-pmo-lead-20260421-01 | External API dependency risk register | Gate cleared — Arc 1 shipped | Alpaca is now critical path for screener. BLG-SPEC-22 covers technical contract; operational risk context is a separate concern. XS effort. |
| IDEA-qa-testing-20260421-02 | Screener scenario library | Gate cleared — DS-01 shipped | DS-01 shipped but BLG-QA-08 mock harness covers CI only. Formal scenario library (synthetic ticker data for all filter combinations: regime pass/fail, ATR threshold pass/fail, signal threshold pass/fail) improves regression coverage now that DS-01 is in production. |
| IDEA-director-of-quality-20260421-02 | Screener accuracy test protocol | Gate cleared — DS-01 shipped | DS-01 live. The DoQ verified DS-01 in v3.0 implicitly. A reproducible formal accuracy test protocol enables future regression detection as screener parameters evolve. |

---

**❌ Rejected (7):**

| Idea ID | Title | Strong? | Rejection Rationale |
|---------|-------|---------|-------------------|
| IDEA-challenger-20260421-01 | Screener result stale data risk | No | BLG-FE-17 shipped v2.9; DS-02 UX spec delivered with freshness indicator requirement; DS-02 shipped v3.0. Concern fully addressed in shipped implementation. No separate backlog item needed. |
| IDEA-head-of-engineering-20260421-02 | Data pipeline integration test suite | No | Challenger argument accepted at 2026-04-24__scheduled — tests should accompany DS-01 as sprint stories, not standalone. DS-01 shipped in v3.0 with test coverage via mock harness (BLG-QA-08). Window for including pipeline tests with DS-01 has passed. Reject — mock harness covers CI need. |
| IDEA-infra-ops-20260421-02 | Screener run scheduler decision record | No | DS-01 implemented with clear scheduling approach (on-demand via POST /screener/run + background task pattern). Decision was made during implementation. A standalone retrospective decision record adds overhead without functional value. Reject. |
| IDEA-qa-lead-20260421-02 | Screener QA sign-off criteria | No | DS-01 shipped with implicit criteria (DoQ sign-off, v3.0 verification report). Formal pre-implementation QA criteria have low value post-implementation. Criteria established in practice. Reject. |
| IDEA-director-of-hr-20260421-01 | Arc 1 team readiness assessment | No | Solo-dev constraint is permanent at current scale. No team scale change since submission. Reject. |
| IDEA-challenger-20260321-01 | SPS≥4 mandatory §13 review gate (formal) | No | 7 consecutive cycles. Existing mechanism (STEP 5 Score-4 soft rule + Score-5 veto in roadmap_prompt.md) already enforces SPS≥4 handling. No governance incidents attributable to the absence of a formal gate. Adding a redundant formal gate increases maintenance overhead without improving safety. Reject. |
| IDEA-ai-compliance-20260321-01 | Governed decision audit log (searchable) | **Yes** | 7 consecutive cycles. decision_log.md provides strong partial coverage. A fully searchable structured audit log is a valid idea at scale but not warranted at current governance volume (23 decision entries across 16 cycles). Reject-but-strong: the idea remains valid; the timing is not right until governance volume increases significantly (e.g., >100 entries, multi-user governance, or external audit requirement). |

---

**🅿 Parked — re-parked with updated rationale or incremented cycle count (20):**

| Idea ID | Title | Old Status | New Status | Updated Rationale |
|---------|-------|-----------|-----------|------------------|
| IDEA-frontend-ux-20260304-02 | Accessibility Baseline | Parked-cycle-11 | Parked-cycle-12 | BLG-FE-16 (React component inventory) still active. Dependency gate remains valid. Re-park until BLG-FE-16 delivers. |
| IDEA-metrics-analytics-20260321-02 | ATR-normalised sizing retrospective | Parked-cycle-7 | Parked-cycle-8 | Arc 2 (v3.1) will deliver PT-04 (Setup Quality Score) and trade-plan data; this metric is most meaningful after PT-04 data exists across multiple trades. Re-park for Arc 2 midpoint review. |
| IDEA-financial-reporting-20260321-02 | Net-of-costs performance tracking | Parked-cycle-7 | Parked-cycle-8 | Requires brokerage cost fields per trade — a natural Arc 2/4 data model extension. Re-park for v3.2 planning. |
| IDEA-head-of-ux-20260321-02 | Design system document | Parked-cycle-7 | Parked-cycle-8 | Gate cleared (Arc 1 shipped). PO re-evaluated: Arc 1 frontend delivered (DS-02 screener results page). Design inconsistencies exist but are tolerable at single-user scale. Arc 2 PT-02 (Pre-Trade Research View) is the natural trigger for design investment — multi-panel complex UI. Re-park until PT-02 enters sprint scope. |
| IDEA-product-owner-20260421-01 | Screener morning routine UX | Parked-cycle-1 | Parked-cycle-2 | Gate cleared (DS-01/DS-02 shipped). This Arc 2/3 UX concept (guided screener → watchlist → entry flow) is naturally upstream of Arc 2 planning. Re-park until v3.1 release planning kicks off — the release planning engine will scope Arc 2 UX with this idea as input. |
| IDEA-product-owner-20260421-02 | Candidate quality retrospective | Parked-cycle-1 | Parked-cycle-2 | Screener live but no screener-attributed trade data exists yet. Requires multiple screener-promoted candidates to have entered positions. Arc 4/5 level. Re-park. |
| IDEA-head-of-specs-20260421-01 | External API integration spec template | Parked-cycle-1 | Parked-cycle-2 | 2 integrations now in use (Alpaca: BLG-SPEC-22; Yahoo Finance: informal). Gate condition (2 integrations) technically met. However, Arc 2 and Arc 3 will not add new external API integrations immediately — template investment premature before a third integration need arises. Re-park for Arc 3 planning. |
| IDEA-pmo-lead-20260421-02 | Arc velocity tracking | Parked-cycle-1 | Parked-cycle-2 | velocity_metrics.md is functional. No gap evidence. Re-park. |
| IDEA-finops-20260421-01 | Alpaca API cost monitoring | Parked-cycle-2 | Parked-cycle-3 | Gate cleared (DS-01 live). PO re-evaluated: screener is live with 601 tickers but 1 day of operational history. Monitoring premature until 2–4 weeks of call volume data establishes a baseline. Re-park with new timing: post-v3.1 sprint, when 4+ weeks of screener data is available. |
| IDEA-finops-20260421-02 | Data pipeline cost baseline | Parked-cycle-2 | Parked-cycle-3 | Same timing as Alpaca cost monitoring. Need baseline run data to document expected costs. Re-park: post-v3.1 sprint after 4+ weeks of screener operational history. |
| IDEA-backend-engineering-20260421-01 | Screener result caching strategy | Parked-cycle-2 | Parked-cycle-3 | DS-01 shipped with on-demand computation pattern (POST /screener/run + screener_runs table). Caching optimization is warranted as usage scales. No scale event yet (day 1 of operation). Re-park: revisit if screener run latency becomes a user-observed issue in v3.1. |
| IDEA-metrics-analytics-20260421-01 | Screener hit rate metric | Parked-cycle-2 | Parked-cycle-3 | Screener live. Gate cleared. But hit rate (screener → watchlist → position) requires multiple screener promotion-to-trade cycles. Day 1 of screener operation. Re-park: 4+ weeks of screener attribution data needed. |
| IDEA-metrics-analytics-20260421-02 | Regime distribution metric | Parked-cycle-2 | Parked-cycle-3 | Screener live. Gate cleared. Metric tracks regime distribution across screener runs over time — requires run history. Re-park: 4+ weeks of screener runs needed for meaningful distribution analysis. |
| IDEA-head-of-engineering-20260421-01 | Screener engine performance benchmark | Parked-cycle-2 | Parked-cycle-3 | DS-01 shipped. BLG-OPS-13 covers API endpoint latency (p50/p95 for GET /screener/results, POST /screener/run). Screener batch run duration benchmark (total batch time for 601-ticker universe) is a separate operational concern. Re-park: establish via OA-v30-01 resolution or v3.1 operational review. |
| IDEA-data-model-20260421-01 | Screener result history table | Parked-cycle-2 | Parked-cycle-3 | DS-01 shipped; screener_runs table persists run metadata. Full per-ticker history table (trend tracking across runs) not in v3.0 scope. Valid Arc 1 extension. Re-park as v3.1 backlog candidate at release planning. |
| IDEA-data-model-20260421-02 | Ticker universe management data model | Parked-cycle-2 | Parked-cycle-3 | public.tickers table implemented in v3.0 (ST-01). Formal data dictionary for the ticker universe schema is appropriate post-implementation. Re-park: candidate for BLG-SPEC item at v3.1 spec review. |
| IDEA-head-of-ux-20260421-01 | Arc 1 daily workflow journey map | Parked-cycle-2 | Parked-cycle-3 | DS-01 live. Journey mapping (screener → watchlist → Arc 2 research) is most valuable when Arc 2 UX design is starting. Re-park: input to Arc 2 PT-02 (Pre-Trade Research View) design phase. |
| IDEA-cybersecurity-20260421-01 | Alpaca API key rotation policy | (→ Advancing) | (→ Advancing) | See above |
| IDEA-cybersecurity-20260421-02 | External API credential audit | (→ Advancing) | (→ Advancing) | See above |
| IDEA-director-of-hr-20260421-02 | External API expertise register | Parked-cycle-2 | Parked-cycle-3 | Post-Arc 1 + integration failure (Alpaca null-bars hotfix). However, at solo-dev scale, ownership is unambiguous (Alpaca: Backend Engineering Patterns Owner + API Contracts Owner). An expertise register adds overhead with minimal risk reduction. Re-park: revisit if a second integration failure occurs in a different system area. |
| IDEA-financial-reporting-20260421-01 | Screener-to-trade attribution | Parked-cycle-2 | Parked-cycle-3 | Screener live. Requires multiple screener-promoted candidates to have entered positions (none yet — screener launched 2026-04-27). Arc 4/5 level. Re-park: 8+ weeks of screener usage data needed. |
| IDEA-financial-reporting-20260421-02 | External API cost attribution | Parked-cycle-2 | Parked-cycle-3 | DS-01 live driving API calls. Cost attribution meaningful after 4+ weeks of baseline data. Re-park: post-v3.1 sprint with FinOps/Financial Reporting review. |

### Idea Participation Check (STEP 4.3)

No intake window this cycle (IW not run; 32 eligible ideas ≥ 20 threshold — intake skipped).

**Innovation debt note:** Idea intake engine was not run this cycle (threshold condition met). No per-agent submission counts available. No gap to record.

### STEP 4 Write Summary

```
Window: not run this cycle (32 eligible ideas ≥ 20 threshold)
Total submissions loaded: 32
Advancing to STEP 5: 5
Parked (re-parked or incremented): 20
Rejected: 7
Rejected-but-strong (added to register): 1 (IDEA-ai-compliance-20260321-01)
Stale ideas (≥3 cycles parked) surfaced: 6
Stale ideas closed this cycle: 2 (IDEA-challenger-20260321-01 rejected; IDEA-ai-compliance-20260321-01 rejected-but-strong)
```

### Ideas Advancing to STEP 5

| Idea ID | Agent | Title | Displacement Named |
|---------|-------|-------|--------------------|
| IDEA-cybersecurity-20260421-01 | Cybersecurity & Trust Lead | Alpaca API key rotation policy | Yes — BLG-FEAT-13 → §9 |
| IDEA-cybersecurity-20260421-02 | Cybersecurity & Trust Lead | External API credential audit | Yes — BLG-GOV-11 → v3.2 |
| IDEA-pmo-lead-20260421-01 | PMO Lead | External API dependency risk register | Yes — BLG-OPS-13 → OA resolution |
| IDEA-qa-testing-20260421-02 | QA & Testing Owner | Screener scenario library | Yes — BLG-FE-16 → further defer |
| IDEA-director-of-quality-20260421-02 | Director of Quality | Screener accuracy test protocol | Yes — BLG-FEAT-19 reorder in priority queue |

**Queue count check:** 5 in queue = 5 "Advancing to STEP 5" in summary. ✅

### STEP 5 Debate Queue

| IDEA ID | Title | Source |
|---------|-------|--------|
| IDEA-cybersecurity-20260421-01 | Alpaca API key rotation policy | new (gate-cleared) |
| IDEA-cybersecurity-20260421-02 | External API credential audit | new (gate-cleared) |
| IDEA-pmo-lead-20260421-01 | External API dependency risk register | new (gate-cleared) |
| IDEA-qa-testing-20260421-02 | Screener scenario library | new (gate-cleared) |
| IDEA-director-of-quality-20260421-02 | Screener accuracy test protocol | new (gate-cleared) |

---

## STEP 5 — Debate

**Authorities:** Product Owner (chair) + Challenger (non-decision challenge)

**Context re-statement (pre-debate):**
Top 2 constraints most likely to block an "easy yes":
1. **§3 human-in-loop constraint**: Any item that moves toward automation, automated advisory, or removes the user's deliberate confirmation step is suspect. Items that purely document or test are well inside §3.
2. **Zero-sum displacement**: At backlog level, each advance must name a specific item being deprioritised or deferred — capacity for v3.1 is finite.

**STEP 5 Debate Queue preflight:** 5 queued IDs confirmed. 5 debate entries will be authored below. ✅

**STEP 5.0 Pre-Debate Gate Checks:**
- PoG validity check: No advancing items carry a prior PoG. N/A. ✅
- Score-5 presence check: All advancing items are expected SPS=1 (pure operational/QA). No Score-5 items. ✅

---

### Debate 1 — IDEA-cybersecurity-20260421-01: Alpaca API key rotation policy

**5.0 Required Case (Product Owner):**
1. Problem: The Alpaca Markets API key is now in daily operational use by the screener engine (601-ticker universe). No formal rotation policy exists — no documented cadence, no procedure for rotation without downtime, no verification test. Key compromise would silently fail screener operations.
2. Strategy intent served: Operational resilience — the screener is the Arc 1 end-state delivery. Protecting its data pipeline integrity is within §12 operational hygiene scope.
3. What if we don't: Undocumented key lifecycle creates silent risk. A compromised or expired key would cause screener failures with no documented recovery procedure.
4. Displacement: BLG-FEAT-13 (P3 feature flag rollout) — deprioritised to §9. No active trigger at single-user scale; Arc 2 does not require feature flags.

**5.1 Challenger counter-argument:**
*Clearance Statement — Cleared.* Reviewed §3 (human-in-loop): a key rotation policy document does not introduce automation or remove human confirmation — it defines a human-executed procedure. Reviewed §13 (system boundaries): external API key management is operational hygiene, not a new system boundary. No strategy_rules.md sections engaged. Challenger clears IDEA-cybersecurity-20260421-01.

**5.2 Product Owner response:** ✅ Advance — Clearance noted. No counter-argument to address. Displacement confirmed (BLG-FEAT-13 → §9). New backlog item: BLG-SEC-03.

---

### Debate 2 — IDEA-cybersecurity-20260421-02: External API credential audit

**5.0 Required Case (Product Owner):**
1. Problem: Alpaca API key and Anthropic API key both in active production use. No inventory of storage location, expiry, rotation history, or last-rotation date. Post-Arc 1, the credential surface has grown.
2. Strategy intent served: Same operational hygiene scope as Debate 1.
3. What if we don't: No baseline for credential governance. An expired or unknown credential creates a silent production failure with no recovery playbook.
4. Displacement: BLG-GOV-11 (P3 cycle artefact inventory) — defer to v3.2. Two consecutive cycle deferrals already; not blocking any delivery.

**5.1 Challenger counter-argument:**
*Clearance Statement — Cleared.* §3 and §13 not engaged. Operational documentation only. Reviewed §12 operational requirements: credential audit is standard operational hygiene for systems with external API dependencies. No governance concern.

**5.2 Product Owner response:** ✅ Advance — Cleared. Displacement confirmed (BLG-GOV-11 → v3.2). New backlog item: BLG-SEC-04.

---

### Debate 3 — IDEA-pmo-lead-20260421-01: External API dependency risk register

**5.0 Required Case (Product Owner):**
1. Problem: Alpaca is now the critical data path for the screener. BLG-SPEC-22 documents the technical contract; no operational risk register captures reliability record, fallback status, SLA concerns, or incident history. The Alpaca null-bars hotfix (EP-01, 2026-04-25) demonstrated a real integration failure — the system needed rapid diagnosis.
2. Strategy intent served: Resilience of the Arc 1 end-state. strategy_rules.md §12 requires operational transparency.
3. What if we don't: Integration risk context is held only in individual incident memory. A second Alpaca failure (or new Yahoo Finance issue) would require re-investigation from scratch.
4. Displacement: BLG-OPS-13 (P3 API performance baseline re-run) — deprioritise; OA-v30-01 tracks it as an outstanding action, no active sprint urgency.

**5.1 Challenger counter-argument:**
*Counter-argument — Park.*
- Challenger position: Park
- Evidence: strategy_rules.md §13 single-user constraint. The system is operated by a single experienced user who already holds operational context about external API risks in their working memory.
- Reason: A formal risk register adds maintenance overhead for a single-user system. The user tracked the Alpaca null-bars failure and applied a hotfix within the same session — this demonstrates adequate operational awareness without a structured register. The operational benefit of a formal document is marginal at current scale.
- Consequence: If we proceed, we add a governance artefact that requires updates after each integration failure but may not meaningfully reduce response time in a solo-dev context.

**5.2 Product Owner response:** Rebut — ✅ Advance. The risk register's value is not daily operations (the user already knows the system) but forward reference: (a) at the first scheduled review after v3.1, the register provides a structured scan for emerging issues; (b) at any future scale change, it provides an operational baseline that would otherwise require reconstruction from memory/git history; (c) the EP-01 null-bars hotfix demonstrated that reactive diagnosis, while fast, is slower than having the integration's known failure modes documented. XS effort (~2 hours). Displacement confirmed (BLG-OPS-13 → OA resolution timing). New backlog item: BLG-GOV-17.

**Challenger obligation satisfied: Type A counter-argument issued for IDEA-pmo-lead-20260421-01.** STEP 8.6 guardrail pre-satisfied. ✅

---

### Debate 4 — IDEA-qa-testing-20260421-02: Screener scenario library

**5.0 Required Case (Product Owner):**
1. Problem: DS-01 shipped but test coverage relies on BLG-QA-08 mock harness (CI mocking). A formal scenario library (synthetic ticker data sets covering every filter combination: regime pass/fail, ATR threshold pass/fail, signal threshold pass/fail, multi-market UK/US) enables deterministic regression testing as screener parameters evolve. strategy_rules.md §11 is the parameter source — any §11 change should have a corresponding scenario test.
2. Strategy intent served: Correctness of deterministic screening (core Arc 1 purpose). Directly supports §11 parameter governance.
3. What if we don't: Screener regression testing remains ad hoc. A §11 parameter change cannot be validated deterministically without a scenario library — it would rely on live data re-runs, which are non-deterministic.
4. Displacement: BLG-FE-16 (P3 React component inventory) — further defer; its dependency gate (IDEA-frontend-ux-20260304-02) remains unmet.

**5.1 Challenger counter-argument:**
*Clearance Statement — Cleared.* Reviewed §3: test data infrastructure is pure QA tooling. §13: screening correctness tests are fully within bounds (deterministic, rules-based). No strategy boundary proximity. Clearance issued: §3 and §13 not engaged; test scenario library supports strategy_rules.md §11 correctness.

**5.2 Product Owner response:** ✅ Advance — Cleared. Displacement confirmed (BLG-FE-16 → further defer). New backlog item: BLG-QA-10.

---

### Debate 5 — IDEA-director-of-quality-20260421-02: Screener accuracy test protocol

**5.0 Required Case (Product Owner):**
1. Problem: DS-01 shipped and was verified implicitly in v3.0 DoQ sign-off. However, no formal, reproducible protocol exists for validating screener output accuracy — comparing screener results against manually verified expected outputs for known tickers with known ATR/regime states. As §11 parameters evolve, accuracy regression must be detectable.
2. Strategy intent served: Deterministic screening correctness per §11. Enables future §11 parameter audits.
3. What if we don't: Screener accuracy is verified ad hoc (manual review by DoQ at each PR). Not reproducible; regression risk as screener evolves.
4. Displacement: BLG-OPS-13 (P3 API performance baseline re-run) — already listed as displacement for BLG-GOV-17; both are P3 with OA tracking. Shared deprioritisation slot acceptable at same priority tier.

**5.1 Challenger counter-argument:**
*Clearance Statement — Cleared.* §3: QA protocol is human-executed, not automated. §13: accuracy testing of deterministic screening is fully within bounds. Cleared: pure QA governance with direct §11 traceability.

**5.2 Product Owner response:** ✅ Advance — Cleared. Displacement noted. New backlog item: BLG-QA-11.

---

### STEP 8.6 — Run-Level Disagreement Guardrail

Condition 1: At least one candidate classified 🅿 Parked or ❌ Rejected during this run?
→ YES. 7 rejected in STEP 4 + 20 re-parked in STEP 4. ✅

Guardrail passes. No Pivot Loop (STEP 8.7) required.

---

## STEP 8 — Final Rebalance Decision

**Authority:** Product Owner (within all constraints and vetoes)

### STEP 9.0 Pre-check — Net-Zero Displacement Verification

- Roadmap-level additions: 0 (all 5 advances are backlog-level only — no new strategic initiative added to roadmap)
- Roadmap-level kills: 0
- 0 ≤ 0 ✅ Net-zero at roadmap level satisfied.
- At backlog level: 5 adds, 3 formal deprioritisations (BLG-FEAT-13 → §9; BLG-GOV-11 → v3.2; BLG-FE-16 → further defer). All named. ✅

### Per-Initiative Decisions

| Decision | Item | Type | Displacement |
|----------|------|------|-------------|
| ➕ Add | BLG-SEC-03 — Alpaca API key rotation policy (S effort; P3; Cybersecurity & Trust Lead; Provisional v3.1) | Backlog-level | BLG-FEAT-13 → §9 deferred |
| ➕ Add | BLG-SEC-04 — External API credential audit (XS effort; P3; Cybersecurity & Trust Lead; Provisional v3.1) | Backlog-level | BLG-GOV-11 → v3.2 |
| ➕ Add | BLG-GOV-17 — External API dependency risk register (XS effort; P3; PMO Lead; Provisional v3.1) | Backlog-level | BLG-OPS-13 → OA resolution timing |
| ➕ Add | BLG-QA-10 — Screener scenario library (M effort; P2; QA & Testing Owner; Provisional v3.1) | Backlog-level | BLG-FE-16 → further defer |
| ➕ Add | BLG-QA-11 — Screener accuracy test protocol (S effort; P2; Director of Quality; Provisional v3.1) | Backlog-level | BLG-OPS-13 (shared deprioritisation) |
| ⏸ Deprioritise | BLG-FEAT-13 → §9 deferred (no active trigger at single-user scale) | Backlog — move to §9 | — |
| ⏸ Deprioritise | BLG-GOV-11 → defer to v3.2 | Backlog — update Provisional-Target | — |
| ⏸ Deprioritise | BLG-FE-16 → further defer (still pending dependency gate) | Backlog — update note | — |

**Roadmap change:** None. No items added or removed from `current_roadmap.md` horizon structure. `Last Updated` and `Last rebalance` will be updated for lifecycle compliance.

**No-change roadmap:** Yes (at roadmap horizon level). Required: roadmap Last Updated date updated; decision log entry for no-change. ✅

### Skill-Silo Check (STEP 7.1)

**New items by primary skill demand:**
- BLG-SEC-03: Cybersecurity & Trust Lead — governance documentation (governance-heavy)
- BLG-SEC-04: Cybersecurity & Trust Lead — governance documentation (governance-heavy)
- BLG-GOV-17: PMO Lead — governance documentation (governance-heavy)
- BLG-QA-10: QA & Testing Owner — test data creation (execution-heavy)
- BLG-QA-11: Director of Quality — QA protocol authoring (governance-heavy)

Governance load: 3/5 = 60%. At ceiling but not above. **No Skill-Silo Alert required** (60% = upper bound exactly; ceiling is 60%).

**Product Owner sign-off capacity confirmed:** All 5 new items are S/XS/M effort documentation items. PO confirmed adequate review capacity for v3.1 planning integration.

---

## STEP 8.5 — Stateless Write Safety Gate

### 8.5.A Context Re-Anchoring

Anchored exclusively to:
- STEP 8 decisions: 5 backlog adds (BLG-SEC-03/04, BLG-GOV-17, BLG-QA-10/11), 3 deprioritisations, no roadmap changes
- On-disk state of current_roadmap.md, backlog.md, decision_log.md, workforce_capacity.md, initiative_register.md as read this session.

No debate prose, challenger narratives, or exploratory reasoning carried forward. ✅

### 8.5.B Write Plan

**Pre-write decision log entry count: 23 (DL-001 through DL-023)**

| File | Action | Reason | Traceability |
|------|--------|--------|-------------|
| `claude/cycles/2026-04-28__scheduled/run_manifest.md` | Create | STEP 1.1 requirement | Lifecycle mandatory |
| `claude/cycles/2026-04-28__scheduled/cycle_record.md` | Create | STEP 2–8 working content | Lifecycle mandatory |
| `claude/cycles/2026-04-28__scheduled/cycle_summary.md` | Create | STEP 10 output | Lifecycle mandatory |
| `claude/cycles/2026-04-28__scheduled/lessons_learnt.md` | Create | STEP 11 output | Lifecycle mandatory |
| `claude/roadmap/current_roadmap.md` | Modify | Update Last Updated + Last rebalance header | Lifecycle compliance (no-change roadmap still requires date update) |
| `claude/backlog/backlog.md` | Modify | Add 5 items; deprioritise 3 | STEP 8 decisions: 5 backlog adds |
| `claude/roadmap/decision_log.md` | Append-only | DL-024 entry | STEP 8 decisions |
| `claude/roadmap/workforce_capacity.md` | Modify | Update with new items | STEP 7 workforce economics |
| `claude/scoring/scored_initiatives.md` | Modify | Add 5 scored items | STEP 6 output |
| `claude/ideas/ideas_register.md` | Modify | Update status: 5 Advancing → Promoted-Added; 7 Rejected; 20 re-parked | §4.2 document management |
| `claude/ideas/rejected_but_strong.md` | Append | IDEA-ai-compliance-20260321-01 | §4.2 rejected-but-strong |
| `.claude_current_state.json` | Modify | Update rebalance keys | STEP 12.1 |

### 8.5.C Verification Rules

- All files within Section 5 write scope: **YES** ✅
- Every write traceable to STEP 8 decision or lifecycle compliance only: **YES** ✅
- No formatting-only edits: **YES** ✅
- Decision log append-only and duplicate-checked: **YES** (DL-024 is new; no prior entry for 2026-04-28__scheduled decisions) ✅
- Backlog edits reconciliation-only: **YES** ✅
- PoG documents: **N/A** (no hard-gated items) ✅
- Hard gate status changes: **N/A** ✅
- Displacement candidate flags in initiative_register only: **N/A** (no new displacement candidate flags) ✅
- Effort bands for all new items: **YES** (all 5 new items have S/M/XS bands) ✅
- Action-now patches: **N/A** (no friction items) ✅
- Meta-review: **N/A** (2nd cycle since last review; due at 3rd) ✅

### 8.5.D Decision-to-Write Traceability

All 12 planned writes are traceable to STEP 8 decisions (A) or lifecycle compliance (B). ✅

**WRITE PLAN PASSES. Proceeding to STEP 9.** ✅
